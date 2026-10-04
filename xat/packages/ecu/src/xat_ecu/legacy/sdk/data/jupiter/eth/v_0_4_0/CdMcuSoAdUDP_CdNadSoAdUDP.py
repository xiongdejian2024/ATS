

class CCUMCUCDToCDNADEthDummyPdu01:
    base_type = "Unsigned"
    client_socket = "SocketCdNadSoAdUDP"
    pdu_header_id = 0x208001
    pdu_length_bytes = 1024
    receiver = ['CCUNAD']
    send_type = "EventTriggered"
    sender = "CCUMCUCD"
    server_socket = "SocketCdMcuSoAdUDP"
    signal_group = {}

    class CDMCU2CDNADDummyData:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Opaque"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Dynamic array for backup use between CDMCU & CDNAD"
        signal_length = 8192
        start_position = 0
        value_definition = {}
