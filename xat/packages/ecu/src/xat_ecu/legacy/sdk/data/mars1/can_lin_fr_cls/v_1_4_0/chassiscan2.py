class SumChas2Fr06:
    msg_name = "SumChas2Fr06"
    msg_id = 447
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "SUM1"
    rx_nodes = ['VDDM', 'ECM']
    sig_group_dict = {'SuspStabyCritFailrDetd': ['SuspStabyCritFailrDetdChks', 'SuspStabyCritFailrDetdCntr', 'SuspStabyCritFailrDetdSts'], 'SuspPosnVertLe1': ['SuspPosnVertLe1Chks', 'SuspPosnVertLe1Frnt', 'SuspPosnVertLe1FrntQf', 'SuspPosnVertLe1Re', 'SuspPosnVertLe1ReQf']}
    sig_group_dataid_dict = {'SuspStabyCritFailrDetd': 1054}

    class SuspPosnVertLe1FrntQf:
        sig_name = "SuspPosnVertLe1FrntQf"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class SuspStabyCritFailrDetd_UB:
        sig_name = "SuspStabyCritFailrDetd_UB"
        sig_start_bit = 58
        update_id_bit = 58
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 58
        byte = 7
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class SuspStabyCritFailrDetdChks:
        sig_name = "SuspStabyCritFailrDetdChks"
        sig_start_bit = 55
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
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SuspStabyCritFailrDetdCntr:
        sig_name = "SuspStabyCritFailrDetdCntr"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class SuspStabyCritFailrDetdSts:
        sig_name = "SuspStabyCritFailrDetdSts"
        sig_start_bit = 59
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 59
        byte = 7
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class SuspPosnVertLe1Frnt:
        sig_name = "SuspPosnVertLe1Frnt"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 6.2e-05
        sig_value_offset = 0.0
        sig_value_min = -16129
        sig_value_max = 16130
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111110, 0b00000001, 7, 1)]

    class SuspPosnVertLe1Re:
        sig_name = "SuspPosnVertLe1Re"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 6.2e-05
        sig_value_offset = 0.0
        sig_value_min = -16129
        sig_value_max = 16130
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111110, 0b00000001, 7, 1)]

    class SuspPosnVertLe1Chks:
        sig_name = "SuspPosnVertLe1Chks"
        sig_start_bit = 39
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
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SuspPosnVertLe1_UB:
        sig_name = "SuspPosnVertLe1_UB"
        sig_start_bit = 43
        update_id_bit = 43
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 43
        byte = 5
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class SuspPosnVertLe1ReQf:
        sig_name = "SuspPosnVertLe1ReQf"
        sig_start_bit = 45
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
        startbit = 45
        byte = 5
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4


class VddmChas2Fr34:
    msg_name = "VddmChas2Fr34"
    msg_id = 562
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.04
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']
    sig_group_dict = {'PtTqHardMax': ['PtTqHardMaxChks', 'PtTqHardMaxCntr', 'PtTqHardMaxGrdtNeg', 'PtTqHardMaxGrdtPos', 'PtTqHardMaxReq']}
    sig_group_dataid_dict = {'PtTqHardMax': 149}

    class PtTqHardMaxGrdtPos:
        sig_name = "PtTqHardMaxGrdtPos"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 4.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 8191
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111000, 0b00000111, 5, 3)]

    class PtTqHardMaxReq:
        sig_name = "PtTqHardMaxReq"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 4.0
        sig_value_offset = 0.0
        sig_value_min = -4096
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 4095
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111000, 0b00000111, 5, 3)]

    class PtTqHardMaxChks:
        sig_name = "PtTqHardMaxChks"
        sig_start_bit = 55
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
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class PtTqHardMaxGrdtNeg:
        sig_name = "PtTqHardMaxGrdtNeg"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 4.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 8191
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111000, 0b00000111, 5, 3)]

    class PtTqHardMaxCntr:
        sig_name = "PtTqHardMaxCntr"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class PtTqHardMax_UB:
        sig_name = "PtTqHardMax_UB"
        sig_start_bit = 56
        update_id_bit = 56
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 56
        byte = 7
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0


class SumChas2VFCVectorFr:
    msg_name = "SumChas2VFCVectorFr"
    msg_id = 1352
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "SUM1"
    rx_nodes = ['CCM']
    sig_group_dict = {'VFCVectorSUM': ['VFCVectorSUMBlockID', 'VFCVectorSUMVFCid0', 'VFCVectorSUMVFCid1', 'VFCVectorSUMVFCid10', 'VFCVectorSUMVFCid11', 'VFCVectorSUMVFCid12', 'VFCVectorSUMVFCid13', 'VFCVectorSUMVFCid14', 'VFCVectorSUMVFCid15', 'VFCVectorSUMVFCid16', 'VFCVectorSUMVFCid17', 'VFCVectorSUMVFCid18', 'VFCVectorSUMVFCid19', 'VFCVectorSUMVFCid2', 'VFCVectorSUMVFCid20', 'VFCVectorSUMVFCid21', 'VFCVectorSUMVFCid22', 'VFCVectorSUMVFCid23', 'VFCVectorSUMVFCid24', 'VFCVectorSUMVFCid25', 'VFCVectorSUMVFCid26', 'VFCVectorSUMVFCid27', 'VFCVectorSUMVFCid28', 'VFCVectorSUMVFCid29', 'VFCVectorSUMVFCid3', 'VFCVectorSUMVFCid30', 'VFCVectorSUMVFCid31', 'VFCVectorSUMVFCid32', 'VFCVectorSUMVFCid33', 'VFCVectorSUMVFCid34', 'VFCVectorSUMVFCid35', 'VFCVectorSUMVFCid36', 'VFCVectorSUMVFCid37', 'VFCVectorSUMVFCid38', 'VFCVectorSUMVFCid39', 'VFCVectorSUMVFCid4', 'VFCVectorSUMVFCid40', 'VFCVectorSUMVFCid41', 'VFCVectorSUMVFCid42', 'VFCVectorSUMVFCid43', 'VFCVectorSUMVFCid44', 'VFCVectorSUMVFCid45', 'VFCVectorSUMVFCid46', 'VFCVectorSUMVFCid47', 'VFCVectorSUMVFCid48', 'VFCVectorSUMVFCid49', 'VFCVectorSUMVFCid5', 'VFCVectorSUMVFCid50', 'VFCVectorSUMVFCid51', 'VFCVectorSUMVFCid52', 'VFCVectorSUMVFCid53', 'VFCVectorSUMVFCid54', 'VFCVectorSUMVFCid55', 'VFCVectorSUMVFCid56', 'VFCVectorSUMVFCid57', 'VFCVectorSUMVFCid58', 'VFCVectorSUMVFCid59', 'VFCVectorSUMVFCid6', 'VFCVectorSUMVFCid60', 'VFCVectorSUMVFCid61', 'VFCVectorSUMVFCid7', 'VFCVectorSUMVFCid8', 'VFCVectorSUMVFCid9']}
    sig_group_dataid_dict = {}

    class VFCVectorSUMVFCid28:
        sig_name = "VFCVectorSUMVFCid28"
        sig_start_bit = 30
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 30
        byte = 3
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorSUMVFCid26:
        sig_name = "VFCVectorSUMVFCid26"
        sig_start_bit = 28
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 28
        byte = 3
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorSUMVFCid32:
        sig_name = "VFCVectorSUMVFCid32"
        sig_start_bit = 34
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 34
        byte = 4
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorSUMVFCid44:
        sig_name = "VFCVectorSUMVFCid44"
        sig_start_bit = 46
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 46
        byte = 5
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorSUMVFCid23:
        sig_name = "VFCVectorSUMVFCid23"
        sig_start_bit = 25
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 25
        byte = 3
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorSUMVFCid54:
        sig_name = "VFCVectorSUMVFCid54"
        sig_start_bit = 56
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 56
        byte = 7
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorSUMVFCid5:
        sig_name = "VFCVectorSUMVFCid5"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorSUMVFCid33:
        sig_name = "VFCVectorSUMVFCid33"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 35
        byte = 4
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorSUMVFCid31:
        sig_name = "VFCVectorSUMVFCid31"
        sig_start_bit = 33
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 33
        byte = 4
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorSUMVFCid39:
        sig_name = "VFCVectorSUMVFCid39"
        sig_start_bit = 41
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 41
        byte = 5
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorSUMVFCid2:
        sig_name = "VFCVectorSUMVFCid2"
        sig_start_bit = 4
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 4
        byte = 0
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorSUMVFCid0:
        sig_name = "VFCVectorSUMVFCid0"
        sig_start_bit = 2
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 2
        byte = 0
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorSUMVFCid1:
        sig_name = "VFCVectorSUMVFCid1"
        sig_start_bit = 3
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 3
        byte = 0
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorSUMVFCid57:
        sig_name = "VFCVectorSUMVFCid57"
        sig_start_bit = 59
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 59
        byte = 7
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorSUMVFCid8:
        sig_name = "VFCVectorSUMVFCid8"
        sig_start_bit = 10
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 10
        byte = 1
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorSUMVFCid48:
        sig_name = "VFCVectorSUMVFCid48"
        sig_start_bit = 50
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 50
        byte = 6
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorSUMVFCid55:
        sig_name = "VFCVectorSUMVFCid55"
        sig_start_bit = 57
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 57
        byte = 7
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorSUMVFCid49:
        sig_name = "VFCVectorSUMVFCid49"
        sig_start_bit = 51
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 51
        byte = 6
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorSUMVFCid53:
        sig_name = "VFCVectorSUMVFCid53"
        sig_start_bit = 55
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 55
        byte = 6
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorSUMVFCid61:
        sig_name = "VFCVectorSUMVFCid61"
        sig_start_bit = 63
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 63
        byte = 7
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorSUMVFCid12:
        sig_name = "VFCVectorSUMVFCid12"
        sig_start_bit = 14
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 14
        byte = 1
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorSUMVFCid36:
        sig_name = "VFCVectorSUMVFCid36"
        sig_start_bit = 38
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 38
        byte = 4
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorSUMVFCid52:
        sig_name = "VFCVectorSUMVFCid52"
        sig_start_bit = 54
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 54
        byte = 6
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorSUMVFCid35:
        sig_name = "VFCVectorSUMVFCid35"
        sig_start_bit = 37
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 37
        byte = 4
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorSUMVFCid11:
        sig_name = "VFCVectorSUMVFCid11"
        sig_start_bit = 13
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 13
        byte = 1
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorSUMVFCid16:
        sig_name = "VFCVectorSUMVFCid16"
        sig_start_bit = 18
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 18
        byte = 2
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorSUMVFCid41:
        sig_name = "VFCVectorSUMVFCid41"
        sig_start_bit = 43
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 43
        byte = 5
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorSUMVFCid47:
        sig_name = "VFCVectorSUMVFCid47"
        sig_start_bit = 49
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 49
        byte = 6
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorSUMVFCid17:
        sig_name = "VFCVectorSUMVFCid17"
        sig_start_bit = 19
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 19
        byte = 2
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorSUMVFCid19:
        sig_name = "VFCVectorSUMVFCid19"
        sig_start_bit = 21
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 21
        byte = 2
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorSUMVFCid9:
        sig_name = "VFCVectorSUMVFCid9"
        sig_start_bit = 11
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 11
        byte = 1
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorSUMVFCid27:
        sig_name = "VFCVectorSUMVFCid27"
        sig_start_bit = 29
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 29
        byte = 3
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorSUMVFCid3:
        sig_name = "VFCVectorSUMVFCid3"
        sig_start_bit = 5
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorSUMVFCid59:
        sig_name = "VFCVectorSUMVFCid59"
        sig_start_bit = 61
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 61
        byte = 7
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorSUMVFCid24:
        sig_name = "VFCVectorSUMVFCid24"
        sig_start_bit = 26
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 26
        byte = 3
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorSUMVFCid46:
        sig_name = "VFCVectorSUMVFCid46"
        sig_start_bit = 48
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 48
        byte = 6
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorSUMVFCid18:
        sig_name = "VFCVectorSUMVFCid18"
        sig_start_bit = 20
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 20
        byte = 2
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorSUMVFCid10:
        sig_name = "VFCVectorSUMVFCid10"
        sig_start_bit = 12
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 12
        byte = 1
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorSUMVFCid29:
        sig_name = "VFCVectorSUMVFCid29"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 31
        byte = 3
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorSUMVFCid37:
        sig_name = "VFCVectorSUMVFCid37"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 39
        byte = 4
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorSUMVFCid40:
        sig_name = "VFCVectorSUMVFCid40"
        sig_start_bit = 42
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 42
        byte = 5
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorSUMVFCid22:
        sig_name = "VFCVectorSUMVFCid22"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 24
        byte = 3
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorSUMVFCid20:
        sig_name = "VFCVectorSUMVFCid20"
        sig_start_bit = 22
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 22
        byte = 2
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorSUMVFCid15:
        sig_name = "VFCVectorSUMVFCid15"
        sig_start_bit = 17
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 17
        byte = 2
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorSUMVFCid34:
        sig_name = "VFCVectorSUMVFCid34"
        sig_start_bit = 36
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 36
        byte = 4
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorSUMVFCid25:
        sig_name = "VFCVectorSUMVFCid25"
        sig_start_bit = 27
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 27
        byte = 3
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorSUMBlockID:
        sig_name = "VFCVectorSUMBlockID"
        sig_start_bit = 1
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VFCVectorSUMVFCid21:
        sig_name = "VFCVectorSUMVFCid21"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 23
        byte = 2
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorSUMVFCid60:
        sig_name = "VFCVectorSUMVFCid60"
        sig_start_bit = 62
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 62
        byte = 7
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorSUMVFCid38:
        sig_name = "VFCVectorSUMVFCid38"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 40
        byte = 5
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorSUMVFCid4:
        sig_name = "VFCVectorSUMVFCid4"
        sig_start_bit = 6
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorSUMVFCid43:
        sig_name = "VFCVectorSUMVFCid43"
        sig_start_bit = 45
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 45
        byte = 5
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorSUMVFCid30:
        sig_name = "VFCVectorSUMVFCid30"
        sig_start_bit = 32
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 32
        byte = 4
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorSUMVFCid14:
        sig_name = "VFCVectorSUMVFCid14"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 16
        byte = 2
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorSUMVFCid7:
        sig_name = "VFCVectorSUMVFCid7"
        sig_start_bit = 9
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 9
        byte = 1
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorSUMVFCid42:
        sig_name = "VFCVectorSUMVFCid42"
        sig_start_bit = 44
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 44
        byte = 5
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorSUMVFCid51:
        sig_name = "VFCVectorSUMVFCid51"
        sig_start_bit = 53
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 53
        byte = 6
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorSUMVFCid56:
        sig_name = "VFCVectorSUMVFCid56"
        sig_start_bit = 58
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 58
        byte = 7
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorSUMVFCid6:
        sig_name = "VFCVectorSUMVFCid6"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 8
        byte = 1
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorSUMVFCid58:
        sig_name = "VFCVectorSUMVFCid58"
        sig_start_bit = 60
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 60
        byte = 7
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorSUMVFCid50:
        sig_name = "VFCVectorSUMVFCid50"
        sig_start_bit = 52
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorSUMVFCid13:
        sig_name = "VFCVectorSUMVFCid13"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 15
        byte = 1
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorSUMVFCid45:
        sig_name = "VFCVectorSUMVFCid45"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 47
        byte = 5
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7


class VddmChas2Fr53:
    msg_name = "VddmChas2Fr53"
    msg_id = 17
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['BBM', 'ECM']
    sig_group_dict = {'PtTqAtAxleMinReq': ['PtTqAtAxleMinReqChks', 'PtTqAtAxleMinReqCntr', 'PtTqAtAxleMinReqPtTqAtAxleFrntReq', 'PtTqAtAxleMinReqPtTqAtAxleReReq'], 'RbuCtrlModReqSafe2': ['RbuCtrlModReqSafe2BrkSysModCfmd', 'RbuCtrlModReqSafe2Chks', 'RbuCtrlModReqSafe2Cntr']}
    sig_group_dataid_dict = {'PtTqAtAxleMinReq': 1108, 'RbuCtrlModReqSafe2': 1065}

    class RbuCtrlModReqSafe2Cntr:
        sig_name = "RbuCtrlModReqSafe2Cntr"
        sig_start_bit = 51
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
        startbit = 51
        byte = 6
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class PtTqAtAxleMinReqCntr:
        sig_name = "PtTqAtAxleMinReqCntr"
        sig_start_bit = 3
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
        startbit = 3
        byte = 0
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class PtTqAtAxleMinReqChks:
        sig_name = "PtTqAtAxleMinReqChks"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RbuCtrlModReqSafe2BrkSysModCfmd:
        sig_name = "RbuCtrlModReqSafe2BrkSysModCfmd"
        sig_start_bit = 55
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ModCfmd_NoReq': 0, 'ModCfmd_MarsParking': 1, 'ModCfmd_Reserved2': 2, 'ModCfmd_Reserved3': 3, 'ModCfmd_Reserved4': 4, 'ModCfmd_ANP': 5, 'ModCfmd_Reserved6': 6, 'ModCfmd_Reserved7': 7, 'ModCfmd_Reserved8': 8, 'ModCfmd_ACC_HWA': 9, 'ModCfmd_PEB': 10, 'ModCfmd_APA': 11, 'ModCfmd_RPA': 12, 'ModCfmd_HPA': 13, 'ModCfmd_TJP_HWC': 14, 'ModCfmd_NOP': 15}
        compute_method = None
        length = 4
        startbit = 55
        byte = 6
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class RbuCtrlModReqSafe2Chks:
        sig_name = "RbuCtrlModReqSafe2Chks"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class PtTqAtAxleMinReq_UB:
        sig_name = "PtTqAtAxleMinReq_UB"
        sig_start_bit = 4
        update_id_bit = 4
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 4
        byte = 0
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class EPedlModCtrlSt:
        sig_name = "EPedlModCtrlSt"
        sig_start_bit = 6
        update_id_bit = 5
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class RbuCtrlModReqSafe2_UB:
        sig_name = "RbuCtrlModReqSafe2_UB"
        sig_start_bit = 7
        update_id_bit = 7
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class PtTqAtAxleMinReqPtTqAtAxleReReq:
        sig_name = "PtTqAtAxleMinReqPtTqAtAxleReReq"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = -20000
        sig_value_max = 20000
        sig_byteorder = "Motorola"
        sig_value_init = -20000.0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class PtTqAtAxleMinReqPtTqAtAxleFrntReq:
        sig_name = "PtTqAtAxleMinReqPtTqAtAxleFrntReq"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = -20000
        sig_value_max = 20000
        sig_byteorder = "Motorola"
        sig_value_init = -20000.0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0)]


class EcmChas2Fr46:
    msg_name = "EcmChas2Fr46"
    msg_id = 1137
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 1.0
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class EcmIntelliClimaResd11:
        sig_name = "EcmIntelliClimaResd11"
        sig_start_bit = 7
        update_id_bit = 55
        sig_length = 32
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 32
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class EcmIntelliClimaResd9:
        sig_name = "EcmIntelliClimaResd9"
        sig_start_bit = 39
        update_id_bit = 54
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0)]


class VddmChas2Fr03:
    msg_name = "VddmChas2Fr03"
    msg_id = 160
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.015
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM', 'SUM1']
    sig_group_dict = {'ADataRawSafe': ['ADataRawSafeALat', 'ADataRawSafeALat1Qf', 'ADataRawSafeALgt', 'ADataRawSafeALgt1Qf', 'ADataRawSafeAVert', 'ADataRawSafeAVertQf', 'ADataRawSafeChks', 'ADataRawSafeCntr']}
    sig_group_dataid_dict = {'ADataRawSafe': 34}

    class ADataRawSafeALgt:
        sig_name = "ADataRawSafeALgt"
        sig_start_bit = 38
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 0.0085
        sig_value_offset = 0.0
        sig_value_min = -16352
        sig_value_max = 16353
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 38
        bmuws_info = [(4, 0b01111111, 0b10000000, 7, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class ADataRawSafe_UB:
        sig_name = "ADataRawSafe_UB"
        sig_start_bit = 56
        update_id_bit = 56
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 56
        byte = 7
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ADataRawSafeALgt1Qf:
        sig_name = "ADataRawSafeALgt1Qf"
        sig_start_bit = 9
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Qf1_DevOfDataUndefd': 0, 'Qf1_DataTmpUndefdAndEvlnInProgs': 1, 'Qf1_DevOfDataNotWithinRngAllwd': 2, 'Qf1_DataCalcdWithDevDefd': 3}
        compute_method = None
        length = 2
        startbit = 9
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class ADataRawSafeCntr:
        sig_name = "ADataRawSafeCntr"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class ADataRawSafeALat1Qf:
        sig_name = "ADataRawSafeALat1Qf"
        sig_start_bit = 11
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Qf1_DevOfDataUndefd': 0, 'Qf1_DataTmpUndefdAndEvlnInProgs': 1, 'Qf1_DevOfDataNotWithinRngAllwd': 2, 'Qf1_DataCalcdWithDevDefd': 3}
        compute_method = None
        length = 2
        startbit = 11
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class ADataRawSafeAVertQf:
        sig_name = "ADataRawSafeAVertQf"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Qf1_DevOfDataUndefd': 0, 'Qf1_DataTmpUndefdAndEvlnInProgs': 1, 'Qf1_DevOfDataNotWithinRngAllwd': 2, 'Qf1_DataCalcdWithDevDefd': 3}
        compute_method = None
        length = 2
        startbit = 24
        bmuws_info = [(3, 0b00000001, 0b11111110, 1, 0), (4, 0b10000000, 0b01111111, 1, 7)]

    class ADataRawSafeALat:
        sig_name = "ADataRawSafeALat"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 0.0085
        sig_value_offset = 0.0
        sig_value_min = -16352
        sig_value_max = 16353
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111110, 0b00000001, 7, 1)]

    class ADataRawSafeAVert:
        sig_name = "ADataRawSafeAVert"
        sig_start_bit = 55
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 0.0085
        sig_value_offset = 0.0
        sig_value_min = -16352
        sig_value_max = 16353
        sig_byteorder = "Motorola"
        sig_value_init = 1155
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 55
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111110, 0b00000001, 7, 1)]

    class ADataRawSafeChks:
        sig_name = "ADataRawSafeChks"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 255
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class VddmChas2Fr20:
    msg_name = "VddmChas2Fr20"
    msg_id = 720
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.08
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM', 'SUM1']
    sig_group_dict = {'DoorDrvrStsWithFacQly': ['DoorDrvrStsWithFacQlyDoorSts', 'DoorDrvrStsWithFacQlyFacQly'], 'DrvrPrsntSts': ['DrvrPrsntStsDrvrPrsnt', 'DrvrPrsntStsDrvrPrsntChks', 'DrvrPrsntStsDrvrPrsntCntr', 'DrvrPrsntStsDrvrPrsntQf']}
    sig_group_dataid_dict = {'DrvrPrsntSts': 121}

    class DoorDrvrStsWithFacQlyDoorSts:
        sig_name = "DoorDrvrStsWithFacQlyDoorSts"
        sig_start_bit = 61
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorSts2_Ukwn': 0, 'DoorSts2_Opend': 1, 'DoorSts2_Clsd': 2}
        compute_method = None
        length = 2
        startbit = 61
        byte = 7
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class ProfPenSts1:
        sig_name = "ProfPenSts1"
        sig_start_bit = 39
        update_id_bit = 44
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'IdPen_ProfUkwn': 0, 'IdPen_Prof1': 1, 'IdPen_Prof2': 2, 'IdPen_Prof3': 3, 'IdPen_Prof4': 4, 'IdPen_Prof5': 5, 'IdPen_Prof6': 6, 'IdPen_Prof7': 7, 'IdPen_Prof8': 8, 'IdPen_Prof9': 9, 'IdPen_Prof10': 10, 'IdPen_Prof11': 11, 'IdPen_Prof12': 12, 'IdPen_Prof13': 13, 'IdPen_Resd14': 14, 'IdPen_ProfAll': 15}
        compute_method = None
        length = 4
        startbit = 39
        byte = 4
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DoorDrvrStsWithFacQly_UB:
        sig_name = "DoorDrvrStsWithFacQly_UB"
        sig_start_bit = 63
        update_id_bit = 63
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 63
        byte = 7
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class DrvrPrsntStsDrvrPrsntChks:
        sig_name = "DrvrPrsntStsDrvrPrsntChks"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DrvrPrsntStsDrvrPrsntCntr:
        sig_name = "DrvrPrsntStsDrvrPrsntCntr"
        sig_start_bit = 3
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
        startbit = 3
        byte = 0
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DoorDrvrStsWithFacQlyFacQly:
        sig_name = "DoorDrvrStsWithFacQlyFacQly"
        sig_start_bit = 59
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
        startbit = 59
        byte = 7
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class SaveSetgToMemPrmnt:
        sig_name = "SaveSetgToMemPrmnt"
        sig_start_bit = 43
        update_id_bit = 54
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OffOnAut1_Off': 0, 'OffOnAut1_On': 1, 'OffOnAut1_Aut': 2}
        compute_method = None
        length = 2
        startbit = 43
        byte = 5
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class DrvrPrsntStsDrvrPrsnt:
        sig_name = "DrvrPrsntStsDrvrPrsnt"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoYesCrit1_NotVld1': 0, 'NoYesCrit1_No': 1, 'NoYesCrit1_Yes': 2, 'NoYesCrit1_NotVld2': 3}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class DrvrPrsntStsDrvrPrsntQf:
        sig_name = "DrvrPrsntStsDrvrPrsntQf"
        sig_start_bit = 5
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Qf1_DevOfDataUndefd': 0, 'Qf1_DataTmpUndefdAndEvlnInProgs': 1, 'Qf1_DevOfDataNotWithinRngAllwd': 2, 'Qf1_DataCalcdWithDevDefd': 3}
        compute_method = None
        length = 2
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class DrvrPrsntSts_UB:
        sig_name = "DrvrPrsntSts_UB"
        sig_start_bit = 22
        update_id_bit = 22
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 22
        byte = 2
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6


class VddmChas2Fr19:
    msg_name = "VddmChas2Fr19"
    msg_id = 736
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.08
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM', 'SUM1']
    sig_group_dict = {'VehModMngtGlbSafe1': ['VehModMngtGlbSafe1CarModSts1', 'VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp', 'VehModMngtGlbSafe1Chks', 'VehModMngtGlbSafe1Cntr', 'VehModMngtGlbSafe1EgyLvlElecMai', 'VehModMngtGlbSafe1EgyLvlElecSubtyp', 'VehModMngtGlbSafe1FltEgyCnsWdSts', 'VehModMngtGlbSafe1PwrLvlElecMai', 'VehModMngtGlbSafe1PwrLvlElecSubtyp', 'VehModMngtGlbSafe1UsgModSts'], 'VehMtnSt': ['VehMtnStChks', 'VehMtnStCntr', 'VehMtnStVehMtnSt']}
    sig_group_dataid_dict = {'VehModMngtGlbSafe1': 116, 'VehMtnSt': 54}

    class VehModMngtGlbSafe1UsgModSts:
        sig_name = "VehModMngtGlbSafe1UsgModSts"
        sig_start_bit = 11
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
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class VehModMngtGlbSafe1Chks:
        sig_name = "VehModMngtGlbSafe1Chks"
        sig_start_bit = 7
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
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehModMngtGlbSafe1_UB:
        sig_name = "VehModMngtGlbSafe1_UB"
        sig_start_bit = 32
        update_id_bit = 32
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 32
        byte = 4
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VehMtnStCntr:
        sig_name = "VehMtnStCntr"
        sig_start_bit = 55
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
        startbit = 55
        byte = 6
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class VehModMngtGlbSafe1PwrLvlElecSubtyp:
        sig_name = "VehModMngtGlbSafe1PwrLvlElecSubtyp"
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

    class VehModMngtGlbSafe1PwrLvlElecMai:
        sig_name = "VehModMngtGlbSafe1PwrLvlElecMai"
        sig_start_bit = 19
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
        startbit = 19
        byte = 2
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class VehModMngtGlbSafe1EgyLvlElecMai:
        sig_name = "VehModMngtGlbSafe1EgyLvlElecMai"
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

    class VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp:
        sig_name = "VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp"
        sig_start_bit = 36
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
        startbit = 36
        byte = 4
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class VehMtnStVehMtnSt:
        sig_name = "VehMtnStVehMtnSt"
        sig_start_bit = 51
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VehMtnSt2_Ukwn': 0, 'VehMtnSt2_StandStillVal1': 1, 'VehMtnSt2_StandStillVal2': 2, 'VehMtnSt2_StandStillVal3': 3, 'VehMtnSt2_RollgFwdVal1': 4, 'VehMtnSt2_RollgFwdVal2': 5, 'VehMtnSt2_RollgBackwVal1': 6, 'VehMtnSt2_RollgBackwVal2': 7}
        compute_method = None
        length = 3
        startbit = 51
        byte = 6
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class VehModMngtGlbSafe1FltEgyCnsWdSts:
        sig_name = "VehModMngtGlbSafe1FltEgyCnsWdSts"
        sig_start_bit = 33
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
        startbit = 33
        byte = 4
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VehModMngtGlbSafe1EgyLvlElecSubtyp:
        sig_name = "VehModMngtGlbSafe1EgyLvlElecSubtyp"
        sig_start_bit = 23
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
        startbit = 23
        byte = 2
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class VehModMngtGlbSafe1CarModSts1:
        sig_name = "VehModMngtGlbSafe1CarModSts1"
        sig_start_bit = 39
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
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class VehModMngtGlbSafe1Cntr:
        sig_name = "VehModMngtGlbSafe1Cntr"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class VehMtnSt_UB:
        sig_name = "VehMtnSt_UB"
        sig_start_bit = 48
        update_id_bit = 48
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 48
        byte = 6
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VehMtnStChks:
        sig_name = "VehMtnStChks"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class VddmChas2Fr21:
    msg_name = "VddmChas2Fr21"
    msg_id = 513
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.03
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM', 'SUM1']
    sig_group_dict = {'BrkSysCylPMst': ['BrkSysCylPMstAct', 'BrkSysCylPMstActQf', 'BrkSysCylPMstChks', 'BrkSysCylPMstCntr', 'BrkSysCylPMstTar', 'BrkSysCylPMstVirt', 'BrkSysCylPMstVirtQf']}
    sig_group_dataid_dict = {'BrkSysCylPMst': 183}

    class BrkSysCylPMstVirt:
        sig_name = "BrkSysCylPMstVirt"
        sig_start_bit = 25
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.25
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 25
        bmuws_info = [(3, 0b00000011, 0b11111100, 2, 0), (4, 0b11111111, 0b00000000, 8, 0)]

    class BrkSysCylPMstActQf:
        sig_name = "BrkSysCylPMstActQf"
        sig_start_bit = 27
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
        startbit = 27
        byte = 3
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class BrkSysCylPMstChks:
        sig_name = "BrkSysCylPMstChks"
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

    class BrkSysCylPMst_UB:
        sig_name = "BrkSysCylPMst_UB"
        sig_start_bit = 7
        update_id_bit = 7
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class BrkSysCylPMstVirtQf:
        sig_name = "BrkSysCylPMstVirtQf"
        sig_start_bit = 29
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
        startbit = 29
        byte = 3
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class BrkSysCylPMstTar:
        sig_name = "BrkSysCylPMstTar"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.25
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class BrkSysCylPMstAct:
        sig_name = "BrkSysCylPMstAct"
        sig_start_bit = 49
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.3
        sig_value_offset = -30.0
        sig_value_min = 0
        sig_value_max = 1022
        sig_byteorder = "Motorola"
        sig_value_init = 100
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 49
        bmuws_info = [(6, 0b00000011, 0b11111100, 2, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class BrkSysCylPMstCntr:
        sig_name = "BrkSysCylPMstCntr"
        sig_start_bit = 53
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
        startbit = 53
        byte = 6
        mask = 0b00111100
        unmask = 0b11000011
        shift = 2


class VddmChas2Fr73:
    msg_name = "VddmChas2Fr73"
    msg_id = 857
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.32
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class CcmRollgCntrSts:
        sig_name = "CcmRollgCntrSts"
        sig_start_bit = 23
        update_id_bit = 43
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

    class HvacAirMFlowReEstimd:
        sig_name = "HvacAirMFlowReEstimd"
        sig_start_bit = 31
        update_id_bit = 55
        sig_length = 10
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11000000, 0b00111111, 2, 6)]


class EcmChas2Fr05:
    msg_name = "EcmChas2Fr05"
    msg_id = 272
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.025
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM', 'SUM1']
    sig_group_dict = {'OvrdDecelByDrvr': ['OvrdDecelByDrvrChks', 'OvrdDecelByDrvrCntr', 'OvrdDecelByDrvrOvrdDecelByDrvr']}
    sig_group_dataid_dict = {'OvrdDecelByDrvr': 110}

    class OvrdDecelByDrvrChks:
        sig_name = "OvrdDecelByDrvrChks"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 255
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class OvrdDecelByDrvrOvrdDecelByDrvr:
        sig_name = "OvrdDecelByDrvrOvrdDecelByDrvr"
        sig_start_bit = 4
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 4
        byte = 0
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class PtTqAtAxleAvlFrntMax:
        sig_name = "PtTqAtAxleAvlFrntMax"
        sig_start_bit = 39
        update_id_bit = 41
        sig_length = 13
        sig_value_factor = 4.0
        sig_value_offset = 0.0
        sig_value_min = -4096
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111000, 0b00000111, 5, 3)]

    class DrvrPrpsnTqReq:
        sig_name = "DrvrPrpsnTqReq"
        sig_start_bit = 55
        update_id_bit = 40
        sig_length = 16
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = -20000
        sig_value_max = 20000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 55
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class CrsCtrlOvrdn:
        sig_name = "CrsCtrlOvrdn"
        sig_start_bit = 29
        update_id_bit = 28
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 29
        byte = 3
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class OvrdDecelByDrvr_UB:
        sig_name = "OvrdDecelByDrvr_UB"
        sig_start_bit = 5
        update_id_bit = 5
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class OvrdDecelByDrvrCntr:
        sig_name = "OvrdDecelByDrvrCntr"
        sig_start_bit = 3
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
        startbit = 3
        byte = 0
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0


class EcmChas2Fr19:
    msg_name = "EcmChas2Fr19"
    msg_id = 944
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 1.0
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']
    sig_group_dict = {'HybErrIndcnReq': ['HybErrIndcnReqTelltlBattTracCutOff', 'HybErrIndcnReqTelltlBattTracFailr', 'HybErrIndcnReqTelltlElecDrvFailr', 'HybErrIndcnReqTelltlSysHybFailr']}
    sig_group_dataid_dict = {}

    class HybErrIndcnReqTelltlElecDrvFailr:
        sig_name = "HybErrIndcnReqTelltlElecDrvFailr"
        sig_start_bit = 17
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flg1_Rst': 0, 'Flg1_Set': 1}
        compute_method = None
        length = 1
        startbit = 17
        byte = 2
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class HybErrIndcnReq_UB:
        sig_name = "HybErrIndcnReq_UB"
        sig_start_bit = 31
        update_id_bit = 31
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 31
        byte = 3
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class HybErrIndcnReqTelltlBattTracCutOff:
        sig_name = "HybErrIndcnReqTelltlBattTracCutOff"
        sig_start_bit = 19
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flg1_Rst': 0, 'Flg1_Set': 1}
        compute_method = None
        length = 1
        startbit = 19
        byte = 2
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class HybErrIndcnReqTelltlBattTracFailr:
        sig_name = "HybErrIndcnReqTelltlBattTracFailr"
        sig_start_bit = 18
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flg1_Rst': 0, 'Flg1_Set': 1}
        compute_method = None
        length = 1
        startbit = 18
        byte = 2
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VehPropSts:
        sig_name = "VehPropSts"
        sig_start_bit = 42
        update_id_bit = 41
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 42
        byte = 5
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class HybErrIndcnReqTelltlSysHybFailr:
        sig_name = "HybErrIndcnReqTelltlSysHybFailr"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flg1_Rst': 0, 'Flg1_Set': 1}
        compute_method = None
        length = 1
        startbit = 16
        byte = 2
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0


class VddmChas2Fr64:
    msg_name = "VddmChas2Fr64"
    msg_id = 548
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.08
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class DstToDestination:
        sig_name = "DstToDestination"
        sig_start_bit = 7
        update_id_bit = 39
        sig_length = 32
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 32
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0)]


class EcmChas2Fr06:
    msg_name = "EcmChas2Fr06"
    msg_id = 304
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.025
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HvCooltHeatrEnad:
        sig_name = "HvCooltHeatrEnad"
        sig_start_bit = 41
        update_id_bit = 40
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 41
        byte = 5
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1


class EcmChas2Fr15:
    msg_name = "EcmChas2Fr15"
    msg_id = 560
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.04
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class PwrCnsReqAtHvBattFlt:
        sig_name = "PwrCnsReqAtHvBattFlt"
        sig_start_bit = 52
        update_id_bit = 51
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class EngLoadReqElec:
        sig_name = "EngLoadReqElec"
        sig_start_bit = 39
        update_id_bit = 11
        sig_length = 16
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = -32768
        sig_value_max = 32767
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class ImobEngSts1:
        sig_name = "ImobEngSts1"
        sig_start_bit = 55
        update_id_bit = 53
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ImobSts_ImobUndefd': 0, 'ImobSts_ImobImobn': 1, 'ImobSts_ImobMtn': 2, 'ImobSts_ImobNoMtn': 3}
        compute_method = None
        length = 2
        startbit = 55
        byte = 6
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HvPwrAvlForClimaEstimd:
        sig_name = "HvPwrAvlForClimaEstimd"
        sig_start_bit = 9
        update_id_bit = 49
        sig_length = 10
        sig_value_factor = 20.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 9
        bmuws_info = [(1, 0b00000011, 0b11111100, 2, 0), (2, 0b11111111, 0b00000000, 8, 0)]


class VddmChas2Fr70:
    msg_name = "VddmChas2Fr70"
    msg_id = 1061
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class IntelliClimaResd10:
        sig_name = "IntelliClimaResd10"
        sig_start_bit = 47
        update_id_bit = 61
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111111, 0b00000000, 8, 0)]

    class IntelliClimaResd4:
        sig_name = "IntelliClimaResd4"
        sig_start_bit = 7
        update_id_bit = 63
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
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class IntelliClimaResd14:
        sig_name = "IntelliClimaResd14"
        sig_start_bit = 15
        update_id_bit = 62
        sig_length = 32
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 32
        startbit = 15
        bmuws_info = [(1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111111, 0b00000000, 8, 0)]


class VddmChas2Fr51:
    msg_name = "VddmChas2Fr51"
    msg_id = 1109
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['SUM1']
    sig_group_dict = {'VehCfgPrmExt': ['VehCfgPrmExtBlkIDBytePosn1', 'VehCfgPrmExtCCPBytePosn2', 'VehCfgPrmExtCCPBytePosn3', 'VehCfgPrmExtCCPBytePosn4', 'VehCfgPrmExtCCPBytePosn5', 'VehCfgPrmExtCCPBytePosn6', 'VehCfgPrmExtCCPBytePosn7', 'VehCfgPrmExtCCPBytePosn8']}
    sig_group_dataid_dict = {}

    class VehCfgPrmExtCCPBytePosn2:
        sig_name = "VehCfgPrmExtCCPBytePosn2"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgPrmExtCCPBytePosn8:
        sig_name = "VehCfgPrmExtCCPBytePosn8"
        sig_start_bit = 63
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgPrmExtBlkIDBytePosn1:
        sig_name = "VehCfgPrmExtBlkIDBytePosn1"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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

    class VehCfgPrmExtCCPBytePosn3:
        sig_name = "VehCfgPrmExtCCPBytePosn3"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 23
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgPrmExtCCPBytePosn4:
        sig_name = "VehCfgPrmExtCCPBytePosn4"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgPrmExtCCPBytePosn5:
        sig_name = "VehCfgPrmExtCCPBytePosn5"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgPrmExtCCPBytePosn7:
        sig_name = "VehCfgPrmExtCCPBytePosn7"
        sig_start_bit = 55
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgPrmExtCCPBytePosn6:
        sig_name = "VehCfgPrmExtCCPBytePosn6"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class VddmChas2Fr12:
    msg_name = "VddmChas2Fr12"
    msg_id = 448
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.03
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']
    sig_group_dict = {'BrkPedlPsd': ['BrkPedlPsdBrkPedlNotPsdSafe', 'BrkPedlPsdBrkPedlPsd', 'BrkPedlPsdChks', 'BrkPedlPsdCntr', 'BrkPedlPsdQf']}
    sig_group_dataid_dict = {'BrkPedlPsd': 56}

    class BrkPedlPsdQf:
        sig_name = "BrkPedlPsdQf"
        sig_start_bit = 5
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class BrkPedlPsdCntr:
        sig_name = "BrkPedlPsdCntr"
        sig_start_bit = 3
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
        startbit = 3
        byte = 0
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class BrkPedlPsd_UB:
        sig_name = "BrkPedlPsd_UB"
        sig_start_bit = 23
        update_id_bit = 23
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 23
        byte = 2
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class BrkPedlPsdBrkPedlPsd:
        sig_name = "BrkPedlPsdBrkPedlPsd"
        sig_start_bit = 6
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class BrkPedlPsdBrkPedlNotPsdSafe:
        sig_name = "BrkPedlPsdBrkPedlNotPsdSafe"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class BrkPedlPsdChks:
        sig_name = "BrkPedlPsdChks"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class VddmChas2Fr30:
    msg_name = "VddmChas2Fr30"
    msg_id = 592
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM', 'SUM1']
    sig_group_dict = {'VehCfgPrm': ['VehCfgPrmBlkIDBytePosn1', 'VehCfgPrmCCPBytePosn2', 'VehCfgPrmCCPBytePosn3', 'VehCfgPrmCCPBytePosn4', 'VehCfgPrmCCPBytePosn5', 'VehCfgPrmCCPBytePosn6', 'VehCfgPrmCCPBytePosn7', 'VehCfgPrmCCPBytePosn8']}
    sig_group_dataid_dict = {}

    class VehCfgPrmCCPBytePosn8:
        sig_name = "VehCfgPrmCCPBytePosn8"
        sig_start_bit = 63
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgPrmBlkIDBytePosn1:
        sig_name = "VehCfgPrmBlkIDBytePosn1"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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

    class VehCfgPrmCCPBytePosn4:
        sig_name = "VehCfgPrmCCPBytePosn4"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgPrmCCPBytePosn3:
        sig_name = "VehCfgPrmCCPBytePosn3"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 23
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgPrmCCPBytePosn6:
        sig_name = "VehCfgPrmCCPBytePosn6"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgPrmCCPBytePosn7:
        sig_name = "VehCfgPrmCCPBytePosn7"
        sig_start_bit = 55
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgPrmCCPBytePosn5:
        sig_name = "VehCfgPrmCCPBytePosn5"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgPrmCCPBytePosn2:
        sig_name = "VehCfgPrmCCPBytePosn2"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class BbmChas2Fr02:
    msg_name = "BbmChas2Fr02"
    msg_id = 367
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "BBM"
    rx_nodes = ['VDDM', 'ECM']
    sig_group_dict = {'SecBrkActrReqParkBrk': ['SecBrkActrReqParkBrkChks', 'SecBrkActrReqParkBrkCntr', 'SecBrkActrReqParkBrkReq'], 'LgtCtrlModReqSafeBkp': ['LgtCtrlModReqSafeBkpChks', 'LgtCtrlModReqSafeBkpCntr', 'LgtCtrlModReqSafeBkpLgtCtrlModReqSafe', 'LgtCtrlModReqSafeBkpLgtFctFailr']}
    sig_group_dataid_dict = {'SecBrkActrReqParkBrk': 1087, 'LgtCtrlModReqSafeBkp': 1074}

    class SecBrkActrReqParkBrkCntr:
        sig_name = "SecBrkActrReqParkBrkCntr"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class SecBrkActrReqParkBrkReq:
        sig_name = "SecBrkActrReqParkBrkReq"
        sig_start_bit = 43
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PrkgBrkElectcCtrlReq_NoRequest': 0, 'PrkgBrkElectcCtrlReq_ReleaseRequest': 1, 'PrkgBrkElectcCtrlReq_ApplyRequest': 2, 'PrkgBrkElectcCtrlReq_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 43
        byte = 5
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class LgtCtrlModReqSafeBkpChks:
        sig_name = "LgtCtrlModReqSafeBkpChks"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class LgtCtrlModReqSafeBkpCntr:
        sig_name = "LgtCtrlModReqSafeBkpCntr"
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

    class LgtCtrlModReqSafeBkpLgtCtrlModReqSafe:
        sig_name = "LgtCtrlModReqSafeBkpLgtCtrlModReqSafe"
        sig_start_bit = 35
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ModCfmd_NoReq': 0, 'ModCfmd_MarsParking': 1, 'ModCfmd_Reserved2': 2, 'ModCfmd_Reserved3': 3, 'ModCfmd_Reserved4': 4, 'ModCfmd_ANP': 5, 'ModCfmd_Reserved6': 6, 'ModCfmd_Reserved7': 7, 'ModCfmd_Reserved8': 8, 'ModCfmd_ACC_HWA': 9, 'ModCfmd_PEB': 10, 'ModCfmd_APA': 11, 'ModCfmd_RPA': 12, 'ModCfmd_HPA': 13, 'ModCfmd_TJP_HWC': 14, 'ModCfmd_NOP': 15}
        compute_method = None
        length = 4
        startbit = 35
        byte = 4
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class SecBrkActrReqParkBrkChks:
        sig_name = "SecBrkActrReqParkBrkChks"
        sig_start_bit = 55
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
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SecBrkActrReqParkBrk_UB:
        sig_name = "SecBrkActrReqParkBrk_UB"
        sig_start_bit = 44
        update_id_bit = 44
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 44
        byte = 5
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class LgtCtrlModReqSafeBkp_UB:
        sig_name = "LgtCtrlModReqSafeBkp_UB"
        sig_start_bit = 16
        update_id_bit = 16
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 16
        byte = 2
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class LgtCtrlModReqSafeBkpLgtFctFailr:
        sig_name = "LgtCtrlModReqSafeBkpLgtFctFailr"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LgtFctFail_NoFailure': 0, 'LgtFctFail_MarsParkingFailure': 1, 'LgtFctFail_APAFailure': 2, 'LgtFctFail_RPAFailure': 3, 'LgtFctFail_HPAFailure': 4, 'LgtFctFail_ACCFailure': 5, 'LgtFctFail_ANPFailure': 6, 'LgtFctFail_E2EFailure': 7}
        compute_method = None
        length = 3
        startbit = 47
        byte = 5
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5


class VddmChas2Fr22:
    msg_name = "VddmChas2Fr22"
    msg_id = 784
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.4
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class DrvModDispd:
        sig_name = "DrvModDispd"
        sig_start_bit = 23
        update_id_bit = 44
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 23
        byte = 2
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class SpdLimFirst:
        sig_name = "SpdLimFirst"
        sig_start_bit = 31
        update_id_bit = 43
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CmptmtRelHum:
        sig_name = "CmptmtRelHum"
        sig_start_bit = 15
        update_id_bit = 3
        sig_length = 8
        sig_value_factor = 0.5
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 200
        sig_byteorder = "Motorola"
        sig_value_init = 80
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class VddmChas2Fr71:
    msg_name = "VddmChas2Fr71"
    msg_id = 1062
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class IntelliClimaResd9:
        sig_name = "IntelliClimaResd9"
        sig_start_bit = 47
        update_id_bit = 61
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111111, 0b00000000, 8, 0)]

    class IntelliClimaResd15:
        sig_name = "IntelliClimaResd15"
        sig_start_bit = 15
        update_id_bit = 62
        sig_length = 32
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 32
        startbit = 15
        bmuws_info = [(1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111111, 0b00000000, 8, 0)]

    class IntelliClimaResd5:
        sig_name = "IntelliClimaResd5"
        sig_start_bit = 7
        update_id_bit = 63
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
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class VddmChas2Fr69:
    msg_name = "VddmChas2Fr69"
    msg_id = 1060
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class IntelliClimaResd13:
        sig_name = "IntelliClimaResd13"
        sig_start_bit = 15
        update_id_bit = 62
        sig_length = 32
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 32
        startbit = 15
        bmuws_info = [(1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111111, 0b00000000, 8, 0)]

    class IntelliClimaResd3:
        sig_name = "IntelliClimaResd3"
        sig_start_bit = 7
        update_id_bit = 63
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
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class IntelliClimaResd8:
        sig_name = "IntelliClimaResd8"
        sig_start_bit = 47
        update_id_bit = 61
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111111, 0b00000000, 8, 0)]


class EcmChas2Fr32:
    msg_name = "EcmChas2Fr32"
    msg_id = 529
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.15
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class BookChrgnStsFb:
        sig_name = "BookChrgnStsFb"
        sig_start_bit = 59
        update_id_bit = 57
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BookChrgnStsFb_Default': 0, 'BookChrgnStsFb_Success': 1, 'BookChrgnStsFb_Fail': 2, 'BookChrgnStsFb_Finished': 3}
        compute_method = None
        length = 2
        startbit = 59
        byte = 7
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class HvHeatrPwrCns:
        sig_name = "HvHeatrPwrCns"
        sig_start_bit = 39
        update_id_bit = 42
        sig_length = 10
        sig_value_factor = 20.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11000000, 0b00111111, 2, 6)]

    class DstFromDestinationFb:
        sig_name = "DstFromDestinationFb"
        sig_start_bit = 45
        update_id_bit = 56
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DstFromDestinationResp_Default': 0, 'DstFromDestinationResp_Success': 1, 'DstFromDestinationResp_Fault': 2, 'DstFromDestinationResp_EndOfDischarge': 3, 'DstFromDestinationResp_Reserved0': 4, 'DstFromDestinationResp_Reserved1': 5, 'DstFromDestinationResp_Reserved2': 6, 'DstFromDestinationResp_Reserved3': 7}
        compute_method = None
        length = 3
        startbit = 45
        byte = 5
        mask = 0b00111000
        unmask = 0b11000111
        shift = 3


class VddmChas2Fr37:
    msg_name = "VddmChas2Fr37"
    msg_id = 774
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.17
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class TireRdEstimd:
        sig_name = "TireRdEstimd"
        sig_start_bit = 41
        update_id_bit = 63
        sig_length = 10
        sig_value_factor = 0.00048828
        sig_value_offset = 0.25
        sig_value_min = 0
        sig_value_max = 513
        sig_byteorder = "Motorola"
        sig_value_init = 266
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 41
        bmuws_info = [(5, 0b00000011, 0b11111100, 2, 0), (6, 0b11111111, 0b00000000, 8, 0)]


class VddmChas2Fr17:
    msg_name = "VddmChas2Fr17"
    msg_id = 576
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.06
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class StopBookChrgnReq:
        sig_name = "StopBookChrgnReq"
        sig_start_bit = 4
        update_id_bit = 5
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ReqSts1_NotReqd': 0, 'ReqSts1_Reqd': 1}
        compute_method = None
        length = 1
        startbit = 4
        byte = 0
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class BrkTracCtrlActv:
        sig_name = "BrkTracCtrlActv"
        sig_start_bit = 51
        update_id_bit = 52
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CtrlSts1_NoCtrl': 0, 'CtrlSts1_InCtrl': 1}
        compute_method = None
        length = 1
        startbit = 51
        byte = 6
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class DrvrSeatSts:
        sig_name = "DrvrSeatSts"
        sig_start_bit = 49
        update_id_bit = 53
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OccptPresSt1_Undefd1': 0, 'OccptPresSt1_OccptNotPrsnt': 1, 'OccptPresSt1_OccptPrsnt': 2, 'OccptPresSt1_Undefd2': 3}
        compute_method = None
        length = 2
        startbit = 49
        byte = 6
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class AbsSts:
        sig_name = "AbsSts"
        sig_start_bit = 50
        update_id_bit = 54
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevErrSts2_NoFlt': 0, 'DevErrSts2_Flt': 1}
        compute_method = None
        length = 1
        startbit = 50
        byte = 6
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2


class VddmChas2Fr29:
    msg_name = "VddmChas2Fr29"
    msg_id = 768
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.3
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']
    sig_group_dict = {'ImobBrkNrSerl': ['ImobBrkNrSerl0', 'ImobBrkNrSerl1', 'ImobBrkNrSerl2', 'ImobBrkNrSerl3', 'ImobBrkNrSerl4', 'ImobBrkNrSerl5']}
    sig_group_dataid_dict = {}

    class EpbDrvrDisp:
        sig_name = "EpbDrvrDisp"
        sig_start_bit = 54
        update_id_bit = 48
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EpbDrvrDisp_Msg0': 0, 'EpbDrvrDisp_Msg3': 3, 'EpbDrvrDisp_Msg4': 4, 'EpbDrvrDisp_Msg5': 5, 'EpbDrvrDisp_Msg6': 6, 'EpbDrvrDisp_Msg8': 8, 'EpbDrvrDisp_Msg11': 11, 'EpbDrvrDisp_Msg12': 12, 'EpbDrvrDisp_Msg13': 13, 'EpbDrvrDisp_Msg14': 14, 'EpbDrvrDisp_Msg15': 15, 'EpbDrvrDisp_Resd1': 1, 'EpbDrvrDisp_Resd2': 2, 'EpbDrvrDisp_Resd7': 7, 'EpbDrvrDisp_Msg9': 9, 'EpbDrvrDisp_Msg10': 10}
        compute_method = None
        length = 4
        startbit = 54
        byte = 6
        mask = 0b01111000
        unmask = 0b10000111
        shift = 3

    class ImobBrkNrSerl4:
        sig_name = "ImobBrkNrSerl4"
        sig_start_bit = 39
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
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SetLimReq:
        sig_name = "SetLimReq"
        sig_start_bit = 50
        update_id_bit = 63
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SetSpdSts_Unknown': 0, 'SetSpdSts_ManuallySet': 1, 'SetSpdSts_AutomaticallySet': 2, 'SetSpdSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 50
        byte = 6
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class ImobBrkNrSerl0:
        sig_name = "ImobBrkNrSerl0"
        sig_start_bit = 7
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
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ImobBrkNrSerl_UB:
        sig_name = "ImobBrkNrSerl_UB"
        sig_start_bit = 55
        update_id_bit = 55
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 55
        byte = 6
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ImobBrkNrSerl2:
        sig_name = "ImobBrkNrSerl2"
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

    class ImobBrkNrSerl5:
        sig_name = "ImobBrkNrSerl5"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ImobBrkNrSerl1:
        sig_name = "ImobBrkNrSerl1"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ImobBrkNrSerl3:
        sig_name = "ImobBrkNrSerl3"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class EcmChas2Fr14:
    msg_name = "EcmChas2Fr14"
    msg_id = 800
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.2
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HvEgyLoadFctReq:
        sig_name = "HvEgyLoadFctReq"
        sig_start_bit = 26
        update_id_bit = 25
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 26
        byte = 3
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class PrpsnModOfTracBlkd:
        sig_name = "PrpsnModOfTracBlkd"
        sig_start_bit = 54
        update_id_bit = 51
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Typ1_Typ0': 0, 'Typ1_Typ1': 1, 'Typ1_Typ2': 2, 'Typ1_Typ3': 3, 'Typ1_Typ4': 4, 'Typ1_Typ5': 5, 'Typ1_Typ6': 6, 'Typ1_Typ7': 7}
        compute_method = None
        length = 3
        startbit = 54
        byte = 6
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4


class EcmChas2Fr11:
    msg_name = "EcmChas2Fr11"
    msg_id = 544
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.03
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class PtTqAtAxleAvlFrntMin:
        sig_name = "PtTqAtAxleAvlFrntMin"
        sig_start_bit = 55
        update_id_bit = 56
        sig_length = 13
        sig_value_factor = 4.0
        sig_value_offset = 0.0
        sig_value_min = -4096
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 55
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111000, 0b00000111, 5, 3)]

    class DispOfBrkPwrPercRgnMin:
        sig_name = "DispOfBrkPwrPercRgnMin"
        sig_start_bit = 17
        update_id_bit = 39
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = -50.0
        sig_value_min = -500
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 500
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 17
        bmuws_info = [(2, 0b00000011, 0b11111100, 2, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class DispOfPrpsnPwrPercElecMax:
        sig_name = "DispOfPrpsnPwrPercElecMax"
        sig_start_bit = 33
        update_id_bit = 38
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 33
        bmuws_info = [(4, 0b00000011, 0b11111100, 2, 0), (5, 0b11111111, 0b00000000, 8, 0)]


class VddmChas2Fr41:
    msg_name = "VddmChas2Fr41"
    msg_id = 776
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.13
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class TotDstTrvld:
        sig_name = "TotDstTrvld"
        sig_start_bit = 0
        update_id_bit = 1
        sig_length = 25
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 20000000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 25
        startbit = 0
        bmuws_info = [(0, 0b00000001, 0b11111110, 1, 0), (1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0)]


class EcmChas2Fr03:
    msg_name = "EcmChas2Fr03"
    msg_id = 53
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']
    sig_group_dict = {'PtTotRgnTarTq': ['PtTotRgnTarTq1', 'PtTotRgnTarTqQf']}
    sig_group_dataid_dict = {}

    class RlyCrashForHvsysReq:
        sig_name = "RlyCrashForHvsysReq"
        sig_start_bit = 39
        update_id_bit = 38
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 39
        byte = 4
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class PtTotRgnTarTq1:
        sig_name = "PtTotRgnTarTq1"
        sig_start_bit = 54
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = -16384
        sig_value_max = 16380
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 54
        bmuws_info = [(6, 0b01111111, 0b10000000, 7, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class PtTotRgnTarTq_UB:
        sig_name = "PtTotRgnTarTq_UB"
        sig_start_bit = 42
        update_id_bit = 42
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 42
        byte = 5
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class PtTotRgnTarTqQf:
        sig_name = "PtTotRgnTarTqQf"
        sig_start_bit = 41
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Qf1_DevOfDataUndefd': 0, 'Qf1_DataTmpUndefdAndEvlnInProgs': 1, 'Qf1_DevOfDataNotWithinRngAllwd': 2, 'Qf1_DataCalcdWithDevDefd': 3}
        compute_method = None
        length = 2
        startbit = 41
        byte = 5
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class AccrPedlRatGrdt:
        sig_name = "AccrPedlRatGrdt"
        sig_start_bit = 23
        update_id_bit = 24
        sig_length = 15
        sig_value_factor = 0.0625
        sig_value_offset = 0.0
        sig_value_min = -16000
        sig_value_max = 16000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111110, 0b00000001, 7, 1)]

    class PrpsnTqReReq:
        sig_name = "PrpsnTqReReq"
        sig_start_bit = 7
        update_id_bit = 37
        sig_length = 16
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = -20000
        sig_value_max = 20000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0)]


class EcmChas2Fr51:
    msg_name = "EcmChas2Fr51"
    msg_id = 1142
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 1.0
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']
    sig_group_dict = {'BexvPosnReq': ['BexvPosnReqExvCalibReq', 'BexvPosnReqExvHeatdReq', 'BexvPosnReqExvMovEnable', 'BexvPosnReqExvPosnReq'], 'CexvPosnReq': ['CexvPosnReqExvCalibReq', 'CexvPosnReqExvHeatdReq', 'CexvPosnReqExvMovEnable', 'CexvPosnReqExvPosnReq'], 'EexvPosnReq': ['EexvPosnReqExvCalibReq', 'EexvPosnReqExvHeatdReq', 'EexvPosnReqExvMovEnable', 'EexvPosnReqExvPosnReq']}
    sig_group_dataid_dict = {}

    class CexvPosnReqExvCalibReq:
        sig_name = "CexvPosnReqExvCalibReq"
        sig_start_bit = 20
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvCalibReq_NoReq': 0, 'ExvCalibReq_InitializationReq': 1}
        compute_method = None
        length = 1
        startbit = 20
        byte = 2
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class EexvPosnReqExvPosnReq:
        sig_name = "EexvPosnReqExvPosnReq"
        sig_start_bit = 34
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.2
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 500
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 34
        bmuws_info = [(4, 0b00000111, 0b11111000, 3, 0), (5, 0b11111110, 0b00000001, 7, 1)]

    class EexvPosnReqExvMovEnable:
        sig_name = "EexvPosnReqExvMovEnable"
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
        sig_value_table = {'EXVNotEnable': 0, 'EXVEnable': 1}
        compute_method = None
        length = 1
        startbit = 35
        byte = 4
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class EexvPosnReqExvHeatdReq:
        sig_name = "EexvPosnReqExvHeatdReq"
        sig_start_bit = 36
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvHeatdReq_NoReq': 0, 'ExvHeatdReq_PreHeatedReq': 1}
        compute_method = None
        length = 1
        startbit = 36
        byte = 4
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class BexvPosnReqExvCalibReq:
        sig_name = "BexvPosnReqExvCalibReq"
        sig_start_bit = 4
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvCalibReq_NoReq': 0, 'ExvCalibReq_InitializationReq': 1}
        compute_method = None
        length = 1
        startbit = 4
        byte = 0
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class BexvPosnReqExvHeatdReq:
        sig_name = "BexvPosnReqExvHeatdReq"
        sig_start_bit = 3
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvHeatdReq_NoReq': 0, 'ExvHeatdReq_PreHeatedReq': 1}
        compute_method = None
        length = 1
        startbit = 3
        byte = 0
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class CexvPosnReqExvHeatdReq:
        sig_name = "CexvPosnReqExvHeatdReq"
        sig_start_bit = 19
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvHeatdReq_NoReq': 0, 'ExvHeatdReq_PreHeatedReq': 1}
        compute_method = None
        length = 1
        startbit = 19
        byte = 2
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class BexvPosnReqExvPosnReq:
        sig_name = "BexvPosnReqExvPosnReq"
        sig_start_bit = 1
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.2
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 500
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 1
        bmuws_info = [(0, 0b00000011, 0b11111100, 2, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class BexvPosnReq_UB:
        sig_name = "BexvPosnReq_UB"
        sig_start_bit = 5
        update_id_bit = 5
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class CexvPosnReq_UB:
        sig_name = "CexvPosnReq_UB"
        sig_start_bit = 21
        update_id_bit = 21
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 21
        byte = 2
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class CexvPosnReqExvMovEnable:
        sig_name = "CexvPosnReqExvMovEnable"
        sig_start_bit = 18
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EXVNotEnable': 0, 'EXVEnable': 1}
        compute_method = None
        length = 1
        startbit = 18
        byte = 2
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class CexvPosnReqExvPosnReq:
        sig_name = "CexvPosnReqExvPosnReq"
        sig_start_bit = 17
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.2
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 500
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 17
        bmuws_info = [(2, 0b00000011, 0b11111100, 2, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class EexvPosnReq_UB:
        sig_name = "EexvPosnReq_UB"
        sig_start_bit = 38
        update_id_bit = 38
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 38
        byte = 4
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class EexvPosnReqExvCalibReq:
        sig_name = "EexvPosnReqExvCalibReq"
        sig_start_bit = 37
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvCalibReq_NoReq': 0, 'ExvCalibReq_InitializationReq': 1}
        compute_method = None
        length = 1
        startbit = 37
        byte = 4
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class HvWtrHeatrPwrCnsAllwd:
        sig_name = "HvWtrHeatrPwrCnsAllwd"
        sig_start_bit = 55
        update_id_bit = 40
        sig_length = 8
        sig_value_factor = 40.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BexvPosnReqExvMovEnable:
        sig_name = "BexvPosnReqExvMovEnable"
        sig_start_bit = 2
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EXVNotEnable': 0, 'EXVEnable': 1}
        compute_method = None
        length = 1
        startbit = 2
        byte = 0
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2


class VddmChas2Fr13:
    msg_name = "VddmChas2Fr13"
    msg_id = 336
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.025
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM', 'SUM1']
    sig_group_dict = {'SteerWhlSnsr': ['SteerWhlSnsrAg', 'SteerWhlSnsrAgSpd', 'SteerWhlSnsrChks', 'SteerWhlSnsrCntr', 'SteerWhlSnsrQf']}
    sig_group_dataid_dict = {'SteerWhlSnsr': 51}

    class EngActvnMod1WdReq:
        sig_name = "EngActvnMod1WdReq"
        sig_start_bit = 59
        update_id_bit = 57
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EngActvnMod1_WakeupFunctionNOTActiveANDExternalRequestNOTPresent': 0, 'EngActvnMod1_WakeupFunctionNOTActiveANDExternalRequestPresent': 1, 'EngActvnMod1_WakeupFunctionActiveANDExternalRequestNOTPresent': 2, 'EngActvnMod1_WakeupFunctionActiveANDExternalRequestPresent': 3}
        compute_method = None
        length = 2
        startbit = 59
        byte = 7
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class SteerWhlSnsrChks:
        sig_name = "SteerWhlSnsrChks"
        sig_start_bit = 7
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
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SteerWhlSnsr_UB:
        sig_name = "SteerWhlSnsr_UB"
        sig_start_bit = 41
        update_id_bit = 41
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 41
        byte = 5
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class SteerWhlSnsrQf:
        sig_name = "SteerWhlSnsrQf"
        sig_start_bit = 11
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
        startbit = 11
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class EpedlTqActvSts:
        sig_name = "EpedlTqActvSts"
        sig_start_bit = 61
        update_id_bit = 56
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 61
        byte = 7
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class PtActvnReq1WdPtActvnReq:
        sig_name = "PtActvnReq1WdPtActvnReq"
        sig_start_bit = 51
        update_id_bit = 40
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PtActvnReq1_NoPtActvnReq': 0, 'PtActvnReq1_PtActvnReq': 1, 'PtActvnReq1_PtActvnReqRem': 2, 'PtActvnReq1_PtActvnNotDriving': 3}
        compute_method = None
        length = 2
        startbit = 51
        byte = 6
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class SteerWhlSnsrAg:
        sig_name = "SteerWhlSnsrAg"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 0.0009765625
        sig_value_offset = 0.0
        sig_value_min = -14848
        sig_value_max = 14848
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111110, 0b00000001, 7, 1)]

    class SteerLockEnagOfPrpsn:
        sig_name = "SteerLockEnagOfPrpsn"
        sig_start_bit = 49
        update_id_bit = 60
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SteerLockEnagOfPrpsn_SteerLockEnagResd1': 0, 'SteerLockEnagOfPrpsn_PrpsnInhbFromSteerLock': 1, 'SteerLockEnagOfPrpsn_PrpsnAllwdFromSteerLock': 2, 'SteerLockEnagOfPrpsn_SteerLockEnagResd2': 3}
        compute_method = None
        length = 2
        startbit = 49
        byte = 6
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class SteerWhlSnsrCntr:
        sig_name = "SteerWhlSnsrCntr"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class SteerWhlSnsrAgSpd:
        sig_name = "SteerWhlSnsrAgSpd"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 14
        sig_value_factor = 0.0078125
        sig_value_offset = 0.0
        sig_value_min = -6400
        sig_value_max = 6400
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 14
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111100, 0b00000011, 6, 2)]


class SumChassisCAN2NmFr:
    msg_name = "SumChassisCAN2NmFr"
    msg_id = 1317
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "SUM1"
    rx_nodes = ['BBM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class EcmChas2Fr80:
    msg_name = "EcmChas2Fr80"
    msg_id = 245
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = []
    sig_group_dict = {'AccrPedlRat': ['AccrPedlRatAccrPedlRat', 'AccrPedlRatChks', 'AccrPedlRatCntr']}
    sig_group_dataid_dict = {'AccrPedlRat': 868}

    class AccrPedlRatAccrPedlRat:
        sig_name = "AccrPedlRatAccrPedlRat"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 0.00390625
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 25600
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111110, 0b00000001, 7, 1)]

    class AccrPedlRat_UB:
        sig_name = "AccrPedlRat_UB"
        sig_start_bit = 15
        update_id_bit = 15
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 15
        byte = 1
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class AccrPedlRatChks:
        sig_name = "AccrPedlRatChks"
        sig_start_bit = 7
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
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class AccrPedlRatCntr:
        sig_name = "AccrPedlRatCntr"
        sig_start_bit = 11
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
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0


class VddmChas2Fr05:
    msg_name = "VddmChas2Fr05"
    msg_id = 224
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM', 'SUM1']
    sig_group_dict = {'DrvrBrkTqAtWhlsReqd': ['DrvrBrkTqAtWhlsReqdChks', 'DrvrBrkTqAtWhlsReqdCntr', 'DrvrBrkTqAtWhlsReqdDrvrBrkTqAtWhlsReqd', 'DrvrBrkTqAtWhlsReqdQf'], 'VehSpdLgt': ['VehSpdLgtA', 'VehSpdLgtChks', 'VehSpdLgtCntr', 'VehSpdLgtQf']}
    sig_group_dataid_dict = {'DrvrBrkTqAtWhlsReqd': 122, 'VehSpdLgt': 55}

    class DrvrBrkTqAtWhlsReqdDrvrBrkTqAtWhlsReqd:
        sig_name = "DrvrBrkTqAtWhlsReqdDrvrBrkTqAtWhlsReqd"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = -20000
        sig_value_max = 20000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class DrvrBrkTqAtWhlsReqd_UB:
        sig_name = "DrvrBrkTqAtWhlsReqd_UB"
        sig_start_bit = 25
        update_id_bit = 25
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 25
        byte = 3
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VehSpdLgtQf:
        sig_name = "VehSpdLgtQf"
        sig_start_bit = 59
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
        startbit = 59
        byte = 7
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VehSpdLgtA:
        sig_name = "VehSpdLgtA"
        sig_start_bit = 38
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 0.00391
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 31970
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 38
        bmuws_info = [(4, 0b01111111, 0b10000000, 7, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class DrvrBrkTqAtWhlsReqdCntr:
        sig_name = "DrvrBrkTqAtWhlsReqdCntr"
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

    class DrvrBrkTqAtWhlsReqdChks:
        sig_name = "DrvrBrkTqAtWhlsReqdChks"
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

    class DrvrBrkTqAtWhlsReqdQf:
        sig_name = "DrvrBrkTqAtWhlsReqdQf"
        sig_start_bit = 27
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
        startbit = 27
        byte = 3
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VehSpdLgtCntr:
        sig_name = "VehSpdLgtCntr"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class VehSpdLgtChks:
        sig_name = "VehSpdLgtChks"
        sig_start_bit = 55
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
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehSpdLgt_UB:
        sig_name = "VehSpdLgt_UB"
        sig_start_bit = 39
        update_id_bit = 39
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 39
        byte = 4
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7


class EcmChas2Fr63:
    msg_name = "EcmChas2Fr63"
    msg_id = 1164
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 1.0
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']
    sig_group_dict = {'ThermMgmtObsrvn7': ['ThermMgmtObsrvn7Byte0', 'ThermMgmtObsrvn7Byte1', 'ThermMgmtObsrvn7Byte2', 'ThermMgmtObsrvn7Byte3', 'ThermMgmtObsrvn7Byte4', 'ThermMgmtObsrvn7Byte5', 'ThermMgmtObsrvn7Byte6', 'ThermMgmtObsrvn7Byte7']}
    sig_group_dataid_dict = {}

    class ThermMgmtObsrvn7Byte6:
        sig_name = "ThermMgmtObsrvn7Byte6"
        sig_start_bit = 55
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
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn7Byte5:
        sig_name = "ThermMgmtObsrvn7Byte5"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn7Byte3:
        sig_name = "ThermMgmtObsrvn7Byte3"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn7Byte4:
        sig_name = "ThermMgmtObsrvn7Byte4"
        sig_start_bit = 39
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
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn7Byte7:
        sig_name = "ThermMgmtObsrvn7Byte7"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn7Byte0:
        sig_name = "ThermMgmtObsrvn7Byte0"
        sig_start_bit = 7
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
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn7Byte1:
        sig_name = "ThermMgmtObsrvn7Byte1"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn7Byte2:
        sig_name = "ThermMgmtObsrvn7Byte2"
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


class VddmChas2Fr16:
    msg_name = "VddmChas2Fr16"
    msg_id = 496
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.03
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['BBM', 'ECM', 'SUM1']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class BkpOfDstTrvld:
        sig_name = "BkpOfDstTrvld"
        sig_start_bit = 7
        update_id_bit = 53
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

    class AutHldAvlSt:
        sig_name = "AutHldAvlSt"
        sig_start_bit = 54
        update_id_bit = 52
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AvlSts2_NotAvl': 0, 'AvlSts2_Avl': 1}
        compute_method = None
        length = 1
        startbit = 54
        byte = 6
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6


class EcmChas2Fr49:
    msg_name = "EcmChas2Fr49"
    msg_id = 1140
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 1.0
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class EcmIntelliClimaResd14:
        sig_name = "EcmIntelliClimaResd14"
        sig_start_bit = 7
        update_id_bit = 55
        sig_length = 32
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 32
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class EcmIntelliClimaResd10:
        sig_name = "EcmIntelliClimaResd10"
        sig_start_bit = 39
        update_id_bit = 54
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0)]


class VddmChas2Fr81:
    msg_name = "VddmChas2Fr81"
    msg_id = 1179
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 1.0
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']
    sig_group_dict = {'HmiCmptmtTSp': ['HmiCmptmtTSpForRowFirstLe', 'HmiCmptmtTSpForRowFirstRi', 'HmiCmptmtTSpForRowSecLe', 'HmiCmptmtTSpForRowSecRi', 'HmiCmptmtTSpSpclForRowFirstLe', 'HmiCmptmtTSpSpclForRowFirstRi', 'HmiCmptmtTSpSpclForRowSecLe', 'HmiCmptmtTSpSpclForRowSecRi']}
    sig_group_dataid_dict = {}

    class HmiCmptmtTSpForRowFirstRi:
        sig_name = "HmiCmptmtTSpForRowFirstRi"
        sig_start_bit = 12
        update_id_bit = None
        sig_length = 5
        sig_value_factor = 0.5
        sig_value_offset = 15.0
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Motorola"
        sig_value_init = 14
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 12
        byte = 1
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class HmiCmptmtTSpForRowFirstLe:
        sig_name = "HmiCmptmtTSpForRowFirstLe"
        sig_start_bit = 4
        update_id_bit = None
        sig_length = 5
        sig_value_factor = 0.5
        sig_value_offset = 15.0
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Motorola"
        sig_value_init = 14
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 4
        byte = 0
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class HmiCmptmtTSpSpclForRowSecLe:
        sig_name = "HmiCmptmtTSpSpclForRowSecLe"
        sig_start_bit = 22
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HmiCmptmtTSpSpcl_Norm': 0, 'HmiCmptmtTSpSpcl_Lo': 1, 'HmiCmptmtTSpSpcl_Hi': 2}
        compute_method = None
        length = 2
        startbit = 22
        byte = 2
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class HmiCmptmtTSpSpclForRowSecRi:
        sig_name = "HmiCmptmtTSpSpclForRowSecRi"
        sig_start_bit = 30
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HmiCmptmtTSpSpcl_Norm': 0, 'HmiCmptmtTSpSpcl_Lo': 1, 'HmiCmptmtTSpSpcl_Hi': 2}
        compute_method = None
        length = 2
        startbit = 30
        byte = 3
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class HmiCmptmtTSpForRowSecLe:
        sig_name = "HmiCmptmtTSpForRowSecLe"
        sig_start_bit = 20
        update_id_bit = None
        sig_length = 5
        sig_value_factor = 0.5
        sig_value_offset = 15.0
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Motorola"
        sig_value_init = 14
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 20
        byte = 2
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class HmiCmptmtTSpSpclForRowFirstRi:
        sig_name = "HmiCmptmtTSpSpclForRowFirstRi"
        sig_start_bit = 14
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HmiCmptmtTSpSpcl_Norm': 0, 'HmiCmptmtTSpSpcl_Lo': 1, 'HmiCmptmtTSpSpcl_Hi': 2}
        compute_method = None
        length = 2
        startbit = 14
        byte = 1
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class HmiCmptmtTSpSpclForRowFirstLe:
        sig_name = "HmiCmptmtTSpSpclForRowFirstLe"
        sig_start_bit = 6
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HmiCmptmtTSpSpcl_Norm': 0, 'HmiCmptmtTSpSpcl_Lo': 1, 'HmiCmptmtTSpSpcl_Hi': 2}
        compute_method = None
        length = 2
        startbit = 6
        byte = 0
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class HmiCmptmtTSp_UB:
        sig_name = "HmiCmptmtTSp_UB"
        sig_start_bit = 7
        update_id_bit = 7
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class HmiCmptmtTSpForRowSecRi:
        sig_name = "HmiCmptmtTSpForRowSecRi"
        sig_start_bit = 28
        update_id_bit = None
        sig_length = 5
        sig_value_factor = 0.5
        sig_value_offset = 15.0
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Motorola"
        sig_value_init = 14
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 28
        byte = 3
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0


class BbmChas2Fr06:
    msg_name = "BbmChas2Fr06"
    msg_id = 150
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "BBM"
    rx_nodes = ['VDDM']
    sig_group_dict = {'IMU2ComStsa': ['IMU2ComStsaChks', 'IMU2ComStsaCntr', 'IMU2ComStsaHvSysPwrOff']}
    sig_group_dataid_dict = {'IMU2ComStsa': 3503}

    class IMU2ComStsaHvSysPwrOff:
        sig_name = "IMU2ComStsaHvSysPwrOff"
        sig_start_bit = 11
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OkNotOk1_Ok': 0, 'OkNotOk1_NotOk': 1}
        compute_method = None
        length = 1
        startbit = 11
        byte = 1
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class IMU2ComStsa_UB:
        sig_name = "IMU2ComStsa_UB"
        sig_start_bit = 10
        update_id_bit = 10
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 10
        byte = 1
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class IMU2ComStsaChks:
        sig_name = "IMU2ComStsaChks"
        sig_start_bit = 7
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
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class IMU2ComStsaCntr:
        sig_name = "IMU2ComStsaCntr"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4


class EcmChas2Fr16:
    msg_name = "EcmChas2Fr16"
    msg_id = 880
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.7
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class DispBattEgyOut:
        sig_name = "DispBattEgyOut"
        sig_start_bit = 31
        update_id_bit = 60
        sig_length = 8
        sig_value_factor = 0.5
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DispBattEgyIn:
        sig_name = "DispBattEgyIn"
        sig_start_bit = 23
        update_id_bit = 49
        sig_length = 8
        sig_value_factor = 0.5
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 23
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class PrpsnModOffroadBlkd:
        sig_name = "PrpsnModOffroadBlkd"
        sig_start_bit = 7
        update_id_bit = 63
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Typ1_Typ0': 0, 'Typ1_Typ1': 1, 'Typ1_Typ2': 2, 'Typ1_Typ3': 3, 'Typ1_Typ4': 4, 'Typ1_Typ5': 5, 'Typ1_Typ6': 6, 'Typ1_Typ7': 7}
        compute_method = None
        length = 3
        startbit = 7
        byte = 0
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5


class VddmChas2Fr72:
    msg_name = "VddmChas2Fr72"
    msg_id = 856
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.3
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']
    sig_group_dict = {'DvlpFrameForCCM': ['DvlpFrameForCCMByte0', 'DvlpFrameForCCMByte1', 'DvlpFrameForCCMByte2', 'DvlpFrameForCCMByte3', 'DvlpFrameForCCMByte4', 'DvlpFrameForCCMByte5', 'DvlpFrameForCCMByte6', 'DvlpFrameForCCMByte7']}
    sig_group_dataid_dict = {}

    class DvlpFrameForCCMByte4:
        sig_name = "DvlpFrameForCCMByte4"
        sig_start_bit = 39
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
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DvlpFrameForCCMByte7:
        sig_name = "DvlpFrameForCCMByte7"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DvlpFrameForCCMByte5:
        sig_name = "DvlpFrameForCCMByte5"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DvlpFrameForCCMByte6:
        sig_name = "DvlpFrameForCCMByte6"
        sig_start_bit = 55
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
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DvlpFrameForCCMByte0:
        sig_name = "DvlpFrameForCCMByte0"
        sig_start_bit = 7
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
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DvlpFrameForCCMByte1:
        sig_name = "DvlpFrameForCCMByte1"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DvlpFrameForCCMByte3:
        sig_name = "DvlpFrameForCCMByte3"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DvlpFrameForCCMByte2:
        sig_name = "DvlpFrameForCCMByte2"
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


class EtctoBbmXcpFr01:
    msg_name = "EtctoBbmXcpFr01"
    msg_id = 1366
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CCM"
    rx_nodes = ['BBM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class EcmChas2Fr48:
    msg_name = "EcmChas2Fr48"
    msg_id = 1139
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 1.0
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class EcmIntelliClimaResd13:
        sig_name = "EcmIntelliClimaResd13"
        sig_start_bit = 7
        update_id_bit = 55
        sig_length = 32
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 32
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class EcmIntelliClimaResd8:
        sig_name = "EcmIntelliClimaResd8"
        sig_start_bit = 39
        update_id_bit = 54
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0)]


class VddmChas2Fr39:
    msg_name = "VddmChas2Fr39"
    msg_id = 1024
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 1.0
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']
    sig_group_dict = {'RoadLoadNom': ['RoadLoadNomCoeff0', 'RoadLoadNomCoeff1', 'RoadLoadNomCoeff2', 'RoadLoadNomCoeffSts']}
    sig_group_dataid_dict = {}

    class RoadLoadNomCoeff0:
        sig_name = "RoadLoadNomCoeff0"
        sig_start_bit = 2
        update_id_bit = None
        sig_length = 11
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 2
        bmuws_info = [(0, 0b00000111, 0b11111000, 3, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class RoadLoadNom_UB:
        sig_name = "RoadLoadNom_UB"
        sig_start_bit = 4
        update_id_bit = 4
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 4
        byte = 0
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class RoadLoadNomCoeffSts:
        sig_name = "RoadLoadNomCoeffSts"
        sig_start_bit = 3
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 3
        byte = 0
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class RoadLoadNomCoeff1:
        sig_name = "RoadLoadNomCoeff1"
        sig_start_bit = 17
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.05859
        sig_value_offset = 0.0
        sig_value_min = -510
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 17
        bmuws_info = [(2, 0b00000011, 0b11111100, 2, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class RoadLoadNomCoeff2:
        sig_name = "RoadLoadNomCoeff2"
        sig_start_bit = 33
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.002929
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 991
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 33
        bmuws_info = [(4, 0b00000011, 0b11111100, 2, 0), (5, 0b11111111, 0b00000000, 8, 0)]


class VddmChas2Fr79:
    msg_name = "VddmChas2Fr79"
    msg_id = 647
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.2
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HvacHeatElmAirMFlowEstimd:
        sig_name = "HvacHeatElmAirMFlowEstimd"
        sig_start_bit = 7
        update_id_bit = 13
        sig_length = 10
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class HvEgyDesForClima:
        sig_name = "HvEgyDesForClima"
        sig_start_bit = 31
        update_id_bit = 12
        sig_length = 8
        sig_value_factor = 50.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvacRecircAct:
        sig_name = "HvacRecircAct"
        sig_start_bit = 23
        update_id_bit = 16
        sig_length = 7
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 23
        byte = 2
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1


class EcmChas2Fr60:
    msg_name = "EcmChas2Fr60"
    msg_id = 1177
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 1.0
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']
    sig_group_dict = {'ThermMgmtObsrvn4': ['ThermMgmtObsrvn4Byte0', 'ThermMgmtObsrvn4Byte1', 'ThermMgmtObsrvn4Byte2', 'ThermMgmtObsrvn4Byte3', 'ThermMgmtObsrvn4Byte4', 'ThermMgmtObsrvn4Byte5', 'ThermMgmtObsrvn4Byte6', 'ThermMgmtObsrvn4Byte7']}
    sig_group_dataid_dict = {}

    class ThermMgmtObsrvn4Byte7:
        sig_name = "ThermMgmtObsrvn4Byte7"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn4Byte3:
        sig_name = "ThermMgmtObsrvn4Byte3"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn4Byte0:
        sig_name = "ThermMgmtObsrvn4Byte0"
        sig_start_bit = 7
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
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn4Byte5:
        sig_name = "ThermMgmtObsrvn4Byte5"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn4Byte2:
        sig_name = "ThermMgmtObsrvn4Byte2"
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

    class ThermMgmtObsrvn4Byte6:
        sig_name = "ThermMgmtObsrvn4Byte6"
        sig_start_bit = 55
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
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn4Byte1:
        sig_name = "ThermMgmtObsrvn4Byte1"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn4Byte4:
        sig_name = "ThermMgmtObsrvn4Byte4"
        sig_start_bit = 39
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
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class SumChas2Fr04:
    msg_name = "SumChas2Fr04"
    msg_id = 431
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "SUM1"
    rx_nodes = ['VDDM', 'ECM']
    sig_group_dict = {'SuspPosnVertRi1': ['SuspPosnVertRi1SuspPosnVertRiChks', 'SuspPosnVertRi1SuspPosnVertRiFrnt', 'SuspPosnVertRi1SuspPosnVertRiFrntQf', 'SuspPosnVertRi1SuspPosnVertRiRe', 'SuspPosnVertRi1SuspPosnVertRiReQf']}
    sig_group_dataid_dict = {}

    class SuspPosnVertRi1SuspPosnVertRiRe:
        sig_name = "SuspPosnVertRi1SuspPosnVertRiRe"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 6.2e-05
        sig_value_offset = 0.0
        sig_value_min = -16129
        sig_value_max = 16130
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111110, 0b00000001, 7, 1)]

    class SuspPosnVertRi1SuspPosnVertRiFrnt:
        sig_name = "SuspPosnVertRi1SuspPosnVertRiFrnt"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 6.2e-05
        sig_value_offset = 0.0
        sig_value_min = -16129
        sig_value_max = 16130
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111110, 0b00000001, 7, 1)]

    class SuspPosnVertRi1SuspPosnVertRiFrntQf:
        sig_name = "SuspPosnVertRi1SuspPosnVertRiFrntQf"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class SuspPosnVertRi1_UB:
        sig_name = "SuspPosnVertRi1_UB"
        sig_start_bit = 43
        update_id_bit = 43
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 43
        byte = 5
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class SuspPosnVertRi1SuspPosnVertRiChks:
        sig_name = "SuspPosnVertRi1SuspPosnVertRiChks"
        sig_start_bit = 39
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
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SuspPosnVertRi1SuspPosnVertRiReQf:
        sig_name = "SuspPosnVertRi1SuspPosnVertRiReQf"
        sig_start_bit = 45
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
        startbit = 45
        byte = 5
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4


class SumChas2Fr10:
    msg_name = "SumChas2Fr10"
    msg_id = 80
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class SUMCtrlSts:
        sig_name = "SUMCtrlSts"
        sig_start_bit = 7
        update_id_bit = 0
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SumCtrlSts_NA': 0, 'SumCtrlSts_Active': 1, 'SumCtrlSts_Idle': 2, 'SumCtrlSts_Error': 3, 'SumCtrlSts_Off': 4, 'SumCtrlSts_Reserved1': 5, 'SumCtrlSts_Reserved2': 6, 'SumCtrlSts_Reserved3': 7}
        compute_method = None
        length = 3
        startbit = 7
        byte = 0
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5


class EcmChas2Fr10:
    msg_name = "EcmChas2Fr10"
    msg_id = 528
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.03
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HvEgyCnsAllwdForClima:
        sig_name = "HvEgyCnsAllwdForClima"
        sig_start_bit = 23
        update_id_bit = 38
        sig_length = 8
        sig_value_factor = 50.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 23
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class PtTqTotDrgAtWhls:
        sig_name = "PtTqTotDrgAtWhls"
        sig_start_bit = 55
        update_id_bit = 35
        sig_length = 16
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = -20000
        sig_value_max = 20000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 55
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class PTStsForRace:
        sig_name = "PTStsForRace"
        sig_start_bit = 34
        update_id_bit = 27
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
        startbit = 34
        byte = 4
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class PtGearRatFrntAct:
        sig_name = "PtGearRatFrntAct"
        sig_start_bit = 3
        update_id_bit = 36
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 3
        bmuws_info = [(0, 0b00001111, 0b11110000, 4, 0), (1, 0b11111111, 0b00000000, 8, 0)]


class EcmChas2Fr28:
    msg_name = "EcmChas2Fr28"
    msg_id = 156
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.015
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']
    sig_group_dict = {'PropLgtCtrlModCfmd': ['PropLgtCtrlModCfmdChks', 'PropLgtCtrlModCfmdCntr', 'PropLgtCtrlModCfmdLgtDegradation', 'PropLgtCtrlModCfmdPropLgtCtrlModCfmd']}
    sig_group_dataid_dict = {'PropLgtCtrlModCfmd': 30}

    class PropLgtCtrlModCfmdChks:
        sig_name = "PropLgtCtrlModCfmdChks"
        sig_start_bit = 7
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
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class PropLgtCtrlModCfmd_UB:
        sig_name = "PropLgtCtrlModCfmd_UB"
        sig_start_bit = 20
        update_id_bit = 20
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 20
        byte = 2
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class PropLgtCtrlModCfmdLgtDegradation:
        sig_name = "PropLgtCtrlModCfmdLgtDegradation"
        sig_start_bit = 11
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LgtDegrad_NoDegradation': 0, 'LgtDegrad_TorqueLimitation': 1, 'LgtDegrad_TotallyFault': 2, 'LgtDegrad_Reserved1': 3, 'LgtDegrad_Reserved2': 4, 'LgtDegrad_Reserved3': 5, 'LgtDegrad_Reserved4': 6, 'LgtDegrad_Reserved5': 7}
        compute_method = None
        length = 3
        startbit = 11
        byte = 1
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class PropLgtCtrlModCfmdPropLgtCtrlModCfmd:
        sig_name = "PropLgtCtrlModCfmdPropLgtCtrlModCfmd"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LgtCtrlModCfmd_NotRequest': 0, 'LgtCtrlModCfmd_MarsParking': 1, 'LgtCtrlModCfmd_APA': 2, 'LgtCtrlModCfmd_RPA': 3, 'LgtCtrlModCfmd_HPA': 4, 'LgtCtrlModCfmd_ANP': 5, 'LgtCtrlModCfmd_E2E': 6, 'LgtCtrlModCfmd_Reserved3': 7}
        compute_method = None
        length = 3
        startbit = 23
        byte = 2
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class PropLgtCtrlModCfmdCntr:
        sig_name = "PropLgtCtrlModCfmdCntr"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4


class VddmChas2Fr80:
    msg_name = "VddmChas2Fr80"
    msg_id = 793
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class RemsSetDchaTarVal:
        sig_name = "RemsSetDchaTarVal"
        sig_start_bit = 19
        update_id_bit = 25
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 19
        bmuws_info = [(2, 0b00001111, 0b11110000, 4, 0), (3, 0b11111100, 0b00000011, 6, 2)]

    class DchaChrgnTarVal:
        sig_name = "DchaChrgnTarVal"
        sig_start_bit = 7
        update_id_bit = 33
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class ChrgnCtrlToEndOrRetartFromApp:
        sig_name = "ChrgnCtrlToEndOrRetartFromApp"
        sig_start_bit = 39
        update_id_bit = 37
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffNoReq_NoReq': 0, 'OnOffNoReq_On': 1, 'OnOffNoReq_Off': 2}
        compute_method = None
        length = 2
        startbit = 39
        byte = 4
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class EcmChas2Fr56:
    msg_name = "EcmChas2Fr56"
    msg_id = 1170
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 1.0
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']
    sig_group_dict = {'ThermMgmtObsrvn1': ['ThermMgmtObsrvn1Byte0', 'ThermMgmtObsrvn1Byte1', 'ThermMgmtObsrvn1Byte2', 'ThermMgmtObsrvn1Byte3', 'ThermMgmtObsrvn1Byte4', 'ThermMgmtObsrvn1Byte5', 'ThermMgmtObsrvn1Byte6', 'ThermMgmtObsrvn1Byte7']}
    sig_group_dataid_dict = {}

    class ThermMgmtObsrvn1Byte5:
        sig_name = "ThermMgmtObsrvn1Byte5"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn1Byte3:
        sig_name = "ThermMgmtObsrvn1Byte3"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn1Byte1:
        sig_name = "ThermMgmtObsrvn1Byte1"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn1Byte6:
        sig_name = "ThermMgmtObsrvn1Byte6"
        sig_start_bit = 55
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
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn1Byte7:
        sig_name = "ThermMgmtObsrvn1Byte7"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn1Byte0:
        sig_name = "ThermMgmtObsrvn1Byte0"
        sig_start_bit = 7
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
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn1Byte2:
        sig_name = "ThermMgmtObsrvn1Byte2"
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

    class ThermMgmtObsrvn1Byte4:
        sig_name = "ThermMgmtObsrvn1Byte4"
        sig_start_bit = 39
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
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class VddmChas2Fr08:
    msg_name = "VddmChas2Fr08"
    msg_id = 928
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.06
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM', 'SUM1']
    sig_group_dict = {'AmbTIndcdWithUnit': ['AmbTIndcdWithUnitAmbTIndcd', 'AmbTIndcdWithUnitAmbTIndcdUnit', 'AmbTIndcdWithUnitQF']}
    sig_group_dataid_dict = {}

    class SetSpdForCrsCtrlFct:
        sig_name = "SetSpdForCrsCtrlFct"
        sig_start_bit = 7
        update_id_bit = 11
        sig_length = 12
        sig_value_factor = 0.03125
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 4000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11110000, 0b00001111, 4, 4)]

    class SpdLimUnit:
        sig_name = "SpdLimUnit"
        sig_start_bit = 49
        update_id_bit = 63
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SpdUnit1_KiloMtrPerHr': 0, 'SpdUnit1_MilePerHr': 1}
        compute_method = None
        length = 1
        startbit = 49
        byte = 6
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class AmbTIndcdWithUnitQF:
        sig_name = "AmbTIndcdWithUnitQF"
        sig_start_bit = 21
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 21
        byte = 2
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class AmbTIndcdWithUnit_UB:
        sig_name = "AmbTIndcdWithUnit_UB"
        sig_start_bit = 9
        update_id_bit = 9
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 9
        byte = 1
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class EpbActrStPrim:
        sig_name = "EpbActrStPrim"
        sig_start_bit = 61
        update_id_bit = 48
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 4
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AppRel_Applied': 0, 'AppRel_Released': 1, 'AppRel_Applying': 2, 'AppRel_Releasing': 3, 'AppRel_Unknown': 4, 'AppRel_HoldApplied': 5, 'AppRel_CompletelyReleased': 6, 'AppRel_HapPrepared': 7}
        compute_method = None
        length = 3
        startbit = 61
        byte = 7
        mask = 0b00111000
        unmask = 0b11000111
        shift = 3

    class AmbTIndcdWithUnitAmbTIndcdUnit:
        sig_name = "AmbTIndcdWithUnitAmbTIndcdUnit"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AmbTIndcdUnit_Celsius': 0, 'AmbTIndcdUnit_Fahrenheit': 1, 'AmbTIndcdUnit_UkwnUnit': 2}
        compute_method = None
        length = 2
        startbit = 23
        byte = 2
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class AmbTIndcdWithUnitAmbTIndcd:
        sig_name = "AmbTIndcdWithUnitAmbTIndcd"
        sig_start_bit = 19
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = -100.0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 1000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 19
        bmuws_info = [(2, 0b00001111, 0b11110000, 4, 0), (3, 0b11111111, 0b00000000, 8, 0)]


class VddmChas2Fr07:
    msg_name = "VddmChas2Fr07"
    msg_id = 320
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.025
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']
    sig_group_dict = {'VehMNom': ['VehMNomTrlrM', 'VehMNomVehM', 'VehMNomVehMQly']}
    sig_group_dataid_dict = {}

    class VehMNom_UB:
        sig_name = "VehMNom_UB"
        sig_start_bit = 34
        update_id_bit = 34
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 34
        byte = 4
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VehMNomVehMQly:
        sig_name = "VehMNomVehMQly"
        sig_start_bit = 49
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Qly2_Flt': 0, 'Qly2_NoInfo': 1, 'Qly2_Vld': 2}
        compute_method = None
        length = 2
        startbit = 49
        byte = 6
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VehMNomTrlrM:
        sig_name = "VehMNomTrlrM"
        sig_start_bit = 33
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TrlrM_Lvl0': 0, 'TrlrM_Lvl1': 1, 'TrlrM_Lvl2': 2, 'TrlrM_Lvl3': 3}
        compute_method = None
        length = 2
        startbit = 33
        byte = 4
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VehMNomVehM:
        sig_name = "VehMNomVehM"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 14
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 10000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 14
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111100, 0b00000011, 6, 2)]

    class DoorLeReSts:
        sig_name = "DoorLeReSts"
        sig_start_bit = 59
        update_id_bit = 57
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorSts2_Ukwn': 0, 'DoorSts2_Opend': 1, 'DoorSts2_Clsd': 2}
        compute_method = None
        length = 2
        startbit = 59
        byte = 7
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class DoorRiReSts:
        sig_name = "DoorRiReSts"
        sig_start_bit = 61
        update_id_bit = 56
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorSts2_Ukwn': 0, 'DoorSts2_Opend': 1, 'DoorSts2_Clsd': 2}
        compute_method = None
        length = 2
        startbit = 61
        byte = 7
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4


class VddmChas2Fr66:
    msg_name = "VddmChas2Fr66"
    msg_id = 579
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.15
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HvahPwrReq:
        sig_name = "HvahPwrReq"
        sig_start_bit = 63
        update_id_bit = 48
        sig_length = 8
        sig_value_factor = 20
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvahHeatgReq:
        sig_name = "HvahHeatgReq"
        sig_start_bit = 52
        update_id_bit = 53
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4


class EcmChas2Fr12:
    msg_name = "EcmChas2Fr12"
    msg_id = 704
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.08
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']
    sig_group_dict = {'ImobEngChk1': ['ImobEngChk1ImobEngChkSts', 'ImobEngChk1ImobEngDataChk0', 'ImobEngChk1ImobEngDataChk1', 'ImobEngChk1ImobEngDataChk2', 'ImobEngChk1ImobEngDataChk3', 'ImobEngChk1ImobEngDataChk4', 'ImobEngChk1ImobEngDataChk5', 'ImobEngChk1ImobEngDataChk6']}
    sig_group_dataid_dict = {}

    class ImobEngChk1ImobEngDataChk0:
        sig_name = "ImobEngChk1ImobEngDataChk0"
        sig_start_bit = 7
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
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ImobEngChk1_UB:
        sig_name = "ImobEngChk1_UB"
        sig_start_bit = 62
        update_id_bit = 62
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 62
        byte = 7
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class ImobEngChk1ImobEngDataChk3:
        sig_name = "ImobEngChk1ImobEngDataChk3"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ImobEngChk1ImobEngDataChk4:
        sig_name = "ImobEngChk1ImobEngDataChk4"
        sig_start_bit = 39
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
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ImobEngChk1ImobEngChkSts:
        sig_name = "ImobEngChk1ImobEngChkSts"
        sig_start_bit = 63
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AvlSts2_NotAvl': 0, 'AvlSts2_Avl': 1}
        compute_method = None
        length = 1
        startbit = 63
        byte = 7
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ImobEngChk1ImobEngDataChk1:
        sig_name = "ImobEngChk1ImobEngDataChk1"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ImobEngChk1ImobEngDataChk2:
        sig_name = "ImobEngChk1ImobEngDataChk2"
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

    class ImobEngChk1ImobEngDataChk5:
        sig_name = "ImobEngChk1ImobEngDataChk5"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ImobEngChk1ImobEngDataChk6:
        sig_name = "ImobEngChk1ImobEngDataChk6"
        sig_start_bit = 55
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
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class EcmChas2Fr33:
    msg_name = "EcmChas2Fr33"
    msg_id = 597
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.15
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class CooltHeatrTOutl:
        sig_name = "CooltHeatrTOutl"
        sig_start_bit = 31
        update_id_bit = 40
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Motorola"
        sig_value_init = 40
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CooltHeatrTIntk:
        sig_name = "CooltHeatrTIntk"
        sig_start_bit = 23
        update_id_bit = 41
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Motorola"
        sig_value_init = 40
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 23
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class EcmChas2Fr02:
    msg_name = "EcmChas2Fr02"
    msg_id = 37
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['BBM', 'VDDM', 'SUM1']
    sig_group_dict = {'PtTqAtWhlReAct': ['PtTqAtWhlReActChks', 'PtTqAtWhlReActCntr', 'PtTqAtWhlReActPtTqAtAxleReAct', 'PtTqAtWhlReActPtTqAtWhlReLeAct', 'PtTqAtWhlReActPtTqAtWhlReRiAct', 'PtTqAtWhlReActPtTqAtWhlsReQly']}
    sig_group_dataid_dict = {'PtTqAtWhlReAct': 89}

    class PtTqAtWhlReAct_UB:
        sig_name = "PtTqAtWhlReAct_UB"
        sig_start_bit = 56
        update_id_bit = 56
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 56
        byte = 7
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class PtTqAtWhlReActPtTqAtWhlReRiAct:
        sig_name = "PtTqAtWhlReActPtTqAtWhlReRiAct"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = -20000
        sig_value_max = 20000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class PtTqAtWhlReActPtTqAtWhlReLeAct:
        sig_name = "PtTqAtWhlReActPtTqAtWhlReLeAct"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = -20000
        sig_value_max = 20000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class PtTqAtWhlReActChks:
        sig_name = "PtTqAtWhlReActChks"
        sig_start_bit = 55
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
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class PtTqAtWhlReActPtTqAtAxleReAct:
        sig_name = "PtTqAtWhlReActPtTqAtAxleReAct"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = -20000
        sig_value_max = 20000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class PtTqAtWhlReActPtTqAtWhlsReQly:
        sig_name = "PtTqAtWhlReActPtTqAtWhlsReQly"
        sig_start_bit = 59
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Qly3_De0': 0, 'Qly3_De1': 1, 'Qly3_De2': 2, 'Qly3_De3': 3, 'Qly3_De4': 4, 'Qly3_De5': 5, 'Qly3_De6': 6, 'Qly3_De7': 7}
        compute_method = None
        length = 3
        startbit = 59
        byte = 7
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class PtTqAtWhlReActCntr:
        sig_name = "PtTqAtWhlReActCntr"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4


class EcmChas2Fr01:
    msg_name = "EcmChas2Fr01"
    msg_id = 128
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['BBM', 'VDDM', 'SUM1']
    sig_group_dict = {'PtTqAtWhlFrntAct': ['PtTqAtWhlFrntActChks', 'PtTqAtWhlFrntActCntr', 'PtTqAtWhlFrntActPtTqAtAxleFrntAct', 'PtTqAtWhlFrntActPtTqAtWhlFrntLeAct', 'PtTqAtWhlFrntActPtTqAtWhlFrntRiAct', 'PtTqAtWhlFrntActPtTqAtWhlsFrntQly']}
    sig_group_dataid_dict = {'PtTqAtWhlFrntAct': 78}

    class PtTqAtWhlFrntActPtTqAtAxleFrntAct:
        sig_name = "PtTqAtWhlFrntActPtTqAtAxleFrntAct"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = -20000
        sig_value_max = 20000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class PtTqAtWhlFrntActPtTqAtWhlFrntLeAct:
        sig_name = "PtTqAtWhlFrntActPtTqAtWhlFrntLeAct"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = -20000
        sig_value_max = 20000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class PtTqAtWhlFrntActPtTqAtWhlFrntRiAct:
        sig_name = "PtTqAtWhlFrntActPtTqAtWhlFrntRiAct"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = -20000
        sig_value_max = 20000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class PtTqAtWhlFrntAct_UB:
        sig_name = "PtTqAtWhlFrntAct_UB"
        sig_start_bit = 56
        update_id_bit = 56
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 56
        byte = 7
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class PtTqAtWhlFrntActPtTqAtWhlsFrntQly:
        sig_name = "PtTqAtWhlFrntActPtTqAtWhlsFrntQly"
        sig_start_bit = 59
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Qly3_De0': 0, 'Qly3_De1': 1, 'Qly3_De2': 2, 'Qly3_De3': 3, 'Qly3_De4': 4, 'Qly3_De5': 5, 'Qly3_De6': 6, 'Qly3_De7': 7}
        compute_method = None
        length = 3
        startbit = 59
        byte = 7
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class PtTqAtWhlFrntActCntr:
        sig_name = "PtTqAtWhlFrntActCntr"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class PtTqAtWhlFrntActChks:
        sig_name = "PtTqAtWhlFrntActChks"
        sig_start_bit = 55
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
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class VddmChas2Fr28:
    msg_name = "VddmChas2Fr28"
    msg_id = 688
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']
    sig_group_dict = {'ImobEngMgrReq1': ['ImobEngMgrReq1ImobEngDataMgrReq0', 'ImobEngMgrReq1ImobEngDataMgrReq1', 'ImobEngMgrReq1ImobEngDataMgrReq2', 'ImobEngMgrReq1ImobEngDataMgrReq3', 'ImobEngMgrReq1ImobEngDataMgrReq4', 'ImobEngMgrReq1ImobEngDataMgrReq5', 'ImobEngMgrReq1ImobEngDataMgrReq6', 'ImobEngMgrReq1ImobEngMgrCmdTar1']}
    sig_group_dataid_dict = {}

    class ImobEngMgrReq1_UB:
        sig_name = "ImobEngMgrReq1_UB"
        sig_start_bit = 2
        update_id_bit = 2
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 2
        byte = 0
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class ImobEngMgrReq1ImobEngDataMgrReq5:
        sig_name = "ImobEngMgrReq1ImobEngDataMgrReq5"
        sig_start_bit = 55
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
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ImobEngMgrReq1ImobEngDataMgrReq1:
        sig_name = "ImobEngMgrReq1ImobEngDataMgrReq1"
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

    class ImobEngMgrReq1ImobEngDataMgrReq6:
        sig_name = "ImobEngMgrReq1ImobEngDataMgrReq6"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ImobEngMgrReq1ImobEngDataMgrReq2:
        sig_name = "ImobEngMgrReq1ImobEngDataMgrReq2"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ImobEngMgrReq1ImobEngDataMgrReq0:
        sig_name = "ImobEngMgrReq1ImobEngDataMgrReq0"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ImobEngMgrReq1ImobEngMgrCmdTar1:
        sig_name = "ImobEngMgrReq1ImobEngMgrCmdTar1"
        sig_start_bit = 1
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ImobEngMgrReqCmd_ImobEngCmdTarIdle': 0, 'ImobEngMgrReqCmd_ImobEngMtnStrtReqCmd': 1, 'ImobEngMgrReqCmd_ImobEngNoMtnStrtReqCmd': 2, 'ImobEngMgrReqCmd_ImobEngTurnOffCmd': 3}
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class ImobEngMgrReq1ImobEngDataMgrReq3:
        sig_name = "ImobEngMgrReq1ImobEngDataMgrReq3"
        sig_start_bit = 39
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
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ImobEngMgrReq1ImobEngDataMgrReq4:
        sig_name = "ImobEngMgrReq1ImobEngDataMgrReq4"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class VddmChas2Fr77:
    msg_name = "VddmChas2Fr77"
    msg_id = 769
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.3
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HvahAirTsp:
        sig_name = "HvahAirTsp"
        sig_start_bit = 50
        update_id_bit = 51
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 600
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 50
        bmuws_info = [(6, 0b00000111, 0b11111000, 3, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class HpReqCritSts:
        sig_name = "HpReqCritSts"
        sig_start_bit = 47
        update_id_bit = 46
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 47
        byte = 5
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class HvacTempFlapActlPosnFrstRowLe:
        sig_name = "HvacTempFlapActlPosnFrstRowLe"
        sig_start_bit = 7
        update_id_bit = 41
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class HvacTempFlapActlPosnSecRowLe:
        sig_name = "HvacTempFlapActlPosnSecRowLe"
        sig_start_bit = 19
        update_id_bit = 55
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 19
        bmuws_info = [(2, 0b00001111, 0b11110000, 4, 0), (3, 0b11111100, 0b00000011, 6, 2)]

    class HvacTempFlapActlPosnSecRowRi:
        sig_name = "HvacTempFlapActlPosnSecRowRi"
        sig_start_bit = 25
        update_id_bit = 54
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 25
        bmuws_info = [(3, 0b00000011, 0b11111100, 2, 0), (4, 0b11111111, 0b00000000, 8, 0)]

    class HvacTempFlapActlPosnFrstRowRi:
        sig_name = "HvacTempFlapActlPosnFrstRowRi"
        sig_start_bit = 13
        update_id_bit = 40
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 13
        bmuws_info = [(1, 0b00111111, 0b11000000, 6, 0), (2, 0b11110000, 0b00001111, 4, 4)]


class VddmToSumChas2DiagReqFrame:
    msg_name = "VddmToSumChas2DiagReqFrame"
    msg_id = 1812
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['SUM1']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class VddmChas2Fr32:
    msg_name = "VddmChas2Fr32"
    msg_id = 464
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.03
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']
    sig_group_dict = {'EscSt': ['EscStChks', 'EscStCntr', 'EscStEscSt'], 'SpdRotlForWhlsAtAxleFrnt': ['SpdRotlForWhlsAtAxleFrntChks', 'SpdRotlForWhlsAtAxleFrntCntr', 'SpdRotlForWhlsAtAxleFrntSpdRotlForWhlsAtAxleFrnt'], 'VehSpdIndcd': ['VehSpdIndcdVehSpdIndcd', 'VehSpdIndcdVeSpdIndcdUnit']}
    sig_group_dataid_dict = {'EscSt': 127, 'SpdRotlForWhlsAtAxleFrnt': 53}

    class EscCtrlIndcn:
        sig_name = "EscCtrlIndcn"
        sig_start_bit = 27
        update_id_bit = 25
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts1_On': 0, 'DevSts1_Off': 1, 'DevSts1_Flt': 2}
        compute_method = None
        length = 2
        startbit = 27
        byte = 3
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class EscStCntr:
        sig_name = "EscStCntr"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class SpdRotlForWhlsAtAxleFrntSpdRotlForWhlsAtAxleFrnt:
        sig_name = "SpdRotlForWhlsAtAxleFrntSpdRotlForWhlsAtAxleFrnt"
        sig_start_bit = 6
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 0.5
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 32767
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 6
        bmuws_info = [(0, 0b01111111, 0b10000000, 7, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class EscStChks:
        sig_name = "EscStChks"
        sig_start_bit = 55
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
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SpdRotlForWhlsAtAxleFrntChks:
        sig_name = "SpdRotlForWhlsAtAxleFrntChks"
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

    class SpdRotlForWhlsAtAxleFrntCntr:
        sig_name = "SpdRotlForWhlsAtAxleFrntCntr"
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

    class EscSt_UB:
        sig_name = "EscSt_UB"
        sig_start_bit = 56
        update_id_bit = 56
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 56
        byte = 7
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class SpdRotlForWhlsAtAxleFrnt_UB:
        sig_name = "SpdRotlForWhlsAtAxleFrnt_UB"
        sig_start_bit = 7
        update_id_bit = 7
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VehSpdIndcdVeSpdIndcdUnit:
        sig_name = "VehSpdIndcdVeSpdIndcdUnit"
        sig_start_bit = 34
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VehSpdIndcdUnit_Kmph': 0, 'VehSpdIndcdUnit_Mph': 1, 'VehSpdIndcdUnit_UkwnUnit': 2}
        compute_method = None
        length = 2
        startbit = 34
        byte = 4
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class EscStEscSt:
        sig_name = "EscStEscSt"
        sig_start_bit = 59
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EscSt1_Inin': 0, 'EscSt1_Ok': 1, 'EscSt1_TmpErr': 2, 'EscSt1_PrmntErr': 3, 'EscSt1_UsrOff': 4}
        compute_method = None
        length = 3
        startbit = 59
        byte = 7
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class VehSpdIndcd_UB:
        sig_name = "VehSpdIndcd_UB"
        sig_start_bit = 35
        update_id_bit = 35
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 35
        byte = 4
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VehSpdIndcdVehSpdIndcd:
        sig_name = "VehSpdIndcdVehSpdIndcd"
        sig_start_bit = 32
        update_id_bit = None
        sig_length = 9
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 32
        bmuws_info = [(4, 0b00000001, 0b11111110, 1, 0), (5, 0b11111111, 0b00000000, 8, 0)]


class EcmChas2Fr08:
    msg_name = "EcmChas2Fr08"
    msg_id = 352
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class AdjSpdLimnMsg:
        sig_name = "AdjSpdLimnMsg"
        sig_start_bit = 62
        update_id_bit = 60
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AdjSpdLimnMsg1_NoMsg0': 0, 'AdjSpdLimnMsg1_AdjSpdLimnCncl': 1, 'AdjSpdLimnMsg1_AdjSpdLimnInhb': 2, 'AdjSpdLimnMsg1_AVSLDegradated': 3}
        compute_method = None
        length = 2
        startbit = 62
        byte = 7
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class CrsCtrlrMsg:
        sig_name = "CrsCtrlrMsg"
        sig_start_bit = 59
        update_id_bit = 56
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CrsCtrlrMsg1_NoMsg': 0, 'CrsCtrlrMsg1_CrsCtrlrCncl': 1, 'CrsCtrlrMsg1_OvrdTiMaxExcdd': 2, 'CrsCtrlrMsg1_CrsCtrlrInhb': 3, 'CrsCtrlrMsg1_SpdLoLimExcdd': 4, 'CrsCtrlrMsg1_CrsCtrlrCnclSpdLoLimExcdd': 5, 'CrsCtrlrMsg1_DrvModSeldNotOk': 6, 'CrsCtrlrMsg1_BrkOvrheatd': 7}
        compute_method = None
        length = 3
        startbit = 59
        byte = 7
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1


class SumChas2Fr08:
    msg_name = "SumChas2Fr08"
    msg_id = 98
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "SUM1"
    rx_nodes = ['CCM']
    sig_group_dict = {'SuspFailrSts2': ['SuspFailrSts2SuspFailrSts', 'SuspFailrSts2SuspFailrStsChks', 'SuspFailrSts2SuspFailrStsCntr', 'SuspFailrSts2SuspFailrStsTypQf']}
    sig_group_dataid_dict = {}

    class SuspFailrSts2SuspFailrSts:
        sig_name = "SuspFailrSts2SuspFailrSts"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 11
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SuspFailrStsTyp3_NoErr': 0, 'SuspFailrStsTyp3_TrSwtConUsg': 1, 'SuspFailrStsTyp3_CmprOvrheated': 2, 'SuspFailrStsTyp3_SrvRqrdErr': 3, 'SuspFailrStsTyp3_StopCritErr': 4, 'SuspFailrStsTyp3_LoAirM': 5, 'SuspFailrStsTyp3_HiAirM': 6, 'SuspFailrStsTyp3_VehLvlHiOrLoErr': 7, 'SuspFailrStsTyp3_ARCLoSts': 8, 'SuspFailrStsTyp3_ARCOffSts': 9, 'SuspFailrStsTyp3_CCDOffSts': 10, 'SuspFailrStsTyp3_VehOvrLd': 11}
        compute_method = None
        length = 4
        startbit = 47
        byte = 5
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class SuspFailrSts2SuspFailrStsChks:
        sig_name = "SuspFailrSts2SuspFailrStsChks"
        sig_start_bit = 55
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
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SuspFailrSts2SuspFailrStsTypQf:
        sig_name = "SuspFailrSts2SuspFailrStsTypQf"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class SuspFailrSts2_UB:
        sig_name = "SuspFailrSts2_UB"
        sig_start_bit = 61
        update_id_bit = 61
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 61
        byte = 7
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class SuspFailrSts2SuspFailrStsCntr:
        sig_name = "SuspFailrSts2SuspFailrStsCntr"
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


class BgmChassisCAN2NmFr:
    msg_name = "BgmChassisCAN2NmFr"
    msg_id = 1281
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class EcmChas2Fr17:
    msg_name = "EcmChas2Fr17"
    msg_id = 848
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.4
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']
    sig_group_dict = {'CoolgLoadGroup': ['CoolgLoadGroupCoolgLimd', 'CoolgLoadGroupCoolgLoad2']}
    sig_group_dataid_dict = {}

    class DstEstimdToEmptyForDrvgElec:
        sig_name = "DstEstimdToEmptyForDrvgElec"
        sig_start_bit = 7
        update_id_bit = 10
        sig_length = 10
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class EcmRoilgCntr:
        sig_name = "EcmRoilgCntr"
        sig_start_bit = 23
        update_id_bit = 8
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

    class CoolgLoadGroup_UB:
        sig_name = "CoolgLoadGroup_UB"
        sig_start_bit = 60
        update_id_bit = 60
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 60
        byte = 7
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class CoolgLoadGroupCoolgLimd:
        sig_name = "CoolgLoadGroupCoolgLimd"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flg1_Rst': 0, 'Flg1_Set': 1}
        compute_method = None
        length = 1
        startbit = 39
        byte = 4
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class CoolgLoadGroupCoolgLoad2:
        sig_name = "CoolgLoadGroupCoolgLoad2"
        sig_start_bit = 38
        update_id_bit = None
        sig_length = 7
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 38
        byte = 4
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class HvClimaCmd:
        sig_name = "HvClimaCmd"
        sig_start_bit = 55
        update_id_bit = 59
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HVBattChargnCmd_OK': 0, 'HVBattChargnCmd_NOK': 1, 'HVBattChargnCmd_INIT': 2, 'HVBattChargnCmd_HOLD': 3}
        compute_method = None
        length = 2
        startbit = 55
        byte = 6
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class UBoostReqByPt:
        sig_name = "UBoostReqByPt"
        sig_start_bit = 53
        update_id_bit = 58
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'UBoostReq_NoOper': 0, 'UBoostReq_InhbDcha': 1, 'UBoostReq_RgnChrgDi': 2, 'UBoostReq_UMax': 3}
        compute_method = None
        length = 2
        startbit = 53
        byte = 6
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class PtCoolgPostRunActv:
        sig_name = "PtCoolgPostRunActv"
        sig_start_bit = 56
        update_id_bit = 57
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 56
        byte = 7
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class HzrdLiIndcnReq:
        sig_name = "HzrdLiIndcnReq"
        sig_start_bit = 49
        update_id_bit = 48
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 49
        byte = 6
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1


class VddmChas2Fr68:
    msg_name = "VddmChas2Fr68"
    msg_id = 1059
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class IntelliClimaResd7:
        sig_name = "IntelliClimaResd7"
        sig_start_bit = 47
        update_id_bit = 61
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111111, 0b00000000, 8, 0)]

    class IntelliClimaResd2:
        sig_name = "IntelliClimaResd2"
        sig_start_bit = 7
        update_id_bit = 63
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
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class IntelliClimaResd12:
        sig_name = "IntelliClimaResd12"
        sig_start_bit = 15
        update_id_bit = 62
        sig_length = 32
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 32
        startbit = 15
        bmuws_info = [(1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111111, 0b00000000, 8, 0)]


class VddmToAllChas2DiagReqFrame:
    msg_name = "VddmToAllChas2DiagReqFrame"
    msg_id = 2047
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['SUM1']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class VddmChas2Fr46:
    msg_name = "VddmChas2Fr46"
    msg_id = 26
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['BBM']
    sig_group_dict = {'WhlDirRotlFrnt': ['WhlDirRotlFrntChks', 'WhlDirRotlFrntCntr', 'WhlDirRotlFrntLe', 'WhlDirRotlFrntRi'], 'BrkFAct2': ['BrkFAct2AutParkBrkSpprtReq', 'BrkFAct2Chks', 'BrkFAct2Cntr', 'BrkFAct2Force'], 'WhlDirRotlRe': ['WhlDirRotlReChks', 'WhlDirRotlReCntr', 'WhlDirRotlReLe', 'WhlDirRotlReRi']}
    sig_group_dataid_dict = {'WhlDirRotlFrnt': 552, 'BrkFAct2': 1069, 'WhlDirRotlRe': 551}

    class WhlDirRotlFrntRi:
        sig_name = "WhlDirRotlFrntRi"
        sig_start_bit = 45
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WhlRotlDirStd1_Undefd': 0, 'WhlRotlDirStd1_StandStill': 1, 'WhlRotlDirStd1_Fwd': 2, 'WhlRotlDirStd1_Backw': 3}
        compute_method = None
        length = 2
        startbit = 45
        byte = 5
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class BrkFAct2Chks:
        sig_name = "BrkFAct2Chks"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class WhlDirRotlFrntChks:
        sig_name = "WhlDirRotlFrntChks"
        sig_start_bit = 39
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
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class WhlDirRotlFrnt_UB:
        sig_name = "WhlDirRotlFrnt_UB"
        sig_start_bit = 7
        update_id_bit = 7
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class BrkFAct2Cntr:
        sig_name = "BrkFAct2Cntr"
        sig_start_bit = 3
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
        startbit = 3
        byte = 0
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class WhlDirRotlReChks:
        sig_name = "WhlDirRotlReChks"
        sig_start_bit = 55
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
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BrkFAct2Force:
        sig_name = "BrkFAct2Force"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class BrkFAct2_UB:
        sig_name = "BrkFAct2_UB"
        sig_start_bit = 5
        update_id_bit = 5
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class WhlDirRotlReCntr:
        sig_name = "WhlDirRotlReCntr"
        sig_start_bit = 59
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
        startbit = 59
        byte = 7
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class WhlDirRotlReRi:
        sig_name = "WhlDirRotlReRi"
        sig_start_bit = 61
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WhlRotlDirStd1_Undefd': 0, 'WhlRotlDirStd1_StandStill': 1, 'WhlRotlDirStd1_Fwd': 2, 'WhlRotlDirStd1_Backw': 3}
        compute_method = None
        length = 2
        startbit = 61
        byte = 7
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class WhlDirRotlRe_UB:
        sig_name = "WhlDirRotlRe_UB"
        sig_start_bit = 6
        update_id_bit = 6
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class WhlDirRotlFrntLe:
        sig_name = "WhlDirRotlFrntLe"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WhlRotlDirStd1_Undefd': 0, 'WhlRotlDirStd1_StandStill': 1, 'WhlRotlDirStd1_Fwd': 2, 'WhlRotlDirStd1_Backw': 3}
        compute_method = None
        length = 2
        startbit = 47
        byte = 5
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class BrkFAct2AutParkBrkSpprtReq:
        sig_name = "BrkFAct2AutParkBrkSpprtReq"
        sig_start_bit = 4
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ReqSts1_NotReqd': 0, 'ReqSts1_Reqd': 1}
        compute_method = None
        length = 1
        startbit = 4
        byte = 0
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class WhlDirRotlReLe:
        sig_name = "WhlDirRotlReLe"
        sig_start_bit = 63
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WhlRotlDirStd1_Undefd': 0, 'WhlRotlDirStd1_StandStill': 1, 'WhlRotlDirStd1_Fwd': 2, 'WhlRotlDirStd1_Backw': 3}
        compute_method = None
        length = 2
        startbit = 63
        byte = 7
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class WhlDirRotlFrntCntr:
        sig_name = "WhlDirRotlFrntCntr"
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


class VddmChas2Fr43:
    msg_name = "VddmChas2Fr43"
    msg_id = 501
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.04
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']
    sig_group_dict = {'WhlSpdCalcALgt': ['WhlSpdCalcALgtALgt', 'WhlSpdCalcALgtChks', 'WhlSpdCalcALgtCntr']}
    sig_group_dataid_dict = {'WhlSpdCalcALgt': 248}

    class WhlSpdCalcALgtCntr:
        sig_name = "WhlSpdCalcALgtCntr"
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

    class WhlSpdCalcALgt_UB:
        sig_name = "WhlSpdCalcALgt_UB"
        sig_start_bit = 6
        update_id_bit = 6
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class WhlSpdCalcALgtChks:
        sig_name = "WhlSpdCalcALgtChks"
        sig_start_bit = 55
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
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class WhlSpdCalcALgtALgt:
        sig_name = "WhlSpdCalcALgtALgt"
        sig_start_bit = 35
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.0059
        sig_value_offset = 0.0
        sig_value_min = -2033
        sig_value_max = 2034
        sig_byteorder = "Motorola"
        sig_value_init = 1017
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 35
        bmuws_info = [(4, 0b00001111, 0b11110000, 4, 0), (5, 0b11111111, 0b00000000, 8, 0)]


class VddmChas2Fr67:
    msg_name = "VddmChas2Fr67"
    msg_id = 1058
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class IntelliClimaResd11:
        sig_name = "IntelliClimaResd11"
        sig_start_bit = 15
        update_id_bit = 62
        sig_length = 32
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 32
        startbit = 15
        bmuws_info = [(1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111111, 0b00000000, 8, 0)]

    class IntelliClimaResd1:
        sig_name = "IntelliClimaResd1"
        sig_start_bit = 7
        update_id_bit = 63
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
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class IntelliClimaResd6:
        sig_name = "IntelliClimaResd6"
        sig_start_bit = 47
        update_id_bit = 61
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111111, 0b00000000, 8, 0)]


class EcmChas2Fr37:
    msg_name = "EcmChas2Fr37"
    msg_id = 785
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.23
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class TInCooltAtStrtOfClima:
        sig_name = "TInCooltAtStrtOfClima"
        sig_start_bit = 31
        update_id_bit = 39
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 40
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CmprSpdAct:
        sig_name = "CmprSpdAct"
        sig_start_bit = 7
        update_id_bit = 15
        sig_length = 8
        sig_value_factor = 50.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 254
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


class EcmChas2Fr55:
    msg_name = "EcmChas2Fr55"
    msg_id = 69
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['BBM', 'VDDM']
    sig_group_dict = {'PtBrkTqCpTot': ['PtBrkTqCpTot1', 'PtBrkTqCpTotQf'], 'DrvrGearShiftParkReq': ['DrvrGearShiftParkReq1', 'DrvrGearShiftParkReqChks', 'DrvrGearShiftParkReqCntr', 'DrvrGearShiftParkReqSts']}
    sig_group_dataid_dict = {'DrvrGearShiftParkReq': 527}

    class DrvrGearShiftParkReq1:
        sig_name = "DrvrGearShiftParkReq1"
        sig_start_bit = 54
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SwtPark1_SwtParkNotActv': 0, 'SwtPark1_SwtParkActv': 1}
        compute_method = None
        length = 1
        startbit = 54
        byte = 6
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class PtTqAtAxleAvlReMin:
        sig_name = "PtTqAtAxleAvlReMin"
        sig_start_bit = 31
        update_id_bit = 32
        sig_length = 15
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = -16384
        sig_value_max = 16380
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111110, 0b00000001, 7, 1)]

    class PtBrkTqCpTot1:
        sig_name = "PtBrkTqCpTot1"
        sig_start_bit = 6
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = -16384
        sig_value_max = 16380
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 6
        bmuws_info = [(0, 0b01111111, 0b10000000, 7, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class PtBrkTqCpTot_UB:
        sig_name = "PtBrkTqCpTot_UB"
        sig_start_bit = 7
        update_id_bit = 7
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class DrvrGearShiftParkReq_UB:
        sig_name = "DrvrGearShiftParkReq_UB"
        sig_start_bit = 55
        update_id_bit = 55
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 55
        byte = 6
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class DrvrGearShiftParkReqCntr:
        sig_name = "DrvrGearShiftParkReqCntr"
        sig_start_bit = 51
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
        startbit = 51
        byte = 6
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class PtBrkTqCpTotQf:
        sig_name = "PtBrkTqCpTotQf"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Qf1_DevOfDataUndefd': 0, 'Qf1_DataTmpUndefdAndEvlnInProgs': 1, 'Qf1_DevOfDataNotWithinRngAllwd': 2, 'Qf1_DataCalcdWithDevDefd': 3}
        compute_method = None
        length = 2
        startbit = 23
        byte = 2
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class DrvrGearShiftParkReqSts:
        sig_name = "DrvrGearShiftParkReqSts"
        sig_start_bit = 53
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ClutchPedlPsd_No': 0, 'ClutchPedlPsd_Yes': 1, 'ClutchPedlPsd_Reserved1': 2, 'ClutchPedlPsd_Reserved2': 3}
        compute_method = None
        length = 2
        startbit = 53
        byte = 6
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class DrvrGearShiftParkReqChks:
        sig_name = "DrvrGearShiftParkReqChks"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class EcmChas2Fr22:
    msg_name = "EcmChas2Fr22"
    msg_id = 570
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.04
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']
    sig_group_dict = {'BrkLiReqRegen': ['BrkLiReqRegenChks', 'BrkLiReqRegenCntr', 'BrkLiReqRegenOnOff'], 'ADModCtrlInhbn': ['ADModCtrlInhbnADModCtrlInhbn', 'ADModCtrlInhbnChks', 'ADModCtrlInhbnCntr'], 'ParkByDrvrWhlsFrntSafe': ['ParkByDrvrWhlsFrntSafeChks', 'ParkByDrvrWhlsFrntSafeCntr', 'ParkByDrvrWhlsFrntSafeSts']}
    sig_group_dataid_dict = {'BrkLiReqRegen': 7007, 'ADModCtrlInhbn': 62, 'ParkByDrvrWhlsFrntSafe': 165}

    class ADModCtrlInhbnADModCtrlInhbn:
        sig_name = "ADModCtrlInhbnADModCtrlInhbn"
        sig_start_bit = 14
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoInhb': 0, 'L12LgtCtrlModInhb': 1, 'AutoParkingModInhb': 2, 'L12AndAutoParkingModInhb': 3, 'L3ADModInhb': 4, 'L3ADAndL12LgtCtrlModInhb': 5, 'L3ADAndAutoParkingModInhb': 6, 'L3ADAndAutoParkingAndL12LgtCtrlModInhb': 7}
        compute_method = None
        length = 3
        startbit = 14
        byte = 1
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class ADModCtrlInhbnCntr:
        sig_name = "ADModCtrlInhbnCntr"
        sig_start_bit = 11
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
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class BrkLiReqRegen_UB:
        sig_name = "BrkLiReqRegen_UB"
        sig_start_bit = 29
        update_id_bit = 29
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 29
        byte = 3
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class CnclWarnForCrsCtrl:
        sig_name = "CnclWarnForCrsCtrl"
        sig_start_bit = 6
        update_id_bit = 7
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoYesCrit1_NotVld1': 0, 'NoYesCrit1_No': 1, 'NoYesCrit1_Yes': 2, 'NoYesCrit1_NotVld2': 3}
        compute_method = None
        length = 2
        startbit = 6
        byte = 0
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class ParkByDrvrWhlsFrntSafeChks:
        sig_name = "ParkByDrvrWhlsFrntSafeChks"
        sig_start_bit = 55
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
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ADModCtrlInhbn_UB:
        sig_name = "ADModCtrlInhbn_UB"
        sig_start_bit = 15
        update_id_bit = 15
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 15
        byte = 1
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ParkByDrvrWhlsFrntSafeCntr:
        sig_name = "ParkByDrvrWhlsFrntSafeCntr"
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

    class ADModCtrlInhbnChks:
        sig_name = "ADModCtrlInhbnChks"
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

    class BrkLiReqRegenOnOff:
        sig_name = "BrkLiReqRegenOnOff"
        sig_start_bit = 28
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 28
        byte = 3
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class BrkLiReqRegenChks:
        sig_name = "BrkLiReqRegenChks"
        sig_start_bit = 39
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
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BrkLiReqRegenCntr:
        sig_name = "BrkLiReqRegenCntr"
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

    class ParkByDrvrWhlsFrntSafeSts:
        sig_name = "ParkByDrvrWhlsFrntSafeSts"
        sig_start_bit = 44
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flg1_Rst': 0, 'Flg1_Set': 1}
        compute_method = None
        length = 1
        startbit = 44
        byte = 5
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class ParkByDrvrWhlsFrntSafe_UB:
        sig_name = "ParkByDrvrWhlsFrntSafe_UB"
        sig_start_bit = 45
        update_id_bit = 45
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 45
        byte = 5
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5


class EtcBbmChas2DevFr01:
    msg_name = "EtcBbmChas2DevFr01"
    msg_id = 1427
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CCM"
    rx_nodes = ['BBM']
    sig_group_dict = {'BBMdevelpsignalgroupreq1': ['BBMdevelpsignalgroupreq1Functiondevpsignalgroup1', 'BBMdevelpsignalgroupreq1Functiondevpsignalgroup2', 'BBMdevelpsignalgroupreq1Functiondevpsignalgroup3', 'BBMdevelpsignalgroupreq1Functiondevpsignalgroup4', 'BBMdevelpsignalgroupreq1Functiondevpsignalgroup5', 'BBMdevelpsignalgroupreq1Functiondevpsignalgroup6', 'BBMdevelpsignalgroupreq1Functiondevpsignalgroup7', 'BBMdevelpsignalgroupreq1Functiondevpsignalgroup8']}
    sig_group_dataid_dict = {}

    class BBMdevelpsignalgroupreq1Functiondevpsignalgroup2:
        sig_name = "BBMdevelpsignalgroupreq1Functiondevpsignalgroup2"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BBMdevelpsignalgroupreq1Functiondevpsignalgroup4:
        sig_name = "BBMdevelpsignalgroupreq1Functiondevpsignalgroup4"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BBMdevelpsignalgroupreq1Functiondevpsignalgroup1:
        sig_name = "BBMdevelpsignalgroupreq1Functiondevpsignalgroup1"
        sig_start_bit = 7
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
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BBMdevelpsignalgroupreq1Functiondevpsignalgroup7:
        sig_name = "BBMdevelpsignalgroupreq1Functiondevpsignalgroup7"
        sig_start_bit = 55
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
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BBMdevelpsignalgroupreq1Functiondevpsignalgroup5:
        sig_name = "BBMdevelpsignalgroupreq1Functiondevpsignalgroup5"
        sig_start_bit = 39
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
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BBMdevelpsignalgroupreq1Functiondevpsignalgroup6:
        sig_name = "BBMdevelpsignalgroupreq1Functiondevpsignalgroup6"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BBMdevelpsignalgroupreq1Functiondevpsignalgroup8:
        sig_name = "BBMdevelpsignalgroupreq1Functiondevpsignalgroup8"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BBMdevelpsignalgroupreq1Functiondevpsignalgroup3:
        sig_name = "BBMdevelpsignalgroupreq1Functiondevpsignalgroup3"
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


class EcmChas2Fr45:
    msg_name = "EcmChas2Fr45"
    msg_id = 1136
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 1.0
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class EcmIntelliClimaResd1:
        sig_name = "EcmIntelliClimaResd1"
        sig_start_bit = 7
        update_id_bit = 63
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
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class EcmIntelliClimaResd6:
        sig_name = "EcmIntelliClimaResd6"
        sig_start_bit = 47
        update_id_bit = 58
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111111, 0b00000000, 8, 0)]

    class EcmIntelliClimaResd5:
        sig_name = "EcmIntelliClimaResd5"
        sig_start_bit = 39
        update_id_bit = 59
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
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class EcmIntelliClimaResd3:
        sig_name = "EcmIntelliClimaResd3"
        sig_start_bit = 23
        update_id_bit = 61
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

    class EcmIntelliClimaResd2:
        sig_name = "EcmIntelliClimaResd2"
        sig_start_bit = 15
        update_id_bit = 62
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class EcmIntelliClimaResd4:
        sig_name = "EcmIntelliClimaResd4"
        sig_start_bit = 31
        update_id_bit = 60
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class VddmChas2Fr04:
    msg_name = "VddmChas2Fr04"
    msg_id = 208
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.015
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']
    sig_group_dict = {'BltLockStAtDrvr': ['BltLockStAtDrvrBltLockSt1', 'BltLockStAtDrvrBltLockSts'], 'PtTqSoftMaxGenn2': ['PtTqSoftMaxGenn2Allwd', 'PtTqSoftMaxGenn2AllwdChks', 'PtTqSoftMaxGenn2AllwdCntr']}
    sig_group_dataid_dict = {'PtTqSoftMaxGenn2': 219}

    class PtTqSoftMaxGenn2AllwdChks:
        sig_name = "PtTqSoftMaxGenn2AllwdChks"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BltLockStAtDrvr_UB:
        sig_name = "BltLockStAtDrvr_UB"
        sig_start_bit = 20
        update_id_bit = 20
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 20
        byte = 2
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class BltLockStAtDrvrBltLockSt1:
        sig_name = "BltLockStAtDrvrBltLockSt1"
        sig_start_bit = 19
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BltLockSt1_Unlock': 0, 'BltLockSt1_Lock': 1}
        compute_method = None
        length = 1
        startbit = 19
        byte = 2
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class PtTqSoftMaxGenn2_UB:
        sig_name = "PtTqSoftMaxGenn2_UB"
        sig_start_bit = 17
        update_id_bit = 17
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 17
        byte = 2
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class PrpsnTqForBrkRels:
        sig_name = "PrpsnTqForBrkRels"
        sig_start_bit = 31
        update_id_bit = 16
        sig_length = 15
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 20000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111110, 0b00000001, 7, 1)]

    class PtTqSoftMaxGenn2Allwd:
        sig_name = "PtTqSoftMaxGenn2Allwd"
        sig_start_bit = 32
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 4.0
        sig_value_offset = 0.0
        sig_value_min = -4096
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 32
        bmuws_info = [(4, 0b00000001, 0b11111110, 1, 0), (5, 0b11111111, 0b00000000, 8, 0), (6, 0b11110000, 0b00001111, 4, 4)]

    class BltLockStAtDrvrBltLockSts:
        sig_name = "BltLockStAtDrvrBltLockSts"
        sig_start_bit = 18
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevErrSts2_NoFlt': 0, 'DevErrSts2_Flt': 1}
        compute_method = None
        length = 1
        startbit = 18
        byte = 2
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class PtTqSoftMaxGenn2AllwdCntr:
        sig_name = "PtTqSoftMaxGenn2AllwdCntr"
        sig_start_bit = 51
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
        startbit = 51
        byte = 6
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0


class VddmChas2Fr33:
    msg_name = "VddmChas2Fr33"
    msg_id = 549
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.04
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']
    sig_group_dict = {'CmptmtTFrnt': ['CmptmtTFrntCmptmtTFrnt', 'CmptmtTFrntFanForCmptmtTRunng', 'CmptmtTFrntQf'], 'EvaprTFrnt': ['EvaprTFrntEvaprTFrnt', 'EvaprTFrntEvaprTQf'], 'CmptmtAirTEstimdExtd': ['CmptmtAirTEstimdExtdComptmtT', 'CmptmtAirTEstimdExtdQlyFlg']}
    sig_group_dataid_dict = {}

    class CmptmtTFrnt_UB:
        sig_name = "CmptmtTFrnt_UB"
        sig_start_bit = 30
        update_id_bit = 30
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 30
        byte = 3
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class EvaprTFrnt_UB:
        sig_name = "EvaprTFrnt_UB"
        sig_start_bit = 7
        update_id_bit = 7
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class CmptmtAirTEstimdExtd_UB:
        sig_name = "CmptmtAirTEstimdExtd_UB"
        sig_start_bit = 53
        update_id_bit = 53
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 53
        byte = 6
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class ClimaHeatgReqLvl:
        sig_name = "ClimaHeatgReqLvl"
        sig_start_bit = 1
        update_id_bit = 5
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvBattCoolgReq_NotReqd': 0, 'HvBattCoolgReq_LoReq': 1, 'HvBattCoolgReq_MedReq': 2, 'HvBattCoolgReq_HiReq': 3}
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class CmptmtAirTEstimdExtdComptmtT:
        sig_name = "CmptmtAirTEstimdExtdComptmtT"
        sig_start_bit = 50
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -60.0
        sig_value_min = 0
        sig_value_max = 1850
        sig_byteorder = "Motorola"
        sig_value_init = 600
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 50
        bmuws_info = [(6, 0b00000111, 0b11111000, 3, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class EvaprTFrntEvaprTQf:
        sig_name = "EvaprTFrntEvaprTQf"
        sig_start_bit = 13
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvacTIfQf_SnsrDataNotOk': 0, 'HvacTIfQf_SnsrDataOk': 1}
        compute_method = None
        length = 1
        startbit = 13
        byte = 1
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class CmptmtAirTEstimdExtdQlyFlg:
        sig_name = "CmptmtAirTEstimdExtdQlyFlg"
        sig_start_bit = 52
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 52
        byte = 6
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class CmptmtTFrntFanForCmptmtTRunng:
        sig_name = "CmptmtTFrntFanForCmptmtTRunng"
        sig_start_bit = 27
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flg1_Rst': 0, 'Flg1_Set': 1}
        compute_method = None
        length = 1
        startbit = 27
        byte = 3
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class HvacAirMFlowEstimd:
        sig_name = "HvacAirMFlowEstimd"
        sig_start_bit = 47
        update_id_bit = 31
        sig_length = 10
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class CmptmtTFrntCmptmtTFrnt:
        sig_name = "CmptmtTFrntCmptmtTFrnt"
        sig_start_bit = 26
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -60.0
        sig_value_min = 0
        sig_value_max = 1850
        sig_byteorder = "Motorola"
        sig_value_init = 600
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 26
        bmuws_info = [(3, 0b00000111, 0b11111000, 3, 0), (4, 0b11111111, 0b00000000, 8, 0)]

    class ClimaCoolgReqLvl:
        sig_name = "ClimaCoolgReqLvl"
        sig_start_bit = 3
        update_id_bit = 4
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvBattCoolgReq_NotReqd': 0, 'HvBattCoolgReq_LoReq': 1, 'HvBattCoolgReq_MedReq': 2, 'HvBattCoolgReq_HiReq': 3}
        compute_method = None
        length = 2
        startbit = 3
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class EvaprTFrntEvaprTFrnt:
        sig_name = "EvaprTFrntEvaprTFrnt"
        sig_start_bit = 12
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = -2560
        sig_value_max = 2559
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 12
        bmuws_info = [(1, 0b00011111, 0b11100000, 5, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class CmptmtTFrntQf:
        sig_name = "CmptmtTFrntQf"
        sig_start_bit = 29
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CmptmtTFrntQf_SnsrDataUndefd': 0, 'CmptmtTFrntQf_FanNotRunning': 1, 'CmptmtTFrntQf_SnsrDataNotOk': 2, 'CmptmtTFrntQf_SnsrDataOk': 3}
        compute_method = None
        length = 2
        startbit = 29
        byte = 3
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4


class EcmChas2Fr52:
    msg_name = "EcmChas2Fr52"
    msg_id = 1143
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 1.0
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HvWtrHeatrWtrTDes:
        sig_name = "HvWtrHeatrWtrTDes"
        sig_start_bit = 7
        update_id_bit = 31
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 40
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class BbmChas2DevFr01:
    msg_name = "BbmChas2DevFr01"
    msg_id = 1424
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BBM"
    rx_nodes = ['CCM']
    sig_group_dict = {'BBMdevelpsignalgroupresp1': ['BBMdevelpsignalgroupresp1Functiondevpsignalgroup1', 'BBMdevelpsignalgroupresp1Functiondevpsignalgroup2', 'BBMdevelpsignalgroupresp1Functiondevpsignalgroup3', 'BBMdevelpsignalgroupresp1Functiondevpsignalgroup4', 'BBMdevelpsignalgroupresp1Functiondevpsignalgroup5', 'BBMdevelpsignalgroupresp1Functiondevpsignalgroup6', 'BBMdevelpsignalgroupresp1Functiondevpsignalgroup7', 'BBMdevelpsignalgroupresp1Functiondevpsignalgroup8']}
    sig_group_dataid_dict = {}

    class BBMdevelpsignalgroupresp1Functiondevpsignalgroup4:
        sig_name = "BBMdevelpsignalgroupresp1Functiondevpsignalgroup4"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BBMdevelpsignalgroupresp1Functiondevpsignalgroup6:
        sig_name = "BBMdevelpsignalgroupresp1Functiondevpsignalgroup6"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BBMdevelpsignalgroupresp1Functiondevpsignalgroup2:
        sig_name = "BBMdevelpsignalgroupresp1Functiondevpsignalgroup2"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BBMdevelpsignalgroupresp1Functiondevpsignalgroup3:
        sig_name = "BBMdevelpsignalgroupresp1Functiondevpsignalgroup3"
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

    class BBMdevelpsignalgroupresp1Functiondevpsignalgroup8:
        sig_name = "BBMdevelpsignalgroupresp1Functiondevpsignalgroup8"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BBMdevelpsignalgroupresp1Functiondevpsignalgroup5:
        sig_name = "BBMdevelpsignalgroupresp1Functiondevpsignalgroup5"
        sig_start_bit = 39
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
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BBMdevelpsignalgroupresp1Functiondevpsignalgroup1:
        sig_name = "BBMdevelpsignalgroupresp1Functiondevpsignalgroup1"
        sig_start_bit = 7
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
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BBMdevelpsignalgroupresp1Functiondevpsignalgroup7:
        sig_name = "BBMdevelpsignalgroupresp1Functiondevpsignalgroup7"
        sig_start_bit = 55
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
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class SumToEtcXcpFr01:
    msg_name = "SumToEtcXcpFr01"
    msg_id = 1417
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "SUM1"
    rx_nodes = ['CCM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class EcmChas2Fr54:
    msg_name = "EcmChas2Fr54"
    msg_id = 36
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['BBM', 'VDDM']
    sig_group_dict = {'PtRgnTarTqAtReAxle': ['PtRgnTarTqAtReAxleAtReAxle', 'PtRgnTarTqAtReAxleQf'], 'PtTotBrkTqReq': ['PtTotBrkTqReqPtTotBrkTqEna', 'PtTotBrkTqReqPtTotBrkTqReq']}
    sig_group_dataid_dict = {}

    class PtTotBrkTqReqPtTotBrkTqEna:
        sig_name = "PtTotBrkTqReqPtTotBrkTqEna"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 47
        byte = 5
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class DeactvtTestCom:
        sig_name = "DeactvtTestCom"
        sig_start_bit = 39
        update_id_bit = 38
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff2_On': 0, 'OnOff2_Off': 1}
        compute_method = None
        length = 1
        startbit = 39
        byte = 4
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class PtTotBrkTqReqPtTotBrkTqReq:
        sig_name = "PtTotBrkTqReqPtTotBrkTqReq"
        sig_start_bit = 46
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = -16384
        sig_value_max = 16380
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 46
        bmuws_info = [(5, 0b01111111, 0b10000000, 7, 0), (6, 0b11111111, 0b00000000, 8, 0)]

    class PtRgnTarTqAtReAxleAtReAxle:
        sig_name = "PtRgnTarTqAtReAxleAtReAxle"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = -16384
        sig_value_max = 16380
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111110, 0b00000001, 7, 1)]

    class PtRgnTarTqAtReAxle_UB:
        sig_name = "PtRgnTarTqAtReAxle_UB"
        sig_start_bit = 21
        update_id_bit = 21
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 21
        byte = 2
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class PtRgnTarTqAtReAxleQf:
        sig_name = "PtRgnTarTqAtReAxleQf"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Qf1_DevOfDataUndefd': 0, 'Qf1_DataTmpUndefdAndEvlnInProgs': 1, 'Qf1_DevOfDataNotWithinRngAllwd': 2, 'Qf1_DataCalcdWithDevDefd': 3}
        compute_method = None
        length = 2
        startbit = 23
        byte = 2
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class PtTotBrkTqReq_UB:
        sig_name = "PtTotBrkTqReq_UB"
        sig_start_bit = 63
        update_id_bit = 63
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 63
        byte = 7
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class PrpsnSysActv:
        sig_name = "PrpsnSysActv"
        sig_start_bit = 35
        update_id_bit = 34
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NotCmpl1_NotCmpl': 0, 'NotCmpl1_Cmpl': 1}
        compute_method = None
        length = 1
        startbit = 35
        byte = 4
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3


class BgmChas2Fr02:
    msg_name = "BgmChas2Fr02"
    msg_id = 64
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []
    sig_group_dict = {'ObjInfo': ['ObjInfoObjConfidenceLvl', 'ObjInfoObjDst1', 'ObjInfoObjDst2', 'ObjInfoObjHei', 'ObjInfoObjSide', 'ObjInfoObjTypMai']}
    sig_group_dataid_dict = {}

    class ObjInfoObjHei:
        sig_name = "ObjInfoObjHei"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = -128
        sig_value_max = 127
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ObjInfoObjDst2:
        sig_name = "ObjInfoObjDst2"
        sig_start_bit = 21
        update_id_bit = None
        sig_length = 10
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 21
        bmuws_info = [(2, 0b00111111, 0b11000000, 6, 0), (3, 0b11110000, 0b00001111, 4, 4)]

    class ObjInfoObjDst1:
        sig_name = "ObjInfoObjDst1"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 10
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 15
        bmuws_info = [(1, 0b11111111, 0b00000000, 8, 0), (2, 0b11000000, 0b00111111, 2, 6)]

    class ObjInfoObjConfidenceLvl:
        sig_name = "ObjInfoObjConfidenceLvl"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 7
        byte = 0
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class ObjInfoObjTypMai:
        sig_name = "ObjInfoObjTypMai"
        sig_start_bit = 45
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ObjTpyMai_None': 0, 'ObjTpyMai_Bump': 1, 'ObjTpyMai_Manhole': 2, 'ObjTpyMai_Pothole': 3, 'ObjTpyMai_Step': 4, 'ObjTpyMai_Reserved_1': 5, 'ObjTpyMai_Reserved_2': 6, 'ObjTpyMai_Reserved_3': 7, 'ObjTpyMai_Reserved_4': 8, 'ObjTpyMai_Reserved_5': 9, 'ObjTpyMai_Reserved_6': 10, 'ObjTpyMai_Reserved_7': 11, 'ObjTpyMai_Reserved_8': 12, 'ObjTpyMai_Reserved_9': 13, 'ObjTpyMai_Reserved_10': 14, 'ObjTpyMai_Reserved_11': 15}
        compute_method = None
        length = 4
        startbit = 45
        byte = 5
        mask = 0b00111100
        unmask = 0b11000011
        shift = 2

    class ObjInfoObjSide:
        sig_name = "ObjInfoObjSide"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ObjSide_None': 0, 'ObjSide_Left': 1, 'ObjSide_Right': 2, 'ObjSide_Both': 3}
        compute_method = None
        length = 2
        startbit = 47
        byte = 5
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class ObjInfo_UB:
        sig_name = "ObjInfo_UB"
        sig_start_bit = 40
        update_id_bit = 40
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 40
        byte = 5
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0


class SumChas2Fr02:
    msg_name = "SumChas2Fr02"
    msg_id = 531
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.13
    msg_length = 8
    tx_node = "SUM1"
    rx_nodes = ['S2SReceiver']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class ActModOfDampr:
        sig_name = "ActModOfDampr"
        sig_start_bit = 15
        update_id_bit = 12
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Level1': 0, 'Level2': 1, 'Level3': 2, 'Level4': 3, 'Reserved1': 4, 'Reserved2': 5, 'Reserved3': 6, 'Reserved4': 7}
        compute_method = None
        length = 3
        startbit = 15
        byte = 1
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5


class VddmChas2Fr09:
    msg_name = "VddmChas2Fr09"
    msg_id = 384
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['BBM', 'ECM', 'SUM1']
    sig_group_dict = {'PrimBrkSysSt2': ['PrimBrkSysSt2BrkSysSt', 'PrimBrkSysSt2Chks', 'PrimBrkSysSt2Cntr'], 'FricEstimnFromVehDyn': ['FricEstimnFromVehDynFricEstimnFromVehDyn', 'FricEstimnFromVehDynQly']}
    sig_group_dataid_dict = {'PrimBrkSysSt2': 6520}

    class PrimBrkSysSt2Chks:
        sig_name = "PrimBrkSysSt2Chks"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class PrimBrkSysSt2_UB:
        sig_name = "PrimBrkSysSt2_UB"
        sig_start_bit = 63
        update_id_bit = 63
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 63
        byte = 7
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class TqRednDurgCllsnMtgtnByBrkg:
        sig_name = "TqRednDurgCllsnMtgtnByBrkg"
        sig_start_bit = 3
        update_id_bit = 61
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TqRednDurgBrk_NoTqRednReqd': 0, 'TqRednDurgBrk_TqRednDurgPreBrk': 1, 'TqRednDurgBrk_TqRednDurgBrkFull': 2, 'TqRednDurgBrk_Resd3': 3}
        compute_method = None
        length = 2
        startbit = 3
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class EscDamprReq:
        sig_name = "EscDamprReq"
        sig_start_bit = 7
        update_id_bit = 41
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DamprChartc_NoReq': 0, 'DamprChartc_DamprChartcForHndlg': 1, 'DamprChartc_DamprChartcForBrkTrig': 2, 'DamprChartc_DamprChartcForBrkGrip': 3}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class FricEstimnFromVehDynFricEstimnFromVehDyn:
        sig_name = "FricEstimnFromVehDynFricEstimnFromVehDyn"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.01
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 200
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FricEstimnFromVehDyn_UB:
        sig_name = "FricEstimnFromVehDyn_UB"
        sig_start_bit = 20
        update_id_bit = 20
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 20
        byte = 2
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class FricEstimnFromVehDynQly:
        sig_name = "FricEstimnFromVehDynQly"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Qly3_De0': 0, 'Qly3_De1': 1, 'Qly3_De2': 2, 'Qly3_De3': 3, 'Qly3_De4': 4, 'Qly3_De5': 5, 'Qly3_De6': 6, 'Qly3_De7': 7}
        compute_method = None
        length = 3
        startbit = 23
        byte = 2
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class PrimBrkSysSt2BrkSysSt:
        sig_name = "PrimBrkSysSt2BrkSysSt"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 11
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NotAvailable_Temporary': 0, 'NotAvailable_NotReleased': 1, 'NotAvailable_Permanent': 2, 'NotActivated_FullAvailable': 3, 'Activation_Preparation': 4, 'Activation_Pending': 5, 'Activation_PendingRedundancyLost': 6, 'Activation_PendingFailOperation': 7, 'Activated_FullAvailable': 8, 'Activated_FailOperation': 9, 'Activated_RedundancyLost': 10, 'Deactivation_Pending': 11}
        compute_method = None
        length = 4
        startbit = 39
        byte = 4
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class PrimBrkSysSt2Cntr:
        sig_name = "PrimBrkSysSt2Cntr"
        sig_start_bit = 19
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
        startbit = 19
        byte = 2
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0


class EcmChas2Fr68:
    msg_name = "EcmChas2Fr68"
    msg_id = 325
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.03
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['BBM']
    sig_group_dict = {'IsgSpdActSgnSafe': ['IsgSpdActSgnSafeChks', 'IsgSpdActSgnSafeCntr', 'IsgSpdActSgnSafeIsgSpdWSgnTyp', 'IsgSpdActSgnSafeQf'], 'WhlMotSysSpdActSafe': ['WhlMotSysSpdActSafeChks', 'WhlMotSysSpdActSafeCntr', 'WhlMotSysSpdActSafeIsgSpdWSgnTyp', 'WhlMotSysSpdActSafeQf']}
    sig_group_dataid_dict = {'IsgSpdActSgnSafe': 7003, 'WhlMotSysSpdActSafe': 7001}

    class WhlMotSysSpdActSafeQf:
        sig_name = "WhlMotSysSpdActSafeQf"
        sig_start_bit = 37
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
        startbit = 37
        byte = 4
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class WhlMotSysSpdActSafeCntr:
        sig_name = "WhlMotSysSpdActSafeCntr"
        sig_start_bit = 35
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
        startbit = 35
        byte = 4
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class IsgSpdActSgnSafe_UB:
        sig_name = "IsgSpdActSgnSafe_UB"
        sig_start_bit = 6
        update_id_bit = 6
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class IsgSpdActSgnSafeIsgSpdWSgnTyp:
        sig_name = "IsgSpdActSgnSafeIsgSpdWSgnTyp"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = -16384
        sig_value_max = 16383
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111110, 0b00000001, 7, 1)]

    class WhlMotSysSpdActSafeIsgSpdWSgnTyp:
        sig_name = "WhlMotSysSpdActSafeIsgSpdWSgnTyp"
        sig_start_bit = 55
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = -16384
        sig_value_max = 16383
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 55
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111110, 0b00000001, 7, 1)]

    class IsgSpdActSgnSafeChks:
        sig_name = "IsgSpdActSgnSafeChks"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class WhlMotSysSpdActSafe_UB:
        sig_name = "WhlMotSysSpdActSafe_UB"
        sig_start_bit = 56
        update_id_bit = 56
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 56
        byte = 7
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class WhlMotSysSpdActSafeChks:
        sig_name = "WhlMotSysSpdActSafeChks"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class IsgSpdActSgnSafeCntr:
        sig_name = "IsgSpdActSgnSafeCntr"
        sig_start_bit = 3
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
        startbit = 3
        byte = 0
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class IsgSpdActSgnSafeQf:
        sig_name = "IsgSpdActSgnSafeQf"
        sig_start_bit = 5
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
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4


class EcmChassisCAN2NmFr:
    msg_name = "EcmChassisCAN2NmFr"
    msg_id = 1311
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['BGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class EcmChas2Fr04:
    msg_name = "EcmChas2Fr04"
    msg_id = 256
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.025
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['BBM', 'VDDM']
    sig_group_dict = {'AccrPedlPsd': ['AccrPedlPsdAccrPedlPsd', 'AccrPedlPsdChks', 'AccrPedlPsdCntr', 'AccrPedlPsdSts']}
    sig_group_dataid_dict = {'AccrPedlPsd': 72}

    class PtTqAtAxleAvlReMax:
        sig_name = "PtTqAtAxleAvlReMax"
        sig_start_bit = 10
        update_id_bit = 56
        sig_length = 13
        sig_value_factor = 4.0
        sig_value_offset = 0.0
        sig_value_min = -4096
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 10
        bmuws_info = [(1, 0b00000111, 0b11111000, 3, 0), (2, 0b11111111, 0b00000000, 8, 0), (3, 0b11000000, 0b00111111, 2, 6)]

    class AccrPedlPsd_UB:
        sig_name = "AccrPedlPsd_UB"
        sig_start_bit = 40
        update_id_bit = 40
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 40
        byte = 5
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class AccrPedlPsdCntr:
        sig_name = "AccrPedlPsdCntr"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class AccrPedlPsdSts:
        sig_name = "AccrPedlPsdSts"
        sig_start_bit = 58
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 58
        byte = 7
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class AccrPedlPsdChks:
        sig_name = "AccrPedlPsdChks"
        sig_start_bit = 55
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 255
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class AccrPedlPsdAccrPedlPsd:
        sig_name = "AccrPedlPsdAccrPedlPsd"
        sig_start_bit = 59
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 59
        byte = 7
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3


class EcmChas2Fr59:
    msg_name = "EcmChas2Fr59"
    msg_id = 1175
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 1.0
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']
    sig_group_dict = {'ThermMgmtObsrvn3': ['ThermMgmtObsrvn3Byte0', 'ThermMgmtObsrvn3Byte1', 'ThermMgmtObsrvn3Byte2', 'ThermMgmtObsrvn3Byte3', 'ThermMgmtObsrvn3Byte4', 'ThermMgmtObsrvn3Byte5', 'ThermMgmtObsrvn3Byte6', 'ThermMgmtObsrvn3Byte7']}
    sig_group_dataid_dict = {}

    class ThermMgmtObsrvn3Byte7:
        sig_name = "ThermMgmtObsrvn3Byte7"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn3Byte0:
        sig_name = "ThermMgmtObsrvn3Byte0"
        sig_start_bit = 7
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
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn3Byte1:
        sig_name = "ThermMgmtObsrvn3Byte1"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn3Byte2:
        sig_name = "ThermMgmtObsrvn3Byte2"
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

    class ThermMgmtObsrvn3Byte6:
        sig_name = "ThermMgmtObsrvn3Byte6"
        sig_start_bit = 55
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
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn3Byte3:
        sig_name = "ThermMgmtObsrvn3Byte3"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn3Byte5:
        sig_name = "ThermMgmtObsrvn3Byte5"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn3Byte4:
        sig_name = "ThermMgmtObsrvn3Byte4"
        sig_start_bit = 39
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
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class EcmChas2Fr67:
    msg_name = "EcmChas2Fr67"
    msg_id = 1091
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.4
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']
    sig_group_dict = {'BexvSts': ['BexvStsExvActrPosn', 'BexvStsExvBlkErr', 'BexvStsExvCalibSts', 'BexvStsExvElecStsErr', 'BexvStsExvMovSts', 'BexvStsExvOvrTempErr', 'BexvStsExvOvrTrvlErr', 'BexvStsExvPreHeatgSts', 'BexvStsExvVoltgRangErr'], 'CexvSts': ['CexvStsExvActrPosn', 'CexvStsExvBlkErr', 'CexvStsExvCalibSts', 'CexvStsExvElecStsErr', 'CexvStsExvMovSts', 'CexvStsExvOvrTempErr', 'CexvStsExvOvrTrvlErr', 'CexvStsExvPreHeatgSts', 'CexvStsExvVoltgRangErr']}
    sig_group_dataid_dict = {}

    class BexvStsExvMovSts:
        sig_name = "BexvStsExvMovSts"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvMovSts_NotMove': 0, 'ExvMovSts_Moving': 1}
        compute_method = None
        length = 1
        startbit = 0
        byte = 0
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class CexvStsExvPreHeatgSts:
        sig_name = "CexvStsExvPreHeatgSts"
        sig_start_bit = 27
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 27
        byte = 3
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class CexvStsExvVoltgRangErr:
        sig_name = "CexvStsExvVoltgRangErr"
        sig_start_bit = 29
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VoltgRangErr_NoErr': 0, 'VoltgRangErr_UnderVoltageErr': 1, 'VoltgRangErr_OverVoltageErr': 2, 'VoltgRangErr_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 29
        byte = 3
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class CexvStsExvElecStsErr:
        sig_name = "CexvStsExvElecStsErr"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvElecStsErr_NoError': 0, 'ExvElecStsErr_OpenCircuit': 1, 'ExvElecStsErr_ShortCircuit': 2, 'ExvElecStsErr_OverTemperatureShutdown': 3, 'ExvElecStsErr_IndeterminateElectricFault': 4, 'ExvElecStsErr_Reserved': 5}
        compute_method = None
        length = 3
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class CexvStsExvMovSts:
        sig_name = "CexvStsExvMovSts"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvMovSts_NotMove': 0, 'ExvMovSts_Moving': 1}
        compute_method = None
        length = 1
        startbit = 24
        byte = 3
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class BexvStsExvOvrTempErr:
        sig_name = "BexvStsExvOvrTempErr"
        sig_start_bit = 1
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err1_NoErr': 0, 'Err1_Err': 1}
        compute_method = None
        length = 1
        startbit = 1
        byte = 0
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class CexvStsExvCalibSts:
        sig_name = "CexvStsExvCalibSts"
        sig_start_bit = 36
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvCalibSts_NotInitialized': 0, 'ExvCalibSts_InitializationInProcess': 1, 'ExvCalibSts_Initialized': 2, 'ExvCalibSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 36
        byte = 4
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class CexvStsExvOvrTempErr:
        sig_name = "CexvStsExvOvrTempErr"
        sig_start_bit = 25
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err1_NoErr': 0, 'Err1_Err': 1}
        compute_method = None
        length = 1
        startbit = 25
        byte = 3
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class BexvSts_UB:
        sig_name = "BexvSts_UB"
        sig_start_bit = 6
        update_id_bit = 6
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class BexvStsExvPreHeatgSts:
        sig_name = "BexvStsExvPreHeatgSts"
        sig_start_bit = 3
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 3
        byte = 0
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class BexvStsExvElecStsErr:
        sig_name = "BexvStsExvElecStsErr"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvElecStsErr_NoError': 0, 'ExvElecStsErr_OpenCircuit': 1, 'ExvElecStsErr_ShortCircuit': 2, 'ExvElecStsErr_OverTemperatureShutdown': 3, 'ExvElecStsErr_IndeterminateElectricFault': 4, 'ExvElecStsErr_Reserved': 5}
        compute_method = None
        length = 3
        startbit = 15
        byte = 1
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class BexvStsExvOvrTrvlErr:
        sig_name = "BexvStsExvOvrTrvlErr"
        sig_start_bit = 2
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err1_NoErr': 0, 'Err1_Err': 1}
        compute_method = None
        length = 1
        startbit = 2
        byte = 0
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class BexvStsExvVoltgRangErr:
        sig_name = "BexvStsExvVoltgRangErr"
        sig_start_bit = 5
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VoltgRangErr_NoErr': 0, 'VoltgRangErr_UnderVoltageErr': 1, 'VoltgRangErr_OverVoltageErr': 2, 'VoltgRangErr_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class CexvStsExvActrPosn:
        sig_name = "CexvStsExvActrPosn"
        sig_start_bit = 33
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.2
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 500
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 33
        bmuws_info = [(4, 0b00000011, 0b11111100, 2, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class BexvStsExvCalibSts:
        sig_name = "BexvStsExvCalibSts"
        sig_start_bit = 12
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvCalibSts_NotInitialized': 0, 'ExvCalibSts_InitializationInProcess': 1, 'ExvCalibSts_Initialized': 2, 'ExvCalibSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 12
        byte = 1
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class CexvStsExvOvrTrvlErr:
        sig_name = "CexvStsExvOvrTrvlErr"
        sig_start_bit = 26
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err1_NoErr': 0, 'Err1_Err': 1}
        compute_method = None
        length = 1
        startbit = 26
        byte = 3
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class CexvSts_UB:
        sig_name = "CexvSts_UB"
        sig_start_bit = 30
        update_id_bit = 30
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 30
        byte = 3
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class BexvStsExvActrPosn:
        sig_name = "BexvStsExvActrPosn"
        sig_start_bit = 9
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.2
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 500
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 9
        bmuws_info = [(1, 0b00000011, 0b11111100, 2, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class BexvStsExvBlkErr:
        sig_name = "BexvStsExvBlkErr"
        sig_start_bit = 10
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err1_NoErr': 0, 'Err1_Err': 1}
        compute_method = None
        length = 1
        startbit = 10
        byte = 1
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class CexvStsExvBlkErr:
        sig_name = "CexvStsExvBlkErr"
        sig_start_bit = 34
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err1_NoErr': 0, 'Err1_Err': 1}
        compute_method = None
        length = 1
        startbit = 34
        byte = 4
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2


class BbmChas2DevFr02:
    msg_name = "BbmChas2DevFr02"
    msg_id = 1425
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BBM"
    rx_nodes = ['CCM']
    sig_group_dict = {'BBMdevelpsignalgroupresp2': ['BBMdevelpsignalgroupresp2Functiondevpsignalgroup1', 'BBMdevelpsignalgroupresp2Functiondevpsignalgroup2', 'BBMdevelpsignalgroupresp2Functiondevpsignalgroup3', 'BBMdevelpsignalgroupresp2Functiondevpsignalgroup4', 'BBMdevelpsignalgroupresp2Functiondevpsignalgroup5', 'BBMdevelpsignalgroupresp2Functiondevpsignalgroup6', 'BBMdevelpsignalgroupresp2Functiondevpsignalgroup7', 'BBMdevelpsignalgroupresp2Functiondevpsignalgroup8']}
    sig_group_dataid_dict = {}

    class BBMdevelpsignalgroupresp2Functiondevpsignalgroup4:
        sig_name = "BBMdevelpsignalgroupresp2Functiondevpsignalgroup4"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BBMdevelpsignalgroupresp2Functiondevpsignalgroup5:
        sig_name = "BBMdevelpsignalgroupresp2Functiondevpsignalgroup5"
        sig_start_bit = 39
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
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BBMdevelpsignalgroupresp2Functiondevpsignalgroup7:
        sig_name = "BBMdevelpsignalgroupresp2Functiondevpsignalgroup7"
        sig_start_bit = 55
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
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BBMdevelpsignalgroupresp2Functiondevpsignalgroup1:
        sig_name = "BBMdevelpsignalgroupresp2Functiondevpsignalgroup1"
        sig_start_bit = 7
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
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BBMdevelpsignalgroupresp2Functiondevpsignalgroup2:
        sig_name = "BBMdevelpsignalgroupresp2Functiondevpsignalgroup2"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BBMdevelpsignalgroupresp2Functiondevpsignalgroup8:
        sig_name = "BBMdevelpsignalgroupresp2Functiondevpsignalgroup8"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BBMdevelpsignalgroupresp2Functiondevpsignalgroup3:
        sig_name = "BBMdevelpsignalgroupresp2Functiondevpsignalgroup3"
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

    class BBMdevelpsignalgroupresp2Functiondevpsignalgroup6:
        sig_name = "BBMdevelpsignalgroupresp2Functiondevpsignalgroup6"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class VddmChas2Fr14:
    msg_name = "VddmChas2Fr14"
    msg_id = 432
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.03
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM', 'SUM1']
    sig_group_dict = {'AgDataRawSafe': ['AgDataRawSafeChks', 'AgDataRawSafeCntr', 'AgDataRawSafeRollRate', 'AgDataRawSafeRollRateQf', 'AgDataRawSafeYawRate', 'AgDataRawSafeYawRateQf']}
    sig_group_dataid_dict = {'AgDataRawSafe': 35}

    class AgDataRawSafe_UB:
        sig_name = "AgDataRawSafe_UB"
        sig_start_bit = 52
        update_id_bit = 52
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class AgDataRawSafeChks:
        sig_name = "AgDataRawSafeChks"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 255
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class AgDataRawSafeRollRateQf:
        sig_name = "AgDataRawSafeRollRateQf"
        sig_start_bit = 43
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Qf1_DevOfDataUndefd': 0, 'Qf1_DataTmpUndefdAndEvlnInProgs': 1, 'Qf1_DevOfDataNotWithinRngAllwd': 2, 'Qf1_DataCalcdWithDevDefd': 3}
        compute_method = None
        length = 2
        startbit = 43
        byte = 5
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class AgDataRawSafeYawRate:
        sig_name = "AgDataRawSafeYawRate"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 0.000244140625
        sig_value_offset = 0.0
        sig_value_min = -24576
        sig_value_max = 24576
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class AgDataRawSafeYawRateQf:
        sig_name = "AgDataRawSafeYawRateQf"
        sig_start_bit = 41
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Qf1_DevOfDataUndefd': 0, 'Qf1_DataTmpUndefdAndEvlnInProgs': 1, 'Qf1_DevOfDataNotWithinRngAllwd': 2, 'Qf1_DataCalcdWithDevDefd': 3}
        compute_method = None
        length = 2
        startbit = 41
        byte = 5
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class AgDataRawSafeRollRate:
        sig_name = "AgDataRawSafeRollRate"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 0.000244140625
        sig_value_offset = 0.0
        sig_value_min = -24576
        sig_value_max = 24576
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class AgDataRawSafeCntr:
        sig_name = "AgDataRawSafeCntr"
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


class VddmChas2Fr78:
    msg_name = "VddmChas2Fr78"
    msg_id = 664
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.3
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HvacCoolgEnaRe:
        sig_name = "HvacCoolgEnaRe"
        sig_start_bit = 49
        update_id_bit = 50
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 49
        byte = 6
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class HvacEvaprTSpFrnt:
        sig_name = "HvacEvaprTSpFrnt"
        sig_start_bit = 63
        update_id_bit = 48
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = -5.0
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Motorola"
        sig_value_init = 50
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ClimaSts:
        sig_name = "ClimaSts"
        sig_start_bit = 20
        update_id_bit = 19
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ClimaSts_Start': 0, 'ClimaSts_Finish': 1}
        compute_method = None
        length = 1
        startbit = 20
        byte = 2
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class CmptModForHp:
        sig_name = "CmptModForHp"
        sig_start_bit = 7
        update_id_bit = 18
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 5
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ModeCmptHp_vent': 0, 'ModeCmptHp_cool': 1, 'ModeCmptHp_hot': 2, 'ModeCmptHp_cool_hot': 3, 'ModeCmptHp_cool_defog': 4, 'ModeCmptHp_hot_defog': 5, 'ModeCmptHp_cool_hot_defog': 6, 'ModeCmptHp_reserved': 7}
        compute_method = None
        length = 3
        startbit = 7
        byte = 0
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class EcoClimaSts:
        sig_name = "EcoClimaSts"
        sig_start_bit = 42
        update_id_bit = 41
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 42
        byte = 5
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class CmptmtAirTEstimdAtRowFirstLoResl:
        sig_name = "CmptmtAirTEstimdAtRowFirstLoResl"
        sig_start_bit = 15
        update_id_bit = 17
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -60.0
        sig_value_min = 0
        sig_value_max = 1850
        sig_byteorder = "Motorola"
        sig_value_init = 600
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 15
        bmuws_info = [(1, 0b11111111, 0b00000000, 8, 0), (2, 0b11100000, 0b00011111, 3, 5)]

    class HvacCoolgEnaFrnt:
        sig_name = "HvacCoolgEnaFrnt"
        sig_start_bit = 52
        update_id_bit = 51
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4


class EcmChas2Fr53:
    msg_name = "EcmChas2Fr53"
    msg_id = 1144
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 1.0
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']
    sig_group_dict = {'DiagFrameForECM': ['DiagFrameForECMByte0', 'DiagFrameForECMByte1', 'DiagFrameForECMByte2', 'DiagFrameForECMByte3', 'DiagFrameForECMByte4', 'DiagFrameForECMByte5', 'DiagFrameForECMByte6', 'DiagFrameForECMByte7']}
    sig_group_dataid_dict = {}

    class DiagFrameForECMByte0:
        sig_name = "DiagFrameForECMByte0"
        sig_start_bit = 7
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
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DiagFrameForECMByte6:
        sig_name = "DiagFrameForECMByte6"
        sig_start_bit = 55
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
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DiagFrameForECMByte3:
        sig_name = "DiagFrameForECMByte3"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DiagFrameForECMByte7:
        sig_name = "DiagFrameForECMByte7"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DiagFrameForECMByte2:
        sig_name = "DiagFrameForECMByte2"
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

    class DiagFrameForECMByte5:
        sig_name = "DiagFrameForECMByte5"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DiagFrameForECMByte4:
        sig_name = "DiagFrameForECMByte4"
        sig_start_bit = 39
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
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DiagFrameForECMByte1:
        sig_name = "DiagFrameForECMByte1"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class VddmChas2Fr38:
    msg_name = "VddmChas2Fr38"
    msg_id = 568
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.04
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']
    sig_group_dict = {'PtTq': ['PtTqChks', 'PtTqCntr', 'PtTqMinReq', 'PtTqSoftMaxReq']}
    sig_group_dataid_dict = {'PtTq': 162}

    class PtTqSoftMaxReq:
        sig_name = "PtTqSoftMaxReq"
        sig_start_bit = 36
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 4.0
        sig_value_offset = 0.0
        sig_value_min = -4096
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 36
        bmuws_info = [(4, 0b00011111, 0b11100000, 5, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class PtTqCntr:
        sig_name = "PtTqCntr"
        sig_start_bit = 59
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
        startbit = 59
        byte = 7
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class PtTqChks:
        sig_name = "PtTqChks"
        sig_start_bit = 55
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
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class PtTq_UB:
        sig_name = "PtTq_UB"
        sig_start_bit = 7
        update_id_bit = 7
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class PtTqMinReq:
        sig_name = "PtTqMinReq"
        sig_start_bit = 20
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 4.0
        sig_value_offset = 0.0
        sig_value_min = -4096
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 20
        bmuws_info = [(2, 0b00011111, 0b11100000, 5, 0), (3, 0b11111111, 0b00000000, 8, 0)]


class BgmChas2Fr03:
    msg_name = "BgmChas2Fr03"
    msg_id = 45
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []
    sig_group_dict = {'ObjInfo2': ['ObjInfo2ObjConfidenceLvl', 'ObjInfo2ObjDst1', 'ObjInfo2ObjDst2', 'ObjInfo2ObjHei', 'ObjInfo2ObjSide', 'ObjInfo2ObjTypMai']}
    sig_group_dataid_dict = {}

    class SumRoadTyp:
        sig_name = "SumRoadTyp"
        sig_start_bit = 55
        update_id_bit = 51
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SumRoadTyp_None': 0, 'SumRoadTyp_Smooth': 1, 'SumRoadTyp_Medium': 2, 'SumRoadTyp_Rough': 3, 'SumRoadTyp_Reserved_0': 4, 'SumRoadTyp_Reserved_1': 5, 'SumRoadTyp_Reserved_2': 6, 'SumRoadTyp_Reserved_3': 7, 'SumRoadTyp_Reserved_4': 8, 'SumRoadTyp_Reserved_5': 9, 'SumRoadTyp_Reserved_6': 10, 'SumRoadTyp_Reserved_7': 11, 'SumRoadTyp_Reserved_8': 12, 'SumRoadTyp_Reserved_9': 13, 'SumRoadTyp_Reserved_10': 14, 'SumRoadTyp_Reserved_11': 15}
        compute_method = None
        length = 4
        startbit = 55
        byte = 6
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class ObjInfo2ObjDst1:
        sig_name = "ObjInfo2ObjDst1"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 10
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 15
        bmuws_info = [(1, 0b11111111, 0b00000000, 8, 0), (2, 0b11000000, 0b00111111, 2, 6)]

    class ObjInfo2ObjDst2:
        sig_name = "ObjInfo2ObjDst2"
        sig_start_bit = 21
        update_id_bit = None
        sig_length = 10
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 21
        bmuws_info = [(2, 0b00111111, 0b11000000, 6, 0), (3, 0b11110000, 0b00001111, 4, 4)]

    class ObjInfo2ObjHei:
        sig_name = "ObjInfo2ObjHei"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = -128
        sig_value_max = 127
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ObjInfo2ObjSide:
        sig_name = "ObjInfo2ObjSide"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ObjSide_None': 0, 'ObjSide_Left': 1, 'ObjSide_Right': 2, 'ObjSide_Both': 3}
        compute_method = None
        length = 2
        startbit = 47
        byte = 5
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class ObjInfo2ObjConfidenceLvl:
        sig_name = "ObjInfo2ObjConfidenceLvl"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 7
        byte = 0
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class ObjInfo2ObjTypMai:
        sig_name = "ObjInfo2ObjTypMai"
        sig_start_bit = 45
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ObjTpyMai_None': 0, 'ObjTpyMai_Bump': 1, 'ObjTpyMai_Manhole': 2, 'ObjTpyMai_Pothole': 3, 'ObjTpyMai_Step': 4, 'ObjTpyMai_Reserved_1': 5, 'ObjTpyMai_Reserved_2': 6, 'ObjTpyMai_Reserved_3': 7, 'ObjTpyMai_Reserved_4': 8, 'ObjTpyMai_Reserved_5': 9, 'ObjTpyMai_Reserved_6': 10, 'ObjTpyMai_Reserved_7': 11, 'ObjTpyMai_Reserved_8': 12, 'ObjTpyMai_Reserved_9': 13, 'ObjTpyMai_Reserved_10': 14, 'ObjTpyMai_Reserved_11': 15}
        compute_method = None
        length = 4
        startbit = 45
        byte = 5
        mask = 0b00111100
        unmask = 0b11000011
        shift = 2

    class SumSnsrSts:
        sig_name = "SumSnsrSts"
        sig_start_bit = 50
        update_id_bit = 63
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SumSnsrSts_NA': 0, 'SumSnsrSts_Active': 1, 'SumSnsrSts_Idle': 2, 'SumSnsrSts_Error': 3, 'SumSnsrSts_Off': 4, 'SumSnsrSts_Reserved1': 5, 'SumSnsrSts_Reserved2': 6, 'SumSnsrSts_Reserved3': 7}
        compute_method = None
        length = 3
        startbit = 50
        byte = 6
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class ObjInfo2_UB:
        sig_name = "ObjInfo2_UB"
        sig_start_bit = 40
        update_id_bit = 40
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 40
        byte = 5
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0


class BbmChassisCAN2NmFr:
    msg_name = "BbmChassisCAN2NmFr"
    msg_id = 1319
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BBM"
    rx_nodes = ['VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class EcmChas2Fr27:
    msg_name = "EcmChas2Fr27"
    msg_id = 101
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']
    sig_group_dict = {'PtBrkTq': ['PtBrkTqActTot', 'PtBrkTqActTotQf', 'PtBrkTqChks', 'PtBrkTqCntr', 'PtBrkTqQf', 'PtBrkTqReqForBrkSys', 'PtBrkTqRgnAtAxleReAct']}
    sig_group_dataid_dict = {'PtBrkTq': 176}

    class PtBrkTqCntr:
        sig_name = "PtBrkTqCntr"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class PtBrkTqRgnAtAxleReAct:
        sig_name = "PtBrkTqRgnAtAxleReAct"
        sig_start_bit = 55
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = -16384
        sig_value_max = 16380
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 55
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111110, 0b00000001, 7, 1)]

    class PtBrkTq_UB:
        sig_name = "PtBrkTq_UB"
        sig_start_bit = 56
        update_id_bit = 56
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 56
        byte = 7
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class PtBrkTqActTotQf:
        sig_name = "PtBrkTqActTotQf"
        sig_start_bit = 11
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Qf1_DevOfDataUndefd': 0, 'Qf1_DataTmpUndefdAndEvlnInProgs': 1, 'Qf1_DevOfDataNotWithinRngAllwd': 2, 'Qf1_DataCalcdWithDevDefd': 3}
        compute_method = None
        length = 2
        startbit = 11
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class PtBrkTqQf:
        sig_name = "PtBrkTqQf"
        sig_start_bit = 9
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Qf1_DevOfDataUndefd': 0, 'Qf1_DataTmpUndefdAndEvlnInProgs': 1, 'Qf1_DevOfDataNotWithinRngAllwd': 2, 'Qf1_DataCalcdWithDevDefd': 3}
        compute_method = None
        length = 2
        startbit = 9
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class PtBrkTqActTot:
        sig_name = "PtBrkTqActTot"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = -16384
        sig_value_max = 16380
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111110, 0b00000001, 7, 1)]

    class PtBrkTqReqForBrkSys:
        sig_name = "PtBrkTqReqForBrkSys"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = -16384
        sig_value_max = 16380
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111110, 0b00000001, 7, 1)]

    class PtBrkTqChks:
        sig_name = "PtBrkTqChks"
        sig_start_bit = 7
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
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class VddmChas2Fr23:
    msg_name = "VddmChas2Fr23"
    msg_id = 864
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.5
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['BBM', 'ECM', 'SUM1']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class CarTiGlb:
        sig_name = "CarTiGlb"
        sig_start_bit = 7
        update_id_bit = 57
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
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0)]


class EcmChas2Fr61:
    msg_name = "EcmChas2Fr61"
    msg_id = 1162
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 1.0
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']
    sig_group_dict = {'ThermMgmtObsrvn5': ['ThermMgmtObsrvn5Byte0', 'ThermMgmtObsrvn5Byte1', 'ThermMgmtObsrvn5Byte2', 'ThermMgmtObsrvn5Byte3', 'ThermMgmtObsrvn5Byte4', 'ThermMgmtObsrvn5Byte5', 'ThermMgmtObsrvn5Byte6', 'ThermMgmtObsrvn5Byte7']}
    sig_group_dataid_dict = {}

    class ThermMgmtObsrvn5Byte5:
        sig_name = "ThermMgmtObsrvn5Byte5"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn5Byte1:
        sig_name = "ThermMgmtObsrvn5Byte1"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn5Byte7:
        sig_name = "ThermMgmtObsrvn5Byte7"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn5Byte4:
        sig_name = "ThermMgmtObsrvn5Byte4"
        sig_start_bit = 39
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
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn5Byte3:
        sig_name = "ThermMgmtObsrvn5Byte3"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn5Byte0:
        sig_name = "ThermMgmtObsrvn5Byte0"
        sig_start_bit = 7
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
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn5Byte6:
        sig_name = "ThermMgmtObsrvn5Byte6"
        sig_start_bit = 55
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
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn5Byte2:
        sig_name = "ThermMgmtObsrvn5Byte2"
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


class SumToVddmChas2DiagRespFrame:
    msg_name = "SumToVddmChas2DiagRespFrame"
    msg_id = 1556
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "SUM1"
    rx_nodes = ['VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class EcmChas2Fr47:
    msg_name = "EcmChas2Fr47"
    msg_id = 1138
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 1.0
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class EcmIntelliClimaResd12:
        sig_name = "EcmIntelliClimaResd12"
        sig_start_bit = 7
        update_id_bit = 55
        sig_length = 32
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 32
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class EcmIntelliClimaResd7:
        sig_name = "EcmIntelliClimaResd7"
        sig_start_bit = 39
        update_id_bit = 54
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0)]


class VddmChas2Fr11:
    msg_name = "VddmChas2Fr11"
    msg_id = 480
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.03
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']
    sig_group_dict = {'RoadIncln': ['RoadInclnQly', 'RoadInclnRoadIncln'], 'ALgtStdFromWhlSpd': ['ALgtStdFromWhlSpdALgtStdFromWhlSpd', 'ALgtStdFromWhlSpdChks', 'ALgtStdFromWhlSpdCntr', 'ALgtStdFromWhlSpdQf']}
    sig_group_dataid_dict = {'ALgtStdFromWhlSpd': 52}

    class ALgtStdFromWhlSpdChks:
        sig_name = "ALgtStdFromWhlSpdChks"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RoadInclnRoadIncln:
        sig_name = "RoadInclnRoadIncln"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 3.0518e-05
        sig_value_offset = 0.0
        sig_value_min = -32767
        sig_value_max = 32767
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class RoadIncln_UB:
        sig_name = "RoadIncln_UB"
        sig_start_bit = 7
        update_id_bit = 7
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ALgtStdFromWhlSpd_UB:
        sig_name = "ALgtStdFromWhlSpd_UB"
        sig_start_bit = 6
        update_id_bit = 6
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class ALgtStdFromWhlSpdQf:
        sig_name = "ALgtStdFromWhlSpdQf"
        sig_start_bit = 5
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
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class RoadInclnQly:
        sig_name = "RoadInclnQly"
        sig_start_bit = 55
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Qly2_Flt': 0, 'Qly2_NoInfo': 1, 'Qly2_Vld': 2}
        compute_method = None
        length = 2
        startbit = 55
        byte = 6
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class ALgtStdFromWhlSpdCntr:
        sig_name = "ALgtStdFromWhlSpdCntr"
        sig_start_bit = 3
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
        startbit = 3
        byte = 0
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class ALgtStdFromWhlSpdALgtStdFromWhlSpd:
        sig_name = "ALgtStdFromWhlSpdALgtStdFromWhlSpd"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 0.0009765625
        sig_value_offset = 0.0
        sig_value_min = -18432
        sig_value_max = 18432
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0)]


class SumChas2Fr05:
    msg_name = "SumChas2Fr05"
    msg_id = 687
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.03
    msg_length = 8
    tx_node = "SUM1"
    rx_nodes = ['S2SReceiver']
    sig_group_dict = {'SuspFailrSts': ['SuspFailrStsChks', 'SuspFailrStsCntr', 'SuspFailrStsSuspFailrSts', 'SuspFailrStsTypQf']}
    sig_group_dataid_dict = {}

    class SuspFailrSts3:
        sig_name = "SuspFailrSts3"
        sig_start_bit = 7
        update_id_bit = 0
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SuspFailrStsTyp4_NoErr': 0, 'SuspFailrStsTyp4_MinorErr': 1, 'SuspFailrStsTyp4_MajorErr': 2, 'SuspFailrStsTyp4_CritErr': 3}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class SuspFailrStsTypQf:
        sig_name = "SuspFailrStsTypQf"
        sig_start_bit = 41
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 41
        byte = 5
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class SuspFailrStsChks:
        sig_name = "SuspFailrStsChks"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SuspFailrStsCntr:
        sig_name = "SuspFailrStsCntr"
        sig_start_bit = 51
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
        startbit = 51
        byte = 6
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class SuspFailrStsSuspFailrSts:
        sig_name = "SuspFailrStsSuspFailrSts"
        sig_start_bit = 54
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SuspFailrStsTyp2_NoErr': 0, 'SuspFailrStsTyp2_TrSwtConUsg': 1, 'SuspFailrStsTyp2_CmprOvrheatd': 2, 'SuspFailrStsTyp2_SrvRqrdErr': 3, 'SuspFailrStsTyp2_StopCritErr': 4, 'SuspFailrStsTyp2_LoAirM': 5, 'SuspFailrStsTyp2_HiAirM': 6, 'SuspFailrStsTyp2_VehLvlHiOrLoErr': 7}
        compute_method = None
        length = 3
        startbit = 54
        byte = 6
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class SuspFailrSts_UB:
        sig_name = "SuspFailrSts_UB"
        sig_start_bit = 42
        update_id_bit = 42
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 42
        byte = 5
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2


class EcmChas2Fr50:
    msg_name = "EcmChas2Fr50"
    msg_id = 1141
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 1.0
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class EcmIntelliClimaResd15:
        sig_name = "EcmIntelliClimaResd15"
        sig_start_bit = 7
        update_id_bit = 45
        sig_length = 32
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 32
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0)]


class BbmChas2Fr03:
    msg_name = "BbmChas2Fr03"
    msg_id = 1245
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 1.0
    msg_length = 8
    tx_node = "BBM"
    rx_nodes = ['ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class BrkBoostClrRdyReq:
        sig_name = "BrkBoostClrRdyReq"
        sig_start_bit = 0
        update_id_bit = 1
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 0
        byte = 0
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class BrkBoostErrIndcnReq:
        sig_name = "BrkBoostErrIndcnReq"
        sig_start_bit = 2
        update_id_bit = 3
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 2
        byte = 0
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2


class EcmChas2Fr58:
    msg_name = "EcmChas2Fr58"
    msg_id = 1174
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 1.0
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']
    sig_group_dict = {'ThermMgmtObsrvn2': ['ThermMgmtObsrvn2Byte0', 'ThermMgmtObsrvn2Byte1', 'ThermMgmtObsrvn2Byte2', 'ThermMgmtObsrvn2Byte3', 'ThermMgmtObsrvn2Byte4', 'ThermMgmtObsrvn2Byte5', 'ThermMgmtObsrvn2Byte6', 'ThermMgmtObsrvn2Byte7']}
    sig_group_dataid_dict = {}

    class ThermMgmtObsrvn2Byte7:
        sig_name = "ThermMgmtObsrvn2Byte7"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn2Byte1:
        sig_name = "ThermMgmtObsrvn2Byte1"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn2Byte6:
        sig_name = "ThermMgmtObsrvn2Byte6"
        sig_start_bit = 55
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
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn2Byte2:
        sig_name = "ThermMgmtObsrvn2Byte2"
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

    class ThermMgmtObsrvn2Byte0:
        sig_name = "ThermMgmtObsrvn2Byte0"
        sig_start_bit = 7
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
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn2Byte3:
        sig_name = "ThermMgmtObsrvn2Byte3"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn2Byte5:
        sig_name = "ThermMgmtObsrvn2Byte5"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn2Byte4:
        sig_name = "ThermMgmtObsrvn2Byte4"
        sig_start_bit = 39
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
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class EcmChas2Fr13:
    msg_name = "EcmChas2Fr13"
    msg_id = 640
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.07
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class StrtMsgToModMngt:
        sig_name = "StrtMsgToModMngt"
        sig_start_bit = 63
        update_id_bit = 20
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'StrtMsgToModMgnt1_NoInhb': 0, 'StrtMsgToModMgnt1_PwrUpDly': 1, 'StrtMsgToModMgnt1_AltvStrt': 2, 'StrtMsgToModMgnt1_inhbremstrt': 3, 'StrtMsgToModMgnt1_diremstrt': 4, 'StrtMsgToModMgnt1_SelnOfParkOrNeut': 5, 'StrtMsgToModMgnt1_Resd1': 6, 'StrtMsgToModMgnt1_Resd2': 7}
        compute_method = None
        length = 3
        startbit = 63
        byte = 7
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5


class EtcToSumXcpFr01:
    msg_name = "EtcToSumXcpFr01"
    msg_id = 1418
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CCM"
    rx_nodes = ['SUM1']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class EtcBbmChas2DevFr02:
    msg_name = "EtcBbmChas2DevFr02"
    msg_id = 1428
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CCM"
    rx_nodes = ['BBM']
    sig_group_dict = {'BBMdevelpsignalgroupreq2': ['BBMdevelpsignalgroupreq2Functiondevpsignalgroup1', 'BBMdevelpsignalgroupreq2Functiondevpsignalgroup2', 'BBMdevelpsignalgroupreq2Functiondevpsignalgroup3', 'BBMdevelpsignalgroupreq2Functiondevpsignalgroup4', 'BBMdevelpsignalgroupreq2Functiondevpsignalgroup5', 'BBMdevelpsignalgroupreq2Functiondevpsignalgroup6', 'BBMdevelpsignalgroupreq2Functiondevpsignalgroup7', 'BBMdevelpsignalgroupreq2Functiondevpsignalgroup8']}
    sig_group_dataid_dict = {}

    class BBMdevelpsignalgroupreq2Functiondevpsignalgroup1:
        sig_name = "BBMdevelpsignalgroupreq2Functiondevpsignalgroup1"
        sig_start_bit = 7
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
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BBMdevelpsignalgroupreq2Functiondevpsignalgroup5:
        sig_name = "BBMdevelpsignalgroupreq2Functiondevpsignalgroup5"
        sig_start_bit = 39
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
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BBMdevelpsignalgroupreq2Functiondevpsignalgroup6:
        sig_name = "BBMdevelpsignalgroupreq2Functiondevpsignalgroup6"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BBMdevelpsignalgroupreq2Functiondevpsignalgroup2:
        sig_name = "BBMdevelpsignalgroupreq2Functiondevpsignalgroup2"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BBMdevelpsignalgroupreq2Functiondevpsignalgroup3:
        sig_name = "BBMdevelpsignalgroupreq2Functiondevpsignalgroup3"
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

    class BBMdevelpsignalgroupreq2Functiondevpsignalgroup4:
        sig_name = "BBMdevelpsignalgroupreq2Functiondevpsignalgroup4"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BBMdevelpsignalgroupreq2Functiondevpsignalgroup8:
        sig_name = "BBMdevelpsignalgroupreq2Functiondevpsignalgroup8"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BBMdevelpsignalgroupreq2Functiondevpsignalgroup7:
        sig_name = "BBMdevelpsignalgroupreq2Functiondevpsignalgroup7"
        sig_start_bit = 55
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
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class VddmChassisCAN2NmFr:
    msg_name = "VddmChassisCAN2NmFr"
    msg_id = 1314
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['SUM1']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class EcmChas2Fr31:
    msg_name = "EcmChas2Fr31"
    msg_id = 563
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.13
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class DrvPfmncRedn:
        sig_name = "DrvPfmncRedn"
        sig_start_bit = 19
        update_id_bit = 32
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoIndcn': 0, 'FltIndcn1': 1, 'FltIndcn2': 2, 'FltIndcn3': 3, 'FltIndcn4': 4, 'FltIndcn5': 5, 'FltIndcn6': 6, 'FltIndcn7': 7, 'FltIndcn8': 8, 'FltIndcn9': 9, 'FltIndcn10': 10, 'FltIndcn11': 11, 'FltIndcn12': 12, 'FltIndcn13': 13, 'FltIndcn14': 14, 'FltIndcn15': 15}
        compute_method = None
        length = 4
        startbit = 19
        byte = 2
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DispOfPrpsnModForEv:
        sig_name = "DispOfPrpsnModForEv"
        sig_start_bit = 23
        update_id_bit = 41
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DispOfPrpsnModForEv_NotReady': 0, 'DispOfPrpsnModForEv_Charging': 1, 'DispOfPrpsnModForEv_PureElecAWD': 2, 'DispOfPrpsnModForEv_OnlyPrpsnMotElecFrnt': 3, 'DispOfPrpsnModForEv_OnlyPrpsnMotElecRe': 4, 'DispOfPrpsnModForEv_NoPrpsnMotElec': 5, 'DispOfPrpsnModForEv_Rgn': 6, 'DispOfPrpsnModForEv_Reserved1': 7, 'DispOfPrpsnModForEv_Reserved2': 8, 'DispOfPrpsnModForEv_Reserved3': 9, 'DispOfPrpsnModForEv_Reserved4': 10, 'DispOfPrpsnModForEv_Reserved5': 11, 'DispOfPrpsnModForEv_Reserved6': 12, 'DispOfPrpsnModForEv_Abnormal': 13, 'DispOfPrpsnModForEv_Invalid': 14, 'DispOfPrpsnModForEv_Reserved7': 15}
        compute_method = None
        length = 4
        startbit = 23
        byte = 2
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class EgyRgnLvlAct:
        sig_name = "EgyRgnLvlAct"
        sig_start_bit = 60
        update_id_bit = 58
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EgyRgnLvlSet_Level1': 0, 'EgyRgnLvlSet_Level2': 1, 'EgyRgnLvlSet_Level3': 2, 'EgyRgnLvlSet_Level4': 3}
        compute_method = None
        length = 2
        startbit = 60
        byte = 7
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3


class VddmChas2Fr06:
    msg_name = "VddmChas2Fr06"
    msg_id = 240
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.025
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']
    sig_group_dict = {'PtTqAtAxleAddReq': ['PtTqAtAxleAddReqChks', 'PtTqAtAxleAddReqCntr', 'PtTqAtAxleAddReqPtTqAtAxleAddFrntReq', 'PtTqAtAxleAddReqPtTqAtAxleAddReReq']}
    sig_group_dataid_dict = {'PtTqAtAxleAddReq': 108}

    class DoorDrvrSts:
        sig_name = "DoorDrvrSts"
        sig_start_bit = 53
        update_id_bit = 5
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorSts2_Ukwn': 0, 'DoorSts2_Opend': 1, 'DoorSts2_Clsd': 2}
        compute_method = None
        length = 2
        startbit = 53
        byte = 6
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class PtTqAtAxleAddReqPtTqAtAxleAddReReq:
        sig_name = "PtTqAtAxleAddReqPtTqAtAxleAddReReq"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11000000, 0b00111111, 2, 6)]

    class PtTqAtAxleAddReqPtTqAtAxleAddFrntReq:
        sig_name = "PtTqAtAxleAddReqPtTqAtAxleAddFrntReq"
        sig_start_bit = 1
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 1
        bmuws_info = [(0, 0b00000011, 0b11111100, 2, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class PtTqAtAxleAddReq_UB:
        sig_name = "PtTqAtAxleAddReq_UB"
        sig_start_bit = 58
        update_id_bit = 58
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 58
        byte = 7
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class HoodSts:
        sig_name = "HoodSts"
        sig_start_bit = 63
        update_id_bit = 2
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorSts2_Ukwn': 0, 'DoorSts2_Opend': 1, 'DoorSts2_Clsd': 2}
        compute_method = None
        length = 2
        startbit = 63
        byte = 7
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class PtTqAtAxleAddReqChks:
        sig_name = "PtTqAtAxleAddReqChks"
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

    class PtTqAtAxleAddReqCntr:
        sig_name = "PtTqAtAxleAddReqCntr"
        sig_start_bit = 37
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
        startbit = 37
        byte = 4
        mask = 0b00111100
        unmask = 0b11000011
        shift = 2

    class DoorPassSts:
        sig_name = "DoorPassSts"
        sig_start_bit = 49
        update_id_bit = 3
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorSts2_Ukwn': 0, 'DoorSts2_Opend': 1, 'DoorSts2_Clsd': 2}
        compute_method = None
        length = 2
        startbit = 49
        byte = 6
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0


class BgmChas2Fr01:
    msg_name = "BgmChas2Fr01"
    msg_id = 96
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['SUM1']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class DrvModSet:
        sig_name = "DrvModSet"
        sig_start_bit = 7
        update_id_bit = 3
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DrvModReqType1_Undefd': 0, 'DrvModReqType1_ECO': 1, 'DrvModReqType1_Comfort_Normal': 2, 'DrvModReqType1_Dynamic_Sport': 3, 'DrvModReqType1_Reserved1': 4, 'DrvModReqType1_Offroad_CrossTerrain': 5, 'DrvModReqType1_Adaptive': 6, 'DrvModReqType1_Race': 7, 'DrvModReqType1_Reserved2': 8, 'DrvModReqType1_ECO_PLUS': 9, 'DrvModReqType1_Power': 10, 'DrvModReqType1_Snow': 11, 'DrvModReqType1_Sand': 12, 'DrvModReqType1_Mud': 13, 'DrvModReqType1_Rock': 14, 'DrvModReqType1_Err': 15}
        compute_method = None
        length = 4
        startbit = 7
        byte = 0
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class ModReqOfDampr:
        sig_name = "ModReqOfDampr"
        sig_start_bit = 2
        update_id_bit = 15
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
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


class EcmChas2Fr57:
    msg_name = "EcmChas2Fr57"
    msg_id = 1173
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 1.0
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']
    sig_group_dict = {'ThermMgmtObsrvn10': ['ThermMgmtObsrvn10Byte0', 'ThermMgmtObsrvn10Byte1', 'ThermMgmtObsrvn10Byte2', 'ThermMgmtObsrvn10Byte3', 'ThermMgmtObsrvn10Byte4', 'ThermMgmtObsrvn10Byte5', 'ThermMgmtObsrvn10Byte6', 'ThermMgmtObsrvn10Byte7']}
    sig_group_dataid_dict = {}

    class ThermMgmtObsrvn10Byte2:
        sig_name = "ThermMgmtObsrvn10Byte2"
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

    class ThermMgmtObsrvn10Byte7:
        sig_name = "ThermMgmtObsrvn10Byte7"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn10Byte3:
        sig_name = "ThermMgmtObsrvn10Byte3"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn10Byte6:
        sig_name = "ThermMgmtObsrvn10Byte6"
        sig_start_bit = 55
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
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn10Byte5:
        sig_name = "ThermMgmtObsrvn10Byte5"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn10Byte4:
        sig_name = "ThermMgmtObsrvn10Byte4"
        sig_start_bit = 39
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
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn10Byte0:
        sig_name = "ThermMgmtObsrvn10Byte0"
        sig_start_bit = 7
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
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn10Byte1:
        sig_name = "ThermMgmtObsrvn10Byte1"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class EcmChas2Fr07:
    msg_name = "EcmChas2Fr07"
    msg_id = 288
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['BBM', 'VDDM']
    sig_group_dict = {'AccrPedlNotCmpl': ['AccrPedlNotCmplPsd', 'AccrPedlNotCmplPsdChks', 'AccrPedlNotCmplPsdCntr', 'AccrPedlNotCmplPsdSts'], 'DtEngdSt': ['DtEngdStDtEngdFrnt', 'DtEngdStDtEngdRe', 'DtEngdStDtNotEngdFrnt', 'DtEngdStDtNotEngdRe']}
    sig_group_dataid_dict = {'AccrPedlNotCmpl': 205}

    class AccrPedlNotCmplPsdCntr:
        sig_name = "AccrPedlNotCmplPsdCntr"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class GearLvrIndcn:
        sig_name = "GearLvrIndcn"
        sig_start_bit = 52
        update_id_bit = 48
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 7
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GearLvrIndcn2_ParkIndcn': 0, 'GearLvrIndcn2_RvsIndcn': 1, 'GearLvrIndcn2_NeutIndcn': 2, 'GearLvrIndcn2_DrvIndcn': 3, 'GearLvrIndcn2_ManModeIndcn': 4, 'GearLvrIndcn2_Resd1': 5, 'GearLvrIndcn2_Resd2': 6, 'GearLvrIndcn2_Undefd': 7}
        compute_method = None
        length = 3
        startbit = 52
        byte = 6
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class AccrPedlNotCmplPsd:
        sig_name = "AccrPedlNotCmplPsd"
        sig_start_bit = 11
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 11
        byte = 1
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class DtEngdStDtEngdFrnt:
        sig_name = "DtEngdStDtEngdFrnt"
        sig_start_bit = 63
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flg1_Rst': 0, 'Flg1_Set': 1}
        compute_method = None
        length = 1
        startbit = 63
        byte = 7
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class DtEngdStDtNotEngdRe:
        sig_name = "DtEngdStDtNotEngdRe"
        sig_start_bit = 60
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flg1_Rst': 0, 'Flg1_Set': 1}
        compute_method = None
        length = 1
        startbit = 60
        byte = 7
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class AccrPedlNotCmpl_UB:
        sig_name = "AccrPedlNotCmpl_UB"
        sig_start_bit = 9
        update_id_bit = 9
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 9
        byte = 1
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class DtEngdSt_UB:
        sig_name = "DtEngdSt_UB"
        sig_start_bit = 38
        update_id_bit = 38
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 38
        byte = 4
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class EPedlModSts:
        sig_name = "EPedlModSts"
        sig_start_bit = 55
        update_id_bit = 8
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 1
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CrsCtrlrSts1_Off': 1, 'CrsCtrlrSts1_Stb': 2, 'CrsCtrlrSts1_Actv': 3}
        compute_method = None
        length = 3
        startbit = 55
        byte = 6
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DtEngdStDtNotEngdFrnt:
        sig_name = "DtEngdStDtNotEngdFrnt"
        sig_start_bit = 61
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flg1_Rst': 0, 'Flg1_Set': 1}
        compute_method = None
        length = 1
        startbit = 61
        byte = 7
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class DtEngdStDtEngdRe:
        sig_name = "DtEngdStDtEngdRe"
        sig_start_bit = 62
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flg1_Rst': 0, 'Flg1_Set': 1}
        compute_method = None
        length = 1
        startbit = 62
        byte = 7
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class AccrPedlNotCmplPsdSts:
        sig_name = "AccrPedlNotCmplPsdSts"
        sig_start_bit = 10
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 10
        byte = 1
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class AccrPedlNotCmplPsdChks:
        sig_name = "AccrPedlNotCmplPsdChks"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 255
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class VddmChas2Fr52:
    msg_name = "VddmChas2Fr52"
    msg_id = 103
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.04
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']
    sig_group_dict = {'PtTqSetSafe': ['PtTqSetSafeChks', 'PtTqSetSafeCntr', 'PtTqSetSafeGrdtNeg', 'PtTqSetSafeGrdtPos', 'PtTqSetSafeReq']}
    sig_group_dataid_dict = {'PtTqSetSafe': 884}

    class PtTqSetSafeGrdtPos:
        sig_name = "PtTqSetSafeGrdtPos"
        sig_start_bit = 36
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 4.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 36
        bmuws_info = [(4, 0b00011111, 0b11100000, 5, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class PtTqSetSafeChks:
        sig_name = "PtTqSetSafeChks"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class PtTqSetSafeGrdtNeg:
        sig_name = "PtTqSetSafeGrdtNeg"
        sig_start_bit = 20
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 4.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 20
        bmuws_info = [(2, 0b00011111, 0b11100000, 5, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class PtTqSetSafeCntr:
        sig_name = "PtTqSetSafeCntr"
        sig_start_bit = 3
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
        startbit = 3
        byte = 0
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class PtTqSetSafeReq:
        sig_name = "PtTqSetSafeReq"
        sig_start_bit = 52
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 4.0
        sig_value_offset = 0.0
        sig_value_min = -4096
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 52
        bmuws_info = [(6, 0b00011111, 0b11100000, 5, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class PtTqSetSafe_UB:
        sig_name = "PtTqSetSafe_UB"
        sig_start_bit = 4
        update_id_bit = 4
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 4
        byte = 0
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4


class BbmRbcmChas2Fr01:
    msg_name = "BbmRbcmChas2Fr01"
    msg_id = 278
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "BBM"
    rx_nodes = ['VDDM']
    sig_group_dict = {'SecBrkSysSt2': ['SecBrkSysSt2BrkSysSt', 'SecBrkSysSt2Chks', 'SecBrkSysSt2Cntr']}
    sig_group_dataid_dict = {'SecBrkSysSt2': 881}

    class SecBrkSysSt2_UB:
        sig_name = "SecBrkSysSt2_UB"
        sig_start_bit = 23
        update_id_bit = 23
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 23
        byte = 2
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class SecBrkSysSt2BrkSysSt:
        sig_name = "SecBrkSysSt2BrkSysSt"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 11
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NotAvailable_Temporary': 0, 'NotAvailable_NotReleased': 1, 'NotAvailable_Permanent': 2, 'NotActivated_FullAvailable': 3, 'Activation_Preparation': 4, 'Activation_Pending': 5, 'Activation_PendingRedundancyLost': 6, 'Activation_PendingFailOperation': 7, 'Activated_FullAvailable': 8, 'Activated_FailOperation': 9, 'Activated_RedundancyLost': 10, 'Deactivation_Pending': 11}
        compute_method = None
        length = 4
        startbit = 7
        byte = 0
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class SecBrkSysSt2Chks:
        sig_name = "SecBrkSysSt2Chks"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SecBrkSysSt2Cntr:
        sig_name = "SecBrkSysSt2Cntr"
        sig_start_bit = 3
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
        startbit = 3
        byte = 0
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0


class EcmChas2Fr64:
    msg_name = "EcmChas2Fr64"
    msg_id = 1165
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 1.0
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']
    sig_group_dict = {'ThermMgmtObsrvn8': ['ThermMgmtObsrvn8Byte0', 'ThermMgmtObsrvn8Byte1', 'ThermMgmtObsrvn8Byte2', 'ThermMgmtObsrvn8Byte3', 'ThermMgmtObsrvn8Byte4', 'ThermMgmtObsrvn8Byte5', 'ThermMgmtObsrvn8Byte6', 'ThermMgmtObsrvn8Byte7']}
    sig_group_dataid_dict = {}

    class ThermMgmtObsrvn8Byte2:
        sig_name = "ThermMgmtObsrvn8Byte2"
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

    class ThermMgmtObsrvn8Byte3:
        sig_name = "ThermMgmtObsrvn8Byte3"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn8Byte4:
        sig_name = "ThermMgmtObsrvn8Byte4"
        sig_start_bit = 39
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
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn8Byte6:
        sig_name = "ThermMgmtObsrvn8Byte6"
        sig_start_bit = 55
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
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn8Byte7:
        sig_name = "ThermMgmtObsrvn8Byte7"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn8Byte5:
        sig_name = "ThermMgmtObsrvn8Byte5"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn8Byte1:
        sig_name = "ThermMgmtObsrvn8Byte1"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn8Byte0:
        sig_name = "ThermMgmtObsrvn8Byte0"
        sig_start_bit = 7
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
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class EcmChas2Fr18:
    msg_name = "EcmChas2Fr18"
    msg_id = 752
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.08
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['BBM', 'VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class PrpsnModSptBlkd:
        sig_name = "PrpsnModSptBlkd"
        sig_start_bit = 27
        update_id_bit = 51
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Typ1_Typ0': 0, 'Typ1_Typ1': 1, 'Typ1_Typ2': 2, 'Typ1_Typ3': 3, 'Typ1_Typ4': 4, 'Typ1_Typ5': 5, 'Typ1_Typ6': 6, 'Typ1_Typ7': 7}
        compute_method = None
        length = 3
        startbit = 27
        byte = 3
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class ImobBrkNrSerlReq:
        sig_name = "ImobBrkNrSerlReq"
        sig_start_bit = 28
        update_id_bit = 42
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 28
        byte = 3
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class EngEgyEffElec:
        sig_name = "EngEgyEffElec"
        sig_start_bit = 14
        update_id_bit = 55
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_byteorder = "Motorola"
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EngEgyEffElec_VeryCheap': 0, 'EngEgyEffElec_Cheap': 1, 'EngEgyEffElec_Norm': 2, 'EngEgyEffElec_Expn': 3, 'EngEgyEffElec_VeryExpn': 4}
        compute_method = None
        length = 3
        startbit = 14
        byte = 1
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class PtParkReqToWhlsRe:
        sig_name = "PtParkReqToWhlsRe"
        sig_start_bit = 47
        update_id_bit = 46
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ReqSts1_NotReqd': 0, 'ReqSts1_Reqd': 1}
        compute_method = None
        length = 1
        startbit = 47
        byte = 5
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7


class EcmChas2Fr20:
    msg_name = "EcmChas2Fr20"
    msg_id = 547
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.03
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM', 'S2SReceiver', 'CCM']
    sig_group_dict = {'PrpsnActvn': ['PrpsnActvnChks', 'PrpsnActvnCntr', 'PrpsnActvnInhbBySteerLock', 'PrpsnActvnSt']}
    sig_group_dataid_dict = {}

    class PrpsnActvnSt:
        sig_name = "PrpsnActvnSt"
        sig_start_bit = 29
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PrpsnActvnSt_Undefined': 0, 'PrpsnActvnSt_PrpsnDi': 1, 'PrpsnActvnSt_PrpsnEnad': 2}
        compute_method = None
        length = 2
        startbit = 29
        byte = 3
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class PrpsnActvn_UB:
        sig_name = "PrpsnActvn_UB"
        sig_start_bit = 31
        update_id_bit = 31
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 31
        byte = 3
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class PrpsnActvnChks:
        sig_name = "PrpsnActvnChks"
        sig_start_bit = 39
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
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CrsCtrlrActvnOk:
        sig_name = "CrsCtrlrActvnOk"
        sig_start_bit = 20
        update_id_bit = 19
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 20
        byte = 2
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class PrpsnActvnInhbBySteerLock:
        sig_name = "PrpsnActvnInhbBySteerLock"
        sig_start_bit = 30
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 30
        byte = 3
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class AdjSpdLimnFusnTrfcSgn:
        sig_name = "AdjSpdLimnFusnTrfcSgn"
        sig_start_bit = 41
        update_id_bit = 40
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 41
        byte = 5
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class LimSts:
        sig_name = "LimSts"
        sig_start_bit = 54
        update_id_bit = 55
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LimSts_Unknown': 0, 'LimSts_ManuallySet': 1, 'LimSts_AutomaticallySet': 2, 'LimSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 54
        byte = 6
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class AdjSpdLimnSts:
        sig_name = "AdjSpdLimnSts"
        sig_start_bit = 51
        update_id_bit = 48
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 1
        sig_value_max = 4
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AdjSpdLimnSts2_Off': 1, 'AdjSpdLimnSts2_Stb': 2, 'AdjSpdLimnSts2_Actv': 3, 'AdjSpdLimnSts2_Ovrd': 4}
        compute_method = None
        length = 3
        startbit = 51
        byte = 6
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class AdjSpdLimnStbOk:
        sig_name = "AdjSpdLimnStbOk"
        sig_start_bit = 59
        update_id_bit = 58
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 59
        byte = 7
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class CrsCtrlrStbOk:
        sig_name = "CrsCtrlrStbOk"
        sig_start_bit = 17
        update_id_bit = 16
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 17
        byte = 2
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class AdjSpdLimnActvnOk:
        sig_name = "AdjSpdLimnActvnOk"
        sig_start_bit = 57
        update_id_bit = 56
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 57
        byte = 7
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class CrsCtrlrSts:
        sig_name = "CrsCtrlrSts"
        sig_start_bit = 62
        update_id_bit = 63
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 1
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CrsCtrlrSts1_Off': 1, 'CrsCtrlrSts1_Stb': 2, 'CrsCtrlrSts1_Actv': 3}
        compute_method = None
        length = 3
        startbit = 62
        byte = 7
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class PrpsnActvnCntr:
        sig_name = "PrpsnActvnCntr"
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

    class AdjSpdLimnWarn:
        sig_name = "AdjSpdLimnWarn"
        sig_start_bit = 23
        update_id_bit = 21
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AdjSpdLimnWarnCoding_NoWarn': 0, 'AdjSpdLimnWarnCoding_SoundWarn': 1, 'AdjSpdLimnWarnCoding_VisWarn': 2, 'AdjSpdLimnWarnCoding_SoundAndVisWarn': 3}
        compute_method = None
        length = 2
        startbit = 23
        byte = 2
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class VddmChas2Fr25:
    msg_name = "VddmChas2Fr25"
    msg_id = 896
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.7
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['BBM', 'ECM', 'SUM1']
    sig_group_dict = {'VehBattU': ['VehBattUSysU', 'VehBattUSysUQf']}
    sig_group_dataid_dict = {}

    class VehBattUSysU:
        sig_name = "VehBattUSysU"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class EngPwrAllwdDeltaWdCmd:
        sig_name = "EngPwrAllwdDeltaWdCmd"
        sig_start_bit = 7
        update_id_bit = 46
        sig_length = 12
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = -2048
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11110000, 0b00001111, 4, 4)]

    class VehBattU_UB:
        sig_name = "VehBattU_UB"
        sig_start_bit = 54
        update_id_bit = 54
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 54
        byte = 6
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class PwrAvlRednWdSts:
        sig_name = "PwrAvlRednWdSts"
        sig_start_bit = 11
        update_id_bit = 45
        sig_length = 12
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = -2048
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 11
        bmuws_info = [(1, 0b00001111, 0b11110000, 4, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class VehBattUSysUQf:
        sig_name = "VehBattUSysUQf"
        sig_start_bit = 49
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
        startbit = 49
        byte = 6
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class EngCooltLvl:
        sig_name = "EngCooltLvl"
        sig_start_bit = 51
        update_id_bit = 50
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FldLvl_FldLvlHi': 0, 'FldLvl_FldLvlLo': 1}
        compute_method = None
        length = 1
        startbit = 51
        byte = 6
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3


class EcmChas2Fr62:
    msg_name = "EcmChas2Fr62"
    msg_id = 1163
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 1.0
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']
    sig_group_dict = {'ThermMgmtObsrvn6': ['ThermMgmtObsrvn6Byte0', 'ThermMgmtObsrvn6Byte1', 'ThermMgmtObsrvn6Byte2', 'ThermMgmtObsrvn6Byte3', 'ThermMgmtObsrvn6Byte4', 'ThermMgmtObsrvn6Byte5', 'ThermMgmtObsrvn6Byte6', 'ThermMgmtObsrvn6Byte7']}
    sig_group_dataid_dict = {}

    class ThermMgmtObsrvn6Byte3:
        sig_name = "ThermMgmtObsrvn6Byte3"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn6Byte4:
        sig_name = "ThermMgmtObsrvn6Byte4"
        sig_start_bit = 39
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
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn6Byte7:
        sig_name = "ThermMgmtObsrvn6Byte7"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn6Byte5:
        sig_name = "ThermMgmtObsrvn6Byte5"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn6Byte2:
        sig_name = "ThermMgmtObsrvn6Byte2"
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

    class ThermMgmtObsrvn6Byte0:
        sig_name = "ThermMgmtObsrvn6Byte0"
        sig_start_bit = 7
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
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn6Byte6:
        sig_name = "ThermMgmtObsrvn6Byte6"
        sig_start_bit = 55
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
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn6Byte1:
        sig_name = "ThermMgmtObsrvn6Byte1"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class EcmChas2Fr66:
    msg_name = "EcmChas2Fr66"
    msg_id = 1114
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.5
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']
    sig_group_dict = {'ISecDcDcActLoSide': ['ISecDcDcActLoSideChks', 'ISecDcDcActLoSideCntr', 'ISecDcDcActLoSideIDcDcActLoSide']}
    sig_group_dataid_dict = {}

    class ISecDcDcActLoSide_UB:
        sig_name = "ISecDcDcActLoSide_UB"
        sig_start_bit = 49
        update_id_bit = 49
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 49
        byte = 6
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class FltElecSecDcDc:
        sig_name = "FltElecSecDcDc"
        sig_start_bit = 57
        update_id_bit = 56
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevErrSts2_NoFlt': 0, 'DevErrSts2_Flt': 1}
        compute_method = None
        length = 1
        startbit = 57
        byte = 7
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class FltTSecDcDc:
        sig_name = "FltTSecDcDc"
        sig_start_bit = 60
        update_id_bit = 59
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevErrSts2_NoFlt': 0, 'DevErrSts2_Flt': 1}
        compute_method = None
        length = 1
        startbit = 60
        byte = 7
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class ISecDcDcActLoSideChks:
        sig_name = "ISecDcDcActLoSideChks"
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

    class ISecDcDcActLoSideIDcDcActLoSide:
        sig_name = "ISecDcDcActLoSideIDcDcActLoSide"
        sig_start_bit = 3
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 3
        bmuws_info = [(0, 0b00001111, 0b11110000, 4, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class LimnIndcnSecDcDc:
        sig_name = "LimnIndcnSecDcDc"
        sig_start_bit = 31
        update_id_bit = 48
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111111, 0b00000000, 8, 0)]

    class ISecDcDcActLoSideCntr:
        sig_name = "ISecDcDcActLoSideCntr"
        sig_start_bit = 7
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
        startbit = 7
        byte = 0
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class ISecDcDcActHiSide:
        sig_name = "ISecDcDcActHiSide"
        sig_start_bit = 47
        update_id_bit = 50
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = -410.0
        sig_value_min = 0
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 4100
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111000, 0b00000111, 5, 3)]


class VddmChas2Fr31:
    msg_name = "VddmChas2Fr31"
    msg_id = 832
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.12
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']
    sig_group_dict = {'Vin': ['VinBlockNr', 'VinVINSignalPos1', 'VinVINSignalPos2', 'VinVINSignalPos3', 'VinVINSignalPos4', 'VinVINSignalPos5', 'VinVINSignalPos6', 'VinVINSignalPos7']}
    sig_group_dataid_dict = {}

    class VinVINSignalPos1:
        sig_name = "VinVINSignalPos1"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VinVINSignalPos2:
        sig_name = "VinVINSignalPos2"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 23
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VinVINSignalPos4:
        sig_name = "VinVINSignalPos4"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VinVINSignalPos3:
        sig_name = "VinVINSignalPos3"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VinVINSignalPos7:
        sig_name = "VinVINSignalPos7"
        sig_start_bit = 63
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VinVINSignalPos5:
        sig_name = "VinVINSignalPos5"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VinVINSignalPos6:
        sig_name = "VinVINSignalPos6"
        sig_start_bit = 55
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VinBlockNr:
        sig_name = "VinBlockNr"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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


class VddmChas2VFCinfoEnaFr:
    msg_name = "VddmChas2VFCinfoEnaFr"
    msg_id = 1519
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['SUM1']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class VFCInfoEna:
        sig_name = "VFCInfoEna"
        sig_start_bit = 57
        update_id_bit = 58
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EnableDisableCoding_Disabled': 0, 'EnableDisableCoding_Enabled': 1}
        compute_method = None
        length = 1
        startbit = 57
        byte = 7
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1


class EcmChas2Fr65:
    msg_name = "EcmChas2Fr65"
    msg_id = 1178
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 1.0
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']
    sig_group_dict = {'ThermMgmtObsrvn9': ['ThermMgmtObsrvn9Byte0', 'ThermMgmtObsrvn9Byte1', 'ThermMgmtObsrvn9Byte2', 'ThermMgmtObsrvn9Byte3', 'ThermMgmtObsrvn9Byte4', 'ThermMgmtObsrvn9Byte5', 'ThermMgmtObsrvn9Byte6', 'ThermMgmtObsrvn9Byte7']}
    sig_group_dataid_dict = {}

    class ThermMgmtObsrvn9Byte3:
        sig_name = "ThermMgmtObsrvn9Byte3"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn9Byte5:
        sig_name = "ThermMgmtObsrvn9Byte5"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn9Byte0:
        sig_name = "ThermMgmtObsrvn9Byte0"
        sig_start_bit = 7
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
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn9Byte4:
        sig_name = "ThermMgmtObsrvn9Byte4"
        sig_start_bit = 39
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
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn9Byte2:
        sig_name = "ThermMgmtObsrvn9Byte2"
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

    class ThermMgmtObsrvn9Byte1:
        sig_name = "ThermMgmtObsrvn9Byte1"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn9Byte6:
        sig_name = "ThermMgmtObsrvn9Byte6"
        sig_start_bit = 55
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
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ThermMgmtObsrvn9Byte7:
        sig_name = "ThermMgmtObsrvn9Byte7"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class BbmChas2Fr01:
    msg_name = "BbmChas2Fr01"
    msg_id = 258
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.04
    msg_length = 8
    tx_node = "BBM"
    rx_nodes = ['ECM']
    sig_group_dict = {'BrkPedlTrvl': ['BrkPedlTrvlAct', 'BrkPedlTrvlChks', 'BrkPedlTrvlCntr', 'BrkPedlTrvlQf', 'BrkPedlTrvlSt', 'BrkPedlTrvlStQf', 'BrkPedlTrvlTar']}
    sig_group_dataid_dict = {'BrkPedlTrvl': 179}

    class BrkPedlTrvlAct:
        sig_name = "BrkPedlTrvlAct"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 0.01
        sig_value_offset = -5.0
        sig_value_min = 0
        sig_value_max = 5200
        sig_byteorder = "Motorola"
        sig_value_init = 500
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111000, 0b00000111, 5, 3)]

    class BrkPedlTrvlCntr:
        sig_name = "BrkPedlTrvlCntr"
        sig_start_bit = 3
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
        startbit = 3
        byte = 0
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class BrkPedlTrvlStQf:
        sig_name = "BrkPedlTrvlStQf"
        sig_start_bit = 26
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
        startbit = 26
        byte = 3
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class BrkPedlTrvlTar:
        sig_name = "BrkPedlTrvlTar"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 0.01
        sig_value_offset = -5.0
        sig_value_min = 0
        sig_value_max = 5200
        sig_byteorder = "Motorola"
        sig_value_init = 500
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111000, 0b00000111, 5, 3)]

    class BrkPedlTrvl_UB:
        sig_name = "BrkPedlTrvl_UB"
        sig_start_bit = 6
        update_id_bit = 6
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class BrkPedlTrvlQf:
        sig_name = "BrkPedlTrvlQf"
        sig_start_bit = 5
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
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class BrkPedlTrvlChks:
        sig_name = "BrkPedlTrvlChks"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 255
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BrkPedlTrvlSt:
        sig_name = "BrkPedlTrvlSt"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PsdNotPsd_NotPsd': 0, 'PsdNotPsd_Psd': 1}
        compute_method = None
        length = 1
        startbit = 24
        byte = 3
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0


class EcmChas2Fr38:
    msg_name = "EcmChas2Fr38"
    msg_id = 819
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.27
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['BBM', 'VDDM']
    sig_group_dict = {'EexvSts': ['EexvStsExvActrPosn', 'EexvStsExvBlkErr', 'EexvStsExvCalibSts', 'EexvStsExvElecStsErr', 'EexvStsExvMovSts', 'EexvStsExvOvrTempErr', 'EexvStsExvOvrTrvlErr', 'EexvStsExvPreHeatgSts', 'EexvStsExvVoltgRangErr']}
    sig_group_dataid_dict = {}

    class EexvStsExvPreHeatgSts:
        sig_name = "EexvStsExvPreHeatgSts"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 35
        byte = 4
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class EexvStsExvActrPosn:
        sig_name = "EexvStsExvActrPosn"
        sig_start_bit = 41
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.2
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 500
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 41
        bmuws_info = [(5, 0b00000011, 0b11111100, 2, 0), (6, 0b11111111, 0b00000000, 8, 0)]

    class HvCooltWtrHeatrWtrTInIntk:
        sig_name = "HvCooltWtrHeatrWtrTInIntk"
        sig_start_bit = 23
        update_id_bit = 12
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 40
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 23
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class EexvStsExvCalibSts:
        sig_name = "EexvStsExvCalibSts"
        sig_start_bit = 44
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvCalibSts_NotInitialized': 0, 'ExvCalibSts_InitializationInProcess': 1, 'ExvCalibSts_Initialized': 2, 'ExvCalibSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 44
        byte = 5
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class ThermFctReq:
        sig_name = "ThermFctReq"
        sig_start_bit = 9
        update_id_bit = 8
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 9
        byte = 1
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class EexvStsExvOvrTempErr:
        sig_name = "EexvStsExvOvrTempErr"
        sig_start_bit = 33
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err1_NoErr': 0, 'Err1_Err': 1}
        compute_method = None
        length = 1
        startbit = 33
        byte = 4
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class EexvStsExvVoltgRangErr:
        sig_name = "EexvStsExvVoltgRangErr"
        sig_start_bit = 37
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VoltgRangErr_NoErr': 0, 'VoltgRangErr_UnderVoltageErr': 1, 'VoltgRangErr_OverVoltageErr': 2, 'VoltgRangErr_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 37
        byte = 4
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class EPedlDrvrIndcnMsg:
        sig_name = "EPedlDrvrIndcnMsg"
        sig_start_bit = 31
        update_id_bit = 29
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'IndcnMsg_NoIndcn': 0, 'IndcnMsg_AVHNoActive': 1, 'IndcnMsg_Flt': 2, 'IndcnMsg_LowPrio': 3}
        compute_method = None
        length = 2
        startbit = 31
        byte = 3
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HvHeatrPwrCnsDes:
        sig_name = "HvHeatrPwrCnsDes"
        sig_start_bit = 7
        update_id_bit = 13
        sig_length = 10
        sig_value_factor = 20.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class EexvStsExvMovSts:
        sig_name = "EexvStsExvMovSts"
        sig_start_bit = 32
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvMovSts_NotMove': 0, 'ExvMovSts_Moving': 1}
        compute_method = None
        length = 1
        startbit = 32
        byte = 4
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class EexvStsExvBlkErr:
        sig_name = "EexvStsExvBlkErr"
        sig_start_bit = 42
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err1_NoErr': 0, 'Err1_Err': 1}
        compute_method = None
        length = 1
        startbit = 42
        byte = 5
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class GearShiftUnitSts:
        sig_name = "GearShiftUnitSts"
        sig_start_bit = 28
        update_id_bit = 25
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoFlt': 0, 'NoUpTipAut': 1, 'NoDwnTipAut': 2, 'NoPark': 3, 'SrvRqrd': 4, 'NoUpUpTipAut': 5, 'NoDownDownTipAut': 6, 'Nounlock': 7}
        compute_method = None
        length = 3
        startbit = 28
        byte = 3
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class EexvSts_UB:
        sig_name = "EexvSts_UB"
        sig_start_bit = 38
        update_id_bit = 38
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 38
        byte = 4
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class EexvStsExvOvrTrvlErr:
        sig_name = "EexvStsExvOvrTrvlErr"
        sig_start_bit = 34
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err1_NoErr': 0, 'Err1_Err': 1}
        compute_method = None
        length = 1
        startbit = 34
        byte = 4
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class EexvStsExvElecStsErr:
        sig_name = "EexvStsExvElecStsErr"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvElecStsErr_NoError': 0, 'ExvElecStsErr_OpenCircuit': 1, 'ExvElecStsErr_ShortCircuit': 2, 'ExvElecStsErr_OverTemperatureShutdown': 3, 'ExvElecStsErr_IndeterminateElectricFault': 4, 'ExvElecStsErr_Reserved': 5}
        compute_method = None
        length = 3
        startbit = 47
        byte = 5
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5


class EcmChas2Fr09:
    msg_name = "EcmChas2Fr09"
    msg_id = 512
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class DispOfPrpsnPwrPercAct:
        sig_name = "DispOfPrpsnPwrPercAct"
        sig_start_bit = 2
        update_id_bit = 3
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = -1000
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 2
        bmuws_info = [(0, 0b00000111, 0b11111000, 3, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class DchaStopByTarDrvrIndcn:
        sig_name = "DchaStopByTarDrvrIndcn"
        sig_start_bit = 7
        update_id_bit = 6
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ReqSts1_NotReqd': 0, 'ReqSts1_Reqd': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class EmotCooltIndcnReq:
        sig_name = "EmotCooltIndcnReq"
        sig_start_bit = 29
        update_id_bit = 28
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 29
        byte = 3
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class EPedlInhbnSts:
        sig_name = "EPedlInhbnSts"
        sig_start_bit = 31
        update_id_bit = 30
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 31
        byte = 3
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7


class VddmChas2Fr02:
    msg_name = "VddmChas2Fr02"
    msg_id = 112
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.015
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM', 'SUM1']
    sig_group_dict = {'VehDynCtrlStsForALgtCmft': ['VehDynCtrlStsForALgtCmftVehDynCtrlStsChks', 'VehDynCtrlStsForALgtCmftVehDynCtrlStsCntr', 'VehDynCtrlStsForALgtCmftVehDynCtrlStsDend', 'VehDynCtrlStsForALgtCmftVehDynCtrlStsForBrkActv', 'VehDynCtrlStsForALgtCmftVehDynCtrlStsForBrkPrecActv', 'VehDynCtrlStsForALgtCmftVehDynCtrlStsForStandStillMgrForPark', 'VehDynCtrlStsForALgtCmftVehDynCtrlStsForWhlBrkWrm', 'VehDynCtrlStsForALgtCmftVehDynCtrlStsNotEna'], 'LimForJerkPosNotExcd': ['LimForJerkPosNotExcdChks', 'LimForJerkPosNotExcdCntr', 'LimForJerkPosNotExcdLimForJerkPosNotExcd']}
    sig_group_dataid_dict = {'VehDynCtrlStsForALgtCmft': 135, 'LimForJerkPosNotExcd': 115}

    class YawRateReqdByDrvr:
        sig_name = "YawRateReqdByDrvr"
        sig_start_bit = 55
        update_id_bit = 9
        sig_length = 16
        sig_value_factor = 0.000244140625
        sig_value_offset = 0.0
        sig_value_min = -20480
        sig_value_max = 20480
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 55
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class VehDynCtrlStsForALgtCmftVehDynCtrlStsChks:
        sig_name = "VehDynCtrlStsForALgtCmftVehDynCtrlStsChks"
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

    class VehDynCtrlStsForALgtCmft_UB:
        sig_name = "VehDynCtrlStsForALgtCmft_UB"
        sig_start_bit = 35
        update_id_bit = 35
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 35
        byte = 4
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class LimForJerkPosNotExcdCntr:
        sig_name = "LimForJerkPosNotExcdCntr"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class VehDynCtrlStsForALgtCmftVehDynCtrlStsCntr:
        sig_name = "VehDynCtrlStsForALgtCmftVehDynCtrlStsCntr"
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

    class HvActvForVehModReq:
        sig_name = "HvActvForVehModReq"
        sig_start_bit = 43
        update_id_bit = 42
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 43
        byte = 5
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VehDynCtrlStsForALgtCmftVehDynCtrlStsForBrkActv:
        sig_name = "VehDynCtrlStsForALgtCmftVehDynCtrlStsForBrkActv"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flg1_Rst': 0, 'Flg1_Set': 1}
        compute_method = None
        length = 1
        startbit = 39
        byte = 4
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VehDynCtrlStsForALgtCmftVehDynCtrlStsForWhlBrkWrm:
        sig_name = "VehDynCtrlStsForALgtCmftVehDynCtrlStsForWhlBrkWrm"
        sig_start_bit = 37
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flg1_Rst': 0, 'Flg1_Set': 1}
        compute_method = None
        length = 1
        startbit = 37
        byte = 4
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class LimForJerkPosNotExcdChks:
        sig_name = "LimForJerkPosNotExcdChks"
        sig_start_bit = 7
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
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehDynCtrlStsForALgtCmftVehDynCtrlStsNotEna:
        sig_name = "VehDynCtrlStsForALgtCmftVehDynCtrlStsNotEna"
        sig_start_bit = 36
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flg1_Rst': 0, 'Flg1_Set': 1}
        compute_method = None
        length = 1
        startbit = 36
        byte = 4
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class DrvrCrsCtrlFctDeactvnReq:
        sig_name = "DrvrCrsCtrlFctDeactvnReq"
        sig_start_bit = 34
        update_id_bit = 33
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 34
        byte = 4
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class LimForJerkPosNotExcd_UB:
        sig_name = "LimForJerkPosNotExcd_UB"
        sig_start_bit = 10
        update_id_bit = 10
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 10
        byte = 1
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class LimForJerkPosNotExcdLimForJerkPosNotExcd:
        sig_name = "LimForJerkPosNotExcdLimForJerkPosNotExcd"
        sig_start_bit = 11
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 11
        byte = 1
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VehDynCtrlStsForALgtCmftVehDynCtrlStsForBrkPrecActv:
        sig_name = "VehDynCtrlStsForALgtCmftVehDynCtrlStsForBrkPrecActv"
        sig_start_bit = 38
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flg1_Rst': 0, 'Flg1_Set': 1}
        compute_method = None
        length = 1
        startbit = 38
        byte = 4
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VehDynCtrlStsForALgtCmftVehDynCtrlStsForStandStillMgrForPark:
        sig_name = "VehDynCtrlStsForALgtCmftVehDynCtrlStsForStandStillMgrForPark"
        sig_start_bit = 26
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'StandStillMgrStsForPark2_ParkNotReqd': 0, 'StandStillMgrStsForPark2_ParkReqdByDrvr': 1, 'StandStillMgrStsForPark2_ParkReqdAutByHldTiExcd': 2, 'StandStillMgrStsForPark2_ParkReqdAut': 3, 'StandStillMgrStsForPark2_ParkNotAvl': 4}
        compute_method = None
        length = 3
        startbit = 26
        byte = 3
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class DrvrCrsCtrlFctReActvReq:
        sig_name = "DrvrCrsCtrlFctReActvReq"
        sig_start_bit = 47
        update_id_bit = 46
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 47
        byte = 5
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VehDynCtrlStsForALgtCmftVehDynCtrlStsDend:
        sig_name = "VehDynCtrlStsForALgtCmftVehDynCtrlStsDend"
        sig_start_bit = 27
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flg1_Rst': 0, 'Flg1_Set': 1}
        compute_method = None
        length = 1
        startbit = 27
        byte = 3
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3


class BbmVcuChas2Fr01:
    msg_name = "BbmVcuChas2Fr01"
    msg_id = 136
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "BBM"
    rx_nodes = ['ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class EpbActrStSec:
        sig_name = "EpbActrStSec"
        sig_start_bit = 58
        update_id_bit = 59
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 4
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AppRel_Applied': 0, 'AppRel_Released': 1, 'AppRel_Applying': 2, 'AppRel_Releasing': 3, 'AppRel_Unknown': 4, 'AppRel_HoldApplied': 5, 'AppRel_CompletelyReleased': 6, 'AppRel_HapPrepared': 7}
        compute_method = None
        length = 3
        startbit = 58
        byte = 7
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0


class VddmChas2Fr26:
    msg_name = "VddmChas2Fr26"
    msg_id = 624
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.07
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class WhlBrkOvrheatd:
        sig_name = "WhlBrkOvrheatd"
        sig_start_bit = 58
        update_id_bit = 57
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TSts1_Norm': 0, 'TSts1_Ovrheatd': 1}
        compute_method = None
        length = 1
        startbit = 58
        byte = 7
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class EscActvCtrlIndcdToDrvr:
        sig_name = "EscActvCtrlIndcdToDrvr"
        sig_start_bit = 62
        update_id_bit = 61
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 62
        byte = 7
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class MsgReqByHillDwnCtrl:
        sig_name = "MsgReqByHillDwnCtrl"
        sig_start_bit = 55
        update_id_bit = 52
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'MsgReqByHillDwnCtrl1_MsgForHillDwnCtrlNotReqd': 0, 'MsgReqByHillDwnCtrl1_MsgForHillDwnCtrlOnReqd': 1, 'MsgReqByHillDwnCtrl1_MsgForHillDwnCtrlReqdForBrkg': 2, 'MsgReqByHillDwnCtrl1_MsgForHillDwnCtrlTmpOffReqd': 3, 'MsgReqByHillDwnCtrl1_Resd4': 4, 'MsgReqByHillDwnCtrl1_Resd5': 5, 'MsgReqByHillDwnCtrl1_Resd6': 6, 'MsgReqByHillDwnCtrl1_Resd7': 7}
        compute_method = None
        length = 3
        startbit = 55
        byte = 6
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5


