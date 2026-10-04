

class CCUMCUADToCCUSOCCDEthSignalIPdu09:
    base_type = "Unsigned"
    client_socket = "SocketCdSocSoAdUDP"
    pdu_header_id = 0x104009
    pdu_length_bytes = 1
    receiver = ['CCUSOCCD']
    send_type = "Cyclic-400ms"
    sender = "CCUMCUAD"
    server_socket = "SocketAdMcuSoAdUDP"
    signal_group = {}

    class SteerAssiLvlCfmd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 4
        signal_description = "Steering Assist Level Confirmation"
        signal_length = 3
        start_position = 7
        value_definition = {'0x0': ' SteerAssiLvl_UnknownLevel', '0x1': ' SteerAssiLvl_Level1', '0x2': ' SteerAssiLvl_Level2', '0x3': ' SteerAssiLvl_Level3', '0x4': ' SteerAssiLvl_Level4', '0x5': ' SteerAssiLvl_Reserved1', '0x6': ' SteerAssiLvl_Reserved2', '0x7': ' SteerAssiLvl_Reserved3'}


class CCUMCUADToCCUSOCCDEthSignalIPdu08:
    base_type = "Unsigned"
    client_socket = "SocketCdSocSoAdUDP"
    pdu_header_id = 0x104008
    pdu_length_bytes = 1
    receiver = ['CCUSOCCD']
    send_type = "Cyclic-130ms"
    sender = "CCUMCUAD"
    server_socket = "SocketAdMcuSoAdUDP"
    signal_group = {}

    class DamprActMod:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1
        signal_description = "Actual damper mode"
        signal_length = 3
        start_position = 7
        value_definition = {'0x0': ' DamprLvl_level1', '0x1': ' DamprLvl_level2', '0x2': ' DamprLvl_level3', '0x3': ' DamprLvl_Reserved1', '0x4': ' DamprLvl_Reserved2', '0x5': ' DamprLvl_Reserved3', '0x6': ' DamprLvl_Reserved4', '0x7': ' DamprLvl_Reserved5'}

    class RoadIndex:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 0
        signal_description = "Road level index"
        signal_length = 3
        start_position = 4
        value_definition = {'0x0': ' RoadIndex_Level1', '0x1': ' RoadIndex_Level2', '0x2': ' RoadIndex_Level3', '0x3': ' RoadIndex_Level4', '0x4': ' RoadIndex_Level5', '0x5': ' RoadIndex_Level6', '0x6': ' RoadIndex_Reserved1', '0x7': ' RoadIndex_Reserved2'}


class CCUMCUADToCCUSOCCDEthSignalIPdu07:
    base_type = "Unsigned"
    client_socket = "SocketCdSocSoAdUDP"
    pdu_header_id = 0x104007
    pdu_length_bytes = 2
    receiver = ['CCUSOCCD']
    send_type = "Cyclic-50ms"
    sender = "CCUMCUAD"
    server_socket = "SocketAdMcuSoAdUDP"
    signal_group = {'SteerWhlCntrCtrl': ['SteerWhlCntrCtrlSts', 'SteerWhlCntrCtrlAvlSts']}

    class ChrgnUReq:
        comments = ""
        factor = 0.025
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 5
        sig_ub = 14
        signal_description = "Charging voltage value"
        signal_length = 9
        start_position = 7
        value_definition = {}

    class SteerWhlCntrCtrlSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 13
        signal_description = "Status of Steering Wheel Centering Control"
        signal_length = 2
        start_position = 9
        value_definition = {'0x0': ' ActvInActv2_Init', '0x1': ' ActvInActv2_InActv', '0x2': ' ActvInActv2_Actv'}

    class SteerWhlCntrCtrlAvlSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 13
        signal_description = "Available Status of Steering Wheel Centering Control"
        signal_length = 1
        start_position = 10
        value_definition = {'0x0': ' AvlSts2_NotAvl', '0x1': ' AvlSts2_Avl'}


class CCUMCUADToCCUSOCCDEthSignalIPdu06:
    base_type = "Unsigned"
    client_socket = "SocketCdSocSoAdUDP"
    pdu_header_id = 0x104006
    pdu_length_bytes = 30
    receiver = ['CCUSOCCD']
    send_type = "Cyclic-40ms"
    sender = "CCUMCUAD"
    server_socket = "SocketAdMcuSoAdUDP"
    signal_group = {'AbsSysWarnReq': ['AbsSysWarnReqAbs', 'AbsSysWarnReqEbd', 'AbsSysWarnReqChks', 'AbsSysWarnReqCntr'], 'AbsWhlActv': ['AbsWhlActvFL', 'AbsWhlActvRL', 'AbsWhlActvRR', 'AbsWhlActvFR'], 'BdwSts': ['BdwStsActv', 'BdwStsEna', 'BdwStsChks', 'BdwStsCntr', 'BdwStsSts2'], 'EblSts': ['EblStsActv', 'EblStsEna', 'EblStsCntr', 'EblStsChks', 'EblStsSts2'], 'EscSysWarnReq': ['EscSysWarnReqEscSysWarn', 'EscSysWarnReqChks', 'EscSysWarnReqCntr'], 'HbaSts': ['HbaStsCntr', 'HbaStsEna', 'HbaStsChks', 'HbaStsActv', 'HbaStsSts2'], 'HbbSts': ['HbbStsChks', 'HbbStsCntr', 'HbbStsEna', 'HbbStsActv', 'HbbStsSts2'], 'HbcSts': ['HbcStsCntr', 'HbcStsActv', 'HbcStsChks', 'HbcStsEna', 'HbcStsSts2'], 'HfcSts': ['HfcStsEna', 'HfcStsChks', 'HfcStsActv', 'HfcStsCntr', 'HfcStsSts2'], 'HhcSts': ['HhcStsActv', 'HhcStsCntr', 'HhcStsEna', 'HhcStsChks', 'HhcStsSts2'], 'HrbSts': ['HrbStsActv', 'HrbStsCntr', 'HrbStsChks', 'HrbStsEna', 'HrbStsSts2'], 'ScmSts': ['ScmStsCntr', 'ScmStsChks', 'ScmStsEna', 'ScmStsActv', 'ScmStsSts2']}

    class AbsSysWarnReqAbs:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 23
        signal_description = "Abs warning indication request"
        signal_length = 2
        start_position = 13
        value_definition = {'0x0': ' BrkLamp_Off', '0x1': ' BrkLamp_On', '0x2': ' BrkLamp_Flash', '0x3': ' BrkLamp_Reserved'}

    class AbsSysWarnReqEbd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 23
        signal_description = "EBD warning indication request"
        signal_length = 2
        start_position = 15
        value_definition = {'0x0': ' BrkLamp_Off', '0x1': ' BrkLamp_On', '0x2': ' BrkLamp_Flash', '0x3': ' BrkLamp_Reserved'}

    class AbsSysWarnReqChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 23
        signal_description = "CRC"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class AbsSysWarnReqCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 23
        signal_description = "counter"
        signal_length = 4
        start_position = 11
        value_definition = {}

    class AbsWhlActvFL:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 22
        signal_description = "Anti Blocking Systems (ABS) control is active or not (for fl)"
        signal_length = 1
        start_position = 19
        value_definition = {'0x0': ' YesNo2_No', '0x1': ' YesNo2_Yes'}

    class AbsWhlActvRL:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 22
        signal_description = "Anti Blocking Systems (ABS) control is active or not (for Rl)"
        signal_length = 1
        start_position = 18
        value_definition = {'0x0': ' YesNo2_No', '0x1': ' YesNo2_Yes'}

    class AbsWhlActvRR:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 22
        signal_description = "Anti Blocking Systems (ABS) control is active or not (for rr)"
        signal_length = 1
        start_position = 17
        value_definition = {'0x0': ' YesNo2_No', '0x1': ' YesNo2_Yes'}

    class AbsWhlActvFR:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 22
        signal_description = "Anti Blocking Systems (ABS) control is active or not (for fr)"
        signal_length = 1
        start_position = 16
        value_definition = {'0x0': ' YesNo2_No', '0x1': ' YesNo2_Yes'}

    class BdwStsActv:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 21
        signal_description = "Bdw function active information"
        signal_length = 2
        start_position = 47
        value_definition = {'0x0': ' Actv_NoActv', '0x1': ' Actv_Actv', '0x2': ' Actv_Reserved1', '0x3': ' Actv_Reserved2'}

    class BdwStsEna:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 21
        signal_description = "Bdw function enable information"
        signal_length = 1
        start_position = 36
        value_definition = {'0x0': ' EnableDisable2_Disabled', '0x1': ' EnableDisable2_Enabled'}

    class BdwStsChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 21
        signal_description = "crc"
        signal_length = 8
        start_position = 31
        value_definition = {}

    class BdwStsCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 21
        signal_description = "counter"
        signal_length = 4
        start_position = 35
        value_definition = {}

    class BdwStsSts2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 21
        signal_description = "function status"
        signal_length = 3
        start_position = 39
        value_definition = {'0x0': ' Sts2_Initial', '0x1': ' Sts2_Normal', '0x2': ' Sts2_Fault', '0x3': ' Sts2_Off'}

    class EblStsActv:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 20
        signal_description = "Ebl function active information"
        signal_length = 2
        start_position = 41
        value_definition = {'0x0': ' Actv_NoActv', '0x1': ' Actv_Actv', '0x2': ' Actv_Reserved1', '0x3': ' Actv_Reserved2'}

    class EblStsEna:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 20
        signal_description = "Ebl function enable information"
        signal_length = 1
        start_position = 60
        value_definition = {'0x0': ' EnableDisable2_Disabled', '0x1': ' EnableDisable2_Enabled'}

    class EblStsCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 20
        signal_description = "counter"
        signal_length = 4
        start_position = 59
        value_definition = {}

    class EblStsChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 20
        signal_description = "crc"
        signal_length = 8
        start_position = 55
        value_definition = {}

    class EblStsSts2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 20
        signal_description = "function status"
        signal_length = 3
        start_position = 63
        value_definition = {'0x0': ' Sts2_Initial', '0x1': ' Sts2_Normal', '0x2': ' Sts2_Fault', '0x3': ' Sts2_Off'}

    class EscSysWarnReqEscSysWarn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 73
        signal_description = "Esc warning indication request or indication to driver that the Esc function is in active intervention"
        signal_length = 2
        start_position = 75
        value_definition = {'0x0': ' BrkLamp_Off', '0x1': ' BrkLamp_On', '0x2': ' BrkLamp_Flash', '0x3': ' BrkLamp_Reserved'}

    class EscSysWarnReqChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 73
        signal_description = "crc"
        signal_length = 8
        start_position = 71
        value_definition = {}

    class EscSysWarnReqCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 73
        signal_description = "counter"
        signal_length = 4
        start_position = 79
        value_definition = {}

    class EucActv:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 43
        signal_description = "Euc function active information"
        signal_length = 2
        start_position = 45
        value_definition = {'0x0': ' ActvInActv2_Init', '0x1': ' ActvInActv2_InActv', '0x2': ' ActvInActv2_Actv'}

    class HbaStsCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 42
        signal_description = "counter"
        signal_length = 4
        start_position = 91
        value_definition = {}

    class HbaStsEna:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 42
        signal_description = "Hba function enable information"
        signal_length = 1
        start_position = 92
        value_definition = {'0x0': ' EnableDisable2_Disabled', '0x1': ' EnableDisable2_Enabled'}

    class HbaStsChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 42
        signal_description = "crc"
        signal_length = 8
        start_position = 87
        value_definition = {}

    class HbaStsActv:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 42
        signal_description = "Hba function active information"
        signal_length = 2
        start_position = 103
        value_definition = {'0x0': ' Actv_NoActv', '0x1': ' Actv_Actv', '0x2': ' Actv_Reserved1', '0x3': ' Actv_Reserved2'}

    class HbaStsSts2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 42
        signal_description = "function status"
        signal_length = 3
        start_position = 95
        value_definition = {'0x0': ' Sts2_Initial', '0x1': ' Sts2_Normal', '0x2': ' Sts2_Fault', '0x3': ' Sts2_Off'}

    class HbbStsChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 72
        signal_description = "crc"
        signal_length = 8
        start_position = 111
        value_definition = {}

    class HbbStsCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 72
        signal_description = "counter"
        signal_length = 4
        start_position = 115
        value_definition = {}

    class HbbStsEna:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 72
        signal_description = "Hbb function enable information"
        signal_length = 1
        start_position = 116
        value_definition = {'0x0': ' EnableDisable2_Disabled', '0x1': ' EnableDisable2_Enabled'}

    class HbbStsActv:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 72
        signal_description = "Hbb function acive information"
        signal_length = 2
        start_position = 97
        value_definition = {'0x0': ' Actv_NoActv', '0x1': ' Actv_Actv', '0x2': ' Actv_Reserved1', '0x3': ' Actv_Reserved2'}

    class HbbStsSts2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 72
        signal_description = "function status"
        signal_length = 3
        start_position = 119
        value_definition = {'0x0': ' Sts2_Initial', '0x1': ' Sts2_Normal', '0x2': ' Sts2_Fault', '0x3': ' Sts2_Off'}

    class HbcStsCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 101
        signal_description = "counter"
        signal_length = 4
        start_position = 131
        value_definition = {}

    class HbcStsActv:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 101
        signal_description = "Hbc function active information"
        signal_length = 2
        start_position = 143
        value_definition = {'0x0': ' Actv_NoActv', '0x1': ' Actv_Actv', '0x2': ' Actv_Reserved1', '0x3': ' Actv_Reserved2'}

    class HbcStsChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 101
        signal_description = "crc"
        signal_length = 8
        start_position = 127
        value_definition = {}

    class HbcStsEna:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 101
        signal_description = "Hbc function enable information"
        signal_length = 1
        start_position = 132
        value_definition = {'0x0': ' EnableDisable2_Disabled', '0x1': ' EnableDisable2_Enabled'}

    class HbcStsSts2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 101
        signal_description = "function status"
        signal_length = 3
        start_position = 135
        value_definition = {'0x0': ' Sts2_Initial', '0x1': ' Sts2_Normal', '0x2': ' Sts2_Fault', '0x3': ' Sts2_Off'}

    class HfcStsEna:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 100
        signal_description = "Hfc function enable information"
        signal_length = 1
        start_position = 156
        value_definition = {'0x0': ' EnableDisable2_Disabled', '0x1': ' EnableDisable2_Enabled'}

    class HfcStsChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 100
        signal_description = "crc"
        signal_length = 8
        start_position = 151
        value_definition = {}

    class HfcStsActv:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 100
        signal_description = "Hfc function active information"
        signal_length = 2
        start_position = 137
        value_definition = {'0x0': ' Actv_NoActv', '0x1': ' Actv_Actv', '0x2': ' Actv_Reserved1', '0x3': ' Actv_Reserved2'}

    class HfcStsCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 100
        signal_description = "counter"
        signal_length = 4
        start_position = 155
        value_definition = {}

    class HfcStsSts2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 100
        signal_description = "function status"
        signal_length = 3
        start_position = 159
        value_definition = {'0x0': ' Sts2_Initial', '0x1': ' Sts2_Normal', '0x2': ' Sts2_Fault', '0x3': ' Sts2_Off'}

    class HhcStsActv:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 99
        signal_description = "Hhc function active information"
        signal_length = 2
        start_position = 183
        value_definition = {'0x0': ' Actv_NoActv', '0x1': ' Actv_Actv', '0x2': ' Actv_Reserved1', '0x3': ' Actv_Reserved2'}

    class HhcStsCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 99
        signal_description = "counter"
        signal_length = 4
        start_position = 171
        value_definition = {}

    class HhcStsEna:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 99
        signal_description = "Hhc function enable information"
        signal_length = 1
        start_position = 172
        value_definition = {'0x0': ' EnableDisable2_Disabled', '0x1': ' EnableDisable2_Enabled'}

    class HhcStsChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 99
        signal_description = "crc"
        signal_length = 8
        start_position = 167
        value_definition = {}

    class HhcStsSts2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 99
        signal_description = "function status"
        signal_length = 3
        start_position = 175
        value_definition = {'0x0': ' Sts2_Initial', '0x1': ' Sts2_Normal', '0x2': ' Sts2_Fault', '0x3': ' Sts2_Off'}

    class HrbStsActv:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 98
        signal_description = "Hrb function active information"
        signal_length = 2
        start_position = 177
        value_definition = {'0x0': ' Actv_NoActv', '0x1': ' Actv_Actv', '0x2': ' Actv_Reserved1', '0x3': ' Actv_Reserved2'}

    class HrbStsCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 98
        signal_description = "counter"
        signal_length = 4
        start_position = 195
        value_definition = {}

    class HrbStsChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 98
        signal_description = "crc"
        signal_length = 8
        start_position = 191
        value_definition = {}

    class HrbStsEna:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 98
        signal_description = "Hrb function enable information"
        signal_length = 1
        start_position = 196
        value_definition = {'0x0': ' EnableDisable2_Disabled', '0x1': ' EnableDisable2_Enabled'}

    class HrbStsSts2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 98
        signal_description = "function status"
        signal_length = 3
        start_position = 199
        value_definition = {'0x0': ' Sts2_Initial', '0x1': ' Sts2_Normal', '0x2': ' Sts2_Fault', '0x3': ' Sts2_Off'}

    class LgtStbIntvIndcn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 139
        signal_description = "longitudinal stability control status"
        signal_length = 2
        start_position = 141
        value_definition = {'0x0': ' ActvInActv2_Init', '0x1': ' ActvInActv2_InActv', '0x2': ' ActvInActv2_Actv'}

    class PTCActvFrnt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 221
        signal_description = "PTC function front axle active information"
        signal_length = 2
        start_position = 219
        value_definition = {'0x0': ' Actv_NoActv', '0x1': ' Actv_Actv', '0x2': ' Actv_Reserved1', '0x3': ' Actv_Reserved2'}

    class PTCActvRe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 220
        signal_description = "PTC function rear axle active information"
        signal_length = 2
        start_position = 217
        value_definition = {'0x0': ' Actv_NoActv', '0x1': ' Actv_Actv', '0x2': ' Actv_Reserved1', '0x3': ' Actv_Reserved2'}

    class ScmStsCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 138
        signal_description = "counter"
        signal_length = 4
        start_position = 211
        value_definition = {}

    class ScmStsChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 138
        signal_description = "crc"
        signal_length = 8
        start_position = 207
        value_definition = {}

    class ScmStsEna:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 138
        signal_description = "Scm function enable information"
        signal_length = 1
        start_position = 212
        value_definition = {'0x0': ' EnableDisable2_Disabled', '0x1': ' EnableDisable2_Enabled'}

    class ScmStsActv:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 138
        signal_description = "Scm function active information"
        signal_length = 2
        start_position = 223
        value_definition = {'0x0': ' Actv_NoActv', '0x1': ' Actv_Actv', '0x2': ' Actv_Reserved1', '0x3': ' Actv_Reserved2'}

    class ScmStsSts2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 138
        signal_description = "function status"
        signal_length = 3
        start_position = 215
        value_definition = {'0x0': ' Sts2_Initial', '0x1': ' Sts2_Normal', '0x2': ' Sts2_Fault', '0x3': ' Sts2_Off'}


class CCUMCUADToCCUSOCCDEthSignalIPdu02:
    base_type = "Unsigned"
    client_socket = "SocketCdSocSoAdUDP"
    pdu_header_id = 0x104002
    pdu_length_bytes = 8
    receiver = ['CCUSOCCD']
    send_type = "Cyclic-10ms"
    sender = "CCUMCUAD"
    server_socket = "SocketAdMcuSoAdUDP"
    signal_group = {}

    class BeltCrashStsAtDrvr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 28
        signal_description = "Belt crash status at driver"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' BeltCrashSts_Invalid', '0x1': ' BeltCrashSts_NotActvn', '0x2': ' BeltCrashSts_Actvn'}

    class BeltCrashStsAtPass:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 27
        signal_description = "Belt crash status at passenger"
        signal_length = 2
        start_position = 5
        value_definition = {'0x0': ' BeltCrashSts_Invalid', '0x1': ' BeltCrashSts_NotActvn', '0x2': ' BeltCrashSts_Actvn'}

    class FrntLeLvl:
        comments = ""
        factor = 1.0
        initial_value = 14
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 26
        signal_description = "Front left level"
        signal_length = 4
        start_position = 3
        value_definition = {'0x0': ' HeightLevel_LowLevel5', '0x1': ' HeightLevel_LowLevel4', '0x2': ' HeightLevel_LowLevel3', '0x3': ' HeightLevel_LowLevel2', '0x4': ' HeightLevel_LowLevel1', '0x5': ' HeightLevel_NormaLevel', '0x6': ' HeightLevel_HighLevel1', '0x7': ' HeightLevel_HighLevel2', '0x8': ' HeightLevel_HighLevel3', '0x9': ' HeightLevel_HighLevel4', '0xA': ' HeightLevel_HighLevel5', '0xB': ' HeightLevel_Reserved1', '0xC': ' HeightLevel_Reserved2', '0xD': ' HeightLevel_Reserved3', '0xE': ' HeightLevel_InitUnknow', '0xF': ' HeightLevel_Invalid'}

    class FrntLeStfnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 25
        signal_description = "Stiffness status for FL"
        signal_length = 1
        start_position = 15
        value_definition = {'0x0': ' OnOff2_On', '0x1': ' OnOff2_Off'}

    class FrntRiLvl:
        comments = ""
        factor = 1.0
        initial_value = 14
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 24
        signal_description = "Front right level"
        signal_length = 4
        start_position = 14
        value_definition = {'0x0': ' HeightLevel_LowLevel5', '0x1': ' HeightLevel_LowLevel4', '0x2': ' HeightLevel_LowLevel3', '0x3': ' HeightLevel_LowLevel2', '0x4': ' HeightLevel_LowLevel1', '0x5': ' HeightLevel_NormaLevel', '0x6': ' HeightLevel_HighLevel1', '0x7': ' HeightLevel_HighLevel2', '0x8': ' HeightLevel_HighLevel3', '0x9': ' HeightLevel_HighLevel4', '0xA': ' HeightLevel_HighLevel5', '0xB': ' HeightLevel_Reserved1', '0xC': ' HeightLevel_Reserved2', '0xD': ' HeightLevel_Reserved3', '0xE': ' HeightLevel_InitUnknow', '0xF': ' HeightLevel_Invalid'}

    class FrntRiStfnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 39
        signal_description = "Stiffness status for FR"
        signal_length = 1
        start_position = 10
        value_definition = {'0x0': ' OnOff2_On', '0x1': ' OnOff2_Off'}

    class ReLeLvl:
        comments = ""
        factor = 1.0
        initial_value = 14
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 38
        signal_description = "Rear left level"
        signal_length = 4
        start_position = 9
        value_definition = {'0x0': ' HeightLevel_LowLevel5', '0x1': ' HeightLevel_LowLevel4', '0x2': ' HeightLevel_LowLevel3', '0x3': ' HeightLevel_LowLevel2', '0x4': ' HeightLevel_LowLevel1', '0x5': ' HeightLevel_NormaLevel', '0x6': ' HeightLevel_HighLevel1', '0x7': ' HeightLevel_HighLevel2', '0x8': ' HeightLevel_HighLevel3', '0x9': ' HeightLevel_HighLevel4', '0xA': ' HeightLevel_HighLevel5', '0xB': ' HeightLevel_Reserved1', '0xC': ' HeightLevel_Reserved2', '0xD': ' HeightLevel_Reserved3', '0xE': ' HeightLevel_InitUnknow', '0xF': ' HeightLevel_Invalid'}

    class ReRiLvl:
        comments = ""
        factor = 1.0
        initial_value = 14
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 37
        signal_description = "Rear right level"
        signal_length = 4
        start_position = 21
        value_definition = {'0x0': ' HeightLevel_LowLevel5', '0x1': ' HeightLevel_LowLevel4', '0x2': ' HeightLevel_LowLevel3', '0x3': ' HeightLevel_LowLevel2', '0x4': ' HeightLevel_LowLevel1', '0x5': ' HeightLevel_NormaLevel', '0x6': ' HeightLevel_HighLevel1', '0x7': ' HeightLevel_HighLevel2', '0x8': ' HeightLevel_HighLevel3', '0x9': ' HeightLevel_HighLevel4', '0xA': ' HeightLevel_HighLevel5', '0xB': ' HeightLevel_Reserved1', '0xC': ' HeightLevel_Reserved2', '0xD': ' HeightLevel_Reserved3', '0xE': ' HeightLevel_InitUnknow', '0xF': ' HeightLevel_Invalid'}

    class SteerAssistAvlSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 36
        signal_description = "Status of power assist"
        signal_length = 1
        start_position = 17
        value_definition = {'0x0': ' AvlSts1_Avl', '0x1': ' AvlSts1_NotAvl'}

    class TarLvl:
        comments = ""
        factor = 1.0
        initial_value = 14
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 35
        signal_description = "Target level"
        signal_length = 4
        start_position = 16
        value_definition = {'0x0': ' HeightLevel_LowLevel5', '0x1': ' HeightLevel_LowLevel4', '0x2': ' HeightLevel_LowLevel3', '0x3': ' HeightLevel_LowLevel2', '0x4': ' HeightLevel_LowLevel1', '0x5': ' HeightLevel_NormaLevel', '0x6': ' HeightLevel_HighLevel1', '0x7': ' HeightLevel_HighLevel2', '0x8': ' HeightLevel_HighLevel3', '0x9': ' HeightLevel_HighLevel4', '0xA': ' HeightLevel_HighLevel5', '0xB': ' HeightLevel_Reserved1', '0xC': ' HeightLevel_Reserved2', '0xD': ' HeightLevel_Reserved3', '0xE': ' HeightLevel_InitUnknow', '0xF': ' HeightLevel_Invalid'}


class CCUMCUADToCCUSOCCDEthSignalIPdu03:
    base_type = "Unsigned"
    client_socket = "SocketCdSocSoAdUDP"
    pdu_header_id = 0x104003
    pdu_length_bytes = 8
    receiver = ['CCUSOCCD']
    send_type = "Cyclic-20ms"
    sender = "CCUMCUAD"
    server_socket = "SocketAdMcuSoAdUDP"
    signal_group = {'BrkPedStkPerc': ['BrkPedStkPercCntr', 'BrkPedStkPercPerc', 'BrkPedStkPercChks']}

    class BrkPedStkPercCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 20
        signal_description = "counter"
        signal_length = 4
        start_position = 15
        value_definition = {}

    class BrkPedStkPercPerc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 20
        signal_description = "Brake pedal Ratio in percentage value"
        signal_length = 7
        start_position = 11
        value_definition = {}

    class BrkPedStkPercChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 20
        signal_description = "crc"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class EpbSecSt:
        comments = ""
        factor = 1.0
        initial_value = 4
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 19
        signal_description = "EPB actuator state for second EPB ECU. Only valid for Dual EPB"
        signal_length = 3
        start_position = 31
        value_definition = {'0x0': ' EpbActrSt_Applied', '0x1': ' EpbActrSt_Released', '0x2': ' EpbActrSt_Applying', '0x3': ' EpbActrSt_Releasing', '0x4': ' EpbActrSt_Unknown', '0x5': ' EpbActrSt_HoldApplied', '0x6': ' EpbActrSt_CompleteReleased', '0x7': ' EpbActrSt_HapPrepared'}

    class LatStbIntvIndcn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 18
        signal_description = "lateral stability control status"
        signal_length = 2
        start_position = 28
        value_definition = {'0x0': ' ActvInActv2_Init', '0x1': ' ActvInActv2_InActv', '0x2': ' ActvInActv2_Actv'}

    class WhlEdgeFL:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 17
        signal_description = "the number of recorded pulses"
        signal_length = 8
        start_position = 39
        value_definition = {}

    class WhlEdgeFR:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 16
        signal_description = "the number of recorded pulses"
        signal_length = 8
        start_position = 47
        value_definition = {}

    class WhlEdgeRL:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 26
        signal_description = "the number of recorded pulses"
        signal_length = 8
        start_position = 55
        value_definition = {}

    class WhlEdgeRR:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 25
        signal_description = "the number of recorded pulses"
        signal_length = 8
        start_position = 63
        value_definition = {}


class CCUMCUADToCCUSOCCDEthSignalIPdu04:
    base_type = "Unsigned"
    client_socket = "SocketCdSocSoAdUDP"
    pdu_header_id = 0x104004
    pdu_length_bytes = 2
    receiver = ['CCUSOCCD']
    send_type = "Cyclic-25ms"
    sender = "CCUMCUAD"
    server_socket = "SocketAdMcuSoAdUDP"
    signal_group = {'SteerWhlHndOn': ['SteerWhlHndOnStsQly', 'SteerWhlHndOnSts']}

    class SteerFailrSts:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 3
        signal_description = "Sent from steering system to display to notify driver if no steering torque assist is available. Messages sent from Steering system to DIM"
        signal_length = 3
        start_position = 7
        value_definition = {'0x0': ' SteerFailrSts_NoFailure', '0x1': ' SteerFailrSts_NoUse', '0x2': ' SteerFailrSts_RedFailure', '0x3': ' SteerFailrSts_YellowFailure', '0x4': ' SteerFailrSts_TemperoryAssitFailure', '0x5': ' SteerFailrSts_Reserved1', '0x6': ' SteerFailrSts_Reserved2', '0x7': ' SteerFailrSts_Reserved3'}

    class SteerServoAvlSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 2
        signal_description = "Status of lateral control request"
        signal_length = 1
        start_position = 4
        value_definition = {'0x0': ' AvlSts1_Avl', '0x1': ' AvlSts1_NotAvl'}

    class SteerWhlHndOnStsQly:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1
        signal_description = "Hands on steering wheel information. Confidence value for the DrvrSteerWhlHld estimation calculation, specifically indicating the confidence for the hands off state."
        signal_length = 4
        start_position = 15
        value_definition = {}

    class SteerWhlHndOnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1
        signal_description = "Hands on steering wheel information. Signal indicating whether the driver has his hands on the steering wheel or not."
        signal_length = 2
        start_position = 11
        value_definition = {'0x0': ' SteerWhlHndOnSts_NoInformation', '0x1': ' SteerWhlHndOnSts_HandsOffDetected', '0x2': ' SteerWhlHndOnSts_NotHandsOnOrHandsOff', '0x3': ' SteerWhlHndOnSts_HandsOnDetected'}


class CCUMCUADToCCUSOCCDEthSignalIPdu05:
    base_type = "Unsigned"
    client_socket = "SocketCdSocSoAdUDP"
    pdu_header_id = 0x104005
    pdu_length_bytes = 8
    receiver = ['CCUSOCCD']
    send_type = "Cyclic-30ms"
    sender = "CCUMCUAD"
    server_socket = "SocketAdMcuSoAdUDP"
    signal_group = {}

    class BrkPedlCrashSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 20
        signal_description = "Brake pedal ignation status"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' BeltCrashSts_Invalid', '0x1': ' BeltCrashSts_NotActvn', '0x2': ' BeltCrashSts_Actvn'}

    class DamprFailrSts3:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 19
        signal_description = "Damper failure status"
        signal_length = 2
        start_position = 5
        value_definition = {'0x0': ' DamprSts3_NoError', '0x1': ' DamprSts3_MinorError', '0x2': ' DamprSts3_MajorError', '0x3': ' DamprSts3_CriticalErrpr'}

    class ExtraHiPosn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 18
        signal_description = "Position Extreme high"
        signal_length = 1
        start_position = 3
        value_definition = {'0x0': ' ExtremeHigh_VehicleHeightNotExtremeHigh', '0x1': ' ExtremeHigh_VehicleHeightExtremeHigh'}

    class ExtraLoPosn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 17
        signal_description = "Position extreme low"
        signal_length = 1
        start_position = 2
        value_definition = {'0x0': ' ExtremeLow_VehicleHeightNotextremeLow', '0x1': ' ExtremeLow_VehicleHeightextremeLow'}

    class FrntLeLvlAdjm:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 16
        signal_description = "Level adjustment for FL"
        signal_length = 1
        start_position = 1
        value_definition = {'0x0': ' LevelAdjust_NoAdjustment', '0x1': ' LevelAdjust_Adjustment'}

    class FrntRiLvlAdjm:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 31
        signal_description = "Level adjustment for FR"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': ' LevelAdjust_NoAdjustment', '0x1': ' LevelAdjust_Adjustment'}

    class LvlAdjRestriction:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 30
        signal_description = "level restriction"
        signal_length = 3
        start_position = 15
        value_definition = {'0x0': ' LevelRestriction_InitOrNoRestriction', '0x2': ' LevelRestriction_VoltageTooLowOrHigh', '0x3': ' LevelRestriction_ActuatorTempRestriction', '0x4': ' LevelRestriction_LevelRestrictionByDoorState', '0x5': ' LevelRestriction_LevelContolManuallyDisable', '0x6': ' LevelRestriction_Torsion', '0x7': ' LevelRestriction_Reserved1'}

    class LvlAdjSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 29
        signal_description = "level adjust status"
        signal_length = 3
        start_position = 12
        value_definition = {'0x0': ' AdjustStatus_StaticPosition', '0x1': ' AdjustStatus_RaisingToNewTargetLevel', '0x2': ' AdjustStatus_LoweringToNewTargetLevel', '0x3': ' AdjustStatus_FrozenPendingOfTargetLevelChange', '0x4': ' AdjustStatus_RaisingForLevelAdjustment', '0x5': ' AdjustStatus_LoweringForLevelAdjustment', '0x6': ' AdjustStatus_FrozenPendingForLevelAdjsutment', '0x7': ' AdjustStatus_Reserved'}

    class ReLeLvlAdjm:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 28
        signal_description = "Level adjustment for RL"
        signal_length = 1
        start_position = 9
        value_definition = {'0x0': ' LevelAdjust_NoAdjustment', '0x1': ' LevelAdjust_Adjustment'}

    class ReLeStfnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 27
        signal_description = "Stiffness status for RL"
        signal_length = 1
        start_position = 8
        value_definition = {'0x0': ' OnOff2_On', '0x1': ' OnOff2_Off'}

    class ReRiLvlAdjm:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 26
        signal_description = "Level adjustment for RR"
        signal_length = 1
        start_position = 23
        value_definition = {'0x0': ' LevelAdjust_NoAdjustment', '0x1': ' LevelAdjust_Adjustment'}

    class ReRiStfnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 25
        signal_description = "Stiffness status for RR"
        signal_length = 1
        start_position = 22
        value_definition = {'0x0': ' OnOff2_On', '0x1': ' OnOff2_Off'}

    class SCFailrSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 24
        signal_description = "SC control failure status"
        signal_length = 1
        start_position = 21
        value_definition = {'0x0': ' StiffnessFailrSts_NoFault', '0x1': ' StiffnessFailrSts_Fault'}


class CCUMCUADToCCUSOCCDEthSignalIPdu01:
    base_type = "Unsigned"
    client_socket = "SocketCdSocSoAdUDP"
    pdu_header_id = 0x104001
    pdu_length_bytes = 13
    receiver = ['CCUSOCCD']
    send_type = "Cyclic-100ms"
    sender = "CCUMCUAD"
    server_socket = "SocketAdMcuSoAdUDP"
    signal_group = {'FrntAxleLoad': ['FrntAxleLoadQF2', 'FrntAxleLoadLoadEstimn'], 'ReAxleLoad': ['ReAxleLoadLoadEstimn', 'ReAxleLoadQF2']}

    class FrntAxleLoadQF2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 5
        signal_description = "QF"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': ' QF2_Invalid', '0x1': ' QF2_Low', '0x2': ' QF2_High'}

    class FrntAxleLoadLoadEstimn:
        comments = ""
        factor = 20.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 5
        signal_description = "Axle load estimation"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class IRawCCUAD:
        comments = ""
        factor = 0.1
        initial_value = 4000
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -400
        sig_ub = 4
        signal_description = "Current"
        signal_length = 13
        start_position = 23
        value_definition = {}

    class IRawPSCM1:
        comments = ""
        factor = 0.1
        initial_value = 4000
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -400
        sig_ub = 3
        signal_description = "Current"
        signal_length = 13
        start_position = 26
        value_definition = {}

    class IRawSUM:
        comments = ""
        factor = 0.1
        initial_value = 4000
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -400
        sig_ub = 2
        signal_description = "Current"
        signal_length = 13
        start_position = 45
        value_definition = {}

    class LCFailrIndcn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 48
        signal_description = "Levelling control failure status"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' FailrSts_NoError', '0x1': ' FailrSts_MajorErr', '0x2': ' FailrSts_CtitErr'}

    class ReAxleLoadLoadEstimn:
        comments = ""
        factor = 20.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 69
        signal_description = "Axle load estimation"
        signal_length = 8
        start_position = 63
        value_definition = {}

    class ReAxleLoadQF2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 69
        signal_description = "QF"
        signal_length = 2
        start_position = 71
        value_definition = {'0x0': ' QF2_Invalid', '0x1': ' QF2_Low', '0x2': ' QF2_High'}

    class URawCCUAD:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 68
        signal_description = "Voltage"
        signal_length = 9
        start_position = 77
        value_definition = {}

    class URawPSCM1:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 79
        signal_description = "Voltage"
        signal_length = 9
        start_position = 84
        value_definition = {}

    class URawSUM:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 78
        signal_description = "Voltage"
        signal_length = 9
        start_position = 91
        value_definition = {}
