

class CCUMCUCDToLCUREthSignalIPdu01:
    base_type = "Unsigned"
    client_socket = "SocketLcuRSoAdUDP"
    pdu_header_id = 0x206001
    pdu_length_bytes = 8
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUMCUCD"
    server_socket = "SocketCdMcuSoAdUDP"
    signal_group = {'FRPwrSideDoorPosnSet': ['FRPwrSideDoorPosnSetPosnCtrlSrc', 'FRPwrSideDoorPosnSetCntr', 'FRPwrSideDoorPosnSetChks', 'FRPwrSideDoorPosnSetPosnCtrl'], 'RRPwrSideDoorPosnSet': ['RRPwrSideDoorPosnSetPosnCtrlSrc', 'RRPwrSideDoorPosnSetChks', 'RRPwrSideDoorPosnSetPosnCtrl', 'RRPwrSideDoorPosnSetCntr']}

    class FRPwrSideDoorPosnSetPosnCtrlSrc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 17
        signal_description = "Set power side Door position trigger source"
        signal_length = 2
        start_position = 19
        value_definition = {'0x0': ' CtrlTrigsrc_NoCtrlReq', '0x1': ' CtrlTrigsrc_OutdCtrl', '0x2': ' CtrlTrigsrc_InsdCtrl'}

    class FRPwrSideDoorPosnSetCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 17
        signal_description = "counter"
        signal_length = 4
        start_position = 15
        value_definition = {}

    class FRPwrSideDoorPosnSetChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 17
        signal_description = "checksum"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class FRPwrSideDoorPosnSetPosnCtrl:
        comments = ""
        factor = 1.0
        initial_value = 101
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 17
        signal_description = "Set power side Door position"
        signal_length = 8
        start_position = 11
        value_definition = {}

    class RRPwrSideDoorPosnSetPosnCtrlSrc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 41
        signal_description = "Set power side Door position trigger source"
        signal_length = 2
        start_position = 43
        value_definition = {'0x0': ' CtrlTrigsrc_NoCtrlReq', '0x1': ' CtrlTrigsrc_OutdCtrl', '0x2': ' CtrlTrigsrc_InsdCtrl'}

    class RRPwrSideDoorPosnSetChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 41
        signal_description = "checksum"
        signal_length = 8
        start_position = 31
        value_definition = {}

    class RRPwrSideDoorPosnSetPosnCtrl:
        comments = ""
        factor = 1.0
        initial_value = 101
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 41
        signal_description = "Set power side Door position"
        signal_length = 8
        start_position = 35
        value_definition = {}

    class RRPwrSideDoorPosnSetCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 41
        signal_description = "counter"
        signal_length = 4
        start_position = 39
        value_definition = {}


class CCUMCUCDToLCUREthSignalIPdu02:
    base_type = "Unsigned"
    client_socket = "SocketLcuRSoAdUDP"
    pdu_header_id = 0x206002
    pdu_length_bytes = 4
    receiver = ['LCUR']
    send_type = "Cyclic-100ms"
    sender = "CCUMCUCD"
    server_socket = "SocketCdMcuSoAdUDP"
    signal_group = {}

    class GrillShttrCmdFromHPC:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 0
        signal_description = "GrillShttrPosnReqFromHPC"
        signal_length = 7
        start_position = 7
        value_definition = {}

    class CoolgFanCmdFromHPC:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 21
        signal_description = "CoolgFanCmdFromHPC"
        signal_length = 10
        start_position = 15
        value_definition = {}


class LCURToCCUMCUCDEthSignalIPdu04:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuSoAdUDP"
    pdu_header_id = 0x602004
    pdu_length_bytes = 4
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-50ms"
    sender = "LCUR"
    server_socket = "SocketLcuRSoAdUDP"
    signal_group = {'FRPwrDoorMotPrm': ['FRPwrDoorMotPrmStopEvnt', 'FRPwrDoorMotPrmPwrDoorStsFb'], 'RRPwrDoorMotPrm': ['RRPwrDoorMotPrmStopEvnt', 'RRPwrDoorMotPrmPwrDoorStsFb']}

    class FRPwrDoorMotPrmStopEvnt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 20
        signal_description = "stop reason of motor "
        signal_length = 4
        start_position = 7
        value_definition = {'0x0': ' StopEvnt_NONE', '0x1': ' StopEvnt_BRAKE', '0x2': ' StopEvnt_KEY', '0x3': ' StopEvnt_VEHSPEED', '0x4': ' StopEvnt_RADAR', '0x5': ' StopEvnt_SLOWDOWN', '0x6': ' StopEvnt_ITINERARYL', '0x7': ' StopEvnt_TIMEOut', '0x8': ' StopEvnt_LATCH', '0x9': ' StopEvnt_OCP', '0xA': ' StopEvnt_ANTIPINCH', '0xB': ' StopEvnt_NOPLAYING', '0xC': ' StopEvnt_HALL', '0xD': ' StopEvnt_NORMAL', '0xE': ' StopEvnt_HAND', '0xF': ' StopEvnt_ERROR'}

    class FRPwrDoorMotPrmPwrDoorStsFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 20
        signal_description = "Power side door motor status"
        signal_length = 4
        start_position = 3
        value_definition = {'0x0': ' PwrDoorStsFb_DoorStUndef', '0x1': ' PwrDoorStsFb_DoorStWait', '0x2': ' PwrDoorStsFb_DoorStOpen', '0x3': ' PwrDoorStsFb_DoorStClose', '0x4': ' PwrDoorStsFb_DoorStRollBack', '0x5': ' PwrDoorStsFb_DoorSecondOpen', '0x6': ' PwrDoorStsFb_DoorTipToRun'}

    class HoodMotActvSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 19
        signal_description = "Hood Motor work status "
        signal_length = 3
        start_position = 15
        value_definition = {'0x0': ' MotSts_Inactive', '0x1': ' MotSts_Active', '0x2': ' MotSts_ResetActive'}

    class RRPwrDoorMotPrmStopEvnt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 18
        signal_description = "stop reason of motor "
        signal_length = 4
        start_position = 12
        value_definition = {'0x0': ' StopEvnt_NONE', '0x1': ' StopEvnt_BRAKE', '0x2': ' StopEvnt_KEY', '0x3': ' StopEvnt_VEHSPEED', '0x4': ' StopEvnt_RADAR', '0x5': ' StopEvnt_SLOWDOWN', '0x6': ' StopEvnt_ITINERARYL', '0x7': ' StopEvnt_TIMEOut', '0x8': ' StopEvnt_LATCH', '0x9': ' StopEvnt_OCP', '0xA': ' StopEvnt_ANTIPINCH', '0xB': ' StopEvnt_NOPLAYING', '0xC': ' StopEvnt_HALL', '0xD': ' StopEvnt_NORMAL', '0xE': ' StopEvnt_HAND', '0xF': ' StopEvnt_ERROR'}

    class RRPwrDoorMotPrmPwrDoorStsFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 18
        signal_description = "Power side door motor status"
        signal_length = 4
        start_position = 8
        value_definition = {'0x0': ' PwrDoorStsFb_DoorStUndef', '0x1': ' PwrDoorStsFb_DoorStWait', '0x2': ' PwrDoorStsFb_DoorStOpen', '0x3': ' PwrDoorStsFb_DoorStClose', '0x4': ' PwrDoorStsFb_DoorStRollBack', '0x5': ' PwrDoorStsFb_DoorSecondOpen', '0x6': ' PwrDoorStsFb_DoorTipToRun'}


class LCURToCCUMCUCDEthSignalIPdu03:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuSoAdUDP"
    pdu_header_id = 0x602003
    pdu_length_bytes = 32
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "LCUR"
    server_socket = "SocketLcuRSoAdUDP"
    signal_group = {'FrntEndCmptCalStsFromRi': ['FrntEndCmptCalStsFromRiCoolgFanCalSts', 'FrntEndCmptCalStsFromRiGrillShttrCalSts']}

    class CoolgFanPwmFb:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 13
        signal_description = "Cooling Fan PWM Feedback"
        signal_length = 10
        start_position = 7
        value_definition = {}

    class CooltTSnsr1TRaw:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 12
        signal_description = "Sensor raw data"
        signal_length = 16
        start_position = 23
        value_definition = {}

    class CooltTSnsr2TRaw:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 11
        signal_description = "Sensor raw data"
        signal_length = 16
        start_position = 39
        value_definition = {}

    class CooltTSnsr3TRaw:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 10
        signal_description = "Sensor raw data"
        signal_length = 16
        start_position = 55
        value_definition = {}

    class CooltTSnsr4TRaw:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 9
        signal_description = "Sensor raw data"
        signal_length = 16
        start_position = 71
        value_definition = {}

    class RdntBattFltTSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 8
        signal_description = "Redundant battery Over T failure status"
        signal_length = 2
        start_position = 87
        value_definition = {'0x0': ' LVFaultSts_Idle', '0x1': ' LVFaultSts_Fault', '0x2': ' LVFaultSts_NoFault', '0x3': ' LVFaultSts_Reserved'}

    class RdntBattThermSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 83
        signal_description = "Redundant battery thermal runaway status"
        signal_length = 2
        start_position = 85
        value_definition = {'0x0': ' LVFaultSts_Idle', '0x1': ' LVFaultSts_Fault', '0x2': ' LVFaultSts_NoFault', '0x3': ' LVFaultSts_Reserved'}

    class RefrigPSnsr1PRaw:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 82
        signal_description = "Sensor raw data"
        signal_length = 16
        start_position = 95
        value_definition = {}

    class RefrigPTSnsr3PRaw:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 81
        signal_description = "Sensor raw data"
        signal_length = 16
        start_position = 111
        value_definition = {}

    class RefrigPTSnsr3TRaw:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 80
        signal_description = "Sensor raw data"
        signal_length = 16
        start_position = 127
        value_definition = {}

    class RefrigPTSnsr4PRaw:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 191
        signal_description = "Sensor raw data"
        signal_length = 16
        start_position = 143
        value_definition = {}

    class RefrigPTSnsr4TRaw:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 190
        signal_description = "Sensor raw data"
        signal_length = 16
        start_position = 159
        value_definition = {}

    class RefrigTSnsr1TRaw:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 189
        signal_description = "Sensor raw data"
        signal_length = 16
        start_position = 175
        value_definition = {}

    class FrntEndCmptCalStsFromRiCoolgFanCalSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 188
        signal_description = "CoolgFanCalSts"
        signal_length = 2
        start_position = 199
        value_definition = {'0x0': ' ExvCalibSts_NotInitialized', '0x1': ' ExvCalibSts_InitializationInProcess', '0x2': ' ExvCalibSts_Initialized', '0x3': ' ExvCalibSts_Reserved'}

    class FrntEndCmptCalStsFromRiGrillShttrCalSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 188
        signal_description = "GrlShttrCalSts"
        signal_length = 2
        start_position = 197
        value_definition = {'0x0': ' ExvCalibSts_NotInitialized', '0x1': ' ExvCalibSts_InitializationInProcess', '0x2': ' ExvCalibSts_Initialized', '0x3': ' ExvCalibSts_Reserved'}

    class RefrigSov3ActrSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 187
        signal_description = "SOV actuator status"
        signal_length = 2
        start_position = 195
        value_definition = {'0x0': ' Flt_Initial', '0x1': ' Flt_NoFault', '0x2': ' Flt_Fault'}


class LCURToCCUMCUCDEthSignalIPdu01:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuSoAdUDP"
    pdu_header_id = 0x602001
    pdu_length_bytes = 3
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-160ms"
    sender = "LCUR"
    server_socket = "SocketLcuRSoAdUDP"
    signal_group = {'CooltCircVlvCalSts': ['CooltCircVlvCalStsDCTVCalSts', 'CooltCircVlvCalStsWCVTCalSts', 'CooltCircVlvCalStsBCTVCalSts', 'CooltCircVlvCalStsHCTVCalSts', 'CooltCircVlvCalStsLCTVCalSts', 'CooltCircVlvCalStsCCTVCalSts', 'CooltCircVlvCalStsCooltSOV1CalSts', 'CooltCircVlvCalStsBCFVCalSts', 'CooltCircVlvCalStsECTVCalSts']}

    class CooltCircVlvCalStsDCTVCalSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 21
        signal_description = "Valve calibration status"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' ExvCalibSts_NotInitialized', '0x1': ' ExvCalibSts_InitializationInProcess', '0x2': ' ExvCalibSts_Initialized', '0x3': ' ExvCalibSts_Reserved'}

    class CooltCircVlvCalStsWCVTCalSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 21
        signal_description = "Valve calibration status"
        signal_length = 2
        start_position = 5
        value_definition = {'0x0': ' ExvCalibSts_NotInitialized', '0x1': ' ExvCalibSts_InitializationInProcess', '0x2': ' ExvCalibSts_Initialized', '0x3': ' ExvCalibSts_Reserved'}

    class CooltCircVlvCalStsBCTVCalSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 21
        signal_description = "Valve calibration status"
        signal_length = 2
        start_position = 3
        value_definition = {'0x0': ' ExvCalibSts_NotInitialized', '0x1': ' ExvCalibSts_InitializationInProcess', '0x2': ' ExvCalibSts_Initialized', '0x3': ' ExvCalibSts_Reserved'}

    class CooltCircVlvCalStsHCTVCalSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 21
        signal_description = "Valve calibration status"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': ' ExvCalibSts_NotInitialized', '0x1': ' ExvCalibSts_InitializationInProcess', '0x2': ' ExvCalibSts_Initialized', '0x3': ' ExvCalibSts_Reserved'}

    class CooltCircVlvCalStsLCTVCalSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 21
        signal_description = "Valve calibration status"
        signal_length = 2
        start_position = 15
        value_definition = {'0x0': ' ExvCalibSts_NotInitialized', '0x1': ' ExvCalibSts_InitializationInProcess', '0x2': ' ExvCalibSts_Initialized', '0x3': ' ExvCalibSts_Reserved'}

    class CooltCircVlvCalStsCCTVCalSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 21
        signal_description = "Valve calibration status"
        signal_length = 2
        start_position = 13
        value_definition = {'0x0': ' ExvCalibSts_NotInitialized', '0x1': ' ExvCalibSts_InitializationInProcess', '0x2': ' ExvCalibSts_Initialized', '0x3': ' ExvCalibSts_Reserved'}

    class CooltCircVlvCalStsCooltSOV1CalSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 21
        signal_description = "Valve calibration status"
        signal_length = 2
        start_position = 11
        value_definition = {'0x0': ' ExvCalibSts_NotInitialized', '0x1': ' ExvCalibSts_InitializationInProcess', '0x2': ' ExvCalibSts_Initialized', '0x3': ' ExvCalibSts_Reserved'}

    class CooltCircVlvCalStsBCFVCalSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 21
        signal_description = "Valve calibration status"
        signal_length = 2
        start_position = 9
        value_definition = {'0x0': ' ExvCalibSts_NotInitialized', '0x1': ' ExvCalibSts_InitializationInProcess', '0x2': ' ExvCalibSts_Initialized', '0x3': ' ExvCalibSts_Reserved'}

    class CooltCircVlvCalStsECTVCalSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 21
        signal_description = "Valve calibration status"
        signal_length = 2
        start_position = 23
        value_definition = {'0x0': ' ExvCalibSts_NotInitialized', '0x1': ' ExvCalibSts_InitializationInProcess', '0x2': ' ExvCalibSts_Initialized', '0x3': ' ExvCalibSts_Reserved'}
