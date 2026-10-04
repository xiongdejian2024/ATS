class BgmBodyALMCANFD1Fr01:
    msg_name = "BgmBodyALMCANFD1Fr01"
    msg_id = 880
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.62
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class CarTiGlb_2_BgmBodyALMCANFD1SignalIPdu01:
        sig_name = "CarTiGlb_2_BgmBodyALMCANFD1SignalIPdu01"
        sig_start_bit = 31
        update_id_bit = 63
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


class BgmBodyALMCANFD1Fr02:
    msg_name = "BgmBodyALMCANFD1Fr02"
    msg_id = 575
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.215
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class VehModMngtGlbSafe1UsgModSts_1_BgmBodyALMCANFD1SignalIPdu02:
        sig_name = "VehModMngtGlbSafe1UsgModSts_1_BgmBodyALMCANFD1SignalIPdu02"
        sig_start_bit = 55
        update_id_bit = None
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

    class VehModMngtGlbSafe1FltEgyCnsWdSts_1_BgmBodyALMCANFD1SignalIPdu02:
        sig_name = "VehModMngtGlbSafe1FltEgyCnsWdSts_1_BgmBodyALMCANFD1SignalIPdu02"
        sig_start_bit = 35
        update_id_bit = None
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

    class VehModMngtGlbSafe1CarModSts1_1_BgmBodyALMCANFD1SignalIPdu02:
        sig_name = "VehModMngtGlbSafe1CarModSts1_1_BgmBodyALMCANFD1SignalIPdu02"
        sig_start_bit = 13
        update_id_bit = None
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

    class VehBattUSysUQf_1_BgmBodyALMCANFD1SignalIPdu02:
        sig_name = "VehBattUSysUQf_1_BgmBodyALMCANFD1SignalIPdu02"
        sig_start_bit = 15
        update_id_bit = None
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

    class VehModMngtGlbSafe1EgyLvlElecMai_1_BgmBodyALMCANFD1SignalIPdu02:
        sig_name = "VehModMngtGlbSafe1EgyLvlElecMai_1_BgmBodyALMCANFD1SignalIPdu02"
        sig_start_bit = 27
        update_id_bit = None
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

    class VehModMngtGlbSafe1PwrLvlElecSubtyp_1_BgmBodyALMCANFD1SignalIPdu02:
        sig_name = "VehModMngtGlbSafe1PwrLvlElecSubtyp_1_BgmBodyALMCANFD1SignalIPdu02"
        sig_start_bit = 43
        update_id_bit = None
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

    class VehModMngtGlbSafe1Cntr_1_BgmBodyALMCANFD1SignalIPdu02:
        sig_name = "VehModMngtGlbSafe1Cntr_1_BgmBodyALMCANFD1SignalIPdu02"
        sig_start_bit = 31
        update_id_bit = None
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

    class VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp_1_BgmBodyALMCANFD1SignalIPdu02:
        sig_name = "VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp_1_BgmBodyALMCANFD1SignalIPdu02"
        sig_start_bit = 10
        update_id_bit = None
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

    class VehBattUSysU_1_BgmBodyALMCANFD1SignalIPdu02:
        sig_name = "VehBattUSysU_1_BgmBodyALMCANFD1SignalIPdu02"
        sig_start_bit = 7
        update_id_bit = None
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

    class VehModMngtGlbSafe1PwrLvlElecMai_1_BgmBodyALMCANFD1SignalIPdu02:
        sig_name = "VehModMngtGlbSafe1PwrLvlElecMai_1_BgmBodyALMCANFD1SignalIPdu02"
        sig_start_bit = 47
        update_id_bit = None
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

    class VehModMngtGlbSafe1Chks_1_BgmBodyALMCANFD1SignalIPdu02:
        sig_name = "VehModMngtGlbSafe1Chks_1_BgmBodyALMCANFD1SignalIPdu02"
        sig_start_bit = 23
        update_id_bit = None
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

    class VehModMngtGlbSafe1EgyLvlElecSubtyp_1_BgmBodyALMCANFD1SignalIPdu02:
        sig_name = "VehModMngtGlbSafe1EgyLvlElecSubtyp_1_BgmBodyALMCANFD1SignalIPdu02"
        sig_start_bit = 39
        update_id_bit = None
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


