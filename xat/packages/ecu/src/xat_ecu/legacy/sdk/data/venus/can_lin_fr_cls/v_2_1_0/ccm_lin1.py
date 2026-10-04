lin_scheduleTable = {'Ccm_Lin1ScheduleTable1_CCM_LIN1': [(0, 'HbmfCcm_Lin1Fr01', 0.015)], 'Ccm_Lin1_DiagRequestSchedule01': [(0, 'DiagRequest5', 0.015)], 'Ccm_Lin1_DiagResponseSchedule01': [(0, 'DiagResponse5', 0.015)]}


class HbmfCcm_Lin1Fr01:
    msg_name = "HbmfCcm_Lin1Fr01"
    msg_id = 50
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "ETC"
    rx_nodes = ['CCM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HvacFanSts3HvacFanBattU:
        sig_name = "HvacFanSts3HvacFanBattU"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 40
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b00000011, 0b11111100, 2, 0)]

    class HvacFanSts3HvacFanSpdFd:
        sig_name = "HvacFanSts3HvacFanSpdFd"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 20
        sig_value_offset = 300
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

    class HvacFanSts3HvacFanBattI:
        sig_name = "HvacFanSts3HvacFanBattI"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.15
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


class DiagResponse5:
    msg_name = "DiagResponse5"
    msg_id = 61
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['CCM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class DiagRequest5:
    msg_name = "DiagRequest5"
    msg_id = 60
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CCM"
    rx_nodes = []
    sig_group_dict = {}
    sig_group_dataid_dict = {}


