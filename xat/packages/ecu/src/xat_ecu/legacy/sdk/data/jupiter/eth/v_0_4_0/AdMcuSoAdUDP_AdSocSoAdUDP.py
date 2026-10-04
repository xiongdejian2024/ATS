

class CCUMCUADToCCUSOCADEthSignalIPdu01:
    base_type = "Unsigned"
    client_socket = "SocketAdSocSoAdUDP"
    pdu_header_id = 0x103001
    pdu_length_bytes = 1
    receiver = ['CCUSOCAD']
    send_type = "Cyclic-100ms"
    sender = "CCUMCUAD"
    server_socket = "SocketAdMcuSoAdUDP"
    signal_group = {}

    class ADSOCPwrSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 4
        signal_description = "CCU AD SOC power status"
        signal_length = 4
        start_position = 3
        value_definition = {'0x0': ' SOCPwrModSts_Default', '0x1': ' SOCPwrModSts_OFF', '0x2': ' SOCPwrModSts_STR', '0x3': ' SOCPwrModSts_Start', '0x4': ' SOCPwrModSts_PowerOn', '0x5': ' SOCPwrModSts_ShutDown'}
