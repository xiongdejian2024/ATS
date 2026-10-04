

class CCUMCUCDToLCULEthSignalIPdu01:
    base_type = "Unsigned"
    client_socket = "SocketLcuLSoAdUDP"
    pdu_header_id = 0x205001
    pdu_length_bytes = 8
    receiver = ['LCUL']
    send_type = "Cyclic-50ms"
    sender = "CCUMCUCD"
    server_socket = "SocketCdMcuSoAdUDP"
    signal_group = {'FLPwrSideDoorPosnSet': ['FLPwrSideDoorPosnSetChks', 'FLPwrSideDoorPosnSetPosnCtrlSrc', 'FLPwrSideDoorPosnSetPosnCtrl', 'FLPwrSideDoorPosnSetCntr'], 'RLPwrSideDoorPosnSet': ['RLPwrSideDoorPosnSetPosnCtrlSrc', 'RLPwrSideDoorPosnSetCntr', 'RLPwrSideDoorPosnSetPosnCtrl', 'RLPwrSideDoorPosnSetChks']}

    class FLPwrSideDoorPosnSetChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 17
        signal_description = "checksum"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class FLPwrSideDoorPosnSetPosnCtrlSrc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 17
        signal_description = "Set power side Door position trigger source"
        signal_length = 2
        start_position = 19
        value_definition = {'0x0': ' CtrlTrigsrc_NoCtrlReq', '0x1': ' CtrlTrigsrc_OutdCtrl', '0x2': ' CtrlTrigsrc_InsdCtrl'}

    class FLPwrSideDoorPosnSetPosnCtrl:
        comments = ""
        factor = 1.0
        initial_value = 101
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 17
        signal_description = "Set power side Door position"
        signal_length = 8
        start_position = 11
        value_definition = {}

    class FLPwrSideDoorPosnSetCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 17
        signal_description = "counter"
        signal_length = 4
        start_position = 15
        value_definition = {}

    class RLPwrSideDoorPosnSetPosnCtrlSrc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 41
        signal_description = "Set power side Door position trigger source"
        signal_length = 2
        start_position = 43
        value_definition = {'0x0': ' CtrlTrigsrc_NoCtrlReq', '0x1': ' CtrlTrigsrc_OutdCtrl', '0x2': ' CtrlTrigsrc_InsdCtrl'}

    class RLPwrSideDoorPosnSetCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 41
        signal_description = "counter"
        signal_length = 4
        start_position = 39
        value_definition = {}

    class RLPwrSideDoorPosnSetPosnCtrl:
        comments = ""
        factor = 1.0
        initial_value = 101
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 41
        signal_description = "Set power side Door position"
        signal_length = 8
        start_position = 35
        value_definition = {}

    class RLPwrSideDoorPosnSetChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 41
        signal_description = "checksum"
        signal_length = 8
        start_position = 31
        value_definition = {}


class LCULToCCUMCUCDEthSignalIPdu01:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuSoAdUDP"
    pdu_header_id = 0x502001
    pdu_length_bytes = 24
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "LCUL"
    server_socket = "SocketLcuLSoAdUDP"
    signal_group = {}

    class PrimBattChrgnUReq:
        comments = ""
        factor = 0.025
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 5
        sig_ub = 10
        signal_description = "Primary battery charging voltage value"
        signal_length = 9
        start_position = 7
        value_definition = {}

    class PrimBattFltTSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 9
        signal_description = "Primary battery Over T failure status"
        signal_length = 2
        start_position = 14
        value_definition = {'0x0': ' LVFaultSts_Idle', '0x1': ' LVFaultSts_Fault', '0x2': ' LVFaultSts_NoFault', '0x3': ' LVFaultSts_Reserved'}

    class PrimBattThermSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 8
        signal_description = "Primary battery thermal runaway status"
        signal_length = 2
        start_position = 12
        value_definition = {'0x0': ' LVFaultSts_Idle', '0x1': ' LVFaultSts_Fault', '0x2': ' LVFaultSts_NoFault', '0x3': ' LVFaultSts_Reserved'}

    class RefrigPTSnsr1PRaw:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 135
        signal_description = "Sensor raw data"
        signal_length = 16
        start_position = 23
        value_definition = {}

    class RefrigPTSnsr1TRaw:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 134
        signal_description = "Sensor raw data"
        signal_length = 16
        start_position = 39
        value_definition = {}

    class RefrigPTSnsr2PRaw:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 133
        signal_description = "Sensor raw data"
        signal_length = 16
        start_position = 55
        value_definition = {}

    class RefrigPTSnsr2TRaw:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 132
        signal_description = "Sensor raw data"
        signal_length = 16
        start_position = 71
        value_definition = {}

    class RefrigTSnsr2TRaw:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 131
        signal_description = "Sensor raw data"
        signal_length = 16
        start_position = 87
        value_definition = {}

    class RefrigTSnsr3TRaw:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 130
        signal_description = "Sensor raw data"
        signal_length = 16
        start_position = 103
        value_definition = {}

    class RefrigTSnsr4TRaw:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 129
        signal_description = "Sensor raw data"
        signal_length = 16
        start_position = 119
        value_definition = {}

    class RefrigSov2ActrSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 138
        signal_description = "SOV actuator status"
        signal_length = 2
        start_position = 141
        value_definition = {'0x0': ' Flt_Initial', '0x1': ' Flt_NoFault', '0x2': ' Flt_Fault'}

    class RefrigSov1ActrSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 139
        signal_description = "SOV actuator status"
        signal_length = 2
        start_position = 143
        value_definition = {'0x0': ' Flt_Initial', '0x1': ' Flt_NoFault', '0x2': ' Flt_Fault'}


class LCULToCCUMCUCDEthSignalIPdu03:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuSoAdUDP"
    pdu_header_id = 0x502003
    pdu_length_bytes = 2
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-50ms"
    sender = "LCUL"
    server_socket = "SocketLcuLSoAdUDP"
    signal_group = {}

    class ChargeLidposn:
        comments = ""
        factor = 1.0
        initial_value = 101
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 15
        signal_description = "charge lid position"
        signal_length = 8
        start_position = 7
        value_definition = {}
