class AcuADCANFDFr15:
    msg_name = "AcuADCANFDFr15"
    msg_id = 256
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "ACU"
    rx_nodes = ['BGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class UsgModChgReqFromACU:
        sig_name = "UsgModChgReqFromACU"
        sig_start_bit = 7
        update_id_bit = 0
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 13
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'UsgModSts1_UsgModAbdnd': 0, 'UsgModSts1_UsgModInActv': 1, 'UsgModSts1_UsgModCnvinc': 2, 'UsgModSts1_UsgModActv': 11, 'UsgModSts1_UsgModDrvg': 13}
        compute_method = None
        length = 4
        startbit = 7
        byte = 0
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4


class BgmADCANFDFr19:
    msg_name = "BgmADCANFDFr19"
    msg_id = 510
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "BGM"
    rx_nodes = ['ACU']
    sig_group_dict = {'RearLeftRdrObj6': ['RearLeftRdrObj6ObjBoxCenterLat', 'RearLeftRdrObj6ObjBoxCenterLgt', 'RearLeftRdrObj6RdrObjChks', 'RearLeftRdrObj6RdrObjCntr', 'RearLeftRdrObj6RdrObjDx', 'RearLeftRdrObj6RdrObjDxStdDe', 'RearLeftRdrObj6RdrObjDy', 'RearLeftRdrObj6RdrObjDynProp', 'RearLeftRdrObj6RdrObjDyStdDe', 'RearLeftRdrObj6RdrObjExistProb', 'RearLeftRdrObj6RdrObjHeight', 'RearLeftRdrObj6RdrObjHeightStdDe', 'RearLeftRdrObj6RdrObjID', 'RearLeftRdrObj6RdrObjLifeCycle', 'RearLeftRdrObj6RdrObjPwr', 'RearLeftRdrObj6RdrObjVx', 'RearLeftRdrObj6RdrObjVxStdDe', 'RearLeftRdrObj6RdrObjVy', 'RearLeftRdrObj6RdrObjVyStdDe'], 'RearLeftRdrObj4': ['RearLeftRdrObj4ObjBoxCenterLat', 'RearLeftRdrObj4ObjBoxCenterLgt', 'RearLeftRdrObj4RdrObjChks', 'RearLeftRdrObj4RdrObjCntr', 'RearLeftRdrObj4RdrObjDx', 'RearLeftRdrObj4RdrObjDxStdDe', 'RearLeftRdrObj4RdrObjDy', 'RearLeftRdrObj4RdrObjDynProp', 'RearLeftRdrObj4RdrObjDyStdDe', 'RearLeftRdrObj4RdrObjExistProb', 'RearLeftRdrObj4RdrObjHeight', 'RearLeftRdrObj4RdrObjHeightStdDe', 'RearLeftRdrObj4RdrObjID', 'RearLeftRdrObj4RdrObjLifeCycle', 'RearLeftRdrObj4RdrObjPwr', 'RearLeftRdrObj4RdrObjVx', 'RearLeftRdrObj4RdrObjVxStdDe', 'RearLeftRdrObj4RdrObjVy', 'RearLeftRdrObj4RdrObjVyStdDe'], 'RearLeftRdrObj5': ['RearLeftRdrObj5ObjBoxCenterLat', 'RearLeftRdrObj5ObjBoxCenterLgt', 'RearLeftRdrObj5RdrObjChks', 'RearLeftRdrObj5RdrObjCntr', 'RearLeftRdrObj5RdrObjDx', 'RearLeftRdrObj5RdrObjDxStdDe', 'RearLeftRdrObj5RdrObjDy', 'RearLeftRdrObj5RdrObjDynProp', 'RearLeftRdrObj5RdrObjDyStdDe', 'RearLeftRdrObj5RdrObjExistProb', 'RearLeftRdrObj5RdrObjHeight', 'RearLeftRdrObj5RdrObjHeightStdDe', 'RearLeftRdrObj5RdrObjID', 'RearLeftRdrObj5RdrObjLifeCycle', 'RearLeftRdrObj5RdrObjPwr', 'RearLeftRdrObj5RdrObjVx', 'RearLeftRdrObj5RdrObjVxStdDe', 'RearLeftRdrObj5RdrObjVy', 'RearLeftRdrObj5RdrObjVyStdDe']}
    sig_group_dataid_dict = {}

    class RearLeftRdrObj5RdrObjExistProb:
        sig_name = "RearLeftRdrObj5RdrObjExistProb"
        sig_start_bit = 252
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 252
        bmuws_info = [(31, 0b00011111, 0b11100000, 5, 0), (32, 0b11111000, 0b00000111, 5, 3)]

    class RearLeftRdrObj4RdrObjVy:
        sig_name = "RearLeftRdrObj4RdrObjVy"
        sig_start_bit = 148
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 148
        bmuws_info = [(18, 0b00011111, 0b11100000, 5, 0), (19, 0b11111100, 0b00000011, 6, 2)]

    class RearLeftRdrObj4RdrObjHeight:
        sig_name = "RearLeftRdrObj4RdrObjHeight"
        sig_start_bit = 82
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 82
        bmuws_info = [(10, 0b00000111, 0b11111000, 3, 0), (11, 0b11111110, 0b00000001, 7, 1)]

    class RearLeftRdrObj5RdrObjHeightStdDe:
        sig_name = "RearLeftRdrObj5RdrObjHeightStdDe"
        sig_start_bit = 264
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 264
        bmuws_info = [(33, 0b00000001, 0b11111110, 1, 0), (34, 0b11111111, 0b00000000, 8, 0), (35, 0b10000000, 0b01111111, 1, 7)]

    class RearLeftRdrObj6ObjBoxCenterLgt:
        sig_name = "RearLeftRdrObj6ObjBoxCenterLgt"
        sig_start_bit = 375
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 375
        byte = 46
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearLeftRdrObj6RdrObjVy:
        sig_name = "RearLeftRdrObj6RdrObjVy"
        sig_start_bit = 492
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 492
        bmuws_info = [(61, 0b00011111, 0b11100000, 5, 0), (62, 0b11111100, 0b00000011, 6, 2)]

    class RearLeftRdrObj4RdrObjDyStdDe:
        sig_name = "RearLeftRdrObj4RdrObjDyStdDe"
        sig_start_bit = 71
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 71
        bmuws_info = [(8, 0b11111111, 0b00000000, 8, 0), (9, 0b11100000, 0b00011111, 3, 5)]

    class RearLeftRdrObj6RdrObjPwr:
        sig_name = "RearLeftRdrObj6RdrObjPwr"
        sig_start_bit = 457
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 457
        bmuws_info = [(57, 0b00000011, 0b11111100, 2, 0), (58, 0b11111100, 0b00000011, 6, 2)]

    class RearLeftRdrObj6_UB:
        sig_name = "RearLeftRdrObj6_UB"
        sig_start_bit = 171
        update_id_bit = 171
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
        startbit = 171
        byte = 21
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class RearLeftRdrObj6RdrObjHeightStdDe:
        sig_name = "RearLeftRdrObj6RdrObjHeightStdDe"
        sig_start_bit = 432
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 432
        bmuws_info = [(54, 0b00000001, 0b11111110, 1, 0), (55, 0b11111111, 0b00000000, 8, 0), (56, 0b10000000, 0b01111111, 1, 7)]

    class RearLeftRdrObj4RdrObjCntr:
        sig_name = "RearLeftRdrObj4RdrObjCntr"
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

    class RearLeftRdrObj5ObjBoxCenterLat:
        sig_name = "RearLeftRdrObj5ObjBoxCenterLat"
        sig_start_bit = 215
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 215
        byte = 26
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearLeftRdrObj5RdrObjDy:
        sig_name = "RearLeftRdrObj5RdrObjDy"
        sig_start_bit = 227
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 227
        bmuws_info = [(28, 0b00001111, 0b11110000, 4, 0), (29, 0b11111111, 0b00000000, 8, 0)]

    class RearLeftRdrObj6RdrObjVxStdDe:
        sig_name = "RearLeftRdrObj6RdrObjVxStdDe"
        sig_start_bit = 486
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 486
        bmuws_info = [(60, 0b01111111, 0b10000000, 7, 0), (61, 0b11100000, 0b00011111, 3, 5)]

    class RearLeftRdrObj4RdrObjDx:
        sig_name = "RearLeftRdrObj4RdrObjDx"
        sig_start_bit = 11
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 11
        bmuws_info = [(1, 0b00001111, 0b11110000, 4, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class RearLeftRdrObj4RdrObjDy:
        sig_name = "RearLeftRdrObj4RdrObjDy"
        sig_start_bit = 51
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 51
        bmuws_info = [(6, 0b00001111, 0b11110000, 4, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class RearLeftRdrObj5RdrObjDxStdDe:
        sig_name = "RearLeftRdrObj5RdrObjDxStdDe"
        sig_start_bit = 223
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 223
        bmuws_info = [(27, 0b11111111, 0b00000000, 8, 0), (28, 0b11100000, 0b00011111, 3, 5)]

    class RearLeftRdrObj6RdrObjDyStdDe:
        sig_name = "RearLeftRdrObj6RdrObjDyStdDe"
        sig_start_bit = 415
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 415
        bmuws_info = [(51, 0b11111111, 0b00000000, 8, 0), (52, 0b11100000, 0b00011111, 3, 5)]

    class RearLeftRdrObj4ObjBoxCenterLgt:
        sig_name = "RearLeftRdrObj4ObjBoxCenterLgt"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
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

    class RearLeftRdrObj5RdrObjVy:
        sig_name = "RearLeftRdrObj5RdrObjVy"
        sig_start_bit = 324
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 324
        bmuws_info = [(40, 0b00011111, 0b11100000, 5, 0), (41, 0b11111100, 0b00000011, 6, 2)]

    class RearLeftRdrObj4RdrObjDxStdDe:
        sig_name = "RearLeftRdrObj4RdrObjDxStdDe"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11100000, 0b00011111, 3, 5)]

    class RearLeftRdrObj4RdrObjVx:
        sig_name = "RearLeftRdrObj4RdrObjVx"
        sig_start_bit = 121
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 121
        bmuws_info = [(15, 0b00000011, 0b11111100, 2, 0), (16, 0b11111111, 0b00000000, 8, 0), (17, 0b10000000, 0b01111111, 1, 7)]

    class RearLeftRdrObj5RdrObjVyStdDe:
        sig_name = "RearLeftRdrObj5RdrObjVyStdDe"
        sig_start_bit = 329
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 329
        bmuws_info = [(41, 0b00000011, 0b11111100, 2, 0), (42, 0b11111111, 0b00000000, 8, 0)]

    class RearLeftRdrObj4RdrObjLifeCycle:
        sig_name = "RearLeftRdrObj4RdrObjLifeCycle"
        sig_start_bit = 104
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
        startbit = 104
        bmuws_info = [(13, 0b00000001, 0b11111110, 1, 0), (14, 0b11111100, 0b00000011, 6, 2)]

    class RearLeftRdrObj6RdrObjHeight:
        sig_name = "RearLeftRdrObj6RdrObjHeight"
        sig_start_bit = 426
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 426
        bmuws_info = [(53, 0b00000111, 0b11111000, 3, 0), (54, 0b11111110, 0b00000001, 7, 1)]

    class RearLeftRdrObj4RdrObjVyStdDe:
        sig_name = "RearLeftRdrObj4RdrObjVyStdDe"
        sig_start_bit = 153
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 153
        bmuws_info = [(19, 0b00000011, 0b11111100, 2, 0), (20, 0b11111111, 0b00000000, 8, 0)]

    class RearLeftRdrObj4RdrObjVxStdDe:
        sig_name = "RearLeftRdrObj4RdrObjVxStdDe"
        sig_start_bit = 142
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 142
        bmuws_info = [(17, 0b01111111, 0b10000000, 7, 0), (18, 0b11100000, 0b00011111, 3, 5)]

    class RearLeftRdrObj5RdrObjChks:
        sig_name = "RearLeftRdrObj5RdrObjChks"
        sig_start_bit = 183
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
        startbit = 183
        byte = 22
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearLeftRdrObj4_UB:
        sig_name = "RearLeftRdrObj4_UB"
        sig_start_bit = 175
        update_id_bit = 175
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
        startbit = 175
        byte = 21
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class RearLeftRdrObj6RdrObjLifeCycle:
        sig_name = "RearLeftRdrObj6RdrObjLifeCycle"
        sig_start_bit = 448
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
        startbit = 448
        bmuws_info = [(56, 0b00000001, 0b11111110, 1, 0), (57, 0b11111100, 0b00000011, 6, 2)]

    class RearLeftRdrObj6ObjBoxCenterLat:
        sig_name = "RearLeftRdrObj6ObjBoxCenterLat"
        sig_start_bit = 383
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 383
        byte = 47
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearLeftRdrObj5RdrObjLifeCycle:
        sig_name = "RearLeftRdrObj5RdrObjLifeCycle"
        sig_start_bit = 280
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
        startbit = 280
        bmuws_info = [(35, 0b00000001, 0b11111110, 1, 0), (36, 0b11111100, 0b00000011, 6, 2)]

    class RearLeftRdrObj6RdrObjCntr:
        sig_name = "RearLeftRdrObj6RdrObjCntr"
        sig_start_bit = 359
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
        startbit = 359
        byte = 44
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class RearLeftRdrObj5RdrObjCntr:
        sig_name = "RearLeftRdrObj5RdrObjCntr"
        sig_start_bit = 191
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
        startbit = 191
        byte = 23
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class RearLeftRdrObj4RdrObjDynProp:
        sig_name = "RearLeftRdrObj4RdrObjDynProp"
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
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class RearLeftRdrObj5RdrObjVx:
        sig_name = "RearLeftRdrObj5RdrObjVx"
        sig_start_bit = 297
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 297
        bmuws_info = [(37, 0b00000011, 0b11111100, 2, 0), (38, 0b11111111, 0b00000000, 8, 0), (39, 0b10000000, 0b01111111, 1, 7)]

    class RearLeftRdrObj4RdrObjID:
        sig_name = "RearLeftRdrObj4RdrObjID"
        sig_start_bit = 110
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 110
        byte = 13
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class RearLeftRdrObj6RdrObjVyStdDe:
        sig_name = "RearLeftRdrObj6RdrObjVyStdDe"
        sig_start_bit = 497
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 497
        bmuws_info = [(62, 0b00000011, 0b11111100, 2, 0), (63, 0b11111111, 0b00000000, 8, 0)]

    class RearLeftRdrObj5ObjBoxCenterLgt:
        sig_name = "RearLeftRdrObj5ObjBoxCenterLgt"
        sig_start_bit = 207
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 207
        byte = 25
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearLeftRdrObj4ObjBoxCenterLat:
        sig_name = "RearLeftRdrObj4ObjBoxCenterLat"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
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

    class RearLeftRdrObj6RdrObjDx:
        sig_name = "RearLeftRdrObj6RdrObjDx"
        sig_start_bit = 355
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 355
        bmuws_info = [(44, 0b00001111, 0b11110000, 4, 0), (45, 0b11111111, 0b00000000, 8, 0)]

    class RearLeftRdrObj5RdrObjID:
        sig_name = "RearLeftRdrObj5RdrObjID"
        sig_start_bit = 286
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 286
        byte = 35
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class RearLeftRdrObj5RdrObjPwr:
        sig_name = "RearLeftRdrObj5RdrObjPwr"
        sig_start_bit = 289
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 289
        bmuws_info = [(36, 0b00000011, 0b11111100, 2, 0), (37, 0b11111100, 0b00000011, 6, 2)]

    class RearLeftRdrObj5RdrObjDx:
        sig_name = "RearLeftRdrObj5RdrObjDx"
        sig_start_bit = 187
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 187
        bmuws_info = [(23, 0b00001111, 0b11110000, 4, 0), (24, 0b11111111, 0b00000000, 8, 0)]

    class RearLeftRdrObj5RdrObjVxStdDe:
        sig_name = "RearLeftRdrObj5RdrObjVxStdDe"
        sig_start_bit = 318
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 318
        bmuws_info = [(39, 0b01111111, 0b10000000, 7, 0), (40, 0b11100000, 0b00011111, 3, 5)]

    class RearLeftRdrObj5_UB:
        sig_name = "RearLeftRdrObj5_UB"
        sig_start_bit = 168
        update_id_bit = 168
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
        startbit = 168
        byte = 21
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class RearLeftRdrObj6RdrObjChks:
        sig_name = "RearLeftRdrObj6RdrObjChks"
        sig_start_bit = 351
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
        startbit = 351
        byte = 43
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearLeftRdrObj4RdrObjChks:
        sig_name = "RearLeftRdrObj4RdrObjChks"
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

    class RearLeftRdrObj6RdrObjDxStdDe:
        sig_name = "RearLeftRdrObj6RdrObjDxStdDe"
        sig_start_bit = 391
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 391
        bmuws_info = [(48, 0b11111111, 0b00000000, 8, 0), (49, 0b11100000, 0b00011111, 3, 5)]

    class RearLeftRdrObj4RdrObjPwr:
        sig_name = "RearLeftRdrObj4RdrObjPwr"
        sig_start_bit = 113
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 113
        bmuws_info = [(14, 0b00000011, 0b11111100, 2, 0), (15, 0b11111100, 0b00000011, 6, 2)]

    class RearLeftRdrObj6RdrObjDynProp:
        sig_name = "RearLeftRdrObj6RdrObjDynProp"
        sig_start_bit = 396
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 396
        byte = 49
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class RearLeftRdrObj4RdrObjExistProb:
        sig_name = "RearLeftRdrObj4RdrObjExistProb"
        sig_start_bit = 76
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 76
        bmuws_info = [(9, 0b00011111, 0b11100000, 5, 0), (10, 0b11111000, 0b00000111, 5, 3)]

    class RearLeftRdrObj5RdrObjDynProp:
        sig_name = "RearLeftRdrObj5RdrObjDynProp"
        sig_start_bit = 228
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 228
        byte = 28
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class RearLeftRdrObj4RdrObjHeightStdDe:
        sig_name = "RearLeftRdrObj4RdrObjHeightStdDe"
        sig_start_bit = 88
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 88
        bmuws_info = [(11, 0b00000001, 0b11111110, 1, 0), (12, 0b11111111, 0b00000000, 8, 0), (13, 0b10000000, 0b01111111, 1, 7)]

    class RearLeftRdrObj6RdrObjExistProb:
        sig_name = "RearLeftRdrObj6RdrObjExistProb"
        sig_start_bit = 420
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 420
        bmuws_info = [(52, 0b00011111, 0b11100000, 5, 0), (53, 0b11111000, 0b00000111, 5, 3)]

    class RearLeftRdrObj6RdrObjID:
        sig_name = "RearLeftRdrObj6RdrObjID"
        sig_start_bit = 454
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 454
        byte = 56
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class RearLeftRdrObj6RdrObjVx:
        sig_name = "RearLeftRdrObj6RdrObjVx"
        sig_start_bit = 465
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 465
        bmuws_info = [(58, 0b00000011, 0b11111100, 2, 0), (59, 0b11111111, 0b00000000, 8, 0), (60, 0b10000000, 0b01111111, 1, 7)]

    class RearLeftRdrObj5RdrObjHeight:
        sig_name = "RearLeftRdrObj5RdrObjHeight"
        sig_start_bit = 258
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 258
        bmuws_info = [(32, 0b00000111, 0b11111000, 3, 0), (33, 0b11111110, 0b00000001, 7, 1)]

    class RearLeftRdrObj5RdrObjDyStdDe:
        sig_name = "RearLeftRdrObj5RdrObjDyStdDe"
        sig_start_bit = 247
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 247
        bmuws_info = [(30, 0b11111111, 0b00000000, 8, 0), (31, 0b11100000, 0b00011111, 3, 5)]

    class RearLeftRdrObj6RdrObjDy:
        sig_name = "RearLeftRdrObj6RdrObjDy"
        sig_start_bit = 395
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 395
        bmuws_info = [(49, 0b00001111, 0b11110000, 4, 0), (50, 0b11111111, 0b00000000, 8, 0)]


class AcuADCANFDTimeSynchFr:
    msg_name = "AcuADCANFDTimeSynchFr"
    msg_id = 33
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "ACU"
    rx_nodes = ['BGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class BgmADCANFDFr26:
    msg_name = "BgmADCANFDFr26"
    msg_id = 518
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "BGM"
    rx_nodes = ['ACU']
    sig_group_dict = {'RearRgtRdrObj7': ['RearRgtRdrObj7ObjBoxCenterLat', 'RearRgtRdrObj7ObjBoxCenterLgt', 'RearRgtRdrObj7RdrObjChks', 'RearRgtRdrObj7RdrObjCntr', 'RearRgtRdrObj7RdrObjDx', 'RearRgtRdrObj7RdrObjDxStdDe', 'RearRgtRdrObj7RdrObjDy', 'RearRgtRdrObj7RdrObjDynProp', 'RearRgtRdrObj7RdrObjDyStdDe', 'RearRgtRdrObj7RdrObjExistProb', 'RearRgtRdrObj7RdrObjHeight', 'RearRgtRdrObj7RdrObjHeightStdDe', 'RearRgtRdrObj7RdrObjID', 'RearRgtRdrObj7RdrObjLifeCycle', 'RearRgtRdrObj7RdrObjPwr', 'RearRgtRdrObj7RdrObjVx', 'RearRgtRdrObj7RdrObjVxStdDe', 'RearRgtRdrObj7RdrObjVy', 'RearRgtRdrObj7RdrObjVyStdDe'], 'RearRgtRdrObj9': ['RearRgtRdrObj9ObjBoxCenterLat', 'RearRgtRdrObj9ObjBoxCenterLgt', 'RearRgtRdrObj9RdrObjChks', 'RearRgtRdrObj9RdrObjCntr', 'RearRgtRdrObj9RdrObjDx', 'RearRgtRdrObj9RdrObjDxStdDe', 'RearRgtRdrObj9RdrObjDy', 'RearRgtRdrObj9RdrObjDynProp', 'RearRgtRdrObj9RdrObjDyStdDe', 'RearRgtRdrObj9RdrObjExistProb', 'RearRgtRdrObj9RdrObjHeight', 'RearRgtRdrObj9RdrObjHeightStdDe', 'RearRgtRdrObj9RdrObjID', 'RearRgtRdrObj9RdrObjLifeCycle', 'RearRgtRdrObj9RdrObjPwr', 'RearRgtRdrObj9RdrObjVx', 'RearRgtRdrObj9RdrObjVxStdDe', 'RearRgtRdrObj9RdrObjVy', 'RearRgtRdrObj9RdrObjVyStdDe'], 'RearRgtRdrObj8': ['RearRgtRdrObj8ObjBoxCenterLat', 'RearRgtRdrObj8ObjBoxCenterLgt', 'RearRgtRdrObj8RdrObjChks', 'RearRgtRdrObj8RdrObjCntr', 'RearRgtRdrObj8RdrObjDx', 'RearRgtRdrObj8RdrObjDxStdDe', 'RearRgtRdrObj8RdrObjDy', 'RearRgtRdrObj8RdrObjDynProp', 'RearRgtRdrObj8RdrObjDyStdDe', 'RearRgtRdrObj8RdrObjExistProb', 'RearRgtRdrObj8RdrObjHeight', 'RearRgtRdrObj8RdrObjHeightStdDe', 'RearRgtRdrObj8RdrObjID', 'RearRgtRdrObj8RdrObjLifeCycle', 'RearRgtRdrObj8RdrObjPwr', 'RearRgtRdrObj8RdrObjVx', 'RearRgtRdrObj8RdrObjVxStdDe', 'RearRgtRdrObj8RdrObjVy', 'RearRgtRdrObj8RdrObjVyStdDe']}
    sig_group_dataid_dict = {}

    class RearRgtRdrObj7RdrObjID:
        sig_name = "RearRgtRdrObj7RdrObjID"
        sig_start_bit = 110
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 110
        byte = 13
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class RearRgtRdrObj9RdrObjVyStdDe:
        sig_name = "RearRgtRdrObj9RdrObjVyStdDe"
        sig_start_bit = 497
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 497
        bmuws_info = [(62, 0b00000011, 0b11111100, 2, 0), (63, 0b11111111, 0b00000000, 8, 0)]

    class RearRgtRdrObj8RdrObjDy:
        sig_name = "RearRgtRdrObj8RdrObjDy"
        sig_start_bit = 227
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 227
        bmuws_info = [(28, 0b00001111, 0b11110000, 4, 0), (29, 0b11111111, 0b00000000, 8, 0)]

    class RearRgtRdrObj7_UB:
        sig_name = "RearRgtRdrObj7_UB"
        sig_start_bit = 175
        update_id_bit = 175
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
        startbit = 175
        byte = 21
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class RearRgtRdrObj8RdrObjDyStdDe:
        sig_name = "RearRgtRdrObj8RdrObjDyStdDe"
        sig_start_bit = 247
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 247
        bmuws_info = [(30, 0b11111111, 0b00000000, 8, 0), (31, 0b11100000, 0b00011111, 3, 5)]

    class RearRgtRdrObj8RdrObjVx:
        sig_name = "RearRgtRdrObj8RdrObjVx"
        sig_start_bit = 297
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 297
        bmuws_info = [(37, 0b00000011, 0b11111100, 2, 0), (38, 0b11111111, 0b00000000, 8, 0), (39, 0b10000000, 0b01111111, 1, 7)]

    class RearRgtRdrObj9RdrObjDynProp:
        sig_name = "RearRgtRdrObj9RdrObjDynProp"
        sig_start_bit = 396
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 396
        byte = 49
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class RearRgtRdrObj9RdrObjDxStdDe:
        sig_name = "RearRgtRdrObj9RdrObjDxStdDe"
        sig_start_bit = 391
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 391
        bmuws_info = [(48, 0b11111111, 0b00000000, 8, 0), (49, 0b11100000, 0b00011111, 3, 5)]

    class RearRgtRdrObj7RdrObjCntr:
        sig_name = "RearRgtRdrObj7RdrObjCntr"
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

    class RearRgtRdrObj7ObjBoxCenterLgt:
        sig_name = "RearRgtRdrObj7ObjBoxCenterLgt"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
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

    class RearRgtRdrObj9RdrObjHeightStdDe:
        sig_name = "RearRgtRdrObj9RdrObjHeightStdDe"
        sig_start_bit = 432
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 432
        bmuws_info = [(54, 0b00000001, 0b11111110, 1, 0), (55, 0b11111111, 0b00000000, 8, 0), (56, 0b10000000, 0b01111111, 1, 7)]

    class RearRgtRdrObj9RdrObjChks:
        sig_name = "RearRgtRdrObj9RdrObjChks"
        sig_start_bit = 351
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
        startbit = 351
        byte = 43
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearRgtRdrObj7ObjBoxCenterLat:
        sig_name = "RearRgtRdrObj7ObjBoxCenterLat"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
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

    class RearRgtRdrObj7RdrObjDxStdDe:
        sig_name = "RearRgtRdrObj7RdrObjDxStdDe"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11100000, 0b00011111, 3, 5)]

    class RearRgtRdrObj8RdrObjDxStdDe:
        sig_name = "RearRgtRdrObj8RdrObjDxStdDe"
        sig_start_bit = 223
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 223
        bmuws_info = [(27, 0b11111111, 0b00000000, 8, 0), (28, 0b11100000, 0b00011111, 3, 5)]

    class RearRgtRdrObj7RdrObjHeight:
        sig_name = "RearRgtRdrObj7RdrObjHeight"
        sig_start_bit = 82
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 82
        bmuws_info = [(10, 0b00000111, 0b11111000, 3, 0), (11, 0b11111110, 0b00000001, 7, 1)]

    class RearRgtRdrObj8RdrObjVy:
        sig_name = "RearRgtRdrObj8RdrObjVy"
        sig_start_bit = 324
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 324
        bmuws_info = [(40, 0b00011111, 0b11100000, 5, 0), (41, 0b11111100, 0b00000011, 6, 2)]

    class RearRgtRdrObj8RdrObjDx:
        sig_name = "RearRgtRdrObj8RdrObjDx"
        sig_start_bit = 187
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 187
        bmuws_info = [(23, 0b00001111, 0b11110000, 4, 0), (24, 0b11111111, 0b00000000, 8, 0)]

    class RearRgtRdrObj8RdrObjID:
        sig_name = "RearRgtRdrObj8RdrObjID"
        sig_start_bit = 286
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 286
        byte = 35
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class RearRgtRdrObj7RdrObjDx:
        sig_name = "RearRgtRdrObj7RdrObjDx"
        sig_start_bit = 11
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 11
        bmuws_info = [(1, 0b00001111, 0b11110000, 4, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class RearRgtRdrObj7RdrObjHeightStdDe:
        sig_name = "RearRgtRdrObj7RdrObjHeightStdDe"
        sig_start_bit = 88
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 88
        bmuws_info = [(11, 0b00000001, 0b11111110, 1, 0), (12, 0b11111111, 0b00000000, 8, 0), (13, 0b10000000, 0b01111111, 1, 7)]

    class RearRgtRdrObj8RdrObjVyStdDe:
        sig_name = "RearRgtRdrObj8RdrObjVyStdDe"
        sig_start_bit = 329
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 329
        bmuws_info = [(41, 0b00000011, 0b11111100, 2, 0), (42, 0b11111111, 0b00000000, 8, 0)]

    class RearRgtRdrObj8RdrObjPwr:
        sig_name = "RearRgtRdrObj8RdrObjPwr"
        sig_start_bit = 289
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 289
        bmuws_info = [(36, 0b00000011, 0b11111100, 2, 0), (37, 0b11111100, 0b00000011, 6, 2)]

    class RearRgtRdrObj8RdrObjLifeCycle:
        sig_name = "RearRgtRdrObj8RdrObjLifeCycle"
        sig_start_bit = 280
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
        startbit = 280
        bmuws_info = [(35, 0b00000001, 0b11111110, 1, 0), (36, 0b11111100, 0b00000011, 6, 2)]

    class RearRgtRdrObj7RdrObjLifeCycle:
        sig_name = "RearRgtRdrObj7RdrObjLifeCycle"
        sig_start_bit = 104
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
        startbit = 104
        bmuws_info = [(13, 0b00000001, 0b11111110, 1, 0), (14, 0b11111100, 0b00000011, 6, 2)]

    class RearRgtRdrObj9RdrObjPwr:
        sig_name = "RearRgtRdrObj9RdrObjPwr"
        sig_start_bit = 457
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 457
        bmuws_info = [(57, 0b00000011, 0b11111100, 2, 0), (58, 0b11111100, 0b00000011, 6, 2)]

    class RearRgtRdrObj9RdrObjVx:
        sig_name = "RearRgtRdrObj9RdrObjVx"
        sig_start_bit = 465
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 465
        bmuws_info = [(58, 0b00000011, 0b11111100, 2, 0), (59, 0b11111111, 0b00000000, 8, 0), (60, 0b10000000, 0b01111111, 1, 7)]

    class RearRgtRdrObj8RdrObjDynProp:
        sig_name = "RearRgtRdrObj8RdrObjDynProp"
        sig_start_bit = 228
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 228
        byte = 28
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class RearRgtRdrObj9_UB:
        sig_name = "RearRgtRdrObj9_UB"
        sig_start_bit = 171
        update_id_bit = 171
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
        startbit = 171
        byte = 21
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class RearRgtRdrObj8_UB:
        sig_name = "RearRgtRdrObj8_UB"
        sig_start_bit = 168
        update_id_bit = 168
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
        startbit = 168
        byte = 21
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class RearRgtRdrObj8RdrObjVxStdDe:
        sig_name = "RearRgtRdrObj8RdrObjVxStdDe"
        sig_start_bit = 318
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 318
        bmuws_info = [(39, 0b01111111, 0b10000000, 7, 0), (40, 0b11100000, 0b00011111, 3, 5)]

    class RearRgtRdrObj9RdrObjDy:
        sig_name = "RearRgtRdrObj9RdrObjDy"
        sig_start_bit = 395
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 395
        bmuws_info = [(49, 0b00001111, 0b11110000, 4, 0), (50, 0b11111111, 0b00000000, 8, 0)]

    class RearRgtRdrObj9RdrObjDyStdDe:
        sig_name = "RearRgtRdrObj9RdrObjDyStdDe"
        sig_start_bit = 415
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 415
        bmuws_info = [(51, 0b11111111, 0b00000000, 8, 0), (52, 0b11100000, 0b00011111, 3, 5)]

    class RearRgtRdrObj7RdrObjDyStdDe:
        sig_name = "RearRgtRdrObj7RdrObjDyStdDe"
        sig_start_bit = 71
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 71
        bmuws_info = [(8, 0b11111111, 0b00000000, 8, 0), (9, 0b11100000, 0b00011111, 3, 5)]

    class RearRgtRdrObj7RdrObjVx:
        sig_name = "RearRgtRdrObj7RdrObjVx"
        sig_start_bit = 121
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 121
        bmuws_info = [(15, 0b00000011, 0b11111100, 2, 0), (16, 0b11111111, 0b00000000, 8, 0), (17, 0b10000000, 0b01111111, 1, 7)]

    class RearRgtRdrObj9ObjBoxCenterLgt:
        sig_name = "RearRgtRdrObj9ObjBoxCenterLgt"
        sig_start_bit = 375
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 375
        byte = 46
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearRgtRdrObj9RdrObjVy:
        sig_name = "RearRgtRdrObj9RdrObjVy"
        sig_start_bit = 492
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 492
        bmuws_info = [(61, 0b00011111, 0b11100000, 5, 0), (62, 0b11111100, 0b00000011, 6, 2)]

    class RearRgtRdrObj7RdrObjVyStdDe:
        sig_name = "RearRgtRdrObj7RdrObjVyStdDe"
        sig_start_bit = 153
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 153
        bmuws_info = [(19, 0b00000011, 0b11111100, 2, 0), (20, 0b11111111, 0b00000000, 8, 0)]

    class RearRgtRdrObj7RdrObjDynProp:
        sig_name = "RearRgtRdrObj7RdrObjDynProp"
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
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class RearRgtRdrObj9ObjBoxCenterLat:
        sig_name = "RearRgtRdrObj9ObjBoxCenterLat"
        sig_start_bit = 383
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 383
        byte = 47
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearRgtRdrObj9RdrObjLifeCycle:
        sig_name = "RearRgtRdrObj9RdrObjLifeCycle"
        sig_start_bit = 448
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
        startbit = 448
        bmuws_info = [(56, 0b00000001, 0b11111110, 1, 0), (57, 0b11111100, 0b00000011, 6, 2)]

    class RearRgtRdrObj7RdrObjExistProb:
        sig_name = "RearRgtRdrObj7RdrObjExistProb"
        sig_start_bit = 76
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 76
        bmuws_info = [(9, 0b00011111, 0b11100000, 5, 0), (10, 0b11111000, 0b00000111, 5, 3)]

    class RearRgtRdrObj8RdrObjCntr:
        sig_name = "RearRgtRdrObj8RdrObjCntr"
        sig_start_bit = 191
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
        startbit = 191
        byte = 23
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class RearRgtRdrObj8RdrObjHeightStdDe:
        sig_name = "RearRgtRdrObj8RdrObjHeightStdDe"
        sig_start_bit = 264
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 264
        bmuws_info = [(33, 0b00000001, 0b11111110, 1, 0), (34, 0b11111111, 0b00000000, 8, 0), (35, 0b10000000, 0b01111111, 1, 7)]

    class RearRgtRdrObj8ObjBoxCenterLgt:
        sig_name = "RearRgtRdrObj8ObjBoxCenterLgt"
        sig_start_bit = 207
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 207
        byte = 25
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearRgtRdrObj7RdrObjVy:
        sig_name = "RearRgtRdrObj7RdrObjVy"
        sig_start_bit = 148
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 148
        bmuws_info = [(18, 0b00011111, 0b11100000, 5, 0), (19, 0b11111100, 0b00000011, 6, 2)]

    class RearRgtRdrObj8RdrObjChks:
        sig_name = "RearRgtRdrObj8RdrObjChks"
        sig_start_bit = 183
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
        startbit = 183
        byte = 22
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearRgtRdrObj9RdrObjExistProb:
        sig_name = "RearRgtRdrObj9RdrObjExistProb"
        sig_start_bit = 420
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 420
        bmuws_info = [(52, 0b00011111, 0b11100000, 5, 0), (53, 0b11111000, 0b00000111, 5, 3)]

    class RearRgtRdrObj7RdrObjVxStdDe:
        sig_name = "RearRgtRdrObj7RdrObjVxStdDe"
        sig_start_bit = 142
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 142
        bmuws_info = [(17, 0b01111111, 0b10000000, 7, 0), (18, 0b11100000, 0b00011111, 3, 5)]

    class RearRgtRdrObj7RdrObjDy:
        sig_name = "RearRgtRdrObj7RdrObjDy"
        sig_start_bit = 51
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 51
        bmuws_info = [(6, 0b00001111, 0b11110000, 4, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class RearRgtRdrObj9RdrObjHeight:
        sig_name = "RearRgtRdrObj9RdrObjHeight"
        sig_start_bit = 426
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 426
        bmuws_info = [(53, 0b00000111, 0b11111000, 3, 0), (54, 0b11111110, 0b00000001, 7, 1)]

    class RearRgtRdrObj8RdrObjHeight:
        sig_name = "RearRgtRdrObj8RdrObjHeight"
        sig_start_bit = 258
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 258
        bmuws_info = [(32, 0b00000111, 0b11111000, 3, 0), (33, 0b11111110, 0b00000001, 7, 1)]

    class RearRgtRdrObj9RdrObjVxStdDe:
        sig_name = "RearRgtRdrObj9RdrObjVxStdDe"
        sig_start_bit = 486
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 486
        bmuws_info = [(60, 0b01111111, 0b10000000, 7, 0), (61, 0b11100000, 0b00011111, 3, 5)]

    class RearRgtRdrObj7RdrObjPwr:
        sig_name = "RearRgtRdrObj7RdrObjPwr"
        sig_start_bit = 113
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 113
        bmuws_info = [(14, 0b00000011, 0b11111100, 2, 0), (15, 0b11111100, 0b00000011, 6, 2)]

    class RearRgtRdrObj7RdrObjChks:
        sig_name = "RearRgtRdrObj7RdrObjChks"
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

    class RearRgtRdrObj9RdrObjCntr:
        sig_name = "RearRgtRdrObj9RdrObjCntr"
        sig_start_bit = 359
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
        startbit = 359
        byte = 44
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class RearRgtRdrObj8ObjBoxCenterLat:
        sig_name = "RearRgtRdrObj8ObjBoxCenterLat"
        sig_start_bit = 215
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 215
        byte = 26
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearRgtRdrObj9RdrObjDx:
        sig_name = "RearRgtRdrObj9RdrObjDx"
        sig_start_bit = 355
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 355
        bmuws_info = [(44, 0b00001111, 0b11110000, 4, 0), (45, 0b11111111, 0b00000000, 8, 0)]

    class RearRgtRdrObj8RdrObjExistProb:
        sig_name = "RearRgtRdrObj8RdrObjExistProb"
        sig_start_bit = 252
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 252
        bmuws_info = [(31, 0b00011111, 0b11100000, 5, 0), (32, 0b11111000, 0b00000111, 5, 3)]

    class RearRgtRdrObj9RdrObjID:
        sig_name = "RearRgtRdrObj9RdrObjID"
        sig_start_bit = 454
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 454
        byte = 56
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1


class BgmADCANFDFr14:
    msg_name = "BgmADCANFDFr14"
    msg_id = 504
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "BGM"
    rx_nodes = ['ACU']
    sig_group_dict = {'FrntRgtRdrObj8': ['FrntRgtRdrObj8ObjBoxCenterLat', 'FrntRgtRdrObj8ObjBoxCenterLgt', 'FrntRgtRdrObj8RdrObjChks', 'FrntRgtRdrObj8RdrObjCntr', 'FrntRgtRdrObj8RdrObjDx', 'FrntRgtRdrObj8RdrObjDxStdDe', 'FrntRgtRdrObj8RdrObjDy', 'FrntRgtRdrObj8RdrObjDynProp', 'FrntRgtRdrObj8RdrObjDyStdDe', 'FrntRgtRdrObj8RdrObjExistProb', 'FrntRgtRdrObj8RdrObjHeight', 'FrntRgtRdrObj8RdrObjHeightStdDe', 'FrntRgtRdrObj8RdrObjID', 'FrntRgtRdrObj8RdrObjLifeCycle', 'FrntRgtRdrObj8RdrObjPwr', 'FrntRgtRdrObj8RdrObjVx', 'FrntRgtRdrObj8RdrObjVxStdDe', 'FrntRgtRdrObj8RdrObjVy', 'FrntRgtRdrObj8RdrObjVyStdDe'], 'FrntRgtRdrObj7': ['FrntRgtRdrObj7ObjBoxCenterLat', 'FrntRgtRdrObj7ObjBoxCenterLgt', 'FrntRgtRdrObj7RdrObjChks', 'FrntRgtRdrObj7RdrObjCntr', 'FrntRgtRdrObj7RdrObjDx', 'FrntRgtRdrObj7RdrObjDxStdDe', 'FrntRgtRdrObj7RdrObjDy', 'FrntRgtRdrObj7RdrObjDynProp', 'FrntRgtRdrObj7RdrObjDyStdDe', 'FrntRgtRdrObj7RdrObjExistProb', 'FrntRgtRdrObj7RdrObjHeight', 'FrntRgtRdrObj7RdrObjHeightStdDe', 'FrntRgtRdrObj7RdrObjID', 'FrntRgtRdrObj7RdrObjLifeCycle', 'FrntRgtRdrObj7RdrObjPwr', 'FrntRgtRdrObj7RdrObjVx', 'FrntRgtRdrObj7RdrObjVxStdDe', 'FrntRgtRdrObj7RdrObjVy', 'FrntRgtRdrObj7RdrObjVyStdDe'], 'FrntRgtRdrObj9': ['FrntRgtRdrObj9ObjBoxCenterLat', 'FrntRgtRdrObj9ObjBoxCenterLgt', 'FrntRgtRdrObj9RdrObjChks', 'FrntRgtRdrObj9RdrObjCntr', 'FrntRgtRdrObj9RdrObjDx', 'FrntRgtRdrObj9RdrObjDxStdDe', 'FrntRgtRdrObj9RdrObjDy', 'FrntRgtRdrObj9RdrObjDynProp', 'FrntRgtRdrObj9RdrObjDyStdDe', 'FrntRgtRdrObj9RdrObjExistProb', 'FrntRgtRdrObj9RdrObjHeight', 'FrntRgtRdrObj9RdrObjHeightStdDe', 'FrntRgtRdrObj9RdrObjID', 'FrntRgtRdrObj9RdrObjLifeCycle', 'FrntRgtRdrObj9RdrObjPwr', 'FrntRgtRdrObj9RdrObjVx', 'FrntRgtRdrObj9RdrObjVxStdDe', 'FrntRgtRdrObj9RdrObjVy', 'FrntRgtRdrObj9RdrObjVyStdDe']}
    sig_group_dataid_dict = {}

    class FrntRgtRdrObj7RdrObjDx:
        sig_name = "FrntRgtRdrObj7RdrObjDx"
        sig_start_bit = 11
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 11
        bmuws_info = [(1, 0b00001111, 0b11110000, 4, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class FrntRgtRdrObj8_UB:
        sig_name = "FrntRgtRdrObj8_UB"
        sig_start_bit = 168
        update_id_bit = 168
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
        startbit = 168
        byte = 21
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FrntRgtRdrObj7_UB:
        sig_name = "FrntRgtRdrObj7_UB"
        sig_start_bit = 175
        update_id_bit = 175
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
        startbit = 175
        byte = 21
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class FrntRgtRdrObj7RdrObjHeight:
        sig_name = "FrntRgtRdrObj7RdrObjHeight"
        sig_start_bit = 82
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 82
        bmuws_info = [(10, 0b00000111, 0b11111000, 3, 0), (11, 0b11111110, 0b00000001, 7, 1)]

    class FrntRgtRdrObj8RdrObjHeightStdDe:
        sig_name = "FrntRgtRdrObj8RdrObjHeightStdDe"
        sig_start_bit = 264
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 264
        bmuws_info = [(33, 0b00000001, 0b11111110, 1, 0), (34, 0b11111111, 0b00000000, 8, 0), (35, 0b10000000, 0b01111111, 1, 7)]

    class FrntRgtRdrObj7RdrObjCntr:
        sig_name = "FrntRgtRdrObj7RdrObjCntr"
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

    class FrntRgtRdrObj9RdrObjVy:
        sig_name = "FrntRgtRdrObj9RdrObjVy"
        sig_start_bit = 492
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 492
        bmuws_info = [(61, 0b00011111, 0b11100000, 5, 0), (62, 0b11111100, 0b00000011, 6, 2)]

    class FrntRgtRdrObj8RdrObjExistProb:
        sig_name = "FrntRgtRdrObj8RdrObjExistProb"
        sig_start_bit = 252
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 252
        bmuws_info = [(31, 0b00011111, 0b11100000, 5, 0), (32, 0b11111000, 0b00000111, 5, 3)]

    class FrntRgtRdrObj9RdrObjDyStdDe:
        sig_name = "FrntRgtRdrObj9RdrObjDyStdDe"
        sig_start_bit = 415
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 415
        bmuws_info = [(51, 0b11111111, 0b00000000, 8, 0), (52, 0b11100000, 0b00011111, 3, 5)]

    class FrntRgtRdrObj8ObjBoxCenterLgt:
        sig_name = "FrntRgtRdrObj8ObjBoxCenterLgt"
        sig_start_bit = 207
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 207
        byte = 25
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntRgtRdrObj7RdrObjVxStdDe:
        sig_name = "FrntRgtRdrObj7RdrObjVxStdDe"
        sig_start_bit = 142
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 142
        bmuws_info = [(17, 0b01111111, 0b10000000, 7, 0), (18, 0b11100000, 0b00011111, 3, 5)]

    class FrntRgtRdrObj8RdrObjLifeCycle:
        sig_name = "FrntRgtRdrObj8RdrObjLifeCycle"
        sig_start_bit = 280
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
        startbit = 280
        bmuws_info = [(35, 0b00000001, 0b11111110, 1, 0), (36, 0b11111100, 0b00000011, 6, 2)]

    class FrntRgtRdrObj8RdrObjVxStdDe:
        sig_name = "FrntRgtRdrObj8RdrObjVxStdDe"
        sig_start_bit = 318
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 318
        bmuws_info = [(39, 0b01111111, 0b10000000, 7, 0), (40, 0b11100000, 0b00011111, 3, 5)]

    class FrntRgtRdrObj8RdrObjID:
        sig_name = "FrntRgtRdrObj8RdrObjID"
        sig_start_bit = 286
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 286
        byte = 35
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class FrntRgtRdrObj7ObjBoxCenterLgt:
        sig_name = "FrntRgtRdrObj7ObjBoxCenterLgt"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
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

    class FrntRgtRdrObj7RdrObjVy:
        sig_name = "FrntRgtRdrObj7RdrObjVy"
        sig_start_bit = 148
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 148
        bmuws_info = [(18, 0b00011111, 0b11100000, 5, 0), (19, 0b11111100, 0b00000011, 6, 2)]

    class FrntRgtRdrObj9RdrObjVxStdDe:
        sig_name = "FrntRgtRdrObj9RdrObjVxStdDe"
        sig_start_bit = 486
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 486
        bmuws_info = [(60, 0b01111111, 0b10000000, 7, 0), (61, 0b11100000, 0b00011111, 3, 5)]

    class FrntRgtRdrObj9RdrObjVyStdDe:
        sig_name = "FrntRgtRdrObj9RdrObjVyStdDe"
        sig_start_bit = 497
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 497
        bmuws_info = [(62, 0b00000011, 0b11111100, 2, 0), (63, 0b11111111, 0b00000000, 8, 0)]

    class FrntRgtRdrObj7RdrObjDxStdDe:
        sig_name = "FrntRgtRdrObj7RdrObjDxStdDe"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11100000, 0b00011111, 3, 5)]

    class FrntRgtRdrObj9RdrObjDynProp:
        sig_name = "FrntRgtRdrObj9RdrObjDynProp"
        sig_start_bit = 396
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 396
        byte = 49
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class FrntRgtRdrObj8RdrObjDynProp:
        sig_name = "FrntRgtRdrObj8RdrObjDynProp"
        sig_start_bit = 228
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 228
        byte = 28
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class FrntRgtRdrObj8RdrObjHeight:
        sig_name = "FrntRgtRdrObj8RdrObjHeight"
        sig_start_bit = 258
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 258
        bmuws_info = [(32, 0b00000111, 0b11111000, 3, 0), (33, 0b11111110, 0b00000001, 7, 1)]

    class FrntRgtRdrObj7RdrObjLifeCycle:
        sig_name = "FrntRgtRdrObj7RdrObjLifeCycle"
        sig_start_bit = 104
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
        startbit = 104
        bmuws_info = [(13, 0b00000001, 0b11111110, 1, 0), (14, 0b11111100, 0b00000011, 6, 2)]

    class FrntRgtRdrObj9ObjBoxCenterLat:
        sig_name = "FrntRgtRdrObj9ObjBoxCenterLat"
        sig_start_bit = 383
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 383
        byte = 47
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntRgtRdrObj8RdrObjCntr:
        sig_name = "FrntRgtRdrObj8RdrObjCntr"
        sig_start_bit = 191
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
        startbit = 191
        byte = 23
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class FrntRgtRdrObj7RdrObjDyStdDe:
        sig_name = "FrntRgtRdrObj7RdrObjDyStdDe"
        sig_start_bit = 71
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 71
        bmuws_info = [(8, 0b11111111, 0b00000000, 8, 0), (9, 0b11100000, 0b00011111, 3, 5)]

    class FrntRgtRdrObj9RdrObjPwr:
        sig_name = "FrntRgtRdrObj9RdrObjPwr"
        sig_start_bit = 457
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 457
        bmuws_info = [(57, 0b00000011, 0b11111100, 2, 0), (58, 0b11111100, 0b00000011, 6, 2)]

    class FrntRgtRdrObj9RdrObjDxStdDe:
        sig_name = "FrntRgtRdrObj9RdrObjDxStdDe"
        sig_start_bit = 391
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 391
        bmuws_info = [(48, 0b11111111, 0b00000000, 8, 0), (49, 0b11100000, 0b00011111, 3, 5)]

    class FrntRgtRdrObj8ObjBoxCenterLat:
        sig_name = "FrntRgtRdrObj8ObjBoxCenterLat"
        sig_start_bit = 215
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 215
        byte = 26
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntRgtRdrObj8RdrObjVx:
        sig_name = "FrntRgtRdrObj8RdrObjVx"
        sig_start_bit = 297
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 297
        bmuws_info = [(37, 0b00000011, 0b11111100, 2, 0), (38, 0b11111111, 0b00000000, 8, 0), (39, 0b10000000, 0b01111111, 1, 7)]

    class FrntRgtRdrObj9ObjBoxCenterLgt:
        sig_name = "FrntRgtRdrObj9ObjBoxCenterLgt"
        sig_start_bit = 375
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 375
        byte = 46
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntRgtRdrObj7RdrObjHeightStdDe:
        sig_name = "FrntRgtRdrObj7RdrObjHeightStdDe"
        sig_start_bit = 88
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 88
        bmuws_info = [(11, 0b00000001, 0b11111110, 1, 0), (12, 0b11111111, 0b00000000, 8, 0), (13, 0b10000000, 0b01111111, 1, 7)]

    class FrntRgtRdrObj9RdrObjHeightStdDe:
        sig_name = "FrntRgtRdrObj9RdrObjHeightStdDe"
        sig_start_bit = 432
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 432
        bmuws_info = [(54, 0b00000001, 0b11111110, 1, 0), (55, 0b11111111, 0b00000000, 8, 0), (56, 0b10000000, 0b01111111, 1, 7)]

    class FrntRgtRdrObj9RdrObjID:
        sig_name = "FrntRgtRdrObj9RdrObjID"
        sig_start_bit = 454
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 454
        byte = 56
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class FrntRgtRdrObj8RdrObjVy:
        sig_name = "FrntRgtRdrObj8RdrObjVy"
        sig_start_bit = 324
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 324
        bmuws_info = [(40, 0b00011111, 0b11100000, 5, 0), (41, 0b11111100, 0b00000011, 6, 2)]

    class FrntRgtRdrObj7RdrObjVx:
        sig_name = "FrntRgtRdrObj7RdrObjVx"
        sig_start_bit = 121
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 121
        bmuws_info = [(15, 0b00000011, 0b11111100, 2, 0), (16, 0b11111111, 0b00000000, 8, 0), (17, 0b10000000, 0b01111111, 1, 7)]

    class FrntRgtRdrObj9RdrObjVx:
        sig_name = "FrntRgtRdrObj9RdrObjVx"
        sig_start_bit = 465
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 465
        bmuws_info = [(58, 0b00000011, 0b11111100, 2, 0), (59, 0b11111111, 0b00000000, 8, 0), (60, 0b10000000, 0b01111111, 1, 7)]

    class FrntRgtRdrObj7RdrObjExistProb:
        sig_name = "FrntRgtRdrObj7RdrObjExistProb"
        sig_start_bit = 76
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 76
        bmuws_info = [(9, 0b00011111, 0b11100000, 5, 0), (10, 0b11111000, 0b00000111, 5, 3)]

    class FrntRgtRdrObj9RdrObjHeight:
        sig_name = "FrntRgtRdrObj9RdrObjHeight"
        sig_start_bit = 426
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 426
        bmuws_info = [(53, 0b00000111, 0b11111000, 3, 0), (54, 0b11111110, 0b00000001, 7, 1)]

    class FrntRgtRdrObj7RdrObjVyStdDe:
        sig_name = "FrntRgtRdrObj7RdrObjVyStdDe"
        sig_start_bit = 153
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 153
        bmuws_info = [(19, 0b00000011, 0b11111100, 2, 0), (20, 0b11111111, 0b00000000, 8, 0)]

    class FrntRgtRdrObj7RdrObjChks:
        sig_name = "FrntRgtRdrObj7RdrObjChks"
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

    class FrntRgtRdrObj9RdrObjExistProb:
        sig_name = "FrntRgtRdrObj9RdrObjExistProb"
        sig_start_bit = 420
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 420
        bmuws_info = [(52, 0b00011111, 0b11100000, 5, 0), (53, 0b11111000, 0b00000111, 5, 3)]

    class FrntRgtRdrObj8RdrObjDxStdDe:
        sig_name = "FrntRgtRdrObj8RdrObjDxStdDe"
        sig_start_bit = 223
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 223
        bmuws_info = [(27, 0b11111111, 0b00000000, 8, 0), (28, 0b11100000, 0b00011111, 3, 5)]

    class FrntRgtRdrObj9RdrObjLifeCycle:
        sig_name = "FrntRgtRdrObj9RdrObjLifeCycle"
        sig_start_bit = 448
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
        startbit = 448
        bmuws_info = [(56, 0b00000001, 0b11111110, 1, 0), (57, 0b11111100, 0b00000011, 6, 2)]

    class FrntRgtRdrObj9RdrObjChks:
        sig_name = "FrntRgtRdrObj9RdrObjChks"
        sig_start_bit = 351
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
        startbit = 351
        byte = 43
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntRgtRdrObj8RdrObjVyStdDe:
        sig_name = "FrntRgtRdrObj8RdrObjVyStdDe"
        sig_start_bit = 329
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 329
        bmuws_info = [(41, 0b00000011, 0b11111100, 2, 0), (42, 0b11111111, 0b00000000, 8, 0)]

    class FrntRgtRdrObj7RdrObjID:
        sig_name = "FrntRgtRdrObj7RdrObjID"
        sig_start_bit = 110
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 110
        byte = 13
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class FrntRgtRdrObj9_UB:
        sig_name = "FrntRgtRdrObj9_UB"
        sig_start_bit = 171
        update_id_bit = 171
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
        startbit = 171
        byte = 21
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class FrntRgtRdrObj7RdrObjPwr:
        sig_name = "FrntRgtRdrObj7RdrObjPwr"
        sig_start_bit = 113
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 113
        bmuws_info = [(14, 0b00000011, 0b11111100, 2, 0), (15, 0b11111100, 0b00000011, 6, 2)]

    class FrntRgtRdrObj9RdrObjCntr:
        sig_name = "FrntRgtRdrObj9RdrObjCntr"
        sig_start_bit = 359
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
        startbit = 359
        byte = 44
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class FrntRgtRdrObj7RdrObjDynProp:
        sig_name = "FrntRgtRdrObj7RdrObjDynProp"
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
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class FrntRgtRdrObj8RdrObjDy:
        sig_name = "FrntRgtRdrObj8RdrObjDy"
        sig_start_bit = 227
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 227
        bmuws_info = [(28, 0b00001111, 0b11110000, 4, 0), (29, 0b11111111, 0b00000000, 8, 0)]

    class FrntRgtRdrObj8RdrObjChks:
        sig_name = "FrntRgtRdrObj8RdrObjChks"
        sig_start_bit = 183
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
        startbit = 183
        byte = 22
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntRgtRdrObj8RdrObjPwr:
        sig_name = "FrntRgtRdrObj8RdrObjPwr"
        sig_start_bit = 289
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 289
        bmuws_info = [(36, 0b00000011, 0b11111100, 2, 0), (37, 0b11111100, 0b00000011, 6, 2)]

    class FrntRgtRdrObj9RdrObjDx:
        sig_name = "FrntRgtRdrObj9RdrObjDx"
        sig_start_bit = 355
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 355
        bmuws_info = [(44, 0b00001111, 0b11110000, 4, 0), (45, 0b11111111, 0b00000000, 8, 0)]

    class FrntRgtRdrObj8RdrObjDyStdDe:
        sig_name = "FrntRgtRdrObj8RdrObjDyStdDe"
        sig_start_bit = 247
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 247
        bmuws_info = [(30, 0b11111111, 0b00000000, 8, 0), (31, 0b11100000, 0b00011111, 3, 5)]

    class FrntRgtRdrObj7RdrObjDy:
        sig_name = "FrntRgtRdrObj7RdrObjDy"
        sig_start_bit = 51
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 51
        bmuws_info = [(6, 0b00001111, 0b11110000, 4, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class FrntRgtRdrObj8RdrObjDx:
        sig_name = "FrntRgtRdrObj8RdrObjDx"
        sig_start_bit = 187
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 187
        bmuws_info = [(23, 0b00001111, 0b11110000, 4, 0), (24, 0b11111111, 0b00000000, 8, 0)]

    class FrntRgtRdrObj7ObjBoxCenterLat:
        sig_name = "FrntRgtRdrObj7ObjBoxCenterLat"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
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

    class FrntRgtRdrObj9RdrObjDy:
        sig_name = "FrntRgtRdrObj9RdrObjDy"
        sig_start_bit = 395
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 395
        bmuws_info = [(49, 0b00001111, 0b11110000, 4, 0), (50, 0b11111111, 0b00000000, 8, 0)]


class AcuADCANFDFr05:
    msg_name = "AcuADCANFDFr05"
    msg_id = 288
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 8
    tx_node = "ACU"
    rx_nodes = ['BGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class LidarPowerReq:
        sig_name = "LidarPowerReq"
        sig_start_bit = 62
        update_id_bit = 60
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
        startbit = 62
        byte = 7
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class SentrWarnReq:
        sig_name = "SentrWarnReq"
        sig_start_bit = 63
        update_id_bit = 61
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
        startbit = 63
        byte = 7
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7


class BgmADCANFDFr17:
    msg_name = "BgmADCANFDFr17"
    msg_id = 508
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "BGM"
    rx_nodes = ['ACU']
    sig_group_dict = {'FrntRgtRdrSync': ['FrntRgtRdrSyncRdrObjTimeStampNSec', 'FrntRgtRdrSyncRdrObjTimeStampSec', 'FrntRgtRdrSyncRdrSyncChks', 'FrntRgtRdrSyncRdrSyncCntr'], 'FrntRgtRdrObj16': ['FrntRgtRdrObj16ObjBoxCenterLat', 'FrntRgtRdrObj16ObjBoxCenterLgt', 'FrntRgtRdrObj16RdrObjChks', 'FrntRgtRdrObj16RdrObjCntr', 'FrntRgtRdrObj16RdrObjDx', 'FrntRgtRdrObj16RdrObjDxStdDe', 'FrntRgtRdrObj16RdrObjDy', 'FrntRgtRdrObj16RdrObjDynProp', 'FrntRgtRdrObj16RdrObjDyStdDe', 'FrntRgtRdrObj16RdrObjExistProb', 'FrntRgtRdrObj16RdrObjHeight', 'FrntRgtRdrObj16RdrObjHeightStdDe', 'FrntRgtRdrObj16RdrObjID', 'FrntRgtRdrObj16RdrObjLifeCycle', 'FrntRgtRdrObj16RdrObjPwr', 'FrntRgtRdrObj16RdrObjVx', 'FrntRgtRdrObj16RdrObjVxStdDe', 'FrntRgtRdrObj16RdrObjVy', 'FrntRgtRdrObj16RdrObjVyStdDe']}
    sig_group_dataid_dict = {}

    class FrntRgtRdrObj16RdrObjVxStdDe:
        sig_name = "FrntRgtRdrObj16RdrObjVxStdDe"
        sig_start_bit = 142
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 142
        bmuws_info = [(17, 0b01111111, 0b10000000, 7, 0), (18, 0b11100000, 0b00011111, 3, 5)]

    class FrntRgtRdrFault:
        sig_name = "FrntRgtRdrFault"
        sig_start_bit = 171
        update_id_bit = 169
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
        startbit = 171
        byte = 21
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class FrntRgtRdrObj16RdrObjPwr:
        sig_name = "FrntRgtRdrObj16RdrObjPwr"
        sig_start_bit = 113
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 113
        bmuws_info = [(14, 0b00000011, 0b11111100, 2, 0), (15, 0b11111100, 0b00000011, 6, 2)]

    class FrntRgtRdrObj16RdrObjVyStdDe:
        sig_name = "FrntRgtRdrObj16RdrObjVyStdDe"
        sig_start_bit = 153
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 153
        bmuws_info = [(19, 0b00000011, 0b11111100, 2, 0), (20, 0b11111111, 0b00000000, 8, 0)]

    class FrntRgtRdrObj16RdrObjDy:
        sig_name = "FrntRgtRdrObj16RdrObjDy"
        sig_start_bit = 51
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 51
        bmuws_info = [(6, 0b00001111, 0b11110000, 4, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class FrntRgtRdrObj16RdrObjCntr:
        sig_name = "FrntRgtRdrObj16RdrObjCntr"
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

    class FrntRgtRdrObj16RdrObjHeightStdDe:
        sig_name = "FrntRgtRdrObj16RdrObjHeightStdDe"
        sig_start_bit = 88
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 88
        bmuws_info = [(11, 0b00000001, 0b11111110, 1, 0), (12, 0b11111111, 0b00000000, 8, 0), (13, 0b10000000, 0b01111111, 1, 7)]

    class FrntRgtRdrObj16RdrObjDx:
        sig_name = "FrntRgtRdrObj16RdrObjDx"
        sig_start_bit = 11
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 11
        bmuws_info = [(1, 0b00001111, 0b11110000, 4, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class FrntRgtRdrObj16RdrObjVx:
        sig_name = "FrntRgtRdrObj16RdrObjVx"
        sig_start_bit = 121
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 121
        bmuws_info = [(15, 0b00000011, 0b11111100, 2, 0), (16, 0b11111111, 0b00000000, 8, 0), (17, 0b10000000, 0b01111111, 1, 7)]

    class FrntRgtRdrObj16RdrObjExistProb:
        sig_name = "FrntRgtRdrObj16RdrObjExistProb"
        sig_start_bit = 76
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 76
        bmuws_info = [(9, 0b00011111, 0b11100000, 5, 0), (10, 0b11111000, 0b00000111, 5, 3)]

    class FrntRgtRdrSyncRdrObjTimeStampSec:
        sig_name = "FrntRgtRdrSyncRdrObjTimeStampSec"
        sig_start_bit = 239
        update_id_bit = None
        sig_length = 32
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4294967295
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 32
        startbit = 239
        bmuws_info = [(29, 0b11111111, 0b00000000, 8, 0), (30, 0b11111111, 0b00000000, 8, 0), (31, 0b11111111, 0b00000000, 8, 0), (32, 0b11111111, 0b00000000, 8, 0)]

    class FrntRgtRdrSyncRdrSyncChks:
        sig_name = "FrntRgtRdrSyncRdrSyncChks"
        sig_start_bit = 191
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
        startbit = 191
        byte = 23
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntRgtRdrObj16RdrObjChks:
        sig_name = "FrntRgtRdrObj16RdrObjChks"
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

    class FrntRgtRdrObj16ObjBoxCenterLat:
        sig_name = "FrntRgtRdrObj16ObjBoxCenterLat"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
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

    class FrntRgtRdrObj16RdrObjVy:
        sig_name = "FrntRgtRdrObj16RdrObjVy"
        sig_start_bit = 148
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 148
        bmuws_info = [(18, 0b00011111, 0b11100000, 5, 0), (19, 0b11111100, 0b00000011, 6, 2)]

    class FrntRgtRdrSyncRdrObjTimeStampNSec:
        sig_name = "FrntRgtRdrSyncRdrObjTimeStampNSec"
        sig_start_bit = 207
        update_id_bit = None
        sig_length = 32
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4294967295
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 32
        startbit = 207
        bmuws_info = [(25, 0b11111111, 0b00000000, 8, 0), (26, 0b11111111, 0b00000000, 8, 0), (27, 0b11111111, 0b00000000, 8, 0), (28, 0b11111111, 0b00000000, 8, 0)]

    class FrntRgtRdrObj16ObjBoxCenterLgt:
        sig_name = "FrntRgtRdrObj16ObjBoxCenterLgt"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
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

    class FrntRgtRdrObj16RdrObjID:
        sig_name = "FrntRgtRdrObj16RdrObjID"
        sig_start_bit = 110
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 110
        byte = 13
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class FrntRgtRdrObj16RdrObjLifeCycle:
        sig_name = "FrntRgtRdrObj16RdrObjLifeCycle"
        sig_start_bit = 104
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
        startbit = 104
        bmuws_info = [(13, 0b00000001, 0b11111110, 1, 0), (14, 0b11111100, 0b00000011, 6, 2)]

    class FrntRgtRdrObj16RdrObjDynProp:
        sig_name = "FrntRgtRdrObj16RdrObjDynProp"
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
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class FrntRgtRdrSync_UB:
        sig_name = "FrntRgtRdrSync_UB"
        sig_start_bit = 271
        update_id_bit = 271
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
        startbit = 271
        byte = 33
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class FrntRgtRdrSyncRdrSyncCntr:
        sig_name = "FrntRgtRdrSyncRdrSyncCntr"
        sig_start_bit = 195
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
        startbit = 195
        byte = 24
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class FrntRgtRdrObj16RdrObjHeight:
        sig_name = "FrntRgtRdrObj16RdrObjHeight"
        sig_start_bit = 82
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 82
        bmuws_info = [(10, 0b00000111, 0b11111000, 3, 0), (11, 0b11111110, 0b00000001, 7, 1)]

    class FrntRgtRdrObj16RdrObjDyStdDe:
        sig_name = "FrntRgtRdrObj16RdrObjDyStdDe"
        sig_start_bit = 71
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 71
        bmuws_info = [(8, 0b11111111, 0b00000000, 8, 0), (9, 0b11100000, 0b00011111, 3, 5)]

    class FrntRgtRdrObj16RdrObjDxStdDe:
        sig_name = "FrntRgtRdrObj16RdrObjDxStdDe"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11100000, 0b00011111, 3, 5)]

    class FrntRgtRdrObj16_UB:
        sig_name = "FrntRgtRdrObj16_UB"
        sig_start_bit = 175
        update_id_bit = 175
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
        startbit = 175
        byte = 21
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7


class BgmADCANFDFr25:
    msg_name = "BgmADCANFDFr25"
    msg_id = 517
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "BGM"
    rx_nodes = ['ACU']
    sig_group_dict = {'RearRgtRdrObj6': ['RearRgtRdrObj6ObjBoxCenterLat', 'RearRgtRdrObj6ObjBoxCenterLgt', 'RearRgtRdrObj6RdrObjChks', 'RearRgtRdrObj6RdrObjCntr', 'RearRgtRdrObj6RdrObjDx', 'RearRgtRdrObj6RdrObjDxStdDe', 'RearRgtRdrObj6RdrObjDy', 'RearRgtRdrObj6RdrObjDynProp', 'RearRgtRdrObj6RdrObjDyStdDe', 'RearRgtRdrObj6RdrObjExistProb', 'RearRgtRdrObj6RdrObjHeight', 'RearRgtRdrObj6RdrObjHeightStdDe', 'RearRgtRdrObj6RdrObjID', 'RearRgtRdrObj6RdrObjLifeCycle', 'RearRgtRdrObj6RdrObjPwr', 'RearRgtRdrObj6RdrObjVx', 'RearRgtRdrObj6RdrObjVxStdDe', 'RearRgtRdrObj6RdrObjVy', 'RearRgtRdrObj6RdrObjVyStdDe'], 'RearRgtRdrObj5': ['RearRgtRdrObj5ObjBoxCenterLat', 'RearRgtRdrObj5ObjBoxCenterLgt', 'RearRgtRdrObj5RdrObjChks', 'RearRgtRdrObj5RdrObjCntr', 'RearRgtRdrObj5RdrObjDx', 'RearRgtRdrObj5RdrObjDxStdDe', 'RearRgtRdrObj5RdrObjDy', 'RearRgtRdrObj5RdrObjDynProp', 'RearRgtRdrObj5RdrObjDyStdDe', 'RearRgtRdrObj5RdrObjExistProb', 'RearRgtRdrObj5RdrObjHeight', 'RearRgtRdrObj5RdrObjHeightStdDe', 'RearRgtRdrObj5RdrObjID', 'RearRgtRdrObj5RdrObjLifeCycle', 'RearRgtRdrObj5RdrObjPwr', 'RearRgtRdrObj5RdrObjVx', 'RearRgtRdrObj5RdrObjVxStdDe', 'RearRgtRdrObj5RdrObjVy', 'RearRgtRdrObj5RdrObjVyStdDe'], 'RearRgtRdrObj4': ['RearRgtRdrObj4ObjBoxCenterLat', 'RearRgtRdrObj4ObjBoxCenterLgt', 'RearRgtRdrObj4RdrObjChks', 'RearRgtRdrObj4RdrObjCntr', 'RearRgtRdrObj4RdrObjDx', 'RearRgtRdrObj4RdrObjDxStdDe', 'RearRgtRdrObj4RdrObjDy', 'RearRgtRdrObj4RdrObjDynProp', 'RearRgtRdrObj4RdrObjDyStdDe', 'RearRgtRdrObj4RdrObjExistProb', 'RearRgtRdrObj4RdrObjHeight', 'RearRgtRdrObj4RdrObjHeightStdDe', 'RearRgtRdrObj4RdrObjID', 'RearRgtRdrObj4RdrObjLifeCycle', 'RearRgtRdrObj4RdrObjPwr', 'RearRgtRdrObj4RdrObjVx', 'RearRgtRdrObj4RdrObjVxStdDe', 'RearRgtRdrObj4RdrObjVy', 'RearRgtRdrObj4RdrObjVyStdDe']}
    sig_group_dataid_dict = {}

    class RearRgtRdrObj5ObjBoxCenterLgt:
        sig_name = "RearRgtRdrObj5ObjBoxCenterLgt"
        sig_start_bit = 207
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 207
        byte = 25
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearRgtRdrObj5RdrObjDy:
        sig_name = "RearRgtRdrObj5RdrObjDy"
        sig_start_bit = 227
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 227
        bmuws_info = [(28, 0b00001111, 0b11110000, 4, 0), (29, 0b11111111, 0b00000000, 8, 0)]

    class RearRgtRdrObj5RdrObjDyStdDe:
        sig_name = "RearRgtRdrObj5RdrObjDyStdDe"
        sig_start_bit = 247
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 247
        bmuws_info = [(30, 0b11111111, 0b00000000, 8, 0), (31, 0b11100000, 0b00011111, 3, 5)]

    class RearRgtRdrObj6RdrObjVyStdDe:
        sig_name = "RearRgtRdrObj6RdrObjVyStdDe"
        sig_start_bit = 497
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 497
        bmuws_info = [(62, 0b00000011, 0b11111100, 2, 0), (63, 0b11111111, 0b00000000, 8, 0)]

    class RearRgtRdrObj6RdrObjChks:
        sig_name = "RearRgtRdrObj6RdrObjChks"
        sig_start_bit = 351
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
        startbit = 351
        byte = 43
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearRgtRdrObj5RdrObjDxStdDe:
        sig_name = "RearRgtRdrObj5RdrObjDxStdDe"
        sig_start_bit = 223
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 223
        bmuws_info = [(27, 0b11111111, 0b00000000, 8, 0), (28, 0b11100000, 0b00011111, 3, 5)]

    class RearRgtRdrObj5RdrObjExistProb:
        sig_name = "RearRgtRdrObj5RdrObjExistProb"
        sig_start_bit = 252
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 252
        bmuws_info = [(31, 0b00011111, 0b11100000, 5, 0), (32, 0b11111000, 0b00000111, 5, 3)]

    class RearRgtRdrObj5RdrObjCntr:
        sig_name = "RearRgtRdrObj5RdrObjCntr"
        sig_start_bit = 191
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
        startbit = 191
        byte = 23
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class RearRgtRdrObj5RdrObjHeight:
        sig_name = "RearRgtRdrObj5RdrObjHeight"
        sig_start_bit = 258
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 258
        bmuws_info = [(32, 0b00000111, 0b11111000, 3, 0), (33, 0b11111110, 0b00000001, 7, 1)]

    class RearRgtRdrObj6RdrObjLifeCycle:
        sig_name = "RearRgtRdrObj6RdrObjLifeCycle"
        sig_start_bit = 448
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
        startbit = 448
        bmuws_info = [(56, 0b00000001, 0b11111110, 1, 0), (57, 0b11111100, 0b00000011, 6, 2)]

    class RearRgtRdrObj6_UB:
        sig_name = "RearRgtRdrObj6_UB"
        sig_start_bit = 171
        update_id_bit = 171
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
        startbit = 171
        byte = 21
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class RearRgtRdrObj5RdrObjVy:
        sig_name = "RearRgtRdrObj5RdrObjVy"
        sig_start_bit = 324
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 324
        bmuws_info = [(40, 0b00011111, 0b11100000, 5, 0), (41, 0b11111100, 0b00000011, 6, 2)]

    class RearRgtRdrObj4RdrObjDx:
        sig_name = "RearRgtRdrObj4RdrObjDx"
        sig_start_bit = 11
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 11
        bmuws_info = [(1, 0b00001111, 0b11110000, 4, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class RearRgtRdrObj5RdrObjVx:
        sig_name = "RearRgtRdrObj5RdrObjVx"
        sig_start_bit = 297
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 297
        bmuws_info = [(37, 0b00000011, 0b11111100, 2, 0), (38, 0b11111111, 0b00000000, 8, 0), (39, 0b10000000, 0b01111111, 1, 7)]

    class RearRgtRdrObj4RdrObjVxStdDe:
        sig_name = "RearRgtRdrObj4RdrObjVxStdDe"
        sig_start_bit = 142
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 142
        bmuws_info = [(17, 0b01111111, 0b10000000, 7, 0), (18, 0b11100000, 0b00011111, 3, 5)]

    class RearRgtRdrObj4RdrObjExistProb:
        sig_name = "RearRgtRdrObj4RdrObjExistProb"
        sig_start_bit = 76
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 76
        bmuws_info = [(9, 0b00011111, 0b11100000, 5, 0), (10, 0b11111000, 0b00000111, 5, 3)]

    class RearRgtRdrObj5RdrObjDx:
        sig_name = "RearRgtRdrObj5RdrObjDx"
        sig_start_bit = 187
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 187
        bmuws_info = [(23, 0b00001111, 0b11110000, 4, 0), (24, 0b11111111, 0b00000000, 8, 0)]

    class RearRgtRdrObj4RdrObjCntr:
        sig_name = "RearRgtRdrObj4RdrObjCntr"
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

    class RearRgtRdrObj5_UB:
        sig_name = "RearRgtRdrObj5_UB"
        sig_start_bit = 168
        update_id_bit = 168
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
        startbit = 168
        byte = 21
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class RearRgtRdrObj6RdrObjDynProp:
        sig_name = "RearRgtRdrObj6RdrObjDynProp"
        sig_start_bit = 396
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 396
        byte = 49
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class RearRgtRdrObj6ObjBoxCenterLgt:
        sig_name = "RearRgtRdrObj6ObjBoxCenterLgt"
        sig_start_bit = 375
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 375
        byte = 46
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearRgtRdrObj6RdrObjPwr:
        sig_name = "RearRgtRdrObj6RdrObjPwr"
        sig_start_bit = 457
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 457
        bmuws_info = [(57, 0b00000011, 0b11111100, 2, 0), (58, 0b11111100, 0b00000011, 6, 2)]

    class RearRgtRdrObj5RdrObjHeightStdDe:
        sig_name = "RearRgtRdrObj5RdrObjHeightStdDe"
        sig_start_bit = 264
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 264
        bmuws_info = [(33, 0b00000001, 0b11111110, 1, 0), (34, 0b11111111, 0b00000000, 8, 0), (35, 0b10000000, 0b01111111, 1, 7)]

    class RearRgtRdrObj4ObjBoxCenterLat:
        sig_name = "RearRgtRdrObj4ObjBoxCenterLat"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
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

    class RearRgtRdrObj6RdrObjHeight:
        sig_name = "RearRgtRdrObj6RdrObjHeight"
        sig_start_bit = 426
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 426
        bmuws_info = [(53, 0b00000111, 0b11111000, 3, 0), (54, 0b11111110, 0b00000001, 7, 1)]

    class RearRgtRdrObj6RdrObjCntr:
        sig_name = "RearRgtRdrObj6RdrObjCntr"
        sig_start_bit = 359
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
        startbit = 359
        byte = 44
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class RearRgtRdrObj6RdrObjDyStdDe:
        sig_name = "RearRgtRdrObj6RdrObjDyStdDe"
        sig_start_bit = 415
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 415
        bmuws_info = [(51, 0b11111111, 0b00000000, 8, 0), (52, 0b11100000, 0b00011111, 3, 5)]

    class RearRgtRdrObj4RdrObjVy:
        sig_name = "RearRgtRdrObj4RdrObjVy"
        sig_start_bit = 148
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 148
        bmuws_info = [(18, 0b00011111, 0b11100000, 5, 0), (19, 0b11111100, 0b00000011, 6, 2)]

    class RearRgtRdrObj5RdrObjID:
        sig_name = "RearRgtRdrObj5RdrObjID"
        sig_start_bit = 286
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 286
        byte = 35
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class RearRgtRdrObj4RdrObjVx:
        sig_name = "RearRgtRdrObj4RdrObjVx"
        sig_start_bit = 121
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 121
        bmuws_info = [(15, 0b00000011, 0b11111100, 2, 0), (16, 0b11111111, 0b00000000, 8, 0), (17, 0b10000000, 0b01111111, 1, 7)]

    class RearRgtRdrObj4_UB:
        sig_name = "RearRgtRdrObj4_UB"
        sig_start_bit = 175
        update_id_bit = 175
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
        startbit = 175
        byte = 21
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class RearRgtRdrObj6RdrObjHeightStdDe:
        sig_name = "RearRgtRdrObj6RdrObjHeightStdDe"
        sig_start_bit = 432
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 432
        bmuws_info = [(54, 0b00000001, 0b11111110, 1, 0), (55, 0b11111111, 0b00000000, 8, 0), (56, 0b10000000, 0b01111111, 1, 7)]

    class RearRgtRdrObj6ObjBoxCenterLat:
        sig_name = "RearRgtRdrObj6ObjBoxCenterLat"
        sig_start_bit = 383
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 383
        byte = 47
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearRgtRdrObj4RdrObjHeight:
        sig_name = "RearRgtRdrObj4RdrObjHeight"
        sig_start_bit = 82
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 82
        bmuws_info = [(10, 0b00000111, 0b11111000, 3, 0), (11, 0b11111110, 0b00000001, 7, 1)]

    class RearRgtRdrObj5RdrObjVyStdDe:
        sig_name = "RearRgtRdrObj5RdrObjVyStdDe"
        sig_start_bit = 329
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 329
        bmuws_info = [(41, 0b00000011, 0b11111100, 2, 0), (42, 0b11111111, 0b00000000, 8, 0)]

    class RearRgtRdrObj4RdrObjDy:
        sig_name = "RearRgtRdrObj4RdrObjDy"
        sig_start_bit = 51
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 51
        bmuws_info = [(6, 0b00001111, 0b11110000, 4, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class RearRgtRdrObj4RdrObjPwr:
        sig_name = "RearRgtRdrObj4RdrObjPwr"
        sig_start_bit = 113
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 113
        bmuws_info = [(14, 0b00000011, 0b11111100, 2, 0), (15, 0b11111100, 0b00000011, 6, 2)]

    class RearRgtRdrObj5RdrObjLifeCycle:
        sig_name = "RearRgtRdrObj5RdrObjLifeCycle"
        sig_start_bit = 280
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
        startbit = 280
        bmuws_info = [(35, 0b00000001, 0b11111110, 1, 0), (36, 0b11111100, 0b00000011, 6, 2)]

    class RearRgtRdrObj5RdrObjChks:
        sig_name = "RearRgtRdrObj5RdrObjChks"
        sig_start_bit = 183
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
        startbit = 183
        byte = 22
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearRgtRdrObj6RdrObjID:
        sig_name = "RearRgtRdrObj6RdrObjID"
        sig_start_bit = 454
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 454
        byte = 56
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class RearRgtRdrObj6RdrObjDy:
        sig_name = "RearRgtRdrObj6RdrObjDy"
        sig_start_bit = 395
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 395
        bmuws_info = [(49, 0b00001111, 0b11110000, 4, 0), (50, 0b11111111, 0b00000000, 8, 0)]

    class RearRgtRdrObj4ObjBoxCenterLgt:
        sig_name = "RearRgtRdrObj4ObjBoxCenterLgt"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
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

    class RearRgtRdrObj5RdrObjPwr:
        sig_name = "RearRgtRdrObj5RdrObjPwr"
        sig_start_bit = 289
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 289
        bmuws_info = [(36, 0b00000011, 0b11111100, 2, 0), (37, 0b11111100, 0b00000011, 6, 2)]

    class RearRgtRdrObj6RdrObjVx:
        sig_name = "RearRgtRdrObj6RdrObjVx"
        sig_start_bit = 465
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 465
        bmuws_info = [(58, 0b00000011, 0b11111100, 2, 0), (59, 0b11111111, 0b00000000, 8, 0), (60, 0b10000000, 0b01111111, 1, 7)]

    class RearRgtRdrObj4RdrObjHeightStdDe:
        sig_name = "RearRgtRdrObj4RdrObjHeightStdDe"
        sig_start_bit = 88
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 88
        bmuws_info = [(11, 0b00000001, 0b11111110, 1, 0), (12, 0b11111111, 0b00000000, 8, 0), (13, 0b10000000, 0b01111111, 1, 7)]

    class RearRgtRdrObj4RdrObjChks:
        sig_name = "RearRgtRdrObj4RdrObjChks"
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

    class RearRgtRdrObj6RdrObjVxStdDe:
        sig_name = "RearRgtRdrObj6RdrObjVxStdDe"
        sig_start_bit = 486
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 486
        bmuws_info = [(60, 0b01111111, 0b10000000, 7, 0), (61, 0b11100000, 0b00011111, 3, 5)]

    class RearRgtRdrObj4RdrObjLifeCycle:
        sig_name = "RearRgtRdrObj4RdrObjLifeCycle"
        sig_start_bit = 104
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
        startbit = 104
        bmuws_info = [(13, 0b00000001, 0b11111110, 1, 0), (14, 0b11111100, 0b00000011, 6, 2)]

    class RearRgtRdrObj4RdrObjDxStdDe:
        sig_name = "RearRgtRdrObj4RdrObjDxStdDe"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11100000, 0b00011111, 3, 5)]

    class RearRgtRdrObj6RdrObjDx:
        sig_name = "RearRgtRdrObj6RdrObjDx"
        sig_start_bit = 355
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 355
        bmuws_info = [(44, 0b00001111, 0b11110000, 4, 0), (45, 0b11111111, 0b00000000, 8, 0)]

    class RearRgtRdrObj6RdrObjExistProb:
        sig_name = "RearRgtRdrObj6RdrObjExistProb"
        sig_start_bit = 420
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 420
        bmuws_info = [(52, 0b00011111, 0b11100000, 5, 0), (53, 0b11111000, 0b00000111, 5, 3)]

    class RearRgtRdrObj4RdrObjID:
        sig_name = "RearRgtRdrObj4RdrObjID"
        sig_start_bit = 110
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 110
        byte = 13
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class RearRgtRdrObj6RdrObjDxStdDe:
        sig_name = "RearRgtRdrObj6RdrObjDxStdDe"
        sig_start_bit = 391
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 391
        bmuws_info = [(48, 0b11111111, 0b00000000, 8, 0), (49, 0b11100000, 0b00011111, 3, 5)]

    class RearRgtRdrObj5RdrObjVxStdDe:
        sig_name = "RearRgtRdrObj5RdrObjVxStdDe"
        sig_start_bit = 318
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 318
        bmuws_info = [(39, 0b01111111, 0b10000000, 7, 0), (40, 0b11100000, 0b00011111, 3, 5)]

    class RearRgtRdrObj4RdrObjVyStdDe:
        sig_name = "RearRgtRdrObj4RdrObjVyStdDe"
        sig_start_bit = 153
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 153
        bmuws_info = [(19, 0b00000011, 0b11111100, 2, 0), (20, 0b11111111, 0b00000000, 8, 0)]

    class RearRgtRdrObj4RdrObjDyStdDe:
        sig_name = "RearRgtRdrObj4RdrObjDyStdDe"
        sig_start_bit = 71
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 71
        bmuws_info = [(8, 0b11111111, 0b00000000, 8, 0), (9, 0b11100000, 0b00011111, 3, 5)]

    class RearRgtRdrObj5ObjBoxCenterLat:
        sig_name = "RearRgtRdrObj5ObjBoxCenterLat"
        sig_start_bit = 215
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 215
        byte = 26
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearRgtRdrObj5RdrObjDynProp:
        sig_name = "RearRgtRdrObj5RdrObjDynProp"
        sig_start_bit = 228
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 228
        byte = 28
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class RearRgtRdrObj4RdrObjDynProp:
        sig_name = "RearRgtRdrObj4RdrObjDynProp"
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
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class RearRgtRdrObj6RdrObjVy:
        sig_name = "RearRgtRdrObj6RdrObjVy"
        sig_start_bit = 492
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 492
        bmuws_info = [(61, 0b00011111, 0b11100000, 5, 0), (62, 0b11111100, 0b00000011, 6, 2)]


class AcuADCANFDNmFr:
    msg_name = "AcuADCANFDNmFr"
    msg_id = 1282
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "ACU"
    rx_nodes = ['BGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class BgmADCANFDFr13:
    msg_name = "BgmADCANFDFr13"
    msg_id = 503
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "BGM"
    rx_nodes = ['ACU']
    sig_group_dict = {'FrntRgtRdrObj5': ['FrntRgtRdrObj5ObjBoxCenterLat', 'FrntRgtRdrObj5ObjBoxCenterLgt', 'FrntRgtRdrObj5RdrObjChks', 'FrntRgtRdrObj5RdrObjCntr', 'FrntRgtRdrObj5RdrObjDx', 'FrntRgtRdrObj5RdrObjDxStdDe', 'FrntRgtRdrObj5RdrObjDy', 'FrntRgtRdrObj5RdrObjDynProp', 'FrntRgtRdrObj5RdrObjDyStdDe', 'FrntRgtRdrObj5RdrObjExistProb', 'FrntRgtRdrObj5RdrObjHeight', 'FrntRgtRdrObj5RdrObjHeightStdDe', 'FrntRgtRdrObj5RdrObjID', 'FrntRgtRdrObj5RdrObjLifeCycle', 'FrntRgtRdrObj5RdrObjPwr', 'FrntRgtRdrObj5RdrObjVx', 'FrntRgtRdrObj5RdrObjVxStdDe', 'FrntRgtRdrObj5RdrObjVy', 'FrntRgtRdrObj5RdrObjVyStdDe'], 'FrntRgtRdrObj6': ['FrntRgtRdrObj6ObjBoxCenterLat', 'FrntRgtRdrObj6ObjBoxCenterLgt', 'FrntRgtRdrObj6RdrObjChks', 'FrntRgtRdrObj6RdrObjCntr', 'FrntRgtRdrObj6RdrObjDx', 'FrntRgtRdrObj6RdrObjDxStdDe', 'FrntRgtRdrObj6RdrObjDy', 'FrntRgtRdrObj6RdrObjDynProp', 'FrntRgtRdrObj6RdrObjDyStdDe', 'FrntRgtRdrObj6RdrObjExistProb', 'FrntRgtRdrObj6RdrObjHeight', 'FrntRgtRdrObj6RdrObjHeightStdDe', 'FrntRgtRdrObj6RdrObjID', 'FrntRgtRdrObj6RdrObjLifeCycle', 'FrntRgtRdrObj6RdrObjPwr', 'FrntRgtRdrObj6RdrObjVx', 'FrntRgtRdrObj6RdrObjVxStdDe', 'FrntRgtRdrObj6RdrObjVy', 'FrntRgtRdrObj6RdrObjVyStdDe'], 'FrntRgtRdrObj4': ['FrntRgtRdrObj4ObjBoxCenterLat', 'FrntRgtRdrObj4ObjBoxCenterLgt', 'FrntRgtRdrObj4RdrObjChks', 'FrntRgtRdrObj4RdrObjCntr', 'FrntRgtRdrObj4RdrObjDx', 'FrntRgtRdrObj4RdrObjDxStdDe', 'FrntRgtRdrObj4RdrObjDy', 'FrntRgtRdrObj4RdrObjDynProp', 'FrntRgtRdrObj4RdrObjDyStdDe', 'FrntRgtRdrObj4RdrObjExistProb', 'FrntRgtRdrObj4RdrObjHeight', 'FrntRgtRdrObj4RdrObjHeightStdDe', 'FrntRgtRdrObj4RdrObjID', 'FrntRgtRdrObj4RdrObjLifeCycle', 'FrntRgtRdrObj4RdrObjPwr', 'FrntRgtRdrObj4RdrObjVx', 'FrntRgtRdrObj4RdrObjVxStdDe', 'FrntRgtRdrObj4RdrObjVy', 'FrntRgtRdrObj4RdrObjVyStdDe']}
    sig_group_dataid_dict = {}

    class FrntRgtRdrObj6RdrObjID:
        sig_name = "FrntRgtRdrObj6RdrObjID"
        sig_start_bit = 454
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 454
        byte = 56
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class FrntRgtRdrObj6RdrObjDynProp:
        sig_name = "FrntRgtRdrObj6RdrObjDynProp"
        sig_start_bit = 396
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 396
        byte = 49
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class FrntRgtRdrObj6RdrObjVyStdDe:
        sig_name = "FrntRgtRdrObj6RdrObjVyStdDe"
        sig_start_bit = 497
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 497
        bmuws_info = [(62, 0b00000011, 0b11111100, 2, 0), (63, 0b11111111, 0b00000000, 8, 0)]

    class FrntRgtRdrObj4RdrObjVy:
        sig_name = "FrntRgtRdrObj4RdrObjVy"
        sig_start_bit = 148
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 148
        bmuws_info = [(18, 0b00011111, 0b11100000, 5, 0), (19, 0b11111100, 0b00000011, 6, 2)]

    class FrntRgtRdrObj4RdrObjVyStdDe:
        sig_name = "FrntRgtRdrObj4RdrObjVyStdDe"
        sig_start_bit = 153
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 153
        bmuws_info = [(19, 0b00000011, 0b11111100, 2, 0), (20, 0b11111111, 0b00000000, 8, 0)]

    class FrntRgtRdrObj4RdrObjID:
        sig_name = "FrntRgtRdrObj4RdrObjID"
        sig_start_bit = 110
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 110
        byte = 13
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class FrntRgtRdrObj5RdrObjVx:
        sig_name = "FrntRgtRdrObj5RdrObjVx"
        sig_start_bit = 297
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 297
        bmuws_info = [(37, 0b00000011, 0b11111100, 2, 0), (38, 0b11111111, 0b00000000, 8, 0), (39, 0b10000000, 0b01111111, 1, 7)]

    class FrntRgtRdrObj4RdrObjChks:
        sig_name = "FrntRgtRdrObj4RdrObjChks"
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

    class FrntRgtRdrObj5RdrObjChks:
        sig_name = "FrntRgtRdrObj5RdrObjChks"
        sig_start_bit = 183
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
        startbit = 183
        byte = 22
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntRgtRdrObj5RdrObjVy:
        sig_name = "FrntRgtRdrObj5RdrObjVy"
        sig_start_bit = 324
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 324
        bmuws_info = [(40, 0b00011111, 0b11100000, 5, 0), (41, 0b11111100, 0b00000011, 6, 2)]

    class FrntRgtRdrObj6RdrObjDyStdDe:
        sig_name = "FrntRgtRdrObj6RdrObjDyStdDe"
        sig_start_bit = 415
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 415
        bmuws_info = [(51, 0b11111111, 0b00000000, 8, 0), (52, 0b11100000, 0b00011111, 3, 5)]

    class FrntRgtRdrObj4RdrObjDxStdDe:
        sig_name = "FrntRgtRdrObj4RdrObjDxStdDe"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11100000, 0b00011111, 3, 5)]

    class FrntRgtRdrObj6ObjBoxCenterLat:
        sig_name = "FrntRgtRdrObj6ObjBoxCenterLat"
        sig_start_bit = 383
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 383
        byte = 47
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntRgtRdrObj6RdrObjExistProb:
        sig_name = "FrntRgtRdrObj6RdrObjExistProb"
        sig_start_bit = 420
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 420
        bmuws_info = [(52, 0b00011111, 0b11100000, 5, 0), (53, 0b11111000, 0b00000111, 5, 3)]

    class FrntRgtRdrObj5RdrObjDy:
        sig_name = "FrntRgtRdrObj5RdrObjDy"
        sig_start_bit = 227
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 227
        bmuws_info = [(28, 0b00001111, 0b11110000, 4, 0), (29, 0b11111111, 0b00000000, 8, 0)]

    class FrntRgtRdrObj5RdrObjHeightStdDe:
        sig_name = "FrntRgtRdrObj5RdrObjHeightStdDe"
        sig_start_bit = 264
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 264
        bmuws_info = [(33, 0b00000001, 0b11111110, 1, 0), (34, 0b11111111, 0b00000000, 8, 0), (35, 0b10000000, 0b01111111, 1, 7)]

    class FrntRgtRdrObj5ObjBoxCenterLgt:
        sig_name = "FrntRgtRdrObj5ObjBoxCenterLgt"
        sig_start_bit = 207
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 207
        byte = 25
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntRgtRdrObj6RdrObjDy:
        sig_name = "FrntRgtRdrObj6RdrObjDy"
        sig_start_bit = 395
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 395
        bmuws_info = [(49, 0b00001111, 0b11110000, 4, 0), (50, 0b11111111, 0b00000000, 8, 0)]

    class FrntRgtRdrObj6RdrObjLifeCycle:
        sig_name = "FrntRgtRdrObj6RdrObjLifeCycle"
        sig_start_bit = 448
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
        startbit = 448
        bmuws_info = [(56, 0b00000001, 0b11111110, 1, 0), (57, 0b11111100, 0b00000011, 6, 2)]

    class FrntRgtRdrObj5ObjBoxCenterLat:
        sig_name = "FrntRgtRdrObj5ObjBoxCenterLat"
        sig_start_bit = 215
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 215
        byte = 26
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntRgtRdrObj6ObjBoxCenterLgt:
        sig_name = "FrntRgtRdrObj6ObjBoxCenterLgt"
        sig_start_bit = 375
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 375
        byte = 46
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntRgtRdrObj6RdrObjPwr:
        sig_name = "FrntRgtRdrObj6RdrObjPwr"
        sig_start_bit = 457
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 457
        bmuws_info = [(57, 0b00000011, 0b11111100, 2, 0), (58, 0b11111100, 0b00000011, 6, 2)]

    class FrntRgtRdrObj4ObjBoxCenterLgt:
        sig_name = "FrntRgtRdrObj4ObjBoxCenterLgt"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
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

    class FrntRgtRdrObj5_UB:
        sig_name = "FrntRgtRdrObj5_UB"
        sig_start_bit = 168
        update_id_bit = 168
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
        startbit = 168
        byte = 21
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FrntRgtRdrObj5RdrObjDyStdDe:
        sig_name = "FrntRgtRdrObj5RdrObjDyStdDe"
        sig_start_bit = 247
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 247
        bmuws_info = [(30, 0b11111111, 0b00000000, 8, 0), (31, 0b11100000, 0b00011111, 3, 5)]

    class FrntRgtRdrObj4RdrObjHeight:
        sig_name = "FrntRgtRdrObj4RdrObjHeight"
        sig_start_bit = 82
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 82
        bmuws_info = [(10, 0b00000111, 0b11111000, 3, 0), (11, 0b11111110, 0b00000001, 7, 1)]

    class FrntRgtRdrObj6RdrObjVy:
        sig_name = "FrntRgtRdrObj6RdrObjVy"
        sig_start_bit = 492
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 492
        bmuws_info = [(61, 0b00011111, 0b11100000, 5, 0), (62, 0b11111100, 0b00000011, 6, 2)]

    class FrntRgtRdrObj4RdrObjVxStdDe:
        sig_name = "FrntRgtRdrObj4RdrObjVxStdDe"
        sig_start_bit = 142
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 142
        bmuws_info = [(17, 0b01111111, 0b10000000, 7, 0), (18, 0b11100000, 0b00011111, 3, 5)]

    class FrntRgtRdrObj5RdrObjLifeCycle:
        sig_name = "FrntRgtRdrObj5RdrObjLifeCycle"
        sig_start_bit = 280
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
        startbit = 280
        bmuws_info = [(35, 0b00000001, 0b11111110, 1, 0), (36, 0b11111100, 0b00000011, 6, 2)]

    class FrntRgtRdrObj6RdrObjCntr:
        sig_name = "FrntRgtRdrObj6RdrObjCntr"
        sig_start_bit = 359
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
        startbit = 359
        byte = 44
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class FrntRgtRdrObj5RdrObjVxStdDe:
        sig_name = "FrntRgtRdrObj5RdrObjVxStdDe"
        sig_start_bit = 318
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 318
        bmuws_info = [(39, 0b01111111, 0b10000000, 7, 0), (40, 0b11100000, 0b00011111, 3, 5)]

    class FrntRgtRdrObj5RdrObjDynProp:
        sig_name = "FrntRgtRdrObj5RdrObjDynProp"
        sig_start_bit = 228
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 228
        byte = 28
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class FrntRgtRdrObj4RdrObjLifeCycle:
        sig_name = "FrntRgtRdrObj4RdrObjLifeCycle"
        sig_start_bit = 104
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
        startbit = 104
        bmuws_info = [(13, 0b00000001, 0b11111110, 1, 0), (14, 0b11111100, 0b00000011, 6, 2)]

    class FrntRgtRdrObj4RdrObjDy:
        sig_name = "FrntRgtRdrObj4RdrObjDy"
        sig_start_bit = 51
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 51
        bmuws_info = [(6, 0b00001111, 0b11110000, 4, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class FrntRgtRdrObj4RdrObjDyStdDe:
        sig_name = "FrntRgtRdrObj4RdrObjDyStdDe"
        sig_start_bit = 71
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 71
        bmuws_info = [(8, 0b11111111, 0b00000000, 8, 0), (9, 0b11100000, 0b00011111, 3, 5)]

    class FrntRgtRdrObj5RdrObjDx:
        sig_name = "FrntRgtRdrObj5RdrObjDx"
        sig_start_bit = 187
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 187
        bmuws_info = [(23, 0b00001111, 0b11110000, 4, 0), (24, 0b11111111, 0b00000000, 8, 0)]

    class FrntRgtRdrObj5RdrObjPwr:
        sig_name = "FrntRgtRdrObj5RdrObjPwr"
        sig_start_bit = 289
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 289
        bmuws_info = [(36, 0b00000011, 0b11111100, 2, 0), (37, 0b11111100, 0b00000011, 6, 2)]

    class FrntRgtRdrObj6RdrObjHeight:
        sig_name = "FrntRgtRdrObj6RdrObjHeight"
        sig_start_bit = 426
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 426
        bmuws_info = [(53, 0b00000111, 0b11111000, 3, 0), (54, 0b11111110, 0b00000001, 7, 1)]

    class FrntRgtRdrObj6RdrObjDxStdDe:
        sig_name = "FrntRgtRdrObj6RdrObjDxStdDe"
        sig_start_bit = 391
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 391
        bmuws_info = [(48, 0b11111111, 0b00000000, 8, 0), (49, 0b11100000, 0b00011111, 3, 5)]

    class FrntRgtRdrObj4RdrObjDx:
        sig_name = "FrntRgtRdrObj4RdrObjDx"
        sig_start_bit = 11
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 11
        bmuws_info = [(1, 0b00001111, 0b11110000, 4, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class FrntRgtRdrObj6_UB:
        sig_name = "FrntRgtRdrObj6_UB"
        sig_start_bit = 171
        update_id_bit = 171
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
        startbit = 171
        byte = 21
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class FrntRgtRdrObj4RdrObjDynProp:
        sig_name = "FrntRgtRdrObj4RdrObjDynProp"
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
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class FrntRgtRdrObj5RdrObjID:
        sig_name = "FrntRgtRdrObj5RdrObjID"
        sig_start_bit = 286
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 286
        byte = 35
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class FrntRgtRdrObj4RdrObjExistProb:
        sig_name = "FrntRgtRdrObj4RdrObjExistProb"
        sig_start_bit = 76
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 76
        bmuws_info = [(9, 0b00011111, 0b11100000, 5, 0), (10, 0b11111000, 0b00000111, 5, 3)]

    class FrntRgtRdrObj4RdrObjCntr:
        sig_name = "FrntRgtRdrObj4RdrObjCntr"
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

    class FrntRgtRdrObj5RdrObjHeight:
        sig_name = "FrntRgtRdrObj5RdrObjHeight"
        sig_start_bit = 258
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 258
        bmuws_info = [(32, 0b00000111, 0b11111000, 3, 0), (33, 0b11111110, 0b00000001, 7, 1)]

    class FrntRgtRdrObj6RdrObjDx:
        sig_name = "FrntRgtRdrObj6RdrObjDx"
        sig_start_bit = 355
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 355
        bmuws_info = [(44, 0b00001111, 0b11110000, 4, 0), (45, 0b11111111, 0b00000000, 8, 0)]

    class FrntRgtRdrObj5RdrObjCntr:
        sig_name = "FrntRgtRdrObj5RdrObjCntr"
        sig_start_bit = 191
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
        startbit = 191
        byte = 23
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class FrntRgtRdrObj4_UB:
        sig_name = "FrntRgtRdrObj4_UB"
        sig_start_bit = 175
        update_id_bit = 175
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
        startbit = 175
        byte = 21
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class FrntRgtRdrObj5RdrObjExistProb:
        sig_name = "FrntRgtRdrObj5RdrObjExistProb"
        sig_start_bit = 252
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 252
        bmuws_info = [(31, 0b00011111, 0b11100000, 5, 0), (32, 0b11111000, 0b00000111, 5, 3)]

    class FrntRgtRdrObj5RdrObjDxStdDe:
        sig_name = "FrntRgtRdrObj5RdrObjDxStdDe"
        sig_start_bit = 223
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 223
        bmuws_info = [(27, 0b11111111, 0b00000000, 8, 0), (28, 0b11100000, 0b00011111, 3, 5)]

    class FrntRgtRdrObj4ObjBoxCenterLat:
        sig_name = "FrntRgtRdrObj4ObjBoxCenterLat"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
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

    class FrntRgtRdrObj4RdrObjVx:
        sig_name = "FrntRgtRdrObj4RdrObjVx"
        sig_start_bit = 121
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 121
        bmuws_info = [(15, 0b00000011, 0b11111100, 2, 0), (16, 0b11111111, 0b00000000, 8, 0), (17, 0b10000000, 0b01111111, 1, 7)]

    class FrntRgtRdrObj4RdrObjHeightStdDe:
        sig_name = "FrntRgtRdrObj4RdrObjHeightStdDe"
        sig_start_bit = 88
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 88
        bmuws_info = [(11, 0b00000001, 0b11111110, 1, 0), (12, 0b11111111, 0b00000000, 8, 0), (13, 0b10000000, 0b01111111, 1, 7)]

    class FrntRgtRdrObj5RdrObjVyStdDe:
        sig_name = "FrntRgtRdrObj5RdrObjVyStdDe"
        sig_start_bit = 329
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 329
        bmuws_info = [(41, 0b00000011, 0b11111100, 2, 0), (42, 0b11111111, 0b00000000, 8, 0)]

    class FrntRgtRdrObj6RdrObjVx:
        sig_name = "FrntRgtRdrObj6RdrObjVx"
        sig_start_bit = 465
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 465
        bmuws_info = [(58, 0b00000011, 0b11111100, 2, 0), (59, 0b11111111, 0b00000000, 8, 0), (60, 0b10000000, 0b01111111, 1, 7)]

    class FrntRgtRdrObj6RdrObjHeightStdDe:
        sig_name = "FrntRgtRdrObj6RdrObjHeightStdDe"
        sig_start_bit = 432
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 432
        bmuws_info = [(54, 0b00000001, 0b11111110, 1, 0), (55, 0b11111111, 0b00000000, 8, 0), (56, 0b10000000, 0b01111111, 1, 7)]

    class FrntRgtRdrObj6RdrObjVxStdDe:
        sig_name = "FrntRgtRdrObj6RdrObjVxStdDe"
        sig_start_bit = 486
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 486
        bmuws_info = [(60, 0b01111111, 0b10000000, 7, 0), (61, 0b11100000, 0b00011111, 3, 5)]

    class FrntRgtRdrObj4RdrObjPwr:
        sig_name = "FrntRgtRdrObj4RdrObjPwr"
        sig_start_bit = 113
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 113
        bmuws_info = [(14, 0b00000011, 0b11111100, 2, 0), (15, 0b11111100, 0b00000011, 6, 2)]

    class FrntRgtRdrObj6RdrObjChks:
        sig_name = "FrntRgtRdrObj6RdrObjChks"
        sig_start_bit = 351
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
        startbit = 351
        byte = 43
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class AcuADCANFDFr01:
    msg_name = "AcuADCANFDFr01"
    msg_id = 304
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "ACU"
    rx_nodes = ['BGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class WhlSpdCmpFac:
        sig_name = "WhlSpdCmpFac"
        sig_start_bit = 7
        update_id_bit = 2
        sig_length = 5
        sig_value_factor = 0.005
        sig_value_offset = 0.92
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Motorola"
        sig_value_init = 16
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 7
        byte = 0
        mask = 0b11111000
        unmask = 0b00000111
        shift = 3


class AcuADCANFDFr03:
    msg_name = "AcuADCANFDFr03"
    msg_id = 389
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.07
    msg_length = 32
    tx_node = "ACU"
    rx_nodes = ['BGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class OutdSnsrFltReShoRi:
        sig_name = "OutdSnsrFltReShoRi"
        sig_start_bit = 81
        update_id_bit = 136
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltAddCover_NoFault': 0, 'FltAddCover_Fault': 1, 'FltAddCover_Cover': 2}
        compute_method = None
        length = 2
        startbit = 81
        byte = 10
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class OutdRiOfSnsrPrkgAssiFrnt:
        sig_name = "OutdRiOfSnsrPrkgAssiFrnt"
        sig_start_bit = 183
        update_id_bit = 141
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
        startbit = 183
        byte = 22
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ReRiOfSideDoor:
        sig_name = "ReRiOfSideDoor"
        sig_start_bit = 215
        update_id_bit = 147
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
        startbit = 215
        byte = 26
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ReRiOfSnsrOfPrkgAssiSide:
        sig_name = "ReRiOfSnsrOfPrkgAssiSide"
        sig_start_bit = 223
        update_id_bit = 146
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
        startbit = 223
        byte = 27
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class AudWarnOfSnsrParkAssiFrntPosn:
        sig_name = "AudWarnOfSnsrParkAssiFrntPosn"
        sig_start_bit = 15
        update_id_bit = 127
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoRequest': 0, 'Region1': 1, 'Region2': 2, 'Region3': 3, 'Region4': 4, 'Reserve': 5}
        compute_method = None
        length = 3
        startbit = 15
        byte = 1
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class OutdRiOfSnsrPrkgAssiRe:
        sig_name = "OutdRiOfSnsrPrkgAssiRe"
        sig_start_bit = 191
        update_id_bit = 140
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
        startbit = 191
        byte = 23
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntRiOfSideDoor:
        sig_name = "FrntRiOfSideDoor"
        sig_start_bit = 47
        update_id_bit = 121
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

    class OutdLeOfSnsrPrkgAssiFrnt:
        sig_name = "OutdLeOfSnsrPrkgAssiFrnt"
        sig_start_bit = 167
        update_id_bit = 143
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
        startbit = 167
        byte = 20
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class AudWarnLvOfSnsrParkAssiRgt:
        sig_name = "AudWarnLvOfSnsrParkAssiRgt"
        sig_start_bit = 1
        update_id_bit = 112
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BuzzerReqUSS_BuzzerOFF': 0, 'BuzzerReqUSS_BuzzerON_Keep': 1, 'BuzzerReqUSS_BuzzerON_4Hz': 2, 'BuzzerReqUSS_BuzzerON_2Hz': 3}
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class InsdSnsrFltFrntShoLe:
        sig_name = "InsdSnsrFltFrntShoLe"
        sig_start_bit = 63
        update_id_bit = 131
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltAddCover_NoFault': 0, 'FltAddCover_Fault': 1, 'FltAddCover_Cover': 2}
        compute_method = None
        length = 2
        startbit = 63
        byte = 7
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class ReLeOfSideDoor:
        sig_name = "ReLeOfSideDoor"
        sig_start_bit = 199
        update_id_bit = 149
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
        startbit = 199
        byte = 24
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class InsdLeOfSnsrPrkgAssiFrnt:
        sig_name = "InsdLeOfSnsrPrkgAssiFrnt"
        sig_start_bit = 71
        update_id_bit = 135
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
        startbit = 71
        byte = 8
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class OutdLeOfSnsrPrkgAssiRe:
        sig_name = "OutdLeOfSnsrPrkgAssiRe"
        sig_start_bit = 175
        update_id_bit = 142
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
        startbit = 175
        byte = 21
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SnsrFltFrntShoSideRi:
        sig_name = "SnsrFltFrntShoSideRi"
        sig_start_bit = 89
        update_id_bit = 144
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltAddCover_NoFault': 0, 'FltAddCover_Fault': 1, 'FltAddCover_Cover': 2}
        compute_method = None
        length = 2
        startbit = 89
        byte = 11
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class InsdRiOfSnsrPrkgAssiFrnt:
        sig_name = "InsdRiOfSnsrPrkgAssiFrnt"
        sig_start_bit = 103
        update_id_bit = 133
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
        startbit = 103
        byte = 12
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntLeOfSideDoor:
        sig_name = "FrntLeOfSideDoor"
        sig_start_bit = 31
        update_id_bit = 123
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

    class AudWarnOfSnsrParkAssiLePosn:
        sig_name = "AudWarnOfSnsrParkAssiLePosn"
        sig_start_bit = 12
        update_id_bit = 126
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoRequest': 0, 'Region1': 1, 'Region2': 2, 'Region3': 3, 'Region4': 4, 'Reserve': 5}
        compute_method = None
        length = 3
        startbit = 12
        byte = 1
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class AudWarnOfSnsrParkAssiRePosn:
        sig_name = "AudWarnOfSnsrParkAssiRePosn"
        sig_start_bit = 23
        update_id_bit = 125
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoRequest': 0, 'Region1': 1, 'Region2': 2, 'Region3': 3, 'Region4': 4, 'Reserve': 5}
        compute_method = None
        length = 3
        startbit = 23
        byte = 2
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class FrntRiOfSnsrOfPrkgAssiSide:
        sig_name = "FrntRiOfSnsrOfPrkgAssiSide"
        sig_start_bit = 55
        update_id_bit = 120
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

    class PrkgDstCtrlWarn:
        sig_name = "PrkgDstCtrlWarn"
        sig_start_bit = 9
        update_id_bit = 150
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WarningInd_NoWarning': 0, 'WarningInd_Warning': 1}
        compute_method = None
        length = 1
        startbit = 9
        byte = 1
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class SnsrFltReShoSideLe:
        sig_name = "SnsrFltReShoSideLe"
        sig_start_bit = 116
        update_id_bit = 158
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltAddCover_NoFault': 0, 'FltAddCover_Fault': 1, 'FltAddCover_Cover': 2}
        compute_method = None
        length = 2
        startbit = 116
        byte = 14
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class InsdSnsrFltFrntShoRi:
        sig_name = "InsdSnsrFltFrntShoRi"
        sig_start_bit = 61
        update_id_bit = 130
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltAddCover_NoFault': 0, 'FltAddCover_Fault': 1, 'FltAddCover_Cover': 2}
        compute_method = None
        length = 2
        startbit = 61
        byte = 7
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class SnsrFltReShoSideRi:
        sig_name = "SnsrFltReShoSideRi"
        sig_start_bit = 114
        update_id_bit = 157
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltAddCover_NoFault': 0, 'FltAddCover_Fault': 1, 'FltAddCover_Cover': 2}
        compute_method = None
        length = 2
        startbit = 114
        byte = 14
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class InsdRiOfSnsrPrkgAssiRe:
        sig_name = "InsdRiOfSnsrPrkgAssiRe"
        sig_start_bit = 111
        update_id_bit = 132
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
        startbit = 111
        byte = 13
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntLeOfSnsrOfPrkgAssiSide:
        sig_name = "FrntLeOfSnsrOfPrkgAssiSide"
        sig_start_bit = 39
        update_id_bit = 122
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

    class ReLeOfSnsrOfPrkgAssiSide:
        sig_name = "ReLeOfSnsrOfPrkgAssiSide"
        sig_start_bit = 207
        update_id_bit = 148
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
        startbit = 207
        byte = 25
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class AudWarnOfSnsrParkAssiRgtPosn:
        sig_name = "AudWarnOfSnsrParkAssiRgtPosn"
        sig_start_bit = 20
        update_id_bit = 124
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoRequest': 0, 'Region1': 1, 'Region2': 2, 'Region3': 3, 'Region4': 4, 'Reserve': 5}
        compute_method = None
        length = 3
        startbit = 20
        byte = 2
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class PrkgDstCtrlSts:
        sig_name = "PrkgDstCtrlSts"
        sig_start_bit = 95
        update_id_bit = 151
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PrkgDstCtrlSysSts_Off': 0, 'PrkgDstCtrlSysSts_Standby': 1, 'PrkgDstCtrlSysSts_FrontRearActive': 2, 'PrkgDstCtrlSysSts_FrontActive': 3, 'PrkgDstCtrlSysSts_RearActive': 4, 'PrkgDstCtrlSysSts_SystemFailure': 5, 'PrkgDstCtrlSysSts_Inhibited': 6, 'PrkgDstCtrlSysSts_Initialize': 7, 'PrkgDstCtrlSysSts_Covered': 8, 'PrkgDstCtrlSysSts_FrontActiveTrailerMode': 9, 'PrkgDstCtrlSysSts_Reserved1': 10, 'PrkgDstCtrlSysSts_Reserved2': 11, 'PrkgDstCtrlSysSts_Reserved3': 12, 'PrkgDstCtrlSysSts_Reserved4': 13, 'PrkgDstCtrlSysSts_Reserved5': 14, 'PrkgDstCtrlSysSts_Reserved6': 15}
        compute_method = None
        length = 4
        startbit = 95
        byte = 11
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class AudWarnLvOfSnsrParkAssiLe:
        sig_name = "AudWarnLvOfSnsrParkAssiLe"
        sig_start_bit = 5
        update_id_bit = 17
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BuzzerReqUSS_BuzzerOFF': 0, 'BuzzerReqUSS_BuzzerON_Keep': 1, 'BuzzerReqUSS_BuzzerON_4Hz': 2, 'BuzzerReqUSS_BuzzerON_2Hz': 3}
        compute_method = None
        length = 2
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class InsdSnsrFltReShoLe:
        sig_name = "InsdSnsrFltReShoLe"
        sig_start_bit = 59
        update_id_bit = 129
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltAddCover_NoFault': 0, 'FltAddCover_Fault': 1, 'FltAddCover_Cover': 2}
        compute_method = None
        length = 2
        startbit = 59
        byte = 7
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class OutdSnsrFltFrntShoLe:
        sig_name = "OutdSnsrFltFrntShoLe"
        sig_start_bit = 87
        update_id_bit = 139
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltAddCover_NoFault': 0, 'FltAddCover_Fault': 1, 'FltAddCover_Cover': 2}
        compute_method = None
        length = 2
        startbit = 87
        byte = 10
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class OutdSnsrFltFrntShoRi:
        sig_name = "OutdSnsrFltFrntShoRi"
        sig_start_bit = 85
        update_id_bit = 138
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltAddCover_NoFault': 0, 'FltAddCover_Fault': 1, 'FltAddCover_Cover': 2}
        compute_method = None
        length = 2
        startbit = 85
        byte = 10
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class InsdSnsrFltReShoRi:
        sig_name = "InsdSnsrFltReShoRi"
        sig_start_bit = 57
        update_id_bit = 128
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltAddCover_NoFault': 0, 'FltAddCover_Fault': 1, 'FltAddCover_Cover': 2}
        compute_method = None
        length = 2
        startbit = 57
        byte = 7
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class AudWarnLvOfSnsrParkAssiRe:
        sig_name = "AudWarnLvOfSnsrParkAssiRe"
        sig_start_bit = 3
        update_id_bit = 16
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BuzzerReqUSS_BuzzerOFF': 0, 'BuzzerReqUSS_BuzzerON_Keep': 1, 'BuzzerReqUSS_BuzzerON_4Hz': 2, 'BuzzerReqUSS_BuzzerON_2Hz': 3}
        compute_method = None
        length = 2
        startbit = 3
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class SnsrFltOfPrkgDstCtrl:
        sig_name = "SnsrFltOfPrkgDstCtrl"
        sig_start_bit = 119
        update_id_bit = 159
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SnsrFltOfPrkgDstCtrl2_NoFault': 0, 'SnsrFltOfPrkgDstCtrl2_Front_USS_Fault': 1, 'SnsrFltOfPrkgDstCtrl2_Rear_USS_Fault': 2, 'SnsrFltOfPrkgDstCtrl2_Front_and_Rear_USS_Fault': 3, 'SnsrFltOfPrkgDstCtrl2_Reserve1': 4, 'SnsrFltOfPrkgDstCtrl2_Reserve2': 5, 'SnsrFltOfPrkgDstCtrl2_Reserve3': 6, 'SnsrFltOfPrkgDstCtrl2_Reserve4': 7}
        compute_method = None
        length = 3
        startbit = 119
        byte = 14
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class InsdLeOfSnsrPrkgAssiRe:
        sig_name = "InsdLeOfSnsrPrkgAssiRe"
        sig_start_bit = 79
        update_id_bit = 134
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
        startbit = 79
        byte = 9
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SnsrFltFrntShoSideLe:
        sig_name = "SnsrFltFrntShoSideLe"
        sig_start_bit = 91
        update_id_bit = 145
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltAddCover_NoFault': 0, 'FltAddCover_Fault': 1, 'FltAddCover_Cover': 2}
        compute_method = None
        length = 2
        startbit = 91
        byte = 11
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class OutdSnsrFltReShoLe:
        sig_name = "OutdSnsrFltReShoLe"
        sig_start_bit = 83
        update_id_bit = 137
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltAddCover_NoFault': 0, 'FltAddCover_Fault': 1, 'FltAddCover_Cover': 2}
        compute_method = None
        length = 2
        startbit = 83
        byte = 10
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class AudWarnLvOfSnsrParkAssiFrnt:
        sig_name = "AudWarnLvOfSnsrParkAssiFrnt"
        sig_start_bit = 7
        update_id_bit = 8
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BuzzerReqUSS_BuzzerOFF': 0, 'BuzzerReqUSS_BuzzerON_Keep': 1, 'BuzzerReqUSS_BuzzerON_4Hz': 2, 'BuzzerReqUSS_BuzzerON_2Hz': 3}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class BgmADCANFDFr31:
    msg_name = "BgmADCANFDFr31"
    msg_id = 608
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 16
    tx_node = "BGM"
    rx_nodes = ['ACU']
    sig_group_dict = {'BGMMPUCtrlACU': ['BGMMPUCtrlACUByte0', 'BGMMPUCtrlACUByte1', 'BGMMPUCtrlACUByte2', 'BGMMPUCtrlACUByte3', 'BGMMPUCtrlACUByte4', 'BGMMPUCtrlACUByte5', 'BGMMPUCtrlACUByte6', 'BGMMPUCtrlACUByte7']}
    sig_group_dataid_dict = {}

    class BGMMPUCtrlACUByte0:
        sig_name = "BGMMPUCtrlACUByte0"
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

    class BGMMPUCtrlACUByte6:
        sig_name = "BGMMPUCtrlACUByte6"
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

    class BGMMPUCtrlACUByte1:
        sig_name = "BGMMPUCtrlACUByte1"
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

    class BGMMPUCtrlACUByte7:
        sig_name = "BGMMPUCtrlACUByte7"
        sig_start_bit = 71
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
        startbit = 71
        byte = 8
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BGMMPUCtrlACUByte2:
        sig_name = "BGMMPUCtrlACUByte2"
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

    class BGMMPUCtrlACUByte4:
        sig_name = "BGMMPUCtrlACUByte4"
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

    class BGMMPUCtrlACUByte5:
        sig_name = "BGMMPUCtrlACUByte5"
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

    class BGMMPUCtrlACU_UB:
        sig_name = "BGMMPUCtrlACU_UB"
        sig_start_bit = 1
        update_id_bit = 1
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
        startbit = 1
        byte = 0
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class BGMMPUCtrlACUByte3:
        sig_name = "BGMMPUCtrlACUByte3"
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


class BgmADCANFDFr22:
    msg_name = "BgmADCANFDFr22"
    msg_id = 514
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "BGM"
    rx_nodes = ['ACU']
    sig_group_dict = {'RearLeftRdrObj14': ['RearLeftRdrObj14ObjBoxCenterLat', 'RearLeftRdrObj14ObjBoxCenterLgt', 'RearLeftRdrObj14RdrObjChks', 'RearLeftRdrObj14RdrObjCntr', 'RearLeftRdrObj14RdrObjDx', 'RearLeftRdrObj14RdrObjDxStdDe', 'RearLeftRdrObj14RdrObjDy', 'RearLeftRdrObj14RdrObjDynProp', 'RearLeftRdrObj14RdrObjDyStdDe', 'RearLeftRdrObj14RdrObjExistProb', 'RearLeftRdrObj14RdrObjHeight', 'RearLeftRdrObj14RdrObjHeightStdDe', 'RearLeftRdrObj14RdrObjID', 'RearLeftRdrObj14RdrObjLifeCycle', 'RearLeftRdrObj14RdrObjPwr', 'RearLeftRdrObj14RdrObjVx', 'RearLeftRdrObj14RdrObjVxStdDe', 'RearLeftRdrObj14RdrObjVy', 'RearLeftRdrObj14RdrObjVyStdDe'], 'RearLeftRdrObj15': ['RearLeftRdrObj15ObjBoxCenterLat', 'RearLeftRdrObj15ObjBoxCenterLgt', 'RearLeftRdrObj15RdrObjChks', 'RearLeftRdrObj15RdrObjCntr', 'RearLeftRdrObj15RdrObjDx', 'RearLeftRdrObj15RdrObjDxStdDe', 'RearLeftRdrObj15RdrObjDy', 'RearLeftRdrObj15RdrObjDynProp', 'RearLeftRdrObj15RdrObjDyStdDe', 'RearLeftRdrObj15RdrObjExistProb', 'RearLeftRdrObj15RdrObjHeight', 'RearLeftRdrObj15RdrObjHeightStdDe', 'RearLeftRdrObj15RdrObjID', 'RearLeftRdrObj15RdrObjLifeCycle', 'RearLeftRdrObj15RdrObjPwr', 'RearLeftRdrObj15RdrObjVx', 'RearLeftRdrObj15RdrObjVxStdDe', 'RearLeftRdrObj15RdrObjVy', 'RearLeftRdrObj15RdrObjVyStdDe'], 'RearLeftRdrObj13': ['RearLeftRdrObj13ObjBoxCenterLat', 'RearLeftRdrObj13ObjBoxCenterLgt', 'RearLeftRdrObj13RdrObjChks', 'RearLeftRdrObj13RdrObjCntr', 'RearLeftRdrObj13RdrObjDx', 'RearLeftRdrObj13RdrObjDxStdDe', 'RearLeftRdrObj13RdrObjDy', 'RearLeftRdrObj13RdrObjDynProp', 'RearLeftRdrObj13RdrObjDyStdDe', 'RearLeftRdrObj13RdrObjExistProb', 'RearLeftRdrObj13RdrObjHeight', 'RearLeftRdrObj13RdrObjHeightStdDe', 'RearLeftRdrObj13RdrObjID', 'RearLeftRdrObj13RdrObjLifeCycle', 'RearLeftRdrObj13RdrObjPwr', 'RearLeftRdrObj13RdrObjVx', 'RearLeftRdrObj13RdrObjVxStdDe', 'RearLeftRdrObj13RdrObjVy', 'RearLeftRdrObj13RdrObjVyStdDe']}
    sig_group_dataid_dict = {}

    class RearLeftRdrObj14RdrObjExistProb:
        sig_name = "RearLeftRdrObj14RdrObjExistProb"
        sig_start_bit = 252
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 252
        bmuws_info = [(31, 0b00011111, 0b11100000, 5, 0), (32, 0b11111000, 0b00000111, 5, 3)]

    class RearLeftRdrObj15RdrObjHeight:
        sig_name = "RearLeftRdrObj15RdrObjHeight"
        sig_start_bit = 426
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 426
        bmuws_info = [(53, 0b00000111, 0b11111000, 3, 0), (54, 0b11111110, 0b00000001, 7, 1)]

    class RearLeftRdrObj13RdrObjDy:
        sig_name = "RearLeftRdrObj13RdrObjDy"
        sig_start_bit = 51
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 51
        bmuws_info = [(6, 0b00001111, 0b11110000, 4, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class RearLeftRdrObj13ObjBoxCenterLgt:
        sig_name = "RearLeftRdrObj13ObjBoxCenterLgt"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
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

    class RearLeftRdrObj14_UB:
        sig_name = "RearLeftRdrObj14_UB"
        sig_start_bit = 168
        update_id_bit = 168
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
        startbit = 168
        byte = 21
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class RearLeftRdrObj13RdrObjExistProb:
        sig_name = "RearLeftRdrObj13RdrObjExistProb"
        sig_start_bit = 76
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 76
        bmuws_info = [(9, 0b00011111, 0b11100000, 5, 0), (10, 0b11111000, 0b00000111, 5, 3)]

    class RearLeftRdrObj15RdrObjLifeCycle:
        sig_name = "RearLeftRdrObj15RdrObjLifeCycle"
        sig_start_bit = 448
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
        startbit = 448
        bmuws_info = [(56, 0b00000001, 0b11111110, 1, 0), (57, 0b11111100, 0b00000011, 6, 2)]

    class RearLeftRdrObj13RdrObjVx:
        sig_name = "RearLeftRdrObj13RdrObjVx"
        sig_start_bit = 121
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 121
        bmuws_info = [(15, 0b00000011, 0b11111100, 2, 0), (16, 0b11111111, 0b00000000, 8, 0), (17, 0b10000000, 0b01111111, 1, 7)]

    class RearLeftRdrObj14RdrObjPwr:
        sig_name = "RearLeftRdrObj14RdrObjPwr"
        sig_start_bit = 289
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 289
        bmuws_info = [(36, 0b00000011, 0b11111100, 2, 0), (37, 0b11111100, 0b00000011, 6, 2)]

    class RearLeftRdrObj13RdrObjDyStdDe:
        sig_name = "RearLeftRdrObj13RdrObjDyStdDe"
        sig_start_bit = 71
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 71
        bmuws_info = [(8, 0b11111111, 0b00000000, 8, 0), (9, 0b11100000, 0b00011111, 3, 5)]

    class RearLeftRdrObj15RdrObjDy:
        sig_name = "RearLeftRdrObj15RdrObjDy"
        sig_start_bit = 395
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 395
        bmuws_info = [(49, 0b00001111, 0b11110000, 4, 0), (50, 0b11111111, 0b00000000, 8, 0)]

    class RearLeftRdrObj13RdrObjHeight:
        sig_name = "RearLeftRdrObj13RdrObjHeight"
        sig_start_bit = 82
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 82
        bmuws_info = [(10, 0b00000111, 0b11111000, 3, 0), (11, 0b11111110, 0b00000001, 7, 1)]

    class RearLeftRdrObj15RdrObjHeightStdDe:
        sig_name = "RearLeftRdrObj15RdrObjHeightStdDe"
        sig_start_bit = 432
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 432
        bmuws_info = [(54, 0b00000001, 0b11111110, 1, 0), (55, 0b11111111, 0b00000000, 8, 0), (56, 0b10000000, 0b01111111, 1, 7)]

    class RearLeftRdrObj14RdrObjVx:
        sig_name = "RearLeftRdrObj14RdrObjVx"
        sig_start_bit = 297
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 297
        bmuws_info = [(37, 0b00000011, 0b11111100, 2, 0), (38, 0b11111111, 0b00000000, 8, 0), (39, 0b10000000, 0b01111111, 1, 7)]

    class RearLeftRdrObj14RdrObjLifeCycle:
        sig_name = "RearLeftRdrObj14RdrObjLifeCycle"
        sig_start_bit = 280
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
        startbit = 280
        bmuws_info = [(35, 0b00000001, 0b11111110, 1, 0), (36, 0b11111100, 0b00000011, 6, 2)]

    class RearLeftRdrObj13ObjBoxCenterLat:
        sig_name = "RearLeftRdrObj13ObjBoxCenterLat"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
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

    class RearLeftRdrObj13RdrObjPwr:
        sig_name = "RearLeftRdrObj13RdrObjPwr"
        sig_start_bit = 113
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 113
        bmuws_info = [(14, 0b00000011, 0b11111100, 2, 0), (15, 0b11111100, 0b00000011, 6, 2)]

    class RearLeftRdrObj15RdrObjChks:
        sig_name = "RearLeftRdrObj15RdrObjChks"
        sig_start_bit = 351
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
        startbit = 351
        byte = 43
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearLeftRdrObj13RdrObjChks:
        sig_name = "RearLeftRdrObj13RdrObjChks"
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

    class RearLeftRdrObj14RdrObjDy:
        sig_name = "RearLeftRdrObj14RdrObjDy"
        sig_start_bit = 227
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 227
        bmuws_info = [(28, 0b00001111, 0b11110000, 4, 0), (29, 0b11111111, 0b00000000, 8, 0)]

    class RearLeftRdrObj14RdrObjHeight:
        sig_name = "RearLeftRdrObj14RdrObjHeight"
        sig_start_bit = 258
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 258
        bmuws_info = [(32, 0b00000111, 0b11111000, 3, 0), (33, 0b11111110, 0b00000001, 7, 1)]

    class RearLeftRdrObj13RdrObjVy:
        sig_name = "RearLeftRdrObj13RdrObjVy"
        sig_start_bit = 148
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 148
        bmuws_info = [(18, 0b00011111, 0b11100000, 5, 0), (19, 0b11111100, 0b00000011, 6, 2)]

    class RearLeftRdrObj15RdrObjPwr:
        sig_name = "RearLeftRdrObj15RdrObjPwr"
        sig_start_bit = 457
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 457
        bmuws_info = [(57, 0b00000011, 0b11111100, 2, 0), (58, 0b11111100, 0b00000011, 6, 2)]

    class RearLeftRdrObj14ObjBoxCenterLgt:
        sig_name = "RearLeftRdrObj14ObjBoxCenterLgt"
        sig_start_bit = 207
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 207
        byte = 25
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearLeftRdrObj15RdrObjVx:
        sig_name = "RearLeftRdrObj15RdrObjVx"
        sig_start_bit = 465
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 465
        bmuws_info = [(58, 0b00000011, 0b11111100, 2, 0), (59, 0b11111111, 0b00000000, 8, 0), (60, 0b10000000, 0b01111111, 1, 7)]

    class RearLeftRdrObj14RdrObjDyStdDe:
        sig_name = "RearLeftRdrObj14RdrObjDyStdDe"
        sig_start_bit = 247
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 247
        bmuws_info = [(30, 0b11111111, 0b00000000, 8, 0), (31, 0b11100000, 0b00011111, 3, 5)]

    class RearLeftRdrObj15RdrObjVy:
        sig_name = "RearLeftRdrObj15RdrObjVy"
        sig_start_bit = 492
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 492
        bmuws_info = [(61, 0b00011111, 0b11100000, 5, 0), (62, 0b11111100, 0b00000011, 6, 2)]

    class RearLeftRdrObj15RdrObjCntr:
        sig_name = "RearLeftRdrObj15RdrObjCntr"
        sig_start_bit = 359
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
        startbit = 359
        byte = 44
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class RearLeftRdrObj14ObjBoxCenterLat:
        sig_name = "RearLeftRdrObj14ObjBoxCenterLat"
        sig_start_bit = 215
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 215
        byte = 26
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearLeftRdrObj14RdrObjDx:
        sig_name = "RearLeftRdrObj14RdrObjDx"
        sig_start_bit = 187
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 187
        bmuws_info = [(23, 0b00001111, 0b11110000, 4, 0), (24, 0b11111111, 0b00000000, 8, 0)]

    class RearLeftRdrObj14RdrObjVyStdDe:
        sig_name = "RearLeftRdrObj14RdrObjVyStdDe"
        sig_start_bit = 329
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 329
        bmuws_info = [(41, 0b00000011, 0b11111100, 2, 0), (42, 0b11111111, 0b00000000, 8, 0)]

    class RearLeftRdrObj15ObjBoxCenterLat:
        sig_name = "RearLeftRdrObj15ObjBoxCenterLat"
        sig_start_bit = 383
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 383
        byte = 47
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearLeftRdrObj15RdrObjExistProb:
        sig_name = "RearLeftRdrObj15RdrObjExistProb"
        sig_start_bit = 420
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 420
        bmuws_info = [(52, 0b00011111, 0b11100000, 5, 0), (53, 0b11111000, 0b00000111, 5, 3)]

    class RearLeftRdrObj14RdrObjHeightStdDe:
        sig_name = "RearLeftRdrObj14RdrObjHeightStdDe"
        sig_start_bit = 264
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 264
        bmuws_info = [(33, 0b00000001, 0b11111110, 1, 0), (34, 0b11111111, 0b00000000, 8, 0), (35, 0b10000000, 0b01111111, 1, 7)]

    class RearLeftRdrObj15ObjBoxCenterLgt:
        sig_name = "RearLeftRdrObj15ObjBoxCenterLgt"
        sig_start_bit = 375
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 375
        byte = 46
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearLeftRdrObj13RdrObjCntr:
        sig_name = "RearLeftRdrObj13RdrObjCntr"
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

    class RearLeftRdrObj15RdrObjDx:
        sig_name = "RearLeftRdrObj15RdrObjDx"
        sig_start_bit = 355
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 355
        bmuws_info = [(44, 0b00001111, 0b11110000, 4, 0), (45, 0b11111111, 0b00000000, 8, 0)]

    class RearLeftRdrObj13RdrObjHeightStdDe:
        sig_name = "RearLeftRdrObj13RdrObjHeightStdDe"
        sig_start_bit = 88
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 88
        bmuws_info = [(11, 0b00000001, 0b11111110, 1, 0), (12, 0b11111111, 0b00000000, 8, 0), (13, 0b10000000, 0b01111111, 1, 7)]

    class RearLeftRdrObj13RdrObjDynProp:
        sig_name = "RearLeftRdrObj13RdrObjDynProp"
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
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class RearLeftRdrObj15RdrObjDynProp:
        sig_name = "RearLeftRdrObj15RdrObjDynProp"
        sig_start_bit = 396
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 396
        byte = 49
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class RearLeftRdrObj13RdrObjVyStdDe:
        sig_name = "RearLeftRdrObj13RdrObjVyStdDe"
        sig_start_bit = 153
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 153
        bmuws_info = [(19, 0b00000011, 0b11111100, 2, 0), (20, 0b11111111, 0b00000000, 8, 0)]

    class RearLeftRdrObj14RdrObjDxStdDe:
        sig_name = "RearLeftRdrObj14RdrObjDxStdDe"
        sig_start_bit = 223
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 223
        bmuws_info = [(27, 0b11111111, 0b00000000, 8, 0), (28, 0b11100000, 0b00011111, 3, 5)]

    class RearLeftRdrObj13RdrObjLifeCycle:
        sig_name = "RearLeftRdrObj13RdrObjLifeCycle"
        sig_start_bit = 104
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
        startbit = 104
        bmuws_info = [(13, 0b00000001, 0b11111110, 1, 0), (14, 0b11111100, 0b00000011, 6, 2)]

    class RearLeftRdrObj14RdrObjID:
        sig_name = "RearLeftRdrObj14RdrObjID"
        sig_start_bit = 286
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 286
        byte = 35
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class RearLeftRdrObj14RdrObjCntr:
        sig_name = "RearLeftRdrObj14RdrObjCntr"
        sig_start_bit = 191
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
        startbit = 191
        byte = 23
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class RearLeftRdrObj15_UB:
        sig_name = "RearLeftRdrObj15_UB"
        sig_start_bit = 171
        update_id_bit = 171
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
        startbit = 171
        byte = 21
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class RearLeftRdrObj13RdrObjVxStdDe:
        sig_name = "RearLeftRdrObj13RdrObjVxStdDe"
        sig_start_bit = 142
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 142
        bmuws_info = [(17, 0b01111111, 0b10000000, 7, 0), (18, 0b11100000, 0b00011111, 3, 5)]

    class RearLeftRdrObj15RdrObjDyStdDe:
        sig_name = "RearLeftRdrObj15RdrObjDyStdDe"
        sig_start_bit = 415
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 415
        bmuws_info = [(51, 0b11111111, 0b00000000, 8, 0), (52, 0b11100000, 0b00011111, 3, 5)]

    class RearLeftRdrObj14RdrObjChks:
        sig_name = "RearLeftRdrObj14RdrObjChks"
        sig_start_bit = 183
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
        startbit = 183
        byte = 22
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearLeftRdrObj14RdrObjVy:
        sig_name = "RearLeftRdrObj14RdrObjVy"
        sig_start_bit = 324
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 324
        bmuws_info = [(40, 0b00011111, 0b11100000, 5, 0), (41, 0b11111100, 0b00000011, 6, 2)]

    class RearLeftRdrObj13RdrObjDx:
        sig_name = "RearLeftRdrObj13RdrObjDx"
        sig_start_bit = 11
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 11
        bmuws_info = [(1, 0b00001111, 0b11110000, 4, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class RearLeftRdrObj13RdrObjID:
        sig_name = "RearLeftRdrObj13RdrObjID"
        sig_start_bit = 110
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 110
        byte = 13
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class RearLeftRdrObj15RdrObjVxStdDe:
        sig_name = "RearLeftRdrObj15RdrObjVxStdDe"
        sig_start_bit = 486
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 486
        bmuws_info = [(60, 0b01111111, 0b10000000, 7, 0), (61, 0b11100000, 0b00011111, 3, 5)]

    class RearLeftRdrObj15RdrObjID:
        sig_name = "RearLeftRdrObj15RdrObjID"
        sig_start_bit = 454
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 454
        byte = 56
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class RearLeftRdrObj14RdrObjDynProp:
        sig_name = "RearLeftRdrObj14RdrObjDynProp"
        sig_start_bit = 228
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 228
        byte = 28
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class RearLeftRdrObj14RdrObjVxStdDe:
        sig_name = "RearLeftRdrObj14RdrObjVxStdDe"
        sig_start_bit = 318
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 318
        bmuws_info = [(39, 0b01111111, 0b10000000, 7, 0), (40, 0b11100000, 0b00011111, 3, 5)]

    class RearLeftRdrObj13RdrObjDxStdDe:
        sig_name = "RearLeftRdrObj13RdrObjDxStdDe"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11100000, 0b00011111, 3, 5)]

    class RearLeftRdrObj15RdrObjDxStdDe:
        sig_name = "RearLeftRdrObj15RdrObjDxStdDe"
        sig_start_bit = 391
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 391
        bmuws_info = [(48, 0b11111111, 0b00000000, 8, 0), (49, 0b11100000, 0b00011111, 3, 5)]

    class RearLeftRdrObj15RdrObjVyStdDe:
        sig_name = "RearLeftRdrObj15RdrObjVyStdDe"
        sig_start_bit = 497
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 497
        bmuws_info = [(62, 0b00000011, 0b11111100, 2, 0), (63, 0b11111111, 0b00000000, 8, 0)]

    class RearLeftRdrObj13_UB:
        sig_name = "RearLeftRdrObj13_UB"
        sig_start_bit = 175
        update_id_bit = 175
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
        startbit = 175
        byte = 21
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7


class AcuADCANFDFr04:
    msg_name = "AcuADCANFDFr04"
    msg_id = 305
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.45
    msg_length = 64
    tx_node = "ACU"
    rx_nodes = ['S2SReceiver']
    sig_group_dict = {'GNSSPosnOnCAN': ['GNSSPosnOnCANCntr', 'GNSSPosnOnCANDay1', 'GNSSPosnOnCANDownVelocity', 'GNSSPosnOnCANEstimatedDownVelocityPrecision', 'GNSSPosnOnCANEstimatedEastVelocityPrecision', 'GNSSPosnOnCANEstimatedEllipsoidPrecision', 'GNSSPosnOnCANEstimatedHeadingPrecision', 'GNSSPosnOnCANEstimatedLatPrecision', 'GNSSPosnOnCANEstimatedLgtPrecision', 'GNSSPosnOnCANEstimatedNorthVelocityPrecision', 'GNSSPosnOnCANGNSSCN0', 'GNSSPosnOnCANGNSSErrorCode', 'GNSSPosnOnCANGNSSStatus', 'GNSSPosnOnCANHDOP', 'GNSSPosnOnCANHeadingFromGNSS', 'GNSSPosnOnCANHr1', 'GNSSPosnOnCANLeapSecond', 'GNSSPosnOnCANMins1', 'GNSSPosnOnCANMth1', 'GNSSPosnOnCANPDOP', 'GNSSPosnOnCANPosnEllipsoid', 'GNSSPosnOnCANPosnLat', 'GNSSPosnOnCANPosnLgt', 'GNSSPosnOnCANSatellitesInUse', 'GNSSPosnOnCANSatellitesInView', 'GNSSPosnOnCANTiFormiliSec', 'GNSSPosnOnCANTrueEastVelocity', 'GNSSPosnOnCANTrueNorthVelocity', 'GNSSPosnOnCANYr1']}
    sig_group_dataid_dict = {}

    class GNSSPosnOnCANTiFormiliSec:
        sig_name = "GNSSPosnOnCANTiFormiliSec"
        sig_start_bit = 343
        update_id_bit = None
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "SCALE_LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 343
        bmuws_info = [(42, 0b11111111, 0b00000000, 8, 0), (43, 0b11111111, 0b00000000, 8, 0)]

    class GNSSPosnOnCANEstimatedEllipsoidPrecision:
        sig_name = "GNSSPosnOnCANEstimatedEllipsoidPrecision"
        sig_start_bit = 67
        update_id_bit = None
        sig_length = 20
        sig_value_factor = 0.001
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 999999
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 20
        startbit = 67
        bmuws_info = [(8, 0b00001111, 0b11110000, 4, 0), (9, 0b11111111, 0b00000000, 8, 0), (10, 0b11111111, 0b00000000, 8, 0)]

    class GNSSPosnOnCANLeapSecond:
        sig_name = "GNSSPosnOnCANLeapSecond"
        sig_start_bit = 223
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 223
        byte = 27
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class GNSSPosnOnCANGNSSErrorCode:
        sig_name = "GNSSPosnOnCANGNSSErrorCode"
        sig_start_bit = 183
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
        startbit = 183
        byte = 22
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class GNSSPosnOnCANMins1:
        sig_name = "GNSSPosnOnCANMins1"
        sig_start_bit = 239
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 239
        byte = 29
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class GNSSPosnOnCANMth1:
        sig_name = "GNSSPosnOnCANMth1"
        sig_start_bit = 315
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 315
        byte = 39
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class GNSSPosnOnCANTrueEastVelocity:
        sig_name = "GNSSPosnOnCANTrueEastVelocity"
        sig_start_bit = 359
        update_id_bit = None
        sig_length = 17
        sig_value_factor = 0.001
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 100000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 17
        startbit = 359
        bmuws_info = [(44, 0b11111111, 0b00000000, 8, 0), (45, 0b11111111, 0b00000000, 8, 0), (46, 0b10000000, 0b01111111, 1, 7)]

    class GNSSPosnOnCANHeadingFromGNSS:
        sig_name = "GNSSPosnOnCANHeadingFromGNSS"
        sig_start_bit = 207
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 0.01
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 35999
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 207
        bmuws_info = [(25, 0b11111111, 0b00000000, 8, 0), (26, 0b11111111, 0b00000000, 8, 0)]

    class GNSSPosnOnCANDay1:
        sig_name = "GNSSPosnOnCANDay1"
        sig_start_bit = 36
        update_id_bit = None
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 36
        byte = 4
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class GNSSPosnOnCANPDOP:
        sig_name = "GNSSPosnOnCANPDOP"
        sig_start_bit = 231
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 231
        byte = 28
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class GNSSPosnOnCANEstimatedLgtPrecision:
        sig_name = "GNSSPosnOnCANEstimatedLgtPrecision"
        sig_start_bit = 113
        update_id_bit = None
        sig_length = 31
        sig_value_factor = 2.7777777777777776e-07
        sig_value_offset = 0.0
        sig_value_min = -648000000
        sig_value_max = 648000000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 31
        startbit = 113
        bmuws_info = [(14, 0b00000011, 0b11111100, 2, 0), (15, 0b11111111, 0b00000000, 8, 0), (16, 0b11111111, 0b00000000, 8, 0), (17, 0b11111111, 0b00000000, 8, 0), (18, 0b11111000, 0b00000111, 5, 3)]

    class GNSSPosnOnCANSatellitesInView:
        sig_name = "GNSSPosnOnCANSatellitesInView"
        sig_start_bit = 335
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
        startbit = 335
        byte = 41
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class GNSSPosnOnCANTrueNorthVelocity:
        sig_name = "GNSSPosnOnCANTrueNorthVelocity"
        sig_start_bit = 374
        update_id_bit = None
        sig_length = 17
        sig_value_factor = 0.001
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 100000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 17
        startbit = 374
        bmuws_info = [(46, 0b01111111, 0b10000000, 7, 0), (47, 0b11111111, 0b00000000, 8, 0), (48, 0b11000000, 0b00111111, 2, 6)]

    class GNSSPosnOnCANEstimatedNorthVelocityPrecision:
        sig_name = "GNSSPosnOnCANEstimatedNorthVelocityPrecision"
        sig_start_bit = 146
        update_id_bit = None
        sig_length = 14
        sig_value_factor = 0.001
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 9999
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 14
        startbit = 146
        bmuws_info = [(18, 0b00000111, 0b11111000, 3, 0), (19, 0b11111111, 0b00000000, 8, 0), (20, 0b11100000, 0b00011111, 3, 5)]

    class GNSSPosnOnCANEstimatedEastVelocityPrecision:
        sig_name = "GNSSPosnOnCANEstimatedEastVelocityPrecision"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 14
        sig_value_factor = 0.001
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 9999
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 14
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111100, 0b00000011, 6, 2)]

    class GNSSPosnOnCANPosnEllipsoid:
        sig_name = "GNSSPosnOnCANPosnEllipsoid"
        sig_start_bit = 233
        update_id_bit = None
        sig_length = 17
        sig_value_factor = 0.1
        sig_value_offset = -900.0
        sig_value_min = 0
        sig_value_max = 99000
        sig_byteorder = "Motorola"
        sig_value_init = 99000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 17
        startbit = 233
        bmuws_info = [(29, 0b00000011, 0b11111100, 2, 0), (30, 0b11111111, 0b00000000, 8, 0), (31, 0b11111110, 0b00000001, 7, 1)]

    class GNSSPosnOnCANHDOP:
        sig_name = "GNSSPosnOnCANHDOP"
        sig_start_bit = 199
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 199
        byte = 24
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class GNSSPosnOnCANPosnLgt:
        sig_name = "GNSSPosnOnCANPosnLgt"
        sig_start_bit = 282
        update_id_bit = None
        sig_length = 31
        sig_value_factor = 2.7777777777777776e-07
        sig_value_offset = 0.0
        sig_value_min = -648000000
        sig_value_max = 648000000
        sig_byteorder = "Motorola"
        sig_value_init = 648000000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 31
        startbit = 282
        bmuws_info = [(35, 0b00000111, 0b11111000, 3, 0), (36, 0b11111111, 0b00000000, 8, 0), (37, 0b11111111, 0b00000000, 8, 0), (38, 0b11111111, 0b00000000, 8, 0), (39, 0b11110000, 0b00001111, 4, 4)]

    class GNSSPosnOnCANDownVelocity:
        sig_name = "GNSSPosnOnCANDownVelocity"
        sig_start_bit = 3
        update_id_bit = None
        sig_length = 17
        sig_value_factor = 0.001
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 100000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 17
        startbit = 3
        bmuws_info = [(0, 0b00001111, 0b11110000, 4, 0), (1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111000, 0b00000111, 5, 3)]

    class GNSSPosnOnCANSatellitesInUse:
        sig_name = "GNSSPosnOnCANSatellitesInUse"
        sig_start_bit = 327
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
        startbit = 327
        byte = 40
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class GNSSPosnOnCANEstimatedLatPrecision:
        sig_name = "GNSSPosnOnCANEstimatedLatPrecision"
        sig_start_bit = 95
        update_id_bit = None
        sig_length = 30
        sig_value_factor = 2.7777777777777776e-07
        sig_value_offset = 0.0
        sig_value_min = -324000000
        sig_value_max = 324000000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 30
        startbit = 95
        bmuws_info = [(11, 0b11111111, 0b00000000, 8, 0), (12, 0b11111111, 0b00000000, 8, 0), (13, 0b11111111, 0b00000000, 8, 0), (14, 0b11111100, 0b00000011, 6, 2)]

    class GNSSPosnOnCAN_UB:
        sig_name = "GNSSPosnOnCAN_UB"
        sig_start_bit = 398
        update_id_bit = 398
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
        startbit = 398
        byte = 49
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class GNSSPosnOnCANYr1:
        sig_name = "GNSSPosnOnCANYr1"
        sig_start_bit = 389
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
        startbit = 389
        bmuws_info = [(48, 0b00111111, 0b11000000, 6, 0), (49, 0b10000000, 0b01111111, 1, 7)]

    class GNSSPosnOnCANEstimatedHeadingPrecision:
        sig_name = "GNSSPosnOnCANEstimatedHeadingPrecision"
        sig_start_bit = 49
        update_id_bit = None
        sig_length = 14
        sig_value_factor = 0.001
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 9999
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 14
        startbit = 49
        bmuws_info = [(6, 0b00000011, 0b11111100, 2, 0), (7, 0b11111111, 0b00000000, 8, 0), (8, 0b11110000, 0b00001111, 4, 4)]

    class GNSSPosnOnCANEstimatedDownVelocityPrecision:
        sig_name = "GNSSPosnOnCANEstimatedDownVelocityPrecision"
        sig_start_bit = 18
        update_id_bit = None
        sig_length = 14
        sig_value_factor = 0.001
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 9999
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 14
        startbit = 18
        bmuws_info = [(2, 0b00000111, 0b11111000, 3, 0), (3, 0b11111111, 0b00000000, 8, 0), (4, 0b11100000, 0b00011111, 3, 5)]

    class GNSSPosnOnCANCntr:
        sig_name = "GNSSPosnOnCANCntr"
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

    class GNSSPosnOnCANGNSSStatus:
        sig_name = "GNSSPosnOnCANGNSSStatus"
        sig_start_bit = 191
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 8
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GNSSStatus_Invalid_Default': 0, 'GNSSStatus_GPS_FIX': 1, 'GNSSStatus_DGPS_FIX': 2, 'GNSSStatus_PPS_FIX': 3, 'GNSSStatus_RTK_FIX': 4, 'GNSSStatus_RTK_FLOAT': 5, 'GNSSStatus_ESTIMATED_DEAD_RECKONING': 6, 'GNSSStatus_MANUAL_INPUT_MODE': 7, 'GNSSStatus_SIMULATOR_MODE': 8}
        compute_method = None
        length = 8
        startbit = 191
        byte = 23
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class GNSSPosnOnCANGNSSCN0:
        sig_name = "GNSSPosnOnCANGNSSCN0"
        sig_start_bit = 175
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.2
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 175
        byte = 21
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class GNSSPosnOnCANHr1:
        sig_name = "GNSSPosnOnCANHr1"
        sig_start_bit = 164
        update_id_bit = None
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 164
        byte = 20
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class GNSSPosnOnCANPosnLat:
        sig_name = "GNSSPosnOnCANPosnLat"
        sig_start_bit = 248
        update_id_bit = None
        sig_length = 30
        sig_value_factor = 2.7777777777777776e-07
        sig_value_offset = 0.0
        sig_value_min = -324000000
        sig_value_max = 324000000
        sig_byteorder = "Motorola"
        sig_value_init = 324000000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 30
        startbit = 248
        bmuws_info = [(31, 0b00000001, 0b11111110, 1, 0), (32, 0b11111111, 0b00000000, 8, 0), (33, 0b11111111, 0b00000000, 8, 0), (34, 0b11111111, 0b00000000, 8, 0), (35, 0b11111000, 0b00000111, 5, 3)]


class BgmADCANFDFr11:
    msg_name = "BgmADCANFDFr11"
    msg_id = 501
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "BGM"
    rx_nodes = ['ACU']
    sig_group_dict = {'FrntLeftRdrSync': ['FrntLeftRdrSyncRdrObjTimeStampNSec', 'FrntLeftRdrSyncRdrObjTimeStampSec', 'FrntLeftRdrSyncRdrSyncChks', 'FrntLeftRdrSyncRdrSyncCntr'], 'FrntLeftRdrObj16': ['FrntLeftRdrObj16ObjBoxCenterLat', 'FrntLeftRdrObj16ObjBoxCenterLgt', 'FrntLeftRdrObj16RdrObjChks', 'FrntLeftRdrObj16RdrObjCntr', 'FrntLeftRdrObj16RdrObjDx', 'FrntLeftRdrObj16RdrObjDxStdDe', 'FrntLeftRdrObj16RdrObjDy', 'FrntLeftRdrObj16RdrObjDynProp', 'FrntLeftRdrObj16RdrObjDyStdDe', 'FrntLeftRdrObj16RdrObjExistProb', 'FrntLeftRdrObj16RdrObjHeight', 'FrntLeftRdrObj16RdrObjHeightStdDe', 'FrntLeftRdrObj16RdrObjID', 'FrntLeftRdrObj16RdrObjLifeCycle', 'FrntLeftRdrObj16RdrObjPwr', 'FrntLeftRdrObj16RdrObjVx', 'FrntLeftRdrObj16RdrObjVxStdDe', 'FrntLeftRdrObj16RdrObjVy', 'FrntLeftRdrObj16RdrObjVyStdDe']}
    sig_group_dataid_dict = {}

    class FrntLeftRdrObj16RdrObjHeightStdDe:
        sig_name = "FrntLeftRdrObj16RdrObjHeightStdDe"
        sig_start_bit = 88
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 88
        bmuws_info = [(11, 0b00000001, 0b11111110, 1, 0), (12, 0b11111111, 0b00000000, 8, 0), (13, 0b10000000, 0b01111111, 1, 7)]

    class FrntLeftRdrSyncRdrSyncCntr:
        sig_name = "FrntLeftRdrSyncRdrSyncCntr"
        sig_start_bit = 195
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
        startbit = 195
        byte = 24
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class FrntLeftRdrObj16ObjBoxCenterLat:
        sig_name = "FrntLeftRdrObj16ObjBoxCenterLat"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
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

    class FrntLeftRdrObj16RdrObjDy:
        sig_name = "FrntLeftRdrObj16RdrObjDy"
        sig_start_bit = 51
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 51
        bmuws_info = [(6, 0b00001111, 0b11110000, 4, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeftRdrFault:
        sig_name = "FrntLeftRdrFault"
        sig_start_bit = 171
        update_id_bit = 169
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
        startbit = 171
        byte = 21
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class FrntLeftRdrObj16RdrObjPwr:
        sig_name = "FrntLeftRdrObj16RdrObjPwr"
        sig_start_bit = 113
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 113
        bmuws_info = [(14, 0b00000011, 0b11111100, 2, 0), (15, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeftRdrObj16RdrObjID:
        sig_name = "FrntLeftRdrObj16RdrObjID"
        sig_start_bit = 110
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 110
        byte = 13
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class FrntLeftRdrSync_UB:
        sig_name = "FrntLeftRdrSync_UB"
        sig_start_bit = 271
        update_id_bit = 271
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
        startbit = 271
        byte = 33
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class FrntLeftRdrObj16RdrObjDynProp:
        sig_name = "FrntLeftRdrObj16RdrObjDynProp"
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
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class FrntLeftRdrObj16RdrObjVx:
        sig_name = "FrntLeftRdrObj16RdrObjVx"
        sig_start_bit = 121
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 121
        bmuws_info = [(15, 0b00000011, 0b11111100, 2, 0), (16, 0b11111111, 0b00000000, 8, 0), (17, 0b10000000, 0b01111111, 1, 7)]

    class FrntLeftRdrObj16RdrObjExistProb:
        sig_name = "FrntLeftRdrObj16RdrObjExistProb"
        sig_start_bit = 76
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 76
        bmuws_info = [(9, 0b00011111, 0b11100000, 5, 0), (10, 0b11111000, 0b00000111, 5, 3)]

    class FrntLeftRdrObj16RdrObjVy:
        sig_name = "FrntLeftRdrObj16RdrObjVy"
        sig_start_bit = 148
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 148
        bmuws_info = [(18, 0b00011111, 0b11100000, 5, 0), (19, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeftRdrObj16RdrObjDyStdDe:
        sig_name = "FrntLeftRdrObj16RdrObjDyStdDe"
        sig_start_bit = 71
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 71
        bmuws_info = [(8, 0b11111111, 0b00000000, 8, 0), (9, 0b11100000, 0b00011111, 3, 5)]

    class FrntLeftRdrSyncRdrObjTimeStampNSec:
        sig_name = "FrntLeftRdrSyncRdrObjTimeStampNSec"
        sig_start_bit = 207
        update_id_bit = None
        sig_length = 32
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4294967295
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 32
        startbit = 207
        bmuws_info = [(25, 0b11111111, 0b00000000, 8, 0), (26, 0b11111111, 0b00000000, 8, 0), (27, 0b11111111, 0b00000000, 8, 0), (28, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeftRdrObj16RdrObjLifeCycle:
        sig_name = "FrntLeftRdrObj16RdrObjLifeCycle"
        sig_start_bit = 104
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
        startbit = 104
        bmuws_info = [(13, 0b00000001, 0b11111110, 1, 0), (14, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeftRdrObj16RdrObjChks:
        sig_name = "FrntLeftRdrObj16RdrObjChks"
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

    class FrntLeftRdrObj16RdrObjDxStdDe:
        sig_name = "FrntLeftRdrObj16RdrObjDxStdDe"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11100000, 0b00011111, 3, 5)]

    class FrntLeftRdrObj16RdrObjCntr:
        sig_name = "FrntLeftRdrObj16RdrObjCntr"
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

    class FrntLeftRdrObj16RdrObjHeight:
        sig_name = "FrntLeftRdrObj16RdrObjHeight"
        sig_start_bit = 82
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 82
        bmuws_info = [(10, 0b00000111, 0b11111000, 3, 0), (11, 0b11111110, 0b00000001, 7, 1)]

    class FrntLeftRdrObj16ObjBoxCenterLgt:
        sig_name = "FrntLeftRdrObj16ObjBoxCenterLgt"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
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

    class FrntLeftRdrSyncRdrObjTimeStampSec:
        sig_name = "FrntLeftRdrSyncRdrObjTimeStampSec"
        sig_start_bit = 239
        update_id_bit = None
        sig_length = 32
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4294967295
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 32
        startbit = 239
        bmuws_info = [(29, 0b11111111, 0b00000000, 8, 0), (30, 0b11111111, 0b00000000, 8, 0), (31, 0b11111111, 0b00000000, 8, 0), (32, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeftRdrObj16RdrObjVxStdDe:
        sig_name = "FrntLeftRdrObj16RdrObjVxStdDe"
        sig_start_bit = 142
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 142
        bmuws_info = [(17, 0b01111111, 0b10000000, 7, 0), (18, 0b11100000, 0b00011111, 3, 5)]

    class FrntLeftRdrObj16RdrObjDx:
        sig_name = "FrntLeftRdrObj16RdrObjDx"
        sig_start_bit = 11
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 11
        bmuws_info = [(1, 0b00001111, 0b11110000, 4, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeftRdrSyncRdrSyncChks:
        sig_name = "FrntLeftRdrSyncRdrSyncChks"
        sig_start_bit = 191
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
        startbit = 191
        byte = 23
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntLeftRdrObj16_UB:
        sig_name = "FrntLeftRdrObj16_UB"
        sig_start_bit = 175
        update_id_bit = 175
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
        startbit = 175
        byte = 21
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class FrntLeftRdrObj16RdrObjVyStdDe:
        sig_name = "FrntLeftRdrObj16RdrObjVyStdDe"
        sig_start_bit = 153
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 153
        bmuws_info = [(19, 0b00000011, 0b11111100, 2, 0), (20, 0b11111111, 0b00000000, 8, 0)]


class AcuADCANFDFr14:
    msg_name = "AcuADCANFDFr14"
    msg_id = 272
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "ACU"
    rx_nodes = ['BGM']
    sig_group_dict = {'ObjInfo2': ['ObjInfo2ObjConfidenceLvl', 'ObjInfo2ObjDst1', 'ObjInfo2ObjDst2', 'ObjInfo2ObjHei', 'ObjInfo2ObjSide', 'ObjInfo2ObjTypMai']}
    sig_group_dataid_dict = {}

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
        update_id_bit = None
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

    class SumRoadTyp:
        sig_name = "SumRoadTyp"
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
        sig_value_table = {'SumRoadTyp_None': 0, 'SumRoadTyp_Smooth': 1, 'SumRoadTyp_Medium': 2, 'SumRoadTyp_Rough': 3, 'SumRoadTyp_Reserved_0': 4, 'SumRoadTyp_Reserved_1': 5, 'SumRoadTyp_Reserved_2': 6, 'SumRoadTyp_Reserved_3': 7, 'SumRoadTyp_Reserved_4': 8, 'SumRoadTyp_Reserved_5': 9, 'SumRoadTyp_Reserved_6': 10, 'SumRoadTyp_Reserved_7': 11, 'SumRoadTyp_Reserved_8': 12, 'SumRoadTyp_Reserved_9': 13, 'SumRoadTyp_Reserved_10': 14, 'SumRoadTyp_Reserved_11': 15}
        compute_method = None
        length = 4
        startbit = 55
        byte = 6
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

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


class BgmADCANFDFr10:
    msg_name = "BgmADCANFDFr10"
    msg_id = 500
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "BGM"
    rx_nodes = ['ACU']
    sig_group_dict = {'FrntLeftRdrObj14': ['FrntLeftRdrObj14ObjBoxCenterLat', 'FrntLeftRdrObj14ObjBoxCenterLgt', 'FrntLeftRdrObj14RdrObjChks', 'FrntLeftRdrObj14RdrObjCntr', 'FrntLeftRdrObj14RdrObjDx', 'FrntLeftRdrObj14RdrObjDxStdDe', 'FrntLeftRdrObj14RdrObjDy', 'FrntLeftRdrObj14RdrObjDynProp', 'FrntLeftRdrObj14RdrObjDyStdDe', 'FrntLeftRdrObj14RdrObjExistProb', 'FrntLeftRdrObj14RdrObjHeight', 'FrntLeftRdrObj14RdrObjHeightStdDe', 'FrntLeftRdrObj14RdrObjID', 'FrntLeftRdrObj14RdrObjLifeCycle', 'FrntLeftRdrObj14RdrObjPwr', 'FrntLeftRdrObj14RdrObjVx', 'FrntLeftRdrObj14RdrObjVxStdDe', 'FrntLeftRdrObj14RdrObjVy', 'FrntLeftRdrObj14RdrObjVyStdDe'], 'FrntLeftRdrObj15': ['FrntLeftRdrObj15ObjBoxCenterLat', 'FrntLeftRdrObj15ObjBoxCenterLgt', 'FrntLeftRdrObj15RdrObjChks', 'FrntLeftRdrObj15RdrObjCntr', 'FrntLeftRdrObj15RdrObjDx', 'FrntLeftRdrObj15RdrObjDxStdDe', 'FrntLeftRdrObj15RdrObjDy', 'FrntLeftRdrObj15RdrObjDynProp', 'FrntLeftRdrObj15RdrObjDyStdDe', 'FrntLeftRdrObj15RdrObjExistProb', 'FrntLeftRdrObj15RdrObjHeight', 'FrntLeftRdrObj15RdrObjHeightStdDe', 'FrntLeftRdrObj15RdrObjID', 'FrntLeftRdrObj15RdrObjLifeCycle', 'FrntLeftRdrObj15RdrObjPwr', 'FrntLeftRdrObj15RdrObjVx', 'FrntLeftRdrObj15RdrObjVxStdDe', 'FrntLeftRdrObj15RdrObjVy', 'FrntLeftRdrObj15RdrObjVyStdDe'], 'FrntLeftRdrObj13': ['FrntLeftRdrObj13ObjBoxCenterLat', 'FrntLeftRdrObj13ObjBoxCenterLgt', 'FrntLeftRdrObj13RdrObjChks', 'FrntLeftRdrObj13RdrObjCntr', 'FrntLeftRdrObj13RdrObjDx', 'FrntLeftRdrObj13RdrObjDxStdDe', 'FrntLeftRdrObj13RdrObjDy', 'FrntLeftRdrObj13RdrObjDynProp', 'FrntLeftRdrObj13RdrObjDyStdDe', 'FrntLeftRdrObj13RdrObjExistProb', 'FrntLeftRdrObj13RdrObjHeight', 'FrntLeftRdrObj13RdrObjHeightStdDe', 'FrntLeftRdrObj13RdrObjID', 'FrntLeftRdrObj13RdrObjLifeCycle', 'FrntLeftRdrObj13RdrObjPwr', 'FrntLeftRdrObj13RdrObjVx', 'FrntLeftRdrObj13RdrObjVxStdDe', 'FrntLeftRdrObj13RdrObjVy', 'FrntLeftRdrObj13RdrObjVyStdDe']}
    sig_group_dataid_dict = {}

    class FrntLeftRdrObj13RdrObjLifeCycle:
        sig_name = "FrntLeftRdrObj13RdrObjLifeCycle"
        sig_start_bit = 104
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
        startbit = 104
        bmuws_info = [(13, 0b00000001, 0b11111110, 1, 0), (14, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeftRdrObj15RdrObjChks:
        sig_name = "FrntLeftRdrObj15RdrObjChks"
        sig_start_bit = 351
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
        startbit = 351
        byte = 43
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntLeftRdrObj13RdrObjCntr:
        sig_name = "FrntLeftRdrObj13RdrObjCntr"
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

    class FrntLeftRdrObj15ObjBoxCenterLgt:
        sig_name = "FrntLeftRdrObj15ObjBoxCenterLgt"
        sig_start_bit = 375
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 375
        byte = 46
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntLeftRdrObj15RdrObjDx:
        sig_name = "FrntLeftRdrObj15RdrObjDx"
        sig_start_bit = 355
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 355
        bmuws_info = [(44, 0b00001111, 0b11110000, 4, 0), (45, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeftRdrObj15RdrObjDxStdDe:
        sig_name = "FrntLeftRdrObj15RdrObjDxStdDe"
        sig_start_bit = 391
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 391
        bmuws_info = [(48, 0b11111111, 0b00000000, 8, 0), (49, 0b11100000, 0b00011111, 3, 5)]

    class FrntLeftRdrObj14RdrObjLifeCycle:
        sig_name = "FrntLeftRdrObj14RdrObjLifeCycle"
        sig_start_bit = 280
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
        startbit = 280
        bmuws_info = [(35, 0b00000001, 0b11111110, 1, 0), (36, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeftRdrObj14RdrObjHeight:
        sig_name = "FrntLeftRdrObj14RdrObjHeight"
        sig_start_bit = 258
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 258
        bmuws_info = [(32, 0b00000111, 0b11111000, 3, 0), (33, 0b11111110, 0b00000001, 7, 1)]

    class FrntLeftRdrObj14_UB:
        sig_name = "FrntLeftRdrObj14_UB"
        sig_start_bit = 168
        update_id_bit = 168
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
        startbit = 168
        byte = 21
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FrntLeftRdrObj15ObjBoxCenterLat:
        sig_name = "FrntLeftRdrObj15ObjBoxCenterLat"
        sig_start_bit = 383
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 383
        byte = 47
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntLeftRdrObj13RdrObjVy:
        sig_name = "FrntLeftRdrObj13RdrObjVy"
        sig_start_bit = 148
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 148
        bmuws_info = [(18, 0b00011111, 0b11100000, 5, 0), (19, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeftRdrObj13RdrObjID:
        sig_name = "FrntLeftRdrObj13RdrObjID"
        sig_start_bit = 110
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 110
        byte = 13
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class FrntLeftRdrObj13RdrObjDx:
        sig_name = "FrntLeftRdrObj13RdrObjDx"
        sig_start_bit = 11
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 11
        bmuws_info = [(1, 0b00001111, 0b11110000, 4, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeftRdrObj15RdrObjExistProb:
        sig_name = "FrntLeftRdrObj15RdrObjExistProb"
        sig_start_bit = 420
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 420
        bmuws_info = [(52, 0b00011111, 0b11100000, 5, 0), (53, 0b11111000, 0b00000111, 5, 3)]

    class FrntLeftRdrObj15RdrObjCntr:
        sig_name = "FrntLeftRdrObj15RdrObjCntr"
        sig_start_bit = 359
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
        startbit = 359
        byte = 44
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class FrntLeftRdrObj15RdrObjDynProp:
        sig_name = "FrntLeftRdrObj15RdrObjDynProp"
        sig_start_bit = 396
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 396
        byte = 49
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class FrntLeftRdrObj15RdrObjDy:
        sig_name = "FrntLeftRdrObj15RdrObjDy"
        sig_start_bit = 395
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 395
        bmuws_info = [(49, 0b00001111, 0b11110000, 4, 0), (50, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeftRdrObj15RdrObjVy:
        sig_name = "FrntLeftRdrObj15RdrObjVy"
        sig_start_bit = 492
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 492
        bmuws_info = [(61, 0b00011111, 0b11100000, 5, 0), (62, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeftRdrObj14RdrObjDx:
        sig_name = "FrntLeftRdrObj14RdrObjDx"
        sig_start_bit = 187
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 187
        bmuws_info = [(23, 0b00001111, 0b11110000, 4, 0), (24, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeftRdrObj13RdrObjExistProb:
        sig_name = "FrntLeftRdrObj13RdrObjExistProb"
        sig_start_bit = 76
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 76
        bmuws_info = [(9, 0b00011111, 0b11100000, 5, 0), (10, 0b11111000, 0b00000111, 5, 3)]

    class FrntLeftRdrObj14RdrObjID:
        sig_name = "FrntLeftRdrObj14RdrObjID"
        sig_start_bit = 286
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 286
        byte = 35
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class FrntLeftRdrObj14RdrObjCntr:
        sig_name = "FrntLeftRdrObj14RdrObjCntr"
        sig_start_bit = 191
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
        startbit = 191
        byte = 23
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class FrntLeftRdrObj13RdrObjDy:
        sig_name = "FrntLeftRdrObj13RdrObjDy"
        sig_start_bit = 51
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 51
        bmuws_info = [(6, 0b00001111, 0b11110000, 4, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeftRdrObj15_UB:
        sig_name = "FrntLeftRdrObj15_UB"
        sig_start_bit = 171
        update_id_bit = 171
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
        startbit = 171
        byte = 21
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class FrntLeftRdrObj13_UB:
        sig_name = "FrntLeftRdrObj13_UB"
        sig_start_bit = 175
        update_id_bit = 175
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
        startbit = 175
        byte = 21
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class FrntLeftRdrObj13RdrObjVx:
        sig_name = "FrntLeftRdrObj13RdrObjVx"
        sig_start_bit = 121
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 121
        bmuws_info = [(15, 0b00000011, 0b11111100, 2, 0), (16, 0b11111111, 0b00000000, 8, 0), (17, 0b10000000, 0b01111111, 1, 7)]

    class FrntLeftRdrObj13RdrObjHeight:
        sig_name = "FrntLeftRdrObj13RdrObjHeight"
        sig_start_bit = 82
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 82
        bmuws_info = [(10, 0b00000111, 0b11111000, 3, 0), (11, 0b11111110, 0b00000001, 7, 1)]

    class FrntLeftRdrObj15RdrObjVyStdDe:
        sig_name = "FrntLeftRdrObj15RdrObjVyStdDe"
        sig_start_bit = 497
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 497
        bmuws_info = [(62, 0b00000011, 0b11111100, 2, 0), (63, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeftRdrObj15RdrObjDyStdDe:
        sig_name = "FrntLeftRdrObj15RdrObjDyStdDe"
        sig_start_bit = 415
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 415
        bmuws_info = [(51, 0b11111111, 0b00000000, 8, 0), (52, 0b11100000, 0b00011111, 3, 5)]

    class FrntLeftRdrObj13RdrObjVxStdDe:
        sig_name = "FrntLeftRdrObj13RdrObjVxStdDe"
        sig_start_bit = 142
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 142
        bmuws_info = [(17, 0b01111111, 0b10000000, 7, 0), (18, 0b11100000, 0b00011111, 3, 5)]

    class FrntLeftRdrObj14RdrObjDynProp:
        sig_name = "FrntLeftRdrObj14RdrObjDynProp"
        sig_start_bit = 228
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 228
        byte = 28
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class FrntLeftRdrObj14RdrObjExistProb:
        sig_name = "FrntLeftRdrObj14RdrObjExistProb"
        sig_start_bit = 252
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 252
        bmuws_info = [(31, 0b00011111, 0b11100000, 5, 0), (32, 0b11111000, 0b00000111, 5, 3)]

    class FrntLeftRdrObj13RdrObjHeightStdDe:
        sig_name = "FrntLeftRdrObj13RdrObjHeightStdDe"
        sig_start_bit = 88
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 88
        bmuws_info = [(11, 0b00000001, 0b11111110, 1, 0), (12, 0b11111111, 0b00000000, 8, 0), (13, 0b10000000, 0b01111111, 1, 7)]

    class FrntLeftRdrObj14RdrObjVyStdDe:
        sig_name = "FrntLeftRdrObj14RdrObjVyStdDe"
        sig_start_bit = 329
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 329
        bmuws_info = [(41, 0b00000011, 0b11111100, 2, 0), (42, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeftRdrObj13RdrObjDxStdDe:
        sig_name = "FrntLeftRdrObj13RdrObjDxStdDe"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11100000, 0b00011111, 3, 5)]

    class FrntLeftRdrObj13RdrObjChks:
        sig_name = "FrntLeftRdrObj13RdrObjChks"
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

    class FrntLeftRdrObj13RdrObjDyStdDe:
        sig_name = "FrntLeftRdrObj13RdrObjDyStdDe"
        sig_start_bit = 71
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 71
        bmuws_info = [(8, 0b11111111, 0b00000000, 8, 0), (9, 0b11100000, 0b00011111, 3, 5)]

    class FrntLeftRdrObj14RdrObjVx:
        sig_name = "FrntLeftRdrObj14RdrObjVx"
        sig_start_bit = 297
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 297
        bmuws_info = [(37, 0b00000011, 0b11111100, 2, 0), (38, 0b11111111, 0b00000000, 8, 0), (39, 0b10000000, 0b01111111, 1, 7)]

    class FrntLeftRdrObj14ObjBoxCenterLgt:
        sig_name = "FrntLeftRdrObj14ObjBoxCenterLgt"
        sig_start_bit = 207
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 207
        byte = 25
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntLeftRdrObj14RdrObjChks:
        sig_name = "FrntLeftRdrObj14RdrObjChks"
        sig_start_bit = 183
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
        startbit = 183
        byte = 22
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntLeftRdrObj13RdrObjPwr:
        sig_name = "FrntLeftRdrObj13RdrObjPwr"
        sig_start_bit = 113
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 113
        bmuws_info = [(14, 0b00000011, 0b11111100, 2, 0), (15, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeftRdrObj14RdrObjDy:
        sig_name = "FrntLeftRdrObj14RdrObjDy"
        sig_start_bit = 227
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 227
        bmuws_info = [(28, 0b00001111, 0b11110000, 4, 0), (29, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeftRdrObj15RdrObjHeight:
        sig_name = "FrntLeftRdrObj15RdrObjHeight"
        sig_start_bit = 426
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 426
        bmuws_info = [(53, 0b00000111, 0b11111000, 3, 0), (54, 0b11111110, 0b00000001, 7, 1)]

    class FrntLeftRdrObj14RdrObjPwr:
        sig_name = "FrntLeftRdrObj14RdrObjPwr"
        sig_start_bit = 289
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 289
        bmuws_info = [(36, 0b00000011, 0b11111100, 2, 0), (37, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeftRdrObj15RdrObjID:
        sig_name = "FrntLeftRdrObj15RdrObjID"
        sig_start_bit = 454
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 454
        byte = 56
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class FrntLeftRdrObj13RdrObjVyStdDe:
        sig_name = "FrntLeftRdrObj13RdrObjVyStdDe"
        sig_start_bit = 153
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 153
        bmuws_info = [(19, 0b00000011, 0b11111100, 2, 0), (20, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeftRdrObj13RdrObjDynProp:
        sig_name = "FrntLeftRdrObj13RdrObjDynProp"
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
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class FrntLeftRdrObj14RdrObjVy:
        sig_name = "FrntLeftRdrObj14RdrObjVy"
        sig_start_bit = 324
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 324
        bmuws_info = [(40, 0b00011111, 0b11100000, 5, 0), (41, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeftRdrObj14RdrObjHeightStdDe:
        sig_name = "FrntLeftRdrObj14RdrObjHeightStdDe"
        sig_start_bit = 264
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 264
        bmuws_info = [(33, 0b00000001, 0b11111110, 1, 0), (34, 0b11111111, 0b00000000, 8, 0), (35, 0b10000000, 0b01111111, 1, 7)]

    class FrntLeftRdrObj14RdrObjDyStdDe:
        sig_name = "FrntLeftRdrObj14RdrObjDyStdDe"
        sig_start_bit = 247
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 247
        bmuws_info = [(30, 0b11111111, 0b00000000, 8, 0), (31, 0b11100000, 0b00011111, 3, 5)]

    class FrntLeftRdrObj15RdrObjLifeCycle:
        sig_name = "FrntLeftRdrObj15RdrObjLifeCycle"
        sig_start_bit = 448
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
        startbit = 448
        bmuws_info = [(56, 0b00000001, 0b11111110, 1, 0), (57, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeftRdrObj15RdrObjPwr:
        sig_name = "FrntLeftRdrObj15RdrObjPwr"
        sig_start_bit = 457
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 457
        bmuws_info = [(57, 0b00000011, 0b11111100, 2, 0), (58, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeftRdrObj14ObjBoxCenterLat:
        sig_name = "FrntLeftRdrObj14ObjBoxCenterLat"
        sig_start_bit = 215
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 215
        byte = 26
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntLeftRdrObj13ObjBoxCenterLgt:
        sig_name = "FrntLeftRdrObj13ObjBoxCenterLgt"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
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

    class FrntLeftRdrObj13ObjBoxCenterLat:
        sig_name = "FrntLeftRdrObj13ObjBoxCenterLat"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
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

    class FrntLeftRdrObj14RdrObjDxStdDe:
        sig_name = "FrntLeftRdrObj14RdrObjDxStdDe"
        sig_start_bit = 223
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 223
        bmuws_info = [(27, 0b11111111, 0b00000000, 8, 0), (28, 0b11100000, 0b00011111, 3, 5)]

    class FrntLeftRdrObj15RdrObjVx:
        sig_name = "FrntLeftRdrObj15RdrObjVx"
        sig_start_bit = 465
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 465
        bmuws_info = [(58, 0b00000011, 0b11111100, 2, 0), (59, 0b11111111, 0b00000000, 8, 0), (60, 0b10000000, 0b01111111, 1, 7)]

    class FrntLeftRdrObj15RdrObjVxStdDe:
        sig_name = "FrntLeftRdrObj15RdrObjVxStdDe"
        sig_start_bit = 486
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 486
        bmuws_info = [(60, 0b01111111, 0b10000000, 7, 0), (61, 0b11100000, 0b00011111, 3, 5)]

    class FrntLeftRdrObj15RdrObjHeightStdDe:
        sig_name = "FrntLeftRdrObj15RdrObjHeightStdDe"
        sig_start_bit = 432
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 432
        bmuws_info = [(54, 0b00000001, 0b11111110, 1, 0), (55, 0b11111111, 0b00000000, 8, 0), (56, 0b10000000, 0b01111111, 1, 7)]

    class FrntLeftRdrObj14RdrObjVxStdDe:
        sig_name = "FrntLeftRdrObj14RdrObjVxStdDe"
        sig_start_bit = 318
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 318
        bmuws_info = [(39, 0b01111111, 0b10000000, 7, 0), (40, 0b11100000, 0b00011111, 3, 5)]


class BgmADCANFDFr27:
    msg_name = "BgmADCANFDFr27"
    msg_id = 519
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "BGM"
    rx_nodes = ['ACU']
    sig_group_dict = {'RearRgtRdrObj10': ['RearRgtRdrObj10ObjBoxCenterLat', 'RearRgtRdrObj10ObjBoxCenterLgt', 'RearRgtRdrObj10RdrObjChks', 'RearRgtRdrObj10RdrObjCntr', 'RearRgtRdrObj10RdrObjDx', 'RearRgtRdrObj10RdrObjDxStdDe', 'RearRgtRdrObj10RdrObjDy', 'RearRgtRdrObj10RdrObjDynProp', 'RearRgtRdrObj10RdrObjDyStdDe', 'RearRgtRdrObj10RdrObjExistProb', 'RearRgtRdrObj10RdrObjHeight', 'RearRgtRdrObj10RdrObjHeightStdDe', 'RearRgtRdrObj10RdrObjID', 'RearRgtRdrObj10RdrObjLifeCycle', 'RearRgtRdrObj10RdrObjPwr', 'RearRgtRdrObj10RdrObjVx', 'RearRgtRdrObj10RdrObjVxStdDe', 'RearRgtRdrObj10RdrObjVy', 'RearRgtRdrObj10RdrObjVyStdDe'], 'RearRgtRdrObj11': ['RearRgtRdrObj11ObjBoxCenterLat', 'RearRgtRdrObj11ObjBoxCenterLgt', 'RearRgtRdrObj11RdrObjChks', 'RearRgtRdrObj11RdrObjCntr', 'RearRgtRdrObj11RdrObjDx', 'RearRgtRdrObj11RdrObjDxStdDe', 'RearRgtRdrObj11RdrObjDy', 'RearRgtRdrObj11RdrObjDynProp', 'RearRgtRdrObj11RdrObjDyStdDe', 'RearRgtRdrObj11RdrObjExistProb', 'RearRgtRdrObj11RdrObjHeight', 'RearRgtRdrObj11RdrObjHeightStdDe', 'RearRgtRdrObj11RdrObjID', 'RearRgtRdrObj11RdrObjLifeCycle', 'RearRgtRdrObj11RdrObjPwr', 'RearRgtRdrObj11RdrObjVx', 'RearRgtRdrObj11RdrObjVxStdDe', 'RearRgtRdrObj11RdrObjVy', 'RearRgtRdrObj11RdrObjVyStdDe'], 'RearRgtRdrObj12': ['RearRgtRdrObj12ObjBoxCenterLat', 'RearRgtRdrObj12ObjBoxCenterLgt', 'RearRgtRdrObj12RdrObjChks', 'RearRgtRdrObj12RdrObjCntr', 'RearRgtRdrObj12RdrObjDx', 'RearRgtRdrObj12RdrObjDxStdDe', 'RearRgtRdrObj12RdrObjDy', 'RearRgtRdrObj12RdrObjDynProp', 'RearRgtRdrObj12RdrObjDyStdDe', 'RearRgtRdrObj12RdrObjExistProb', 'RearRgtRdrObj12RdrObjHeight', 'RearRgtRdrObj12RdrObjHeightStdDe', 'RearRgtRdrObj12RdrObjID', 'RearRgtRdrObj12RdrObjLifeCycle', 'RearRgtRdrObj12RdrObjPwr', 'RearRgtRdrObj12RdrObjVx', 'RearRgtRdrObj12RdrObjVxStdDe', 'RearRgtRdrObj12RdrObjVy', 'RearRgtRdrObj12RdrObjVyStdDe']}
    sig_group_dataid_dict = {}

    class RearRgtRdrObj11RdrObjDx:
        sig_name = "RearRgtRdrObj11RdrObjDx"
        sig_start_bit = 187
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 187
        bmuws_info = [(23, 0b00001111, 0b11110000, 4, 0), (24, 0b11111111, 0b00000000, 8, 0)]

    class RearRgtRdrObj11ObjBoxCenterLat:
        sig_name = "RearRgtRdrObj11ObjBoxCenterLat"
        sig_start_bit = 215
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 215
        byte = 26
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearRgtRdrObj12RdrObjVx:
        sig_name = "RearRgtRdrObj12RdrObjVx"
        sig_start_bit = 465
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 465
        bmuws_info = [(58, 0b00000011, 0b11111100, 2, 0), (59, 0b11111111, 0b00000000, 8, 0), (60, 0b10000000, 0b01111111, 1, 7)]

    class RearRgtRdrObj12RdrObjHeight:
        sig_name = "RearRgtRdrObj12RdrObjHeight"
        sig_start_bit = 426
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 426
        bmuws_info = [(53, 0b00000111, 0b11111000, 3, 0), (54, 0b11111110, 0b00000001, 7, 1)]

    class RearRgtRdrObj12RdrObjVxStdDe:
        sig_name = "RearRgtRdrObj12RdrObjVxStdDe"
        sig_start_bit = 486
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 486
        bmuws_info = [(60, 0b01111111, 0b10000000, 7, 0), (61, 0b11100000, 0b00011111, 3, 5)]

    class RearRgtRdrObj11RdrObjVx:
        sig_name = "RearRgtRdrObj11RdrObjVx"
        sig_start_bit = 297
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 297
        bmuws_info = [(37, 0b00000011, 0b11111100, 2, 0), (38, 0b11111111, 0b00000000, 8, 0), (39, 0b10000000, 0b01111111, 1, 7)]

    class RearRgtRdrObj10RdrObjCntr:
        sig_name = "RearRgtRdrObj10RdrObjCntr"
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

    class RearRgtRdrObj11RdrObjDynProp:
        sig_name = "RearRgtRdrObj11RdrObjDynProp"
        sig_start_bit = 228
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 228
        byte = 28
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class RearRgtRdrObj11RdrObjDxStdDe:
        sig_name = "RearRgtRdrObj11RdrObjDxStdDe"
        sig_start_bit = 223
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 223
        bmuws_info = [(27, 0b11111111, 0b00000000, 8, 0), (28, 0b11100000, 0b00011111, 3, 5)]

    class RearRgtRdrObj10RdrObjDyStdDe:
        sig_name = "RearRgtRdrObj10RdrObjDyStdDe"
        sig_start_bit = 71
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 71
        bmuws_info = [(8, 0b11111111, 0b00000000, 8, 0), (9, 0b11100000, 0b00011111, 3, 5)]

    class RearRgtRdrObj11RdrObjHeight:
        sig_name = "RearRgtRdrObj11RdrObjHeight"
        sig_start_bit = 258
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 258
        bmuws_info = [(32, 0b00000111, 0b11111000, 3, 0), (33, 0b11111110, 0b00000001, 7, 1)]

    class RearRgtRdrObj10RdrObjPwr:
        sig_name = "RearRgtRdrObj10RdrObjPwr"
        sig_start_bit = 113
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 113
        bmuws_info = [(14, 0b00000011, 0b11111100, 2, 0), (15, 0b11111100, 0b00000011, 6, 2)]

    class RearRgtRdrObj10ObjBoxCenterLat:
        sig_name = "RearRgtRdrObj10ObjBoxCenterLat"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
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

    class RearRgtRdrObj12RdrObjPwr:
        sig_name = "RearRgtRdrObj12RdrObjPwr"
        sig_start_bit = 457
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 457
        bmuws_info = [(57, 0b00000011, 0b11111100, 2, 0), (58, 0b11111100, 0b00000011, 6, 2)]

    class RearRgtRdrObj12RdrObjDx:
        sig_name = "RearRgtRdrObj12RdrObjDx"
        sig_start_bit = 355
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 355
        bmuws_info = [(44, 0b00001111, 0b11110000, 4, 0), (45, 0b11111111, 0b00000000, 8, 0)]

    class RearRgtRdrObj12RdrObjDynProp:
        sig_name = "RearRgtRdrObj12RdrObjDynProp"
        sig_start_bit = 396
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 396
        byte = 49
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class RearRgtRdrObj11RdrObjID:
        sig_name = "RearRgtRdrObj11RdrObjID"
        sig_start_bit = 286
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 286
        byte = 35
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class RearRgtRdrObj11RdrObjCntr:
        sig_name = "RearRgtRdrObj11RdrObjCntr"
        sig_start_bit = 191
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
        startbit = 191
        byte = 23
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class RearRgtRdrObj11RdrObjVyStdDe:
        sig_name = "RearRgtRdrObj11RdrObjVyStdDe"
        sig_start_bit = 329
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 329
        bmuws_info = [(41, 0b00000011, 0b11111100, 2, 0), (42, 0b11111111, 0b00000000, 8, 0)]

    class RearRgtRdrObj12RdrObjID:
        sig_name = "RearRgtRdrObj12RdrObjID"
        sig_start_bit = 454
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 454
        byte = 56
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class RearRgtRdrObj10RdrObjDy:
        sig_name = "RearRgtRdrObj10RdrObjDy"
        sig_start_bit = 51
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 51
        bmuws_info = [(6, 0b00001111, 0b11110000, 4, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class RearRgtRdrObj11RdrObjLifeCycle:
        sig_name = "RearRgtRdrObj11RdrObjLifeCycle"
        sig_start_bit = 280
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
        startbit = 280
        bmuws_info = [(35, 0b00000001, 0b11111110, 1, 0), (36, 0b11111100, 0b00000011, 6, 2)]

    class RearRgtRdrObj11RdrObjExistProb:
        sig_name = "RearRgtRdrObj11RdrObjExistProb"
        sig_start_bit = 252
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 252
        bmuws_info = [(31, 0b00011111, 0b11100000, 5, 0), (32, 0b11111000, 0b00000111, 5, 3)]

    class RearRgtRdrObj11RdrObjDyStdDe:
        sig_name = "RearRgtRdrObj11RdrObjDyStdDe"
        sig_start_bit = 247
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 247
        bmuws_info = [(30, 0b11111111, 0b00000000, 8, 0), (31, 0b11100000, 0b00011111, 3, 5)]

    class RearRgtRdrObj12RdrObjLifeCycle:
        sig_name = "RearRgtRdrObj12RdrObjLifeCycle"
        sig_start_bit = 448
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
        startbit = 448
        bmuws_info = [(56, 0b00000001, 0b11111110, 1, 0), (57, 0b11111100, 0b00000011, 6, 2)]

    class RearRgtRdrObj10RdrObjHeightStdDe:
        sig_name = "RearRgtRdrObj10RdrObjHeightStdDe"
        sig_start_bit = 88
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 88
        bmuws_info = [(11, 0b00000001, 0b11111110, 1, 0), (12, 0b11111111, 0b00000000, 8, 0), (13, 0b10000000, 0b01111111, 1, 7)]

    class RearRgtRdrObj10RdrObjVx:
        sig_name = "RearRgtRdrObj10RdrObjVx"
        sig_start_bit = 121
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 121
        bmuws_info = [(15, 0b00000011, 0b11111100, 2, 0), (16, 0b11111111, 0b00000000, 8, 0), (17, 0b10000000, 0b01111111, 1, 7)]

    class RearRgtRdrObj10_UB:
        sig_name = "RearRgtRdrObj10_UB"
        sig_start_bit = 175
        update_id_bit = 175
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
        startbit = 175
        byte = 21
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class RearRgtRdrObj10RdrObjVy:
        sig_name = "RearRgtRdrObj10RdrObjVy"
        sig_start_bit = 148
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 148
        bmuws_info = [(18, 0b00011111, 0b11100000, 5, 0), (19, 0b11111100, 0b00000011, 6, 2)]

    class RearRgtRdrObj11RdrObjChks:
        sig_name = "RearRgtRdrObj11RdrObjChks"
        sig_start_bit = 183
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
        startbit = 183
        byte = 22
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearRgtRdrObj11RdrObjHeightStdDe:
        sig_name = "RearRgtRdrObj11RdrObjHeightStdDe"
        sig_start_bit = 264
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 264
        bmuws_info = [(33, 0b00000001, 0b11111110, 1, 0), (34, 0b11111111, 0b00000000, 8, 0), (35, 0b10000000, 0b01111111, 1, 7)]

    class RearRgtRdrObj11_UB:
        sig_name = "RearRgtRdrObj11_UB"
        sig_start_bit = 168
        update_id_bit = 168
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
        startbit = 168
        byte = 21
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class RearRgtRdrObj10RdrObjVxStdDe:
        sig_name = "RearRgtRdrObj10RdrObjVxStdDe"
        sig_start_bit = 142
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 142
        bmuws_info = [(17, 0b01111111, 0b10000000, 7, 0), (18, 0b11100000, 0b00011111, 3, 5)]

    class RearRgtRdrObj11RdrObjPwr:
        sig_name = "RearRgtRdrObj11RdrObjPwr"
        sig_start_bit = 289
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 289
        bmuws_info = [(36, 0b00000011, 0b11111100, 2, 0), (37, 0b11111100, 0b00000011, 6, 2)]

    class RearRgtRdrObj10ObjBoxCenterLgt:
        sig_name = "RearRgtRdrObj10ObjBoxCenterLgt"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
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

    class RearRgtRdrObj10RdrObjChks:
        sig_name = "RearRgtRdrObj10RdrObjChks"
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

    class RearRgtRdrObj10RdrObjDx:
        sig_name = "RearRgtRdrObj10RdrObjDx"
        sig_start_bit = 11
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 11
        bmuws_info = [(1, 0b00001111, 0b11110000, 4, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class RearRgtRdrObj10RdrObjLifeCycle:
        sig_name = "RearRgtRdrObj10RdrObjLifeCycle"
        sig_start_bit = 104
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
        startbit = 104
        bmuws_info = [(13, 0b00000001, 0b11111110, 1, 0), (14, 0b11111100, 0b00000011, 6, 2)]

    class RearRgtRdrObj12_UB:
        sig_name = "RearRgtRdrObj12_UB"
        sig_start_bit = 171
        update_id_bit = 171
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
        startbit = 171
        byte = 21
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class RearRgtRdrObj11ObjBoxCenterLgt:
        sig_name = "RearRgtRdrObj11ObjBoxCenterLgt"
        sig_start_bit = 207
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 207
        byte = 25
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearRgtRdrObj12RdrObjChks:
        sig_name = "RearRgtRdrObj12RdrObjChks"
        sig_start_bit = 351
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
        startbit = 351
        byte = 43
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearRgtRdrObj11RdrObjDy:
        sig_name = "RearRgtRdrObj11RdrObjDy"
        sig_start_bit = 227
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 227
        bmuws_info = [(28, 0b00001111, 0b11110000, 4, 0), (29, 0b11111111, 0b00000000, 8, 0)]

    class RearRgtRdrObj12RdrObjCntr:
        sig_name = "RearRgtRdrObj12RdrObjCntr"
        sig_start_bit = 359
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
        startbit = 359
        byte = 44
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class RearRgtRdrObj12RdrObjDy:
        sig_name = "RearRgtRdrObj12RdrObjDy"
        sig_start_bit = 395
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 395
        bmuws_info = [(49, 0b00001111, 0b11110000, 4, 0), (50, 0b11111111, 0b00000000, 8, 0)]

    class RearRgtRdrObj12RdrObjDxStdDe:
        sig_name = "RearRgtRdrObj12RdrObjDxStdDe"
        sig_start_bit = 391
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 391
        bmuws_info = [(48, 0b11111111, 0b00000000, 8, 0), (49, 0b11100000, 0b00011111, 3, 5)]

    class RearRgtRdrObj12RdrObjExistProb:
        sig_name = "RearRgtRdrObj12RdrObjExistProb"
        sig_start_bit = 420
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 420
        bmuws_info = [(52, 0b00011111, 0b11100000, 5, 0), (53, 0b11111000, 0b00000111, 5, 3)]

    class RearRgtRdrObj12ObjBoxCenterLat:
        sig_name = "RearRgtRdrObj12ObjBoxCenterLat"
        sig_start_bit = 383
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 383
        byte = 47
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearRgtRdrObj12RdrObjVy:
        sig_name = "RearRgtRdrObj12RdrObjVy"
        sig_start_bit = 492
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 492
        bmuws_info = [(61, 0b00011111, 0b11100000, 5, 0), (62, 0b11111100, 0b00000011, 6, 2)]

    class RearRgtRdrObj10RdrObjDynProp:
        sig_name = "RearRgtRdrObj10RdrObjDynProp"
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
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class RearRgtRdrObj10RdrObjID:
        sig_name = "RearRgtRdrObj10RdrObjID"
        sig_start_bit = 110
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 110
        byte = 13
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class RearRgtRdrObj12ObjBoxCenterLgt:
        sig_name = "RearRgtRdrObj12ObjBoxCenterLgt"
        sig_start_bit = 375
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 375
        byte = 46
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearRgtRdrObj12RdrObjVyStdDe:
        sig_name = "RearRgtRdrObj12RdrObjVyStdDe"
        sig_start_bit = 497
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 497
        bmuws_info = [(62, 0b00000011, 0b11111100, 2, 0), (63, 0b11111111, 0b00000000, 8, 0)]

    class RearRgtRdrObj10RdrObjVyStdDe:
        sig_name = "RearRgtRdrObj10RdrObjVyStdDe"
        sig_start_bit = 153
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 153
        bmuws_info = [(19, 0b00000011, 0b11111100, 2, 0), (20, 0b11111111, 0b00000000, 8, 0)]

    class RearRgtRdrObj12RdrObjHeightStdDe:
        sig_name = "RearRgtRdrObj12RdrObjHeightStdDe"
        sig_start_bit = 432
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 432
        bmuws_info = [(54, 0b00000001, 0b11111110, 1, 0), (55, 0b11111111, 0b00000000, 8, 0), (56, 0b10000000, 0b01111111, 1, 7)]

    class RearRgtRdrObj10RdrObjExistProb:
        sig_name = "RearRgtRdrObj10RdrObjExistProb"
        sig_start_bit = 76
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 76
        bmuws_info = [(9, 0b00011111, 0b11100000, 5, 0), (10, 0b11111000, 0b00000111, 5, 3)]

    class RearRgtRdrObj11RdrObjVy:
        sig_name = "RearRgtRdrObj11RdrObjVy"
        sig_start_bit = 324
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 324
        bmuws_info = [(40, 0b00011111, 0b11100000, 5, 0), (41, 0b11111100, 0b00000011, 6, 2)]

    class RearRgtRdrObj12RdrObjDyStdDe:
        sig_name = "RearRgtRdrObj12RdrObjDyStdDe"
        sig_start_bit = 415
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 415
        bmuws_info = [(51, 0b11111111, 0b00000000, 8, 0), (52, 0b11100000, 0b00011111, 3, 5)]

    class RearRgtRdrObj10RdrObjDxStdDe:
        sig_name = "RearRgtRdrObj10RdrObjDxStdDe"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11100000, 0b00011111, 3, 5)]

    class RearRgtRdrObj10RdrObjHeight:
        sig_name = "RearRgtRdrObj10RdrObjHeight"
        sig_start_bit = 82
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 82
        bmuws_info = [(10, 0b00000111, 0b11111000, 3, 0), (11, 0b11111110, 0b00000001, 7, 1)]

    class RearRgtRdrObj11RdrObjVxStdDe:
        sig_name = "RearRgtRdrObj11RdrObjVxStdDe"
        sig_start_bit = 318
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 318
        bmuws_info = [(39, 0b01111111, 0b10000000, 7, 0), (40, 0b11100000, 0b00011111, 3, 5)]


class BgmADCANFDFr15:
    msg_name = "BgmADCANFDFr15"
    msg_id = 505
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "BGM"
    rx_nodes = ['ACU']
    sig_group_dict = {'FrntRgtRdrObj11': ['FrntRgtRdrObj11ObjBoxCenterLat', 'FrntRgtRdrObj11ObjBoxCenterLgt', 'FrntRgtRdrObj11RdrObjChks', 'FrntRgtRdrObj11RdrObjCntr', 'FrntRgtRdrObj11RdrObjDx', 'FrntRgtRdrObj11RdrObjDxStdDe', 'FrntRgtRdrObj11RdrObjDy', 'FrntRgtRdrObj11RdrObjDynProp', 'FrntRgtRdrObj11RdrObjDyStdDe', 'FrntRgtRdrObj11RdrObjExistProb', 'FrntRgtRdrObj11RdrObjHeight', 'FrntRgtRdrObj11RdrObjHeightStdDe', 'FrntRgtRdrObj11RdrObjID', 'FrntRgtRdrObj11RdrObjLifeCycle', 'FrntRgtRdrObj11RdrObjPwr', 'FrntRgtRdrObj11RdrObjVx', 'FrntRgtRdrObj11RdrObjVxStdDe', 'FrntRgtRdrObj11RdrObjVy', 'FrntRgtRdrObj11RdrObjVyStdDe'], 'FrntRgtRdrObj12': ['FrntRgtRdrObj12ObjBoxCenterLat', 'FrntRgtRdrObj12ObjBoxCenterLgt', 'FrntRgtRdrObj12RdrObjChks', 'FrntRgtRdrObj12RdrObjCntr', 'FrntRgtRdrObj12RdrObjDx', 'FrntRgtRdrObj12RdrObjDxStdDe', 'FrntRgtRdrObj12RdrObjDy', 'FrntRgtRdrObj12RdrObjDynProp', 'FrntRgtRdrObj12RdrObjDyStdDe', 'FrntRgtRdrObj12RdrObjExistProb', 'FrntRgtRdrObj12RdrObjHeight', 'FrntRgtRdrObj12RdrObjHeightStdDe', 'FrntRgtRdrObj12RdrObjID', 'FrntRgtRdrObj12RdrObjLifeCycle', 'FrntRgtRdrObj12RdrObjPwr', 'FrntRgtRdrObj12RdrObjVx', 'FrntRgtRdrObj12RdrObjVxStdDe', 'FrntRgtRdrObj12RdrObjVy', 'FrntRgtRdrObj12RdrObjVyStdDe'], 'FrntRgtRdrObj10': ['FrntRgtRdrObj10ObjBoxCenterLat', 'FrntRgtRdrObj10ObjBoxCenterLgt', 'FrntRgtRdrObj10RdrObjChks', 'FrntRgtRdrObj10RdrObjCntr', 'FrntRgtRdrObj10RdrObjDx', 'FrntRgtRdrObj10RdrObjDxStdDe', 'FrntRgtRdrObj10RdrObjDy', 'FrntRgtRdrObj10RdrObjDynProp', 'FrntRgtRdrObj10RdrObjDyStdDe', 'FrntRgtRdrObj10RdrObjExistProb', 'FrntRgtRdrObj10RdrObjHeight', 'FrntRgtRdrObj10RdrObjHeightStdDe', 'FrntRgtRdrObj10RdrObjID', 'FrntRgtRdrObj10RdrObjLifeCycle', 'FrntRgtRdrObj10RdrObjPwr', 'FrntRgtRdrObj10RdrObjVx', 'FrntRgtRdrObj10RdrObjVxStdDe', 'FrntRgtRdrObj10RdrObjVy', 'FrntRgtRdrObj10RdrObjVyStdDe']}
    sig_group_dataid_dict = {}

    class FrntRgtRdrObj10RdrObjDyStdDe:
        sig_name = "FrntRgtRdrObj10RdrObjDyStdDe"
        sig_start_bit = 71
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 71
        bmuws_info = [(8, 0b11111111, 0b00000000, 8, 0), (9, 0b11100000, 0b00011111, 3, 5)]

    class FrntRgtRdrObj10ObjBoxCenterLgt:
        sig_name = "FrntRgtRdrObj10ObjBoxCenterLgt"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
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

    class FrntRgtRdrObj10RdrObjHeight:
        sig_name = "FrntRgtRdrObj10RdrObjHeight"
        sig_start_bit = 82
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 82
        bmuws_info = [(10, 0b00000111, 0b11111000, 3, 0), (11, 0b11111110, 0b00000001, 7, 1)]

    class FrntRgtRdrObj12RdrObjDynProp:
        sig_name = "FrntRgtRdrObj12RdrObjDynProp"
        sig_start_bit = 396
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 396
        byte = 49
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class FrntRgtRdrObj12RdrObjDyStdDe:
        sig_name = "FrntRgtRdrObj12RdrObjDyStdDe"
        sig_start_bit = 415
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 415
        bmuws_info = [(51, 0b11111111, 0b00000000, 8, 0), (52, 0b11100000, 0b00011111, 3, 5)]

    class FrntRgtRdrObj12RdrObjVyStdDe:
        sig_name = "FrntRgtRdrObj12RdrObjVyStdDe"
        sig_start_bit = 497
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 497
        bmuws_info = [(62, 0b00000011, 0b11111100, 2, 0), (63, 0b11111111, 0b00000000, 8, 0)]

    class FrntRgtRdrObj12RdrObjHeight:
        sig_name = "FrntRgtRdrObj12RdrObjHeight"
        sig_start_bit = 426
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 426
        bmuws_info = [(53, 0b00000111, 0b11111000, 3, 0), (54, 0b11111110, 0b00000001, 7, 1)]

    class FrntRgtRdrObj12RdrObjExistProb:
        sig_name = "FrntRgtRdrObj12RdrObjExistProb"
        sig_start_bit = 420
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 420
        bmuws_info = [(52, 0b00011111, 0b11100000, 5, 0), (53, 0b11111000, 0b00000111, 5, 3)]

    class FrntRgtRdrObj10RdrObjVy:
        sig_name = "FrntRgtRdrObj10RdrObjVy"
        sig_start_bit = 148
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 148
        bmuws_info = [(18, 0b00011111, 0b11100000, 5, 0), (19, 0b11111100, 0b00000011, 6, 2)]

    class FrntRgtRdrObj10RdrObjDynProp:
        sig_name = "FrntRgtRdrObj10RdrObjDynProp"
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
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class FrntRgtRdrObj11RdrObjID:
        sig_name = "FrntRgtRdrObj11RdrObjID"
        sig_start_bit = 286
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 286
        byte = 35
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class FrntRgtRdrObj11RdrObjDx:
        sig_name = "FrntRgtRdrObj11RdrObjDx"
        sig_start_bit = 187
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 187
        bmuws_info = [(23, 0b00001111, 0b11110000, 4, 0), (24, 0b11111111, 0b00000000, 8, 0)]

    class FrntRgtRdrObj11ObjBoxCenterLat:
        sig_name = "FrntRgtRdrObj11ObjBoxCenterLat"
        sig_start_bit = 215
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 215
        byte = 26
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntRgtRdrObj11RdrObjExistProb:
        sig_name = "FrntRgtRdrObj11RdrObjExistProb"
        sig_start_bit = 252
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 252
        bmuws_info = [(31, 0b00011111, 0b11100000, 5, 0), (32, 0b11111000, 0b00000111, 5, 3)]

    class FrntRgtRdrObj10RdrObjID:
        sig_name = "FrntRgtRdrObj10RdrObjID"
        sig_start_bit = 110
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 110
        byte = 13
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class FrntRgtRdrObj12RdrObjDy:
        sig_name = "FrntRgtRdrObj12RdrObjDy"
        sig_start_bit = 395
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 395
        bmuws_info = [(49, 0b00001111, 0b11110000, 4, 0), (50, 0b11111111, 0b00000000, 8, 0)]

    class FrntRgtRdrObj12RdrObjVx:
        sig_name = "FrntRgtRdrObj12RdrObjVx"
        sig_start_bit = 465
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 465
        bmuws_info = [(58, 0b00000011, 0b11111100, 2, 0), (59, 0b11111111, 0b00000000, 8, 0), (60, 0b10000000, 0b01111111, 1, 7)]

    class FrntRgtRdrObj11RdrObjPwr:
        sig_name = "FrntRgtRdrObj11RdrObjPwr"
        sig_start_bit = 289
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 289
        bmuws_info = [(36, 0b00000011, 0b11111100, 2, 0), (37, 0b11111100, 0b00000011, 6, 2)]

    class FrntRgtRdrObj11RdrObjHeight:
        sig_name = "FrntRgtRdrObj11RdrObjHeight"
        sig_start_bit = 258
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 258
        bmuws_info = [(32, 0b00000111, 0b11111000, 3, 0), (33, 0b11111110, 0b00000001, 7, 1)]

    class FrntRgtRdrObj12RdrObjCntr:
        sig_name = "FrntRgtRdrObj12RdrObjCntr"
        sig_start_bit = 359
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
        startbit = 359
        byte = 44
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class FrntRgtRdrObj11RdrObjVxStdDe:
        sig_name = "FrntRgtRdrObj11RdrObjVxStdDe"
        sig_start_bit = 318
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 318
        bmuws_info = [(39, 0b01111111, 0b10000000, 7, 0), (40, 0b11100000, 0b00011111, 3, 5)]

    class FrntRgtRdrObj11RdrObjDy:
        sig_name = "FrntRgtRdrObj11RdrObjDy"
        sig_start_bit = 227
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 227
        bmuws_info = [(28, 0b00001111, 0b11110000, 4, 0), (29, 0b11111111, 0b00000000, 8, 0)]

    class FrntRgtRdrObj11_UB:
        sig_name = "FrntRgtRdrObj11_UB"
        sig_start_bit = 168
        update_id_bit = 168
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
        startbit = 168
        byte = 21
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FrntRgtRdrObj12RdrObjDxStdDe:
        sig_name = "FrntRgtRdrObj12RdrObjDxStdDe"
        sig_start_bit = 391
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 391
        bmuws_info = [(48, 0b11111111, 0b00000000, 8, 0), (49, 0b11100000, 0b00011111, 3, 5)]

    class FrntRgtRdrObj12RdrObjLifeCycle:
        sig_name = "FrntRgtRdrObj12RdrObjLifeCycle"
        sig_start_bit = 448
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
        startbit = 448
        bmuws_info = [(56, 0b00000001, 0b11111110, 1, 0), (57, 0b11111100, 0b00000011, 6, 2)]

    class FrntRgtRdrObj11RdrObjVyStdDe:
        sig_name = "FrntRgtRdrObj11RdrObjVyStdDe"
        sig_start_bit = 329
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 329
        bmuws_info = [(41, 0b00000011, 0b11111100, 2, 0), (42, 0b11111111, 0b00000000, 8, 0)]

    class FrntRgtRdrObj11RdrObjLifeCycle:
        sig_name = "FrntRgtRdrObj11RdrObjLifeCycle"
        sig_start_bit = 280
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
        startbit = 280
        bmuws_info = [(35, 0b00000001, 0b11111110, 1, 0), (36, 0b11111100, 0b00000011, 6, 2)]

    class FrntRgtRdrObj10RdrObjVyStdDe:
        sig_name = "FrntRgtRdrObj10RdrObjVyStdDe"
        sig_start_bit = 153
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 153
        bmuws_info = [(19, 0b00000011, 0b11111100, 2, 0), (20, 0b11111111, 0b00000000, 8, 0)]

    class FrntRgtRdrObj11RdrObjCntr:
        sig_name = "FrntRgtRdrObj11RdrObjCntr"
        sig_start_bit = 191
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
        startbit = 191
        byte = 23
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class FrntRgtRdrObj11RdrObjDynProp:
        sig_name = "FrntRgtRdrObj11RdrObjDynProp"
        sig_start_bit = 228
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 228
        byte = 28
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class FrntRgtRdrObj10RdrObjHeightStdDe:
        sig_name = "FrntRgtRdrObj10RdrObjHeightStdDe"
        sig_start_bit = 88
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 88
        bmuws_info = [(11, 0b00000001, 0b11111110, 1, 0), (12, 0b11111111, 0b00000000, 8, 0), (13, 0b10000000, 0b01111111, 1, 7)]

    class FrntRgtRdrObj12RdrObjVy:
        sig_name = "FrntRgtRdrObj12RdrObjVy"
        sig_start_bit = 492
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 492
        bmuws_info = [(61, 0b00011111, 0b11100000, 5, 0), (62, 0b11111100, 0b00000011, 6, 2)]

    class FrntRgtRdrObj12_UB:
        sig_name = "FrntRgtRdrObj12_UB"
        sig_start_bit = 171
        update_id_bit = 171
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
        startbit = 171
        byte = 21
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class FrntRgtRdrObj12RdrObjVxStdDe:
        sig_name = "FrntRgtRdrObj12RdrObjVxStdDe"
        sig_start_bit = 486
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 486
        bmuws_info = [(60, 0b01111111, 0b10000000, 7, 0), (61, 0b11100000, 0b00011111, 3, 5)]

    class FrntRgtRdrObj10ObjBoxCenterLat:
        sig_name = "FrntRgtRdrObj10ObjBoxCenterLat"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
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

    class FrntRgtRdrObj11RdrObjVx:
        sig_name = "FrntRgtRdrObj11RdrObjVx"
        sig_start_bit = 297
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 297
        bmuws_info = [(37, 0b00000011, 0b11111100, 2, 0), (38, 0b11111111, 0b00000000, 8, 0), (39, 0b10000000, 0b01111111, 1, 7)]

    class FrntRgtRdrObj11RdrObjDyStdDe:
        sig_name = "FrntRgtRdrObj11RdrObjDyStdDe"
        sig_start_bit = 247
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 247
        bmuws_info = [(30, 0b11111111, 0b00000000, 8, 0), (31, 0b11100000, 0b00011111, 3, 5)]

    class FrntRgtRdrObj12RdrObjID:
        sig_name = "FrntRgtRdrObj12RdrObjID"
        sig_start_bit = 454
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 454
        byte = 56
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class FrntRgtRdrObj12RdrObjPwr:
        sig_name = "FrntRgtRdrObj12RdrObjPwr"
        sig_start_bit = 457
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 457
        bmuws_info = [(57, 0b00000011, 0b11111100, 2, 0), (58, 0b11111100, 0b00000011, 6, 2)]

    class FrntRgtRdrObj10_UB:
        sig_name = "FrntRgtRdrObj10_UB"
        sig_start_bit = 175
        update_id_bit = 175
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
        startbit = 175
        byte = 21
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class FrntRgtRdrObj11ObjBoxCenterLgt:
        sig_name = "FrntRgtRdrObj11ObjBoxCenterLgt"
        sig_start_bit = 207
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 207
        byte = 25
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntRgtRdrObj10RdrObjLifeCycle:
        sig_name = "FrntRgtRdrObj10RdrObjLifeCycle"
        sig_start_bit = 104
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
        startbit = 104
        bmuws_info = [(13, 0b00000001, 0b11111110, 1, 0), (14, 0b11111100, 0b00000011, 6, 2)]

    class FrntRgtRdrObj12RdrObjChks:
        sig_name = "FrntRgtRdrObj12RdrObjChks"
        sig_start_bit = 351
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
        startbit = 351
        byte = 43
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntRgtRdrObj10RdrObjExistProb:
        sig_name = "FrntRgtRdrObj10RdrObjExistProb"
        sig_start_bit = 76
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 76
        bmuws_info = [(9, 0b00011111, 0b11100000, 5, 0), (10, 0b11111000, 0b00000111, 5, 3)]

    class FrntRgtRdrObj10RdrObjDx:
        sig_name = "FrntRgtRdrObj10RdrObjDx"
        sig_start_bit = 11
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 11
        bmuws_info = [(1, 0b00001111, 0b11110000, 4, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class FrntRgtRdrObj12RdrObjDx:
        sig_name = "FrntRgtRdrObj12RdrObjDx"
        sig_start_bit = 355
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 355
        bmuws_info = [(44, 0b00001111, 0b11110000, 4, 0), (45, 0b11111111, 0b00000000, 8, 0)]

    class FrntRgtRdrObj10RdrObjCntr:
        sig_name = "FrntRgtRdrObj10RdrObjCntr"
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

    class FrntRgtRdrObj12ObjBoxCenterLgt:
        sig_name = "FrntRgtRdrObj12ObjBoxCenterLgt"
        sig_start_bit = 375
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 375
        byte = 46
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntRgtRdrObj12RdrObjHeightStdDe:
        sig_name = "FrntRgtRdrObj12RdrObjHeightStdDe"
        sig_start_bit = 432
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 432
        bmuws_info = [(54, 0b00000001, 0b11111110, 1, 0), (55, 0b11111111, 0b00000000, 8, 0), (56, 0b10000000, 0b01111111, 1, 7)]

    class FrntRgtRdrObj10RdrObjDy:
        sig_name = "FrntRgtRdrObj10RdrObjDy"
        sig_start_bit = 51
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 51
        bmuws_info = [(6, 0b00001111, 0b11110000, 4, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class FrntRgtRdrObj10RdrObjPwr:
        sig_name = "FrntRgtRdrObj10RdrObjPwr"
        sig_start_bit = 113
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 113
        bmuws_info = [(14, 0b00000011, 0b11111100, 2, 0), (15, 0b11111100, 0b00000011, 6, 2)]

    class FrntRgtRdrObj10RdrObjChks:
        sig_name = "FrntRgtRdrObj10RdrObjChks"
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

    class FrntRgtRdrObj12ObjBoxCenterLat:
        sig_name = "FrntRgtRdrObj12ObjBoxCenterLat"
        sig_start_bit = 383
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 383
        byte = 47
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntRgtRdrObj11RdrObjChks:
        sig_name = "FrntRgtRdrObj11RdrObjChks"
        sig_start_bit = 183
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
        startbit = 183
        byte = 22
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntRgtRdrObj11RdrObjHeightStdDe:
        sig_name = "FrntRgtRdrObj11RdrObjHeightStdDe"
        sig_start_bit = 264
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 264
        bmuws_info = [(33, 0b00000001, 0b11111110, 1, 0), (34, 0b11111111, 0b00000000, 8, 0), (35, 0b10000000, 0b01111111, 1, 7)]

    class FrntRgtRdrObj10RdrObjVxStdDe:
        sig_name = "FrntRgtRdrObj10RdrObjVxStdDe"
        sig_start_bit = 142
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 142
        bmuws_info = [(17, 0b01111111, 0b10000000, 7, 0), (18, 0b11100000, 0b00011111, 3, 5)]

    class FrntRgtRdrObj10RdrObjDxStdDe:
        sig_name = "FrntRgtRdrObj10RdrObjDxStdDe"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11100000, 0b00011111, 3, 5)]

    class FrntRgtRdrObj11RdrObjDxStdDe:
        sig_name = "FrntRgtRdrObj11RdrObjDxStdDe"
        sig_start_bit = 223
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 223
        bmuws_info = [(27, 0b11111111, 0b00000000, 8, 0), (28, 0b11100000, 0b00011111, 3, 5)]

    class FrntRgtRdrObj11RdrObjVy:
        sig_name = "FrntRgtRdrObj11RdrObjVy"
        sig_start_bit = 324
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 324
        bmuws_info = [(40, 0b00011111, 0b11100000, 5, 0), (41, 0b11111100, 0b00000011, 6, 2)]

    class FrntRgtRdrObj10RdrObjVx:
        sig_name = "FrntRgtRdrObj10RdrObjVx"
        sig_start_bit = 121
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 121
        bmuws_info = [(15, 0b00000011, 0b11111100, 2, 0), (16, 0b11111111, 0b00000000, 8, 0), (17, 0b10000000, 0b01111111, 1, 7)]


class BgmADCANFDFr20:
    msg_name = "BgmADCANFDFr20"
    msg_id = 511
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "BGM"
    rx_nodes = ['ACU']
    sig_group_dict = {'RearLeftRdrObj9': ['RearLeftRdrObj9ObjBoxCenterLat', 'RearLeftRdrObj9ObjBoxCenterLgt', 'RearLeftRdrObj9RdrObjChks', 'RearLeftRdrObj9RdrObjCntr', 'RearLeftRdrObj9RdrObjDx', 'RearLeftRdrObj9RdrObjDxStdDe', 'RearLeftRdrObj9RdrObjDy', 'RearLeftRdrObj9RdrObjDynProp', 'RearLeftRdrObj9RdrObjDyStdDe', 'RearLeftRdrObj9RdrObjExistProb', 'RearLeftRdrObj9RdrObjHeight', 'RearLeftRdrObj9RdrObjHeightStdDe', 'RearLeftRdrObj9RdrObjID', 'RearLeftRdrObj9RdrObjLifeCycle', 'RearLeftRdrObj9RdrObjPwr', 'RearLeftRdrObj9RdrObjVx', 'RearLeftRdrObj9RdrObjVxStdDe', 'RearLeftRdrObj9RdrObjVy', 'RearLeftRdrObj9RdrObjVyStdDe'], 'RearLeftRdrObj7': ['RearLeftRdrObj7ObjBoxCenterLat', 'RearLeftRdrObj7ObjBoxCenterLgt', 'RearLeftRdrObj7RdrObjChks', 'RearLeftRdrObj7RdrObjCntr', 'RearLeftRdrObj7RdrObjDx', 'RearLeftRdrObj7RdrObjDxStdDe', 'RearLeftRdrObj7RdrObjDy', 'RearLeftRdrObj7RdrObjDynProp', 'RearLeftRdrObj7RdrObjDyStdDe', 'RearLeftRdrObj7RdrObjExistProb', 'RearLeftRdrObj7RdrObjHeight', 'RearLeftRdrObj7RdrObjHeightStdDe', 'RearLeftRdrObj7RdrObjID', 'RearLeftRdrObj7RdrObjLifeCycle', 'RearLeftRdrObj7RdrObjPwr', 'RearLeftRdrObj7RdrObjVx', 'RearLeftRdrObj7RdrObjVxStdDe', 'RearLeftRdrObj7RdrObjVy', 'RearLeftRdrObj7RdrObjVyStdDe'], 'RearLeftRdrObj8': ['RearLeftRdrObj8ObjBoxCenterLat', 'RearLeftRdrObj8ObjBoxCenterLgt', 'RearLeftRdrObj8RdrObjChks', 'RearLeftRdrObj8RdrObjCntr', 'RearLeftRdrObj8RdrObjDx', 'RearLeftRdrObj8RdrObjDxStdDe', 'RearLeftRdrObj8RdrObjDy', 'RearLeftRdrObj8RdrObjDynProp', 'RearLeftRdrObj8RdrObjDyStdDe', 'RearLeftRdrObj8RdrObjExistProb', 'RearLeftRdrObj8RdrObjHeight', 'RearLeftRdrObj8RdrObjHeightStdDe', 'RearLeftRdrObj8RdrObjID', 'RearLeftRdrObj8RdrObjLifeCycle', 'RearLeftRdrObj8RdrObjPwr', 'RearLeftRdrObj8RdrObjVx', 'RearLeftRdrObj8RdrObjVxStdDe', 'RearLeftRdrObj8RdrObjVy', 'RearLeftRdrObj8RdrObjVyStdDe']}
    sig_group_dataid_dict = {}

    class RearLeftRdrObj8RdrObjVyStdDe:
        sig_name = "RearLeftRdrObj8RdrObjVyStdDe"
        sig_start_bit = 329
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 329
        bmuws_info = [(41, 0b00000011, 0b11111100, 2, 0), (42, 0b11111111, 0b00000000, 8, 0)]

    class RearLeftRdrObj7RdrObjExistProb:
        sig_name = "RearLeftRdrObj7RdrObjExistProb"
        sig_start_bit = 76
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 76
        bmuws_info = [(9, 0b00011111, 0b11100000, 5, 0), (10, 0b11111000, 0b00000111, 5, 3)]

    class RearLeftRdrObj8RdrObjHeight:
        sig_name = "RearLeftRdrObj8RdrObjHeight"
        sig_start_bit = 258
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 258
        bmuws_info = [(32, 0b00000111, 0b11111000, 3, 0), (33, 0b11111110, 0b00000001, 7, 1)]

    class RearLeftRdrObj9RdrObjVx:
        sig_name = "RearLeftRdrObj9RdrObjVx"
        sig_start_bit = 465
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 465
        bmuws_info = [(58, 0b00000011, 0b11111100, 2, 0), (59, 0b11111111, 0b00000000, 8, 0), (60, 0b10000000, 0b01111111, 1, 7)]

    class RearLeftRdrObj7RdrObjVyStdDe:
        sig_name = "RearLeftRdrObj7RdrObjVyStdDe"
        sig_start_bit = 153
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 153
        bmuws_info = [(19, 0b00000011, 0b11111100, 2, 0), (20, 0b11111111, 0b00000000, 8, 0)]

    class RearLeftRdrObj9_UB:
        sig_name = "RearLeftRdrObj9_UB"
        sig_start_bit = 171
        update_id_bit = 171
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
        startbit = 171
        byte = 21
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class RearLeftRdrObj7RdrObjVxStdDe:
        sig_name = "RearLeftRdrObj7RdrObjVxStdDe"
        sig_start_bit = 142
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 142
        bmuws_info = [(17, 0b01111111, 0b10000000, 7, 0), (18, 0b11100000, 0b00011111, 3, 5)]

    class RearLeftRdrObj7RdrObjLifeCycle:
        sig_name = "RearLeftRdrObj7RdrObjLifeCycle"
        sig_start_bit = 104
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
        startbit = 104
        bmuws_info = [(13, 0b00000001, 0b11111110, 1, 0), (14, 0b11111100, 0b00000011, 6, 2)]

    class RearLeftRdrObj9RdrObjID:
        sig_name = "RearLeftRdrObj9RdrObjID"
        sig_start_bit = 454
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 454
        byte = 56
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class RearLeftRdrObj9RdrObjChks:
        sig_name = "RearLeftRdrObj9RdrObjChks"
        sig_start_bit = 351
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
        startbit = 351
        byte = 43
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearLeftRdrObj8RdrObjPwr:
        sig_name = "RearLeftRdrObj8RdrObjPwr"
        sig_start_bit = 289
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 289
        bmuws_info = [(36, 0b00000011, 0b11111100, 2, 0), (37, 0b11111100, 0b00000011, 6, 2)]

    class RearLeftRdrObj8RdrObjID:
        sig_name = "RearLeftRdrObj8RdrObjID"
        sig_start_bit = 286
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 286
        byte = 35
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class RearLeftRdrObj8RdrObjDynProp:
        sig_name = "RearLeftRdrObj8RdrObjDynProp"
        sig_start_bit = 228
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 228
        byte = 28
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class RearLeftRdrObj8RdrObjVx:
        sig_name = "RearLeftRdrObj8RdrObjVx"
        sig_start_bit = 297
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 297
        bmuws_info = [(37, 0b00000011, 0b11111100, 2, 0), (38, 0b11111111, 0b00000000, 8, 0), (39, 0b10000000, 0b01111111, 1, 7)]

    class RearLeftRdrObj8ObjBoxCenterLgt:
        sig_name = "RearLeftRdrObj8ObjBoxCenterLgt"
        sig_start_bit = 207
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 207
        byte = 25
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearLeftRdrObj7RdrObjDynProp:
        sig_name = "RearLeftRdrObj7RdrObjDynProp"
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
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class RearLeftRdrObj7_UB:
        sig_name = "RearLeftRdrObj7_UB"
        sig_start_bit = 175
        update_id_bit = 175
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
        startbit = 175
        byte = 21
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class RearLeftRdrObj8RdrObjDy:
        sig_name = "RearLeftRdrObj8RdrObjDy"
        sig_start_bit = 227
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 227
        bmuws_info = [(28, 0b00001111, 0b11110000, 4, 0), (29, 0b11111111, 0b00000000, 8, 0)]

    class RearLeftRdrObj9ObjBoxCenterLgt:
        sig_name = "RearLeftRdrObj9ObjBoxCenterLgt"
        sig_start_bit = 375
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 375
        byte = 46
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearLeftRdrObj9RdrObjVyStdDe:
        sig_name = "RearLeftRdrObj9RdrObjVyStdDe"
        sig_start_bit = 497
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 497
        bmuws_info = [(62, 0b00000011, 0b11111100, 2, 0), (63, 0b11111111, 0b00000000, 8, 0)]

    class RearLeftRdrObj9RdrObjDxStdDe:
        sig_name = "RearLeftRdrObj9RdrObjDxStdDe"
        sig_start_bit = 391
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 391
        bmuws_info = [(48, 0b11111111, 0b00000000, 8, 0), (49, 0b11100000, 0b00011111, 3, 5)]

    class RearLeftRdrObj8RdrObjDxStdDe:
        sig_name = "RearLeftRdrObj8RdrObjDxStdDe"
        sig_start_bit = 223
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 223
        bmuws_info = [(27, 0b11111111, 0b00000000, 8, 0), (28, 0b11100000, 0b00011111, 3, 5)]

    class RearLeftRdrObj7RdrObjVy:
        sig_name = "RearLeftRdrObj7RdrObjVy"
        sig_start_bit = 148
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 148
        bmuws_info = [(18, 0b00011111, 0b11100000, 5, 0), (19, 0b11111100, 0b00000011, 6, 2)]

    class RearLeftRdrObj7RdrObjDxStdDe:
        sig_name = "RearLeftRdrObj7RdrObjDxStdDe"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11100000, 0b00011111, 3, 5)]

    class RearLeftRdrObj8RdrObjDx:
        sig_name = "RearLeftRdrObj8RdrObjDx"
        sig_start_bit = 187
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 187
        bmuws_info = [(23, 0b00001111, 0b11110000, 4, 0), (24, 0b11111111, 0b00000000, 8, 0)]

    class RearLeftRdrObj7RdrObjHeightStdDe:
        sig_name = "RearLeftRdrObj7RdrObjHeightStdDe"
        sig_start_bit = 88
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 88
        bmuws_info = [(11, 0b00000001, 0b11111110, 1, 0), (12, 0b11111111, 0b00000000, 8, 0), (13, 0b10000000, 0b01111111, 1, 7)]

    class RearLeftRdrObj8RdrObjDyStdDe:
        sig_name = "RearLeftRdrObj8RdrObjDyStdDe"
        sig_start_bit = 247
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 247
        bmuws_info = [(30, 0b11111111, 0b00000000, 8, 0), (31, 0b11100000, 0b00011111, 3, 5)]

    class RearLeftRdrObj7RdrObjDy:
        sig_name = "RearLeftRdrObj7RdrObjDy"
        sig_start_bit = 51
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 51
        bmuws_info = [(6, 0b00001111, 0b11110000, 4, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class RearLeftRdrObj9RdrObjDyStdDe:
        sig_name = "RearLeftRdrObj9RdrObjDyStdDe"
        sig_start_bit = 415
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 415
        bmuws_info = [(51, 0b11111111, 0b00000000, 8, 0), (52, 0b11100000, 0b00011111, 3, 5)]

    class RearLeftRdrObj9ObjBoxCenterLat:
        sig_name = "RearLeftRdrObj9ObjBoxCenterLat"
        sig_start_bit = 383
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 383
        byte = 47
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearLeftRdrObj8RdrObjVy:
        sig_name = "RearLeftRdrObj8RdrObjVy"
        sig_start_bit = 324
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 324
        bmuws_info = [(40, 0b00011111, 0b11100000, 5, 0), (41, 0b11111100, 0b00000011, 6, 2)]

    class RearLeftRdrObj8RdrObjChks:
        sig_name = "RearLeftRdrObj8RdrObjChks"
        sig_start_bit = 183
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
        startbit = 183
        byte = 22
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearLeftRdrObj8_UB:
        sig_name = "RearLeftRdrObj8_UB"
        sig_start_bit = 168
        update_id_bit = 168
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
        startbit = 168
        byte = 21
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class RearLeftRdrObj7RdrObjDx:
        sig_name = "RearLeftRdrObj7RdrObjDx"
        sig_start_bit = 11
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 11
        bmuws_info = [(1, 0b00001111, 0b11110000, 4, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class RearLeftRdrObj9RdrObjLifeCycle:
        sig_name = "RearLeftRdrObj9RdrObjLifeCycle"
        sig_start_bit = 448
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
        startbit = 448
        bmuws_info = [(56, 0b00000001, 0b11111110, 1, 0), (57, 0b11111100, 0b00000011, 6, 2)]

    class RearLeftRdrObj9RdrObjHeightStdDe:
        sig_name = "RearLeftRdrObj9RdrObjHeightStdDe"
        sig_start_bit = 432
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 432
        bmuws_info = [(54, 0b00000001, 0b11111110, 1, 0), (55, 0b11111111, 0b00000000, 8, 0), (56, 0b10000000, 0b01111111, 1, 7)]

    class RearLeftRdrObj9RdrObjExistProb:
        sig_name = "RearLeftRdrObj9RdrObjExistProb"
        sig_start_bit = 420
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 420
        bmuws_info = [(52, 0b00011111, 0b11100000, 5, 0), (53, 0b11111000, 0b00000111, 5, 3)]

    class RearLeftRdrObj7RdrObjID:
        sig_name = "RearLeftRdrObj7RdrObjID"
        sig_start_bit = 110
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 110
        byte = 13
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class RearLeftRdrObj7RdrObjVx:
        sig_name = "RearLeftRdrObj7RdrObjVx"
        sig_start_bit = 121
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 121
        bmuws_info = [(15, 0b00000011, 0b11111100, 2, 0), (16, 0b11111111, 0b00000000, 8, 0), (17, 0b10000000, 0b01111111, 1, 7)]

    class RearLeftRdrObj8RdrObjExistProb:
        sig_name = "RearLeftRdrObj8RdrObjExistProb"
        sig_start_bit = 252
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 252
        bmuws_info = [(31, 0b00011111, 0b11100000, 5, 0), (32, 0b11111000, 0b00000111, 5, 3)]

    class RearLeftRdrObj9RdrObjPwr:
        sig_name = "RearLeftRdrObj9RdrObjPwr"
        sig_start_bit = 457
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 457
        bmuws_info = [(57, 0b00000011, 0b11111100, 2, 0), (58, 0b11111100, 0b00000011, 6, 2)]

    class RearLeftRdrObj8RdrObjLifeCycle:
        sig_name = "RearLeftRdrObj8RdrObjLifeCycle"
        sig_start_bit = 280
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
        startbit = 280
        bmuws_info = [(35, 0b00000001, 0b11111110, 1, 0), (36, 0b11111100, 0b00000011, 6, 2)]

    class RearLeftRdrObj7RdrObjHeight:
        sig_name = "RearLeftRdrObj7RdrObjHeight"
        sig_start_bit = 82
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 82
        bmuws_info = [(10, 0b00000111, 0b11111000, 3, 0), (11, 0b11111110, 0b00000001, 7, 1)]

    class RearLeftRdrObj9RdrObjVy:
        sig_name = "RearLeftRdrObj9RdrObjVy"
        sig_start_bit = 492
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 492
        bmuws_info = [(61, 0b00011111, 0b11100000, 5, 0), (62, 0b11111100, 0b00000011, 6, 2)]

    class RearLeftRdrObj7RdrObjPwr:
        sig_name = "RearLeftRdrObj7RdrObjPwr"
        sig_start_bit = 113
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 113
        bmuws_info = [(14, 0b00000011, 0b11111100, 2, 0), (15, 0b11111100, 0b00000011, 6, 2)]

    class RearLeftRdrObj9RdrObjHeight:
        sig_name = "RearLeftRdrObj9RdrObjHeight"
        sig_start_bit = 426
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 426
        bmuws_info = [(53, 0b00000111, 0b11111000, 3, 0), (54, 0b11111110, 0b00000001, 7, 1)]

    class RearLeftRdrObj7ObjBoxCenterLgt:
        sig_name = "RearLeftRdrObj7ObjBoxCenterLgt"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
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

    class RearLeftRdrObj8ObjBoxCenterLat:
        sig_name = "RearLeftRdrObj8ObjBoxCenterLat"
        sig_start_bit = 215
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 215
        byte = 26
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearLeftRdrObj8RdrObjCntr:
        sig_name = "RearLeftRdrObj8RdrObjCntr"
        sig_start_bit = 191
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
        startbit = 191
        byte = 23
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class RearLeftRdrObj8RdrObjHeightStdDe:
        sig_name = "RearLeftRdrObj8RdrObjHeightStdDe"
        sig_start_bit = 264
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 264
        bmuws_info = [(33, 0b00000001, 0b11111110, 1, 0), (34, 0b11111111, 0b00000000, 8, 0), (35, 0b10000000, 0b01111111, 1, 7)]

    class RearLeftRdrObj7RdrObjDyStdDe:
        sig_name = "RearLeftRdrObj7RdrObjDyStdDe"
        sig_start_bit = 71
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 71
        bmuws_info = [(8, 0b11111111, 0b00000000, 8, 0), (9, 0b11100000, 0b00011111, 3, 5)]

    class RearLeftRdrObj9RdrObjDx:
        sig_name = "RearLeftRdrObj9RdrObjDx"
        sig_start_bit = 355
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 355
        bmuws_info = [(44, 0b00001111, 0b11110000, 4, 0), (45, 0b11111111, 0b00000000, 8, 0)]

    class RearLeftRdrObj9RdrObjCntr:
        sig_name = "RearLeftRdrObj9RdrObjCntr"
        sig_start_bit = 359
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
        startbit = 359
        byte = 44
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class RearLeftRdrObj9RdrObjVxStdDe:
        sig_name = "RearLeftRdrObj9RdrObjVxStdDe"
        sig_start_bit = 486
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 486
        bmuws_info = [(60, 0b01111111, 0b10000000, 7, 0), (61, 0b11100000, 0b00011111, 3, 5)]

    class RearLeftRdrObj7ObjBoxCenterLat:
        sig_name = "RearLeftRdrObj7ObjBoxCenterLat"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
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

    class RearLeftRdrObj7RdrObjChks:
        sig_name = "RearLeftRdrObj7RdrObjChks"
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

    class RearLeftRdrObj9RdrObjDynProp:
        sig_name = "RearLeftRdrObj9RdrObjDynProp"
        sig_start_bit = 396
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 396
        byte = 49
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class RearLeftRdrObj8RdrObjVxStdDe:
        sig_name = "RearLeftRdrObj8RdrObjVxStdDe"
        sig_start_bit = 318
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 318
        bmuws_info = [(39, 0b01111111, 0b10000000, 7, 0), (40, 0b11100000, 0b00011111, 3, 5)]

    class RearLeftRdrObj7RdrObjCntr:
        sig_name = "RearLeftRdrObj7RdrObjCntr"
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

    class RearLeftRdrObj9RdrObjDy:
        sig_name = "RearLeftRdrObj9RdrObjDy"
        sig_start_bit = 395
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 395
        bmuws_info = [(49, 0b00001111, 0b11110000, 4, 0), (50, 0b11111111, 0b00000000, 8, 0)]


class BgmADCANFDFr09:
    msg_name = "BgmADCANFDFr09"
    msg_id = 499
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "BGM"
    rx_nodes = ['ACU']
    sig_group_dict = {'FrntLeftRdrObj10': ['FrntLeftRdrObj10ObjBoxCenterLat', 'FrntLeftRdrObj10ObjBoxCenterLgt', 'FrntLeftRdrObj10RdrObjChks', 'FrntLeftRdrObj10RdrObjCntr', 'FrntLeftRdrObj10RdrObjDx', 'FrntLeftRdrObj10RdrObjDxStdDe', 'FrntLeftRdrObj10RdrObjDy', 'FrntLeftRdrObj10RdrObjDynProp', 'FrntLeftRdrObj10RdrObjDyStdDe', 'FrntLeftRdrObj10RdrObjExistProb', 'FrntLeftRdrObj10RdrObjHeight', 'FrntLeftRdrObj10RdrObjHeightStdDe', 'FrntLeftRdrObj10RdrObjID', 'FrntLeftRdrObj10RdrObjLifeCycle', 'FrntLeftRdrObj10RdrObjPwr', 'FrntLeftRdrObj10RdrObjVx', 'FrntLeftRdrObj10RdrObjVxStdDe', 'FrntLeftRdrObj10RdrObjVy', 'FrntLeftRdrObj10RdrObjVyStdDe'], 'FrntLeftRdrObj12': ['FrntLeftRdrObj12ObjBoxCenterLat', 'FrntLeftRdrObj12ObjBoxCenterLgt', 'FrntLeftRdrObj12RdrObjChks', 'FrntLeftRdrObj12RdrObjCntr', 'FrntLeftRdrObj12RdrObjDx', 'FrntLeftRdrObj12RdrObjDxStdDe', 'FrntLeftRdrObj12RdrObjDy', 'FrntLeftRdrObj12RdrObjDynProp', 'FrntLeftRdrObj12RdrObjDyStdDe', 'FrntLeftRdrObj12RdrObjExistProb', 'FrntLeftRdrObj12RdrObjHeight', 'FrntLeftRdrObj12RdrObjHeightStdDe', 'FrntLeftRdrObj12RdrObjID', 'FrntLeftRdrObj12RdrObjLifeCycle', 'FrntLeftRdrObj12RdrObjPwr', 'FrntLeftRdrObj12RdrObjVx', 'FrntLeftRdrObj12RdrObjVxStdDe', 'FrntLeftRdrObj12RdrObjVy', 'FrntLeftRdrObj12RdrObjVyStdDe'], 'FrntLeftRdrObj11': ['FrntLeftRdrObj11ObjBoxCenterLat', 'FrntLeftRdrObj11ObjBoxCenterLgt', 'FrntLeftRdrObj11RdrObjChks', 'FrntLeftRdrObj11RdrObjCntr', 'FrntLeftRdrObj11RdrObjDx', 'FrntLeftRdrObj11RdrObjDxStdDe', 'FrntLeftRdrObj11RdrObjDy', 'FrntLeftRdrObj11RdrObjDynProp', 'FrntLeftRdrObj11RdrObjDyStdDe', 'FrntLeftRdrObj11RdrObjExistProb', 'FrntLeftRdrObj11RdrObjHeight', 'FrntLeftRdrObj11RdrObjHeightStdDe', 'FrntLeftRdrObj11RdrObjID', 'FrntLeftRdrObj11RdrObjLifeCycle', 'FrntLeftRdrObj11RdrObjPwr', 'FrntLeftRdrObj11RdrObjVx', 'FrntLeftRdrObj11RdrObjVxStdDe', 'FrntLeftRdrObj11RdrObjVy', 'FrntLeftRdrObj11RdrObjVyStdDe']}
    sig_group_dataid_dict = {}

    class FrntLeftRdrObj10RdrObjDynProp:
        sig_name = "FrntLeftRdrObj10RdrObjDynProp"
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
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class FrntLeftRdrObj12RdrObjVyStdDe:
        sig_name = "FrntLeftRdrObj12RdrObjVyStdDe"
        sig_start_bit = 497
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 497
        bmuws_info = [(62, 0b00000011, 0b11111100, 2, 0), (63, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeftRdrObj12RdrObjID:
        sig_name = "FrntLeftRdrObj12RdrObjID"
        sig_start_bit = 454
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 454
        byte = 56
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class FrntLeftRdrObj12RdrObjHeight:
        sig_name = "FrntLeftRdrObj12RdrObjHeight"
        sig_start_bit = 426
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 426
        bmuws_info = [(53, 0b00000111, 0b11111000, 3, 0), (54, 0b11111110, 0b00000001, 7, 1)]

    class FrntLeftRdrObj10RdrObjCntr:
        sig_name = "FrntLeftRdrObj10RdrObjCntr"
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

    class FrntLeftRdrObj12RdrObjDyStdDe:
        sig_name = "FrntLeftRdrObj12RdrObjDyStdDe"
        sig_start_bit = 415
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 415
        bmuws_info = [(51, 0b11111111, 0b00000000, 8, 0), (52, 0b11100000, 0b00011111, 3, 5)]

    class FrntLeftRdrObj11RdrObjExistProb:
        sig_name = "FrntLeftRdrObj11RdrObjExistProb"
        sig_start_bit = 252
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 252
        bmuws_info = [(31, 0b00011111, 0b11100000, 5, 0), (32, 0b11111000, 0b00000111, 5, 3)]

    class FrntLeftRdrObj12RdrObjDynProp:
        sig_name = "FrntLeftRdrObj12RdrObjDynProp"
        sig_start_bit = 396
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 396
        byte = 49
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class FrntLeftRdrObj12RdrObjChks:
        sig_name = "FrntLeftRdrObj12RdrObjChks"
        sig_start_bit = 351
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
        startbit = 351
        byte = 43
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntLeftRdrObj12RdrObjVy:
        sig_name = "FrntLeftRdrObj12RdrObjVy"
        sig_start_bit = 492
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 492
        bmuws_info = [(61, 0b00011111, 0b11100000, 5, 0), (62, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeftRdrObj10_UB:
        sig_name = "FrntLeftRdrObj10_UB"
        sig_start_bit = 175
        update_id_bit = 175
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
        startbit = 175
        byte = 21
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class FrntLeftRdrObj10RdrObjVx:
        sig_name = "FrntLeftRdrObj10RdrObjVx"
        sig_start_bit = 121
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 121
        bmuws_info = [(15, 0b00000011, 0b11111100, 2, 0), (16, 0b11111111, 0b00000000, 8, 0), (17, 0b10000000, 0b01111111, 1, 7)]

    class FrntLeftRdrObj12RdrObjVxStdDe:
        sig_name = "FrntLeftRdrObj12RdrObjVxStdDe"
        sig_start_bit = 486
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 486
        bmuws_info = [(60, 0b01111111, 0b10000000, 7, 0), (61, 0b11100000, 0b00011111, 3, 5)]

    class FrntLeftRdrObj10ObjBoxCenterLat:
        sig_name = "FrntLeftRdrObj10ObjBoxCenterLat"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
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

    class FrntLeftRdrObj11RdrObjCntr:
        sig_name = "FrntLeftRdrObj11RdrObjCntr"
        sig_start_bit = 191
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
        startbit = 191
        byte = 23
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class FrntLeftRdrObj11RdrObjVx:
        sig_name = "FrntLeftRdrObj11RdrObjVx"
        sig_start_bit = 297
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 297
        bmuws_info = [(37, 0b00000011, 0b11111100, 2, 0), (38, 0b11111111, 0b00000000, 8, 0), (39, 0b10000000, 0b01111111, 1, 7)]

    class FrntLeftRdrObj11RdrObjVy:
        sig_name = "FrntLeftRdrObj11RdrObjVy"
        sig_start_bit = 324
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 324
        bmuws_info = [(40, 0b00011111, 0b11100000, 5, 0), (41, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeftRdrObj10RdrObjVyStdDe:
        sig_name = "FrntLeftRdrObj10RdrObjVyStdDe"
        sig_start_bit = 153
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 153
        bmuws_info = [(19, 0b00000011, 0b11111100, 2, 0), (20, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeftRdrObj12RdrObjDy:
        sig_name = "FrntLeftRdrObj12RdrObjDy"
        sig_start_bit = 395
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 395
        bmuws_info = [(49, 0b00001111, 0b11110000, 4, 0), (50, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeftRdrObj10RdrObjDx:
        sig_name = "FrntLeftRdrObj10RdrObjDx"
        sig_start_bit = 11
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 11
        bmuws_info = [(1, 0b00001111, 0b11110000, 4, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeftRdrObj12RdrObjDxStdDe:
        sig_name = "FrntLeftRdrObj12RdrObjDxStdDe"
        sig_start_bit = 391
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 391
        bmuws_info = [(48, 0b11111111, 0b00000000, 8, 0), (49, 0b11100000, 0b00011111, 3, 5)]

    class FrntLeftRdrObj11ObjBoxCenterLat:
        sig_name = "FrntLeftRdrObj11ObjBoxCenterLat"
        sig_start_bit = 215
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 215
        byte = 26
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntLeftRdrObj11RdrObjChks:
        sig_name = "FrntLeftRdrObj11RdrObjChks"
        sig_start_bit = 183
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
        startbit = 183
        byte = 22
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntLeftRdrObj10RdrObjHeight:
        sig_name = "FrntLeftRdrObj10RdrObjHeight"
        sig_start_bit = 82
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 82
        bmuws_info = [(10, 0b00000111, 0b11111000, 3, 0), (11, 0b11111110, 0b00000001, 7, 1)]

    class FrntLeftRdrObj11RdrObjLifeCycle:
        sig_name = "FrntLeftRdrObj11RdrObjLifeCycle"
        sig_start_bit = 280
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
        startbit = 280
        bmuws_info = [(35, 0b00000001, 0b11111110, 1, 0), (36, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeftRdrObj12RdrObjPwr:
        sig_name = "FrntLeftRdrObj12RdrObjPwr"
        sig_start_bit = 457
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 457
        bmuws_info = [(57, 0b00000011, 0b11111100, 2, 0), (58, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeftRdrObj11ObjBoxCenterLgt:
        sig_name = "FrntLeftRdrObj11ObjBoxCenterLgt"
        sig_start_bit = 207
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 207
        byte = 25
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntLeftRdrObj12_UB:
        sig_name = "FrntLeftRdrObj12_UB"
        sig_start_bit = 171
        update_id_bit = 171
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
        startbit = 171
        byte = 21
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class FrntLeftRdrObj12ObjBoxCenterLgt:
        sig_name = "FrntLeftRdrObj12ObjBoxCenterLgt"
        sig_start_bit = 375
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 375
        byte = 46
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntLeftRdrObj11RdrObjPwr:
        sig_name = "FrntLeftRdrObj11RdrObjPwr"
        sig_start_bit = 289
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 289
        bmuws_info = [(36, 0b00000011, 0b11111100, 2, 0), (37, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeftRdrObj10RdrObjID:
        sig_name = "FrntLeftRdrObj10RdrObjID"
        sig_start_bit = 110
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 110
        byte = 13
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class FrntLeftRdrObj11RdrObjVxStdDe:
        sig_name = "FrntLeftRdrObj11RdrObjVxStdDe"
        sig_start_bit = 318
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 318
        bmuws_info = [(39, 0b01111111, 0b10000000, 7, 0), (40, 0b11100000, 0b00011111, 3, 5)]

    class FrntLeftRdrObj10ObjBoxCenterLgt:
        sig_name = "FrntLeftRdrObj10ObjBoxCenterLgt"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
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

    class FrntLeftRdrObj10RdrObjHeightStdDe:
        sig_name = "FrntLeftRdrObj10RdrObjHeightStdDe"
        sig_start_bit = 88
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 88
        bmuws_info = [(11, 0b00000001, 0b11111110, 1, 0), (12, 0b11111111, 0b00000000, 8, 0), (13, 0b10000000, 0b01111111, 1, 7)]

    class FrntLeftRdrObj10RdrObjDy:
        sig_name = "FrntLeftRdrObj10RdrObjDy"
        sig_start_bit = 51
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 51
        bmuws_info = [(6, 0b00001111, 0b11110000, 4, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeftRdrObj10RdrObjLifeCycle:
        sig_name = "FrntLeftRdrObj10RdrObjLifeCycle"
        sig_start_bit = 104
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
        startbit = 104
        bmuws_info = [(13, 0b00000001, 0b11111110, 1, 0), (14, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeftRdrObj12RdrObjVx:
        sig_name = "FrntLeftRdrObj12RdrObjVx"
        sig_start_bit = 465
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 465
        bmuws_info = [(58, 0b00000011, 0b11111100, 2, 0), (59, 0b11111111, 0b00000000, 8, 0), (60, 0b10000000, 0b01111111, 1, 7)]

    class FrntLeftRdrObj11RdrObjDy:
        sig_name = "FrntLeftRdrObj11RdrObjDy"
        sig_start_bit = 227
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 227
        bmuws_info = [(28, 0b00001111, 0b11110000, 4, 0), (29, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeftRdrObj12RdrObjHeightStdDe:
        sig_name = "FrntLeftRdrObj12RdrObjHeightStdDe"
        sig_start_bit = 432
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 432
        bmuws_info = [(54, 0b00000001, 0b11111110, 1, 0), (55, 0b11111111, 0b00000000, 8, 0), (56, 0b10000000, 0b01111111, 1, 7)]

    class FrntLeftRdrObj12RdrObjCntr:
        sig_name = "FrntLeftRdrObj12RdrObjCntr"
        sig_start_bit = 359
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
        startbit = 359
        byte = 44
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class FrntLeftRdrObj10RdrObjVy:
        sig_name = "FrntLeftRdrObj10RdrObjVy"
        sig_start_bit = 148
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 148
        bmuws_info = [(18, 0b00011111, 0b11100000, 5, 0), (19, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeftRdrObj12RdrObjLifeCycle:
        sig_name = "FrntLeftRdrObj12RdrObjLifeCycle"
        sig_start_bit = 448
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
        startbit = 448
        bmuws_info = [(56, 0b00000001, 0b11111110, 1, 0), (57, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeftRdrObj10RdrObjChks:
        sig_name = "FrntLeftRdrObj10RdrObjChks"
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

    class FrntLeftRdrObj12RdrObjDx:
        sig_name = "FrntLeftRdrObj12RdrObjDx"
        sig_start_bit = 355
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 355
        bmuws_info = [(44, 0b00001111, 0b11110000, 4, 0), (45, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeftRdrObj11RdrObjDynProp:
        sig_name = "FrntLeftRdrObj11RdrObjDynProp"
        sig_start_bit = 228
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 228
        byte = 28
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class FrntLeftRdrObj10RdrObjDyStdDe:
        sig_name = "FrntLeftRdrObj10RdrObjDyStdDe"
        sig_start_bit = 71
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 71
        bmuws_info = [(8, 0b11111111, 0b00000000, 8, 0), (9, 0b11100000, 0b00011111, 3, 5)]

    class FrntLeftRdrObj12RdrObjExistProb:
        sig_name = "FrntLeftRdrObj12RdrObjExistProb"
        sig_start_bit = 420
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 420
        bmuws_info = [(52, 0b00011111, 0b11100000, 5, 0), (53, 0b11111000, 0b00000111, 5, 3)]

    class FrntLeftRdrObj10RdrObjDxStdDe:
        sig_name = "FrntLeftRdrObj10RdrObjDxStdDe"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11100000, 0b00011111, 3, 5)]

    class FrntLeftRdrObj11RdrObjID:
        sig_name = "FrntLeftRdrObj11RdrObjID"
        sig_start_bit = 286
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 286
        byte = 35
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class FrntLeftRdrObj11RdrObjDxStdDe:
        sig_name = "FrntLeftRdrObj11RdrObjDxStdDe"
        sig_start_bit = 223
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 223
        bmuws_info = [(27, 0b11111111, 0b00000000, 8, 0), (28, 0b11100000, 0b00011111, 3, 5)]

    class FrntLeftRdrObj11RdrObjHeightStdDe:
        sig_name = "FrntLeftRdrObj11RdrObjHeightStdDe"
        sig_start_bit = 264
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 264
        bmuws_info = [(33, 0b00000001, 0b11111110, 1, 0), (34, 0b11111111, 0b00000000, 8, 0), (35, 0b10000000, 0b01111111, 1, 7)]

    class FrntLeftRdrObj11_UB:
        sig_name = "FrntLeftRdrObj11_UB"
        sig_start_bit = 168
        update_id_bit = 168
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
        startbit = 168
        byte = 21
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FrntLeftRdrObj12ObjBoxCenterLat:
        sig_name = "FrntLeftRdrObj12ObjBoxCenterLat"
        sig_start_bit = 383
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 383
        byte = 47
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntLeftRdrObj11RdrObjDx:
        sig_name = "FrntLeftRdrObj11RdrObjDx"
        sig_start_bit = 187
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 187
        bmuws_info = [(23, 0b00001111, 0b11110000, 4, 0), (24, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeftRdrObj10RdrObjExistProb:
        sig_name = "FrntLeftRdrObj10RdrObjExistProb"
        sig_start_bit = 76
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 76
        bmuws_info = [(9, 0b00011111, 0b11100000, 5, 0), (10, 0b11111000, 0b00000111, 5, 3)]

    class FrntLeftRdrObj11RdrObjVyStdDe:
        sig_name = "FrntLeftRdrObj11RdrObjVyStdDe"
        sig_start_bit = 329
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 329
        bmuws_info = [(41, 0b00000011, 0b11111100, 2, 0), (42, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeftRdrObj11RdrObjHeight:
        sig_name = "FrntLeftRdrObj11RdrObjHeight"
        sig_start_bit = 258
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 258
        bmuws_info = [(32, 0b00000111, 0b11111000, 3, 0), (33, 0b11111110, 0b00000001, 7, 1)]

    class FrntLeftRdrObj10RdrObjVxStdDe:
        sig_name = "FrntLeftRdrObj10RdrObjVxStdDe"
        sig_start_bit = 142
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 142
        bmuws_info = [(17, 0b01111111, 0b10000000, 7, 0), (18, 0b11100000, 0b00011111, 3, 5)]

    class FrntLeftRdrObj11RdrObjDyStdDe:
        sig_name = "FrntLeftRdrObj11RdrObjDyStdDe"
        sig_start_bit = 247
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 247
        bmuws_info = [(30, 0b11111111, 0b00000000, 8, 0), (31, 0b11100000, 0b00011111, 3, 5)]

    class FrntLeftRdrObj10RdrObjPwr:
        sig_name = "FrntLeftRdrObj10RdrObjPwr"
        sig_start_bit = 113
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 113
        bmuws_info = [(14, 0b00000011, 0b11111100, 2, 0), (15, 0b11111100, 0b00000011, 6, 2)]


class BgmADCANFDFr08:
    msg_name = "BgmADCANFDFr08"
    msg_id = 498
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "BGM"
    rx_nodes = ['ACU']
    sig_group_dict = {'FrntLeftRdrObj7': ['FrntLeftRdrObj7ObjBoxCenterLat', 'FrntLeftRdrObj7ObjBoxCenterLgt', 'FrntLeftRdrObj7RdrObjChks', 'FrntLeftRdrObj7RdrObjCntr', 'FrntLeftRdrObj7RdrObjDx', 'FrntLeftRdrObj7RdrObjDxStdDe', 'FrntLeftRdrObj7RdrObjDy', 'FrntLeftRdrObj7RdrObjDynProp', 'FrntLeftRdrObj7RdrObjDyStdDe', 'FrntLeftRdrObj7RdrObjExistProb', 'FrntLeftRdrObj7RdrObjHeight', 'FrntLeftRdrObj7RdrObjHeightStdDe', 'FrntLeftRdrObj7RdrObjID', 'FrntLeftRdrObj7RdrObjLifeCycle', 'FrntLeftRdrObj7RdrObjPwr', 'FrntLeftRdrObj7RdrObjVx', 'FrntLeftRdrObj7RdrObjVxStdDe', 'FrntLeftRdrObj7RdrObjVy', 'FrntLeftRdrObj7RdrObjVyStdDe'], 'FrntLeftRdrObj9': ['FrntLeftRdrObj9ObjBoxCenterLat', 'FrntLeftRdrObj9ObjBoxCenterLgt', 'FrntLeftRdrObj9RdrObjChks', 'FrntLeftRdrObj9RdrObjCntr', 'FrntLeftRdrObj9RdrObjDx', 'FrntLeftRdrObj9RdrObjDxStdDe', 'FrntLeftRdrObj9RdrObjDy', 'FrntLeftRdrObj9RdrObjDynProp', 'FrntLeftRdrObj9RdrObjDyStdDe', 'FrntLeftRdrObj9RdrObjExistProb', 'FrntLeftRdrObj9RdrObjHeight', 'FrntLeftRdrObj9RdrObjHeightStdDe', 'FrntLeftRdrObj9RdrObjID', 'FrntLeftRdrObj9RdrObjLifeCycle', 'FrntLeftRdrObj9RdrObjPwr', 'FrntLeftRdrObj9RdrObjVx', 'FrntLeftRdrObj9RdrObjVxStdDe', 'FrntLeftRdrObj9RdrObjVy', 'FrntLeftRdrObj9RdrObjVyStdDe'], 'FrntLeftRdrObj8': ['FrntLeftRdrObj8ObjBoxCenterLat', 'FrntLeftRdrObj8ObjBoxCenterLgt', 'FrntLeftRdrObj8RdrObjChks', 'FrntLeftRdrObj8RdrObjCntr', 'FrntLeftRdrObj8RdrObjDx', 'FrntLeftRdrObj8RdrObjDxStdDe', 'FrntLeftRdrObj8RdrObjDy', 'FrntLeftRdrObj8RdrObjDynProp', 'FrntLeftRdrObj8RdrObjDyStdDe', 'FrntLeftRdrObj8RdrObjExistProb', 'FrntLeftRdrObj8RdrObjHeight', 'FrntLeftRdrObj8RdrObjHeightStdDe', 'FrntLeftRdrObj8RdrObjID', 'FrntLeftRdrObj8RdrObjLifeCycle', 'FrntLeftRdrObj8RdrObjPwr', 'FrntLeftRdrObj8RdrObjVx', 'FrntLeftRdrObj8RdrObjVxStdDe', 'FrntLeftRdrObj8RdrObjVy', 'FrntLeftRdrObj8RdrObjVyStdDe']}
    sig_group_dataid_dict = {}

    class FrntLeftRdrObj9RdrObjVxStdDe:
        sig_name = "FrntLeftRdrObj9RdrObjVxStdDe"
        sig_start_bit = 486
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 486
        bmuws_info = [(60, 0b01111111, 0b10000000, 7, 0), (61, 0b11100000, 0b00011111, 3, 5)]

    class FrntLeftRdrObj8RdrObjDx:
        sig_name = "FrntLeftRdrObj8RdrObjDx"
        sig_start_bit = 187
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 187
        bmuws_info = [(23, 0b00001111, 0b11110000, 4, 0), (24, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeftRdrObj9RdrObjDy:
        sig_name = "FrntLeftRdrObj9RdrObjDy"
        sig_start_bit = 395
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 395
        bmuws_info = [(49, 0b00001111, 0b11110000, 4, 0), (50, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeftRdrObj7RdrObjExistProb:
        sig_name = "FrntLeftRdrObj7RdrObjExistProb"
        sig_start_bit = 76
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 76
        bmuws_info = [(9, 0b00011111, 0b11100000, 5, 0), (10, 0b11111000, 0b00000111, 5, 3)]

    class FrntLeftRdrObj9RdrObjDxStdDe:
        sig_name = "FrntLeftRdrObj9RdrObjDxStdDe"
        sig_start_bit = 391
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 391
        bmuws_info = [(48, 0b11111111, 0b00000000, 8, 0), (49, 0b11100000, 0b00011111, 3, 5)]

    class FrntLeftRdrObj9RdrObjHeightStdDe:
        sig_name = "FrntLeftRdrObj9RdrObjHeightStdDe"
        sig_start_bit = 432
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 432
        bmuws_info = [(54, 0b00000001, 0b11111110, 1, 0), (55, 0b11111111, 0b00000000, 8, 0), (56, 0b10000000, 0b01111111, 1, 7)]

    class FrntLeftRdrObj8RdrObjVy:
        sig_name = "FrntLeftRdrObj8RdrObjVy"
        sig_start_bit = 324
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 324
        bmuws_info = [(40, 0b00011111, 0b11100000, 5, 0), (41, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeftRdrObj9RdrObjHeight:
        sig_name = "FrntLeftRdrObj9RdrObjHeight"
        sig_start_bit = 426
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 426
        bmuws_info = [(53, 0b00000111, 0b11111000, 3, 0), (54, 0b11111110, 0b00000001, 7, 1)]

    class FrntLeftRdrObj9RdrObjChks:
        sig_name = "FrntLeftRdrObj9RdrObjChks"
        sig_start_bit = 351
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
        startbit = 351
        byte = 43
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntLeftRdrObj7RdrObjChks:
        sig_name = "FrntLeftRdrObj7RdrObjChks"
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

    class FrntLeftRdrObj8RdrObjCntr:
        sig_name = "FrntLeftRdrObj8RdrObjCntr"
        sig_start_bit = 191
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
        startbit = 191
        byte = 23
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class FrntLeftRdrObj8RdrObjDxStdDe:
        sig_name = "FrntLeftRdrObj8RdrObjDxStdDe"
        sig_start_bit = 223
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 223
        bmuws_info = [(27, 0b11111111, 0b00000000, 8, 0), (28, 0b11100000, 0b00011111, 3, 5)]

    class FrntLeftRdrObj8RdrObjChks:
        sig_name = "FrntLeftRdrObj8RdrObjChks"
        sig_start_bit = 183
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
        startbit = 183
        byte = 22
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntLeftRdrObj9RdrObjVx:
        sig_name = "FrntLeftRdrObj9RdrObjVx"
        sig_start_bit = 465
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 465
        bmuws_info = [(58, 0b00000011, 0b11111100, 2, 0), (59, 0b11111111, 0b00000000, 8, 0), (60, 0b10000000, 0b01111111, 1, 7)]

    class FrntLeftRdrObj9RdrObjDynProp:
        sig_name = "FrntLeftRdrObj9RdrObjDynProp"
        sig_start_bit = 396
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 396
        byte = 49
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class FrntLeftRdrObj9RdrObjCntr:
        sig_name = "FrntLeftRdrObj9RdrObjCntr"
        sig_start_bit = 359
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
        startbit = 359
        byte = 44
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class FrntLeftRdrObj8RdrObjVyStdDe:
        sig_name = "FrntLeftRdrObj8RdrObjVyStdDe"
        sig_start_bit = 329
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 329
        bmuws_info = [(41, 0b00000011, 0b11111100, 2, 0), (42, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeftRdrObj7RdrObjDyStdDe:
        sig_name = "FrntLeftRdrObj7RdrObjDyStdDe"
        sig_start_bit = 71
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 71
        bmuws_info = [(8, 0b11111111, 0b00000000, 8, 0), (9, 0b11100000, 0b00011111, 3, 5)]

    class FrntLeftRdrObj7RdrObjVy:
        sig_name = "FrntLeftRdrObj7RdrObjVy"
        sig_start_bit = 148
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 148
        bmuws_info = [(18, 0b00011111, 0b11100000, 5, 0), (19, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeftRdrObj7_UB:
        sig_name = "FrntLeftRdrObj7_UB"
        sig_start_bit = 175
        update_id_bit = 175
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
        startbit = 175
        byte = 21
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class FrntLeftRdrObj9_UB:
        sig_name = "FrntLeftRdrObj9_UB"
        sig_start_bit = 171
        update_id_bit = 171
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
        startbit = 171
        byte = 21
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class FrntLeftRdrObj7ObjBoxCenterLat:
        sig_name = "FrntLeftRdrObj7ObjBoxCenterLat"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
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

    class FrntLeftRdrObj7RdrObjDx:
        sig_name = "FrntLeftRdrObj7RdrObjDx"
        sig_start_bit = 11
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 11
        bmuws_info = [(1, 0b00001111, 0b11110000, 4, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeftRdrObj7ObjBoxCenterLgt:
        sig_name = "FrntLeftRdrObj7ObjBoxCenterLgt"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
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

    class FrntLeftRdrObj8RdrObjVx:
        sig_name = "FrntLeftRdrObj8RdrObjVx"
        sig_start_bit = 297
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 297
        bmuws_info = [(37, 0b00000011, 0b11111100, 2, 0), (38, 0b11111111, 0b00000000, 8, 0), (39, 0b10000000, 0b01111111, 1, 7)]

    class FrntLeftRdrObj8RdrObjDyStdDe:
        sig_name = "FrntLeftRdrObj8RdrObjDyStdDe"
        sig_start_bit = 247
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 247
        bmuws_info = [(30, 0b11111111, 0b00000000, 8, 0), (31, 0b11100000, 0b00011111, 3, 5)]

    class FrntLeftRdrObj7RdrObjID:
        sig_name = "FrntLeftRdrObj7RdrObjID"
        sig_start_bit = 110
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 110
        byte = 13
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class FrntLeftRdrObj9RdrObjDyStdDe:
        sig_name = "FrntLeftRdrObj9RdrObjDyStdDe"
        sig_start_bit = 415
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 415
        bmuws_info = [(51, 0b11111111, 0b00000000, 8, 0), (52, 0b11100000, 0b00011111, 3, 5)]

    class FrntLeftRdrObj8RdrObjHeight:
        sig_name = "FrntLeftRdrObj8RdrObjHeight"
        sig_start_bit = 258
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 258
        bmuws_info = [(32, 0b00000111, 0b11111000, 3, 0), (33, 0b11111110, 0b00000001, 7, 1)]

    class FrntLeftRdrObj9RdrObjPwr:
        sig_name = "FrntLeftRdrObj9RdrObjPwr"
        sig_start_bit = 457
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 457
        bmuws_info = [(57, 0b00000011, 0b11111100, 2, 0), (58, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeftRdrObj8RdrObjDynProp:
        sig_name = "FrntLeftRdrObj8RdrObjDynProp"
        sig_start_bit = 228
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 228
        byte = 28
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class FrntLeftRdrObj8RdrObjVxStdDe:
        sig_name = "FrntLeftRdrObj8RdrObjVxStdDe"
        sig_start_bit = 318
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 318
        bmuws_info = [(39, 0b01111111, 0b10000000, 7, 0), (40, 0b11100000, 0b00011111, 3, 5)]

    class FrntLeftRdrObj9RdrObjVyStdDe:
        sig_name = "FrntLeftRdrObj9RdrObjVyStdDe"
        sig_start_bit = 497
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 497
        bmuws_info = [(62, 0b00000011, 0b11111100, 2, 0), (63, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeftRdrObj8RdrObjLifeCycle:
        sig_name = "FrntLeftRdrObj8RdrObjLifeCycle"
        sig_start_bit = 280
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
        startbit = 280
        bmuws_info = [(35, 0b00000001, 0b11111110, 1, 0), (36, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeftRdrObj9ObjBoxCenterLat:
        sig_name = "FrntLeftRdrObj9ObjBoxCenterLat"
        sig_start_bit = 383
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 383
        byte = 47
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntLeftRdrObj8_UB:
        sig_name = "FrntLeftRdrObj8_UB"
        sig_start_bit = 168
        update_id_bit = 168
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
        startbit = 168
        byte = 21
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FrntLeftRdrObj7RdrObjDynProp:
        sig_name = "FrntLeftRdrObj7RdrObjDynProp"
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
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class FrntLeftRdrObj8ObjBoxCenterLgt:
        sig_name = "FrntLeftRdrObj8ObjBoxCenterLgt"
        sig_start_bit = 207
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 207
        byte = 25
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntLeftRdrObj8RdrObjID:
        sig_name = "FrntLeftRdrObj8RdrObjID"
        sig_start_bit = 286
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 286
        byte = 35
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class FrntLeftRdrObj7RdrObjVyStdDe:
        sig_name = "FrntLeftRdrObj7RdrObjVyStdDe"
        sig_start_bit = 153
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 153
        bmuws_info = [(19, 0b00000011, 0b11111100, 2, 0), (20, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeftRdrObj8RdrObjPwr:
        sig_name = "FrntLeftRdrObj8RdrObjPwr"
        sig_start_bit = 289
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 289
        bmuws_info = [(36, 0b00000011, 0b11111100, 2, 0), (37, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeftRdrObj7RdrObjHeightStdDe:
        sig_name = "FrntLeftRdrObj7RdrObjHeightStdDe"
        sig_start_bit = 88
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 88
        bmuws_info = [(11, 0b00000001, 0b11111110, 1, 0), (12, 0b11111111, 0b00000000, 8, 0), (13, 0b10000000, 0b01111111, 1, 7)]

    class FrntLeftRdrObj7RdrObjVxStdDe:
        sig_name = "FrntLeftRdrObj7RdrObjVxStdDe"
        sig_start_bit = 142
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 142
        bmuws_info = [(17, 0b01111111, 0b10000000, 7, 0), (18, 0b11100000, 0b00011111, 3, 5)]

    class FrntLeftRdrObj8RdrObjHeightStdDe:
        sig_name = "FrntLeftRdrObj8RdrObjHeightStdDe"
        sig_start_bit = 264
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 264
        bmuws_info = [(33, 0b00000001, 0b11111110, 1, 0), (34, 0b11111111, 0b00000000, 8, 0), (35, 0b10000000, 0b01111111, 1, 7)]

    class FrntLeftRdrObj8ObjBoxCenterLat:
        sig_name = "FrntLeftRdrObj8ObjBoxCenterLat"
        sig_start_bit = 215
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 215
        byte = 26
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntLeftRdrObj9ObjBoxCenterLgt:
        sig_name = "FrntLeftRdrObj9ObjBoxCenterLgt"
        sig_start_bit = 375
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 375
        byte = 46
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntLeftRdrObj9RdrObjLifeCycle:
        sig_name = "FrntLeftRdrObj9RdrObjLifeCycle"
        sig_start_bit = 448
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
        startbit = 448
        bmuws_info = [(56, 0b00000001, 0b11111110, 1, 0), (57, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeftRdrObj7RdrObjHeight:
        sig_name = "FrntLeftRdrObj7RdrObjHeight"
        sig_start_bit = 82
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 82
        bmuws_info = [(10, 0b00000111, 0b11111000, 3, 0), (11, 0b11111110, 0b00000001, 7, 1)]

    class FrntLeftRdrObj7RdrObjPwr:
        sig_name = "FrntLeftRdrObj7RdrObjPwr"
        sig_start_bit = 113
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 113
        bmuws_info = [(14, 0b00000011, 0b11111100, 2, 0), (15, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeftRdrObj7RdrObjVx:
        sig_name = "FrntLeftRdrObj7RdrObjVx"
        sig_start_bit = 121
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 121
        bmuws_info = [(15, 0b00000011, 0b11111100, 2, 0), (16, 0b11111111, 0b00000000, 8, 0), (17, 0b10000000, 0b01111111, 1, 7)]

    class FrntLeftRdrObj9RdrObjVy:
        sig_name = "FrntLeftRdrObj9RdrObjVy"
        sig_start_bit = 492
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 492
        bmuws_info = [(61, 0b00011111, 0b11100000, 5, 0), (62, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeftRdrObj9RdrObjDx:
        sig_name = "FrntLeftRdrObj9RdrObjDx"
        sig_start_bit = 355
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 355
        bmuws_info = [(44, 0b00001111, 0b11110000, 4, 0), (45, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeftRdrObj8RdrObjDy:
        sig_name = "FrntLeftRdrObj8RdrObjDy"
        sig_start_bit = 227
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 227
        bmuws_info = [(28, 0b00001111, 0b11110000, 4, 0), (29, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeftRdrObj8RdrObjExistProb:
        sig_name = "FrntLeftRdrObj8RdrObjExistProb"
        sig_start_bit = 252
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 252
        bmuws_info = [(31, 0b00011111, 0b11100000, 5, 0), (32, 0b11111000, 0b00000111, 5, 3)]

    class FrntLeftRdrObj9RdrObjID:
        sig_name = "FrntLeftRdrObj9RdrObjID"
        sig_start_bit = 454
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 454
        byte = 56
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class FrntLeftRdrObj7RdrObjDxStdDe:
        sig_name = "FrntLeftRdrObj7RdrObjDxStdDe"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11100000, 0b00011111, 3, 5)]

    class FrntLeftRdrObj7RdrObjCntr:
        sig_name = "FrntLeftRdrObj7RdrObjCntr"
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

    class FrntLeftRdrObj9RdrObjExistProb:
        sig_name = "FrntLeftRdrObj9RdrObjExistProb"
        sig_start_bit = 420
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 420
        bmuws_info = [(52, 0b00011111, 0b11100000, 5, 0), (53, 0b11111000, 0b00000111, 5, 3)]

    class FrntLeftRdrObj7RdrObjLifeCycle:
        sig_name = "FrntLeftRdrObj7RdrObjLifeCycle"
        sig_start_bit = 104
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
        startbit = 104
        bmuws_info = [(13, 0b00000001, 0b11111110, 1, 0), (14, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeftRdrObj7RdrObjDy:
        sig_name = "FrntLeftRdrObj7RdrObjDy"
        sig_start_bit = 51
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 51
        bmuws_info = [(6, 0b00001111, 0b11110000, 4, 0), (7, 0b11111111, 0b00000000, 8, 0)]


class BgmADCANFDFr30:
    msg_name = "BgmADCANFDFr30"
    msg_id = 640
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 16
    tx_node = "BGM"
    rx_nodes = ['ACU']
    sig_group_dict = {'SteerWhlScRightButtonLe': ['SteerWhlScRightButtonLeChks', 'SteerWhlScRightButtonLeCntr', 'SteerWhlScRightButtonLeSteerWhlTouchSwt2'], 'SteerWhlScLeftButtonLe': ['SteerWhlScLeftButtonLeChks', 'SteerWhlScLeftButtonLeCntr', 'SteerWhlScLeftButtonLeSteerWhlTouchSwt2'], 'SteerWhlScButtonMidLe2': ['SteerWhlScButtonMidLe2Chks', 'SteerWhlScButtonMidLe2Cntr', 'SteerWhlScButtonMidLe2SteerWhlTouchSwt2'], 'SteerWhlTouchTurnLightSwtLe': ['SteerWhlTouchTurnLightSwtLeChks', 'SteerWhlTouchTurnLightSwtLeCntr', 'SteerWhlTouchTurnLightSwtLeSteerWhlTouchTurnLightSwtLe'], 'SteerWhlTouchTurnLightSwtRi': ['SteerWhlTouchTurnLightSwtRiChks', 'SteerWhlTouchTurnLightSwtRiCntr', 'SteerWhlTouchTurnLightSwtRiSteerWhlTouchTurnLightSwtLe'], 'SteerWhlScButtonMidLe1': ['SteerWhlScButtonMidLe1Chks', 'SteerWhlScButtonMidLe1Cntr', 'SteerWhlScButtonMidLe1SteerWhlTouchSwt1']}
    sig_group_dataid_dict = {'SteerWhlScRightButtonLe': 8090, 'SteerWhlScLeftButtonLe': 8089, 'SteerWhlScButtonMidLe2': 8088, 'SteerWhlTouchTurnLightSwtLe': 8093, 'SteerWhlTouchTurnLightSwtRi': 8092, 'SteerWhlScButtonMidLe1': 8087}

    class SteerWhlTouchTurnLightSwtLeChks:
        sig_name = "SteerWhlTouchTurnLightSwtLeChks"
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

    class SteerWhlScButtonMidLe2SteerWhlTouchSwt2:
        sig_name = "SteerWhlScButtonMidLe2SteerWhlTouchSwt2"
        sig_start_bit = 87
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SteerWhlTouchSwt_NotAvailble': 0, 'SteerWhlTouchSwt_ShortPress': 1, 'SteerWhlTouchSwt_LongPress': 2, 'SteerWhlTouchSwt_Error': 3}
        compute_method = None
        length = 2
        startbit = 87
        byte = 10
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class SteerWhlTouchTurnLightSwtLeCntr:
        sig_name = "SteerWhlTouchTurnLightSwtLeCntr"
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

    class SteerWhlTouchTurnLightSwtRiChks:
        sig_name = "SteerWhlTouchTurnLightSwtRiChks"
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

    class SteerWhlScButtonMidLe1Cntr:
        sig_name = "SteerWhlScButtonMidLe1Cntr"
        sig_start_bit = 67
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
        startbit = 67
        byte = 8
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class SteerWhlScRightButtonLeChks:
        sig_name = "SteerWhlScRightButtonLeChks"
        sig_start_bit = 111
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
        startbit = 111
        byte = 13
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SteerWhlScRightButtonLe_UB:
        sig_name = "SteerWhlScRightButtonLe_UB"
        sig_start_bit = 116
        update_id_bit = 116
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
        startbit = 116
        byte = 14
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class SteerWhlTouchTurnLightSwtRiSteerWhlTouchTurnLightSwtLe:
        sig_name = "SteerWhlTouchTurnLightSwtRiSteerWhlTouchTurnLightSwtLe"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SteerWhlTouchTurnLightSwt_NotAvailable': 0, 'SteerWhlTouchTurnLightSwt_LightPress': 1, 'SteerWhlTouchTurnLightSwt_FullPress': 2, 'SteerWhlTouchTurnLightSwt_Error': 3}
        compute_method = None
        length = 2
        startbit = 31
        byte = 3
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class SteerWhlScLeftButtonLe_UB:
        sig_name = "SteerWhlScLeftButtonLe_UB"
        sig_start_bit = 100
        update_id_bit = 100
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
        startbit = 100
        byte = 12
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class SteerWhlScButtonMidLe2_UB:
        sig_name = "SteerWhlScButtonMidLe2_UB"
        sig_start_bit = 84
        update_id_bit = 84
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
        startbit = 84
        byte = 10
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class SteerWhlScLeftButtonLeChks:
        sig_name = "SteerWhlScLeftButtonLeChks"
        sig_start_bit = 95
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
        startbit = 95
        byte = 11
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SteerWhlScLeftButtonLeSteerWhlTouchSwt2:
        sig_name = "SteerWhlScLeftButtonLeSteerWhlTouchSwt2"
        sig_start_bit = 103
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SteerWhlTouchSwt_NotAvailble': 0, 'SteerWhlTouchSwt_ShortPress': 1, 'SteerWhlTouchSwt_LongPress': 2, 'SteerWhlTouchSwt_Error': 3}
        compute_method = None
        length = 2
        startbit = 103
        byte = 12
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class SteerWhlScButtonMidLe1Chks:
        sig_name = "SteerWhlScButtonMidLe1Chks"
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

    class SteerWhlScButtonMidLe1SteerWhlTouchSwt1:
        sig_name = "SteerWhlScButtonMidLe1SteerWhlTouchSwt1"
        sig_start_bit = 71
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SteerWhlTouchSwt2_NotAvalible': 0, 'SteerWhlTouchSwt2_UpPsd': 1, 'SteerWhlTouchSwt2_LongUpPsd': 2, 'SteerWhlTouchSwt2_DownPsd': 3, 'SteerWhlTouchSwt2_LongDownPsd': 4, 'SteerWhlTouchSwt2_Error': 5}
        compute_method = None
        length = 4
        startbit = 71
        byte = 8
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class SteerWhlTouchTurnLightSwtLeSteerWhlTouchTurnLightSwtLe:
        sig_name = "SteerWhlTouchTurnLightSwtLeSteerWhlTouchTurnLightSwtLe"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SteerWhlTouchTurnLightSwt_NotAvailable': 0, 'SteerWhlTouchTurnLightSwt_LightPress': 1, 'SteerWhlTouchTurnLightSwt_FullPress': 2, 'SteerWhlTouchTurnLightSwt_Error': 3}
        compute_method = None
        length = 2
        startbit = 15
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class SteerWhlTouchTurnLightSwtLe_UB:
        sig_name = "SteerWhlTouchTurnLightSwtLe_UB"
        sig_start_bit = 13
        update_id_bit = 13
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
        startbit = 13
        byte = 1
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class SteerWhlTouchTurnLightSwtRi_UB:
        sig_name = "SteerWhlTouchTurnLightSwtRi_UB"
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

    class SteerWhlScLeftButtonLeCntr:
        sig_name = "SteerWhlScLeftButtonLeCntr"
        sig_start_bit = 99
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
        startbit = 99
        byte = 12
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class SteerWhlScButtonMidLe1_UB:
        sig_name = "SteerWhlScButtonMidLe1_UB"
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

    class IgnRly3Cmd:
        sig_name = "IgnRly3Cmd"
        sig_start_bit = 47
        update_id_bit = 55
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

    class WhlMotSysCooltT:
        sig_name = "WhlMotSysCooltT"
        sig_start_bit = 39
        update_id_bit = 40
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
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SteerWhlScButtonMidLe2Cntr:
        sig_name = "SteerWhlScButtonMidLe2Cntr"
        sig_start_bit = 83
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
        startbit = 83
        byte = 10
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class SteerWhlScButtonMidLe2Chks:
        sig_name = "SteerWhlScButtonMidLe2Chks"
        sig_start_bit = 79
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
        startbit = 79
        byte = 9
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SteerWhlScRightButtonLeCntr:
        sig_name = "SteerWhlScRightButtonLeCntr"
        sig_start_bit = 115
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
        startbit = 115
        byte = 14
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class SteerWhlScRightButtonLeSteerWhlTouchSwt2:
        sig_name = "SteerWhlScRightButtonLeSteerWhlTouchSwt2"
        sig_start_bit = 119
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SteerWhlTouchSwt_NotAvailble': 0, 'SteerWhlTouchSwt_ShortPress': 1, 'SteerWhlTouchSwt_LongPress': 2, 'SteerWhlTouchSwt_Error': 3}
        compute_method = None
        length = 2
        startbit = 119
        byte = 14
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class SteerWhlTouchTurnLightSwtRiCntr:
        sig_name = "SteerWhlTouchTurnLightSwtRiCntr"
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


class BgmADCANFDFr23:
    msg_name = "BgmADCANFDFr23"
    msg_id = 515
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "BGM"
    rx_nodes = ['ACU']
    sig_group_dict = {'RearLeftRdrObj16': ['RearLeftRdrObj16ObjBoxCenterLat', 'RearLeftRdrObj16ObjBoxCenterLgt', 'RearLeftRdrObj16RdrObjChks', 'RearLeftRdrObj16RdrObjCntr', 'RearLeftRdrObj16RdrObjDx', 'RearLeftRdrObj16RdrObjDxStdDe', 'RearLeftRdrObj16RdrObjDy', 'RearLeftRdrObj16RdrObjDynProp', 'RearLeftRdrObj16RdrObjDyStdDe', 'RearLeftRdrObj16RdrObjExistProb', 'RearLeftRdrObj16RdrObjHeight', 'RearLeftRdrObj16RdrObjHeightStdDe', 'RearLeftRdrObj16RdrObjID', 'RearLeftRdrObj16RdrObjLifeCycle', 'RearLeftRdrObj16RdrObjPwr', 'RearLeftRdrObj16RdrObjVx', 'RearLeftRdrObj16RdrObjVxStdDe', 'RearLeftRdrObj16RdrObjVy', 'RearLeftRdrObj16RdrObjVyStdDe'], 'RearLeftRdrSync': ['RearLeftRdrSyncRdrObjTimeStampNSec', 'RearLeftRdrSyncRdrObjTimeStampSec', 'RearLeftRdrSyncRdrSyncChks', 'RearLeftRdrSyncRdrSyncCntr']}
    sig_group_dataid_dict = {}

    class RearLeftRdrObj16RdrObjDynProp:
        sig_name = "RearLeftRdrObj16RdrObjDynProp"
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
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class RearLeftRdrObj16RdrObjChks:
        sig_name = "RearLeftRdrObj16RdrObjChks"
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

    class RearLeftRdrObj16ObjBoxCenterLat:
        sig_name = "RearLeftRdrObj16ObjBoxCenterLat"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
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

    class RearLeftRdrObj16RdrObjID:
        sig_name = "RearLeftRdrObj16RdrObjID"
        sig_start_bit = 110
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 110
        byte = 13
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class RearLeftRdrObj16_UB:
        sig_name = "RearLeftRdrObj16_UB"
        sig_start_bit = 175
        update_id_bit = 175
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
        startbit = 175
        byte = 21
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class RearLeftRdrObj16ObjBoxCenterLgt:
        sig_name = "RearLeftRdrObj16ObjBoxCenterLgt"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
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

    class RearLeftRdrSyncRdrObjTimeStampNSec:
        sig_name = "RearLeftRdrSyncRdrObjTimeStampNSec"
        sig_start_bit = 207
        update_id_bit = None
        sig_length = 32
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4294967295
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 32
        startbit = 207
        bmuws_info = [(25, 0b11111111, 0b00000000, 8, 0), (26, 0b11111111, 0b00000000, 8, 0), (27, 0b11111111, 0b00000000, 8, 0), (28, 0b11111111, 0b00000000, 8, 0)]

    class RearLeftRdrObj16RdrObjDy:
        sig_name = "RearLeftRdrObj16RdrObjDy"
        sig_start_bit = 51
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 51
        bmuws_info = [(6, 0b00001111, 0b11110000, 4, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class RearLeftRdrObj16RdrObjVyStdDe:
        sig_name = "RearLeftRdrObj16RdrObjVyStdDe"
        sig_start_bit = 153
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 153
        bmuws_info = [(19, 0b00000011, 0b11111100, 2, 0), (20, 0b11111111, 0b00000000, 8, 0)]

    class RearLeftRdrSyncRdrObjTimeStampSec:
        sig_name = "RearLeftRdrSyncRdrObjTimeStampSec"
        sig_start_bit = 239
        update_id_bit = None
        sig_length = 32
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4294967295
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 32
        startbit = 239
        bmuws_info = [(29, 0b11111111, 0b00000000, 8, 0), (30, 0b11111111, 0b00000000, 8, 0), (31, 0b11111111, 0b00000000, 8, 0), (32, 0b11111111, 0b00000000, 8, 0)]

    class RearLeftRdrFault:
        sig_name = "RearLeftRdrFault"
        sig_start_bit = 171
        update_id_bit = 169
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
        startbit = 171
        byte = 21
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class RearLeftRdrSyncRdrSyncCntr:
        sig_name = "RearLeftRdrSyncRdrSyncCntr"
        sig_start_bit = 195
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
        startbit = 195
        byte = 24
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class RearLeftRdrObj16RdrObjDxStdDe:
        sig_name = "RearLeftRdrObj16RdrObjDxStdDe"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11100000, 0b00011111, 3, 5)]

    class RearLeftRdrObj16RdrObjExistProb:
        sig_name = "RearLeftRdrObj16RdrObjExistProb"
        sig_start_bit = 76
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 76
        bmuws_info = [(9, 0b00011111, 0b11100000, 5, 0), (10, 0b11111000, 0b00000111, 5, 3)]

    class RearLeftRdrObj16RdrObjPwr:
        sig_name = "RearLeftRdrObj16RdrObjPwr"
        sig_start_bit = 113
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 113
        bmuws_info = [(14, 0b00000011, 0b11111100, 2, 0), (15, 0b11111100, 0b00000011, 6, 2)]

    class RearLeftRdrObj16RdrObjVx:
        sig_name = "RearLeftRdrObj16RdrObjVx"
        sig_start_bit = 121
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 121
        bmuws_info = [(15, 0b00000011, 0b11111100, 2, 0), (16, 0b11111111, 0b00000000, 8, 0), (17, 0b10000000, 0b01111111, 1, 7)]

    class RearLeftRdrSyncRdrSyncChks:
        sig_name = "RearLeftRdrSyncRdrSyncChks"
        sig_start_bit = 191
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
        startbit = 191
        byte = 23
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearLeftRdrObj16RdrObjHeight:
        sig_name = "RearLeftRdrObj16RdrObjHeight"
        sig_start_bit = 82
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 82
        bmuws_info = [(10, 0b00000111, 0b11111000, 3, 0), (11, 0b11111110, 0b00000001, 7, 1)]

    class RearLeftRdrSync_UB:
        sig_name = "RearLeftRdrSync_UB"
        sig_start_bit = 271
        update_id_bit = 271
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
        startbit = 271
        byte = 33
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class RearLeftRdrObj16RdrObjVy:
        sig_name = "RearLeftRdrObj16RdrObjVy"
        sig_start_bit = 148
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 148
        bmuws_info = [(18, 0b00011111, 0b11100000, 5, 0), (19, 0b11111100, 0b00000011, 6, 2)]

    class RearLeftRdrObj16RdrObjLifeCycle:
        sig_name = "RearLeftRdrObj16RdrObjLifeCycle"
        sig_start_bit = 104
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
        startbit = 104
        bmuws_info = [(13, 0b00000001, 0b11111110, 1, 0), (14, 0b11111100, 0b00000011, 6, 2)]

    class RearLeftRdrObj16RdrObjVxStdDe:
        sig_name = "RearLeftRdrObj16RdrObjVxStdDe"
        sig_start_bit = 142
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 142
        bmuws_info = [(17, 0b01111111, 0b10000000, 7, 0), (18, 0b11100000, 0b00011111, 3, 5)]

    class RearLeftRdrObj16RdrObjCntr:
        sig_name = "RearLeftRdrObj16RdrObjCntr"
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

    class RearLeftRdrObj16RdrObjDx:
        sig_name = "RearLeftRdrObj16RdrObjDx"
        sig_start_bit = 11
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 11
        bmuws_info = [(1, 0b00001111, 0b11110000, 4, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class RearLeftRdrObj16RdrObjHeightStdDe:
        sig_name = "RearLeftRdrObj16RdrObjHeightStdDe"
        sig_start_bit = 88
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 88
        bmuws_info = [(11, 0b00000001, 0b11111110, 1, 0), (12, 0b11111111, 0b00000000, 8, 0), (13, 0b10000000, 0b01111111, 1, 7)]

    class RearLeftRdrObj16RdrObjDyStdDe:
        sig_name = "RearLeftRdrObj16RdrObjDyStdDe"
        sig_start_bit = 71
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 71
        bmuws_info = [(8, 0b11111111, 0b00000000, 8, 0), (9, 0b11100000, 0b00011111, 3, 5)]


class BgmADCANFDFr03:
    msg_name = "BgmADCANFDFr03"
    msg_id = 321
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['ACU']
    sig_group_dict = {'VehTiAndData': ['VehTiAndDataDataValid', 'VehTiAndDataDay', 'VehTiAndDataHr1', 'VehTiAndDataMins1', 'VehTiAndDataMth1', 'VehTiAndDataSec1', 'VehTiAndDataYr1']}
    sig_group_dataid_dict = {}

    class VehTiAndDataMth1:
        sig_name = "VehTiAndDataMth1"
        sig_start_bit = 35
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 35
        byte = 4
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class VehTiAndDataDay:
        sig_name = "VehTiAndDataDay"
        sig_start_bit = 28
        update_id_bit = None
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 28
        byte = 3
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class VehTiAndDataSec1:
        sig_name = "VehTiAndDataSec1"
        sig_start_bit = 5
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 5
        byte = 0
        mask = 0b00111111
        unmask = 0b11000000
        shift = 0

    class VehTiAndDataDataValid:
        sig_name = "VehTiAndDataDataValid"
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

    class VehTiAndData_UB:
        sig_name = "VehTiAndData_UB"
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

    class VehTiAndDataMins1:
        sig_name = "VehTiAndDataMins1"
        sig_start_bit = 13
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 13
        byte = 1
        mask = 0b00111111
        unmask = 0b11000000
        shift = 0

    class VehTiAndDataYr1:
        sig_name = "VehTiAndDataYr1"
        sig_start_bit = 46
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
        startbit = 46
        byte = 5
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class VehTiAndDataHr1:
        sig_name = "VehTiAndDataHr1"
        sig_start_bit = 20
        update_id_bit = None
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 20
        byte = 2
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0


class BgmADCANFDFr04:
    msg_name = "BgmADCANFDFr04"
    msg_id = 848
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.6
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['ACU', 'S2SReceiver']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class CarTiGlb:
        sig_name = "CarTiGlb"
        sig_start_bit = 39
        update_id_bit = 13
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
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111111, 0b00000000, 8, 0)]


class BgmADCANFDFr01:
    msg_name = "BgmADCANFDFr01"
    msg_id = 784
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['ACU', 'S2SReceiver']
    sig_group_dict = {'HandsOnDetection': ['HandsOnDetectionChks', 'HandsOnDetectionCntr', 'HandsOnDetectionErrorStatus', 'HandsOnDetectionHandsOnStatus']}
    sig_group_dataid_dict = {'HandsOnDetection': 3001}

    class HandsOnDetectionHandsOnStatus:
        sig_name = "HandsOnDetectionHandsOnStatus"
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
        sig_value_table = {'Init_Class': 0, 'Hands_ON': 1, 'Hands_OFF': 2, 'Undetermined_Class': 3}
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class HandsOnDetectionCntr:
        sig_name = "HandsOnDetectionCntr"
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

    class HandsOnDetection_UB:
        sig_name = "HandsOnDetection_UB"
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

    class HandsOnDetectionErrorStatus:
        sig_name = "HandsOnDetectionErrorStatus"
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
        sig_value_table = {'ErrorSts_Init_Diag': 0, 'ErrorSts_Reserved1': 1, 'ErrorSts_HOSWD_Ready': 2, 'ErrorSts_HOSWD_CUFault': 3, 'ErrorSts_HOSWD_SMFault': 4, 'ErrorSts_HOSWD_SVFault': 5, 'ErrorSts_Reserved2': 6, 'ErrorSts_Reserved3': 7}
        compute_method = None
        length = 3
        startbit = 14
        byte = 1
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class HandsOnDetectionChks:
        sig_name = "HandsOnDetectionChks"
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


class BgmADCANFDFr18:
    msg_name = "BgmADCANFDFr18"
    msg_id = 509
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "BGM"
    rx_nodes = ['ACU']
    sig_group_dict = {'RearLeftRdrObj1': ['RearLeftRdrObj1ObjBoxCenterLat', 'RearLeftRdrObj1ObjBoxCenterLgt', 'RearLeftRdrObj1RdrObjChks', 'RearLeftRdrObj1RdrObjCntr', 'RearLeftRdrObj1RdrObjDx', 'RearLeftRdrObj1RdrObjDxStdDe', 'RearLeftRdrObj1RdrObjDy', 'RearLeftRdrObj1RdrObjDynProp', 'RearLeftRdrObj1RdrObjDyStdDe', 'RearLeftRdrObj1RdrObjExistProb', 'RearLeftRdrObj1RdrObjHeight', 'RearLeftRdrObj1RdrObjHeightStdDe', 'RearLeftRdrObj1RdrObjID', 'RearLeftRdrObj1RdrObjLifeCycle', 'RearLeftRdrObj1RdrObjPwr', 'RearLeftRdrObj1RdrObjVx', 'RearLeftRdrObj1RdrObjVxStdDe', 'RearLeftRdrObj1RdrObjVy', 'RearLeftRdrObj1RdrObjVyStdDe'], 'RearLeftRdrObj3': ['RearLeftRdrObj3ObjBoxCenterLat', 'RearLeftRdrObj3ObjBoxCenterLgt', 'RearLeftRdrObj3RdrObjChks', 'RearLeftRdrObj3RdrObjCntr', 'RearLeftRdrObj3RdrObjDx', 'RearLeftRdrObj3RdrObjDxStdDe', 'RearLeftRdrObj3RdrObjDy', 'RearLeftRdrObj3RdrObjDynProp', 'RearLeftRdrObj3RdrObjDyStdDe', 'RearLeftRdrObj3RdrObjExistProb', 'RearLeftRdrObj3RdrObjHeight', 'RearLeftRdrObj3RdrObjHeightStdDe', 'RearLeftRdrObj3RdrObjID', 'RearLeftRdrObj3RdrObjLifeCycle', 'RearLeftRdrObj3RdrObjPwr', 'RearLeftRdrObj3RdrObjVx', 'RearLeftRdrObj3RdrObjVxStdDe', 'RearLeftRdrObj3RdrObjVy', 'RearLeftRdrObj3RdrObjVyStdDe'], 'RearLeftRdrObj2': ['RearLeftRdrObj2ObjBoxCenterLat', 'RearLeftRdrObj2ObjBoxCenterLgt', 'RearLeftRdrObj2RdrObjChks', 'RearLeftRdrObj2RdrObjCntr', 'RearLeftRdrObj2RdrObjDx', 'RearLeftRdrObj2RdrObjDxStdDe', 'RearLeftRdrObj2RdrObjDy', 'RearLeftRdrObj2RdrObjDynProp', 'RearLeftRdrObj2RdrObjDyStdDe', 'RearLeftRdrObj2RdrObjExistProb', 'RearLeftRdrObj2RdrObjHeight', 'RearLeftRdrObj2RdrObjHeightStdDe', 'RearLeftRdrObj2RdrObjID', 'RearLeftRdrObj2RdrObjLifeCycle', 'RearLeftRdrObj2RdrObjPwr', 'RearLeftRdrObj2RdrObjVx', 'RearLeftRdrObj2RdrObjVxStdDe', 'RearLeftRdrObj2RdrObjVy', 'RearLeftRdrObj2RdrObjVyStdDe']}
    sig_group_dataid_dict = {}

    class RearLeftRdrObj1RdrObjVyStdDe:
        sig_name = "RearLeftRdrObj1RdrObjVyStdDe"
        sig_start_bit = 153
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 153
        bmuws_info = [(19, 0b00000011, 0b11111100, 2, 0), (20, 0b11111111, 0b00000000, 8, 0)]

    class RearLeftRdrObj2ObjBoxCenterLgt:
        sig_name = "RearLeftRdrObj2ObjBoxCenterLgt"
        sig_start_bit = 207
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 207
        byte = 25
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearLeftRdrObj1_UB:
        sig_name = "RearLeftRdrObj1_UB"
        sig_start_bit = 175
        update_id_bit = 175
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
        startbit = 175
        byte = 21
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class RearLeftRdrObj1RdrObjPwr:
        sig_name = "RearLeftRdrObj1RdrObjPwr"
        sig_start_bit = 113
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 113
        bmuws_info = [(14, 0b00000011, 0b11111100, 2, 0), (15, 0b11111100, 0b00000011, 6, 2)]

    class RearLeftRdrObj1RdrObjLifeCycle:
        sig_name = "RearLeftRdrObj1RdrObjLifeCycle"
        sig_start_bit = 104
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
        startbit = 104
        bmuws_info = [(13, 0b00000001, 0b11111110, 1, 0), (14, 0b11111100, 0b00000011, 6, 2)]

    class RearLeftRdrObj1RdrObjDxStdDe:
        sig_name = "RearLeftRdrObj1RdrObjDxStdDe"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11100000, 0b00011111, 3, 5)]

    class RearLeftRdrObj1RdrObjChks:
        sig_name = "RearLeftRdrObj1RdrObjChks"
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

    class RearLeftRdrObj2RdrObjDyStdDe:
        sig_name = "RearLeftRdrObj2RdrObjDyStdDe"
        sig_start_bit = 247
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 247
        bmuws_info = [(30, 0b11111111, 0b00000000, 8, 0), (31, 0b11100000, 0b00011111, 3, 5)]

    class RearLeftRdrObj2RdrObjDynProp:
        sig_name = "RearLeftRdrObj2RdrObjDynProp"
        sig_start_bit = 228
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 228
        byte = 28
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class RearLeftRdrObj3RdrObjHeightStdDe:
        sig_name = "RearLeftRdrObj3RdrObjHeightStdDe"
        sig_start_bit = 432
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 432
        bmuws_info = [(54, 0b00000001, 0b11111110, 1, 0), (55, 0b11111111, 0b00000000, 8, 0), (56, 0b10000000, 0b01111111, 1, 7)]

    class RearLeftRdrObj3RdrObjDynProp:
        sig_name = "RearLeftRdrObj3RdrObjDynProp"
        sig_start_bit = 396
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 396
        byte = 49
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class RearLeftRdrObj2RdrObjLifeCycle:
        sig_name = "RearLeftRdrObj2RdrObjLifeCycle"
        sig_start_bit = 280
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
        startbit = 280
        bmuws_info = [(35, 0b00000001, 0b11111110, 1, 0), (36, 0b11111100, 0b00000011, 6, 2)]

    class RearLeftRdrObj3RdrObjCntr:
        sig_name = "RearLeftRdrObj3RdrObjCntr"
        sig_start_bit = 359
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
        startbit = 359
        byte = 44
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class RearLeftRdrObj3RdrObjVxStdDe:
        sig_name = "RearLeftRdrObj3RdrObjVxStdDe"
        sig_start_bit = 486
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 486
        bmuws_info = [(60, 0b01111111, 0b10000000, 7, 0), (61, 0b11100000, 0b00011111, 3, 5)]

    class RearLeftRdrObj2RdrObjHeightStdDe:
        sig_name = "RearLeftRdrObj2RdrObjHeightStdDe"
        sig_start_bit = 264
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 264
        bmuws_info = [(33, 0b00000001, 0b11111110, 1, 0), (34, 0b11111111, 0b00000000, 8, 0), (35, 0b10000000, 0b01111111, 1, 7)]

    class RearLeftRdrObj2RdrObjVy:
        sig_name = "RearLeftRdrObj2RdrObjVy"
        sig_start_bit = 324
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 324
        bmuws_info = [(40, 0b00011111, 0b11100000, 5, 0), (41, 0b11111100, 0b00000011, 6, 2)]

    class RearLeftRdrObj3ObjBoxCenterLat:
        sig_name = "RearLeftRdrObj3ObjBoxCenterLat"
        sig_start_bit = 383
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 383
        byte = 47
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearLeftRdrObj3RdrObjDxStdDe:
        sig_name = "RearLeftRdrObj3RdrObjDxStdDe"
        sig_start_bit = 391
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 391
        bmuws_info = [(48, 0b11111111, 0b00000000, 8, 0), (49, 0b11100000, 0b00011111, 3, 5)]

    class RearLeftRdrObj3RdrObjLifeCycle:
        sig_name = "RearLeftRdrObj3RdrObjLifeCycle"
        sig_start_bit = 448
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
        startbit = 448
        bmuws_info = [(56, 0b00000001, 0b11111110, 1, 0), (57, 0b11111100, 0b00000011, 6, 2)]

    class RearLeftRdrObj3RdrObjVy:
        sig_name = "RearLeftRdrObj3RdrObjVy"
        sig_start_bit = 492
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 492
        bmuws_info = [(61, 0b00011111, 0b11100000, 5, 0), (62, 0b11111100, 0b00000011, 6, 2)]

    class RearLeftRdrObj1RdrObjID:
        sig_name = "RearLeftRdrObj1RdrObjID"
        sig_start_bit = 110
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 110
        byte = 13
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class RearLeftRdrObj2RdrObjVx:
        sig_name = "RearLeftRdrObj2RdrObjVx"
        sig_start_bit = 297
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 297
        bmuws_info = [(37, 0b00000011, 0b11111100, 2, 0), (38, 0b11111111, 0b00000000, 8, 0), (39, 0b10000000, 0b01111111, 1, 7)]

    class RearLeftRdrObj3_UB:
        sig_name = "RearLeftRdrObj3_UB"
        sig_start_bit = 171
        update_id_bit = 171
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
        startbit = 171
        byte = 21
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class RearLeftRdrObj2RdrObjChks:
        sig_name = "RearLeftRdrObj2RdrObjChks"
        sig_start_bit = 183
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
        startbit = 183
        byte = 22
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearLeftRdrObj2ObjBoxCenterLat:
        sig_name = "RearLeftRdrObj2ObjBoxCenterLat"
        sig_start_bit = 215
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 215
        byte = 26
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearLeftRdrObj2RdrObjDx:
        sig_name = "RearLeftRdrObj2RdrObjDx"
        sig_start_bit = 187
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 187
        bmuws_info = [(23, 0b00001111, 0b11110000, 4, 0), (24, 0b11111111, 0b00000000, 8, 0)]

    class RearLeftRdrObj3RdrObjDyStdDe:
        sig_name = "RearLeftRdrObj3RdrObjDyStdDe"
        sig_start_bit = 415
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 415
        bmuws_info = [(51, 0b11111111, 0b00000000, 8, 0), (52, 0b11100000, 0b00011111, 3, 5)]

    class RearLeftRdrObj3RdrObjVx:
        sig_name = "RearLeftRdrObj3RdrObjVx"
        sig_start_bit = 465
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 465
        bmuws_info = [(58, 0b00000011, 0b11111100, 2, 0), (59, 0b11111111, 0b00000000, 8, 0), (60, 0b10000000, 0b01111111, 1, 7)]

    class RearLeftRdrObj2RdrObjID:
        sig_name = "RearLeftRdrObj2RdrObjID"
        sig_start_bit = 286
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 286
        byte = 35
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class RearLeftRdrObj2RdrObjDy:
        sig_name = "RearLeftRdrObj2RdrObjDy"
        sig_start_bit = 227
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 227
        bmuws_info = [(28, 0b00001111, 0b11110000, 4, 0), (29, 0b11111111, 0b00000000, 8, 0)]

    class RearLeftRdrObj1RdrObjDyStdDe:
        sig_name = "RearLeftRdrObj1RdrObjDyStdDe"
        sig_start_bit = 71
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 71
        bmuws_info = [(8, 0b11111111, 0b00000000, 8, 0), (9, 0b11100000, 0b00011111, 3, 5)]

    class RearLeftRdrObj1RdrObjVx:
        sig_name = "RearLeftRdrObj1RdrObjVx"
        sig_start_bit = 121
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 121
        bmuws_info = [(15, 0b00000011, 0b11111100, 2, 0), (16, 0b11111111, 0b00000000, 8, 0), (17, 0b10000000, 0b01111111, 1, 7)]

    class RearLeftRdrObj3RdrObjDy:
        sig_name = "RearLeftRdrObj3RdrObjDy"
        sig_start_bit = 395
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 395
        bmuws_info = [(49, 0b00001111, 0b11110000, 4, 0), (50, 0b11111111, 0b00000000, 8, 0)]

    class RearLeftRdrObj2RdrObjHeight:
        sig_name = "RearLeftRdrObj2RdrObjHeight"
        sig_start_bit = 258
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 258
        bmuws_info = [(32, 0b00000111, 0b11111000, 3, 0), (33, 0b11111110, 0b00000001, 7, 1)]

    class RearLeftRdrObj1ObjBoxCenterLgt:
        sig_name = "RearLeftRdrObj1ObjBoxCenterLgt"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
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

    class RearLeftRdrObj3RdrObjChks:
        sig_name = "RearLeftRdrObj3RdrObjChks"
        sig_start_bit = 351
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
        startbit = 351
        byte = 43
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearLeftRdrObj1RdrObjDy:
        sig_name = "RearLeftRdrObj1RdrObjDy"
        sig_start_bit = 51
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 51
        bmuws_info = [(6, 0b00001111, 0b11110000, 4, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class RearLeftRdrObj3RdrObjHeight:
        sig_name = "RearLeftRdrObj3RdrObjHeight"
        sig_start_bit = 426
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 426
        bmuws_info = [(53, 0b00000111, 0b11111000, 3, 0), (54, 0b11111110, 0b00000001, 7, 1)]

    class RearLeftRdrObj1RdrObjHeightStdDe:
        sig_name = "RearLeftRdrObj1RdrObjHeightStdDe"
        sig_start_bit = 88
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 88
        bmuws_info = [(11, 0b00000001, 0b11111110, 1, 0), (12, 0b11111111, 0b00000000, 8, 0), (13, 0b10000000, 0b01111111, 1, 7)]

    class RearLeftRdrObj1RdrObjVy:
        sig_name = "RearLeftRdrObj1RdrObjVy"
        sig_start_bit = 148
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 148
        bmuws_info = [(18, 0b00011111, 0b11100000, 5, 0), (19, 0b11111100, 0b00000011, 6, 2)]

    class RearLeftRdrObj1RdrObjDx:
        sig_name = "RearLeftRdrObj1RdrObjDx"
        sig_start_bit = 11
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 11
        bmuws_info = [(1, 0b00001111, 0b11110000, 4, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class RearLeftRdrObj1ObjBoxCenterLat:
        sig_name = "RearLeftRdrObj1ObjBoxCenterLat"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
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

    class RearLeftRdrObj2RdrObjVxStdDe:
        sig_name = "RearLeftRdrObj2RdrObjVxStdDe"
        sig_start_bit = 318
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 318
        bmuws_info = [(39, 0b01111111, 0b10000000, 7, 0), (40, 0b11100000, 0b00011111, 3, 5)]

    class RearLeftRdrObj2RdrObjPwr:
        sig_name = "RearLeftRdrObj2RdrObjPwr"
        sig_start_bit = 289
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 289
        bmuws_info = [(36, 0b00000011, 0b11111100, 2, 0), (37, 0b11111100, 0b00000011, 6, 2)]

    class RearLeftRdrObj2_UB:
        sig_name = "RearLeftRdrObj2_UB"
        sig_start_bit = 168
        update_id_bit = 168
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
        startbit = 168
        byte = 21
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class RearLeftRdrObj3RdrObjPwr:
        sig_name = "RearLeftRdrObj3RdrObjPwr"
        sig_start_bit = 457
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 457
        bmuws_info = [(57, 0b00000011, 0b11111100, 2, 0), (58, 0b11111100, 0b00000011, 6, 2)]

    class RearLeftRdrObj2RdrObjDxStdDe:
        sig_name = "RearLeftRdrObj2RdrObjDxStdDe"
        sig_start_bit = 223
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 223
        bmuws_info = [(27, 0b11111111, 0b00000000, 8, 0), (28, 0b11100000, 0b00011111, 3, 5)]

    class RearLeftRdrObj2RdrObjVyStdDe:
        sig_name = "RearLeftRdrObj2RdrObjVyStdDe"
        sig_start_bit = 329
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 329
        bmuws_info = [(41, 0b00000011, 0b11111100, 2, 0), (42, 0b11111111, 0b00000000, 8, 0)]

    class RearLeftRdrObj1RdrObjDynProp:
        sig_name = "RearLeftRdrObj1RdrObjDynProp"
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
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class RearLeftRdrObj1RdrObjExistProb:
        sig_name = "RearLeftRdrObj1RdrObjExistProb"
        sig_start_bit = 76
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 76
        bmuws_info = [(9, 0b00011111, 0b11100000, 5, 0), (10, 0b11111000, 0b00000111, 5, 3)]

    class RearLeftRdrObj3RdrObjID:
        sig_name = "RearLeftRdrObj3RdrObjID"
        sig_start_bit = 454
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 454
        byte = 56
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class RearLeftRdrObj2RdrObjCntr:
        sig_name = "RearLeftRdrObj2RdrObjCntr"
        sig_start_bit = 191
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
        startbit = 191
        byte = 23
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class RearLeftRdrObj1RdrObjCntr:
        sig_name = "RearLeftRdrObj1RdrObjCntr"
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

    class RearLeftRdrObj3ObjBoxCenterLgt:
        sig_name = "RearLeftRdrObj3ObjBoxCenterLgt"
        sig_start_bit = 375
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 375
        byte = 46
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearLeftRdrObj3RdrObjVyStdDe:
        sig_name = "RearLeftRdrObj3RdrObjVyStdDe"
        sig_start_bit = 497
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 497
        bmuws_info = [(62, 0b00000011, 0b11111100, 2, 0), (63, 0b11111111, 0b00000000, 8, 0)]

    class RearLeftRdrObj3RdrObjExistProb:
        sig_name = "RearLeftRdrObj3RdrObjExistProb"
        sig_start_bit = 420
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 420
        bmuws_info = [(52, 0b00011111, 0b11100000, 5, 0), (53, 0b11111000, 0b00000111, 5, 3)]

    class RearLeftRdrObj2RdrObjExistProb:
        sig_name = "RearLeftRdrObj2RdrObjExistProb"
        sig_start_bit = 252
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 252
        bmuws_info = [(31, 0b00011111, 0b11100000, 5, 0), (32, 0b11111000, 0b00000111, 5, 3)]

    class RearLeftRdrObj1RdrObjVxStdDe:
        sig_name = "RearLeftRdrObj1RdrObjVxStdDe"
        sig_start_bit = 142
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 142
        bmuws_info = [(17, 0b01111111, 0b10000000, 7, 0), (18, 0b11100000, 0b00011111, 3, 5)]

    class RearLeftRdrObj1RdrObjHeight:
        sig_name = "RearLeftRdrObj1RdrObjHeight"
        sig_start_bit = 82
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 82
        bmuws_info = [(10, 0b00000111, 0b11111000, 3, 0), (11, 0b11111110, 0b00000001, 7, 1)]

    class RearLeftRdrObj3RdrObjDx:
        sig_name = "RearLeftRdrObj3RdrObjDx"
        sig_start_bit = 355
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 355
        bmuws_info = [(44, 0b00001111, 0b11110000, 4, 0), (45, 0b11111111, 0b00000000, 8, 0)]


class AcuADCANFDFr06:
    msg_name = "AcuADCANFDFr06"
    msg_id = 289
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.045
    msg_length = 8
    tx_node = "ACU"
    rx_nodes = ['S2SReceiver']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class DrvModSetFbk:
        sig_name = "DrvModSetFbk"
        sig_start_bit = 63
        update_id_bit = 55
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
        startbit = 63
        byte = 7
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4


class BgmADCANFDFr24:
    msg_name = "BgmADCANFDFr24"
    msg_id = 516
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "BGM"
    rx_nodes = ['ACU']
    sig_group_dict = {'RearRgtRdrObj3': ['RearRgtRdrObj3ObjBoxCenterLat', 'RearRgtRdrObj3ObjBoxCenterLgt', 'RearRgtRdrObj3RdrObjChks', 'RearRgtRdrObj3RdrObjCntr', 'RearRgtRdrObj3RdrObjDx', 'RearRgtRdrObj3RdrObjDxStdDe', 'RearRgtRdrObj3RdrObjDy', 'RearRgtRdrObj3RdrObjDynProp', 'RearRgtRdrObj3RdrObjDyStdDe', 'RearRgtRdrObj3RdrObjExistProb', 'RearRgtRdrObj3RdrObjHeight', 'RearRgtRdrObj3RdrObjHeightStdDe', 'RearRgtRdrObj3RdrObjID', 'RearRgtRdrObj3RdrObjLifeCycle', 'RearRgtRdrObj3RdrObjPwr', 'RearRgtRdrObj3RdrObjVx', 'RearRgtRdrObj3RdrObjVxStdDe', 'RearRgtRdrObj3RdrObjVy', 'RearRgtRdrObj3RdrObjVyStdDe'], 'RearRgtRdrObj1': ['RearRgtRdrObj1ObjBoxCenterLat', 'RearRgtRdrObj1ObjBoxCenterLgt', 'RearRgtRdrObj1RdrObjChks', 'RearRgtRdrObj1RdrObjCntr', 'RearRgtRdrObj1RdrObjDx', 'RearRgtRdrObj1RdrObjDxStdDe', 'RearRgtRdrObj1RdrObjDy', 'RearRgtRdrObj1RdrObjDynProp', 'RearRgtRdrObj1RdrObjDyStdDe', 'RearRgtRdrObj1RdrObjExistProb', 'RearRgtRdrObj1RdrObjHeight', 'RearRgtRdrObj1RdrObjHeightStdDe', 'RearRgtRdrObj1RdrObjID', 'RearRgtRdrObj1RdrObjLifeCycle', 'RearRgtRdrObj1RdrObjPwr', 'RearRgtRdrObj1RdrObjVx', 'RearRgtRdrObj1RdrObjVxStdDe', 'RearRgtRdrObj1RdrObjVy', 'RearRgtRdrObj1RdrObjVyStdDe'], 'RearRgtRdrObj2': ['RearRgtRdrObj2ObjBoxCenterLat', 'RearRgtRdrObj2ObjBoxCenterLgt', 'RearRgtRdrObj2RdrObjChks', 'RearRgtRdrObj2RdrObjCntr', 'RearRgtRdrObj2RdrObjDx', 'RearRgtRdrObj2RdrObjDxStdDe', 'RearRgtRdrObj2RdrObjDy', 'RearRgtRdrObj2RdrObjDynProp', 'RearRgtRdrObj2RdrObjDyStdDe', 'RearRgtRdrObj2RdrObjExistProb', 'RearRgtRdrObj2RdrObjHeight', 'RearRgtRdrObj2RdrObjHeightStdDe', 'RearRgtRdrObj2RdrObjID', 'RearRgtRdrObj2RdrObjLifeCycle', 'RearRgtRdrObj2RdrObjPwr', 'RearRgtRdrObj2RdrObjVx', 'RearRgtRdrObj2RdrObjVxStdDe', 'RearRgtRdrObj2RdrObjVy', 'RearRgtRdrObj2RdrObjVyStdDe']}
    sig_group_dataid_dict = {}

    class RearRgtRdrObj2RdrObjDx:
        sig_name = "RearRgtRdrObj2RdrObjDx"
        sig_start_bit = 187
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 187
        bmuws_info = [(23, 0b00001111, 0b11110000, 4, 0), (24, 0b11111111, 0b00000000, 8, 0)]

    class RearRgtRdrObj2RdrObjDy:
        sig_name = "RearRgtRdrObj2RdrObjDy"
        sig_start_bit = 227
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 227
        bmuws_info = [(28, 0b00001111, 0b11110000, 4, 0), (29, 0b11111111, 0b00000000, 8, 0)]

    class RearRgtRdrObj3ObjBoxCenterLat:
        sig_name = "RearRgtRdrObj3ObjBoxCenterLat"
        sig_start_bit = 383
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 383
        byte = 47
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearRgtRdrObj3RdrObjDyStdDe:
        sig_name = "RearRgtRdrObj3RdrObjDyStdDe"
        sig_start_bit = 415
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 415
        bmuws_info = [(51, 0b11111111, 0b00000000, 8, 0), (52, 0b11100000, 0b00011111, 3, 5)]

    class RearRgtRdrObj3RdrObjPwr:
        sig_name = "RearRgtRdrObj3RdrObjPwr"
        sig_start_bit = 457
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 457
        bmuws_info = [(57, 0b00000011, 0b11111100, 2, 0), (58, 0b11111100, 0b00000011, 6, 2)]

    class RearRgtRdrObj2RdrObjID:
        sig_name = "RearRgtRdrObj2RdrObjID"
        sig_start_bit = 286
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 286
        byte = 35
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class RearRgtRdrObj2ObjBoxCenterLat:
        sig_name = "RearRgtRdrObj2ObjBoxCenterLat"
        sig_start_bit = 215
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 215
        byte = 26
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearRgtRdrObj1RdrObjExistProb:
        sig_name = "RearRgtRdrObj1RdrObjExistProb"
        sig_start_bit = 76
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 76
        bmuws_info = [(9, 0b00011111, 0b11100000, 5, 0), (10, 0b11111000, 0b00000111, 5, 3)]

    class RearRgtRdrObj3_UB:
        sig_name = "RearRgtRdrObj3_UB"
        sig_start_bit = 171
        update_id_bit = 171
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
        startbit = 171
        byte = 21
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class RearRgtRdrObj1RdrObjDy:
        sig_name = "RearRgtRdrObj1RdrObjDy"
        sig_start_bit = 51
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 51
        bmuws_info = [(6, 0b00001111, 0b11110000, 4, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class RearRgtRdrObj2RdrObjVx:
        sig_name = "RearRgtRdrObj2RdrObjVx"
        sig_start_bit = 297
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 297
        bmuws_info = [(37, 0b00000011, 0b11111100, 2, 0), (38, 0b11111111, 0b00000000, 8, 0), (39, 0b10000000, 0b01111111, 1, 7)]

    class RearRgtRdrObj1ObjBoxCenterLat:
        sig_name = "RearRgtRdrObj1ObjBoxCenterLat"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
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

    class RearRgtRdrObj2ObjBoxCenterLgt:
        sig_name = "RearRgtRdrObj2ObjBoxCenterLgt"
        sig_start_bit = 207
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 207
        byte = 25
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearRgtRdrObj3RdrObjExistProb:
        sig_name = "RearRgtRdrObj3RdrObjExistProb"
        sig_start_bit = 420
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 420
        bmuws_info = [(52, 0b00011111, 0b11100000, 5, 0), (53, 0b11111000, 0b00000111, 5, 3)]

    class RearRgtRdrObj3RdrObjDynProp:
        sig_name = "RearRgtRdrObj3RdrObjDynProp"
        sig_start_bit = 396
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 396
        byte = 49
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class RearRgtRdrObj1RdrObjDx:
        sig_name = "RearRgtRdrObj1RdrObjDx"
        sig_start_bit = 11
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 11
        bmuws_info = [(1, 0b00001111, 0b11110000, 4, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class RearRgtRdrObj1RdrObjID:
        sig_name = "RearRgtRdrObj1RdrObjID"
        sig_start_bit = 110
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 110
        byte = 13
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class RearRgtRdrObj1RdrObjChks:
        sig_name = "RearRgtRdrObj1RdrObjChks"
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

    class RearRgtRdrObj3RdrObjVyStdDe:
        sig_name = "RearRgtRdrObj3RdrObjVyStdDe"
        sig_start_bit = 497
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 497
        bmuws_info = [(62, 0b00000011, 0b11111100, 2, 0), (63, 0b11111111, 0b00000000, 8, 0)]

    class RearRgtRdrObj1ObjBoxCenterLgt:
        sig_name = "RearRgtRdrObj1ObjBoxCenterLgt"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
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

    class RearRgtRdrObj3RdrObjLifeCycle:
        sig_name = "RearRgtRdrObj3RdrObjLifeCycle"
        sig_start_bit = 448
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
        startbit = 448
        bmuws_info = [(56, 0b00000001, 0b11111110, 1, 0), (57, 0b11111100, 0b00000011, 6, 2)]

    class RearRgtRdrObj1RdrObjPwr:
        sig_name = "RearRgtRdrObj1RdrObjPwr"
        sig_start_bit = 113
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 113
        bmuws_info = [(14, 0b00000011, 0b11111100, 2, 0), (15, 0b11111100, 0b00000011, 6, 2)]

    class RearRgtRdrObj1RdrObjVyStdDe:
        sig_name = "RearRgtRdrObj1RdrObjVyStdDe"
        sig_start_bit = 153
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 153
        bmuws_info = [(19, 0b00000011, 0b11111100, 2, 0), (20, 0b11111111, 0b00000000, 8, 0)]

    class RearRgtRdrObj1RdrObjDynProp:
        sig_name = "RearRgtRdrObj1RdrObjDynProp"
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
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class RearRgtRdrObj2RdrObjHeightStdDe:
        sig_name = "RearRgtRdrObj2RdrObjHeightStdDe"
        sig_start_bit = 264
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 264
        bmuws_info = [(33, 0b00000001, 0b11111110, 1, 0), (34, 0b11111111, 0b00000000, 8, 0), (35, 0b10000000, 0b01111111, 1, 7)]

    class RearRgtRdrObj1_UB:
        sig_name = "RearRgtRdrObj1_UB"
        sig_start_bit = 175
        update_id_bit = 175
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
        startbit = 175
        byte = 21
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class RearRgtRdrObj3RdrObjVy:
        sig_name = "RearRgtRdrObj3RdrObjVy"
        sig_start_bit = 492
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 492
        bmuws_info = [(61, 0b00011111, 0b11100000, 5, 0), (62, 0b11111100, 0b00000011, 6, 2)]

    class RearRgtRdrObj1RdrObjDyStdDe:
        sig_name = "RearRgtRdrObj1RdrObjDyStdDe"
        sig_start_bit = 71
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 71
        bmuws_info = [(8, 0b11111111, 0b00000000, 8, 0), (9, 0b11100000, 0b00011111, 3, 5)]

    class RearRgtRdrObj3RdrObjChks:
        sig_name = "RearRgtRdrObj3RdrObjChks"
        sig_start_bit = 351
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
        startbit = 351
        byte = 43
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearRgtRdrObj1RdrObjVx:
        sig_name = "RearRgtRdrObj1RdrObjVx"
        sig_start_bit = 121
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 121
        bmuws_info = [(15, 0b00000011, 0b11111100, 2, 0), (16, 0b11111111, 0b00000000, 8, 0), (17, 0b10000000, 0b01111111, 1, 7)]

    class RearRgtRdrObj3RdrObjHeight:
        sig_name = "RearRgtRdrObj3RdrObjHeight"
        sig_start_bit = 426
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 426
        bmuws_info = [(53, 0b00000111, 0b11111000, 3, 0), (54, 0b11111110, 0b00000001, 7, 1)]

    class RearRgtRdrObj2RdrObjDynProp:
        sig_name = "RearRgtRdrObj2RdrObjDynProp"
        sig_start_bit = 228
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 228
        byte = 28
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class RearRgtRdrObj2RdrObjExistProb:
        sig_name = "RearRgtRdrObj2RdrObjExistProb"
        sig_start_bit = 252
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 252
        bmuws_info = [(31, 0b00011111, 0b11100000, 5, 0), (32, 0b11111000, 0b00000111, 5, 3)]

    class RearRgtRdrObj3RdrObjVx:
        sig_name = "RearRgtRdrObj3RdrObjVx"
        sig_start_bit = 465
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 465
        bmuws_info = [(58, 0b00000011, 0b11111100, 2, 0), (59, 0b11111111, 0b00000000, 8, 0), (60, 0b10000000, 0b01111111, 1, 7)]

    class RearRgtRdrObj2RdrObjLifeCycle:
        sig_name = "RearRgtRdrObj2RdrObjLifeCycle"
        sig_start_bit = 280
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
        startbit = 280
        bmuws_info = [(35, 0b00000001, 0b11111110, 1, 0), (36, 0b11111100, 0b00000011, 6, 2)]

    class RearRgtRdrObj1RdrObjHeightStdDe:
        sig_name = "RearRgtRdrObj1RdrObjHeightStdDe"
        sig_start_bit = 88
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 88
        bmuws_info = [(11, 0b00000001, 0b11111110, 1, 0), (12, 0b11111111, 0b00000000, 8, 0), (13, 0b10000000, 0b01111111, 1, 7)]

    class RearRgtRdrObj3RdrObjCntr:
        sig_name = "RearRgtRdrObj3RdrObjCntr"
        sig_start_bit = 359
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
        startbit = 359
        byte = 44
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class RearRgtRdrObj2RdrObjPwr:
        sig_name = "RearRgtRdrObj2RdrObjPwr"
        sig_start_bit = 289
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 289
        bmuws_info = [(36, 0b00000011, 0b11111100, 2, 0), (37, 0b11111100, 0b00000011, 6, 2)]

    class RearRgtRdrObj2RdrObjVyStdDe:
        sig_name = "RearRgtRdrObj2RdrObjVyStdDe"
        sig_start_bit = 329
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 329
        bmuws_info = [(41, 0b00000011, 0b11111100, 2, 0), (42, 0b11111111, 0b00000000, 8, 0)]

    class RearRgtRdrObj1RdrObjVxStdDe:
        sig_name = "RearRgtRdrObj1RdrObjVxStdDe"
        sig_start_bit = 142
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 142
        bmuws_info = [(17, 0b01111111, 0b10000000, 7, 0), (18, 0b11100000, 0b00011111, 3, 5)]

    class RearRgtRdrObj3ObjBoxCenterLgt:
        sig_name = "RearRgtRdrObj3ObjBoxCenterLgt"
        sig_start_bit = 375
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 375
        byte = 46
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearRgtRdrObj3RdrObjDxStdDe:
        sig_name = "RearRgtRdrObj3RdrObjDxStdDe"
        sig_start_bit = 391
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 391
        bmuws_info = [(48, 0b11111111, 0b00000000, 8, 0), (49, 0b11100000, 0b00011111, 3, 5)]

    class RearRgtRdrObj2RdrObjDxStdDe:
        sig_name = "RearRgtRdrObj2RdrObjDxStdDe"
        sig_start_bit = 223
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 223
        bmuws_info = [(27, 0b11111111, 0b00000000, 8, 0), (28, 0b11100000, 0b00011111, 3, 5)]

    class RearRgtRdrObj2_UB:
        sig_name = "RearRgtRdrObj2_UB"
        sig_start_bit = 168
        update_id_bit = 168
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
        startbit = 168
        byte = 21
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class RearRgtRdrObj2RdrObjChks:
        sig_name = "RearRgtRdrObj2RdrObjChks"
        sig_start_bit = 183
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
        startbit = 183
        byte = 22
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearRgtRdrObj1RdrObjHeight:
        sig_name = "RearRgtRdrObj1RdrObjHeight"
        sig_start_bit = 82
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 82
        bmuws_info = [(10, 0b00000111, 0b11111000, 3, 0), (11, 0b11111110, 0b00000001, 7, 1)]

    class RearRgtRdrObj3RdrObjHeightStdDe:
        sig_name = "RearRgtRdrObj3RdrObjHeightStdDe"
        sig_start_bit = 432
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 432
        bmuws_info = [(54, 0b00000001, 0b11111110, 1, 0), (55, 0b11111111, 0b00000000, 8, 0), (56, 0b10000000, 0b01111111, 1, 7)]

    class RearRgtRdrObj2RdrObjHeight:
        sig_name = "RearRgtRdrObj2RdrObjHeight"
        sig_start_bit = 258
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 258
        bmuws_info = [(32, 0b00000111, 0b11111000, 3, 0), (33, 0b11111110, 0b00000001, 7, 1)]

    class RearRgtRdrObj3RdrObjDx:
        sig_name = "RearRgtRdrObj3RdrObjDx"
        sig_start_bit = 355
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 355
        bmuws_info = [(44, 0b00001111, 0b11110000, 4, 0), (45, 0b11111111, 0b00000000, 8, 0)]

    class RearRgtRdrObj1RdrObjVy:
        sig_name = "RearRgtRdrObj1RdrObjVy"
        sig_start_bit = 148
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 148
        bmuws_info = [(18, 0b00011111, 0b11100000, 5, 0), (19, 0b11111100, 0b00000011, 6, 2)]

    class RearRgtRdrObj1RdrObjLifeCycle:
        sig_name = "RearRgtRdrObj1RdrObjLifeCycle"
        sig_start_bit = 104
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
        startbit = 104
        bmuws_info = [(13, 0b00000001, 0b11111110, 1, 0), (14, 0b11111100, 0b00000011, 6, 2)]

    class RearRgtRdrObj3RdrObjID:
        sig_name = "RearRgtRdrObj3RdrObjID"
        sig_start_bit = 454
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 454
        byte = 56
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class RearRgtRdrObj2RdrObjCntr:
        sig_name = "RearRgtRdrObj2RdrObjCntr"
        sig_start_bit = 191
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
        startbit = 191
        byte = 23
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class RearRgtRdrObj1RdrObjCntr:
        sig_name = "RearRgtRdrObj1RdrObjCntr"
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

    class RearRgtRdrObj2RdrObjVy:
        sig_name = "RearRgtRdrObj2RdrObjVy"
        sig_start_bit = 324
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 324
        bmuws_info = [(40, 0b00011111, 0b11100000, 5, 0), (41, 0b11111100, 0b00000011, 6, 2)]

    class RearRgtRdrObj3RdrObjDy:
        sig_name = "RearRgtRdrObj3RdrObjDy"
        sig_start_bit = 395
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 395
        bmuws_info = [(49, 0b00001111, 0b11110000, 4, 0), (50, 0b11111111, 0b00000000, 8, 0)]

    class RearRgtRdrObj3RdrObjVxStdDe:
        sig_name = "RearRgtRdrObj3RdrObjVxStdDe"
        sig_start_bit = 486
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 486
        bmuws_info = [(60, 0b01111111, 0b10000000, 7, 0), (61, 0b11100000, 0b00011111, 3, 5)]

    class RearRgtRdrObj2RdrObjVxStdDe:
        sig_name = "RearRgtRdrObj2RdrObjVxStdDe"
        sig_start_bit = 318
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 318
        bmuws_info = [(39, 0b01111111, 0b10000000, 7, 0), (40, 0b11100000, 0b00011111, 3, 5)]

    class RearRgtRdrObj1RdrObjDxStdDe:
        sig_name = "RearRgtRdrObj1RdrObjDxStdDe"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11100000, 0b00011111, 3, 5)]

    class RearRgtRdrObj2RdrObjDyStdDe:
        sig_name = "RearRgtRdrObj2RdrObjDyStdDe"
        sig_start_bit = 247
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 247
        bmuws_info = [(30, 0b11111111, 0b00000000, 8, 0), (31, 0b11100000, 0b00011111, 3, 5)]


class BgmADCANFDFr07:
    msg_name = "BgmADCANFDFr07"
    msg_id = 497
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "BGM"
    rx_nodes = ['ACU']
    sig_group_dict = {'FrntLeftRdrObj6': ['FrntLeftRdrObj6ObjBoxCenterLat', 'FrntLeftRdrObj6ObjBoxCenterLgt', 'FrntLeftRdrObj6RdrObjChks', 'FrntLeftRdrObj6RdrObjCntr', 'FrntLeftRdrObj6RdrObjDx', 'FrntLeftRdrObj6RdrObjDxStdDe', 'FrntLeftRdrObj6RdrObjDy', 'FrntLeftRdrObj6RdrObjDynProp', 'FrntLeftRdrObj6RdrObjDyStdDe', 'FrntLeftRdrObj6RdrObjExistProb', 'FrntLeftRdrObj6RdrObjHeight', 'FrntLeftRdrObj6RdrObjHeightStdDe', 'FrntLeftRdrObj6RdrObjID', 'FrntLeftRdrObj6RdrObjLifeCycle', 'FrntLeftRdrObj6RdrObjPwr', 'FrntLeftRdrObj6RdrObjVx', 'FrntLeftRdrObj6RdrObjVxStdDe', 'FrntLeftRdrObj6RdrObjVy', 'FrntLeftRdrObj6RdrObjVyStdDe'], 'FrntLeftRdrObj4': ['FrntLeftRdrObj4ObjBoxCenterLat', 'FrntLeftRdrObj4ObjBoxCenterLgt', 'FrntLeftRdrObj4RdrObjChks', 'FrntLeftRdrObj4RdrObjCntr', 'FrntLeftRdrObj4RdrObjDx', 'FrntLeftRdrObj4RdrObjDxStdDe', 'FrntLeftRdrObj4RdrObjDy', 'FrntLeftRdrObj4RdrObjDynProp', 'FrntLeftRdrObj4RdrObjDyStdDe', 'FrntLeftRdrObj4RdrObjExistProb', 'FrntLeftRdrObj4RdrObjHeight', 'FrntLeftRdrObj4RdrObjHeightStdDe', 'FrntLeftRdrObj4RdrObjID', 'FrntLeftRdrObj4RdrObjLifeCycle', 'FrntLeftRdrObj4RdrObjPwr', 'FrntLeftRdrObj4RdrObjVx', 'FrntLeftRdrObj4RdrObjVxStdDe', 'FrntLeftRdrObj4RdrObjVy', 'FrntLeftRdrObj4RdrObjVyStdDe'], 'FrntLeftRdrObj5': ['FrntLeftRdrObj5ObjBoxCenterLat', 'FrntLeftRdrObj5ObjBoxCenterLgt', 'FrntLeftRdrObj5RdrObjChks', 'FrntLeftRdrObj5RdrObjCntr', 'FrntLeftRdrObj5RdrObjDx', 'FrntLeftRdrObj5RdrObjDxStdDe', 'FrntLeftRdrObj5RdrObjDy', 'FrntLeftRdrObj5RdrObjDynProp', 'FrntLeftRdrObj5RdrObjDyStdDe', 'FrntLeftRdrObj5RdrObjExistProb', 'FrntLeftRdrObj5RdrObjHeight', 'FrntLeftRdrObj5RdrObjHeightStdDe', 'FrntLeftRdrObj5RdrObjID', 'FrntLeftRdrObj5RdrObjLifeCycle', 'FrntLeftRdrObj5RdrObjPwr', 'FrntLeftRdrObj5RdrObjVx', 'FrntLeftRdrObj5RdrObjVxStdDe', 'FrntLeftRdrObj5RdrObjVy', 'FrntLeftRdrObj5RdrObjVyStdDe']}
    sig_group_dataid_dict = {}

    class FrntLeftRdrObj5RdrObjHeightStdDe:
        sig_name = "FrntLeftRdrObj5RdrObjHeightStdDe"
        sig_start_bit = 264
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 264
        bmuws_info = [(33, 0b00000001, 0b11111110, 1, 0), (34, 0b11111111, 0b00000000, 8, 0), (35, 0b10000000, 0b01111111, 1, 7)]

    class FrntLeftRdrObj5RdrObjCntr:
        sig_name = "FrntLeftRdrObj5RdrObjCntr"
        sig_start_bit = 191
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
        startbit = 191
        byte = 23
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class FrntLeftRdrObj4RdrObjChks:
        sig_name = "FrntLeftRdrObj4RdrObjChks"
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

    class FrntLeftRdrObj4RdrObjVyStdDe:
        sig_name = "FrntLeftRdrObj4RdrObjVyStdDe"
        sig_start_bit = 153
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 153
        bmuws_info = [(19, 0b00000011, 0b11111100, 2, 0), (20, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeftRdrObj4RdrObjDxStdDe:
        sig_name = "FrntLeftRdrObj4RdrObjDxStdDe"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11100000, 0b00011111, 3, 5)]

    class FrntLeftRdrObj5RdrObjVyStdDe:
        sig_name = "FrntLeftRdrObj5RdrObjVyStdDe"
        sig_start_bit = 329
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 329
        bmuws_info = [(41, 0b00000011, 0b11111100, 2, 0), (42, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeftRdrObj4RdrObjHeight:
        sig_name = "FrntLeftRdrObj4RdrObjHeight"
        sig_start_bit = 82
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 82
        bmuws_info = [(10, 0b00000111, 0b11111000, 3, 0), (11, 0b11111110, 0b00000001, 7, 1)]

    class FrntLeftRdrObj6RdrObjPwr:
        sig_name = "FrntLeftRdrObj6RdrObjPwr"
        sig_start_bit = 457
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 457
        bmuws_info = [(57, 0b00000011, 0b11111100, 2, 0), (58, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeftRdrObj6_UB:
        sig_name = "FrntLeftRdrObj6_UB"
        sig_start_bit = 171
        update_id_bit = 171
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
        startbit = 171
        byte = 21
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class FrntLeftRdrObj6RdrObjVx:
        sig_name = "FrntLeftRdrObj6RdrObjVx"
        sig_start_bit = 465
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 465
        bmuws_info = [(58, 0b00000011, 0b11111100, 2, 0), (59, 0b11111111, 0b00000000, 8, 0), (60, 0b10000000, 0b01111111, 1, 7)]

    class FrntLeftRdrObj5RdrObjVxStdDe:
        sig_name = "FrntLeftRdrObj5RdrObjVxStdDe"
        sig_start_bit = 318
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 318
        bmuws_info = [(39, 0b01111111, 0b10000000, 7, 0), (40, 0b11100000, 0b00011111, 3, 5)]

    class FrntLeftRdrObj6RdrObjLifeCycle:
        sig_name = "FrntLeftRdrObj6RdrObjLifeCycle"
        sig_start_bit = 448
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
        startbit = 448
        bmuws_info = [(56, 0b00000001, 0b11111110, 1, 0), (57, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeftRdrObj5RdrObjLifeCycle:
        sig_name = "FrntLeftRdrObj5RdrObjLifeCycle"
        sig_start_bit = 280
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
        startbit = 280
        bmuws_info = [(35, 0b00000001, 0b11111110, 1, 0), (36, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeftRdrObj4RdrObjCntr:
        sig_name = "FrntLeftRdrObj4RdrObjCntr"
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

    class FrntLeftRdrObj6ObjBoxCenterLat:
        sig_name = "FrntLeftRdrObj6ObjBoxCenterLat"
        sig_start_bit = 383
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 383
        byte = 47
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntLeftRdrObj4RdrObjVx:
        sig_name = "FrntLeftRdrObj4RdrObjVx"
        sig_start_bit = 121
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 121
        bmuws_info = [(15, 0b00000011, 0b11111100, 2, 0), (16, 0b11111111, 0b00000000, 8, 0), (17, 0b10000000, 0b01111111, 1, 7)]

    class FrntLeftRdrObj4RdrObjDyStdDe:
        sig_name = "FrntLeftRdrObj4RdrObjDyStdDe"
        sig_start_bit = 71
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 71
        bmuws_info = [(8, 0b11111111, 0b00000000, 8, 0), (9, 0b11100000, 0b00011111, 3, 5)]

    class FrntLeftRdrObj5RdrObjID:
        sig_name = "FrntLeftRdrObj5RdrObjID"
        sig_start_bit = 286
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 286
        byte = 35
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class FrntLeftRdrObj5RdrObjExistProb:
        sig_name = "FrntLeftRdrObj5RdrObjExistProb"
        sig_start_bit = 252
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 252
        bmuws_info = [(31, 0b00011111, 0b11100000, 5, 0), (32, 0b11111000, 0b00000111, 5, 3)]

    class FrntLeftRdrObj4RdrObjDy:
        sig_name = "FrntLeftRdrObj4RdrObjDy"
        sig_start_bit = 51
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 51
        bmuws_info = [(6, 0b00001111, 0b11110000, 4, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeftRdrObj4ObjBoxCenterLgt:
        sig_name = "FrntLeftRdrObj4ObjBoxCenterLgt"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
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

    class FrntLeftRdrObj5RdrObjChks:
        sig_name = "FrntLeftRdrObj5RdrObjChks"
        sig_start_bit = 183
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
        startbit = 183
        byte = 22
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntLeftRdrObj5RdrObjDy:
        sig_name = "FrntLeftRdrObj5RdrObjDy"
        sig_start_bit = 227
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 227
        bmuws_info = [(28, 0b00001111, 0b11110000, 4, 0), (29, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeftRdrObj5RdrObjVy:
        sig_name = "FrntLeftRdrObj5RdrObjVy"
        sig_start_bit = 324
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 324
        bmuws_info = [(40, 0b00011111, 0b11100000, 5, 0), (41, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeftRdrObj5RdrObjDyStdDe:
        sig_name = "FrntLeftRdrObj5RdrObjDyStdDe"
        sig_start_bit = 247
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 247
        bmuws_info = [(30, 0b11111111, 0b00000000, 8, 0), (31, 0b11100000, 0b00011111, 3, 5)]

    class FrntLeftRdrObj5RdrObjDynProp:
        sig_name = "FrntLeftRdrObj5RdrObjDynProp"
        sig_start_bit = 228
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 228
        byte = 28
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class FrntLeftRdrObj4ObjBoxCenterLat:
        sig_name = "FrntLeftRdrObj4ObjBoxCenterLat"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
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

    class FrntLeftRdrObj6RdrObjVxStdDe:
        sig_name = "FrntLeftRdrObj6RdrObjVxStdDe"
        sig_start_bit = 486
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 486
        bmuws_info = [(60, 0b01111111, 0b10000000, 7, 0), (61, 0b11100000, 0b00011111, 3, 5)]

    class FrntLeftRdrObj6RdrObjHeight:
        sig_name = "FrntLeftRdrObj6RdrObjHeight"
        sig_start_bit = 426
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 426
        bmuws_info = [(53, 0b00000111, 0b11111000, 3, 0), (54, 0b11111110, 0b00000001, 7, 1)]

    class FrntLeftRdrObj4RdrObjPwr:
        sig_name = "FrntLeftRdrObj4RdrObjPwr"
        sig_start_bit = 113
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 113
        bmuws_info = [(14, 0b00000011, 0b11111100, 2, 0), (15, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeftRdrObj4RdrObjDynProp:
        sig_name = "FrntLeftRdrObj4RdrObjDynProp"
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
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class FrntLeftRdrObj5RdrObjPwr:
        sig_name = "FrntLeftRdrObj5RdrObjPwr"
        sig_start_bit = 289
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 289
        bmuws_info = [(36, 0b00000011, 0b11111100, 2, 0), (37, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeftRdrObj6RdrObjDy:
        sig_name = "FrntLeftRdrObj6RdrObjDy"
        sig_start_bit = 395
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 395
        bmuws_info = [(49, 0b00001111, 0b11110000, 4, 0), (50, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeftRdrObj6RdrObjDyStdDe:
        sig_name = "FrntLeftRdrObj6RdrObjDyStdDe"
        sig_start_bit = 415
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 415
        bmuws_info = [(51, 0b11111111, 0b00000000, 8, 0), (52, 0b11100000, 0b00011111, 3, 5)]

    class FrntLeftRdrObj6RdrObjDxStdDe:
        sig_name = "FrntLeftRdrObj6RdrObjDxStdDe"
        sig_start_bit = 391
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 391
        bmuws_info = [(48, 0b11111111, 0b00000000, 8, 0), (49, 0b11100000, 0b00011111, 3, 5)]

    class FrntLeftRdrObj6RdrObjExistProb:
        sig_name = "FrntLeftRdrObj6RdrObjExistProb"
        sig_start_bit = 420
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 420
        bmuws_info = [(52, 0b00011111, 0b11100000, 5, 0), (53, 0b11111000, 0b00000111, 5, 3)]

    class FrntLeftRdrObj4RdrObjHeightStdDe:
        sig_name = "FrntLeftRdrObj4RdrObjHeightStdDe"
        sig_start_bit = 88
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 88
        bmuws_info = [(11, 0b00000001, 0b11111110, 1, 0), (12, 0b11111111, 0b00000000, 8, 0), (13, 0b10000000, 0b01111111, 1, 7)]

    class FrntLeftRdrObj5RdrObjHeight:
        sig_name = "FrntLeftRdrObj5RdrObjHeight"
        sig_start_bit = 258
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 258
        bmuws_info = [(32, 0b00000111, 0b11111000, 3, 0), (33, 0b11111110, 0b00000001, 7, 1)]

    class FrntLeftRdrObj5RdrObjDxStdDe:
        sig_name = "FrntLeftRdrObj5RdrObjDxStdDe"
        sig_start_bit = 223
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 223
        bmuws_info = [(27, 0b11111111, 0b00000000, 8, 0), (28, 0b11100000, 0b00011111, 3, 5)]

    class FrntLeftRdrObj4RdrObjVy:
        sig_name = "FrntLeftRdrObj4RdrObjVy"
        sig_start_bit = 148
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 148
        bmuws_info = [(18, 0b00011111, 0b11100000, 5, 0), (19, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeftRdrObj4RdrObjDx:
        sig_name = "FrntLeftRdrObj4RdrObjDx"
        sig_start_bit = 11
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 11
        bmuws_info = [(1, 0b00001111, 0b11110000, 4, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeftRdrObj4_UB:
        sig_name = "FrntLeftRdrObj4_UB"
        sig_start_bit = 175
        update_id_bit = 175
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
        startbit = 175
        byte = 21
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class FrntLeftRdrObj5ObjBoxCenterLgt:
        sig_name = "FrntLeftRdrObj5ObjBoxCenterLgt"
        sig_start_bit = 207
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 207
        byte = 25
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntLeftRdrObj5ObjBoxCenterLat:
        sig_name = "FrntLeftRdrObj5ObjBoxCenterLat"
        sig_start_bit = 215
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 215
        byte = 26
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntLeftRdrObj6RdrObjCntr:
        sig_name = "FrntLeftRdrObj6RdrObjCntr"
        sig_start_bit = 359
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
        startbit = 359
        byte = 44
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class FrntLeftRdrObj4RdrObjVxStdDe:
        sig_name = "FrntLeftRdrObj4RdrObjVxStdDe"
        sig_start_bit = 142
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 142
        bmuws_info = [(17, 0b01111111, 0b10000000, 7, 0), (18, 0b11100000, 0b00011111, 3, 5)]

    class FrntLeftRdrObj4RdrObjLifeCycle:
        sig_name = "FrntLeftRdrObj4RdrObjLifeCycle"
        sig_start_bit = 104
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
        startbit = 104
        bmuws_info = [(13, 0b00000001, 0b11111110, 1, 0), (14, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeftRdrObj6RdrObjDynProp:
        sig_name = "FrntLeftRdrObj6RdrObjDynProp"
        sig_start_bit = 396
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 396
        byte = 49
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class FrntLeftRdrObj4RdrObjID:
        sig_name = "FrntLeftRdrObj4RdrObjID"
        sig_start_bit = 110
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 110
        byte = 13
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class FrntLeftRdrObj6RdrObjVy:
        sig_name = "FrntLeftRdrObj6RdrObjVy"
        sig_start_bit = 492
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 492
        bmuws_info = [(61, 0b00011111, 0b11100000, 5, 0), (62, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeftRdrObj6RdrObjID:
        sig_name = "FrntLeftRdrObj6RdrObjID"
        sig_start_bit = 454
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 454
        byte = 56
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class FrntLeftRdrObj5RdrObjDx:
        sig_name = "FrntLeftRdrObj5RdrObjDx"
        sig_start_bit = 187
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 187
        bmuws_info = [(23, 0b00001111, 0b11110000, 4, 0), (24, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeftRdrObj6RdrObjVyStdDe:
        sig_name = "FrntLeftRdrObj6RdrObjVyStdDe"
        sig_start_bit = 497
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 497
        bmuws_info = [(62, 0b00000011, 0b11111100, 2, 0), (63, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeftRdrObj6RdrObjHeightStdDe:
        sig_name = "FrntLeftRdrObj6RdrObjHeightStdDe"
        sig_start_bit = 432
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 432
        bmuws_info = [(54, 0b00000001, 0b11111110, 1, 0), (55, 0b11111111, 0b00000000, 8, 0), (56, 0b10000000, 0b01111111, 1, 7)]

    class FrntLeftRdrObj5RdrObjVx:
        sig_name = "FrntLeftRdrObj5RdrObjVx"
        sig_start_bit = 297
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 297
        bmuws_info = [(37, 0b00000011, 0b11111100, 2, 0), (38, 0b11111111, 0b00000000, 8, 0), (39, 0b10000000, 0b01111111, 1, 7)]

    class FrntLeftRdrObj4RdrObjExistProb:
        sig_name = "FrntLeftRdrObj4RdrObjExistProb"
        sig_start_bit = 76
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 76
        bmuws_info = [(9, 0b00011111, 0b11100000, 5, 0), (10, 0b11111000, 0b00000111, 5, 3)]

    class FrntLeftRdrObj6RdrObjDx:
        sig_name = "FrntLeftRdrObj6RdrObjDx"
        sig_start_bit = 355
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 355
        bmuws_info = [(44, 0b00001111, 0b11110000, 4, 0), (45, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeftRdrObj6ObjBoxCenterLgt:
        sig_name = "FrntLeftRdrObj6ObjBoxCenterLgt"
        sig_start_bit = 375
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 375
        byte = 46
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntLeftRdrObj6RdrObjChks:
        sig_name = "FrntLeftRdrObj6RdrObjChks"
        sig_start_bit = 351
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
        startbit = 351
        byte = 43
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntLeftRdrObj5_UB:
        sig_name = "FrntLeftRdrObj5_UB"
        sig_start_bit = 168
        update_id_bit = 168
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
        startbit = 168
        byte = 21
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0


class AcuADCANFDFr13:
    msg_name = "AcuADCANFDFr13"
    msg_id = 309
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "ACU"
    rx_nodes = ['BGM']
    sig_group_dict = {'ObjInfo': ['ObjInfoObjConfidenceLvl', 'ObjInfoObjDst1', 'ObjInfoObjDst2', 'ObjInfoObjHei', 'ObjInfoObjSide', 'ObjInfoObjTypMai']}
    sig_group_dataid_dict = {}

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


class BgmADCANFDFr16:
    msg_name = "BgmADCANFDFr16"
    msg_id = 507
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "BGM"
    rx_nodes = ['ACU']
    sig_group_dict = {'FrntRgtRdrObj14': ['FrntRgtRdrObj14ObjBoxCenterLat', 'FrntRgtRdrObj14ObjBoxCenterLgt', 'FrntRgtRdrObj14RdrObjChks', 'FrntRgtRdrObj14RdrObjCntr', 'FrntRgtRdrObj14RdrObjDx', 'FrntRgtRdrObj14RdrObjDxStdDe', 'FrntRgtRdrObj14RdrObjDy', 'FrntRgtRdrObj14RdrObjDynProp', 'FrntRgtRdrObj14RdrObjDyStdDe', 'FrntRgtRdrObj14RdrObjExistProb', 'FrntRgtRdrObj14RdrObjHeight', 'FrntRgtRdrObj14RdrObjHeightStdDe', 'FrntRgtRdrObj14RdrObjID', 'FrntRgtRdrObj14RdrObjLifeCycle', 'FrntRgtRdrObj14RdrObjPwr', 'FrntRgtRdrObj14RdrObjVx', 'FrntRgtRdrObj14RdrObjVxStdDe', 'FrntRgtRdrObj14RdrObjVy', 'FrntRgtRdrObj14RdrObjVyStdDe'], 'FrntRgtRdrObj15': ['FrntRgtRdrObj15ObjBoxCenterLat', 'FrntRgtRdrObj15ObjBoxCenterLgt', 'FrntRgtRdrObj15RdrObjChks', 'FrntRgtRdrObj15RdrObjCntr', 'FrntRgtRdrObj15RdrObjDx', 'FrntRgtRdrObj15RdrObjDxStdDe', 'FrntRgtRdrObj15RdrObjDy', 'FrntRgtRdrObj15RdrObjDynProp', 'FrntRgtRdrObj15RdrObjDyStdDe', 'FrntRgtRdrObj15RdrObjExistProb', 'FrntRgtRdrObj15RdrObjHeight', 'FrntRgtRdrObj15RdrObjHeightStdDe', 'FrntRgtRdrObj15RdrObjID', 'FrntRgtRdrObj15RdrObjLifeCycle', 'FrntRgtRdrObj15RdrObjPwr', 'FrntRgtRdrObj15RdrObjVx', 'FrntRgtRdrObj15RdrObjVxStdDe', 'FrntRgtRdrObj15RdrObjVy', 'FrntRgtRdrObj15RdrObjVyStdDe'], 'FrntRgtRdrObj13': ['FrntRgtRdrObj13ObjBoxCenterLat', 'FrntRgtRdrObj13ObjBoxCenterLgt', 'FrntRgtRdrObj13RdrObjChks', 'FrntRgtRdrObj13RdrObjCntr', 'FrntRgtRdrObj13RdrObjDx', 'FrntRgtRdrObj13RdrObjDxStdDe', 'FrntRgtRdrObj13RdrObjDy', 'FrntRgtRdrObj13RdrObjDynProp', 'FrntRgtRdrObj13RdrObjDyStdDe', 'FrntRgtRdrObj13RdrObjExistProb', 'FrntRgtRdrObj13RdrObjHeight', 'FrntRgtRdrObj13RdrObjHeightStdDe', 'FrntRgtRdrObj13RdrObjID', 'FrntRgtRdrObj13RdrObjLifeCycle', 'FrntRgtRdrObj13RdrObjPwr', 'FrntRgtRdrObj13RdrObjVx', 'FrntRgtRdrObj13RdrObjVxStdDe', 'FrntRgtRdrObj13RdrObjVy', 'FrntRgtRdrObj13RdrObjVyStdDe']}
    sig_group_dataid_dict = {}

    class FrntRgtRdrObj14_UB:
        sig_name = "FrntRgtRdrObj14_UB"
        sig_start_bit = 168
        update_id_bit = 168
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
        startbit = 168
        byte = 21
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FrntRgtRdrObj13RdrObjHeightStdDe:
        sig_name = "FrntRgtRdrObj13RdrObjHeightStdDe"
        sig_start_bit = 88
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 88
        bmuws_info = [(11, 0b00000001, 0b11111110, 1, 0), (12, 0b11111111, 0b00000000, 8, 0), (13, 0b10000000, 0b01111111, 1, 7)]

    class FrntRgtRdrObj15RdrObjDyStdDe:
        sig_name = "FrntRgtRdrObj15RdrObjDyStdDe"
        sig_start_bit = 415
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 415
        bmuws_info = [(51, 0b11111111, 0b00000000, 8, 0), (52, 0b11100000, 0b00011111, 3, 5)]

    class FrntRgtRdrObj13RdrObjPwr:
        sig_name = "FrntRgtRdrObj13RdrObjPwr"
        sig_start_bit = 113
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 113
        bmuws_info = [(14, 0b00000011, 0b11111100, 2, 0), (15, 0b11111100, 0b00000011, 6, 2)]

    class FrntRgtRdrObj15RdrObjHeightStdDe:
        sig_name = "FrntRgtRdrObj15RdrObjHeightStdDe"
        sig_start_bit = 432
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 432
        bmuws_info = [(54, 0b00000001, 0b11111110, 1, 0), (55, 0b11111111, 0b00000000, 8, 0), (56, 0b10000000, 0b01111111, 1, 7)]

    class FrntRgtRdrObj13RdrObjHeight:
        sig_name = "FrntRgtRdrObj13RdrObjHeight"
        sig_start_bit = 82
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 82
        bmuws_info = [(10, 0b00000111, 0b11111000, 3, 0), (11, 0b11111110, 0b00000001, 7, 1)]

    class FrntRgtRdrObj13RdrObjVy:
        sig_name = "FrntRgtRdrObj13RdrObjVy"
        sig_start_bit = 148
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 148
        bmuws_info = [(18, 0b00011111, 0b11100000, 5, 0), (19, 0b11111100, 0b00000011, 6, 2)]

    class FrntRgtRdrObj15RdrObjVyStdDe:
        sig_name = "FrntRgtRdrObj15RdrObjVyStdDe"
        sig_start_bit = 497
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 497
        bmuws_info = [(62, 0b00000011, 0b11111100, 2, 0), (63, 0b11111111, 0b00000000, 8, 0)]

    class FrntRgtRdrObj15RdrObjVx:
        sig_name = "FrntRgtRdrObj15RdrObjVx"
        sig_start_bit = 465
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 465
        bmuws_info = [(58, 0b00000011, 0b11111100, 2, 0), (59, 0b11111111, 0b00000000, 8, 0), (60, 0b10000000, 0b01111111, 1, 7)]

    class FrntRgtRdrObj15RdrObjChks:
        sig_name = "FrntRgtRdrObj15RdrObjChks"
        sig_start_bit = 351
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
        startbit = 351
        byte = 43
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntRgtRdrObj15_UB:
        sig_name = "FrntRgtRdrObj15_UB"
        sig_start_bit = 171
        update_id_bit = 171
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
        startbit = 171
        byte = 21
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class FrntRgtRdrObj13RdrObjVx:
        sig_name = "FrntRgtRdrObj13RdrObjVx"
        sig_start_bit = 121
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 121
        bmuws_info = [(15, 0b00000011, 0b11111100, 2, 0), (16, 0b11111111, 0b00000000, 8, 0), (17, 0b10000000, 0b01111111, 1, 7)]

    class FrntRgtRdrObj13RdrObjVyStdDe:
        sig_name = "FrntRgtRdrObj13RdrObjVyStdDe"
        sig_start_bit = 153
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 153
        bmuws_info = [(19, 0b00000011, 0b11111100, 2, 0), (20, 0b11111111, 0b00000000, 8, 0)]

    class FrntRgtRdrObj15RdrObjExistProb:
        sig_name = "FrntRgtRdrObj15RdrObjExistProb"
        sig_start_bit = 420
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 420
        bmuws_info = [(52, 0b00011111, 0b11100000, 5, 0), (53, 0b11111000, 0b00000111, 5, 3)]

    class FrntRgtRdrObj15RdrObjDynProp:
        sig_name = "FrntRgtRdrObj15RdrObjDynProp"
        sig_start_bit = 396
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 396
        byte = 49
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class FrntRgtRdrObj14RdrObjPwr:
        sig_name = "FrntRgtRdrObj14RdrObjPwr"
        sig_start_bit = 289
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 289
        bmuws_info = [(36, 0b00000011, 0b11111100, 2, 0), (37, 0b11111100, 0b00000011, 6, 2)]

    class FrntRgtRdrObj14RdrObjVxStdDe:
        sig_name = "FrntRgtRdrObj14RdrObjVxStdDe"
        sig_start_bit = 318
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 318
        bmuws_info = [(39, 0b01111111, 0b10000000, 7, 0), (40, 0b11100000, 0b00011111, 3, 5)]

    class FrntRgtRdrObj14RdrObjID:
        sig_name = "FrntRgtRdrObj14RdrObjID"
        sig_start_bit = 286
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 286
        byte = 35
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class FrntRgtRdrObj13RdrObjVxStdDe:
        sig_name = "FrntRgtRdrObj13RdrObjVxStdDe"
        sig_start_bit = 142
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 142
        bmuws_info = [(17, 0b01111111, 0b10000000, 7, 0), (18, 0b11100000, 0b00011111, 3, 5)]

    class FrntRgtRdrObj13ObjBoxCenterLat:
        sig_name = "FrntRgtRdrObj13ObjBoxCenterLat"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
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

    class FrntRgtRdrObj13RdrObjChks:
        sig_name = "FrntRgtRdrObj13RdrObjChks"
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

    class FrntRgtRdrObj15ObjBoxCenterLat:
        sig_name = "FrntRgtRdrObj15ObjBoxCenterLat"
        sig_start_bit = 383
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 383
        byte = 47
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntRgtRdrObj14RdrObjVx:
        sig_name = "FrntRgtRdrObj14RdrObjVx"
        sig_start_bit = 297
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 297
        bmuws_info = [(37, 0b00000011, 0b11111100, 2, 0), (38, 0b11111111, 0b00000000, 8, 0), (39, 0b10000000, 0b01111111, 1, 7)]

    class FrntRgtRdrObj14RdrObjVy:
        sig_name = "FrntRgtRdrObj14RdrObjVy"
        sig_start_bit = 324
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 324
        bmuws_info = [(40, 0b00011111, 0b11100000, 5, 0), (41, 0b11111100, 0b00000011, 6, 2)]

    class FrntRgtRdrObj15RdrObjDx:
        sig_name = "FrntRgtRdrObj15RdrObjDx"
        sig_start_bit = 355
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 355
        bmuws_info = [(44, 0b00001111, 0b11110000, 4, 0), (45, 0b11111111, 0b00000000, 8, 0)]

    class FrntRgtRdrObj13RdrObjDx:
        sig_name = "FrntRgtRdrObj13RdrObjDx"
        sig_start_bit = 11
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 11
        bmuws_info = [(1, 0b00001111, 0b11110000, 4, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class FrntRgtRdrObj14RdrObjCntr:
        sig_name = "FrntRgtRdrObj14RdrObjCntr"
        sig_start_bit = 191
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
        startbit = 191
        byte = 23
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class FrntRgtRdrObj14ObjBoxCenterLgt:
        sig_name = "FrntRgtRdrObj14ObjBoxCenterLgt"
        sig_start_bit = 207
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 207
        byte = 25
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntRgtRdrObj14RdrObjDyStdDe:
        sig_name = "FrntRgtRdrObj14RdrObjDyStdDe"
        sig_start_bit = 247
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 247
        bmuws_info = [(30, 0b11111111, 0b00000000, 8, 0), (31, 0b11100000, 0b00011111, 3, 5)]

    class FrntRgtRdrObj14RdrObjDx:
        sig_name = "FrntRgtRdrObj14RdrObjDx"
        sig_start_bit = 187
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 187
        bmuws_info = [(23, 0b00001111, 0b11110000, 4, 0), (24, 0b11111111, 0b00000000, 8, 0)]

    class FrntRgtRdrObj14ObjBoxCenterLat:
        sig_name = "FrntRgtRdrObj14ObjBoxCenterLat"
        sig_start_bit = 215
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 215
        byte = 26
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntRgtRdrObj14RdrObjLifeCycle:
        sig_name = "FrntRgtRdrObj14RdrObjLifeCycle"
        sig_start_bit = 280
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
        startbit = 280
        bmuws_info = [(35, 0b00000001, 0b11111110, 1, 0), (36, 0b11111100, 0b00000011, 6, 2)]

    class FrntRgtRdrObj15RdrObjHeight:
        sig_name = "FrntRgtRdrObj15RdrObjHeight"
        sig_start_bit = 426
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 426
        bmuws_info = [(53, 0b00000111, 0b11111000, 3, 0), (54, 0b11111110, 0b00000001, 7, 1)]

    class FrntRgtRdrObj15RdrObjID:
        sig_name = "FrntRgtRdrObj15RdrObjID"
        sig_start_bit = 454
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 454
        byte = 56
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class FrntRgtRdrObj13RdrObjDyStdDe:
        sig_name = "FrntRgtRdrObj13RdrObjDyStdDe"
        sig_start_bit = 71
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 71
        bmuws_info = [(8, 0b11111111, 0b00000000, 8, 0), (9, 0b11100000, 0b00011111, 3, 5)]

    class FrntRgtRdrObj15RdrObjCntr:
        sig_name = "FrntRgtRdrObj15RdrObjCntr"
        sig_start_bit = 359
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
        startbit = 359
        byte = 44
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class FrntRgtRdrObj13_UB:
        sig_name = "FrntRgtRdrObj13_UB"
        sig_start_bit = 175
        update_id_bit = 175
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
        startbit = 175
        byte = 21
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class FrntRgtRdrObj15RdrObjLifeCycle:
        sig_name = "FrntRgtRdrObj15RdrObjLifeCycle"
        sig_start_bit = 448
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
        startbit = 448
        bmuws_info = [(56, 0b00000001, 0b11111110, 1, 0), (57, 0b11111100, 0b00000011, 6, 2)]

    class FrntRgtRdrObj13RdrObjLifeCycle:
        sig_name = "FrntRgtRdrObj13RdrObjLifeCycle"
        sig_start_bit = 104
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
        startbit = 104
        bmuws_info = [(13, 0b00000001, 0b11111110, 1, 0), (14, 0b11111100, 0b00000011, 6, 2)]

    class FrntRgtRdrObj13RdrObjDxStdDe:
        sig_name = "FrntRgtRdrObj13RdrObjDxStdDe"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11100000, 0b00011111, 3, 5)]

    class FrntRgtRdrObj15RdrObjDxStdDe:
        sig_name = "FrntRgtRdrObj15RdrObjDxStdDe"
        sig_start_bit = 391
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 391
        bmuws_info = [(48, 0b11111111, 0b00000000, 8, 0), (49, 0b11100000, 0b00011111, 3, 5)]

    class FrntRgtRdrObj13RdrObjCntr:
        sig_name = "FrntRgtRdrObj13RdrObjCntr"
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

    class FrntRgtRdrObj14RdrObjVyStdDe:
        sig_name = "FrntRgtRdrObj14RdrObjVyStdDe"
        sig_start_bit = 329
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 329
        bmuws_info = [(41, 0b00000011, 0b11111100, 2, 0), (42, 0b11111111, 0b00000000, 8, 0)]

    class FrntRgtRdrObj14RdrObjHeightStdDe:
        sig_name = "FrntRgtRdrObj14RdrObjHeightStdDe"
        sig_start_bit = 264
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 264
        bmuws_info = [(33, 0b00000001, 0b11111110, 1, 0), (34, 0b11111111, 0b00000000, 8, 0), (35, 0b10000000, 0b01111111, 1, 7)]

    class FrntRgtRdrObj14RdrObjDy:
        sig_name = "FrntRgtRdrObj14RdrObjDy"
        sig_start_bit = 227
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 227
        bmuws_info = [(28, 0b00001111, 0b11110000, 4, 0), (29, 0b11111111, 0b00000000, 8, 0)]

    class FrntRgtRdrObj15RdrObjVy:
        sig_name = "FrntRgtRdrObj15RdrObjVy"
        sig_start_bit = 492
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 492
        bmuws_info = [(61, 0b00011111, 0b11100000, 5, 0), (62, 0b11111100, 0b00000011, 6, 2)]

    class FrntRgtRdrObj13ObjBoxCenterLgt:
        sig_name = "FrntRgtRdrObj13ObjBoxCenterLgt"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
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

    class FrntRgtRdrObj14RdrObjChks:
        sig_name = "FrntRgtRdrObj14RdrObjChks"
        sig_start_bit = 183
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
        startbit = 183
        byte = 22
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntRgtRdrObj15RdrObjDy:
        sig_name = "FrntRgtRdrObj15RdrObjDy"
        sig_start_bit = 395
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 395
        bmuws_info = [(49, 0b00001111, 0b11110000, 4, 0), (50, 0b11111111, 0b00000000, 8, 0)]

    class FrntRgtRdrObj14RdrObjExistProb:
        sig_name = "FrntRgtRdrObj14RdrObjExistProb"
        sig_start_bit = 252
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 252
        bmuws_info = [(31, 0b00011111, 0b11100000, 5, 0), (32, 0b11111000, 0b00000111, 5, 3)]

    class FrntRgtRdrObj14RdrObjHeight:
        sig_name = "FrntRgtRdrObj14RdrObjHeight"
        sig_start_bit = 258
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 258
        bmuws_info = [(32, 0b00000111, 0b11111000, 3, 0), (33, 0b11111110, 0b00000001, 7, 1)]

    class FrntRgtRdrObj13RdrObjDynProp:
        sig_name = "FrntRgtRdrObj13RdrObjDynProp"
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
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class FrntRgtRdrObj14RdrObjDxStdDe:
        sig_name = "FrntRgtRdrObj14RdrObjDxStdDe"
        sig_start_bit = 223
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 223
        bmuws_info = [(27, 0b11111111, 0b00000000, 8, 0), (28, 0b11100000, 0b00011111, 3, 5)]

    class FrntRgtRdrObj13RdrObjDy:
        sig_name = "FrntRgtRdrObj13RdrObjDy"
        sig_start_bit = 51
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 51
        bmuws_info = [(6, 0b00001111, 0b11110000, 4, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class FrntRgtRdrObj14RdrObjDynProp:
        sig_name = "FrntRgtRdrObj14RdrObjDynProp"
        sig_start_bit = 228
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 228
        byte = 28
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class FrntRgtRdrObj13RdrObjID:
        sig_name = "FrntRgtRdrObj13RdrObjID"
        sig_start_bit = 110
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 110
        byte = 13
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class FrntRgtRdrObj15RdrObjVxStdDe:
        sig_name = "FrntRgtRdrObj15RdrObjVxStdDe"
        sig_start_bit = 486
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 486
        bmuws_info = [(60, 0b01111111, 0b10000000, 7, 0), (61, 0b11100000, 0b00011111, 3, 5)]

    class FrntRgtRdrObj15RdrObjPwr:
        sig_name = "FrntRgtRdrObj15RdrObjPwr"
        sig_start_bit = 457
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 457
        bmuws_info = [(57, 0b00000011, 0b11111100, 2, 0), (58, 0b11111100, 0b00000011, 6, 2)]

    class FrntRgtRdrObj13RdrObjExistProb:
        sig_name = "FrntRgtRdrObj13RdrObjExistProb"
        sig_start_bit = 76
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 76
        bmuws_info = [(9, 0b00011111, 0b11100000, 5, 0), (10, 0b11111000, 0b00000111, 5, 3)]

    class FrntRgtRdrObj15ObjBoxCenterLgt:
        sig_name = "FrntRgtRdrObj15ObjBoxCenterLgt"
        sig_start_bit = 375
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 375
        byte = 46
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class BgmADCANFDFr29:
    msg_name = "BgmADCANFDFr29"
    msg_id = 521
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "BGM"
    rx_nodes = ['ACU']
    sig_group_dict = {'RearRgtRdrSync': ['RearRgtRdrSyncRdrObjTimeStampNSec', 'RearRgtRdrSyncRdrObjTimeStampSec', 'RearRgtRdrSyncRdrSyncChks', 'RearRgtRdrSyncRdrSyncCntr'], 'RearRgtRdrObj16': ['RearRgtRdrObj16ObjBoxCenterLat', 'RearRgtRdrObj16ObjBoxCenterLgt', 'RearRgtRdrObj16RdrObjChks', 'RearRgtRdrObj16RdrObjCntr', 'RearRgtRdrObj16RdrObjDx', 'RearRgtRdrObj16RdrObjDxStdDe', 'RearRgtRdrObj16RdrObjDy', 'RearRgtRdrObj16RdrObjDynProp', 'RearRgtRdrObj16RdrObjDyStdDe', 'RearRgtRdrObj16RdrObjExistProb', 'RearRgtRdrObj16RdrObjHeight', 'RearRgtRdrObj16RdrObjHeightStdDe', 'RearRgtRdrObj16RdrObjID', 'RearRgtRdrObj16RdrObjLifeCycle', 'RearRgtRdrObj16RdrObjPwr', 'RearRgtRdrObj16RdrObjVx', 'RearRgtRdrObj16RdrObjVxStdDe', 'RearRgtRdrObj16RdrObjVy', 'RearRgtRdrObj16RdrObjVyStdDe']}
    sig_group_dataid_dict = {}

    class RearRgtRdrObj16RdrObjDxStdDe:
        sig_name = "RearRgtRdrObj16RdrObjDxStdDe"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11100000, 0b00011111, 3, 5)]

    class RearRgtRdrSyncRdrObjTimeStampSec:
        sig_name = "RearRgtRdrSyncRdrObjTimeStampSec"
        sig_start_bit = 239
        update_id_bit = None
        sig_length = 32
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4294967295
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 32
        startbit = 239
        bmuws_info = [(29, 0b11111111, 0b00000000, 8, 0), (30, 0b11111111, 0b00000000, 8, 0), (31, 0b11111111, 0b00000000, 8, 0), (32, 0b11111111, 0b00000000, 8, 0)]

    class RearRgtRdrObj16RdrObjPwr:
        sig_name = "RearRgtRdrObj16RdrObjPwr"
        sig_start_bit = 113
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 113
        bmuws_info = [(14, 0b00000011, 0b11111100, 2, 0), (15, 0b11111100, 0b00000011, 6, 2)]

    class RearRgtRdrObj16RdrObjChks:
        sig_name = "RearRgtRdrObj16RdrObjChks"
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

    class RearRgtRdrSyncRdrObjTimeStampNSec:
        sig_name = "RearRgtRdrSyncRdrObjTimeStampNSec"
        sig_start_bit = 207
        update_id_bit = None
        sig_length = 32
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4294967295
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 32
        startbit = 207
        bmuws_info = [(25, 0b11111111, 0b00000000, 8, 0), (26, 0b11111111, 0b00000000, 8, 0), (27, 0b11111111, 0b00000000, 8, 0), (28, 0b11111111, 0b00000000, 8, 0)]

    class RearRgtRdrObj16RdrObjExistProb:
        sig_name = "RearRgtRdrObj16RdrObjExistProb"
        sig_start_bit = 76
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 76
        bmuws_info = [(9, 0b00011111, 0b11100000, 5, 0), (10, 0b11111000, 0b00000111, 5, 3)]

    class RearRgtRdrObj16RdrObjID:
        sig_name = "RearRgtRdrObj16RdrObjID"
        sig_start_bit = 110
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 110
        byte = 13
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class RearRgtRdrObj16ObjBoxCenterLgt:
        sig_name = "RearRgtRdrObj16ObjBoxCenterLgt"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
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

    class RearRgtRdrSync_UB:
        sig_name = "RearRgtRdrSync_UB"
        sig_start_bit = 271
        update_id_bit = 271
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
        startbit = 271
        byte = 33
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class RearRgtRdrSyncRdrSyncChks:
        sig_name = "RearRgtRdrSyncRdrSyncChks"
        sig_start_bit = 191
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
        startbit = 191
        byte = 23
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearRgtRdrObj16RdrObjDy:
        sig_name = "RearRgtRdrObj16RdrObjDy"
        sig_start_bit = 51
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 51
        bmuws_info = [(6, 0b00001111, 0b11110000, 4, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class RearRgtRdrFault:
        sig_name = "RearRgtRdrFault"
        sig_start_bit = 171
        update_id_bit = 169
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
        startbit = 171
        byte = 21
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class RearRgtRdrObj16ObjBoxCenterLat:
        sig_name = "RearRgtRdrObj16ObjBoxCenterLat"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
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

    class RearRgtRdrObj16RdrObjVy:
        sig_name = "RearRgtRdrObj16RdrObjVy"
        sig_start_bit = 148
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 148
        bmuws_info = [(18, 0b00011111, 0b11100000, 5, 0), (19, 0b11111100, 0b00000011, 6, 2)]

    class RearRgtRdrObj16RdrObjDynProp:
        sig_name = "RearRgtRdrObj16RdrObjDynProp"
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
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class RearRgtRdrObj16RdrObjVx:
        sig_name = "RearRgtRdrObj16RdrObjVx"
        sig_start_bit = 121
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 121
        bmuws_info = [(15, 0b00000011, 0b11111100, 2, 0), (16, 0b11111111, 0b00000000, 8, 0), (17, 0b10000000, 0b01111111, 1, 7)]

    class RearRgtRdrObj16RdrObjLifeCycle:
        sig_name = "RearRgtRdrObj16RdrObjLifeCycle"
        sig_start_bit = 104
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
        startbit = 104
        bmuws_info = [(13, 0b00000001, 0b11111110, 1, 0), (14, 0b11111100, 0b00000011, 6, 2)]

    class RearRgtRdrObj16RdrObjVyStdDe:
        sig_name = "RearRgtRdrObj16RdrObjVyStdDe"
        sig_start_bit = 153
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 153
        bmuws_info = [(19, 0b00000011, 0b11111100, 2, 0), (20, 0b11111111, 0b00000000, 8, 0)]

    class RearRgtRdrObj16RdrObjCntr:
        sig_name = "RearRgtRdrObj16RdrObjCntr"
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

    class RearRgtRdrSyncRdrSyncCntr:
        sig_name = "RearRgtRdrSyncRdrSyncCntr"
        sig_start_bit = 195
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
        startbit = 195
        byte = 24
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class RearRgtRdrObj16RdrObjHeightStdDe:
        sig_name = "RearRgtRdrObj16RdrObjHeightStdDe"
        sig_start_bit = 88
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 88
        bmuws_info = [(11, 0b00000001, 0b11111110, 1, 0), (12, 0b11111111, 0b00000000, 8, 0), (13, 0b10000000, 0b01111111, 1, 7)]

    class RearRgtRdrObj16RdrObjVxStdDe:
        sig_name = "RearRgtRdrObj16RdrObjVxStdDe"
        sig_start_bit = 142
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 142
        bmuws_info = [(17, 0b01111111, 0b10000000, 7, 0), (18, 0b11100000, 0b00011111, 3, 5)]

    class RearRgtRdrObj16RdrObjDyStdDe:
        sig_name = "RearRgtRdrObj16RdrObjDyStdDe"
        sig_start_bit = 71
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 71
        bmuws_info = [(8, 0b11111111, 0b00000000, 8, 0), (9, 0b11100000, 0b00011111, 3, 5)]

    class RearRgtRdrObj16_UB:
        sig_name = "RearRgtRdrObj16_UB"
        sig_start_bit = 175
        update_id_bit = 175
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
        startbit = 175
        byte = 21
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class RearRgtRdrObj16RdrObjDx:
        sig_name = "RearRgtRdrObj16RdrObjDx"
        sig_start_bit = 11
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 11
        bmuws_info = [(1, 0b00001111, 0b11110000, 4, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class RearRgtRdrObj16RdrObjHeight:
        sig_name = "RearRgtRdrObj16RdrObjHeight"
        sig_start_bit = 82
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 82
        bmuws_info = [(10, 0b00000111, 0b11111000, 3, 0), (11, 0b11111110, 0b00000001, 7, 1)]


class BgmADCANFDNmFr:
    msg_name = "BgmADCANFDNmFr"
    msg_id = 1281
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['ACU']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class BgmADCANFDFr12:
    msg_name = "BgmADCANFDFr12"
    msg_id = 502
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "BGM"
    rx_nodes = ['ACU']
    sig_group_dict = {'FrntRgtRdrObj2': ['FrntRgtRdrObj2ObjBoxCenterLat', 'FrntRgtRdrObj2ObjBoxCenterLgt', 'FrntRgtRdrObj2RdrObjChks', 'FrntRgtRdrObj2RdrObjCntr', 'FrntRgtRdrObj2RdrObjDx', 'FrntRgtRdrObj2RdrObjDxStdDe', 'FrntRgtRdrObj2RdrObjDy', 'FrntRgtRdrObj2RdrObjDynProp', 'FrntRgtRdrObj2RdrObjDyStdDe', 'FrntRgtRdrObj2RdrObjExistProb', 'FrntRgtRdrObj2RdrObjHeight', 'FrntRgtRdrObj2RdrObjHeightStdDe', 'FrntRgtRdrObj2RdrObjID', 'FrntRgtRdrObj2RdrObjLifeCycle', 'FrntRgtRdrObj2RdrObjPwr', 'FrntRgtRdrObj2RdrObjVx', 'FrntRgtRdrObj2RdrObjVxStdDe', 'FrntRgtRdrObj2RdrObjVy', 'FrntRgtRdrObj2RdrObjVyStdDe'], 'FrntRgtRdrObj1': ['FrntRgtRdrObj1ObjBoxCenterLat', 'FrntRgtRdrObj1ObjBoxCenterLgt', 'FrntRgtRdrObj1RdrObjChks', 'FrntRgtRdrObj1RdrObjCntr', 'FrntRgtRdrObj1RdrObjDx', 'FrntRgtRdrObj1RdrObjDxStdDe', 'FrntRgtRdrObj1RdrObjDy', 'FrntRgtRdrObj1RdrObjDynProp', 'FrntRgtRdrObj1RdrObjDyStdDe', 'FrntRgtRdrObj1RdrObjExistProb', 'FrntRgtRdrObj1RdrObjHeight', 'FrntRgtRdrObj1RdrObjHeightStdDe', 'FrntRgtRdrObj1RdrObjID', 'FrntRgtRdrObj1RdrObjLifeCycle', 'FrntRgtRdrObj1RdrObjPwr', 'FrntRgtRdrObj1RdrObjVx', 'FrntRgtRdrObj1RdrObjVxStdDe', 'FrntRgtRdrObj1RdrObjVy', 'FrntRgtRdrObj1RdrObjVyStdDe'], 'FrntRgtRdrObj3': ['FrntRgtRdrObj3ObjBoxCenterLat', 'FrntRgtRdrObj3ObjBoxCenterLgt', 'FrntRgtRdrObj3RdrObjChks', 'FrntRgtRdrObj3RdrObjCntr', 'FrntRgtRdrObj3RdrObjDx', 'FrntRgtRdrObj3RdrObjDxStdDe', 'FrntRgtRdrObj3RdrObjDy', 'FrntRgtRdrObj3RdrObjDynProp', 'FrntRgtRdrObj3RdrObjDyStdDe', 'FrntRgtRdrObj3RdrObjExistProb', 'FrntRgtRdrObj3RdrObjHeight', 'FrntRgtRdrObj3RdrObjHeightStdDe', 'FrntRgtRdrObj3RdrObjID', 'FrntRgtRdrObj3RdrObjLifeCycle', 'FrntRgtRdrObj3RdrObjPwr', 'FrntRgtRdrObj3RdrObjVx', 'FrntRgtRdrObj3RdrObjVxStdDe', 'FrntRgtRdrObj3RdrObjVy', 'FrntRgtRdrObj3RdrObjVyStdDe']}
    sig_group_dataid_dict = {}

    class FrntRgtRdrObj1RdrObjCntr:
        sig_name = "FrntRgtRdrObj1RdrObjCntr"
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

    class FrntRgtRdrObj3RdrObjPwr:
        sig_name = "FrntRgtRdrObj3RdrObjPwr"
        sig_start_bit = 457
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 457
        bmuws_info = [(57, 0b00000011, 0b11111100, 2, 0), (58, 0b11111100, 0b00000011, 6, 2)]

    class FrntRgtRdrObj2RdrObjVxStdDe:
        sig_name = "FrntRgtRdrObj2RdrObjVxStdDe"
        sig_start_bit = 318
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 318
        bmuws_info = [(39, 0b01111111, 0b10000000, 7, 0), (40, 0b11100000, 0b00011111, 3, 5)]

    class FrntRgtRdrObj3RdrObjVx:
        sig_name = "FrntRgtRdrObj3RdrObjVx"
        sig_start_bit = 465
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 465
        bmuws_info = [(58, 0b00000011, 0b11111100, 2, 0), (59, 0b11111111, 0b00000000, 8, 0), (60, 0b10000000, 0b01111111, 1, 7)]

    class FrntRgtRdrObj1RdrObjDy:
        sig_name = "FrntRgtRdrObj1RdrObjDy"
        sig_start_bit = 51
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 51
        bmuws_info = [(6, 0b00001111, 0b11110000, 4, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class FrntRgtRdrObj1RdrObjHeightStdDe:
        sig_name = "FrntRgtRdrObj1RdrObjHeightStdDe"
        sig_start_bit = 88
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 88
        bmuws_info = [(11, 0b00000001, 0b11111110, 1, 0), (12, 0b11111111, 0b00000000, 8, 0), (13, 0b10000000, 0b01111111, 1, 7)]

    class FrntRgtRdrObj2RdrObjHeight:
        sig_name = "FrntRgtRdrObj2RdrObjHeight"
        sig_start_bit = 258
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 258
        bmuws_info = [(32, 0b00000111, 0b11111000, 3, 0), (33, 0b11111110, 0b00000001, 7, 1)]

    class FrntRgtRdrObj3RdrObjID:
        sig_name = "FrntRgtRdrObj3RdrObjID"
        sig_start_bit = 454
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 454
        byte = 56
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class FrntRgtRdrObj2_UB:
        sig_name = "FrntRgtRdrObj2_UB"
        sig_start_bit = 168
        update_id_bit = 168
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
        startbit = 168
        byte = 21
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FrntRgtRdrObj3RdrObjHeight:
        sig_name = "FrntRgtRdrObj3RdrObjHeight"
        sig_start_bit = 426
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 426
        bmuws_info = [(53, 0b00000111, 0b11111000, 3, 0), (54, 0b11111110, 0b00000001, 7, 1)]

    class FrntRgtRdrObj1RdrObjVyStdDe:
        sig_name = "FrntRgtRdrObj1RdrObjVyStdDe"
        sig_start_bit = 153
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 153
        bmuws_info = [(19, 0b00000011, 0b11111100, 2, 0), (20, 0b11111111, 0b00000000, 8, 0)]

    class FrntRgtRdrObj1RdrObjDx:
        sig_name = "FrntRgtRdrObj1RdrObjDx"
        sig_start_bit = 11
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 11
        bmuws_info = [(1, 0b00001111, 0b11110000, 4, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class FrntRgtRdrObj1RdrObjHeight:
        sig_name = "FrntRgtRdrObj1RdrObjHeight"
        sig_start_bit = 82
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 82
        bmuws_info = [(10, 0b00000111, 0b11111000, 3, 0), (11, 0b11111110, 0b00000001, 7, 1)]

    class FrntRgtRdrObj2RdrObjPwr:
        sig_name = "FrntRgtRdrObj2RdrObjPwr"
        sig_start_bit = 289
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 289
        bmuws_info = [(36, 0b00000011, 0b11111100, 2, 0), (37, 0b11111100, 0b00000011, 6, 2)]

    class FrntRgtRdrObj3RdrObjDy:
        sig_name = "FrntRgtRdrObj3RdrObjDy"
        sig_start_bit = 395
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 395
        bmuws_info = [(49, 0b00001111, 0b11110000, 4, 0), (50, 0b11111111, 0b00000000, 8, 0)]

    class FrntRgtRdrObj2RdrObjLifeCycle:
        sig_name = "FrntRgtRdrObj2RdrObjLifeCycle"
        sig_start_bit = 280
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
        startbit = 280
        bmuws_info = [(35, 0b00000001, 0b11111110, 1, 0), (36, 0b11111100, 0b00000011, 6, 2)]

    class FrntRgtRdrObj1RdrObjDynProp:
        sig_name = "FrntRgtRdrObj1RdrObjDynProp"
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
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class FrntRgtRdrObj2RdrObjChks:
        sig_name = "FrntRgtRdrObj2RdrObjChks"
        sig_start_bit = 183
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
        startbit = 183
        byte = 22
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntRgtRdrObj2RdrObjDynProp:
        sig_name = "FrntRgtRdrObj2RdrObjDynProp"
        sig_start_bit = 228
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 228
        byte = 28
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class FrntRgtRdrObj3RdrObjDynProp:
        sig_name = "FrntRgtRdrObj3RdrObjDynProp"
        sig_start_bit = 396
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 396
        byte = 49
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class FrntRgtRdrObj1RdrObjDxStdDe:
        sig_name = "FrntRgtRdrObj1RdrObjDxStdDe"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11100000, 0b00011111, 3, 5)]

    class FrntRgtRdrObj1RdrObjDyStdDe:
        sig_name = "FrntRgtRdrObj1RdrObjDyStdDe"
        sig_start_bit = 71
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 71
        bmuws_info = [(8, 0b11111111, 0b00000000, 8, 0), (9, 0b11100000, 0b00011111, 3, 5)]

    class FrntRgtRdrObj3RdrObjLifeCycle:
        sig_name = "FrntRgtRdrObj3RdrObjLifeCycle"
        sig_start_bit = 448
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
        startbit = 448
        bmuws_info = [(56, 0b00000001, 0b11111110, 1, 0), (57, 0b11111100, 0b00000011, 6, 2)]

    class FrntRgtRdrObj1RdrObjVx:
        sig_name = "FrntRgtRdrObj1RdrObjVx"
        sig_start_bit = 121
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 121
        bmuws_info = [(15, 0b00000011, 0b11111100, 2, 0), (16, 0b11111111, 0b00000000, 8, 0), (17, 0b10000000, 0b01111111, 1, 7)]

    class FrntRgtRdrObj1RdrObjID:
        sig_name = "FrntRgtRdrObj1RdrObjID"
        sig_start_bit = 110
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 110
        byte = 13
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class FrntRgtRdrObj1RdrObjChks:
        sig_name = "FrntRgtRdrObj1RdrObjChks"
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

    class FrntRgtRdrObj1ObjBoxCenterLat:
        sig_name = "FrntRgtRdrObj1ObjBoxCenterLat"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
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

    class FrntRgtRdrObj2RdrObjDx:
        sig_name = "FrntRgtRdrObj2RdrObjDx"
        sig_start_bit = 187
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 187
        bmuws_info = [(23, 0b00001111, 0b11110000, 4, 0), (24, 0b11111111, 0b00000000, 8, 0)]

    class FrntRgtRdrObj3RdrObjChks:
        sig_name = "FrntRgtRdrObj3RdrObjChks"
        sig_start_bit = 351
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
        startbit = 351
        byte = 43
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntRgtRdrObj2RdrObjVx:
        sig_name = "FrntRgtRdrObj2RdrObjVx"
        sig_start_bit = 297
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 297
        bmuws_info = [(37, 0b00000011, 0b11111100, 2, 0), (38, 0b11111111, 0b00000000, 8, 0), (39, 0b10000000, 0b01111111, 1, 7)]

    class FrntRgtRdrObj2RdrObjDy:
        sig_name = "FrntRgtRdrObj2RdrObjDy"
        sig_start_bit = 227
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 227
        bmuws_info = [(28, 0b00001111, 0b11110000, 4, 0), (29, 0b11111111, 0b00000000, 8, 0)]

    class FrntRgtRdrObj3RdrObjCntr:
        sig_name = "FrntRgtRdrObj3RdrObjCntr"
        sig_start_bit = 359
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
        startbit = 359
        byte = 44
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class FrntRgtRdrObj2ObjBoxCenterLgt:
        sig_name = "FrntRgtRdrObj2ObjBoxCenterLgt"
        sig_start_bit = 207
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 207
        byte = 25
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntRgtRdrObj3RdrObjExistProb:
        sig_name = "FrntRgtRdrObj3RdrObjExistProb"
        sig_start_bit = 420
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 420
        bmuws_info = [(52, 0b00011111, 0b11100000, 5, 0), (53, 0b11111000, 0b00000111, 5, 3)]

    class FrntRgtRdrObj1RdrObjLifeCycle:
        sig_name = "FrntRgtRdrObj1RdrObjLifeCycle"
        sig_start_bit = 104
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
        startbit = 104
        bmuws_info = [(13, 0b00000001, 0b11111110, 1, 0), (14, 0b11111100, 0b00000011, 6, 2)]

    class FrntRgtRdrObj3RdrObjDxStdDe:
        sig_name = "FrntRgtRdrObj3RdrObjDxStdDe"
        sig_start_bit = 391
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 391
        bmuws_info = [(48, 0b11111111, 0b00000000, 8, 0), (49, 0b11100000, 0b00011111, 3, 5)]

    class FrntRgtRdrObj1_UB:
        sig_name = "FrntRgtRdrObj1_UB"
        sig_start_bit = 175
        update_id_bit = 175
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
        startbit = 175
        byte = 21
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class FrntRgtRdrObj3RdrObjHeightStdDe:
        sig_name = "FrntRgtRdrObj3RdrObjHeightStdDe"
        sig_start_bit = 432
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 432
        bmuws_info = [(54, 0b00000001, 0b11111110, 1, 0), (55, 0b11111111, 0b00000000, 8, 0), (56, 0b10000000, 0b01111111, 1, 7)]

    class FrntRgtRdrObj2ObjBoxCenterLat:
        sig_name = "FrntRgtRdrObj2ObjBoxCenterLat"
        sig_start_bit = 215
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 215
        byte = 26
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntRgtRdrObj3RdrObjDyStdDe:
        sig_name = "FrntRgtRdrObj3RdrObjDyStdDe"
        sig_start_bit = 415
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 415
        bmuws_info = [(51, 0b11111111, 0b00000000, 8, 0), (52, 0b11100000, 0b00011111, 3, 5)]

    class FrntRgtRdrObj1RdrObjExistProb:
        sig_name = "FrntRgtRdrObj1RdrObjExistProb"
        sig_start_bit = 76
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 76
        bmuws_info = [(9, 0b00011111, 0b11100000, 5, 0), (10, 0b11111000, 0b00000111, 5, 3)]

    class FrntRgtRdrObj2RdrObjID:
        sig_name = "FrntRgtRdrObj2RdrObjID"
        sig_start_bit = 286
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 286
        byte = 35
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class FrntRgtRdrObj2RdrObjDyStdDe:
        sig_name = "FrntRgtRdrObj2RdrObjDyStdDe"
        sig_start_bit = 247
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 247
        bmuws_info = [(30, 0b11111111, 0b00000000, 8, 0), (31, 0b11100000, 0b00011111, 3, 5)]

    class FrntRgtRdrObj2RdrObjExistProb:
        sig_name = "FrntRgtRdrObj2RdrObjExistProb"
        sig_start_bit = 252
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 252
        bmuws_info = [(31, 0b00011111, 0b11100000, 5, 0), (32, 0b11111000, 0b00000111, 5, 3)]

    class FrntRgtRdrObj3_UB:
        sig_name = "FrntRgtRdrObj3_UB"
        sig_start_bit = 171
        update_id_bit = 171
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
        startbit = 171
        byte = 21
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class FrntRgtRdrObj3RdrObjVxStdDe:
        sig_name = "FrntRgtRdrObj3RdrObjVxStdDe"
        sig_start_bit = 486
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 486
        bmuws_info = [(60, 0b01111111, 0b10000000, 7, 0), (61, 0b11100000, 0b00011111, 3, 5)]

    class FrntRgtRdrObj2RdrObjDxStdDe:
        sig_name = "FrntRgtRdrObj2RdrObjDxStdDe"
        sig_start_bit = 223
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 223
        bmuws_info = [(27, 0b11111111, 0b00000000, 8, 0), (28, 0b11100000, 0b00011111, 3, 5)]

    class FrntRgtRdrObj3RdrObjVy:
        sig_name = "FrntRgtRdrObj3RdrObjVy"
        sig_start_bit = 492
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 492
        bmuws_info = [(61, 0b00011111, 0b11100000, 5, 0), (62, 0b11111100, 0b00000011, 6, 2)]

    class FrntRgtRdrObj1ObjBoxCenterLgt:
        sig_name = "FrntRgtRdrObj1ObjBoxCenterLgt"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
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

    class FrntRgtRdrObj3ObjBoxCenterLat:
        sig_name = "FrntRgtRdrObj3ObjBoxCenterLat"
        sig_start_bit = 383
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 383
        byte = 47
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntRgtRdrObj3RdrObjVyStdDe:
        sig_name = "FrntRgtRdrObj3RdrObjVyStdDe"
        sig_start_bit = 497
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 497
        bmuws_info = [(62, 0b00000011, 0b11111100, 2, 0), (63, 0b11111111, 0b00000000, 8, 0)]

    class FrntRgtRdrObj1RdrObjVxStdDe:
        sig_name = "FrntRgtRdrObj1RdrObjVxStdDe"
        sig_start_bit = 142
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 142
        bmuws_info = [(17, 0b01111111, 0b10000000, 7, 0), (18, 0b11100000, 0b00011111, 3, 5)]

    class FrntRgtRdrObj3ObjBoxCenterLgt:
        sig_name = "FrntRgtRdrObj3ObjBoxCenterLgt"
        sig_start_bit = 375
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 375
        byte = 46
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntRgtRdrObj2RdrObjCntr:
        sig_name = "FrntRgtRdrObj2RdrObjCntr"
        sig_start_bit = 191
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
        startbit = 191
        byte = 23
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class FrntRgtRdrObj1RdrObjVy:
        sig_name = "FrntRgtRdrObj1RdrObjVy"
        sig_start_bit = 148
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 148
        bmuws_info = [(18, 0b00011111, 0b11100000, 5, 0), (19, 0b11111100, 0b00000011, 6, 2)]

    class FrntRgtRdrObj3RdrObjDx:
        sig_name = "FrntRgtRdrObj3RdrObjDx"
        sig_start_bit = 355
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 355
        bmuws_info = [(44, 0b00001111, 0b11110000, 4, 0), (45, 0b11111111, 0b00000000, 8, 0)]

    class FrntRgtRdrObj2RdrObjHeightStdDe:
        sig_name = "FrntRgtRdrObj2RdrObjHeightStdDe"
        sig_start_bit = 264
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 264
        bmuws_info = [(33, 0b00000001, 0b11111110, 1, 0), (34, 0b11111111, 0b00000000, 8, 0), (35, 0b10000000, 0b01111111, 1, 7)]

    class FrntRgtRdrObj2RdrObjVyStdDe:
        sig_name = "FrntRgtRdrObj2RdrObjVyStdDe"
        sig_start_bit = 329
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 329
        bmuws_info = [(41, 0b00000011, 0b11111100, 2, 0), (42, 0b11111111, 0b00000000, 8, 0)]

    class FrntRgtRdrObj2RdrObjVy:
        sig_name = "FrntRgtRdrObj2RdrObjVy"
        sig_start_bit = 324
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 324
        bmuws_info = [(40, 0b00011111, 0b11100000, 5, 0), (41, 0b11111100, 0b00000011, 6, 2)]

    class FrntRgtRdrObj1RdrObjPwr:
        sig_name = "FrntRgtRdrObj1RdrObjPwr"
        sig_start_bit = 113
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 113
        bmuws_info = [(14, 0b00000011, 0b11111100, 2, 0), (15, 0b11111100, 0b00000011, 6, 2)]


class BgmADCANFDFr21:
    msg_name = "BgmADCANFDFr21"
    msg_id = 513
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "BGM"
    rx_nodes = ['ACU']
    sig_group_dict = {'RearLeftRdrObj10': ['RearLeftRdrObj10ObjBoxCenterLat', 'RearLeftRdrObj10ObjBoxCenterLgt', 'RearLeftRdrObj10RdrObjChks', 'RearLeftRdrObj10RdrObjCntr', 'RearLeftRdrObj10RdrObjDx', 'RearLeftRdrObj10RdrObjDxStdDe', 'RearLeftRdrObj10RdrObjDy', 'RearLeftRdrObj10RdrObjDynProp', 'RearLeftRdrObj10RdrObjDyStdDe', 'RearLeftRdrObj10RdrObjExistProb', 'RearLeftRdrObj10RdrObjHeight', 'RearLeftRdrObj10RdrObjHeightStdDe', 'RearLeftRdrObj10RdrObjID', 'RearLeftRdrObj10RdrObjLifeCycle', 'RearLeftRdrObj10RdrObjPwr', 'RearLeftRdrObj10RdrObjVx', 'RearLeftRdrObj10RdrObjVxStdDe', 'RearLeftRdrObj10RdrObjVy', 'RearLeftRdrObj10RdrObjVyStdDe'], 'RearLeftRdrObj12': ['RearLeftRdrObj12ObjBoxCenterLat', 'RearLeftRdrObj12ObjBoxCenterLgt', 'RearLeftRdrObj12RdrObjChks', 'RearLeftRdrObj12RdrObjCntr', 'RearLeftRdrObj12RdrObjDx', 'RearLeftRdrObj12RdrObjDxStdDe', 'RearLeftRdrObj12RdrObjDy', 'RearLeftRdrObj12RdrObjDynProp', 'RearLeftRdrObj12RdrObjDyStdDe', 'RearLeftRdrObj12RdrObjExistProb', 'RearLeftRdrObj12RdrObjHeight', 'RearLeftRdrObj12RdrObjHeightStdDe', 'RearLeftRdrObj12RdrObjID', 'RearLeftRdrObj12RdrObjLifeCycle', 'RearLeftRdrObj12RdrObjPwr', 'RearLeftRdrObj12RdrObjVx', 'RearLeftRdrObj12RdrObjVxStdDe', 'RearLeftRdrObj12RdrObjVy', 'RearLeftRdrObj12RdrObjVyStdDe'], 'RearLeftRdrObj11': ['RearLeftRdrObj11ObjBoxCenterLat', 'RearLeftRdrObj11ObjBoxCenterLgt', 'RearLeftRdrObj11RdrObjChks', 'RearLeftRdrObj11RdrObjCntr', 'RearLeftRdrObj11RdrObjDx', 'RearLeftRdrObj11RdrObjDxStdDe', 'RearLeftRdrObj11RdrObjDy', 'RearLeftRdrObj11RdrObjDynProp', 'RearLeftRdrObj11RdrObjDyStdDe', 'RearLeftRdrObj11RdrObjExistProb', 'RearLeftRdrObj11RdrObjHeight', 'RearLeftRdrObj11RdrObjHeightStdDe', 'RearLeftRdrObj11RdrObjID', 'RearLeftRdrObj11RdrObjLifeCycle', 'RearLeftRdrObj11RdrObjPwr', 'RearLeftRdrObj11RdrObjVx', 'RearLeftRdrObj11RdrObjVxStdDe', 'RearLeftRdrObj11RdrObjVy', 'RearLeftRdrObj11RdrObjVyStdDe']}
    sig_group_dataid_dict = {}

    class RearLeftRdrObj12RdrObjDynProp:
        sig_name = "RearLeftRdrObj12RdrObjDynProp"
        sig_start_bit = 396
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 396
        byte = 49
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class RearLeftRdrObj12ObjBoxCenterLat:
        sig_name = "RearLeftRdrObj12ObjBoxCenterLat"
        sig_start_bit = 383
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 383
        byte = 47
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearLeftRdrObj11RdrObjID:
        sig_name = "RearLeftRdrObj11RdrObjID"
        sig_start_bit = 286
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 286
        byte = 35
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class RearLeftRdrObj10RdrObjVyStdDe:
        sig_name = "RearLeftRdrObj10RdrObjVyStdDe"
        sig_start_bit = 153
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 153
        bmuws_info = [(19, 0b00000011, 0b11111100, 2, 0), (20, 0b11111111, 0b00000000, 8, 0)]

    class RearLeftRdrObj11RdrObjVy:
        sig_name = "RearLeftRdrObj11RdrObjVy"
        sig_start_bit = 324
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 324
        bmuws_info = [(40, 0b00011111, 0b11100000, 5, 0), (41, 0b11111100, 0b00000011, 6, 2)]

    class RearLeftRdrObj12RdrObjDxStdDe:
        sig_name = "RearLeftRdrObj12RdrObjDxStdDe"
        sig_start_bit = 391
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 391
        bmuws_info = [(48, 0b11111111, 0b00000000, 8, 0), (49, 0b11100000, 0b00011111, 3, 5)]

    class RearLeftRdrObj11RdrObjVxStdDe:
        sig_name = "RearLeftRdrObj11RdrObjVxStdDe"
        sig_start_bit = 318
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 318
        bmuws_info = [(39, 0b01111111, 0b10000000, 7, 0), (40, 0b11100000, 0b00011111, 3, 5)]

    class RearLeftRdrObj12RdrObjExistProb:
        sig_name = "RearLeftRdrObj12RdrObjExistProb"
        sig_start_bit = 420
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 420
        bmuws_info = [(52, 0b00011111, 0b11100000, 5, 0), (53, 0b11111000, 0b00000111, 5, 3)]

    class RearLeftRdrObj11RdrObjHeightStdDe:
        sig_name = "RearLeftRdrObj11RdrObjHeightStdDe"
        sig_start_bit = 264
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 264
        bmuws_info = [(33, 0b00000001, 0b11111110, 1, 0), (34, 0b11111111, 0b00000000, 8, 0), (35, 0b10000000, 0b01111111, 1, 7)]

    class RearLeftRdrObj11RdrObjVyStdDe:
        sig_name = "RearLeftRdrObj11RdrObjVyStdDe"
        sig_start_bit = 329
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 329
        bmuws_info = [(41, 0b00000011, 0b11111100, 2, 0), (42, 0b11111111, 0b00000000, 8, 0)]

    class RearLeftRdrObj11RdrObjHeight:
        sig_name = "RearLeftRdrObj11RdrObjHeight"
        sig_start_bit = 258
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 258
        bmuws_info = [(32, 0b00000111, 0b11111000, 3, 0), (33, 0b11111110, 0b00000001, 7, 1)]

    class RearLeftRdrObj11RdrObjDx:
        sig_name = "RearLeftRdrObj11RdrObjDx"
        sig_start_bit = 187
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 187
        bmuws_info = [(23, 0b00001111, 0b11110000, 4, 0), (24, 0b11111111, 0b00000000, 8, 0)]

    class RearLeftRdrObj10RdrObjID:
        sig_name = "RearLeftRdrObj10RdrObjID"
        sig_start_bit = 110
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 110
        byte = 13
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class RearLeftRdrObj11RdrObjExistProb:
        sig_name = "RearLeftRdrObj11RdrObjExistProb"
        sig_start_bit = 252
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 252
        bmuws_info = [(31, 0b00011111, 0b11100000, 5, 0), (32, 0b11111000, 0b00000111, 5, 3)]

    class RearLeftRdrObj10RdrObjDxStdDe:
        sig_name = "RearLeftRdrObj10RdrObjDxStdDe"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11100000, 0b00011111, 3, 5)]

    class RearLeftRdrObj10ObjBoxCenterLat:
        sig_name = "RearLeftRdrObj10ObjBoxCenterLat"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
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

    class RearLeftRdrObj11RdrObjPwr:
        sig_name = "RearLeftRdrObj11RdrObjPwr"
        sig_start_bit = 289
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 289
        bmuws_info = [(36, 0b00000011, 0b11111100, 2, 0), (37, 0b11111100, 0b00000011, 6, 2)]

    class RearLeftRdrObj10RdrObjCntr:
        sig_name = "RearLeftRdrObj10RdrObjCntr"
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

    class RearLeftRdrObj12RdrObjDy:
        sig_name = "RearLeftRdrObj12RdrObjDy"
        sig_start_bit = 395
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 395
        bmuws_info = [(49, 0b00001111, 0b11110000, 4, 0), (50, 0b11111111, 0b00000000, 8, 0)]

    class RearLeftRdrObj10_UB:
        sig_name = "RearLeftRdrObj10_UB"
        sig_start_bit = 175
        update_id_bit = 175
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
        startbit = 175
        byte = 21
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class RearLeftRdrObj11RdrObjDy:
        sig_name = "RearLeftRdrObj11RdrObjDy"
        sig_start_bit = 227
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 227
        bmuws_info = [(28, 0b00001111, 0b11110000, 4, 0), (29, 0b11111111, 0b00000000, 8, 0)]

    class RearLeftRdrObj12RdrObjVy:
        sig_name = "RearLeftRdrObj12RdrObjVy"
        sig_start_bit = 492
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 492
        bmuws_info = [(61, 0b00011111, 0b11100000, 5, 0), (62, 0b11111100, 0b00000011, 6, 2)]

    class RearLeftRdrObj10RdrObjVxStdDe:
        sig_name = "RearLeftRdrObj10RdrObjVxStdDe"
        sig_start_bit = 142
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 142
        bmuws_info = [(17, 0b01111111, 0b10000000, 7, 0), (18, 0b11100000, 0b00011111, 3, 5)]

    class RearLeftRdrObj12RdrObjLifeCycle:
        sig_name = "RearLeftRdrObj12RdrObjLifeCycle"
        sig_start_bit = 448
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
        startbit = 448
        bmuws_info = [(56, 0b00000001, 0b11111110, 1, 0), (57, 0b11111100, 0b00000011, 6, 2)]

    class RearLeftRdrObj12_UB:
        sig_name = "RearLeftRdrObj12_UB"
        sig_start_bit = 171
        update_id_bit = 171
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
        startbit = 171
        byte = 21
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class RearLeftRdrObj11RdrObjCntr:
        sig_name = "RearLeftRdrObj11RdrObjCntr"
        sig_start_bit = 191
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
        startbit = 191
        byte = 23
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class RearLeftRdrObj12ObjBoxCenterLgt:
        sig_name = "RearLeftRdrObj12ObjBoxCenterLgt"
        sig_start_bit = 375
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 375
        byte = 46
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearLeftRdrObj11RdrObjDyStdDe:
        sig_name = "RearLeftRdrObj11RdrObjDyStdDe"
        sig_start_bit = 247
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 247
        bmuws_info = [(30, 0b11111111, 0b00000000, 8, 0), (31, 0b11100000, 0b00011111, 3, 5)]

    class RearLeftRdrObj10RdrObjDynProp:
        sig_name = "RearLeftRdrObj10RdrObjDynProp"
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
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class RearLeftRdrObj12RdrObjDx:
        sig_name = "RearLeftRdrObj12RdrObjDx"
        sig_start_bit = 355
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 355
        bmuws_info = [(44, 0b00001111, 0b11110000, 4, 0), (45, 0b11111111, 0b00000000, 8, 0)]

    class RearLeftRdrObj12RdrObjVyStdDe:
        sig_name = "RearLeftRdrObj12RdrObjVyStdDe"
        sig_start_bit = 497
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 497
        bmuws_info = [(62, 0b00000011, 0b11111100, 2, 0), (63, 0b11111111, 0b00000000, 8, 0)]

    class RearLeftRdrObj12RdrObjVxStdDe:
        sig_name = "RearLeftRdrObj12RdrObjVxStdDe"
        sig_start_bit = 486
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 486
        bmuws_info = [(60, 0b01111111, 0b10000000, 7, 0), (61, 0b11100000, 0b00011111, 3, 5)]

    class RearLeftRdrObj10RdrObjLifeCycle:
        sig_name = "RearLeftRdrObj10RdrObjLifeCycle"
        sig_start_bit = 104
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
        startbit = 104
        bmuws_info = [(13, 0b00000001, 0b11111110, 1, 0), (14, 0b11111100, 0b00000011, 6, 2)]

    class RearLeftRdrObj11RdrObjDynProp:
        sig_name = "RearLeftRdrObj11RdrObjDynProp"
        sig_start_bit = 228
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 228
        byte = 28
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class RearLeftRdrObj10RdrObjDyStdDe:
        sig_name = "RearLeftRdrObj10RdrObjDyStdDe"
        sig_start_bit = 71
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 71
        bmuws_info = [(8, 0b11111111, 0b00000000, 8, 0), (9, 0b11100000, 0b00011111, 3, 5)]

    class RearLeftRdrObj10RdrObjDy:
        sig_name = "RearLeftRdrObj10RdrObjDy"
        sig_start_bit = 51
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 51
        bmuws_info = [(6, 0b00001111, 0b11110000, 4, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class RearLeftRdrObj10RdrObjHeight:
        sig_name = "RearLeftRdrObj10RdrObjHeight"
        sig_start_bit = 82
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 82
        bmuws_info = [(10, 0b00000111, 0b11111000, 3, 0), (11, 0b11111110, 0b00000001, 7, 1)]

    class RearLeftRdrObj10RdrObjDx:
        sig_name = "RearLeftRdrObj10RdrObjDx"
        sig_start_bit = 11
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 11
        bmuws_info = [(1, 0b00001111, 0b11110000, 4, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class RearLeftRdrObj10RdrObjVy:
        sig_name = "RearLeftRdrObj10RdrObjVy"
        sig_start_bit = 148
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 148
        bmuws_info = [(18, 0b00011111, 0b11100000, 5, 0), (19, 0b11111100, 0b00000011, 6, 2)]

    class RearLeftRdrObj12RdrObjChks:
        sig_name = "RearLeftRdrObj12RdrObjChks"
        sig_start_bit = 351
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
        startbit = 351
        byte = 43
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearLeftRdrObj12RdrObjHeightStdDe:
        sig_name = "RearLeftRdrObj12RdrObjHeightStdDe"
        sig_start_bit = 432
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 432
        bmuws_info = [(54, 0b00000001, 0b11111110, 1, 0), (55, 0b11111111, 0b00000000, 8, 0), (56, 0b10000000, 0b01111111, 1, 7)]

    class RearLeftRdrObj10RdrObjExistProb:
        sig_name = "RearLeftRdrObj10RdrObjExistProb"
        sig_start_bit = 76
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 76
        bmuws_info = [(9, 0b00011111, 0b11100000, 5, 0), (10, 0b11111000, 0b00000111, 5, 3)]

    class RearLeftRdrObj12RdrObjID:
        sig_name = "RearLeftRdrObj12RdrObjID"
        sig_start_bit = 454
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 454
        byte = 56
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class RearLeftRdrObj12RdrObjDyStdDe:
        sig_name = "RearLeftRdrObj12RdrObjDyStdDe"
        sig_start_bit = 415
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 415
        bmuws_info = [(51, 0b11111111, 0b00000000, 8, 0), (52, 0b11100000, 0b00011111, 3, 5)]

    class RearLeftRdrObj12RdrObjCntr:
        sig_name = "RearLeftRdrObj12RdrObjCntr"
        sig_start_bit = 359
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
        startbit = 359
        byte = 44
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class RearLeftRdrObj11RdrObjDxStdDe:
        sig_name = "RearLeftRdrObj11RdrObjDxStdDe"
        sig_start_bit = 223
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 223
        bmuws_info = [(27, 0b11111111, 0b00000000, 8, 0), (28, 0b11100000, 0b00011111, 3, 5)]

    class RearLeftRdrObj10RdrObjPwr:
        sig_name = "RearLeftRdrObj10RdrObjPwr"
        sig_start_bit = 113
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 113
        bmuws_info = [(14, 0b00000011, 0b11111100, 2, 0), (15, 0b11111100, 0b00000011, 6, 2)]

    class RearLeftRdrObj12RdrObjHeight:
        sig_name = "RearLeftRdrObj12RdrObjHeight"
        sig_start_bit = 426
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 426
        bmuws_info = [(53, 0b00000111, 0b11111000, 3, 0), (54, 0b11111110, 0b00000001, 7, 1)]

    class RearLeftRdrObj12RdrObjPwr:
        sig_name = "RearLeftRdrObj12RdrObjPwr"
        sig_start_bit = 457
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 457
        bmuws_info = [(57, 0b00000011, 0b11111100, 2, 0), (58, 0b11111100, 0b00000011, 6, 2)]

    class RearLeftRdrObj10ObjBoxCenterLgt:
        sig_name = "RearLeftRdrObj10ObjBoxCenterLgt"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
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

    class RearLeftRdrObj11ObjBoxCenterLat:
        sig_name = "RearLeftRdrObj11ObjBoxCenterLat"
        sig_start_bit = 215
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 215
        byte = 26
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearLeftRdrObj11RdrObjChks:
        sig_name = "RearLeftRdrObj11RdrObjChks"
        sig_start_bit = 183
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
        startbit = 183
        byte = 22
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearLeftRdrObj11RdrObjLifeCycle:
        sig_name = "RearLeftRdrObj11RdrObjLifeCycle"
        sig_start_bit = 280
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
        startbit = 280
        bmuws_info = [(35, 0b00000001, 0b11111110, 1, 0), (36, 0b11111100, 0b00000011, 6, 2)]

    class RearLeftRdrObj11_UB:
        sig_name = "RearLeftRdrObj11_UB"
        sig_start_bit = 168
        update_id_bit = 168
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
        startbit = 168
        byte = 21
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class RearLeftRdrObj10RdrObjVx:
        sig_name = "RearLeftRdrObj10RdrObjVx"
        sig_start_bit = 121
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 121
        bmuws_info = [(15, 0b00000011, 0b11111100, 2, 0), (16, 0b11111111, 0b00000000, 8, 0), (17, 0b10000000, 0b01111111, 1, 7)]

    class RearLeftRdrObj11ObjBoxCenterLgt:
        sig_name = "RearLeftRdrObj11ObjBoxCenterLgt"
        sig_start_bit = 207
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 207
        byte = 25
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearLeftRdrObj10RdrObjHeightStdDe:
        sig_name = "RearLeftRdrObj10RdrObjHeightStdDe"
        sig_start_bit = 88
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 88
        bmuws_info = [(11, 0b00000001, 0b11111110, 1, 0), (12, 0b11111111, 0b00000000, 8, 0), (13, 0b10000000, 0b01111111, 1, 7)]

    class RearLeftRdrObj10RdrObjChks:
        sig_name = "RearLeftRdrObj10RdrObjChks"
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

    class RearLeftRdrObj11RdrObjVx:
        sig_name = "RearLeftRdrObj11RdrObjVx"
        sig_start_bit = 297
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 297
        bmuws_info = [(37, 0b00000011, 0b11111100, 2, 0), (38, 0b11111111, 0b00000000, 8, 0), (39, 0b10000000, 0b01111111, 1, 7)]

    class RearLeftRdrObj12RdrObjVx:
        sig_name = "RearLeftRdrObj12RdrObjVx"
        sig_start_bit = 465
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 465
        bmuws_info = [(58, 0b00000011, 0b11111100, 2, 0), (59, 0b11111111, 0b00000000, 8, 0), (60, 0b10000000, 0b01111111, 1, 7)]


class BgmADCANFDFr28:
    msg_name = "BgmADCANFDFr28"
    msg_id = 520
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "BGM"
    rx_nodes = ['ACU']
    sig_group_dict = {'RearRgtRdrObj15': ['RearRgtRdrObj15ObjBoxCenterLat', 'RearRgtRdrObj15ObjBoxCenterLgt', 'RearRgtRdrObj15RdrObjChks', 'RearRgtRdrObj15RdrObjCntr', 'RearRgtRdrObj15RdrObjDx', 'RearRgtRdrObj15RdrObjDxStdDe', 'RearRgtRdrObj15RdrObjDy', 'RearRgtRdrObj15RdrObjDynProp', 'RearRgtRdrObj15RdrObjDyStdDe', 'RearRgtRdrObj15RdrObjExistProb', 'RearRgtRdrObj15RdrObjHeight', 'RearRgtRdrObj15RdrObjHeightStdDe', 'RearRgtRdrObj15RdrObjID', 'RearRgtRdrObj15RdrObjLifeCycle', 'RearRgtRdrObj15RdrObjPwr', 'RearRgtRdrObj15RdrObjVx', 'RearRgtRdrObj15RdrObjVxStdDe', 'RearRgtRdrObj15RdrObjVy', 'RearRgtRdrObj15RdrObjVyStdDe'], 'RearRgtRdrObj13': ['RearRgtRdrObj13ObjBoxCenterLat', 'RearRgtRdrObj13ObjBoxCenterLgt', 'RearRgtRdrObj13RdrObjChks', 'RearRgtRdrObj13RdrObjCntr', 'RearRgtRdrObj13RdrObjDx', 'RearRgtRdrObj13RdrObjDxStdDe', 'RearRgtRdrObj13RdrObjDy', 'RearRgtRdrObj13RdrObjDynProp', 'RearRgtRdrObj13RdrObjDyStdDe', 'RearRgtRdrObj13RdrObjExistProb', 'RearRgtRdrObj13RdrObjHeight', 'RearRgtRdrObj13RdrObjHeightStdDe', 'RearRgtRdrObj13RdrObjID', 'RearRgtRdrObj13RdrObjLifeCycle', 'RearRgtRdrObj13RdrObjPwr', 'RearRgtRdrObj13RdrObjVx', 'RearRgtRdrObj13RdrObjVxStdDe', 'RearRgtRdrObj13RdrObjVy', 'RearRgtRdrObj13RdrObjVyStdDe'], 'RearRgtRdrObj14': ['RearRgtRdrObj14ObjBoxCenterLat', 'RearRgtRdrObj14ObjBoxCenterLgt', 'RearRgtRdrObj14RdrObjChks', 'RearRgtRdrObj14RdrObjCntr', 'RearRgtRdrObj14RdrObjDx', 'RearRgtRdrObj14RdrObjDxStdDe', 'RearRgtRdrObj14RdrObjDy', 'RearRgtRdrObj14RdrObjDynProp', 'RearRgtRdrObj14RdrObjDyStdDe', 'RearRgtRdrObj14RdrObjExistProb', 'RearRgtRdrObj14RdrObjHeight', 'RearRgtRdrObj14RdrObjHeightStdDe', 'RearRgtRdrObj14RdrObjID', 'RearRgtRdrObj14RdrObjLifeCycle', 'RearRgtRdrObj14RdrObjPwr', 'RearRgtRdrObj14RdrObjVx', 'RearRgtRdrObj14RdrObjVxStdDe', 'RearRgtRdrObj14RdrObjVy', 'RearRgtRdrObj14RdrObjVyStdDe']}
    sig_group_dataid_dict = {}

    class RearRgtRdrObj14RdrObjCntr:
        sig_name = "RearRgtRdrObj14RdrObjCntr"
        sig_start_bit = 191
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
        startbit = 191
        byte = 23
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class RearRgtRdrObj15RdrObjVxStdDe:
        sig_name = "RearRgtRdrObj15RdrObjVxStdDe"
        sig_start_bit = 486
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 486
        bmuws_info = [(60, 0b01111111, 0b10000000, 7, 0), (61, 0b11100000, 0b00011111, 3, 5)]

    class RearRgtRdrObj14RdrObjChks:
        sig_name = "RearRgtRdrObj14RdrObjChks"
        sig_start_bit = 183
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
        startbit = 183
        byte = 22
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearRgtRdrObj13RdrObjVy:
        sig_name = "RearRgtRdrObj13RdrObjVy"
        sig_start_bit = 148
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 148
        bmuws_info = [(18, 0b00011111, 0b11100000, 5, 0), (19, 0b11111100, 0b00000011, 6, 2)]

    class RearRgtRdrObj15_UB:
        sig_name = "RearRgtRdrObj15_UB"
        sig_start_bit = 171
        update_id_bit = 171
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
        startbit = 171
        byte = 21
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class RearRgtRdrObj14RdrObjExistProb:
        sig_name = "RearRgtRdrObj14RdrObjExistProb"
        sig_start_bit = 252
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 252
        bmuws_info = [(31, 0b00011111, 0b11100000, 5, 0), (32, 0b11111000, 0b00000111, 5, 3)]

    class RearRgtRdrObj13RdrObjDyStdDe:
        sig_name = "RearRgtRdrObj13RdrObjDyStdDe"
        sig_start_bit = 71
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 71
        bmuws_info = [(8, 0b11111111, 0b00000000, 8, 0), (9, 0b11100000, 0b00011111, 3, 5)]

    class RearRgtRdrObj13RdrObjDxStdDe:
        sig_name = "RearRgtRdrObj13RdrObjDxStdDe"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11100000, 0b00011111, 3, 5)]

    class RearRgtRdrObj15RdrObjHeight:
        sig_name = "RearRgtRdrObj15RdrObjHeight"
        sig_start_bit = 426
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 426
        bmuws_info = [(53, 0b00000111, 0b11111000, 3, 0), (54, 0b11111110, 0b00000001, 7, 1)]

    class RearRgtRdrObj14RdrObjHeightStdDe:
        sig_name = "RearRgtRdrObj14RdrObjHeightStdDe"
        sig_start_bit = 264
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 264
        bmuws_info = [(33, 0b00000001, 0b11111110, 1, 0), (34, 0b11111111, 0b00000000, 8, 0), (35, 0b10000000, 0b01111111, 1, 7)]

    class RearRgtRdrObj14ObjBoxCenterLgt:
        sig_name = "RearRgtRdrObj14ObjBoxCenterLgt"
        sig_start_bit = 207
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 207
        byte = 25
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearRgtRdrObj14RdrObjDyStdDe:
        sig_name = "RearRgtRdrObj14RdrObjDyStdDe"
        sig_start_bit = 247
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 247
        bmuws_info = [(30, 0b11111111, 0b00000000, 8, 0), (31, 0b11100000, 0b00011111, 3, 5)]

    class RearRgtRdrObj15RdrObjVx:
        sig_name = "RearRgtRdrObj15RdrObjVx"
        sig_start_bit = 465
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 465
        bmuws_info = [(58, 0b00000011, 0b11111100, 2, 0), (59, 0b11111111, 0b00000000, 8, 0), (60, 0b10000000, 0b01111111, 1, 7)]

    class RearRgtRdrObj14RdrObjDy:
        sig_name = "RearRgtRdrObj14RdrObjDy"
        sig_start_bit = 227
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 227
        bmuws_info = [(28, 0b00001111, 0b11110000, 4, 0), (29, 0b11111111, 0b00000000, 8, 0)]

    class RearRgtRdrObj13RdrObjVyStdDe:
        sig_name = "RearRgtRdrObj13RdrObjVyStdDe"
        sig_start_bit = 153
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 153
        bmuws_info = [(19, 0b00000011, 0b11111100, 2, 0), (20, 0b11111111, 0b00000000, 8, 0)]

    class RearRgtRdrObj15RdrObjVyStdDe:
        sig_name = "RearRgtRdrObj15RdrObjVyStdDe"
        sig_start_bit = 497
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 497
        bmuws_info = [(62, 0b00000011, 0b11111100, 2, 0), (63, 0b11111111, 0b00000000, 8, 0)]

    class RearRgtRdrObj13RdrObjExistProb:
        sig_name = "RearRgtRdrObj13RdrObjExistProb"
        sig_start_bit = 76
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 76
        bmuws_info = [(9, 0b00011111, 0b11100000, 5, 0), (10, 0b11111000, 0b00000111, 5, 3)]

    class RearRgtRdrObj15RdrObjDyStdDe:
        sig_name = "RearRgtRdrObj15RdrObjDyStdDe"
        sig_start_bit = 415
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 415
        bmuws_info = [(51, 0b11111111, 0b00000000, 8, 0), (52, 0b11100000, 0b00011111, 3, 5)]

    class RearRgtRdrObj14RdrObjDxStdDe:
        sig_name = "RearRgtRdrObj14RdrObjDxStdDe"
        sig_start_bit = 223
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 223
        bmuws_info = [(27, 0b11111111, 0b00000000, 8, 0), (28, 0b11100000, 0b00011111, 3, 5)]

    class RearRgtRdrObj13RdrObjDynProp:
        sig_name = "RearRgtRdrObj13RdrObjDynProp"
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
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class RearRgtRdrObj13ObjBoxCenterLat:
        sig_name = "RearRgtRdrObj13ObjBoxCenterLat"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
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

    class RearRgtRdrObj13ObjBoxCenterLgt:
        sig_name = "RearRgtRdrObj13ObjBoxCenterLgt"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
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

    class RearRgtRdrObj13RdrObjVxStdDe:
        sig_name = "RearRgtRdrObj13RdrObjVxStdDe"
        sig_start_bit = 142
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 142
        bmuws_info = [(17, 0b01111111, 0b10000000, 7, 0), (18, 0b11100000, 0b00011111, 3, 5)]

    class RearRgtRdrObj13RdrObjPwr:
        sig_name = "RearRgtRdrObj13RdrObjPwr"
        sig_start_bit = 113
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 113
        bmuws_info = [(14, 0b00000011, 0b11111100, 2, 0), (15, 0b11111100, 0b00000011, 6, 2)]

    class RearRgtRdrObj13_UB:
        sig_name = "RearRgtRdrObj13_UB"
        sig_start_bit = 175
        update_id_bit = 175
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
        startbit = 175
        byte = 21
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class RearRgtRdrObj15RdrObjChks:
        sig_name = "RearRgtRdrObj15RdrObjChks"
        sig_start_bit = 351
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
        startbit = 351
        byte = 43
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearRgtRdrObj15RdrObjDx:
        sig_name = "RearRgtRdrObj15RdrObjDx"
        sig_start_bit = 355
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 355
        bmuws_info = [(44, 0b00001111, 0b11110000, 4, 0), (45, 0b11111111, 0b00000000, 8, 0)]

    class RearRgtRdrObj14RdrObjDynProp:
        sig_name = "RearRgtRdrObj14RdrObjDynProp"
        sig_start_bit = 228
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 228
        byte = 28
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class RearRgtRdrObj15RdrObjCntr:
        sig_name = "RearRgtRdrObj15RdrObjCntr"
        sig_start_bit = 359
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
        startbit = 359
        byte = 44
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class RearRgtRdrObj15RdrObjDynProp:
        sig_name = "RearRgtRdrObj15RdrObjDynProp"
        sig_start_bit = 396
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 396
        byte = 49
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class RearRgtRdrObj13RdrObjDy:
        sig_name = "RearRgtRdrObj13RdrObjDy"
        sig_start_bit = 51
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 51
        bmuws_info = [(6, 0b00001111, 0b11110000, 4, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class RearRgtRdrObj15RdrObjHeightStdDe:
        sig_name = "RearRgtRdrObj15RdrObjHeightStdDe"
        sig_start_bit = 432
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 432
        bmuws_info = [(54, 0b00000001, 0b11111110, 1, 0), (55, 0b11111111, 0b00000000, 8, 0), (56, 0b10000000, 0b01111111, 1, 7)]

    class RearRgtRdrObj14RdrObjLifeCycle:
        sig_name = "RearRgtRdrObj14RdrObjLifeCycle"
        sig_start_bit = 280
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
        startbit = 280
        bmuws_info = [(35, 0b00000001, 0b11111110, 1, 0), (36, 0b11111100, 0b00000011, 6, 2)]

    class RearRgtRdrObj13RdrObjCntr:
        sig_name = "RearRgtRdrObj13RdrObjCntr"
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

    class RearRgtRdrObj14RdrObjVy:
        sig_name = "RearRgtRdrObj14RdrObjVy"
        sig_start_bit = 324
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 324
        bmuws_info = [(40, 0b00011111, 0b11100000, 5, 0), (41, 0b11111100, 0b00000011, 6, 2)]

    class RearRgtRdrObj14RdrObjID:
        sig_name = "RearRgtRdrObj14RdrObjID"
        sig_start_bit = 286
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 286
        byte = 35
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class RearRgtRdrObj14ObjBoxCenterLat:
        sig_name = "RearRgtRdrObj14ObjBoxCenterLat"
        sig_start_bit = 215
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 215
        byte = 26
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearRgtRdrObj15RdrObjLifeCycle:
        sig_name = "RearRgtRdrObj15RdrObjLifeCycle"
        sig_start_bit = 448
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
        startbit = 448
        bmuws_info = [(56, 0b00000001, 0b11111110, 1, 0), (57, 0b11111100, 0b00000011, 6, 2)]

    class RearRgtRdrObj15RdrObjDy:
        sig_name = "RearRgtRdrObj15RdrObjDy"
        sig_start_bit = 395
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 395
        bmuws_info = [(49, 0b00001111, 0b11110000, 4, 0), (50, 0b11111111, 0b00000000, 8, 0)]

    class RearRgtRdrObj14RdrObjVxStdDe:
        sig_name = "RearRgtRdrObj14RdrObjVxStdDe"
        sig_start_bit = 318
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 318
        bmuws_info = [(39, 0b01111111, 0b10000000, 7, 0), (40, 0b11100000, 0b00011111, 3, 5)]

    class RearRgtRdrObj15ObjBoxCenterLat:
        sig_name = "RearRgtRdrObj15ObjBoxCenterLat"
        sig_start_bit = 383
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 383
        byte = 47
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearRgtRdrObj15RdrObjPwr:
        sig_name = "RearRgtRdrObj15RdrObjPwr"
        sig_start_bit = 457
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 457
        bmuws_info = [(57, 0b00000011, 0b11111100, 2, 0), (58, 0b11111100, 0b00000011, 6, 2)]

    class RearRgtRdrObj13RdrObjID:
        sig_name = "RearRgtRdrObj13RdrObjID"
        sig_start_bit = 110
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 110
        byte = 13
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class RearRgtRdrObj13RdrObjDx:
        sig_name = "RearRgtRdrObj13RdrObjDx"
        sig_start_bit = 11
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 11
        bmuws_info = [(1, 0b00001111, 0b11110000, 4, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class RearRgtRdrObj13RdrObjChks:
        sig_name = "RearRgtRdrObj13RdrObjChks"
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

    class RearRgtRdrObj15RdrObjVy:
        sig_name = "RearRgtRdrObj15RdrObjVy"
        sig_start_bit = 492
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 492
        bmuws_info = [(61, 0b00011111, 0b11100000, 5, 0), (62, 0b11111100, 0b00000011, 6, 2)]

    class RearRgtRdrObj14RdrObjHeight:
        sig_name = "RearRgtRdrObj14RdrObjHeight"
        sig_start_bit = 258
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 258
        bmuws_info = [(32, 0b00000111, 0b11111000, 3, 0), (33, 0b11111110, 0b00000001, 7, 1)]

    class RearRgtRdrObj15RdrObjID:
        sig_name = "RearRgtRdrObj15RdrObjID"
        sig_start_bit = 454
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 454
        byte = 56
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class RearRgtRdrObj13RdrObjHeightStdDe:
        sig_name = "RearRgtRdrObj13RdrObjHeightStdDe"
        sig_start_bit = 88
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 88
        bmuws_info = [(11, 0b00000001, 0b11111110, 1, 0), (12, 0b11111111, 0b00000000, 8, 0), (13, 0b10000000, 0b01111111, 1, 7)]

    class RearRgtRdrObj14RdrObjPwr:
        sig_name = "RearRgtRdrObj14RdrObjPwr"
        sig_start_bit = 289
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 289
        bmuws_info = [(36, 0b00000011, 0b11111100, 2, 0), (37, 0b11111100, 0b00000011, 6, 2)]

    class RearRgtRdrObj13RdrObjVx:
        sig_name = "RearRgtRdrObj13RdrObjVx"
        sig_start_bit = 121
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 121
        bmuws_info = [(15, 0b00000011, 0b11111100, 2, 0), (16, 0b11111111, 0b00000000, 8, 0), (17, 0b10000000, 0b01111111, 1, 7)]

    class RearRgtRdrObj13RdrObjLifeCycle:
        sig_name = "RearRgtRdrObj13RdrObjLifeCycle"
        sig_start_bit = 104
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
        startbit = 104
        bmuws_info = [(13, 0b00000001, 0b11111110, 1, 0), (14, 0b11111100, 0b00000011, 6, 2)]

    class RearRgtRdrObj15ObjBoxCenterLgt:
        sig_name = "RearRgtRdrObj15ObjBoxCenterLgt"
        sig_start_bit = 375
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 375
        byte = 46
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearRgtRdrObj15RdrObjDxStdDe:
        sig_name = "RearRgtRdrObj15RdrObjDxStdDe"
        sig_start_bit = 391
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 391
        bmuws_info = [(48, 0b11111111, 0b00000000, 8, 0), (49, 0b11100000, 0b00011111, 3, 5)]

    class RearRgtRdrObj15RdrObjExistProb:
        sig_name = "RearRgtRdrObj15RdrObjExistProb"
        sig_start_bit = 420
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 420
        bmuws_info = [(52, 0b00011111, 0b11100000, 5, 0), (53, 0b11111000, 0b00000111, 5, 3)]

    class RearRgtRdrObj13RdrObjHeight:
        sig_name = "RearRgtRdrObj13RdrObjHeight"
        sig_start_bit = 82
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 82
        bmuws_info = [(10, 0b00000111, 0b11111000, 3, 0), (11, 0b11111110, 0b00000001, 7, 1)]

    class RearRgtRdrObj14RdrObjDx:
        sig_name = "RearRgtRdrObj14RdrObjDx"
        sig_start_bit = 187
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 187
        bmuws_info = [(23, 0b00001111, 0b11110000, 4, 0), (24, 0b11111111, 0b00000000, 8, 0)]

    class RearRgtRdrObj14_UB:
        sig_name = "RearRgtRdrObj14_UB"
        sig_start_bit = 168
        update_id_bit = 168
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
        startbit = 168
        byte = 21
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class RearRgtRdrObj14RdrObjVx:
        sig_name = "RearRgtRdrObj14RdrObjVx"
        sig_start_bit = 297
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 297
        bmuws_info = [(37, 0b00000011, 0b11111100, 2, 0), (38, 0b11111111, 0b00000000, 8, 0), (39, 0b10000000, 0b01111111, 1, 7)]

    class RearRgtRdrObj14RdrObjVyStdDe:
        sig_name = "RearRgtRdrObj14RdrObjVyStdDe"
        sig_start_bit = 329
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 329
        bmuws_info = [(41, 0b00000011, 0b11111100, 2, 0), (42, 0b11111111, 0b00000000, 8, 0)]


class BgmADCANFDFr06:
    msg_name = "BgmADCANFDFr06"
    msg_id = 496
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "BGM"
    rx_nodes = ['ACU']
    sig_group_dict = {'FrntLeftRdrObj1': ['FrntLeftRdrObj1ObjBoxCenterLat', 'FrntLeftRdrObj1ObjBoxCenterLgt', 'FrntLeftRdrObj1RdrObjChks', 'FrntLeftRdrObj1RdrObjCntr', 'FrntLeftRdrObj1RdrObjDx', 'FrntLeftRdrObj1RdrObjDxStdDe', 'FrntLeftRdrObj1RdrObjDy', 'FrntLeftRdrObj1RdrObjDynProp', 'FrntLeftRdrObj1RdrObjDyStdDe', 'FrntLeftRdrObj1RdrObjExistProb', 'FrntLeftRdrObj1RdrObjHeight', 'FrntLeftRdrObj1RdrObjHeightStdDe', 'FrntLeftRdrObj1RdrObjID', 'FrntLeftRdrObj1RdrObjLifeCycle', 'FrntLeftRdrObj1RdrObjPwr', 'FrntLeftRdrObj1RdrObjVx', 'FrntLeftRdrObj1RdrObjVxStdDe', 'FrntLeftRdrObj1RdrObjVy', 'FrntLeftRdrObj1RdrObjVyStdDe'], 'FrntLeftRdrObj2': ['FrntLeftRdrObj2ObjBoxCenterLat', 'FrntLeftRdrObj2ObjBoxCenterLgt', 'FrntLeftRdrObj2RdrObjChks', 'FrntLeftRdrObj2RdrObjCntr', 'FrntLeftRdrObj2RdrObjDx', 'FrntLeftRdrObj2RdrObjDxStdDe', 'FrntLeftRdrObj2RdrObjDy', 'FrntLeftRdrObj2RdrObjDynProp', 'FrntLeftRdrObj2RdrObjDyStdDe', 'FrntLeftRdrObj2RdrObjExistProb', 'FrntLeftRdrObj2RdrObjHeight', 'FrntLeftRdrObj2RdrObjHeightStdDe', 'FrntLeftRdrObj2RdrObjID', 'FrntLeftRdrObj2RdrObjLifeCycle', 'FrntLeftRdrObj2RdrObjPwr', 'FrntLeftRdrObj2RdrObjVx', 'FrntLeftRdrObj2RdrObjVxStdDe', 'FrntLeftRdrObj2RdrObjVy', 'FrntLeftRdrObj2RdrObjVyStdDe'], 'FrntLeftRdrObj3': ['FrntLeftRdrObj3ObjBoxCenterLat', 'FrntLeftRdrObj3ObjBoxCenterLgt', 'FrntLeftRdrObj3RdrObjChks', 'FrntLeftRdrObj3RdrObjCntr', 'FrntLeftRdrObj3RdrObjDx', 'FrntLeftRdrObj3RdrObjDxStdDe', 'FrntLeftRdrObj3RdrObjDy', 'FrntLeftRdrObj3RdrObjDynProp', 'FrntLeftRdrObj3RdrObjDyStdDe', 'FrntLeftRdrObj3RdrObjExistProb', 'FrntLeftRdrObj3RdrObjHeight', 'FrntLeftRdrObj3RdrObjHeightStdDe', 'FrntLeftRdrObj3RdrObjID', 'FrntLeftRdrObj3RdrObjLifeCycle', 'FrntLeftRdrObj3RdrObjPwr', 'FrntLeftRdrObj3RdrObjVx', 'FrntLeftRdrObj3RdrObjVxStdDe', 'FrntLeftRdrObj3RdrObjVy', 'FrntLeftRdrObj3RdrObjVyStdDe']}
    sig_group_dataid_dict = {}

    class FrntLeftRdrObj3RdrObjChks:
        sig_name = "FrntLeftRdrObj3RdrObjChks"
        sig_start_bit = 351
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
        startbit = 351
        byte = 43
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntLeftRdrObj1RdrObjCntr:
        sig_name = "FrntLeftRdrObj1RdrObjCntr"
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

    class FrntLeftRdrObj1RdrObjVyStdDe:
        sig_name = "FrntLeftRdrObj1RdrObjVyStdDe"
        sig_start_bit = 153
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 153
        bmuws_info = [(19, 0b00000011, 0b11111100, 2, 0), (20, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeftRdrObj1ObjBoxCenterLat:
        sig_name = "FrntLeftRdrObj1ObjBoxCenterLat"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
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

    class FrntLeftRdrObj2ObjBoxCenterLat:
        sig_name = "FrntLeftRdrObj2ObjBoxCenterLat"
        sig_start_bit = 215
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 215
        byte = 26
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntLeftRdrObj1RdrObjDynProp:
        sig_name = "FrntLeftRdrObj1RdrObjDynProp"
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
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class FrntLeftRdrObj3RdrObjHeight:
        sig_name = "FrntLeftRdrObj3RdrObjHeight"
        sig_start_bit = 426
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 426
        bmuws_info = [(53, 0b00000111, 0b11111000, 3, 0), (54, 0b11111110, 0b00000001, 7, 1)]

    class FrntLeftRdrObj3RdrObjHeightStdDe:
        sig_name = "FrntLeftRdrObj3RdrObjHeightStdDe"
        sig_start_bit = 432
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 432
        bmuws_info = [(54, 0b00000001, 0b11111110, 1, 0), (55, 0b11111111, 0b00000000, 8, 0), (56, 0b10000000, 0b01111111, 1, 7)]

    class FrntLeftRdrObj3RdrObjDxStdDe:
        sig_name = "FrntLeftRdrObj3RdrObjDxStdDe"
        sig_start_bit = 391
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 391
        bmuws_info = [(48, 0b11111111, 0b00000000, 8, 0), (49, 0b11100000, 0b00011111, 3, 5)]

    class FrntLeftRdrObj1RdrObjID:
        sig_name = "FrntLeftRdrObj1RdrObjID"
        sig_start_bit = 110
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 110
        byte = 13
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class FrntLeftRdrObj1RdrObjVy:
        sig_name = "FrntLeftRdrObj1RdrObjVy"
        sig_start_bit = 148
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 148
        bmuws_info = [(18, 0b00011111, 0b11100000, 5, 0), (19, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeftRdrObj3RdrObjDyStdDe:
        sig_name = "FrntLeftRdrObj3RdrObjDyStdDe"
        sig_start_bit = 415
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 415
        bmuws_info = [(51, 0b11111111, 0b00000000, 8, 0), (52, 0b11100000, 0b00011111, 3, 5)]

    class FrntLeftRdrObj1RdrObjPwr:
        sig_name = "FrntLeftRdrObj1RdrObjPwr"
        sig_start_bit = 113
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 113
        bmuws_info = [(14, 0b00000011, 0b11111100, 2, 0), (15, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeftRdrObj1RdrObjVxStdDe:
        sig_name = "FrntLeftRdrObj1RdrObjVxStdDe"
        sig_start_bit = 142
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 142
        bmuws_info = [(17, 0b01111111, 0b10000000, 7, 0), (18, 0b11100000, 0b00011111, 3, 5)]

    class FrntLeftRdrObj1RdrObjDxStdDe:
        sig_name = "FrntLeftRdrObj1RdrObjDxStdDe"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11100000, 0b00011111, 3, 5)]

    class FrntLeftRdrObj1RdrObjDyStdDe:
        sig_name = "FrntLeftRdrObj1RdrObjDyStdDe"
        sig_start_bit = 71
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 71
        bmuws_info = [(8, 0b11111111, 0b00000000, 8, 0), (9, 0b11100000, 0b00011111, 3, 5)]

    class FrntLeftRdrObj1_UB:
        sig_name = "FrntLeftRdrObj1_UB"
        sig_start_bit = 175
        update_id_bit = 175
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
        startbit = 175
        byte = 21
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class FrntLeftRdrObj3RdrObjID:
        sig_name = "FrntLeftRdrObj3RdrObjID"
        sig_start_bit = 454
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 454
        byte = 56
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class FrntLeftRdrObj2RdrObjHeight:
        sig_name = "FrntLeftRdrObj2RdrObjHeight"
        sig_start_bit = 258
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 258
        bmuws_info = [(32, 0b00000111, 0b11111000, 3, 0), (33, 0b11111110, 0b00000001, 7, 1)]

    class FrntLeftRdrObj2ObjBoxCenterLgt:
        sig_name = "FrntLeftRdrObj2ObjBoxCenterLgt"
        sig_start_bit = 207
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 207
        byte = 25
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntLeftRdrObj2RdrObjChks:
        sig_name = "FrntLeftRdrObj2RdrObjChks"
        sig_start_bit = 183
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
        startbit = 183
        byte = 22
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntLeftRdrObj2RdrObjDy:
        sig_name = "FrntLeftRdrObj2RdrObjDy"
        sig_start_bit = 227
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 227
        bmuws_info = [(28, 0b00001111, 0b11110000, 4, 0), (29, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeftRdrObj2RdrObjID:
        sig_name = "FrntLeftRdrObj2RdrObjID"
        sig_start_bit = 286
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 286
        byte = 35
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class FrntLeftRdrObj1RdrObjVx:
        sig_name = "FrntLeftRdrObj1RdrObjVx"
        sig_start_bit = 121
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 121
        bmuws_info = [(15, 0b00000011, 0b11111100, 2, 0), (16, 0b11111111, 0b00000000, 8, 0), (17, 0b10000000, 0b01111111, 1, 7)]

    class FrntLeftRdrObj2RdrObjVx:
        sig_name = "FrntLeftRdrObj2RdrObjVx"
        sig_start_bit = 297
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 297
        bmuws_info = [(37, 0b00000011, 0b11111100, 2, 0), (38, 0b11111111, 0b00000000, 8, 0), (39, 0b10000000, 0b01111111, 1, 7)]

    class FrntLeftRdrObj2RdrObjHeightStdDe:
        sig_name = "FrntLeftRdrObj2RdrObjHeightStdDe"
        sig_start_bit = 264
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 264
        bmuws_info = [(33, 0b00000001, 0b11111110, 1, 0), (34, 0b11111111, 0b00000000, 8, 0), (35, 0b10000000, 0b01111111, 1, 7)]

    class FrntLeftRdrObj2RdrObjPwr:
        sig_name = "FrntLeftRdrObj2RdrObjPwr"
        sig_start_bit = 289
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 289
        bmuws_info = [(36, 0b00000011, 0b11111100, 2, 0), (37, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeftRdrObj3RdrObjVx:
        sig_name = "FrntLeftRdrObj3RdrObjVx"
        sig_start_bit = 465
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 465
        bmuws_info = [(58, 0b00000011, 0b11111100, 2, 0), (59, 0b11111111, 0b00000000, 8, 0), (60, 0b10000000, 0b01111111, 1, 7)]

    class FrntLeftRdrObj3RdrObjVy:
        sig_name = "FrntLeftRdrObj3RdrObjVy"
        sig_start_bit = 492
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 492
        bmuws_info = [(61, 0b00011111, 0b11100000, 5, 0), (62, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeftRdrObj2RdrObjVy:
        sig_name = "FrntLeftRdrObj2RdrObjVy"
        sig_start_bit = 324
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -6.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 324
        bmuws_info = [(40, 0b00011111, 0b11100000, 5, 0), (41, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeftRdrObj3RdrObjDx:
        sig_name = "FrntLeftRdrObj3RdrObjDx"
        sig_start_bit = 355
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 355
        bmuws_info = [(44, 0b00001111, 0b11110000, 4, 0), (45, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeftRdrObj3RdrObjDy:
        sig_name = "FrntLeftRdrObj3RdrObjDy"
        sig_start_bit = 395
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 395
        bmuws_info = [(49, 0b00001111, 0b11110000, 4, 0), (50, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeftRdrObj1ObjBoxCenterLgt:
        sig_name = "FrntLeftRdrObj1ObjBoxCenterLgt"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
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

    class FrntLeftRdrObj2RdrObjLifeCycle:
        sig_name = "FrntLeftRdrObj2RdrObjLifeCycle"
        sig_start_bit = 280
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
        startbit = 280
        bmuws_info = [(35, 0b00000001, 0b11111110, 1, 0), (36, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeftRdrObj1RdrObjHeight:
        sig_name = "FrntLeftRdrObj1RdrObjHeight"
        sig_start_bit = 82
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 82
        bmuws_info = [(10, 0b00000111, 0b11111000, 3, 0), (11, 0b11111110, 0b00000001, 7, 1)]

    class FrntLeftRdrObj2RdrObjCntr:
        sig_name = "FrntLeftRdrObj2RdrObjCntr"
        sig_start_bit = 191
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
        startbit = 191
        byte = 23
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class FrntLeftRdrObj2RdrObjDx:
        sig_name = "FrntLeftRdrObj2RdrObjDx"
        sig_start_bit = 187
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 187
        bmuws_info = [(23, 0b00001111, 0b11110000, 4, 0), (24, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeftRdrObj2RdrObjVxStdDe:
        sig_name = "FrntLeftRdrObj2RdrObjVxStdDe"
        sig_start_bit = 318
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 318
        bmuws_info = [(39, 0b01111111, 0b10000000, 7, 0), (40, 0b11100000, 0b00011111, 3, 5)]

    class FrntLeftRdrObj3ObjBoxCenterLgt:
        sig_name = "FrntLeftRdrObj3ObjBoxCenterLgt"
        sig_start_bit = 375
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 375
        byte = 46
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntLeftRdrObj3RdrObjCntr:
        sig_name = "FrntLeftRdrObj3RdrObjCntr"
        sig_start_bit = 359
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
        startbit = 359
        byte = 44
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class FrntLeftRdrObj2RdrObjDynProp:
        sig_name = "FrntLeftRdrObj2RdrObjDynProp"
        sig_start_bit = 228
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 228
        byte = 28
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class FrntLeftRdrObj2_UB:
        sig_name = "FrntLeftRdrObj2_UB"
        sig_start_bit = 168
        update_id_bit = 168
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
        startbit = 168
        byte = 21
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FrntLeftRdrObj1RdrObjDx:
        sig_name = "FrntLeftRdrObj1RdrObjDx"
        sig_start_bit = 11
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 11
        bmuws_info = [(1, 0b00001111, 0b11110000, 4, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeftRdrObj2RdrObjVyStdDe:
        sig_name = "FrntLeftRdrObj2RdrObjVyStdDe"
        sig_start_bit = 329
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 329
        bmuws_info = [(41, 0b00000011, 0b11111100, 2, 0), (42, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeftRdrObj2RdrObjDxStdDe:
        sig_name = "FrntLeftRdrObj2RdrObjDxStdDe"
        sig_start_bit = 223
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 223
        bmuws_info = [(27, 0b11111111, 0b00000000, 8, 0), (28, 0b11100000, 0b00011111, 3, 5)]

    class FrntLeftRdrObj1RdrObjChks:
        sig_name = "FrntLeftRdrObj1RdrObjChks"
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

    class FrntLeftRdrObj3RdrObjDynProp:
        sig_name = "FrntLeftRdrObj3RdrObjDynProp"
        sig_start_bit = 396
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 396
        byte = 49
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class FrntLeftRdrObj2RdrObjExistProb:
        sig_name = "FrntLeftRdrObj2RdrObjExistProb"
        sig_start_bit = 252
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 252
        bmuws_info = [(31, 0b00011111, 0b11100000, 5, 0), (32, 0b11111000, 0b00000111, 5, 3)]

    class FrntLeftRdrObj3RdrObjVxStdDe:
        sig_name = "FrntLeftRdrObj3RdrObjVxStdDe"
        sig_start_bit = 486
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 486
        bmuws_info = [(60, 0b01111111, 0b10000000, 7, 0), (61, 0b11100000, 0b00011111, 3, 5)]

    class FrntLeftRdrObj1RdrObjDy:
        sig_name = "FrntLeftRdrObj1RdrObjDy"
        sig_start_bit = 51
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 51
        bmuws_info = [(6, 0b00001111, 0b11110000, 4, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeftRdrObj3RdrObjVyStdDe:
        sig_name = "FrntLeftRdrObj3RdrObjVyStdDe"
        sig_start_bit = 497
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 497
        bmuws_info = [(62, 0b00000011, 0b11111100, 2, 0), (63, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeftRdrObj2RdrObjDyStdDe:
        sig_name = "FrntLeftRdrObj2RdrObjDyStdDe"
        sig_start_bit = 247
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 247
        bmuws_info = [(30, 0b11111111, 0b00000000, 8, 0), (31, 0b11100000, 0b00011111, 3, 5)]

    class FrntLeftRdrObj3RdrObjLifeCycle:
        sig_name = "FrntLeftRdrObj3RdrObjLifeCycle"
        sig_start_bit = 448
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
        startbit = 448
        bmuws_info = [(56, 0b00000001, 0b11111110, 1, 0), (57, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeftRdrObj1RdrObjExistProb:
        sig_name = "FrntLeftRdrObj1RdrObjExistProb"
        sig_start_bit = 76
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 76
        bmuws_info = [(9, 0b00011111, 0b11100000, 5, 0), (10, 0b11111000, 0b00000111, 5, 3)]

    class FrntLeftRdrObj3RdrObjExistProb:
        sig_name = "FrntLeftRdrObj3RdrObjExistProb"
        sig_start_bit = 420
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 420
        bmuws_info = [(52, 0b00011111, 0b11100000, 5, 0), (53, 0b11111000, 0b00000111, 5, 3)]

    class FrntLeftRdrObj3RdrObjPwr:
        sig_name = "FrntLeftRdrObj3RdrObjPwr"
        sig_start_bit = 457
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -20.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 457
        bmuws_info = [(57, 0b00000011, 0b11111100, 2, 0), (58, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeftRdrObj3_UB:
        sig_name = "FrntLeftRdrObj3_UB"
        sig_start_bit = 171
        update_id_bit = 171
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
        startbit = 171
        byte = 21
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class FrntLeftRdrObj3ObjBoxCenterLat:
        sig_name = "FrntLeftRdrObj3ObjBoxCenterLat"
        sig_start_bit = 383
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 383
        byte = 47
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntLeftRdrObj1RdrObjHeightStdDe:
        sig_name = "FrntLeftRdrObj1RdrObjHeightStdDe"
        sig_start_bit = 88
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 88
        bmuws_info = [(11, 0b00000001, 0b11111110, 1, 0), (12, 0b11111111, 0b00000000, 8, 0), (13, 0b10000000, 0b01111111, 1, 7)]

    class FrntLeftRdrObj1RdrObjLifeCycle:
        sig_name = "FrntLeftRdrObj1RdrObjLifeCycle"
        sig_start_bit = 104
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
        startbit = 104
        bmuws_info = [(13, 0b00000001, 0b11111110, 1, 0), (14, 0b11111100, 0b00000011, 6, 2)]


class AcuADCANFDFr12:
    msg_name = "AcuADCANFDFr12"
    msg_id = 1040
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.32
    msg_length = 8
    tx_node = "ACU"
    rx_nodes = ['BGM']
    sig_group_dict = {'ACUActT': ['ACUActTEngT', 'ACUActTEngTQf']}
    sig_group_dataid_dict = {}

    class ACUCoolantFlwReq:
        sig_name = "ACUCoolantFlwReq"
        sig_start_bit = 23
        update_id_bit = 29
        sig_length = 9
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 511
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b10000000, 0b01111111, 1, 7)]

    class ACUActTEngT:
        sig_name = "ACUActTEngT"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -50.0
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Motorola"
        sig_value_init = 50
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ACUActT_UB:
        sig_name = "ACUActT_UB"
        sig_start_bit = 12
        update_id_bit = 12
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
        startbit = 12
        byte = 1
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class ACUActTEngTQf:
        sig_name = "ACUActTEngTQf"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class BgmADCANFDFr02:
    msg_name = "BgmADCANFDFr02"
    msg_id = 320
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.045
    msg_length = 16
    tx_node = "BGM"
    rx_nodes = ['ACU']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class OutsidePrkOutReq:
        sig_name = "OutsidePrkOutReq"
        sig_start_bit = 54
        update_id_bit = 53
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 54
        byte = 6
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class BLEConRPACtrlRear:
        sig_name = "BLEConRPACtrlRear"
        sig_start_bit = 47
        update_id_bit = 40
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoRequest': 0, 'Touch': 1, 'Release': 2, 'Reserved': 3}
        compute_method = None
        length = 3
        startbit = 47
        byte = 5
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class BLEConRPACtrlLeft:
        sig_name = "BLEConRPACtrlLeft"
        sig_start_bit = 35
        update_id_bit = 41
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoRequest': 0, 'Touch': 1, 'Release': 2, 'Reserved': 3}
        compute_method = None
        length = 3
        startbit = 35
        byte = 4
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class RRDRMWorkModeFB:
        sig_name = "RRDRMWorkModeFB"
        sig_start_bit = 75
        update_id_bit = 72
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'No_Request': 0, 'Sentry_Mode': 1, 'AVP_Mode': 2, 'Reserved_3': 3, 'Reserved_4': 4, 'Reserved_5': 5, 'Reserved_6': 6, 'Reserved_7': 7}
        compute_method = None
        length = 3
        startbit = 75
        byte = 9
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class BLEConRPACtrlFrnt:
        sig_name = "BLEConRPACtrlFrnt"
        sig_start_bit = 38
        update_id_bit = 32
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoRequest': 0, 'Touch': 1, 'Release': 2, 'Reserved': 3}
        compute_method = None
        length = 3
        startbit = 38
        byte = 4
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class RLDRMWorkModeFB:
        sig_name = "RLDRMWorkModeFB"
        sig_start_bit = 79
        update_id_bit = 76
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'No_Request': 0, 'Sentry_Mode': 1, 'AVP_Mode': 2, 'Reserved_3': 3, 'Reserved_4': 4, 'Reserved_5': 5, 'Reserved_6': 6, 'Reserved_7': 7}
        compute_method = None
        length = 3
        startbit = 79
        byte = 9
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class BLEConRPACtrlRgt:
        sig_name = "BLEConRPACtrlRgt"
        sig_start_bit = 44
        update_id_bit = 55
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoRequest': 0, 'Touch': 1, 'Release': 2, 'Reserved': 3}
        compute_method = None
        length = 3
        startbit = 44
        byte = 5
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class FLDRMWorkModeFB:
        sig_name = "FLDRMWorkModeFB"
        sig_start_bit = 71
        update_id_bit = 68
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'No_Request': 0, 'Sentry_Mode': 1, 'AVP_Mode': 2, 'Reserved_3': 3, 'Reserved_4': 4, 'Reserved_5': 5, 'Reserved_6': 6, 'Reserved_7': 7}
        compute_method = None
        length = 3
        startbit = 71
        byte = 8
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DrvModSet:
        sig_name = "DrvModSet"
        sig_start_bit = 52
        update_id_bit = 48
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
        startbit = 52
        byte = 6
        mask = 0b00011110
        unmask = 0b11100001
        shift = 1

    class IgnRlyFb:
        sig_name = "IgnRlyFb"
        sig_start_bit = 63
        update_id_bit = 62
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
        startbit = 63
        byte = 7
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class FRDRMWorkModeFB:
        sig_name = "FRDRMWorkModeFB"
        sig_start_bit = 67
        update_id_bit = 64
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'No_Request': 0, 'Sentry_Mode': 1, 'AVP_Mode': 2, 'Reserved_3': 3, 'Reserved_4': 4, 'Reserved_5': 5, 'Reserved_6': 6, 'Reserved_7': 7}
        compute_method = None
        length = 3
        startbit = 67
        byte = 8
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1


