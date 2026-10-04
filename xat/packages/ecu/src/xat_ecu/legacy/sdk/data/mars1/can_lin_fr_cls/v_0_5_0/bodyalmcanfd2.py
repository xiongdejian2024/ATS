class BgmToSalm7BodyALMCANFD2DiagReqFrame:
    msg_name = "BgmToSalm7BodyALMCANFD2DiagReqFrame"
    msg_id = 2003
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []


class Salm6BodyALMCANFD2NmFr:
    msg_name = "Salm6BodyALMCANFD2NmFr"
    msg_id = 1287
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "SALM6"
    rx_nodes = ['SALM5']


class Salm6ToBgmBodyALMCANFD2DiagRespFrame:
    msg_name = "Salm6ToBgmBodyALMCANFD2DiagRespFrame"
    msg_id = 1746
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "SALM6"
    rx_nodes = ['BGM']


class Salm5BodyALMCANFD2NmFr:
    msg_name = "Salm5BodyALMCANFD2NmFr"
    msg_id = 1286
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "SALM5"
    rx_nodes = ['SALM4']


class BgmToSalm4BodyALMCANFD2DiagReqFrame:
    msg_name = "BgmToSalm4BodyALMCANFD2DiagReqFrame"
    msg_id = 2000
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['SALM4']


class BgmBodyALMCANFD2NmFr:
    msg_name = "BgmBodyALMCANFD2NmFr"
    msg_id = 1281
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []


class Salm4BodyALMCANFD2NmFr:
    msg_name = "Salm4BodyALMCANFD2NmFr"
    msg_id = 1285
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "SALM4"
    rx_nodes = ['BGM']


class BgmBodyALMCANFD2Fr01:
    msg_name = "BgmBodyALMCANFD2Fr01"
    msg_id = 880
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.62
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['SALM4', 'SALM5', 'SALM6']

    class CarTiGlb_3_BgmBodyALMCANFD2SignalIPdu01:
        sig_name = "CarTiGlb_3_BgmBodyALMCANFD2SignalIPdu01"
        sig_start_bit = 31
        sig_length = 32
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 4294967295
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 32
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111111, 0b00000000, 8, 0)]

    class BkpOfDstTrvld_2_BgmBodyALMCANFD2SignalIPdu01:
        sig_name = "BkpOfDstTrvld_2_BgmBodyALMCANFD2SignalIPdu01"
        sig_start_bit = 7
        sig_length = 21
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 2000000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 21
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111000, 0b00000111, 5, 3)]


class Salm5ToBgmBodyALMCANFD2DiagRespFrame:
    msg_name = "Salm5ToBgmBodyALMCANFD2DiagRespFrame"
    msg_id = 1745
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "SALM5"
    rx_nodes = ['BGM']


class BgmToSalm6BodyALMCANFD2DiagReqFrame:
    msg_name = "BgmToSalm6BodyALMCANFD2DiagReqFrame"
    msg_id = 2002
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['SALM6']


class Salm4ToBgmBodyALMCANFD2DiagRespFrame:
    msg_name = "Salm4ToBgmBodyALMCANFD2DiagRespFrame"
    msg_id = 1744
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "SALM4"
    rx_nodes = ['BGM']


class BgmBodyALMCANFD2Fr02:
    msg_name = "BgmBodyALMCANFD2Fr02"
    msg_id = 575
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.215
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['SALM4', 'SALM5', 'SALM6']

    class VehModMngtGlbSafe1EgyLvlElecMai_2_BgmBodyALMCANFD2SignalIPdu02:
        sig_name = "VehModMngtGlbSafe1EgyLvlElecMai_2_BgmBodyALMCANFD2SignalIPdu02"
        sig_start_bit = 27
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 27
        byte = 3
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class VehBattUSysU_2_BgmBodyALMCANFD2SignalIPdu02:
        sig_name = "VehBattUSysU_2_BgmBodyALMCANFD2SignalIPdu02"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehModMngtGlbSafe1Chks_2_BgmBodyALMCANFD2SignalIPdu02:
        sig_name = "VehModMngtGlbSafe1Chks_2_BgmBodyALMCANFD2SignalIPdu02"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 23
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehModMngtGlbSafe1FltEgyCnsWdSts_2_BgmBodyALMCANFD2SignalIPdu02:
        sig_name = "VehModMngtGlbSafe1FltEgyCnsWdSts_2_BgmBodyALMCANFD2SignalIPdu02"
        sig_start_bit = 35
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltEgyCns1_NoFlt': 0, 'FltEgyCns1_Flt': 1}
        compute_method = None
        length = 1
        startbit = 35
        byte = 4
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VehBattUSysUQf_2_BgmBodyALMCANFD2SignalIPdu02:
        sig_name = "VehBattUSysUQf_2_BgmBodyALMCANFD2SignalIPdu02"
        sig_start_bit = 15
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 15
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp_2_BgmBodyALMCANFD2SignalIPdu02:
        sig_name = "VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp_2_BgmBodyALMCANFD2SignalIPdu02"
        sig_start_bit = 10
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 10
        byte = 1
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class VehModMngtGlbSafe1Cntr_2_BgmBodyALMCANFD2SignalIPdu02:
        sig_name = "VehModMngtGlbSafe1Cntr_2_BgmBodyALMCANFD2SignalIPdu02"
        sig_start_bit = 31
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 31
        byte = 3
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class VehModMngtGlbSafe1CarModSts1_2_BgmBodyALMCANFD2SignalIPdu02:
        sig_name = "VehModMngtGlbSafe1CarModSts1_2_BgmBodyALMCANFD2SignalIPdu02"
        sig_start_bit = 13
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CarModSts1_CarModNorm': 0, 'CarModSts1_CarModTrnsp': 1, 'CarModSts1_CarModFcy': 2, 'CarModSts1_CarModCrash': 3, 'CarModSts1_CarModDyno': 5}
        compute_method = None
        length = 3
        startbit = 13
        byte = 1
        mask = 0b00111000
        unmask = 0b11000111
        shift = 3

    class VehModMngtGlbSafe1UsgModSts_2_BgmBodyALMCANFD2SignalIPdu02:
        sig_name = "VehModMngtGlbSafe1UsgModSts_2_BgmBodyALMCANFD2SignalIPdu02"
        sig_start_bit = 55
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 13
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'UsgModSts1_UsgModAbdnd': 0, 'UsgModSts1_UsgModInActv': 1, 'UsgModSts1_UsgModCnvinc': 2, 'UsgModSts1_UsgModActv': 11, 'UsgModSts1_UsgModDrvg': 13}
        compute_method = None
        length = 4
        startbit = 55
        byte = 6
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class VehModMngtGlbSafe1EgyLvlElecSubtyp_2_BgmBodyALMCANFD2SignalIPdu02:
        sig_name = "VehModMngtGlbSafe1EgyLvlElecSubtyp_2_BgmBodyALMCANFD2SignalIPdu02"
        sig_start_bit = 39
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 39
        byte = 4
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class VehModMngtGlbSafe1PwrLvlElecSubtyp_2_BgmBodyALMCANFD2SignalIPdu02:
        sig_name = "VehModMngtGlbSafe1PwrLvlElecSubtyp_2_BgmBodyALMCANFD2SignalIPdu02"
        sig_start_bit = 43
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 43
        byte = 5
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class VehModMngtGlbSafe1PwrLvlElecMai_2_BgmBodyALMCANFD2SignalIPdu02:
        sig_name = "VehModMngtGlbSafe1PwrLvlElecMai_2_BgmBodyALMCANFD2SignalIPdu02"
        sig_start_bit = 47
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 47
        byte = 5
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4


class BgmToSalm5BodyALMCANFD2DiagReqFrame:
    msg_name = "BgmToSalm5BodyALMCANFD2DiagReqFrame"
    msg_id = 2001
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['SALM5']


class BgmToAllFuncBodyALMCANFD2DiagReqFrame:
    msg_name = "BgmToAllFuncBodyALMCANFD2DiagReqFrame"
    msg_id = 2047
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['SALM4', 'SALM5', 'SALM6']


