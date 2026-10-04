class CemBodyExpoFr57:
    msg_name = "CemBodyExpoFr57"
    msg_id = 331
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLitPrmLedRePosnLampRi4ContTiPrm:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi4ContTiPrm"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedRePosnLampRi4LowBriPrm:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi4LowBriPrm"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmLedRePosnLampRi4ModePrm:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi4ModePrm"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
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

    class DwnLoadDynLitPrmLedRePosnLampRi4Tistamp:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi4Tistamp"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmLedRePosnLampRi4UpprBriPrm:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi4UpprBriPrm"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmLedRePosnLampRi4OffsTiPrm:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi4OffsTiPrm"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]


class CemBodyExpoFr19:
    msg_name = "CemBodyExpoFr19"
    msg_id = 305
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLitPrmLedReTurnIndcrLe1UpprBriPrm:
        sig_name = "DwnLoadDynLitPrmLedReTurnIndcrLe1UpprBriPrm"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmLedReTurnIndcrLe1Tistamp:
        sig_name = "DwnLoadDynLitPrmLedReTurnIndcrLe1Tistamp"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmLedReTurnIndcrLe1ModePrm:
        sig_name = "DwnLoadDynLitPrmLedReTurnIndcrLe1ModePrm"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
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

    class DwnLoadDynLitPrmLedReTurnIndcrLe1ContTiPrm:
        sig_name = "DwnLoadDynLitPrmLedReTurnIndcrLe1ContTiPrm"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedReTurnIndcrLe1OffsTiPrm:
        sig_name = "DwnLoadDynLitPrmLedReTurnIndcrLe1OffsTiPrm"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedReTurnIndcrLe1LowBriPrm:
        sig_name = "DwnLoadDynLitPrmLedReTurnIndcrLe1LowBriPrm"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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


class HcmrBodyExpoFr04:
    msg_name = "HcmrBodyExpoFr04"
    msg_id = 127
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class HdlampRiInpSts2:
        sig_name = "HdlampRiInpSts2"
        sig_start_bit = 63
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class DwnLoadStsFbOfHdlampRi:
        sig_name = "DwnLoadStsFbOfHdlampRi"
        sig_start_bit = 5
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class StsOfFrntSideMkrLampRi2:
        sig_name = "StsOfFrntSideMkrLampRi2"
        sig_start_bit = 9
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class ExtrLiShowActvnFrntRiFb:
        sig_name = "ExtrLiShowActvnFrntRiFb"
        sig_start_bit = 28
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class StsOfSwvlgRi:
        sig_name = "StsOfSwvlgRi"
        sig_start_bit = 7
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class StsOfTouristModRi:
        sig_name = "StsOfTouristModRi"
        sig_start_bit = 25
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class StsOfLvlgRiCntr:
        sig_name = "StsOfLvlgRiCntr"
        sig_start_bit = 55
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class StsOfAfsRi:
        sig_name = "StsOfAfsRi"
        sig_start_bit = 1
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class StsOfLedFrntFogLampRi:
        sig_name = "StsOfLedFrntFogLampRi"
        sig_start_bit = 15
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class HdlampRiInpSts1:
        sig_name = "HdlampRiInpSts1"
        sig_start_bit = 49
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class StsOfLedDaytiRunngLampRi:
        sig_name = "StsOfLedDaytiRunngLampRi"
        sig_start_bit = 13
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class StsOfLvlgRiChks:
        sig_name = "StsOfLvlgRiChks"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class StsOfLedFrntPosnLampRi:
        sig_name = "StsOfLedFrntPosnLampRi"
        sig_start_bit = 17
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class StsOfLvlgRiStsOfLvlgRi:
        sig_name = "StsOfLvlgRiStsOfLvlgRi"
        sig_start_bit = 51
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class StsOfWelGbyFrntRi:
        sig_name = "StsOfWelGbyFrntRi"
        sig_start_bit = 61
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class StsOfLedCornrgLampRi:
        sig_name = "StsOfLedCornrgLampRi"
        sig_start_bit = 11
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class StsOfLedFrntTurnIndcrRi:
        sig_name = "StsOfLedFrntTurnIndcrRi"
        sig_start_bit = 19
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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


class CemBodyExpoFr56:
    msg_name = "CemBodyExpoFr56"
    msg_id = 330
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLitPrmLedRePosnLampRi3ModePrm:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi3ModePrm"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
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

    class DwnLoadDynLitPrmLedRePosnLampRi3ContTiPrm:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi3ContTiPrm"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedRePosnLampRi3OffsTiPrm:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi3OffsTiPrm"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedRePosnLampRi3Tistamp:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi3Tistamp"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmLedRePosnLampRi3LowBriPrm:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi3LowBriPrm"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmLedRePosnLampRi3UpprBriPrm:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi3UpprBriPrm"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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


class CemBodyExpoFr28:
    msg_name = "CemBodyExpoFr28"
    msg_id = 313
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForLedAllWthrLampLeModePrm:
        sig_name = "DwnLoadDynLtgPrmForLedAllWthrLampLeModePrm"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
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

    class DwnLoadDynLtgPrmForLedAllWthrLampLeLowBriPrm:
        sig_name = "DwnLoadDynLtgPrmForLedAllWthrLampLeLowBriPrm"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLtgPrmForLedAllWthrLampLeContTiPrm:
        sig_name = "DwnLoadDynLtgPrmForLedAllWthrLampLeContTiPrm"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLtgPrmForLedAllWthrLampLeUpprBriPrm:
        sig_name = "DwnLoadDynLtgPrmForLedAllWthrLampLeUpprBriPrm"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLtgPrmForLedAllWthrLampLeOffsTiPrm:
        sig_name = "DwnLoadDynLtgPrmForLedAllWthrLampLeOffsTiPrm"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLtgPrmForLedAllWthrLampLeTistamp:
        sig_name = "DwnLoadDynLtgPrmForLedAllWthrLampLeTistamp"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]


class CemBodyExpoFr86:
    msg_name = "CemBodyExpoFr86"
    msg_id = 820
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForFrntLeGrp20HighBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp20HighBrightness"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntLeGrp20Timestamp:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp20Timestamp"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DwnLoadDynLtgPrmForFrntLeGrp20LowBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp20LowBrightness"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntLeGrp20OffsetTime:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp20OffsetTime"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
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

    class DwnLoadDynLtgPrmForFrntLeGrp20Mode1:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp20Mode1"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
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

    class DwnLoadDynLtgPrmForFrntLeGrp20ContinueTime:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp20ContinueTime"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
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


class CemBodyExpoFr105:
    msg_name = "CemBodyExpoFr105"
    msg_id = 839
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForFrntRIGrp15Mode1:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp15Mode1"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
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

    class DwnLoadDynLtgPrmForFrntRIGrp15LowBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp15LowBrightness"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntRIGrp15OffsetTime:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp15OffsetTime"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
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

    class DwnLoadDynLtgPrmForFrntRIGrp15ContinueTime:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp15ContinueTime"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
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

    class DwnLoadDynLtgPrmForFrntRIGrp15Timestamp:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp15Timestamp"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DwnLoadDynLtgPrmForFrntRIGrp15HighBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp15HighBrightness"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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


class CemBodyExpoCommonFr10:
    msg_name = "CemBodyExpoCommonFr10"
    msg_id = 389
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.045
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class TrafficSignForADB1AdbTrkInfo:
        sig_name = "TrafficSignForADB1AdbTrkInfo"
        sig_start_bit = 42
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class TrafficSignForADB1AdbVertAgTop:
        sig_name = "TrafficSignForADB1AdbVertAgTop"
        sig_start_bit = 41
        sig_length = 9
        sig_value_factor = 0.05
        sig_value_offset = "-3"
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 60
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 41
        bmuws_info = [(5, 0b00000011, 0b11111100, 2, 0), (6, 0b11111110, 0b00000001, 7, 1)]

    class TrafficSignForADB1AdbHozlAgRi:
        sig_name = "TrafficSignForADB1AdbHozlAgRi"
        sig_start_bit = 30
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = "-40"
        sig_value_min = 0
        sig_value_max = 1600
        sig_value_init = 800
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 30
        bmuws_info = [(3, 0b01111111, 0b10000000, 7, 0), (4, 0b11110000, 0b00001111, 4, 4)]

    class TrafficSignForADB1AdbVertAgBot:
        sig_name = "TrafficSignForADB1AdbVertAgBot"
        sig_start_bit = 35
        sig_length = 9
        sig_value_factor = 0.05
        sig_value_offset = "-3"
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 60
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 35
        bmuws_info = [(4, 0b00001111, 0b11110000, 4, 0), (5, 0b11111000, 0b00000111, 5, 3)]

    class TrafficSignForADB1AdbHozlAgLe:
        sig_name = "TrafficSignForADB1AdbHozlAgLe"
        sig_start_bit = 9
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = "-40"
        sig_value_min = 0
        sig_value_max = 1600
        sig_value_init = 800
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 9
        bmuws_info = [(1, 0b00000011, 0b11111100, 2, 0), (2, 0b11111111, 0b00000000, 8, 0), (3, 0b10000000, 0b01111111, 1, 7)]

    class TrafficSignForADB1AdbDetdQly:
        sig_name = "TrafficSignForADB1AdbDetdQly"
        sig_start_bit = 11
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
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

    class TrafficSignForADB1AdbAbsDist:
        sig_name = "TrafficSignForADB1AdbAbsDist"
        sig_start_bit = 7
        sig_length = 12
        sig_value_factor = 0.2
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11110000, 0b00001111, 4, 4)]


class BgmBodyExposedCANNmFr:
    msg_name = "BgmBodyExposedCANNmFr"
    msg_id = 1322
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []


class CemBodyExpoCommonFr17:
    msg_name = "CemBodyExpoCommonFr17"
    msg_id = 396
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.045
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class VehObjforADB5AdbClassn:
        sig_name = "VehObjforADB5AdbClassn"
        sig_start_bit = 13
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
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

    class VehObjforADB5AdbHozlAgRi:
        sig_name = "VehObjforADB5AdbHozlAgRi"
        sig_start_bit = 31
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = "-40"
        sig_value_min = 0
        sig_value_max = 1600
        sig_value_init = 800
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11100000, 0b00011111, 3, 5)]

    class VehObjforADB5AdbAbsDist:
        sig_name = "VehObjforADB5AdbAbsDist"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class VehObjforADB5AdbObjDir:
        sig_name = "VehObjforADB5AdbObjDir"
        sig_start_bit = 36
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class VehObjforADB5AdbObjHozlAgSpdLe:
        sig_name = "VehObjforADB5AdbObjHozlAgSpdLe"
        sig_start_bit = 34
        sig_length = 9
        sig_value_factor = 0.2
        sig_value_offset = "-50"
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 250
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 34
        bmuws_info = [(4, 0b00000111, 0b11111000, 3, 0), (5, 0b11111100, 0b00000011, 6, 2)]

    class VehObjforADB5AdbObjHozlAgSpdRi:
        sig_name = "VehObjforADB5AdbObjHozlAgSpdRi"
        sig_start_bit = 41
        sig_length = 9
        sig_value_factor = 0.2
        sig_value_offset = "-50"
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 250
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 41
        bmuws_info = [(5, 0b00000011, 0b11111100, 2, 0), (6, 0b11111110, 0b00000001, 7, 1)]

    class VehObjforADB5AdbTrkInfo:
        sig_name = "VehObjforADB5AdbTrkInfo"
        sig_start_bit = 48
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class VehObjforADB5AdbVertAg:
        sig_name = "VehObjforADB5AdbVertAg"
        sig_start_bit = 63
        sig_length = 5
        sig_value_factor = 0.5
        sig_value_offset = "-3"
        sig_value_min = 0
        sig_value_max = 31
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

    class VehObjforADB5AdbHozlAgLe:
        sig_name = "VehObjforADB5AdbHozlAgLe"
        sig_start_bit = 10
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = "-40"
        sig_value_min = 0
        sig_value_max = 1600
        sig_value_init = 800
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 10
        bmuws_info = [(1, 0b00000111, 0b11111000, 3, 0), (2, 0b11111111, 0b00000000, 8, 0)]


class CemBodyExpoFr53:
    msg_name = "CemBodyExpoFr53"
    msg_id = 327
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLitPrmLedRePosnLampLe3OffsTiPrm:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe3OffsTiPrm"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedRePosnLampLe3Tistamp:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe3Tistamp"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmLedRePosnLampLe3ContTiPrm:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe3ContTiPrm"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedRePosnLampLe3UpprBriPrm:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe3UpprBriPrm"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmLedRePosnLampLe3LowBriPrm:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe3LowBriPrm"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmLedRePosnLampLe3ModePrm:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe3ModePrm"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
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


class CemBodyExpoFr73:
    msg_name = "CemBodyExpoFr73"
    msg_id = 807
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForFrntLeGrp7Timestamp:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp7Timestamp"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DwnLoadDynLtgPrmForFrntLeGrp7HighBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp7HighBrightness"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntLeGrp7Mode1:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp7Mode1"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
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

    class DwnLoadDynLtgPrmForFrntLeGrp7ContinueTime:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp7ContinueTime"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
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

    class DwnLoadDynLtgPrmForFrntLeGrp7LowBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp7LowBrightness"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntLeGrp7OffsetTime:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp7OffsetTime"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
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


class CemBodyExpoFr11:
    msg_name = "CemBodyExpoFr11"
    msg_id = 297
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLitPrmForLedStopLampLe2ModePrm:
        sig_name = "DwnLoadDynLitPrmForLedStopLampLe2ModePrm"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
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

    class DwnLoadDynLitPrmForLedStopLampLe2OffsTiPrm:
        sig_name = "DwnLoadDynLitPrmForLedStopLampLe2OffsTiPrm"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmForLedStopLampLe2LowBriPrm:
        sig_name = "DwnLoadDynLitPrmForLedStopLampLe2LowBriPrm"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmForLedStopLampLe2Tistamp:
        sig_name = "DwnLoadDynLitPrmForLedStopLampLe2Tistamp"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmForLedStopLampLe2ContTiPrm:
        sig_name = "DwnLoadDynLitPrmForLedStopLampLe2ContTiPrm"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmForLedStopLampLe2UpprBriPrm:
        sig_name = "DwnLoadDynLitPrmForLedStopLampLe2UpprBriPrm"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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


class CemBodyExpoFr22:
    msg_name = "CemBodyExpoFr22"
    msg_id = 308
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLitPrmLedRvsgLampLe1ModePrm:
        sig_name = "DwnLoadDynLitPrmLedRvsgLampLe1ModePrm"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
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

    class DwnLoadDynLitPrmLedRvsgLampLe1UpprBriPrm:
        sig_name = "DwnLoadDynLitPrmLedRvsgLampLe1UpprBriPrm"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmLedRvsgLampLe1ContTiPrm:
        sig_name = "DwnLoadDynLitPrmLedRvsgLampLe1ContTiPrm"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedRvsgLampLe1Tistamp:
        sig_name = "DwnLoadDynLitPrmLedRvsgLampLe1Tistamp"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmLedRvsgLampLe1LowBriPrm:
        sig_name = "DwnLoadDynLitPrmLedRvsgLampLe1LowBriPrm"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmLedRvsgLampLe1OffsTiPrm:
        sig_name = "DwnLoadDynLitPrmLedRvsgLampLe1OffsTiPrm"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]


class CemBodyExpoFr13:
    msg_name = "CemBodyExpoFr13"
    msg_id = 299
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLitPrmLedReFogLampLe1ModePrm:
        sig_name = "DwnLoadDynLitPrmLedReFogLampLe1ModePrm"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
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

    class DwnLoadDynLitPrmLedReFogLampLe1ContTiPrm:
        sig_name = "DwnLoadDynLitPrmLedReFogLampLe1ContTiPrm"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedReFogLampLe1OffsTiPrm:
        sig_name = "DwnLoadDynLitPrmLedReFogLampLe1OffsTiPrm"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedReFogLampLe1UpprBriPrm:
        sig_name = "DwnLoadDynLitPrmLedReFogLampLe1UpprBriPrm"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmLedReFogLampLe1Tistamp:
        sig_name = "DwnLoadDynLitPrmLedReFogLampLe1Tistamp"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmLedReFogLampLe1LowBriPrm:
        sig_name = "DwnLoadDynLitPrmLedReFogLampLe1LowBriPrm"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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


class CemBodyExpoFr34:
    msg_name = "CemBodyExpoFr34"
    msg_id = 319
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForLedFrntPosnLampLeContTiPrm:
        sig_name = "DwnLoadDynLtgPrmForLedFrntPosnLampLeContTiPrm"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLtgPrmForLedFrntPosnLampLeUpprBriPrm:
        sig_name = "DwnLoadDynLtgPrmForLedFrntPosnLampLeUpprBriPrm"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLtgPrmForLedFrntPosnLampLeLowBriPrm:
        sig_name = "DwnLoadDynLtgPrmForLedFrntPosnLampLeLowBriPrm"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLtgPrmForLedFrntPosnLampLeOffsTiPrm:
        sig_name = "DwnLoadDynLtgPrmForLedFrntPosnLampLeOffsTiPrm"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLtgPrmForLedFrntPosnLampLeTistamp:
        sig_name = "DwnLoadDynLtgPrmForLedFrntPosnLampLeTistamp"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLtgPrmForLedFrntPosnLampLeModePrm:
        sig_name = "DwnLoadDynLtgPrmForLedFrntPosnLampLeModePrm"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
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


class CemBodyExpoCommonFr15:
    msg_name = "CemBodyExpoCommonFr15"
    msg_id = 394
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.045
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class VehObjforADB3AdbHozlAgLe:
        sig_name = "VehObjforADB3AdbHozlAgLe"
        sig_start_bit = 10
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = "-40"
        sig_value_min = 0
        sig_value_max = 1600
        sig_value_init = 800
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 10
        bmuws_info = [(1, 0b00000111, 0b11111000, 3, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class VehObjforADB3AdbTrkInfo:
        sig_name = "VehObjforADB3AdbTrkInfo"
        sig_start_bit = 48
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class VehObjforADB3AdbAbsDist:
        sig_name = "VehObjforADB3AdbAbsDist"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class VehObjforADB3AdbObjHozlAgSpdLe:
        sig_name = "VehObjforADB3AdbObjHozlAgSpdLe"
        sig_start_bit = 34
        sig_length = 9
        sig_value_factor = 0.2
        sig_value_offset = "-50"
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 250
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 34
        bmuws_info = [(4, 0b00000111, 0b11111000, 3, 0), (5, 0b11111100, 0b00000011, 6, 2)]

    class VehObjforADB3AdbClassn:
        sig_name = "VehObjforADB3AdbClassn"
        sig_start_bit = 13
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
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

    class VehObjforADB3AdbVertAg:
        sig_name = "VehObjforADB3AdbVertAg"
        sig_start_bit = 63
        sig_length = 5
        sig_value_factor = 0.5
        sig_value_offset = "-3"
        sig_value_min = 0
        sig_value_max = 31
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

    class VehObjforADB3AdbObjDir:
        sig_name = "VehObjforADB3AdbObjDir"
        sig_start_bit = 36
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class VehObjforADB3AdbHozlAgRi:
        sig_name = "VehObjforADB3AdbHozlAgRi"
        sig_start_bit = 31
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = "-40"
        sig_value_min = 0
        sig_value_max = 1600
        sig_value_init = 800
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11100000, 0b00011111, 3, 5)]

    class VehObjforADB3AdbObjHozlAgSpdRi:
        sig_name = "VehObjforADB3AdbObjHozlAgSpdRi"
        sig_start_bit = 41
        sig_length = 9
        sig_value_factor = 0.2
        sig_value_offset = "-50"
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 250
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 41
        bmuws_info = [(5, 0b00000011, 0b11111100, 2, 0), (6, 0b11111110, 0b00000001, 7, 1)]


class CemBodyExpoFr103:
    msg_name = "CemBodyExpoFr103"
    msg_id = 837
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForFrntRIGrp13OffsetTime:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp13OffsetTime"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
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

    class DwnLoadDynLtgPrmForFrntRIGrp13HighBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp13HighBrightness"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntRIGrp13ContinueTime:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp13ContinueTime"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
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

    class DwnLoadDynLtgPrmForFrntRIGrp13Mode1:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp13Mode1"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
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

    class DwnLoadDynLtgPrmForFrntRIGrp13LowBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp13LowBrightness"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntRIGrp13Timestamp:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp13Timestamp"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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


class CemBodyExpoCommonFr02:
    msg_name = "CemBodyExpoCommonFr02"
    msg_id = 768
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.045
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class BrkPedlrRatQf:
        sig_name = "BrkPedlrRatQf"
        sig_start_bit = 63
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class ActvnOfRvsg:
        sig_name = "ActvnOfRvsg"
        sig_start_bit = 23
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class BrkPedlrRatPerc:
        sig_name = "BrkPedlrRatPerc"
        sig_start_bit = 46
        sig_length = 15
        sig_value_factor = 0.00390625
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 25600
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 46
        bmuws_info = [(5, 0b01111111, 0b10000000, 7, 0), (6, 0b11111111, 0b00000000, 8, 0)]

    class YawRateReqdByDrvr:
        sig_name = "YawRateReqdByDrvr"
        sig_start_bit = 7
        sig_length = 16
        sig_value_factor = "2.44140625E-4"
        sig_value_offset = 0.0
        sig_value_min = -20480
        sig_value_max = 20480
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0)]


class CemBodyExpoFr24:
    msg_name = "CemBodyExpoFr24"
    msg_id = 310
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLitPrmLedRvsgLampRi1LowBriPrm:
        sig_name = "DwnLoadDynLitPrmLedRvsgLampRi1LowBriPrm"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmLedRvsgLampRi1ModePrm:
        sig_name = "DwnLoadDynLitPrmLedRvsgLampRi1ModePrm"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
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

    class DwnLoadDynLitPrmLedRvsgLampRi1OffsTiPrm:
        sig_name = "DwnLoadDynLitPrmLedRvsgLampRi1OffsTiPrm"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedRvsgLampRi1Tistamp:
        sig_name = "DwnLoadDynLitPrmLedRvsgLampRi1Tistamp"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmLedRvsgLampRi1UpprBriPrm:
        sig_name = "DwnLoadDynLitPrmLedRvsgLampRi1UpprBriPrm"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmLedRvsgLampRi1ContTiPrm:
        sig_name = "DwnLoadDynLitPrmLedRvsgLampRi1ContTiPrm"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]


class CemBodyExpoFr42:
    msg_name = "CemBodyExpoFr42"
    msg_id = 381
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.065
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class AgDataRawSafeYawRateQf:
        sig_name = "AgDataRawSafeYawRateQf"
        sig_start_bit = 41
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class AgDataRawSafeYawRate:
        sig_name = "AgDataRawSafeYawRate"
        sig_start_bit = 23
        sig_length = 16
        sig_value_factor = "2.44140625E-4"
        sig_value_offset = 0.0
        sig_value_min = -24576
        sig_value_max = 24576
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

    class AgDataRawSafeRollRateQf:
        sig_name = "AgDataRawSafeRollRateQf"
        sig_start_bit = 43
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class AgDataRawSafeCntr:
        sig_name = "AgDataRawSafeCntr"
        sig_start_bit = 47
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class AgDataRawSafeRollRate:
        sig_name = "AgDataRawSafeRollRate"
        sig_start_bit = 7
        sig_length = 16
        sig_value_factor = "2.44140625E-4"
        sig_value_offset = 0.0
        sig_value_min = -24576
        sig_value_max = 24576
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class ActnOfLedPosnLampDyn:
        sig_name = "ActnOfLedPosnLampDyn"
        sig_start_bit = 53
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class AgDataRawSafeChks:
        sig_name = "AgDataRawSafeChks"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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


class CemBodyExpoFr48:
    msg_name = "CemBodyExpoFr48"
    msg_id = 324
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLitPrmForLedMkrLampRi2ContTiPrm:
        sig_name = "DwnLoadDynLitPrmForLedMkrLampRi2ContTiPrm"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmForLedMkrLampRi2LowBriPrm:
        sig_name = "DwnLoadDynLitPrmForLedMkrLampRi2LowBriPrm"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmForLedMkrLampRi2UpprBriPrm:
        sig_name = "DwnLoadDynLitPrmForLedMkrLampRi2UpprBriPrm"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmForLedMkrLampRi2Tistamp:
        sig_name = "DwnLoadDynLitPrmForLedMkrLampRi2Tistamp"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmForLedMkrLampRi2ModePrm:
        sig_name = "DwnLoadDynLitPrmForLedMkrLampRi2ModePrm"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
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

    class DwnLoadDynLitPrmForLedMkrLampRi2OffsTiPrm:
        sig_name = "DwnLoadDynLitPrmForLedMkrLampRi2OffsTiPrm"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]


class CemBodyExpoFr92:
    msg_name = "CemBodyExpoFr92"
    msg_id = 826
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForFrntRIGrp2LowBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp2LowBrightness"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntRIGrp2ContinueTime:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp2ContinueTime"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
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

    class DwnLoadDynLtgPrmForFrntRIGrp2Timestamp:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp2Timestamp"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DwnLoadDynLtgPrmForFrntRIGrp2HighBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp2HighBrightness"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntRIGrp2OffsetTime:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp2OffsetTime"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
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

    class DwnLoadDynLtgPrmForFrntRIGrp2Mode1:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp2Mode1"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
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


class BgmToAllFuncBodyExpoDiagReqFrame:
    msg_name = "BgmToAllFuncBodyExpoDiagReqFrame"
    msg_id = 2047
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []


class CemBodyExpoFr54:
    msg_name = "CemBodyExpoFr54"
    msg_id = 328
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLitPrmLedRePosnLampLe4ModePrm:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe4ModePrm"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
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

    class DwnLoadDynLitPrmLedRePosnLampLe4ContTiPrm:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe4ContTiPrm"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedRePosnLampLe4Tistamp:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe4Tistamp"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmLedRePosnLampLe4UpprBriPrm:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe4UpprBriPrm"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmLedRePosnLampLe4LowBriPrm:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe4LowBriPrm"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmLedRePosnLampLe4OffsTiPrm:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe4OffsTiPrm"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]


class CemBodyExpoFr89:
    msg_name = "CemBodyExpoFr89"
    msg_id = 823
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForFrntLeGrp23Timestamp:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp23Timestamp"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DwnLoadDynLtgPrmForFrntLeGrp23HighBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp23HighBrightness"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntLeGrp23ContinueTime:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp23ContinueTime"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
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

    class DwnLoadDynLtgPrmForFrntLeGrp23LowBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp23LowBrightness"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntLeGrp23Mode1:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp23Mode1"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
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

    class DwnLoadDynLtgPrmForFrntLeGrp23OffsetTime:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp23OffsetTime"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
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


class BgmToHcmmBodyExpoDiagReqFrame:
    msg_name = "BgmToHcmmBodyExpoDiagReqFrame"
    msg_id = 1970
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []


class CemBodyExpoDevDiagFr01:
    msg_name = "CemBodyExpoDevDiagFr01"
    msg_id = 1432
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class CEMdevelpsignalgrouprespFunctiondevpsignalgroup5:
        sig_name = "CEMdevelpsignalgrouprespFunctiondevpsignalgroup5"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CEMdevelpsignalgrouprespFunctiondevpsignalgroup6:
        sig_name = "CEMdevelpsignalgrouprespFunctiondevpsignalgroup6"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CEMdevelpsignalgrouprespFunctiondevpsignalgroup1:
        sig_name = "CEMdevelpsignalgrouprespFunctiondevpsignalgroup1"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CEMdevelpsignalgrouprespFunctiondevpsignalgroup8:
        sig_name = "CEMdevelpsignalgrouprespFunctiondevpsignalgroup8"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CEMdevelpsignalgrouprespFunctiondevpsignalgroup3:
        sig_name = "CEMdevelpsignalgrouprespFunctiondevpsignalgroup3"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CEMdevelpsignalgrouprespFunctiondevpsignalgroup7:
        sig_name = "CEMdevelpsignalgrouprespFunctiondevpsignalgroup7"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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


class CemBodyExpoFr99:
    msg_name = "CemBodyExpoFr99"
    msg_id = 833
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForFrntRIGrp9ContinueTime:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp9ContinueTime"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
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

    class DwnLoadDynLtgPrmForFrntRIGrp9Timestamp:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp9Timestamp"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DwnLoadDynLtgPrmForFrntRIGrp9OffsetTime:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp9OffsetTime"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
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

    class DwnLoadDynLtgPrmForFrntRIGrp9HighBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp9HighBrightness"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntRIGrp9Mode1:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp9Mode1"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
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

    class DwnLoadDynLtgPrmForFrntRIGrp9LowBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp9LowBrightness"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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


class BgmToHcmlBodyExpoDiagReqFrame:
    msg_name = "BgmToHcmlBodyExpoDiagReqFrame"
    msg_id = 1971
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []


class CemBodyExpoFr88:
    msg_name = "CemBodyExpoFr88"
    msg_id = 822
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForFrntLeGrp22LowBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp22LowBrightness"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntLeGrp22Mode1:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp22Mode1"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
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

    class DwnLoadDynLtgPrmForFrntLeGrp22ContinueTime:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp22ContinueTime"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
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

    class DwnLoadDynLtgPrmForFrntLeGrp22Timestamp:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp22Timestamp"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DwnLoadDynLtgPrmForFrntLeGrp22OffsetTime:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp22OffsetTime"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
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

    class DwnLoadDynLtgPrmForFrntLeGrp22HighBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp22HighBrightness"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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


class RcmrToBgmBodyExpoDiagRespFrame:
    msg_name = "RcmrToBgmBodyExpoDiagRespFrame"
    msg_id = 1718
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']


class CemBodyExpoFr25:
    msg_name = "CemBodyExpoFr25"
    msg_id = 120
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.085
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class LvlgSwtSetReqADModCtrlInhbn:
        sig_name = "LvlgSwtSetReqADModCtrlInhbn"
        sig_start_bit = 54
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
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

    class OutdBriSts:
        sig_name = "OutdBriSts"
        sig_start_bit = 37
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class OutdBriChks:
        sig_name = "OutdBriChks"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class LvlgSwtSetReqCntr:
        sig_name = "LvlgSwtSetReqCntr"
        sig_start_bit = 51
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class OutdBriCntr:
        sig_name = "OutdBriCntr"
        sig_start_bit = 35
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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


class CemBodyExpoCommonFr11:
    msg_name = "CemBodyExpoCommonFr11"
    msg_id = 390
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.045
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class TrafficSignForADB2AdbDetdQly:
        sig_name = "TrafficSignForADB2AdbDetdQly"
        sig_start_bit = 11
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
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

    class TrafficSignForADB2AdbTrkInfo:
        sig_name = "TrafficSignForADB2AdbTrkInfo"
        sig_start_bit = 42
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class TrafficSignForADB2AdbVertAgTop:
        sig_name = "TrafficSignForADB2AdbVertAgTop"
        sig_start_bit = 41
        sig_length = 9
        sig_value_factor = 0.05
        sig_value_offset = "-3"
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 60
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 41
        bmuws_info = [(5, 0b00000011, 0b11111100, 2, 0), (6, 0b11111110, 0b00000001, 7, 1)]

    class TrafficSignForADB2AdbHozlAgLe:
        sig_name = "TrafficSignForADB2AdbHozlAgLe"
        sig_start_bit = 9
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = "-40"
        sig_value_min = 0
        sig_value_max = 1600
        sig_value_init = 800
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 9
        bmuws_info = [(1, 0b00000011, 0b11111100, 2, 0), (2, 0b11111111, 0b00000000, 8, 0), (3, 0b10000000, 0b01111111, 1, 7)]

    class TrafficSignForADB2AdbHozlAgRi:
        sig_name = "TrafficSignForADB2AdbHozlAgRi"
        sig_start_bit = 30
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = "-40"
        sig_value_min = 0
        sig_value_max = 1600
        sig_value_init = 800
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 30
        bmuws_info = [(3, 0b01111111, 0b10000000, 7, 0), (4, 0b11110000, 0b00001111, 4, 4)]

    class TrafficSignForADB2AdbVertAgBot:
        sig_name = "TrafficSignForADB2AdbVertAgBot"
        sig_start_bit = 35
        sig_length = 9
        sig_value_factor = 0.05
        sig_value_offset = "-3"
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 60
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 35
        bmuws_info = [(4, 0b00001111, 0b11110000, 4, 0), (5, 0b11111000, 0b00000111, 5, 3)]

    class TrafficSignForADB2AdbAbsDist:
        sig_name = "TrafficSignForADB2AdbAbsDist"
        sig_start_bit = 7
        sig_length = 12
        sig_value_factor = 0.2
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11110000, 0b00001111, 4, 4)]


class CemBodyExpoCommonFr20:
    msg_name = "CemBodyExpoCommonFr20"
    msg_id = 399
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.045
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class VehObjforADB8AdbObjHozlAgSpdLe:
        sig_name = "VehObjforADB8AdbObjHozlAgSpdLe"
        sig_start_bit = 34
        sig_length = 9
        sig_value_factor = 0.2
        sig_value_offset = "-50"
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 250
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 34
        bmuws_info = [(4, 0b00000111, 0b11111000, 3, 0), (5, 0b11111100, 0b00000011, 6, 2)]

    class VehObjforADB8AdbTrkInfo:
        sig_name = "VehObjforADB8AdbTrkInfo"
        sig_start_bit = 48
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class VehObjforADB8AdbAbsDist:
        sig_name = "VehObjforADB8AdbAbsDist"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class VehObjforADB8AdbObjDir:
        sig_name = "VehObjforADB8AdbObjDir"
        sig_start_bit = 36
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class VehObjforADB8AdbObjHozlAgSpdRi:
        sig_name = "VehObjforADB8AdbObjHozlAgSpdRi"
        sig_start_bit = 41
        sig_length = 9
        sig_value_factor = 0.2
        sig_value_offset = "-50"
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 250
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 41
        bmuws_info = [(5, 0b00000011, 0b11111100, 2, 0), (6, 0b11111110, 0b00000001, 7, 1)]

    class VehObjforADB8AdbClassn:
        sig_name = "VehObjforADB8AdbClassn"
        sig_start_bit = 13
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
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

    class VehObjforADB8AdbVertAg:
        sig_name = "VehObjforADB8AdbVertAg"
        sig_start_bit = 63
        sig_length = 5
        sig_value_factor = 0.5
        sig_value_offset = "-3"
        sig_value_min = 0
        sig_value_max = 31
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

    class VehObjforADB8AdbHozlAgRi:
        sig_name = "VehObjforADB8AdbHozlAgRi"
        sig_start_bit = 31
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = "-40"
        sig_value_min = 0
        sig_value_max = 1600
        sig_value_init = 800
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11100000, 0b00011111, 3, 5)]

    class VehObjforADB8AdbHozlAgLe:
        sig_name = "VehObjforADB8AdbHozlAgLe"
        sig_start_bit = 10
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = "-40"
        sig_value_min = 0
        sig_value_max = 1600
        sig_value_init = 800
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 10
        bmuws_info = [(1, 0b00000111, 0b11111000, 3, 0), (2, 0b11111111, 0b00000000, 8, 0)]


class CemBodyExpoFr76:
    msg_name = "CemBodyExpoFr76"
    msg_id = 810
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForFrntLeGrp10HighBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp10HighBrightness"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntLeGrp10LowBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp10LowBrightness"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntLeGrp10Mode1:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp10Mode1"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
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

    class DwnLoadDynLtgPrmForFrntLeGrp10ContinueTime:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp10ContinueTime"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
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

    class DwnLoadDynLtgPrmForFrntLeGrp10Timestamp:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp10Timestamp"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DwnLoadDynLtgPrmForFrntLeGrp10OffsetTime:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp10OffsetTime"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
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


class CemBodyExpoFr75:
    msg_name = "CemBodyExpoFr75"
    msg_id = 809
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForFrntLeGrp9Timestamp:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp9Timestamp"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DwnLoadDynLtgPrmForFrntLeGrp9LowBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp9LowBrightness"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntLeGrp9ContinueTime:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp9ContinueTime"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
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

    class DwnLoadDynLtgPrmForFrntLeGrp9Mode1:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp9Mode1"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
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

    class DwnLoadDynLtgPrmForFrntLeGrp9OffsetTime:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp9OffsetTime"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
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

    class DwnLoadDynLtgPrmForFrntLeGrp9HighBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp9HighBrightness"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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


class CemBodyExpoFr10:
    msg_name = "CemBodyExpoFr10"
    msg_id = 296
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLitPrmForLedStopLampLe1ModePrm:
        sig_name = "DwnLoadDynLitPrmForLedStopLampLe1ModePrm"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
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

    class DwnLoadDynLitPrmForLedStopLampLe1UpprBriPrm:
        sig_name = "DwnLoadDynLitPrmForLedStopLampLe1UpprBriPrm"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmForLedStopLampLe1LowBriPrm:
        sig_name = "DwnLoadDynLitPrmForLedStopLampLe1LowBriPrm"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmForLedStopLampLe1OffsTiPrm:
        sig_name = "DwnLoadDynLitPrmForLedStopLampLe1OffsTiPrm"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmForLedStopLampLe1Tistamp:
        sig_name = "DwnLoadDynLitPrmForLedStopLampLe1Tistamp"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmForLedStopLampLe1ContTiPrm:
        sig_name = "DwnLoadDynLitPrmForLedStopLampLe1ContTiPrm"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]


class CemBodyExpoFr26:
    msg_name = "CemBodyExpoFr26"
    msg_id = 311
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLitPrmForLedHiBeamLeTistamp:
        sig_name = "DwnLoadDynLitPrmForLedHiBeamLeTistamp"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmForLedHiBeamLeContTiPrm:
        sig_name = "DwnLoadDynLitPrmForLedHiBeamLeContTiPrm"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmForLedHiBeamLeUpprBriPrm:
        sig_name = "DwnLoadDynLitPrmForLedHiBeamLeUpprBriPrm"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmForLedHiBeamLeModePrm:
        sig_name = "DwnLoadDynLitPrmForLedHiBeamLeModePrm"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
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

    class DwnLoadDynLitPrmForLedHiBeamLeOffsTiPrm:
        sig_name = "DwnLoadDynLitPrmForLedHiBeamLeOffsTiPrm"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmForLedHiBeamLeLowBriPrm:
        sig_name = "DwnLoadDynLitPrmForLedHiBeamLeLowBriPrm"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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


class CemBodyExpoFr45:
    msg_name = "CemBodyExpoFr45"
    msg_id = 612
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.065
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class BrkPedlValQf:
        sig_name = "BrkPedlValQf"
        sig_start_bit = 41
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class WipgInfoWiprActv:
        sig_name = "WipgInfoWiprActv"
        sig_start_bit = 27
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class LitArea:
        sig_name = "LitArea"
        sig_start_bit = 10
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class WipgInfoWiprInWipgAr:
        sig_name = "WipgInfoWiprInWipgAr"
        sig_start_bit = 28
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class BrkPedlValBrkPedlVal:
        sig_name = "BrkPedlValBrkPedlVal"
        sig_start_bit = 54
        sig_length = 15
        sig_value_factor = 0.00390625
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 25600
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 54
        bmuws_info = [(6, 0b01111111, 0b10000000, 7, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class WipgInfoWipgSpdInfo:
        sig_name = "WipgInfoWipgSpdInfo"
        sig_start_bit = 26
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
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


class HcmmToBgmBodyExpoDiagRespFrame:
    msg_name = "HcmmToBgmBodyExpoDiagRespFrame"
    msg_id = 1714
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']


class HcmlBodyExpoFr04:
    msg_name = "HcmlBodyExpoFr04"
    msg_id = 124
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class StsOfLedFrntTurnIndcrLe:
        sig_name = "StsOfLedFrntTurnIndcrLe"
        sig_start_bit = 19
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class DwnLoadStsFbOfHdlampLe:
        sig_name = "DwnLoadStsFbOfHdlampLe"
        sig_start_bit = 5
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class StsOfLvlgLeCntr:
        sig_name = "StsOfLvlgLeCntr"
        sig_start_bit = 55
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class StsOfLedCornrgLampLe:
        sig_name = "StsOfLedCornrgLampLe"
        sig_start_bit = 11
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class StsOfTouristModLe:
        sig_name = "StsOfTouristModLe"
        sig_start_bit = 25
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class StsOfAhbcLe:
        sig_name = "StsOfAhbcLe"
        sig_start_bit = 3
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class HdlampLeInpSts1:
        sig_name = "HdlampLeInpSts1"
        sig_start_bit = 49
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class HdlampLeInpSts2:
        sig_name = "HdlampLeInpSts2"
        sig_start_bit = 63
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class StsOfLedFrntPosnLampLe:
        sig_name = "StsOfLedFrntPosnLampLe"
        sig_start_bit = 17
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class StsOfSwvlgLe:
        sig_name = "StsOfSwvlgLe"
        sig_start_bit = 7
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class StsOfLedDaytiRunngLampLe:
        sig_name = "StsOfLedDaytiRunngLampLe"
        sig_start_bit = 13
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class ExtrLiShowActvnFrntLeFb:
        sig_name = "ExtrLiShowActvnFrntLeFb"
        sig_start_bit = 28
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class StsOfFrntSideMkrLampLe2:
        sig_name = "StsOfFrntSideMkrLampLe2"
        sig_start_bit = 9
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class StsOfLvlgLeChks:
        sig_name = "StsOfLvlgLeChks"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class StsOfWelGbyFrntLe:
        sig_name = "StsOfWelGbyFrntLe"
        sig_start_bit = 61
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class StsOfAfsLe:
        sig_name = "StsOfAfsLe"
        sig_start_bit = 1
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class StsOfLvlgLeStsOfLvlgLe:
        sig_name = "StsOfLvlgLeStsOfLvlgLe"
        sig_start_bit = 51
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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


class CemBodyExpoFr58:
    msg_name = "CemBodyExpoFr58"
    msg_id = 332
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLitPrmLedRePosnLampRi5LowBriPrm:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi5LowBriPrm"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmLedRePosnLampRi5OffsTiPrm:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi5OffsTiPrm"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedRePosnLampRi5ModePrm:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi5ModePrm"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
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

    class DwnLoadDynLitPrmLedRePosnLampRi5UpprBriPrm:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi5UpprBriPrm"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmLedRePosnLampRi5Tistamp:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi5Tistamp"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmLedRePosnLampRi5ContTiPrm:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi5ContTiPrm"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]


class CemBodyExpoFr60:
    msg_name = "CemBodyExpoFr60"
    msg_id = 333
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLitPrmLedLeGrilleLampUpprBriPrm:
        sig_name = "DwnLoadDynLitPrmLedLeGrilleLampUpprBriPrm"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmLedLeGrilleLampTistamp:
        sig_name = "DwnLoadDynLitPrmLedLeGrilleLampTistamp"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmLedLeGrilleLampOffsTiPrm:
        sig_name = "DwnLoadDynLitPrmLedLeGrilleLampOffsTiPrm"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedLeGrilleLampModePrm:
        sig_name = "DwnLoadDynLitPrmLedLeGrilleLampModePrm"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
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

    class DwnLoadDynLitPrmLedLeGrilleLampLowBriPrm:
        sig_name = "DwnLoadDynLitPrmLedLeGrilleLampLowBriPrm"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmLedLeGrilleLampContTiPrm:
        sig_name = "DwnLoadDynLitPrmLedLeGrilleLampContTiPrm"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]


class CemBodyExpoFr18:
    msg_name = "CemBodyExpoFr18"
    msg_id = 304
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLitPrmLedRePosnLampRi1LowBriPrm:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi1LowBriPrm"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmLedRePosnLampRi1Tistamp:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi1Tistamp"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmLedRePosnLampRi1OffsTiPrm:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi1OffsTiPrm"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedRePosnLampRi1ModePrm:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi1ModePrm"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
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

    class DwnLoadDynLitPrmLedRePosnLampRi1UpprBriPrm:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi1UpprBriPrm"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmLedRePosnLampRi1ContTiPrm:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi1ContTiPrm"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]


class CemBodyExpoCommonFr14:
    msg_name = "CemBodyExpoCommonFr14"
    msg_id = 393
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.045
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class VehObjforADB2AdbHozlAgLe:
        sig_name = "VehObjforADB2AdbHozlAgLe"
        sig_start_bit = 10
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = "-40"
        sig_value_min = 0
        sig_value_max = 1600
        sig_value_init = 800
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 10
        bmuws_info = [(1, 0b00000111, 0b11111000, 3, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class VehObjforADB2AdbObjHozlAgSpdRi:
        sig_name = "VehObjforADB2AdbObjHozlAgSpdRi"
        sig_start_bit = 41
        sig_length = 9
        sig_value_factor = 0.2
        sig_value_offset = "-50"
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 250
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 41
        bmuws_info = [(5, 0b00000011, 0b11111100, 2, 0), (6, 0b11111110, 0b00000001, 7, 1)]

    class VehObjforADB2AdbObjDir:
        sig_name = "VehObjforADB2AdbObjDir"
        sig_start_bit = 36
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class VehObjforADB2AdbHozlAgRi:
        sig_name = "VehObjforADB2AdbHozlAgRi"
        sig_start_bit = 31
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = "-40"
        sig_value_min = 0
        sig_value_max = 1600
        sig_value_init = 800
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11100000, 0b00011111, 3, 5)]

    class VehObjforADB2AdbTrkInfo:
        sig_name = "VehObjforADB2AdbTrkInfo"
        sig_start_bit = 48
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class VehObjforADB2AdbClassn:
        sig_name = "VehObjforADB2AdbClassn"
        sig_start_bit = 13
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
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

    class VehObjforADB2AdbObjHozlAgSpdLe:
        sig_name = "VehObjforADB2AdbObjHozlAgSpdLe"
        sig_start_bit = 34
        sig_length = 9
        sig_value_factor = 0.2
        sig_value_offset = "-50"
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 250
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 34
        bmuws_info = [(4, 0b00000111, 0b11111000, 3, 0), (5, 0b11111100, 0b00000011, 6, 2)]

    class VehObjforADB2AdbVertAg:
        sig_name = "VehObjforADB2AdbVertAg"
        sig_start_bit = 63
        sig_length = 5
        sig_value_factor = 0.5
        sig_value_offset = "-3"
        sig_value_min = 0
        sig_value_max = 31
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

    class VehObjforADB2AdbAbsDist:
        sig_name = "VehObjforADB2AdbAbsDist"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]


class CemBodyExpoCommonFr01:
    msg_name = "CemBodyExpoCommonFr01"
    msg_id = 82
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class SteerWhlSnsrChks:
        sig_name = "SteerWhlSnsrChks"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class LiOprnMod:
        sig_name = "LiOprnMod"
        sig_start_bit = 43
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class SteerWhlSnsrCntr:
        sig_name = "SteerWhlSnsrCntr"
        sig_start_bit = 47
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class SteerWhlSnsrAgSpd:
        sig_name = "SteerWhlSnsrAgSpd"
        sig_start_bit = 21
        sig_length = 14
        sig_value_factor = 0.0078125
        sig_value_offset = 0.0
        sig_value_min = -6400
        sig_value_max = 6400
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 14
        startbit = 21
        bmuws_info = [(2, 0b00111111, 0b11000000, 6, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class SteerWhlSnsrQf:
        sig_name = "SteerWhlSnsrQf"
        sig_start_bit = 23
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class AutWinWipgCmd:
        sig_name = "AutWinWipgCmd"
        sig_start_bit = 55
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
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

    class SteerWhlSnsrAg:
        sig_name = "SteerWhlSnsrAg"
        sig_start_bit = 6
        sig_length = 15
        sig_value_factor = "9.765625E-4"
        sig_value_offset = 0.0
        sig_value_min = -14848
        sig_value_max = 14848
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 6
        bmuws_info = [(0, 0b01111111, 0b10000000, 7, 0), (1, 0b11111111, 0b00000000, 8, 0)]


class HcmlToBgmBodyExpoDiagRespFrame:
    msg_name = "HcmlToBgmBodyExpoDiagRespFrame"
    msg_id = 1715
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']


class CemBodyExpoFr06:
    msg_name = "CemBodyExpoFr06"
    msg_id = 292
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLitPrmForLedMkrLampLe1UpprBriPrm:
        sig_name = "DwnLoadDynLitPrmForLedMkrLampLe1UpprBriPrm"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmForLedMkrLampLe1Tistamp:
        sig_name = "DwnLoadDynLitPrmForLedMkrLampLe1Tistamp"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmForLedMkrLampLe1OffsTiPrm:
        sig_name = "DwnLoadDynLitPrmForLedMkrLampLe1OffsTiPrm"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmForLedMkrLampLe1ModePrm:
        sig_name = "DwnLoadDynLitPrmForLedMkrLampLe1ModePrm"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
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

    class DwnLoadDynLitPrmForLedMkrLampLe1LowBriPrm:
        sig_name = "DwnLoadDynLitPrmForLedMkrLampLe1LowBriPrm"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmForLedMkrLampLe1ContTiPrm:
        sig_name = "DwnLoadDynLitPrmForLedMkrLampLe1ContTiPrm"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]


class CemBodyExpoCommonFr04:
    msg_name = "CemBodyExpoCommonFr04"
    msg_id = 80
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.04
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class VehSpdLgtChks:
        sig_name = "VehSpdLgtChks"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class VehSpdLgtCntr:
        sig_name = "VehSpdLgtCntr"
        sig_start_bit = 31
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class VehSpdLgtQf:
        sig_name = "VehSpdLgtQf"
        sig_start_bit = 27
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class VehSpdLgtA:
        sig_name = "VehSpdLgtA"
        sig_start_bit = 6
        sig_length = 15
        sig_value_factor = 0.00391
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 31970
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 6
        bmuws_info = [(0, 0b01111111, 0b10000000, 7, 0), (1, 0b11111111, 0b00000000, 8, 0)]


class CemBodyExpoFr35:
    msg_name = "CemBodyExpoFr35"
    msg_id = 320
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForLedFrntPosnLampRiUpprBriPrm:
        sig_name = "DwnLoadDynLtgPrmForLedFrntPosnLampRiUpprBriPrm"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLtgPrmForLedFrntPosnLampRiOffsTiPrm:
        sig_name = "DwnLoadDynLtgPrmForLedFrntPosnLampRiOffsTiPrm"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLtgPrmForLedFrntPosnLampRiTistamp:
        sig_name = "DwnLoadDynLtgPrmForLedFrntPosnLampRiTistamp"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLtgPrmForLedFrntPosnLampRiContTiPrm:
        sig_name = "DwnLoadDynLtgPrmForLedFrntPosnLampRiContTiPrm"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLtgPrmForLedFrntPosnLampRiLowBriPrm:
        sig_name = "DwnLoadDynLtgPrmForLedFrntPosnLampRiLowBriPrm"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLtgPrmForLedFrntPosnLampRiModePrm:
        sig_name = "DwnLoadDynLtgPrmForLedFrntPosnLampRiModePrm"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
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


class CemBodyExpoFr106:
    msg_name = "CemBodyExpoFr106"
    msg_id = 840
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForFrntRIGrp16Mode1:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp16Mode1"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
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

    class DwnLoadDynLtgPrmForFrntRIGrp16HighBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp16HighBrightness"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntRIGrp16LowBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp16LowBrightness"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntRIGrp16ContinueTime:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp16ContinueTime"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
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

    class DwnLoadDynLtgPrmForFrntRIGrp16Timestamp:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp16Timestamp"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DwnLoadDynLtgPrmForFrntRIGrp16OffsetTime:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp16OffsetTime"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
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


class CemBodyExpoFr90:
    msg_name = "CemBodyExpoFr90"
    msg_id = 824
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForFrntLeGrp24OffsetTime:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp24OffsetTime"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
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

    class DwnLoadDynLtgPrmForFrntLeGrp24HighBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp24HighBrightness"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntLeGrp24Mode1:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp24Mode1"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
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

    class DwnLoadDynLtgPrmForFrntLeGrp24Timestamp:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp24Timestamp"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DwnLoadDynLtgPrmForFrntLeGrp24LowBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp24LowBrightness"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntLeGrp24ContinueTime:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp24ContinueTime"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
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


class CemBodyExpoFr61:
    msg_name = "CemBodyExpoFr61"
    msg_id = 334
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLitPrmLedRiGrilleLampTistamp:
        sig_name = "DwnLoadDynLitPrmLedRiGrilleLampTistamp"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmLedRiGrilleLampOffsTiPrm:
        sig_name = "DwnLoadDynLitPrmLedRiGrilleLampOffsTiPrm"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedRiGrilleLampLowBriPrm:
        sig_name = "DwnLoadDynLitPrmLedRiGrilleLampLowBriPrm"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmLedRiGrilleLampModePrm:
        sig_name = "DwnLoadDynLitPrmLedRiGrilleLampModePrm"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
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

    class DwnLoadDynLitPrmLedRiGrilleLampContTiPrm:
        sig_name = "DwnLoadDynLitPrmLedRiGrilleLampContTiPrm"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedRiGrilleLampUpprBriPrm:
        sig_name = "DwnLoadDynLitPrmLedRiGrilleLampUpprBriPrm"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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


class CemBodyExpoFr15:
    msg_name = "CemBodyExpoFr15"
    msg_id = 301
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLitPrmLedReFogLampRi1ModePrm:
        sig_name = "DwnLoadDynLitPrmLedReFogLampRi1ModePrm"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
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

    class DwnLoadDynLitPrmLedReFogLampRi1OffsTiPrm:
        sig_name = "DwnLoadDynLitPrmLedReFogLampRi1OffsTiPrm"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedReFogLampRi1UpprBriPrm:
        sig_name = "DwnLoadDynLitPrmLedReFogLampRi1UpprBriPrm"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmLedReFogLampRi1ContTiPrm:
        sig_name = "DwnLoadDynLitPrmLedReFogLampRi1ContTiPrm"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedReFogLampRi1LowBriPrm:
        sig_name = "DwnLoadDynLitPrmLedReFogLampRi1LowBriPrm"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmLedReFogLampRi1Tistamp:
        sig_name = "DwnLoadDynLitPrmLedReFogLampRi1Tistamp"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]


class CemBodyExpoFr52:
    msg_name = "CemBodyExpoFr52"
    msg_id = 326
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLitPrmForLedLogoLampLowBriPrm:
        sig_name = "DwnLoadDynLitPrmForLedLogoLampLowBriPrm"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmForLedLogoLampUpprBriPrm:
        sig_name = "DwnLoadDynLitPrmForLedLogoLampUpprBriPrm"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmForLedLogoLampModePrm:
        sig_name = "DwnLoadDynLitPrmForLedLogoLampModePrm"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
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

    class DwnLoadDynLitPrmForLedLogoLampOffsTiPrm:
        sig_name = "DwnLoadDynLitPrmForLedLogoLampOffsTiPrm"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmForLedLogoLampTistamp:
        sig_name = "DwnLoadDynLitPrmForLedLogoLampTistamp"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmForLedLogoLampContTiPrm:
        sig_name = "DwnLoadDynLitPrmForLedLogoLampContTiPrm"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]


class CemBodyExpoFr50:
    msg_name = "CemBodyExpoFr50"
    msg_id = 522
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class ActnOfLedStopLampCntr:
        sig_name = "ActnOfLedStopLampCntr"
        sig_start_bit = 19
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class ActnOfLedLoBeamActnOfLedLoBeam:
        sig_name = "ActnOfLedLoBeamActnOfLedLoBeam"
        sig_start_bit = 4
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class ActnOfLedRvsgLamp:
        sig_name = "ActnOfLedRvsgLamp"
        sig_start_bit = 42
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class ActvnOfAhbc:
        sig_name = "ActvnOfAhbc"
        sig_start_bit = 46
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class ActnOfLedHiBeam:
        sig_name = "ActnOfLedHiBeam"
        sig_start_bit = 36
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class ActvnOfAfs:
        sig_name = "ActvnOfAfs"
        sig_start_bit = 44
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class ActvnOfWelcomeLi:
        sig_name = "ActvnOfWelcomeLi"
        sig_start_bit = 58
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class ActnOfLedDaytiRunngLamp:
        sig_name = "ActnOfLedDaytiRunngLamp"
        sig_start_bit = 32
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class ActvnOfDbl:
        sig_name = "ActvnOfDbl"
        sig_start_bit = 52
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class ActnOfLedFrntFogLamp:
        sig_name = "ActnOfLedFrntFogLamp"
        sig_start_bit = 34
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class ActnOfLedPosnLamp:
        sig_name = "ActnOfLedPosnLamp"
        sig_start_bit = 38
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class ActvnOfGoodByeLi:
        sig_name = "ActvnOfGoodByeLi"
        sig_start_bit = 54
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class ActnOfLedReFogLamp:
        sig_name = "ActnOfLedReFogLamp"
        sig_start_bit = 40
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class ActnOfLedLoBeamChks:
        sig_name = "ActnOfLedLoBeamChks"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class ActnOfLedCornrgLampRi:
        sig_name = "ActnOfLedCornrgLampRi"
        sig_start_bit = 22
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class ActvnOfBrkLi:
        sig_name = "ActvnOfBrkLi"
        sig_start_bit = 50
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class ActnOfLedStopLampChks:
        sig_name = "ActnOfLedStopLampChks"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class ActvnOfAhl:
        sig_name = "ActvnOfAhl"
        sig_start_bit = 48
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class ActnOfLedCornrgLampLe:
        sig_name = "ActnOfLedCornrgLampLe"
        sig_start_bit = 6
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class ActvnOfTouristMod:
        sig_name = "ActvnOfTouristMod"
        sig_start_bit = 56
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class ActnOfLedStopLampActnOfLedStopLamp:
        sig_name = "ActnOfLedStopLampActnOfLedStopLamp"
        sig_start_bit = 20
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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


class CemBodyExpoFr04:
    msg_name = "CemBodyExpoFr04"
    msg_id = 290
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLitPrmLedRePosnLampRi2ContTiPrm:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi2ContTiPrm"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedRePosnLampRi2Tistamp:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi2Tistamp"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmLedRePosnLampRi2OffsTiPrm:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi2OffsTiPrm"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedRePosnLampRi2LowBriPrm:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi2LowBriPrm"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmLedRePosnLampRi2UpprBriPrm:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi2UpprBriPrm"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmLedRePosnLampRi2ModePrm:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampRi2ModePrm"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
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


class CemBodyExpoFr37:
    msg_name = "CemBodyExpoFr37"
    msg_id = 322
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForLedFrntTurnIndcrRiLowBriPrm:
        sig_name = "DwnLoadDynLtgPrmForLedFrntTurnIndcrRiLowBriPrm"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLtgPrmForLedFrntTurnIndcrRiModePrm:
        sig_name = "DwnLoadDynLtgPrmForLedFrntTurnIndcrRiModePrm"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
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

    class DwnLoadDynLtgPrmForLedFrntTurnIndcrRiUpprBriPrm:
        sig_name = "DwnLoadDynLtgPrmForLedFrntTurnIndcrRiUpprBriPrm"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLtgPrmForLedFrntTurnIndcrRiOffsTiPrm:
        sig_name = "DwnLoadDynLtgPrmForLedFrntTurnIndcrRiOffsTiPrm"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLtgPrmForLedFrntTurnIndcrRiContTiPrm:
        sig_name = "DwnLoadDynLtgPrmForLedFrntTurnIndcrRiContTiPrm"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLtgPrmForLedFrntTurnIndcrRiTistamp:
        sig_name = "DwnLoadDynLtgPrmForLedFrntTurnIndcrRiTistamp"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]


class CemBodyExpoFr16:
    msg_name = "CemBodyExpoFr16"
    msg_id = 302
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLitPrmLedRePosnLampLe1UpprBriPrm:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe1UpprBriPrm"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmLedRePosnLampLe1ContTiPrm:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe1ContTiPrm"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedRePosnLampLe1LowBriPrm:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe1LowBriPrm"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmLedRePosnLampLe1Tistamp:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe1Tistamp"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmLedRePosnLampLe1ModePrm:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe1ModePrm"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
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

    class DwnLoadDynLitPrmLedRePosnLampLe1OffsTiPrm:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe1OffsTiPrm"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]


class CemBodyExpoFr101:
    msg_name = "CemBodyExpoFr101"
    msg_id = 835
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForFrntRIGrp11HighBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp11HighBrightness"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntRIGrp11OffsetTime:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp11OffsetTime"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
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

    class DwnLoadDynLtgPrmForFrntRIGrp11ContinueTime:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp11ContinueTime"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
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

    class DwnLoadDynLtgPrmForFrntRIGrp11LowBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp11LowBrightness"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntRIGrp11Mode1:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp11Mode1"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
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

    class DwnLoadDynLtgPrmForFrntRIGrp11Timestamp:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp11Timestamp"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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


class RcmrBodyExpoFr01:
    msg_name = "RcmrBodyExpoFr01"
    msg_id = 608
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class ExtrLiShowStoreStsReRi1:
        sig_name = "ExtrLiShowStoreStsReRi1"
        sig_start_bit = 1
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class StsOfLedStopLampRi1:
        sig_name = "StsOfLedStopLampRi1"
        sig_start_bit = 23
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class DwnLoadStsFbOfReLampCtrlRi1:
        sig_name = "DwnLoadStsFbOfReLampCtrlRi1"
        sig_start_bit = 17
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class StsOfWelGbyReRi1:
        sig_name = "StsOfWelGbyReRi1"
        sig_start_bit = 39
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class StsOfLedPosnLampRi1:
        sig_name = "StsOfLedPosnLampRi1"
        sig_start_bit = 9
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class StsOfLedTurnIndcrRi1:
        sig_name = "StsOfLedTurnIndcrRi1"
        sig_start_bit = 25
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class StsOfLedReFogLampRi1:
        sig_name = "StsOfLedReFogLampRi1"
        sig_start_bit = 11
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class StsOfLedReLampRi1:
        sig_name = "StsOfLedReLampRi1"
        sig_start_bit = 13
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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


class CemBodyExpoFr03:
    msg_name = "CemBodyExpoFr03"
    msg_id = 289
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLitPrmLedReFogLampRi2UpprBriPrm:
        sig_name = "DwnLoadDynLitPrmLedReFogLampRi2UpprBriPrm"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmLedReFogLampRi2ContTiPrm:
        sig_name = "DwnLoadDynLitPrmLedReFogLampRi2ContTiPrm"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedReFogLampRi2Tistamp:
        sig_name = "DwnLoadDynLitPrmLedReFogLampRi2Tistamp"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmLedReFogLampRi2LowBriPrm:
        sig_name = "DwnLoadDynLitPrmLedReFogLampRi2LowBriPrm"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmLedReFogLampRi2ModePrm:
        sig_name = "DwnLoadDynLitPrmLedReFogLampRi2ModePrm"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
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

    class DwnLoadDynLitPrmLedReFogLampRi2OffsTiPrm:
        sig_name = "DwnLoadDynLitPrmLedReFogLampRi2OffsTiPrm"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]


class CemBodyExpoFr84:
    msg_name = "CemBodyExpoFr84"
    msg_id = 818
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForFrntLeGrp18HighBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp18HighBrightness"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntLeGrp18ContinueTime:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp18ContinueTime"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
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

    class DwnLoadDynLtgPrmForFrntLeGrp18Mode1:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp18Mode1"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
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

    class DwnLoadDynLtgPrmForFrntLeGrp18Timestamp:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp18Timestamp"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DwnLoadDynLtgPrmForFrntLeGrp18OffsetTime:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp18OffsetTime"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
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

    class DwnLoadDynLtgPrmForFrntLeGrp18LowBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp18LowBrightness"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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


class CemBodyExpoFr23:
    msg_name = "CemBodyExpoFr23"
    msg_id = 309
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLitPrmLedRvsgLampLe2ModePrm:
        sig_name = "DwnLoadDynLitPrmLedRvsgLampLe2ModePrm"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
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

    class DwnLoadDynLitPrmLedRvsgLampLe2UpprBriPrm:
        sig_name = "DwnLoadDynLitPrmLedRvsgLampLe2UpprBriPrm"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmLedRvsgLampLe2OffsTiPrm:
        sig_name = "DwnLoadDynLitPrmLedRvsgLampLe2OffsTiPrm"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedRvsgLampLe2Tistamp:
        sig_name = "DwnLoadDynLitPrmLedRvsgLampLe2Tistamp"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmLedRvsgLampLe2LowBriPrm:
        sig_name = "DwnLoadDynLitPrmLedRvsgLampLe2LowBriPrm"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmLedRvsgLampLe2ContTiPrm:
        sig_name = "DwnLoadDynLitPrmLedRvsgLampLe2ContTiPrm"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]


class HcmrToBgmBodyExpoDiagRespFrame:
    msg_name = "HcmrToBgmBodyExpoDiagRespFrame"
    msg_id = 1716
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']


class CemBodyExpoFr62:
    msg_name = "CemBodyExpoFr62"
    msg_id = 788
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.94
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DHUcontrolLedMkrLampLe1:
        sig_name = "DHUcontrolLedMkrLampLe1"
        sig_start_bit = 7
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
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

    class DHUcontrolLedMkrLampRi1:
        sig_name = "DHUcontrolLedMkrLampRi1"
        sig_start_bit = 3
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
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

    class DHUcontrolLedStopLampRi1:
        sig_name = "DHUcontrolLedStopLampRi1"
        sig_start_bit = 11
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
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

    class DHUcontrolLedMkrLampRi2:
        sig_name = "DHUcontrolLedMkrLampRi2"
        sig_start_bit = 1
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
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

    class DHUcontrolLedStopLampLe1:
        sig_name = "DHUcontrolLedStopLampLe1"
        sig_start_bit = 15
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
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

    class DHUcontrolLedStopLampLe2:
        sig_name = "DHUcontrolLedStopLampLe2"
        sig_start_bit = 13
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
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

    class DHUcontrolmiddlebrakelight:
        sig_name = "DHUcontrolmiddlebrakelight"
        sig_start_bit = 23
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
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

    class DHUcontrolmiddlepositionlight:
        sig_name = "DHUcontrolmiddlepositionlight"
        sig_start_bit = 19
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
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

    class DHUcontrolLedMkrLampLe2:
        sig_name = "DHUcontrolLedMkrLampLe2"
        sig_start_bit = 5
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
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

    class DHUcontrolmiddlecorneringlamp:
        sig_name = "DHUcontrolmiddlecorneringlamp"
        sig_start_bit = 21
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
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


class CemBodyExpoFr114:
    msg_name = "CemBodyExpoFr114"
    msg_id = 848
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForFrntRIGrp24ContinueTime:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp24ContinueTime"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
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

    class DwnLoadDynLtgPrmForFrntRIGrp24Mode1:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp24Mode1"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
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

    class DwnLoadDynLtgPrmForFrntRIGrp24OffsetTime:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp24OffsetTime"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
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

    class DwnLoadDynLtgPrmForFrntRIGrp24LowBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp24LowBrightness"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntRIGrp24HighBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp24HighBrightness"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntRIGrp24Timestamp:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp24Timestamp"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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


class CemBodyExpoCommonFr05:
    msg_name = "CemBodyExpoCommonFr05"
    msg_id = 384
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class VehCfgPrmCCPBytePosn3:
        sig_name = "VehCfgPrmCCPBytePosn3"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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

    class VehCfgPrmCCPBytePosn6:
        sig_name = "VehCfgPrmCCPBytePosn6"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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

    class VehCfgPrmCCPBytePosn5:
        sig_name = "VehCfgPrmCCPBytePosn5"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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

    class VehCfgPrmCCPBytePosn7:
        sig_name = "VehCfgPrmCCPBytePosn7"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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

    class VehCfgPrmBlkIDBytePosn1:
        sig_name = "VehCfgPrmBlkIDBytePosn1"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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

    class VehCfgPrmCCPBytePosn4:
        sig_name = "VehCfgPrmCCPBytePosn4"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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

    class VehCfgPrmCCPBytePosn8:
        sig_name = "VehCfgPrmCCPBytePosn8"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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

    class VehCfgPrmCCPBytePosn2:
        sig_name = "VehCfgPrmCCPBytePosn2"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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


class CemBodyExpoFr08:
    msg_name = "CemBodyExpoFr08"
    msg_id = 294
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLitPrmForLedMkrLampLe2ContTiPrm:
        sig_name = "DwnLoadDynLitPrmForLedMkrLampLe2ContTiPrm"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmForLedMkrLampLe2LowBriPrm:
        sig_name = "DwnLoadDynLitPrmForLedMkrLampLe2LowBriPrm"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmForLedMkrLampLe2UpprBriPrm:
        sig_name = "DwnLoadDynLitPrmForLedMkrLampLe2UpprBriPrm"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmForLedMkrLampLe2ModePrm:
        sig_name = "DwnLoadDynLitPrmForLedMkrLampLe2ModePrm"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
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

    class DwnLoadDynLitPrmForLedMkrLampLe2Tistamp:
        sig_name = "DwnLoadDynLitPrmForLedMkrLampLe2Tistamp"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmForLedMkrLampLe2OffsTiPrm:
        sig_name = "DwnLoadDynLitPrmForLedMkrLampLe2OffsTiPrm"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]


class CemBodyExpoFr100:
    msg_name = "CemBodyExpoFr100"
    msg_id = 834
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForFrntRIGrp10Timestamp:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp10Timestamp"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DwnLoadDynLtgPrmForFrntRIGrp10LowBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp10LowBrightness"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntRIGrp10Mode1:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp10Mode1"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
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

    class DwnLoadDynLtgPrmForFrntRIGrp10OffsetTime:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp10OffsetTime"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
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

    class DwnLoadDynLtgPrmForFrntRIGrp10ContinueTime:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp10ContinueTime"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
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

    class DwnLoadDynLtgPrmForFrntRIGrp10HighBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp10HighBrightness"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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


class BgmToRcmlBodyExpoDiagReqFrame:
    msg_name = "BgmToRcmlBodyExpoDiagReqFrame"
    msg_id = 1973
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []


class CemBodyExpoFr32:
    msg_name = "CemBodyExpoFr32"
    msg_id = 317
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForLedDaytiRunngLampLeModePrm:
        sig_name = "DwnLoadDynLtgPrmForLedDaytiRunngLampLeModePrm"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
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

    class DwnLoadDynLtgPrmForLedDaytiRunngLampLeOffsTiPrm:
        sig_name = "DwnLoadDynLtgPrmForLedDaytiRunngLampLeOffsTiPrm"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLtgPrmForLedDaytiRunngLampLeTistamp:
        sig_name = "DwnLoadDynLtgPrmForLedDaytiRunngLampLeTistamp"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLtgPrmForLedDaytiRunngLampLeLowBriPrm:
        sig_name = "DwnLoadDynLtgPrmForLedDaytiRunngLampLeLowBriPrm"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLtgPrmForLedDaytiRunngLampLeContTiPrm:
        sig_name = "DwnLoadDynLtgPrmForLedDaytiRunngLampLeContTiPrm"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLtgPrmForLedDaytiRunngLampLeUpprBriPrm:
        sig_name = "DwnLoadDynLtgPrmForLedDaytiRunngLampLeUpprBriPrm"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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


class CemBodyExpoFr12:
    msg_name = "CemBodyExpoFr12"
    msg_id = 298
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLitPrmForLedStopLampRi1Tistamp:
        sig_name = "DwnLoadDynLitPrmForLedStopLampRi1Tistamp"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmForLedStopLampRi1ModePrm:
        sig_name = "DwnLoadDynLitPrmForLedStopLampRi1ModePrm"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
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

    class DwnLoadDynLitPrmForLedStopLampRi1OffsTiPrm:
        sig_name = "DwnLoadDynLitPrmForLedStopLampRi1OffsTiPrm"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmForLedStopLampRi1ContTiPrm:
        sig_name = "DwnLoadDynLitPrmForLedStopLampRi1ContTiPrm"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmForLedStopLampRi1LowBriPrm:
        sig_name = "DwnLoadDynLitPrmForLedStopLampRi1LowBriPrm"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmForLedStopLampRi1UpprBriPrm:
        sig_name = "DwnLoadDynLitPrmForLedStopLampRi1UpprBriPrm"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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


class CemBodyExpoFr85:
    msg_name = "CemBodyExpoFr85"
    msg_id = 819
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForFrntLeGrp19OffsetTime:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp19OffsetTime"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
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

    class DwnLoadDynLtgPrmForFrntLeGrp19HighBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp19HighBrightness"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntLeGrp19LowBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp19LowBrightness"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntLeGrp19Timestamp:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp19Timestamp"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DwnLoadDynLtgPrmForFrntLeGrp19ContinueTime:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp19ContinueTime"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
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

    class DwnLoadDynLtgPrmForFrntLeGrp19Mode1:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp19Mode1"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
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


class HcmrBodyExposedCANNmFr:
    msg_name = "HcmrBodyExposedCANNmFr"
    msg_id = 1330
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']


class CemBodyExpoFr93:
    msg_name = "CemBodyExpoFr93"
    msg_id = 827
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForFrntRIGrp3LowBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp3LowBrightness"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntRIGrp3Mode1:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp3Mode1"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
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

    class DwnLoadDynLtgPrmForFrntRIGrp3Timestamp:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp3Timestamp"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DwnLoadDynLtgPrmForFrntRIGrp3HighBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp3HighBrightness"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntRIGrp3ContinueTime:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp3ContinueTime"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
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

    class DwnLoadDynLtgPrmForFrntRIGrp3OffsetTime:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp3OffsetTime"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
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


class RcmlToBgmBodyExpoDiagRespFrame:
    msg_name = "RcmlToBgmBodyExpoDiagRespFrame"
    msg_id = 1717
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']


class CemBodyExpoFr36:
    msg_name = "CemBodyExpoFr36"
    msg_id = 321
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForLedFrntTurnIndcrLeContTiPrm:
        sig_name = "DwnLoadDynLtgPrmForLedFrntTurnIndcrLeContTiPrm"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLtgPrmForLedFrntTurnIndcrLeLowBriPrm:
        sig_name = "DwnLoadDynLtgPrmForLedFrntTurnIndcrLeLowBriPrm"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLtgPrmForLedFrntTurnIndcrLeUpprBriPrm:
        sig_name = "DwnLoadDynLtgPrmForLedFrntTurnIndcrLeUpprBriPrm"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLtgPrmForLedFrntTurnIndcrLeOffsTiPrm:
        sig_name = "DwnLoadDynLtgPrmForLedFrntTurnIndcrLeOffsTiPrm"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLtgPrmForLedFrntTurnIndcrLeModePrm:
        sig_name = "DwnLoadDynLtgPrmForLedFrntTurnIndcrLeModePrm"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
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

    class DwnLoadDynLtgPrmForLedFrntTurnIndcrLeTistamp:
        sig_name = "DwnLoadDynLtgPrmForLedFrntTurnIndcrLeTistamp"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]


class CemBodyExpoFr87:
    msg_name = "CemBodyExpoFr87"
    msg_id = 821
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForFrntLeGrp21Mode1:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp21Mode1"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
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

    class DwnLoadDynLtgPrmForFrntLeGrp21Timestamp:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp21Timestamp"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DwnLoadDynLtgPrmForFrntLeGrp21LowBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp21LowBrightness"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntLeGrp21HighBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp21HighBrightness"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntLeGrp21ContinueTime:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp21ContinueTime"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
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

    class DwnLoadDynLtgPrmForFrntLeGrp21OffsetTime:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp21OffsetTime"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
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


class HcmlBodyExpoFr02:
    msg_name = "HcmlBodyExpoFr02"
    msg_id = 593
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 3
    tx_node = None
    rx_nodes = ['BGM']

    class StsOfLedHiBeamLe:
        sig_name = "StsOfLedHiBeamLe"
        sig_start_bit = 1
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class ExtrLiShowStoreStsFrntLe:
        sig_name = "ExtrLiShowStoreStsFrntLe"
        sig_start_bit = 7
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class StsOfLedLoBeamLe:
        sig_name = "StsOfLedLoBeamLe"
        sig_start_bit = 4
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class StsOfLedReFogLampLe2:
        sig_name = "StsOfLedReFogLampLe2"
        sig_start_bit = 13
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class StsOfWelGbyReRi2:
        sig_name = "StsOfWelGbyReRi2"
        sig_start_bit = 53
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class StsOfLedPosnLampLe2:
        sig_name = "StsOfLedPosnLampLe2"
        sig_start_bit = 9
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class ExtrLiShowActvnReRi2Fb:
        sig_name = "ExtrLiShowActvnReRi2Fb"
        sig_start_bit = 7
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class StsOfLedReLampLe2:
        sig_name = "StsOfLedReLampLe2"
        sig_start_bit = 17
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class DwnLoadStsFbOfReLampCtrlLe2:
        sig_name = "DwnLoadStsFbOfReLampCtrlLe2"
        sig_start_bit = 1
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class StsOfWelGbyReLe2:
        sig_name = "StsOfWelGbyReLe2"
        sig_start_bit = 55
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class StsOfLedRvsgLampRi2:
        sig_name = "StsOfLedRvsgLampRi2"
        sig_start_bit = 23
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class StsOfLedRvsgLampLe2:
        sig_name = "StsOfLedRvsgLampLe2"
        sig_start_bit = 21
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class DwnLoadStsFbOfReLampCtrlRi2:
        sig_name = "DwnLoadStsFbOfReLampCtrlRi2"
        sig_start_bit = 3
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class StsOfLedPosnLampRi2:
        sig_name = "StsOfLedPosnLampRi2"
        sig_start_bit = 11
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class StsOfLedStopLampLe2:
        sig_name = "StsOfLedStopLampLe2"
        sig_start_bit = 25
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class StsOfLedReLampRi2:
        sig_name = "StsOfLedReLampRi2"
        sig_start_bit = 19
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class StsOfLedReFogLampRi2:
        sig_name = "StsOfLedReFogLampRi2"
        sig_start_bit = 15
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class ExtrLiShowStoreStsReRi2:
        sig_name = "ExtrLiShowStoreStsReRi2"
        sig_start_bit = 49
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class ExtrLiShowStoreStsReLe2:
        sig_name = "ExtrLiShowStoreStsReLe2"
        sig_start_bit = 51
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class StsOfLedTurnIndcrRi2:
        sig_name = "StsOfLedTurnIndcrRi2"
        sig_start_bit = 31
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class StsOfLedStopLampRi2:
        sig_name = "StsOfLedStopLampRi2"
        sig_start_bit = 27
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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


class CemBodyExpoCommonFr18:
    msg_name = "CemBodyExpoCommonFr18"
    msg_id = 397
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.045
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class VehObjforADB6AdbAbsDist:
        sig_name = "VehObjforADB6AdbAbsDist"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class VehObjforADB6AdbHozlAgLe:
        sig_name = "VehObjforADB6AdbHozlAgLe"
        sig_start_bit = 10
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = "-40"
        sig_value_min = 0
        sig_value_max = 1600
        sig_value_init = 800
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 10
        bmuws_info = [(1, 0b00000111, 0b11111000, 3, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class VehObjforADB6AdbObjHozlAgSpdLe:
        sig_name = "VehObjforADB6AdbObjHozlAgSpdLe"
        sig_start_bit = 34
        sig_length = 9
        sig_value_factor = 0.2
        sig_value_offset = "-50"
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 250
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 34
        bmuws_info = [(4, 0b00000111, 0b11111000, 3, 0), (5, 0b11111100, 0b00000011, 6, 2)]

    class VehObjforADB6AdbVertAg:
        sig_name = "VehObjforADB6AdbVertAg"
        sig_start_bit = 63
        sig_length = 5
        sig_value_factor = 0.5
        sig_value_offset = "-3"
        sig_value_min = 0
        sig_value_max = 31
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

    class VehObjforADB6AdbObjHozlAgSpdRi:
        sig_name = "VehObjforADB6AdbObjHozlAgSpdRi"
        sig_start_bit = 41
        sig_length = 9
        sig_value_factor = 0.2
        sig_value_offset = "-50"
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 250
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 41
        bmuws_info = [(5, 0b00000011, 0b11111100, 2, 0), (6, 0b11111110, 0b00000001, 7, 1)]

    class VehObjforADB6AdbHozlAgRi:
        sig_name = "VehObjforADB6AdbHozlAgRi"
        sig_start_bit = 31
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = "-40"
        sig_value_min = 0
        sig_value_max = 1600
        sig_value_init = 800
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11100000, 0b00011111, 3, 5)]

    class VehObjforADB6AdbClassn:
        sig_name = "VehObjforADB6AdbClassn"
        sig_start_bit = 13
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
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

    class VehObjforADB6AdbTrkInfo:
        sig_name = "VehObjforADB6AdbTrkInfo"
        sig_start_bit = 48
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class VehObjforADB6AdbObjDir:
        sig_name = "VehObjforADB6AdbObjDir"
        sig_start_bit = 36
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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


class CemBodyExpoFr09:
    msg_name = "CemBodyExpoFr09"
    msg_id = 295
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLitPrmForLedMkrLampRi1OffsTiPrm:
        sig_name = "DwnLoadDynLitPrmForLedMkrLampRi1OffsTiPrm"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmForLedMkrLampRi1ModePrm:
        sig_name = "DwnLoadDynLitPrmForLedMkrLampRi1ModePrm"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
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

    class DwnLoadDynLitPrmForLedMkrLampRi1LowBriPrm:
        sig_name = "DwnLoadDynLitPrmForLedMkrLampRi1LowBriPrm"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmForLedMkrLampRi1Tistamp:
        sig_name = "DwnLoadDynLitPrmForLedMkrLampRi1Tistamp"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmForLedMkrLampRi1ContTiPrm:
        sig_name = "DwnLoadDynLitPrmForLedMkrLampRi1ContTiPrm"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmForLedMkrLampRi1UpprBriPrm:
        sig_name = "DwnLoadDynLitPrmForLedMkrLampRi1UpprBriPrm"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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


class CemBodyExpoFr38:
    msg_name = "CemBodyExpoFr38"
    msg_id = 323
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForLedHiBeamRiContTiPrm:
        sig_name = "DwnLoadDynLtgPrmForLedHiBeamRiContTiPrm"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLtgPrmForLedHiBeamRiTistamp:
        sig_name = "DwnLoadDynLtgPrmForLedHiBeamRiTistamp"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLtgPrmForLedHiBeamRiLowBriPrm:
        sig_name = "DwnLoadDynLtgPrmForLedHiBeamRiLowBriPrm"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLtgPrmForLedHiBeamRiModePrm:
        sig_name = "DwnLoadDynLtgPrmForLedHiBeamRiModePrm"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
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

    class DwnLoadDynLtgPrmForLedHiBeamRiUpprBriPrm:
        sig_name = "DwnLoadDynLtgPrmForLedHiBeamRiUpprBriPrm"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLtgPrmForLedHiBeamRiOffsTiPrm:
        sig_name = "DwnLoadDynLtgPrmForLedHiBeamRiOffsTiPrm"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]


class CemBodyExpoDevFr02:
    msg_name = "CemBodyExpoDevFr02"
    msg_id = 1431
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class CEMdevelpsignalgroupcheckFunctiondevpsignalgroup4:
        sig_name = "CEMdevelpsignalgroupcheckFunctiondevpsignalgroup4"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CEMdevelpsignalgroupcheckFunctiondevpsignalgroup7:
        sig_name = "CEMdevelpsignalgroupcheckFunctiondevpsignalgroup7"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CEMdevelpsignalgroupcheckFunctiondevpsignalgroup6:
        sig_name = "CEMdevelpsignalgroupcheckFunctiondevpsignalgroup6"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CEMdevelpsignalgroupcheckFunctiondevpsignalgroup8:
        sig_name = "CEMdevelpsignalgroupcheckFunctiondevpsignalgroup8"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CEMdevelpsignalgroupcheckFunctiondevpsignalgroup3:
        sig_name = "CEMdevelpsignalgroupcheckFunctiondevpsignalgroup3"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CEMdevelpsignalgroupcheckFunctiondevpsignalgroup5:
        sig_name = "CEMdevelpsignalgroupcheckFunctiondevpsignalgroup5"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CEMdevelpsignalgroupcheckFunctiondevpsignalgroup1:
        sig_name = "CEMdevelpsignalgroupcheckFunctiondevpsignalgroup1"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CEMdevelpsignalgroupcheckFunctiondevpsignalgroup2:
        sig_name = "CEMdevelpsignalgroupcheckFunctiondevpsignalgroup2"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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


class CemBodyExpoFr110:
    msg_name = "CemBodyExpoFr110"
    msg_id = 844
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForFrntRIGrp20LowBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp20LowBrightness"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntRIGrp20OffsetTime:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp20OffsetTime"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
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

    class DwnLoadDynLtgPrmForFrntRIGrp20Mode1:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp20Mode1"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
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

    class DwnLoadDynLtgPrmForFrntRIGrp20Timestamp:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp20Timestamp"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DwnLoadDynLtgPrmForFrntRIGrp20ContinueTime:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp20ContinueTime"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
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

    class DwnLoadDynLtgPrmForFrntRIGrp20HighBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp20HighBrightness"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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


class CemBodyExpoFr108:
    msg_name = "CemBodyExpoFr108"
    msg_id = 842
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForFrntRIGrp18LowBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp18LowBrightness"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntRIGrp18HighBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp18HighBrightness"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntRIGrp18Timestamp:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp18Timestamp"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DwnLoadDynLtgPrmForFrntRIGrp18ContinueTime:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp18ContinueTime"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
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

    class DwnLoadDynLtgPrmForFrntRIGrp18OffsetTime:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp18OffsetTime"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
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

    class DwnLoadDynLtgPrmForFrntRIGrp18Mode1:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp18Mode1"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
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
    rx_nodes = []

    class DwnLoadDynLitPrmLedReTurnIndcrRi1LowBriPrm:
        sig_name = "DwnLoadDynLitPrmLedReTurnIndcrRi1LowBriPrm"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmLedReTurnIndcrRi1ModePrm:
        sig_name = "DwnLoadDynLitPrmLedReTurnIndcrRi1ModePrm"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
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

    class DwnLoadDynLitPrmLedReTurnIndcrRi1UpprBriPrm:
        sig_name = "DwnLoadDynLitPrmLedReTurnIndcrRi1UpprBriPrm"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmLedReTurnIndcrRi1Tistamp:
        sig_name = "DwnLoadDynLitPrmLedReTurnIndcrRi1Tistamp"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmLedReTurnIndcrRi1ContTiPrm:
        sig_name = "DwnLoadDynLitPrmLedReTurnIndcrRi1ContTiPrm"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedReTurnIndcrRi1OffsTiPrm:
        sig_name = "DwnLoadDynLitPrmLedReTurnIndcrRi1OffsTiPrm"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]


class CemBodyExpoFr72:
    msg_name = "CemBodyExpoFr72"
    msg_id = 806
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForFrntLeGrp6HighBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp6HighBrightness"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntLeGrp6Mode1:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp6Mode1"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
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

    class DwnLoadDynLtgPrmForFrntLeGrp6ContinueTime:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp6ContinueTime"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
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

    class DwnLoadDynLtgPrmForFrntLeGrp6LowBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp6LowBrightness"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntLeGrp6Timestamp:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp6Timestamp"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DwnLoadDynLtgPrmForFrntLeGrp6OffsetTime:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp6OffsetTime"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
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


class CemBodyExpoCommonFr08:
    msg_name = "CemBodyExpoCommonFr08"
    msg_id = 128
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class AccrPedlRatChks:
        sig_name = "AccrPedlRatChks"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class AmbTRawAmbTVal:
        sig_name = "AmbTRawAmbTVal"
        sig_start_bit = 50
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = "-70.0"
        sig_value_min = 0
        sig_value_max = 2047
        sig_value_init = 700
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 50
        bmuws_info = [(6, 0b00000111, 0b11111000, 3, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class AmbTRawQly:
        sig_name = "AmbTRawQly"
        sig_start_bit = 52
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class BrkPedlSnsrChks:
        sig_name = "BrkPedlSnsrChks"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class AccrPedlRatAccrPedlRat:
        sig_name = "AccrPedlRatAccrPedlRat"
        sig_start_bit = 6
        sig_length = 15
        sig_value_factor = 0.00390625
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 25600
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 6
        bmuws_info = [(0, 0b01111111, 0b10000000, 7, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class BrkPedlSnsrSt:
        sig_name = "BrkPedlSnsrSt"
        sig_start_bit = 37
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class AccrPedlRatCntr:
        sig_name = "AccrPedlRatCntr"
        sig_start_bit = 31
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class TooManyCars:
        sig_name = "TooManyCars"
        sig_start_bit = 54
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class BrkPedlSnsrQf:
        sig_name = "BrkPedlSnsrQf"
        sig_start_bit = 39
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class BrkPedlSnsrCntr:
        sig_name = "BrkPedlSnsrCntr"
        sig_start_bit = 35
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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


class CemBodyExpoCommonFr09:
    msg_name = "CemBodyExpoCommonFr09"
    msg_id = 387
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class VehCfgPrmExtCCPBytePosn2:
        sig_name = "VehCfgPrmExtCCPBytePosn2"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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

    class VehCfgPrmExtCCPBytePosn5:
        sig_name = "VehCfgPrmExtCCPBytePosn5"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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

    class VehCfgPrmExtBlkIDBytePosn1:
        sig_name = "VehCfgPrmExtBlkIDBytePosn1"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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

    class VehCfgPrmExtCCPBytePosn6:
        sig_name = "VehCfgPrmExtCCPBytePosn6"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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

    class VehCfgPrmExtCCPBytePosn4:
        sig_name = "VehCfgPrmExtCCPBytePosn4"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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

    class VehCfgPrmExtCCPBytePosn3:
        sig_name = "VehCfgPrmExtCCPBytePosn3"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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

    class VehCfgPrmExtCCPBytePosn8:
        sig_name = "VehCfgPrmExtCCPBytePosn8"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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

    class VehCfgPrmExtCCPBytePosn7:
        sig_name = "VehCfgPrmExtCCPBytePosn7"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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


class CemBodyExpoFr17:
    msg_name = "CemBodyExpoFr17"
    msg_id = 303
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLitPrmLedRePosnLampLe2ContTiPrm:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe2ContTiPrm"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedRePosnLampLe2ModePrm:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe2ModePrm"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
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

    class DwnLoadDynLitPrmLedRePosnLampLe2UpprBriPrm:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe2UpprBriPrm"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmLedRePosnLampLe2LowBriPrm:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe2LowBriPrm"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmLedRePosnLampLe2Tistamp:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe2Tistamp"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmLedRePosnLampLe2OffsTiPrm:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe2OffsTiPrm"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]


class CemBodyExpoFr83:
    msg_name = "CemBodyExpoFr83"
    msg_id = 817
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForFrntLeGrp17Mode1:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp17Mode1"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
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

    class DwnLoadDynLtgPrmForFrntLeGrp17LowBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp17LowBrightness"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntLeGrp17Timestamp:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp17Timestamp"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DwnLoadDynLtgPrmForFrntLeGrp17OffsetTime:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp17OffsetTime"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
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

    class DwnLoadDynLtgPrmForFrntLeGrp17HighBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp17HighBrightness"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntLeGrp17ContinueTime:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp17ContinueTime"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
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


class CemBodyExpoCommonFr12:
    msg_name = "CemBodyExpoCommonFr12"
    msg_id = 391
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.045
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class VehObjforAHBAdbClassnQly:
        sig_name = "VehObjforAHBAdbClassnQly"
        sig_start_bit = 58
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
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

    class VehObjforAHBAdbDetdQly:
        sig_name = "VehObjforAHBAdbDetdQly"
        sig_start_bit = 60
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
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

    class VehObjforAHBAdbAbsDist:
        sig_name = "VehObjforAHBAdbAbsDist"
        sig_start_bit = 39
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11000000, 0b00111111, 2, 6)]

    class VehObjforAHBAdbObjHozlAgSpd:
        sig_name = "VehObjforAHBAdbObjHozlAgSpd"
        sig_start_bit = 15
        sig_length = 13
        sig_value_factor = 0.05
        sig_value_offset = "-144"
        sig_value_min = 0
        sig_value_max = 5760
        sig_value_init = 2880
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 15
        bmuws_info = [(1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111000, 0b00000111, 5, 3)]

    class VehObjforAHBAdbObjDir:
        sig_name = "VehObjforAHBAdbObjDir"
        sig_start_bit = 62
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class VehObjforAHBAdbVertAg:
        sig_name = "VehObjforAHBAdbVertAg"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 0.2
        sig_value_offset = "-15"
        sig_value_min = 0
        sig_value_max = 150
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

    class VehObjforAHBAdbObjVertAgSpd:
        sig_name = "VehObjforAHBAdbObjVertAgSpd"
        sig_start_bit = 42
        sig_length = 11
        sig_value_factor = 0.2
        sig_value_offset = "-144"
        sig_value_min = 0
        sig_value_max = 1440
        sig_value_init = 720
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 42
        bmuws_info = [(5, 0b00000111, 0b11111000, 3, 0), (6, 0b11111111, 0b00000000, 8, 0)]

    class VehObjforAHBAdbClassn:
        sig_name = "VehObjforAHBAdbClassn"
        sig_start_bit = 45
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
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

    class VehObjforAHBAdbTrkInfo:
        sig_name = "VehObjforAHBAdbTrkInfo"
        sig_start_bit = 63
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class VehObjforAHBAdbHozlAg:
        sig_name = "VehObjforAHBAdbHozlAg"
        sig_start_bit = 18
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = "-40"
        sig_value_min = 0
        sig_value_max = 1600
        sig_value_init = 800
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 18
        bmuws_info = [(2, 0b00000111, 0b11111000, 3, 0), (3, 0b11111111, 0b00000000, 8, 0)]


class CemBodyExpoFr77:
    msg_name = "CemBodyExpoFr77"
    msg_id = 811
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForFrntLeGrp11Mode1:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp11Mode1"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
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

    class DwnLoadDynLtgPrmForFrntLeGrp11OffsetTime:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp11OffsetTime"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
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

    class DwnLoadDynLtgPrmForFrntLeGrp11HighBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp11HighBrightness"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntLeGrp11Timestamp:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp11Timestamp"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DwnLoadDynLtgPrmForFrntLeGrp11LowBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp11LowBrightness"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntLeGrp11ContinueTime:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp11ContinueTime"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
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


class CemBodyExpoFr111:
    msg_name = "CemBodyExpoFr111"
    msg_id = 845
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForFrntRIGrp21HighBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp21HighBrightness"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntRIGrp21Timestamp:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp21Timestamp"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DwnLoadDynLtgPrmForFrntRIGrp21LowBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp21LowBrightness"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntRIGrp21ContinueTime:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp21ContinueTime"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
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

    class DwnLoadDynLtgPrmForFrntRIGrp21OffsetTime:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp21OffsetTime"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
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

    class DwnLoadDynLtgPrmForFrntRIGrp21Mode1:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp21Mode1"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
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


class CemBodyExpoCommonFr22:
    msg_name = "CemBodyExpoCommonFr22"
    msg_id = 400
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.045
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class SuspPosnVertLvlFrnt:
        sig_name = "SuspPosnVertLvlFrnt"
        sig_start_bit = 14
        sig_length = 15
        sig_value_factor = "6.2E-5"
        sig_value_offset = 0.0
        sig_value_min = -16129
        sig_value_max = 16130
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 14
        bmuws_info = [(1, 0b01111111, 0b10000000, 7, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class SuspPosnVertLvlReQf:
        sig_name = "SuspPosnVertLvlReQf"
        sig_start_bit = 3
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class SuspPosnVertLvlFrntQf:
        sig_name = "SuspPosnVertLvlFrntQf"
        sig_start_bit = 1
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class SuspPosnVertLvlRe:
        sig_name = "SuspPosnVertLvlRe"
        sig_start_bit = 30
        sig_length = 15
        sig_value_factor = "6.2E-5"
        sig_value_offset = 0.0
        sig_value_min = -16129
        sig_value_max = 16130
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 30
        bmuws_info = [(3, 0b01111111, 0b10000000, 7, 0), (4, 0b11111111, 0b00000000, 8, 0)]

    class SuspPosnVertAgGenQf:
        sig_name = "SuspPosnVertAgGenQf"
        sig_start_bit = 45
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class SuspPosnVertAgSuspPosnVertAg:
        sig_name = "SuspPosnVertAgSuspPosnVertAg"
        sig_start_bit = 43
        sig_length = 12
        sig_value_factor = "1.278941807E-4"
        sig_value_offset = 0.0
        sig_value_min = -2046
        sig_value_max = 2047
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 43
        bmuws_info = [(5, 0b00001111, 0b11110000, 4, 0), (6, 0b11111111, 0b00000000, 8, 0)]


class CemBodyExpoCommonFr16:
    msg_name = "CemBodyExpoCommonFr16"
    msg_id = 395
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.045
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class VehObjforADB4AdbAbsDist:
        sig_name = "VehObjforADB4AdbAbsDist"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class VehObjforADB4AdbVertAg:
        sig_name = "VehObjforADB4AdbVertAg"
        sig_start_bit = 63
        sig_length = 5
        sig_value_factor = 0.5
        sig_value_offset = "-3"
        sig_value_min = 0
        sig_value_max = 31
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

    class VehObjforADB4AdbObjHozlAgSpdRi:
        sig_name = "VehObjforADB4AdbObjHozlAgSpdRi"
        sig_start_bit = 41
        sig_length = 9
        sig_value_factor = 0.2
        sig_value_offset = "-50"
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 250
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 41
        bmuws_info = [(5, 0b00000011, 0b11111100, 2, 0), (6, 0b11111110, 0b00000001, 7, 1)]

    class VehObjforADB4AdbObjHozlAgSpdLe:
        sig_name = "VehObjforADB4AdbObjHozlAgSpdLe"
        sig_start_bit = 34
        sig_length = 9
        sig_value_factor = 0.2
        sig_value_offset = "-50"
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 250
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 34
        bmuws_info = [(4, 0b00000111, 0b11111000, 3, 0), (5, 0b11111100, 0b00000011, 6, 2)]

    class VehObjforADB4AdbHozlAgLe:
        sig_name = "VehObjforADB4AdbHozlAgLe"
        sig_start_bit = 10
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = "-40"
        sig_value_min = 0
        sig_value_max = 1600
        sig_value_init = 800
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 10
        bmuws_info = [(1, 0b00000111, 0b11111000, 3, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class VehObjforADB4AdbClassn:
        sig_name = "VehObjforADB4AdbClassn"
        sig_start_bit = 13
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
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

    class VehObjforADB4AdbTrkInfo:
        sig_name = "VehObjforADB4AdbTrkInfo"
        sig_start_bit = 48
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class VehObjforADB4AdbHozlAgRi:
        sig_name = "VehObjforADB4AdbHozlAgRi"
        sig_start_bit = 31
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = "-40"
        sig_value_min = 0
        sig_value_max = 1600
        sig_value_init = 800
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11100000, 0b00011111, 3, 5)]

    class VehObjforADB4AdbObjDir:
        sig_name = "VehObjforADB4AdbObjDir"
        sig_start_bit = 36
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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


class CemBodyExpoFr95:
    msg_name = "CemBodyExpoFr95"
    msg_id = 829
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForFrntRIGrp5OffsetTime:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp5OffsetTime"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
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

    class DwnLoadDynLtgPrmForFrntRIGrp5ContinueTime:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp5ContinueTime"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
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

    class DwnLoadDynLtgPrmForFrntRIGrp5Timestamp:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp5Timestamp"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DwnLoadDynLtgPrmForFrntRIGrp5LowBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp5LowBrightness"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntRIGrp5HighBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp5HighBrightness"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntRIGrp5Mode1:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp5Mode1"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
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


class BgmToHcmrBodyExpoDiagReqFrame:
    msg_name = "BgmToHcmrBodyExpoDiagReqFrame"
    msg_id = 1972
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []


class BgmToRcmmBodyExpoDiagReqFrame:
    msg_name = "BgmToRcmmBodyExpoDiagReqFrame"
    msg_id = 1975
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []


class CemBodyExpoCommonFr19:
    msg_name = "CemBodyExpoCommonFr19"
    msg_id = 398
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.045
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class VehObjforADB7AdbAbsDist:
        sig_name = "VehObjforADB7AdbAbsDist"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class VehObjforADB7AdbTrkInfo:
        sig_name = "VehObjforADB7AdbTrkInfo"
        sig_start_bit = 48
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class VehObjforADB7AdbObjHozlAgSpdLe:
        sig_name = "VehObjforADB7AdbObjHozlAgSpdLe"
        sig_start_bit = 34
        sig_length = 9
        sig_value_factor = 0.2
        sig_value_offset = "-50"
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 250
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 34
        bmuws_info = [(4, 0b00000111, 0b11111000, 3, 0), (5, 0b11111100, 0b00000011, 6, 2)]

    class VehObjforADB7AdbObjHozlAgSpdRi:
        sig_name = "VehObjforADB7AdbObjHozlAgSpdRi"
        sig_start_bit = 41
        sig_length = 9
        sig_value_factor = 0.2
        sig_value_offset = "-50"
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 250
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 41
        bmuws_info = [(5, 0b00000011, 0b11111100, 2, 0), (6, 0b11111110, 0b00000001, 7, 1)]

    class VehObjforADB7AdbHozlAgRi:
        sig_name = "VehObjforADB7AdbHozlAgRi"
        sig_start_bit = 31
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = "-40"
        sig_value_min = 0
        sig_value_max = 1600
        sig_value_init = 800
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11100000, 0b00011111, 3, 5)]

    class VehObjforADB7AdbClassn:
        sig_name = "VehObjforADB7AdbClassn"
        sig_start_bit = 13
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
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

    class VehObjforADB7AdbVertAg:
        sig_name = "VehObjforADB7AdbVertAg"
        sig_start_bit = 63
        sig_length = 5
        sig_value_factor = 0.5
        sig_value_offset = "-3"
        sig_value_min = 0
        sig_value_max = 31
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

    class VehObjforADB7AdbHozlAgLe:
        sig_name = "VehObjforADB7AdbHozlAgLe"
        sig_start_bit = 10
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = "-40"
        sig_value_min = 0
        sig_value_max = 1600
        sig_value_init = 800
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 10
        bmuws_info = [(1, 0b00000111, 0b11111000, 3, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class VehObjforADB7AdbObjDir:
        sig_name = "VehObjforADB7AdbObjDir"
        sig_start_bit = 36
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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


class CemBodyExpoFr113:
    msg_name = "CemBodyExpoFr113"
    msg_id = 847
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForFrntRIGrp23HighBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp23HighBrightness"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntRIGrp23Timestamp:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp23Timestamp"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DwnLoadDynLtgPrmForFrntRIGrp23Mode1:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp23Mode1"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
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

    class DwnLoadDynLtgPrmForFrntRIGrp23OffsetTime:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp23OffsetTime"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
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

    class DwnLoadDynLtgPrmForFrntRIGrp23LowBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp23LowBrightness"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntRIGrp23ContinueTime:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp23ContinueTime"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
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


class CemBodyExpoFr80:
    msg_name = "CemBodyExpoFr80"
    msg_id = 814
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForFrntLeGrp14ContinueTime:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp14ContinueTime"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
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

    class DwnLoadDynLtgPrmForFrntLeGrp14OffsetTime:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp14OffsetTime"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
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

    class DwnLoadDynLtgPrmForFrntLeGrp14Mode1:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp14Mode1"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
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

    class DwnLoadDynLtgPrmForFrntLeGrp14Timestamp:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp14Timestamp"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DwnLoadDynLtgPrmForFrntLeGrp14LowBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp14LowBrightness"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntLeGrp14HighBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp14HighBrightness"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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


class CemBodyExpoFr01:
    msg_name = "CemBodyExpoFr01"
    msg_id = 28
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class ExtrLiShowFileTxReq:
        sig_name = "ExtrLiShowFileTxReq"
        sig_start_bit = 42
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class ExtrLiShowActvnReq:
        sig_name = "ExtrLiShowActvnReq"
        sig_start_bit = 44
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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


class CemBodyExpoFr27:
    msg_name = "CemBodyExpoFr27"
    msg_id = 312
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLitPrmForLedLoBeamLeLowBriPrm:
        sig_name = "DwnLoadDynLitPrmForLedLoBeamLeLowBriPrm"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmForLedLoBeamLeOffsTiPrm:
        sig_name = "DwnLoadDynLitPrmForLedLoBeamLeOffsTiPrm"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmForLedLoBeamLeUpprBriPrm:
        sig_name = "DwnLoadDynLitPrmForLedLoBeamLeUpprBriPrm"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmForLedLoBeamLeContTiPrm:
        sig_name = "DwnLoadDynLitPrmForLedLoBeamLeContTiPrm"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmForLedLoBeamLeTistamp:
        sig_name = "DwnLoadDynLitPrmForLedLoBeamLeTistamp"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmForLedLoBeamLeModePrm:
        sig_name = "DwnLoadDynLitPrmForLedLoBeamLeModePrm"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
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


class CemBodyExpoFr69:
    msg_name = "CemBodyExpoFr69"
    msg_id = 803
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForFrntLeGrp3HighBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp3HighBrightness"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntLeGrp3Mode1:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp3Mode1"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
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

    class DwnLoadDynLtgPrmForFrntLeGrp3LowBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp3LowBrightness"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntLeGrp3Timestamp:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp3Timestamp"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DwnLoadDynLtgPrmForFrntLeGrp3OffsetTime:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp3OffsetTime"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
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

    class DwnLoadDynLtgPrmForFrntLeGrp3ContinueTime:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp3ContinueTime"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
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


class CemBodyExpoFr109:
    msg_name = "CemBodyExpoFr109"
    msg_id = 843
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForFrntRIGrp19OffsetTime:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp19OffsetTime"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
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

    class DwnLoadDynLtgPrmForFrntRIGrp19ContinueTime:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp19ContinueTime"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
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

    class DwnLoadDynLtgPrmForFrntRIGrp19Mode1:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp19Mode1"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
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

    class DwnLoadDynLtgPrmForFrntRIGrp19LowBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp19LowBrightness"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntRIGrp19Timestamp:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp19Timestamp"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DwnLoadDynLtgPrmForFrntRIGrp19HighBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp19HighBrightness"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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


class RcmlBodyExpoFr01:
    msg_name = "RcmlBodyExpoFr01"
    msg_id = 592
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class StsOfLedStopLampLe1:
        sig_name = "StsOfLedStopLampLe1"
        sig_start_bit = 21
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class DwnLoadStsFbOfReLampCtrlLe1:
        sig_name = "DwnLoadStsFbOfReLampCtrlLe1"
        sig_start_bit = 17
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class StsOfLedPosnLampLe1:
        sig_name = "StsOfLedPosnLampLe1"
        sig_start_bit = 9
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class ExtrLiShowActvnReLeFb:
        sig_name = "ExtrLiShowActvnReLeFb"
        sig_start_bit = 19
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class ExtrLiShowStoreStsReLe1:
        sig_name = "ExtrLiShowStoreStsReLe1"
        sig_start_bit = 1
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class StsOfLedReLampLe1:
        sig_name = "StsOfLedReLampLe1"
        sig_start_bit = 13
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class StsOfLedTurnIndcrLe1:
        sig_name = "StsOfLedTurnIndcrLe1"
        sig_start_bit = 29
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class StsOfWelGbyReLe1:
        sig_name = "StsOfWelGbyReLe1"
        sig_start_bit = 39
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class StsOfLedReFogLampLe1:
        sig_name = "StsOfLedReFogLampLe1"
        sig_start_bit = 11
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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


class CemBodyExpoFr68:
    msg_name = "CemBodyExpoFr68"
    msg_id = 802
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForFrntLeGrp2LowBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp2LowBrightness"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntLeGrp2Mode1:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp2Mode1"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
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

    class DwnLoadDynLtgPrmForFrntLeGrp2ContinueTime:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp2ContinueTime"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
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

    class DwnLoadDynLtgPrmForFrntLeGrp2HighBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp2HighBrightness"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntLeGrp2Timestamp:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp2Timestamp"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DwnLoadDynLtgPrmForFrntLeGrp2OffsetTime:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp2OffsetTime"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
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


class CemBodyExpoFr79:
    msg_name = "CemBodyExpoFr79"
    msg_id = 813
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForFrntLeGrp13Mode1:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp13Mode1"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
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

    class DwnLoadDynLtgPrmForFrntLeGrp13OffsetTime:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp13OffsetTime"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
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

    class DwnLoadDynLtgPrmForFrntLeGrp13LowBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp13LowBrightness"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntLeGrp13Timestamp:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp13Timestamp"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DwnLoadDynLtgPrmForFrntLeGrp13ContinueTime:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp13ContinueTime"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
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

    class DwnLoadDynLtgPrmForFrntLeGrp13HighBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp13HighBrightness"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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


class CEMBodyExpoCommonFr06:
    msg_name = "CEMBodyExpoCommonFr06"
    msg_id = 512
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class ExtrLiRlyPwrDwn:
        sig_name = "ExtrLiRlyPwrDwn"
        sig_start_bit = 6
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class VehBattUSysUQf:
        sig_name = "VehBattUSysUQf"
        sig_start_bit = 41
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class BkpOfDstTrvld:
        sig_name = "BkpOfDstTrvld"
        sig_start_bit = 23
        sig_length = 21
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 2000000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 21
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111000, 0b00000111, 5, 3)]

    class VehBattUSysU:
        sig_name = "VehBattUSysU"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 250
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


class CemBodyExpoFr74:
    msg_name = "CemBodyExpoFr74"
    msg_id = 808
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForFrntLeGrp8OffsetTime:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp8OffsetTime"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
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

    class DwnLoadDynLtgPrmForFrntLeGrp8ContinueTime:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp8ContinueTime"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
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

    class DwnLoadDynLtgPrmForFrntLeGrp8Timestamp:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp8Timestamp"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DwnLoadDynLtgPrmForFrntLeGrp8Mode1:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp8Mode1"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
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

    class DwnLoadDynLtgPrmForFrntLeGrp8LowBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp8LowBrightness"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntLeGrp8HighBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp8HighBrightness"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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


class CEMBodyExpoCommonFr07:
    msg_name = "CEMBodyExpoCommonFr07"
    msg_id = 544
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.06
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class ActnOfLedGrilleLamp:
        sig_name = "ActnOfLedGrilleLamp"
        sig_start_bit = 36
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class CarTiGlb:
        sig_name = "CarTiGlb"
        sig_start_bit = 7
        sig_length = 32
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 4294967295
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 32
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class TrSts:
        sig_name = "TrSts"
        sig_start_bit = 52
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
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

    class Body2CntrForMissCom:
        sig_name = "Body2CntrForMissCom"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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


class CemBodyExpoFr112:
    msg_name = "CemBodyExpoFr112"
    msg_id = 846
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForFrntRIGrp22OffsetTime:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp22OffsetTime"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
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

    class DwnLoadDynLtgPrmForFrntRIGrp22Mode1:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp22Mode1"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
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

    class DwnLoadDynLtgPrmForFrntRIGrp22LowBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp22LowBrightness"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntRIGrp22ContinueTime:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp22ContinueTime"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
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

    class DwnLoadDynLtgPrmForFrntRIGrp22HighBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp22HighBrightness"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntRIGrp22Timestamp:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp22Timestamp"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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


class CemBodyExpoFr05:
    msg_name = "CemBodyExpoFr05"
    msg_id = 291
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLitPrmLedReTurnIndcrRi2Tistamp:
        sig_name = "DwnLoadDynLitPrmLedReTurnIndcrRi2Tistamp"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmLedReTurnIndcrRi2UpprBriPrm:
        sig_name = "DwnLoadDynLitPrmLedReTurnIndcrRi2UpprBriPrm"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmLedReTurnIndcrRi2LowBriPrm:
        sig_name = "DwnLoadDynLitPrmLedReTurnIndcrRi2LowBriPrm"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmLedReTurnIndcrRi2OffsTiPrm:
        sig_name = "DwnLoadDynLitPrmLedReTurnIndcrRi2OffsTiPrm"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedReTurnIndcrRi2ContTiPrm:
        sig_name = "DwnLoadDynLitPrmLedReTurnIndcrRi2ContTiPrm"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedReTurnIndcrRi2ModePrm:
        sig_name = "DwnLoadDynLitPrmLedReTurnIndcrRi2ModePrm"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
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


class CemBodyExpoFr71:
    msg_name = "CemBodyExpoFr71"
    msg_id = 805
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForFrntLeGrp5HighBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp5HighBrightness"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntLeGrp5Timestamp:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp5Timestamp"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DwnLoadDynLtgPrmForFrntLeGrp5OffsetTime:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp5OffsetTime"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
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

    class DwnLoadDynLtgPrmForFrntLeGrp5Mode1:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp5Mode1"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
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

    class DwnLoadDynLtgPrmForFrntLeGrp5ContinueTime:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp5ContinueTime"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
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

    class DwnLoadDynLtgPrmForFrntLeGrp5LowBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp5LowBrightness"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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


class CemBodyExpoFr02:
    msg_name = "CemBodyExpoFr02"
    msg_id = 288
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLitPrmForLedStopLampRi2LowBriPrm:
        sig_name = "DwnLoadDynLitPrmForLedStopLampRi2LowBriPrm"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmForLedStopLampRi2Tistamp:
        sig_name = "DwnLoadDynLitPrmForLedStopLampRi2Tistamp"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmForLedStopLampRi2ContTiPrm:
        sig_name = "DwnLoadDynLitPrmForLedStopLampRi2ContTiPrm"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmForLedStopLampRi2ModePrm:
        sig_name = "DwnLoadDynLitPrmForLedStopLampRi2ModePrm"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
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

    class DwnLoadDynLitPrmForLedStopLampRi2UpprBriPrm:
        sig_name = "DwnLoadDynLitPrmForLedStopLampRi2UpprBriPrm"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmForLedStopLampRi2OffsTiPrm:
        sig_name = "DwnLoadDynLitPrmForLedStopLampRi2OffsTiPrm"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]


class CemBodyExpoFr49:
    msg_name = "CemBodyExpoFr49"
    msg_id = 325
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLitPrmLedRvsgLampRi2ModePrm:
        sig_name = "DwnLoadDynLitPrmLedRvsgLampRi2ModePrm"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
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

    class DwnLoadDynLitPrmLedRvsgLampRi2ContTiPrm:
        sig_name = "DwnLoadDynLitPrmLedRvsgLampRi2ContTiPrm"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedRvsgLampRi2OffsTiPrm:
        sig_name = "DwnLoadDynLitPrmLedRvsgLampRi2OffsTiPrm"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedRvsgLampRi2Tistamp:
        sig_name = "DwnLoadDynLitPrmLedRvsgLampRi2Tistamp"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmLedRvsgLampRi2UpprBriPrm:
        sig_name = "DwnLoadDynLitPrmLedRvsgLampRi2UpprBriPrm"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmLedRvsgLampRi2LowBriPrm:
        sig_name = "DwnLoadDynLitPrmLedRvsgLampRi2LowBriPrm"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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


class CemBodyExpoFr98:
    msg_name = "CemBodyExpoFr98"
    msg_id = 832
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForFrntRIGrp8OffsetTime:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp8OffsetTime"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
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

    class DwnLoadDynLtgPrmForFrntRIGrp8Timestamp:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp8Timestamp"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DwnLoadDynLtgPrmForFrntRIGrp8Mode1:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp8Mode1"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
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

    class DwnLoadDynLtgPrmForFrntRIGrp8HighBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp8HighBrightness"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntRIGrp8ContinueTime:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp8ContinueTime"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
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

    class DwnLoadDynLtgPrmForFrntRIGrp8LowBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp8LowBrightness"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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


class CemBodyExpoFr78:
    msg_name = "CemBodyExpoFr78"
    msg_id = 812
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForFrntLeGrp12HighBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp12HighBrightness"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntLeGrp12Timestamp:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp12Timestamp"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DwnLoadDynLtgPrmForFrntLeGrp12OffsetTime:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp12OffsetTime"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
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

    class DwnLoadDynLtgPrmForFrntLeGrp12Mode1:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp12Mode1"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
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

    class DwnLoadDynLtgPrmForFrntLeGrp12LowBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp12LowBrightness"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntLeGrp12ContinueTime:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp12ContinueTime"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
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


class CemBodyExpoFr102:
    msg_name = "CemBodyExpoFr102"
    msg_id = 836
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForFrntRIGrp12LowBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp12LowBrightness"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntRIGrp12Mode1:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp12Mode1"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
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

    class DwnLoadDynLtgPrmForFrntRIGrp12Timestamp:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp12Timestamp"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DwnLoadDynLtgPrmForFrntRIGrp12OffsetTime:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp12OffsetTime"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
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

    class DwnLoadDynLtgPrmForFrntRIGrp12HighBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp12HighBrightness"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntRIGrp12ContinueTime:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp12ContinueTime"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
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


class CemBodyExpoCommonFr21:
    msg_name = "CemBodyExpoCommonFr21"
    msg_id = 64
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.015
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class WipgAutFrntMod:
        sig_name = "WipgAutFrntMod"
        sig_start_bit = 59
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class RainLi:
        sig_name = "RainLi"
        sig_start_bit = 47
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class VehModMngtGlbSafe1FltEgyCnsWdSts:
        sig_name = "VehModMngtGlbSafe1FltEgyCnsWdSts"
        sig_start_bit = 36
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class CameraStsforAHBC:
        sig_name = "CameraStsforAHBC"
        sig_start_bit = 62
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class VehModMngtGlbSafe1EgyLvlElecMai:
        sig_name = "VehModMngtGlbSafe1EgyLvlElecMai"
        sig_start_bit = 27
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class VehModMngtGlbSafe1UsgModSts:
        sig_name = "VehModMngtGlbSafe1UsgModSts"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 13
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

    class VehModMngtGlbSafe1CarModSts1:
        sig_name = "VehModMngtGlbSafe1CarModSts1"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
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

    class VehModMngtGlbSafe1Chks:
        sig_name = "VehModMngtGlbSafe1Chks"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class VehModMngtGlbSafe1Cntr:
        sig_name = "VehModMngtGlbSafe1Cntr"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class VehModMngtGlbSafe1PwrLvlElecMai:
        sig_name = "VehModMngtGlbSafe1PwrLvlElecMai"
        sig_start_bit = 19
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class VehModMngtGlbSafe1EgyLvlElecSubtyp:
        sig_name = "VehModMngtGlbSafe1EgyLvlElecSubtyp"
        sig_start_bit = 31
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class VehModMngtGlbSafe1PwrLvlElecSubtyp:
        sig_name = "VehModMngtGlbSafe1PwrLvlElecSubtyp"
        sig_start_bit = 23
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp:
        sig_name = "VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp"
        sig_start_bit = 35
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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


class CemBodyExpoFr70:
    msg_name = "CemBodyExpoFr70"
    msg_id = 804
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForFrntLeGrp4ContinueTime:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp4ContinueTime"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
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

    class DwnLoadDynLtgPrmForFrntLeGrp4Timestamp:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp4Timestamp"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DwnLoadDynLtgPrmForFrntLeGrp4Mode1:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp4Mode1"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
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

    class DwnLoadDynLtgPrmForFrntLeGrp4HighBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp4HighBrightness"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntLeGrp4OffsetTime:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp4OffsetTime"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
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

    class DwnLoadDynLtgPrmForFrntLeGrp4LowBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp4LowBrightness"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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


class CemBodyExpoFr33:
    msg_name = "CemBodyExpoFr33"
    msg_id = 318
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForLedDaytiRunngLampRiLowBriPrm:
        sig_name = "DwnLoadDynLtgPrmForLedDaytiRunngLampRiLowBriPrm"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLtgPrmForLedDaytiRunngLampRiModePrm:
        sig_name = "DwnLoadDynLtgPrmForLedDaytiRunngLampRiModePrm"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
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

    class DwnLoadDynLtgPrmForLedDaytiRunngLampRiContTiPrm:
        sig_name = "DwnLoadDynLtgPrmForLedDaytiRunngLampRiContTiPrm"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLtgPrmForLedDaytiRunngLampRiUpprBriPrm:
        sig_name = "DwnLoadDynLtgPrmForLedDaytiRunngLampRiUpprBriPrm"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLtgPrmForLedDaytiRunngLampRiOffsTiPrm:
        sig_name = "DwnLoadDynLtgPrmForLedDaytiRunngLampRiOffsTiPrm"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLtgPrmForLedDaytiRunngLampRiTistamp:
        sig_name = "DwnLoadDynLtgPrmForLedDaytiRunngLampRiTistamp"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
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
    rx_nodes = []

    class DwnLoadDynLtgPrmForFrntRIGrp14ContinueTime:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp14ContinueTime"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
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

    class DwnLoadDynLtgPrmForFrntRIGrp14Timestamp:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp14Timestamp"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DwnLoadDynLtgPrmForFrntRIGrp14HighBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp14HighBrightness"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntRIGrp14OffsetTime:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp14OffsetTime"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
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

    class DwnLoadDynLtgPrmForFrntRIGrp14Mode1:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp14Mode1"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
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

    class DwnLoadDynLtgPrmForFrntRIGrp14LowBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp14LowBrightness"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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


class CemBodyExpoFr31:
    msg_name = "CemBodyExpoFr31"
    msg_id = 316
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForLedCornrgLampRiModePrm:
        sig_name = "DwnLoadDynLtgPrmForLedCornrgLampRiModePrm"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
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

    class DwnLoadDynLtgPrmForLedCornrgLampRiTistamp:
        sig_name = "DwnLoadDynLtgPrmForLedCornrgLampRiTistamp"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLtgPrmForLedCornrgLampRiUpprBriPrm:
        sig_name = "DwnLoadDynLtgPrmForLedCornrgLampRiUpprBriPrm"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLtgPrmForLedCornrgLampRiLowBriPrm:
        sig_name = "DwnLoadDynLtgPrmForLedCornrgLampRiLowBriPrm"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLtgPrmForLedCornrgLampRiContTiPrm:
        sig_name = "DwnLoadDynLtgPrmForLedCornrgLampRiContTiPrm"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLtgPrmForLedCornrgLampRiOffsTiPrm:
        sig_name = "DwnLoadDynLtgPrmForLedCornrgLampRiOffsTiPrm"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]


class CemBodyExpoFr30:
    msg_name = "CemBodyExpoFr30"
    msg_id = 315
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForLedCornrgLampLeUpprBriPrm:
        sig_name = "DwnLoadDynLtgPrmForLedCornrgLampLeUpprBriPrm"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLtgPrmForLedCornrgLampLeContTiPrm:
        sig_name = "DwnLoadDynLtgPrmForLedCornrgLampLeContTiPrm"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLtgPrmForLedCornrgLampLeModePrm:
        sig_name = "DwnLoadDynLtgPrmForLedCornrgLampLeModePrm"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
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

    class DwnLoadDynLtgPrmForLedCornrgLampLeLowBriPrm:
        sig_name = "DwnLoadDynLtgPrmForLedCornrgLampLeLowBriPrm"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLtgPrmForLedCornrgLampLeTistamp:
        sig_name = "DwnLoadDynLtgPrmForLedCornrgLampLeTistamp"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLtgPrmForLedCornrgLampLeOffsTiPrm:
        sig_name = "DwnLoadDynLtgPrmForLedCornrgLampLeOffsTiPrm"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]


class CemBodyExpoFr107:
    msg_name = "CemBodyExpoFr107"
    msg_id = 841
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForFrntRIGrp17Mode1:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp17Mode1"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
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

    class DwnLoadDynLtgPrmForFrntRIGrp17Timestamp:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp17Timestamp"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DwnLoadDynLtgPrmForFrntRIGrp17OffsetTime:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp17OffsetTime"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
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

    class DwnLoadDynLtgPrmForFrntRIGrp17HighBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp17HighBrightness"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntRIGrp17ContinueTime:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp17ContinueTime"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
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

    class DwnLoadDynLtgPrmForFrntRIGrp17LowBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp17LowBrightness"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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


class CemBodyExpoFr59:
    msg_name = "CemBodyExpoFr59"
    msg_id = 24
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class WelcomeGoodbyeModeReq:
        sig_name = "WelcomeGoodbyeModeReq"
        sig_start_bit = 7
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
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


class RcmmToBgmBodyExpoDiagRespFrame:
    msg_name = "RcmmToBgmBodyExpoDiagRespFrame"
    msg_id = 1719
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']


class HcmrBodyExpoFr02:
    msg_name = "HcmrBodyExpoFr02"
    msg_id = 594
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 3
    tx_node = None
    rx_nodes = ['BGM']

    class StsOfLedHiBeamRi:
        sig_name = "StsOfLedHiBeamRi"
        sig_start_bit = 1
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class StsOfLedLoBeamRi:
        sig_name = "StsOfLedLoBeamRi"
        sig_start_bit = 4
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class ExtrLiShowStoreStsFrntRi:
        sig_name = "ExtrLiShowStoreStsFrntRi"
        sig_start_bit = 7
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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


class CemBodyExpoFr51:
    msg_name = "CemBodyExpoFr51"
    msg_id = 538
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class IndcrPatCmd1WdTiOff:
        sig_name = "IndcrPatCmd1WdTiOff"
        sig_start_bit = 7
        sig_length = 16
        sig_value_factor = 0.001
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 65535
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class IndcrPatCmd1WdTiOn:
        sig_name = "IndcrPatCmd1WdTiOn"
        sig_start_bit = 23
        sig_length = 16
        sig_value_factor = 0.001
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 65535
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class ActvnOfIndcrIndcrOut:
        sig_name = "ActvnOfIndcrIndcrOut"
        sig_start_bit = 37
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class EmgyBrkLiIndcrTurn:
        sig_name = "EmgyBrkLiIndcrTurn"
        sig_start_bit = 49
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class ActvnOfIndcrIndcrOutChks:
        sig_name = "ActvnOfIndcrIndcrOutChks"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class IndcrSts:
        sig_name = "IndcrSts"
        sig_start_bit = 52
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class ActvnOfIndcrIndcrOutCntr:
        sig_name = "ActvnOfIndcrIndcrOutCntr"
        sig_start_bit = 35
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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


class CemBodyExpoFr41:
    msg_name = "CemBodyExpoFr41"
    msg_id = 377
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.065
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class ADataRawSafeCntr:
        sig_name = "ADataRawSafeCntr"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class ADataRawSafeALgt:
        sig_name = "ADataRawSafeALgt"
        sig_start_bit = 38
        sig_length = 15
        sig_value_factor = 0.0085
        sig_value_offset = 0.0
        sig_value_min = -16352
        sig_value_max = 16353
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 38
        bmuws_info = [(4, 0b01111111, 0b10000000, 7, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class ADataRawSafeAVertQf:
        sig_name = "ADataRawSafeAVertQf"
        sig_start_bit = 24
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Qf1_DevOfDataUndefd': 0, 'Qf1_DataTmpUndefdAndEvlnInProgs': 1, 'Qf1_DevOfDataNotWithinRngAllwd': 2, 'Qf1_DataCalcdWithDevDefd': 3}
        compute_method = None
        length = 2
        startbit = 24
        bmuws_info = [(3, 0b00000001, 0b11111110, 1, 0), (4, 0b10000000, 0b01111111, 1, 7)]

    class ADataRawSafeALat:
        sig_name = "ADataRawSafeALat"
        sig_start_bit = 23
        sig_length = 15
        sig_value_factor = 0.0085
        sig_value_offset = 0.0
        sig_value_min = -16352
        sig_value_max = 16353
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111110, 0b00000001, 7, 1)]

    class ADataRawSafeALgt1Qf:
        sig_name = "ADataRawSafeALgt1Qf"
        sig_start_bit = 9
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class ADataRawSafeALat1Qf:
        sig_name = "ADataRawSafeALat1Qf"
        sig_start_bit = 11
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class ADataRawSafeAVert:
        sig_name = "ADataRawSafeAVert"
        sig_start_bit = 55
        sig_length = 15
        sig_value_factor = 0.0085
        sig_value_offset = 0.0
        sig_value_min = -16352
        sig_value_max = 16353
        sig_value_init = 1155
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 55
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111110, 0b00000001, 7, 1)]

    class ADataRawSafeChks:
        sig_name = "ADataRawSafeChks"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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


class CemBodyExpoFr55:
    msg_name = "CemBodyExpoFr55"
    msg_id = 329
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLitPrmLedRePosnLampLe5UpprBriPrm:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe5UpprBriPrm"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmLedRePosnLampLe5OffsTiPrm:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe5OffsTiPrm"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedRePosnLampLe5ContTiPrm:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe5ContTiPrm"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedRePosnLampLe5LowBriPrm:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe5LowBriPrm"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmLedRePosnLampLe5ModePrm:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe5ModePrm"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
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

    class DwnLoadDynLitPrmLedRePosnLampLe5Tistamp:
        sig_name = "DwnLoadDynLitPrmLedRePosnLampLe5Tistamp"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]


class CemBodyExpoFr91:
    msg_name = "CemBodyExpoFr91"
    msg_id = 825
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForFrntRIGrp1Mode1:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp1Mode1"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
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

    class DwnLoadDynLtgPrmForFrntRIGrp1OffsetTime:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp1OffsetTime"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
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

    class DwnLoadDynLtgPrmForFrntRIGrp1HighBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp1HighBrightness"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntRIGrp1ContinueTime:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp1ContinueTime"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
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

    class DwnLoadDynLtgPrmForFrntRIGrp1LowBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp1LowBrightness"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntRIGrp1Timestamp:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp1Timestamp"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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


class CemBodyExpoFr96:
    msg_name = "CemBodyExpoFr96"
    msg_id = 830
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForFrntRIGrp6ContinueTime:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp6ContinueTime"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
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

    class DwnLoadDynLtgPrmForFrntRIGrp6Timestamp:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp6Timestamp"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DwnLoadDynLtgPrmForFrntRIGrp6HighBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp6HighBrightness"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntRIGrp6LowBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp6LowBrightness"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntRIGrp6Mode1:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp6Mode1"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
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

    class DwnLoadDynLtgPrmForFrntRIGrp6OffsetTime:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp6OffsetTime"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
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


class CemBodyExpoFr29:
    msg_name = "CemBodyExpoFr29"
    msg_id = 314
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForLedAllWthrLampRiTistamp:
        sig_name = "DwnLoadDynLtgPrmForLedAllWthrLampRiTistamp"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLtgPrmForLedAllWthrLampRiUpprBriPrm:
        sig_name = "DwnLoadDynLtgPrmForLedAllWthrLampRiUpprBriPrm"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLtgPrmForLedAllWthrLampRiContTiPrm:
        sig_name = "DwnLoadDynLtgPrmForLedAllWthrLampRiContTiPrm"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLtgPrmForLedAllWthrLampRiModePrm:
        sig_name = "DwnLoadDynLtgPrmForLedAllWthrLampRiModePrm"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
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

    class DwnLoadDynLtgPrmForLedAllWthrLampRiLowBriPrm:
        sig_name = "DwnLoadDynLtgPrmForLedAllWthrLampRiLowBriPrm"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLtgPrmForLedAllWthrLampRiOffsTiPrm:
        sig_name = "DwnLoadDynLtgPrmForLedAllWthrLampRiOffsTiPrm"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]


class CemBodyExpoFr07:
    msg_name = "CemBodyExpoFr07"
    msg_id = 293
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForLedLoBeamRiContTiPrm:
        sig_name = "DwnLoadDynLtgPrmForLedLoBeamRiContTiPrm"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLtgPrmForLedLoBeamRiTistamp:
        sig_name = "DwnLoadDynLtgPrmForLedLoBeamRiTistamp"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLtgPrmForLedLoBeamRiUpprBriPrm:
        sig_name = "DwnLoadDynLtgPrmForLedLoBeamRiUpprBriPrm"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLtgPrmForLedLoBeamRiModePrm:
        sig_name = "DwnLoadDynLtgPrmForLedLoBeamRiModePrm"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
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

    class DwnLoadDynLtgPrmForLedLoBeamRiLowBriPrm:
        sig_name = "DwnLoadDynLtgPrmForLedLoBeamRiLowBriPrm"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLtgPrmForLedLoBeamRiOffsTiPrm:
        sig_name = "DwnLoadDynLtgPrmForLedLoBeamRiOffsTiPrm"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]


class CemBodyExpoFr14:
    msg_name = "CemBodyExpoFr14"
    msg_id = 300
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLitPrmLedReFogLampLe2OffsTiPrm:
        sig_name = "DwnLoadDynLitPrmLedReFogLampLe2OffsTiPrm"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedReFogLampLe2ModePrm:
        sig_name = "DwnLoadDynLitPrmLedReFogLampLe2ModePrm"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
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

    class DwnLoadDynLitPrmLedReFogLampLe2LowBriPrm:
        sig_name = "DwnLoadDynLitPrmLedReFogLampLe2LowBriPrm"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmLedReFogLampLe2ContTiPrm:
        sig_name = "DwnLoadDynLitPrmLedReFogLampLe2ContTiPrm"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedReFogLampLe2UpprBriPrm:
        sig_name = "DwnLoadDynLitPrmLedReFogLampLe2UpprBriPrm"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmLedReFogLampLe2Tistamp:
        sig_name = "DwnLoadDynLitPrmLedReFogLampLe2Tistamp"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]


class CemBodyExpoFr63:
    msg_name = "CemBodyExpoFr63"
    msg_id = 789
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.94
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DHUcontrolleftlowbeamlamp:
        sig_name = "DHUcontrolleftlowbeamlamp"
        sig_start_bit = 9
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
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

    class DHUcontrolrightpositionLamp:
        sig_name = "DHUcontrolrightpositionLamp"
        sig_start_bit = 39
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
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

    class DHUcontrolrightcorneringlamp:
        sig_name = "DHUcontrolrightcorneringlamp"
        sig_start_bit = 17
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
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

    class DHUcontrolleftcorneringlamp:
        sig_name = "DHUcontrolleftcorneringlamp"
        sig_start_bit = 3
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
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

    class DHUcontrollefthighbeamlamp:
        sig_name = "DHUcontrollefthighbeamlamp"
        sig_start_bit = 11
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
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

    class DHUcontrolrightlowbeamlamp:
        sig_name = "DHUcontrolrightlowbeamlamp"
        sig_start_bit = 25
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
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

    class DHUcontrolleftheadcorneringlamp:
        sig_name = "DHUcontrolleftheadcorneringlamp"
        sig_start_bit = 13
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
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

    class DHUcontrolrightfroglight:
        sig_name = "DHUcontrolrightfroglight"
        sig_start_bit = 29
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
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

    class DHUcontrolrighthighbeamlamp:
        sig_name = "DHUcontrolrighthighbeamlamp"
        sig_start_bit = 27
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
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

    class DHUcontrolrightrearcorneringlamp:
        sig_name = "DHUcontrolrightrearcorneringlamp"
        sig_start_bit = 37
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
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

    class DHUcontrolrightbrakelight:
        sig_name = "DHUcontrolrightbrakelight"
        sig_start_bit = 19
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
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

    class DHUcontrolrightrearpositionLamp:
        sig_name = "DHUcontrolrightrearpositionLamp"
        sig_start_bit = 35
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
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

    class DHUcontrolCrossreversinglight:
        sig_name = "DHUcontrolCrossreversinglight"
        sig_start_bit = 7
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
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

    class DHUcontrolleftbrakelightLamp:
        sig_name = "DHUcontrolleftbrakelightLamp"
        sig_start_bit = 5
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
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

    class DHUcontrolleftfroglight:
        sig_name = "DHUcontrolleftfroglight"
        sig_start_bit = 15
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
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

    class DHUcontrolrightdaytimerunninglamp:
        sig_name = "DHUcontrolrightdaytimerunninglamp"
        sig_start_bit = 31
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
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

    class DHUcontrolleftpositionlight:
        sig_name = "DHUcontrolleftpositionlight"
        sig_start_bit = 21
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
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


class BgmToRcmrBodyExpoDiagReqFrame:
    msg_name = "BgmToRcmrBodyExpoDiagReqFrame"
    msg_id = 1974
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []


class CemBodyExpoFr82:
    msg_name = "CemBodyExpoFr82"
    msg_id = 816
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForFrntLeGrp16ContinueTime:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp16ContinueTime"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
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

    class DwnLoadDynLtgPrmForFrntLeGrp16Timestamp:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp16Timestamp"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DwnLoadDynLtgPrmForFrntLeGrp16Mode1:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp16Mode1"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
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

    class DwnLoadDynLtgPrmForFrntLeGrp16OffsetTime:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp16OffsetTime"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
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

    class DwnLoadDynLtgPrmForFrntLeGrp16LowBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp16LowBrightness"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntLeGrp16HighBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp16HighBrightness"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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


class CemBodyExpoFr97:
    msg_name = "CemBodyExpoFr97"
    msg_id = 831
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForFrntRIGrp7Timestamp:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp7Timestamp"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DwnLoadDynLtgPrmForFrntRIGrp7HighBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp7HighBrightness"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntRIGrp7LowBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp7LowBrightness"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntRIGrp7Mode1:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp7Mode1"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
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

    class DwnLoadDynLtgPrmForFrntRIGrp7ContinueTime:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp7ContinueTime"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
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

    class DwnLoadDynLtgPrmForFrntRIGrp7OffsetTime:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp7OffsetTime"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
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


class CemBodyExpoFr94:
    msg_name = "CemBodyExpoFr94"
    msg_id = 828
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForFrntRIGrp4LowBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp4LowBrightness"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntRIGrp4ContinueTime:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp4ContinueTime"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
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

    class DwnLoadDynLtgPrmForFrntRIGrp4Timestamp:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp4Timestamp"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DwnLoadDynLtgPrmForFrntRIGrp4OffsetTime:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp4OffsetTime"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
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

    class DwnLoadDynLtgPrmForFrntRIGrp4HighBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp4HighBrightness"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntRIGrp4Mode1:
        sig_name = "DwnLoadDynLtgPrmForFrntRIGrp4Mode1"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
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


class CemBodyExpoCommonFr13:
    msg_name = "CemBodyExpoCommonFr13"
    msg_id = 392
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.045
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class VehObjforADB1AdbTrkInfo:
        sig_name = "VehObjforADB1AdbTrkInfo"
        sig_start_bit = 48
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class VehObjforADB1AdbVertAg:
        sig_name = "VehObjforADB1AdbVertAg"
        sig_start_bit = 63
        sig_length = 5
        sig_value_factor = 0.5
        sig_value_offset = "-3"
        sig_value_min = 0
        sig_value_max = 31
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

    class VehObjforADB1AdbObjHozlAgSpdLe:
        sig_name = "VehObjforADB1AdbObjHozlAgSpdLe"
        sig_start_bit = 34
        sig_length = 9
        sig_value_factor = 0.2
        sig_value_offset = "-50"
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 250
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 34
        bmuws_info = [(4, 0b00000111, 0b11111000, 3, 0), (5, 0b11111100, 0b00000011, 6, 2)]

    class VehObjforADB1AdbHozlAgRi:
        sig_name = "VehObjforADB1AdbHozlAgRi"
        sig_start_bit = 31
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = "-40"
        sig_value_min = 0
        sig_value_max = 1600
        sig_value_init = 800
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11100000, 0b00011111, 3, 5)]

    class VehObjforADB1AdbObjDir:
        sig_name = "VehObjforADB1AdbObjDir"
        sig_start_bit = 36
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class VehObjforADB1AdbClassn:
        sig_name = "VehObjforADB1AdbClassn"
        sig_start_bit = 13
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
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

    class VehObjforADB1AdbObjHozlAgSpdRi:
        sig_name = "VehObjforADB1AdbObjHozlAgSpdRi"
        sig_start_bit = 41
        sig_length = 9
        sig_value_factor = 0.2
        sig_value_offset = "-50"
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 250
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 41
        bmuws_info = [(5, 0b00000011, 0b11111100, 2, 0), (6, 0b11111110, 0b00000001, 7, 1)]

    class VehObjforADB1AdbAbsDist:
        sig_name = "VehObjforADB1AdbAbsDist"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class VehObjforADB1AdbHozlAgLe:
        sig_name = "VehObjforADB1AdbHozlAgLe"
        sig_start_bit = 10
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = "-40"
        sig_value_min = 0
        sig_value_max = 1600
        sig_value_init = 800
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 10
        bmuws_info = [(1, 0b00000111, 0b11111000, 3, 0), (2, 0b11111111, 0b00000000, 8, 0)]


class CemBodyExpoFr67:
    msg_name = "CemBodyExpoFr67"
    msg_id = 801
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForFrntLeGrp1OffsetTime:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp1OffsetTime"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
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

    class DwnLoadDynLtgPrmForFrntLeGrp1Timestamp:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp1Timestamp"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DwnLoadDynLtgPrmForFrntLeGrp1HighBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp1HighBrightness"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntLeGrp1LowBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp1LowBrightness"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntLeGrp1Mode1:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp1Mode1"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
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

    class DwnLoadDynLtgPrmForFrntLeGrp1ContinueTime:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp1ContinueTime"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
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


class EtcToCemBodyExpoDevDiagFr03:
    msg_name = "EtcToCemBodyExpoDevDiagFr03"
    msg_id = 1425
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class CEMdevelpsignalgroupreqFunctiondevpsignalgroup3:
        sig_name = "CEMdevelpsignalgroupreqFunctiondevpsignalgroup3"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CEMdevelpsignalgroupreqFunctiondevpsignalgroup5:
        sig_name = "CEMdevelpsignalgroupreqFunctiondevpsignalgroup5"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CEMdevelpsignalgroupreqFunctiondevpsignalgroup8:
        sig_name = "CEMdevelpsignalgroupreqFunctiondevpsignalgroup8"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CEMdevelpsignalgroupreqFunctiondevpsignalgroup6:
        sig_name = "CEMdevelpsignalgroupreqFunctiondevpsignalgroup6"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CEMdevelpsignalgroupreqFunctiondevpsignalgroup7:
        sig_name = "CEMdevelpsignalgroupreqFunctiondevpsignalgroup7"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CEMdevelpsignalgroupreqFunctiondevpsignalgroup2:
        sig_name = "CEMdevelpsignalgroupreqFunctiondevpsignalgroup2"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CEMdevelpsignalgroupreqFunctiondevpsignalgroup1:
        sig_name = "CEMdevelpsignalgroupreqFunctiondevpsignalgroup1"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CEMdevelpsignalgroupreqFunctiondevpsignalgroup4:
        sig_name = "CEMdevelpsignalgroupreqFunctiondevpsignalgroup4"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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


class CemBodyExpoFr20:
    msg_name = "CemBodyExpoFr20"
    msg_id = 306
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLitPrmLedReTurnIndcrLe2UpprBriPrm:
        sig_name = "DwnLoadDynLitPrmLedReTurnIndcrLe2UpprBriPrm"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmLedReTurnIndcrLe2Tistamp:
        sig_name = "DwnLoadDynLitPrmLedReTurnIndcrLe2Tistamp"
        sig_start_bit = 8
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DwnLoadDynLitPrmLedReTurnIndcrLe2OffsTiPrm:
        sig_name = "DwnLoadDynLitPrmLedReTurnIndcrLe2OffsTiPrm"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedReTurnIndcrLe2ContTiPrm:
        sig_name = "DwnLoadDynLitPrmLedReTurnIndcrLe2ContTiPrm"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DwnLoadDynLitPrmLedReTurnIndcrLe2LowBriPrm:
        sig_name = "DwnLoadDynLitPrmLedReTurnIndcrLe2LowBriPrm"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DwnLoadDynLitPrmLedReTurnIndcrLe2ModePrm:
        sig_name = "DwnLoadDynLitPrmLedReTurnIndcrLe2ModePrm"
        sig_start_bit = 13
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 17
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


class CemBodyExpoFr81:
    msg_name = "CemBodyExpoFr81"
    msg_id = 815
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DwnLoadDynLtgPrmForFrntLeGrp15Mode1:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp15Mode1"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 49
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

    class DwnLoadDynLtgPrmForFrntLeGrp15Timestamp:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp15Timestamp"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DwnLoadDynLtgPrmForFrntLeGrp15ContinueTime:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp15ContinueTime"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
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

    class DwnLoadDynLtgPrmForFrntLeGrp15LowBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp15LowBrightness"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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

    class DwnLoadDynLtgPrmForFrntLeGrp15OffsetTime:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp15OffsetTime"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 63
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

    class DwnLoadDynLtgPrmForFrntLeGrp15HighBrightness:
        sig_name = "DwnLoadDynLtgPrmForFrntLeGrp15HighBrightness"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10
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


