

class CCUSOCCDToLCULEthSignalIPdu07:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405007
    pdu_length_bytes = 3
    receiver = ['LCUL']
    send_type = "Cyclic-80ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {'BackLightingIllumSelnDay': ['BackLightingIllumSelnDayReadingLiDimsSpdCmd', 'BackLightingIllumSelnDayLiPerc'], 'BackLightingIllumSelnNight': ['BackLightingIllumSelnNightLiPerc', 'BackLightingIllumSelnNightReadingLiDimsSpdCmd']}

    class BackLightingIllumSelnDayReadingLiDimsSpdCmd:
        comments = ""
        factor = 1.0
        initial_value = 2
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "dim speed"
        signal_length = 3
        start_position = 15
        value_definition = {'0x0': ' ReadingLiDimsSpdCmd_NoCmd', '0x1': ' ReadingLiDimsSpdCmd_400ms', '0x2': ' ReadingLiDimsSpdCmd_800ms', '0x3': ' ReadingLiDimsSpdCmd_1000ms', '0x4': ' ReadingLiDimsSpdCmd_2000ms', '0x5': ' ReadingLiDimsSpdCmd_Resverd'}

    class BackLightingIllumSelnDayLiPerc:
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

    class BackLightingIllumSelnNightLiPerc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "brightness percent"
        signal_length = 7
        start_position = 23
        value_definition = {}

    class BackLightingIllumSelnNightReadingLiDimsSpdCmd:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "dim speed"
        signal_length = 3
        start_position = 10
        value_definition = {'0x0': ' ReadingLiDimsSpdCmd_NoCmd', '0x1': ' ReadingLiDimsSpdCmd_400ms', '0x2': ' ReadingLiDimsSpdCmd_800ms', '0x3': ' ReadingLiDimsSpdCmd_1000ms', '0x4': ' ReadingLiDimsSpdCmd_2000ms', '0x5': ' ReadingLiDimsSpdCmd_Resverd'}

    class BackLightingModSeln:
        comments = ""
        factor = 1.0
        initial_value = 3
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "mode setting information"
        signal_length = 2
        start_position = 12
        value_definition = {'0x0': ' IntrLampSelnMod_NoCmd', '0x1': ' IntrLampSelnMod_OFF', '0x2': ' IntrLampSelnMod_ON', '0x3': ' IntrLampSelnMod_AUTO'}


class CCUSOCCDToLCULEthSignalIPdu06:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405006
    pdu_length_bytes = 1
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
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


class CCUSOCCDToLCULEthSignalIPdu04:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405004
    pdu_length_bytes = 2
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {'FootwellLiFrntLeCmd': ['FootwellLiFrntLeCmdLiPerc', 'FootwellLiFrntLeCmdLightCmd', 'FootwellLiFrntLeCmdReadingLiDimsSpdCmd']}

    class FootwellLiFrntLeCmdLiPerc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "illumination percent"
        signal_length = 7
        start_position = 7
        value_definition = {}

    class FootwellLiFrntLeCmdLightCmd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Light cmd"
        signal_length = 4
        start_position = 15
        value_definition = {'0x0': ' LightCmd_NoReq', '0x1': ' LightCmd_ON', '0x2': ' LightCmd_OFF', '0x3': ' LightCmd_TBD'}

    class FootwellLiFrntLeCmdReadingLiDimsSpdCmd:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "activate speed command of the front left monochromatic footwell light"
        signal_length = 3
        start_position = 11
        value_definition = {'0x0': ' ReadingLiDimsSpdCmd_NoCmd', '0x1': ' ReadingLiDimsSpdCmd_400ms', '0x2': ' ReadingLiDimsSpdCmd_800ms', '0x3': ' ReadingLiDimsSpdCmd_1000ms', '0x4': ' ReadingLiDimsSpdCmd_2000ms', '0x5': ' ReadingLiDimsSpdCmd_Resverd'}


class CCUSOCCDToLCULEthSignalIPdu03:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405003
    pdu_length_bytes = 6
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {'FuncReqOfHighBeam': ['FuncReqOfHighBeamLightCmd', 'FuncReqOfHighBeamFlashParamterOnTime', 'FuncReqOfHighBeamHoldEn', 'FuncReqOfHighBeamFlashParamterOffTime', 'FuncReqOfHighBeamLightID1', 'FuncReqOfHighBeamLightPriority', 'FuncReqOfHighBeamFlashParamterFlashNTime']}

    class FuncReqOfHighBeamLightCmd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "LightCmd"
        signal_length = 4
        start_position = 35
        value_definition = {'0x0': ' LightCmd_NoReq', '0x1': ' LightCmd_ON', '0x2': ' LightCmd_OFF', '0x3': ' LightCmd_TBD'}

    class FuncReqOfHighBeamFlashParamterOnTime:
        comments = ""
        factor = 1.0
        initial_value = 20
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "FunctionParameter1"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class FuncReqOfHighBeamHoldEn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "keep or not when function is finished"
        signal_length = 1
        start_position = 47
        value_definition = {'0x0': ' EnableDisable2_Disabled', '0x1': ' EnableDisable2_Enabled'}

    class FuncReqOfHighBeamFlashParamterOffTime:
        comments = ""
        factor = 1.0
        initial_value = 20
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "FunctionParameter2"
        signal_length = 8
        start_position = 31
        value_definition = {}

    class FuncReqOfHighBeamLightID1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "LightID"
        signal_length = 4
        start_position = 39
        value_definition = {'0x0': ' LightID1_ALL', '0x1': ' LightID1_Front', '0x2': ' LightID1_Rear', '0x3': ' LightID1_LeftFrontLeftRearLeft', '0x4': ' LightID1_RightFrontRightRearRight', '0x5': ' LightID1_FrontLeft', '0x6': ' LightID1_FrontRight', '0x7': ' LightID1_RearLeft', '0x8': ' LightID1_FrontLeftRearRight', '0x9': ' LightID1_FrontRightRearLeft', '0xA': ' LightID1_ExceptFrontLeft', '0xB': ' LightID1_ExceptFrontRight', '0xC': ' LightID1_ExceptRearLeft', '0xD': ' LightID1_ExceptRearRight', '0xE': ' LightID1_Reserved1', '0xF': ' LightID1_Reserved2'}

    class FuncReqOfHighBeamLightPriority:
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

    class FuncReqOfHighBeamFlashParamterFlashNTime:
        comments = ""
        factor = 1.0
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "FunctionParameter3"
        signal_length = 8
        start_position = 23
        value_definition = {}


class CCUSOCCDToLCULEthSignalIPdu01:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405001
    pdu_length_bytes = 1
    receiver = ['LCUL']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {}

    class ADCamDefrostReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Reques AD Camera Defrost"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' ReqSts2_Default', '0x1': ' ReqSts2_NotReqd', '0x2': ' ReqSts2_Reqd', '0x3': ' ReqSts2_Reserved'}


class CCUSOCCDToLCULEthSignalIPdu02:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405002
    pdu_length_bytes = 4
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {'ConsoleLeALMRGBL': ['ConsoleLeALMRGBLGreen', 'ConsoleLeALMRGBLBlue', 'ConsoleLeALMRGBLLuminance', 'ConsoleLeALMRGBLRed']}

    class ConsoleLeALMRGBLGreen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Geen,Console left alm"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class ConsoleLeALMRGBLBlue:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Blue,Console left alm"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class ConsoleLeALMRGBLLuminance:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Luminance,Console left alm"
        signal_length = 7
        start_position = 31
        value_definition = {}

    class ConsoleLeALMRGBLRed:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Red,Console left alm"
        signal_length = 8
        start_position = 23
        value_definition = {}


class CCUSOCCDToLCULEthSignalIPdu05:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405005
    pdu_length_bytes = 1
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {}

    class CarLoctrToExtrLiVisReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Car locator to external lighting request"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}


class CCUSOCCDToLCULEthSignalIPdu08:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405008
    pdu_length_bytes = 1
    receiver = ['LCUL']
    send_type = "EventTriggered"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
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


class CCUSOCCDToLCULEthSignalIPdu09:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405009
    pdu_length_bytes = 1
    receiver = ['LCUL']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {}

    class FrntWiperMode:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Front Wiper Mode"
        signal_length = 4
        start_position = 7
        value_definition = {'0x0': ' FrntWiperMode_OFF', '0x1': ' FrntWiperMode_SingleScrape', '0x2': ' FrntWiperMode_Interval1', '0x3': ' FrntWiperMode_Interval2', '0x4': ' FrntWiperMode_IntervalReserve', '0x5': ' FrntWiperMode_ContinuousLow', '0x6': ' FrntWiperMode_ContinuousHigh', '0x7': ' FrntWiperMode_Auto', '0x8': ' FrntWiperMode_Maintenance', '0x9': ' FrntWiperMode_Reserve'}

    class WiprMotIntlCmd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "the rain sensor sensitivity or the pause time of the interval mode."
        signal_length = 3
        start_position = 3
        value_definition = {'0x0': ' WipgSpdIntlCmd_Posn0', '0x1': ' WipgSpdIntlCmd_Posn1', '0x2': ' WipgSpdIntlCmd_Posn2', '0x3': ' WipgSpdIntlCmd_Posn3', '0x4': ' WipgSpdIntlCmd_Posn4', '0x5': ' WipgSpdIntlCmd_Posn5', '0x6': ' WipgSpdIntlCmd_Posn6', '0x7': ' WipgSpdIntlCmd_Posn7'}


class CCUSOCCDToLCULEthSignalIPdu10:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x40500A
    pdu_length_bytes = 4
    receiver = ['LCUL']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {}

    class ElecVentSrvFrntLeLeXPosnReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Vent Grill Motor 1 Position Request"
        signal_length = 16
        start_position = 7
        value_definition = {}

    class ElecVentSrvFrntLeLeYPosnReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Vent Grill Motor 2 Position Request"
        signal_length = 16
        start_position = 23
        value_definition = {}


class CCUSOCCDToLCULEthSignalIPdu11:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x40500B
    pdu_length_bytes = 4
    receiver = ['LCUL']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {}

    class ElecVentSrvFrntLeRiXPosnReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Vent Grill Motor 3 Position Request"
        signal_length = 16
        start_position = 7
        value_definition = {}

    class ElecVentSrvFrntLeRiYPosnReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Vent Grill Motor 4 Position Request"
        signal_length = 16
        start_position = 23
        value_definition = {}


class CCUSOCCDToLCULEthSignalIPdu12:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x40500C
    pdu_length_bytes = 4
    receiver = ['LCUL']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {}

    class ElecVentSrvReLeXPosnReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Vent Grill Motor 9 Position Request"
        signal_length = 16
        start_position = 7
        value_definition = {}

    class ElecVentSrvReLeYPosnReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Vent Grill Motor 10 Position Request"
        signal_length = 16
        start_position = 23
        value_definition = {}


class CCUSOCCDToLCULEthSignalIPdu64:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405040
    pdu_length_bytes = 2
    receiver = ['LCUL']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {}

    class PNGLowUSetKL30B:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = ""
        signal_length = 9
        start_position = 7
        value_definition = {}


class CCUSOCCDToLCULEthSignalIPdu62:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x40503E
    pdu_length_bytes = 2
    receiver = ['LCUL']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {}

    class PNGIPrmSetKL30B:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = ""
        signal_length = 12
        start_position = 7
        value_definition = {}


class CCUSOCCDToLCULEthSignalIPdu61:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x40503D
    pdu_length_bytes = 2
    receiver = ['LCUL']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {}

    class PNGIPrmSetKL30A:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = ""
        signal_length = 12
        start_position = 7
        value_definition = {}


class CCUSOCCDToLCULEthSignalIPdu65:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405041
    pdu_length_bytes = 2
    receiver = ['LCUL']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {}

    class PNGOverTSetKL30A:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = None
        signal_description = ""
        signal_length = 13
        start_position = 7
        value_definition = {}


class CCUSOCCDToLCULEthSignalIPdu63:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x40503F
    pdu_length_bytes = 2
    receiver = ['LCUL']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {}

    class PNGLowUSetKL30A:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = ""
        signal_length = 9
        start_position = 7
        value_definition = {}


class CCUSOCCDToLCULEthSignalIPdu68:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405044
    pdu_length_bytes = 2
    receiver = ['LCUL']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {}

    class PNGOverUSetKL30B:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = ""
        signal_length = 9
        start_position = 7
        value_definition = {}


class CCUSOCCDToLCULEthSignalIPdu66:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405042
    pdu_length_bytes = 2
    receiver = ['LCUL']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {}

    class PNGOverTSetKL30B:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = None
        signal_description = ""
        signal_length = 13
        start_position = 7
        value_definition = {}


class CCUSOCCDToLCULEthSignalIPdu70:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405046
    pdu_length_bytes = 4
    receiver = ['LCUL']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {'RainSnsrSnvtyForUsrSnvty': ['RainSnsrSnvtyForUsrSnvty1', 'RainSnsrSnvtyForUsrSnvty4', 'RainSnsrSnvtyForUsrSnvty5', 'RainSnsrSnvtyForUsrSnvty0', 'RainSnsrSnvtyForUsrSnvty3', 'RainSnsrSnvtyForUsrSnvty6', 'RainSnsrSnvtyForUsrSnvty2']}

    class RainSnsrSnvtyForUsrSnvty1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Signal1 used to map the different sensitivity settings that can be selected by the driver to an internal sensitivity in the rain sensor"
        signal_length = 4
        start_position = 3
        value_definition = {}

    class RainSnsrSnvtyForUsrSnvty4:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Signal4 used to map the different sensitivity settings that can be selected by the driver to an internal sensitivity in the rain sensor"
        signal_length = 4
        start_position = 23
        value_definition = {}

    class RainSnsrSnvtyForUsrSnvty5:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Signal5 used to map the different sensitivity settings that can be selected by the driver to an internal sensitivity in the rain sensor"
        signal_length = 4
        start_position = 19
        value_definition = {}

    class RainSnsrSnvtyForUsrSnvty0:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Signal0 used to map the different sensitivity settings that can be selected by the driver to an internal sensitivity in the rain sensor"
        signal_length = 4
        start_position = 7
        value_definition = {}

    class RainSnsrSnvtyForUsrSnvty3:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Signal3 used to map the different sensitivity settings that can be selected by the driver to an internal sensitivity in the rain sensor"
        signal_length = 4
        start_position = 11
        value_definition = {}

    class RainSnsrSnvtyForUsrSnvty6:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Signal6 used to map the different sensitivity settings that can be selected by the driver to an internal sensitivity in the rain sensor"
        signal_length = 4
        start_position = 31
        value_definition = {}

    class RainSnsrSnvtyForUsrSnvty2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Signal2 used to map the different sensitivity settings that can be selected by the driver to an internal sensitivity in the rain sensor"
        signal_length = 4
        start_position = 15
        value_definition = {}


class CCUSOCCDToLCULEthSignalIPdu67:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405043
    pdu_length_bytes = 2
    receiver = ['LCUL']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {}

    class PNGOverUSetKL30A:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = ""
        signal_length = 9
        start_position = 7
        value_definition = {}


class CCUSOCCDToLCULEthSignalIPdu69:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405045
    pdu_length_bytes = 2
    receiver = ['LCUL']
    send_type = "EventTriggered"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {'PwrContnsChLeCfgReq': ['PwrContnsChLeCfgReqContnsLeCh3CfgReq', 'PwrContnsChLeCfgReqContnsLeCh5CfgReq', 'PwrContnsChLeCfgReqContnsLeCh2CfgReq', 'PwrContnsChLeCfgReqContnsLeCh1CfgReq', 'PwrContnsChLeCfgReqContnsLeCh4CfgReq']}

    class PwrContnsChLeCfgReqContnsLeCh3CfgReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Left Zone Contns Power Channel 3 Config Request"
        signal_length = 2
        start_position = 3
        value_definition = {'0x0': ' OnOffNoCmd_NoCmd', '0x1': ' OnOffNoCmd_OFF', '0x2': ' OnOffNoCmd_ON'}

    class PwrContnsChLeCfgReqContnsLeCh5CfgReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Left Zone Contns Power Channel 5 Config Request"
        signal_length = 2
        start_position = 15
        value_definition = {'0x0': ' OnOffNoCmd_NoCmd', '0x1': ' OnOffNoCmd_OFF', '0x2': ' OnOffNoCmd_ON'}

    class PwrContnsChLeCfgReqContnsLeCh2CfgReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Left Zone Contns Power Channel 2 Config Request"
        signal_length = 2
        start_position = 5
        value_definition = {'0x0': ' OnOffNoCmd_NoCmd', '0x1': ' OnOffNoCmd_OFF', '0x2': ' OnOffNoCmd_ON'}

    class PwrContnsChLeCfgReqContnsLeCh1CfgReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Left Zone Contns Power Channel 1 Config Request"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' OnOffNoCmd_NoCmd', '0x1': ' OnOffNoCmd_OFF', '0x2': ' OnOffNoCmd_ON'}

    class PwrContnsChLeCfgReqContnsLeCh4CfgReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Left Zone Contns Power Channel 4 Config Request"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': ' OnOffNoCmd_NoCmd', '0x1': ' OnOffNoCmd_OFF', '0x2': ' OnOffNoCmd_ON'}


class CCUSOCCDToLCULEthSignalIPdu73:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405049
    pdu_length_bytes = 1
    receiver = ['LCUL']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {}

    class RemClimaReqIndcr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Remote Cliamte Request Indicator"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' Flg1_Rst', '0x1': ' Flg1_Set'}


class CCUSOCCDToLCULEthSignalIPdu71:
    base_type = "Boolean"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405047
    pdu_length_bytes = 1
    receiver = ['LCUL']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {}

    class ReBlwrAftRunSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Rear Blower AfterRun Status"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}


class CCUSOCCDToLCULEthSignalIPdu74:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x40504A
    pdu_length_bytes = 1
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {}

    class ReSunroofCurtSwtCmd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "switch command of rear sunroof curt"
        signal_length = 3
        start_position = 7
        value_definition = {'0x0': ' SunroofCurtSwtSts_Idle', '0x1': ' SunroofCurtSwtSts_OpenMan', '0x2': ' SunroofCurtSwtSts_OpenAut', '0x3': ' SunroofCurtSwtSts_ClsMan1', '0x4': ' SunroofCurtSwtSts_ClsMan2', '0x5': ' SunroofCurtSwtSts_Stop'}


class CCUSOCCDToLCULEthSignalIPdu75:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x40504B
    pdu_length_bytes = 1
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {}

    class ReViewMirrDimEna:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Anti-dazzling adjustment command for the interior rear view mirror"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' OnOffNoCmd_NoCmd', '0x1': ' OnOffNoCmd_OFF', '0x2': ' OnOffNoCmd_ON'}


class CCUSOCCDToLCULEthSignalIPdu72:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405048
    pdu_length_bytes = 1
    receiver = ['LCUL']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {}

    class ReBlwrLvlSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Rear Blower Actual Level Status"
        signal_length = 4
        start_position = 7
        value_definition = {'0x0': ' FrntBlwrLvl_Off', '0x1': ' FrntBlwrLvl_LvlMan1', '0x2': ' FrntBlwrLvl_LvlMan2', '0x3': ' FrntBlwrLvl_LvlMan3', '0x4': ' FrntBlwrLvl_LvlMan4', '0x5': ' FrntBlwrLvl_LvlMan5', '0x6': ' FrntBlwrLvl_LvlMan6', '0x7': ' FrntBlwrLvl_LvlMan7', '0x8': ' FrntBlwrLvl_LvlMan8', '0x9': ' FrntBlwrLvl_LvlMan9', '0xA': ' FrntBlwrLvl_LvlAutoLo', '0xB': ' FrntBlwrLvl_LvlAutoNormal', '0xC': ' FrntBlwrLvl_LvlAutoHi'}


class CCUSOCCDToLCULEthSignalIPdu77:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x40504D
    pdu_length_bytes = 1
    receiver = ['LCUL']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {}

    class RLDoorManResistCtrl:
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


class CCUSOCCDToLCULEthSignalIPdu76:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x40504C
    pdu_length_bytes = 1
    receiver = ['LCUL']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {}

    class ReWshrActvn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "to activate the rear washing"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' OnOffNoCmd_NoCmd', '0x1': ' OnOffNoCmd_OFF', '0x2': ' OnOffNoCmd_ON'}


class CCUSOCCDToLCULEthSignalIPdu78:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x40504E
    pdu_length_bytes = 2
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {}

    class RLPwrSideDoorMaxPosnSet:
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


class CCUSOCCDToLCULEthSignalIPdu79:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x40504F
    pdu_length_bytes = 4
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {'SeatAdj1RowLeReq': ['SeatAdj1RowLeReqMotorCtrlBack', 'SeatAdj1RowLeReqMotorCtrlRe', 'SeatAdj1RowLeReqMotorCtrlOTF', 'SeatAdj1RowLeReqMotorCtrlTilt', 'SeatAdj1RowLeReqMotorCtrlOTTOAg', 'SeatAdj1RowLeReqMotorCtrlHei', 'SeatAdj1RowLeReqMotorCtrlLen', 'SeatAdj1RowLeReqMotorCtrlOTTOLen', 'SeatAdj1RowLeReqMotorCtrlCLA']}

    class SeatAdj1RowLeReqMotorCtrlBack:
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

    class SeatAdj1RowLeReqMotorCtrlRe:
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

    class SeatAdj1RowLeReqMotorCtrlOTF:
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

    class SeatAdj1RowLeReqMotorCtrlTilt:
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

    class SeatAdj1RowLeReqMotorCtrlOTTOAg:
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

    class SeatAdj1RowLeReqMotorCtrlHei:
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

    class SeatAdj1RowLeReqMotorCtrlLen:
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

    class SeatAdj1RowLeReqMotorCtrlOTTOLen:
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

    class SeatAdj1RowLeReqMotorCtrlCLA:
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


class CCUSOCCDToLCULEthSignalIPdu80:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405050
    pdu_length_bytes = 4
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {'SeatAdj2RowLeReq': ['SeatAdj2RowLeReqMotorCtrlOTTOLen', 'SeatAdj2RowLeReqMotorCtrlTilt', 'SeatAdj2RowLeReqMotorCtrlBack', 'SeatAdj2RowLeReqMotorCtrlLen', 'SeatAdj2RowLeReqMotorCtrlCLA', 'SeatAdj2RowLeReqMotorCtrlOTTOAg', 'SeatAdj2RowLeReqMotorCtrlRe', 'SeatAdj2RowLeReqMotorCtrlOTF', 'SeatAdj2RowLeReqMotorCtrlHei']}

    class SeatAdj2RowLeReqMotorCtrlOTTOLen:
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

    class SeatAdj2RowLeReqMotorCtrlTilt:
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

    class SeatAdj2RowLeReqMotorCtrlBack:
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

    class SeatAdj2RowLeReqMotorCtrlLen:
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

    class SeatAdj2RowLeReqMotorCtrlCLA:
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

    class SeatAdj2RowLeReqMotorCtrlOTTOAg:
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

    class SeatAdj2RowLeReqMotorCtrlRe:
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

    class SeatAdj2RowLeReqMotorCtrlOTF:
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

    class SeatAdj2RowLeReqMotorCtrlHei:
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


class CCUSOCCDToLCULEthSignalIPdu13:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x40500D
    pdu_length_bytes = 1
    receiver = ['LCUL']
    send_type = "EventTriggered"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {}

    class ActvReSplrSeldCmd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Setting ActiveWing Mode"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' ActvReSplrSeldCmd_OFF', '0x1': ' ActvReSplrSeldCmd_ON', '0x2': ' ActvReSplrSeldCmd_AUTO'}


class CCUSOCCDToLCULEthSignalIPdu81:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405051
    pdu_length_bytes = 4
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {'SeatAdj3RowLeReq': ['SeatAdj3RowLeReqMotorCtrlOTTOAg', 'SeatAdj3RowLeReqMotorCtrlTilt', 'SeatAdj3RowLeReqMotorCtrlHei', 'SeatAdj3RowLeReqMotorCtrlOTTOLen', 'SeatAdj3RowLeReqMotorCtrlLen', 'SeatAdj3RowLeReqMotorCtrlCLA', 'SeatAdj3RowLeReqMotorCtrlOTF', 'SeatAdj3RowLeReqMotorCtrlBack', 'SeatAdj3RowLeReqMotorCtrlRe']}

    class SeatAdj3RowLeReqMotorCtrlOTTOAg:
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

    class SeatAdj3RowLeReqMotorCtrlTilt:
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

    class SeatAdj3RowLeReqMotorCtrlHei:
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

    class SeatAdj3RowLeReqMotorCtrlOTTOLen:
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

    class SeatAdj3RowLeReqMotorCtrlLen:
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

    class SeatAdj3RowLeReqMotorCtrlCLA:
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

    class SeatAdj3RowLeReqMotorCtrlOTF:
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

    class SeatAdj3RowLeReqMotorCtrlBack:
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

    class SeatAdj3RowLeReqMotorCtrlRe:
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


class CCUSOCCDToLCULEthSignalIPdu83:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405053
    pdu_length_bytes = 1
    receiver = ['LCUL']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {}

    class SeatAdjLe2RowAntiPinchEna:
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


class CCUSOCCDToLCULEthSignalIPdu85:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405055
    pdu_length_bytes = 9
    receiver = ['LCUL']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {'SeatClimaLeReqFromSrv': ['SeatClimaLeReqFromSrvHeatgTSet3Row', 'SeatClimaLeReqFromSrvVentOnOff3Row', 'SeatClimaLeReqFromSrvHeatgTSet1Row', 'SeatClimaLeReqFromSrvVentPwmSet2Row', 'SeatClimaLeReqFromSrvVentPwmSet3Row', 'SeatClimaLeReqFromSrvHeatgOnOff3Row', 'SeatClimaLeReqFromSrvVentPwmSet1Row', 'SeatClimaLeReqFromSrvHeatgOnOff1Row', 'SeatClimaLeReqFromSrvVentOnOff1Row', 'SeatClimaLeReqFromSrvHeatgTSet2Row', 'SeatClimaLeReqFromSrvHeatgOnOff2Row', 'SeatClimaLeReqFromSrvVentOnOff2Row']}

    class SeatClimaLeReqFromSrvHeatgTSet3Row:
        comments = ""
        factor = 0.1
        initial_value = 400
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -40
        sig_ub = None
        signal_description = "Third Row Left Side Seat Heating Temperature Setting From Service"
        signal_length = 11
        start_position = 30
        value_definition = {}

    class SeatClimaLeReqFromSrvVentOnOff3Row:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Third Row Left Side Seat Venting On-Off Setting From Service"
        signal_length = 1
        start_position = 33
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class SeatClimaLeReqFromSrvHeatgTSet1Row:
        comments = ""
        factor = 0.1
        initial_value = 400
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -40
        sig_ub = None
        signal_description = "First Row Left Side Seat Heating Temperature Setting From Service"
        signal_length = 11
        start_position = 4
        value_definition = {}

    class SeatClimaLeReqFromSrvVentPwmSet2Row:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Second Row Left Side Seat Venting Pwm Setting From Service"
        signal_length = 10
        start_position = 53
        value_definition = {}

    class SeatClimaLeReqFromSrvVentPwmSet3Row:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Third Row Left Side Seat Venting Pwm Setting From Service"
        signal_length = 10
        start_position = 59
        value_definition = {}

    class SeatClimaLeReqFromSrvHeatgOnOff3Row:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Third Row Left Side Seat Heating On-Off Setting From Service"
        signal_length = 1
        start_position = 5
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class SeatClimaLeReqFromSrvVentPwmSet1Row:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "First Row Left Side Seat Venting Pwm Setting From Service"
        signal_length = 10
        start_position = 47
        value_definition = {}

    class SeatClimaLeReqFromSrvHeatgOnOff1Row:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "First Row Left Side Seat Heating On-Off Setting From Service"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class SeatClimaLeReqFromSrvVentOnOff1Row:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "First Row Left Side Seat Venting On-Off Setting From Service"
        signal_length = 1
        start_position = 35
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class SeatClimaLeReqFromSrvHeatgTSet2Row:
        comments = ""
        factor = 0.1
        initial_value = 400
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -40
        sig_ub = None
        signal_description = "Second Row Left Side Seat Heating Temperature Setting From Service"
        signal_length = 11
        start_position = 9
        value_definition = {}

    class SeatClimaLeReqFromSrvHeatgOnOff2Row:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Second Row Left Side Seat Heating On-Off Setting From Service"
        signal_length = 1
        start_position = 6
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class SeatClimaLeReqFromSrvVentOnOff2Row:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Second Row Left Side Seat Venting On-Off Setting From Service"
        signal_length = 1
        start_position = 34
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}


class CCUSOCCDToLCULEthSignalIPdu82:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405052
    pdu_length_bytes = 1
    receiver = ['LCUL']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {}

    class SeatAdjLe1RowAntiPinchEna:
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


class CCUSOCCDToLCULEthSignalIPdu84:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405054
    pdu_length_bytes = 1
    receiver = ['LCUL']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {}

    class SeatAdjLe3RowAntiPinchEna:
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


class CCUSOCCDToLCULEthSignalIPdu89:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405059
    pdu_length_bytes = 1
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {'SeatMassgReqReLe': ['SeatMassgReqReLeReqLvl', 'SeatMassgReqReLeMassgProg']}

    class SeatMassgReqReLeReqLvl:
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

    class SeatMassgReqReLeMassgProg:
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


class CCUSOCCDToLCULEthSignalIPdu90:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x40505A
    pdu_length_bytes = 3
    receiver = ['LCUL']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {'SftyBltTensionCtrl': ['SftyBltTensionCtrlF', 'SftyBltTensionCtrlTi']}

    class SftyBltTensionCtrlF:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "force"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class SftyBltTensionCtrlTi:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "time"
        signal_length = 16
        start_position = 15
        value_definition = {}


class CCUSOCCDToLCULEthSignalIPdu86:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405056
    pdu_length_bytes = 1
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {}

    class SeatLumReqFrntLe:
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


class CCUSOCCDToLCULEthSignalIPdu88:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405058
    pdu_length_bytes = 1
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {'SeatMassgReqFrntLe': ['SeatMassgReqFrntLeReqLvl', 'SeatMassgReqFrntLeMassgProg']}

    class SeatMassgReqFrntLeReqLvl:
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

    class SeatMassgReqFrntLeMassgProg:
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


class CCUSOCCDToLCULEthSignalIPdu87:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405057
    pdu_length_bytes = 1
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {}

    class SeatLumReqReLe:
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


class CCUSOCCDToLCULEthSignalIPdu92:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x40505C
    pdu_length_bytes = 1
    receiver = ['LCUL']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {}

    class SteerWhlAdjAgReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "SteerWheel Angle Adjustment Request"
        signal_length = 3
        start_position = 7
        value_definition = {'0x0': ' MotorCmd_IDLE', '0x1': ' MotorCmd_Positiv', '0x2': ' MotorCmd_Negativ', '0x3': ' MotorCmd_Reserved'}


class CCUSOCCDToLCULEthSignalIPdu91:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x40505B
    pdu_length_bytes = 6
    receiver = ['LCUL']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {'SftyBltVibrationCtrl': ['SftyBltVibrationCtrlFrq', 'SftyBltVibrationCtrlTi', 'SftyBltVibrationCtrlF']}

    class SftyBltVibrationCtrlFrq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "frequency"
        signal_length = 16
        start_position = 15
        value_definition = {}

    class SftyBltVibrationCtrlTi:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "time"
        signal_length = 16
        start_position = 31
        value_definition = {}

    class SftyBltVibrationCtrlF:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "force"
        signal_length = 8
        start_position = 7
        value_definition = {}


class CCUSOCCDToLCULEthSignalIPdu99:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405063
    pdu_length_bytes = 1
    receiver = ['LCUL']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {}

    class TowBarReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Tow Bar (Fold/Unfold)Request"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' TowBarReqType_NoReq', '0x1': ' TowBarReqType_Unfold', '0x2': ' TowBarReqType_Fold'}


class CCUSOCCDToLCULEthSignalIPdu98:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405062
    pdu_length_bytes = 4
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {'SteerWhlRiSymbolLightCtrl': ['SteerWhlRiSymbolLightCtrlBlue', 'SteerWhlRiSymbolLightCtrlGreen', 'SteerWhlRiSymbolLightCtrlBrightness', 'SteerWhlRiSymbolLightCtrlRed']}

    class SteerWhlRiSymbolLightCtrlBlue:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "RGB中B值"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class SteerWhlRiSymbolLightCtrlGreen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "RGB中G值"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class SteerWhlRiSymbolLightCtrlBrightness:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "背光亮度值"
        signal_length = 7
        start_position = 15
        value_definition = {}

    class SteerWhlRiSymbolLightCtrlRed:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "RGB中R值"
        signal_length = 8
        start_position = 31
        value_definition = {}


class CCUSOCCDToLCULEthSignalIPdu95:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x40505F
    pdu_length_bytes = 2
    receiver = ['LCUL']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {}

    class SteerWhlClimaHeatgTsetFromSrv:
        comments = ""
        factor = 0.1
        initial_value = 400
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -40
        sig_ub = None
        signal_description = "Steering Wheel Heating Temperature Setting From Service"
        signal_length = 11
        start_position = 7
        value_definition = {}


class CCUSOCCDToLCULEthSignalIPdu94:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x40505E
    pdu_length_bytes = 1
    receiver = ['LCUL']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {}

    class SteerWhlClimaHeatgReqFromSrv:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Steering Wheel Heating OnOff Request From Service"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}


class CCUSOCCDToLCULEthSignalIPdu96:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405060
    pdu_length_bytes = 4
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {'SteerWhlLeLightingBarCtrl': ['SteerWhlLeLightingBarCtrlGreen', 'SteerWhlLeLightingBarCtrlBlue', 'SteerWhlLeLightingBarCtrlRed', 'SteerWhlLeLightingBarCtrlBrightness']}

    class SteerWhlLeLightingBarCtrlGreen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "RGB中G值"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class SteerWhlLeLightingBarCtrlBlue:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "RGB中B值"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class SteerWhlLeLightingBarCtrlRed:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "RGB中R值"
        signal_length = 8
        start_position = 31
        value_definition = {}

    class SteerWhlLeLightingBarCtrlBrightness:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "背光亮度值"
        signal_length = 7
        start_position = 15
        value_definition = {}


class CCUSOCCDToLCULEthSignalIPdu97:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405061
    pdu_length_bytes = 4
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {'SteerWhlLeSymbolLightCtrl': ['SteerWhlLeSymbolLightCtrlBrightness', 'SteerWhlLeSymbolLightCtrlGreen', 'SteerWhlLeSymbolLightCtrlBlue', 'SteerWhlLeSymbolLightCtrlRed']}

    class SteerWhlLeSymbolLightCtrlBrightness:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "背光亮度值"
        signal_length = 7
        start_position = 15
        value_definition = {}

    class SteerWhlLeSymbolLightCtrlGreen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "RGB中G值"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class SteerWhlLeSymbolLightCtrlBlue:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "RGB中B值"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class SteerWhlLeSymbolLightCtrlRed:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "RGB中R值"
        signal_length = 8
        start_position = 31
        value_definition = {}


class CCUSOCCDToLCULEthSignalIPdu93:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x40505D
    pdu_length_bytes = 1
    receiver = ['LCUL']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {}

    class SteerWhlAdjLenReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "SteerWheel Length Adjustment Request"
        signal_length = 3
        start_position = 7
        value_definition = {'0x0': ' MotorCmd_IDLE', '0x1': ' MotorCmd_Positiv', '0x2': ' MotorCmd_Negativ', '0x3': ' MotorCmd_Reserved'}


class CCUSOCCDToLCULEthSignalIPdu104:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405068
    pdu_length_bytes = 4
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {'TweeterLeUpprALMRGBL': ['TweeterLeUpprALMRGBLGreen', 'TweeterLeUpprALMRGBLLuminance', 'TweeterLeUpprALMRGBLBlue', 'TweeterLeUpprALMRGBLRed']}

    class TweeterLeUpprALMRGBLGreen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Green,TweeterLeUpprALMRGBL"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class TweeterLeUpprALMRGBLLuminance:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Luminance,TweeterLeUpprALMRGBL"
        signal_length = 7
        start_position = 23
        value_definition = {}

    class TweeterLeUpprALMRGBLBlue:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Blue,TweeterLeUpprALMRGBL"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class TweeterLeUpprALMRGBLRed:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Red,TweeterLeUpprALMRGBL"
        signal_length = 8
        start_position = 31
        value_definition = {}


class CCUSOCCDToLCULEthSignalIPdu108:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x40506C
    pdu_length_bytes = 1
    receiver = ['LCUL']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {}

    class WiprMotFrntOffsAg:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Information to calibrate the upper reversal position of the wiper arm by introducing an offset to the wiper crank angle in the upper reversal position."
        signal_length = 4
        start_position = 7
        value_definition = {}


class CCUSOCCDToLCULEthSignalIPdu106:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x40506A
    pdu_length_bytes = 1
    receiver = ['LCUL']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {}

    class WinLockAutoClsEnable:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Request On Auto Close Window When Lock"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}


class CCUSOCCDToLCULEthSignalIPdu102:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405066
    pdu_length_bytes = 4
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {'TweeterLeBotmALMRGBL': ['TweeterLeBotmALMRGBLGreen', 'TweeterLeBotmALMRGBLLuminance', 'TweeterLeBotmALMRGBLRed', 'TweeterLeBotmALMRGBLBlue']}

    class TweeterLeBotmALMRGBLGreen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Green,TweeterLeBotmALMRGBL"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class TweeterLeBotmALMRGBLLuminance:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Luminance,TweeterLeBotmALMRGBL"
        signal_length = 7
        start_position = 23
        value_definition = {}

    class TweeterLeBotmALMRGBLRed:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Red,TweeterLeBotmALMRGBL"
        signal_length = 8
        start_position = 31
        value_definition = {}

    class TweeterLeBotmALMRGBLBlue:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Blue,TweeterLeBotmALMRGBL"
        signal_length = 8
        start_position = 7
        value_definition = {}


class CCUSOCCDToLCULEthSignalIPdu109:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x40506D
    pdu_length_bytes = 1
    receiver = ['LCUL']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {}

    class WiprPosnForSrvReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "front wiper server position ,ON or OFF"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}


class CCUSOCCDToLCULEthSignalIPdu105:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405069
    pdu_length_bytes = 3
    receiver = ['LCUL']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {'WindCorrnVal': ['WindCorrnValAmb', 'WindCorrnValFrnt', 'WindCorrnValHud']}

    class WindCorrnValAmb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "The transmittance parameter of ambient sensor related front windshield"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class WindCorrnValFrnt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "The transmittance parameter of Forward sensor related front windshield"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class WindCorrnValHud:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "The transmittance parameter of HUD sensor related front windshield"
        signal_length = 8
        start_position = 23
        value_definition = {}


class CCUSOCCDToLCULEthSignalIPdu100:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405064
    pdu_length_bytes = 1
    receiver = ['LCUL']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {}

    class TrlrFctChkReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Trailer Function Check Request"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' ReqSts1_NotReqd', '0x1': ' ReqSts1_Reqd'}


class CCUSOCCDToLCULEthSignalIPdu101:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405065
    pdu_length_bytes = 4
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {'TweeterLeALMRGBL': ['TweeterLeALMRGBLLuminance', 'TweeterLeALMRGBLRed', 'TweeterLeALMRGBLGreen', 'TweeterLeALMRGBLBlue']}

    class TweeterLeALMRGBLLuminance:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Luminance,,tweeter left alm"
        signal_length = 7
        start_position = 23
        value_definition = {}

    class TweeterLeALMRGBLRed:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Red,tweeter left alm"
        signal_length = 8
        start_position = 31
        value_definition = {}

    class TweeterLeALMRGBLGreen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Geen,,tweeter left alm"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class TweeterLeALMRGBLBlue:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Blue,,tweeter left alm"
        signal_length = 8
        start_position = 7
        value_definition = {}


class CCUSOCCDToLCULEthSignalIPdu107:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x40506B
    pdu_length_bytes = 1
    receiver = ['LCUL']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {}

    class WinRainAutoClsEnable:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "window rain auto close enable"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' EnableDisable3_Invalid', '0x1': ' EnableDisable3_Disabled', '0x2': ' EnableDisable3_Enabled'}


class CCUSOCCDToLCULEthSignalIPdu103:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405067
    pdu_length_bytes = 4
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {'TweeterLeMidALMRGBL': ['TweeterLeMidALMRGBLRed', 'TweeterLeMidALMRGBLBlue', 'TweeterLeMidALMRGBLLuminance', 'TweeterLeMidALMRGBLGreen']}

    class TweeterLeMidALMRGBLRed:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Red,TweeterLeMidALMRGBL"
        signal_length = 8
        start_position = 31
        value_definition = {}

    class TweeterLeMidALMRGBLBlue:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Blue,TweeterLeMidALMRGBL"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class TweeterLeMidALMRGBLLuminance:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Luminance,TweeterLeMidALMRGBL"
        signal_length = 7
        start_position = 23
        value_definition = {}

    class TweeterLeMidALMRGBLGreen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Green,TweeterLeMidALMRGBL"
        signal_length = 8
        start_position = 15
        value_definition = {}


class CCUSOCCDToLCULEthSignalIPdu114:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405072
    pdu_length_bytes = 1
    receiver = ['LCUL']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
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


class CCUSOCCDToLCULEthSignalIPdu117:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405075
    pdu_length_bytes = 3
    receiver = ['LCUL']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
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


class CCUSOCCDToLCULEthSignalIPdu110:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x40506E
    pdu_length_bytes = 5
    receiver = ['LCUL']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
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
        start_position = 19
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
        start_position = 13
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
        start_position = 25
        value_definition = {}


class CCUSOCCDToLCULEthSignalIPdu115:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405073
    pdu_length_bytes = 2
    receiver = ['LCUL']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
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


class CCUSOCCDToLCULEthSignalIPdu111:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x40506F
    pdu_length_bytes = 5
    receiver = ['LCUL']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
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
        start_position = 25
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
        start_position = 19
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
        start_position = 13
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


class CCUSOCCDToLCULEthSignalIPdu116:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405074
    pdu_length_bytes = 2
    receiver = ['LCUL']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
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


class CCUSOCCDToLCULEthSignalIPdu112:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405070
    pdu_length_bytes = 1
    receiver = ['LCUL']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
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


class CCUSOCCDToLCULEthSignalIPdu113:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405071
    pdu_length_bytes = 1
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
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


class CCUSOCCDToLCULEthSignalIPdu29:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x40501D
    pdu_length_bytes = 1
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {'DualSunroofCurtlrnCmd': ['DualSunroofCurtlrnCmdFrntLrnCmd', 'DualSunroofCurtlrnCmdRearLrnCmd']}

    class DualSunroofCurtlrnCmdFrntLrnCmd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "the learn command of the front sunroof curt"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' LrnCmd_NoCmd', '0x1': ' LrnCmd_ClrCmd', '0x2': ' LrnCmd_LrngCmd', '0x3': ' LrnCmd_Resd'}

    class DualSunroofCurtlrnCmdRearLrnCmd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "the learn command of the rear sunroof curt"
        signal_length = 2
        start_position = 5
        value_definition = {'0x0': ' LrnCmd_NoCmd', '0x1': ' LrnCmd_ClrCmd', '0x2': ' LrnCmd_LrngCmd', '0x3': ' LrnCmd_Resd'}


class CCUSOCCDToLCULEthSignalIPdu55:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405037
    pdu_length_bytes = 4
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {'IPFrntALMRGBL': ['IPFrntALMRGBLGreen', 'IPFrntALMRGBLBlue', 'IPFrntALMRGBLLuminance', 'IPFrntALMRGBLRed']}

    class IPFrntALMRGBLGreen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Green,IPFrntALMRGBL"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class IPFrntALMRGBLBlue:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Blue,IPFrntALMRGBL"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class IPFrntALMRGBLLuminance:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Luminance,IPFrntALMRGBL"
        signal_length = 7
        start_position = 23
        value_definition = {}

    class IPFrntALMRGBLRed:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Red,IPFrntALMRGBL"
        signal_length = 8
        start_position = 31
        value_definition = {}


class CCUSOCCDToLCULEthSignalIPdu31:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x40501F
    pdu_length_bytes = 1
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {}

    class ExtrReViewMirrDirAdjCmdDrvr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "external rear view mirror orientation adjustment at driver side"
        signal_length = 3
        start_position = 7
        value_definition = {'0x0': ' DirCmd_NoCmd', '0x1': ' DirCmd_Stop', '0x2': ' DirCmd_Left', '0x3': ' DirCmd_Right', '0x4': ' DirCmd_Up', '0x5': ' DirCmd_Down'}


class CCUSOCCDToLCULEthSignalIPdu33:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405021
    pdu_length_bytes = 1
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {}

    class ExtrReViewMirrFoldRemCmdDrvr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Automatic folding command for external rear view mirror at driver side"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' MirrFodCmd_Idle', '0x1': ' MirrFodCmd_Fold', '0x2': ' MirrFodCmd_Unfold'}


class CCUSOCCDToLCULEthSignalIPdu38:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405026
    pdu_length_bytes = 2
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {'FootwellLiFrntRiCmd': ['FootwellLiFrntRiCmdLightCmd', 'FootwellLiFrntRiCmdReadingLiDimsSpdCmd', 'FootwellLiFrntRiCmdLiPerc']}

    class FootwellLiFrntRiCmdLightCmd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Light cmd"
        signal_length = 4
        start_position = 7
        value_definition = {'0x0': ' LightCmd_NoReq', '0x1': ' LightCmd_ON', '0x2': ' LightCmd_OFF', '0x3': ' LightCmd_TBD'}

    class FootwellLiFrntRiCmdReadingLiDimsSpdCmd:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "dim speed of footwell light"
        signal_length = 3
        start_position = 3
        value_definition = {'0x0': ' ReadingLiDimsSpdCmd_NoCmd', '0x1': ' ReadingLiDimsSpdCmd_400ms', '0x2': ' ReadingLiDimsSpdCmd_800ms', '0x3': ' ReadingLiDimsSpdCmd_1000ms', '0x4': ' ReadingLiDimsSpdCmd_2000ms', '0x5': ' ReadingLiDimsSpdCmd_Resverd'}

    class FootwellLiFrntRiCmdLiPerc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "illumination percent"
        signal_length = 7
        start_position = 15
        value_definition = {}


class CCUSOCCDToLCULEthSignalIPdu57:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405039
    pdu_length_bytes = 1
    receiver = ['LCUL']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {}

    class LeSpkrRiseOrFallCtrl:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "The left Speaker Elevating Command"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' RiseOrFallControl_Stop', '0x1': ' RiseOrFallControl_Rise', '0x2': ' RiseOrFallControl_Fall', '0x3': ' RiseOrFallControl_Reserved'}


class CCUSOCCDToLCULEthSignalIPdu45:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x40502D
    pdu_length_bytes = 1
    receiver = ['LCUL']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {}

    class FrntWiperSingleScrape:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Front Wiper Single Scrape"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}


class CCUSOCCDToLCULEthSignalIPdu46:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x40502E
    pdu_length_bytes = 1
    receiver = ['LCUL']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {}

    class FrntWshrActvnSafe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "to activate the front washing"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' OnOffNoCmd_NoCmd', '0x1': ' OnOffNoCmd_OFF', '0x2': ' OnOffNoCmd_ON'}


class CCUSOCCDToLCULEthSignalIPdu35:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405023
    pdu_length_bytes = 1
    receiver = ['LCUL']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {}

    class FLDoorManResistCtrl:
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


class CCUSOCCDToLCULEthSignalIPdu39:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405027
    pdu_length_bytes = 2
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {'FootwellLiSecLeCmd': ['FootwellLiSecLeCmdLiPerc', 'FootwellLiSecLeCmdLightCmd', 'FootwellLiSecLeCmdReadingLiDimsSpdCmd']}

    class FootwellLiSecLeCmdLiPerc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "illumination percent"
        signal_length = 7
        start_position = 7
        value_definition = {}

    class FootwellLiSecLeCmdLightCmd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Light cmd"
        signal_length = 4
        start_position = 15
        value_definition = {'0x0': ' LightCmd_NoReq', '0x1': ' LightCmd_ON', '0x2': ' LightCmd_OFF', '0x3': ' LightCmd_TBD'}

    class FootwellLiSecLeCmdReadingLiDimsSpdCmd:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "dim speed of footwell light"
        signal_length = 3
        start_position = 11
        value_definition = {'0x0': ' ReadingLiDimsSpdCmd_NoCmd', '0x1': ' ReadingLiDimsSpdCmd_400ms', '0x2': ' ReadingLiDimsSpdCmd_800ms', '0x3': ' ReadingLiDimsSpdCmd_1000ms', '0x4': ' ReadingLiDimsSpdCmd_2000ms', '0x5': ' ReadingLiDimsSpdCmd_Resverd'}


class CCUSOCCDToLCULEthSignalIPdu47:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x40502F
    pdu_length_bytes = 5
    receiver = ['LCUL']
    send_type = "Cyclic-20ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {'FuncReqOfHorn': ['FuncReqOfHornNTimePrm', 'FuncReqOfHornPriority', 'FuncReqOfHornOffTimePrm', 'FuncReqOfHornCmd', 'FuncReqOfHornOnTimePrm']}

    class FuncReqOfHornNTimePrm:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "N time parameter"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class FuncReqOfHornPriority:
        comments = ""
        factor = 1.0
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "priority info"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class FuncReqOfHornOffTimePrm:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "offtime parameter"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class FuncReqOfHornCmd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "command"
        signal_length = 4
        start_position = 31
        value_definition = {'0x0': ' LightCmd_NoReq', '0x1': ' LightCmd_ON', '0x2': ' LightCmd_OFF', '0x3': ' LightCmd_TBD'}

    class FuncReqOfHornOnTimePrm:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "ontime parameter"
        signal_length = 8
        start_position = 39
        value_definition = {}


class CCUSOCCDToLCULEthSignalIPdu48:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405030
    pdu_length_bytes = 2
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {'FuncReqOfLicensePlateLamp': ['FuncReqOfLicensePlateLampLightID1', 'FuncReqOfLicensePlateLampLightPriority', 'FuncReqOfLicensePlateLampLightCmd']}

    class FuncReqOfLicensePlateLampLightID1:
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

    class FuncReqOfLicensePlateLampLightPriority:
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

    class FuncReqOfLicensePlateLampLightCmd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "LightCmd"
        signal_length = 4
        start_position = 3
        value_definition = {'0x0': ' LightCmd_NoReq', '0x1': ' LightCmd_ON', '0x2': ' LightCmd_OFF', '0x3': ' LightCmd_TBD'}


class CCUSOCCDToLCULEthSignalIPdu19:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405013
    pdu_length_bytes = 4
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {'CpilSaucerLeALMRGBL': ['CpilSaucerLeALMRGBLGreen', 'CpilSaucerLeALMRGBLRed', 'CpilSaucerLeALMRGBLBlue', 'CpilSaucerLeALMRGBLLuminance']}

    class CpilSaucerLeALMRGBLGreen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Green,CpilSaucerLeALMRGBL"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class CpilSaucerLeALMRGBLRed:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "RED,CpilSaucerLeALMRGBL"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class CpilSaucerLeALMRGBLBlue:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Blue,CpilSaucerLeALMRGBL"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class CpilSaucerLeALMRGBLLuminance:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Luminance,CpilSaucerLeALMRGBL"
        signal_length = 7
        start_position = 31
        value_definition = {}


class CCUSOCCDToLCULEthSignalIPdu37:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405025
    pdu_length_bytes = 4
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {'FootwellFirstLeALMRGBL': ['FootwellFirstLeALMRGBLLuminance', 'FootwellFirstLeALMRGBLBlue', 'FootwellFirstLeALMRGBLRed', 'FootwellFirstLeALMRGBLGreen']}

    class FootwellFirstLeALMRGBLLuminance:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Luminance,FootwellFirstLeALMRGBL"
        signal_length = 7
        start_position = 7
        value_definition = {}

    class FootwellFirstLeALMRGBLBlue:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Blue,FootwellFirstLeALMRGBL"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class FootwellFirstLeALMRGBLRed:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Red,FootwellFirstLeALMRGBL"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class FootwellFirstLeALMRGBLGreen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Green,FootwellFirstLeALMRGBL"
        signal_length = 8
        start_position = 31
        value_definition = {}


class CCUSOCCDToLCULEthSignalIPdu22:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405016
    pdu_length_bytes = 1
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {}

    class DefrstReCmd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "the defrosting conmand of the rear windshield"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' OffOnCmd_NoCmd', '0x1': ' OffOnCmd_Off', '0x2': ' OffOnCmd_On'}


class CCUSOCCDToLCULEthSignalIPdu20:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405014
    pdu_length_bytes = 2
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {'DayNightServiceSts': ['DayNightServiceStsOutdBriSts', 'DayNightServiceStsChks', 'DayNightServiceStsCntr']}

    class DayNightServiceStsOutdBriSts:
        comments = ""
        factor = 1.0
        initial_value = 3
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "DayNightStatus"
        signal_length = 2
        start_position = 11
        value_definition = {'0x0': ' OutdBriSts_Ukwn', '0x1': ' OutdBriSts_Night', '0x2': ' OutdBriSts_Day', '0x3': ' OutdBriSts_Invld'}

    class DayNightServiceStsChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "checksum"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class DayNightServiceStsCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "counter"
        signal_length = 4
        start_position = 15
        value_definition = {}


class CCUSOCCDToLCULEthSignalIPdu50:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405032
    pdu_length_bytes = 6
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {'FuncReqOfOuterDoorSwLampFR': ['FuncReqOfOuterDoorSwLampFRLightParameterPerc1', 'FuncReqOfOuterDoorSwLampFROnTime1', 'FuncReqOfOuterDoorSwLampFRLightMode', 'FuncReqOfOuterDoorSwLampFRLightPriority', 'FuncReqOfOuterDoorSwLampFRLightParameterPerc2', 'FuncReqOfOuterDoorSwLampFROnTime2']}

    class FuncReqOfOuterDoorSwLampFRLightParameterPerc1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "FunctionParameter1"
        signal_length = 7
        start_position = 7
        value_definition = {}

    class FuncReqOfOuterDoorSwLampFROnTime1:
        comments = ""
        factor = 1.0
        initial_value = 50
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "OnTimePrm1"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class FuncReqOfOuterDoorSwLampFRLightMode:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "LightCmd"
        signal_length = 8
        start_position = 23
        value_definition = {'0x0': ' LightMode_OFF', '0x1': ' LightMode_ON', '0x2': ' LightMode_FLASH', '0x3': ' LightMode_BREATH1', '0x4': ' LightMode_BREATH2', '0x5': ' LightMode_Reserved1', '0xFF': ' LightMode_Reserved'}

    class FuncReqOfOuterDoorSwLampFRLightPriority:
        comments = ""
        factor = 1.0
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "LightPriority"
        signal_length = 8
        start_position = 31
        value_definition = {}

    class FuncReqOfOuterDoorSwLampFRLightParameterPerc2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "FunctionParameter2"
        signal_length = 7
        start_position = 39
        value_definition = {}

    class FuncReqOfOuterDoorSwLampFROnTime2:
        comments = ""
        factor = 1.0
        initial_value = 50
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "OnTimePrm2"
        signal_length = 8
        start_position = 47
        value_definition = {}


class CCUSOCCDToLCULEthSignalIPdu26:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x40501A
    pdu_length_bytes = 4
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {'DoorMapBeltFrntLeALMRGBL': ['DoorMapBeltFrntLeALMRGBLLuminance', 'DoorMapBeltFrntLeALMRGBLGreen', 'DoorMapBeltFrntLeALMRGBLBlue', 'DoorMapBeltFrntLeALMRGBLRed']}

    class DoorMapBeltFrntLeALMRGBLLuminance:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Luminance,DoorMapBeltFrntLeALMRGBL"
        signal_length = 7
        start_position = 7
        value_definition = {}

    class DoorMapBeltFrntLeALMRGBLGreen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Green,DoorMapBeltFrntLeALMRGBL"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class DoorMapBeltFrntLeALMRGBLBlue:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Blue,DoorMapBeltFrntLeALMRGBL"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class DoorMapBeltFrntLeALMRGBLRed:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Red,DoorMapBeltFrntLeALMRGBL"
        signal_length = 8
        start_position = 31
        value_definition = {}


class CCUSOCCDToLCULEthSignalIPdu36:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405024
    pdu_length_bytes = 1
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {}

    class FLPwrSideDoorMaxPosnSet:
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


class CCUSOCCDToLCULEthSignalIPdu27:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x40501B
    pdu_length_bytes = 4
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {'DoorMapBeltRearLeALMRGBL': ['DoorMapBeltRearLeALMRGBLLuminance', 'DoorMapBeltRearLeALMRGBLBlue', 'DoorMapBeltRearLeALMRGBLRed', 'DoorMapBeltRearLeALMRGBLGreen']}

    class DoorMapBeltRearLeALMRGBLLuminance:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Luminance,DoorMapBeltRearLeALMRGBL"
        signal_length = 7
        start_position = 7
        value_definition = {}

    class DoorMapBeltRearLeALMRGBLBlue:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Blue,DoorMapBeltRearLeALMRGBL"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class DoorMapBeltRearLeALMRGBLRed:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "RED,DoorMapBeltRearLeALMRGBL"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class DoorMapBeltRearLeALMRGBLGreen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Green,DoorMapBeltRearLeALMRGBL"
        signal_length = 8
        start_position = 31
        value_definition = {}


class CCUSOCCDToLCULEthSignalIPdu24:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405018
    pdu_length_bytes = 4
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {'DoorArmrestRearLeALMRGBL': ['DoorArmrestRearLeALMRGBLBlue', 'DoorArmrestRearLeALMRGBLGreen', 'DoorArmrestRearLeALMRGBLLuminance', 'DoorArmrestRearLeALMRGBLRed']}

    class DoorArmrestRearLeALMRGBLBlue:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Blue,DoorArmrestRearLeALMRGBL"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class DoorArmrestRearLeALMRGBLGreen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Green,DoorArmrestRearLeALMRGBL"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class DoorArmrestRearLeALMRGBLLuminance:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Luminance,DoorArmrestRearLeALMRGBL"
        signal_length = 7
        start_position = 23
        value_definition = {}

    class DoorArmrestRearLeALMRGBLRed:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Red,DoorArmrestRearLeALMRGBL"
        signal_length = 8
        start_position = 31
        value_definition = {}


class CCUSOCCDToLCULEthSignalIPdu43:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x40502B
    pdu_length_bytes = 4
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {'FootwellSecLeALMRGBL': ['FootwellSecLeALMRGBLRed', 'FootwellSecLeALMRGBLBlue', 'FootwellSecLeALMRGBLLuminance', 'FootwellSecLeALMRGBLGreen']}

    class FootwellSecLeALMRGBLRed:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Red,FootwellSecLeALMRGBL"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class FootwellSecLeALMRGBLBlue:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Blue,FootwellSecLeALMRGBL"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class FootwellSecLeALMRGBLLuminance:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Luminance,FootwellSecLeALMRGBL"
        signal_length = 7
        start_position = 23
        value_definition = {}

    class FootwellSecLeALMRGBLGreen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Green,FootwellSecLeALMRGBL"
        signal_length = 8
        start_position = 31
        value_definition = {}


class CCUSOCCDToLCULEthSignalIPdu58:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x40503A
    pdu_length_bytes = 1
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {}

    class NormLeftPedalMoveCtrl:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "left pedal move control"
        signal_length = 3
        start_position = 7
        value_definition = {'0x0': ' ElecPedlCtrlReq_Idle', '0x1': ' ElecPedlCtrlReq_Open', '0x2': ' ElecPedlCtrlReq_Close', '0x3': ' ElecPedlCtrlReq_Resd1', '0x4': ' ElecPedlCtrlReq_Resd2', '0x5': ' ElecPedlCtrlReq_Resd3'}


class CCUSOCCDToLCULEthSignalIPdu15:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x40500F
    pdu_length_bytes = 1
    receiver = ['LCUL']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {}

    class CabinRefrigorDoorReqFromSrv:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Cabin Refrigerator Door Request From Service"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' DoorSts_Unknow', '0x1': ' DoorSts_Open', '0x2': ' DoorSts_Close'}


class CCUSOCCDToLCULEthSignalIPdu40:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405028
    pdu_length_bytes = 2
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {'FootwellLiSecRiCmd': ['FootwellLiSecRiCmdLightCmd', 'FootwellLiSecRiCmdLiPerc', 'FootwellLiSecRiCmdReadingLiDimsSpdCmd']}

    class FootwellLiSecRiCmdLightCmd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Light cmd"
        signal_length = 4
        start_position = 7
        value_definition = {'0x0': ' LightCmd_NoReq', '0x1': ' LightCmd_ON', '0x2': ' LightCmd_OFF', '0x3': ' LightCmd_TBD'}

    class FootwellLiSecRiCmdLiPerc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "illumination percent"
        signal_length = 7
        start_position = 15
        value_definition = {}

    class FootwellLiSecRiCmdReadingLiDimsSpdCmd:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "dim speed of footwell light"
        signal_length = 3
        start_position = 3
        value_definition = {'0x0': ' ReadingLiDimsSpdCmd_NoCmd', '0x1': ' ReadingLiDimsSpdCmd_400ms', '0x2': ' ReadingLiDimsSpdCmd_800ms', '0x3': ' ReadingLiDimsSpdCmd_1000ms', '0x4': ' ReadingLiDimsSpdCmd_2000ms', '0x5': ' ReadingLiDimsSpdCmd_Resverd'}


class CCUSOCCDToLCULEthSignalIPdu51:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405033
    pdu_length_bytes = 6
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {'FuncReqOfOuterDoorSwLampRL': ['FuncReqOfOuterDoorSwLampRLOnTime2', 'FuncReqOfOuterDoorSwLampRLOnTime1', 'FuncReqOfOuterDoorSwLampRLLightMode', 'FuncReqOfOuterDoorSwLampRLLightParameterPerc1', 'FuncReqOfOuterDoorSwLampRLLightParameterPerc2', 'FuncReqOfOuterDoorSwLampRLLightPriority']}

    class FuncReqOfOuterDoorSwLampRLOnTime2:
        comments = ""
        factor = 1.0
        initial_value = 50
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "OnTimePrm2"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class FuncReqOfOuterDoorSwLampRLOnTime1:
        comments = ""
        factor = 1.0
        initial_value = 50
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "OnTimePrm1"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class FuncReqOfOuterDoorSwLampRLLightMode:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "LightCmd"
        signal_length = 8
        start_position = 23
        value_definition = {'0x0': ' LightMode_OFF', '0x1': ' LightMode_ON', '0x2': ' LightMode_FLASH', '0x3': ' LightMode_BREATH1', '0x4': ' LightMode_BREATH2', '0x5': ' LightMode_Reserved1', '0xFF': ' LightMode_Reserved'}

    class FuncReqOfOuterDoorSwLampRLLightParameterPerc1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "FunctionParameter1"
        signal_length = 7
        start_position = 31
        value_definition = {}

    class FuncReqOfOuterDoorSwLampRLLightParameterPerc2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "FunctionParameter2"
        signal_length = 7
        start_position = 24
        value_definition = {}

    class FuncReqOfOuterDoorSwLampRLLightPriority:
        comments = ""
        factor = 1.0
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "LightPriority"
        signal_length = 8
        start_position = 47
        value_definition = {}


class CCUSOCCDToLCULEthSignalIPdu56:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405038
    pdu_length_bytes = 1
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {}

    class LeChdLockCtrlReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "left children lock control request "
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' LockCmd_Idle', '0x1': ' LockCmd_LockCmd', '0x2': ' LockCmd_UnLockCmd', '0x3': ' LockCmd_CrashUnLockCmd'}


class CCUSOCCDToLCULEthSignalIPdu42:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x40502A
    pdu_length_bytes = 2
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {'FootwellLiThrdRiCmd': ['FootwellLiThrdRiCmdReadingLiDimsSpdCmd', 'FootwellLiThrdRiCmdLiPerc', 'FootwellLiThrdRiCmdLightCmd']}

    class FootwellLiThrdRiCmdReadingLiDimsSpdCmd:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "dim speed of footwell light"
        signal_length = 3
        start_position = 7
        value_definition = {'0x0': ' ReadingLiDimsSpdCmd_NoCmd', '0x1': ' ReadingLiDimsSpdCmd_400ms', '0x2': ' ReadingLiDimsSpdCmd_800ms', '0x3': ' ReadingLiDimsSpdCmd_1000ms', '0x4': ' ReadingLiDimsSpdCmd_2000ms', '0x5': ' ReadingLiDimsSpdCmd_Resverd'}

    class FootwellLiThrdRiCmdLiPerc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "illumination percent"
        signal_length = 7
        start_position = 15
        value_definition = {}

    class FootwellLiThrdRiCmdLightCmd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Light cmd"
        signal_length = 4
        start_position = 4
        value_definition = {'0x0': ' LightCmd_NoReq', '0x1': ' LightCmd_ON', '0x2': ' LightCmd_OFF', '0x3': ' LightCmd_TBD'}


class CCUSOCCDToLCULEthSignalIPdu34:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405022
    pdu_length_bytes = 2
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {'ExtrReViewMirrTarAdjCmdDrvr': ['ExtrReViewMirrTarAdjCmdDrvrLeAndRi', 'ExtrReViewMirrTarAdjCmdDrvrUpAndDown']}

    class ExtrReViewMirrTarAdjCmdDrvrLeAndRi:
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

    class ExtrReViewMirrTarAdjCmdDrvrUpAndDown:
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


class CCUSOCCDToLCULEthSignalIPdu23:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405017
    pdu_length_bytes = 4
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {'DoorArmrestFrntLeALMRGBL': ['DoorArmrestFrntLeALMRGBLGreen', 'DoorArmrestFrntLeALMRGBLLuminance', 'DoorArmrestFrntLeALMRGBLBlue', 'DoorArmrestFrntLeALMRGBLRed']}

    class DoorArmrestFrntLeALMRGBLGreen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Green,DoorArmrestFrntLeALMRGBL"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class DoorArmrestFrntLeALMRGBLLuminance:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Luminance,DoorArmrestFrntLeALMRGBL"
        signal_length = 7
        start_position = 15
        value_definition = {}

    class DoorArmrestFrntLeALMRGBLBlue:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Blue,DoorArmrestFrntLeALMRGBL"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class DoorArmrestFrntLeALMRGBLRed:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Red,DoorArmrestFrntLeALMRGBL"
        signal_length = 8
        start_position = 31
        value_definition = {}


class CCUSOCCDToLCULEthSignalIPdu44:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x40502C
    pdu_length_bytes = 1
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {}

    class FrntSunroofCurtSwtCmd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "switch command of front sunroof curt"
        signal_length = 3
        start_position = 7
        value_definition = {'0x0': ' SunroofCurtSwtSts_Idle', '0x1': ' SunroofCurtSwtSts_OpenMan', '0x2': ' SunroofCurtSwtSts_OpenAut', '0x3': ' SunroofCurtSwtSts_ClsMan1', '0x4': ' SunroofCurtSwtSts_ClsMan2', '0x5': ' SunroofCurtSwtSts_Stop'}


class CCUSOCCDToLCULEthSignalIPdu18:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405012
    pdu_length_bytes = 4
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {'CpilLeALMRGBL': ['CpilLeALMRGBLGreen', 'CpilLeALMRGBLRed', 'CpilLeALMRGBLBlue', 'CpilLeALMRGBLLuminance']}

    class CpilLeALMRGBLGreen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Green,CpilLeALMRGBL"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class CpilLeALMRGBLRed:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Red,CpilLeALMRGBL"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class CpilLeALMRGBLBlue:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Blue,CpilLeALMRGBL"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class CpilLeALMRGBLLuminance:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Luminance,CpilLeALMRGBL"
        signal_length = 7
        start_position = 31
        value_definition = {}


class CCUSOCCDToLCULEthSignalIPdu21:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405015
    pdu_length_bytes = 1
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {}

    class DefrstDrvrCmd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "defrosting command of the driver side mirror"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' OffOnCmd_NoCmd', '0x1': ' OffOnCmd_Off', '0x2': ' OffOnCmd_On'}


class CCUSOCCDToLCULEthSignalIPdu17:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405011
    pdu_length_bytes = 4
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {'ConsoleMidLeALMRGBL': ['ConsoleMidLeALMRGBLBlue', 'ConsoleMidLeALMRGBLLuminance', 'ConsoleMidLeALMRGBLGreen', 'ConsoleMidLeALMRGBLRed']}

    class ConsoleMidLeALMRGBLBlue:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Blue,Console middle left alm"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class ConsoleMidLeALMRGBLLuminance:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Luminance,Console middle left alm"
        signal_length = 7
        start_position = 15
        value_definition = {}

    class ConsoleMidLeALMRGBLGreen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Green,Console middle left alm"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class ConsoleMidLeALMRGBLRed:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Red,Console middle left alm"
        signal_length = 8
        start_position = 31
        value_definition = {}


class CCUSOCCDToLCULEthSignalIPdu25:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405019
    pdu_length_bytes = 4
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {'DoorFrntLeALMRGBL': ['DoorFrntLeALMRGBLRed', 'DoorFrntLeALMRGBLBlue', 'DoorFrntLeALMRGBLLuminance', 'DoorFrntLeALMRGBLGreen']}

    class DoorFrntLeALMRGBLRed:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Red, front left ALM"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class DoorFrntLeALMRGBLBlue:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Blue,front left ALM"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class DoorFrntLeALMRGBLLuminance:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Luminance,front left ALM"
        signal_length = 7
        start_position = 23
        value_definition = {}

    class DoorFrntLeALMRGBLGreen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Green, front left ALM"
        signal_length = 8
        start_position = 31
        value_definition = {}


class CCUSOCCDToLCULEthSignalIPdu41:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405029
    pdu_length_bytes = 2
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {'FootwellLiThrdLeCmd': ['FootwellLiThrdLeCmdLiPerc', 'FootwellLiThrdLeCmdReadingLiDimsSpdCmd', 'FootwellLiThrdLeCmdLightCmd']}

    class FootwellLiThrdLeCmdLiPerc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "illumination percent"
        signal_length = 7
        start_position = 7
        value_definition = {}

    class FootwellLiThrdLeCmdReadingLiDimsSpdCmd:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "dim speed of footwell light"
        signal_length = 3
        start_position = 15
        value_definition = {'0x0': ' ReadingLiDimsSpdCmd_NoCmd', '0x1': ' ReadingLiDimsSpdCmd_400ms', '0x2': ' ReadingLiDimsSpdCmd_800ms', '0x3': ' ReadingLiDimsSpdCmd_1000ms', '0x4': ' ReadingLiDimsSpdCmd_2000ms', '0x5': ' ReadingLiDimsSpdCmd_Resverd'}

    class FootwellLiThrdLeCmdLightCmd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Light cmd"
        signal_length = 4
        start_position = 12
        value_definition = {'0x0': ' LightCmd_NoReq', '0x1': ' LightCmd_ON', '0x2': ' LightCmd_OFF', '0x3': ' LightCmd_TBD'}


class CCUSOCCDToLCULEthSignalIPdu14:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x40500E
    pdu_length_bytes = 2
    receiver = ['LCUL']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {'CabinRefrigorClimaReqFromSrv': ['CabinRefrigorClimaReqFromSrvTemp', 'CabinRefrigorClimaReqFromSrvMod']}

    class CabinRefrigorClimaReqFromSrvTemp:
        comments = ""
        factor = 0.5
        initial_value = 80
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -40
        sig_ub = None
        signal_description = "Cabin Refrigerator Chamber Temperature Request From Service"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class CabinRefrigorClimaReqFromSrvMod:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Cabin Refrigerator Working Mode Request From Service"
        signal_length = 2
        start_position = 15
        value_definition = {'0x0': ' RefrigorMod_Off', '0x1': ' RefrigorMod_Cooling', '0x2': ' RefrigorMod_Heating'}


class CCUSOCCDToLCULEthSignalIPdu28:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x40501C
    pdu_length_bytes = 4
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {'DoorRearLeALMRGBL': ['DoorRearLeALMRGBLGreen', 'DoorRearLeALMRGBLBlue', 'DoorRearLeALMRGBLRed', 'DoorRearLeALMRGBLLuminance']}

    class DoorRearLeALMRGBLGreen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Green,DoorRearLeALMRGBL"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class DoorRearLeALMRGBLBlue:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Blue,DoorRearLeALMRGBL"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class DoorRearLeALMRGBLRed:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "RED,DoorRearLeALMRGBL"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class DoorRearLeALMRGBLLuminance:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Luminance,DoorRearLeALMRGBL"
        signal_length = 7
        start_position = 31
        value_definition = {}


class CCUSOCCDToLCULEthSignalIPdu30:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x40501E
    pdu_length_bytes = 2
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {'DualSunroofCurtPosnCmd': ['DualSunroofCurtPosnCmdRearPosnPercCmd', 'DualSunroofCurtPosnCmdFrntPosnPercCmd']}

    class DualSunroofCurtPosnCmdRearPosnPercCmd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = " position percentage command of rear sunroof curt"
        signal_length = 5
        start_position = 7
        value_definition = {'0x0': ' PosnPercCmd_NoCmd', '0x1': ' PosnPercCmd_FullCls', '0x2': ' PosnPercCmd_Perc4', '0x3': ' PosnPercCmd_Perc8', '0x4': ' PosnPercCmd_Perc12', '0x5': ' PosnPercCmd_Perc16', '0x6': ' PosnPercCmd_Perc20', '0x7': ' PosnPercCmd_Perc24', '0x8': ' PosnPercCmd_Perc28', '0x9': ' PosnPercCmd_Perc32', '0xA': ' PosnPercCmd_Perc36', '0xB': ' PosnPercCmd_Perc40', '0xC': ' PosnPercCmd_Perc44', '0xD': ' PosnPercCmd_Perc48', '0xE': ' PosnPercCmd_Perc52', '0xF': ' PosnPercCmd_Perc56', '0x10': ' PosnPercCmd_Perc60', '0x11': ' PosnPercCmd_Perc64', '0x12': ' PosnPercCmd_Perc68', '0x13': ' PosnPercCmd_Perc72', '0x14': ' PosnPercCmd_Perc76', '0x15': ' PosnPercCmd_Perc80', '0x16': ' PosnPercCmd_Perc84', '0x17': ' PosnPercCmd_Perc88', '0x18': ' PosnPercCmd_Perc92', '0x19': ' PosnPercCmd_Perc96', '0x1A': ' PosnPercCmd_FullOpen', '0x1B': ' PosnPercCmd_Resd1', '0x1C': ' PosnPercCmd_Resd2', '0x1D': ' PosnPercCmd_Resd3'}

    class DualSunroofCurtPosnCmdFrntPosnPercCmd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = " position percentage command of front sunroof curt"
        signal_length = 5
        start_position = 15
        value_definition = {'0x0': ' PosnPercCmd_NoCmd', '0x1': ' PosnPercCmd_FullCls', '0x2': ' PosnPercCmd_Perc4', '0x3': ' PosnPercCmd_Perc8', '0x4': ' PosnPercCmd_Perc12', '0x5': ' PosnPercCmd_Perc16', '0x6': ' PosnPercCmd_Perc20', '0x7': ' PosnPercCmd_Perc24', '0x8': ' PosnPercCmd_Perc28', '0x9': ' PosnPercCmd_Perc32', '0xA': ' PosnPercCmd_Perc36', '0xB': ' PosnPercCmd_Perc40', '0xC': ' PosnPercCmd_Perc44', '0xD': ' PosnPercCmd_Perc48', '0xE': ' PosnPercCmd_Perc52', '0xF': ' PosnPercCmd_Perc56', '0x10': ' PosnPercCmd_Perc60', '0x11': ' PosnPercCmd_Perc64', '0x12': ' PosnPercCmd_Perc68', '0x13': ' PosnPercCmd_Perc72', '0x14': ' PosnPercCmd_Perc76', '0x15': ' PosnPercCmd_Perc80', '0x16': ' PosnPercCmd_Perc84', '0x17': ' PosnPercCmd_Perc88', '0x18': ' PosnPercCmd_Perc92', '0x19': ' PosnPercCmd_Perc96', '0x1A': ' PosnPercCmd_FullOpen', '0x1B': ' PosnPercCmd_Resd1', '0x1C': ' PosnPercCmd_Resd2', '0x1D': ' PosnPercCmd_Resd3'}


class CCUSOCCDToLCULEthSignalIPdu52:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405034
    pdu_length_bytes = 6
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {'FuncReqOfOuterDoorSwLampRR': ['FuncReqOfOuterDoorSwLampRRLightMode', 'FuncReqOfOuterDoorSwLampRRLightParameterPerc2', 'FuncReqOfOuterDoorSwLampRRLightParameterPerc1', 'FuncReqOfOuterDoorSwLampRROnTime1', 'FuncReqOfOuterDoorSwLampRRLightPriority', 'FuncReqOfOuterDoorSwLampRROnTime2']}

    class FuncReqOfOuterDoorSwLampRRLightMode:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "LightCmd"
        signal_length = 8
        start_position = 7
        value_definition = {'0x0': ' LightMode_OFF', '0x1': ' LightMode_ON', '0x2': ' LightMode_FLASH', '0x3': ' LightMode_BREATH1', '0x4': ' LightMode_BREATH2', '0x5': ' LightMode_Reserved1', '0xFF': ' LightMode_Reserved'}

    class FuncReqOfOuterDoorSwLampRRLightParameterPerc2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "FunctionParameter2"
        signal_length = 7
        start_position = 15
        value_definition = {}

    class FuncReqOfOuterDoorSwLampRRLightParameterPerc1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "FunctionParameter1"
        signal_length = 7
        start_position = 8
        value_definition = {}

    class FuncReqOfOuterDoorSwLampRROnTime1:
        comments = ""
        factor = 1.0
        initial_value = 50
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "OnTimePrm1"
        signal_length = 8
        start_position = 31
        value_definition = {}

    class FuncReqOfOuterDoorSwLampRRLightPriority:
        comments = ""
        factor = 1.0
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "LightPriority"
        signal_length = 8
        start_position = 39
        value_definition = {}

    class FuncReqOfOuterDoorSwLampRROnTime2:
        comments = ""
        factor = 1.0
        initial_value = 50
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "OnTimePrm2"
        signal_length = 8
        start_position = 47
        value_definition = {}


class CCUSOCCDToLCULEthSignalIPdu53:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405035
    pdu_length_bytes = 4
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {'FuncReqOfStopLamp': ['FuncReqOfStopLampChks', 'FuncReqOfStopLampLightPriority', 'FuncReqOfStopLampLightCmd', 'FuncReqOfStopLampLightID1', 'FuncReqOfStopLampCntr']}

    class FuncReqOfStopLampChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "checksum"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class FuncReqOfStopLampLightPriority:
        comments = ""
        factor = 1.0
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "priority"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class FuncReqOfStopLampLightCmd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "lightcmd"
        signal_length = 4
        start_position = 23
        value_definition = {'0x0': ' LightCmd_NoReq', '0x1': ' LightCmd_ON', '0x2': ' LightCmd_OFF', '0x3': ' LightCmd_TBD'}

    class FuncReqOfStopLampLightID1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "lightid"
        signal_length = 4
        start_position = 19
        value_definition = {'0x0': ' LightID1_ALL', '0x1': ' LightID1_Front', '0x2': ' LightID1_Rear', '0x3': ' LightID1_LeftFrontLeftRearLeft', '0x4': ' LightID1_RightFrontRightRearRight', '0x5': ' LightID1_FrontLeft', '0x6': ' LightID1_FrontRight', '0x7': ' LightID1_RearLeft', '0x8': ' LightID1_FrontLeftRearRight', '0x9': ' LightID1_FrontRightRearLeft', '0xA': ' LightID1_ExceptFrontLeft', '0xB': ' LightID1_ExceptFrontRight', '0xC': ' LightID1_ExceptRearLeft', '0xD': ' LightID1_ExceptRearRight', '0xE': ' LightID1_Reserved1', '0xF': ' LightID1_Reserved2'}

    class FuncReqOfStopLampCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "counter"
        signal_length = 4
        start_position = 31
        value_definition = {}


class CCUSOCCDToLCULEthSignalIPdu118:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405076
    pdu_length_bytes = 1
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
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


class CCUSOCCDToLCULEthSignalIPdu59:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x40503B
    pdu_length_bytes = 1
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {}

    class NormRightPedalMoveCtrl:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "right pedal move control"
        signal_length = 3
        start_position = 7
        value_definition = {'0x0': ' ElecPedlCtrlReq_Idle', '0x1': ' ElecPedlCtrlReq_Open', '0x2': ' ElecPedlCtrlReq_Close', '0x3': ' ElecPedlCtrlReq_Resd1', '0x4': ' ElecPedlCtrlReq_Resd2', '0x5': ' ElecPedlCtrlReq_Resd3'}


class CCUSOCCDToLCULEthSignalIPdu16:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405010
    pdu_length_bytes = 1
    receiver = ['LCUL']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {}

    class CabinRefrigorEcoReqFromSrv:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Cabin Refrigerator Eco Request From Service"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}


class CCUSOCCDToLCULEthSignalIPdu32:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405020
    pdu_length_bytes = 1
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {}

    class ExtrReViewMirrFoldManCmdDrvr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "manual folding command of the external rear view mirror at driver side"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' MirrFodCmd_Idle', '0x1': ' MirrFodCmd_Fold', '0x2': ' MirrFodCmd_Unfold'}


class CCUSOCCDToLCULEthSignalIPdu54:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405036
    pdu_length_bytes = 7
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {'FuncReqOfTurnLamp': ['FuncReqOfTurnLampHoldEn', 'FuncReqOfTurnLampLightCmd', 'FuncReqOfTurnLampTLParamterOnTime', 'FuncReqOfTurnLampSteerWhlSnsrEn', 'FuncReqOfTurnLampLightPriority', 'FuncReqOfTurnLampLightID1', 'FuncReqOfTurnLampTLParamterOFFTime', 'FuncReqOfTurnLampTLParamterFlashNTime', 'FuncReqOfTurnLampChks', 'FuncReqOfTurnLampCntr', 'FuncReqOfTurnLampHornSyncFlag']}

    class FuncReqOfTurnLampHoldEn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "keepornotwhenfunctionisfinished"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': ' EnableDisable2_Disabled', '0x1': ' EnableDisable2_Enabled'}

    class FuncReqOfTurnLampLightCmd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "LightCmd"
        signal_length = 4
        start_position = 6
        value_definition = {'0x0': ' LightCmd_NoReq', '0x1': ' LightCmd_ON', '0x2': ' LightCmd_OFF', '0x3': ' LightCmd_TBD'}

    class FuncReqOfTurnLampTLParamterOnTime:
        comments = ""
        factor = 1.0
        initial_value = 40
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "functionparameter1"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class FuncReqOfTurnLampSteerWhlSnsrEn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "SteerWhlturnoffturnlampenable"
        signal_length = 1
        start_position = 2
        value_definition = {'0x0': ' EnableDisable2_Disabled', '0x1': ' EnableDisable2_Enabled'}

    class FuncReqOfTurnLampLightPriority:
        comments = ""
        factor = 1.0
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "LightPriority"
        signal_length = 8
        start_position = 31
        value_definition = {}

    class FuncReqOfTurnLampLightID1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "LightID"
        signal_length = 4
        start_position = 39
        value_definition = {'0x0': ' LightID1_ALL', '0x1': ' LightID1_Front', '0x2': ' LightID1_Rear', '0x3': ' LightID1_LeftFrontLeftRearLeft', '0x4': ' LightID1_RightFrontRightRearRight', '0x5': ' LightID1_FrontLeft', '0x6': ' LightID1_FrontRight', '0x7': ' LightID1_RearLeft', '0x8': ' LightID1_FrontLeftRearRight', '0x9': ' LightID1_FrontRightRearLeft', '0xA': ' LightID1_ExceptFrontLeft', '0xB': ' LightID1_ExceptFrontRight', '0xC': ' LightID1_ExceptRearLeft', '0xD': ' LightID1_ExceptRearRight', '0xE': ' LightID1_Reserved1', '0xF': ' LightID1_Reserved2'}

    class FuncReqOfTurnLampTLParamterOFFTime:
        comments = ""
        factor = 1.0
        initial_value = 40
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "functionparameter2"
        signal_length = 8
        start_position = 47
        value_definition = {}

    class FuncReqOfTurnLampTLParamterFlashNTime:
        comments = ""
        factor = 1.0
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "functionparameter3"
        signal_length = 8
        start_position = 55
        value_definition = {}

    class FuncReqOfTurnLampChks:
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

    class FuncReqOfTurnLampCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "counter"
        signal_length = 4
        start_position = 35
        value_definition = {}

    class FuncReqOfTurnLampHornSyncFlag:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Horn syncroniazation flag"
        signal_length = 1
        start_position = 1
        value_definition = {'0x0': ' EnableDisable2_Disabled', '0x1': ' EnableDisable2_Enabled'}


class CCUSOCCDToLCULEthSignalIPdu49:
    base_type = "Unsigned"
    client_socket = "SocketLcuLTCPServer"
    pdu_header_id = 0x405031
    pdu_length_bytes = 6
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient3"
    signal_group = {'FuncReqOfOuterDoorSwLampFL': ['FuncReqOfOuterDoorSwLampFLLightParameterPerc1', 'FuncReqOfOuterDoorSwLampFLLightPriority', 'FuncReqOfOuterDoorSwLampFLOnTime1', 'FuncReqOfOuterDoorSwLampFLLightParameterPerc2', 'FuncReqOfOuterDoorSwLampFLOnTime2', 'FuncReqOfOuterDoorSwLampFLLightMode']}

    class FuncReqOfOuterDoorSwLampFLLightParameterPerc1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "FunctionParameter1"
        signal_length = 7
        start_position = 7
        value_definition = {}

    class FuncReqOfOuterDoorSwLampFLLightPriority:
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

    class FuncReqOfOuterDoorSwLampFLOnTime1:
        comments = ""
        factor = 1.0
        initial_value = 50
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "OnTimePrm1"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class FuncReqOfOuterDoorSwLampFLLightParameterPerc2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "FunctionParameter2"
        signal_length = 7
        start_position = 31
        value_definition = {}

    class FuncReqOfOuterDoorSwLampFLOnTime2:
        comments = ""
        factor = 1.0
        initial_value = 50
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "OnTimePrm2"
        signal_length = 8
        start_position = 39
        value_definition = {}

    class FuncReqOfOuterDoorSwLampFLLightMode:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "LightCmd"
        signal_length = 8
        start_position = 47
        value_definition = {'0x0': ' LightMode_OFF', '0x1': ' LightMode_ON', '0x2': ' LightMode_FLASH', '0x3': ' LightMode_BREATH1', '0x4': ' LightMode_BREATH2', '0x5': ' LightMode_Reserved1', '0xFF': ' LightMode_Reserved'}
