#!/usr/local/bin/python2.6
#
# This file is part of snmpfwd software.
#
# Copyright (c) 2014-2017, Ilya Etingof <etingof@gmail.com>
# License: https://github.com/etingof/snmpfwd/blob/master/LICENSE.txt
#
import os
import sys
import getopt
import traceback
import random
import re
import socket
from pysnmp.error import PySnmpError
from pysnmp.entity import engine, config
from pysnmp.entity.rfc3413 import cmdrsp, ntfrcv, context
from pysnmp.proto.proxy import rfc2576
from pysnmp.carrier.asynsock.dgram import udp
try:
    from pysnmp.carrier.asynsock.dgram import udp6
except ImportError:
    udp6 = None
try:
    from pysnmp.carrier.asynsock.dgram import unix
except ImportError:
    unix = None
from pysnmp.carrier.asynsock.dispatch import AsynsockDispatcher
from pysnmp.proto import rfc1157, rfc1902, rfc1905
from pysnmp.proto.api import v1, v2c
from pyasn1 import debug as pyasn1_debug
from pysnmp import debug as pysnmp_debug
from snmpfwd.error import SnmpfwdError
from snmpfwd import log, daemon, cparser, macro
from snmpfwd.plugins.manager import PluginManager
from snmpfwd.plugins import status
from snmpfwd.trunking.manager import TrunkingManager

# Settings
PROGRAM_NAME = 'snmpfwd-server'
CONFIG_VERSION = '2'
PLUGIN_API_VERSION = 2
CONFIG_FILE = '/usr/local/etc/snmpfwd/server.cfg'

authProtocols = {
  'MD5': config.usmHMACMD5AuthProtocol,
  'SHA': config.usmHMACSHAAuthProtocol,
  'NONE': config.usmNoAuthProtocol
}

privProtocols = {
  'DES': config.usmDESPrivProtocol,
  '3DES': config.usm3DESEDEPrivProtocol,
  'AES': config.usmAesCfb128Protocol,
  'AES128': config.usmAesCfb128Protocol,
  'AES192': config.usmAesCfb192Protocol,
  'AES256': config.usmAesCfb256Protocol,
  'NONE': config.usmNoPrivProtocol
}


def main():
    helpMessage = """\
    Usage: %s [--help]
        [--version ]
        [--debug-snmp=<%s>]
        [--debug-asn1=<%s>]
        [--daemonize]
        [--process-user=<uname>] [--process-group=<gname>]
        [--pid-file=<file>]
        [--logging-method=<%s[:args>]>]
        [--config-file=<file>]""" % (
            sys.argv[0],
            '|'.join([x for x in pysnmp_debug.flagMap.keys() if x != 'mibview']),
            '|'.join([x for x in pyasn1_debug.flagMap.keys()]),
            '|'.join(log.gMap.keys())
        )

    try:
        opts, params = getopt.getopt(sys.argv[1:], 'hv', [
            'help', 'version', 'debug=', 'debug-snmp=', 'debug-asn1=', 'daemonize',
            'process-user=', 'process-group=', 'pid-file=', 'logging-method=',
            'config-file='
        ])

    except Exception:
        sys.stderr.write('ERROR: %s\r\n%s\r\n' % (sys.exc_info()[1], helpMessage))
        sys.exit(-1)

    if params:
        sys.stderr.write('ERROR: extra arguments supplied %s\r\n%s\r\n' % (params, helpMessage))
        sys.exit(-1)

    pidFile = ''
    cfgFile = CONFIG_FILE
    foregroundFlag = True
    procUser = procGroup = None

    for opt in opts:
        if opt[0] == '-h' or opt[0] == '--help':
            sys.stderr.write("""\
    Synopsis:
      SNMP Proxy Forwarder: server part. Receives SNMP requests at one or many
      built-in SNMP Agents and routes them to encrypted trunks established with
      Forwarder's Manager part(s) running elsewhere.
      Can implement complex routing logic through analyzing parts of SNMP messages
      and matching them against proxying rules.
    Documentation:
      http://snmpfwd.sourceforge.net/
    %s
    """ % helpMessage)
            sys.exit(-1)
        if opt[0] == '-v' or opt[0] == '--version':
            import snmpfwd
            import pysnmp
            import pyasn1
            sys.stderr.write("""\
    SNMP Proxy Forwarder version %s, written by Ilya Etingof <etingof@gmail.com>
    Using foundation libraries: pysnmp %s, pyasn1 %s.
    Python interpreter: %s
    Software documentation and support at https://github.com/etingof/snmpfwd
    %s
    """ % (snmpfwd.__version__, hasattr(pysnmp, '__version__') and pysnmp.__version__ or 'unknown', hasattr(pyasn1, '__version__') and pyasn1.__version__ or 'unknown', sys.version, helpMessage))
            sys.exit(-1)
        elif opt[0] == '--debug-snmp':
            pysnmp_debug.setLogger(pysnmp_debug.Debug(*opt[1].split(','), **dict(loggerName=PROGRAM_NAME + '.pysnmp')))
        elif opt[0] == '--debug-asn1':
            pyasn1_debug.setLogger(pyasn1_debug.Debug(*opt[1].split(','), **dict(loggerName=PROGRAM_NAME + '.pyasn1')))
        elif opt[0] == '--daemonize':
            foregroundFlag = False
        elif opt[0] == '--process-user':
            procUser = opt[1]
        elif opt[0] == '--process-group':
            procGroup = opt[1]
        elif opt[0] == '--pid-file':
            pidFile = opt[1]
        elif opt[0] == '--logging-method':
            try:
                log.setLogger(PROGRAM_NAME, *opt[1].split(':'), **dict(force=True))
            except SnmpfwdError:
                sys.stderr.write('%s\r\n%s\r\n' % (sys.exc_info()[1], helpMessage))
                sys.exit(-1)
        elif opt[0] == '--config-file':
            cfgFile = opt[1]

    log.setLogger(PROGRAM_NAME, 'stderr')

    try:
        cfgTree = cparser.Config().load(cfgFile)
    except SnmpfwdError:
        sys.stderr.write('ERROR: %s\r\n%s\r\n' % (sys.exc_info()[1], helpMessage))
        sys.exit(-1)

    if cfgTree.getAttrValue('program-name', '', default=None) != PROGRAM_NAME:
        sys.stderr.write('ERROR: config file %s does not match program name %s\r\n' % (cfgFile, PROGRAM_NAME))
        sys.exit(-1)

    if cfgTree.getAttrValue('config-version', '', default=None) != CONFIG_VERSION:
        sys.stderr.write('ERROR: config file %s version is not compatible with program version %s\r\n' % (cfgFile, CONFIG_VERSION))
        sys.exit(-1)

    random.seed()

    def prettyVarBinds(pdu):
        return not pdu and '<none>' or ';'.join(['%s:%s' % (vb[0].prettyPrint(), vb[1].prettyPrint()) for vb in v2c.apiPDU.getVarBinds(pdu)])

    gCurrentRequestContext = {}

    #
    # SNMPv3 CommandResponder implementation
    #

    class CommandResponder(cmdrsp.CommandResponderBase):
        pduTypes = (rfc1905.SetRequestPDU.tagSet,
                    rfc1905.GetRequestPDU.tagSet,
                    rfc1905.GetNextRequestPDU.tagSet,
                    rfc1905.GetBulkRequestPDU.tagSet)

        def handleMgmtOperation(self, snmpEngine, stateReference, contextName,
                                PDU, acInfo):
            trunkReq = gCurrentRequestContext['request']

            for classifier in ('snmp-credentials-id', 'snmp-context-id', 'snmp-content-id', 'snmp-peer-id'):
                trunkReq['server-' + classifier] = gCurrentRequestContext[classifier]

            logMsg = '(SNMP request %s), matched keys: %s' % (', '.join([x == 'snmp-pdu' and 'snmp-var-binds=%s' % prettyVarBinds(trunkReq['snmp-pdu']) or '%s=%s' % (x, isinstance(trunkReq[x], int) and trunkReq[x] or rfc1902.OctetString(trunkReq[x]).prettyPrint()) for x in trunkReq]), ', '.join(['%s=%s' % (k, gCurrentRequestContext[k]) for k in gCurrentRequestContext if k[-2:] == 'id']))

            pluginIdList = gCurrentRequestContext['plugins-list']
            snmpReqInfo = gCurrentRequestContext['request'].copy()
            reqCtx = {}

            for pluginNum, pluginId in enumerate(pluginIdList):

                st, PDU = pluginManager.processCommandRequest(
                    pluginId, snmpEngine, PDU, snmpReqInfo, reqCtx
                )

                if st == status.BREAK:
                    pluginIdList = pluginIdList[:pluginNum]
                    break

                elif st == status.DROP:
                    log.msg('plugin %s muted request %s' % (pluginId, logMsg))
                    self.releaseStateInformation(stateReference)
                    return

                elif st == status.RESPOND:
                    log.msg('plugin %s forced immediate response %s' % (pluginId, logMsg))
                    self.sendPdu(
                        snmpEngine,
                        stateReference,
                        PDU
                    )
                    self.releaseStateInformation(stateReference)
                    return

            # pass query to trunk

            trunkReq['snmp-pdu'] = PDU
            trunkIdList = gCurrentRequestContext['trunk-id-list']
            if trunkIdList is None:
                log.msg('no route configured %s' % logMsg)
                self.releaseStateInformation(stateReference)
                return

            for trunkId in trunkIdList:
                log.msg('received SNMP message (%s), sending through trunk %s' % (', '.join([x == 'snmp-pdu' and 'snmp-var-binds=%s' % prettyVarBinds(trunkReq['snmp-pdu']) or '%s=%s' % (x, isinstance(trunkReq[x], int) and trunkReq[x] or rfc1902.OctetString(trunkReq[x]).prettyPrint()) for x in trunkReq]), trunkId))

                cbCtx = pluginIdList, trunkId, trunkReq, snmpEngine, stateReference, snmpReqInfo, reqCtx

                trunkingManager.sendReq(trunkId, trunkReq, self.__recvCb, cbCtx)

        def __recvCb(self, trunkRsp, cbCtx):
            pluginIdList, trunkId, trunkReq, snmpEngine, stateReference, snmpReqInfo, reqCtx = cbCtx

            if trunkRsp['error-indication']:
                log.msg('received trunk message through trunk %s, remote end reported error-indication %s, NOT sending response to peer address %s:%s from %s:%s' % (trunkId, trunkRsp['error-indication'], trunkReq['snmp-peer-address'], trunkReq['snmp-peer-port'], trunkReq['snmp-bind-address'], trunkReq['snmp-bind-port']))
            else:
                PDU = trunkRsp['snmp-pdu']
                for pluginId in pluginIdList:
                    st, PDU = pluginManager.processCommandResponse(
                        pluginId, snmpEngine, PDU, snmpReqInfo, reqCtx
                    )

                    if st == status.BREAK:
                        break
                    elif st == status.DROP:
                        log.msg('received trunk message through trunk %s, snmp-var-binds=%s, plugin %s muted response' % (trunkId, prettyVarBinds(PDU), pluginId))
                        self.releaseStateInformation(stateReference)
                        return

                log.msg('received trunk message through trunk %s, sending SNMP response to peer address %s:%s from %s:%s, snmp-var-binds=%s' % (trunkId, trunkReq['snmp-peer-address'], trunkReq['snmp-peer-port'], trunkReq['snmp-bind-address'], trunkReq['snmp-bind-port'], prettyVarBinds(PDU)))

                self.sendPdu(
                    snmpEngine,
                    stateReference,
                    PDU
                )

            self.releaseStateInformation(stateReference)

    #
    # SNMPv3 NotificationReceiver implementation
    #

    class NotificationReceiver(ntfrcv.NotificationReceiver):
        pduTypes = (rfc1157.TrapPDU.tagSet,
                    rfc1905.SNMPv2TrapPDU.tagSet)

        def processPdu(self, snmpEngine, messageProcessingModel,
                       securityModel, securityName, securityLevel,
                       contextEngineId, contextName, pduVersion, PDU,
                       maxSizeResponseScopedPDU, stateReference):

            trunkReq = gCurrentRequestContext['request']

            for classifier in ('snmp-credentials-id', 'snmp-context-id', 'snmp-content-id', 'snmp-peer-id'):
                trunkReq['server-' + classifier] = gCurrentRequestContext[classifier]

            if messageProcessingModel == 0:
                PDU = rfc2576.v1ToV2(PDU)

                # TODO: why this is not automatic?
                v2c.apiTrapPDU.setDefaults(PDU)

            trunkReq['snmp-pdu'] = PDU

            logMsg = '(SNMP notification %s), matched keys: %s' % (', '.join([x == 'snmp-pdu' and 'snmp-var-binds=%s' % prettyVarBinds(trunkReq['snmp-pdu']) or '%s=%s' % (x, isinstance(trunkReq[x], int) and trunkReq[x] or rfc1902.OctetString(trunkReq[x]).prettyPrint()) for x in trunkReq]), ', '.join(['%s=%s' % (k, gCurrentRequestContext[k]) for k in gCurrentRequestContext if k[-2:] == 'id']))

            pluginIdList = gCurrentRequestContext['plugins-list']
            snmpReqInfo = gCurrentRequestContext['request'].copy()
            reqCtx = {}

            for pluginNum, pluginId in enumerate(pluginIdList):

                st, PDU = pluginManager.processNotificationRequest(
                    pluginId, snmpEngine, PDU, snmpReqInfo, reqCtx
                )

                if st == status.BREAK:
                    pluginIdList = pluginIdList[:pluginNum]
                    break

                elif st == status.DROP:
                    log.msg('plugin %s muted request %s' % (pluginId, logMsg))
                    return

                elif st == status.RESPOND:
                    log.msg('plugin %s NOT forced immediate response %s' % (pluginId, logMsg))
                    # TODO: implement immediate response for confirmed-class PDU
                    return

            # pass query to trunk

            trunkIdList = gCurrentRequestContext['trunk-id-list']
            if trunkIdList is None:
                log.msg('no route configured %s' % logMsg)
                return

            for trunkId in trunkIdList:
                log.msg('received SNMP message (%s), sending through trunk %s' % (', '.join([x == 'snmp-pdu' and 'snmp-var-binds=%s' % prettyVarBinds(trunkReq['snmp-pdu']) or '%s=%s' % (x, isinstance(trunkReq[x], int) and trunkReq[x] or rfc1902.OctetString(trunkReq[x]).prettyPrint()) for x in trunkReq]), trunkId))

                # TODO: pass messageProcessingModel to respond
                cbCtx = pluginIdList, trunkId, trunkReq, snmpEngine, stateReference, snmpReqInfo, reqCtx

                trunkingManager.sendReq(trunkId, trunkReq, self.__recvCb, cbCtx)

        def __recvCb(self, trunkRsp, cbCtx):
            pluginIdList, trunkId, trunkReq, snmpEngine, stateReference, snmpReqInfo, reqCtx = cbCtx

            if trunkRsp['error-indication']:
                log.msg('received trunk message through trunk %s, remote end reported error-indication %s, NOT sending response to peer address %s:%s from %s:%s' % (trunkId, trunkRsp['error-indication'], trunkReq['snmp-peer-address'], trunkReq['snmp-peer-port'], trunkReq['snmp-bind-address'], trunkReq['snmp-bind-port']))
            else:
                if 'snmp-pdu' not in trunkRsp:
                    log.msg('received trunk message through trunk %s, unconfirmed SNMP message originally from peer address %s:%s towards %s:%s' % (trunkId, trunkReq['snmp-peer-address'], trunkReq['snmp-peer-port'], trunkReq['snmp-bind-address'], trunkReq['snmp-bind-port']))
                    return

                PDU = trunkRsp['snmp-pdu']

                for pluginId in pluginIdList:
                    st, PDU = pluginManager.processNotificationResponse(
                        pluginId, snmpEngine, PDU, snmpReqInfo, reqCtx
                    )

                    if st == status.BREAK:
                        break
                    elif st == status.DROP:
                        log.msg('received trunk message through trunk %s, snmp-var-binds=%s, plugin %s muted response' % (trunkId, prettyVarBinds(PDU), pluginId))
                        return

                log.msg('received trunk message through trunk %s, sending SNMP response to peer address %s:%s from %s:%s, snmp-var-binds=%s' % (trunkId, trunkReq['snmp-peer-address'], trunkReq['snmp-peer-port'], trunkReq['snmp-bind-address'], trunkReq['snmp-bind-port'], prettyVarBinds(PDU)))

                # TODO: implement response part

                # # Agent-side API complies with SMIv2
                # if messageProcessingModel == 0:
                #     PDU = rfc2576.v2ToV1(PDU, origPdu)
                #
                # statusInformation = {}
                #
                # # 3.4.3
                # try:
                #     snmpEngine.msgAndPduDsp.returnResponsePdu(
                #         snmpEngine, messageProcessingModel, securityModel,
                #         securityName, securityLevel, contextEngineId,
                #         contextName, pduVersion, rspPDU, maxSizeResponseScopedPDU,
                #         stateReference, statusInformation)
                #
                # except error.StatusInformation:
                #         log.msg('processPdu: stateReference %s, statusInformation %s' % (stateReference, sys.exc_info()[1]))

    credIdMap = {}
    peerIdMap = {}
    contextIdList = []
    contentIdList = []
    pluginIdMap = {}
    trunkIdMap = {}
    engineIdMap = {}

    transportDispatcher = AsynsockDispatcher()
    transportDispatcher.registerRoutingCbFun(lambda td, t, d: td)
    transportDispatcher.setSocketMap()  # use global asyncore socket map

    snmpPduTypesMap = {
        rfc1905.GetRequestPDU.tagSet: 'GET',
        rfc1905.SetRequestPDU.tagSet: 'SET',
        rfc1905.GetNextRequestPDU.tagSet: 'GETNEXT',
        rfc1905.GetBulkRequestPDU.tagSet: 'GETBULK',
        rfc1905.ResponsePDU.tagSet: 'RESPONSE',
        rfc1157.TrapPDU.tagSet: 'TRAPv1',
        rfc1905.SNMPv2TrapPDU.tagSet: 'TRAPv2'
    }

    def requestObserver(snmpEngine, execpoint, variables, cbCtx):
        msg = {
            'snmp-engine-id': snmpEngine.snmpEngineID,
            'snmp-transport-domain': variables['transportDomain'],
            'snmp-peer-address': variables['transportAddress'][0],
            'snmp-peer-port': variables['transportAddress'][1],
            'snmp-bind-address': variables['transportAddress'].getLocalAddress()[0],
            'snmp-bind-port': variables['transportAddress'].getLocalAddress()[1],
            'snmp-security-model': variables['securityModel'],
            'snmp-security-level': variables['securityLevel'],
            'snmp-security-name': variables['securityName'],
            'snmp-context-engine-id': variables['contextEngineId'],
            'snmp-context-name': variables['contextName']
        }

        cbCtx['snmp-credentials-id'] = macro.expandMacro(
            credIdMap.get(
                (str(snmpEngine.snmpEngineID),
                 variables['transportDomain'],
                 variables['securityModel'],
                 variables['securityLevel'],
                 str(variables['securityName']))
            ),
            msg
        )

        k = '#'.join([str(x) for x in (variables['contextEngineId'], variables['contextName'])])
        for x, y in contextIdList:
            if y.match(k):
                cbCtx['snmp-context-id'] = macro.expandMacro(x, msg)
                break
            else:
                cbCtx['snmp-context-id'] = None

        addr = '%s:%s#%s:%s' % (variables['transportAddress'][0], variables['transportAddress'][1], variables['transportAddress'].getLocalAddress()[0], variables['transportAddress'].getLocalAddress()[1])

        for pat, peerId in peerIdMap.get(str(variables['transportDomain']), ()):
            if pat.match(addr):
                cbCtx['snmp-peer-id'] = macro.expandMacro(peerId, msg)
                break
        else:
            cbCtx['snmp-peer-id'] = None

        pdu = variables['pdu']
        if pdu.tagSet in v1.TrapPDU.tagSet:
            apiPDU = v1.apiTrapPDU
        else:
            apiPDU = v2c.apiPDU

        k = '#'.join(
            [snmpPduTypesMap.get(variables['pdu'].tagSet, '?'),
             '|'.join([str(x[0]) for x in apiPDU.getVarBinds(variables['pdu'])])]
        )

        for x, y in contentIdList:
            if y.match(k):
                cbCtx['snmp-content-id'] = macro.expandMacro(x, msg)
                break
            else:
                cbCtx['snmp-content-id'] = None

        cbCtx['plugins-list'] = pluginIdMap.get(
            (cbCtx['snmp-credentials-id'],
             cbCtx['snmp-context-id'],
             cbCtx['snmp-peer-id'],
             cbCtx['snmp-content-id']), []
        )
        cbCtx['trunk-id-list'] = trunkIdMap.get(
            (cbCtx['snmp-credentials-id'],
             cbCtx['snmp-context-id'],
             cbCtx['snmp-peer-id'],
             cbCtx['snmp-content-id'])
        )
        cbCtx['request'] = msg

    pluginManager = PluginManager(
        macro.expandMacros(
            cfgTree.getAttrValue('plugin-modules-path-list', '', default=[], vector=True),
            {'config-dir': os.path.dirname(cfgFile)}
        ),
        progId=PROGRAM_NAME,
        apiVer=PLUGIN_API_VERSION
    )

    for pluginCfgPath in cfgTree.getPathsToAttr('plugin-id'):
        pluginId = cfgTree.getAttrValue('plugin-id', *pluginCfgPath)
        pluginMod = cfgTree.getAttrValue('plugin-module', *pluginCfgPath)
        pluginOptions = macro.expandMacro(
            cfgTree.getAttrValue('plugin-options', *pluginCfgPath, **dict(default='')),
            {'config-dir': os.path.dirname(cfgFile)}
        )

        log.msg('configuring plugin ID %s (at %s) from module %s with options %s...' % (pluginId, '.'.join(pluginCfgPath), pluginMod, pluginOptions or '<none>'))
        try:
            pluginManager.loadPlugin(pluginId, pluginMod, pluginOptions)

        except SnmpfwdError:
            log.msg('ERROR: plugin %s not loaded: %s' % (pluginId, sys.exc_info()[1]))
            sys.exit(-1)

    for configEntryPath in cfgTree.getPathsToAttr('snmp-credentials-id'):
        credId = cfgTree.getAttrValue('snmp-credentials-id', *configEntryPath)
        configKey = []
        log.msg('configuring snmp-credentials %s (at %s)...' % (credId, '.'.join(configEntryPath)))

        engineId = cfgTree.getAttrValue('snmp-engine-id', *configEntryPath)

        if engineId in engineIdMap:
            snmpEngine, snmpContext, snmpEngineMap = engineIdMap[engineId]
            log.msg('using engine-id %s' % snmpEngine.snmpEngineID.prettyPrint())
        else:
            snmpEngine = engine.SnmpEngine(snmpEngineID=engineId)
            snmpContext = context.SnmpContext(snmpEngine)
            snmpEngineMap = {
                'transportDomain': {},
                'securityName': {}
            }

            snmpEngine.observer.registerObserver(
                requestObserver,
                'rfc3412.receiveMessage:request',
                cbCtx=gCurrentRequestContext
            )

            CommandResponder(snmpEngine, snmpContext)

            NotificationReceiver(snmpEngine, None)

            engineIdMap[engineId] = snmpEngine, snmpContext, snmpEngineMap

            log.msg('new engine-id %s' % snmpEngine.snmpEngineID.prettyPrint())

        configKey.append(str(snmpEngine.snmpEngineID))

        transportDomain = cfgTree.getAttrValue('snmp-transport-domain', *configEntryPath)
        transportDomain = rfc1902.ObjectName(transportDomain)

        if transportDomain in snmpEngineMap['transportDomain']:
            h, p, transportDomain = snmpEngineMap['transportDomain'][transportDomain]
            log.msg('using transport endpoint %s:%s, transport ID %s' % (h, p, transportDomain))
        else:
            if transportDomain[:len(udp.domainName)] == udp.domainName:
                transport = udp.UdpTransport()
            elif transportDomain[:len(udp6.domainName)] == udp6.domainName:
                transport = udp6.Udp6Transport()
            else:
                log.msg('unknown transport domain %s' % (transportDomain,))
                sys.exit(-1)

            h, p = cfgTree.getAttrValue('snmp-bind-address', *configEntryPath).split(':', 1)

            snmpEngine.registerTransportDispatcher(
                transportDispatcher, transportDomain
            )

            transportOptions = cfgTree.getAttrValue('snmp-transport-options', *configEntryPath, **dict(default=[], vector=True))

            t = transport.openServerMode((h, int(p)))

            if 'transparent-proxy' in transportOptions:
                t.enablePktInfo()
                t.enableTransparent()
            elif 'virtual-interface' in transportOptions:
                t.enablePktInfo()

            config.addSocketTransport(snmpEngine, transportDomain, t)

            snmpEngineMap['transportDomain'][transportDomain] = h, p, transportDomain
            log.msg('new transport endpoint %s:%s, options %s, transport ID %s' % (h, p, transportOptions and '/'.join(transportOptions) or '<none>', transportDomain))

        configKey.append(transportDomain)

        securityModel = cfgTree.getAttrValue('snmp-security-model', *configEntryPath)
        securityModel = rfc1902.Integer(securityModel)
        securityLevel = cfgTree.getAttrValue('snmp-security-level', *configEntryPath)
        securityLevel = rfc1902.Integer(securityLevel)
        securityName = cfgTree.getAttrValue('snmp-security-name', *configEntryPath)

        if securityModel in (1, 2):
            if securityName in snmpEngineMap['securityName']:
                if snmpEngineMap['securityName'][securityModel] == securityModel:
                    log.msg('using security-name %s' % securityName)
                else:
                    raise SnmpfwdError('snmp-security-name %s already in use at snmp-security-model %s' % (securityName, securityModel))
            else:
                communityName = cfgTree.getAttrValue('snmp-community-name', *configEntryPath)
                config.addV1System(snmpEngine, securityName, communityName,
                                   securityName=securityName)
                log.msg('new community-name %s, security-model %s, security-name %s, security-level %s' % (communityName, securityModel, securityName, securityLevel))
                snmpEngineMap['securityName'][securityName] = securityModel

            configKey.append(securityModel)
            configKey.append(securityLevel)
            configKey.append(securityName)

        elif securityModel == 3:
            if securityName in snmpEngineMap['securityName']:
                log.msg('using USM security-name: %s' % securityName)
            else:
                usmUser = cfgTree.getAttrValue('snmp-usm-user', *configEntryPath)
                log.msg('new USM user %s, security-model %s, security-level %s, security-name %s' % (usmUser, securityModel, securityLevel, securityName))

                if securityLevel in (2, 3):
                    usmAuthProto = cfgTree.getAttrValue('snmp-usm-auth-protocol', *configEntryPath, **dict(default=config.usmHMACMD5AuthProtocol))
                    usmAuthProto = rfc1902.ObjectName(usmAuthProto)
                    usmAuthKey = cfgTree.getAttrValue('snmp-usm-auth-key', *configEntryPath)
                    log.msg('new USM authentication key: %s, authentication protocol: %s' % (usmAuthKey, usmAuthProto))

                    if securityLevel == 3:
                        usmPrivProto = cfgTree.getAttrValue('snmp-usm-priv-protocol', *configEntryPath, **dict(default=config.usmDESPrivProtocol))
                        usmPrivProto = rfc1902.ObjectName(usmPrivProto)
                        usmPrivKey = cfgTree.getAttrValue('snmp-usm-priv-key', *configEntryPath, **dict(default=None))
                        log.msg('new USM encryption key: %s, encryption protocol: %s' % (usmPrivKey, usmPrivProto))

                        config.addV3User(
                            snmpEngine, usmUser,
                            usmAuthProto, usmAuthKey,
                            usmPrivProto, usmPrivKey
                        )

                    else:
                        config.addV3User(snmpEngine, usmUser, usmAuthProto, usmAuthKey)

                else:
                    config.addV3User(snmpEngine, usmUser)

                snmpEngineMap['securityName'][securityName] = securityModel


            configKey.append(securityModel)
            configKey.append(securityLevel)
            configKey.append(securityName)

        else:
            raise SnmpfwdError('unknown snmp-security-model: %s' % securityModel)

        configKey = tuple(configKey)
        if configKey in credIdMap:
            log.msg('ambiguous configuration for key snmp-credentials-id=%s at %s' % (credId, '.'.join(configEntryPath)))
            sys.exit(-1)

        credIdMap[configKey] = credId

    duplicates = {}

    for peerCfgPath in cfgTree.getPathsToAttr('snmp-peer-id'):
        peerId = cfgTree.getAttrValue('snmp-peer-id', *peerCfgPath)
        if peerId in duplicates:
            log.msg('duplicate snmp-peer-id=%s at %s and %s' % (peerId, '.'.join(peerCfgPath), '.'.join(duplicates[peerId])))
            sys.exit(-1)

        duplicates[peerId] = peerCfgPath

        log.msg('configuring peer ID %s (at %s)...' % (peerId, '.'.join(peerCfgPath)))
        transportDomain = cfgTree.getAttrValue('snmp-transport-domain', *peerCfgPath)
        if transportDomain not in peerIdMap:
            peerIdMap[transportDomain] = []
        for peerAddress in cfgTree.getAttrValue('snmp-peer-address-pattern-list', *peerCfgPath, **dict(vector=True)):
            for bindAddress in cfgTree.getAttrValue('snmp-bind-address-pattern-list', *peerCfgPath, **dict(vector=True)):
                peerIdMap[transportDomain].append(
                    (re.compile(peerAddress+'#'+bindAddress), peerId)
                )

    duplicates = {}

    for contextCfgPath in cfgTree.getPathsToAttr('snmp-context-id'):
        contextId = cfgTree.getAttrValue('snmp-context-id', *contextCfgPath)
        if contextId in duplicates:
            log.msg('duplicate snmp-context-id=%s at %s and %s' % (contextId, '.'.join(contextCfgPath), '.'.join(duplicates[contextId])))
            sys.exit(-1)

        duplicates[contextId] = contextCfgPath

        k = '#'.join(
            (cfgTree.getAttrValue('snmp-context-engine-id-pattern', *contextCfgPath),
             cfgTree.getAttrValue('snmp-context-name-pattern', *contextCfgPath))
        )

        log.msg('configuring context ID %s (at %s), composite key: %s' % (contextId, '.'.join(contextCfgPath), k))

        contextIdList.append((contextId, re.compile(k)))

    duplicates = {}

    for contentCfgPath in cfgTree.getPathsToAttr('snmp-content-id'):
        contentId = cfgTree.getAttrValue('snmp-content-id', *contentCfgPath)
        if contentId in duplicates:
            log.msg('duplicate snmp-content-id=%s at %s and %s' % (contentId, '.'.join(contentCfgPath), '.'.join(duplicates[contentId])))
            sys.exit(-1)

        duplicates[contentId] = contentCfgPath

        for x in cfgTree.getAttrValue('snmp-pdu-oid-prefix-pattern-list', *contentCfgPath, **dict(vector=True)):
            k = '#'.join([cfgTree.getAttrValue('snmp-pdu-type-pattern', *contentCfgPath), x])

            log.msg('configuring content ID %s (at %s), composite key: %s' % (contentId, '.'.join(contentCfgPath), k))

            contentIdList.append((contentId, re.compile(k)))

    del duplicates

    for pluginCfgPath in cfgTree.getPathsToAttr('using-plugin-id-list'):
        pluginIdList = cfgTree.getAttrValue('using-plugin-id-list', *pluginCfgPath, **dict(vector=True))
        log.msg('configuring plugin ID(s) %s (at %s)...' % (','.join(pluginIdList), '.'.join(pluginCfgPath)))
        for credId in cfgTree.getAttrValue('matching-snmp-credentials-id-list', *pluginCfgPath, **dict(vector=True)):
            for peerId in cfgTree.getAttrValue('matching-snmp-peer-id-list', *pluginCfgPath, **dict(vector=True)):
                for contextId in cfgTree.getAttrValue('matching-snmp-context-id-list', *pluginCfgPath, **dict(vector=True)):
                    for contentId in cfgTree.getAttrValue('matching-snmp-content-id-list', *pluginCfgPath, **dict(vector=True)):
                        k = credId, contextId, peerId, contentId
                        if k in pluginIdMap:
                            log.msg('duplicate snmp-credentials-id %s, snmp-context-id %s, snmp-peer-id %s, snmp-content-id %s at plugin-id(s) %s' % (credId, contextId, peerId, contentId, ','.join(pluginIdList)))
                            sys.exit(-1)
                        else:
                            log.msg('configuring plugin(s) %s (at %s), composite key: %s' % (','.join(pluginIdList), '.'.join(pluginCfgPath), '/'.join(k)))

                            for pluginId in pluginIdList:
                                if not pluginManager.hasPlugin(pluginId):
                                    log.msg('ERROR: undefined plugin ID %s referenced at %s' % (pluginId, '.'.join(pluginCfgPath)))
                                    sys.exit(-1)

                            pluginIdMap[k] = pluginIdList

    for routeCfgPath in cfgTree.getPathsToAttr('using-trunk-id-list'):
        trunkIdList = cfgTree.getAttrValue('using-trunk-id-list', *routeCfgPath, **dict(vector=True))
        log.msg('configuring destination trunk ID(s) %s (at %s)...' % (','.join(trunkIdList), '.'.join(routeCfgPath)))
        for credId in cfgTree.getAttrValue('matching-snmp-credentials-id-list', *routeCfgPath, **dict(vector=True)):
            for peerId in cfgTree.getAttrValue('matching-snmp-peer-id-list', *routeCfgPath, **dict(vector=True)):
                for contextId in cfgTree.getAttrValue('matching-snmp-context-id-list', *routeCfgPath, **dict(vector=True)):
                    for contentId in cfgTree.getAttrValue('matching-snmp-content-id-list', *routeCfgPath, **dict(vector=True)):
                        k = credId, contextId, peerId, contentId
                        if k in trunkIdMap:
                            log.msg('duplicate snmp-credentials-id %s, snmp-context-id %s, snmp-peer-id %s, snmp-content-id %s at trunk-id(s) %s' % (credId, contextId, peerId, contentId, ','.join(trunkIdList)))
                            sys.exit(-1)
                        else:
                            trunkIdMap[k] = trunkIdList

                        log.msg('configuring trunk routing to %s (at %s), composite key: %s' % (','.join(trunkIdList), '.'.join(routeCfgPath), '/'.join(k)))

    def dataCbFun(trunkId, msgId, msg):
        log.msg('message ID %s received from trunk %s' % (msgId, trunkId))

    trunkingManager = TrunkingManager(dataCbFun)

    def getTrunkAddr(a, port=0):
        f = lambda h, p=port: (h, int(p))
        try:
            return f(*a.split(':'))

        except Exception:
            raise SnmpfwdError('improper IPv4 endpoint %s' % a)

    for trunkCfgPath in cfgTree.getPathsToAttr('trunk-id'):
        trunkId = cfgTree.getAttrValue('trunk-id', *trunkCfgPath)
        secret = cfgTree.getAttrValue('trunk-crypto-key', *trunkCfgPath, **dict(default=''))
        secret = secret and (secret*((16//len(secret))+1))[:16]
        log.msg('configuring trunk ID %s (at %s)...' % (trunkId, '.'.join(trunkCfgPath)))
        connectionMode = cfgTree.getAttrValue('trunk-connection-mode', *trunkCfgPath)
        if connectionMode == 'client':
            trunkingManager.addClient(
                trunkId,
                getTrunkAddr(cfgTree.getAttrValue('trunk-bind-address', *trunkCfgPath)),
                getTrunkAddr(cfgTree.getAttrValue('trunk-peer-address', *trunkCfgPath), 30201),
                cfgTree.getAttrValue('trunk-ping-period', *trunkCfgPath, default=0, expect=int),
                secret
            )
            log.msg('new trunking client from %s to %s' % (cfgTree.getAttrValue('trunk-bind-address', *trunkCfgPath), cfgTree.getAttrValue('trunk-peer-address', *trunkCfgPath)))
        if connectionMode == 'server':
            trunkingManager.addServer(
                getTrunkAddr(cfgTree.getAttrValue('trunk-bind-address', *trunkCfgPath), 30201),
                cfgTree.getAttrValue('trunk-ping-period', *trunkCfgPath, default=0, expect=int),
                secret
            )
            log.msg('new trunking server at %s' % (cfgTree.getAttrValue('trunk-bind-address', *trunkCfgPath)))

    transportDispatcher.registerTimerCbFun(
        trunkingManager.setupTrunks, random.randrange(1, 5)
    )
    transportDispatcher.registerTimerCbFun(
        trunkingManager.monitorTrunks, random.randrange(1, 5)
    )

    try:
        daemon.dropPrivileges(procUser, procGroup)

    except Exception:
        sys.stderr.write('ERROR: cant drop privileges: %s\r\n%s\r\n' % (sys.exc_info()[1], helpMessage))
        sys.exit(-1)

    if not foregroundFlag:
        try:
            daemon.daemonize(pidFile)

        except Exception:
            sys.stderr.write('ERROR: cant daemonize process: %s\r\n%s\r\n' % (sys.exc_info()[1], helpMessage))
            sys.exit(-1)

    # Run mainloop

    log.msg('starting I/O engine...')

    transportDispatcher.jobStarted(1)  # server job would never finish

    # Python 2.4 does not support the "finally" clause

    exc_info = None

    while True:
        try:
            transportDispatcher.runDispatcher()

        except KeyboardInterrupt:
            log.msg('shutting down process...')
            break

        except (PySnmpError, SnmpfwdError, socket.error):
            log.msg('error: %s' % sys.exc_info()[1])
            continue

        except Exception:
            exc_info = sys.exc_info()
            break

    transportDispatcher.closeDispatcher()

    log.msg('process terminated')

    if exc_info:
        for line in traceback.format_exception(*exc_info):
            log.msg(line.replace('\n', ';'))


if __name__ == '__main__':
    main()