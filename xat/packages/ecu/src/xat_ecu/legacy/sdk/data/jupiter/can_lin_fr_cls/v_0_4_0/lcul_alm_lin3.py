lin_scheduleTable = {'LCUL_ALM_LIN3_ScheduleFailrSts_LCUL_ALM_LIN3': [(0, 'ALMLCULLIN3LCUL_ALM_LIN3Fr02', 0.005), (1, 'ALMLCULLIN3LCUL_ALM_LIN3Fr03', 0.005), (2, 'ALMLCULLIN3LCUL_ALM_LIN3Fr04', 0.005), (3, 'ALMLCULLIN3LCUL_ALM_LIN3Fr05', 0.005), (4, 'ALMLCULLIN3LCUL_ALM_LIN3Fr06', 0.005), (5, 'ALMLCULLIN3LCUL_ALM_LIN3Fr07', 0.005), (6, 'ALMLCULLIN3LCUL_ALM_LIN3Fr08', 0.005), (7, 'ALMLCULLIN3LCUL_ALM_LIN3Fr09', 0.005), (8, 'ALMLCULLIN3LCUL_ALM_LIN3Fr10', 0.005), (9, 'ALMLCULLIN3LCUL_ALM_LIN3Fr11', 0.005)], 'LCUL_ALM_LIN3Schedule01_LCUL_ALM_LIN3': [(0, 'LCULLCUL_ALM_LIN3Fr02', 0.01), (1, 'LCULLCUL_ALM_LIN3Fr03', 0.01), (2, 'LCULLCUL_ALM_LIN3Fr04', 0.01), (3, 'LCULLCUL_ALM_LIN3Fr05', 0.01), (4, 'LCULLCUL_ALM_LIN3Fr06', 0.01), (5, 'LCULLCUL_ALM_LIN3Fr07', 0.01), (6, 'LCULLCUL_ALM_LIN3Fr08', 0.01), (7, 'LCULLCUL_ALM_LIN3Fr09', 0.01), (8, 'LCULLCUL_ALM_LIN3Fr10', 0.01), (9, 'LCULLCUL_ALM_LIN3Fr11', 0.01)], 'LCUL_ALM_LIN3_DiagSchedule01': [(0, 'LCULToALMLCULALMLIN3ReqFrame', 0.015), (1, 'ALMToLCULLCULALMLIN3RespFrame', 0.015)]}


class LCULLCUL_ALM_LIN3Fr07:
    msg_name = "LCULLCUL_ALM_LIN3Fr07"
    msg_id = 17
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "LCUL"
    rx_nodes = ['ALMLCULLIN3']
    sig_group_dict = {'LcuLLin3ALM6RGBL': ['LcuLLin3ALM6RGBLBlue', 'LcuLLin3ALM6RGBLDayOrNightSts', 'LcuLLin3ALM6RGBLGreen', 'LcuLLin3ALM6RGBLLuminance', 'LcuLLin3ALM6RGBLRed']}
    sig_group_dataid_dict = {}

    class LcuLLin3ALM6RGBLGreen:
        sig_name = "LcuLLin3ALM6RGBLGreen"
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

    class LcuLLin3ALM6RGBLBlue:
        sig_name = "LcuLLin3ALM6RGBLBlue"
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

    class LcuLLin3ALM6RGBLDayOrNightSts:
        sig_name = "LcuLLin3ALM6RGBLDayOrNightSts"
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

    class LcuLLin3ALM6RGBLLuminance:
        sig_name = "LcuLLin3ALM6RGBLLuminance"
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

    class LcuLLin3ALM6RGBLRed:
        sig_name = "LcuLLin3ALM6RGBLRed"
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


class ALMLCULLIN3LCUL_ALM_LIN3Fr07:
    msg_name = "ALMLCULLIN3LCUL_ALM_LIN3Fr07"
    msg_id = 6
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 1
    tx_node = "ALMLCULLIN3"
    rx_nodes = ['LCUL']
    sig_group_dict = {'LcuLLin3ALM6Failr': ['LcuLLin3ALM6FailrLEDSts', 'LcuLLin3ALM6FailrTmpSts', 'LcuLLin3ALM6FailrVltSts']}
    sig_group_dataid_dict = {}

    class LcuLLin3ALM6FailrLEDSts:
        sig_name = "LcuLLin3ALM6FailrLEDSts"
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

    class LcuLLin3ALM6FailrVltSts:
        sig_name = "LcuLLin3ALM6FailrVltSts"
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

    class LcuLLin3ALM6FailrTmpSts:
        sig_name = "LcuLLin3ALM6FailrTmpSts"
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


class LCULLCUL_ALM_LIN3Fr11:
    msg_name = "LCULLCUL_ALM_LIN3Fr11"
    msg_id = 21
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "LCUL"
    rx_nodes = ['ALMLCULLIN3']
    sig_group_dict = {'LcuLLin3ALM10RGBL': ['LcuLLin3ALM10RGBLBlue', 'LcuLLin3ALM10RGBLDayOrNightSts', 'LcuLLin3ALM10RGBLGreen', 'LcuLLin3ALM10RGBLLuminance', 'LcuLLin3ALM10RGBLRed']}
    sig_group_dataid_dict = {}

    class LcuLLin3ALM10RGBLRed:
        sig_name = "LcuLLin3ALM10RGBLRed"
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

    class LcuLLin3ALM10RGBLBlue:
        sig_name = "LcuLLin3ALM10RGBLBlue"
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

    class LcuLLin3ALM10RGBLLuminance:
        sig_name = "LcuLLin3ALM10RGBLLuminance"
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

    class LcuLLin3ALM10RGBLGreen:
        sig_name = "LcuLLin3ALM10RGBLGreen"
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

    class LcuLLin3ALM10RGBLDayOrNightSts:
        sig_name = "LcuLLin3ALM10RGBLDayOrNightSts"
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


class LCULLCUL_ALM_LIN3Fr08:
    msg_name = "LCULLCUL_ALM_LIN3Fr08"
    msg_id = 18
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "LCUL"
    rx_nodes = ['ALMLCULLIN3']
    sig_group_dict = {'LcuLLin3ALM7RGBL': ['LcuLLin3ALM7RGBLBlue', 'LcuLLin3ALM7RGBLDayOrNightSts', 'LcuLLin3ALM7RGBLGreen', 'LcuLLin3ALM7RGBLLuminance', 'LcuLLin3ALM7RGBLRed']}
    sig_group_dataid_dict = {}

    class LcuLLin3ALM7RGBLLuminance:
        sig_name = "LcuLLin3ALM7RGBLLuminance"
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

    class LcuLLin3ALM7RGBLDayOrNightSts:
        sig_name = "LcuLLin3ALM7RGBLDayOrNightSts"
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

    class LcuLLin3ALM7RGBLBlue:
        sig_name = "LcuLLin3ALM7RGBLBlue"
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

    class LcuLLin3ALM7RGBLGreen:
        sig_name = "LcuLLin3ALM7RGBLGreen"
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

    class LcuLLin3ALM7RGBLRed:
        sig_name = "LcuLLin3ALM7RGBLRed"
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


class ALMLCULLIN3LCUL_ALM_LIN3Fr05:
    msg_name = "ALMLCULLIN3LCUL_ALM_LIN3Fr05"
    msg_id = 4
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 1
    tx_node = "ALMLCULLIN3"
    rx_nodes = ['LCUL']
    sig_group_dict = {'LcuLLin3ALM4Failr': ['LcuLLin3ALM4FailrLEDSts', 'LcuLLin3ALM4FailrTmpSts', 'LcuLLin3ALM4FailrVltSts']}
    sig_group_dataid_dict = {}

    class LcuLLin3ALM4FailrTmpSts:
        sig_name = "LcuLLin3ALM4FailrTmpSts"
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

    class LcuLLin3ALM4FailrVltSts:
        sig_name = "LcuLLin3ALM4FailrVltSts"
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

    class LcuLLin3ALM4FailrLEDSts:
        sig_name = "LcuLLin3ALM4FailrLEDSts"
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


class LCULLCUL_ALM_LIN3Fr09:
    msg_name = "LCULLCUL_ALM_LIN3Fr09"
    msg_id = 19
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "LCUL"
    rx_nodes = ['ALMLCULLIN3']
    sig_group_dict = {'LcuLLin3ALM8RGBL': ['LcuLLin3ALM8RGBLBlue', 'LcuLLin3ALM8RGBLDayOrNightSts', 'LcuLLin3ALM8RGBLGreen', 'LcuLLin3ALM8RGBLLuminance', 'LcuLLin3ALM8RGBLRed']}
    sig_group_dataid_dict = {}

    class LcuLLin3ALM8RGBLDayOrNightSts:
        sig_name = "LcuLLin3ALM8RGBLDayOrNightSts"
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

    class LcuLLin3ALM8RGBLLuminance:
        sig_name = "LcuLLin3ALM8RGBLLuminance"
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

    class LcuLLin3ALM8RGBLBlue:
        sig_name = "LcuLLin3ALM8RGBLBlue"
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

    class LcuLLin3ALM8RGBLGreen:
        sig_name = "LcuLLin3ALM8RGBLGreen"
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

    class LcuLLin3ALM8RGBLRed:
        sig_name = "LcuLLin3ALM8RGBLRed"
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


class ALMLCULLIN3LCUL_ALM_LIN3Fr06:
    msg_name = "ALMLCULLIN3LCUL_ALM_LIN3Fr06"
    msg_id = 5
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 1
    tx_node = "ALMLCULLIN3"
    rx_nodes = ['LCUL']
    sig_group_dict = {'LcuLLin3ALM5Failr': ['LcuLLin3ALM5FailrLEDSts', 'LcuLLin3ALM5FailrTmpSts', 'LcuLLin3ALM5FailrVltSts']}
    sig_group_dataid_dict = {}

    class LcuLLin3ALM5FailrTmpSts:
        sig_name = "LcuLLin3ALM5FailrTmpSts"
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

    class LcuLLin3ALM5FailrLEDSts:
        sig_name = "LcuLLin3ALM5FailrLEDSts"
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

    class LcuLLin3ALM5FailrVltSts:
        sig_name = "LcuLLin3ALM5FailrVltSts"
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


class LCULToALMLCULALMLIN3ReqFrame:
    msg_name = "LCULToALMLCULALMLIN3ReqFrame"
    msg_id = 60
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "LCUL"
    rx_nodes = ['ALMLCULLIN3']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class LCULLCUL_ALM_LIN3Fr03:
    msg_name = "LCULLCUL_ALM_LIN3Fr03"
    msg_id = 13
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "LCUL"
    rx_nodes = ['ALMLCULLIN3']
    sig_group_dict = {'LcuLLin3ALM2RGBL': ['LcuLLin3ALM2RGBLBlue', 'LcuLLin3ALM2RGBLDayOrNightSts', 'LcuLLin3ALM2RGBLGreen', 'LcuLLin3ALM2RGBLLuminance', 'LcuLLin3ALM2RGBLRed']}
    sig_group_dataid_dict = {}

    class LcuLLin3ALM2RGBLRed:
        sig_name = "LcuLLin3ALM2RGBLRed"
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

    class LcuLLin3ALM2RGBLLuminance:
        sig_name = "LcuLLin3ALM2RGBLLuminance"
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

    class LcuLLin3ALM2RGBLBlue:
        sig_name = "LcuLLin3ALM2RGBLBlue"
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

    class LcuLLin3ALM2RGBLGreen:
        sig_name = "LcuLLin3ALM2RGBLGreen"
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

    class LcuLLin3ALM2RGBLDayOrNightSts:
        sig_name = "LcuLLin3ALM2RGBLDayOrNightSts"
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


class ALMLCULLIN3LCUL_ALM_LIN3Fr10:
    msg_name = "ALMLCULLIN3LCUL_ALM_LIN3Fr10"
    msg_id = 9
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 1
    tx_node = "ALMLCULLIN3"
    rx_nodes = ['LCUL']
    sig_group_dict = {'LcuLLin3ALM9Failr': ['LcuLLin3ALM9FailrLEDSts', 'LcuLLin3ALM9FailrTmpSts', 'LcuLLin3ALM9FailrVltSts']}
    sig_group_dataid_dict = {}

    class LcuLLin3ALM9FailrTmpSts:
        sig_name = "LcuLLin3ALM9FailrTmpSts"
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

    class LcuLLin3ALM9FailrVltSts:
        sig_name = "LcuLLin3ALM9FailrVltSts"
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

    class LcuLLin3ALM9FailrLEDSts:
        sig_name = "LcuLLin3ALM9FailrLEDSts"
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


class LCULLCUL_ALM_LIN3Fr04:
    msg_name = "LCULLCUL_ALM_LIN3Fr04"
    msg_id = 14
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "LCUL"
    rx_nodes = ['ALMLCULLIN3']
    sig_group_dict = {'LcuLLin3ALM3RGBL': ['LcuLLin3ALM3RGBLBlue', 'LcuLLin3ALM3RGBLDayOrNightSts', 'LcuLLin3ALM3RGBLGreen', 'LcuLLin3ALM3RGBLLuminance', 'LcuLLin3ALM3RGBLRed']}
    sig_group_dataid_dict = {}

    class LcuLLin3ALM3RGBLRed:
        sig_name = "LcuLLin3ALM3RGBLRed"
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

    class LcuLLin3ALM3RGBLGreen:
        sig_name = "LcuLLin3ALM3RGBLGreen"
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

    class LcuLLin3ALM3RGBLLuminance:
        sig_name = "LcuLLin3ALM3RGBLLuminance"
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

    class LcuLLin3ALM3RGBLBlue:
        sig_name = "LcuLLin3ALM3RGBLBlue"
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

    class LcuLLin3ALM3RGBLDayOrNightSts:
        sig_name = "LcuLLin3ALM3RGBLDayOrNightSts"
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


class LCULLCUL_ALM_LIN3Fr06:
    msg_name = "LCULLCUL_ALM_LIN3Fr06"
    msg_id = 16
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "LCUL"
    rx_nodes = ['ALMLCULLIN3']
    sig_group_dict = {'LcuLLin3ALM5RGBL': ['LcuLLin3ALM5RGBLBlue', 'LcuLLin3ALM5RGBLDayOrNightSts', 'LcuLLin3ALM5RGBLGreen', 'LcuLLin3ALM5RGBLLuminance', 'LcuLLin3ALM5RGBLRed']}
    sig_group_dataid_dict = {}

    class LcuLLin3ALM5RGBLGreen:
        sig_name = "LcuLLin3ALM5RGBLGreen"
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

    class LcuLLin3ALM5RGBLLuminance:
        sig_name = "LcuLLin3ALM5RGBLLuminance"
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

    class LcuLLin3ALM5RGBLBlue:
        sig_name = "LcuLLin3ALM5RGBLBlue"
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

    class LcuLLin3ALM5RGBLDayOrNightSts:
        sig_name = "LcuLLin3ALM5RGBLDayOrNightSts"
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

    class LcuLLin3ALM5RGBLRed:
        sig_name = "LcuLLin3ALM5RGBLRed"
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


class ALMLCULLIN3LCUL_ALM_LIN3Fr02:
    msg_name = "ALMLCULLIN3LCUL_ALM_LIN3Fr02"
    msg_id = 1
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 1
    tx_node = "ALMLCULLIN3"
    rx_nodes = ['LCUL']
    sig_group_dict = {'LcuLLin3ALM1Failr': ['LcuLLin3ALM1FailrLEDSts', 'LcuLLin3ALM1FailrTmpSts', 'LcuLLin3ALM1FailrVltSts']}
    sig_group_dataid_dict = {}

    class LcuLLin3ALM1FailrTmpSts:
        sig_name = "LcuLLin3ALM1FailrTmpSts"
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

    class LcuLLin3ALM1FailrVltSts:
        sig_name = "LcuLLin3ALM1FailrVltSts"
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

    class LcuLLin3ALM1FailrLEDSts:
        sig_name = "LcuLLin3ALM1FailrLEDSts"
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


class LCULLCUL_ALM_LIN3Fr10:
    msg_name = "LCULLCUL_ALM_LIN3Fr10"
    msg_id = 20
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "LCUL"
    rx_nodes = ['ALMLCULLIN3']
    sig_group_dict = {'LcuLLin3ALM9RGBL': ['LcuLLin3ALM9RGBLBlue', 'LcuLLin3ALM9RGBLDayOrNightSts', 'LcuLLin3ALM9RGBLGreen', 'LcuLLin3ALM9RGBLLuminance', 'LcuLLin3ALM9RGBLRed']}
    sig_group_dataid_dict = {}

    class LcuLLin3ALM9RGBLDayOrNightSts:
        sig_name = "LcuLLin3ALM9RGBLDayOrNightSts"
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

    class LcuLLin3ALM9RGBLLuminance:
        sig_name = "LcuLLin3ALM9RGBLLuminance"
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

    class LcuLLin3ALM9RGBLGreen:
        sig_name = "LcuLLin3ALM9RGBLGreen"
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

    class LcuLLin3ALM9RGBLBlue:
        sig_name = "LcuLLin3ALM9RGBLBlue"
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

    class LcuLLin3ALM9RGBLRed:
        sig_name = "LcuLLin3ALM9RGBLRed"
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


class ALMLCULLIN3LCUL_ALM_LIN3Fr09:
    msg_name = "ALMLCULLIN3LCUL_ALM_LIN3Fr09"
    msg_id = 8
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 1
    tx_node = "ALMLCULLIN3"
    rx_nodes = ['LCUL']
    sig_group_dict = {'LcuLLin3ALM8Failr': ['LcuLLin3ALM8FailrLEDSts', 'LcuLLin3ALM8FailrTmpSts', 'LcuLLin3ALM8FailrVltSts']}
    sig_group_dataid_dict = {}

    class LcuLLin3ALM8FailrLEDSts:
        sig_name = "LcuLLin3ALM8FailrLEDSts"
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

    class LcuLLin3ALM8FailrVltSts:
        sig_name = "LcuLLin3ALM8FailrVltSts"
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

    class LcuLLin3ALM8FailrTmpSts:
        sig_name = "LcuLLin3ALM8FailrTmpSts"
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


class ALMLCULLIN3LCUL_ALM_LIN3Fr04:
    msg_name = "ALMLCULLIN3LCUL_ALM_LIN3Fr04"
    msg_id = 3
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 1
    tx_node = "ALMLCULLIN3"
    rx_nodes = ['LCUL']
    sig_group_dict = {'LcuLLin3ALM3Failr': ['LcuLLin3ALM3FailrLEDSts', 'LcuLLin3ALM3FailrTmpSts', 'LcuLLin3ALM3FailrVltSts']}
    sig_group_dataid_dict = {}

    class LcuLLin3ALM3FailrVltSts:
        sig_name = "LcuLLin3ALM3FailrVltSts"
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

    class LcuLLin3ALM3FailrLEDSts:
        sig_name = "LcuLLin3ALM3FailrLEDSts"
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

    class LcuLLin3ALM3FailrTmpSts:
        sig_name = "LcuLLin3ALM3FailrTmpSts"
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


class ALMLCULLIN3LCUL_ALM_LIN3Fr11:
    msg_name = "ALMLCULLIN3LCUL_ALM_LIN3Fr11"
    msg_id = 10
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 1
    tx_node = "ALMLCULLIN3"
    rx_nodes = ['LCUL']
    sig_group_dict = {'LcuLLin3ALM10Failr': ['LcuLLin3ALM10FailrLEDSts', 'LcuLLin3ALM10FailrTmpSts', 'LcuLLin3ALM10FailrVltSts']}
    sig_group_dataid_dict = {}

    class LcuLLin3ALM10FailrTmpSts:
        sig_name = "LcuLLin3ALM10FailrTmpSts"
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

    class LcuLLin3ALM10FailrLEDSts:
        sig_name = "LcuLLin3ALM10FailrLEDSts"
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

    class LcuLLin3ALM10FailrVltSts:
        sig_name = "LcuLLin3ALM10FailrVltSts"
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


class ALMLCULLIN3LCUL_ALM_LIN3Fr08:
    msg_name = "ALMLCULLIN3LCUL_ALM_LIN3Fr08"
    msg_id = 7
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 1
    tx_node = "ALMLCULLIN3"
    rx_nodes = ['LCUL']
    sig_group_dict = {'LcuLLin3ALM7Failr': ['LcuLLin3ALM7FailrLEDSts', 'LcuLLin3ALM7FailrTmpSts', 'LcuLLin3ALM7FailrVltSts']}
    sig_group_dataid_dict = {}

    class LcuLLin3ALM7FailrLEDSts:
        sig_name = "LcuLLin3ALM7FailrLEDSts"
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

    class LcuLLin3ALM7FailrVltSts:
        sig_name = "LcuLLin3ALM7FailrVltSts"
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

    class LcuLLin3ALM7FailrTmpSts:
        sig_name = "LcuLLin3ALM7FailrTmpSts"
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


class LCULLCUL_ALM_LIN3Fr05:
    msg_name = "LCULLCUL_ALM_LIN3Fr05"
    msg_id = 15
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "LCUL"
    rx_nodes = ['ALMLCULLIN3']
    sig_group_dict = {'LcuLLin3ALM4RGBL': ['LcuLLin3ALM4RGBLBlue', 'LcuLLin3ALM4RGBLDayOrNightSts', 'LcuLLin3ALM4RGBLGreen', 'LcuLLin3ALM4RGBLLuminance', 'LcuLLin3ALM4RGBLRed']}
    sig_group_dataid_dict = {}

    class LcuLLin3ALM4RGBLDayOrNightSts:
        sig_name = "LcuLLin3ALM4RGBLDayOrNightSts"
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

    class LcuLLin3ALM4RGBLGreen:
        sig_name = "LcuLLin3ALM4RGBLGreen"
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

    class LcuLLin3ALM4RGBLLuminance:
        sig_name = "LcuLLin3ALM4RGBLLuminance"
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

    class LcuLLin3ALM4RGBLRed:
        sig_name = "LcuLLin3ALM4RGBLRed"
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

    class LcuLLin3ALM4RGBLBlue:
        sig_name = "LcuLLin3ALM4RGBLBlue"
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


class LCULLCUL_ALM_LIN3Fr02:
    msg_name = "LCULLCUL_ALM_LIN3Fr02"
    msg_id = 12
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "LCUL"
    rx_nodes = ['ALMLCULLIN3']
    sig_group_dict = {'LcuLLin3ALM1RGBL': ['LcuLLin3ALM1RGBLBlue', 'LcuLLin3ALM1RGBLDayOrNightSts', 'LcuLLin3ALM1RGBLGreen', 'LcuLLin3ALM1RGBLLuminance', 'LcuLLin3ALM1RGBLRed']}
    sig_group_dataid_dict = {}

    class LcuLLin3ALM1RGBLRed:
        sig_name = "LcuLLin3ALM1RGBLRed"
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

    class LcuLLin3ALM1RGBLBlue:
        sig_name = "LcuLLin3ALM1RGBLBlue"
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

    class LcuLLin3ALM1RGBLGreen:
        sig_name = "LcuLLin3ALM1RGBLGreen"
        sig_start_bit = 8
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
        startbit = 8
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class LcuLLin3ALM1RGBLLuminance:
        sig_name = "LcuLLin3ALM1RGBLLuminance"
        sig_start_bit = 17
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
        startbit = 17
        byte = 2
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class LcuLLin3ALM1RGBLDayOrNightSts:
        sig_name = "LcuLLin3ALM1RGBLDayOrNightSts"
        sig_start_bit = 16
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
        startbit = 16
        byte = 2
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0


class ALMLCULLIN3LCUL_ALM_LIN3Fr03:
    msg_name = "ALMLCULLIN3LCUL_ALM_LIN3Fr03"
    msg_id = 2
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 1
    tx_node = "ALMLCULLIN3"
    rx_nodes = ['LCUL']
    sig_group_dict = {'LcuLLin3ALM2Failr': ['LcuLLin3ALM2FailrLEDSts', 'LcuLLin3ALM2FailrTmpSts', 'LcuLLin3ALM2FailrVltSts']}
    sig_group_dataid_dict = {}

    class LcuLLin3ALM2FailrLEDSts:
        sig_name = "LcuLLin3ALM2FailrLEDSts"
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

    class LcuLLin3ALM2FailrVltSts:
        sig_name = "LcuLLin3ALM2FailrVltSts"
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

    class LcuLLin3ALM2FailrTmpSts:
        sig_name = "LcuLLin3ALM2FailrTmpSts"
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


class ALMToLCULLCULALMLIN3RespFrame:
    msg_name = "ALMToLCULLCULALMLIN3RespFrame"
    msg_id = 61
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "ALMLCULLIN3"
    rx_nodes = ['LCUL']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


