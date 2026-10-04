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


class HbmfCcm_Lin1Fr01:
    msg_name = "HbmfCcm_Lin1Fr01"
    msg_id = 50
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 8
    tx_node = "ETC"
    rx_nodes = ['CCM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HvacFanSts3HvacFanBattU_0_HbmfCcm_Lin1SignalIPdu01:
        sig_name = "HvacFanSts3HvacFanBattU_0_HbmfCcm_Lin1SignalIPdu01"
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

    class HvacFanSts3HvacFanSpdFd_0_HbmfCcm_Lin1SignalIPdu01:
        sig_name = "HvacFanSts3HvacFanSpdFd_0_HbmfCcm_Lin1SignalIPdu01"
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

    class HvacFanSts3HvacFanBattI_0_HbmfCcm_Lin1SignalIPdu01:
        sig_name = "HvacFanSts3HvacFanBattI_0_HbmfCcm_Lin1SignalIPdu01"
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


