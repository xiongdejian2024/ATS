lin_scheduleTable = {'LCUR_ALM_LIN3_ScheduleFailrSts_LCUR_ALM_LIN3': [(0, 'ALMLCURLIN3LCUR_ALM_LIN3Fr02', 0.005), (1, 'ALMLCURLIN3LCUR_ALM_LIN3Fr03', 0.005), (2, 'ALMLCURLIN3LCUR_ALM_LIN3Fr04', 0.005), (3, 'ALMLCURLIN3LCUR_ALM_LIN3Fr05', 0.005), (4, 'ALMLCURLIN3LCUR_ALM_LIN3Fr06', 0.005), (5, 'ALMLCURLIN3LCUR_ALM_LIN3Fr07', 0.005), (6, 'ALMLCURLIN3LCUR_ALM_LIN3Fr08', 0.005), (7, 'ALMLCURLIN3LCUR_ALM_LIN3Fr09', 0.005), (8, 'ALMLCURLIN3LCUR_ALM_LIN3Fr10', 0.005), (9, 'ALMLCURLIN3LCUR_ALM_LIN3Fr11', 0.005)], 'LCUR_ALM_LIN3Schedule01_LCUR_ALM_LIN3': [(0, 'LCURLCUR_ALM_LIN3Fr02', 0.01), (1, 'LCURLCUR_ALM_LIN3Fr03', 0.01), (2, 'LCURLCUR_ALM_LIN3Fr04', 0.01), (3, 'LCURLCUR_ALM_LIN3Fr05', 0.01), (4, 'LCURLCUR_ALM_LIN3Fr06', 0.01), (5, 'LCURLCUR_ALM_LIN3Fr07', 0.01), (6, 'LCURLCUR_ALM_LIN3Fr08', 0.01), (7, 'LCURLCUR_ALM_LIN3Fr09', 0.01), (8, 'LCURLCUR_ALM_LIN3Fr10', 0.01), (9, 'LCURLCUR_ALM_LIN3Fr11', 0.01)], 'LCUR_ALM_LIN3_DiagSchedule01': [(0, 'LCURToALMLCURALMLIN3ReqFrame', 0.015), (1, 'ALMToLCURLCURALMLIN3RespFrame', 0.015)]}


class LCURLCUR_ALM_LIN3Fr08:
    msg_name = "LCURLCUR_ALM_LIN3Fr08"
    msg_id = 18
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "LCUR"
    rx_nodes = ['ALMLCURLIN3']
    sig_group_dict = {'LcuRLin3ALM7RGBL': ['LcuRLin3ALM7RGBLBlue', 'LcuRLin3ALM7RGBLDayOrNightSts', 'LcuRLin3ALM7RGBLGreen', 'LcuRLin3ALM7RGBLLuminance', 'LcuRLin3ALM7RGBLRed']}
    sig_group_dataid_dict = {}

    class LcuRLin3ALM7RGBLBlue:
        sig_name = "LcuRLin3ALM7RGBLBlue"
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

    class LcuRLin3ALM7RGBLRed:
        sig_name = "LcuRLin3ALM7RGBLRed"
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

    class LcuRLin3ALM7RGBLDayOrNightSts:
        sig_name = "LcuRLin3ALM7RGBLDayOrNightSts"
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

    class LcuRLin3ALM7RGBLGreen:
        sig_name = "LcuRLin3ALM7RGBLGreen"
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

    class LcuRLin3ALM7RGBLLuminance:
        sig_name = "LcuRLin3ALM7RGBLLuminance"
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


class ALMLCURLIN3LCUR_ALM_LIN3Fr02:
    msg_name = "ALMLCURLIN3LCUR_ALM_LIN3Fr02"
    msg_id = 1
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 1
    tx_node = "ALMLCURLIN3"
    rx_nodes = ['LCUR']
    sig_group_dict = {'LcuRLin3ALM1Failr': ['LcuRLin3ALM1FailrLEDSts', 'LcuRLin3ALM1FailrTmpSts', 'LcuRLin3ALM1FailrVltSts']}
    sig_group_dataid_dict = {}

    class LcuRLin3ALM1FailrLEDSts:
        sig_name = "LcuRLin3ALM1FailrLEDSts"
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

    class LcuRLin3ALM1FailrVltSts:
        sig_name = "LcuRLin3ALM1FailrVltSts"
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

    class LcuRLin3ALM1FailrTmpSts:
        sig_name = "LcuRLin3ALM1FailrTmpSts"
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


class ALMLCURLIN3LCUR_ALM_LIN3Fr07:
    msg_name = "ALMLCURLIN3LCUR_ALM_LIN3Fr07"
    msg_id = 6
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 1
    tx_node = "ALMLCURLIN3"
    rx_nodes = ['LCUR']
    sig_group_dict = {'LcuRLin3ALM6Failr': ['LcuRLin3ALM6FailrLEDSts', 'LcuRLin3ALM6FailrTmpSts', 'LcuRLin3ALM6FailrVltSts']}
    sig_group_dataid_dict = {}

    class LcuRLin3ALM6FailrTmpSts:
        sig_name = "LcuRLin3ALM6FailrTmpSts"
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

    class LcuRLin3ALM6FailrLEDSts:
        sig_name = "LcuRLin3ALM6FailrLEDSts"
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

    class LcuRLin3ALM6FailrVltSts:
        sig_name = "LcuRLin3ALM6FailrVltSts"
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


class ALMLCURLIN3LCUR_ALM_LIN3Fr04:
    msg_name = "ALMLCURLIN3LCUR_ALM_LIN3Fr04"
    msg_id = 3
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 1
    tx_node = "ALMLCURLIN3"
    rx_nodes = ['LCUR']
    sig_group_dict = {'LcuRLin3ALM3Failr': ['LcuRLin3ALM3FailrLEDSts', 'LcuRLin3ALM3FailrTmpSts', 'LcuRLin3ALM3FailrVltSts']}
    sig_group_dataid_dict = {}

    class LcuRLin3ALM3FailrLEDSts:
        sig_name = "LcuRLin3ALM3FailrLEDSts"
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

    class LcuRLin3ALM3FailrVltSts:
        sig_name = "LcuRLin3ALM3FailrVltSts"
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

    class LcuRLin3ALM3FailrTmpSts:
        sig_name = "LcuRLin3ALM3FailrTmpSts"
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


class ALMLCURLIN3LCUR_ALM_LIN3Fr09:
    msg_name = "ALMLCURLIN3LCUR_ALM_LIN3Fr09"
    msg_id = 8
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 1
    tx_node = "ALMLCURLIN3"
    rx_nodes = ['LCUR']
    sig_group_dict = {'LcuRLin3ALM8Failr': ['LcuRLin3ALM8FailrLEDSts', 'LcuRLin3ALM8FailrTmpSts', 'LcuRLin3ALM8FailrVltSts']}
    sig_group_dataid_dict = {}

    class LcuRLin3ALM8FailrLEDSts:
        sig_name = "LcuRLin3ALM8FailrLEDSts"
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

    class LcuRLin3ALM8FailrTmpSts:
        sig_name = "LcuRLin3ALM8FailrTmpSts"
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

    class LcuRLin3ALM8FailrVltSts:
        sig_name = "LcuRLin3ALM8FailrVltSts"
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


class ALMLCURLIN3LCUR_ALM_LIN3Fr10:
    msg_name = "ALMLCURLIN3LCUR_ALM_LIN3Fr10"
    msg_id = 9
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 1
    tx_node = "ALMLCURLIN3"
    rx_nodes = ['LCUR']
    sig_group_dict = {'LcuRLin3ALM9Failr': ['LcuRLin3ALM9FailrLEDSts', 'LcuRLin3ALM9FailrTmpSts', 'LcuRLin3ALM9FailrVltSts']}
    sig_group_dataid_dict = {}

    class LcuRLin3ALM9FailrVltSts:
        sig_name = "LcuRLin3ALM9FailrVltSts"
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

    class LcuRLin3ALM9FailrTmpSts:
        sig_name = "LcuRLin3ALM9FailrTmpSts"
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

    class LcuRLin3ALM9FailrLEDSts:
        sig_name = "LcuRLin3ALM9FailrLEDSts"
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


class ALMToLCURLCURALMLIN3RespFrame:
    msg_name = "ALMToLCURLCURALMLIN3RespFrame"
    msg_id = 61
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "ALMLCURLIN3"
    rx_nodes = ['LCUR']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class ALMLCURLIN3LCUR_ALM_LIN3Fr11:
    msg_name = "ALMLCURLIN3LCUR_ALM_LIN3Fr11"
    msg_id = 10
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 1
    tx_node = "ALMLCURLIN3"
    rx_nodes = ['LCUR']
    sig_group_dict = {'LcuRLin3ALM10Failr': ['LcuRLin3ALM10FailrLEDSts', 'LcuRLin3ALM10FailrTmpSts', 'LcuRLin3ALM10FailrVltSts']}
    sig_group_dataid_dict = {}

    class LcuRLin3ALM10FailrTmpSts:
        sig_name = "LcuRLin3ALM10FailrTmpSts"
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

    class LcuRLin3ALM10FailrVltSts:
        sig_name = "LcuRLin3ALM10FailrVltSts"
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

    class LcuRLin3ALM10FailrLEDSts:
        sig_name = "LcuRLin3ALM10FailrLEDSts"
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


class LCURToALMLCURALMLIN3ReqFrame:
    msg_name = "LCURToALMLCURALMLIN3ReqFrame"
    msg_id = 60
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "LCUR"
    rx_nodes = ['ALMLCURLIN3']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class ALMLCURLIN3LCUR_ALM_LIN3Fr05:
    msg_name = "ALMLCURLIN3LCUR_ALM_LIN3Fr05"
    msg_id = 4
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 1
    tx_node = "ALMLCURLIN3"
    rx_nodes = ['LCUR']
    sig_group_dict = {'LcuRLin3ALM4Failr': ['LcuRLin3ALM4FailrLEDSts', 'LcuRLin3ALM4FailrTmpSts', 'LcuRLin3ALM4FailrVltSts']}
    sig_group_dataid_dict = {}

    class LcuRLin3ALM4FailrVltSts:
        sig_name = "LcuRLin3ALM4FailrVltSts"
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

    class LcuRLin3ALM4FailrLEDSts:
        sig_name = "LcuRLin3ALM4FailrLEDSts"
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

    class LcuRLin3ALM4FailrTmpSts:
        sig_name = "LcuRLin3ALM4FailrTmpSts"
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


class LCURLCUR_ALM_LIN3Fr04:
    msg_name = "LCURLCUR_ALM_LIN3Fr04"
    msg_id = 14
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "LCUR"
    rx_nodes = ['ALMLCURLIN3']
    sig_group_dict = {'LcuRLin3ALM3RGBL': ['LcuRLin3ALM3RGBLBlue', 'LcuRLin3ALM3RGBLDayOrNightSts', 'LcuRLin3ALM3RGBLGreen', 'LcuRLin3ALM3RGBLLuminance', 'LcuRLin3ALM3RGBLRed']}
    sig_group_dataid_dict = {}

    class LcuRLin3ALM3RGBLBlue:
        sig_name = "LcuRLin3ALM3RGBLBlue"
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

    class LcuRLin3ALM3RGBLLuminance:
        sig_name = "LcuRLin3ALM3RGBLLuminance"
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

    class LcuRLin3ALM3RGBLGreen:
        sig_name = "LcuRLin3ALM3RGBLGreen"
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

    class LcuRLin3ALM3RGBLRed:
        sig_name = "LcuRLin3ALM3RGBLRed"
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

    class LcuRLin3ALM3RGBLDayOrNightSts:
        sig_name = "LcuRLin3ALM3RGBLDayOrNightSts"
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


class LCURLCUR_ALM_LIN3Fr09:
    msg_name = "LCURLCUR_ALM_LIN3Fr09"
    msg_id = 19
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "LCUR"
    rx_nodes = ['ALMLCURLIN3']
    sig_group_dict = {'LcuRLin3ALM8RGBL': ['LcuRLin3ALM8RGBLBlue', 'LcuRLin3ALM8RGBLDayOrNightSts', 'LcuRLin3ALM8RGBLGreen', 'LcuRLin3ALM8RGBLLuminance', 'LcuRLin3ALM8RGBLRed']}
    sig_group_dataid_dict = {}

    class LcuRLin3ALM8RGBLBlue:
        sig_name = "LcuRLin3ALM8RGBLBlue"
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

    class LcuRLin3ALM8RGBLDayOrNightSts:
        sig_name = "LcuRLin3ALM8RGBLDayOrNightSts"
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

    class LcuRLin3ALM8RGBLGreen:
        sig_name = "LcuRLin3ALM8RGBLGreen"
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

    class LcuRLin3ALM8RGBLLuminance:
        sig_name = "LcuRLin3ALM8RGBLLuminance"
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

    class LcuRLin3ALM8RGBLRed:
        sig_name = "LcuRLin3ALM8RGBLRed"
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


class ALMLCURLIN3LCUR_ALM_LIN3Fr06:
    msg_name = "ALMLCURLIN3LCUR_ALM_LIN3Fr06"
    msg_id = 5
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 1
    tx_node = "ALMLCURLIN3"
    rx_nodes = ['LCUR']
    sig_group_dict = {'LcuRLin3ALM5Failr': ['LcuRLin3ALM5FailrLEDSts', 'LcuRLin3ALM5FailrTmpSts', 'LcuRLin3ALM5FailrVltSts']}
    sig_group_dataid_dict = {}

    class LcuRLin3ALM5FailrLEDSts:
        sig_name = "LcuRLin3ALM5FailrLEDSts"
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

    class LcuRLin3ALM5FailrVltSts:
        sig_name = "LcuRLin3ALM5FailrVltSts"
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

    class LcuRLin3ALM5FailrTmpSts:
        sig_name = "LcuRLin3ALM5FailrTmpSts"
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


class LCURLCUR_ALM_LIN3Fr03:
    msg_name = "LCURLCUR_ALM_LIN3Fr03"
    msg_id = 13
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "LCUR"
    rx_nodes = ['ALMLCURLIN3']
    sig_group_dict = {'LcuRLin3ALM2RGBL': ['LcuRLin3ALM2RGBLBlue', 'LcuRLin3ALM2RGBLDayOrNightSts', 'LcuRLin3ALM2RGBLGreen', 'LcuRLin3ALM2RGBLLuminance', 'LcuRLin3ALM2RGBLRed']}
    sig_group_dataid_dict = {}

    class LcuRLin3ALM2RGBLGreen:
        sig_name = "LcuRLin3ALM2RGBLGreen"
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

    class LcuRLin3ALM2RGBLRed:
        sig_name = "LcuRLin3ALM2RGBLRed"
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

    class LcuRLin3ALM2RGBLBlue:
        sig_name = "LcuRLin3ALM2RGBLBlue"
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

    class LcuRLin3ALM2RGBLLuminance:
        sig_name = "LcuRLin3ALM2RGBLLuminance"
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

    class LcuRLin3ALM2RGBLDayOrNightSts:
        sig_name = "LcuRLin3ALM2RGBLDayOrNightSts"
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


class LCURLCUR_ALM_LIN3Fr10:
    msg_name = "LCURLCUR_ALM_LIN3Fr10"
    msg_id = 20
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "LCUR"
    rx_nodes = ['ALMLCURLIN3']
    sig_group_dict = {'LcuRLin3ALM9RGBL': ['LcuRLin3ALM9RGBLBlue', 'LcuRLin3ALM9RGBLDayOrNightSts', 'LcuRLin3ALM9RGBLGreen', 'LcuRLin3ALM9RGBLLuminance', 'LcuRLin3ALM9RGBLRed']}
    sig_group_dataid_dict = {}

    class LcuRLin3ALM9RGBLDayOrNightSts:
        sig_name = "LcuRLin3ALM9RGBLDayOrNightSts"
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

    class LcuRLin3ALM9RGBLLuminance:
        sig_name = "LcuRLin3ALM9RGBLLuminance"
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

    class LcuRLin3ALM9RGBLRed:
        sig_name = "LcuRLin3ALM9RGBLRed"
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

    class LcuRLin3ALM9RGBLGreen:
        sig_name = "LcuRLin3ALM9RGBLGreen"
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

    class LcuRLin3ALM9RGBLBlue:
        sig_name = "LcuRLin3ALM9RGBLBlue"
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


class LCURLCUR_ALM_LIN3Fr11:
    msg_name = "LCURLCUR_ALM_LIN3Fr11"
    msg_id = 21
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "LCUR"
    rx_nodes = ['ALMLCURLIN3']
    sig_group_dict = {'LcuRLin3ALM10RGBL': ['LcuRLin3ALM10RGBLBlue', 'LcuRLin3ALM10RGBLDayOrNightSts', 'LcuRLin3ALM10RGBLGreen', 'LcuRLin3ALM10RGBLLuminance', 'LcuRLin3ALM10RGBLRed']}
    sig_group_dataid_dict = {}

    class LcuRLin3ALM10RGBLGreen:
        sig_name = "LcuRLin3ALM10RGBLGreen"
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

    class LcuRLin3ALM10RGBLRed:
        sig_name = "LcuRLin3ALM10RGBLRed"
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

    class LcuRLin3ALM10RGBLDayOrNightSts:
        sig_name = "LcuRLin3ALM10RGBLDayOrNightSts"
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

    class LcuRLin3ALM10RGBLLuminance:
        sig_name = "LcuRLin3ALM10RGBLLuminance"
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

    class LcuRLin3ALM10RGBLBlue:
        sig_name = "LcuRLin3ALM10RGBLBlue"
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


class LCURLCUR_ALM_LIN3Fr02:
    msg_name = "LCURLCUR_ALM_LIN3Fr02"
    msg_id = 12
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "LCUR"
    rx_nodes = ['ALMLCURLIN3']
    sig_group_dict = {'LcuRLin3ALM1RGBL': ['LcuRLin3ALM1RGBLBlue', 'LcuRLin3ALM1RGBLDayOrNightSts', 'LcuRLin3ALM1RGBLGreen', 'LcuRLin3ALM1RGBLLuminance', 'LcuRLin3ALM1RGBLRed']}
    sig_group_dataid_dict = {}

    class LcuRLin3ALM1RGBLDayOrNightSts:
        sig_name = "LcuRLin3ALM1RGBLDayOrNightSts"
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
        sig_value_table = {'DayOrNightSts_Night': 0, 'DayOrNightSts_Day': 1}
        compute_method = None
        length = 1
        startbit = 24
        byte = 3
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class LcuRLin3ALM1RGBLGreen:
        sig_name = "LcuRLin3ALM1RGBLGreen"
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

    class LcuRLin3ALM1RGBLLuminance:
        sig_name = "LcuRLin3ALM1RGBLLuminance"
        sig_start_bit = 25
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
        startbit = 25
        byte = 3
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class LcuRLin3ALM1RGBLRed:
        sig_name = "LcuRLin3ALM1RGBLRed"
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

    class LcuRLin3ALM1RGBLBlue:
        sig_name = "LcuRLin3ALM1RGBLBlue"
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


class ALMLCURLIN3LCUR_ALM_LIN3Fr03:
    msg_name = "ALMLCURLIN3LCUR_ALM_LIN3Fr03"
    msg_id = 2
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 1
    tx_node = "ALMLCURLIN3"
    rx_nodes = ['LCUR']
    sig_group_dict = {'LcuRLin3ALM2Failr': ['LcuRLin3ALM2FailrLEDSts', 'LcuRLin3ALM2FailrTmpSts', 'LcuRLin3ALM2FailrVltSts']}
    sig_group_dataid_dict = {}

    class LcuRLin3ALM2FailrLEDSts:
        sig_name = "LcuRLin3ALM2FailrLEDSts"
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

    class LcuRLin3ALM2FailrTmpSts:
        sig_name = "LcuRLin3ALM2FailrTmpSts"
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

    class LcuRLin3ALM2FailrVltSts:
        sig_name = "LcuRLin3ALM2FailrVltSts"
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


class LCURLCUR_ALM_LIN3Fr05:
    msg_name = "LCURLCUR_ALM_LIN3Fr05"
    msg_id = 15
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "LCUR"
    rx_nodes = ['ALMLCURLIN3']
    sig_group_dict = {'LcuRLin3ALM4RGBL': ['LcuRLin3ALM4RGBLBlue', 'LcuRLin3ALM4RGBLDayOrNightSts', 'LcuRLin3ALM4RGBLGreen', 'LcuRLin3ALM4RGBLLuminance', 'LcuRLin3ALM4RGBLRed']}
    sig_group_dataid_dict = {}

    class LcuRLin3ALM4RGBLLuminance:
        sig_name = "LcuRLin3ALM4RGBLLuminance"
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

    class LcuRLin3ALM4RGBLGreen:
        sig_name = "LcuRLin3ALM4RGBLGreen"
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

    class LcuRLin3ALM4RGBLBlue:
        sig_name = "LcuRLin3ALM4RGBLBlue"
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

    class LcuRLin3ALM4RGBLRed:
        sig_name = "LcuRLin3ALM4RGBLRed"
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

    class LcuRLin3ALM4RGBLDayOrNightSts:
        sig_name = "LcuRLin3ALM4RGBLDayOrNightSts"
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


class LCURLCUR_ALM_LIN3Fr07:
    msg_name = "LCURLCUR_ALM_LIN3Fr07"
    msg_id = 17
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "LCUR"
    rx_nodes = ['ALMLCURLIN3']
    sig_group_dict = {'LcuRLin3ALM6RGBL': ['LcuRLin3ALM6RGBLBlue', 'LcuRLin3ALM6RGBLDayOrNightSts', 'LcuRLin3ALM6RGBLGreen', 'LcuRLin3ALM6RGBLLuminance', 'LcuRLin3ALM6RGBLRed']}
    sig_group_dataid_dict = {}

    class LcuRLin3ALM6RGBLRed:
        sig_name = "LcuRLin3ALM6RGBLRed"
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

    class LcuRLin3ALM6RGBLBlue:
        sig_name = "LcuRLin3ALM6RGBLBlue"
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

    class LcuRLin3ALM6RGBLDayOrNightSts:
        sig_name = "LcuRLin3ALM6RGBLDayOrNightSts"
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

    class LcuRLin3ALM6RGBLLuminance:
        sig_name = "LcuRLin3ALM6RGBLLuminance"
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

    class LcuRLin3ALM6RGBLGreen:
        sig_name = "LcuRLin3ALM6RGBLGreen"
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


class LCURLCUR_ALM_LIN3Fr06:
    msg_name = "LCURLCUR_ALM_LIN3Fr06"
    msg_id = 16
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "LCUR"
    rx_nodes = ['ALMLCURLIN3']
    sig_group_dict = {'LcuRLin3ALM5RGBL': ['LcuRLin3ALM5RGBLBlue', 'LcuRLin3ALM5RGBLDayOrNightSts', 'LcuRLin3ALM5RGBLGreen', 'LcuRLin3ALM5RGBLLuminance', 'LcuRLin3ALM5RGBLRed']}
    sig_group_dataid_dict = {}

    class LcuRLin3ALM5RGBLBlue:
        sig_name = "LcuRLin3ALM5RGBLBlue"
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

    class LcuRLin3ALM5RGBLLuminance:
        sig_name = "LcuRLin3ALM5RGBLLuminance"
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

    class LcuRLin3ALM5RGBLRed:
        sig_name = "LcuRLin3ALM5RGBLRed"
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

    class LcuRLin3ALM5RGBLGreen:
        sig_name = "LcuRLin3ALM5RGBLGreen"
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

    class LcuRLin3ALM5RGBLDayOrNightSts:
        sig_name = "LcuRLin3ALM5RGBLDayOrNightSts"
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


class ALMLCURLIN3LCUR_ALM_LIN3Fr08:
    msg_name = "ALMLCURLIN3LCUR_ALM_LIN3Fr08"
    msg_id = 7
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 1
    tx_node = "ALMLCURLIN3"
    rx_nodes = ['LCUR']
    sig_group_dict = {'LcuRLin3ALM7Failr': ['LcuRLin3ALM7FailrLEDSts', 'LcuRLin3ALM7FailrTmpSts', 'LcuRLin3ALM7FailrVltSts']}
    sig_group_dataid_dict = {}

    class LcuRLin3ALM7FailrVltSts:
        sig_name = "LcuRLin3ALM7FailrVltSts"
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

    class LcuRLin3ALM7FailrLEDSts:
        sig_name = "LcuRLin3ALM7FailrLEDSts"
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

    class LcuRLin3ALM7FailrTmpSts:
        sig_name = "LcuRLin3ALM7FailrTmpSts"
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


