class RcmlToBgmBodyExpoDiagRespFrame:
    msg_name = "RcmlToBgmBodyExpoDiagRespFrame"
    msg_id = 1717
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "RCML"
    rx_nodes = ['BGM']


class CemBodyExpoFr112:
    msg_name = "CemBodyExpoFr112"
    msg_id = 846
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR']

    class DwnLoadDynLtgPrmForFrntRIGrp22ContinueTime_1_CemBodyExpoSignalIPdu112:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp22ContinueTime_1_CemBodyExpoSignalIPdu112"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForFrntRIGrp22Mode1_1_CemBodyExpoSignalIPdu112:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp22Mode1_1_CemBodyExpoSignalIPdu112"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode4_Off': 0, 'Mode4_On': 1, 'Mode4_GradualOn': 2, 'Mode4_GradualOff': 3, 'Mode4_ForwardWipingOn': 4, 'Mode4_BackwardWipingOn': 5, 'Mode4_OutwardWipingOn': 6, 'Mode4_InwardWipingOn': 7, 'Mode4_ForwardWipingOff': 8, 'Mode4_BackwardWipingOff': 9, 'Mode4_OutwardWipingOff': 10, 'Mode4_InwardWipingOff': 11, 'Mode4_ForwardScanning': 12, 'Mode4_BackwardScanning': 13, 'Mode4_BreathOn': 14, 'Mode4_BreathOff': 15, 'Mode4_1stHalfONand2ndHalfOFF': 16, 'Mode4_HalfOFFHalfON': 17, 'Mode4_HalfDimmingONHalfOFF': 18, 'Mode4_HalfDimmingONHalfON': 19, 'Mode4_HalfOFFHalfDimmingON': 20, 'Mode4_HalfONHalfDimmingON': 21, 'Mode4_HalfDimmingOFFHalfOFF': 22, 'Mode4_HalfDimmingOFFHalfON': 23, 'Mode4_HalfOFFHalfDimmingOFF': 24, 'Mode4_HalfONHalfDimmingOFF': 25, 'Mode4_SingleOn1': 26, 'Mode4_SingleOn2': 27, 'Mode4_SingleOn3': 28, 'Mode4_SingleOn4': 29, 'Mode4_SingleOn5': 30, 'Mode4_SingleOn6': 31, 'Mode4_SingleOn7': 32, 'Mode4_SingleOn8': 33, 'Mode4_SingleOn9': 34, 'Mode4_SingleOn10': 35, 'Mode4_SingleOn11': 36, 'Mode4_SingleOn12': 37, 'Mode4_SingleOff1': 38, 'Mode4_SingleOff2': 39, 'Mode4_SingleOff3': 40, 'Mode4_SingleOff4': 41, 'Mode4_SingleOff5': 42, 'Mode4_SingleOff6': 43, 'Mode4_SingleOff7': 44, 'Mode4_SingleOff8': 45, 'Mode4_SingleOff9': 46, 'Mode4_SingleOff10': 47, 'Mode4_SingleOff11': 48, 'Mode4_SingleOff12': 49}
        compute_method = None
        length = 6
        startbit = 23
        byte = 2
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntRIGrp22OffsetTime_1_CemBodyExpoSignalIPdu112:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp22OffsetTime_1_CemBodyExpoSignalIPdu112"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 31
        byte = 3
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntRIGrp22HighBrightness_1_CemBodyExpoSignalIPdu112:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp22HighBrightness_1_CemBodyExpoSignalIPdu112"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DwnLoadDynLtgPrmForFrntRIGrp22LowBrightness_1_CemBodyExpoSignalIPdu112:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp22LowBrightness_1_CemBodyExpoSignalIPdu112"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DwnLoadDynLtgPrmForFrntRIGrp22Timestamp_1_CemBodyExpoSignalIPdu112:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp22Timestamp_1_CemBodyExpoSignalIPdu112"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5


class CemBodyExpoCommonFr11:
    msg_name = "CemBodyExpoCommonFr11"
    msg_id = 390
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.045
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR', 'HCML']

    class TrafficSignForADB2AdbDetdQly_1_CemBodyExpoCommonSignalIPdu11:
        sig_name = "TrafficSignForADB2AdbDetdQly_1_CemBodyExpoCommonSignalIPdu11"
        sig_start_bit = 11
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ClassnQly_Low': 0, 'ClassnQly_Medium': 1, 'ClassnQly_High': 2}
        compute_method = None
        length = 2
        startbit = 11
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class TrafficSignForADB2AdbVertAgBot_1_CemBodyExpoCommonSignalIPdu11:
        sig_name = "TrafficSignForADB2AdbVertAgBot_1_CemBodyExpoCommonSignalIPdu11"
        sig_start_bit = 35
        sig_length = 9
        sig_value_factor = 0.05
        sig_value_offset = "-3"
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 60
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 35
        bmuws_info = [(4, 0b00001111, 0b11110000, 4, 0), (5, 0b11111000, 0b00000111, 5, 3)]

    class TrafficSignForADB2AdbHozlAgLe_1_CemBodyExpoCommonSignalIPdu11:
        sig_name = "TrafficSignForADB2AdbHozlAgLe_1_CemBodyExpoCommonSignalIPdu11"
        sig_start_bit = 9
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = "-40"
        sig_value_min = 0
        sig_value_max = 1600
        sig_byteorder = "Motorola"
        sig_value_init = 800
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 9
        bmuws_info = [(1, 0b00000011, 0b11111100, 2, 0), (2, 0b11111111, 0b00000000, 8, 0), (3, 0b10000000, 0b01111111, 1, 7)]

    class TrafficSignForADB2AdbTrkInfo_1_CemBodyExpoCommonSignalIPdu11:
        sig_name = "TrafficSignForADB2AdbTrkInfo_1_CemBodyExpoCommonSignalIPdu11"
        sig_start_bit = 42
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NotTracked': 0, 'Tracking': 1}
        compute_method = None
        length = 1
        startbit = 42
        byte = 5
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class TrafficSignForADB2AdbVertAgTop_1_CemBodyExpoCommonSignalIPdu11:
        sig_name = "TrafficSignForADB2AdbVertAgTop_1_CemBodyExpoCommonSignalIPdu11"
        sig_start_bit = 41
        sig_length = 9
        sig_value_factor = 0.05
        sig_value_offset = "-3"
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 60
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 41
        bmuws_info = [(5, 0b00000011, 0b11111100, 2, 0), (6, 0b11111110, 0b00000001, 7, 1)]

    class TrafficSignForADB2AdbHozlAgRi_1_CemBodyExpoCommonSignalIPdu11:
        sig_name = "TrafficSignForADB2AdbHozlAgRi_1_CemBodyExpoCommonSignalIPdu11"
        sig_start_bit = 30
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = "-40"
        sig_value_min = 0
        sig_value_max = 1600
        sig_byteorder = "Motorola"
        sig_value_init = 800
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 30
        bmuws_info = [(3, 0b01111111, 0b10000000, 7, 0), (4, 0b11110000, 0b00001111, 4, 4)]

    class TrafficSignForADB2AdbAbsDist_1_CemBodyExpoCommonSignalIPdu11:
        sig_name = "TrafficSignForADB2AdbAbsDist_1_CemBodyExpoCommonSignalIPdu11"
        sig_start_bit = 7
        sig_length = 12
        sig_value_factor = 0.2
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11110000, 0b00001111, 4, 4)]


class CemBodyExpoFr73:
    msg_name = "CemBodyExpoFr73"
    msg_id = 807
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCML']

    class DwnLoadDynLtgPrmForFrntLeGrp7LowBrightness_1_CemBodyExpoSignalIPdu73:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp7LowBrightness_1_CemBodyExpoSignalIPdu73"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DwnLoadDynLtgPrmForFrntLeGrp7OffsetTime_1_CemBodyExpoSignalIPdu73:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp7OffsetTime_1_CemBodyExpoSignalIPdu73"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 31
        byte = 3
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntLeGrp7Mode1_1_CemBodyExpoSignalIPdu73:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp7Mode1_1_CemBodyExpoSignalIPdu73"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode4_Off': 0, 'Mode4_On': 1, 'Mode4_GradualOn': 2, 'Mode4_GradualOff': 3, 'Mode4_ForwardWipingOn': 4, 'Mode4_BackwardWipingOn': 5, 'Mode4_OutwardWipingOn': 6, 'Mode4_InwardWipingOn': 7, 'Mode4_ForwardWipingOff': 8, 'Mode4_BackwardWipingOff': 9, 'Mode4_OutwardWipingOff': 10, 'Mode4_InwardWipingOff': 11, 'Mode4_ForwardScanning': 12, 'Mode4_BackwardScanning': 13, 'Mode4_BreathOn': 14, 'Mode4_BreathOff': 15, 'Mode4_1stHalfONand2ndHalfOFF': 16, 'Mode4_HalfOFFHalfON': 17, 'Mode4_HalfDimmingONHalfOFF': 18, 'Mode4_HalfDimmingONHalfON': 19, 'Mode4_HalfOFFHalfDimmingON': 20, 'Mode4_HalfONHalfDimmingON': 21, 'Mode4_HalfDimmingOFFHalfOFF': 22, 'Mode4_HalfDimmingOFFHalfON': 23, 'Mode4_HalfOFFHalfDimmingOFF': 24, 'Mode4_HalfONHalfDimmingOFF': 25, 'Mode4_SingleOn1': 26, 'Mode4_SingleOn2': 27, 'Mode4_SingleOn3': 28, 'Mode4_SingleOn4': 29, 'Mode4_SingleOn5': 30, 'Mode4_SingleOn6': 31, 'Mode4_SingleOn7': 32, 'Mode4_SingleOn8': 33, 'Mode4_SingleOn9': 34, 'Mode4_SingleOn10': 35, 'Mode4_SingleOn11': 36, 'Mode4_SingleOn12': 37, 'Mode4_SingleOff1': 38, 'Mode4_SingleOff2': 39, 'Mode4_SingleOff3': 40, 'Mode4_SingleOff4': 41, 'Mode4_SingleOff5': 42, 'Mode4_SingleOff6': 43, 'Mode4_SingleOff7': 44, 'Mode4_SingleOff8': 45, 'Mode4_SingleOff9': 46, 'Mode4_SingleOff10': 47, 'Mode4_SingleOff11': 48, 'Mode4_SingleOff12': 49}
        compute_method = None
        length = 6
        startbit = 23
        byte = 2
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntLeGrp7ContinueTime_1_CemBodyExpoSignalIPdu73:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp7ContinueTime_1_CemBodyExpoSignalIPdu73"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForFrntLeGrp7HighBrightness_1_CemBodyExpoSignalIPdu73:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp7HighBrightness_1_CemBodyExpoSignalIPdu73"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DwnLoadDynLtgPrmForFrntLeGrp7Timestamp_1_CemBodyExpoSignalIPdu73:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp7Timestamp_1_CemBodyExpoSignalIPdu73"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5


class CemBodyExpoFr51:
    msg_name = "CemBodyExpoFr51"
    msg_id = 538
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR', 'RCMR', 'HCML', 'RCMM', 'RCML']

    class IndcrSts_1_CemBodyExpoSignalIPdu51:
        sig_name = "IndcrSts_1_CemBodyExpoSignalIPdu51"
        sig_start_bit = 52
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'IndcrSts1_Off': 0, 'IndcrSts1_LeOn': 1, 'IndcrSts1_RiOn': 2, 'IndcrSts1_LeAndRiOn': 3}
        compute_method = None
        length = 2
        startbit = 52
        byte = 6
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class ActvnOfIndcrIndcrOut_1_CemBodyExpoSignalIPdu51:
        sig_name = "ActvnOfIndcrIndcrOut_1_CemBodyExpoSignalIPdu51"
        sig_start_bit = 37
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'IndcrSts1_Off': 0, 'IndcrSts1_LeOn': 1, 'IndcrSts1_RiOn': 2, 'IndcrSts1_LeAndRiOn': 3}
        compute_method = None
        length = 2
        startbit = 37
        byte = 4
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class IndcrPatCmd1WdTiOff_0_CemBodyExpoSignalIPdu51:
        sig_name = "IndcrPatCmd1WdTiOff_0_CemBodyExpoSignalIPdu51"
        sig_start_bit = 7
        sig_length = 16
        sig_value_factor = 0.001
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 65535
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class IndcrPatCmd1WdTiOn_0_CemBodyExpoSignalIPdu51:
        sig_name = "IndcrPatCmd1WdTiOn_0_CemBodyExpoSignalIPdu51"
        sig_start_bit = 23
        sig_length = 16
        sig_value_factor = 0.001
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 65535
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class ActvnOfIndcrIndcrOutChks_1_CemBodyExpoSignalIPdu51:
        sig_name = "ActvnOfIndcrIndcrOutChks_1_CemBodyExpoSignalIPdu51"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ActvnOfIndcrIndcrOutCntr_1_CemBodyExpoSignalIPdu51:
        sig_name = "ActvnOfIndcrIndcrOutCntr_1_CemBodyExpoSignalIPdu51"
        sig_start_bit = 35
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 35
        byte = 4
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class EmgyBrkLiIndcrTurn:
        sig_name = "EmgyBrkLiIndcrTurn"
        sig_start_bit = 49
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffCrit1_NotVld1': 0, 'OnOffCrit1_Off': 1, 'OnOffCrit1_On': 2, 'OnOffCrit1_NotVld2': 3}
        compute_method = None
        length = 2
        startbit = 49
        byte = 6
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0


class BgmToRcmlBodyExpoDiagReqFrame:
    msg_name = "BgmToRcmlBodyExpoDiagReqFrame"
    msg_id = 1973
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RCML']


class CemBodyExpoCommonFr22:
    msg_name = "CemBodyExpoCommonFr22"
    msg_id = 400
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.045
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR', 'HCML']

    class SuspPosnVertAgGenQf_1_CemBodyExpoCommonSignalIPdu22:
        sig_name = "SuspPosnVertAgGenQf_1_CemBodyExpoCommonSignalIPdu22"
        sig_start_bit = 45
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 45
        byte = 5
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class SuspPosnVertLvlFrnt_1_CemBodyExpoCommonSignalIPdu22:
        sig_name = "SuspPosnVertLvlFrnt_1_CemBodyExpoCommonSignalIPdu22"
        sig_start_bit = 14
        sig_length = 15
        sig_value_factor = "6.2E-5"
        sig_value_offset = 0.0
        sig_value_min = -16129
        sig_value_max = 16130
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 14
        bmuws_info = [(1, 0b01111111, 0b10000000, 7, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class SuspPosnVertLvlRe_1_CemBodyExpoCommonSignalIPdu22:
        sig_name = "SuspPosnVertLvlRe_1_CemBodyExpoCommonSignalIPdu22"
        sig_start_bit = 30
        sig_length = 15
        sig_value_factor = "6.2E-5"
        sig_value_offset = 0.0
        sig_value_min = -16129
        sig_value_max = 16130
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 30
        bmuws_info = [(3, 0b01111111, 0b10000000, 7, 0), (4, 0b11111111, 0b00000000, 8, 0)]

    class SuspPosnVertAgSuspPosnVertAg_1_CemBodyExpoCommonSignalIPdu22:
        sig_name = "SuspPosnVertAgSuspPosnVertAg_1_CemBodyExpoCommonSignalIPdu22"
        sig_start_bit = 43
        sig_length = 12
        sig_value_factor = "1.278941807E-4"
        sig_value_offset = 0.0
        sig_value_min = -2046
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 43
        bmuws_info = [(5, 0b00001111, 0b11110000, 4, 0), (6, 0b11111111, 0b00000000, 8, 0)]

    class SuspPosnVertLvlReQf_1_CemBodyExpoCommonSignalIPdu22:
        sig_name = "SuspPosnVertLvlReQf_1_CemBodyExpoCommonSignalIPdu22"
        sig_start_bit = 3
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 3
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class SuspPosnVertLvlFrntQf_1_CemBodyExpoCommonSignalIPdu22:
        sig_name = "SuspPosnVertLvlFrntQf_1_CemBodyExpoCommonSignalIPdu22"
        sig_start_bit = 1
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0


class HcmmToBgmBodyExpoDiagRespFrame:
    msg_name = "HcmmToBgmBodyExpoDiagRespFrame"
    msg_id = 1714
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "PCM"
    rx_nodes = ['BGM']


class CemBodyExpoFr89:
    msg_name = "CemBodyExpoFr89"
    msg_id = 823
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCML']

    class DwnLoadDynLtgPrmForFrntLeGrp23Mode1_1_CemBodyExpoSignalIPdu89:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp23Mode1_1_CemBodyExpoSignalIPdu89"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode4_Off': 0, 'Mode4_On': 1, 'Mode4_GradualOn': 2, 'Mode4_GradualOff': 3, 'Mode4_ForwardWipingOn': 4, 'Mode4_BackwardWipingOn': 5, 'Mode4_OutwardWipingOn': 6, 'Mode4_InwardWipingOn': 7, 'Mode4_ForwardWipingOff': 8, 'Mode4_BackwardWipingOff': 9, 'Mode4_OutwardWipingOff': 10, 'Mode4_InwardWipingOff': 11, 'Mode4_ForwardScanning': 12, 'Mode4_BackwardScanning': 13, 'Mode4_BreathOn': 14, 'Mode4_BreathOff': 15, 'Mode4_1stHalfONand2ndHalfOFF': 16, 'Mode4_HalfOFFHalfON': 17, 'Mode4_HalfDimmingONHalfOFF': 18, 'Mode4_HalfDimmingONHalfON': 19, 'Mode4_HalfOFFHalfDimmingON': 20, 'Mode4_HalfONHalfDimmingON': 21, 'Mode4_HalfDimmingOFFHalfOFF': 22, 'Mode4_HalfDimmingOFFHalfON': 23, 'Mode4_HalfOFFHalfDimmingOFF': 24, 'Mode4_HalfONHalfDimmingOFF': 25, 'Mode4_SingleOn1': 26, 'Mode4_SingleOn2': 27, 'Mode4_SingleOn3': 28, 'Mode4_SingleOn4': 29, 'Mode4_SingleOn5': 30, 'Mode4_SingleOn6': 31, 'Mode4_SingleOn7': 32, 'Mode4_SingleOn8': 33, 'Mode4_SingleOn9': 34, 'Mode4_SingleOn10': 35, 'Mode4_SingleOn11': 36, 'Mode4_SingleOn12': 37, 'Mode4_SingleOff1': 38, 'Mode4_SingleOff2': 39, 'Mode4_SingleOff3': 40, 'Mode4_SingleOff4': 41, 'Mode4_SingleOff5': 42, 'Mode4_SingleOff6': 43, 'Mode4_SingleOff7': 44, 'Mode4_SingleOff8': 45, 'Mode4_SingleOff9': 46, 'Mode4_SingleOff10': 47, 'Mode4_SingleOff11': 48, 'Mode4_SingleOff12': 49}
        compute_method = None
        length = 6
        startbit = 23
        byte = 2
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntLeGrp23ContinueTime_1_CemBodyExpoSignalIPdu89:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp23ContinueTime_1_CemBodyExpoSignalIPdu89"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForFrntLeGrp23LowBrightness_1_CemBodyExpoSignalIPdu89:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp23LowBrightness_1_CemBodyExpoSignalIPdu89"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DwnLoadDynLtgPrmForFrntLeGrp23Timestamp_1_CemBodyExpoSignalIPdu89:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp23Timestamp_1_CemBodyExpoSignalIPdu89"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DwnLoadDynLtgPrmForFrntLeGrp23OffsetTime_1_CemBodyExpoSignalIPdu89:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp23OffsetTime_1_CemBodyExpoSignalIPdu89"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 31
        byte = 3
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntLeGrp23HighBrightness_1_CemBodyExpoSignalIPdu89:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp23HighBrightness_1_CemBodyExpoSignalIPdu89"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4


class CemBodyExpoFr52:
    msg_name = "CemBodyExpoFr52"
    msg_id = 326
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RCMM']

    class DwnLoadDynLitPrmForLedLogoLampOffsTiPrm_1_CemBodyExpoSignalIPdu52:
        sig_name = "DwnLoadDynLitPrmForLedLogoLampOffsTiPrm_1_CemBodyExpoSignalIPdu52"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmForLedLogoLampModePrm_1_CemBodyExpoSignalIPdu52:
        sig_name = "DwnLoadDynLitPrmForLedLogoLampModePrm_1_CemBodyExpoSignalIPdu52"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode1_Off': 0, 'Mode1_On': 1, 'Mode1_GradualOn': 2, 'Mode1_GradualOff': 3, 'Mode1_ForwardWipingOn': 4, 'Mode1_BackwardWipingOn': 5, 'Mode1_OutwardWipingOn': 6, 'Mode1_InwardWipingOn': 7, 'Mode1_ForwardWipingOff': 8, 'Mode1_BackwardWipingOff': 9, 'Mode1_OutwardWipingOff': 10, 'Mode1_InwardWipingOff': 11, 'Mode1_ForwardScanning': 12, 'Mode1_BackwardScanning': 13, 'Mode1_BreathOn': 14, 'Mode1_BreathOff': 15, 'Mode1_Spare1': 16, 'Mode1_Spare2': 17}
        compute_method = None
        length = 5
        startbit = 13
        byte = 1
        mask = 0b00111110
        unmask = 0b11000001
        shift = 1

    class DwnLoadDynLitPrmForLedLogoLampContTiPrm_1_CemBodyExpoSignalIPdu52:
        sig_name = "DwnLoadDynLitPrmForLedLogoLampContTiPrm_1_CemBodyExpoSignalIPdu52"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmForLedLogoLampLowBriPrm_1_CemBodyExpoSignalIPdu52:
        sig_name = "DwnLoadDynLitPrmForLedLogoLampLowBriPrm_1_CemBodyExpoSignalIPdu52"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmForLedLogoLampUpprBriPrm_1_CemBodyExpoSignalIPdu52:
        sig_name = "DwnLoadDynLitPrmForLedLogoLampUpprBriPrm_1_CemBodyExpoSignalIPdu52"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmForLedLogoLampTistamp_1_CemBodyExpoSignalIPdu52:
        sig_name = "DwnLoadDynLitPrmForLedLogoLampTistamp_1_CemBodyExpoSignalIPdu52"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]


class CemBodyExpoFr32:
    msg_name = "CemBodyExpoFr32"
    msg_id = 317
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCML']

    class DwnLoadDynLtgPrmForLedDaytiRunngLampLeOffsTiPrm_1_CemBodyExpoSignalIPdu32:
        sig_name = "DwnLoadDynLtgPrmForLedDaytiRunngLampLeOffsTiPrm_1_CemBodyExpoSignalIPdu32"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLtgPrmForLedDaytiRunngLampLeLowBriPrm_1_CemBodyExpoSignalIPdu32:
        sig_name = "DwnLoadDynLtgPrmForLedDaytiRunngLampLeLowBriPrm_1_CemBodyExpoSignalIPdu32"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForLedDaytiRunngLampLeContTiPrm_1_CemBodyExpoSignalIPdu32:
        sig_name = "DwnLoadDynLtgPrmForLedDaytiRunngLampLeContTiPrm_1_CemBodyExpoSignalIPdu32"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLtgPrmForLedDaytiRunngLampLeTistamp_1_CemBodyExpoSignalIPdu32:
        sig_name = "DwnLoadDynLtgPrmForLedDaytiRunngLampLeTistamp_1_CemBodyExpoSignalIPdu32"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLtgPrmForLedDaytiRunngLampLeUpprBriPrm_1_CemBodyExpoSignalIPdu32:
        sig_name = "DwnLoadDynLtgPrmForLedDaytiRunngLampLeUpprBriPrm_1_CemBodyExpoSignalIPdu32"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForLedDaytiRunngLampLeModePrm_1_CemBodyExpoSignalIPdu32:
        sig_name = "DwnLoadDynLtgPrmForLedDaytiRunngLampLeModePrm_1_CemBodyExpoSignalIPdu32"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode1_Off': 0, 'Mode1_On': 1, 'Mode1_GradualOn': 2, 'Mode1_GradualOff': 3, 'Mode1_ForwardWipingOn': 4, 'Mode1_BackwardWipingOn': 5, 'Mode1_OutwardWipingOn': 6, 'Mode1_InwardWipingOn': 7, 'Mode1_ForwardWipingOff': 8, 'Mode1_BackwardWipingOff': 9, 'Mode1_OutwardWipingOff': 10, 'Mode1_InwardWipingOff': 11, 'Mode1_ForwardScanning': 12, 'Mode1_BackwardScanning': 13, 'Mode1_BreathOn': 14, 'Mode1_BreathOff': 15, 'Mode1_Spare1': 16, 'Mode1_Spare2': 17}
        compute_method = None
        length = 5
        startbit = 13
        byte = 1
        mask = 0b00111110
        unmask = 0b11000001
        shift = 1


class CemBodyExpoFr34:
    msg_name = "CemBodyExpoFr34"
    msg_id = 319
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCML']

    class DwnLoadDynLtgPrmForLedFrntPosnLampLeOffsTiPrm_1_CemBodyExpoSignalIPdu34:
        sig_name = "DwnLoadDynLtgPrmForLedFrntPosnLampLeOffsTiPrm_1_CemBodyExpoSignalIPdu34"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLtgPrmForLedFrntPosnLampLeContTiPrm_1_CemBodyExpoSignalIPdu34:
        sig_name = "DwnLoadDynLtgPrmForLedFrntPosnLampLeContTiPrm_1_CemBodyExpoSignalIPdu34"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLtgPrmForLedFrntPosnLampLeLowBriPrm_1_CemBodyExpoSignalIPdu34:
        sig_name = "DwnLoadDynLtgPrmForLedFrntPosnLampLeLowBriPrm_1_CemBodyExpoSignalIPdu34"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForLedFrntPosnLampLeTistamp_1_CemBodyExpoSignalIPdu34:
        sig_name = "DwnLoadDynLtgPrmForLedFrntPosnLampLeTistamp_1_CemBodyExpoSignalIPdu34"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLtgPrmForLedFrntPosnLampLeUpprBriPrm_1_CemBodyExpoSignalIPdu34:
        sig_name = "DwnLoadDynLtgPrmForLedFrntPosnLampLeUpprBriPrm_1_CemBodyExpoSignalIPdu34"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForLedFrntPosnLampLeModePrm_1_CemBodyExpoSignalIPdu34:
        sig_name = "DwnLoadDynLtgPrmForLedFrntPosnLampLeModePrm_1_CemBodyExpoSignalIPdu34"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode1_Off': 0, 'Mode1_On': 1, 'Mode1_GradualOn': 2, 'Mode1_GradualOff': 3, 'Mode1_ForwardWipingOn': 4, 'Mode1_BackwardWipingOn': 5, 'Mode1_OutwardWipingOn': 6, 'Mode1_InwardWipingOn': 7, 'Mode1_ForwardWipingOff': 8, 'Mode1_BackwardWipingOff': 9, 'Mode1_OutwardWipingOff': 10, 'Mode1_InwardWipingOff': 11, 'Mode1_ForwardScanning': 12, 'Mode1_BackwardScanning': 13, 'Mode1_BreathOn': 14, 'Mode1_BreathOff': 15, 'Mode1_Spare1': 16, 'Mode1_Spare2': 17}
        compute_method = None
        length = 5
        startbit = 13
        byte = 1
        mask = 0b00111110
        unmask = 0b11000001
        shift = 1


class CemBodyExpoFr93:
    msg_name = "CemBodyExpoFr93"
    msg_id = 827
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR']

    class DwnLoadDynLtgPrmForFrntRIGrp3ContinueTime_1_CemBodyExpoSignalIPdu93:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp3ContinueTime_1_CemBodyExpoSignalIPdu93"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForFrntRIGrp3Mode1_1_CemBodyExpoSignalIPdu93:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp3Mode1_1_CemBodyExpoSignalIPdu93"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode4_Off': 0, 'Mode4_On': 1, 'Mode4_GradualOn': 2, 'Mode4_GradualOff': 3, 'Mode4_ForwardWipingOn': 4, 'Mode4_BackwardWipingOn': 5, 'Mode4_OutwardWipingOn': 6, 'Mode4_InwardWipingOn': 7, 'Mode4_ForwardWipingOff': 8, 'Mode4_BackwardWipingOff': 9, 'Mode4_OutwardWipingOff': 10, 'Mode4_InwardWipingOff': 11, 'Mode4_ForwardScanning': 12, 'Mode4_BackwardScanning': 13, 'Mode4_BreathOn': 14, 'Mode4_BreathOff': 15, 'Mode4_1stHalfONand2ndHalfOFF': 16, 'Mode4_HalfOFFHalfON': 17, 'Mode4_HalfDimmingONHalfOFF': 18, 'Mode4_HalfDimmingONHalfON': 19, 'Mode4_HalfOFFHalfDimmingON': 20, 'Mode4_HalfONHalfDimmingON': 21, 'Mode4_HalfDimmingOFFHalfOFF': 22, 'Mode4_HalfDimmingOFFHalfON': 23, 'Mode4_HalfOFFHalfDimmingOFF': 24, 'Mode4_HalfONHalfDimmingOFF': 25, 'Mode4_SingleOn1': 26, 'Mode4_SingleOn2': 27, 'Mode4_SingleOn3': 28, 'Mode4_SingleOn4': 29, 'Mode4_SingleOn5': 30, 'Mode4_SingleOn6': 31, 'Mode4_SingleOn7': 32, 'Mode4_SingleOn8': 33, 'Mode4_SingleOn9': 34, 'Mode4_SingleOn10': 35, 'Mode4_SingleOn11': 36, 'Mode4_SingleOn12': 37, 'Mode4_SingleOff1': 38, 'Mode4_SingleOff2': 39, 'Mode4_SingleOff3': 40, 'Mode4_SingleOff4': 41, 'Mode4_SingleOff5': 42, 'Mode4_SingleOff6': 43, 'Mode4_SingleOff7': 44, 'Mode4_SingleOff8': 45, 'Mode4_SingleOff9': 46, 'Mode4_SingleOff10': 47, 'Mode4_SingleOff11': 48, 'Mode4_SingleOff12': 49}
        compute_method = None
        length = 6
        startbit = 23
        byte = 2
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntRIGrp3HighBrightness_1_CemBodyExpoSignalIPdu93:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp3HighBrightness_1_CemBodyExpoSignalIPdu93"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DwnLoadDynLtgPrmForFrntRIGrp3LowBrightness_1_CemBodyExpoSignalIPdu93:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp3LowBrightness_1_CemBodyExpoSignalIPdu93"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DwnLoadDynLtgPrmForFrntRIGrp3OffsetTime_1_CemBodyExpoSignalIPdu93:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp3OffsetTime_1_CemBodyExpoSignalIPdu93"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 31
        byte = 3
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntRIGrp3Timestamp_1_CemBodyExpoSignalIPdu93:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp3Timestamp_1_CemBodyExpoSignalIPdu93"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5


class CemBodyExpoFr111:
    msg_name = "CemBodyExpoFr111"
    msg_id = 845
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR']

    class DwnLoadDynLtgPrmForFrntRIGrp21Timestamp_1_CemBodyExpoSignalIPdu111:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp21Timestamp_1_CemBodyExpoSignalIPdu111"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DwnLoadDynLtgPrmForFrntRIGrp21HighBrightness_1_CemBodyExpoSignalIPdu111:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp21HighBrightness_1_CemBodyExpoSignalIPdu111"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DwnLoadDynLtgPrmForFrntRIGrp21LowBrightness_1_CemBodyExpoSignalIPdu111:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp21LowBrightness_1_CemBodyExpoSignalIPdu111"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DwnLoadDynLtgPrmForFrntRIGrp21ContinueTime_1_CemBodyExpoSignalIPdu111:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp21ContinueTime_1_CemBodyExpoSignalIPdu111"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForFrntRIGrp21Mode1_1_CemBodyExpoSignalIPdu111:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp21Mode1_1_CemBodyExpoSignalIPdu111"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode4_Off': 0, 'Mode4_On': 1, 'Mode4_GradualOn': 2, 'Mode4_GradualOff': 3, 'Mode4_ForwardWipingOn': 4, 'Mode4_BackwardWipingOn': 5, 'Mode4_OutwardWipingOn': 6, 'Mode4_InwardWipingOn': 7, 'Mode4_ForwardWipingOff': 8, 'Mode4_BackwardWipingOff': 9, 'Mode4_OutwardWipingOff': 10, 'Mode4_InwardWipingOff': 11, 'Mode4_ForwardScanning': 12, 'Mode4_BackwardScanning': 13, 'Mode4_BreathOn': 14, 'Mode4_BreathOff': 15, 'Mode4_1stHalfONand2ndHalfOFF': 16, 'Mode4_HalfOFFHalfON': 17, 'Mode4_HalfDimmingONHalfOFF': 18, 'Mode4_HalfDimmingONHalfON': 19, 'Mode4_HalfOFFHalfDimmingON': 20, 'Mode4_HalfONHalfDimmingON': 21, 'Mode4_HalfDimmingOFFHalfOFF': 22, 'Mode4_HalfDimmingOFFHalfON': 23, 'Mode4_HalfOFFHalfDimmingOFF': 24, 'Mode4_HalfONHalfDimmingOFF': 25, 'Mode4_SingleOn1': 26, 'Mode4_SingleOn2': 27, 'Mode4_SingleOn3': 28, 'Mode4_SingleOn4': 29, 'Mode4_SingleOn5': 30, 'Mode4_SingleOn6': 31, 'Mode4_SingleOn7': 32, 'Mode4_SingleOn8': 33, 'Mode4_SingleOn9': 34, 'Mode4_SingleOn10': 35, 'Mode4_SingleOn11': 36, 'Mode4_SingleOn12': 37, 'Mode4_SingleOff1': 38, 'Mode4_SingleOff2': 39, 'Mode4_SingleOff3': 40, 'Mode4_SingleOff4': 41, 'Mode4_SingleOff5': 42, 'Mode4_SingleOff6': 43, 'Mode4_SingleOff7': 44, 'Mode4_SingleOff8': 45, 'Mode4_SingleOff9': 46, 'Mode4_SingleOff10': 47, 'Mode4_SingleOff11': 48, 'Mode4_SingleOff12': 49}
        compute_method = None
        length = 6
        startbit = 23
        byte = 2
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntRIGrp21OffsetTime_1_CemBodyExpoSignalIPdu111:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp21OffsetTime_1_CemBodyExpoSignalIPdu111"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 31
        byte = 3
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2


class CemBodyExpoFr72:
    msg_name = "CemBodyExpoFr72"
    msg_id = 806
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCML']

    class DwnLoadDynLtgPrmForFrntLeGrp6Mode1_1_CemBodyExpoSignalIPdu72:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp6Mode1_1_CemBodyExpoSignalIPdu72"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode4_Off': 0, 'Mode4_On': 1, 'Mode4_GradualOn': 2, 'Mode4_GradualOff': 3, 'Mode4_ForwardWipingOn': 4, 'Mode4_BackwardWipingOn': 5, 'Mode4_OutwardWipingOn': 6, 'Mode4_InwardWipingOn': 7, 'Mode4_ForwardWipingOff': 8, 'Mode4_BackwardWipingOff': 9, 'Mode4_OutwardWipingOff': 10, 'Mode4_InwardWipingOff': 11, 'Mode4_ForwardScanning': 12, 'Mode4_BackwardScanning': 13, 'Mode4_BreathOn': 14, 'Mode4_BreathOff': 15, 'Mode4_1stHalfONand2ndHalfOFF': 16, 'Mode4_HalfOFFHalfON': 17, 'Mode4_HalfDimmingONHalfOFF': 18, 'Mode4_HalfDimmingONHalfON': 19, 'Mode4_HalfOFFHalfDimmingON': 20, 'Mode4_HalfONHalfDimmingON': 21, 'Mode4_HalfDimmingOFFHalfOFF': 22, 'Mode4_HalfDimmingOFFHalfON': 23, 'Mode4_HalfOFFHalfDimmingOFF': 24, 'Mode4_HalfONHalfDimmingOFF': 25, 'Mode4_SingleOn1': 26, 'Mode4_SingleOn2': 27, 'Mode4_SingleOn3': 28, 'Mode4_SingleOn4': 29, 'Mode4_SingleOn5': 30, 'Mode4_SingleOn6': 31, 'Mode4_SingleOn7': 32, 'Mode4_SingleOn8': 33, 'Mode4_SingleOn9': 34, 'Mode4_SingleOn10': 35, 'Mode4_SingleOn11': 36, 'Mode4_SingleOn12': 37, 'Mode4_SingleOff1': 38, 'Mode4_SingleOff2': 39, 'Mode4_SingleOff3': 40, 'Mode4_SingleOff4': 41, 'Mode4_SingleOff5': 42, 'Mode4_SingleOff6': 43, 'Mode4_SingleOff7': 44, 'Mode4_SingleOff8': 45, 'Mode4_SingleOff9': 46, 'Mode4_SingleOff10': 47, 'Mode4_SingleOff11': 48, 'Mode4_SingleOff12': 49}
        compute_method = None
        length = 6
        startbit = 23
        byte = 2
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntLeGrp6Timestamp_1_CemBodyExpoSignalIPdu72:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp6Timestamp_1_CemBodyExpoSignalIPdu72"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DwnLoadDynLtgPrmForFrntLeGrp6ContinueTime_1_CemBodyExpoSignalIPdu72:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp6ContinueTime_1_CemBodyExpoSignalIPdu72"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForFrntLeGrp6OffsetTime_1_CemBodyExpoSignalIPdu72:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp6OffsetTime_1_CemBodyExpoSignalIPdu72"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 31
        byte = 3
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntLeGrp6HighBrightness_1_CemBodyExpoSignalIPdu72:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp6HighBrightness_1_CemBodyExpoSignalIPdu72"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DwnLoadDynLtgPrmForFrntLeGrp6LowBrightness_1_CemBodyExpoSignalIPdu72:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp6LowBrightness_1_CemBodyExpoSignalIPdu72"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0


class CemBodyExpoFr79:
    msg_name = "CemBodyExpoFr79"
    msg_id = 813
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCML']

    class DwnLoadDynLtgPrmForFrntLeGrp13ContinueTime_1_CemBodyExpoSignalIPdu79:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp13ContinueTime_1_CemBodyExpoSignalIPdu79"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForFrntLeGrp13OffsetTime_1_CemBodyExpoSignalIPdu79:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp13OffsetTime_1_CemBodyExpoSignalIPdu79"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 31
        byte = 3
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntLeGrp13Timestamp_1_CemBodyExpoSignalIPdu79:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp13Timestamp_1_CemBodyExpoSignalIPdu79"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DwnLoadDynLtgPrmForFrntLeGrp13HighBrightness_1_CemBodyExpoSignalIPdu79:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp13HighBrightness_1_CemBodyExpoSignalIPdu79"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DwnLoadDynLtgPrmForFrntLeGrp13LowBrightness_1_CemBodyExpoSignalIPdu79:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp13LowBrightness_1_CemBodyExpoSignalIPdu79"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DwnLoadDynLtgPrmForFrntLeGrp13Mode1_1_CemBodyExpoSignalIPdu79:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp13Mode1_1_CemBodyExpoSignalIPdu79"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode4_Off': 0, 'Mode4_On': 1, 'Mode4_GradualOn': 2, 'Mode4_GradualOff': 3, 'Mode4_ForwardWipingOn': 4, 'Mode4_BackwardWipingOn': 5, 'Mode4_OutwardWipingOn': 6, 'Mode4_InwardWipingOn': 7, 'Mode4_ForwardWipingOff': 8, 'Mode4_BackwardWipingOff': 9, 'Mode4_OutwardWipingOff': 10, 'Mode4_InwardWipingOff': 11, 'Mode4_ForwardScanning': 12, 'Mode4_BackwardScanning': 13, 'Mode4_BreathOn': 14, 'Mode4_BreathOff': 15, 'Mode4_1stHalfONand2ndHalfOFF': 16, 'Mode4_HalfOFFHalfON': 17, 'Mode4_HalfDimmingONHalfOFF': 18, 'Mode4_HalfDimmingONHalfON': 19, 'Mode4_HalfOFFHalfDimmingON': 20, 'Mode4_HalfONHalfDimmingON': 21, 'Mode4_HalfDimmingOFFHalfOFF': 22, 'Mode4_HalfDimmingOFFHalfON': 23, 'Mode4_HalfOFFHalfDimmingOFF': 24, 'Mode4_HalfONHalfDimmingOFF': 25, 'Mode4_SingleOn1': 26, 'Mode4_SingleOn2': 27, 'Mode4_SingleOn3': 28, 'Mode4_SingleOn4': 29, 'Mode4_SingleOn5': 30, 'Mode4_SingleOn6': 31, 'Mode4_SingleOn7': 32, 'Mode4_SingleOn8': 33, 'Mode4_SingleOn9': 34, 'Mode4_SingleOn10': 35, 'Mode4_SingleOn11': 36, 'Mode4_SingleOn12': 37, 'Mode4_SingleOff1': 38, 'Mode4_SingleOff2': 39, 'Mode4_SingleOff3': 40, 'Mode4_SingleOff4': 41, 'Mode4_SingleOff5': 42, 'Mode4_SingleOff6': 43, 'Mode4_SingleOff7': 44, 'Mode4_SingleOff8': 45, 'Mode4_SingleOff9': 46, 'Mode4_SingleOff10': 47, 'Mode4_SingleOff11': 48, 'Mode4_SingleOff12': 49}
        compute_method = None
        length = 6
        startbit = 23
        byte = 2
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2


class CemBodyExpoFr96:
    msg_name = "CemBodyExpoFr96"
    msg_id = 830
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR']

    class DwnLoadDynLtgPrmForFrntRIGrp6Mode1_1_CemBodyExpoSignalIPdu96:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp6Mode1_1_CemBodyExpoSignalIPdu96"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode4_Off': 0, 'Mode4_On': 1, 'Mode4_GradualOn': 2, 'Mode4_GradualOff': 3, 'Mode4_ForwardWipingOn': 4, 'Mode4_BackwardWipingOn': 5, 'Mode4_OutwardWipingOn': 6, 'Mode4_InwardWipingOn': 7, 'Mode4_ForwardWipingOff': 8, 'Mode4_BackwardWipingOff': 9, 'Mode4_OutwardWipingOff': 10, 'Mode4_InwardWipingOff': 11, 'Mode4_ForwardScanning': 12, 'Mode4_BackwardScanning': 13, 'Mode4_BreathOn': 14, 'Mode4_BreathOff': 15, 'Mode4_1stHalfONand2ndHalfOFF': 16, 'Mode4_HalfOFFHalfON': 17, 'Mode4_HalfDimmingONHalfOFF': 18, 'Mode4_HalfDimmingONHalfON': 19, 'Mode4_HalfOFFHalfDimmingON': 20, 'Mode4_HalfONHalfDimmingON': 21, 'Mode4_HalfDimmingOFFHalfOFF': 22, 'Mode4_HalfDimmingOFFHalfON': 23, 'Mode4_HalfOFFHalfDimmingOFF': 24, 'Mode4_HalfONHalfDimmingOFF': 25, 'Mode4_SingleOn1': 26, 'Mode4_SingleOn2': 27, 'Mode4_SingleOn3': 28, 'Mode4_SingleOn4': 29, 'Mode4_SingleOn5': 30, 'Mode4_SingleOn6': 31, 'Mode4_SingleOn7': 32, 'Mode4_SingleOn8': 33, 'Mode4_SingleOn9': 34, 'Mode4_SingleOn10': 35, 'Mode4_SingleOn11': 36, 'Mode4_SingleOn12': 37, 'Mode4_SingleOff1': 38, 'Mode4_SingleOff2': 39, 'Mode4_SingleOff3': 40, 'Mode4_SingleOff4': 41, 'Mode4_SingleOff5': 42, 'Mode4_SingleOff6': 43, 'Mode4_SingleOff7': 44, 'Mode4_SingleOff8': 45, 'Mode4_SingleOff9': 46, 'Mode4_SingleOff10': 47, 'Mode4_SingleOff11': 48, 'Mode4_SingleOff12': 49}
        compute_method = None
        length = 6
        startbit = 23
        byte = 2
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntRIGrp6Timestamp_1_CemBodyExpoSignalIPdu96:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp6Timestamp_1_CemBodyExpoSignalIPdu96"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DwnLoadDynLtgPrmForFrntRIGrp6OffsetTime_1_CemBodyExpoSignalIPdu96:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp6OffsetTime_1_CemBodyExpoSignalIPdu96"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 31
        byte = 3
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntRIGrp6ContinueTime_1_CemBodyExpoSignalIPdu96:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp6ContinueTime_1_CemBodyExpoSignalIPdu96"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForFrntRIGrp6LowBrightness_1_CemBodyExpoSignalIPdu96:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp6LowBrightness_1_CemBodyExpoSignalIPdu96"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DwnLoadDynLtgPrmForFrntRIGrp6HighBrightness_1_CemBodyExpoSignalIPdu96:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp6HighBrightness_1_CemBodyExpoSignalIPdu96"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4


class CemBodyExpoFr48:
    msg_name = "CemBodyExpoFr48"
    msg_id = 324
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RCMM']

    class DwnLoadDynLitPrmForLedMkrLampRi2ContTiPrm_1_CemBodyExpoSignalIPdu48:
        sig_name = "DwnLoadDynLitPrmForLedMkrLampRi2ContTiPrm_1_CemBodyExpoSignalIPdu48"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmForLedMkrLampRi2ModePrm_1_CemBodyExpoSignalIPdu48:
        sig_name = "DwnLoadDynLitPrmForLedMkrLampRi2ModePrm_1_CemBodyExpoSignalIPdu48"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode1_Off': 0, 'Mode1_On': 1, 'Mode1_GradualOn': 2, 'Mode1_GradualOff': 3, 'Mode1_ForwardWipingOn': 4, 'Mode1_BackwardWipingOn': 5, 'Mode1_OutwardWipingOn': 6, 'Mode1_InwardWipingOn': 7, 'Mode1_ForwardWipingOff': 8, 'Mode1_BackwardWipingOff': 9, 'Mode1_OutwardWipingOff': 10, 'Mode1_InwardWipingOff': 11, 'Mode1_ForwardScanning': 12, 'Mode1_BackwardScanning': 13, 'Mode1_BreathOn': 14, 'Mode1_BreathOff': 15, 'Mode1_Spare1': 16, 'Mode1_Spare2': 17}
        compute_method = None
        length = 5
        startbit = 13
        byte = 1
        mask = 0b00111110
        unmask = 0b11000001
        shift = 1

    class DwnLoadDynLitPrmForLedMkrLampRi2UpprBriPrm_1_CemBodyExpoSignalIPdu48:
        sig_name = "DwnLoadDynLitPrmForLedMkrLampRi2UpprBriPrm_1_CemBodyExpoSignalIPdu48"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmForLedMkrLampRi2OffsTiPrm_1_CemBodyExpoSignalIPdu48:
        sig_name = "DwnLoadDynLitPrmForLedMkrLampRi2OffsTiPrm_1_CemBodyExpoSignalIPdu48"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmForLedMkrLampRi2LowBriPrm_1_CemBodyExpoSignalIPdu48:
        sig_name = "DwnLoadDynLitPrmForLedMkrLampRi2LowBriPrm_1_CemBodyExpoSignalIPdu48"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmForLedMkrLampRi2Tistamp_1_CemBodyExpoSignalIPdu48:
        sig_name = "DwnLoadDynLitPrmForLedMkrLampRi2Tistamp_1_CemBodyExpoSignalIPdu48"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]


class CemBodyExpoFr97:
    msg_name = "CemBodyExpoFr97"
    msg_id = 831
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR']

    class DwnLoadDynLtgPrmForFrntRIGrp7Mode1_1_CemBodyExpoSignalIPdu97:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp7Mode1_1_CemBodyExpoSignalIPdu97"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode4_Off': 0, 'Mode4_On': 1, 'Mode4_GradualOn': 2, 'Mode4_GradualOff': 3, 'Mode4_ForwardWipingOn': 4, 'Mode4_BackwardWipingOn': 5, 'Mode4_OutwardWipingOn': 6, 'Mode4_InwardWipingOn': 7, 'Mode4_ForwardWipingOff': 8, 'Mode4_BackwardWipingOff': 9, 'Mode4_OutwardWipingOff': 10, 'Mode4_InwardWipingOff': 11, 'Mode4_ForwardScanning': 12, 'Mode4_BackwardScanning': 13, 'Mode4_BreathOn': 14, 'Mode4_BreathOff': 15, 'Mode4_1stHalfONand2ndHalfOFF': 16, 'Mode4_HalfOFFHalfON': 17, 'Mode4_HalfDimmingONHalfOFF': 18, 'Mode4_HalfDimmingONHalfON': 19, 'Mode4_HalfOFFHalfDimmingON': 20, 'Mode4_HalfONHalfDimmingON': 21, 'Mode4_HalfDimmingOFFHalfOFF': 22, 'Mode4_HalfDimmingOFFHalfON': 23, 'Mode4_HalfOFFHalfDimmingOFF': 24, 'Mode4_HalfONHalfDimmingOFF': 25, 'Mode4_SingleOn1': 26, 'Mode4_SingleOn2': 27, 'Mode4_SingleOn3': 28, 'Mode4_SingleOn4': 29, 'Mode4_SingleOn5': 30, 'Mode4_SingleOn6': 31, 'Mode4_SingleOn7': 32, 'Mode4_SingleOn8': 33, 'Mode4_SingleOn9': 34, 'Mode4_SingleOn10': 35, 'Mode4_SingleOn11': 36, 'Mode4_SingleOn12': 37, 'Mode4_SingleOff1': 38, 'Mode4_SingleOff2': 39, 'Mode4_SingleOff3': 40, 'Mode4_SingleOff4': 41, 'Mode4_SingleOff5': 42, 'Mode4_SingleOff6': 43, 'Mode4_SingleOff7': 44, 'Mode4_SingleOff8': 45, 'Mode4_SingleOff9': 46, 'Mode4_SingleOff10': 47, 'Mode4_SingleOff11': 48, 'Mode4_SingleOff12': 49}
        compute_method = None
        length = 6
        startbit = 23
        byte = 2
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntRIGrp7Timestamp_1_CemBodyExpoSignalIPdu97:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp7Timestamp_1_CemBodyExpoSignalIPdu97"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DwnLoadDynLtgPrmForFrntRIGrp7HighBrightness_1_CemBodyExpoSignalIPdu97:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp7HighBrightness_1_CemBodyExpoSignalIPdu97"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DwnLoadDynLtgPrmForFrntRIGrp7OffsetTime_1_CemBodyExpoSignalIPdu97:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp7OffsetTime_1_CemBodyExpoSignalIPdu97"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 31
        byte = 3
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntRIGrp7LowBrightness_1_CemBodyExpoSignalIPdu97:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp7LowBrightness_1_CemBodyExpoSignalIPdu97"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DwnLoadDynLtgPrmForFrntRIGrp7ContinueTime_1_CemBodyExpoSignalIPdu97:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp7ContinueTime_1_CemBodyExpoSignalIPdu97"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class CemBodyExpoFr25:
    msg_name = "CemBodyExpoFr25"
    msg_id = 120
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.085
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR', 'HCML', 'RCMM']

    class LvlgSwtSetReqADModCtrlInhbn:
        sig_name = "LvlgSwtSetReqADModCtrlInhbn"
        sig_start_bit = 54
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoInhb': 0, 'L12LgtCtrlModInhb': 1, 'AutoParkingModInhb': 2, 'L12AndAutoParkingModInhb': 3, 'L3ADModInhb': 4, 'L3ADAndL12LgtCtrlModInhb': 5, 'L3ADAndAutoParkingModInhb': 6, 'L3ADAndAutoParkingAndL12LgtCtrlModInhb': 7}
        compute_method = None
        length = 3
        startbit = 54
        byte = 6
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class LvlgSwtSetReqChks:
        sig_name = "LvlgSwtSetReqChks"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class LvlgSwtSetReqCntr:
        sig_name = "LvlgSwtSetReqCntr"
        sig_start_bit = 51
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 51
        byte = 6
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class ActvnOfReLogoLamp:
        sig_name = "ActvnOfReLogoLamp"
        sig_start_bit = 7
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class OutdBriChks_1_CemBodyExpoSignalIPdu25:
        sig_name = "OutdBriChks_1_CemBodyExpoSignalIPdu25"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class OutdBriCntr_1_CemBodyExpoSignalIPdu25:
        sig_name = "OutdBriCntr_1_CemBodyExpoSignalIPdu25"
        sig_start_bit = 35
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 35
        byte = 4
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class OutdBriSts_1_CemBodyExpoSignalIPdu25:
        sig_name = "OutdBriSts_1_CemBodyExpoSignalIPdu25"
        sig_start_bit = 37
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OutdBriSts_Ukwn': 0, 'OutdBriSts_Night': 1, 'OutdBriSts_Day': 2, 'OutdBriSts_Invld': 3}
        compute_method = None
        length = 2
        startbit = 37
        byte = 4
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4


class CemBodyExpoCommonFr21:
    msg_name = "CemBodyExpoCommonFr21"
    msg_id = 64
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.015
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR', 'RCMR', 'HCML', 'RCMM', 'PCM', 'RCML']

    class VehModMngtGlbSafe1PwrLvlElecMai_4_CemBodyExpoCommonSignalIPdu21:
        sig_name = "VehModMngtGlbSafe1PwrLvlElecMai_4_CemBodyExpoCommonSignalIPdu21"
        sig_start_bit = 19
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 19
        byte = 2
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class VehModMngtGlbSafe1FltEgyCnsWdSts_4_CemBodyExpoCommonSignalIPdu21:
        sig_name = "VehModMngtGlbSafe1FltEgyCnsWdSts_4_CemBodyExpoCommonSignalIPdu21"
        sig_start_bit = 36
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltEgyCns1_NoFlt': 0, 'FltEgyCns1_Flt': 1}
        compute_method = None
        length = 1
        startbit = 36
        byte = 4
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VehModMngtGlbSafe1Chks_4_CemBodyExpoCommonSignalIPdu21:
        sig_name = "VehModMngtGlbSafe1Chks_4_CemBodyExpoCommonSignalIPdu21"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehModMngtGlbSafe1Cntr_4_CemBodyExpoCommonSignalIPdu21:
        sig_name = "VehModMngtGlbSafe1Cntr_4_CemBodyExpoCommonSignalIPdu21"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class RainLi_1_CemBodyExpoCommonSignalIPdu21:
        sig_name = "RainLi_1_CemBodyExpoCommonSignalIPdu21"
        sig_start_bit = 47
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 47
        byte = 5
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class WipgAutFrntMod_1_CemBodyExpoCommonSignalIPdu21:
        sig_name = "WipgAutFrntMod_1_CemBodyExpoCommonSignalIPdu21"
        sig_start_bit = 59
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WipgAutFrntMod_Off': 0, 'WipgAutFrntMod_ImdtMod': 1, 'WipgAutFrntMod_IntlMod': 2, 'WipgAutFrntMod_ContnsMod': 3}
        compute_method = None
        length = 2
        startbit = 59
        byte = 7
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VehModMngtGlbSafe1EgyLvlElecSubtyp_4_CemBodyExpoCommonSignalIPdu21:
        sig_name = "VehModMngtGlbSafe1EgyLvlElecSubtyp_4_CemBodyExpoCommonSignalIPdu21"
        sig_start_bit = 31
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 31
        byte = 3
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class CameraStsforAHBC_1_CemBodyExpoCommonSignalIPdu21:
        sig_name = "CameraStsforAHBC_1_CemBodyExpoCommonSignalIPdu21"
        sig_start_bit = 62
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AdbCamSts_Idle': 0, 'AdbCamSts_Normal': 1, 'AdbCamSts_Blocking': 2, 'AdbCamSts_Unknown': 3}
        compute_method = None
        length = 2
        startbit = 62
        byte = 7
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp_4_CemBodyExpoCommonSignalIPdu21:
        sig_name = "VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp_4_CemBodyExpoCommonSignalIPdu21"
        sig_start_bit = 35
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 35
        byte = 4
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class VehModMngtGlbSafe1UsgModSts_4_CemBodyExpoCommonSignalIPdu21:
        sig_name = "VehModMngtGlbSafe1UsgModSts_4_CemBodyExpoCommonSignalIPdu21"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 13
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'UsgModSts1_UsgModAbdnd': 0, 'UsgModSts1_UsgModInActv': 1, 'UsgModSts1_UsgModCnvinc': 2, 'UsgModSts1_UsgModActv': 11, 'UsgModSts1_UsgModDrvg': 13}
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class VehModMngtGlbSafe1PwrLvlElecSubtyp_4_CemBodyExpoCommonSignalIPdu21:
        sig_name = "VehModMngtGlbSafe1PwrLvlElecSubtyp_4_CemBodyExpoCommonSignalIPdu21"
        sig_start_bit = 23
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 23
        byte = 2
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class VehModMngtGlbSafe1EgyLvlElecMai_4_CemBodyExpoCommonSignalIPdu21:
        sig_name = "VehModMngtGlbSafe1EgyLvlElecMai_4_CemBodyExpoCommonSignalIPdu21"
        sig_start_bit = 27
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 27
        byte = 3
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class VehModMngtGlbSafe1CarModSts1_4_CemBodyExpoCommonSignalIPdu21:
        sig_name = "VehModMngtGlbSafe1CarModSts1_4_CemBodyExpoCommonSignalIPdu21"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CarModSts1_CarModNorm': 0, 'CarModSts1_CarModTrnsp': 1, 'CarModSts1_CarModFcy': 2, 'CarModSts1_CarModCrash': 3, 'CarModSts1_CarModDyno': 5}
        compute_method = None
        length = 3
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5


class EtctoHcmlXCPFr01:
    msg_name = "EtctoHcmlXCPFr01"
    msg_id = 1430
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CCM"
    rx_nodes = ['HCML']


class CemBodyExpoCommonFr15:
    msg_name = "CemBodyExpoCommonFr15"
    msg_id = 394
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.045
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR', 'HCML']

    class VehObjforADB3AdbClassn_1_CemBodyExpoCommonSignalIPdu15:
        sig_name = "VehObjforADB3AdbClassn_1_CemBodyExpoCommonSignalIPdu15"
        sig_start_bit = 13
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AdbClassn_NoVehicle': 0, 'AdbClassn_Car': 1, 'AdbClassn_Truck': 2, 'AdbClassn_Bus': 3, 'AdbClassn_BikeOrMotorBike': 4, 'AdbClassn_Pedestrain': 5, 'AdbClassn_Mixed': 6, 'AdbClassn_Unknown': 7}
        compute_method = None
        length = 3
        startbit = 13
        byte = 1
        mask = 0b00111000
        unmask = 0b11000111
        shift = 3

    class VehObjforADB3AdbHozlAgLe_1_CemBodyExpoCommonSignalIPdu15:
        sig_name = "VehObjforADB3AdbHozlAgLe_1_CemBodyExpoCommonSignalIPdu15"
        sig_start_bit = 10
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = "-40"
        sig_value_min = 0
        sig_value_max = 1600
        sig_byteorder = "Motorola"
        sig_value_init = 800
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 10
        bmuws_info = [(1, 0b00000111, 0b11111000, 3, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class VehObjforADB3AdbVertAg_1_CemBodyExpoCommonSignalIPdu15:
        sig_name = "VehObjforADB3AdbVertAg_1_CemBodyExpoCommonSignalIPdu15"
        sig_start_bit = 63
        sig_length = 5
        sig_value_factor = 0.5
        sig_value_offset = "-3"
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Motorola"
        sig_value_init = 6
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 63
        byte = 7
        mask = 0b11111000
        unmask = 0b00000111
        shift = 3

    class VehObjforADB3AdbAbsDist_1_CemBodyExpoCommonSignalIPdu15:
        sig_name = "VehObjforADB3AdbAbsDist_1_CemBodyExpoCommonSignalIPdu15"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class VehObjforADB3AdbObjDir_1_CemBodyExpoCommonSignalIPdu15:
        sig_name = "VehObjforADB3AdbObjDir_1_CemBodyExpoCommonSignalIPdu15"
        sig_start_bit = 36
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AdbObjDir_Idle': 0, 'AdbObjDir_Oncoming': 1, 'AdbObjDir_Preceding': 2, 'AdbObjDir_Others': 3}
        compute_method = None
        length = 2
        startbit = 36
        byte = 4
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class VehObjforADB3AdbTrkInfo_1_CemBodyExpoCommonSignalIPdu15:
        sig_name = "VehObjforADB3AdbTrkInfo_1_CemBodyExpoCommonSignalIPdu15"
        sig_start_bit = 48
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NotTracked': 0, 'Tracking': 1}
        compute_method = None
        length = 1
        startbit = 48
        byte = 6
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VehObjforADB3AdbObjHozlAgSpdRi_1_CemBodyExpoCommonSignalIPdu15:
        sig_name = "VehObjforADB3AdbObjHozlAgSpdRi_1_CemBodyExpoCommonSignalIPdu15"
        sig_start_bit = 41
        sig_length = 9
        sig_value_factor = 0.2
        sig_value_offset = "-50"
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 250
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 41
        bmuws_info = [(5, 0b00000011, 0b11111100, 2, 0), (6, 0b11111110, 0b00000001, 7, 1)]

    class VehObjforADB3AdbHozlAgRi_1_CemBodyExpoCommonSignalIPdu15:
        sig_name = "VehObjforADB3AdbHozlAgRi_1_CemBodyExpoCommonSignalIPdu15"
        sig_start_bit = 31
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = "-40"
        sig_value_min = 0
        sig_value_max = 1600
        sig_byteorder = "Motorola"
        sig_value_init = 800
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11100000, 0b00011111, 3, 5)]

    class VehObjforADB3AdbObjHozlAgSpdLe_1_CemBodyExpoCommonSignalIPdu15:
        sig_name = "VehObjforADB3AdbObjHozlAgSpdLe_1_CemBodyExpoCommonSignalIPdu15"
        sig_start_bit = 34
        sig_length = 9
        sig_value_factor = 0.2
        sig_value_offset = "-50"
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 250
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 34
        bmuws_info = [(4, 0b00000111, 0b11111000, 3, 0), (5, 0b11111100, 0b00000011, 6, 2)]


class CemBodyExpoFr03:
    msg_name = "CemBodyExpoFr03"
    msg_id = 289
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RCMM']

    class DwnLoadDynLitPrmLedReFogLampRi2Tistamp_1_CemBodyExpoSignalIPdu03:
        sig_name = "DwnLoadDynLitPrmLedReFogLampRi2Tistamp_1_CemBodyExpoSignalIPdu03"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmLedReFogLampRi2UpprBriPrm_1_CemBodyExpoSignalIPdu03:
        sig_name = "DwnLoadDynLitPrmLedReFogLampRi2UpprBriPrm_1_CemBodyExpoSignalIPdu03"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmLedReFogLampRi2LowBriPrm_1_CemBodyExpoSignalIPdu03:
        sig_name = "DwnLoadDynLitPrmLedReFogLampRi2LowBriPrm_1_CemBodyExpoSignalIPdu03"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmLedReFogLampRi2OffsTiPrm_1_CemBodyExpoSignalIPdu03:
        sig_name = "DwnLoadDynLitPrmLedReFogLampRi2OffsTiPrm_1_CemBodyExpoSignalIPdu03"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedReFogLampRi2ModePrm_1_CemBodyExpoSignalIPdu03:
        sig_name = "DwnLoadDynLitPrmLedReFogLampRi2ModePrm_1_CemBodyExpoSignalIPdu03"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode1_Off': 0, 'Mode1_On': 1, 'Mode1_GradualOn': 2, 'Mode1_GradualOff': 3, 'Mode1_ForwardWipingOn': 4, 'Mode1_BackwardWipingOn': 5, 'Mode1_OutwardWipingOn': 6, 'Mode1_InwardWipingOn': 7, 'Mode1_ForwardWipingOff': 8, 'Mode1_BackwardWipingOff': 9, 'Mode1_OutwardWipingOff': 10, 'Mode1_InwardWipingOff': 11, 'Mode1_ForwardScanning': 12, 'Mode1_BackwardScanning': 13, 'Mode1_BreathOn': 14, 'Mode1_BreathOff': 15, 'Mode1_Spare1': 16, 'Mode1_Spare2': 17}
        compute_method = None
        length = 5
        startbit = 13
        byte = 1
        mask = 0b00111110
        unmask = 0b11000001
        shift = 1

    class DwnLoadDynLitPrmLedReFogLampRi2ContTiPrm_1_CemBodyExpoSignalIPdu03:
        sig_name = "DwnLoadDynLitPrmLedReFogLampRi2ContTiPrm_1_CemBodyExpoSignalIPdu03"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]


class CemBodyExpoDevFr02:
    msg_name = "CemBodyExpoDevFr02"
    msg_id = 1431
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['CCM']

    class CEMdevelpsignalgroupcheckFunctiondevpsignalgroup1:
        sig_name = "CEMdevelpsignalgroupcheckFunctiondevpsignalgroup1"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CEMdevelpsignalgroupcheckFunctiondevpsignalgroup5:
        sig_name = "CEMdevelpsignalgroupcheckFunctiondevpsignalgroup5"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CEMdevelpsignalgroupcheckFunctiondevpsignalgroup4:
        sig_name = "CEMdevelpsignalgroupcheckFunctiondevpsignalgroup4"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CEMdevelpsignalgroupcheckFunctiondevpsignalgroup8:
        sig_name = "CEMdevelpsignalgroupcheckFunctiondevpsignalgroup8"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CEMdevelpsignalgroupcheckFunctiondevpsignalgroup2:
        sig_name = "CEMdevelpsignalgroupcheckFunctiondevpsignalgroup2"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CEMdevelpsignalgroupcheckFunctiondevpsignalgroup6:
        sig_name = "CEMdevelpsignalgroupcheckFunctiondevpsignalgroup6"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CEMdevelpsignalgroupcheckFunctiondevpsignalgroup7:
        sig_name = "CEMdevelpsignalgroupcheckFunctiondevpsignalgroup7"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CEMdevelpsignalgroupcheckFunctiondevpsignalgroup3:
        sig_name = "CEMdevelpsignalgroupcheckFunctiondevpsignalgroup3"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 23
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class CemBodyExpoCommonFr08:
    msg_name = "CemBodyExpoCommonFr08"
    msg_id = 128
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR', 'HCML']

    class BrkPedlSnsrCntr_1_CemBodyExpoCommonSignalIPdu08:
        sig_name = "BrkPedlSnsrCntr_1_CemBodyExpoCommonSignalIPdu08"
        sig_start_bit = 35
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 35
        byte = 4
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class AccrPedlRatCntr_2_CemBodyExpoCommonSignalIPdu08:
        sig_name = "AccrPedlRatCntr_2_CemBodyExpoCommonSignalIPdu08"
        sig_start_bit = 31
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 31
        byte = 3
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class AmbTRawQly_1_CemBodyExpoCommonSignalIPdu08:
        sig_name = "AmbTRawQly_1_CemBodyExpoCommonSignalIPdu08"
        sig_start_bit = 52
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 52
        byte = 6
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class BrkPedlSnsrSt_1_CemBodyExpoCommonSignalIPdu08:
        sig_name = "BrkPedlSnsrSt_1_CemBodyExpoCommonSignalIPdu08"
        sig_start_bit = 37
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PsdNotPsd2_NoInfo1': 0, 'PsdNotPsd2_NotPsd': 1, 'PsdNotPsd2_Psd': 2, 'PsdNotPsd2_NoInfo2': 3}
        compute_method = None
        length = 2
        startbit = 37
        byte = 4
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class TooManyCars_1_CemBodyExpoCommonSignalIPdu08:
        sig_name = "TooManyCars_1_CemBodyExpoCommonSignalIPdu08"
        sig_start_bit = 54
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 54
        byte = 6
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class AccrPedlRatAccrPedlRat_2_CemBodyExpoCommonSignalIPdu08:
        sig_name = "AccrPedlRatAccrPedlRat_2_CemBodyExpoCommonSignalIPdu08"
        sig_start_bit = 6
        sig_length = 15
        sig_value_factor = 0.00390625
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 25600
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 6
        bmuws_info = [(0, 0b01111111, 0b10000000, 7, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class AmbTRawAmbTVal_1_CemBodyExpoCommonSignalIPdu08:
        sig_name = "AmbTRawAmbTVal_1_CemBodyExpoCommonSignalIPdu08"
        sig_start_bit = 50
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = "-70.0"
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 700
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 50
        bmuws_info = [(6, 0b00000111, 0b11111000, 3, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class AccrPedlRatChks_2_CemBodyExpoCommonSignalIPdu08:
        sig_name = "AccrPedlRatChks_2_CemBodyExpoCommonSignalIPdu08"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 23
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BrkPedlSnsrQf_1_CemBodyExpoCommonSignalIPdu08:
        sig_name = "BrkPedlSnsrQf_1_CemBodyExpoCommonSignalIPdu08"
        sig_start_bit = 39
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 39
        byte = 4
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class BrkPedlSnsrChks_1_CemBodyExpoCommonSignalIPdu08:
        sig_name = "BrkPedlSnsrChks_1_CemBodyExpoCommonSignalIPdu08"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class HcmrToBgmBodyExpoDiagRespFrame:
    msg_name = "HcmrToBgmBodyExpoDiagRespFrame"
    msg_id = 1716
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "HCMR"
    rx_nodes = ['BGM']


class CemBodyExpoFr08:
    msg_name = "CemBodyExpoFr08"
    msg_id = 294
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RCMM']

    class DwnLoadDynLitPrmForLedMkrLampLe2Tistamp_1_CemBodyExpoSignalIPdu08:
        sig_name = "DwnLoadDynLitPrmForLedMkrLampLe2Tistamp_1_CemBodyExpoSignalIPdu08"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmForLedMkrLampLe2OffsTiPrm_1_CemBodyExpoSignalIPdu08:
        sig_name = "DwnLoadDynLitPrmForLedMkrLampLe2OffsTiPrm_1_CemBodyExpoSignalIPdu08"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmForLedMkrLampLe2UpprBriPrm_1_CemBodyExpoSignalIPdu08:
        sig_name = "DwnLoadDynLitPrmForLedMkrLampLe2UpprBriPrm_1_CemBodyExpoSignalIPdu08"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmForLedMkrLampLe2LowBriPrm_1_CemBodyExpoSignalIPdu08:
        sig_name = "DwnLoadDynLitPrmForLedMkrLampLe2LowBriPrm_1_CemBodyExpoSignalIPdu08"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmForLedMkrLampLe2ModePrm_1_CemBodyExpoSignalIPdu08:
        sig_name = "DwnLoadDynLitPrmForLedMkrLampLe2ModePrm_1_CemBodyExpoSignalIPdu08"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode1_Off': 0, 'Mode1_On': 1, 'Mode1_GradualOn': 2, 'Mode1_GradualOff': 3, 'Mode1_ForwardWipingOn': 4, 'Mode1_BackwardWipingOn': 5, 'Mode1_OutwardWipingOn': 6, 'Mode1_InwardWipingOn': 7, 'Mode1_ForwardWipingOff': 8, 'Mode1_BackwardWipingOff': 9, 'Mode1_OutwardWipingOff': 10, 'Mode1_InwardWipingOff': 11, 'Mode1_ForwardScanning': 12, 'Mode1_BackwardScanning': 13, 'Mode1_BreathOn': 14, 'Mode1_BreathOff': 15, 'Mode1_Spare1': 16, 'Mode1_Spare2': 17}
        compute_method = None
        length = 5
        startbit = 13
        byte = 1
        mask = 0b00111110
        unmask = 0b11000001
        shift = 1

    class DwnLoadDynLitPrmForLedMkrLampLe2ContTiPrm_1_CemBodyExpoSignalIPdu08:
        sig_name = "DwnLoadDynLitPrmForLedMkrLampLe2ContTiPrm_1_CemBodyExpoSignalIPdu08"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]


class CemBodyExpoFr94:
    msg_name = "CemBodyExpoFr94"
    msg_id = 828
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR']

    class DwnLoadDynLtgPrmForFrntRIGrp4Timestamp_1_CemBodyExpoSignalIPdu94:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp4Timestamp_1_CemBodyExpoSignalIPdu94"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DwnLoadDynLtgPrmForFrntRIGrp4ContinueTime_1_CemBodyExpoSignalIPdu94:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp4ContinueTime_1_CemBodyExpoSignalIPdu94"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForFrntRIGrp4Mode1_1_CemBodyExpoSignalIPdu94:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp4Mode1_1_CemBodyExpoSignalIPdu94"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode4_Off': 0, 'Mode4_On': 1, 'Mode4_GradualOn': 2, 'Mode4_GradualOff': 3, 'Mode4_ForwardWipingOn': 4, 'Mode4_BackwardWipingOn': 5, 'Mode4_OutwardWipingOn': 6, 'Mode4_InwardWipingOn': 7, 'Mode4_ForwardWipingOff': 8, 'Mode4_BackwardWipingOff': 9, 'Mode4_OutwardWipingOff': 10, 'Mode4_InwardWipingOff': 11, 'Mode4_ForwardScanning': 12, 'Mode4_BackwardScanning': 13, 'Mode4_BreathOn': 14, 'Mode4_BreathOff': 15, 'Mode4_1stHalfONand2ndHalfOFF': 16, 'Mode4_HalfOFFHalfON': 17, 'Mode4_HalfDimmingONHalfOFF': 18, 'Mode4_HalfDimmingONHalfON': 19, 'Mode4_HalfOFFHalfDimmingON': 20, 'Mode4_HalfONHalfDimmingON': 21, 'Mode4_HalfDimmingOFFHalfOFF': 22, 'Mode4_HalfDimmingOFFHalfON': 23, 'Mode4_HalfOFFHalfDimmingOFF': 24, 'Mode4_HalfONHalfDimmingOFF': 25, 'Mode4_SingleOn1': 26, 'Mode4_SingleOn2': 27, 'Mode4_SingleOn3': 28, 'Mode4_SingleOn4': 29, 'Mode4_SingleOn5': 30, 'Mode4_SingleOn6': 31, 'Mode4_SingleOn7': 32, 'Mode4_SingleOn8': 33, 'Mode4_SingleOn9': 34, 'Mode4_SingleOn10': 35, 'Mode4_SingleOn11': 36, 'Mode4_SingleOn12': 37, 'Mode4_SingleOff1': 38, 'Mode4_SingleOff2': 39, 'Mode4_SingleOff3': 40, 'Mode4_SingleOff4': 41, 'Mode4_SingleOff5': 42, 'Mode4_SingleOff6': 43, 'Mode4_SingleOff7': 44, 'Mode4_SingleOff8': 45, 'Mode4_SingleOff9': 46, 'Mode4_SingleOff10': 47, 'Mode4_SingleOff11': 48, 'Mode4_SingleOff12': 49}
        compute_method = None
        length = 6
        startbit = 23
        byte = 2
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntRIGrp4OffsetTime_1_CemBodyExpoSignalIPdu94:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp4OffsetTime_1_CemBodyExpoSignalIPdu94"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 31
        byte = 3
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntRIGrp4LowBrightness_1_CemBodyExpoSignalIPdu94:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp4LowBrightness_1_CemBodyExpoSignalIPdu94"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DwnLoadDynLtgPrmForFrntRIGrp4HighBrightness_1_CemBodyExpoSignalIPdu94:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp4HighBrightness_1_CemBodyExpoSignalIPdu94"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4


class CemBodyExpoFr105:
    msg_name = "CemBodyExpoFr105"
    msg_id = 839
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR']

    class DwnLoadDynLtgPrmForFrntRIGrp15LowBrightness_1_CemBodyExpoSignalIPdu105:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp15LowBrightness_1_CemBodyExpoSignalIPdu105"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DwnLoadDynLtgPrmForFrntRIGrp15ContinueTime_1_CemBodyExpoSignalIPdu105:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp15ContinueTime_1_CemBodyExpoSignalIPdu105"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForFrntRIGrp15OffsetTime_1_CemBodyExpoSignalIPdu105:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp15OffsetTime_1_CemBodyExpoSignalIPdu105"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 31
        byte = 3
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntRIGrp15Timestamp_1_CemBodyExpoSignalIPdu105:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp15Timestamp_1_CemBodyExpoSignalIPdu105"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DwnLoadDynLtgPrmForFrntRIGrp15Mode1_1_CemBodyExpoSignalIPdu105:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp15Mode1_1_CemBodyExpoSignalIPdu105"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode4_Off': 0, 'Mode4_On': 1, 'Mode4_GradualOn': 2, 'Mode4_GradualOff': 3, 'Mode4_ForwardWipingOn': 4, 'Mode4_BackwardWipingOn': 5, 'Mode4_OutwardWipingOn': 6, 'Mode4_InwardWipingOn': 7, 'Mode4_ForwardWipingOff': 8, 'Mode4_BackwardWipingOff': 9, 'Mode4_OutwardWipingOff': 10, 'Mode4_InwardWipingOff': 11, 'Mode4_ForwardScanning': 12, 'Mode4_BackwardScanning': 13, 'Mode4_BreathOn': 14, 'Mode4_BreathOff': 15, 'Mode4_1stHalfONand2ndHalfOFF': 16, 'Mode4_HalfOFFHalfON': 17, 'Mode4_HalfDimmingONHalfOFF': 18, 'Mode4_HalfDimmingONHalfON': 19, 'Mode4_HalfOFFHalfDimmingON': 20, 'Mode4_HalfONHalfDimmingON': 21, 'Mode4_HalfDimmingOFFHalfOFF': 22, 'Mode4_HalfDimmingOFFHalfON': 23, 'Mode4_HalfOFFHalfDimmingOFF': 24, 'Mode4_HalfONHalfDimmingOFF': 25, 'Mode4_SingleOn1': 26, 'Mode4_SingleOn2': 27, 'Mode4_SingleOn3': 28, 'Mode4_SingleOn4': 29, 'Mode4_SingleOn5': 30, 'Mode4_SingleOn6': 31, 'Mode4_SingleOn7': 32, 'Mode4_SingleOn8': 33, 'Mode4_SingleOn9': 34, 'Mode4_SingleOn10': 35, 'Mode4_SingleOn11': 36, 'Mode4_SingleOn12': 37, 'Mode4_SingleOff1': 38, 'Mode4_SingleOff2': 39, 'Mode4_SingleOff3': 40, 'Mode4_SingleOff4': 41, 'Mode4_SingleOff5': 42, 'Mode4_SingleOff6': 43, 'Mode4_SingleOff7': 44, 'Mode4_SingleOff8': 45, 'Mode4_SingleOff9': 46, 'Mode4_SingleOff10': 47, 'Mode4_SingleOff11': 48, 'Mode4_SingleOff12': 49}
        compute_method = None
        length = 6
        startbit = 23
        byte = 2
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntRIGrp15HighBrightness_1_CemBodyExpoSignalIPdu105:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp15HighBrightness_1_CemBodyExpoSignalIPdu105"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4


class EtcToCemBodyExpoDevDiagFr03:
    msg_name = "EtcToCemBodyExpoDevDiagFr03"
    msg_id = 1425
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CCM"
    rx_nodes = ['BGM']

    class CEMdevelpsignalgroupreqFunctiondevpsignalgroup4:
        sig_name = "CEMdevelpsignalgroupreqFunctiondevpsignalgroup4"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CEMdevelpsignalgroupreqFunctiondevpsignalgroup2:
        sig_name = "CEMdevelpsignalgroupreqFunctiondevpsignalgroup2"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CEMdevelpsignalgroupreqFunctiondevpsignalgroup8:
        sig_name = "CEMdevelpsignalgroupreqFunctiondevpsignalgroup8"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CEMdevelpsignalgroupreqFunctiondevpsignalgroup1:
        sig_name = "CEMdevelpsignalgroupreqFunctiondevpsignalgroup1"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CEMdevelpsignalgroupreqFunctiondevpsignalgroup5:
        sig_name = "CEMdevelpsignalgroupreqFunctiondevpsignalgroup5"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CEMdevelpsignalgroupreqFunctiondevpsignalgroup3:
        sig_name = "CEMdevelpsignalgroupreqFunctiondevpsignalgroup3"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 23
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CEMdevelpsignalgroupreqFunctiondevpsignalgroup7:
        sig_name = "CEMdevelpsignalgroupreqFunctiondevpsignalgroup7"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CEMdevelpsignalgroupreqFunctiondevpsignalgroup6:
        sig_name = "CEMdevelpsignalgroupreqFunctiondevpsignalgroup6"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class CemBodyExpoFr56:
    msg_name = "CemBodyExpoFr56"
    msg_id = 330
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RCMR']

    class DwnLoadDynLitPrmLedRePosnLampRi3ContTiPrm_1_CemBodyExpoSignalIPdu56:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi3ContTiPrm_1_CemBodyExpoSignalIPdu56"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedRePosnLampRi3OffsTiPrm_1_CemBodyExpoSignalIPdu56:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi3OffsTiPrm_1_CemBodyExpoSignalIPdu56"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedRePosnLampRi3Tistamp_1_CemBodyExpoSignalIPdu56:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi3Tistamp_1_CemBodyExpoSignalIPdu56"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmLedRePosnLampRi3UpprBriPrm_1_CemBodyExpoSignalIPdu56:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi3UpprBriPrm_1_CemBodyExpoSignalIPdu56"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmLedRePosnLampRi3LowBriPrm_1_CemBodyExpoSignalIPdu56:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi3LowBriPrm_1_CemBodyExpoSignalIPdu56"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmLedRePosnLampRi3ModePrm_1_CemBodyExpoSignalIPdu56:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi3ModePrm_1_CemBodyExpoSignalIPdu56"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode1_Off': 0, 'Mode1_On': 1, 'Mode1_GradualOn': 2, 'Mode1_GradualOff': 3, 'Mode1_ForwardWipingOn': 4, 'Mode1_BackwardWipingOn': 5, 'Mode1_OutwardWipingOn': 6, 'Mode1_InwardWipingOn': 7, 'Mode1_ForwardWipingOff': 8, 'Mode1_BackwardWipingOff': 9, 'Mode1_OutwardWipingOff': 10, 'Mode1_InwardWipingOff': 11, 'Mode1_ForwardScanning': 12, 'Mode1_BackwardScanning': 13, 'Mode1_BreathOn': 14, 'Mode1_BreathOff': 15, 'Mode1_Spare1': 16, 'Mode1_Spare2': 17}
        compute_method = None
        length = 5
        startbit = 13
        byte = 1
        mask = 0b00111110
        unmask = 0b11000001
        shift = 1


class CemBodyExpoFr61:
    msg_name = "CemBodyExpoFr61"
    msg_id = 334
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR']

    class DwnLoadDynLitPrmLedRiGrilleLampOffsTiPrm_1_CemBodyExpoSignalIPdu61:
        sig_name = "DwnLoadDynLitPrmLedRiGrilleLampOffsTiPrm_1_CemBodyExpoSignalIPdu61"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedRiGrilleLampUpprBriPrm_1_CemBodyExpoSignalIPdu61:
        sig_name = "DwnLoadDynLitPrmLedRiGrilleLampUpprBriPrm_1_CemBodyExpoSignalIPdu61"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmLedRiGrilleLampTistamp_1_CemBodyExpoSignalIPdu61:
        sig_name = "DwnLoadDynLitPrmLedRiGrilleLampTistamp_1_CemBodyExpoSignalIPdu61"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmLedRiGrilleLampModePrm_1_CemBodyExpoSignalIPdu61:
        sig_name = "DwnLoadDynLitPrmLedRiGrilleLampModePrm_1_CemBodyExpoSignalIPdu61"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode1_Off': 0, 'Mode1_On': 1, 'Mode1_GradualOn': 2, 'Mode1_GradualOff': 3, 'Mode1_ForwardWipingOn': 4, 'Mode1_BackwardWipingOn': 5, 'Mode1_OutwardWipingOn': 6, 'Mode1_InwardWipingOn': 7, 'Mode1_ForwardWipingOff': 8, 'Mode1_BackwardWipingOff': 9, 'Mode1_OutwardWipingOff': 10, 'Mode1_InwardWipingOff': 11, 'Mode1_ForwardScanning': 12, 'Mode1_BackwardScanning': 13, 'Mode1_BreathOn': 14, 'Mode1_BreathOff': 15, 'Mode1_Spare1': 16, 'Mode1_Spare2': 17}
        compute_method = None
        length = 5
        startbit = 13
        byte = 1
        mask = 0b00111110
        unmask = 0b11000001
        shift = 1

    class DwnLoadDynLitPrmLedRiGrilleLampLowBriPrm_1_CemBodyExpoSignalIPdu61:
        sig_name = "DwnLoadDynLitPrmLedRiGrilleLampLowBriPrm_1_CemBodyExpoSignalIPdu61"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmLedRiGrilleLampContTiPrm_1_CemBodyExpoSignalIPdu61:
        sig_name = "DwnLoadDynLitPrmLedRiGrilleLampContTiPrm_1_CemBodyExpoSignalIPdu61"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]


class EtctoHcmrXCPFr01:
    msg_name = "EtctoHcmrXCPFr01"
    msg_id = 1428
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CCM"
    rx_nodes = ['HCMR']


class CemBodyExpoFr109:
    msg_name = "CemBodyExpoFr109"
    msg_id = 843
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR']

    class DwnLoadDynLtgPrmForFrntRIGrp19OffsetTime_1_CemBodyExpoSignalIPdu109:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp19OffsetTime_1_CemBodyExpoSignalIPdu109"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 31
        byte = 3
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntRIGrp19Mode1_1_CemBodyExpoSignalIPdu109:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp19Mode1_1_CemBodyExpoSignalIPdu109"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode4_Off': 0, 'Mode4_On': 1, 'Mode4_GradualOn': 2, 'Mode4_GradualOff': 3, 'Mode4_ForwardWipingOn': 4, 'Mode4_BackwardWipingOn': 5, 'Mode4_OutwardWipingOn': 6, 'Mode4_InwardWipingOn': 7, 'Mode4_ForwardWipingOff': 8, 'Mode4_BackwardWipingOff': 9, 'Mode4_OutwardWipingOff': 10, 'Mode4_InwardWipingOff': 11, 'Mode4_ForwardScanning': 12, 'Mode4_BackwardScanning': 13, 'Mode4_BreathOn': 14, 'Mode4_BreathOff': 15, 'Mode4_1stHalfONand2ndHalfOFF': 16, 'Mode4_HalfOFFHalfON': 17, 'Mode4_HalfDimmingONHalfOFF': 18, 'Mode4_HalfDimmingONHalfON': 19, 'Mode4_HalfOFFHalfDimmingON': 20, 'Mode4_HalfONHalfDimmingON': 21, 'Mode4_HalfDimmingOFFHalfOFF': 22, 'Mode4_HalfDimmingOFFHalfON': 23, 'Mode4_HalfOFFHalfDimmingOFF': 24, 'Mode4_HalfONHalfDimmingOFF': 25, 'Mode4_SingleOn1': 26, 'Mode4_SingleOn2': 27, 'Mode4_SingleOn3': 28, 'Mode4_SingleOn4': 29, 'Mode4_SingleOn5': 30, 'Mode4_SingleOn6': 31, 'Mode4_SingleOn7': 32, 'Mode4_SingleOn8': 33, 'Mode4_SingleOn9': 34, 'Mode4_SingleOn10': 35, 'Mode4_SingleOn11': 36, 'Mode4_SingleOn12': 37, 'Mode4_SingleOff1': 38, 'Mode4_SingleOff2': 39, 'Mode4_SingleOff3': 40, 'Mode4_SingleOff4': 41, 'Mode4_SingleOff5': 42, 'Mode4_SingleOff6': 43, 'Mode4_SingleOff7': 44, 'Mode4_SingleOff8': 45, 'Mode4_SingleOff9': 46, 'Mode4_SingleOff10': 47, 'Mode4_SingleOff11': 48, 'Mode4_SingleOff12': 49}
        compute_method = None
        length = 6
        startbit = 23
        byte = 2
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntRIGrp19LowBrightness_1_CemBodyExpoSignalIPdu109:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp19LowBrightness_1_CemBodyExpoSignalIPdu109"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DwnLoadDynLtgPrmForFrntRIGrp19HighBrightness_1_CemBodyExpoSignalIPdu109:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp19HighBrightness_1_CemBodyExpoSignalIPdu109"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DwnLoadDynLtgPrmForFrntRIGrp19ContinueTime_1_CemBodyExpoSignalIPdu109:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp19ContinueTime_1_CemBodyExpoSignalIPdu109"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForFrntRIGrp19Timestamp_1_CemBodyExpoSignalIPdu109:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp19Timestamp_1_CemBodyExpoSignalIPdu109"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5


class CemBodyExpoCommonFr04:
    msg_name = "CemBodyExpoCommonFr04"
    msg_id = 80
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.04
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR', 'RCMR', 'HCML', 'RCMM', 'RCML']

    class VehSpdLgtCntr_2_CEMBodyExpoCommonSignalIPdu04:
        sig_name = "VehSpdLgtCntr_2_CEMBodyExpoCommonSignalIPdu04"
        sig_start_bit = 31
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 31
        byte = 3
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class VehSpdLgtA_2_CEMBodyExpoCommonSignalIPdu04:
        sig_name = "VehSpdLgtA_2_CEMBodyExpoCommonSignalIPdu04"
        sig_start_bit = 6
        sig_length = 15
        sig_value_factor = 0.00391
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 31970
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 6
        bmuws_info = [(0, 0b01111111, 0b10000000, 7, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class VehSpdLgtChks_2_CEMBodyExpoCommonSignalIPdu04:
        sig_name = "VehSpdLgtChks_2_CEMBodyExpoCommonSignalIPdu04"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 23
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehSpdLgtQf_2_CEMBodyExpoCommonSignalIPdu04:
        sig_name = "VehSpdLgtQf_2_CEMBodyExpoCommonSignalIPdu04"
        sig_start_bit = 27
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 27
        byte = 3
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2


class BgmToHcmlBodyExpoDiagReqFrame:
    msg_name = "BgmToHcmlBodyExpoDiagReqFrame"
    msg_id = 1971
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCML']


class CemBodyExpoCommonFr20:
    msg_name = "CemBodyExpoCommonFr20"
    msg_id = 399
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.045
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR', 'HCML']

    class VehObjforADB8AdbObjHozlAgSpdRi_1_CemBodyExpoCommonSignalIPdu20:
        sig_name = "VehObjforADB8AdbObjHozlAgSpdRi_1_CemBodyExpoCommonSignalIPdu20"
        sig_start_bit = 41
        sig_length = 9
        sig_value_factor = 0.2
        sig_value_offset = "-50"
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 250
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 41
        bmuws_info = [(5, 0b00000011, 0b11111100, 2, 0), (6, 0b11111110, 0b00000001, 7, 1)]

    class VehObjforADB8AdbTrkInfo_1_CemBodyExpoCommonSignalIPdu20:
        sig_name = "VehObjforADB8AdbTrkInfo_1_CemBodyExpoCommonSignalIPdu20"
        sig_start_bit = 48
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NotTracked': 0, 'Tracking': 1}
        compute_method = None
        length = 1
        startbit = 48
        byte = 6
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VehObjforADB8AdbVertAg_1_CemBodyExpoCommonSignalIPdu20:
        sig_name = "VehObjforADB8AdbVertAg_1_CemBodyExpoCommonSignalIPdu20"
        sig_start_bit = 63
        sig_length = 5
        sig_value_factor = 0.5
        sig_value_offset = "-3"
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Motorola"
        sig_value_init = 6
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 63
        byte = 7
        mask = 0b11111000
        unmask = 0b00000111
        shift = 3

    class VehObjforADB8AdbHozlAgRi_1_CemBodyExpoCommonSignalIPdu20:
        sig_name = "VehObjforADB8AdbHozlAgRi_1_CemBodyExpoCommonSignalIPdu20"
        sig_start_bit = 31
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = "-40"
        sig_value_min = 0
        sig_value_max = 1600
        sig_byteorder = "Motorola"
        sig_value_init = 800
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11100000, 0b00011111, 3, 5)]

    class VehObjforADB8AdbObjDir_1_CemBodyExpoCommonSignalIPdu20:
        sig_name = "VehObjforADB8AdbObjDir_1_CemBodyExpoCommonSignalIPdu20"
        sig_start_bit = 36
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AdbObjDir_Idle': 0, 'AdbObjDir_Oncoming': 1, 'AdbObjDir_Preceding': 2, 'AdbObjDir_Others': 3}
        compute_method = None
        length = 2
        startbit = 36
        byte = 4
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class VehObjforADB8AdbObjHozlAgSpdLe_1_CemBodyExpoCommonSignalIPdu20:
        sig_name = "VehObjforADB8AdbObjHozlAgSpdLe_1_CemBodyExpoCommonSignalIPdu20"
        sig_start_bit = 34
        sig_length = 9
        sig_value_factor = 0.2
        sig_value_offset = "-50"
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 250
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 34
        bmuws_info = [(4, 0b00000111, 0b11111000, 3, 0), (5, 0b11111100, 0b00000011, 6, 2)]

    class VehObjforADB8AdbClassn_1_CemBodyExpoCommonSignalIPdu20:
        sig_name = "VehObjforADB8AdbClassn_1_CemBodyExpoCommonSignalIPdu20"
        sig_start_bit = 13
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AdbClassn_NoVehicle': 0, 'AdbClassn_Car': 1, 'AdbClassn_Truck': 2, 'AdbClassn_Bus': 3, 'AdbClassn_BikeOrMotorBike': 4, 'AdbClassn_Pedestrain': 5, 'AdbClassn_Mixed': 6, 'AdbClassn_Unknown': 7}
        compute_method = None
        length = 3
        startbit = 13
        byte = 1
        mask = 0b00111000
        unmask = 0b11000111
        shift = 3

    class VehObjforADB8AdbHozlAgLe_1_CemBodyExpoCommonSignalIPdu20:
        sig_name = "VehObjforADB8AdbHozlAgLe_1_CemBodyExpoCommonSignalIPdu20"
        sig_start_bit = 10
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = "-40"
        sig_value_min = 0
        sig_value_max = 1600
        sig_byteorder = "Motorola"
        sig_value_init = 800
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 10
        bmuws_info = [(1, 0b00000111, 0b11111000, 3, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class VehObjforADB8AdbAbsDist_1_CemBodyExpoCommonSignalIPdu20:
        sig_name = "VehObjforADB8AdbAbsDist_1_CemBodyExpoCommonSignalIPdu20"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]


class CemBodyExpoFr75:
    msg_name = "CemBodyExpoFr75"
    msg_id = 809
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCML']

    class DwnLoadDynLtgPrmForFrntLeGrp9Timestamp_1_CemBodyExpoSignalIPdu75:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp9Timestamp_1_CemBodyExpoSignalIPdu75"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DwnLoadDynLtgPrmForFrntLeGrp9ContinueTime_1_CemBodyExpoSignalIPdu75:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp9ContinueTime_1_CemBodyExpoSignalIPdu75"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForFrntLeGrp9LowBrightness_1_CemBodyExpoSignalIPdu75:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp9LowBrightness_1_CemBodyExpoSignalIPdu75"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DwnLoadDynLtgPrmForFrntLeGrp9OffsetTime_1_CemBodyExpoSignalIPdu75:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp9OffsetTime_1_CemBodyExpoSignalIPdu75"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 31
        byte = 3
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntLeGrp9Mode1_1_CemBodyExpoSignalIPdu75:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp9Mode1_1_CemBodyExpoSignalIPdu75"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode4_Off': 0, 'Mode4_On': 1, 'Mode4_GradualOn': 2, 'Mode4_GradualOff': 3, 'Mode4_ForwardWipingOn': 4, 'Mode4_BackwardWipingOn': 5, 'Mode4_OutwardWipingOn': 6, 'Mode4_InwardWipingOn': 7, 'Mode4_ForwardWipingOff': 8, 'Mode4_BackwardWipingOff': 9, 'Mode4_OutwardWipingOff': 10, 'Mode4_InwardWipingOff': 11, 'Mode4_ForwardScanning': 12, 'Mode4_BackwardScanning': 13, 'Mode4_BreathOn': 14, 'Mode4_BreathOff': 15, 'Mode4_1stHalfONand2ndHalfOFF': 16, 'Mode4_HalfOFFHalfON': 17, 'Mode4_HalfDimmingONHalfOFF': 18, 'Mode4_HalfDimmingONHalfON': 19, 'Mode4_HalfOFFHalfDimmingON': 20, 'Mode4_HalfONHalfDimmingON': 21, 'Mode4_HalfDimmingOFFHalfOFF': 22, 'Mode4_HalfDimmingOFFHalfON': 23, 'Mode4_HalfOFFHalfDimmingOFF': 24, 'Mode4_HalfONHalfDimmingOFF': 25, 'Mode4_SingleOn1': 26, 'Mode4_SingleOn2': 27, 'Mode4_SingleOn3': 28, 'Mode4_SingleOn4': 29, 'Mode4_SingleOn5': 30, 'Mode4_SingleOn6': 31, 'Mode4_SingleOn7': 32, 'Mode4_SingleOn8': 33, 'Mode4_SingleOn9': 34, 'Mode4_SingleOn10': 35, 'Mode4_SingleOn11': 36, 'Mode4_SingleOn12': 37, 'Mode4_SingleOff1': 38, 'Mode4_SingleOff2': 39, 'Mode4_SingleOff3': 40, 'Mode4_SingleOff4': 41, 'Mode4_SingleOff5': 42, 'Mode4_SingleOff6': 43, 'Mode4_SingleOff7': 44, 'Mode4_SingleOff8': 45, 'Mode4_SingleOff9': 46, 'Mode4_SingleOff10': 47, 'Mode4_SingleOff11': 48, 'Mode4_SingleOff12': 49}
        compute_method = None
        length = 6
        startbit = 23
        byte = 2
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntLeGrp9HighBrightness_1_CemBodyExpoSignalIPdu75:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp9HighBrightness_1_CemBodyExpoSignalIPdu75"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4


class RcmmToBgmBodyExpoDiagRespFrame:
    msg_name = "RcmmToBgmBodyExpoDiagRespFrame"
    msg_id = 1719
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "RCMM"
    rx_nodes = ['BGM']


class CemBodyExpoFr108:
    msg_name = "CemBodyExpoFr108"
    msg_id = 842
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR']

    class DwnLoadDynLtgPrmForFrntRIGrp18OffsetTime_1_CemBodyExpoSignalIPdu108:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp18OffsetTime_1_CemBodyExpoSignalIPdu108"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 31
        byte = 3
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntRIGrp18Mode1_1_CemBodyExpoSignalIPdu108:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp18Mode1_1_CemBodyExpoSignalIPdu108"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode4_Off': 0, 'Mode4_On': 1, 'Mode4_GradualOn': 2, 'Mode4_GradualOff': 3, 'Mode4_ForwardWipingOn': 4, 'Mode4_BackwardWipingOn': 5, 'Mode4_OutwardWipingOn': 6, 'Mode4_InwardWipingOn': 7, 'Mode4_ForwardWipingOff': 8, 'Mode4_BackwardWipingOff': 9, 'Mode4_OutwardWipingOff': 10, 'Mode4_InwardWipingOff': 11, 'Mode4_ForwardScanning': 12, 'Mode4_BackwardScanning': 13, 'Mode4_BreathOn': 14, 'Mode4_BreathOff': 15, 'Mode4_1stHalfONand2ndHalfOFF': 16, 'Mode4_HalfOFFHalfON': 17, 'Mode4_HalfDimmingONHalfOFF': 18, 'Mode4_HalfDimmingONHalfON': 19, 'Mode4_HalfOFFHalfDimmingON': 20, 'Mode4_HalfONHalfDimmingON': 21, 'Mode4_HalfDimmingOFFHalfOFF': 22, 'Mode4_HalfDimmingOFFHalfON': 23, 'Mode4_HalfOFFHalfDimmingOFF': 24, 'Mode4_HalfONHalfDimmingOFF': 25, 'Mode4_SingleOn1': 26, 'Mode4_SingleOn2': 27, 'Mode4_SingleOn3': 28, 'Mode4_SingleOn4': 29, 'Mode4_SingleOn5': 30, 'Mode4_SingleOn6': 31, 'Mode4_SingleOn7': 32, 'Mode4_SingleOn8': 33, 'Mode4_SingleOn9': 34, 'Mode4_SingleOn10': 35, 'Mode4_SingleOn11': 36, 'Mode4_SingleOn12': 37, 'Mode4_SingleOff1': 38, 'Mode4_SingleOff2': 39, 'Mode4_SingleOff3': 40, 'Mode4_SingleOff4': 41, 'Mode4_SingleOff5': 42, 'Mode4_SingleOff6': 43, 'Mode4_SingleOff7': 44, 'Mode4_SingleOff8': 45, 'Mode4_SingleOff9': 46, 'Mode4_SingleOff10': 47, 'Mode4_SingleOff11': 48, 'Mode4_SingleOff12': 49}
        compute_method = None
        length = 6
        startbit = 23
        byte = 2
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntRIGrp18ContinueTime_1_CemBodyExpoSignalIPdu108:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp18ContinueTime_1_CemBodyExpoSignalIPdu108"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForFrntRIGrp18Timestamp_1_CemBodyExpoSignalIPdu108:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp18Timestamp_1_CemBodyExpoSignalIPdu108"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DwnLoadDynLtgPrmForFrntRIGrp18HighBrightness_1_CemBodyExpoSignalIPdu108:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp18HighBrightness_1_CemBodyExpoSignalIPdu108"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DwnLoadDynLtgPrmForFrntRIGrp18LowBrightness_1_CemBodyExpoSignalIPdu108:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp18LowBrightness_1_CemBodyExpoSignalIPdu108"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0


class CemBodyExpoFr85:
    msg_name = "CemBodyExpoFr85"
    msg_id = 819
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCML']

    class DwnLoadDynLtgPrmForFrntLeGrp19Timestamp_1_CemBodyExpoSignalIPdu85:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp19Timestamp_1_CemBodyExpoSignalIPdu85"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DwnLoadDynLtgPrmForFrntLeGrp19Mode1_1_CemBodyExpoSignalIPdu85:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp19Mode1_1_CemBodyExpoSignalIPdu85"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode4_Off': 0, 'Mode4_On': 1, 'Mode4_GradualOn': 2, 'Mode4_GradualOff': 3, 'Mode4_ForwardWipingOn': 4, 'Mode4_BackwardWipingOn': 5, 'Mode4_OutwardWipingOn': 6, 'Mode4_InwardWipingOn': 7, 'Mode4_ForwardWipingOff': 8, 'Mode4_BackwardWipingOff': 9, 'Mode4_OutwardWipingOff': 10, 'Mode4_InwardWipingOff': 11, 'Mode4_ForwardScanning': 12, 'Mode4_BackwardScanning': 13, 'Mode4_BreathOn': 14, 'Mode4_BreathOff': 15, 'Mode4_1stHalfONand2ndHalfOFF': 16, 'Mode4_HalfOFFHalfON': 17, 'Mode4_HalfDimmingONHalfOFF': 18, 'Mode4_HalfDimmingONHalfON': 19, 'Mode4_HalfOFFHalfDimmingON': 20, 'Mode4_HalfONHalfDimmingON': 21, 'Mode4_HalfDimmingOFFHalfOFF': 22, 'Mode4_HalfDimmingOFFHalfON': 23, 'Mode4_HalfOFFHalfDimmingOFF': 24, 'Mode4_HalfONHalfDimmingOFF': 25, 'Mode4_SingleOn1': 26, 'Mode4_SingleOn2': 27, 'Mode4_SingleOn3': 28, 'Mode4_SingleOn4': 29, 'Mode4_SingleOn5': 30, 'Mode4_SingleOn6': 31, 'Mode4_SingleOn7': 32, 'Mode4_SingleOn8': 33, 'Mode4_SingleOn9': 34, 'Mode4_SingleOn10': 35, 'Mode4_SingleOn11': 36, 'Mode4_SingleOn12': 37, 'Mode4_SingleOff1': 38, 'Mode4_SingleOff2': 39, 'Mode4_SingleOff3': 40, 'Mode4_SingleOff4': 41, 'Mode4_SingleOff5': 42, 'Mode4_SingleOff6': 43, 'Mode4_SingleOff7': 44, 'Mode4_SingleOff8': 45, 'Mode4_SingleOff9': 46, 'Mode4_SingleOff10': 47, 'Mode4_SingleOff11': 48, 'Mode4_SingleOff12': 49}
        compute_method = None
        length = 6
        startbit = 23
        byte = 2
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntLeGrp19OffsetTime_1_CemBodyExpoSignalIPdu85:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp19OffsetTime_1_CemBodyExpoSignalIPdu85"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 31
        byte = 3
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntLeGrp19ContinueTime_1_CemBodyExpoSignalIPdu85:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp19ContinueTime_1_CemBodyExpoSignalIPdu85"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForFrntLeGrp19LowBrightness_1_CemBodyExpoSignalIPdu85:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp19LowBrightness_1_CemBodyExpoSignalIPdu85"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DwnLoadDynLtgPrmForFrntLeGrp19HighBrightness_1_CemBodyExpoSignalIPdu85:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp19HighBrightness_1_CemBodyExpoSignalIPdu85"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4


class CemBodyExpoFr98:
    msg_name = "CemBodyExpoFr98"
    msg_id = 832
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR']

    class DwnLoadDynLtgPrmForFrntRIGrp8Mode1_1_CemBodyExpoSignalIPdu98:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp8Mode1_1_CemBodyExpoSignalIPdu98"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode4_Off': 0, 'Mode4_On': 1, 'Mode4_GradualOn': 2, 'Mode4_GradualOff': 3, 'Mode4_ForwardWipingOn': 4, 'Mode4_BackwardWipingOn': 5, 'Mode4_OutwardWipingOn': 6, 'Mode4_InwardWipingOn': 7, 'Mode4_ForwardWipingOff': 8, 'Mode4_BackwardWipingOff': 9, 'Mode4_OutwardWipingOff': 10, 'Mode4_InwardWipingOff': 11, 'Mode4_ForwardScanning': 12, 'Mode4_BackwardScanning': 13, 'Mode4_BreathOn': 14, 'Mode4_BreathOff': 15, 'Mode4_1stHalfONand2ndHalfOFF': 16, 'Mode4_HalfOFFHalfON': 17, 'Mode4_HalfDimmingONHalfOFF': 18, 'Mode4_HalfDimmingONHalfON': 19, 'Mode4_HalfOFFHalfDimmingON': 20, 'Mode4_HalfONHalfDimmingON': 21, 'Mode4_HalfDimmingOFFHalfOFF': 22, 'Mode4_HalfDimmingOFFHalfON': 23, 'Mode4_HalfOFFHalfDimmingOFF': 24, 'Mode4_HalfONHalfDimmingOFF': 25, 'Mode4_SingleOn1': 26, 'Mode4_SingleOn2': 27, 'Mode4_SingleOn3': 28, 'Mode4_SingleOn4': 29, 'Mode4_SingleOn5': 30, 'Mode4_SingleOn6': 31, 'Mode4_SingleOn7': 32, 'Mode4_SingleOn8': 33, 'Mode4_SingleOn9': 34, 'Mode4_SingleOn10': 35, 'Mode4_SingleOn11': 36, 'Mode4_SingleOn12': 37, 'Mode4_SingleOff1': 38, 'Mode4_SingleOff2': 39, 'Mode4_SingleOff3': 40, 'Mode4_SingleOff4': 41, 'Mode4_SingleOff5': 42, 'Mode4_SingleOff6': 43, 'Mode4_SingleOff7': 44, 'Mode4_SingleOff8': 45, 'Mode4_SingleOff9': 46, 'Mode4_SingleOff10': 47, 'Mode4_SingleOff11': 48, 'Mode4_SingleOff12': 49}
        compute_method = None
        length = 6
        startbit = 23
        byte = 2
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntRIGrp8OffsetTime_1_CemBodyExpoSignalIPdu98:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp8OffsetTime_1_CemBodyExpoSignalIPdu98"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 31
        byte = 3
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntRIGrp8LowBrightness_1_CemBodyExpoSignalIPdu98:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp8LowBrightness_1_CemBodyExpoSignalIPdu98"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DwnLoadDynLtgPrmForFrntRIGrp8ContinueTime_1_CemBodyExpoSignalIPdu98:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp8ContinueTime_1_CemBodyExpoSignalIPdu98"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForFrntRIGrp8Timestamp_1_CemBodyExpoSignalIPdu98:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp8Timestamp_1_CemBodyExpoSignalIPdu98"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DwnLoadDynLtgPrmForFrntRIGrp8HighBrightness_1_CemBodyExpoSignalIPdu98:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp8HighBrightness_1_CemBodyExpoSignalIPdu98"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4


class BgmToHcmrBodyExpoDiagReqFrame:
    msg_name = "BgmToHcmrBodyExpoDiagReqFrame"
    msg_id = 1972
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR']


class CemBodyExpoFr05:
    msg_name = "CemBodyExpoFr05"
    msg_id = 291
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RCMM']

    class DwnLoadDynLitPrmLedReTurnIndcrRi2Tistamp_1_CemBodyExpoSignalIPdu05:
        sig_name = "DwnLoadDynLitPrmLedReTurnIndcrRi2Tistamp_1_CemBodyExpoSignalIPdu05"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmLedReTurnIndcrRi2OffsTiPrm_1_CemBodyExpoSignalIPdu05:
        sig_name = "DwnLoadDynLitPrmLedReTurnIndcrRi2OffsTiPrm_1_CemBodyExpoSignalIPdu05"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedReTurnIndcrRi2ModePrm_1_CemBodyExpoSignalIPdu05:
        sig_name = "DwnLoadDynLitPrmLedReTurnIndcrRi2ModePrm_1_CemBodyExpoSignalIPdu05"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode1_Off': 0, 'Mode1_On': 1, 'Mode1_GradualOn': 2, 'Mode1_GradualOff': 3, 'Mode1_ForwardWipingOn': 4, 'Mode1_BackwardWipingOn': 5, 'Mode1_OutwardWipingOn': 6, 'Mode1_InwardWipingOn': 7, 'Mode1_ForwardWipingOff': 8, 'Mode1_BackwardWipingOff': 9, 'Mode1_OutwardWipingOff': 10, 'Mode1_InwardWipingOff': 11, 'Mode1_ForwardScanning': 12, 'Mode1_BackwardScanning': 13, 'Mode1_BreathOn': 14, 'Mode1_BreathOff': 15, 'Mode1_Spare1': 16, 'Mode1_Spare2': 17}
        compute_method = None
        length = 5
        startbit = 13
        byte = 1
        mask = 0b00111110
        unmask = 0b11000001
        shift = 1

    class DwnLoadDynLitPrmLedReTurnIndcrRi2ContTiPrm_1_CemBodyExpoSignalIPdu05:
        sig_name = "DwnLoadDynLitPrmLedReTurnIndcrRi2ContTiPrm_1_CemBodyExpoSignalIPdu05"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedReTurnIndcrRi2LowBriPrm_1_CemBodyExpoSignalIPdu05:
        sig_name = "DwnLoadDynLitPrmLedReTurnIndcrRi2LowBriPrm_1_CemBodyExpoSignalIPdu05"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmLedReTurnIndcrRi2UpprBriPrm_1_CemBodyExpoSignalIPdu05:
        sig_name = "DwnLoadDynLitPrmLedReTurnIndcrRi2UpprBriPrm_1_CemBodyExpoSignalIPdu05"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class CemBodyExpoFr88:
    msg_name = "CemBodyExpoFr88"
    msg_id = 822
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCML']

    class DwnLoadDynLtgPrmForFrntLeGrp22ContinueTime_1_CemBodyExpoSignalIPdu88:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp22ContinueTime_1_CemBodyExpoSignalIPdu88"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForFrntLeGrp22Mode1_1_CemBodyExpoSignalIPdu88:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp22Mode1_1_CemBodyExpoSignalIPdu88"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode4_Off': 0, 'Mode4_On': 1, 'Mode4_GradualOn': 2, 'Mode4_GradualOff': 3, 'Mode4_ForwardWipingOn': 4, 'Mode4_BackwardWipingOn': 5, 'Mode4_OutwardWipingOn': 6, 'Mode4_InwardWipingOn': 7, 'Mode4_ForwardWipingOff': 8, 'Mode4_BackwardWipingOff': 9, 'Mode4_OutwardWipingOff': 10, 'Mode4_InwardWipingOff': 11, 'Mode4_ForwardScanning': 12, 'Mode4_BackwardScanning': 13, 'Mode4_BreathOn': 14, 'Mode4_BreathOff': 15, 'Mode4_1stHalfONand2ndHalfOFF': 16, 'Mode4_HalfOFFHalfON': 17, 'Mode4_HalfDimmingONHalfOFF': 18, 'Mode4_HalfDimmingONHalfON': 19, 'Mode4_HalfOFFHalfDimmingON': 20, 'Mode4_HalfONHalfDimmingON': 21, 'Mode4_HalfDimmingOFFHalfOFF': 22, 'Mode4_HalfDimmingOFFHalfON': 23, 'Mode4_HalfOFFHalfDimmingOFF': 24, 'Mode4_HalfONHalfDimmingOFF': 25, 'Mode4_SingleOn1': 26, 'Mode4_SingleOn2': 27, 'Mode4_SingleOn3': 28, 'Mode4_SingleOn4': 29, 'Mode4_SingleOn5': 30, 'Mode4_SingleOn6': 31, 'Mode4_SingleOn7': 32, 'Mode4_SingleOn8': 33, 'Mode4_SingleOn9': 34, 'Mode4_SingleOn10': 35, 'Mode4_SingleOn11': 36, 'Mode4_SingleOn12': 37, 'Mode4_SingleOff1': 38, 'Mode4_SingleOff2': 39, 'Mode4_SingleOff3': 40, 'Mode4_SingleOff4': 41, 'Mode4_SingleOff5': 42, 'Mode4_SingleOff6': 43, 'Mode4_SingleOff7': 44, 'Mode4_SingleOff8': 45, 'Mode4_SingleOff9': 46, 'Mode4_SingleOff10': 47, 'Mode4_SingleOff11': 48, 'Mode4_SingleOff12': 49}
        compute_method = None
        length = 6
        startbit = 23
        byte = 2
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntLeGrp22OffsetTime_1_CemBodyExpoSignalIPdu88:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp22OffsetTime_1_CemBodyExpoSignalIPdu88"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 31
        byte = 3
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntLeGrp22Timestamp_1_CemBodyExpoSignalIPdu88:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp22Timestamp_1_CemBodyExpoSignalIPdu88"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DwnLoadDynLtgPrmForFrntLeGrp22LowBrightness_1_CemBodyExpoSignalIPdu88:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp22LowBrightness_1_CemBodyExpoSignalIPdu88"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DwnLoadDynLtgPrmForFrntLeGrp22HighBrightness_1_CemBodyExpoSignalIPdu88:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp22HighBrightness_1_CemBodyExpoSignalIPdu88"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4


class CemBodyExpoCommonFr09:
    msg_name = "CemBodyExpoCommonFr09"
    msg_id = 387
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR', 'RCMR', 'HCML', 'RCMM', 'PCM', 'RCML']

    class VehCfgPrmExtCCPBytePosn7_2_CemBodyExpoCommonSignalIPdu09:
        sig_name = "VehCfgPrmExtCCPBytePosn7_2_CemBodyExpoCommonSignalIPdu09"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgPrmExtCCPBytePosn6_2_CemBodyExpoCommonSignalIPdu09:
        sig_name = "VehCfgPrmExtCCPBytePosn6_2_CemBodyExpoCommonSignalIPdu09"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgPrmExtCCPBytePosn5_2_CemBodyExpoCommonSignalIPdu09:
        sig_name = "VehCfgPrmExtCCPBytePosn5_2_CemBodyExpoCommonSignalIPdu09"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgPrmExtBlkIDBytePosn1_2_CemBodyExpoCommonSignalIPdu09:
        sig_name = "VehCfgPrmExtBlkIDBytePosn1_2_CemBodyExpoCommonSignalIPdu09"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgPrmExtCCPBytePosn2_2_CemBodyExpoCommonSignalIPdu09:
        sig_name = "VehCfgPrmExtCCPBytePosn2_2_CemBodyExpoCommonSignalIPdu09"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgPrmExtCCPBytePosn8_2_CemBodyExpoCommonSignalIPdu09:
        sig_name = "VehCfgPrmExtCCPBytePosn8_2_CemBodyExpoCommonSignalIPdu09"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgPrmExtCCPBytePosn3_2_CemBodyExpoCommonSignalIPdu09:
        sig_name = "VehCfgPrmExtCCPBytePosn3_2_CemBodyExpoCommonSignalIPdu09"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 23
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgPrmExtCCPBytePosn4_2_CemBodyExpoCommonSignalIPdu09:
        sig_name = "VehCfgPrmExtCCPBytePosn4_2_CemBodyExpoCommonSignalIPdu09"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class CEMBodyExpoCommonFr06:
    msg_name = "CEMBodyExpoCommonFr06"
    msg_id = 512
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR', 'RCMR', 'HCML', 'RCMM', 'PCM', 'RCML']

    class VehBattUSysUQf_4_CEMBodyExpoCommonSignalIPdu06:
        sig_name = "VehBattUSysUQf_4_CEMBodyExpoCommonSignalIPdu06"
        sig_start_bit = 41
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 41
        byte = 5
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class ExtrLiRlyPwrDwn:
        sig_name = "ExtrLiRlyPwrDwn"
        sig_start_bit = 6
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class BkpOfDstTrvld_3_CEMBodyExpoCommonSignalIPdu06:
        sig_name = "BkpOfDstTrvld_3_CEMBodyExpoCommonSignalIPdu06"
        sig_start_bit = 23
        sig_length = 21
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 2000000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 21
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111000, 0b00000111, 5, 3)]

    class VehBattUSysU_4_CEMBodyExpoCommonSignalIPdu06:
        sig_name = "VehBattUSysU_4_CEMBodyExpoCommonSignalIPdu06"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class CemBodyExpoFr90:
    msg_name = "CemBodyExpoFr90"
    msg_id = 824
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCML']

    class DwnLoadDynLtgPrmForFrntLeGrp24HighBrightness_1_CemBodyExpoSignalIPdu90:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp24HighBrightness_1_CemBodyExpoSignalIPdu90"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DwnLoadDynLtgPrmForFrntLeGrp24LowBrightness_1_CemBodyExpoSignalIPdu90:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp24LowBrightness_1_CemBodyExpoSignalIPdu90"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DwnLoadDynLtgPrmForFrntLeGrp24Timestamp_1_CemBodyExpoSignalIPdu90:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp24Timestamp_1_CemBodyExpoSignalIPdu90"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DwnLoadDynLtgPrmForFrntLeGrp24OffsetTime_1_CemBodyExpoSignalIPdu90:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp24OffsetTime_1_CemBodyExpoSignalIPdu90"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 31
        byte = 3
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntLeGrp24Mode1_1_CemBodyExpoSignalIPdu90:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp24Mode1_1_CemBodyExpoSignalIPdu90"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode4_Off': 0, 'Mode4_On': 1, 'Mode4_GradualOn': 2, 'Mode4_GradualOff': 3, 'Mode4_ForwardWipingOn': 4, 'Mode4_BackwardWipingOn': 5, 'Mode4_OutwardWipingOn': 6, 'Mode4_InwardWipingOn': 7, 'Mode4_ForwardWipingOff': 8, 'Mode4_BackwardWipingOff': 9, 'Mode4_OutwardWipingOff': 10, 'Mode4_InwardWipingOff': 11, 'Mode4_ForwardScanning': 12, 'Mode4_BackwardScanning': 13, 'Mode4_BreathOn': 14, 'Mode4_BreathOff': 15, 'Mode4_1stHalfONand2ndHalfOFF': 16, 'Mode4_HalfOFFHalfON': 17, 'Mode4_HalfDimmingONHalfOFF': 18, 'Mode4_HalfDimmingONHalfON': 19, 'Mode4_HalfOFFHalfDimmingON': 20, 'Mode4_HalfONHalfDimmingON': 21, 'Mode4_HalfDimmingOFFHalfOFF': 22, 'Mode4_HalfDimmingOFFHalfON': 23, 'Mode4_HalfOFFHalfDimmingOFF': 24, 'Mode4_HalfONHalfDimmingOFF': 25, 'Mode4_SingleOn1': 26, 'Mode4_SingleOn2': 27, 'Mode4_SingleOn3': 28, 'Mode4_SingleOn4': 29, 'Mode4_SingleOn5': 30, 'Mode4_SingleOn6': 31, 'Mode4_SingleOn7': 32, 'Mode4_SingleOn8': 33, 'Mode4_SingleOn9': 34, 'Mode4_SingleOn10': 35, 'Mode4_SingleOn11': 36, 'Mode4_SingleOn12': 37, 'Mode4_SingleOff1': 38, 'Mode4_SingleOff2': 39, 'Mode4_SingleOff3': 40, 'Mode4_SingleOff4': 41, 'Mode4_SingleOff5': 42, 'Mode4_SingleOff6': 43, 'Mode4_SingleOff7': 44, 'Mode4_SingleOff8': 45, 'Mode4_SingleOff9': 46, 'Mode4_SingleOff10': 47, 'Mode4_SingleOff11': 48, 'Mode4_SingleOff12': 49}
        compute_method = None
        length = 6
        startbit = 23
        byte = 2
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntLeGrp24ContinueTime_1_CemBodyExpoSignalIPdu90:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp24ContinueTime_1_CemBodyExpoSignalIPdu90"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class HcmlBodyExpoFr04:
    msg_name = "HcmlBodyExpoFr04"
    msg_id = 124
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 8
    tx_node = "HCML"
    rx_nodes = ['BGM']

    class StsOfLvlgLeChks:
        sig_name = "StsOfLvlgLeChks"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HdlampLeInpSts1:
        sig_name = "HdlampLeInpSts1"
        sig_start_bit = 49
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 49
        byte = 6
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class StsOfLedDaytiRunngLampLe:
        sig_name = "StsOfLedDaytiRunngLampLe"
        sig_start_bit = 13
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 13
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class StsOfLedCornrgLampLe:
        sig_name = "StsOfLedCornrgLampLe"
        sig_start_bit = 11
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 11
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class StsOfAhbcLe:
        sig_name = "StsOfAhbcLe"
        sig_start_bit = 3
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 3
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class StsOfLedFrntTurnIndcrLe:
        sig_name = "StsOfLedFrntTurnIndcrLe"
        sig_start_bit = 19
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 19
        byte = 2
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class StsOfSwvlgLe:
        sig_name = "StsOfSwvlgLe"
        sig_start_bit = 7
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class StsOfAfsLe:
        sig_name = "StsOfAfsLe"
        sig_start_bit = 1
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class StsOfTouristModLe:
        sig_name = "StsOfTouristModLe"
        sig_start_bit = 25
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 25
        byte = 3
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class StsOfLvlgLeCntr:
        sig_name = "StsOfLvlgLeCntr"
        sig_start_bit = 55
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 55
        byte = 6
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class ExtrLiShowActvnFrntLeFb:
        sig_name = "ExtrLiShowActvnFrntLeFb"
        sig_start_bit = 28
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Sts_Resd': 0, 'Sts_Err': 1, 'Sts_CmplOk': 2, 'Sts_InProgs': 3}
        compute_method = None
        length = 2
        startbit = 28
        byte = 3
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class HdlampLeInpSts2:
        sig_name = "HdlampLeInpSts2"
        sig_start_bit = 63
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 63
        byte = 7
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class StsOfLvlgLeStsOfLvlgLe:
        sig_name = "StsOfLvlgLeStsOfLvlgLe"
        sig_start_bit = 51
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 51
        byte = 6
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class DwnLoadStsFbOfHdlampLe:
        sig_name = "DwnLoadStsFbOfHdlampLe"
        sig_start_bit = 5
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Sts_Resd': 0, 'Sts_Err': 1, 'Sts_CmplOk': 2, 'Sts_InProgs': 3}
        compute_method = None
        length = 2
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class StsOfWelGbyFrntLe:
        sig_name = "StsOfWelGbyFrntLe"
        sig_start_bit = 61
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 61
        byte = 7
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class StsOfLedFrntPosnLampLe:
        sig_name = "StsOfLedFrntPosnLampLe"
        sig_start_bit = 17
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 17
        byte = 2
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class StsOfFrntSideMkrLampLe2:
        sig_name = "StsOfFrntSideMkrLampLe2"
        sig_start_bit = 9
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 9
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class StsOfLedFrntFogLampLe:
        sig_name = "StsOfLedFrntFogLampLe"
        sig_start_bit = 15
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 15
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class HcmlBodyExpoFr02:
    msg_name = "HcmlBodyExpoFr02"
    msg_id = 593
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 3
    tx_node = "HCML"
    rx_nodes = ['BGM']

    class StsOfLedHiBeamLe:
        sig_name = "StsOfLedHiBeamLe"
        sig_start_bit = 1
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class StsOfLedLoBeamLe:
        sig_name = "StsOfLedLoBeamLe"
        sig_start_bit = 4
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 4
        byte = 0
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class ExtrLiShowStoreStsFrntLe_0_HcmlBodyExpoSignalIPdu02:
        sig_name = "ExtrLiShowStoreStsFrntLe_0_HcmlBodyExpoSignalIPdu02"
        sig_start_bit = 7
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7


class CemBodyExpoFr101:
    msg_name = "CemBodyExpoFr101"
    msg_id = 835
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR']

    class DwnLoadDynLtgPrmForFrntRIGrp11Timestamp_1_CemBodyExpoSignalIPdu101:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp11Timestamp_1_CemBodyExpoSignalIPdu101"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DwnLoadDynLtgPrmForFrntRIGrp11Mode1_1_CemBodyExpoSignalIPdu101:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp11Mode1_1_CemBodyExpoSignalIPdu101"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode4_Off': 0, 'Mode4_On': 1, 'Mode4_GradualOn': 2, 'Mode4_GradualOff': 3, 'Mode4_ForwardWipingOn': 4, 'Mode4_BackwardWipingOn': 5, 'Mode4_OutwardWipingOn': 6, 'Mode4_InwardWipingOn': 7, 'Mode4_ForwardWipingOff': 8, 'Mode4_BackwardWipingOff': 9, 'Mode4_OutwardWipingOff': 10, 'Mode4_InwardWipingOff': 11, 'Mode4_ForwardScanning': 12, 'Mode4_BackwardScanning': 13, 'Mode4_BreathOn': 14, 'Mode4_BreathOff': 15, 'Mode4_1stHalfONand2ndHalfOFF': 16, 'Mode4_HalfOFFHalfON': 17, 'Mode4_HalfDimmingONHalfOFF': 18, 'Mode4_HalfDimmingONHalfON': 19, 'Mode4_HalfOFFHalfDimmingON': 20, 'Mode4_HalfONHalfDimmingON': 21, 'Mode4_HalfDimmingOFFHalfOFF': 22, 'Mode4_HalfDimmingOFFHalfON': 23, 'Mode4_HalfOFFHalfDimmingOFF': 24, 'Mode4_HalfONHalfDimmingOFF': 25, 'Mode4_SingleOn1': 26, 'Mode4_SingleOn2': 27, 'Mode4_SingleOn3': 28, 'Mode4_SingleOn4': 29, 'Mode4_SingleOn5': 30, 'Mode4_SingleOn6': 31, 'Mode4_SingleOn7': 32, 'Mode4_SingleOn8': 33, 'Mode4_SingleOn9': 34, 'Mode4_SingleOn10': 35, 'Mode4_SingleOn11': 36, 'Mode4_SingleOn12': 37, 'Mode4_SingleOff1': 38, 'Mode4_SingleOff2': 39, 'Mode4_SingleOff3': 40, 'Mode4_SingleOff4': 41, 'Mode4_SingleOff5': 42, 'Mode4_SingleOff6': 43, 'Mode4_SingleOff7': 44, 'Mode4_SingleOff8': 45, 'Mode4_SingleOff9': 46, 'Mode4_SingleOff10': 47, 'Mode4_SingleOff11': 48, 'Mode4_SingleOff12': 49}
        compute_method = None
        length = 6
        startbit = 23
        byte = 2
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntRIGrp11LowBrightness_1_CemBodyExpoSignalIPdu101:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp11LowBrightness_1_CemBodyExpoSignalIPdu101"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DwnLoadDynLtgPrmForFrntRIGrp11HighBrightness_1_CemBodyExpoSignalIPdu101:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp11HighBrightness_1_CemBodyExpoSignalIPdu101"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DwnLoadDynLtgPrmForFrntRIGrp11ContinueTime_1_CemBodyExpoSignalIPdu101:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp11ContinueTime_1_CemBodyExpoSignalIPdu101"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForFrntRIGrp11OffsetTime_1_CemBodyExpoSignalIPdu101:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp11OffsetTime_1_CemBodyExpoSignalIPdu101"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 31
        byte = 3
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2


class CemBodyExpoFr33:
    msg_name = "CemBodyExpoFr33"
    msg_id = 318
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR']

    class DwnLoadDynLtgPrmForLedDaytiRunngLampRiContTiPrm_1_CemBodyExpoSignalIPdu33:
        sig_name = "DwnLoadDynLtgPrmForLedDaytiRunngLampRiContTiPrm_1_CemBodyExpoSignalIPdu33"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLtgPrmForLedDaytiRunngLampRiTistamp_1_CemBodyExpoSignalIPdu33:
        sig_name = "DwnLoadDynLtgPrmForLedDaytiRunngLampRiTistamp_1_CemBodyExpoSignalIPdu33"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLtgPrmForLedDaytiRunngLampRiUpprBriPrm_1_CemBodyExpoSignalIPdu33:
        sig_name = "DwnLoadDynLtgPrmForLedDaytiRunngLampRiUpprBriPrm_1_CemBodyExpoSignalIPdu33"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForLedDaytiRunngLampRiLowBriPrm_1_CemBodyExpoSignalIPdu33:
        sig_name = "DwnLoadDynLtgPrmForLedDaytiRunngLampRiLowBriPrm_1_CemBodyExpoSignalIPdu33"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForLedDaytiRunngLampRiOffsTiPrm_1_CemBodyExpoSignalIPdu33:
        sig_name = "DwnLoadDynLtgPrmForLedDaytiRunngLampRiOffsTiPrm_1_CemBodyExpoSignalIPdu33"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLtgPrmForLedDaytiRunngLampRiModePrm_1_CemBodyExpoSignalIPdu33:
        sig_name = "DwnLoadDynLtgPrmForLedDaytiRunngLampRiModePrm_1_CemBodyExpoSignalIPdu33"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode1_Off': 0, 'Mode1_On': 1, 'Mode1_GradualOn': 2, 'Mode1_GradualOff': 3, 'Mode1_ForwardWipingOn': 4, 'Mode1_BackwardWipingOn': 5, 'Mode1_OutwardWipingOn': 6, 'Mode1_InwardWipingOn': 7, 'Mode1_ForwardWipingOff': 8, 'Mode1_BackwardWipingOff': 9, 'Mode1_OutwardWipingOff': 10, 'Mode1_InwardWipingOff': 11, 'Mode1_ForwardScanning': 12, 'Mode1_BackwardScanning': 13, 'Mode1_BreathOn': 14, 'Mode1_BreathOff': 15, 'Mode1_Spare1': 16, 'Mode1_Spare2': 17}
        compute_method = None
        length = 5
        startbit = 13
        byte = 1
        mask = 0b00111110
        unmask = 0b11000001
        shift = 1


class CemBodyExpoFr92:
    msg_name = "CemBodyExpoFr92"
    msg_id = 826
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR']

    class DwnLoadDynLtgPrmForFrntRIGrp2LowBrightness_1_CemBodyExpoSignalIPdu92:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp2LowBrightness_1_CemBodyExpoSignalIPdu92"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DwnLoadDynLtgPrmForFrntRIGrp2OffsetTime_1_CemBodyExpoSignalIPdu92:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp2OffsetTime_1_CemBodyExpoSignalIPdu92"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 31
        byte = 3
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntRIGrp2Mode1_1_CemBodyExpoSignalIPdu92:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp2Mode1_1_CemBodyExpoSignalIPdu92"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode4_Off': 0, 'Mode4_On': 1, 'Mode4_GradualOn': 2, 'Mode4_GradualOff': 3, 'Mode4_ForwardWipingOn': 4, 'Mode4_BackwardWipingOn': 5, 'Mode4_OutwardWipingOn': 6, 'Mode4_InwardWipingOn': 7, 'Mode4_ForwardWipingOff': 8, 'Mode4_BackwardWipingOff': 9, 'Mode4_OutwardWipingOff': 10, 'Mode4_InwardWipingOff': 11, 'Mode4_ForwardScanning': 12, 'Mode4_BackwardScanning': 13, 'Mode4_BreathOn': 14, 'Mode4_BreathOff': 15, 'Mode4_1stHalfONand2ndHalfOFF': 16, 'Mode4_HalfOFFHalfON': 17, 'Mode4_HalfDimmingONHalfOFF': 18, 'Mode4_HalfDimmingONHalfON': 19, 'Mode4_HalfOFFHalfDimmingON': 20, 'Mode4_HalfONHalfDimmingON': 21, 'Mode4_HalfDimmingOFFHalfOFF': 22, 'Mode4_HalfDimmingOFFHalfON': 23, 'Mode4_HalfOFFHalfDimmingOFF': 24, 'Mode4_HalfONHalfDimmingOFF': 25, 'Mode4_SingleOn1': 26, 'Mode4_SingleOn2': 27, 'Mode4_SingleOn3': 28, 'Mode4_SingleOn4': 29, 'Mode4_SingleOn5': 30, 'Mode4_SingleOn6': 31, 'Mode4_SingleOn7': 32, 'Mode4_SingleOn8': 33, 'Mode4_SingleOn9': 34, 'Mode4_SingleOn10': 35, 'Mode4_SingleOn11': 36, 'Mode4_SingleOn12': 37, 'Mode4_SingleOff1': 38, 'Mode4_SingleOff2': 39, 'Mode4_SingleOff3': 40, 'Mode4_SingleOff4': 41, 'Mode4_SingleOff5': 42, 'Mode4_SingleOff6': 43, 'Mode4_SingleOff7': 44, 'Mode4_SingleOff8': 45, 'Mode4_SingleOff9': 46, 'Mode4_SingleOff10': 47, 'Mode4_SingleOff11': 48, 'Mode4_SingleOff12': 49}
        compute_method = None
        length = 6
        startbit = 23
        byte = 2
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntRIGrp2HighBrightness_1_CemBodyExpoSignalIPdu92:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp2HighBrightness_1_CemBodyExpoSignalIPdu92"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DwnLoadDynLtgPrmForFrntRIGrp2ContinueTime_1_CemBodyExpoSignalIPdu92:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp2ContinueTime_1_CemBodyExpoSignalIPdu92"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForFrntRIGrp2Timestamp_1_CemBodyExpoSignalIPdu92:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp2Timestamp_1_CemBodyExpoSignalIPdu92"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5


class HcmrtoEtcXCPFr01:
    msg_name = "HcmrtoEtcXCPFr01"
    msg_id = 1426
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "HCMR"
    rx_nodes = ['CCM']


class CemBodyExpoFr31:
    msg_name = "CemBodyExpoFr31"
    msg_id = 316
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR']

    class DwnLoadDynLtgPrmForLedCornrgLampRiLowBriPrm_1_CemBodyExpoSignalIPdu31:
        sig_name = "DwnLoadDynLtgPrmForLedCornrgLampRiLowBriPrm_1_CemBodyExpoSignalIPdu31"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForLedCornrgLampRiModePrm_1_CemBodyExpoSignalIPdu31:
        sig_name = "DwnLoadDynLtgPrmForLedCornrgLampRiModePrm_1_CemBodyExpoSignalIPdu31"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode1_Off': 0, 'Mode1_On': 1, 'Mode1_GradualOn': 2, 'Mode1_GradualOff': 3, 'Mode1_ForwardWipingOn': 4, 'Mode1_BackwardWipingOn': 5, 'Mode1_OutwardWipingOn': 6, 'Mode1_InwardWipingOn': 7, 'Mode1_ForwardWipingOff': 8, 'Mode1_BackwardWipingOff': 9, 'Mode1_OutwardWipingOff': 10, 'Mode1_InwardWipingOff': 11, 'Mode1_ForwardScanning': 12, 'Mode1_BackwardScanning': 13, 'Mode1_BreathOn': 14, 'Mode1_BreathOff': 15, 'Mode1_Spare1': 16, 'Mode1_Spare2': 17}
        compute_method = None
        length = 5
        startbit = 13
        byte = 1
        mask = 0b00111110
        unmask = 0b11000001
        shift = 1

    class DwnLoadDynLtgPrmForLedCornrgLampRiOffsTiPrm_1_CemBodyExpoSignalIPdu31:
        sig_name = "DwnLoadDynLtgPrmForLedCornrgLampRiOffsTiPrm_1_CemBodyExpoSignalIPdu31"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLtgPrmForLedCornrgLampRiContTiPrm_1_CemBodyExpoSignalIPdu31:
        sig_name = "DwnLoadDynLtgPrmForLedCornrgLampRiContTiPrm_1_CemBodyExpoSignalIPdu31"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLtgPrmForLedCornrgLampRiUpprBriPrm_1_CemBodyExpoSignalIPdu31:
        sig_name = "DwnLoadDynLtgPrmForLedCornrgLampRiUpprBriPrm_1_CemBodyExpoSignalIPdu31"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForLedCornrgLampRiTistamp_1_CemBodyExpoSignalIPdu31:
        sig_name = "DwnLoadDynLtgPrmForLedCornrgLampRiTistamp_1_CemBodyExpoSignalIPdu31"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]


class CemBodyExpoFr107:
    msg_name = "CemBodyExpoFr107"
    msg_id = 841
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR']

    class DwnLoadDynLtgPrmForFrntRIGrp17OffsetTime_1_CemBodyExpoSignalIPdu107:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp17OffsetTime_1_CemBodyExpoSignalIPdu107"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 31
        byte = 3
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntRIGrp17ContinueTime_1_CemBodyExpoSignalIPdu107:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp17ContinueTime_1_CemBodyExpoSignalIPdu107"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForFrntRIGrp17Mode1_1_CemBodyExpoSignalIPdu107:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp17Mode1_1_CemBodyExpoSignalIPdu107"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode4_Off': 0, 'Mode4_On': 1, 'Mode4_GradualOn': 2, 'Mode4_GradualOff': 3, 'Mode4_ForwardWipingOn': 4, 'Mode4_BackwardWipingOn': 5, 'Mode4_OutwardWipingOn': 6, 'Mode4_InwardWipingOn': 7, 'Mode4_ForwardWipingOff': 8, 'Mode4_BackwardWipingOff': 9, 'Mode4_OutwardWipingOff': 10, 'Mode4_InwardWipingOff': 11, 'Mode4_ForwardScanning': 12, 'Mode4_BackwardScanning': 13, 'Mode4_BreathOn': 14, 'Mode4_BreathOff': 15, 'Mode4_1stHalfONand2ndHalfOFF': 16, 'Mode4_HalfOFFHalfON': 17, 'Mode4_HalfDimmingONHalfOFF': 18, 'Mode4_HalfDimmingONHalfON': 19, 'Mode4_HalfOFFHalfDimmingON': 20, 'Mode4_HalfONHalfDimmingON': 21, 'Mode4_HalfDimmingOFFHalfOFF': 22, 'Mode4_HalfDimmingOFFHalfON': 23, 'Mode4_HalfOFFHalfDimmingOFF': 24, 'Mode4_HalfONHalfDimmingOFF': 25, 'Mode4_SingleOn1': 26, 'Mode4_SingleOn2': 27, 'Mode4_SingleOn3': 28, 'Mode4_SingleOn4': 29, 'Mode4_SingleOn5': 30, 'Mode4_SingleOn6': 31, 'Mode4_SingleOn7': 32, 'Mode4_SingleOn8': 33, 'Mode4_SingleOn9': 34, 'Mode4_SingleOn10': 35, 'Mode4_SingleOn11': 36, 'Mode4_SingleOn12': 37, 'Mode4_SingleOff1': 38, 'Mode4_SingleOff2': 39, 'Mode4_SingleOff3': 40, 'Mode4_SingleOff4': 41, 'Mode4_SingleOff5': 42, 'Mode4_SingleOff6': 43, 'Mode4_SingleOff7': 44, 'Mode4_SingleOff8': 45, 'Mode4_SingleOff9': 46, 'Mode4_SingleOff10': 47, 'Mode4_SingleOff11': 48, 'Mode4_SingleOff12': 49}
        compute_method = None
        length = 6
        startbit = 23
        byte = 2
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntRIGrp17LowBrightness_1_CemBodyExpoSignalIPdu107:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp17LowBrightness_1_CemBodyExpoSignalIPdu107"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DwnLoadDynLtgPrmForFrntRIGrp17HighBrightness_1_CemBodyExpoSignalIPdu107:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp17HighBrightness_1_CemBodyExpoSignalIPdu107"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DwnLoadDynLtgPrmForFrntRIGrp17Timestamp_1_CemBodyExpoSignalIPdu107:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp17Timestamp_1_CemBodyExpoSignalIPdu107"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5


class CemBodyExpoFr91:
    msg_name = "CemBodyExpoFr91"
    msg_id = 825
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR']

    class DwnLoadDynLtgPrmForFrntRIGrp1HighBrightness_1_CemBodyExpoSignalIPdu91:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp1HighBrightness_1_CemBodyExpoSignalIPdu91"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DwnLoadDynLtgPrmForFrntRIGrp1LowBrightness_1_CemBodyExpoSignalIPdu91:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp1LowBrightness_1_CemBodyExpoSignalIPdu91"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DwnLoadDynLtgPrmForFrntRIGrp1ContinueTime_1_CemBodyExpoSignalIPdu91:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp1ContinueTime_1_CemBodyExpoSignalIPdu91"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForFrntRIGrp1Mode1_1_CemBodyExpoSignalIPdu91:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp1Mode1_1_CemBodyExpoSignalIPdu91"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode4_Off': 0, 'Mode4_On': 1, 'Mode4_GradualOn': 2, 'Mode4_GradualOff': 3, 'Mode4_ForwardWipingOn': 4, 'Mode4_BackwardWipingOn': 5, 'Mode4_OutwardWipingOn': 6, 'Mode4_InwardWipingOn': 7, 'Mode4_ForwardWipingOff': 8, 'Mode4_BackwardWipingOff': 9, 'Mode4_OutwardWipingOff': 10, 'Mode4_InwardWipingOff': 11, 'Mode4_ForwardScanning': 12, 'Mode4_BackwardScanning': 13, 'Mode4_BreathOn': 14, 'Mode4_BreathOff': 15, 'Mode4_1stHalfONand2ndHalfOFF': 16, 'Mode4_HalfOFFHalfON': 17, 'Mode4_HalfDimmingONHalfOFF': 18, 'Mode4_HalfDimmingONHalfON': 19, 'Mode4_HalfOFFHalfDimmingON': 20, 'Mode4_HalfONHalfDimmingON': 21, 'Mode4_HalfDimmingOFFHalfOFF': 22, 'Mode4_HalfDimmingOFFHalfON': 23, 'Mode4_HalfOFFHalfDimmingOFF': 24, 'Mode4_HalfONHalfDimmingOFF': 25, 'Mode4_SingleOn1': 26, 'Mode4_SingleOn2': 27, 'Mode4_SingleOn3': 28, 'Mode4_SingleOn4': 29, 'Mode4_SingleOn5': 30, 'Mode4_SingleOn6': 31, 'Mode4_SingleOn7': 32, 'Mode4_SingleOn8': 33, 'Mode4_SingleOn9': 34, 'Mode4_SingleOn10': 35, 'Mode4_SingleOn11': 36, 'Mode4_SingleOn12': 37, 'Mode4_SingleOff1': 38, 'Mode4_SingleOff2': 39, 'Mode4_SingleOff3': 40, 'Mode4_SingleOff4': 41, 'Mode4_SingleOff5': 42, 'Mode4_SingleOff6': 43, 'Mode4_SingleOff7': 44, 'Mode4_SingleOff8': 45, 'Mode4_SingleOff9': 46, 'Mode4_SingleOff10': 47, 'Mode4_SingleOff11': 48, 'Mode4_SingleOff12': 49}
        compute_method = None
        length = 6
        startbit = 23
        byte = 2
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntRIGrp1Timestamp_1_CemBodyExpoSignalIPdu91:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp1Timestamp_1_CemBodyExpoSignalIPdu91"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DwnLoadDynLtgPrmForFrntRIGrp1OffsetTime_1_CemBodyExpoSignalIPdu91:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp1OffsetTime_1_CemBodyExpoSignalIPdu91"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 31
        byte = 3
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2


class CemBodyExpoFr12:
    msg_name = "CemBodyExpoFr12"
    msg_id = 298
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RCMR']

    class DwnLoadDynLitPrmForLedStopLampRi1LowBriPrm_1_CemBodyExpoSignalIPdu12:
        sig_name = "DwnLoadDynLitPrmForLedStopLampRi1LowBriPrm_1_CemBodyExpoSignalIPdu12"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmForLedStopLampRi1UpprBriPrm_1_CemBodyExpoSignalIPdu12:
        sig_name = "DwnLoadDynLitPrmForLedStopLampRi1UpprBriPrm_1_CemBodyExpoSignalIPdu12"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmForLedStopLampRi1Tistamp_1_CemBodyExpoSignalIPdu12:
        sig_name = "DwnLoadDynLitPrmForLedStopLampRi1Tistamp_1_CemBodyExpoSignalIPdu12"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmForLedStopLampRi1ModePrm_1_CemBodyExpoSignalIPdu12:
        sig_name = "DwnLoadDynLitPrmForLedStopLampRi1ModePrm_1_CemBodyExpoSignalIPdu12"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode1_Off': 0, 'Mode1_On': 1, 'Mode1_GradualOn': 2, 'Mode1_GradualOff': 3, 'Mode1_ForwardWipingOn': 4, 'Mode1_BackwardWipingOn': 5, 'Mode1_OutwardWipingOn': 6, 'Mode1_InwardWipingOn': 7, 'Mode1_ForwardWipingOff': 8, 'Mode1_BackwardWipingOff': 9, 'Mode1_OutwardWipingOff': 10, 'Mode1_InwardWipingOff': 11, 'Mode1_ForwardScanning': 12, 'Mode1_BackwardScanning': 13, 'Mode1_BreathOn': 14, 'Mode1_BreathOff': 15, 'Mode1_Spare1': 16, 'Mode1_Spare2': 17}
        compute_method = None
        length = 5
        startbit = 13
        byte = 1
        mask = 0b00111110
        unmask = 0b11000001
        shift = 1

    class DwnLoadDynLitPrmForLedStopLampRi1ContTiPrm_1_CemBodyExpoSignalIPdu12:
        sig_name = "DwnLoadDynLitPrmForLedStopLampRi1ContTiPrm_1_CemBodyExpoSignalIPdu12"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmForLedStopLampRi1OffsTiPrm_1_CemBodyExpoSignalIPdu12:
        sig_name = "DwnLoadDynLitPrmForLedStopLampRi1OffsTiPrm_1_CemBodyExpoSignalIPdu12"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]


class CemBodyExpoFr38:
    msg_name = "CemBodyExpoFr38"
    msg_id = 323
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR']

    class DwnLoadDynLtgPrmForLedHiBeamRiOffsTiPrm_1_CemBodyExpoSignalIPdu38:
        sig_name = "DwnLoadDynLtgPrmForLedHiBeamRiOffsTiPrm_1_CemBodyExpoSignalIPdu38"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLtgPrmForLedHiBeamRiTistamp_1_CemBodyExpoSignalIPdu38:
        sig_name = "DwnLoadDynLtgPrmForLedHiBeamRiTistamp_1_CemBodyExpoSignalIPdu38"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLtgPrmForLedHiBeamRiModePrm_1_CemBodyExpoSignalIPdu38:
        sig_name = "DwnLoadDynLtgPrmForLedHiBeamRiModePrm_1_CemBodyExpoSignalIPdu38"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode1_Off': 0, 'Mode1_On': 1, 'Mode1_GradualOn': 2, 'Mode1_GradualOff': 3, 'Mode1_ForwardWipingOn': 4, 'Mode1_BackwardWipingOn': 5, 'Mode1_OutwardWipingOn': 6, 'Mode1_InwardWipingOn': 7, 'Mode1_ForwardWipingOff': 8, 'Mode1_BackwardWipingOff': 9, 'Mode1_OutwardWipingOff': 10, 'Mode1_InwardWipingOff': 11, 'Mode1_ForwardScanning': 12, 'Mode1_BackwardScanning': 13, 'Mode1_BreathOn': 14, 'Mode1_BreathOff': 15, 'Mode1_Spare1': 16, 'Mode1_Spare2': 17}
        compute_method = None
        length = 5
        startbit = 13
        byte = 1
        mask = 0b00111110
        unmask = 0b11000001
        shift = 1

    class DwnLoadDynLtgPrmForLedHiBeamRiUpprBriPrm_1_CemBodyExpoSignalIPdu38:
        sig_name = "DwnLoadDynLtgPrmForLedHiBeamRiUpprBriPrm_1_CemBodyExpoSignalIPdu38"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForLedHiBeamRiContTiPrm_1_CemBodyExpoSignalIPdu38:
        sig_name = "DwnLoadDynLtgPrmForLedHiBeamRiContTiPrm_1_CemBodyExpoSignalIPdu38"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLtgPrmForLedHiBeamRiLowBriPrm_1_CemBodyExpoSignalIPdu38:
        sig_name = "DwnLoadDynLtgPrmForLedHiBeamRiLowBriPrm_1_CemBodyExpoSignalIPdu38"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class CemBodyExpoFr16:
    msg_name = "CemBodyExpoFr16"
    msg_id = 302
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RCML']

    class DwnLoadDynLitPrmLedRePosnLampLe1Tistamp_1_CemBodyExpoSignalIPdu16:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe1Tistamp_1_CemBodyExpoSignalIPdu16"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmLedRePosnLampLe1LowBriPrm_1_CemBodyExpoSignalIPdu16:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe1LowBriPrm_1_CemBodyExpoSignalIPdu16"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmLedRePosnLampLe1ModePrm_1_CemBodyExpoSignalIPdu16:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe1ModePrm_1_CemBodyExpoSignalIPdu16"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode1_Off': 0, 'Mode1_On': 1, 'Mode1_GradualOn': 2, 'Mode1_GradualOff': 3, 'Mode1_ForwardWipingOn': 4, 'Mode1_BackwardWipingOn': 5, 'Mode1_OutwardWipingOn': 6, 'Mode1_InwardWipingOn': 7, 'Mode1_ForwardWipingOff': 8, 'Mode1_BackwardWipingOff': 9, 'Mode1_OutwardWipingOff': 10, 'Mode1_InwardWipingOff': 11, 'Mode1_ForwardScanning': 12, 'Mode1_BackwardScanning': 13, 'Mode1_BreathOn': 14, 'Mode1_BreathOff': 15, 'Mode1_Spare1': 16, 'Mode1_Spare2': 17}
        compute_method = None
        length = 5
        startbit = 13
        byte = 1
        mask = 0b00111110
        unmask = 0b11000001
        shift = 1

    class DwnLoadDynLitPrmLedRePosnLampLe1ContTiPrm_1_CemBodyExpoSignalIPdu16:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe1ContTiPrm_1_CemBodyExpoSignalIPdu16"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedRePosnLampLe1OffsTiPrm_1_CemBodyExpoSignalIPdu16:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe1OffsTiPrm_1_CemBodyExpoSignalIPdu16"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedRePosnLampLe1UpprBriPrm_1_CemBodyExpoSignalIPdu16:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe1UpprBriPrm_1_CemBodyExpoSignalIPdu16"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class CemBodyExpoFr19:
    msg_name = "CemBodyExpoFr19"
    msg_id = 305
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RCML']

    class DwnLoadDynLitPrmLedReTurnIndcrLe1LowBriPrm_1_CemBodyExpoSignalIPdu19:
        sig_name = "DwnLoadDynLitPrmLedReTurnIndcrLe1LowBriPrm_1_CemBodyExpoSignalIPdu19"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmLedReTurnIndcrLe1Tistamp_1_CemBodyExpoSignalIPdu19:
        sig_name = "DwnLoadDynLitPrmLedReTurnIndcrLe1Tistamp_1_CemBodyExpoSignalIPdu19"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmLedReTurnIndcrLe1ModePrm_1_CemBodyExpoSignalIPdu19:
        sig_name = "DwnLoadDynLitPrmLedReTurnIndcrLe1ModePrm_1_CemBodyExpoSignalIPdu19"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode1_Off': 0, 'Mode1_On': 1, 'Mode1_GradualOn': 2, 'Mode1_GradualOff': 3, 'Mode1_ForwardWipingOn': 4, 'Mode1_BackwardWipingOn': 5, 'Mode1_OutwardWipingOn': 6, 'Mode1_InwardWipingOn': 7, 'Mode1_ForwardWipingOff': 8, 'Mode1_BackwardWipingOff': 9, 'Mode1_OutwardWipingOff': 10, 'Mode1_InwardWipingOff': 11, 'Mode1_ForwardScanning': 12, 'Mode1_BackwardScanning': 13, 'Mode1_BreathOn': 14, 'Mode1_BreathOff': 15, 'Mode1_Spare1': 16, 'Mode1_Spare2': 17}
        compute_method = None
        length = 5
        startbit = 13
        byte = 1
        mask = 0b00111110
        unmask = 0b11000001
        shift = 1

    class DwnLoadDynLitPrmLedReTurnIndcrLe1OffsTiPrm_1_CemBodyExpoSignalIPdu19:
        sig_name = "DwnLoadDynLitPrmLedReTurnIndcrLe1OffsTiPrm_1_CemBodyExpoSignalIPdu19"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedReTurnIndcrLe1ContTiPrm_1_CemBodyExpoSignalIPdu19:
        sig_name = "DwnLoadDynLitPrmLedReTurnIndcrLe1ContTiPrm_1_CemBodyExpoSignalIPdu19"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedReTurnIndcrLe1UpprBriPrm_1_CemBodyExpoSignalIPdu19:
        sig_name = "DwnLoadDynLitPrmLedReTurnIndcrLe1UpprBriPrm_1_CemBodyExpoSignalIPdu19"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class CemBodyExpoFr69:
    msg_name = "CemBodyExpoFr69"
    msg_id = 803
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCML']

    class DwnLoadDynLtgPrmForFrntLeGrp3Timestamp_1_CemBodyExpoSignalIPdu69:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp3Timestamp_1_CemBodyExpoSignalIPdu69"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DwnLoadDynLtgPrmForFrntLeGrp3LowBrightness_1_CemBodyExpoSignalIPdu69:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp3LowBrightness_1_CemBodyExpoSignalIPdu69"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DwnLoadDynLtgPrmForFrntLeGrp3ContinueTime_1_CemBodyExpoSignalIPdu69:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp3ContinueTime_1_CemBodyExpoSignalIPdu69"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForFrntLeGrp3OffsetTime_1_CemBodyExpoSignalIPdu69:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp3OffsetTime_1_CemBodyExpoSignalIPdu69"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 31
        byte = 3
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntLeGrp3HighBrightness_1_CemBodyExpoSignalIPdu69:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp3HighBrightness_1_CemBodyExpoSignalIPdu69"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DwnLoadDynLtgPrmForFrntLeGrp3Mode1_1_CemBodyExpoSignalIPdu69:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp3Mode1_1_CemBodyExpoSignalIPdu69"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode4_Off': 0, 'Mode4_On': 1, 'Mode4_GradualOn': 2, 'Mode4_GradualOff': 3, 'Mode4_ForwardWipingOn': 4, 'Mode4_BackwardWipingOn': 5, 'Mode4_OutwardWipingOn': 6, 'Mode4_InwardWipingOn': 7, 'Mode4_ForwardWipingOff': 8, 'Mode4_BackwardWipingOff': 9, 'Mode4_OutwardWipingOff': 10, 'Mode4_InwardWipingOff': 11, 'Mode4_ForwardScanning': 12, 'Mode4_BackwardScanning': 13, 'Mode4_BreathOn': 14, 'Mode4_BreathOff': 15, 'Mode4_1stHalfONand2ndHalfOFF': 16, 'Mode4_HalfOFFHalfON': 17, 'Mode4_HalfDimmingONHalfOFF': 18, 'Mode4_HalfDimmingONHalfON': 19, 'Mode4_HalfOFFHalfDimmingON': 20, 'Mode4_HalfONHalfDimmingON': 21, 'Mode4_HalfDimmingOFFHalfOFF': 22, 'Mode4_HalfDimmingOFFHalfON': 23, 'Mode4_HalfOFFHalfDimmingOFF': 24, 'Mode4_HalfONHalfDimmingOFF': 25, 'Mode4_SingleOn1': 26, 'Mode4_SingleOn2': 27, 'Mode4_SingleOn3': 28, 'Mode4_SingleOn4': 29, 'Mode4_SingleOn5': 30, 'Mode4_SingleOn6': 31, 'Mode4_SingleOn7': 32, 'Mode4_SingleOn8': 33, 'Mode4_SingleOn9': 34, 'Mode4_SingleOn10': 35, 'Mode4_SingleOn11': 36, 'Mode4_SingleOn12': 37, 'Mode4_SingleOff1': 38, 'Mode4_SingleOff2': 39, 'Mode4_SingleOff3': 40, 'Mode4_SingleOff4': 41, 'Mode4_SingleOff5': 42, 'Mode4_SingleOff6': 43, 'Mode4_SingleOff7': 44, 'Mode4_SingleOff8': 45, 'Mode4_SingleOff9': 46, 'Mode4_SingleOff10': 47, 'Mode4_SingleOff11': 48, 'Mode4_SingleOff12': 49}
        compute_method = None
        length = 6
        startbit = 23
        byte = 2
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2


class CemBodyExpoFr21:
    msg_name = "CemBodyExpoFr21"
    msg_id = 307
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RCMR']

    class DwnLoadDynLitPrmLedReTurnIndcrRi1ContTiPrm_1_CemBodyExpoSignalIPdu21:
        sig_name = "DwnLoadDynLitPrmLedReTurnIndcrRi1ContTiPrm_1_CemBodyExpoSignalIPdu21"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedReTurnIndcrRi1Tistamp_1_CemBodyExpoSignalIPdu21:
        sig_name = "DwnLoadDynLitPrmLedReTurnIndcrRi1Tistamp_1_CemBodyExpoSignalIPdu21"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmLedReTurnIndcrRi1OffsTiPrm_1_CemBodyExpoSignalIPdu21:
        sig_name = "DwnLoadDynLitPrmLedReTurnIndcrRi1OffsTiPrm_1_CemBodyExpoSignalIPdu21"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedReTurnIndcrRi1LowBriPrm_1_CemBodyExpoSignalIPdu21:
        sig_name = "DwnLoadDynLitPrmLedReTurnIndcrRi1LowBriPrm_1_CemBodyExpoSignalIPdu21"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmLedReTurnIndcrRi1UpprBriPrm_1_CemBodyExpoSignalIPdu21:
        sig_name = "DwnLoadDynLitPrmLedReTurnIndcrRi1UpprBriPrm_1_CemBodyExpoSignalIPdu21"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmLedReTurnIndcrRi1ModePrm_1_CemBodyExpoSignalIPdu21:
        sig_name = "DwnLoadDynLitPrmLedReTurnIndcrRi1ModePrm_1_CemBodyExpoSignalIPdu21"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode1_Off': 0, 'Mode1_On': 1, 'Mode1_GradualOn': 2, 'Mode1_GradualOff': 3, 'Mode1_ForwardWipingOn': 4, 'Mode1_BackwardWipingOn': 5, 'Mode1_OutwardWipingOn': 6, 'Mode1_InwardWipingOn': 7, 'Mode1_ForwardWipingOff': 8, 'Mode1_BackwardWipingOff': 9, 'Mode1_OutwardWipingOff': 10, 'Mode1_InwardWipingOff': 11, 'Mode1_ForwardScanning': 12, 'Mode1_BackwardScanning': 13, 'Mode1_BreathOn': 14, 'Mode1_BreathOff': 15, 'Mode1_Spare1': 16, 'Mode1_Spare2': 17}
        compute_method = None
        length = 5
        startbit = 13
        byte = 1
        mask = 0b00111110
        unmask = 0b11000001
        shift = 1


class RcmlBodyExposedCANNmFr:
    msg_name = "RcmlBodyExposedCANNmFr"
    msg_id = 1331
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "RCML"
    rx_nodes = ['HCMR']


class CemBodyExpoFr57:
    msg_name = "CemBodyExpoFr57"
    msg_id = 331
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RCMR']

    class DwnLoadDynLitPrmLedRePosnLampRi4ModePrm_1_CemBodyExpoSignalIPdu57:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi4ModePrm_1_CemBodyExpoSignalIPdu57"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode1_Off': 0, 'Mode1_On': 1, 'Mode1_GradualOn': 2, 'Mode1_GradualOff': 3, 'Mode1_ForwardWipingOn': 4, 'Mode1_BackwardWipingOn': 5, 'Mode1_OutwardWipingOn': 6, 'Mode1_InwardWipingOn': 7, 'Mode1_ForwardWipingOff': 8, 'Mode1_BackwardWipingOff': 9, 'Mode1_OutwardWipingOff': 10, 'Mode1_InwardWipingOff': 11, 'Mode1_ForwardScanning': 12, 'Mode1_BackwardScanning': 13, 'Mode1_BreathOn': 14, 'Mode1_BreathOff': 15, 'Mode1_Spare1': 16, 'Mode1_Spare2': 17}
        compute_method = None
        length = 5
        startbit = 13
        byte = 1
        mask = 0b00111110
        unmask = 0b11000001
        shift = 1

    class DwnLoadDynLitPrmLedRePosnLampRi4OffsTiPrm_1_CemBodyExpoSignalIPdu57:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi4OffsTiPrm_1_CemBodyExpoSignalIPdu57"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedRePosnLampRi4Tistamp_1_CemBodyExpoSignalIPdu57:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi4Tistamp_1_CemBodyExpoSignalIPdu57"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmLedRePosnLampRi4ContTiPrm_1_CemBodyExpoSignalIPdu57:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi4ContTiPrm_1_CemBodyExpoSignalIPdu57"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedRePosnLampRi4UpprBriPrm_1_CemBodyExpoSignalIPdu57:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi4UpprBriPrm_1_CemBodyExpoSignalIPdu57"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmLedRePosnLampRi4LowBriPrm_1_CemBodyExpoSignalIPdu57:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi4LowBriPrm_1_CemBodyExpoSignalIPdu57"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class CemBodyExpoFr86:
    msg_name = "CemBodyExpoFr86"
    msg_id = 820
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCML']

    class DwnLoadDynLtgPrmForFrntLeGrp20Timestamp_1_CemBodyExpoSignalIPdu86:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp20Timestamp_1_CemBodyExpoSignalIPdu86"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DwnLoadDynLtgPrmForFrntLeGrp20ContinueTime_1_CemBodyExpoSignalIPdu86:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp20ContinueTime_1_CemBodyExpoSignalIPdu86"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForFrntLeGrp20HighBrightness_1_CemBodyExpoSignalIPdu86:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp20HighBrightness_1_CemBodyExpoSignalIPdu86"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DwnLoadDynLtgPrmForFrntLeGrp20LowBrightness_1_CemBodyExpoSignalIPdu86:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp20LowBrightness_1_CemBodyExpoSignalIPdu86"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DwnLoadDynLtgPrmForFrntLeGrp20OffsetTime_1_CemBodyExpoSignalIPdu86:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp20OffsetTime_1_CemBodyExpoSignalIPdu86"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 31
        byte = 3
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntLeGrp20Mode1_1_CemBodyExpoSignalIPdu86:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp20Mode1_1_CemBodyExpoSignalIPdu86"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode4_Off': 0, 'Mode4_On': 1, 'Mode4_GradualOn': 2, 'Mode4_GradualOff': 3, 'Mode4_ForwardWipingOn': 4, 'Mode4_BackwardWipingOn': 5, 'Mode4_OutwardWipingOn': 6, 'Mode4_InwardWipingOn': 7, 'Mode4_ForwardWipingOff': 8, 'Mode4_BackwardWipingOff': 9, 'Mode4_OutwardWipingOff': 10, 'Mode4_InwardWipingOff': 11, 'Mode4_ForwardScanning': 12, 'Mode4_BackwardScanning': 13, 'Mode4_BreathOn': 14, 'Mode4_BreathOff': 15, 'Mode4_1stHalfONand2ndHalfOFF': 16, 'Mode4_HalfOFFHalfON': 17, 'Mode4_HalfDimmingONHalfOFF': 18, 'Mode4_HalfDimmingONHalfON': 19, 'Mode4_HalfOFFHalfDimmingON': 20, 'Mode4_HalfONHalfDimmingON': 21, 'Mode4_HalfDimmingOFFHalfOFF': 22, 'Mode4_HalfDimmingOFFHalfON': 23, 'Mode4_HalfOFFHalfDimmingOFF': 24, 'Mode4_HalfONHalfDimmingOFF': 25, 'Mode4_SingleOn1': 26, 'Mode4_SingleOn2': 27, 'Mode4_SingleOn3': 28, 'Mode4_SingleOn4': 29, 'Mode4_SingleOn5': 30, 'Mode4_SingleOn6': 31, 'Mode4_SingleOn7': 32, 'Mode4_SingleOn8': 33, 'Mode4_SingleOn9': 34, 'Mode4_SingleOn10': 35, 'Mode4_SingleOn11': 36, 'Mode4_SingleOn12': 37, 'Mode4_SingleOff1': 38, 'Mode4_SingleOff2': 39, 'Mode4_SingleOff3': 40, 'Mode4_SingleOff4': 41, 'Mode4_SingleOff5': 42, 'Mode4_SingleOff6': 43, 'Mode4_SingleOff7': 44, 'Mode4_SingleOff8': 45, 'Mode4_SingleOff9': 46, 'Mode4_SingleOff10': 47, 'Mode4_SingleOff11': 48, 'Mode4_SingleOff12': 49}
        compute_method = None
        length = 6
        startbit = 23
        byte = 2
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2


class CemBodyExpoFr10:
    msg_name = "CemBodyExpoFr10"
    msg_id = 296
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RCML']

    class DwnLoadDynLitPrmForLedStopLampLe1ContTiPrm_1_CemBodyExpoSignalIPdu10:
        sig_name = "DwnLoadDynLitPrmForLedStopLampLe1ContTiPrm_1_CemBodyExpoSignalIPdu10"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmForLedStopLampLe1ModePrm_1_CemBodyExpoSignalIPdu10:
        sig_name = "DwnLoadDynLitPrmForLedStopLampLe1ModePrm_1_CemBodyExpoSignalIPdu10"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode1_Off': 0, 'Mode1_On': 1, 'Mode1_GradualOn': 2, 'Mode1_GradualOff': 3, 'Mode1_ForwardWipingOn': 4, 'Mode1_BackwardWipingOn': 5, 'Mode1_OutwardWipingOn': 6, 'Mode1_InwardWipingOn': 7, 'Mode1_ForwardWipingOff': 8, 'Mode1_BackwardWipingOff': 9, 'Mode1_OutwardWipingOff': 10, 'Mode1_InwardWipingOff': 11, 'Mode1_ForwardScanning': 12, 'Mode1_BackwardScanning': 13, 'Mode1_BreathOn': 14, 'Mode1_BreathOff': 15, 'Mode1_Spare1': 16, 'Mode1_Spare2': 17}
        compute_method = None
        length = 5
        startbit = 13
        byte = 1
        mask = 0b00111110
        unmask = 0b11000001
        shift = 1

    class DwnLoadDynLitPrmForLedStopLampLe1LowBriPrm_1_CemBodyExpoSignalIPdu10:
        sig_name = "DwnLoadDynLitPrmForLedStopLampLe1LowBriPrm_1_CemBodyExpoSignalIPdu10"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmForLedStopLampLe1UpprBriPrm_1_CemBodyExpoSignalIPdu10:
        sig_name = "DwnLoadDynLitPrmForLedStopLampLe1UpprBriPrm_1_CemBodyExpoSignalIPdu10"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmForLedStopLampLe1OffsTiPrm_1_CemBodyExpoSignalIPdu10:
        sig_name = "DwnLoadDynLitPrmForLedStopLampLe1OffsTiPrm_1_CemBodyExpoSignalIPdu10"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmForLedStopLampLe1Tistamp_1_CemBodyExpoSignalIPdu10:
        sig_name = "DwnLoadDynLitPrmForLedStopLampLe1Tistamp_1_CemBodyExpoSignalIPdu10"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]


class CemBodyExpoFr59:
    msg_name = "CemBodyExpoFr59"
    msg_id = 24
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR', 'HCML']

    class WelcomeGoodbyeModeReq:
        sig_name = "WelcomeGoodbyeModeReq"
        sig_start_bit = 7
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ModeReq_Mode1': 0, 'ModeReq_Mode2': 1, 'ModeReq_Mode3': 2, 'ModeReq_Mode4': 3, 'ModeReq_Mode5': 4, 'ModeReq_Mode6': 5}
        compute_method = None
        length = 4
        startbit = 7
        byte = 0
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4


class CemBodyExpoFr11:
    msg_name = "CemBodyExpoFr11"
    msg_id = 297
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RCMM']

    class DwnLoadDynLitPrmForLedStopLampLe2UpprBriPrm_1_CemBodyExpoSignalIPdu11:
        sig_name = "DwnLoadDynLitPrmForLedStopLampLe2UpprBriPrm_1_CemBodyExpoSignalIPdu11"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmForLedStopLampLe2OffsTiPrm_1_CemBodyExpoSignalIPdu11:
        sig_name = "DwnLoadDynLitPrmForLedStopLampLe2OffsTiPrm_1_CemBodyExpoSignalIPdu11"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmForLedStopLampLe2LowBriPrm_1_CemBodyExpoSignalIPdu11:
        sig_name = "DwnLoadDynLitPrmForLedStopLampLe2LowBriPrm_1_CemBodyExpoSignalIPdu11"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmForLedStopLampLe2ContTiPrm_1_CemBodyExpoSignalIPdu11:
        sig_name = "DwnLoadDynLitPrmForLedStopLampLe2ContTiPrm_1_CemBodyExpoSignalIPdu11"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmForLedStopLampLe2Tistamp_1_CemBodyExpoSignalIPdu11:
        sig_name = "DwnLoadDynLitPrmForLedStopLampLe2Tistamp_1_CemBodyExpoSignalIPdu11"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmForLedStopLampLe2ModePrm_1_CemBodyExpoSignalIPdu11:
        sig_name = "DwnLoadDynLitPrmForLedStopLampLe2ModePrm_1_CemBodyExpoSignalIPdu11"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode1_Off': 0, 'Mode1_On': 1, 'Mode1_GradualOn': 2, 'Mode1_GradualOff': 3, 'Mode1_ForwardWipingOn': 4, 'Mode1_BackwardWipingOn': 5, 'Mode1_OutwardWipingOn': 6, 'Mode1_InwardWipingOn': 7, 'Mode1_ForwardWipingOff': 8, 'Mode1_BackwardWipingOff': 9, 'Mode1_OutwardWipingOff': 10, 'Mode1_InwardWipingOff': 11, 'Mode1_ForwardScanning': 12, 'Mode1_BackwardScanning': 13, 'Mode1_BreathOn': 14, 'Mode1_BreathOff': 15, 'Mode1_Spare1': 16, 'Mode1_Spare2': 17}
        compute_method = None
        length = 5
        startbit = 13
        byte = 1
        mask = 0b00111110
        unmask = 0b11000001
        shift = 1


class CemBodyExpoFr80:
    msg_name = "CemBodyExpoFr80"
    msg_id = 814
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCML']

    class DwnLoadDynLtgPrmForFrntLeGrp14Mode1_1_CemBodyExpoSignalIPdu80:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp14Mode1_1_CemBodyExpoSignalIPdu80"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode4_Off': 0, 'Mode4_On': 1, 'Mode4_GradualOn': 2, 'Mode4_GradualOff': 3, 'Mode4_ForwardWipingOn': 4, 'Mode4_BackwardWipingOn': 5, 'Mode4_OutwardWipingOn': 6, 'Mode4_InwardWipingOn': 7, 'Mode4_ForwardWipingOff': 8, 'Mode4_BackwardWipingOff': 9, 'Mode4_OutwardWipingOff': 10, 'Mode4_InwardWipingOff': 11, 'Mode4_ForwardScanning': 12, 'Mode4_BackwardScanning': 13, 'Mode4_BreathOn': 14, 'Mode4_BreathOff': 15, 'Mode4_1stHalfONand2ndHalfOFF': 16, 'Mode4_HalfOFFHalfON': 17, 'Mode4_HalfDimmingONHalfOFF': 18, 'Mode4_HalfDimmingONHalfON': 19, 'Mode4_HalfOFFHalfDimmingON': 20, 'Mode4_HalfONHalfDimmingON': 21, 'Mode4_HalfDimmingOFFHalfOFF': 22, 'Mode4_HalfDimmingOFFHalfON': 23, 'Mode4_HalfOFFHalfDimmingOFF': 24, 'Mode4_HalfONHalfDimmingOFF': 25, 'Mode4_SingleOn1': 26, 'Mode4_SingleOn2': 27, 'Mode4_SingleOn3': 28, 'Mode4_SingleOn4': 29, 'Mode4_SingleOn5': 30, 'Mode4_SingleOn6': 31, 'Mode4_SingleOn7': 32, 'Mode4_SingleOn8': 33, 'Mode4_SingleOn9': 34, 'Mode4_SingleOn10': 35, 'Mode4_SingleOn11': 36, 'Mode4_SingleOn12': 37, 'Mode4_SingleOff1': 38, 'Mode4_SingleOff2': 39, 'Mode4_SingleOff3': 40, 'Mode4_SingleOff4': 41, 'Mode4_SingleOff5': 42, 'Mode4_SingleOff6': 43, 'Mode4_SingleOff7': 44, 'Mode4_SingleOff8': 45, 'Mode4_SingleOff9': 46, 'Mode4_SingleOff10': 47, 'Mode4_SingleOff11': 48, 'Mode4_SingleOff12': 49}
        compute_method = None
        length = 6
        startbit = 23
        byte = 2
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntLeGrp14HighBrightness_1_CemBodyExpoSignalIPdu80:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp14HighBrightness_1_CemBodyExpoSignalIPdu80"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DwnLoadDynLtgPrmForFrntLeGrp14Timestamp_1_CemBodyExpoSignalIPdu80:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp14Timestamp_1_CemBodyExpoSignalIPdu80"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DwnLoadDynLtgPrmForFrntLeGrp14LowBrightness_1_CemBodyExpoSignalIPdu80:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp14LowBrightness_1_CemBodyExpoSignalIPdu80"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DwnLoadDynLtgPrmForFrntLeGrp14OffsetTime_1_CemBodyExpoSignalIPdu80:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp14OffsetTime_1_CemBodyExpoSignalIPdu80"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 31
        byte = 3
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntLeGrp14ContinueTime_1_CemBodyExpoSignalIPdu80:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp14ContinueTime_1_CemBodyExpoSignalIPdu80"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class CemBodyExpoFr07:
    msg_name = "CemBodyExpoFr07"
    msg_id = 293
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR']

    class DwnLoadDynLtgPrmForLedLoBeamRiModePrm_1_CemBodyExpoSignalIPdu07:
        sig_name = "DwnLoadDynLtgPrmForLedLoBeamRiModePrm_1_CemBodyExpoSignalIPdu07"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode1_Off': 0, 'Mode1_On': 1, 'Mode1_GradualOn': 2, 'Mode1_GradualOff': 3, 'Mode1_ForwardWipingOn': 4, 'Mode1_BackwardWipingOn': 5, 'Mode1_OutwardWipingOn': 6, 'Mode1_InwardWipingOn': 7, 'Mode1_ForwardWipingOff': 8, 'Mode1_BackwardWipingOff': 9, 'Mode1_OutwardWipingOff': 10, 'Mode1_InwardWipingOff': 11, 'Mode1_ForwardScanning': 12, 'Mode1_BackwardScanning': 13, 'Mode1_BreathOn': 14, 'Mode1_BreathOff': 15, 'Mode1_Spare1': 16, 'Mode1_Spare2': 17}
        compute_method = None
        length = 5
        startbit = 13
        byte = 1
        mask = 0b00111110
        unmask = 0b11000001
        shift = 1

    class DwnLoadDynLtgPrmForLedLoBeamRiUpprBriPrm_1_CemBodyExpoSignalIPdu07:
        sig_name = "DwnLoadDynLtgPrmForLedLoBeamRiUpprBriPrm_1_CemBodyExpoSignalIPdu07"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForLedLoBeamRiOffsTiPrm_1_CemBodyExpoSignalIPdu07:
        sig_name = "DwnLoadDynLtgPrmForLedLoBeamRiOffsTiPrm_1_CemBodyExpoSignalIPdu07"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLtgPrmForLedLoBeamRiContTiPrm_1_CemBodyExpoSignalIPdu07:
        sig_name = "DwnLoadDynLtgPrmForLedLoBeamRiContTiPrm_1_CemBodyExpoSignalIPdu07"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLtgPrmForLedLoBeamRiTistamp_1_CemBodyExpoSignalIPdu07:
        sig_name = "DwnLoadDynLtgPrmForLedLoBeamRiTistamp_1_CemBodyExpoSignalIPdu07"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLtgPrmForLedLoBeamRiLowBriPrm_1_CemBodyExpoSignalIPdu07:
        sig_name = "DwnLoadDynLtgPrmForLedLoBeamRiLowBriPrm_1_CemBodyExpoSignalIPdu07"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class CemBodyExpoFr58:
    msg_name = "CemBodyExpoFr58"
    msg_id = 332
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RCMM']

    class DwnLoadDynLitPrmLedRePosnLampRi5UpprBriPrm_1_CemBodyExpoSignalIPdu58:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi5UpprBriPrm_1_CemBodyExpoSignalIPdu58"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmLedRePosnLampRi5Tistamp_1_CemBodyExpoSignalIPdu58:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi5Tistamp_1_CemBodyExpoSignalIPdu58"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmLedRePosnLampRi5LowBriPrm_1_CemBodyExpoSignalIPdu58:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi5LowBriPrm_1_CemBodyExpoSignalIPdu58"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmLedRePosnLampRi5ModePrm_1_CemBodyExpoSignalIPdu58:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi5ModePrm_1_CemBodyExpoSignalIPdu58"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode1_Off': 0, 'Mode1_On': 1, 'Mode1_GradualOn': 2, 'Mode1_GradualOff': 3, 'Mode1_ForwardWipingOn': 4, 'Mode1_BackwardWipingOn': 5, 'Mode1_OutwardWipingOn': 6, 'Mode1_InwardWipingOn': 7, 'Mode1_ForwardWipingOff': 8, 'Mode1_BackwardWipingOff': 9, 'Mode1_OutwardWipingOff': 10, 'Mode1_InwardWipingOff': 11, 'Mode1_ForwardScanning': 12, 'Mode1_BackwardScanning': 13, 'Mode1_BreathOn': 14, 'Mode1_BreathOff': 15, 'Mode1_Spare1': 16, 'Mode1_Spare2': 17}
        compute_method = None
        length = 5
        startbit = 13
        byte = 1
        mask = 0b00111110
        unmask = 0b11000001
        shift = 1

    class DwnLoadDynLitPrmLedRePosnLampRi5ContTiPrm_1_CemBodyExpoSignalIPdu58:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi5ContTiPrm_1_CemBodyExpoSignalIPdu58"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedRePosnLampRi5OffsTiPrm_1_CemBodyExpoSignalIPdu58:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi5OffsTiPrm_1_CemBodyExpoSignalIPdu58"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]


class BgmBodyExposedCANNmFr:
    msg_name = "BgmBodyExposedCANNmFr"
    msg_id = 1322
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RCMR']


class CemBodyExpoFr37:
    msg_name = "CemBodyExpoFr37"
    msg_id = 322
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR']

    class DwnLoadDynLtgPrmForLedFrntTurnIndcrRiOffsTiPrm_1_CemBodyExpoSignalIPdu37:
        sig_name = "DwnLoadDynLtgPrmForLedFrntTurnIndcrRiOffsTiPrm_1_CemBodyExpoSignalIPdu37"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLtgPrmForLedFrntTurnIndcrRiContTiPrm_1_CemBodyExpoSignalIPdu37:
        sig_name = "DwnLoadDynLtgPrmForLedFrntTurnIndcrRiContTiPrm_1_CemBodyExpoSignalIPdu37"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLtgPrmForLedFrntTurnIndcrRiLowBriPrm_1_CemBodyExpoSignalIPdu37:
        sig_name = "DwnLoadDynLtgPrmForLedFrntTurnIndcrRiLowBriPrm_1_CemBodyExpoSignalIPdu37"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForLedFrntTurnIndcrRiModePrm_1_CemBodyExpoSignalIPdu37:
        sig_name = "DwnLoadDynLtgPrmForLedFrntTurnIndcrRiModePrm_1_CemBodyExpoSignalIPdu37"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode1_Off': 0, 'Mode1_On': 1, 'Mode1_GradualOn': 2, 'Mode1_GradualOff': 3, 'Mode1_ForwardWipingOn': 4, 'Mode1_BackwardWipingOn': 5, 'Mode1_OutwardWipingOn': 6, 'Mode1_InwardWipingOn': 7, 'Mode1_ForwardWipingOff': 8, 'Mode1_BackwardWipingOff': 9, 'Mode1_OutwardWipingOff': 10, 'Mode1_InwardWipingOff': 11, 'Mode1_ForwardScanning': 12, 'Mode1_BackwardScanning': 13, 'Mode1_BreathOn': 14, 'Mode1_BreathOff': 15, 'Mode1_Spare1': 16, 'Mode1_Spare2': 17}
        compute_method = None
        length = 5
        startbit = 13
        byte = 1
        mask = 0b00111110
        unmask = 0b11000001
        shift = 1

    class DwnLoadDynLtgPrmForLedFrntTurnIndcrRiUpprBriPrm_1_CemBodyExpoSignalIPdu37:
        sig_name = "DwnLoadDynLtgPrmForLedFrntTurnIndcrRiUpprBriPrm_1_CemBodyExpoSignalIPdu37"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForLedFrntTurnIndcrRiTistamp_1_CemBodyExpoSignalIPdu37:
        sig_name = "DwnLoadDynLtgPrmForLedFrntTurnIndcrRiTistamp_1_CemBodyExpoSignalIPdu37"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]


class CemBodyExpoCommonFr17:
    msg_name = "CemBodyExpoCommonFr17"
    msg_id = 396
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.045
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR', 'HCML']

    class VehObjforADB5AdbTrkInfo_1_CemBodyExpoCommonSignalIPdu17:
        sig_name = "VehObjforADB5AdbTrkInfo_1_CemBodyExpoCommonSignalIPdu17"
        sig_start_bit = 48
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NotTracked': 0, 'Tracking': 1}
        compute_method = None
        length = 1
        startbit = 48
        byte = 6
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VehObjforADB5AdbObjHozlAgSpdLe_1_CemBodyExpoCommonSignalIPdu17:
        sig_name = "VehObjforADB5AdbObjHozlAgSpdLe_1_CemBodyExpoCommonSignalIPdu17"
        sig_start_bit = 34
        sig_length = 9
        sig_value_factor = 0.2
        sig_value_offset = "-50"
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 250
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 34
        bmuws_info = [(4, 0b00000111, 0b11111000, 3, 0), (5, 0b11111100, 0b00000011, 6, 2)]

    class VehObjforADB5AdbClassn_1_CemBodyExpoCommonSignalIPdu17:
        sig_name = "VehObjforADB5AdbClassn_1_CemBodyExpoCommonSignalIPdu17"
        sig_start_bit = 13
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AdbClassn_NoVehicle': 0, 'AdbClassn_Car': 1, 'AdbClassn_Truck': 2, 'AdbClassn_Bus': 3, 'AdbClassn_BikeOrMotorBike': 4, 'AdbClassn_Pedestrain': 5, 'AdbClassn_Mixed': 6, 'AdbClassn_Unknown': 7}
        compute_method = None
        length = 3
        startbit = 13
        byte = 1
        mask = 0b00111000
        unmask = 0b11000111
        shift = 3

    class VehObjforADB5AdbHozlAgRi_1_CemBodyExpoCommonSignalIPdu17:
        sig_name = "VehObjforADB5AdbHozlAgRi_1_CemBodyExpoCommonSignalIPdu17"
        sig_start_bit = 31
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = "-40"
        sig_value_min = 0
        sig_value_max = 1600
        sig_byteorder = "Motorola"
        sig_value_init = 800
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11100000, 0b00011111, 3, 5)]

    class VehObjforADB5AdbObjHozlAgSpdRi_1_CemBodyExpoCommonSignalIPdu17:
        sig_name = "VehObjforADB5AdbObjHozlAgSpdRi_1_CemBodyExpoCommonSignalIPdu17"
        sig_start_bit = 41
        sig_length = 9
        sig_value_factor = 0.2
        sig_value_offset = "-50"
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 250
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 41
        bmuws_info = [(5, 0b00000011, 0b11111100, 2, 0), (6, 0b11111110, 0b00000001, 7, 1)]

    class VehObjforADB5AdbHozlAgLe_1_CemBodyExpoCommonSignalIPdu17:
        sig_name = "VehObjforADB5AdbHozlAgLe_1_CemBodyExpoCommonSignalIPdu17"
        sig_start_bit = 10
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = "-40"
        sig_value_min = 0
        sig_value_max = 1600
        sig_byteorder = "Motorola"
        sig_value_init = 800
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 10
        bmuws_info = [(1, 0b00000111, 0b11111000, 3, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class VehObjforADB5AdbVertAg_1_CemBodyExpoCommonSignalIPdu17:
        sig_name = "VehObjforADB5AdbVertAg_1_CemBodyExpoCommonSignalIPdu17"
        sig_start_bit = 63
        sig_length = 5
        sig_value_factor = 0.5
        sig_value_offset = "-3"
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Motorola"
        sig_value_init = 6
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 63
        byte = 7
        mask = 0b11111000
        unmask = 0b00000111
        shift = 3

    class VehObjforADB5AdbAbsDist_1_CemBodyExpoCommonSignalIPdu17:
        sig_name = "VehObjforADB5AdbAbsDist_1_CemBodyExpoCommonSignalIPdu17"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class VehObjforADB5AdbObjDir_1_CemBodyExpoCommonSignalIPdu17:
        sig_name = "VehObjforADB5AdbObjDir_1_CemBodyExpoCommonSignalIPdu17"
        sig_start_bit = 36
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AdbObjDir_Idle': 0, 'AdbObjDir_Oncoming': 1, 'AdbObjDir_Preceding': 2, 'AdbObjDir_Others': 3}
        compute_method = None
        length = 2
        startbit = 36
        byte = 4
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3


class RcmrBodyExposedCANeNmFr:
    msg_name = "RcmrBodyExposedCANeNmFr"
    msg_id = 1332
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "RCMR"
    rx_nodes = ['HCML']


class CemBodyExpoFr55:
    msg_name = "CemBodyExpoFr55"
    msg_id = 329
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RCMM']

    class DwnLoadDynLitPrmLedRePosnLampLe5OffsTiPrm_1_CemBodyExpoSignalIPdu55:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe5OffsTiPrm_1_CemBodyExpoSignalIPdu55"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedRePosnLampLe5Tistamp_1_CemBodyExpoSignalIPdu55:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe5Tistamp_1_CemBodyExpoSignalIPdu55"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmLedRePosnLampLe5ContTiPrm_1_CemBodyExpoSignalIPdu55:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe5ContTiPrm_1_CemBodyExpoSignalIPdu55"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedRePosnLampLe5UpprBriPrm_1_CemBodyExpoSignalIPdu55:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe5UpprBriPrm_1_CemBodyExpoSignalIPdu55"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmLedRePosnLampLe5ModePrm_1_CemBodyExpoSignalIPdu55:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe5ModePrm_1_CemBodyExpoSignalIPdu55"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode1_Off': 0, 'Mode1_On': 1, 'Mode1_GradualOn': 2, 'Mode1_GradualOff': 3, 'Mode1_ForwardWipingOn': 4, 'Mode1_BackwardWipingOn': 5, 'Mode1_OutwardWipingOn': 6, 'Mode1_InwardWipingOn': 7, 'Mode1_ForwardWipingOff': 8, 'Mode1_BackwardWipingOff': 9, 'Mode1_OutwardWipingOff': 10, 'Mode1_InwardWipingOff': 11, 'Mode1_ForwardScanning': 12, 'Mode1_BackwardScanning': 13, 'Mode1_BreathOn': 14, 'Mode1_BreathOff': 15, 'Mode1_Spare1': 16, 'Mode1_Spare2': 17}
        compute_method = None
        length = 5
        startbit = 13
        byte = 1
        mask = 0b00111110
        unmask = 0b11000001
        shift = 1

    class DwnLoadDynLitPrmLedRePosnLampLe5LowBriPrm_1_CemBodyExpoSignalIPdu55:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe5LowBriPrm_1_CemBodyExpoSignalIPdu55"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class HcmltoEtcXCPFr01:
    msg_name = "HcmltoEtcXCPFr01"
    msg_id = 1424
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "HCML"
    rx_nodes = ['CCM']


class CemBodyExpoFr02:
    msg_name = "CemBodyExpoFr02"
    msg_id = 288
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RCMM']

    class DwnLoadDynLitPrmForLedStopLampRi2ContTiPrm_1_CemBodyExpoSignalIPdu02:
        sig_name = "DwnLoadDynLitPrmForLedStopLampRi2ContTiPrm_1_CemBodyExpoSignalIPdu02"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmForLedStopLampRi2LowBriPrm_1_CemBodyExpoSignalIPdu02:
        sig_name = "DwnLoadDynLitPrmForLedStopLampRi2LowBriPrm_1_CemBodyExpoSignalIPdu02"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmForLedStopLampRi2OffsTiPrm_1_CemBodyExpoSignalIPdu02:
        sig_name = "DwnLoadDynLitPrmForLedStopLampRi2OffsTiPrm_1_CemBodyExpoSignalIPdu02"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmForLedStopLampRi2ModePrm_1_CemBodyExpoSignalIPdu02:
        sig_name = "DwnLoadDynLitPrmForLedStopLampRi2ModePrm_1_CemBodyExpoSignalIPdu02"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode1_Off': 0, 'Mode1_On': 1, 'Mode1_GradualOn': 2, 'Mode1_GradualOff': 3, 'Mode1_ForwardWipingOn': 4, 'Mode1_BackwardWipingOn': 5, 'Mode1_OutwardWipingOn': 6, 'Mode1_InwardWipingOn': 7, 'Mode1_ForwardWipingOff': 8, 'Mode1_BackwardWipingOff': 9, 'Mode1_OutwardWipingOff': 10, 'Mode1_InwardWipingOff': 11, 'Mode1_ForwardScanning': 12, 'Mode1_BackwardScanning': 13, 'Mode1_BreathOn': 14, 'Mode1_BreathOff': 15, 'Mode1_Spare1': 16, 'Mode1_Spare2': 17}
        compute_method = None
        length = 5
        startbit = 13
        byte = 1
        mask = 0b00111110
        unmask = 0b11000001
        shift = 1

    class DwnLoadDynLitPrmForLedStopLampRi2UpprBriPrm_1_CemBodyExpoSignalIPdu02:
        sig_name = "DwnLoadDynLitPrmForLedStopLampRi2UpprBriPrm_1_CemBodyExpoSignalIPdu02"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmForLedStopLampRi2Tistamp_1_CemBodyExpoSignalIPdu02:
        sig_name = "DwnLoadDynLitPrmForLedStopLampRi2Tistamp_1_CemBodyExpoSignalIPdu02"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]


class CemBodyExpoFr09:
    msg_name = "CemBodyExpoFr09"
    msg_id = 295
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RCMR']

    class DwnLoadDynLitPrmForLedMkrLampRi1Tistamp_1_CemBodyExpoSignalIPdu09:
        sig_name = "DwnLoadDynLitPrmForLedMkrLampRi1Tistamp_1_CemBodyExpoSignalIPdu09"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmForLedMkrLampRi1UpprBriPrm_1_CemBodyExpoSignalIPdu09:
        sig_name = "DwnLoadDynLitPrmForLedMkrLampRi1UpprBriPrm_1_CemBodyExpoSignalIPdu09"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmForLedMkrLampRi1ContTiPrm_1_CemBodyExpoSignalIPdu09:
        sig_name = "DwnLoadDynLitPrmForLedMkrLampRi1ContTiPrm_1_CemBodyExpoSignalIPdu09"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmForLedMkrLampRi1LowBriPrm_1_CemBodyExpoSignalIPdu09:
        sig_name = "DwnLoadDynLitPrmForLedMkrLampRi1LowBriPrm_1_CemBodyExpoSignalIPdu09"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmForLedMkrLampRi1ModePrm_1_CemBodyExpoSignalIPdu09:
        sig_name = "DwnLoadDynLitPrmForLedMkrLampRi1ModePrm_1_CemBodyExpoSignalIPdu09"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode1_Off': 0, 'Mode1_On': 1, 'Mode1_GradualOn': 2, 'Mode1_GradualOff': 3, 'Mode1_ForwardWipingOn': 4, 'Mode1_BackwardWipingOn': 5, 'Mode1_OutwardWipingOn': 6, 'Mode1_InwardWipingOn': 7, 'Mode1_ForwardWipingOff': 8, 'Mode1_BackwardWipingOff': 9, 'Mode1_OutwardWipingOff': 10, 'Mode1_InwardWipingOff': 11, 'Mode1_ForwardScanning': 12, 'Mode1_BackwardScanning': 13, 'Mode1_BreathOn': 14, 'Mode1_BreathOff': 15, 'Mode1_Spare1': 16, 'Mode1_Spare2': 17}
        compute_method = None
        length = 5
        startbit = 13
        byte = 1
        mask = 0b00111110
        unmask = 0b11000001
        shift = 1

    class DwnLoadDynLitPrmForLedMkrLampRi1OffsTiPrm_1_CemBodyExpoSignalIPdu09:
        sig_name = "DwnLoadDynLitPrmForLedMkrLampRi1OffsTiPrm_1_CemBodyExpoSignalIPdu09"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]


class BgmToAllFuncBodyExpoDiagReqFrame:
    msg_name = "BgmToAllFuncBodyExpoDiagReqFrame"
    msg_id = 2047
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR', 'RCMR', 'HCML', 'RCMM', 'PCM', 'RCML']


class CemBodyExpoFr78:
    msg_name = "CemBodyExpoFr78"
    msg_id = 812
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCML']

    class DwnLoadDynLtgPrmForFrntLeGrp12ContinueTime_1_CemBodyExpoSignalIPdu78:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp12ContinueTime_1_CemBodyExpoSignalIPdu78"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForFrntLeGrp12Mode1_1_CemBodyExpoSignalIPdu78:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp12Mode1_1_CemBodyExpoSignalIPdu78"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode4_Off': 0, 'Mode4_On': 1, 'Mode4_GradualOn': 2, 'Mode4_GradualOff': 3, 'Mode4_ForwardWipingOn': 4, 'Mode4_BackwardWipingOn': 5, 'Mode4_OutwardWipingOn': 6, 'Mode4_InwardWipingOn': 7, 'Mode4_ForwardWipingOff': 8, 'Mode4_BackwardWipingOff': 9, 'Mode4_OutwardWipingOff': 10, 'Mode4_InwardWipingOff': 11, 'Mode4_ForwardScanning': 12, 'Mode4_BackwardScanning': 13, 'Mode4_BreathOn': 14, 'Mode4_BreathOff': 15, 'Mode4_1stHalfONand2ndHalfOFF': 16, 'Mode4_HalfOFFHalfON': 17, 'Mode4_HalfDimmingONHalfOFF': 18, 'Mode4_HalfDimmingONHalfON': 19, 'Mode4_HalfOFFHalfDimmingON': 20, 'Mode4_HalfONHalfDimmingON': 21, 'Mode4_HalfDimmingOFFHalfOFF': 22, 'Mode4_HalfDimmingOFFHalfON': 23, 'Mode4_HalfOFFHalfDimmingOFF': 24, 'Mode4_HalfONHalfDimmingOFF': 25, 'Mode4_SingleOn1': 26, 'Mode4_SingleOn2': 27, 'Mode4_SingleOn3': 28, 'Mode4_SingleOn4': 29, 'Mode4_SingleOn5': 30, 'Mode4_SingleOn6': 31, 'Mode4_SingleOn7': 32, 'Mode4_SingleOn8': 33, 'Mode4_SingleOn9': 34, 'Mode4_SingleOn10': 35, 'Mode4_SingleOn11': 36, 'Mode4_SingleOn12': 37, 'Mode4_SingleOff1': 38, 'Mode4_SingleOff2': 39, 'Mode4_SingleOff3': 40, 'Mode4_SingleOff4': 41, 'Mode4_SingleOff5': 42, 'Mode4_SingleOff6': 43, 'Mode4_SingleOff7': 44, 'Mode4_SingleOff8': 45, 'Mode4_SingleOff9': 46, 'Mode4_SingleOff10': 47, 'Mode4_SingleOff11': 48, 'Mode4_SingleOff12': 49}
        compute_method = None
        length = 6
        startbit = 23
        byte = 2
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntLeGrp12OffsetTime_1_CemBodyExpoSignalIPdu78:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp12OffsetTime_1_CemBodyExpoSignalIPdu78"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 31
        byte = 3
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntLeGrp12Timestamp_1_CemBodyExpoSignalIPdu78:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp12Timestamp_1_CemBodyExpoSignalIPdu78"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DwnLoadDynLtgPrmForFrntLeGrp12LowBrightness_1_CemBodyExpoSignalIPdu78:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp12LowBrightness_1_CemBodyExpoSignalIPdu78"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DwnLoadDynLtgPrmForFrntLeGrp12HighBrightness_1_CemBodyExpoSignalIPdu78:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp12HighBrightness_1_CemBodyExpoSignalIPdu78"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4


class CemBodyExpoFr82:
    msg_name = "CemBodyExpoFr82"
    msg_id = 816
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCML']

    class DwnLoadDynLtgPrmForFrntLeGrp16Timestamp_1_CemBodyExpoSignalIPdu82:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp16Timestamp_1_CemBodyExpoSignalIPdu82"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DwnLoadDynLtgPrmForFrntLeGrp16OffsetTime_1_CemBodyExpoSignalIPdu82:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp16OffsetTime_1_CemBodyExpoSignalIPdu82"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 31
        byte = 3
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntLeGrp16ContinueTime_1_CemBodyExpoSignalIPdu82:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp16ContinueTime_1_CemBodyExpoSignalIPdu82"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForFrntLeGrp16HighBrightness_1_CemBodyExpoSignalIPdu82:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp16HighBrightness_1_CemBodyExpoSignalIPdu82"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DwnLoadDynLtgPrmForFrntLeGrp16Mode1_1_CemBodyExpoSignalIPdu82:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp16Mode1_1_CemBodyExpoSignalIPdu82"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode4_Off': 0, 'Mode4_On': 1, 'Mode4_GradualOn': 2, 'Mode4_GradualOff': 3, 'Mode4_ForwardWipingOn': 4, 'Mode4_BackwardWipingOn': 5, 'Mode4_OutwardWipingOn': 6, 'Mode4_InwardWipingOn': 7, 'Mode4_ForwardWipingOff': 8, 'Mode4_BackwardWipingOff': 9, 'Mode4_OutwardWipingOff': 10, 'Mode4_InwardWipingOff': 11, 'Mode4_ForwardScanning': 12, 'Mode4_BackwardScanning': 13, 'Mode4_BreathOn': 14, 'Mode4_BreathOff': 15, 'Mode4_1stHalfONand2ndHalfOFF': 16, 'Mode4_HalfOFFHalfON': 17, 'Mode4_HalfDimmingONHalfOFF': 18, 'Mode4_HalfDimmingONHalfON': 19, 'Mode4_HalfOFFHalfDimmingON': 20, 'Mode4_HalfONHalfDimmingON': 21, 'Mode4_HalfDimmingOFFHalfOFF': 22, 'Mode4_HalfDimmingOFFHalfON': 23, 'Mode4_HalfOFFHalfDimmingOFF': 24, 'Mode4_HalfONHalfDimmingOFF': 25, 'Mode4_SingleOn1': 26, 'Mode4_SingleOn2': 27, 'Mode4_SingleOn3': 28, 'Mode4_SingleOn4': 29, 'Mode4_SingleOn5': 30, 'Mode4_SingleOn6': 31, 'Mode4_SingleOn7': 32, 'Mode4_SingleOn8': 33, 'Mode4_SingleOn9': 34, 'Mode4_SingleOn10': 35, 'Mode4_SingleOn11': 36, 'Mode4_SingleOn12': 37, 'Mode4_SingleOff1': 38, 'Mode4_SingleOff2': 39, 'Mode4_SingleOff3': 40, 'Mode4_SingleOff4': 41, 'Mode4_SingleOff5': 42, 'Mode4_SingleOff6': 43, 'Mode4_SingleOff7': 44, 'Mode4_SingleOff8': 45, 'Mode4_SingleOff9': 46, 'Mode4_SingleOff10': 47, 'Mode4_SingleOff11': 48, 'Mode4_SingleOff12': 49}
        compute_method = None
        length = 6
        startbit = 23
        byte = 2
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntLeGrp16LowBrightness_1_CemBodyExpoSignalIPdu82:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp16LowBrightness_1_CemBodyExpoSignalIPdu82"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0


class HcmrBodyExposedCANNmFr:
    msg_name = "HcmrBodyExposedCANNmFr"
    msg_id = 1330
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "HCMR"
    rx_nodes = ['BGM']


class CemBodyExpoFr42:
    msg_name = "CemBodyExpoFr42"
    msg_id = 381
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.065
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR', 'RCMR', 'HCML', 'RCMM', 'RCML']

    class AgDataRawSafeRollRate_1_CemBodyExpoSignalIPdu42:
        sig_name = "AgDataRawSafeRollRate_1_CemBodyExpoSignalIPdu42"
        sig_start_bit = 7
        sig_length = 16
        sig_value_factor = "2.44140625E-4"
        sig_value_offset = 0.0
        sig_value_min = -24576
        sig_value_max = 24576
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class AgDataRawSafeRollRateQf_1_CemBodyExpoSignalIPdu42:
        sig_name = "AgDataRawSafeRollRateQf_1_CemBodyExpoSignalIPdu42"
        sig_start_bit = 43
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Qf1_DevOfDataUndefd': 0, 'Qf1_DataTmpUndefdAndEvlnInProgs': 1, 'Qf1_DevOfDataNotWithinRngAllwd': 2, 'Qf1_DataCalcdWithDevDefd': 3}
        compute_method = None
        length = 2
        startbit = 43
        byte = 5
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class AgDataRawSafeYawRate_1_CemBodyExpoSignalIPdu42:
        sig_name = "AgDataRawSafeYawRate_1_CemBodyExpoSignalIPdu42"
        sig_start_bit = 23
        sig_length = 16
        sig_value_factor = "2.44140625E-4"
        sig_value_offset = 0.0
        sig_value_min = -24576
        sig_value_max = 24576
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class ActnOfLedGrilleLampDyn:
        sig_name = "ActnOfLedGrilleLampDyn"
        sig_start_bit = 50
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 50
        byte = 6
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class AgDataRawSafeYawRateQf_1_CemBodyExpoSignalIPdu42:
        sig_name = "AgDataRawSafeYawRateQf_1_CemBodyExpoSignalIPdu42"
        sig_start_bit = 41
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Qf1_DevOfDataUndefd': 0, 'Qf1_DataTmpUndefdAndEvlnInProgs': 1, 'Qf1_DevOfDataNotWithinRngAllwd': 2, 'Qf1_DataCalcdWithDevDefd': 3}
        compute_method = None
        length = 2
        startbit = 41
        byte = 5
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class AgDataRawSafeChks_1_CemBodyExpoSignalIPdu42:
        sig_name = "AgDataRawSafeChks_1_CemBodyExpoSignalIPdu42"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 255
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ActnOfLedPosnLampDyn:
        sig_name = "ActnOfLedPosnLampDyn"
        sig_start_bit = 53
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 53
        byte = 6
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class AgDataRawSafeCntr_1_CemBodyExpoSignalIPdu42:
        sig_name = "AgDataRawSafeCntr_1_CemBodyExpoSignalIPdu42"
        sig_start_bit = 47
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 47
        byte = 5
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4


class CemBodyExpoFr102:
    msg_name = "CemBodyExpoFr102"
    msg_id = 836
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR']

    class DwnLoadDynLtgPrmForFrntRIGrp12Timestamp_1_CemBodyExpoSignalIPdu102:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp12Timestamp_1_CemBodyExpoSignalIPdu102"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DwnLoadDynLtgPrmForFrntRIGrp12OffsetTime_1_CemBodyExpoSignalIPdu102:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp12OffsetTime_1_CemBodyExpoSignalIPdu102"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 31
        byte = 3
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntRIGrp12ContinueTime_1_CemBodyExpoSignalIPdu102:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp12ContinueTime_1_CemBodyExpoSignalIPdu102"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForFrntRIGrp12Mode1_1_CemBodyExpoSignalIPdu102:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp12Mode1_1_CemBodyExpoSignalIPdu102"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode4_Off': 0, 'Mode4_On': 1, 'Mode4_GradualOn': 2, 'Mode4_GradualOff': 3, 'Mode4_ForwardWipingOn': 4, 'Mode4_BackwardWipingOn': 5, 'Mode4_OutwardWipingOn': 6, 'Mode4_InwardWipingOn': 7, 'Mode4_ForwardWipingOff': 8, 'Mode4_BackwardWipingOff': 9, 'Mode4_OutwardWipingOff': 10, 'Mode4_InwardWipingOff': 11, 'Mode4_ForwardScanning': 12, 'Mode4_BackwardScanning': 13, 'Mode4_BreathOn': 14, 'Mode4_BreathOff': 15, 'Mode4_1stHalfONand2ndHalfOFF': 16, 'Mode4_HalfOFFHalfON': 17, 'Mode4_HalfDimmingONHalfOFF': 18, 'Mode4_HalfDimmingONHalfON': 19, 'Mode4_HalfOFFHalfDimmingON': 20, 'Mode4_HalfONHalfDimmingON': 21, 'Mode4_HalfDimmingOFFHalfOFF': 22, 'Mode4_HalfDimmingOFFHalfON': 23, 'Mode4_HalfOFFHalfDimmingOFF': 24, 'Mode4_HalfONHalfDimmingOFF': 25, 'Mode4_SingleOn1': 26, 'Mode4_SingleOn2': 27, 'Mode4_SingleOn3': 28, 'Mode4_SingleOn4': 29, 'Mode4_SingleOn5': 30, 'Mode4_SingleOn6': 31, 'Mode4_SingleOn7': 32, 'Mode4_SingleOn8': 33, 'Mode4_SingleOn9': 34, 'Mode4_SingleOn10': 35, 'Mode4_SingleOn11': 36, 'Mode4_SingleOn12': 37, 'Mode4_SingleOff1': 38, 'Mode4_SingleOff2': 39, 'Mode4_SingleOff3': 40, 'Mode4_SingleOff4': 41, 'Mode4_SingleOff5': 42, 'Mode4_SingleOff6': 43, 'Mode4_SingleOff7': 44, 'Mode4_SingleOff8': 45, 'Mode4_SingleOff9': 46, 'Mode4_SingleOff10': 47, 'Mode4_SingleOff11': 48, 'Mode4_SingleOff12': 49}
        compute_method = None
        length = 6
        startbit = 23
        byte = 2
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntRIGrp12HighBrightness_1_CemBodyExpoSignalIPdu102:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp12HighBrightness_1_CemBodyExpoSignalIPdu102"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DwnLoadDynLtgPrmForFrntRIGrp12LowBrightness_1_CemBodyExpoSignalIPdu102:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp12LowBrightness_1_CemBodyExpoSignalIPdu102"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0


class HcmrBodyExpoFr02:
    msg_name = "HcmrBodyExpoFr02"
    msg_id = 594
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 3
    tx_node = "HCMR"
    rx_nodes = ['BGM']

    class StsOfLedHiBeamRi:
        sig_name = "StsOfLedHiBeamRi"
        sig_start_bit = 1
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class ExtrLiShowStoreStsFrntRi_0_HcmrBodyExpoSignalIPdu02:
        sig_name = "ExtrLiShowStoreStsFrntRi_0_HcmrBodyExpoSignalIPdu02"
        sig_start_bit = 7
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class StsOfLedLoBeamRi:
        sig_name = "StsOfLedLoBeamRi"
        sig_start_bit = 4
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 4
        byte = 0
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3


class RcmmBodyExpoFr02:
    msg_name = "RcmmBodyExpoFr02"
    msg_id = 596
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 8
    tx_node = "RCMM"
    rx_nodes = ['BGM']

    class StsOfLedRvsgLampLe2:
        sig_name = "StsOfLedRvsgLampLe2"
        sig_start_bit = 21
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 21
        byte = 2
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class StsOfLedTurnIndcrRi2:
        sig_name = "StsOfLedTurnIndcrRi2"
        sig_start_bit = 31
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 31
        byte = 3
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class StsOfLedReFogLampRi2:
        sig_name = "StsOfLedReFogLampRi2"
        sig_start_bit = 15
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 15
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class StsOfLedReFogLampLe2:
        sig_name = "StsOfLedReFogLampLe2"
        sig_start_bit = 13
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 13
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class ExtrLiShowActvnReLe2Fb:
        sig_name = "ExtrLiShowActvnReLe2Fb"
        sig_start_bit = 5
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Sts_Resd': 0, 'Sts_Err': 1, 'Sts_CmplOk': 2, 'Sts_InProgs': 3}
        compute_method = None
        length = 2
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class ExtrLiShowStoreStsReRi2_0_RcmmBodyExpoSignalIPdu02:
        sig_name = "ExtrLiShowStoreStsReRi2_0_RcmmBodyExpoSignalIPdu02"
        sig_start_bit = 49
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 49
        byte = 6
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class StsOfLedStopLampLe2:
        sig_name = "StsOfLedStopLampLe2"
        sig_start_bit = 25
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 25
        byte = 3
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class StsOfLedTurnIndcrLe2:
        sig_name = "StsOfLedTurnIndcrLe2"
        sig_start_bit = 29
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 29
        byte = 3
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class StsOfLedPosnLampLe2:
        sig_name = "StsOfLedPosnLampLe2"
        sig_start_bit = 9
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 9
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class StsOfLedStopLampRi2:
        sig_name = "StsOfLedStopLampRi2"
        sig_start_bit = 27
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 27
        byte = 3
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class StsOfLedReLampRi2:
        sig_name = "StsOfLedReLampRi2"
        sig_start_bit = 19
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 19
        byte = 2
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class StsOfWelGbyReRi2:
        sig_name = "StsOfWelGbyReRi2"
        sig_start_bit = 53
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 53
        byte = 6
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class ExtrLiShowStoreStsReLe2_0_RcmmBodyExpoSignalIPdu02:
        sig_name = "ExtrLiShowStoreStsReLe2_0_RcmmBodyExpoSignalIPdu02"
        sig_start_bit = 51
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 51
        byte = 6
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class StsOfWelGbyReLe2:
        sig_name = "StsOfWelGbyReLe2"
        sig_start_bit = 55
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 55
        byte = 6
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ExtrLiShowActvnReRi2Fb:
        sig_name = "ExtrLiShowActvnReRi2Fb"
        sig_start_bit = 7
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Sts_Resd': 0, 'Sts_Err': 1, 'Sts_CmplOk': 2, 'Sts_InProgs': 3}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class StsOfLedPosnLampRi2:
        sig_name = "StsOfLedPosnLampRi2"
        sig_start_bit = 11
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 11
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class StsOfLedRvsgLampRi2:
        sig_name = "StsOfLedRvsgLampRi2"
        sig_start_bit = 23
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 23
        byte = 2
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class DwnLoadStsFbOfReLampCtrlRi2:
        sig_name = "DwnLoadStsFbOfReLampCtrlRi2"
        sig_start_bit = 3
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Sts_Resd': 0, 'Sts_Err': 1, 'Sts_CmplOk': 2, 'Sts_InProgs': 3}
        compute_method = None
        length = 2
        startbit = 3
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class DwnLoadStsFbOfReLampCtrlLe2:
        sig_name = "DwnLoadStsFbOfReLampCtrlLe2"
        sig_start_bit = 1
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Sts_Resd': 0, 'Sts_Err': 1, 'Sts_CmplOk': 2, 'Sts_InProgs': 3}
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class StsOfLedReLampLe2:
        sig_name = "StsOfLedReLampLe2"
        sig_start_bit = 17
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 17
        byte = 2
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0


class CemBodyExpoFr50:
    msg_name = "CemBodyExpoFr50"
    msg_id = 522
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR', 'RCMR', 'HCML', 'RCMM', 'RCML']

    class ActnOfLedStopLampChks:
        sig_name = "ActnOfLedStopLampChks"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ActvnOfGoodByeLi_1_CemBodyExpoSignalIPdu50:
        sig_name = "ActvnOfGoodByeLi_1_CemBodyExpoSignalIPdu50"
        sig_start_bit = 54
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 54
        byte = 6
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class ActnOfLedStopLampActnOfLedStopLamp:
        sig_name = "ActnOfLedStopLampActnOfLedStopLamp"
        sig_start_bit = 20
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 20
        byte = 2
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class ActnOfLedPosnLamp:
        sig_name = "ActnOfLedPosnLamp"
        sig_start_bit = 38
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 38
        byte = 4
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class ActvnOfAhbc:
        sig_name = "ActvnOfAhbc"
        sig_start_bit = 46
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 46
        byte = 5
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class ActvnOfBrkLi:
        sig_name = "ActvnOfBrkLi"
        sig_start_bit = 50
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 50
        byte = 6
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class ActnOfLedDaytiRunngLamp:
        sig_name = "ActnOfLedDaytiRunngLamp"
        sig_start_bit = 32
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 32
        byte = 4
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ActvnOfAhl:
        sig_name = "ActvnOfAhl"
        sig_start_bit = 48
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 48
        byte = 6
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ActnOfLedLoBeamChks:
        sig_name = "ActnOfLedLoBeamChks"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ActnOfLedHiBeam:
        sig_name = "ActnOfLedHiBeam"
        sig_start_bit = 36
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 36
        byte = 4
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class ActvnOfDbl:
        sig_name = "ActvnOfDbl"
        sig_start_bit = 52
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class ActnOfLedCornrgLampRi:
        sig_name = "ActnOfLedCornrgLampRi"
        sig_start_bit = 22
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 22
        byte = 2
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class ActnOfLedReFogLamp:
        sig_name = "ActnOfLedReFogLamp"
        sig_start_bit = 40
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 40
        byte = 5
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ActnOfLedFrntFogLamp:
        sig_name = "ActnOfLedFrntFogLamp"
        sig_start_bit = 34
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 34
        byte = 4
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class ActnOfLedRvsgLamp:
        sig_name = "ActnOfLedRvsgLamp"
        sig_start_bit = 42
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 42
        byte = 5
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class ActvnOfTouristMod:
        sig_name = "ActvnOfTouristMod"
        sig_start_bit = 56
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 56
        byte = 7
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ActnOfLedLoBeamActnOfLedLoBeam:
        sig_name = "ActnOfLedLoBeamActnOfLedLoBeam"
        sig_start_bit = 4
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 4
        byte = 0
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class ActnOfLedLoBeamCntr:
        sig_name = "ActnOfLedLoBeamCntr"
        sig_start_bit = 3
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 3
        byte = 0
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class ActnOfLedCornrgLampLe:
        sig_name = "ActnOfLedCornrgLampLe"
        sig_start_bit = 6
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class ActvnOfAfs:
        sig_name = "ActvnOfAfs"
        sig_start_bit = 44
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 44
        byte = 5
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class ActnOfLedStopLampCntr:
        sig_name = "ActnOfLedStopLampCntr"
        sig_start_bit = 19
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 19
        byte = 2
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class ActvnOfWelcomeLi_1_CemBodyExpoSignalIPdu50:
        sig_name = "ActvnOfWelcomeLi_1_CemBodyExpoSignalIPdu50"
        sig_start_bit = 58
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 58
        byte = 7
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2


class CemBodyExpoFr99:
    msg_name = "CemBodyExpoFr99"
    msg_id = 833
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR']

    class DwnLoadDynLtgPrmForFrntRIGrp9LowBrightness_1_CemBodyExpoSignalIPdu99:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp9LowBrightness_1_CemBodyExpoSignalIPdu99"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DwnLoadDynLtgPrmForFrntRIGrp9ContinueTime_1_CemBodyExpoSignalIPdu99:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp9ContinueTime_1_CemBodyExpoSignalIPdu99"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForFrntRIGrp9Timestamp_1_CemBodyExpoSignalIPdu99:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp9Timestamp_1_CemBodyExpoSignalIPdu99"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DwnLoadDynLtgPrmForFrntRIGrp9Mode1_1_CemBodyExpoSignalIPdu99:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp9Mode1_1_CemBodyExpoSignalIPdu99"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode4_Off': 0, 'Mode4_On': 1, 'Mode4_GradualOn': 2, 'Mode4_GradualOff': 3, 'Mode4_ForwardWipingOn': 4, 'Mode4_BackwardWipingOn': 5, 'Mode4_OutwardWipingOn': 6, 'Mode4_InwardWipingOn': 7, 'Mode4_ForwardWipingOff': 8, 'Mode4_BackwardWipingOff': 9, 'Mode4_OutwardWipingOff': 10, 'Mode4_InwardWipingOff': 11, 'Mode4_ForwardScanning': 12, 'Mode4_BackwardScanning': 13, 'Mode4_BreathOn': 14, 'Mode4_BreathOff': 15, 'Mode4_1stHalfONand2ndHalfOFF': 16, 'Mode4_HalfOFFHalfON': 17, 'Mode4_HalfDimmingONHalfOFF': 18, 'Mode4_HalfDimmingONHalfON': 19, 'Mode4_HalfOFFHalfDimmingON': 20, 'Mode4_HalfONHalfDimmingON': 21, 'Mode4_HalfDimmingOFFHalfOFF': 22, 'Mode4_HalfDimmingOFFHalfON': 23, 'Mode4_HalfOFFHalfDimmingOFF': 24, 'Mode4_HalfONHalfDimmingOFF': 25, 'Mode4_SingleOn1': 26, 'Mode4_SingleOn2': 27, 'Mode4_SingleOn3': 28, 'Mode4_SingleOn4': 29, 'Mode4_SingleOn5': 30, 'Mode4_SingleOn6': 31, 'Mode4_SingleOn7': 32, 'Mode4_SingleOn8': 33, 'Mode4_SingleOn9': 34, 'Mode4_SingleOn10': 35, 'Mode4_SingleOn11': 36, 'Mode4_SingleOn12': 37, 'Mode4_SingleOff1': 38, 'Mode4_SingleOff2': 39, 'Mode4_SingleOff3': 40, 'Mode4_SingleOff4': 41, 'Mode4_SingleOff5': 42, 'Mode4_SingleOff6': 43, 'Mode4_SingleOff7': 44, 'Mode4_SingleOff8': 45, 'Mode4_SingleOff9': 46, 'Mode4_SingleOff10': 47, 'Mode4_SingleOff11': 48, 'Mode4_SingleOff12': 49}
        compute_method = None
        length = 6
        startbit = 23
        byte = 2
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntRIGrp9HighBrightness_1_CemBodyExpoSignalIPdu99:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp9HighBrightness_1_CemBodyExpoSignalIPdu99"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DwnLoadDynLtgPrmForFrntRIGrp9OffsetTime_1_CemBodyExpoSignalIPdu99:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp9OffsetTime_1_CemBodyExpoSignalIPdu99"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 31
        byte = 3
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2


class CemBodyExpoFr35:
    msg_name = "CemBodyExpoFr35"
    msg_id = 320
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR']

    class DwnLoadDynLtgPrmForLedFrntPosnLampRiOffsTiPrm_1_CemBodyExpoSignalIPdu35:
        sig_name = "DwnLoadDynLtgPrmForLedFrntPosnLampRiOffsTiPrm_1_CemBodyExpoSignalIPdu35"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLtgPrmForLedFrntPosnLampRiContTiPrm_1_CemBodyExpoSignalIPdu35:
        sig_name = "DwnLoadDynLtgPrmForLedFrntPosnLampRiContTiPrm_1_CemBodyExpoSignalIPdu35"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLtgPrmForLedFrntPosnLampRiModePrm_1_CemBodyExpoSignalIPdu35:
        sig_name = "DwnLoadDynLtgPrmForLedFrntPosnLampRiModePrm_1_CemBodyExpoSignalIPdu35"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode1_Off': 0, 'Mode1_On': 1, 'Mode1_GradualOn': 2, 'Mode1_GradualOff': 3, 'Mode1_ForwardWipingOn': 4, 'Mode1_BackwardWipingOn': 5, 'Mode1_OutwardWipingOn': 6, 'Mode1_InwardWipingOn': 7, 'Mode1_ForwardWipingOff': 8, 'Mode1_BackwardWipingOff': 9, 'Mode1_OutwardWipingOff': 10, 'Mode1_InwardWipingOff': 11, 'Mode1_ForwardScanning': 12, 'Mode1_BackwardScanning': 13, 'Mode1_BreathOn': 14, 'Mode1_BreathOff': 15, 'Mode1_Spare1': 16, 'Mode1_Spare2': 17}
        compute_method = None
        length = 5
        startbit = 13
        byte = 1
        mask = 0b00111110
        unmask = 0b11000001
        shift = 1

    class DwnLoadDynLtgPrmForLedFrntPosnLampRiUpprBriPrm_1_CemBodyExpoSignalIPdu35:
        sig_name = "DwnLoadDynLtgPrmForLedFrntPosnLampRiUpprBriPrm_1_CemBodyExpoSignalIPdu35"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForLedFrntPosnLampRiLowBriPrm_1_CemBodyExpoSignalIPdu35:
        sig_name = "DwnLoadDynLtgPrmForLedFrntPosnLampRiLowBriPrm_1_CemBodyExpoSignalIPdu35"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForLedFrntPosnLampRiTistamp_1_CemBodyExpoSignalIPdu35:
        sig_name = "DwnLoadDynLtgPrmForLedFrntPosnLampRiTistamp_1_CemBodyExpoSignalIPdu35"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]


class CemBodyExpoFr15:
    msg_name = "CemBodyExpoFr15"
    msg_id = 301
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RCMR']

    class DwnLoadDynLitPrmLedReFogLampRi1LowBriPrm_1_CemBodyExpoSignalIPdu15:
        sig_name = "DwnLoadDynLitPrmLedReFogLampRi1LowBriPrm_1_CemBodyExpoSignalIPdu15"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmLedReFogLampRi1ModePrm_1_CemBodyExpoSignalIPdu15:
        sig_name = "DwnLoadDynLitPrmLedReFogLampRi1ModePrm_1_CemBodyExpoSignalIPdu15"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode1_Off': 0, 'Mode1_On': 1, 'Mode1_GradualOn': 2, 'Mode1_GradualOff': 3, 'Mode1_ForwardWipingOn': 4, 'Mode1_BackwardWipingOn': 5, 'Mode1_OutwardWipingOn': 6, 'Mode1_InwardWipingOn': 7, 'Mode1_ForwardWipingOff': 8, 'Mode1_BackwardWipingOff': 9, 'Mode1_OutwardWipingOff': 10, 'Mode1_InwardWipingOff': 11, 'Mode1_ForwardScanning': 12, 'Mode1_BackwardScanning': 13, 'Mode1_BreathOn': 14, 'Mode1_BreathOff': 15, 'Mode1_Spare1': 16, 'Mode1_Spare2': 17}
        compute_method = None
        length = 5
        startbit = 13
        byte = 1
        mask = 0b00111110
        unmask = 0b11000001
        shift = 1

    class DwnLoadDynLitPrmLedReFogLampRi1OffsTiPrm_1_CemBodyExpoSignalIPdu15:
        sig_name = "DwnLoadDynLitPrmLedReFogLampRi1OffsTiPrm_1_CemBodyExpoSignalIPdu15"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedReFogLampRi1ContTiPrm_1_CemBodyExpoSignalIPdu15:
        sig_name = "DwnLoadDynLitPrmLedReFogLampRi1ContTiPrm_1_CemBodyExpoSignalIPdu15"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedReFogLampRi1Tistamp_1_CemBodyExpoSignalIPdu15:
        sig_name = "DwnLoadDynLitPrmLedReFogLampRi1Tistamp_1_CemBodyExpoSignalIPdu15"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmLedReFogLampRi1UpprBriPrm_1_CemBodyExpoSignalIPdu15:
        sig_name = "DwnLoadDynLitPrmLedReFogLampRi1UpprBriPrm_1_CemBodyExpoSignalIPdu15"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class CemBodyExpoFr71:
    msg_name = "CemBodyExpoFr71"
    msg_id = 805
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCML']

    class DwnLoadDynLtgPrmForFrntLeGrp5LowBrightness_1_CemBodyExpoSignalIPdu71:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp5LowBrightness_1_CemBodyExpoSignalIPdu71"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DwnLoadDynLtgPrmForFrntLeGrp5ContinueTime_1_CemBodyExpoSignalIPdu71:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp5ContinueTime_1_CemBodyExpoSignalIPdu71"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForFrntLeGrp5Timestamp_1_CemBodyExpoSignalIPdu71:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp5Timestamp_1_CemBodyExpoSignalIPdu71"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DwnLoadDynLtgPrmForFrntLeGrp5OffsetTime_1_CemBodyExpoSignalIPdu71:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp5OffsetTime_1_CemBodyExpoSignalIPdu71"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 31
        byte = 3
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntLeGrp5HighBrightness_1_CemBodyExpoSignalIPdu71:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp5HighBrightness_1_CemBodyExpoSignalIPdu71"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DwnLoadDynLtgPrmForFrntLeGrp5Mode1_1_CemBodyExpoSignalIPdu71:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp5Mode1_1_CemBodyExpoSignalIPdu71"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode4_Off': 0, 'Mode4_On': 1, 'Mode4_GradualOn': 2, 'Mode4_GradualOff': 3, 'Mode4_ForwardWipingOn': 4, 'Mode4_BackwardWipingOn': 5, 'Mode4_OutwardWipingOn': 6, 'Mode4_InwardWipingOn': 7, 'Mode4_ForwardWipingOff': 8, 'Mode4_BackwardWipingOff': 9, 'Mode4_OutwardWipingOff': 10, 'Mode4_InwardWipingOff': 11, 'Mode4_ForwardScanning': 12, 'Mode4_BackwardScanning': 13, 'Mode4_BreathOn': 14, 'Mode4_BreathOff': 15, 'Mode4_1stHalfONand2ndHalfOFF': 16, 'Mode4_HalfOFFHalfON': 17, 'Mode4_HalfDimmingONHalfOFF': 18, 'Mode4_HalfDimmingONHalfON': 19, 'Mode4_HalfOFFHalfDimmingON': 20, 'Mode4_HalfONHalfDimmingON': 21, 'Mode4_HalfDimmingOFFHalfOFF': 22, 'Mode4_HalfDimmingOFFHalfON': 23, 'Mode4_HalfOFFHalfDimmingOFF': 24, 'Mode4_HalfONHalfDimmingOFF': 25, 'Mode4_SingleOn1': 26, 'Mode4_SingleOn2': 27, 'Mode4_SingleOn3': 28, 'Mode4_SingleOn4': 29, 'Mode4_SingleOn5': 30, 'Mode4_SingleOn6': 31, 'Mode4_SingleOn7': 32, 'Mode4_SingleOn8': 33, 'Mode4_SingleOn9': 34, 'Mode4_SingleOn10': 35, 'Mode4_SingleOn11': 36, 'Mode4_SingleOn12': 37, 'Mode4_SingleOff1': 38, 'Mode4_SingleOff2': 39, 'Mode4_SingleOff3': 40, 'Mode4_SingleOff4': 41, 'Mode4_SingleOff5': 42, 'Mode4_SingleOff6': 43, 'Mode4_SingleOff7': 44, 'Mode4_SingleOff8': 45, 'Mode4_SingleOff9': 46, 'Mode4_SingleOff10': 47, 'Mode4_SingleOff11': 48, 'Mode4_SingleOff12': 49}
        compute_method = None
        length = 6
        startbit = 23
        byte = 2
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2


class CemBodyExpoFr23:
    msg_name = "CemBodyExpoFr23"
    msg_id = 309
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RCMM']

    class DwnLoadDynLitPrmLedRvsgLampLe2LowBriPrm_1_CemBodyExpoSignalIPdu23:
        sig_name = "DwnLoadDynLitPrmLedRvsgLampLe2LowBriPrm_1_CemBodyExpoSignalIPdu23"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmLedRvsgLampLe2ContTiPrm_1_CemBodyExpoSignalIPdu23:
        sig_name = "DwnLoadDynLitPrmLedRvsgLampLe2ContTiPrm_1_CemBodyExpoSignalIPdu23"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedRvsgLampLe2ModePrm_1_CemBodyExpoSignalIPdu23:
        sig_name = "DwnLoadDynLitPrmLedRvsgLampLe2ModePrm_1_CemBodyExpoSignalIPdu23"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode1_Off': 0, 'Mode1_On': 1, 'Mode1_GradualOn': 2, 'Mode1_GradualOff': 3, 'Mode1_ForwardWipingOn': 4, 'Mode1_BackwardWipingOn': 5, 'Mode1_OutwardWipingOn': 6, 'Mode1_InwardWipingOn': 7, 'Mode1_ForwardWipingOff': 8, 'Mode1_BackwardWipingOff': 9, 'Mode1_OutwardWipingOff': 10, 'Mode1_InwardWipingOff': 11, 'Mode1_ForwardScanning': 12, 'Mode1_BackwardScanning': 13, 'Mode1_BreathOn': 14, 'Mode1_BreathOff': 15, 'Mode1_Spare1': 16, 'Mode1_Spare2': 17}
        compute_method = None
        length = 5
        startbit = 13
        byte = 1
        mask = 0b00111110
        unmask = 0b11000001
        shift = 1

    class DwnLoadDynLitPrmLedRvsgLampLe2OffsTiPrm_1_CemBodyExpoSignalIPdu23:
        sig_name = "DwnLoadDynLitPrmLedRvsgLampLe2OffsTiPrm_1_CemBodyExpoSignalIPdu23"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedRvsgLampLe2UpprBriPrm_1_CemBodyExpoSignalIPdu23:
        sig_name = "DwnLoadDynLitPrmLedRvsgLampLe2UpprBriPrm_1_CemBodyExpoSignalIPdu23"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmLedRvsgLampLe2Tistamp_1_CemBodyExpoSignalIPdu23:
        sig_name = "DwnLoadDynLitPrmLedRvsgLampLe2Tistamp_1_CemBodyExpoSignalIPdu23"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]


class BgmToHcmmBodyExpoDiagReqFrame:
    msg_name = "BgmToHcmmBodyExpoDiagReqFrame"
    msg_id = 1970
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['PCM']


class CemBodyExpoFr17:
    msg_name = "CemBodyExpoFr17"
    msg_id = 303
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RCMM']

    class DwnLoadDynLitPrmLedRePosnLampLe2Tistamp_1_CemBodyExpoSignalIPdu17:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe2Tistamp_1_CemBodyExpoSignalIPdu17"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmLedRePosnLampLe2ModePrm_1_CemBodyExpoSignalIPdu17:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe2ModePrm_1_CemBodyExpoSignalIPdu17"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode1_Off': 0, 'Mode1_On': 1, 'Mode1_GradualOn': 2, 'Mode1_GradualOff': 3, 'Mode1_ForwardWipingOn': 4, 'Mode1_BackwardWipingOn': 5, 'Mode1_OutwardWipingOn': 6, 'Mode1_InwardWipingOn': 7, 'Mode1_ForwardWipingOff': 8, 'Mode1_BackwardWipingOff': 9, 'Mode1_OutwardWipingOff': 10, 'Mode1_InwardWipingOff': 11, 'Mode1_ForwardScanning': 12, 'Mode1_BackwardScanning': 13, 'Mode1_BreathOn': 14, 'Mode1_BreathOff': 15, 'Mode1_Spare1': 16, 'Mode1_Spare2': 17}
        compute_method = None
        length = 5
        startbit = 13
        byte = 1
        mask = 0b00111110
        unmask = 0b11000001
        shift = 1

    class DwnLoadDynLitPrmLedRePosnLampLe2UpprBriPrm_1_CemBodyExpoSignalIPdu17:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe2UpprBriPrm_1_CemBodyExpoSignalIPdu17"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmLedRePosnLampLe2ContTiPrm_1_CemBodyExpoSignalIPdu17:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe2ContTiPrm_1_CemBodyExpoSignalIPdu17"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedRePosnLampLe2LowBriPrm_1_CemBodyExpoSignalIPdu17:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe2LowBriPrm_1_CemBodyExpoSignalIPdu17"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmLedRePosnLampLe2OffsTiPrm_1_CemBodyExpoSignalIPdu17:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe2OffsTiPrm_1_CemBodyExpoSignalIPdu17"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]


class CemBodyExpoFr28:
    msg_name = "CemBodyExpoFr28"
    msg_id = 313
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCML']

    class DwnLoadDynLtgPrmForLedAllWthrLampLeContTiPrm_1_CemBodyExpoSignalIPdu28:
        sig_name = "DwnLoadDynLtgPrmForLedAllWthrLampLeContTiPrm_1_CemBodyExpoSignalIPdu28"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLtgPrmForLedAllWthrLampLeModePrm_1_CemBodyExpoSignalIPdu28:
        sig_name = "DwnLoadDynLtgPrmForLedAllWthrLampLeModePrm_1_CemBodyExpoSignalIPdu28"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode1_Off': 0, 'Mode1_On': 1, 'Mode1_GradualOn': 2, 'Mode1_GradualOff': 3, 'Mode1_ForwardWipingOn': 4, 'Mode1_BackwardWipingOn': 5, 'Mode1_OutwardWipingOn': 6, 'Mode1_InwardWipingOn': 7, 'Mode1_ForwardWipingOff': 8, 'Mode1_BackwardWipingOff': 9, 'Mode1_OutwardWipingOff': 10, 'Mode1_InwardWipingOff': 11, 'Mode1_ForwardScanning': 12, 'Mode1_BackwardScanning': 13, 'Mode1_BreathOn': 14, 'Mode1_BreathOff': 15, 'Mode1_Spare1': 16, 'Mode1_Spare2': 17}
        compute_method = None
        length = 5
        startbit = 13
        byte = 1
        mask = 0b00111110
        unmask = 0b11000001
        shift = 1

    class DwnLoadDynLtgPrmForLedAllWthrLampLeUpprBriPrm_1_CemBodyExpoSignalIPdu28:
        sig_name = "DwnLoadDynLtgPrmForLedAllWthrLampLeUpprBriPrm_1_CemBodyExpoSignalIPdu28"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForLedAllWthrLampLeLowBriPrm_1_CemBodyExpoSignalIPdu28:
        sig_name = "DwnLoadDynLtgPrmForLedAllWthrLampLeLowBriPrm_1_CemBodyExpoSignalIPdu28"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForLedAllWthrLampLeTistamp_1_CemBodyExpoSignalIPdu28:
        sig_name = "DwnLoadDynLtgPrmForLedAllWthrLampLeTistamp_1_CemBodyExpoSignalIPdu28"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLtgPrmForLedAllWthrLampLeOffsTiPrm_1_CemBodyExpoSignalIPdu28:
        sig_name = "DwnLoadDynLtgPrmForLedAllWthrLampLeOffsTiPrm_1_CemBodyExpoSignalIPdu28"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]


class CemBodyExpoFr26:
    msg_name = "CemBodyExpoFr26"
    msg_id = 311
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCML']

    class DwnLoadDynLitPrmForLedHiBeamLeContTiPrm_1_CemBodyExpoSignalIPdu26:
        sig_name = "DwnLoadDynLitPrmForLedHiBeamLeContTiPrm_1_CemBodyExpoSignalIPdu26"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmForLedHiBeamLeTistamp_1_CemBodyExpoSignalIPdu26:
        sig_name = "DwnLoadDynLitPrmForLedHiBeamLeTistamp_1_CemBodyExpoSignalIPdu26"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmForLedHiBeamLeLowBriPrm_1_CemBodyExpoSignalIPdu26:
        sig_name = "DwnLoadDynLitPrmForLedHiBeamLeLowBriPrm_1_CemBodyExpoSignalIPdu26"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmForLedHiBeamLeUpprBriPrm_1_CemBodyExpoSignalIPdu26:
        sig_name = "DwnLoadDynLitPrmForLedHiBeamLeUpprBriPrm_1_CemBodyExpoSignalIPdu26"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmForLedHiBeamLeOffsTiPrm_1_CemBodyExpoSignalIPdu26:
        sig_name = "DwnLoadDynLitPrmForLedHiBeamLeOffsTiPrm_1_CemBodyExpoSignalIPdu26"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmForLedHiBeamLeModePrm_1_CemBodyExpoSignalIPdu26:
        sig_name = "DwnLoadDynLitPrmForLedHiBeamLeModePrm_1_CemBodyExpoSignalIPdu26"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode1_Off': 0, 'Mode1_On': 1, 'Mode1_GradualOn': 2, 'Mode1_GradualOff': 3, 'Mode1_ForwardWipingOn': 4, 'Mode1_BackwardWipingOn': 5, 'Mode1_OutwardWipingOn': 6, 'Mode1_InwardWipingOn': 7, 'Mode1_ForwardWipingOff': 8, 'Mode1_BackwardWipingOff': 9, 'Mode1_OutwardWipingOff': 10, 'Mode1_InwardWipingOff': 11, 'Mode1_ForwardScanning': 12, 'Mode1_BackwardScanning': 13, 'Mode1_BreathOn': 14, 'Mode1_BreathOff': 15, 'Mode1_Spare1': 16, 'Mode1_Spare2': 17}
        compute_method = None
        length = 5
        startbit = 13
        byte = 1
        mask = 0b00111110
        unmask = 0b11000001
        shift = 1


class CemBodyExpoFr83:
    msg_name = "CemBodyExpoFr83"
    msg_id = 817
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCML']

    class DwnLoadDynLtgPrmForFrntLeGrp17OffsetTime_1_CemBodyExpoSignalIPdu83:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp17OffsetTime_1_CemBodyExpoSignalIPdu83"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 31
        byte = 3
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntLeGrp17LowBrightness_1_CemBodyExpoSignalIPdu83:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp17LowBrightness_1_CemBodyExpoSignalIPdu83"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DwnLoadDynLtgPrmForFrntLeGrp17Mode1_1_CemBodyExpoSignalIPdu83:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp17Mode1_1_CemBodyExpoSignalIPdu83"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode4_Off': 0, 'Mode4_On': 1, 'Mode4_GradualOn': 2, 'Mode4_GradualOff': 3, 'Mode4_ForwardWipingOn': 4, 'Mode4_BackwardWipingOn': 5, 'Mode4_OutwardWipingOn': 6, 'Mode4_InwardWipingOn': 7, 'Mode4_ForwardWipingOff': 8, 'Mode4_BackwardWipingOff': 9, 'Mode4_OutwardWipingOff': 10, 'Mode4_InwardWipingOff': 11, 'Mode4_ForwardScanning': 12, 'Mode4_BackwardScanning': 13, 'Mode4_BreathOn': 14, 'Mode4_BreathOff': 15, 'Mode4_1stHalfONand2ndHalfOFF': 16, 'Mode4_HalfOFFHalfON': 17, 'Mode4_HalfDimmingONHalfOFF': 18, 'Mode4_HalfDimmingONHalfON': 19, 'Mode4_HalfOFFHalfDimmingON': 20, 'Mode4_HalfONHalfDimmingON': 21, 'Mode4_HalfDimmingOFFHalfOFF': 22, 'Mode4_HalfDimmingOFFHalfON': 23, 'Mode4_HalfOFFHalfDimmingOFF': 24, 'Mode4_HalfONHalfDimmingOFF': 25, 'Mode4_SingleOn1': 26, 'Mode4_SingleOn2': 27, 'Mode4_SingleOn3': 28, 'Mode4_SingleOn4': 29, 'Mode4_SingleOn5': 30, 'Mode4_SingleOn6': 31, 'Mode4_SingleOn7': 32, 'Mode4_SingleOn8': 33, 'Mode4_SingleOn9': 34, 'Mode4_SingleOn10': 35, 'Mode4_SingleOn11': 36, 'Mode4_SingleOn12': 37, 'Mode4_SingleOff1': 38, 'Mode4_SingleOff2': 39, 'Mode4_SingleOff3': 40, 'Mode4_SingleOff4': 41, 'Mode4_SingleOff5': 42, 'Mode4_SingleOff6': 43, 'Mode4_SingleOff7': 44, 'Mode4_SingleOff8': 45, 'Mode4_SingleOff9': 46, 'Mode4_SingleOff10': 47, 'Mode4_SingleOff11': 48, 'Mode4_SingleOff12': 49}
        compute_method = None
        length = 6
        startbit = 23
        byte = 2
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntLeGrp17HighBrightness_1_CemBodyExpoSignalIPdu83:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp17HighBrightness_1_CemBodyExpoSignalIPdu83"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DwnLoadDynLtgPrmForFrntLeGrp17Timestamp_1_CemBodyExpoSignalIPdu83:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp17Timestamp_1_CemBodyExpoSignalIPdu83"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DwnLoadDynLtgPrmForFrntLeGrp17ContinueTime_1_CemBodyExpoSignalIPdu83:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp17ContinueTime_1_CemBodyExpoSignalIPdu83"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class RcmrBodyExpoFr01:
    msg_name = "RcmrBodyExpoFr01"
    msg_id = 608
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 8
    tx_node = "RCMR"
    rx_nodes = ['BGM']

    class StsOfLedStopLampRi1:
        sig_name = "StsOfLedStopLampRi1"
        sig_start_bit = 23
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 23
        byte = 2
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class StsOfLedReFogLampRi1:
        sig_name = "StsOfLedReFogLampRi1"
        sig_start_bit = 11
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 11
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class ExtrLiShowActvnReRiFb:
        sig_name = "ExtrLiShowActvnReRiFb"
        sig_start_bit = 19
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Sts_Resd': 0, 'Sts_Err': 1, 'Sts_CmplOk': 2, 'Sts_InProgs': 3}
        compute_method = None
        length = 2
        startbit = 19
        byte = 2
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class StsOfLedPosnLampRi1:
        sig_name = "StsOfLedPosnLampRi1"
        sig_start_bit = 9
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 9
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class StsOfLedReLampRi1:
        sig_name = "StsOfLedReLampRi1"
        sig_start_bit = 13
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 13
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class StsOfLedTurnIndcrRi1:
        sig_name = "StsOfLedTurnIndcrRi1"
        sig_start_bit = 25
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 25
        byte = 3
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class DwnLoadStsFbOfReLampCtrlRi1:
        sig_name = "DwnLoadStsFbOfReLampCtrlRi1"
        sig_start_bit = 17
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Sts_Resd': 0, 'Sts_Err': 1, 'Sts_CmplOk': 2, 'Sts_InProgs': 3}
        compute_method = None
        length = 2
        startbit = 17
        byte = 2
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class ExtrLiShowStoreStsReRi1_0_RcmrBodyExpoSignalIPdu01:
        sig_name = "ExtrLiShowStoreStsReRi1_0_RcmrBodyExpoSignalIPdu01"
        sig_start_bit = 1
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 1
        byte = 0
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class StsOfWelGbyReRi1:
        sig_name = "StsOfWelGbyReRi1"
        sig_start_bit = 39
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 39
        byte = 4
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class StsOfLedRvsgLampRi1:
        sig_name = "StsOfLedRvsgLampRi1"
        sig_start_bit = 15
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 15
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class CemBodyExpoFr45:
    msg_name = "CemBodyExpoFr45"
    msg_id = 612
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.065
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR', 'HCML']

    class WipgInfoWipgSpdInfo_1_CemBodyExpoSignalIPdu45:
        sig_name = "WipgInfoWipgSpdInfo_1_CemBodyExpoSignalIPdu45"
        sig_start_bit = 26
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WipgSpdInfo_Off': 0, 'WipgSpdInfo_IntlLo': 1, 'WipgSpdInfo_IntlHi': 2, 'WipgSpdInfo_WipgSpd4045': 3, 'WipgSpdInfo_WipgSpd4650': 4, 'WipgSpdInfo_WipgSpd5155': 5, 'WipgSpdInfo_WipgSpd5660': 6, 'WipgSpdInfo_WiprErr': 7}
        compute_method = None
        length = 3
        startbit = 26
        byte = 3
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class LitArea_1_CemBodyExpoSignalIPdu45:
        sig_name = "LitArea_1_CemBodyExpoSignalIPdu45"
        sig_start_bit = 10
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 10
        byte = 1
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class WipgInfoWiprActv_1_CemBodyExpoSignalIPdu45:
        sig_name = "WipgInfoWiprActv_1_CemBodyExpoSignalIPdu45"
        sig_start_bit = 27
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 27
        byte = 3
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class BrkPedlValBrkPedlVal_1_CemBodyExpoSignalIPdu45:
        sig_name = "BrkPedlValBrkPedlVal_1_CemBodyExpoSignalIPdu45"
        sig_start_bit = 54
        sig_length = 15
        sig_value_factor = 0.00390625
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 25600
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 54
        bmuws_info = [(6, 0b01111111, 0b10000000, 7, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class WipgInfoWiprInWipgAr_1_CemBodyExpoSignalIPdu45:
        sig_name = "WipgInfoWiprInWipgAr_1_CemBodyExpoSignalIPdu45"
        sig_start_bit = 28
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 28
        byte = 3
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class BrkPedlValQf_1_CemBodyExpoSignalIPdu45:
        sig_name = "BrkPedlValQf_1_CemBodyExpoSignalIPdu45"
        sig_start_bit = 41
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 41
        byte = 5
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0


class BgmToRcmrBodyExpoDiagReqFrame:
    msg_name = "BgmToRcmrBodyExpoDiagReqFrame"
    msg_id = 1974
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RCMR']


class CemBodyExpoFr103:
    msg_name = "CemBodyExpoFr103"
    msg_id = 837
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR']

    class DwnLoadDynLtgPrmForFrntRIGrp13ContinueTime_1_CemBodyExpoSignalIPdu103:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp13ContinueTime_1_CemBodyExpoSignalIPdu103"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForFrntRIGrp13LowBrightness_1_CemBodyExpoSignalIPdu103:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp13LowBrightness_1_CemBodyExpoSignalIPdu103"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DwnLoadDynLtgPrmForFrntRIGrp13Timestamp_1_CemBodyExpoSignalIPdu103:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp13Timestamp_1_CemBodyExpoSignalIPdu103"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DwnLoadDynLtgPrmForFrntRIGrp13Mode1_1_CemBodyExpoSignalIPdu103:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp13Mode1_1_CemBodyExpoSignalIPdu103"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode4_Off': 0, 'Mode4_On': 1, 'Mode4_GradualOn': 2, 'Mode4_GradualOff': 3, 'Mode4_ForwardWipingOn': 4, 'Mode4_BackwardWipingOn': 5, 'Mode4_OutwardWipingOn': 6, 'Mode4_InwardWipingOn': 7, 'Mode4_ForwardWipingOff': 8, 'Mode4_BackwardWipingOff': 9, 'Mode4_OutwardWipingOff': 10, 'Mode4_InwardWipingOff': 11, 'Mode4_ForwardScanning': 12, 'Mode4_BackwardScanning': 13, 'Mode4_BreathOn': 14, 'Mode4_BreathOff': 15, 'Mode4_1stHalfONand2ndHalfOFF': 16, 'Mode4_HalfOFFHalfON': 17, 'Mode4_HalfDimmingONHalfOFF': 18, 'Mode4_HalfDimmingONHalfON': 19, 'Mode4_HalfOFFHalfDimmingON': 20, 'Mode4_HalfONHalfDimmingON': 21, 'Mode4_HalfDimmingOFFHalfOFF': 22, 'Mode4_HalfDimmingOFFHalfON': 23, 'Mode4_HalfOFFHalfDimmingOFF': 24, 'Mode4_HalfONHalfDimmingOFF': 25, 'Mode4_SingleOn1': 26, 'Mode4_SingleOn2': 27, 'Mode4_SingleOn3': 28, 'Mode4_SingleOn4': 29, 'Mode4_SingleOn5': 30, 'Mode4_SingleOn6': 31, 'Mode4_SingleOn7': 32, 'Mode4_SingleOn8': 33, 'Mode4_SingleOn9': 34, 'Mode4_SingleOn10': 35, 'Mode4_SingleOn11': 36, 'Mode4_SingleOn12': 37, 'Mode4_SingleOff1': 38, 'Mode4_SingleOff2': 39, 'Mode4_SingleOff3': 40, 'Mode4_SingleOff4': 41, 'Mode4_SingleOff5': 42, 'Mode4_SingleOff6': 43, 'Mode4_SingleOff7': 44, 'Mode4_SingleOff8': 45, 'Mode4_SingleOff9': 46, 'Mode4_SingleOff10': 47, 'Mode4_SingleOff11': 48, 'Mode4_SingleOff12': 49}
        compute_method = None
        length = 6
        startbit = 23
        byte = 2
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntRIGrp13HighBrightness_1_CemBodyExpoSignalIPdu103:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp13HighBrightness_1_CemBodyExpoSignalIPdu103"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DwnLoadDynLtgPrmForFrntRIGrp13OffsetTime_1_CemBodyExpoSignalIPdu103:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp13OffsetTime_1_CemBodyExpoSignalIPdu103"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 31
        byte = 3
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2


class CemBodyExpoCommonFr16:
    msg_name = "CemBodyExpoCommonFr16"
    msg_id = 395
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.045
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR', 'HCML']

    class VehObjforADB4AdbObjHozlAgSpdRi_1_CemBodyExpoCommonSignalIPdu16:
        sig_name = "VehObjforADB4AdbObjHozlAgSpdRi_1_CemBodyExpoCommonSignalIPdu16"
        sig_start_bit = 41
        sig_length = 9
        sig_value_factor = 0.2
        sig_value_offset = "-50"
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 250
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 41
        bmuws_info = [(5, 0b00000011, 0b11111100, 2, 0), (6, 0b11111110, 0b00000001, 7, 1)]

    class VehObjforADB4AdbObjDir_1_CemBodyExpoCommonSignalIPdu16:
        sig_name = "VehObjforADB4AdbObjDir_1_CemBodyExpoCommonSignalIPdu16"
        sig_start_bit = 36
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AdbObjDir_Idle': 0, 'AdbObjDir_Oncoming': 1, 'AdbObjDir_Preceding': 2, 'AdbObjDir_Others': 3}
        compute_method = None
        length = 2
        startbit = 36
        byte = 4
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class VehObjforADB4AdbVertAg_1_CemBodyExpoCommonSignalIPdu16:
        sig_name = "VehObjforADB4AdbVertAg_1_CemBodyExpoCommonSignalIPdu16"
        sig_start_bit = 63
        sig_length = 5
        sig_value_factor = 0.5
        sig_value_offset = "-3"
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Motorola"
        sig_value_init = 6
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 63
        byte = 7
        mask = 0b11111000
        unmask = 0b00000111
        shift = 3

    class VehObjforADB4AdbTrkInfo_1_CemBodyExpoCommonSignalIPdu16:
        sig_name = "VehObjforADB4AdbTrkInfo_1_CemBodyExpoCommonSignalIPdu16"
        sig_start_bit = 48
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NotTracked': 0, 'Tracking': 1}
        compute_method = None
        length = 1
        startbit = 48
        byte = 6
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VehObjforADB4AdbHozlAgLe_1_CemBodyExpoCommonSignalIPdu16:
        sig_name = "VehObjforADB4AdbHozlAgLe_1_CemBodyExpoCommonSignalIPdu16"
        sig_start_bit = 10
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = "-40"
        sig_value_min = 0
        sig_value_max = 1600
        sig_byteorder = "Motorola"
        sig_value_init = 800
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 10
        bmuws_info = [(1, 0b00000111, 0b11111000, 3, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class VehObjforADB4AdbAbsDist_1_CemBodyExpoCommonSignalIPdu16:
        sig_name = "VehObjforADB4AdbAbsDist_1_CemBodyExpoCommonSignalIPdu16"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class VehObjforADB4AdbObjHozlAgSpdLe_1_CemBodyExpoCommonSignalIPdu16:
        sig_name = "VehObjforADB4AdbObjHozlAgSpdLe_1_CemBodyExpoCommonSignalIPdu16"
        sig_start_bit = 34
        sig_length = 9
        sig_value_factor = 0.2
        sig_value_offset = "-50"
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 250
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 34
        bmuws_info = [(4, 0b00000111, 0b11111000, 3, 0), (5, 0b11111100, 0b00000011, 6, 2)]

    class VehObjforADB4AdbClassn_1_CemBodyExpoCommonSignalIPdu16:
        sig_name = "VehObjforADB4AdbClassn_1_CemBodyExpoCommonSignalIPdu16"
        sig_start_bit = 13
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AdbClassn_NoVehicle': 0, 'AdbClassn_Car': 1, 'AdbClassn_Truck': 2, 'AdbClassn_Bus': 3, 'AdbClassn_BikeOrMotorBike': 4, 'AdbClassn_Pedestrain': 5, 'AdbClassn_Mixed': 6, 'AdbClassn_Unknown': 7}
        compute_method = None
        length = 3
        startbit = 13
        byte = 1
        mask = 0b00111000
        unmask = 0b11000111
        shift = 3

    class VehObjforADB4AdbHozlAgRi_1_CemBodyExpoCommonSignalIPdu16:
        sig_name = "VehObjforADB4AdbHozlAgRi_1_CemBodyExpoCommonSignalIPdu16"
        sig_start_bit = 31
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = "-40"
        sig_value_min = 0
        sig_value_max = 1600
        sig_byteorder = "Motorola"
        sig_value_init = 800
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11100000, 0b00011111, 3, 5)]


class CemBodyExpoFr01:
    msg_name = "CemBodyExpoFr01"
    msg_id = 28
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR', 'RCMR', 'HCML', 'RCMM', 'RCML']

    class ExtrLiShowActvnReq:
        sig_name = "ExtrLiShowActvnReq"
        sig_start_bit = 44
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 44
        byte = 5
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class ExtrLiShowFileTxReq:
        sig_name = "ExtrLiShowFileTxReq"
        sig_start_bit = 42
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 42
        byte = 5
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2


class CemBodyExpoCommonFr02:
    msg_name = "CemBodyExpoCommonFr02"
    msg_id = 768
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.045
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR', 'RCMR', 'HCML', 'RCMM', 'RCML']

    class BrkPedlrRatPerc_1_CemBodyExpoCommonSignalIPdu02:
        sig_name = "BrkPedlrRatPerc_1_CemBodyExpoCommonSignalIPdu02"
        sig_start_bit = 46
        sig_length = 15
        sig_value_factor = 0.00390625
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 25600
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 46
        bmuws_info = [(5, 0b01111111, 0b10000000, 7, 0), (6, 0b11111111, 0b00000000, 8, 0)]

    class ActvnOfRvsg:
        sig_name = "ActvnOfRvsg"
        sig_start_bit = 23
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 23
        byte = 2
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class YawRateReqdByDrvr_1_CemBodyExpoCommonSignalIPdu02:
        sig_name = "YawRateReqdByDrvr_1_CemBodyExpoCommonSignalIPdu02"
        sig_start_bit = 7
        sig_length = 16
        sig_value_factor = "2.44140625E-4"
        sig_value_offset = 0.0
        sig_value_min = -20480
        sig_value_max = 20480
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class BrkPedlrRatQf_1_CemBodyExpoCommonSignalIPdu02:
        sig_name = "BrkPedlrRatQf_1_CemBodyExpoCommonSignalIPdu02"
        sig_start_bit = 63
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 63
        byte = 7
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class CemBodyExpoFr36:
    msg_name = "CemBodyExpoFr36"
    msg_id = 321
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCML']

    class DwnLoadDynLtgPrmForLedFrntTurnIndcrLeContTiPrm_1_CemBodyExpoSignalIPdu36:
        sig_name = "DwnLoadDynLtgPrmForLedFrntTurnIndcrLeContTiPrm_1_CemBodyExpoSignalIPdu36"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLtgPrmForLedFrntTurnIndcrLeOffsTiPrm_1_CemBodyExpoSignalIPdu36:
        sig_name = "DwnLoadDynLtgPrmForLedFrntTurnIndcrLeOffsTiPrm_1_CemBodyExpoSignalIPdu36"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLtgPrmForLedFrntTurnIndcrLeUpprBriPrm_1_CemBodyExpoSignalIPdu36:
        sig_name = "DwnLoadDynLtgPrmForLedFrntTurnIndcrLeUpprBriPrm_1_CemBodyExpoSignalIPdu36"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForLedFrntTurnIndcrLeModePrm_1_CemBodyExpoSignalIPdu36:
        sig_name = "DwnLoadDynLtgPrmForLedFrntTurnIndcrLeModePrm_1_CemBodyExpoSignalIPdu36"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode1_Off': 0, 'Mode1_On': 1, 'Mode1_GradualOn': 2, 'Mode1_GradualOff': 3, 'Mode1_ForwardWipingOn': 4, 'Mode1_BackwardWipingOn': 5, 'Mode1_OutwardWipingOn': 6, 'Mode1_InwardWipingOn': 7, 'Mode1_ForwardWipingOff': 8, 'Mode1_BackwardWipingOff': 9, 'Mode1_OutwardWipingOff': 10, 'Mode1_InwardWipingOff': 11, 'Mode1_ForwardScanning': 12, 'Mode1_BackwardScanning': 13, 'Mode1_BreathOn': 14, 'Mode1_BreathOff': 15, 'Mode1_Spare1': 16, 'Mode1_Spare2': 17}
        compute_method = None
        length = 5
        startbit = 13
        byte = 1
        mask = 0b00111110
        unmask = 0b11000001
        shift = 1

    class DwnLoadDynLtgPrmForLedFrntTurnIndcrLeLowBriPrm_1_CemBodyExpoSignalIPdu36:
        sig_name = "DwnLoadDynLtgPrmForLedFrntTurnIndcrLeLowBriPrm_1_CemBodyExpoSignalIPdu36"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForLedFrntTurnIndcrLeTistamp_1_CemBodyExpoSignalIPdu36:
        sig_name = "DwnLoadDynLtgPrmForLedFrntTurnIndcrLeTistamp_1_CemBodyExpoSignalIPdu36"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]


class CemBodyExpoFr104:
    msg_name = "CemBodyExpoFr104"
    msg_id = 838
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR']

    class DwnLoadDynLtgPrmForFrntRIGrp14LowBrightness_1_CemBodyExpoSignalIPdu104:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp14LowBrightness_1_CemBodyExpoSignalIPdu104"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DwnLoadDynLtgPrmForFrntRIGrp14Timestamp_1_CemBodyExpoSignalIPdu104:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp14Timestamp_1_CemBodyExpoSignalIPdu104"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DwnLoadDynLtgPrmForFrntRIGrp14OffsetTime_1_CemBodyExpoSignalIPdu104:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp14OffsetTime_1_CemBodyExpoSignalIPdu104"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 31
        byte = 3
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntRIGrp14ContinueTime_1_CemBodyExpoSignalIPdu104:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp14ContinueTime_1_CemBodyExpoSignalIPdu104"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForFrntRIGrp14Mode1_1_CemBodyExpoSignalIPdu104:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp14Mode1_1_CemBodyExpoSignalIPdu104"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode4_Off': 0, 'Mode4_On': 1, 'Mode4_GradualOn': 2, 'Mode4_GradualOff': 3, 'Mode4_ForwardWipingOn': 4, 'Mode4_BackwardWipingOn': 5, 'Mode4_OutwardWipingOn': 6, 'Mode4_InwardWipingOn': 7, 'Mode4_ForwardWipingOff': 8, 'Mode4_BackwardWipingOff': 9, 'Mode4_OutwardWipingOff': 10, 'Mode4_InwardWipingOff': 11, 'Mode4_ForwardScanning': 12, 'Mode4_BackwardScanning': 13, 'Mode4_BreathOn': 14, 'Mode4_BreathOff': 15, 'Mode4_1stHalfONand2ndHalfOFF': 16, 'Mode4_HalfOFFHalfON': 17, 'Mode4_HalfDimmingONHalfOFF': 18, 'Mode4_HalfDimmingONHalfON': 19, 'Mode4_HalfOFFHalfDimmingON': 20, 'Mode4_HalfONHalfDimmingON': 21, 'Mode4_HalfDimmingOFFHalfOFF': 22, 'Mode4_HalfDimmingOFFHalfON': 23, 'Mode4_HalfOFFHalfDimmingOFF': 24, 'Mode4_HalfONHalfDimmingOFF': 25, 'Mode4_SingleOn1': 26, 'Mode4_SingleOn2': 27, 'Mode4_SingleOn3': 28, 'Mode4_SingleOn4': 29, 'Mode4_SingleOn5': 30, 'Mode4_SingleOn6': 31, 'Mode4_SingleOn7': 32, 'Mode4_SingleOn8': 33, 'Mode4_SingleOn9': 34, 'Mode4_SingleOn10': 35, 'Mode4_SingleOn11': 36, 'Mode4_SingleOn12': 37, 'Mode4_SingleOff1': 38, 'Mode4_SingleOff2': 39, 'Mode4_SingleOff3': 40, 'Mode4_SingleOff4': 41, 'Mode4_SingleOff5': 42, 'Mode4_SingleOff6': 43, 'Mode4_SingleOff7': 44, 'Mode4_SingleOff8': 45, 'Mode4_SingleOff9': 46, 'Mode4_SingleOff10': 47, 'Mode4_SingleOff11': 48, 'Mode4_SingleOff12': 49}
        compute_method = None
        length = 6
        startbit = 23
        byte = 2
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntRIGrp14HighBrightness_1_CemBodyExpoSignalIPdu104:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp14HighBrightness_1_CemBodyExpoSignalIPdu104"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4


class CemBodyExpoFr106:
    msg_name = "CemBodyExpoFr106"
    msg_id = 840
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR']

    class DwnLoadDynLtgPrmForFrntRIGrp16Mode1_1_CemBodyExpoSignalIPdu106:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp16Mode1_1_CemBodyExpoSignalIPdu106"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode4_Off': 0, 'Mode4_On': 1, 'Mode4_GradualOn': 2, 'Mode4_GradualOff': 3, 'Mode4_ForwardWipingOn': 4, 'Mode4_BackwardWipingOn': 5, 'Mode4_OutwardWipingOn': 6, 'Mode4_InwardWipingOn': 7, 'Mode4_ForwardWipingOff': 8, 'Mode4_BackwardWipingOff': 9, 'Mode4_OutwardWipingOff': 10, 'Mode4_InwardWipingOff': 11, 'Mode4_ForwardScanning': 12, 'Mode4_BackwardScanning': 13, 'Mode4_BreathOn': 14, 'Mode4_BreathOff': 15, 'Mode4_1stHalfONand2ndHalfOFF': 16, 'Mode4_HalfOFFHalfON': 17, 'Mode4_HalfDimmingONHalfOFF': 18, 'Mode4_HalfDimmingONHalfON': 19, 'Mode4_HalfOFFHalfDimmingON': 20, 'Mode4_HalfONHalfDimmingON': 21, 'Mode4_HalfDimmingOFFHalfOFF': 22, 'Mode4_HalfDimmingOFFHalfON': 23, 'Mode4_HalfOFFHalfDimmingOFF': 24, 'Mode4_HalfONHalfDimmingOFF': 25, 'Mode4_SingleOn1': 26, 'Mode4_SingleOn2': 27, 'Mode4_SingleOn3': 28, 'Mode4_SingleOn4': 29, 'Mode4_SingleOn5': 30, 'Mode4_SingleOn6': 31, 'Mode4_SingleOn7': 32, 'Mode4_SingleOn8': 33, 'Mode4_SingleOn9': 34, 'Mode4_SingleOn10': 35, 'Mode4_SingleOn11': 36, 'Mode4_SingleOn12': 37, 'Mode4_SingleOff1': 38, 'Mode4_SingleOff2': 39, 'Mode4_SingleOff3': 40, 'Mode4_SingleOff4': 41, 'Mode4_SingleOff5': 42, 'Mode4_SingleOff6': 43, 'Mode4_SingleOff7': 44, 'Mode4_SingleOff8': 45, 'Mode4_SingleOff9': 46, 'Mode4_SingleOff10': 47, 'Mode4_SingleOff11': 48, 'Mode4_SingleOff12': 49}
        compute_method = None
        length = 6
        startbit = 23
        byte = 2
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntRIGrp16ContinueTime_1_CemBodyExpoSignalIPdu106:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp16ContinueTime_1_CemBodyExpoSignalIPdu106"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForFrntRIGrp16OffsetTime_1_CemBodyExpoSignalIPdu106:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp16OffsetTime_1_CemBodyExpoSignalIPdu106"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 31
        byte = 3
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntRIGrp16LowBrightness_1_CemBodyExpoSignalIPdu106:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp16LowBrightness_1_CemBodyExpoSignalIPdu106"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DwnLoadDynLtgPrmForFrntRIGrp16Timestamp_1_CemBodyExpoSignalIPdu106:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp16Timestamp_1_CemBodyExpoSignalIPdu106"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DwnLoadDynLtgPrmForFrntRIGrp16HighBrightness_1_CemBodyExpoSignalIPdu106:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp16HighBrightness_1_CemBodyExpoSignalIPdu106"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4


class HcmlBodyExposedCANNmFr:
    msg_name = "HcmlBodyExposedCANNmFr"
    msg_id = 1329
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "HCML"
    rx_nodes = ['RCMM']


class CemBodyExpoCommonFr10:
    msg_name = "CemBodyExpoCommonFr10"
    msg_id = 389
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.045
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR', 'HCML']

    class TrafficSignForADB1AdbAbsDist_1_CemBodyExpoCommonSignalIPdu10:
        sig_name = "TrafficSignForADB1AdbAbsDist_1_CemBodyExpoCommonSignalIPdu10"
        sig_start_bit = 7
        sig_length = 12
        sig_value_factor = 0.2
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11110000, 0b00001111, 4, 4)]

    class TrafficSignForADB1AdbDetdQly_1_CemBodyExpoCommonSignalIPdu10:
        sig_name = "TrafficSignForADB1AdbDetdQly_1_CemBodyExpoCommonSignalIPdu10"
        sig_start_bit = 11
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ClassnQly_Low': 0, 'ClassnQly_Medium': 1, 'ClassnQly_High': 2}
        compute_method = None
        length = 2
        startbit = 11
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class TrafficSignForADB1AdbHozlAgLe_1_CemBodyExpoCommonSignalIPdu10:
        sig_name = "TrafficSignForADB1AdbHozlAgLe_1_CemBodyExpoCommonSignalIPdu10"
        sig_start_bit = 9
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = "-40"
        sig_value_min = 0
        sig_value_max = 1600
        sig_byteorder = "Motorola"
        sig_value_init = 800
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 9
        bmuws_info = [(1, 0b00000011, 0b11111100, 2, 0), (2, 0b11111111, 0b00000000, 8, 0), (3, 0b10000000, 0b01111111, 1, 7)]

    class TrafficSignForADB1AdbTrkInfo_1_CemBodyExpoCommonSignalIPdu10:
        sig_name = "TrafficSignForADB1AdbTrkInfo_1_CemBodyExpoCommonSignalIPdu10"
        sig_start_bit = 42
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NotTracked': 0, 'Tracking': 1}
        compute_method = None
        length = 1
        startbit = 42
        byte = 5
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class TrafficSignForADB1AdbHozlAgRi_1_CemBodyExpoCommonSignalIPdu10:
        sig_name = "TrafficSignForADB1AdbHozlAgRi_1_CemBodyExpoCommonSignalIPdu10"
        sig_start_bit = 30
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = "-40"
        sig_value_min = 0
        sig_value_max = 1600
        sig_byteorder = "Motorola"
        sig_value_init = 800
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 30
        bmuws_info = [(3, 0b01111111, 0b10000000, 7, 0), (4, 0b11110000, 0b00001111, 4, 4)]

    class TrafficSignForADB1AdbVertAgBot_1_CemBodyExpoCommonSignalIPdu10:
        sig_name = "TrafficSignForADB1AdbVertAgBot_1_CemBodyExpoCommonSignalIPdu10"
        sig_start_bit = 35
        sig_length = 9
        sig_value_factor = 0.05
        sig_value_offset = "-3"
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 60
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 35
        bmuws_info = [(4, 0b00001111, 0b11110000, 4, 0), (5, 0b11111000, 0b00000111, 5, 3)]

    class TrafficSignForADB1AdbVertAgTop_1_CemBodyExpoCommonSignalIPdu10:
        sig_name = "TrafficSignForADB1AdbVertAgTop_1_CemBodyExpoCommonSignalIPdu10"
        sig_start_bit = 41
        sig_length = 9
        sig_value_factor = 0.05
        sig_value_offset = "-3"
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 60
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 41
        bmuws_info = [(5, 0b00000011, 0b11111100, 2, 0), (6, 0b11111110, 0b00000001, 7, 1)]


class CemBodyExpoFr49:
    msg_name = "CemBodyExpoFr49"
    msg_id = 325
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RCMM']

    class DwnLoadDynLitPrmLedRvsgLampRi2ContTiPrm_1_CemBodyExpoSignalIPdu49:
        sig_name = "DwnLoadDynLitPrmLedRvsgLampRi2ContTiPrm_1_CemBodyExpoSignalIPdu49"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedRvsgLampRi2Tistamp_1_CemBodyExpoSignalIPdu49:
        sig_name = "DwnLoadDynLitPrmLedRvsgLampRi2Tistamp_1_CemBodyExpoSignalIPdu49"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmLedRvsgLampRi2UpprBriPrm_1_CemBodyExpoSignalIPdu49:
        sig_name = "DwnLoadDynLitPrmLedRvsgLampRi2UpprBriPrm_1_CemBodyExpoSignalIPdu49"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmLedRvsgLampRi2LowBriPrm_1_CemBodyExpoSignalIPdu49:
        sig_name = "DwnLoadDynLitPrmLedRvsgLampRi2LowBriPrm_1_CemBodyExpoSignalIPdu49"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmLedRvsgLampRi2OffsTiPrm_1_CemBodyExpoSignalIPdu49:
        sig_name = "DwnLoadDynLitPrmLedRvsgLampRi2OffsTiPrm_1_CemBodyExpoSignalIPdu49"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedRvsgLampRi2ModePrm_1_CemBodyExpoSignalIPdu49:
        sig_name = "DwnLoadDynLitPrmLedRvsgLampRi2ModePrm_1_CemBodyExpoSignalIPdu49"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode1_Off': 0, 'Mode1_On': 1, 'Mode1_GradualOn': 2, 'Mode1_GradualOff': 3, 'Mode1_ForwardWipingOn': 4, 'Mode1_BackwardWipingOn': 5, 'Mode1_OutwardWipingOn': 6, 'Mode1_InwardWipingOn': 7, 'Mode1_ForwardWipingOff': 8, 'Mode1_BackwardWipingOff': 9, 'Mode1_OutwardWipingOff': 10, 'Mode1_InwardWipingOff': 11, 'Mode1_ForwardScanning': 12, 'Mode1_BackwardScanning': 13, 'Mode1_BreathOn': 14, 'Mode1_BreathOff': 15, 'Mode1_Spare1': 16, 'Mode1_Spare2': 17}
        compute_method = None
        length = 5
        startbit = 13
        byte = 1
        mask = 0b00111110
        unmask = 0b11000001
        shift = 1


class CemBodyExpoFr18:
    msg_name = "CemBodyExpoFr18"
    msg_id = 304
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RCMR']

    class DwnLoadDynLitPrmLedRePosnLampRi1OffsTiPrm_1_CemBodyExpoSignalIPdu18:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi1OffsTiPrm_1_CemBodyExpoSignalIPdu18"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedRePosnLampRi1Tistamp_1_CemBodyExpoSignalIPdu18:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi1Tistamp_1_CemBodyExpoSignalIPdu18"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmLedRePosnLampRi1ContTiPrm_1_CemBodyExpoSignalIPdu18:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi1ContTiPrm_1_CemBodyExpoSignalIPdu18"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedRePosnLampRi1LowBriPrm_1_CemBodyExpoSignalIPdu18:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi1LowBriPrm_1_CemBodyExpoSignalIPdu18"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmLedRePosnLampRi1UpprBriPrm_1_CemBodyExpoSignalIPdu18:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi1UpprBriPrm_1_CemBodyExpoSignalIPdu18"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmLedRePosnLampRi1ModePrm_1_CemBodyExpoSignalIPdu18:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi1ModePrm_1_CemBodyExpoSignalIPdu18"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode1_Off': 0, 'Mode1_On': 1, 'Mode1_GradualOn': 2, 'Mode1_GradualOff': 3, 'Mode1_ForwardWipingOn': 4, 'Mode1_BackwardWipingOn': 5, 'Mode1_OutwardWipingOn': 6, 'Mode1_InwardWipingOn': 7, 'Mode1_ForwardWipingOff': 8, 'Mode1_BackwardWipingOff': 9, 'Mode1_OutwardWipingOff': 10, 'Mode1_InwardWipingOff': 11, 'Mode1_ForwardScanning': 12, 'Mode1_BackwardScanning': 13, 'Mode1_BreathOn': 14, 'Mode1_BreathOff': 15, 'Mode1_Spare1': 16, 'Mode1_Spare2': 17}
        compute_method = None
        length = 5
        startbit = 13
        byte = 1
        mask = 0b00111110
        unmask = 0b11000001
        shift = 1


class CemBodyExpoFr60:
    msg_name = "CemBodyExpoFr60"
    msg_id = 333
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCML']

    class DwnLoadDynLitPrmLedLeGrilleLampUpprBriPrm_1_CemBodyExpoSignalIPdu60:
        sig_name = "DwnLoadDynLitPrmLedLeGrilleLampUpprBriPrm_1_CemBodyExpoSignalIPdu60"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmLedLeGrilleLampTistamp_1_CemBodyExpoSignalIPdu60:
        sig_name = "DwnLoadDynLitPrmLedLeGrilleLampTistamp_1_CemBodyExpoSignalIPdu60"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmLedLeGrilleLampLowBriPrm_1_CemBodyExpoSignalIPdu60:
        sig_name = "DwnLoadDynLitPrmLedLeGrilleLampLowBriPrm_1_CemBodyExpoSignalIPdu60"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmLedLeGrilleLampContTiPrm_1_CemBodyExpoSignalIPdu60:
        sig_name = "DwnLoadDynLitPrmLedLeGrilleLampContTiPrm_1_CemBodyExpoSignalIPdu60"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedLeGrilleLampModePrm_1_CemBodyExpoSignalIPdu60:
        sig_name = "DwnLoadDynLitPrmLedLeGrilleLampModePrm_1_CemBodyExpoSignalIPdu60"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode1_Off': 0, 'Mode1_On': 1, 'Mode1_GradualOn': 2, 'Mode1_GradualOff': 3, 'Mode1_ForwardWipingOn': 4, 'Mode1_BackwardWipingOn': 5, 'Mode1_OutwardWipingOn': 6, 'Mode1_InwardWipingOn': 7, 'Mode1_ForwardWipingOff': 8, 'Mode1_BackwardWipingOff': 9, 'Mode1_OutwardWipingOff': 10, 'Mode1_InwardWipingOff': 11, 'Mode1_ForwardScanning': 12, 'Mode1_BackwardScanning': 13, 'Mode1_BreathOn': 14, 'Mode1_BreathOff': 15, 'Mode1_Spare1': 16, 'Mode1_Spare2': 17}
        compute_method = None
        length = 5
        startbit = 13
        byte = 1
        mask = 0b00111110
        unmask = 0b11000001
        shift = 1

    class DwnLoadDynLitPrmLedLeGrilleLampOffsTiPrm_1_CemBodyExpoSignalIPdu60:
        sig_name = "DwnLoadDynLitPrmLedLeGrilleLampOffsTiPrm_1_CemBodyExpoSignalIPdu60"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]


class CemBodyExpoFr77:
    msg_name = "CemBodyExpoFr77"
    msg_id = 811
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCML']

    class DwnLoadDynLtgPrmForFrntLeGrp11LowBrightness_1_CemBodyExpoSignalIPdu77:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp11LowBrightness_1_CemBodyExpoSignalIPdu77"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DwnLoadDynLtgPrmForFrntLeGrp11Timestamp_1_CemBodyExpoSignalIPdu77:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp11Timestamp_1_CemBodyExpoSignalIPdu77"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DwnLoadDynLtgPrmForFrntLeGrp11OffsetTime_1_CemBodyExpoSignalIPdu77:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp11OffsetTime_1_CemBodyExpoSignalIPdu77"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 31
        byte = 3
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntLeGrp11HighBrightness_1_CemBodyExpoSignalIPdu77:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp11HighBrightness_1_CemBodyExpoSignalIPdu77"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DwnLoadDynLtgPrmForFrntLeGrp11ContinueTime_1_CemBodyExpoSignalIPdu77:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp11ContinueTime_1_CemBodyExpoSignalIPdu77"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForFrntLeGrp11Mode1_1_CemBodyExpoSignalIPdu77:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp11Mode1_1_CemBodyExpoSignalIPdu77"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode4_Off': 0, 'Mode4_On': 1, 'Mode4_GradualOn': 2, 'Mode4_GradualOff': 3, 'Mode4_ForwardWipingOn': 4, 'Mode4_BackwardWipingOn': 5, 'Mode4_OutwardWipingOn': 6, 'Mode4_InwardWipingOn': 7, 'Mode4_ForwardWipingOff': 8, 'Mode4_BackwardWipingOff': 9, 'Mode4_OutwardWipingOff': 10, 'Mode4_InwardWipingOff': 11, 'Mode4_ForwardScanning': 12, 'Mode4_BackwardScanning': 13, 'Mode4_BreathOn': 14, 'Mode4_BreathOff': 15, 'Mode4_1stHalfONand2ndHalfOFF': 16, 'Mode4_HalfOFFHalfON': 17, 'Mode4_HalfDimmingONHalfOFF': 18, 'Mode4_HalfDimmingONHalfON': 19, 'Mode4_HalfOFFHalfDimmingON': 20, 'Mode4_HalfONHalfDimmingON': 21, 'Mode4_HalfDimmingOFFHalfOFF': 22, 'Mode4_HalfDimmingOFFHalfON': 23, 'Mode4_HalfOFFHalfDimmingOFF': 24, 'Mode4_HalfONHalfDimmingOFF': 25, 'Mode4_SingleOn1': 26, 'Mode4_SingleOn2': 27, 'Mode4_SingleOn3': 28, 'Mode4_SingleOn4': 29, 'Mode4_SingleOn5': 30, 'Mode4_SingleOn6': 31, 'Mode4_SingleOn7': 32, 'Mode4_SingleOn8': 33, 'Mode4_SingleOn9': 34, 'Mode4_SingleOn10': 35, 'Mode4_SingleOn11': 36, 'Mode4_SingleOn12': 37, 'Mode4_SingleOff1': 38, 'Mode4_SingleOff2': 39, 'Mode4_SingleOff3': 40, 'Mode4_SingleOff4': 41, 'Mode4_SingleOff5': 42, 'Mode4_SingleOff6': 43, 'Mode4_SingleOff7': 44, 'Mode4_SingleOff8': 45, 'Mode4_SingleOff9': 46, 'Mode4_SingleOff10': 47, 'Mode4_SingleOff11': 48, 'Mode4_SingleOff12': 49}
        compute_method = None
        length = 6
        startbit = 23
        byte = 2
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2


class CemBodyExpoDevDiagFr01:
    msg_name = "CemBodyExpoDevDiagFr01"
    msg_id = 1432
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['CCM']

    class CEMdevelpsignalgrouprespFunctiondevpsignalgroup1:
        sig_name = "CEMdevelpsignalgrouprespFunctiondevpsignalgroup1"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CEMdevelpsignalgrouprespFunctiondevpsignalgroup6:
        sig_name = "CEMdevelpsignalgrouprespFunctiondevpsignalgroup6"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CEMdevelpsignalgrouprespFunctiondevpsignalgroup2:
        sig_name = "CEMdevelpsignalgrouprespFunctiondevpsignalgroup2"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CEMdevelpsignalgrouprespFunctiondevpsignalgroup7:
        sig_name = "CEMdevelpsignalgrouprespFunctiondevpsignalgroup7"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CEMdevelpsignalgrouprespFunctiondevpsignalgroup5:
        sig_name = "CEMdevelpsignalgrouprespFunctiondevpsignalgroup5"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CEMdevelpsignalgrouprespFunctiondevpsignalgroup3:
        sig_name = "CEMdevelpsignalgrouprespFunctiondevpsignalgroup3"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 23
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CEMdevelpsignalgrouprespFunctiondevpsignalgroup8:
        sig_name = "CEMdevelpsignalgrouprespFunctiondevpsignalgroup8"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CEMdevelpsignalgrouprespFunctiondevpsignalgroup4:
        sig_name = "CEMdevelpsignalgrouprespFunctiondevpsignalgroup4"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class CemBodyExpoCommonFr14:
    msg_name = "CemBodyExpoCommonFr14"
    msg_id = 393
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.045
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR', 'HCML']

    class VehObjforADB2AdbVertAg_1_CemBodyExpoCommonSignalIPdu14:
        sig_name = "VehObjforADB2AdbVertAg_1_CemBodyExpoCommonSignalIPdu14"
        sig_start_bit = 63
        sig_length = 5
        sig_value_factor = 0.5
        sig_value_offset = "-3"
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Motorola"
        sig_value_init = 6
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 63
        byte = 7
        mask = 0b11111000
        unmask = 0b00000111
        shift = 3

    class VehObjforADB2AdbTrkInfo_1_CemBodyExpoCommonSignalIPdu14:
        sig_name = "VehObjforADB2AdbTrkInfo_1_CemBodyExpoCommonSignalIPdu14"
        sig_start_bit = 48
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NotTracked': 0, 'Tracking': 1}
        compute_method = None
        length = 1
        startbit = 48
        byte = 6
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VehObjforADB2AdbObjDir_1_CemBodyExpoCommonSignalIPdu14:
        sig_name = "VehObjforADB2AdbObjDir_1_CemBodyExpoCommonSignalIPdu14"
        sig_start_bit = 36
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AdbObjDir_Idle': 0, 'AdbObjDir_Oncoming': 1, 'AdbObjDir_Preceding': 2, 'AdbObjDir_Others': 3}
        compute_method = None
        length = 2
        startbit = 36
        byte = 4
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class VehObjforADB2AdbObjHozlAgSpdRi_1_CemBodyExpoCommonSignalIPdu14:
        sig_name = "VehObjforADB2AdbObjHozlAgSpdRi_1_CemBodyExpoCommonSignalIPdu14"
        sig_start_bit = 41
        sig_length = 9
        sig_value_factor = 0.2
        sig_value_offset = "-50"
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 250
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 41
        bmuws_info = [(5, 0b00000011, 0b11111100, 2, 0), (6, 0b11111110, 0b00000001, 7, 1)]

    class VehObjforADB2AdbHozlAgRi_1_CemBodyExpoCommonSignalIPdu14:
        sig_name = "VehObjforADB2AdbHozlAgRi_1_CemBodyExpoCommonSignalIPdu14"
        sig_start_bit = 31
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = "-40"
        sig_value_min = 0
        sig_value_max = 1600
        sig_byteorder = "Motorola"
        sig_value_init = 800
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11100000, 0b00011111, 3, 5)]

    class VehObjforADB2AdbAbsDist_1_CemBodyExpoCommonSignalIPdu14:
        sig_name = "VehObjforADB2AdbAbsDist_1_CemBodyExpoCommonSignalIPdu14"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class VehObjforADB2AdbHozlAgLe_1_CemBodyExpoCommonSignalIPdu14:
        sig_name = "VehObjforADB2AdbHozlAgLe_1_CemBodyExpoCommonSignalIPdu14"
        sig_start_bit = 10
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = "-40"
        sig_value_min = 0
        sig_value_max = 1600
        sig_byteorder = "Motorola"
        sig_value_init = 800
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 10
        bmuws_info = [(1, 0b00000111, 0b11111000, 3, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class VehObjforADB2AdbClassn_1_CemBodyExpoCommonSignalIPdu14:
        sig_name = "VehObjforADB2AdbClassn_1_CemBodyExpoCommonSignalIPdu14"
        sig_start_bit = 13
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AdbClassn_NoVehicle': 0, 'AdbClassn_Car': 1, 'AdbClassn_Truck': 2, 'AdbClassn_Bus': 3, 'AdbClassn_BikeOrMotorBike': 4, 'AdbClassn_Pedestrain': 5, 'AdbClassn_Mixed': 6, 'AdbClassn_Unknown': 7}
        compute_method = None
        length = 3
        startbit = 13
        byte = 1
        mask = 0b00111000
        unmask = 0b11000111
        shift = 3

    class VehObjforADB2AdbObjHozlAgSpdLe_1_CemBodyExpoCommonSignalIPdu14:
        sig_name = "VehObjforADB2AdbObjHozlAgSpdLe_1_CemBodyExpoCommonSignalIPdu14"
        sig_start_bit = 34
        sig_length = 9
        sig_value_factor = 0.2
        sig_value_offset = "-50"
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 250
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 34
        bmuws_info = [(4, 0b00000111, 0b11111000, 3, 0), (5, 0b11111100, 0b00000011, 6, 2)]


class CemBodyExpoCommonFr12:
    msg_name = "CemBodyExpoCommonFr12"
    msg_id = 391
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.045
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR', 'HCML']

    class VehObjforAHBAdbDetdQly_1_CemBodyExpoCommonSignalIPdu12:
        sig_name = "VehObjforAHBAdbDetdQly_1_CemBodyExpoCommonSignalIPdu12"
        sig_start_bit = 60
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ClassnQly_Low': 0, 'ClassnQly_Medium': 1, 'ClassnQly_High': 2}
        compute_method = None
        length = 2
        startbit = 60
        byte = 7
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class VehObjforAHBAdbClassn_1_CemBodyExpoCommonSignalIPdu12:
        sig_name = "VehObjforAHBAdbClassn_1_CemBodyExpoCommonSignalIPdu12"
        sig_start_bit = 45
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AdbClassn_NoVehicle': 0, 'AdbClassn_Car': 1, 'AdbClassn_Truck': 2, 'AdbClassn_Bus': 3, 'AdbClassn_BikeOrMotorBike': 4, 'AdbClassn_Pedestrain': 5, 'AdbClassn_Mixed': 6, 'AdbClassn_Unknown': 7}
        compute_method = None
        length = 3
        startbit = 45
        byte = 5
        mask = 0b00111000
        unmask = 0b11000111
        shift = 3

    class VehObjforAHBAdbObjVertAgSpd_1_CemBodyExpoCommonSignalIPdu12:
        sig_name = "VehObjforAHBAdbObjVertAgSpd_1_CemBodyExpoCommonSignalIPdu12"
        sig_start_bit = 42
        sig_length = 11
        sig_value_factor = 0.2
        sig_value_offset = "-144"
        sig_value_min = 0
        sig_value_max = 1440
        sig_byteorder = "Motorola"
        sig_value_init = 720
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 42
        bmuws_info = [(5, 0b00000111, 0b11111000, 3, 0), (6, 0b11111111, 0b00000000, 8, 0)]

    class VehObjforAHBAdbAbsDist_1_CemBodyExpoCommonSignalIPdu12:
        sig_name = "VehObjforAHBAdbAbsDist_1_CemBodyExpoCommonSignalIPdu12"
        sig_start_bit = 39
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11000000, 0b00111111, 2, 6)]

    class VehObjforAHBAdbObjDir_1_CemBodyExpoCommonSignalIPdu12:
        sig_name = "VehObjforAHBAdbObjDir_1_CemBodyExpoCommonSignalIPdu12"
        sig_start_bit = 62
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AdbObjDir_Idle': 0, 'AdbObjDir_Oncoming': 1, 'AdbObjDir_Preceding': 2, 'AdbObjDir_Others': 3}
        compute_method = None
        length = 2
        startbit = 62
        byte = 7
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class VehObjforAHBAdbTrkInfo_1_CemBodyExpoCommonSignalIPdu12:
        sig_name = "VehObjforAHBAdbTrkInfo_1_CemBodyExpoCommonSignalIPdu12"
        sig_start_bit = 63
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NotTracked': 0, 'Tracking': 1}
        compute_method = None
        length = 1
        startbit = 63
        byte = 7
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VehObjforAHBAdbHozlAg_1_CemBodyExpoCommonSignalIPdu12:
        sig_name = "VehObjforAHBAdbHozlAg_1_CemBodyExpoCommonSignalIPdu12"
        sig_start_bit = 18
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = "-40"
        sig_value_min = 0
        sig_value_max = 1600
        sig_byteorder = "Motorola"
        sig_value_init = 800
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 18
        bmuws_info = [(2, 0b00000111, 0b11111000, 3, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class VehObjforAHBAdbVertAg_1_CemBodyExpoCommonSignalIPdu12:
        sig_name = "VehObjforAHBAdbVertAg_1_CemBodyExpoCommonSignalIPdu12"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 0.2
        sig_value_offset = "-15"
        sig_value_min = 0
        sig_value_max = 150
        sig_byteorder = "Motorola"
        sig_value_init = 75
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehObjforAHBAdbObjHozlAgSpd_1_CemBodyExpoCommonSignalIPdu12:
        sig_name = "VehObjforAHBAdbObjHozlAgSpd_1_CemBodyExpoCommonSignalIPdu12"
        sig_start_bit = 15
        sig_length = 13
        sig_value_factor = 0.05
        sig_value_offset = "-144"
        sig_value_min = 0
        sig_value_max = 5760
        sig_byteorder = "Motorola"
        sig_value_init = 2880
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 15
        bmuws_info = [(1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111000, 0b00000111, 5, 3)]

    class VehObjforAHBAdbClassnQly_1_CemBodyExpoCommonSignalIPdu12:
        sig_name = "VehObjforAHBAdbClassnQly_1_CemBodyExpoCommonSignalIPdu12"
        sig_start_bit = 58
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ClassnQly_Low': 0, 'ClassnQly_Medium': 1, 'ClassnQly_High': 2}
        compute_method = None
        length = 2
        startbit = 58
        byte = 7
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1


class CemBodyExpoFr24:
    msg_name = "CemBodyExpoFr24"
    msg_id = 310
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RCMR']

    class DwnLoadDynLitPrmLedRvsgLampRi1Tistamp_1_CemBodyExpoSignalIPdu24:
        sig_name = "DwnLoadDynLitPrmLedRvsgLampRi1Tistamp_1_CemBodyExpoSignalIPdu24"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmLedRvsgLampRi1OffsTiPrm_1_CemBodyExpoSignalIPdu24:
        sig_name = "DwnLoadDynLitPrmLedRvsgLampRi1OffsTiPrm_1_CemBodyExpoSignalIPdu24"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedRvsgLampRi1ContTiPrm_1_CemBodyExpoSignalIPdu24:
        sig_name = "DwnLoadDynLitPrmLedRvsgLampRi1ContTiPrm_1_CemBodyExpoSignalIPdu24"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedRvsgLampRi1ModePrm_1_CemBodyExpoSignalIPdu24:
        sig_name = "DwnLoadDynLitPrmLedRvsgLampRi1ModePrm_1_CemBodyExpoSignalIPdu24"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode1_Off': 0, 'Mode1_On': 1, 'Mode1_GradualOn': 2, 'Mode1_GradualOff': 3, 'Mode1_ForwardWipingOn': 4, 'Mode1_BackwardWipingOn': 5, 'Mode1_OutwardWipingOn': 6, 'Mode1_InwardWipingOn': 7, 'Mode1_ForwardWipingOff': 8, 'Mode1_BackwardWipingOff': 9, 'Mode1_OutwardWipingOff': 10, 'Mode1_InwardWipingOff': 11, 'Mode1_ForwardScanning': 12, 'Mode1_BackwardScanning': 13, 'Mode1_BreathOn': 14, 'Mode1_BreathOff': 15, 'Mode1_Spare1': 16, 'Mode1_Spare2': 17}
        compute_method = None
        length = 5
        startbit = 13
        byte = 1
        mask = 0b00111110
        unmask = 0b11000001
        shift = 1

    class DwnLoadDynLitPrmLedRvsgLampRi1LowBriPrm_1_CemBodyExpoSignalIPdu24:
        sig_name = "DwnLoadDynLitPrmLedRvsgLampRi1LowBriPrm_1_CemBodyExpoSignalIPdu24"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmLedRvsgLampRi1UpprBriPrm_1_CemBodyExpoSignalIPdu24:
        sig_name = "DwnLoadDynLitPrmLedRvsgLampRi1UpprBriPrm_1_CemBodyExpoSignalIPdu24"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class BgmToRcmmBodyExpoDiagReqFrame:
    msg_name = "BgmToRcmmBodyExpoDiagReqFrame"
    msg_id = 1975
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RCMM']


class CemBodyExpoFr20:
    msg_name = "CemBodyExpoFr20"
    msg_id = 306
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RCMM']

    class DwnLoadDynLitPrmLedReTurnIndcrLe2Tistamp_1_CemBodyExpoSignalIPdu20:
        sig_name = "DwnLoadDynLitPrmLedReTurnIndcrLe2Tistamp_1_CemBodyExpoSignalIPdu20"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmLedReTurnIndcrLe2ModePrm_1_CemBodyExpoSignalIPdu20:
        sig_name = "DwnLoadDynLitPrmLedReTurnIndcrLe2ModePrm_1_CemBodyExpoSignalIPdu20"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode1_Off': 0, 'Mode1_On': 1, 'Mode1_GradualOn': 2, 'Mode1_GradualOff': 3, 'Mode1_ForwardWipingOn': 4, 'Mode1_BackwardWipingOn': 5, 'Mode1_OutwardWipingOn': 6, 'Mode1_InwardWipingOn': 7, 'Mode1_ForwardWipingOff': 8, 'Mode1_BackwardWipingOff': 9, 'Mode1_OutwardWipingOff': 10, 'Mode1_InwardWipingOff': 11, 'Mode1_ForwardScanning': 12, 'Mode1_BackwardScanning': 13, 'Mode1_BreathOn': 14, 'Mode1_BreathOff': 15, 'Mode1_Spare1': 16, 'Mode1_Spare2': 17}
        compute_method = None
        length = 5
        startbit = 13
        byte = 1
        mask = 0b00111110
        unmask = 0b11000001
        shift = 1

    class DwnLoadDynLitPrmLedReTurnIndcrLe2ContTiPrm_1_CemBodyExpoSignalIPdu20:
        sig_name = "DwnLoadDynLitPrmLedReTurnIndcrLe2ContTiPrm_1_CemBodyExpoSignalIPdu20"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedReTurnIndcrLe2OffsTiPrm_1_CemBodyExpoSignalIPdu20:
        sig_name = "DwnLoadDynLitPrmLedReTurnIndcrLe2OffsTiPrm_1_CemBodyExpoSignalIPdu20"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedReTurnIndcrLe2LowBriPrm_1_CemBodyExpoSignalIPdu20:
        sig_name = "DwnLoadDynLitPrmLedReTurnIndcrLe2LowBriPrm_1_CemBodyExpoSignalIPdu20"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmLedReTurnIndcrLe2UpprBriPrm_1_CemBodyExpoSignalIPdu20:
        sig_name = "DwnLoadDynLitPrmLedReTurnIndcrLe2UpprBriPrm_1_CemBodyExpoSignalIPdu20"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class RcmrToBgmBodyExpoDiagRespFrame:
    msg_name = "RcmrToBgmBodyExpoDiagRespFrame"
    msg_id = 1718
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "RCMR"
    rx_nodes = ['BGM']


class CemBodyExpoFr110:
    msg_name = "CemBodyExpoFr110"
    msg_id = 844
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR']

    class DwnLoadDynLtgPrmForFrntRIGrp20OffsetTime_1_CemBodyExpoSignalIPdu110:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp20OffsetTime_1_CemBodyExpoSignalIPdu110"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 31
        byte = 3
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntRIGrp20LowBrightness_1_CemBodyExpoSignalIPdu110:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp20LowBrightness_1_CemBodyExpoSignalIPdu110"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DwnLoadDynLtgPrmForFrntRIGrp20Timestamp_1_CemBodyExpoSignalIPdu110:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp20Timestamp_1_CemBodyExpoSignalIPdu110"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DwnLoadDynLtgPrmForFrntRIGrp20HighBrightness_1_CemBodyExpoSignalIPdu110:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp20HighBrightness_1_CemBodyExpoSignalIPdu110"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DwnLoadDynLtgPrmForFrntRIGrp20Mode1_1_CemBodyExpoSignalIPdu110:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp20Mode1_1_CemBodyExpoSignalIPdu110"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode4_Off': 0, 'Mode4_On': 1, 'Mode4_GradualOn': 2, 'Mode4_GradualOff': 3, 'Mode4_ForwardWipingOn': 4, 'Mode4_BackwardWipingOn': 5, 'Mode4_OutwardWipingOn': 6, 'Mode4_InwardWipingOn': 7, 'Mode4_ForwardWipingOff': 8, 'Mode4_BackwardWipingOff': 9, 'Mode4_OutwardWipingOff': 10, 'Mode4_InwardWipingOff': 11, 'Mode4_ForwardScanning': 12, 'Mode4_BackwardScanning': 13, 'Mode4_BreathOn': 14, 'Mode4_BreathOff': 15, 'Mode4_1stHalfONand2ndHalfOFF': 16, 'Mode4_HalfOFFHalfON': 17, 'Mode4_HalfDimmingONHalfOFF': 18, 'Mode4_HalfDimmingONHalfON': 19, 'Mode4_HalfOFFHalfDimmingON': 20, 'Mode4_HalfONHalfDimmingON': 21, 'Mode4_HalfDimmingOFFHalfOFF': 22, 'Mode4_HalfDimmingOFFHalfON': 23, 'Mode4_HalfOFFHalfDimmingOFF': 24, 'Mode4_HalfONHalfDimmingOFF': 25, 'Mode4_SingleOn1': 26, 'Mode4_SingleOn2': 27, 'Mode4_SingleOn3': 28, 'Mode4_SingleOn4': 29, 'Mode4_SingleOn5': 30, 'Mode4_SingleOn6': 31, 'Mode4_SingleOn7': 32, 'Mode4_SingleOn8': 33, 'Mode4_SingleOn9': 34, 'Mode4_SingleOn10': 35, 'Mode4_SingleOn11': 36, 'Mode4_SingleOn12': 37, 'Mode4_SingleOff1': 38, 'Mode4_SingleOff2': 39, 'Mode4_SingleOff3': 40, 'Mode4_SingleOff4': 41, 'Mode4_SingleOff5': 42, 'Mode4_SingleOff6': 43, 'Mode4_SingleOff7': 44, 'Mode4_SingleOff8': 45, 'Mode4_SingleOff9': 46, 'Mode4_SingleOff10': 47, 'Mode4_SingleOff11': 48, 'Mode4_SingleOff12': 49}
        compute_method = None
        length = 6
        startbit = 23
        byte = 2
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntRIGrp20ContinueTime_1_CemBodyExpoSignalIPdu110:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp20ContinueTime_1_CemBodyExpoSignalIPdu110"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class CemBodyExpoFr29:
    msg_name = "CemBodyExpoFr29"
    msg_id = 314
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR']

    class DwnLoadDynLtgPrmForLedAllWthrLampRiOffsTiPrm_1_CemBodyExpoSignalIPdu29:
        sig_name = "DwnLoadDynLtgPrmForLedAllWthrLampRiOffsTiPrm_1_CemBodyExpoSignalIPdu29"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLtgPrmForLedAllWthrLampRiTistamp_1_CemBodyExpoSignalIPdu29:
        sig_name = "DwnLoadDynLtgPrmForLedAllWthrLampRiTistamp_1_CemBodyExpoSignalIPdu29"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLtgPrmForLedAllWthrLampRiContTiPrm_1_CemBodyExpoSignalIPdu29:
        sig_name = "DwnLoadDynLtgPrmForLedAllWthrLampRiContTiPrm_1_CemBodyExpoSignalIPdu29"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLtgPrmForLedAllWthrLampRiLowBriPrm_1_CemBodyExpoSignalIPdu29:
        sig_name = "DwnLoadDynLtgPrmForLedAllWthrLampRiLowBriPrm_1_CemBodyExpoSignalIPdu29"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForLedAllWthrLampRiUpprBriPrm_1_CemBodyExpoSignalIPdu29:
        sig_name = "DwnLoadDynLtgPrmForLedAllWthrLampRiUpprBriPrm_1_CemBodyExpoSignalIPdu29"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForLedAllWthrLampRiModePrm_1_CemBodyExpoSignalIPdu29:
        sig_name = "DwnLoadDynLtgPrmForLedAllWthrLampRiModePrm_1_CemBodyExpoSignalIPdu29"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode1_Off': 0, 'Mode1_On': 1, 'Mode1_GradualOn': 2, 'Mode1_GradualOff': 3, 'Mode1_ForwardWipingOn': 4, 'Mode1_BackwardWipingOn': 5, 'Mode1_OutwardWipingOn': 6, 'Mode1_InwardWipingOn': 7, 'Mode1_ForwardWipingOff': 8, 'Mode1_BackwardWipingOff': 9, 'Mode1_OutwardWipingOff': 10, 'Mode1_InwardWipingOff': 11, 'Mode1_ForwardScanning': 12, 'Mode1_BackwardScanning': 13, 'Mode1_BreathOn': 14, 'Mode1_BreathOff': 15, 'Mode1_Spare1': 16, 'Mode1_Spare2': 17}
        compute_method = None
        length = 5
        startbit = 13
        byte = 1
        mask = 0b00111110
        unmask = 0b11000001
        shift = 1


class CemBodyExpoFr70:
    msg_name = "CemBodyExpoFr70"
    msg_id = 804
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCML']

    class DwnLoadDynLtgPrmForFrntLeGrp4OffsetTime_1_CemBodyExpoSignalIPdu70:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp4OffsetTime_1_CemBodyExpoSignalIPdu70"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 31
        byte = 3
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntLeGrp4HighBrightness_1_CemBodyExpoSignalIPdu70:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp4HighBrightness_1_CemBodyExpoSignalIPdu70"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DwnLoadDynLtgPrmForFrntLeGrp4Mode1_1_CemBodyExpoSignalIPdu70:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp4Mode1_1_CemBodyExpoSignalIPdu70"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode4_Off': 0, 'Mode4_On': 1, 'Mode4_GradualOn': 2, 'Mode4_GradualOff': 3, 'Mode4_ForwardWipingOn': 4, 'Mode4_BackwardWipingOn': 5, 'Mode4_OutwardWipingOn': 6, 'Mode4_InwardWipingOn': 7, 'Mode4_ForwardWipingOff': 8, 'Mode4_BackwardWipingOff': 9, 'Mode4_OutwardWipingOff': 10, 'Mode4_InwardWipingOff': 11, 'Mode4_ForwardScanning': 12, 'Mode4_BackwardScanning': 13, 'Mode4_BreathOn': 14, 'Mode4_BreathOff': 15, 'Mode4_1stHalfONand2ndHalfOFF': 16, 'Mode4_HalfOFFHalfON': 17, 'Mode4_HalfDimmingONHalfOFF': 18, 'Mode4_HalfDimmingONHalfON': 19, 'Mode4_HalfOFFHalfDimmingON': 20, 'Mode4_HalfONHalfDimmingON': 21, 'Mode4_HalfDimmingOFFHalfOFF': 22, 'Mode4_HalfDimmingOFFHalfON': 23, 'Mode4_HalfOFFHalfDimmingOFF': 24, 'Mode4_HalfONHalfDimmingOFF': 25, 'Mode4_SingleOn1': 26, 'Mode4_SingleOn2': 27, 'Mode4_SingleOn3': 28, 'Mode4_SingleOn4': 29, 'Mode4_SingleOn5': 30, 'Mode4_SingleOn6': 31, 'Mode4_SingleOn7': 32, 'Mode4_SingleOn8': 33, 'Mode4_SingleOn9': 34, 'Mode4_SingleOn10': 35, 'Mode4_SingleOn11': 36, 'Mode4_SingleOn12': 37, 'Mode4_SingleOff1': 38, 'Mode4_SingleOff2': 39, 'Mode4_SingleOff3': 40, 'Mode4_SingleOff4': 41, 'Mode4_SingleOff5': 42, 'Mode4_SingleOff6': 43, 'Mode4_SingleOff7': 44, 'Mode4_SingleOff8': 45, 'Mode4_SingleOff9': 46, 'Mode4_SingleOff10': 47, 'Mode4_SingleOff11': 48, 'Mode4_SingleOff12': 49}
        compute_method = None
        length = 6
        startbit = 23
        byte = 2
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntLeGrp4ContinueTime_1_CemBodyExpoSignalIPdu70:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp4ContinueTime_1_CemBodyExpoSignalIPdu70"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForFrntLeGrp4LowBrightness_1_CemBodyExpoSignalIPdu70:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp4LowBrightness_1_CemBodyExpoSignalIPdu70"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DwnLoadDynLtgPrmForFrntLeGrp4Timestamp_1_CemBodyExpoSignalIPdu70:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp4Timestamp_1_CemBodyExpoSignalIPdu70"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5


class CemBodyExpoFr04:
    msg_name = "CemBodyExpoFr04"
    msg_id = 290
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RCMM']

    class DwnLoadDynLitPrmLedRePosnLampRi2ModePrm_1_CemBodyExpoSignalIPdu04:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi2ModePrm_1_CemBodyExpoSignalIPdu04"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode1_Off': 0, 'Mode1_On': 1, 'Mode1_GradualOn': 2, 'Mode1_GradualOff': 3, 'Mode1_ForwardWipingOn': 4, 'Mode1_BackwardWipingOn': 5, 'Mode1_OutwardWipingOn': 6, 'Mode1_InwardWipingOn': 7, 'Mode1_ForwardWipingOff': 8, 'Mode1_BackwardWipingOff': 9, 'Mode1_OutwardWipingOff': 10, 'Mode1_InwardWipingOff': 11, 'Mode1_ForwardScanning': 12, 'Mode1_BackwardScanning': 13, 'Mode1_BreathOn': 14, 'Mode1_BreathOff': 15, 'Mode1_Spare1': 16, 'Mode1_Spare2': 17}
        compute_method = None
        length = 5
        startbit = 13
        byte = 1
        mask = 0b00111110
        unmask = 0b11000001
        shift = 1

    class DwnLoadDynLitPrmLedRePosnLampRi2LowBriPrm_1_CemBodyExpoSignalIPdu04:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi2LowBriPrm_1_CemBodyExpoSignalIPdu04"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmLedRePosnLampRi2OffsTiPrm_1_CemBodyExpoSignalIPdu04:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi2OffsTiPrm_1_CemBodyExpoSignalIPdu04"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedRePosnLampRi2UpprBriPrm_1_CemBodyExpoSignalIPdu04:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi2UpprBriPrm_1_CemBodyExpoSignalIPdu04"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmLedRePosnLampRi2Tistamp_1_CemBodyExpoSignalIPdu04:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi2Tistamp_1_CemBodyExpoSignalIPdu04"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmLedRePosnLampRi2ContTiPrm_1_CemBodyExpoSignalIPdu04:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi2ContTiPrm_1_CemBodyExpoSignalIPdu04"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]


class HcmlToBgmBodyExpoDiagRespFrame:
    msg_name = "HcmlToBgmBodyExpoDiagRespFrame"
    msg_id = 1715
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "HCML"
    rx_nodes = ['BGM']


class CemBodyExpoCommonFr01:
    msg_name = "CemBodyExpoCommonFr01"
    msg_id = 82
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR', 'HCML']

    class AutWinWipgCmd_1_CemBodyExpoCommonSignalIPdu01:
        sig_name = "AutWinWipgCmd_1_CemBodyExpoCommonSignalIPdu01"
        sig_start_bit = 55
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WipgSpd2_WipgSpd0Rpm': 0, 'WipgSpd2_WipgSpd40Rpm': 1, 'WipgSpd2_WipgSpd43Rpm': 2, 'WipgSpd2_WipgSpd46Rpm': 3, 'WipgSpd2_WipgSpd50Rpm': 4, 'WipgSpd2_WipgSpd54Rpm': 5, 'WipgSpd2_WipgSpd57Rpm': 6, 'WipgSpd2_WipgSpd60Rpm': 7}
        compute_method = None
        length = 3
        startbit = 55
        byte = 6
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class SteerWhlSnsrQf_3_CemBodyExpoCommonSignalIPdu01:
        sig_name = "SteerWhlSnsrQf_3_CemBodyExpoCommonSignalIPdu01"
        sig_start_bit = 23
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 23
        byte = 2
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class SteerWhlSnsrAg_3_CemBodyExpoCommonSignalIPdu01:
        sig_name = "SteerWhlSnsrAg_3_CemBodyExpoCommonSignalIPdu01"
        sig_start_bit = 6
        sig_length = 15
        sig_value_factor = "9.765625E-4"
        sig_value_offset = 0.0
        sig_value_min = -14848
        sig_value_max = 14848
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 6
        bmuws_info = [(0, 0b01111111, 0b10000000, 7, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class SteerWhlSnsrChks_3_CemBodyExpoCommonSignalIPdu01:
        sig_name = "SteerWhlSnsrChks_3_CemBodyExpoCommonSignalIPdu01"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SteerWhlSnsrAgSpd_3_CemBodyExpoCommonSignalIPdu01:
        sig_name = "SteerWhlSnsrAgSpd_3_CemBodyExpoCommonSignalIPdu01"
        sig_start_bit = 21
        sig_length = 14
        sig_value_factor = 0.0078125
        sig_value_offset = 0.0
        sig_value_min = -6400
        sig_value_max = 6400
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 14
        startbit = 21
        bmuws_info = [(2, 0b00111111, 0b11000000, 6, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class LiOprnMod_1_CemBodyExpoCommonSignalIPdu01:
        sig_name = "LiOprnMod_1_CemBodyExpoCommonSignalIPdu01"
        sig_start_bit = 43
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LiOperMod_Night': 0, 'LiOperMod_Day': 1, 'LiOperMod_Twli': 2, 'LiOperMod_Tnl': 3}
        compute_method = None
        length = 2
        startbit = 43
        byte = 5
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class SteerWhlSnsrCntr_3_CemBodyExpoCommonSignalIPdu01:
        sig_name = "SteerWhlSnsrCntr_3_CemBodyExpoCommonSignalIPdu01"
        sig_start_bit = 47
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 47
        byte = 5
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4


class CemBodyExpoFr100:
    msg_name = "CemBodyExpoFr100"
    msg_id = 834
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR']

    class DwnLoadDynLtgPrmForFrntRIGrp10Mode1_1_CemBodyExpoSignalIPdu100:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp10Mode1_1_CemBodyExpoSignalIPdu100"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode4_Off': 0, 'Mode4_On': 1, 'Mode4_GradualOn': 2, 'Mode4_GradualOff': 3, 'Mode4_ForwardWipingOn': 4, 'Mode4_BackwardWipingOn': 5, 'Mode4_OutwardWipingOn': 6, 'Mode4_InwardWipingOn': 7, 'Mode4_ForwardWipingOff': 8, 'Mode4_BackwardWipingOff': 9, 'Mode4_OutwardWipingOff': 10, 'Mode4_InwardWipingOff': 11, 'Mode4_ForwardScanning': 12, 'Mode4_BackwardScanning': 13, 'Mode4_BreathOn': 14, 'Mode4_BreathOff': 15, 'Mode4_1stHalfONand2ndHalfOFF': 16, 'Mode4_HalfOFFHalfON': 17, 'Mode4_HalfDimmingONHalfOFF': 18, 'Mode4_HalfDimmingONHalfON': 19, 'Mode4_HalfOFFHalfDimmingON': 20, 'Mode4_HalfONHalfDimmingON': 21, 'Mode4_HalfDimmingOFFHalfOFF': 22, 'Mode4_HalfDimmingOFFHalfON': 23, 'Mode4_HalfOFFHalfDimmingOFF': 24, 'Mode4_HalfONHalfDimmingOFF': 25, 'Mode4_SingleOn1': 26, 'Mode4_SingleOn2': 27, 'Mode4_SingleOn3': 28, 'Mode4_SingleOn4': 29, 'Mode4_SingleOn5': 30, 'Mode4_SingleOn6': 31, 'Mode4_SingleOn7': 32, 'Mode4_SingleOn8': 33, 'Mode4_SingleOn9': 34, 'Mode4_SingleOn10': 35, 'Mode4_SingleOn11': 36, 'Mode4_SingleOn12': 37, 'Mode4_SingleOff1': 38, 'Mode4_SingleOff2': 39, 'Mode4_SingleOff3': 40, 'Mode4_SingleOff4': 41, 'Mode4_SingleOff5': 42, 'Mode4_SingleOff6': 43, 'Mode4_SingleOff7': 44, 'Mode4_SingleOff8': 45, 'Mode4_SingleOff9': 46, 'Mode4_SingleOff10': 47, 'Mode4_SingleOff11': 48, 'Mode4_SingleOff12': 49}
        compute_method = None
        length = 6
        startbit = 23
        byte = 2
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntRIGrp10LowBrightness_1_CemBodyExpoSignalIPdu100:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp10LowBrightness_1_CemBodyExpoSignalIPdu100"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DwnLoadDynLtgPrmForFrntRIGrp10OffsetTime_1_CemBodyExpoSignalIPdu100:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp10OffsetTime_1_CemBodyExpoSignalIPdu100"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 31
        byte = 3
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntRIGrp10HighBrightness_1_CemBodyExpoSignalIPdu100:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp10HighBrightness_1_CemBodyExpoSignalIPdu100"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DwnLoadDynLtgPrmForFrntRIGrp10Timestamp_1_CemBodyExpoSignalIPdu100:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp10Timestamp_1_CemBodyExpoSignalIPdu100"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DwnLoadDynLtgPrmForFrntRIGrp10ContinueTime_1_CemBodyExpoSignalIPdu100:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp10ContinueTime_1_CemBodyExpoSignalIPdu100"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class CemBodyExpoCommonFr18:
    msg_name = "CemBodyExpoCommonFr18"
    msg_id = 397
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.045
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR', 'HCML']

    class VehObjforADB6AdbObjDir_1_CemBodyExpoCommonSignalIPdu18:
        sig_name = "VehObjforADB6AdbObjDir_1_CemBodyExpoCommonSignalIPdu18"
        sig_start_bit = 36
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AdbObjDir_Idle': 0, 'AdbObjDir_Oncoming': 1, 'AdbObjDir_Preceding': 2, 'AdbObjDir_Others': 3}
        compute_method = None
        length = 2
        startbit = 36
        byte = 4
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class VehObjforADB6AdbTrkInfo_1_CemBodyExpoCommonSignalIPdu18:
        sig_name = "VehObjforADB6AdbTrkInfo_1_CemBodyExpoCommonSignalIPdu18"
        sig_start_bit = 48
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NotTracked': 0, 'Tracking': 1}
        compute_method = None
        length = 1
        startbit = 48
        byte = 6
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VehObjforADB6AdbHozlAgLe_1_CemBodyExpoCommonSignalIPdu18:
        sig_name = "VehObjforADB6AdbHozlAgLe_1_CemBodyExpoCommonSignalIPdu18"
        sig_start_bit = 10
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = "-40"
        sig_value_min = 0
        sig_value_max = 1600
        sig_byteorder = "Motorola"
        sig_value_init = 800
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 10
        bmuws_info = [(1, 0b00000111, 0b11111000, 3, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class VehObjforADB6AdbAbsDist_1_CemBodyExpoCommonSignalIPdu18:
        sig_name = "VehObjforADB6AdbAbsDist_1_CemBodyExpoCommonSignalIPdu18"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class VehObjforADB6AdbObjHozlAgSpdRi_1_CemBodyExpoCommonSignalIPdu18:
        sig_name = "VehObjforADB6AdbObjHozlAgSpdRi_1_CemBodyExpoCommonSignalIPdu18"
        sig_start_bit = 41
        sig_length = 9
        sig_value_factor = 0.2
        sig_value_offset = "-50"
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 250
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 41
        bmuws_info = [(5, 0b00000011, 0b11111100, 2, 0), (6, 0b11111110, 0b00000001, 7, 1)]

    class VehObjforADB6AdbVertAg_1_CemBodyExpoCommonSignalIPdu18:
        sig_name = "VehObjforADB6AdbVertAg_1_CemBodyExpoCommonSignalIPdu18"
        sig_start_bit = 63
        sig_length = 5
        sig_value_factor = 0.5
        sig_value_offset = "-3"
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Motorola"
        sig_value_init = 6
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 63
        byte = 7
        mask = 0b11111000
        unmask = 0b00000111
        shift = 3

    class VehObjforADB6AdbObjHozlAgSpdLe_1_CemBodyExpoCommonSignalIPdu18:
        sig_name = "VehObjforADB6AdbObjHozlAgSpdLe_1_CemBodyExpoCommonSignalIPdu18"
        sig_start_bit = 34
        sig_length = 9
        sig_value_factor = 0.2
        sig_value_offset = "-50"
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 250
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 34
        bmuws_info = [(4, 0b00000111, 0b11111000, 3, 0), (5, 0b11111100, 0b00000011, 6, 2)]

    class VehObjforADB6AdbClassn_1_CemBodyExpoCommonSignalIPdu18:
        sig_name = "VehObjforADB6AdbClassn_1_CemBodyExpoCommonSignalIPdu18"
        sig_start_bit = 13
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AdbClassn_NoVehicle': 0, 'AdbClassn_Car': 1, 'AdbClassn_Truck': 2, 'AdbClassn_Bus': 3, 'AdbClassn_BikeOrMotorBike': 4, 'AdbClassn_Pedestrain': 5, 'AdbClassn_Mixed': 6, 'AdbClassn_Unknown': 7}
        compute_method = None
        length = 3
        startbit = 13
        byte = 1
        mask = 0b00111000
        unmask = 0b11000111
        shift = 3

    class VehObjforADB6AdbHozlAgRi_1_CemBodyExpoCommonSignalIPdu18:
        sig_name = "VehObjforADB6AdbHozlAgRi_1_CemBodyExpoCommonSignalIPdu18"
        sig_start_bit = 31
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = "-40"
        sig_value_min = 0
        sig_value_max = 1600
        sig_byteorder = "Motorola"
        sig_value_init = 800
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11100000, 0b00011111, 3, 5)]


class HcmrBodyExpoFr04:
    msg_name = "HcmrBodyExpoFr04"
    msg_id = 127
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 8
    tx_node = "HCMR"
    rx_nodes = ['BGM']

    class StsOfLvlgRiChks:
        sig_name = "StsOfLvlgRiChks"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class StsOfLedCornrgLampRi:
        sig_name = "StsOfLedCornrgLampRi"
        sig_start_bit = 11
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 11
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class StsOfTouristModRi:
        sig_name = "StsOfTouristModRi"
        sig_start_bit = 25
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 25
        byte = 3
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class StsOfSwvlgRi:
        sig_name = "StsOfSwvlgRi"
        sig_start_bit = 7
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class StsOfLvlgRiStsOfLvlgRi:
        sig_name = "StsOfLvlgRiStsOfLvlgRi"
        sig_start_bit = 51
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 51
        byte = 6
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class StsOfLedFrntFogLampRi:
        sig_name = "StsOfLedFrntFogLampRi"
        sig_start_bit = 15
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 15
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class StsOfLedDaytiRunngLampRi:
        sig_name = "StsOfLedDaytiRunngLampRi"
        sig_start_bit = 13
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 13
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class HdlampRiInpSts1:
        sig_name = "HdlampRiInpSts1"
        sig_start_bit = 49
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 49
        byte = 6
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class DwnLoadStsFbOfHdlampRi:
        sig_name = "DwnLoadStsFbOfHdlampRi"
        sig_start_bit = 5
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Sts_Resd': 0, 'Sts_Err': 1, 'Sts_CmplOk': 2, 'Sts_InProgs': 3}
        compute_method = None
        length = 2
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class StsOfWelGbyFrntRi:
        sig_name = "StsOfWelGbyFrntRi"
        sig_start_bit = 61
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 61
        byte = 7
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class StsOfAfsRi:
        sig_name = "StsOfAfsRi"
        sig_start_bit = 1
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class StsOfLvlgRiCntr:
        sig_name = "StsOfLvlgRiCntr"
        sig_start_bit = 55
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 55
        byte = 6
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class StsOfLedFrntTurnIndcrRi:
        sig_name = "StsOfLedFrntTurnIndcrRi"
        sig_start_bit = 19
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 19
        byte = 2
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class StsOfAhbcRi:
        sig_name = "StsOfAhbcRi"
        sig_start_bit = 3
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 3
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class ExtrLiShowActvnFrntRiFb:
        sig_name = "ExtrLiShowActvnFrntRiFb"
        sig_start_bit = 28
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Sts_Resd': 0, 'Sts_Err': 1, 'Sts_CmplOk': 2, 'Sts_InProgs': 3}
        compute_method = None
        length = 2
        startbit = 28
        byte = 3
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class StsOfLedFrntPosnLampRi:
        sig_name = "StsOfLedFrntPosnLampRi"
        sig_start_bit = 17
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 17
        byte = 2
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class HdlampRiInpSts2:
        sig_name = "HdlampRiInpSts2"
        sig_start_bit = 63
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 63
        byte = 7
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class StsOfFrntSideMkrLampRi2:
        sig_name = "StsOfFrntSideMkrLampRi2"
        sig_start_bit = 9
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 9
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0


class CemBodyExpoFr13:
    msg_name = "CemBodyExpoFr13"
    msg_id = 299
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RCML']

    class DwnLoadDynLitPrmLedReFogLampLe1Tistamp_1_CemBodyExpoSignalIPdu13:
        sig_name = "DwnLoadDynLitPrmLedReFogLampLe1Tistamp_1_CemBodyExpoSignalIPdu13"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmLedReFogLampLe1ModePrm_1_CemBodyExpoSignalIPdu13:
        sig_name = "DwnLoadDynLitPrmLedReFogLampLe1ModePrm_1_CemBodyExpoSignalIPdu13"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode1_Off': 0, 'Mode1_On': 1, 'Mode1_GradualOn': 2, 'Mode1_GradualOff': 3, 'Mode1_ForwardWipingOn': 4, 'Mode1_BackwardWipingOn': 5, 'Mode1_OutwardWipingOn': 6, 'Mode1_InwardWipingOn': 7, 'Mode1_ForwardWipingOff': 8, 'Mode1_BackwardWipingOff': 9, 'Mode1_OutwardWipingOff': 10, 'Mode1_InwardWipingOff': 11, 'Mode1_ForwardScanning': 12, 'Mode1_BackwardScanning': 13, 'Mode1_BreathOn': 14, 'Mode1_BreathOff': 15, 'Mode1_Spare1': 16, 'Mode1_Spare2': 17}
        compute_method = None
        length = 5
        startbit = 13
        byte = 1
        mask = 0b00111110
        unmask = 0b11000001
        shift = 1

    class DwnLoadDynLitPrmLedReFogLampLe1OffsTiPrm_1_CemBodyExpoSignalIPdu13:
        sig_name = "DwnLoadDynLitPrmLedReFogLampLe1OffsTiPrm_1_CemBodyExpoSignalIPdu13"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedReFogLampLe1LowBriPrm_1_CemBodyExpoSignalIPdu13:
        sig_name = "DwnLoadDynLitPrmLedReFogLampLe1LowBriPrm_1_CemBodyExpoSignalIPdu13"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmLedReFogLampLe1UpprBriPrm_1_CemBodyExpoSignalIPdu13:
        sig_name = "DwnLoadDynLitPrmLedReFogLampLe1UpprBriPrm_1_CemBodyExpoSignalIPdu13"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmLedReFogLampLe1ContTiPrm_1_CemBodyExpoSignalIPdu13:
        sig_name = "DwnLoadDynLitPrmLedReFogLampLe1ContTiPrm_1_CemBodyExpoSignalIPdu13"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]


class HcmmBodyExposedCANNmFr:
    msg_name = "HcmmBodyExposedCANNmFr"
    msg_id = 1334
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "PCM"
    rx_nodes = ['RCML']


class CemBodyExpoFr114:
    msg_name = "CemBodyExpoFr114"
    msg_id = 848
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR']

    class DwnLoadDynLtgPrmForFrntRIGrp24ContinueTime_1_CemBodyExpoSignalIPdu114:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp24ContinueTime_1_CemBodyExpoSignalIPdu114"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForFrntRIGrp24LowBrightness_1_CemBodyExpoSignalIPdu114:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp24LowBrightness_1_CemBodyExpoSignalIPdu114"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DwnLoadDynLtgPrmForFrntRIGrp24OffsetTime_1_CemBodyExpoSignalIPdu114:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp24OffsetTime_1_CemBodyExpoSignalIPdu114"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 31
        byte = 3
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntRIGrp24HighBrightness_1_CemBodyExpoSignalIPdu114:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp24HighBrightness_1_CemBodyExpoSignalIPdu114"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DwnLoadDynLtgPrmForFrntRIGrp24Timestamp_1_CemBodyExpoSignalIPdu114:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp24Timestamp_1_CemBodyExpoSignalIPdu114"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DwnLoadDynLtgPrmForFrntRIGrp24Mode1_1_CemBodyExpoSignalIPdu114:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp24Mode1_1_CemBodyExpoSignalIPdu114"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode4_Off': 0, 'Mode4_On': 1, 'Mode4_GradualOn': 2, 'Mode4_GradualOff': 3, 'Mode4_ForwardWipingOn': 4, 'Mode4_BackwardWipingOn': 5, 'Mode4_OutwardWipingOn': 6, 'Mode4_InwardWipingOn': 7, 'Mode4_ForwardWipingOff': 8, 'Mode4_BackwardWipingOff': 9, 'Mode4_OutwardWipingOff': 10, 'Mode4_InwardWipingOff': 11, 'Mode4_ForwardScanning': 12, 'Mode4_BackwardScanning': 13, 'Mode4_BreathOn': 14, 'Mode4_BreathOff': 15, 'Mode4_1stHalfONand2ndHalfOFF': 16, 'Mode4_HalfOFFHalfON': 17, 'Mode4_HalfDimmingONHalfOFF': 18, 'Mode4_HalfDimmingONHalfON': 19, 'Mode4_HalfOFFHalfDimmingON': 20, 'Mode4_HalfONHalfDimmingON': 21, 'Mode4_HalfDimmingOFFHalfOFF': 22, 'Mode4_HalfDimmingOFFHalfON': 23, 'Mode4_HalfOFFHalfDimmingOFF': 24, 'Mode4_HalfONHalfDimmingOFF': 25, 'Mode4_SingleOn1': 26, 'Mode4_SingleOn2': 27, 'Mode4_SingleOn3': 28, 'Mode4_SingleOn4': 29, 'Mode4_SingleOn5': 30, 'Mode4_SingleOn6': 31, 'Mode4_SingleOn7': 32, 'Mode4_SingleOn8': 33, 'Mode4_SingleOn9': 34, 'Mode4_SingleOn10': 35, 'Mode4_SingleOn11': 36, 'Mode4_SingleOn12': 37, 'Mode4_SingleOff1': 38, 'Mode4_SingleOff2': 39, 'Mode4_SingleOff3': 40, 'Mode4_SingleOff4': 41, 'Mode4_SingleOff5': 42, 'Mode4_SingleOff6': 43, 'Mode4_SingleOff7': 44, 'Mode4_SingleOff8': 45, 'Mode4_SingleOff9': 46, 'Mode4_SingleOff10': 47, 'Mode4_SingleOff11': 48, 'Mode4_SingleOff12': 49}
        compute_method = None
        length = 6
        startbit = 23
        byte = 2
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2


class CemBodyExpoFr14:
    msg_name = "CemBodyExpoFr14"
    msg_id = 300
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RCMM']

    class DwnLoadDynLitPrmLedReFogLampLe2ContTiPrm_1_CemBodyExpoSignalIPdu14:
        sig_name = "DwnLoadDynLitPrmLedReFogLampLe2ContTiPrm_1_CemBodyExpoSignalIPdu14"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedReFogLampLe2UpprBriPrm_1_CemBodyExpoSignalIPdu14:
        sig_name = "DwnLoadDynLitPrmLedReFogLampLe2UpprBriPrm_1_CemBodyExpoSignalIPdu14"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmLedReFogLampLe2LowBriPrm_1_CemBodyExpoSignalIPdu14:
        sig_name = "DwnLoadDynLitPrmLedReFogLampLe2LowBriPrm_1_CemBodyExpoSignalIPdu14"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmLedReFogLampLe2OffsTiPrm_1_CemBodyExpoSignalIPdu14:
        sig_name = "DwnLoadDynLitPrmLedReFogLampLe2OffsTiPrm_1_CemBodyExpoSignalIPdu14"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedReFogLampLe2ModePrm_1_CemBodyExpoSignalIPdu14:
        sig_name = "DwnLoadDynLitPrmLedReFogLampLe2ModePrm_1_CemBodyExpoSignalIPdu14"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode1_Off': 0, 'Mode1_On': 1, 'Mode1_GradualOn': 2, 'Mode1_GradualOff': 3, 'Mode1_ForwardWipingOn': 4, 'Mode1_BackwardWipingOn': 5, 'Mode1_OutwardWipingOn': 6, 'Mode1_InwardWipingOn': 7, 'Mode1_ForwardWipingOff': 8, 'Mode1_BackwardWipingOff': 9, 'Mode1_OutwardWipingOff': 10, 'Mode1_InwardWipingOff': 11, 'Mode1_ForwardScanning': 12, 'Mode1_BackwardScanning': 13, 'Mode1_BreathOn': 14, 'Mode1_BreathOff': 15, 'Mode1_Spare1': 16, 'Mode1_Spare2': 17}
        compute_method = None
        length = 5
        startbit = 13
        byte = 1
        mask = 0b00111110
        unmask = 0b11000001
        shift = 1

    class DwnLoadDynLitPrmLedReFogLampLe2Tistamp_1_CemBodyExpoSignalIPdu14:
        sig_name = "DwnLoadDynLitPrmLedReFogLampLe2Tistamp_1_CemBodyExpoSignalIPdu14"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]


class RcmlBodyExpoFr01:
    msg_name = "RcmlBodyExpoFr01"
    msg_id = 592
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 8
    tx_node = "RCML"
    rx_nodes = ['BGM']

    class StsOfWelGbyReLe1:
        sig_name = "StsOfWelGbyReLe1"
        sig_start_bit = 39
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 39
        byte = 4
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class StsOfLedPosnLampLe1:
        sig_name = "StsOfLedPosnLampLe1"
        sig_start_bit = 9
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 9
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class StsOfLedTurnIndcrLe1:
        sig_name = "StsOfLedTurnIndcrLe1"
        sig_start_bit = 29
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 29
        byte = 3
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class ExtrLiShowStoreStsReLe1_0_RcmlBodyExpoSignalIPdu01:
        sig_name = "ExtrLiShowStoreStsReLe1_0_RcmlBodyExpoSignalIPdu01"
        sig_start_bit = 1
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 1
        byte = 0
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class StsOfLedReFogLampLe1:
        sig_name = "StsOfLedReFogLampLe1"
        sig_start_bit = 11
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 11
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class ExtrLiShowActvnReLeFb:
        sig_name = "ExtrLiShowActvnReLeFb"
        sig_start_bit = 19
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Sts_Resd': 0, 'Sts_Err': 1, 'Sts_CmplOk': 2, 'Sts_InProgs': 3}
        compute_method = None
        length = 2
        startbit = 19
        byte = 2
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class DwnLoadStsFbOfReLampCtrlLe1:
        sig_name = "DwnLoadStsFbOfReLampCtrlLe1"
        sig_start_bit = 17
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Sts_Resd': 0, 'Sts_Err': 1, 'Sts_CmplOk': 2, 'Sts_InProgs': 3}
        compute_method = None
        length = 2
        startbit = 17
        byte = 2
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class StsOfLedRvsgLampLe1:
        sig_name = "StsOfLedRvsgLampLe1"
        sig_start_bit = 15
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 15
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class StsOfLedReLampLe1:
        sig_name = "StsOfLedReLampLe1"
        sig_start_bit = 13
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 13
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class StsOfLedStopLampLe1:
        sig_name = "StsOfLedStopLampLe1"
        sig_start_bit = 21
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 21
        byte = 2
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4


class CemBodyExpoFr67:
    msg_name = "CemBodyExpoFr67"
    msg_id = 801
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCML']

    class DwnLoadDynLtgPrmForFrntLeGrp1LowBrightness_1_CemBodyExpoSignalIPdu67:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp1LowBrightness_1_CemBodyExpoSignalIPdu67"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DwnLoadDynLtgPrmForFrntLeGrp1Mode1_1_CemBodyExpoSignalIPdu67:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp1Mode1_1_CemBodyExpoSignalIPdu67"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode4_Off': 0, 'Mode4_On': 1, 'Mode4_GradualOn': 2, 'Mode4_GradualOff': 3, 'Mode4_ForwardWipingOn': 4, 'Mode4_BackwardWipingOn': 5, 'Mode4_OutwardWipingOn': 6, 'Mode4_InwardWipingOn': 7, 'Mode4_ForwardWipingOff': 8, 'Mode4_BackwardWipingOff': 9, 'Mode4_OutwardWipingOff': 10, 'Mode4_InwardWipingOff': 11, 'Mode4_ForwardScanning': 12, 'Mode4_BackwardScanning': 13, 'Mode4_BreathOn': 14, 'Mode4_BreathOff': 15, 'Mode4_1stHalfONand2ndHalfOFF': 16, 'Mode4_HalfOFFHalfON': 17, 'Mode4_HalfDimmingONHalfOFF': 18, 'Mode4_HalfDimmingONHalfON': 19, 'Mode4_HalfOFFHalfDimmingON': 20, 'Mode4_HalfONHalfDimmingON': 21, 'Mode4_HalfDimmingOFFHalfOFF': 22, 'Mode4_HalfDimmingOFFHalfON': 23, 'Mode4_HalfOFFHalfDimmingOFF': 24, 'Mode4_HalfONHalfDimmingOFF': 25, 'Mode4_SingleOn1': 26, 'Mode4_SingleOn2': 27, 'Mode4_SingleOn3': 28, 'Mode4_SingleOn4': 29, 'Mode4_SingleOn5': 30, 'Mode4_SingleOn6': 31, 'Mode4_SingleOn7': 32, 'Mode4_SingleOn8': 33, 'Mode4_SingleOn9': 34, 'Mode4_SingleOn10': 35, 'Mode4_SingleOn11': 36, 'Mode4_SingleOn12': 37, 'Mode4_SingleOff1': 38, 'Mode4_SingleOff2': 39, 'Mode4_SingleOff3': 40, 'Mode4_SingleOff4': 41, 'Mode4_SingleOff5': 42, 'Mode4_SingleOff6': 43, 'Mode4_SingleOff7': 44, 'Mode4_SingleOff8': 45, 'Mode4_SingleOff9': 46, 'Mode4_SingleOff10': 47, 'Mode4_SingleOff11': 48, 'Mode4_SingleOff12': 49}
        compute_method = None
        length = 6
        startbit = 23
        byte = 2
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntLeGrp1Timestamp_1_CemBodyExpoSignalIPdu67:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp1Timestamp_1_CemBodyExpoSignalIPdu67"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DwnLoadDynLtgPrmForFrntLeGrp1HighBrightness_1_CemBodyExpoSignalIPdu67:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp1HighBrightness_1_CemBodyExpoSignalIPdu67"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DwnLoadDynLtgPrmForFrntLeGrp1ContinueTime_1_CemBodyExpoSignalIPdu67:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp1ContinueTime_1_CemBodyExpoSignalIPdu67"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForFrntLeGrp1OffsetTime_1_CemBodyExpoSignalIPdu67:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp1OffsetTime_1_CemBodyExpoSignalIPdu67"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 31
        byte = 3
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2


class CemBodyExpoFr113:
    msg_name = "CemBodyExpoFr113"
    msg_id = 847
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR']

    class DwnLoadDynLtgPrmForFrntRIGrp23ContinueTime_1_CemBodyExpoSignalIPdu113:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp23ContinueTime_1_CemBodyExpoSignalIPdu113"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForFrntRIGrp23OffsetTime_1_CemBodyExpoSignalIPdu113:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp23OffsetTime_1_CemBodyExpoSignalIPdu113"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 31
        byte = 3
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntRIGrp23Mode1_1_CemBodyExpoSignalIPdu113:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp23Mode1_1_CemBodyExpoSignalIPdu113"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode4_Off': 0, 'Mode4_On': 1, 'Mode4_GradualOn': 2, 'Mode4_GradualOff': 3, 'Mode4_ForwardWipingOn': 4, 'Mode4_BackwardWipingOn': 5, 'Mode4_OutwardWipingOn': 6, 'Mode4_InwardWipingOn': 7, 'Mode4_ForwardWipingOff': 8, 'Mode4_BackwardWipingOff': 9, 'Mode4_OutwardWipingOff': 10, 'Mode4_InwardWipingOff': 11, 'Mode4_ForwardScanning': 12, 'Mode4_BackwardScanning': 13, 'Mode4_BreathOn': 14, 'Mode4_BreathOff': 15, 'Mode4_1stHalfONand2ndHalfOFF': 16, 'Mode4_HalfOFFHalfON': 17, 'Mode4_HalfDimmingONHalfOFF': 18, 'Mode4_HalfDimmingONHalfON': 19, 'Mode4_HalfOFFHalfDimmingON': 20, 'Mode4_HalfONHalfDimmingON': 21, 'Mode4_HalfDimmingOFFHalfOFF': 22, 'Mode4_HalfDimmingOFFHalfON': 23, 'Mode4_HalfOFFHalfDimmingOFF': 24, 'Mode4_HalfONHalfDimmingOFF': 25, 'Mode4_SingleOn1': 26, 'Mode4_SingleOn2': 27, 'Mode4_SingleOn3': 28, 'Mode4_SingleOn4': 29, 'Mode4_SingleOn5': 30, 'Mode4_SingleOn6': 31, 'Mode4_SingleOn7': 32, 'Mode4_SingleOn8': 33, 'Mode4_SingleOn9': 34, 'Mode4_SingleOn10': 35, 'Mode4_SingleOn11': 36, 'Mode4_SingleOn12': 37, 'Mode4_SingleOff1': 38, 'Mode4_SingleOff2': 39, 'Mode4_SingleOff3': 40, 'Mode4_SingleOff4': 41, 'Mode4_SingleOff5': 42, 'Mode4_SingleOff6': 43, 'Mode4_SingleOff7': 44, 'Mode4_SingleOff8': 45, 'Mode4_SingleOff9': 46, 'Mode4_SingleOff10': 47, 'Mode4_SingleOff11': 48, 'Mode4_SingleOff12': 49}
        compute_method = None
        length = 6
        startbit = 23
        byte = 2
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntRIGrp23Timestamp_1_CemBodyExpoSignalIPdu113:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp23Timestamp_1_CemBodyExpoSignalIPdu113"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DwnLoadDynLtgPrmForFrntRIGrp23HighBrightness_1_CemBodyExpoSignalIPdu113:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp23HighBrightness_1_CemBodyExpoSignalIPdu113"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DwnLoadDynLtgPrmForFrntRIGrp23LowBrightness_1_CemBodyExpoSignalIPdu113:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp23LowBrightness_1_CemBodyExpoSignalIPdu113"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0


class CemBodyExpoFr74:
    msg_name = "CemBodyExpoFr74"
    msg_id = 808
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCML']

    class DwnLoadDynLtgPrmForFrntLeGrp8HighBrightness_1_CemBodyExpoSignalIPdu74:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp8HighBrightness_1_CemBodyExpoSignalIPdu74"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DwnLoadDynLtgPrmForFrntLeGrp8Timestamp_1_CemBodyExpoSignalIPdu74:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp8Timestamp_1_CemBodyExpoSignalIPdu74"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DwnLoadDynLtgPrmForFrntLeGrp8OffsetTime_1_CemBodyExpoSignalIPdu74:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp8OffsetTime_1_CemBodyExpoSignalIPdu74"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 31
        byte = 3
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntLeGrp8ContinueTime_1_CemBodyExpoSignalIPdu74:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp8ContinueTime_1_CemBodyExpoSignalIPdu74"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForFrntLeGrp8Mode1_1_CemBodyExpoSignalIPdu74:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp8Mode1_1_CemBodyExpoSignalIPdu74"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode4_Off': 0, 'Mode4_On': 1, 'Mode4_GradualOn': 2, 'Mode4_GradualOff': 3, 'Mode4_ForwardWipingOn': 4, 'Mode4_BackwardWipingOn': 5, 'Mode4_OutwardWipingOn': 6, 'Mode4_InwardWipingOn': 7, 'Mode4_ForwardWipingOff': 8, 'Mode4_BackwardWipingOff': 9, 'Mode4_OutwardWipingOff': 10, 'Mode4_InwardWipingOff': 11, 'Mode4_ForwardScanning': 12, 'Mode4_BackwardScanning': 13, 'Mode4_BreathOn': 14, 'Mode4_BreathOff': 15, 'Mode4_1stHalfONand2ndHalfOFF': 16, 'Mode4_HalfOFFHalfON': 17, 'Mode4_HalfDimmingONHalfOFF': 18, 'Mode4_HalfDimmingONHalfON': 19, 'Mode4_HalfOFFHalfDimmingON': 20, 'Mode4_HalfONHalfDimmingON': 21, 'Mode4_HalfDimmingOFFHalfOFF': 22, 'Mode4_HalfDimmingOFFHalfON': 23, 'Mode4_HalfOFFHalfDimmingOFF': 24, 'Mode4_HalfONHalfDimmingOFF': 25, 'Mode4_SingleOn1': 26, 'Mode4_SingleOn2': 27, 'Mode4_SingleOn3': 28, 'Mode4_SingleOn4': 29, 'Mode4_SingleOn5': 30, 'Mode4_SingleOn6': 31, 'Mode4_SingleOn7': 32, 'Mode4_SingleOn8': 33, 'Mode4_SingleOn9': 34, 'Mode4_SingleOn10': 35, 'Mode4_SingleOn11': 36, 'Mode4_SingleOn12': 37, 'Mode4_SingleOff1': 38, 'Mode4_SingleOff2': 39, 'Mode4_SingleOff3': 40, 'Mode4_SingleOff4': 41, 'Mode4_SingleOff5': 42, 'Mode4_SingleOff6': 43, 'Mode4_SingleOff7': 44, 'Mode4_SingleOff8': 45, 'Mode4_SingleOff9': 46, 'Mode4_SingleOff10': 47, 'Mode4_SingleOff11': 48, 'Mode4_SingleOff12': 49}
        compute_method = None
        length = 6
        startbit = 23
        byte = 2
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntLeGrp8LowBrightness_1_CemBodyExpoSignalIPdu74:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp8LowBrightness_1_CemBodyExpoSignalIPdu74"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0


class CemBodyExpoFr30:
    msg_name = "CemBodyExpoFr30"
    msg_id = 315
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCML']

    class DwnLoadDynLtgPrmForLedCornrgLampLeTistamp_1_CemBodyExpoSignalIPdu30:
        sig_name = "DwnLoadDynLtgPrmForLedCornrgLampLeTistamp_1_CemBodyExpoSignalIPdu30"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLtgPrmForLedCornrgLampLeLowBriPrm_1_CemBodyExpoSignalIPdu30:
        sig_name = "DwnLoadDynLtgPrmForLedCornrgLampLeLowBriPrm_1_CemBodyExpoSignalIPdu30"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForLedCornrgLampLeModePrm_1_CemBodyExpoSignalIPdu30:
        sig_name = "DwnLoadDynLtgPrmForLedCornrgLampLeModePrm_1_CemBodyExpoSignalIPdu30"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode1_Off': 0, 'Mode1_On': 1, 'Mode1_GradualOn': 2, 'Mode1_GradualOff': 3, 'Mode1_ForwardWipingOn': 4, 'Mode1_BackwardWipingOn': 5, 'Mode1_OutwardWipingOn': 6, 'Mode1_InwardWipingOn': 7, 'Mode1_ForwardWipingOff': 8, 'Mode1_BackwardWipingOff': 9, 'Mode1_OutwardWipingOff': 10, 'Mode1_InwardWipingOff': 11, 'Mode1_ForwardScanning': 12, 'Mode1_BackwardScanning': 13, 'Mode1_BreathOn': 14, 'Mode1_BreathOff': 15, 'Mode1_Spare1': 16, 'Mode1_Spare2': 17}
        compute_method = None
        length = 5
        startbit = 13
        byte = 1
        mask = 0b00111110
        unmask = 0b11000001
        shift = 1

    class DwnLoadDynLtgPrmForLedCornrgLampLeOffsTiPrm_1_CemBodyExpoSignalIPdu30:
        sig_name = "DwnLoadDynLtgPrmForLedCornrgLampLeOffsTiPrm_1_CemBodyExpoSignalIPdu30"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLtgPrmForLedCornrgLampLeContTiPrm_1_CemBodyExpoSignalIPdu30:
        sig_name = "DwnLoadDynLtgPrmForLedCornrgLampLeContTiPrm_1_CemBodyExpoSignalIPdu30"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLtgPrmForLedCornrgLampLeUpprBriPrm_1_CemBodyExpoSignalIPdu30:
        sig_name = "DwnLoadDynLtgPrmForLedCornrgLampLeUpprBriPrm_1_CemBodyExpoSignalIPdu30"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class CemBodyExpoFr54:
    msg_name = "CemBodyExpoFr54"
    msg_id = 328
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RCML']

    class DwnLoadDynLitPrmLedRePosnLampLe4LowBriPrm_1_CemBodyExpoSignalIPdu54:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe4LowBriPrm_1_CemBodyExpoSignalIPdu54"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmLedRePosnLampLe4ModePrm_1_CemBodyExpoSignalIPdu54:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe4ModePrm_1_CemBodyExpoSignalIPdu54"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode1_Off': 0, 'Mode1_On': 1, 'Mode1_GradualOn': 2, 'Mode1_GradualOff': 3, 'Mode1_ForwardWipingOn': 4, 'Mode1_BackwardWipingOn': 5, 'Mode1_OutwardWipingOn': 6, 'Mode1_InwardWipingOn': 7, 'Mode1_ForwardWipingOff': 8, 'Mode1_BackwardWipingOff': 9, 'Mode1_OutwardWipingOff': 10, 'Mode1_InwardWipingOff': 11, 'Mode1_ForwardScanning': 12, 'Mode1_BackwardScanning': 13, 'Mode1_BreathOn': 14, 'Mode1_BreathOff': 15, 'Mode1_Spare1': 16, 'Mode1_Spare2': 17}
        compute_method = None
        length = 5
        startbit = 13
        byte = 1
        mask = 0b00111110
        unmask = 0b11000001
        shift = 1

    class DwnLoadDynLitPrmLedRePosnLampLe4OffsTiPrm_1_CemBodyExpoSignalIPdu54:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe4OffsTiPrm_1_CemBodyExpoSignalIPdu54"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedRePosnLampLe4Tistamp_1_CemBodyExpoSignalIPdu54:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe4Tistamp_1_CemBodyExpoSignalIPdu54"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmLedRePosnLampLe4ContTiPrm_1_CemBodyExpoSignalIPdu54:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe4ContTiPrm_1_CemBodyExpoSignalIPdu54"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedRePosnLampLe4UpprBriPrm_1_CemBodyExpoSignalIPdu54:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe4UpprBriPrm_1_CemBodyExpoSignalIPdu54"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class CemBodyExpoCommonFr05:
    msg_name = "CemBodyExpoCommonFr05"
    msg_id = 384
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR', 'RCMR', 'HCML', 'RCMM', 'PCM', 'RCML']

    class VehCfgPrmCCPBytePosn3_2_CemBodyExpoCommonSignalIPdu05:
        sig_name = "VehCfgPrmCCPBytePosn3_2_CemBodyExpoCommonSignalIPdu05"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 23
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgPrmCCPBytePosn5_2_CemBodyExpoCommonSignalIPdu05:
        sig_name = "VehCfgPrmCCPBytePosn5_2_CemBodyExpoCommonSignalIPdu05"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgPrmCCPBytePosn2_2_CemBodyExpoCommonSignalIPdu05:
        sig_name = "VehCfgPrmCCPBytePosn2_2_CemBodyExpoCommonSignalIPdu05"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgPrmCCPBytePosn4_2_CemBodyExpoCommonSignalIPdu05:
        sig_name = "VehCfgPrmCCPBytePosn4_2_CemBodyExpoCommonSignalIPdu05"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgPrmCCPBytePosn8_2_CemBodyExpoCommonSignalIPdu05:
        sig_name = "VehCfgPrmCCPBytePosn8_2_CemBodyExpoCommonSignalIPdu05"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgPrmBlkIDBytePosn1_2_CemBodyExpoCommonSignalIPdu05:
        sig_name = "VehCfgPrmBlkIDBytePosn1_2_CemBodyExpoCommonSignalIPdu05"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgPrmCCPBytePosn6_2_CemBodyExpoCommonSignalIPdu05:
        sig_name = "VehCfgPrmCCPBytePosn6_2_CemBodyExpoCommonSignalIPdu05"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgPrmCCPBytePosn7_2_CemBodyExpoCommonSignalIPdu05:
        sig_name = "VehCfgPrmCCPBytePosn7_2_CemBodyExpoCommonSignalIPdu05"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class CemBodyExpoFr84:
    msg_name = "CemBodyExpoFr84"
    msg_id = 818
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCML']

    class DwnLoadDynLtgPrmForFrntLeGrp18Timestamp_1_CemBodyExpoSignalIPdu84:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp18Timestamp_1_CemBodyExpoSignalIPdu84"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DwnLoadDynLtgPrmForFrntLeGrp18Mode1_1_CemBodyExpoSignalIPdu84:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp18Mode1_1_CemBodyExpoSignalIPdu84"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode4_Off': 0, 'Mode4_On': 1, 'Mode4_GradualOn': 2, 'Mode4_GradualOff': 3, 'Mode4_ForwardWipingOn': 4, 'Mode4_BackwardWipingOn': 5, 'Mode4_OutwardWipingOn': 6, 'Mode4_InwardWipingOn': 7, 'Mode4_ForwardWipingOff': 8, 'Mode4_BackwardWipingOff': 9, 'Mode4_OutwardWipingOff': 10, 'Mode4_InwardWipingOff': 11, 'Mode4_ForwardScanning': 12, 'Mode4_BackwardScanning': 13, 'Mode4_BreathOn': 14, 'Mode4_BreathOff': 15, 'Mode4_1stHalfONand2ndHalfOFF': 16, 'Mode4_HalfOFFHalfON': 17, 'Mode4_HalfDimmingONHalfOFF': 18, 'Mode4_HalfDimmingONHalfON': 19, 'Mode4_HalfOFFHalfDimmingON': 20, 'Mode4_HalfONHalfDimmingON': 21, 'Mode4_HalfDimmingOFFHalfOFF': 22, 'Mode4_HalfDimmingOFFHalfON': 23, 'Mode4_HalfOFFHalfDimmingOFF': 24, 'Mode4_HalfONHalfDimmingOFF': 25, 'Mode4_SingleOn1': 26, 'Mode4_SingleOn2': 27, 'Mode4_SingleOn3': 28, 'Mode4_SingleOn4': 29, 'Mode4_SingleOn5': 30, 'Mode4_SingleOn6': 31, 'Mode4_SingleOn7': 32, 'Mode4_SingleOn8': 33, 'Mode4_SingleOn9': 34, 'Mode4_SingleOn10': 35, 'Mode4_SingleOn11': 36, 'Mode4_SingleOn12': 37, 'Mode4_SingleOff1': 38, 'Mode4_SingleOff2': 39, 'Mode4_SingleOff3': 40, 'Mode4_SingleOff4': 41, 'Mode4_SingleOff5': 42, 'Mode4_SingleOff6': 43, 'Mode4_SingleOff7': 44, 'Mode4_SingleOff8': 45, 'Mode4_SingleOff9': 46, 'Mode4_SingleOff10': 47, 'Mode4_SingleOff11': 48, 'Mode4_SingleOff12': 49}
        compute_method = None
        length = 6
        startbit = 23
        byte = 2
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntLeGrp18LowBrightness_1_CemBodyExpoSignalIPdu84:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp18LowBrightness_1_CemBodyExpoSignalIPdu84"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DwnLoadDynLtgPrmForFrntLeGrp18ContinueTime_1_CemBodyExpoSignalIPdu84:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp18ContinueTime_1_CemBodyExpoSignalIPdu84"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForFrntLeGrp18HighBrightness_1_CemBodyExpoSignalIPdu84:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp18HighBrightness_1_CemBodyExpoSignalIPdu84"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DwnLoadDynLtgPrmForFrntLeGrp18OffsetTime_1_CemBodyExpoSignalIPdu84:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp18OffsetTime_1_CemBodyExpoSignalIPdu84"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 31
        byte = 3
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2


class CemBodyExpoFr68:
    msg_name = "CemBodyExpoFr68"
    msg_id = 802
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCML']

    class DwnLoadDynLtgPrmForFrntLeGrp2Mode1_1_CemBodyExpoSignalIPdu68:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp2Mode1_1_CemBodyExpoSignalIPdu68"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode4_Off': 0, 'Mode4_On': 1, 'Mode4_GradualOn': 2, 'Mode4_GradualOff': 3, 'Mode4_ForwardWipingOn': 4, 'Mode4_BackwardWipingOn': 5, 'Mode4_OutwardWipingOn': 6, 'Mode4_InwardWipingOn': 7, 'Mode4_ForwardWipingOff': 8, 'Mode4_BackwardWipingOff': 9, 'Mode4_OutwardWipingOff': 10, 'Mode4_InwardWipingOff': 11, 'Mode4_ForwardScanning': 12, 'Mode4_BackwardScanning': 13, 'Mode4_BreathOn': 14, 'Mode4_BreathOff': 15, 'Mode4_1stHalfONand2ndHalfOFF': 16, 'Mode4_HalfOFFHalfON': 17, 'Mode4_HalfDimmingONHalfOFF': 18, 'Mode4_HalfDimmingONHalfON': 19, 'Mode4_HalfOFFHalfDimmingON': 20, 'Mode4_HalfONHalfDimmingON': 21, 'Mode4_HalfDimmingOFFHalfOFF': 22, 'Mode4_HalfDimmingOFFHalfON': 23, 'Mode4_HalfOFFHalfDimmingOFF': 24, 'Mode4_HalfONHalfDimmingOFF': 25, 'Mode4_SingleOn1': 26, 'Mode4_SingleOn2': 27, 'Mode4_SingleOn3': 28, 'Mode4_SingleOn4': 29, 'Mode4_SingleOn5': 30, 'Mode4_SingleOn6': 31, 'Mode4_SingleOn7': 32, 'Mode4_SingleOn8': 33, 'Mode4_SingleOn9': 34, 'Mode4_SingleOn10': 35, 'Mode4_SingleOn11': 36, 'Mode4_SingleOn12': 37, 'Mode4_SingleOff1': 38, 'Mode4_SingleOff2': 39, 'Mode4_SingleOff3': 40, 'Mode4_SingleOff4': 41, 'Mode4_SingleOff5': 42, 'Mode4_SingleOff6': 43, 'Mode4_SingleOff7': 44, 'Mode4_SingleOff8': 45, 'Mode4_SingleOff9': 46, 'Mode4_SingleOff10': 47, 'Mode4_SingleOff11': 48, 'Mode4_SingleOff12': 49}
        compute_method = None
        length = 6
        startbit = 23
        byte = 2
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntLeGrp2OffsetTime_1_CemBodyExpoSignalIPdu68:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp2OffsetTime_1_CemBodyExpoSignalIPdu68"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 31
        byte = 3
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntLeGrp2LowBrightness_1_CemBodyExpoSignalIPdu68:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp2LowBrightness_1_CemBodyExpoSignalIPdu68"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DwnLoadDynLtgPrmForFrntLeGrp2Timestamp_1_CemBodyExpoSignalIPdu68:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp2Timestamp_1_CemBodyExpoSignalIPdu68"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DwnLoadDynLtgPrmForFrntLeGrp2ContinueTime_1_CemBodyExpoSignalIPdu68:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp2ContinueTime_1_CemBodyExpoSignalIPdu68"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForFrntLeGrp2HighBrightness_1_CemBodyExpoSignalIPdu68:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp2HighBrightness_1_CemBodyExpoSignalIPdu68"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4


class CemBodyExpoFr53:
    msg_name = "CemBodyExpoFr53"
    msg_id = 327
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RCML']

    class DwnLoadDynLitPrmLedRePosnLampLe3LowBriPrm_1_CemBodyExpoSignalIPdu53:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe3LowBriPrm_1_CemBodyExpoSignalIPdu53"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmLedRePosnLampLe3ContTiPrm_1_CemBodyExpoSignalIPdu53:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe3ContTiPrm_1_CemBodyExpoSignalIPdu53"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedRePosnLampLe3ModePrm_1_CemBodyExpoSignalIPdu53:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe3ModePrm_1_CemBodyExpoSignalIPdu53"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode1_Off': 0, 'Mode1_On': 1, 'Mode1_GradualOn': 2, 'Mode1_GradualOff': 3, 'Mode1_ForwardWipingOn': 4, 'Mode1_BackwardWipingOn': 5, 'Mode1_OutwardWipingOn': 6, 'Mode1_InwardWipingOn': 7, 'Mode1_ForwardWipingOff': 8, 'Mode1_BackwardWipingOff': 9, 'Mode1_OutwardWipingOff': 10, 'Mode1_InwardWipingOff': 11, 'Mode1_ForwardScanning': 12, 'Mode1_BackwardScanning': 13, 'Mode1_BreathOn': 14, 'Mode1_BreathOff': 15, 'Mode1_Spare1': 16, 'Mode1_Spare2': 17}
        compute_method = None
        length = 5
        startbit = 13
        byte = 1
        mask = 0b00111110
        unmask = 0b11000001
        shift = 1

    class DwnLoadDynLitPrmLedRePosnLampLe3OffsTiPrm_1_CemBodyExpoSignalIPdu53:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe3OffsTiPrm_1_CemBodyExpoSignalIPdu53"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedRePosnLampLe3Tistamp_1_CemBodyExpoSignalIPdu53:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe3Tistamp_1_CemBodyExpoSignalIPdu53"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmLedRePosnLampLe3UpprBriPrm_1_CemBodyExpoSignalIPdu53:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe3UpprBriPrm_1_CemBodyExpoSignalIPdu53"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class CemBodyExpoFr76:
    msg_name = "CemBodyExpoFr76"
    msg_id = 810
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCML']

    class DwnLoadDynLtgPrmForFrntLeGrp10HighBrightness_1_CemBodyExpoSignalIPdu76:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp10HighBrightness_1_CemBodyExpoSignalIPdu76"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DwnLoadDynLtgPrmForFrntLeGrp10OffsetTime_1_CemBodyExpoSignalIPdu76:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp10OffsetTime_1_CemBodyExpoSignalIPdu76"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 31
        byte = 3
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntLeGrp10Mode1_1_CemBodyExpoSignalIPdu76:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp10Mode1_1_CemBodyExpoSignalIPdu76"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode4_Off': 0, 'Mode4_On': 1, 'Mode4_GradualOn': 2, 'Mode4_GradualOff': 3, 'Mode4_ForwardWipingOn': 4, 'Mode4_BackwardWipingOn': 5, 'Mode4_OutwardWipingOn': 6, 'Mode4_InwardWipingOn': 7, 'Mode4_ForwardWipingOff': 8, 'Mode4_BackwardWipingOff': 9, 'Mode4_OutwardWipingOff': 10, 'Mode4_InwardWipingOff': 11, 'Mode4_ForwardScanning': 12, 'Mode4_BackwardScanning': 13, 'Mode4_BreathOn': 14, 'Mode4_BreathOff': 15, 'Mode4_1stHalfONand2ndHalfOFF': 16, 'Mode4_HalfOFFHalfON': 17, 'Mode4_HalfDimmingONHalfOFF': 18, 'Mode4_HalfDimmingONHalfON': 19, 'Mode4_HalfOFFHalfDimmingON': 20, 'Mode4_HalfONHalfDimmingON': 21, 'Mode4_HalfDimmingOFFHalfOFF': 22, 'Mode4_HalfDimmingOFFHalfON': 23, 'Mode4_HalfOFFHalfDimmingOFF': 24, 'Mode4_HalfONHalfDimmingOFF': 25, 'Mode4_SingleOn1': 26, 'Mode4_SingleOn2': 27, 'Mode4_SingleOn3': 28, 'Mode4_SingleOn4': 29, 'Mode4_SingleOn5': 30, 'Mode4_SingleOn6': 31, 'Mode4_SingleOn7': 32, 'Mode4_SingleOn8': 33, 'Mode4_SingleOn9': 34, 'Mode4_SingleOn10': 35, 'Mode4_SingleOn11': 36, 'Mode4_SingleOn12': 37, 'Mode4_SingleOff1': 38, 'Mode4_SingleOff2': 39, 'Mode4_SingleOff3': 40, 'Mode4_SingleOff4': 41, 'Mode4_SingleOff5': 42, 'Mode4_SingleOff6': 43, 'Mode4_SingleOff7': 44, 'Mode4_SingleOff8': 45, 'Mode4_SingleOff9': 46, 'Mode4_SingleOff10': 47, 'Mode4_SingleOff11': 48, 'Mode4_SingleOff12': 49}
        compute_method = None
        length = 6
        startbit = 23
        byte = 2
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntLeGrp10LowBrightness_1_CemBodyExpoSignalIPdu76:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp10LowBrightness_1_CemBodyExpoSignalIPdu76"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DwnLoadDynLtgPrmForFrntLeGrp10Timestamp_1_CemBodyExpoSignalIPdu76:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp10Timestamp_1_CemBodyExpoSignalIPdu76"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DwnLoadDynLtgPrmForFrntLeGrp10ContinueTime_1_CemBodyExpoSignalIPdu76:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp10ContinueTime_1_CemBodyExpoSignalIPdu76"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class CemBodyExpoFr22:
    msg_name = "CemBodyExpoFr22"
    msg_id = 308
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RCML']

    class DwnLoadDynLitPrmLedRvsgLampLe1UpprBriPrm_1_CemBodyExpoSignalIPdu22:
        sig_name = "DwnLoadDynLitPrmLedRvsgLampLe1UpprBriPrm_1_CemBodyExpoSignalIPdu22"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmLedRvsgLampLe1LowBriPrm_1_CemBodyExpoSignalIPdu22:
        sig_name = "DwnLoadDynLitPrmLedRvsgLampLe1LowBriPrm_1_CemBodyExpoSignalIPdu22"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmLedRvsgLampLe1ModePrm_1_CemBodyExpoSignalIPdu22:
        sig_name = "DwnLoadDynLitPrmLedRvsgLampLe1ModePrm_1_CemBodyExpoSignalIPdu22"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode1_Off': 0, 'Mode1_On': 1, 'Mode1_GradualOn': 2, 'Mode1_GradualOff': 3, 'Mode1_ForwardWipingOn': 4, 'Mode1_BackwardWipingOn': 5, 'Mode1_OutwardWipingOn': 6, 'Mode1_InwardWipingOn': 7, 'Mode1_ForwardWipingOff': 8, 'Mode1_BackwardWipingOff': 9, 'Mode1_OutwardWipingOff': 10, 'Mode1_InwardWipingOff': 11, 'Mode1_ForwardScanning': 12, 'Mode1_BackwardScanning': 13, 'Mode1_BreathOn': 14, 'Mode1_BreathOff': 15, 'Mode1_Spare1': 16, 'Mode1_Spare2': 17}
        compute_method = None
        length = 5
        startbit = 13
        byte = 1
        mask = 0b00111110
        unmask = 0b11000001
        shift = 1

    class DwnLoadDynLitPrmLedRvsgLampLe1ContTiPrm_1_CemBodyExpoSignalIPdu22:
        sig_name = "DwnLoadDynLitPrmLedRvsgLampLe1ContTiPrm_1_CemBodyExpoSignalIPdu22"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedRvsgLampLe1OffsTiPrm_1_CemBodyExpoSignalIPdu22:
        sig_name = "DwnLoadDynLitPrmLedRvsgLampLe1OffsTiPrm_1_CemBodyExpoSignalIPdu22"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedRvsgLampLe1Tistamp_1_CemBodyExpoSignalIPdu22:
        sig_name = "DwnLoadDynLitPrmLedRvsgLampLe1Tistamp_1_CemBodyExpoSignalIPdu22"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]


class CemBodyExpoFr95:
    msg_name = "CemBodyExpoFr95"
    msg_id = 829
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR']

    class DwnLoadDynLtgPrmForFrntRIGrp5OffsetTime_1_CemBodyExpoSignalIPdu95:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp5OffsetTime_1_CemBodyExpoSignalIPdu95"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 31
        byte = 3
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntRIGrp5Mode1_1_CemBodyExpoSignalIPdu95:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp5Mode1_1_CemBodyExpoSignalIPdu95"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode4_Off': 0, 'Mode4_On': 1, 'Mode4_GradualOn': 2, 'Mode4_GradualOff': 3, 'Mode4_ForwardWipingOn': 4, 'Mode4_BackwardWipingOn': 5, 'Mode4_OutwardWipingOn': 6, 'Mode4_InwardWipingOn': 7, 'Mode4_ForwardWipingOff': 8, 'Mode4_BackwardWipingOff': 9, 'Mode4_OutwardWipingOff': 10, 'Mode4_InwardWipingOff': 11, 'Mode4_ForwardScanning': 12, 'Mode4_BackwardScanning': 13, 'Mode4_BreathOn': 14, 'Mode4_BreathOff': 15, 'Mode4_1stHalfONand2ndHalfOFF': 16, 'Mode4_HalfOFFHalfON': 17, 'Mode4_HalfDimmingONHalfOFF': 18, 'Mode4_HalfDimmingONHalfON': 19, 'Mode4_HalfOFFHalfDimmingON': 20, 'Mode4_HalfONHalfDimmingON': 21, 'Mode4_HalfDimmingOFFHalfOFF': 22, 'Mode4_HalfDimmingOFFHalfON': 23, 'Mode4_HalfOFFHalfDimmingOFF': 24, 'Mode4_HalfONHalfDimmingOFF': 25, 'Mode4_SingleOn1': 26, 'Mode4_SingleOn2': 27, 'Mode4_SingleOn3': 28, 'Mode4_SingleOn4': 29, 'Mode4_SingleOn5': 30, 'Mode4_SingleOn6': 31, 'Mode4_SingleOn7': 32, 'Mode4_SingleOn8': 33, 'Mode4_SingleOn9': 34, 'Mode4_SingleOn10': 35, 'Mode4_SingleOn11': 36, 'Mode4_SingleOn12': 37, 'Mode4_SingleOff1': 38, 'Mode4_SingleOff2': 39, 'Mode4_SingleOff3': 40, 'Mode4_SingleOff4': 41, 'Mode4_SingleOff5': 42, 'Mode4_SingleOff6': 43, 'Mode4_SingleOff7': 44, 'Mode4_SingleOff8': 45, 'Mode4_SingleOff9': 46, 'Mode4_SingleOff10': 47, 'Mode4_SingleOff11': 48, 'Mode4_SingleOff12': 49}
        compute_method = None
        length = 6
        startbit = 23
        byte = 2
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntRIGrp5ContinueTime_1_CemBodyExpoSignalIPdu95:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp5ContinueTime_1_CemBodyExpoSignalIPdu95"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForFrntRIGrp5HighBrightness_1_CemBodyExpoSignalIPdu95:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp5HighBrightness_1_CemBodyExpoSignalIPdu95"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DwnLoadDynLtgPrmForFrntRIGrp5LowBrightness_1_CemBodyExpoSignalIPdu95:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp5LowBrightness_1_CemBodyExpoSignalIPdu95"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DwnLoadDynLtgPrmForFrntRIGrp5Timestamp_1_CemBodyExpoSignalIPdu95:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp5Timestamp_1_CemBodyExpoSignalIPdu95"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5


class CemBodyExpoFr63:
    msg_name = "CemBodyExpoFr63"
    msg_id = 789
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.94
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR', 'RCMR', 'HCML', 'RCMM', 'RCML']

    class DHUcontrolrightlowbeamlamp:
        sig_name = "DHUcontrolrightlowbeamlamp"
        sig_start_bit = 25
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffNoReq_NoReq': 0, 'OnOffNoReq_On': 1, 'OnOffNoReq_Off': 2}
        compute_method = None
        length = 2
        startbit = 25
        byte = 3
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class DHUcontrolrightbrakelight:
        sig_name = "DHUcontrolrightbrakelight"
        sig_start_bit = 19
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffNoReq_NoReq': 0, 'OnOffNoReq_On': 1, 'OnOffNoReq_Off': 2}
        compute_method = None
        length = 2
        startbit = 19
        byte = 2
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class DHUcontrolrightcorneringlamp:
        sig_name = "DHUcontrolrightcorneringlamp"
        sig_start_bit = 17
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffNoReq_NoReq': 0, 'OnOffNoReq_On': 1, 'OnOffNoReq_Off': 2}
        compute_method = None
        length = 2
        startbit = 17
        byte = 2
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class DHUcontrolleftbrakelightLamp:
        sig_name = "DHUcontrolleftbrakelightLamp"
        sig_start_bit = 5
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffNoReq_NoReq': 0, 'OnOffNoReq_On': 1, 'OnOffNoReq_Off': 2}
        compute_method = None
        length = 2
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class DHUcontrollefthighbeamlamp:
        sig_name = "DHUcontrollefthighbeamlamp"
        sig_start_bit = 11
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffNoReq_NoReq': 0, 'OnOffNoReq_On': 1, 'OnOffNoReq_Off': 2}
        compute_method = None
        length = 2
        startbit = 11
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class DHUcontrolleftfroglight:
        sig_name = "DHUcontrolleftfroglight"
        sig_start_bit = 15
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffNoReq_NoReq': 0, 'OnOffNoReq_On': 1, 'OnOffNoReq_Off': 2}
        compute_method = None
        length = 2
        startbit = 15
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class DHUcontrolrightrearcorneringlamp:
        sig_name = "DHUcontrolrightrearcorneringlamp"
        sig_start_bit = 37
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffNoReq_NoReq': 0, 'OnOffNoReq_On': 1, 'OnOffNoReq_Off': 2}
        compute_method = None
        length = 2
        startbit = 37
        byte = 4
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class DHUcontrolleftheadcorneringlamp:
        sig_name = "DHUcontrolleftheadcorneringlamp"
        sig_start_bit = 13
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffNoReq_NoReq': 0, 'OnOffNoReq_On': 1, 'OnOffNoReq_Off': 2}
        compute_method = None
        length = 2
        startbit = 13
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class DHUcontrolrightdaytimerunninglamp:
        sig_name = "DHUcontrolrightdaytimerunninglamp"
        sig_start_bit = 31
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffNoReq_NoReq': 0, 'OnOffNoReq_On': 1, 'OnOffNoReq_Off': 2}
        compute_method = None
        length = 2
        startbit = 31
        byte = 3
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class DHUcontrolrightpositionLamp:
        sig_name = "DHUcontrolrightpositionLamp"
        sig_start_bit = 39
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffNoReq_NoReq': 0, 'OnOffNoReq_On': 1, 'OnOffNoReq_Off': 2}
        compute_method = None
        length = 2
        startbit = 39
        byte = 4
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class DHUcontrolCrossreversinglight:
        sig_name = "DHUcontrolCrossreversinglight"
        sig_start_bit = 7
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffNoReq_NoReq': 0, 'OnOffNoReq_On': 1, 'OnOffNoReq_Off': 2}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class DHUcontrolrightrearpositionLamp:
        sig_name = "DHUcontrolrightrearpositionLamp"
        sig_start_bit = 35
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffNoReq_NoReq': 0, 'OnOffNoReq_On': 1, 'OnOffNoReq_Off': 2}
        compute_method = None
        length = 2
        startbit = 35
        byte = 4
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class DHUcontrolleftcorneringlamp:
        sig_name = "DHUcontrolleftcorneringlamp"
        sig_start_bit = 3
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffNoReq_NoReq': 0, 'OnOffNoReq_On': 1, 'OnOffNoReq_Off': 2}
        compute_method = None
        length = 2
        startbit = 3
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class DHUcontrolleftpositionlamp:
        sig_name = "DHUcontrolleftpositionlamp"
        sig_start_bit = 23
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffNoReq_NoReq': 0, 'OnOffNoReq_On': 1, 'OnOffNoReq_Off': 2}
        compute_method = None
        length = 2
        startbit = 23
        byte = 2
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class DHUcontrolrightfroglight:
        sig_name = "DHUcontrolrightfroglight"
        sig_start_bit = 29
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffNoReq_NoReq': 0, 'OnOffNoReq_On': 1, 'OnOffNoReq_Off': 2}
        compute_method = None
        length = 2
        startbit = 29
        byte = 3
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class DHUcontrolleftlowbeamlamp:
        sig_name = "DHUcontrolleftlowbeamlamp"
        sig_start_bit = 9
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffNoReq_NoReq': 0, 'OnOffNoReq_On': 1, 'OnOffNoReq_Off': 2}
        compute_method = None
        length = 2
        startbit = 9
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class DHUcontrolleftdaytimerunninglamp:
        sig_name = "DHUcontrolleftdaytimerunninglamp"
        sig_start_bit = 1
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffNoReq_NoReq': 0, 'OnOffNoReq_On': 1, 'OnOffNoReq_Off': 2}
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class DHUcontrolrighthighbeamlamp:
        sig_name = "DHUcontrolrighthighbeamlamp"
        sig_start_bit = 27
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffNoReq_NoReq': 0, 'OnOffNoReq_On': 1, 'OnOffNoReq_Off': 2}
        compute_method = None
        length = 2
        startbit = 27
        byte = 3
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class DHUcontrolleftpositionlight:
        sig_name = "DHUcontrolleftpositionlight"
        sig_start_bit = 21
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffNoReq_NoReq': 0, 'OnOffNoReq_On': 1, 'OnOffNoReq_Off': 2}
        compute_method = None
        length = 2
        startbit = 21
        byte = 2
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4


class CemBodyExpoFr87:
    msg_name = "CemBodyExpoFr87"
    msg_id = 821
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCML']

    class DwnLoadDynLtgPrmForFrntLeGrp21OffsetTime_1_CemBodyExpoSignalIPdu87:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp21OffsetTime_1_CemBodyExpoSignalIPdu87"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 31
        byte = 3
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntLeGrp21Timestamp_1_CemBodyExpoSignalIPdu87:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp21Timestamp_1_CemBodyExpoSignalIPdu87"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DwnLoadDynLtgPrmForFrntLeGrp21LowBrightness_1_CemBodyExpoSignalIPdu87:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp21LowBrightness_1_CemBodyExpoSignalIPdu87"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DwnLoadDynLtgPrmForFrntLeGrp21HighBrightness_1_CemBodyExpoSignalIPdu87:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp21HighBrightness_1_CemBodyExpoSignalIPdu87"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DwnLoadDynLtgPrmForFrntLeGrp21ContinueTime_1_CemBodyExpoSignalIPdu87:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp21ContinueTime_1_CemBodyExpoSignalIPdu87"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForFrntLeGrp21Mode1_1_CemBodyExpoSignalIPdu87:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp21Mode1_1_CemBodyExpoSignalIPdu87"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode4_Off': 0, 'Mode4_On': 1, 'Mode4_GradualOn': 2, 'Mode4_GradualOff': 3, 'Mode4_ForwardWipingOn': 4, 'Mode4_BackwardWipingOn': 5, 'Mode4_OutwardWipingOn': 6, 'Mode4_InwardWipingOn': 7, 'Mode4_ForwardWipingOff': 8, 'Mode4_BackwardWipingOff': 9, 'Mode4_OutwardWipingOff': 10, 'Mode4_InwardWipingOff': 11, 'Mode4_ForwardScanning': 12, 'Mode4_BackwardScanning': 13, 'Mode4_BreathOn': 14, 'Mode4_BreathOff': 15, 'Mode4_1stHalfONand2ndHalfOFF': 16, 'Mode4_HalfOFFHalfON': 17, 'Mode4_HalfDimmingONHalfOFF': 18, 'Mode4_HalfDimmingONHalfON': 19, 'Mode4_HalfOFFHalfDimmingON': 20, 'Mode4_HalfONHalfDimmingON': 21, 'Mode4_HalfDimmingOFFHalfOFF': 22, 'Mode4_HalfDimmingOFFHalfON': 23, 'Mode4_HalfOFFHalfDimmingOFF': 24, 'Mode4_HalfONHalfDimmingOFF': 25, 'Mode4_SingleOn1': 26, 'Mode4_SingleOn2': 27, 'Mode4_SingleOn3': 28, 'Mode4_SingleOn4': 29, 'Mode4_SingleOn5': 30, 'Mode4_SingleOn6': 31, 'Mode4_SingleOn7': 32, 'Mode4_SingleOn8': 33, 'Mode4_SingleOn9': 34, 'Mode4_SingleOn10': 35, 'Mode4_SingleOn11': 36, 'Mode4_SingleOn12': 37, 'Mode4_SingleOff1': 38, 'Mode4_SingleOff2': 39, 'Mode4_SingleOff3': 40, 'Mode4_SingleOff4': 41, 'Mode4_SingleOff5': 42, 'Mode4_SingleOff6': 43, 'Mode4_SingleOff7': 44, 'Mode4_SingleOff8': 45, 'Mode4_SingleOff9': 46, 'Mode4_SingleOff10': 47, 'Mode4_SingleOff11': 48, 'Mode4_SingleOff12': 49}
        compute_method = None
        length = 6
        startbit = 23
        byte = 2
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2


class CemBodyExpoFr81:
    msg_name = "CemBodyExpoFr81"
    msg_id = 815
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCML']

    class DwnLoadDynLtgPrmForFrntLeGrp15OffsetTime_1_CemBodyExpoSignalIPdu81:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp15OffsetTime_1_CemBodyExpoSignalIPdu81"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 31
        byte = 3
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntLeGrp15ContinueTime_1_CemBodyExpoSignalIPdu81:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp15ContinueTime_1_CemBodyExpoSignalIPdu81"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLtgPrmForFrntLeGrp15Mode1_1_CemBodyExpoSignalIPdu81:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp15Mode1_1_CemBodyExpoSignalIPdu81"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode4_Off': 0, 'Mode4_On': 1, 'Mode4_GradualOn': 2, 'Mode4_GradualOff': 3, 'Mode4_ForwardWipingOn': 4, 'Mode4_BackwardWipingOn': 5, 'Mode4_OutwardWipingOn': 6, 'Mode4_InwardWipingOn': 7, 'Mode4_ForwardWipingOff': 8, 'Mode4_BackwardWipingOff': 9, 'Mode4_OutwardWipingOff': 10, 'Mode4_InwardWipingOff': 11, 'Mode4_ForwardScanning': 12, 'Mode4_BackwardScanning': 13, 'Mode4_BreathOn': 14, 'Mode4_BreathOff': 15, 'Mode4_1stHalfONand2ndHalfOFF': 16, 'Mode4_HalfOFFHalfON': 17, 'Mode4_HalfDimmingONHalfOFF': 18, 'Mode4_HalfDimmingONHalfON': 19, 'Mode4_HalfOFFHalfDimmingON': 20, 'Mode4_HalfONHalfDimmingON': 21, 'Mode4_HalfDimmingOFFHalfOFF': 22, 'Mode4_HalfDimmingOFFHalfON': 23, 'Mode4_HalfOFFHalfDimmingOFF': 24, 'Mode4_HalfONHalfDimmingOFF': 25, 'Mode4_SingleOn1': 26, 'Mode4_SingleOn2': 27, 'Mode4_SingleOn3': 28, 'Mode4_SingleOn4': 29, 'Mode4_SingleOn5': 30, 'Mode4_SingleOn6': 31, 'Mode4_SingleOn7': 32, 'Mode4_SingleOn8': 33, 'Mode4_SingleOn9': 34, 'Mode4_SingleOn10': 35, 'Mode4_SingleOn11': 36, 'Mode4_SingleOn12': 37, 'Mode4_SingleOff1': 38, 'Mode4_SingleOff2': 39, 'Mode4_SingleOff3': 40, 'Mode4_SingleOff4': 41, 'Mode4_SingleOff5': 42, 'Mode4_SingleOff6': 43, 'Mode4_SingleOff7': 44, 'Mode4_SingleOff8': 45, 'Mode4_SingleOff9': 46, 'Mode4_SingleOff10': 47, 'Mode4_SingleOff11': 48, 'Mode4_SingleOff12': 49}
        compute_method = None
        length = 6
        startbit = 23
        byte = 2
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DwnLoadDynLtgPrmForFrntLeGrp15Timestamp_1_CemBodyExpoSignalIPdu81:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp15Timestamp_1_CemBodyExpoSignalIPdu81"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DwnLoadDynLtgPrmForFrntLeGrp15HighBrightness_1_CemBodyExpoSignalIPdu81:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp15HighBrightness_1_CemBodyExpoSignalIPdu81"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DwnLoadDynLtgPrmForFrntLeGrp15LowBrightness_1_CemBodyExpoSignalIPdu81:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp15LowBrightness_1_CemBodyExpoSignalIPdu81"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0


class CemBodyExpoFr06:
    msg_name = "CemBodyExpoFr06"
    msg_id = 292
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RCML']

    class DwnLoadDynLitPrmForLedMkrLampLe1UpprBriPrm_1_CemBodyExpoSignalIPdu06:
        sig_name = "DwnLoadDynLitPrmForLedMkrLampLe1UpprBriPrm_1_CemBodyExpoSignalIPdu06"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmForLedMkrLampLe1Tistamp_1_CemBodyExpoSignalIPdu06:
        sig_name = "DwnLoadDynLitPrmForLedMkrLampLe1Tistamp_1_CemBodyExpoSignalIPdu06"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmForLedMkrLampLe1ContTiPrm_1_CemBodyExpoSignalIPdu06:
        sig_name = "DwnLoadDynLitPrmForLedMkrLampLe1ContTiPrm_1_CemBodyExpoSignalIPdu06"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmForLedMkrLampLe1LowBriPrm_1_CemBodyExpoSignalIPdu06:
        sig_name = "DwnLoadDynLitPrmForLedMkrLampLe1LowBriPrm_1_CemBodyExpoSignalIPdu06"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmForLedMkrLampLe1OffsTiPrm_1_CemBodyExpoSignalIPdu06:
        sig_name = "DwnLoadDynLitPrmForLedMkrLampLe1OffsTiPrm_1_CemBodyExpoSignalIPdu06"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmForLedMkrLampLe1ModePrm_1_CemBodyExpoSignalIPdu06:
        sig_name = "DwnLoadDynLitPrmForLedMkrLampLe1ModePrm_1_CemBodyExpoSignalIPdu06"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode1_Off': 0, 'Mode1_On': 1, 'Mode1_GradualOn': 2, 'Mode1_GradualOff': 3, 'Mode1_ForwardWipingOn': 4, 'Mode1_BackwardWipingOn': 5, 'Mode1_OutwardWipingOn': 6, 'Mode1_InwardWipingOn': 7, 'Mode1_ForwardWipingOff': 8, 'Mode1_BackwardWipingOff': 9, 'Mode1_OutwardWipingOff': 10, 'Mode1_InwardWipingOff': 11, 'Mode1_ForwardScanning': 12, 'Mode1_BackwardScanning': 13, 'Mode1_BreathOn': 14, 'Mode1_BreathOff': 15, 'Mode1_Spare1': 16, 'Mode1_Spare2': 17}
        compute_method = None
        length = 5
        startbit = 13
        byte = 1
        mask = 0b00111110
        unmask = 0b11000001
        shift = 1


class CemBodyExpoFr27:
    msg_name = "CemBodyExpoFr27"
    msg_id = 312
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCML']

    class DwnLoadDynLitPrmForLedLoBeamLeUpprBriPrm_1_CemBodyExpoSignalIPdu27:
        sig_name = "DwnLoadDynLitPrmForLedLoBeamLeUpprBriPrm_1_CemBodyExpoSignalIPdu27"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmForLedLoBeamLeOffsTiPrm_1_CemBodyExpoSignalIPdu27:
        sig_name = "DwnLoadDynLitPrmForLedLoBeamLeOffsTiPrm_1_CemBodyExpoSignalIPdu27"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmForLedLoBeamLeLowBriPrm_1_CemBodyExpoSignalIPdu27:
        sig_name = "DwnLoadDynLitPrmForLedLoBeamLeLowBriPrm_1_CemBodyExpoSignalIPdu27"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DwnLoadDynLitPrmForLedLoBeamLeModePrm_1_CemBodyExpoSignalIPdu27:
        sig_name = "DwnLoadDynLitPrmForLedLoBeamLeModePrm_1_CemBodyExpoSignalIPdu27"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Mode1_Off': 0, 'Mode1_On': 1, 'Mode1_GradualOn': 2, 'Mode1_GradualOff': 3, 'Mode1_ForwardWipingOn': 4, 'Mode1_BackwardWipingOn': 5, 'Mode1_OutwardWipingOn': 6, 'Mode1_InwardWipingOn': 7, 'Mode1_ForwardWipingOff': 8, 'Mode1_BackwardWipingOff': 9, 'Mode1_OutwardWipingOff': 10, 'Mode1_InwardWipingOff': 11, 'Mode1_ForwardScanning': 12, 'Mode1_BackwardScanning': 13, 'Mode1_BreathOn': 14, 'Mode1_BreathOff': 15, 'Mode1_Spare1': 16, 'Mode1_Spare2': 17}
        compute_method = None
        length = 5
        startbit = 13
        byte = 1
        mask = 0b00111110
        unmask = 0b11000001
        shift = 1

    class DwnLoadDynLitPrmForLedLoBeamLeTistamp_1_CemBodyExpoSignalIPdu27:
        sig_name = "DwnLoadDynLitPrmForLedLoBeamLeTistamp_1_CemBodyExpoSignalIPdu27"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmForLedLoBeamLeContTiPrm_1_CemBodyExpoSignalIPdu27:
        sig_name = "DwnLoadDynLitPrmForLedLoBeamLeContTiPrm_1_CemBodyExpoSignalIPdu27"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]


class CEMBodyExpoCommonFr07:
    msg_name = "CEMBodyExpoCommonFr07"
    msg_id = 544
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.06
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR', 'RCMR', 'HCML', 'RCMM', 'PCM', 'RCML']

    class ActnOfLedGrilleLamp:
        sig_name = "ActnOfLedGrilleLamp"
        sig_start_bit = 36
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 36
        byte = 4
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class CarTiGlb_6_CEMBodyExpoCommonSignalIPdu07:
        sig_name = "CarTiGlb_6_CEMBodyExpoCommonSignalIPdu07"
        sig_start_bit = 7
        sig_length = 32
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 4294967295
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 32
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class Body2CntrForMissCom:
        sig_name = "Body2CntrForMissCom"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class TrSts_1_CEMBodyExpoCommonSignalIPdu07:
        sig_name = "TrSts_1_CEMBodyExpoCommonSignalIPdu07"
        sig_start_bit = 52
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorSts2_Ukwn': 0, 'DoorSts2_Opend': 1, 'DoorSts2_Clsd': 2}
        compute_method = None
        length = 2
        startbit = 52
        byte = 6
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3


class CemBodyExpoCommonFr13:
    msg_name = "CemBodyExpoCommonFr13"
    msg_id = 392
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.045
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR', 'HCML']

    class VehObjforADB1AdbHozlAgRi_1_CemBodyExpoCommonSignalIPdu13:
        sig_name = "VehObjforADB1AdbHozlAgRi_1_CemBodyExpoCommonSignalIPdu13"
        sig_start_bit = 31
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = "-40"
        sig_value_min = 0
        sig_value_max = 1600
        sig_byteorder = "Motorola"
        sig_value_init = 800
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11100000, 0b00011111, 3, 5)]

    class VehObjforADB1AdbClassn_1_CemBodyExpoCommonSignalIPdu13:
        sig_name = "VehObjforADB1AdbClassn_1_CemBodyExpoCommonSignalIPdu13"
        sig_start_bit = 13
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AdbClassn_NoVehicle': 0, 'AdbClassn_Car': 1, 'AdbClassn_Truck': 2, 'AdbClassn_Bus': 3, 'AdbClassn_BikeOrMotorBike': 4, 'AdbClassn_Pedestrain': 5, 'AdbClassn_Mixed': 6, 'AdbClassn_Unknown': 7}
        compute_method = None
        length = 3
        startbit = 13
        byte = 1
        mask = 0b00111000
        unmask = 0b11000111
        shift = 3

    class VehObjforADB1AdbAbsDist_1_CemBodyExpoCommonSignalIPdu13:
        sig_name = "VehObjforADB1AdbAbsDist_1_CemBodyExpoCommonSignalIPdu13"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class VehObjforADB1AdbHozlAgLe_1_CemBodyExpoCommonSignalIPdu13:
        sig_name = "VehObjforADB1AdbHozlAgLe_1_CemBodyExpoCommonSignalIPdu13"
        sig_start_bit = 10
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = "-40"
        sig_value_min = 0
        sig_value_max = 1600
        sig_byteorder = "Motorola"
        sig_value_init = 800
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 10
        bmuws_info = [(1, 0b00000111, 0b11111000, 3, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class VehObjforADB1AdbObjHozlAgSpdLe_1_CemBodyExpoCommonSignalIPdu13:
        sig_name = "VehObjforADB1AdbObjHozlAgSpdLe_1_CemBodyExpoCommonSignalIPdu13"
        sig_start_bit = 34
        sig_length = 9
        sig_value_factor = 0.2
        sig_value_offset = "-50"
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 250
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 34
        bmuws_info = [(4, 0b00000111, 0b11111000, 3, 0), (5, 0b11111100, 0b00000011, 6, 2)]

    class VehObjforADB1AdbVertAg_1_CemBodyExpoCommonSignalIPdu13:
        sig_name = "VehObjforADB1AdbVertAg_1_CemBodyExpoCommonSignalIPdu13"
        sig_start_bit = 63
        sig_length = 5
        sig_value_factor = 0.5
        sig_value_offset = "-3"
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Motorola"
        sig_value_init = 6
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 63
        byte = 7
        mask = 0b11111000
        unmask = 0b00000111
        shift = 3

    class VehObjforADB1AdbObjDir_1_CemBodyExpoCommonSignalIPdu13:
        sig_name = "VehObjforADB1AdbObjDir_1_CemBodyExpoCommonSignalIPdu13"
        sig_start_bit = 36
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AdbObjDir_Idle': 0, 'AdbObjDir_Oncoming': 1, 'AdbObjDir_Preceding': 2, 'AdbObjDir_Others': 3}
        compute_method = None
        length = 2
        startbit = 36
        byte = 4
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class VehObjforADB1AdbTrkInfo_1_CemBodyExpoCommonSignalIPdu13:
        sig_name = "VehObjforADB1AdbTrkInfo_1_CemBodyExpoCommonSignalIPdu13"
        sig_start_bit = 48
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NotTracked': 0, 'Tracking': 1}
        compute_method = None
        length = 1
        startbit = 48
        byte = 6
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VehObjforADB1AdbObjHozlAgSpdRi_1_CemBodyExpoCommonSignalIPdu13:
        sig_name = "VehObjforADB1AdbObjHozlAgSpdRi_1_CemBodyExpoCommonSignalIPdu13"
        sig_start_bit = 41
        sig_length = 9
        sig_value_factor = 0.2
        sig_value_offset = "-50"
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 250
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 41
        bmuws_info = [(5, 0b00000011, 0b11111100, 2, 0), (6, 0b11111110, 0b00000001, 7, 1)]


class CemBodyExpoCommonFr19:
    msg_name = "CemBodyExpoCommonFr19"
    msg_id = 398
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.045
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR', 'HCML']

    class VehObjforADB7AdbHozlAgRi_1_CemBodyExpoCommonSignalIPdu19:
        sig_name = "VehObjforADB7AdbHozlAgRi_1_CemBodyExpoCommonSignalIPdu19"
        sig_start_bit = 31
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = "-40"
        sig_value_min = 0
        sig_value_max = 1600
        sig_byteorder = "Motorola"
        sig_value_init = 800
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11100000, 0b00011111, 3, 5)]

    class VehObjforADB7AdbObjHozlAgSpdRi_1_CemBodyExpoCommonSignalIPdu19:
        sig_name = "VehObjforADB7AdbObjHozlAgSpdRi_1_CemBodyExpoCommonSignalIPdu19"
        sig_start_bit = 41
        sig_length = 9
        sig_value_factor = 0.2
        sig_value_offset = "-50"
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 250
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 41
        bmuws_info = [(5, 0b00000011, 0b11111100, 2, 0), (6, 0b11111110, 0b00000001, 7, 1)]

    class VehObjforADB7AdbObjDir_1_CemBodyExpoCommonSignalIPdu19:
        sig_name = "VehObjforADB7AdbObjDir_1_CemBodyExpoCommonSignalIPdu19"
        sig_start_bit = 36
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AdbObjDir_Idle': 0, 'AdbObjDir_Oncoming': 1, 'AdbObjDir_Preceding': 2, 'AdbObjDir_Others': 3}
        compute_method = None
        length = 2
        startbit = 36
        byte = 4
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class VehObjforADB7AdbAbsDist_1_CemBodyExpoCommonSignalIPdu19:
        sig_name = "VehObjforADB7AdbAbsDist_1_CemBodyExpoCommonSignalIPdu19"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class VehObjforADB7AdbClassn_1_CemBodyExpoCommonSignalIPdu19:
        sig_name = "VehObjforADB7AdbClassn_1_CemBodyExpoCommonSignalIPdu19"
        sig_start_bit = 13
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AdbClassn_NoVehicle': 0, 'AdbClassn_Car': 1, 'AdbClassn_Truck': 2, 'AdbClassn_Bus': 3, 'AdbClassn_BikeOrMotorBike': 4, 'AdbClassn_Pedestrain': 5, 'AdbClassn_Mixed': 6, 'AdbClassn_Unknown': 7}
        compute_method = None
        length = 3
        startbit = 13
        byte = 1
        mask = 0b00111000
        unmask = 0b11000111
        shift = 3

    class VehObjforADB7AdbTrkInfo_1_CemBodyExpoCommonSignalIPdu19:
        sig_name = "VehObjforADB7AdbTrkInfo_1_CemBodyExpoCommonSignalIPdu19"
        sig_start_bit = 48
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NotTracked': 0, 'Tracking': 1}
        compute_method = None
        length = 1
        startbit = 48
        byte = 6
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VehObjforADB7AdbObjHozlAgSpdLe_1_CemBodyExpoCommonSignalIPdu19:
        sig_name = "VehObjforADB7AdbObjHozlAgSpdLe_1_CemBodyExpoCommonSignalIPdu19"
        sig_start_bit = 34
        sig_length = 9
        sig_value_factor = 0.2
        sig_value_offset = "-50"
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 250
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 34
        bmuws_info = [(4, 0b00000111, 0b11111000, 3, 0), (5, 0b11111100, 0b00000011, 6, 2)]

    class VehObjforADB7AdbHozlAgLe_1_CemBodyExpoCommonSignalIPdu19:
        sig_name = "VehObjforADB7AdbHozlAgLe_1_CemBodyExpoCommonSignalIPdu19"
        sig_start_bit = 10
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = "-40"
        sig_value_min = 0
        sig_value_max = 1600
        sig_byteorder = "Motorola"
        sig_value_init = 800
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 10
        bmuws_info = [(1, 0b00000111, 0b11111000, 3, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class VehObjforADB7AdbVertAg_1_CemBodyExpoCommonSignalIPdu19:
        sig_name = "VehObjforADB7AdbVertAg_1_CemBodyExpoCommonSignalIPdu19"
        sig_start_bit = 63
        sig_length = 5
        sig_value_factor = 0.5
        sig_value_offset = "-3"
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Motorola"
        sig_value_init = 6
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 63
        byte = 7
        mask = 0b11111000
        unmask = 0b00000111
        shift = 3


class CemBodyExpoFr62:
    msg_name = "CemBodyExpoFr62"
    msg_id = 788
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.94
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RCMR', 'RCML', 'RCMM']

    class DHUcontrolmiddlecorneringlamp:
        sig_name = "DHUcontrolmiddlecorneringlamp"
        sig_start_bit = 21
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffNoReq_NoReq': 0, 'OnOffNoReq_On': 1, 'OnOffNoReq_Off': 2}
        compute_method = None
        length = 2
        startbit = 21
        byte = 2
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class DHUcontrolLedStopLampRi2:
        sig_name = "DHUcontrolLedStopLampRi2"
        sig_start_bit = 9
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffNoReq_NoReq': 0, 'OnOffNoReq_On': 1, 'OnOffNoReq_Off': 2}
        compute_method = None
        length = 2
        startbit = 9
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class DHUcontrolLedMkrLampLe2:
        sig_name = "DHUcontrolLedMkrLampLe2"
        sig_start_bit = 5
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffNoReq_NoReq': 0, 'OnOffNoReq_On': 1, 'OnOffNoReq_Off': 2}
        compute_method = None
        length = 2
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class DHUcontrolLedStopLampLe2:
        sig_name = "DHUcontrolLedStopLampLe2"
        sig_start_bit = 13
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffNoReq_NoReq': 0, 'OnOffNoReq_On': 1, 'OnOffNoReq_Off': 2}
        compute_method = None
        length = 2
        startbit = 13
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class DHUcontrolLedMkrLampRi1:
        sig_name = "DHUcontrolLedMkrLampRi1"
        sig_start_bit = 3
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffNoReq_NoReq': 0, 'OnOffNoReq_On': 1, 'OnOffNoReq_Off': 2}
        compute_method = None
        length = 2
        startbit = 3
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class DHUcontrolmiddlepositionlight:
        sig_name = "DHUcontrolmiddlepositionlight"
        sig_start_bit = 19
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffNoReq_NoReq': 0, 'OnOffNoReq_On': 1, 'OnOffNoReq_Off': 2}
        compute_method = None
        length = 2
        startbit = 19
        byte = 2
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class DHUcontrolLedMkrLampRi2:
        sig_name = "DHUcontrolLedMkrLampRi2"
        sig_start_bit = 1
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffNoReq_NoReq': 0, 'OnOffNoReq_On': 1, 'OnOffNoReq_Off': 2}
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class DHUcontrolmiddlebrakelight:
        sig_name = "DHUcontrolmiddlebrakelight"
        sig_start_bit = 23
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffNoReq_NoReq': 0, 'OnOffNoReq_On': 1, 'OnOffNoReq_Off': 2}
        compute_method = None
        length = 2
        startbit = 23
        byte = 2
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class DHUcontrolLedMkrLampLe1:
        sig_name = "DHUcontrolLedMkrLampLe1"
        sig_start_bit = 7
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffNoReq_NoReq': 0, 'OnOffNoReq_On': 1, 'OnOffNoReq_Off': 2}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class DHUcontrolLedStopLampLe1:
        sig_name = "DHUcontrolLedStopLampLe1"
        sig_start_bit = 15
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffNoReq_NoReq': 0, 'OnOffNoReq_On': 1, 'OnOffNoReq_Off': 2}
        compute_method = None
        length = 2
        startbit = 15
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class DHUcontrolLedStopLampRi1:
        sig_name = "DHUcontrolLedStopLampRi1"
        sig_start_bit = 11
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffNoReq_NoReq': 0, 'OnOffNoReq_On': 1, 'OnOffNoReq_Off': 2}
        compute_method = None
        length = 2
        startbit = 11
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2


class RcmmBodyExposedCANNmFr:
    msg_name = "RcmmBodyExposedCANNmFr"
    msg_id = 1333
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "RCMM"
    rx_nodes = ['PCM']


class CemBodyExpoFr41:
    msg_name = "CemBodyExpoFr41"
    msg_id = 377
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.065
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR', 'HCML']

    class ADataRawSafeALat_1_CemBodyExpoSignalIPdu41:
        sig_name = "ADataRawSafeALat_1_CemBodyExpoSignalIPdu41"
        sig_start_bit = 23
        sig_length = 15
        sig_value_factor = 0.0085
        sig_value_offset = 0.0
        sig_value_min = -16352
        sig_value_max = 16353
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111110, 0b00000001, 7, 1)]

    class ADataRawSafeALat1Qf_1_CemBodyExpoSignalIPdu41:
        sig_name = "ADataRawSafeALat1Qf_1_CemBodyExpoSignalIPdu41"
        sig_start_bit = 11
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Qf1_DevOfDataUndefd': 0, 'Qf1_DataTmpUndefdAndEvlnInProgs': 1, 'Qf1_DevOfDataNotWithinRngAllwd': 2, 'Qf1_DataCalcdWithDevDefd': 3}
        compute_method = None
        length = 2
        startbit = 11
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class ADataRawSafeChks_1_CemBodyExpoSignalIPdu41:
        sig_name = "ADataRawSafeChks_1_CemBodyExpoSignalIPdu41"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 255
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ADataRawSafeAVert_1_CemBodyExpoSignalIPdu41:
        sig_name = "ADataRawSafeAVert_1_CemBodyExpoSignalIPdu41"
        sig_start_bit = 55
        sig_length = 15
        sig_value_factor = 0.0085
        sig_value_offset = 0.0
        sig_value_min = -16352
        sig_value_max = 16353
        sig_byteorder = "Motorola"
        sig_value_init = 1155
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 55
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111110, 0b00000001, 7, 1)]

    class ADataRawSafeAVertQf_1_CemBodyExpoSignalIPdu41:
        sig_name = "ADataRawSafeAVertQf_1_CemBodyExpoSignalIPdu41"
        sig_start_bit = 24
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Qf1_DevOfDataUndefd': 0, 'Qf1_DataTmpUndefdAndEvlnInProgs': 1, 'Qf1_DevOfDataNotWithinRngAllwd': 2, 'Qf1_DataCalcdWithDevDefd': 3}
        compute_method = None
        length = 2
        startbit = 24
        bmuws_info = [(3, 0b00000001, 0b11111110, 1, 0), (4, 0b10000000, 0b01111111, 1, 7)]

    class ADataRawSafeCntr_1_CemBodyExpoSignalIPdu41:
        sig_name = "ADataRawSafeCntr_1_CemBodyExpoSignalIPdu41"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class ADataRawSafeALgt_1_CemBodyExpoSignalIPdu41:
        sig_name = "ADataRawSafeALgt_1_CemBodyExpoSignalIPdu41"
        sig_start_bit = 38
        sig_length = 15
        sig_value_factor = 0.0085
        sig_value_offset = 0.0
        sig_value_min = -16352
        sig_value_max = 16353
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 38
        bmuws_info = [(4, 0b01111111, 0b10000000, 7, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class ADataRawSafeALgt1Qf_1_CemBodyExpoSignalIPdu41:
        sig_name = "ADataRawSafeALgt1Qf_1_CemBodyExpoSignalIPdu41"
        sig_start_bit = 9
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Qf1_DevOfDataUndefd': 0, 'Qf1_DataTmpUndefdAndEvlnInProgs': 1, 'Qf1_DevOfDataNotWithinRngAllwd': 2, 'Qf1_DataCalcdWithDevDefd': 3}
        compute_method = None
        length = 2
        startbit = 9
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0


