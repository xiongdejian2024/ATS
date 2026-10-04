

class LCULMulticastEthSignalIPdu05:
    base_type = "Unsigned"
    client_socket = "SocketMulticast"
    pdu_header_id = 0x50FF05
    pdu_length_bytes = 24
    receiver = ['CCUMCUAD', 'CCUMCUCD', 'CCUSOCCD', 'LCUR']
    send_type = "Cyclic-50ms"
    sender = "LCUL"
    server_socket = "SocketLcuLSoAdUDP"
    signal_group = {'FuncStsOfStopLamp': ['FuncStsOfStopLampLightSts', 'FuncStsOfStopLampLightSts', 'FuncStsOfStopLampLightErrorCode', 'FuncStsOfStopLampLightErrorCode', 'FuncStsOfStopLampLightPriority', 'FuncStsOfStopLampLightPriority'], 'ChargeLidAntiPnchSts': ['ChargeLidAntiPnchStsCloseAntiPnchSts', 'ChargeLidAntiPnchStsCloseAntiPnchSts', 'ChargeLidAntiPnchStsOPenAntiPnchSts', 'ChargeLidAntiPnchStsOPenAntiPnchSts'], 'FLDoorAntiPnchFb': ['FLDoorAntiPnchFbOPenAntiPnchSts', 'FLDoorAntiPnchFbOPenAntiPnchSts', 'FLDoorAntiPnchFbCloseAntiPnchSts', 'FLDoorAntiPnchFbCloseAntiPnchSts'], 'FLDoorPosnSts': ['FLDoorPosnStsDoorAngPosn', 'FLDoorPosnStsDoorAngPosn', 'FLDoorPosnStsDoorPercPosn', 'FLDoorPosnStsDoorPercPosn'], 'RLPwrDoorMotPrm': ['RLPwrDoorMotPrmPwrDoorStsFb', 'RLPwrDoorMotPrmStopEvnt'], 'FLPwrDoorMotPrm': ['FLPwrDoorMotPrmPwrDoorStsFb', 'FLPwrDoorMotPrmStopEvnt'], 'RLDoorAntiPnchFb': ['RLDoorAntiPnchFbCloseAntiPnchSts', 'RLDoorAntiPnchFbCloseAntiPnchSts', 'RLDoorAntiPnchFbOPenAntiPnchSts', 'RLDoorAntiPnchFbOPenAntiPnchSts'], 'RLDoorPosnSts': ['RLDoorPosnStsDoorAngPosn', 'RLDoorPosnStsDoorAngPosn', 'RLDoorPosnStsDoorPercPosn', 'RLDoorPosnStsDoorPercPosn']}

    class FLDoorOutdSwtSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 135
        signal_description = "Switch status of Outside door"
        signal_length = 3
        start_position = 10
        value_definition = {'0x0': ' SwtSts_IniVal', '0x1': ' SwtSts_Pressd', '0x2': ' SwtSts_NotPressd', '0x3': ' SwtSts_SWStuck', '0x4': ' SwtSts_Error'}

    class FuncStsOfStopLampLightSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 131
        signal_description = "LightSts"
        signal_length = 4
        start_position = 51
        value_definition = {'0x0': ' LightSts_Off', '0x1': ' LightSts_On', '0x2': ' LightSts_Error', '0x3': ' LightSts_Reserved'}

    class FuncStsOfStopLampLightErrorCode:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 131
        signal_description = "ErrorCode"
        signal_length = 8
        start_position = 63
        value_definition = {'0x0': ' LightErrorCode_ChipError', '0x1': ' LightErrorCode_ShortError', '0x2': ' LightErrorCode_OpenError', '0xFF': ' LightErrorCode_NoneError'}

    class FuncStsOfStopLampLightPriority:
        comments = ""
        factor = 1.0
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 131
        signal_description = "LightPriority"
        signal_length = 8
        start_position = 71
        value_definition = {}

    class RLDoorOutdSwtSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 138
        signal_description = "Switch status of Outside door"
        signal_length = 3
        start_position = 84
        value_definition = {'0x0': ' SwtSts_IniVal', '0x1': ' SwtSts_Pressd', '0x2': ' SwtSts_NotPressd', '0x3': ' SwtSts_SWStuck', '0x4': ' SwtSts_Error'}

    class ExtrReViewMirrFoldStsDrvr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 147
        signal_description = "the folding status of external rear view mirror at driver"
        signal_length = 3
        start_position = 150
        value_definition = {'0x0': ' MirrFoldSts_MirrPosnIdle', '0x1': ' MirrFoldSts_MirrUnFoldPosn', '0x2': ' MirrFoldSts_MirrFoldPosn', '0x3': ' MirrFoldSts_MirrMovgToUnFold', '0x4': ' MirrFoldSts_MirrMovgToFold', '0x5': ' MirrFoldSts_MirrPosnUndefd'}

    class ChargeLidAntiPnchStsCloseAntiPnchSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 19
        signal_description = "chargelid close direction AntiPnch status"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class ChargeLidAntiPnchStsOPenAntiPnchSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 19
        signal_description = "chargelid open direction AntiPnch status"
        signal_length = 1
        start_position = 6
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class ChargeLidMoveSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 18
        signal_description = "charge lid move status"
        signal_length = 3
        start_position = 5
        value_definition = {'0x0': ' ChargeLidMtnSts_IniVal', '0x1': ' ChargeLidMtnSts_Moving', '0x2': ' ChargeLidMtnSts_Close', '0x3': ' ChargeLidMtnSts_Open', '0x4': ' ChargeLidMtnSts_Unknow'}

    class ChrgLidOutdSwtSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 17
        signal_description = "outside Switch status of chargelid"
        signal_length = 3
        start_position = 2
        value_definition = {'0x0': ' SwtSts_IniVal', '0x1': ' SwtSts_Pressd', '0x2': ' SwtSts_NotPressd', '0x3': ' SwtSts_SWStuck', '0x4': ' SwtSts_Error'}

    class FLDoorAntiPnchFbOPenAntiPnchSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 16
        signal_description = "power side door open direction AntiPnch status"
        signal_length = 1
        start_position = 15
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class FLDoorAntiPnchFbCloseAntiPnchSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 16
        signal_description = "power side door close direction AntiPnch status"
        signal_length = 1
        start_position = 14
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class FLDoorInsdSwtSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 31
        signal_description = "Switch status of inside door"
        signal_length = 3
        start_position = 13
        value_definition = {'0x0': ' SwtSts_IniVal', '0x1': ' SwtSts_Pressd', '0x2': ' SwtSts_NotPressd', '0x3': ' SwtSts_SWStuck', '0x4': ' SwtSts_Error'}

    class FLDoorMtnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 111
        signal_description = "Power side door motion status"
        signal_length = 4
        start_position = 23
        value_definition = {'0x0': ' DoorMtnSts_IniVal', '0x1': ' DoorMtnSts_FullOpen', '0x2': ' DoorMtnSts_FullClose', '0x3': ' DoorMtnSts_StopDurOpen', '0x4': ' DoorMtnSts_StopDurClose', '0x5': ' DoorMtnSts_MovingOut', '0x6': ' DoorMtnSts_MovingIn', '0x7': ' DoorMtnSts_HalfClose', '0x8': ' DoorMtnSts_Unknow', '0x9': ' DoorMtnSts_OnlyOpenPosn'}

    class FLDoorPosnStsDoorAngPosn:
        comments = ""
        factor = 1.0
        initial_value = 101
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 134
        signal_description = "power side door Opening angle"
        signal_length = 7
        start_position = 30
        value_definition = {}

    class FLDoorPosnStsDoorPercPosn:
        comments = ""
        factor = 1.0
        initial_value = 101
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 134
        signal_description = "power side door Opening percentage"
        signal_length = 8
        start_position = 39
        value_definition = {}

    class FLDoorSpd:
        comments = ""
        factor = 0.5
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 133
        signal_description = "Speed of power side door"
        signal_length = 8
        start_position = 47
        value_definition = {}

    class LeftElecPealAntiPnchFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 130
        signal_description = "Electric pedal AntiPnch status"
        signal_length = 1
        start_position = 79
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class LeftElecPealSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 129
        signal_description = "Electric pedal status"
        signal_length = 2
        start_position = 78
        value_definition = {'0x0': ' DoorSts_Unknow', '0x1': ' DoorSts_Open', '0x2': ' DoorSts_Close'}

    class RightElecPealAntiPnchFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 128
        signal_description = "Electric pedal AntiPnch status"
        signal_length = 1
        start_position = 76
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class RightElecPealSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 143
        signal_description = "Electric pedal status"
        signal_length = 2
        start_position = 75
        value_definition = {'0x0': ' DoorSts_Unknow', '0x1': ' DoorSts_Open', '0x2': ' DoorSts_Close'}

    class RLChdLockSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 142
        signal_description = "children lock status"
        signal_length = 2
        start_position = 73
        value_definition = {'0x0': ' DoorLockSts_Unknow', '0x1': ' DoorLockSts_Lock', '0x2': ' DoorLockSts_Unlock'}

    class RLDoorInsdSwtSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 140
        signal_description = "Switch status of inside door"
        signal_length = 3
        start_position = 87
        value_definition = {'0x0': ' SwtSts_IniVal', '0x1': ' SwtSts_Pressd', '0x2': ' SwtSts_NotPressd', '0x3': ' SwtSts_SWStuck', '0x4': ' SwtSts_Error'}

    class RLPwrDoorMotPrmPwrDoorStsFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 151
        signal_description = "Power side door motor status"
        signal_length = 4
        start_position = 103
        value_definition = {'0x0': ' PwrDoorStsFb_DoorStUndef', '0x1': ' PwrDoorStsFb_DoorStWait', '0x2': ' PwrDoorStsFb_DoorStOpen', '0x3': ' PwrDoorStsFb_DoorStClose', '0x4': ' PwrDoorStsFb_DoorStRollBack', '0x5': ' PwrDoorStsFb_DoorSecondOpen', '0x6': ' PwrDoorStsFb_DoorTipToRun'}

    class RLPwrDoorMotPrmStopEvnt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 151
        signal_description = "stop reason of motor "
        signal_length = 4
        start_position = 99
        value_definition = {'0x0': ' StopEvnt_NONE', '0x1': ' StopEvnt_BRAKE', '0x2': ' StopEvnt_KEY', '0x3': ' StopEvnt_VEHSPEED', '0x4': ' StopEvnt_RADAR', '0x5': ' StopEvnt_SLOWDOWN', '0x6': ' StopEvnt_ITINERARYL', '0x7': ' StopEvnt_TIMEOut', '0x8': ' StopEvnt_LATCH', '0x9': ' StopEvnt_OCP', '0xA': ' StopEvnt_ANTIPINCH', '0xB': ' StopEvnt_NOPLAYING', '0xC': ' StopEvnt_HALL', '0xD': ' StopEvnt_NORMAL', '0xE': ' StopEvnt_HAND', '0xF': ' StopEvnt_ERROR'}

    class FLPwrDoorMotPrmPwrDoorStsFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 132
        signal_description = "Power side door motor status"
        signal_length = 4
        start_position = 95
        value_definition = {'0x0': ' PwrDoorStsFb_DoorStUndef', '0x1': ' PwrDoorStsFb_DoorStWait', '0x2': ' PwrDoorStsFb_DoorStOpen', '0x3': ' PwrDoorStsFb_DoorStClose', '0x4': ' PwrDoorStsFb_DoorStRollBack', '0x5': ' PwrDoorStsFb_DoorSecondOpen', '0x6': ' PwrDoorStsFb_DoorTipToRun'}

    class FLPwrDoorMotPrmStopEvnt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 132
        signal_description = "stop reason of motor "
        signal_length = 4
        start_position = 91
        value_definition = {'0x0': ' StopEvnt_NONE', '0x1': ' StopEvnt_BRAKE', '0x2': ' StopEvnt_KEY', '0x3': ' StopEvnt_VEHSPEED', '0x4': ' StopEvnt_RADAR', '0x5': ' StopEvnt_SLOWDOWN', '0x6': ' StopEvnt_ITINERARYL', '0x7': ' StopEvnt_TIMEOut', '0x8': ' StopEvnt_LATCH', '0x9': ' StopEvnt_OCP', '0xA': ' StopEvnt_ANTIPINCH', '0xB': ' StopEvnt_NOPLAYING', '0xC': ' StopEvnt_HALL', '0xD': ' StopEvnt_NORMAL', '0xE': ' StopEvnt_HAND', '0xF': ' StopEvnt_ERROR'}

    class RLDoorAntiPnchFbCloseAntiPnchSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 141
        signal_description = "power side door close direction AntiPnch status"
        signal_length = 1
        start_position = 81
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class RLDoorAntiPnchFbOPenAntiPnchSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 141
        signal_description = "power side door open direction AntiPnch status"
        signal_length = 1
        start_position = 80
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class RLDoorMtnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 139
        signal_description = "Power side door motion status"
        signal_length = 4
        start_position = 55
        value_definition = {'0x0': ' DoorMtnSts_IniVal', '0x1': ' DoorMtnSts_FullOpen', '0x2': ' DoorMtnSts_FullClose', '0x3': ' DoorMtnSts_StopDurOpen', '0x4': ' DoorMtnSts_StopDurClose', '0x5': ' DoorMtnSts_MovingOut', '0x6': ' DoorMtnSts_MovingIn', '0x7': ' DoorMtnSts_HalfClose', '0x8': ' DoorMtnSts_Unknow', '0x9': ' DoorMtnSts_OnlyOpenPosn'}

    class RLDoorSpd:
        comments = ""
        factor = 0.5
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 136
        signal_description = "Speed of power side door"
        signal_length = 8
        start_position = 127
        value_definition = {}

    class RLDoorPosnStsDoorAngPosn:
        comments = ""
        factor = 1.0
        initial_value = 101
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 137
        signal_description = "power side door Opening angle"
        signal_length = 7
        start_position = 110
        value_definition = {}

    class RLDoorPosnStsDoorPercPosn:
        comments = ""
        factor = 1.0
        initial_value = 101
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 137
        signal_description = "door percentage position"
        signal_length = 8
        start_position = 119
        value_definition = {}

    class IntrReViewMirrDimPerc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 152
        signal_description = "内后视镜防眩目驱动百分比"
        signal_length = 7
        start_position = 159
        value_definition = {}


class LCULMulticastEthSignalIPdu03:
    base_type = "Unsigned"
    client_socket = "SocketMulticast"
    pdu_header_id = 0x50FF03
    pdu_length_bytes = 11
    receiver = ['CCUMCUAD', 'CCUMCUCD', 'LCUR', 'CCUSOCCD']
    send_type = "Cyclic-20ms"
    sender = "LCUL"
    server_socket = "SocketLcuLSoAdUDP"
    signal_group = {'BrkPedlInfoSec': ['BrkPedlInfoSecChks', 'BrkPedlInfoSecChks', 'BrkPedlInfoSecPsd', 'BrkPedlInfoSecPsd', 'BrkPedlInfoSecCntr', 'BrkPedlInfoSecCntr', 'BrkPedlInfoSecQf', 'BrkPedlInfoSecQf'], 'DrvReqOfTurnLamp': ['DrvReqOfTurnLampDrvReqOfTurnLamp', 'DrvReqOfTurnLampDrvReqOfTurnLamp', 'DrvReqOfTurnLampChks', 'DrvReqOfTurnLampChks', 'DrvReqOfTurnLampCntr', 'DrvReqOfTurnLampCntr'], 'FuncStsOfTurnLamp': ['FuncStsOfTurnLampDisplayOfTurnLamp', 'FuncStsOfTurnLampDisplayOfTurnLamp', 'FuncStsOfTurnLampRiTurnLampLightSts', 'FuncStsOfTurnLampRiTurnLampLightSts', 'FuncStsOfTurnLampLeTurnLampLightSts', 'FuncStsOfTurnLampLeTurnLampLightSts', 'FuncStsOfTurnLampLightErrorCode', 'FuncStsOfTurnLampLightErrorCode', 'FuncStsOfTurnLampModeStsOfTurnLamp', 'FuncStsOfTurnLampModeStsOfTurnLamp', 'FuncStsOfTurnLampLightPriority', 'FuncStsOfTurnLampLightPriority'], 'WinDrvrBtnSts': ['WinDrvrBtnStsWinBtnFL', 'WinDrvrBtnStsWinBtnFL', 'WinDrvrBtnStsWinBtnFR', 'WinDrvrBtnStsWinBtnFR', 'WinDrvrBtnStsWinBtnRR', 'WinDrvrBtnStsWinBtnRR', 'WinDrvrBtnStsWinBtnRL', 'WinDrvrBtnStsWinBtnRL']}

    class FLDoorOpenClsSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 24
        signal_description = "Door Status/latch status"
        signal_length = 2
        start_position = 71
        value_definition = {'0x0': ' DoorSts_Unknow', '0x1': ' DoorSts_Open', '0x2': ' DoorSts_Close'}

    class RLDoorOpenClsSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 58
        signal_description = "Door Status/latch status"
        signal_length = 2
        start_position = 79
        value_definition = {'0x0': ' DoorSts_Unknow', '0x1': ' DoorSts_Open', '0x2': ' DoorSts_Close'}

    class BrkPedlInfoSecChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 8
        signal_description = "crc"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class BrkPedlInfoSecPsd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 8
        signal_description = "backup brak pedal pressed information"
        signal_length = 1
        start_position = 11
        value_definition = {'0x0': ' NoYes1_No', '0x1': ' NoYes1_Yes'}

    class BrkPedlInfoSecCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 8
        signal_description = "counter"
        signal_length = 4
        start_position = 15
        value_definition = {}

    class BrkPedlInfoSecQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 8
        signal_description = "quality factor"
        signal_length = 2
        start_position = 10
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class DrvReqOfTurnLampDrvReqOfTurnLamp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 25
        signal_description = "Lightdrivecmd"
        signal_length = 2
        start_position = 27
        value_definition = {'0x0': ' DrvReqOfTurnLamp_OFF', '0x1': ' DrvReqOfTurnLamp_Left', '0x2': ' DrvReqOfTurnLamp_Right', '0x3': ' DrvReqOfTurnLamp_HWL'}

    class DrvReqOfTurnLampChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 25
        signal_description = "checksum"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class DrvReqOfTurnLampCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 25
        signal_description = "Counter"
        signal_length = 4
        start_position = 31
        value_definition = {}

    class FuncStsOfTurnLampDisplayOfTurnLamp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 59
        signal_description = "TL Status for HMI"
        signal_length = 2
        start_position = 61
        value_definition = {'0x0': ' ModeStsOfTurnLamp_OFF', '0x1': ' ModeStsOfTurnLamp_Left', '0x2': ' ModeStsOfTurnLamp_Right', '0x3': ' ModeStsOfTurnLamp_HWL'}

    class FuncStsOfTurnLampRiTurnLampLightSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 59
        signal_description = "Right Turn Lamp Status"
        signal_length = 4
        start_position = 47
        value_definition = {'0x0': ' LightSts_Off', '0x1': ' LightSts_On', '0x2': ' LightSts_Error', '0x3': ' LightSts_Reserved'}

    class FuncStsOfTurnLampLeTurnLampLightSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 59
        signal_description = "Left Turn Lamp Status"
        signal_length = 4
        start_position = 43
        value_definition = {'0x0': ' LightSts_Off', '0x1': ' LightSts_On', '0x2': ' LightSts_Error', '0x3': ' LightSts_Reserved'}

    class FuncStsOfTurnLampLightErrorCode:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 59
        signal_description = "ErrorCode"
        signal_length = 8
        start_position = 55
        value_definition = {'0x0': ' LightErrorCode_ChipError', '0x1': ' LightErrorCode_ShortError', '0x2': ' LightErrorCode_OpenError', '0xFF': ' LightErrorCode_NoneError'}

    class FuncStsOfTurnLampModeStsOfTurnLamp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 59
        signal_description = "LightSts"
        signal_length = 2
        start_position = 63
        value_definition = {'0x0': ' ModeStsOfTurnLamp_OFF', '0x1': ' ModeStsOfTurnLamp_Left', '0x2': ' ModeStsOfTurnLamp_Right', '0x3': ' ModeStsOfTurnLamp_HWL'}

    class FuncStsOfTurnLampLightPriority:
        comments = ""
        factor = 1.0
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 59
        signal_description = "LightPriority"
        signal_length = 8
        start_position = 39
        value_definition = {}

    class WinDrvrBtnStsWinBtnFL:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 57
        signal_description = "frontLeft Window Switch"
        signal_length = 3
        start_position = 77
        value_definition = {'0x0': ' WinBtnReq_Idle', '0x1': ' WinBtnReq_Up1', '0x2': ' WinBtnReq_Up2', '0x3': ' WinBtnReq_Dwn1', '0x4': ' WinBtnReq_Dwn2', '0x5': ' WinBtnReq_Undef', '0x6': ' WinBtnReq_Reserved1', '0x7': ' WinBtnReq_Reserved2'}

    class WinDrvrBtnStsWinBtnFR:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 57
        signal_description = "frontRight Window Switch"
        signal_length = 3
        start_position = 74
        value_definition = {'0x0': ' WinBtnReq_Idle', '0x1': ' WinBtnReq_Up1', '0x2': ' WinBtnReq_Up2', '0x3': ' WinBtnReq_Dwn1', '0x4': ' WinBtnReq_Dwn2', '0x5': ' WinBtnReq_Undef', '0x6': ' WinBtnReq_Reserved1', '0x7': ' WinBtnReq_Reserved2'}

    class WinDrvrBtnStsWinBtnRR:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 57
        signal_description = "RearRight Window Switch"
        signal_length = 3
        start_position = 86
        value_definition = {'0x0': ' WinBtnReq_Idle', '0x1': ' WinBtnReq_Up1', '0x2': ' WinBtnReq_Up2', '0x3': ' WinBtnReq_Dwn1', '0x4': ' WinBtnReq_Dwn2', '0x5': ' WinBtnReq_Undef', '0x6': ' WinBtnReq_Reserved1', '0x7': ' WinBtnReq_Reserved2'}

    class WinDrvrBtnStsWinBtnRL:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 57
        signal_description = "RearLeft Window Switch"
        signal_length = 3
        start_position = 83
        value_definition = {'0x0': ' WinBtnReq_Idle', '0x1': ' WinBtnReq_Up1', '0x2': ' WinBtnReq_Up2', '0x3': ' WinBtnReq_Dwn1', '0x4': ' WinBtnReq_Dwn2', '0x5': ' WinBtnReq_Undef', '0x6': ' WinBtnReq_Reserved1', '0x7': ' WinBtnReq_Reserved2'}


class LCULMulticastEthSignalIPdu04:
    base_type = "Unsigned"
    client_socket = "SocketMulticast"
    pdu_header_id = 0x50FF04
    pdu_length_bytes = 2
    receiver = ['CCUMCUCD', 'CCUSOCCD', 'LCUR']
    send_type = "Cyclic-30ms"
    sender = "LCUL"
    server_socket = "SocketLcuLSoAdUDP"
    signal_group = {'BackLiDrvReq': ['BackLiDrvReqLiPerc', 'BackLiDrvReqLiPerc', 'BackLiDrvReqLiPerc', 'BackLiDrvReqLightCmd', 'BackLiDrvReqLightCmd', 'BackLiDrvReqLightCmd', 'BackLiDrvReqReadingLiDimsSpdCmd', 'BackLiDrvReqReadingLiDimsSpdCmd', 'BackLiDrvReqReadingLiDimsSpdCmd']}

    class BackLiDrvReqLiPerc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 9
        signal_description = "brightness percent"
        signal_length = 7
        start_position = 7
        value_definition = {}

    class BackLiDrvReqLightCmd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 9
        signal_description = "Light cmd"
        signal_length = 4
        start_position = 0
        value_definition = {'0x0': ' LightCmd_NoReq', '0x1': ' LightCmd_ON', '0x2': ' LightCmd_OFF', '0x3': ' LightCmd_TBD'}

    class BackLiDrvReqReadingLiDimsSpdCmd:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 9
        signal_description = "dim speed"
        signal_length = 3
        start_position = 12
        value_definition = {'0x0': ' ReadingLiDimsSpdCmd_NoCmd', '0x1': ' ReadingLiDimsSpdCmd_400ms', '0x2': ' ReadingLiDimsSpdCmd_800ms', '0x3': ' ReadingLiDimsSpdCmd_1000ms', '0x4': ' ReadingLiDimsSpdCmd_2000ms', '0x5': ' ReadingLiDimsSpdCmd_Resverd'}


class LCULMulticastEthSignalIPdu01:
    base_type = "Unsigned"
    client_socket = "SocketMulticast"
    pdu_header_id = 0x50FF01
    pdu_length_bytes = 70
    receiver = ['CCUMCUCD', 'CCUSOCCD', 'LCUR']
    send_type = "Cyclic-100ms"
    sender = "LCUL"
    server_socket = "SocketLcuLSoAdUDP"
    signal_group = {'CooltCircPmpStsFromRi': ['CooltCircPmpStsFromRiHVBattPmpSts', 'CooltCircPmpStsFromRiHVBattPmpSts', 'CooltCircPmpStsFromRiPWTPmpSts', 'CooltCircPmpStsFromRiPWTPmpSts', 'CooltCircPmpStsFromRiHeatrPmpSts', 'CooltCircPmpStsFromRiHeatrPmpSts'], 'FLPwrDoorErrFb': ['FLPwrDoorErrFbHallErrFb', 'FLPwrDoorErrFbHallErrFb', 'FLPwrDoorErrFbPosnUnknowFb', 'FLPwrDoorErrFbPosnUnknowFb', 'FLPwrDoorErrFbBoolean', 'FLPwrDoorErrFbBoolean', 'FLPwrDoorErrFbMotThermErrFb', 'FLPwrDoorErrFbMotThermErrFb', 'FLPwrDoorErrFbRollAngErrFb', 'FLPwrDoorErrFbRollAngErrFb'], 'LeftElecPeaErrFb': ['LeftElecPeaErrFbBoolean4', 'LeftElecPeaErrFbBoolean4', 'LeftElecPeaErrFbBoolean5', 'LeftElecPeaErrFbBoolean5', 'LeftElecPeaErrFbBoolean3', 'LeftElecPeaErrFbBoolean3', 'LeftElecPeaErrFbBoolean1', 'LeftElecPeaErrFbBoolean1', 'LeftElecPeaErrFbBoolean2', 'LeftElecPeaErrFbBoolean2'], 'PwrChLeActSts': ['PwrChLeActStsSwilPwrChLe12ActSts', 'PwrChLeActStsSwilPwrChLe12ActSts', 'PwrChLeActStsSwilPwrChLe19ActSts', 'PwrChLeActStsSwilPwrChLe19ActSts', 'PwrChLeActStsSwilPwrChLe20ActSts', 'PwrChLeActStsSwilPwrChLe20ActSts', 'PwrChLeActStsSwilPwrChLe15ActSts', 'PwrChLeActStsSwilPwrChLe15ActSts', 'PwrChLeActStsSwilPwrChLe1ActSts', 'PwrChLeActStsSwilPwrChLe1ActSts', 'PwrChLeActStsContnsPwrChLe1ActSts', 'PwrChLeActStsContnsPwrChLe1ActSts', 'PwrChLeActStsSwilPwrChLe9ActSts', 'PwrChLeActStsSwilPwrChLe9ActSts', 'PwrChLeActStsSwilPwrChLe28ActSts', 'PwrChLeActStsSwilPwrChLe28ActSts', 'PwrChLeActStsSwilPwrChLe29ActSts', 'PwrChLeActStsSwilPwrChLe29ActSts', 'PwrChLeActStsSwilPwrChLe27ActSts', 'PwrChLeActStsSwilPwrChLe27ActSts', 'PwrChLeActStsContnsPwrChLe3ActSts', 'PwrChLeActStsContnsPwrChLe3ActSts', 'PwrChLeActStsSwilPwrChLe7ActSts', 'PwrChLeActStsSwilPwrChLe7ActSts', 'PwrChLeActStsSwilPwrChLe26ActSts', 'PwrChLeActStsSwilPwrChLe26ActSts', 'PwrChLeActStsSwilPwrChLe3ActSts', 'PwrChLeActStsSwilPwrChLe3ActSts', 'PwrChLeActStsSwilPwrChLe18ActSts', 'PwrChLeActStsSwilPwrChLe18ActSts', 'PwrChLeActStsSwilPwrChLe8ActSts', 'PwrChLeActStsSwilPwrChLe8ActSts', 'PwrChLeActStsSwilPwrChLe21ActSts', 'PwrChLeActStsSwilPwrChLe21ActSts', 'PwrChLeActStsContnsPwrChLe4ActSts', 'PwrChLeActStsContnsPwrChLe4ActSts', 'PwrChLeActStsSwilPwrChLe10ActSts', 'PwrChLeActStsSwilPwrChLe10ActSts', 'PwrChLeActStsSwilPwrChLe16ActSts', 'PwrChLeActStsSwilPwrChLe16ActSts', 'PwrChLeActStsContnsPwrChLe2ActSts', 'PwrChLeActStsContnsPwrChLe2ActSts', 'PwrChLeActStsSwilPwrChLe11ActSts', 'PwrChLeActStsSwilPwrChLe11ActSts', 'PwrChLeActStsSwilPwrChLe22ActSts', 'PwrChLeActStsSwilPwrChLe22ActSts', 'PwrChLeActStsContnsPwrChLe5ActSts', 'PwrChLeActStsContnsPwrChLe5ActSts', 'PwrChLeActStsSwilPwrChLe6ActSts', 'PwrChLeActStsSwilPwrChLe6ActSts', 'PwrChLeActStsSwilPwrChLe24ActSts', 'PwrChLeActStsSwilPwrChLe24ActSts', 'PwrChLeActStsSwilPwrChLe2ActSts', 'PwrChLeActStsSwilPwrChLe2ActSts', 'PwrChLeActStsSwilPwrChLe5ActSts', 'PwrChLeActStsSwilPwrChLe5ActSts', 'PwrChLeActStsSwilPwrChLe4ActSts', 'PwrChLeActStsSwilPwrChLe4ActSts', 'PwrChLeActStsSwilPwrChLe14ActSts', 'PwrChLeActStsSwilPwrChLe14ActSts', 'PwrChLeActStsSwilPwrChLe25ActSts', 'PwrChLeActStsSwilPwrChLe25ActSts', 'PwrChLeActStsSwilPwrChLe13ActSts', 'PwrChLeActStsSwilPwrChLe13ActSts', 'PwrChLeActStsSwilPwrChLe23ActSts', 'PwrChLeActStsSwilPwrChLe23ActSts', 'PwrChLeActStsSwilPwrChLe17ActSts', 'PwrChLeActStsSwilPwrChLe17ActSts'], 'PwrChLeErr': ['PwrChLeErrSwilPwrChLe28Err', 'PwrChLeErrSwilPwrChLe28Err', 'PwrChLeErrSwilPwrChLe11Err', 'PwrChLeErrSwilPwrChLe11Err', 'PwrChLeErrSwilPwrChLe21Err', 'PwrChLeErrSwilPwrChLe21Err', 'PwrChLeErrSwilPwrChLe19Err', 'PwrChLeErrSwilPwrChLe19Err', 'PwrChLeErrContnsPwrChLe4Err', 'PwrChLeErrContnsPwrChLe4Err', 'PwrChLeErrSwilPwrChLe18Err', 'PwrChLeErrSwilPwrChLe18Err', 'PwrChLeErrSwilPwrChLe14Err', 'PwrChLeErrSwilPwrChLe14Err', 'PwrChLeErrSwilPwrChLe5Err', 'PwrChLeErrSwilPwrChLe5Err', 'PwrChLeErrSwilPwrChLe15Err', 'PwrChLeErrSwilPwrChLe15Err', 'PwrChLeErrSwilPwrChLe8Err', 'PwrChLeErrSwilPwrChLe8Err', 'PwrChLeErrContnsPwrChLe3Err', 'PwrChLeErrContnsPwrChLe3Err', 'PwrChLeErrSwilPwrChLe2Err', 'PwrChLeErrSwilPwrChLe2Err', 'PwrChLeErrContnsPwrChLe5Err', 'PwrChLeErrContnsPwrChLe5Err', 'PwrChLeErrSwilPwrChLe24Err', 'PwrChLeErrSwilPwrChLe24Err', 'PwrChLeErrSwilPwrChLe25Err', 'PwrChLeErrSwilPwrChLe25Err', 'PwrChLeErrContnsPwrChLe2Err', 'PwrChLeErrContnsPwrChLe2Err', 'PwrChLeErrSwilPwrChLe16Err', 'PwrChLeErrSwilPwrChLe16Err', 'PwrChLeErrContnsPwrChLe1Err', 'PwrChLeErrContnsPwrChLe1Err', 'PwrChLeErrSwilPwrChLe10Err', 'PwrChLeErrSwilPwrChLe10Err', 'PwrChLeErrSwilPwrChLe3Err', 'PwrChLeErrSwilPwrChLe3Err', 'PwrChLeErrSwilPwrChLe12Err', 'PwrChLeErrSwilPwrChLe12Err', 'PwrChLeErrSwilPwrChLe6Err', 'PwrChLeErrSwilPwrChLe6Err', 'PwrChLeErrSwilPwrChLe26Err', 'PwrChLeErrSwilPwrChLe26Err', 'PwrChLeErrSwilPwrChLe29Err', 'PwrChLeErrSwilPwrChLe29Err', 'PwrChLeErrSwilPwrChLe27Err', 'PwrChLeErrSwilPwrChLe27Err', 'PwrChLeErrSwilPwrChLe13Err', 'PwrChLeErrSwilPwrChLe13Err', 'PwrChLeErrSwilPwrChLe20Err', 'PwrChLeErrSwilPwrChLe20Err', 'PwrChLeErrSwilPwrChLe17Err', 'PwrChLeErrSwilPwrChLe17Err', 'PwrChLeErrSwilPwrChLe9Err', 'PwrChLeErrSwilPwrChLe9Err', 'PwrChLeErrSwilPwrChLe1Err', 'PwrChLeErrSwilPwrChLe1Err', 'PwrChLeErrSwilPwrChLe22Err', 'PwrChLeErrSwilPwrChLe22Err', 'PwrChLeErrSwilPwrChLe4Err', 'PwrChLeErrSwilPwrChLe4Err', 'PwrChLeErrSwilPwrChLe7Err', 'PwrChLeErrSwilPwrChLe7Err', 'PwrChLeErrSwilPwrChLe23Err', 'PwrChLeErrSwilPwrChLe23Err'], 'RefrigCircVlvCalStsFromLe': ['RefrigCircVlvCalStsFromLeCERVCalSts', 'RefrigCircVlvCalStsFromLeCERVCalSts', 'RefrigCircVlvCalStsFromLeWERVCalSts', 'RefrigCircVlvCalStsFromLeWERVCalSts', 'RefrigCircVlvCalStsFromLeBEXVCalSts', 'RefrigCircVlvCalStsFromLeBEXVCalSts', 'RefrigCircVlvCalStsFromLeREXVCalSts', 'RefrigCircVlvCalStsFromLeREXVCalSts', 'RefrigCircVlvCalStsFromLeTERVCalSts', 'RefrigCircVlvCalStsFromLeTERVCalSts', 'RefrigCircVlvCalStsFromLeFEXVCalSts', 'RefrigCircVlvCalStsFromLeFEXVCalSts'], 'RefrigCircVlvStsFromLe': ['RefrigCircVlvStsFromLeRefrigSOV2Sts', 'RefrigCircVlvStsFromLeRefrigSOV2Sts', 'RefrigCircVlvStsFromLeWERVSts', 'RefrigCircVlvStsFromLeWERVSts', 'RefrigCircVlvStsFromLeTERVSts', 'RefrigCircVlvStsFromLeTERVSts', 'RefrigCircVlvStsFromLeFEXVSts', 'RefrigCircVlvStsFromLeFEXVSts', 'RefrigCircVlvStsFromLeCERVSts', 'RefrigCircVlvStsFromLeCERVSts', 'RefrigCircVlvStsFromLeRefrigSOV1Sts', 'RefrigCircVlvStsFromLeRefrigSOV1Sts', 'RefrigCircVlvStsFromLeREXVSts', 'RefrigCircVlvStsFromLeREXVSts', 'RefrigCircVlvStsFromLeBEXVSts', 'RefrigCircVlvStsFromLeBEXVSts', 'RefrigCircVlvStsFromLeRefrigSOV3Sts', 'RefrigCircVlvStsFromLeRefrigSOV3Sts'], 'RightElecPeaErrFb': ['RightElecPeaErrFbBoolean4', 'RightElecPeaErrFbBoolean4', 'RightElecPeaErrFbBoolean2', 'RightElecPeaErrFbBoolean2', 'RightElecPeaErrFbBoolean3', 'RightElecPeaErrFbBoolean3', 'RightElecPeaErrFbBoolean5', 'RightElecPeaErrFbBoolean5', 'RightElecPeaErrFbBoolean1', 'RightElecPeaErrFbBoolean1'], 'RLChdLockErrFb': ['RLChdLockErrFbUnlockFail', 'RLChdLockErrFbUnlockFail', 'RLChdLockErrFbLockFail', 'RLChdLockErrFbLockFail', 'RLChdLockErrFbError1', 'RLChdLockErrFbError1', 'RLChdLockErrFbError2', 'RLChdLockErrFbError2', 'RLChdLockErrFbMotorOverTherm', 'RLChdLockErrFbMotorOverTherm'], 'RLPwrDoorErrFb': ['RLPwrDoorErrFbPosnUnknowFb', 'RLPwrDoorErrFbPosnUnknowFb', 'RLPwrDoorErrFbBoolean', 'RLPwrDoorErrFbBoolean', 'RLPwrDoorErrFbMotThermErrFb', 'RLPwrDoorErrFbMotThermErrFb', 'RLPwrDoorErrFbRollAngErrFb', 'RLPwrDoorErrFbRollAngErrFb', 'RLPwrDoorErrFbHallErrFb', 'RLPwrDoorErrFbHallErrFb']}

    class CooltCircPmpStsFromRiHVBattPmpSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 9
        signal_description = "HvBatt Pump Status"
        signal_length = 3
        start_position = 1
        value_definition = {'0x0': ' ThermPmpSts_Initial', '0x1': ' ThermPmpSts_Normal', '0x2': ' ThermPmpSts_DryRun', '0x3': ' ThermPmpSts_Err'}

    class CooltCircPmpStsFromRiPWTPmpSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 9
        signal_description = "PWT Pump Status"
        signal_length = 3
        start_position = 7
        value_definition = {'0x0': ' ThermPmpSts_Initial', '0x1': ' ThermPmpSts_Normal', '0x2': ' ThermPmpSts_DryRun', '0x3': ' ThermPmpSts_Err'}

    class CooltCircPmpStsFromRiHeatrPmpSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 9
        signal_description = "HVCH Pump Status"
        signal_length = 3
        start_position = 4
        value_definition = {'0x0': ' ThermPmpSts_Initial', '0x1': ' ThermPmpSts_Normal', '0x2': ' ThermPmpSts_DryRun', '0x3': ' ThermPmpSts_Err'}

    class FLDoorMaxPosnSetFb:
        comments = ""
        factor = 1.0
        initial_value = 101
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 101
        signal_description = "Maximum percentage feedback that power side doors can open"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class FLPwrDoorErrFbHallErrFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 100
        signal_description = "hall error"
        signal_length = 1
        start_position = 31
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class FLPwrDoorErrFbPosnUnknowFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 100
        signal_description = "door position lost"
        signal_length = 1
        start_position = 30
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class FLPwrDoorErrFbBoolean:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 100
        signal_description = "error status"
        signal_length = 1
        start_position = 29
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class FLPwrDoorErrFbMotThermErrFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 100
        signal_description = "Motor overheating"
        signal_length = 1
        start_position = 28
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class FLPwrDoorErrFbRollAngErrFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 100
        signal_description = "roll angle error"
        signal_length = 1
        start_position = 27
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class HeatrCooltPmpPwmFb:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 99
        signal_description = "Pump PWM feedback"
        signal_length = 10
        start_position = 26
        value_definition = {}

    class HeatrCooltPmpPwrCns:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 98
        signal_description = "HVCH Coolant Pump Power Consumption"
        signal_length = 12
        start_position = 32
        value_definition = {}

    class HVBattCooltPmpPwmFb:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 97
        signal_description = "Pump PWM feedback"
        signal_length = 10
        start_position = 52
        value_definition = {}

    class HVBattCooltPmpPwrCns:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 96
        signal_description = "HvBatt Coolant Pump Power Consumption"
        signal_length = 12
        start_position = 58
        value_definition = {}

    class LeftElecPeaErrFbBoolean4:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 172
        signal_description = "Electric pedal Error status feedback"
        signal_length = 1
        start_position = 78
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class LeftElecPeaErrFbBoolean5:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 172
        signal_description = "Electric pedal Error status feedback"
        signal_length = 1
        start_position = 77
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class LeftElecPeaErrFbBoolean3:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 172
        signal_description = "Electric pedal Error status feedback"
        signal_length = 1
        start_position = 76
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class LeftElecPeaErrFbBoolean1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 172
        signal_description = "Electric pedal Error status feedback"
        signal_length = 1
        start_position = 75
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class LeftElecPeaErrFbBoolean2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 172
        signal_description = "Electric pedal Error status feedback"
        signal_length = 1
        start_position = 74
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class PrimBattIRaw:
        comments = ""
        factor = 0.015625
        initial_value = 32768
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -512
        sig_ub = 171
        signal_description = "Primary battery current"
        signal_length = 16
        start_position = 87
        value_definition = {}

    class PrimBattLockLoadSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 170
        signal_description = "Primary Battery Lock Load Status"
        signal_length = 2
        start_position = 103
        value_definition = {'0x0': ' BattLockLoadSts_Idle', '0x1': ' BattLockLoadSts_UnLockLoad', '0x2': ' BattLockLoadSts_PreLockLoad', '0x3': ' BattLockLoadSts_LockLoad'}

    class PrimBattSOCRaw:
        comments = ""
        factor = 1.0
        initial_value = 100
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 169
        signal_description = "Primary battery SOC"
        signal_length = 8
        start_position = 111
        value_definition = {'0xFF': 'BattSOH_Invalid'}

    class PrimBattSOCSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 168
        signal_description = "Primary battery SOC accuracy status"
        signal_length = 2
        start_position = 119
        value_definition = {'0x0': ' LVBattCal_Idle', '0x1': ' LVBattCal_CmplCal', '0x2': ' LVBattCal_InCmplCal', '0x3': ' LVBattCal_Resvd'}

    class PrimBattTRaw:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = 513
        signal_description = "Primary battery temperature"
        signal_length = 13
        start_position = 117
        value_definition = {}

    class PrimBattURaw:
        comments = ""
        factor = 0.02
        initial_value = 1023
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 512
        signal_description = "Primary battery voltage"
        signal_length = 10
        start_position = 120
        value_definition = {'0x3FF': 'BattU2_BMSVolWakeUpThd'}

    class PwrChLeActStsSwilPwrChLe12ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 522
        signal_description = "Left Zone Swil Power Channel 12 Actual Status"
        signal_length = 1
        start_position = 142
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChLeActStsSwilPwrChLe19ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 522
        signal_description = "Left Zone Swil Power Channel 19 Actual Status"
        signal_length = 1
        start_position = 141
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChLeActStsSwilPwrChLe20ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 522
        signal_description = "Left Zone Swil Power Channel 20 Actual Status"
        signal_length = 1
        start_position = 140
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChLeActStsSwilPwrChLe15ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 522
        signal_description = "Left Zone Swil Power Channel 15 Actual Status"
        signal_length = 1
        start_position = 139
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChLeActStsSwilPwrChLe1ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 522
        signal_description = "Left Zone Swil Power Channel 1 Actual Status"
        signal_length = 1
        start_position = 138
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChLeActStsContnsPwrChLe1ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 522
        signal_description = "Left Zone Contns Power Channel 1 Actual Status"
        signal_length = 1
        start_position = 137
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChLeActStsSwilPwrChLe9ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 522
        signal_description = "Left Zone Swil Power Channel 9 Actual Status"
        signal_length = 1
        start_position = 136
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChLeActStsSwilPwrChLe28ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 522
        signal_description = "Left Zone Swil Power Channel 28 Actual Status"
        signal_length = 1
        start_position = 151
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChLeActStsSwilPwrChLe29ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 522
        signal_description = "Left Zone Swil Power Channel 29 Actual Status"
        signal_length = 1
        start_position = 150
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChLeActStsSwilPwrChLe27ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 522
        signal_description = "Left Zone Swil Power Channel 27 Actual Status"
        signal_length = 1
        start_position = 149
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChLeActStsContnsPwrChLe3ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 522
        signal_description = "Left Zone Contns Power Channel 3 Actual Status"
        signal_length = 1
        start_position = 148
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChLeActStsSwilPwrChLe7ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 522
        signal_description = "Left Zone Swil Power Channel 7 Actual Status"
        signal_length = 1
        start_position = 147
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChLeActStsSwilPwrChLe26ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 522
        signal_description = "Left Zone Swil Power Channel 26 Actual Status"
        signal_length = 1
        start_position = 146
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChLeActStsSwilPwrChLe3ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 522
        signal_description = "Left Zone Swil Power Channel 3 Actual Status"
        signal_length = 1
        start_position = 145
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChLeActStsSwilPwrChLe18ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 522
        signal_description = "Left Zone Swil Power Channel 18 Actual Status"
        signal_length = 1
        start_position = 144
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChLeActStsSwilPwrChLe8ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 522
        signal_description = "Left Zone Swil Power Channel 8 Actual Status"
        signal_length = 1
        start_position = 159
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChLeActStsSwilPwrChLe21ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 522
        signal_description = "Left Zone Swil Power Channel 21 Actual Status"
        signal_length = 1
        start_position = 158
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChLeActStsContnsPwrChLe4ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 522
        signal_description = "Left Zone Contns Power Channel 4 Actual Status"
        signal_length = 1
        start_position = 157
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChLeActStsSwilPwrChLe10ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 522
        signal_description = "Left Zone Swil Power Channel 10 Actual Status"
        signal_length = 1
        start_position = 156
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChLeActStsSwilPwrChLe16ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 522
        signal_description = "Left Zone Swil Power Channel 16 Actual Status"
        signal_length = 1
        start_position = 155
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChLeActStsContnsPwrChLe2ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 522
        signal_description = "Left Zone Contns Power Channel 2 Actual Status"
        signal_length = 1
        start_position = 154
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChLeActStsSwilPwrChLe11ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 522
        signal_description = "Left Zone Swil Power Channel 11 Actual Status"
        signal_length = 1
        start_position = 153
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChLeActStsSwilPwrChLe22ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 522
        signal_description = "Left Zone Swil Power Channel 22 Actual Status"
        signal_length = 1
        start_position = 152
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChLeActStsContnsPwrChLe5ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 522
        signal_description = "Left Zone Contns Power Channel 5 Actual Status"
        signal_length = 1
        start_position = 167
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChLeActStsSwilPwrChLe6ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 522
        signal_description = "Left Zone Swil Power Channel 6 Actual Status"
        signal_length = 1
        start_position = 166
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChLeActStsSwilPwrChLe24ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 522
        signal_description = "Left Zone Swil Power Channel 24 Actual Status"
        signal_length = 1
        start_position = 165
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChLeActStsSwilPwrChLe2ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 522
        signal_description = "Left Zone Swil Power Channel 2 Actual Status"
        signal_length = 1
        start_position = 164
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChLeActStsSwilPwrChLe5ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 522
        signal_description = "Left Zone Swil Power Channel 5 Actual Status"
        signal_length = 1
        start_position = 163
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChLeActStsSwilPwrChLe4ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 522
        signal_description = "Left Zone Swil Power Channel 4 Actual Status"
        signal_length = 1
        start_position = 162
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChLeActStsSwilPwrChLe14ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 522
        signal_description = "Left Zone Swil Power Channel 14 Actual Status"
        signal_length = 1
        start_position = 161
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChLeActStsSwilPwrChLe25ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 522
        signal_description = "Left Zone Swil Power Channel 25 Actual Status"
        signal_length = 1
        start_position = 160
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChLeActStsSwilPwrChLe13ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 522
        signal_description = "Left Zone Swil Power Channel 13 Actual Status"
        signal_length = 1
        start_position = 175
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChLeActStsSwilPwrChLe23ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 522
        signal_description = "Left Zone Swil Power Channel 23 Actual Status"
        signal_length = 1
        start_position = 174
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChLeActStsSwilPwrChLe17ActSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 522
        signal_description = "Left Zone Swil Power Channel 17 Actual Status"
        signal_length = 1
        start_position = 173
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrChLeErrSwilPwrChLe28Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 521
        signal_description = "Left Zone Swil Power Channel 28 Error Status"
        signal_length = 8
        start_position = 183
        value_definition = {}

    class PwrChLeErrSwilPwrChLe11Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 521
        signal_description = "Left Zone Swil Power Channel 11 Error Status"
        signal_length = 8
        start_position = 191
        value_definition = {}

    class PwrChLeErrSwilPwrChLe21Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 521
        signal_description = "Left Zone Swil Power Channel 21 Error Status"
        signal_length = 8
        start_position = 199
        value_definition = {}

    class PwrChLeErrSwilPwrChLe19Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 521
        signal_description = "Left Zone Swil Power Channel 19 Error Status"
        signal_length = 8
        start_position = 207
        value_definition = {}

    class PwrChLeErrContnsPwrChLe4Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 521
        signal_description = "Left Zone Contns Power Channel 4 Error Status"
        signal_length = 8
        start_position = 215
        value_definition = {}

    class PwrChLeErrSwilPwrChLe18Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 521
        signal_description = "Left Zone Swil Power Channel 18 Error Status"
        signal_length = 8
        start_position = 223
        value_definition = {}

    class PwrChLeErrSwilPwrChLe14Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 521
        signal_description = "Left Zone Swil Power Channel 14 Error Status"
        signal_length = 8
        start_position = 231
        value_definition = {}

    class PwrChLeErrSwilPwrChLe5Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 521
        signal_description = "Left Zone Swil Power Channel 5 Error Status"
        signal_length = 8
        start_position = 239
        value_definition = {}

    class PwrChLeErrSwilPwrChLe15Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 521
        signal_description = "Left Zone Swil Power Channel 15 Error Status"
        signal_length = 8
        start_position = 247
        value_definition = {}

    class PwrChLeErrSwilPwrChLe8Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 521
        signal_description = "Left Zone Swil Power Channel 8 Error Status"
        signal_length = 8
        start_position = 255
        value_definition = {}

    class PwrChLeErrContnsPwrChLe3Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 521
        signal_description = "Left Zone Contns Power Channel 3 Error Status"
        signal_length = 8
        start_position = 263
        value_definition = {}

    class PwrChLeErrSwilPwrChLe2Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 521
        signal_description = "Left Zone Swil Power Channel 2 Error Status"
        signal_length = 8
        start_position = 271
        value_definition = {}

    class PwrChLeErrContnsPwrChLe5Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 521
        signal_description = "Left Zone Contns Power Channel 5 Error Status"
        signal_length = 8
        start_position = 279
        value_definition = {}

    class PwrChLeErrSwilPwrChLe24Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 521
        signal_description = "Left Zone Swil Power Channel 24 Error Status"
        signal_length = 8
        start_position = 287
        value_definition = {}

    class PwrChLeErrSwilPwrChLe25Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 521
        signal_description = "Left Zone Swil Power Channel 25 Error Status"
        signal_length = 8
        start_position = 295
        value_definition = {}

    class PwrChLeErrContnsPwrChLe2Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 521
        signal_description = "Left Zone Contns Power Channel 2 Error Status"
        signal_length = 8
        start_position = 303
        value_definition = {}

    class PwrChLeErrSwilPwrChLe16Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 521
        signal_description = "Left Zone Swil Power Channel 16 Error Status"
        signal_length = 8
        start_position = 311
        value_definition = {}

    class PwrChLeErrContnsPwrChLe1Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 521
        signal_description = "Left Zone Contns Power Channel 1 Error Status"
        signal_length = 8
        start_position = 319
        value_definition = {}

    class PwrChLeErrSwilPwrChLe10Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 521
        signal_description = "Left Zone Swil Power Channel 10 Error Status"
        signal_length = 8
        start_position = 327
        value_definition = {}

    class PwrChLeErrSwilPwrChLe3Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 521
        signal_description = "Left Zone Swil Power Channel 3 Error Status"
        signal_length = 8
        start_position = 335
        value_definition = {}

    class PwrChLeErrSwilPwrChLe12Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 521
        signal_description = "Left Zone Swil Power Channel 12 Error Status"
        signal_length = 8
        start_position = 343
        value_definition = {}

    class PwrChLeErrSwilPwrChLe6Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 521
        signal_description = "Left Zone Swil Power Channel 6 Error Status"
        signal_length = 8
        start_position = 351
        value_definition = {}

    class PwrChLeErrSwilPwrChLe26Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 521
        signal_description = "Left Zone Swil Power Channel 26 Error Status"
        signal_length = 8
        start_position = 359
        value_definition = {}

    class PwrChLeErrSwilPwrChLe29Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 521
        signal_description = "Left Zone Swil Power Channel 29 Error Status"
        signal_length = 8
        start_position = 367
        value_definition = {}

    class PwrChLeErrSwilPwrChLe27Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 521
        signal_description = "Left Zone Swil Power Channel 27 Error Status"
        signal_length = 8
        start_position = 375
        value_definition = {}

    class PwrChLeErrSwilPwrChLe13Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 521
        signal_description = "Left Zone Swil Power Channel 13 Error Status"
        signal_length = 8
        start_position = 383
        value_definition = {}

    class PwrChLeErrSwilPwrChLe20Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 521
        signal_description = "Left Zone Swil Power Channel 20 Error Status"
        signal_length = 8
        start_position = 391
        value_definition = {}

    class PwrChLeErrSwilPwrChLe17Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 521
        signal_description = "Left Zone Swil Power Channel 17 Error Status"
        signal_length = 8
        start_position = 399
        value_definition = {}

    class PwrChLeErrSwilPwrChLe9Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 521
        signal_description = "Left Zone Swil Power Channel 9 Error Status"
        signal_length = 8
        start_position = 407
        value_definition = {}

    class PwrChLeErrSwilPwrChLe1Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 521
        signal_description = "Left Zone Swil Power Channel 1 Error Status"
        signal_length = 8
        start_position = 415
        value_definition = {}

    class PwrChLeErrSwilPwrChLe22Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 521
        signal_description = "Left Zone Swil Power Channel 22 Error Status"
        signal_length = 8
        start_position = 423
        value_definition = {}

    class PwrChLeErrSwilPwrChLe4Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 521
        signal_description = "Left Zone Swil Power Channel 4 Error Status"
        signal_length = 8
        start_position = 431
        value_definition = {}

    class PwrChLeErrSwilPwrChLe7Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 521
        signal_description = "Left Zone Swil Power Channel 7 Error Status"
        signal_length = 8
        start_position = 439
        value_definition = {}

    class PwrChLeErrSwilPwrChLe23Err:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 521
        signal_description = "Left Zone Swil Power Channel 23 Error Status"
        signal_length = 8
        start_position = 447
        value_definition = {}

    class PWTCooltPmpPwmFb:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 520
        signal_description = "Pump PWM feedback"
        signal_length = 10
        start_position = 455
        value_definition = {}

    class PWTCooltPmpPwrCns:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 543
        signal_description = "PWT Coolant Pump Power Consumption"
        signal_length = 12
        start_position = 461
        value_definition = {}

    class RefrigCircVlvCalStsFromLeCERVCalSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 542
        signal_description = "Valve Calibration Stauts"
        signal_length = 2
        start_position = 465
        value_definition = {'0x0': ' ExvCalibSts_NotInitialized', '0x1': ' ExvCalibSts_InitializationInProcess', '0x2': ' ExvCalibSts_Initialized', '0x3': ' ExvCalibSts_Reserved'}

    class RefrigCircVlvCalStsFromLeWERVCalSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 542
        signal_description = "Valve Calibration Stauts"
        signal_length = 2
        start_position = 479
        value_definition = {'0x0': ' ExvCalibSts_NotInitialized', '0x1': ' ExvCalibSts_InitializationInProcess', '0x2': ' ExvCalibSts_Initialized', '0x3': ' ExvCalibSts_Reserved'}

    class RefrigCircVlvCalStsFromLeBEXVCalSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 542
        signal_description = "Valve Calibration Stauts"
        signal_length = 2
        start_position = 477
        value_definition = {'0x0': ' ExvCalibSts_NotInitialized', '0x1': ' ExvCalibSts_InitializationInProcess', '0x2': ' ExvCalibSts_Initialized', '0x3': ' ExvCalibSts_Reserved'}

    class RefrigCircVlvCalStsFromLeREXVCalSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 542
        signal_description = "Valve Calibration Stauts"
        signal_length = 2
        start_position = 475
        value_definition = {'0x0': ' ExvCalibSts_NotInitialized', '0x1': ' ExvCalibSts_InitializationInProcess', '0x2': ' ExvCalibSts_Initialized', '0x3': ' ExvCalibSts_Reserved'}

    class RefrigCircVlvCalStsFromLeTERVCalSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 542
        signal_description = "Valve Calibration Stauts"
        signal_length = 2
        start_position = 473
        value_definition = {'0x0': ' ExvCalibSts_NotInitialized', '0x1': ' ExvCalibSts_InitializationInProcess', '0x2': ' ExvCalibSts_Initialized', '0x3': ' ExvCalibSts_Reserved'}

    class RefrigCircVlvCalStsFromLeFEXVCalSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 542
        signal_description = "Valve Calibration Stauts"
        signal_length = 2
        start_position = 487
        value_definition = {'0x0': ' ExvCalibSts_NotInitialized', '0x1': ' ExvCalibSts_InitializationInProcess', '0x2': ' ExvCalibSts_Initialized', '0x3': ' ExvCalibSts_Reserved'}

    class RefrigCircVlvStsFromLeRefrigSOV2Sts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 541
        signal_description = "Valve Stauts"
        signal_length = 3
        start_position = 485
        value_definition = {'0x0': ' ThermCooltVlvSts_Unknow', '0x1': ' ThermCooltVlvSts_Normal', '0x2': ' ThermCooltVlvSts_Err'}

    class RefrigCircVlvStsFromLeWERVSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 541
        signal_description = "Valve Stauts"
        signal_length = 3
        start_position = 482
        value_definition = {'0x0': ' ThermCooltVlvSts_Unknow', '0x1': ' ThermCooltVlvSts_Normal', '0x2': ' ThermCooltVlvSts_Err'}

    class RefrigCircVlvStsFromLeTERVSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 541
        signal_description = "Valve Stauts"
        signal_length = 3
        start_position = 495
        value_definition = {'0x0': ' ThermCooltVlvSts_Unknow', '0x1': ' ThermCooltVlvSts_Normal', '0x2': ' ThermCooltVlvSts_Err'}

    class RefrigCircVlvStsFromLeFEXVSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 541
        signal_description = "Valve Stauts"
        signal_length = 3
        start_position = 492
        value_definition = {'0x0': ' ThermCooltVlvSts_Unknow', '0x1': ' ThermCooltVlvSts_Normal', '0x2': ' ThermCooltVlvSts_Err'}

    class RefrigCircVlvStsFromLeCERVSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 541
        signal_description = "Valve Stauts"
        signal_length = 3
        start_position = 489
        value_definition = {'0x0': ' ThermCooltVlvSts_Unknow', '0x1': ' ThermCooltVlvSts_Normal', '0x2': ' ThermCooltVlvSts_Err'}

    class RefrigCircVlvStsFromLeRefrigSOV1Sts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 541
        signal_description = "Valve Stauts"
        signal_length = 3
        start_position = 502
        value_definition = {'0x0': ' ThermCooltVlvSts_Unknow', '0x1': ' ThermCooltVlvSts_Normal', '0x2': ' ThermCooltVlvSts_Err'}

    class RefrigCircVlvStsFromLeREXVSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 541
        signal_description = "Valve Stauts"
        signal_length = 3
        start_position = 499
        value_definition = {'0x0': ' ThermCooltVlvSts_Unknow', '0x1': ' ThermCooltVlvSts_Normal', '0x2': ' ThermCooltVlvSts_Err'}

    class RefrigCircVlvStsFromLeBEXVSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 541
        signal_description = "Valve Stauts"
        signal_length = 3
        start_position = 496
        value_definition = {'0x0': ' ThermCooltVlvSts_Unknow', '0x1': ' ThermCooltVlvSts_Normal', '0x2': ' ThermCooltVlvSts_Err'}

    class RefrigCircVlvStsFromLeRefrigSOV3Sts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 541
        signal_description = "Valve Status"
        signal_length = 3
        start_position = 509
        value_definition = {'0x0': ' ThermCooltVlvSts_Unknow', '0x1': ' ThermCooltVlvSts_Normal', '0x2': ' ThermCooltVlvSts_Err'}

    class RightElecPeaErrFbBoolean4:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 540
        signal_description = "Electric pedal Error status feedback"
        signal_length = 1
        start_position = 548
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class RightElecPeaErrFbBoolean2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 540
        signal_description = "Electric pedal Error status feedback"
        signal_length = 1
        start_position = 550
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class RightElecPeaErrFbBoolean3:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 540
        signal_description = "Electric pedal Error status feedback"
        signal_length = 1
        start_position = 549
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class RightElecPeaErrFbBoolean5:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 540
        signal_description = "Electric pedal Error status feedback"
        signal_length = 1
        start_position = 547
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class RightElecPeaErrFbBoolean1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 540
        signal_description = "Electric pedal Error status feedback"
        signal_length = 1
        start_position = 551
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class RLChdLockErrFbUnlockFail:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 539
        signal_description = "unlock fail"
        signal_length = 1
        start_position = 504
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class RLChdLockErrFbLockFail:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 539
        signal_description = "lock fail"
        signal_length = 1
        start_position = 519
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class RLChdLockErrFbError1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 539
        signal_description = "error1"
        signal_length = 1
        start_position = 518
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class RLChdLockErrFbError2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 539
        signal_description = "error2"
        signal_length = 1
        start_position = 517
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class RLChdLockErrFbMotorOverTherm:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 539
        signal_description = "motor over therm"
        signal_length = 1
        start_position = 516
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class RLPwrDoorErrFbPosnUnknowFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 536
        signal_description = "door position lost"
        signal_length = 1
        start_position = 524
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class RLPwrDoorErrFbBoolean:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 536
        signal_description = "error status"
        signal_length = 1
        start_position = 527
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class RLPwrDoorErrFbMotThermErrFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 536
        signal_description = "Motor overheating"
        signal_length = 1
        start_position = 525
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class RLPwrDoorErrFbRollAngErrFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 536
        signal_description = "roll angle error"
        signal_length = 1
        start_position = 523
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class RLPwrDoorErrFbHallErrFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 536
        signal_description = "hall error"
        signal_length = 1
        start_position = 526
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class RLDoorMaxPosnSetFb:
        comments = ""
        factor = 1.0
        initial_value = 101
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 538
        signal_description = "Maximum percentage feedback that power side doors can open"
        signal_length = 8
        start_position = 535
        value_definition = {}

    class RLDoorModSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 537
        signal_description = "power side door mode status"
        signal_length = 2
        start_position = 515
        value_definition = {'0x0': ' DoorModSts_ElecMode', '0x1': ' DoorModSts_ManualMode'}

    class CooltLvlIndReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 8
        signal_description = "coolant level indication request"
        signal_length = 2
        start_position = 14
        value_definition = {'0x0': ' ReqSts2_Default', '0x1': ' ReqSts2_NotReqd', '0x2': ' ReqSts2_Reqd', '0x3': ' ReqSts2_Reserved'}

    class CooltSov1ActrSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 72
        signal_description = "Cooling fan actuator status"
        signal_length = 2
        start_position = 11
        value_definition = {'0x0': ' Flt_Initial', '0x1': ' Flt_NoFault', '0x2': ' Flt_Fault'}


class LCULMulticastEthSignalIPdu06:
    base_type = "Unsigned"
    client_socket = "SocketMulticast"
    pdu_header_id = 0x50FF06
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD', 'CCUSOCCD', 'LCUR']
    send_type = "Cyclic-80ms"
    sender = "LCUL"
    server_socket = "SocketLcuLSoAdUDP"
    signal_group = {}

    class DayOrNightSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 6
        signal_description = "the state of day or night"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' DayOrNightSts_Night', '0x1': ' DayOrNightSts_Day'}


class LCULMulticastEthSignalIPdu02:
    base_type = "Unsigned"
    client_socket = "SocketMulticast"
    pdu_header_id = 0x50FF02
    pdu_length_bytes = 4
    receiver = ['CCUMCUCD', 'CCUSOCCD']
    send_type = "Cyclic-200ms"
    sender = "LCUL"
    server_socket = "SocketLcuLSoAdUDP"
    signal_group = {}

    class SecRowLeOccpSnsrRawSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 23
        signal_description = "Second Row Left Seat Occupy Sensor Raw Status"
        signal_length = 4
        start_position = 7
        value_definition = {'0x0': ' OccptSnsrOutpSts_Empty', '0x1': ' OccptSnsrOutpSts_L1', '0x2': ' OccptSnsrOutpSts_L2', '0x3': ' OccptSnsrOutpSts_L3', '0x4': ' OccptSnsrOutpSts_L4', '0x5': ' OccptSnsrOutpSts_Occupied', '0x6': ' OccptSnsrOutpSts_Unknown'}

    class SecRowMidOccpSnsrRawSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 22
        signal_description = "SecondRow Middle Occupy Sensor Raw Status"
        signal_length = 4
        start_position = 3
        value_definition = {'0x0': ' OccptSnsrOutpSts_Empty', '0x1': ' OccptSnsrOutpSts_L1', '0x2': ' OccptSnsrOutpSts_L2', '0x3': ' OccptSnsrOutpSts_L3', '0x4': ' OccptSnsrOutpSts_L4', '0x5': ' OccptSnsrOutpSts_Occupied', '0x6': ' OccptSnsrOutpSts_Unknown'}

    class ThrdRowLeOccpSnsrRawSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 21
        signal_description = "Third Row Left Occupy Sensor Raw Status"
        signal_length = 4
        start_position = 15
        value_definition = {'0x0': ' OccptSnsrOutpSts_Empty', '0x1': ' OccptSnsrOutpSts_L1', '0x2': ' OccptSnsrOutpSts_L2', '0x3': ' OccptSnsrOutpSts_L3', '0x4': ' OccptSnsrOutpSts_L4', '0x5': ' OccptSnsrOutpSts_Occupied', '0x6': ' OccptSnsrOutpSts_Unknown'}

    class ThrdRowMidOccpSnsrRawSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 20
        signal_description = "Third Row Middle Occupy Sensor Raw Status"
        signal_length = 4
        start_position = 11
        value_definition = {'0x0': ' OccptSnsrOutpSts_Empty', '0x1': ' OccptSnsrOutpSts_L1', '0x2': ' OccptSnsrOutpSts_L2', '0x3': ' OccptSnsrOutpSts_L3', '0x4': ' OccptSnsrOutpSts_L4', '0x5': ' OccptSnsrOutpSts_Occupied', '0x6': ' OccptSnsrOutpSts_Unknown'}

    class ThrdRowMidOccpSnsrOKSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 16
        signal_description = "Third Row Middle Occupy Sensor OK Status"
        signal_length = 1
        start_position = 28
        value_definition = {'0x0': ' OkNotOk1_Ok', '0x1': ' OkNotOk1_NotOk'}

    class SecRowLeOccpSnsrOKSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 19
        signal_description = "Second Row Left Seat Occupy Sensor OK Status"
        signal_length = 1
        start_position = 31
        value_definition = {'0x0': ' OkNotOk1_Ok', '0x1': ' OkNotOk1_NotOk'}

    class ThrdRowLeOccpSnsrOKSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 17
        signal_description = "Third Row Left Occupy Sensor OK Status"
        signal_length = 1
        start_position = 29
        value_definition = {'0x0': ' OkNotOk1_Ok', '0x1': ' OkNotOk1_NotOk'}

    class SecRowMidOccpSnsrOKSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 18
        signal_description = "SecondRow Middle Occupy Sensor OK Status"
        signal_length = 1
        start_position = 30
        value_definition = {'0x0': ' OkNotOk1_Ok', '0x1': ' OkNotOk1_NotOk'}
