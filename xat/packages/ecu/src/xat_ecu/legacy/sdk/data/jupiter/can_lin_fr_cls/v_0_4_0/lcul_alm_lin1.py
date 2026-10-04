lin_scheduleTable = {'LCUL_ALM_LIN1_DiagSchedule01': [(0, 'LCULToALMLCULALMLIN1ReqFrame', 0.015), (1, 'ALMToLCULLCULALMLIN1RespFrame', 0.015)], 'LCUL_ALM_LIN1Schedule01_LCUL_ALM_LIN1': [(0, 'LCULLCUL_ALM_LIN1Fr02', 0.01), (1, 'LCULLCUL_ALM_LIN1Fr03', 0.01), (2, 'LCULLCUL_ALM_LIN1Fr04', 0.01), (3, 'LCULLCUL_ALM_LIN1Fr05', 0.01), (4, 'LCULLCUL_ALM_LIN1Fr06', 0.01), (5, 'LCULLCUL_ALM_LIN1Fr07', 0.01), (6, 'LCULLCUL_ALM_LIN1Fr08', 0.01), (7, 'LCULLCUL_ALM_LIN1Fr09', 0.01), (8, 'LCULLCUL_ALM_LIN1Fr10', 0.01), (9, 'LCULLCUL_ALM_LIN1Fr11', 0.01)], 'LCUL_ALM_LIN1_ScheduleFailrSts_LCUL_ALM_LIN1': [(0, 'ALMLCULLIN1LCUL_ALM_LIN1Fr02', 0.01), (1, 'ALMLCULLIN1LCUL_ALM_LIN1Fr03', 0.01), (2, 'ALMLCULLIN1LCUL_ALM_LIN1Fr04', 0.01), (3, 'ALMLCULLIN1LCUL_ALM_LIN1Fr05', 0.01), (4, 'ALMLCULLIN1LCUL_ALM_LIN1Fr06', 0.01), (5, 'ALMLCULLIN1LCUL_ALM_LIN1Fr07', 0.01), (6, 'ALMLCULLIN1LCUL_ALM_LIN1Fr08', 0.01), (7, 'ALMLCULLIN1LCUL_ALM_LIN1Fr09', 0.01), (8, 'ALMLCULLIN1LCUL_ALM_LIN1Fr10', 0.01), (9, 'ALMLCULLIN1LCUL_ALM_LIN1Fr11', 0.01)]}


class ALMLCULLIN1LCUL_ALM_LIN1Fr09:
    msg_name = "ALMLCULLIN1LCUL_ALM_LIN1Fr09"
    msg_id = 8
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 1
    tx_node = "ALMLCULLIN1"
    rx_nodes = ['LCUL']
    sig_group_dict = {'LcuLLin1ALM8Failr': ['LcuLLin1ALM8FailrLEDSts', 'LcuLLin1ALM8FailrTmpSts', 'LcuLLin1ALM8FailrVltSts']}
    sig_group_dataid_dict = {}

    class LcuLLin1ALM8FailrLEDSts:
        sig_name = "LcuLLin1ALM8FailrLEDSts"
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

    class LcuLLin1ALM8FailrTmpSts:
        sig_name = "LcuLLin1ALM8FailrTmpSts"
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

    class LcuLLin1ALM8FailrVltSts:
        sig_name = "LcuLLin1ALM8FailrVltSts"
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


class LCULLCUL_ALM_LIN1Fr06:
    msg_name = "LCULLCUL_ALM_LIN1Fr06"
    msg_id = 16
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "LCUL"
    rx_nodes = ['ALMLCULLIN1']
    sig_group_dict = {'LcuLLin1ALM5RGBL': ['LcuLLin1ALM5RGBLBlue', 'LcuLLin1ALM5RGBLDayOrNightSts', 'LcuLLin1ALM5RGBLGreen', 'LcuLLin1ALM5RGBLLuminance', 'LcuLLin1ALM5RGBLRed']}
    sig_group_dataid_dict = {}

    class LcuLLin1ALM5RGBLGreen:
        sig_name = "LcuLLin1ALM5RGBLGreen"
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

    class LcuLLin1ALM5RGBLLuminance:
        sig_name = "LcuLLin1ALM5RGBLLuminance"
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

    class LcuLLin1ALM5RGBLDayOrNightSts:
        sig_name = "LcuLLin1ALM5RGBLDayOrNightSts"
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

    class LcuLLin1ALM5RGBLRed:
        sig_name = "LcuLLin1ALM5RGBLRed"
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

    class LcuLLin1ALM5RGBLBlue:
        sig_name = "LcuLLin1ALM5RGBLBlue"
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


class ALMLCULLIN1LCUL_ALM_LIN1Fr04:
    msg_name = "ALMLCULLIN1LCUL_ALM_LIN1Fr04"
    msg_id = 3
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 1
    tx_node = "ALMLCULLIN1"
    rx_nodes = ['LCUL']
    sig_group_dict = {'LcuLLin1ALM3Failr': ['LcuLLin1ALM3FailrLEDSts', 'LcuLLin1ALM3FailrTmpSts', 'LcuLLin1ALM3FailrVltSts']}
    sig_group_dataid_dict = {}

    class LcuLLin1ALM3FailrVltSts:
        sig_name = "LcuLLin1ALM3FailrVltSts"
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

    class LcuLLin1ALM3FailrLEDSts:
        sig_name = "LcuLLin1ALM3FailrLEDSts"
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

    class LcuLLin1ALM3FailrTmpSts:
        sig_name = "LcuLLin1ALM3FailrTmpSts"
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


class LCULLCUL_ALM_LIN1Fr03:
    msg_name = "LCULLCUL_ALM_LIN1Fr03"
    msg_id = 13
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "LCUL"
    rx_nodes = ['ALMLCULLIN1']
    sig_group_dict = {'LcuLLin1ALM2RGBL': ['LcuLLin1ALM2RGBLBlue', 'LcuLLin1ALM2RGBLDayOrNightSts', 'LcuLLin1ALM2RGBLGreen', 'LcuLLin1ALM2RGBLLuminance', 'LcuLLin1ALM2RGBLRed']}
    sig_group_dataid_dict = {}

    class LcuLLin1ALM2RGBLRed:
        sig_name = "LcuLLin1ALM2RGBLRed"
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

    class LcuLLin1ALM2RGBLLuminance:
        sig_name = "LcuLLin1ALM2RGBLLuminance"
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

    class LcuLLin1ALM2RGBLDayOrNightSts:
        sig_name = "LcuLLin1ALM2RGBLDayOrNightSts"
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

    class LcuLLin1ALM2RGBLGreen:
        sig_name = "LcuLLin1ALM2RGBLGreen"
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

    class LcuLLin1ALM2RGBLBlue:
        sig_name = "LcuLLin1ALM2RGBLBlue"
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


class ALMToLCULLCULALMLIN1RespFrame:
    msg_name = "ALMToLCULLCULALMLIN1RespFrame"
    msg_id = 61
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "ALMLCULLIN1"
    rx_nodes = ['LCUL']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class ALMLCULLIN1LCUL_ALM_LIN1Fr06:
    msg_name = "ALMLCULLIN1LCUL_ALM_LIN1Fr06"
    msg_id = 5
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 1
    tx_node = "ALMLCULLIN1"
    rx_nodes = ['LCUL']
    sig_group_dict = {'LcuLLin1ALM5Failr': ['LcuLLin1ALM5FailrLEDSts', 'LcuLLin1ALM5FailrTmpSts', 'LcuLLin1ALM5FailrVltSts']}
    sig_group_dataid_dict = {}

    class LcuLLin1ALM5FailrTmpSts:
        sig_name = "LcuLLin1ALM5FailrTmpSts"
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

    class LcuLLin1ALM5FailrLEDSts:
        sig_name = "LcuLLin1ALM5FailrLEDSts"
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

    class LcuLLin1ALM5FailrVltSts:
        sig_name = "LcuLLin1ALM5FailrVltSts"
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


class LCULLCUL_ALM_LIN1Fr04:
    msg_name = "LCULLCUL_ALM_LIN1Fr04"
    msg_id = 14
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "LCUL"
    rx_nodes = ['ALMLCULLIN1']
    sig_group_dict = {'LcuLLin1ALM3RGBL': ['LcuLLin1ALM3RGBLBlue', 'LcuLLin1ALM3RGBLDayOrNightSts', 'LcuLLin1ALM3RGBLGreen', 'LcuLLin1ALM3RGBLLuminance', 'LcuLLin1ALM3RGBLRed']}
    sig_group_dataid_dict = {}

    class LcuLLin1ALM3RGBLBlue:
        sig_name = "LcuLLin1ALM3RGBLBlue"
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

    class LcuLLin1ALM3RGBLGreen:
        sig_name = "LcuLLin1ALM3RGBLGreen"
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

    class LcuLLin1ALM3RGBLLuminance:
        sig_name = "LcuLLin1ALM3RGBLLuminance"
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

    class LcuLLin1ALM3RGBLDayOrNightSts:
        sig_name = "LcuLLin1ALM3RGBLDayOrNightSts"
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

    class LcuLLin1ALM3RGBLRed:
        sig_name = "LcuLLin1ALM3RGBLRed"
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


class LCULLCUL_ALM_LIN1Fr11:
    msg_name = "LCULLCUL_ALM_LIN1Fr11"
    msg_id = 21
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "LCUL"
    rx_nodes = ['ALMLCULLIN1']
    sig_group_dict = {'LcuLLin1ALM10RGBL': ['LcuLLin1ALM10RGBLBlue', 'LcuLLin1ALM10RGBLDayOrNightSts', 'LcuLLin1ALM10RGBLGreen', 'LcuLLin1ALM10RGBLLuminance', 'LcuLLin1ALM10RGBLRed']}
    sig_group_dataid_dict = {}

    class LcuLLin1ALM10RGBLLuminance:
        sig_name = "LcuLLin1ALM10RGBLLuminance"
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

    class LcuLLin1ALM10RGBLDayOrNightSts:
        sig_name = "LcuLLin1ALM10RGBLDayOrNightSts"
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

    class LcuLLin1ALM10RGBLRed:
        sig_name = "LcuLLin1ALM10RGBLRed"
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

    class LcuLLin1ALM10RGBLGreen:
        sig_name = "LcuLLin1ALM10RGBLGreen"
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

    class LcuLLin1ALM10RGBLBlue:
        sig_name = "LcuLLin1ALM10RGBLBlue"
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


class ALMLCULLIN1LCUL_ALM_LIN1Fr03:
    msg_name = "ALMLCULLIN1LCUL_ALM_LIN1Fr03"
    msg_id = 2
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 1
    tx_node = "ALMLCULLIN1"
    rx_nodes = ['LCUL']
    sig_group_dict = {'LcuLLin1ALM2Failr': ['LcuLLin1ALM2FailrLEDSts', 'LcuLLin1ALM2FailrTmpSts', 'LcuLLin1ALM2FailrVltSts']}
    sig_group_dataid_dict = {}

    class LcuLLin1ALM2FailrLEDSts:
        sig_name = "LcuLLin1ALM2FailrLEDSts"
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

    class LcuLLin1ALM2FailrVltSts:
        sig_name = "LcuLLin1ALM2FailrVltSts"
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

    class LcuLLin1ALM2FailrTmpSts:
        sig_name = "LcuLLin1ALM2FailrTmpSts"
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


class ALMLCULLIN1LCUL_ALM_LIN1Fr07:
    msg_name = "ALMLCULLIN1LCUL_ALM_LIN1Fr07"
    msg_id = 6
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 1
    tx_node = "ALMLCULLIN1"
    rx_nodes = ['LCUL']
    sig_group_dict = {'LcuLLin1ALM6Failr': ['LcuLLin1ALM6FailrLEDSts', 'LcuLLin1ALM6FailrTmpSts', 'LcuLLin1ALM6FailrVltSts']}
    sig_group_dataid_dict = {}

    class LcuLLin1ALM6FailrVltSts:
        sig_name = "LcuLLin1ALM6FailrVltSts"
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

    class LcuLLin1ALM6FailrTmpSts:
        sig_name = "LcuLLin1ALM6FailrTmpSts"
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

    class LcuLLin1ALM6FailrLEDSts:
        sig_name = "LcuLLin1ALM6FailrLEDSts"
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


class LCULToALMLCULALMLIN1ReqFrame:
    msg_name = "LCULToALMLCULALMLIN1ReqFrame"
    msg_id = 60
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "LCUL"
    rx_nodes = ['ALMLCULLIN1']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class LCULLCUL_ALM_LIN1Fr05:
    msg_name = "LCULLCUL_ALM_LIN1Fr05"
    msg_id = 15
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "LCUL"
    rx_nodes = ['ALMLCULLIN1']
    sig_group_dict = {'LcuLLin1ALM4RGBL': ['LcuLLin1ALM4RGBLBlue', 'LcuLLin1ALM4RGBLDayOrNightSts', 'LcuLLin1ALM4RGBLGreen', 'LcuLLin1ALM4RGBLLuminance', 'LcuLLin1ALM4RGBLRed']}
    sig_group_dataid_dict = {}

    class LcuLLin1ALM4RGBLBlue:
        sig_name = "LcuLLin1ALM4RGBLBlue"
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

    class LcuLLin1ALM4RGBLLuminance:
        sig_name = "LcuLLin1ALM4RGBLLuminance"
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

    class LcuLLin1ALM4RGBLGreen:
        sig_name = "LcuLLin1ALM4RGBLGreen"
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

    class LcuLLin1ALM4RGBLDayOrNightSts:
        sig_name = "LcuLLin1ALM4RGBLDayOrNightSts"
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

    class LcuLLin1ALM4RGBLRed:
        sig_name = "LcuLLin1ALM4RGBLRed"
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


class ALMLCULLIN1LCUL_ALM_LIN1Fr02:
    msg_name = "ALMLCULLIN1LCUL_ALM_LIN1Fr02"
    msg_id = 1
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 1
    tx_node = "ALMLCULLIN1"
    rx_nodes = ['LCUL']
    sig_group_dict = {'LcuLLin1ALM1Failr': ['LcuLLin1ALM1FailrLEDSts', 'LcuLLin1ALM1FailrTmpSts', 'LcuLLin1ALM1FailrVltSts']}
    sig_group_dataid_dict = {}

    class LcuLLin1ALM1FailrTmpSts:
        sig_name = "LcuLLin1ALM1FailrTmpSts"
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

    class LcuLLin1ALM1FailrVltSts:
        sig_name = "LcuLLin1ALM1FailrVltSts"
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

    class LcuLLin1ALM1FailrLEDSts:
        sig_name = "LcuLLin1ALM1FailrLEDSts"
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


class LCULLCUL_ALM_LIN1Fr08:
    msg_name = "LCULLCUL_ALM_LIN1Fr08"
    msg_id = 18
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "LCUL"
    rx_nodes = ['ALMLCULLIN1']
    sig_group_dict = {'LcuLLin1ALM7RGBL': ['LcuLLin1ALM7RGBLBlue', 'LcuLLin1ALM7RGBLDayOrNightSts', 'LcuLLin1ALM7RGBLGreen', 'LcuLLin1ALM7RGBLLuminance', 'LcuLLin1ALM7RGBLRed']}
    sig_group_dataid_dict = {}

    class LcuLLin1ALM7RGBLGreen:
        sig_name = "LcuLLin1ALM7RGBLGreen"
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

    class LcuLLin1ALM7RGBLDayOrNightSts:
        sig_name = "LcuLLin1ALM7RGBLDayOrNightSts"
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

    class LcuLLin1ALM7RGBLRed:
        sig_name = "LcuLLin1ALM7RGBLRed"
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

    class LcuLLin1ALM7RGBLLuminance:
        sig_name = "LcuLLin1ALM7RGBLLuminance"
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

    class LcuLLin1ALM7RGBLBlue:
        sig_name = "LcuLLin1ALM7RGBLBlue"
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


class ALMLCULLIN1LCUL_ALM_LIN1Fr10:
    msg_name = "ALMLCULLIN1LCUL_ALM_LIN1Fr10"
    msg_id = 9
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 1
    tx_node = "ALMLCULLIN1"
    rx_nodes = ['LCUL']
    sig_group_dict = {'LcuLLin1ALM9Failr': ['LcuLLin1ALM9FailrLEDSts', 'LcuLLin1ALM9FailrTmpSts', 'LcuLLin1ALM9FailrVltSts']}
    sig_group_dataid_dict = {}

    class LcuLLin1ALM9FailrLEDSts:
        sig_name = "LcuLLin1ALM9FailrLEDSts"
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

    class LcuLLin1ALM9FailrTmpSts:
        sig_name = "LcuLLin1ALM9FailrTmpSts"
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

    class LcuLLin1ALM9FailrVltSts:
        sig_name = "LcuLLin1ALM9FailrVltSts"
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


class ALMLCULLIN1LCUL_ALM_LIN1Fr11:
    msg_name = "ALMLCULLIN1LCUL_ALM_LIN1Fr11"
    msg_id = 10
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 1
    tx_node = "ALMLCULLIN1"
    rx_nodes = ['LCUL']
    sig_group_dict = {'LcuLLin1ALM10Failr': ['LcuLLin1ALM10FailrLEDSts', 'LcuLLin1ALM10FailrTmpSts', 'LcuLLin1ALM10FailrVltSts']}
    sig_group_dataid_dict = {}

    class LcuLLin1ALM10FailrLEDSts:
        sig_name = "LcuLLin1ALM10FailrLEDSts"
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

    class LcuLLin1ALM10FailrTmpSts:
        sig_name = "LcuLLin1ALM10FailrTmpSts"
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

    class LcuLLin1ALM10FailrVltSts:
        sig_name = "LcuLLin1ALM10FailrVltSts"
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


class LCULLCUL_ALM_LIN1Fr09:
    msg_name = "LCULLCUL_ALM_LIN1Fr09"
    msg_id = 19
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "LCUL"
    rx_nodes = ['ALMLCULLIN1']
    sig_group_dict = {'LcuLLin1ALM8RGBL': ['LcuLLin1ALM8RGBLBlue', 'LcuLLin1ALM8RGBLDayOrNightSts', 'LcuLLin1ALM8RGBLGreen', 'LcuLLin1ALM8RGBLLuminance', 'LcuLLin1ALM8RGBLRed']}
    sig_group_dataid_dict = {}

    class LcuLLin1ALM8RGBLGreen:
        sig_name = "LcuLLin1ALM8RGBLGreen"
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

    class LcuLLin1ALM8RGBLRed:
        sig_name = "LcuLLin1ALM8RGBLRed"
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

    class LcuLLin1ALM8RGBLBlue:
        sig_name = "LcuLLin1ALM8RGBLBlue"
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

    class LcuLLin1ALM8RGBLLuminance:
        sig_name = "LcuLLin1ALM8RGBLLuminance"
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

    class LcuLLin1ALM8RGBLDayOrNightSts:
        sig_name = "LcuLLin1ALM8RGBLDayOrNightSts"
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


class LCULLCUL_ALM_LIN1Fr10:
    msg_name = "LCULLCUL_ALM_LIN1Fr10"
    msg_id = 20
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "LCUL"
    rx_nodes = ['ALMLCULLIN1']
    sig_group_dict = {'LcuLLin1ALM9RGBL': ['LcuLLin1ALM9RGBLBlue', 'LcuLLin1ALM9RGBLDayOrNightSts', 'LcuLLin1ALM9RGBLGreen', 'LcuLLin1ALM9RGBLLuminance', 'LcuLLin1ALM9RGBLRed']}
    sig_group_dataid_dict = {}

    class LcuLLin1ALM9RGBLDayOrNightSts:
        sig_name = "LcuLLin1ALM9RGBLDayOrNightSts"
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

    class LcuLLin1ALM9RGBLGreen:
        sig_name = "LcuLLin1ALM9RGBLGreen"
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

    class LcuLLin1ALM9RGBLLuminance:
        sig_name = "LcuLLin1ALM9RGBLLuminance"
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

    class LcuLLin1ALM9RGBLRed:
        sig_name = "LcuLLin1ALM9RGBLRed"
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

    class LcuLLin1ALM9RGBLBlue:
        sig_name = "LcuLLin1ALM9RGBLBlue"
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


class LCULLCUL_ALM_LIN1Fr02:
    msg_name = "LCULLCUL_ALM_LIN1Fr02"
    msg_id = 12
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "LCUL"
    rx_nodes = ['ALMLCULLIN1']
    sig_group_dict = {'LcuLLin1ALM1RGBL': ['LcuLLin1ALM1RGBLBlue', 'LcuLLin1ALM1RGBLDayOrNightSts', 'LcuLLin1ALM1RGBLGreen', 'LcuLLin1ALM1RGBLLuminance', 'LcuLLin1ALM1RGBLRed']}
    sig_group_dataid_dict = {}

    class LcuLLin1ALM1RGBLLuminance:
        sig_name = "LcuLLin1ALM1RGBLLuminance"
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

    class LcuLLin1ALM1RGBLGreen:
        sig_name = "LcuLLin1ALM1RGBLGreen"
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

    class LcuLLin1ALM1RGBLBlue:
        sig_name = "LcuLLin1ALM1RGBLBlue"
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

    class LcuLLin1ALM1RGBLDayOrNightSts:
        sig_name = "LcuLLin1ALM1RGBLDayOrNightSts"
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

    class LcuLLin1ALM1RGBLRed:
        sig_name = "LcuLLin1ALM1RGBLRed"
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


class LCULLCUL_ALM_LIN1Fr07:
    msg_name = "LCULLCUL_ALM_LIN1Fr07"
    msg_id = 17
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "LCUL"
    rx_nodes = ['ALMLCULLIN1']
    sig_group_dict = {'LcuLLin1ALM6RGBL': ['LcuLLin1ALM6RGBLBlue', 'LcuLLin1ALM6RGBLDayOrNightSts', 'LcuLLin1ALM6RGBLGreen', 'LcuLLin1ALM6RGBLLuminance', 'LcuLLin1ALM6RGBLRed']}
    sig_group_dataid_dict = {}

    class LcuLLin1ALM6RGBLRed:
        sig_name = "LcuLLin1ALM6RGBLRed"
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

    class LcuLLin1ALM6RGBLGreen:
        sig_name = "LcuLLin1ALM6RGBLGreen"
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

    class LcuLLin1ALM6RGBLDayOrNightSts:
        sig_name = "LcuLLin1ALM6RGBLDayOrNightSts"
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

    class LcuLLin1ALM6RGBLBlue:
        sig_name = "LcuLLin1ALM6RGBLBlue"
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

    class LcuLLin1ALM6RGBLLuminance:
        sig_name = "LcuLLin1ALM6RGBLLuminance"
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


class ALMLCULLIN1LCUL_ALM_LIN1Fr08:
    msg_name = "ALMLCULLIN1LCUL_ALM_LIN1Fr08"
    msg_id = 7
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 1
    tx_node = "ALMLCULLIN1"
    rx_nodes = ['LCUL']
    sig_group_dict = {'LcuLLin1ALM7Failr': ['LcuLLin1ALM7FailrLEDSts', 'LcuLLin1ALM7FailrTmpSts', 'LcuLLin1ALM7FailrVltSts']}
    sig_group_dataid_dict = {}

    class LcuLLin1ALM7FailrTmpSts:
        sig_name = "LcuLLin1ALM7FailrTmpSts"
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

    class LcuLLin1ALM7FailrVltSts:
        sig_name = "LcuLLin1ALM7FailrVltSts"
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

    class LcuLLin1ALM7FailrLEDSts:
        sig_name = "LcuLLin1ALM7FailrLEDSts"
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


class ALMLCULLIN1LCUL_ALM_LIN1Fr05:
    msg_name = "ALMLCULLIN1LCUL_ALM_LIN1Fr05"
    msg_id = 4
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 1
    tx_node = "ALMLCULLIN1"
    rx_nodes = ['LCUL']
    sig_group_dict = {'LcuLLin1ALM4Failr': ['LcuLLin1ALM4FailrLEDSts', 'LcuLLin1ALM4FailrTmpSts', 'LcuLLin1ALM4FailrVltSts']}
    sig_group_dataid_dict = {}

    class LcuLLin1ALM4FailrLEDSts:
        sig_name = "LcuLLin1ALM4FailrLEDSts"
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

    class LcuLLin1ALM4FailrTmpSts:
        sig_name = "LcuLLin1ALM4FailrTmpSts"
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

    class LcuLLin1ALM4FailrVltSts:
        sig_name = "LcuLLin1ALM4FailrVltSts"
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


