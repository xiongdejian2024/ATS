

class CCUMCUADToCCUMCUCDEthSignalIPdu02:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuSoAdUDP"
    pdu_header_id = 0x102002
    pdu_length_bytes = 2
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-25ms"
    sender = "CCUMCUAD"
    server_socket = "SocketAdMcuSoAdUDP"
    signal_group = {}

    class DoorOpenWarnLeIndcn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 15
        signal_description = "Indicate if a left door open, warning shall be shown to the driver or not."
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' DoorOpenWarnIndcn1_Initialization', '0x1': ' DoorOpenWarnIndcn1_NoWarn', '0x2': ' DoorOpenWarnIndcn1_WarnLvl1', '0x3': ' DoorOpenWarnIndcn1_WarnLvl2'}

    class DoorOpenWarnOn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 14
        signal_description = "Show DOW function status"
        signal_length = 2
        start_position = 5
        value_definition = {'0x0': ' CllsnReSideWarnOn1_Off', '0x1': ' CllsnReSideWarnOn1_Passive', '0x2': ' CllsnReSideWarnOn1_Active', '0x3': ' CllsnReSideWarnOn1_TrlrOff'}

    class DoorOpenWarnRiIndcn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 13
        signal_description = "Indicate if a right door open, warning shall be shown to the driver or not."
        signal_length = 2
        start_position = 3
        value_definition = {'0x0': ' DoorOpenWarnIndcn1_Initialization', '0x1': ' DoorOpenWarnIndcn1_NoWarn', '0x2': ' DoorOpenWarnIndcn1_WarnLvl1', '0x3': ' DoorOpenWarnIndcn1_WarnLvl2'}


class CCUMCUADToCCUMCUCDEthSignalIPdu03:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuSoAdUDP"
    pdu_header_id = 0x102003
    pdu_length_bytes = 16
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-50ms"
    sender = "CCUMCUAD"
    server_socket = "SocketAdMcuSoAdUDP"
    signal_group = {}

    class FrntLeDoorRdrDst:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 9
        signal_description = "Door Radar Distance"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class FrntLeMidPrkgSnsrFlt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 8
        signal_description = "PDC Single Sensor Fault Output"
        signal_length = 2
        start_position = 15
        value_definition = {'0x0': ' PrkgSnsrFlt_NoFault', '0x1': ' PrkgSnsrFlt_Fault', '0x2': ' PrkgSnsrFlt_Cover'}

    class FrntLeOutrPrkgSnsrFlt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 25
        signal_description = "PDC Single Sensor Fault Output"
        signal_length = 2
        start_position = 13
        value_definition = {'0x0': ' PrkgSnsrFlt_NoFault', '0x1': ' PrkgSnsrFlt_Fault', '0x2': ' PrkgSnsrFlt_Cover'}

    class FrntLeSidePrkgSnsrFlt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 24
        signal_description = "PDC Single Sensor Fault Output"
        signal_length = 2
        start_position = 11
        value_definition = {'0x0': ' PrkgSnsrFlt_NoFault', '0x1': ' PrkgSnsrFlt_Fault', '0x2': ' PrkgSnsrFlt_Cover'}

    class FrntRiDoorRdrDst:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 41
        signal_description = "Door Radar Distance"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class FrntRiMidPrkgSnsrFlt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 40
        signal_description = "PDC Single Sensor Fault Output"
        signal_length = 2
        start_position = 31
        value_definition = {'0x0': ' PrkgSnsrFlt_NoFault', '0x1': ' PrkgSnsrFlt_Fault', '0x2': ' PrkgSnsrFlt_Cover'}

    class FrntRiOutrPrkgSnsrFlt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 57
        signal_description = "PDC Single Sensor Fault Output"
        signal_length = 2
        start_position = 29
        value_definition = {'0x0': ' PrkgSnsrFlt_NoFault', '0x1': ' PrkgSnsrFlt_Fault', '0x2': ' PrkgSnsrFlt_Cover'}

    class FrntRiSidePrkgSnsrFlt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 56
        signal_description = "PDC Single Sensor Fault Output"
        signal_length = 2
        start_position = 27
        value_definition = {'0x0': ' PrkgSnsrFlt_NoFault', '0x1': ' PrkgSnsrFlt_Fault', '0x2': ' PrkgSnsrFlt_Cover'}

    class ReLeDoorRdrDst:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 71
        signal_description = "Door Radar Distance"
        signal_length = 8
        start_position = 39
        value_definition = {}

    class ReLeMidPrkgSnsrFlt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 70
        signal_description = "PDC Single Sensor Fault Output"
        signal_length = 2
        start_position = 47
        value_definition = {'0x0': ' PrkgSnsrFlt_NoFault', '0x1': ' PrkgSnsrFlt_Fault', '0x2': ' PrkgSnsrFlt_Cover'}

    class ReLeOutrPrkgSnsrFlt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 69
        signal_description = "PDC Single Sensor Fault Output"
        signal_length = 2
        start_position = 45
        value_definition = {'0x0': ' PrkgSnsrFlt_NoFault', '0x1': ' PrkgSnsrFlt_Fault', '0x2': ' PrkgSnsrFlt_Cover'}

    class ReLeSidePrkgSnsrFlt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 68
        signal_description = "PDC Single Sensor Fault Output"
        signal_length = 2
        start_position = 43
        value_definition = {'0x0': ' PrkgSnsrFlt_NoFault', '0x1': ' PrkgSnsrFlt_Fault', '0x2': ' PrkgSnsrFlt_Cover'}

    class ReRiDoorRdrDst:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 67
        signal_description = "Door Radar Distance"
        signal_length = 8
        start_position = 55
        value_definition = {}

    class ReRiMidPrkgSnsrFlt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 66
        signal_description = "PDC Single Sensor Fault Output"
        signal_length = 2
        start_position = 63
        value_definition = {'0x0': ' PrkgSnsrFlt_NoFault', '0x1': ' PrkgSnsrFlt_Fault', '0x2': ' PrkgSnsrFlt_Cover'}

    class ReRiOutrPrkgSnsrFlt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 65
        signal_description = "PDC Single Sensor Fault Output"
        signal_length = 2
        start_position = 61
        value_definition = {'0x0': ' PrkgSnsrFlt_NoFault', '0x1': ' PrkgSnsrFlt_Fault', '0x2': ' PrkgSnsrFlt_Cover'}

    class ReRiSidePrkgSnsrFlt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 64
        signal_description = "PDC Single Sensor Fault Output"
        signal_length = 2
        start_position = 59
        value_definition = {'0x0': ' PrkgSnsrFlt_NoFault', '0x1': ' PrkgSnsrFlt_Fault', '0x2': ' PrkgSnsrFlt_Cover'}


class CCUMCUADToCCUMCUCDEthSignalIPdu01:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuSoAdUDP"
    pdu_header_id = 0x102001
    pdu_length_bytes = 16
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUMCUAD"
    server_socket = "SocketAdMcuSoAdUDP"
    signal_group = {}

    class FrntLeMidPrkgSnsrDst:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 111
        signal_description = "PDC Distance Output"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class FrntLeOutrPrkgSnsrDst:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 110
        signal_description = "PDC Distance Output"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class FrntLeSidePrkgSnsrDst:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 109
        signal_description = "PDC Distance Output"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class FrntRiMidPrkgSnsrDst:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 108
        signal_description = "PDC Distance Output"
        signal_length = 8
        start_position = 31
        value_definition = {}

    class FrntRiOutrPrkgSnsrDst:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 107
        signal_description = "PDC Distance Output"
        signal_length = 8
        start_position = 39
        value_definition = {}

    class FrntRiSidePrkgSnsrDst:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 106
        signal_description = "PDC Distance Output"
        signal_length = 8
        start_position = 47
        value_definition = {}

    class PrkgDstCtrlSnsrSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 105
        signal_description = "PDC Sensor Staus"
        signal_length = 3
        start_position = 55
        value_definition = {'0x0': ' PrkgDstCtrlSnsrSts_NoFault', '0x1': ' PrkgDstCtrlSnsrSts_Front_USS_Fault', '0x2': ' PrkgDstCtrlSnsrSts_Rear_USS_Fault', '0x3': ' PrkgDstCtrlSnsrSts_Front_and_Rear_USS_Fault', '0x4': ' PrkgDstCtrlSnsrSts_Reserve1', '0x5': ' PrkgDstCtrlSnsrSts_Reserve2', '0x6': ' PrkgDstCtrlSnsrSts_Reserve3', '0x7': ' PrkgDstCtrlSnsrSts_Reserve4'}

    class PrkgDstCtrlSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 104
        signal_description = "Parking Distance Control Status"
        signal_length = 4
        start_position = 52
        value_definition = {'0x0': ' PrkgDstCtrlSts_OFF', '0x1': ' PrkgDstCtrlSts_Initialize', '0x2': ' PrkgDstCtrlSts_Standby', '0x3': ' PrkgDstCtrlSts_FrontRearActive', '0x4': ' PrkgDstCtrlSts_FrontActive', '0x5': ' PrkgDstCtrlSts_RearActive', '0x6': ' PrkgDstCtrlSts_SystemFailure', '0x7': ' PrkgDstCtrlSts_Inhibited', '0x8': ' PrkgDstCtrlSts_Covered', '0x9': ' PrkgDstCtrlSts_Reserved1', '0xA': ' PrkgDstCtrlSts_Reserved2', '0xB': ' PrkgDstCtrlSts_Reserved3', '0xC': ' PrkgDstCtrlSts_Reserved4', '0xD': ' PrkgDstCtrlSts_Reserved5', '0xE': ' PrkgDstCtrlSts_Reserved6', '0xF': ' PrkgDstCtrlSts_Reserved7'}

    class PrkgDstCtrlWarn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 119
        signal_description = "PDC Warning"
        signal_length = 1
        start_position = 48
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class ReLeMidPrkgSnsrDst:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 118
        signal_description = "PDC Distance Output"
        signal_length = 8
        start_position = 63
        value_definition = {}

    class ReLeOutrPrkgSnsrDst:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 117
        signal_description = "PDC Distance Output"
        signal_length = 8
        start_position = 71
        value_definition = {}

    class ReLeSidePrkgSnsrDst:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 116
        signal_description = "PDC Distance Output"
        signal_length = 8
        start_position = 79
        value_definition = {}

    class ReRiMidPrkgSnsrDst:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 115
        signal_description = "PDC Distance Output"
        signal_length = 8
        start_position = 87
        value_definition = {}

    class ReRiOutrPrkgSnsrDst:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 114
        signal_description = "PDC Distance Output"
        signal_length = 8
        start_position = 95
        value_definition = {}

    class ReRiSidePrkgSnsrDst:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 113
        signal_description = "PDC Distance Output"
        signal_length = 8
        start_position = 103
        value_definition = {}
