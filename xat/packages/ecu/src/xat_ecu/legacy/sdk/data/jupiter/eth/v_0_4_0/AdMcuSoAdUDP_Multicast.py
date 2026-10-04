

class CCUMCUADMulticastEthSignalIPdu03:
    base_type = "Unsigned"
    client_socket = "SocketMulticast"
    pdu_header_id = 0x10FF03
    pdu_length_bytes = 8
    receiver = ['CCUSOCCD']
    send_type = "Cyclic-30ms"
    sender = "CCUMCUAD"
    server_socket = "SocketAdMcuSoAdUDP"
    signal_group = {}

    class FrntAxleLvl:
        comments = ""
        factor = 1.0
        initial_value = 14
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 15
        signal_description = "front axle level"
        signal_length = 4
        start_position = 7
        value_definition = {'0x0': ' HeightLevel_LowLevel5', '0x1': ' HeightLevel_LowLevel4', '0x2': ' HeightLevel_LowLevel3', '0x3': ' HeightLevel_LowLevel2', '0x4': ' HeightLevel_LowLevel1', '0x5': ' HeightLevel_NormaLevel', '0x6': ' HeightLevel_HighLevel1', '0x7': ' HeightLevel_HighLevel2', '0x8': ' HeightLevel_HighLevel3', '0x9': ' HeightLevel_HighLevel4', '0xA': ' HeightLevel_HighLevel5', '0xB': ' HeightLevel_Reserved1', '0xC': ' HeightLevel_Reserved2', '0xD': ' HeightLevel_Reserved3', '0xE': ' HeightLevel_InitUnknow', '0xF': ' HeightLevel_Invalid'}

    class ReAxleLvl:
        comments = ""
        factor = 1.0
        initial_value = 14
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 14
        signal_description = "Rear axle level"
        signal_length = 4
        start_position = 3
        value_definition = {'0x0': ' HeightLevel_LowLevel5', '0x1': ' HeightLevel_LowLevel4', '0x2': ' HeightLevel_LowLevel3', '0x3': ' HeightLevel_LowLevel2', '0x4': ' HeightLevel_LowLevel1', '0x5': ' HeightLevel_NormaLevel', '0x6': ' HeightLevel_HighLevel1', '0x7': ' HeightLevel_HighLevel2', '0x8': ' HeightLevel_HighLevel3', '0x9': ' HeightLevel_HighLevel4', '0xA': ' HeightLevel_HighLevel5', '0xB': ' HeightLevel_Reserved1', '0xC': ' HeightLevel_Reserved2', '0xD': ' HeightLevel_Reserved3', '0xE': ' HeightLevel_InitUnknow', '0xF': ' HeightLevel_Invalid'}


class CCUMCUADMulticastEthSignalIPdu04:
    base_type = "Unsigned"
    client_socket = "SocketMulticast"
    pdu_header_id = 0x10FF04
    pdu_length_bytes = 22
    receiver = ['CCUMCUCD', 'CCUSOCCD']
    send_type = "Cyclic-40ms"
    sender = "CCUMCUAD"
    server_socket = "SocketAdMcuSoAdUDP"
    signal_group = {'ArpSts': ['ArpStsActv', 'ArpStsActv', 'ArpStsEna', 'ArpStsEna', 'ArpStsCntr', 'ArpStsCntr', 'ArpStsChks', 'ArpStsChks', 'ArpStsSts2', 'ArpStsSts2'], 'DtcSts': ['DtcStsActv', 'DtcStsActv', 'DtcStsEna', 'DtcStsEna', 'DtcStsCntr', 'DtcStsCntr', 'DtcStsChks', 'DtcStsChks', 'DtcStsSts2', 'DtcStsSts2'], 'DtvSts': ['DtvStsActv', 'DtvStsActv', 'DtvStsEna', 'DtvStsEna', 'DtvStsChks', 'DtvStsChks', 'DtvStsCntr', 'DtvStsCntr', 'DtvStsSts2', 'DtvStsSts2'], 'EbdSts': ['EbdStsEna', 'EbdStsEna', 'EbdStsCntr', 'EbdStsCntr', 'EbdStsChks', 'EbdStsChks', 'EbdStsActv', 'EbdStsActv', 'EbdStsSts2', 'EbdStsSts2'], 'EbpSts': ['EbpStsEna', 'EbpStsEna', 'EbpStsChks', 'EbpStsChks', 'EbpStsActv', 'EbpStsActv', 'EbpStsCntr', 'EbpStsCntr', 'EbpStsSts2', 'EbpStsSts2'], 'TcsSts': ['TcsStsChks', 'TcsStsChks', 'TcsStsEna', 'TcsStsEna', 'TcsStsActv', 'TcsStsActv', 'TcsStsCntr', 'TcsStsCntr', 'TcsStsSts2', 'TcsStsSts2'], 'TscSts': ['TscStsEna', 'TscStsEna', 'TscStsChks', 'TscStsChks', 'TscStsActv', 'TscStsActv', 'TscStsCntr', 'TscStsCntr', 'TscStsSts2', 'TscStsSts2'], 'VdcSts': ['VdcStsActv', 'VdcStsActv', 'VdcStsEna', 'VdcStsEna', 'VdcStsChks', 'VdcStsChks', 'VdcStsCntr', 'VdcStsCntr', 'VdcStsSts2', 'VdcStsSts2']}

    class ArpStsActv:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 21
        signal_description = "Arp function active information"
        signal_length = 2
        start_position = 23
        value_definition = {'0x0': ' Actv_NoActv', '0x1': ' Actv_Actv', '0x2': ' Actv_Reserved1', '0x3': ' Actv_Reserved2'}

    class ArpStsEna:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 21
        signal_description = "Arp function enable information"
        signal_length = 1
        start_position = 12
        value_definition = {'0x0': ' EnableDisable2_Disabled', '0x1': ' EnableDisable2_Enabled'}

    class ArpStsCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 21
        signal_description = "counter"
        signal_length = 4
        start_position = 11
        value_definition = {}

    class ArpStsChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 21
        signal_description = "CRC"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class ArpStsSts2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 21
        signal_description = "function status"
        signal_length = 3
        start_position = 15
        value_definition = {'0x0': ' Sts2_Initial', '0x1': ' Sts2_Normal', '0x2': ' Sts2_Fault', '0x3': ' Sts2_Off'}

    class DtcStsActv:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 20
        signal_description = "DTC function active information"
        signal_length = 2
        start_position = 17
        value_definition = {'0x0': ' Actv_NoActv', '0x1': ' Actv_Actv', '0x2': ' Actv_Reserved1', '0x3': ' Actv_Reserved2'}

    class DtcStsEna:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 20
        signal_description = "DTC function enable information"
        signal_length = 1
        start_position = 36
        value_definition = {'0x0': ' EnableDisable2_Disabled', '0x1': ' EnableDisable2_Enabled'}

    class DtcStsCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 20
        signal_description = "counter"
        signal_length = 4
        start_position = 35
        value_definition = {}

    class DtcStsChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 20
        signal_description = "CRC"
        signal_length = 8
        start_position = 31
        value_definition = {}

    class DtcStsSts2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 20
        signal_description = "function status"
        signal_length = 3
        start_position = 39
        value_definition = {'0x0': ' Sts2_Initial', '0x1': ' Sts2_Normal', '0x2': ' Sts2_Fault', '0x3': ' Sts2_Off'}

    class DtvStsActv:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 19
        signal_description = "Dtv function active information"
        signal_length = 2
        start_position = 63
        value_definition = {'0x0': ' Actv_NoActv', '0x1': ' Actv_Actv', '0x2': ' Actv_Reserved1', '0x3': ' Actv_Reserved2'}

    class DtvStsEna:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 19
        signal_description = "Dtv function enable information"
        signal_length = 1
        start_position = 52
        value_definition = {'0x0': ' EnableDisable2_Disabled', '0x1': ' EnableDisable2_Enabled'}

    class DtvStsChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 19
        signal_description = "CRC"
        signal_length = 8
        start_position = 47
        value_definition = {}

    class DtvStsCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 19
        signal_description = "counter"
        signal_length = 4
        start_position = 51
        value_definition = {}

    class DtvStsSts2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 19
        signal_description = "function status"
        signal_length = 3
        start_position = 55
        value_definition = {'0x0': ' Sts2_Initial', '0x1': ' Sts2_Normal', '0x2': ' Sts2_Fault', '0x3': ' Sts2_Off'}

    class EbdStsEna:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 18
        signal_description = "EBD function enable information"
        signal_length = 1
        start_position = 76
        value_definition = {'0x0': ' EnableDisable2_Disabled', '0x1': ' EnableDisable2_Enabled'}

    class EbdStsCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 18
        signal_description = "Counter"
        signal_length = 4
        start_position = 75
        value_definition = {}

    class EbdStsChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 18
        signal_description = "CRC"
        signal_length = 8
        start_position = 71
        value_definition = {}

    class EbdStsActv:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 18
        signal_description = "EBD function active information"
        signal_length = 2
        start_position = 57
        value_definition = {'0x0': ' Actv_NoActv', '0x1': ' Actv_Actv', '0x2': ' Actv_Reserved1', '0x3': ' Actv_Reserved2'}

    class EbdStsSts2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 18
        signal_description = "function status"
        signal_length = 3
        start_position = 79
        value_definition = {'0x0': ' Sts2_Initial', '0x1': ' Sts2_Normal', '0x2': ' Sts2_Fault', '0x3': ' Sts2_Off'}

    class EbpStsEna:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 61
        signal_description = "Ebp function enable information"
        signal_length = 1
        start_position = 92
        value_definition = {'0x0': ' EnableDisable2_Disabled', '0x1': ' EnableDisable2_Enabled'}

    class EbpStsChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 61
        signal_description = "crc"
        signal_length = 8
        start_position = 87
        value_definition = {}

    class EbpStsActv:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 61
        signal_description = "Ebp function active information"
        signal_length = 2
        start_position = 103
        value_definition = {'0x0': ' Actv_NoActv', '0x1': ' Actv_Actv', '0x2': ' Actv_Reserved1', '0x3': ' Actv_Reserved2'}

    class EbpStsCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 61
        signal_description = "counter"
        signal_length = 4
        start_position = 91
        value_definition = {}

    class EbpStsSts2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 61
        signal_description = "function status"
        signal_length = 3
        start_position = 95
        value_definition = {'0x0': ' Sts2_Initial', '0x1': ' Sts2_Normal', '0x2': ' Sts2_Fault', '0x3': ' Sts2_Off'}

    class EscOffSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 98
        signal_description = "ESC system status"
        signal_length = 3
        start_position = 101
        value_definition = {'0x0': ' EscOff_Init', '0x1': ' EscOff_ok', '0x2': ' EscOff_Fault', '0x3': ' EscOff_Off'}

    class TcsStsChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 60
        signal_description = "CRC"
        signal_length = 8
        start_position = 111
        value_definition = {}

    class TcsStsEna:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 60
        signal_description = "Tcs function enable information"
        signal_length = 1
        start_position = 116
        value_definition = {'0x0': ' EnableDisable2_Disabled', '0x1': ' EnableDisable2_Enabled'}

    class TcsStsActv:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 60
        signal_description = "Tcs function active information"
        signal_length = 2
        start_position = 97
        value_definition = {'0x0': ' Actv_NoActv', '0x1': ' Actv_Actv', '0x2': ' Actv_Reserved1', '0x3': ' Actv_Reserved2'}

    class TcsStsCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 60
        signal_description = "counter"
        signal_length = 4
        start_position = 115
        value_definition = {}

    class TcsStsSts2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 60
        signal_description = "function status"
        signal_length = 3
        start_position = 119
        value_definition = {'0x0': ' Sts2_Initial', '0x1': ' Sts2_Normal', '0x2': ' Sts2_Fault', '0x3': ' Sts2_Off'}

    class TscStsEna:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 59
        signal_description = "Tsc function enable information"
        signal_length = 1
        start_position = 132
        value_definition = {'0x0': ' EnableDisable2_Disabled', '0x1': ' EnableDisable2_Enabled'}

    class TscStsChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 59
        signal_description = "CRC"
        signal_length = 8
        start_position = 127
        value_definition = {}

    class TscStsActv:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 59
        signal_description = "Tsc function active information"
        signal_length = 2
        start_position = 143
        value_definition = {'0x0': ' Actv_NoActv', '0x1': ' Actv_Actv', '0x2': ' Actv_Reserved1', '0x3': ' Actv_Reserved2'}

    class TscStsCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 59
        signal_description = "counter"
        signal_length = 4
        start_position = 131
        value_definition = {}

    class TscStsSts2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 59
        signal_description = "function status"
        signal_length = 3
        start_position = 135
        value_definition = {'0x0': ' Sts2_Initial', '0x1': ' Sts2_Normal', '0x2': ' Sts2_Fault', '0x3': ' Sts2_Off'}

    class VdcStsActv:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 58
        signal_description = "Vdc function active information"
        signal_length = 2
        start_position = 137
        value_definition = {'0x0': ' Actv_NoActv', '0x1': ' Actv_Actv', '0x2': ' Actv_Reserved1', '0x3': ' Actv_Reserved2'}

    class VdcStsEna:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 58
        signal_description = "Vdc function enable information"
        signal_length = 1
        start_position = 156
        value_definition = {'0x0': ' EnableDisable2_Disabled', '0x1': ' EnableDisable2_Enabled'}

    class VdcStsChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 58
        signal_description = "CRC"
        signal_length = 8
        start_position = 151
        value_definition = {}

    class VdcStsCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 58
        signal_description = "counter"
        signal_length = 4
        start_position = 155
        value_definition = {}

    class VdcStsSts2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 58
        signal_description = "function status"
        signal_length = 3
        start_position = 159
        value_definition = {'0x0': ' Sts2_Initial', '0x1': ' Sts2_Normal', '0x2': ' Sts2_Fault', '0x3': ' Sts2_Off'}


class CCUMCUADMulticastEthSignalIPdu01:
    base_type = "Unsigned"
    client_socket = "SocketMulticast"
    pdu_header_id = 0x10FF01
    pdu_length_bytes = 16
    receiver = ['CCUSOCCD', 'LCUL', 'LCUR']
    send_type = "Cyclic-10ms"
    sender = "CCUMCUAD"
    server_socket = "SocketAdMcuSoAdUDP"
    signal_group = {'SteerInfoRef': ['SteerInfoRefSteerPinionAgSpdVal', 'SteerInfoRefCntr', 'SteerInfoRefChks', 'SteerInfoRefSteerPinionAgSpdValQf', 'SteerInfoRefSteerPinionAgVal', 'SteerInfoRefSteerWhlTqVal', 'SteerInfoRefSteerPinionAgValQf', 'SteerInfoRefSteerTorqueValQf']}

    class CurrentLvl:
        comments = ""
        factor = 1.0
        initial_value = 14
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 65
        signal_description = "Current level"
        signal_length = 4
        start_position = 7
        value_definition = {'0x0': ' HeightLevel_LowLevel5', '0x1': ' HeightLevel_LowLevel4', '0x2': ' HeightLevel_LowLevel3', '0x3': ' HeightLevel_LowLevel2', '0x4': ' HeightLevel_LowLevel1', '0x5': ' HeightLevel_NormaLevel', '0x6': ' HeightLevel_HighLevel1', '0x7': ' HeightLevel_HighLevel2', '0x8': ' HeightLevel_HighLevel3', '0x9': ' HeightLevel_HighLevel4', '0xA': ' HeightLevel_HighLevel5', '0xB': ' HeightLevel_Reserved1', '0xC': ' HeightLevel_Reserved2', '0xD': ' HeightLevel_Reserved3', '0xE': ' HeightLevel_InitUnknow', '0xF': ' HeightLevel_Invalid'}

    class SteerInfoRefSteerPinionAgSpdVal:
        comments = ""
        factor = 0.0078125
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 64
        signal_description = "Calculated pinion steer angle speed at the front steering device "
        signal_length = 14
        start_position = 31
        value_definition = {}

    class SteerInfoRefCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 64
        signal_description = "Counter for PinionSteerAgGroup"
        signal_length = 4
        start_position = 19
        value_definition = {}

    class SteerInfoRefChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 64
        signal_description = "Checksum for PinionSteerAgGroup"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class SteerInfoRefSteerPinionAgSpdValQf:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 64
        signal_description = "Quality factor for PinionSteerAgSpd1"
        signal_length = 2
        start_position = 33
        value_definition = {}

    class SteerInfoRefSteerPinionAgVal:
        comments = ""
        factor = 0.000976563
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 64
        signal_description = "Calculated pinion steer angle at the front steering device"
        signal_length = 15
        start_position = 47
        value_definition = {}

    class SteerInfoRefSteerWhlTqVal:
        comments = ""
        factor = 0.00390625
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 64
        signal_description = "Torque on steering wheel"
        signal_length = 14
        start_position = 63
        value_definition = {}

    class SteerInfoRefSteerPinionAgValQf:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 64
        signal_description = "Quality factor for PinionSteerAg1"
        signal_length = 2
        start_position = 23
        value_definition = {}

    class SteerInfoRefSteerTorqueValQf:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 64
        signal_description = "Quality factor for SteerWhlTq"
        signal_length = 2
        start_position = 21
        value_definition = {}


class CCUMCUADMulticastEthSignalIPdu02:
    base_type = "Unsigned"
    client_socket = "SocketMulticast"
    pdu_header_id = 0x10FF02
    pdu_length_bytes = 16
    receiver = ['LCUL', 'LCUR', 'CCUMCUCD', 'CCUSOCCD']
    send_type = "Cyclic-20ms"
    sender = "CCUMCUAD"
    server_socket = "SocketAdMcuSoAdUDP"
    signal_group = {'BrkLiReq': ['BrkLiReqChks', 'BrkLiReqChks', 'BrkLiReqCntr', 'BrkLiReqCntr', 'BrkLiReqBrkLiReq', 'BrkLiReqBrkLiReq'], 'BrkPedlInfo': ['BrkPedlInfoNotPsd', 'BrkPedlInfoNotPsd', 'BrkPedlInfoNotPsd', 'BrkPedlInfoNotPsd', 'BrkPedlInfoPsd', 'BrkPedlInfoPsd', 'BrkPedlInfoPsd', 'BrkPedlInfoPsd', 'BrkPedlInfoQf', 'BrkPedlInfoQf', 'BrkPedlInfoQf', 'BrkPedlInfoQf', 'BrkPedlInfoChks', 'BrkPedlInfoChks', 'BrkPedlInfoChks', 'BrkPedlInfoChks', 'BrkPedlInfoCntr', 'BrkPedlInfoCntr', 'BrkPedlInfoCntr', 'BrkPedlInfoCntr'], 'WhlPlsCntr': ['WhlPlsCntrFL', 'WhlPlsCntrFL', 'WhlPlsCntrCntr', 'WhlPlsCntrCntr', 'WhlPlsCntrChks', 'WhlPlsCntrChks', 'WhlPlsCntrRR', 'WhlPlsCntrRR', 'WhlPlsCntrFR', 'WhlPlsCntrFR', 'WhlPlsCntrRL', 'WhlPlsCntrRL']}

    class BrkLiReqChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 10
        signal_description = "crc"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class BrkLiReqCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 10
        signal_description = "counter"
        signal_length = 4
        start_position = 15
        value_definition = {}

    class BrkLiReqBrkLiReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 10
        signal_description = "brake light request"
        signal_length = 1
        start_position = 11
        value_definition = {'0x0': ' ReqSts1_NotReqd', '0x1': ' ReqSts1_Reqd'}

    class BrkPedlInfoNotPsd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 9
        signal_description = "Set to 1 if brake pedal is not pressed, otherwise 0"
        signal_length = 1
        start_position = 31
        value_definition = {'0x0': ' NoYes1_No', '0x1': ' NoYes1_Yes'}

    class BrkPedlInfoPsd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 9
        signal_description = "Set to 1 if brake pedal is pressed, otherwise 0"
        signal_length = 1
        start_position = 30
        value_definition = {'0x0': ' NoYes1_No', '0x1': ' NoYes1_Yes'}

    class BrkPedlInfoQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 9
        signal_description = "Quality factor"
        signal_length = 2
        start_position = 29
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class BrkPedlInfoChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 9
        signal_description = "crc"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class BrkPedlInfoCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 9
        signal_description = "counter"
        signal_length = 4
        start_position = 27
        value_definition = {}

    class WhlPlsCntrFL:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 8
        signal_description = "Wheel rotation ticks for each individual wheel,fl"
        signal_length = 8
        start_position = 55
        value_definition = {}

    class WhlPlsCntrCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 8
        signal_description = "counter"
        signal_length = 4
        start_position = 43
        value_definition = {}

    class WhlPlsCntrChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 8
        signal_description = "crc"
        signal_length = 8
        start_position = 39
        value_definition = {}

    class WhlPlsCntrRR:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 8
        signal_description = "Wheel rotation ticks for each individual wheel,rr"
        signal_length = 8
        start_position = 79
        value_definition = {}

    class WhlPlsCntrFR:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 8
        signal_description = "Wheel rotation ticks for each individual wheel,fr"
        signal_length = 8
        start_position = 63
        value_definition = {}

    class WhlPlsCntrRL:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 8
        signal_description = "Wheel rotation ticks for each individual wheel,rl"
        signal_length = 8
        start_position = 71
        value_definition = {}
