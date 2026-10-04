lin_scheduleTable = {'LCUL_LIN3Schedule01_LCUL_LIN3': [(0, 'LCULLCUL_LIN3Fr01', 0.015)], 'LCUL_LIN3_DiagSchedule01': [(0, 'DiagRequest2', 0.015), (1, 'DiagResponse2', 0.015)]}


class DiagResponse2:
    msg_name = "DiagResponse2"
    msg_id = 61
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['LCUL']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class DiagRequest2:
    msg_name = "DiagRequest2"
    msg_id = 60
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "LCUL"
    rx_nodes = []
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class LCULLCUL_LIN3Fr01:
    msg_name = "LCULLCUL_LIN3Fr01"
    msg_id = 0
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "LCUL"
    rx_nodes = []
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class CalforAWMPosn:
        sig_name = "CalforAWMPosn"
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
        sig_value_table = {'LrnCmd_NoCmd': 0, 'LrnCmd_ClrCmd': 1, 'LrnCmd_LrngCmd': 2, 'LrnCmd_Resd': 3}
        compute_method = None
        length = 2
        startbit = 0
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0


