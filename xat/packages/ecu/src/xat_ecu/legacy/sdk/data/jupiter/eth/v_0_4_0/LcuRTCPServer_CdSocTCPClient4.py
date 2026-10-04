

class CCUSOCCDToLCUREthSignalIPdu06:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x406006
    pdu_length_bytes = 1
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {}

    class ExtrReViewMirrAutoFoldEna:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Mirror Auto Enable"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' MirrAutoEn_Idle', '0x1': ' MirrAutoEn_EnableBoth', '0x2': ' MirrAutoEn_EnableFoldOnly', '0x3': ' MirrAutoEn_EnableUnfoldOnly', '0x4': ' MirrAutoEn_Disable'}


class CCUSOCCDToLCUREthSignalIPdu04:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x406004
    pdu_length_bytes = 2
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {'ReadingLiFrntLeAdjReq': ['ReadingLiFrntLeAdjReqLightCmd', 'ReadingLiFrntLeAdjReqReadingLiDimsSpdCmd', 'ReadingLiFrntLeAdjReqLiPerc']}

    class ReadingLiFrntLeAdjReqLightCmd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "mode req of fl"
        signal_length = 4
        start_position = 7
        value_definition = {'0x0': ' LightCmd_NoReq', '0x1': ' LightCmd_ON', '0x2': ' LightCmd_OFF', '0x3': ' LightCmd_TBD'}

    class ReadingLiFrntLeAdjReqReadingLiDimsSpdCmd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "adjustment speed command of the  front left reading light intensity "
        signal_length = 3
        start_position = 3
        value_definition = {'0x0': ' ReadingLiDimsSpdCmd_NoCmd', '0x1': ' ReadingLiDimsSpdCmd_400ms', '0x2': ' ReadingLiDimsSpdCmd_800ms', '0x3': ' ReadingLiDimsSpdCmd_1000ms', '0x4': ' ReadingLiDimsSpdCmd_2000ms', '0x5': ' ReadingLiDimsSpdCmd_Resverd'}

    class ReadingLiFrntLeAdjReqLiPerc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "adjustment command of the  front left reading light intensity "
        signal_length = 7
        start_position = 15
        value_definition = {}


class CCUSOCCDToLCUREthSignalIPdu01:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x406001
    pdu_length_bytes = 6
    receiver = ['LCUR']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {'AFUOnOffReqFromSrv': ['AFUOnOffReqFromSrvCh4', 'AFUOnOffReqFromSrvCh5', 'AFUOnOffReqFromSrvCh3', 'AFUOnOffReqFromSrvCh1', 'AFUOnOffReqFromSrvCh2'], 'AFURelsRatReqFromSrv': ['AFURelsRatReqFromSrvCh5', 'AFURelsRatReqFromSrvCh1', 'AFURelsRatReqFromSrvCh4', 'AFURelsRatReqFromSrvCh3', 'AFURelsRatReqFromSrvCh2']}

    class AFUOnOffReqFromSrvCh4:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Air Fragrance Channel 4 OnOff Request From Service"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class AFUOnOffReqFromSrvCh5:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Air Fragrance Channel 5 OnOff Request From Service"
        signal_length = 1
        start_position = 6
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class AFUOnOffReqFromSrvCh3:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Air Fragrance Channel 3 OnOff Request From Service"
        signal_length = 1
        start_position = 5
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class AFUOnOffReqFromSrvCh1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Air Fragrance Channel 1 OnOff Request From Service"
        signal_length = 1
        start_position = 4
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class AFUOnOffReqFromSrvCh2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Air Fragrance Channel 2 OnOff Request From Service"
        signal_length = 1
        start_position = 3
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class AFURelsRatReqFromSrvCh5:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Air Fragrance Channel 5 Release Ratio Request From Service"
        signal_length = 7
        start_position = 47
        value_definition = {}

    class AFURelsRatReqFromSrvCh1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Air Fragrance Channel 1 Release Ratio Request From Service"
        signal_length = 7
        start_position = 15
        value_definition = {}

    class AFURelsRatReqFromSrvCh4:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Air Fragrance Channel 4 Release Ratio Request From Service"
        signal_length = 7
        start_position = 39
        value_definition = {}

    class AFURelsRatReqFromSrvCh3:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Air Fragrance Channel 3 Release Ratio Request From Service"
        signal_length = 7
        start_position = 31
        value_definition = {}

    class AFURelsRatReqFromSrvCh2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Air Fragrance Channel 2 Release Ratio Request From Service"
        signal_length = 7
        start_position = 23
        value_definition = {}


class CCUSOCCDToLCUREthSignalIPdu02:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x406002
    pdu_length_bytes = 4
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {'ConsoleDwnALMRGBL': ['ConsoleDwnALMRGBLRed', 'ConsoleDwnALMRGBLBlue', 'ConsoleDwnALMRGBLGreen', 'ConsoleDwnALMRGBLLuminance']}

    class ConsoleDwnALMRGBLRed:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Red,ConsoleDwnALMRGBL"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class ConsoleDwnALMRGBLBlue:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Blue,ConsoleDwnALMRGBL"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class ConsoleDwnALMRGBLGreen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Green,ConsoleDwnALMRGBL"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class ConsoleDwnALMRGBLLuminance:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Luminance,ConsoleDwnALMRGBL"
        signal_length = 7
        start_position = 31
        value_definition = {}


class CCUSOCCDToLCUREthSignalIPdu03:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x406003
    pdu_length_bytes = 2
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {'FuncReqOfDaytimeRunningLamp': ['FuncReqOfDaytimeRunningLampLightCmd', 'FuncReqOfDaytimeRunningLampLightID1', 'FuncReqOfDaytimeRunningLampLightPriority']}

    class FuncReqOfDaytimeRunningLampLightCmd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "LightCmd"
        signal_length = 4
        start_position = 7
        value_definition = {'0x0': ' LightCmd_NoReq', '0x1': ' LightCmd_ON', '0x2': ' LightCmd_OFF', '0x3': ' LightCmd_TBD'}

    class FuncReqOfDaytimeRunningLampLightID1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "LightID"
        signal_length = 4
        start_position = 3
        value_definition = {'0x0': ' LightID1_ALL', '0x1': ' LightID1_Front', '0x2': ' LightID1_Rear', '0x3': ' LightID1_LeftFrontLeftRearLeft', '0x4': ' LightID1_RightFrontRightRearRight', '0x5': ' LightID1_FrontLeft', '0x6': ' LightID1_FrontRight', '0x7': ' LightID1_RearLeft', '0x8': ' LightID1_FrontLeftRearRight', '0x9': ' LightID1_FrontRightRearLeft', '0xA': ' LightID1_ExceptFrontLeft', '0xB': ' LightID1_ExceptFrontRight', '0xC': ' LightID1_ExceptRearLeft', '0xD': ' LightID1_ExceptRearRight', '0xE': ' LightID1_Reserved1', '0xF': ' LightID1_Reserved2'}

    class FuncReqOfDaytimeRunningLampLightPriority:
        comments = ""
        factor = 1.0
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "LightPriority"
        signal_length = 8
        start_position = 15
        value_definition = {}


class CCUSOCCDToLCUREthSignalIPdu05:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x406005
    pdu_length_bytes = 1
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {}

    class DoorSpdModeSet:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "power side door speed mode set"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' SpdMode_Low', '0x1': ' SpdMode_Middle', '0x2': ' SpdMode_High'}


class CCUSOCCDToLCUREthSignalIPdu07:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x406007
    pdu_length_bytes = 1
    receiver = ['LCUR']
    send_type = "EventTriggered"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {}

    class PwrChProtRstReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Power Channel Protection Reset Request"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}


class CCUSOCCDToLCUREthSignalIPdu08:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x406008
    pdu_length_bytes = 4
    receiver = ['LCUR']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {}

    class ElecVentSrvFrntRiLeXPosnReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Vent Grill Motor 5 Position Request"
        signal_length = 16
        start_position = 7
        value_definition = {}

    class ElecVentSrvFrntRiLeYPosnReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Vent Grill Motor 6 Position Request"
        signal_length = 16
        start_position = 23
        value_definition = {}


class CCUSOCCDToLCUREthSignalIPdu09:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x406009
    pdu_length_bytes = 4
    receiver = ['LCUR']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {}

    class ElecVentSrvFrntRiRiXPosnReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Vent Grill Motor 7 Position Request"
        signal_length = 16
        start_position = 7
        value_definition = {}

    class ElecVentSrvFrntRiRiYPosnReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Vent Grill Motor 8 Position Request"
        signal_length = 16
        start_position = 23
        value_definition = {}


class CCUSOCCDToLCUREthSignalIPdu14:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x40600E
    pdu_length_bytes = 1
    receiver = ['LCUR']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {}

    class PwrUnLockReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Power Unlock Requirement"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' ReqSts2_Default', '0x1': ' ReqSts2_NotReqd', '0x2': ' ReqSts2_Reqd', '0x3': ' ReqSts2_Reserved'}


class CCUSOCCDToLCUREthSignalIPdu17:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x406011
    pdu_length_bytes = 3
    receiver = ['LCUR']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {'WinSrvOpenValueReq': ['WinSrvOpenValueReqWinDrvrOpenValue', 'WinSrvOpenValueReqWinReLeOpenValue', 'WinSrvOpenValueReqWinReRiOpenValue', 'WinSrvOpenValueReqWinPassOpenValue']}

    class WinSrvOpenValueReqWinDrvrOpenValue:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Driver Window Open Value"
        signal_length = 5
        start_position = 7
        value_definition = {'0x0': ' CmdPosnPerc_PosnUkwn', '0x1': ' CmdPosnPerc_Close', '0x2': ' CmdPosnPerc_Open4', '0x3': ' CmdPosnPerc_Open8', '0x4': ' CmdPosnPerc_Open12', '0x5': ' CmdPosnPerc_Open16', '0x6': ' CmdPosnPerc_Open20', '0x7': ' CmdPosnPerc_Open24', '0x8': ' CmdPosnPerc_Open28', '0x9': ' CmdPosnPerc_Open32', '0xA': ' CmdPosnPerc_Open36', '0xB': ' CmdPosnPerc_Open40', '0xC': ' CmdPosnPerc_Open44', '0xD': ' CmdPosnPerc_Open48', '0xE': ' CmdPosnPerc_Open52', '0xF': ' CmdPosnPerc_Open56', '0x10': ' CmdPosnPerc_Open60', '0x11': ' CmdPosnPerc_Open64', '0x12': ' CmdPosnPerc_Open68', '0x13': ' CmdPosnPerc_Open72', '0x14': ' CmdPosnPerc_Open76', '0x15': ' CmdPosnPerc_Open80', '0x16': ' CmdPosnPerc_Open84', '0x17': ' CmdPosnPerc_Open88', '0x18': ' CmdPosnPerc_Open92', '0x19': ' CmdPosnPerc_Open96', '0x1A': ' CmdPosnPerc_Open100', '0x1B': ' CmdPosnPerc_Stop', '0x1C': ' CmdPosnPerc_Resd2', '0x1D': ' CmdPosnPerc_Resd3', '0x1E': ' CmdPosnPerc_Resd4', '0x1F': ' CmdPosnPerc_Resd5'}

    class WinSrvOpenValueReqWinReLeOpenValue:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Rear Left Window Open Value"
        signal_length = 5
        start_position = 13
        value_definition = {'0x0': ' CmdPosnPerc_PosnUkwn', '0x1': ' CmdPosnPerc_Close', '0x2': ' CmdPosnPerc_Open4', '0x3': ' CmdPosnPerc_Open8', '0x4': ' CmdPosnPerc_Open12', '0x5': ' CmdPosnPerc_Open16', '0x6': ' CmdPosnPerc_Open20', '0x7': ' CmdPosnPerc_Open24', '0x8': ' CmdPosnPerc_Open28', '0x9': ' CmdPosnPerc_Open32', '0xA': ' CmdPosnPerc_Open36', '0xB': ' CmdPosnPerc_Open40', '0xC': ' CmdPosnPerc_Open44', '0xD': ' CmdPosnPerc_Open48', '0xE': ' CmdPosnPerc_Open52', '0xF': ' CmdPosnPerc_Open56', '0x10': ' CmdPosnPerc_Open60', '0x11': ' CmdPosnPerc_Open64', '0x12': ' CmdPosnPerc_Open68', '0x13': ' CmdPosnPerc_Open72', '0x14': ' CmdPosnPerc_Open76', '0x15': ' CmdPosnPerc_Open80', '0x16': ' CmdPosnPerc_Open84', '0x17': ' CmdPosnPerc_Open88', '0x18': ' CmdPosnPerc_Open92', '0x19': ' CmdPosnPerc_Open96', '0x1A': ' CmdPosnPerc_Open100', '0x1B': ' CmdPosnPerc_Stop', '0x1C': ' CmdPosnPerc_Resd2', '0x1D': ' CmdPosnPerc_Resd3', '0x1E': ' CmdPosnPerc_Resd4', '0x1F': ' CmdPosnPerc_Resd5'}

    class WinSrvOpenValueReqWinReRiOpenValue:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Rear Right Window Open Value"
        signal_length = 5
        start_position = 8
        value_definition = {'0x0': ' CmdPosnPerc_PosnUkwn', '0x1': ' CmdPosnPerc_Close', '0x2': ' CmdPosnPerc_Open4', '0x3': ' CmdPosnPerc_Open8', '0x4': ' CmdPosnPerc_Open12', '0x5': ' CmdPosnPerc_Open16', '0x6': ' CmdPosnPerc_Open20', '0x7': ' CmdPosnPerc_Open24', '0x8': ' CmdPosnPerc_Open28', '0x9': ' CmdPosnPerc_Open32', '0xA': ' CmdPosnPerc_Open36', '0xB': ' CmdPosnPerc_Open40', '0xC': ' CmdPosnPerc_Open44', '0xD': ' CmdPosnPerc_Open48', '0xE': ' CmdPosnPerc_Open52', '0xF': ' CmdPosnPerc_Open56', '0x10': ' CmdPosnPerc_Open60', '0x11': ' CmdPosnPerc_Open64', '0x12': ' CmdPosnPerc_Open68', '0x13': ' CmdPosnPerc_Open72', '0x14': ' CmdPosnPerc_Open76', '0x15': ' CmdPosnPerc_Open80', '0x16': ' CmdPosnPerc_Open84', '0x17': ' CmdPosnPerc_Open88', '0x18': ' CmdPosnPerc_Open92', '0x19': ' CmdPosnPerc_Open96', '0x1A': ' CmdPosnPerc_Open100', '0x1B': ' CmdPosnPerc_Stop', '0x1C': ' CmdPosnPerc_Resd2', '0x1D': ' CmdPosnPerc_Resd3', '0x1E': ' CmdPosnPerc_Resd4', '0x1F': ' CmdPosnPerc_Resd5'}

    class WinSrvOpenValueReqWinPassOpenValue:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Passenger Window Open Value"
        signal_length = 5
        start_position = 2
        value_definition = {'0x0': ' CmdPosnPerc_PosnUkwn', '0x1': ' CmdPosnPerc_Close', '0x2': ' CmdPosnPerc_Open4', '0x3': ' CmdPosnPerc_Open8', '0x4': ' CmdPosnPerc_Open12', '0x5': ' CmdPosnPerc_Open16', '0x6': ' CmdPosnPerc_Open20', '0x7': ' CmdPosnPerc_Open24', '0x8': ' CmdPosnPerc_Open28', '0x9': ' CmdPosnPerc_Open32', '0xA': ' CmdPosnPerc_Open36', '0xB': ' CmdPosnPerc_Open40', '0xC': ' CmdPosnPerc_Open44', '0xD': ' CmdPosnPerc_Open48', '0xE': ' CmdPosnPerc_Open52', '0xF': ' CmdPosnPerc_Open56', '0x10': ' CmdPosnPerc_Open60', '0x11': ' CmdPosnPerc_Open64', '0x12': ' CmdPosnPerc_Open68', '0x13': ' CmdPosnPerc_Open72', '0x14': ' CmdPosnPerc_Open76', '0x15': ' CmdPosnPerc_Open80', '0x16': ' CmdPosnPerc_Open84', '0x17': ' CmdPosnPerc_Open88', '0x18': ' CmdPosnPerc_Open92', '0x19': ' CmdPosnPerc_Open96', '0x1A': ' CmdPosnPerc_Open100', '0x1B': ' CmdPosnPerc_Stop', '0x1C': ' CmdPosnPerc_Resd2', '0x1D': ' CmdPosnPerc_Resd3', '0x1E': ' CmdPosnPerc_Resd4', '0x1F': ' CmdPosnPerc_Resd5'}


class CCUSOCCDToLCUREthSignalIPdu11:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x40600B
    pdu_length_bytes = 6
    receiver = ['LCUR']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {'CmptmtTempFlapPosnReq': ['CmptmtTempFlapPosnReqReRi', 'CmptmtTempFlapPosnReqReLe', 'CmptmtTempFlapPosnReqFrntRi', 'CmptmtTempFlapPosnReqFrntLe']}

    class CmptmtTempFlapPosnReqReRi:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Compartment Rear Right Area Temperature Flap Request Position"
        signal_length = 10
        start_position = 33
        value_definition = {}

    class CmptmtTempFlapPosnReqReLe:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Compartment Rear Left Area Temperature Flap Request Position"
        signal_length = 10
        start_position = 31
        value_definition = {}

    class CmptmtTempFlapPosnReqFrntRi:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Compartment Front Right Area Temperature Flap Request Position"
        signal_length = 10
        start_position = 9
        value_definition = {}

    class CmptmtTempFlapPosnReqFrntLe:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Compartment Front Left Area Temperature Flap Request Position"
        signal_length = 10
        start_position = 7
        value_definition = {}


class CCUSOCCDToLCUREthSignalIPdu10:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x40600A
    pdu_length_bytes = 6
    receiver = ['LCUR']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {'CmptmtModFlapPosnReq': ['CmptmtModFlapPosnReqReLe', 'CmptmtModFlapPosnReqFrntRi', 'CmptmtModFlapPosnReqFrntLe', 'CmptmtModFlapPosnReqReRi']}

    class CmptmtModFlapPosnReqReLe:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Compartment Rear Left Area Air Distribution Flap Request Position"
        signal_length = 10
        start_position = 31
        value_definition = {}

    class CmptmtModFlapPosnReqFrntRi:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Compartment Front Right Area Air Distribution Flap Request Position"
        signal_length = 10
        start_position = 9
        value_definition = {}

    class CmptmtModFlapPosnReqFrntLe:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Compartment Front Left Area Air Distribution Flap Request Position"
        signal_length = 10
        start_position = 7
        value_definition = {}

    class CmptmtModFlapPosnReqReRi:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Compartment Rear Right Area Air Distribution Flap Request Position"
        signal_length = 10
        start_position = 33
        value_definition = {}


class CCUSOCCDToLCUREthSignalIPdu13:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x40600D
    pdu_length_bytes = 1
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {}

    class PwrSideDoorModeSet:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "power side door mode set"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' DoorModSts_ElecMode', '0x1': ' DoorModSts_ManualMode'}


class CCUSOCCDToLCUREthSignalIPdu15:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x40600F
    pdu_length_bytes = 3
    receiver = ['LCUR']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {}

    class TiForBattLock:
        comments = ""
        factor = 1.0
        initial_value = 65535
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Time for Battery Lock"
        signal_length = 16
        start_position = 7
        value_definition = {}


class CCUSOCCDToLCUREthSignalIPdu12:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x40600C
    pdu_length_bytes = 1
    receiver = ['LCUR']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {}

    class PwrLockReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Battery Power Lock Requirement"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' ReqSts2_Default', '0x1': ' ReqSts2_NotReqd', '0x2': ' ReqSts2_Reqd', '0x3': ' ReqSts2_Reserved'}


class CCUSOCCDToLCUREthSignalIPdu16:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x406010
    pdu_length_bytes = 2
    receiver = ['LCUR']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {}

    class TiForBattUnLock:
        comments = ""
        factor = 1.0
        initial_value = 65535
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Time for Battery UnLock"
        signal_length = 16
        start_position = 7
        value_definition = {}


class CCUSOCCDToLCUREthSignalIPdu18:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x406012
    pdu_length_bytes = 1
    receiver = ['LCUR']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {}

    class AFURelsLvlReqFromSrv:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Air Fragrance Release Level Request From Service"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' ReqLvl_NoReq', '0x1': ' ReqLvl_LoReq', '0x2': ' ReqLvl_MidReq', '0x3': ' ReqLvl_HiReq'}


class CCUSOCCDToLCUREthSignalIPdu50:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x406032
    pdu_length_bytes = 1
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {}

    class GloveBoxCtrleq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "control request of glove box"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}


class CCUSOCCDToLCUREthSignalIPdu24:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x406018
    pdu_length_bytes = 4
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {'ConsoleMidRiALMRGBL': ['ConsoleMidRiALMRGBLRed', 'ConsoleMidRiALMRGBLBlue', 'ConsoleMidRiALMRGBLGreen', 'ConsoleMidRiALMRGBLLuminance']}

    class ConsoleMidRiALMRGBLRed:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Red,Console middle right alm"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class ConsoleMidRiALMRGBLBlue:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Blue,Console middle right alm"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class ConsoleMidRiALMRGBLGreen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Green,Console middle right alm"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class ConsoleMidRiALMRGBLLuminance:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Luminance,Console middle right alm"
        signal_length = 7
        start_position = 31
        value_definition = {}


class CCUSOCCDToLCUREthSignalIPdu64:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x406040
    pdu_length_bytes = 1
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {}

    class RiChdLockCtrlReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "right children lock control request "
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' LockCmd_Idle', '0x1': ' LockCmd_LockCmd', '0x2': ' LockCmd_UnLockCmd', '0x3': ' LockCmd_CrashUnLockCmd'}


class CCUSOCCDToLCUREthSignalIPdu19:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x406013
    pdu_length_bytes = 1
    receiver = ['LCUR']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {}

    class AGUActvReqFromSrv:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Anion Generator Active Request  From Service"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}


class CCUSOCCDToLCUREthSignalIPdu78:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x40604E
    pdu_length_bytes = 1
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {}

    class SeatLumReqReRi:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Lumbar Request"
        signal_length = 7
        start_position = 7
        value_definition = {'0x0': ' SeatLumCmd_Idle', '0x1': ' SeatLumCmd_Up', '0x2': ' SeatLumCmd_Down', '0x3': ' SeatLumCmd_Foreward', '0x4': ' SeatLumCmd_Backward', '0x5': ' SeatLumCmd_resd1', '0x6': ' SeatLumCmd_resd2', '0x7': ' SeatLumCmd_resd3'}


class CCUSOCCDToLCUREthSignalIPdu21:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x406015
    pdu_length_bytes = 4
    receiver = ['LCUR']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {'CmptmtBlwrPwmReq': ['CmptmtBlwrPwmReqRe', 'CmptmtBlwrPwmReqBoost', 'CmptmtBlwrPwmReqFrnt']}

    class CmptmtBlwrPwmReqRe:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Compartment Rear Blower Pwm Request"
        signal_length = 10
        start_position = 7
        value_definition = {}

    class CmptmtBlwrPwmReqBoost:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Compartment Booster Blower Pwm Request"
        signal_length = 10
        start_position = 13
        value_definition = {}

    class CmptmtBlwrPwmReqFrnt:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Compartment Front Blower Pwm Request"
        signal_length = 10
        start_position = 19
        value_definition = {}


class CCUSOCCDToLCUREthSignalIPdu77:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x40604D
    pdu_length_bytes = 1
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {}

    class SeatLumReqFrntRi:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Lumbar Request"
        signal_length = 7
        start_position = 7
        value_definition = {'0x0': ' SeatLumCmd_Idle', '0x1': ' SeatLumCmd_Up', '0x2': ' SeatLumCmd_Down', '0x3': ' SeatLumCmd_Foreward', '0x4': ' SeatLumCmd_Backward', '0x5': ' SeatLumCmd_resd1', '0x6': ' SeatLumCmd_resd2', '0x7': ' SeatLumCmd_resd3'}


class CCUSOCCDToLCUREthSignalIPdu30:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x40601E
    pdu_length_bytes = 4
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {'DoorArmrestFrntRiALMRGBL': ['DoorArmrestFrntRiALMRGBLBlue', 'DoorArmrestFrntRiALMRGBLRed', 'DoorArmrestFrntRiALMRGBLLuminance', 'DoorArmrestFrntRiALMRGBLGreen']}

    class DoorArmrestFrntRiALMRGBLBlue:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Blue,DoorArmrestFrntRiALMRGBL"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class DoorArmrestFrntRiALMRGBLRed:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Red,DoorArmrestFrntRiALMRGBL"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class DoorArmrestFrntRiALMRGBLLuminance:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Luminance,DoorArmrestFrntRiALMRGBL"
        signal_length = 7
        start_position = 23
        value_definition = {}

    class DoorArmrestFrntRiALMRGBLGreen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Green,DoorArmrestFrntRiALMRGBL"
        signal_length = 8
        start_position = 31
        value_definition = {}


class CCUSOCCDToLCUREthSignalIPdu75:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x40604B
    pdu_length_bytes = 1
    receiver = ['LCUR']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {}

    class SeatAdjRi3RowAntiPinchEna:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Antipinch Enable or Disable"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' EnableDisable4_NoCmd', '0x1': ' EnableDisable4_Disable', '0x2': ' EnableDisable4_Enable'}


class CCUSOCCDToLCUREthSignalIPdu35:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x406023
    pdu_length_bytes = 4
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {'DoorRearRiALMRGBL': ['DoorRearRiALMRGBLBlue', 'DoorRearRiALMRGBLRed', 'DoorRearRiALMRGBLLuminance', 'DoorRearRiALMRGBLGreen']}

    class DoorRearRiALMRGBLBlue:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Blue,DoorRearRiALMRGBL"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class DoorRearRiALMRGBLRed:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Red,DoorRearRiALMRGBL"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class DoorRearRiALMRGBLLuminance:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Luminance,DoorRearRiALMRGBL"
        signal_length = 7
        start_position = 23
        value_definition = {}

    class DoorRearRiALMRGBLGreen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Green,DoorRearRiALMRGBL"
        signal_length = 8
        start_position = 31
        value_definition = {}


class CCUSOCCDToLCUREthSignalIPdu51:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x406033
    pdu_length_bytes = 2
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {'InnerLightingIllumSeln': ['InnerLightingIllumSelnReadingLiDimsSpdCmd', 'InnerLightingIllumSelnLiPerc']}

    class InnerLightingIllumSelnReadingLiDimsSpdCmd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "dim speed of the innerlighting illumination"
        signal_length = 3
        start_position = 7
        value_definition = {'0x0': ' ReadingLiDimsSpdCmd_NoCmd', '0x1': ' ReadingLiDimsSpdCmd_400ms', '0x2': ' ReadingLiDimsSpdCmd_800ms', '0x3': ' ReadingLiDimsSpdCmd_1000ms', '0x4': ' ReadingLiDimsSpdCmd_2000ms', '0x5': ' ReadingLiDimsSpdCmd_Resverd'}

    class InnerLightingIllumSelnLiPerc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "brightness percent"
        signal_length = 7
        start_position = 4
        value_definition = {}


class CCUSOCCDToLCUREthSignalIPdu66:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x406042
    pdu_length_bytes = 4
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {'RoofLeALMRGBL': ['RoofLeALMRGBLBlue', 'RoofLeALMRGBLLuminance', 'RoofLeALMRGBLRed', 'RoofLeALMRGBLGreen']}

    class RoofLeALMRGBLBlue:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Blue,RoofLeALMRGBL"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class RoofLeALMRGBLLuminance:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Luminance,RoofLeALMRGBL"
        signal_length = 7
        start_position = 15
        value_definition = {}

    class RoofLeALMRGBLRed:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Red,RoofLeALMRGBL"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class RoofLeALMRGBLGreen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Green,RoofLeALMRGBL"
        signal_length = 8
        start_position = 31
        value_definition = {}


class CCUSOCCDToLCUREthSignalIPdu33:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x406021
    pdu_length_bytes = 4
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {'DoorMapBeltFrntRiALMRGBL': ['DoorMapBeltFrntRiALMRGBLBlue', 'DoorMapBeltFrntRiALMRGBLRed', 'DoorMapBeltFrntRiALMRGBLLuminance', 'DoorMapBeltFrntRiALMRGBLGreen']}

    class DoorMapBeltFrntRiALMRGBLBlue:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Blue,DoorMapBeltFrntRiALMRGBL"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class DoorMapBeltFrntRiALMRGBLRed:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Red,DoorMapBeltFrntRiALMRGBL"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class DoorMapBeltFrntRiALMRGBLLuminance:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Luminance,DoorMapBeltFrntRiALMRGBL"
        signal_length = 7
        start_position = 23
        value_definition = {}

    class DoorMapBeltFrntRiALMRGBLGreen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Green,DoorMapBeltFrntRiALMRGBL"
        signal_length = 8
        start_position = 31
        value_definition = {}


class CCUSOCCDToLCUREthSignalIPdu65:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x406041
    pdu_length_bytes = 1
    receiver = ['LCUR']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {}

    class RiSpkrRiseOrFallCtrl:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "The Right Speaker Elevating Command"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' RiseOrFallControl_Stop', '0x1': ' RiseOrFallControl_Rise', '0x2': ' RiseOrFallControl_Fall', '0x3': ' RiseOrFallControl_Reserved'}


class CCUSOCCDToLCUREthSignalIPdu84:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x406054
    pdu_length_bytes = 4
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {'TweeterRiALMRGBL': ['TweeterRiALMRGBLBlue', 'TweeterRiALMRGBLRed', 'TweeterRiALMRGBLLuminance', 'TweeterRiALMRGBLGreen']}

    class TweeterRiALMRGBLBlue:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Blue,tweeter right alm"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class TweeterRiALMRGBLRed:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Red,tweeter right alm"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class TweeterRiALMRGBLLuminance:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Luminance,,tweeter right alm"
        signal_length = 7
        start_position = 23
        value_definition = {}

    class TweeterRiALMRGBLGreen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Green,tweeter right alm"
        signal_length = 8
        start_position = 31
        value_definition = {}


class CCUSOCCDToLCUREthSignalIPdu22:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x406016
    pdu_length_bytes = 2
    receiver = ['LCUR']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {}

    class CmptmtFreshFlapPosnReq:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Compartment Fresh Flap Request Position"
        signal_length = 10
        start_position = 7
        value_definition = {}


class CCUSOCCDToLCUREthSignalIPdu76:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x40604C
    pdu_length_bytes = 9
    receiver = ['LCUR']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {'SeatClimaRiReqFromSrv': ['SeatClimaRiReqFromSrvHeatgTSet3Row', 'SeatClimaRiReqFromSrvHeatgOnOff2Row', 'SeatClimaRiReqFromSrvVentPwmSet3Row', 'SeatClimaRiReqFromSrvVentOnOff3Row', 'SeatClimaRiReqFromSrvVentPwmSet2Row', 'SeatClimaRiReqFromSrvHeatgOnOff1Row', 'SeatClimaRiReqFromSrvVentOnOff1Row', 'SeatClimaRiReqFromSrvHeatgTSet2Row', 'SeatClimaRiReqFromSrvHeatgTSet1Row', 'SeatClimaRiReqFromSrvVentPwmSet1Row', 'SeatClimaRiReqFromSrvVentOnOff2Row', 'SeatClimaRiReqFromSrvHeatgOnOff3Row']}

    class SeatClimaRiReqFromSrvHeatgTSet3Row:
        comments = ""
        factor = 0.1
        initial_value = 400
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -40
        sig_ub = None
        signal_description = "Third Row Right Side Seat Heating Temperature Setting From Service"
        signal_length = 11
        start_position = 7
        value_definition = {}

    class SeatClimaRiReqFromSrvHeatgOnOff2Row:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Second Row Right Side Seat Heating On-Off Setting From Service"
        signal_length = 1
        start_position = 12
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class SeatClimaRiReqFromSrvVentPwmSet3Row:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Third Row Right Side Seat Venting Pwm Setting From Service"
        signal_length = 10
        start_position = 11
        value_definition = {}

    class SeatClimaRiReqFromSrvVentOnOff3Row:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Third Row Right Side Seat Venting On-Off Setting From Service"
        signal_length = 1
        start_position = 17
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class SeatClimaRiReqFromSrvVentPwmSet2Row:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Second Row Right Side Seat Venting Pwm Setting From Service"
        signal_length = 10
        start_position = 16
        value_definition = {}

    class SeatClimaRiReqFromSrvHeatgOnOff1Row:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "First Row Right Side Seat Heating On-Off Setting From Service"
        signal_length = 1
        start_position = 38
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class SeatClimaRiReqFromSrvVentOnOff1Row:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "First Row Right Side Seat Venting On-Off Setting From Service"
        signal_length = 1
        start_position = 37
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class SeatClimaRiReqFromSrvHeatgTSet2Row:
        comments = ""
        factor = 0.1
        initial_value = 400
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -40
        sig_ub = None
        signal_description = "Second Row Right Side Seat Heating Temperature Setting From Service"
        signal_length = 11
        start_position = 36
        value_definition = {}

    class SeatClimaRiReqFromSrvHeatgTSet1Row:
        comments = ""
        factor = 0.1
        initial_value = 400
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -40
        sig_ub = None
        signal_description = "First Row Right Side Seat Heating Temperature Setting From Service"
        signal_length = 11
        start_position = 41
        value_definition = {}

    class SeatClimaRiReqFromSrvVentPwmSet1Row:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "First Row Right Side Seat Venting Pwm Setting From Service"
        signal_length = 10
        start_position = 62
        value_definition = {}

    class SeatClimaRiReqFromSrvVentOnOff2Row:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Second Row Right Side Seat Venting On-Off Setting From Service"
        signal_length = 1
        start_position = 68
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class SeatClimaRiReqFromSrvHeatgOnOff3Row:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Third Row Right Side Seat Heating On-Off Setting From Service"
        signal_length = 1
        start_position = 67
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}


class CCUSOCCDToLCUREthSignalIPdu32:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x406020
    pdu_length_bytes = 4
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {'DoorFrntRiALMRGBL': ['DoorFrntRiALMRGBLBlue', 'DoorFrntRiALMRGBLGreen', 'DoorFrntRiALMRGBLRed', 'DoorFrntRiALMRGBLLuminance']}

    class DoorFrntRiALMRGBLBlue:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Blue,DoorFrntRiALMRGBL"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class DoorFrntRiALMRGBLGreen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Green,DoorFrntRiALMRGBL"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class DoorFrntRiALMRGBLRed:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Red,DoorFrntRiALMRGBL"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class DoorFrntRiALMRGBLLuminance:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Luminance,DoorFrntRiALMRGBL"
        signal_length = 7
        start_position = 31
        value_definition = {}


class CCUSOCCDToLCUREthSignalIPdu38:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x406026
    pdu_length_bytes = 1
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {}

    class ExtrReViewMirrFoldRemCmdPass:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Automatic folding command for external rear view mirror at passenger side"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' MirrFodCmd_Idle', '0x1': ' MirrFodCmd_Fold', '0x2': ' MirrFodCmd_Unfold'}


class CCUSOCCDToLCUREthSignalIPdu80:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x406050
    pdu_length_bytes = 1
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {'SeatMassgReqReRi': ['SeatMassgReqReRiMassgProg', 'SeatMassgReqReRiReqLvl']}

    class SeatMassgReqReRiMassgProg:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Massage Type"
        signal_length = 3
        start_position = 7
        value_definition = {'0x0': ' MassgProg_Prog0', '0x1': ' MassgProg_Prog1', '0x2': ' MassgProg_Prog2', '0x3': ' MassgProg_Prog3', '0x4': ' MassgProg_Prog4', '0x5': ' MassgProg_Prog5', '0x6': ' MassgProg_Prog6', '0x7': ' MassgProg_Prog7'}

    class SeatMassgReqReRiReqLvl:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Massage Intensity Level Request"
        signal_length = 2
        start_position = 4
        value_definition = {'0x0': ' ReqLvl_NoReq', '0x1': ' ReqLvl_LoReq', '0x2': ' ReqLvl_MidReq', '0x3': ' ReqLvl_HiReq'}


class CCUSOCCDToLCUREthSignalIPdu70:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x406046
    pdu_length_bytes = 4
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {'SeatAdj1RowRiReq': ['SeatAdj1RowRiReqMotorCtrlOTTOLen', 'SeatAdj1RowRiReqMotorCtrlCLA', 'SeatAdj1RowRiReqMotorCtrlTilt', 'SeatAdj1RowRiReqMotorCtrlOTTOAg', 'SeatAdj1RowRiReqMotorCtrlRe', 'SeatAdj1RowRiReqMotorCtrlHei', 'SeatAdj1RowRiReqMotorCtrlLen', 'SeatAdj1RowRiReqMotorCtrlOTF', 'SeatAdj1RowRiReqMotorCtrlBack']}

    class SeatAdj1RowRiReqMotorCtrlOTTOLen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Motr Control"
        signal_length = 3
        start_position = 7
        value_definition = {'0x0': ' MotorCtrl_Idle', '0x1': ' MotorCtrl_RunningUp', '0x2': ' MotorCtrl_RunningDown', '0x3': ' MotorCtrl_Stop', '0x4': ' MotorCtrl_Reserved1', '0x5': ' MotorCtrl_Reserved2', '0x6': ' MotorCtrl_Reserved3', '0x7': ' MotorCtrl_Reserved4'}

    class SeatAdj1RowRiReqMotorCtrlCLA:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Motr Control"
        signal_length = 3
        start_position = 4
        value_definition = {'0x0': ' MotorCtrl_Idle', '0x1': ' MotorCtrl_RunningUp', '0x2': ' MotorCtrl_RunningDown', '0x3': ' MotorCtrl_Stop', '0x4': ' MotorCtrl_Reserved1', '0x5': ' MotorCtrl_Reserved2', '0x6': ' MotorCtrl_Reserved3', '0x7': ' MotorCtrl_Reserved4'}

    class SeatAdj1RowRiReqMotorCtrlTilt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Motr Control"
        signal_length = 3
        start_position = 1
        value_definition = {'0x0': ' MotorCtrl_Idle', '0x1': ' MotorCtrl_RunningUp', '0x2': ' MotorCtrl_RunningDown', '0x3': ' MotorCtrl_Stop', '0x4': ' MotorCtrl_Reserved1', '0x5': ' MotorCtrl_Reserved2', '0x6': ' MotorCtrl_Reserved3', '0x7': ' MotorCtrl_Reserved4'}

    class SeatAdj1RowRiReqMotorCtrlOTTOAg:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Motr Control"
        signal_length = 3
        start_position = 14
        value_definition = {'0x0': ' MotorCtrl_Idle', '0x1': ' MotorCtrl_RunningUp', '0x2': ' MotorCtrl_RunningDown', '0x3': ' MotorCtrl_Stop', '0x4': ' MotorCtrl_Reserved1', '0x5': ' MotorCtrl_Reserved2', '0x6': ' MotorCtrl_Reserved3', '0x7': ' MotorCtrl_Reserved4'}

    class SeatAdj1RowRiReqMotorCtrlRe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Motr Control"
        signal_length = 3
        start_position = 11
        value_definition = {'0x0': ' MotorCtrl_Idle', '0x1': ' MotorCtrl_RunningUp', '0x2': ' MotorCtrl_RunningDown', '0x3': ' MotorCtrl_Stop', '0x4': ' MotorCtrl_Reserved1', '0x5': ' MotorCtrl_Reserved2', '0x6': ' MotorCtrl_Reserved3', '0x7': ' MotorCtrl_Reserved4'}

    class SeatAdj1RowRiReqMotorCtrlHei:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Motr Control"
        signal_length = 3
        start_position = 8
        value_definition = {'0x0': ' MotorCtrl_Idle', '0x1': ' MotorCtrl_RunningUp', '0x2': ' MotorCtrl_RunningDown', '0x3': ' MotorCtrl_Stop', '0x4': ' MotorCtrl_Reserved1', '0x5': ' MotorCtrl_Reserved2', '0x6': ' MotorCtrl_Reserved3', '0x7': ' MotorCtrl_Reserved4'}

    class SeatAdj1RowRiReqMotorCtrlLen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Motr Control"
        signal_length = 3
        start_position = 21
        value_definition = {'0x0': ' MotorCtrl_Idle', '0x1': ' MotorCtrl_RunningUp', '0x2': ' MotorCtrl_RunningDown', '0x3': ' MotorCtrl_Stop', '0x4': ' MotorCtrl_Reserved1', '0x5': ' MotorCtrl_Reserved2', '0x6': ' MotorCtrl_Reserved3', '0x7': ' MotorCtrl_Reserved4'}

    class SeatAdj1RowRiReqMotorCtrlOTF:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Motr Control"
        signal_length = 3
        start_position = 18
        value_definition = {'0x0': ' MotorCtrl_Idle', '0x1': ' MotorCtrl_RunningUp', '0x2': ' MotorCtrl_RunningDown', '0x3': ' MotorCtrl_Stop', '0x4': ' MotorCtrl_Reserved1', '0x5': ' MotorCtrl_Reserved2', '0x6': ' MotorCtrl_Reserved3', '0x7': ' MotorCtrl_Reserved4'}

    class SeatAdj1RowRiReqMotorCtrlBack:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Motr Control"
        signal_length = 3
        start_position = 31
        value_definition = {'0x0': ' MotorCtrl_Idle', '0x1': ' MotorCtrl_RunningUp', '0x2': ' MotorCtrl_RunningDown', '0x3': ' MotorCtrl_Stop', '0x4': ' MotorCtrl_Reserved1', '0x5': ' MotorCtrl_Reserved2', '0x6': ' MotorCtrl_Reserved3', '0x7': ' MotorCtrl_Reserved4'}


class CCUSOCCDToLCUREthSignalIPdu85:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x406055
    pdu_length_bytes = 4
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {'TweeterRiBotmALMRGBL': ['TweeterRiBotmALMRGBLRed', 'TweeterRiBotmALMRGBLGreen', 'TweeterRiBotmALMRGBLBlue', 'TweeterRiBotmALMRGBLLuminance']}

    class TweeterRiBotmALMRGBLRed:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Red,TweeterRiBotmALMRGBL"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class TweeterRiBotmALMRGBLGreen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Green,TweeterRiBotmALMRGBL"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class TweeterRiBotmALMRGBLBlue:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Blue,TweeterRiBotmALMRGBL"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class TweeterRiBotmALMRGBLLuminance:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Luminance,TweeterRiBotmALMRGBL"
        signal_length = 7
        start_position = 31
        value_definition = {}


class CCUSOCCDToLCUREthSignalIPdu43:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x40602B
    pdu_length_bytes = 1
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {}

    class FRPwrSideDoorMaxPosnSet:
        comments = ""
        factor = 1.0
        initial_value = 101
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "power side door Max position set"
        signal_length = 8
        start_position = 7
        value_definition = {}


class CCUSOCCDToLCUREthSignalIPdu25:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x406019
    pdu_length_bytes = 4
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {'ConsoleOShapeALMRGBL': ['ConsoleOShapeALMRGBLGreen', 'ConsoleOShapeALMRGBLLuminance', 'ConsoleOShapeALMRGBLRed', 'ConsoleOShapeALMRGBLBlue']}

    class ConsoleOShapeALMRGBLGreen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Green,ConsoleOShapeALMRGBL"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class ConsoleOShapeALMRGBLLuminance:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Luminance,ConsoleOShapeALMRGBL"
        signal_length = 7
        start_position = 15
        value_definition = {}

    class ConsoleOShapeALMRGBLRed:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Red,ConsoleOShapeALMRGBL"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class ConsoleOShapeALMRGBLBlue:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Blue,ConsoleOShapeALMRGBL"
        signal_length = 8
        start_position = 31
        value_definition = {}


class CCUSOCCDToLCUREthSignalIPdu82:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x406052
    pdu_length_bytes = 1
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {}

    class TrMaxPosnSet:
        comments = ""
        factor = 1.0
        initial_value = 101
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "trunk max position set"
        signal_length = 8
        start_position = 7
        value_definition = {}


class CCUSOCCDToLCUREthSignalIPdu60:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x40603C
    pdu_length_bytes = 2
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {'ReadingLiThrRowLeAdjReq': ['ReadingLiThrRowLeAdjReqLiPerc', 'ReadingLiThrRowLeAdjReqLightCmd', 'ReadingLiThrRowLeAdjReqReadingLiDimsSpdCmd']}

    class ReadingLiThrRowLeAdjReqLiPerc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "adjustment command of the  front left reading light intensity "
        signal_length = 7
        start_position = 7
        value_definition = {}

    class ReadingLiThrRowLeAdjReqLightCmd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "mode req of 3rd L"
        signal_length = 4
        start_position = 0
        value_definition = {'0x0': ' LightCmd_NoReq', '0x1': ' LightCmd_ON', '0x2': ' LightCmd_OFF', '0x3': ' LightCmd_TBD'}

    class ReadingLiThrRowLeAdjReqReadingLiDimsSpdCmd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "adjustment speed command of the  front left reading light intensity "
        signal_length = 3
        start_position = 12
        value_definition = {'0x0': ' ReadingLiDimsSpdCmd_NoCmd', '0x1': ' ReadingLiDimsSpdCmd_400ms', '0x2': ' ReadingLiDimsSpdCmd_800ms', '0x3': ' ReadingLiDimsSpdCmd_1000ms', '0x4': ' ReadingLiDimsSpdCmd_2000ms', '0x5': ' ReadingLiDimsSpdCmd_Resverd'}


class CCUSOCCDToLCUREthSignalIPdu34:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x406022
    pdu_length_bytes = 4
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {'DoorMapBeltRearRiALMRGBL': ['DoorMapBeltRearRiALMRGBLGreen', 'DoorMapBeltRearRiALMRGBLLuminance', 'DoorMapBeltRearRiALMRGBLRed', 'DoorMapBeltRearRiALMRGBLBlue']}

    class DoorMapBeltRearRiALMRGBLGreen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Green,DoorMapBeltRearRiALMRGBL"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class DoorMapBeltRearRiALMRGBLLuminance:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Luminance,DoorMapBeltRearRiALMRGBL"
        signal_length = 7
        start_position = 15
        value_definition = {}

    class DoorMapBeltRearRiALMRGBLRed:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Red,DoorMapBeltRearRiALMRGBL"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class DoorMapBeltRearRiALMRGBLBlue:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Blue,DoorMapBeltRearRiALMRGBL"
        signal_length = 8
        start_position = 31
        value_definition = {}


class CCUSOCCDToLCUREthSignalIPdu81:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x406051
    pdu_length_bytes = 1
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {}

    class SwivelingMotorEn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "MotorEnableDisable"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' EnableDisable2_Disabled', '0x1': ' EnableDisable2_Enabled'}


class CCUSOCCDToLCUREthSignalIPdu67:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x406043
    pdu_length_bytes = 4
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {'RoofRiALMRGBL': ['RoofRiALMRGBLBlue', 'RoofRiALMRGBLLuminance', 'RoofRiALMRGBLGreen', 'RoofRiALMRGBLRed']}

    class RoofRiALMRGBLBlue:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Blue,RoofRiALMRGBL"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class RoofRiALMRGBLLuminance:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Luminance,RoofRiALMRGBL"
        signal_length = 7
        start_position = 15
        value_definition = {}

    class RoofRiALMRGBLGreen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Green,RoofRiALMRGBL"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class RoofRiALMRGBLRed:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Red,RoofRiALMRGBL"
        signal_length = 8
        start_position = 31
        value_definition = {}


class CCUSOCCDToLCUREthSignalIPdu29:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x40601D
    pdu_length_bytes = 1
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {}

    class DefrstPassCmd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "defrosting command of the passenger side mirror"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' OffOnCmd_NoCmd', '0x1': ' OffOnCmd_Off', '0x2': ' OffOnCmd_On'}


class CCUSOCCDToLCUREthSignalIPdu63:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x40603F
    pdu_length_bytes = 1
    receiver = ['LCUR']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {}

    class ReWiprForSrvReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "the requestion for rear wiper service "
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' OnOffNoCmd_NoCmd', '0x1': ' OnOffNoCmd_OFF', '0x2': ' OnOffNoCmd_ON'}


class CCUSOCCDToLCUREthSignalIPdu39:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x406027
    pdu_length_bytes = 2
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {'ExtrReViewMirrTarAdjCmdPass': ['ExtrReViewMirrTarAdjCmdPassUpAndDown', 'ExtrReViewMirrTarAdjCmdPassLeAndRi']}

    class ExtrReViewMirrTarAdjCmdPassUpAndDown:
        comments = ""
        factor = 1.0
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "目标外后视镜位置调用"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class ExtrReViewMirrTarAdjCmdPassLeAndRi:
        comments = ""
        factor = 1.0
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "目标外后视镜位置调用"
        signal_length = 8
        start_position = 15
        value_definition = {}


class CCUSOCCDToLCUREthSignalIPdu79:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x40604F
    pdu_length_bytes = 1
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {'SeatMassgReqFrntRi': ['SeatMassgReqFrntRiReqLvl', 'SeatMassgReqFrntRiMassgProg']}

    class SeatMassgReqFrntRiReqLvl:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Massage Intensity Level Request"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' ReqLvl_NoReq', '0x1': ' ReqLvl_LoReq', '0x2': ' ReqLvl_MidReq', '0x3': ' ReqLvl_HiReq'}

    class SeatMassgReqFrntRiMassgProg:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Massage Type"
        signal_length = 3
        start_position = 5
        value_definition = {'0x0': ' MassgProg_Prog0', '0x1': ' MassgProg_Prog1', '0x2': ' MassgProg_Prog2', '0x3': ' MassgProg_Prog3', '0x4': ' MassgProg_Prog4', '0x5': ' MassgProg_Prog5', '0x6': ' MassgProg_Prog6', '0x7': ' MassgProg_Prog7'}


class CCUSOCCDToLCUREthSignalIPdu68:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x406044
    pdu_length_bytes = 1
    receiver = ['LCUR']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {}

    class RRDoorManResistCtrl:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Door manual resistance control"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' DoorManResistCmd_Idle', '0x1': ' DoorManResistCmd_AddLevel1Cmd', '0x2': ' DoorManResistCmd_AddLevel2Cmd', '0x3': ' DoorManResistCmd_SubCmd'}


class CCUSOCCDToLCUREthSignalIPdu69:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x406045
    pdu_length_bytes = 1
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {}

    class RRPwrSideDoorMaxPosnSet:
        comments = ""
        factor = 1.0
        initial_value = 101
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "power side door Max position set"
        signal_length = 8
        start_position = 7
        value_definition = {}


class CCUSOCCDToLCUREthSignalIPdu49:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x406031
    pdu_length_bytes = 2
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {'FuncReqOfReverseLamp': ['FuncReqOfReverseLampLightPriority', 'FuncReqOfReverseLampLightID1', 'FuncReqOfReverseLampLightCmd']}

    class FuncReqOfReverseLampLightPriority:
        comments = ""
        factor = 1.0
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "LightPriority"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class FuncReqOfReverseLampLightID1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "LightID"
        signal_length = 4
        start_position = 15
        value_definition = {'0x0': ' LightID1_ALL', '0x1': ' LightID1_Front', '0x2': ' LightID1_Rear', '0x3': ' LightID1_LeftFrontLeftRearLeft', '0x4': ' LightID1_RightFrontRightRearRight', '0x5': ' LightID1_FrontLeft', '0x6': ' LightID1_FrontRight', '0x7': ' LightID1_RearLeft', '0x8': ' LightID1_FrontLeftRearRight', '0x9': ' LightID1_FrontRightRearLeft', '0xA': ' LightID1_ExceptFrontLeft', '0xB': ' LightID1_ExceptFrontRight', '0xC': ' LightID1_ExceptRearLeft', '0xD': ' LightID1_ExceptRearRight', '0xE': ' LightID1_Reserved1', '0xF': ' LightID1_Reserved2'}

    class FuncReqOfReverseLampLightCmd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "LightCmd"
        signal_length = 4
        start_position = 11
        value_definition = {'0x0': ' LightCmd_NoReq', '0x1': ' LightCmd_ON', '0x2': ' LightCmd_OFF', '0x3': ' LightCmd_TBD'}


class CCUSOCCDToLCUREthSignalIPdu40:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x406028
    pdu_length_bytes = 4
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {'FootwellFirstRiALMRGBL': ['FootwellFirstRiALMRGBLBlue', 'FootwellFirstRiALMRGBLRed', 'FootwellFirstRiALMRGBLGreen', 'FootwellFirstRiALMRGBLLuminance']}

    class FootwellFirstRiALMRGBLBlue:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Blue,FootwellFirstRiALMRGBL"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class FootwellFirstRiALMRGBLRed:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Red,FootwellFirstRiALMRGBL"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class FootwellFirstRiALMRGBLGreen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Green,FootwellFirstRiALMRGBL"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class FootwellFirstRiALMRGBLLuminance:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Luminance,FootwellFirstRiALMRGBL"
        signal_length = 7
        start_position = 31
        value_definition = {}


class CCUSOCCDToLCUREthSignalIPdu48:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x406030
    pdu_length_bytes = 2
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {'FuncReqOfRearFogLamp': ['FuncReqOfRearFogLampLightCmd', 'FuncReqOfRearFogLampLightID1', 'FuncReqOfRearFogLampLightPriority']}

    class FuncReqOfRearFogLampLightCmd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "LightCmd"
        signal_length = 4
        start_position = 7
        value_definition = {'0x0': ' LightCmd_NoReq', '0x1': ' LightCmd_ON', '0x2': ' LightCmd_OFF', '0x3': ' LightCmd_TBD'}

    class FuncReqOfRearFogLampLightID1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "LightID"
        signal_length = 4
        start_position = 3
        value_definition = {'0x0': ' LightID1_ALL', '0x1': ' LightID1_Front', '0x2': ' LightID1_Rear', '0x3': ' LightID1_LeftFrontLeftRearLeft', '0x4': ' LightID1_RightFrontRightRearRight', '0x5': ' LightID1_FrontLeft', '0x6': ' LightID1_FrontRight', '0x7': ' LightID1_RearLeft', '0x8': ' LightID1_FrontLeftRearRight', '0x9': ' LightID1_FrontRightRearLeft', '0xA': ' LightID1_ExceptFrontLeft', '0xB': ' LightID1_ExceptFrontRight', '0xC': ' LightID1_ExceptRearLeft', '0xD': ' LightID1_ExceptRearRight', '0xE': ' LightID1_Reserved1', '0xF': ' LightID1_Reserved2'}

    class FuncReqOfRearFogLampLightPriority:
        comments = ""
        factor = 1.0
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "LightPriority"
        signal_length = 8
        start_position = 15
        value_definition = {}


class CCUSOCCDToLCUREthSignalIPdu52:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x406034
    pdu_length_bytes = 1
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {}

    class InnerLightingModSeln:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "the select mode of the interior lamp"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' IntrLampSelnMod_NoCmd', '0x1': ' IntrLampSelnMod_OFF', '0x2': ' IntrLampSelnMod_ON', '0x3': ' IntrLampSelnMod_AUTO'}


class CCUSOCCDToLCUREthSignalIPdu27:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x40601B
    pdu_length_bytes = 4
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {'CpilRiALMRGBL': ['CpilRiALMRGBLRed', 'CpilRiALMRGBLLuminance', 'CpilRiALMRGBLBlue', 'CpilRiALMRGBLGreen']}

    class CpilRiALMRGBLRed:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Red,CpilRiALMRGBL"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class CpilRiALMRGBLLuminance:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Luminance,CpilRiALMRGBL"
        signal_length = 7
        start_position = 15
        value_definition = {}

    class CpilRiALMRGBLBlue:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Blue,CpilRiALMRGBL"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class CpilRiALMRGBLGreen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Green,CpilRiALMRGBL"
        signal_length = 8
        start_position = 31
        value_definition = {}


class CCUSOCCDToLCUREthSignalIPdu37:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x406025
    pdu_length_bytes = 1
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {}

    class ExtrReViewMirrFoldManCmdPass:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "manual folding command for external rear view mirror at passenger side"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' MirrFodCmd_Idle', '0x1': ' MirrFodCmd_Fold', '0x2': ' MirrFodCmd_Unfold'}


class CCUSOCCDToLCUREthSignalIPdu73:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x406049
    pdu_length_bytes = 1
    receiver = ['LCUR']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {}

    class SeatAdjRi1RowAntiPinchEna:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Antipinch Enable or Disable"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' EnableDisable4_NoCmd', '0x1': ' EnableDisable4_Disable', '0x2': ' EnableDisable4_Enable'}


class CCUSOCCDToLCUREthSignalIPdu54:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x406036
    pdu_length_bytes = 1
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {}

    class LevelingMotorDynamicEn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "MotorEnableDisable"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' EnableDisable2_Disabled', '0x1': ' EnableDisable2_Enabled'}


class CCUSOCCDToLCUREthSignalIPdu86:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x406056
    pdu_length_bytes = 4
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {'TweeterRiMidALMRGBL': ['TweeterRiMidALMRGBLBlue', 'TweeterRiMidALMRGBLRed', 'TweeterRiMidALMRGBLLuminance', 'TweeterRiMidALMRGBLGreen']}

    class TweeterRiMidALMRGBLBlue:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Blue,TweeterRiMidALMRGBL"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class TweeterRiMidALMRGBLRed:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Red,TweeterRiMidALMRGBL"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class TweeterRiMidALMRGBLLuminance:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Luminance,TweeterRiMidALMRGBL"
        signal_length = 7
        start_position = 23
        value_definition = {}

    class TweeterRiMidALMRGBLGreen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Green,TweeterRiMidALMRGBL"
        signal_length = 8
        start_position = 31
        value_definition = {}


class CCUSOCCDToLCUREthSignalIPdu53:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x406035
    pdu_length_bytes = 1
    receiver = ['LCUR']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {}

    class InsdAirPM25ActvReqFromSrv:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Inside Air PM2.5 Active Request From Service"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}


class CCUSOCCDToLCUREthSignalIPdu31:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x40601F
    pdu_length_bytes = 4
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {'DoorArmrestRearRiALMRGBL': ['DoorArmrestRearRiALMRGBLGreen', 'DoorArmrestRearRiALMRGBLLuminance', 'DoorArmrestRearRiALMRGBLBlue', 'DoorArmrestRearRiALMRGBLRed']}

    class DoorArmrestRearRiALMRGBLGreen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Green,.DoorArmrestRearRiALMRGBL"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class DoorArmrestRearRiALMRGBLLuminance:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Luminance,DoorArmrestRearRiALMRGBL"
        signal_length = 7
        start_position = 15
        value_definition = {}

    class DoorArmrestRearRiALMRGBLBlue:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Blue,DoorArmrestRearRiALMRGBL"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class DoorArmrestRearRiALMRGBLRed:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Red,DoorArmrestRearRiALMRGBL"
        signal_length = 8
        start_position = 31
        value_definition = {}


class CCUSOCCDToLCUREthSignalIPdu62:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x40603E
    pdu_length_bytes = 1
    receiver = ['LCUR']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {}

    class ReWiprActvn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "to activate the rear wiper"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' OnOffNoCmd_NoCmd', '0x1': ' OnOffNoCmd_OFF', '0x2': ' OnOffNoCmd_ON'}


class CCUSOCCDToLCUREthSignalIPdu74:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x40604A
    pdu_length_bytes = 1
    receiver = ['LCUR']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {}

    class SeatAdjRi2RowAntiPinchEna:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Antipinch Enable or Disable"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' EnableDisable4_NoCmd', '0x1': ' EnableDisable4_Disable', '0x2': ' EnableDisable4_Enable'}


class CCUSOCCDToLCUREthSignalIPdu23:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x406017
    pdu_length_bytes = 2
    receiver = ['LCUR']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {}

    class CmptmtRecFlapPosnReq:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Compartment Recirculation Flap Request Position"
        signal_length = 10
        start_position = 7
        value_definition = {}


class CCUSOCCDToLCUREthSignalIPdu61:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x40603D
    pdu_length_bytes = 2
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {'ReadingLiThrRowRiAdjReq': ['ReadingLiThrRowRiAdjReqLiPerc', 'ReadingLiThrRowRiAdjReqLightCmd', 'ReadingLiThrRowRiAdjReqReadingLiDimsSpdCmd']}

    class ReadingLiThrRowRiAdjReqLiPerc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "adjustment command of the  front left reading light intensity "
        signal_length = 7
        start_position = 7
        value_definition = {}

    class ReadingLiThrRowRiAdjReqLightCmd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "mode req of 3rd R"
        signal_length = 4
        start_position = 0
        value_definition = {'0x0': ' LightCmd_NoReq', '0x1': ' LightCmd_ON', '0x2': ' LightCmd_OFF', '0x3': ' LightCmd_TBD'}

    class ReadingLiThrRowRiAdjReqReadingLiDimsSpdCmd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "adjustment speed command of the  front left reading light intensity "
        signal_length = 3
        start_position = 12
        value_definition = {'0x0': ' ReadingLiDimsSpdCmd_NoCmd', '0x1': ' ReadingLiDimsSpdCmd_400ms', '0x2': ' ReadingLiDimsSpdCmd_800ms', '0x3': ' ReadingLiDimsSpdCmd_1000ms', '0x4': ' ReadingLiDimsSpdCmd_2000ms', '0x5': ' ReadingLiDimsSpdCmd_Resverd'}


class CCUSOCCDToLCUREthSignalIPdu57:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x406039
    pdu_length_bytes = 2
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {'ReadingLiFrntRiAdjReq': ['ReadingLiFrntRiAdjReqLightCmd', 'ReadingLiFrntRiAdjReqReadingLiDimsSpdCmd', 'ReadingLiFrntRiAdjReqLiPerc']}

    class ReadingLiFrntRiAdjReqLightCmd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "mode req of fr"
        signal_length = 4
        start_position = 7
        value_definition = {'0x0': ' LightCmd_NoReq', '0x1': ' LightCmd_ON', '0x2': ' LightCmd_OFF', '0x3': ' LightCmd_TBD'}

    class ReadingLiFrntRiAdjReqReadingLiDimsSpdCmd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "adjustment speed command of the  front left reading light intensity "
        signal_length = 3
        start_position = 3
        value_definition = {'0x0': ' ReadingLiDimsSpdCmd_NoCmd', '0x1': ' ReadingLiDimsSpdCmd_400ms', '0x2': ' ReadingLiDimsSpdCmd_800ms', '0x3': ' ReadingLiDimsSpdCmd_1000ms', '0x4': ' ReadingLiDimsSpdCmd_2000ms', '0x5': ' ReadingLiDimsSpdCmd_Resverd'}

    class ReadingLiFrntRiAdjReqLiPerc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "adjustment command of the  front left reading light intensity "
        signal_length = 7
        start_position = 0
        value_definition = {}


class CCUSOCCDToLCUREthSignalIPdu20:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x406014
    pdu_length_bytes = 1
    receiver = ['LCUR']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {}

    class AirFragActvReqFromSrv:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Air Fragrance Unit Active Request  From Service"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}


class CCUSOCCDToLCUREthSignalIPdu36:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x406024
    pdu_length_bytes = 1
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {}

    class ExtrReViewMirrDirAdjCmdPass:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "external rear view mirror orientation adjustment at passenger side"
        signal_length = 3
        start_position = 7
        value_definition = {'0x0': ' DirCmd_NoCmd', '0x1': ' DirCmd_Stop', '0x2': ' DirCmd_Left', '0x3': ' DirCmd_Right', '0x4': ' DirCmd_Up', '0x5': ' DirCmd_Down'}


class CCUSOCCDToLCUREthSignalIPdu45:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x40602D
    pdu_length_bytes = 2
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {'FuncReqOfLightShow': ['FuncReqOfLightShowLightPriority', 'FuncReqOfLightShowLightCmd', 'FuncReqOfLightShowLightID1']}

    class FuncReqOfLightShowLightPriority:
        comments = ""
        factor = 1.0
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Priority"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class FuncReqOfLightShowLightCmd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Light On or OFF command"
        signal_length = 4
        start_position = 15
        value_definition = {'0x0': ' LightCmd_NoReq', '0x1': ' LightCmd_ON', '0x2': ' LightCmd_OFF', '0x3': ' LightCmd_TBD'}

    class FuncReqOfLightShowLightID1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Light ID"
        signal_length = 4
        start_position = 11
        value_definition = {'0x0': ' LightID1_ALL', '0x1': ' LightID1_Front', '0x2': ' LightID1_Rear', '0x3': ' LightID1_LeftFrontLeftRearLeft', '0x4': ' LightID1_RightFrontRightRearRight', '0x5': ' LightID1_FrontLeft', '0x6': ' LightID1_FrontRight', '0x7': ' LightID1_RearLeft', '0x8': ' LightID1_FrontLeftRearRight', '0x9': ' LightID1_FrontRightRearLeft', '0xA': ' LightID1_ExceptFrontLeft', '0xB': ' LightID1_ExceptFrontRight', '0xC': ' LightID1_ExceptRearLeft', '0xD': ' LightID1_ExceptRearRight', '0xE': ' LightID1_Reserved1', '0xF': ' LightID1_Reserved2'}


class CCUSOCCDToLCUREthSignalIPdu47:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x40602F
    pdu_length_bytes = 2
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {'FuncReqOfPositionLamp': ['FuncReqOfPositionLampLightPriority', 'FuncReqOfPositionLampLightCmd', 'FuncReqOfPositionLampLightID1']}

    class FuncReqOfPositionLampLightPriority:
        comments = ""
        factor = 1.0
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "LightPriority"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class FuncReqOfPositionLampLightCmd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "LightCmd"
        signal_length = 4
        start_position = 15
        value_definition = {'0x0': ' LightCmd_NoReq', '0x1': ' LightCmd_ON', '0x2': ' LightCmd_OFF', '0x3': ' LightCmd_TBD'}

    class FuncReqOfPositionLampLightID1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "LightID"
        signal_length = 4
        start_position = 11
        value_definition = {'0x0': ' LightID1_ALL', '0x1': ' LightID1_Front', '0x2': ' LightID1_Rear', '0x3': ' LightID1_LeftFrontLeftRearLeft', '0x4': ' LightID1_RightFrontRightRearRight', '0x5': ' LightID1_FrontLeft', '0x6': ' LightID1_FrontRight', '0x7': ' LightID1_RearLeft', '0x8': ' LightID1_FrontLeftRearRight', '0x9': ' LightID1_FrontRightRearLeft', '0xA': ' LightID1_ExceptFrontLeft', '0xB': ' LightID1_ExceptFrontRight', '0xC': ' LightID1_ExceptRearLeft', '0xD': ' LightID1_ExceptRearRight', '0xE': ' LightID1_Reserved1', '0xF': ' LightID1_Reserved2'}


class CCUSOCCDToLCUREthSignalIPdu56:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x406038
    pdu_length_bytes = 2
    receiver = ['LCUR']
    send_type = "EventTriggered"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {'PwrContnsChRiCfgReq': ['PwrContnsChRiCfgReqContnsRiCh2CfgReq', 'PwrContnsChRiCfgReqContnsRiCh1CfgReq', 'PwrContnsChRiCfgReqContnsRiCh4CfgReq', 'PwrContnsChRiCfgReqContnsRiCh5CfgReq', 'PwrContnsChRiCfgReqContnsRiCh3CfgReq']}

    class PwrContnsChRiCfgReqContnsRiCh2CfgReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Right Zone Contns Power Channel 2 Config Request"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' OnOffNoCmd_NoCmd', '0x1': ' OnOffNoCmd_OFF', '0x2': ' OnOffNoCmd_ON'}

    class PwrContnsChRiCfgReqContnsRiCh1CfgReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Right Zone Contns Power Channel 1 Config Request"
        signal_length = 2
        start_position = 5
        value_definition = {'0x0': ' OnOffNoCmd_NoCmd', '0x1': ' OnOffNoCmd_OFF', '0x2': ' OnOffNoCmd_ON'}

    class PwrContnsChRiCfgReqContnsRiCh4CfgReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Right Zone Contns Power Channel 4 Config Request"
        signal_length = 2
        start_position = 3
        value_definition = {'0x0': ' OnOffNoCmd_NoCmd', '0x1': ' OnOffNoCmd_OFF', '0x2': ' OnOffNoCmd_ON'}

    class PwrContnsChRiCfgReqContnsRiCh5CfgReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Right Zone Contns Power Channel 5 Config Request"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': ' OnOffNoCmd_NoCmd', '0x1': ' OnOffNoCmd_OFF', '0x2': ' OnOffNoCmd_ON'}

    class PwrContnsChRiCfgReqContnsRiCh3CfgReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Right Zone Contns Power Channel 3 Config Request"
        signal_length = 2
        start_position = 15
        value_definition = {'0x0': ' OnOffNoCmd_NoCmd', '0x1': ' OnOffNoCmd_OFF', '0x2': ' OnOffNoCmd_ON'}


class CCUSOCCDToLCUREthSignalIPdu71:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x406047
    pdu_length_bytes = 4
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {'SeatAdj2RowRiReq': ['SeatAdj2RowRiReqMotorCtrlTilt', 'SeatAdj2RowRiReqMotorCtrlHei', 'SeatAdj2RowRiReqMotorCtrlOTTOLen', 'SeatAdj2RowRiReqMotorCtrlRe', 'SeatAdj2RowRiReqMotorCtrlBack', 'SeatAdj2RowRiReqMotorCtrlOTF', 'SeatAdj2RowRiReqMotorCtrlLen', 'SeatAdj2RowRiReqMotorCtrlCLA', 'SeatAdj2RowRiReqMotorCtrlOTTOAg']}

    class SeatAdj2RowRiReqMotorCtrlTilt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Motr Control"
        signal_length = 3
        start_position = 7
        value_definition = {'0x0': ' MotorCtrl_Idle', '0x1': ' MotorCtrl_RunningUp', '0x2': ' MotorCtrl_RunningDown', '0x3': ' MotorCtrl_Stop', '0x4': ' MotorCtrl_Reserved1', '0x5': ' MotorCtrl_Reserved2', '0x6': ' MotorCtrl_Reserved3', '0x7': ' MotorCtrl_Reserved4'}

    class SeatAdj2RowRiReqMotorCtrlHei:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Motr Control"
        signal_length = 3
        start_position = 4
        value_definition = {'0x0': ' MotorCtrl_Idle', '0x1': ' MotorCtrl_RunningUp', '0x2': ' MotorCtrl_RunningDown', '0x3': ' MotorCtrl_Stop', '0x4': ' MotorCtrl_Reserved1', '0x5': ' MotorCtrl_Reserved2', '0x6': ' MotorCtrl_Reserved3', '0x7': ' MotorCtrl_Reserved4'}

    class SeatAdj2RowRiReqMotorCtrlOTTOLen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Motr Control"
        signal_length = 3
        start_position = 1
        value_definition = {'0x0': ' MotorCtrl_Idle', '0x1': ' MotorCtrl_RunningUp', '0x2': ' MotorCtrl_RunningDown', '0x3': ' MotorCtrl_Stop', '0x4': ' MotorCtrl_Reserved1', '0x5': ' MotorCtrl_Reserved2', '0x6': ' MotorCtrl_Reserved3', '0x7': ' MotorCtrl_Reserved4'}

    class SeatAdj2RowRiReqMotorCtrlRe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Motr Control"
        signal_length = 3
        start_position = 14
        value_definition = {'0x0': ' MotorCtrl_Idle', '0x1': ' MotorCtrl_RunningUp', '0x2': ' MotorCtrl_RunningDown', '0x3': ' MotorCtrl_Stop', '0x4': ' MotorCtrl_Reserved1', '0x5': ' MotorCtrl_Reserved2', '0x6': ' MotorCtrl_Reserved3', '0x7': ' MotorCtrl_Reserved4'}

    class SeatAdj2RowRiReqMotorCtrlBack:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Motr Control"
        signal_length = 3
        start_position = 11
        value_definition = {'0x0': ' MotorCtrl_Idle', '0x1': ' MotorCtrl_RunningUp', '0x2': ' MotorCtrl_RunningDown', '0x3': ' MotorCtrl_Stop', '0x4': ' MotorCtrl_Reserved1', '0x5': ' MotorCtrl_Reserved2', '0x6': ' MotorCtrl_Reserved3', '0x7': ' MotorCtrl_Reserved4'}

    class SeatAdj2RowRiReqMotorCtrlOTF:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Motr Control"
        signal_length = 3
        start_position = 8
        value_definition = {'0x0': ' MotorCtrl_Idle', '0x1': ' MotorCtrl_RunningUp', '0x2': ' MotorCtrl_RunningDown', '0x3': ' MotorCtrl_Stop', '0x4': ' MotorCtrl_Reserved1', '0x5': ' MotorCtrl_Reserved2', '0x6': ' MotorCtrl_Reserved3', '0x7': ' MotorCtrl_Reserved4'}

    class SeatAdj2RowRiReqMotorCtrlLen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Motr Control"
        signal_length = 3
        start_position = 21
        value_definition = {'0x0': ' MotorCtrl_Idle', '0x1': ' MotorCtrl_RunningUp', '0x2': ' MotorCtrl_RunningDown', '0x3': ' MotorCtrl_Stop', '0x4': ' MotorCtrl_Reserved1', '0x5': ' MotorCtrl_Reserved2', '0x6': ' MotorCtrl_Reserved3', '0x7': ' MotorCtrl_Reserved4'}

    class SeatAdj2RowRiReqMotorCtrlCLA:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Motr Control"
        signal_length = 3
        start_position = 18
        value_definition = {'0x0': ' MotorCtrl_Idle', '0x1': ' MotorCtrl_RunningUp', '0x2': ' MotorCtrl_RunningDown', '0x3': ' MotorCtrl_Stop', '0x4': ' MotorCtrl_Reserved1', '0x5': ' MotorCtrl_Reserved2', '0x6': ' MotorCtrl_Reserved3', '0x7': ' MotorCtrl_Reserved4'}

    class SeatAdj2RowRiReqMotorCtrlOTTOAg:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Motr Control"
        signal_length = 3
        start_position = 31
        value_definition = {'0x0': ' MotorCtrl_Idle', '0x1': ' MotorCtrl_RunningUp', '0x2': ' MotorCtrl_RunningDown', '0x3': ' MotorCtrl_Stop', '0x4': ' MotorCtrl_Reserved1', '0x5': ' MotorCtrl_Reserved2', '0x6': ' MotorCtrl_Reserved3', '0x7': ' MotorCtrl_Reserved4'}


class CCUSOCCDToLCUREthSignalIPdu42:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x40602A
    pdu_length_bytes = 1
    receiver = ['LCUR']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {}

    class FRDoorManResistCtrl:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Door manual resistance control"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' DoorManResistCmd_Idle', '0x1': ' DoorManResistCmd_AddLevel1Cmd', '0x2': ' DoorManResistCmd_AddLevel2Cmd', '0x3': ' DoorManResistCmd_SubCmd'}


class CCUSOCCDToLCUREthSignalIPdu46:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x40602E
    pdu_length_bytes = 4
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {'FuncReqOfLowBeam': ['FuncReqOfLowBeamLightCmd', 'FuncReqOfLowBeamLightID1', 'FuncReqOfLowBeamChks', 'FuncReqOfLowBeamCntr', 'FuncReqOfLowBeamLightPriority']}

    class FuncReqOfLowBeamLightCmd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "light cmd"
        signal_length = 4
        start_position = 7
        value_definition = {'0x0': ' LightCmd_NoReq', '0x1': ' LightCmd_ON', '0x2': ' LightCmd_OFF', '0x3': ' LightCmd_TBD'}

    class FuncReqOfLowBeamLightID1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "lightid"
        signal_length = 4
        start_position = 3
        value_definition = {'0x0': ' LightID1_ALL', '0x1': ' LightID1_Front', '0x2': ' LightID1_Rear', '0x3': ' LightID1_LeftFrontLeftRearLeft', '0x4': ' LightID1_RightFrontRightRearRight', '0x5': ' LightID1_FrontLeft', '0x6': ' LightID1_FrontRight', '0x7': ' LightID1_RearLeft', '0x8': ' LightID1_FrontLeftRearRight', '0x9': ' LightID1_FrontRightRearLeft', '0xA': ' LightID1_ExceptFrontLeft', '0xB': ' LightID1_ExceptFrontRight', '0xC': ' LightID1_ExceptRearLeft', '0xD': ' LightID1_ExceptRearRight', '0xE': ' LightID1_Reserved1', '0xF': ' LightID1_Reserved2'}

    class FuncReqOfLowBeamChks:
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

    class FuncReqOfLowBeamCntr:
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

    class FuncReqOfLowBeamLightPriority:
        comments = ""
        factor = 1.0
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "priorityoflightrequest"
        signal_length = 8
        start_position = 31
        value_definition = {}


class CCUSOCCDToLCUREthSignalIPdu72:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x406048
    pdu_length_bytes = 4
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {'SeatAdj3RowRiReq': ['SeatAdj3RowRiReqMotorCtrlHei', 'SeatAdj3RowRiReqMotorCtrlBack', 'SeatAdj3RowRiReqMotorCtrlOTTOLen', 'SeatAdj3RowRiReqMotorCtrlOTTOAg', 'SeatAdj3RowRiReqMotorCtrlOTF', 'SeatAdj3RowRiReqMotorCtrlRe', 'SeatAdj3RowRiReqMotorCtrlLen', 'SeatAdj3RowRiReqMotorCtrlCLA', 'SeatAdj3RowRiReqMotorCtrlTilt']}

    class SeatAdj3RowRiReqMotorCtrlHei:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Motr Control"
        signal_length = 3
        start_position = 7
        value_definition = {'0x0': ' MotorCtrl_Idle', '0x1': ' MotorCtrl_RunningUp', '0x2': ' MotorCtrl_RunningDown', '0x3': ' MotorCtrl_Stop', '0x4': ' MotorCtrl_Reserved1', '0x5': ' MotorCtrl_Reserved2', '0x6': ' MotorCtrl_Reserved3', '0x7': ' MotorCtrl_Reserved4'}

    class SeatAdj3RowRiReqMotorCtrlBack:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Motr Control"
        signal_length = 3
        start_position = 4
        value_definition = {'0x0': ' MotorCtrl_Idle', '0x1': ' MotorCtrl_RunningUp', '0x2': ' MotorCtrl_RunningDown', '0x3': ' MotorCtrl_Stop', '0x4': ' MotorCtrl_Reserved1', '0x5': ' MotorCtrl_Reserved2', '0x6': ' MotorCtrl_Reserved3', '0x7': ' MotorCtrl_Reserved4'}

    class SeatAdj3RowRiReqMotorCtrlOTTOLen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Motr Control"
        signal_length = 3
        start_position = 1
        value_definition = {'0x0': ' MotorCtrl_Idle', '0x1': ' MotorCtrl_RunningUp', '0x2': ' MotorCtrl_RunningDown', '0x3': ' MotorCtrl_Stop', '0x4': ' MotorCtrl_Reserved1', '0x5': ' MotorCtrl_Reserved2', '0x6': ' MotorCtrl_Reserved3', '0x7': ' MotorCtrl_Reserved4'}

    class SeatAdj3RowRiReqMotorCtrlOTTOAg:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Motr Control"
        signal_length = 3
        start_position = 14
        value_definition = {'0x0': ' MotorCtrl_Idle', '0x1': ' MotorCtrl_RunningUp', '0x2': ' MotorCtrl_RunningDown', '0x3': ' MotorCtrl_Stop', '0x4': ' MotorCtrl_Reserved1', '0x5': ' MotorCtrl_Reserved2', '0x6': ' MotorCtrl_Reserved3', '0x7': ' MotorCtrl_Reserved4'}

    class SeatAdj3RowRiReqMotorCtrlOTF:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Motr Control"
        signal_length = 3
        start_position = 11
        value_definition = {'0x0': ' MotorCtrl_Idle', '0x1': ' MotorCtrl_RunningUp', '0x2': ' MotorCtrl_RunningDown', '0x3': ' MotorCtrl_Stop', '0x4': ' MotorCtrl_Reserved1', '0x5': ' MotorCtrl_Reserved2', '0x6': ' MotorCtrl_Reserved3', '0x7': ' MotorCtrl_Reserved4'}

    class SeatAdj3RowRiReqMotorCtrlRe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Motr Control"
        signal_length = 3
        start_position = 8
        value_definition = {'0x0': ' MotorCtrl_Idle', '0x1': ' MotorCtrl_RunningUp', '0x2': ' MotorCtrl_RunningDown', '0x3': ' MotorCtrl_Stop', '0x4': ' MotorCtrl_Reserved1', '0x5': ' MotorCtrl_Reserved2', '0x6': ' MotorCtrl_Reserved3', '0x7': ' MotorCtrl_Reserved4'}

    class SeatAdj3RowRiReqMotorCtrlLen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Motr Control"
        signal_length = 3
        start_position = 21
        value_definition = {'0x0': ' MotorCtrl_Idle', '0x1': ' MotorCtrl_RunningUp', '0x2': ' MotorCtrl_RunningDown', '0x3': ' MotorCtrl_Stop', '0x4': ' MotorCtrl_Reserved1', '0x5': ' MotorCtrl_Reserved2', '0x6': ' MotorCtrl_Reserved3', '0x7': ' MotorCtrl_Reserved4'}

    class SeatAdj3RowRiReqMotorCtrlCLA:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Motr Control"
        signal_length = 3
        start_position = 18
        value_definition = {'0x0': ' MotorCtrl_Idle', '0x1': ' MotorCtrl_RunningUp', '0x2': ' MotorCtrl_RunningDown', '0x3': ' MotorCtrl_Stop', '0x4': ' MotorCtrl_Reserved1', '0x5': ' MotorCtrl_Reserved2', '0x6': ' MotorCtrl_Reserved3', '0x7': ' MotorCtrl_Reserved4'}

    class SeatAdj3RowRiReqMotorCtrlTilt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Motr Control"
        signal_length = 3
        start_position = 31
        value_definition = {'0x0': ' MotorCtrl_Idle', '0x1': ' MotorCtrl_RunningUp', '0x2': ' MotorCtrl_RunningDown', '0x3': ' MotorCtrl_Stop', '0x4': ' MotorCtrl_Reserved1', '0x5': ' MotorCtrl_Reserved2', '0x6': ' MotorCtrl_Reserved3', '0x7': ' MotorCtrl_Reserved4'}


class CCUSOCCDToLCUREthSignalIPdu28:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x40601C
    pdu_length_bytes = 4
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {'CpilSaucerRiALMRGBL': ['CpilSaucerRiALMRGBLRed', 'CpilSaucerRiALMRGBLGreen', 'CpilSaucerRiALMRGBLLuminance', 'CpilSaucerRiALMRGBLBlue']}

    class CpilSaucerRiALMRGBLRed:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Red,CpilSaucerRiALMRGBL"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class CpilSaucerRiALMRGBLGreen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Green,CpilSaucerRiALMRGBL"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class CpilSaucerRiALMRGBLLuminance:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Luminance,CpilSaucerRiALMRGBL"
        signal_length = 7
        start_position = 23
        value_definition = {}

    class CpilSaucerRiALMRGBLBlue:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Blue,CpilSaucerRiALMRGBL"
        signal_length = 8
        start_position = 31
        value_definition = {}


class CCUSOCCDToLCUREthSignalIPdu44:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x40602C
    pdu_length_bytes = 3
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {'FuncReqOfFrontFogLamp': ['FuncReqOfFrontFogLampLightID1', 'FuncReqOfFrontFogLampLightPriority', 'FuncReqOfFrontFogLampLightCmd']}

    class FuncReqOfFrontFogLampLightID1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "LightID"
        signal_length = 4
        start_position = 7
        value_definition = {'0x0': ' LightID1_ALL', '0x1': ' LightID1_Front', '0x2': ' LightID1_Rear', '0x3': ' LightID1_LeftFrontLeftRearLeft', '0x4': ' LightID1_RightFrontRightRearRight', '0x5': ' LightID1_FrontLeft', '0x6': ' LightID1_FrontRight', '0x7': ' LightID1_RearLeft', '0x8': ' LightID1_FrontLeftRearRight', '0x9': ' LightID1_FrontRightRearLeft', '0xA': ' LightID1_ExceptFrontLeft', '0xB': ' LightID1_ExceptFrontRight', '0xC': ' LightID1_ExceptRearLeft', '0xD': ' LightID1_ExceptRearRight', '0xE': ' LightID1_Reserved1', '0xF': ' LightID1_Reserved2'}

    class FuncReqOfFrontFogLampLightPriority:
        comments = ""
        factor = 1.0
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "LightPriority"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class FuncReqOfFrontFogLampLightCmd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "LightCmd"
        signal_length = 4
        start_position = 23
        value_definition = {'0x0': ' LightCmd_NoReq', '0x1': ' LightCmd_ON', '0x2': ' LightCmd_OFF', '0x3': ' LightCmd_TBD'}


class CCUSOCCDToLCUREthSignalIPdu83:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x406053
    pdu_length_bytes = 2
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {'TrunkLiFuncReq': ['TrunkLiFuncReqLiPerc', 'TrunkLiFuncReqLightCmd', 'TrunkLiFuncReqReadingLiDimsSpdCmd']}

    class TrunkLiFuncReqLiPerc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "brightness percent"
        signal_length = 7
        start_position = 7
        value_definition = {}

    class TrunkLiFuncReqLightCmd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "light command"
        signal_length = 4
        start_position = 0
        value_definition = {'0x0': ' LightCmd_NoReq', '0x1': ' LightCmd_ON', '0x2': ' LightCmd_OFF', '0x3': ' LightCmd_TBD'}

    class TrunkLiFuncReqReadingLiDimsSpdCmd:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "required dim speed"
        signal_length = 3
        start_position = 12
        value_definition = {'0x0': ' ReadingLiDimsSpdCmd_NoCmd', '0x1': ' ReadingLiDimsSpdCmd_400ms', '0x2': ' ReadingLiDimsSpdCmd_800ms', '0x3': ' ReadingLiDimsSpdCmd_1000ms', '0x4': ' ReadingLiDimsSpdCmd_2000ms', '0x5': ' ReadingLiDimsSpdCmd_Resverd'}


class CCUSOCCDToLCUREthSignalIPdu55:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x406037
    pdu_length_bytes = 1
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {}

    class LevelingMotorStaticEn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "MotorEnableDisable"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' EnableDisable2_Disabled', '0x1': ' EnableDisable2_Enabled'}


class CCUSOCCDToLCUREthSignalIPdu41:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x406029
    pdu_length_bytes = 4
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {'FootwellSecRiALMRGBL': ['FootwellSecRiALMRGBLLuminance', 'FootwellSecRiALMRGBLRed', 'FootwellSecRiALMRGBLBlue', 'FootwellSecRiALMRGBLGreen']}

    class FootwellSecRiALMRGBLLuminance:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Luminance,FootwellSecRiALMRGBL"
        signal_length = 7
        start_position = 7
        value_definition = {}

    class FootwellSecRiALMRGBLRed:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Red,FootwellSecRiALMRGBL"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class FootwellSecRiALMRGBLBlue:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Blue,FootwellSecRiALMRGBL"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class FootwellSecRiALMRGBLGreen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Green,FootwellSecRiALMRGBL"
        signal_length = 8
        start_position = 31
        value_definition = {}


class CCUSOCCDToLCUREthSignalIPdu58:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x40603A
    pdu_length_bytes = 2
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {'ReadingLiSecRowLeAdjReq': ['ReadingLiSecRowLeAdjReqLiPerc', 'ReadingLiSecRowLeAdjReqLightCmd', 'ReadingLiSecRowLeAdjReqReadingLiDimsSpdCmd']}

    class ReadingLiSecRowLeAdjReqLiPerc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "adjustment command of the  front left reading light intensity "
        signal_length = 7
        start_position = 7
        value_definition = {}

    class ReadingLiSecRowLeAdjReqLightCmd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "mode req of 2nd L"
        signal_length = 4
        start_position = 0
        value_definition = {'0x0': ' LightCmd_NoReq', '0x1': ' LightCmd_ON', '0x2': ' LightCmd_OFF', '0x3': ' LightCmd_TBD'}

    class ReadingLiSecRowLeAdjReqReadingLiDimsSpdCmd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "adjustment speed command of the  front left reading light intensity "
        signal_length = 3
        start_position = 12
        value_definition = {'0x0': ' ReadingLiDimsSpdCmd_NoCmd', '0x1': ' ReadingLiDimsSpdCmd_400ms', '0x2': ' ReadingLiDimsSpdCmd_800ms', '0x3': ' ReadingLiDimsSpdCmd_1000ms', '0x4': ' ReadingLiDimsSpdCmd_2000ms', '0x5': ' ReadingLiDimsSpdCmd_Resverd'}


class CCUSOCCDToLCUREthSignalIPdu87:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x406057
    pdu_length_bytes = 4
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {'TweeterRiUpprALMRGBL': ['TweeterRiUpprALMRGBLLuminance', 'TweeterRiUpprALMRGBLGreen', 'TweeterRiUpprALMRGBLRed', 'TweeterRiUpprALMRGBLBlue']}

    class TweeterRiUpprALMRGBLLuminance:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Luminance,TweeterRiUpprALMRGBL"
        signal_length = 7
        start_position = 7
        value_definition = {}

    class TweeterRiUpprALMRGBLGreen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Green,TweeterRiUpprALMRGBL"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class TweeterRiUpprALMRGBLRed:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Red,TweeterRiUpprALMRGBL"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class TweeterRiUpprALMRGBLBlue:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Blue,TweeterRiUpprALMRGBL"
        signal_length = 8
        start_position = 31
        value_definition = {}


class CCUSOCCDToLCUREthSignalIPdu26:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x40601A
    pdu_length_bytes = 4
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {'ConsoleRiALMRGBL': ['ConsoleRiALMRGBLRed', 'ConsoleRiALMRGBLBlue', 'ConsoleRiALMRGBLGreen', 'ConsoleRiALMRGBLLuminance']}

    class ConsoleRiALMRGBLRed:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Red,Console right alm"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class ConsoleRiALMRGBLBlue:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Blue,Console right alm"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class ConsoleRiALMRGBLGreen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Green,Console right alm"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class ConsoleRiALMRGBLLuminance:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Luminance,Console right alm"
        signal_length = 7
        start_position = 31
        value_definition = {}


class CCUSOCCDToLCUREthSignalIPdu59:
    base_type = "Unsigned"
    client_socket = "SocketLcuRTCPServer"
    pdu_header_id = 0x40603B
    pdu_length_bytes = 2
    receiver = ['LCUR']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient4"
    signal_group = {'ReadingLiSecRowRiAdjReq': ['ReadingLiSecRowRiAdjReqLightCmd', 'ReadingLiSecRowRiAdjReqReadingLiDimsSpdCmd', 'ReadingLiSecRowRiAdjReqLiPerc']}

    class ReadingLiSecRowRiAdjReqLightCmd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "mode req of 2nd R"
        signal_length = 4
        start_position = 7
        value_definition = {'0x0': ' LightCmd_NoReq', '0x1': ' LightCmd_ON', '0x2': ' LightCmd_OFF', '0x3': ' LightCmd_TBD'}

    class ReadingLiSecRowRiAdjReqReadingLiDimsSpdCmd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "adjustment speed command of the  front left reading light intensity "
        signal_length = 3
        start_position = 3
        value_definition = {'0x0': ' ReadingLiDimsSpdCmd_NoCmd', '0x1': ' ReadingLiDimsSpdCmd_400ms', '0x2': ' ReadingLiDimsSpdCmd_800ms', '0x3': ' ReadingLiDimsSpdCmd_1000ms', '0x4': ' ReadingLiDimsSpdCmd_2000ms', '0x5': ' ReadingLiDimsSpdCmd_Resverd'}

    class ReadingLiSecRowRiAdjReqLiPerc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "adjustment command of the  front left reading light intensity "
        signal_length = 7
        start_position = 0
        value_definition = {}
