

class CCUMCUCDToCCUSOCCDPMEthSignalPdu02:
    base_type = "Unsigned"
    client_socket = "SocketCdSocPMTCPClient"
    pdu_header_id = 0x2040FF
    pdu_length_bytes = 2
    receiver = ['CCUSOCCD']
    send_type = "Cyclic-50ms"
    sender = "CCUMCUCD"
    server_socket = "SocketCdMcuTCPServer"
    signal_group = {}

    class CDSOCPwrSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 15
        signal_description = "CCU CD SOC power status"
        signal_length = 4
        start_position = 7
        value_definition = {'0x0': ' SOCPwrModSts_Default', '0x1': ' SOCPwrModSts_OFF', '0x2': ' SOCPwrModSts_STR', '0x3': ' SOCPwrModSts_Start', '0x4': ' SOCPwrModSts_PowerOn', '0x5': ' SOCPwrModSts_ShutDown'}

    class CDSOCPwrSubSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 14
        signal_description = "CDSOC Power status sub-status"
        signal_length = 4
        start_position = 3
        value_definition = {'0x0': ' SOCPwrSubSts_Default', '0x1': ' SOCPwrSubSts_ColdStart', '0x2': ' SOCPwrSubSts_WarmStart', '0x3': ' SOCPwrSubSts_ShutDownToSTR', '0x4': ' SOCPwrSubSts_ShutDownToOFF', '0x5': ' SOCPwrSubSts_ErrorToOFF', '0x6': ' SOCPwrSubSts_Reset', '0x7': ' SOCPwrSubSts_STRFailedToOFF', '0x8': ' SOCPwrSubSts_StartFailed', '0x9': ' SOCPwrSubSts_StartInhibit', '0xA': ' SOCPwrSubSts_SelfWakeup'}


class CCUMCUCDToCCUSOCCDPMEthSignalPdu01:
    base_type = "Unsigned"
    client_socket = "SocketCdSocPMTCPClient"
    pdu_header_id = 0x2040FE
    pdu_length_bytes = 2
    receiver = ['CCUSOCCD']
    send_type = "Cyclic-100ms"
    sender = "CCUMCUCD"
    server_socket = "SocketCdMcuTCPServer"
    signal_group = {}

    class CDMCUHeartBeatSig:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 12
        signal_description = "Heart beat signal send from CD MCU to CD SOC and NAD"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class CDSOCShutDwnReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 11
        signal_description = "Request CD SOC switch to STR mode"
        signal_length = 3
        start_position = 15
        value_definition = {'0x0': ' SOCShutDownReq_Idle', '0x1': ' SOCShutDownReq_STR', '0x2': ' SOCShutDownReq_OFF', '0x3': ' SOCShutDownReq_Reset', '0x4': ' SOCShutDownReq_ErrorOFF'}


class CCUSOCCDToCCUMCUCDPMEthSignalIPdu01:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x4020FA
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-200ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocPMTCPClient"
    signal_group = {}

    class CDSOCHeartBeatSig:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Heart beat signal send from CD SOC  to CD MCU"
        signal_length = 8
        start_position = 7
        value_definition = {}


class CCUSOCCDToCCUMCUCDPMEthSignalIPdu02:
    base_type = "Boolean"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x4020FB
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-200ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocPMTCPClient"
    signal_group = {}

    class CDSOCKeepPwrReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "CDSOC request MCU to keep its power, not allow to shutdown"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}


class CCUSOCCDToCCUMCUCDPMEthSignalIPdu04:
    base_type = "Boolean"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x4020FD
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-200ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocPMTCPClient"
    signal_group = {}

    class CDSOCRstReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "CD SOC request MCU reboot SOC"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}


class CCUSOCCDToCCUMCUCDPMEthSignalIPdu03:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x4020FC
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocPMTCPClient"
    signal_group = {}

    class CDSOCOperModSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Operation mode of CD SOC"
        signal_length = 3
        start_position = 7
        value_definition = {'0x0': ' CDSOCOperModSts_Lite', '0x1': ' CDSOCOperModSts_Standard', '0x2': ' CDSOCOperModSts_StandardFOTA', '0x3': ' CDSOCOperModSts_StandardStamina'}


class CCUSOCCDToCCUMCUCDPMEthSignalIPdu05:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x4020FE
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-200ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocPMTCPClient"
    signal_group = {}

    class CDSOCShutDwnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "CD SOC feedback shut down status to CD MCU"
        signal_length = 3
        start_position = 7
        value_definition = {'0x0': ' SOCShutDownSts_Idle', '0x1': ' SOCShutDownSts_STRAck', '0x2': ' SOCShutDownSts_STRFailed', '0x3': ' SOCShutDownSts_STRDone', '0x4': ' SOCShutDownSts_OFFAck', '0x5': ' SOCShutDownSts_OFFAllowed', '0x6': ' SOCShutDownSts_ToStart'}


class CCUSOCCDToCCUMCUCDPMEthSignalIPdu06:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x4020FF
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-200ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocPMTCPClient"
    signal_group = {}

    class CDSOCStrtSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "CD SOC feedback start up status to CD MCU"
        signal_length = 3
        start_position = 7
        value_definition = {'0x0': ' SOCStrtSts_Idle', '0x1': ' SOCStrtSts_ColdStartInit', '0x2': ' SOCStrtSts_ColdStartComplete', '0x3': ' SOCStrtSts_WarmStartInit', '0x4': ' SOCStrtSts_WarmStartComplete', '0x5': ' SOCStrtSts_Failed'}
