

class LCULToLCUREthSignalIPdu03:
    base_type = "Unsigned"
    client_socket = "SocketLcuRSoAdUDP"
    pdu_header_id = 0x506003
    pdu_length_bytes = 8
    receiver = ['LCUR']
    send_type = "Cyclic-20ms"
    sender = "LCUL"
    server_socket = "SocketLcuLSoAdUDP"
    signal_group = {'FootwellLiFrntRiDrvReq': ['FootwellLiFrntRiDrvReqLiPerc', 'FootwellLiFrntRiDrvReqLightCmd', 'FootwellLiFrntRiDrvReqReadingLiDimsSpdCmd'], 'FootwellLiSecRiDrvReq': ['FootwellLiSecRiDrvReqLightCmd', 'FootwellLiSecRiDrvReqReadingLiDimsSpdCmd', 'FootwellLiSecRiDrvReqLiPerc'], 'FootwellLiThrdRiDrvReq': ['FootwellLiThrdRiDrvReqReadingLiDimsSpdCmd', 'FootwellLiThrdRiDrvReqLiPerc', 'FootwellLiThrdRiDrvReqLightCmd']}

    class DayNightSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 41
        signal_description = "Day Night Status"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' OutdBriSts_Ukwn', '0x1': ' OutdBriSts_Night', '0x2': ' OutdBriSts_Day', '0x3': ' OutdBriSts_Invld'}

    class FLDoorLtchOpenSwt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 40
        signal_description = "switch status of door latch"
        signal_length = 1
        start_position = 5
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class FootwellLiFrntRiDrvReqLiPerc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 55
        signal_description = "brightness percent"
        signal_length = 7
        start_position = 4
        value_definition = {}

    class FootwellLiFrntRiDrvReqLightCmd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 55
        signal_description = "light command"
        signal_length = 4
        start_position = 13
        value_definition = {'0x0': ' LightCmd_NoReq', '0x1': ' LightCmd_ON', '0x2': ' LightCmd_OFF', '0x3': ' LightCmd_TBD'}

    class FootwellLiFrntRiDrvReqReadingLiDimsSpdCmd:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 55
        signal_description = "required dim speed"
        signal_length = 3
        start_position = 9
        value_definition = {'0x0': ' ReadingLiDimsSpdCmd_NoCmd', '0x1': ' ReadingLiDimsSpdCmd_400ms', '0x2': ' ReadingLiDimsSpdCmd_800ms', '0x3': ' ReadingLiDimsSpdCmd_1000ms', '0x4': ' ReadingLiDimsSpdCmd_2000ms', '0x5': ' ReadingLiDimsSpdCmd_Resverd'}

    class FootwellLiSecRiDrvReqLightCmd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 54
        signal_description = "light command"
        signal_length = 4
        start_position = 22
        value_definition = {'0x0': ' LightCmd_NoReq', '0x1': ' LightCmd_ON', '0x2': ' LightCmd_OFF', '0x3': ' LightCmd_TBD'}

    class FootwellLiSecRiDrvReqReadingLiDimsSpdCmd:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 54
        signal_description = "required dim speed"
        signal_length = 3
        start_position = 18
        value_definition = {'0x0': ' ReadingLiDimsSpdCmd_NoCmd', '0x1': ' ReadingLiDimsSpdCmd_400ms', '0x2': ' ReadingLiDimsSpdCmd_800ms', '0x3': ' ReadingLiDimsSpdCmd_1000ms', '0x4': ' ReadingLiDimsSpdCmd_2000ms', '0x5': ' ReadingLiDimsSpdCmd_Resverd'}

    class FootwellLiSecRiDrvReqLiPerc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 54
        signal_description = "brightness percent"
        signal_length = 7
        start_position = 31
        value_definition = {}

    class FootwellLiThrdRiDrvReqReadingLiDimsSpdCmd:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 53
        signal_description = "required dim speed"
        signal_length = 3
        start_position = 24
        value_definition = {'0x0': ' ReadingLiDimsSpdCmd_NoCmd', '0x1': ' ReadingLiDimsSpdCmd_400ms', '0x2': ' ReadingLiDimsSpdCmd_800ms', '0x3': ' ReadingLiDimsSpdCmd_1000ms', '0x4': ' ReadingLiDimsSpdCmd_2000ms', '0x5': ' ReadingLiDimsSpdCmd_Resverd'}

    class FootwellLiThrdRiDrvReqLiPerc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 53
        signal_description = "brightness percent"
        signal_length = 7
        start_position = 37
        value_definition = {}

    class FootwellLiThrdRiDrvReqLightCmd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 53
        signal_description = "light command"
        signal_length = 4
        start_position = 46
        value_definition = {'0x0': ' LightCmd_NoReq', '0x1': ' LightCmd_ON', '0x2': ' LightCmd_OFF', '0x3': ' LightCmd_TBD'}

    class RLDoorLtchOpenSwt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 52
        signal_description = "switch status of door latch"
        signal_length = 1
        start_position = 42
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}


class LCULToLCUREthSignalIPdu04:
    base_type = "Unsigned"
    client_socket = "SocketLcuRSoAdUDP"
    pdu_header_id = 0x506004
    pdu_length_bytes = 2
    receiver = ['LCUR']
    send_type = "Cyclic-80ms"
    sender = "LCUL"
    server_socket = "SocketLcuLSoAdUDP"
    signal_group = {}

    class ThdLiPWMFbFrntLe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 9
        signal_description = "the PWM feedback of the front leftthreshold light "
        signal_length = 7
        start_position = 7
        value_definition = {}

    class ThdLiPWMFbReLe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 8
        signal_description = "the PWM feedback of the rear left threshold light "
        signal_length = 7
        start_position = 0
        value_definition = {}


class LCULToLCUREthSignalIPdu01:
    base_type = "Unsigned"
    client_socket = "SocketLcuRSoAdUDP"
    pdu_header_id = 0x506001
    pdu_length_bytes = 32
    receiver = ['LCUR']
    send_type = "Cyclic-100ms"
    sender = "LCUL"
    server_socket = "SocketLcuLSoAdUDP"
    signal_group = {'AmbTRawLeSide': ['AmbTRawLeSideTQF', 'AmbTRawLeSideT'], 'TrunkLiDrvSts': ['TrunkLiDrvStsLiPerc', 'TrunkLiDrvStsLightSts', 'TrunkLiDrvStsLightErrorCode'], 'WinOpenValueReq': ['WinOpenValueReqWinReLeOpenValue', 'WinOpenValueReqWinDrvrOpenValue', 'WinOpenValueReqWinReRiOpenValue', 'WinOpenValueReqWinPassOpenValue']}

    class AmbTRawLeSideTQF:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 9
        signal_description = "Left Side Ambient Temperature Raw Value Quality Flag"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' HVACTempQf_SnsrDataNotOk', '0x1': ' HVACTempQf_SnsrDataOk'}

    class AmbTRawLeSideT:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = 9
        signal_description = "Left Side Ambient Temperature Raw Value"
        signal_length = 13
        start_position = 6
        value_definition = {}

    class TrunkLiDrvStsLiPerc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 8
        signal_description = "brightness percent"
        signal_length = 7
        start_position = 27
        value_definition = {}

    class TrunkLiDrvStsLightSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 8
        signal_description = "light status"
        signal_length = 4
        start_position = 31
        value_definition = {'0x0': ' LightSts_Off', '0x1': ' LightSts_On', '0x2': ' LightSts_Error', '0x3': ' LightSts_Reserved'}

    class TrunkLiDrvStsLightErrorCode:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 8
        signal_description = "error status"
        signal_length = 8
        start_position = 23
        value_definition = {'0x0': ' LightErrorCode_ChipError', '0x1': ' LightErrorCode_ShortError', '0x2': ' LightErrorCode_OpenError', '0xFF': ' LightErrorCode_NoneError'}

    class LeSpkrObstrcnSts:
        comments = ""
        factor = 1.0
        initial_value = 4
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 106
        signal_description = "LeftSpeakerObstructionStatus"
        signal_length = 8
        start_position = 119
        value_definition = {'0x0': ' LeSpkrObstrcnSts_FirstObstructionDuringMovingUp', '0x1': ' LeSpkrObstrcnSts_FirstObstructionDuringMovingDown', '0x2': ' LeSpkrObstrcnSts_SecondaryObstructionDuringMovingUp', '0x3': ' LeSpkrObstrcnSts_SecondaryObstructionDuringMovingDown', '0x4': ' LeSpkrObstrcnSts_Normal'}

    class WinOpenValueReqWinReLeOpenValue:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 139
        signal_description = "Rear Left Window Open Value"
        signal_length = 5
        start_position = 133
        value_definition = {'0x0': ' CmdPosnPerc_PosnUkwn', '0x1': ' CmdPosnPerc_Close', '0x2': ' CmdPosnPerc_Open4', '0x3': ' CmdPosnPerc_Open8', '0x4': ' CmdPosnPerc_Open12', '0x5': ' CmdPosnPerc_Open16', '0x6': ' CmdPosnPerc_Open20', '0x7': ' CmdPosnPerc_Open24', '0x8': ' CmdPosnPerc_Open28', '0x9': ' CmdPosnPerc_Open32', '0xA': ' CmdPosnPerc_Open36', '0xB': ' CmdPosnPerc_Open40', '0xC': ' CmdPosnPerc_Open44', '0xD': ' CmdPosnPerc_Open48', '0xE': ' CmdPosnPerc_Open52', '0xF': ' CmdPosnPerc_Open56', '0x10': ' CmdPosnPerc_Open60', '0x11': ' CmdPosnPerc_Open64', '0x12': ' CmdPosnPerc_Open68', '0x13': ' CmdPosnPerc_Open72', '0x14': ' CmdPosnPerc_Open76', '0x15': ' CmdPosnPerc_Open80', '0x16': ' CmdPosnPerc_Open84', '0x17': ' CmdPosnPerc_Open88', '0x18': ' CmdPosnPerc_Open92', '0x19': ' CmdPosnPerc_Open96', '0x1A': ' CmdPosnPerc_Open100', '0x1B': ' CmdPosnPerc_Stop', '0x1C': ' CmdPosnPerc_Resd2', '0x1D': ' CmdPosnPerc_Resd3', '0x1E': ' CmdPosnPerc_Resd4', '0x1F': ' CmdPosnPerc_Resd5'}

    class WinOpenValueReqWinDrvrOpenValue:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 139
        signal_description = "Driver Window Open Value"
        signal_length = 5
        start_position = 127
        value_definition = {'0x0': ' CmdPosnPerc_PosnUkwn', '0x1': ' CmdPosnPerc_Close', '0x2': ' CmdPosnPerc_Open4', '0x3': ' CmdPosnPerc_Open8', '0x4': ' CmdPosnPerc_Open12', '0x5': ' CmdPosnPerc_Open16', '0x6': ' CmdPosnPerc_Open20', '0x7': ' CmdPosnPerc_Open24', '0x8': ' CmdPosnPerc_Open28', '0x9': ' CmdPosnPerc_Open32', '0xA': ' CmdPosnPerc_Open36', '0xB': ' CmdPosnPerc_Open40', '0xC': ' CmdPosnPerc_Open44', '0xD': ' CmdPosnPerc_Open48', '0xE': ' CmdPosnPerc_Open52', '0xF': ' CmdPosnPerc_Open56', '0x10': ' CmdPosnPerc_Open60', '0x11': ' CmdPosnPerc_Open64', '0x12': ' CmdPosnPerc_Open68', '0x13': ' CmdPosnPerc_Open72', '0x14': ' CmdPosnPerc_Open76', '0x15': ' CmdPosnPerc_Open80', '0x16': ' CmdPosnPerc_Open84', '0x17': ' CmdPosnPerc_Open88', '0x18': ' CmdPosnPerc_Open92', '0x19': ' CmdPosnPerc_Open96', '0x1A': ' CmdPosnPerc_Open100', '0x1B': ' CmdPosnPerc_Stop', '0x1C': ' CmdPosnPerc_Resd2', '0x1D': ' CmdPosnPerc_Resd3', '0x1E': ' CmdPosnPerc_Resd4', '0x1F': ' CmdPosnPerc_Resd5'}

    class WinOpenValueReqWinReRiOpenValue:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 139
        signal_description = "Rear Right Window Open Value"
        signal_length = 5
        start_position = 128
        value_definition = {'0x0': ' CmdPosnPerc_PosnUkwn', '0x1': ' CmdPosnPerc_Close', '0x2': ' CmdPosnPerc_Open4', '0x3': ' CmdPosnPerc_Open8', '0x4': ' CmdPosnPerc_Open12', '0x5': ' CmdPosnPerc_Open16', '0x6': ' CmdPosnPerc_Open20', '0x7': ' CmdPosnPerc_Open24', '0x8': ' CmdPosnPerc_Open28', '0x9': ' CmdPosnPerc_Open32', '0xA': ' CmdPosnPerc_Open36', '0xB': ' CmdPosnPerc_Open40', '0xC': ' CmdPosnPerc_Open44', '0xD': ' CmdPosnPerc_Open48', '0xE': ' CmdPosnPerc_Open52', '0xF': ' CmdPosnPerc_Open56', '0x10': ' CmdPosnPerc_Open60', '0x11': ' CmdPosnPerc_Open64', '0x12': ' CmdPosnPerc_Open68', '0x13': ' CmdPosnPerc_Open72', '0x14': ' CmdPosnPerc_Open76', '0x15': ' CmdPosnPerc_Open80', '0x16': ' CmdPosnPerc_Open84', '0x17': ' CmdPosnPerc_Open88', '0x18': ' CmdPosnPerc_Open92', '0x19': ' CmdPosnPerc_Open96', '0x1A': ' CmdPosnPerc_Open100', '0x1B': ' CmdPosnPerc_Stop', '0x1C': ' CmdPosnPerc_Resd2', '0x1D': ' CmdPosnPerc_Resd3', '0x1E': ' CmdPosnPerc_Resd4', '0x1F': ' CmdPosnPerc_Resd5'}

    class WinOpenValueReqWinPassOpenValue:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 139
        signal_description = "Passenger Window Open Value"
        signal_length = 5
        start_position = 122
        value_definition = {'0x0': ' CmdPosnPerc_PosnUkwn', '0x1': ' CmdPosnPerc_Close', '0x2': ' CmdPosnPerc_Open4', '0x3': ' CmdPosnPerc_Open8', '0x4': ' CmdPosnPerc_Open12', '0x5': ' CmdPosnPerc_Open16', '0x6': ' CmdPosnPerc_Open20', '0x7': ' CmdPosnPerc_Open24', '0x8': ' CmdPosnPerc_Open28', '0x9': ' CmdPosnPerc_Open32', '0xA': ' CmdPosnPerc_Open36', '0xB': ' CmdPosnPerc_Open40', '0xC': ' CmdPosnPerc_Open44', '0xD': ' CmdPosnPerc_Open48', '0xE': ' CmdPosnPerc_Open52', '0xF': ' CmdPosnPerc_Open56', '0x10': ' CmdPosnPerc_Open60', '0x11': ' CmdPosnPerc_Open64', '0x12': ' CmdPosnPerc_Open68', '0x13': ' CmdPosnPerc_Open72', '0x14': ' CmdPosnPerc_Open76', '0x15': ' CmdPosnPerc_Open80', '0x16': ' CmdPosnPerc_Open84', '0x17': ' CmdPosnPerc_Open88', '0x18': ' CmdPosnPerc_Open92', '0x19': ' CmdPosnPerc_Open96', '0x1A': ' CmdPosnPerc_Open100', '0x1B': ' CmdPosnPerc_Stop', '0x1C': ' CmdPosnPerc_Resd2', '0x1D': ' CmdPosnPerc_Resd3', '0x1E': ' CmdPosnPerc_Resd4', '0x1F': ' CmdPosnPerc_Resd5'}


class LCULToLCUREthSignalIPdu02:
    base_type = "Unsigned"
    client_socket = "SocketLcuRSoAdUDP"
    pdu_header_id = 0x506002
    pdu_length_bytes = 1
    receiver = ['LCUR']
    send_type = "Cyclic-200ms"
    sender = "LCUL"
    server_socket = "SocketLcuLSoAdUDP"
    signal_group = {'ThdLiFailrFrntLe': ['ThdLiFailrFrntLeOpenCirc', 'ThdLiFailrFrntLeShoCircToGND', 'ThdLiFailrFrntLeShoCircToBatt'], 'ThdLiFailrReLe': ['ThdLiFailrReLeShoCircToBatt', 'ThdLiFailrReLeShoCircToGND', 'ThdLiFailrReLeOpenCirc']}

    class ThdLiFailrFrntLeOpenCirc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1
        signal_description = "open circuit,the front left threshold light"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' FailrNoFailr1_NoFailr', '0x1': ' FailrNoFailr1_Failr'}

    class ThdLiFailrFrntLeShoCircToGND:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1
        signal_description = "short circuit to ground,the front left threshold light"
        signal_length = 1
        start_position = 6
        value_definition = {'0x0': ' FailrNoFailr1_NoFailr', '0x1': ' FailrNoFailr1_Failr'}

    class ThdLiFailrFrntLeShoCircToBatt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1
        signal_description = "short circuit to battery,the front left threshold light"
        signal_length = 1
        start_position = 5
        value_definition = {'0x0': ' FailrNoFailr1_NoFailr', '0x1': ' FailrNoFailr1_Failr'}

    class ThdLiFailrReLeShoCircToBatt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 0
        signal_description = "short circuit to battery,the rear left threshold light"
        signal_length = 1
        start_position = 4
        value_definition = {'0x0': ' FailrNoFailr1_NoFailr', '0x1': ' FailrNoFailr1_Failr'}

    class ThdLiFailrReLeShoCircToGND:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 0
        signal_description = "short circuit to ground,the rear left threshold light"
        signal_length = 1
        start_position = 3
        value_definition = {'0x0': ' FailrNoFailr1_NoFailr', '0x1': ' FailrNoFailr1_Failr'}

    class ThdLiFailrReLeOpenCirc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 0
        signal_description = "open circuit,the rear left threshold light"
        signal_length = 1
        start_position = 2
        value_definition = {'0x0': ' FailrNoFailr1_NoFailr', '0x1': ' FailrNoFailr1_Failr'}


class LCURToLCULEthSignalIPdu01:
    base_type = "Unsigned"
    client_socket = "SocketLcuLSoAdUDP"
    pdu_header_id = 0x605001
    pdu_length_bytes = 9
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "LCUR"
    server_socket = "SocketLcuRSoAdUDP"
    signal_group = {'FootwellLiFrntRiDrvSts': ['FootwellLiFrntRiDrvStsLiPerc', 'FootwellLiFrntRiDrvStsLightErrorCode', 'FootwellLiFrntRiDrvStsLightSts'], 'FootwellLiSecRiDrvSts': ['FootwellLiSecRiDrvStsLightSts', 'FootwellLiSecRiDrvStsLiPerc', 'FootwellLiSecRiDrvStsLightErrorCode'], 'FootwellLiThrdRiDrvSts': ['FootwellLiThrdRiDrvStsLightSts', 'FootwellLiThrdRiDrvStsLightErrorCode', 'FootwellLiThrdRiDrvStsLiPerc']}

    class FootwellLiFrntRiDrvStsLiPerc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 20
        signal_description = "brightness percent"
        signal_length = 7
        start_position = 11
        value_definition = {}

    class FootwellLiFrntRiDrvStsLightErrorCode:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 20
        signal_description = "error status"
        signal_length = 8
        start_position = 7
        value_definition = {'0x0': ' LightErrorCode_ChipError', '0x1': ' LightErrorCode_ShortError', '0x2': ' LightErrorCode_OpenError', '0xFF': ' LightErrorCode_NoneError'}

    class FootwellLiFrntRiDrvStsLightSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 20
        signal_description = "light status"
        signal_length = 4
        start_position = 15
        value_definition = {'0x0': ' LightSts_Off', '0x1': ' LightSts_On', '0x2': ' LightSts_Error', '0x3': ' LightSts_Reserved'}

    class FootwellLiSecRiDrvStsLightSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 44
        signal_description = "light status"
        signal_length = 4
        start_position = 39
        value_definition = {'0x0': ' LightSts_Off', '0x1': ' LightSts_On', '0x2': ' LightSts_Error', '0x3': ' LightSts_Reserved'}

    class FootwellLiSecRiDrvStsLiPerc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 44
        signal_description = "brightness percent"
        signal_length = 7
        start_position = 35
        value_definition = {}

    class FootwellLiSecRiDrvStsLightErrorCode:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 44
        signal_description = "error status"
        signal_length = 8
        start_position = 31
        value_definition = {'0x0': ' LightErrorCode_ChipError', '0x1': ' LightErrorCode_ShortError', '0x2': ' LightErrorCode_OpenError', '0xFF': ' LightErrorCode_NoneError'}

    class FootwellLiThrdRiDrvStsLightSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 68
        signal_description = "light status"
        signal_length = 4
        start_position = 63
        value_definition = {'0x0': ' LightSts_Off', '0x1': ' LightSts_On', '0x2': ' LightSts_Error', '0x3': ' LightSts_Reserved'}

    class FootwellLiThrdRiDrvStsLightErrorCode:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 68
        signal_description = "error status"
        signal_length = 8
        start_position = 55
        value_definition = {'0x0': ' LightErrorCode_ChipError', '0x1': ' LightErrorCode_ShortError', '0x2': ' LightErrorCode_OpenError', '0xFF': ' LightErrorCode_NoneError'}

    class FootwellLiThrdRiDrvStsLiPerc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 68
        signal_description = "brightness percent"
        signal_length = 7
        start_position = 59
        value_definition = {}


class LCURToLCULEthSignalIPdu03:
    base_type = "Unsigned"
    client_socket = "SocketLcuLSoAdUDP"
    pdu_header_id = 0x605003
    pdu_length_bytes = 1
    receiver = ['LCUL']
    send_type = "Cyclic-80ms"
    sender = "LCUR"
    server_socket = "SocketLcuRSoAdUDP"
    signal_group = {}

    class ThdLiActvFrntLe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 3
        signal_description = "Front left threshold light activation command"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' ActvInActv2_Init', '0x1': ' ActvInActv2_InActv', '0x2': ' ActvInActv2_Actv'}

    class ThdLiActvReLe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 2
        signal_description = "Rear left threshold light activation command"
        signal_length = 2
        start_position = 5
        value_definition = {'0x0': ' ActvInActv2_Init', '0x1': ' ActvInActv2_InActv', '0x2': ' ActvInActv2_Actv'}


class LCURToLCULEthSignalIPdu02:
    base_type = "Unsigned"
    client_socket = "SocketLcuLSoAdUDP"
    pdu_header_id = 0x605002
    pdu_length_bytes = 1
    receiver = ['LCUL']
    send_type = "Cyclic-20ms"
    sender = "LCUR"
    server_socket = "SocketLcuRSoAdUDP"
    signal_group = {}

    class FRDoorLtchOpenSwt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 5
        signal_description = "switch status of door latch"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class RRDoorLtchOpenSwt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 4
        signal_description = "switch status of door latch"
        signal_length = 1
        start_position = 6
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}


class LCURToLCULEthSignalIPdu04:
    base_type = "Unsigned"
    client_socket = "SocketLcuLSoAdUDP"
    pdu_header_id = 0x605004
    pdu_length_bytes = 2
    receiver = ['LCUL']
    send_type = "Cyclic-100ms"
    sender = "LCUR"
    server_socket = "SocketLcuRSoAdUDP"
    signal_group = {}

    class RiSpkrObstrcnSts:
        comments = ""
        factor = 1.0
        initial_value = 4
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 15
        signal_description = "LeftSpeakerObstructionStatus"
        signal_length = 8
        start_position = 7
        value_definition = {'0x0': ' RiSpkrObstrcnSts_FirstObstructionDuringMovingUp', '0x1': ' RiSpkrObstrcnSts_FirstObstructionDuringMovingDown', '0x2': ' RiSpkrObstrcnSts_SecondaryObstructionDuringMovingUp', '0x3': ' RiSpkrObstrcnSts_SecondaryObstructionDuringMovingDown', '0x4': ' RiSpkrObstrcnSts_Normal'}
