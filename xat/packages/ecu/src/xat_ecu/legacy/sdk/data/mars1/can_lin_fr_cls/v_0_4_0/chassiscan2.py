class BgmChas2Fr01:
    msg_name = "BgmChas2Fr01"
    msg_id = 96
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class ModReqOfDampr:
        sig_name = "ModReqOfDampr"
        sig_start_bit = 2
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Level1': 0, 'Level2': 1, 'Level3': 2, 'Level4': 3, 'Reserved1': 4, 'Reserved2': 5, 'Reserved3': 6, 'Reserved4': 7}
        compute_method = None
        length = 3
        startbit = 2
        byte = 0
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class DrvModSet:
        sig_name = "DrvModSet"
        sig_start_bit = 7
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DrvModReqType1_Undefd': 0, 'DrvModReqType1_ECO': 1, 'DrvModReqType1_Comfort_Normal': 2, 'DrvModReqType1_Dynamic_Sport': 3, 'DrvModReqType1_Reserved': 8, 'DrvModReqType1_Offroad_CrossTerrain': 5, 'DrvModReqType1_Adaptive': 6, 'DrvModReqType1_Race': 7, 'DrvModReqType1_ECO_PLUS': 9, 'DrvModReqType1_Power': 10, 'DrvModReqType1_Snow': 11, 'DrvModReqType1_Sand': 12, 'DrvModReqType1_Mud': 13, 'DrvModReqType1_Rock': 14, 'DrvModReqType1_Err': 15}
        compute_method = None
        length = 4
        startbit = 7
        byte = 0
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4


class BgmChassisCAN2NmFr:
    msg_name = "BgmChassisCAN2NmFr"
    msg_id = 1281
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []


class EcmChassisCAN2NmFr:
    msg_name = "EcmChassisCAN2NmFr"
    msg_id = 1311
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']


