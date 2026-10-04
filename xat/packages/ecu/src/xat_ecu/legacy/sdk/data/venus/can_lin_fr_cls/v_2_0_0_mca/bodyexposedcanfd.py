class BgmToHcmlBodyExpoDiagReqFrame:
    msg_name = "BgmToHcmlBodyExpoDiagReqFrame"
    msg_id = 1971
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCML']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class BgmBodyExposedCANFr01:
    msg_name = "BgmBodyExposedCANFr01"
    msg_id = 368
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.03
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCML', 'RCMM', 'HCMR']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class ActnOfLedAddLoBeam:
        sig_name = "ActnOfLedAddLoBeam"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ActnOfLedStopLampMid:
        sig_name = "ActnOfLedStopLampMid"
        sig_start_bit = 5
        update_id_bit = 4
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
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5


class BgmToRcmrBodyExpoDiagReqFrame:
    msg_name = "BgmToRcmrBodyExpoDiagReqFrame"
    msg_id = 1974
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RCMR']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class BgmBodyExposedCANFr03:
    msg_name = "BgmBodyExposedCANFr03"
    msg_id = 147
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 64
    tx_node = "BGM"
    rx_nodes = ['HCML']
    sig_group_dict = {'CrossFrntX1': ['CrossFrntX1Y1', 'CrossFrntX1Y10', 'CrossFrntX1Y11', 'CrossFrntX1Y12', 'CrossFrntX1Y13', 'CrossFrntX1Y14', 'CrossFrntX1Y15', 'CrossFrntX1Y16', 'CrossFrntX1Y17', 'CrossFrntX1Y18', 'CrossFrntX1Y19', 'CrossFrntX1Y2', 'CrossFrntX1Y20', 'CrossFrntX1Y21', 'CrossFrntX1Y22', 'CrossFrntX1Y23', 'CrossFrntX1Y24', 'CrossFrntX1Y25', 'CrossFrntX1Y26', 'CrossFrntX1Y27', 'CrossFrntX1Y28', 'CrossFrntX1Y29', 'CrossFrntX1Y3', 'CrossFrntX1Y30', 'CrossFrntX1Y31', 'CrossFrntX1Y32', 'CrossFrntX1Y33', 'CrossFrntX1Y34', 'CrossFrntX1Y35', 'CrossFrntX1Y36', 'CrossFrntX1Y37', 'CrossFrntX1Y38', 'CrossFrntX1Y39', 'CrossFrntX1Y4', 'CrossFrntX1Y40', 'CrossFrntX1Y41', 'CrossFrntX1Y42', 'CrossFrntX1Y43', 'CrossFrntX1Y44', 'CrossFrntX1Y45', 'CrossFrntX1Y46', 'CrossFrntX1Y47', 'CrossFrntX1Y48', 'CrossFrntX1Y49', 'CrossFrntX1Y5', 'CrossFrntX1Y50', 'CrossFrntX1Y51', 'CrossFrntX1Y52', 'CrossFrntX1Y53', 'CrossFrntX1Y54', 'CrossFrntX1Y55', 'CrossFrntX1Y56', 'CrossFrntX1Y57', 'CrossFrntX1Y58', 'CrossFrntX1Y59', 'CrossFrntX1Y6', 'CrossFrntX1Y60', 'CrossFrntX1Y61', 'CrossFrntX1Y62', 'CrossFrntX1Y63', 'CrossFrntX1Y64', 'CrossFrntX1Y65', 'CrossFrntX1Y66', 'CrossFrntX1Y67', 'CrossFrntX1Y68', 'CrossFrntX1Y69', 'CrossFrntX1Y7', 'CrossFrntX1Y70', 'CrossFrntX1Y8', 'CrossFrntX1Y9']}
    sig_group_dataid_dict = {}

    class CrossFrntX1Y68:
        sig_name = "CrossFrntX1Y68"
        sig_start_bit = 466
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 466
        bmuws_info = [(58, 0b00000111, 0b11111000, 3, 0), (59, 0b11110000, 0b00001111, 4, 4)]

    class CrossFrntX1Y67:
        sig_name = "CrossFrntX1Y67"
        sig_start_bit = 457
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 457
        bmuws_info = [(57, 0b00000011, 0b11111100, 2, 0), (58, 0b11111000, 0b00000111, 5, 3)]

    class CrossFrntX1Y29:
        sig_name = "CrossFrntX1Y29"
        sig_start_bit = 195
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 195
        bmuws_info = [(24, 0b00001111, 0b11110000, 4, 0), (25, 0b11100000, 0b00011111, 3, 5)]

    class CrossFrntX1Y66:
        sig_name = "CrossFrntX1Y66"
        sig_start_bit = 448
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 448
        bmuws_info = [(56, 0b00000001, 0b11111110, 1, 0), (57, 0b11111100, 0b00000011, 6, 2)]

    class CrossFrntX1Y14:
        sig_name = "CrossFrntX1Y14"
        sig_start_bit = 92
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 92
        bmuws_info = [(11, 0b00011111, 0b11100000, 5, 0), (12, 0b11000000, 0b00111111, 2, 6)]

    class CrossFrntX1Y16:
        sig_name = "CrossFrntX1Y16"
        sig_start_bit = 110
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 110
        byte = 13
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossFrntX1Y57:
        sig_name = "CrossFrntX1Y57"
        sig_start_bit = 399
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 399
        byte = 49
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class CrossFrntX1Y24:
        sig_name = "CrossFrntX1Y24"
        sig_start_bit = 166
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 166
        byte = 20
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossFrntX1Y34:
        sig_name = "CrossFrntX1Y34"
        sig_start_bit = 224
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 224
        bmuws_info = [(28, 0b00000001, 0b11111110, 1, 0), (29, 0b11111100, 0b00000011, 6, 2)]

    class CrossFrntX1Y13:
        sig_name = "CrossFrntX1Y13"
        sig_start_bit = 83
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 83
        bmuws_info = [(10, 0b00001111, 0b11110000, 4, 0), (11, 0b11100000, 0b00011111, 3, 5)]

    class CrossFrntX1Y8:
        sig_name = "CrossFrntX1Y8"
        sig_start_bit = 54
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 54
        byte = 6
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossFrntX1Y46:
        sig_name = "CrossFrntX1Y46"
        sig_start_bit = 316
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 316
        bmuws_info = [(39, 0b00011111, 0b11100000, 5, 0), (40, 0b11000000, 0b00111111, 2, 6)]

    class CrossFrntX1Y69:
        sig_name = "CrossFrntX1Y69"
        sig_start_bit = 475
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 475
        bmuws_info = [(59, 0b00001111, 0b11110000, 4, 0), (60, 0b11100000, 0b00011111, 3, 5)]

    class CrossFrntX1Y62:
        sig_name = "CrossFrntX1Y62"
        sig_start_bit = 428
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 428
        bmuws_info = [(53, 0b00011111, 0b11100000, 5, 0), (54, 0b11000000, 0b00111111, 2, 6)]

    class CrossFrntX1Y28:
        sig_name = "CrossFrntX1Y28"
        sig_start_bit = 186
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 186
        bmuws_info = [(23, 0b00000111, 0b11111000, 3, 0), (24, 0b11110000, 0b00001111, 4, 4)]

    class CrossFrntX1Y15:
        sig_name = "CrossFrntX1Y15"
        sig_start_bit = 101
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 101
        bmuws_info = [(12, 0b00111111, 0b11000000, 6, 0), (13, 0b10000000, 0b01111111, 1, 7)]

    class CrossFrntX1Y5:
        sig_name = "CrossFrntX1Y5"
        sig_start_bit = 27
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 27
        bmuws_info = [(3, 0b00001111, 0b11110000, 4, 0), (4, 0b11100000, 0b00011111, 3, 5)]

    class CrossFrntX1Y19:
        sig_name = "CrossFrntX1Y19"
        sig_start_bit = 121
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 121
        bmuws_info = [(15, 0b00000011, 0b11111100, 2, 0), (16, 0b11111000, 0b00000111, 5, 3)]

    class CrossFrntX1Y42:
        sig_name = "CrossFrntX1Y42"
        sig_start_bit = 280
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 280
        bmuws_info = [(35, 0b00000001, 0b11111110, 1, 0), (36, 0b11111100, 0b00000011, 6, 2)]

    class CrossFrntX1Y20:
        sig_name = "CrossFrntX1Y20"
        sig_start_bit = 130
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 130
        bmuws_info = [(16, 0b00000111, 0b11111000, 3, 0), (17, 0b11110000, 0b00001111, 4, 4)]

    class CrossFrntX1Y11:
        sig_name = "CrossFrntX1Y11"
        sig_start_bit = 65
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 65
        bmuws_info = [(8, 0b00000011, 0b11111100, 2, 0), (9, 0b11111000, 0b00000111, 5, 3)]

    class CrossFrntX1Y12:
        sig_name = "CrossFrntX1Y12"
        sig_start_bit = 74
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 74
        bmuws_info = [(9, 0b00000111, 0b11111000, 3, 0), (10, 0b11110000, 0b00001111, 4, 4)]

    class CrossFrntX1Y6:
        sig_name = "CrossFrntX1Y6"
        sig_start_bit = 36
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 36
        bmuws_info = [(4, 0b00011111, 0b11100000, 5, 0), (5, 0b11000000, 0b00111111, 2, 6)]

    class CrossFrntX1Y18:
        sig_name = "CrossFrntX1Y18"
        sig_start_bit = 112
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 112
        bmuws_info = [(14, 0b00000001, 0b11111110, 1, 0), (15, 0b11111100, 0b00000011, 6, 2)]

    class CrossFrntX1Y55:
        sig_name = "CrossFrntX1Y55"
        sig_start_bit = 381
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 381
        bmuws_info = [(47, 0b00111111, 0b11000000, 6, 0), (48, 0b10000000, 0b01111111, 1, 7)]

    class CrossFrntX1Y35:
        sig_name = "CrossFrntX1Y35"
        sig_start_bit = 233
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 233
        bmuws_info = [(29, 0b00000011, 0b11111100, 2, 0), (30, 0b11111000, 0b00000111, 5, 3)]

    class CrossFrntX1Y4:
        sig_name = "CrossFrntX1Y4"
        sig_start_bit = 18
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 18
        bmuws_info = [(2, 0b00000111, 0b11111000, 3, 0), (3, 0b11110000, 0b00001111, 4, 4)]

    class CrossFrntX1Y27:
        sig_name = "CrossFrntX1Y27"
        sig_start_bit = 177
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 177
        bmuws_info = [(22, 0b00000011, 0b11111100, 2, 0), (23, 0b11111000, 0b00000111, 5, 3)]

    class CrossFrntX1Y63:
        sig_name = "CrossFrntX1Y63"
        sig_start_bit = 437
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 437
        bmuws_info = [(54, 0b00111111, 0b11000000, 6, 0), (55, 0b10000000, 0b01111111, 1, 7)]

    class CrossFrntX1Y25:
        sig_name = "CrossFrntX1Y25"
        sig_start_bit = 175
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 175
        byte = 21
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class CrossFrntX1Y50:
        sig_name = "CrossFrntX1Y50"
        sig_start_bit = 336
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 336
        bmuws_info = [(42, 0b00000001, 0b11111110, 1, 0), (43, 0b11111100, 0b00000011, 6, 2)]

    class CrossFrntX1Y47:
        sig_name = "CrossFrntX1Y47"
        sig_start_bit = 325
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 325
        bmuws_info = [(40, 0b00111111, 0b11000000, 6, 0), (41, 0b10000000, 0b01111111, 1, 7)]

    class CrossFrntX1Y61:
        sig_name = "CrossFrntX1Y61"
        sig_start_bit = 419
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 419
        bmuws_info = [(52, 0b00001111, 0b11110000, 4, 0), (53, 0b11100000, 0b00011111, 3, 5)]

    class CrossFrntX1Y36:
        sig_name = "CrossFrntX1Y36"
        sig_start_bit = 242
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 242
        bmuws_info = [(30, 0b00000111, 0b11111000, 3, 0), (31, 0b11110000, 0b00001111, 4, 4)]

    class CrossFrntX1Y54:
        sig_name = "CrossFrntX1Y54"
        sig_start_bit = 372
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 372
        bmuws_info = [(46, 0b00011111, 0b11100000, 5, 0), (47, 0b11000000, 0b00111111, 2, 6)]

    class CrossFrntX1Y44:
        sig_name = "CrossFrntX1Y44"
        sig_start_bit = 298
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 298
        bmuws_info = [(37, 0b00000111, 0b11111000, 3, 0), (38, 0b11110000, 0b00001111, 4, 4)]

    class CrossFrntX1Y56:
        sig_name = "CrossFrntX1Y56"
        sig_start_bit = 390
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 390
        byte = 48
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossFrntX1Y7:
        sig_name = "CrossFrntX1Y7"
        sig_start_bit = 45
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 45
        bmuws_info = [(5, 0b00111111, 0b11000000, 6, 0), (6, 0b10000000, 0b01111111, 1, 7)]

    class CrossFrntX1Y9:
        sig_name = "CrossFrntX1Y9"
        sig_start_bit = 63
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
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

    class CrossFrntX1Y23:
        sig_name = "CrossFrntX1Y23"
        sig_start_bit = 157
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 157
        bmuws_info = [(19, 0b00111111, 0b11000000, 6, 0), (20, 0b10000000, 0b01111111, 1, 7)]

    class CrossFrntX1Y41:
        sig_name = "CrossFrntX1Y41"
        sig_start_bit = 287
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 287
        byte = 35
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class CrossFrntX1Y52:
        sig_name = "CrossFrntX1Y52"
        sig_start_bit = 354
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 354
        bmuws_info = [(44, 0b00000111, 0b11111000, 3, 0), (45, 0b11110000, 0b00001111, 4, 4)]

    class CrossFrntX1Y49:
        sig_name = "CrossFrntX1Y49"
        sig_start_bit = 343
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 343
        byte = 42
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class CrossFrntX1Y30:
        sig_name = "CrossFrntX1Y30"
        sig_start_bit = 204
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 204
        bmuws_info = [(25, 0b00011111, 0b11100000, 5, 0), (26, 0b11000000, 0b00111111, 2, 6)]

    class CrossFrntX1Y43:
        sig_name = "CrossFrntX1Y43"
        sig_start_bit = 289
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 289
        bmuws_info = [(36, 0b00000011, 0b11111100, 2, 0), (37, 0b11111000, 0b00000111, 5, 3)]

    class CrossFrntX1Y48:
        sig_name = "CrossFrntX1Y48"
        sig_start_bit = 334
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 334
        byte = 41
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossFrntX1Y39:
        sig_name = "CrossFrntX1Y39"
        sig_start_bit = 269
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 269
        bmuws_info = [(33, 0b00111111, 0b11000000, 6, 0), (34, 0b10000000, 0b01111111, 1, 7)]

    class CrossFrntX1Y60:
        sig_name = "CrossFrntX1Y60"
        sig_start_bit = 410
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 410
        bmuws_info = [(51, 0b00000111, 0b11111000, 3, 0), (52, 0b11110000, 0b00001111, 4, 4)]

    class CrossFrntX1Y10:
        sig_name = "CrossFrntX1Y10"
        sig_start_bit = 56
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 56
        bmuws_info = [(7, 0b00000001, 0b11111110, 1, 0), (8, 0b11111100, 0b00000011, 6, 2)]

    class CrossFrntX1Y45:
        sig_name = "CrossFrntX1Y45"
        sig_start_bit = 307
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 307
        bmuws_info = [(38, 0b00001111, 0b11110000, 4, 0), (39, 0b11100000, 0b00011111, 3, 5)]

    class CrossFrntX1Y22:
        sig_name = "CrossFrntX1Y22"
        sig_start_bit = 148
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 148
        bmuws_info = [(18, 0b00011111, 0b11100000, 5, 0), (19, 0b11000000, 0b00111111, 2, 6)]

    class CrossFrntX1Y2:
        sig_name = "CrossFrntX1Y2"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 0
        bmuws_info = [(0, 0b00000001, 0b11111110, 1, 0), (1, 0b11111100, 0b00000011, 6, 2)]

    class CrossFrntX1Y38:
        sig_name = "CrossFrntX1Y38"
        sig_start_bit = 260
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 260
        bmuws_info = [(32, 0b00011111, 0b11100000, 5, 0), (33, 0b11000000, 0b00111111, 2, 6)]

    class CrossFrntX1Y59:
        sig_name = "CrossFrntX1Y59"
        sig_start_bit = 401
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 401
        bmuws_info = [(50, 0b00000011, 0b11111100, 2, 0), (51, 0b11111000, 0b00000111, 5, 3)]

    class CrossFrntX1Y58:
        sig_name = "CrossFrntX1Y58"
        sig_start_bit = 392
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 392
        bmuws_info = [(49, 0b00000001, 0b11111110, 1, 0), (50, 0b11111100, 0b00000011, 6, 2)]

    class CrossFrntX1Y37:
        sig_name = "CrossFrntX1Y37"
        sig_start_bit = 251
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 251
        bmuws_info = [(31, 0b00001111, 0b11110000, 4, 0), (32, 0b11100000, 0b00011111, 3, 5)]

    class CrossFrntX1Y33:
        sig_name = "CrossFrntX1Y33"
        sig_start_bit = 231
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 231
        byte = 28
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class CrossFrntX1Y1:
        sig_name = "CrossFrntX1Y1"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
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

    class CrossFrntX1Y53:
        sig_name = "CrossFrntX1Y53"
        sig_start_bit = 363
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 363
        bmuws_info = [(45, 0b00001111, 0b11110000, 4, 0), (46, 0b11100000, 0b00011111, 3, 5)]

    class CrossFrntX1_UB:
        sig_name = "CrossFrntX1_UB"
        sig_start_bit = 493
        update_id_bit = 493
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
        startbit = 493
        byte = 61
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class CrossFrntX1Y26:
        sig_name = "CrossFrntX1Y26"
        sig_start_bit = 168
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 168
        bmuws_info = [(21, 0b00000001, 0b11111110, 1, 0), (22, 0b11111100, 0b00000011, 6, 2)]

    class CrossFrntX1Y32:
        sig_name = "CrossFrntX1Y32"
        sig_start_bit = 222
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 222
        byte = 27
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossFrntX1Y21:
        sig_name = "CrossFrntX1Y21"
        sig_start_bit = 139
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 139
        bmuws_info = [(17, 0b00001111, 0b11110000, 4, 0), (18, 0b11100000, 0b00011111, 3, 5)]

    class CrossFrntX1Y64:
        sig_name = "CrossFrntX1Y64"
        sig_start_bit = 446
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 446
        byte = 55
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossFrntX1Y65:
        sig_name = "CrossFrntX1Y65"
        sig_start_bit = 455
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 455
        byte = 56
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class CrossFrntX1Y31:
        sig_name = "CrossFrntX1Y31"
        sig_start_bit = 213
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 213
        bmuws_info = [(26, 0b00111111, 0b11000000, 6, 0), (27, 0b10000000, 0b01111111, 1, 7)]

    class CrossFrntX1Y51:
        sig_name = "CrossFrntX1Y51"
        sig_start_bit = 345
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 345
        bmuws_info = [(43, 0b00000011, 0b11111100, 2, 0), (44, 0b11111000, 0b00000111, 5, 3)]

    class CrossFrntX1Y70:
        sig_name = "CrossFrntX1Y70"
        sig_start_bit = 484
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 484
        bmuws_info = [(60, 0b00011111, 0b11100000, 5, 0), (61, 0b11000000, 0b00111111, 2, 6)]

    class CrossFrntX1Y17:
        sig_name = "CrossFrntX1Y17"
        sig_start_bit = 119
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 119
        byte = 14
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class CrossFrntX1Y3:
        sig_name = "CrossFrntX1Y3"
        sig_start_bit = 9
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 9
        bmuws_info = [(1, 0b00000011, 0b11111100, 2, 0), (2, 0b11111000, 0b00000111, 5, 3)]

    class CrossFrntX1Y40:
        sig_name = "CrossFrntX1Y40"
        sig_start_bit = 278
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 278
        byte = 34
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0


class HcmlBodyExpoFr05:
    msg_name = "HcmlBodyExpoFr05"
    msg_id = 256
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.03
    msg_length = 8
    tx_node = "HCML"
    rx_nodes = ['S2SReceiver', 'BGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class StsOfFrntPosnLampLeScopeStore:
        sig_name = "StsOfFrntPosnLampLeScopeStore"
        sig_start_bit = 7
        update_id_bit = 5
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Sts_Resd': 0, 'Sts_Err': 1, 'Sts_CmplOk': 2, 'Sts_InProgs': 3}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class RcmmBodyExpoFr02:
    msg_name = "RcmmBodyExpoFr02"
    msg_id = 596
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 12
    tx_node = "RCMM"
    rx_nodes = ['S2SReceiver', 'BGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class StsOfRePosnLampMidScopeStore:
        sig_name = "StsOfRePosnLampMidScopeStore"
        sig_start_bit = 70
        update_id_bit = 68
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Sts_Resd': 0, 'Sts_Err': 1, 'Sts_CmplOk': 2, 'Sts_InProgs': 3}
        compute_method = None
        length = 2
        startbit = 70
        byte = 8
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class StsOfLedStopLampMid:
        sig_name = "StsOfLedStopLampMid"
        sig_start_bit = 57
        update_id_bit = 71
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 57
        byte = 7
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class StsOfLedReLampMid:
        sig_name = "StsOfLedReLampMid"
        sig_start_bit = 63
        update_id_bit = 61
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 63
        byte = 7
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class StsOfLedPosnLampMid:
        sig_name = "StsOfLedPosnLampMid"
        sig_start_bit = 67
        update_id_bit = 65
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 67
        byte = 8
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class StsOfLedReLampMid1:
        sig_name = "StsOfLedReLampMid1"
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
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 60
        byte = 7
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3


class RcmmBodyExposedCANNmFr:
    msg_name = "RcmmBodyExposedCANNmFr"
    msg_id = 1333
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "RCMM"
    rx_nodes = []
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class RcmlToBgmBodyExpoDiagRespFrame:
    msg_name = "RcmlToBgmBodyExpoDiagRespFrame"
    msg_id = 1717
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "RCML"
    rx_nodes = ['BGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class BgmBodyExposedCANFr04:
    msg_name = "BgmBodyExposedCANFr04"
    msg_id = 148
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 64
    tx_node = "BGM"
    rx_nodes = ['RCML', 'RCMR', 'HCMR', 'HCML']
    sig_group_dict = {'CrossReRiX1': ['CrossReRiX1Y1', 'CrossReRiX1Y10', 'CrossReRiX1Y11', 'CrossReRiX1Y12', 'CrossReRiX1Y13', 'CrossReRiX1Y14', 'CrossReRiX1Y15', 'CrossReRiX1Y16', 'CrossReRiX1Y17', 'CrossReRiX1Y18', 'CrossReRiX1Y19', 'CrossReRiX1Y2', 'CrossReRiX1Y20', 'CrossReRiX1Y3', 'CrossReRiX1Y4', 'CrossReRiX1Y5', 'CrossReRiX1Y6', 'CrossReRiX1Y7', 'CrossReRiX1Y8', 'CrossReRiX1Y9'], 'CrossReLeX1': ['CrossReLeX1Y1', 'CrossReLeX1Y10', 'CrossReLeX1Y11', 'CrossReLeX1Y12', 'CrossReLeX1Y13', 'CrossReLeX1Y14', 'CrossReLeX1Y15', 'CrossReLeX1Y16', 'CrossReLeX1Y17', 'CrossReLeX1Y18', 'CrossReLeX1Y19', 'CrossReLeX1Y2', 'CrossReLeX1Y20', 'CrossReLeX1Y3', 'CrossReLeX1Y4', 'CrossReLeX1Y5', 'CrossReLeX1Y6', 'CrossReLeX1Y7', 'CrossReLeX1Y8', 'CrossReLeX1Y9']}
    sig_group_dataid_dict = {}

    class CrossReLeX1Y1:
        sig_name = "CrossReLeX1Y1"
        sig_start_bit = 6
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 6
        byte = 0
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReLeX1Y18:
        sig_name = "CrossReLeX1Y18"
        sig_start_bit = 142
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 142
        byte = 17
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReRiX1Y16:
        sig_name = "CrossReRiX1Y16"
        sig_start_bit = 294
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 294
        byte = 36
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReLeX1Y13:
        sig_name = "CrossReLeX1Y13"
        sig_start_bit = 102
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 102
        byte = 12
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReLeX1Y9:
        sig_name = "CrossReLeX1Y9"
        sig_start_bit = 70
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
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

    class CrossReRiX1Y3:
        sig_name = "CrossReRiX1Y3"
        sig_start_bit = 198
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 198
        byte = 24
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReLeX1Y4:
        sig_name = "CrossReLeX1Y4"
        sig_start_bit = 30
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 30
        byte = 3
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class LoBeamRi:
        sig_name = "LoBeamRi"
        sig_start_bit = 495
        update_id_bit = 500
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 495
        byte = 61
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class CrossReRiX1Y13:
        sig_name = "CrossReRiX1Y13"
        sig_start_bit = 270
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 270
        byte = 33
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReRiX1Y7:
        sig_name = "CrossReRiX1Y7"
        sig_start_bit = 230
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 230
        byte = 28
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class HiBeamLe:
        sig_name = "HiBeamLe"
        sig_start_bit = 471
        update_id_bit = 503
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 471
        byte = 58
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class CrossReLeX1Y6:
        sig_name = "CrossReLeX1Y6"
        sig_start_bit = 46
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 46
        byte = 5
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class LoBeamLe:
        sig_name = "LoBeamLe"
        sig_start_bit = 487
        update_id_bit = 501
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 487
        byte = 60
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class CrossReRiX1Y20:
        sig_name = "CrossReRiX1Y20"
        sig_start_bit = 326
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 326
        byte = 40
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReLeX1Y14:
        sig_name = "CrossReLeX1Y14"
        sig_start_bit = 110
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 110
        byte = 13
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReRiX1Y11:
        sig_name = "CrossReRiX1Y11"
        sig_start_bit = 254
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 254
        byte = 31
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReLeX1Y20:
        sig_name = "CrossReLeX1Y20"
        sig_start_bit = 158
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 158
        byte = 19
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReRiX1Y14:
        sig_name = "CrossReRiX1Y14"
        sig_start_bit = 278
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 278
        byte = 34
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReLeX1Y3:
        sig_name = "CrossReLeX1Y3"
        sig_start_bit = 22
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 22
        byte = 2
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReRiX1Y1:
        sig_name = "CrossReRiX1Y1"
        sig_start_bit = 174
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 174
        byte = 21
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReLeX1Y5:
        sig_name = "CrossReLeX1Y5"
        sig_start_bit = 38
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 38
        byte = 4
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReLeX1Y11:
        sig_name = "CrossReLeX1Y11"
        sig_start_bit = 86
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 86
        byte = 10
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReRiX1Y18:
        sig_name = "CrossReRiX1Y18"
        sig_start_bit = 310
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 310
        byte = 38
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReRiX1Y8:
        sig_name = "CrossReRiX1Y8"
        sig_start_bit = 238
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 238
        byte = 29
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReRiX1_UB:
        sig_name = "CrossReRiX1_UB"
        sig_start_bit = 328
        update_id_bit = 328
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
        startbit = 328
        byte = 41
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class CrossReLeX1Y8:
        sig_name = "CrossReLeX1Y8"
        sig_start_bit = 62
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 62
        byte = 7
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReLeX1Y2:
        sig_name = "CrossReLeX1Y2"
        sig_start_bit = 14
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 14
        byte = 1
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReLeX1Y17:
        sig_name = "CrossReLeX1Y17"
        sig_start_bit = 134
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 134
        byte = 16
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReLeX1Y10:
        sig_name = "CrossReLeX1Y10"
        sig_start_bit = 78
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 78
        byte = 9
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReRiX1Y12:
        sig_name = "CrossReRiX1Y12"
        sig_start_bit = 262
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 262
        byte = 32
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReLeX1Y15:
        sig_name = "CrossReLeX1Y15"
        sig_start_bit = 118
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 118
        byte = 14
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReRiX1Y10:
        sig_name = "CrossReRiX1Y10"
        sig_start_bit = 182
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 182
        byte = 22
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReRiX1Y4:
        sig_name = "CrossReRiX1Y4"
        sig_start_bit = 206
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 206
        byte = 25
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReRiX1Y6:
        sig_name = "CrossReRiX1Y6"
        sig_start_bit = 222
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 222
        byte = 27
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReLeX1Y12:
        sig_name = "CrossReLeX1Y12"
        sig_start_bit = 94
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 94
        byte = 11
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReRiX1Y2:
        sig_name = "CrossReRiX1Y2"
        sig_start_bit = 190
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 190
        byte = 23
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReLeX1Y19:
        sig_name = "CrossReLeX1Y19"
        sig_start_bit = 150
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 150
        byte = 18
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReLeX1_UB:
        sig_name = "CrossReLeX1_UB"
        sig_start_bit = 160
        update_id_bit = 160
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
        startbit = 160
        byte = 20
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class CrossReRiX1Y5:
        sig_name = "CrossReRiX1Y5"
        sig_start_bit = 214
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 214
        byte = 26
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReRiX1Y9:
        sig_name = "CrossReRiX1Y9"
        sig_start_bit = 246
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 246
        byte = 30
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReLeX1Y7:
        sig_name = "CrossReLeX1Y7"
        sig_start_bit = 54
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 54
        byte = 6
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class HiBeamRi:
        sig_name = "HiBeamRi"
        sig_start_bit = 479
        update_id_bit = 502
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 479
        byte = 59
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class CrossReLeX1Y16:
        sig_name = "CrossReLeX1Y16"
        sig_start_bit = 126
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 126
        byte = 15
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReRiX1Y19:
        sig_name = "CrossReRiX1Y19"
        sig_start_bit = 318
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 318
        byte = 39
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReRiX1Y15:
        sig_name = "CrossReRiX1Y15"
        sig_start_bit = 286
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 286
        byte = 35
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReRiX1Y17:
        sig_name = "CrossReRiX1Y17"
        sig_start_bit = 302
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 302
        byte = 37
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0


class BgmBodyExposedCANFr10:
    msg_name = "BgmBodyExposedCANFr10"
    msg_id = 154
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 64
    tx_node = "BGM"
    rx_nodes = ['RCML', 'RCMR', 'RCMM', 'HCMR', 'HCML']
    sig_group_dict = {'PIXReRiX8': ['PIXReRiX8Y1', 'PIXReRiX8Y2', 'PIXReRiX8Y3', 'PIXReRiX8Y4', 'PIXReRiX8Y5', 'PIXReRiX8Y6'], 'PIXReRiX7': ['PIXReRiX7Y1', 'PIXReRiX7Y2', 'PIXReRiX7Y3', 'PIXReRiX7Y4', 'PIXReRiX7Y5', 'PIXReRiX7Y6'], 'PIXReRiX5': ['PIXReRiX5Y1', 'PIXReRiX5Y2', 'PIXReRiX5Y3', 'PIXReRiX5Y4', 'PIXReRiX5Y5', 'PIXReRiX5Y6'], 'PIXReRiX4': ['PIXReRiX4Y1', 'PIXReRiX4Y2', 'PIXReRiX4Y3', 'PIXReRiX4Y4', 'PIXReRiX4Y5', 'PIXReRiX4Y6'], 'PIXReRiX6': ['PIXReRiX6Y1', 'PIXReRiX6Y2', 'PIXReRiX6Y3', 'PIXReRiX6Y4', 'PIXReRiX6Y5', 'PIXReRiX6Y6'], 'PIXReRiX3': ['PIXReRiX3Y1', 'PIXReRiX3Y2', 'PIXReRiX3Y3', 'PIXReRiX3Y4', 'PIXReRiX3Y5', 'PIXReRiX3Y6'], 'PIXReRiX2': ['PIXReRiX2IsY1Yellow', 'PIXReRiX2IsY2Yellow', 'PIXReRiX2IsY3Yellow', 'PIXReRiX2IsY4Yellow', 'PIXReRiX2IsY5Yellow', 'PIXReRiX2IsY6Yellow', 'PIXReRiX2Y1', 'PIXReRiX2Y2', 'PIXReRiX2Y3', 'PIXReRiX2Y4', 'PIXReRiX2Y5', 'PIXReRiX2Y6'], 'PIXReRiX9': ['PIXReRiX9Y1', 'PIXReRiX9Y2', 'PIXReRiX9Y3', 'PIXReRiX9Y4', 'PIXReRiX9Y5', 'PIXReRiX9Y6'], 'PIXReRiX1': ['PIXReRiX1IsY1Yellow', 'PIXReRiX1IsY2Yellow', 'PIXReRiX1IsY3Yellow', 'PIXReRiX1IsY4Yellow', 'PIXReRiX1IsY5Yellow', 'PIXReRiX1IsY6Yellow', 'PIXReRiX1Y1', 'PIXReRiX1Y2', 'PIXReRiX1Y3', 'PIXReRiX1Y4', 'PIXReRiX1Y5', 'PIXReRiX1Y6']}
    sig_group_dataid_dict = {}

    class PIXReRiX2Y6:
        sig_name = "PIXReRiX2Y6"
        sig_start_bit = 95
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 95
        byte = 11
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXReRiX2Y1:
        sig_name = "PIXReRiX2Y1"
        sig_start_bit = 55
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 55
        byte = 6
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXReRiX5Y1:
        sig_name = "PIXReRiX5Y1"
        sig_start_bit = 179
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 179
        bmuws_info = [(22, 0b00001111, 0b11110000, 4, 0), (23, 0b11100000, 0b00011111, 3, 5)]

    class PIXReRiX3Y3:
        sig_name = "PIXReRiX3Y3"
        sig_start_bit = 105
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 105
        bmuws_info = [(13, 0b00000011, 0b11111100, 2, 0), (14, 0b11111000, 0b00000111, 5, 3)]

    class PIXReRiX8_UB:
        sig_name = "PIXReRiX8_UB"
        sig_start_bit = 408
        update_id_bit = 408
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
        startbit = 408
        byte = 51
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class PIXReRiX7Y4:
        sig_name = "PIXReRiX7Y4"
        sig_start_bit = 295
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 295
        byte = 36
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXReRiX1IsY6Yellow:
        sig_name = "PIXReRiX1IsY6Yellow"
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
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 40
        byte = 5
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class PIXReRiX3Y2:
        sig_name = "PIXReRiX3Y2"
        sig_start_bit = 96
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 96
        bmuws_info = [(12, 0b00000001, 0b11111110, 1, 0), (13, 0b11111100, 0b00000011, 6, 2)]

    class PIXReRiX3Y6:
        sig_name = "PIXReRiX3Y6"
        sig_start_bit = 132
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 132
        bmuws_info = [(16, 0b00011111, 0b11100000, 5, 0), (17, 0b11000000, 0b00111111, 2, 6)]

    class PIXReRiX1Y5:
        sig_name = "PIXReRiX1Y5"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 39
        byte = 4
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXReRiX8Y4:
        sig_name = "PIXReRiX8Y4"
        sig_start_bit = 343
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 343
        byte = 42
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXReRiX7_UB:
        sig_name = "PIXReRiX7_UB"
        sig_start_bit = 409
        update_id_bit = 409
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
        startbit = 409
        byte = 51
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class PIXReRiX5_UB:
        sig_name = "PIXReRiX5_UB"
        sig_start_bit = 411
        update_id_bit = 411
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
        startbit = 411
        byte = 51
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class PIXReRiX4Y5:
        sig_name = "PIXReRiX4Y5"
        sig_start_bit = 161
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 161
        bmuws_info = [(20, 0b00000011, 0b11111100, 2, 0), (21, 0b11111000, 0b00000111, 5, 3)]

    class PIXReRiX4_UB:
        sig_name = "PIXReRiX4_UB"
        sig_start_bit = 412
        update_id_bit = 412
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
        startbit = 412
        byte = 51
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class PIXReRiX2Y3:
        sig_name = "PIXReRiX2Y3"
        sig_start_bit = 71
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 71
        byte = 8
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXReRiX2IsY3Yellow:
        sig_name = "PIXReRiX2IsY3Yellow"
        sig_start_bit = 64
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
        startbit = 64
        byte = 8
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class PIXReRiX7Y3:
        sig_name = "PIXReRiX7Y3"
        sig_start_bit = 287
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 287
        byte = 35
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXReRiX1Y1:
        sig_name = "PIXReRiX1Y1"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
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

    class PIXReRiX8Y5:
        sig_name = "PIXReRiX8Y5"
        sig_start_bit = 351
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 351
        byte = 43
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXReRiX2IsY4Yellow:
        sig_name = "PIXReRiX2IsY4Yellow"
        sig_start_bit = 72
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
        startbit = 72
        byte = 9
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class PIXReRiX4Y1:
        sig_name = "PIXReRiX4Y1"
        sig_start_bit = 141
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 141
        bmuws_info = [(17, 0b00111111, 0b11000000, 6, 0), (18, 0b10000000, 0b01111111, 1, 7)]

    class PIXReRiX6_UB:
        sig_name = "PIXReRiX6_UB"
        sig_start_bit = 410
        update_id_bit = 410
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
        startbit = 410
        byte = 51
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class PIXReRiX2Y5:
        sig_name = "PIXReRiX2Y5"
        sig_start_bit = 87
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 87
        byte = 10
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class SetOfPosnLampScopeReq:
        sig_name = "SetOfPosnLampScopeReq"
        sig_start_bit = 422
        update_id_bit = 418
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
        startbit = 422
        byte = 52
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class PIXReRiX8Y6:
        sig_name = "PIXReRiX8Y6"
        sig_start_bit = 359
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 359
        byte = 44
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class ReFogLe:
        sig_name = "ReFogLe"
        sig_start_bit = 431
        update_id_bit = 424
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 431
        byte = 53
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXReRiX1Y3:
        sig_name = "PIXReRiX1Y3"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 23
        byte = 2
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXReRiX1IsY5Yellow:
        sig_name = "PIXReRiX1IsY5Yellow"
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
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 32
        byte = 4
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class PIXReRiX2IsY1Yellow:
        sig_name = "PIXReRiX2IsY1Yellow"
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
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 48
        byte = 6
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class PIXReRiX7Y6:
        sig_name = "PIXReRiX7Y6"
        sig_start_bit = 311
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 311
        byte = 38
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXReRiX1IsY4Yellow:
        sig_name = "PIXReRiX1IsY4Yellow"
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
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 24
        byte = 3
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class PIXReRiX4Y4:
        sig_name = "PIXReRiX4Y4"
        sig_start_bit = 152
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 152
        bmuws_info = [(19, 0b00000001, 0b11111110, 1, 0), (20, 0b11111100, 0b00000011, 6, 2)]

    class PIXReRiX4Y6:
        sig_name = "PIXReRiX4Y6"
        sig_start_bit = 170
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 170
        bmuws_info = [(21, 0b00000111, 0b11111000, 3, 0), (22, 0b11110000, 0b00001111, 4, 4)]

    class PIXReRiX3_UB:
        sig_name = "PIXReRiX3_UB"
        sig_start_bit = 413
        update_id_bit = 413
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
        startbit = 413
        byte = 51
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class PIXReRiX1Y4:
        sig_name = "PIXReRiX1Y4"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 31
        byte = 3
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class StaticLightingModeEn:
        sig_name = "StaticLightingModeEn"
        sig_start_bit = 420
        update_id_bit = 417
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
        startbit = 420
        byte = 52
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class PIXReRiX2Y4:
        sig_name = "PIXReRiX2Y4"
        sig_start_bit = 79
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 79
        byte = 9
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXReRiX6Y5:
        sig_name = "PIXReRiX6Y5"
        sig_start_bit = 253
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 253
        bmuws_info = [(31, 0b00111111, 0b11000000, 6, 0), (32, 0b10000000, 0b01111111, 1, 7)]

    class PIXReRiX5Y4:
        sig_name = "PIXReRiX5Y4"
        sig_start_bit = 206
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 206
        byte = 25
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class PIXReRiX1IsY3Yellow:
        sig_name = "PIXReRiX1IsY3Yellow"
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
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 16
        byte = 2
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class PIXReRiX9Y6:
        sig_name = "PIXReRiX9Y6"
        sig_start_bit = 407
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 407
        byte = 50
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXReRiX9Y5:
        sig_name = "PIXReRiX9Y5"
        sig_start_bit = 399
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 399
        byte = 49
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXReRiX6Y3:
        sig_name = "PIXReRiX6Y3"
        sig_start_bit = 235
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 235
        bmuws_info = [(29, 0b00001111, 0b11110000, 4, 0), (30, 0b11100000, 0b00011111, 3, 5)]

    class PIXReRiX1IsY2Yellow:
        sig_name = "PIXReRiX1IsY2Yellow"
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
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 8
        byte = 1
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class PIXReRiX5Y3:
        sig_name = "PIXReRiX5Y3"
        sig_start_bit = 197
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 197
        bmuws_info = [(24, 0b00111111, 0b11000000, 6, 0), (25, 0b10000000, 0b01111111, 1, 7)]

    class PIXReRiX2IsY2Yellow:
        sig_name = "PIXReRiX2IsY2Yellow"
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
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 56
        byte = 7
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class PIXReRiX4Y2:
        sig_name = "PIXReRiX4Y2"
        sig_start_bit = 150
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 150
        byte = 18
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class PIXReRiX9Y1:
        sig_name = "PIXReRiX9Y1"
        sig_start_bit = 367
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 367
        byte = 45
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXReRiX9Y4:
        sig_name = "PIXReRiX9Y4"
        sig_start_bit = 391
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
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

    class PIXReRiX2IsY6Yellow:
        sig_name = "PIXReRiX2IsY6Yellow"
        sig_start_bit = 88
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
        startbit = 88
        byte = 11
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class PIXReRiX6Y6:
        sig_name = "PIXReRiX6Y6"
        sig_start_bit = 262
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 262
        byte = 32
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class PIXReRiX6Y4:
        sig_name = "PIXReRiX6Y4"
        sig_start_bit = 244
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 244
        bmuws_info = [(30, 0b00011111, 0b11100000, 5, 0), (31, 0b11000000, 0b00111111, 2, 6)]

    class PIXReRiX2Y2:
        sig_name = "PIXReRiX2Y2"
        sig_start_bit = 63
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
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

    class PIXReRiX8Y3:
        sig_name = "PIXReRiX8Y3"
        sig_start_bit = 335
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 335
        byte = 41
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class ReverseRi:
        sig_name = "ReverseRi"
        sig_start_bit = 439
        update_id_bit = 432
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 439
        byte = 54
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXReRiX6Y2:
        sig_name = "PIXReRiX6Y2"
        sig_start_bit = 226
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 226
        bmuws_info = [(28, 0b00000111, 0b11111000, 3, 0), (29, 0b11110000, 0b00001111, 4, 4)]

    class PIXReRiX7Y2:
        sig_name = "PIXReRiX7Y2"
        sig_start_bit = 279
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 279
        byte = 34
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXReRiX2_UB:
        sig_name = "PIXReRiX2_UB"
        sig_start_bit = 414
        update_id_bit = 414
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
        startbit = 414
        byte = 51
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class PIXReRiX1Y6:
        sig_name = "PIXReRiX1Y6"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 47
        byte = 5
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXReRiX3Y1:
        sig_name = "PIXReRiX3Y1"
        sig_start_bit = 103
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 103
        byte = 12
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXReRiX1IsY1Yellow:
        sig_name = "PIXReRiX1IsY1Yellow"
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
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 0
        byte = 0
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class PIXReRiX9_UB:
        sig_name = "PIXReRiX9_UB"
        sig_start_bit = 423
        update_id_bit = 423
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
        startbit = 423
        byte = 52
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class PIXReRiX1Y2:
        sig_name = "PIXReRiX1Y2"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 15
        byte = 1
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXReRiX3Y5:
        sig_name = "PIXReRiX3Y5"
        sig_start_bit = 123
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 123
        bmuws_info = [(15, 0b00001111, 0b11110000, 4, 0), (16, 0b11100000, 0b00011111, 3, 5)]

    class PIXReRiX5Y5:
        sig_name = "PIXReRiX5Y5"
        sig_start_bit = 215
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 215
        byte = 26
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXReRiX8Y2:
        sig_name = "PIXReRiX8Y2"
        sig_start_bit = 327
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
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

    class PIXReRiX8Y1:
        sig_name = "PIXReRiX8Y1"
        sig_start_bit = 319
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
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

    class PIXReRiX7Y1:
        sig_name = "PIXReRiX7Y1"
        sig_start_bit = 271
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 271
        byte = 33
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXReRiX9Y2:
        sig_name = "PIXReRiX9Y2"
        sig_start_bit = 375
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 375
        byte = 46
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXReRiX9Y3:
        sig_name = "PIXReRiX9Y3"
        sig_start_bit = 383
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 383
        byte = 47
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXReRiX3Y4:
        sig_name = "PIXReRiX3Y4"
        sig_start_bit = 114
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 114
        bmuws_info = [(14, 0b00000111, 0b11111000, 3, 0), (15, 0b11110000, 0b00001111, 4, 4)]

    class PIXReRiX6Y1:
        sig_name = "PIXReRiX6Y1"
        sig_start_bit = 217
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 217
        bmuws_info = [(27, 0b00000011, 0b11111100, 2, 0), (28, 0b11111000, 0b00000111, 5, 3)]

    class PIXReRiX4Y3:
        sig_name = "PIXReRiX4Y3"
        sig_start_bit = 159
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 159
        byte = 19
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXReRiX7Y5:
        sig_name = "PIXReRiX7Y5"
        sig_start_bit = 303
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 303
        byte = 37
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXReRiX5Y6:
        sig_name = "PIXReRiX5Y6"
        sig_start_bit = 208
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 208
        bmuws_info = [(26, 0b00000001, 0b11111110, 1, 0), (27, 0b11111100, 0b00000011, 6, 2)]

    class PIXReRiX1_UB:
        sig_name = "PIXReRiX1_UB"
        sig_start_bit = 415
        update_id_bit = 415
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
        startbit = 415
        byte = 51
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class PIXReRiX2IsY5Yellow:
        sig_name = "PIXReRiX2IsY5Yellow"
        sig_start_bit = 80
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
        startbit = 80
        byte = 10
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class PIXReRiX5Y2:
        sig_name = "PIXReRiX5Y2"
        sig_start_bit = 188
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 188
        bmuws_info = [(23, 0b00011111, 0b11100000, 5, 0), (24, 0b11000000, 0b00111111, 2, 6)]


class RcmmToBgmBodyExpoDiagRespFrame:
    msg_name = "RcmmToBgmBodyExpoDiagRespFrame"
    msg_id = 1719
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "RCMM"
    rx_nodes = ['BGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class RcmrToBgmBodyExpoDiagRespFrame:
    msg_name = "RcmrToBgmBodyExpoDiagRespFrame"
    msg_id = 1718
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "RCMR"
    rx_nodes = ['BGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class RcmlBodyExpoFr01:
    msg_name = "RcmlBodyExpoFr01"
    msg_id = 592
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 8
    tx_node = "RCML"
    rx_nodes = ['S2SReceiver', 'BGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class StsOfLedTurnIndcrLe1:
        sig_name = "StsOfLedTurnIndcrLe1"
        sig_start_bit = 29
        update_id_bit = 31
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 29
        byte = 3
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class StsOfLedRvsgLampLe1:
        sig_name = "StsOfLedRvsgLampLe1"
        sig_start_bit = 15
        update_id_bit = 22
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 15
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class StsOfLedReLampLe1:
        sig_name = "StsOfLedReLampLe1"
        sig_start_bit = 13
        update_id_bit = 23
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 13
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class StsOfLedReFogLampLe1:
        sig_name = "StsOfLedReFogLampLe1"
        sig_start_bit = 11
        update_id_bit = 24
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 11
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class StsOfRePosnLampLeScopeStore:
        sig_name = "StsOfRePosnLampLeScopeStore"
        sig_start_bit = 44
        update_id_bit = 42
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Sts_Resd': 0, 'Sts_Err': 1, 'Sts_CmplOk': 2, 'Sts_InProgs': 3}
        compute_method = None
        length = 2
        startbit = 44
        byte = 5
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class StsOfLedStopLampLe1:
        sig_name = "StsOfLedStopLampLe1"
        sig_start_bit = 21
        update_id_bit = 30
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 21
        byte = 2
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class StsOfLedReLampLe2:
        sig_name = "StsOfLedReLampLe2"
        sig_start_bit = 34
        update_id_bit = 32
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 34
        byte = 4
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class StsOfLedPosnLampLe1:
        sig_name = "StsOfLedPosnLampLe1"
        sig_start_bit = 9
        update_id_bit = 25
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 9
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class StsOfLedReLampLe:
        sig_name = "StsOfLedReLampLe"
        sig_start_bit = 37
        update_id_bit = 35
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 37
        byte = 4
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class StsOfLedReWheelLampLe:
        sig_name = "StsOfLedReWheelLampLe"
        sig_start_bit = 47
        update_id_bit = 45
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 47
        byte = 5
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class HcmrBodyExposedCANNmFr:
    msg_name = "HcmrBodyExposedCANNmFr"
    msg_id = 1330
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "HCMR"
    rx_nodes = ['BGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class CemBodyExpoCommonFr21:
    msg_name = "CemBodyExpoCommonFr21"
    msg_id = 64
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.015
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RCML', 'RCMR', 'RCMM', 'HCMR', 'CCM', 'HCML']
    sig_group_dict = {'VehModMngtGlbSafe1': ['VehModMngtGlbSafe1CarModSts1', 'VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp', 'VehModMngtGlbSafe1Chks', 'VehModMngtGlbSafe1Cntr', 'VehModMngtGlbSafe1EgyLvlElecMai', 'VehModMngtGlbSafe1EgyLvlElecSubtyp', 'VehModMngtGlbSafe1FltEgyCnsWdSts', 'VehModMngtGlbSafe1PwrLvlElecMai', 'VehModMngtGlbSafe1PwrLvlElecSubtyp', 'VehModMngtGlbSafe1UsgModSts']}
    sig_group_dataid_dict = {'VehModMngtGlbSafe1': 116}

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

    class VehModMngtGlbSafe1FltEgyCnsWdSts:
        sig_name = "VehModMngtGlbSafe1FltEgyCnsWdSts"
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
        sig_value_table = {'FltEgyCns1_NoFlt': 0, 'FltEgyCns1_Flt': 1}
        compute_method = None
        length = 1
        startbit = 36
        byte = 4
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp:
        sig_name = "VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp"
        sig_start_bit = 35
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
        startbit = 35
        byte = 4
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

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

    class VehModMngtGlbSafe1PwrLvlElecSubtyp:
        sig_name = "VehModMngtGlbSafe1PwrLvlElecSubtyp"
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

    class VehModMngtGlbSafe1EgyLvlElecSubtyp:
        sig_name = "VehModMngtGlbSafe1EgyLvlElecSubtyp"
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

    class RainLi:
        sig_name = "RainLi"
        sig_start_bit = 47
        update_id_bit = 63
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


class CemBodyExpoCommonFr04:
    msg_name = "CemBodyExpoCommonFr04"
    msg_id = 80
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.04
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RCML', 'RCMR', 'RCMM', 'HCMR', 'HCML']
    sig_group_dict = {'VehSpdLgt': ['VehSpdLgtA', 'VehSpdLgtChks', 'VehSpdLgtCntr', 'VehSpdLgtQf']}
    sig_group_dataid_dict = {'VehSpdLgt': 55}

    class VehSpdLgtCntr:
        sig_name = "VehSpdLgtCntr"
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

    class VehSpdLgtChks:
        sig_name = "VehSpdLgtChks"
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

    class VehSpdLgtA:
        sig_name = "VehSpdLgtA"
        sig_start_bit = 6
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
        startbit = 6
        bmuws_info = [(0, 0b01111111, 0b10000000, 7, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class VehSpdLgtQf:
        sig_name = "VehSpdLgtQf"
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

    class VehSpdLgt_UB:
        sig_name = "VehSpdLgt_UB"
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


class BgmToRcmlBodyExpoDiagReqFrame:
    msg_name = "BgmToRcmlBodyExpoDiagReqFrame"
    msg_id = 1973
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RCML']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class HcmlBodyExpoFr02:
    msg_name = "HcmlBodyExpoFr02"
    msg_id = 593
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 3
    tx_node = "HCML"
    rx_nodes = ['S2SReceiver', 'BGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class StsOfLedLoBeamLe:
        sig_name = "StsOfLedLoBeamLe"
        sig_start_bit = 4
        update_id_bit = 5
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 4
        byte = 0
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class StsOfLedFrntLampLe2:
        sig_name = "StsOfLedFrntLampLe2"
        sig_start_bit = 13
        update_id_bit = 8
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 13
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class StsOfLedHiBeamLe:
        sig_name = "StsOfLedHiBeamLe"
        sig_start_bit = 1
        update_id_bit = 2
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class StsOfLedFrntLampLe1:
        sig_name = "StsOfLedFrntLampLe1"
        sig_start_bit = 15
        update_id_bit = 9
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 15
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class StsOfLedFrntWheelLampLe:
        sig_name = "StsOfLedFrntWheelLampLe"
        sig_start_bit = 22
        update_id_bit = 20
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 22
        byte = 2
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class StsOfLedFrntLampMid1:
        sig_name = "StsOfLedFrntLampMid1"
        sig_start_bit = 11
        update_id_bit = 23
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 11
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2


class HcmrtoEtcXCPFr01:
    msg_name = "HcmrtoEtcXCPFr01"
    msg_id = 1426
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "HCMR"
    rx_nodes = ['CCM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class BgmBodyExposedCANFr02:
    msg_name = "BgmBodyExposedCANFr02"
    msg_id = 146
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 16
    tx_node = "BGM"
    rx_nodes = ['RCML', 'RCMR', 'HCMR', 'HCML']
    sig_group_dict = {'DIDRLFrntRi': ['DIDRLFrntRiBrightness', 'DIDRLFrntRiIsYellow'], 'DrvrDesDir': ['DrvrDesDirChks', 'DrvrDesDirCntr', 'DrvrDesDirDrvrDesDir'], 'DIDRLFrntLe': ['DIDRLFrntLeBrightness', 'DIDRLFrntLeIsYellow']}
    sig_group_dataid_dict = {'DrvrDesDir': 627}

    class WheelLampRearRi:
        sig_name = "WheelLampRearRi"
        sig_start_bit = 79
        update_id_bit = 72
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 79
        byte = 9
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class DIDRLFrntRi_UB:
        sig_name = "DIDRLFrntRi_UB"
        sig_start_bit = 46
        update_id_bit = 46
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
        startbit = 46
        byte = 5
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class DIDRLFrntRiBrightness:
        sig_name = "DIDRLFrntRiBrightness"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 23
        byte = 2
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class DrvrDesDirCntr:
        sig_name = "DrvrDesDirCntr"
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

    class WheelLampFrntLe:
        sig_name = "WheelLampFrntLe"
        sig_start_bit = 55
        update_id_bit = 48
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 55
        byte = 6
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class WheelLampFrntRi:
        sig_name = "WheelLampFrntRi"
        sig_start_bit = 63
        update_id_bit = 56
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
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

    class DrvrDesDir_UB:
        sig_name = "DrvrDesDir_UB"
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

    class ActvnOfLedReWheelLampRi:
        sig_name = "ActvnOfLedReWheelLampRi"
        sig_start_bit = 4
        update_id_bit = 0
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
        startbit = 4
        byte = 0
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class DIDRLFrntLe_UB:
        sig_name = "DIDRLFrntLe_UB"
        sig_start_bit = 47
        update_id_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class DIDRLFrntRiIsYellow:
        sig_name = "DIDRLFrntRiIsYellow"
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
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 16
        byte = 2
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ActvnOfLedFrntWheelLampRi:
        sig_name = "ActvnOfLedFrntWheelLampRi"
        sig_start_bit = 6
        update_id_bit = 2
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

    class DrvrDesDirDrvrDesDir:
        sig_name = "DrvrDesDirDrvrDesDir"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DrvrDesDir1_Undefd': 0, 'DrvrDesDir1_Fwd': 1, 'DrvrDesDir1_Rvs': 2, 'DrvrDesDir1_Neut': 3, 'DrvrDesDir1_Resd0': 4, 'DrvrDesDir1_Resd1': 5, 'DrvrDesDir1_Resd2': 6, 'DrvrDesDir1_Resd3': 7}
        compute_method = None
        length = 3
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class WheelLampRearLe:
        sig_name = "WheelLampRearLe"
        sig_start_bit = 71
        update_id_bit = 64
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 71
        byte = 8
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class DIDRLFrntLeBrightness:
        sig_name = "DIDRLFrntLeBrightness"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 15
        byte = 1
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class ActvnOfLedFrntWheelLampLe:
        sig_name = "ActvnOfLedFrntWheelLampLe"
        sig_start_bit = 7
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
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class DIDRLFrntLeIsYellow:
        sig_name = "DIDRLFrntLeIsYellow"
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
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 8
        byte = 1
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ActvnOfLedReWheelLampLe:
        sig_name = "ActvnOfLedReWheelLampLe"
        sig_start_bit = 5
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
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class DrvrDesDirChks:
        sig_name = "DrvrDesDirChks"
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


class HcmrBodyExpoFr05:
    msg_name = "HcmrBodyExpoFr05"
    msg_id = 272
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.03
    msg_length = 8
    tx_node = "HCMR"
    rx_nodes = ['S2SReceiver', 'BGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class StsOfFrntPosnLampRiScopeStore:
        sig_name = "StsOfFrntPosnLampRiScopeStore"
        sig_start_bit = 7
        update_id_bit = 5
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Sts_Resd': 0, 'Sts_Err': 1, 'Sts_CmplOk': 2, 'Sts_InProgs': 3}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class HcmlBodyExpoFr04:
    msg_name = "HcmlBodyExpoFr04"
    msg_id = 124
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 8
    tx_node = "HCML"
    rx_nodes = ['S2SReceiver', 'BGM']
    sig_group_dict = {'StsOfLvlgLe': ['StsOfLvlgLeChks', 'StsOfLvlgLeCntr', 'StsOfLvlgLeStsOfLvlgLe']}
    sig_group_dataid_dict = {}

    class HdlampLeInpSts1:
        sig_name = "HdlampLeInpSts1"
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

    class StsOfLvlgLeCntr:
        sig_name = "StsOfLvlgLeCntr"
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

    class StsOfLvlgLeChks:
        sig_name = "StsOfLvlgLeChks"
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

    class StsOfLedFrntFogLampLe:
        sig_name = "StsOfLedFrntFogLampLe"
        sig_start_bit = 15
        update_id_bit = 31
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 15
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class StsOfLvlgLe_UB:
        sig_name = "StsOfLvlgLe_UB"
        sig_start_bit = 36
        update_id_bit = 36
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
        startbit = 36
        byte = 4
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class StsOfLvlgLeStsOfLvlgLe:
        sig_name = "StsOfLvlgLeStsOfLvlgLe"
        sig_start_bit = 51
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 51
        byte = 6
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class StsOfLedFrntPosnLampLe:
        sig_name = "StsOfLedFrntPosnLampLe"
        sig_start_bit = 17
        update_id_bit = 30
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 17
        byte = 2
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class StsOfLedDaytiRunngLampLe:
        sig_name = "StsOfLedDaytiRunngLampLe"
        sig_start_bit = 13
        update_id_bit = 32
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 13
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class StsOfLedFrntTurnIndcrLe:
        sig_name = "StsOfLedFrntTurnIndcrLe"
        sig_start_bit = 19
        update_id_bit = 29
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 19
        byte = 2
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class HdlampLeInpSts2:
        sig_name = "HdlampLeInpSts2"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 63
        byte = 7
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class StsOfSwvlgLe:
        sig_name = "StsOfSwvlgLe"
        sig_start_bit = 7
        update_id_bit = 35
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class BgmToAllFuncBodyExpoDiagReqFrame:
    msg_name = "BgmToAllFuncBodyExpoDiagReqFrame"
    msg_id = 2047
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RCML', 'RCMR', 'RCMM', 'HCMR', 'HCML']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class CemBodyExpoCommonFr22:
    msg_name = "CemBodyExpoCommonFr22"
    msg_id = 400
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.045
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCML', 'HCMR']
    sig_group_dict = {'SuspPosnVertLvl': ['SuspPosnVertLvlFrnt', 'SuspPosnVertLvlFrntQf', 'SuspPosnVertLvlRe', 'SuspPosnVertLvlReQf'], 'SuspPosnVertAg': ['SuspPosnVertAgGenQf', 'SuspPosnVertAgSuspPosnVertAg']}
    sig_group_dataid_dict = {}

    class SuspPosnVertLvl_UB:
        sig_name = "SuspPosnVertLvl_UB"
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

    class SuspPosnVertAg_UB:
        sig_name = "SuspPosnVertAg_UB"
        sig_start_bit = 46
        update_id_bit = 46
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
        startbit = 46
        byte = 5
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class SuspPosnVertAgSuspPosnVertAg:
        sig_name = "SuspPosnVertAgSuspPosnVertAg"
        sig_start_bit = 43
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.0001278941807
        sig_value_offset = 0.0
        sig_value_min = -2046
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 43
        bmuws_info = [(5, 0b00001111, 0b11110000, 4, 0), (6, 0b11111111, 0b00000000, 8, 0)]

    class SuspPosnVertLvlFrnt:
        sig_name = "SuspPosnVertLvlFrnt"
        sig_start_bit = 14
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
        startbit = 14
        bmuws_info = [(1, 0b01111111, 0b10000000, 7, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class SuspPosnVertLvlFrntQf:
        sig_name = "SuspPosnVertLvlFrntQf"
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
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class SuspPosnVertLvlRe:
        sig_name = "SuspPosnVertLvlRe"
        sig_start_bit = 30
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
        startbit = 30
        bmuws_info = [(3, 0b01111111, 0b10000000, 7, 0), (4, 0b11111111, 0b00000000, 8, 0)]

    class SuspPosnVertLvlReQf:
        sig_name = "SuspPosnVertLvlReQf"
        sig_start_bit = 3
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
        startbit = 3
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class SuspPosnVertAgGenQf:
        sig_name = "SuspPosnVertAgGenQf"
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


class CemBodyExpoFr51:
    msg_name = "CemBodyExpoFr51"
    msg_id = 538
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RCML', 'RCMR', 'HCMR', 'HCML']
    sig_group_dict = {'IndcrPat': ['IndcrPatCmd1WdTiOff', 'IndcrPatCmd1WdTiOn'], 'ActvnOfIndcr': ['ActvnOfIndcrIndcrOut', 'ActvnOfIndcrIndcrOutChks', 'ActvnOfIndcrIndcrOutCntr']}
    sig_group_dataid_dict = {'ActvnOfIndcr': 158}

    class IndcrPat_UB:
        sig_name = "IndcrPat_UB"
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

    class IndcrSts:
        sig_name = "IndcrSts"
        sig_start_bit = 52
        update_id_bit = 53
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'IndcrSts1_Off': 0, 'IndcrSts1_LeOn': 1, 'IndcrSts1_RiOn': 2, 'IndcrSts1_LeAndRiOn': 3}
        compute_method = None
        length = 2
        startbit = 52
        byte = 6
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class ActvnOfIndcr_UB:
        sig_name = "ActvnOfIndcr_UB"
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

    class ActvnOfIndcrIndcrOutChks:
        sig_name = "ActvnOfIndcrIndcrOutChks"
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

    class ActvnOfIndcrIndcrOut:
        sig_name = "ActvnOfIndcrIndcrOut"
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
        sig_value_table = {'IndcrSts1_Off': 0, 'IndcrSts1_LeOn': 1, 'IndcrSts1_RiOn': 2, 'IndcrSts1_LeAndRiOn': 3}
        compute_method = None
        length = 2
        startbit = 37
        byte = 4
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class EmgyBrkLiIndcrTurn:
        sig_name = "EmgyBrkLiIndcrTurn"
        sig_start_bit = 49
        update_id_bit = 50
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffCrit1_NotVld1': 0, 'OnOffCrit1_Off': 1, 'OnOffCrit1_On': 2, 'OnOffCrit1_NotVld2': 3}
        compute_method = None
        length = 2
        startbit = 49
        byte = 6
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class ActvnOfIndcrIndcrOutCntr:
        sig_name = "ActvnOfIndcrIndcrOutCntr"
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

    class IndcrPatCmd1WdTiOff:
        sig_name = "IndcrPatCmd1WdTiOff"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 0.001
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 65535
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class IndcrPatCmd1WdTiOn:
        sig_name = "IndcrPatCmd1WdTiOn"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 0.001
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 65535
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0)]


class HcmltoEtcXCPFr01:
    msg_name = "HcmltoEtcXCPFr01"
    msg_id = 1424
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "HCML"
    rx_nodes = ['CCM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class BgmBodyExposedCANFr08:
    msg_name = "BgmBodyExposedCANFr08"
    msg_id = 152
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 64
    tx_node = "BGM"
    rx_nodes = ['RCML']
    sig_group_dict = {'PIXReLeX6': ['PIXReLeX6Y1', 'PIXReLeX6Y2', 'PIXReLeX6Y3', 'PIXReLeX6Y4', 'PIXReLeX6Y5', 'PIXReLeX6Y6'], 'PIXReLeX7': ['PIXReLeX7Y1', 'PIXReLeX7Y2', 'PIXReLeX7Y3', 'PIXReLeX7Y4', 'PIXReLeX7Y5', 'PIXReLeX7Y6'], 'PIXReLeXA': ['PIXReLeXAY1', 'PIXReLeXAY2', 'PIXReLeXAY3', 'PIXReLeXAY4', 'PIXReLeXAY5', 'PIXReLeXAY6'], 'PIXReLeX8': ['PIXReLeX8Y1', 'PIXReLeX8Y2', 'PIXReLeX8Y3', 'PIXReLeX8Y4', 'PIXReLeX8Y5', 'PIXReLeX8Y6'], 'PIXReLeX2': ['PIXReLeX2IsY1Yellow', 'PIXReLeX2IsY2Yellow', 'PIXReLeX2IsY3Yellow', 'PIXReLeX2IsY4Yellow', 'PIXReLeX2IsY5Yellow', 'PIXReLeX2IsY6Yellow', 'PIXReLeX2Y1', 'PIXReLeX2Y2', 'PIXReLeX2Y3', 'PIXReLeX2Y4', 'PIXReLeX2Y5', 'PIXReLeX2Y6'], 'PIXReLeXB': ['PIXReLeXBY1', 'PIXReLeXBY2', 'PIXReLeXBY3', 'PIXReLeXBY4', 'PIXReLeXBY5', 'PIXReLeXBY6'], 'PIXReLeX5': ['PIXReLeX5Y1', 'PIXReLeX5Y2', 'PIXReLeX5Y3', 'PIXReLeX5Y4', 'PIXReLeX5Y5', 'PIXReLeX5Y6'], 'PIXReLeX4': ['PIXReLeX4Y1', 'PIXReLeX4Y2', 'PIXReLeX4Y3', 'PIXReLeX4Y4', 'PIXReLeX4Y5', 'PIXReLeX4Y6'], 'PIXReLeX1': ['PIXReLeX1IsY1Yellow', 'PIXReLeX1IsY2Yellow', 'PIXReLeX1IsY3Yellow', 'PIXReLeX1IsY4Yellow', 'PIXReLeX1IsY5Yellow', 'PIXReLeX1IsY6Yellow', 'PIXReLeX1Y1', 'PIXReLeX1Y2', 'PIXReLeX1Y3', 'PIXReLeX1Y4', 'PIXReLeX1Y5', 'PIXReLeX1Y6'], 'PIXReLeX3': ['PIXReLeX3Y1', 'PIXReLeX3Y2', 'PIXReLeX3Y3', 'PIXReLeX3Y4', 'PIXReLeX3Y5', 'PIXReLeX3Y6'], 'PIXReLeX9': ['PIXReLeX9Y1', 'PIXReLeX9Y2', 'PIXReLeX9Y3', 'PIXReLeX9Y4', 'PIXReLeX9Y5', 'PIXReLeX9Y6']}
    sig_group_dataid_dict = {}

    class PIXReLeX9Y6:
        sig_name = "PIXReLeX9Y6"
        sig_start_bit = 376
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 376
        bmuws_info = [(47, 0b00000001, 0b11111110, 1, 0), (48, 0b11111100, 0b00000011, 6, 2)]

    class PIXReLeX2Y3:
        sig_name = "PIXReLeX2Y3"
        sig_start_bit = 71
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 71
        byte = 8
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXReLeX9Y4:
        sig_name = "PIXReLeX9Y4"
        sig_start_bit = 374
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 374
        byte = 46
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class PIXReLeX6Y1:
        sig_name = "PIXReLeX6Y1"
        sig_start_bit = 217
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 217
        bmuws_info = [(27, 0b00000011, 0b11111100, 2, 0), (28, 0b11111000, 0b00000111, 5, 3)]

    class PIXReLeX6_UB:
        sig_name = "PIXReLeX6_UB"
        sig_start_bit = 472
        update_id_bit = 472
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
        startbit = 472
        byte = 59
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class PIXReLeXAY6:
        sig_name = "PIXReLeXAY6"
        sig_start_bit = 430
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 430
        byte = 53
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class PIXReLeX2IsY2Yellow:
        sig_name = "PIXReLeX2IsY2Yellow"
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
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 56
        byte = 7
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class PIXReLeXBY4:
        sig_name = "PIXReLeXBY4"
        sig_start_bit = 450
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 450
        bmuws_info = [(56, 0b00000111, 0b11111000, 3, 0), (57, 0b11110000, 0b00001111, 4, 4)]

    class PIXReLeX5Y3:
        sig_name = "PIXReLeX5Y3"
        sig_start_bit = 197
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 197
        bmuws_info = [(24, 0b00111111, 0b11000000, 6, 0), (25, 0b10000000, 0b01111111, 1, 7)]

    class PIXReLeX8Y5:
        sig_name = "PIXReLeX8Y5"
        sig_start_bit = 329
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 329
        bmuws_info = [(41, 0b00000011, 0b11111100, 2, 0), (42, 0b11111000, 0b00000111, 5, 3)]

    class PIXReLeX8Y2:
        sig_name = "PIXReLeX8Y2"
        sig_start_bit = 318
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 318
        byte = 39
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class PIXReLeXBY1:
        sig_name = "PIXReLeXBY1"
        sig_start_bit = 439
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 439
        byte = 54
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXReLeX2IsY5Yellow:
        sig_name = "PIXReLeX2IsY5Yellow"
        sig_start_bit = 80
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
        startbit = 80
        byte = 10
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class PIXReLeX6Y4:
        sig_name = "PIXReLeX6Y4"
        sig_start_bit = 244
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 244
        bmuws_info = [(30, 0b00011111, 0b11100000, 5, 0), (31, 0b11000000, 0b00111111, 2, 6)]

    class PIXReLeX5Y2:
        sig_name = "PIXReLeX5Y2"
        sig_start_bit = 188
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 188
        bmuws_info = [(23, 0b00011111, 0b11100000, 5, 0), (24, 0b11000000, 0b00111111, 2, 6)]

    class PIXReLeX1Y1:
        sig_name = "PIXReLeX1Y1"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
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

    class PIXReLeX7_UB:
        sig_name = "PIXReLeX7_UB"
        sig_start_bit = 487
        update_id_bit = 487
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
        startbit = 487
        byte = 60
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class PIXReLeX6Y3:
        sig_name = "PIXReLeX6Y3"
        sig_start_bit = 235
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 235
        bmuws_info = [(29, 0b00001111, 0b11110000, 4, 0), (30, 0b11100000, 0b00011111, 3, 5)]

    class PIXReLeX5Y5:
        sig_name = "PIXReLeX5Y5"
        sig_start_bit = 215
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 215
        byte = 26
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXReLeXAY2:
        sig_name = "PIXReLeXAY2"
        sig_start_bit = 394
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 394
        bmuws_info = [(49, 0b00000111, 0b11111000, 3, 0), (50, 0b11110000, 0b00001111, 4, 4)]

    class PIXReLeX1IsY1Yellow:
        sig_name = "PIXReLeX1IsY1Yellow"
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
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 0
        byte = 0
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class PIXReLeXA_UB:
        sig_name = "PIXReLeXA_UB"
        sig_start_bit = 484
        update_id_bit = 484
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
        startbit = 484
        byte = 60
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class PIXReLeX7Y1:
        sig_name = "PIXReLeX7Y1"
        sig_start_bit = 271
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 271
        byte = 33
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXReLeX1IsY2Yellow:
        sig_name = "PIXReLeX1IsY2Yellow"
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
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 8
        byte = 1
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class PIXReLeX2Y1:
        sig_name = "PIXReLeX2Y1"
        sig_start_bit = 55
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 55
        byte = 6
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXReLeX8Y1:
        sig_name = "PIXReLeX8Y1"
        sig_start_bit = 309
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 309
        bmuws_info = [(38, 0b00111111, 0b11000000, 6, 0), (39, 0b10000000, 0b01111111, 1, 7)]

    class PIXReLeXBY3:
        sig_name = "PIXReLeXBY3"
        sig_start_bit = 441
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 441
        bmuws_info = [(55, 0b00000011, 0b11111100, 2, 0), (56, 0b11111000, 0b00000111, 5, 3)]

    class PIXReLeX1IsY3Yellow:
        sig_name = "PIXReLeX1IsY3Yellow"
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
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 16
        byte = 2
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class PIXReLeXAY1:
        sig_name = "PIXReLeXAY1"
        sig_start_bit = 385
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 385
        bmuws_info = [(48, 0b00000011, 0b11111100, 2, 0), (49, 0b11111000, 0b00000111, 5, 3)]

    class PIXReLeX9Y2:
        sig_name = "PIXReLeX9Y2"
        sig_start_bit = 356
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 356
        bmuws_info = [(44, 0b00011111, 0b11100000, 5, 0), (45, 0b11000000, 0b00111111, 2, 6)]

    class PIXReLeXAY4:
        sig_name = "PIXReLeXAY4"
        sig_start_bit = 412
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 412
        bmuws_info = [(51, 0b00011111, 0b11100000, 5, 0), (52, 0b11000000, 0b00111111, 2, 6)]

    class PIXReLeX6Y5:
        sig_name = "PIXReLeX6Y5"
        sig_start_bit = 253
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 253
        bmuws_info = [(31, 0b00111111, 0b11000000, 6, 0), (32, 0b10000000, 0b01111111, 1, 7)]

    class PIXReLeXAY3:
        sig_name = "PIXReLeXAY3"
        sig_start_bit = 403
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 403
        bmuws_info = [(50, 0b00001111, 0b11110000, 4, 0), (51, 0b11100000, 0b00011111, 3, 5)]

    class PIXReLeX8Y4:
        sig_name = "PIXReLeX8Y4"
        sig_start_bit = 320
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 320
        bmuws_info = [(40, 0b00000001, 0b11111110, 1, 0), (41, 0b11111100, 0b00000011, 6, 2)]

    class PIXReLeX4Y6:
        sig_name = "PIXReLeX4Y6"
        sig_start_bit = 170
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 170
        bmuws_info = [(21, 0b00000111, 0b11111000, 3, 0), (22, 0b11110000, 0b00001111, 4, 4)]

    class PIXReLeX5Y1:
        sig_name = "PIXReLeX5Y1"
        sig_start_bit = 179
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 179
        bmuws_info = [(22, 0b00001111, 0b11110000, 4, 0), (23, 0b11100000, 0b00011111, 3, 5)]

    class PIXReLeX2Y6:
        sig_name = "PIXReLeX2Y6"
        sig_start_bit = 95
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 95
        byte = 11
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXReLeX4Y4:
        sig_name = "PIXReLeX4Y4"
        sig_start_bit = 152
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 152
        bmuws_info = [(19, 0b00000001, 0b11111110, 1, 0), (20, 0b11111100, 0b00000011, 6, 2)]

    class PIXReLeX8_UB:
        sig_name = "PIXReLeX8_UB"
        sig_start_bit = 486
        update_id_bit = 486
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
        startbit = 486
        byte = 60
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class PIXReLeXBY2:
        sig_name = "PIXReLeXBY2"
        sig_start_bit = 432
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 432
        bmuws_info = [(54, 0b00000001, 0b11111110, 1, 0), (55, 0b11111100, 0b00000011, 6, 2)]

    class PIXReLeXBY5:
        sig_name = "PIXReLeXBY5"
        sig_start_bit = 459
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 459
        bmuws_info = [(57, 0b00001111, 0b11110000, 4, 0), (58, 0b11100000, 0b00011111, 3, 5)]

    class PIXReLeX2_UB:
        sig_name = "PIXReLeX2_UB"
        sig_start_bit = 476
        update_id_bit = 476
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
        startbit = 476
        byte = 59
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class PIXReLeX6Y2:
        sig_name = "PIXReLeX6Y2"
        sig_start_bit = 226
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 226
        bmuws_info = [(28, 0b00000111, 0b11111000, 3, 0), (29, 0b11110000, 0b00001111, 4, 4)]

    class PIXReLeX3Y4:
        sig_name = "PIXReLeX3Y4"
        sig_start_bit = 114
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 114
        bmuws_info = [(14, 0b00000111, 0b11111000, 3, 0), (15, 0b11110000, 0b00001111, 4, 4)]

    class PIXReLeX3Y1:
        sig_name = "PIXReLeX3Y1"
        sig_start_bit = 103
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 103
        byte = 12
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXReLeX5Y6:
        sig_name = "PIXReLeX5Y6"
        sig_start_bit = 208
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 208
        bmuws_info = [(26, 0b00000001, 0b11111110, 1, 0), (27, 0b11111100, 0b00000011, 6, 2)]

    class PIXReLeX6Y6:
        sig_name = "PIXReLeX6Y6"
        sig_start_bit = 262
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 262
        byte = 32
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class PIXReLeXAY5:
        sig_name = "PIXReLeXAY5"
        sig_start_bit = 421
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 421
        bmuws_info = [(52, 0b00111111, 0b11000000, 6, 0), (53, 0b10000000, 0b01111111, 1, 7)]

    class PIXReLeX7Y6:
        sig_name = "PIXReLeX7Y6"
        sig_start_bit = 300
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 300
        bmuws_info = [(37, 0b00011111, 0b11100000, 5, 0), (38, 0b11000000, 0b00111111, 2, 6)]

    class PIXReLeX1IsY4Yellow:
        sig_name = "PIXReLeX1IsY4Yellow"
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
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 24
        byte = 3
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class PIXReLeX2IsY1Yellow:
        sig_name = "PIXReLeX2IsY1Yellow"
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
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 48
        byte = 6
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class PIXReLeXB_UB:
        sig_name = "PIXReLeXB_UB"
        sig_start_bit = 483
        update_id_bit = 483
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
        startbit = 483
        byte = 60
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class PIXReLeX7Y3:
        sig_name = "PIXReLeX7Y3"
        sig_start_bit = 273
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 273
        bmuws_info = [(34, 0b00000011, 0b11111100, 2, 0), (35, 0b11111000, 0b00000111, 5, 3)]

    class PIXReLeX2IsY3Yellow:
        sig_name = "PIXReLeX2IsY3Yellow"
        sig_start_bit = 64
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
        startbit = 64
        byte = 8
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class PIXReLeX1Y6:
        sig_name = "PIXReLeX1Y6"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 47
        byte = 5
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXReLeX9Y3:
        sig_name = "PIXReLeX9Y3"
        sig_start_bit = 365
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 365
        bmuws_info = [(45, 0b00111111, 0b11000000, 6, 0), (46, 0b10000000, 0b01111111, 1, 7)]

    class PIXReLeX5_UB:
        sig_name = "PIXReLeX5_UB"
        sig_start_bit = 473
        update_id_bit = 473
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
        startbit = 473
        byte = 59
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class PIXReLeX2IsY6Yellow:
        sig_name = "PIXReLeX2IsY6Yellow"
        sig_start_bit = 88
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
        startbit = 88
        byte = 11
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class PIXReLeX9Y5:
        sig_name = "PIXReLeX9Y5"
        sig_start_bit = 383
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 383
        byte = 47
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXReLeX4_UB:
        sig_name = "PIXReLeX4_UB"
        sig_start_bit = 474
        update_id_bit = 474
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
        startbit = 474
        byte = 59
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class PIXReLeX3Y5:
        sig_name = "PIXReLeX3Y5"
        sig_start_bit = 123
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 123
        bmuws_info = [(15, 0b00001111, 0b11110000, 4, 0), (16, 0b11100000, 0b00011111, 3, 5)]

    class PIXReLeX9Y1:
        sig_name = "PIXReLeX9Y1"
        sig_start_bit = 347
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 347
        bmuws_info = [(43, 0b00001111, 0b11110000, 4, 0), (44, 0b11100000, 0b00011111, 3, 5)]

    class PIXReLeX3Y6:
        sig_name = "PIXReLeX3Y6"
        sig_start_bit = 132
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 132
        bmuws_info = [(16, 0b00011111, 0b11100000, 5, 0), (17, 0b11000000, 0b00111111, 2, 6)]

    class PIXReLeXBY6:
        sig_name = "PIXReLeXBY6"
        sig_start_bit = 468
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 468
        bmuws_info = [(58, 0b00011111, 0b11100000, 5, 0), (59, 0b11000000, 0b00111111, 2, 6)]

    class PIXReLeX4Y3:
        sig_name = "PIXReLeX4Y3"
        sig_start_bit = 159
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 159
        byte = 19
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXReLeX1Y2:
        sig_name = "PIXReLeX1Y2"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 15
        byte = 1
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXReLeX1_UB:
        sig_name = "PIXReLeX1_UB"
        sig_start_bit = 477
        update_id_bit = 477
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
        startbit = 477
        byte = 59
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class PIXReLeX7Y4:
        sig_name = "PIXReLeX7Y4"
        sig_start_bit = 282
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 282
        bmuws_info = [(35, 0b00000111, 0b11111000, 3, 0), (36, 0b11110000, 0b00001111, 4, 4)]

    class PIXReLeX4Y1:
        sig_name = "PIXReLeX4Y1"
        sig_start_bit = 141
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 141
        bmuws_info = [(17, 0b00111111, 0b11000000, 6, 0), (18, 0b10000000, 0b01111111, 1, 7)]

    class PIXReLeX2Y2:
        sig_name = "PIXReLeX2Y2"
        sig_start_bit = 63
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
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

    class PIXReLeX2Y5:
        sig_name = "PIXReLeX2Y5"
        sig_start_bit = 87
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 87
        byte = 10
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXReLeX3Y3:
        sig_name = "PIXReLeX3Y3"
        sig_start_bit = 105
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 105
        bmuws_info = [(13, 0b00000011, 0b11111100, 2, 0), (14, 0b11111000, 0b00000111, 5, 3)]

    class PIXReLeX5Y4:
        sig_name = "PIXReLeX5Y4"
        sig_start_bit = 206
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 206
        byte = 25
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class PIXReLeX4Y5:
        sig_name = "PIXReLeX4Y5"
        sig_start_bit = 161
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 161
        bmuws_info = [(20, 0b00000011, 0b11111100, 2, 0), (21, 0b11111000, 0b00000111, 5, 3)]

    class PIXReLeX7Y2:
        sig_name = "PIXReLeX7Y2"
        sig_start_bit = 264
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 264
        bmuws_info = [(33, 0b00000001, 0b11111110, 1, 0), (34, 0b11111100, 0b00000011, 6, 2)]

    class PIXReLeX1IsY6Yellow:
        sig_name = "PIXReLeX1IsY6Yellow"
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
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 40
        byte = 5
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class PIXReLeX1IsY5Yellow:
        sig_name = "PIXReLeX1IsY5Yellow"
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
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 32
        byte = 4
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class PIXReLeX4Y2:
        sig_name = "PIXReLeX4Y2"
        sig_start_bit = 150
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 150
        byte = 18
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class PIXReLeX3_UB:
        sig_name = "PIXReLeX3_UB"
        sig_start_bit = 475
        update_id_bit = 475
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
        startbit = 475
        byte = 59
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class PIXReLeX2Y4:
        sig_name = "PIXReLeX2Y4"
        sig_start_bit = 79
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 79
        byte = 9
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXReLeX1Y5:
        sig_name = "PIXReLeX1Y5"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 39
        byte = 4
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXReLeX1Y3:
        sig_name = "PIXReLeX1Y3"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 23
        byte = 2
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXReLeX1Y4:
        sig_name = "PIXReLeX1Y4"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 31
        byte = 3
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXReLeX3Y2:
        sig_name = "PIXReLeX3Y2"
        sig_start_bit = 96
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 96
        bmuws_info = [(12, 0b00000001, 0b11111110, 1, 0), (13, 0b11111100, 0b00000011, 6, 2)]

    class PIXReLeX2IsY4Yellow:
        sig_name = "PIXReLeX2IsY4Yellow"
        sig_start_bit = 72
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
        startbit = 72
        byte = 9
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class PIXReLeX8Y6:
        sig_name = "PIXReLeX8Y6"
        sig_start_bit = 338
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 338
        bmuws_info = [(42, 0b00000111, 0b11111000, 3, 0), (43, 0b11110000, 0b00001111, 4, 4)]

    class PIXReLeX7Y5:
        sig_name = "PIXReLeX7Y5"
        sig_start_bit = 291
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 291
        bmuws_info = [(36, 0b00001111, 0b11110000, 4, 0), (37, 0b11100000, 0b00011111, 3, 5)]

    class PIXReLeX8Y3:
        sig_name = "PIXReLeX8Y3"
        sig_start_bit = 327
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
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

    class PIXReLeX9_UB:
        sig_name = "PIXReLeX9_UB"
        sig_start_bit = 485
        update_id_bit = 485
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
        startbit = 485
        byte = 60
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5


class HcmrBodyExpoFr02:
    msg_name = "HcmrBodyExpoFr02"
    msg_id = 594
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 3
    tx_node = "HCMR"
    rx_nodes = ['S2SReceiver', 'BGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class StsOfLedLoBeamRi:
        sig_name = "StsOfLedLoBeamRi"
        sig_start_bit = 4
        update_id_bit = 5
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 4
        byte = 0
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class StsOfLedFrntLampRi2:
        sig_name = "StsOfLedFrntLampRi2"
        sig_start_bit = 13
        update_id_bit = 10
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 13
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class StsOfLedHiBeamRi:
        sig_name = "StsOfLedHiBeamRi"
        sig_start_bit = 1
        update_id_bit = 2
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class StsOfLedFrntLampRi1:
        sig_name = "StsOfLedFrntLampRi1"
        sig_start_bit = 15
        update_id_bit = 11
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 15
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class StsOfLedFrntWheelLampRi:
        sig_name = "StsOfLedFrntWheelLampRi"
        sig_start_bit = 9
        update_id_bit = 23
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 9
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0


class EtcToCemBodyExpoDevDiagFr03:
    msg_name = "EtcToCemBodyExpoDevDiagFr03"
    msg_id = 1425
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CCM"
    rx_nodes = ['BGM']
    sig_group_dict = {'CEMdevelpsignalgroupreq': ['CEMdevelpsignalgroupreqFunctiondevpsignalgroup1', 'CEMdevelpsignalgroupreqFunctiondevpsignalgroup2', 'CEMdevelpsignalgroupreqFunctiondevpsignalgroup3', 'CEMdevelpsignalgroupreqFunctiondevpsignalgroup4', 'CEMdevelpsignalgroupreqFunctiondevpsignalgroup5', 'CEMdevelpsignalgroupreqFunctiondevpsignalgroup6', 'CEMdevelpsignalgroupreqFunctiondevpsignalgroup7', 'CEMdevelpsignalgroupreqFunctiondevpsignalgroup8']}
    sig_group_dataid_dict = {}

    class CEMdevelpsignalgroupreqFunctiondevpsignalgroup6:
        sig_name = "CEMdevelpsignalgroupreqFunctiondevpsignalgroup6"
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

    class CEMdevelpsignalgroupreqFunctiondevpsignalgroup8:
        sig_name = "CEMdevelpsignalgroupreqFunctiondevpsignalgroup8"
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

    class CEMdevelpsignalgroupreqFunctiondevpsignalgroup4:
        sig_name = "CEMdevelpsignalgroupreqFunctiondevpsignalgroup4"
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

    class CEMdevelpsignalgroupreqFunctiondevpsignalgroup3:
        sig_name = "CEMdevelpsignalgroupreqFunctiondevpsignalgroup3"
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

    class CEMdevelpsignalgroupreqFunctiondevpsignalgroup7:
        sig_name = "CEMdevelpsignalgroupreqFunctiondevpsignalgroup7"
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

    class CEMdevelpsignalgroupreqFunctiondevpsignalgroup5:
        sig_name = "CEMdevelpsignalgroupreqFunctiondevpsignalgroup5"
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

    class CEMdevelpsignalgroupreqFunctiondevpsignalgroup1:
        sig_name = "CEMdevelpsignalgroupreqFunctiondevpsignalgroup1"
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

    class CEMdevelpsignalgroupreqFunctiondevpsignalgroup2:
        sig_name = "CEMdevelpsignalgroupreqFunctiondevpsignalgroup2"
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


class BgmBodyExposedCANFr06:
    msg_name = "BgmBodyExposedCANFr06"
    msg_id = 150
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 64
    tx_node = "BGM"
    rx_nodes = ['HCML']
    sig_group_dict = {'PIXFrntLeX7': ['PIXFrntLeX7Y1', 'PIXFrntLeX7Y2', 'PIXFrntLeX7Y3', 'PIXFrntLeX7Y4', 'PIXFrntLeX7Y5', 'PIXFrntLeX7Y6'], 'PIXFrntLeX8': ['PIXFrntLeX8Y1', 'PIXFrntLeX8Y2', 'PIXFrntLeX8Y3', 'PIXFrntLeX8Y4', 'PIXFrntLeX8Y5', 'PIXFrntLeX8Y6'], 'PIXFrntLeX3': ['PIXFrntLeX3Y1', 'PIXFrntLeX3Y2', 'PIXFrntLeX3Y3', 'PIXFrntLeX3Y4', 'PIXFrntLeX3Y5', 'PIXFrntLeX3Y6'], 'PIXFrntLeX4': ['PIXFrntLeX4Y1', 'PIXFrntLeX4Y2', 'PIXFrntLeX4Y3', 'PIXFrntLeX4Y4', 'PIXFrntLeX4Y5', 'PIXFrntLeX4Y6'], 'PIXFrntLeX5': ['PIXFrntLeX5Y1', 'PIXFrntLeX5Y2', 'PIXFrntLeX5Y3', 'PIXFrntLeX5Y4', 'PIXFrntLeX5Y5', 'PIXFrntLeX5Y6'], 'PIXFrntLeXB': ['PIXFrntLeXBY1', 'PIXFrntLeXBY2', 'PIXFrntLeXBY3', 'PIXFrntLeXBY4', 'PIXFrntLeXBY5', 'PIXFrntLeXBY6'], 'PIXFrntLeX1': ['PIXFrntLeX1Y1', 'PIXFrntLeX1Y2', 'PIXFrntLeX1Y3', 'PIXFrntLeX1Y4', 'PIXFrntLeX1Y5', 'PIXFrntLeX1Y6'], 'PIXFrntLeX9': ['PIXFrntLeX9Y1', 'PIXFrntLeX9Y2', 'PIXFrntLeX9Y3', 'PIXFrntLeX9Y4', 'PIXFrntLeX9Y5', 'PIXFrntLeX9Y6'], 'PIXFrntLeXA': ['PIXFrntLeXAY1', 'PIXFrntLeXAY2', 'PIXFrntLeXAY3', 'PIXFrntLeXAY4', 'PIXFrntLeXAY5', 'PIXFrntLeXAY6'], 'PIXFrntLeX6': ['PIXFrntLeX6Y1', 'PIXFrntLeX6Y2', 'PIXFrntLeX6Y3', 'PIXFrntLeX6Y4', 'PIXFrntLeX6Y5', 'PIXFrntLeX6Y6'], 'PIXFrntLeX2': ['PIXFrntLeX2Y1', 'PIXFrntLeX2Y2', 'PIXFrntLeX2Y3', 'PIXFrntLeX2Y4', 'PIXFrntLeX2Y5', 'PIXFrntLeX2Y6']}
    sig_group_dataid_dict = {}

    class PIXFrntLeX8Y3:
        sig_name = "PIXFrntLeX8Y3"
        sig_start_bit = 317
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 317
        bmuws_info = [(39, 0b00111111, 0b11000000, 6, 0), (40, 0b10000000, 0b01111111, 1, 7)]

    class PIXFrntLeXBY4:
        sig_name = "PIXFrntLeXBY4"
        sig_start_bit = 463
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 463
        byte = 57
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXFrntLeXBY2:
        sig_name = "PIXFrntLeXBY2"
        sig_start_bit = 447
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 447
        byte = 55
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXFrntLeX2Y3:
        sig_name = "PIXFrntLeX2Y3"
        sig_start_bit = 62
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 62
        byte = 7
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class PIXFrntLeX7_UB:
        sig_name = "PIXFrntLeX7_UB"
        sig_start_bit = 485
        update_id_bit = 485
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
        startbit = 485
        byte = 60
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class PIXFrntLeX9Y5:
        sig_name = "PIXFrntLeX9Y5"
        sig_start_bit = 371
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 371
        bmuws_info = [(46, 0b00001111, 0b11110000, 4, 0), (47, 0b11100000, 0b00011111, 3, 5)]

    class PIXFrntLeX7Y4:
        sig_name = "PIXFrntLeX7Y4"
        sig_start_bit = 272
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 272
        bmuws_info = [(34, 0b00000001, 0b11111110, 1, 0), (35, 0b11111100, 0b00000011, 6, 2)]

    class PIXFrntLeX3Y5:
        sig_name = "PIXFrntLeX3Y5"
        sig_start_bit = 117
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 117
        bmuws_info = [(14, 0b00111111, 0b11000000, 6, 0), (15, 0b10000000, 0b01111111, 1, 7)]

    class PIXFrntLeX9Y6:
        sig_name = "PIXFrntLeX9Y6"
        sig_start_bit = 380
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 380
        bmuws_info = [(47, 0b00011111, 0b11100000, 5, 0), (48, 0b11000000, 0b00111111, 2, 6)]

    class PIXFrntLeX8_UB:
        sig_name = "PIXFrntLeX8_UB"
        sig_start_bit = 487
        update_id_bit = 487
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
        startbit = 487
        byte = 60
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class PIXFrntLeX8Y4:
        sig_name = "PIXFrntLeX8Y4"
        sig_start_bit = 326
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 326
        byte = 40
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class PIXFrntLeX8Y5:
        sig_name = "PIXFrntLeX8Y5"
        sig_start_bit = 335
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 335
        byte = 41
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXFrntLeX5Y4:
        sig_name = "PIXFrntLeX5Y4"
        sig_start_bit = 198
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 198
        byte = 24
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class PIXFrntLeX4Y4:
        sig_name = "PIXFrntLeX4Y4"
        sig_start_bit = 145
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 145
        bmuws_info = [(18, 0b00000011, 0b11111100, 2, 0), (19, 0b11111000, 0b00000111, 5, 3)]

    class PIXFrntLeX6Y5:
        sig_name = "PIXFrntLeX6Y5"
        sig_start_bit = 243
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 243
        bmuws_info = [(30, 0b00001111, 0b11110000, 4, 0), (31, 0b11100000, 0b00011111, 3, 5)]

    class PIXFrntLeX3_UB:
        sig_name = "PIXFrntLeX3_UB"
        sig_start_bit = 135
        update_id_bit = 135
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
        startbit = 135
        byte = 16
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class PIXFrntLeX1Y4:
        sig_name = "PIXFrntLeX1Y4"
        sig_start_bit = 18
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 18
        bmuws_info = [(2, 0b00000111, 0b11111000, 3, 0), (3, 0b11110000, 0b00001111, 4, 4)]

    class PIXFrntLeX5Y5:
        sig_name = "PIXFrntLeX5Y5"
        sig_start_bit = 207
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 207
        byte = 25
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXFrntLeX6Y6:
        sig_name = "PIXFrntLeX6Y6"
        sig_start_bit = 252
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 252
        bmuws_info = [(31, 0b00011111, 0b11100000, 5, 0), (32, 0b11000000, 0b00111111, 2, 6)]

    class PIXFrntLeX5Y1:
        sig_name = "PIXFrntLeX5Y1"
        sig_start_bit = 171
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 171
        bmuws_info = [(21, 0b00001111, 0b11110000, 4, 0), (22, 0b11100000, 0b00011111, 3, 5)]

    class PIXFrntLeX4_UB:
        sig_name = "PIXFrntLeX4_UB"
        sig_start_bit = 172
        update_id_bit = 172
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
        startbit = 172
        byte = 21
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class PIXFrntLeX1Y6:
        sig_name = "PIXFrntLeX1Y6"
        sig_start_bit = 36
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 36
        bmuws_info = [(4, 0b00011111, 0b11100000, 5, 0), (5, 0b11000000, 0b00111111, 2, 6)]

    class PIXFrntLeXBY1:
        sig_name = "PIXFrntLeXBY1"
        sig_start_bit = 439
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 439
        byte = 54
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXFrntLeXBY5:
        sig_name = "PIXFrntLeXBY5"
        sig_start_bit = 471
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 471
        byte = 58
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXFrntLeXAY6:
        sig_name = "PIXFrntLeXAY6"
        sig_start_bit = 418
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 418
        bmuws_info = [(52, 0b00000111, 0b11111000, 3, 0), (53, 0b11110000, 0b00001111, 4, 4)]

    class PIXFrntLeX6Y4:
        sig_name = "PIXFrntLeX6Y4"
        sig_start_bit = 234
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 234
        bmuws_info = [(29, 0b00000111, 0b11111000, 3, 0), (30, 0b11110000, 0b00001111, 4, 4)]

    class PIXFrntLeX3Y6:
        sig_name = "PIXFrntLeX3Y6"
        sig_start_bit = 126
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 126
        byte = 15
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class PIXFrntLeX7Y2:
        sig_name = "PIXFrntLeX7Y2"
        sig_start_bit = 270
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 270
        byte = 33
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class PIXFrntLeX6Y2:
        sig_name = "PIXFrntLeX6Y2"
        sig_start_bit = 216
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 216
        bmuws_info = [(27, 0b00000001, 0b11111110, 1, 0), (28, 0b11111100, 0b00000011, 6, 2)]

    class PIXFrntLeX1Y5:
        sig_name = "PIXFrntLeX1Y5"
        sig_start_bit = 27
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 27
        bmuws_info = [(3, 0b00001111, 0b11110000, 4, 0), (4, 0b11100000, 0b00011111, 3, 5)]

    class PIXFrntLeXAY2:
        sig_name = "PIXFrntLeXAY2"
        sig_start_bit = 398
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 398
        byte = 49
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class PIXFrntLeX5_UB:
        sig_name = "PIXFrntLeX5_UB"
        sig_start_bit = 209
        update_id_bit = 209
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
        startbit = 209
        byte = 26
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class PIXFrntLeXB_UB:
        sig_name = "PIXFrntLeXB_UB"
        sig_start_bit = 472
        update_id_bit = 472
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
        startbit = 472
        byte = 59
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class PIXFrntLeX8Y2:
        sig_name = "PIXFrntLeX8Y2"
        sig_start_bit = 308
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 308
        bmuws_info = [(38, 0b00011111, 0b11100000, 5, 0), (39, 0b11000000, 0b00111111, 2, 6)]

    class PIXFrntLeX1_UB:
        sig_name = "PIXFrntLeX1_UB"
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

    class PIXFrntLeX9_UB:
        sig_name = "PIXFrntLeX9_UB"
        sig_start_bit = 486
        update_id_bit = 486
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
        startbit = 486
        byte = 60
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class PIXFrntLeX1Y2:
        sig_name = "PIXFrntLeX1Y2"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 0
        bmuws_info = [(0, 0b00000001, 0b11111110, 1, 0), (1, 0b11111100, 0b00000011, 6, 2)]

    class PIXFrntLeX7Y6:
        sig_name = "PIXFrntLeX7Y6"
        sig_start_bit = 290
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 290
        bmuws_info = [(36, 0b00000111, 0b11111000, 3, 0), (37, 0b11110000, 0b00001111, 4, 4)]

    class PIXFrntLeX8Y1:
        sig_name = "PIXFrntLeX8Y1"
        sig_start_bit = 299
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 299
        bmuws_info = [(37, 0b00001111, 0b11110000, 4, 0), (38, 0b11100000, 0b00011111, 3, 5)]

    class PIXFrntLeXA_UB:
        sig_name = "PIXFrntLeXA_UB"
        sig_start_bit = 427
        update_id_bit = 427
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
        startbit = 427
        byte = 53
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class PIXFrntLeX1Y1:
        sig_name = "PIXFrntLeX1Y1"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
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

    class PIXFrntLeX4Y5:
        sig_name = "PIXFrntLeX4Y5"
        sig_start_bit = 154
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 154
        bmuws_info = [(19, 0b00000111, 0b11111000, 3, 0), (20, 0b11110000, 0b00001111, 4, 4)]

    class PIXFrntLeX6Y3:
        sig_name = "PIXFrntLeX6Y3"
        sig_start_bit = 225
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 225
        bmuws_info = [(28, 0b00000011, 0b11111100, 2, 0), (29, 0b11111000, 0b00000111, 5, 3)]

    class PIXFrntLeX7Y5:
        sig_name = "PIXFrntLeX7Y5"
        sig_start_bit = 281
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 281
        bmuws_info = [(35, 0b00000011, 0b11111100, 2, 0), (36, 0b11111000, 0b00000111, 5, 3)]

    class PIXFrntLeX2Y5:
        sig_name = "PIXFrntLeX2Y5"
        sig_start_bit = 64
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 64
        bmuws_info = [(8, 0b00000001, 0b11111110, 1, 0), (9, 0b11111100, 0b00000011, 6, 2)]

    class PIXFrntLeXBY6:
        sig_name = "PIXFrntLeXBY6"
        sig_start_bit = 479
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 479
        byte = 59
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXFrntLeX3Y2:
        sig_name = "PIXFrntLeX3Y2"
        sig_start_bit = 90
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 90
        bmuws_info = [(11, 0b00000111, 0b11111000, 3, 0), (12, 0b11110000, 0b00001111, 4, 4)]

    class PIXFrntLeX4Y3:
        sig_name = "PIXFrntLeX4Y3"
        sig_start_bit = 136
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 136
        bmuws_info = [(17, 0b00000001, 0b11111110, 1, 0), (18, 0b11111100, 0b00000011, 6, 2)]

    class PIXFrntLeX4Y1:
        sig_name = "PIXFrntLeX4Y1"
        sig_start_bit = 134
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 134
        byte = 16
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class PIXFrntLeX3Y1:
        sig_name = "PIXFrntLeX3Y1"
        sig_start_bit = 81
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 81
        bmuws_info = [(10, 0b00000011, 0b11111100, 2, 0), (11, 0b11111000, 0b00000111, 5, 3)]

    class PIXFrntLeX1Y3:
        sig_name = "PIXFrntLeX1Y3"
        sig_start_bit = 9
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 9
        bmuws_info = [(1, 0b00000011, 0b11111100, 2, 0), (2, 0b11111000, 0b00000111, 5, 3)]

    class PIXFrntLeX5Y2:
        sig_name = "PIXFrntLeX5Y2"
        sig_start_bit = 180
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 180
        bmuws_info = [(22, 0b00011111, 0b11100000, 5, 0), (23, 0b11000000, 0b00111111, 2, 6)]

    class PIXFrntLeX6_UB:
        sig_name = "PIXFrntLeX6_UB"
        sig_start_bit = 208
        update_id_bit = 208
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
        startbit = 208
        byte = 26
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class PIXFrntLeX9Y3:
        sig_name = "PIXFrntLeX9Y3"
        sig_start_bit = 353
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 353
        bmuws_info = [(44, 0b00000011, 0b11111100, 2, 0), (45, 0b11111000, 0b00000111, 5, 3)]

    class PIXFrntLeX3Y4:
        sig_name = "PIXFrntLeX3Y4"
        sig_start_bit = 108
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 108
        bmuws_info = [(13, 0b00011111, 0b11100000, 5, 0), (14, 0b11000000, 0b00111111, 2, 6)]

    class PIXFrntLeX2Y2:
        sig_name = "PIXFrntLeX2Y2"
        sig_start_bit = 53
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 53
        bmuws_info = [(6, 0b00111111, 0b11000000, 6, 0), (7, 0b10000000, 0b01111111, 1, 7)]

    class PIXFrntLeXAY4:
        sig_name = "PIXFrntLeXAY4"
        sig_start_bit = 400
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 400
        bmuws_info = [(50, 0b00000001, 0b11111110, 1, 0), (51, 0b11111100, 0b00000011, 6, 2)]

    class PIXFrntLeX7Y3:
        sig_name = "PIXFrntLeX7Y3"
        sig_start_bit = 279
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 279
        byte = 34
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXFrntLeX9Y2:
        sig_name = "PIXFrntLeX9Y2"
        sig_start_bit = 344
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 344
        bmuws_info = [(43, 0b00000001, 0b11111110, 1, 0), (44, 0b11111100, 0b00000011, 6, 2)]

    class PIXFrntLeX9Y4:
        sig_name = "PIXFrntLeX9Y4"
        sig_start_bit = 362
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 362
        bmuws_info = [(45, 0b00000111, 0b11111000, 3, 0), (46, 0b11110000, 0b00001111, 4, 4)]

    class PIXFrntLeX4Y2:
        sig_name = "PIXFrntLeX4Y2"
        sig_start_bit = 143
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 143
        byte = 17
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXFrntLeX2_UB:
        sig_name = "PIXFrntLeX2_UB"
        sig_start_bit = 82
        update_id_bit = 82
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
        startbit = 82
        byte = 10
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class PIXFrntLeXAY1:
        sig_name = "PIXFrntLeXAY1"
        sig_start_bit = 389
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 389
        bmuws_info = [(48, 0b00111111, 0b11000000, 6, 0), (49, 0b10000000, 0b01111111, 1, 7)]

    class PIXFrntLeXBY3:
        sig_name = "PIXFrntLeXBY3"
        sig_start_bit = 455
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 455
        byte = 56
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXFrntLeX9Y1:
        sig_name = "PIXFrntLeX9Y1"
        sig_start_bit = 351
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 351
        byte = 43
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXFrntLeX2Y1:
        sig_name = "PIXFrntLeX2Y1"
        sig_start_bit = 44
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 44
        bmuws_info = [(5, 0b00011111, 0b11100000, 5, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class PIXFrntLeX5Y3:
        sig_name = "PIXFrntLeX5Y3"
        sig_start_bit = 189
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 189
        bmuws_info = [(23, 0b00111111, 0b11000000, 6, 0), (24, 0b10000000, 0b01111111, 1, 7)]

    class PIXFrntLeX2Y6:
        sig_name = "PIXFrntLeX2Y6"
        sig_start_bit = 73
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 73
        bmuws_info = [(9, 0b00000011, 0b11111100, 2, 0), (10, 0b11111000, 0b00000111, 5, 3)]

    class PIXFrntLeX7Y1:
        sig_name = "PIXFrntLeX7Y1"
        sig_start_bit = 261
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 261
        bmuws_info = [(32, 0b00111111, 0b11000000, 6, 0), (33, 0b10000000, 0b01111111, 1, 7)]

    class PIXFrntLeX8Y6:
        sig_name = "PIXFrntLeX8Y6"
        sig_start_bit = 343
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 343
        byte = 42
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXFrntLeX4Y6:
        sig_name = "PIXFrntLeX4Y6"
        sig_start_bit = 163
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 163
        bmuws_info = [(20, 0b00001111, 0b11110000, 4, 0), (21, 0b11100000, 0b00011111, 3, 5)]

    class PIXFrntLeXAY5:
        sig_name = "PIXFrntLeXAY5"
        sig_start_bit = 409
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 409
        bmuws_info = [(51, 0b00000011, 0b11111100, 2, 0), (52, 0b11111000, 0b00000111, 5, 3)]

    class PIXFrntLeX2Y4:
        sig_name = "PIXFrntLeX2Y4"
        sig_start_bit = 71
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 71
        byte = 8
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXFrntLeX6Y1:
        sig_name = "PIXFrntLeX6Y1"
        sig_start_bit = 223
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 223
        byte = 27
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXFrntLeX3Y3:
        sig_name = "PIXFrntLeX3Y3"
        sig_start_bit = 99
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 99
        bmuws_info = [(12, 0b00001111, 0b11110000, 4, 0), (13, 0b11100000, 0b00011111, 3, 5)]

    class PIXFrntLeXAY3:
        sig_name = "PIXFrntLeXAY3"
        sig_start_bit = 407
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 407
        byte = 50
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXFrntLeX5Y6:
        sig_name = "PIXFrntLeX5Y6"
        sig_start_bit = 200
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 200
        bmuws_info = [(25, 0b00000001, 0b11111110, 1, 0), (26, 0b11111100, 0b00000011, 6, 2)]


class CemBodyExpoCommonFr05:
    msg_name = "CemBodyExpoCommonFr05"
    msg_id = 384
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RCML', 'RCMR', 'RCMM', 'HCMR', 'HCML']
    sig_group_dict = {'VehCfgPrm': ['VehCfgPrmBlkIDBytePosn1', 'VehCfgPrmCCPBytePosn2', 'VehCfgPrmCCPBytePosn3', 'VehCfgPrmCCPBytePosn4', 'VehCfgPrmCCPBytePosn5', 'VehCfgPrmCCPBytePosn6', 'VehCfgPrmCCPBytePosn7', 'VehCfgPrmCCPBytePosn8']}
    sig_group_dataid_dict = {}

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


class BgmBodyExposedCANFr09:
    msg_name = "BgmBodyExposedCANFr09"
    msg_id = 153
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 64
    tx_node = "BGM"
    rx_nodes = ['RCML', 'RCMR']
    sig_group_dict = {'PIXReLeXC': ['PIXReLeXCY1', 'PIXReLeXCY2', 'PIXReLeXCY3', 'PIXReLeXCY4', 'PIXReLeXCY5', 'PIXReLeXCY6'], 'PIXReRiXF': ['PIXReRiXFY1', 'PIXReRiXFY2', 'PIXReRiXFY3', 'PIXReRiXFY4', 'PIXReRiXFY5', 'PIXReRiXFY6'], 'PIXReLeXF': ['PIXReLeXFY1', 'PIXReLeXFY2', 'PIXReLeXFY3', 'PIXReLeXFY4', 'PIXReLeXFY5', 'PIXReLeXFY6'], 'PIXReRiXA': ['PIXReRiXAY1', 'PIXReRiXAY2', 'PIXReRiXAY3', 'PIXReRiXAY4', 'PIXReRiXAY5', 'PIXReRiXAY6'], 'PIXReRiXB': ['PIXReRiXBY1', 'PIXReRiXBY2', 'PIXReRiXBY3', 'PIXReRiXBY4', 'PIXReRiXBY5', 'PIXReRiXBY6'], 'PIXReLeXD': ['PIXReLeXDY1', 'PIXReLeXDY2', 'PIXReLeXDY3', 'PIXReLeXDY4', 'PIXReLeXDY5', 'PIXReLeXDY6'], 'PIXReLeXE': ['PIXReLeXEY1', 'PIXReLeXEY2', 'PIXReLeXEY3', 'PIXReLeXEY4', 'PIXReLeXEY5', 'PIXReLeXEY6'], 'PIXReRiXE': ['PIXReRiXEY1', 'PIXReRiXEY2', 'PIXReRiXEY3', 'PIXReRiXEY4', 'PIXReRiXEY5', 'PIXReRiXEY6'], 'PIXReRiXC': ['PIXReRiXCY1', 'PIXReRiXCY2', 'PIXReRiXCY3', 'PIXReRiXCY4', 'PIXReRiXCY5', 'PIXReRiXCY6'], 'PIXReRiXD': ['PIXReRiXDY1', 'PIXReRiXDY2', 'PIXReRiXDY3', 'PIXReRiXDY4', 'PIXReRiXDY5', 'PIXReRiXDY6']}
    sig_group_dataid_dict = {}

    class PIXReRiXEY6:
        sig_name = "PIXReRiXEY6"
        sig_start_bit = 372
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 372
        bmuws_info = [(46, 0b00011111, 0b11100000, 5, 0), (47, 0b11000000, 0b00111111, 2, 6)]

    class PIXReLeXFY4:
        sig_name = "PIXReLeXFY4"
        sig_start_bit = 148
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 148
        bmuws_info = [(18, 0b00011111, 0b11100000, 5, 0), (19, 0b11000000, 0b00111111, 2, 6)]

    class PIXReRiXCY1:
        sig_name = "PIXReRiXCY1"
        sig_start_bit = 251
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 251
        bmuws_info = [(31, 0b00001111, 0b11110000, 4, 0), (32, 0b11100000, 0b00011111, 3, 5)]

    class PIXReRiXFY1:
        sig_name = "PIXReRiXFY1"
        sig_start_bit = 381
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 381
        bmuws_info = [(47, 0b00111111, 0b11000000, 6, 0), (48, 0b10000000, 0b01111111, 1, 7)]

    class PIXReLeXDY4:
        sig_name = "PIXReLeXDY4"
        sig_start_bit = 56
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 56
        bmuws_info = [(7, 0b00000001, 0b11111110, 1, 0), (8, 0b11111100, 0b00000011, 6, 2)]

    class PIXReLeXEY3:
        sig_name = "PIXReLeXEY3"
        sig_start_bit = 101
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 101
        bmuws_info = [(12, 0b00111111, 0b11000000, 6, 0), (13, 0b10000000, 0b01111111, 1, 7)]

    class PIXReRiXDY1:
        sig_name = "PIXReRiXDY1"
        sig_start_bit = 289
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 289
        bmuws_info = [(36, 0b00000011, 0b11111100, 2, 0), (37, 0b11111000, 0b00000111, 5, 3)]

    class PIXReRiXDY4:
        sig_name = "PIXReRiXDY4"
        sig_start_bit = 316
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 316
        bmuws_info = [(39, 0b00011111, 0b11100000, 5, 0), (40, 0b11000000, 0b00111111, 2, 6)]

    class PIXReRiXCY5:
        sig_name = "PIXReRiXCY5"
        sig_start_bit = 287
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 287
        byte = 35
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXReLeXCY6:
        sig_name = "PIXReLeXCY6"
        sig_start_bit = 36
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 36
        bmuws_info = [(4, 0b00011111, 0b11100000, 5, 0), (5, 0b11000000, 0b00111111, 2, 6)]

    class PIXReLeXC_UB:
        sig_name = "PIXReLeXC_UB"
        sig_start_bit = 431
        update_id_bit = 431
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
        startbit = 431
        byte = 53
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class PIXReRiXCY2:
        sig_name = "PIXReRiXCY2"
        sig_start_bit = 260
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 260
        bmuws_info = [(32, 0b00011111, 0b11100000, 5, 0), (33, 0b11000000, 0b00111111, 2, 6)]

    class PIXReRiXF_UB:
        sig_name = "PIXReRiXF_UB"
        sig_start_bit = 438
        update_id_bit = 438
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
        startbit = 438
        byte = 54
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class PIXReLeXF_UB:
        sig_name = "PIXReLeXF_UB"
        sig_start_bit = 428
        update_id_bit = 428
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
        startbit = 428
        byte = 53
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class PIXReRiXAY4:
        sig_name = "PIXReRiXAY4"
        sig_start_bit = 186
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 186
        bmuws_info = [(23, 0b00000111, 0b11111000, 3, 0), (24, 0b11110000, 0b00001111, 4, 4)]

    class PIXReLeXDY5:
        sig_name = "PIXReLeXDY5"
        sig_start_bit = 65
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 65
        bmuws_info = [(8, 0b00000011, 0b11111100, 2, 0), (9, 0b11111000, 0b00000111, 5, 3)]

    class PIXReLeXEY1:
        sig_name = "PIXReLeXEY1"
        sig_start_bit = 83
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 83
        bmuws_info = [(10, 0b00001111, 0b11110000, 4, 0), (11, 0b11100000, 0b00011111, 3, 5)]

    class PIXReLeXDY6:
        sig_name = "PIXReLeXDY6"
        sig_start_bit = 74
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 74
        bmuws_info = [(9, 0b00000111, 0b11111000, 3, 0), (10, 0b11110000, 0b00001111, 4, 4)]

    class PIXReRiXBY5:
        sig_name = "PIXReRiXBY5"
        sig_start_bit = 233
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 233
        bmuws_info = [(29, 0b00000011, 0b11111100, 2, 0), (30, 0b11111000, 0b00000111, 5, 3)]

    class PIXReRiXBY6:
        sig_name = "PIXReRiXBY6"
        sig_start_bit = 242
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 242
        bmuws_info = [(30, 0b00000111, 0b11111000, 3, 0), (31, 0b11110000, 0b00001111, 4, 4)]

    class PIXReRiXFY2:
        sig_name = "PIXReRiXFY2"
        sig_start_bit = 390
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 390
        byte = 48
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class PIXReLeXCY4:
        sig_name = "PIXReLeXCY4"
        sig_start_bit = 18
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 18
        bmuws_info = [(2, 0b00000111, 0b11111000, 3, 0), (3, 0b11110000, 0b00001111, 4, 4)]

    class PIXReLeXFY2:
        sig_name = "PIXReLeXFY2"
        sig_start_bit = 130
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 130
        bmuws_info = [(16, 0b00000111, 0b11111000, 3, 0), (17, 0b11110000, 0b00001111, 4, 4)]

    class PIXReRiXCY4:
        sig_name = "PIXReRiXCY4"
        sig_start_bit = 278
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 278
        byte = 34
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class PIXReLeXEY5:
        sig_name = "PIXReLeXEY5"
        sig_start_bit = 119
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 119
        byte = 14
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXReRiXCY6:
        sig_name = "PIXReRiXCY6"
        sig_start_bit = 280
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 280
        bmuws_info = [(35, 0b00000001, 0b11111110, 1, 0), (36, 0b11111100, 0b00000011, 6, 2)]

    class PIXReLeXFY3:
        sig_name = "PIXReLeXFY3"
        sig_start_bit = 139
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 139
        bmuws_info = [(17, 0b00001111, 0b11110000, 4, 0), (18, 0b11100000, 0b00011111, 3, 5)]

    class PIXReLeXFY5:
        sig_name = "PIXReLeXFY5"
        sig_start_bit = 157
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 157
        bmuws_info = [(19, 0b00111111, 0b11000000, 6, 0), (20, 0b10000000, 0b01111111, 1, 7)]

    class PIXReRiXEY2:
        sig_name = "PIXReRiXEY2"
        sig_start_bit = 336
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 336
        bmuws_info = [(42, 0b00000001, 0b11111110, 1, 0), (43, 0b11111100, 0b00000011, 6, 2)]

    class PIXReRiXEY4:
        sig_name = "PIXReRiXEY4"
        sig_start_bit = 354
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 354
        bmuws_info = [(44, 0b00000111, 0b11111000, 3, 0), (45, 0b11110000, 0b00001111, 4, 4)]

    class PIXReLeXFY6:
        sig_name = "PIXReLeXFY6"
        sig_start_bit = 166
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 166
        byte = 20
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class PIXReRiXBY1:
        sig_name = "PIXReRiXBY1"
        sig_start_bit = 213
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 213
        bmuws_info = [(26, 0b00111111, 0b11000000, 6, 0), (27, 0b10000000, 0b01111111, 1, 7)]

    class PIXReRiXFY4:
        sig_name = "PIXReRiXFY4"
        sig_start_bit = 407
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 407
        byte = 50
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXReRiXAY3:
        sig_name = "PIXReRiXAY3"
        sig_start_bit = 177
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 177
        bmuws_info = [(22, 0b00000011, 0b11111100, 2, 0), (23, 0b11111000, 0b00000111, 5, 3)]

    class PIXReRiXBY4:
        sig_name = "PIXReRiXBY4"
        sig_start_bit = 224
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 224
        bmuws_info = [(28, 0b00000001, 0b11111110, 1, 0), (29, 0b11111100, 0b00000011, 6, 2)]

    class PIXReRiXEY5:
        sig_name = "PIXReRiXEY5"
        sig_start_bit = 363
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 363
        bmuws_info = [(45, 0b00001111, 0b11110000, 4, 0), (46, 0b11100000, 0b00011111, 3, 5)]

    class PIXReRiXBY3:
        sig_name = "PIXReRiXBY3"
        sig_start_bit = 231
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 231
        byte = 28
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXReRiXA_UB:
        sig_name = "PIXReRiXA_UB"
        sig_start_bit = 427
        update_id_bit = 427
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
        startbit = 427
        byte = 53
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class PIXReRiXB_UB:
        sig_name = "PIXReRiXB_UB"
        sig_start_bit = 426
        update_id_bit = 426
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
        startbit = 426
        byte = 53
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class PIXReLeXCY1:
        sig_name = "PIXReLeXCY1"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
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

    class PIXReLeXCY5:
        sig_name = "PIXReLeXCY5"
        sig_start_bit = 27
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 27
        bmuws_info = [(3, 0b00001111, 0b11110000, 4, 0), (4, 0b11100000, 0b00011111, 3, 5)]

    class PIXReLeXEY4:
        sig_name = "PIXReLeXEY4"
        sig_start_bit = 110
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 110
        byte = 13
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class PIXReLeXD_UB:
        sig_name = "PIXReLeXD_UB"
        sig_start_bit = 430
        update_id_bit = 430
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
        startbit = 430
        byte = 53
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class PIXReRiXDY5:
        sig_name = "PIXReRiXDY5"
        sig_start_bit = 325
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 325
        bmuws_info = [(40, 0b00111111, 0b11000000, 6, 0), (41, 0b10000000, 0b01111111, 1, 7)]

    class PIXReRiXDY2:
        sig_name = "PIXReRiXDY2"
        sig_start_bit = 298
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 298
        bmuws_info = [(37, 0b00000111, 0b11111000, 3, 0), (38, 0b11110000, 0b00001111, 4, 4)]

    class PIXReLeXDY3:
        sig_name = "PIXReLeXDY3"
        sig_start_bit = 63
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
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

    class PIXReRiXDY6:
        sig_name = "PIXReRiXDY6"
        sig_start_bit = 334
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 334
        byte = 41
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class PIXReRiXBY2:
        sig_name = "PIXReRiXBY2"
        sig_start_bit = 222
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 222
        byte = 27
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class PIXReRiXCY3:
        sig_name = "PIXReRiXCY3"
        sig_start_bit = 269
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 269
        bmuws_info = [(33, 0b00111111, 0b11000000, 6, 0), (34, 0b10000000, 0b01111111, 1, 7)]

    class PIXReRiXEY1:
        sig_name = "PIXReRiXEY1"
        sig_start_bit = 343
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 343
        byte = 42
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXReRiXAY5:
        sig_name = "PIXReRiXAY5"
        sig_start_bit = 195
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 195
        bmuws_info = [(24, 0b00001111, 0b11110000, 4, 0), (25, 0b11100000, 0b00011111, 3, 5)]

    class PIXReRiXAY1:
        sig_name = "PIXReRiXAY1"
        sig_start_bit = 175
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 175
        byte = 21
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXReLeXFY1:
        sig_name = "PIXReLeXFY1"
        sig_start_bit = 121
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 121
        bmuws_info = [(15, 0b00000011, 0b11111100, 2, 0), (16, 0b11111000, 0b00000111, 5, 3)]

    class PIXReRiXFY3:
        sig_name = "PIXReRiXFY3"
        sig_start_bit = 399
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 399
        byte = 49
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXReRiXEY3:
        sig_name = "PIXReRiXEY3"
        sig_start_bit = 345
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 345
        bmuws_info = [(43, 0b00000011, 0b11111100, 2, 0), (44, 0b11111000, 0b00000111, 5, 3)]

    class PIXReRiXFY5:
        sig_name = "PIXReRiXFY5"
        sig_start_bit = 415
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 415
        byte = 51
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXReLeXE_UB:
        sig_name = "PIXReLeXE_UB"
        sig_start_bit = 429
        update_id_bit = 429
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
        startbit = 429
        byte = 53
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class PIXReRiXDY3:
        sig_name = "PIXReRiXDY3"
        sig_start_bit = 307
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 307
        bmuws_info = [(38, 0b00001111, 0b11110000, 4, 0), (39, 0b11100000, 0b00011111, 3, 5)]

    class PIXReRiXFY6:
        sig_name = "PIXReRiXFY6"
        sig_start_bit = 423
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 423
        byte = 52
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXReRiXAY6:
        sig_name = "PIXReRiXAY6"
        sig_start_bit = 204
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 204
        bmuws_info = [(25, 0b00011111, 0b11100000, 5, 0), (26, 0b11000000, 0b00111111, 2, 6)]

    class PIXReLeXCY3:
        sig_name = "PIXReLeXCY3"
        sig_start_bit = 9
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 9
        bmuws_info = [(1, 0b00000011, 0b11111100, 2, 0), (2, 0b11111000, 0b00000111, 5, 3)]

    class PIXReLeXCY2:
        sig_name = "PIXReLeXCY2"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 0
        bmuws_info = [(0, 0b00000001, 0b11111110, 1, 0), (1, 0b11111100, 0b00000011, 6, 2)]

    class PIXReRiXAY2:
        sig_name = "PIXReRiXAY2"
        sig_start_bit = 168
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 168
        bmuws_info = [(21, 0b00000001, 0b11111110, 1, 0), (22, 0b11111100, 0b00000011, 6, 2)]

    class PIXReRiXE_UB:
        sig_name = "PIXReRiXE_UB"
        sig_start_bit = 439
        update_id_bit = 439
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
        startbit = 439
        byte = 54
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class PIXReLeXDY1:
        sig_name = "PIXReLeXDY1"
        sig_start_bit = 45
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 45
        bmuws_info = [(5, 0b00111111, 0b11000000, 6, 0), (6, 0b10000000, 0b01111111, 1, 7)]

    class PIXReRiXC_UB:
        sig_name = "PIXReRiXC_UB"
        sig_start_bit = 425
        update_id_bit = 425
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
        startbit = 425
        byte = 53
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class PIXReLeXEY6:
        sig_name = "PIXReLeXEY6"
        sig_start_bit = 112
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 112
        bmuws_info = [(14, 0b00000001, 0b11111110, 1, 0), (15, 0b11111100, 0b00000011, 6, 2)]

    class PIXReLeXDY2:
        sig_name = "PIXReLeXDY2"
        sig_start_bit = 54
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 54
        byte = 6
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class PIXReLeXEY2:
        sig_name = "PIXReLeXEY2"
        sig_start_bit = 92
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 92
        bmuws_info = [(11, 0b00011111, 0b11100000, 5, 0), (12, 0b11000000, 0b00111111, 2, 6)]

    class PIXReRiXD_UB:
        sig_name = "PIXReRiXD_UB"
        sig_start_bit = 424
        update_id_bit = 424
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
        startbit = 424
        byte = 53
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0


class HcmlBodyExposedCANNmFr:
    msg_name = "HcmlBodyExposedCANNmFr"
    msg_id = 1329
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "HCML"
    rx_nodes = ['RCMM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class CemBodyExpoFr45:
    msg_name = "CemBodyExpoFr45"
    msg_id = 612
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.065
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCML', 'HCMR']
    sig_group_dict = {'BrkPedlVal': ['BrkPedlValBrkPedlVal', 'BrkPedlValQf']}
    sig_group_dataid_dict = {}

    class BrkPedlValQf:
        sig_name = "BrkPedlValQf"
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
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 41
        byte = 5
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class BrkPedlValBrkPedlVal:
        sig_name = "BrkPedlValBrkPedlVal"
        sig_start_bit = 54
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
        startbit = 54
        bmuws_info = [(6, 0b01111111, 0b10000000, 7, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class BrkPedlVal_UB:
        sig_name = "BrkPedlVal_UB"
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


class CemBodyExpoCommonFr01:
    msg_name = "CemBodyExpoCommonFr01"
    msg_id = 82
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCML', 'CCM', 'HCMR']
    sig_group_dict = {'SteerWhlSnsr': ['SteerWhlSnsrAg', 'SteerWhlSnsrAgSpd', 'SteerWhlSnsrChks', 'SteerWhlSnsrCntr', 'SteerWhlSnsrQf']}
    sig_group_dataid_dict = {'SteerWhlSnsr': 51}

    class SteerWhlSnsrCntr:
        sig_name = "SteerWhlSnsrCntr"
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

    class SteerWhlSnsrAg:
        sig_name = "SteerWhlSnsrAg"
        sig_start_bit = 6
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
        startbit = 6
        bmuws_info = [(0, 0b01111111, 0b10000000, 7, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class SteerWhlSnsrChks:
        sig_name = "SteerWhlSnsrChks"
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

    class SteerWhlSnsrAgSpd:
        sig_name = "SteerWhlSnsrAgSpd"
        sig_start_bit = 21
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
        startbit = 21
        bmuws_info = [(2, 0b00111111, 0b11000000, 6, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class SteerWhlSnsrQf:
        sig_name = "SteerWhlSnsrQf"
        sig_start_bit = 23
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
        startbit = 23
        byte = 2
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class SteerWhlSnsr_UB:
        sig_name = "SteerWhlSnsr_UB"
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

    class LiOprnMod:
        sig_name = "LiOprnMod"
        sig_start_bit = 43
        update_id_bit = 41
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LiOperMod_Night': 0, 'LiOperMod_Day': 1, 'LiOperMod_Twli': 2, 'LiOperMod_Tnl': 3}
        compute_method = None
        length = 2
        startbit = 43
        byte = 5
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2


class RcmlBodyExposedCANNmFr:
    msg_name = "RcmlBodyExposedCANNmFr"
    msg_id = 1331
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "RCML"
    rx_nodes = ['HCMR']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class HcmlToBgmBodyExpoDiagRespFrame:
    msg_name = "HcmlToBgmBodyExpoDiagRespFrame"
    msg_id = 1715
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "HCML"
    rx_nodes = ['BGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class RcmrBodyExposedCANeNmFr:
    msg_name = "RcmrBodyExposedCANeNmFr"
    msg_id = 1332
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "RCMR"
    rx_nodes = ['HCML']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class BgmBodyExposedCANFr05:
    msg_name = "BgmBodyExposedCANFr05"
    msg_id = 160
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 64
    tx_node = "BGM"
    rx_nodes = ['RCMM']
    sig_group_dict = {'CrossReMidX1': ['CrossReMidX1Y1', 'CrossReMidX1Y10', 'CrossReMidX1Y11', 'CrossReMidX1Y12', 'CrossReMidX1Y13', 'CrossReMidX1Y14', 'CrossReMidX1Y15', 'CrossReMidX1Y16', 'CrossReMidX1Y17', 'CrossReMidX1Y18', 'CrossReMidX1Y19', 'CrossReMidX1Y2', 'CrossReMidX1Y20', 'CrossReMidX1Y21', 'CrossReMidX1Y22', 'CrossReMidX1Y23', 'CrossReMidX1Y24', 'CrossReMidX1Y25', 'CrossReMidX1Y26', 'CrossReMidX1Y27', 'CrossReMidX1Y28', 'CrossReMidX1Y29', 'CrossReMidX1Y3', 'CrossReMidX1Y30', 'CrossReMidX1Y31', 'CrossReMidX1Y32', 'CrossReMidX1Y33', 'CrossReMidX1Y34', 'CrossReMidX1Y35', 'CrossReMidX1Y36', 'CrossReMidX1Y37', 'CrossReMidX1Y38', 'CrossReMidX1Y39', 'CrossReMidX1Y4', 'CrossReMidX1Y40', 'CrossReMidX1Y41', 'CrossReMidX1Y42', 'CrossReMidX1Y43', 'CrossReMidX1Y44', 'CrossReMidX1Y45', 'CrossReMidX1Y46', 'CrossReMidX1Y47', 'CrossReMidX1Y48', 'CrossReMidX1Y49', 'CrossReMidX1Y5', 'CrossReMidX1Y50', 'CrossReMidX1Y51', 'CrossReMidX1Y52', 'CrossReMidX1Y53', 'CrossReMidX1Y54', 'CrossReMidX1Y55', 'CrossReMidX1Y56', 'CrossReMidX1Y57', 'CrossReMidX1Y58', 'CrossReMidX1Y59', 'CrossReMidX1Y6', 'CrossReMidX1Y60', 'CrossReMidX1Y7', 'CrossReMidX1Y8', 'CrossReMidX1Y9']}
    sig_group_dataid_dict = {}

    class CrossReMidX1Y1:
        sig_name = "CrossReMidX1Y1"
        sig_start_bit = 6
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 6
        byte = 0
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReMidX1Y44:
        sig_name = "CrossReMidX1Y44"
        sig_start_bit = 350
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 350
        byte = 43
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReMidX1Y20:
        sig_name = "CrossReMidX1Y20"
        sig_start_bit = 158
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 158
        byte = 19
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReMidX1Y28:
        sig_name = "CrossReMidX1Y28"
        sig_start_bit = 222
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 222
        byte = 27
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReMidX1Y31:
        sig_name = "CrossReMidX1Y31"
        sig_start_bit = 246
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 246
        byte = 30
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReMidX1Y17:
        sig_name = "CrossReMidX1Y17"
        sig_start_bit = 134
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 134
        byte = 16
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReMidX1Y36:
        sig_name = "CrossReMidX1Y36"
        sig_start_bit = 286
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 286
        byte = 35
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReMidX1Y14:
        sig_name = "CrossReMidX1Y14"
        sig_start_bit = 110
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 110
        byte = 13
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReMidX1Y24:
        sig_name = "CrossReMidX1Y24"
        sig_start_bit = 190
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 190
        byte = 23
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReMidX1Y25:
        sig_name = "CrossReMidX1Y25"
        sig_start_bit = 198
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 198
        byte = 24
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReMidX1Y3:
        sig_name = "CrossReMidX1Y3"
        sig_start_bit = 22
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 22
        byte = 2
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReMidX1Y33:
        sig_name = "CrossReMidX1Y33"
        sig_start_bit = 262
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 262
        byte = 32
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReMidX1Y6:
        sig_name = "CrossReMidX1Y6"
        sig_start_bit = 46
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 46
        byte = 5
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReMidX1Y7:
        sig_name = "CrossReMidX1Y7"
        sig_start_bit = 54
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 54
        byte = 6
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReMidX1Y5:
        sig_name = "CrossReMidX1Y5"
        sig_start_bit = 38
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 38
        byte = 4
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReMidX1Y16:
        sig_name = "CrossReMidX1Y16"
        sig_start_bit = 126
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 126
        byte = 15
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReMidX1Y45:
        sig_name = "CrossReMidX1Y45"
        sig_start_bit = 358
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 358
        byte = 44
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReMidX1Y46:
        sig_name = "CrossReMidX1Y46"
        sig_start_bit = 366
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 366
        byte = 45
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReMidX1Y2:
        sig_name = "CrossReMidX1Y2"
        sig_start_bit = 14
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 14
        byte = 1
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReMidX1Y41:
        sig_name = "CrossReMidX1Y41"
        sig_start_bit = 326
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 326
        byte = 40
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReMidX1Y11:
        sig_name = "CrossReMidX1Y11"
        sig_start_bit = 86
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 86
        byte = 10
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReMidX1Y47:
        sig_name = "CrossReMidX1Y47"
        sig_start_bit = 374
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 374
        byte = 46
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReMidX1Y12:
        sig_name = "CrossReMidX1Y12"
        sig_start_bit = 94
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 94
        byte = 11
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReMidX1Y52:
        sig_name = "CrossReMidX1Y52"
        sig_start_bit = 414
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 414
        byte = 51
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReMidX1Y55:
        sig_name = "CrossReMidX1Y55"
        sig_start_bit = 438
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 438
        byte = 54
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReMidX1Y50:
        sig_name = "CrossReMidX1Y50"
        sig_start_bit = 398
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 398
        byte = 49
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReMidX1Y37:
        sig_name = "CrossReMidX1Y37"
        sig_start_bit = 294
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 294
        byte = 36
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReMidX1Y34:
        sig_name = "CrossReMidX1Y34"
        sig_start_bit = 270
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 270
        byte = 33
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReMidX1Y54:
        sig_name = "CrossReMidX1Y54"
        sig_start_bit = 430
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 430
        byte = 53
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReMidX1Y48:
        sig_name = "CrossReMidX1Y48"
        sig_start_bit = 382
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 382
        byte = 47
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReMidX1Y57:
        sig_name = "CrossReMidX1Y57"
        sig_start_bit = 454
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 454
        byte = 56
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReMidX1Y22:
        sig_name = "CrossReMidX1Y22"
        sig_start_bit = 174
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 174
        byte = 21
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReMidX1Y10:
        sig_name = "CrossReMidX1Y10"
        sig_start_bit = 78
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 78
        byte = 9
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReMidX1Y15:
        sig_name = "CrossReMidX1Y15"
        sig_start_bit = 118
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 118
        byte = 14
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReMidX1Y53:
        sig_name = "CrossReMidX1Y53"
        sig_start_bit = 422
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 422
        byte = 52
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReMidX1Y30:
        sig_name = "CrossReMidX1Y30"
        sig_start_bit = 238
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 238
        byte = 29
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReMidX1Y18:
        sig_name = "CrossReMidX1Y18"
        sig_start_bit = 142
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 142
        byte = 17
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReMidX1Y38:
        sig_name = "CrossReMidX1Y38"
        sig_start_bit = 302
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 302
        byte = 37
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReMidX1Y23:
        sig_name = "CrossReMidX1Y23"
        sig_start_bit = 182
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 182
        byte = 22
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReMidX1Y40:
        sig_name = "CrossReMidX1Y40"
        sig_start_bit = 318
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 318
        byte = 39
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReMidX1Y39:
        sig_name = "CrossReMidX1Y39"
        sig_start_bit = 310
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 310
        byte = 38
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReMidX1Y59:
        sig_name = "CrossReMidX1Y59"
        sig_start_bit = 470
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 470
        byte = 58
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReMidX1Y13:
        sig_name = "CrossReMidX1Y13"
        sig_start_bit = 102
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 102
        byte = 12
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReMidX1Y27:
        sig_name = "CrossReMidX1Y27"
        sig_start_bit = 214
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 214
        byte = 26
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReMidX1Y56:
        sig_name = "CrossReMidX1Y56"
        sig_start_bit = 446
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 446
        byte = 55
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReMidX1Y26:
        sig_name = "CrossReMidX1Y26"
        sig_start_bit = 206
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 206
        byte = 25
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReMidX1Y42:
        sig_name = "CrossReMidX1Y42"
        sig_start_bit = 334
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 334
        byte = 41
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReMidX1Y58:
        sig_name = "CrossReMidX1Y58"
        sig_start_bit = 462
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 462
        byte = 57
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReMidX1Y43:
        sig_name = "CrossReMidX1Y43"
        sig_start_bit = 342
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 342
        byte = 42
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReMidX1Y8:
        sig_name = "CrossReMidX1Y8"
        sig_start_bit = 62
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 62
        byte = 7
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReMidX1Y21:
        sig_name = "CrossReMidX1Y21"
        sig_start_bit = 166
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 166
        byte = 20
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReMidX1Y35:
        sig_name = "CrossReMidX1Y35"
        sig_start_bit = 278
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 278
        byte = 34
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReMidX1Y9:
        sig_name = "CrossReMidX1Y9"
        sig_start_bit = 70
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
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

    class CrossReMidX1Y60:
        sig_name = "CrossReMidX1Y60"
        sig_start_bit = 478
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 478
        byte = 59
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReMidX1Y19:
        sig_name = "CrossReMidX1Y19"
        sig_start_bit = 150
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 150
        byte = 18
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReMidX1Y51:
        sig_name = "CrossReMidX1Y51"
        sig_start_bit = 406
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 406
        byte = 50
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReMidX1Y29:
        sig_name = "CrossReMidX1Y29"
        sig_start_bit = 230
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 230
        byte = 28
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReMidX1Y32:
        sig_name = "CrossReMidX1Y32"
        sig_start_bit = 254
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 254
        byte = 31
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReMidX1Y49:
        sig_name = "CrossReMidX1Y49"
        sig_start_bit = 390
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 390
        byte = 48
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CrossReMidX1Y4:
        sig_name = "CrossReMidX1Y4"
        sig_start_bit = 30
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 30
        byte = 3
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0


class CemBodyExpoCommonFr02:
    msg_name = "CemBodyExpoCommonFr02"
    msg_id = 768
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.045
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCML', 'HCMR']
    sig_group_dict = {'BrkPedlrRat': ['BrkPedlrRatPerc', 'BrkPedlrRatQf']}
    sig_group_dataid_dict = {}

    class BrkPedlrRatQf:
        sig_name = "BrkPedlrRatQf"
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
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 63
        byte = 7
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class BrkPedlrRatPerc:
        sig_name = "BrkPedlrRatPerc"
        sig_start_bit = 46
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
        startbit = 46
        bmuws_info = [(5, 0b01111111, 0b10000000, 7, 0), (6, 0b11111111, 0b00000000, 8, 0)]

    class BrkPedlrRat_UB:
        sig_name = "BrkPedlrRat_UB"
        sig_start_bit = 47
        update_id_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class YawRateReqdByDrvr:
        sig_name = "YawRateReqdByDrvr"
        sig_start_bit = 7
        update_id_bit = 21
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
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0)]


class EtctoHcmrXCPFr01:
    msg_name = "EtctoHcmrXCPFr01"
    msg_id = 1428
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CCM"
    rx_nodes = ['HCMR']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class BgmToHcmrBodyExpoDiagReqFrame:
    msg_name = "BgmToHcmrBodyExpoDiagReqFrame"
    msg_id = 1972
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class CemBodyExpoDevDiagFr01:
    msg_name = "CemBodyExpoDevDiagFr01"
    msg_id = 1432
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['CCM']
    sig_group_dict = {'CEMdevelpsignalgroupresp': ['CEMdevelpsignalgrouprespFunctiondevpsignalgroup1', 'CEMdevelpsignalgrouprespFunctiondevpsignalgroup2', 'CEMdevelpsignalgrouprespFunctiondevpsignalgroup3', 'CEMdevelpsignalgrouprespFunctiondevpsignalgroup4', 'CEMdevelpsignalgrouprespFunctiondevpsignalgroup5', 'CEMdevelpsignalgrouprespFunctiondevpsignalgroup6', 'CEMdevelpsignalgrouprespFunctiondevpsignalgroup7', 'CEMdevelpsignalgrouprespFunctiondevpsignalgroup8']}
    sig_group_dataid_dict = {}

    class CEMdevelpsignalgrouprespFunctiondevpsignalgroup7:
        sig_name = "CEMdevelpsignalgrouprespFunctiondevpsignalgroup7"
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

    class CEMdevelpsignalgrouprespFunctiondevpsignalgroup6:
        sig_name = "CEMdevelpsignalgrouprespFunctiondevpsignalgroup6"
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

    class CEMdevelpsignalgrouprespFunctiondevpsignalgroup2:
        sig_name = "CEMdevelpsignalgrouprespFunctiondevpsignalgroup2"
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

    class CEMdevelpsignalgrouprespFunctiondevpsignalgroup4:
        sig_name = "CEMdevelpsignalgrouprespFunctiondevpsignalgroup4"
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

    class CEMdevelpsignalgrouprespFunctiondevpsignalgroup3:
        sig_name = "CEMdevelpsignalgrouprespFunctiondevpsignalgroup3"
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

    class CEMdevelpsignalgrouprespFunctiondevpsignalgroup8:
        sig_name = "CEMdevelpsignalgrouprespFunctiondevpsignalgroup8"
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

    class CEMdevelpsignalgrouprespFunctiondevpsignalgroup5:
        sig_name = "CEMdevelpsignalgrouprespFunctiondevpsignalgroup5"
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

    class CEMdevelpsignalgrouprespFunctiondevpsignalgroup1:
        sig_name = "CEMdevelpsignalgrouprespFunctiondevpsignalgroup1"
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


class CemBodyExpoDevFr02:
    msg_name = "CemBodyExpoDevFr02"
    msg_id = 1431
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['CCM']
    sig_group_dict = {'CEMdevelpsignalgroupcheck': ['CEMdevelpsignalgroupcheckFunctiondevpsignalgroup1', 'CEMdevelpsignalgroupcheckFunctiondevpsignalgroup2', 'CEMdevelpsignalgroupcheckFunctiondevpsignalgroup3', 'CEMdevelpsignalgroupcheckFunctiondevpsignalgroup4', 'CEMdevelpsignalgroupcheckFunctiondevpsignalgroup5', 'CEMdevelpsignalgroupcheckFunctiondevpsignalgroup6', 'CEMdevelpsignalgroupcheckFunctiondevpsignalgroup7', 'CEMdevelpsignalgroupcheckFunctiondevpsignalgroup8']}
    sig_group_dataid_dict = {}

    class CEMdevelpsignalgroupcheckFunctiondevpsignalgroup6:
        sig_name = "CEMdevelpsignalgroupcheckFunctiondevpsignalgroup6"
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

    class CEMdevelpsignalgroupcheckFunctiondevpsignalgroup3:
        sig_name = "CEMdevelpsignalgroupcheckFunctiondevpsignalgroup3"
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

    class CEMdevelpsignalgroupcheckFunctiondevpsignalgroup7:
        sig_name = "CEMdevelpsignalgroupcheckFunctiondevpsignalgroup7"
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

    class CEMdevelpsignalgroupcheckFunctiondevpsignalgroup2:
        sig_name = "CEMdevelpsignalgroupcheckFunctiondevpsignalgroup2"
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

    class CEMdevelpsignalgroupcheckFunctiondevpsignalgroup4:
        sig_name = "CEMdevelpsignalgroupcheckFunctiondevpsignalgroup4"
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

    class CEMdevelpsignalgroupcheckFunctiondevpsignalgroup5:
        sig_name = "CEMdevelpsignalgroupcheckFunctiondevpsignalgroup5"
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

    class CEMdevelpsignalgroupcheckFunctiondevpsignalgroup1:
        sig_name = "CEMdevelpsignalgroupcheckFunctiondevpsignalgroup1"
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

    class CEMdevelpsignalgroupcheckFunctiondevpsignalgroup8:
        sig_name = "CEMdevelpsignalgroupcheckFunctiondevpsignalgroup8"
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


class CemBodyExpoCommonFr09:
    msg_name = "CemBodyExpoCommonFr09"
    msg_id = 387
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RCML', 'RCMR', 'RCMM', 'HCMR', 'HCML']
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


class BgmToRcmmBodyExpoDiagReqFrame:
    msg_name = "BgmToRcmmBodyExpoDiagReqFrame"
    msg_id = 1975
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RCMM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class CEMBodyExpoCommonFr06:
    msg_name = "CEMBodyExpoCommonFr06"
    msg_id = 512
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RCML', 'RCMR', 'RCMM', 'HCMR', 'HCML']
    sig_group_dict = {'VehBattU': ['VehBattUSysU', 'VehBattUSysUQf']}
    sig_group_dataid_dict = {}

    class BkpOfDstTrvld:
        sig_name = "BkpOfDstTrvld"
        sig_start_bit = 23
        update_id_bit = 46
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
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111000, 0b00000111, 5, 3)]

    class VehBattUSysU:
        sig_name = "VehBattUSysU"
        sig_start_bit = 55
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
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehBattU_UB:
        sig_name = "VehBattU_UB"
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

    class ExtrLiRlyPwrDwn:
        sig_name = "ExtrLiRlyPwrDwn"
        sig_start_bit = 6
        update_id_bit = 7
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
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VehBattUSysUQf:
        sig_name = "VehBattUSysUQf"
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
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 41
        byte = 5
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0


class BgmBodyExposedCANNmFr:
    msg_name = "BgmBodyExposedCANNmFr"
    msg_id = 1322
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RCMR']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class RcmrBodyExpoFr01:
    msg_name = "RcmrBodyExpoFr01"
    msg_id = 608
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 8
    tx_node = "RCMR"
    rx_nodes = ['S2SReceiver', 'BGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class StsOfLedRvsgLampRi1:
        sig_name = "StsOfLedRvsgLampRi1"
        sig_start_bit = 15
        update_id_bit = 28
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 15
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class StsOfLedTurnIndcrRi1:
        sig_name = "StsOfLedTurnIndcrRi1"
        sig_start_bit = 25
        update_id_bit = 26
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 25
        byte = 3
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class StsOfLedReLampRi2:
        sig_name = "StsOfLedReLampRi2"
        sig_start_bit = 34
        update_id_bit = 32
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 34
        byte = 4
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class StsOfLedStopLampRi1:
        sig_name = "StsOfLedStopLampRi1"
        sig_start_bit = 23
        update_id_bit = 27
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 23
        byte = 2
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class StsOfLedReLampRi1:
        sig_name = "StsOfLedReLampRi1"
        sig_start_bit = 13
        update_id_bit = 29
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 13
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class StsOfLedReLampRi:
        sig_name = "StsOfLedReLampRi"
        sig_start_bit = 37
        update_id_bit = 35
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 37
        byte = 4
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class StsOfLedPosnLampRi1:
        sig_name = "StsOfLedPosnLampRi1"
        sig_start_bit = 9
        update_id_bit = 31
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 9
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class StsOfLedReWheelLampRi:
        sig_name = "StsOfLedReWheelLampRi"
        sig_start_bit = 47
        update_id_bit = 45
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 47
        byte = 5
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class StsOfRePosnLampRiScopeStore:
        sig_name = "StsOfRePosnLampRiScopeStore"
        sig_start_bit = 44
        update_id_bit = 42
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Sts_Resd': 0, 'Sts_Err': 1, 'Sts_CmplOk': 2, 'Sts_InProgs': 3}
        compute_method = None
        length = 2
        startbit = 44
        byte = 5
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class StsOfLedReFogLampRi1:
        sig_name = "StsOfLedReFogLampRi1"
        sig_start_bit = 11
        update_id_bit = 30
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 11
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2


class HcmrBodyExpoFr04:
    msg_name = "HcmrBodyExpoFr04"
    msg_id = 127
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 8
    tx_node = "HCMR"
    rx_nodes = ['S2SReceiver', 'BGM']
    sig_group_dict = {'StsOfLvlgRi': ['StsOfLvlgRiChks', 'StsOfLvlgRiCntr', 'StsOfLvlgRiStsOfLvlgRi']}
    sig_group_dataid_dict = {}

    class StsOfLvlgRiStsOfLvlgRi:
        sig_name = "StsOfLvlgRiStsOfLvlgRi"
        sig_start_bit = 51
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 51
        byte = 6
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class StsOfLedDaytiRunngLampRi:
        sig_name = "StsOfLedDaytiRunngLampRi"
        sig_start_bit = 13
        update_id_bit = 32
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 13
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class HdlampRiInpSts2:
        sig_name = "HdlampRiInpSts2"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 63
        byte = 7
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class StsOfLvlgRiChks:
        sig_name = "StsOfLvlgRiChks"
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

    class StsOfLedFrntFogLampRi:
        sig_name = "StsOfLedFrntFogLampRi"
        sig_start_bit = 15
        update_id_bit = 31
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 15
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class StsOfSwvlgRi:
        sig_name = "StsOfSwvlgRi"
        sig_start_bit = 7
        update_id_bit = 35
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class StsOfLvlgRi_UB:
        sig_name = "StsOfLvlgRi_UB"
        sig_start_bit = 36
        update_id_bit = 36
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
        startbit = 36
        byte = 4
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class HdlampRiInpSts1:
        sig_name = "HdlampRiInpSts1"
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

    class StsOfLedFrntTurnIndcrRi:
        sig_name = "StsOfLedFrntTurnIndcrRi"
        sig_start_bit = 19
        update_id_bit = 29
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 19
        byte = 2
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class StsOfLvlgRiCntr:
        sig_name = "StsOfLvlgRiCntr"
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

    class StsOfLedFrntPosnLampRi:
        sig_name = "StsOfLedFrntPosnLampRi"
        sig_start_bit = 17
        update_id_bit = 30
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 17
        byte = 2
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0


class CemBodyExpoCommonFr08:
    msg_name = "CemBodyExpoCommonFr08"
    msg_id = 128
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCML', 'HCMR']
    sig_group_dict = {'AmbTRaw': ['AmbTRawAmbTVal', 'AmbTRawQly'], 'AccrPedlRat': ['AccrPedlRatAccrPedlRat', 'AccrPedlRatChks', 'AccrPedlRatCntr'], 'BrkPedlSnsr': ['BrkPedlSnsrChks', 'BrkPedlSnsrCntr', 'BrkPedlSnsrQf', 'BrkPedlSnsrSt']}
    sig_group_dataid_dict = {'AccrPedlRat': 868, 'BrkPedlSnsr': 175}

    class BrkPedlSnsrSt:
        sig_name = "BrkPedlSnsrSt"
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
        sig_value_table = {'PsdNotPsd2_NoInfo1': 0, 'PsdNotPsd2_NotPsd': 1, 'PsdNotPsd2_Psd': 2, 'PsdNotPsd2_NoInfo2': 3}
        compute_method = None
        length = 2
        startbit = 37
        byte = 4
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class BrkPedlSnsrChks:
        sig_name = "BrkPedlSnsrChks"
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

    class BrkPedlSnsrCntr:
        sig_name = "BrkPedlSnsrCntr"
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

    class AmbTRawQly:
        sig_name = "AmbTRawQly"
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

    class AmbTRaw_UB:
        sig_name = "AmbTRaw_UB"
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

    class BrkPedlSnsrQf:
        sig_name = "BrkPedlSnsrQf"
        sig_start_bit = 39
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
        startbit = 39
        byte = 4
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class AccrPedlRat_UB:
        sig_name = "AccrPedlRat_UB"
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

    class AmbTRawAmbTVal:
        sig_name = "AmbTRawAmbTVal"
        sig_start_bit = 50
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -70.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 700
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 50
        bmuws_info = [(6, 0b00000111, 0b11111000, 3, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class BrkPedlSnsr_UB:
        sig_name = "BrkPedlSnsr_UB"
        sig_start_bit = 27
        update_id_bit = 27
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
        startbit = 27
        byte = 3
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class AccrPedlRatAccrPedlRat:
        sig_name = "AccrPedlRatAccrPedlRat"
        sig_start_bit = 6
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
        startbit = 6
        bmuws_info = [(0, 0b01111111, 0b10000000, 7, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class AccrPedlRatChks:
        sig_name = "AccrPedlRatChks"
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

    class AccrPedlRatCntr:
        sig_name = "AccrPedlRatCntr"
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


class HcmrToBgmBodyExpoDiagRespFrame:
    msg_name = "HcmrToBgmBodyExpoDiagRespFrame"
    msg_id = 1716
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "HCMR"
    rx_nodes = ['BGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class EtctoHcmlXCPFr01:
    msg_name = "EtctoHcmlXCPFr01"
    msg_id = 1430
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CCM"
    rx_nodes = ['HCML']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class HcmmBodyExposedCANNmFr:
    msg_name = "HcmmBodyExposedCANNmFr"
    msg_id = 1334
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['RCML']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class CEMBodyExpoCommonFr07:
    msg_name = "CEMBodyExpoCommonFr07"
    msg_id = 544
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.06
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RCML', 'RCMR', 'RCMM', 'HCMR', 'HCML']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class CarTiGlb:
        sig_name = "CarTiGlb"
        sig_start_bit = 7
        update_id_bit = 39
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

    class TrSts:
        sig_name = "TrSts"
        sig_start_bit = 52
        update_id_bit = 50
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
        startbit = 52
        byte = 6
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class Body2CntrForMissCom:
        sig_name = "Body2CntrForMissCom"
        sig_start_bit = 63
        update_id_bit = 48
        sig_length = 8
        sig_value_factor = None
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


class BgmBodyExposedCANFr07:
    msg_name = "BgmBodyExposedCANFr07"
    msg_id = 151
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 64
    tx_node = "BGM"
    rx_nodes = ['HCMR']
    sig_group_dict = {'PIXFrntRiX3': ['PIXFrntRiX3Y1', 'PIXFrntRiX3Y2', 'PIXFrntRiX3Y3', 'PIXFrntRiX3Y4', 'PIXFrntRiX3Y5', 'PIXFrntRiX3Y6'], 'PIXFrntRiX1': ['PIXFrntRiX1Y1', 'PIXFrntRiX1Y2', 'PIXFrntRiX1Y3', 'PIXFrntRiX1Y4', 'PIXFrntRiX1Y5', 'PIXFrntRiX1Y6'], 'PIXFrntRiX6': ['PIXFrntRiX6Y1', 'PIXFrntRiX6Y2', 'PIXFrntRiX6Y3', 'PIXFrntRiX6Y4', 'PIXFrntRiX6Y5', 'PIXFrntRiX6Y6'], 'PIXFrntRiX4': ['PIXFrntRiX4Y1', 'PIXFrntRiX4Y2', 'PIXFrntRiX4Y3', 'PIXFrntRiX4Y4', 'PIXFrntRiX4Y5', 'PIXFrntRiX4Y6'], 'PIXFrntRiXB': ['PIXFrntRiXBY1', 'PIXFrntRiXBY2', 'PIXFrntRiXBY3', 'PIXFrntRiXBY4', 'PIXFrntRiXBY5', 'PIXFrntRiXBY6'], 'PIXFrntRiXA': ['PIXFrntRiXAY1', 'PIXFrntRiXAY2', 'PIXFrntRiXAY3', 'PIXFrntRiXAY4', 'PIXFrntRiXAY5', 'PIXFrntRiXAY6'], 'PIXFrntRiX2': ['PIXFrntRiX2Y1', 'PIXFrntRiX2Y2', 'PIXFrntRiX2Y3', 'PIXFrntRiX2Y4', 'PIXFrntRiX2Y5', 'PIXFrntRiX2Y6'], 'PIXFrntRiX9': ['PIXFrntRiX9Y1', 'PIXFrntRiX9Y2', 'PIXFrntRiX9Y3', 'PIXFrntRiX9Y4', 'PIXFrntRiX9Y5', 'PIXFrntRiX9Y6'], 'PIXFrntRiX7': ['PIXFrntRiX7Y1', 'PIXFrntRiX7Y2', 'PIXFrntRiX7Y3', 'PIXFrntRiX7Y4', 'PIXFrntRiX7Y5', 'PIXFrntRiX7Y6'], 'PIXFrntRiX8': ['PIXFrntRiX8Y1', 'PIXFrntRiX8Y2', 'PIXFrntRiX8Y3', 'PIXFrntRiX8Y4', 'PIXFrntRiX8Y5', 'PIXFrntRiX8Y6'], 'PIXFrntRiX5': ['PIXFrntRiX5Y1', 'PIXFrntRiX5Y2', 'PIXFrntRiX5Y3', 'PIXFrntRiX5Y4', 'PIXFrntRiX5Y5', 'PIXFrntRiX5Y6']}
    sig_group_dataid_dict = {}

    class PIXFrntRiXBY2:
        sig_name = "PIXFrntRiXBY2"
        sig_start_bit = 428
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 428
        bmuws_info = [(53, 0b00011111, 0b11100000, 5, 0), (54, 0b11000000, 0b00111111, 2, 6)]

    class PIXFrntRiXAY1:
        sig_name = "PIXFrntRiXAY1"
        sig_start_bit = 381
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 381
        bmuws_info = [(47, 0b00111111, 0b11000000, 6, 0), (48, 0b10000000, 0b01111111, 1, 7)]

    class PIXFrntRiXAY2:
        sig_name = "PIXFrntRiXAY2"
        sig_start_bit = 390
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 390
        byte = 48
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class PIXFrntRiX1Y5:
        sig_name = "PIXFrntRiX1Y5"
        sig_start_bit = 27
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 27
        bmuws_info = [(3, 0b00001111, 0b11110000, 4, 0), (4, 0b11100000, 0b00011111, 3, 5)]

    class PIXFrntRiX3_UB:
        sig_name = "PIXFrntRiX3_UB"
        sig_start_bit = 465
        update_id_bit = 465
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
        startbit = 465
        byte = 58
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class PIXFrntRiX7Y4:
        sig_name = "PIXFrntRiX7Y4"
        sig_start_bit = 278
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 278
        byte = 34
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class PIXFrntRiX9Y3:
        sig_name = "PIXFrntRiX9Y3"
        sig_start_bit = 345
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 345
        bmuws_info = [(43, 0b00000011, 0b11111100, 2, 0), (44, 0b11111000, 0b00000111, 5, 3)]

    class PIXFrntRiXBY3:
        sig_name = "PIXFrntRiXBY3"
        sig_start_bit = 437
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 437
        bmuws_info = [(54, 0b00111111, 0b11000000, 6, 0), (55, 0b10000000, 0b01111111, 1, 7)]

    class PIXFrntRiX3Y5:
        sig_name = "PIXFrntRiX3Y5"
        sig_start_bit = 119
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 119
        byte = 14
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXFrntRiX8Y2:
        sig_name = "PIXFrntRiX8Y2"
        sig_start_bit = 298
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 298
        bmuws_info = [(37, 0b00000111, 0b11111000, 3, 0), (38, 0b11110000, 0b00001111, 4, 4)]

    class PIXFrntRiX1_UB:
        sig_name = "PIXFrntRiX1_UB"
        sig_start_bit = 479
        update_id_bit = 479
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
        startbit = 479
        byte = 59
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class PIXFrntRiX8Y1:
        sig_name = "PIXFrntRiX8Y1"
        sig_start_bit = 289
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 289
        bmuws_info = [(36, 0b00000011, 0b11111100, 2, 0), (37, 0b11111000, 0b00000111, 5, 3)]

    class PIXFrntRiX6Y6:
        sig_name = "PIXFrntRiX6Y6"
        sig_start_bit = 242
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 242
        bmuws_info = [(30, 0b00000111, 0b11111000, 3, 0), (31, 0b11110000, 0b00001111, 4, 4)]

    class PIXFrntRiX9Y1:
        sig_name = "PIXFrntRiX9Y1"
        sig_start_bit = 343
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 343
        byte = 42
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXFrntRiX6_UB:
        sig_name = "PIXFrntRiX6_UB"
        sig_start_bit = 468
        update_id_bit = 468
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
        startbit = 468
        byte = 58
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class PIXFrntRiX4Y6:
        sig_name = "PIXFrntRiX4Y6"
        sig_start_bit = 166
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 166
        byte = 20
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class PIXFrntRiX4Y5:
        sig_name = "PIXFrntRiX4Y5"
        sig_start_bit = 157
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 157
        bmuws_info = [(19, 0b00111111, 0b11000000, 6, 0), (20, 0b10000000, 0b01111111, 1, 7)]

    class PIXFrntRiX1Y4:
        sig_name = "PIXFrntRiX1Y4"
        sig_start_bit = 18
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 18
        bmuws_info = [(2, 0b00000111, 0b11111000, 3, 0), (3, 0b11110000, 0b00001111, 4, 4)]

    class PIXFrntRiXAY5:
        sig_name = "PIXFrntRiXAY5"
        sig_start_bit = 401
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 401
        bmuws_info = [(50, 0b00000011, 0b11111100, 2, 0), (51, 0b11111000, 0b00000111, 5, 3)]

    class PIXFrntRiX6Y5:
        sig_name = "PIXFrntRiX6Y5"
        sig_start_bit = 233
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 233
        bmuws_info = [(29, 0b00000011, 0b11111100, 2, 0), (30, 0b11111000, 0b00000111, 5, 3)]

    class PIXFrntRiXAY6:
        sig_name = "PIXFrntRiXAY6"
        sig_start_bit = 410
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 410
        bmuws_info = [(51, 0b00000111, 0b11111000, 3, 0), (52, 0b11110000, 0b00001111, 4, 4)]

    class PIXFrntRiX4_UB:
        sig_name = "PIXFrntRiX4_UB"
        sig_start_bit = 466
        update_id_bit = 466
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
        startbit = 466
        byte = 58
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class PIXFrntRiX3Y2:
        sig_name = "PIXFrntRiX3Y2"
        sig_start_bit = 92
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 92
        bmuws_info = [(11, 0b00011111, 0b11100000, 5, 0), (12, 0b11000000, 0b00111111, 2, 6)]

    class PIXFrntRiXB_UB:
        sig_name = "PIXFrntRiXB_UB"
        sig_start_bit = 457
        update_id_bit = 457
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
        startbit = 457
        byte = 57
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class PIXFrntRiX6Y4:
        sig_name = "PIXFrntRiX6Y4"
        sig_start_bit = 224
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 224
        bmuws_info = [(28, 0b00000001, 0b11111110, 1, 0), (29, 0b11111100, 0b00000011, 6, 2)]

    class PIXFrntRiX8Y3:
        sig_name = "PIXFrntRiX8Y3"
        sig_start_bit = 307
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 307
        bmuws_info = [(38, 0b00001111, 0b11110000, 4, 0), (39, 0b11100000, 0b00011111, 3, 5)]

    class PIXFrntRiXAY3:
        sig_name = "PIXFrntRiXAY3"
        sig_start_bit = 399
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 399
        byte = 49
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXFrntRiX1Y1:
        sig_name = "PIXFrntRiX1Y1"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
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

    class PIXFrntRiX5Y1:
        sig_name = "PIXFrntRiX5Y1"
        sig_start_bit = 175
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 175
        byte = 21
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXFrntRiX1Y3:
        sig_name = "PIXFrntRiX1Y3"
        sig_start_bit = 9
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 9
        bmuws_info = [(1, 0b00000011, 0b11111100, 2, 0), (2, 0b11111000, 0b00000111, 5, 3)]

    class PIXFrntRiX5Y6:
        sig_name = "PIXFrntRiX5Y6"
        sig_start_bit = 204
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 204
        bmuws_info = [(25, 0b00011111, 0b11100000, 5, 0), (26, 0b11000000, 0b00111111, 2, 6)]

    class PIXFrntRiX4Y4:
        sig_name = "PIXFrntRiX4Y4"
        sig_start_bit = 148
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 148
        bmuws_info = [(18, 0b00011111, 0b11100000, 5, 0), (19, 0b11000000, 0b00111111, 2, 6)]

    class PIXFrntRiX8Y4:
        sig_name = "PIXFrntRiX8Y4"
        sig_start_bit = 316
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 316
        bmuws_info = [(39, 0b00011111, 0b11100000, 5, 0), (40, 0b11000000, 0b00111111, 2, 6)]

    class PIXFrntRiX7Y5:
        sig_name = "PIXFrntRiX7Y5"
        sig_start_bit = 287
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 287
        byte = 35
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXFrntRiXA_UB:
        sig_name = "PIXFrntRiXA_UB"
        sig_start_bit = 456
        update_id_bit = 456
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
        startbit = 456
        byte = 57
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class PIXFrntRiX4Y1:
        sig_name = "PIXFrntRiX4Y1"
        sig_start_bit = 121
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 121
        bmuws_info = [(15, 0b00000011, 0b11111100, 2, 0), (16, 0b11111000, 0b00000111, 5, 3)]

    class PIXFrntRiX5Y3:
        sig_name = "PIXFrntRiX5Y3"
        sig_start_bit = 177
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 177
        bmuws_info = [(22, 0b00000011, 0b11111100, 2, 0), (23, 0b11111000, 0b00000111, 5, 3)]

    class PIXFrntRiX2Y4:
        sig_name = "PIXFrntRiX2Y4"
        sig_start_bit = 56
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 56
        bmuws_info = [(7, 0b00000001, 0b11111110, 1, 0), (8, 0b11111100, 0b00000011, 6, 2)]

    class PIXFrntRiXBY4:
        sig_name = "PIXFrntRiXBY4"
        sig_start_bit = 446
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 446
        byte = 55
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class PIXFrntRiX3Y3:
        sig_name = "PIXFrntRiX3Y3"
        sig_start_bit = 101
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 101
        bmuws_info = [(12, 0b00111111, 0b11000000, 6, 0), (13, 0b10000000, 0b01111111, 1, 7)]

    class PIXFrntRiX9Y6:
        sig_name = "PIXFrntRiX9Y6"
        sig_start_bit = 372
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 372
        bmuws_info = [(46, 0b00011111, 0b11100000, 5, 0), (47, 0b11000000, 0b00111111, 2, 6)]

    class PIXFrntRiX2_UB:
        sig_name = "PIXFrntRiX2_UB"
        sig_start_bit = 464
        update_id_bit = 464
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
        startbit = 464
        byte = 58
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class PIXFrntRiX5Y4:
        sig_name = "PIXFrntRiX5Y4"
        sig_start_bit = 186
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 186
        bmuws_info = [(23, 0b00000111, 0b11111000, 3, 0), (24, 0b11110000, 0b00001111, 4, 4)]

    class PIXFrntRiXBY5:
        sig_name = "PIXFrntRiXBY5"
        sig_start_bit = 455
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 455
        byte = 56
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXFrntRiX9_UB:
        sig_name = "PIXFrntRiX9_UB"
        sig_start_bit = 471
        update_id_bit = 471
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
        startbit = 471
        byte = 58
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class PIXFrntRiX7_UB:
        sig_name = "PIXFrntRiX7_UB"
        sig_start_bit = 469
        update_id_bit = 469
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
        startbit = 469
        byte = 58
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class PIXFrntRiX7Y2:
        sig_name = "PIXFrntRiX7Y2"
        sig_start_bit = 260
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 260
        bmuws_info = [(32, 0b00011111, 0b11100000, 5, 0), (33, 0b11000000, 0b00111111, 2, 6)]

    class PIXFrntRiX4Y3:
        sig_name = "PIXFrntRiX4Y3"
        sig_start_bit = 139
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 139
        bmuws_info = [(17, 0b00001111, 0b11110000, 4, 0), (18, 0b11100000, 0b00011111, 3, 5)]

    class PIXFrntRiX2Y1:
        sig_name = "PIXFrntRiX2Y1"
        sig_start_bit = 45
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 45
        bmuws_info = [(5, 0b00111111, 0b11000000, 6, 0), (6, 0b10000000, 0b01111111, 1, 7)]

    class PIXFrntRiX3Y4:
        sig_name = "PIXFrntRiX3Y4"
        sig_start_bit = 110
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 110
        byte = 13
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class PIXFrntRiXAY4:
        sig_name = "PIXFrntRiXAY4"
        sig_start_bit = 392
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 392
        bmuws_info = [(49, 0b00000001, 0b11111110, 1, 0), (50, 0b11111100, 0b00000011, 6, 2)]

    class PIXFrntRiX8_UB:
        sig_name = "PIXFrntRiX8_UB"
        sig_start_bit = 470
        update_id_bit = 470
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
        startbit = 470
        byte = 58
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class PIXFrntRiX9Y2:
        sig_name = "PIXFrntRiX9Y2"
        sig_start_bit = 336
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 336
        bmuws_info = [(42, 0b00000001, 0b11111110, 1, 0), (43, 0b11111100, 0b00000011, 6, 2)]

    class PIXFrntRiX6Y3:
        sig_name = "PIXFrntRiX6Y3"
        sig_start_bit = 231
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 231
        byte = 28
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class PIXFrntRiX9Y4:
        sig_name = "PIXFrntRiX9Y4"
        sig_start_bit = 354
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 354
        bmuws_info = [(44, 0b00000111, 0b11111000, 3, 0), (45, 0b11110000, 0b00001111, 4, 4)]

    class PIXFrntRiX4Y2:
        sig_name = "PIXFrntRiX4Y2"
        sig_start_bit = 130
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 130
        bmuws_info = [(16, 0b00000111, 0b11111000, 3, 0), (17, 0b11110000, 0b00001111, 4, 4)]

    class PIXFrntRiX2Y3:
        sig_name = "PIXFrntRiX2Y3"
        sig_start_bit = 63
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
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

    class PIXFrntRiX7Y6:
        sig_name = "PIXFrntRiX7Y6"
        sig_start_bit = 280
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 280
        bmuws_info = [(35, 0b00000001, 0b11111110, 1, 0), (36, 0b11111100, 0b00000011, 6, 2)]

    class PIXFrntRiX8Y6:
        sig_name = "PIXFrntRiX8Y6"
        sig_start_bit = 334
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 334
        byte = 41
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class PIXFrntRiX2Y6:
        sig_name = "PIXFrntRiX2Y6"
        sig_start_bit = 74
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 74
        bmuws_info = [(9, 0b00000111, 0b11111000, 3, 0), (10, 0b11110000, 0b00001111, 4, 4)]

    class PIXFrntRiXBY6:
        sig_name = "PIXFrntRiXBY6"
        sig_start_bit = 448
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 448
        bmuws_info = [(56, 0b00000001, 0b11111110, 1, 0), (57, 0b11111100, 0b00000011, 6, 2)]

    class PIXFrntRiX1Y6:
        sig_name = "PIXFrntRiX1Y6"
        sig_start_bit = 36
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 36
        bmuws_info = [(4, 0b00011111, 0b11100000, 5, 0), (5, 0b11000000, 0b00111111, 2, 6)]

    class PIXFrntRiX5_UB:
        sig_name = "PIXFrntRiX5_UB"
        sig_start_bit = 467
        update_id_bit = 467
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
        startbit = 467
        byte = 58
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class PIXFrntRiX2Y5:
        sig_name = "PIXFrntRiX2Y5"
        sig_start_bit = 65
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 65
        bmuws_info = [(8, 0b00000011, 0b11111100, 2, 0), (9, 0b11111000, 0b00000111, 5, 3)]

    class PIXFrntRiX3Y6:
        sig_name = "PIXFrntRiX3Y6"
        sig_start_bit = 112
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 112
        bmuws_info = [(14, 0b00000001, 0b11111110, 1, 0), (15, 0b11111100, 0b00000011, 6, 2)]

    class PIXFrntRiX7Y1:
        sig_name = "PIXFrntRiX7Y1"
        sig_start_bit = 251
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 251
        bmuws_info = [(31, 0b00001111, 0b11110000, 4, 0), (32, 0b11100000, 0b00011111, 3, 5)]

    class PIXFrntRiX3Y1:
        sig_name = "PIXFrntRiX3Y1"
        sig_start_bit = 83
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 83
        bmuws_info = [(10, 0b00001111, 0b11110000, 4, 0), (11, 0b11100000, 0b00011111, 3, 5)]

    class PIXFrntRiX7Y3:
        sig_name = "PIXFrntRiX7Y3"
        sig_start_bit = 269
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 269
        bmuws_info = [(33, 0b00111111, 0b11000000, 6, 0), (34, 0b10000000, 0b01111111, 1, 7)]

    class PIXFrntRiX2Y2:
        sig_name = "PIXFrntRiX2Y2"
        sig_start_bit = 54
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 54
        byte = 6
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class PIXFrntRiX6Y2:
        sig_name = "PIXFrntRiX6Y2"
        sig_start_bit = 222
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 222
        byte = 27
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class PIXFrntRiX8Y5:
        sig_name = "PIXFrntRiX8Y5"
        sig_start_bit = 325
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 325
        bmuws_info = [(40, 0b00111111, 0b11000000, 6, 0), (41, 0b10000000, 0b01111111, 1, 7)]

    class PIXFrntRiX1Y2:
        sig_name = "PIXFrntRiX1Y2"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 0
        bmuws_info = [(0, 0b00000001, 0b11111110, 1, 0), (1, 0b11111100, 0b00000011, 6, 2)]

    class PIXFrntRiX5Y5:
        sig_name = "PIXFrntRiX5Y5"
        sig_start_bit = 195
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 195
        bmuws_info = [(24, 0b00001111, 0b11110000, 4, 0), (25, 0b11100000, 0b00011111, 3, 5)]

    class PIXFrntRiX9Y5:
        sig_name = "PIXFrntRiX9Y5"
        sig_start_bit = 363
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 363
        bmuws_info = [(45, 0b00001111, 0b11110000, 4, 0), (46, 0b11100000, 0b00011111, 3, 5)]

    class PIXFrntRiXBY1:
        sig_name = "PIXFrntRiXBY1"
        sig_start_bit = 419
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 419
        bmuws_info = [(52, 0b00001111, 0b11110000, 4, 0), (53, 0b11100000, 0b00011111, 3, 5)]

    class PIXFrntRiX5Y2:
        sig_name = "PIXFrntRiX5Y2"
        sig_start_bit = 168
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 168
        bmuws_info = [(21, 0b00000001, 0b11111110, 1, 0), (22, 0b11111100, 0b00000011, 6, 2)]

    class PIXFrntRiX6Y1:
        sig_name = "PIXFrntRiX6Y1"
        sig_start_bit = 213
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 213
        bmuws_info = [(26, 0b00111111, 0b11000000, 6, 0), (27, 0b10000000, 0b01111111, 1, 7)]


class CemBodyExpoFr50:
    msg_name = "CemBodyExpoFr50"
    msg_id = 522
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.03
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RCML', 'RCMR', 'RCMM', 'HCMR', 'HCML']
    sig_group_dict = {'ActnOfLedStopLamp': ['ActnOfLedStopLampActnOfLedStopLamp', 'ActnOfLedStopLampChks', 'ActnOfLedStopLampCntr'], 'ActnOfLedLoBeam': ['ActnOfLedLoBeamActnOfLedLoBeam', 'ActnOfLedLoBeamChks', 'ActnOfLedLoBeamCntr']}
    sig_group_dataid_dict = {'ActnOfLedStopLamp': 1091, 'ActnOfLedLoBeam': 1089}

    class ActnOfLedRvsgLamp:
        sig_name = "ActnOfLedRvsgLamp"
        sig_start_bit = 42
        update_id_bit = 43
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

    class ActnOfLedLoBeamActnOfLedLoBeam:
        sig_name = "ActnOfLedLoBeamActnOfLedLoBeam"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 4
        byte = 0
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class ActnOfLedDaytiRunngLamp:
        sig_name = "ActnOfLedDaytiRunngLamp"
        sig_start_bit = 32
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
        startbit = 32
        byte = 4
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ActnOfLedStopLamp_UB:
        sig_name = "ActnOfLedStopLamp_UB"
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

    class ActnOfLedHiBeam:
        sig_name = "ActnOfLedHiBeam"
        sig_start_bit = 36
        update_id_bit = 37
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
        startbit = 36
        byte = 4
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class ActnOfLedPosnLamp:
        sig_name = "ActnOfLedPosnLamp"
        sig_start_bit = 38
        update_id_bit = 39
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
        startbit = 38
        byte = 4
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class ActnOfLedLoBeam_UB:
        sig_name = "ActnOfLedLoBeam_UB"
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

    class ActnOfLedFrntFogLamp:
        sig_name = "ActnOfLedFrntFogLamp"
        sig_start_bit = 34
        update_id_bit = 35
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

    class ActnOfLedLoBeamCntr:
        sig_name = "ActnOfLedLoBeamCntr"
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

    class ActnOfLedStopLampActnOfLedStopLamp:
        sig_name = "ActnOfLedStopLampActnOfLedStopLamp"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 20
        byte = 2
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class ActnOfLedLoBeamChks:
        sig_name = "ActnOfLedLoBeamChks"
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

    class ActnOfLedStopLampChks:
        sig_name = "ActnOfLedStopLampChks"
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

    class ActnOfLedStopLampCntr:
        sig_name = "ActnOfLedStopLampCntr"
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

    class ActnOfLedReFogLamp:
        sig_name = "ActnOfLedReFogLamp"
        sig_start_bit = 40
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
        startbit = 40
        byte = 5
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ActvnOfDbl:
        sig_name = "ActvnOfDbl"
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

    class ActvnOfAhl:
        sig_name = "ActvnOfAhl"
        sig_start_bit = 48
        update_id_bit = 49
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
        startbit = 48
        byte = 6
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0


