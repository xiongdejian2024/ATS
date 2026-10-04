class MGMPropulsionCANFDFr06:
    msg_name = "MGMPropulsionCANFDFr06"
    msg_id = 19
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 32
    tx_node = "MGM"
    rx_nodes = ['ETC', 'CCUMCUCD']
    sig_group_dict = {'FrntMotDevelpSignalGroup3': ['FrntMotDevelpSignalGroup3DevelpSignalGroup1', 'FrntMotDevelpSignalGroup3DevelpSignalGroup2', 'FrntMotDevelpSignalGroup3DevelpSignalGroup3', 'FrntMotDevelpSignalGroup3DevelpSignalGroup4', 'FrntMotDevelpSignalGroup3DevelpSignalGroup5', 'FrntMotDevelpSignalGroup3DevelpSignalGroup6', 'FrntMotDevelpSignalGroup3DevelpSignalGroup7', 'FrntMotDevelpSignalGroup3DevelpSignalGroup8'], 'FrntMotDevelpSignalGroup2': ['FrntMotDevelpSignalGroup2DTC1HighByte', 'FrntMotDevelpSignalGroup2DTC1LowByte', 'FrntMotDevelpSignalGroup2DTC1MiddleByte', 'FrntMotDevelpSignalGroup2DTC1Sts', 'FrntMotDevelpSignalGroup2DTC2HighByte', 'FrntMotDevelpSignalGroup2DTC2LowByte', 'FrntMotDevelpSignalGroup2DTC2MiddleByte', 'FrntMotDevelpSignalGroup2DTC2Sts'], 'FrntMotDevelpSignalGroup1': ['FrntMotDevelpSignalGroup1DTC1HighByte', 'FrntMotDevelpSignalGroup1DTC1LowByte', 'FrntMotDevelpSignalGroup1DTC1MiddleByte', 'FrntMotDevelpSignalGroup1DTC1Sts', 'FrntMotDevelpSignalGroup1DTC2HighByte', 'FrntMotDevelpSignalGroup1DTC2LowByte', 'FrntMotDevelpSignalGroup1DTC2MiddleByte', 'FrntMotDevelpSignalGroup1DTC2Sts']}
    sig_group_dataid_dict = {}

    class FrntMotDevelpSignalGroup2DTC1Sts:
        sig_name = "FrntMotDevelpSignalGroup2DTC1Sts"
        sig_start_bit = 103
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
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

    class FrntMotDevelpSignalGroup1DTC1LowByte:
        sig_name = "FrntMotDevelpSignalGroup1DTC1LowByte"
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

    class FrntMotDevelpSignalGroup3DevelpSignalGroup5:
        sig_name = "FrntMotDevelpSignalGroup3DevelpSignalGroup5"
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

    class FrntMotDevelpSignalGroup3DevelpSignalGroup2:
        sig_name = "FrntMotDevelpSignalGroup3DevelpSignalGroup2"
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

    class FrntMotDevelpSignalGroup3_UB:
        sig_name = "FrntMotDevelpSignalGroup3_UB"
        sig_start_bit = 215
        update_id_bit = 215
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
        startbit = 215
        byte = 26
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class FrntMotDevelpSignalGroup3DevelpSignalGroup7:
        sig_name = "FrntMotDevelpSignalGroup3DevelpSignalGroup7"
        sig_start_bit = 199
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
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

    class FrntMotDevelpSignalGroup1DTC2HighByte:
        sig_name = "FrntMotDevelpSignalGroup1DTC2HighByte"
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

    class FrntMotDevelpSignalGroup2DTC2MiddleByte:
        sig_name = "FrntMotDevelpSignalGroup2DTC2MiddleByte"
        sig_start_bit = 127
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 127
        byte = 15
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntMotDevelpSignalGroup3DevelpSignalGroup4:
        sig_name = "FrntMotDevelpSignalGroup3DevelpSignalGroup4"
        sig_start_bit = 175
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
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

    class FrntMotDevelpSignalGroup1DTC1MiddleByte:
        sig_name = "FrntMotDevelpSignalGroup1DTC1MiddleByte"
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

    class FrntMotDevelpSignalGroup1DTC2MiddleByte:
        sig_name = "FrntMotDevelpSignalGroup1DTC2MiddleByte"
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

    class FrntMotDevelpSignalGroup3DevelpSignalGroup8:
        sig_name = "FrntMotDevelpSignalGroup3DevelpSignalGroup8"
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

    class FrntMotDevelpSignalGroup2DTC1MiddleByte:
        sig_name = "FrntMotDevelpSignalGroup2DTC1MiddleByte"
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

    class FrntMotDevelpSignalGroup1DTC1Sts:
        sig_name = "FrntMotDevelpSignalGroup1DTC1Sts"
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

    class FrntMotDevelpSignalGroup1DTC2Sts:
        sig_name = "FrntMotDevelpSignalGroup1DTC2Sts"
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

    class FrntMotDevelpSignalGroup2_UB:
        sig_name = "FrntMotDevelpSignalGroup2_UB"
        sig_start_bit = 143
        update_id_bit = 143
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
        startbit = 143
        byte = 17
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class FrntMotDevelpSignalGroup2DTC1HighByte:
        sig_name = "FrntMotDevelpSignalGroup2DTC1HighByte"
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

    class FrntMotDevelpSignalGroup1_UB:
        sig_name = "FrntMotDevelpSignalGroup1_UB"
        sig_start_bit = 71
        update_id_bit = 71
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
        startbit = 71
        byte = 8
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class FrntMotDevelpSignalGroup1DTC2LowByte:
        sig_name = "FrntMotDevelpSignalGroup1DTC2LowByte"
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

    class FrntMotDevelpSignalGroup3DevelpSignalGroup3:
        sig_name = "FrntMotDevelpSignalGroup3DevelpSignalGroup3"
        sig_start_bit = 167
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
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

    class FrntMotDevelpSignalGroup2DTC2Sts:
        sig_name = "FrntMotDevelpSignalGroup2DTC2Sts"
        sig_start_bit = 135
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 135
        byte = 16
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntMotDevelpSignalGroup1DTC1HighByte:
        sig_name = "FrntMotDevelpSignalGroup1DTC1HighByte"
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

    class FrntMotDevelpSignalGroup3DevelpSignalGroup1:
        sig_name = "FrntMotDevelpSignalGroup3DevelpSignalGroup1"
        sig_start_bit = 151
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 151
        byte = 18
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntMotDevelpSignalGroup2DTC2LowByte:
        sig_name = "FrntMotDevelpSignalGroup2DTC2LowByte"
        sig_start_bit = 119
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 119
        byte = 14
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntMotDevelpSignalGroup3DevelpSignalGroup6:
        sig_name = "FrntMotDevelpSignalGroup3DevelpSignalGroup6"
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

    class FrntMotDevelpSignalGroup2DTC2HighByte:
        sig_name = "FrntMotDevelpSignalGroup2DTC2HighByte"
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

    class FrntMotDevelpSignalGroup2DTC1LowByte:
        sig_name = "FrntMotDevelpSignalGroup2DTC1LowByte"
        sig_start_bit = 87
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 87
        byte = 10
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class CCUMCUCDPropulsionCANFDFr04:
    msg_name = "CCUMCUCDPropulsionCANFDFr04"
    msg_id = 385
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 48
    tx_node = "CCUMCUCD"
    rx_nodes = ['VCU', 'SRS', 'ODP', 'MGM', 'EGSM', 'IEM', 'BECM', 'BCU2', 'CCUMCUAD', 'BCU1']
    sig_group_dict = {'ImobRespMGM': ['ImobRespMGMChks', 'ImobRespMGMCntr', 'ImobRespMGMImobDateResp0', 'ImobRespMGMImobDateResp1', 'ImobRespMGMImobDateResp2', 'ImobRespMGMImobDateResp3', 'ImobRespMGMImobDateResp4', 'ImobRespMGMImobDateResp5', 'ImobRespMGMImobRespCmd'], 'ImobRespIEM': ['ImobRespIEMChks', 'ImobRespIEMCntr', 'ImobRespIEMImobDateResp0', 'ImobRespIEMImobDateResp1', 'ImobRespIEMImobDateResp2', 'ImobRespIEMImobDateResp3', 'ImobRespIEMImobDateResp4', 'ImobRespIEMImobDateResp5', 'ImobRespIEMImobRespCmd'], 'ImobRespVCU': ['ImobRespVCUChks', 'ImobRespVCUCntr', 'ImobRespVCUImobDateResp0', 'ImobRespVCUImobDateResp1', 'ImobRespVCUImobDateResp2', 'ImobRespVCUImobDateResp3', 'ImobRespVCUImobDateResp4', 'ImobRespVCUImobDateResp5', 'ImobRespVCUImobRespCmd'], 'Odometer': ['OdometerValidity', 'OdometerValue']}
    sig_group_dataid_dict = {}

    class ImobRespVCUImobRespCmd:
        sig_name = "ImobRespVCUImobRespCmd"
        sig_start_bit = 183
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ImobReqCmd_Idle': 0, 'ImobReqCmd_StrtReqCmd': 1, 'ImobReqCmd_RemStrtReqCmd': 2, 'ImobReqCmd_TurnOffCmd': 3}
        compute_method = None
        length = 2
        startbit = 183
        byte = 22
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class ImobRespMGMImobDateResp2:
        sig_name = "ImobRespMGMImobDateResp2"
        sig_start_bit = 135
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 135
        byte = 16
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ImobRespMGMImobDateResp3:
        sig_name = "ImobRespMGMImobDateResp3"
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

    class ImobRespVCUChks:
        sig_name = "ImobRespVCUChks"
        sig_start_bit = 175
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
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

    class ImobRespMGMImobDateResp1:
        sig_name = "ImobRespMGMImobDateResp1"
        sig_start_bit = 127
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 127
        byte = 15
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ImobRespMGMImobDateResp5:
        sig_name = "ImobRespMGMImobDateResp5"
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

    class OdometerValidity:
        sig_name = "OdometerValidity"
        sig_start_bit = 247
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Validity_NotValid': 0, 'Validity_Valid': 1}
        compute_method = None
        length = 1
        startbit = 247
        byte = 30
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ImobRespVCUCntr:
        sig_name = "ImobRespVCUCntr"
        sig_start_bit = 179
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
        startbit = 179
        byte = 22
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class VehBattU:
        sig_name = "VehBattU"
        sig_start_bit = 13
        update_id_bit = 19
        sig_length = 10
        sig_value_factor = 0.02
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1022
        sig_byteorder = "Motorola"
        sig_value_init = 1023
        sig_value_type = "SCALE_LINEAR_AND_TEXTTABLE"
        sig_value_table = {'BattU2_BMSVolWakeUpThd': 1023}
        compute_method = None
        length = 10
        startbit = 13
        bmuws_info = [(1, 0b00111111, 0b11000000, 6, 0), (2, 0b11110000, 0b00001111, 4, 4)]

    class ImobRespIEMImobDateResp1:
        sig_name = "ImobRespIEMImobDateResp1"
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

    class ImobRespVCUImobDateResp4:
        sig_name = "ImobRespVCUImobDateResp4"
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

    class ImobRespMGM_UB:
        sig_name = "ImobRespMGM_UB"
        sig_start_bit = 108
        update_id_bit = 108
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
        startbit = 108
        byte = 13
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class ImobRespVCUImobDateResp0:
        sig_name = "ImobRespVCUImobDateResp0"
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

    class ImobRespIEMImobDateResp3:
        sig_name = "ImobRespIEMImobDateResp3"
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

    class ImobRespIEMCntr:
        sig_name = "ImobRespIEMCntr"
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

    class ImobRespIEMImobDateResp5:
        sig_name = "ImobRespIEMImobDateResp5"
        sig_start_bit = 87
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 87
        byte = 10
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ImobRespIEMImobDateResp0:
        sig_name = "ImobRespIEMImobDateResp0"
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

    class ImobRespIEM_UB:
        sig_name = "ImobRespIEM_UB"
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

    class ImobRespMGMImobDateResp4:
        sig_name = "ImobRespMGMImobDateResp4"
        sig_start_bit = 151
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 151
        byte = 18
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ImobRespVCU_UB:
        sig_name = "ImobRespVCU_UB"
        sig_start_bit = 180
        update_id_bit = 180
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
        startbit = 180
        byte = 22
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class ImobRespVCUImobDateResp5:
        sig_name = "ImobRespVCUImobDateResp5"
        sig_start_bit = 231
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 231
        byte = 28
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ImobRespIEMImobDateResp2:
        sig_name = "ImobRespIEMImobDateResp2"
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

    class OdometerValue:
        sig_name = "OdometerValue"
        sig_start_bit = 246
        update_id_bit = None
        sig_length = 21
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 21
        startbit = 246
        bmuws_info = [(30, 0b01111111, 0b10000000, 7, 0), (31, 0b11111111, 0b00000000, 8, 0), (32, 0b11111100, 0b00000011, 6, 2)]

    class ImobRespMGMImobDateResp0:
        sig_name = "ImobRespMGMImobDateResp0"
        sig_start_bit = 119
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 119
        byte = 14
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ImobRespIEMImobRespCmd:
        sig_name = "ImobRespIEMImobRespCmd"
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
        sig_value_table = {'ImobReqCmd_Idle': 0, 'ImobReqCmd_StrtReqCmd': 1, 'ImobReqCmd_RemStrtReqCmd': 2, 'ImobReqCmd_TurnOffCmd': 3}
        compute_method = None
        length = 2
        startbit = 39
        byte = 4
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class ImobRespIEMChks:
        sig_name = "ImobRespIEMChks"
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

    class VehTiGlb:
        sig_name = "VehTiGlb"
        sig_start_bit = 271
        update_id_bit = 303
        sig_length = 32
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4294967295
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 32
        startbit = 271
        bmuws_info = [(33, 0b11111111, 0b00000000, 8, 0), (34, 0b11111111, 0b00000000, 8, 0), (35, 0b11111111, 0b00000000, 8, 0), (36, 0b11111111, 0b00000000, 8, 0)]

    class ImobRespVCUImobDateResp1:
        sig_name = "ImobRespVCUImobDateResp1"
        sig_start_bit = 199
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
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

    class ImobRespMGMCntr:
        sig_name = "ImobRespMGMCntr"
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

    class ImobRespMGMImobRespCmd:
        sig_name = "ImobRespMGMImobRespCmd"
        sig_start_bit = 111
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ImobReqCmd_Idle': 0, 'ImobReqCmd_StrtReqCmd': 1, 'ImobReqCmd_RemStrtReqCmd': 2, 'ImobReqCmd_TurnOffCmd': 3}
        compute_method = None
        length = 2
        startbit = 111
        byte = 13
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class ImobRespIEMImobDateResp4:
        sig_name = "ImobRespIEMImobDateResp4"
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

    class ImobRespVCUImobDateResp3:
        sig_name = "ImobRespVCUImobDateResp3"
        sig_start_bit = 215
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
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

    class ImobRespMGMChks:
        sig_name = "ImobRespMGMChks"
        sig_start_bit = 103
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
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

    class ImobRespVCUImobDateResp2:
        sig_name = "ImobRespVCUImobDateResp2"
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

    class Odometer_UB:
        sig_name = "Odometer_UB"
        sig_start_bit = 257
        update_id_bit = 257
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
        startbit = 257
        byte = 32
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class ChrgnUReq:
        sig_name = "ChrgnUReq"
        sig_start_bit = 7
        update_id_bit = 14
        sig_length = 9
        sig_value_factor = 0.025
        sig_value_offset = 5
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b10000000, 0b01111111, 1, 7)]


class BCU1PropulsionCANFDFr02:
    msg_name = "BCU1PropulsionCANFDFr02"
    msg_id = 128
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 64
    tx_node = "BCU1"
    rx_nodes = ['VCU', 'CCUMCUCD', 'ETC', 'SRS', 'ODP', 'MGM', 'EGSM', 'IEM', 'BECM', 'BCU2', 'CCUMCUAD']
    sig_group_dict = {'EpbTotSts': ['EpbTotStsChks', 'EpbTotStsCntr', 'EpbTotStsEpbSt'], 'BrkPedlInfo': ['BrkPedlInfoChks', 'BrkPedlInfoCntr', 'BrkPedlInfoNotPsd', 'BrkPedlInfoPsd', 'BrkPedlInfoQf'], 'WhlMovgDirRe': ['WhlMovgDirReChks', 'WhlMovgDirReCntr', 'WhlMovgDirReDirLe', 'WhlMovgDirReDirRi'], 'AebSts': ['AebStsActv', 'AebStsAllw', 'AebStsDenied', 'AebStsEna', 'AebStsSts1'], 'WhlMovgDirFrnt': ['WhlMovgDirFrntChks', 'WhlMovgDirFrntCntr', 'WhlMovgDirFrntDirLe', 'WhlMovgDirFrntDirRi'], 'VehLgtAccelFromWhlSpdWithCmp': ['VehLgtAccelFromWhlSpdWithCmpChks', 'VehLgtAccelFromWhlSpdWithCmpCntr', 'VehLgtAccelFromWhlSpdWithCmpLgt', 'VehLgtAccelFromWhlSpdWithCmpQf'], 'PropAxleTqAdd': ['PropAxleTqAddChks', 'PropAxleTqAddCntr', 'PropAxleTqAddFrnt', 'PropAxleTqAddRe'], 'AcbStsPrim': ['AcbStsPrimActv', 'AcbStsPrimAdAllow', 'AcbStsPrimDecelCompAllow', 'AcbStsPrimEna', 'AcbStsPrimEpedalAllow', 'AcbStsPrimSts1'], 'BrkPedlStk': ['BrkPedlStkAct', 'BrkPedlStkChks', 'BrkPedlStkCntr', 'BrkPedlStkQf', 'BrkPedlStkSt', 'BrkPedlStkStQf', 'BrkPedlStkTar'], 'VehMovgDir': ['VehMovgDirChks', 'VehMovgDirCntr', 'VehMovgDirVehMovgDir'], 'VehSpd': ['VehSpdChks', 'VehSpdCntr', 'VehSpdQf', 'VehSpdSpd'], 'VehSpdSafe': ['VehSpdSafeChks', 'VehSpdSafeCntr', 'VehSpdSafeQf', 'VehSpdSafeSpd'], 'VehLgtAccelFromWhlSpd': ['VehLgtAccelFromWhlSpdChks', 'VehLgtAccelFromWhlSpdCntr', 'VehLgtAccelFromWhlSpdLgt', 'VehLgtAccelFromWhlSpdQf'], 'EpbLampReq': ['EpbLampReqChks', 'EpbLampReqCntr', 'EpbLampReqEpbLampReq']}
    sig_group_dataid_dict = {'EpbTotSts': 1050, 'BrkPedlInfo': 1049, 'PropAxleTqAdd': 1048, 'BrkPedlStk': 1054, 'VehSpd': 1043, 'VehSpdSafe': 1044}

    class VehLgtAccelFromWhlSpdQf:
        sig_name = "VehLgtAccelFromWhlSpdQf"
        sig_start_bit = 247
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
        startbit = 247
        byte = 30
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class VehLgtAccelFromWhlSpdLgt:
        sig_name = "VehLgtAccelFromWhlSpdLgt"
        sig_start_bit = 255
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 0.00097654254
        sig_value_offset = 0
        sig_value_min = -18432
        sig_value_max = 18432
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 255
        bmuws_info = [(31, 0b11111111, 0b00000000, 8, 0), (32, 0b11111111, 0b00000000, 8, 0)]

    class EpbTotSts_UB:
        sig_name = "EpbTotSts_UB"
        sig_start_bit = 230
        update_id_bit = 230
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
        startbit = 230
        byte = 28
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class EpbLampReqCntr:
        sig_name = "EpbLampReqCntr"
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

    class PropAxleTqAddCntr:
        sig_name = "PropAxleTqAddCntr"
        sig_start_bit = 207
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
        startbit = 207
        byte = 25
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class WhlMovgDirReChks:
        sig_name = "WhlMovgDirReChks"
        sig_start_bit = 399
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 399
        byte = 49
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class PropAxleTqAddChks:
        sig_name = "PropAxleTqAddChks"
        sig_start_bit = 199
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
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

    class VehMovgDirVehMovgDir:
        sig_name = "VehMovgDirVehMovgDir"
        sig_start_bit = 311
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VehMovgDir_Unknown': 0, 'VehMovgDir_Standstill1': 1, 'VehMovgDir_Standstill2': 2, 'VehMovgDir_Standstill3': 3, 'VehMovgDir_Forward1': 4, 'VehMovgDir_Forward2': 5, 'VehMovgDir_Backward1': 6, 'VehMovgDir_Backward2': 7}
        compute_method = None
        length = 3
        startbit = 311
        byte = 38
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class PropAxleTqAddFrnt:
        sig_name = "PropAxleTqAddFrnt"
        sig_start_bit = 203
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 203
        bmuws_info = [(25, 0b00001111, 0b11110000, 4, 0), (26, 0b11111100, 0b00000011, 6, 2)]

    class BrkPedlStkQf:
        sig_name = "BrkPedlStkQf"
        sig_start_bit = 127
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
        startbit = 127
        byte = 15
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class AcbStsPrimEna:
        sig_name = "AcbStsPrimEna"
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
        sig_value_table = {'EnableDisable2_Disabled': 0, 'EnableDisable2_Enabled': 1}
        compute_method = None
        length = 1
        startbit = 15
        byte = 1
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class AcbStsPrimSts1:
        sig_name = "AcbStsPrimSts1"
        sig_start_bit = 14
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Sts1_Initial': 0, 'Sts1_Normal': 1, 'Sts1_Fault': 2, 'Sts1_Limited': 3}
        compute_method = None
        length = 3
        startbit = 14
        byte = 1
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class BrkPedlStkChks:
        sig_name = "BrkPedlStkChks"
        sig_start_bit = 119
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 119
        byte = 14
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BrkPedlStkTar:
        sig_name = "BrkPedlStkTar"
        sig_start_bit = 138
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
        startbit = 138
        bmuws_info = [(17, 0b00000111, 0b11111000, 3, 0), (18, 0b11111111, 0b00000000, 8, 0), (19, 0b11000000, 0b00111111, 2, 6)]

    class AebStsSts1:
        sig_name = "AebStsSts1"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Sts1_Initial': 0, 'Sts1_Normal': 1, 'Sts1_Fault': 2, 'Sts1_Limited': 3}
        compute_method = None
        length = 3
        startbit = 31
        byte = 3
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class BrkPedlInfo_UB:
        sig_name = "BrkPedlInfo_UB"
        sig_start_bit = 153
        update_id_bit = 153
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
        startbit = 153
        byte = 19
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VehMovgDirChks:
        sig_name = "VehMovgDirChks"
        sig_start_bit = 303
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 303
        byte = 37
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class PropAxleTqAddRe:
        sig_name = "PropAxleTqAddRe"
        sig_start_bit = 209
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 209
        bmuws_info = [(26, 0b00000011, 0b11111100, 2, 0), (27, 0b11111111, 0b00000000, 8, 0)]

    class AebStsEna:
        sig_name = "AebStsEna"
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
        sig_value_table = {'EnableDisable2_Disabled': 0, 'EnableDisable2_Enabled': 1}
        compute_method = None
        length = 1
        startbit = 17
        byte = 2
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class WhlMovgDirRe_UB:
        sig_name = "WhlMovgDirRe_UB"
        sig_start_bit = 416
        update_id_bit = 416
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
        startbit = 416
        byte = 52
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class AebStsAllw:
        sig_name = "AebStsAllw"
        sig_start_bit = 21
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AllwdorNot2_NotAllw': 0, 'AllwdorNot2_Allw': 1}
        compute_method = None
        length = 2
        startbit = 21
        byte = 2
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class EpbTotStsEpbSt:
        sig_name = "EpbTotStsEpbSt"
        sig_start_bit = 191
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EpbSt_Reserved0': 0, 'EpbSt_Roller': 1, 'EpbSt_Maintain': 2, 'EpbSt_AllApplid': 3, 'EpbSt_PrimApplidSecUnkown': 4, 'EpbSt_AllTran': 5, 'EpbSt_ADBF': 6, 'EpbSt_PrimReldSecUnkown': 7, 'EpbSt_SecApplidPrimUnkown': 8, 'EpbSt_AllReleased': 9, 'EpbSt_DDBF': 10, 'EpbSt_SecReldPrimUnkown': 11, 'EpbSt_DBF': 12, 'EpbSt_OneSideAppliedAtLeast': 13, 'EpbSt_Reserved3': 14, 'EpbSt_Error': 15}
        compute_method = None
        length = 4
        startbit = 191
        byte = 23
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class AebSts_UB:
        sig_name = "AebSts_UB"
        sig_start_bit = 24
        update_id_bit = 24
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
        startbit = 24
        byte = 3
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class BrkPedlInfoQf:
        sig_name = "BrkPedlInfoQf"
        sig_start_bit = 109
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
        startbit = 109
        byte = 13
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class WhlMovgDirFrnt_UB:
        sig_name = "WhlMovgDirFrnt_UB"
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

    class BrkPedlStkStQf:
        sig_name = "BrkPedlStkStQf"
        sig_start_bit = 125
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
        startbit = 125
        byte = 15
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class VehLgtAccelFromWhlSpdWithCmp_UB:
        sig_name = "VehLgtAccelFromWhlSpdWithCmp_UB"
        sig_start_bit = 276
        update_id_bit = 276
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
        startbit = 276
        byte = 34
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class AcbStsPrimAdAllow:
        sig_name = "AcbStsPrimAdAllow"
        sig_start_bit = 5
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AllwdorNot2_NotAllw': 0, 'AllwdorNot2_Allw': 1}
        compute_method = None
        length = 2
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class BrkPedlCrv:
        sig_name = "BrkPedlCrv"
        sig_start_bit = 36
        update_id_bit = 33
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BrkCalParas_Nromal': 0, 'BrkCalParas_Comfort': 1, 'BrkCalParas_Sport': 2, 'BrkCalParas_Reserved1': 3, 'BrkCalParas_Reserved2': 4, 'BrkCalParas_Reserved3': 5}
        compute_method = None
        length = 3
        startbit = 36
        byte = 4
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class BrkPedlCrvAvl:
        sig_name = "BrkPedlCrvAvl"
        sig_start_bit = 32
        update_id_bit = 47
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
        startbit = 32
        byte = 4
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class PropAxleTqAdd_UB:
        sig_name = "PropAxleTqAdd_UB"
        sig_start_bit = 231
        update_id_bit = 231
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
        startbit = 231
        byte = 28
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class EpbMsgReq:
        sig_name = "EpbMsgReq"
        sig_start_bit = 62
        update_id_bit = 58
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 12
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EpbMsg_Msg0': 0, 'EpbMsg_Msg1': 1, 'EpbMsg_Msg2': 2, 'EpbMsg_Msg3': 3, 'EpbMsg_Msg4': 4, 'EpbMsg_Msg5': 5, 'EpbMsg_Msg6': 6, 'EpbMsg_Msg7': 7, 'EpbMsg_Msg8': 8, 'EpbMsg_Msg9': 9, 'EpbMsg_Msg10': 10, 'EpbMsg_Msg11': 11, 'EpbMsg_Msg12': 12}
        compute_method = None
        length = 4
        startbit = 62
        byte = 7
        mask = 0b01111000
        unmask = 0b10000111
        shift = 3

    class DrvrBrkPReq:
        sig_name = "DrvrBrkPReq"
        sig_start_bit = 79
        update_id_bit = 87
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 220
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 79
        byte = 9
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehSpdSafeSpd:
        sig_name = "VehSpdSafeSpd"
        sig_start_bit = 367
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 0.00391
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 31970
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 367
        bmuws_info = [(45, 0b11111111, 0b00000000, 8, 0), (46, 0b11111110, 0b00000001, 7, 1)]

    class VehSpdQf:
        sig_name = "VehSpdQf"
        sig_start_bit = 327
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
        startbit = 327
        byte = 40
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class EpbTotStsChks:
        sig_name = "EpbTotStsChks"
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

    class EpbWarnReq:
        sig_name = "EpbWarnReq"
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
        sig_value_table = {'OnOff2_On': 0, 'OnOff2_Off': 1}
        compute_method = None
        length = 1
        startbit = 57
        byte = 7
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class BrkPedlInfoPsd:
        sig_name = "BrkPedlInfoPsd"
        sig_start_bit = 110
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
        startbit = 110
        byte = 13
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class AcbStsPrim_UB:
        sig_name = "AcbStsPrim_UB"
        sig_start_bit = 8
        update_id_bit = 8
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
        startbit = 8
        byte = 1
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VehLgtAccelFromWhlSpdWithCmpChks:
        sig_name = "VehLgtAccelFromWhlSpdWithCmpChks"
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

    class BrkPedlStk_UB:
        sig_name = "BrkPedlStk_UB"
        sig_start_bit = 152
        update_id_bit = 152
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
        startbit = 152
        byte = 19
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class BrkPedlInfoNotPsd:
        sig_name = "BrkPedlInfoNotPsd"
        sig_start_bit = 111
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
        startbit = 111
        byte = 13
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class EpbLampReqEpbLampReq:
        sig_name = "EpbLampReqEpbLampReq"
        sig_start_bit = 175
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EpbLampReq_On': 0, 'EpbLampReq_Off': 1, 'EpbLampReq_Flash2': 2, 'EpbLampReq_Flash3': 3}
        compute_method = None
        length = 3
        startbit = 175
        byte = 21
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class WhlMovgDirReDirRi:
        sig_name = "WhlMovgDirReDirRi"
        sig_start_bit = 405
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DirRi_Undefined': 0, 'DirRi_Standstill': 1, 'DirRi_Forward': 2, 'DirRi_Backward': 3}
        compute_method = None
        length = 2
        startbit = 405
        byte = 50
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class WhlMovgDirReCntr:
        sig_name = "WhlMovgDirReCntr"
        sig_start_bit = 403
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
        startbit = 403
        byte = 50
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class VehSpdCntr:
        sig_name = "VehSpdCntr"
        sig_start_bit = 323
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
        startbit = 323
        byte = 40
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class AcbStsPrimEpedalAllow:
        sig_name = "AcbStsPrimEpedalAllow"
        sig_start_bit = 1
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AllwdorNot2_NotAllw': 0, 'AllwdorNot2_Allw': 1}
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class EpbTotStsCntr:
        sig_name = "EpbTotStsCntr"
        sig_start_bit = 187
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
        startbit = 187
        byte = 23
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class AcbStsPrimActv:
        sig_name = "AcbStsPrimActv"
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
        sig_value_table = {'Actv_NoActv': 0, 'Actv_Actv': 1, 'Actv_Reserved1': 2, 'Actv_Reserved2': 3}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class VehLgtAccelFromWhlSpdCntr:
        sig_name = "VehLgtAccelFromWhlSpdCntr"
        sig_start_bit = 243
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
        startbit = 243
        byte = 30
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class BrkPedlInfoChks:
        sig_name = "BrkPedlInfoChks"
        sig_start_bit = 103
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
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

    class DrvrBrkTqReq:
        sig_name = "DrvrBrkTqReq"
        sig_start_bit = 46
        update_id_bit = 63
        sig_length = 15
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 32000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 46
        bmuws_info = [(5, 0b01111111, 0b10000000, 7, 0), (6, 0b11111111, 0b00000000, 8, 0)]

    class WhlMovgDirFrntDirLe:
        sig_name = "WhlMovgDirFrntDirLe"
        sig_start_bit = 391
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DirLe_Undefined': 0, 'DirLe_Standstill': 1, 'DirLe_Forward': 2, 'DirLe_Backward': 3}
        compute_method = None
        length = 2
        startbit = 391
        byte = 48
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class VehMovgDir_UB:
        sig_name = "VehMovgDir_UB"
        sig_start_bit = 308
        update_id_bit = 308
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
        startbit = 308
        byte = 38
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class WhlMovgDirFrntChks:
        sig_name = "WhlMovgDirFrntChks"
        sig_start_bit = 383
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 383
        byte = 47
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehLgtAccelFromWhlSpdChks:
        sig_name = "VehLgtAccelFromWhlSpdChks"
        sig_start_bit = 239
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 239
        byte = 29
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehSpd_UB:
        sig_name = "VehSpd_UB"
        sig_start_bit = 324
        update_id_bit = 324
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
        startbit = 324
        byte = 40
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class BrkPedlStkCntr:
        sig_name = "BrkPedlStkCntr"
        sig_start_bit = 123
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
        startbit = 123
        byte = 15
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class VehSpdSafeCntr:
        sig_name = "VehSpdSafeCntr"
        sig_start_bit = 355
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
        startbit = 355
        byte = 44
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class AebStsDenied:
        sig_name = "AebStsDenied"
        sig_start_bit = 19
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DeniedOrNot_NotDenied': 0, 'DeniedOrNot_Denied': 1}
        compute_method = None
        length = 2
        startbit = 19
        byte = 2
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VehMovgDirCntr:
        sig_name = "VehMovgDirCntr"
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

    class VehSpdChks:
        sig_name = "VehSpdChks"
        sig_start_bit = 319
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 319
        byte = 39
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehLgtAccelFromWhlSpdWithCmpQf:
        sig_name = "VehLgtAccelFromWhlSpdWithCmpQf"
        sig_start_bit = 279
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
        startbit = 279
        byte = 34
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class WhlMovgDirFrntDirRi:
        sig_name = "WhlMovgDirFrntDirRi"
        sig_start_bit = 389
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DirRi_Undefined': 0, 'DirRi_Standstill': 1, 'DirRi_Forward': 2, 'DirRi_Backward': 3}
        compute_method = None
        length = 2
        startbit = 389
        byte = 48
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class WhlMovgDirFrntCntr:
        sig_name = "WhlMovgDirFrntCntr"
        sig_start_bit = 387
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
        startbit = 387
        byte = 48
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class BrkPedlInfoCntr:
        sig_name = "BrkPedlInfoCntr"
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

    class AcbStsPrimDecelCompAllow:
        sig_name = "AcbStsPrimDecelCompAllow"
        sig_start_bit = 3
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AllwdorNot2_NotAllw': 0, 'AllwdorNot2_Allw': 1}
        compute_method = None
        length = 2
        startbit = 3
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class BrkPedlStkSt:
        sig_name = "BrkPedlStkSt"
        sig_start_bit = 157
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PsdNotPsd1_NotPsd': 0, 'PsdNotPsd1_Psd': 1}
        compute_method = None
        length = 1
        startbit = 157
        byte = 19
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VehSpdSpd:
        sig_name = "VehSpdSpd"
        sig_start_bit = 335
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 0.00391
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 31970
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 335
        bmuws_info = [(41, 0b11111111, 0b00000000, 8, 0), (42, 0b11111110, 0b00000001, 7, 1)]

    class AebStsActv:
        sig_name = "AebStsActv"
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
        sig_value_table = {'AebActv_NoActv': 0, 'AebActv_AebIb': 1, 'AebActv_AebBa': 2, 'AebActv_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 23
        byte = 2
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class WhlMovgDirReDirLe:
        sig_name = "WhlMovgDirReDirLe"
        sig_start_bit = 407
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DirLe_Undefined': 0, 'DirLe_Standstill': 1, 'DirLe_Forward': 2, 'DirLe_Backward': 3}
        compute_method = None
        length = 2
        startbit = 407
        byte = 50
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class BrkPedlStkAct:
        sig_name = "BrkPedlStkAct"
        sig_start_bit = 135
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
        startbit = 135
        bmuws_info = [(16, 0b11111111, 0b00000000, 8, 0), (17, 0b11111000, 0b00000111, 5, 3)]

    class VehLgtAccelFromWhlSpdWithCmpLgt:
        sig_name = "VehLgtAccelFromWhlSpdWithCmpLgt"
        sig_start_bit = 287
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 0.00097654254
        sig_value_offset = 0
        sig_value_min = -18432
        sig_value_max = 18432
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 287
        bmuws_info = [(35, 0b11111111, 0b00000000, 8, 0), (36, 0b11111111, 0b00000000, 8, 0)]

    class BrkOilLvl:
        sig_name = "BrkOilLvl"
        sig_start_bit = 39
        update_id_bit = 37
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FldLvl_Hi': 0, 'FldLvl_Low': 1, 'FldLvl_Reserved1': 2, 'FldLvl_Reserved2': 3}
        compute_method = None
        length = 2
        startbit = 39
        byte = 4
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class VehLgtAccelFromWhlSpdWithCmpCntr:
        sig_name = "VehLgtAccelFromWhlSpdWithCmpCntr"
        sig_start_bit = 275
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
        startbit = 275
        byte = 34
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class VehSpdSafeQf:
        sig_name = "VehSpdSafeQf"
        sig_start_bit = 359
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
        startbit = 359
        byte = 44
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class EpbPrimSt:
        sig_name = "EpbPrimSt"
        sig_start_bit = 71
        update_id_bit = 68
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 4
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EpbActrSt_Applied': 0, 'EpbActrSt_Released': 1, 'EpbActrSt_Applying': 2, 'EpbActrSt_Releasing': 3, 'EpbActrSt_Unknown': 4, 'EpbActrSt_HoldApplied': 5, 'EpbActrSt_CompleteReleased': 6, 'EpbActrSt_HapPrepared': 7}
        compute_method = None
        length = 3
        startbit = 71
        byte = 8
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class VehSpdSafe_UB:
        sig_name = "VehSpdSafe_UB"
        sig_start_bit = 356
        update_id_bit = 356
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
        startbit = 356
        byte = 44
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class EpbLampReqChks:
        sig_name = "EpbLampReqChks"
        sig_start_bit = 167
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
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

    class VehLgtAccelFromWhlSpd_UB:
        sig_name = "VehLgtAccelFromWhlSpd_UB"
        sig_start_bit = 244
        update_id_bit = 244
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
        startbit = 244
        byte = 30
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class EpbLampReq_UB:
        sig_name = "EpbLampReq_UB"
        sig_start_bit = 154
        update_id_bit = 154
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
        startbit = 154
        byte = 19
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VehSpdSafeChks:
        sig_name = "VehSpdSafeChks"
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


class SRSToCCUMCUCDPropulsionCANFDDiagRespFrame:
    msg_name = "SRSToCCUMCUCDPropulsionCANFDDiagRespFrame"
    msg_id = 1537
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "SRS"
    rx_nodes = ['CCUMCUCD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class EGSMToCCUMCUCDPropulsionCANFDDiagRespFrame:
    msg_name = "EGSMToCCUMCUCDPropulsionCANFDDiagRespFrame"
    msg_id = 1587
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "EGSM"
    rx_nodes = ['CCUMCUCD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class CCUMCUCDToSRSPropulsionCANFDDiagReqFrame:
    msg_name = "CCUMCUCDToSRSPropulsionCANFDDiagReqFrame"
    msg_id = 1793
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "CCUMCUCD"
    rx_nodes = ['SRS']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class ODPPropulsionCANFDNmFr:
    msg_name = "ODPPropulsionCANFDNmFr"
    msg_id = 1297
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "ODP"
    rx_nodes = ['MGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class IEMPropulsionCANFDFr06:
    msg_name = "IEMPropulsionCANFDFr06"
    msg_id = 18
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 32
    tx_node = "IEM"
    rx_nodes = ['ETC', 'CCUMCUCD']
    sig_group_dict = {'ReMotDevelpSignalGroup1': ['ReMotDevelpSignalGroup1DTC1HighByte', 'ReMotDevelpSignalGroup1DTC1LowByte', 'ReMotDevelpSignalGroup1DTC1MiddleByte', 'ReMotDevelpSignalGroup1DTC1Sts', 'ReMotDevelpSignalGroup1DTC2HighByte', 'ReMotDevelpSignalGroup1DTC2LowByte', 'ReMotDevelpSignalGroup1DTC2MiddleByte', 'ReMotDevelpSignalGroup1DTC2Sts'], 'ReMotDevelpSignalGroup3': ['ReMotDevelpSignalGroup3DevelpSignalGroup1', 'ReMotDevelpSignalGroup3DevelpSignalGroup2', 'ReMotDevelpSignalGroup3DevelpSignalGroup3', 'ReMotDevelpSignalGroup3DevelpSignalGroup4', 'ReMotDevelpSignalGroup3DevelpSignalGroup5', 'ReMotDevelpSignalGroup3DevelpSignalGroup6', 'ReMotDevelpSignalGroup3DevelpSignalGroup7', 'ReMotDevelpSignalGroup3DevelpSignalGroup8'], 'ReMotDevelpSignalGroup2': ['ReMotDevelpSignalGroup2DTC1HighByte', 'ReMotDevelpSignalGroup2DTC1LowByte', 'ReMotDevelpSignalGroup2DTC1MiddleByte', 'ReMotDevelpSignalGroup2DTC1Sts', 'ReMotDevelpSignalGroup2DTC2HighByte', 'ReMotDevelpSignalGroup2DTC2LowByte', 'ReMotDevelpSignalGroup2DTC2MiddleByte', 'ReMotDevelpSignalGroup2DTC2Sts']}
    sig_group_dataid_dict = {}

    class ReMotDevelpSignalGroup3DevelpSignalGroup2:
        sig_name = "ReMotDevelpSignalGroup3DevelpSignalGroup2"
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

    class ReMotDevelpSignalGroup2DTC1LowByte:
        sig_name = "ReMotDevelpSignalGroup2DTC1LowByte"
        sig_start_bit = 87
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 87
        byte = 10
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ReMotDevelpSignalGroup1_UB:
        sig_name = "ReMotDevelpSignalGroup1_UB"
        sig_start_bit = 71
        update_id_bit = 71
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
        startbit = 71
        byte = 8
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ReMotDevelpSignalGroup1DTC1LowByte:
        sig_name = "ReMotDevelpSignalGroup1DTC1LowByte"
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

    class ReMotDevelpSignalGroup1DTC1Sts:
        sig_name = "ReMotDevelpSignalGroup1DTC1Sts"
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

    class ReMotDevelpSignalGroup1DTC1MiddleByte:
        sig_name = "ReMotDevelpSignalGroup1DTC1MiddleByte"
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

    class ReMotDevelpSignalGroup3DevelpSignalGroup7:
        sig_name = "ReMotDevelpSignalGroup3DevelpSignalGroup7"
        sig_start_bit = 199
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
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

    class ReMotDevelpSignalGroup3DevelpSignalGroup6:
        sig_name = "ReMotDevelpSignalGroup3DevelpSignalGroup6"
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

    class ReMotDevelpSignalGroup1DTC2MiddleByte:
        sig_name = "ReMotDevelpSignalGroup1DTC2MiddleByte"
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

    class ReMotDevelpSignalGroup3_UB:
        sig_name = "ReMotDevelpSignalGroup3_UB"
        sig_start_bit = 215
        update_id_bit = 215
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
        startbit = 215
        byte = 26
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ReMotDevelpSignalGroup2DTC1MiddleByte:
        sig_name = "ReMotDevelpSignalGroup2DTC1MiddleByte"
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

    class ReMotDevelpSignalGroup1DTC2LowByte:
        sig_name = "ReMotDevelpSignalGroup1DTC2LowByte"
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

    class ReMotDevelpSignalGroup3DevelpSignalGroup4:
        sig_name = "ReMotDevelpSignalGroup3DevelpSignalGroup4"
        sig_start_bit = 175
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
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

    class ReMotDevelpSignalGroup1DTC2HighByte:
        sig_name = "ReMotDevelpSignalGroup1DTC2HighByte"
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

    class ReMotDevelpSignalGroup1DTC1HighByte:
        sig_name = "ReMotDevelpSignalGroup1DTC1HighByte"
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

    class ReMotDevelpSignalGroup2DTC1HighByte:
        sig_name = "ReMotDevelpSignalGroup2DTC1HighByte"
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

    class ReMotDevelpSignalGroup3DevelpSignalGroup1:
        sig_name = "ReMotDevelpSignalGroup3DevelpSignalGroup1"
        sig_start_bit = 151
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 151
        byte = 18
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ReMotDevelpSignalGroup3DevelpSignalGroup8:
        sig_name = "ReMotDevelpSignalGroup3DevelpSignalGroup8"
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

    class ReMotDevelpSignalGroup2DTC2MiddleByte:
        sig_name = "ReMotDevelpSignalGroup2DTC2MiddleByte"
        sig_start_bit = 127
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 127
        byte = 15
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ReMotDevelpSignalGroup3DevelpSignalGroup5:
        sig_name = "ReMotDevelpSignalGroup3DevelpSignalGroup5"
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

    class ReMotDevelpSignalGroup1DTC2Sts:
        sig_name = "ReMotDevelpSignalGroup1DTC2Sts"
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

    class ReMotDevelpSignalGroup2_UB:
        sig_name = "ReMotDevelpSignalGroup2_UB"
        sig_start_bit = 143
        update_id_bit = 143
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
        startbit = 143
        byte = 17
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ReMotDevelpSignalGroup2DTC2LowByte:
        sig_name = "ReMotDevelpSignalGroup2DTC2LowByte"
        sig_start_bit = 119
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 119
        byte = 14
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ReMotDevelpSignalGroup2DTC1Sts:
        sig_name = "ReMotDevelpSignalGroup2DTC1Sts"
        sig_start_bit = 103
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
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

    class ReMotDevelpSignalGroup2DTC2HighByte:
        sig_name = "ReMotDevelpSignalGroup2DTC2HighByte"
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

    class ReMotDevelpSignalGroup3DevelpSignalGroup3:
        sig_name = "ReMotDevelpSignalGroup3DevelpSignalGroup3"
        sig_start_bit = 167
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
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

    class ReMotDevelpSignalGroup2DTC2Sts:
        sig_name = "ReMotDevelpSignalGroup2DTC2Sts"
        sig_start_bit = 135
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 135
        byte = 16
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class BCU1PropulsionCANFDFr04:
    msg_name = "BCU1PropulsionCANFDFr04"
    msg_id = 608
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 16
    tx_node = "BCU1"
    rx_nodes = ['VCU', 'CCUMCUCD', 'ETC']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class IRawBCU1:
        sig_name = "IRawBCU1"
        sig_start_bit = 15
        update_id_bit = 17
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = -400.0
        sig_value_min = 0
        sig_value_max = 8000
        sig_byteorder = "Motorola"
        sig_value_init = 4000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 15
        bmuws_info = [(1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111000, 0b00000111, 5, 3)]

    class URawBCU1:
        sig_name = "URawBCU1"
        sig_start_bit = 16
        update_id_bit = 39
        sig_length = 9
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 16
        bmuws_info = [(2, 0b00000001, 0b11111110, 1, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class BrkSysTemp:
        sig_name = "BrkSysTemp"
        sig_start_bit = 7
        update_id_bit = 18
        sig_length = 8
        sig_value_factor = 4
        sig_value_offset = 0
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


class IEMPropulsionCANFDNmFr:
    msg_name = "IEMPropulsionCANFDNmFr"
    msg_id = 1288
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "IEM"
    rx_nodes = ['EGSM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class CCUMCUCDPropulsionCANFDFr01:
    msg_name = "CCUMCUCDPropulsionCANFDFr01"
    msg_id = 66
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 16
    tx_node = "CCUMCUCD"
    rx_nodes = ['VCU', 'SRS', 'ODP', 'MGM', 'EGSM', 'IEM', 'BECM', 'BCU2', 'CCUMCUAD', 'BCU1']
    sig_group_dict = {'VMMGlbSig': ['VMMGlbSigCarModSts', 'VMMGlbSigChks', 'VMMGlbSigCntr', 'VMMGlbSigCnvincSubSts1', 'VMMGlbSigDrvgSubSts1', 'VMMGlbSigInactvSubSts1', 'VMMGlbSigLoBattModSts', 'VMMGlbSigUsgModSts']}
    sig_group_dataid_dict = {'VMMGlbSig': 1074}

    class VMMGlbSigInactvSubSts1:
        sig_name = "VMMGlbSigInactvSubSts1"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'InactvSubSts_Invalid': 0, 'InactvSubSts_Awake': 1, 'InactvSubSts_UserPresent': 2}
        compute_method = None
        length = 8
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VMMGlbSig_UB:
        sig_name = "VMMGlbSig_UB"
        sig_start_bit = 50
        update_id_bit = 50
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
        startbit = 50
        byte = 6
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VMMGlbSigCnvincSubSts1:
        sig_name = "VMMGlbSigCnvincSubSts1"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CnvincSubSts_Invalid': 0, 'CnvincSubSts_EnterExit': 1, 'CnvincSubSts_AllDoorClosed': 2}
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VMMGlbSigDrvgSubSts1:
        sig_name = "VMMGlbSigDrvgSubSts1"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DrvgSubSts_Invalid': 0, 'DrvgSubSts_Manual': 1, 'DrvgSubSts_Automatic': 2, 'DrvgSubSts_NoTorque': 3}
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VMMGlbSigLoBattModSts:
        sig_name = "VMMGlbSigLoBattModSts"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 55
        byte = 6
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VMMGlbSigCarModSts:
        sig_name = "VMMGlbSigCarModSts"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 8
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CarModStsType_CarModNorm': 0, 'CarModStsType_CarModTrnsp': 1, 'CarModStsType_CarModFcy': 2, 'CarModStsType_CarModExhib': 3, 'CarModStsType_CarModCrash': 8}
        compute_method = None
        length = 4
        startbit = 23
        byte = 2
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class UsgModSts:
        sig_name = "UsgModSts"
        sig_start_bit = 7
        update_id_bit = 3
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 13
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'UsgModSts1_UsgModAbdnd': 0, 'UsgModSts1_UsgModInActv': 1, 'UsgModSts1_UsgModCnvinc': 2, 'UsgModSts1_UsgModDrvg': 13}
        compute_method = None
        length = 4
        startbit = 7
        byte = 0
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class VMMGlbSigChks:
        sig_name = "VMMGlbSigChks"
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

    class VMMGlbSigCntr:
        sig_name = "VMMGlbSigCntr"
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

    class VMMGlbSigUsgModSts:
        sig_name = "VMMGlbSigUsgModSts"
        sig_start_bit = 54
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 13
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'UsgModSts1_UsgModAbdnd': 0, 'UsgModSts1_UsgModInActv': 1, 'UsgModSts1_UsgModCnvinc': 2, 'UsgModSts1_UsgModDrvg': 13}
        compute_method = None
        length = 4
        startbit = 54
        byte = 6
        mask = 0b01111000
        unmask = 0b10000111
        shift = 3


class CCUMCUCDToMGMPropulsionCANFDDiagReqFrame:
    msg_name = "CCUMCUCDToMGMPropulsionCANFDDiagReqFrame"
    msg_id = 1841
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "CCUMCUCD"
    rx_nodes = ['MGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class VCUPropulsionCANFDFr04:
    msg_name = "VCUPropulsionCANFDFr04"
    msg_id = 261
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.025
    msg_length = 16
    tx_node = "VCU"
    rx_nodes = ['ETC', 'MGM', 'IEM', 'BECM']
    sig_group_dict = {'ReMotTqAllwd': ['ReMotTqAllwdChks', 'ReMotTqAllwdCntr', 'ReMotTqAllwdTqAllwd'], 'FrntMotTqAllwd': ['FrntMotTqAllwdChks', 'FrntMotTqAllwdCntr', 'FrntMotTqAllwdTqAllwd']}
    sig_group_dataid_dict = {}

    class FrntMotTqAllwdChks:
        sig_name = "FrntMotTqAllwdChks"
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

    class ReMotTqAllwdCntr:
        sig_name = "ReMotTqAllwdCntr"
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

    class FrntMotTqAllwdCntr:
        sig_name = "FrntMotTqAllwdCntr"
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

    class ReMotTqAllwd_UB:
        sig_name = "ReMotTqAllwd_UB"
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

    class FrntMotTqAllwdTqAllwd:
        sig_name = "FrntMotTqAllwdTqAllwd"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class HVBattChrgnAllwd:
        sig_name = "HVBattChrgnAllwd"
        sig_start_bit = 30
        update_id_bit = 28
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ChrgnAllwd_Init': 0, 'ChrgnAllwd_NOK': 1, 'ChrgnAllwd_OK': 2, 'ChrgnAllwd_HOLD': 3}
        compute_method = None
        length = 2
        startbit = 30
        byte = 3
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class ReMotTqAllwdTqAllwd:
        sig_name = "ReMotTqAllwdTqAllwd"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class FrntMotTqAllwd_UB:
        sig_name = "FrntMotTqAllwd_UB"
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

    class ReMotActvHeatPwrAllwd:
        sig_name = "ReMotActvHeatPwrAllwd"
        sig_start_bit = 23
        update_id_bit = 31
        sig_length = 8
        sig_value_factor = 50
        sig_value_offset = 0
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

    class ReMotTqAllwdChks:
        sig_name = "ReMotTqAllwdChks"
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


class CCUMCUCDPropulsionCANFDFr02:
    msg_name = "CCUMCUCDPropulsionCANFDFr02"
    msg_id = 131
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 32
    tx_node = "CCUMCUCD"
    rx_nodes = ['VCU', 'EGSM', 'BCU2', 'CCUMCUAD', 'BCU1']
    sig_group_dict = {'BrkPedlInfoSec': ['BrkPedlInfoSecChks', 'BrkPedlInfoSecCntr', 'BrkPedlInfoSecPsd', 'BrkPedlInfoSecQf'], 'ScrnGearShiftReq1': ['ScrnGearShiftReq1Chks', 'ScrnGearShiftReq1Cntr', 'ScrnGearShiftReq1GearFltSts', 'ScrnGearShiftReq1GearReq'], 'ScrnGearShiftReq2': ['ScrnGearShiftReq2Chks', 'ScrnGearShiftReq2Cntr', 'ScrnGearShiftReq2GearFltSts', 'ScrnGearShiftReq2GearReq'], 'VehSpdSec': ['VehSpdSecChks', 'VehSpdSecCntr', 'VehSpdSecQf', 'VehSpdSecSpd']}
    sig_group_dataid_dict = {'ScrnGearShiftReq1': 1009, 'ScrnGearShiftReq2': 1010}

    class HbaSoftSwt:
        sig_name = "HbaSoftSwt"
        sig_start_bit = 25
        update_id_bit = 24
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
        startbit = 25
        byte = 3
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class BrkPedlInfoSec_UB:
        sig_name = "BrkPedlInfoSec_UB"
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

    class VehSpdSecQf:
        sig_name = "VehSpdSecQf"
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
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 119
        byte = 14
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class PtActvnReq:
        sig_name = "PtActvnReq"
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
        sig_value_table = {'ReqSts1_NotReqd': 0, 'ReqSts1_Reqd': 1}
        compute_method = None
        length = 1
        startbit = 35
        byte = 4
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class ScrnGearShiftReq1GearFltSts:
        sig_name = "ScrnGearShiftReq1GearFltSts"
        sig_start_bit = 71
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GearFltSts_Normal': 0, 'GearFltSts_PFlt': 1, 'GearFltSts_RFlt': 2, 'GearFltSts_NFlt': 3, 'GearFltSts_DFlt': 4, 'GearFltSts_SrvReq': 5, 'GearFltSts_Reserved1': 6, 'GearFltSts_Reserved2': 7}
        compute_method = None
        length = 3
        startbit = 71
        byte = 8
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class BrkPedlInfoSecPsd:
        sig_name = "BrkPedlInfoSecPsd"
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
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 15
        byte = 1
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ScrnGearShiftReq2Chks:
        sig_name = "ScrnGearShiftReq2Chks"
        sig_start_bit = 87
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 87
        byte = 10
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BrkPedlInfoSecCntr:
        sig_name = "BrkPedlInfoSecCntr"
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

    class ChrgHndlStrtEna:
        sig_name = "ChrgHndlStrtEna"
        sig_start_bit = 21
        update_id_bit = 20
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EnableDisable2_Disabled': 0, 'EnableDisable2_Enabled': 1}
        compute_method = None
        length = 1
        startbit = 21
        byte = 2
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class ScrnGearShiftReq2GearReq:
        sig_name = "ScrnGearShiftReq2GearReq"
        sig_start_bit = 103
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GearLvrIndcn_Default': 0, 'GearLvrIndcn_P': 1, 'GearLvrIndcn_R': 2, 'GearLvrIndcn_N': 3, 'GearLvrIndcn_D': 4, 'GearLvrIndcn_Reserved1': 5, 'GearLvrIndcn_Reserved2': 6, 'GearLvrIndcn_Undefd': 7}
        compute_method = None
        length = 3
        startbit = 103
        byte = 12
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class TowModeSt:
        sig_name = "TowModeSt"
        sig_start_bit = 55
        update_id_bit = 52
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TowMode_NoActv': 0, 'TowMode_Entering': 1, 'TowMode_Actv': 2, 'TowMode_Exiting': 3, 'TowMode_Reserved1': 4, 'TowMode_Reserved2': 5}
        compute_method = None
        length = 3
        startbit = 55
        byte = 6
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class ScrnGearShiftReq1_UB:
        sig_name = "ScrnGearShiftReq1_UB"
        sig_start_bit = 68
        update_id_bit = 68
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
        startbit = 68
        byte = 8
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class ScrnGearShiftReq2Cntr:
        sig_name = "ScrnGearShiftReq2Cntr"
        sig_start_bit = 91
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
        startbit = 91
        byte = 11
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class VehSpdSecCntr:
        sig_name = "VehSpdSecCntr"
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

    class ScrnGearShiftReq2GearFltSts:
        sig_name = "ScrnGearShiftReq2GearFltSts"
        sig_start_bit = 95
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GearFltSts_Normal': 0, 'GearFltSts_PFlt': 1, 'GearFltSts_RFlt': 2, 'GearFltSts_NFlt': 3, 'GearFltSts_DFlt': 4, 'GearFltSts_SrvReq': 5, 'GearFltSts_Reserved1': 6, 'GearFltSts_Reserved2': 7}
        compute_method = None
        length = 3
        startbit = 95
        byte = 11
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class ScrnGearShiftReq2_UB:
        sig_name = "ScrnGearShiftReq2_UB"
        sig_start_bit = 92
        update_id_bit = 92
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
        startbit = 92
        byte = 11
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class HhcSoftSwt:
        sig_name = "HhcSoftSwt"
        sig_start_bit = 37
        update_id_bit = 36
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
        startbit = 37
        byte = 4
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class ScrnGearShiftReq1GearReq:
        sig_name = "ScrnGearShiftReq1GearReq"
        sig_start_bit = 79
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GearLvrIndcn_Default': 0, 'GearLvrIndcn_P': 1, 'GearLvrIndcn_R': 2, 'GearLvrIndcn_N': 3, 'GearLvrIndcn_D': 4, 'GearLvrIndcn_Reserved1': 5, 'GearLvrIndcn_Reserved2': 6, 'GearLvrIndcn_Undefd': 7}
        compute_method = None
        length = 3
        startbit = 79
        byte = 9
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class HdcSoftSwt:
        sig_name = "HdcSoftSwt"
        sig_start_bit = 39
        update_id_bit = 38
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff2_On': 0, 'OnOff2_Off': 1}
        compute_method = None
        length = 1
        startbit = 39
        byte = 4
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ScrnGearShiftReq1Cntr:
        sig_name = "ScrnGearShiftReq1Cntr"
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

    class ScrnGearShiftReq1Chks:
        sig_name = "ScrnGearShiftReq1Chks"
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

    class EpbAutoapplySwt:
        sig_name = "EpbAutoapplySwt"
        sig_start_bit = 27
        update_id_bit = 26
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
        startbit = 27
        byte = 3
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class BrkPedlInfoSecQf:
        sig_name = "BrkPedlInfoSecQf"
        sig_start_bit = 14
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
        startbit = 14
        byte = 1
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class VehSpdSec_UB:
        sig_name = "VehSpdSec_UB"
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

    class VehSpdSecChks:
        sig_name = "VehSpdSecChks"
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

    class BrkPedlInfoSecChks:
        sig_name = "BrkPedlInfoSecChks"
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

    class VehSpdSecSpd:
        sig_name = "VehSpdSecSpd"
        sig_start_bit = 127
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 0.00391
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 31970
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 127
        bmuws_info = [(15, 0b11111111, 0b00000000, 8, 0), (16, 0b11111110, 0b00000001, 7, 1)]

    class EpbSoftSwt:
        sig_name = "EpbSoftSwt"
        sig_start_bit = 47
        update_id_bit = 44
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EpbSoftSwt_NoReq': 0, 'EpbSoftSwt_Apply': 1, 'EpbSoftSwt_Release': 2, 'EpbSoftSwt_Forbidden': 3, 'EpbSoftSwt_Unknown': 4, 'EpbSoftSwt_Reserved': 5}
        compute_method = None
        length = 3
        startbit = 47
        byte = 5
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5


class SRSPropulsionCANFDFr02:
    msg_name = "SRSPropulsionCANFDFr02"
    msg_id = 135
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 48
    tx_node = "SRS"
    rx_nodes = ['CCUMCUCD', 'BCU2', 'VCU']
    sig_group_dict = {'IMUACmpData': ['IMUACmpDataChks', 'IMUACmpDataCntr', 'IMUACmpDataLat', 'IMUACmpDataLatQf', 'IMUACmpDataLgt', 'IMUACmpDataLgtQf', 'IMUACmpDataVert', 'IMUACmpDataVertQf'], 'IMUARawData': ['IMUARawDataChks', 'IMUARawDataCntr', 'IMUARawDataLat', 'IMUARawDataLatQf', 'IMUARawDataLgt', 'IMUARawDataLgtQf', 'IMUARawDataVert', 'IMUARawDataVertQf'], 'IMUAgRawData': ['IMUAgRawDataChks', 'IMUAgRawDataCntr', 'IMUAgRawDataPitch', 'IMUAgRawDataPitchQf', 'IMUAgRawDataRoll', 'IMUAgRawDataRollQf', 'IMUAgRawDataYaw', 'IMUAgRawDataYawQf'], 'IMUAgCmpData': ['IMUAgCmpDataChks', 'IMUAgCmpDataCntr', 'IMUAgCmpDataPitch', 'IMUAgCmpDataPitchQf', 'IMUAgCmpDataRoll', 'IMUAgCmpDataRollQf', 'IMUAgCmpDataYaw', 'IMUAgCmpDataYawQf']}
    sig_group_dataid_dict = {}

    class IMUARawDataLgt:
        sig_name = "IMUARawDataLgt"
        sig_start_bit = 271
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 0.0085
        sig_value_offset = 0
        sig_value_min = -16352
        sig_value_max = 16353
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 271
        bmuws_info = [(33, 0b11111111, 0b00000000, 8, 0), (34, 0b11111110, 0b00000001, 7, 1)]

    class IMUACmpData_UB:
        sig_name = "IMUACmpData_UB"
        sig_start_bit = 85
        update_id_bit = 85
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
        startbit = 85
        byte = 10
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class IMUACmpDataCntr:
        sig_name = "IMUACmpDataCntr"
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

    class IMUARawData_UB:
        sig_name = "IMUARawData_UB"
        sig_start_bit = 301
        update_id_bit = 301
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
        startbit = 301
        byte = 37
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class IMUAgRawDataPitch:
        sig_name = "IMUAgRawDataPitch"
        sig_start_bit = 183
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 0.000244141
        sig_value_offset = 0
        sig_value_min = -24576
        sig_value_max = 24576
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 183
        bmuws_info = [(22, 0b11111111, 0b00000000, 8, 0), (23, 0b11111111, 0b00000000, 8, 0)]

    class IMUARawDataCntr:
        sig_name = "IMUARawDataCntr"
        sig_start_bit = 243
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
        startbit = 243
        byte = 30
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class IMUACmpDataChks:
        sig_name = "IMUACmpDataChks"
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

    class IMUACmpDataLat:
        sig_name = "IMUACmpDataLat"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 0.0085
        sig_value_offset = 0
        sig_value_min = -16352
        sig_value_max = 16353
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111110, 0b00000001, 7, 1)]

    class IMUACmpDataLgt:
        sig_name = "IMUACmpDataLgt"
        sig_start_bit = 55
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 0.0085
        sig_value_offset = 0
        sig_value_min = -16352
        sig_value_max = 16353
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 55
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111110, 0b00000001, 7, 1)]

    class EDRTrig:
        sig_name = "EDRTrig"
        sig_start_bit = 1
        update_id_bit = 10
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EnableDisable3_Invalid': 0, 'EnableDisable3_Disabled': 1, 'EnableDisable3_Enabled': 2}
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class IMUARawDataVertQf:
        sig_name = "IMUARawDataVertQf"
        sig_start_bit = 303
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
        startbit = 303
        byte = 37
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class IMUARawDataLatQf:
        sig_name = "IMUARawDataLatQf"
        sig_start_bit = 247
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
        startbit = 247
        byte = 30
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class CrashEnd:
        sig_name = "CrashEnd"
        sig_start_bit = 7
        update_id_bit = 13
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EnableDisable3_Invalid': 0, 'EnableDisable3_Disabled': 1, 'EnableDisable3_Enabled': 2}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class IMUAgCmpDataYawQf:
        sig_name = "IMUAgCmpDataYawQf"
        sig_start_bit = 159
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
        startbit = 159
        byte = 19
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class IMUAgCmpDataCntr:
        sig_name = "IMUAgCmpDataCntr"
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

    class IMUAgRawData_UB:
        sig_name = "IMUAgRawData_UB"
        sig_start_bit = 229
        update_id_bit = 229
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
        startbit = 229
        byte = 28
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class IMUACmpDataLgtQf:
        sig_name = "IMUACmpDataLgtQf"
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
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 29
        byte = 3
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class CrashSrt:
        sig_name = "CrashSrt"
        sig_start_bit = 5
        update_id_bit = 12
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EnableDisable3_Invalid': 0, 'EnableDisable3_Disabled': 1, 'EnableDisable3_Enabled': 2}
        compute_method = None
        length = 2
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class IMUAgRawDataYawQf:
        sig_name = "IMUAgRawDataYawQf"
        sig_start_bit = 231
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
        startbit = 231
        byte = 28
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class IMUARawDataChks:
        sig_name = "IMUARawDataChks"
        sig_start_bit = 239
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 239
        byte = 29
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class IMUAgRawDataChks:
        sig_name = "IMUAgRawDataChks"
        sig_start_bit = 167
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
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

    class IMUAgRawDataRoll:
        sig_name = "IMUAgRawDataRoll"
        sig_start_bit = 199
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 0.000244141
        sig_value_offset = 0
        sig_value_min = -24576
        sig_value_max = 24576
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 199
        bmuws_info = [(24, 0b11111111, 0b00000000, 8, 0), (25, 0b11111111, 0b00000000, 8, 0)]

    class IMUAgRawDataYaw:
        sig_name = "IMUAgRawDataYaw"
        sig_start_bit = 215
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 0.000244141
        sig_value_offset = 0
        sig_value_min = -24576
        sig_value_max = 24576
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 215
        bmuws_info = [(26, 0b11111111, 0b00000000, 8, 0), (27, 0b11111111, 0b00000000, 8, 0)]

    class IMUAgCmpDataYaw:
        sig_name = "IMUAgCmpDataYaw"
        sig_start_bit = 143
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 0.000244141
        sig_value_offset = 0
        sig_value_min = -24576
        sig_value_max = 24576
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 143
        bmuws_info = [(17, 0b11111111, 0b00000000, 8, 0), (18, 0b11111111, 0b00000000, 8, 0)]

    class IMUACmpDataVert:
        sig_name = "IMUACmpDataVert"
        sig_start_bit = 71
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 0.0085
        sig_value_offset = 0
        sig_value_min = -16352
        sig_value_max = 16353
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 71
        bmuws_info = [(8, 0b11111111, 0b00000000, 8, 0), (9, 0b11111110, 0b00000001, 7, 1)]

    class IMUAgCmpDataPitchQf:
        sig_name = "IMUAgCmpDataPitchQf"
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
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 103
        byte = 12
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class IMUAgRawDataRollQf:
        sig_name = "IMUAgRawDataRollQf"
        sig_start_bit = 173
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
        startbit = 173
        byte = 21
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class IMUACmpDataVertQf:
        sig_name = "IMUACmpDataVertQf"
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
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 87
        byte = 10
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class IMUARawDataVert:
        sig_name = "IMUARawDataVert"
        sig_start_bit = 287
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 0.0085
        sig_value_offset = 0
        sig_value_min = -16352
        sig_value_max = 16353
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 287
        bmuws_info = [(35, 0b11111111, 0b00000000, 8, 0), (36, 0b11111110, 0b00000001, 7, 1)]

    class IMUARawDataLat:
        sig_name = "IMUARawDataLat"
        sig_start_bit = 255
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 0.0085
        sig_value_offset = 0
        sig_value_min = -16352
        sig_value_max = 16353
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 255
        bmuws_info = [(31, 0b11111111, 0b00000000, 8, 0), (32, 0b11111110, 0b00000001, 7, 1)]

    class IMUAgCmpDataRollQf:
        sig_name = "IMUAgCmpDataRollQf"
        sig_start_bit = 101
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
        startbit = 101
        byte = 12
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class IMUARawDataLgtQf:
        sig_name = "IMUARawDataLgtQf"
        sig_start_bit = 245
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
        startbit = 245
        byte = 30
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class RtrctrReqFromRestrntSys:
        sig_name = "RtrctrReqFromRestrntSys"
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
        sig_value_table = {'RtrctrReq_Invalid': 0, 'RtrctrReq_NoActvn': 1, 'RtrctrReq_LowForce': 2, 'RtrctrReq_HighForce': 3}
        compute_method = None
        length = 2
        startbit = 15
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class IMUAgCmpDataPitch:
        sig_name = "IMUAgCmpDataPitch"
        sig_start_bit = 111
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 0.000244141
        sig_value_offset = 0
        sig_value_min = -24576
        sig_value_max = 24576
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 111
        bmuws_info = [(13, 0b11111111, 0b00000000, 8, 0), (14, 0b11111111, 0b00000000, 8, 0)]

    class IMUAgCmpDataChks:
        sig_name = "IMUAgCmpDataChks"
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

    class EDRLockd:
        sig_name = "EDRLockd"
        sig_start_bit = 3
        update_id_bit = 11
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EnableDisable3_Invalid': 0, 'EnableDisable3_Disabled': 1, 'EnableDisable3_Enabled': 2}
        compute_method = None
        length = 2
        startbit = 3
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class IMUAgRawDataCntr:
        sig_name = "IMUAgRawDataCntr"
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

    class IMUACmpDataLatQf:
        sig_name = "IMUACmpDataLatQf"
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
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 31
        byte = 3
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class IMUAgCmpDataRoll:
        sig_name = "IMUAgCmpDataRoll"
        sig_start_bit = 127
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 0.000244141
        sig_value_offset = 0
        sig_value_min = -24576
        sig_value_max = 24576
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 127
        bmuws_info = [(15, 0b11111111, 0b00000000, 8, 0), (16, 0b11111111, 0b00000000, 8, 0)]

    class IMUAgRawDataPitchQf:
        sig_name = "IMUAgRawDataPitchQf"
        sig_start_bit = 175
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
        startbit = 175
        byte = 21
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class IMUAgCmpData_UB:
        sig_name = "IMUAgCmpData_UB"
        sig_start_bit = 157
        update_id_bit = 157
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
        startbit = 157
        byte = 19
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5


class VCUPropulsionCANFDFr02:
    msg_name = "VCUPropulsionCANFDFr02"
    msg_id = 71
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 32
    tx_node = "VCU"
    rx_nodes = ['CCUMCUCD', 'EGSM', 'BCU2', 'CCUMCUAD', 'BCU1']
    sig_group_dict = {'PtSysWhlTqReAct': ['PtSysWhlTqReActChks', 'PtSysWhlTqReActCntr', 'PtSysWhlTqReActPtWhlTqReAct', 'PtSysWhlTqReActPtWhlTqReActQf', 'PtSysWhlTqReActPtWhlTqReLeAct', 'PtSysWhlTqReActPtWhlTqReRiAct'], 'PtSysWhlTqFrntAct': ['PtSysWhlTqFrntActChks', 'PtSysWhlTqFrntActCntr', 'PtSysWhlTqFrntActPtWhlTqActQf', 'PtSysWhlTqFrntActPtWhlTqFrntAct', 'PtSysWhlTqFrntActPtWhlTqFrntLeAct', 'PtSysWhlTqFrntActPtWhlTqFrntRiAct']}
    sig_group_dataid_dict = {'PtSysWhlTqReAct': 1012, 'PtSysWhlTqFrntAct': 1011}

    class PtSysWhlTqFrntActCntr:
        sig_name = "PtSysWhlTqFrntActCntr"
        sig_start_bit = 75
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
        startbit = 75
        byte = 9
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class PtSysWhlTqReActPtWhlTqReRiAct:
        sig_name = "PtSysWhlTqReActPtWhlTqReRiAct"
        sig_start_bit = 183
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 1
        sig_value_offset = -15000.0
        sig_value_min = 0
        sig_value_max = 32767
        sig_byteorder = "Motorola"
        sig_value_init = 15000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 183
        bmuws_info = [(22, 0b11111111, 0b00000000, 8, 0), (23, 0b11111110, 0b00000001, 7, 1)]

    class PtSysTqAxleAvlReMax:
        sig_name = "PtSysTqAxleAvlReMax"
        sig_start_bit = 39
        update_id_bit = 40
        sig_length = 15
        sig_value_factor = 1
        sig_value_offset = -15000.0
        sig_value_min = 0
        sig_value_max = 32767
        sig_byteorder = "Motorola"
        sig_value_init = 15000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111110, 0b00000001, 7, 1)]

    class PtSysWhlTqFrntActPtWhlTqFrntLeAct:
        sig_name = "PtSysWhlTqFrntActPtWhlTqFrntLeAct"
        sig_start_bit = 103
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 1
        sig_value_offset = -15000.0
        sig_value_min = 0
        sig_value_max = 32767
        sig_byteorder = "Motorola"
        sig_value_init = 15000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 103
        bmuws_info = [(12, 0b11111111, 0b00000000, 8, 0), (13, 0b11111110, 0b00000001, 7, 1)]

    class PtSysWhlTqReActPtWhlTqReAct:
        sig_name = "PtSysWhlTqReActPtWhlTqReAct"
        sig_start_bit = 151
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 1
        sig_value_offset = -15000.0
        sig_value_min = 0
        sig_value_max = 32767
        sig_byteorder = "Motorola"
        sig_value_init = 15000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 151
        bmuws_info = [(18, 0b11111111, 0b00000000, 8, 0), (19, 0b11111110, 0b00000001, 7, 1)]

    class PtSysWhlTqFrntActPtWhlTqActQf:
        sig_name = "PtSysWhlTqFrntActPtWhlTqActQf"
        sig_start_bit = 79
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
        startbit = 79
        byte = 9
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class PtSysWhlTqReAct_UB:
        sig_name = "PtSysWhlTqReAct_UB"
        sig_start_bit = 140
        update_id_bit = 140
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
        startbit = 140
        byte = 17
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class PtSysWhlTqFrntAct_UB:
        sig_name = "PtSysWhlTqFrntAct_UB"
        sig_start_bit = 76
        update_id_bit = 76
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
        startbit = 76
        byte = 9
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class PtSysWhlTqFrntActChks:
        sig_name = "PtSysWhlTqFrntActChks"
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

    class PtSysWhlTqReActPtWhlTqReActQf:
        sig_name = "PtSysWhlTqReActPtWhlTqReActQf"
        sig_start_bit = 143
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
        startbit = 143
        byte = 17
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class PtSysWhlTqFrntActPtWhlTqFrntRiAct:
        sig_name = "PtSysWhlTqFrntActPtWhlTqFrntRiAct"
        sig_start_bit = 119
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 1
        sig_value_offset = -15000.0
        sig_value_min = 0
        sig_value_max = 32767
        sig_byteorder = "Motorola"
        sig_value_init = 15000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 119
        bmuws_info = [(14, 0b11111111, 0b00000000, 8, 0), (15, 0b11111110, 0b00000001, 7, 1)]

    class PtSysWhlTqReActPtWhlTqReLeAct:
        sig_name = "PtSysWhlTqReActPtWhlTqReLeAct"
        sig_start_bit = 167
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 1
        sig_value_offset = -15000.0
        sig_value_min = 0
        sig_value_max = 32767
        sig_byteorder = "Motorola"
        sig_value_init = 15000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 167
        bmuws_info = [(20, 0b11111111, 0b00000000, 8, 0), (21, 0b11111110, 0b00000001, 7, 1)]

    class PtSysWhlTqReActChks:
        sig_name = "PtSysWhlTqReActChks"
        sig_start_bit = 135
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 135
        byte = 16
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class PtSysTqAxleAvlFrntMax:
        sig_name = "PtSysTqAxleAvlFrntMax"
        sig_start_bit = 7
        update_id_bit = 8
        sig_length = 15
        sig_value_factor = 1
        sig_value_offset = -15000.0
        sig_value_min = 0
        sig_value_max = 32767
        sig_byteorder = "Motorola"
        sig_value_init = 15000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111110, 0b00000001, 7, 1)]

    class GearLvrIndcnDes:
        sig_name = "GearLvrIndcnDes"
        sig_start_bit = 199
        update_id_bit = 196
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 7
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GearLvrIndcn_Default': 0, 'GearLvrIndcn_P': 1, 'GearLvrIndcn_R': 2, 'GearLvrIndcn_N': 3, 'GearLvrIndcn_D': 4, 'GearLvrIndcn_Reserved1': 5, 'GearLvrIndcn_Reserved2': 6, 'GearLvrIndcn_Undefd': 7}
        compute_method = None
        length = 3
        startbit = 199
        byte = 24
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class PtSysWhlTqFrntActPtWhlTqFrntAct:
        sig_name = "PtSysWhlTqFrntActPtWhlTqFrntAct"
        sig_start_bit = 87
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 1
        sig_value_offset = -15000.0
        sig_value_min = 0
        sig_value_max = 32767
        sig_byteorder = "Motorola"
        sig_value_init = 15000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 87
        bmuws_info = [(10, 0b11111111, 0b00000000, 8, 0), (11, 0b11111110, 0b00000001, 7, 1)]

    class PtSysTqAxleAvlFrntMin:
        sig_name = "PtSysTqAxleAvlFrntMin"
        sig_start_bit = 23
        update_id_bit = 24
        sig_length = 15
        sig_value_factor = 1
        sig_value_offset = -15000.0
        sig_value_min = 0
        sig_value_max = 32767
        sig_byteorder = "Motorola"
        sig_value_init = 15000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111110, 0b00000001, 7, 1)]

    class PtSysWhlTqReActCntr:
        sig_name = "PtSysWhlTqReActCntr"
        sig_start_bit = 139
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
        startbit = 139
        byte = 17
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class PtSysTqAxleAvlReMin:
        sig_name = "PtSysTqAxleAvlReMin"
        sig_start_bit = 55
        update_id_bit = 56
        sig_length = 15
        sig_value_factor = 1
        sig_value_offset = -15000.0
        sig_value_min = 0
        sig_value_max = 32767
        sig_byteorder = "Motorola"
        sig_value_init = 15000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 55
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111110, 0b00000001, 7, 1)]


class VCUPropulsionCANFDFr07:
    msg_name = "VCUPropulsionCANFDFr07"
    msg_id = 389
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 64
    tx_node = "VCU"
    rx_nodes = ['ETC', 'CCUMCUCD', 'ODP', 'MGM', 'IEM', 'BECM']
    sig_group_dict = {'ChrgnEquipMax': ['ChrgnEquipMaxI', 'ChrgnEquipMaxU'], 'DCChrgrPortT': ['DCChrgrPortTNegPortT', 'DCChrgrPortTPosPortT'], 'ImobChkVCU': ['ImobChkVCUChks', 'ImobChkVCUCntr', 'ImobChkVCUImobChkSts', 'ImobChkVCUImobDateChk0', 'ImobChkVCUImobDateChk1', 'ImobChkVCUImobDateChk2', 'ImobChkVCUImobDateChk3', 'ImobChkVCUImobDateChk4', 'ImobChkVCUImobDateChk5']}
    sig_group_dataid_dict = {}

    class DCChrgIReq:
        sig_name = "DCChrgIReq"
        sig_start_bit = 111
        update_id_bit = 138
        sig_length = 16
        sig_value_factor = 0.1
        sig_value_offset = -3000.0
        sig_value_min = 0
        sig_value_max = 65535
        sig_byteorder = "Motorola"
        sig_value_init = 30000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 111
        bmuws_info = [(13, 0b11111111, 0b00000000, 8, 0), (14, 0b11111111, 0b00000000, 8, 0)]

    class ReMotPwrLimMin:
        sig_name = "ReMotPwrLimMin"
        sig_start_bit = 261
        update_id_bit = 266
        sig_length = 11
        sig_value_factor = 0.5
        sig_value_offset = -511.0
        sig_value_min = 0
        sig_value_max = 2044
        sig_byteorder = "Motorola"
        sig_value_init = 1022
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 261
        bmuws_info = [(32, 0b00111111, 0b11000000, 6, 0), (33, 0b11111000, 0b00000111, 5, 3)]

    class ChrgrChrgnUMin:
        sig_name = "ChrgrChrgnUMin"
        sig_start_bit = 95
        update_id_bit = 139
        sig_length = 16
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 65535
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 95
        bmuws_info = [(11, 0b11111111, 0b00000000, 8, 0), (12, 0b11111111, 0b00000000, 8, 0)]

    class DchrgTarSOCLnr:
        sig_name = "DchrgTarSOCLnr"
        sig_start_bit = 161
        update_id_bit = 182
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 2040
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 161
        bmuws_info = [(20, 0b00000011, 0b11111100, 2, 0), (21, 0b11111111, 0b00000000, 8, 0), (22, 0b10000000, 0b01111111, 1, 7)]

    class HVBattChrgnSt:
        sig_name = "HVBattChrgnSt"
        sig_start_bit = 21
        update_id_bit = 19
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'StartFinish1_Start': 0, 'StartFinish1_Finish': 1, 'StartFinish1_Reserved1': 2, 'StartFinish1_Reserved2': 3}
        compute_method = None
        length = 2
        startbit = 21
        byte = 2
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class ImobChkVCUImobDateChk2:
        sig_name = "ImobChkVCUImobDateChk2"
        sig_start_bit = 367
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 367
        byte = 45
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ImobChkVCUChks:
        sig_name = "ImobChkVCUChks"
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

    class ChrgrChrgnUMax:
        sig_name = "ChrgrChrgnUMax"
        sig_start_bit = 79
        update_id_bit = 140
        sig_length = 16
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 65535
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 79
        bmuws_info = [(9, 0b11111111, 0b00000000, 8, 0), (10, 0b11111111, 0b00000000, 8, 0)]

    class HVEgyAllwdForClima:
        sig_name = "HVEgyAllwdForClima"
        sig_start_bit = 210
        update_id_bit = 216
        sig_length = 10
        sig_value_factor = 50
        sig_value_offset = -1.0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 210
        bmuws_info = [(26, 0b00000111, 0b11111000, 3, 0), (27, 0b11111110, 0b00000001, 7, 1)]

    class DCChrgrPortTNegPortT:
        sig_name = "DCChrgrPortTNegPortT"
        sig_start_bit = 311
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -50.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 311
        byte = 38
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class C1TargetChrgU:
        sig_name = "C1TargetChrgU"
        sig_start_bit = 31
        update_id_bit = 143
        sig_length = 16
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 65535
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111111, 0b00000000, 8, 0)]

    class ChrgrChrgnIMin:
        sig_name = "ChrgrChrgnIMin"
        sig_start_bit = 63
        update_id_bit = 141
        sig_length = 16
        sig_value_factor = 0.1
        sig_value_offset = -3000.0
        sig_value_min = 0
        sig_value_max = 65535
        sig_byteorder = "Motorola"
        sig_value_init = 30000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 63
        bmuws_info = [(7, 0b11111111, 0b00000000, 8, 0), (8, 0b11111111, 0b00000000, 8, 0)]

    class ImobStsVCU:
        sig_name = "ImobStsVCU"
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
        sig_value_table = {'ImobSts_Undefd': 0, 'ImobSts_ImobNotPass': 1, 'ImobSts_ImobPass': 2, 'ImobSts_ImobRemPass': 3}
        compute_method = None
        length = 2
        startbit = 11
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class ChrgnEquipMax_UB:
        sig_name = "ChrgnEquipMax_UB"
        sig_start_bit = 264
        update_id_bit = 264
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
        startbit = 264
        byte = 33
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ChrgrChrgnIMax:
        sig_name = "ChrgrChrgnIMax"
        sig_start_bit = 47
        update_id_bit = 142
        sig_length = 16
        sig_value_factor = 0.1
        sig_value_offset = -3000.0
        sig_value_min = 0
        sig_value_max = 65535
        sig_byteorder = "Motorola"
        sig_value_init = 30000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111111, 0b00000000, 8, 0)]

    class DCChrgUReq:
        sig_name = "DCChrgUReq"
        sig_start_bit = 127
        update_id_bit = 137
        sig_length = 16
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 65535
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 127
        bmuws_info = [(15, 0b11111111, 0b00000000, 8, 0), (16, 0b11111111, 0b00000000, 8, 0)]

    class ImobChkVCUImobDateChk1:
        sig_name = "ImobChkVCUImobDateChk1"
        sig_start_bit = 359
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 359
        byte = 44
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BookChrgTarSocLnr:
        sig_name = "BookChrgTarSocLnr"
        sig_start_bit = 7
        update_id_bit = 12
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 2040
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11100000, 0b00011111, 3, 5)]

    class HVLoadActPwr:
        sig_name = "HVLoadActPwr"
        sig_start_bit = 231
        update_id_bit = 237
        sig_length = 10
        sig_value_factor = 20
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 231
        bmuws_info = [(28, 0b11111111, 0b00000000, 8, 0), (29, 0b11000000, 0b00111111, 2, 6)]

    class DCChrgrPortT_UB:
        sig_name = "DCChrgrPortT_UB"
        sig_start_bit = 327
        update_id_bit = 327
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
        startbit = 327
        byte = 40
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ImobChkVCUImobDateChk5:
        sig_name = "ImobChkVCUImobDateChk5"
        sig_start_bit = 391
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 391
        byte = 48
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ReMotPwrLimMax:
        sig_name = "ReMotPwrLimMax"
        sig_start_bit = 241
        update_id_bit = 262
        sig_length = 11
        sig_value_factor = 0.5
        sig_value_offset = -511.0
        sig_value_min = 0
        sig_value_max = 2044
        sig_byteorder = "Motorola"
        sig_value_init = 1022
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 241
        bmuws_info = [(30, 0b00000011, 0b11111100, 2, 0), (31, 0b11111111, 0b00000000, 8, 0), (32, 0b10000000, 0b01111111, 1, 7)]

    class ReMotActvHeatModEna:
        sig_name = "ReMotActvHeatModEna"
        sig_start_bit = 9
        update_id_bit = 22
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HeatModEna_Heatg': 0, 'HeatModEna_PwrLoss': 1, 'HeatModEna_Off': 2, 'HeatModEna_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 9
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class DCChrgrPortTPosPortT:
        sig_name = "DCChrgrPortTPosPortT"
        sig_start_bit = 319
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -50.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 319
        byte = 39
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ImobChkVCUCntr:
        sig_name = "ImobChkVCUCntr"
        sig_start_bit = 339
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
        startbit = 339
        byte = 42
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class HVCnvnPwrAllwd:
        sig_name = "HVCnvnPwrAllwd"
        sig_start_bit = 205
        update_id_bit = 211
        sig_length = 10
        sig_value_factor = 20
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 1023
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 205
        bmuws_info = [(25, 0b00111111, 0b11000000, 6, 0), (26, 0b11110000, 0b00001111, 4, 4)]

    class ImobChkVCUImobDateChk0:
        sig_name = "ImobChkVCUImobDateChk0"
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

    class ChrgILimCoeff:
        sig_name = "ChrgILimCoeff"
        sig_start_bit = 151
        update_id_bit = 157
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
        startbit = 151
        bmuws_info = [(18, 0b11111111, 0b00000000, 8, 0), (19, 0b11000000, 0b00111111, 2, 6)]

    class ImobChkVCUImobDateChk4:
        sig_name = "ImobChkVCUImobDateChk4"
        sig_start_bit = 383
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 383
        byte = 47
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ImobChkVCUImobDateChk3:
        sig_name = "ImobChkVCUImobDateChk3"
        sig_start_bit = 375
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 375
        byte = 46
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DchrgPwrAllwd:
        sig_name = "DchrgPwrAllwd"
        sig_start_bit = 156
        update_id_bit = 162
        sig_length = 10
        sig_value_factor = 20
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 156
        bmuws_info = [(19, 0b00011111, 0b11100000, 5, 0), (20, 0b11111000, 0b00000111, 5, 3)]

    class HVPwrAvlForClimaEstim:
        sig_name = "HVPwrAvlForClimaEstim"
        sig_start_bit = 236
        update_id_bit = 242
        sig_length = 10
        sig_value_factor = 20
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 236
        bmuws_info = [(29, 0b00011111, 0b11100000, 5, 0), (30, 0b11111000, 0b00000111, 5, 3)]

    class ImobChkVCUImobChkSts:
        sig_name = "ImobChkVCUImobChkSts"
        sig_start_bit = 343
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AvlSts1_Avl': 0, 'AvlSts1_NotAvl': 1}
        compute_method = None
        length = 1
        startbit = 343
        byte = 42
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ImobChkVCU_UB:
        sig_name = "ImobChkVCU_UB"
        sig_start_bit = 340
        update_id_bit = 340
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
        startbit = 340
        byte = 42
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class FrntMotPwrLimMin:
        sig_name = "FrntMotPwrLimMin"
        sig_start_bit = 185
        update_id_bit = 206
        sig_length = 11
        sig_value_factor = 0.5
        sig_value_offset = -511.0
        sig_value_min = 0
        sig_value_max = 2044
        sig_byteorder = "Motorola"
        sig_value_init = 1022
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 185
        bmuws_info = [(23, 0b00000011, 0b11111100, 2, 0), (24, 0b11111111, 0b00000000, 8, 0), (25, 0b10000000, 0b01111111, 1, 7)]

    class FrntMotPwrLimMax:
        sig_name = "FrntMotPwrLimMax"
        sig_start_bit = 181
        update_id_bit = 186
        sig_length = 11
        sig_value_factor = 0.5
        sig_value_offset = -511.0
        sig_value_min = 0
        sig_value_max = 2044
        sig_byteorder = "Motorola"
        sig_value_init = 1022
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 181
        bmuws_info = [(22, 0b00111111, 0b11000000, 6, 0), (23, 0b11111000, 0b00000111, 5, 3)]

    class ChrgnEquipMaxI:
        sig_name = "ChrgnEquipMaxI"
        sig_start_bit = 279
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 0.1
        sig_value_offset = -3000.0
        sig_value_min = 0
        sig_value_max = 65535
        sig_byteorder = "Motorola"
        sig_value_init = 30000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 279
        bmuws_info = [(34, 0b11111111, 0b00000000, 8, 0), (35, 0b11111111, 0b00000000, 8, 0)]

    class ChrgnEquipMaxU:
        sig_name = "ChrgnEquipMaxU"
        sig_start_bit = 295
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 65535
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 295
        bmuws_info = [(36, 0b11111111, 0b00000000, 8, 0), (37, 0b11111111, 0b00000000, 8, 0)]


class VCUToCCUMCUCDOBDPropulsionCANFDDiagRespFrame:
    msg_name = "VCUToCCUMCUCDOBDPropulsionCANFDDiagRespFrame"
    msg_id = 2024
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "VCU"
    rx_nodes = ['CCUMCUCD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class MGMPropulsionCANFDFr01:
    msg_name = "MGMPropulsionCANFDFr01"
    msg_id = 68
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 32
    tx_node = "MGM"
    rx_nodes = ['VCU', 'CCUMCUCD', 'CCUMCUAD', 'BCU1']
    sig_group_dict = {'FrntMotTqAvl': ['FrntMotTqAvlHVMotorTqAvlMax', 'FrntMotTqAvlHVMotorTqAvlMin'], 'FrntMotTqAct': ['FrntMotTqActChks', 'FrntMotTqActCntr', 'FrntMotTqActTq', 'FrntMotTqActTqQf'], 'DmcStsFrnt': ['DmcStsFrntChks', 'DmcStsFrntCntr', 'DmcStsFrntDmcSt', 'DmcStsFrntDmcSwInfo', 'DmcStsFrntDmcTarTq'], 'FrntMotSpdActSafe': ['FrntMotSpdActSafeChks', 'FrntMotSpdActSafeCntr', 'FrntMotSpdActSafeMotorSpdActSafe', 'FrntMotSpdActSafeQf']}
    sig_group_dataid_dict = {'FrntMotTqAct': 1062, 'FrntMotSpdActSafe': 1019}

    class FrntMotSpdActSafeMotorSpdActSafe:
        sig_name = "FrntMotSpdActSafeMotorSpdActSafe"
        sig_start_bit = 103
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = -32768
        sig_value_max = 32767
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 103
        bmuws_info = [(12, 0b11111111, 0b00000000, 8, 0), (13, 0b11111111, 0b00000000, 8, 0)]

    class FrntMotSpdAct:
        sig_name = "FrntMotSpdAct"
        sig_start_bit = 63
        update_id_bit = 78
        sig_length = 16
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = -32768
        sig_value_max = 32767
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 63
        bmuws_info = [(7, 0b11111111, 0b00000000, 8, 0), (8, 0b11111111, 0b00000000, 8, 0)]

    class DmcStsFrntDmcSt:
        sig_name = "DmcStsFrntDmcSt"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DmcSt_Init': 0, 'DmcSt_On': 1, 'DmcSt_Off': 2, 'DmcSt_Fault': 3}
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class FrntMotTqAvl_UB:
        sig_name = "FrntMotTqAvl_UB"
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

    class DmcStsFrntChks:
        sig_name = "DmcStsFrntChks"
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

    class FrntMotSpdActSafeChks:
        sig_name = "FrntMotSpdActSafeChks"
        sig_start_bit = 87
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 87
        byte = 10
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntMotTqActCntr:
        sig_name = "FrntMotTqActCntr"
        sig_start_bit = 123
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
        startbit = 123
        byte = 15
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DmcStsFrntDmcSwInfo:
        sig_name = "DmcStsFrntDmcSwInfo"
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

    class FrntMotTqActTq:
        sig_name = "FrntMotTqActTq"
        sig_start_bit = 135
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 1
        sig_value_offset = -15000.0
        sig_value_min = 0
        sig_value_max = 32767
        sig_byteorder = "Motorola"
        sig_value_init = 15000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 135
        bmuws_info = [(16, 0b11111111, 0b00000000, 8, 0), (17, 0b11111110, 0b00000001, 7, 1)]

    class FrntMotDampgModSts:
        sig_name = "FrntMotDampgModSts"
        sig_start_bit = 54
        update_id_bit = 52
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'MotDampgMod_NoDampg': 0, 'MotDampgMod_LoDampg': 1, 'MotDampgMod_MeDampg': 2, 'MotDampgMod_HiDampg': 3}
        compute_method = None
        length = 2
        startbit = 54
        byte = 6
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class DmcStsFrntCntr:
        sig_name = "DmcStsFrntCntr"
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

    class FrntMotTqActChks:
        sig_name = "FrntMotTqActChks"
        sig_start_bit = 119
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 119
        byte = 14
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntMotTqAct_UB:
        sig_name = "FrntMotTqAct_UB"
        sig_start_bit = 124
        update_id_bit = 124
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
        startbit = 124
        byte = 15
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class FrntMotTqAvlHVMotorTqAvlMax:
        sig_name = "FrntMotTqAvlHVMotorTqAvlMax"
        sig_start_bit = 151
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 4
        sig_value_offset = -8188.0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 2047
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 151
        bmuws_info = [(18, 0b11111111, 0b00000000, 8, 0), (19, 0b11110000, 0b00001111, 4, 4)]

    class FrntMotTqAvlHVMotorTqAvlMin:
        sig_name = "FrntMotTqAvlHVMotorTqAvlMin"
        sig_start_bit = 155
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 4
        sig_value_offset = -8188.0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 2047
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 155
        bmuws_info = [(19, 0b00001111, 0b11110000, 4, 0), (20, 0b11111111, 0b00000000, 8, 0)]

    class DmcStsFrnt_UB:
        sig_name = "DmcStsFrnt_UB"
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

    class FrntMotSpdActSafe_UB:
        sig_name = "FrntMotSpdActSafe_UB"
        sig_start_bit = 92
        update_id_bit = 92
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
        startbit = 92
        byte = 11
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class FrntMotTqActTqQf:
        sig_name = "FrntMotTqActTqQf"
        sig_start_bit = 127
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
        startbit = 127
        byte = 15
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class DmcStsFrntDmcTarTq:
        sig_name = "DmcStsFrntDmcTarTq"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = -30000
        sig_value_max = 30000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class FrntMotSpdActSafeCntr:
        sig_name = "FrntMotSpdActSafeCntr"
        sig_start_bit = 91
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
        startbit = 91
        byte = 11
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class FrntMotModSts:
        sig_name = "FrntMotModSts"
        sig_start_bit = 51
        update_id_bit = 79
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'MotModSts_Inin': 0, 'MotModSts_MonChk': 1, 'MotModSts_Stb': 2, 'MotModSts_PreChrg': 3, 'MotModSts_HVReady': 4, 'MotModSts_TqCtrl': 5, 'MotModSts_PwrDwn': 6, 'MotModSts_Flt': 7, 'MotModSts_TCSCtrl': 8, 'MotModSts_DTCSCtrl': 9, 'MotModSts_ActiveDsicharge': 10, 'MotModSts_PassiveDsicharge': 11, 'MotModSts_ActiveHeat': 12, 'MotModSts_Boost': 13, 'MotModSts_PulseHeat': 14, 'MotModSts_SpdCtrl': 15}
        compute_method = None
        length = 4
        startbit = 51
        byte = 6
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class FrntMotSpdActSafeQf:
        sig_name = "FrntMotSpdActSafeQf"
        sig_start_bit = 95
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
        startbit = 95
        byte = 11
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class CCUMCUCDToIEMPropulsionCANFDDiagReqFrame:
    msg_name = "CCUMCUCDToIEMPropulsionCANFDDiagReqFrame"
    msg_id = 1847
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "CCUMCUCD"
    rx_nodes = ['IEM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class SRSToCCUMCUCDOBDPropulsionCANFDDiagRespFrame:
    msg_name = "SRSToCCUMCUCDOBDPropulsionCANFDDiagRespFrame"
    msg_id = 2041
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "SRS"
    rx_nodes = ['CCUMCUCD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class BECMPropulsionCANFDFr01:
    msg_name = "BECMPropulsionCANFDFr01"
    msg_id = 130
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 48
    tx_node = "BECM"
    rx_nodes = ['VCU', 'CCUMCUCD', 'ODP', 'MGM', 'IEM']
    sig_group_dict = {'HVMainRlySts': ['HVMainRlyStsChks', 'HVMainRlyStsCntr', 'HVMainRlyStsMainRly1'], 'HVBattThermRunAway': ['HVBattThermRunAwayErrSts', 'HVBattThermRunAwaySts']}
    sig_group_dataid_dict = {'HVMainRlySts': 1016}

    class HVBattSelfAwakeDetn:
        sig_name = "HVBattSelfAwakeDetn"
        sig_start_bit = 125
        update_id_bit = 124
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
        startbit = 125
        byte = 15
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class HVBattAmntPwrLimDchaSoft:
        sig_name = "HVBattAmntPwrLimDchaSoft"
        sig_start_bit = 31
        update_id_bit = 76
        sig_length = 12
        sig_value_factor = 0.25
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11110000, 0b00001111, 4, 4)]

    class HVMainRlyStsCntr:
        sig_name = "HVMainRlyStsCntr"
        sig_start_bit = 163
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
        startbit = 163
        byte = 20
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class HVMainRlyPosSts:
        sig_name = "HVMainRlyPosSts"
        sig_start_bit = 135
        update_id_bit = 132
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'QCRlySt_Open': 0, 'QCRlySt_Closed': 1, 'QCRlySt_StuckOpen': 2, 'QCRlySt_StuckClosed': 3, 'QCRlySt_Reserved1': 4, 'QCRlySt_Reserved2': 5, 'QCRlySt_Reserved3': 6, 'QCRlySt_Reserved4': 7}
        compute_method = None
        length = 3
        startbit = 135
        byte = 16
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class HVPreChrgRlySts:
        sig_name = "HVPreChrgRlySts"
        sig_start_bit = 131
        update_id_bit = 128
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'QCRlySt_Open': 0, 'QCRlySt_Closed': 1, 'QCRlySt_StuckOpen': 2, 'QCRlySt_StuckClosed': 3, 'QCRlySt_Reserved1': 4, 'QCRlySt_Reserved2': 5, 'QCRlySt_Reserved3': 6, 'QCRlySt_Reserved4': 7}
        compute_method = None
        length = 3
        startbit = 131
        byte = 16
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class HVMainRlyNegSts:
        sig_name = "HVMainRlyNegSts"
        sig_start_bit = 123
        update_id_bit = 120
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'QCRlySt_Open': 0, 'QCRlySt_Closed': 1, 'QCRlySt_StuckOpen': 2, 'QCRlySt_StuckClosed': 3, 'QCRlySt_Reserved1': 4, 'QCRlySt_Reserved2': 5, 'QCRlySt_Reserved3': 6, 'QCRlySt_Reserved4': 7}
        compute_method = None
        length = 3
        startbit = 123
        byte = 15
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class FastBoostRlySt:
        sig_name = "FastBoostRlySt"
        sig_start_bit = 35
        update_id_bit = 79
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'QCRlySt_Open': 0, 'QCRlySt_Closed': 1, 'QCRlySt_StuckOpen': 2, 'QCRlySt_StuckClosed': 3, 'QCRlySt_Reserved1': 4, 'QCRlySt_Reserved2': 5, 'QCRlySt_Reserved3': 6, 'QCRlySt_Reserved4': 7}
        compute_method = None
        length = 3
        startbit = 35
        byte = 4
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class HVBattAmntPwrLimDcha1:
        sig_name = "HVBattAmntPwrLimDcha1"
        sig_start_bit = 11
        update_id_bit = 77
        sig_length = 12
        sig_value_factor = 0.25
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

    class HVBattQCNRlySt:
        sig_name = "HVBattQCNRlySt"
        sig_start_bit = 87
        update_id_bit = 84
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'QCRlySt_Open': 0, 'QCRlySt_Closed': 1, 'QCRlySt_StuckOpen': 2, 'QCRlySt_StuckClosed': 3, 'QCRlySt_Reserved1': 4, 'QCRlySt_Reserved2': 5, 'QCRlySt_Reserved3': 6, 'QCRlySt_Reserved4': 7}
        compute_method = None
        length = 3
        startbit = 87
        byte = 10
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class HVMainRlyStsMainRly1:
        sig_name = "HVMainRlyStsMainRly1"
        sig_start_bit = 167
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'MainRly1_Open': 0, 'MainRly1_Clsd': 1, 'MainRly1_KeepSt': 2, 'MainRly1_OpenAndReqActvDcha': 3}
        compute_method = None
        length = 2
        startbit = 167
        byte = 20
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HVBattThermRunAwayErrSts:
        sig_name = "HVBattThermRunAwayErrSts"
        sig_start_bit = 95
        update_id_bit = None
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
        startbit = 95
        bmuws_info = [(11, 0b11111111, 0b00000000, 8, 0), (12, 0b11111111, 0b00000000, 8, 0), (13, 0b11111111, 0b00000000, 8, 0), (14, 0b11111111, 0b00000000, 8, 0)]

    class HVBattThermRunAwaySts:
        sig_name = "HVBattThermRunAwaySts"
        sig_start_bit = 127
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
        startbit = 127
        byte = 15
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class HVMainRlySts_UB:
        sig_name = "HVMainRlySts_UB"
        sig_start_bit = 164
        update_id_bit = 164
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
        startbit = 164
        byte = 20
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class HVSysSt:
        sig_name = "HVSysSt"
        sig_start_bit = 137
        update_id_bit = 151
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HVSysSt_Inin': 0, 'HVSysSt_Test': 1, 'HVSysSt_Rdy': 2}
        compute_method = None
        length = 2
        startbit = 137
        byte = 17
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class HVBattAmntPwrLimChrg1:
        sig_name = "HVBattAmntPwrLimChrg1"
        sig_start_bit = 7
        update_id_bit = 78
        sig_length = 12
        sig_value_factor = 0.25
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11110000, 0b00001111, 4, 4)]

    class HVBattLimnIndcnInfo:
        sig_name = "HVBattLimnIndcnInfo"
        sig_start_bit = 47
        update_id_bit = 75
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

    class HVBattThermRunAway_UB:
        sig_name = "HVBattThermRunAway_UB"
        sig_start_bit = 126
        update_id_bit = 126
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
        startbit = 126
        byte = 15
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class HVSysActvInhb:
        sig_name = "HVSysActvInhb"
        sig_start_bit = 143
        update_id_bit = 141
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffCrit1_NotVld1': 0, 'OnOffCrit1_Off': 1, 'OnOffCrit1_On': 2, 'OnOffCrit1_NotVld2': 3}
        compute_method = None
        length = 2
        startbit = 143
        byte = 17
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HVBattQCPRlySt:
        sig_name = "HVBattQCPRlySt"
        sig_start_bit = 83
        update_id_bit = 80
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'QCRlySt_Open': 0, 'QCRlySt_Closed': 1, 'QCRlySt_StuckOpen': 2, 'QCRlySt_StuckClosed': 3, 'QCRlySt_Reserved1': 4, 'QCRlySt_Reserved2': 5, 'QCRlySt_Reserved3': 6, 'QCRlySt_Reserved4': 7}
        compute_method = None
        length = 3
        startbit = 83
        byte = 10
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class HVMainRlyStsChks:
        sig_name = "HVMainRlyStsChks"
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

    class HVBattPackU:
        sig_name = "HVBattPackU"
        sig_start_bit = 63
        update_id_bit = 74
        sig_length = 16
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 65535
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 63
        bmuws_info = [(7, 0b11111111, 0b00000000, 8, 0), (8, 0b11111111, 0b00000000, 8, 0)]

    class HVSysPwrOffReq:
        sig_name = "HVSysPwrOffReq"
        sig_start_bit = 140
        update_id_bit = 138
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ReqSts2_Default': 0, 'ReqSts2_NotReqd': 1, 'ReqSts2_Reqd': 2, 'ReqSts2_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 140
        byte = 17
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3


class ODPPropulsionCANFDFr02:
    msg_name = "ODPPropulsionCANFDFr02"
    msg_id = 615
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 16
    tx_node = "ODP"
    rx_nodes = ['VCU', 'CCUMCUCD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class DCDCCooltFlwReq:
        sig_name = "DCDCCooltFlwReq"
        sig_start_bit = 63
        update_id_bit = 70
        sig_length = 9
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 500
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 63
        bmuws_info = [(7, 0b11111111, 0b00000000, 8, 0), (8, 0b10000000, 0b01111111, 1, 7)]

    class OnBdChrgrCooltT:
        sig_name = "OnBdChrgrCooltT"
        sig_start_bit = 27
        update_id_bit = 46
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = -256.0
        sig_value_min = 0
        sig_value_max = 5119
        sig_byteorder = "Motorola"
        sig_value_init = 2560
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 27
        bmuws_info = [(3, 0b00001111, 0b11110000, 4, 0), (4, 0b11111111, 0b00000000, 8, 0), (5, 0b10000000, 0b01111111, 1, 7)]

    class DCDCCooltT:
        sig_name = "DCDCCooltT"
        sig_start_bit = 7
        update_id_bit = 10
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = -256.0
        sig_value_min = 0
        sig_value_max = 5119
        sig_byteorder = "Motorola"
        sig_value_init = 2560
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111000, 0b00000111, 5, 3)]

    class OnBdChrgrT:
        sig_name = "OnBdChrgrT"
        sig_start_bit = 45
        update_id_bit = 48
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = -256.0
        sig_value_min = 0
        sig_value_max = 5119
        sig_byteorder = "Motorola"
        sig_value_init = 2560
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 45
        bmuws_info = [(5, 0b00111111, 0b11000000, 6, 0), (6, 0b11111110, 0b00000001, 7, 1)]

    class DCDCCoolgReq:
        sig_name = "DCDCCoolgReq"
        sig_start_bit = 75
        update_id_bit = 74
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
        startbit = 75
        byte = 9
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class DCDCTAct:
        sig_name = "DCDCTAct"
        sig_start_bit = 9
        update_id_bit = 28
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = -256.0
        sig_value_min = 0
        sig_value_max = 5119
        sig_byteorder = "Motorola"
        sig_value_init = 2560
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 9
        bmuws_info = [(1, 0b00000011, 0b11111100, 2, 0), (2, 0b11111111, 0b00000000, 8, 0), (3, 0b11100000, 0b00011111, 3, 5)]

    class OnBdChrgrCoolgReq:
        sig_name = "OnBdChrgrCoolgReq"
        sig_start_bit = 73
        update_id_bit = 72
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
        startbit = 73
        byte = 9
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class OnBdChrgrCooltFlwReq:
        sig_name = "OnBdChrgrCooltFlwReq"
        sig_start_bit = 69
        update_id_bit = 76
        sig_length = 9
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 500
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 69
        bmuws_info = [(8, 0b00111111, 0b11000000, 6, 0), (9, 0b11100000, 0b00011111, 3, 5)]


class CCUMCUCDToAllPropulsionCANFDDiagFuncReqFrame:
    msg_name = "CCUMCUCDToAllPropulsionCANFDDiagFuncReqFrame"
    msg_id = 2047
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CCUMCUCD"
    rx_nodes = ['SRS', 'ODP', 'MGM', 'EGSM', 'IEM', 'BECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class BECMPropulsionCANFDFr02:
    msg_name = "BECMPropulsionCANFDFr02"
    msg_id = 277
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.03
    msg_length = 8
    tx_node = "BECM"
    rx_nodes = ['VCU', 'CCUMCUCD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HVBattPackIDC:
        sig_name = "HVBattPackIDC"
        sig_start_bit = 7
        update_id_bit = 21
        sig_length = 16
        sig_value_factor = 0.1
        sig_value_offset = -3000.0
        sig_value_min = 0
        sig_value_max = 65535
        sig_byteorder = "Motorola"
        sig_value_init = 65535
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class HVBattSOCCorrnFlg:
        sig_name = "HVBattSOCCorrnFlg"
        sig_start_bit = 23
        update_id_bit = 20
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffCrit1_NotVld1': 0, 'OnOffCrit1_Off': 1, 'OnOffCrit1_On': 2, 'OnOffCrit1_NotVld2': 3}
        compute_method = None
        length = 2
        startbit = 23
        byte = 2
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class BCU2PropulsionCANFDFr02:
    msg_name = "BCU2PropulsionCANFDFr02"
    msg_id = 129
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "BCU2"
    rx_nodes = ['VCU', 'CCUMCUCD', 'CCUMCUAD', 'BCU1']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class EpbSecSt:
        sig_name = "EpbSecSt"
        sig_start_bit = 7
        update_id_bit = 4
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 4
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EpbActrSt_Applied': 0, 'EpbActrSt_Released': 1, 'EpbActrSt_Applying': 2, 'EpbActrSt_Releasing': 3, 'EpbActrSt_Unknown': 4, 'EpbActrSt_HoldApplied': 5, 'EpbActrSt_CompleteReleased': 6, 'EpbActrSt_HapPrepared': 7}
        compute_method = None
        length = 3
        startbit = 7
        byte = 0
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5


class EGSMPropulsionCANFDNmFr:
    msg_name = "EGSMPropulsionCANFDNmFr"
    msg_id = 1287
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "EGSM"
    rx_nodes = ['CCUMCUCD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class IEMPropulsionCANFDFr03:
    msg_name = "IEMPropulsionCANFDFr03"
    msg_id = 279
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.03
    msg_length = 8
    tx_node = "IEM"
    rx_nodes = ['VCU', 'BCU1']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class ReMotActvDchgSts:
        sig_name = "ReMotActvDchgSts"
        sig_start_bit = 4
        update_id_bit = 0
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 6
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ActvDchgSts_Initial': 0, 'ActvDchgSts_Inactive': 1, 'ActvDchgSts_Active': 2, 'ActvDchgSts_Finished': 3, 'ActvDchgSts_Timeout': 4, 'ActvDchgSts_Reserved1': 5, 'ActvDchgSts_Reserved2': 6}
        compute_method = None
        length = 3
        startbit = 4
        byte = 0
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class ReMot3PhaShoCricSt:
        sig_name = "ReMot3PhaShoCricSt"
        sig_start_bit = 7
        update_id_bit = 1
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ThreePhaShoCricSts_Initial': 0, 'ThreePhaShoCricSts_NoShoCirc': 1, 'ThreePhaShoCricSts_UpprShoCirc': 2, 'ThreePhaShoCricSts_UndrShoCirc': 3, 'ThreePhaShoCricSts_Others': 4, 'ThreePhaShoCricSts_Unknown': 5, 'ThreePhaShoCricSts_Reserved1': 6, 'ThreePhaShoCricSts_Reserved2': 7}
        compute_method = None
        length = 3
        startbit = 7
        byte = 0
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class ReMotLimnIndcn:
        sig_name = "ReMotLimnIndcn"
        sig_start_bit = 15
        update_id_bit = 31
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
        startbit = 15
        bmuws_info = [(1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111111, 0b00000000, 8, 0)]


class CCUMCUCDPropulsionCANFDFr08:
    msg_name = "CCUMCUCDPropulsionCANFDFr08"
    msg_id = 611
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 64
    tx_node = "CCUMCUCD"
    rx_nodes = ['VCU', 'SRS', 'ODP', 'MGM', 'EGSM', 'IEM', 'BECM', 'BCU2', 'CCUMCUAD', 'BCU1']
    sig_group_dict = {'VirtGearShiftModeReq': ['VirtGearShiftModeReqChks', 'VirtGearShiftModeReqCntr', 'VirtGearShiftModeReqVirtShiftModeSts'], 'LoadPwrActSts': ['LoadPwrActStsACCMPwrActSts', 'LoadPwrActStsAFUPwrActSts', 'LoadPwrActStsAGMPwrActSts', 'LoadPwrActStsAGUPwrActSts', 'LoadPwrActStsALMLPwrActSts', 'LoadPwrActStsALMRPwrActSts', 'LoadPwrActStsAWMPwrActSts', 'LoadPwrActStsBCCPPwrActSts', 'LoadPwrActStsBCFVPwrActSts', 'LoadPwrActStsBCTVPwrActSts', 'LoadPwrActStsBEXVPwrActSts', 'LoadPwrActStsBNCMPwrActSts', 'LoadPwrActStsBoosterBlowerPwrActSts', 'LoadPwrActStsCCTVPwrActSts', 'LoadPwrActStsCDPwrActSts', 'LoadPwrActStsCERVPwrActSts', 'LoadPwrActStsCRCMPwrActSts', 'LoadPwrActStsCSOVPwrActSts', 'LoadPwrActStsDCTVPwrActSts', 'LoadPwrActStsDICPwrActSts', 'LoadPwrActStsDMFLPwrActSts', 'LoadPwrActStsDPODPwrActSts', 'LoadPwrActStsDRFPwrActSts', 'LoadPwrActStsDRMFRPwrActSts', 'LoadPwrActStsDRMRLPwrActSts', 'LoadPwrActStsDRMRRPwrActSts', 'LoadPwrActStsECTVPwrActSts', 'LoadPwrActStsEDCPPwrActSts', 'LoadPwrActStsEGSMPwrActSts', 'LoadPwrActStsEPMPwrActSts', 'LoadPwrActStsFCSIPwrActSts', 'LoadPwrActStsFEXVPwrActSts', 'LoadPwrActStsFLRPwrActSts', 'LoadPwrActStsFSRLPwrActSts', 'LoadPwrActStsFSRRPwrActSts', 'LoadPwrActStsHBMFPwrActSts', 'LoadPwrActStsHBMRPwrActSts', 'LoadPwrActStsHCCPPwrActSts', 'LoadPwrActStsHCMLPwrActSts', 'LoadPwrActStsHCMRPwrActSts', 'LoadPwrActStsHCTVPwrActSts', 'LoadPwrActStsHODPwrActSts', 'LoadPwrActStsHUBFPwrActSts', 'LoadPwrActStsHUBRPwrActSts', 'LoadPwrActStsHVAHPwrActSts', 'LoadPwrActStsHVCHPwrActSts', 'LoadPwrActStsHVCMPwrActSts', 'LoadPwrActStsIEMPwrActSts', 'LoadPwrActStsIRMMPwrActSts', 'LoadPwrActStsLCTVPwrActSts', 'LoadPwrActStsLPODPwrActSts', 'LoadPwrActStsMGMPwrActSts', 'LoadPwrActStsMMDPwrActSts', 'LoadPwrActStsMMPPwrActSts', 'LoadPwrActStsNKRPwrActSts', 'LoadPwrActStsOHCPwrActSts', 'LoadPwrActStsOPCFPwrActSts', 'LoadPwrActStsOPCRPwrActSts', 'LoadPwrActStsPMSIPwrActSts', 'LoadPwrActStsPOFPwrActSts', 'LoadPwrActStsPORPwrActSts', 'LoadPwrActStsPPODPwrActSts', 'LoadPwrActStsRCMLPwrActSts', 'LoadPwrActStsRCMRPwrActSts', 'LoadPwrActStsReserved1', 'LoadPwrActStsReserved10', 'LoadPwrActStsReserved11', 'LoadPwrActStsReserved12', 'LoadPwrActStsReserved13', 'LoadPwrActStsReserved14', 'LoadPwrActStsReserved15', 'LoadPwrActStsReserved16', 'LoadPwrActStsReserved17', 'LoadPwrActStsReserved18', 'LoadPwrActStsReserved2', 'LoadPwrActStsReserved3', 'LoadPwrActStsReserved4', 'LoadPwrActStsReserved5', 'LoadPwrActStsReserved6', 'LoadPwrActStsReserved7', 'LoadPwrActStsReserved8', 'LoadPwrActStsReserved9', 'LoadPwrActStsREXVPwrActSts', 'LoadPwrActStsRLMMPwrActSts', 'LoadPwrActStsRLSMPwrActSts', 'LoadPwrActStsRMLPwrActSts', 'LoadPwrActStsRPODPwrActSts', 'LoadPwrActStsRRMMPwrActSts', 'LoadPwrActStsRSOV1PwrActSts', 'LoadPwrActStsRSOV2PwrActSts', 'LoadPwrActStsSCMFPwrActSts', 'LoadPwrActStsSCMRPwrActSts', 'LoadPwrActStsSODLPwrActSts', 'LoadPwrActStsSODRPwrActSts', 'LoadPwrActStsSRSPwrActSts', 'LoadPwrActStsSWTLPwrActSts', 'LoadPwrActStsSWTRPwrActSts', 'LoadPwrActStsTERVPwrActSts', 'LoadPwrActStsUSBR1PwrActSts', 'LoadPwrActStsUSBR2PwrActSts', 'LoadPwrActStsUWBPwrActSts', 'LoadPwrActStsVCUPwrActSts', 'LoadPwrActStsWERVPwrActSts', 'LoadPwrActStsWPCPwrActSts'], 'VehDateAndTi': ['VehDateAndTiDay', 'VehDateAndTiHr', 'VehDateAndTiMins', 'VehDateAndTiMth', 'VehDateAndTiSec', 'VehDateAndTiValid', 'VehDateAndTiYr'], 'Vin': ['VinInfoBytePosn1', 'VinInfoBytePosn10', 'VinInfoBytePosn11', 'VinInfoBytePosn12', 'VinInfoBytePosn13', 'VinInfoBytePosn14', 'VinInfoBytePosn15', 'VinInfoBytePosn16', 'VinInfoBytePosn17', 'VinInfoBytePosn2', 'VinInfoBytePosn3', 'VinInfoBytePosn4', 'VinInfoBytePosn5', 'VinInfoBytePosn6', 'VinInfoBytePosn7', 'VinInfoBytePosn8', 'VinInfoBytePosn9']}
    sig_group_dataid_dict = {}

    class LoadPwrActStsHBMFPwrActSts:
        sig_name = "LoadPwrActStsHBMFPwrActSts"
        sig_start_bit = 65
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 65
        byte = 8
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class LoadPwrActStsReserved7:
        sig_name = "LoadPwrActStsReserved7"
        sig_start_bit = 157
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 157
        byte = 19
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class LoadPwrActStsSODRPwrActSts:
        sig_name = "LoadPwrActStsSODRPwrActSts"
        sig_start_bit = 177
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 177
        byte = 22
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class LoadPwrActStsECTVPwrActSts:
        sig_name = "LoadPwrActStsECTVPwrActSts"
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
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 51
        byte = 6
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class LoadPwrActStsCSOVPwrActSts:
        sig_name = "LoadPwrActStsCSOVPwrActSts"
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
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 37
        byte = 4
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class LoadPwrActStsRMLPwrActSts:
        sig_name = "LoadPwrActStsRMLPwrActSts"
        sig_start_bit = 161
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 161
        byte = 20
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class LoadPwrActStsSCMRPwrActSts:
        sig_name = "LoadPwrActStsSCMRPwrActSts"
        sig_start_bit = 181
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 181
        byte = 22
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class LoadPwrActStsWPCPwrActSts:
        sig_name = "LoadPwrActStsWPCPwrActSts"
        sig_start_bit = 201
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 201
        byte = 25
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class LoadPwrActStsCRCMPwrActSts:
        sig_name = "LoadPwrActStsCRCMPwrActSts"
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
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 39
        byte = 4
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class LoadPwrActStsWERVPwrActSts:
        sig_name = "LoadPwrActStsWERVPwrActSts"
        sig_start_bit = 203
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 203
        byte = 25
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class LoadPwrActStsFEXVPwrActSts:
        sig_name = "LoadPwrActStsFEXVPwrActSts"
        sig_start_bit = 57
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 57
        byte = 7
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class LoadPwrActStsHCMRPwrActSts:
        sig_name = "LoadPwrActStsHCMRPwrActSts"
        sig_start_bit = 73
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 73
        byte = 9
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class LoadPwrActStsSODLPwrActSts:
        sig_name = "LoadPwrActStsSODLPwrActSts"
        sig_start_bit = 179
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 179
        byte = 22
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class LoadPwrActStsSRSPwrActSts:
        sig_name = "LoadPwrActStsSRSPwrActSts"
        sig_start_bit = 191
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 191
        byte = 23
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class LoadPwrActStsREXVPwrActSts:
        sig_name = "LoadPwrActStsREXVPwrActSts"
        sig_start_bit = 167
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 167
        byte = 20
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class LoadPwrActStsDMFLPwrActSts:
        sig_name = "LoadPwrActStsDMFLPwrActSts"
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
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 47
        byte = 5
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class LoadPwrActStsReserved4:
        sig_name = "LoadPwrActStsReserved4"
        sig_start_bit = 147
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 147
        byte = 18
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VinInfoBytePosn15:
        sig_name = "VinInfoBytePosn15"
        sig_start_bit = 343
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
        startbit = 343
        byte = 42
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class LoadPwrActStsEGSMPwrActSts:
        sig_name = "LoadPwrActStsEGSMPwrActSts"
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
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 63
        byte = 7
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class LoadPwrActStsMMPPwrActSts:
        sig_name = "LoadPwrActStsMMPPwrActSts"
        sig_start_bit = 109
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 109
        byte = 13
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class LoadPwrActStsBNCMPwrActSts:
        sig_name = "LoadPwrActStsBNCMPwrActSts"
        sig_start_bit = 17
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 17
        byte = 2
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class LoadPwrActStsReserved11:
        sig_name = "LoadPwrActStsReserved11"
        sig_start_bit = 131
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 131
        byte = 16
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VinInfoBytePosn5:
        sig_name = "VinInfoBytePosn5"
        sig_start_bit = 263
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
        startbit = 263
        byte = 32
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class LoadPwrActStsHODPwrActSts:
        sig_name = "LoadPwrActStsHODPwrActSts"
        sig_start_bit = 85
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 85
        byte = 10
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class LoadPwrActStsFLRPwrActSts:
        sig_name = "LoadPwrActStsFLRPwrActSts"
        sig_start_bit = 71
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 71
        byte = 8
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class LoadPwrActStsLPODPwrActSts:
        sig_name = "LoadPwrActStsLPODPwrActSts"
        sig_start_bit = 99
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 99
        byte = 12
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class LoadPwrActStsFSRRPwrActSts:
        sig_name = "LoadPwrActStsFSRRPwrActSts"
        sig_start_bit = 67
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 67
        byte = 8
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class LoadPwrActStsAGUPwrActSts:
        sig_name = "LoadPwrActStsAGUPwrActSts"
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
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VirtGearShiftModeReq_UB:
        sig_name = "VirtGearShiftModeReq_UB"
        sig_start_bit = 420
        update_id_bit = 420
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
        startbit = 420
        byte = 52
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class LoadPwrActStsRCMLPwrActSts:
        sig_name = "LoadPwrActStsRCMLPwrActSts"
        sig_start_bit = 123
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 123
        byte = 15
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class LoadPwrActStsIRMMPwrActSts:
        sig_name = "LoadPwrActStsIRMMPwrActSts"
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
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 103
        byte = 12
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class VinInfoBytePosn10:
        sig_name = "VinInfoBytePosn10"
        sig_start_bit = 303
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
        startbit = 303
        byte = 37
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class LoadPwrActStsReserved9:
        sig_name = "LoadPwrActStsReserved9"
        sig_start_bit = 153
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 153
        byte = 19
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class LoadPwrActSts_UB:
        sig_name = "LoadPwrActSts_UB"
        sig_start_bit = 215
        update_id_bit = 215
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
        startbit = 215
        byte = 26
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class LoadPwrActStsRLMMPwrActSts:
        sig_name = "LoadPwrActStsRLMMPwrActSts"
        sig_start_bit = 165
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 165
        byte = 20
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class VinInfoBytePosn9:
        sig_name = "VinInfoBytePosn9"
        sig_start_bit = 295
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
        startbit = 295
        byte = 36
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class LoadPwrActStsRLSMPwrActSts:
        sig_name = "LoadPwrActStsRLSMPwrActSts"
        sig_start_bit = 163
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 163
        byte = 20
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class LoadPwrActStsHCTVPwrActSts:
        sig_name = "LoadPwrActStsHCTVPwrActSts"
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
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 87
        byte = 10
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class LoadPwrActStsFSRLPwrActSts:
        sig_name = "LoadPwrActStsFSRLPwrActSts"
        sig_start_bit = 69
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 69
        byte = 8
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class LoadPwrActStsReserved17:
        sig_name = "LoadPwrActStsReserved17"
        sig_start_bit = 199
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 199
        byte = 24
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class VinInfoBytePosn13:
        sig_name = "VinInfoBytePosn13"
        sig_start_bit = 327
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
        startbit = 327
        byte = 40
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class LoadPwrActStsReserved13:
        sig_name = "LoadPwrActStsReserved13"
        sig_start_bit = 143
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 143
        byte = 17
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class LoadPwrActStsDRFPwrActSts:
        sig_name = "LoadPwrActStsDRFPwrActSts"
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
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 43
        byte = 5
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class LoadPwrActStsBCTVPwrActSts:
        sig_name = "LoadPwrActStsBCTVPwrActSts"
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
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 21
        byte = 2
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class LoadPwrActStsEPMPwrActSts:
        sig_name = "LoadPwrActStsEPMPwrActSts"
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
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 61
        byte = 7
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class LoadPwrActStsCERVPwrActSts:
        sig_name = "LoadPwrActStsCERVPwrActSts"
        sig_start_bit = 25
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 25
        byte = 3
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class LoadPwrActStsUSBR1PwrActSts:
        sig_name = "LoadPwrActStsUSBR1PwrActSts"
        sig_start_bit = 195
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 195
        byte = 24
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class LoadPwrActStsMMDPwrActSts:
        sig_name = "LoadPwrActStsMMDPwrActSts"
        sig_start_bit = 111
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 111
        byte = 13
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class LoadPwrActStsNKRPwrActSts:
        sig_name = "LoadPwrActStsNKRPwrActSts"
        sig_start_bit = 107
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 107
        byte = 13
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class LoadPwrActStsReserved18:
        sig_name = "LoadPwrActStsReserved18"
        sig_start_bit = 197
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 197
        byte = 24
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class LoadPwrActStsBEXVPwrActSts:
        sig_name = "LoadPwrActStsBEXVPwrActSts"
        sig_start_bit = 19
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 19
        byte = 2
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class LoadPwrActStsCDPwrActSts:
        sig_name = "LoadPwrActStsCDPwrActSts"
        sig_start_bit = 27
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 27
        byte = 3
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class LoadPwrActStsCCTVPwrActSts:
        sig_name = "LoadPwrActStsCCTVPwrActSts"
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
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 29
        byte = 3
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class LoadPwrActStsReserved2:
        sig_name = "LoadPwrActStsReserved2"
        sig_start_bit = 151
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 151
        byte = 18
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class LoadPwrActStsReserved1:
        sig_name = "LoadPwrActStsReserved1"
        sig_start_bit = 135
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 135
        byte = 16
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class LoadPwrActStsPOFPwrActSts:
        sig_name = "LoadPwrActStsPOFPwrActSts"
        sig_start_bit = 113
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 113
        byte = 14
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VirtGearShiftModeReqVirtShiftModeSts:
        sig_name = "VirtGearShiftModeReqVirtShiftModeSts"
        sig_start_bit = 423
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
        startbit = 423
        byte = 52
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class LoadPwrActStsReserved6:
        sig_name = "LoadPwrActStsReserved6"
        sig_start_bit = 159
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 159
        byte = 19
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class LoadPwrActStsHVCMPwrActSts:
        sig_name = "LoadPwrActStsHVCMPwrActSts"
        sig_start_bit = 91
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 91
        byte = 11
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VinInfoBytePosn8:
        sig_name = "VinInfoBytePosn8"
        sig_start_bit = 287
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
        startbit = 287
        byte = 35
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VirtGearShiftModeReqChks:
        sig_name = "VirtGearShiftModeReqChks"
        sig_start_bit = 415
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 415
        byte = 51
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VinInfoBytePosn6:
        sig_name = "VinInfoBytePosn6"
        sig_start_bit = 271
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
        startbit = 271
        byte = 33
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class LoadPwrActStsPMSIPwrActSts:
        sig_name = "LoadPwrActStsPMSIPwrActSts"
        sig_start_bit = 115
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 115
        byte = 14
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class LoadPwrActStsDPODPwrActSts:
        sig_name = "LoadPwrActStsDPODPwrActSts"
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
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 45
        byte = 5
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class LoadPwrActStsBCFVPwrActSts:
        sig_name = "LoadPwrActStsBCFVPwrActSts"
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
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 23
        byte = 2
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class LoadPwrActStsOPCRPwrActSts:
        sig_name = "LoadPwrActStsOPCRPwrActSts"
        sig_start_bit = 117
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 117
        byte = 14
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class LoadPwrActStsRPODPwrActSts:
        sig_name = "LoadPwrActStsRPODPwrActSts"
        sig_start_bit = 175
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 175
        byte = 21
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class LoadPwrActStsHUBRPwrActSts:
        sig_name = "LoadPwrActStsHUBRPwrActSts"
        sig_start_bit = 81
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 81
        byte = 10
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class LoadPwrActStsDRMRRPwrActSts:
        sig_name = "LoadPwrActStsDRMRRPwrActSts"
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
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 53
        byte = 6
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class LoadPwrActStsSCMFPwrActSts:
        sig_name = "LoadPwrActStsSCMFPwrActSts"
        sig_start_bit = 183
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 183
        byte = 22
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class VehDateAndTiHr:
        sig_name = "VehDateAndTiHr"
        sig_start_bit = 370
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
        startbit = 370
        bmuws_info = [(46, 0b00000111, 0b11111000, 3, 0), (47, 0b11000000, 0b00111111, 2, 6)]

    class VehDateAndTi_UB:
        sig_name = "VehDateAndTi_UB"
        sig_start_bit = 404
        update_id_bit = 404
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
        startbit = 404
        byte = 50
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class LoadPwrActStsFCSIPwrActSts:
        sig_name = "LoadPwrActStsFCSIPwrActSts"
        sig_start_bit = 59
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 59
        byte = 7
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class LoadPwrActStsHVCHPwrActSts:
        sig_name = "LoadPwrActStsHVCHPwrActSts"
        sig_start_bit = 93
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 93
        byte = 11
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class LoadPwrActStsBCCPPwrActSts:
        sig_name = "LoadPwrActStsBCCPPwrActSts"
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
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 9
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VehDateAndTiMins:
        sig_name = "VehDateAndTiMins"
        sig_start_bit = 381
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
        startbit = 381
        byte = 47
        mask = 0b00111111
        unmask = 0b11000000
        shift = 0

    class LoadPwrActStsBoosterBlowerPwrActSts:
        sig_name = "LoadPwrActStsBoosterBlowerPwrActSts"
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
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 31
        byte = 3
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class VehDateAndTiValid:
        sig_name = "VehDateAndTiValid"
        sig_start_bit = 397
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
        startbit = 397
        byte = 49
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class LoadPwrActStsHVAHPwrActSts:
        sig_name = "LoadPwrActStsHVAHPwrActSts"
        sig_start_bit = 95
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 95
        byte = 11
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class LoadPwrActStsTERVPwrActSts:
        sig_name = "LoadPwrActStsTERVPwrActSts"
        sig_start_bit = 185
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 185
        byte = 23
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class LoadPwrActStsDICPwrActSts:
        sig_name = "LoadPwrActStsDICPwrActSts"
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
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 33
        byte = 4
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VinInfoBytePosn7:
        sig_name = "VinInfoBytePosn7"
        sig_start_bit = 279
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
        startbit = 279
        byte = 34
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class LoadPwrActStsRRMMPwrActSts:
        sig_name = "LoadPwrActStsRRMMPwrActSts"
        sig_start_bit = 173
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 173
        byte = 21
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class LoadPwrActStsReserved8:
        sig_name = "LoadPwrActStsReserved8"
        sig_start_bit = 155
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 155
        byte = 19
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class LoadPwrActStsReserved3:
        sig_name = "LoadPwrActStsReserved3"
        sig_start_bit = 149
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 149
        byte = 18
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class VinInfoBytePosn11:
        sig_name = "VinInfoBytePosn11"
        sig_start_bit = 311
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
        startbit = 311
        byte = 38
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VinInfoBytePosn2:
        sig_name = "VinInfoBytePosn2"
        sig_start_bit = 239
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
        startbit = 239
        byte = 29
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehDateAndTiMth:
        sig_name = "VehDateAndTiMth"
        sig_start_bit = 391
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 3
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 391
        byte = 48
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class LoadPwrActStsOPCFPwrActSts:
        sig_name = "LoadPwrActStsOPCFPwrActSts"
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
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 119
        byte = 14
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class LoadPwrActStsHCCPPwrActSts:
        sig_name = "LoadPwrActStsHCCPPwrActSts"
        sig_start_bit = 77
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 77
        byte = 9
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class LoadPwrActStsReserved10:
        sig_name = "LoadPwrActStsReserved10"
        sig_start_bit = 133
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 133
        byte = 16
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class LoadPwrActStsReserved16:
        sig_name = "LoadPwrActStsReserved16"
        sig_start_bit = 137
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 137
        byte = 17
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class LoadPwrActStsACCMPwrActSts:
        sig_name = "LoadPwrActStsACCMPwrActSts"
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
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class LoadPwrActStsPPODPwrActSts:
        sig_name = "LoadPwrActStsPPODPwrActSts"
        sig_start_bit = 125
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 125
        byte = 15
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class VinInfoBytePosn14:
        sig_name = "VinInfoBytePosn14"
        sig_start_bit = 335
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
        startbit = 335
        byte = 41
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class LoadPwrActStsAGMPwrActSts:
        sig_name = "LoadPwrActStsAGMPwrActSts"
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
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 3
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VinInfoBytePosn12:
        sig_name = "VinInfoBytePosn12"
        sig_start_bit = 319
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
        startbit = 319
        byte = 39
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class LoadPwrActStsVCUPwrActSts:
        sig_name = "LoadPwrActStsVCUPwrActSts"
        sig_start_bit = 205
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 205
        byte = 25
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class LoadPwrActStsHBMRPwrActSts:
        sig_name = "LoadPwrActStsHBMRPwrActSts"
        sig_start_bit = 79
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 79
        byte = 9
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class LoadPwrActStsReserved5:
        sig_name = "LoadPwrActStsReserved5"
        sig_start_bit = 145
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 145
        byte = 18
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VinInfoBytePosn1:
        sig_name = "VinInfoBytePosn1"
        sig_start_bit = 231
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
        startbit = 231
        byte = 28
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class LoadPwrActStsLCTVPwrActSts:
        sig_name = "LoadPwrActStsLCTVPwrActSts"
        sig_start_bit = 101
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 101
        byte = 12
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class LoadPwrActStsPORPwrActSts:
        sig_name = "LoadPwrActStsPORPwrActSts"
        sig_start_bit = 127
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 127
        byte = 15
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class LoadPwrActStsOHCPwrActSts:
        sig_name = "LoadPwrActStsOHCPwrActSts"
        sig_start_bit = 105
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 105
        byte = 13
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class LoadPwrActStsALMRPwrActSts:
        sig_name = "LoadPwrActStsALMRPwrActSts"
        sig_start_bit = 13
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 13
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class LoadPwrActStsDRMFRPwrActSts:
        sig_name = "LoadPwrActStsDRMFRPwrActSts"
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
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 41
        byte = 5
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VinInfoBytePosn16:
        sig_name = "VinInfoBytePosn16"
        sig_start_bit = 351
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
        startbit = 351
        byte = 43
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehDateAndTiYr:
        sig_name = "VehDateAndTiYr"
        sig_start_bit = 396
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 21
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 396
        bmuws_info = [(49, 0b00011111, 0b11100000, 5, 0), (50, 0b11100000, 0b00011111, 3, 5)]

    class LoadPwrActStsRCMRPwrActSts:
        sig_name = "LoadPwrActStsRCMRPwrActSts"
        sig_start_bit = 121
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 121
        byte = 15
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VehDateAndTiSec:
        sig_name = "VehDateAndTiSec"
        sig_start_bit = 387
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
        startbit = 387
        bmuws_info = [(48, 0b00001111, 0b11110000, 4, 0), (49, 0b11000000, 0b00111111, 2, 6)]

    class VirtGearShiftModeReqCntr:
        sig_name = "VirtGearShiftModeReqCntr"
        sig_start_bit = 419
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
        startbit = 419
        byte = 52
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class LoadPwrActStsSWTLPwrActSts:
        sig_name = "LoadPwrActStsSWTLPwrActSts"
        sig_start_bit = 189
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 189
        byte = 23
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class LoadPwrActStsDRMRLPwrActSts:
        sig_name = "LoadPwrActStsDRMRLPwrActSts"
        sig_start_bit = 55
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 55
        byte = 6
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class LoadPwrActStsEDCPPwrActSts:
        sig_name = "LoadPwrActStsEDCPPwrActSts"
        sig_start_bit = 49
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 49
        byte = 6
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class LoadPwrActStsHCMLPwrActSts:
        sig_name = "LoadPwrActStsHCMLPwrActSts"
        sig_start_bit = 75
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 75
        byte = 9
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class LoadPwrActStsRSOV1PwrActSts:
        sig_name = "LoadPwrActStsRSOV1PwrActSts"
        sig_start_bit = 171
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 171
        byte = 21
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class LoadPwrActStsUSBR2PwrActSts:
        sig_name = "LoadPwrActStsUSBR2PwrActSts"
        sig_start_bit = 193
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 193
        byte = 24
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class LoadPwrActStsIEMPwrActSts:
        sig_name = "LoadPwrActStsIEMPwrActSts"
        sig_start_bit = 89
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 89
        byte = 11
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class LoadPwrActStsUWBPwrActSts:
        sig_name = "LoadPwrActStsUWBPwrActSts"
        sig_start_bit = 207
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 207
        byte = 25
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class LoadPwrActStsReserved12:
        sig_name = "LoadPwrActStsReserved12"
        sig_start_bit = 129
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 129
        byte = 16
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class LoadPwrActStsRSOV2PwrActSts:
        sig_name = "LoadPwrActStsRSOV2PwrActSts"
        sig_start_bit = 169
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 169
        byte = 21
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class LoadPwrActStsHUBFPwrActSts:
        sig_name = "LoadPwrActStsHUBFPwrActSts"
        sig_start_bit = 83
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 83
        byte = 10
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class LoadPwrActStsMGMPwrActSts:
        sig_name = "LoadPwrActStsMGMPwrActSts"
        sig_start_bit = 97
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 97
        byte = 12
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VehDateAndTiDay:
        sig_name = "VehDateAndTiDay"
        sig_start_bit = 375
        update_id_bit = None
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 2
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 375
        byte = 46
        mask = 0b11111000
        unmask = 0b00000111
        shift = 3

    class LoadPwrActStsAFUPwrActSts:
        sig_name = "LoadPwrActStsAFUPwrActSts"
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
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class LoadPwrActStsReserved14:
        sig_name = "LoadPwrActStsReserved14"
        sig_start_bit = 141
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 141
        byte = 17
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class VinInfoBytePosn17:
        sig_name = "VinInfoBytePosn17"
        sig_start_bit = 359
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
        startbit = 359
        byte = 44
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class LoadPwrActStsReserved15:
        sig_name = "LoadPwrActStsReserved15"
        sig_start_bit = 139
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 139
        byte = 17
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class LoadPwrActStsALMLPwrActSts:
        sig_name = "LoadPwrActStsALMLPwrActSts"
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
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 15
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class VinInfoBytePosn4:
        sig_name = "VinInfoBytePosn4"
        sig_start_bit = 255
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
        startbit = 255
        byte = 31
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VinInfoBytePosn3:
        sig_name = "VinInfoBytePosn3"
        sig_start_bit = 247
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
        startbit = 247
        byte = 30
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class LoadPwrActStsDCTVPwrActSts:
        sig_name = "LoadPwrActStsDCTVPwrActSts"
        sig_start_bit = 35
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 35
        byte = 4
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class LoadPwrActStsAWMPwrActSts:
        sig_name = "LoadPwrActStsAWMPwrActSts"
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
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 11
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class LoadPwrActStsSWTRPwrActSts:
        sig_name = "LoadPwrActStsSWTRPwrActSts"
        sig_start_bit = 187
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 187
        byte = 23
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2


class BCU2PropulsionCANFDNmFr:
    msg_name = "BCU2PropulsionCANFDNmFr"
    msg_id = 1284
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BCU2"
    rx_nodes = ['BCU1']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class CCUMCUCDToEGSMPropulsionCANFDDiagReqFrame:
    msg_name = "CCUMCUCDToEGSMPropulsionCANFDDiagReqFrame"
    msg_id = 1843
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "CCUMCUCD"
    rx_nodes = ['EGSM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class BECMPropulsionCANFDFr07:
    msg_name = "BECMPropulsionCANFDFr07"
    msg_id = 917
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.5
    msg_length = 8
    tx_node = "BECM"
    rx_nodes = ['CCUMCUCD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HVBattCellBalFlg:
        sig_name = "HVBattCellBalFlg"
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
        sig_value_table = {'OnOffCrit1_NotVld1': 0, 'OnOffCrit1_Off': 1, 'OnOffCrit1_On': 2, 'OnOffCrit1_NotVld2': 3}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class VCUPropulsionCANFDFr06:
    msg_name = "VCUPropulsionCANFDFr06"
    msg_id = 337
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.04
    msg_length = 8
    tx_node = "VCU"
    rx_nodes = ['BCU1']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class BrkRegenLiReq:
        sig_name = "BrkRegenLiReq"
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
        sig_value_table = {'ReqSts2_Default': 0, 'ReqSts2_NotReqd': 1, 'ReqSts2_Reqd': 2, 'ReqSts2_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class ODPToCCUMCUCDPropulsionCANFDDiagRespFrame:
    msg_name = "ODPToCCUMCUCDPropulsionCANFDDiagRespFrame"
    msg_id = 1616
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "ODP"
    rx_nodes = ['CCUMCUCD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class CCUMCUCDPropulsionCANFDFr05:
    msg_name = "CCUMCUCDPropulsionCANFDFr05"
    msg_id = 512
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.06
    msg_length = 8
    tx_node = "CCUMCUCD"
    rx_nodes = ['VCU', 'BCU1']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class DrvModReq:
        sig_name = "DrvModReq"
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
        sig_value_table = {'DrvModReqType_Undefd': 0, 'DrvModReqType_ECO': 1, 'DrvModReqType_Comfort_Normal': 2, 'DrvModReqType_Dynamic_Sport': 3, 'DrvModReqType_Tank': 4, 'DrvModReqType_Offroad_CrossTerrain': 5, 'DrvModReqType_Adaptive': 6, 'DrvModReqType_Race': 7, 'DrvModReqType_Reserved': 8, 'DrvModReqType_ECO_PLUS': 9, 'DrvModReqType_Power': 10, 'DrvModReqType_Snow': 11, 'DrvModReqType_Sand': 12, 'DrvModReqType_Mud': 13, 'DrvModReqType_Rock': 14, 'DrvModReqType_Err': 15}
        compute_method = None
        length = 4
        startbit = 7
        byte = 0
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4


class EGSMPropulsionCANFDFr01:
    msg_name = "EGSMPropulsionCANFDFr01"
    msg_id = 132
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 64
    tx_node = "EGSM"
    rx_nodes = ['VCU', 'ETC', 'CCUMCUCD', 'BCU2', 'CCUMCUAD', 'BCU1']
    sig_group_dict = {'ElecGearShiftDevelpSignalGroup2': ['ElecGearShiftDevelpSignalGroup2DevelpSignalGroup1', 'ElecGearShiftDevelpSignalGroup2DevelpSignalGroup2', 'ElecGearShiftDevelpSignalGroup2DevelpSignalGroup3', 'ElecGearShiftDevelpSignalGroup2DevelpSignalGroup4', 'ElecGearShiftDevelpSignalGroup2DevelpSignalGroup5', 'ElecGearShiftDevelpSignalGroup2DevelpSignalGroup6', 'ElecGearShiftDevelpSignalGroup2DevelpSignalGroup7', 'ElecGearShiftDevelpSignalGroup2DevelpSignalGroup8'], 'ElecGearShiftDevelpSignalGroup1': ['ElecGearShiftDevelpSignalGroup1DevelpSignalGroup1', 'ElecGearShiftDevelpSignalGroup1DevelpSignalGroup2', 'ElecGearShiftDevelpSignalGroup1DevelpSignalGroup3', 'ElecGearShiftDevelpSignalGroup1DevelpSignalGroup4', 'ElecGearShiftDevelpSignalGroup1DevelpSignalGroup5', 'ElecGearShiftDevelpSignalGroup1DevelpSignalGroup6', 'ElecGearShiftDevelpSignalGroup1DevelpSignalGroup7', 'ElecGearShiftDevelpSignalGroup1DevelpSignalGroup8'], 'ElecGearShiftReq2': ['ElecGearShiftReq2Chks', 'ElecGearShiftReq2Cntr', 'ElecGearShiftReq2GearFltSts', 'ElecGearShiftReq2GearReq'], 'ElecGearShiftReq1': ['ElecGearShiftReq1Chks', 'ElecGearShiftReq1Cntr', 'ElecGearShiftReq1GearFltSts', 'ElecGearShiftReq1GearReq']}
    sig_group_dataid_dict = {'ElecGearShiftReq2': 1008, 'ElecGearShiftReq1': 1007}

    class ElecGearShiftDevelpSignalGroup1DevelpSignalGroup4:
        sig_name = "ElecGearShiftDevelpSignalGroup1DevelpSignalGroup4"
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

    class ElecGearShiftDevelpSignalGroup2_UB:
        sig_name = "ElecGearShiftDevelpSignalGroup2_UB"
        sig_start_bit = 134
        update_id_bit = 134
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
        startbit = 134
        byte = 16
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class ElecGearShiftDevelpSignalGroup2DevelpSignalGroup8:
        sig_name = "ElecGearShiftDevelpSignalGroup2DevelpSignalGroup8"
        sig_start_bit = 127
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 127
        byte = 15
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ElecGearShiftDevelpSignalGroup1_UB:
        sig_name = "ElecGearShiftDevelpSignalGroup1_UB"
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

    class ElecGearShiftReq1GearReq:
        sig_name = "ElecGearShiftReq1GearReq"
        sig_start_bit = 175
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GearLvrIndcn_Default': 0, 'GearLvrIndcn_P': 1, 'GearLvrIndcn_R': 2, 'GearLvrIndcn_N': 3, 'GearLvrIndcn_D': 4, 'GearLvrIndcn_Reserved1': 5, 'GearLvrIndcn_Reserved2': 6, 'GearLvrIndcn_Undefd': 7}
        compute_method = None
        length = 3
        startbit = 175
        byte = 21
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class ElecGearShiftSts:
        sig_name = "ElecGearShiftSts"
        sig_start_bit = 150
        update_id_bit = 147
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GearFltSts_Normal': 0, 'GearFltSts_PFlt': 1, 'GearFltSts_RFlt': 2, 'GearFltSts_NFlt': 3, 'GearFltSts_DFlt': 4, 'GearFltSts_SrvReq': 5, 'GearFltSts_Reserved1': 6, 'GearFltSts_Reserved2': 7}
        compute_method = None
        length = 3
        startbit = 150
        byte = 18
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class ElecGearShiftReq2_UB:
        sig_name = "ElecGearShiftReq2_UB"
        sig_start_bit = 188
        update_id_bit = 188
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
        startbit = 188
        byte = 23
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class ElecGearShiftDevelpSignalGroup2DevelpSignalGroup6:
        sig_name = "ElecGearShiftDevelpSignalGroup2DevelpSignalGroup6"
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

    class ElecGearShiftReq1Cntr:
        sig_name = "ElecGearShiftReq1Cntr"
        sig_start_bit = 163
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
        startbit = 163
        byte = 20
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class ElecGearShiftLiSts:
        sig_name = "ElecGearShiftLiSts"
        sig_start_bit = 143
        update_id_bit = 139
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LightSts_Off': 0, 'LightSts_On': 1, 'LightSts_Error': 2, 'LightSts_Reserved': 3}
        compute_method = None
        length = 4
        startbit = 143
        byte = 17
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class ElecGearShiftDevelpSignalGroup2DevelpSignalGroup5:
        sig_name = "ElecGearShiftDevelpSignalGroup2DevelpSignalGroup5"
        sig_start_bit = 103
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
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

    class ElecGearShiftDevelpSignalGroup2DevelpSignalGroup2:
        sig_name = "ElecGearShiftDevelpSignalGroup2DevelpSignalGroup2"
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

    class ElecGearShiftReq2GearFltSts:
        sig_name = "ElecGearShiftReq2GearFltSts"
        sig_start_bit = 191
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GearFltSts_Normal': 0, 'GearFltSts_PFlt': 1, 'GearFltSts_RFlt': 2, 'GearFltSts_NFlt': 3, 'GearFltSts_DFlt': 4, 'GearFltSts_SrvReq': 5, 'GearFltSts_Reserved1': 6, 'GearFltSts_Reserved2': 7}
        compute_method = None
        length = 3
        startbit = 191
        byte = 23
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class ElecGearShiftReq1_UB:
        sig_name = "ElecGearShiftReq1_UB"
        sig_start_bit = 164
        update_id_bit = 164
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
        startbit = 164
        byte = 20
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class ElecGearShiftReq2GearReq:
        sig_name = "ElecGearShiftReq2GearReq"
        sig_start_bit = 199
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GearLvrIndcn_Default': 0, 'GearLvrIndcn_P': 1, 'GearLvrIndcn_R': 2, 'GearLvrIndcn_N': 3, 'GearLvrIndcn_D': 4, 'GearLvrIndcn_Reserved1': 5, 'GearLvrIndcn_Reserved2': 6, 'GearLvrIndcn_Undefd': 7}
        compute_method = None
        length = 3
        startbit = 199
        byte = 24
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class ElecGearShiftReq2Cntr:
        sig_name = "ElecGearShiftReq2Cntr"
        sig_start_bit = 187
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
        startbit = 187
        byte = 23
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class ElecGearShiftReqVirt:
        sig_name = "ElecGearShiftReqVirt"
        sig_start_bit = 138
        update_id_bit = 151
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GearLvrIndcn_Default': 0, 'GearLvrIndcn_P': 1, 'GearLvrIndcn_R': 2, 'GearLvrIndcn_N': 3, 'GearLvrIndcn_D': 4, 'GearLvrIndcn_Reserved1': 5, 'GearLvrIndcn_Reserved2': 6, 'GearLvrIndcn_Undefd': 7}
        compute_method = None
        length = 3
        startbit = 138
        byte = 17
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class ElecGearShiftDevelpSignalGroup2DevelpSignalGroup3:
        sig_name = "ElecGearShiftDevelpSignalGroup2DevelpSignalGroup3"
        sig_start_bit = 87
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 87
        byte = 10
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ElecGearShiftDevelpSignalGroup1DevelpSignalGroup2:
        sig_name = "ElecGearShiftDevelpSignalGroup1DevelpSignalGroup2"
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

    class ElecGearShiftReq2Chks:
        sig_name = "ElecGearShiftReq2Chks"
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

    class ElecGearShiftDevelpSignalGroup2DevelpSignalGroup4:
        sig_name = "ElecGearShiftDevelpSignalGroup2DevelpSignalGroup4"
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

    class ElecGearShiftDevelpSignalGroup2DevelpSignalGroup1:
        sig_name = "ElecGearShiftDevelpSignalGroup2DevelpSignalGroup1"
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

    class ElecGearShiftDevelpSignalGroup1DevelpSignalGroup5:
        sig_name = "ElecGearShiftDevelpSignalGroup1DevelpSignalGroup5"
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

    class ElecGearShiftReq1Chks:
        sig_name = "ElecGearShiftReq1Chks"
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

    class ElecGearShiftDevelpSignalGroup1DevelpSignalGroup3:
        sig_name = "ElecGearShiftDevelpSignalGroup1DevelpSignalGroup3"
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

    class ElecGearShiftDevelpSignalGroup1DevelpSignalGroup6:
        sig_name = "ElecGearShiftDevelpSignalGroup1DevelpSignalGroup6"
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

    class ElecGearShiftDevelpSignalGroup1DevelpSignalGroup1:
        sig_name = "ElecGearShiftDevelpSignalGroup1DevelpSignalGroup1"
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

    class ElecGearShiftDevelpSignalGroup1DevelpSignalGroup8:
        sig_name = "ElecGearShiftDevelpSignalGroup1DevelpSignalGroup8"
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

    class ElecGearShiftDevelpSignalGroup2DevelpSignalGroup7:
        sig_name = "ElecGearShiftDevelpSignalGroup2DevelpSignalGroup7"
        sig_start_bit = 119
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 119
        byte = 14
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ElecGearShiftReq1GearFltSts:
        sig_name = "ElecGearShiftReq1GearFltSts"
        sig_start_bit = 167
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GearFltSts_Normal': 0, 'GearFltSts_PFlt': 1, 'GearFltSts_RFlt': 2, 'GearFltSts_NFlt': 3, 'GearFltSts_DFlt': 4, 'GearFltSts_SrvReq': 5, 'GearFltSts_Reserved1': 6, 'GearFltSts_Reserved2': 7}
        compute_method = None
        length = 3
        startbit = 167
        byte = 20
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class ElecGearShiftDevelpSignalGroup1DevelpSignalGroup7:
        sig_name = "ElecGearShiftDevelpSignalGroup1DevelpSignalGroup7"
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


class CCUMCUCDToAllOBDPropulsionCANFDDiagFuncReqFrame:
    msg_name = "CCUMCUCDToAllOBDPropulsionCANFDDiagFuncReqFrame"
    msg_id = 2015
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CCUMCUCD"
    rx_nodes = ['SRS', 'VCU']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class BCU1PropulsionCANFDFr03:
    msg_name = "BCU1PropulsionCANFDFr03"
    msg_id = 336
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.04
    msg_length = 64
    tx_node = "BCU1"
    rx_nodes = ['VCU', 'CCUMCUCD', 'ETC', 'CCUMCUAD']
    sig_group_dict = {'HdcSts': ['HdcStsActv', 'HdcStsChks', 'HdcStsCntr', 'HdcStsEna', 'HdcStsSts2'], 'AbsFctSts': ['AbsFctStsActv', 'AbsFctStsChks', 'AbsFctStsCntr', 'AbsFctStsEna', 'AbsFctStsSts2'], 'BrkTqFricAct': ['BrkTqFricActFL', 'BrkTqFricActFR', 'BrkTqFricActRL', 'BrkTqFricActRR'], 'CstSts': ['CstStsActv', 'CstStsChks', 'CstStsCntr', 'CstStsEna', 'CstStsSts2'], 'CrbSts': ['CrbStsActv', 'CrbStsChks', 'CrbStsCntr', 'CrbStsEna', 'CrbStsSts2'], 'DsrSts': ['DsrStsActv', 'DsrStsChks', 'DsrStsCntr', 'DsrStsEna', 'DsrStsSts2'], 'CdpSts': ['CdpStsActv', 'CdpStsChks', 'CdpStsCntr', 'CdpStsEna', 'CdpStsSts2'], 'SsmStsByBrk': ['SsmStsByBrkChks', 'SsmStsByBrkCntr', 'SsmStsByBrkStandstilMgrSts'], 'BrkSysWarnReq': ['BrkSysWarnReqBrkSysWarn', 'BrkSysWarnReqChks', 'BrkSysWarnReqCntr'], 'AvhSts': ['AvhStsActv', 'AvhStsChks', 'AvhStsCntr', 'AvhStsEna', 'AvhStsSts2'], 'VdcSts': ['VdcStsActv', 'VdcStsChks', 'VdcStsCntr', 'VdcStsEna', 'VdcStsSts2']}
    sig_group_dataid_dict = {}

    class BrySysOvrheated:
        sig_name = "BrySysOvrheated"
        sig_start_bit = 53
        update_id_bit = 52
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
        startbit = 53
        byte = 6
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class BTCActvRe:
        sig_name = "BTCActvRe"
        sig_start_bit = 65
        update_id_bit = 48
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Actv_NoActv': 0, 'Actv_Actv': 1, 'Actv_Reserved1': 2, 'Actv_Reserved2': 3}
        compute_method = None
        length = 2
        startbit = 65
        byte = 8
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class CbcActv:
        sig_name = "CbcActv"
        sig_start_bit = 164
        update_id_bit = 162
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ActvInActv2_Init': 0, 'ActvInActv2_InActv': 1, 'ActvInActv2_Actv': 2}
        compute_method = None
        length = 2
        startbit = 164
        byte = 20
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class VdcStsActv:
        sig_name = "VdcStsActv"
        sig_start_bit = 287
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Actv_NoActv': 0, 'Actv_Actv': 1, 'Actv_Reserved1': 2, 'Actv_Reserved2': 3}
        compute_method = None
        length = 2
        startbit = 287
        byte = 35
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class CdpStsActv:
        sig_name = "CdpStsActv"
        sig_start_bit = 167
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Actv_NoActv': 0, 'Actv_Actv': 1, 'Actv_Reserved1': 2, 'Actv_Reserved2': 3}
        compute_method = None
        length = 2
        startbit = 167
        byte = 20
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class CstStsSts2:
        sig_name = "CstStsSts2"
        sig_start_bit = 203
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Sts2_Initial': 0, 'Sts2_Normal': 1, 'Sts2_Fault': 2, 'Sts2_Off': 3}
        compute_method = None
        length = 3
        startbit = 203
        byte = 25
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class BTCActvFrnt:
        sig_name = "BTCActvFrnt"
        sig_start_bit = 51
        update_id_bit = 49
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Actv_NoActv': 0, 'Actv_Actv': 1, 'Actv_Reserved1': 2, 'Actv_Reserved2': 3}
        compute_method = None
        length = 2
        startbit = 51
        byte = 6
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class BrkSysWarnReqCntr:
        sig_name = "BrkSysWarnReqCntr"
        sig_start_bit = 71
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
        startbit = 71
        byte = 8
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class AvhStsActv:
        sig_name = "AvhStsActv"
        sig_start_bit = 55
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Actv_NoActv': 0, 'Actv_Actv': 1, 'Actv_Reserved1': 2, 'Actv_Reserved2': 3}
        compute_method = None
        length = 2
        startbit = 55
        byte = 6
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class AbsFctStsCntr:
        sig_name = "AbsFctStsCntr"
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

    class HdcSts_UB:
        sig_name = "HdcSts_UB"
        sig_start_bit = 261
        update_id_bit = 261
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
        startbit = 261
        byte = 32
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class HdcTarSpd:
        sig_name = "HdcTarSpd"
        sig_start_bit = 295
        update_id_bit = 256
        sig_length = 8
        sig_value_factor = 0.5
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 295
        byte = 36
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BrkSysWarnMsgReq:
        sig_name = "BrkSysWarnMsgReq"
        sig_start_bit = 31
        update_id_bit = 16
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BrkMsg_NoMsg': 0, 'BrkMsg_EbdFault': 1, 'BrkMsg_AbsFault': 2, 'BrkMsg_EscFault': 3, 'BrkMsg_EscOff': 4, 'BrkMsg_TcsOff': 5, 'BrkMsg_Reduced': 6, 'BrkMsg_Reserved': 7}
        compute_method = None
        length = 4
        startbit = 31
        byte = 3
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class HdcMsgReq:
        sig_name = "HdcMsgReq"
        sig_start_bit = 260
        update_id_bit = 257
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HdcMsg_NoReq': 0, 'HdcMsg_StandbyOn': 1, 'HdcMsg_ActiveOn': 2, 'HdcMsg_Fault': 3, 'HdcMsg_TempOff': 4, 'HdcMsg_Reserved': 5}
        compute_method = None
        length = 3
        startbit = 260
        byte = 32
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class CrbStsEna:
        sig_name = "CrbStsEna"
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
        sig_value_table = {'EnableDisable2_Disabled': 0, 'EnableDisable2_Enabled': 1}
        compute_method = None
        length = 1
        startbit = 176
        byte = 22
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class CstStsEna:
        sig_name = "CstStsEna"
        sig_start_bit = 200
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EnableDisable2_Disabled': 0, 'EnableDisable2_Enabled': 1}
        compute_method = None
        length = 1
        startbit = 200
        byte = 25
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class BrkSysWarnReqChks:
        sig_name = "BrkSysWarnReqChks"
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

    class AbsFctSts_UB:
        sig_name = "AbsFctSts_UB"
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

    class DsrStsEna:
        sig_name = "DsrStsEna"
        sig_start_bit = 224
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EnableDisable2_Disabled': 0, 'EnableDisable2_Enabled': 1}
        compute_method = None
        length = 1
        startbit = 224
        byte = 28
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class BrkTqFricActRL:
        sig_name = "BrkTqFricActRL"
        sig_start_bit = 115
        update_id_bit = None
        sig_length = 14
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 16000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 14
        startbit = 115
        bmuws_info = [(14, 0b00001111, 0b11110000, 4, 0), (15, 0b11111111, 0b00000000, 8, 0), (16, 0b11000000, 0b00111111, 2, 6)]

    class CrbStsCntr:
        sig_name = "CrbStsCntr"
        sig_start_bit = 183
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
        startbit = 183
        byte = 22
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class BrkTqFricAct_UB:
        sig_name = "BrkTqFricAct_UB"
        sig_start_bit = 80
        update_id_bit = 80
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
        startbit = 80
        byte = 10
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class CstSts_UB:
        sig_name = "CstSts_UB"
        sig_start_bit = 213
        update_id_bit = 213
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
        startbit = 213
        byte = 26
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class CrbSts_UB:
        sig_name = "CrbSts_UB"
        sig_start_bit = 189
        update_id_bit = 189
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
        startbit = 189
        byte = 23
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class CstStsCntr:
        sig_name = "CstStsCntr"
        sig_start_bit = 207
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
        startbit = 207
        byte = 25
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DTCActvFrnt:
        sig_name = "DTCActvFrnt"
        sig_start_bit = 188
        update_id_bit = 186
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Actv_NoActv': 0, 'Actv_Actv': 1, 'Actv_Reserved1': 2, 'Actv_Reserved2': 3}
        compute_method = None
        length = 2
        startbit = 188
        byte = 23
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class CstStsActv:
        sig_name = "CstStsActv"
        sig_start_bit = 215
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Actv_NoActv': 0, 'Actv_Actv': 1, 'Actv_Reserved1': 2, 'Actv_Reserved2': 3}
        compute_method = None
        length = 2
        startbit = 215
        byte = 26
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class AvhStsEna:
        sig_name = "AvhStsEna"
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
        sig_value_table = {'EnableDisable2_Disabled': 0, 'EnableDisable2_Enabled': 1}
        compute_method = None
        length = 1
        startbit = 40
        byte = 5
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class DsrSts_UB:
        sig_name = "DsrSts_UB"
        sig_start_bit = 237
        update_id_bit = 237
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
        startbit = 237
        byte = 29
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class CrbStsChks:
        sig_name = "CrbStsChks"
        sig_start_bit = 175
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
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

    class DsrStsActv:
        sig_name = "DsrStsActv"
        sig_start_bit = 239
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Actv_NoActv': 0, 'Actv_Actv': 1, 'Actv_Reserved1': 2, 'Actv_Reserved2': 3}
        compute_method = None
        length = 2
        startbit = 239
        byte = 29
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class AvhStsChks:
        sig_name = "AvhStsChks"
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

    class AbsFctStsSts2:
        sig_name = "AbsFctStsSts2"
        sig_start_bit = 11
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Sts2_Initial': 0, 'Sts2_Normal': 1, 'Sts2_Fault': 2, 'Sts2_Off': 3}
        compute_method = None
        length = 3
        startbit = 11
        byte = 1
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class CrbStsSts2:
        sig_name = "CrbStsSts2"
        sig_start_bit = 179
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Sts2_Initial': 0, 'Sts2_Normal': 1, 'Sts2_Fault': 2, 'Sts2_Off': 3}
        compute_method = None
        length = 3
        startbit = 179
        byte = 22
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class VdcStsChks:
        sig_name = "VdcStsChks"
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

    class CdpStsSts2:
        sig_name = "CdpStsSts2"
        sig_start_bit = 155
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Sts2_Initial': 0, 'Sts2_Normal': 1, 'Sts2_Fault': 2, 'Sts2_Off': 3}
        compute_method = None
        length = 3
        startbit = 155
        byte = 19
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class BrkSysWarnReqBrkSysWarn:
        sig_name = "BrkSysWarnReqBrkSysWarn"
        sig_start_bit = 67
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
        startbit = 67
        byte = 8
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class CrbStsActv:
        sig_name = "CrbStsActv"
        sig_start_bit = 191
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Actv_NoActv': 0, 'Actv_Actv': 1, 'Actv_Reserved1': 2, 'Actv_Reserved2': 3}
        compute_method = None
        length = 2
        startbit = 191
        byte = 23
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class AvhStsCntr:
        sig_name = "AvhStsCntr"
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

    class SsmStsByPark:
        sig_name = "SsmStsByPark"
        sig_start_bit = 284
        update_id_bit = 281
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'StandstillMgrStsByPark_NoReq': 0, 'StandstillMgrStsByPark_ByDrvr': 1, 'StandstillMgrStsByPark_ByTimeOut': 2, 'StandstillMgrStsByPark_ByAuto': 3, 'StandstillMgrStsByPark_Reserved1': 4, 'StandstillMgrStsByPark_Reserved2': 5}
        compute_method = None
        length = 3
        startbit = 284
        byte = 35
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class AbsFctStsChks:
        sig_name = "AbsFctStsChks"
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

    class AvhStsSts2:
        sig_name = "AvhStsSts2"
        sig_start_bit = 43
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Sts2_Initial': 0, 'Sts2_Normal': 1, 'Sts2_Fault': 2, 'Sts2_Off': 3}
        compute_method = None
        length = 3
        startbit = 43
        byte = 5
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class CdpSts_UB:
        sig_name = "CdpSts_UB"
        sig_start_bit = 165
        update_id_bit = 165
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
        startbit = 165
        byte = 20
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VdcStsCntr:
        sig_name = "VdcStsCntr"
        sig_start_bit = 279
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
        startbit = 279
        byte = 34
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class BrkTqFricActFR:
        sig_name = "BrkTqFricActFR"
        sig_start_bit = 97
        update_id_bit = None
        sig_length = 14
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 16000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 14
        startbit = 97
        bmuws_info = [(12, 0b00000011, 0b11111100, 2, 0), (13, 0b11111111, 0b00000000, 8, 0), (14, 0b11110000, 0b00001111, 4, 4)]

    class SsmStsByBrk_UB:
        sig_name = "SsmStsByBrk_UB"
        sig_start_bit = 304
        update_id_bit = 304
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
        startbit = 304
        byte = 38
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class BrkTqFricActRR:
        sig_name = "BrkTqFricActRR"
        sig_start_bit = 133
        update_id_bit = None
        sig_length = 14
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 16000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 14
        startbit = 133
        bmuws_info = [(16, 0b00111111, 0b11000000, 6, 0), (17, 0b11111111, 0b00000000, 8, 0)]

    class BrkTqFricActFL:
        sig_name = "BrkTqFricActFL"
        sig_start_bit = 95
        update_id_bit = None
        sig_length = 14
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 16000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 14
        startbit = 95
        bmuws_info = [(11, 0b11111111, 0b00000000, 8, 0), (12, 0b11111100, 0b00000011, 6, 2)]

    class AbsFctStsEna:
        sig_name = "AbsFctStsEna"
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
        sig_value_table = {'EnableDisable2_Disabled': 0, 'EnableDisable2_Enabled': 1}
        compute_method = None
        length = 1
        startbit = 8
        byte = 1
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VdcStsSts2:
        sig_name = "VdcStsSts2"
        sig_start_bit = 275
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Sts2_Initial': 0, 'Sts2_Normal': 1, 'Sts2_Fault': 2, 'Sts2_Off': 3}
        compute_method = None
        length = 3
        startbit = 275
        byte = 34
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class VdcStsEna:
        sig_name = "VdcStsEna"
        sig_start_bit = 272
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EnableDisable2_Disabled': 0, 'EnableDisable2_Enabled': 1}
        compute_method = None
        length = 1
        startbit = 272
        byte = 34
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class AbsFctStsActv:
        sig_name = "AbsFctStsActv"
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
        sig_value_table = {'Actv_NoActv': 0, 'Actv_Actv': 1, 'Actv_Reserved1': 2, 'Actv_Reserved2': 3}
        compute_method = None
        length = 2
        startbit = 23
        byte = 2
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class BrkTqArbdReq:
        sig_name = "BrkTqArbdReq"
        sig_start_bit = 79
        update_id_bit = 81
        sig_length = 14
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 16000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 14
        startbit = 79
        bmuws_info = [(9, 0b11111111, 0b00000000, 8, 0), (10, 0b11111100, 0b00000011, 6, 2)]

    class DsrStsSts2:
        sig_name = "DsrStsSts2"
        sig_start_bit = 227
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Sts2_Initial': 0, 'Sts2_Normal': 1, 'Sts2_Fault': 2, 'Sts2_Off': 3}
        compute_method = None
        length = 3
        startbit = 227
        byte = 28
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class SsmStsByBrkChks:
        sig_name = "SsmStsByBrkChks"
        sig_start_bit = 303
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 303
        byte = 37
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CdpStsEna:
        sig_name = "CdpStsEna"
        sig_start_bit = 152
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EnableDisable2_Disabled': 0, 'EnableDisable2_Enabled': 1}
        compute_method = None
        length = 1
        startbit = 152
        byte = 19
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class HdcStsCntr:
        sig_name = "HdcStsCntr"
        sig_start_bit = 255
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
        startbit = 255
        byte = 31
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class HdcStsActv:
        sig_name = "HdcStsActv"
        sig_start_bit = 263
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Actv_NoActv': 0, 'Actv_Actv': 1, 'Actv_Reserved1': 2, 'Actv_Reserved2': 3}
        compute_method = None
        length = 2
        startbit = 263
        byte = 32
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class DTCActvRe:
        sig_name = "DTCActvRe"
        sig_start_bit = 212
        update_id_bit = 210
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Actv_NoActv': 0, 'Actv_Actv': 1, 'Actv_Reserved1': 2, 'Actv_Reserved2': 3}
        compute_method = None
        length = 2
        startbit = 212
        byte = 26
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class BrkSysWarnReq_UB:
        sig_name = "BrkSysWarnReq_UB"
        sig_start_bit = 66
        update_id_bit = 66
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
        startbit = 66
        byte = 8
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class DsrStsChks:
        sig_name = "DsrStsChks"
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

    class HdcStsEna:
        sig_name = "HdcStsEna"
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
        sig_value_table = {'EnableDisable2_Disabled': 0, 'EnableDisable2_Enabled': 1}
        compute_method = None
        length = 1
        startbit = 248
        byte = 31
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class HdcLampReq:
        sig_name = "HdcLampReq"
        sig_start_bit = 236
        update_id_bit = 234
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BrkLamp3_Off': 0, 'BrkLamp3_Standby': 1, 'BrkLamp3_Active': 2, 'BrkLamp3_Fault': 3}
        compute_method = None
        length = 2
        startbit = 236
        byte = 29
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class AvhSts_UB:
        sig_name = "AvhSts_UB"
        sig_start_bit = 24
        update_id_bit = 24
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
        startbit = 24
        byte = 3
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VdcSts_UB:
        sig_name = "VdcSts_UB"
        sig_start_bit = 285
        update_id_bit = 285
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
        startbit = 285
        byte = 35
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class SsmStsByBrkCntr:
        sig_name = "SsmStsByBrkCntr"
        sig_start_bit = 311
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
        startbit = 311
        byte = 38
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class AvhLampReq:
        sig_name = "AvhLampReq"
        sig_start_bit = 20
        update_id_bit = 18
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BrkLamp3_Off': 0, 'BrkLamp3_Standby': 1, 'BrkLamp3_Active': 2, 'BrkLamp3_Fault': 3}
        compute_method = None
        length = 2
        startbit = 20
        byte = 2
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class AvhMsgReq:
        sig_name = "AvhMsgReq"
        sig_start_bit = 27
        update_id_bit = 17
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AvhMsg_NoMsg': 0, 'AvhMsg_StandbyOn': 1, 'AvhMsg_ActiveOn': 2, 'AvhMsg_BrkPedlToRel': 3, 'AvhMsg_Fault': 4, 'AvhMsg_Reserved': 5}
        compute_method = None
        length = 3
        startbit = 27
        byte = 3
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class CstStsChks:
        sig_name = "CstStsChks"
        sig_start_bit = 199
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
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

    class DsrStsCntr:
        sig_name = "DsrStsCntr"
        sig_start_bit = 231
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
        startbit = 231
        byte = 28
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class HAZBrkLiReq:
        sig_name = "HAZBrkLiReq"
        sig_start_bit = 185
        update_id_bit = 160
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HazBrkLight_NotInprogress': 0, 'HazBrkLight_InProgress': 1, 'HazBrkLight_InProgressSpdLow': 2}
        compute_method = None
        length = 2
        startbit = 185
        byte = 23
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class SsmStsByBrkStandstilMgrSts:
        sig_name = "SsmStsByBrkStandstilMgrSts"
        sig_start_bit = 307
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'StandstilMgrSts_Val0': 0, 'StandstilMgrSts_Val1': 1, 'StandstilMgrSts_Val2': 2, 'StandstilMgrSts_Val3': 3, 'StandstilMgrSts_Val4': 4, 'StandstilMgrSts_Val5': 5, 'StandstilMgrSts_Val6': 6, 'StandstilMgrSts_Val7': 7}
        compute_method = None
        length = 3
        startbit = 307
        byte = 38
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class CdpStsChks:
        sig_name = "CdpStsChks"
        sig_start_bit = 151
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 151
        byte = 18
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CdpStsCntr:
        sig_name = "CdpStsCntr"
        sig_start_bit = 159
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
        startbit = 159
        byte = 19
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class HdcStsChks:
        sig_name = "HdcStsChks"
        sig_start_bit = 247
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 247
        byte = 30
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HdcStsSts2:
        sig_name = "HdcStsSts2"
        sig_start_bit = 251
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Sts2_Initial': 0, 'Sts2_Normal': 1, 'Sts2_Fault': 2, 'Sts2_Off': 3}
        compute_method = None
        length = 3
        startbit = 251
        byte = 31
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1


class BCU2PropulsionCANFDFr01:
    msg_name = "BCU2PropulsionCANFDFr01"
    msg_id = 65
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "BCU2"
    rx_nodes = ['BCU1']
    sig_group_dict = {'BrkSysStSec': ['BrkSysStSecBrkSysSts', 'BrkSysStSecChks', 'BrkSysStSecCntr']}
    sig_group_dataid_dict = {}

    class BrkSysStSecChks:
        sig_name = "BrkSysStSecChks"
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

    class BrkSysStSecBrkSysSts:
        sig_name = "BrkSysStSecBrkSysSts"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class BrkSysStSecCntr:
        sig_name = "BrkSysStSecCntr"
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

    class BrkSysStSec_UB:
        sig_name = "BrkSysStSec_UB"
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


class BECMPropulsionCANFDFr06:
    msg_name = "BECMPropulsionCANFDFr06"
    msg_id = 816
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.2
    msg_length = 64
    tx_node = "BECM"
    rx_nodes = ['VCU', 'CCUMCUCD']
    sig_group_dict = {'HvBattCod': ['HvBattCodPackCodeIndex', 'HvBattCodPackCodeX1', 'HvBattCodPackCodeX2', 'HvBattCodPackCodeX3', 'HvBattCodPackCodeX4', 'HvBattCodPackCodeX5', 'HvBattCodPackCodeX6'], 'HVBattCellTVal': ['HVBattCellTValCellTMax', 'HVBattCellTValCellTMaxSnsrSerlNr', 'HVBattCellTValCellTMin', 'HVBattCellTValCellTMinSnsrSerlNr', 'HVBattCellTValCellTSnsrNr', 'HVBattCellTValCellTSnsrT'], 'HVBattCellUVal': ['HVBattCellUValU1', 'HVBattCellUValU2', 'HVBattCellUValU3', 'HVBattCellUValU4'], 'HvBattCellT': ['HvBattCellTAvg', 'HvBattCellTMax', 'HvBattCellTMin']}
    sig_group_dataid_dict = {}

    class HVBattUMinSerlNr:
        sig_name = "HVBattUMinSerlNr"
        sig_start_bit = 127
        update_id_bit = 150
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 127
        byte = 15
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvBattCodPackCodeX4:
        sig_name = "HvBattCodPackCodeX4"
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

    class HVBattCellTValCellTSnsrNr:
        sig_name = "HVBattCellTValCellTSnsrNr"
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

    class HvBattCellTMin:
        sig_name = "HvBattCellTMin"
        sig_start_bit = 29
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = -256.0
        sig_value_min = 0
        sig_value_max = 5119
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 29
        bmuws_info = [(3, 0b00111111, 0b11000000, 6, 0), (4, 0b11111110, 0b00000001, 7, 1)]

    class HvBattCellTAvg:
        sig_name = "HvBattCellTAvg"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = -256.0
        sig_value_min = 0
        sig_value_max = 5119
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111000, 0b00000111, 5, 3)]

    class HVBattCellTValCellTMax:
        sig_name = "HVBattCellTValCellTMax"
        sig_start_bit = 159
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 159
        byte = 19
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvBattCodPackCodeX5:
        sig_name = "HvBattCodPackCodeX5"
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

    class HVBattCellTValCellTMaxSnsrSerlNr:
        sig_name = "HVBattCellTValCellTMaxSnsrSerlNr"
        sig_start_bit = 167
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
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

    class HvBattTotChrgCap:
        sig_name = "HvBattTotChrgCap"
        sig_start_bit = 319
        update_id_bit = 447
        sig_length = 32
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4294967295
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 32
        startbit = 319
        bmuws_info = [(39, 0b11111111, 0b00000000, 8, 0), (40, 0b11111111, 0b00000000, 8, 0), (41, 0b11111111, 0b00000000, 8, 0), (42, 0b11111111, 0b00000000, 8, 0)]

    class HvBattTotChrgEgy:
        sig_name = "HvBattTotChrgEgy"
        sig_start_bit = 351
        update_id_bit = 446
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
        startbit = 351
        bmuws_info = [(43, 0b11111111, 0b00000000, 8, 0), (44, 0b11111111, 0b00000000, 8, 0), (45, 0b11111111, 0b00000000, 8, 0), (46, 0b11111111, 0b00000000, 8, 0)]

    class HVPackUUnderFltLvl:
        sig_name = "HVPackUUnderFltLvl"
        sig_start_bit = 469
        update_id_bit = 484
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltLvl_Normal': 0, 'FltLvl_LevelI': 1, 'FltLvl_LevelII': 2, 'FltLvl_LevelIII': 3}
        compute_method = None
        length = 2
        startbit = 469
        byte = 58
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class HvBattTotDchaCap:
        sig_name = "HvBattTotDchaCap"
        sig_start_bit = 383
        update_id_bit = 445
        sig_length = 32
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4294967295
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 32
        startbit = 383
        bmuws_info = [(47, 0b11111111, 0b00000000, 8, 0), (48, 0b11111111, 0b00000000, 8, 0), (49, 0b11111111, 0b00000000, 8, 0), (50, 0b11111111, 0b00000000, 8, 0)]

    class HVSOCLoFltLvl:
        sig_name = "HVSOCLoFltLvl"
        sig_start_bit = 479
        update_id_bit = 481
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltLvl_Normal': 0, 'FltLvl_LevelI': 1, 'FltLvl_LevelII': 2, 'FltLvl_LevelIII': 3}
        compute_method = None
        length = 2
        startbit = 479
        byte = 59
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HvBattCod_UB:
        sig_name = "HvBattCod_UB"
        sig_start_bit = 232
        update_id_bit = 232
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
        startbit = 232
        byte = 29
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class HVBattCellTSnsrNr:
        sig_name = "HVBattCellTSnsrNr"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HVCellTOverFltLvl:
        sig_name = "HVCellTOverFltLvl"
        sig_start_bit = 453
        update_id_bit = 476
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltLvl_Normal': 0, 'FltLvl_LevelI': 1, 'FltLvl_LevelII': 2, 'FltLvl_LevelIII': 3}
        compute_method = None
        length = 2
        startbit = 453
        byte = 56
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class HVBattCellTValCellTSnsrT:
        sig_name = "HVBattCellTValCellTSnsrT"
        sig_start_bit = 199
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -40.0
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

    class HVBattCellUValU4:
        sig_name = "HVBattCellUValU4"
        sig_start_bit = 231
        update_id_bit = None
        sig_length = 13
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 231
        bmuws_info = [(28, 0b11111111, 0b00000000, 8, 0), (29, 0b11111000, 0b00000111, 5, 3)]

    class HvBattCodPackCodeIndex:
        sig_name = "HvBattCodPackCodeIndex"
        sig_start_bit = 247
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 247
        byte = 30
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HVCellUOverFltLvl:
        sig_name = "HVCellUOverFltLvl"
        sig_start_bit = 449
        update_id_bit = 474
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltLvl_Normal': 0, 'FltLvl_LevelI': 1, 'FltLvl_LevelII': 2, 'FltLvl_LevelIII': 3}
        compute_method = None
        length = 2
        startbit = 449
        byte = 56
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class HVBattCp:
        sig_name = "HVBattCp"
        sig_start_bit = 79
        update_id_bit = 139
        sig_length = 16
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 65535
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 79
        bmuws_info = [(9, 0b11111111, 0b00000000, 8, 0), (10, 0b11111111, 0b00000000, 8, 0)]

    class HVBattCellTVal_UB:
        sig_name = "HVBattCellTVal_UB"
        sig_start_bit = 148
        update_id_bit = 148
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
        startbit = 148
        byte = 18
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class HVIsoFltLvl:
        sig_name = "HVIsoFltLvl"
        sig_start_bit = 459
        update_id_bit = 487
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltLvl_Normal': 0, 'FltLvl_LevelI': 1, 'FltLvl_LevelII': 2, 'FltLvl_LevelIII': 3}
        compute_method = None
        length = 2
        startbit = 459
        byte = 57
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class HVBattCellUVal_UB:
        sig_name = "HVBattCellUVal_UB"
        sig_start_bit = 147
        update_id_bit = 147
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
        startbit = 147
        byte = 18
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class HVBattPackSOCR:
        sig_name = "HVBattPackSOCR"
        sig_start_bit = 299
        update_id_bit = 305
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1020
        sig_byteorder = "Motorola"
        sig_value_init = 1020
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 299
        bmuws_info = [(37, 0b00001111, 0b11110000, 4, 0), (38, 0b11111100, 0b00000011, 6, 2)]

    class HVBattCellTMinSerlNr:
        sig_name = "HVBattCellTMinSerlNr"
        sig_start_bit = 55
        update_id_bit = 142
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
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

    class HVBattCellTValCellTMinSnsrSerlNr:
        sig_name = "HVBattCellTValCellTMinSnsrSerlNr"
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

    class HvBattCellT_UB:
        sig_name = "HvBattCellT_UB"
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

    class HVCellUUnderFltLvl:
        sig_name = "HVCellUUnderFltLvl"
        sig_start_bit = 463
        update_id_bit = 473
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltLvl_Normal': 0, 'FltLvl_LevelI': 1, 'FltLvl_LevelII': 2, 'FltLvl_LevelIII': 3}
        compute_method = None
        length = 2
        startbit = 463
        byte = 57
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HVBattCellUValU1:
        sig_name = "HVBattCellUValU1"
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

    class HVPackSerlNr:
        sig_name = "HVPackSerlNr"
        sig_start_bit = 135
        update_id_bit = 149
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 135
        byte = 16
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HVBattCellTValCellTMin:
        sig_name = "HVBattCellTValCellTMin"
        sig_start_bit = 175
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -40.0
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

    class HVBattCellUValU3:
        sig_name = "HVBattCellUValU3"
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

    class HVILFltSt:
        sig_name = "HVILFltSt"
        sig_start_bit = 461
        update_id_bit = 472
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OpenCls2_Default': 0, 'OpenCls2_Close': 1, 'OpenCls2_Open': 2, 'OpenCls2_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 461
        byte = 57
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class HvBattCodPackCodeX2:
        sig_name = "HvBattCodPackCodeX2"
        sig_start_bit = 263
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 263
        byte = 32
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HVBattMngtSysNr:
        sig_name = "HVBattMngtSysNr"
        sig_start_bit = 95
        update_id_bit = 138
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 95
        byte = 11
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvBattCodPackCodeX3:
        sig_name = "HvBattCodPackCodeX3"
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

    class HVBattMatchErr:
        sig_name = "HVBattMatchErr"
        sig_start_bit = 301
        update_id_bit = 300
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
        startbit = 301
        byte = 37
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class HVBattMngtSysPackNr:
        sig_name = "HVBattMngtSysPackNr"
        sig_start_bit = 103
        update_id_bit = 137
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 103
        byte = 12
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HVBattCodLen:
        sig_name = "HVBattCodLen"
        sig_start_bit = 71
        update_id_bit = 140
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 71
        byte = 8
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HVBattCellUValU2:
        sig_name = "HVBattCellUValU2"
        sig_start_bit = 215
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
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

    class HVBattUMaxSerlNr:
        sig_name = "HVBattUMaxSerlNr"
        sig_start_bit = 119
        update_id_bit = 151
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 119
        byte = 14
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HVBattFltIndcn:
        sig_name = "HVBattFltIndcn"
        sig_start_bit = 303
        update_id_bit = 302
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
        startbit = 303
        byte = 37
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class HVBattCellTMaxSerlNr:
        sig_name = "HVBattCellTMaxSerlNr"
        sig_start_bit = 47
        update_id_bit = 143
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 250
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

    class HVBattSubSysNr:
        sig_name = "HVBattSubSysNr"
        sig_start_bit = 111
        update_id_bit = 136
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 111
        byte = 13
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HVCellUDifFltLvl:
        sig_name = "HVCellUDifFltLvl"
        sig_start_bit = 451
        update_id_bit = 475
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltLvl_Normal': 0, 'FltLvl_LevelI': 1, 'FltLvl_LevelII': 2, 'FltLvl_LevelIII': 3}
        compute_method = None
        length = 2
        startbit = 451
        byte = 56
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class HvBattTotDchaEgy:
        sig_name = "HvBattTotDchaEgy"
        sig_start_bit = 415
        update_id_bit = 444
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
        startbit = 415
        bmuws_info = [(51, 0b11111111, 0b00000000, 8, 0), (52, 0b11111111, 0b00000000, 8, 0), (53, 0b11111111, 0b00000000, 8, 0), (54, 0b11111111, 0b00000000, 8, 0)]

    class HVCellTDifFltLvl:
        sig_name = "HVCellTDifFltLvl"
        sig_start_bit = 455
        update_id_bit = 477
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltLvl_Normal': 0, 'FltLvl_LevelI': 1, 'FltLvl_LevelII': 2, 'FltLvl_LevelIII': 3}
        compute_method = None
        length = 2
        startbit = 455
        byte = 56
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HvBattCodPackCodeX6:
        sig_name = "HvBattCodPackCodeX6"
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

    class HVSOCHiFltLvl:
        sig_name = "HVSOCHiFltLvl"
        sig_start_bit = 467
        update_id_bit = 483
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltLvl_Normal': 0, 'FltLvl_LevelI': 1, 'FltLvl_LevelII': 2, 'FltLvl_LevelIII': 3}
        compute_method = None
        length = 2
        startbit = 467
        byte = 58
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class HVPackOverChrgFltLvl:
        sig_name = "HVPackOverChrgFltLvl"
        sig_start_bit = 457
        update_id_bit = 486
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltLvl_Normal': 0, 'FltLvl_LevelI': 1, 'FltLvl_LevelII': 2, 'FltLvl_LevelIII': 3}
        compute_method = None
        length = 2
        startbit = 457
        byte = 57
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class HVSOCHopFltLvl:
        sig_name = "HVSOCHopFltLvl"
        sig_start_bit = 465
        update_id_bit = 482
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltLvl_Normal': 0, 'FltLvl_LevelI': 1, 'FltLvl_LevelII': 2, 'FltLvl_LevelIII': 3}
        compute_method = None
        length = 2
        startbit = 465
        byte = 58
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class HvBattCellTMax:
        sig_name = "HvBattCellTMax"
        sig_start_bit = 10
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = -256.0
        sig_value_min = 0
        sig_value_max = 5119
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 10
        bmuws_info = [(1, 0b00000111, 0b11111000, 3, 0), (2, 0b11111111, 0b00000000, 8, 0), (3, 0b11000000, 0b00111111, 2, 6)]

    class HVPackUOverFltLvl:
        sig_name = "HVPackUOverFltLvl"
        sig_start_bit = 471
        update_id_bit = 485
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltLvl_Normal': 0, 'FltLvl_LevelI': 1, 'FltLvl_LevelII': 2, 'FltLvl_LevelIII': 3}
        compute_method = None
        length = 2
        startbit = 471
        byte = 58
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HvBattCodPackCodeX1:
        sig_name = "HvBattCodPackCodeX1"
        sig_start_bit = 255
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 255
        byte = 31
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class BCU1PropulsionCANFDNmFr:
    msg_name = "BCU1PropulsionCANFDNmFr"
    msg_id = 1283
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BCU1"
    rx_nodes = ['VCU']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class BECMPropulsionCANFDFr03:
    msg_name = "BECMPropulsionCANFDFr03"
    msg_id = 384
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 32
    tx_node = "BECM"
    rx_nodes = ['VCU', 'CCUMCUCD', 'MGM', 'IEM']
    sig_group_dict = {'HVBattCellU': ['HVBattCellUUMax', 'HVBattCellUUMaxId', 'HVBattCellUUMin', 'HVBattCellUUMinId'], 'HVBattPackSOCLim': ['HVBattPackSOCLimHi', 'HVBattPackSOCLimLow', 'HVBattPackSOCLimMax', 'HVBattPackSOCLimMin']}
    sig_group_dataid_dict = {}

    class HVBattPackILim:
        sig_name = "HVBattPackILim"
        sig_start_bit = 87
        update_id_bit = 72
        sig_length = 16
        sig_value_factor = 0.1
        sig_value_offset = -3000.0
        sig_value_min = 0
        sig_value_max = 65535
        sig_byteorder = "Motorola"
        sig_value_init = 30000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 87
        bmuws_info = [(10, 0b11111111, 0b00000000, 8, 0), (11, 0b11111111, 0b00000000, 8, 0)]

    class HVBattCellUUMaxId:
        sig_name = "HVBattCellUUMaxId"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 250
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

    class HVBattCellUUMin:
        sig_name = "HVBattCellUUMin"
        sig_start_bit = 10
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 0.001
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 5000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 10
        bmuws_info = [(1, 0b00000111, 0b11111000, 3, 0), (2, 0b11111111, 0b00000000, 8, 0), (3, 0b11000000, 0b00111111, 2, 6)]

    class HVBattCellUUMax:
        sig_name = "HVBattCellUUMax"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 0.001
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 5000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111000, 0b00000111, 5, 3)]

    class HVBattCellU_UB:
        sig_name = "HVBattCellU_UB"
        sig_start_bit = 24
        update_id_bit = 24
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
        startbit = 24
        byte = 3
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class HVBattCellUUMinId:
        sig_name = "HVBattCellUUMinId"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 250
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

    class HVBattPackEgyAvlDcha:
        sig_name = "HVBattPackEgyAvlDcha"
        sig_start_bit = 57
        update_id_bit = 76
        sig_length = 13
        sig_value_factor = 20
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 57
        bmuws_info = [(7, 0b00000011, 0b11111100, 2, 0), (8, 0b11111111, 0b00000000, 8, 0), (9, 0b11100000, 0b00011111, 3, 5)]

    class HVBattPackSOCLimHi:
        sig_name = "HVBattPackSOCLimHi"
        sig_start_bit = 119
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 2040
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 119
        bmuws_info = [(14, 0b11111111, 0b00000000, 8, 0), (15, 0b11100000, 0b00011111, 3, 5)]

    class HVBattPrecReq:
        sig_name = "HVBattPrecReq"
        sig_start_bit = 107
        update_id_bit = 106
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
        startbit = 107
        byte = 13
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class HVBattPackSOCLimMin:
        sig_name = "HVBattPackSOCLimMin"
        sig_start_bit = 150
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 2040
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 150
        bmuws_info = [(18, 0b01111111, 0b10000000, 7, 0), (19, 0b11110000, 0b00001111, 4, 4)]

    class HVBattPackSOCLim_UB:
        sig_name = "HVBattPackSOCLim_UB"
        sig_start_bit = 155
        update_id_bit = 155
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
        startbit = 155
        byte = 19
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class HVBattPackULim:
        sig_name = "HVBattPackULim"
        sig_start_bit = 167
        update_id_bit = 152
        sig_length = 16
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 65535
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 167
        bmuws_info = [(20, 0b11111111, 0b00000000, 8, 0), (21, 0b11111111, 0b00000000, 8, 0)]

    class HVBattPackEgyAvlChrg:
        sig_name = "HVBattPackEgyAvlChrg"
        sig_start_bit = 55
        update_id_bit = 58
        sig_length = 13
        sig_value_factor = 20
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 55
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111000, 0b00000111, 5, 3)]

    class HVBattPackSOCLimMax:
        sig_name = "HVBattPackSOCLimMax"
        sig_start_bit = 129
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 2040
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 129
        bmuws_info = [(16, 0b00000011, 0b11111100, 2, 0), (17, 0b11111111, 0b00000000, 8, 0), (18, 0b10000000, 0b01111111, 1, 7)]

    class HVBattPackOverDchaFlg:
        sig_name = "HVBattPackOverDchaFlg"
        sig_start_bit = 75
        update_id_bit = 73
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffCrit1_NotVld1': 0, 'OnOffCrit1_Off': 1, 'OnOffCrit1_On': 2, 'OnOffCrit1_NotVld2': 3}
        compute_method = None
        length = 2
        startbit = 75
        byte = 9
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class HVBattPackSOC:
        sig_name = "HVBattPackSOC"
        sig_start_bit = 103
        update_id_bit = 108
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 2040
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 103
        bmuws_info = [(12, 0b11111111, 0b00000000, 8, 0), (13, 0b11100000, 0b00011111, 3, 5)]

    class HVBattPackSOCLimLow:
        sig_name = "HVBattPackSOCLimLow"
        sig_start_bit = 124
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 2040
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 124
        bmuws_info = [(15, 0b00011111, 0b11100000, 5, 0), (16, 0b11111100, 0b00000011, 6, 2)]


class SRSPropulsionCANFDFr01:
    msg_name = "SRSPropulsionCANFDFr01"
    msg_id = 69
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 16
    tx_node = "SRS"
    rx_nodes = ['VCU', 'CCUMCUCD', 'MGM', 'IEM', 'BECM']
    sig_group_dict = {'CrashInfo': ['CrashInfoCrashFrnt', 'CrashInfoCrashOffroadA', 'CrashInfoCrashOffroadD', 'CrashInfoCrashOffroadRT', 'CrashInfoCrashOffroadRTsevere', 'CrashInfoCrashPed', 'CrashInfoCrashRe', 'CrashInfoCrashRollovr', 'CrashInfoCrashSideLe', 'CrashInfoCrashSideRi', 'CrashInfoCrashState', 'CrashInfoImpctDvx', 'CrashInfoImpctDvy', 'CrashInfoImpctRollAg', 'CrashInfoVehOri'], 'CrashSts': ['CrashSts2', 'CrashStsChks', 'CrashStsCntr']}
    sig_group_dataid_dict = {'CrashSts': 1073}

    class CrashStsChks:
        sig_name = "CrashStsChks"
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

    class CrashInfoCrashOffroadRTsevere:
        sig_name = "CrashInfoCrashOffroadRTsevere"
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

    class CrashInfo_UB:
        sig_name = "CrashInfo_UB"
        sig_start_bit = 8
        update_id_bit = 8
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
        startbit = 8
        byte = 1
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class CrashInfoCrashPed:
        sig_name = "CrashInfoCrashPed"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 2
        byte = 0
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class CrashSts_UB:
        sig_name = "CrashSts_UB"
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

    class CrashInfoCrashOffroadD:
        sig_name = "CrashInfoCrashOffroadD"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class PedProtnSts:
        sig_name = "PedProtnSts"
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
        sig_value_table = {'PedProtnSts_Invalid': 0, 'PedProtnSts_NotActvn': 1, 'PedProtnSts_Actvn': 2, 'PedProtnSts_Error': 3}
        compute_method = None
        length = 2
        startbit = 63
        byte = 7
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class CrashInfoCrashRollovr:
        sig_name = "CrashInfoCrashRollovr"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 0
        byte = 0
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class CrashInfoCrashRe:
        sig_name = "CrashInfoCrashRe"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 1
        byte = 0
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class LgtSpdChgSts:
        sig_name = "LgtSpdChgSts"
        sig_start_bit = 77
        update_id_bit = 84
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = -256
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 77
        bmuws_info = [(9, 0b00111111, 0b11000000, 6, 0), (10, 0b11100000, 0b00011111, 3, 5)]

    class CrashInfoCrashOffroadRT:
        sig_name = "CrashInfoCrashOffroadRT"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 4
        byte = 0
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class CrashSts2:
        sig_name = "CrashSts2"
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
        sig_value_table = {'CrashSts2_NoCrash': 0, 'CrashSts2_Crash': 1}
        compute_method = None
        length = 1
        startbit = 55
        byte = 6
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class CrashInfoCrashSideRi:
        sig_name = "CrashInfoCrashSideRi"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 14
        byte = 1
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class CrashInfoImpctDvy:
        sig_name = "CrashInfoImpctDvy"
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

    class CrashInfoVehOri:
        sig_name = "CrashInfoVehOri"
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
        sig_value_table = {'Orntn_Invalid': 0, 'Orntn_OnWheels': 1, 'Orntn_LeftSide': 2, 'Orntn_RightSide': 3, 'Orntn_OnRoof': 4, 'Orntn_Indeterminate': 5, 'Orntn_Resd1': 6, 'Orntn_Resd2': 7}
        compute_method = None
        length = 3
        startbit = 11
        byte = 1
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class CrashInfoImpctRollAg:
        sig_name = "CrashInfoImpctRollAg"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 15
        sig_value_offset = 0
        sig_value_min = 0
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

    class CrashInfoCrashState:
        sig_name = "CrashInfoCrashState"
        sig_start_bit = 13
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CrashProc_NoCrash': 0, 'CrashProc_CrashImminent': 1, 'CrashProc_CrashInProgress': 2, 'CrashProc_CrashEnding': 3}
        compute_method = None
        length = 2
        startbit = 13
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class CrashInfoImpctDvx:
        sig_name = "CrashInfoImpctDvx"
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

    class RestrntSysSts:
        sig_name = "RestrntSysSts"
        sig_start_bit = 60
        update_id_bit = 57
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'RestrntSysSts_Invalid': 0, 'RestrntSysSts_Normal': 1, 'RestrntSysSts_Fault_Level1': 2, 'RestrntSysSts_Fault_Level2': 3, 'RestrntSysSts_Fault_Level3': 4, 'RestrntSysSts_Others': 5}
        compute_method = None
        length = 3
        startbit = 60
        byte = 7
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class CrashStsCntr:
        sig_name = "CrashStsCntr"
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

    class CrashInfoCrashFrnt:
        sig_name = "CrashInfoCrashFrnt"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class LatSpdChgSts:
        sig_name = "LatSpdChgSts"
        sig_start_bit = 71
        update_id_bit = 78
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = -256
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 71
        bmuws_info = [(8, 0b11111111, 0b00000000, 8, 0), (9, 0b10000000, 0b01111111, 1, 7)]

    class CrashInfoCrashSideLe:
        sig_name = "CrashInfoCrashSideLe"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 15
        byte = 1
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class CrashInfoCrashOffroadA:
        sig_name = "CrashInfoCrashOffroadA"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6


class IEMPropulsionCANFDFr05:
    msg_name = "IEMPropulsionCANFDFr05"
    msg_id = 613
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 64
    tx_node = "IEM"
    rx_nodes = ['VCU', 'BECM', 'CCUMCUCD']
    sig_group_dict = {'ReMotHeatgFb': ['ReMotHeatgFbMotSts', 'ReMotHeatgFbPwrAvl'], 'BoostFcnResvSigGrp': ['BoostFcnResvSigGrpDevelpSignalGroup1', 'BoostFcnResvSigGrpDevelpSignalGroup2', 'BoostFcnResvSigGrpDevelpSignalGroup3', 'BoostFcnResvSigGrpDevelpSignalGroup4', 'BoostFcnResvSigGrpDevelpSignalGroup5', 'BoostFcnResvSigGrpDevelpSignalGroup6', 'BoostFcnResvSigGrpDevelpSignalGroup7', 'BoostFcnResvSigGrpDevelpSignalGroup8'], 'BoostFcnResvSigGrp1': ['BoostFcnResvSigGrp1Word0', 'BoostFcnResvSigGrp1Word1', 'BoostFcnResvSigGrp1Word2', 'BoostFcnResvSigGrp1Word3'], 'ReMotInfo': ['ReMotInfoActvDchaAlrmSt', 'ReMotInfoActvHeatgAlrmSt', 'ReMotInfoBoostAlrmSt', 'ReMotInfoDTCHig', 'ReMotInfoDTCLMid', 'ReMotInfoDTCLow', 'ReMotInfoDTCSts', 'ReMotInfoEMQnty', 'ReMotInfoEMSeqNr', 'ReMotInfoFltAlrmSt', 'ReMotInfoInvrtTAlrmSt', 'ReMotInfoIPhaAlrmSt', 'ReMotInfoModStRms', 'ReMotInfoMotTAlrmSt', 'ReMotInfoOilTAlrmSt', 'ReMotInfoOverSpdAlrmSt', 'ReMotInfoPasDchaAlrmSt', 'ReMotInfoPlsHeatAlrmSt', 'ReMotInfoRatTypeInfo', 'ReMotInfoRslAlrmSt', 'ReMotInfoTqAlrmSt', 'ReMotInfoUDCAlrmSt']}
    sig_group_dataid_dict = {}

    class ReMotHeatgPwrMax:
        sig_name = "ReMotHeatgPwrMax"
        sig_start_bit = 300
        update_id_bit = 307
        sig_length = 9
        sig_value_factor = 10
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 300
        bmuws_info = [(37, 0b00011111, 0b11100000, 5, 0), (38, 0b11110000, 0b00001111, 4, 4)]

    class BoostFcnResvSigGrpDevelpSignalGroup6:
        sig_name = "BoostFcnResvSigGrpDevelpSignalGroup6"
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

    class BoostFcnResvSigGrpDevelpSignalGroup7:
        sig_name = "BoostFcnResvSigGrpDevelpSignalGroup7"
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

    class ReMotInfoPlsHeatAlrmSt:
        sig_name = "ReMotInfoPlsHeatAlrmSt"
        sig_start_bit = 331
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSts_Disarmd': 0, 'AlrmSts_Armd': 1, 'AlrmSts_Actv': 2, 'AlrmSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 331
        byte = 41
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class BoostPwrMax:
        sig_name = "BoostPwrMax"
        sig_start_bit = 231
        update_id_bit = 237
        sig_length = 10
        sig_value_factor = 0.5
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 1023
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 231
        bmuws_info = [(28, 0b11111111, 0b00000000, 8, 0), (29, 0b11000000, 0b00111111, 2, 6)]

    class ReMotInfoIPhaAlrmSt:
        sig_name = "ReMotInfoIPhaAlrmSt"
        sig_start_bit = 325
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSts_Disarmd': 0, 'AlrmSts_Armd': 1, 'AlrmSts_Actv': 2, 'AlrmSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 325
        byte = 40
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class ReMotCoolgReq:
        sig_name = "ReMotCoolgReq"
        sig_start_bit = 236
        update_id_bit = 235
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
        startbit = 236
        byte = 29
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class ReMotCooltFlowReq:
        sig_name = "ReMotCooltFlowReq"
        sig_start_bit = 234
        update_id_bit = 241
        sig_length = 9
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 500
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 234
        bmuws_info = [(29, 0b00000111, 0b11111000, 3, 0), (30, 0b11111100, 0b00000011, 6, 2)]

    class BoostChrgVCfm:
        sig_name = "BoostChrgVCfm"
        sig_start_bit = 7
        update_id_bit = 4
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BoostChrgVCfm1_Default': 0, 'BoostChrgVCfm1_loEffBoostChrgRng': 1, 'BoostChrgVCfm1_HiEffBoostChrgRng': 2, 'BoostChrgVCfm1_DCChrgRng': 3, 'BoostChrgVCfm1_Reserved1': 4, 'BoostChrgVCfm1_Reserved2': 5, 'BoostChrgVCfm1_Reserved3': 6, 'BoostChrgVCfm1_Reserved4': 7}
        compute_method = None
        length = 3
        startbit = 7
        byte = 0
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class BoostUDCLv1:
        sig_name = "BoostUDCLv1"
        sig_start_bit = 215
        update_id_bit = 137
        sig_length = 16
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 65535
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 215
        bmuws_info = [(26, 0b11111111, 0b00000000, 8, 0), (27, 0b11111111, 0b00000000, 8, 0)]

    class ReMotInfoRatTypeInfo:
        sig_name = "ReMotInfoRatTypeInfo"
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

    class ReMotInfoBoostAlrmSt:
        sig_name = "ReMotInfoBoostAlrmSt"
        sig_start_bit = 315
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSts_Disarmd': 0, 'AlrmSts_Armd': 1, 'AlrmSts_Actv': 2, 'AlrmSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 315
        byte = 39
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class BoostFcnResvSigGrpDevelpSignalGroup5:
        sig_name = "BoostFcnResvSigGrpDevelpSignalGroup5"
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

    class ReMotHeatgPwrAct:
        sig_name = "ReMotHeatgPwrAct"
        sig_start_bit = 294
        update_id_bit = 301
        sig_length = 9
        sig_value_factor = 10
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 294
        bmuws_info = [(36, 0b01111111, 0b10000000, 7, 0), (37, 0b11000000, 0b00111111, 2, 6)]

    class ReMotInfoEMQnty:
        sig_name = "ReMotInfoEMQnty"
        sig_start_bit = 339
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
        startbit = 339
        byte = 42
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class BoostLvRlySts:
        sig_name = "BoostLvRlySts"
        sig_start_bit = 3
        update_id_bit = 0
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BoostLvRlySts1_Default': 0, 'BoostLvRlySts1_Open': 1, 'BoostLvRlySts1_Close': 2, 'BoostLvRlySts1_StuckOpen': 3, 'BoostLvRlySts1_StuckClose': 4, 'BoostLvRlySts1_Undefined': 5, 'BoostLvRlySts1_Reserved1': 6, 'BoostLvRlySts1_Reserved2': 7}
        compute_method = None
        length = 3
        startbit = 3
        byte = 0
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class ReMotCooltT:
        sig_name = "ReMotCooltT"
        sig_start_bit = 255
        update_id_bit = 258
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = -256.0
        sig_value_min = 0
        sig_value_max = 5119
        sig_byteorder = "Motorola"
        sig_value_init = 2560
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 255
        bmuws_info = [(31, 0b11111111, 0b00000000, 8, 0), (32, 0b11111000, 0b00000111, 5, 3)]

    class WhlMotPlsIMax:
        sig_name = "WhlMotPlsIMax"
        sig_start_bit = 473
        update_id_bit = 493
        sig_length = 12
        sig_value_factor = 1
        sig_value_offset = -2000.0
        sig_value_min = 0
        sig_value_max = 4000
        sig_byteorder = "Motorola"
        sig_value_init = 2000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 473
        bmuws_info = [(59, 0b00000011, 0b11111100, 2, 0), (60, 0b11111111, 0b00000000, 8, 0), (61, 0b11000000, 0b00111111, 2, 6)]

    class ReMotHeatGenRate:
        sig_name = "ReMotHeatGenRate"
        sig_start_bit = 257
        update_id_bit = 276
        sig_length = 13
        sig_value_factor = 10
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 257
        bmuws_info = [(32, 0b00000011, 0b11111100, 2, 0), (33, 0b11111111, 0b00000000, 8, 0), (34, 0b11100000, 0b00011111, 3, 5)]

    class BoostFcnResvSigGrpDevelpSignalGroup2:
        sig_name = "BoostFcnResvSigGrpDevelpSignalGroup2"
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

    class BoostFcnResvSigGrp1Word1:
        sig_name = "BoostFcnResvSigGrp1Word1"
        sig_start_bit = 95
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
        startbit = 95
        bmuws_info = [(11, 0b11111111, 0b00000000, 8, 0), (12, 0b11111111, 0b00000000, 8, 0)]

    class BoostFcnResvSigGrp1Word3:
        sig_name = "BoostFcnResvSigGrp1Word3"
        sig_start_bit = 127
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
        startbit = 127
        bmuws_info = [(15, 0b11111111, 0b00000000, 8, 0), (16, 0b11111111, 0b00000000, 8, 0)]

    class WhlMotPlsFrq:
        sig_name = "WhlMotPlsFrq"
        sig_start_bit = 445
        update_id_bit = 448
        sig_length = 13
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 5000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 445
        bmuws_info = [(55, 0b00111111, 0b11000000, 6, 0), (56, 0b11111110, 0b00000001, 7, 1)]

    class ReMotInfoPasDchaAlrmSt:
        sig_name = "ReMotInfoPasDchaAlrmSt"
        sig_start_bit = 333
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSts_Disarmd': 0, 'AlrmSts_Armd': 1, 'AlrmSts_Actv': 2, 'AlrmSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 333
        byte = 41
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class BoostFcnResvSigGrpDevelpSignalGroup1:
        sig_name = "BoostFcnResvSigGrpDevelpSignalGroup1"
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

    class ReMotInfoDTCLow:
        sig_name = "ReMotInfoDTCLow"
        sig_start_bit = 383
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 383
        byte = 47
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BoostFcnResvSigGrp1Word2:
        sig_name = "BoostFcnResvSigGrp1Word2"
        sig_start_bit = 111
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
        startbit = 111
        bmuws_info = [(13, 0b11111111, 0b00000000, 8, 0), (14, 0b11111111, 0b00000000, 8, 0)]

    class BoostUDCHv1:
        sig_name = "BoostUDCHv1"
        sig_start_bit = 199
        update_id_bit = 138
        sig_length = 16
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 65535
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 199
        bmuws_info = [(24, 0b11111111, 0b00000000, 8, 0), (25, 0b11111111, 0b00000000, 8, 0)]

    class ReMotHeatgFb_UB:
        sig_name = "ReMotHeatgFb_UB"
        sig_start_bit = 295
        update_id_bit = 295
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
        startbit = 295
        byte = 36
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ReMotInfoRslAlrmSt:
        sig_name = "ReMotInfoRslAlrmSt"
        sig_start_bit = 329
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSts_Disarmd': 0, 'AlrmSts_Armd': 1, 'AlrmSts_Actv': 2, 'AlrmSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 329
        byte = 41
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class ReMotInfoActvDchaAlrmSt:
        sig_name = "ReMotInfoActvDchaAlrmSt"
        sig_start_bit = 319
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSts_Disarmd': 0, 'AlrmSts_Armd': 1, 'AlrmSts_Actv': 2, 'AlrmSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 319
        byte = 39
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class BoostFcnResvSigGrpDevelpSignalGroup3:
        sig_name = "BoostFcnResvSigGrpDevelpSignalGroup3"
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

    class ReMotInfoActvHeatgAlrmSt:
        sig_name = "ReMotInfoActvHeatgAlrmSt"
        sig_start_bit = 317
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSts_Disarmd': 0, 'AlrmSts_Armd': 1, 'AlrmSts_Actv': 2, 'AlrmSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 317
        byte = 39
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class ReMotInfoOverSpdAlrmSt:
        sig_name = "ReMotInfoOverSpdAlrmSt"
        sig_start_bit = 335
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSts_Disarmd': 0, 'AlrmSts_Armd': 1, 'AlrmSts_Actv': 2, 'AlrmSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 335
        byte = 41
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class ReMotInfoDTCSts:
        sig_name = "ReMotInfoDTCSts"
        sig_start_bit = 391
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 391
        byte = 48
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ReMotHeatgFbPwrAvl:
        sig_name = "ReMotHeatgFbPwrAvl"
        sig_start_bit = 272
        update_id_bit = None
        sig_length = 9
        sig_value_factor = 10
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 272
        bmuws_info = [(34, 0b00000001, 0b11111110, 1, 0), (35, 0b11111111, 0b00000000, 8, 0)]

    class ReMotOilT:
        sig_name = "ReMotOilT"
        sig_start_bit = 427
        update_id_bit = 446
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = -256.0
        sig_value_min = 0
        sig_value_max = 5119
        sig_byteorder = "Motorola"
        sig_value_init = 2560
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 427
        bmuws_info = [(53, 0b00001111, 0b11110000, 4, 0), (54, 0b11111111, 0b00000000, 8, 0), (55, 0b10000000, 0b01111111, 1, 7)]

    class ReMotInfoEMSeqNr:
        sig_name = "ReMotInfoEMSeqNr"
        sig_start_bit = 351
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
        startbit = 351
        byte = 43
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class BoostIDCLvMaxLim1:
        sig_name = "BoostIDCLvMaxLim1"
        sig_start_bit = 183
        update_id_bit = 139
        sig_length = 16
        sig_value_factor = 0.1
        sig_value_offset = -3000.0
        sig_value_min = 0
        sig_value_max = 65535
        sig_byteorder = "Motorola"
        sig_value_init = 30000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 183
        bmuws_info = [(22, 0b11111111, 0b00000000, 8, 0), (23, 0b11111111, 0b00000000, 8, 0)]

    class WhlMotPlsI:
        sig_name = "WhlMotPlsI"
        sig_start_bit = 463
        update_id_bit = 469
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 463
        bmuws_info = [(57, 0b11111111, 0b00000000, 8, 0), (58, 0b11000000, 0b00111111, 2, 6)]

    class ReMotInfoDTCLMid:
        sig_name = "ReMotInfoDTCLMid"
        sig_start_bit = 375
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 375
        byte = 46
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BoostFcnResvSigGrp_UB:
        sig_name = "BoostFcnResvSigGrp_UB"
        sig_start_bit = 143
        update_id_bit = 143
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
        startbit = 143
        byte = 17
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class WhlMotPlsHeatgFltSts:
        sig_name = "WhlMotPlsHeatgFltSts"
        sig_start_bit = 399
        update_id_bit = 395
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WhlMotPlsHeatgFltSts_NoErr': 0, 'WhlMotPlsHeatgFltSts_Err': 1, 'WhlMotPlsHeatgFltSts_Reserve1': 2, 'WhlMotPlsHeatgFltSts_Reserve2': 3}
        compute_method = None
        length = 2
        startbit = 399
        byte = 49
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class BoostFcnResvSigGrp1Word0:
        sig_name = "BoostFcnResvSigGrp1Word0"
        sig_start_bit = 79
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
        startbit = 79
        bmuws_info = [(9, 0b11111111, 0b00000000, 8, 0), (10, 0b11111111, 0b00000000, 8, 0)]

    class ReMotInvrT:
        sig_name = "ReMotInvrT"
        sig_start_bit = 407
        update_id_bit = 410
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = -256.0
        sig_value_min = 0
        sig_value_max = 5119
        sig_byteorder = "Motorola"
        sig_value_init = 2560
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 407
        bmuws_info = [(50, 0b11111111, 0b00000000, 8, 0), (51, 0b11111000, 0b00000111, 5, 3)]

    class BoostFcnResvSigGrp1_UB:
        sig_name = "BoostFcnResvSigGrp1_UB"
        sig_start_bit = 142
        update_id_bit = 142
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
        startbit = 142
        byte = 17
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class ReMotInfoInvrtTAlrmSt:
        sig_name = "ReMotInfoInvrtTAlrmSt"
        sig_start_bit = 327
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSts_Disarmd': 0, 'AlrmSts_Armd': 1, 'AlrmSts_Actv': 2, 'AlrmSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 327
        byte = 40
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class ReMotInfoTqAlrmSt:
        sig_name = "ReMotInfoTqAlrmSt"
        sig_start_bit = 343
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSts_Disarmd': 0, 'AlrmSts_Armd': 1, 'AlrmSts_Actv': 2, 'AlrmSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 343
        byte = 42
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class ReMotInfoDTCHig:
        sig_name = "ReMotInfoDTCHig"
        sig_start_bit = 367
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 367
        byte = 45
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class WhlMotPlsHeatgSts:
        sig_name = "WhlMotPlsHeatgSts"
        sig_start_bit = 397
        update_id_bit = 394
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WhlMotPlsHeatgSts_Idle': 0, 'WhlMotPlsHeatgSts_HeatgFullpwr': 1, 'WhlMotPlsHeatgSts_Heatg': 2, 'WhlMotPlsHeatgSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 397
        byte = 49
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class BoostIDCHv1:
        sig_name = "BoostIDCHv1"
        sig_start_bit = 151
        update_id_bit = 141
        sig_length = 16
        sig_value_factor = 0.1
        sig_value_offset = -3000.0
        sig_value_min = 0
        sig_value_max = 65535
        sig_byteorder = "Motorola"
        sig_value_init = 30000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 151
        bmuws_info = [(18, 0b11111111, 0b00000000, 8, 0), (19, 0b11111111, 0b00000000, 8, 0)]

    class BoostFcnResvSigGrpDevelpSignalGroup8:
        sig_name = "BoostFcnResvSigGrpDevelpSignalGroup8"
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

    class ReMotInfoMotTAlrmSt:
        sig_name = "ReMotInfoMotTAlrmSt"
        sig_start_bit = 323
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSts_Disarmd': 0, 'AlrmSts_Armd': 1, 'AlrmSts_Actv': 2, 'AlrmSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 323
        byte = 40
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class ReMotInfoFltAlrmSt:
        sig_name = "ReMotInfoFltAlrmSt"
        sig_start_bit = 313
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSts_Disarmd': 0, 'AlrmSts_Armd': 1, 'AlrmSts_Actv': 2, 'AlrmSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 313
        byte = 39
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class BoostFcnResvSigGrpDevelpSignalGroup4:
        sig_name = "BoostFcnResvSigGrpDevelpSignalGroup4"
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

    class ReMotInfoModStRms:
        sig_name = "ReMotInfoModStRms"
        sig_start_bit = 347
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 3
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ModStatusRms_Invalid': 0, 'ModStatusRms_PwrCns': 1, 'ModStatusRms_PwrGen': 2, 'ModStatusRms_OffSts': 3, 'ModStatusRms_RdySts': 4, 'ModStatusRms_Abnormal': 5, 'ModStatusRms_Invalid1': 6, 'ModStatusRms_Invalid2': 7, 'ModStatusRms_Invalid3': 8, 'ModStatusRms_Invalid4': 9, 'ModStatusRms_Invalid5': 10, 'ModStatusRms_Invalid6': 11, 'ModStatusRms_Invalid7': 12, 'ModStatusRms_Invalid8': 13, 'ModStatusRms_Invalid9': 14, 'ModStatusRms_Invalid10': 15}
        compute_method = None
        length = 4
        startbit = 347
        byte = 43
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class ReMotInfo_UB:
        sig_name = "ReMotInfo_UB"
        sig_start_bit = 352
        update_id_bit = 352
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
        startbit = 352
        byte = 44
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ReMotHeatgFbMotSts:
        sig_name = "ReMotHeatgFbMotSts"
        sig_start_bit = 275
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 6
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'MotHeatgSts_Ini': 0, 'MotHeatgSts_Standby': 1, 'MotHeatgSts_Heatg': 2, 'MotHeatgSts_ElecErr': 3, 'MotHeatgSts_OvrTemp': 4, 'MotHeatgSts_PwrLim': 5, 'MotHeatgSts_Reserved1': 6}
        compute_method = None
        length = 3
        startbit = 275
        byte = 34
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class ReMotInfoUDCAlrmSt:
        sig_name = "ReMotInfoUDCAlrmSt"
        sig_start_bit = 341
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSts_Disarmd': 0, 'AlrmSts_Armd': 1, 'AlrmSts_Actv': 2, 'AlrmSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 341
        byte = 42
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class BoostIDCLv1:
        sig_name = "BoostIDCLv1"
        sig_start_bit = 167
        update_id_bit = 140
        sig_length = 16
        sig_value_factor = 0.1
        sig_value_offset = -3000.0
        sig_value_min = 0
        sig_value_max = 65535
        sig_byteorder = "Motorola"
        sig_value_init = 30000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 167
        bmuws_info = [(20, 0b11111111, 0b00000000, 8, 0), (21, 0b11111111, 0b00000000, 8, 0)]

    class ReMotInfoOilTAlrmSt:
        sig_name = "ReMotInfoOilTAlrmSt"
        sig_start_bit = 321
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSts_Disarmd': 0, 'AlrmSts_Armd': 1, 'AlrmSts_Actv': 2, 'AlrmSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 321
        byte = 40
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class WhlMotPlsIAvl:
        sig_name = "WhlMotPlsIAvl"
        sig_start_bit = 468
        update_id_bit = 474
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 468
        bmuws_info = [(58, 0b00011111, 0b11100000, 5, 0), (59, 0b11111000, 0b00000111, 5, 3)]

    class ReMotMotT:
        sig_name = "ReMotMotT"
        sig_start_bit = 409
        update_id_bit = 428
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = -256.0
        sig_value_min = 0
        sig_value_max = 5119
        sig_byteorder = "Motorola"
        sig_value_init = 2560
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 409
        bmuws_info = [(51, 0b00000011, 0b11111100, 2, 0), (52, 0b11111111, 0b00000000, 8, 0), (53, 0b11100000, 0b00011111, 3, 5)]


class VCUPropulsionCANFDFr03:
    msg_name = "VCUPropulsionCANFDFr03"
    msg_id = 136
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 64
    tx_node = "VCU"
    rx_nodes = ['CCUMCUCD', 'ODP', 'EGSM', 'IEM', 'BECM', 'CCUMCUAD', 'BCU1']
    sig_group_dict = {'AccrPedlCmplPsd': ['AccrPedlCmplPsdChks', 'AccrPedlCmplPsdCmplPsd', 'AccrPedlCmplPsdCntr', 'AccrPedlCmplPsdSts'], 'TrsmParkLockSts': ['TrsmParkLockStsChks', 'TrsmParkLockStsCntr', 'TrsmParkLockStsTrsmParkLockSt'], 'DecelOvrdByDrvrAccel': ['DecelOvrdByDrvrAccelChks', 'DecelOvrdByDrvrAccelCntr', 'DecelOvrdByDrvrAccelOvrdDecelByDrvr']}
    sig_group_dataid_dict = {'TrsmParkLockSts': 1001}

    class IntllntChrgnAllwd:
        sig_name = "IntllntChrgnAllwd"
        sig_start_bit = 73
        update_id_bit = 119
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AllwdorNot_Init': 0, 'AllwdorNot_NotAllwd': 1, 'AllwdorNot_Allwd': 2, 'AllwdorNot_Resd1': 3}
        compute_method = None
        length = 2
        startbit = 73
        byte = 9
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class TrsmParkLockStsTrsmParkLockSt:
        sig_name = "TrsmParkLockStsTrsmParkLockSt"
        sig_start_bit = 99
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 3
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TrsmParkLock_ParkNotEngd': 0, 'TrsmParkLock_ParkEngd': 1, 'TrsmParkLock_NotInUse': 2, 'TrsmParkLock_Undefd': 3}
        compute_method = None
        length = 2
        startbit = 99
        byte = 12
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class FastBoostRlyReq:
        sig_name = "FastBoostRlyReq"
        sig_start_bit = 114
        update_id_bit = 8
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'QCRlySt_Open': 0, 'QCRlySt_Closed': 1, 'QCRlySt_StuckOpen': 2, 'QCRlySt_StuckClosed': 3, 'QCRlySt_Reserved1': 4, 'QCRlySt_Reserved2': 5, 'QCRlySt_Reserved3': 6, 'QCRlySt_Reserved4': 7}
        compute_method = None
        length = 3
        startbit = 114
        byte = 14
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class HVBattChrgnCCOrCVMod:
        sig_name = "HVBattChrgnCCOrCVMod"
        sig_start_bit = 69
        update_id_bit = 109
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CCOrCVModSt_Default': 0, 'CCOrCVModSt_CV': 1, 'CCOrCVModSt_CC': 2, 'CCOrCVModSt_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 69
        byte = 8
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class DecelOvrdByDrvrAccelChks:
        sig_name = "DecelOvrdByDrvrAccelChks"
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

    class OwnBrandChrgrFlg:
        sig_name = "OwnBrandChrgrFlg"
        sig_start_bit = 83
        update_id_bit = 116
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffCrit1_NotVld1': 0, 'OnOffCrit1_Off': 1, 'OnOffCrit1_On': 2, 'OnOffCrit1_NotVld2': 3}
        compute_method = None
        length = 2
        startbit = 83
        byte = 10
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class HVCmprInhb:
        sig_name = "HVCmprInhb"
        sig_start_bit = 77
        update_id_bit = 105
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffCrit1_NotVld1': 0, 'OnOffCrit1_Off': 1, 'OnOffCrit1_On': 2, 'OnOffCrit1_NotVld2': 3}
        compute_method = None
        length = 2
        startbit = 77
        byte = 9
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class HVChrgnStopReq:
        sig_name = "HVChrgnStopReq"
        sig_start_bit = 79
        update_id_bit = 106
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HVChrgnStopReq_Default': 0, 'HVChrgnStopReq_BST': 1, 'HVChrgnStopReq_CST': 2, 'HVChrgnStopReq_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 79
        byte = 9
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HVAirHeatrInhb:
        sig_name = "HVAirHeatrInhb"
        sig_start_bit = 71
        update_id_bit = 110
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffCrit1_NotVld1': 0, 'OnOffCrit1_Off': 1, 'OnOffCrit1_On': 2, 'OnOffCrit1_NotVld2': 3}
        compute_method = None
        length = 2
        startbit = 71
        byte = 8
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class AccrPedlCmplPsdCntr:
        sig_name = "AccrPedlCmplPsdCntr"
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

    class AccrPedlCmplPsd_UB:
        sig_name = "AccrPedlCmplPsd_UB"
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

    class AccrPedlCmplPsdChks:
        sig_name = "AccrPedlCmplPsdChks"
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

    class AccrPedlCmplPsdSts:
        sig_name = "AccrPedlCmplPsdSts"
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

    class DCChrgModReq:
        sig_name = "DCChrgModReq"
        sig_start_bit = 23
        update_id_bit = 27
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DCChrgModReq_Default': 0, 'DCChrgModReq_CC': 1, 'DCChrgModReq_CV': 2, 'DCChrgModReq_Reserved1': 3, 'DCChrgModReq_Reserved2': 4, 'DCChrgModReq_Reserved3': 5, 'DCChrgModReq_Reserved4': 6, 'DCChrgModReq_Reserved5': 7}
        compute_method = None
        length = 3
        startbit = 23
        byte = 2
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DecelOvrdByDrvrAccelOvrdDecelByDrvr:
        sig_name = "DecelOvrdByDrvrAccelOvrdDecelByDrvr"
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
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 43
        byte = 5
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class DCChrgnSts:
        sig_name = "DCChrgnSts"
        sig_start_bit = 31
        update_id_bit = 26
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ChrgrSts_Idle': 0, 'ChrgrSts_Prestart': 1, 'ChrgrSts_Charging': 2, 'ChrgrSts_DCChrgnFltVehSide': 3, 'ChrgrSts_DCChrgnFltChrgrSideTempFlt': 4, 'ChrgrSts_DCChrgnFltChrgrSideConnectFlt': 5, 'ChrgrSts_DCChrgnFltChrgrSideOtherFlt': 6, 'ChrgrSts_DCChrgnFltChrgrSideEmgyFlt': 7, 'ChrgrSts_DCChrgnFltChrgrSideComFlt': 8, 'ChrgrSts_Bookcharging': 9, 'ChrgrSts_Shuntdown': 10, 'ChrgrSts_Heating': 11, 'ChrgrSts_Supercharging': 12, 'ChrgrSts_SuperchargingEnd': 13, 'ChrgrSts_Reserved1': 14, 'ChrgrSts_Reserved2': 15}
        compute_method = None
        length = 4
        startbit = 31
        byte = 3
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class HVBattQCNRlyReq:
        sig_name = "HVBattQCNRlyReq"
        sig_start_bit = 127
        update_id_bit = 108
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'QCRlySt_Open': 0, 'QCRlySt_Closed': 1, 'QCRlySt_StuckOpen': 2, 'QCRlySt_StuckClosed': 3, 'QCRlySt_Reserved1': 4, 'QCRlySt_Reserved2': 5, 'QCRlySt_Reserved3': 6, 'QCRlySt_Reserved4': 7}
        compute_method = None
        length = 3
        startbit = 127
        byte = 15
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class TrsmParkLockStsChks:
        sig_name = "TrsmParkLockStsChks"
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

    class AccrPedlCmplPsdCmplPsd:
        sig_name = "AccrPedlCmplPsdCmplPsd"
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
        sig_value_table = {'NotCmpl1_NotCmpl': 0, 'NotCmpl1_Cmpl': 1}
        compute_method = None
        length = 1
        startbit = 11
        byte = 1
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class PrpsnSysActvCmpl:
        sig_name = "PrpsnSysActvCmpl"
        sig_start_bit = 81
        update_id_bit = 115
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OffOnInvld_Invalid1': 0, 'OffOnInvld_Off': 1, 'OffOnInvld_On': 2, 'OffOnInvld_Invalid2': 3}
        compute_method = None
        length = 2
        startbit = 81
        byte = 10
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class ElecGearShiftLiOnReq:
        sig_name = "ElecGearShiftLiOnReq"
        sig_start_bit = 53
        update_id_bit = 40
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ReqSts2_Default': 0, 'ReqSts2_NotReqd': 1, 'ReqSts2_Reqd': 2, 'ReqSts2_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 53
        byte = 6
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class EgyRgnLimFlg:
        sig_name = "EgyRgnLimFlg"
        sig_start_bit = 55
        update_id_bit = 41
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OffOnNoCmd_NoCmd': 0, 'OffOnNoCmd_Off': 1, 'OffOnNoCmd_On': 2}
        compute_method = None
        length = 2
        startbit = 55
        byte = 6
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HVCooltHeatrInhb:
        sig_name = "HVCooltHeatrInhb"
        sig_start_bit = 75
        update_id_bit = 104
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffCrit1_NotVld1': 0, 'OnOffCrit1_Off': 1, 'OnOffCrit1_On': 2, 'OnOffCrit1_NotVld2': 3}
        compute_method = None
        length = 2
        startbit = 75
        byte = 9
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class DecelOvrdByDrvrAccelCntr:
        sig_name = "DecelOvrdByDrvrAccelCntr"
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

    class TrsmParkLockSts_UB:
        sig_name = "TrsmParkLockSts_UB"
        sig_start_bit = 97
        update_id_bit = 97
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
        startbit = 97
        byte = 12
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class OnBdChrgrPwrEnaAllwd:
        sig_name = "OnBdChrgrPwrEnaAllwd"
        sig_start_bit = 96
        update_id_bit = 118
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
        startbit = 96
        byte = 12
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class HMIHvBattSOC:
        sig_name = "HMIHvBattSOC"
        sig_start_bit = 49
        update_id_bit = 111
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1020
        sig_byteorder = "Motorola"
        sig_value_init = 1020
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 49
        bmuws_info = [(6, 0b00000011, 0b11111100, 2, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class HVBattQCPRlyReq:
        sig_name = "HVBattQCPRlyReq"
        sig_start_bit = 67
        update_id_bit = 107
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'QCRlySt_Open': 0, 'QCRlySt_Closed': 1, 'QCRlySt_StuckOpen': 2, 'QCRlySt_StuckClosed': 3, 'QCRlySt_Reserved1': 4, 'QCRlySt_Reserved2': 5, 'QCRlySt_Reserved3': 6, 'QCRlySt_Reserved4': 7}
        compute_method = None
        length = 3
        startbit = 67
        byte = 8
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class OnBdChrgrSt:
        sig_name = "OnBdChrgrSt"
        sig_start_bit = 87
        update_id_bit = 117
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ChrgrSts1_Idle': 0, 'ChrgrSts1_PreStrt': 1, 'ChrgrSts1_Chrgn': 2, 'ChrgrSts1_Alrm': 3, 'ChrgrSts1_Srv': 4, 'ChrgrSts1_Diagc': 5, 'ChrgrSts1_Boot': 6, 'ChrgrSts1_Rstrt': 7, 'ChrgrSts1_DisChrgn': 8, 'ChrgrSts1_BookChrgn': 9, 'ChrgrSts1_Shutdown': 10, 'ChrgrSts1_Heating': 11, 'ChrgrSts1_Cooling': 12, 'ChrgrSts1_Reserved1': 13, 'ChrgrSts1_Reserved2': 14, 'ChrgrSts1_Reserved3': 15}
        compute_method = None
        length = 4
        startbit = 87
        byte = 10
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DcDcActvReq:
        sig_name = "DcDcActvReq"
        sig_start_bit = 17
        update_id_bit = 24
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ReqSts2_Default': 0, 'ReqSts2_NotReqd': 1, 'ReqSts2_Reqd': 2, 'ReqSts2_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 17
        byte = 2
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class DCChrgrHndlSts:
        sig_name = "DCChrgrHndlSts"
        sig_start_bit = 20
        update_id_bit = 25
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 4
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ChrgrHndlSt_Disconnected': 0, 'ChrgrHndlSt_ConnectedWithoutPower': 1, 'ChrgrHndlSt_PowerAvailableButNotActivated': 2, 'ChrgrHndlSt_ConnectedWithPower': 3, 'ChrgrHndlSt_Init': 4, 'ChrgrHndlSt_Fault': 5, 'ChrgrHndlSt_Reserved1': 6, 'ChrgrHndlSt_Reserved2': 7}
        compute_method = None
        length = 3
        startbit = 20
        byte = 2
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class DecelOvrdByDrvrAccel_UB:
        sig_name = "DecelOvrdByDrvrAccel_UB"
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

    class TrsmParkLockStsCntr:
        sig_name = "TrsmParkLockStsCntr"
        sig_start_bit = 103
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
        startbit = 103
        byte = 12
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4


class CCUMCUCDPropulsionCANFDFr07:
    msg_name = "CCUMCUCDPropulsionCANFDFr07"
    msg_id = 610
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 64
    tx_node = "CCUMCUCD"
    rx_nodes = ['VCU', 'ETC', 'SRS', 'ODP', 'MGM', 'EGSM', 'IEM', 'BECM', 'BCU2', 'CCUMCUAD', 'BCU1']
    sig_group_dict = {'HVBattThermReqActual': ['HVBattThermReqActualCellTTar', 'HVBattThermReqActualCellTType', 'HVBattThermReqActualCooltFlwReq', 'HVBattThermReqActualCooltTReq', 'HVBattThermReqActualSourceID', 'HVBattThermReqActualThermLvlReq', 'HVBattThermReqActualThermReq'], 'CooltTSnsrT2Estimd': ['CooltTSnsrT2EstimdDataQly', 'CooltTSnsrT2EstimdT'], 'SeatOccpSts': ['SeatOccpStsDrvrSeatSts', 'SeatOccpStsPassSeatSts', 'SeatOccpStsSecRowLeSeatSts', 'SeatOccpStsSecRowMidSeatSts', 'SeatOccpStsSecRowRiSeatSts', 'SeatOccpStsThrdRowLeSeatSts', 'SeatOccpStsThrdRowMidSeatSts', 'SeatOccpStsThrdRowRiSeatSts'], 'CooltCircFlwEstimd': ['CooltCircFlwEstimdHeatrCirc', 'CooltCircFlwEstimdHvBattCirc', 'CooltCircFlwEstimdPWTCirc'], 'RearRightTyreAlarmInfo': ['RearRightTyreAlarmInfoBattLowWarnFlag', 'RearRightTyreAlarmInfoFastLoseWarnFlag', 'RearRightTyreAlarmInfoPWarnFlag', 'RearRightTyreAlarmInfoSysWarnFlag', 'RearRightTyreAlarmInfoTWarnFlag'], 'FrontLeftTyreAlarmInfo': ['FrontLeftTyreAlarmInfoBattLowWarnFlag', 'FrontLeftTyreAlarmInfoFastLoseWarnFlag', 'FrontLeftTyreAlarmInfoPWarnFlag', 'FrontLeftTyreAlarmInfoSysWarnFlag', 'FrontLeftTyreAlarmInfoTWarnFlag'], 'CooltTSnsrT4Estimd': ['CooltTSnsrT4EstimdDataQly', 'CooltTSnsrT4EstimdT'], 'FrontRightTyreAlarmInfo': ['FrontRightTyreAlarmInfoBattLowWarnFlag', 'FrontRightTyreAlarmInfoFastLoseWarnFlag', 'FrontRightTyreAlarmInfoPWarnFlag', 'FrontRightTyreAlarmInfoSysWarnFlag', 'FrontRightTyreAlarmInfoTWarnFlag'], 'HVBattThermReqFromSrv': ['HVBattThermReqFromSrvCellTTar', 'HVBattThermReqFromSrvCellTType', 'HVBattThermReqFromSrvCooltFlwReq', 'HVBattThermReqFromSrvCooltTReq', 'HVBattThermReqFromSrvSourceID', 'HVBattThermReqFromSrvThermLvlReq', 'HVBattThermReqFromSrvThermReq'], 'CooltTSnsrT3Estimd': ['CooltTSnsrT3EstimdDataQly', 'CooltTSnsrT3EstimdT'], 'CmptmtTSpHdLvlTarT': ['CmptmtTSpHdLvlTarTFrntLe', 'CmptmtTSpHdLvlTarTFrntRi', 'CmptmtTSpHdLvlTarTReLe', 'CmptmtTSpHdLvlTarTReRi'], 'RearLeftTyreAlarmInfo': ['RearLeftTyreAlarmInfoBattLowWarnFlag', 'RearLeftTyreAlarmInfoFastLoseWarnFlag', 'RearLeftTyreAlarmInfoPWarnFlag', 'RearLeftTyreAlarmInfoSysWarnFlag', 'RearLeftTyreAlarmInfoTWarnFlag'], 'CooltTSnsrT1Estimd': ['CooltTSnsrT1EstimdDataQly', 'CooltTSnsrT1EstimdT'], 'AmbTEstimd': ['AmbTEstimdT', 'AmbTEstimdTQF']}
    sig_group_dataid_dict = {}

    class CmptmtTSpHdLvlTarTFrntRi:
        sig_name = "CmptmtTSpHdLvlTarTFrntRi"
        sig_start_bit = 58
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = -256.0
        sig_value_min = 0
        sig_value_max = 5119
        sig_byteorder = "Motorola"
        sig_value_init = 2560
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 58
        bmuws_info = [(7, 0b00000111, 0b11111000, 3, 0), (8, 0b11111111, 0b00000000, 8, 0), (9, 0b11000000, 0b00111111, 2, 6)]

    class FrontRightTyreAlarmInfoSysWarnFlag:
        sig_name = "FrontRightTyreAlarmInfoSysWarnFlag"
        sig_start_bit = 243
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SysWarnFlag_Nromal': 0, 'SysWarnFlag_Warning': 1}
        compute_method = None
        length = 1
        startbit = 243
        byte = 30
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class HVBattThermReqActualCooltTReq:
        sig_name = "HVBattThermReqActualCooltTReq"
        sig_start_bit = 331
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
        startbit = 331
        bmuws_info = [(41, 0b00001111, 0b11110000, 4, 0), (42, 0b11111110, 0b00000001, 7, 1)]

    class SeatOccpStsSecRowLeSeatSts:
        sig_name = "SeatOccpStsSecRowLeSeatSts"
        sig_start_bit = 445
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
        startbit = 445
        byte = 55
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class MotHeatgReq:
        sig_name = "MotHeatgReq"
        sig_start_bit = 415
        update_id_bit = 414
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
        startbit = 415
        byte = 51
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class CooltTSnsrT2EstimdT:
        sig_name = "CooltTSnsrT2EstimdT"
        sig_start_bit = 157
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = -256.0
        sig_value_min = 0
        sig_value_max = 5119
        sig_byteorder = "Motorola"
        sig_value_init = 2560
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 157
        bmuws_info = [(19, 0b00111111, 0b11000000, 6, 0), (20, 0b11111110, 0b00000001, 7, 1)]

    class SeatOccpStsPassSeatSts:
        sig_name = "SeatOccpStsPassSeatSts"
        sig_start_bit = 446
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
        startbit = 446
        byte = 55
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class RearRightTyreAlarmInfoTWarnFlag:
        sig_name = "RearRightTyreAlarmInfoTWarnFlag"
        sig_start_bit = 434
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TWarnFlag_Nromal': 0, 'TWarnFlag_HighTWarn': 1, 'TWarnFlag_Reserve1': 2, 'TWarnFlag_Reserve2': 3}
        compute_method = None
        length = 2
        startbit = 434
        byte = 54
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class CooltTSnsrT2EstimdDataQly:
        sig_name = "CooltTSnsrT2EstimdDataQly"
        sig_start_bit = 159
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SnsrQly_SnsrNotOk': 0, 'SnsrQly_SnsrOk': 1}
        compute_method = None
        length = 2
        startbit = 159
        byte = 19
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class FrontLeftTyreAlarmInfoFastLoseWarnFlag:
        sig_name = "FrontLeftTyreAlarmInfoFastLoseWarnFlag"
        sig_start_bit = 238
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FastLoseWarnFlag_Normal': 0, 'FastLoseWarnFlag_Warning': 1}
        compute_method = None
        length = 1
        startbit = 238
        byte = 29
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class PlsHeatgReq:
        sig_name = "PlsHeatgReq"
        sig_start_bit = 413
        update_id_bit = 412
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
        startbit = 413
        byte = 51
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class RearLeftTyreAlarmInfoPWarnFlag:
        sig_name = "RearLeftTyreAlarmInfoPWarnFlag"
        sig_start_bit = 429
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PWarnFlag_Normal': 0, 'PWarnFlag_LowPWarn': 1, 'PWarnFlag_Reserve1': 2, 'PWarnFlag_Reserve2': 3}
        compute_method = None
        length = 2
        startbit = 429
        byte = 53
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class HVBattThermReqActualThermReq:
        sig_name = "HVBattThermReqActualThermReq"
        sig_start_bit = 346
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HVBattThermReq_Idle': 0, 'HVBattThermReq_ThermalBalancing': 1, 'HVBattThermReq_PassiveHeating': 2, 'HVBattThermReq_ActiveHeating': 3, 'HVBattThermReq_PassiveCooling': 4, 'HVBattThermReq_ActiveCooling': 5, 'HVBattThermReq_CombinedCooling': 6, 'HVBattThermReq_Reserved': 7}
        compute_method = None
        length = 3
        startbit = 346
        byte = 43
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class CooltTSnsrT4EstimdT:
        sig_name = "CooltTSnsrT4EstimdT"
        sig_start_bit = 189
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = -256.0
        sig_value_min = 0
        sig_value_max = 5119
        sig_byteorder = "Motorola"
        sig_value_init = 2560
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 189
        bmuws_info = [(23, 0b00111111, 0b11000000, 6, 0), (24, 0b11111110, 0b00000001, 7, 1)]

    class HVBattThermReqActual_UB:
        sig_name = "HVBattThermReqActual_UB"
        sig_start_bit = 336
        update_id_bit = 336
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
        startbit = 336
        byte = 42
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class CooltTSnsrT1EstimdT:
        sig_name = "CooltTSnsrT1EstimdT"
        sig_start_bit = 141
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = -256.0
        sig_value_min = 0
        sig_value_max = 5119
        sig_byteorder = "Motorola"
        sig_value_init = 2560
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 141
        bmuws_info = [(17, 0b00111111, 0b11000000, 6, 0), (18, 0b11111110, 0b00000001, 7, 1)]

    class HVBattThermReqActualCellTType:
        sig_name = "HVBattThermReqActualCellTType"
        sig_start_bit = 351
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BattTemperatureType_Idle': 0, 'BattTemperatureType_Tmin': 1, 'BattTemperatureType_TAvg': 2, 'BattTemperatureType_TMax': 3}
        compute_method = None
        length = 2
        startbit = 351
        byte = 43
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class CooltTSnsrT2Estimd_UB:
        sig_name = "CooltTSnsrT2Estimd_UB"
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

    class AmbTEstimdTQF:
        sig_name = "AmbTEstimdTQF"
        sig_start_bit = 10
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HVACTempQf_SnsrDataNotOk': 0, 'HVACTempQf_SnsrDataOk': 1}
        compute_method = None
        length = 1
        startbit = 10
        byte = 1
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class RearLeftTyreAlarmInfoBattLowWarnFlag:
        sig_name = "RearLeftTyreAlarmInfoBattLowWarnFlag"
        sig_start_bit = 431
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BattLowWarnFlag_Normal': 0, 'BattLowWarnFlag_Warning': 1}
        compute_method = None
        length = 1
        startbit = 431
        byte = 53
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class HVBattThermReqFromSrvCellTTar:
        sig_name = "HVBattThermReqFromSrvCellTTar"
        sig_start_bit = 453
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
        startbit = 453
        bmuws_info = [(56, 0b00111111, 0b11000000, 6, 0), (57, 0b11111000, 0b00000111, 5, 3)]

    class CmptmtTSpHdLvlTarTReRi:
        sig_name = "CmptmtTSpHdLvlTarTReRi"
        sig_start_bit = 80
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = -256.0
        sig_value_min = 0
        sig_value_max = 5119
        sig_byteorder = "Motorola"
        sig_value_init = 2560
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 80
        bmuws_info = [(10, 0b00000001, 0b11111110, 1, 0), (11, 0b11111111, 0b00000000, 8, 0), (12, 0b11110000, 0b00001111, 4, 4)]

    class HVBattThermReqFromSrvCooltTReq:
        sig_name = "HVBattThermReqFromSrvCooltTReq"
        sig_start_bit = 465
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
        startbit = 465
        bmuws_info = [(58, 0b00000011, 0b11111100, 2, 0), (59, 0b11111111, 0b00000000, 8, 0), (60, 0b10000000, 0b01111111, 1, 7)]

    class HVBattThermReqFromSrvThermLvlReq:
        sig_name = "HVBattThermReqFromSrvThermLvlReq"
        sig_start_bit = 486
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ReqLvl_NoReq': 0, 'ReqLvl_LoReq': 1, 'ReqLvl_MidReq': 2, 'ReqLvl_HiReq': 3}
        compute_method = None
        length = 2
        startbit = 486
        byte = 60
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class PWTThermReqResp:
        sig_name = "PWTThermReqResp"
        sig_start_bit = 411
        update_id_bit = 423
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 9
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PwtThermMod_Idle': 0, 'PwtThermMod_Off': 1, 'PwtThermMod_SeparateLoopCoolg': 2, 'PwtThermMod_SeparateLoopHeatg': 3, 'PwtThermMod_OneLoopCoolg': 4, 'PwtThermMod_OneLoopHeating': 5, 'PwtThermMod_AfterRun': 6, 'PwtThermMod_SuperChrgn': 7, 'PwtThermMod_Reserved1': 8, 'PwtThermMod_Reserved2': 9}
        compute_method = None
        length = 4
        startbit = 411
        byte = 51
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class RearLeftTyreAlarmInfoFastLoseWarnFlag:
        sig_name = "RearLeftTyreAlarmInfoFastLoseWarnFlag"
        sig_start_bit = 430
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FastLoseWarnFlag_Normal': 0, 'FastLoseWarnFlag_Warning': 1}
        compute_method = None
        length = 1
        startbit = 430
        byte = 53
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class CooltTSnsrT1EstimdDataQly:
        sig_name = "CooltTSnsrT1EstimdDataQly"
        sig_start_bit = 143
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SnsrQly_SnsrNotOk': 0, 'SnsrQly_SnsrOk': 1}
        compute_method = None
        length = 2
        startbit = 143
        byte = 17
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class FrontRightTyreAlarmInfoFastLoseWarnFlag:
        sig_name = "FrontRightTyreAlarmInfoFastLoseWarnFlag"
        sig_start_bit = 246
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FastLoseWarnFlag_Normal': 0, 'FastLoseWarnFlag_Warning': 1}
        compute_method = None
        length = 1
        startbit = 246
        byte = 30
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class CmptmtTSpHdLvlTarTReLe:
        sig_name = "CmptmtTSpHdLvlTarTReLe"
        sig_start_bit = 77
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = -256.0
        sig_value_min = 0
        sig_value_max = 5119
        sig_byteorder = "Motorola"
        sig_value_init = 2560
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 77
        bmuws_info = [(9, 0b00111111, 0b11000000, 6, 0), (10, 0b11111110, 0b00000001, 7, 1)]

    class RearRightTyreAlarmInfoFastLoseWarnFlag:
        sig_name = "RearRightTyreAlarmInfoFastLoseWarnFlag"
        sig_start_bit = 438
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FastLoseWarnFlag_Normal': 0, 'FastLoseWarnFlag_Warning': 1}
        compute_method = None
        length = 1
        startbit = 438
        byte = 54
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class DCDCFltElecWarn:
        sig_name = "DCDCFltElecWarn"
        sig_start_bit = 205
        update_id_bit = 203
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flt_Initial': 0, 'Flt_NoFault': 1, 'Flt_Fault': 2}
        compute_method = None
        length = 2
        startbit = 205
        byte = 25
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class FrontLeftTyreAlarmInfoBattLowWarnFlag:
        sig_name = "FrontLeftTyreAlarmInfoBattLowWarnFlag"
        sig_start_bit = 239
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BattLowWarnFlag_Normal': 0, 'BattLowWarnFlag_Warning': 1}
        compute_method = None
        length = 1
        startbit = 239
        byte = 29
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class HvActvForVehModReq:
        sig_name = "HvActvForVehModReq"
        sig_start_bit = 255
        update_id_bit = 254
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
        startbit = 255
        byte = 31
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class HVBattThermReqActualThermLvlReq:
        sig_name = "HVBattThermReqActualThermLvlReq"
        sig_start_bit = 348
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ReqLvl_NoReq': 0, 'ReqLvl_LoReq': 1, 'ReqLvl_MidReq': 2, 'ReqLvl_HiReq': 3}
        compute_method = None
        length = 2
        startbit = 348
        byte = 43
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class HVBattThermReqActualCooltFlwReq:
        sig_name = "HVBattThermReqActualCooltFlwReq"
        sig_start_bit = 324
        update_id_bit = None
        sig_length = 9
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 500
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 324
        bmuws_info = [(40, 0b00011111, 0b11100000, 5, 0), (41, 0b11110000, 0b00001111, 4, 4)]

    class CmptmtTSpHdLvlTarTFrntLe:
        sig_name = "CmptmtTSpHdLvlTarTFrntLe"
        sig_start_bit = 55
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = -256.0
        sig_value_min = 0
        sig_value_max = 5119
        sig_byteorder = "Motorola"
        sig_value_init = 2560
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 55
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111000, 0b00000111, 5, 3)]

    class HVBattCoolgPwrDes:
        sig_name = "HVBattCoolgPwrDes"
        sig_start_bit = 253
        update_id_bit = 256
        sig_length = 13
        sig_value_factor = 10
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 253
        bmuws_info = [(31, 0b00111111, 0b11000000, 6, 0), (32, 0b11111110, 0b00000001, 7, 1)]

    class HVBattThermReqActualSourceID:
        sig_name = "HVBattThermReqActualSourceID"
        sig_start_bit = 359
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
        startbit = 359
        bmuws_info = [(44, 0b11111111, 0b00000000, 8, 0), (45, 0b11111111, 0b00000000, 8, 0)]

    class FrontLeftTyreAlarmInfoPWarnFlag:
        sig_name = "FrontLeftTyreAlarmInfoPWarnFlag"
        sig_start_bit = 237
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PWarnFlag_Normal': 0, 'PWarnFlag_LowPWarn': 1, 'PWarnFlag_Reserve1': 2, 'PWarnFlag_Reserve2': 3}
        compute_method = None
        length = 2
        startbit = 237
        byte = 29
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class SeatOccpSts_UB:
        sig_name = "SeatOccpSts_UB"
        sig_start_bit = 455
        update_id_bit = 455
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
        startbit = 455
        byte = 56
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class CooltCircFlwEstimdHvBattCirc:
        sig_name = "CooltCircFlwEstimdHvBattCirc"
        sig_start_bit = 118
        update_id_bit = None
        sig_length = 9
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 500
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 118
        bmuws_info = [(14, 0b01111111, 0b10000000, 7, 0), (15, 0b11000000, 0b00111111, 2, 6)]

    class CooltCircFlwEstimd_UB:
        sig_name = "CooltCircFlwEstimd_UB"
        sig_start_bit = 132
        update_id_bit = 132
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
        startbit = 132
        byte = 16
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class DCDCFltTWarn:
        sig_name = "DCDCFltTWarn"
        sig_start_bit = 202
        update_id_bit = 200
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flt_Initial': 0, 'Flt_NoFault': 1, 'Flt_Fault': 2}
        compute_method = None
        length = 2
        startbit = 202
        byte = 25
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class RearRightTyreAlarmInfo_UB:
        sig_name = "RearRightTyreAlarmInfo_UB"
        sig_start_bit = 432
        update_id_bit = 432
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
        startbit = 432
        byte = 54
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class SeatOccpStsDrvrSeatSts:
        sig_name = "SeatOccpStsDrvrSeatSts"
        sig_start_bit = 447
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
        startbit = 447
        byte = 55
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class MotHeatgPwrDes:
        sig_name = "MotHeatgPwrDes"
        sig_start_bit = 394
        update_id_bit = 400
        sig_length = 10
        sig_value_factor = 20
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 394
        bmuws_info = [(49, 0b00000111, 0b11111000, 3, 0), (50, 0b11111110, 0b00000001, 7, 1)]

    class HVBattThermReqFromSrvCooltFlwReq:
        sig_name = "HVBattThermReqFromSrvCooltFlwReq"
        sig_start_bit = 458
        update_id_bit = None
        sig_length = 9
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 500
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 458
        bmuws_info = [(57, 0b00000111, 0b11111000, 3, 0), (58, 0b11111100, 0b00000011, 6, 2)]

    class HVBattHeatgPwrDes:
        sig_name = "HVBattHeatgPwrDes"
        sig_start_bit = 271
        update_id_bit = 274
        sig_length = 13
        sig_value_factor = 10
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 271
        bmuws_info = [(33, 0b11111111, 0b00000000, 8, 0), (34, 0b11111000, 0b00000111, 5, 3)]

    class SeatOccpStsThrdRowLeSeatSts:
        sig_name = "SeatOccpStsThrdRowLeSeatSts"
        sig_start_bit = 442
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
        startbit = 442
        byte = 55
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class RearRightTyreAlarmInfoBattLowWarnFlag:
        sig_name = "RearRightTyreAlarmInfoBattLowWarnFlag"
        sig_start_bit = 439
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BattLowWarnFlag_Normal': 0, 'BattLowWarnFlag_Warning': 1}
        compute_method = None
        length = 1
        startbit = 439
        byte = 54
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class DynoModSts:
        sig_name = "DynoModSts"
        sig_start_bit = 230
        update_id_bit = 229
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
        startbit = 230
        byte = 28
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class FrontLeftTyreAlarmInfo_UB:
        sig_name = "FrontLeftTyreAlarmInfo_UB"
        sig_start_bit = 232
        update_id_bit = 232
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
        startbit = 232
        byte = 29
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class CooltTSnsrT3EstimdT:
        sig_name = "CooltTSnsrT3EstimdT"
        sig_start_bit = 173
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = -256.0
        sig_value_min = 0
        sig_value_max = 5119
        sig_byteorder = "Motorola"
        sig_value_init = 2560
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 173
        bmuws_info = [(21, 0b00111111, 0b11000000, 6, 0), (22, 0b11111110, 0b00000001, 7, 1)]

    class CmpmtClimaSteadySts:
        sig_name = "CmpmtClimaSteadySts"
        sig_start_bit = 23
        update_id_bit = 22
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
        startbit = 23
        byte = 2
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class FrontRightTyreAlarmInfoBattLowWarnFlag:
        sig_name = "FrontRightTyreAlarmInfoBattLowWarnFlag"
        sig_start_bit = 247
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BattLowWarnFlag_Normal': 0, 'BattLowWarnFlag_Warning': 1}
        compute_method = None
        length = 1
        startbit = 247
        byte = 30
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class CmptmtThermMngtHVPwrCns:
        sig_name = "CmptmtThermMngtHVPwrCns"
        sig_start_bit = 39
        update_id_bit = 42
        sig_length = 13
        sig_value_factor = 10
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111000, 0b00000111, 5, 3)]

    class TrlrModSts:
        sig_name = "TrlrModSts"
        sig_start_bit = 418
        update_id_bit = 416
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TrlrModSts_Off': 0, 'TrlrModSts_On': 1}
        compute_method = None
        length = 2
        startbit = 418
        byte = 52
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class CmptmtAirPTCOutlTEstimd:
        sig_name = "CmptmtAirPTCOutlTEstimd"
        sig_start_bit = 21
        update_id_bit = 24
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = -256.0
        sig_value_min = 0
        sig_value_max = 5119
        sig_byteorder = "Motorola"
        sig_value_init = 2560
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 21
        bmuws_info = [(2, 0b00111111, 0b11000000, 6, 0), (3, 0b11111110, 0b00000001, 7, 1)]

    class HVBattThermPwrAllwd:
        sig_name = "HVBattThermPwrAllwd"
        sig_start_bit = 291
        update_id_bit = 310
        sig_length = 13
        sig_value_factor = 10
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 291
        bmuws_info = [(36, 0b00001111, 0b11110000, 4, 0), (37, 0b11111111, 0b00000000, 8, 0), (38, 0b10000000, 0b01111111, 1, 7)]

    class CooltTSnsrT4Estimd_UB:
        sig_name = "CooltTSnsrT4Estimd_UB"
        sig_start_bit = 192
        update_id_bit = 192
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
        startbit = 192
        byte = 24
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class CooltTSnsrT3EstimdDataQly:
        sig_name = "CooltTSnsrT3EstimdDataQly"
        sig_start_bit = 175
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SnsrQly_SnsrNotOk': 0, 'SnsrQly_SnsrOk': 1}
        compute_method = None
        length = 2
        startbit = 175
        byte = 21
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class FrontRightTyreAlarmInfoTWarnFlag:
        sig_name = "FrontRightTyreAlarmInfoTWarnFlag"
        sig_start_bit = 242
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TWarnFlag_Nromal': 0, 'TWarnFlag_HighTWarn': 1, 'TWarnFlag_Reserve1': 2, 'TWarnFlag_Reserve2': 3}
        compute_method = None
        length = 2
        startbit = 242
        byte = 30
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class FrontRightTyreAlarmInfo_UB:
        sig_name = "FrontRightTyreAlarmInfo_UB"
        sig_start_bit = 240
        update_id_bit = 240
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
        startbit = 240
        byte = 30
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class CooltTSnsrT4EstimdDataQly:
        sig_name = "CooltTSnsrT4EstimdDataQly"
        sig_start_bit = 191
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SnsrQly_SnsrNotOk': 0, 'SnsrQly_SnsrOk': 1}
        compute_method = None
        length = 2
        startbit = 191
        byte = 23
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HVBattThermReqFromSrvThermReq:
        sig_name = "HVBattThermReqFromSrvThermReq"
        sig_start_bit = 484
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HVBattThermReq_Idle': 0, 'HVBattThermReq_ThermalBalancing': 1, 'HVBattThermReq_PassiveHeating': 2, 'HVBattThermReq_ActiveHeating': 3, 'HVBattThermReq_PassiveCooling': 4, 'HVBattThermReq_ActiveCooling': 5, 'HVBattThermReq_CombinedCooling': 6, 'HVBattThermReq_Reserved': 7}
        compute_method = None
        length = 3
        startbit = 484
        byte = 60
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class CooltCircFlwEstimdHeatrCirc:
        sig_name = "CooltCircFlwEstimdHeatrCirc"
        sig_start_bit = 111
        update_id_bit = None
        sig_length = 9
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 500
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 111
        bmuws_info = [(13, 0b11111111, 0b00000000, 8, 0), (14, 0b10000000, 0b01111111, 1, 7)]

    class HVBattThermReqFromSrv_UB:
        sig_name = "HVBattThermReqFromSrv_UB"
        sig_start_bit = 481
        update_id_bit = 481
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
        startbit = 481
        byte = 60
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class AmbTEstimdT:
        sig_name = "AmbTEstimdT"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = -256.0
        sig_value_min = 0
        sig_value_max = 5119
        sig_byteorder = "Motorola"
        sig_value_init = 2560
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111000, 0b00000111, 5, 3)]

    class FrontRightTyreAlarmInfoPWarnFlag:
        sig_name = "FrontRightTyreAlarmInfoPWarnFlag"
        sig_start_bit = 245
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PWarnFlag_Normal': 0, 'PWarnFlag_LowPWarn': 1, 'PWarnFlag_Reserve1': 2, 'PWarnFlag_Reserve2': 3}
        compute_method = None
        length = 2
        startbit = 245
        byte = 30
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class CrashSaved:
        sig_name = "CrashSaved"
        sig_start_bit = 207
        update_id_bit = 206
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
        startbit = 207
        byte = 25
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class SeatOccpStsSecRowRiSeatSts:
        sig_name = "SeatOccpStsSecRowRiSeatSts"
        sig_start_bit = 443
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
        startbit = 443
        byte = 55
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class SeatOccpStsThrdRowMidSeatSts:
        sig_name = "SeatOccpStsThrdRowMidSeatSts"
        sig_start_bit = 441
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
        startbit = 441
        byte = 55
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class HVBattThermReqActualCellTTar:
        sig_name = "HVBattThermReqActualCellTTar"
        sig_start_bit = 319
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
        startbit = 319
        bmuws_info = [(39, 0b11111111, 0b00000000, 8, 0), (40, 0b11100000, 0b00011111, 3, 5)]

    class RearLeftTyreAlarmInfoSysWarnFlag:
        sig_name = "RearLeftTyreAlarmInfoSysWarnFlag"
        sig_start_bit = 427
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SysWarnFlag_Nromal': 0, 'SysWarnFlag_Warning': 1}
        compute_method = None
        length = 1
        startbit = 427
        byte = 53
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class FrontLeftTyreAlarmInfoTWarnFlag:
        sig_name = "FrontLeftTyreAlarmInfoTWarnFlag"
        sig_start_bit = 234
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TWarnFlag_Nromal': 0, 'TWarnFlag_HighTWarn': 1, 'TWarnFlag_Reserve1': 2, 'TWarnFlag_Reserve2': 3}
        compute_method = None
        length = 2
        startbit = 234
        byte = 29
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class HVBattThermReqResp:
        sig_name = "HVBattThermReqResp"
        sig_start_bit = 399
        update_id_bit = 395
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 12
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HVBattThermReqFb_Idle': 0, 'HVBattThermReqFb_ThermalBalancing': 1, 'HVBattThermReqFb_PassiveHeating': 2, 'HVBattThermReqFb_ActiveHeating': 3, 'HVBattThermReqFb_PassiveCooling': 4, 'HVBattThermReqFb_ActiveCooling': 5, 'HVBattThermReqFb_CombineCooling': 6, 'HVBattThermReqFb_ActivePassiveHeating': 7, 'HVBattThermReqFb_Inhibt': 8, 'HVBattThermReqFb_HeatingFinish': 9, 'HVBattThermReqFb_CoolingFinish': 10, 'HVBattThermReqFb_Reserve01': 11, 'HVBattThermReqFb_Reserve02': 12}
        compute_method = None
        length = 4
        startbit = 399
        byte = 49
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class CooltTSnsrT3Estimd_UB:
        sig_name = "CooltTSnsrT3Estimd_UB"
        sig_start_bit = 176
        update_id_bit = 176
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
        startbit = 176
        byte = 22
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class HVBattThermMngtHVPwrCns:
        sig_name = "HVBattThermMngtHVPwrCns"
        sig_start_bit = 273
        update_id_bit = 292
        sig_length = 13
        sig_value_factor = 10
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 273
        bmuws_info = [(34, 0b00000011, 0b11111100, 2, 0), (35, 0b11111111, 0b00000000, 8, 0), (36, 0b11100000, 0b00011111, 3, 5)]

    class ScrnGearLvrIndcnVirt:
        sig_name = "ScrnGearLvrIndcnVirt"
        sig_start_bit = 422
        update_id_bit = 419
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 7
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GearLvrIndcn_Default': 0, 'GearLvrIndcn_P': 1, 'GearLvrIndcn_R': 2, 'GearLvrIndcn_N': 3, 'GearLvrIndcn_D': 4, 'GearLvrIndcn_Reserved1': 5, 'GearLvrIndcn_Reserved2': 6, 'GearLvrIndcn_Undefd': 7}
        compute_method = None
        length = 3
        startbit = 422
        byte = 52
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class CmptmtTSpHdLvlTarT_UB:
        sig_name = "CmptmtTSpHdLvlTarT_UB"
        sig_start_bit = 99
        update_id_bit = 99
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
        startbit = 99
        byte = 12
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class SeatOccpStsThrdRowRiSeatSts:
        sig_name = "SeatOccpStsThrdRowRiSeatSts"
        sig_start_bit = 440
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
        startbit = 440
        byte = 55
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class HVBattThermReqFromSrvSourceID:
        sig_name = "HVBattThermReqFromSrvSourceID"
        sig_start_bit = 495
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
        startbit = 495
        bmuws_info = [(61, 0b11111111, 0b00000000, 8, 0), (62, 0b11111111, 0b00000000, 8, 0)]

    class RearRightTyreAlarmInfoSysWarnFlag:
        sig_name = "RearRightTyreAlarmInfoSysWarnFlag"
        sig_start_bit = 435
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SysWarnFlag_Nromal': 0, 'SysWarnFlag_Warning': 1}
        compute_method = None
        length = 1
        startbit = 435
        byte = 54
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class RearLeftTyreAlarmInfoTWarnFlag:
        sig_name = "RearLeftTyreAlarmInfoTWarnFlag"
        sig_start_bit = 426
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TWarnFlag_Nromal': 0, 'TWarnFlag_HighTWarn': 1, 'TWarnFlag_Reserve1': 2, 'TWarnFlag_Reserve2': 3}
        compute_method = None
        length = 2
        startbit = 426
        byte = 53
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class DcDcLimnIndcnWarn:
        sig_name = "DcDcLimnIndcnWarn"
        sig_start_bit = 215
        update_id_bit = 231
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
        startbit = 215
        bmuws_info = [(26, 0b11111111, 0b00000000, 8, 0), (27, 0b11111111, 0b00000000, 8, 0)]

    class FrontLeftTyreAlarmInfoSysWarnFlag:
        sig_name = "FrontLeftTyreAlarmInfoSysWarnFlag"
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
        sig_value_table = {'SysWarnFlag_Nromal': 0, 'SysWarnFlag_Warning': 1}
        compute_method = None
        length = 1
        startbit = 235
        byte = 29
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class CooltCircFlwEstimdPWTCirc:
        sig_name = "CooltCircFlwEstimdPWTCirc"
        sig_start_bit = 125
        update_id_bit = None
        sig_length = 9
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 500
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 125
        bmuws_info = [(15, 0b00111111, 0b11000000, 6, 0), (16, 0b11100000, 0b00011111, 3, 5)]

    class SeatOccpStsSecRowMidSeatSts:
        sig_name = "SeatOccpStsSecRowMidSeatSts"
        sig_start_bit = 444
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
        startbit = 444
        byte = 55
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class RearLeftTyreAlarmInfo_UB:
        sig_name = "RearLeftTyreAlarmInfo_UB"
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

    class CooltTSnsrT1Estimd_UB:
        sig_name = "CooltTSnsrT1Estimd_UB"
        sig_start_bit = 144
        update_id_bit = 144
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
        startbit = 144
        byte = 18
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class HVBattThermReqFromSrvCellTType:
        sig_name = "HVBattThermReqFromSrvCellTType"
        sig_start_bit = 511
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BattTemperatureType_Idle': 0, 'BattTemperatureType_Tmin': 1, 'BattTemperatureType_TAvg': 2, 'BattTemperatureType_TMax': 3}
        compute_method = None
        length = 2
        startbit = 511
        byte = 63
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class RearRightTyreAlarmInfoPWarnFlag:
        sig_name = "RearRightTyreAlarmInfoPWarnFlag"
        sig_start_bit = 437
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PWarnFlag_Normal': 0, 'PWarnFlag_LowPWarn': 1, 'PWarnFlag_Reserve1': 2, 'PWarnFlag_Reserve2': 3}
        compute_method = None
        length = 2
        startbit = 437
        byte = 54
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class AmbTEstimd_UB:
        sig_name = "AmbTEstimd_UB"
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


class CCUMCUCDToVCUOBDPropulsionCANFDDiagReqFrame:
    msg_name = "CCUMCUCDToVCUOBDPropulsionCANFDDiagReqFrame"
    msg_id = 2016
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CCUMCUCD"
    rx_nodes = ['VCU']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class CCUMCUCDPropulsionCANFDFr10:
    msg_name = "CCUMCUCDPropulsionCANFDFr10"
    msg_id = 17
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CCUMCUCD"
    rx_nodes = ['BECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HiUDeactvn:
        sig_name = "HiUDeactvn"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7


class VCUPropulsionCANFDNmFr:
    msg_name = "VCUPropulsionCANFDNmFr"
    msg_id = 1285
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "VCU"
    rx_nodes = ['SRS']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class CCUMCUCDPropulsionCANFDNmFr:
    msg_name = "CCUMCUCDPropulsionCANFDNmFr"
    msg_id = 1281
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CCUMCUCD"
    rx_nodes = ['CCUMCUAD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class MGMPropulsionCANFDFr03:
    msg_name = "MGMPropulsionCANFDFr03"
    msg_id = 280
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.03
    msg_length = 8
    tx_node = "MGM"
    rx_nodes = ['VCU', 'BCU1']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class FrntMotLimnIndcn:
        sig_name = "FrntMotLimnIndcn"
        sig_start_bit = 15
        update_id_bit = 31
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
        startbit = 15
        bmuws_info = [(1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class FrntMot3PhaShoCricSt:
        sig_name = "FrntMot3PhaShoCricSt"
        sig_start_bit = 7
        update_id_bit = 1
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ThreePhaShoCricSts_Initial': 0, 'ThreePhaShoCricSts_NoShoCirc': 1, 'ThreePhaShoCricSts_UpprShoCirc': 2, 'ThreePhaShoCricSts_UndrShoCirc': 3, 'ThreePhaShoCricSts_Others': 4, 'ThreePhaShoCricSts_Unknown': 5, 'ThreePhaShoCricSts_Reserved1': 6, 'ThreePhaShoCricSts_Reserved2': 7}
        compute_method = None
        length = 3
        startbit = 7
        byte = 0
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class FrntMotActvDchgSts:
        sig_name = "FrntMotActvDchgSts"
        sig_start_bit = 4
        update_id_bit = 0
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 6
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ActvDchgSts_Initial': 0, 'ActvDchgSts_Inactive': 1, 'ActvDchgSts_Active': 2, 'ActvDchgSts_Finished': 3, 'ActvDchgSts_Timeout': 4, 'ActvDchgSts_Reserved1': 5, 'ActvDchgSts_Reserved2': 6}
        compute_method = None
        length = 3
        startbit = 4
        byte = 0
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2


class CCUMCUCDToSRSOBDPropulsionCANFDDiagReqFrame:
    msg_name = "CCUMCUCDToSRSOBDPropulsionCANFDDiagReqFrame"
    msg_id = 2033
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CCUMCUCD"
    rx_nodes = ['SRS']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class BECMToCCUMCUCDPropulsionCANFDDiagRespFrame:
    msg_name = "BECMToCCUMCUCDPropulsionCANFDDiagRespFrame"
    msg_id = 1589
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "BECM"
    rx_nodes = ['CCUMCUCD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class MGMPropulsionCANFDFr02:
    msg_name = "MGMPropulsionCANFDFr02"
    msg_id = 134
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "MGM"
    rx_nodes = ['VCU', 'CCUMCUCD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class FrntMotIDc:
        sig_name = "FrntMotIDc"
        sig_start_bit = 7
        update_id_bit = 39
        sig_length = 16
        sig_value_factor = 0.1
        sig_value_offset = -3000.0
        sig_value_min = 0
        sig_value_max = 65535
        sig_byteorder = "Motorola"
        sig_value_init = 30000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class FrntMotUDc:
        sig_name = "FrntMotUDc"
        sig_start_bit = 23
        update_id_bit = 38
        sig_length = 16
        sig_value_factor = 0.1
        sig_value_offset = 0
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


class CCUMCUCDPropulsionCANFDFr09:
    msg_name = "CCUMCUCDPropulsionCANFDFr09"
    msg_id = 612
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 64
    tx_node = "CCUMCUCD"
    rx_nodes = ['VCU', 'SRS', 'MGM', 'EGSM', 'IEM', 'BECM', 'BCU2', 'CCUMCUAD', 'BCU1']
    sig_group_dict = {'VehCfgDataGrp': ['VehCfgDataGrpVehCfgData1BlkIDBytePosn1', 'VehCfgDataGrpVehCfgData1BytePosn10', 'VehCfgDataGrpVehCfgData1BytePosn11', 'VehCfgDataGrpVehCfgData1BytePosn12', 'VehCfgDataGrpVehCfgData1BytePosn13', 'VehCfgDataGrpVehCfgData1BytePosn14', 'VehCfgDataGrpVehCfgData1BytePosn15', 'VehCfgDataGrpVehCfgData1BytePosn16', 'VehCfgDataGrpVehCfgData1BytePosn17', 'VehCfgDataGrpVehCfgData1BytePosn18', 'VehCfgDataGrpVehCfgData1BytePosn19', 'VehCfgDataGrpVehCfgData1BytePosn2', 'VehCfgDataGrpVehCfgData1BytePosn20', 'VehCfgDataGrpVehCfgData1BytePosn21', 'VehCfgDataGrpVehCfgData1BytePosn22', 'VehCfgDataGrpVehCfgData1BytePosn23', 'VehCfgDataGrpVehCfgData1BytePosn24', 'VehCfgDataGrpVehCfgData1BytePosn25', 'VehCfgDataGrpVehCfgData1BytePosn26', 'VehCfgDataGrpVehCfgData1BytePosn27', 'VehCfgDataGrpVehCfgData1BytePosn28', 'VehCfgDataGrpVehCfgData1BytePosn29', 'VehCfgDataGrpVehCfgData1BytePosn3', 'VehCfgDataGrpVehCfgData1BytePosn30', 'VehCfgDataGrpVehCfgData1BytePosn31', 'VehCfgDataGrpVehCfgData1BytePosn32', 'VehCfgDataGrpVehCfgData1BytePosn33', 'VehCfgDataGrpVehCfgData1BytePosn34', 'VehCfgDataGrpVehCfgData1BytePosn35', 'VehCfgDataGrpVehCfgData1BytePosn36', 'VehCfgDataGrpVehCfgData1BytePosn37', 'VehCfgDataGrpVehCfgData1BytePosn38', 'VehCfgDataGrpVehCfgData1BytePosn39', 'VehCfgDataGrpVehCfgData1BytePosn4', 'VehCfgDataGrpVehCfgData1BytePosn40', 'VehCfgDataGrpVehCfgData1BytePosn41', 'VehCfgDataGrpVehCfgData1BytePosn42', 'VehCfgDataGrpVehCfgData1BytePosn43', 'VehCfgDataGrpVehCfgData1BytePosn44', 'VehCfgDataGrpVehCfgData1BytePosn45', 'VehCfgDataGrpVehCfgData1BytePosn46', 'VehCfgDataGrpVehCfgData1BytePosn47', 'VehCfgDataGrpVehCfgData1BytePosn48', 'VehCfgDataGrpVehCfgData1BytePosn49', 'VehCfgDataGrpVehCfgData1BytePosn5', 'VehCfgDataGrpVehCfgData1BytePosn50', 'VehCfgDataGrpVehCfgData1BytePosn51', 'VehCfgDataGrpVehCfgData1BytePosn52', 'VehCfgDataGrpVehCfgData1BytePosn53', 'VehCfgDataGrpVehCfgData1BytePosn54', 'VehCfgDataGrpVehCfgData1BytePosn55', 'VehCfgDataGrpVehCfgData1BytePosn56', 'VehCfgDataGrpVehCfgData1BytePosn57', 'VehCfgDataGrpVehCfgData1BytePosn58', 'VehCfgDataGrpVehCfgData1BytePosn59', 'VehCfgDataGrpVehCfgData1BytePosn6', 'VehCfgDataGrpVehCfgData1BytePosn60', 'VehCfgDataGrpVehCfgData1BytePosn61', 'VehCfgDataGrpVehCfgData1BytePosn62', 'VehCfgDataGrpVehCfgData1BytePosn63', 'VehCfgDataGrpVehCfgData1BytePosn64', 'VehCfgDataGrpVehCfgData1BytePosn7', 'VehCfgDataGrpVehCfgData1BytePosn8', 'VehCfgDataGrpVehCfgData1BytePosn9']}
    sig_group_dataid_dict = {}

    class VehCfgDataGrpVehCfgData1BytePosn36:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn36"
        sig_start_bit = 287
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
        startbit = 287
        byte = 35
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn39:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn39"
        sig_start_bit = 311
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
        startbit = 311
        byte = 38
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn31:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn31"
        sig_start_bit = 247
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
        startbit = 247
        byte = 30
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn12:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn12"
        sig_start_bit = 95
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
        startbit = 95
        byte = 11
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn64:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn64"
        sig_start_bit = 511
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
        startbit = 511
        byte = 63
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn22:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn22"
        sig_start_bit = 175
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
        startbit = 175
        byte = 21
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn6:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn6"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn38:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn38"
        sig_start_bit = 303
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
        startbit = 303
        byte = 37
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn17:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn17"
        sig_start_bit = 135
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
        startbit = 135
        byte = 16
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn33:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn33"
        sig_start_bit = 263
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
        startbit = 263
        byte = 32
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn40:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn40"
        sig_start_bit = 319
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
        startbit = 319
        byte = 39
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn9:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn9"
        sig_start_bit = 71
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
        startbit = 71
        byte = 8
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn48:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn48"
        sig_start_bit = 383
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
        startbit = 383
        byte = 47
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn13:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn13"
        sig_start_bit = 103
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
        startbit = 103
        byte = 12
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn51:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn51"
        sig_start_bit = 407
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
        startbit = 407
        byte = 50
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn60:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn60"
        sig_start_bit = 479
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
        startbit = 479
        byte = 59
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn34:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn34"
        sig_start_bit = 271
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
        startbit = 271
        byte = 33
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn57:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn57"
        sig_start_bit = 455
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
        startbit = 455
        byte = 56
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn18:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn18"
        sig_start_bit = 143
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
        startbit = 143
        byte = 17
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn4:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn4"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BlkIDBytePosn1:
        sig_name = "VehCfgDataGrpVehCfgData1BlkIDBytePosn1"
        sig_start_bit = 7
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
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn49:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn49"
        sig_start_bit = 391
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
        startbit = 391
        byte = 48
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn3:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn3"
        sig_start_bit = 23
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
        startbit = 23
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn7:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn7"
        sig_start_bit = 55
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
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn54:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn54"
        sig_start_bit = 431
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
        startbit = 431
        byte = 53
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn47:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn47"
        sig_start_bit = 375
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
        startbit = 375
        byte = 46
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn19:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn19"
        sig_start_bit = 151
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
        startbit = 151
        byte = 18
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn46:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn46"
        sig_start_bit = 367
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
        startbit = 367
        byte = 45
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn28:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn28"
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

    class VehCfgDataGrpVehCfgData1BytePosn52:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn52"
        sig_start_bit = 415
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
        startbit = 415
        byte = 51
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn27:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn27"
        sig_start_bit = 215
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
        startbit = 215
        byte = 26
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn5:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn5"
        sig_start_bit = 39
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
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn37:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn37"
        sig_start_bit = 295
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
        startbit = 295
        byte = 36
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn32:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn32"
        sig_start_bit = 255
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
        startbit = 255
        byte = 31
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn10:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn10"
        sig_start_bit = 79
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
        startbit = 79
        byte = 9
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn15:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn15"
        sig_start_bit = 119
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
        startbit = 119
        byte = 14
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn58:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn58"
        sig_start_bit = 463
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
        startbit = 463
        byte = 57
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn23:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn23"
        sig_start_bit = 183
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
        startbit = 183
        byte = 22
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn44:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn44"
        sig_start_bit = 351
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
        startbit = 351
        byte = 43
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn14:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn14"
        sig_start_bit = 111
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
        startbit = 111
        byte = 13
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn16:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn16"
        sig_start_bit = 127
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
        startbit = 127
        byte = 15
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn59:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn59"
        sig_start_bit = 471
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
        startbit = 471
        byte = 58
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn50:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn50"
        sig_start_bit = 399
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
        startbit = 399
        byte = 49
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn25:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn25"
        sig_start_bit = 199
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
        startbit = 199
        byte = 24
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn26:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn26"
        sig_start_bit = 207
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
        startbit = 207
        byte = 25
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn42:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn42"
        sig_start_bit = 335
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
        startbit = 335
        byte = 41
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn30:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn30"
        sig_start_bit = 239
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
        startbit = 239
        byte = 29
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn35:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn35"
        sig_start_bit = 279
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
        startbit = 279
        byte = 34
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn8:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn8"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn43:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn43"
        sig_start_bit = 343
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
        startbit = 343
        byte = 42
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn20:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn20"
        sig_start_bit = 159
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
        startbit = 159
        byte = 19
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn45:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn45"
        sig_start_bit = 359
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
        startbit = 359
        byte = 44
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn61:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn61"
        sig_start_bit = 487
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
        startbit = 487
        byte = 60
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn41:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn41"
        sig_start_bit = 327
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
        startbit = 327
        byte = 40
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn63:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn63"
        sig_start_bit = 503
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
        startbit = 503
        byte = 62
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn55:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn55"
        sig_start_bit = 439
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
        startbit = 439
        byte = 54
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn53:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn53"
        sig_start_bit = 423
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
        startbit = 423
        byte = 52
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn56:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn56"
        sig_start_bit = 447
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
        startbit = 447
        byte = 55
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn62:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn62"
        sig_start_bit = 495
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
        startbit = 495
        byte = 61
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn29:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn29"
        sig_start_bit = 231
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
        startbit = 231
        byte = 28
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn21:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn21"
        sig_start_bit = 167
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
        startbit = 167
        byte = 20
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn2:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn2"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn11:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn11"
        sig_start_bit = 87
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
        startbit = 87
        byte = 10
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgDataGrpVehCfgData1BytePosn24:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn24"
        sig_start_bit = 191
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
        startbit = 191
        byte = 23
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class IEMPropulsionCANFDFr04:
    msg_name = "IEMPropulsionCANFDFr04"
    msg_id = 386
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 16
    tx_node = "IEM"
    rx_nodes = ['VCU', 'CCUMCUCD']
    sig_group_dict = {'ImobChkIEM': ['ImobChkIEMChks', 'ImobChkIEMCntr', 'ImobChkIEMImobChkSts', 'ImobChkIEMImobDateChk0', 'ImobChkIEMImobDateChk1', 'ImobChkIEMImobDateChk2', 'ImobChkIEMImobDateChk3', 'ImobChkIEMImobDateChk4', 'ImobChkIEMImobDateChk5'], 'ReMotOilPmpPwrSplyU': ['ReMotOilPmpPwrSplyUMotOilPmpPwrSplyU', 'ReMotOilPmpPwrSplyUQf']}
    sig_group_dataid_dict = {}

    class ImobStsIEM:
        sig_name = "ImobStsIEM"
        sig_start_bit = 3
        update_id_bit = 1
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ImobSts_Undefd': 0, 'ImobSts_ImobNotPass': 1, 'ImobSts_ImobPass': 2, 'ImobSts_ImobRemPass': 3}
        compute_method = None
        length = 2
        startbit = 3
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class ImobChkIEMCntr:
        sig_name = "ImobChkIEMCntr"
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

    class ImobChkIEMImobDateChk0:
        sig_name = "ImobChkIEMImobDateChk0"
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

    class ImobChkIEM_UB:
        sig_name = "ImobChkIEM_UB"
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

    class ImobChkIEMImobDateChk5:
        sig_name = "ImobChkIEMImobDateChk5"
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

    class ImobChkIEMImobDateChk3:
        sig_name = "ImobChkIEMImobDateChk3"
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

    class ImobChkIEMChks:
        sig_name = "ImobChkIEMChks"
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

    class ImobChkIEMImobDateChk4:
        sig_name = "ImobChkIEMImobDateChk4"
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

    class ReMotOilPmpPwrSplyUQf:
        sig_name = "ReMotOilPmpPwrSplyUQf"
        sig_start_bit = 86
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
        startbit = 86
        byte = 10
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class ReMotOilPmpPwrSplyUMotOilPmpPwrSplyU:
        sig_name = "ReMotOilPmpPwrSplyUMotOilPmpPwrSplyU"
        sig_start_bit = 79
        update_id_bit = None
        sig_length = 9
        sig_value_factor = 0.025
        sig_value_offset = 5
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 280
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 79
        bmuws_info = [(9, 0b11111111, 0b00000000, 8, 0), (10, 0b10000000, 0b01111111, 1, 7)]

    class ImobChkIEMImobDateChk2:
        sig_name = "ImobChkIEMImobDateChk2"
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

    class ImobChkIEMImobChkSts:
        sig_name = "ImobChkIEMImobChkSts"
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
        sig_value_table = {'AvlSts1_Avl': 0, 'AvlSts1_NotAvl': 1}
        compute_method = None
        length = 1
        startbit = 23
        byte = 2
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ImobChkIEMImobDateChk1:
        sig_name = "ImobChkIEMImobDateChk1"
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

    class ReMotOilPmpPwrSplyU_UB:
        sig_name = "ReMotOilPmpPwrSplyU_UB"
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

    class BoostStsFb1:
        sig_name = "BoostStsFb1"
        sig_start_bit = 7
        update_id_bit = 4
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 7
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BoostSt_Init': 0, 'BoostSt_C1Precharge': 1, 'BoostSt_BoostReady': 2, 'BoostSt_BoostActive': 3, 'BoostSt_C1activedischarge': 4, 'BoostSt_Fault': 5, 'BoostSt_Derating': 6, 'BoostSt_BoostOff': 7}
        compute_method = None
        length = 3
        startbit = 7
        byte = 0
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5


class ODPPropulsionCANFDFr01:
    msg_name = "ODPPropulsionCANFDFr01"
    msg_id = 388
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 24
    tx_node = "ODP"
    rx_nodes = ['VCU', 'ETC', 'CCUMCUCD']
    sig_group_dict = {'DCDCActILoSide': ['DCDCActILoSideChks', 'DCDCActILoSideCntr', 'DCDCActILoSideDCDCILowside']}
    sig_group_dataid_dict = {}

    class DCDCActOutpPwr:
        sig_name = "DCDCActOutpPwr"
        sig_start_bit = 49
        update_id_bit = 70
        sig_length = 11
        sig_value_factor = 10
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2046
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 49
        bmuws_info = [(6, 0b00000011, 0b11111100, 2, 0), (7, 0b11111111, 0b00000000, 8, 0), (8, 0b10000000, 0b01111111, 1, 7)]

    class DCDCActILoSide_UB:
        sig_name = "DCDCActILoSide_UB"
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

    class DCDCActInpPwr:
        sig_name = "DCDCActInpPwr"
        sig_start_bit = 45
        update_id_bit = 50
        sig_length = 11
        sig_value_factor = 10
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2046
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 45
        bmuws_info = [(5, 0b00111111, 0b11000000, 6, 0), (6, 0b11111000, 0b00000111, 5, 3)]

    class DCDCActUHiSide:
        sig_name = "DCDCActUHiSide"
        sig_start_bit = 95
        update_id_bit = 129
        sig_length = 16
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 65535
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 95
        bmuws_info = [(11, 0b11111111, 0b00000000, 8, 0), (12, 0b11111111, 0b00000000, 8, 0)]

    class DCDCAvlIMaxLoSide:
        sig_name = "DCDCAvlIMaxLoSide"
        sig_start_bit = 127
        update_id_bit = 130
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
        startbit = 127
        bmuws_info = [(15, 0b11111111, 0b00000000, 8, 0), (16, 0b11110000, 0b00001111, 4, 4)]

    class DCDCActIHiSide:
        sig_name = "DCDCActIHiSide"
        sig_start_bit = 7
        update_id_bit = 47
        sig_length = 16
        sig_value_factor = 0.1
        sig_value_offset = -3000.0
        sig_value_min = 0
        sig_value_max = 65535
        sig_byteorder = "Motorola"
        sig_value_init = 30000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class DCDCActULoSide:
        sig_name = "DCDCActULoSide"
        sig_start_bit = 69
        update_id_bit = 76
        sig_length = 9
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 69
        bmuws_info = [(8, 0b00111111, 0b11000000, 6, 0), (9, 0b11100000, 0b00011111, 3, 5)]

    class DcDcLimnIndcn:
        sig_name = "DcDcLimnIndcn"
        sig_start_bit = 111
        update_id_bit = 128
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
        startbit = 111
        bmuws_info = [(13, 0b11111111, 0b00000000, 8, 0), (14, 0b11111111, 0b00000000, 8, 0)]

    class DCDCActILoSideCntr:
        sig_name = "DCDCActILoSideCntr"
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

    class DCDCActvdModSts:
        sig_name = "DCDCActvdModSts"
        sig_start_bit = 75
        update_id_bit = 74
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DcDcActvdModSts_NoConversion': 0, 'DcDcActvdModSts_Conversion': 1}
        compute_method = None
        length = 1
        startbit = 75
        byte = 9
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class DCDCActILoSideChks:
        sig_name = "DCDCActILoSideChks"
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

    class DCDCFltElecSts:
        sig_name = "DCDCFltElecSts"
        sig_start_bit = 73
        update_id_bit = 87
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flt_Initial': 0, 'Flt_NoFault': 1, 'Flt_Fault': 2}
        compute_method = None
        length = 2
        startbit = 73
        byte = 9
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class DCDCFltTSts:
        sig_name = "DCDCFltTSts"
        sig_start_bit = 86
        update_id_bit = 84
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flt_Initial': 0, 'Flt_NoFault': 1, 'Flt_Fault': 2}
        compute_method = None
        length = 2
        startbit = 86
        byte = 10
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class DCDCActILoSideDCDCILowside:
        sig_name = "DCDCActILoSideDCDCILowside"
        sig_start_bit = 27
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
        startbit = 27
        bmuws_info = [(3, 0b00001111, 0b11110000, 4, 0), (4, 0b11111111, 0b00000000, 8, 0)]


class BCU1PropulsionCANFDFr01:
    msg_name = "BCU1PropulsionCANFDFr01"
    msg_id = 64
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 64
    tx_node = "BCU1"
    rx_nodes = ['VCU', 'CCUMCUCD', 'MGM', 'IEM', 'BCU2']
    sig_group_dict = {'WhlSpdRe': ['WhlSpdReChks', 'WhlSpdReCntr', 'WhlSpdReLeQf', 'WhlSpdReLeSpd', 'WhlSpdReRiQf', 'WhlSpdReRiSpd'], 'BrkMstCtrlModeReq': ['BrkMstCtrlModeReqChks', 'BrkMstCtrlModeReqCntr', 'BrkMstCtrlModeReqReq'], 'PropAxleTqMin': ['PropAxleTqMinChks', 'PropAxleTqMinCntr', 'PropAxleTqMinFrnt', 'PropAxleTqMinRe'], 'PropAxleTqMax': ['PropAxleTqMaxChks', 'PropAxleTqMaxCntr', 'PropAxleTqMaxFrnt', 'PropAxleTqMaxRe'], 'BrkRgnTqReq': ['BrkRgnTqReqBrkAtv', 'BrkRgnTqReqChks', 'BrkRgnTqReqCntr', 'BrkRgnTqReqQf1', 'BrkRgnTqReqRe', 'BrkRgnTqReqTot'], 'EscStsToDmc': ['EscStsToDmcChks', 'EscStsToDmcCntr', 'EscStsToDmcEscModeToDmcFrnt', 'EscStsToDmcEscModeToDmcRe', 'EscStsToDmcTarSpdFrnt', 'EscStsToDmcTarSpdRe'], 'WhlSpdFrnt': ['WhlSpdFrntChks', 'WhlSpdFrntCntr', 'WhlSpdFrntLeQf', 'WhlSpdFrntLeSpd', 'WhlSpdFrntRiQf', 'WhlSpdFrntRiSpd'], 'BrkSysStPrim': ['BrkSysStPrimBrkSysSts', 'BrkSysStPrimChks', 'BrkSysStPrimCntr'], 'EscVariantToDmc': ['EscVariantToDmcChks', 'EscVariantToDmcCntr', 'EscVariantToDmcEscVariantToDmc']}
    sig_group_dataid_dict = {'WhlSpdRe': 1055, 'PropAxleTqMin': 1047, 'PropAxleTqMax': 1046, 'BrkRgnTqReq': 1053, 'WhlSpdFrnt': 1045}

    class WhlSpdRe_UB:
        sig_name = "WhlSpdRe_UB"
        sig_start_bit = 368
        update_id_bit = 368
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
        startbit = 368
        byte = 46
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class PropAxleTqMinFrnt:
        sig_name = "PropAxleTqMinFrnt"
        sig_start_bit = 255
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = -20000
        sig_value_max = 20000
        sig_byteorder = "Motorola"
        sig_value_init = -20000.0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 255
        bmuws_info = [(31, 0b11111111, 0b00000000, 8, 0), (32, 0b11111111, 0b00000000, 8, 0)]

    class WhlSpdReRiSpd:
        sig_name = "WhlSpdReRiSpd"
        sig_start_bit = 367
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 0.00391
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 31970
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 367
        bmuws_info = [(45, 0b11111111, 0b00000000, 8, 0), (46, 0b11111110, 0b00000001, 7, 1)]

    class WhlSpdReRiQf:
        sig_name = "WhlSpdReRiQf"
        sig_start_bit = 341
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
        startbit = 341
        byte = 42
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class BrkRgnTqReqRe:
        sig_name = "BrkRgnTqReqRe"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = -20000
        sig_value_max = 20000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111111, 0b00000000, 8, 0)]

    class BrkRgnTqReqBrkAtv:
        sig_name = "BrkRgnTqReqBrkAtv"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ActvInActv2_Init': 0, 'ActvInActv2_InActv': 1, 'ActvInActv2_Actv': 2}
        compute_method = None
        length = 2
        startbit = 39
        byte = 4
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class BrkMstCtrlModeReq_UB:
        sig_name = "BrkMstCtrlModeReq_UB"
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

    class EscVariantToDmcCntr:
        sig_name = "EscVariantToDmcCntr"
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

    class WhlSpdReLeSpd:
        sig_name = "WhlSpdReLeSpd"
        sig_start_bit = 351
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 0.00391
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 31970
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 351
        bmuws_info = [(43, 0b11111111, 0b00000000, 8, 0), (44, 0b11111110, 0b00000001, 7, 1)]

    class EscVariantToDmcEscVariantToDmc:
        sig_name = "EscVariantToDmcEscVariantToDmc"
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

    class BrkRgnTqReqTot:
        sig_name = "BrkRgnTqReqTot"
        sig_start_bit = 63
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = -20000
        sig_value_max = 20000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 63
        bmuws_info = [(7, 0b11111111, 0b00000000, 8, 0), (8, 0b11111111, 0b00000000, 8, 0)]

    class BrkRgnTqReqChks:
        sig_name = "BrkRgnTqReqChks"
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

    class PropAxleTqMin_UB:
        sig_name = "PropAxleTqMin_UB"
        sig_start_bit = 244
        update_id_bit = 244
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
        startbit = 244
        byte = 30
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class WhlSpdFrntLeSpd:
        sig_name = "WhlSpdFrntLeSpd"
        sig_start_bit = 303
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 0.00391
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 31970
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 303
        bmuws_info = [(37, 0b11111111, 0b00000000, 8, 0), (38, 0b11111110, 0b00000001, 7, 1)]

    class PropAxleTqMinChks:
        sig_name = "PropAxleTqMinChks"
        sig_start_bit = 239
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 239
        byte = 29
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class WhlSpdReChks:
        sig_name = "WhlSpdReChks"
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

    class BrkMstCtrlModeReqReq:
        sig_name = "BrkMstCtrlModeReqReq"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ModCfmd_NoReq': 0, 'ModCfmd_ANP': 1, 'ModCfmd_AVP': 2, 'ModCfmd_ACC': 3, 'ModCfmd_Lcc': 4, 'ModCfmd_Reserved1': 5, 'ModCfmd_Reserved2': 6, 'ModCfmd_Reserved3': 7, 'ModCfmd_Reserved4': 8, 'ModCfmd_Reserved5': 9, 'ModCfmd_Reserved6': 10}
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class EscStsToDmcTarSpdRe:
        sig_name = "EscStsToDmcTarSpdRe"
        sig_start_bit = 143
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
        startbit = 143
        bmuws_info = [(17, 0b11111111, 0b00000000, 8, 0), (18, 0b11111111, 0b00000000, 8, 0)]

    class EscStsToDmcEscModeToDmcFrnt:
        sig_name = "EscStsToDmcEscModeToDmcFrnt"
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
        sig_value_table = {'EscModeToDmc_Off': 0, 'EscModeToDmc_Rpm': 1, 'EscModeToDmc_Tq': 2, 'EscModeToDmc_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 119
        byte = 14
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class PropAxleTqMax_UB:
        sig_name = "PropAxleTqMax_UB"
        sig_start_bit = 196
        update_id_bit = 196
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
        startbit = 196
        byte = 24
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class BrkRgnTqReqQf1:
        sig_name = "BrkRgnTqReqQf1"
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
        sig_value_table = {'Qf1_DevOfDataUndefd': 0, 'Qf1_DataTmpUndefdAndEvlnInProgs': 1, 'Qf1_DevOfDataNotWithinRngAllwd': 2, 'Qf1_DataCalcdWithDevDefd': 3}
        compute_method = None
        length = 2
        startbit = 37
        byte = 4
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class EscStsToDmcChks:
        sig_name = "EscStsToDmcChks"
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

    class EscStsToDmcEscModeToDmcRe:
        sig_name = "EscStsToDmcEscModeToDmcRe"
        sig_start_bit = 117
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EscModeToDmc_Off': 0, 'EscModeToDmc_Rpm': 1, 'EscModeToDmc_Tq': 2, 'EscModeToDmc_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 117
        byte = 14
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class BrkRgnTqReqCntr:
        sig_name = "BrkRgnTqReqCntr"
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

    class EscVariantToDmcChks:
        sig_name = "EscVariantToDmcChks"
        sig_start_bit = 167
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
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

    class PropAxleTqMaxCntr:
        sig_name = "PropAxleTqMaxCntr"
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

    class BrkRgnTqReq_UB:
        sig_name = "BrkRgnTqReq_UB"
        sig_start_bit = 72
        update_id_bit = 72
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
        startbit = 72
        byte = 9
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class EscStsToDmc_UB:
        sig_name = "EscStsToDmc_UB"
        sig_start_bit = 152
        update_id_bit = 152
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
        startbit = 152
        byte = 19
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class WhlSpdReLeQf:
        sig_name = "WhlSpdReLeQf"
        sig_start_bit = 343
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
        startbit = 343
        byte = 42
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class WhlSpdReCntr:
        sig_name = "WhlSpdReCntr"
        sig_start_bit = 339
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
        startbit = 339
        byte = 42
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class PropAxleTqMaxChks:
        sig_name = "PropAxleTqMaxChks"
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

    class PropAxleTqMaxRe:
        sig_name = "PropAxleTqMaxRe"
        sig_start_bit = 223
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = -20000
        sig_value_max = 20000
        sig_byteorder = "Motorola"
        sig_value_init = 20000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 223
        bmuws_info = [(27, 0b11111111, 0b00000000, 8, 0), (28, 0b11111111, 0b00000000, 8, 0)]

    class EscStsToDmcCntr:
        sig_name = "EscStsToDmcCntr"
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

    class BrkSysStPrimBrkSysSts:
        sig_name = "BrkSysStPrimBrkSysSts"
        sig_start_bit = 95
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
        startbit = 95
        byte = 11
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class WhlSpdFrntRiQf:
        sig_name = "WhlSpdFrntRiQf"
        sig_start_bit = 293
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
        startbit = 293
        byte = 36
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class WhlSpdFrntLeQf:
        sig_name = "WhlSpdFrntLeQf"
        sig_start_bit = 295
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
        startbit = 295
        byte = 36
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class BrkMstCtrlModeReqChks:
        sig_name = "BrkMstCtrlModeReqChks"
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

    class WhlSpdFrntChks:
        sig_name = "WhlSpdFrntChks"
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

    class BrkMstCtrlModeReqCntr:
        sig_name = "BrkMstCtrlModeReqCntr"
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

    class BrkSysStPrimChks:
        sig_name = "BrkSysStPrimChks"
        sig_start_bit = 87
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 87
        byte = 10
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class WhlSpdFrnt_UB:
        sig_name = "WhlSpdFrnt_UB"
        sig_start_bit = 320
        update_id_bit = 320
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
        startbit = 320
        byte = 40
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class PropAxleTqMaxFrnt:
        sig_name = "PropAxleTqMaxFrnt"
        sig_start_bit = 207
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = -20000
        sig_value_max = 20000
        sig_byteorder = "Motorola"
        sig_value_init = 20000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 207
        bmuws_info = [(25, 0b11111111, 0b00000000, 8, 0), (26, 0b11111111, 0b00000000, 8, 0)]

    class PropAxleTqMinCntr:
        sig_name = "PropAxleTqMinCntr"
        sig_start_bit = 243
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
        startbit = 243
        byte = 30
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class WhlSpdFrntCntr:
        sig_name = "WhlSpdFrntCntr"
        sig_start_bit = 291
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
        startbit = 291
        byte = 36
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class BrkSysStPrim_UB:
        sig_name = "BrkSysStPrim_UB"
        sig_start_bit = 96
        update_id_bit = 96
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
        startbit = 96
        byte = 12
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class BrkSysStPrimCntr:
        sig_name = "BrkSysStPrimCntr"
        sig_start_bit = 91
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
        startbit = 91
        byte = 11
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class EscStsToDmcTarSpdFrnt:
        sig_name = "EscStsToDmcTarSpdFrnt"
        sig_start_bit = 127
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
        startbit = 127
        bmuws_info = [(15, 0b11111111, 0b00000000, 8, 0), (16, 0b11111111, 0b00000000, 8, 0)]

    class EscVariantToDmc_UB:
        sig_name = "EscVariantToDmc_UB"
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

    class PropAxleTqMinRe:
        sig_name = "PropAxleTqMinRe"
        sig_start_bit = 271
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = -20000
        sig_value_max = 20000
        sig_byteorder = "Motorola"
        sig_value_init = -20000.0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 271
        bmuws_info = [(33, 0b11111111, 0b00000000, 8, 0), (34, 0b11111111, 0b00000000, 8, 0)]

    class WhlSpdFrntRiSpd:
        sig_name = "WhlSpdFrntRiSpd"
        sig_start_bit = 319
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 0.00391
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 31970
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 319
        bmuws_info = [(39, 0b11111111, 0b00000000, 8, 0), (40, 0b11111110, 0b00000001, 7, 1)]


class MGMPropulsionCANFDNmFr:
    msg_name = "MGMPropulsionCANFDNmFr"
    msg_id = 1289
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "MGM"
    rx_nodes = ['IEM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class MGMPropulsionCANFDFr04:
    msg_name = "MGMPropulsionCANFDFr04"
    msg_id = 387
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 16
    tx_node = "MGM"
    rx_nodes = ['VCU', 'CCUMCUCD']
    sig_group_dict = {'ImobChkMGM': ['ImobChkMGMChks', 'ImobChkMGMCntr', 'ImobChkMGMImobChkSts', 'ImobChkMGMImobDateChk0', 'ImobChkMGMImobDateChk1', 'ImobChkMGMImobDateChk2', 'ImobChkMGMImobDateChk3', 'ImobChkMGMImobDateChk4', 'ImobChkMGMImobDateChk5'], 'FrntMotOilPmpPwrSplyU': ['FrntMotOilPmpPwrSplyUMotOilPmpPwrSplyU', 'FrntMotOilPmpPwrSplyUQf']}
    sig_group_dataid_dict = {}

    class FrntMotOilPmpPwrSplyUMotOilPmpPwrSplyU:
        sig_name = "FrntMotOilPmpPwrSplyUMotOilPmpPwrSplyU"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 9
        sig_value_factor = 0.025
        sig_value_offset = 5
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 280
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b10000000, 0b01111111, 1, 7)]

    class ImobChkMGM_UB:
        sig_name = "ImobChkMGM_UB"
        sig_start_bit = 78
        update_id_bit = 78
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
        startbit = 78
        byte = 9
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class FrntMotOilPmpPwrSplyU_UB:
        sig_name = "FrntMotOilPmpPwrSplyU_UB"
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

    class ImobChkMGMImobDateChk0:
        sig_name = "ImobChkMGMImobDateChk0"
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

    class ImobChkMGMImobDateChk4:
        sig_name = "ImobChkMGMImobDateChk4"
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

    class ImobChkMGMImobChkSts:
        sig_name = "ImobChkMGMImobChkSts"
        sig_start_bit = 79
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AvlSts1_Avl': 0, 'AvlSts1_NotAvl': 1}
        compute_method = None
        length = 1
        startbit = 79
        byte = 9
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ImobChkMGMImobDateChk3:
        sig_name = "ImobChkMGMImobDateChk3"
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

    class ImobChkMGMImobDateChk5:
        sig_name = "ImobChkMGMImobDateChk5"
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

    class ImobChkMGMCntr:
        sig_name = "ImobChkMGMCntr"
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

    class ImobChkMGMImobDateChk1:
        sig_name = "ImobChkMGMImobDateChk1"
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

    class FrntMotOilPmpPwrSplyUQf:
        sig_name = "FrntMotOilPmpPwrSplyUQf"
        sig_start_bit = 14
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
        startbit = 14
        byte = 1
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class ImobChkMGMImobDateChk2:
        sig_name = "ImobChkMGMImobDateChk2"
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

    class ImobStsMGM:
        sig_name = "ImobStsMGM"
        sig_start_bit = 77
        update_id_bit = 75
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ImobSts_Undefd': 0, 'ImobSts_ImobNotPass': 1, 'ImobSts_ImobPass': 2, 'ImobSts_ImobRemPass': 3}
        compute_method = None
        length = 2
        startbit = 77
        byte = 9
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class ImobChkMGMChks:
        sig_name = "ImobChkMGMChks"
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


class CCUMCUCDPropulsionCANFDFr06:
    msg_name = "CCUMCUCDPropulsionCANFDFr06"
    msg_id = 576
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.08
    msg_length = 1
    tx_node = "CCUMCUCD"
    rx_nodes = ['EGSM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class DayOrNightSts:
        sig_name = "DayOrNightSts"
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
        sig_value_table = {'DayOrNightSts_Night': 0, 'DayOrNightSts_Day': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7


class BECMPropulsionCANFDFr08:
    msg_name = "BECMPropulsionCANFDFr08"
    msg_id = 16
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 48
    tx_node = "BECM"
    rx_nodes = ['CCUMCUCD']
    sig_group_dict = {'HVBattDevelpSignalGroup4': ['HVBattDevelpSignalGroup4DevelpSignalGroup1', 'HVBattDevelpSignalGroup4DevelpSignalGroup2', 'HVBattDevelpSignalGroup4DevelpSignalGroup3', 'HVBattDevelpSignalGroup4DevelpSignalGroup4', 'HVBattDevelpSignalGroup4DevelpSignalGroup5', 'HVBattDevelpSignalGroup4DevelpSignalGroup6', 'HVBattDevelpSignalGroup4DevelpSignalGroup7', 'HVBattDevelpSignalGroup4DevelpSignalGroup8'], 'HVBattDevelpSignalGroup1': ['HVBattDevelpSignalGroup1DevelpSignalGroup1', 'HVBattDevelpSignalGroup1DevelpSignalGroup2', 'HVBattDevelpSignalGroup1DevelpSignalGroup3', 'HVBattDevelpSignalGroup1DevelpSignalGroup4', 'HVBattDevelpSignalGroup1DevelpSignalGroup5', 'HVBattDevelpSignalGroup1DevelpSignalGroup6', 'HVBattDevelpSignalGroup1DevelpSignalGroup7', 'HVBattDevelpSignalGroup1DevelpSignalGroup8'], 'HVBattDevelpSignalGroup2': ['HVBattDevelpSignalGroup2DevelpSignalGroup1', 'HVBattDevelpSignalGroup2DevelpSignalGroup2', 'HVBattDevelpSignalGroup2DevelpSignalGroup3', 'HVBattDevelpSignalGroup2DevelpSignalGroup4', 'HVBattDevelpSignalGroup2DevelpSignalGroup5', 'HVBattDevelpSignalGroup2DevelpSignalGroup6', 'HVBattDevelpSignalGroup2DevelpSignalGroup7', 'HVBattDevelpSignalGroup2DevelpSignalGroup8'], 'HVBattDevelpSignalGroup3': ['HVBattDevelpSignalGroup3DevelpSignalGroup1', 'HVBattDevelpSignalGroup3DevelpSignalGroup2', 'HVBattDevelpSignalGroup3DevelpSignalGroup3', 'HVBattDevelpSignalGroup3DevelpSignalGroup4', 'HVBattDevelpSignalGroup3DevelpSignalGroup5', 'HVBattDevelpSignalGroup3DevelpSignalGroup6', 'HVBattDevelpSignalGroup3DevelpSignalGroup7', 'HVBattDevelpSignalGroup3DevelpSignalGroup8']}
    sig_group_dataid_dict = {}

    class HVBattDevelpSignalGroup4DevelpSignalGroup8:
        sig_name = "HVBattDevelpSignalGroup4DevelpSignalGroup8"
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

    class HVBattDevelpSignalGroup1DevelpSignalGroup3:
        sig_name = "HVBattDevelpSignalGroup1DevelpSignalGroup3"
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

    class HVBattDevelpSignalGroup2DevelpSignalGroup8:
        sig_name = "HVBattDevelpSignalGroup2DevelpSignalGroup8"
        sig_start_bit = 135
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 135
        byte = 16
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HVBattDevelpSignalGroup3DevelpSignalGroup1:
        sig_name = "HVBattDevelpSignalGroup3DevelpSignalGroup1"
        sig_start_bit = 151
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 151
        byte = 18
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HVBattDevelpSignalGroup2DevelpSignalGroup7:
        sig_name = "HVBattDevelpSignalGroup2DevelpSignalGroup7"
        sig_start_bit = 127
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 127
        byte = 15
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HVBattDevelpSignalGroup2DevelpSignalGroup2:
        sig_name = "HVBattDevelpSignalGroup2DevelpSignalGroup2"
        sig_start_bit = 87
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 87
        byte = 10
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HVBattDevelpSignalGroup2DevelpSignalGroup3:
        sig_name = "HVBattDevelpSignalGroup2DevelpSignalGroup3"
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

    class HVBattDevelpSignalGroup3DevelpSignalGroup7:
        sig_name = "HVBattDevelpSignalGroup3DevelpSignalGroup7"
        sig_start_bit = 199
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
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

    class HVBattDevelpSignalGroup4DevelpSignalGroup4:
        sig_name = "HVBattDevelpSignalGroup4DevelpSignalGroup4"
        sig_start_bit = 247
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 247
        byte = 30
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HVBattDevelpSignalGroup4DevelpSignalGroup2:
        sig_name = "HVBattDevelpSignalGroup4DevelpSignalGroup2"
        sig_start_bit = 231
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 231
        byte = 28
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HVBattDevelpSignalGroup1DevelpSignalGroup5:
        sig_name = "HVBattDevelpSignalGroup1DevelpSignalGroup5"
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

    class HVBattDevelpSignalGroup1DevelpSignalGroup4:
        sig_name = "HVBattDevelpSignalGroup1DevelpSignalGroup4"
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

    class HVBattDevelpSignalGroup4DevelpSignalGroup5:
        sig_name = "HVBattDevelpSignalGroup4DevelpSignalGroup5"
        sig_start_bit = 255
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 255
        byte = 31
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HVBattDevelpSignalGroup2DevelpSignalGroup6:
        sig_name = "HVBattDevelpSignalGroup2DevelpSignalGroup6"
        sig_start_bit = 119
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 119
        byte = 14
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HVBattDevelpSignalGroup3DevelpSignalGroup3:
        sig_name = "HVBattDevelpSignalGroup3DevelpSignalGroup3"
        sig_start_bit = 167
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
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

    class HVBattDevelpSignalGroup4DevelpSignalGroup1:
        sig_name = "HVBattDevelpSignalGroup4DevelpSignalGroup1"
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

    class HVBattDevelpSignalGroup4_UB:
        sig_name = "HVBattDevelpSignalGroup4_UB"
        sig_start_bit = 287
        update_id_bit = 287
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
        startbit = 287
        byte = 35
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class HVBattDevelpSignalGroup2DevelpSignalGroup5:
        sig_name = "HVBattDevelpSignalGroup2DevelpSignalGroup5"
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

    class HVBattDevelpSignalGroup4DevelpSignalGroup3:
        sig_name = "HVBattDevelpSignalGroup4DevelpSignalGroup3"
        sig_start_bit = 239
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 239
        byte = 29
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HVBattDevelpSignalGroup3DevelpSignalGroup6:
        sig_name = "HVBattDevelpSignalGroup3DevelpSignalGroup6"
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

    class HVBattDevelpSignalGroup1DevelpSignalGroup1:
        sig_name = "HVBattDevelpSignalGroup1DevelpSignalGroup1"
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

    class HVBattDevelpSignalGroup4DevelpSignalGroup7:
        sig_name = "HVBattDevelpSignalGroup4DevelpSignalGroup7"
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

    class HVBattDevelpSignalGroup3DevelpSignalGroup2:
        sig_name = "HVBattDevelpSignalGroup3DevelpSignalGroup2"
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

    class HVBattDevelpSignalGroup1_UB:
        sig_name = "HVBattDevelpSignalGroup1_UB"
        sig_start_bit = 71
        update_id_bit = 71
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
        startbit = 71
        byte = 8
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class HVBattDevelpSignalGroup3DevelpSignalGroup5:
        sig_name = "HVBattDevelpSignalGroup3DevelpSignalGroup5"
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

    class HVBattDevelpSignalGroup2_UB:
        sig_name = "HVBattDevelpSignalGroup2_UB"
        sig_start_bit = 143
        update_id_bit = 143
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
        startbit = 143
        byte = 17
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class HVBattDevelpSignalGroup2DevelpSignalGroup4:
        sig_name = "HVBattDevelpSignalGroup2DevelpSignalGroup4"
        sig_start_bit = 103
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
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

    class HVBattDevelpSignalGroup1DevelpSignalGroup6:
        sig_name = "HVBattDevelpSignalGroup1DevelpSignalGroup6"
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

    class HVBattDevelpSignalGroup1DevelpSignalGroup7:
        sig_name = "HVBattDevelpSignalGroup1DevelpSignalGroup7"
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

    class HVBattDevelpSignalGroup1DevelpSignalGroup2:
        sig_name = "HVBattDevelpSignalGroup1DevelpSignalGroup2"
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

    class HVBattDevelpSignalGroup3DevelpSignalGroup4:
        sig_name = "HVBattDevelpSignalGroup3DevelpSignalGroup4"
        sig_start_bit = 175
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
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

    class HVBattDevelpSignalGroup3_UB:
        sig_name = "HVBattDevelpSignalGroup3_UB"
        sig_start_bit = 215
        update_id_bit = 215
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
        startbit = 215
        byte = 26
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class HVBattDevelpSignalGroup3DevelpSignalGroup8:
        sig_name = "HVBattDevelpSignalGroup3DevelpSignalGroup8"
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

    class HVBattDevelpSignalGroup2DevelpSignalGroup1:
        sig_name = "HVBattDevelpSignalGroup2DevelpSignalGroup1"
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

    class HVBattDevelpSignalGroup1DevelpSignalGroup8:
        sig_name = "HVBattDevelpSignalGroup1DevelpSignalGroup8"
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

    class HVBattDevelpSignalGroup4DevelpSignalGroup6:
        sig_name = "HVBattDevelpSignalGroup4DevelpSignalGroup6"
        sig_start_bit = 263
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 263
        byte = 32
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class VCUPropulsionCANFDFr05:
    msg_name = "VCUPropulsionCANFDFr05"
    msg_id = 281
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.03
    msg_length = 8
    tx_node = "VCU"
    rx_nodes = ['BECM', 'CCUMCUCD', 'ETC']
    sig_group_dict = {'ChrgnEquipAct': ['ChrgnEquipActI', 'ChrgnEquipActU']}
    sig_group_dataid_dict = {}

    class ChrgnEquipActU:
        sig_name = "ChrgnEquipActU"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 0.1
        sig_value_offset = 0
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

    class ChrgnEquipAct_UB:
        sig_name = "ChrgnEquipAct_UB"
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

    class ChrgnEquipActI:
        sig_name = "ChrgnEquipActI"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 0.1
        sig_value_offset = -3000.0
        sig_value_min = 0
        sig_value_max = 65535
        sig_byteorder = "Motorola"
        sig_value_init = 30000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class HMIBattTracFailrIndcnReq:
        sig_name = "HMIBattTracFailrIndcnReq"
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
        sig_value_table = {'ReqSts2_Default': 0, 'ReqSts2_NotReqd': 1, 'ReqSts2_Reqd': 2, 'ReqSts2_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 37
        byte = 4
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4


class BECMPropulsionCANFDNmFr:
    msg_name = "BECMPropulsionCANFDNmFr"
    msg_id = 1286
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BECM"
    rx_nodes = ['BCU2']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class IEMPropulsionCANFDFr01:
    msg_name = "IEMPropulsionCANFDFr01"
    msg_id = 67
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 48
    tx_node = "IEM"
    rx_nodes = ['VCU', 'ETC', 'CCUMCUCD', 'CCUMCUAD', 'BCU1']
    sig_group_dict = {'ReMotTqAct': ['ReMotTqActChks', 'ReMotTqActCntr', 'ReMotTqActTq', 'ReMotTqActTqQf'], 'ReMotSpdActSafe': ['ReMotSpdActSafeChks', 'ReMotSpdActSafeCntr', 'ReMotSpdActSafeMotorSpdActSafe', 'ReMotSpdActSafeQf'], 'ReMotTqAvl': ['ReMotTqAvlHVMotorTqAvlMax', 'ReMotTqAvlHVMotorTqAvlMin'], 'DmcStsRe': ['DmcStsReChks', 'DmcStsReCntr', 'DmcStsReDmcSt', 'DmcStsReDmcSwInfo', 'DmcStsReDmcTarTq']}
    sig_group_dataid_dict = {'ReMotTqAct': 1064, 'ReMotSpdActSafe': 1017}

    class ReMotTqAvlHVMotorTqAvlMax:
        sig_name = "ReMotTqAvlHVMotorTqAvlMax"
        sig_start_bit = 151
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 4
        sig_value_offset = -8188.0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 2047
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 151
        bmuws_info = [(18, 0b11111111, 0b00000000, 8, 0), (19, 0b11110000, 0b00001111, 4, 4)]

    class ReMotTqAvlHVMotorTqAvlMin:
        sig_name = "ReMotTqAvlHVMotorTqAvlMin"
        sig_start_bit = 155
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 4
        sig_value_offset = -8188.0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 2047
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 155
        bmuws_info = [(19, 0b00001111, 0b11110000, 4, 0), (20, 0b11111111, 0b00000000, 8, 0)]

    class ReMotTqActCntr:
        sig_name = "ReMotTqActCntr"
        sig_start_bit = 123
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
        startbit = 123
        byte = 15
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class ReMotTqActTq:
        sig_name = "ReMotTqActTq"
        sig_start_bit = 135
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 1
        sig_value_offset = -15000.0
        sig_value_min = 0
        sig_value_max = 32767
        sig_byteorder = "Motorola"
        sig_value_init = 15000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 135
        bmuws_info = [(16, 0b11111111, 0b00000000, 8, 0), (17, 0b11111110, 0b00000001, 7, 1)]

    class ReMotModSts:
        sig_name = "ReMotModSts"
        sig_start_bit = 51
        update_id_bit = 79
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'MotModSts_Inin': 0, 'MotModSts_MonChk': 1, 'MotModSts_Stb': 2, 'MotModSts_PreChrg': 3, 'MotModSts_HVReady': 4, 'MotModSts_TqCtrl': 5, 'MotModSts_PwrDwn': 6, 'MotModSts_Flt': 7, 'MotModSts_TCSCtrl': 8, 'MotModSts_DTCSCtrl': 9, 'MotModSts_ActiveDsicharge': 10, 'MotModSts_PassiveDsicharge': 11, 'MotModSts_ActiveHeat': 12, 'MotModSts_Boost': 13, 'MotModSts_PulseHeat': 14, 'MotModSts_SpdCtrl': 15}
        compute_method = None
        length = 4
        startbit = 51
        byte = 6
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class ReMotSpdAct:
        sig_name = "ReMotSpdAct"
        sig_start_bit = 63
        update_id_bit = 78
        sig_length = 16
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = -32768
        sig_value_max = 32767
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 63
        bmuws_info = [(7, 0b11111111, 0b00000000, 8, 0), (8, 0b11111111, 0b00000000, 8, 0)]

    class DmcStsReChks:
        sig_name = "DmcStsReChks"
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

    class ReMotTqActTqQf:
        sig_name = "ReMotTqActTqQf"
        sig_start_bit = 127
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
        startbit = 127
        byte = 15
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class DmcStsReDmcSwInfo:
        sig_name = "DmcStsReDmcSwInfo"
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

    class ReMotTqAct_UB:
        sig_name = "ReMotTqAct_UB"
        sig_start_bit = 124
        update_id_bit = 124
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
        startbit = 124
        byte = 15
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class ReMotTqActChks:
        sig_name = "ReMotTqActChks"
        sig_start_bit = 119
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 119
        byte = 14
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ReMotSpdActSafe_UB:
        sig_name = "ReMotSpdActSafe_UB"
        sig_start_bit = 92
        update_id_bit = 92
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
        startbit = 92
        byte = 11
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class DmcStsReCntr:
        sig_name = "DmcStsReCntr"
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

    class ReMotSpdActSafeChks:
        sig_name = "ReMotSpdActSafeChks"
        sig_start_bit = 87
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 87
        byte = 10
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ReMotTqAvl_UB:
        sig_name = "ReMotTqAvl_UB"
        sig_start_bit = 136
        update_id_bit = 136
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
        startbit = 136
        byte = 17
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ReMotDampgModSts:
        sig_name = "ReMotDampgModSts"
        sig_start_bit = 54
        update_id_bit = 52
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'MotDampgMod_NoDampg': 0, 'MotDampgMod_LoDampg': 1, 'MotDampgMod_MeDampg': 2, 'MotDampgMod_HiDampg': 3}
        compute_method = None
        length = 2
        startbit = 54
        byte = 6
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class ReMotSpdActSafeCntr:
        sig_name = "ReMotSpdActSafeCntr"
        sig_start_bit = 91
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
        startbit = 91
        byte = 11
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class ReMotSpdActSafeMotorSpdActSafe:
        sig_name = "ReMotSpdActSafeMotorSpdActSafe"
        sig_start_bit = 103
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = -32768
        sig_value_max = 32767
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 103
        bmuws_info = [(12, 0b11111111, 0b00000000, 8, 0), (13, 0b11111111, 0b00000000, 8, 0)]

    class DmcStsRe_UB:
        sig_name = "DmcStsRe_UB"
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

    class ReMotSpdActSafeQf:
        sig_name = "ReMotSpdActSafeQf"
        sig_start_bit = 95
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
        startbit = 95
        byte = 11
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class DmcStsReDmcSt:
        sig_name = "DmcStsReDmcSt"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DmcSt_Init': 0, 'DmcSt_On': 1, 'DmcSt_Off': 2, 'DmcSt_Fault': 3}
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DmcStsReDmcTarTq:
        sig_name = "DmcStsReDmcTarTq"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = -30000
        sig_value_max = 30000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0)]


class VCUPropulsionCANFDFr01:
    msg_name = "VCUPropulsionCANFDFr01"
    msg_id = 70
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 64
    tx_node = "VCU"
    rx_nodes = ['ETC', 'CCUMCUCD', 'ODP', 'MGM', 'EGSM', 'IEM', 'BECM', 'BCU2', 'CCUMCUAD', 'BCU1']
    sig_group_dict = {'PtSysTotBrkTqReqFromEPedl': ['PtSysTotBrkTqReqFromEPedlBrkTqReq', 'PtSysTotBrkTqReqFromEPedlBrkTqReqOnOff'], 'PtBrkTqRgnAtAxleReAct': ['PtBrkTqRgnAtAxleReActTq', 'PtBrkTqRgnAtAxleReActTqQf'], 'PropSysSt': ['PropSysStCapibility', 'PropSysStChks', 'PropSysStCntr', 'PropSysStCtrlSts', 'PropSysStDegrad', 'PropSysStModCfmd'], 'PtSysRgnTarTqReAxle': ['PtSysRgnTarTqReAxleTq', 'PtSysRgnTarTqReAxleTqQf'], 'PtBrkTqTotCp': ['PtBrkTqTotCpTq', 'PtBrkTqTotCpTqQf'], 'PtSysTotRgnTqReq': ['PtSysTotRgnTqReqTq', 'PtSysTotRgnTqReqTqQf'], 'PtBrkTqActTot': ['PtBrkTqActTotTq', 'PtBrkTqActTotTqQf'], 'GearLvrIndcnReal': ['GearLvrIndcnRealChks', 'GearLvrIndcnRealCntr', 'GearLvrIndcnRealGearLvrIndcn'], 'PrpsnSysModSts': ['PrpsnSysModStsChks', 'PrpsnSysModStsCntr', 'PrpsnSysModStsPrpsnModSt'], 'AccrPedlVal': ['AccrPedlValChks', 'AccrPedlValCntr', 'AccrPedlValPedlFild'], 'AccrPedlPsd': ['AccrPedlPsdAccrPedlPsd', 'AccrPedlPsdChks', 'AccrPedlPsdCntr', 'AccrPedlPsdSafe'], 'DrvrDesDir': ['DrvrDesDirChks', 'DrvrDesDirCntr', 'DrvrDesDirDrvrDesDir']}
    sig_group_dataid_dict = {'GearLvrIndcnReal': 1065, 'PrpsnSysModSts': 1004, 'DrvrDesDir': 1000}

    class PtSysTotBrkTqReqFromEPedl_UB:
        sig_name = "PtSysTotBrkTqReqFromEPedl_UB"
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

    class ReMotDampgModReq:
        sig_name = "ReMotDampgModReq"
        sig_start_bit = 293
        update_id_bit = 303
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'MotDampgMod_NoDampg': 0, 'MotDampgMod_LoDampg': 1, 'MotDampgMod_MeDampg': 2, 'MotDampgMod_HiDampg': 3}
        compute_method = None
        length = 2
        startbit = 293
        byte = 36
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class AccrPedlValChks:
        sig_name = "AccrPedlValChks"
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

    class PtSysRgnTarTqReAxleTq:
        sig_name = "PtSysRgnTarTqReAxleTq"
        sig_start_bit = 279
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 1
        sig_value_offset = -15000.0
        sig_value_min = 0
        sig_value_max = 32767
        sig_byteorder = "Motorola"
        sig_value_init = 15000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 279
        bmuws_info = [(34, 0b11111111, 0b00000000, 8, 0), (35, 0b11111110, 0b00000001, 7, 1)]

    class FrntMotModReq:
        sig_name = "FrntMotModReq"
        sig_start_bit = 151
        update_id_bit = 167
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'MotModSts_Inin': 0, 'MotModSts_MonChk': 1, 'MotModSts_Stb': 2, 'MotModSts_PreChrg': 3, 'MotModSts_HVReady': 4, 'MotModSts_TqCtrl': 5, 'MotModSts_PwrDwn': 6, 'MotModSts_Flt': 7, 'MotModSts_TCSCtrl': 8, 'MotModSts_DTCSCtrl': 9, 'MotModSts_ActiveDsicharge': 10, 'MotModSts_PassiveDsicharge': 11, 'MotModSts_ActiveHeat': 12, 'MotModSts_Boost': 13, 'MotModSts_PulseHeat': 14, 'MotModSts_SpdCtrl': 15}
        compute_method = None
        length = 4
        startbit = 151
        byte = 18
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class PrpsnTqReAxleReq:
        sig_name = "PrpsnTqReAxleReq"
        sig_start_bit = 263
        update_id_bit = 264
        sig_length = 15
        sig_value_factor = 1
        sig_value_offset = -15000.0
        sig_value_min = 0
        sig_value_max = 32767
        sig_byteorder = "Motorola"
        sig_value_init = 15000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 263
        bmuws_info = [(32, 0b11111111, 0b00000000, 8, 0), (33, 0b11111110, 0b00000001, 7, 1)]

    class FrntMotDampgModReq:
        sig_name = "FrntMotDampgModReq"
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
        sig_value_table = {'MotDampgMod_NoDampg': 0, 'MotDampgMod_LoDampg': 1, 'MotDampgMod_MeDampg': 2, 'MotDampgMod_HiDampg': 3}
        compute_method = None
        length = 2
        startbit = 22
        byte = 2
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class GearLvrIndcnRealGearLvrIndcn:
        sig_name = "GearLvrIndcnRealGearLvrIndcn"
        sig_start_bit = 455
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 7
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GearLvrIndcn_Default': 0, 'GearLvrIndcn_P': 1, 'GearLvrIndcn_R': 2, 'GearLvrIndcn_N': 3, 'GearLvrIndcn_D': 4, 'GearLvrIndcn_Reserved1': 5, 'GearLvrIndcn_Reserved2': 6, 'GearLvrIndcn_Undefd': 7}
        compute_method = None
        length = 3
        startbit = 455
        byte = 56
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DrvrDesDirChks:
        sig_name = "DrvrDesDirChks"
        sig_start_bit = 135
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 135
        byte = 16
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class PtBrkTqRgnAtAxleReAct_UB:
        sig_name = "PtBrkTqRgnAtAxleReAct_UB"
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

    class GearShiftByDrvr:
        sig_name = "GearShiftByDrvr"
        sig_start_bit = 190
        update_id_bit = 175
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GearLvrIndcn_Default': 0, 'GearLvrIndcn_P': 1, 'GearLvrIndcn_R': 2, 'GearLvrIndcn_N': 3, 'GearLvrIndcn_D': 4, 'GearLvrIndcn_Reserved1': 5, 'GearLvrIndcn_Reserved2': 6, 'GearLvrIndcn_Undefd': 7}
        compute_method = None
        length = 3
        startbit = 190
        byte = 23
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class PtBrkTqRgnAtAxleReActTq:
        sig_name = "PtBrkTqRgnAtAxleReActTq"
        sig_start_bit = 407
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 1
        sig_value_offset = -15000.0
        sig_value_min = 0
        sig_value_max = 32767
        sig_byteorder = "Motorola"
        sig_value_init = 15000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 407
        bmuws_info = [(50, 0b11111111, 0b00000000, 8, 0), (51, 0b11111110, 0b00000001, 7, 1)]

    class AccrPedlValPedlFild:
        sig_name = "AccrPedlValPedlFild"
        sig_start_bit = 43
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 0.00390625
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 32767
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 43
        bmuws_info = [(5, 0b00001111, 0b11110000, 4, 0), (6, 0b11111111, 0b00000000, 8, 0), (7, 0b11100000, 0b00011111, 3, 5)]

    class PropSysSt_UB:
        sig_name = "PropSysSt_UB"
        sig_start_bit = 204
        update_id_bit = 204
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
        startbit = 204
        byte = 25
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class StandStillReqForEPedl:
        sig_name = "StandStillReqForEPedl"
        sig_start_bit = 319
        update_id_bit = 318
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
        startbit = 319
        byte = 39
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class PrpnSysStrtDlyInhbMsg:
        sig_name = "PrpnSysStrtDlyInhbMsg"
        sig_start_bit = 222
        update_id_bit = 216
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 6
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PrpnSysStrtMsg_NoInhb': 0, 'PrpnSysStrtMsg_StrtDly': 1, 'PrpnSysStrtMsg_InhbRemStrt': 2, 'PrpnSysStrtMsg_DiRemStrt': 3, 'PrpnSysStrtMsg_SelParkOrNeut': 4, 'PrpnSysStrtMsg_Resd1': 5, 'PrpnSysStrtMsg_Resd2': 6}
        compute_method = None
        length = 3
        startbit = 222
        byte = 27
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class DrvrDesDirDrvrDesDir:
        sig_name = "DrvrDesDirDrvrDesDir"
        sig_start_bit = 143
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DrvrDesDir_Undefd': 0, 'DrvrDesDir_Fwd': 1, 'DrvrDesDir_Rvs': 2, 'DrvrDesDir_Neut': 3, 'DrvrDesDir_Resd1': 4, 'DrvrDesDir_Resd2': 5, 'DrvrDesDir_Resd3': 6, 'DrvrDesDir_Resd4': 7}
        compute_method = None
        length = 3
        startbit = 143
        byte = 17
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class EgyRgnLimTqCmpReq:
        sig_name = "EgyRgnLimTqCmpReq"
        sig_start_bit = 119
        update_id_bit = 120
        sig_length = 15
        sig_value_factor = 1
        sig_value_offset = -15000.0
        sig_value_min = 0
        sig_value_max = 32767
        sig_byteorder = "Motorola"
        sig_value_init = 15000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 119
        bmuws_info = [(14, 0b11111111, 0b00000000, 8, 0), (15, 0b11111110, 0b00000001, 7, 1)]

    class PtSysTotRgnTqReqTqQf:
        sig_name = "PtSysTotRgnTqReqTqQf"
        sig_start_bit = 342
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
        startbit = 342
        byte = 42
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class PtSysRgnTarTqReAxle_UB:
        sig_name = "PtSysRgnTarTqReAxle_UB"
        sig_start_bit = 280
        update_id_bit = 280
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
        startbit = 280
        byte = 35
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class PtBrkTqTotCp_UB:
        sig_name = "PtBrkTqTotCp_UB"
        sig_start_bit = 432
        update_id_bit = 432
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
        startbit = 432
        byte = 54
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class OvrdByDrvr:
        sig_name = "OvrdByDrvr"
        sig_start_bit = 177
        update_id_bit = 191
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OffOnNoCmd_NoCmd': 0, 'OffOnNoCmd_Off': 1, 'OffOnNoCmd_On': 2}
        compute_method = None
        length = 2
        startbit = 177
        byte = 22
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class GearLvrIndcnRealCntr:
        sig_name = "GearLvrIndcnRealCntr"
        sig_start_bit = 451
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
        startbit = 451
        byte = 56
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class ReMotActvDampgGain:
        sig_name = "ReMotActvDampgGain"
        sig_start_bit = 355
        update_id_bit = 356
        sig_length = 8
        sig_value_factor = 0.05
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 355
        bmuws_info = [(44, 0b00001111, 0b11110000, 4, 0), (45, 0b11110000, 0b00001111, 4, 4)]

    class PtSysTotRgnTqReq_UB:
        sig_name = "PtSysTotRgnTqReq_UB"
        sig_start_bit = 340
        update_id_bit = 340
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
        startbit = 340
        byte = 42
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class PropSysStDegrad:
        sig_name = "PropSysStDegrad"
        sig_start_bit = 215
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 13
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BrkAdDegrad_No': 0, 'BrkAdDegrad_Degrade1': 1, 'BrkAdDegrad_Degrade2': 2, 'BrkAdDegrad_Degrade3': 3, 'BrkAdDegrad_Degrade4': 4, 'BrkAdDegrad_Degrade5': 5, 'BrkAdDegrad_Degrade6': 6, 'BrkAdDegrad_Degrade7': 7, 'BrkAdDegrad_Degrade8': 8, 'BrkAdDegrad_Degrade9': 9, 'BrkAdDegrad_Degrade10': 10, 'BrkAdDegrad_Degrade11': 11, 'BrkAdDegrad_Degrade12': 12, 'BrkAdDegrad_Degrade13': 13}
        compute_method = None
        length = 4
        startbit = 215
        byte = 26
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class AccrPedlValDev:
        sig_name = "AccrPedlValDev"
        sig_start_bit = 71
        update_id_bit = 72
        sig_length = 15
        sig_value_factor = 0.0625
        sig_value_offset = 0
        sig_value_min = -16000
        sig_value_max = 16000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 71
        bmuws_info = [(8, 0b11111111, 0b00000000, 8, 0), (9, 0b11111110, 0b00000001, 7, 1)]

    class PtSysRgnTarTqReAxleTqQf:
        sig_name = "PtSysRgnTarTqReAxleTqQf"
        sig_start_bit = 295
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
        startbit = 295
        byte = 36
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class PrpsnSysModStsPrpsnModSt:
        sig_name = "PrpsnSysModStsPrpsnModSt"
        sig_start_bit = 239
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PrpsnSysSts_initialize': 0, 'PrpsnSysSts_Awake': 1, 'PrpsnSysSts_Ready': 2, 'PrpsnSysSts_Standby': 3, 'PrpsnSysSts_Running': 4, 'PrpsnSysSts_AftRun': 5, 'PrpsnSysSts_Reserved1': 6, 'PrpsnSysSts_Reserved2': 7}
        compute_method = None
        length = 3
        startbit = 239
        byte = 29
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class PrpsnSysModStsChks:
        sig_name = "PrpsnSysModStsChks"
        sig_start_bit = 231
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 231
        byte = 28
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CrpTqReq:
        sig_name = "CrpTqReq"
        sig_start_bit = 103
        update_id_bit = 104
        sig_length = 15
        sig_value_factor = 1
        sig_value_offset = -15000.0
        sig_value_min = 0
        sig_value_max = 32767
        sig_byteorder = "Motorola"
        sig_value_init = 15000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 103
        bmuws_info = [(12, 0b11111111, 0b00000000, 8, 0), (13, 0b11111110, 0b00000001, 7, 1)]

    class HVBattPrechrgnReq:
        sig_name = "HVBattPrechrgnReq"
        sig_start_bit = 170
        update_id_bit = 168
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OffOnCmd_NoCmd': 0, 'OffOnCmd_Off': 1, 'OffOnCmd_On': 2}
        compute_method = None
        length = 2
        startbit = 170
        byte = 21
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class PtBrkTqTotCpTqQf:
        sig_name = "PtBrkTqTotCpTqQf"
        sig_start_bit = 417
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
        startbit = 417
        byte = 52
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class PtBrkTqActTot_UB:
        sig_name = "PtBrkTqActTot_UB"
        sig_start_bit = 384
        update_id_bit = 384
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
        startbit = 384
        byte = 48
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class AccrPedlPsdAccrPedlPsd:
        sig_name = "AccrPedlPsdAccrPedlPsd"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoYesInitial_Initial': 0, 'NoYesInitial_No': 1, 'NoYesInitial_Yes': 2}
        compute_method = None
        length = 2
        startbit = 15
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class PropSysStModCfmd:
        sig_name = "PropSysStModCfmd"
        sig_start_bit = 211
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ModCfmd_NoReq': 0, 'ModCfmd_ANP': 1, 'ModCfmd_AVP': 2, 'ModCfmd_ACC': 3, 'ModCfmd_Lcc': 4, 'ModCfmd_Reserved1': 5, 'ModCfmd_Reserved2': 6, 'ModCfmd_Reserved3': 7, 'ModCfmd_Reserved4': 8, 'ModCfmd_Reserved5': 9, 'ModCfmd_Reserved6': 10}
        compute_method = None
        length = 4
        startbit = 211
        byte = 26
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class PtBrkTqRgnAtAxleReActTqQf:
        sig_name = "PtBrkTqRgnAtAxleReActTqQf"
        sig_start_bit = 393
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
        startbit = 393
        byte = 49
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class HVMainRlyReq:
        sig_name = "HVMainRlyReq"
        sig_start_bit = 183
        update_id_bit = 181
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'MainRly1_Open': 0, 'MainRly1_Clsd': 1, 'MainRly1_KeepSt': 2, 'MainRly1_OpenAndReqActvDcha': 3}
        compute_method = None
        length = 2
        startbit = 183
        byte = 22
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class DrvrDesDirCntr:
        sig_name = "DrvrDesDirCntr"
        sig_start_bit = 139
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
        startbit = 139
        byte = 17
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class PrpsnTqFrntAxleReq:
        sig_name = "PrpsnTqFrntAxleReq"
        sig_start_bit = 247
        update_id_bit = 248
        sig_length = 15
        sig_value_factor = 1
        sig_value_offset = -15000.0
        sig_value_min = 0
        sig_value_max = 32767
        sig_byteorder = "Motorola"
        sig_value_init = 15000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 247
        bmuws_info = [(30, 0b11111111, 0b00000000, 8, 0), (31, 0b11111110, 0b00000001, 7, 1)]

    class GearLvrIndcnReal_UB:
        sig_name = "GearLvrIndcnReal_UB"
        sig_start_bit = 452
        update_id_bit = 452
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
        startbit = 452
        byte = 56
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class HvSysActvSts:
        sig_name = "HvSysActvSts"
        sig_start_bit = 180
        update_id_bit = 178
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvSysActvSts_Default': 0, 'HvSysActvSts_CtrldSplyIsActivated': 1, 'HvSysActvSts_CtrldSplyPlusContactorsIsActivated': 2, 'HvSysActvSts_Error': 3}
        compute_method = None
        length = 2
        startbit = 180
        byte = 22
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class GearLvrIndcnRealChks:
        sig_name = "GearLvrIndcnRealChks"
        sig_start_bit = 447
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 447
        byte = 55
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntMotActvDampgGain:
        sig_name = "FrntMotActvDampgGain"
        sig_start_bit = 31
        update_id_bit = 16
        sig_length = 8
        sig_value_factor = 0.05
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

    class FrntMotTqReq:
        sig_name = "FrntMotTqReq"
        sig_start_bit = 147
        update_id_bit = 166
        sig_length = 12
        sig_value_factor = 4
        sig_value_offset = -8188.0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 2047
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 147
        bmuws_info = [(18, 0b00001111, 0b11110000, 4, 0), (19, 0b11111111, 0b00000000, 8, 0)]

    class PrpsnSysModSts_UB:
        sig_name = "PrpsnSysModSts_UB"
        sig_start_bit = 236
        update_id_bit = 236
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
        startbit = 236
        byte = 29
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class AccrPedlVal_UB:
        sig_name = "AccrPedlVal_UB"
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

    class AccrPedlPsd_UB:
        sig_name = "AccrPedlPsd_UB"
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

    class PtSysTotBrkTqReqFromEPedlBrkTqReqOnOff:
        sig_name = "PtSysTotBrkTqReqFromEPedlBrkTqReqOnOff"
        sig_start_bit = 343
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
        startbit = 343
        byte = 42
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class PtEPBReq:
        sig_name = "PtEPBReq"
        sig_start_bit = 219
        update_id_bit = 217
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ReqSts2_Default': 0, 'ReqSts2_NotReqd': 1, 'ReqSts2_Reqd': 2, 'ReqSts2_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 219
        byte = 27
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class AccrPedlTqReq:
        sig_name = "AccrPedlTqReq"
        sig_start_bit = 87
        update_id_bit = 88
        sig_length = 15
        sig_value_factor = 1
        sig_value_offset = -15000.0
        sig_value_min = 0
        sig_value_max = 32767
        sig_byteorder = "Motorola"
        sig_value_init = 15000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 87
        bmuws_info = [(10, 0b11111111, 0b00000000, 8, 0), (11, 0b11111110, 0b00000001, 7, 1)]

    class PropSysStCapibility:
        sig_name = "PropSysStCapibility"
        sig_start_bit = 207
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Sts1_Initial': 0, 'Sts1_Normal': 1, 'Sts1_Fault': 2, 'Sts1_Limited': 3}
        compute_method = None
        length = 3
        startbit = 207
        byte = 25
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class PropSysStCntr:
        sig_name = "PropSysStCntr"
        sig_start_bit = 203
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
        startbit = 203
        byte = 25
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class PtBrkTqActTotTq:
        sig_name = "PtBrkTqActTotTq"
        sig_start_bit = 383
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 1
        sig_value_offset = -15000.0
        sig_value_min = 0
        sig_value_max = 32767
        sig_byteorder = "Motorola"
        sig_value_init = 15000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 383
        bmuws_info = [(47, 0b11111111, 0b00000000, 8, 0), (48, 0b11111110, 0b00000001, 7, 1)]

    class AccrPedlPsdCntr:
        sig_name = "AccrPedlPsdCntr"
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

    class PropSysStChks:
        sig_name = "PropSysStChks"
        sig_start_bit = 199
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
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

    class PtSysTotBrkTqReqFromEPedlBrkTqReq:
        sig_name = "PtSysTotBrkTqReqFromEPedlBrkTqReq"
        sig_start_bit = 327
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 1
        sig_value_offset = -15000.0
        sig_value_min = 0
        sig_value_max = 32767
        sig_byteorder = "Motorola"
        sig_value_init = 15000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 327
        bmuws_info = [(40, 0b11111111, 0b00000000, 8, 0), (41, 0b11111110, 0b00000001, 7, 1)]

    class ReMotModReq:
        sig_name = "ReMotModReq"
        sig_start_bit = 291
        update_id_bit = 302
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'MotModSts_Inin': 0, 'MotModSts_MonChk': 1, 'MotModSts_Stb': 2, 'MotModSts_PreChrg': 3, 'MotModSts_HVReady': 4, 'MotModSts_TqCtrl': 5, 'MotModSts_PwrDwn': 6, 'MotModSts_Flt': 7, 'MotModSts_TCSCtrl': 8, 'MotModSts_DTCSCtrl': 9, 'MotModSts_ActiveDsicharge': 10, 'MotModSts_PassiveDsicharge': 11, 'MotModSts_ActiveHeat': 12, 'MotModSts_Boost': 13, 'MotModSts_PulseHeat': 14, 'MotModSts_SpdCtrl': 15}
        compute_method = None
        length = 4
        startbit = 291
        byte = 36
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class PrpsnSysModStsCntr:
        sig_name = "PrpsnSysModStsCntr"
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

    class PtBrkTqActTotTqQf:
        sig_name = "PtBrkTqActTotTqQf"
        sig_start_bit = 369
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
        startbit = 369
        byte = 46
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class PropSysStCtrlSts:
        sig_name = "PropSysStCtrlSts"
        sig_start_bit = 223
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CtrlSts_Primary': 0, 'CtrlSts_Secondary': 1}
        compute_method = None
        length = 1
        startbit = 223
        byte = 27
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class AccrPedlPsdChks:
        sig_name = "AccrPedlPsdChks"
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

    class PtBrkTqTotCpTq:
        sig_name = "PtBrkTqTotCpTq"
        sig_start_bit = 431
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 1
        sig_value_offset = -15000.0
        sig_value_min = 0
        sig_value_max = 32767
        sig_byteorder = "Motorola"
        sig_value_init = 15000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 431
        bmuws_info = [(53, 0b11111111, 0b00000000, 8, 0), (54, 0b11111110, 0b00000001, 7, 1)]

    class ReMotTqReq:
        sig_name = "ReMotTqReq"
        sig_start_bit = 301
        update_id_bit = 305
        sig_length = 12
        sig_value_factor = 4
        sig_value_offset = -8188.0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 2047
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 301
        bmuws_info = [(37, 0b00111111, 0b11000000, 6, 0), (38, 0b11111100, 0b00000011, 6, 2)]

    class AccrPedlPsdSafe:
        sig_name = "AccrPedlPsdSafe"
        sig_start_bit = 13
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoYesInitial_Initial': 0, 'NoYesInitial_No': 1, 'NoYesInitial_Yes': 2}
        compute_method = None
        length = 2
        startbit = 13
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class PtSysTotRgnTqReqTq:
        sig_name = "PtSysTotRgnTqReqTq"
        sig_start_bit = 339
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 1
        sig_value_offset = -15000.0
        sig_value_min = 0
        sig_value_max = 32767
        sig_byteorder = "Motorola"
        sig_value_init = 15000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 339
        bmuws_info = [(42, 0b00001111, 0b11110000, 4, 0), (43, 0b11111111, 0b00000000, 8, 0), (44, 0b11100000, 0b00011111, 3, 5)]

    class AccrPedlValCntr:
        sig_name = "AccrPedlValCntr"
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

    class DrvrDesDir_UB:
        sig_name = "DrvrDesDir_UB"
        sig_start_bit = 140
        update_id_bit = 140
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
        startbit = 140
        byte = 17
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4


class BECMPropulsionCANFDFr04:
    msg_name = "BECMPropulsionCANFDFr04"
    msg_id = 544
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.07
    msg_length = 8
    tx_node = "BECM"
    rx_nodes = ['CCUMCUCD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HVBattLimnIndcnDTCInfo:
        sig_name = "HVBattLimnIndcnDTCInfo"
        sig_start_bit = 7
        update_id_bit = 23
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
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0)]


class BECMPropulsionCANFDFr05:
    msg_name = "BECMPropulsionCANFDFr05"
    msg_id = 609
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 64
    tx_node = "BECM"
    rx_nodes = ['VCU', 'ETC', 'CCUMCUCD', 'MGM', 'IEM']
    sig_group_dict = {'HVBattCellTTar': ['HVBattCellTTarCellTTar', 'HVBattCellTTarType'], 'HVBattThermMngtPwrAct': ['HVBattThermMngtPwrActCoolgPwr', 'HVBattThermMngtPwrActHeatgPwr'], 'HVBattOverHeatgStopReq': ['HVBattOverHeatgStopReqChks', 'HVBattOverHeatgStopReqCntr', 'HVBattOverHeatgStopReqReqSt']}
    sig_group_dataid_dict = {}

    class HVBattThermMngtEgyReq:
        sig_name = "HVBattThermMngtEgyReq"
        sig_start_bit = 227
        update_id_bit = 233
        sig_length = 10
        sig_value_factor = 50
        sig_value_offset = -1.0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 227
        bmuws_info = [(28, 0b00001111, 0b11110000, 4, 0), (29, 0b11111100, 0b00000011, 6, 2)]

    class HVIL3St:
        sig_name = "HVIL3St"
        sig_start_bit = 291
        update_id_bit = 313
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OpenCls2_Default': 0, 'OpenCls2_Close': 1, 'OpenCls2_Open': 2, 'OpenCls2_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 291
        byte = 36
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class HVSysIsoSts:
        sig_name = "HVSysIsoSts"
        sig_start_bit = 319
        update_id_bit = 326
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvSysIsoSts_Default': 0, 'HvSysIsoSts_Error_Battery_before_HV_Ready': 1, 'HvSysIsoSts_Error_HV_bus_after_HV_Ready': 2, 'HvSysIsoSts_OK': 3}
        compute_method = None
        length = 2
        startbit = 319
        byte = 39
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HVBattCellTTar_UB:
        sig_name = "HVBattCellTTar_UB"
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

    class HVBattOverHeatgStopReqChks:
        sig_name = "HVBattOverHeatgStopReqChks"
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

    class HVBattOverHeatgStopReqCntr:
        sig_name = "HVBattOverHeatgStopReqCntr"
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

    class HvBattPlsHeatgFrq:
        sig_name = "HvBattPlsHeatgFrq"
        sig_start_bit = 191
        update_id_bit = 194
        sig_length = 13
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 5000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 191
        bmuws_info = [(23, 0b11111111, 0b00000000, 8, 0), (24, 0b11111000, 0b00000111, 5, 3)]

    class HVBattCooltTReq:
        sig_name = "HVBattCooltTReq"
        sig_start_bit = 77
        update_id_bit = 82
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
        startbit = 77
        bmuws_info = [(9, 0b00111111, 0b11000000, 6, 0), (10, 0b11111000, 0b00000111, 5, 3)]

    class HvBattPlsHeatgI:
        sig_name = "HvBattPlsHeatgI"
        sig_start_bit = 193
        update_id_bit = 215
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 193
        bmuws_info = [(24, 0b00000011, 0b11111100, 2, 0), (25, 0b11111111, 0b00000000, 8, 0)]

    class HvBattPlsHeatgILimMax:
        sig_name = "HvBattPlsHeatgILimMax"
        sig_start_bit = 214
        update_id_bit = 220
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 214
        bmuws_info = [(26, 0b01111111, 0b10000000, 7, 0), (27, 0b11100000, 0b00011111, 3, 5)]

    class HvBattPackSOH:
        sig_name = "HvBattPackSOH"
        sig_start_bit = 127
        update_id_bit = 172
        sig_length = 8
        sig_value_factor = 0.5
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 204
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 127
        byte = 15
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvBattHeatGenRate:
        sig_name = "HvBattHeatGenRate"
        sig_start_bit = 81
        update_id_bit = 102
        sig_length = 11
        sig_value_factor = 10
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1600
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 81
        bmuws_info = [(10, 0b00000011, 0b11111100, 2, 0), (11, 0b11111111, 0b00000000, 8, 0), (12, 0b10000000, 0b01111111, 1, 7)]

    class HVBattPcakSOCE:
        sig_name = "HVBattPcakSOCE"
        sig_start_bit = 167
        update_id_bit = 169
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 2040
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 167
        bmuws_info = [(20, 0b11111111, 0b00000000, 8, 0), (21, 0b11100000, 0b00011111, 3, 5)]

    class HvBattPlsHeatgFltSts:
        sig_name = "HvBattPlsHeatgFltSts"
        sig_start_bit = 183
        update_id_bit = 168
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 9
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvBattPlsHeatgFltSts_Idle': 0, 'HvBattPlsHeatgFltSts_OverT': 1, 'HvBattPlsHeatgFltSts_TRiseErr': 2, 'HvBattPlsHeatgFltSts_HvIsoRErr': 3, 'HvBattPlsHeatgFltSts_HVILFlt': 4, 'HvBattPlsHeatgFltSts_OverUFlt': 5, 'HvBattPlsHeatgFltSts_UnderUFlt': 6, 'HvBattPlsHeatgFltSts_OverIFlt': 7, 'HvBattPlsHeatgFltSts_TDif': 8, 'HvBattPlsHeatgFltSts_Reserved': 9}
        compute_method = None
        length = 4
        startbit = 183
        byte = 22
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class HVBattCellTRate:
        sig_name = "HVBattCellTRate"
        sig_start_bit = 24
        update_id_bit = 47
        sig_length = 9
        sig_value_factor = 0.1
        sig_value_offset = -25.0
        sig_value_min = 0
        sig_value_max = 500
        sig_byteorder = "Motorola"
        sig_value_init = 250
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 24
        bmuws_info = [(3, 0b00000001, 0b11111110, 1, 0), (4, 0b11111111, 0b00000000, 8, 0)]

    class MntnBattTReq:
        sig_name = "MntnBattTReq"
        sig_start_bit = 317
        update_id_bit = 325
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ReqSts2_Default': 0, 'ReqSts2_NotReqd': 1, 'ReqSts2_Reqd': 2, 'ReqSts2_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 317
        byte = 39
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class HVBattClimaTiEstimd:
        sig_name = "HVBattClimaTiEstimd"
        sig_start_bit = 63
        update_id_bit = 48
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HVIsoRVal:
        sig_name = "HVIsoRVal"
        sig_start_bit = 303
        update_id_bit = 327
        sig_length = 16
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 60000
        sig_byteorder = "Motorola"
        sig_value_init = 60000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 303
        bmuws_info = [(37, 0b11111111, 0b00000000, 8, 0), (38, 0b11111111, 0b00000000, 8, 0)]

    class HVBattPackUMinLim:
        sig_name = "HVBattPackUMinLim"
        sig_start_bit = 151
        update_id_bit = 170
        sig_length = 16
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 65535
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 151
        bmuws_info = [(18, 0b11111111, 0b00000000, 8, 0), (19, 0b11111111, 0b00000000, 8, 0)]

    class HVBattThermMngtPwrAct_UB:
        sig_name = "HVBattThermMngtPwrAct_UB"
        sig_start_bit = 269
        update_id_bit = 269
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
        startbit = 269
        byte = 33
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class DCChrgrIsoUMax:
        sig_name = "DCChrgrIsoUMax"
        sig_start_bit = 7
        update_id_bit = 23
        sig_length = 16
        sig_value_factor = 0.1
        sig_value_offset = 0
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

    class HVBattCellUMaxLim:
        sig_name = "HVBattCellUMaxLim"
        sig_start_bit = 46
        update_id_bit = 49
        sig_length = 13
        sig_value_factor = 0.001
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 5000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 46
        bmuws_info = [(5, 0b01111111, 0b10000000, 7, 0), (6, 0b11111100, 0b00000011, 6, 2)]

    class HVBattThermMngtPwrActHeatgPwr:
        sig_name = "HVBattThermMngtPwrActHeatgPwr"
        sig_start_bit = 250
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 10
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 250
        bmuws_info = [(31, 0b00000111, 0b11111000, 3, 0), (32, 0b11111111, 0b00000000, 8, 0), (33, 0b11000000, 0b00111111, 2, 6)]

    class HVIL1St:
        sig_name = "HVIL1St"
        sig_start_bit = 295
        update_id_bit = 315
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OpenCls2_Default': 0, 'OpenCls2_Close': 1, 'OpenCls2_Open': 2, 'OpenCls2_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 295
        byte = 36
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HVBattOverHeatgStopReq_UB:
        sig_name = "HVBattOverHeatgStopReq_UB"
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

    class HVBattCellTTarCellTTar:
        sig_name = "HVBattCellTTarCellTTar"
        sig_start_bit = 20
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
        startbit = 20
        bmuws_info = [(2, 0b00011111, 0b11100000, 5, 0), (3, 0b11111100, 0b00000011, 6, 2)]

    class HVBattThermReq:
        sig_name = "HVBattThermReq"
        sig_start_bit = 279
        update_id_bit = 276
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HVBattThermReq_Idle': 0, 'HVBattThermReq_ThermalBalancing': 1, 'HVBattThermReq_PassiveHeating': 2, 'HVBattThermReq_ActiveHeating': 3, 'HVBattThermReq_PassiveCooling': 4, 'HVBattThermReq_ActiveCooling': 5, 'HVBattThermReq_CombinedCooling': 6, 'HVBattThermReq_Reserved': 7}
        compute_method = None
        length = 3
        startbit = 279
        byte = 34
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class HVBattPreHeatgReqSts:
        sig_name = "HVBattPreHeatgReqSts"
        sig_start_bit = 219
        update_id_bit = 217
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ReqSts2_Default': 0, 'ReqSts2_NotReqd': 1, 'ReqSts2_Reqd': 2, 'ReqSts2_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 219
        byte = 27
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class HVBattPackUMaxLim:
        sig_name = "HVBattPackUMaxLim"
        sig_start_bit = 135
        update_id_bit = 171
        sig_length = 16
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 65535
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 135
        bmuws_info = [(16, 0b11111111, 0b00000000, 8, 0), (17, 0b11111111, 0b00000000, 8, 0)]

    class HVBattOverHeatgStopReqReqSt:
        sig_name = "HVBattOverHeatgStopReqReqSt"
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
        sig_value_table = {'ReqSts2_Default': 0, 'ReqSts2_NotReqd': 1, 'ReqSts2_Reqd': 2, 'ReqSts2_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 119
        byte = 14
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HVBattOptmzSts:
        sig_name = "HVBattOptmzSts"
        sig_start_bit = 101
        update_id_bit = 99
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ReqSts2_Default': 0, 'ReqSts2_NotReqd': 1, 'ReqSts2_Reqd': 2, 'ReqSts2_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 101
        byte = 12
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class HVIsoCrashFb:
        sig_name = "HVIsoCrashFb"
        sig_start_bit = 289
        update_id_bit = 312
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'IsoCrashFb_Idle': 0, 'IsoCrashFb_Evln': 1, 'IsoCrashFb_Nok': 2, 'IsoCrashFb_Ok': 3}
        compute_method = None
        length = 2
        startbit = 289
        byte = 36
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class HvBattThermReqLvl:
        sig_name = "HvBattThermReqLvl"
        sig_start_bit = 275
        update_id_bit = 273
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ReqLvl_NoReq': 0, 'ReqLvl_LoReq': 1, 'ReqLvl_MidReq': 2, 'ReqLvl_HiReq': 3}
        compute_method = None
        length = 2
        startbit = 275
        byte = 34
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class HVBattThermMngtSts:
        sig_name = "HVBattThermMngtSts"
        sig_start_bit = 268
        update_id_bit = 266
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'StartFinish1_Start': 0, 'StartFinish1_Finish': 1, 'StartFinish1_Reserved1': 2, 'StartFinish1_Reserved2': 3}
        compute_method = None
        length = 2
        startbit = 268
        byte = 33
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class HVBattThermMngtPwrActCoolgPwr:
        sig_name = "HVBattThermMngtPwrActCoolgPwr"
        sig_start_bit = 247
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 10
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 247
        bmuws_info = [(30, 0b11111111, 0b00000000, 8, 0), (31, 0b11111000, 0b00000111, 5, 3)]

    class HVIL2St:
        sig_name = "HVIL2St"
        sig_start_bit = 293
        update_id_bit = 314
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OpenCls2_Default': 0, 'OpenCls2_Close': 1, 'OpenCls2_Open': 2, 'OpenCls2_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 293
        byte = 36
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class HVBattCellTTarType:
        sig_name = "HVBattCellTTarType"
        sig_start_bit = 22
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BattTemperatureType_Idle': 0, 'BattTemperatureType_Tmin': 1, 'BattTemperatureType_TAvg': 2, 'BattTemperatureType_TMax': 3}
        compute_method = None
        length = 2
        startbit = 22
        byte = 2
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class HVBattCooltFlwReq:
        sig_name = "HVBattCooltFlwReq"
        sig_start_bit = 71
        update_id_bit = 78
        sig_length = 9
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 500
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 71
        bmuws_info = [(8, 0b11111111, 0b00000000, 8, 0), (9, 0b10000000, 0b01111111, 1, 7)]

    class HVBattWakeUpU:
        sig_name = "HVBattWakeUpU"
        sig_start_bit = 287
        update_id_bit = 272
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 287
        byte = 35
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class LVCtrldSplyU:
        sig_name = "LVCtrldSplyU"
        sig_start_bit = 335
        update_id_bit = 343
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 335
        byte = 41
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HVBattSuperChrgnThermSts:
        sig_name = "HVBattSuperChrgnThermSts"
        sig_start_bit = 231
        update_id_bit = 228
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HVBattThermSts1_Idle': 0, 'HVBattThermSts1_Prestart': 1, 'HVBattThermSts1_Standby': 2, 'HVBattThermSts1_Active': 3, 'HVBattThermSts1_Off': 4}
        compute_method = None
        length = 3
        startbit = 231
        byte = 28
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5


class CCUMCUCDPropulsionCANFDFr03:
    msg_name = "CCUMCUCDPropulsionCANFDFr03"
    msg_id = 278
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.03
    msg_length = 8
    tx_node = "CCUMCUCD"
    rx_nodes = ['EGSM']
    sig_group_dict = {'BackLiDrvReq': ['BackLiDrvReqLightCmd', 'BackLiDrvReqLiPerc', 'BackLiDrvReqReadingLiDimsSpdCmd']}
    sig_group_dataid_dict = {}

    class BackLiDrvReqLiPerc:
        sig_name = "BackLiDrvReqLiPerc"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class BackLiDrvReqReadingLiDimsSpdCmd:
        sig_name = "BackLiDrvReqReadingLiDimsSpdCmd"
        sig_start_bit = 3
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ReadingLiDimsSpdCmd_NoCmd': 0, 'ReadingLiDimsSpdCmd_400ms': 1, 'ReadingLiDimsSpdCmd_800ms': 2, 'ReadingLiDimsSpdCmd_1000ms': 3, 'ReadingLiDimsSpdCmd_2000ms': 4, 'ReadingLiDimsSpdCmd_Resverd': 5}
        compute_method = None
        length = 3
        startbit = 3
        byte = 0
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class BackLiDrvReq_UB:
        sig_name = "BackLiDrvReq_UB"
        sig_start_bit = 0
        update_id_bit = 0
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
        startbit = 0
        byte = 0
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class BackLiDrvReqLightCmd:
        sig_name = "BackLiDrvReqLightCmd"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LightCmd_NoReq': 0, 'LightCmd_ON': 1, 'LightCmd_OFF': 2, 'LightCmd_TBD': 3}
        compute_method = None
        length = 4
        startbit = 7
        byte = 0
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4


class MGMPropulsionCANFDFr05:
    msg_name = "MGMPropulsionCANFDFr05"
    msg_id = 614
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 32
    tx_node = "MGM"
    rx_nodes = ['VCU', 'CCUMCUCD']
    sig_group_dict = {'FrntMotHeatgFb': ['FrntMotHeatgFbMotSts', 'FrntMotHeatgFbPwrAvl'], 'FrntMotInfo': ['FrntMotInfoActvDchaAlrmSt', 'FrntMotInfoActvHeatgAlrmSt', 'FrntMotInfoBoostAlrmSt', 'FrntMotInfoDTCHig', 'FrntMotInfoDTCLMid', 'FrntMotInfoDTCLow', 'FrntMotInfoDTCSts', 'FrntMotInfoEMQnty', 'FrntMotInfoEMSeqNr', 'FrntMotInfoFltAlrmSt', 'FrntMotInfoInvrtTAlrmSt', 'FrntMotInfoIPhaAlrmSt', 'FrntMotInfoModStRms', 'FrntMotInfoMotTAlrmSt', 'FrntMotInfoOilTAlrmSt', 'FrntMotInfoOverSpdAlrmSt', 'FrntMotInfoPasDchaAlrmSt', 'FrntMotInfoPlsHeatAlrmSt', 'FrntMotInfoRatTypeInfo', 'FrntMotInfoRslAlrmSt', 'FrntMotInfoTqAlrmSt', 'FrntMotInfoUDCAlrmSt']}
    sig_group_dataid_dict = {}

    class FrntMotInfoRslAlrmSt:
        sig_name = "FrntMotInfoRslAlrmSt"
        sig_start_bit = 133
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSts_Disarmd': 0, 'AlrmSts_Armd': 1, 'AlrmSts_Actv': 2, 'AlrmSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 133
        byte = 16
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class FrntMotInfoDTCHig:
        sig_name = "FrntMotInfoDTCHig"
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

    class FrntMotInfoTqAlrmSt:
        sig_name = "FrntMotInfoTqAlrmSt"
        sig_start_bit = 131
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSts_Disarmd': 0, 'AlrmSts_Armd': 1, 'AlrmSts_Actv': 2, 'AlrmSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 131
        byte = 16
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class FrntMotMotT:
        sig_name = "FrntMotMotT"
        sig_start_bit = 171
        update_id_bit = 190
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = -256.0
        sig_value_min = 0
        sig_value_max = 5119
        sig_byteorder = "Motorola"
        sig_value_init = 2560
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 171
        bmuws_info = [(21, 0b00001111, 0b11110000, 4, 0), (22, 0b11111111, 0b00000000, 8, 0), (23, 0b10000000, 0b01111111, 1, 7)]

    class FrntMotHeatgPwrAct:
        sig_name = "FrntMotHeatgPwrAct"
        sig_start_bit = 47
        update_id_bit = 54
        sig_length = 9
        sig_value_factor = 10
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b10000000, 0b01111111, 1, 7)]

    class FrntMotInfoEMQnty:
        sig_name = "FrntMotInfoEMQnty"
        sig_start_bit = 111
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
        startbit = 111
        byte = 13
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class FrntMotInfoDTCLMid:
        sig_name = "FrntMotInfoDTCLMid"
        sig_start_bit = 87
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 87
        byte = 10
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntMotInfoMotTAlrmSt:
        sig_name = "FrntMotInfoMotTAlrmSt"
        sig_start_bit = 127
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSts_Disarmd': 0, 'AlrmSts_Armd': 1, 'AlrmSts_Actv': 2, 'AlrmSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 127
        byte = 15
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class FrntMotCooltFlowReq:
        sig_name = "FrntMotCooltFlowReq"
        sig_start_bit = 5
        update_id_bit = 12
        sig_length = 9
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 500
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 5
        bmuws_info = [(0, 0b00111111, 0b11000000, 6, 0), (1, 0b11100000, 0b00011111, 3, 5)]

    class FrntMotInfoIPhaAlrmSt:
        sig_name = "FrntMotInfoIPhaAlrmSt"
        sig_start_bit = 117
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSts_Disarmd': 0, 'AlrmSts_Armd': 1, 'AlrmSts_Actv': 2, 'AlrmSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 117
        byte = 14
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class FrntMotInfoPasDchaAlrmSt:
        sig_name = "FrntMotInfoPasDchaAlrmSt"
        sig_start_bit = 121
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSts_Disarmd': 0, 'AlrmSts_Armd': 1, 'AlrmSts_Actv': 2, 'AlrmSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 121
        byte = 15
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class FrntMotInvrT:
        sig_name = "FrntMotInvrT"
        sig_start_bit = 151
        update_id_bit = 154
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = -256.0
        sig_value_min = 0
        sig_value_max = 5119
        sig_byteorder = "Motorola"
        sig_value_init = 2560
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 151
        bmuws_info = [(18, 0b11111111, 0b00000000, 8, 0), (19, 0b11111000, 0b00000111, 5, 3)]

    class FrntMotInfoRatTypeInfo:
        sig_name = "FrntMotInfoRatTypeInfo"
        sig_start_bit = 143
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
        startbit = 143
        byte = 17
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class FrntMotInfoActvDchaAlrmSt:
        sig_name = "FrntMotInfoActvDchaAlrmSt"
        sig_start_bit = 71
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSts_Disarmd': 0, 'AlrmSts_Armd': 1, 'AlrmSts_Actv': 2, 'AlrmSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 71
        byte = 8
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class FrntMotInfoEMSeqNr:
        sig_name = "FrntMotInfoEMSeqNr"
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

    class FrntMotInfoUDCAlrmSt:
        sig_name = "FrntMotInfoUDCAlrmSt"
        sig_start_bit = 129
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSts_Disarmd': 0, 'AlrmSts_Armd': 1, 'AlrmSts_Actv': 2, 'AlrmSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 129
        byte = 16
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class FrntMotInfoDTCSts:
        sig_name = "FrntMotInfoDTCSts"
        sig_start_bit = 103
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
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

    class FrntMotHeatgFbMotSts:
        sig_name = "FrntMotHeatgFbMotSts"
        sig_start_bit = 11
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 6
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'MotHeatgSts_Ini': 0, 'MotHeatgSts_Standby': 1, 'MotHeatgSts_Heatg': 2, 'MotHeatgSts_ElecErr': 3, 'MotHeatgSts_OvrTemp': 4, 'MotHeatgSts_PwrLim': 5, 'MotHeatgSts_Reserved1': 6}
        compute_method = None
        length = 3
        startbit = 11
        byte = 1
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class FrntMotHeatgPwrMax:
        sig_name = "FrntMotHeatgPwrMax"
        sig_start_bit = 53
        update_id_bit = 60
        sig_length = 9
        sig_value_factor = 10
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 53
        bmuws_info = [(6, 0b00111111, 0b11000000, 6, 0), (7, 0b11100000, 0b00011111, 3, 5)]

    class FrntMotInfoDTCLow:
        sig_name = "FrntMotInfoDTCLow"
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

    class FrntMotInfoBoostAlrmSt:
        sig_name = "FrntMotInfoBoostAlrmSt"
        sig_start_bit = 67
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSts_Disarmd': 0, 'AlrmSts_Armd': 1, 'AlrmSts_Actv': 2, 'AlrmSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 67
        byte = 8
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class FrntMotInfoInvrtTAlrmSt:
        sig_name = "FrntMotInfoInvrtTAlrmSt"
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
        sig_value_table = {'AlrmSts_Disarmd': 0, 'AlrmSts_Armd': 1, 'AlrmSts_Actv': 2, 'AlrmSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 119
        byte = 14
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class FrntMotInfoOverSpdAlrmSt:
        sig_name = "FrntMotInfoOverSpdAlrmSt"
        sig_start_bit = 123
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSts_Disarmd': 0, 'AlrmSts_Armd': 1, 'AlrmSts_Actv': 2, 'AlrmSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 123
        byte = 15
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class FrntMotOilT:
        sig_name = "FrntMotOilT"
        sig_start_bit = 189
        update_id_bit = 192
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = -256.0
        sig_value_min = 0
        sig_value_max = 5119
        sig_byteorder = "Motorola"
        sig_value_init = 2560
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 189
        bmuws_info = [(23, 0b00111111, 0b11000000, 6, 0), (24, 0b11111110, 0b00000001, 7, 1)]

    class FrntMotInfoActvHeatgAlrmSt:
        sig_name = "FrntMotInfoActvHeatgAlrmSt"
        sig_start_bit = 69
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSts_Disarmd': 0, 'AlrmSts_Armd': 1, 'AlrmSts_Actv': 2, 'AlrmSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 69
        byte = 8
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class FrntMotInfoFltAlrmSt:
        sig_name = "FrntMotInfoFltAlrmSt"
        sig_start_bit = 65
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSts_Disarmd': 0, 'AlrmSts_Armd': 1, 'AlrmSts_Actv': 2, 'AlrmSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 65
        byte = 8
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class FrntMotHeatgFb_UB:
        sig_name = "FrntMotHeatgFb_UB"
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

    class FrntMotInfoPlsHeatAlrmSt:
        sig_name = "FrntMotInfoPlsHeatAlrmSt"
        sig_start_bit = 135
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSts_Disarmd': 0, 'AlrmSts_Armd': 1, 'AlrmSts_Actv': 2, 'AlrmSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 135
        byte = 16
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class FrntMotHeatgFbPwrAvl:
        sig_name = "FrntMotHeatgFbPwrAvl"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 9
        sig_value_factor = 10
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class FrntMotInfoModStRms:
        sig_name = "FrntMotInfoModStRms"
        sig_start_bit = 115
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 3
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ModStatusRms_Invalid': 0, 'ModStatusRms_PwrCns': 1, 'ModStatusRms_PwrGen': 2, 'ModStatusRms_OffSts': 3, 'ModStatusRms_RdySts': 4, 'ModStatusRms_Abnormal': 5, 'ModStatusRms_Invalid1': 6, 'ModStatusRms_Invalid2': 7, 'ModStatusRms_Invalid3': 8, 'ModStatusRms_Invalid4': 9, 'ModStatusRms_Invalid5': 10, 'ModStatusRms_Invalid6': 11, 'ModStatusRms_Invalid7': 12, 'ModStatusRms_Invalid8': 13, 'ModStatusRms_Invalid9': 14, 'ModStatusRms_Invalid10': 15}
        compute_method = None
        length = 4
        startbit = 115
        byte = 14
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class FrntMotMotHeatGenRate:
        sig_name = "FrntMotMotHeatGenRate"
        sig_start_bit = 153
        update_id_bit = 172
        sig_length = 13
        sig_value_factor = 10
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 153
        bmuws_info = [(19, 0b00000011, 0b11111100, 2, 0), (20, 0b11111111, 0b00000000, 8, 0), (21, 0b11100000, 0b00011111, 3, 5)]

    class FrntMotCoolgReq:
        sig_name = "FrntMotCoolgReq"
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
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class FrntMotInfo_UB:
        sig_name = "FrntMotInfo_UB"
        sig_start_bit = 139
        update_id_bit = 139
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
        startbit = 139
        byte = 17
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class FrntMotCooltT:
        sig_name = "FrntMotCooltT"
        sig_start_bit = 30
        update_id_bit = 33
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = -256.0
        sig_value_min = 0
        sig_value_max = 5119
        sig_byteorder = "Motorola"
        sig_value_init = 2560
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 30
        bmuws_info = [(3, 0b01111111, 0b10000000, 7, 0), (4, 0b11111100, 0b00000011, 6, 2)]

    class FrntMotInfoOilTAlrmSt:
        sig_name = "FrntMotInfoOilTAlrmSt"
        sig_start_bit = 125
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSts_Disarmd': 0, 'AlrmSts_Armd': 1, 'AlrmSts_Actv': 2, 'AlrmSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 125
        byte = 15
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4


class IEMToCCUMCUCDPropulsionCANFDDiagRespFrame:
    msg_name = "IEMToCCUMCUCDPropulsionCANFDDiagRespFrame"
    msg_id = 1591
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "IEM"
    rx_nodes = ['CCUMCUCD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class CCUMCUADPropulsionCANFDNmFr:
    msg_name = "CCUMCUADPropulsionCANFDNmFr"
    msg_id = 1282
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CCUMCUAD"
    rx_nodes = ['BECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class MGMToCCUMCUCDPropulsionCANFDDiagRespFrame:
    msg_name = "MGMToCCUMCUCDPropulsionCANFDDiagRespFrame"
    msg_id = 1585
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "MGM"
    rx_nodes = ['CCUMCUCD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class VCUPropulsionCANFDFr08:
    msg_name = "VCUPropulsionCANFDFr08"
    msg_id = 617
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 32
    tx_node = "VCU"
    rx_nodes = ['ETC', 'CCUMCUCD', 'MGM', 'IEM', 'BECM', 'CCUMCUAD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class PlsHeatgCmd:
        sig_name = "PlsHeatgCmd"
        sig_start_bit = 119
        update_id_bit = 113
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PlsHeatgCmd_Init': 0, 'PlsHeatgCmd_Nok': 1, 'PlsHeatgCmd_Ok': 2, 'PlsHeatgCmd_Hold': 3}
        compute_method = None
        length = 2
        startbit = 119
        byte = 14
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HVBattChrgnILim:
        sig_name = "HVBattChrgnILim"
        sig_start_bit = 62
        update_id_bit = 65
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 8190
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 62
        bmuws_info = [(7, 0b01111111, 0b10000000, 7, 0), (8, 0b11111100, 0b00000011, 6, 2)]

    class ReMotHeatgPwrReq:
        sig_name = "ReMotHeatgPwrReq"
        sig_start_bit = 127
        update_id_bit = 134
        sig_length = 9
        sig_value_factor = 10
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 127
        bmuws_info = [(15, 0b11111111, 0b00000000, 8, 0), (16, 0b10000000, 0b01111111, 1, 7)]

    class ReMotOilTEstimdFromVCU:
        sig_name = "ReMotOilTEstimdFromVCU"
        sig_start_bit = 133
        update_id_bit = 136
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = -256.0
        sig_value_min = 0
        sig_value_max = 5119
        sig_byteorder = "Motorola"
        sig_value_init = 2560
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 133
        bmuws_info = [(16, 0b00111111, 0b11000000, 6, 0), (17, 0b11111110, 0b00000001, 7, 1)]

    class BoostChrgILim:
        sig_name = "BoostChrgILim"
        sig_start_bit = 7
        update_id_bit = 23
        sig_length = 16
        sig_value_factor = 0.1
        sig_value_offset = -3000.0
        sig_value_min = 0
        sig_value_max = 65535
        sig_byteorder = "Motorola"
        sig_value_init = 30000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class HVSysActvFctReq:
        sig_name = "HVSysActvFctReq"
        sig_start_bit = 89
        update_id_bit = 115
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OffOnNoCmd_NoCmd': 0, 'OffOnNoCmd_Off': 1, 'OffOnNoCmd_On': 2}
        compute_method = None
        length = 2
        startbit = 89
        byte = 11
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class HVChrgModReq:
        sig_name = "HVChrgModReq"
        sig_start_bit = 93
        update_id_bit = 116
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 15
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HVChrgModReq_NoReq': 0, 'HVChrgModReq_ACChrgn': 1, 'HVChrgModReq_BoostPreChrg': 2, 'HVChrgModReq_BoostChrgn': 3, 'HVChrgModReq_DCChrgn': 4, 'HVChrgModReq_ACDisChrgn': 5, 'HVChrgModReq_DCDisChrgn': 6, 'HVChrgModReq_WirelsChrgn': 7, 'HVChrgModReq_Reserved1': 8, 'HVChrgModReq_Reserved2': 9, 'HVChrgModReq_Init': 15}
        compute_method = None
        length = 4
        startbit = 93
        byte = 11
        mask = 0b00111100
        unmask = 0b11000011
        shift = 2

    class FrntMotOilTEstimdFromVCU:
        sig_name = "FrntMotOilTEstimdFromVCU"
        sig_start_bit = 47
        update_id_bit = 50
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = -256.0
        sig_value_min = 0
        sig_value_max = 5119
        sig_byteorder = "Motorola"
        sig_value_init = 2560
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111000, 0b00000111, 5, 3)]

    class ReMotHeatgEna:
        sig_name = "ReMotHeatgEna"
        sig_start_bit = 64
        update_id_bit = 79
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
        startbit = 64
        byte = 8
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FrntMotHeatgPwrReq:
        sig_name = "FrntMotHeatgPwrReq"
        sig_start_bit = 27
        update_id_bit = 34
        sig_length = 9
        sig_value_factor = 10
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 27
        bmuws_info = [(3, 0b00001111, 0b11110000, 4, 0), (4, 0b11111000, 0b00000111, 5, 3)]

    class FrntMotHeatgEna:
        sig_name = "FrntMotHeatgEna"
        sig_start_bit = 33
        update_id_bit = 32
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
        startbit = 33
        byte = 4
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class HVBattThermAllwd:
        sig_name = "HVBattThermAllwd"
        sig_start_bit = 95
        update_id_bit = 117
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ThermAllwd_Init': 0, 'ThermAllwd_NOK': 1, 'ThermAllwd_OK': 2, 'ThermAllwd_HOLD': 3}
        compute_method = None
        length = 2
        startbit = 95
        byte = 11
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class OnBdChrgrHndlSts:
        sig_name = "OnBdChrgrHndlSts"
        sig_start_bit = 103
        update_id_bit = 114
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 14
        sig_byteorder = "Motorola"
        sig_value_init = 8
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OBCChrgrHndlSt_Disconnected': 0, 'OBCChrgrHndlSt_ConnectedWithoutPower': 1, 'OBCChrgrHndlSt_PowerAvailableButNotActivated': 2, 'OBCChrgrHndlSt_ConnectedWithPower': 3, 'OBCChrgrHndlSt_DischargeConnectwithoutpowerincar': 4, 'OBCChrgrHndlSt_DischargeConnectwithoutpoweroutcar': 5, 'OBCChrgrHndlSt_DischargeConnectwithpowerincar': 6, 'OBCChrgrHndlSt_DischargeConnectwithpoweroutcar': 7, 'OBCChrgrHndlSt_Init': 8, 'OBCChrgrHndlSt_Fault': 9, 'OBCChrgrHndlSt_NotCompleteConnnected': 10, 'OBCChrgrHndlSt_ConnectedWithPowerButNotPWM': 11, 'OBCChrgrHndlSt_Reserved1': 12, 'OBCChrgrHndlSt_Reserved2': 13, 'OBCChrgrHndlSt_Reserved3': 14}
        compute_method = None
        length = 4
        startbit = 103
        byte = 12
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class PlsHeatgTarT1:
        sig_name = "PlsHeatgTarT1"
        sig_start_bit = 111
        update_id_bit = 112
        sig_length = 8
        sig_value_factor = 0.5
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 256
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 111
        byte = 13
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HndlLockgSts:
        sig_name = "HndlLockgSts"
        sig_start_bit = 49
        update_id_bit = 63
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LockgSts_Unknown': 0, 'LockgSts_Locked': 1, 'LockgSts_Unlocked': 2, 'LockgSts_Fault': 3}
        compute_method = None
        length = 2
        startbit = 49
        byte = 6
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class HVBattChrgPwrActCns1:
        sig_name = "HVBattChrgPwrActCns1"
        sig_start_bit = 78
        update_id_bit = 81
        sig_length = 13
        sig_value_factor = 100
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 78
        bmuws_info = [(9, 0b01111111, 0b10000000, 7, 0), (10, 0b11111100, 0b00000011, 6, 2)]

    class BoostPwrReq:
        sig_name = "BoostPwrReq"
        sig_start_bit = 22
        update_id_bit = 28
        sig_length = 10
        sig_value_factor = 0.5
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 22
        bmuws_info = [(2, 0b01111111, 0b10000000, 7, 0), (3, 0b11100000, 0b00011111, 3, 5)]

    class VehChrgnSts:
        sig_name = "VehChrgnSts"
        sig_start_bit = 99
        update_id_bit = 96
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 3
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ChrgnSts_Fault': 0, 'ChrgnSts_ChargingInParkingState': 1, 'ChrgnSts_ChargingInDrivingState': 2, 'ChrgnSts_NotCharging': 3, 'ChrgnSts_ChargingCompleted': 4, 'ChrgnSts_Invalid': 5, 'ChrgnSts_Reserved1': 6, 'ChrgnSts_Reserved2': 7}
        compute_method = None
        length = 3
        startbit = 99
        byte = 12
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1


class CCUMCUCDToODPPropulsionCANFDDiagReqFrame:
    msg_name = "CCUMCUCDToODPPropulsionCANFDDiagReqFrame"
    msg_id = 1872
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "CCUMCUCD"
    rx_nodes = ['ODP']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class CCUMCUCDToBECMPropulsionCANFDDiagReqFrame:
    msg_name = "CCUMCUCDToBECMPropulsionCANFDDiagReqFrame"
    msg_id = 1845
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "CCUMCUCD"
    rx_nodes = ['BECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class IEMPropulsionCANFDFr02:
    msg_name = "IEMPropulsionCANFDFr02"
    msg_id = 133
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 16
    tx_node = "IEM"
    rx_nodes = ['VCU', 'BECM', 'CCUMCUCD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class ReMotUDc:
        sig_name = "ReMotUDc"
        sig_start_bit = 23
        update_id_bit = 38
        sig_length = 16
        sig_value_factor = 0.1
        sig_value_offset = 0
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

    class ReMotIDc:
        sig_name = "ReMotIDc"
        sig_start_bit = 7
        update_id_bit = 39
        sig_length = 16
        sig_value_factor = 0.1
        sig_value_offset = -3000.0
        sig_value_min = 0
        sig_value_max = 65535
        sig_byteorder = "Motorola"
        sig_value_init = 30000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0)]


class SRSPropulsionCANFDNmFr:
    msg_name = "SRSPropulsionCANFDNmFr"
    msg_id = 1296
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "SRS"
    rx_nodes = ['ODP']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class CCUMCUADPropulsionCANFDFr01:
    msg_name = "CCUMCUADPropulsionCANFDFr01"
    msg_id = 292
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.03
    msg_length = 8
    tx_node = "CCUMCUAD"
    rx_nodes = ['VCU']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class ReAxleLvl:
        sig_name = "ReAxleLvl"
        sig_start_bit = 15
        update_id_bit = 11
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 14
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HeightLevel_LowLevel5': 0, 'HeightLevel_LowLevel4': 1, 'HeightLevel_LowLevel3': 2, 'HeightLevel_LowLevel2': 3, 'HeightLevel_LowLevel1': 4, 'HeightLevel_NormaLevel': 5, 'HeightLevel_HighLevel1': 6, 'HeightLevel_HighLevel2': 7, 'HeightLevel_HighLevel3': 8, 'HeightLevel_HighLevel4': 9, 'HeightLevel_HighLevel5': 10, 'HeightLevel_Reserved1': 11, 'HeightLevel_Reserved2': 12, 'HeightLevel_Reserved3': 13, 'HeightLevel_InitUnknow': 14, 'HeightLevel_Invalid': 15}
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class FrntAxleLvl:
        sig_name = "FrntAxleLvl"
        sig_start_bit = 7
        update_id_bit = 3
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 14
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HeightLevel_LowLevel5': 0, 'HeightLevel_LowLevel4': 1, 'HeightLevel_LowLevel3': 2, 'HeightLevel_LowLevel2': 3, 'HeightLevel_LowLevel1': 4, 'HeightLevel_NormaLevel': 5, 'HeightLevel_HighLevel1': 6, 'HeightLevel_HighLevel2': 7, 'HeightLevel_HighLevel3': 8, 'HeightLevel_HighLevel4': 9, 'HeightLevel_HighLevel5': 10, 'HeightLevel_Reserved1': 11, 'HeightLevel_Reserved2': 12, 'HeightLevel_Reserved3': 13, 'HeightLevel_InitUnknow': 14, 'HeightLevel_Invalid': 15}
        compute_method = None
        length = 4
        startbit = 7
        byte = 0
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4


class SRSPropulsionCANFDFr03:
    msg_name = "SRSPropulsionCANFDFr03"
    msg_id = 616
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 12
    tx_node = "SRS"
    rx_nodes = ['VCU', 'CCUMCUCD', 'BCU2', 'CCUMCUAD', 'BCU1']
    sig_group_dict = {'NotifyForEmercyCall': ['NotifyForEmercyCallChks', 'NotifyForEmercyCallCntr', 'NotifyForEmercyCallNotifyForEmercyCall']}
    sig_group_dataid_dict = {'NotifyForEmercyCall': 1066}

    class BucSwtStsAtRowSecMid:
        sig_name = "BucSwtStsAtRowSecMid"
        sig_start_bit = 1
        update_id_bit = 17
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BucSwtSts_Invalid': 0, 'BucSwtSts_Error': 1, 'BucSwtSts_Unlocked': 2, 'BucSwtSts_Locked': 3}
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class RollOverSts:
        sig_name = "RollOverSts"
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

    class NotifyForEmercyCallCntr:
        sig_name = "NotifyForEmercyCallCntr"
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

    class BucSwtStsAtRowSecLe:
        sig_name = "BucSwtStsAtRowSecLe"
        sig_start_bit = 3
        update_id_bit = 18
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BucSwtSts_Invalid': 0, 'BucSwtSts_Error': 1, 'BucSwtSts_Unlocked': 2, 'BucSwtSts_Locked': 3}
        compute_method = None
        length = 2
        startbit = 3
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class BucSwtStsAtRowSecRi:
        sig_name = "BucSwtStsAtRowSecRi"
        sig_start_bit = 15
        update_id_bit = 16
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BucSwtSts_Invalid': 0, 'BucSwtSts_Error': 1, 'BucSwtSts_Unlocked': 2, 'BucSwtSts_Locked': 3}
        compute_method = None
        length = 2
        startbit = 15
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class PassAirbEnaSts:
        sig_name = "PassAirbEnaSts"
        sig_start_bit = 9
        update_id_bit = 28
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EnableDisable3_Invalid': 0, 'EnableDisable3_Disabled': 1, 'EnableDisable3_Enabled': 2}
        compute_method = None
        length = 2
        startbit = 9
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class BucSwtStsAtDrvr:
        sig_name = "BucSwtStsAtDrvr"
        sig_start_bit = 7
        update_id_bit = 20
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BucSwtSts_Invalid': 0, 'BucSwtSts_Error': 1, 'BucSwtSts_Unlocked': 2, 'BucSwtSts_Locked': 3}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class BucSwtStsAtPass:
        sig_name = "BucSwtStsAtPass"
        sig_start_bit = 5
        update_id_bit = 19
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BucSwtSts_Invalid': 0, 'BucSwtSts_Error': 1, 'BucSwtSts_Unlocked': 2, 'BucSwtSts_Locked': 3}
        compute_method = None
        length = 2
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class NotifyForEmercyCallNotifyForEmercyCall:
        sig_name = "NotifyForEmercyCallNotifyForEmercyCall"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 47
        byte = 5
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class NotifyForEmercyCallChks:
        sig_name = "NotifyForEmercyCallChks"
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

    class BucSwtStsAtRowThrdRi:
        sig_name = "BucSwtStsAtRowThrdRi"
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
        sig_value_table = {'BucSwtSts_Invalid': 0, 'BucSwtSts_Error': 1, 'BucSwtSts_Unlocked': 2, 'BucSwtSts_Locked': 3}
        compute_method = None
        length = 2
        startbit = 11
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class BucSwtStsAtRowThrdLe:
        sig_name = "BucSwtStsAtRowThrdLe"
        sig_start_bit = 13
        update_id_bit = 31
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BucSwtSts_Invalid': 0, 'BucSwtSts_Error': 1, 'BucSwtSts_Unlocked': 2, 'BucSwtSts_Locked': 3}
        compute_method = None
        length = 2
        startbit = 13
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class PassAirbInjSts:
        sig_name = "PassAirbInjSts"
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
        sig_value_table = {'OffOnInvld_Invalid1': 0, 'OffOnInvld_Off': 1, 'OffOnInvld_On': 2, 'OffOnInvld_Invalid2': 3}
        compute_method = None
        length = 2
        startbit = 23
        byte = 2
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class NotifyForEmercyCall_UB:
        sig_name = "NotifyForEmercyCall_UB"
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


