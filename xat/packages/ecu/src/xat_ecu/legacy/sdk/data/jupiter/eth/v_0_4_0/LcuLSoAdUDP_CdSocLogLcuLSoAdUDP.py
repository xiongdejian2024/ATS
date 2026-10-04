

class LCULToCCUSOCCDEthLogPdu01:
    base_type = "Unsigned"
    client_socket = "SocketCdSocLogLcuLSoAdUDP"
    pdu_header_id = 0x5040F0
    pdu_length_bytes = 1024
    receiver = ['CCUSOCCD']
    send_type = "EventTriggered"
    sender = "LCUL"
    server_socket = "SocketLcuLSoAdUDP"
    signal_group = {}

    class LCULogInfoData1:
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
