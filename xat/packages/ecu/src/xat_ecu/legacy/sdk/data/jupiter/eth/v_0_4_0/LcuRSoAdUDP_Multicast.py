

class LCURMulticastEthSignalIPdu04:
    base_type = "Unsigned"
    client_socket = "SocketMulticast"
    pdu_header_id = 0x60FF04
    pdu_length_bytes = 2
    receiver = ['CCUMCUAD', 'CCUMCUCD', 'LCUL', 'CCUSOCCD']
    send_type = "Cyclic-20ms"
    sender = "LCUR"
    server_socket = "SocketLcuRSoAdUDP"
    signal_group = {}

    class FRDoorOpenClsSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 15
        signal_description = "Door Status/latch status"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' DoorSts_Unknow', '0x1': ' DoorSts_Open', '0x2': ' DoorSts_Close'}

    class HoodSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 14
        signal_description = "Door Status/latch status"
        signal_length = 2
        start_position = 5
        value_definition = {'0x0': ' DoorSts_Unknow', '0x1': ' DoorSts_Open', '0x2': ' DoorSts_Close'}

    class RRDoorOpenClsSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 13
        signal_description = "Door Status/latch status"
        signal_length = 2
        start_position = 3
        value_definition = {'0x0': ' DoorSts_Unknow', '0x1': ' DoorSts_Open', '0x2': ' DoorSts_Close'}

    class TrSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 12
        signal_description = "Trunk Status / Trunk latch status"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': ' DoorSts_Unknow', '0x1': ' DoorSts_Open', '0x2': ' DoorSts_Close'}


class LCURMulticastEthSignalIPdu06:
    base_type = "Unsigned"
    client_socket = "SocketMulticast"
    pdu_header_id = 0x60FF06
    pdu_length_bytes = 12
    receiver = ['CCUMCUAD', 'CCUMCUCD', 'CCUSOCCD', 'LCUL']
    send_type = "Cyclic-50ms"
    sender = "LCUR"
    server_socket = "SocketLcuRSoAdUDP"
    signal_group = {'FRDoorAntiPnchFb': ['FRDoorAntiPnchFbCloseAntiPnchSts', 'FRDoorAntiPnchFbCloseAntiPnchSts', 'FRDoorAntiPnchFbOPenAntiPnchSts', 'FRDoorAntiPnchFbOPenAntiPnchSts'], 'FRDoorPosnSts': ['FRDoorPosnStsDoorPercPosn', 'FRDoorPosnStsDoorPercPosn', 'FRDoorPosnStsDoorAngPosn', 'FRDoorPosnStsDoorAngPosn'], 'RRDoorAntiPnchFb': ['RRDoorAntiPnchFbCloseAntiPnchSts', 'RRDoorAntiPnchFbCloseAntiPnchSts', 'RRDoorAntiPnchFbOPenAntiPnchSts', 'RRDoorAntiPnchFbOPenAntiPnchSts'], 'RRDoorPosnSts': ['RRDoorPosnStsDoorAngPosn', 'RRDoorPosnStsDoorAngPosn', 'RRDoorPosnStsDoorPercPosn', 'RRDoorPosnStsDoorPercPosn']}

    class FRDoorOutdSwtSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 51
        signal_description = "Switch status of Outside door"
        signal_length = 3
        start_position = 2
        value_definition = {'0x0': ' SwtSts_IniVal', '0x1': ' SwtSts_Pressd', '0x2': ' SwtSts_NotPressd', '0x3': ' SwtSts_SWStuck', '0x4': ' SwtSts_Error'}

    class RRDoorOutdSwtSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 85
        signal_description = "Switch status of Outside door"
        signal_length = 3
        start_position = 55
        value_definition = {'0x0': ' SwtSts_IniVal', '0x1': ' SwtSts_Pressd', '0x2': ' SwtSts_NotPressd', '0x3': ' SwtSts_SWStuck', '0x4': ' SwtSts_Error'}

    class ExtrReViewMirrFoldStsPass:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 92
        signal_description = "the folding status of external rear view mirror at passenger"
        signal_length = 3
        start_position = 95
        value_definition = {'0x0': ' MirrFoldSts_MirrPosnIdle', '0x1': ' MirrFoldSts_MirrUnFoldPosn', '0x2': ' MirrFoldSts_MirrFoldPosn', '0x3': ' MirrFoldSts_MirrMovgToUnFold', '0x4': ' MirrFoldSts_MirrMovgToFold', '0x5': ' MirrFoldSts_MirrPosnUndefd'}

    class FRDoorAntiPnchFbCloseAntiPnchSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 24
        signal_description = "Door closing direction antipnch status"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class FRDoorAntiPnchFbOPenAntiPnchSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 24
        signal_description = "Door opening direction antipnch status"
        signal_length = 1
        start_position = 6
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class FRDoorInsdSwtSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 40
        signal_description = "Switch status of inside door"
        signal_length = 3
        start_position = 5
        value_definition = {'0x0': ' SwtSts_IniVal', '0x1': ' SwtSts_Pressd', '0x2': ' SwtSts_NotPressd', '0x3': ' SwtSts_SWStuck', '0x4': ' SwtSts_Error'}

    class FRDoorMtnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 52
        signal_description = "Power side door motion status"
        signal_length = 4
        start_position = 15
        value_definition = {'0x0': ' DoorMtnSts_IniVal', '0x1': ' DoorMtnSts_FullOpen', '0x2': ' DoorMtnSts_FullClose', '0x3': ' DoorMtnSts_StopDurOpen', '0x4': ' DoorMtnSts_StopDurClose', '0x5': ' DoorMtnSts_MovingOut', '0x6': ' DoorMtnSts_MovingIn', '0x7': ' DoorMtnSts_HalfClose', '0x8': ' DoorMtnSts_Unknow', '0x9': ' DoorMtnSts_OnlyOpenPosn'}

    class FRDoorPosnStsDoorPercPosn:
        comments = ""
        factor = 1.0
        initial_value = 101
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 50
        signal_description = "door percentage position"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class FRDoorPosnStsDoorAngPosn:
        comments = ""
        factor = 1.0
        initial_value = 101
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 50
        signal_description = "power side door Opening angle"
        signal_length = 7
        start_position = 31
        value_definition = {}

    class FRDoorSpd:
        comments = ""
        factor = 0.5
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 49
        signal_description = "Speed of power side door"
        signal_length = 8
        start_position = 39
        value_definition = {}

    class RRChdLockSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 48
        signal_description = "children lock status"
        signal_length = 2
        start_position = 47
        value_definition = {'0x0': ' DoorLockSts_Unknow', '0x1': ' DoorLockSts_Lock', '0x2': ' DoorLockSts_Unlock'}

    class RRDoorAntiPnchFbCloseAntiPnchSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 64
        signal_description = "power side door close direction AntiPnch status"
        signal_length = 1
        start_position = 45
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class RRDoorAntiPnchFbOPenAntiPnchSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 64
        signal_description = "power side door open direction AntiPnch status"
        signal_length = 1
        start_position = 44
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class RRDoorInsdSwtSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 87
        signal_description = "Switch status of inside door"
        signal_length = 3
        start_position = 43
        value_definition = {'0x0': ' SwtSts_IniVal', '0x1': ' SwtSts_Pressd', '0x2': ' SwtSts_NotPressd', '0x3': ' SwtSts_SWStuck', '0x4': ' SwtSts_Error'}

    class RRDoorMtnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 86
        signal_description = "Power side door motion status"
        signal_length = 4
        start_position = 11
        value_definition = {'0x0': ' DoorMtnSts_IniVal', '0x1': ' DoorMtnSts_FullOpen', '0x2': ' DoorMtnSts_FullClose', '0x3': ' DoorMtnSts_StopDurOpen', '0x4': ' DoorMtnSts_StopDurClose', '0x5': ' DoorMtnSts_MovingOut', '0x6': ' DoorMtnSts_MovingIn', '0x7': ' DoorMtnSts_HalfClose', '0x8': ' DoorMtnSts_Unknow', '0x9': ' DoorMtnSts_OnlyOpenPosn'}

    class RRDoorPosnStsDoorAngPosn:
        comments = ""
        factor = 1.0
        initial_value = 101
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 84
        signal_description = "door angle position"
        signal_length = 7
        start_position = 71
        value_definition = {}

    class RRDoorPosnStsDoorPercPosn:
        comments = ""
        factor = 1.0
        initial_value = 101
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 84
        signal_description = "door percentage position"
        signal_length = 8
        start_position = 63
        value_definition = {}

    class RRDoorSpd:
        comments = ""
        factor = 0.5
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 83
        signal_description = "Speed of power side door"
        signal_length = 8
        start_position = 79
        value_definition = {}

    class PassReViewMirrDimFailr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 80
        signal_description = "副驾侧后视镜防眩光故障"
        signal_length = 2
        start_position = 82
        value_definition = {'0x0': ' IntrReViewMirrDimFailr_NoFault', '0x1': ' IntrReViewMirrDimFailr_InternalFailure', '0x2': ' IntrReViewMirrDimFailr_Reserved1', '0x3': ' IntrReViewMirrDimFailr_Reserved2'}


class LCURMulticastEthSignalIPdu01:
    base_type = "Unsigned"
    client_socket = "SocketMulticast"
    pdu_header_id = 0x60FF01
    pdu_length_bytes = 90
    receiver = ['CCUMCUAD', 'CCUMCUCD', 'CCUSOCCD', 'LCUL']
    send_type = "Cyclic-100ms"
    sender = "LCUR"
    server_socket = "SocketLcuRSoAdUDP"
    signal_group = {'AmbTEstimd': ['AmbTEstimdTQF', 'AmbTEstimdTQF', 'AmbTEstimdTQF', 'AmbTEstimdTQF', 'AmbTEstimdT', 'AmbTEstimdT', 'AmbTEstimdT', 'AmbTEstimdT'], 'EvaprTEstimdFrnt': ['EvaprTEstimdFrntTQF', 'EvaprTEstimdFrntTQF', 'EvaprTEstimdFrntT', 'EvaprTEstimdFrntT'], 'EvaprTEstimdRe': ['EvaprTEstimdReTQF', 'EvaprTEstimdReTQF', 'EvaprTEstimdReT', 'EvaprTEstimdReT'], 'FrntBlwrSts': ['FrntBlwrStsActPWM', 'FrntBlwrStsActPWM', 'FrntBlwrStsOnOffSts', 'FrntBlwrStsOnOffSts', 'FrntBlwrStsElecErr', 'FrntBlwrStsElecErr', 'FrntBlwrStsEgyLim', 'FrntBlwrStsEgyLim', 'FrntBlwrStsOverTemp', 'FrntBlwrStsOverTemp', 'FrntBlwrStsVoltErr', 'FrntBlwrStsVoltErr'], 'FrntEndCmptStsFromRi': ['FrntEndCmptStsFromRiGrillShttrSts', 'FrntEndCmptStsFromRiGrillShttrSts', 'FrntEndCmptStsFromRiCoolgFanSts', 'FrntEndCmptStsFromRiCoolgFanSts'], 'FRPwrDoorErrFb': ['FRPwrDoorErrFbPosnUnknowFb', 'FRPwrDoorErrFbPosnUnknowFb', 'FRPwrDoorErrFbBoolean', 'FRPwrDoorErrFbBoolean', 'FRPwrDoorErrFbMotThermErrFb', 'FRPwrDoorErrFbMotThermErrFb', 'FRPwrDoorErrFbHallErrFb', 'FRPwrDoorErrFbHallErrFb', 'FRPwrDoorErrFbRollAngErrFb', 'FRPwrDoorErrFbRollAngErrFb'], 'HexTEstimdFrnt': ['HexTEstimdFrntTQF', 'HexTEstimdFrntTQF', 'HexTEstimdFrntT', 'HexTEstimdFrntT'], 'HoodMotErrFb': ['HoodMotErrFbBoolean4', 'HoodMotErrFbBoolean4', 'HoodMotErrFbBoolean3', 'HoodMotErrFbBoolean3', 'HoodMotErrFbBoolean1', 'HoodMotErrFbBoolean1', 'HoodMotErrFbBoolean2', 'HoodMotErrFbBoolean2'], 'PwrChRiActSts': ['PwrChRiActStsSwilPwrChRi24ActSts', 'PwrChRiActStsSwilPwrChRi24ActSts', 'PwrChRiActStsSwilPwrChRi3ActSts', 'PwrChRiActStsSwilPwrChRi3ActSts', 'PwrChRiActStsSwilPwrChRi14ActSts', 'PwrChRiActStsSwilPwrChRi14ActSts', 'PwrChRiActStsSwilPwrChRi28ActSts', 'PwrChRiActStsSwilPwrChRi28ActSts', 'PwrChRiActStsSwilPwrChRi7ActSts', 'PwrChRiActStsSwilPwrChRi7ActSts', 'PwrChRiActStsSwilPwrChRi15ActSts', 'PwrChRiActStsSwilPwrChRi15ActSts', 'PwrChRiActStsSwilPwrChRi23ActSts', 'PwrChRiActStsSwilPwrChRi23ActSts', 'PwrChRiActStsSwilPwrChRi4ActSts', 'PwrChRiActStsSwilPwrChRi4ActSts', 'PwrChRiActStsContnsPwrChRi3ActSts', 'PwrChRiActStsContnsPwrChRi3ActSts', 'PwrChRiActStsSwilPwrChRi25ActSts', 'PwrChRiActStsSwilPwrChRi25ActSts', 'PwrChRiActStsSwilPwrChRi9ActSts', 'PwrChRiActStsSwilPwrChRi9ActSts', 'PwrChRiActStsSwilPwrChRi21ActSts', 'PwrChRiActStsSwilPwrChRi21ActSts', 'PwrChRiActStsSwilPwrChRi19ActSts', 'PwrChRiActStsSwilPwrChRi19ActSts', 'PwrChRiActStsContnsPwrChRi1ActSts', 'PwrChRiActStsContnsPwrChRi1ActSts', 'PwrChRiActStsSwilPwrChRi13ActSts', 'PwrChRiActStsSwilPwrChRi13ActSts', 'PwrChRiActStsContnsPwrChRi2ActSts', 'PwrChRiActStsContnsPwrChRi2ActSts', 'PwrChRiActStsSwilPwrChRi5ActSts', 'PwrChRiActStsSwilPwrChRi5ActSts', 'PwrChRiActStsSwilPwrChRi11ActSts', 'PwrChRiActStsSwilPwrChRi11ActSts', 'PwrChRiActStsSwilPwrChRi27ActSts', 'PwrChRiActStsSwilPwrChRi27ActSts', 'PwrChRiActStsSwilPwrChRi12ActSts', 'PwrChRiActStsSwilPwrChRi12ActSts', 'PwrChRiActStsSwilPwrChRi29ActSts', 'PwrChRiActStsSwilPwrChRi29ActSts', 'PwrChRiActStsSwilPwrChRi1ActSts', 'PwrChRiActStsSwilPwrChRi1ActSts', 'PwrChRiActStsSwilPwrChRi10ActSts', 'PwrChRiActStsSwilPwrChRi10ActSts', 'PwrChRiActStsSwilPwrChRi16ActSts', 'PwrChRiActStsSwilPwrChRi16ActSts', 'PwrChRiActStsSwilPwrChRi2ActSts', 'PwrChRiActStsSwilPwrChRi2ActSts', 'PwrChRiActStsSwilPwrChRi26ActSts', 'PwrChRiActStsSwilPwrChRi26ActSts', 'PwrChRiActStsSwilPwrChRi17ActSts', 'PwrChRiActStsSwilPwrChRi17ActSts', 'PwrChRiActStsContnsPwrChRi4ActSts', 'PwrChRiActStsContnsPwrChRi4ActSts', 'PwrChRiActStsSwilPwrChRi6ActSts', 'PwrChRiActStsSwilPwrChRi6ActSts', 'PwrChRiActStsSwilPwrChRi22ActSts', 'PwrChRiActStsSwilPwrChRi22ActSts', 'PwrChRiActStsContnsPwrChRi5ActSts', 'PwrChRiActStsContnsPwrChRi5ActSts', 'PwrChRiActStsSwilPwrChRi8ActSts', 'PwrChRiActStsSwilPwrChRi8ActSts', 'PwrChRiActStsSwilPwrChRi20ActSts', 'PwrChRiActStsSwilPwrChRi20ActSts', 'PwrChRiActStsSwilPwrChRi18ActSts', 'PwrChRiActStsSwilPwrChRi18ActSts'], 'PwrChRiErr': ['PwrChRiErrSwilPwrChRi29Err', 'PwrChRiErrSwilPwrChRi29Err', 'PwrChRiErrSwilPwrChRi9Err', 'PwrChRiErrSwilPwrChRi9Err', 'PwrChRiErrSwilPwrChRi19Err', 'PwrChRiErrSwilPwrChRi19Err', 'PwrChRiErrSwilPwrChRi7Err', 'PwrChRiErrSwilPwrChRi7Err', 'PwrChRiErrSwilPwrChRi20Err', 'PwrChRiErrSwilPwrChRi20Err', 'PwrChRiErrContnsPwrChRi2Err', 'PwrChRiErrContnsPwrChRi2Err', 'PwrChRiErrSwilPwrChRi27Err', 'PwrChRiErrSwilPwrChRi27Err', 'PwrChRiErrSwilPwrChRi3Err', 'PwrChRiErrSwilPwrChRi3Err', 'PwrChRiErrSwilPwrChRi18Err', 'PwrChRiErrSwilPwrChRi18Err', 'PwrChRiErrSwilPwrChRi22Err', 'PwrChRiErrSwilPwrChRi22Err', 'PwrChRiErrSwilPwrChRi13Err', 'PwrChRiErrSwilPwrChRi13Err', 'PwrChRiErrSwilPwrChRi10Err', 'PwrChRiErrSwilPwrChRi10Err', 'PwrChRiErrSwilPwrChRi24Err', 'PwrChRiErrSwilPwrChRi24Err', 'PwrChRiErrSwilPwrChRi28Err', 'PwrChRiErrSwilPwrChRi28Err', 'PwrChRiErrContnsPwrChRi4Err', 'PwrChRiErrContnsPwrChRi4Err', 'PwrChRiErrSwilPwrChRi1Err', 'PwrChRiErrSwilPwrChRi1Err', 'PwrChRiErrSwilPwrChRi16Err', 'PwrChRiErrSwilPwrChRi16Err', 'PwrChRiErrSwilPwrChRi25Err', 'PwrChRiErrSwilPwrChRi25Err', 'PwrChRiErrSwilPwrChRi12Err', 'PwrChRiErrSwilPwrChRi12Err', 'PwrChRiErrContnsPwrChRi5Err', 'PwrChRiErrContnsPwrChRi5Err', 'PwrChRiErrContnsPwrChRi1Err', 'PwrChRiErrContnsPwrChRi1Err', 'PwrChRiErrSwilPwrChRi17Err', 'PwrChRiErrSwilPwrChRi17Err', 'PwrChRiErrSwilPwrChRi21Err', 'PwrChRiErrSwilPwrChRi21Err', 'PwrChRiErrSwilPwrChRi2Err', 'PwrChRiErrSwilPwrChRi2Err', 'PwrChRiErrSwilPwrChRi6Err', 'PwrChRiErrSwilPwrChRi6Err', 'PwrChRiErrSwilPwrChRi14Err', 'PwrChRiErrSwilPwrChRi14Err', 'PwrChRiErrSwilPwrChRi15Err', 'PwrChRiErrSwilPwrChRi15Err', 'PwrChRiErrSwilPwrChRi4Err', 'PwrChRiErrSwilPwrChRi4Err', 'PwrChRiErrSwilPwrChRi8Err', 'PwrChRiErrSwilPwrChRi8Err', 'PwrChRiErrSwilPwrChRi5Err', 'PwrChRiErrSwilPwrChRi5Err', 'PwrChRiErrSwilPwrChRi11Err', 'PwrChRiErrSwilPwrChRi11Err', 'PwrChRiErrSwilPwrChRi23Err', 'PwrChRiErrSwilPwrChRi23Err', 'PwrChRiErrSwilPwrChRi26Err', 'PwrChRiErrSwilPwrChRi26Err', 'PwrChRiErrContnsPwrChRi3Err', 'PwrChRiErrContnsPwrChRi3Err'], 'ReBlwrSts': ['ReBlwrStsOverTemp', 'ReBlwrStsOverTemp', 'ReBlwrStsElecErr', 'ReBlwrStsElecErr', 'ReBlwrStsEgyLim', 'ReBlwrStsEgyLim', 'ReBlwrStsOnOffSts', 'ReBlwrStsOnOffSts', 'ReBlwrStsVoltErr', 'ReBlwrStsVoltErr', 'ReBlwrStsActPWM', 'ReBlwrStsActPWM'], 'RefrigCircVlvCalStsFromRi': ['RefrigCircVlvCalStsFromRiREXVCalSts', 'RefrigCircVlvCalStsFromRiREXVCalSts', 'RefrigCircVlvCalStsFromRiCERVCalSts', 'RefrigCircVlvCalStsFromRiCERVCalSts', 'RefrigCircVlvCalStsFromRiFEXVCalSts', 'RefrigCircVlvCalStsFromRiFEXVCalSts', 'RefrigCircVlvCalStsFromRiBEXVCalSts', 'RefrigCircVlvCalStsFromRiBEXVCalSts', 'RefrigCircVlvCalStsFromRiTERVCalSts', 'RefrigCircVlvCalStsFromRiTERVCalSts', 'RefrigCircVlvCalStsFromRiWERVCalSts', 'RefrigCircVlvCalStsFromRiWERVCalSts'], 'RefrigCircVlvStsFromRi': ['RefrigCircVlvStsFromRiRefrigSOV2Sts', 'RefrigCircVlvStsFromRiRefrigSOV2Sts', 'RefrigCircVlvStsFromRiREXVSts', 'RefrigCircVlvStsFromRiREXVSts', 'RefrigCircVlvStsFromRiRefrigSOV1Sts', 'RefrigCircVlvStsFromRiRefrigSOV1Sts', 'RefrigCircVlvStsFromRiWERVSts', 'RefrigCircVlvStsFromRiWERVSts', 'RefrigCircVlvStsFromRiFEXVSts', 'RefrigCircVlvStsFromRiFEXVSts', 'RefrigCircVlvStsFromRiCERVSts', 'RefrigCircVlvStsFromRiCERVSts', 'RefrigCircVlvStsFromRiTERVSts', 'RefrigCircVlvStsFromRiTERVSts', 'RefrigCircVlvStsFromRiBEXVSts', 'RefrigCircVlvStsFromRiBEXVSts', 'RefrigCircVlvStsFromRiRefrigSOV3Sts', 'RefrigCircVlvStsFromRiRefrigSOV3Sts'], 'RRChdLockErrFb': ['RRChdLockErrFbLockFail', 'RRChdLockErrFbLockFail', 'RRChdLockErrFbUnlockFail', 'RRChdLockErrFbUnlockFail', 'RRChdLockErrFbError1', 'RRChdLockErrFbError1', 'RRChdLockErrFbMotorOverTherm', 'RRChdLockErrFbMotorOverTherm', 'RRChdLockErrFbError2', 'RRChdLockErrFbError2'], 'RRPwrDoorErrFb': ['RRPwrDoorErrFbRollAngErrFb', 'RRPwrDoorErrFbRollAngErrFb', 'RRPwrDoorErrFbBoolean', 'RRPwrDoorErrFbBoolean', 'RRPwrDoorErrFbPosnUnknowFb', 'RRPwrDoorErrFbPosnUnknowFb', 'RRPwrDoorErrFbHallErrFb', 'RRPwrDoorErrFbHallErrFb', 'RRPwrDoorErrFbMotThermErrFb', 'RRPwrDoorErrFbMotThermErrFb'], 'CmptmtAirFlwEstimd': ['CmptmtAirFlwEstimdFrnt', 'CmptmtAirFlwEstimdFrnt', 'CmptmtAirFlwEstimdRe', 'CmptmtAirFlwEstimdRe'], 'IncarTFrntEstimd': ['IncarTFrntEstimdFanRunng', 'IncarTFrntEstimdFanRunng', 'IncarTFrntEstimdTQf', 'IncarTFrntEstimdTQf', 'IncarTFrntEstimdT', 'IncarTFrntEstimdT'], 'TrunkLiDrvReq': ['TrunkLiDrvReqLiPerc', 'TrunkLiDrvReqLightCmd', 'TrunkLiDrvReqReadingLiDimsSpdCmd']}

    class AmbTEstimdTQF:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 80
        signal_description = "Ambient Temperature Quality Flag"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' HVACTempQf_SnsrDataNotOk', '0x1': ' HVACTempQf_SnsrDataOk'}

    class AmbTEstimdT:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = 80
        signal_description = "Ambient Temperature"
        signal_length = 13
        start_position = 6
        value_definition = {}

    class HVECmprPwrCns:
        comments = ""
        factor = 10.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 213
        signal_description = "Compressor Power Consumption"
        signal_length = 13
        start_position = 9
        value_definition = {}

    class CoolgFanPwrCns:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 211
        signal_description = "Cooling Fan Power Consumption"
        signal_length = 12
        start_position = 40
        value_definition = {}

    class EvaprTEstimdFrntTQF:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 210
        signal_description = "Front Evaporator Air Temperature Quality Flag"
        signal_length = 1
        start_position = 60
        value_definition = {'0x0': ' HVACTempQf_SnsrDataNotOk', '0x1': ' HVACTempQf_SnsrDataOk'}

    class EvaprTEstimdFrntT:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = 210
        signal_description = "Front Evaporator Air Temperature"
        signal_length = 13
        start_position = 59
        value_definition = {}

    class EvaprTEstimdReTQF:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 209
        signal_description = "Rear Evaporator Air Temperature Quality Flag"
        signal_length = 1
        start_position = 78
        value_definition = {'0x0': ' HVACTempQf_SnsrDataNotOk', '0x1': ' HVACTempQf_SnsrDataOk'}

    class EvaprTEstimdReT:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = 209
        signal_description = "Rear Evaporator Air Temperature"
        signal_length = 13
        start_position = 77
        value_definition = {}

    class FRDoorMaxPosnSetFb:
        comments = ""
        factor = 1.0
        initial_value = 101
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 208
        signal_description = "Maximum percentage feedback that power side doors can open"
        signal_length = 8
        start_position = 95
        value_definition = {}

    class FRDoorModSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 509
        signal_description = "power side door mode status"
        signal_length = 2
        start_position = 103
        value_definition = {'0x0': ' DoorModSts_ElecMode', '0x1': ' DoorModSts_ManualMode'}

    class FrntBlwrStsActPWM:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 508
        signal_description = "Compartment Front Blower Actual PWM"
        signal_length = 10
        start_position = 101
        value_definition = {}

    class FrntBlwrStsOnOffSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 508
        signal_description = "Compartment Front Blower OnOff Status"
        signal_length = 2
        start_position = 107
        value_definition = {'0x0': ' BlwrSts_OFF', '0x1': ' BlwrSts_ON', '0x2': ' BlwrSts_Err', '0x3': ' BlwrSts_Reserved'}

    class FrntBlwrStsElecErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 508
        signal_description = "Compartment Front Blower Electrical Error"
        signal_length = 2
        start_position = 105
        value_definition = {'0x0': ' ElecErr_Normal', '0x1': ' ElecErr_ShortToGroundOrOpenCircuit', '0x2': ' ElecErr_ShortToBatt', '0x3': ' ElecErr_Reserved'}

    class FrntBlwrStsEgyLim:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 508
        signal_description = "Compartment Front Blower Energy Limit Status"
        signal_length = 1
        start_position = 119
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class FrntBlwrStsOverTemp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 508
        signal_description = "Compartment Front Blower Over Temperature"
        signal_length = 1
        start_position = 118
        value_definition = {'0x0': ' MotOverTemp_Normal', '0x1': ' MotOverTemp_OverTemp'}

    class FrntBlwrStsVoltErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 508
        signal_description = "Compartment Front Blower Voltage Error"
        signal_length = 2
        start_position = 117
        value_definition = {'0x0': ' VoltErr_Normal', '0x1': ' VoltErr_UnderVolt', '0x2': ' VoltErr_OverVolt', '0x3': ' VoltErr_Reserved'}

    class FrntEndCmptStsFromRiGrillShttrSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 506
        signal_description = "AGM Status"
        signal_length = 3
        start_position = 133
        value_definition = {'0x0': ' ThermCooltVlvSts_Unknow', '0x1': ' ThermCooltVlvSts_Normal', '0x2': ' ThermCooltVlvSts_Err'}

    class FrntEndCmptStsFromRiCoolgFanSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 506
        signal_description = "Cooling Fan Status"
        signal_length = 3
        start_position = 130
        value_definition = {'0x0': ' ThermCooltVlvSts_Unknow', '0x1': ' ThermCooltVlvSts_Normal', '0x2': ' ThermCooltVlvSts_Err'}

    class FRPwrDoorErrFbPosnUnknowFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 505
        signal_description = "door position lost"
        signal_length = 1
        start_position = 143
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class FRPwrDoorErrFbBoolean:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 505
        signal_description = "error status"
        signal_length = 1
        start_position = 142
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class FRPwrDoorErrFbMotThermErrFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 505
        signal_description = "Motor overheating"
        signal_length = 1
        start_position = 141
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class FRPwrDoorErrFbHallErrFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 505
        signal_description = "hall error"
        signal_length = 1
        start_position = 140
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class FRPwrDoorErrFbRollAngErrFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 505
        signal_description = "roll angle error"
        signal_length = 1
        start_position = 139
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class GloveBoxMotSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 504
        signal_description = "glove box motor active status"
        signal_length = 3
        start_position = 138
        value_definition = {'0x0': ' MotSts_Inactive', '0x1': ' MotSts_Active', '0x2': ' MotSts_ResetActive'}

    class HexTEstimdFrntTQF:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 655
        signal_description = "Front Hex Air Temperature Quality Flag"
        signal_length = 1
        start_position = 151
        value_definition = {'0x0': ' HVACTempQf_SnsrDataNotOk', '0x1': ' HVACTempQf_SnsrDataOk'}

    class HexTEstimdFrntT:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = 655
        signal_description = "Front Hex Air Temperature"
        signal_length = 13
        start_position = 150
        value_definition = {}

    class HoodMotErrFbBoolean4:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 654
        signal_description = "Hood Error status feedback"
        signal_length = 1
        start_position = 153
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class HoodMotErrFbBoolean3:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 654
        signal_description = "Hood Error status feedback"
        signal_length = 1
        start_position = 152
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class HoodMotErrFbBoolean1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 654
        signal_description = "Hood Error status feedback"
        signal_length = 1
        start_position = 167
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class HoodMotErrFbBoolean2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 654
        signal_description = "Hood Error status feedback"
        signal_length = 1
        start_position = 166
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class PwrChRiActStsSwilPwrChRi24ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 652
        signal_description = "Right Zone Swil Power Channel 24 Actual Status"
        signal_length = 1
        start_position = 183
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChRiActStsSwilPwrChRi3ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 652
        signal_description = "Right Zone Swil Power Channel 3 Actual Status"
        signal_length = 1
        start_position = 182
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChRiActStsSwilPwrChRi14ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 652
        signal_description = "Right Zone Swil Power Channel 14 Actual Status"
        signal_length = 1
        start_position = 181
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChRiActStsSwilPwrChRi28ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 652
        signal_description = "Right Zone Swil Power Channel 28 Actual Status"
        signal_length = 1
        start_position = 180
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChRiActStsSwilPwrChRi7ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 652
        signal_description = "Right Zone Swil Power Channel 7 Actual Status"
        signal_length = 1
        start_position = 179
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChRiActStsSwilPwrChRi15ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 652
        signal_description = "Right Zone Swil Power Channel 15 Actual Status"
        signal_length = 1
        start_position = 178
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChRiActStsSwilPwrChRi23ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 652
        signal_description = "Right Zone Swil Power Channel 23 Actual Status"
        signal_length = 1
        start_position = 177
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChRiActStsSwilPwrChRi4ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 652
        signal_description = "Right Zone Swil Power Channel 4 Actual Status"
        signal_length = 1
        start_position = 176
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChRiActStsContnsPwrChRi3ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 652
        signal_description = "Right Zone Contns Power Channel 3 Actual Status"
        signal_length = 1
        start_position = 191
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChRiActStsSwilPwrChRi25ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 652
        signal_description = "Right Zone Swil Power Channel 25 Actual Status"
        signal_length = 1
        start_position = 190
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChRiActStsSwilPwrChRi9ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 652
        signal_description = "Right Zone Swil Power Channel 9 Actual Status"
        signal_length = 1
        start_position = 189
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChRiActStsSwilPwrChRi21ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 652
        signal_description = "Right Zone Swil Power Channel 21 Actual Status"
        signal_length = 1
        start_position = 188
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChRiActStsSwilPwrChRi19ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 652
        signal_description = "Right Zone Swil Power Channel 19 Actual Status"
        signal_length = 1
        start_position = 187
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChRiActStsContnsPwrChRi1ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 652
        signal_description = "Right Zone Contns Power Channel 1 Actual Status"
        signal_length = 1
        start_position = 186
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChRiActStsSwilPwrChRi13ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 652
        signal_description = "Right Zone Swil Power Channel 13 Actual Status"
        signal_length = 1
        start_position = 185
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChRiActStsContnsPwrChRi2ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 652
        signal_description = "Right Zone Contns Power Channel 2 Actual Status"
        signal_length = 1
        start_position = 184
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChRiActStsSwilPwrChRi5ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 652
        signal_description = "Right Zone Swil Power Channel 5 Actual Status"
        signal_length = 1
        start_position = 199
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChRiActStsSwilPwrChRi11ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 652
        signal_description = "Right Zone Swil Power Channel 11 Actual Status"
        signal_length = 1
        start_position = 198
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChRiActStsSwilPwrChRi27ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 652
        signal_description = "Right Zone Swil Power Channel 27 Actual Status"
        signal_length = 1
        start_position = 197
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChRiActStsSwilPwrChRi12ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 652
        signal_description = "Right Zone Swil Power Channel 12 Actual Status"
        signal_length = 1
        start_position = 196
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChRiActStsSwilPwrChRi29ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 652
        signal_description = "Right Zone Swil Power Channel 29 Actual Status"
        signal_length = 1
        start_position = 195
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChRiActStsSwilPwrChRi1ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 652
        signal_description = "Right Zone Swil Power Channel 1 Actual Status"
        signal_length = 1
        start_position = 194
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChRiActStsSwilPwrChRi10ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 652
        signal_description = "Right Zone Swil Power Channel 10 Actual Status"
        signal_length = 1
        start_position = 193
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChRiActStsSwilPwrChRi16ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 652
        signal_description = "Right Zone Swil Power Channel 16 Actual Status"
        signal_length = 1
        start_position = 192
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChRiActStsSwilPwrChRi2ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 652
        signal_description = "Right Zone Swil Power Channel 2 Actual Status"
        signal_length = 1
        start_position = 207
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChRiActStsSwilPwrChRi26ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 652
        signal_description = "Right Zone Swil Power Channel 26 Actual Status"
        signal_length = 1
        start_position = 206
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChRiActStsSwilPwrChRi17ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 652
        signal_description = "Right Zone Swil Power Channel 17 Actual Status"
        signal_length = 1
        start_position = 205
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChRiActStsContnsPwrChRi4ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 652
        signal_description = "Right Zone Contns Power Channel 4 Actual Status"
        signal_length = 1
        start_position = 204
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChRiActStsSwilPwrChRi6ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 652
        signal_description = "Right Zone Swil Power Channel 6 Actual Status"
        signal_length = 1
        start_position = 203
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChRiActStsSwilPwrChRi22ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 652
        signal_description = "Right Zone Swil Power Channel 22 Actual Status"
        signal_length = 1
        start_position = 202
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChRiActStsContnsPwrChRi5ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 652
        signal_description = "Right Zone Contns Power Channel 5 Actual Status"
        signal_length = 1
        start_position = 201
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChRiActStsSwilPwrChRi8ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 652
        signal_description = "Right Zone Swil Power Channel 8 Actual Status"
        signal_length = 1
        start_position = 200
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChRiActStsSwilPwrChRi20ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 652
        signal_description = "Right Zone Swil Power Channel 20 Actual Status"
        signal_length = 1
        start_position = 215
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChRiActStsSwilPwrChRi18ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 652
        signal_description = "Right Zone Swil Power Channel 18 Actual Status"
        signal_length = 1
        start_position = 214
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChRiErrSwilPwrChRi29Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 651
        signal_description = "Right Zone Swil Power Channel 29 Error Status"
        signal_length = 8
        start_position = 223
        value_definition = {}

    class PwrChRiErrSwilPwrChRi9Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 651
        signal_description = "Right Zone Swil Power Channel 9 Error Status"
        signal_length = 8
        start_position = 231
        value_definition = {}

    class PwrChRiErrSwilPwrChRi19Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 651
        signal_description = "Right Zone Swil Power Channel 19 Error Status"
        signal_length = 8
        start_position = 239
        value_definition = {}

    class PwrChRiErrSwilPwrChRi7Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 651
        signal_description = "Right Zone Swil Power Channel 7 Error Status"
        signal_length = 8
        start_position = 247
        value_definition = {}

    class PwrChRiErrSwilPwrChRi20Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 651
        signal_description = "Right Zone Swil Power Channel 20 Error Status"
        signal_length = 8
        start_position = 255
        value_definition = {}

    class PwrChRiErrContnsPwrChRi2Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 651
        signal_description = "Right Zone Contns Power Channel 2 Error Status"
        signal_length = 8
        start_position = 263
        value_definition = {}

    class PwrChRiErrSwilPwrChRi27Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 651
        signal_description = "Right Zone Swil Power Channel 27 Error Status"
        signal_length = 8
        start_position = 271
        value_definition = {}

    class PwrChRiErrSwilPwrChRi3Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 651
        signal_description = "Right Zone Swil Power Channel 3 Error Status"
        signal_length = 8
        start_position = 279
        value_definition = {}

    class PwrChRiErrSwilPwrChRi18Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 651
        signal_description = "Right Zone Swil Power Channel 18 Error Status"
        signal_length = 8
        start_position = 287
        value_definition = {}

    class PwrChRiErrSwilPwrChRi22Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 651
        signal_description = "Right Zone Swil Power Channel 22 Error Status"
        signal_length = 8
        start_position = 295
        value_definition = {}

    class PwrChRiErrSwilPwrChRi13Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 651
        signal_description = "Right Zone Swil Power Channel 13 Error Status"
        signal_length = 8
        start_position = 303
        value_definition = {}

    class PwrChRiErrSwilPwrChRi10Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 651
        signal_description = "Right Zone Swil Power Channel 10 Error Status"
        signal_length = 8
        start_position = 311
        value_definition = {}

    class PwrChRiErrSwilPwrChRi24Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 651
        signal_description = "Right Zone Swil Power Channel 24 Error Status"
        signal_length = 8
        start_position = 319
        value_definition = {}

    class PwrChRiErrSwilPwrChRi28Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 651
        signal_description = "Right Zone Swil Power Channel 28 Error Status"
        signal_length = 8
        start_position = 327
        value_definition = {}

    class PwrChRiErrContnsPwrChRi4Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 651
        signal_description = "Right Zone Contns Power Channel 4 Error Status"
        signal_length = 8
        start_position = 335
        value_definition = {}

    class PwrChRiErrSwilPwrChRi1Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 651
        signal_description = "Right Zone Swil Power Channel 1 Error Status"
        signal_length = 8
        start_position = 343
        value_definition = {}

    class PwrChRiErrSwilPwrChRi16Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 651
        signal_description = "Right Zone Swil Power Channel 16 Error Status"
        signal_length = 8
        start_position = 351
        value_definition = {}

    class PwrChRiErrSwilPwrChRi25Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 651
        signal_description = "Right Zone Swil Power Channel 25 Error Status"
        signal_length = 8
        start_position = 359
        value_definition = {}

    class PwrChRiErrSwilPwrChRi12Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 651
        signal_description = "Right Zone Swil Power Channel 12 Error Status"
        signal_length = 8
        start_position = 367
        value_definition = {}

    class PwrChRiErrContnsPwrChRi5Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 651
        signal_description = "Right Zone Contns Power Channel 5 Error Status"
        signal_length = 8
        start_position = 375
        value_definition = {}

    class PwrChRiErrContnsPwrChRi1Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 651
        signal_description = "Right Zone Contns Power Channel 1 Error Status"
        signal_length = 8
        start_position = 383
        value_definition = {}

    class PwrChRiErrSwilPwrChRi17Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 651
        signal_description = "Right Zone Swil Power Channel 17 Error Status"
        signal_length = 8
        start_position = 391
        value_definition = {}

    class PwrChRiErrSwilPwrChRi21Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 651
        signal_description = "Right Zone Swil Power Channel 21 Error Status"
        signal_length = 8
        start_position = 399
        value_definition = {}

    class PwrChRiErrSwilPwrChRi2Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 651
        signal_description = "Right Zone Swil Power Channel 2 Error Status"
        signal_length = 8
        start_position = 407
        value_definition = {}

    class PwrChRiErrSwilPwrChRi6Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 651
        signal_description = "Right Zone Swil Power Channel 6 Error Status"
        signal_length = 8
        start_position = 415
        value_definition = {}

    class PwrChRiErrSwilPwrChRi14Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 651
        signal_description = "Right Zone Swil Power Channel 14 Error Status"
        signal_length = 8
        start_position = 423
        value_definition = {}

    class PwrChRiErrSwilPwrChRi15Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 651
        signal_description = "Right Zone Swil Power Channel 15 Error Status"
        signal_length = 8
        start_position = 431
        value_definition = {}

    class PwrChRiErrSwilPwrChRi4Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 651
        signal_description = "Right Zone Swil Power Channel 4 Error Status"
        signal_length = 8
        start_position = 439
        value_definition = {}

    class PwrChRiErrSwilPwrChRi8Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 651
        signal_description = "Right Zone Swil Power Channel 8 Error Status"
        signal_length = 8
        start_position = 447
        value_definition = {}

    class PwrChRiErrSwilPwrChRi5Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 651
        signal_description = "Right Zone Swil Power Channel 5 Error Status"
        signal_length = 8
        start_position = 455
        value_definition = {}

    class PwrChRiErrSwilPwrChRi11Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 651
        signal_description = "Right Zone Swil Power Channel 11 Error Status"
        signal_length = 8
        start_position = 463
        value_definition = {}

    class PwrChRiErrSwilPwrChRi23Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 651
        signal_description = "Right Zone Swil Power Channel 23 Error Status"
        signal_length = 8
        start_position = 471
        value_definition = {}

    class PwrChRiErrSwilPwrChRi26Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 651
        signal_description = "Right Zone Swil Power Channel 26 Error Status"
        signal_length = 8
        start_position = 479
        value_definition = {}

    class PwrChRiErrContnsPwrChRi3Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 651
        signal_description = "Right Zone Contns Power Channel 3 Error Status"
        signal_length = 8
        start_position = 487
        value_definition = {}

    class RdntBattIRaw:
        comments = ""
        factor = 0.015625
        initial_value = 32768
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -512
        sig_ub = 650
        signal_description = "Redundant battery current"
        signal_length = 16
        start_position = 495
        value_definition = {}

    class RdntBattLockLoadSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 649
        signal_description = "Redundant battery mode status"
        signal_length = 2
        start_position = 511
        value_definition = {'0x0': ' BattLockLoadSts_Idle', '0x1': ' BattLockLoadSts_UnLockLoad', '0x2': ' BattLockLoadSts_PreLockLoad', '0x3': ' BattLockLoadSts_LockLoad'}

    class RdntBattSOCRaw:
        comments = ""
        factor = 1.0
        initial_value = 100
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 648
        signal_description = "Redundant battery SOC"
        signal_length = 8
        start_position = 519
        value_definition = {'0xFF': 'BattSOH_Invalid'}

    class RdntBattSOCSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 663
        signal_description = "Redundant battery SOC accuracy status"
        signal_length = 2
        start_position = 527
        value_definition = {'0x0': ' LVBattCal_Idle', '0x1': ' LVBattCal_CmplCal', '0x2': ' LVBattCal_InCmplCal', '0x3': ' LVBattCal_Resvd'}

    class RdntBattTRaw:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = 662
        signal_description = "Redundant battery temperature"
        signal_length = 13
        start_position = 525
        value_definition = {}

    class RdntBattURaw:
        comments = ""
        factor = 0.02
        initial_value = 1023
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 661
        signal_description = "Redundant battery voltage"
        signal_length = 10
        start_position = 528
        value_definition = {'0x3FF': 'BattU2_BMSVolWakeUpThd'}

    class ReBlwrStsOverTemp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 660
        signal_description = "Compartment Rear Blower Over Temperature"
        signal_length = 1
        start_position = 550
        value_definition = {'0x0': ' MotOverTemp_Normal', '0x1': ' MotOverTemp_OverTemp'}

    class ReBlwrStsElecErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 660
        signal_description = "Compartment Rear Blower Electrical Error"
        signal_length = 2
        start_position = 549
        value_definition = {'0x0': ' ElecErr_Normal', '0x1': ' ElecErr_ShortToGroundOrOpenCircuit', '0x2': ' ElecErr_ShortToBatt', '0x3': ' ElecErr_Reserved'}

    class ReBlwrStsEgyLim:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 660
        signal_description = "Compartment Front Blower Energy Limit Status"
        signal_length = 1
        start_position = 547
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class ReBlwrStsOnOffSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 660
        signal_description = "Compartment Rear Blower OnOff Status"
        signal_length = 2
        start_position = 546
        value_definition = {'0x0': ' BlwrSts_OFF', '0x1': ' BlwrSts_ON', '0x2': ' BlwrSts_Err', '0x3': ' BlwrSts_Reserved'}

    class ReBlwrStsVoltErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 660
        signal_description = "Compartment Rear Blower Voltage Error"
        signal_length = 2
        start_position = 544
        value_definition = {'0x0': ' VoltErr_Normal', '0x1': ' VoltErr_UnderVolt', '0x2': ' VoltErr_OverVolt', '0x3': ' VoltErr_Reserved'}

    class ReBlwrStsActPWM:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 660
        signal_description = "Compartment Front Blower Actual PWM"
        signal_length = 10
        start_position = 558
        value_definition = {}

    class RecircRat:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 659
        signal_description = "Compartment Recirculation Ratio"
        signal_length = 10
        start_position = 564
        value_definition = {}

    class RefrigCircVlvCalStsFromRiREXVCalSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 658
        signal_description = "Valve Calibration Stauts"
        signal_length = 2
        start_position = 570
        value_definition = {'0x0': ' ExvCalibSts_NotInitialized', '0x1': ' ExvCalibSts_InitializationInProcess', '0x2': ' ExvCalibSts_Initialized', '0x3': ' ExvCalibSts_Reserved'}

    class RefrigCircVlvCalStsFromRiCERVCalSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 658
        signal_description = "Valve Calibration Stauts"
        signal_length = 2
        start_position = 568
        value_definition = {'0x0': ' ExvCalibSts_NotInitialized', '0x1': ' ExvCalibSts_InitializationInProcess', '0x2': ' ExvCalibSts_Initialized', '0x3': ' ExvCalibSts_Reserved'}

    class RefrigCircVlvCalStsFromRiFEXVCalSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 658
        signal_description = "Valve Calibration Stauts"
        signal_length = 2
        start_position = 582
        value_definition = {'0x0': ' ExvCalibSts_NotInitialized', '0x1': ' ExvCalibSts_InitializationInProcess', '0x2': ' ExvCalibSts_Initialized', '0x3': ' ExvCalibSts_Reserved'}

    class RefrigCircVlvCalStsFromRiBEXVCalSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 658
        signal_description = "Valve Calibration Stauts"
        signal_length = 2
        start_position = 580
        value_definition = {'0x0': ' ExvCalibSts_NotInitialized', '0x1': ' ExvCalibSts_InitializationInProcess', '0x2': ' ExvCalibSts_Initialized', '0x3': ' ExvCalibSts_Reserved'}

    class RefrigCircVlvCalStsFromRiTERVCalSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 658
        signal_description = "Valve Calibration Stauts"
        signal_length = 2
        start_position = 578
        value_definition = {'0x0': ' ExvCalibSts_NotInitialized', '0x1': ' ExvCalibSts_InitializationInProcess', '0x2': ' ExvCalibSts_Initialized', '0x3': ' ExvCalibSts_Reserved'}

    class RefrigCircVlvCalStsFromRiWERVCalSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 658
        signal_description = "Valve Calibration Stauts"
        signal_length = 2
        start_position = 576
        value_definition = {'0x0': ' ExvCalibSts_NotInitialized', '0x1': ' ExvCalibSts_InitializationInProcess', '0x2': ' ExvCalibSts_Initialized', '0x3': ' ExvCalibSts_Reserved'}

    class RefrigCircVlvStsFromRiRefrigSOV2Sts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 657
        signal_description = "Valve Stauts"
        signal_length = 3
        start_position = 590
        value_definition = {'0x0': ' ThermCooltVlvSts_Unknow', '0x1': ' ThermCooltVlvSts_Normal', '0x2': ' ThermCooltVlvSts_Err'}

    class RefrigCircVlvStsFromRiREXVSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 657
        signal_description = "Valve Stauts"
        signal_length = 3
        start_position = 587
        value_definition = {'0x0': ' ThermCooltVlvSts_Unknow', '0x1': ' ThermCooltVlvSts_Normal', '0x2': ' ThermCooltVlvSts_Err'}

    class RefrigCircVlvStsFromRiRefrigSOV1Sts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 657
        signal_description = "Valve Stauts"
        signal_length = 3
        start_position = 584
        value_definition = {'0x0': ' ThermCooltVlvSts_Unknow', '0x1': ' ThermCooltVlvSts_Normal', '0x2': ' ThermCooltVlvSts_Err'}

    class RefrigCircVlvStsFromRiWERVSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 657
        signal_description = "Valve Stauts"
        signal_length = 3
        start_position = 597
        value_definition = {'0x0': ' ThermCooltVlvSts_Unknow', '0x1': ' ThermCooltVlvSts_Normal', '0x2': ' ThermCooltVlvSts_Err'}

    class RefrigCircVlvStsFromRiFEXVSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 657
        signal_description = "Valve Stauts"
        signal_length = 3
        start_position = 594
        value_definition = {'0x0': ' ThermCooltVlvSts_Unknow', '0x1': ' ThermCooltVlvSts_Normal', '0x2': ' ThermCooltVlvSts_Err'}

    class RefrigCircVlvStsFromRiCERVSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 657
        signal_description = "Valve Stauts"
        signal_length = 3
        start_position = 607
        value_definition = {'0x0': ' ThermCooltVlvSts_Unknow', '0x1': ' ThermCooltVlvSts_Normal', '0x2': ' ThermCooltVlvSts_Err'}

    class RefrigCircVlvStsFromRiTERVSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 657
        signal_description = "Valve Stauts"
        signal_length = 3
        start_position = 604
        value_definition = {'0x0': ' ThermCooltVlvSts_Unknow', '0x1': ' ThermCooltVlvSts_Normal', '0x2': ' ThermCooltVlvSts_Err'}

    class RefrigCircVlvStsFromRiBEXVSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 657
        signal_description = "Valve Stauts"
        signal_length = 3
        start_position = 601
        value_definition = {'0x0': ' ThermCooltVlvSts_Unknow', '0x1': ' ThermCooltVlvSts_Normal', '0x2': ' ThermCooltVlvSts_Err'}

    class RefrigCircVlvStsFromRiRefrigSOV3Sts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 657
        signal_description = "Valve Stauts"
        signal_length = 3
        start_position = 614
        value_definition = {'0x0': ' ThermCooltVlvSts_Unknow', '0x1': ' ThermCooltVlvSts_Normal', '0x2': ' ThermCooltVlvSts_Err'}

    class RRChdLockErrFbLockFail:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 656
        signal_description = "lock fail"
        signal_length = 1
        start_position = 677
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class RRChdLockErrFbUnlockFail:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 656
        signal_description = "unlock fail"
        signal_length = 1
        start_position = 675
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class RRChdLockErrFbError1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 656
        signal_description = "error1"
        signal_length = 1
        start_position = 679
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class RRChdLockErrFbMotorOverTherm:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 656
        signal_description = "motor over Therm"
        signal_length = 1
        start_position = 676
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class RRChdLockErrFbError2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 656
        signal_description = "error2"
        signal_length = 1
        start_position = 678
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class RRDoorMaxPosnSetFb:
        comments = ""
        factor = 1.0
        initial_value = 101
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 671
        signal_description = "Maximum percentage feedback that power side doors can open"
        signal_length = 8
        start_position = 623
        value_definition = {}

    class RRDoorModSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 670
        signal_description = "power side door mode status"
        signal_length = 2
        start_position = 631
        value_definition = {'0x0': ' DoorModSts_ElecMode', '0x1': ' DoorModSts_ManualMode'}

    class RRPwrDoorErrFbRollAngErrFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 669
        signal_description = "roll angle error"
        signal_length = 1
        start_position = 629
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class RRPwrDoorErrFbBoolean:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 669
        signal_description = "error status"
        signal_length = 1
        start_position = 628
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class RRPwrDoorErrFbPosnUnknowFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 669
        signal_description = "door position lost"
        signal_length = 1
        start_position = 627
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class RRPwrDoorErrFbHallErrFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 669
        signal_description = "hall error"
        signal_length = 1
        start_position = 626
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class RRPwrDoorErrFbMotThermErrFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 669
        signal_description = "Motor overheating"
        signal_length = 1
        start_position = 625
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class CmptmtAirFlwEstimdFrnt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 212
        signal_description = "Estimated Air Mass Flow Of Compartment Front Blower "
        signal_length = 10
        start_position = 28
        value_definition = {}

    class CmptmtAirFlwEstimdRe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 212
        signal_description = "Estimated Air Mass Flow Of Compartment Rear Blower "
        signal_length = 10
        start_position = 34
        value_definition = {}

    class IncarTFrntEstimdFanRunng:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 653
        signal_description = "Fan For Front Incar Temperature Running Status"
        signal_length = 1
        start_position = 165
        value_definition = {'0x0': ' Flg1_Rst', '0x1': ' Flg1_Set'}

    class IncarTFrntEstimdTQf:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 653
        signal_description = "Front Incar Temperature Quality Flag "
        signal_length = 2
        start_position = 164
        value_definition = {'0x0': ' IncarTQf_SnsrDataUndefd', '0x1': ' IncarTQf_FanNotRunning', '0x2': ' IncarTQf_SnsrDataNotOk', '0x3': ' IncarTQf_SnsrDataOk'}

    class IncarTFrntEstimdT:
        comments = ""
        factor = 0.1
        initial_value = 600
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -60
        sig_ub = 653
        signal_description = "Front Incar Temperature"
        signal_length = 11
        start_position = 162
        value_definition = {}

    class TrunkLiDrvReqLiPerc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 668
        signal_description = "brightness percent"
        signal_length = 7
        start_position = 647
        value_definition = {}

    class TrunkLiDrvReqLightCmd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 668
        signal_description = "light command"
        signal_length = 4
        start_position = 639
        value_definition = {'0x0': ' LightCmd_NoReq', '0x1': ' LightCmd_ON', '0x2': ' LightCmd_OFF', '0x3': ' LightCmd_TBD'}

    class TrunkLiDrvReqReadingLiDimsSpdCmd:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 668
        signal_description = "required dim speed"
        signal_length = 3
        start_position = 635
        value_definition = {'0x0': ' ReadingLiDimsSpdCmd_NoCmd', '0x1': ' ReadingLiDimsSpdCmd_400ms', '0x2': ' ReadingLiDimsSpdCmd_800ms', '0x3': ' ReadingLiDimsSpdCmd_1000ms', '0x4': ' ReadingLiDimsSpdCmd_2000ms', '0x5': ' ReadingLiDimsSpdCmd_Resverd'}


class LCURMulticastEthSignalIPdu02:
    base_type = "Boolean"
    client_socket = "SocketMulticast"
    pdu_header_id = 0x60FF02
    pdu_length_bytes = 11
    receiver = ['CCUMCUCD', 'CCUSOCCD', 'LCUL']
    send_type = "Cyclic-160ms"
    sender = "LCUR"
    server_socket = "SocketLcuRSoAdUDP"
    signal_group = {'CooltCircVlvSts': ['CooltCircVlvStsLCTVSts', 'CooltCircVlvStsLCTVSts', 'CooltCircVlvStsBCTVSts', 'CooltCircVlvStsBCTVSts', 'CooltCircVlvStsCCTVsts', 'CooltCircVlvStsCCTVsts', 'CooltCircVlvStsCooltSOV1Sts', 'CooltCircVlvStsCooltSOV1Sts', 'CooltCircVlvStsECTVSts', 'CooltCircVlvStsECTVSts', 'CooltCircVlvStsDCTVSts', 'CooltCircVlvStsDCTVSts', 'CooltCircVlvStsHCTVSts', 'CooltCircVlvStsHCTVSts', 'CooltCircVlvStsBCFVSts', 'CooltCircVlvStsBCFVSts', 'CooltCircVlvStsWCTVSts', 'CooltCircVlvStsWCTVSts'], 'HVHeatrCmptPwrCns': ['HVHeatrCmptPwrCnsHVCooltHeatrPwrCns', 'HVHeatrCmptPwrCnsHVCooltHeatrPwrCns', 'HVHeatrCmptPwrCnsHVAirHeatrPwrCns', 'HVHeatrCmptPwrCnsHVAirHeatrPwrCns'], 'HVHeatrCmptStsFromRi': ['HVHeatrCmptStsFromRiAirHeatrSts', 'HVHeatrCmptStsFromRiAirHeatrSts', 'HVHeatrCmptStsFromRiCooltHeatrSts', 'HVHeatrCmptStsFromRiCooltHeatrSts']}

    class CooltCircVlvStsLCTVSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 10
        signal_description = "LCTV Status"
        signal_length = 3
        start_position = 31
        value_definition = {'0x0': ' ThermCooltVlvSts_Unknow', '0x1': ' ThermCooltVlvSts_Normal', '0x2': ' ThermCooltVlvSts_Err'}

    class CooltCircVlvStsBCTVSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 10
        signal_description = "BCTV Status"
        signal_length = 3
        start_position = 28
        value_definition = {'0x0': ' ThermCooltVlvSts_Unknow', '0x1': ' ThermCooltVlvSts_Normal', '0x2': ' ThermCooltVlvSts_Err'}

    class CooltCircVlvStsCCTVsts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 10
        signal_description = "CCTV Status"
        signal_length = 3
        start_position = 25
        value_definition = {'0x0': ' ThermCooltVlvSts_Unknow', '0x1': ' ThermCooltVlvSts_Normal', '0x2': ' ThermCooltVlvSts_Err'}

    class CooltCircVlvStsCooltSOV1Sts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 10
        signal_description = "Coolant Solenoid Valve 1 Status"
        signal_length = 3
        start_position = 38
        value_definition = {'0x0': ' ThermCooltVlvSts_Unknow', '0x1': ' ThermCooltVlvSts_Normal', '0x2': ' ThermCooltVlvSts_Err'}

    class CooltCircVlvStsECTVSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 10
        signal_description = "ECTV Status"
        signal_length = 3
        start_position = 35
        value_definition = {'0x0': ' ThermCooltVlvSts_Unknow', '0x1': ' ThermCooltVlvSts_Normal', '0x2': ' ThermCooltVlvSts_Err'}

    class CooltCircVlvStsDCTVSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 10
        signal_description = "DCTV Status"
        signal_length = 3
        start_position = 32
        value_definition = {'0x0': ' ThermCooltVlvSts_Unknow', '0x1': ' ThermCooltVlvSts_Normal', '0x2': ' ThermCooltVlvSts_Err'}

    class CooltCircVlvStsHCTVSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 10
        signal_description = "HCTV Status"
        signal_length = 3
        start_position = 45
        value_definition = {'0x0': ' ThermCooltVlvSts_Unknow', '0x1': ' ThermCooltVlvSts_Normal', '0x2': ' ThermCooltVlvSts_Err'}

    class CooltCircVlvStsBCFVSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 10
        signal_description = "BCFV Status"
        signal_length = 3
        start_position = 42
        value_definition = {'0x0': ' ThermCooltVlvSts_Unknow', '0x1': ' ThermCooltVlvSts_Normal', '0x2': ' ThermCooltVlvSts_Err'}

    class CooltCircVlvStsWCTVSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 10
        signal_description = "WCTV Status"
        signal_length = 3
        start_position = 55
        value_definition = {'0x0': ' ThermCooltVlvSts_Unknow', '0x1': ' ThermCooltVlvSts_Normal', '0x2': ' ThermCooltVlvSts_Err'}

    class HVHeatrCmptPwrCnsHVCooltHeatrPwrCns:
        comments = ""
        factor = 10.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 82
        signal_description = "HVCH Power Consumption"
        signal_length = 13
        start_position = 49
        value_definition = {}

    class HVHeatrCmptPwrCnsHVAirHeatrPwrCns:
        comments = ""
        factor = 10.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 82
        signal_description = "HVAH Power Consumption"
        signal_length = 13
        start_position = 68
        value_definition = {}

    class HVHeatrCmptStsFromRiAirHeatrSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 81
        signal_description = "HVAH Status"
        signal_length = 2
        start_position = 87
        value_definition = {'0x0': ' Err_Initial', '0x1': ' Err_NoError', '0x2': ' Err_Error', '0x3': ' Err_Reserve'}

    class HVHeatrCmptStsFromRiCooltHeatrSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 81
        signal_description = "HVCH Status"
        signal_length = 2
        start_position = 85
        value_definition = {'0x0': ' Err_Initial', '0x1': ' Err_NoError', '0x2': ' Err_Error', '0x3': ' Err_Reserve'}

    class CmprReqCmprPwrLim:
        comments = ""
        factor = 40.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 13
        signal_description = "Maximum allowed compressor power."
        signal_length = 8
        start_position = 7
        value_definition = {}

    class CmprReqCmprRunReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 12
        signal_description = "Ac compressor run request."
        signal_length = 2
        start_position = 15
        value_definition = {'0x0': ' CmprRunReq_CmprOff', '0x1': ' CmprRunReq_CmprOn', '0x2': ' CmprRunReq_Resd', '0x3': ' CmprRunReq_SigNotAvl'}

    class CmprReqCmprSpdReq:
        comments = ""
        factor = 50.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 11
        signal_description = "AC compressor rotational speed request."
        signal_length = 8
        start_position = 23
        value_definition = {}

    class CooltSov1ActvReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 9
        signal_description = "Coolant Solenoid Valve 1 Active Request"
        signal_length = 1
        start_position = 52
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class HVAirHeatrEna:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 8
        signal_description = "HVAH enable signal sent by thermal management."
        signal_length = 1
        start_position = 51
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class HvCooltHeatrEnad:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 83
        signal_description = "HVCH enable signal sent by thermal management."
        signal_length = 1
        start_position = 50
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}


class LCURMulticastEthSignalIPdu03:
    base_type = "Unsigned"
    client_socket = "SocketMulticast"
    pdu_header_id = 0x60FF03
    pdu_length_bytes = 3
    receiver = ['CCUMCUCD', 'CCUSOCCD']
    send_type = "Cyclic-200ms"
    sender = "LCUR"
    server_socket = "SocketLcuRSoAdUDP"
    signal_group = {}

    class PassSeatOccpSnsrRawSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 11
        signal_description = "Passanger Seat Occupy Sensor Raw Status"
        signal_length = 4
        start_position = 7
        value_definition = {'0x0': ' OccptSnsrOutpSts_Empty', '0x1': ' OccptSnsrOutpSts_L1', '0x2': ' OccptSnsrOutpSts_L2', '0x3': ' OccptSnsrOutpSts_L3', '0x4': ' OccptSnsrOutpSts_L4', '0x5': ' OccptSnsrOutpSts_Occupied', '0x6': ' OccptSnsrOutpSts_Unknown'}

    class SecRowRiOccpSnsrRawSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 10
        signal_description = "SecondRow Right Occupy Sensor Raw Status"
        signal_length = 4
        start_position = 3
        value_definition = {'0x0': ' OccptSnsrOutpSts_Empty', '0x1': ' OccptSnsrOutpSts_L1', '0x2': ' OccptSnsrOutpSts_L2', '0x3': ' OccptSnsrOutpSts_L3', '0x4': ' OccptSnsrOutpSts_L4', '0x5': ' OccptSnsrOutpSts_Occupied', '0x6': ' OccptSnsrOutpSts_Unknown'}

    class ThrdRowRiOccpSnsrRawSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 9
        signal_description = "Third Row Right Occupy Sensor Raw Status"
        signal_length = 4
        start_position = 15
        value_definition = {'0x0': ' OccptSnsrOutpSts_Empty', '0x1': ' OccptSnsrOutpSts_L1', '0x2': ' OccptSnsrOutpSts_L2', '0x3': ' OccptSnsrOutpSts_L3', '0x4': ' OccptSnsrOutpSts_L4', '0x5': ' OccptSnsrOutpSts_Occupied', '0x6': ' OccptSnsrOutpSts_Unknown'}

    class ThrdRowRiOccpSnsrOKSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 18
        signal_description = "Third Row Right Occupy Sensor OK Status"
        signal_length = 1
        start_position = 19
        value_definition = {'0x0': ' OkNotOk1_Ok', '0x1': ' OkNotOk1_NotOk'}

    class SecRowRiOccpSnsrOKSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 20
        signal_description = "SecondRow Middle Occupy Sensor OK Status"
        signal_length = 1
        start_position = 21
        value_definition = {'0x0': ' OkNotOk1_Ok', '0x1': ' OkNotOk1_NotOk'}

    class PassSeatOccpSnsrOKSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 22
        signal_description = "Passanger Seat Occupy Sensor OK Status"
        signal_length = 1
        start_position = 23
        value_definition = {'0x0': ' OkNotOk1_Ok', '0x1': ' OkNotOk1_NotOk'}


class LCURMulticastEthSignalIPdu05:
    base_type = "Unsigned"
    client_socket = "SocketMulticast"
    pdu_header_id = 0x60FF05
    pdu_length_bytes = 3
    receiver = ['CCUSOCCD', 'LCUL']
    send_type = "Cyclic-30ms"
    sender = "LCUR"
    server_socket = "SocketLcuRSoAdUDP"
    signal_group = {'FuncStsOfPositionLamp': ['FuncStsOfPositionLampLightPriority', 'FuncStsOfPositionLampLightPriority', 'FuncStsOfPositionLampLightSts', 'FuncStsOfPositionLampLightSts', 'FuncStsOfPositionLampLightErrorCode', 'FuncStsOfPositionLampLightErrorCode']}

    class FuncStsOfPositionLampLightPriority:
        comments = ""
        factor = 1.0
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 19
        signal_description = "LightPriority"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class FuncStsOfPositionLampLightSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 19
        signal_description = "LightStatus"
        signal_length = 4
        start_position = 23
        value_definition = {'0x0': ' LightSts_Off', '0x1': ' LightSts_On', '0x2': ' LightSts_Error', '0x3': ' LightSts_Reserved'}

    class FuncStsOfPositionLampLightErrorCode:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 19
        signal_description = "ErrorCode"
        signal_length = 8
        start_position = 7
        value_definition = {'0x0': ' LightErrorCode_ChipError', '0x1': ' LightErrorCode_ShortError', '0x2': ' LightErrorCode_OpenError', '0xFF': ' LightErrorCode_NoneError'}
