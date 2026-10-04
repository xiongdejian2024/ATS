

class CCUMCUCDMulticastEthSignalIPdu02:
    base_type = "Unsigned"
    client_socket = "SocketMulticast"
    pdu_header_id = 0x20FF02
    pdu_length_bytes = 32
    receiver = ['CCUMCUAD', 'CCUSOCCD', 'LCUL', 'LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUMCUCD"
    server_socket = "SocketCdMcuSoAdUDP"
    signal_group = {'Odometer': ['OdometerValidity', 'OdometerValue'], 'CenLockStsAndKeyID': ['CenLockStsAndKeyIDKeyIDByte1', 'CenLockStsAndKeyIDKeyIDByte8', 'CenLockStsAndKeyIDUpdateEvnt', 'CenLockStsAndKeyIDKeyIDByte5', 'CenLockStsAndKeyIDKeyIDByte10', 'CenLockStsAndKeyIDKeyIDByte13', 'CenLockStsAndKeyIDKeyIDByte15', 'CenLockStsAndKeyIDKeyIDByte3', 'CenLockStsAndKeyIDKeyIDByte0', 'CenLockStsAndKeyIDKeyIDByte12', 'CenLockStsAndKeyIDKeyIDByte11', 'CenLockStsAndKeyIDKeyIDByte2', 'CenLockStsAndKeyIDTrigSrc', 'CenLockStsAndKeyIDKeyIDByte9', 'CenLockStsAndKeyIDKeyIDByte6', 'CenLockStsAndKeyIDKeyIDByte7', 'CenLockStsAndKeyIDKeyIDByte4', 'CenLockStsAndKeyIDKeyIDByte14', 'CenLockStsAndKeyIDLockSts', 'CenLockStsAndKeyIDTrigSrcType'], 'CentralLockSts': ['CentralLockStsTrigSrc', 'CentralLockStsTrigSrc', 'CentralLockStsTrigSrc', 'CentralLockStsUpdateEvnt', 'CentralLockStsUpdateEvnt', 'CentralLockStsUpdateEvnt', 'CentralLockStsCenLockSts', 'CentralLockStsCenLockSts', 'CentralLockStsCenLockSts', 'CentralLockStsTrigSrcType', 'CentralLockStsTrigSrcType', 'CentralLockStsTrigSrcType']}

    class OdometerValidity:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 172
        signal_description = "Validity Flag"
        signal_length = 1
        start_position = 221
        value_definition = {'0x0': ' Validity_NotValid', '0x1': ' Validity_Valid'}

    class OdometerValue:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 172
        signal_description = "Vehicle Total Odometer,The Unit is Km"
        signal_length = 21
        start_position = 220
        value_definition = {}

    class AlrmSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 254
        signal_description = "Alarm status"
        signal_length = 2
        start_position = 5
        value_definition = {'0x0': ' AlrmSts_Disarmd', '0x1': ' AlrmSts_Armd', '0x2': ' AlrmSts_Actv', '0x3': ' AlrmSts_Reserved'}

    class AlrmToExtrLiFbVisReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 156
        signal_description = "Request from Alarm to Exterior light to flash exterior lights when vehicle is armed by passive arming"
        signal_length = 3
        start_position = 12
        value_definition = {'0x0': ' LockActvn_Off', '0x1': ' LockActvn_Unlock', '0x2': ' LockActvn_Lock', '0x3': ' LockActvn_Safe', '0x4': ' LockActvn_UnlockByCrash', '0x5': ' LockActvn_Resvd1', '0x6': ' LockActvn_Resvd2', '0x7': ' LockActvn_Resvd3'}

    class AlrmToExtrLiVisReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 155
        signal_description = "Alarm to external lighting request"
        signal_length = 2
        start_position = 9
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class AlrmTrigSrc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 154
        signal_description = "Alarm trigger source"
        signal_length = 4
        start_position = 3
        value_definition = {'0x0': ' AlrmTrigSrc_NoTrigSrc', '0x1': ' AlrmTrigSrc_DoorDrvr', '0x2': ' AlrmTrigSrc_DoorPass', '0x3': ' AlrmTrigSrc_DoorReLe', '0x4': ' AlrmTrigSrc_DoorReRi', '0x5': ' AlrmTrigSrc_Hood', '0x6': ' AlrmTrigSrc_Tr', '0x7': ' AlrmTrigSrc_IMMOFaild', '0x8': ' AlrmTrigSrc_Alcohol', '0x9': ' AlrmTrigSrc_SnsrSoundrBattBacked', '0xA': ' AlrmTrigSrc_SnsrIncln', '0xB': ' AlrmTrigSrc_SnsrIntrScanr', '0xC': ' AlrmTrigSrc_VSTD', '0xD': ' AlrmTrigSrc_Reserved1', '0xE': ' AlrmTrigSrc_Reserved2', '0xF': ' AlrmTrigSrc_Reserved3'}

    class CenLockStsAndKeyIDKeyIDByte1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 153
        signal_description = "key ID byte1"
        signal_length = 8
        start_position = 31
        value_definition = {}

    class CenLockStsAndKeyIDKeyIDByte8:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 153
        signal_description = "key ID byte8"
        signal_length = 8
        start_position = 87
        value_definition = {}

    class CenLockStsAndKeyIDUpdateEvnt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 153
        signal_description = "update event"
        signal_length = 1
        start_position = 149
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class CenLockStsAndKeyIDKeyIDByte5:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 153
        signal_description = "key ID byte5"
        signal_length = 8
        start_position = 63
        value_definition = {}

    class CenLockStsAndKeyIDKeyIDByte10:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 153
        signal_description = "key ID byte10"
        signal_length = 8
        start_position = 103
        value_definition = {}

    class CenLockStsAndKeyIDKeyIDByte13:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 153
        signal_description = "key ID byte13"
        signal_length = 8
        start_position = 127
        value_definition = {}

    class CenLockStsAndKeyIDKeyIDByte15:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 153
        signal_description = "key ID byte15"
        signal_length = 8
        start_position = 143
        value_definition = {}

    class CenLockStsAndKeyIDKeyIDByte3:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 153
        signal_description = "key ID byte3"
        signal_length = 8
        start_position = 47
        value_definition = {}

    class CenLockStsAndKeyIDKeyIDByte0:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 153
        signal_description = "key ID byte0"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class CenLockStsAndKeyIDKeyIDByte12:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 153
        signal_description = "key ID byte12"
        signal_length = 8
        start_position = 119
        value_definition = {}

    class CenLockStsAndKeyIDKeyIDByte11:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 153
        signal_description = "key ID byte11"
        signal_length = 8
        start_position = 111
        value_definition = {}

    class CenLockStsAndKeyIDKeyIDByte2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 153
        signal_description = "key ID byte2"
        signal_length = 8
        start_position = 39
        value_definition = {}

    class CenLockStsAndKeyIDTrigSrc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 153
        signal_description = "central lock trigger source"
        signal_length = 5
        start_position = 148
        value_definition = {'0x0': ' TrigSrc_IniVal', '0x1': ' TrigSrc_RKE_Outd', '0x2': ' TrigSrc_PE_APP', '0x3': ' TrigSrc_Approach_APP', '0x4': ' TrigSrc_PE_KeyFob', '0x5': ' TrigSrc_Approach_KeyFob', '0x6': ' TrigSrc_NFC', '0x7': ' TrigSrc_Telematic_Outd', '0x8': ' TrigSrc_Relock', '0x9': ' TrigSrc_OutdVoice', '0xA': ' TrigSrc_OutdLockCtrl', '0xB': ' TrigSrc_SpdLock', '0xC': ' TrigSrc_GearPUnlck', '0xD': ' TrigSrc_InsdSwtUnlck', '0xE': ' TrigSrc_InsdVoice', '0xF': ' TrigSrc_CrashUnlck', '0x10': ' TrigSrc_HMI', '0x11': ' TrigSrc_RKE_Insd', '0x12': ' TrigSrc_Telematic_Insd', '0x13': ' TrigSrc_ThermAwayUnlck', '0x14': ' TrigSrc_InsdLockCtrl'}

    class CenLockStsAndKeyIDKeyIDByte9:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 153
        signal_description = "key ID byte9"
        signal_length = 8
        start_position = 95
        value_definition = {}

    class CenLockStsAndKeyIDKeyIDByte6:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 153
        signal_description = "key ID byte6"
        signal_length = 8
        start_position = 71
        value_definition = {}

    class CenLockStsAndKeyIDKeyIDByte7:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 153
        signal_description = "key ID byte7"
        signal_length = 8
        start_position = 79
        value_definition = {}

    class CenLockStsAndKeyIDKeyIDByte4:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 153
        signal_description = "key ID byte4"
        signal_length = 8
        start_position = 55
        value_definition = {}

    class CenLockStsAndKeyIDKeyIDByte14:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 153
        signal_description = "key ID byte14"
        signal_length = 8
        start_position = 135
        value_definition = {}

    class CenLockStsAndKeyIDLockSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 153
        signal_description = "central lock status"
        signal_length = 2
        start_position = 151
        value_definition = {'0x0': ' LockSts_IniVal', '0x1': ' LockSts_CenLocked', '0x2': ' LockSts_CenUnLcked', '0x3': ' LockSts_OnlyTrUnlcked'}

    class CenLockStsAndKeyIDTrigSrcType:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 153
        signal_description = "central lock trigger source type"
        signal_length = 2
        start_position = 159
        value_definition = {'0x0': ' TrigSrcType_IniVal', '0x1': ' TrigSrcType_Outd', '0x2': ' TrigSrcType_Insd'}

    class CentralLockStsTrigSrc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 152
        signal_description = "central lock trigger source"
        signal_length = 5
        start_position = 164
        value_definition = {'0x0': ' TrigSrc_IniVal', '0x1': ' TrigSrc_RKE_Outd', '0x2': ' TrigSrc_PE_APP', '0x3': ' TrigSrc_Approach_APP', '0x4': ' TrigSrc_PE_KeyFob', '0x5': ' TrigSrc_Approach_KeyFob', '0x6': ' TrigSrc_NFC', '0x7': ' TrigSrc_Telematic_Outd', '0x8': ' TrigSrc_Relock', '0x9': ' TrigSrc_OutdVoice', '0xA': ' TrigSrc_OutdLockCtrl', '0xB': ' TrigSrc_SpdLock', '0xC': ' TrigSrc_GearPUnlck', '0xD': ' TrigSrc_InsdSwtUnlck', '0xE': ' TrigSrc_InsdVoice', '0xF': ' TrigSrc_CrashUnlck', '0x10': ' TrigSrc_HMI', '0x11': ' TrigSrc_RKE_Insd', '0x12': ' TrigSrc_Telematic_Insd', '0x13': ' TrigSrc_ThermAwayUnlck', '0x14': ' TrigSrc_InsdLockCtrl'}

    class CentralLockStsUpdateEvnt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 152
        signal_description = "central lock update event"
        signal_length = 1
        start_position = 165
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class CentralLockStsCenLockSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 152
        signal_description = "central lock status"
        signal_length = 2
        start_position = 175
        value_definition = {'0x0': ' LockSts_IniVal', '0x1': ' LockSts_CenLocked', '0x2': ' LockSts_CenUnLcked', '0x3': ' LockSts_OnlyTrUnlcked'}

    class CentralLockStsTrigSrcType:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 152
        signal_description = "central lock trigger source type"
        signal_length = 2
        start_position = 167
        value_definition = {'0x0': ' TrigSrcType_IniVal', '0x1': ' TrigSrcType_Outd', '0x2': ' TrigSrcType_Insd'}

    class LVBattChrgnReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 173
        signal_description = "Low voltage charging request"
        signal_length = 2
        start_position = 171
        value_definition = {'0x0': ' LVChrgnReq_Idle', '0x1': ' LVChrgnReq_Chrgn', '0x2': ' LVChrgnReq_NoReq', '0x3': ' LVChrgnReq_Resvd'}


class CCUMCUCDMulticastEthSignalIPdu03:
    base_type = "Unsigned"
    client_socket = "SocketMulticast"
    pdu_header_id = 0x20FF03
    pdu_length_bytes = 175
    receiver = ['CCUMCUAD', 'CCUSOCCD', 'LCUL', 'LCUR', 'CCUNAD']
    send_type = "Cyclic-100ms"
    sender = "CCUMCUCD"
    server_socket = "SocketCdMcuSoAdUDP"
    signal_group = {'LoadPwrActSts': ['LoadPwrActStsHCMLPwrActSts', 'LoadPwrActStsHCMLPwrActSts', 'LoadPwrActStsHCMLPwrActSts', 'LoadPwrActStsHCMLPwrActSts', 'LoadPwrActStsReserved4', 'LoadPwrActStsReserved4', 'LoadPwrActStsReserved4', 'LoadPwrActStsReserved4', 'LoadPwrActStsPOFPwrActSts', 'LoadPwrActStsPOFPwrActSts', 'LoadPwrActStsPOFPwrActSts', 'LoadPwrActStsPOFPwrActSts', 'LoadPwrActStsReserved16', 'LoadPwrActStsReserved16', 'LoadPwrActStsReserved16', 'LoadPwrActStsReserved16', 'LoadPwrActStsAGMPwrActSts', 'LoadPwrActStsAGMPwrActSts', 'LoadPwrActStsAGMPwrActSts', 'LoadPwrActStsAGMPwrActSts', 'LoadPwrActStsUWBPwrActSts', 'LoadPwrActStsUWBPwrActSts', 'LoadPwrActStsUWBPwrActSts', 'LoadPwrActStsUWBPwrActSts', 'LoadPwrActStsOPCRPwrActSts', 'LoadPwrActStsOPCRPwrActSts', 'LoadPwrActStsOPCRPwrActSts', 'LoadPwrActStsOPCRPwrActSts', 'LoadPwrActStsReserved10', 'LoadPwrActStsReserved10', 'LoadPwrActStsReserved10', 'LoadPwrActStsReserved10', 'LoadPwrActStsRSOV1PwrActSts', 'LoadPwrActStsRSOV1PwrActSts', 'LoadPwrActStsRSOV1PwrActSts', 'LoadPwrActStsRSOV1PwrActSts', 'LoadPwrActStsRSOV2PwrActSts', 'LoadPwrActStsRSOV2PwrActSts', 'LoadPwrActStsRSOV2PwrActSts', 'LoadPwrActStsRSOV2PwrActSts', 'LoadPwrActStsFLRPwrActSts', 'LoadPwrActStsFLRPwrActSts', 'LoadPwrActStsFLRPwrActSts', 'LoadPwrActStsFLRPwrActSts', 'LoadPwrActStsCDPwrActSts', 'LoadPwrActStsCDPwrActSts', 'LoadPwrActStsCDPwrActSts', 'LoadPwrActStsCDPwrActSts', 'LoadPwrActStsHVAHPwrActSts', 'LoadPwrActStsHVAHPwrActSts', 'LoadPwrActStsHVAHPwrActSts', 'LoadPwrActStsHVAHPwrActSts', 'LoadPwrActStsHUBRPwrActSts', 'LoadPwrActStsHUBRPwrActSts', 'LoadPwrActStsHUBRPwrActSts', 'LoadPwrActStsHUBRPwrActSts', 'LoadPwrActStsHVCMPwrActSts', 'LoadPwrActStsHVCMPwrActSts', 'LoadPwrActStsHVCMPwrActSts', 'LoadPwrActStsHVCMPwrActSts', 'LoadPwrActStsWERVPwrActSts', 'LoadPwrActStsWERVPwrActSts', 'LoadPwrActStsWERVPwrActSts', 'LoadPwrActStsWERVPwrActSts', 'LoadPwrActStsACCMPwrActSts', 'LoadPwrActStsACCMPwrActSts', 'LoadPwrActStsACCMPwrActSts', 'LoadPwrActStsACCMPwrActSts', 'LoadPwrActStsEDCPPwrActSts', 'LoadPwrActStsEDCPPwrActSts', 'LoadPwrActStsEDCPPwrActSts', 'LoadPwrActStsEDCPPwrActSts', 'LoadPwrActStsSWTRPwrActSts', 'LoadPwrActStsSWTRPwrActSts', 'LoadPwrActStsSWTRPwrActSts', 'LoadPwrActStsSWTRPwrActSts', 'LoadPwrActStsRLMMPwrActSts', 'LoadPwrActStsRLMMPwrActSts', 'LoadPwrActStsRLMMPwrActSts', 'LoadPwrActStsRLMMPwrActSts', 'LoadPwrActStsCRCMPwrActSts', 'LoadPwrActStsCRCMPwrActSts', 'LoadPwrActStsCRCMPwrActSts', 'LoadPwrActStsCRCMPwrActSts', 'LoadPwrActStsHBMRPwrActSts', 'LoadPwrActStsHBMRPwrActSts', 'LoadPwrActStsHBMRPwrActSts', 'LoadPwrActStsHBMRPwrActSts', 'LoadPwrActStsCERVPwrActSts', 'LoadPwrActStsCERVPwrActSts', 'LoadPwrActStsCERVPwrActSts', 'LoadPwrActStsCERVPwrActSts', 'LoadPwrActStsReserved1', 'LoadPwrActStsReserved1', 'LoadPwrActStsReserved1', 'LoadPwrActStsReserved1', 'LoadPwrActStsRRMMPwrActSts', 'LoadPwrActStsRRMMPwrActSts', 'LoadPwrActStsRRMMPwrActSts', 'LoadPwrActStsRRMMPwrActSts', 'LoadPwrActStsHCCPPwrActSts', 'LoadPwrActStsHCCPPwrActSts', 'LoadPwrActStsHCCPPwrActSts', 'LoadPwrActStsHCCPPwrActSts', 'LoadPwrActStsDMFLPwrActSts', 'LoadPwrActStsDMFLPwrActSts', 'LoadPwrActStsDMFLPwrActSts', 'LoadPwrActStsDMFLPwrActSts', 'LoadPwrActStsBEXVPwrActSts', 'LoadPwrActStsBEXVPwrActSts', 'LoadPwrActStsBEXVPwrActSts', 'LoadPwrActStsBEXVPwrActSts', 'LoadPwrActStsDRMRRPwrActSts', 'LoadPwrActStsDRMRRPwrActSts', 'LoadPwrActStsDRMRRPwrActSts', 'LoadPwrActStsDRMRRPwrActSts', 'LoadPwrActStsHCTVPwrActSts', 'LoadPwrActStsHCTVPwrActSts', 'LoadPwrActStsHCTVPwrActSts', 'LoadPwrActStsHCTVPwrActSts', 'LoadPwrActStsHCMRPwrActSts', 'LoadPwrActStsHCMRPwrActSts', 'LoadPwrActStsHCMRPwrActSts', 'LoadPwrActStsHCMRPwrActSts', 'LoadPwrActStsSWTLPwrActSts', 'LoadPwrActStsSWTLPwrActSts', 'LoadPwrActStsSWTLPwrActSts', 'LoadPwrActStsSWTLPwrActSts', 'LoadPwrActStsSRSPwrActSts', 'LoadPwrActStsSRSPwrActSts', 'LoadPwrActStsSRSPwrActSts', 'LoadPwrActStsSRSPwrActSts', 'LoadPwrActStsBNCMPwrActSts', 'LoadPwrActStsBNCMPwrActSts', 'LoadPwrActStsBNCMPwrActSts', 'LoadPwrActStsBNCMPwrActSts', 'LoadPwrActStsHODPwrActSts', 'LoadPwrActStsHODPwrActSts', 'LoadPwrActStsHODPwrActSts', 'LoadPwrActStsHODPwrActSts', 'LoadPwrActStsMMDPwrActSts', 'LoadPwrActStsMMDPwrActSts', 'LoadPwrActStsMMDPwrActSts', 'LoadPwrActStsMMDPwrActSts', 'LoadPwrActStsCCTVPwrActSts', 'LoadPwrActStsCCTVPwrActSts', 'LoadPwrActStsCCTVPwrActSts', 'LoadPwrActStsCCTVPwrActSts', 'LoadPwrActStsReserved13', 'LoadPwrActStsReserved13', 'LoadPwrActStsReserved13', 'LoadPwrActStsReserved13', 'LoadPwrActStsUSBR1PwrActSts', 'LoadPwrActStsUSBR1PwrActSts', 'LoadPwrActStsUSBR1PwrActSts', 'LoadPwrActStsUSBR1PwrActSts', 'LoadPwrActStsReserved15', 'LoadPwrActStsReserved15', 'LoadPwrActStsReserved15', 'LoadPwrActStsReserved15', 'LoadPwrActStsRMLPwrActSts', 'LoadPwrActStsRMLPwrActSts', 'LoadPwrActStsRMLPwrActSts', 'LoadPwrActStsRMLPwrActSts', 'LoadPwrActStsReserved8', 'LoadPwrActStsReserved8', 'LoadPwrActStsReserved8', 'LoadPwrActStsReserved8', 'LoadPwrActStsAWMPwrActSts', 'LoadPwrActStsAWMPwrActSts', 'LoadPwrActStsAWMPwrActSts', 'LoadPwrActStsAWMPwrActSts', 'LoadPwrActStsRCMLPwrActSts', 'LoadPwrActStsRCMLPwrActSts', 'LoadPwrActStsRCMLPwrActSts', 'LoadPwrActStsRCMLPwrActSts', 'LoadPwrActStsIEMPwrActSts', 'LoadPwrActStsIEMPwrActSts', 'LoadPwrActStsIEMPwrActSts', 'LoadPwrActStsIEMPwrActSts', 'LoadPwrActStsEGSMPwrActSts', 'LoadPwrActStsEGSMPwrActSts', 'LoadPwrActStsEGSMPwrActSts', 'LoadPwrActStsEGSMPwrActSts', 'LoadPwrActStsSODLPwrActSts', 'LoadPwrActStsSODLPwrActSts', 'LoadPwrActStsSODLPwrActSts', 'LoadPwrActStsSODLPwrActSts', 'LoadPwrActStsReserved7', 'LoadPwrActStsReserved7', 'LoadPwrActStsReserved7', 'LoadPwrActStsReserved7', 'LoadPwrActStsReserved2', 'LoadPwrActStsReserved2', 'LoadPwrActStsReserved2', 'LoadPwrActStsReserved2', 'LoadPwrActStsHUBFPwrActSts', 'LoadPwrActStsHUBFPwrActSts', 'LoadPwrActStsHUBFPwrActSts', 'LoadPwrActStsHUBFPwrActSts', 'LoadPwrActStsHVCHPwrActSts', 'LoadPwrActStsHVCHPwrActSts', 'LoadPwrActStsHVCHPwrActSts', 'LoadPwrActStsHVCHPwrActSts', 'LoadPwrActStsLPODPwrActSts', 'LoadPwrActStsLPODPwrActSts', 'LoadPwrActStsLPODPwrActSts', 'LoadPwrActStsLPODPwrActSts', 'LoadPwrActStsReserved3', 'LoadPwrActStsReserved3', 'LoadPwrActStsReserved3', 'LoadPwrActStsReserved3', 'LoadPwrActStsReserved11', 'LoadPwrActStsReserved11', 'LoadPwrActStsReserved11', 'LoadPwrActStsReserved11', 'LoadPwrActStsPPODPwrActSts', 'LoadPwrActStsPPODPwrActSts', 'LoadPwrActStsPPODPwrActSts', 'LoadPwrActStsPPODPwrActSts', 'LoadPwrActStsALMLPwrActSts', 'LoadPwrActStsALMLPwrActSts', 'LoadPwrActStsALMLPwrActSts', 'LoadPwrActStsALMLPwrActSts', 'LoadPwrActStsPORPwrActSts', 'LoadPwrActStsPORPwrActSts', 'LoadPwrActStsPORPwrActSts', 'LoadPwrActStsPORPwrActSts', 'LoadPwrActStsRCMRPwrActSts', 'LoadPwrActStsRCMRPwrActSts', 'LoadPwrActStsRCMRPwrActSts', 'LoadPwrActStsRCMRPwrActSts', 'LoadPwrActStsReserved12', 'LoadPwrActStsReserved12', 'LoadPwrActStsReserved12', 'LoadPwrActStsReserved12', 'LoadPwrActStsDRMRLPwrActSts', 'LoadPwrActStsDRMRLPwrActSts', 'LoadPwrActStsDRMRLPwrActSts', 'LoadPwrActStsDRMRLPwrActSts', 'LoadPwrActStsOPCFPwrActSts', 'LoadPwrActStsOPCFPwrActSts', 'LoadPwrActStsOPCFPwrActSts', 'LoadPwrActStsOPCFPwrActSts', 'LoadPwrActStsEPMPwrActSts', 'LoadPwrActStsEPMPwrActSts', 'LoadPwrActStsEPMPwrActSts', 'LoadPwrActStsEPMPwrActSts', 'LoadPwrActStsLCTVPwrActSts', 'LoadPwrActStsLCTVPwrActSts', 'LoadPwrActStsLCTVPwrActSts', 'LoadPwrActStsLCTVPwrActSts', 'LoadPwrActStsSCMFPwrActSts', 'LoadPwrActStsSCMFPwrActSts', 'LoadPwrActStsSCMFPwrActSts', 'LoadPwrActStsSCMFPwrActSts', 'LoadPwrActStsTERVPwrActSts', 'LoadPwrActStsTERVPwrActSts', 'LoadPwrActStsTERVPwrActSts', 'LoadPwrActStsTERVPwrActSts', 'LoadPwrActStsReserved14', 'LoadPwrActStsReserved14', 'LoadPwrActStsReserved14', 'LoadPwrActStsReserved14', 'LoadPwrActStsECTVPwrActSts', 'LoadPwrActStsECTVPwrActSts', 'LoadPwrActStsECTVPwrActSts', 'LoadPwrActStsECTVPwrActSts', 'LoadPwrActStsREXVPwrActSts', 'LoadPwrActStsREXVPwrActSts', 'LoadPwrActStsREXVPwrActSts', 'LoadPwrActStsREXVPwrActSts', 'LoadPwrActStsDRMFRPwrActSts', 'LoadPwrActStsDRMFRPwrActSts', 'LoadPwrActStsDRMFRPwrActSts', 'LoadPwrActStsDRMFRPwrActSts', 'LoadPwrActStsDCTVPwrActSts', 'LoadPwrActStsDCTVPwrActSts', 'LoadPwrActStsDCTVPwrActSts', 'LoadPwrActStsDCTVPwrActSts', 'LoadPwrActStsSCMRPwrActSts', 'LoadPwrActStsSCMRPwrActSts', 'LoadPwrActStsSCMRPwrActSts', 'LoadPwrActStsSCMRPwrActSts', 'LoadPwrActStsDRFPwrActSts', 'LoadPwrActStsDRFPwrActSts', 'LoadPwrActStsDRFPwrActSts', 'LoadPwrActStsDRFPwrActSts', 'LoadPwrActStsBCTVPwrActSts', 'LoadPwrActStsBCTVPwrActSts', 'LoadPwrActStsBCTVPwrActSts', 'LoadPwrActStsBCTVPwrActSts', 'LoadPwrActStsCSOVPwrActSts', 'LoadPwrActStsCSOVPwrActSts', 'LoadPwrActStsCSOVPwrActSts', 'LoadPwrActStsCSOVPwrActSts', 'LoadPwrActStsHBMFPwrActSts', 'LoadPwrActStsHBMFPwrActSts', 'LoadPwrActStsHBMFPwrActSts', 'LoadPwrActStsHBMFPwrActSts', 'LoadPwrActStsWPCPwrActSts', 'LoadPwrActStsWPCPwrActSts', 'LoadPwrActStsWPCPwrActSts', 'LoadPwrActStsWPCPwrActSts', 'LoadPwrActStsIRMMPwrActSts', 'LoadPwrActStsIRMMPwrActSts', 'LoadPwrActStsIRMMPwrActSts', 'LoadPwrActStsIRMMPwrActSts', 'LoadPwrActStsBoosterBlowerPwrActSts', 'LoadPwrActStsBoosterBlowerPwrActSts', 'LoadPwrActStsBoosterBlowerPwrActSts', 'LoadPwrActStsBoosterBlowerPwrActSts', 'LoadPwrActStsRLSMPwrActSts', 'LoadPwrActStsRLSMPwrActSts', 'LoadPwrActStsRLSMPwrActSts', 'LoadPwrActStsRLSMPwrActSts', 'LoadPwrActStsReserved5', 'LoadPwrActStsReserved5', 'LoadPwrActStsReserved5', 'LoadPwrActStsReserved5', 'LoadPwrActStsReserved6', 'LoadPwrActStsReserved6', 'LoadPwrActStsReserved6', 'LoadPwrActStsReserved6', 'LoadPwrActStsDPODPwrActSts', 'LoadPwrActStsDPODPwrActSts', 'LoadPwrActStsDPODPwrActSts', 'LoadPwrActStsDPODPwrActSts', 'LoadPwrActStsOHCPwrActSts', 'LoadPwrActStsOHCPwrActSts', 'LoadPwrActStsOHCPwrActSts', 'LoadPwrActStsOHCPwrActSts', 'LoadPwrActStsSODRPwrActSts', 'LoadPwrActStsSODRPwrActSts', 'LoadPwrActStsSODRPwrActSts', 'LoadPwrActStsSODRPwrActSts', 'LoadPwrActStsFEXVPwrActSts', 'LoadPwrActStsFEXVPwrActSts', 'LoadPwrActStsFEXVPwrActSts', 'LoadPwrActStsFEXVPwrActSts', 'LoadPwrActStsALMRPwrActSts', 'LoadPwrActStsALMRPwrActSts', 'LoadPwrActStsALMRPwrActSts', 'LoadPwrActStsALMRPwrActSts', 'LoadPwrActStsMGMPwrActSts', 'LoadPwrActStsMGMPwrActSts', 'LoadPwrActStsMGMPwrActSts', 'LoadPwrActStsMGMPwrActSts', 'LoadPwrActStsPMSIPwrActSts', 'LoadPwrActStsPMSIPwrActSts', 'LoadPwrActStsPMSIPwrActSts', 'LoadPwrActStsPMSIPwrActSts', 'LoadPwrActStsAFUPwrActSts', 'LoadPwrActStsAFUPwrActSts', 'LoadPwrActStsAFUPwrActSts', 'LoadPwrActStsAFUPwrActSts', 'LoadPwrActStsUSBR2PwrActSts', 'LoadPwrActStsUSBR2PwrActSts', 'LoadPwrActStsUSBR2PwrActSts', 'LoadPwrActStsUSBR2PwrActSts', 'LoadPwrActStsDICPwrActSts', 'LoadPwrActStsDICPwrActSts', 'LoadPwrActStsDICPwrActSts', 'LoadPwrActStsDICPwrActSts', 'LoadPwrActStsReserved9', 'LoadPwrActStsReserved9', 'LoadPwrActStsReserved9', 'LoadPwrActStsReserved9', 'LoadPwrActStsVCUPwrActSts', 'LoadPwrActStsVCUPwrActSts', 'LoadPwrActStsVCUPwrActSts', 'LoadPwrActStsVCUPwrActSts', 'LoadPwrActStsNKRPwrActSts', 'LoadPwrActStsNKRPwrActSts', 'LoadPwrActStsNKRPwrActSts', 'LoadPwrActStsNKRPwrActSts', 'LoadPwrActStsMMPPwrActSts', 'LoadPwrActStsMMPPwrActSts', 'LoadPwrActStsMMPPwrActSts', 'LoadPwrActStsMMPPwrActSts', 'LoadPwrActStsBCFVPwrActSts', 'LoadPwrActStsBCFVPwrActSts', 'LoadPwrActStsBCFVPwrActSts', 'LoadPwrActStsBCFVPwrActSts', 'LoadPwrActStsFSRRPwrActSts', 'LoadPwrActStsFSRRPwrActSts', 'LoadPwrActStsFSRRPwrActSts', 'LoadPwrActStsFSRRPwrActSts', 'LoadPwrActStsFCSIPwrActSts', 'LoadPwrActStsFCSIPwrActSts', 'LoadPwrActStsFCSIPwrActSts', 'LoadPwrActStsFCSIPwrActSts', 'LoadPwrActStsBCCPPwrActSts', 'LoadPwrActStsBCCPPwrActSts', 'LoadPwrActStsBCCPPwrActSts', 'LoadPwrActStsBCCPPwrActSts', 'LoadPwrActStsAGUPwrActSts', 'LoadPwrActStsAGUPwrActSts', 'LoadPwrActStsAGUPwrActSts', 'LoadPwrActStsAGUPwrActSts', 'LoadPwrActStsRPODPwrActSts', 'LoadPwrActStsRPODPwrActSts', 'LoadPwrActStsRPODPwrActSts', 'LoadPwrActStsRPODPwrActSts', 'LoadPwrActStsFSRLPwrActSts', 'LoadPwrActStsFSRLPwrActSts', 'LoadPwrActStsFSRLPwrActSts', 'LoadPwrActStsFSRLPwrActSts', 'LoadPwrActStsReserved17', 'LoadPwrActStsReserved17', 'LoadPwrActStsReserved17', 'LoadPwrActStsReserved17', 'LoadPwrActStsReserved18', 'LoadPwrActStsReserved18', 'LoadPwrActStsReserved18', 'LoadPwrActStsReserved18'], 'HVECmprCmdFromHPC': ['HVECmprCmdFromHPCCmprEna', 'HVECmprCmdFromHPCCmprEna', 'HVECmprCmdFromHPCCmprDuty', 'HVECmprCmdFromHPCCmprDuty'], 'CooltCircFlwDes': ['CooltCircFlwDesPWTCircFlwTar', 'CooltCircFlwDesHVBattCircFlwTar', 'CooltCircFlwDesHeatrCircFlwTar'], 'CooltCircFlwEstimd': ['CooltCircFlwEstimdHvBattCirc', 'CooltCircFlwEstimdHvBattCirc', 'CooltCircFlwEstimdHeatrCirc', 'CooltCircFlwEstimdHeatrCirc', 'CooltCircFlwEstimdPWTCirc', 'CooltCircFlwEstimdPWTCirc'], 'CooltCircPmpCmdFromHPC': ['CooltCircPmpCmdFromHPCHvBattPmp', 'CooltCircPmpCmdFromHPCHvBattPmp', 'CooltCircPmpCmdFromHPCPWTPmp', 'CooltCircPmpCmdFromHPCPWTPmp', 'CooltCircPmpCmdFromHPCHeatrPmp', 'CooltCircPmpCmdFromHPCHeatrPmp'], 'CooltCircTDes': ['CooltCircTDesHVBattCircTTar', 'CooltCircTDesHeatrCircTTar', 'CooltCircTDesPWTCircTTar'], 'CooltCircVlvCmdFromHPC': ['CooltCircVlvCmdFromHPCECTVCmd', 'CooltCircVlvCmdFromHPCECTVCmd', 'CooltCircVlvCmdFromHPCDCTVCmd', 'CooltCircVlvCmdFromHPCDCTVCmd', 'CooltCircVlvCmdFromHPCCooltSOV1Cmd', 'CooltCircVlvCmdFromHPCCooltSOV1Cmd', 'CooltCircVlvCmdFromHPCWCTVCmd', 'CooltCircVlvCmdFromHPCWCTVCmd', 'CooltCircVlvCmdFromHPCBCFVCmd', 'CooltCircVlvCmdFromHPCBCFVCmd', 'CooltCircVlvCmdFromHPCCCTVCmd', 'CooltCircVlvCmdFromHPCCCTVCmd', 'CooltCircVlvCmdFromHPCHCTVCmd', 'CooltCircVlvCmdFromHPCHCTVCmd', 'CooltCircVlvCmdFromHPCLCTVCmd', 'CooltCircVlvCmdFromHPCLCTVCmd', 'CooltCircVlvCmdFromHPCBCTVCmd', 'CooltCircVlvCmdFromHPCBCTVCmd'], 'CooltTSnsrT1Estimd': ['CooltTSnsrT1EstimdT', 'CooltTSnsrT1EstimdDataQly'], 'CooltTSnsrT2Estimd': ['CooltTSnsrT2EstimdDataQly', 'CooltTSnsrT2EstimdT'], 'CooltTSnsrT3Estimd': ['CooltTSnsrT3EstimdT', 'CooltTSnsrT3EstimdDataQly'], 'CooltTSnsrT4Estimd': ['CooltTSnsrT4EstimdDataQly', 'CooltTSnsrT4EstimdT'], 'FrntEndAirFlwCmd': ['FrntEndAirFlwCmdRefrigCirc', 'FrntEndAirFlwCmdCooltCirc'], 'HvAirHeatrCmdFromHPC': ['HvAirHeatrCmdFromHPCCtrlMod', 'HvAirHeatrCmdFromHPCCtrlMod', 'HvAirHeatrCmdFromHPCDutyTar', 'HvAirHeatrCmdFromHPCDutyTar', 'HvAirHeatrCmdFromHPCPwrTar', 'HvAirHeatrCmdFromHPCPwrTar', 'HvAirHeatrCmdFromHPCHeatrEna', 'HvAirHeatrCmdFromHPCHeatrEna'], 'HVBattOverHeatgStopReq': ['HVBattOverHeatgStopReqChks', 'HVBattOverHeatgStopReqChks', 'HVBattOverHeatgStopReqCntr', 'HVBattOverHeatgStopReqCntr', 'HVBattOverHeatgStopReqReqSt', 'HVBattOverHeatgStopReqReqSt'], 'HvCooltHeatrCmdFromHPC': ['HvCooltHeatrCmdFromHPCTarT', 'HvCooltHeatrCmdFromHPCTarT', 'HvCooltHeatrCmdFromHPCCtrlMod', 'HvCooltHeatrCmdFromHPCCtrlMod', 'HvCooltHeatrCmdFromHPCTarPwr', 'HvCooltHeatrCmdFromHPCTarPwr', 'HvCooltHeatrCmdFromHPCHeatrEna', 'HvCooltHeatrCmdFromHPCHeatrEna'], 'RefrigCircVlvCmdFromHPC': ['RefrigCircVlvCmdFromHPCRefrigSOV1Cmd', 'RefrigCircVlvCmdFromHPCRefrigSOV1Cmd', 'RefrigCircVlvCmdFromHPCRefrigSOV1Cmd', 'RefrigCircVlvCmdFromHPCBEXVCmd', 'RefrigCircVlvCmdFromHPCBEXVCmd', 'RefrigCircVlvCmdFromHPCBEXVCmd', 'RefrigCircVlvCmdFromHPCREXVCmd', 'RefrigCircVlvCmdFromHPCREXVCmd', 'RefrigCircVlvCmdFromHPCREXVCmd', 'RefrigCircVlvCmdFromHPCFEXVCmd', 'RefrigCircVlvCmdFromHPCFEXVCmd', 'RefrigCircVlvCmdFromHPCFEXVCmd', 'RefrigCircVlvCmdFromHPCRefrigSOV3Cmd', 'RefrigCircVlvCmdFromHPCRefrigSOV3Cmd', 'RefrigCircVlvCmdFromHPCRefrigSOV3Cmd', 'RefrigCircVlvCmdFromHPCCERVCmd', 'RefrigCircVlvCmdFromHPCCERVCmd', 'RefrigCircVlvCmdFromHPCCERVCmd', 'RefrigCircVlvCmdFromHPCRefrigSOV2Cmd', 'RefrigCircVlvCmdFromHPCRefrigSOV2Cmd', 'RefrigCircVlvCmdFromHPCRefrigSOV2Cmd', 'RefrigCircVlvCmdFromHPCTERVCmd', 'RefrigCircVlvCmdFromHPCTERVCmd', 'RefrigCircVlvCmdFromHPCTERVCmd', 'RefrigCircVlvCmdFromHPCWERVCmd', 'RefrigCircVlvCmdFromHPCWERVCmd', 'RefrigCircVlvCmdFromHPCWERVCmd'], 'RefrigPSnsr1PEstimd': ['RefrigPSnsr1PEstimdP', 'RefrigPSnsr1PEstimdP', 'RefrigPSnsr1PEstimdDataQly', 'RefrigPSnsr1PEstimdDataQly'], 'RefrigPTSnsr1PEstimd': ['RefrigPTSnsr1PEstimdP', 'RefrigPTSnsr1PEstimdP', 'RefrigPTSnsr1PEstimdDataQly', 'RefrigPTSnsr1PEstimdDataQly'], 'RefrigPTSnsr1TEstimd': ['RefrigPTSnsr1TEstimdDataQly', 'RefrigPTSnsr1TEstimdDataQly', 'RefrigPTSnsr1TEstimdT', 'RefrigPTSnsr1TEstimdT'], 'RefrigPTSnsr2PEstimd': ['RefrigPTSnsr2PEstimdDataQly', 'RefrigPTSnsr2PEstimdDataQly', 'RefrigPTSnsr2PEstimdP', 'RefrigPTSnsr2PEstimdP'], 'RefrigPTSnsr2TEstimd': ['RefrigPTSnsr2TEstimdDataQly', 'RefrigPTSnsr2TEstimdDataQly', 'RefrigPTSnsr2TEstimdT', 'RefrigPTSnsr2TEstimdT'], 'RefrigPTSnsr3PEstimd': ['RefrigPTSnsr3PEstimdP', 'RefrigPTSnsr3PEstimdP', 'RefrigPTSnsr3PEstimdDataQly', 'RefrigPTSnsr3PEstimdDataQly'], 'RefrigPTSnsr3TEstimd': ['RefrigPTSnsr3TEstimdT', 'RefrigPTSnsr3TEstimdT', 'RefrigPTSnsr3TEstimdDataQly', 'RefrigPTSnsr3TEstimdDataQly'], 'RefrigPTSnsr4PEstimd': ['RefrigPTSnsr4PEstimdP', 'RefrigPTSnsr4PEstimdP', 'RefrigPTSnsr4PEstimdDataQly', 'RefrigPTSnsr4PEstimdDataQly'], 'RefrigPTSnsr4TEstimd': ['RefrigPTSnsr4TEstimdDataQly', 'RefrigPTSnsr4TEstimdDataQly', 'RefrigPTSnsr4TEstimdT', 'RefrigPTSnsr4TEstimdT'], 'RefrigTSnsr1TEstimd': ['RefrigTSnsr1TEstimdDataQly', 'RefrigTSnsr1TEstimdDataQly', 'RefrigTSnsr1TEstimdT', 'RefrigTSnsr1TEstimdT'], 'RefrigTSnsr2TEstimd': ['RefrigTSnsr2TEstimdDataQly', 'RefrigTSnsr2TEstimdDataQly', 'RefrigTSnsr2TEstimdT', 'RefrigTSnsr2TEstimdT'], 'RefrigTSnsr3TEstimd': ['RefrigTSnsr3TEstimdDataQly', 'RefrigTSnsr3TEstimdDataQly', 'RefrigTSnsr3TEstimdT', 'RefrigTSnsr3TEstimdT'], 'RefrigTSnsr4TEstimd': ['RefrigTSnsr4TEstimdT', 'RefrigTSnsr4TEstimdT', 'RefrigTSnsr4TEstimdDataQly', 'RefrigTSnsr4TEstimdDataQly']}

    class LoadPwrActStsHCMLPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 509
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsReserved4:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 611
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsPOFPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 547
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsReserved16:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 635
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsAGMPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 435
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsUWBPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 593
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsOPCRPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 551
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsReserved10:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 631
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsRSOV1PwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 573
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsRSOV2PwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 571
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsFLRPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 489
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsCDPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 461
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsHVAHPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 513
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsHUBRPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 515
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsHVCMPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 525
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsWERVPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 605
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsACCMPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 439
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsEDCPPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 483
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsSWTRPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 589
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsRLMMPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 567
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsCRCMPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 457
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsHBMRPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 497
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsCERVPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 459
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsReserved1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 601
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsRRMMPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 575
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsHCCPPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 511
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsDMFLPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 465
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsBEXVPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 451
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsDRMRRPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 487
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsHCTVPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 505
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsHCMRPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 507
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsSWTLPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 591
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsSRSPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 577
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsBNCMPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 449
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsHODPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 519
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsMMDPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 529
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsCCTVPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 463
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsReserved13:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 625
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsUSBR1PwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 597
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsReserved15:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 637
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsRMLPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 563
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsReserved8:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 619
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsAWMPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 443
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsRCMLPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 557
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsIEMPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 523
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsEGSMPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 481
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsSODLPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 581
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsReserved7:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 621
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsReserved2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 615
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsHUBFPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 517
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsHVCHPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 527
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsLPODPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 533
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsReserved3:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 613
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsReserved11:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 629
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsPPODPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 559
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsALMLPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 447
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsPORPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 545
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsRCMRPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 555
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsReserved12:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 627
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsDRMRLPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 473
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsOPCFPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 537
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsEPMPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 495
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsLCTVPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 535
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsSCMFPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 569
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsTERVPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 587
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsReserved14:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 639
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsECTVPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 485
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsREXVPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 553
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsDRMFRPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 475
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsDCTVPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 469
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsSCMRPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 583
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsDRFPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 477
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsBCTVPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 453
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsCSOVPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 471
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsHBMFPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 499
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsWPCPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 603
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsIRMMPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 521
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsBoosterBlowerPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 633
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsRLSMPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 565
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsReserved5:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 609
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsReserved6:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 623
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsDPODPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 479
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsOHCPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 539
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsSODRPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 579
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsFEXVPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 491
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsALMRPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 445
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsMGMPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 531
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsPMSIPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 549
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsAFUPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 437
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsUSBR2PwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 595
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsDICPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 467
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsReserved9:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 617
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsVCUPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 607
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsNKRPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 541
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsMMPPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 543
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsBCFVPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 455
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsFSRRPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 501
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsFCSIPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 493
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsBCCPPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 441
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsAGUPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 433
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsRPODPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 561
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsFSRLPwrActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 503
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsReserved17:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 585
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class LoadPwrActStsReserved18:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1117
        signal_description = "Load Power Actual Status"
        signal_length = 2
        start_position = 599
        value_definition = {'0x0': ' LVPowerSts_PowerOff', '0x1': ' LVPowerSts_PowerOn', '0x2': ' LVPowerSts_PowerGoingOff', '0x3': ' LVPowerSts_PowerFault'}

    class TimeSrcSyncSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1272
        signal_description = "the current time source of vehicle time, default invalid"
        signal_length = 3
        start_position = 1231
        value_definition = {'0x0': ' TimeSrcSyncType_Invalid', '0x1': ' TimeSrcSyncType_DefaultTime', '0x2': ' TimeSrcSyncType_RTCTime', '0x3': ' TimeSrcSyncType_NTPTime', '0x4': ' TimeSrcSyncType_LPGNSSTime', '0x5': ' TimeSrcSyncType_HPGNSSTime'}

    class BucSwtStsAtDrvr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 9
        signal_description = "Buckle switch status at driver"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' BucSwtSts_Invalid', '0x1': ' BucSwtSts_Error', '0x2': ' BucSwtSts_Unlocked', '0x3': ' BucSwtSts_Locked'}

    class BucSwtStsAtPass:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 8
        signal_description = "Buckle switch status at passenger"
        signal_length = 2
        start_position = 5
        value_definition = {'0x0': ' BucSwtSts_Invalid', '0x1': ' BucSwtSts_Error', '0x2': ' BucSwtSts_Unlocked', '0x3': ' BucSwtSts_Locked'}

    class BucSwtStsAtRowSecLe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 82
        signal_description = "Buckle switch status at second left"
        signal_length = 2
        start_position = 3
        value_definition = {'0x0': ' BucSwtSts_Invalid', '0x1': ' BucSwtSts_Error', '0x2': ' BucSwtSts_Unlocked', '0x3': ' BucSwtSts_Locked'}

    class BucSwtStsAtRowSecMid:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 81
        signal_description = "Buckle switch status at second middle"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': ' BucSwtSts_Invalid', '0x1': ' BucSwtSts_Error', '0x2': ' BucSwtSts_Unlocked', '0x3': ' BucSwtSts_Locked'}

    class BucSwtStsAtRowSecRi:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 80
        signal_description = "Buckle switch status at second right"
        signal_length = 2
        start_position = 15
        value_definition = {'0x0': ' BucSwtSts_Invalid', '0x1': ' BucSwtSts_Error', '0x2': ' BucSwtSts_Unlocked', '0x3': ' BucSwtSts_Locked'}

    class BucSwtStsAtRowThrdLe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 90
        signal_description = "Buckle switch status at third left"
        signal_length = 2
        start_position = 13
        value_definition = {'0x0': ' BucSwtSts_Invalid', '0x1': ' BucSwtSts_Error', '0x2': ' BucSwtSts_Unlocked', '0x3': ' BucSwtSts_Locked'}

    class BucSwtStsAtRowThrdRi:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 89
        signal_description = "Buckle switch status at third right"
        signal_length = 2
        start_position = 11
        value_definition = {'0x0': ' BucSwtSts_Invalid', '0x1': ' BucSwtSts_Error', '0x2': ' BucSwtSts_Unlocked', '0x3': ' BucSwtSts_Locked'}

    class HVECmprCmdFromHPCCmprEna:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 88
        signal_description = "Compressor eanble command"
        signal_length = 1
        start_position = 16
        value_definition = {'0x0': ' EnableDisable2_Disabled', '0x1': ' EnableDisable2_Enabled'}

    class HVECmprCmdFromHPCCmprDuty:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 88
        signal_description = "Compressor duty command"
        signal_length = 7
        start_position = 23
        value_definition = {}

    class HVECmprPwrAllwd:
        comments = ""
        factor = 10.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1287
        signal_description = "E-Compressor power allwd"
        signal_length = 13
        start_position = 1228
        value_definition = {}

    class CooltCircFlwDesPWTCircFlwTar:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 253
        signal_description = "PWT circuit target flowrate"
        signal_length = 9
        start_position = 45
        value_definition = {}

    class CooltCircFlwDesHVBattCircFlwTar:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 253
        signal_description = "Hvbatt circuit target flowrate"
        signal_length = 9
        start_position = 38
        value_definition = {}

    class CooltCircFlwDesHeatrCircFlwTar:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 253
        signal_description = "Heatr circuit target flowrate"
        signal_length = 9
        start_position = 31
        value_definition = {}

    class CooltCircFlwEstimdHvBattCirc:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 252
        signal_description = "Hvbatt coolant flow estimd"
        signal_length = 9
        start_position = 70
        value_definition = {}

    class CooltCircFlwEstimdHeatrCirc:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 252
        signal_description = "Heatr coolant flow estimd"
        signal_length = 9
        start_position = 63
        value_definition = {}

    class CooltCircFlwEstimdPWTCirc:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 252
        signal_description = "pwt coolant flow estimd"
        signal_length = 9
        start_position = 77
        value_definition = {}

    class CooltCircModDes:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 251
        signal_description = "Desire cooling circuit mode"
        signal_length = 5
        start_position = 52
        value_definition = {'0x0': ' ThermMod_Mode0', '0x1': ' ThermMod_Mode1', '0x2': ' ThermMod_Mode2', '0x3': ' ThermMod_Mode3', '0x4': ' ThermMod_Mode4', '0x5': ' ThermMod_Mode5', '0x6': ' ThermMod_Mode6', '0x7': ' ThermMod_Mode7', '0x8': ' ThermMod_Mode8', '0x9': ' ThermMod_Mode9', '0xA': ' ThermMod_Mode10', '0xB': ' ThermMod_Mode11', '0xC': ' ThermMod_Mode12', '0xD': ' ThermMod_Mode13', '0xE': ' ThermMod_Mode14', '0xF': ' ThermMod_Mode15', '0x10': ' ThermMod_Mode16', '0x11': ' ThermMod_Mode17', '0x12': ' ThermMod_Mode18', '0x13': ' ThermMod_Mode19', '0x14': ' ThermMod_Mode20', '0x15': ' ThermMod_Mode21', '0x16': ' ThermMod_Mode22', '0x17': ' ThermMod_Mode23', '0x18': ' ThermMod_Mode24', '0x19': ' ThermMod_Mode25', '0x1A': ' ThermMod_Mode26', '0x1B': ' ThermMod_Mode27', '0x1C': ' ThermMod_Mode28', '0x1D': ' ThermMod_Mode29', '0x1E': ' ThermMod_Mode30', '0x1F': ' ThermMod_Mode31'}

    class CooltCircModSwtSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 250
        signal_description = "Mode switch status"
        signal_length = 2
        start_position = 84
        value_definition = {'0x0': ' StartFinish1_Start', '0x1': ' StartFinish1_Finish', '0x2': ' StartFinish1_Reserved1', '0x3': ' StartFinish1_Reserved2'}

    class CooltCircPmpCmdFromHPCHvBattPmp:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 399
        signal_description = "Hvbatt pump cmd"
        signal_length = 10
        start_position = 109
        value_definition = {}

    class CooltCircPmpCmdFromHPCPWTPmp:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 399
        signal_description = "PWT pump cmd"
        signal_length = 10
        start_position = 115
        value_definition = {}

    class CooltCircPmpCmdFromHPCHeatrPmp:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 399
        signal_description = "Heatr pump cmd"
        signal_length = 10
        start_position = 103
        value_definition = {}

    class CooltCircTDesHVBattCircTTar:
        comments = ""
        factor = 0.1
        initial_value = 600
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -60
        sig_ub = 152
        signal_description = "Hvbatt circuit target temperature "
        signal_length = 11
        start_position = 142
        value_definition = {}

    class CooltCircTDesHeatrCircTTar:
        comments = ""
        factor = 0.1
        initial_value = 600
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -60
        sig_ub = 152
        signal_description = "Heatr circuit target temperature "
        signal_length = 11
        start_position = 121
        value_definition = {}

    class CooltCircTDesPWTCircTTar:
        comments = ""
        factor = 0.1
        initial_value = 600
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -60
        sig_ub = 152
        signal_description = "PWT circuit target temperature "
        signal_length = 11
        start_position = 147
        value_definition = {}

    class CooltCircVlvCmdFromHPCECTVCmd:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 398
        signal_description = "ECTV position Cmd"
        signal_length = 10
        start_position = 173
        value_definition = {}

    class CooltCircVlvCmdFromHPCDCTVCmd:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 398
        signal_description = "DCTV position Cmd"
        signal_length = 10
        start_position = 225
        value_definition = {}

    class CooltCircVlvCmdFromHPCCooltSOV1Cmd:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 398
        signal_description = "Coolt SOV position Cmd"
        signal_length = 10
        start_position = 219
        value_definition = {}

    class CooltCircVlvCmdFromHPCWCTVCmd:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 398
        signal_description = "WCTV position Cmd"
        signal_length = 10
        start_position = 179
        value_definition = {}

    class CooltCircVlvCmdFromHPCBCFVCmd:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 398
        signal_description = "BCFV position Cmd"
        signal_length = 10
        start_position = 185
        value_definition = {}

    class CooltCircVlvCmdFromHPCCCTVCmd:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 398
        signal_description = "CCTV position Cmd"
        signal_length = 10
        start_position = 167
        value_definition = {}

    class CooltCircVlvCmdFromHPCHCTVCmd:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 398
        signal_description = "HCTV position Cmd"
        signal_length = 10
        start_position = 247
        value_definition = {}

    class CooltCircVlvCmdFromHPCLCTVCmd:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 398
        signal_description = "LCTV position Cmd"
        signal_length = 10
        start_position = 213
        value_definition = {}

    class CooltCircVlvCmdFromHPCBCTVCmd:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 398
        signal_description = "BCTV position Cmd"
        signal_length = 10
        start_position = 207
        value_definition = {}

    class CooltCricModAct:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 426
        signal_description = "Coolant Circult Actual Mode"
        signal_length = 5
        start_position = 95
        value_definition = {'0x0': ' ThermMod_Mode0', '0x1': ' ThermMod_Mode1', '0x2': ' ThermMod_Mode2', '0x3': ' ThermMod_Mode3', '0x4': ' ThermMod_Mode4', '0x5': ' ThermMod_Mode5', '0x6': ' ThermMod_Mode6', '0x7': ' ThermMod_Mode7', '0x8': ' ThermMod_Mode8', '0x9': ' ThermMod_Mode9', '0xA': ' ThermMod_Mode10', '0xB': ' ThermMod_Mode11', '0xC': ' ThermMod_Mode12', '0xD': ' ThermMod_Mode13', '0xE': ' ThermMod_Mode14', '0xF': ' ThermMod_Mode15', '0x10': ' ThermMod_Mode16', '0x11': ' ThermMod_Mode17', '0x12': ' ThermMod_Mode18', '0x13': ' ThermMod_Mode19', '0x14': ' ThermMod_Mode20', '0x15': ' ThermMod_Mode21', '0x16': ' ThermMod_Mode22', '0x17': ' ThermMod_Mode23', '0x18': ' ThermMod_Mode24', '0x19': ' ThermMod_Mode25', '0x1A': ' ThermMod_Mode26', '0x1B': ' ThermMod_Mode27', '0x1C': ' ThermMod_Mode28', '0x1D': ' ThermMod_Mode29', '0x1E': ' ThermMod_Mode30', '0x1F': ' ThermMod_Mode31'}

    class CooltTSnsrT1EstimdT:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = 425
        signal_description = "Sensor value"
        signal_length = 13
        start_position = 249
        value_definition = {}

    class CooltTSnsrT1EstimdDataQly:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 425
        signal_description = "Sensor data quality"
        signal_length = 2
        start_position = 268
        value_definition = {'0x0': ' SnsrQly_SnsrNotOk', '0x1': ' SnsrQly_SnsrOk'}

    class CooltTSnsrT2EstimdDataQly:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 424
        signal_description = "Sensor data quality"
        signal_length = 2
        start_position = 266
        value_definition = {'0x0': ' SnsrQly_SnsrNotOk', '0x1': ' SnsrQly_SnsrOk'}

    class CooltTSnsrT2EstimdT:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = 424
        signal_description = "Sensor value"
        signal_length = 13
        start_position = 264
        value_definition = {}

    class CooltTSnsrT3EstimdT:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = 641
        signal_description = "Sensor value"
        signal_length = 13
        start_position = 283
        value_definition = {}

    class CooltTSnsrT3EstimdDataQly:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 641
        signal_description = "Sensor data quality"
        signal_length = 2
        start_position = 302
        value_definition = {'0x0': ' SnsrQly_SnsrNotOk', '0x1': ' SnsrQly_SnsrOk'}

    class CooltTSnsrT4EstimdDataQly:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 640
        signal_description = "Sensor data quality"
        signal_length = 2
        start_position = 300
        value_definition = {'0x0': ' SnsrQly_SnsrNotOk', '0x1': ' SnsrQly_SnsrOk'}

    class CooltTSnsrT4EstimdT:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = 640
        signal_description = "Sensor value"
        signal_length = 13
        start_position = 298
        value_definition = {}

    class FrntEndAirFlwCmdRefrigCirc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1118
        signal_description = "CRFM air flow requewt from RefrigCirc"
        signal_length = 14
        start_position = 317
        value_definition = {}

    class FrntEndAirFlwCmdCooltCirc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1118
        signal_description = "CRFM air flow requewt from CooltCirc"
        signal_length = 14
        start_position = 335
        value_definition = {}

    class HvAirHeatrCmdFromHPCCtrlMod:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 366
        signal_description = "HVAH control mode"
        signal_length = 2
        start_position = 337
        value_definition = {'0x0': ' PTCCtrlMod_Default', '0x1': ' PTCCtrlMod_Duty', '0x2': ' PTCCtrlMod_Pwr', '0x3': ' PTCCtrlMod_Reserved'}

    class HvAirHeatrCmdFromHPCDutyTar:
        comments = ""
        factor = 0.5
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 366
        signal_description = "HVAH target duty"
        signal_length = 8
        start_position = 359
        value_definition = {}

    class HvAirHeatrCmdFromHPCPwrTar:
        comments = ""
        factor = 20.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 366
        signal_description = "HVAH target power"
        signal_length = 8
        start_position = 351
        value_definition = {}

    class HvAirHeatrCmdFromHPCHeatrEna:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 366
        signal_description = "air heater enable command"
        signal_length = 1
        start_position = 367
        value_definition = {'0x0': ' EnableDisable2_Disabled', '0x1': ' EnableDisable2_Enabled'}

    class HVAirHeatrPwrAllwd:
        comments = ""
        factor = 10.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 365
        signal_description = "HV air heatr power allowed"
        signal_length = 13
        start_position = 364
        value_definition = {}

    class HVBattOverHeatgStopReqChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 385
        signal_description = "Checksum"
        signal_length = 8
        start_position = 383
        value_definition = {}

    class HVBattOverHeatgStopReqCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 385
        signal_description = "Counter"
        signal_length = 4
        start_position = 391
        value_definition = {}

    class HVBattOverHeatgStopReqReqSt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 385
        signal_description = "Require state"
        signal_length = 2
        start_position = 387
        value_definition = {'0x0': ' ReqSts2_Default', '0x1': ' ReqSts2_NotReqd', '0x2': ' ReqSts2_Reqd', '0x3': ' ReqSts2_Reserved'}

    class HvCooltHeatrCmdFromHPCTarT:
        comments = ""
        factor = 1.0
        initial_value = 40
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -40
        sig_ub = 397
        signal_description = "HVCH temperature target"
        signal_length = 8
        start_position = 415
        value_definition = {}

    class HvCooltHeatrCmdFromHPCCtrlMod:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 397
        signal_description = "HVCH control mode"
        signal_length = 2
        start_position = 396
        value_definition = {'0x0': ' HVCHCtrlMod_TCtrl', '0x1': ' HVCHCtrlMod_PwrCtrl', '0x2': ' HVCHCtrlMod_Reserve'}

    class HvCooltHeatrCmdFromHPCTarPwr:
        comments = ""
        factor = 20.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 397
        signal_description = "HVCH power target"
        signal_length = 10
        start_position = 393
        value_definition = {}

    class HvCooltHeatrCmdFromHPCHeatrEna:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 397
        signal_description = "Coolant heater command"
        signal_length = 1
        start_position = 394
        value_definition = {'0x0': ' EnableDisable2_Disabled', '0x1': ' EnableDisable2_Enabled'}

    class HVCooltHeatrPwrAllwd:
        comments = ""
        factor = 10.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 384
        signal_description = "HV coolant heater power allowd"
        signal_length = 13
        start_position = 423
        value_definition = {}

    class LVBattChrgnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1116
        signal_description = "Low voltage battery charging Status"
        signal_length = 3
        start_position = 660
        value_definition = {'0x0': ' ChrgSts_Idle', '0x1': ' ChrgSts_Handshake', '0x2': ' ChrgSts_Charging', '0x3': ' ChrgSts_Abort', '0x4': ' ChrgSts_Reserved1', '0x5': ' ChrgSts_Reserved2', '0x6': ' ChrgSts_Reserved3', '0x7': ' ChrgSts_Reserved4'}

    class LVChrgnFailCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1115
        signal_description = "Low voltage Charging fail counter"
        signal_length = 2
        start_position = 647
        value_definition = {}

    class LVChrgnFailWarn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1114
        signal_description = "Low voltage Charging fail warn"
        signal_length = 2
        start_position = 645
        value_definition = {'0x0': ' ChrgnFailWarn_Idle', '0x1': ' ChrgnFailWarn_Warning', '0x2': ' ChrgnFailWarn_NoWarning', '0x3': ' ChrgnFailWarn_Resvd'}

    class LVSysEgyLvl:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1113
        signal_description = "Low voltage start level"
        signal_length = 2
        start_position = 643
        value_definition = {'0x0': ' EgyLvl_Norm', '0x1': ' EgyLvl_Level1', '0x2': ' EgyLvl_Level2', '0x3': ' EgyLvl_Reserved'}

    class PrimBattComFltSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1112
        signal_description = "primary battery system communication fault flag"
        signal_length = 1
        start_position = 655
        value_definition = {'0x0': ' Flg1_Rst', '0x1': ' Flg1_Set'}

    class PrimBattComFltWarn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1286
        signal_description = "Primary Battery Communication failure"
        signal_length = 2
        start_position = 657
        value_definition = {'0x0': ' LVFaultSts_Idle', '0x1': ' LVFaultSts_Fault', '0x2': ' LVFaultSts_NoFault', '0x3': ' LVFaultSts_Reserved'}

    class PrimBattFltHiUWarn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1285
        signal_description = "Primary Battery over voltage"
        signal_length = 2
        start_position = 654
        value_definition = {'0x0': ' LVFaultSts_Idle', '0x1': ' LVFaultSts_Fault', '0x2': ' LVFaultSts_NoFault', '0x3': ' LVFaultSts_Reserved'}

    class PrimBattFltLoSOCWarn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1284
        signal_description = "Primary Battery SOC Low"
        signal_length = 2
        start_position = 652
        value_definition = {'0x0': ' LVFaultSts_Idle', '0x1': ' LVFaultSts_Fault', '0x2': ' LVFaultSts_NoFault', '0x3': ' LVFaultSts_Reserved'}

    class PrimBattFltLoUWarn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1247
        signal_description = "Primary Battery under voltage"
        signal_length = 2
        start_position = 650
        value_definition = {'0x0': ' LVFaultSts_Idle', '0x1': ' LVFaultSts_Fault', '0x2': ' LVFaultSts_NoFault', '0x3': ' LVFaultSts_Reserved'}

    class PrimBattFltTWarn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1246
        signal_description = "Primary Battery over temperature"
        signal_length = 2
        start_position = 648
        value_definition = {'0x0': ' LVFaultSts_Idle', '0x1': ' LVFaultSts_Fault', '0x2': ' LVFaultSts_NoFault', '0x3': ' LVFaultSts_Reserved'}

    class PrimBattHwFailrWarn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1245
        signal_description = "Primary Battery Hardware malfunction"
        signal_length = 2
        start_position = 662
        value_definition = {'0x0': ' LVFaultSts_Idle', '0x1': ' LVFaultSts_Fault', '0x2': ' LVFaultSts_NoFault', '0x3': ' LVFaultSts_Reserved'}

    class PrimBattIFild:
        comments = ""
        factor = 0.015625
        initial_value = 32768
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -512
        sig_ub = 1244
        signal_description = "Primary battery current filtering value"
        signal_length = 16
        start_position = 671
        value_definition = {}

    class PrimBattShoCircWarn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1243
        signal_description = "Primary Battery Short circuit fault"
        signal_length = 2
        start_position = 687
        value_definition = {'0x0': ' LVFaultSts_Idle', '0x1': ' LVFaultSts_Fault', '0x2': ' LVFaultSts_NoFault', '0x3': ' LVFaultSts_Reserved'}

    class PrimBattTFild:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = 1242
        signal_description = "Primary battery temperature filtering value"
        signal_length = 13
        start_position = 685
        value_definition = {}

    class PrimBattThermWarn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1241
        signal_description = "Primary Battery Thermal runaway"
        signal_length = 2
        start_position = 688
        value_definition = {'0x0': ' LVFaultSts_Idle', '0x1': ' LVFaultSts_Fault', '0x2': ' LVFaultSts_NoFault', '0x3': ' LVFaultSts_Reserved'}

    class PrimBattUFild:
        comments = ""
        factor = 0.02
        initial_value = 1023
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1240
        signal_description = "Primary battery voltage filtering value"
        signal_length = 10
        start_position = 702
        value_definition = {'0x3FF': 'BattU2_BMSVolWakeUpThd'}

    class PtInin:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1255
        signal_description = "Ptlnin"
        signal_length = 1
        start_position = 708
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class RdntBattComFltSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 706
        signal_description = "Redundant battery system communication fault flag"
        signal_length = 1
        start_position = 707
        value_definition = {'0x0': ' Flg1_Rst', '0x1': ' Flg1_Set'}

    class RdntBattComFltWarn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 705
        signal_description = "Redundant Battery Communication failure"
        signal_length = 2
        start_position = 725
        value_definition = {'0x0': ' LVFaultSts_Idle', '0x1': ' LVFaultSts_Fault', '0x2': ' LVFaultSts_NoFault', '0x3': ' LVFaultSts_Reserved'}

    class RdntBattFltHiUWarn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 704
        signal_description = "Redundant Battery over voltage"
        signal_length = 2
        start_position = 719
        value_definition = {'0x0': ' LVFaultSts_Idle', '0x1': ' LVFaultSts_Fault', '0x2': ' LVFaultSts_NoFault', '0x3': ' LVFaultSts_Reserved'}

    class RdntBattFltLoSOCWarn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 723
        signal_description = "Redundant Battery SOC Low"
        signal_length = 2
        start_position = 717
        value_definition = {'0x0': ' LVFaultSts_Idle', '0x1': ' LVFaultSts_Fault', '0x2': ' LVFaultSts_NoFault', '0x3': ' LVFaultSts_Reserved'}

    class RdntBattFltLoUWarn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 722
        signal_description = "Redundant Battery under voltage"
        signal_length = 2
        start_position = 715
        value_definition = {'0x0': ' LVFaultSts_Idle', '0x1': ' LVFaultSts_Fault', '0x2': ' LVFaultSts_NoFault', '0x3': ' LVFaultSts_Reserved'}

    class RdntBattFltTWarn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 721
        signal_description = "Redundant Battery over temperature"
        signal_length = 2
        start_position = 713
        value_definition = {'0x0': ' LVFaultSts_Idle', '0x1': ' LVFaultSts_Fault', '0x2': ' LVFaultSts_NoFault', '0x3': ' LVFaultSts_Reserved'}

    class RdntBattHwFailrWarn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 720
        signal_description = "Redundant Battery Hardware malfunction"
        signal_length = 2
        start_position = 727
        value_definition = {'0x0': ' LVFaultSts_Idle', '0x1': ' LVFaultSts_Fault', '0x2': ' LVFaultSts_NoFault', '0x3': ' LVFaultSts_Reserved'}

    class RdntBattIFild:
        comments = ""
        factor = 0.015625
        initial_value = 32768
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -512
        sig_ub = 1254
        signal_description = "Redundant battery current filtering value"
        signal_length = 16
        start_position = 735
        value_definition = {}

    class RdntBattShoCircWarn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1253
        signal_description = "Redundant Battery Short circuit fault"
        signal_length = 2
        start_position = 751
        value_definition = {'0x0': ' LVFaultSts_Idle', '0x1': ' LVFaultSts_Fault', '0x2': ' LVFaultSts_NoFault', '0x3': ' LVFaultSts_Reserved'}

    class RdntBattTFild:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = 1252
        signal_description = "Redundant battery temperature filtering value"
        signal_length = 13
        start_position = 749
        value_definition = {}

    class RdntBattThermWarn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1251
        signal_description = "Redundant Battery Thermal runaway"
        signal_length = 2
        start_position = 752
        value_definition = {'0x0': ' LVFaultSts_Idle', '0x1': ' LVFaultSts_Fault', '0x2': ' LVFaultSts_NoFault', '0x3': ' LVFaultSts_Reserved'}

    class RdntBattUFild:
        comments = ""
        factor = 0.02
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1250
        signal_description = "Redundant battery voltage filtering value"
        signal_length = 10
        start_position = 766
        value_definition = {'0x3FF': 'BattU2_BMSVolWakeUpThd'}

    class RefrigCircVlvCmdFromHPCRefrigSOV1Cmd:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1249
        signal_description = "Refrigerant SOV position Cmd"
        signal_length = 10
        start_position = 824
        value_definition = {}

    class RefrigCircVlvCmdFromHPCBEXVCmd:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1249
        signal_description = "BEXV position Cmd"
        signal_length = 10
        start_position = 852
        value_definition = {}

    class RefrigCircVlvCmdFromHPCREXVCmd:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1249
        signal_description = "REXV position Cmd"
        signal_length = 10
        start_position = 806
        value_definition = {}

    class RefrigCircVlvCmdFromHPCFEXVCmd:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1249
        signal_description = "FEXV position Cmd"
        signal_length = 10
        start_position = 778
        value_definition = {}

    class RefrigCircVlvCmdFromHPCRefrigSOV3Cmd:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1249
        signal_description = "Refrigerant SOV position Cmd"
        signal_length = 10
        start_position = 846
        value_definition = {}

    class RefrigCircVlvCmdFromHPCCERVCmd:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1249
        signal_description = "CERV position Cmd"
        signal_length = 10
        start_position = 812
        value_definition = {}

    class RefrigCircVlvCmdFromHPCRefrigSOV2Cmd:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1249
        signal_description = "Refrigerant SOV position Cmd"
        signal_length = 10
        start_position = 784
        value_definition = {}

    class RefrigCircVlvCmdFromHPCTERVCmd:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1249
        signal_description = "TERV position Cmd"
        signal_length = 10
        start_position = 772
        value_definition = {}

    class RefrigCircVlvCmdFromHPCWERVCmd:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1249
        signal_description = "WERV position Cmd"
        signal_length = 10
        start_position = 818
        value_definition = {}

    class RefrigPSnsr1PEstimdP:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1248
        signal_description = "Sensor value"
        signal_length = 12
        start_position = 858
        value_definition = {}

    class RefrigPSnsr1PEstimdDataQly:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1248
        signal_description = "Sensor data quality"
        signal_length = 2
        start_position = 878
        value_definition = {'0x0': ' SnsrQly_SnsrNotOk', '0x1': ' SnsrQly_SnsrOk'}

    class RefrigPTSnsr1PEstimdP:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1263
        signal_description = "Sensor value"
        signal_length = 12
        start_position = 876
        value_definition = {}

    class RefrigPTSnsr1PEstimdDataQly:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1263
        signal_description = "Sensor data quality"
        signal_length = 2
        start_position = 880
        value_definition = {'0x0': ' SnsrQly_SnsrNotOk', '0x1': ' SnsrQly_SnsrOk'}

    class RefrigPTSnsr1TEstimdDataQly:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1262
        signal_description = "Sensor data quality"
        signal_length = 2
        start_position = 894
        value_definition = {'0x0': ' SnsrQly_SnsrNotOk', '0x1': ' SnsrQly_SnsrOk'}

    class RefrigPTSnsr1TEstimdT:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = 1262
        signal_description = "Sensor value"
        signal_length = 13
        start_position = 892
        value_definition = {}

    class RefrigPTSnsr2PEstimdDataQly:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1261
        signal_description = "Sensor data quality"
        signal_length = 2
        start_position = 911
        value_definition = {'0x0': ' SnsrQly_SnsrNotOk', '0x1': ' SnsrQly_SnsrOk'}

    class RefrigPTSnsr2PEstimdP:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1261
        signal_description = "Sensor value"
        signal_length = 12
        start_position = 909
        value_definition = {}

    class RefrigPTSnsr2TEstimdDataQly:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1260
        signal_description = "Sensor data quality"
        signal_length = 2
        start_position = 913
        value_definition = {'0x0': ' SnsrQly_SnsrNotOk', '0x1': ' SnsrQly_SnsrOk'}

    class RefrigPTSnsr2TEstimdT:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = 1260
        signal_description = "Sensor value"
        signal_length = 13
        start_position = 927
        value_definition = {}

    class RefrigPTSnsr3PEstimdP:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1259
        signal_description = "Sensor value"
        signal_length = 12
        start_position = 930
        value_definition = {}

    class RefrigPTSnsr3PEstimdDataQly:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1259
        signal_description = "Sensor data quality"
        signal_length = 2
        start_position = 950
        value_definition = {'0x0': ' SnsrQly_SnsrNotOk', '0x1': ' SnsrQly_SnsrOk'}

    class RefrigPTSnsr3TEstimdT:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = 1258
        signal_description = "Sensor value"
        signal_length = 13
        start_position = 948
        value_definition = {}

    class RefrigPTSnsr3TEstimdDataQly:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1258
        signal_description = "Sensor data quality"
        signal_length = 2
        start_position = 967
        value_definition = {'0x0': ' SnsrQly_SnsrNotOk', '0x1': ' SnsrQly_SnsrOk'}

    class RefrigPTSnsr4PEstimdP:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1257
        signal_description = "Sensor value"
        signal_length = 12
        start_position = 965
        value_definition = {}

    class RefrigPTSnsr4PEstimdDataQly:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1257
        signal_description = "Sensor data quality"
        signal_length = 2
        start_position = 969
        value_definition = {'0x0': ' SnsrQly_SnsrNotOk', '0x1': ' SnsrQly_SnsrOk'}

    class RefrigPTSnsr4TEstimdDataQly:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1256
        signal_description = "Sensor data quality"
        signal_length = 2
        start_position = 983
        value_definition = {'0x0': ' SnsrQly_SnsrNotOk', '0x1': ' SnsrQly_SnsrOk'}

    class RefrigPTSnsr4TEstimdT:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = 1256
        signal_description = "Sensor value"
        signal_length = 13
        start_position = 981
        value_definition = {}

    class RefrigTSnsr1TEstimdDataQly:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1279
        signal_description = "Sensor data quality"
        signal_length = 2
        start_position = 984
        value_definition = {'0x0': ' SnsrQly_SnsrNotOk', '0x1': ' SnsrQly_SnsrOk'}

    class RefrigTSnsr1TEstimdT:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = 1279
        signal_description = "Sensor value"
        signal_length = 13
        start_position = 998
        value_definition = {}

    class RefrigTSnsr2TEstimdDataQly:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1271
        signal_description = "Sensor data quality"
        signal_length = 2
        start_position = 1001
        value_definition = {'0x0': ' SnsrQly_SnsrNotOk', '0x1': ' SnsrQly_SnsrOk'}

    class RefrigTSnsr2TEstimdT:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = 1271
        signal_description = "Sensor value"
        signal_length = 13
        start_position = 1015
        value_definition = {}

    class RefrigTSnsr3TEstimdDataQly:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1270
        signal_description = "Sensor data quality"
        signal_length = 2
        start_position = 1018
        value_definition = {'0x0': ' SnsrQly_SnsrNotOk', '0x1': ' SnsrQly_SnsrOk'}

    class RefrigTSnsr3TEstimdT:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = 1270
        signal_description = "Sensor value"
        signal_length = 13
        start_position = 1016
        value_definition = {}

    class RefrigTSnsr4TEstimdT:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = 1269
        signal_description = "Sensor value"
        signal_length = 13
        start_position = 1035
        value_definition = {}

    class RefrigTSnsr4TEstimdDataQly:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1269
        signal_description = "Sensor data quality"
        signal_length = 2
        start_position = 1054
        value_definition = {'0x0': ' SnsrQly_SnsrNotOk', '0x1': ' SnsrQly_SnsrOk'}

    class ThermFctReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1268
        signal_description = "Thermal management system VMM hold request"
        signal_length = 1
        start_position = 1052
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class ThermMngtHVEgyReq:
        comments = ""
        factor = 50.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -1
        sig_ub = 1267
        signal_description = "thermal management energy request"
        signal_length = 10
        start_position = 1051
        value_definition = {}

    class ThermMngtHVPwrCritDes:
        comments = ""
        factor = 10.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1266
        signal_description = "thermal management power critical desire"
        signal_length = 13
        start_position = 1057
        value_definition = {}

    class ThermMngtHVPwrNormDes:
        comments = ""
        factor = 10.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1265
        signal_description = "thermal management power normal desire"
        signal_length = 13
        start_position = 1076
        value_definition = {}

    class ThermMngtLVPwrCns:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1264
        signal_description = "thermal management LV power desire"
        signal_length = 12
        start_position = 1095
        value_definition = {}

    class ThermMngtLVPwrDes:
        comments = ""
        factor = 10.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -1
        sig_ub = 1278
        signal_description = "thermal management Low Voltage Power request "
        signal_length = 13
        start_position = 1099
        value_definition = {}

    class ThermMngtSysSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1277
        signal_description = "Thermal Management System Status"
        signal_length = 32
        start_position = 1127
        value_definition = {}

    class ThermSysCmptErrInd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1276
        signal_description = "thermal system compressor Error indication"
        signal_length = 32
        start_position = 1159
        value_definition = {}

    class ThermSysProtnInd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1275
        signal_description = "thermal system protection indication"
        signal_length = 32
        start_position = 1191
        value_definition = {}

    class ThermSysRecFlapCtrlReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1274
        signal_description = "Recric flap control request from thermal"
        signal_length = 3
        start_position = 1223
        value_definition = {'0x0': ' FlapCtrlReq_Normal', '0x1': ' FlapCtrlReq_CoolgPwrOvrLoad', '0x2': ' FlapCtrlReq_HeatgPwrOvrLoad'}

    class ThermSysWarnInd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1273
        signal_description = "thermal system compressor protection indication"
        signal_length = 32
        start_position = 1295
        value_definition = {}

    class CallSysWarnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1283
        signal_description = "Call system warn status"
        signal_length = 2
        start_position = 1220
        value_definition = {'0x0': ' CallSysWarnSts_Unkown', '0x1': ' CallSysWarnSts_Normal', '0x2': ' CallSysWarnSts_MinorFailure', '0x3': ' CallSysWarnSts_MajorFailure'}


class CCUMCUCDMulticastEthSignalIPdu01:
    base_type = "Unsigned"
    client_socket = "SocketMulticast"
    pdu_header_id = 0x20FF01
    pdu_length_bytes = 16
    receiver = ['LCUL', 'CCUSOCCD', 'LCUR']
    send_type = "Cyclic-20ms"
    sender = "CCUMCUCD"
    server_socket = "SocketCdMcuSoAdUDP"
    signal_group = {'BrkLiReqSec': ['BrkLiReqSecChks', 'BrkLiReqSecBrkLiReq', 'BrkLiReqSecCntr'], 'BrkPedlStk': ['BrkPedlStkTar', 'BrkPedlStkChks', 'BrkPedlStkStQf', 'BrkPedlStkQf', 'BrkPedlStkAct', 'BrkPedlStkSt', 'BrkPedlStkCntr']}

    class BrkLiReqSecChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 57
        signal_description = "crc"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class BrkLiReqSecBrkLiReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 57
        signal_description = "Brake light request"
        signal_length = 1
        start_position = 11
        value_definition = {'0x0': ' ReqSts1_NotReqd', '0x1': ' ReqSts1_Reqd'}

    class BrkLiReqSecCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 57
        signal_description = "counter"
        signal_length = 4
        start_position = 15
        value_definition = {}

    class BrkOilLvl:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 56
        signal_description = "brake fule level"
        signal_length = 2
        start_position = 10
        value_definition = {'0x0': ' FldLvl_Hi', '0x1': ' FldLvl_Low', '0x2': ' FldLvl_Reserved1', '0x3': ' FldLvl_Reserved2'}

    class BrkPedlCrv:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 87
        signal_description = "current brake pedal curve"
        signal_length = 3
        start_position = 23
        value_definition = {'0x0': ' BrkCalParas_Nromal', '0x1': ' BrkCalParas_Comfort', '0x2': ' BrkCalParas_Sport', '0x3': ' BrkCalParas_Reserved1', '0x4': ' BrkCalParas_Reserved2', '0x5': ' BrkCalParas_Reserved3'}

    class BrkPedlCrvAvl:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 86
        signal_description = "brake pedal curve adjustable or not"
        signal_length = 1
        start_position = 8
        value_definition = {'0x0': ' AvlSts2_NotAvl', '0x1': ' AvlSts2_Avl'}

    class BrkPedlStkTar:
        comments = ""
        factor = 0.01
        initial_value = 500
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -5
        sig_ub = 85
        signal_description = "Target value for the output rod"
        signal_length = 13
        start_position = 20
        value_definition = {}

    class BrkPedlStkChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 85
        signal_description = "crc"
        signal_length = 8
        start_position = 39
        value_definition = {}

    class BrkPedlStkStQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 85
        signal_description = "Brake pedal applied information quality factor"
        signal_length = 2
        start_position = 47
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class BrkPedlStkQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 85
        signal_description = "Travel sensor quality factor"
        signal_length = 2
        start_position = 45
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class BrkPedlStkAct:
        comments = ""
        factor = 0.01
        initial_value = 500
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -5
        sig_ub = 85
        signal_description = "Actual value for the output rod"
        signal_length = 13
        start_position = 55
        value_definition = {}

    class BrkPedlStkSt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 85
        signal_description = "Brake pedal applied information"
        signal_length = 1
        start_position = 58
        value_definition = {'0x0': ' PsdNotPsd1_NotPsd', '0x1': ' PsdNotPsd1_Psd'}

    class BrkPedlStkCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 85
        signal_description = "counter"
        signal_length = 4
        start_position = 43
        value_definition = {}

    class HVBattLimnIndcnInfo:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 84
        signal_description = "Indication signal from HV battery that tells a DTC is set"
        signal_length = 16
        start_position = 71
        value_definition = {}


class CCUMCUCDMulticastEthSignalIPdu04:
    base_type = "Unsigned"
    client_socket = "SocketMulticast"
    pdu_header_id = 0x20FF04
    pdu_length_bytes = 16
    receiver = ['CCUSOCCD', 'LCUL', 'LCUR']
    send_type = "Cyclic-10ms"
    sender = "CCUMCUCD"
    server_socket = "SocketCdMcuSoAdUDP"
    signal_group = {'CrashInfo': ['CrashInfoImpctDvy', 'CrashInfoImpctDvy', 'CrashInfoCrashRollovr', 'CrashInfoCrashRollovr', 'CrashInfoCrashFrnt', 'CrashInfoCrashFrnt', 'CrashInfoCrashRe', 'CrashInfoCrashRe', 'CrashInfoCrashOffroadRT', 'CrashInfoCrashOffroadRT', 'CrashInfoCrashOffroadD', 'CrashInfoCrashOffroadD', 'CrashInfoCrashPed', 'CrashInfoCrashPed', 'CrashInfoCrashSideLe', 'CrashInfoCrashSideLe', 'CrashInfoCrashOffroadRTsevere', 'CrashInfoCrashOffroadRTsevere', 'CrashInfoVehOri', 'CrashInfoVehOri', 'CrashInfoImpctDvx', 'CrashInfoImpctDvx', 'CrashInfoCrashOffroadA', 'CrashInfoCrashOffroadA', 'CrashInfoCrashState', 'CrashInfoCrashState', 'CrashInfoImpctRollAg', 'CrashInfoImpctRollAg', 'CrashInfoCrashSideRi', 'CrashInfoCrashSideRi'], 'CrashSts': ['CrashStsCntr', 'CrashStsCntr', 'CrashStsCntr', 'CrashStsChks', 'CrashStsChks', 'CrashStsChks', 'CrashSts2', 'CrashSts2', 'CrashSts2'], 'VMMGlbSig': ['VMMGlbSigUsgModSts', 'VMMGlbSigLoBattModSts', 'VMMGlbSigCntr', 'VMMGlbSigChks', 'VMMGlbSigCarModSts', 'VMMGlbSigInactvSubSts1', 'VMMGlbSigCnvincSubSts1', 'VMMGlbSigDrvgSubSts1'], 'GearLvrIndcnReal': ['GearLvrIndcnRealGearLvrIndcn', 'GearLvrIndcnRealGearLvrIndcn', 'GearLvrIndcnRealGearLvrIndcn', 'GearLvrIndcnRealCntr', 'GearLvrIndcnRealCntr', 'GearLvrIndcnRealCntr', 'GearLvrIndcnRealChks', 'GearLvrIndcnRealChks', 'GearLvrIndcnRealChks']}

    class CrashInfoImpctDvy:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 32
        signal_description = "Crash information, change in velocity in y-direction"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class CrashInfoCrashRollovr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 32
        signal_description = "Crash information, if crash is roll-over."
        signal_length = 1
        start_position = 35
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class CrashInfoCrashFrnt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 32
        signal_description = "Crash information, if crash is frontal"
        signal_length = 1
        start_position = 26
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class CrashInfoCrashRe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 32
        signal_description = "Crash information, if crash is rear"
        signal_length = 1
        start_position = 36
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class CrashInfoCrashOffroadRT:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 32
        signal_description = "Incident information, if driving off the road and into rough terrain has been detected"
        signal_length = 1
        start_position = 39
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class CrashInfoCrashOffroadD:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 32
        signal_description = "Incident information, if driving into a ditch has been detected."
        signal_length = 1
        start_position = 24
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class CrashInfoCrashPed:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 32
        signal_description = "Incident information, if a pedestrain protection triggering has been made."
        signal_length = 1
        start_position = 37
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class CrashInfoCrashSideLe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 32
        signal_description = "Crash information, if crash is left side"
        signal_length = 1
        start_position = 34
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class CrashInfoCrashOffroadRTsevere:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 32
        signal_description = "Incident information, if driving off the road and into severe rough terrain has been detected"
        signal_length = 1
        start_position = 38
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class CrashInfoVehOri:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 32
        signal_description = "Crash information, Vehicle orientation once crash subsides"
        signal_length = 3
        start_position = 31
        value_definition = {'0x0': ' Orntn_Invalid', '0x1': ' Orntn_OnWheels', '0x2': ' Orntn_LeftSide', '0x3': ' Orntn_RightSide', '0x4': ' Orntn_OnRoof', '0x5': ' Orntn_Indeterminate', '0x6': ' Orntn_Resd1', '0x7': ' Orntn_Resd2'}

    class CrashInfoImpctDvx:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 32
        signal_description = "Crash information, change in velocity in x-direction"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class CrashInfoCrashOffroadA:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 32
        signal_description = "Incident information, if driving off the road and becoming airbourne has been detected."
        signal_length = 1
        start_position = 25
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class CrashInfoCrashState:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 32
        signal_description = "Crash information, State of the crash"
        signal_length = 2
        start_position = 28
        value_definition = {'0x0': ' CrashProc_NoCrash', '0x1': ' CrashProc_CrashImminent', '0x2': ' CrashProc_CrashInProgress', '0x3': ' CrashProc_CrashEnding'}

    class CrashInfoImpctRollAg:
        comments = ""
        factor = 15.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 32
        signal_description = "Crash information, cumulative roll angle"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class CrashInfoCrashSideRi:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 32
        signal_description = "Crash information, if crash is right side"
        signal_length = 1
        start_position = 33
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class CrashStsCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 50
        signal_description = "rolling counter"
        signal_length = 4
        start_position = 55
        value_definition = {}

    class CrashStsChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 50
        signal_description = "checksum"
        signal_length = 8
        start_position = 47
        value_definition = {}

    class CrashSts2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 50
        signal_description = "crash status"
        signal_length = 1
        start_position = 51
        value_definition = {'0x0': ' CrashSts2_NoCrash', '0x1': ' CrashSts2_Crash'}

    class VMMGlbSigUsgModSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 49
        signal_description = "to be modified"
        signal_length = 4
        start_position = 103
        value_definition = {'0x0': ' UsgModSts1_UsgModAbdnd', '0x1': ' UsgModSts1_UsgModInActv', '0x2': ' UsgModSts1_UsgModCnvinc', '0xD': ' UsgModSts1_UsgModDrvg'}

    class VMMGlbSigLoBattModSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 49
        signal_description = "to be modified"
        signal_length = 1
        start_position = 99
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class VMMGlbSigCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 49
        signal_description = "to be modified"
        signal_length = 4
        start_position = 67
        value_definition = {}

    class VMMGlbSigChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 49
        signal_description = "to be modified"
        signal_length = 8
        start_position = 63
        value_definition = {}

    class VMMGlbSigCarModSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 49
        signal_description = "to be modified"
        signal_length = 4
        start_position = 71
        value_definition = {'0x0': ' CarModStsType_CarModNorm', '0x1': ' CarModStsType_CarModTrnsp', '0x2': ' CarModStsType_CarModFcy', '0x3': ' CarModStsType_CarModExhib', '0x8': ' CarModStsType_CarModCrash'}

    class VMMGlbSigInactvSubSts1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 49
        signal_description = ""
        signal_length = 8
        start_position = 95
        value_definition = {'0x0': ' InactvSubSts_Invalid', '0x1': ' InactvSubSts_Awake', '0x2': ' InactvSubSts_UserPresent'}

    class VMMGlbSigCnvincSubSts1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 49
        signal_description = ""
        signal_length = 8
        start_position = 79
        value_definition = {'0x0': ' CnvincSubSts_Invalid', '0x1': ' CnvincSubSts_EnterExit', '0x2': ' CnvincSubSts_AllDoorClosed'}

    class VMMGlbSigDrvgSubSts1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 49
        signal_description = ""
        signal_length = 8
        start_position = 87
        value_definition = {'0x0': ' DrvgSubSts_Invalid', '0x1': ' DrvgSubSts_Manual', '0x2': ' DrvgSubSts_Automatic', '0x3': ' DrvgSubSts_NoTorque'}

    class GearLvrIndcnRealGearLvrIndcn:
        comments = ""
        factor = 1.0
        initial_value = 7
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 112
        signal_description = "Real gear level"
        signal_length = 3
        start_position = 115
        value_definition = {'0x0': ' GearLvrIndcn_Default', '0x1': ' GearLvrIndcn_P', '0x2': ' GearLvrIndcn_R', '0x3': ' GearLvrIndcn_N', '0x4': ' GearLvrIndcn_D', '0x5': ' GearLvrIndcn_Reserved1', '0x6': ' GearLvrIndcn_Reserved2', '0x7': ' GearLvrIndcn_Undefd'}

    class GearLvrIndcnRealCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 112
        signal_description = "Cntr"
        signal_length = 4
        start_position = 119
        value_definition = {}

    class GearLvrIndcnRealChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 112
        signal_description = "Chks"
        signal_length = 8
        start_position = 111
        value_definition = {}

    class GearLvrIndcnDes:
        comments = ""
        factor = 1.0
        initial_value = 7
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 48
        signal_description = "Target gear information: After the user requests a gear shift, the target gear information jumps to the requested gear for EPB release and other functions."
        signal_length = 3
        start_position = 98
        value_definition = {'0x0': ' GearLvrIndcn_Default', '0x1': ' GearLvrIndcn_P', '0x2': ' GearLvrIndcn_R', '0x3': ' GearLvrIndcn_N', '0x4': ' GearLvrIndcn_D', '0x5': ' GearLvrIndcn_Reserved1', '0x6': ' GearLvrIndcn_Reserved2', '0x7': ' GearLvrIndcn_Undefd'}
