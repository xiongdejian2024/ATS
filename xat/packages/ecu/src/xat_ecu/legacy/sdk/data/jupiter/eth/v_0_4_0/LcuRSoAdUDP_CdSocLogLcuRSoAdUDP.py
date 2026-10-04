

class LCURToCCUSOCCDEthLogPdu01:
    base_type = "Unsigned"
    client_socket = "SocketCdSocLogLcuRSoAdUDP"
    pdu_header_id = 0x6040F0
    pdu_length_bytes = 1024
    receiver = ['CCUSOCCD']
    send_type = "EventTriggered"
    sender = "LCUR"
    server_socket = "SocketLcuRSoAdUDP"
    signal_group = {}

    class LCURLogInfoData1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Opaque"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Dynamic array used to transfer MCU log data."
        signal_length = 8192
        start_position = 0
        value_definition = {}
