

class CCUSOCADToCCUMCUADEthSignalIPdu01:
    base_type = "Unsigned"
    client_socket = "SocketAdMcuTCPServer"
    pdu_header_id = 0x301001
    pdu_length_bytes = 4
    receiver = ['CCUMCUAD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCAD"
    server_socket = "SocketAdSocTCPClient2"
    signal_group = {'GearAutoShiftReq': ['GearAutoShiftReqCntr', 'GearAutoShiftReqGearAutoShiftReq', 'GearAutoShiftReqChks'], 'GearAutoShiftReqSts': ['GearAutoShiftReqStsChks', 'GearAutoShiftReqStsCntr', 'GearAutoShiftReqStsSafe']}

    class GearAutoShiftReqCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Counter"
        signal_length = 4
        start_position = 15
        value_definition = {}

    class GearAutoShiftReqGearAutoShiftReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "The Target gear request for Auto Gear shifting mode."
        signal_length = 3
        start_position = 11
        value_definition = {'0x0': ' GearLvrIndcn_Default', '0x1': ' GearLvrIndcn_P', '0x2': ' GearLvrIndcn_R', '0x3': ' GearLvrIndcn_N', '0x4': ' GearLvrIndcn_D', '0x5': ' GearLvrIndcn_Reserved1', '0x6': ' GearLvrIndcn_Reserved2', '0x7': ' GearLvrIndcn_Undefd'}

    class GearAutoShiftReqChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Checksum"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class GearAutoShiftReqStsChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Checksum"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class GearAutoShiftReqStsCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Counter"
        signal_length = 4
        start_position = 31
        value_definition = {}

    class GearAutoShiftReqStsSafe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Auto shift request status. "
        signal_length = 2
        start_position = 27
        value_definition = {'0x0': ' GearAutoShiftReqSts_NoAction', '0x1': ' GearAutoShiftReqSts_GearReqEnable', '0x2': ' GearAutoShiftReqSts_GearReqComplete', '0x3': ' GearAutoShiftReqSts_GearReqInhibit'}
