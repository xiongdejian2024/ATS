lin_scheduleTable = {'LCU_LIN1ScheduleSerlNrPartNr_LCU_LIN1': [(0, 'WMMLCUL_LIN1Fr02', 0.015), (1, 'WMMLCUL_LIN1Fr03', 0.015), (2, 'RLSMLCUL_LIN1Fr03', 0.015), (3, 'RLSMLCUL_LIN1Fr04', 0.015), (4, 'RLSMLCUL_LIN1Fr05', 0.015), (5, 'RLMMLCUL_LIN1Fr01', 0.015), (6, 'RLMMLCUL_LIN1Fr03', 0.015), (7, 'MMDLCUL_LIN1Fr01', 0.015), (8, 'MMDLCUL_LIN1Fr03', 0.015), (9, 'HODLCUL_LIN1Fr02', 0.015), (10, 'HODLCUL_LIN1Fr03', 0.015)], 'LCUL_LIN1_DiagSchedule01': [(0, 'DiagRequest', 0.015), (1, 'DiagResponse', 0.015)], 'LCUL_LIN1Schedule01_LCUL_LIN1': [(0, 'HODLCUL_LIN1Fr01', 0.015), (1, 'LCULLCUL_LIN1Fr01', 0.015), (2, 'LCULLCUL_LIN1Fr02', 0.015), (3, 'LCULLCUL_LIN1Fr03', 0.015), (4, 'LCULLCUL_LIN1Fr04', 0.015), (5, 'LCULLCUL_LIN1Fr05', 0.015), (6, 'LCULLCUL_LIN1Fr06', 0.015), (7, 'LCULLCUL_LIN1Fr07', 0.015), (8, 'MMDLCUL_LIN1Fr02', 0.015), (9, 'RLMMLCUL_LIN1Fr02', 0.015), (10, 'RLSMLCUL_LIN1Fr01', 0.015), (11, 'RLSMLCUL_LIN1Fr02', 0.015), (12, 'WMMLCUL_LIN1Fr01', 0.015)]}


class HODLCUL_LIN1Fr02:
    msg_name = "HODLCUL_LIN1Fr02"
    msg_id = 1
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "HOD"
    rx_nodes = ['LCUL']
    sig_group_dict = {'HODPartNo': ['HODPartNoEndSgn1', 'HODPartNoEndSgn2', 'HODPartNoEndSgn3', 'HODPartNoNr1', 'HODPartNoNr2', 'HODPartNoNr3', 'HODPartNoNr4', 'HODPartNoNr5']}
    sig_group_dataid_dict = {}

    class HODPartNoNr3:
        sig_name = "HODPartNoNr3"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 40
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HODPartNoNr4:
        sig_name = "HODPartNoNr4"
        sig_start_bit = 48
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 48
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HODPartNoEndSgn3:
        sig_name = "HODPartNoEndSgn3"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HODPartNoEndSgn1:
        sig_name = "HODPartNoEndSgn1"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HODPartNoNr2:
        sig_name = "HODPartNoNr2"
        sig_start_bit = 32
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 32
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HODPartNoEndSgn2:
        sig_name = "HODPartNoEndSgn2"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 8
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HODPartNoNr1:
        sig_name = "HODPartNoNr1"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HODPartNoNr5:
        sig_name = "HODPartNoNr5"
        sig_start_bit = 56
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 56
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class RLSMLCUL_LIN1Fr01:
    msg_name = "RLSMLCUL_LIN1Fr01"
    msg_id = 16
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "RLSM"
    rx_nodes = ['LCUL', 'WMM']
    sig_group_dict = {'RainSnsrErr': ['RainSnsrErrCallErr', 'RainSnsrErrCallErrActv', 'RainSnsrErrRainDetnErr', 'RainSnsrErrRainDetnErrActv'], 'RainSnsrDiagc': ['RainSnsrDiagcRainSnsrHiTDetd', 'RainSnsrDiagcRainSnsrHiVoltDetd'], 'HudSnsrErr': ['HudSnsrErrParChk', 'HudSnsrErrSnsrErr'], 'OutdBri': ['OutdBriChks', 'OutdBriCntr', 'OutdBriSts']}
    sig_group_dataid_dict = {}

    class RainLi:
        sig_name = "RainLi"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
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

    class RainSnsrErrRainDetnErrActv:
        sig_name = "RainSnsrErrRainDetnErrActv"
        sig_start_bit = 59
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 59
        byte = 7
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class LiOprnMod:
        sig_name = "LiOprnMod"
        sig_start_bit = 5
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LiOperMod_Night': 0, 'LiOperMod_Day': 1, 'LiOperMod_Twli': 2, 'LiOperMod_Tnl': 3}
        compute_method = None
        length = 2
        startbit = 5
        byte = 0
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class RainSnsrErrRainDetnErr:
        sig_name = "RainSnsrErrRainDetnErr"
        sig_start_bit = 58
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
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

    class HudSnsrErrSnsrErr:
        sig_name = "HudSnsrErrSnsrErr"
        sig_start_bit = 4
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SnsrErr_FltStsTestPassd1': 0, 'SnsrErr_FltStsTestFaild2': 1}
        compute_method = None
        length = 1
        startbit = 4
        byte = 0
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class RainSnsrErrCallErrActv:
        sig_name = "RainSnsrErrCallErrActv"
        sig_start_bit = 57
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 57
        byte = 7
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class HudSnsrErrParChk:
        sig_name = "HudSnsrErrParChk"
        sig_start_bit = 3
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ParChk_Unevennrof': 0, 'ParChk_Evennrof': 1}
        compute_method = None
        length = 1
        startbit = 3
        byte = 0
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class AutWinWipgCmd:
        sig_name = "AutWinWipgCmd"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WipgSpd_WipgSpd0Rpm': 0, 'WipgSpd_WipgSpd40Rpm': 1, 'WipgSpd_WipgSpd43Rpm': 2, 'WipgSpd_WipgSpd46Rpm': 3, 'WipgSpd_WipgSpd50Rpm': 4, 'WipgSpd_WipgSpd54Rpm': 5, 'WipgSpd_WipgSpd57Rpm': 6, 'WipgSpd_WipgSpd60Rpm': 7}
        compute_method = None
        length = 3
        startbit = 0
        byte = 0
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class RainfallAmnt:
        sig_name = "RainfallAmnt"
        sig_start_bit = 19
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'RainfallAmnt_0': 0, 'RainfallAmnt_1': 1, 'RainfallAmnt_2': 2, 'RainfallAmnt_3': 3, 'RainfallAmnt_4': 4, 'RainfallAmnt_5': 5, 'RainfallAmnt_6': 6, 'RainfallAmnt_7': 7, 'RainfallAmnt_8': 8, 'RainfallAmnt_9': 9, 'RainfallAmnt_10': 10, 'RainfallAmnt_11': 11, 'RainfallAmnt_12': 12, 'RainfallAmnt_13': 13, 'RainfallAmnt_InitValue': 14, 'RainfallAmnt_Error': 15}
        compute_method = None
        length = 4
        startbit = 19
        byte = 2
        mask = 0b01111000
        unmask = 0b10000111
        shift = 3

    class RainSnsrErrCallErr:
        sig_name = "RainSnsrErrCallErr"
        sig_start_bit = 56
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
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

    class RainSnsrDiagcRainSnsrHiTDetd:
        sig_name = "RainSnsrDiagcRainSnsrHiTDetd"
        sig_start_bit = 35
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 35
        byte = 4
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class OutdBriCntr:
        sig_name = "OutdBriCntr"
        sig_start_bit = 48
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 48
        byte = 6
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class OutdBriChks:
        sig_name = "OutdBriChks"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 40
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CmptFrntWindDewT:
        sig_name = "CmptFrntWindDewT"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -40
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Intel"
        sig_value_init = 600
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 8
        bmuws_info = [(1, 0b11111111, 0b00000000, 8, 0), (2, 0b00000111, 0b11111000, 3, 0)]

    class RainDetected:
        sig_name = "RainDetected"
        sig_start_bit = 54
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OffOnNoCmd_NoCmd': 0, 'OffOnNoCmd_Off': 1, 'OffOnNoCmd_On': 2}
        compute_method = None
        length = 2
        startbit = 54
        byte = 6
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class CmptFrntWindT:
        sig_name = "CmptFrntWindT"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -40
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Intel"
        sig_value_init = 650
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 24
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b00000111, 0b11111000, 3, 0)]

    class RainSnsrDiagcRainSnsrHiVoltDetd:
        sig_name = "RainSnsrDiagcRainSnsrHiVoltDetd"
        sig_start_bit = 36
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
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

    class OutdBriSts:
        sig_name = "OutdBriSts"
        sig_start_bit = 52
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OutdBriSts_Ukwn': 0, 'OutdBriSts_Night': 1, 'OutdBriSts_Day': 2, 'OutdBriSts_Invld': 3}
        compute_method = None
        length = 2
        startbit = 52
        byte = 6
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4


class LCULLCUL_LIN1Fr07:
    msg_name = "LCULLCUL_LIN1Fr07"
    msg_id = 9
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "LCUL"
    rx_nodes = ['RLSM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class RainSnsrLiThd:
        sig_name = "RainSnsrLiThd"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 4
        sig_value_factor = 5
        sig_value_offset = -40
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Intel"
        sig_value_init = 8
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 0
        byte = 0
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0


class LCULLCUL_LIN1Fr03:
    msg_name = "LCULLCUL_LIN1Fr03"
    msg_id = 5
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "LCUL"
    rx_nodes = ['RLMM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class VehTiGlb:
        sig_name = "VehTiGlb"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 32
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4294967295
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 32
        startbit = 16
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0)]


class RLSMLCUL_LIN1Fr05:
    msg_name = "RLSMLCUL_LIN1Fr05"
    msg_id = 20
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "RLSM"
    rx_nodes = ['LCUL']
    sig_group_dict = {'TwliBriRaw': ['TwliBriRawQf', 'TwliBriRawTwliBriRaw']}
    sig_group_dataid_dict = {}

    class TwliBriRawQf:
        sig_name = "TwliBriRawQf"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 0
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class TwliBriRawTwliBriRaw:
        sig_name = "TwliBriRawTwliBriRaw"
        sig_start_bit = 2
        update_id_bit = None
        sig_length = 14
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 10000
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 14
        startbit = 2
        bmuws_info = [(0, 0b11111100, 0b00000011, 6, 2), (1, 0b11111111, 0b00000000, 8, 0)]


class RLMMLCUL_LIN1Fr03:
    msg_name = "RLMMLCUL_LIN1Fr03"
    msg_id = 15
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "RLMM"
    rx_nodes = ['LCUL']
    sig_group_dict = {'RLMMSerNo': ['RLMMSerNoNr1', 'RLMMSerNoNr2', 'RLMMSerNoNr3', 'RLMMSerNoNr4']}
    sig_group_dataid_dict = {}

    class RLMMSerNoNr3:
        sig_name = "RLMMSerNoNr3"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RLMMSerNoNr2:
        sig_name = "RLMMSerNoNr2"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 8
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RLMMSerNoNr1:
        sig_name = "RLMMSerNoNr1"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RLMMSerNoNr4:
        sig_name = "RLMMSerNoNr4"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class MMDLCUL_LIN1Fr02:
    msg_name = "MMDLCUL_LIN1Fr02"
    msg_id = 11
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "MMD"
    rx_nodes = ['LCUL']
    sig_group_dict = {'SeatMassgFrntLeRunSts': ['SeatMassgFrntLeRunStsMassgLvlSts', 'SeatMassgFrntLeRunStsMassgProg', 'SeatMassgFrntLeRunStsOnOffNoCmd']}
    sig_group_dataid_dict = {}

    class SeatMassgFrntLeRunStsOnOffNoCmd:
        sig_name = "SeatMassgFrntLeRunStsOnOffNoCmd"
        sig_start_bit = 13
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffNoCmd_NoCmd': 0, 'OnOffNoCmd_OFF': 1, 'OnOffNoCmd_ON': 2}
        compute_method = None
        length = 2
        startbit = 13
        byte = 1
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class SeatMassgEcuFrntLeErrSts:
        sig_name = "SeatMassgEcuFrntLeErrSts"
        sig_start_bit = 2
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EcuErrorType_Idle': 0, 'EcuErrorType_InternalError': 1, 'EcuErrorType_ExternalError': 2, 'EcuErrorType_reserved': 3}
        compute_method = None
        length = 2
        startbit = 2
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class SeatLumFrntLeRunSts:
        sig_name = "SeatLumFrntLeRunSts"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OffOnNoCmd_NoCmd': 0, 'OffOnNoCmd_Off': 1, 'OffOnNoCmd_On': 2}
        compute_method = None
        length = 2
        startbit = 0
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class SeatMassgFrntLeRunStsMassgProg:
        sig_name = "SeatMassgFrntLeRunStsMassgProg"
        sig_start_bit = 10
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'MassgProg_Prog0': 0, 'MassgProg_Prog1': 1, 'MassgProg_Prog2': 2, 'MassgProg_Prog3': 3, 'MassgProg_Prog4': 4, 'MassgProg_Prog5': 5, 'MassgProg_Prog6': 6, 'MassgProg_Prog7': 7}
        compute_method = None
        length = 3
        startbit = 10
        byte = 1
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class SeatMassgFrntLeRunStsMassgLvlSts:
        sig_name = "SeatMassgFrntLeRunStsMassgLvlSts"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'MassgLvlSts_Idle': 0, 'MassgLvlSts_Low': 1, 'MassgLvlSts_Mid': 2, 'MassgLvlSts_High': 3}
        compute_method = None
        length = 2
        startbit = 8
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0


class DiagResponse:
    msg_name = "DiagResponse"
    msg_id = 61
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['LCUL']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class RLMMLCUL_LIN1Fr02:
    msg_name = "RLMMLCUL_LIN1Fr02"
    msg_id = 14
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "RLMM"
    rx_nodes = ['LCUL']
    sig_group_dict = {'SeatMassgReLeRunSts': ['SeatMassgReLeRunStsMassgLvlSts', 'SeatMassgReLeRunStsMassgProg', 'SeatMassgReLeRunStsOnOffNoCmd']}
    sig_group_dataid_dict = {}

    class SeatMassgReLeRunStsMassgProg:
        sig_name = "SeatMassgReLeRunStsMassgProg"
        sig_start_bit = 10
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'MassgProg_Prog0': 0, 'MassgProg_Prog1': 1, 'MassgProg_Prog2': 2, 'MassgProg_Prog3': 3, 'MassgProg_Prog4': 4, 'MassgProg_Prog5': 5, 'MassgProg_Prog6': 6, 'MassgProg_Prog7': 7}
        compute_method = None
        length = 3
        startbit = 10
        byte = 1
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class SeatLumReLeRunSts:
        sig_name = "SeatLumReLeRunSts"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OffOnNoCmd_NoCmd': 0, 'OffOnNoCmd_Off': 1, 'OffOnNoCmd_On': 2}
        compute_method = None
        length = 2
        startbit = 0
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class SeatMassgReLeRunStsMassgLvlSts:
        sig_name = "SeatMassgReLeRunStsMassgLvlSts"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'MassgLvlSts_Idle': 0, 'MassgLvlSts_Low': 1, 'MassgLvlSts_Mid': 2, 'MassgLvlSts_High': 3}
        compute_method = None
        length = 2
        startbit = 8
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class SeatMassgReLeRunStsOnOffNoCmd:
        sig_name = "SeatMassgReLeRunStsOnOffNoCmd"
        sig_start_bit = 13
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffNoCmd_NoCmd': 0, 'OnOffNoCmd_OFF': 1, 'OnOffNoCmd_ON': 2}
        compute_method = None
        length = 2
        startbit = 13
        byte = 1
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class SeatMassgEcuReLeErrSts:
        sig_name = "SeatMassgEcuReLeErrSts"
        sig_start_bit = 2
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EcuErrorType_Idle': 0, 'EcuErrorType_InternalError': 1, 'EcuErrorType_ExternalError': 2, 'EcuErrorType_reserved': 3}
        compute_method = None
        length = 2
        startbit = 2
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2


class WMMLCUL_LIN1Fr02:
    msg_name = "WMMLCUL_LIN1Fr02"
    msg_id = 22
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "WMM"
    rx_nodes = ['LCUL']
    sig_group_dict = {'WMMPartNo': ['WMMPartNoEndSgn1', 'WMMPartNoEndSgn2', 'WMMPartNoEndSgn3', 'WMMPartNoNr1', 'WMMPartNoNr2', 'WMMPartNoNr3', 'WMMPartNoNr4', 'WMMPartNoNr5']}
    sig_group_dataid_dict = {}

    class WMMPartNoNr1:
        sig_name = "WMMPartNoNr1"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class WMMPartNoEndSgn3:
        sig_name = "WMMPartNoEndSgn3"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class WMMPartNoNr5:
        sig_name = "WMMPartNoNr5"
        sig_start_bit = 56
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 56
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class WMMPartNoNr2:
        sig_name = "WMMPartNoNr2"
        sig_start_bit = 32
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 32
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class WMMPartNoEndSgn1:
        sig_name = "WMMPartNoEndSgn1"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class WMMPartNoNr4:
        sig_name = "WMMPartNoNr4"
        sig_start_bit = 48
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 48
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class WMMPartNoNr3:
        sig_name = "WMMPartNoNr3"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 40
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class WMMPartNoEndSgn2:
        sig_name = "WMMPartNoEndSgn2"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 8
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class LCULLCUL_LIN1Fr02:
    msg_name = "LCULLCUL_LIN1Fr02"
    msg_id = 4
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "LCUL"
    rx_nodes = ['WMM', 'RLSM']
    sig_group_dict = {'RainSnsrSnvtyForUsrSnvty': ['RainSnsrSnvtyForUsrSnvty0', 'RainSnsrSnvtyForUsrSnvty1', 'RainSnsrSnvtyForUsrSnvty2', 'RainSnsrSnvtyForUsrSnvty3', 'RainSnsrSnvtyForUsrSnvty4', 'RainSnsrSnvtyForUsrSnvty5', 'RainSnsrSnvtyForUsrSnvty6']}
    sig_group_dataid_dict = {}

    class RainSnsrSnvtyForUsrSnvty4:
        sig_name = "RainSnsrSnvtyForUsrSnvty4"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 16
        byte = 2
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class VehTyp:
        sig_name = "VehTyp"
        sig_start_bit = 28
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 28
        byte = 3
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class ReAdaptReq:
        sig_name = "ReAdaptReq"
        sig_start_bit = 32
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
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

    class RainSnsrSnvtyForUsrSnvty0:
        sig_name = "RainSnsrSnvtyForUsrSnvty0"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 0
        byte = 0
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class RainSnsrSnvtyForUsrSnvty6:
        sig_name = "RainSnsrSnvtyForUsrSnvty6"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 24
        byte = 3
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class RainSnsrSnvtyForUsrSnvty1:
        sig_name = "RainSnsrSnvtyForUsrSnvty1"
        sig_start_bit = 4
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 4
        byte = 0
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class RainSnsrSnvtyForUsrSnvty2:
        sig_name = "RainSnsrSnvtyForUsrSnvty2"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 8
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class RainSnsrSnvtyForUsrSnvty3:
        sig_name = "RainSnsrSnvtyForUsrSnvty3"
        sig_start_bit = 12
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 12
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class WshrLvrPosnSafe:
        sig_name = "WshrLvrPosnSafe"
        sig_start_bit = 41
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffCrit1_NotVld1': 0, 'OnOffCrit1_Off': 1, 'OnOffCrit1_On': 2, 'OnOffCrit1_NotVld2': 3}
        compute_method = None
        length = 2
        startbit = 41
        byte = 5
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class WiprMotIntlCmd:
        sig_name = "WiprMotIntlCmd"
        sig_start_bit = 37
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WipgSpdIntlCmd_Posn0': 0, 'WipgSpdIntlCmd_Posn1': 1, 'WipgSpdIntlCmd_Posn2': 2, 'WipgSpdIntlCmd_Posn3': 3, 'WipgSpdIntlCmd_Posn4': 4, 'WipgSpdIntlCmd_Posn5': 5, 'WipgSpdIntlCmd_Posn6': 6, 'WipgSpdIntlCmd_Posn7': 7}
        compute_method = None
        length = 3
        startbit = 37
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class WiprMotFrntOffsAg:
        sig_name = "WiprMotFrntOffsAg"
        sig_start_bit = 33
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 33
        byte = 4
        mask = 0b00011110
        unmask = 0b11100001
        shift = 1

    class RainSnsrSnvtyForUsrSnvty5:
        sig_name = "RainSnsrSnvtyForUsrSnvty5"
        sig_start_bit = 20
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 20
        byte = 2
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class WiprPosnForSrvReq:
        sig_name = "WiprPosnForSrvReq"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
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


class MMDLCUL_LIN1Fr01:
    msg_name = "MMDLCUL_LIN1Fr01"
    msg_id = 10
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "MMD"
    rx_nodes = ['LCUL']
    sig_group_dict = {'MMDPartNo': ['MMDPartNoEndSgn1', 'MMDPartNoEndSgn2', 'MMDPartNoEndSgn3', 'MMDPartNoNr1', 'MMDPartNoNr2', 'MMDPartNoNr3', 'MMDPartNoNr4', 'MMDPartNoNr5']}
    sig_group_dataid_dict = {}

    class MMDPartNoEndSgn3:
        sig_name = "MMDPartNoEndSgn3"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class MMDPartNoNr3:
        sig_name = "MMDPartNoNr3"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 40
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class MMDPartNoEndSgn1:
        sig_name = "MMDPartNoEndSgn1"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class MMDPartNoNr5:
        sig_name = "MMDPartNoNr5"
        sig_start_bit = 56
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 56
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class MMDPartNoNr1:
        sig_name = "MMDPartNoNr1"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class MMDPartNoNr2:
        sig_name = "MMDPartNoNr2"
        sig_start_bit = 32
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 32
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class MMDPartNoEndSgn2:
        sig_name = "MMDPartNoEndSgn2"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 8
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class MMDPartNoNr4:
        sig_name = "MMDPartNoNr4"
        sig_start_bit = 48
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 48
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class RLMMLCUL_LIN1Fr01:
    msg_name = "RLMMLCUL_LIN1Fr01"
    msg_id = 13
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "RLMM"
    rx_nodes = ['LCUL']
    sig_group_dict = {'RLMMPartNo': ['RLMMPartNoEndSgn1', 'RLMMPartNoEndSgn2', 'RLMMPartNoEndSgn3', 'RLMMPartNoNr1', 'RLMMPartNoNr2', 'RLMMPartNoNr3', 'RLMMPartNoNr4', 'RLMMPartNoNr5']}
    sig_group_dataid_dict = {}

    class RLMMPartNoNr3:
        sig_name = "RLMMPartNoNr3"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 40
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RLMMPartNoNr2:
        sig_name = "RLMMPartNoNr2"
        sig_start_bit = 32
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 32
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RLMMPartNoNr1:
        sig_name = "RLMMPartNoNr1"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RLMMPartNoNr4:
        sig_name = "RLMMPartNoNr4"
        sig_start_bit = 48
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 48
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RLMMPartNoEndSgn3:
        sig_name = "RLMMPartNoEndSgn3"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RLMMPartNoEndSgn2:
        sig_name = "RLMMPartNoEndSgn2"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 8
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RLMMPartNoEndSgn1:
        sig_name = "RLMMPartNoEndSgn1"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RLMMPartNoNr5:
        sig_name = "RLMMPartNoNr5"
        sig_start_bit = 56
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 56
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class MMDLCUL_LIN1Fr03:
    msg_name = "MMDLCUL_LIN1Fr03"
    msg_id = 12
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "MMD"
    rx_nodes = ['LCUL']
    sig_group_dict = {'MMDSerNo': ['MMDSerNoNr1', 'MMDSerNoNr2', 'MMDSerNoNr3', 'MMDSerNoNr4']}
    sig_group_dataid_dict = {}

    class MMDSerNoNr3:
        sig_name = "MMDSerNoNr3"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class MMDSerNoNr4:
        sig_name = "MMDSerNoNr4"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class MMDSerNoNr2:
        sig_name = "MMDSerNoNr2"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 8
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class MMDSerNoNr1:
        sig_name = "MMDSerNoNr1"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class DiagRequest:
    msg_name = "DiagRequest"
    msg_id = 60
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "LCUL"
    rx_nodes = []
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class RLSMLCUL_LIN1Fr04:
    msg_name = "RLSMLCUL_LIN1Fr04"
    msg_id = 19
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "RLSM"
    rx_nodes = ['LCUL']
    sig_group_dict = {'RLSMSerNo': ['RLSMSerNoNr1', 'RLSMSerNoNr2', 'RLSMSerNoNr3', 'RLSMSerNoNr4']}
    sig_group_dataid_dict = {}

    class RLSMSerNoNr4:
        sig_name = "RLSMSerNoNr4"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RLSMSerNoNr2:
        sig_name = "RLSMSerNoNr2"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 8
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RLSMSerNoNr1:
        sig_name = "RLSMSerNoNr1"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RLSMSerNoNr3:
        sig_name = "RLSMSerNoNr3"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class RLSMLCUL_LIN1Fr02:
    msg_name = "RLSMLCUL_LIN1Fr02"
    msg_id = 17
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "RLSM"
    rx_nodes = ['LCUL', 'WMM']
    sig_group_dict = {'AmbIllmnFwdSts': ['AmbIllmnFwdStsAmbIllmn1', 'AmbIllmnFwdStsAmbIllmn2', 'AmbIllmnFwdStsChks', 'AmbIllmnFwdStsCntr']}
    sig_group_dataid_dict = {}

    class WipgAutFrntMod:
        sig_name = "WipgAutFrntMod"
        sig_start_bit = 26
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WipgAutFrntMod_Off': 0, 'WipgAutFrntMod_ImdMod': 1, 'WipgAutFrntMod_Intlmod': 2, 'WipgAutFrntMod_ContnsMod': 3}
        compute_method = None
        length = 2
        startbit = 26
        byte = 3
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class AmbIllmnFwdStsCntr:
        sig_name = "AmbIllmnFwdStsCntr"
        sig_start_bit = 56
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 56
        byte = 7
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class SolarSnsrLeValue:
        sig_name = "SolarSnsrLeValue"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 5
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 8
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SolarSnsrErr:
        sig_name = "SolarSnsrErr"
        sig_start_bit = 25
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err1_NoErr': 0, 'Err1_Err': 1}
        compute_method = None
        length = 1
        startbit = 25
        byte = 3
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class AmbIllmnFwdStsChks:
        sig_name = "AmbIllmnFwdStsChks"
        sig_start_bit = 48
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 48
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SolarSnsrRiValue:
        sig_name = "SolarSnsrRiValue"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 5
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class AmbIllmnFwdStsAmbIllmn2:
        sig_name = "AmbIllmnFwdStsAmbIllmn2"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 40
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RelHumSnsrRelHum:
        sig_name = "RelHumSnsrRelHum"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.5
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 200
        sig_byteorder = "Intel"
        sig_value_init = 80
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class AmbIllmnFwdStsAmbIllmn1:
        sig_name = "AmbIllmnFwdStsAmbIllmn1"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 31
        bmuws_info = [(3, 0b10000000, 0b01111111, 1, 7), (4, 0b11111111, 0b00000000, 8, 0)]

    class RelHumSnsrErr:
        sig_name = "RelHumSnsrErr"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err1_NoErr': 0, 'Err1_Err': 1}
        compute_method = None
        length = 1
        startbit = 24
        byte = 3
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0


class LCULLCUL_LIN1Fr01:
    msg_name = "LCULLCUL_LIN1Fr01"
    msg_id = 3
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "LCUL"
    rx_nodes = ['MMD', 'RLMM', 'HOD']
    sig_group_dict = {'SeatOccpSts': ['SeatOccpStsDrvrSeatSts', 'SeatOccpStsPassSeatSts', 'SeatOccpStsSecRowLeSeatSts', 'SeatOccpStsSecRowMidSeatSts', 'SeatOccpStsSecRowRiSeatSts', 'SeatOccpStsThrdRowLeSeatSts', 'SeatOccpStsThrdRowMidSeatSts', 'SeatOccpStsThrdRowRiSeatSts'], 'Odometer': ['OdometerValidity', 'OdometerValue'], 'SeatMassgActReLe': ['SeatMassgActReLeMassgProg', 'SeatMassgActReLeReqLvl'], 'SeatMassgActFrntLe': ['SeatMassgActFrntLeMassgProg', 'SeatMassgActFrntLeReqLvl']}
    sig_group_dataid_dict = {}

    class SeatOccpStsThrdRowRiSeatSts:
        sig_name = "SeatOccpStsThrdRowRiSeatSts"
        sig_start_bit = 55
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 55
        byte = 6
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class SeatOccpStsSecRowRiSeatSts:
        sig_name = "SeatOccpStsSecRowRiSeatSts"
        sig_start_bit = 52
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class SeatOccpStsDrvrSeatSts:
        sig_name = "SeatOccpStsDrvrSeatSts"
        sig_start_bit = 48
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 48
        byte = 6
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class SeatOccpStsThrdRowMidSeatSts:
        sig_name = "SeatOccpStsThrdRowMidSeatSts"
        sig_start_bit = 54
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 54
        byte = 6
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VehBattU:
        sig_name = "VehBattU"
        sig_start_bit = 38
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.02
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1022
        sig_byteorder = "Intel"
        sig_value_init = 1023
        sig_value_type = "SCALE_LINEAR_AND_TEXTTABLE"
        sig_value_table = {'BattU2_BMSVolWakeUpThd': 1023}
        compute_method = None
        length = 10
        startbit = 38
        bmuws_info = [(4, 0b11000000, 0b00111111, 2, 6), (5, 0b11111111, 0b00000000, 8, 0)]

    class SeatMassgActReLeReqLvl:
        sig_name = "SeatMassgActReLeReqLvl"
        sig_start_bit = 36
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ReqLvl_NoReq': 0, 'ReqLvl_LoReq': 1, 'ReqLvl_MidReq': 2, 'ReqLvl_HiReq': 3}
        compute_method = None
        length = 2
        startbit = 36
        byte = 4
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class SeatOccpStsThrdRowLeSeatSts:
        sig_name = "SeatOccpStsThrdRowLeSeatSts"
        sig_start_bit = 53
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 53
        byte = 6
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class SeatMassgActFrntLeMassgProg:
        sig_name = "SeatMassgActFrntLeMassgProg"
        sig_start_bit = 28
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'MassgProg_Prog0': 0, 'MassgProg_Prog1': 1, 'MassgProg_Prog2': 2, 'MassgProg_Prog3': 3, 'MassgProg_Prog4': 4, 'MassgProg_Prog5': 5, 'MassgProg_Prog6': 6, 'MassgProg_Prog7': 7}
        compute_method = None
        length = 3
        startbit = 28
        byte = 3
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class OdometerValue:
        sig_name = "OdometerValue"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 21
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 21
        startbit = 0
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0), (2, 0b00011111, 0b11100000, 5, 0)]

    class SeatLumActReLe:
        sig_name = "SeatLumActReLe"
        sig_start_bit = 25
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SeatDir_Idle': 0, 'SeatDir_Up_Fwd_ReleaseOn': 1, 'SeatDir_Dwn_Backw_ReleaseOff': 2, 'SeatDir_Fault': 3, 'SeatDir_Reserved2': 4, 'SeatDir_Reserved3': 5, 'SeatDir_Reserved4': 6, 'SeatDir_Reserved5': 7}
        compute_method = None
        length = 3
        startbit = 25
        byte = 3
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class SeatOccpStsSecRowLeSeatSts:
        sig_name = "SeatOccpStsSecRowLeSeatSts"
        sig_start_bit = 50
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 50
        byte = 6
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class SeatMassgActFrntLeReqLvl:
        sig_name = "SeatMassgActFrntLeReqLvl"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ReqLvl_NoReq': 0, 'ReqLvl_LoReq': 1, 'ReqLvl_MidReq': 2, 'ReqLvl_HiReq': 3}
        compute_method = None
        length = 2
        startbit = 31
        bmuws_info = [(3, 0b10000000, 0b01111111, 1, 7), (4, 0b00000001, 0b11111110, 1, 0)]

    class SeatOccpStsSecRowMidSeatSts:
        sig_name = "SeatOccpStsSecRowMidSeatSts"
        sig_start_bit = 51
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 51
        byte = 6
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class SeatMassgActReLeMassgProg:
        sig_name = "SeatMassgActReLeMassgProg"
        sig_start_bit = 33
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'MassgProg_Prog0': 0, 'MassgProg_Prog1': 1, 'MassgProg_Prog2': 2, 'MassgProg_Prog3': 3, 'MassgProg_Prog4': 4, 'MassgProg_Prog5': 5, 'MassgProg_Prog6': 6, 'MassgProg_Prog7': 7}
        compute_method = None
        length = 3
        startbit = 33
        byte = 4
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class SeatLumActFrntLe:
        sig_name = "SeatLumActFrntLe"
        sig_start_bit = 22
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SeatDir_Idle': 0, 'SeatDir_Up_Fwd_ReleaseOn': 1, 'SeatDir_Dwn_Backw_ReleaseOff': 2, 'SeatDir_Fault': 3, 'SeatDir_Reserved2': 4, 'SeatDir_Reserved3': 5, 'SeatDir_Reserved4': 6, 'SeatDir_Reserved5': 7}
        compute_method = None
        length = 3
        startbit = 22
        bmuws_info = [(2, 0b11000000, 0b00111111, 2, 6), (3, 0b00000001, 0b11111110, 1, 0)]

    class OdometerValidity:
        sig_name = "OdometerValidity"
        sig_start_bit = 21
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Validity_NotValid': 0, 'Validity_Valid': 1}
        compute_method = None
        length = 1
        startbit = 21
        byte = 2
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class SeatOccpStsPassSeatSts:
        sig_name = "SeatOccpStsPassSeatSts"
        sig_start_bit = 49
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
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


class WMMLCUL_LIN1Fr01:
    msg_name = "WMMLCUL_LIN1Fr01"
    msg_id = 21
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "WMM"
    rx_nodes = ['LCUL', 'RLSM']
    sig_group_dict = {'WiprMotDiagc': ['WiprMotDiagcWiprMotHiVltDetd', 'WiprMotDiagcWiprMotLoVltDetd', 'WiprMotDiagcWiprMotOvldDetd']}
    sig_group_dataid_dict = {}

    class WiprInPrkgPosnLo:
        sig_name = "WiprInPrkgPosnLo"
        sig_start_bit = 27
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
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

    class WshngCycActv:
        sig_name = "WshngCycActv"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 15
        byte = 1
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class WiprInPosnForSrv:
        sig_name = "WiprInPosnForSrv"
        sig_start_bit = 26
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 26
        byte = 3
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class WiprMotErrSafe:
        sig_name = "WiprMotErrSafe"
        sig_start_bit = 13
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OffOnInvld_Invalid1': 0, 'OffOnInvld_Off': 1, 'OffOnInvld_On': 2, 'OffOnInvld_Invalid2': 3}
        compute_method = None
        length = 2
        startbit = 13
        byte = 1
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class WiprActv:
        sig_name = "WiprActv"
        sig_start_bit = 25
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 25
        byte = 3
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class WiprInWipgAr:
        sig_name = "WiprInWipgAr"
        sig_start_bit = 28
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
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

    class WiprMotDiagcWiprMotHiVltDetd:
        sig_name = "WiprMotDiagcWiprMotHiVltDetd"
        sig_start_bit = 41
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffCrit1_NotVld1': 0, 'OnOffCrit1_Off': 1, 'OnOffCrit1_On': 2, 'OnOffCrit1_NotVld2': 3}
        compute_method = None
        length = 2
        startbit = 41
        byte = 5
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class IRawWMM:
        sig_name = "IRawWMM"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = -400
        sig_value_min = 0
        sig_value_max = 8000
        sig_byteorder = "Intel"
        sig_value_init = 4000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 0
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b00011111, 0b11100000, 5, 0)]

    class URawWMM:
        sig_name = "URawWMM"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 9
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 16
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b00000001, 0b11111110, 1, 0)]

    class WiprMotCrkAg:
        sig_name = "WiprMotCrkAg"
        sig_start_bit = 32
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 32
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class WiprMotDiagcWiprMotOvldDetd:
        sig_name = "WiprMotDiagcWiprMotOvldDetd"
        sig_start_bit = 45
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffCrit1_NotVld1': 0, 'OnOffCrit1_Off': 1, 'OnOffCrit1_On': 2, 'OnOffCrit1_NotVld2': 3}
        compute_method = None
        length = 2
        startbit = 45
        byte = 5
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class WiprMotDiagcWiprMotLoVltDetd:
        sig_name = "WiprMotDiagcWiprMotLoVltDetd"
        sig_start_bit = 43
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffCrit1_NotVld1': 0, 'OnOffCrit1_Off': 1, 'OnOffCrit1_On': 2, 'OnOffCrit1_NotVld2': 3}
        compute_method = None
        length = 2
        startbit = 43
        byte = 5
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3


class LCULLCUL_LIN1Fr04:
    msg_name = "LCULLCUL_LIN1Fr04"
    msg_id = 6
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "LCUL"
    rx_nodes = ['WMM', 'RLMM', 'HOD']
    sig_group_dict = {'VMMGlbSig': ['VMMGlbSigCarModSts', 'VMMGlbSigChks', 'VMMGlbSigCntr', 'VMMGlbSigCnvincSubSts1', 'VMMGlbSigDrvgSubSts1', 'VMMGlbSigInactvSubSts1', 'VMMGlbSigLoBattModSts', 'VMMGlbSigUsgModSts']}
    sig_group_dataid_dict = {'VMMGlbSig': 1074}

    class VMMGlbSigCnvincSubSts1:
        sig_name = "VMMGlbSigCnvincSubSts1"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CnvincSubSts_Invalid': 0, 'CnvincSubSts_EnterExit': 1, 'CnvincSubSts_AllDoorClosed': 2}
        compute_method = None
        length = 8
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VMMGlbSigLoBattModSts:
        sig_name = "VMMGlbSigLoBattModSts"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
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

    class VMMGlbSigInactvSubSts1:
        sig_name = "VMMGlbSigInactvSubSts1"
        sig_start_bit = 32
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'InactvSubSts_Invalid': 0, 'InactvSubSts_Awake': 1, 'InactvSubSts_UserPresent': 2}
        compute_method = None
        length = 8
        startbit = 32
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VMMGlbSigDrvgSubSts1:
        sig_name = "VMMGlbSigDrvgSubSts1"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DrvgSubSts_Invalid': 0, 'DrvgSubSts_Manual': 1, 'DrvgSubSts_Automatic': 2, 'DrvgSubSts_NoTorque': 3}
        compute_method = None
        length = 8
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VMMGlbSigChks:
        sig_name = "VMMGlbSigChks"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 8
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VMMGlbSigUsgModSts:
        sig_name = "VMMGlbSigUsgModSts"
        sig_start_bit = 41
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 13
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'UsgModSts1_UsgModAbdnd': 0, 'UsgModSts1_UsgModInActv': 1, 'UsgModSts1_UsgModCnvinc': 2, 'UsgModSts1_UsgModDrvg': 13}
        compute_method = None
        length = 4
        startbit = 41
        byte = 5
        mask = 0b00011110
        unmask = 0b11100001
        shift = 1

    class VMMGlbSigCntr:
        sig_name = "VMMGlbSigCntr"
        sig_start_bit = 4
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 4
        byte = 0
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class VMMGlbSigCarModSts:
        sig_name = "VMMGlbSigCarModSts"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 8
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CarModStsType_CarModNorm': 0, 'CarModStsType_CarModTrnsp': 1, 'CarModStsType_CarModFcy': 2, 'CarModStsType_CarModExhib': 3, 'CarModStsType_CarModCrash': 8}
        compute_method = None
        length = 4
        startbit = 0
        byte = 0
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0


class WMMLCUL_LIN1Fr03:
    msg_name = "WMMLCUL_LIN1Fr03"
    msg_id = 23
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "WMM"
    rx_nodes = ['LCUL']
    sig_group_dict = {'WMMSerNo': ['WMMSerNoNr1', 'WMMSerNoNr2', 'WMMSerNoNr3', 'WMMSerNoNr4']}
    sig_group_dataid_dict = {}

    class WMMSerNoNr2:
        sig_name = "WMMSerNoNr2"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 8
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class WMMSerNoNr3:
        sig_name = "WMMSerNoNr3"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class WMMSerNoNr4:
        sig_name = "WMMSerNoNr4"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class WMMSerNoNr1:
        sig_name = "WMMSerNoNr1"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class HODLCUL_LIN1Fr01:
    msg_name = "HODLCUL_LIN1Fr01"
    msg_id = 0
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "HOD"
    rx_nodes = ['LCUL']
    sig_group_dict = {'HandsFreeDetnHOD': ['HandsFreeDetnHODChks', 'HandsFreeDetnHODCntr', 'HandsFreeDetnHODHandsOnSts', 'HandsFreeDetnHODHodErrorSts']}
    sig_group_dataid_dict = {}

    class HandsFreeDetnHODHodErrorSts:
        sig_name = "HandsFreeDetnHODHodErrorSts"
        sig_start_bit = 14
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HodErrorSts_Init': 0, 'HodErrorSts_Reserved1': 1, 'HodErrorSts_Ready': 2, 'HodErrorSts_CUFault': 3, 'HodErrorSts_SMFault': 4, 'HodErrorSts_SVFault': 5, 'HodErrorSts_Reserved2': 6, 'HodErrorSts_Reserved3': 7}
        compute_method = None
        length = 3
        startbit = 14
        bmuws_info = [(1, 0b11000000, 0b00111111, 2, 6), (2, 0b00000001, 0b11111110, 1, 0)]

    class HandsFreeDetnHODChks:
        sig_name = "HandsFreeDetnHODChks"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HandsFreeDetnHODHandsOnSts:
        sig_name = "HandsFreeDetnHODHandsOnSts"
        sig_start_bit = 12
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HandsOnSts_Init': 0, 'HandsOnSts_HandsON': 1, 'HandsOnSts_HandsOFF': 2, 'HandsOnSts_Undetermined': 3}
        compute_method = None
        length = 2
        startbit = 12
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class HandsFreeDetnHODCntr:
        sig_name = "HandsFreeDetnHODCntr"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 8
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0


class RLSMLCUL_LIN1Fr03:
    msg_name = "RLSMLCUL_LIN1Fr03"
    msg_id = 18
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "RLSM"
    rx_nodes = ['LCUL']
    sig_group_dict = {'RLSMPartNo': ['RLSMPartNoEndSgn1', 'RLSMPartNoEndSgn2', 'RLSMPartNoEndSgn3', 'RLSMPartNoNr1', 'RLSMPartNoNr2', 'RLSMPartNoNr3', 'RLSMPartNoNr4', 'RLSMPartNoNr5']}
    sig_group_dataid_dict = {}

    class RLSMPartNoNr2:
        sig_name = "RLSMPartNoNr2"
        sig_start_bit = 32
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 32
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RLSMPartNoNr1:
        sig_name = "RLSMPartNoNr1"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RLSMPartNoNr5:
        sig_name = "RLSMPartNoNr5"
        sig_start_bit = 56
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 56
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RLSMPartNoEndSgn1:
        sig_name = "RLSMPartNoEndSgn1"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RLSMPartNoNr3:
        sig_name = "RLSMPartNoNr3"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 40
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RLSMPartNoEndSgn3:
        sig_name = "RLSMPartNoEndSgn3"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RLSMPartNoEndSgn2:
        sig_name = "RLSMPartNoEndSgn2"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 8
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RLSMPartNoNr4:
        sig_name = "RLSMPartNoNr4"
        sig_start_bit = 48
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 48
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class LCULLCUL_LIN1Fr06:
    msg_name = "LCULLCUL_LIN1Fr06"
    msg_id = 8
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "LCUL"
    rx_nodes = ['RLSM', 'WMM', 'HOD']
    sig_group_dict = {'VehSpd': ['VehSpdChks', 'VehSpdCntr', 'VehSpdQf', 'VehSpdSpd']}
    sig_group_dataid_dict = {'VehSpd': 1043}

    class FRDoorOpenClsSts:
        sig_name = "FRDoorOpenClsSts"
        sig_start_bit = 34
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorSts_Unknow': 0, 'DoorSts_Open': 1, 'DoorSts_Close': 2}
        compute_method = None
        length = 2
        startbit = 34
        byte = 4
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VehSpdCntr:
        sig_name = "VehSpdCntr"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 8
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class VehSpdSpd:
        sig_name = "VehSpdSpd"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 0.00391
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 31970
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 16
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b01111111, 0b10000000, 7, 0)]

    class FLDoorOpenClsSts:
        sig_name = "FLDoorOpenClsSts"
        sig_start_bit = 32
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorSts_Unknow': 0, 'DoorSts_Open': 1, 'DoorSts_Close': 2}
        compute_method = None
        length = 2
        startbit = 32
        byte = 4
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VehSpdQf:
        sig_name = "VehSpdQf"
        sig_start_bit = 12
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 12
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class VehSpdChks:
        sig_name = "VehSpdChks"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class LCULLCUL_LIN1Fr05:
    msg_name = "LCULLCUL_LIN1Fr05"
    msg_id = 7
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "LCUL"
    rx_nodes = ['WMM', 'RLSM']
    sig_group_dict = {'WindCorrnVal': ['WindCorrnValAmb', 'WindCorrnValFrnt', 'WindCorrnValHud'], 'AmbTEstimd': ['AmbTEstimdT', 'AmbTEstimdTQF']}
    sig_group_dataid_dict = {}

    class FrntWiperMode:
        sig_name = "FrntWiperMode"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 9
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FrntWiperMode_OFF': 0, 'FrntWiperMode_SingleScrape': 1, 'FrntWiperMode_Interval1': 2, 'FrntWiperMode_Interval2': 3, 'FrntWiperMode_IntervalReserve': 4, 'FrntWiperMode_ContinuousLow': 5, 'FrntWiperMode_ContinuousHigh': 6, 'FrntWiperMode_Auto': 7, 'FrntWiperMode_Maintenance': 8, 'FrntWiperMode_Reserve': 9}
        compute_method = None
        length = 4
        startbit = 40
        byte = 5
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class WindCorrnValAmb:
        sig_name = "WindCorrnValAmb"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntWiperSingleScrape:
        sig_name = "FrntWiperSingleScrape"
        sig_start_bit = 38
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
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

    class WindCorrnValHud:
        sig_name = "WindCorrnValHud"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class WindCorrnValFrnt:
        sig_name = "WindCorrnValFrnt"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 8
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class AmbTEstimdT:
        sig_name = "AmbTEstimdT"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = -256
        sig_value_min = 0
        sig_value_max = 5119
        sig_byteorder = "Intel"
        sig_value_init = 2560
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 24
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b00011111, 0b11100000, 5, 0)]

    class AmbTEstimdTQF:
        sig_name = "AmbTEstimdTQF"
        sig_start_bit = 37
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HVACTempQf_SnsrDataNotOk': 0, 'HVACTempQf_SnsrDataOk': 1}
        compute_method = None
        length = 1
        startbit = 37
        byte = 4
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5


class HODLCUL_LIN1Fr03:
    msg_name = "HODLCUL_LIN1Fr03"
    msg_id = 2
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "HOD"
    rx_nodes = ['LCUL']
    sig_group_dict = {'HODSerNo': ['HODSerNoNr1', 'HODSerNoNr2', 'HODSerNoNr3', 'HODSerNoNr4']}
    sig_group_dataid_dict = {}

    class HODSerNoNr4:
        sig_name = "HODSerNoNr4"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HODSerNoNr1:
        sig_name = "HODSerNoNr1"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HODSerNoNr2:
        sig_name = "HODSerNoNr2"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 8
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HODSerNoNr3:
        sig_name = "HODSerNoNr3"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


