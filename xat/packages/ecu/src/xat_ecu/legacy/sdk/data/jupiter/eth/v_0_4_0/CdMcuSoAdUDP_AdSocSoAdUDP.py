

class CCUMCUCDToCCUSOCADEthSignalIPdu01:
    base_type = "Unsigned"
    client_socket = "SocketAdSocSoAdUDP"
    pdu_header_id = 0x203001
    pdu_length_bytes = 1
    receiver = ['CCUSOCAD']
    send_type = "Cyclic-10ms"
    sender = "CCUMCUCD"
    server_socket = "SocketCdMcuSoAdUDP"
    signal_group = {}

    class GearAutoShiftModDsbl:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 5
        signal_description = "Proplsion request to Enable/Disable the Auto Gear Shifting mode."
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' EnaDsblDefault_Default', '0x1': ' EnaDsblDefault_Enable', '0x2': ' EnaDsblDefault_Disable', '0x3': ' EnaDsblDefault_Reserved'}
