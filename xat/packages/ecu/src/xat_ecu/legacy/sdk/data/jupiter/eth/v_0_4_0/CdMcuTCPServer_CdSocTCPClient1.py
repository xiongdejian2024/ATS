

class CCUMCUCDToCCUSOCCDEthSignalIPdu11:
    base_type = "Unsigned"
    client_socket = "SocketCdSocTCPClient1"
    pdu_header_id = 0x20400B
    pdu_length_bytes = 1500
    receiver = ['CCUSOCCD']
    send_type = "EventTriggered"
    sender = "CCUMCUCD"
    server_socket = "SocketCdMcuTCPServer"
    signal_group = {}

    class DKDataUpLink:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Opaque"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "General channel used to send data to Digital Key Service"
        signal_length = 32760
        start_position = 0
        value_definition = {}


class CCUMCUCDToCCUSOCCDEthSignalIPdu16:
    base_type = "Unsigned"
    client_socket = "SocketCdSocTCPClient1"
    pdu_header_id = 0x204010
    pdu_length_bytes = 1500
    receiver = ['CCUSOCCD']
    send_type = "EventTriggered"
    sender = "CCUMCUCD"
    server_socket = "SocketCdMcuTCPServer"
    signal_group = {}

    class DigKeyLogInfo:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Opaque"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "BNCM Log info"
        signal_length = 32760
        start_position = 0
        value_definition = {}


class CCUMCUCDToCCUSOCCDEthSignalIPdu23:
    base_type = "Unsigned"
    client_socket = "SocketCdSocTCPClient1"
    pdu_header_id = 0x204017
    pdu_length_bytes = 1500
    receiver = ['CCUSOCCD']
    send_type = "EventTriggered"
    sender = "CCUMCUCD"
    server_socket = "SocketCdMcuTCPServer"
    signal_group = {}

    class RKEDataUpLink:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Opaque"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "used to send RKE command data to Digital Key Service"
        signal_length = 32760
        start_position = 0
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu02:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402002
    pdu_length_bytes = 5
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'ClimateAirFlwBascCalcn': ['ClimateAirFlwBascCalcnReLe', 'ClimateAirFlwBascCalcnFrntRi', 'ClimateAirFlwBascCalcnFrntLe', 'ClimateAirFlwBascCalcnReRi']}

    class ClimateAirFlwBascCalcnReLe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Climate Rear Left Area Basic Air Flow Calculation Value For Automatic Air Conditioning Algorithm"
        signal_length = 10
        start_position = 19
        value_definition = {}

    class ClimateAirFlwBascCalcnFrntRi:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Climate Front Right Area Basic Air Flow Calculation Value For Automatic Air Conditioning Algorithm"
        signal_length = 10
        start_position = 13
        value_definition = {}

    class ClimateAirFlwBascCalcnFrntLe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Climate Front Left Area Basic Air Flow Calculation Value For Automatic Air Conditioning Algorithm"
        signal_length = 10
        start_position = 7
        value_definition = {}

    class ClimateAirFlwBascCalcnReRi:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Climate Rear Right Area Basic Air Flow Calculation Value For Automatic Air Conditioning Algorithm"
        signal_length = 10
        start_position = 25
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu01:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402001
    pdu_length_bytes = 3
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-1000ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'VehAlti': ['VehAltiAlti', 'VehAltiAltiQf']}

    class VehAltiAlti:
        comments = ""
        factor = 0.1
        initial_value = 1000
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -100
        sig_ub = None
        signal_description = "Vehicle altitude based on Global Location."
        signal_length = 16
        start_position = 7
        value_definition = {}

    class VehAltiAltiQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "The signal quality of the vehicle altitude."
        signal_length = 2
        start_position = 23
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu03:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402003
    pdu_length_bytes = 2
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'CabinControlFlt': ['CabinControlFltCntr', 'CabinControlFltChks', 'CabinControlFltsts']}

    class CabinControlFltCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Counter"
        signal_length = 4
        start_position = 15
        value_definition = {}

    class CabinControlFltChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Checks"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class CabinControlFltsts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "The Cabin Control Chips Status,including MCU And SOC"
        signal_length = 1
        start_position = 11
        value_definition = {'0x0': ' Flt1_NoFault', '0x1': ' Flt1_Fault'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu05:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402005
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class EpbSoftSwt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "epb soft switch"
        signal_length = 3
        start_position = 7
        value_definition = {'0x0': ' EpbSoftSwt_NoReq', '0x1': ' EpbSoftSwt_Apply', '0x2': ' EpbSoftSwt_Release', '0x3': ' EpbSoftSwt_Forbidden', '0x4': ' EpbSoftSwt_Unknown', '0x5': ' EpbSoftSwt_Reserved'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu06:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402006
    pdu_length_bytes = 17
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'LocalCenLockCtrl': ['LocalCenLockCtrlKeyIDByte9', 'LocalCenLockCtrlKeyIDByte0', 'LocalCenLockCtrlKeyIDByte1', 'LocalCenLockCtrlKeyIDByte15', 'LocalCenLockCtrlKeyIDByte3', 'LocalCenLockCtrlKeyIDByte5', 'LocalCenLockCtrlKeyIDByte10', 'LocalCenLockCtrlKeyIDByte8', 'LocalCenLockCtrlKeyIDByte4', 'LocalCenLockCtrlLockCmdTrigSrc', 'LocalCenLockCtrlKeyIDByte6', 'LocalCenLockCtrlKeyIDByte14', 'LocalCenLockCtrlKeyIDByte11', 'LocalCenLockCtrlKeyIDByte2', 'LocalCenLockCtrlKeyIDByte7', 'LocalCenLockCtrlKeyIDByte13', 'LocalCenLockCtrlKeyIDByte12', 'LocalCenLockCtrlCentralLockCmd']}

    class LocalCenLockCtrlKeyIDByte9:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Central Lock KeyID"
        signal_length = 8
        start_position = 103
        value_definition = {}

    class LocalCenLockCtrlKeyIDByte0:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Central Lock KeyID"
        signal_length = 8
        start_position = 31
        value_definition = {}

    class LocalCenLockCtrlKeyIDByte1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Central Lock KeyID"
        signal_length = 8
        start_position = 39
        value_definition = {}

    class LocalCenLockCtrlKeyIDByte15:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Central Lock KeyID"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class LocalCenLockCtrlKeyIDByte3:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Central Lock KeyID"
        signal_length = 8
        start_position = 55
        value_definition = {}

    class LocalCenLockCtrlKeyIDByte5:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Central Lock KeyID"
        signal_length = 8
        start_position = 71
        value_definition = {}

    class LocalCenLockCtrlKeyIDByte10:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Central Lock KeyID"
        signal_length = 8
        start_position = 111
        value_definition = {}

    class LocalCenLockCtrlKeyIDByte8:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Central Lock KeyID"
        signal_length = 8
        start_position = 95
        value_definition = {}

    class LocalCenLockCtrlKeyIDByte4:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Central Lock KeyID"
        signal_length = 8
        start_position = 63
        value_definition = {}

    class LocalCenLockCtrlLockCmdTrigSrc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Trigger source of Central Lock Command"
        signal_length = 4
        start_position = 3
        value_definition = {'0x0': ' LockCmdTrigSrc_No_TrigSrc', '0x1': ' LockCmdTrigSrc_RKE_Outd', '0x2': ' LockCmdTrigSrc_Tele_Outd', '0x3': ' LockCmdTrigSrc_OutdVoice', '0x4': ' LockCmdTrigSrc_OutdLockCtrl', '0x5': ' LockCmdTrigSrc_AutoRelock', '0x6': ' LockCmdTrigSrc_InsdVoice', '0x7': ' LockCmdTrigSrc_GearPUnlock', '0x8': ' LockCmdTrigSrc_HMI', '0x9': ' LockCmdTrigSrc_RKE_Insd', '0xA': ' LockCmdTrigSrc_Tele_Insd', '0xB': ' LockCmdTrigSrc_SpdLock', '0xC': ' LockCmdTrigSrc_InsdLockCtrl'}

    class LocalCenLockCtrlKeyIDByte6:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Central Lock KeyID"
        signal_length = 8
        start_position = 79
        value_definition = {}

    class LocalCenLockCtrlKeyIDByte14:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Central Lock KeyID"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class LocalCenLockCtrlKeyIDByte11:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Central Lock KeyID"
        signal_length = 8
        start_position = 119
        value_definition = {}

    class LocalCenLockCtrlKeyIDByte2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Central Lock KeyID"
        signal_length = 8
        start_position = 47
        value_definition = {}

    class LocalCenLockCtrlKeyIDByte7:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Central Lock KeyID"
        signal_length = 8
        start_position = 87
        value_definition = {}

    class LocalCenLockCtrlKeyIDByte13:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Central Lock KeyID"
        signal_length = 8
        start_position = 135
        value_definition = {}

    class LocalCenLockCtrlKeyIDByte12:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Central Lock KeyID"
        signal_length = 8
        start_position = 127
        value_definition = {}

    class LocalCenLockCtrlCentralLockCmd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "central lock Cmd"
        signal_length = 2
        start_position = 5
        value_definition = {'0x0': ' CenLockCmd_Idle', '0x1': ' CenLockCmd_CenLockCmd', '0x2': ' CenLockCmd_CenUnLckCmd', '0x3': ' CenLockCmd_TrunkUnlckCmd'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu07:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402007
    pdu_length_bytes = 1500
    receiver = ['CCUMCUCD']
    send_type = "EventTriggered"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class BLEVehDataUpd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Opaque"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Send RVS data through BLE channel"
        signal_length = 32760
        start_position = 0
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu08:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402008
    pdu_length_bytes = 1500
    receiver = ['CCUMCUCD']
    send_type = "EventTriggered"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class DKDataDwnLink:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Opaque"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "General data channel sent from Digital Key Service to MCU"
        signal_length = 32760
        start_position = 0
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu09:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402009
    pdu_length_bytes = 26
    receiver = ['CCUMCUCD']
    send_type = "EventTriggered"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'LoadPwrProxyReq': ['LoadPwrProxyReqReserved16', 'LoadPwrProxyReqSODLPwrProxyReq', 'LoadPwrProxyReqSRSPwrProxyReq', 'LoadPwrProxyReqAWMPwrProxyReq', 'LoadPwrProxyReqReserved8', 'LoadPwrProxyReqEGSMPwrProxyReq', 'LoadPwrProxyReqReserved2', 'LoadPwrProxyReqLCTVPwrProxyReq', 'LoadPwrProxyReqPORPwrProxyReq', 'LoadPwrProxyReqEPMPwrProxyReq', 'LoadPwrProxyReqReserved14', 'LoadPwrProxyReqDRMRRPwrProxyReq', 'LoadPwrProxyReqSCMRPwrProxyReq', 'LoadPwrProxyReqHVCMPwrProxyReq', 'LoadPwrProxyReqWERVPwrProxyReq', 'LoadPwrProxyReqPMSIPwrProxyReq', 'LoadPwrProxyReqOPCRPwrProxyReq', 'LoadPwrProxyReqBCTVPwrProxyReq', 'LoadPwrProxyReqCRCMPwrProxyReq', 'LoadPwrProxyReqHVCHPwrProxyReq', 'LoadPwrProxyReqHUBRPwrProxyReq', 'LoadPwrProxyReqUSBR2PwrProxyReq', 'LoadPwrProxyReqFLRPwrProxyReq', 'LoadPwrProxyReqPOFPwrProxyReq', 'LoadPwrProxyReqNKRPwrProxyReq', 'LoadPwrProxyReqOHCPwrProxyReq', 'LoadPwrProxyReqOPCFPwrProxyReq', 'LoadPwrProxyReqMGMPwrProxyReq', 'LoadPwrProxyReqDCTVPwrProxyReq', 'LoadPwrProxyReqCCTVPwrProxyReq', 'LoadPwrProxyReqLPODPwrProxyReq', 'LoadPwrProxyReqRCMRPwrProxyReq', 'LoadPwrProxyReqReserved9', 'LoadPwrProxyReqHCTVPwrProxyReq', 'LoadPwrProxyReqReserved1', 'LoadPwrProxyReqAGUPwrProxyReq', 'LoadPwrProxyReqReserved7', 'LoadPwrProxyReqACCMPwrProxyReq', 'LoadPwrProxyReqBEXVPwrProxyReq', 'LoadPwrProxyReqFEXVPwrProxyReq', 'LoadPwrProxyReqMMPPwrProxyReq', 'LoadPwrProxyReqDRMFRPwrProxyReq', 'LoadPwrProxyReqPPODPwrProxyReq', 'LoadPwrProxyReqCDPwrProxyReq', 'LoadPwrProxyReqFSRRPwrProxyReq', 'LoadPwrProxyReqRMLPwrProxyReq', 'LoadPwrProxyReqIRMMPwrProxyReq', 'LoadPwrProxyReqDICPwrProxyReq', 'LoadPwrProxyReqVCUPwrProxyReq', 'LoadPwrProxyReqMMDPwrProxyReq', 'LoadPwrProxyReqHBMRPwrProxyReq', 'LoadPwrProxyReqBoosterBlowerPwrProxyReq', 'LoadPwrProxyReqSWTLPwrProxyReq', 'LoadPwrProxyReqSWTRPwrProxyReq', 'LoadPwrProxyReqDRMFLPwrProxyReq', 'LoadPwrProxyReqUWBPwrProxyReq', 'LoadPwrProxyReqAFUPwrProxyReq', 'LoadPwrProxyReqHODPwrProxyReq', 'LoadPwrProxyReqALMLPwrProxyReq', 'LoadPwrProxyReqSODRPwrProxyReq', 'LoadPwrProxyReqAGMPwrProxyReq', 'LoadPwrProxyReqReserved12', 'LoadPwrProxyReqBCFVPwrProxyReq', 'LoadPwrProxyReqWPCPwrProxyReq', 'LoadPwrProxyReqHCCPPwrProxyReq', 'LoadPwrProxyReqReserved13', 'LoadPwrProxyReqReserved6', 'LoadPwrProxyReqRSOV1PwrProxyReq', 'LoadPwrProxyReqUSBR1PwrProxyReq', 'LoadPwrProxyReqReserved5', 'LoadPwrProxyReqHUBFPwrProxyReq', 'LoadPwrProxyReqReserved3', 'LoadPwrProxyReqFCSIPwrProxyReq', 'LoadPwrProxyReqHCMRPwrProxyReq', 'LoadPwrProxyReqRLSMPwrProxyReq', 'LoadPwrProxyReqHVAHPwrProxyReq', 'LoadPwrProxyReqDRFPwrProxyReq', 'LoadPwrProxyReqIEMPwrProxyReq', 'LoadPwrProxyReqDRMRLPwrProxyReq', 'LoadPwrProxyReqRSOV2PwrProxyReq', 'LoadPwrProxyReqReserved10', 'LoadPwrProxyReqBNCMPwrProxyReq', 'LoadPwrProxyReqSCMFPwrProxyReq', 'LoadPwrProxyReqCSOVPwrProxyReq', 'LoadPwrProxyReqEDCPPwrProxyReq', 'LoadPwrProxyReqBCCPPwrProxyReq', 'LoadPwrProxyReqRRMMPwrProxyReq', 'LoadPwrProxyReqECTVPwrProxyReq', 'LoadPwrProxyReqALMRPwrProxyReq', 'LoadPwrProxyReqRLMMPwrProxyReq', 'LoadPwrProxyReqTERVPwrProxyReq', 'LoadPwrProxyReqReserved11', 'LoadPwrProxyReqReserved4', 'LoadPwrProxyReqCERVPwrProxyReq', 'LoadPwrProxyReqREXVPwrProxyReq', 'LoadPwrProxyReqFSRLPwrProxyReq', 'LoadPwrProxyReqReserved15', 'LoadPwrProxyReqHBMFPwrProxyReq', 'LoadPwrProxyReqRPODPwrProxyReq', 'LoadPwrProxyReqDPODPwrProxyReq', 'LoadPwrProxyReqRCMLPwrProxyReq', 'LoadPwrProxyReqHCMLPwrProxyReq', 'LoadPwrProxyReqReserved17', 'LoadPwrProxyReqReserved18']}

    class LoadPwrProxyReqReserved16:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 189
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqSODLPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 147
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqSRSPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 159
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqAWMPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 11
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqReserved8:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 203
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqEGSMPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 63
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqReserved2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 199
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqLCTVPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 101
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqPORPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 127
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqEPMPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 61
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqReserved14:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 177
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqDRMRRPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 53
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqSCMRPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 149
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqHVCMPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 91
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqWERVPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 175
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqPMSIPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 115
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqOPCRPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 117
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqBCTVPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 21
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqCRCMPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 39
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqHVCHPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 93
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqHUBRPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 81
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqUSBR2PwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 165
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqFLRPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 71
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqPOFPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 113
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqNKRPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 107
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqOHCPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 105
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqOPCFPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 119
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqMGMPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 97
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqDCTVPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 35
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqCCTVPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 29
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqLPODPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 99
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqRCMRPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 121
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqReserved9:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 201
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqHCTVPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 87
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqReserved1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 171
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqAGUPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqReserved7:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 205
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqACCMPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqBEXVPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 19
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqFEXVPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 57
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqMMPPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 109
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqDRMFRPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 41
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqPPODPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 125
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqCDPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 27
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqFSRRPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 67
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqRMLPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 129
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqIRMMPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 103
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqDICPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 33
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqVCUPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 161
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqMMDPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 111
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqHBMRPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 79
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqBoosterBlowerPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 31
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqSWTLPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 157
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqSWTRPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 155
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqDRMFLPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 43
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqUWBPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 163
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqAFUPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 5
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqHODPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 85
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqALMLPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 15
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqSODRPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 145
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqAGMPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 3
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqReserved12:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 181
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqBCFVPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 23
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqWPCPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 173
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqHCCPPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 77
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqReserved13:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 179
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqReserved6:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 207
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqRSOV1PwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 139
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqUSBR1PwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 167
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqReserved5:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 193
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqHUBFPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 83
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqReserved3:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 197
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqFCSIPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 59
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqHCMRPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 73
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqRLSMPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 131
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqHVAHPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 95
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqDRFPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 45
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqIEMPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 89
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqDRMRLPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 55
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqRSOV2PwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 137
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqReserved10:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 169
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqBNCMPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 17
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqSCMFPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 151
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqCSOVPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 37
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqEDCPPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 49
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqBCCPPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 9
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqRRMMPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 141
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqECTVPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 51
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqALMRPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 13
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqRLMMPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 133
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqTERVPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 153
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqReserved11:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 183
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqReserved4:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 195
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqCERVPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 25
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqREXVPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 135
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqFSRLPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 69
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqReserved15:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 191
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqHBMFPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 65
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqRPODPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 143
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqDPODPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 47
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqRCMLPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 123
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqHCMLPwrProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 75
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqReserved17:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 187
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class LoadPwrProxyReqReserved18:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Load Power Proxy Request"
        signal_length = 2
        start_position = 185
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu10:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40200A
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "EventTriggered"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class RoofFolderDisplayBrightnessLevelReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "The Brightness of RFD required: 0-100perc"
        signal_length = 8
        start_position = 7
        value_definition = {'0xFF': 'BattSOH_Invalid'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu11:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40200B
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-60ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class DrvModReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Drive Mode Request."
        signal_length = 4
        start_position = 7
        value_definition = {'0x0': ' DrvModReqType_Undefd', '0x1': ' DrvModReqType_ECO', '0x2': ' DrvModReqType_Comfort_Normal', '0x3': ' DrvModReqType_Dynamic_Sport', '0x4': ' DrvModReqType_Tank', '0x5': ' DrvModReqType_Offroad_CrossTerrain', '0x6': ' DrvModReqType_Adaptive', '0x7': ' DrvModReqType_Race', '0x8': ' DrvModReqType_Reserved', '0x9': ' DrvModReqType_ECO_PLUS', '0xA': ' DrvModReqType_Power', '0xB': ' DrvModReqType_Snow', '0xC': ' DrvModReqType_Sand', '0xD': ' DrvModReqType_Mud', '0xE': ' DrvModReqType_Rock', '0xF': ' DrvModReqType_Err'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu16:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402010
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class BrightnessLvlSet:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "The Percent Brightness value Setted By cabin"
        signal_length = 8
        start_position = 7
        value_definition = {'0xFF': 'BattSOH_Invalid'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu25:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402019
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'ChrgSoftSwCtrlSt': ['ChrgSoftSwCtrlStSource', 'ChrgSoftSwCtrlStCmd']}

    class ChrgSoftSwCtrlStSource:
        comments = ""
        factor = 1.0
        initial_value = 15
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Charging soft switch request source"
        signal_length = 4
        start_position = 7
        value_definition = {'0x0': ' HVCmdSource_HMI', '0x1': ' HVCmdSource_APP', '0x2': ' HVCmdSource_HVIntelligentChrgn', '0x3': ' HVCmdSource_Fota', '0x4': ' HVCmdSource_BookChrgn', '0x5': ' HVCmdSource_RemDrv', '0x6': ' HVCmdSource_Therm', '0x7': ' HVCmdSource_Reserved1', '0x8': ' HVCmdSource_Reserved2', '0xF': ' HVCmdSource_Default'}

    class ChrgSoftSwCtrlStCmd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Charging soft-switch request status"
        signal_length = 2
        start_position = 3
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu18:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402012
    pdu_length_bytes = 1027
    receiver = ['CCUMCUCD']
    send_type = "EventTriggered"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'CDSOCDiagDIDInfo': ['CDSOCDiagDIDInfoLength', 'CDSOCDiagDIDInfoDIDCode']}

    class CDSOCDiagDIDInfoLength:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "DID data length"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class CDSOCDiagDIDInfoDIDCode:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "DID Code info"
        signal_length = 16
        start_position = 15
        value_definition = {}

    class CDSOCDiagDIDInfoData:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Opaque"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "DID payload data"
        signal_length = 8192
        start_position = 24
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu15:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40200F
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class AntiFlashFogFlg:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Anti Flash Fog Flag"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' Flg1_Rst', '0x1': ' Flg1_Set'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu12:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40200C
    pdu_length_bytes = 3
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class AmplfrChFltSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Amplifier Channel Fault Status"
        signal_length = 24
        start_position = 7
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu13:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40200D
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class AmplfrFltSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Amplifier Fault Status"
        signal_length = 8
        start_position = 7
        value_definition = {'0x0': ' AmplfrFltSts_Normal', '0x1': ' AmplfrFltSts_Recovering', '0x2': ' AmplfrFltSts_Diagnosing', '0x3': ' AmplfrFltSts_Fault', '0x4': ' AmplfrFltSts_OpenCircuit', '0x5': ' AmplfrFltSts_ShorttoGround', '0x6': ' AmplfrFltSts_ShorttoBattery', '0x7': ' AmplfrFltSts_WrongPort', '0x8': ' AmplfrFltSts_ReverseWire', '0x9': ' AmplfrFltSts_ShortofWires', '0xA': ' AmplfrFltSts_EABOverTemperature', '0xB': ' AmplfrFltSts_EABAbnormalvoltage', '0xFF': ' AmplfrFltSts_Unknown'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu14:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40200E
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'AntiColdFlowFlg': ['AntiColdFlowFlgFrnt', 'AntiColdFlowFlgRe']}

    class AntiColdFlowFlgFrnt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Front Row Anti Clod Air Flow Flag"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' Flg1_Rst', '0x1': ' Flg1_Set'}

    class AntiColdFlowFlgRe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Rear Row Anti Clod Air Flow Flag"
        signal_length = 1
        start_position = 6
        value_definition = {'0x0': ' Flg1_Rst', '0x1': ' Flg1_Set'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu19:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402013
    pdu_length_bytes = 1024
    receiver = ['CCUMCUCD']
    send_type = "EventTriggered"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class CDSOCDiagDTCInfoData:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Opaque"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "DTC payload data"
        signal_length = 8192
        start_position = 0
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu17:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402011
    pdu_length_bytes = 1024
    receiver = ['CCUMCUCD']
    send_type = "EventTriggered"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class CDSOC2CDMCUDummyData:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Opaque"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Dynamic array for backup use between CDMCU & CDSOC"
        signal_length = 8192
        start_position = 0
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu27:
    base_type = "Boolean"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40201B
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'VisFusnSeatRes': ['VisFusnSeatResDrvrSeatSts', 'VisFusnSeatResThrdRowMidSeatSts', 'VisFusnSeatResThrdRowLeSeatSts', 'VisFusnSeatResThrdRowRiSeatSts', 'VisFusnSeatResPassSeatSts', 'VisFusnSeatResSecRowRiSeatSts', 'VisFusnSeatResSecRowLeSeatSts', 'VisFusnSeatResSecRowMidSeatSts']}

    class VisFusnSeatResDrvrSeatSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Driver Seat result with visual perception "
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class VisFusnSeatResThrdRowMidSeatSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Thrid Row middle Seat result with visualI perception "
        signal_length = 1
        start_position = 6
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class VisFusnSeatResThrdRowLeSeatSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Thrid Row left Seat result with visualI perception "
        signal_length = 1
        start_position = 5
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class VisFusnSeatResThrdRowRiSeatSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Thrid Row Right Seat result with visualI perception "
        signal_length = 1
        start_position = 4
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class VisFusnSeatResPassSeatSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Passanger Seat result with visual perception "
        signal_length = 1
        start_position = 3
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class VisFusnSeatResSecRowRiSeatSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Second Row right Seat result with visual perception "
        signal_length = 1
        start_position = 2
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class VisFusnSeatResSecRowLeSeatSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Second Row Left Seat result with visual perception "
        signal_length = 1
        start_position = 1
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class VisFusnSeatResSecRowMidSeatSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Second Row middle Seat result with visual perception "
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu26:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40201A
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class SetUsgModUpProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = ""
        signal_length = 4
        start_position = 3
        value_definition = {'0x0': ' UsgModReq_Idle', '0x1': ' UsgModReq_Inactive', '0x2': ' UsgModReq_Convenience', '0xD': ' UsgModReq_Driving'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu28:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40201C
    pdu_length_bytes = 2
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class VehSpdLimnOnReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Speed limit request "
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' SetSpdSts_Off', '0x1': ' SetSpdSts_ManuallySet', '0x2': ' SetSpdSts_AutomaticallySet', '0x3': ' SetSpdSts_Reserved'}

    class VehSpdLimnTargtValReq:
        comments = ""
        factor = 1.0
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "The speed limit set by the driver"
        signal_length = 8
        start_position = 15
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu49:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402031
    pdu_length_bytes = 4
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'ClimateTranProgsIndcr': ['ClimateTranProgsIndcrFrntLe', 'ClimateTranProgsIndcrFrntRi', 'ClimateTranProgsIndcrReLe', 'ClimateTranProgsIndcrReRi']}

    class ClimateTranProgsIndcrFrntLe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Climate Front Left Area Transition Progress Indicator"
        signal_length = 7
        start_position = 7
        value_definition = {}

    class ClimateTranProgsIndcrFrntRi:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Climate Front Right Area Transition Progress Indicator"
        signal_length = 7
        start_position = 0
        value_definition = {}

    class ClimateTranProgsIndcrReLe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Climate Rear Left Area Transition Progress Indicator"
        signal_length = 7
        start_position = 9
        value_definition = {}

    class ClimateTranProgsIndcrReRi:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Climate Rear Right Area Transition Progress Indicator"
        signal_length = 7
        start_position = 18
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu51:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402033
    pdu_length_bytes = 7
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'ClimateTSoak': ['ClimateTSoakReRi', 'ClimateTSoakReLe', 'ClimateTSoakFrntRi', 'ClimateTSoakFrntLe']}

    class ClimateTSoakReRi:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = None
        signal_description = "Climate Rear Right Area Soak Temperature For Automatic Air Conditioning Algorithm"
        signal_length = 13
        start_position = 7
        value_definition = {}

    class ClimateTSoakReLe:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = None
        signal_description = "Climate Rear Left Area Soak Temperature For Automatic Air Conditioning Algorithm"
        signal_length = 13
        start_position = 10
        value_definition = {}

    class ClimateTSoakFrntRi:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = None
        signal_description = "Climate Front Right Area Soak Temperature For Automatic Air Conditioning Algorithm"
        signal_length = 13
        start_position = 29
        value_definition = {}

    class ClimateTSoakFrntLe:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = None
        signal_description = "Climate Front Left Area Soak Temperature For Automatic Air Conditioning Algorithm"
        signal_length = 13
        start_position = 32
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu57:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402039
    pdu_length_bytes = 5
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'CmptmtHeatgPwrAct': ['CmptmtHeatgPwrActFrntRi', 'CmptmtHeatgPwrActReLe', 'CmptmtHeatgPwrActReRi', 'CmptmtHeatgPwrActFrntLe']}

    class CmptmtHeatgPwrActFrntRi:
        comments = ""
        factor = 10.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Compartment Front Right Area Actual Heating Power"
        signal_length = 9
        start_position = 7
        value_definition = {}

    class CmptmtHeatgPwrActReLe:
        comments = ""
        factor = 10.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Compartment Rear Left Area Actual Heating Power"
        signal_length = 9
        start_position = 14
        value_definition = {}

    class CmptmtHeatgPwrActReRi:
        comments = ""
        factor = 10.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Compartment Rear Right Area Actual Heating Power"
        signal_length = 9
        start_position = 21
        value_definition = {}

    class CmptmtHeatgPwrActFrntLe:
        comments = ""
        factor = 10.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Compartment Front Left Area Actual Heating Power"
        signal_length = 9
        start_position = 28
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu61:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40203D
    pdu_length_bytes = 2
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class CmptmtReHvacInletAirT:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = None
        signal_description = "Compartment Rear HVAC Air Inlet Temperature"
        signal_length = 13
        start_position = 7
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu55:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402037
    pdu_length_bytes = 5
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'CmptmtCoolgPwrDes': ['CmptmtCoolgPwrDesFrntLe', 'CmptmtCoolgPwrDesReLe', 'CmptmtCoolgPwrDesReRi', 'CmptmtCoolgPwrDesFrntRi']}

    class CmptmtCoolgPwrDesFrntLe:
        comments = ""
        factor = 10.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Compartment Front Left Area Cooling Power Request"
        signal_length = 9
        start_position = 7
        value_definition = {}

    class CmptmtCoolgPwrDesReLe:
        comments = ""
        factor = 10.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Compartment Rear Left Area Cooling Power Request"
        signal_length = 9
        start_position = 14
        value_definition = {}

    class CmptmtCoolgPwrDesReRi:
        comments = ""
        factor = 10.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Compartment Rear Right Area Cooling Power Request"
        signal_length = 9
        start_position = 21
        value_definition = {}

    class CmptmtCoolgPwrDesFrntRi:
        comments = ""
        factor = 10.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Compartment Front Right Area Cooling Power Request"
        signal_length = 9
        start_position = 28
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu53:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402035
    pdu_length_bytes = 2
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class CmptmtAirPTCOutlTEstimd:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = None
        signal_description = "Compartment HVPTC Outlet Air Estimated Temperature"
        signal_length = 13
        start_position = 7
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu54:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402036
    pdu_length_bytes = 5
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'CmptmtCoolgPwrAct': ['CmptmtCoolgPwrActReLe', 'CmptmtCoolgPwrActFrntRi', 'CmptmtCoolgPwrActReRi', 'CmptmtCoolgPwrActFrntLe']}

    class CmptmtCoolgPwrActReLe:
        comments = ""
        factor = 10.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Compartment Rear Left Area Actual Cooling Power"
        signal_length = 9
        start_position = 7
        value_definition = {}

    class CmptmtCoolgPwrActFrntRi:
        comments = ""
        factor = 10.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Compartment Front Right Area Actual Cooling Power"
        signal_length = 9
        start_position = 14
        value_definition = {}

    class CmptmtCoolgPwrActReRi:
        comments = ""
        factor = 10.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Compartment Rear Right Area Actual Cooling Power"
        signal_length = 9
        start_position = 21
        value_definition = {}

    class CmptmtCoolgPwrActFrntLe:
        comments = ""
        factor = 10.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Compartment Front Left Area Actual Cooling Power"
        signal_length = 9
        start_position = 28
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu47:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40202F
    pdu_length_bytes = 4
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'ClimateHiAirFlwSectn': ['ClimateHiAirFlwSectnReLe', 'ClimateHiAirFlwSectnFrntRi', 'ClimateHiAirFlwSectnReRi', 'ClimateHiAirFlwSectnFrntLe']}

    class ClimateHiAirFlwSectnReLe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Climate Rear Left Area High Air Flow Section For Automatic Air Conditioning Algorithm"
        signal_length = 7
        start_position = 7
        value_definition = {}

    class ClimateHiAirFlwSectnFrntRi:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Climate Front Right Area High Air Flow Section For Automatic Air Conditioning Algorithm"
        signal_length = 7
        start_position = 0
        value_definition = {}

    class ClimateHiAirFlwSectnReRi:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Climate Rear Right Area High Air Flow Section For Automatic Air Conditioning Algorithm"
        signal_length = 7
        start_position = 9
        value_definition = {}

    class ClimateHiAirFlwSectnFrntLe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Climate Front Left Area High Air Flow Section For Automatic Air Conditioning Algorithm"
        signal_length = 7
        start_position = 18
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu42:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40202A
    pdu_length_bytes = 4
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'ClimateAirTempDecaySectn': ['ClimateAirTempDecaySectnFrntRi', 'ClimateAirTempDecaySectnReRi', 'ClimateAirTempDecaySectnFrntLe', 'ClimateAirTempDecaySectnReLe']}

    class ClimateAirTempDecaySectnFrntRi:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Climate Front Right Area Outlet Air Temperature Decay Section For Automatic Air Conditioning Algorithm"
        signal_length = 7
        start_position = 7
        value_definition = {}

    class ClimateAirTempDecaySectnReRi:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Climate Rear Right Area Outlet Air Temperature Decay Section For Automatic Air Conditioning Algorithm"
        signal_length = 7
        start_position = 0
        value_definition = {}

    class ClimateAirTempDecaySectnFrntLe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Climate Front Left Area Outlet Air Temperature Decay Section For Automatic Air Conditioning Algorithm"
        signal_length = 7
        start_position = 9
        value_definition = {}

    class ClimateAirTempDecaySectnReLe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Climate Rear Left Area Outlet Air Temperature Decay Section For Automatic Air Conditioning Algorithm"
        signal_length = 7
        start_position = 18
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu50:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402032
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class ClimateTrfFlg:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Climate Steady State Transfers To Transient State Flag For Automatic Air Conditioning Algorithm"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' Flg1_Rst', '0x1': ' Flg1_Set'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu39:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402027
    pdu_length_bytes = 5
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'ClimateAirFlwTarCalcn': ['ClimateAirFlwTarCalcnReLe', 'ClimateAirFlwTarCalcnFrntLe', 'ClimateAirFlwTarCalcnFrntRi', 'ClimateAirFlwTarCalcnReRi']}

    class ClimateAirFlwTarCalcnReLe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Climate Rear Left Area Target Air Flow Calculation Value For Automatic Air Conditioning Algorithm"
        signal_length = 10
        start_position = 7
        value_definition = {}

    class ClimateAirFlwTarCalcnFrntLe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Climate Front Left Area Target Air Flow Calculation Value For Automatic Air Conditioning Algorithm"
        signal_length = 10
        start_position = 13
        value_definition = {}

    class ClimateAirFlwTarCalcnFrntRi:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Climate Front Right Area Target Air Flow Calculation Value For Automatic Air Conditioning Algorithm"
        signal_length = 10
        start_position = 19
        value_definition = {}

    class ClimateAirFlwTarCalcnReRi:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Climate Rear Right Area Target Air Flow Calculation Value For Automatic Air Conditioning Algorithm"
        signal_length = 10
        start_position = 25
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu36:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402024
    pdu_length_bytes = 4
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'ClimateAirFlwDecaySectn': ['ClimateAirFlwDecaySectnFrntLe', 'ClimateAirFlwDecaySectnReLe', 'ClimateAirFlwDecaySectnFrntRi', 'ClimateAirFlwDecaySectnReRi']}

    class ClimateAirFlwDecaySectnFrntLe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Climate Front Left Area Air Flow Decay Section For Automatic Air Conditioning Algorithm"
        signal_length = 7
        start_position = 7
        value_definition = {}

    class ClimateAirFlwDecaySectnReLe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Climate Rear Left Area Air Flow Decay Section For Automatic Air Conditioning Algorithm"
        signal_length = 7
        start_position = 0
        value_definition = {}

    class ClimateAirFlwDecaySectnFrntRi:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Climate Front Right Area Air Flow Decay Section For Automatic Air Conditioning Algorithm"
        signal_length = 7
        start_position = 9
        value_definition = {}

    class ClimateAirFlwDecaySectnReRi:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Climate Rear Right Area Air Flow Decay Section For Automatic Air Conditioning Algorithm"
        signal_length = 7
        start_position = 18
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu52:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402034
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class CmpmtClimaSteadySts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Compartment Climate Steady Status"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu64:
    base_type = "Boolean"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402040
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class CmptmtThermHeatgEna:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Compartment Thermal Heating Enable"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu48:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402030
    pdu_length_bytes = 4
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'ClimateStrictAirTempSectn': ['ClimateStrictAirTempSectnReRi', 'ClimateStrictAirTempSectnFrntLe', 'ClimateStrictAirTempSectnFrntRi', 'ClimateStrictAirTempSectnReLe']}

    class ClimateStrictAirTempSectnReRi:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Climate Rear Right Area Strict Outlet Air Temperature Section For Automatic Air Conditioning Algorithm"
        signal_length = 7
        start_position = 7
        value_definition = {}

    class ClimateStrictAirTempSectnFrntLe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Climate Front Left Area Strict Outlet Air Temperature Section For Automatic Air Conditioning Algorithm"
        signal_length = 7
        start_position = 0
        value_definition = {}

    class ClimateStrictAirTempSectnFrntRi:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Climate Front Right Area Strict Outlet Air Temperature Section For Automatic Air Conditioning Algorithm"
        signal_length = 7
        start_position = 9
        value_definition = {}

    class ClimateStrictAirTempSectnReLe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Climate Rear Left Area Strict Outlet Air Temperature Section For Automatic Air Conditioning Algorithm"
        signal_length = 7
        start_position = 18
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu41:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402029
    pdu_length_bytes = 4
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'ClimateAirTempDecayRat': ['ClimateAirTempDecayRatReLe', 'ClimateAirTempDecayRatFrntLe', 'ClimateAirTempDecayRatReRi', 'ClimateAirTempDecayRatFrntRi']}

    class ClimateAirTempDecayRatReLe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Climate Rear Left Area Outlet Air Temperature Decay Ratio For Automatic Air Conditioning Algorithm"
        signal_length = 7
        start_position = 7
        value_definition = {}

    class ClimateAirTempDecayRatFrntLe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Climate Front Left Area Outlet Air Temperature Decay Ratio For Automatic Air Conditioning Algorithm"
        signal_length = 7
        start_position = 0
        value_definition = {}

    class ClimateAirTempDecayRatReRi:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Climate Rear Right Area Outlet Air Temperature Decay Ratio For Automatic Air Conditioning Algorithm"
        signal_length = 7
        start_position = 9
        value_definition = {}

    class ClimateAirTempDecayRatFrntRi:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Climate Front Right Area Outlet Air Temperature Decay Ratio For Automatic Air Conditioning Algorithm"
        signal_length = 7
        start_position = 18
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu43:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40202B
    pdu_length_bytes = 7
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'ClimateAirTempIniSuppsn': ['ClimateAirTempIniSuppsnReLe', 'ClimateAirTempIniSuppsnFrntRi', 'ClimateAirTempIniSuppsnFrntLe', 'ClimateAirTempIniSuppsnReRi']}

    class ClimateAirTempIniSuppsnReLe:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = None
        signal_description = "Climate Rear Left Area Outlet Air Temperature Initial Superposition For Automatic Air Conditioning Algorithm"
        signal_length = 13
        start_position = 7
        value_definition = {}

    class ClimateAirTempIniSuppsnFrntRi:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = None
        signal_description = "Climate Front Right Area Outlet Air Temperature Initial Superposition For Automatic Air Conditioning Algorithm"
        signal_length = 13
        start_position = 10
        value_definition = {}

    class ClimateAirTempIniSuppsnFrntLe:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = None
        signal_description = "Climate Front Left Area Outlet Air Temperature Initial Superposition For Automatic Air Conditioning Algorithm"
        signal_length = 13
        start_position = 29
        value_definition = {}

    class ClimateAirTempIniSuppsnReRi:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = None
        signal_description = "Climate Rear Right Area Outlet Air Temperature Initial Superposition For Automatic Air Conditioning Algorithm"
        signal_length = 13
        start_position = 32
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu45:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40202D
    pdu_length_bytes = 7
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'ClimateAirTempTarCalcn': ['ClimateAirTempTarCalcnReLe', 'ClimateAirTempTarCalcnReRi', 'ClimateAirTempTarCalcnFrntLe', 'ClimateAirTempTarCalcnFrntRi']}

    class ClimateAirTempTarCalcnReLe:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = None
        signal_description = "Climate Rear Left Area Target Outlet Air Temperature Calculation Value For Automatic Air Conditioning Algorithm"
        signal_length = 13
        start_position = 7
        value_definition = {}

    class ClimateAirTempTarCalcnReRi:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = None
        signal_description = "Climate Rear Right Area Target Outlet Air Temperature Calculation Value For Automatic Air Conditioning Algorithm"
        signal_length = 13
        start_position = 10
        value_definition = {}

    class ClimateAirTempTarCalcnFrntLe:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = None
        signal_description = "Climate Front Left Area Target Outlet Air Temperature Calculation Value For Automatic Air Conditioning Algorithm"
        signal_length = 13
        start_position = 29
        value_definition = {}

    class ClimateAirTempTarCalcnFrntRi:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = None
        signal_description = "Climate Front Right Area Target Outlet Air Temperature Calculation Value For Automatic Air Conditioning Algorithm"
        signal_length = 13
        start_position = 32
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu56:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402038
    pdu_length_bytes = 2
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class CmptmtFrntHvacInletAirT:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = None
        signal_description = "Compartment Front HVAC Air Inlet Temperature"
        signal_length = 13
        start_position = 7
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu33:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402021
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class BookStopTimeAchieved:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Book charge stop time achieved flag"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' Falsetrue_Init', '0x1': ' Falsetrue_False', '0x2': ' Falsetrue_True', '0x3': ' Falsetrue_Reserved'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu46:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40202E
    pdu_length_bytes = 4
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'ClimateBlwrActPwr': ['ClimateBlwrActPwrBoost', 'ClimateBlwrActPwrRe', 'ClimateBlwrActPwrFrnt']}

    class ClimateBlwrActPwrBoost:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Climate Boost Blower Actual Power"
        signal_length = 10
        start_position = 7
        value_definition = {}

    class ClimateBlwrActPwrRe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Climate Rear Blower Actual Power"
        signal_length = 10
        start_position = 13
        value_definition = {}

    class ClimateBlwrActPwrFrnt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Climate Front Blower Actual Power"
        signal_length = 10
        start_position = 19
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu44:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40202C
    pdu_length_bytes = 7
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'ClimateAirTempRealSuppsn': ['ClimateAirTempRealSuppsnFrntRi', 'ClimateAirTempRealSuppsnReLe', 'ClimateAirTempRealSuppsnFrntLe', 'ClimateAirTempRealSuppsnReRi']}

    class ClimateAirTempRealSuppsnFrntRi:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = None
        signal_description = "Climate Front Right Area Outlet Air Temperature Real Time Superposition For Automatic Air Conditioning Algorithm"
        signal_length = 13
        start_position = 7
        value_definition = {}

    class ClimateAirTempRealSuppsnReLe:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = None
        signal_description = "Climate Rear Left Area Outlet Air Temperature Real Time Superposition For Automatic Air Conditioning Algorithm"
        signal_length = 13
        start_position = 10
        value_definition = {}

    class ClimateAirTempRealSuppsnFrntLe:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = None
        signal_description = "Climate Front Left Area Outlet Air Temperature Real Time Superposition For Automatic Air Conditioning Algorithm"
        signal_length = 13
        start_position = 29
        value_definition = {}

    class ClimateAirTempRealSuppsnReRi:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = None
        signal_description = "Climate Rear Right Area Outlet Air Temperature Real Time Superposition For Automatic Air Conditioning Algorithm"
        signal_length = 13
        start_position = 32
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu32:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402020
    pdu_length_bytes = 2
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class BookDischrgnTarVal:
        comments = ""
        factor = 0.05
        initial_value = 2040
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "The discharge target SOC value is set from the interactive."
        signal_length = 11
        start_position = 7
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu34:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402022
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class ClimaEcoSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Cliamte Eco Status"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu35:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402023
    pdu_length_bytes = 4
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'ClimateAirFlwDecayRat': ['ClimateAirFlwDecayRatFrntRi', 'ClimateAirFlwDecayRatReLe', 'ClimateAirFlwDecayRatReRi', 'ClimateAirFlwDecayRatFrntLe']}

    class ClimateAirFlwDecayRatFrntRi:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Climate Front Right Area Air Flow Decay Ratio For Automatic Air Conditioning Algorithm"
        signal_length = 7
        start_position = 7
        value_definition = {}

    class ClimateAirFlwDecayRatReLe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Climate Rear Left Area Air Flow Decay Ratio For Automatic Air Conditioning Algorithm"
        signal_length = 7
        start_position = 0
        value_definition = {}

    class ClimateAirFlwDecayRatReRi:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Climate Rear Right Area Air Flow Decay Ratio For Automatic Air Conditioning Algorithm"
        signal_length = 7
        start_position = 9
        value_definition = {}

    class ClimateAirFlwDecayRatFrntLe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Climate Front Left Area Air Flow Decay Ratio For Automatic Air Conditioning Algorithm"
        signal_length = 7
        start_position = 18
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu40:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402028
    pdu_length_bytes = 7
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'ClimateAirTempBascCalcn': ['ClimateAirTempBascCalcnFrntLe', 'ClimateAirTempBascCalcnFrntRi', 'ClimateAirTempBascCalcnReLe', 'ClimateAirTempBascCalcnReRi']}

    class ClimateAirTempBascCalcnFrntLe:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = None
        signal_description = "Climate Front Left Area Basic Outlet Air Temperature Calculation Value For Automatic Air Conditioning Algorithm"
        signal_length = 13
        start_position = 7
        value_definition = {}

    class ClimateAirTempBascCalcnFrntRi:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = None
        signal_description = "Climate Front Right Area Basic Outlet Air Temperature Calculation Value For Automatic Air Conditioning Algorithm"
        signal_length = 13
        start_position = 10
        value_definition = {}

    class ClimateAirTempBascCalcnReLe:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = None
        signal_description = "Climate Rear Left Area Basic Outlet Air Temperature Calculation Value For Automatic Air Conditioning Algorithm"
        signal_length = 13
        start_position = 29
        value_definition = {}

    class ClimateAirTempBascCalcnReRi:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = None
        signal_description = "Climate Rear Right Area Basic Outlet Air Temperature Calculation Value For Automatic Air Conditioning Algorithm"
        signal_length = 13
        start_position = 32
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu63:
    base_type = "Boolean"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40203F
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class CmptmtThermCoolgEna:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Compartment Thermal Cooling Enable"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu58:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40203A
    pdu_length_bytes = 5
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'CmptmtHeatgPwrDes': ['CmptmtHeatgPwrDesReRi', 'CmptmtHeatgPwrDesFrntLe', 'CmptmtHeatgPwrDesFrntRi', 'CmptmtHeatgPwrDesReLe']}

    class CmptmtHeatgPwrDesReRi:
        comments = ""
        factor = 10.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Compartment Rear Right Area Heating Power Request"
        signal_length = 9
        start_position = 7
        value_definition = {}

    class CmptmtHeatgPwrDesFrntLe:
        comments = ""
        factor = 10.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Compartment Front Left Area Heating Power Request"
        signal_length = 9
        start_position = 14
        value_definition = {}

    class CmptmtHeatgPwrDesFrntRi:
        comments = ""
        factor = 10.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Compartment Front Right Area Heating Power Request"
        signal_length = 9
        start_position = 21
        value_definition = {}

    class CmptmtHeatgPwrDesReLe:
        comments = ""
        factor = 10.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Compartment Rear Left Area Heating Power Request"
        signal_length = 9
        start_position = 28
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu37:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402025
    pdu_length_bytes = 5
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'ClimateAirFlwIniSuppsn': ['ClimateAirFlwIniSuppsnFrntLe', 'ClimateAirFlwIniSuppsnFrntRi', 'ClimateAirFlwIniSuppsnReRi', 'ClimateAirFlwIniSuppsnReLe']}

    class ClimateAirFlwIniSuppsnFrntLe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Climate Front Left Area Air Flow Initial Superposition For Automatic Air Conditioning Algorithm"
        signal_length = 10
        start_position = 7
        value_definition = {}

    class ClimateAirFlwIniSuppsnFrntRi:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Climate Front Right Area Air Flow Initial Superposition For Automatic Air Conditioning Algorithm"
        signal_length = 10
        start_position = 13
        value_definition = {}

    class ClimateAirFlwIniSuppsnReRi:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Climate Rear Right Area Air Flow Initial Superposition For Automatic Air Conditioning Algorithm"
        signal_length = 10
        start_position = 19
        value_definition = {}

    class ClimateAirFlwIniSuppsnReLe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Climate Rear Left Area Air Flow Initial Superposition For Automatic Air Conditioning Algorithm"
        signal_length = 10
        start_position = 25
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu59:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40203B
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class CmptmtMaxDefrstSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Compartment Max Defrost Status"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu38:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402026
    pdu_length_bytes = 5
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'ClimateAirFlwRealSuppsn': ['ClimateAirFlwRealSuppsnFrntRi', 'ClimateAirFlwRealSuppsnReRi', 'ClimateAirFlwRealSuppsnFrntLe', 'ClimateAirFlwRealSuppsnReLe']}

    class ClimateAirFlwRealSuppsnFrntRi:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Climate Front Right Area Air Flow Real Time Superposition For Automatic Air Conditioning Algorithm"
        signal_length = 10
        start_position = 7
        value_definition = {}

    class ClimateAirFlwRealSuppsnReRi:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Climate Rear Right Area Air Flow Real Time Superposition For Automatic Air Conditioning Algorithm"
        signal_length = 10
        start_position = 13
        value_definition = {}

    class ClimateAirFlwRealSuppsnFrntLe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Climate Front Left Area Air Flow Real Time Superposition For Automatic Air Conditioning Algorithm"
        signal_length = 10
        start_position = 19
        value_definition = {}

    class ClimateAirFlwRealSuppsnReLe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Climate Rear Left Area Air Flow Real Time Superposition For Automatic Air Conditioning Algorithm"
        signal_length = 10
        start_position = 25
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu62:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40203E
    pdu_length_bytes = 7
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'CmptmtTCalcdHdLvl': ['CmptmtTCalcdHdLvlReRi', 'CmptmtTCalcdHdLvlFrntRi', 'CmptmtTCalcdHdLvlFrntLe', 'CmptmtTCalcdHdLvlReLe']}

    class CmptmtTCalcdHdLvlReRi:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = None
        signal_description = "Compartment Rear Right Area Head Level Temperature Calculated Value"
        signal_length = 13
        start_position = 7
        value_definition = {}

    class CmptmtTCalcdHdLvlFrntRi:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = None
        signal_description = "Compartment Front Right Area Head Level Temperature Calculated Value"
        signal_length = 13
        start_position = 10
        value_definition = {}

    class CmptmtTCalcdHdLvlFrntLe:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = None
        signal_description = "Compartment Front Left Area Head Level Temperature Calculated Value"
        signal_length = 13
        start_position = 29
        value_definition = {}

    class CmptmtTCalcdHdLvlReLe:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = None
        signal_description = "Compartment Rear Left Area Head Level Temperature Calculated Value"
        signal_length = 13
        start_position = 32
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu60:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40203C
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class CmptmtMistRisk:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Compartment Mist Risk"
        signal_length = 7
        start_position = 7
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu97:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402061
    pdu_length_bytes = 7
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'HVBattThermReqFromSrv': ['HVBattThermReqFromSrvCooltFlwReq', 'HVBattThermReqFromSrvCooltTReq', 'HVBattThermReqFromSrvThermLvlReq', 'HVBattThermReqFromSrvCellTTar', 'HVBattThermReqFromSrvThermReq', 'HVBattThermReqFromSrvSourceID', 'HVBattThermReqFromSrvCellTType']}

    class HVBattThermReqFromSrvCooltFlwReq:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Hvbatt thermal management coolant flow request from smart app"
        signal_length = 9
        start_position = 7
        value_definition = {}

    class HVBattThermReqFromSrvCooltTReq:
        comments = ""
        factor = 0.1
        initial_value = 600
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -60
        sig_ub = None
        signal_description = "Hvbatt thermal management coolant temperature request from smart app"
        signal_length = 11
        start_position = 14
        value_definition = {}

    class HVBattThermReqFromSrvThermLvlReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Hvbatt thermal management level request from smart app"
        signal_length = 2
        start_position = 19
        value_definition = {'0x0': ' ReqLvl_NoReq', '0x1': ' ReqLvl_LoReq', '0x2': ' ReqLvl_MidReq', '0x3': ' ReqLvl_HiReq'}

    class HVBattThermReqFromSrvCellTTar:
        comments = ""
        factor = 0.1
        initial_value = 600
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -60
        sig_ub = None
        signal_description = "Hvbatt thermal management cell temperature request from smart app"
        signal_length = 11
        start_position = 17
        value_definition = {}

    class HVBattThermReqFromSrvThermReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Hvbatt thermal management request from smart app"
        signal_length = 3
        start_position = 38
        value_definition = {'0x0': ' HVBattThermReq_Idle', '0x1': ' HVBattThermReq_ThermalBalancing', '0x2': ' HVBattThermReq_PassiveHeating', '0x3': ' HVBattThermReq_ActiveHeating', '0x4': ' HVBattThermReq_PassiveCooling', '0x5': ' HVBattThermReq_ActiveCooling', '0x6': ' HVBattThermReq_CombinedCooling', '0x7': ' HVBattThermReq_Reserved'}

    class HVBattThermReqFromSrvSourceID:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "SourceID"
        signal_length = 16
        start_position = 47
        value_definition = {}

    class HVBattThermReqFromSrvCellTType:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Hvbatt thermal management cell type from smart app"
        signal_length = 2
        start_position = 35
        value_definition = {'0x0': ' BattTemperatureType_Idle', '0x1': ' BattTemperatureType_Tmin', '0x2': ' BattTemperatureType_TAvg', '0x3': ' BattTemperatureType_TMax'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu98:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402062
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class HVChrgnOrDchaReqSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "The charging soft-switch requests the source state"
        signal_length = 4
        start_position = 7
        value_definition = {'0x0': ' HVChrgnOrDchaReqSts_Default', '0x1': ' HVChrgnOrDchaReqSts_HMIOn', '0x2': ' HVChrgnOrDchaReqSts_HMIOff', '0x3': ' HVChrgnOrDchaReqSts_APPOn', '0x4': ' HVChrgnOrDchaReqSts_APPOff', '0x5': ' HVChrgnOrDchaReqSts_BookChrgnOn', '0x6': ' HVChrgnOrDchaReqSts_BookChrgnOff', '0x7': ' HVChrgnOrDchaReqSts_DisChrgProtnOn', '0x8': ' HVChrgnOrDchaReqSts_DisChrgProtnOff', '0x9': ' HVChrgnOrDchaReqSts_HVIntelligentOn', '0xA': ' HVChrgnOrDchaReqSts_FotaOn', '0xB': ' HVChrgnOrDchaReqSts_Reserved1', '0xC': ' HVChrgnOrDchaReqSts_Reserved2', '0xD': ' HVChrgnOrDchaReqSts_Reserved3', '0xE': ' HVChrgnOrDchaReqSts_Reserved4', '0xF': ' HVChrgnOrDchaReqSts_Reserved'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu91:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40205B
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class GearLvrIndcnVirtReq:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Virtual shift request, containing P/R/N/D gear."
        signal_length = 3
        start_position = 7
        value_definition = {'0x0': ' GearLvrIndcn_Default', '0x1': ' GearLvrIndcn_P', '0x2': ' GearLvrIndcn_R', '0x3': ' GearLvrIndcn_N', '0x4': ' GearLvrIndcn_D', '0x5': ' GearLvrIndcn_Reserved1', '0x6': ' GearLvrIndcn_Reserved2', '0x7': ' GearLvrIndcn_Undefd'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu92:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40205C
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class HbaSoftSwt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Hba soft switch"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' OnOff2_On', '0x1': ' OnOff2_Off'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu84:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402054
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class DoorOpenProtectSet:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "set door open protect function able or disable"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu72:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402048
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class CnvModProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Convinence Mode Proxy Request"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu66:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402042
    pdu_length_bytes = 3
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'CmptmtTSet': ['CmptmtTSetReLe', 'CmptmtTSetFrntLe', 'CmptmtTSetFrntRi', 'CmptmtTSetReRi']}

    class CmptmtTSetReLe:
        comments = ""
        factor = 0.5
        initial_value = 14
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 15
        sig_ub = None
        signal_description = "Compartment Rear Left Area Temperature Setting"
        signal_length = 6
        start_position = 7
        value_definition = {'0x0': 'HmiCmptmtT_Lo', '0x1F': 'HmiCmptmtT_Hi'}

    class CmptmtTSetFrntLe:
        comments = ""
        factor = 0.5
        initial_value = 14
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 15
        sig_ub = None
        signal_description = "Compartment Front Left Area Temperature Setting"
        signal_length = 6
        start_position = 1
        value_definition = {'0x0': 'HmiCmptmtT_Lo', '0x1F': 'HmiCmptmtT_Hi'}

    class CmptmtTSetFrntRi:
        comments = ""
        factor = 0.5
        initial_value = 14
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 15
        sig_ub = None
        signal_description = "Compartment Front Right Area Temperature Setting"
        signal_length = 6
        start_position = 11
        value_definition = {'0x0': 'HmiCmptmtT_Lo', '0x1F': 'HmiCmptmtT_Hi'}

    class CmptmtTSetReRi:
        comments = ""
        factor = 0.5
        initial_value = 14
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 15
        sig_ub = None
        signal_description = "Compartment Rear Right Area Temperature Setting"
        signal_length = 6
        start_position = 21
        value_definition = {'0x0': 'HmiCmptmtT_Lo', '0x1F': 'HmiCmptmtT_Hi'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu81:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402051
    pdu_length_bytes = 3
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'DisplaySafeEnable': ['DisplaySafeEnableSts', 'DisplaySafeEnableChks', 'DisplaySafeEnableCntr']}

    class DisplaySafeEnableSts:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "The Switch of Front Screen Function safe "
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' EnableDisable_Enable', '0x1': ' EnableDisable_Disable'}

    class DisplaySafeEnableChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Checks"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class DisplaySafeEnableCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Counter"
        signal_length = 4
        start_position = 23
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu83:
    base_type = "Boolean"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402053
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class DKSrvSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Indicate if Digital Key Service is ready to receive data"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu86:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402056
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class EgyRgnLimCmpSet:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Brake compensation switch when energy recovery is limited"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' OffOnCmd_NoCmd', '0x1': ' OffOnCmd_Off', '0x2': ' OffOnCmd_On'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu89:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402059
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class FrntBlwrLvlSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Front Blower Actual Level Status"
        signal_length = 4
        start_position = 7
        value_definition = {'0x0': ' FrntBlwrLvl_Off', '0x1': ' FrntBlwrLvl_LvlMan1', '0x2': ' FrntBlwrLvl_LvlMan2', '0x3': ' FrntBlwrLvl_LvlMan3', '0x4': ' FrntBlwrLvl_LvlMan4', '0x5': ' FrntBlwrLvl_LvlMan5', '0x6': ' FrntBlwrLvl_LvlMan6', '0x7': ' FrntBlwrLvl_LvlMan7', '0x8': ' FrntBlwrLvl_LvlMan8', '0x9': ' FrntBlwrLvl_LvlMan9', '0xA': ' FrntBlwrLvl_LvlAutoLo', '0xB': ' FrntBlwrLvl_LvlAutoNormal', '0xC': ' FrntBlwrLvl_LvlAutoHi'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu80:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402050
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class DisplayMode:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "The Day or Night Mode"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' DisplayMode_Unknow', '0x1': ' DisplayMode_DayMode', '0x2': ' DisplayMode_NightMode', '0x3': ' DisplayMode_Reserved1'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu88:
    base_type = "Boolean"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402058
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class FrntBlwrAftRunSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Front Blower AfterRun Status"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu74:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40204A
    pdu_length_bytes = 5
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'CoolAirTarRat': ['CoolAirTarRatReRi', 'CoolAirTarRatFrntRi', 'CoolAirTarRatFrntLe', 'CoolAirTarRatReLe']}

    class CoolAirTarRatReRi:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Rear Right Area Target Cooling Air Mass Flow Ratio"
        signal_length = 10
        start_position = 7
        value_definition = {}

    class CoolAirTarRatFrntRi:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Front Right Area Target Cooling Air Mass Flow Ratio"
        signal_length = 10
        start_position = 13
        value_definition = {}

    class CoolAirTarRatFrntLe:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Front Left Area Target Cooling Air Mass Flow Ratio"
        signal_length = 10
        start_position = 19
        value_definition = {}

    class CoolAirTarRatReLe:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Rear Left Area Target Cooling Air Mass Flow Ratio"
        signal_length = 10
        start_position = 25
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu79:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40204F
    pdu_length_bytes = 2
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'DisplayGear': ['DisplayGearCntr', 'DisplayGearLvl', 'DisplayGearChks']}

    class DisplayGearCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Counter"
        signal_length = 4
        start_position = 7
        value_definition = {}

    class DisplayGearLvl:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "The  Rendering Gear For Display"
        signal_length = 3
        start_position = 3
        value_definition = {'0x0': ' GearLvrIndcn_Default', '0x1': ' GearLvrIndcn_P', '0x2': ' GearLvrIndcn_R', '0x3': ' GearLvrIndcn_N', '0x4': ' GearLvrIndcn_D', '0x5': ' GearLvrIndcn_Reserved1', '0x6': ' GearLvrIndcn_Reserved2', '0x7': ' GearLvrIndcn_Undefd'}

    class DisplayGearChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Checks"
        signal_length = 8
        start_position = 15
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu93:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40205D
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class HdcSoftSwt:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Hdc soft switch"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' OnOff2_On', '0x1': ' OnOff2_Off'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu99:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402063
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class HVIntelligentChrgSWSt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "The state of HV charging  intelligent power supply switch."
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' OnOffCrit1_NotVld1', '0x1': ' OnOffCrit1_Off', '0x2': ' OnOffCrit1_On', '0x3': ' OnOffCrit1_NotVld2'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu90:
    base_type = "Boolean"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40205A
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class FrntScrnWakeup:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "The signal to wakeup The Front Screen"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu70:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402046
    pdu_length_bytes = 7
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'CmptmtTSpHdLvlTarT': ['CmptmtTSpHdLvlTarTFrntLe', 'CmptmtTSpHdLvlTarTFrntRi', 'CmptmtTSpHdLvlTarTReLe', 'CmptmtTSpHdLvlTarTReRi']}

    class CmptmtTSpHdLvlTarTFrntLe:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = None
        signal_description = "Compartment Front Left Area Head Level Target Temperature"
        signal_length = 13
        start_position = 7
        value_definition = {}

    class CmptmtTSpHdLvlTarTFrntRi:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = None
        signal_description = "Compartment Front Right Area Head Level Target Temperature"
        signal_length = 13
        start_position = 10
        value_definition = {}

    class CmptmtTSpHdLvlTarTReLe:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = None
        signal_description = "Compartment Rear Left Area Head Level Target Temperature"
        signal_length = 13
        start_position = 29
        value_definition = {}

    class CmptmtTSpHdLvlTarTReRi:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = None
        signal_description = "Compartment Rear Right Area Head Level Target Temperature"
        signal_length = 13
        start_position = 32
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu85:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402055
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class DrvModReqInd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Custom driving mode request, including normal, sport, snow, etc"
        signal_length = 4
        start_position = 7
        value_definition = {'0x0': ' DrvModReqType_Undefd', '0x1': ' DrvModReqType_ECO', '0x2': ' DrvModReqType_Comfort_Normal', '0x3': ' DrvModReqType_Dynamic_Sport', '0x4': ' DrvModReqType_Tank', '0x5': ' DrvModReqType_Offroad_CrossTerrain', '0x6': ' DrvModReqType_Adaptive', '0x7': ' DrvModReqType_Race', '0x8': ' DrvModReqType_Reserved', '0x9': ' DrvModReqType_ECO_PLUS', '0xA': ' DrvModReqType_Power', '0xB': ' DrvModReqType_Snow', '0xC': ' DrvModReqType_Sand', '0xD': ' DrvModReqType_Mud', '0xE': ' DrvModReqType_Rock', '0xF': ' DrvModReqType_Err'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu73:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402049
    pdu_length_bytes = 5
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'CoolAirActRat': ['CoolAirActRatFrntRi', 'CoolAirActRatReLe', 'CoolAirActRatReRi', 'CoolAirActRatFrntLe']}

    class CoolAirActRatFrntRi:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Front Right Area Actual Cooling Air Mass Flow Ratio"
        signal_length = 10
        start_position = 7
        value_definition = {}

    class CoolAirActRatReLe:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Rear Left Area Actual Cooling Air Mass Flow Ratio"
        signal_length = 10
        start_position = 13
        value_definition = {}

    class CoolAirActRatReRi:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Rear Right Area Actual Cooling Air Mass Flow Ratio"
        signal_length = 10
        start_position = 19
        value_definition = {}

    class CoolAirActRatFrntLe:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Front Left Area Actual Cooling Air Mass Flow Ratio"
        signal_length = 10
        start_position = 25
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu76:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40204C
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class CstRgnModSet:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "This Signal represents the setting of the Coast Mode."
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' OnOff2_On', '0x1': ' OnOff2_Off'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu78:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40204E
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class DisplayAreaCtrl:
        comments = ""
        factor = 1.0
        initial_value = 7
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "The Display Area Command"
        signal_length = 3
        start_position = 7
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu96:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402060
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class HMIStopModReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Stop mode requests, including: stop, slow, roll."
        signal_length = 3
        start_position = 7
        value_definition = {'0x0': ' EPedlMod_Initial', '0x1': ' EPedlMod_Crp', '0x2': ' EPedlMod_EPedl', '0x3': ' EPedlMod_Roll', '0x4': ' EPedlMod_Resvd'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu94:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40205E
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class HhcSoftSwt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Hhc soft switch"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' OnOff2_On', '0x1': ' OnOff2_Off'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu68:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402044
    pdu_length_bytes = 7
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'CmptmtTSpAirTarT': ['CmptmtTSpAirTarTReLe', 'CmptmtTSpAirTarTFrntLe', 'CmptmtTSpAirTarTFrntRi', 'CmptmtTSpAirTarTReRi']}

    class CmptmtTSpAirTarTReLe:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = None
        signal_description = "Compartment Rear Left Area Target Air Outlet Temperature"
        signal_length = 13
        start_position = 7
        value_definition = {}

    class CmptmtTSpAirTarTFrntLe:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = None
        signal_description = "Compartment Front Left Area Target Air Outlet Temperature"
        signal_length = 13
        start_position = 10
        value_definition = {}

    class CmptmtTSpAirTarTFrntRi:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = None
        signal_description = "Compartment Front Right Area Target Air Outlet Temperature"
        signal_length = 13
        start_position = 29
        value_definition = {}

    class CmptmtTSpAirTarTReRi:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = None
        signal_description = "Compartment Rear Right Area Target Air Outlet Temperature"
        signal_length = 13
        start_position = 32
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu87:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402057
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class EpbAutoapplySwt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Epb auto apply function switch"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' OnOff2_On', '0x1': ' OnOff2_Off'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu67:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402043
    pdu_length_bytes = 2
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class CmptmtTSpAirPTCTarT:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = None
        signal_description = "High Voltage PTC Outlet Air Temperature Setting"
        signal_length = 13
        start_position = 7
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu69:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402045
    pdu_length_bytes = 10
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'CmptmtTSpEvaprTarT': ['CmptmtTSpEvaprTarTFrntRi', 'CmptmtTSpEvaprTarTRe', 'CmptmtTSpEvaprTarTFrnt', 'CmptmtTSpEvaprTarTReRi', 'CmptmtTSpEvaprTarTFrntLe', 'CmptmtTSpEvaprTarTReLe']}

    class CmptmtTSpEvaprTarTFrntRi:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = None
        signal_description = "Compartment Front Right Area Target Evaporator Air Temperature"
        signal_length = 13
        start_position = 7
        value_definition = {}

    class CmptmtTSpEvaprTarTRe:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = None
        signal_description = "Compartment Rear Target Evaporator Air Temperature"
        signal_length = 13
        start_position = 10
        value_definition = {}

    class CmptmtTSpEvaprTarTFrnt:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = None
        signal_description = "Compartment Front Target Evaporator Air Temperature"
        signal_length = 13
        start_position = 29
        value_definition = {}

    class CmptmtTSpEvaprTarTReRi:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = None
        signal_description = "Compartment Rear Right Area Target Evaporator Air Temperature"
        signal_length = 13
        start_position = 32
        value_definition = {}

    class CmptmtTSpEvaprTarTFrntLe:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = None
        signal_description = "Compartment Front Left Area Target Evaporator Air Temperature"
        signal_length = 13
        start_position = 51
        value_definition = {}

    class CmptmtTSpEvaprTarTReLe:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = None
        signal_description = "Compartment Rear Left Area Target Evaporator Air Temperature"
        signal_length = 13
        start_position = 70
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu75:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40204B
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class CrpModStsSet:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Creep mode state set by the driver "
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' OffOnCmd_NoCmd', '0x1': ' OffOnCmd_Off', '0x2': ' OffOnCmd_On'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu71:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402047
    pdu_length_bytes = 10
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'CmptmtTSpHexTarT': ['CmptmtTSpHexTarTFrnt', 'CmptmtTSpHexTarTFrntLe', 'CmptmtTSpHexTarTReRi', 'CmptmtTSpHexTarTRe', 'CmptmtTSpHexTarTReLe', 'CmptmtTSpHexTarTFrntRi']}

    class CmptmtTSpHexTarTFrnt:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = None
        signal_description = "Compartment Front Target Hex Air Temperature"
        signal_length = 13
        start_position = 7
        value_definition = {}

    class CmptmtTSpHexTarTFrntLe:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = None
        signal_description = "Compartment Front Left Area Target Hex Air Temperature"
        signal_length = 13
        start_position = 10
        value_definition = {}

    class CmptmtTSpHexTarTReRi:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = None
        signal_description = "Compartment Rear Right Area Target Hex Air Temperature"
        signal_length = 13
        start_position = 29
        value_definition = {}

    class CmptmtTSpHexTarTRe:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = None
        signal_description = "Compartment Rear Target Hex Air Temperature"
        signal_length = 13
        start_position = 32
        value_definition = {}

    class CmptmtTSpHexTarTReLe:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = None
        signal_description = "Compartment Rear Left Area Target Hex Air Temperature"
        signal_length = 13
        start_position = 51
        value_definition = {}

    class CmptmtTSpHexTarTFrntRi:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = None
        signal_description = "Compartment Front Right Area Target Hex Air Temperature"
        signal_length = 13
        start_position = 70
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu77:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40204D
    pdu_length_bytes = 4
    receiver = ['CCUMCUCD']
    send_type = "EventTriggered"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'DiagDTCInfoRec': ['DiagDTCInfoRecDTCCode', 'DiagDTCInfoRecDTCStatus']}

    class DiagDTCInfoRecDTCCode:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "DTC Code info"
        signal_length = 24
        start_position = 7
        value_definition = {}

    class DiagDTCInfoRecDTCStatus:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "DTC status flag"
        signal_length = 8
        start_position = 31
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu65:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402041
    pdu_length_bytes = 2
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'CmptmtThermReq': ['CmptmtThermReqReRi', 'CmptmtThermReqReLe', 'CmptmtThermReqFrntLe', 'CmptmtThermReqFrntRi']}

    class CmptmtThermReqReRi:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Compartment Rear Right Area Thermal Request"
        signal_length = 3
        start_position = 7
        value_definition = {'0x0': ' CmptHpMode_Idle', '0x1': ' CmptHpMode_Vent', '0x2': ' CmptHpMode_Heat', '0x3': ' CmptHpMode_Cool', '0x4': ' CmptHpMode_Dehum', '0x5': ' CmptHpMode_Cool_Heat', '0x6': ' CmptHpMode_Reserve'}

    class CmptmtThermReqReLe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Compartment Rear Left Area Thermal Request"
        signal_length = 3
        start_position = 4
        value_definition = {'0x0': ' CmptHpMode_Idle', '0x1': ' CmptHpMode_Vent', '0x2': ' CmptHpMode_Heat', '0x3': ' CmptHpMode_Cool', '0x4': ' CmptHpMode_Dehum', '0x5': ' CmptHpMode_Cool_Heat', '0x6': ' CmptHpMode_Reserve'}

    class CmptmtThermReqFrntLe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Compartment Front Left Area Thermal Request"
        signal_length = 3
        start_position = 1
        value_definition = {'0x0': ' CmptHpMode_Idle', '0x1': ' CmptHpMode_Vent', '0x2': ' CmptHpMode_Heat', '0x3': ' CmptHpMode_Cool', '0x4': ' CmptHpMode_Dehum', '0x5': ' CmptHpMode_Cool_Heat', '0x6': ' CmptHpMode_Reserve'}

    class CmptmtThermReqFrntRi:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Compartment Front Right Area Thermal Request"
        signal_length = 3
        start_position = 14
        value_definition = {'0x0': ' CmptHpMode_Idle', '0x1': ' CmptHpMode_Vent', '0x2': ' CmptHpMode_Heat', '0x3': ' CmptHpMode_Cool', '0x4': ' CmptHpMode_Dehum', '0x5': ' CmptHpMode_Cool_Heat', '0x6': ' CmptHpMode_Reserve'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu95:
    base_type = "Boolean"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40205F
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "EventTriggered"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class HiUDeactvn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "To notify the BECM GB32960 of high voltage actions under the power system, inform the BECM to remain awake for 1 hour and monitor level 3 and level 4 alarms if any alarms occur during the monitoring period."
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu82:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402052
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-200ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class DisplayTheme:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "The UI layout of full/half width steering wheel to Notify the Front Screen"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' DisplayTheme_Unknow', '0x1': ' DisplayTheme1', '0x2': ' DisplayTheme2', '0x3': ' DisplayTheme3'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu100:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402064
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class IntllntChrgnReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Intelligent charge request"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' ReqSts2_Default', '0x1': ' ReqSts2_NotReqd', '0x2': ' ReqSts2_Reqd', '0x3': ' ReqSts2_Reserved'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu101:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402065
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class SetDrivingwithoutkeyProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Set UsageMode Up Proxy Request"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' ReqSts1_NotReqd', '0x1': ' ReqSts1_Reqd'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu102:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402066
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class KeepUsgModProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Keep UsageMode Proxy Request"
        signal_length = 4
        start_position = 7
        value_definition = {'0x0': ' UsgModReq_Idle', '0x1': ' UsgModReq_Inactive', '0x2': ' UsgModReq_Convenience', '0xD': ' UsgModReq_Driving'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu108:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40206C
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class Mic1FltSts:
        comments = ""
        factor = 1.0
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Mic1 Fault Status"
        signal_length = 8
        start_position = 7
        value_definition = {'0x0': ' Mic1FltSts_Normal', '0x1': ' Mic1FltSts_OpenCircuit', '0x2': ' Mic1FltSts_ShorttoGround', '0x3': ' Mic1FltSts_ShorttoBattery', '0x4': ' Mic1FltSts_WrongPort', '0x5': ' Mic1FltSts_ReverseWire', '0x6': ' Mic1FltSts_ShortofWires', '0xFF': ' Mic1FltSts_Unknown'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu109:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40206D
    pdu_length_bytes = 8
    receiver = ['CCUMCUCD']
    send_type = "EventTriggered"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class NextAlarmTimestamp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "the time of next alarm event, unit:s"
        signal_length = 64
        start_position = 7
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu103:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402067
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class KeyFindReqFromService:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Key find request from Service"
        signal_length = 4
        start_position = 7
        value_definition = {'0x0': ' KeyLocnReq_Idle', '0x1': ' KeyLocnReq_PEAllExtAndInt', '0x2': ' KeyLocnReq_PEAllExt', '0x3': ' KeyLocnReq_PEDrvrExt', '0x4': ' KeyLocnReq_PEPassExt', '0x5': ' KeyLocnReq_PEFrntExt', '0x6': ' KeyLocnReq_PERearExt', '0x7': ' KeyLocnReq_PEAllInt', '0x8': ' KeyLocnReq_PSAllInt', '0x9': ' KeyLocnReq_Reserved1', '0xA': ' KeyLocnReq_Reserved2'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu106:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40206A
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class LuminanceLevelReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "The command to adjust the front screen brightness"
        signal_length = 8
        start_position = 7
        value_definition = {'0xFF': 'BattSOH_Invalid'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu107:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40206B
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class MaxAcInpCurrentSet:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "set the input current"
        signal_length = 8
        start_position = 7
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu104:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402068
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class LnchModReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Launch mode switch request. "
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' ReqSts2_Default', '0x1': ' ReqSts2_NotReqd', '0x2': ' ReqSts2_Reqd', '0x3': ' ReqSts2_Reserved'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu105:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402069
    pdu_length_bytes = 2
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class LocalBookChrgnTarVal:
        comments = ""
        factor = 0.1
        initial_value = 1020
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Local book charge target SOC value"
        signal_length = 10
        start_position = 7
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu114:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402072
    pdu_length_bytes = 3
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'NormFRPwrDoorCtrl': ['NormFRPwrDoorCtrlMoveCtrlSrc', 'NormFRPwrDoorCtrlMovCtrl', 'NormFRPwrDoorCtrlChks', 'NormFRPwrDoorCtrlCntr']}

    class NormFRPwrDoorCtrlMoveCtrlSrc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "power side door move control trigsrc"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' CtrlTrigsrc_NoCtrlReq', '0x1': ' CtrlTrigsrc_OutdCtrl', '0x2': ' CtrlTrigsrc_InsdCtrl'}

    class NormFRPwrDoorCtrlMovCtrl:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "power side door move control"
        signal_length = 3
        start_position = 5
        value_definition = {'0x0': ' DoorCtrlReq_Idle', '0x1': ' DoorCtrlReq_Open', '0x2': ' DoorCtrlReq_Close', '0x3': ' DoorCtrlReq_Stop', '0x4': ' DoorCtrlReq_OpenMinAng', '0x5': ' DoorCtrlReq_Resd2'}

    class NormFRPwrDoorCtrlChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "checksum"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class NormFRPwrDoorCtrlCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "counter"
        signal_length = 4
        start_position = 23
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu119:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402077
    pdu_length_bytes = 3
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'NormRRPwrDoorCtrl': ['NormRRPwrDoorCtrlMovCtrl', 'NormRRPwrDoorCtrlMoveCtrlSrc', 'NormRRPwrDoorCtrlChks', 'NormRRPwrDoorCtrlCntr']}

    class NormRRPwrDoorCtrlMovCtrl:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "power side door move control"
        signal_length = 3
        start_position = 7
        value_definition = {'0x0': ' DoorCtrlReq_Idle', '0x1': ' DoorCtrlReq_Open', '0x2': ' DoorCtrlReq_Close', '0x3': ' DoorCtrlReq_Stop', '0x4': ' DoorCtrlReq_OpenMinAng', '0x5': ' DoorCtrlReq_Resd2'}

    class NormRRPwrDoorCtrlMoveCtrlSrc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "power side door move control trigsrc"
        signal_length = 2
        start_position = 4
        value_definition = {'0x0': ' CtrlTrigsrc_NoCtrlReq', '0x1': ' CtrlTrigsrc_OutdCtrl', '0x2': ' CtrlTrigsrc_InsdCtrl'}

    class NormRRPwrDoorCtrlChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "checksum"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class NormRRPwrDoorCtrlCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "counter"
        signal_length = 4
        start_position = 23
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu149:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402095
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class SetTrlrModSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Set Trailer Mode Status"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu158:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40209E
    pdu_length_bytes = 3
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'VirtGearShiftModeReq': ['VirtGearShiftModeReqVirtShiftModeSts', 'VirtGearShiftModeReqChks', 'VirtGearShiftModeReqCntr']}

    class VirtGearShiftModeReqVirtShiftModeSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Virtual gear shift mode request"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class VirtGearShiftModeReqChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Checksum"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class VirtGearShiftModeReqCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Counter"
        signal_length = 4
        start_position = 23
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu132:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402084
    pdu_length_bytes = 2
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class ResdSigForTherm04:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Reserved Signal For Thermal"
        signal_length = 16
        start_position = 7
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu140:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40208C
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "EventTriggered"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class RoofFolderDisplayFoldedReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "The folded/unfolded requirement of RFD"
        signal_length = 2
        start_position = 7
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu141:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40208D
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class ScreenDispErrProcess:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "The Cabin Process Command According to the Front Srceen Status reported"
        signal_length = 2
        start_position = 7
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu118:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402076
    pdu_length_bytes = 4
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'NormRLPwrDoorPosnCtrl': ['NormRLPwrDoorPosnCtrlPosnCtrlSrc', 'NormRLPwrDoorPosnCtrlPosnCtrl', 'NormRLPwrDoorPosnCtrlCntr', 'NormRLPwrDoorPosnCtrlChks']}

    class NormRLPwrDoorPosnCtrlPosnCtrlSrc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "power side door position control trigsrc"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' CtrlTrigsrc_NoCtrlReq', '0x1': ' CtrlTrigsrc_OutdCtrl', '0x2': ' CtrlTrigsrc_InsdCtrl'}

    class NormRLPwrDoorPosnCtrlPosnCtrl:
        comments = ""
        factor = 1.0
        initial_value = 101
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "power side door position control"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class NormRLPwrDoorPosnCtrlCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "rolling counter"
        signal_length = 4
        start_position = 23
        value_definition = {}

    class NormRLPwrDoorPosnCtrlChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "checksum"
        signal_length = 8
        start_position = 31
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu133:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402085
    pdu_length_bytes = 2
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class ResdSigForTherm05:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Reserved Signal For Thermal"
        signal_length = 16
        start_position = 7
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu120:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402078
    pdu_length_bytes = 3
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'NormRRPwrDoorPosnCtrl': ['NormRRPwrDoorPosnCtrlPosnCtrl', 'NormRRPwrDoorPosnCtrlPosnCtrlSrc', 'NormRRPwrDoorPosnCtrlCntr', 'NormRRPwrDoorPosnCtrlChks']}

    class NormRRPwrDoorPosnCtrlPosnCtrl:
        comments = ""
        factor = 1.0
        initial_value = 101
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "power side door position control"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class NormRRPwrDoorPosnCtrlPosnCtrlSrc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "power side door position control trigsrc"
        signal_length = 2
        start_position = 15
        value_definition = {'0x0': ' CtrlTrigsrc_NoCtrlReq', '0x1': ' CtrlTrigsrc_OutdCtrl', '0x2': ' CtrlTrigsrc_InsdCtrl'}

    class NormRRPwrDoorPosnCtrlCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "rolling counter"
        signal_length = 4
        start_position = 13
        value_definition = {}

    class NormRRPwrDoorPosnCtrlChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "checksum"
        signal_length = 8
        start_position = 23
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu131:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402083
    pdu_length_bytes = 2
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class ResdSigForTherm03:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Reserved Signal For Thermal"
        signal_length = 16
        start_position = 7
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu150:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402096
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class StrtInhbProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Start Inhibit Proxy Request"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' ReqSts1_NotReqd', '0x1': ' ReqSts1_Reqd'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu123:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40207B
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class PlsHeatgReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Pulse heating enable form service"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu124:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40207C
    pdu_length_bytes = 48
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-1000ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'PNCRequest': ['PNCRequestPNC1', 'PNCRequestPNC20', 'PNCRequestPNC14', 'PNCRequestPNC18', 'PNCRequestPNC4', 'PNCRequestPNC26', 'PNCRequestPNC46', 'PNCRequestPNC25', 'PNCRequestPNC5', 'PNCRequestPNC13', 'PNCRequestPNC30', 'PNCRequestPNC2', 'PNCRequestPNC48', 'PNCRequestPNC15', 'PNCRequestPNC12', 'PNCRequestPNC31', 'PNCRequestPNC37', 'PNCRequestPNC19', 'PNCRequestPNC24', 'PNCRequestPNC23', 'PNCRequestPNC3', 'PNCRequestPNC28', 'PNCRequestPNC42', 'PNCRequestPNC39', 'PNCRequestPNC45', 'PNCRequestPNC17', 'PNCRequestPNC22', 'PNCRequestPNC11', 'PNCRequestPNC34', 'PNCRequestPNC36', 'PNCRequestPNC43', 'PNCRequestPNC41', 'PNCRequestPNC8', 'PNCRequestPNC6', 'PNCRequestPNC29', 'PNCRequestPNC9', 'PNCRequestPNC10', 'PNCRequestPNC21', 'PNCRequestPNC40', 'PNCRequestPNC7', 'PNCRequestPNC16', 'PNCRequestPNC38', 'PNCRequestPNC33', 'PNCRequestPNC27', 'PNCRequestPNC32', 'PNCRequestPNC44', 'PNCRequestPNC47', 'PNCRequestPNC35']}

    class PNCRequestPNC1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "PNC1"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class PNCRequestPNC20:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "PNC20"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class PNCRequestPNC14:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "PNC14"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class PNCRequestPNC18:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "PNC18"
        signal_length = 8
        start_position = 31
        value_definition = {}

    class PNCRequestPNC4:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "PNC4"
        signal_length = 8
        start_position = 39
        value_definition = {}

    class PNCRequestPNC26:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "PNC26"
        signal_length = 8
        start_position = 47
        value_definition = {}

    class PNCRequestPNC46:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "PNC46"
        signal_length = 8
        start_position = 55
        value_definition = {}

    class PNCRequestPNC25:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "PNC25"
        signal_length = 8
        start_position = 63
        value_definition = {}

    class PNCRequestPNC5:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "PNC5"
        signal_length = 8
        start_position = 71
        value_definition = {}

    class PNCRequestPNC13:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "PNC13"
        signal_length = 8
        start_position = 79
        value_definition = {}

    class PNCRequestPNC30:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "PNC30"
        signal_length = 8
        start_position = 87
        value_definition = {}

    class PNCRequestPNC2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "PNC2"
        signal_length = 8
        start_position = 95
        value_definition = {}

    class PNCRequestPNC48:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "PNC48"
        signal_length = 8
        start_position = 103
        value_definition = {}

    class PNCRequestPNC15:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "PNC15"
        signal_length = 8
        start_position = 111
        value_definition = {}

    class PNCRequestPNC12:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "PNC12"
        signal_length = 8
        start_position = 119
        value_definition = {}

    class PNCRequestPNC31:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "PNC31"
        signal_length = 8
        start_position = 127
        value_definition = {}

    class PNCRequestPNC37:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "PNC37"
        signal_length = 8
        start_position = 135
        value_definition = {}

    class PNCRequestPNC19:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "PNC19"
        signal_length = 8
        start_position = 143
        value_definition = {}

    class PNCRequestPNC24:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "PNC24"
        signal_length = 8
        start_position = 151
        value_definition = {}

    class PNCRequestPNC23:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "PNC23"
        signal_length = 8
        start_position = 159
        value_definition = {}

    class PNCRequestPNC3:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "PNC3"
        signal_length = 8
        start_position = 167
        value_definition = {}

    class PNCRequestPNC28:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "PNC28"
        signal_length = 8
        start_position = 175
        value_definition = {}

    class PNCRequestPNC42:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "PNC42"
        signal_length = 8
        start_position = 183
        value_definition = {}

    class PNCRequestPNC39:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "PNC39"
        signal_length = 8
        start_position = 191
        value_definition = {}

    class PNCRequestPNC45:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "PNC45"
        signal_length = 8
        start_position = 199
        value_definition = {}

    class PNCRequestPNC17:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "PNC17"
        signal_length = 8
        start_position = 207
        value_definition = {}

    class PNCRequestPNC22:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "PNC22"
        signal_length = 8
        start_position = 215
        value_definition = {}

    class PNCRequestPNC11:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "PNC11"
        signal_length = 8
        start_position = 223
        value_definition = {}

    class PNCRequestPNC34:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "PNC34"
        signal_length = 8
        start_position = 231
        value_definition = {}

    class PNCRequestPNC36:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "PNC36"
        signal_length = 8
        start_position = 239
        value_definition = {}

    class PNCRequestPNC43:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "PNC43"
        signal_length = 8
        start_position = 247
        value_definition = {}

    class PNCRequestPNC41:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "PNC41"
        signal_length = 8
        start_position = 255
        value_definition = {}

    class PNCRequestPNC8:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "PNC8"
        signal_length = 8
        start_position = 263
        value_definition = {}

    class PNCRequestPNC6:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "PNC6"
        signal_length = 8
        start_position = 271
        value_definition = {}

    class PNCRequestPNC29:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "PNC29"
        signal_length = 8
        start_position = 279
        value_definition = {}

    class PNCRequestPNC9:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "PNC9"
        signal_length = 8
        start_position = 287
        value_definition = {}

    class PNCRequestPNC10:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "PNC10"
        signal_length = 8
        start_position = 295
        value_definition = {}

    class PNCRequestPNC21:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "PNC21"
        signal_length = 8
        start_position = 303
        value_definition = {}

    class PNCRequestPNC40:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "PNC40"
        signal_length = 8
        start_position = 311
        value_definition = {}

    class PNCRequestPNC7:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "PNC7"
        signal_length = 8
        start_position = 319
        value_definition = {}

    class PNCRequestPNC16:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "PNC16"
        signal_length = 8
        start_position = 327
        value_definition = {}

    class PNCRequestPNC38:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "PNC38"
        signal_length = 8
        start_position = 335
        value_definition = {}

    class PNCRequestPNC33:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "PNC33"
        signal_length = 8
        start_position = 343
        value_definition = {}

    class PNCRequestPNC27:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "PNC27"
        signal_length = 8
        start_position = 351
        value_definition = {}

    class PNCRequestPNC32:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "PNC32"
        signal_length = 8
        start_position = 359
        value_definition = {}

    class PNCRequestPNC44:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "PNC44"
        signal_length = 8
        start_position = 367
        value_definition = {}

    class PNCRequestPNC47:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "PNC47"
        signal_length = 8
        start_position = 375
        value_definition = {}

    class PNCRequestPNC35:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "PNC35"
        signal_length = 8
        start_position = 383
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu147:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402093
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class SetDynoModProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Set DynoMode Proxy Request"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu144:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402090
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class SetCarModProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Set CarMode Proxy Request"
        signal_length = 4
        start_position = 7
        value_definition = {'0x0': ' CarModReq_Idle', '0x1': ' CarModReq_Norm', '0x2': ' CarModReq_Trnsp', '0x3': ' CarModReq_Fcy', '0x4': ' CarModReq_Exhib'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu134:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402086
    pdu_length_bytes = 2
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class ResdSigForTherm06:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Reserved Signal For Thermal"
        signal_length = 16
        start_position = 7
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu136:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402088
    pdu_length_bytes = 2
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class ResdSigForTherm08:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Reserved Signal For Thermal"
        signal_length = 16
        start_position = 7
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu121:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402079
    pdu_length_bytes = 3
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'NormTrunkMovCtrl': ['NormTrunkMovCtrlMovCtrl', 'NormTrunkMovCtrlMoveCtrlSrc', 'NormTrunkMovCtrlChks', 'NormTrunkMovCtrlCntr']}

    class NormTrunkMovCtrlMovCtrl:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "trunk move control "
        signal_length = 3
        start_position = 7
        value_definition = {'0x0': ' DoorCtrlReq_Idle', '0x1': ' DoorCtrlReq_Open', '0x2': ' DoorCtrlReq_Close', '0x3': ' DoorCtrlReq_Stop', '0x4': ' DoorCtrlReq_OpenMinAng', '0x5': ' DoorCtrlReq_Resd2'}

    class NormTrunkMovCtrlMoveCtrlSrc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "trigger source of trunk move control "
        signal_length = 2
        start_position = 4
        value_definition = {'0x0': ' CtrlTrigsrc_NoCtrlReq', '0x1': ' CtrlTrigsrc_OutdCtrl', '0x2': ' CtrlTrigsrc_InsdCtrl'}

    class NormTrunkMovCtrlChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "checksum"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class NormTrunkMovCtrlCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "counter"
        signal_length = 4
        start_position = 23
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu154:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40209A
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class VehAxleTqDistbnModReq:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Target vehicle axle torque distribution mode"
        signal_length = 4
        start_position = 7
        value_definition = {'0x0': ' VehAxleTqDistbnMod_Initial', '0x1': ' VehAxleTqDistbnMod_Auto', '0x2': ' VehAxleTqDistbnMod_Manual', '0x3': ' VehAxleTqDistbnMod_Unknow', '0x4': ' VehAxleTqDistbnMod_Reserved'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu160:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x4020A0
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class WirelschrgActvReqFromHmi:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Wireless charging activation request from Hmi"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' OffOnCmd_NoCmd', '0x1': ' OffOnCmd_Off', '0x2': ' OffOnCmd_On'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu126:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40207E
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class PrpsnEgyRgnLvlSet:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "The energy recovery level set by the driver supports stepless energy regulation, the accuracy is 1percentage, and the range is 1-100 percentage."
        signal_length = 8
        start_position = 7
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu161:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x4020A1
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class WirelschrgActvReqFromHmiPass:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Wireless charging activation request from Hmi of passenger side"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' OffOnCmd_NoCmd', '0x1': ' OffOnCmd_Off', '0x2': ' OffOnCmd_On'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu155:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40209B
    pdu_length_bytes = 2
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'VehAxleTqDistbnReq': ['VehAxleTqDistbnReqManualAuto', 'VehAxleTqDistbnReqPerc']}

    class VehAxleTqDistbnReqManualAuto:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Can distinguish between manual and automatic."
        signal_length = 4
        start_position = 7
        value_definition = {'0x0': ' VehAxleTqDistbnMod_Initial', '0x1': ' VehAxleTqDistbnMod_Auto', '0x2': ' VehAxleTqDistbnMod_Manual', '0x3': ' VehAxleTqDistbnMod_Unknow', '0x4': ' VehAxleTqDistbnMod_Reserved'}

    class VehAxleTqDistbnReqPerc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "The range is 0-100 percentage, 1 represents the front motor distribution 100 percentage, the rear motor distribution 0, 100 percentage means that the front motor is allocated 0, the back motor is allocated 100percentage, and so on. "
        signal_length = 8
        start_position = 15
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu113:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402071
    pdu_length_bytes = 4
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'NormFLPwrDoorPosnCtrl': ['NormFLPwrDoorPosnCtrlPosnCtrl', 'NormFLPwrDoorPosnCtrlPosnCtrlSrc', 'NormFLPwrDoorPosnCtrlChks', 'NormFLPwrDoorPosnCtrlCntr']}

    class NormFLPwrDoorPosnCtrlPosnCtrl:
        comments = ""
        factor = 1.0
        initial_value = 101
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "power side door position control "
        signal_length = 8
        start_position = 7
        value_definition = {}

    class NormFLPwrDoorPosnCtrlPosnCtrlSrc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "power side door position control trigsrc"
        signal_length = 2
        start_position = 15
        value_definition = {'0x0': ' CtrlTrigsrc_NoCtrlReq', '0x1': ' CtrlTrigsrc_OutdCtrl', '0x2': ' CtrlTrigsrc_InsdCtrl'}

    class NormFLPwrDoorPosnCtrlChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "checksum"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class NormFLPwrDoorPosnCtrlCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "rolling counter"
        signal_length = 4
        start_position = 31
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu139:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40208B
    pdu_length_bytes = 1500
    receiver = ['CCUMCUCD']
    send_type = "EventTriggered"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class RKEDataDwnLink:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Opaque"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "used to send RKE response data from Digital Key Service to MCU"
        signal_length = 32760
        start_position = 0
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu159:
    base_type = "Boolean"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40209F
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class WakeupADProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "wakeup AD domain request from service proxy"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu156:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40209C
    pdu_length_bytes = 1008
    receiver = ['CCUMCUCD']
    send_type = "EventTriggered"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class VehCfgDataGrpOrg:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Opaque"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Vehicle Configuration Data Group"
        signal_length = 8064
        start_position = 0
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu137:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402089
    pdu_length_bytes = 2
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class ResdSigForTherm09:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Reserved Signal For Thermal"
        signal_length = 16
        start_position = 7
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu142:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40208E
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class ScrnGearLvrIndcnVirt:
        comments = ""
        factor = 1.0
        initial_value = 7
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Virtual gear information sent by screen shift. "
        signal_length = 3
        start_position = 7
        value_definition = {'0x0': ' GearLvrIndcn_Default', '0x1': ' GearLvrIndcn_P', '0x2': ' GearLvrIndcn_R', '0x3': ' GearLvrIndcn_N', '0x4': ' GearLvrIndcn_D', '0x5': ' GearLvrIndcn_Reserved1', '0x6': ' GearLvrIndcn_Reserved2', '0x7': ' GearLvrIndcn_Undefd'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu130:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402082
    pdu_length_bytes = 2
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class ResdSigForTherm02:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Reserved Signal For Thermal"
        signal_length = 16
        start_position = 7
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu151:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402097
    pdu_length_bytes = 6
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'ThermLoadDistbReqFromSrv': ['ThermLoadDistbReqFromSrvCmptmtLoadCtrl', 'ThermLoadDistbReqFromSrvHVBattLoadLim', 'ThermLoadDistbReqFromSrvCmptmtLoadLim', 'ThermLoadDistbReqFromSrvHVBattLoadCtrl', 'ThermLoadDistbReqFromSrvSourceID']}

    class ThermLoadDistbReqFromSrvCmptmtLoadCtrl:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Compartment thermal management load control enable"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class ThermLoadDistbReqFromSrvHVBattLoadLim:
        comments = ""
        factor = 10.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Hvbatt thermal management load control limlit"
        signal_length = 13
        start_position = 6
        value_definition = {}

    class ThermLoadDistbReqFromSrvCmptmtLoadLim:
        comments = ""
        factor = 10.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Compartment thermal management load control limit"
        signal_length = 13
        start_position = 9
        value_definition = {}

    class ThermLoadDistbReqFromSrvHVBattLoadCtrl:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Hvbatt thermal management load control enable"
        signal_length = 1
        start_position = 28
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class ThermLoadDistbReqFromSrvSourceID:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "SourceID"
        signal_length = 16
        start_position = 39
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu115:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402073
    pdu_length_bytes = 4
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'NormFRPwrDoorPosnCtrl': ['NormFRPwrDoorPosnCtrlPosnCtrlSrc', 'NormFRPwrDoorPosnCtrlPosnCtrl', 'NormFRPwrDoorPosnCtrlChks', 'NormFRPwrDoorPosnCtrlCntr']}

    class NormFRPwrDoorPosnCtrlPosnCtrlSrc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "power side door position control trigsrc"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' CtrlTrigsrc_NoCtrlReq', '0x1': ' CtrlTrigsrc_OutdCtrl', '0x2': ' CtrlTrigsrc_InsdCtrl'}

    class NormFRPwrDoorPosnCtrlPosnCtrl:
        comments = ""
        factor = 1.0
        initial_value = 101
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "power side door position control "
        signal_length = 8
        start_position = 15
        value_definition = {}

    class NormFRPwrDoorPosnCtrlChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "checksum"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class NormFRPwrDoorPosnCtrlCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "rolling counter"
        signal_length = 4
        start_position = 31
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu117:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402075
    pdu_length_bytes = 3
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'NormRLPwrDoorCtrl': ['NormRLPwrDoorCtrlMovCtrl', 'NormRLPwrDoorCtrlMoveCtrlSrc', 'NormRLPwrDoorCtrlCntr', 'NormRLPwrDoorCtrlChks']}

    class NormRLPwrDoorCtrlMovCtrl:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "power side door move control"
        signal_length = 3
        start_position = 7
        value_definition = {'0x0': ' DoorCtrlReq_Idle', '0x1': ' DoorCtrlReq_Open', '0x2': ' DoorCtrlReq_Close', '0x3': ' DoorCtrlReq_Stop', '0x4': ' DoorCtrlReq_OpenMinAng', '0x5': ' DoorCtrlReq_Resd2'}

    class NormRLPwrDoorCtrlMoveCtrlSrc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "power side door move control trigsrc"
        signal_length = 2
        start_position = 4
        value_definition = {'0x0': ' CtrlTrigsrc_NoCtrlReq', '0x1': ' CtrlTrigsrc_OutdCtrl', '0x2': ' CtrlTrigsrc_InsdCtrl'}

    class NormRLPwrDoorCtrlCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "counter"
        signal_length = 4
        start_position = 2
        value_definition = {}

    class NormRLPwrDoorCtrlChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "checksum"
        signal_length = 8
        start_position = 23
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu116:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402074
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class NormHoodRelsCtrl:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "hood release control"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu127:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40207F
    pdu_length_bytes = 7
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'PWTThermReqFromSrv': ['PWTThermReqFromSrvCoolgReq', 'PWTThermReqFromSrvCooltFlwReq', 'PWTThermReqFromSrvCooltTMaxReq', 'PWTThermReqFromSrvCooltTMinReq', 'PWTThermReqFromSrvCoolgReqLvl', 'PWTThermReqFromSrvSourceID']}

    class PWTThermReqFromSrvCoolgReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Pwt thermal management cooling request from smart app"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' YesNo2_No', '0x1': ' YesNo2_Yes'}

    class PWTThermReqFromSrvCooltFlwReq:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Pwt thermal management coolant flow  request from smart app"
        signal_length = 9
        start_position = 6
        value_definition = {}

    class PWTThermReqFromSrvCooltTMaxReq:
        comments = ""
        factor = 0.1
        initial_value = 600
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -60
        sig_ub = None
        signal_description = "Pwt thermal management coolant temperature request from smart app"
        signal_length = 11
        start_position = 13
        value_definition = {}

    class PWTThermReqFromSrvCooltTMinReq:
        comments = ""
        factor = 0.1
        initial_value = 600
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -60
        sig_ub = None
        signal_description = "Pwt thermal management coolant temperature request from smart app"
        signal_length = 11
        start_position = 18
        value_definition = {}

    class PWTThermReqFromSrvCoolgReqLvl:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Pwt thermal management cooling level request from smart app"
        signal_length = 2
        start_position = 39
        value_definition = {'0x0': ' ReqLvl_NoReq', '0x1': ' ReqLvl_LoReq', '0x2': ' ReqLvl_MidReq', '0x3': ' ReqLvl_HiReq'}

    class PWTThermReqFromSrvSourceID:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "SourceID"
        signal_length = 16
        start_position = 47
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu145:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402091
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class SetDigKeyMaxWakeUpTime:
        comments = ""
        factor = 1.0
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "digitalKey Max WakeUp Time"
        signal_length = 8
        start_position = 7
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu148:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402094
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class SetFotaModProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = ""
        signal_length = 8
        start_position = 7
        value_definition = {'0x0': ' FotaModReq_Noreq', '0x1': ' FotaModReq_Idle', '0x2': ' FotaModReq_Update', '0x3': ' FotaModReq_UpdateFail'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu153:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402099
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class V2XDchaSwt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "The state of which discharge type customer selected"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' DisChrgrSW_Off', '0x1': ' DisChrgrSW_V2V', '0x2': ' DisChrgrSW_V2L', '0x3': ' DisChrgrSW_Reserved'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu143:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40208F
    pdu_length_bytes = 3
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'ScrnGearShiftReq2': ['ScrnGearShiftReq2GearFltSts', 'ScrnGearShiftReq2GearReq', 'ScrnGearShiftReq2Chks', 'ScrnGearShiftReq2Cntr']}

    class ScrnGearShiftReq2GearFltSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Screen Shift request signal Group 1 quality status."
        signal_length = 3
        start_position = 7
        value_definition = {'0x0': ' GearFltSts_Normal', '0x1': ' GearFltSts_PFlt', '0x2': ' GearFltSts_RFlt', '0x3': ' GearFltSts_NFlt', '0x4': ' GearFltSts_DFlt', '0x5': ' GearFltSts_SrvReq', '0x6': ' GearFltSts_Reserved1', '0x7': ' GearFltSts_Reserved2'}

    class ScrnGearShiftReq2GearReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Screen Shift request signal Group 2, containing NoReq/P/R/N (reserved) /D files.E2E verification."
        signal_length = 3
        start_position = 4
        value_definition = {'0x0': ' GearLvrIndcn_Default', '0x1': ' GearLvrIndcn_P', '0x2': ' GearLvrIndcn_R', '0x3': ' GearLvrIndcn_N', '0x4': ' GearLvrIndcn_D', '0x5': ' GearLvrIndcn_Reserved1', '0x6': ' GearLvrIndcn_Reserved2', '0x7': ' GearLvrIndcn_Undefd'}

    class ScrnGearShiftReq2Chks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Checksum"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class ScrnGearShiftReq2Cntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Counter"
        signal_length = 4
        start_position = 23
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu122:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40207A
    pdu_length_bytes = 4
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'NormTrunkPosnCtrl': ['NormTrunkPosnCtrlPosnCtrlSrc', 'NormTrunkPosnCtrlPosnCtrl', 'NormTrunkPosnCtrlCntr', 'NormTrunkPosnCtrlChks']}

    class NormTrunkPosnCtrlPosnCtrlSrc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "trigger source of trunk position control "
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' CtrlTrigsrc_NoCtrlReq', '0x1': ' CtrlTrigsrc_OutdCtrl', '0x2': ' CtrlTrigsrc_InsdCtrl'}

    class NormTrunkPosnCtrlPosnCtrl:
        comments = ""
        factor = 1.0
        initial_value = 101
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "trunk position control "
        signal_length = 8
        start_position = 15
        value_definition = {}

    class NormTrunkPosnCtrlCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "rolling counter"
        signal_length = 4
        start_position = 23
        value_definition = {}

    class NormTrunkPosnCtrlChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "checksum"
        signal_length = 8
        start_position = 31
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu146:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402092
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class SetDigKeyWakeUpZone:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Set Digital Key wakeup zone Status"
        signal_length = 3
        start_position = 7
        value_definition = {'0x0': ' DigKeyWakeUpZone_Unkown', '0x1': ' DigKeyWakeUpZone_Connected', '0x2': ' DigKeyWakeUpZone_Welcome', '0x3': ' DigKeyWakeUpZone_WalkAway', '0x4': ' DigKeyWakeUpZone_PE', '0x5': ' DigKeyWakeUpZone_Reserved1', '0x6': ' DigKeyWakeUpZone_Reserved2', '0x7': ' DigKeyWakeUpZone_Reserved3'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu125:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40207D
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class ProxySterSysWkReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "steeringsystem awake request from proxy"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' ReqSts1_NotReqd', '0x1': ' ReqSts1_Reqd'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu129:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402081
    pdu_length_bytes = 2
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class ResdSigForTherm01:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Reserved Signal For Thermal"
        signal_length = 16
        start_position = 7
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu110:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40206E
    pdu_length_bytes = 258
    receiver = ['CCUMCUCD']
    send_type = "EventTriggered"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class NodeListInfoOrg:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Opaque"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "List of Node"
        signal_length = 2064
        start_position = 0
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu138:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40208A
    pdu_length_bytes = 2
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class ResdSigForTherm10:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Reserved Signal For Thermal"
        signal_length = 16
        start_position = 7
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu112:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402070
    pdu_length_bytes = 3
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'NormFLPwrDoorCtrl': ['NormFLPwrDoorCtrlMovCtrl', 'NormFLPwrDoorCtrlMoveCtrlSrc', 'NormFLPwrDoorCtrlChks', 'NormFLPwrDoorCtrlCntr']}

    class NormFLPwrDoorCtrlMovCtrl:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "power side door move control "
        signal_length = 3
        start_position = 7
        value_definition = {'0x0': ' DoorCtrlReq_Idle', '0x1': ' DoorCtrlReq_Open', '0x2': ' DoorCtrlReq_Close', '0x3': ' DoorCtrlReq_Stop', '0x4': ' DoorCtrlReq_OpenMinAng', '0x5': ' DoorCtrlReq_Resd2'}

    class NormFLPwrDoorCtrlMoveCtrlSrc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "power side door move control trigsrc"
        signal_length = 2
        start_position = 4
        value_definition = {'0x0': ' CtrlTrigsrc_NoCtrlReq', '0x1': ' CtrlTrigsrc_OutdCtrl', '0x2': ' CtrlTrigsrc_InsdCtrl'}

    class NormFLPwrDoorCtrlChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "checksum"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class NormFLPwrDoorCtrlCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "counter"
        signal_length = 4
        start_position = 23
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu157:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40209D
    pdu_length_bytes = 17
    receiver = ['CCUMCUCD']
    send_type = "EventTriggered"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'VinOrg': ['VinOrgVinInfoBytePosn11', 'VinOrgVinInfoBytePosn15', 'VinOrgVinInfoBytePosn8', 'VinOrgVinInfoBytePosn5', 'VinOrgVinInfoBytePosn4', 'VinOrgVinInfoBytePosn13', 'VinOrgVinInfoBytePosn12', 'VinOrgVinInfoBytePosn14', 'VinOrgVinInfoBytePosn16', 'VinOrgVinInfoBytePosn7', 'VinOrgVinInfoBytePosn3', 'VinOrgVinInfoBytePosn9', 'VinOrgVinInfoBytePosn17', 'VinOrgVinInfoBytePosn1', 'VinOrgVinInfoBytePosn6', 'VinOrgVinInfoBytePosn10', 'VinOrgVinInfoBytePosn2']}

    class VinOrgVinInfoBytePosn11:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "VIN-11th code"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class VinOrgVinInfoBytePosn15:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "VIN-15th code"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class VinOrgVinInfoBytePosn8:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "VIN-8th code"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class VinOrgVinInfoBytePosn5:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "VIN-5th code"
        signal_length = 8
        start_position = 31
        value_definition = {}

    class VinOrgVinInfoBytePosn4:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "VIN-4th code"
        signal_length = 8
        start_position = 39
        value_definition = {}

    class VinOrgVinInfoBytePosn13:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "VIN-13th code"
        signal_length = 8
        start_position = 47
        value_definition = {}

    class VinOrgVinInfoBytePosn12:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "VIN-12th code"
        signal_length = 8
        start_position = 55
        value_definition = {}

    class VinOrgVinInfoBytePosn14:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "VIN-14th code"
        signal_length = 8
        start_position = 63
        value_definition = {}

    class VinOrgVinInfoBytePosn16:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "VIN-16th code"
        signal_length = 8
        start_position = 71
        value_definition = {}

    class VinOrgVinInfoBytePosn7:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "VIN-7th code"
        signal_length = 8
        start_position = 79
        value_definition = {}

    class VinOrgVinInfoBytePosn3:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "VIN-3rd code"
        signal_length = 8
        start_position = 87
        value_definition = {}

    class VinOrgVinInfoBytePosn9:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "VIN-9th code"
        signal_length = 8
        start_position = 95
        value_definition = {}

    class VinOrgVinInfoBytePosn17:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "VIN-17th code"
        signal_length = 8
        start_position = 103
        value_definition = {}

    class VinOrgVinInfoBytePosn1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "VIN-1st code"
        signal_length = 8
        start_position = 111
        value_definition = {}

    class VinOrgVinInfoBytePosn6:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "VIN-6th code"
        signal_length = 8
        start_position = 119
        value_definition = {}

    class VinOrgVinInfoBytePosn10:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "VIN-10th code"
        signal_length = 8
        start_position = 127
        value_definition = {}

    class VinOrgVinInfoBytePosn2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "VIN-2nd code"
        signal_length = 8
        start_position = 135
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu135:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402087
    pdu_length_bytes = 2
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class ResdSigForTherm07:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Reserved Signal For Thermal"
        signal_length = 16
        start_position = 7
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu128:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402080
    pdu_length_bytes = 2
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class RemBookChrgnTarVal:
        comments = ""
        factor = 0.1
        initial_value = 1020
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Remote book charge target SOC value"
        signal_length = 10
        start_position = 7
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu152:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x402098
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class TowModeSt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Tow mode state"
        signal_length = 3
        start_position = 7
        value_definition = {'0x0': ' TowMode_NoActv', '0x1': ' TowMode_Entering', '0x2': ' TowMode_Actv', '0x3': ' TowMode_Exiting', '0x4': ' TowMode_Reserved1', '0x5': ' TowMode_Reserved2'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu111:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40206F
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class NormChargeLidMoveCtrl:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "chargelid move control"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' OpenClsCtrlReq_Idle', '0x1': ' OpenClsCtrlReq_Open', '0x2': ' OpenClsCtrlReq_Close'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu162:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x4020A2
    pdu_length_bytes = 3
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-1000ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'AmbPBasLocn': ['AmbPBasLocnPQf', 'AmbPBasLocnP']}

    class AmbPBasLocnPQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "The signal quality of ambient pressure."
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class AmbPBasLocnP:
        comments = ""
        factor = 0.025
        initial_value = 40520
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Estimated ambient pressure based on global location."
        signal_length = 16
        start_position = 15
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu164:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x4020A4
    pdu_length_bytes = 3
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'ScrnGearShiftReq1': ['ScrnGearShiftReq1GearReq', 'ScrnGearShiftReq1Chks', 'ScrnGearShiftReq1Cntr', 'ScrnGearShiftReq1GearFltSts']}

    class ScrnGearShiftReq1GearReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Screen Shift request signal Group 1, containing NoReq/P/R/N (reserved) /D files.E2E verification."
        signal_length = 3
        start_position = 7
        value_definition = {'0x0': ' GearLvrIndcn_Default', '0x1': ' GearLvrIndcn_P', '0x2': ' GearLvrIndcn_R', '0x3': ' GearLvrIndcn_N', '0x4': ' GearLvrIndcn_D', '0x5': ' GearLvrIndcn_Reserved1', '0x6': ' GearLvrIndcn_Reserved2', '0x7': ' GearLvrIndcn_Undefd'}

    class ScrnGearShiftReq1Chks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Checksum"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class ScrnGearShiftReq1Cntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Counter"
        signal_length = 4
        start_position = 23
        value_definition = {}

    class ScrnGearShiftReq1GearFltSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Screen Shift request signal Group 1 quality status."
        signal_length = 3
        start_position = 19
        value_definition = {'0x0': ' GearFltSts_Normal', '0x1': ' GearFltSts_PFlt', '0x2': ' GearFltSts_RFlt', '0x3': ' GearFltSts_NFlt', '0x4': ' GearFltSts_DFlt', '0x5': ' GearFltSts_SrvReq', '0x6': ' GearFltSts_Reserved1', '0x7': ' GearFltSts_Reserved2'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu163:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x4020A3
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class DiagcComActv:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Represent Vehicle Diagnostic Requirement"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' YesNo2_No', '0x1': ' YesNo2_Yes'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu166:
    base_type = "Boolean"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x4020A6
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class VisFusnUsrInCarRes:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "user In car result with visual perception "
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu165:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x4020A5
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class SetUsgModDwnProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Set UsageMOde Down Proxy Request"
        signal_length = 4
        start_position = 7
        value_definition = {'0x0': ' UsgModReq_Idle', '0x1': ' UsgModReq_Inactive', '0x2': ' UsgModReq_Convenience', '0xD': ' UsgModReq_Driving'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu30:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40201E
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class AccrTqModSteplessReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "The drive torque mode is stepless,1-100 percentage."
        signal_length = 8
        start_position = 7
        value_definition = {}


class CCUSOCCDToCCUMCUCDEthSignalIPdu29:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40201D
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {}

    class BookChrgingSetReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Book charge set request from user"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' OffOnCmd_NoCmd', '0x1': ' OffOnCmd_Off', '0x2': ' OffOnCmd_On'}


class CCUSOCCDToCCUMCUCDEthSignalIPdu31:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x40201F
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient1"
    signal_group = {'HVActvReqFromSrv': ['HVActvReqFromSrvCmd', 'HVActvReqFromSrvSource']}

    class HVActvReqFromSrvCmd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "HV power on and off request"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class HVActvReqFromSrvSource:
        comments = ""
        factor = 1.0
        initial_value = 7
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "HV power on and off request source"
        signal_length = 3
        start_position = 5
        value_definition = {'0x0': ' HVOnSource1_Rem', '0x1': ' HVOnSource1_LV', '0x2': ' HVOnSource1_Therm', '0x3': ' HVOnSource1_Diag', '0x4': ' HVOnSource1_Reserved1', '0x5': ' HVOnSource1_Reserved2', '0x6': ' HVOnSource1_HVReld', '0x7': ' HVOnSource1_Default'}
