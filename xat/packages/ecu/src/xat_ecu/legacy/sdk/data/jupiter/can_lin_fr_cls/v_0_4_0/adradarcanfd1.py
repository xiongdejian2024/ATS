class SODLADRadarCANFD1Fr01:
    msg_name = "SODLADRadarCANFD1Fr01"
    msg_id = 256
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "SODL"
    rx_nodes = ['ADSOCFSI']
    sig_group_dict = {'ReSideRdrLeDent3': ['ReSideRdrLeDent3RdrDetnChks', 'ReSideRdrLeDent3RdrDetnCntr', 'ReSideRdrLeDent3RdrDetnDynProp', 'ReSideRdrLeDent3RdrDetnElevn', 'ReSideRdrLeDent3RdrDetnID', 'ReSideRdrLeDent3RdrDetnLocationValid', 'ReSideRdrLeDent3RdrDetnPwr', 'ReSideRdrLeDent3RdrDetnRng', 'ReSideRdrLeDent3RdrDetnRngV', 'ReSideRdrLeDent3RdrDetnSNR'], 'ReSideRdrLeDent5': ['ReSideRdrLeDent5RdrDetnChks', 'ReSideRdrLeDent5RdrDetnCntr', 'ReSideRdrLeDent5RdrDetnDynProp', 'ReSideRdrLeDent5RdrDetnElevn', 'ReSideRdrLeDent5RdrDetnID', 'ReSideRdrLeDent5RdrDetnLocationValid', 'ReSideRdrLeDent5RdrDetnPwr', 'ReSideRdrLeDent5RdrDetnRng', 'ReSideRdrLeDent5RdrDetnRngV', 'ReSideRdrLeDent5RdrDetnSNR'], 'ReSideRdrLeDent4': ['ReSideRdrLeDent4RdrDetnChks', 'ReSideRdrLeDent4RdrDetnCntr', 'ReSideRdrLeDent4RdrDetnDynProp', 'ReSideRdrLeDent4RdrDetnElevn', 'ReSideRdrLeDent4RdrDetnID', 'ReSideRdrLeDent4RdrDetnLocationValid', 'ReSideRdrLeDent4RdrDetnPwr', 'ReSideRdrLeDent4RdrDetnRng', 'ReSideRdrLeDent4RdrDetnRngV', 'ReSideRdrLeDent4RdrDetnSNR'], 'ReSideRdrLeDent0': ['ReSideRdrLeDent0RdrDetnChks', 'ReSideRdrLeDent0RdrDetnCntr', 'ReSideRdrLeDent0RdrDetnDynProp', 'ReSideRdrLeDent0RdrDetnElevn', 'ReSideRdrLeDent0RdrDetnID', 'ReSideRdrLeDent0RdrDetnLocationValid', 'ReSideRdrLeDent0RdrDetnPwr', 'ReSideRdrLeDent0RdrDetnRng', 'ReSideRdrLeDent0RdrDetnRngV', 'ReSideRdrLeDent0RdrDetnSNR'], 'ReSideRdrLeDent2': ['ReSideRdrLeDent2RdrDetnChks', 'ReSideRdrLeDent2RdrDetnCntr', 'ReSideRdrLeDent2RdrDetnDynProp', 'ReSideRdrLeDent2RdrDetnElevn', 'ReSideRdrLeDent2RdrDetnID', 'ReSideRdrLeDent2RdrDetnLocationValid', 'ReSideRdrLeDent2RdrDetnPwr', 'ReSideRdrLeDent2RdrDetnRng', 'ReSideRdrLeDent2RdrDetnRngV', 'ReSideRdrLeDent2RdrDetnSNR'], 'ReSideRdrLeDent1': ['ReSideRdrLeDent1RdrDetnChks', 'ReSideRdrLeDent1RdrDetnCntr', 'ReSideRdrLeDent1RdrDetnDynProp', 'ReSideRdrLeDent1RdrDetnElevn', 'ReSideRdrLeDent1RdrDetnID', 'ReSideRdrLeDent1RdrDetnLocationValid', 'ReSideRdrLeDent1RdrDetnPwr', 'ReSideRdrLeDent1RdrDetnRng', 'ReSideRdrLeDent1RdrDetnRngV', 'ReSideRdrLeDent1RdrDetnSNR']}
    sig_group_dataid_dict = {}

    class ReSideRdrLeDent5RdrDetnSNR:
        sig_name = "ReSideRdrLeDent5RdrDetnSNR"
        sig_start_bit = 391
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 0.5
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 127
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 391
        byte = 48
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class ReSideRdrLeDent3_UB:
        sig_name = "ReSideRdrLeDent3_UB"
        sig_start_bit = 396
        update_id_bit = 396
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
        startbit = 396
        byte = 49
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class ReSideRdrLeDent0RdrDetnRng:
        sig_name = "ReSideRdrLeDent0RdrDetnRng"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0.4
        sig_value_min = 0
        sig_value_max = 2996
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11110000, 0b00001111, 4, 4)]

    class ReSideRdrLeDent4RdrDetnID:
        sig_name = "ReSideRdrLeDent4RdrDetnID"
        sig_start_bit = 295
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 295
        byte = 36
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ReSideRdrLeDent0RdrDetnID:
        sig_name = "ReSideRdrLeDent0RdrDetnID"
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

    class ReSideRdrLeDent4RdrDetnElevn:
        sig_name = "ReSideRdrLeDent4RdrDetnElevn"
        sig_start_bit = 287
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.0039
        sig_value_offset = -0.5
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 128
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 287
        byte = 35
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ReSideRdrLeDent1RdrDetnCntr:
        sig_name = "ReSideRdrLeDent1RdrDetnCntr"
        sig_start_bit = 107
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
        startbit = 107
        byte = 13
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class ReSideRdrLeDent5RdrDetnChks:
        sig_name = "ReSideRdrLeDent5RdrDetnChks"
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

    class ReSideRdrLeDent5RdrDetnPwr:
        sig_name = "ReSideRdrLeDent5RdrDetnPwr"
        sig_start_bit = 380
        update_id_bit = None
        sig_length = 5
        sig_value_factor = 2
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Motorola"
        sig_value_init = 30
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 380
        byte = 47
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class ReSideRdrLeDent3RdrDetnPwr:
        sig_name = "ReSideRdrLeDent3RdrDetnPwr"
        sig_start_bit = 263
        update_id_bit = None
        sig_length = 5
        sig_value_factor = 2
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Motorola"
        sig_value_init = 30
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 263
        byte = 32
        mask = 0b11111000
        unmask = 0b00000111
        shift = 3

    class ReSideRdrLeDent1RdrDetnElevn:
        sig_name = "ReSideRdrLeDent1RdrDetnElevn"
        sig_start_bit = 87
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.0039
        sig_value_offset = -0.5
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 128
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 87
        byte = 10
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ReSideRdrLeDent4RdrDetnPwr:
        sig_name = "ReSideRdrLeDent4RdrDetnPwr"
        sig_start_bit = 327
        update_id_bit = None
        sig_length = 5
        sig_value_factor = 2
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Motorola"
        sig_value_init = 30
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 327
        byte = 40
        mask = 0b11111000
        unmask = 0b00000111
        shift = 3

    class ReSideRdrLeDent3RdrDetnRngV:
        sig_name = "ReSideRdrLeDent3RdrDetnRngV"
        sig_start_bit = 234
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -111.1
        sig_value_min = 0
        sig_value_max = 1667
        sig_byteorder = "Motorola"
        sig_value_init = 1111
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 234
        bmuws_info = [(29, 0b00000111, 0b11111000, 3, 0), (30, 0b11111111, 0b00000000, 8, 0)]

    class ReSideRdrLeDent2RdrDetnRng:
        sig_name = "ReSideRdrLeDent2RdrDetnRng"
        sig_start_bit = 167
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0.4
        sig_value_min = 0
        sig_value_max = 2996
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 167
        bmuws_info = [(20, 0b11111111, 0b00000000, 8, 0), (21, 0b11110000, 0b00001111, 4, 4)]

    class ReSideRdrLeDent3RdrDetnCntr:
        sig_name = "ReSideRdrLeDent3RdrDetnCntr"
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

    class ReSideRdrLeDent1RdrDetnRng:
        sig_name = "ReSideRdrLeDent1RdrDetnRng"
        sig_start_bit = 103
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0.4
        sig_value_min = 0
        sig_value_max = 2996
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 103
        bmuws_info = [(12, 0b11111111, 0b00000000, 8, 0), (13, 0b11110000, 0b00001111, 4, 4)]

    class ReSideRdrLeDent2RdrDetnPwr:
        sig_name = "ReSideRdrLeDent2RdrDetnPwr"
        sig_start_bit = 133
        update_id_bit = None
        sig_length = 5
        sig_value_factor = 2
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Motorola"
        sig_value_init = 30
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 133
        byte = 16
        mask = 0b00111110
        unmask = 0b11000001
        shift = 1

    class ReSideRdrLeDent3RdrDetnDynProp:
        sig_name = "ReSideRdrLeDent3RdrDetnDynProp"
        sig_start_bit = 248
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'RdrDetnDynProp_Stationary': 0, 'RdrDetnDynProp_Moving': 1}
        compute_method = None
        length = 1
        startbit = 248
        byte = 31
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ReSideRdrLeDent4RdrDetnSNR:
        sig_name = "ReSideRdrLeDent4RdrDetnSNR"
        sig_start_bit = 319
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 0.5
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 127
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 319
        byte = 39
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class ReSideRdrLeDent5RdrDetnDynProp:
        sig_name = "ReSideRdrLeDent5RdrDetnDynProp"
        sig_start_bit = 384
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'RdrDetnDynProp_Stationary': 0, 'RdrDetnDynProp_Moving': 1}
        compute_method = None
        length = 1
        startbit = 384
        byte = 48
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ReSideRdrLeDent1RdrDetnChks:
        sig_name = "ReSideRdrLeDent1RdrDetnChks"
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

    class ReSideRdrLeDent0RdrDetnPwr:
        sig_name = "ReSideRdrLeDent0RdrDetnPwr"
        sig_start_bit = 52
        update_id_bit = None
        sig_length = 5
        sig_value_factor = 2
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Motorola"
        sig_value_init = 30
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 52
        byte = 6
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class ReSideRdrLeDent1RdrDetnLocationValid:
        sig_name = "ReSideRdrLeDent1RdrDetnLocationValid"
        sig_start_bit = 134
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Validity2_Valid': 0, 'Validity2_Invalid': 1}
        compute_method = None
        length = 1
        startbit = 134
        byte = 16
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class ReSideRdrLeDent2RdrDetnRngV:
        sig_name = "ReSideRdrLeDent2RdrDetnRngV"
        sig_start_bit = 191
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -111.1
        sig_value_min = 0
        sig_value_max = 1667
        sig_byteorder = "Motorola"
        sig_value_init = 1111
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 191
        bmuws_info = [(23, 0b11111111, 0b00000000, 8, 0), (24, 0b11100000, 0b00011111, 3, 5)]

    class ReSideRdrLeDent2RdrDetnID:
        sig_name = "ReSideRdrLeDent2RdrDetnID"
        sig_start_bit = 159
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 159
        byte = 19
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ReSideRdrLeDent5RdrDetnLocationValid:
        sig_name = "ReSideRdrLeDent5RdrDetnLocationValid"
        sig_start_bit = 320
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Validity2_Valid': 0, 'Validity2_Invalid': 1}
        compute_method = None
        length = 1
        startbit = 320
        byte = 40
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ReSideRdrLeDent2RdrDetnDynProp:
        sig_name = "ReSideRdrLeDent2RdrDetnDynProp"
        sig_start_bit = 128
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'RdrDetnDynProp_Stationary': 0, 'RdrDetnDynProp_Moving': 1}
        compute_method = None
        length = 1
        startbit = 128
        byte = 16
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ReSideRdrLeDent5_UB:
        sig_name = "ReSideRdrLeDent5_UB"
        sig_start_bit = 394
        update_id_bit = 394
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
        startbit = 394
        byte = 49
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class ReSideRdrLeDent3RdrDetnChks:
        sig_name = "ReSideRdrLeDent3RdrDetnChks"
        sig_start_bit = 207
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
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

    class ReSideRdrLeDent0RdrDetnDynProp:
        sig_name = "ReSideRdrLeDent0RdrDetnDynProp"
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
        sig_value_table = {'RdrDetnDynProp_Stationary': 0, 'RdrDetnDynProp_Moving': 1}
        compute_method = None
        length = 1
        startbit = 56
        byte = 7
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ReSideRdrLeDent3RdrDetnLocationValid:
        sig_name = "ReSideRdrLeDent3RdrDetnLocationValid"
        sig_start_bit = 235
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Validity2_Valid': 0, 'Validity2_Invalid': 1}
        compute_method = None
        length = 1
        startbit = 235
        byte = 29
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class ReSideRdrLeDent4RdrDetnCntr:
        sig_name = "ReSideRdrLeDent4RdrDetnCntr"
        sig_start_bit = 307
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
        startbit = 307
        byte = 38
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class ReSideRdrLeDent5RdrDetnRng:
        sig_name = "ReSideRdrLeDent5RdrDetnRng"
        sig_start_bit = 359
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0.4
        sig_value_min = 0
        sig_value_max = 2996
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 359
        bmuws_info = [(44, 0b11111111, 0b00000000, 8, 0), (45, 0b11110000, 0b00001111, 4, 4)]

    class ReSideRdrLeDent4_UB:
        sig_name = "ReSideRdrLeDent4_UB"
        sig_start_bit = 395
        update_id_bit = 395
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
        startbit = 395
        byte = 49
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class ReSideRdrLeDent0RdrDetnChks:
        sig_name = "ReSideRdrLeDent0RdrDetnChks"
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

    class ReSideRdrLeDent0RdrDetnElevn:
        sig_name = "ReSideRdrLeDent0RdrDetnElevn"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.0039
        sig_value_offset = -0.5
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 128
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ReSideRdrLeDent1RdrDetnID:
        sig_name = "ReSideRdrLeDent1RdrDetnID"
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

    class ReSideRdrLeDent1RdrDetnPwr:
        sig_name = "ReSideRdrLeDent1RdrDetnPwr"
        sig_start_bit = 124
        update_id_bit = None
        sig_length = 5
        sig_value_factor = 2
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Motorola"
        sig_value_init = 30
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 124
        byte = 15
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class ReSideRdrLeDent4RdrDetnDynProp:
        sig_name = "ReSideRdrLeDent4RdrDetnDynProp"
        sig_start_bit = 312
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'RdrDetnDynProp_Stationary': 0, 'RdrDetnDynProp_Moving': 1}
        compute_method = None
        length = 1
        startbit = 312
        byte = 39
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ReSideRdrLeDent0RdrDetnCntr:
        sig_name = "ReSideRdrLeDent0RdrDetnCntr"
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

    class ReSideRdrLeDent3RdrDetnSNR:
        sig_name = "ReSideRdrLeDent3RdrDetnSNR"
        sig_start_bit = 255
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 0.5
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 127
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 255
        byte = 31
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class ReSideRdrLeDent2RdrDetnSNR:
        sig_name = "ReSideRdrLeDent2RdrDetnSNR"
        sig_start_bit = 183
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 0.5
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 127
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 183
        byte = 22
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class ReSideRdrLeDent5RdrDetnCntr:
        sig_name = "ReSideRdrLeDent5RdrDetnCntr"
        sig_start_bit = 363
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
        startbit = 363
        byte = 45
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class ReSideRdrLeDent1RdrDetnDynProp:
        sig_name = "ReSideRdrLeDent1RdrDetnDynProp"
        sig_start_bit = 135
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'RdrDetnDynProp_Stationary': 0, 'RdrDetnDynProp_Moving': 1}
        compute_method = None
        length = 1
        startbit = 135
        byte = 16
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ReSideRdrLeDent0_UB:
        sig_name = "ReSideRdrLeDent0_UB"
        sig_start_bit = 399
        update_id_bit = 399
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
        startbit = 399
        byte = 49
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ReSideRdrLeDent2RdrDetnElevn:
        sig_name = "ReSideRdrLeDent2RdrDetnElevn"
        sig_start_bit = 151
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.0039
        sig_value_offset = -0.5
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 128
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 151
        byte = 18
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ReSideRdrLeDent4RdrDetnRng:
        sig_name = "ReSideRdrLeDent4RdrDetnRng"
        sig_start_bit = 303
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0.4
        sig_value_min = 0
        sig_value_max = 2996
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 303
        bmuws_info = [(37, 0b11111111, 0b00000000, 8, 0), (38, 0b11110000, 0b00001111, 4, 4)]

    class ReSideRdrLeDent0RdrDetnLocationValid:
        sig_name = "ReSideRdrLeDent0RdrDetnLocationValid"
        sig_start_bit = 71
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Validity2_Valid': 0, 'Validity2_Invalid': 1}
        compute_method = None
        length = 1
        startbit = 71
        byte = 8
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ReSideRdrLeDent4RdrDetnRngV:
        sig_name = "ReSideRdrLeDent4RdrDetnRngV"
        sig_start_bit = 258
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -111.1
        sig_value_min = 0
        sig_value_max = 1667
        sig_byteorder = "Motorola"
        sig_value_init = 1111
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 258
        bmuws_info = [(32, 0b00000111, 0b11111000, 3, 0), (33, 0b11111111, 0b00000000, 8, 0)]

    class ReSideRdrLeDent2RdrDetnChks:
        sig_name = "ReSideRdrLeDent2RdrDetnChks"
        sig_start_bit = 143
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 143
        byte = 17
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ReSideRdrLeDent1RdrDetnRngV:
        sig_name = "ReSideRdrLeDent1RdrDetnRngV"
        sig_start_bit = 119
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -111.1
        sig_value_min = 0
        sig_value_max = 1667
        sig_byteorder = "Motorola"
        sig_value_init = 1111
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 119
        bmuws_info = [(14, 0b11111111, 0b00000000, 8, 0), (15, 0b11100000, 0b00011111, 3, 5)]

    class ReSideRdrLeDent5RdrDetnElevn:
        sig_name = "ReSideRdrLeDent5RdrDetnElevn"
        sig_start_bit = 343
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.0039
        sig_value_offset = -0.5
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 128
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 343
        byte = 42
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ReSideRdrLeDent5RdrDetnRngV:
        sig_name = "ReSideRdrLeDent5RdrDetnRngV"
        sig_start_bit = 375
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -111.1
        sig_value_min = 0
        sig_value_max = 1667
        sig_byteorder = "Motorola"
        sig_value_init = 1111
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 375
        bmuws_info = [(46, 0b11111111, 0b00000000, 8, 0), (47, 0b11100000, 0b00011111, 3, 5)]

    class ReSideRdrLeDent0RdrDetnRngV:
        sig_name = "ReSideRdrLeDent0RdrDetnRngV"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -111.1
        sig_value_min = 0
        sig_value_max = 1667
        sig_byteorder = "Motorola"
        sig_value_init = 1111
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11100000, 0b00011111, 3, 5)]

    class ReSideRdrLeDent2_UB:
        sig_name = "ReSideRdrLeDent2_UB"
        sig_start_bit = 397
        update_id_bit = 397
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
        startbit = 397
        byte = 49
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class ReSideRdrLeDent2RdrDetnLocationValid:
        sig_name = "ReSideRdrLeDent2RdrDetnLocationValid"
        sig_start_bit = 176
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Validity2_Valid': 0, 'Validity2_Invalid': 1}
        compute_method = None
        length = 1
        startbit = 176
        byte = 22
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ReSideRdrLeDent5RdrDetnID:
        sig_name = "ReSideRdrLeDent5RdrDetnID"
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

    class ReSideRdrLeDent4RdrDetnChks:
        sig_name = "ReSideRdrLeDent4RdrDetnChks"
        sig_start_bit = 279
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 279
        byte = 34
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ReSideRdrLeDent1RdrDetnSNR:
        sig_name = "ReSideRdrLeDent1RdrDetnSNR"
        sig_start_bit = 70
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 0.5
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 127
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 70
        byte = 8
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class ReSideRdrLeDent3RdrDetnElevn:
        sig_name = "ReSideRdrLeDent3RdrDetnElevn"
        sig_start_bit = 215
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.0039
        sig_value_offset = -0.5
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 128
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 215
        byte = 26
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ReSideRdrLeDent3RdrDetnID:
        sig_name = "ReSideRdrLeDent3RdrDetnID"
        sig_start_bit = 223
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
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

    class ReSideRdrLeDent0RdrDetnSNR:
        sig_name = "ReSideRdrLeDent0RdrDetnSNR"
        sig_start_bit = 63
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 0.5
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 127
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 63
        byte = 7
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class ReSideRdrLeDent3RdrDetnRng:
        sig_name = "ReSideRdrLeDent3RdrDetnRng"
        sig_start_bit = 231
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0.4
        sig_value_min = 0
        sig_value_max = 2996
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 231
        bmuws_info = [(28, 0b11111111, 0b00000000, 8, 0), (29, 0b11110000, 0b00001111, 4, 4)]

    class ReSideRdrLeDent2RdrDetnCntr:
        sig_name = "ReSideRdrLeDent2RdrDetnCntr"
        sig_start_bit = 171
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
        startbit = 171
        byte = 21
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class ReSideRdrLeDent1_UB:
        sig_name = "ReSideRdrLeDent1_UB"
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

    class ReSideRdrLeDent4RdrDetnLocationValid:
        sig_name = "ReSideRdrLeDent4RdrDetnLocationValid"
        sig_start_bit = 322
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Validity2_Valid': 0, 'Validity2_Invalid': 1}
        compute_method = None
        length = 1
        startbit = 322
        byte = 40
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2


class SODLADRadarCANFD1Fr03:
    msg_name = "SODLADRadarCANFD1Fr03"
    msg_id = 4
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 64
    tx_node = "SODL"
    rx_nodes = ['ADSOCFSI']
    sig_group_dict = {'ReSideRdrLeSts': ['ReSideRdrLeStsChks', 'ReSideRdrLeStsCntr', 'ReSideRdrLeStsRdrStsCalibrationSts', 'ReSideRdrLeStsRdrStsDetnValid', 'ReSideRdrLeStsRdrStsDstbc', 'ReSideRdrLeStsRdrStsEolHoriAg', 'ReSideRdrLeStsRdrStsEolVerAg', 'ReSideRdrLeStsRdrStsFailureHighTemp', 'ReSideRdrLeStsRdrStsFailureNVM', 'ReSideRdrLeStsRdrStsFailureTemperature', 'ReSideRdrLeStsRdrStsFailureVoltage', 'ReSideRdrLeStsRdrStsFaulty', 'ReSideRdrLeStsRdrStsLastTimeLeap', 'ReSideRdrLeStsRdrStsMaxTimeLeap', 'ReSideRdrLeStsRdrStsMissCom', 'ReSideRdrLeStsRdrStsOnlineHoriAg', 'ReSideRdrLeStsRdrStsOnlineVerAg', 'ReSideRdrLeStsRdrStsOperationMode']}
    sig_group_dataid_dict = {'ReSideRdrLeSts': 1020}

    class ReSideRdrLeStsRdrStsMaxTimeLeap:
        sig_name = "ReSideRdrLeStsRdrStsMaxTimeLeap"
        sig_start_bit = 19
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.0001
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 19
        bmuws_info = [(2, 0b00001111, 0b11110000, 4, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class ReSideRdrLeStsRdrStsDstbc:
        sig_name = "ReSideRdrLeStsRdrStsDstbc"
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
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 57
        byte = 7
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class ReSideRdrLeStsRdrStsFaulty:
        sig_name = "ReSideRdrLeStsRdrStsFaulty"
        sig_start_bit = 93
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
        startbit = 93
        byte = 11
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class ReSideRdrLeStsRdrStsEolVerAg:
        sig_name = "ReSideRdrLeStsRdrStsEolVerAg"
        sig_start_bit = 71
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = -5.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 500
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 71
        bmuws_info = [(8, 0b11111111, 0b00000000, 8, 0), (9, 0b11000000, 0b00111111, 2, 6)]

    class ReSideRdrLeStsRdrStsOnlineHoriAg:
        sig_name = "ReSideRdrLeStsRdrStsOnlineHoriAg"
        sig_start_bit = 55
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -10.0
        sig_value_min = 0
        sig_value_max = 2000
        sig_byteorder = "Motorola"
        sig_value_init = 1000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 55
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b11100000, 0b00011111, 3, 5)]

    class ReSideRdrLeStsRdrStsFailureHighTemp:
        sig_name = "ReSideRdrLeStsRdrStsFailureHighTemp"
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
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 56
        byte = 7
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ReSideRdrLeStsRdrStsMissCom:
        sig_name = "ReSideRdrLeStsRdrStsMissCom"
        sig_start_bit = 92
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
        startbit = 92
        byte = 11
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class ReSideRdrLeStsRdrStsEolHoriAg:
        sig_name = "ReSideRdrLeStsRdrStsEolHoriAg"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -10.0
        sig_value_min = 0
        sig_value_max = 2000
        sig_byteorder = "Motorola"
        sig_value_init = 1000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11100000, 0b00011111, 3, 5)]

    class ReSideRdrLeStsRdrStsFailureNVM:
        sig_name = "ReSideRdrLeStsRdrStsFailureNVM"
        sig_start_bit = 74
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 74
        byte = 9
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class ReSideRdrLeStsRdrStsOperationMode:
        sig_name = "ReSideRdrLeStsRdrStsOperationMode"
        sig_start_bit = 77
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OperationMode_Reserved1': 0, 'OperationMode_Init': 1, 'OperationMode_Normal': 2, 'OperationMode_Degraded': 3, 'OperationMode_Blocked': 4}
        compute_method = None
        length = 3
        startbit = 77
        byte = 9
        mask = 0b00111000
        unmask = 0b11000111
        shift = 3

    class ReSideRdrLeStsRdrStsFailureVoltage:
        sig_name = "ReSideRdrLeStsRdrStsFailureVoltage"
        sig_start_bit = 94
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 94
        byte = 11
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class ReSideRdrLeStsRdrStsCalibrationSts:
        sig_name = "ReSideRdrLeStsRdrStsCalibrationSts"
        sig_start_bit = 60
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'RdrStsCalibrationSts_Unknown': 0, 'RdrStsCalibrationSts_Calibrated': 1, 'RdrStsCalibrationSts_SensorMisalignmentDetected': 2, 'RdrStsCalibrationSts_CalibrationInProcess': 3, 'RdrStsCalibrationSts_NotCalibrated': 4, 'RdrStsCalibrationSts_Reserved1': 5, 'RdrStsCalibrationSts_Reserved2': 6, 'RdrStsCalibrationSts_Reserved3': 7}
        compute_method = None
        length = 3
        startbit = 60
        byte = 7
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class ReSideRdrLeStsCntr:
        sig_name = "ReSideRdrLeStsCntr"
        sig_start_bit = 44
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
        startbit = 44
        byte = 5
        mask = 0b00011110
        unmask = 0b11100001
        shift = 1

    class ReSideRdrLeStsRdrStsOnlineVerAg:
        sig_name = "ReSideRdrLeStsRdrStsOnlineVerAg"
        sig_start_bit = 73
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = -5.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 500
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 73
        bmuws_info = [(9, 0b00000011, 0b11111100, 2, 0), (10, 0b11111111, 0b00000000, 8, 0)]

    class ReSideRdrLeStsRdrStsDetnValid:
        sig_name = "ReSideRdrLeStsRdrStsDetnValid"
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
        sig_value_table = {'Validity2_Valid': 0, 'Validity2_Invalid': 1}
        compute_method = None
        length = 1
        startbit = 40
        byte = 5
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ReSideRdrLeStsChks:
        sig_name = "ReSideRdrLeStsChks"
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

    class ReSideRdrLeStsRdrStsLastTimeLeap:
        sig_name = "ReSideRdrLeStsRdrStsLastTimeLeap"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.0001
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 15
        bmuws_info = [(1, 0b11111111, 0b00000000, 8, 0), (2, 0b11110000, 0b00001111, 4, 4)]

    class ReSideRdrLeStsRdrStsFailureTemperature:
        sig_name = "ReSideRdrLeStsRdrStsFailureTemperature"
        sig_start_bit = 95
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 95
        byte = 11
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ReSideRdrLeSts_UB:
        sig_name = "ReSideRdrLeSts_UB"
        sig_start_bit = 91
        update_id_bit = 91
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
        startbit = 91
        byte = 11
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3


class ADSOCFSIADRadarCANFD1TimeSynchFr01:
    msg_name = "ADSOCFSIADRadarCANFD1TimeSynchFr01"
    msg_id = 1
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "ADSOCFSI"
    rx_nodes = ['SODL']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class ADSOCFSIADRadarCANFD1NmFr:
    msg_name = "ADSOCFSIADRadarCANFD1NmFr"
    msg_id = 1281
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "ADSOCFSI"
    rx_nodes = ['SODL']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class SODLADRadarCANFD1Fr02:
    msg_name = "SODLADRadarCANFD1Fr02"
    msg_id = 257
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "SODL"
    rx_nodes = ['ADSOCFSI']
    sig_group_dict = {'ReSideRdrLeDent9': ['ReSideRdrLeDent9RdrDetnChks', 'ReSideRdrLeDent9RdrDetnCntr', 'ReSideRdrLeDent9RdrDetnDynProp', 'ReSideRdrLeDent9RdrDetnElevn', 'ReSideRdrLeDent9RdrDetnID', 'ReSideRdrLeDent9RdrDetnLocationValid', 'ReSideRdrLeDent9RdrDetnPwr', 'ReSideRdrLeDent9RdrDetnRng', 'ReSideRdrLeDent9RdrDetnRngV', 'ReSideRdrLeDent9RdrDetnSNR'], 'ReSideRdrLeDent7': ['ReSideRdrLeDent7RdrDetnChks', 'ReSideRdrLeDent7RdrDetnCntr', 'ReSideRdrLeDent7RdrDetnDynProp', 'ReSideRdrLeDent7RdrDetnElevn', 'ReSideRdrLeDent7RdrDetnID', 'ReSideRdrLeDent7RdrDetnLocationValid', 'ReSideRdrLeDent7RdrDetnPwr', 'ReSideRdrLeDent7RdrDetnRng', 'ReSideRdrLeDent7RdrDetnRngV', 'ReSideRdrLeDent7RdrDetnSNR'], 'ReSideRdrLeDent8': ['ReSideRdrLeDent8RdrDetnChks', 'ReSideRdrLeDent8RdrDetnCntr', 'ReSideRdrLeDent8RdrDetnDynProp', 'ReSideRdrLeDent8RdrDetnElevn', 'ReSideRdrLeDent8RdrDetnID', 'ReSideRdrLeDent8RdrDetnLocationValid', 'ReSideRdrLeDent8RdrDetnPwr', 'ReSideRdrLeDent8RdrDetnRng', 'ReSideRdrLeDent8RdrDetnRngV', 'ReSideRdrLeDent8RdrDetnSNR'], 'ReSideRdrLeDent6': ['ReSideRdrLeDent6RdrDetnChks', 'ReSideRdrLeDent6RdrDetnCntr', 'ReSideRdrLeDent6RdrDetnDynProp', 'ReSideRdrLeDent6RdrDetnElevn', 'ReSideRdrLeDent6RdrDetnID', 'ReSideRdrLeDent6RdrDetnLocationValid', 'ReSideRdrLeDent6RdrDetnPwr', 'ReSideRdrLeDent6RdrDetnRng', 'ReSideRdrLeDent6RdrDetnRngV', 'ReSideRdrLeDent6RdrDetnSNR'], 'ReSideRdrLeDent10': ['ReSideRdrLeDent10RdrDetnChks', 'ReSideRdrLeDent10RdrDetnCntr', 'ReSideRdrLeDent10RdrDetnDynProp', 'ReSideRdrLeDent10RdrDetnElevn', 'ReSideRdrLeDent10RdrDetnID', 'ReSideRdrLeDent10RdrDetnLocationValid', 'ReSideRdrLeDent10RdrDetnPwr', 'ReSideRdrLeDent10RdrDetnRng', 'ReSideRdrLeDent10RdrDetnRngV', 'ReSideRdrLeDent10RdrDetnSNR']}
    sig_group_dataid_dict = {}

    class ReSideRdrLeDent6RdrDetnPwr:
        sig_name = "ReSideRdrLeDent6RdrDetnPwr"
        sig_start_bit = 124
        update_id_bit = None
        sig_length = 5
        sig_value_factor = 2
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Motorola"
        sig_value_init = 30
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 124
        byte = 15
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class ReSideRdrLeDent7RdrDetnID:
        sig_name = "ReSideRdrLeDent7RdrDetnID"
        sig_start_bit = 159
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 159
        byte = 19
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ReSideRdrLeDent7RdrDetnElevn:
        sig_name = "ReSideRdrLeDent7RdrDetnElevn"
        sig_start_bit = 151
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.0039
        sig_value_offset = -0.5
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 128
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 151
        byte = 18
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ReSideRdrLeDent9_UB:
        sig_name = "ReSideRdrLeDent9_UB"
        sig_start_bit = 330
        update_id_bit = 330
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
        startbit = 330
        byte = 41
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class ReSideRdrLeDent6RdrDetnElevn:
        sig_name = "ReSideRdrLeDent6RdrDetnElevn"
        sig_start_bit = 87
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.0039
        sig_value_offset = -0.5
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 128
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 87
        byte = 10
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ReSideRdrLeDent7_UB:
        sig_name = "ReSideRdrLeDent7_UB"
        sig_start_bit = 332
        update_id_bit = 332
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
        startbit = 332
        byte = 41
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class ReSideRdrLeDent9RdrDetnSNR:
        sig_name = "ReSideRdrLeDent9RdrDetnSNR"
        sig_start_bit = 327
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 0.5
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 127
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 327
        byte = 40
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class ReSideRdrLeDent7RdrDetnLocationValid:
        sig_name = "ReSideRdrLeDent7RdrDetnLocationValid"
        sig_start_bit = 188
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Validity2_Valid': 0, 'Validity2_Invalid': 1}
        compute_method = None
        length = 1
        startbit = 188
        byte = 23
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class ReSideRdrLeDent7RdrDetnDynProp:
        sig_name = "ReSideRdrLeDent7RdrDetnDynProp"
        sig_start_bit = 128
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'RdrDetnDynProp_Stationary': 0, 'RdrDetnDynProp_Moving': 1}
        compute_method = None
        length = 1
        startbit = 128
        byte = 16
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ReSideRdrLeDent6RdrDetnRngV:
        sig_name = "ReSideRdrLeDent6RdrDetnRngV"
        sig_start_bit = 119
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -111.1
        sig_value_min = 0
        sig_value_max = 1667
        sig_byteorder = "Motorola"
        sig_value_init = 1111
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 119
        bmuws_info = [(14, 0b11111111, 0b00000000, 8, 0), (15, 0b11100000, 0b00011111, 3, 5)]

    class ReSideRdrLeDent8RdrDetnRng:
        sig_name = "ReSideRdrLeDent8RdrDetnRng"
        sig_start_bit = 231
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0.4
        sig_value_min = 0
        sig_value_max = 2996
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 231
        bmuws_info = [(28, 0b11111111, 0b00000000, 8, 0), (29, 0b11110000, 0b00001111, 4, 4)]

    class ReSideRdrLeDent8RdrDetnLocationValid:
        sig_name = "ReSideRdrLeDent8RdrDetnLocationValid"
        sig_start_bit = 256
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Validity2_Valid': 0, 'Validity2_Invalid': 1}
        compute_method = None
        length = 1
        startbit = 256
        byte = 32
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ReSideRdrLeDent8RdrDetnDynProp:
        sig_name = "ReSideRdrLeDent8RdrDetnDynProp"
        sig_start_bit = 192
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'RdrDetnDynProp_Stationary': 0, 'RdrDetnDynProp_Moving': 1}
        compute_method = None
        length = 1
        startbit = 192
        byte = 24
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ReSideRdrLeDent8RdrDetnChks:
        sig_name = "ReSideRdrLeDent8RdrDetnChks"
        sig_start_bit = 207
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
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

    class ReSideRdrLeDent8_UB:
        sig_name = "ReSideRdrLeDent8_UB"
        sig_start_bit = 331
        update_id_bit = 331
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
        startbit = 331
        byte = 41
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class ReSideRdrLeDent8RdrDetnRngV:
        sig_name = "ReSideRdrLeDent8RdrDetnRngV"
        sig_start_bit = 247
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -111.1
        sig_value_min = 0
        sig_value_max = 1667
        sig_byteorder = "Motorola"
        sig_value_init = 1111
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 247
        bmuws_info = [(30, 0b11111111, 0b00000000, 8, 0), (31, 0b11100000, 0b00011111, 3, 5)]

    class ReSideRdrLeDent10RdrDetnID:
        sig_name = "ReSideRdrLeDent10RdrDetnID"
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

    class ReSideRdrLeDent6RdrDetnSNR:
        sig_name = "ReSideRdrLeDent6RdrDetnSNR"
        sig_start_bit = 70
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 0.5
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 127
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 70
        byte = 8
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class ReSideRdrLeDent9RdrDetnElevn:
        sig_name = "ReSideRdrLeDent9RdrDetnElevn"
        sig_start_bit = 279
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.0039
        sig_value_offset = -0.5
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 128
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 279
        byte = 34
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ReSideRdrLeDent8RdrDetnSNR:
        sig_name = "ReSideRdrLeDent8RdrDetnSNR"
        sig_start_bit = 263
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 0.5
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 127
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 263
        byte = 32
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class ReSideRdrLeDent9RdrDetnCntr:
        sig_name = "ReSideRdrLeDent9RdrDetnCntr"
        sig_start_bit = 299
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
        startbit = 299
        byte = 37
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class ReSideRdrLeDent8RdrDetnID:
        sig_name = "ReSideRdrLeDent8RdrDetnID"
        sig_start_bit = 223
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
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

    class ReSideRdrLeDent10RdrDetnDynProp:
        sig_name = "ReSideRdrLeDent10RdrDetnDynProp"
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
        sig_value_table = {'RdrDetnDynProp_Stationary': 0, 'RdrDetnDynProp_Moving': 1}
        compute_method = None
        length = 1
        startbit = 56
        byte = 7
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ReSideRdrLeDent10RdrDetnCntr:
        sig_name = "ReSideRdrLeDent10RdrDetnCntr"
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

    class ReSideRdrLeDent10RdrDetnRngV:
        sig_name = "ReSideRdrLeDent10RdrDetnRngV"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -111.1
        sig_value_min = 0
        sig_value_max = 1667
        sig_byteorder = "Motorola"
        sig_value_init = 1111
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11100000, 0b00011111, 3, 5)]

    class ReSideRdrLeDent7RdrDetnPwr:
        sig_name = "ReSideRdrLeDent7RdrDetnPwr"
        sig_start_bit = 133
        update_id_bit = None
        sig_length = 5
        sig_value_factor = 2
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Motorola"
        sig_value_init = 30
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 133
        byte = 16
        mask = 0b00111110
        unmask = 0b11000001
        shift = 1

    class ReSideRdrLeDent6RdrDetnLocationValid:
        sig_name = "ReSideRdrLeDent6RdrDetnLocationValid"
        sig_start_bit = 134
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Validity2_Valid': 0, 'Validity2_Invalid': 1}
        compute_method = None
        length = 1
        startbit = 134
        byte = 16
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class ReSideRdrLeDent7RdrDetnRngV:
        sig_name = "ReSideRdrLeDent7RdrDetnRngV"
        sig_start_bit = 183
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -111.1
        sig_value_min = 0
        sig_value_max = 1667
        sig_byteorder = "Motorola"
        sig_value_init = 1111
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 183
        bmuws_info = [(22, 0b11111111, 0b00000000, 8, 0), (23, 0b11100000, 0b00011111, 3, 5)]

    class ReSideRdrLeDent9RdrDetnChks:
        sig_name = "ReSideRdrLeDent9RdrDetnChks"
        sig_start_bit = 271
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 271
        byte = 33
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ReSideRdrLeDent7RdrDetnChks:
        sig_name = "ReSideRdrLeDent7RdrDetnChks"
        sig_start_bit = 143
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 143
        byte = 17
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ReSideRdrLeDent6RdrDetnRng:
        sig_name = "ReSideRdrLeDent6RdrDetnRng"
        sig_start_bit = 103
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0.4
        sig_value_min = 0
        sig_value_max = 2996
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 103
        bmuws_info = [(12, 0b11111111, 0b00000000, 8, 0), (13, 0b11110000, 0b00001111, 4, 4)]

    class ReSideRdrLeDent9RdrDetnDynProp:
        sig_name = "ReSideRdrLeDent9RdrDetnDynProp"
        sig_start_bit = 320
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'RdrDetnDynProp_Stationary': 0, 'RdrDetnDynProp_Moving': 1}
        compute_method = None
        length = 1
        startbit = 320
        byte = 40
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ReSideRdrLeDent10RdrDetnRng:
        sig_name = "ReSideRdrLeDent10RdrDetnRng"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0.4
        sig_value_min = 0
        sig_value_max = 2996
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11110000, 0b00001111, 4, 4)]

    class ReSideRdrLeDent6_UB:
        sig_name = "ReSideRdrLeDent6_UB"
        sig_start_bit = 333
        update_id_bit = 333
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
        startbit = 333
        byte = 41
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class ReSideRdrLeDent10RdrDetnElevn:
        sig_name = "ReSideRdrLeDent10RdrDetnElevn"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.0039
        sig_value_offset = -0.5
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 128
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ReSideRdrLeDent10RdrDetnPwr:
        sig_name = "ReSideRdrLeDent10RdrDetnPwr"
        sig_start_bit = 52
        update_id_bit = None
        sig_length = 5
        sig_value_factor = 2
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Motorola"
        sig_value_init = 30
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 52
        byte = 6
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class ReSideRdrLeDent9RdrDetnLocationValid:
        sig_name = "ReSideRdrLeDent9RdrDetnLocationValid"
        sig_start_bit = 335
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Validity2_Valid': 0, 'Validity2_Invalid': 1}
        compute_method = None
        length = 1
        startbit = 335
        byte = 41
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ReSideRdrLeDent8RdrDetnCntr:
        sig_name = "ReSideRdrLeDent8RdrDetnCntr"
        sig_start_bit = 235
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
        startbit = 235
        byte = 29
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class ReSideRdrLeDent10RdrDetnChks:
        sig_name = "ReSideRdrLeDent10RdrDetnChks"
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

    class ReSideRdrLeDent10RdrDetnLocationValid:
        sig_name = "ReSideRdrLeDent10RdrDetnLocationValid"
        sig_start_bit = 71
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Validity2_Valid': 0, 'Validity2_Invalid': 1}
        compute_method = None
        length = 1
        startbit = 71
        byte = 8
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ReSideRdrLeDent10_UB:
        sig_name = "ReSideRdrLeDent10_UB"
        sig_start_bit = 334
        update_id_bit = 334
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
        startbit = 334
        byte = 41
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class ReSideRdrLeDent6RdrDetnCntr:
        sig_name = "ReSideRdrLeDent6RdrDetnCntr"
        sig_start_bit = 107
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
        startbit = 107
        byte = 13
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class ReSideRdrLeDent6RdrDetnID:
        sig_name = "ReSideRdrLeDent6RdrDetnID"
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

    class ReSideRdrLeDent8RdrDetnPwr:
        sig_name = "ReSideRdrLeDent8RdrDetnPwr"
        sig_start_bit = 252
        update_id_bit = None
        sig_length = 5
        sig_value_factor = 2
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Motorola"
        sig_value_init = 30
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 252
        byte = 31
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class ReSideRdrLeDent6RdrDetnDynProp:
        sig_name = "ReSideRdrLeDent6RdrDetnDynProp"
        sig_start_bit = 135
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'RdrDetnDynProp_Stationary': 0, 'RdrDetnDynProp_Moving': 1}
        compute_method = None
        length = 1
        startbit = 135
        byte = 16
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ReSideRdrLeDent7RdrDetnRng:
        sig_name = "ReSideRdrLeDent7RdrDetnRng"
        sig_start_bit = 167
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0.4
        sig_value_min = 0
        sig_value_max = 2996
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 167
        bmuws_info = [(20, 0b11111111, 0b00000000, 8, 0), (21, 0b11110000, 0b00001111, 4, 4)]

    class ReSideRdrLeDent6RdrDetnChks:
        sig_name = "ReSideRdrLeDent6RdrDetnChks"
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

    class ReSideRdrLeDent9RdrDetnRng:
        sig_name = "ReSideRdrLeDent9RdrDetnRng"
        sig_start_bit = 295
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0.4
        sig_value_min = 0
        sig_value_max = 2996
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 295
        bmuws_info = [(36, 0b11111111, 0b00000000, 8, 0), (37, 0b11110000, 0b00001111, 4, 4)]

    class ReSideRdrLeDent10RdrDetnSNR:
        sig_name = "ReSideRdrLeDent10RdrDetnSNR"
        sig_start_bit = 63
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 0.5
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 127
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 63
        byte = 7
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class ReSideRdrLeDent8RdrDetnElevn:
        sig_name = "ReSideRdrLeDent8RdrDetnElevn"
        sig_start_bit = 215
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.0039
        sig_value_offset = -0.5
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 128
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 215
        byte = 26
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ReSideRdrLeDent9RdrDetnRngV:
        sig_name = "ReSideRdrLeDent9RdrDetnRngV"
        sig_start_bit = 311
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -111.1
        sig_value_min = 0
        sig_value_max = 1667
        sig_byteorder = "Motorola"
        sig_value_init = 1111
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 311
        bmuws_info = [(38, 0b11111111, 0b00000000, 8, 0), (39, 0b11100000, 0b00011111, 3, 5)]

    class ReSideRdrLeDent9RdrDetnID:
        sig_name = "ReSideRdrLeDent9RdrDetnID"
        sig_start_bit = 287
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 287
        byte = 35
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ReSideRdrLeDent7RdrDetnSNR:
        sig_name = "ReSideRdrLeDent7RdrDetnSNR"
        sig_start_bit = 199
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 0.5
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 127
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 199
        byte = 24
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class ReSideRdrLeDent7RdrDetnCntr:
        sig_name = "ReSideRdrLeDent7RdrDetnCntr"
        sig_start_bit = 171
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
        startbit = 171
        byte = 21
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class ReSideRdrLeDent9RdrDetnPwr:
        sig_name = "ReSideRdrLeDent9RdrDetnPwr"
        sig_start_bit = 316
        update_id_bit = None
        sig_length = 5
        sig_value_factor = 2
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Motorola"
        sig_value_init = 30
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 316
        byte = 39
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0


class SODLADRadarCANFD1NmFr:
    msg_name = "SODLADRadarCANFD1NmFr"
    msg_id = 1283
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "SODL"
    rx_nodes = ['ADSOCFSI']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


