lin_scheduleTable = {'LCUR_ALM_LIN2_DiagSchedule01': [(0, 'LCURToALMLCURALMLIN2ReqFrame', 0.015), (1, 'ALMToLCURLCURALMLIN2RespFrame', 0.015)], 'LCUR_ALM_LIN2Schedule01_LCUR_ALM_LIN2': [(0, 'LCURLCUR_ALM_LIN2Fr02', 0.01), (1, 'LCURLCUR_ALM_LIN2Fr03', 0.01), (2, 'LCURLCUR_ALM_LIN2Fr04', 0.01), (3, 'LCURLCUR_ALM_LIN2Fr05', 0.01), (4, 'LCURLCUR_ALM_LIN2Fr06', 0.01), (5, 'LCURLCUR_ALM_LIN2Fr07', 0.01), (6, 'LCURLCUR_ALM_LIN2Fr08', 0.01), (7, 'LCURLCUR_ALM_LIN2Fr09', 0.01), (8, 'LCURLCUR_ALM_LIN2Fr10', 0.01), (9, 'LCURLCUR_ALM_LIN2Fr11', 0.01)], 'LCUR_ALM_LIN2_ScheduleFailrSts_LCUR_ALM_LIN2': [(0, 'ALMLCURLIN2LCUR_ALM_LIN2Fr02', 0.005), (1, 'ALMLCURLIN2LCUR_ALM_LIN2Fr03', 0.005), (2, 'ALMLCURLIN2LCUR_ALM_LIN2Fr04', 0.005), (3, 'ALMLCURLIN2LCUR_ALM_LIN2Fr05', 0.005), (4, 'ALMLCURLIN2LCUR_ALM_LIN2Fr06', 0.005), (5, 'ALMLCURLIN2LCUR_ALM_LIN2Fr07', 0.005), (6, 'ALMLCURLIN2LCUR_ALM_LIN2Fr08', 0.005), (7, 'ALMLCURLIN2LCUR_ALM_LIN2Fr09', 0.005), (8, 'ALMLCURLIN2LCUR_ALM_LIN2Fr10', 0.005), (9, 'ALMLCURLIN2LCUR_ALM_LIN2Fr11', 0.005)]}


class LCURLCUR_ALM_LIN2Fr04:
    msg_name = "LCURLCUR_ALM_LIN2Fr04"
    msg_id = 14
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "LCUR"
    rx_nodes = ['ALMLCURLIN2']
    sig_group_dict = {'LcuRLin2ALM3RGBL': ['LcuRLin2ALM3RGBLBlue', 'LcuRLin2ALM3RGBLDayOrNightSts', 'LcuRLin2ALM3RGBLGreen', 'LcuRLin2ALM3RGBLLuminance', 'LcuRLin2ALM3RGBLRed']}
    sig_group_dataid_dict = {}

    class LcuRLin2ALM3RGBLDayOrNightSts:
        sig_name = "LcuRLin2ALM3RGBLDayOrNightSts"
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

    class LcuRLin2ALM3RGBLGreen:
        sig_name = "LcuRLin2ALM3RGBLGreen"
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

    class LcuRLin2ALM3RGBLRed:
        sig_name = "LcuRLin2ALM3RGBLRed"
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

    class LcuRLin2ALM3RGBLLuminance:
        sig_name = "LcuRLin2ALM3RGBLLuminance"
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

    class LcuRLin2ALM3RGBLBlue:
        sig_name = "LcuRLin2ALM3RGBLBlue"
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


class ALMLCURLIN2LCUR_ALM_LIN2Fr05:
    msg_name = "ALMLCURLIN2LCUR_ALM_LIN2Fr05"
    msg_id = 4
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 1
    tx_node = "ALMLCURLIN2"
    rx_nodes = ['LCUR']
    sig_group_dict = {'LcuRLin2ALM4Failr': ['LcuRLin2ALM4FailrLEDSts', 'LcuRLin2ALM4FailrTmpSts', 'LcuRLin2ALM4FailrVltSts']}
    sig_group_dataid_dict = {}

    class LcuRLin2ALM4FailrVltSts:
        sig_name = "LcuRLin2ALM4FailrVltSts"
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

    class LcuRLin2ALM4FailrTmpSts:
        sig_name = "LcuRLin2ALM4FailrTmpSts"
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

    class LcuRLin2ALM4FailrLEDSts:
        sig_name = "LcuRLin2ALM4FailrLEDSts"
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


class LCURLCUR_ALM_LIN2Fr03:
    msg_name = "LCURLCUR_ALM_LIN2Fr03"
    msg_id = 13
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "LCUR"
    rx_nodes = ['ALMLCURLIN2']
    sig_group_dict = {'LcuRLin2ALM2RGBL': ['LcuRLin2ALM2RGBLBlue', 'LcuRLin2ALM2RGBLDayOrNightSts', 'LcuRLin2ALM2RGBLGreen', 'LcuRLin2ALM2RGBLLuminance', 'LcuRLin2ALM2RGBLRed']}
    sig_group_dataid_dict = {}

    class LcuRLin2ALM2RGBLBlue:
        sig_name = "LcuRLin2ALM2RGBLBlue"
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

    class LcuRLin2ALM2RGBLGreen:
        sig_name = "LcuRLin2ALM2RGBLGreen"
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

    class LcuRLin2ALM2RGBLDayOrNightSts:
        sig_name = "LcuRLin2ALM2RGBLDayOrNightSts"
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

    class LcuRLin2ALM2RGBLLuminance:
        sig_name = "LcuRLin2ALM2RGBLLuminance"
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

    class LcuRLin2ALM2RGBLRed:
        sig_name = "LcuRLin2ALM2RGBLRed"
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


class LCURLCUR_ALM_LIN2Fr02:
    msg_name = "LCURLCUR_ALM_LIN2Fr02"
    msg_id = 12
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "LCUR"
    rx_nodes = ['ALMLCURLIN2']
    sig_group_dict = {'LcuRLin2ALM1RGBL': ['LcuRLin2ALM1RGBLBlue', 'LcuRLin2ALM1RGBLDayOrNightSts', 'LcuRLin2ALM1RGBLGreen', 'LcuRLin2ALM1RGBLLuminance', 'LcuRLin2ALM1RGBLRed']}
    sig_group_dataid_dict = {}

    class LcuRLin2ALM1RGBLLuminance:
        sig_name = "LcuRLin2ALM1RGBLLuminance"
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

    class LcuRLin2ALM1RGBLDayOrNightSts:
        sig_name = "LcuRLin2ALM1RGBLDayOrNightSts"
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

    class LcuRLin2ALM1RGBLGreen:
        sig_name = "LcuRLin2ALM1RGBLGreen"
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

    class LcuRLin2ALM1RGBLRed:
        sig_name = "LcuRLin2ALM1RGBLRed"
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

    class LcuRLin2ALM1RGBLBlue:
        sig_name = "LcuRLin2ALM1RGBLBlue"
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


class LCURToALMLCURALMLIN2ReqFrame:
    msg_name = "LCURToALMLCURALMLIN2ReqFrame"
    msg_id = 60
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "LCUR"
    rx_nodes = ['ALMLCURLIN2']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class ALMLCURLIN2LCUR_ALM_LIN2Fr04:
    msg_name = "ALMLCURLIN2LCUR_ALM_LIN2Fr04"
    msg_id = 3
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 1
    tx_node = "ALMLCURLIN2"
    rx_nodes = ['LCUR']
    sig_group_dict = {'LcuRLin2ALM3Failr': ['LcuRLin2ALM3FailrLEDSts', 'LcuRLin2ALM3FailrTmpSts', 'LcuRLin2ALM3FailrVltSts']}
    sig_group_dataid_dict = {}

    class LcuRLin2ALM3FailrTmpSts:
        sig_name = "LcuRLin2ALM3FailrTmpSts"
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

    class LcuRLin2ALM3FailrVltSts:
        sig_name = "LcuRLin2ALM3FailrVltSts"
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

    class LcuRLin2ALM3FailrLEDSts:
        sig_name = "LcuRLin2ALM3FailrLEDSts"
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


class ALMLCURLIN2LCUR_ALM_LIN2Fr07:
    msg_name = "ALMLCURLIN2LCUR_ALM_LIN2Fr07"
    msg_id = 6
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 1
    tx_node = "ALMLCURLIN2"
    rx_nodes = ['LCUR']
    sig_group_dict = {'LcuRLin2ALM6Failr': ['LcuRLin2ALM6FailrLEDSts', 'LcuRLin2ALM6FailrTmpSts', 'LcuRLin2ALM6FailrVltSts']}
    sig_group_dataid_dict = {}

    class LcuRLin2ALM6FailrLEDSts:
        sig_name = "LcuRLin2ALM6FailrLEDSts"
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

    class LcuRLin2ALM6FailrVltSts:
        sig_name = "LcuRLin2ALM6FailrVltSts"
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

    class LcuRLin2ALM6FailrTmpSts:
        sig_name = "LcuRLin2ALM6FailrTmpSts"
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


class ALMLCURLIN2LCUR_ALM_LIN2Fr03:
    msg_name = "ALMLCURLIN2LCUR_ALM_LIN2Fr03"
    msg_id = 2
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 1
    tx_node = "ALMLCURLIN2"
    rx_nodes = ['LCUR']
    sig_group_dict = {'LcuRLin2ALM2Failr': ['LcuRLin2ALM2FailrLEDSts', 'LcuRLin2ALM2FailrTmpSts', 'LcuRLin2ALM2FailrVltSts']}
    sig_group_dataid_dict = {}

    class LcuRLin2ALM2FailrTmpSts:
        sig_name = "LcuRLin2ALM2FailrTmpSts"
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

    class LcuRLin2ALM2FailrVltSts:
        sig_name = "LcuRLin2ALM2FailrVltSts"
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

    class LcuRLin2ALM2FailrLEDSts:
        sig_name = "LcuRLin2ALM2FailrLEDSts"
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


class ALMLCURLIN2LCUR_ALM_LIN2Fr02:
    msg_name = "ALMLCURLIN2LCUR_ALM_LIN2Fr02"
    msg_id = 1
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 1
    tx_node = "ALMLCURLIN2"
    rx_nodes = ['LCUR']
    sig_group_dict = {'LcuRLin2ALM1Failr': ['LcuRLin2ALM1FailrLEDSts', 'LcuRLin2ALM1FailrTmpSts', 'LcuRLin2ALM1FailrVltSts']}
    sig_group_dataid_dict = {}

    class LcuRLin2ALM1FailrLEDSts:
        sig_name = "LcuRLin2ALM1FailrLEDSts"
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

    class LcuRLin2ALM1FailrVltSts:
        sig_name = "LcuRLin2ALM1FailrVltSts"
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

    class LcuRLin2ALM1FailrTmpSts:
        sig_name = "LcuRLin2ALM1FailrTmpSts"
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


class LCURLCUR_ALM_LIN2Fr05:
    msg_name = "LCURLCUR_ALM_LIN2Fr05"
    msg_id = 15
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "LCUR"
    rx_nodes = ['ALMLCURLIN2']
    sig_group_dict = {'LcuRLin2ALM4RGBL': ['LcuRLin2ALM4RGBLBlue', 'LcuRLin2ALM4RGBLDayOrNightSts', 'LcuRLin2ALM4RGBLGreen', 'LcuRLin2ALM4RGBLLuminance', 'LcuRLin2ALM4RGBLRed']}
    sig_group_dataid_dict = {}

    class LcuRLin2ALM4RGBLRed:
        sig_name = "LcuRLin2ALM4RGBLRed"
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

    class LcuRLin2ALM4RGBLBlue:
        sig_name = "LcuRLin2ALM4RGBLBlue"
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

    class LcuRLin2ALM4RGBLDayOrNightSts:
        sig_name = "LcuRLin2ALM4RGBLDayOrNightSts"
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

    class LcuRLin2ALM4RGBLLuminance:
        sig_name = "LcuRLin2ALM4RGBLLuminance"
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

    class LcuRLin2ALM4RGBLGreen:
        sig_name = "LcuRLin2ALM4RGBLGreen"
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


class ALMLCURLIN2LCUR_ALM_LIN2Fr11:
    msg_name = "ALMLCURLIN2LCUR_ALM_LIN2Fr11"
    msg_id = 10
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 1
    tx_node = "ALMLCURLIN2"
    rx_nodes = ['LCUR']
    sig_group_dict = {'LcuRLin2ALM10Failr': ['LcuRLin2ALM10FailrLEDSts', 'LcuRLin2ALM10FailrTmpSts', 'LcuRLin2ALM10FailrVltSts']}
    sig_group_dataid_dict = {}

    class LcuRLin2ALM10FailrLEDSts:
        sig_name = "LcuRLin2ALM10FailrLEDSts"
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

    class LcuRLin2ALM10FailrVltSts:
        sig_name = "LcuRLin2ALM10FailrVltSts"
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

    class LcuRLin2ALM10FailrTmpSts:
        sig_name = "LcuRLin2ALM10FailrTmpSts"
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


class LCURLCUR_ALM_LIN2Fr07:
    msg_name = "LCURLCUR_ALM_LIN2Fr07"
    msg_id = 17
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "LCUR"
    rx_nodes = ['ALMLCURLIN2']
    sig_group_dict = {'LcuRLin2ALM6RGBL': ['LcuRLin2ALM6RGBLBlue', 'LcuRLin2ALM6RGBLDayOrNightSts', 'LcuRLin2ALM6RGBLGreen', 'LcuRLin2ALM6RGBLLuminance', 'LcuRLin2ALM6RGBLRed']}
    sig_group_dataid_dict = {}

    class LcuRLin2ALM6RGBLRed:
        sig_name = "LcuRLin2ALM6RGBLRed"
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

    class LcuRLin2ALM6RGBLDayOrNightSts:
        sig_name = "LcuRLin2ALM6RGBLDayOrNightSts"
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

    class LcuRLin2ALM6RGBLBlue:
        sig_name = "LcuRLin2ALM6RGBLBlue"
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

    class LcuRLin2ALM6RGBLLuminance:
        sig_name = "LcuRLin2ALM6RGBLLuminance"
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

    class LcuRLin2ALM6RGBLGreen:
        sig_name = "LcuRLin2ALM6RGBLGreen"
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


class ALMLCURLIN2LCUR_ALM_LIN2Fr09:
    msg_name = "ALMLCURLIN2LCUR_ALM_LIN2Fr09"
    msg_id = 8
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 1
    tx_node = "ALMLCURLIN2"
    rx_nodes = ['LCUR']
    sig_group_dict = {'LcuRLin2ALM8Failr': ['LcuRLin2ALM8FailrLEDSts', 'LcuRLin2ALM8FailrTmpSts', 'LcuRLin2ALM8FailrVltSts']}
    sig_group_dataid_dict = {}

    class LcuRLin2ALM8FailrLEDSts:
        sig_name = "LcuRLin2ALM8FailrLEDSts"
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

    class LcuRLin2ALM8FailrTmpSts:
        sig_name = "LcuRLin2ALM8FailrTmpSts"
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

    class LcuRLin2ALM8FailrVltSts:
        sig_name = "LcuRLin2ALM8FailrVltSts"
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


class LCURLCUR_ALM_LIN2Fr08:
    msg_name = "LCURLCUR_ALM_LIN2Fr08"
    msg_id = 18
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "LCUR"
    rx_nodes = ['ALMLCURLIN2']
    sig_group_dict = {'LcuRLin2ALM7RGBL': ['LcuRLin2ALM7RGBLBlue', 'LcuRLin2ALM7RGBLDayOrNightSts', 'LcuRLin2ALM7RGBLGreen', 'LcuRLin2ALM7RGBLLuminance', 'LcuRLin2ALM7RGBLRed']}
    sig_group_dataid_dict = {}

    class LcuRLin2ALM7RGBLGreen:
        sig_name = "LcuRLin2ALM7RGBLGreen"
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

    class LcuRLin2ALM7RGBLRed:
        sig_name = "LcuRLin2ALM7RGBLRed"
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

    class LcuRLin2ALM7RGBLDayOrNightSts:
        sig_name = "LcuRLin2ALM7RGBLDayOrNightSts"
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

    class LcuRLin2ALM7RGBLLuminance:
        sig_name = "LcuRLin2ALM7RGBLLuminance"
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

    class LcuRLin2ALM7RGBLBlue:
        sig_name = "LcuRLin2ALM7RGBLBlue"
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


class ALMLCURLIN2LCUR_ALM_LIN2Fr10:
    msg_name = "ALMLCURLIN2LCUR_ALM_LIN2Fr10"
    msg_id = 9
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 1
    tx_node = "ALMLCURLIN2"
    rx_nodes = ['LCUR']
    sig_group_dict = {'LcuRLin2ALM9Failr': ['LcuRLin2ALM9FailrLEDSts', 'LcuRLin2ALM9FailrTmpSts', 'LcuRLin2ALM9FailrVltSts']}
    sig_group_dataid_dict = {}

    class LcuRLin2ALM9FailrLEDSts:
        sig_name = "LcuRLin2ALM9FailrLEDSts"
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

    class LcuRLin2ALM9FailrTmpSts:
        sig_name = "LcuRLin2ALM9FailrTmpSts"
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

    class LcuRLin2ALM9FailrVltSts:
        sig_name = "LcuRLin2ALM9FailrVltSts"
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


class LCURLCUR_ALM_LIN2Fr10:
    msg_name = "LCURLCUR_ALM_LIN2Fr10"
    msg_id = 20
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "LCUR"
    rx_nodes = ['ALMLCURLIN2']
    sig_group_dict = {'LcuRLin2ALM9RGBL': ['LcuRLin2ALM9RGBLBlue', 'LcuRLin2ALM9RGBLDayOrNightSts', 'LcuRLin2ALM9RGBLGreen', 'LcuRLin2ALM9RGBLLuminance', 'LcuRLin2ALM9RGBLRed']}
    sig_group_dataid_dict = {}

    class LcuRLin2ALM9RGBLRed:
        sig_name = "LcuRLin2ALM9RGBLRed"
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

    class LcuRLin2ALM9RGBLBlue:
        sig_name = "LcuRLin2ALM9RGBLBlue"
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

    class LcuRLin2ALM9RGBLLuminance:
        sig_name = "LcuRLin2ALM9RGBLLuminance"
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

    class LcuRLin2ALM9RGBLGreen:
        sig_name = "LcuRLin2ALM9RGBLGreen"
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

    class LcuRLin2ALM9RGBLDayOrNightSts:
        sig_name = "LcuRLin2ALM9RGBLDayOrNightSts"
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


class ALMLCURLIN2LCUR_ALM_LIN2Fr08:
    msg_name = "ALMLCURLIN2LCUR_ALM_LIN2Fr08"
    msg_id = 7
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 1
    tx_node = "ALMLCURLIN2"
    rx_nodes = ['LCUR']
    sig_group_dict = {'LcuRLin2ALM7Failr': ['LcuRLin2ALM7FailrLEDSts', 'LcuRLin2ALM7FailrTmpSts', 'LcuRLin2ALM7FailrVltSts']}
    sig_group_dataid_dict = {}

    class LcuRLin2ALM7FailrLEDSts:
        sig_name = "LcuRLin2ALM7FailrLEDSts"
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

    class LcuRLin2ALM7FailrVltSts:
        sig_name = "LcuRLin2ALM7FailrVltSts"
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

    class LcuRLin2ALM7FailrTmpSts:
        sig_name = "LcuRLin2ALM7FailrTmpSts"
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


class LCURLCUR_ALM_LIN2Fr11:
    msg_name = "LCURLCUR_ALM_LIN2Fr11"
    msg_id = 21
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "LCUR"
    rx_nodes = ['ALMLCURLIN2']
    sig_group_dict = {'LcuRLin2ALM10RGBL': ['LcuRLin2ALM10RGBLBlue', 'LcuRLin2ALM10RGBLDayOrNightSts', 'LcuRLin2ALM10RGBLGreen', 'LcuRLin2ALM10RGBLLuminance', 'LcuRLin2ALM10RGBLRed']}
    sig_group_dataid_dict = {}

    class LcuRLin2ALM10RGBLGreen:
        sig_name = "LcuRLin2ALM10RGBLGreen"
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

    class LcuRLin2ALM10RGBLBlue:
        sig_name = "LcuRLin2ALM10RGBLBlue"
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

    class LcuRLin2ALM10RGBLDayOrNightSts:
        sig_name = "LcuRLin2ALM10RGBLDayOrNightSts"
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

    class LcuRLin2ALM10RGBLRed:
        sig_name = "LcuRLin2ALM10RGBLRed"
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

    class LcuRLin2ALM10RGBLLuminance:
        sig_name = "LcuRLin2ALM10RGBLLuminance"
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


class ALMLCURLIN2LCUR_ALM_LIN2Fr06:
    msg_name = "ALMLCURLIN2LCUR_ALM_LIN2Fr06"
    msg_id = 5
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 1
    tx_node = "ALMLCURLIN2"
    rx_nodes = ['LCUR']
    sig_group_dict = {'LcuRLin2ALM5Failr': ['LcuRLin2ALM5FailrLEDSts', 'LcuRLin2ALM5FailrTmpSts', 'LcuRLin2ALM5FailrVltSts']}
    sig_group_dataid_dict = {}

    class LcuRLin2ALM5FailrTmpSts:
        sig_name = "LcuRLin2ALM5FailrTmpSts"
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

    class LcuRLin2ALM5FailrLEDSts:
        sig_name = "LcuRLin2ALM5FailrLEDSts"
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

    class LcuRLin2ALM5FailrVltSts:
        sig_name = "LcuRLin2ALM5FailrVltSts"
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


class LCURLCUR_ALM_LIN2Fr09:
    msg_name = "LCURLCUR_ALM_LIN2Fr09"
    msg_id = 19
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "LCUR"
    rx_nodes = ['ALMLCURLIN2']
    sig_group_dict = {'LcuRLin2ALM8RGBL': ['LcuRLin2ALM8RGBLBlue', 'LcuRLin2ALM8RGBLDayOrNightSts', 'LcuRLin2ALM8RGBLGreen', 'LcuRLin2ALM8RGBLLuminance', 'LcuRLin2ALM8RGBLRed']}
    sig_group_dataid_dict = {}

    class LcuRLin2ALM8RGBLLuminance:
        sig_name = "LcuRLin2ALM8RGBLLuminance"
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

    class LcuRLin2ALM8RGBLDayOrNightSts:
        sig_name = "LcuRLin2ALM8RGBLDayOrNightSts"
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

    class LcuRLin2ALM8RGBLBlue:
        sig_name = "LcuRLin2ALM8RGBLBlue"
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

    class LcuRLin2ALM8RGBLRed:
        sig_name = "LcuRLin2ALM8RGBLRed"
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

    class LcuRLin2ALM8RGBLGreen:
        sig_name = "LcuRLin2ALM8RGBLGreen"
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


class ALMToLCURLCURALMLIN2RespFrame:
    msg_name = "ALMToLCURLCURALMLIN2RespFrame"
    msg_id = 61
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "ALMLCURLIN2"
    rx_nodes = ['LCUR']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class LCURLCUR_ALM_LIN2Fr06:
    msg_name = "LCURLCUR_ALM_LIN2Fr06"
    msg_id = 16
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "LCUR"
    rx_nodes = ['ALMLCURLIN2']
    sig_group_dict = {'LcuRLin2ALM5RGBL': ['LcuRLin2ALM5RGBLBlue', 'LcuRLin2ALM5RGBLDayOrNightSts', 'LcuRLin2ALM5RGBLGreen', 'LcuRLin2ALM5RGBLLuminance', 'LcuRLin2ALM5RGBLRed']}
    sig_group_dataid_dict = {}

    class LcuRLin2ALM5RGBLDayOrNightSts:
        sig_name = "LcuRLin2ALM5RGBLDayOrNightSts"
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

    class LcuRLin2ALM5RGBLGreen:
        sig_name = "LcuRLin2ALM5RGBLGreen"
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

    class LcuRLin2ALM5RGBLBlue:
        sig_name = "LcuRLin2ALM5RGBLBlue"
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

    class LcuRLin2ALM5RGBLRed:
        sig_name = "LcuRLin2ALM5RGBLRed"
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

    class LcuRLin2ALM5RGBLLuminance:
        sig_name = "LcuRLin2ALM5RGBLLuminance"
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


