lin_scheduleTable = {'LCUL_ALM_LIN2_DiagSchedule01': [(0, 'LCULToALMLCULALMLIN2ReqFrame', 0.015), (1, 'ALMToLCULLCULALMLIN2RespFrame', 0.015)], 'LCUL_ALM_LIN2Schedule01_LCUL_ALM_LIN2': [(0, 'LCULLCUL_ALM_LIN2Fr01', 0.01), (1, 'LCULLCUL_ALM_LIN2Fr03', 0.01), (2, 'LCULLCUL_ALM_LIN2Fr04', 0.01), (3, 'LCULLCUL_ALM_LIN2Fr05', 0.01), (4, 'LCULLCUL_ALM_LIN2Fr06', 0.01), (5, 'LCULLCUL_ALM_LIN2Fr07', 0.01), (6, 'LCULLCUL_ALM_LIN2Fr08', 0.01), (7, 'LCULLCUL_ALM_LIN2Fr09', 0.01), (8, 'LCULLCUL_ALM_LIN2Fr10', 0.01), (9, 'LCULLCUL_ALM_LIN2Fr11', 0.01), (10, 'LCULLCUL_ALM_LIN2Fr12', 0.01)], 'LCUL_ALM_LIN2_ScheduleFailrSts_LCUL_ALM_LIN2': [(0, 'ALMLCULLIN2LCUL_ALM_LIN2Fr02', 0.01), (1, 'ALMLCULLIN2LCUL_ALM_LIN2Fr03', 0.01), (2, 'ALMLCULLIN2LCUL_ALM_LIN2Fr04', 0.01), (3, 'ALMLCULLIN2LCUL_ALM_LIN2Fr05', 0.01), (4, 'ALMLCULLIN2LCUL_ALM_LIN2Fr06', 0.01), (5, 'ALMLCULLIN2LCUL_ALM_LIN2Fr07', 0.01), (6, 'ALMLCULLIN2LCUL_ALM_LIN2Fr08', 0.01), (7, 'ALMLCULLIN2LCUL_ALM_LIN2Fr09', 0.01), (8, 'ALMLCULLIN2LCUL_ALM_LIN2Fr10', 0.01), (9, 'ALMLCULLIN2LCUL_ALM_LIN2Fr11', 0.01)]}


class ALMLCULLIN2LCUL_ALM_LIN2Fr08:
    msg_name = "ALMLCULLIN2LCUL_ALM_LIN2Fr08"
    msg_id = 7
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 1
    tx_node = "ALMLCULLIN2"
    rx_nodes = ['LCUL']
    sig_group_dict = {'LcuLLin2ALM7Failr': ['LcuLLin2ALM7FailrLEDSts', 'LcuLLin2ALM7FailrTmpSts', 'LcuLLin2ALM7FailrVltSts']}
    sig_group_dataid_dict = {}

    class LcuLLin2ALM7FailrTmpSts:
        sig_name = "LcuLLin2ALM7FailrTmpSts"
        sig_start_bit = 1
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 1
        byte = 0
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class LcuLLin2ALM7FailrLEDSts:
        sig_name = "LcuLLin2ALM7FailrLEDSts"
        sig_start_bit = 2
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 2
        byte = 0
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class LcuLLin2ALM7FailrVltSts:
        sig_name = "LcuLLin2ALM7FailrVltSts"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 0
        byte = 0
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0


class LCULLCUL_ALM_LIN2Fr04:
    msg_name = "LCULLCUL_ALM_LIN2Fr04"
    msg_id = 14
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "LCUL"
    rx_nodes = ['ALMLCULLIN2']
    sig_group_dict = {'LcuLLin2ALM2RGBL': ['LcuLLin2ALM2RGBLBlue', 'LcuLLin2ALM2RGBLDayOrNightSts', 'LcuLLin2ALM2RGBLGreen', 'LcuLLin2ALM2RGBLLuminance', 'LcuLLin2ALM2RGBLRed']}
    sig_group_dataid_dict = {}

    class LcuLLin2ALM2RGBLDayOrNightSts:
        sig_name = "LcuLLin2ALM2RGBLDayOrNightSts"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DayOrNightSts_Night': 0, 'DayOrNightSts_Day': 1}
        compute_method = None
        length = 1
        startbit = 8
        byte = 1
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class LcuLLin2ALM2RGBLBlue:
        sig_name = "LcuLLin2ALM2RGBLBlue"
        sig_start_bit = 0
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
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class LcuLLin2ALM2RGBLRed:
        sig_name = "LcuLLin2ALM2RGBLRed"
        sig_start_bit = 24
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
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class LcuLLin2ALM2RGBLGreen:
        sig_name = "LcuLLin2ALM2RGBLGreen"
        sig_start_bit = 16
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
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class LcuLLin2ALM2RGBLLuminance:
        sig_name = "LcuLLin2ALM2RGBLLuminance"
        sig_start_bit = 9
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 9
        byte = 1
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1


class ALMLCULLIN2LCUL_ALM_LIN2Fr06:
    msg_name = "ALMLCULLIN2LCUL_ALM_LIN2Fr06"
    msg_id = 5
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 1
    tx_node = "ALMLCULLIN2"
    rx_nodes = ['LCUL']
    sig_group_dict = {'LcuLLin2ALM5Failr': ['LcuLLin2ALM5FailrLEDSts', 'LcuLLin2ALM5FailrTmpSts', 'LcuLLin2ALM5FailrVltSts']}
    sig_group_dataid_dict = {}

    class LcuLLin2ALM5FailrLEDSts:
        sig_name = "LcuLLin2ALM5FailrLEDSts"
        sig_start_bit = 2
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 2
        byte = 0
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class LcuLLin2ALM5FailrTmpSts:
        sig_name = "LcuLLin2ALM5FailrTmpSts"
        sig_start_bit = 1
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 1
        byte = 0
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class LcuLLin2ALM5FailrVltSts:
        sig_name = "LcuLLin2ALM5FailrVltSts"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 0
        byte = 0
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0


class ALMLCULLIN2LCUL_ALM_LIN2Fr05:
    msg_name = "ALMLCULLIN2LCUL_ALM_LIN2Fr05"
    msg_id = 4
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 1
    tx_node = "ALMLCULLIN2"
    rx_nodes = ['LCUL']
    sig_group_dict = {'LcuLLin2ALM4Failr': ['LcuLLin2ALM4FailrLEDSts', 'LcuLLin2ALM4FailrTmpSts', 'LcuLLin2ALM4FailrVltSts']}
    sig_group_dataid_dict = {}

    class LcuLLin2ALM4FailrLEDSts:
        sig_name = "LcuLLin2ALM4FailrLEDSts"
        sig_start_bit = 2
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 2
        byte = 0
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class LcuLLin2ALM4FailrTmpSts:
        sig_name = "LcuLLin2ALM4FailrTmpSts"
        sig_start_bit = 1
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 1
        byte = 0
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class LcuLLin2ALM4FailrVltSts:
        sig_name = "LcuLLin2ALM4FailrVltSts"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 0
        byte = 0
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0


class LCULLCUL_ALM_LIN2Fr07:
    msg_name = "LCULLCUL_ALM_LIN2Fr07"
    msg_id = 17
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "LCUL"
    rx_nodes = ['ALMLCULLIN2']
    sig_group_dict = {'LcuLLin2ALM5RGBL': ['LcuLLin2ALM5RGBLBlue', 'LcuLLin2ALM5RGBLDayOrNightSts', 'LcuLLin2ALM5RGBLGreen', 'LcuLLin2ALM5RGBLLuminance', 'LcuLLin2ALM5RGBLRed']}
    sig_group_dataid_dict = {}

    class LcuLLin2ALM5RGBLDayOrNightSts:
        sig_name = "LcuLLin2ALM5RGBLDayOrNightSts"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DayOrNightSts_Night': 0, 'DayOrNightSts_Day': 1}
        compute_method = None
        length = 1
        startbit = 8
        byte = 1
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class LcuLLin2ALM5RGBLRed:
        sig_name = "LcuLLin2ALM5RGBLRed"
        sig_start_bit = 24
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
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class LcuLLin2ALM5RGBLLuminance:
        sig_name = "LcuLLin2ALM5RGBLLuminance"
        sig_start_bit = 9
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 9
        byte = 1
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class LcuLLin2ALM5RGBLGreen:
        sig_name = "LcuLLin2ALM5RGBLGreen"
        sig_start_bit = 16
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
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class LcuLLin2ALM5RGBLBlue:
        sig_name = "LcuLLin2ALM5RGBLBlue"
        sig_start_bit = 0
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
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class LCULLCUL_ALM_LIN2Fr12:
    msg_name = "LCULLCUL_ALM_LIN2Fr12"
    msg_id = 22
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "LCUL"
    rx_nodes = ['ALMLCULLIN2']
    sig_group_dict = {'LcuLLin2ALM10RGBL': ['LcuLLin2ALM10RGBLBlue', 'LcuLLin2ALM10RGBLDayOrNightSts', 'LcuLLin2ALM10RGBLGreen', 'LcuLLin2ALM10RGBLLuminance', 'LcuLLin2ALM10RGBLRed']}
    sig_group_dataid_dict = {}

    class LcuLLin2ALM10RGBLDayOrNightSts:
        sig_name = "LcuLLin2ALM10RGBLDayOrNightSts"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DayOrNightSts_Night': 0, 'DayOrNightSts_Day': 1}
        compute_method = None
        length = 1
        startbit = 8
        byte = 1
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class LcuLLin2ALM10RGBLLuminance:
        sig_name = "LcuLLin2ALM10RGBLLuminance"
        sig_start_bit = 9
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 9
        byte = 1
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class LcuLLin2ALM10RGBLRed:
        sig_name = "LcuLLin2ALM10RGBLRed"
        sig_start_bit = 24
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
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class LcuLLin2ALM10RGBLGreen:
        sig_name = "LcuLLin2ALM10RGBLGreen"
        sig_start_bit = 16
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
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class LcuLLin2ALM10RGBLBlue:
        sig_name = "LcuLLin2ALM10RGBLBlue"
        sig_start_bit = 0
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
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class LCULLCUL_ALM_LIN2Fr05:
    msg_name = "LCULLCUL_ALM_LIN2Fr05"
    msg_id = 15
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "LCUL"
    rx_nodes = ['ALMLCULLIN2']
    sig_group_dict = {'LcuLLin2ALM3RGBL': ['LcuLLin2ALM3RGBLBlue', 'LcuLLin2ALM3RGBLDayOrNightSts', 'LcuLLin2ALM3RGBLGreen', 'LcuLLin2ALM3RGBLLuminance', 'LcuLLin2ALM3RGBLRed']}
    sig_group_dataid_dict = {}

    class LcuLLin2ALM3RGBLBlue:
        sig_name = "LcuLLin2ALM3RGBLBlue"
        sig_start_bit = 0
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
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class LcuLLin2ALM3RGBLDayOrNightSts:
        sig_name = "LcuLLin2ALM3RGBLDayOrNightSts"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DayOrNightSts_Night': 0, 'DayOrNightSts_Day': 1}
        compute_method = None
        length = 1
        startbit = 8
        byte = 1
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class LcuLLin2ALM3RGBLRed:
        sig_name = "LcuLLin2ALM3RGBLRed"
        sig_start_bit = 24
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
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class LcuLLin2ALM3RGBLGreen:
        sig_name = "LcuLLin2ALM3RGBLGreen"
        sig_start_bit = 16
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
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class LcuLLin2ALM3RGBLLuminance:
        sig_name = "LcuLLin2ALM3RGBLLuminance"
        sig_start_bit = 9
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 9
        byte = 1
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1


class ALMLCULLIN2LCUL_ALM_LIN2Fr10:
    msg_name = "ALMLCULLIN2LCUL_ALM_LIN2Fr10"
    msg_id = 9
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 1
    tx_node = "ALMLCULLIN2"
    rx_nodes = ['LCUL']
    sig_group_dict = {'LcuLLin2ALM9Failr': ['LcuLLin2ALM9FailrLEDSts', 'LcuLLin2ALM9FailrTmpSts', 'LcuLLin2ALM9FailrVltSts']}
    sig_group_dataid_dict = {}

    class LcuLLin2ALM9FailrTmpSts:
        sig_name = "LcuLLin2ALM9FailrTmpSts"
        sig_start_bit = 1
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 1
        byte = 0
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class LcuLLin2ALM9FailrLEDSts:
        sig_name = "LcuLLin2ALM9FailrLEDSts"
        sig_start_bit = 2
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 2
        byte = 0
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class LcuLLin2ALM9FailrVltSts:
        sig_name = "LcuLLin2ALM9FailrVltSts"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 0
        byte = 0
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0


class ALMLCULLIN2LCUL_ALM_LIN2Fr11:
    msg_name = "ALMLCULLIN2LCUL_ALM_LIN2Fr11"
    msg_id = 10
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 1
    tx_node = "ALMLCULLIN2"
    rx_nodes = ['LCUL']
    sig_group_dict = {'LcuLLin2ALM10Failr': ['LcuLLin2ALM10FailrLEDSts', 'LcuLLin2ALM10FailrTmpSts', 'LcuLLin2ALM10FailrVltSts']}
    sig_group_dataid_dict = {}

    class LcuLLin2ALM10FailrVltSts:
        sig_name = "LcuLLin2ALM10FailrVltSts"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 0
        byte = 0
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class LcuLLin2ALM10FailrLEDSts:
        sig_name = "LcuLLin2ALM10FailrLEDSts"
        sig_start_bit = 2
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 2
        byte = 0
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class LcuLLin2ALM10FailrTmpSts:
        sig_name = "LcuLLin2ALM10FailrTmpSts"
        sig_start_bit = 1
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 1
        byte = 0
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1


class ALMLCULLIN2LCUL_ALM_LIN2Fr09:
    msg_name = "ALMLCULLIN2LCUL_ALM_LIN2Fr09"
    msg_id = 8
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 1
    tx_node = "ALMLCULLIN2"
    rx_nodes = ['LCUL']
    sig_group_dict = {'LcuLLin2ALM8Failr': ['LcuLLin2ALM8FailrLEDSts', 'LcuLLin2ALM8FailrTmpSts', 'LcuLLin2ALM8FailrVltSts']}
    sig_group_dataid_dict = {}

    class LcuLLin2ALM8FailrVltSts:
        sig_name = "LcuLLin2ALM8FailrVltSts"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 0
        byte = 0
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class LcuLLin2ALM8FailrTmpSts:
        sig_name = "LcuLLin2ALM8FailrTmpSts"
        sig_start_bit = 1
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 1
        byte = 0
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class LcuLLin2ALM8FailrLEDSts:
        sig_name = "LcuLLin2ALM8FailrLEDSts"
        sig_start_bit = 2
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 2
        byte = 0
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2


class ALMLCULLIN2LCUL_ALM_LIN2Fr04:
    msg_name = "ALMLCULLIN2LCUL_ALM_LIN2Fr04"
    msg_id = 3
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 1
    tx_node = "ALMLCULLIN2"
    rx_nodes = ['LCUL']
    sig_group_dict = {'LcuLLin2ALM3Failr': ['LcuLLin2ALM3FailrLEDSts', 'LcuLLin2ALM3FailrTmpSts', 'LcuLLin2ALM3FailrVltSts']}
    sig_group_dataid_dict = {}

    class LcuLLin2ALM3FailrVltSts:
        sig_name = "LcuLLin2ALM3FailrVltSts"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 0
        byte = 0
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class LcuLLin2ALM3FailrTmpSts:
        sig_name = "LcuLLin2ALM3FailrTmpSts"
        sig_start_bit = 1
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 1
        byte = 0
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class LcuLLin2ALM3FailrLEDSts:
        sig_name = "LcuLLin2ALM3FailrLEDSts"
        sig_start_bit = 2
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 2
        byte = 0
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2


class LCULLCUL_ALM_LIN2Fr10:
    msg_name = "LCULLCUL_ALM_LIN2Fr10"
    msg_id = 20
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "LCUL"
    rx_nodes = ['ALMLCULLIN2']
    sig_group_dict = {'LcuLLin2ALM8RGBL': ['LcuLLin2ALM8RGBLBlue', 'LcuLLin2ALM8RGBLDayOrNightSts', 'LcuLLin2ALM8RGBLGreen', 'LcuLLin2ALM8RGBLLuminance', 'LcuLLin2ALM8RGBLRed']}
    sig_group_dataid_dict = {}

    class LcuLLin2ALM8RGBLLuminance:
        sig_name = "LcuLLin2ALM8RGBLLuminance"
        sig_start_bit = 9
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 9
        byte = 1
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class LcuLLin2ALM8RGBLBlue:
        sig_name = "LcuLLin2ALM8RGBLBlue"
        sig_start_bit = 0
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
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class LcuLLin2ALM8RGBLDayOrNightSts:
        sig_name = "LcuLLin2ALM8RGBLDayOrNightSts"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DayOrNightSts_Night': 0, 'DayOrNightSts_Day': 1}
        compute_method = None
        length = 1
        startbit = 8
        byte = 1
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class LcuLLin2ALM8RGBLGreen:
        sig_name = "LcuLLin2ALM8RGBLGreen"
        sig_start_bit = 16
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
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class LcuLLin2ALM8RGBLRed:
        sig_name = "LcuLLin2ALM8RGBLRed"
        sig_start_bit = 24
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
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class LCULLCUL_ALM_LIN2Fr03:
    msg_name = "LCULLCUL_ALM_LIN2Fr03"
    msg_id = 13
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "LCUL"
    rx_nodes = ['ALMLCULLIN2']
    sig_group_dict = {'LcuLLin2ALM1RGBL': ['LcuLLin2ALM1RGBLBlue', 'LcuLLin2ALM1RGBLDayOrNightSts', 'LcuLLin2ALM1RGBLGreen', 'LcuLLin2ALM1RGBLLuminance', 'LcuLLin2ALM1RGBLRed']}
    sig_group_dataid_dict = {}

    class LcuLLin2ALM1RGBLRed:
        sig_name = "LcuLLin2ALM1RGBLRed"
        sig_start_bit = 24
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
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class LcuLLin2ALM1RGBLBlue:
        sig_name = "LcuLLin2ALM1RGBLBlue"
        sig_start_bit = 0
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
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class LcuLLin2ALM1RGBLDayOrNightSts:
        sig_name = "LcuLLin2ALM1RGBLDayOrNightSts"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DayOrNightSts_Night': 0, 'DayOrNightSts_Day': 1}
        compute_method = None
        length = 1
        startbit = 8
        byte = 1
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class LcuLLin2ALM1RGBLLuminance:
        sig_name = "LcuLLin2ALM1RGBLLuminance"
        sig_start_bit = 9
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 9
        byte = 1
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class LcuLLin2ALM1RGBLGreen:
        sig_name = "LcuLLin2ALM1RGBLGreen"
        sig_start_bit = 16
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
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class LCULLCUL_ALM_LIN2Fr09:
    msg_name = "LCULLCUL_ALM_LIN2Fr09"
    msg_id = 19
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "LCUL"
    rx_nodes = ['ALMLCULLIN2']
    sig_group_dict = {'LcuLLin2ALM7RGBL': ['LcuLLin2ALM7RGBLBlue', 'LcuLLin2ALM7RGBLDayOrNightSts', 'LcuLLin2ALM7RGBLGreen', 'LcuLLin2ALM7RGBLLuminance', 'LcuLLin2ALM7RGBLRed']}
    sig_group_dataid_dict = {}

    class LcuLLin2ALM7RGBLLuminance:
        sig_name = "LcuLLin2ALM7RGBLLuminance"
        sig_start_bit = 9
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 9
        byte = 1
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class LcuLLin2ALM7RGBLBlue:
        sig_name = "LcuLLin2ALM7RGBLBlue"
        sig_start_bit = 0
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
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class LcuLLin2ALM7RGBLRed:
        sig_name = "LcuLLin2ALM7RGBLRed"
        sig_start_bit = 24
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
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class LcuLLin2ALM7RGBLGreen:
        sig_name = "LcuLLin2ALM7RGBLGreen"
        sig_start_bit = 16
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
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class LcuLLin2ALM7RGBLDayOrNightSts:
        sig_name = "LcuLLin2ALM7RGBLDayOrNightSts"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DayOrNightSts_Night': 0, 'DayOrNightSts_Day': 1}
        compute_method = None
        length = 1
        startbit = 8
        byte = 1
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0


class ALMToLCULLCULALMLIN2RespFrame:
    msg_name = "ALMToLCULLCULALMLIN2RespFrame"
    msg_id = 61
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "ALMLCULLIN2"
    rx_nodes = ['LCUL']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class ALMLCULLIN2LCUL_ALM_LIN2Fr07:
    msg_name = "ALMLCULLIN2LCUL_ALM_LIN2Fr07"
    msg_id = 6
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 1
    tx_node = "ALMLCULLIN2"
    rx_nodes = ['LCUL']
    sig_group_dict = {'LcuLLin2ALM6Failr': ['LcuLLin2ALM6FailrLEDSts', 'LcuLLin2ALM6FailrTmpSts', 'LcuLLin2ALM6FailrVltSts']}
    sig_group_dataid_dict = {}

    class LcuLLin2ALM6FailrTmpSts:
        sig_name = "LcuLLin2ALM6FailrTmpSts"
        sig_start_bit = 1
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 1
        byte = 0
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class LcuLLin2ALM6FailrVltSts:
        sig_name = "LcuLLin2ALM6FailrVltSts"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 0
        byte = 0
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class LcuLLin2ALM6FailrLEDSts:
        sig_name = "LcuLLin2ALM6FailrLEDSts"
        sig_start_bit = 2
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 2
        byte = 0
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2


class LCULToALMLCULALMLIN2ReqFrame:
    msg_name = "LCULToALMLCULALMLIN2ReqFrame"
    msg_id = 60
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "LCUL"
    rx_nodes = ['ALMLCULLIN2']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class ALMLCULLIN2LCUL_ALM_LIN2Fr02:
    msg_name = "ALMLCULLIN2LCUL_ALM_LIN2Fr02"
    msg_id = 1
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 1
    tx_node = "ALMLCULLIN2"
    rx_nodes = ['LCUL']
    sig_group_dict = {'LcuLLin2ALM1Failr': ['LcuLLin2ALM1FailrLEDSts', 'LcuLLin2ALM1FailrTmpSts', 'LcuLLin2ALM1FailrVltSts']}
    sig_group_dataid_dict = {}

    class LcuLLin2ALM1FailrTmpSts:
        sig_name = "LcuLLin2ALM1FailrTmpSts"
        sig_start_bit = 1
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 1
        byte = 0
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class LcuLLin2ALM1FailrLEDSts:
        sig_name = "LcuLLin2ALM1FailrLEDSts"
        sig_start_bit = 2
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 2
        byte = 0
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class LcuLLin2ALM1FailrVltSts:
        sig_name = "LcuLLin2ALM1FailrVltSts"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 0
        byte = 0
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0


class ALMLCULLIN2LCUL_ALM_LIN2Fr03:
    msg_name = "ALMLCULLIN2LCUL_ALM_LIN2Fr03"
    msg_id = 2
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 1
    tx_node = "ALMLCULLIN2"
    rx_nodes = ['LCUL']
    sig_group_dict = {'LcuLLin2ALM2Failr': ['LcuLLin2ALM2FailrLEDSts', 'LcuLLin2ALM2FailrTmpSts', 'LcuLLin2ALM2FailrVltSts']}
    sig_group_dataid_dict = {}

    class LcuLLin2ALM2FailrVltSts:
        sig_name = "LcuLLin2ALM2FailrVltSts"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 0
        byte = 0
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class LcuLLin2ALM2FailrTmpSts:
        sig_name = "LcuLLin2ALM2FailrTmpSts"
        sig_start_bit = 1
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 1
        byte = 0
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class LcuLLin2ALM2FailrLEDSts:
        sig_name = "LcuLLin2ALM2FailrLEDSts"
        sig_start_bit = 2
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 2
        byte = 0
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2


class LCULLCUL_ALM_LIN2Fr11:
    msg_name = "LCULLCUL_ALM_LIN2Fr11"
    msg_id = 21
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "LCUL"
    rx_nodes = ['ALMLCULLIN2']
    sig_group_dict = {'LcuLLin2ALM9RGBL': ['LcuLLin2ALM9RGBLBlue', 'LcuLLin2ALM9RGBLDayOrNightSts', 'LcuLLin2ALM9RGBLGreen', 'LcuLLin2ALM9RGBLLuminance', 'LcuLLin2ALM9RGBLRed']}
    sig_group_dataid_dict = {}

    class LcuLLin2ALM9RGBLRed:
        sig_name = "LcuLLin2ALM9RGBLRed"
        sig_start_bit = 24
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
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class LcuLLin2ALM9RGBLGreen:
        sig_name = "LcuLLin2ALM9RGBLGreen"
        sig_start_bit = 16
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
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class LcuLLin2ALM9RGBLBlue:
        sig_name = "LcuLLin2ALM9RGBLBlue"
        sig_start_bit = 0
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
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class LcuLLin2ALM9RGBLDayOrNightSts:
        sig_name = "LcuLLin2ALM9RGBLDayOrNightSts"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DayOrNightSts_Night': 0, 'DayOrNightSts_Day': 1}
        compute_method = None
        length = 1
        startbit = 8
        byte = 1
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class LcuLLin2ALM9RGBLLuminance:
        sig_name = "LcuLLin2ALM9RGBLLuminance"
        sig_start_bit = 9
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 9
        byte = 1
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1


class LCULLCUL_ALM_LIN2Fr01:
    msg_name = "LCULLCUL_ALM_LIN2Fr01"
    msg_id = 11
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 1
    tx_node = "LCUL"
    rx_nodes = ['ALMLCULLIN2']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class DayOrNightSts:
        sig_name = "DayOrNightSts"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DayOrNightSts_Night': 0, 'DayOrNightSts_Day': 1}
        compute_method = None
        length = 1
        startbit = 0
        byte = 0
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0


class LCULLCUL_ALM_LIN2Fr06:
    msg_name = "LCULLCUL_ALM_LIN2Fr06"
    msg_id = 16
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "LCUL"
    rx_nodes = ['ALMLCULLIN2']
    sig_group_dict = {'LcuLLin2ALM4RGBL': ['LcuLLin2ALM4RGBLBlue', 'LcuLLin2ALM4RGBLDayOrNightSts', 'LcuLLin2ALM4RGBLGreen', 'LcuLLin2ALM4RGBLLuminance', 'LcuLLin2ALM4RGBLRed']}
    sig_group_dataid_dict = {}

    class LcuLLin2ALM4RGBLBlue:
        sig_name = "LcuLLin2ALM4RGBLBlue"
        sig_start_bit = 0
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
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class LcuLLin2ALM4RGBLRed:
        sig_name = "LcuLLin2ALM4RGBLRed"
        sig_start_bit = 24
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
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class LcuLLin2ALM4RGBLLuminance:
        sig_name = "LcuLLin2ALM4RGBLLuminance"
        sig_start_bit = 9
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 9
        byte = 1
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class LcuLLin2ALM4RGBLDayOrNightSts:
        sig_name = "LcuLLin2ALM4RGBLDayOrNightSts"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DayOrNightSts_Night': 0, 'DayOrNightSts_Day': 1}
        compute_method = None
        length = 1
        startbit = 8
        byte = 1
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class LcuLLin2ALM4RGBLGreen:
        sig_name = "LcuLLin2ALM4RGBLGreen"
        sig_start_bit = 16
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
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class LCULLCUL_ALM_LIN2Fr08:
    msg_name = "LCULLCUL_ALM_LIN2Fr08"
    msg_id = 18
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "LCUL"
    rx_nodes = ['ALMLCULLIN2']
    sig_group_dict = {'LcuLLin2ALM6RGBL': ['LcuLLin2ALM6RGBLBlue', 'LcuLLin2ALM6RGBLDayOrNightSts', 'LcuLLin2ALM6RGBLGreen', 'LcuLLin2ALM6RGBLLuminance', 'LcuLLin2ALM6RGBLRed']}
    sig_group_dataid_dict = {}

    class LcuLLin2ALM6RGBLDayOrNightSts:
        sig_name = "LcuLLin2ALM6RGBLDayOrNightSts"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DayOrNightSts_Night': 0, 'DayOrNightSts_Day': 1}
        compute_method = None
        length = 1
        startbit = 8
        byte = 1
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class LcuLLin2ALM6RGBLRed:
        sig_name = "LcuLLin2ALM6RGBLRed"
        sig_start_bit = 24
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
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class LcuLLin2ALM6RGBLLuminance:
        sig_name = "LcuLLin2ALM6RGBLLuminance"
        sig_start_bit = 9
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 9
        byte = 1
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class LcuLLin2ALM6RGBLGreen:
        sig_name = "LcuLLin2ALM6RGBLGreen"
        sig_start_bit = 16
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
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class LcuLLin2ALM6RGBLBlue:
        sig_name = "LcuLLin2ALM6RGBLBlue"
        sig_start_bit = 0
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
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


