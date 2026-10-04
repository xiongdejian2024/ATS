class SRSChassis1CANFDFr02:
    msg_name = "SRSChassis1CANFDFr02"
    msg_id = 163
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 64
    tx_node = "SRS"
    rx_nodes = ['PSCM1', 'SUM', 'CCUMCUAD', 'BCU1']
    sig_group_dict = {'IMUACmpData': ['IMUACmpDataChks', 'IMUACmpDataCntr', 'IMUACmpDataLat', 'IMUACmpDataLatQf', 'IMUACmpDataLgt', 'IMUACmpDataLgtQf', 'IMUACmpDataVert', 'IMUACmpDataVertQf'], 'IMUARawData': ['IMUARawDataChks', 'IMUARawDataCntr', 'IMUARawDataLat', 'IMUARawDataLatQf', 'IMUARawDataLgt', 'IMUARawDataLgtQf', 'IMUARawDataVert', 'IMUARawDataVertQf'], 'IMUAgCmpData': ['IMUAgCmpDataChks', 'IMUAgCmpDataCntr', 'IMUAgCmpDataPitch', 'IMUAgCmpDataPitchQf', 'IMUAgCmpDataRoll', 'IMUAgCmpDataRollQf', 'IMUAgCmpDataYaw', 'IMUAgCmpDataYawQf'], 'RestrntSysUnitSerlNr': ['RestrntSysUnitSerlNrByte0', 'RestrntSysUnitSerlNrByte1', 'RestrntSysUnitSerlNrByte2', 'RestrntSysUnitSerlNrByte3', 'RestrntSysUnitSerlNrByte4', 'RestrntSysUnitSerlNrByte5', 'RestrntSysUnitSerlNrByte6', 'RestrntSysUnitSerlNrByte7'], 'IMUAgRawData': ['IMUAgRawDataChks', 'IMUAgRawDataCntr', 'IMUAgRawDataPitch', 'IMUAgRawDataPitchQf', 'IMUAgRawDataRoll', 'IMUAgRawDataRollQf', 'IMUAgRawDataYaw', 'IMUAgRawDataYawQf']}
    sig_group_dataid_dict = {}

    class IMUAgCmpDataPitchQf:
        sig_name = "IMUAgCmpDataPitchQf"
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

    class RestrntSysUnitSerlNrByte2:
        sig_name = "RestrntSysUnitSerlNrByte2"
        sig_start_bit = 311
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 311
        byte = 38
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class IMUACmpDataVertQf:
        sig_name = "IMUACmpDataVertQf"
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
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 71
        byte = 8
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class RestrntSysUnitSerlNrByte3:
        sig_name = "RestrntSysUnitSerlNrByte3"
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

    class IMUAgRawDataCntr:
        sig_name = "IMUAgRawDataCntr"
        sig_start_bit = 155
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
        startbit = 155
        byte = 19
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class IMUACmpDataLgt:
        sig_name = "IMUACmpDataLgt"
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

    class IMUACmpDataLatQf:
        sig_name = "IMUACmpDataLatQf"
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
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 15
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class IMUAgRawDataPitch:
        sig_name = "IMUAgRawDataPitch"
        sig_start_bit = 167
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
        startbit = 167
        bmuws_info = [(20, 0b11111111, 0b00000000, 8, 0), (21, 0b11111111, 0b00000000, 8, 0)]

    class IMUACmpData_UB:
        sig_name = "IMUACmpData_UB"
        sig_start_bit = 69
        update_id_bit = 69
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 69
        byte = 8
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class IMUAgCmpDataPitch:
        sig_name = "IMUAgCmpDataPitch"
        sig_start_bit = 95
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
        startbit = 95
        bmuws_info = [(11, 0b11111111, 0b00000000, 8, 0), (12, 0b11111111, 0b00000000, 8, 0)]

    class IMUAgRawDataRollQf:
        sig_name = "IMUAgRawDataRollQf"
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
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 157
        byte = 19
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class RestrntSysUnitSerlNrByte7:
        sig_name = "RestrntSysUnitSerlNrByte7"
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

    class RestrntSysUnitSerlNrByte4:
        sig_name = "RestrntSysUnitSerlNrByte4"
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

    class IMUARawDataVert:
        sig_name = "IMUARawDataVert"
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

    class IMUAgCmpDataYawQf:
        sig_name = "IMUAgCmpDataYawQf"
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

    class RestrntSysUnitSerlNrByte1:
        sig_name = "RestrntSysUnitSerlNrByte1"
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

    class IMUACmpDataLgtQf:
        sig_name = "IMUACmpDataLgtQf"
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
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 13
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class IMUAgCmpDataRollQf:
        sig_name = "IMUAgCmpDataRollQf"
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
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 85
        byte = 10
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class IMUACmpDataChks:
        sig_name = "IMUACmpDataChks"
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

    class IMUARawDataCntr:
        sig_name = "IMUARawDataCntr"
        sig_start_bit = 227
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
        startbit = 227
        byte = 28
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class IMUAgCmpDataCntr:
        sig_name = "IMUAgCmpDataCntr"
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

    class IMUARawData_UB:
        sig_name = "IMUARawData_UB"
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

    class RestrntSysUnitSerlNrByte0:
        sig_name = "RestrntSysUnitSerlNrByte0"
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

    class IMUAgRawDataRoll:
        sig_name = "IMUAgRawDataRoll"
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

    class IMUARawDataLatQf:
        sig_name = "IMUARawDataLatQf"
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

    class IMUACmpDataVert:
        sig_name = "IMUACmpDataVert"
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

    class RestrntSysUnitSerlNrByte6:
        sig_name = "RestrntSysUnitSerlNrByte6"
        sig_start_bit = 343
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 343
        byte = 42
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class IMUARawDataLgtQf:
        sig_name = "IMUARawDataLgtQf"
        sig_start_bit = 229
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
        startbit = 229
        byte = 28
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class IMUAgCmpDataYaw:
        sig_name = "IMUAgCmpDataYaw"
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

    class IMUAgCmpDataChks:
        sig_name = "IMUAgCmpDataChks"
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

    class IMUAgRawDataPitchQf:
        sig_name = "IMUAgRawDataPitchQf"
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

    class IMUAgCmpDataRoll:
        sig_name = "IMUAgCmpDataRoll"
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

    class IMUAgRawDataYawQf:
        sig_name = "IMUAgRawDataYawQf"
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
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 215
        byte = 26
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class IMUACmpDataLat:
        sig_name = "IMUACmpDataLat"
        sig_start_bit = 23
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
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111110, 0b00000001, 7, 1)]

    class IMUACmpDataCntr:
        sig_name = "IMUACmpDataCntr"
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

    class IMUAgCmpData_UB:
        sig_name = "IMUAgCmpData_UB"
        sig_start_bit = 141
        update_id_bit = 141
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 141
        byte = 17
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class RestrntSysUnitSerlNrByte5:
        sig_name = "RestrntSysUnitSerlNrByte5"
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

    class IMUARawDataChks:
        sig_name = "IMUARawDataChks"
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

    class IMUARawDataLat:
        sig_name = "IMUARawDataLat"
        sig_start_bit = 239
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
        startbit = 239
        bmuws_info = [(29, 0b11111111, 0b00000000, 8, 0), (30, 0b11111110, 0b00000001, 7, 1)]

    class RestrntSysUnitSerlNr_UB:
        sig_name = "RestrntSysUnitSerlNr_UB"
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

    class IMUAgRawData_UB:
        sig_name = "IMUAgRawData_UB"
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

    class IMUAgRawDataChks:
        sig_name = "IMUAgRawDataChks"
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

    class IMUARawDataVertQf:
        sig_name = "IMUARawDataVertQf"
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
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 287
        byte = 35
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class IMUAgRawDataYaw:
        sig_name = "IMUAgRawDataYaw"
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

    class IMUARawDataLgt:
        sig_name = "IMUARawDataLgt"
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


class CCUMCUADChassis1CANFDFr08:
    msg_name = "CCUMCUADChassis1CANFDFr08"
    msg_id = 1104
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 1.0
    msg_length = 8
    tx_node = "CCUMCUAD"
    rx_nodes = ['SUM']
    sig_group_dict = {'AmbPBasLocn': ['AmbPBasLocnP', 'AmbPBasLocnPQf']}
    sig_group_dataid_dict = {}

    class AmbPBasLocnP:
        sig_name = "AmbPBasLocnP"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 0.025
        sig_value_offset = 0
        sig_value_min = 10400
        sig_value_max = 50400
        sig_byteorder = "Motorola"
        sig_value_init = 40520
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class AmbPBasLocn_UB:
        sig_name = "AmbPBasLocn_UB"
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

    class AmbPBasLocnPQf:
        sig_name = "AmbPBasLocnPQf"
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
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 23
        byte = 2
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class CCUMCUADChassis1CANFDFr09:
    msg_name = "CCUMCUADChassis1CANFDFr09"
    msg_id = 16
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 12
    tx_node = "CCUMCUAD"
    rx_nodes = ['SUM']
    sig_group_dict = {'Objlnfo2': ['Objlnfo2ObjConfidenceLvl', 'Objlnfo2ObjDst1', 'Objlnfo2ObjDst2', 'Objlnfo2ObjHei', 'Objlnfo2ObjSide', 'Objlnfo2ObjTypMai']}
    sig_group_dataid_dict = {}

    class Objlnfo2ObjDst1:
        sig_name = "Objlnfo2ObjDst1"
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

    class Objlnfo2ObjHei:
        sig_name = "Objlnfo2ObjHei"
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
        sig_value_table = {'SumRoadTyp1_None': 0, 'SumRoadTyp1_Smooth': 1, 'SumRoadTyp1_Medium': 2, 'SumRoadTyp1_Rough': 3, 'SumRoadTyp1_Reserved0': 4, 'SumRoadTyp1_Reserved1': 5, 'SumRoadTyp1_Reserved2': 6, 'SumRoadTyp1_Reserved3': 7, 'SumRoadTyp1_Reserved4': 8, 'SumRoadTyp1_Reserved5': 9, 'SumRoadTyp1_Reserved6': 10, 'SumRoadTyp1_Reserved7': 11, 'SumRoadTyp1_Reserved8': 12, 'SumRoadTyp1_Reserved9': 13, 'SumRoadTyp1_Reserved10': 14, 'SumRoadTyp1_Reserved11': 15}
        compute_method = None
        length = 4
        startbit = 55
        byte = 6
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

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
        sig_value_table = {'SumSnsrSts1_NA': 0, 'SumSnsrSts1_Active': 1, 'SumSnsrSts1_Idle': 2, 'SumSnsrSts1_Error': 3, 'SumSnsrSts1_Off': 4, 'SumSnsrSts1_Reserved1': 5, 'SumSnsrSts1_Reserved2': 6, 'SumSnsrSts1_Reserved3': 7}
        compute_method = None
        length = 3
        startbit = 50
        byte = 6
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class Objlnfo2ObjSide:
        sig_name = "Objlnfo2ObjSide"
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

    class Objlnfo2ObjDst2:
        sig_name = "Objlnfo2ObjDst2"
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

    class Objlnfo2ObjTypMai:
        sig_name = "Objlnfo2ObjTypMai"
        sig_start_bit = 27
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ObjTypMai_None': 0, 'ObjTypMai_Bump': 1, 'ObjTypMai_Manhole': 2, 'ObjTypMai_Pothole': 3, 'ObjTypMai_Step': 4, 'ObjTypMai_Reserved1': 5, 'ObjTypMai_Reserved2': 6, 'ObjTypMai_Reserved3': 7, 'ObjTypMai_Reserved4': 8, 'ObjTypMai_Reserved5': 9, 'ObjTypMai_Reserved6': 10, 'ObjTypMai_Reserved7': 11, 'ObjTypMai_Reserved8': 12, 'ObjTypMai_Reserved9': 13, 'ObjTypMai_Reserved10': 14, 'ObjTypMai_Reserved11': 15}
        compute_method = None
        length = 4
        startbit = 27
        byte = 3
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class Objlnfo2ObjConfidenceLvl:
        sig_name = "Objlnfo2ObjConfidenceLvl"
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

    class Objlnfo2_UB:
        sig_name = "Objlnfo2_UB"
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


class SRSChassis1CANFDFr03:
    msg_name = "SRSChassis1CANFDFr03"
    msg_id = 289
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.03
    msg_length = 8
    tx_node = "SRS"
    rx_nodes = ['CCUMCUAD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class BrkPedlCrashSts:
        sig_name = "BrkPedlCrashSts"
        sig_start_bit = 7
        update_id_bit = 5
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BeltCrashSts_Invalid': 0, 'BeltCrashSts_NotActvn': 1, 'BeltCrashSts_Actvn': 2}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class BCU1Chassis1CANFDFr03:
    msg_name = "BCU1Chassis1CANFDFr03"
    msg_id = 320
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.04
    msg_length = 64
    tx_node = "BCU1"
    rx_nodes = ['ETC', 'PSCM1', 'SUM', 'CCUMCUAD']
    sig_group_dict = {'AbsWhlActv': ['AbsWhlActvFL', 'AbsWhlActvFR', 'AbsWhlActvRL', 'AbsWhlActvRR'], 'TcsSts': ['TcsStsActv', 'TcsStsChks', 'TcsStsCntr', 'TcsStsEna', 'TcsStsSts2'], 'HbaSts': ['HbaStsActv', 'HbaStsChks', 'HbaStsCntr', 'HbaStsEna', 'HbaStsSts2'], 'HhcSts': ['HhcStsActv', 'HhcStsChks', 'HhcStsCntr', 'HhcStsEna', 'HhcStsSts2'], 'HbcSts': ['HbcStsActv', 'HbcStsChks', 'HbcStsCntr', 'HbcStsEna', 'HbcStsSts2'], 'HfcSts': ['HfcStsActv', 'HfcStsChks', 'HfcStsCntr', 'HfcStsEna', 'HfcStsSts2'], 'EblSts': ['EblStsActv', 'EblStsChks', 'EblStsCntr', 'EblStsEna', 'EblStsSts2'], 'BdwSts': ['BdwStsActv', 'BdwStsChks', 'BdwStsCntr', 'BdwStsEna', 'BdwStsSts2'], 'TscSts': ['TscStsActv', 'TscStsChks', 'TscStsCntr', 'TscStsEna', 'TscStsSts2'], 'AbsSysWarnReq': ['AbsSysWarnReqAbs', 'AbsSysWarnReqChks', 'AbsSysWarnReqCntr', 'AbsSysWarnReqEbd'], 'ArpSts': ['ArpStsActv', 'ArpStsChks', 'ArpStsCntr', 'ArpStsEna', 'ArpStsSts2'], 'VdcSts': ['VdcStsActv', 'VdcStsChks', 'VdcStsCntr', 'VdcStsEna', 'VdcStsSts2'], 'EbpSts': ['EbpStsActv', 'EbpStsChks', 'EbpStsCntr', 'EbpStsEna', 'EbpStsSts2'], 'EscSysWarnReq': ['EscSysWarnReqChks', 'EscSysWarnReqCntr', 'EscSysWarnReqEscSysWarn'], 'AbsFctSts': ['AbsFctStsActv', 'AbsFctStsChks', 'AbsFctStsCntr', 'AbsFctStsEna', 'AbsFctStsSts2'], 'HrbSts': ['HrbStsActv', 'HrbStsChks', 'HrbStsCntr', 'HrbStsEna', 'HrbStsSts2'], 'DtcSts': ['DtcStsActv', 'DtcStsChks', 'DtcStsCntr', 'DtcStsEna', 'DtcStsSts2'], 'ScmSts': ['ScmStsActv', 'ScmStsChks', 'ScmStsCntr', 'ScmStsEna', 'ScmStsSts2'], 'WhlBrkP': ['WhlBrkPFL', 'WhlBrkPFR', 'WhlBrkPRL', 'WhlBrkPRR'], 'HbbSts': ['HbbStsActv', 'HbbStsChks', 'HbbStsCntr', 'HbbStsEna', 'HbbStsSts2'], 'DtvSts': ['DtvStsActv', 'DtvStsChks', 'DtvStsCntr', 'DtvStsEna', 'DtvStsSts2'], 'EbdSts': ['EbdStsActv', 'EbdStsChks', 'EbdStsCntr', 'EbdStsEna', 'EbdStsSts2']}
    sig_group_dataid_dict = {}

    class EbdStsEna:
        sig_name = "EbdStsEna"
        sig_start_bit = 159
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
        startbit = 159
        byte = 19
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class HbaStsEna:
        sig_name = "HbaStsEna"
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
        sig_value_table = {'EnableDisable2_Disabled': 0, 'EnableDisable2_Enabled': 1}
        compute_method = None
        length = 1
        startbit = 247
        byte = 30
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class BdwStsSts2:
        sig_name = "BdwStsSts2"
        sig_start_bit = 86
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
        startbit = 86
        byte = 10
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class AbsWhlActv_UB:
        sig_name = "AbsWhlActv_UB"
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

    class TscStsActv:
        sig_name = "TscStsActv"
        sig_start_bit = 415
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
        startbit = 415
        byte = 51
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class TcsSts_UB:
        sig_name = "TcsSts_UB"
        sig_start_bit = 385
        update_id_bit = 385
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 385
        byte = 48
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class TscStsChks:
        sig_name = "TscStsChks"
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

    class LgtStbIntvIndcn:
        sig_name = "LgtStbIntvIndcn"
        sig_start_bit = 139
        update_id_bit = 137
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
        startbit = 139
        byte = 17
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class ArpStsChks:
        sig_name = "ArpStsChks"
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

    class TcsStsChks:
        sig_name = "TcsStsChks"
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

    class ScmLigtReq:
        sig_name = "ScmLigtReq"
        sig_start_bit = 211
        update_id_bit = 210
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
        startbit = 211
        byte = 26
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class HrbStsEna:
        sig_name = "HrbStsEna"
        sig_start_bit = 331
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
        startbit = 331
        byte = 41
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class HbaSts_UB:
        sig_name = "HbaSts_UB"
        sig_start_bit = 253
        update_id_bit = 253
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 253
        byte = 31
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class HhcSts_UB:
        sig_name = "HhcSts_UB"
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

    class VdcStsActv:
        sig_name = "VdcStsActv"
        sig_start_bit = 427
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
        startbit = 427
        byte = 53
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class TscStsCntr:
        sig_name = "TscStsCntr"
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

    class HbcSts_UB:
        sig_name = "HbcSts_UB"
        sig_start_bit = 293
        update_id_bit = 293
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 293
        byte = 36
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class ArpStsSts2:
        sig_name = "ArpStsSts2"
        sig_start_bit = 62
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
        startbit = 62
        byte = 7
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class AbsFctStsCntr:
        sig_name = "AbsFctStsCntr"
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

    class PTCActvRe:
        sig_name = "PTCActvRe"
        sig_start_bit = 187
        update_id_bit = 185
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
        startbit = 187
        byte = 23
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VdcStsEna:
        sig_name = "VdcStsEna"
        sig_start_bit = 411
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
        startbit = 411
        byte = 51
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

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

    class HfcSts_UB:
        sig_name = "HfcSts_UB"
        sig_start_bit = 305
        update_id_bit = 305
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 305
        byte = 38
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class HbcStsActv:
        sig_name = "HbcStsActv"
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
        sig_value_table = {'Actv_NoActv': 0, 'Actv_Actv': 1, 'Actv_Reserved1': 2, 'Actv_Reserved2': 3}
        compute_method = None
        length = 2
        startbit = 295
        byte = 36
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class ScmStsSts2:
        sig_name = "ScmStsSts2"
        sig_start_bit = 366
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
        startbit = 366
        byte = 45
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class EblSts_UB:
        sig_name = "EblSts_UB"
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

    class HbbStsActv:
        sig_name = "HbbStsActv"
        sig_start_bit = 267
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
        startbit = 267
        byte = 33
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class HbaStsChks:
        sig_name = "HbaStsChks"
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

    class BdwStsCntr:
        sig_name = "BdwStsCntr"
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

    class BdwSts_UB:
        sig_name = "BdwSts_UB"
        sig_start_bit = 93
        update_id_bit = 93
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 93
        byte = 11
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class HhcStsActv:
        sig_name = "HhcStsActv"
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
        sig_value_table = {'Actv_NoActv': 0, 'Actv_Actv': 1, 'Actv_Reserved1': 2, 'Actv_Reserved2': 3}
        compute_method = None
        length = 2
        startbit = 335
        byte = 41
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class TscSts_UB:
        sig_name = "TscSts_UB"
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

    class HbbStsChks:
        sig_name = "HbbStsChks"
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

    class PTCActvFrnt:
        sig_name = "PTCActvFrnt"
        sig_start_bit = 163
        update_id_bit = 161
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
        startbit = 163
        byte = 20
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class HhcStsSts2:
        sig_name = "HhcStsSts2"
        sig_start_bit = 326
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
        startbit = 326
        byte = 40
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class HrbStsActv:
        sig_name = "HrbStsActv"
        sig_start_bit = 347
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
        startbit = 347
        byte = 43
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class HhcStsChks:
        sig_name = "HhcStsChks"
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

    class HbbStsSts2:
        sig_name = "HbbStsSts2"
        sig_start_bit = 250
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
        startbit = 250
        byte = 31
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class AbsFctStsSts2:
        sig_name = "AbsFctStsSts2"
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
        sig_value_table = {'Sts2_Initial': 0, 'Sts2_Normal': 1, 'Sts2_Fault': 2, 'Sts2_Off': 3}
        compute_method = None
        length = 3
        startbit = 14
        byte = 1
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class DtvStsSts2:
        sig_name = "DtvStsSts2"
        sig_start_bit = 134
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
        startbit = 134
        byte = 16
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class WhlBrkPFL:
        sig_name = "WhlBrkPFL"
        sig_start_bit = 439
        update_id_bit = None
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
        startbit = 439
        byte = 54
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class AbsWhlActvRL:
        sig_name = "AbsWhlActvRL"
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
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 45
        byte = 5
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class TscStsSts2:
        sig_name = "TscStsSts2"
        sig_start_bit = 406
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
        startbit = 406
        byte = 50
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class HhcStsEna:
        sig_name = "HhcStsEna"
        sig_start_bit = 327
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
        startbit = 327
        byte = 40
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ScmStsActv:
        sig_name = "ScmStsActv"
        sig_start_bit = 375
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
        startbit = 375
        byte = 46
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HfcStsChks:
        sig_name = "HfcStsChks"
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

    class HfcStsEna:
        sig_name = "HfcStsEna"
        sig_start_bit = 291
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
        startbit = 291
        byte = 36
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class HbcStsEna:
        sig_name = "HbcStsEna"
        sig_start_bit = 287
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
        startbit = 287
        byte = 35
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class EblStsCntr:
        sig_name = "EblStsCntr"
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

    class ArpStsEna:
        sig_name = "ArpStsEna"
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
        sig_value_table = {'EnableDisable2_Disabled': 0, 'EnableDisable2_Enabled': 1}
        compute_method = None
        length = 1
        startbit = 63
        byte = 7
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class AbsSysWarnReq_UB:
        sig_name = "AbsSysWarnReq_UB"
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

    class HbbStsEna:
        sig_name = "HbbStsEna"
        sig_start_bit = 251
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
        startbit = 251
        byte = 31
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class HbaStsSts2:
        sig_name = "HbaStsSts2"
        sig_start_bit = 246
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
        startbit = 246
        byte = 30
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class EbpStsSts2:
        sig_name = "EbpStsSts2"
        sig_start_bit = 206
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
        startbit = 206
        byte = 25
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class WhlBrkPRL:
        sig_name = "WhlBrkPRL"
        sig_start_bit = 455
        update_id_bit = None
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
        startbit = 455
        byte = 56
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HbcStsCntr:
        sig_name = "HbcStsCntr"
        sig_start_bit = 283
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
        startbit = 283
        byte = 35
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DtcStsActv:
        sig_name = "DtcStsActv"
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
        sig_value_table = {'Actv_NoActv': 0, 'Actv_Actv': 1, 'Actv_Reserved1': 2, 'Actv_Reserved2': 3}
        compute_method = None
        length = 2
        startbit = 119
        byte = 14
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HrbStsChks:
        sig_name = "HrbStsChks"
        sig_start_bit = 343
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 343
        byte = 42
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HfcStsSts2:
        sig_name = "HfcStsSts2"
        sig_start_bit = 290
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
        startbit = 290
        byte = 36
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class AbsSysWarnReqAbs:
        sig_name = "AbsSysWarnReqAbs"
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
        sig_value_table = {'BrkLamp_Off': 0, 'BrkLamp_On': 1, 'BrkLamp_Flash': 2, 'BrkLamp_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 39
        byte = 4
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class EPBHpsAck:
        sig_name = "EPBHpsAck"
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
        sig_value_table = {'NoYes3_No': 0, 'NoYes3_Yes': 1}
        compute_method = None
        length = 1
        startbit = 20
        byte = 2
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class TcsStsSts2:
        sig_name = "TcsStsSts2"
        sig_start_bit = 370
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
        startbit = 370
        byte = 46
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class ArpSts_UB:
        sig_name = "ArpSts_UB"
        sig_start_bit = 69
        update_id_bit = 69
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 69
        byte = 8
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class EbdStsActv:
        sig_name = "EbdStsActv"
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

    class EblStsActv:
        sig_name = "EblStsActv"
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

    class DtvStsChks:
        sig_name = "DtvStsChks"
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

    class AbsSysWarnReqChks:
        sig_name = "AbsSysWarnReqChks"
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

    class TcsStsCntr:
        sig_name = "TcsStsCntr"
        sig_start_bit = 391
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
        startbit = 391
        byte = 48
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class HhcStsCntr:
        sig_name = "HhcStsCntr"
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

    class AbsWhlActvFR:
        sig_name = "AbsWhlActvFR"
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
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 46
        byte = 5
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class DtvStsActv:
        sig_name = "DtvStsActv"
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
        sig_value_table = {'Actv_NoActv': 0, 'Actv_Actv': 1, 'Actv_Reserved1': 2, 'Actv_Reserved2': 3}
        compute_method = None
        length = 2
        startbit = 143
        byte = 17
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class EscSuspReq:
        sig_name = "EscSuspReq"
        sig_start_bit = 91
        update_id_bit = 89
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EscSusReq_No': 0, 'EscSusReq_Handling': 1, 'EscSusReq_BrakeTrig': 2, 'EscSusReq_BrakeGrip': 3}
        compute_method = None
        length = 2
        startbit = 91
        byte = 11
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class DtvStsEna:
        sig_name = "DtvStsEna"
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
        sig_value_table = {'EnableDisable2_Disabled': 0, 'EnableDisable2_Enabled': 1}
        compute_method = None
        length = 1
        startbit = 135
        byte = 16
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class HrbStsCntr:
        sig_name = "HrbStsCntr"
        sig_start_bit = 351
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
        startbit = 351
        byte = 43
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class HbaStsCntr:
        sig_name = "HbaStsCntr"
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

    class VdcSts_UB:
        sig_name = "VdcSts_UB"
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

    class WhlBrkPRR:
        sig_name = "WhlBrkPRR"
        sig_start_bit = 463
        update_id_bit = None
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
        startbit = 463
        byte = 57
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class EbpStsEna:
        sig_name = "EbpStsEna"
        sig_start_bit = 207
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
        startbit = 207
        byte = 25
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class EscSysWarnReqCntr:
        sig_name = "EscSysWarnReqCntr"
        sig_start_bit = 227
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
        startbit = 227
        byte = 28
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class EbpStsChks:
        sig_name = "EbpStsChks"
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

    class HbbStsCntr:
        sig_name = "HbbStsCntr"
        sig_start_bit = 271
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
        startbit = 271
        byte = 33
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class VdcStsSts2:
        sig_name = "VdcStsSts2"
        sig_start_bit = 410
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
        startbit = 410
        byte = 51
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class EbpStsActv:
        sig_name = "EbpStsActv"
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

    class AbsFctStsEna:
        sig_name = "AbsFctStsEna"
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

    class HbcStsChks:
        sig_name = "HbcStsChks"
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

    class BdwStsEna:
        sig_name = "BdwStsEna"
        sig_start_bit = 87
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
        startbit = 87
        byte = 10
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class EbpSts_UB:
        sig_name = "EbpSts_UB"
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

    class EscSysWarnReq_UB:
        sig_name = "EscSysWarnReq_UB"
        sig_start_bit = 228
        update_id_bit = 228
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 228
        byte = 28
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

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

    class HrbSts_UB:
        sig_name = "HrbSts_UB"
        sig_start_bit = 345
        update_id_bit = 345
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 345
        byte = 43
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class EblStsChks:
        sig_name = "EblStsChks"
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

    class AbsWhlActvRR:
        sig_name = "AbsWhlActvRR"
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
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 44
        byte = 5
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class DtcSts_UB:
        sig_name = "DtcSts_UB"
        sig_start_bit = 117
        update_id_bit = 117
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 117
        byte = 14
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class TcsStsActv:
        sig_name = "TcsStsActv"
        sig_start_bit = 387
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
        startbit = 387
        byte = 48
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class EscOffSts:
        sig_name = "EscOffSts"
        sig_start_bit = 67
        update_id_bit = 64
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EscOff_Init': 0, 'EscOff_ok': 1, 'EscOff_Fault': 2, 'EscOff_Off': 3}
        compute_method = None
        length = 3
        startbit = 67
        byte = 8
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class EbdStsChks:
        sig_name = "EbdStsChks"
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

    class EucActv:
        sig_name = "EucActv"
        sig_start_bit = 115
        update_id_bit = 113
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
        startbit = 115
        byte = 14
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class BdwStsChks:
        sig_name = "BdwStsChks"
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

    class DtcStsSts2:
        sig_name = "DtcStsSts2"
        sig_start_bit = 110
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
        startbit = 110
        byte = 13
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class AbsSysWarnReqEbd:
        sig_name = "AbsSysWarnReqEbd"
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
        sig_value_table = {'BrkLamp_Off': 0, 'BrkLamp_On': 1, 'BrkLamp_Flash': 2, 'BrkLamp_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 37
        byte = 4
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class DtcStsChks:
        sig_name = "DtcStsChks"
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

    class ScmSts_UB:
        sig_name = "ScmSts_UB"
        sig_start_bit = 373
        update_id_bit = 373
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 373
        byte = 46
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class ArpStsActv:
        sig_name = "ArpStsActv"
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
        sig_value_table = {'Actv_NoActv': 0, 'Actv_Actv': 1, 'Actv_Reserved1': 2, 'Actv_Reserved2': 3}
        compute_method = None
        length = 2
        startbit = 71
        byte = 8
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class TscStsEna:
        sig_name = "TscStsEna"
        sig_start_bit = 407
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
        startbit = 407
        byte = 50
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class HfcStsCntr:
        sig_name = "HfcStsCntr"
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

    class WhlBrkPFR:
        sig_name = "WhlBrkPFR"
        sig_start_bit = 447
        update_id_bit = None
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
        startbit = 447
        byte = 55
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class EscSysWarnReqChks:
        sig_name = "EscSysWarnReqChks"
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

    class HrbStsSts2:
        sig_name = "HrbStsSts2"
        sig_start_bit = 330
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
        startbit = 330
        byte = 41
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class DtcStsCntr:
        sig_name = "DtcStsCntr"
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

    class EblStsEna:
        sig_name = "EblStsEna"
        sig_start_bit = 183
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
        startbit = 183
        byte = 22
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class EPBHpsAvl:
        sig_name = "EPBHpsAvl"
        sig_start_bit = 18
        update_id_bit = 17
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
        startbit = 18
        byte = 2
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class EbpStsCntr:
        sig_name = "EbpStsCntr"
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

    class EscSysWarnReqEscSysWarn:
        sig_name = "EscSysWarnReqEscSysWarn"
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
        sig_value_table = {'BrkLamp_Off': 0, 'BrkLamp_On': 1, 'BrkLamp_Flash': 2, 'BrkLamp_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 231
        byte = 28
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class EbdStsSts2:
        sig_name = "EbdStsSts2"
        sig_start_bit = 158
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
        startbit = 158
        byte = 19
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class ScmStsEna:
        sig_name = "ScmStsEna"
        sig_start_bit = 367
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
        startbit = 367
        byte = 45
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class WhlBrkP_UB:
        sig_name = "WhlBrkP_UB"
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

    class ArpStsCntr:
        sig_name = "ArpStsCntr"
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

    class BdwStsActv:
        sig_name = "BdwStsActv"
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
        sig_value_table = {'Actv_NoActv': 0, 'Actv_Actv': 1, 'Actv_Reserved1': 2, 'Actv_Reserved2': 3}
        compute_method = None
        length = 2
        startbit = 95
        byte = 11
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class ScmStsChks:
        sig_name = "ScmStsChks"
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

    class HbcStsSts2:
        sig_name = "HbcStsSts2"
        sig_start_bit = 286
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
        startbit = 286
        byte = 35
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class DtcStsEna:
        sig_name = "DtcStsEna"
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
        sig_value_table = {'EnableDisable2_Disabled': 0, 'EnableDisable2_Enabled': 1}
        compute_method = None
        length = 1
        startbit = 111
        byte = 13
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class TcsStsEna:
        sig_name = "TcsStsEna"
        sig_start_bit = 371
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
        startbit = 371
        byte = 46
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class HbbSts_UB:
        sig_name = "HbbSts_UB"
        sig_start_bit = 265
        update_id_bit = 265
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 265
        byte = 33
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class AbsSysWarnReqCntr:
        sig_name = "AbsSysWarnReqCntr"
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

    class VdcStsChks:
        sig_name = "VdcStsChks"
        sig_start_bit = 423
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 423
        byte = 52
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DtvStsCntr:
        sig_name = "DtvStsCntr"
        sig_start_bit = 131
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
        startbit = 131
        byte = 16
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class VdcStsCntr:
        sig_name = "VdcStsCntr"
        sig_start_bit = 431
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
        startbit = 431
        byte = 53
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class HfcStsActv:
        sig_name = "HfcStsActv"
        sig_start_bit = 307
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
        startbit = 307
        byte = 38
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class DtvSts_UB:
        sig_name = "DtvSts_UB"
        sig_start_bit = 141
        update_id_bit = 141
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 141
        byte = 17
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class EbdSts_UB:
        sig_name = "EbdSts_UB"
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

    class HbaStsActv:
        sig_name = "HbaStsActv"
        sig_start_bit = 255
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
        startbit = 255
        byte = 31
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class AbsWhlActvFL:
        sig_name = "AbsWhlActvFL"
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
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 47
        byte = 5
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ScmStsCntr:
        sig_name = "ScmStsCntr"
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

    class EbdStsCntr:
        sig_name = "EbdStsCntr"
        sig_start_bit = 155
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
        startbit = 155
        byte = 19
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class EblStsSts2:
        sig_name = "EblStsSts2"
        sig_start_bit = 182
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
        startbit = 182
        byte = 22
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4


class CCUMCUADToBCU1Chassis1CANFDDiagReqFrame:
    msg_name = "CCUMCUADToBCU1Chassis1CANFDDiagReqFrame"
    msg_id = 1794
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "CCUMCUAD"
    rx_nodes = ['BCU1']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class SUMChassis1CANFDNmFr:
    msg_name = "SUMChassis1CANFDNmFr"
    msg_id = 1288
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "SUM"
    rx_nodes = ['SRS']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class SRSChassis1CANFDNmFr:
    msg_name = "SRSChassis1CANFDNmFr"
    msg_id = 1296
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "SRS"
    rx_nodes = ['PSCM1']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class CCUMCUADChassis1CANFDFr02:
    msg_name = "CCUMCUADChassis1CANFDFr02"
    msg_id = 161
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 64
    tx_node = "CCUMCUAD"
    rx_nodes = ['PSCM1', 'SUM', 'BCU1']
    sig_group_dict = {'AdfBrkReq': ['AdfBrkReqActvReq', 'AdfBrkReqChks', 'AdfBrkReqCntr', 'AdfBrkReqDeActvReq'], 'VmcHoldType': ['VmcHoldTypeChks', 'VmcHoldTypeCntr', 'VmcHoldTypeStandstilMgrSts'], 'SecBrkEpbReq': ['SecBrkEpbReqAppRel', 'SecBrkEpbReqChks', 'SecBrkEpbReqCntr'], 'VmcDrvoffReq': ['VmcDrvoffReqChks', 'VmcDrvoffReqCntr', 'VmcDrvoffReqReq'], 'AdfCtrlSts': ['AdfCtrlStsChks', 'AdfCtrlStsCntr', 'AdfCtrlStsColorSts', 'AdfCtrlStsCtrlSts', 'AdfCtrlStsDegraded', 'AdfCtrlStsMode'], 'VmcEpbAplReq': ['VmcEpbAplReqChks', 'VmcEpbAplReqCntr', 'VmcEpbAplReqReq'], 'AdfLatReq': ['AdfLatReqActvReq', 'AdfLatReqChks', 'AdfLatReqCntr', 'AdfLatReqDeActvReq'], 'VmcHoldReqToBcu': ['VmcHoldReqToBcuChks', 'VmcHoldReqToBcuCntr', 'VmcHoldReqToBcuReq'], 'AdfBrkCtrlReq': ['AdfBrkCtrlReqChks', 'AdfBrkCtrlReqCntr', 'AdfBrkCtrlReqCtrlSts', 'AdfBrkCtrlReqMode'], 'VmcEpbRelsReq': ['VmcEpbRelsReqChks', 'VmcEpbRelsReqCntr', 'VmcEpbRelsReqReq'], 'VmcSteerOvrdnAllwd': ['VmcSteerOvrdnAllwdChks', 'VmcSteerOvrdnAllwdCntr', 'VmcSteerOvrdnAllwdStrAllwdReq'], 'AdfLatCtrlReq': ['AdfLatCtrlReqChks', 'AdfLatCtrlReqCntr', 'AdfLatCtrlReqCtrlSts', 'AdfLatCtrlReqMode']}
    sig_group_dataid_dict = {}

    class BrkPedlCrvReq:
        sig_name = "BrkPedlCrvReq"
        sig_start_bit = 13
        update_id_bit = 10
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
        startbit = 13
        byte = 1
        mask = 0b00111000
        unmask = 0b11000111
        shift = 3

    class TscSet:
        sig_name = "TscSet"
        sig_start_bit = 46
        update_id_bit = 45
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EnableDisable_Enable': 0, 'EnableDisable_Disable': 1}
        compute_method = None
        length = 1
        startbit = 46
        byte = 5
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VmcEpbRelsReqReq:
        sig_name = "VmcEpbRelsReqReq"
        sig_start_bit = 184
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
        startbit = 184
        byte = 23
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class TcsBtcSet:
        sig_name = "TcsBtcSet"
        sig_start_bit = 38
        update_id_bit = 37
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EnableDisable_Enable': 0, 'EnableDisable_Disable': 1}
        compute_method = None
        length = 1
        startbit = 38
        byte = 4
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VmcHoldReqToBcuCntr:
        sig_name = "VmcHoldReqToBcuCntr"
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

    class FLDoorOpenClsSts:
        sig_name = "FLDoorOpenClsSts"
        sig_start_bit = 21
        update_id_bit = 19
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorSts_Unknow': 0, 'DoorSts_Open': 1, 'DoorSts_Close': 2}
        compute_method = None
        length = 2
        startbit = 21
        byte = 2
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class AdfBrkReq_UB:
        sig_name = "AdfBrkReq_UB"
        sig_start_bit = 86
        update_id_bit = 86
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 86
        byte = 10
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class AdfLatReqChks:
        sig_name = "AdfLatReqChks"
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

    class VmcHoldTypeStandstilMgrSts:
        sig_name = "VmcHoldTypeStandstilMgrSts"
        sig_start_bit = 219
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
        startbit = 219
        byte = 27
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class SecBrkEpbReqChks:
        sig_name = "SecBrkEpbReqChks"
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

    class AdfLatCtrlReqCtrlSts:
        sig_name = "AdfLatCtrlReqCtrlSts"
        sig_start_bit = 123
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
        startbit = 123
        byte = 15
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class AdfLatCtrlReqChks:
        sig_name = "AdfLatCtrlReqChks"
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

    class AdfCtrlStsColorSts:
        sig_name = "AdfCtrlStsColorSts"
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
        sig_value_table = {'ColorSts_Red': 0, 'ColorSts_Yellow': 1, 'ColorSts_Green': 2, 'ColorSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 85
        byte = 10
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class VmcEpbAplReqCntr:
        sig_name = "VmcEpbAplReqCntr"
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

    class AdfLatReqActvReq:
        sig_name = "AdfLatReqActvReq"
        sig_start_bit = 139
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
        startbit = 139
        byte = 17
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class VmcDrvoffReqCntr:
        sig_name = "VmcDrvoffReqCntr"
        sig_start_bit = 175
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
        startbit = 175
        byte = 21
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class AdfCtrlStsDegraded:
        sig_name = "AdfCtrlStsDegraded"
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

    class VmcHoldType_UB:
        sig_name = "VmcHoldType_UB"
        sig_start_bit = 216
        update_id_bit = 216
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 216
        byte = 27
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class TrSts:
        sig_name = "TrSts"
        sig_start_bit = 33
        update_id_bit = 47
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorSts_Unknow': 0, 'DoorSts_Open': 1, 'DoorSts_Close': 2}
        compute_method = None
        length = 2
        startbit = 33
        byte = 4
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class AdfBrkCtrlReqChks:
        sig_name = "AdfBrkCtrlReqChks"
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

    class FRDoorOpenClsSts:
        sig_name = "FRDoorOpenClsSts"
        sig_start_bit = 18
        update_id_bit = 16
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorSts_Unknow': 0, 'DoorSts_Open': 1, 'DoorSts_Close': 2}
        compute_method = None
        length = 2
        startbit = 18
        byte = 2
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class AdfBrkCtrlReqCntr:
        sig_name = "AdfBrkCtrlReqCntr"
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

    class AdfBrkCtrlReqMode:
        sig_name = "AdfBrkCtrlReqMode"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class AvhActvPattern:
        sig_name = "AvhActvPattern"
        sig_start_bit = 3
        update_id_bit = 0
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AvhActvPattern_AvhActvPattern0': 0, 'AvhActvPattern_AvhActvPattern1': 1, 'AvhActvPattern_AvhActvPattern2': 2, 'AvhActvPattern_AvhActvPattern3': 3}
        compute_method = None
        length = 3
        startbit = 3
        byte = 0
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class VmcEpbAplReqReq:
        sig_name = "VmcEpbAplReqReq"
        sig_start_bit = 168
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
        startbit = 168
        byte = 21
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class AdfBrkReqChks:
        sig_name = "AdfBrkReqChks"
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

    class AdfBrkCtrlReqCtrlSts:
        sig_name = "AdfBrkCtrlReqCtrlSts"
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
        sig_value_table = {'CtrlSts_Primary': 0, 'CtrlSts_Secondary': 1}
        compute_method = None
        length = 1
        startbit = 40
        byte = 5
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ArpSet:
        sig_name = "ArpSet"
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
        sig_value_table = {'EnableDisable_Enable': 0, 'EnableDisable_Disable': 1}
        compute_method = None
        length = 1
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class SecBrkEpbReq_UB:
        sig_name = "SecBrkEpbReq_UB"
        sig_start_bit = 156
        update_id_bit = 156
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 156
        byte = 19
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class CstSoftSwt:
        sig_name = "CstSoftSwt"
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
        sig_value_table = {'OnOff2_On': 0, 'OnOff2_Off': 1}
        compute_method = None
        length = 1
        startbit = 23
        byte = 2
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VmcEpbRelsReqChks:
        sig_name = "VmcEpbRelsReqChks"
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

    class AvhSoftSwt:
        sig_name = "AvhSoftSwt"
        sig_start_bit = 15
        update_id_bit = 14
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
        startbit = 15
        byte = 1
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class RRDoorOpenClsSts:
        sig_name = "RRDoorOpenClsSts"
        sig_start_bit = 25
        update_id_bit = 39
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorSts_Unknow': 0, 'DoorSts_Open': 1, 'DoorSts_Close': 2}
        compute_method = None
        length = 2
        startbit = 25
        byte = 3
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VmcHoldTypeChks:
        sig_name = "VmcHoldTypeChks"
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

    class VmcSteerOvrdnAllwdCntr:
        sig_name = "VmcSteerOvrdnAllwdCntr"
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

    class VmcDrvoffReq_UB:
        sig_name = "VmcDrvoffReq_UB"
        sig_start_bit = 170
        update_id_bit = 170
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 170
        byte = 21
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class AbsSet:
        sig_name = "AbsSet"
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
        sig_value_table = {'EnableDisable_Enable': 0, 'EnableDisable_Disable': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VmcHoldReqToBcuReq:
        sig_name = "VmcHoldReqToBcuReq"
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
        sig_value_table = {'ReqSts1_NotReqd': 0, 'ReqSts1_Reqd': 1}
        compute_method = None
        length = 1
        startbit = 223
        byte = 27
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class AdfLatCtrlReqMode:
        sig_name = "AdfLatCtrlReqMode"
        sig_start_bit = 107
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
        startbit = 107
        byte = 13
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class AdfCtrlSts_UB:
        sig_name = "AdfCtrlSts_UB"
        sig_start_bit = 110
        update_id_bit = 110
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 110
        byte = 13
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class AdfBrkReqActvReq:
        sig_name = "AdfBrkReqActvReq"
        sig_start_bit = 79
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
        startbit = 79
        byte = 9
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class AdfCtrlStsCtrlSts:
        sig_name = "AdfCtrlStsCtrlSts"
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
        sig_value_table = {'CtrlSts_Primary': 0, 'CtrlSts_Secondary': 1}
        compute_method = None
        length = 1
        startbit = 111
        byte = 13
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class AdfCtrlStsChks:
        sig_name = "AdfCtrlStsChks"
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

    class VmcDrvoffReqReq:
        sig_name = "VmcDrvoffReqReq"
        sig_start_bit = 171
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
        startbit = 171
        byte = 21
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class AdfBrkReqDeActvReq:
        sig_name = "AdfBrkReqDeActvReq"
        sig_start_bit = 87
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
        startbit = 87
        byte = 10
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VmcSteerOvrdnAllwdChks:
        sig_name = "VmcSteerOvrdnAllwdChks"
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

    class VmcEpbAplReq_UB:
        sig_name = "VmcEpbAplReq_UB"
        sig_start_bit = 169
        update_id_bit = 169
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 169
        byte = 21
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class AdfLatReq_UB:
        sig_name = "AdfLatReq_UB"
        sig_start_bit = 121
        update_id_bit = 121
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 121
        byte = 15
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class AdfCtrlStsCntr:
        sig_name = "AdfCtrlStsCntr"
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

    class VmcHoldReqToBcu_UB:
        sig_name = "VmcHoldReqToBcu_UB"
        sig_start_bit = 222
        update_id_bit = 222
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 222
        byte = 27
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class AdfBrkReqCntr:
        sig_name = "AdfBrkReqCntr"
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

    class VmcEpbAplReqChks:
        sig_name = "VmcEpbAplReqChks"
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

    class AdfBrkCtrlReq_UB:
        sig_name = "AdfBrkCtrlReq_UB"
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

    class AdfLatCtrlReqCntr:
        sig_name = "AdfLatCtrlReqCntr"
        sig_start_bit = 127
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
        startbit = 127
        byte = 15
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class VmcEpbRelsReqCntr:
        sig_name = "VmcEpbRelsReqCntr"
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

    class AdfLatReqCntr:
        sig_name = "AdfLatReqCntr"
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

    class HoodSts:
        sig_name = "HoodSts"
        sig_start_bit = 31
        update_id_bit = 29
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorSts_Unknow': 0, 'DoorSts_Open': 1, 'DoorSts_Close': 2}
        compute_method = None
        length = 2
        startbit = 31
        byte = 3
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class AdfLatReqDeActvReq:
        sig_name = "AdfLatReqDeActvReq"
        sig_start_bit = 120
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
        startbit = 120
        byte = 15
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class AdfCtrlStsMode:
        sig_name = "AdfCtrlStsMode"
        sig_start_bit = 99
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
        startbit = 99
        byte = 12
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class RLDoorOpenClsSts:
        sig_name = "RLDoorOpenClsSts"
        sig_start_bit = 28
        update_id_bit = 26
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorSts_Unknow': 0, 'DoorSts_Open': 1, 'DoorSts_Close': 2}
        compute_method = None
        length = 2
        startbit = 28
        byte = 3
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class VmcSteerOvrdnAllwdStrAllwdReq:
        sig_name = "VmcSteerOvrdnAllwdStrAllwdReq"
        sig_start_bit = 255
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
        startbit = 255
        byte = 31
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VmcDrvoffReqChks:
        sig_name = "VmcDrvoffReqChks"
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

    class VmcEpbRelsReq_UB:
        sig_name = "VmcEpbRelsReq_UB"
        sig_start_bit = 185
        update_id_bit = 185
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 185
        byte = 23
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class SecBrkEpbReqCntr:
        sig_name = "SecBrkEpbReqCntr"
        sig_start_bit = 155
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
        startbit = 155
        byte = 19
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class TcsPtcSet:
        sig_name = "TcsPtcSet"
        sig_start_bit = 36
        update_id_bit = 34
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TcsSet_None': 0, 'TcsSet_PtcDisable': 1, 'TcsSet_BtcDisable': 2, 'TcsSet_AllDisable': 3}
        compute_method = None
        length = 2
        startbit = 36
        byte = 4
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class VmcHoldReqToBcuChks:
        sig_name = "VmcHoldReqToBcuChks"
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

    class VmcSteerOvrdnAllwd_UB:
        sig_name = "VmcSteerOvrdnAllwd_UB"
        sig_start_bit = 254
        update_id_bit = 254
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 254
        byte = 31
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class SecBrkEpbReqAppRel:
        sig_name = "SecBrkEpbReqAppRel"
        sig_start_bit = 159
        update_id_bit = None
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
        startbit = 159
        byte = 19
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class VdcSet:
        sig_name = "VdcSet"
        sig_start_bit = 44
        update_id_bit = 43
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EnableDisable_Enable': 0, 'EnableDisable_Disable': 1}
        compute_method = None
        length = 1
        startbit = 44
        byte = 5
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VmcHoldTypeCntr:
        sig_name = "VmcHoldTypeCntr"
        sig_start_bit = 239
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
        startbit = 239
        byte = 29
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class AdfLatCtrlReq_UB:
        sig_name = "AdfLatCtrlReq_UB"
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

    class CrbSoftSwt:
        sig_name = "CrbSoftSwt"
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
        sig_value_table = {'OnOff2_On': 0, 'OnOff2_Off': 1}
        compute_method = None
        length = 1
        startbit = 9
        byte = 1
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1


class PSCM1Chassis1CANFDFr05:
    msg_name = "PSCM1Chassis1CANFDFr05"
    msg_id = 288
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.03
    msg_length = 8
    tx_node = "PSCM1"
    rx_nodes = ['CCUMCUAD']
    sig_group_dict = {'DrvrSteerInt': ['DrvrSteerIntChks', 'DrvrSteerIntCntr', 'DrvrSteerIntSts']}
    sig_group_dataid_dict = {'DrvrSteerInt': 1032}

    class DrvrSteerIntSts:
        sig_name = "DrvrSteerIntSts"
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
        sig_value_table = {'DrvrSteerIntSts_NoIntention': 0, 'DrvrSteerIntSts_WithIntention': 1}
        compute_method = None
        length = 1
        startbit = 15
        byte = 1
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class DrvrSteerInt_UB:
        sig_name = "DrvrSteerInt_UB"
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

    class DrvrSteerIntChks:
        sig_name = "DrvrSteerIntChks"
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

    class DrvrSteerIntCntr:
        sig_name = "DrvrSteerIntCntr"
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


class CCUMCUADChassis1CANFDFr01:
    msg_name = "CCUMCUADChassis1CANFDFr01"
    msg_id = 49
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 64
    tx_node = "CCUMCUAD"
    rx_nodes = ['ETC', 'PSCM1', 'SUM', 'BCU1']
    sig_group_dict = {'ADSMstAgCtrlTqLim': ['ADSMstAgCtrlTqLimChks', 'ADSMstAgCtrlTqLimCntr', 'ADSMstAgCtrlTqLimLowrLim', 'ADSMstAgCtrlTqLimUpperLim'], 'VmcPinionAgReq': ['VmcPinionAgReqChks', 'VmcPinionAgReqCntr', 'VmcPinionAgReqPinionReq'], 'EpbCoornSec': ['EpbCoornSecChks', 'EpbCoornSecCntr', 'EpbCoornSecCommunicationAvl', 'EpbCoornSecHostAvailabilityFull', 'EpbCoornSecHostAvailabilityRelOnly', 'EpbCoornSecReserved1', 'EpbCoornSecReserved2', 'EpbCoornSecReserved3', 'EpbCoornSecReserved4', 'EpbCoornSecReserved5', 'EpbCoornSecReserved6', 'EpbCoornSecReserved7'], 'VmcAgCtrlTqLim': ['VmcAgCtrlTqLimChks', 'VmcAgCtrlTqLimCntr', 'VmcAgCtrlTqLimLowrLim', 'VmcAgCtrlTqLimUpperLim'], 'PtSysWhlTqFrntAct': ['PtSysWhlTqFrntActChks', 'PtSysWhlTqFrntActCntr', 'PtSysWhlTqFrntActPtWhlTqActQf', 'PtSysWhlTqFrntActPtWhlTqFrntAct', 'PtSysWhlTqFrntActPtWhlTqFrntLeAct', 'PtSysWhlTqFrntActPtWhlTqFrntRiAct'], 'AccrPedlVal': ['AccrPedlValChks', 'AccrPedlValCntr', 'AccrPedlValPedlFild'], 'BrkSysStSecRdnt': ['BrkSysStSecRdntBrkSysSts', 'BrkSysStSecRdntChks', 'BrkSysStSecRdntCntr'], 'Objlnfo': ['ObjlnfoObjConfidenceLvl', 'ObjlnfoObjDst1', 'ObjlnfoObjDst2', 'ObjlnfoObjHei', 'ObjlnfoObjSide', 'ObjlnfoObjTypMai'], 'EPBHpsReqSec': ['EPBHpsReqSecChks', 'EPBHpsReqSecCntr', 'EPBHpsReqSecHpsReq'], 'VmcBrkTqReq': ['VmcBrkTqReqChks', 'VmcBrkTqReqCntr', 'VmcBrkTqReqGrdtNeg', 'VmcBrkTqReqGrdtPos', 'VmcBrkTqReqReq'], 'VMMGlbSig': ['VMMGlbSigCarModSts', 'VMMGlbSigChks', 'VMMGlbSigCntr', 'VMMGlbSigCnvincSubSts1', 'VMMGlbSigDrvgSubSts1', 'VMMGlbSigInactvSubSts1', 'VMMGlbSigLoBattModSts', 'VMMGlbSigUsgModSts'], 'ADSMstPinAgReq': ['ADSMstPinAgReqChks', 'ADSMstPinAgReqCntr', 'ADSMstPinAgReqReq'], 'GearLvrIndcnReal': ['GearLvrIndcnRealChks', 'GearLvrIndcnRealCntr', 'GearLvrIndcnRealGearLvrIndcn']}
    sig_group_dataid_dict = {'ADSMstAgCtrlTqLim': 1057, 'PtSysWhlTqFrntAct': 1011, 'VMMGlbSig': 1074, 'ADSMstPinAgReq': 1058, 'GearLvrIndcnReal': 1065}

    class VmcAgCtrlTqLimLowrLim:
        sig_name = "VmcAgCtrlTqLimLowrLim"
        sig_start_bit = 347
        update_id_bit = None
        sig_length = 9
        sig_value_factor = 0.125
        sig_value_offset = -30.0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 240
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 347
        bmuws_info = [(43, 0b00001111, 0b11110000, 4, 0), (44, 0b11111000, 0b00000111, 5, 3)]

    class ADSMstAgCtrlTqLim_UB:
        sig_name = "ADSMstAgCtrlTqLim_UB"
        sig_start_bit = 57
        update_id_bit = 57
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 57
        byte = 7
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class EpbCoornSecHostAvailabilityRelOnly:
        sig_name = "EpbCoornSecHostAvailabilityRelOnly"
        sig_start_bit = 149
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CoornSt_Inactive': 0, 'CoornSt_Active': 1}
        compute_method = None
        length = 1
        startbit = 149
        byte = 18
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class AccrPedlValChks:
        sig_name = "AccrPedlValChks"
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

    class VmcPinionAgReq_UB:
        sig_name = "VmcPinionAgReq_UB"
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

    class VmcBrkTqReqGrdtNeg:
        sig_name = "VmcBrkTqReqGrdtNeg"
        sig_start_bit = 379
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 300
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2048
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 379
        bmuws_info = [(47, 0b00001111, 0b11110000, 4, 0), (48, 0b11111110, 0b00000001, 7, 1)]

    class VMMGlbSigLoBattModSts:
        sig_name = "VMMGlbSigLoBattModSts"
        sig_start_bit = 491
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
        startbit = 491
        byte = 61
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VmcAgCtrlTqLimUpperLim:
        sig_name = "VmcAgCtrlTqLimUpperLim"
        sig_start_bit = 354
        update_id_bit = None
        sig_length = 9
        sig_value_factor = 0.125
        sig_value_offset = -30.0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 240
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 354
        bmuws_info = [(44, 0b00000111, 0b11111000, 3, 0), (45, 0b11111100, 0b00000011, 6, 2)]

    class BrkSysStSecRdntChks:
        sig_name = "BrkSysStSecRdntChks"
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

    class PtSysWhlTqFrntActPtWhlTqFrntAct:
        sig_name = "PtSysWhlTqFrntActPtWhlTqFrntAct"
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

    class EpbCoornSec_UB:
        sig_name = "EpbCoornSec_UB"
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

    class VMMGlbSigCnvincSubSts1:
        sig_name = "VMMGlbSigCnvincSubSts1"
        sig_start_bit = 471
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
        startbit = 471
        byte = 58
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class EPBHpsReqSecChks:
        sig_name = "EPBHpsReqSecChks"
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

    class PtSysWhlTqFrntActPtWhlTqActQf:
        sig_name = "PtSysWhlTqFrntActPtWhlTqActQf"
        sig_start_bit = 271
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
        startbit = 271
        byte = 33
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class EpbCoornSecReserved2:
        sig_name = "EpbCoornSecReserved2"
        sig_start_bit = 159
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CoornSt_Inactive': 0, 'CoornSt_Active': 1}
        compute_method = None
        length = 1
        startbit = 159
        byte = 19
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class PtSysWhlTqFrntActChks:
        sig_name = "PtSysWhlTqFrntActChks"
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

    class VmcAgCtrlTqLim_UB:
        sig_name = "VmcAgCtrlTqLim_UB"
        sig_start_bit = 361
        update_id_bit = 361
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 361
        byte = 45
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VmcAgCtrlTqLimChks:
        sig_name = "VmcAgCtrlTqLimChks"
        sig_start_bit = 343
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 343
        byte = 42
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class PrpsnTqReAxleReq:
        sig_name = "PrpsnTqReAxleReq"
        sig_start_bit = 236
        update_id_bit = 253
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
        startbit = 236
        bmuws_info = [(29, 0b00011111, 0b11100000, 5, 0), (30, 0b11111111, 0b00000000, 8, 0), (31, 0b11000000, 0b00111111, 2, 6)]

    class VMMGlbSigCntr:
        sig_name = "VMMGlbSigCntr"
        sig_start_bit = 459
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
        startbit = 459
        byte = 57
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class PtSysWhlTqFrntAct_UB:
        sig_name = "PtSysWhlTqFrntAct_UB"
        sig_start_bit = 268
        update_id_bit = 268
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 268
        byte = 33
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class ObjlnfoObjDst2:
        sig_name = "ObjlnfoObjDst2"
        sig_start_bit = 197
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
        startbit = 197
        bmuws_info = [(24, 0b00111111, 0b11000000, 6, 0), (25, 0b11110000, 0b00001111, 4, 4)]

    class BrkSysStSecRdntBrkSysSts:
        sig_name = "BrkSysStSecRdntBrkSysSts"
        sig_start_bit = 111
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
        startbit = 111
        byte = 13
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class EpbCoornSecReserved4:
        sig_name = "EpbCoornSecReserved4"
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
        sig_value_table = {'CoornSt_Inactive': 0, 'CoornSt_Active': 1}
        compute_method = None
        length = 1
        startbit = 157
        byte = 19
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class EpbCoornSecHostAvailabilityFull:
        sig_name = "EpbCoornSecHostAvailabilityFull"
        sig_start_bit = 150
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CoornSt_Inactive': 0, 'CoornSt_Active': 1}
        compute_method = None
        length = 1
        startbit = 150
        byte = 18
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class LCDeactvnReq:
        sig_name = "LCDeactvnReq"
        sig_start_bit = 114
        update_id_bit = 112
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
        startbit = 114
        byte = 14
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class ADSMstAgCtrlTqLimUpperLim:
        sig_name = "ADSMstAgCtrlTqLimUpperLim"
        sig_start_bit = 50
        update_id_bit = None
        sig_length = 9
        sig_value_factor = 0.125
        sig_value_offset = -30.0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 480
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 50
        bmuws_info = [(6, 0b00000111, 0b11111000, 3, 0), (7, 0b11111100, 0b00000011, 6, 2)]

    class UsgModSts:
        sig_name = "UsgModSts"
        sig_start_bit = 323
        update_id_bit = 335
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
        startbit = 323
        byte = 40
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class VMMGlbSigDrvgSubSts1:
        sig_name = "VMMGlbSigDrvgSubSts1"
        sig_start_bit = 479
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
        startbit = 479
        byte = 59
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class EpbCoornSecReserved6:
        sig_name = "EpbCoornSecReserved6"
        sig_start_bit = 155
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CoornSt_Inactive': 0, 'CoornSt_Active': 1}
        compute_method = None
        length = 1
        startbit = 155
        byte = 19
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class AccrPedlVal_UB:
        sig_name = "AccrPedlVal_UB"
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

    class BrkSysStSecRdnt_UB:
        sig_name = "BrkSysStSecRdnt_UB"
        sig_start_bit = 119
        update_id_bit = 119
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 119
        byte = 14
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class Objlnfo_UB:
        sig_name = "Objlnfo_UB"
        sig_start_bit = 221
        update_id_bit = 221
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 221
        byte = 27
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class PtSysWhlTqFrntActCntr:
        sig_name = "PtSysWhlTqFrntActCntr"
        sig_start_bit = 267
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
        startbit = 267
        byte = 33
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class VmcPinionAgReqPinionReq:
        sig_name = "VmcPinionAgReqPinionReq"
        sig_start_bit = 439
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 0.000976563
        sig_value_offset = 0
        sig_value_min = -16384
        sig_value_max = 16383
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 439
        bmuws_info = [(54, 0b11111111, 0b00000000, 8, 0), (55, 0b11111110, 0b00000001, 7, 1)]

    class VMMGlbSigChks:
        sig_name = "VMMGlbSigChks"
        sig_start_bit = 455
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 455
        byte = 56
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VmcBrkTqReqChks:
        sig_name = "VmcBrkTqReqChks"
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

    class StfnLvlReq:
        sig_name = "StfnLvlReq"
        sig_start_bit = 327
        update_id_bit = 324
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'StfnLvl_Level1': 0, 'StfnLvl_Level2': 1, 'StfnLvl_Level3': 2, 'StfnLvl_Level4': 3, 'StfnLvl_Level5': 4, 'StfnLvl_Level6': 5, 'StfnLvl_Level7': 6, 'StfnLvl_Level8': 7}
        compute_method = None
        length = 3
        startbit = 327
        byte = 40
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class EpbCoornSecReserved7:
        sig_name = "EpbCoornSecReserved7"
        sig_start_bit = 154
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CoornSt_Inactive': 0, 'CoornSt_Active': 1}
        compute_method = None
        length = 1
        startbit = 154
        byte = 19
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VMMGlbSigUsgModSts:
        sig_name = "VMMGlbSigUsgModSts"
        sig_start_bit = 495
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
        startbit = 495
        byte = 61
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class ADSMstPinAgReqChks:
        sig_name = "ADSMstPinAgReqChks"
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

    class ObjlnfoObjConfidenceLvl:
        sig_name = "ObjlnfoObjConfidenceLvl"
        sig_start_bit = 183
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
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

    class ModReqOfDampr:
        sig_name = "ModReqOfDampr"
        sig_start_bit = 132
        update_id_bit = 129
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DamprLvl_level1': 0, 'DamprLvl_level2': 1, 'DamprLvl_level3': 2, 'DamprLvl_Reserved1': 3, 'DamprLvl_Reserved2': 4, 'DamprLvl_Reserved3': 5, 'DamprLvl_Reserved4': 6, 'DamprLvl_Reserved5': 7}
        compute_method = None
        length = 3
        startbit = 132
        byte = 16
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class EPBHpsReqSecHpsReq:
        sig_name = "EPBHpsReqSecHpsReq"
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
        sig_value_table = {'HpsReq_NoReq': 0, 'HpsReq_Normal': 1, 'HpsReq_Max': 2, 'HpsReq_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 175
        byte = 21
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class VmcPinionAgReqChks:
        sig_name = "VmcPinionAgReqChks"
        sig_start_bit = 431
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 431
        byte = 53
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ObjlnfoObjHei:
        sig_name = "ObjlnfoObjHei"
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

    class ADSMstAgCtrlTqLimLowrLim:
        sig_name = "ADSMstAgCtrlTqLimLowrLim"
        sig_start_bit = 43
        update_id_bit = None
        sig_length = 9
        sig_value_factor = 0.125
        sig_value_offset = -30.0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 43
        bmuws_info = [(5, 0b00001111, 0b11110000, 4, 0), (6, 0b11111000, 0b00000111, 5, 3)]

    class ObjlnfoObjDst1:
        sig_name = "ObjlnfoObjDst1"
        sig_start_bit = 191
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
        startbit = 191
        bmuws_info = [(23, 0b11111111, 0b00000000, 8, 0), (24, 0b11000000, 0b00111111, 2, 6)]

    class EPBHpsReqSec_UB:
        sig_name = "EPBHpsReqSec_UB"
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

    class VmcBrkTqReq_UB:
        sig_name = "VmcBrkTqReq_UB"
        sig_start_bit = 422
        update_id_bit = 422
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 422
        byte = 52
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class EpbApplyReqByAEBR:
        sig_name = "EpbApplyReqByAEBR"
        sig_start_bit = 91
        update_id_bit = 90
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
        startbit = 91
        byte = 11
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class ADSMstAgCtrlTqLimChks:
        sig_name = "ADSMstAgCtrlTqLimChks"
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

    class EPBHpsReqSecCntr:
        sig_name = "EPBHpsReqSecCntr"
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

    class VmcPinionAgReqCntr:
        sig_name = "VmcPinionAgReqCntr"
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

    class GearLvrIndcnRealCntr:
        sig_name = "GearLvrIndcnRealCntr"
        sig_start_bit = 507
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
        startbit = 507
        byte = 63
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class EpbCoornSecReserved5:
        sig_name = "EpbCoornSecReserved5"
        sig_start_bit = 156
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CoornSt_Inactive': 0, 'CoornSt_Active': 1}
        compute_method = None
        length = 1
        startbit = 156
        byte = 19
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class AccrPedlValCntr:
        sig_name = "AccrPedlValCntr"
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

    class VMMGlbSigCarModSts:
        sig_name = "VMMGlbSigCarModSts"
        sig_start_bit = 463
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
        startbit = 463
        byte = 57
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class VmcBrkTqReqReq:
        sig_name = "VmcBrkTqReqReq"
        sig_start_bit = 404
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
        startbit = 404
        bmuws_info = [(50, 0b00011111, 0b11100000, 5, 0), (51, 0b11111111, 0b00000000, 8, 0), (52, 0b10000000, 0b01111111, 1, 7)]

    class VmcAgCtrlTqLimCntr:
        sig_name = "VmcAgCtrlTqLimCntr"
        sig_start_bit = 351
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
        startbit = 351
        byte = 43
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class VMMGlbSig_UB:
        sig_name = "VMMGlbSig_UB"
        sig_start_bit = 490
        update_id_bit = 490
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 490
        byte = 61
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class GearLvrIndcnRealGearLvrIndcn:
        sig_name = "GearLvrIndcnRealGearLvrIndcn"
        sig_start_bit = 511
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
        startbit = 511
        byte = 63
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class AccrPedlValPedlFild:
        sig_name = "AccrPedlValPedlFild"
        sig_start_bit = 15
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
        startbit = 15
        bmuws_info = [(1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111110, 0b00000001, 7, 1)]

    class ObjlnfoObjSide:
        sig_name = "ObjlnfoObjSide"
        sig_start_bit = 223
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
        startbit = 223
        byte = 27
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class ADSMstPinAgReq_UB:
        sig_name = "ADSMstPinAgReq_UB"
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

    class ObjlnfoObjTypMai:
        sig_name = "ObjlnfoObjTypMai"
        sig_start_bit = 203
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ObjTypMai_None': 0, 'ObjTypMai_Bump': 1, 'ObjTypMai_Manhole': 2, 'ObjTypMai_Pothole': 3, 'ObjTypMai_Step': 4, 'ObjTypMai_Reserved1': 5, 'ObjTypMai_Reserved2': 6, 'ObjTypMai_Reserved3': 7, 'ObjTypMai_Reserved4': 8, 'ObjTypMai_Reserved5': 9, 'ObjTypMai_Reserved6': 10, 'ObjTypMai_Reserved7': 11, 'ObjTypMai_Reserved8': 12, 'ObjTypMai_Reserved9': 13, 'ObjTypMai_Reserved10': 14, 'ObjTypMai_Reserved11': 15}
        compute_method = None
        length = 4
        startbit = 203
        byte = 25
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class GearLvrIndcnRealChks:
        sig_name = "GearLvrIndcnRealChks"
        sig_start_bit = 503
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 503
        byte = 62
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ADSMstAgCtrlTqLimCntr:
        sig_name = "ADSMstAgCtrlTqLimCntr"
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

    class EpbCoornSecCommunicationAvl:
        sig_name = "EpbCoornSecCommunicationAvl"
        sig_start_bit = 151
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CoornSt_Inactive': 0, 'CoornSt_Active': 1}
        compute_method = None
        length = 1
        startbit = 151
        byte = 18
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class PtSysWhlTqFrntActPtWhlTqFrntRiAct:
        sig_name = "PtSysWhlTqFrntActPtWhlTqFrntRiAct"
        sig_start_bit = 311
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
        startbit = 311
        bmuws_info = [(38, 0b11111111, 0b00000000, 8, 0), (39, 0b11111110, 0b00000001, 7, 1)]

    class PtSysWhlTqFrntActPtWhlTqFrntLeAct:
        sig_name = "PtSysWhlTqFrntActPtWhlTqFrntLeAct"
        sig_start_bit = 295
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
        startbit = 295
        bmuws_info = [(36, 0b11111111, 0b00000000, 8, 0), (37, 0b11111110, 0b00000001, 7, 1)]

    class EpbCoornSecReserved3:
        sig_name = "EpbCoornSecReserved3"
        sig_start_bit = 158
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CoornSt_Inactive': 0, 'CoornSt_Active': 1}
        compute_method = None
        length = 1
        startbit = 158
        byte = 19
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class LvlCtrlEna:
        sig_name = "LvlCtrlEna"
        sig_start_bit = 134
        update_id_bit = 133
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
        startbit = 134
        byte = 16
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VmcBrkTqReqGrdtPos:
        sig_name = "VmcBrkTqReqGrdtPos"
        sig_start_bit = 399
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 300
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2048
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 399
        bmuws_info = [(49, 0b11111111, 0b00000000, 8, 0), (50, 0b11100000, 0b00011111, 3, 5)]

    class GearLvrIndcnReal_UB:
        sig_name = "GearLvrIndcnReal_UB"
        sig_start_bit = 508
        update_id_bit = 508
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 508
        byte = 63
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class EpbCoornSecCntr:
        sig_name = "EpbCoornSecCntr"
        sig_start_bit = 147
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
        startbit = 147
        byte = 18
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class ADSMstPinAgReqReq:
        sig_name = "ADSMstPinAgReqReq"
        sig_start_bit = 75
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 0.0009765625
        sig_value_offset = -14.5
        sig_value_min = 0
        sig_value_max = 29696
        sig_byteorder = "Motorola"
        sig_value_init = 14848
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 75
        bmuws_info = [(9, 0b00001111, 0b11110000, 4, 0), (10, 0b11111111, 0b00000000, 8, 0), (11, 0b11100000, 0b00011111, 3, 5)]

    class BrkSysStSecRdntCntr:
        sig_name = "BrkSysStSecRdntCntr"
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

    class EPBHpsTarPSec:
        sig_name = "EPBHpsTarPSec"
        sig_start_bit = 127
        update_id_bit = 135
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
        startbit = 127
        byte = 15
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VMMGlbSigInactvSubSts1:
        sig_name = "VMMGlbSigInactvSubSts1"
        sig_start_bit = 487
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
        startbit = 487
        byte = 60
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class EpbCoornSecReserved1:
        sig_name = "EpbCoornSecReserved1"
        sig_start_bit = 148
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CoornSt_Inactive': 0, 'CoornSt_Active': 1}
        compute_method = None
        length = 1
        startbit = 148
        byte = 18
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VmcBrkTqReqCntr:
        sig_name = "VmcBrkTqReqCntr"
        sig_start_bit = 383
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
        startbit = 383
        byte = 47
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class EpbCoornSecChks:
        sig_name = "EpbCoornSecChks"
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

    class PrpsnTqFrntAxleReq:
        sig_name = "PrpsnTqFrntAxleReq"
        sig_start_bit = 220
        update_id_bit = 237
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
        startbit = 220
        bmuws_info = [(27, 0b00011111, 0b11100000, 5, 0), (28, 0b11111111, 0b00000000, 8, 0), (29, 0b11000000, 0b00111111, 2, 6)]

    class ADSMstPinAgReqCntr:
        sig_name = "ADSMstPinAgReqCntr"
        sig_start_bit = 79
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
        startbit = 79
        byte = 9
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4


class SUMChassis1CANFDFr04:
    msg_name = "SUMChassis1CANFDFr04"
    msg_id = 17
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "SUM"
    rx_nodes = ['CCUMCUAD', 'ETC']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class PreviewDamprCtrlSts:
        sig_name = "PreviewDamprCtrlSts"
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
        sig_value_table = {'PreviewDamprSts_NA': 0, 'PreviewDamprSts_Active': 1, 'PreviewDamprSts_Idle': 2, 'PreviewDamprSts_Error': 3, 'PreviewDamprSts_Off': 4, 'PreviewDamprSts_Reserved1': 5, 'PreviewDamprSts_Reserved2': 6, 'PreviewDamprSts_Reserved3': 7}
        compute_method = None
        length = 3
        startbit = 7
        byte = 0
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5


class SUMChassis1CANFDFr02:
    msg_name = "SUMChassis1CANFDFr02"
    msg_id = 290
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.03
    msg_length = 12
    tx_node = "SUM"
    rx_nodes = ['CCUMCUAD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class FrntRiLvlAdjm:
        sig_name = "FrntRiLvlAdjm"
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
        sig_value_table = {'LevelAdjust_NoAdjustment': 0, 'LevelAdjust_Adjustment': 1}
        compute_method = None
        length = 1
        startbit = 9
        byte = 1
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class ExtraLoPosn:
        sig_name = "ExtraLoPosn"
        sig_start_bit = 2
        update_id_bit = 1
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExtremeLow_VehicleHeightNotextremeLow': 0, 'ExtremeLow_VehicleHeightextremeLow': 1}
        compute_method = None
        length = 1
        startbit = 2
        byte = 0
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class LvlAdjRestriction:
        sig_name = "LvlAdjRestriction"
        sig_start_bit = 23
        update_id_bit = 20
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LevelRestriction_InitOrNoRestriction': 0, 'LevelRestriction_VoltageTooLowOrHigh': 2, 'LevelRestriction_ActuatorTempRestriction': 3, 'LevelRestriction_LevelRestrictionByDoorState': 4, 'LevelRestriction_LevelContolManuallyDisable': 5, 'LevelRestriction_Torsion': 6, 'LevelRestriction_Reserved1': 7}
        compute_method = None
        length = 3
        startbit = 23
        byte = 2
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class SCFailrSts:
        sig_name = "SCFailrSts"
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
        sig_value_table = {'StiffnessFailrSts_NoFault': 0, 'StiffnessFailrSts_Fault': 1}
        compute_method = None
        length = 1
        startbit = 34
        byte = 4
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class FrntLeLvlAdjm:
        sig_name = "FrntLeLvlAdjm"
        sig_start_bit = 0
        update_id_bit = 15
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LevelAdjust_NoAdjustment': 0, 'LevelAdjust_Adjustment': 1}
        compute_method = None
        length = 1
        startbit = 0
        byte = 0
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ReAxleLvl:
        sig_name = "ReAxleLvl"
        sig_start_bit = 31
        update_id_bit = 27
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
        startbit = 31
        byte = 3
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DamprFailrSts3:
        sig_name = "DamprFailrSts3"
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
        sig_value_table = {'DamprSts3_NoError': 0, 'DamprSts3_MinorError': 1, 'DamprSts3_MajorError': 2, 'DamprSts3_CriticalErrpr': 3}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class FrntAxleLvl:
        sig_name = "FrntAxleLvl"
        sig_start_bit = 14
        update_id_bit = 10
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
        startbit = 14
        byte = 1
        mask = 0b01111000
        unmask = 0b10000111
        shift = 3

    class ReLeStfnSts:
        sig_name = "ReLeStfnSts"
        sig_start_bit = 24
        update_id_bit = 39
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
        startbit = 24
        byte = 3
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ReRiStfnSts:
        sig_name = "ReRiStfnSts"
        sig_start_bit = 36
        update_id_bit = 35
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
        startbit = 36
        byte = 4
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class ReRiLvlAdjm:
        sig_name = "ReRiLvlAdjm"
        sig_start_bit = 38
        update_id_bit = 37
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LevelAdjust_NoAdjustment': 0, 'LevelAdjust_Adjustment': 1}
        compute_method = None
        length = 1
        startbit = 38
        byte = 4
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class ReLeLvlAdjm:
        sig_name = "ReLeLvlAdjm"
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
        sig_value_table = {'LevelAdjust_NoAdjustment': 0, 'LevelAdjust_Adjustment': 1}
        compute_method = None
        length = 1
        startbit = 26
        byte = 3
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class LvlAdjSts:
        sig_name = "LvlAdjSts"
        sig_start_bit = 19
        update_id_bit = 16
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AdjustStatus_StaticPosition': 0, 'AdjustStatus_RaisingToNewTargetLevel': 1, 'AdjustStatus_LoweringToNewTargetLevel': 2, 'AdjustStatus_FrozenPendingOfTargetLevelChange': 3, 'AdjustStatus_RaisingForLevelAdjustment': 4, 'AdjustStatus_LoweringForLevelAdjustment': 5, 'AdjustStatus_FrozenPendingForLevelAdjsutment': 6, 'AdjustStatus_Reserved': 7}
        compute_method = None
        length = 3
        startbit = 19
        byte = 2
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class ExtraHiPosn:
        sig_name = "ExtraHiPosn"
        sig_start_bit = 4
        update_id_bit = 3
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExtremeHigh_VehicleHeightNotExtremeHigh': 0, 'ExtremeHigh_VehicleHeightExtremeHigh': 1}
        compute_method = None
        length = 1
        startbit = 4
        byte = 0
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4


class PSCM1Chassis1CANFDFr07:
    msg_name = "PSCM1Chassis1CANFDFr07"
    msg_id = 644
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "PSCM1"
    rx_nodes = ['CCUMCUAD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class URawPSCM1:
        sig_name = "URawPSCM1"
        sig_start_bit = 9
        update_id_bit = 16
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
        startbit = 9
        bmuws_info = [(1, 0b00000011, 0b11111100, 2, 0), (2, 0b11111110, 0b00000001, 7, 1)]

    class IRawPSCM1:
        sig_name = "IRawPSCM1"
        sig_start_bit = 7
        update_id_bit = 10
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
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111000, 0b00000111, 5, 3)]


class SUMChassis1CANFDFr01:
    msg_name = "SUMChassis1CANFDFr01"
    msg_id = 52
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 24
    tx_node = "SUM"
    rx_nodes = ['CCUMCUAD', 'ETC']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class CurrentLvl:
        sig_name = "CurrentLvl"
        sig_start_bit = 7
        update_id_bit = 31
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

    class ReRiLvl:
        sig_name = "ReRiLvl"
        sig_start_bit = 23
        update_id_bit = 27
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
        startbit = 23
        byte = 2
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class FrntLeStfnSts:
        sig_name = "FrntLeStfnSts"
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

    class ReLeLvl:
        sig_name = "ReLeLvl"
        sig_start_bit = 11
        update_id_bit = 28
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
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class SuspPosnHeiFrntLe:
        sig_name = "SuspPosnHeiFrntLe"
        sig_start_bit = 47
        update_id_bit = 48
        sig_length = 15
        sig_value_factor = 6.2e-05
        sig_value_offset = 0
        sig_value_min = -16129
        sig_value_max = 16130
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111110, 0b00000001, 7, 1)]

    class SuspPosnHeiFrntRi:
        sig_name = "SuspPosnHeiFrntRi"
        sig_start_bit = 63
        update_id_bit = 64
        sig_length = 15
        sig_value_factor = 6.2e-05
        sig_value_offset = 0
        sig_value_min = -16129
        sig_value_max = 16130
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 63
        bmuws_info = [(7, 0b11111111, 0b00000000, 8, 0), (8, 0b11111110, 0b00000001, 7, 1)]

    class TarLvl:
        sig_name = "TarLvl"
        sig_start_bit = 19
        update_id_bit = 26
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
        startbit = 19
        byte = 2
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class FrntLeLvl:
        sig_name = "FrntLeLvl"
        sig_start_bit = 3
        update_id_bit = 30
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
        startbit = 3
        byte = 0
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class SuspPosnHeiReRi:
        sig_name = "SuspPosnHeiReRi"
        sig_start_bit = 95
        update_id_bit = 96
        sig_length = 15
        sig_value_factor = 6.2e-05
        sig_value_offset = 0
        sig_value_min = -16129
        sig_value_max = 16130
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 95
        bmuws_info = [(11, 0b11111111, 0b00000000, 8, 0), (12, 0b11111110, 0b00000001, 7, 1)]

    class FrntRiLvl:
        sig_name = "FrntRiLvl"
        sig_start_bit = 15
        update_id_bit = 29
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

    class SuspPosnHeiReLe:
        sig_name = "SuspPosnHeiReLe"
        sig_start_bit = 79
        update_id_bit = 80
        sig_length = 15
        sig_value_factor = 6.2e-05
        sig_value_offset = 0
        sig_value_min = -16129
        sig_value_max = 16130
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 79
        bmuws_info = [(9, 0b11111111, 0b00000000, 8, 0), (10, 0b11111110, 0b00000001, 7, 1)]

    class FrntRiStfnSts:
        sig_name = "FrntRiStfnSts"
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


class SUMToCCUMCUADChassis1CANFDDiagRespFrame:
    msg_name = "SUMToCCUMCUADChassis1CANFDDiagRespFrame"
    msg_id = 1556
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "SUM"
    rx_nodes = ['CCUMCUAD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class BCU1ToCCUMCUADChassis1CANFDDiagRespFrame:
    msg_name = "BCU1ToCCUMCUADChassis1CANFDDiagRespFrame"
    msg_id = 1538
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "BCU1"
    rx_nodes = ['CCUMCUAD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class SRSChassis1CANFDFr01:
    msg_name = "SRSChassis1CANFDFr01"
    msg_id = 51
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 16
    tx_node = "SRS"
    rx_nodes = ['CCUMCUAD', 'BCU1']
    sig_group_dict = {'PostImpctBrkgCfmd': ['PostImpctBrkgCfmdChks', 'PostImpctBrkgCfmdCntr', 'PostImpctBrkgCfmdCrashFrnt', 'PostImpctBrkgCfmdCrashLargeAnimal', 'PostImpctBrkgCfmdCrashOffroadA', 'PostImpctBrkgCfmdCrashOffroadD', 'PostImpctBrkgCfmdCrashOffroadRT', 'PostImpctBrkgCfmdCrashOffroadRTsevere', 'PostImpctBrkgCfmdCrashOz', 'PostImpctBrkgCfmdCrashPed', 'PostImpctBrkgCfmdCrashRollovr', 'PostImpctBrkgCfmdCrashSideLe', 'PostImpctBrkgCfmdCrashSideRi', 'PostImpctBrkgCfmdPostImpctBrkgCfmd'], 'PostImpctBrkgSuspc': ['PostImpctBrkgSuspcChks', 'PostImpctBrkgSuspcCntr', 'PostImpctBrkgSuspcPostImpctBrkgSuspc']}
    sig_group_dataid_dict = {}

    class PostImpctBrkgCfmdChks:
        sig_name = "PostImpctBrkgCfmdChks"
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

    class BeltCrashStsAtPass:
        sig_name = "BeltCrashStsAtPass"
        sig_start_bit = 5
        update_id_bit = 2
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BeltCrashSts_Invalid': 0, 'BeltCrashSts_NotActvn': 1, 'BeltCrashSts_Actvn': 2}
        compute_method = None
        length = 2
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class PostImpctBrkgCfmdCrashLargeAnimal:
        sig_name = "PostImpctBrkgCfmdCrashLargeAnimal"
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
        sig_value_table = {'OnOffCrit1_NotVld1': 0, 'OnOffCrit1_Off': 1, 'OnOffCrit1_On': 2, 'OnOffCrit1_NotVld2': 3}
        compute_method = None
        length = 2
        startbit = 29
        byte = 3
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class BeltCrashStsAtDrvr:
        sig_name = "BeltCrashStsAtDrvr"
        sig_start_bit = 7
        update_id_bit = 3
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BeltCrashSts_Invalid': 0, 'BeltCrashSts_NotActvn': 1, 'BeltCrashSts_Actvn': 2}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class PostImpctBrkgCfmdCrashOz:
        sig_name = "PostImpctBrkgCfmdCrashOz"
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
        sig_value_table = {'OnOffCrit1_NotVld1': 0, 'OnOffCrit1_Off': 1, 'OnOffCrit1_On': 2, 'OnOffCrit1_NotVld2': 3}
        compute_method = None
        length = 2
        startbit = 35
        byte = 4
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class PostImpctBrkgCfmdCrashFrnt:
        sig_name = "PostImpctBrkgCfmdCrashFrnt"
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
        sig_value_table = {'OnOffCrit1_NotVld1': 0, 'OnOffCrit1_Off': 1, 'OnOffCrit1_On': 2, 'OnOffCrit1_NotVld2': 3}
        compute_method = None
        length = 2
        startbit = 31
        byte = 3
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class PostImpctBrkgCfmdCrashSideLe:
        sig_name = "PostImpctBrkgCfmdCrashSideLe"
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
        sig_value_table = {'OnOffCrit1_NotVld1': 0, 'OnOffCrit1_Off': 1, 'OnOffCrit1_On': 2, 'OnOffCrit1_NotVld2': 3}
        compute_method = None
        length = 2
        startbit = 45
        byte = 5
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class PostImpctBrkgSuspcPostImpctBrkgSuspc:
        sig_name = "PostImpctBrkgSuspcPostImpctBrkgSuspc"
        sig_start_bit = 63
        update_id_bit = None
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
        startbit = 63
        byte = 7
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class PostImpctBrkgCfmd_UB:
        sig_name = "PostImpctBrkgCfmd_UB"
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

    class PostImpctBrkgCfmdCrashOffroadRT:
        sig_name = "PostImpctBrkgCfmdCrashOffroadRT"
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
        sig_value_table = {'OnOffCrit1_NotVld1': 0, 'OnOffCrit1_Off': 1, 'OnOffCrit1_On': 2, 'OnOffCrit1_NotVld2': 3}
        compute_method = None
        length = 2
        startbit = 39
        byte = 4
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class PostImpctBrkgSuspcChks:
        sig_name = "PostImpctBrkgSuspcChks"
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

    class PostImpctBrkgSuspc_UB:
        sig_name = "PostImpctBrkgSuspc_UB"
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

    class PostImpctBrkgCfmdPostImpctBrkgCfmd:
        sig_name = "PostImpctBrkgCfmdPostImpctBrkgCfmd"
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
        sig_value_table = {'OnOffCrit1_NotVld1': 0, 'OnOffCrit1_Off': 1, 'OnOffCrit1_On': 2, 'OnOffCrit1_NotVld2': 3}
        compute_method = None
        length = 2
        startbit = 41
        byte = 5
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class PostImpctBrkgCfmdCrashRollovr:
        sig_name = "PostImpctBrkgCfmdCrashRollovr"
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
        sig_value_table = {'OnOffCrit1_NotVld1': 0, 'OnOffCrit1_Off': 1, 'OnOffCrit1_On': 2, 'OnOffCrit1_NotVld2': 3}
        compute_method = None
        length = 2
        startbit = 47
        byte = 5
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class PostImpctBrkgCfmdCrashOffroadRTsevere:
        sig_name = "PostImpctBrkgCfmdCrashOffroadRTsevere"
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
        sig_value_table = {'OnOffCrit1_NotVld1': 0, 'OnOffCrit1_Off': 1, 'OnOffCrit1_On': 2, 'OnOffCrit1_NotVld2': 3}
        compute_method = None
        length = 2
        startbit = 37
        byte = 4
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class PostImpctBrkgCfmdCrashSideRi:
        sig_name = "PostImpctBrkgCfmdCrashSideRi"
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
        sig_value_table = {'OnOffCrit1_NotVld1': 0, 'OnOffCrit1_Off': 1, 'OnOffCrit1_On': 2, 'OnOffCrit1_NotVld2': 3}
        compute_method = None
        length = 2
        startbit = 43
        byte = 5
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class PostImpctBrkgCfmdCntr:
        sig_name = "PostImpctBrkgCfmdCntr"
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

    class PostImpctBrkgCfmdCrashPed:
        sig_name = "PostImpctBrkgCfmdCrashPed"
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
        sig_value_table = {'OnOffCrit1_NotVld1': 0, 'OnOffCrit1_Off': 1, 'OnOffCrit1_On': 2, 'OnOffCrit1_NotVld2': 3}
        compute_method = None
        length = 2
        startbit = 33
        byte = 4
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class PostImpctBrkgSuspcCntr:
        sig_name = "PostImpctBrkgSuspcCntr"
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

    class PostImpctBrkgCfmdCrashOffroadD:
        sig_name = "PostImpctBrkgCfmdCrashOffroadD"
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
        sig_value_table = {'OnOffCrit1_NotVld1': 0, 'OnOffCrit1_Off': 1, 'OnOffCrit1_On': 2, 'OnOffCrit1_NotVld2': 3}
        compute_method = None
        length = 2
        startbit = 25
        byte = 3
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class PostImpctBrkgCfmdCrashOffroadA:
        sig_name = "PostImpctBrkgCfmdCrashOffroadA"
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
        sig_value_table = {'OnOffCrit1_NotVld1': 0, 'OnOffCrit1_Off': 1, 'OnOffCrit1_On': 2, 'OnOffCrit1_NotVld2': 3}
        compute_method = None
        length = 2
        startbit = 27
        byte = 3
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2


class PSCM1Chassis1CANFDFr01:
    msg_name = "PSCM1Chassis1CANFDFr01"
    msg_id = 50
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 25
    tx_node = "PSCM1"
    rx_nodes = ['ETC', 'SUM', 'CCUMCUAD', 'BCU1']
    sig_group_dict = {'SteerInfoRef': ['SteerInfoRefChks', 'SteerInfoRefCntr', 'SteerInfoRefSteerPinionAgSpdVal', 'SteerInfoRefSteerPinionAgSpdValQf', 'SteerInfoRefSteerPinionAgVal', 'SteerInfoRefSteerPinionAgValQf', 'SteerInfoRefSteerTorqueValQf', 'SteerInfoRefSteerWhlTqVal'], 'SteerWhlSnsr': ['SteerWhlSnsrAg', 'SteerWhlSnsrAgSpd', 'SteerWhlSnsrChks', 'SteerWhlSnsrCntr', 'SteerWhlSnsrQf']}
    sig_group_dataid_dict = {'SteerInfoRef': 1037, 'SteerWhlSnsr': 1056}

    class SteerInfoRefSteerPinionAgSpdVal:
        sig_name = "SteerInfoRefSteerPinionAgSpdVal"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 14
        sig_value_factor = 0.0078125
        sig_value_offset = 0
        sig_value_min = -8192
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 14
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111100, 0b00000011, 6, 2)]

    class SteerInfoRefSteerPinionAgValQf:
        sig_name = "SteerInfoRefSteerPinionAgValQf"
        sig_start_bit = 13
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 2
        startbit = 13
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class SteerInfoRefCntr:
        sig_name = "SteerInfoRefCntr"
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

    class SteerAssistAvlSts:
        sig_name = "SteerAssistAvlSts"
        sig_start_bit = 135
        update_id_bit = 134
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
        startbit = 135
        byte = 16
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class SteerInfoRefSteerTorqueValQf:
        sig_name = "SteerInfoRefSteerTorqueValQf"
        sig_start_bit = 60
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 2
        startbit = 60
        byte = 7
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class SteerWhlSnsrAgSpd:
        sig_name = "SteerWhlSnsrAgSpd"
        sig_start_bit = 119
        update_id_bit = None
        sig_length = 14
        sig_value_factor = 0.0078125
        sig_value_offset = 0
        sig_value_min = -8192
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 14
        startbit = 119
        bmuws_info = [(14, 0b11111111, 0b00000000, 8, 0), (15, 0b11111100, 0b00000011, 6, 2)]

    class SteerInfoRefSteerPinionAgVal:
        sig_name = "SteerInfoRefSteerPinionAgVal"
        sig_start_bit = 25
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 0.000976563
        sig_value_offset = 0
        sig_value_min = -16384
        sig_value_max = 16383
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 25
        bmuws_info = [(3, 0b00000011, 0b11111100, 2, 0), (4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111000, 0b00000111, 5, 3)]

    class SteerInfoRefChks:
        sig_name = "SteerInfoRefChks"
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

    class SteerInfoRef_UB:
        sig_name = "SteerInfoRef_UB"
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

    class SteerWhlSnsrQf:
        sig_name = "SteerWhlSnsrQf"
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

    class SteerWhlSnsrAg:
        sig_name = "SteerWhlSnsrAg"
        sig_start_bit = 103
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 0.000976563
        sig_value_offset = 0
        sig_value_min = -16384
        sig_value_max = 16383
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 103
        bmuws_info = [(12, 0b11111111, 0b00000000, 8, 0), (13, 0b11111110, 0b00000001, 7, 1)]

    class SteerInfoRefSteerPinionAgSpdValQf:
        sig_name = "SteerInfoRefSteerPinionAgSpdValQf"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 2
        startbit = 15
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class SteerWhlSnsrChks:
        sig_name = "SteerWhlSnsrChks"
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

    class SteerWhlSnsr_UB:
        sig_name = "SteerWhlSnsr_UB"
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

    class SteerRackFVal:
        sig_name = "SteerRackFVal"
        sig_start_bit = 71
        update_id_bit = 56
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
        startbit = 71
        bmuws_info = [(8, 0b11111111, 0b00000000, 8, 0), (9, 0b11111111, 0b00000000, 8, 0)]

    class SteerWhlSnsrCntr:
        sig_name = "SteerWhlSnsrCntr"
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

    class SteerInfoRefSteerWhlTqVal:
        sig_name = "SteerInfoRefSteerWhlTqVal"
        sig_start_bit = 42
        update_id_bit = None
        sig_length = 14
        sig_value_factor = 0.00390625
        sig_value_offset = 0
        sig_value_min = -8192
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 14
        startbit = 42
        bmuws_info = [(5, 0b00000111, 0b11111000, 3, 0), (6, 0b11111111, 0b00000000, 8, 0), (7, 0b11100000, 0b00011111, 3, 5)]


class CCUMCUADChassis1CANFDFr11:
    msg_name = "CCUMCUADChassis1CANFDFr11"
    msg_id = 321
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.04
    msg_length = 8
    tx_node = "CCUMCUAD"
    rx_nodes = ['BCU1']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class FLLtchPosn:
        sig_name = "FLLtchPosn"
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
        sig_value_table = {'LatPosn_Unknow': 0, 'LatPosn_FullOpen': 1, 'LatPosn_SecLtchPosn': 2, 'LatPosn_FullClose': 3}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class BCU1Chassis1CANFDNmFr:
    msg_name = "BCU1Chassis1CANFDNmFr"
    msg_id = 1283
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BCU1"
    rx_nodes = ['SUM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class BCU1Chassis1CANFDFr02:
    msg_name = "BCU1Chassis1CANFDFr02"
    msg_id = 160
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 64
    tx_node = "BCU1"
    rx_nodes = ['ETC', 'PSCM1', 'SUM', 'CCUMCUAD', 'SRS']
    sig_group_dict = {'WhlMovgDirFrnt': ['WhlMovgDirFrntChks', 'WhlMovgDirFrntCntr', 'WhlMovgDirFrntDirLe', 'WhlMovgDirFrntDirRi'], 'BrkPedStkPerc': ['BrkPedStkPercChks', 'BrkPedStkPercCntr', 'BrkPedStkPercPerc'], 'BrkLiReq': ['BrkLiReqBrkLiReq', 'BrkLiReqChks', 'BrkLiReqCntr'], 'VehMovgDir': ['VehMovgDirChks', 'VehMovgDirCntr', 'VehMovgDirVehMovgDir'], 'WhlPlsCntr': ['WhlPlsCntrChks', 'WhlPlsCntrCntr', 'WhlPlsCntrFL', 'WhlPlsCntrFR', 'WhlPlsCntrRL', 'WhlPlsCntrRR'], 'VehSpdSafe': ['VehSpdSafeChks', 'VehSpdSafeCntr', 'VehSpdSafeQf', 'VehSpdSafeSpd'], 'VehSpd': ['VehSpdChks', 'VehSpdCntr', 'VehSpdQf', 'VehSpdSpd'], 'EpbTotSts': ['EpbTotStsChks', 'EpbTotStsCntr', 'EpbTotStsEpbSt'], 'WhlMovgDirRe': ['WhlMovgDirReChks', 'WhlMovgDirReCntr', 'WhlMovgDirReDirLe', 'WhlMovgDirReDirRi'], 'BrkPedlInfo': ['BrkPedlInfoChks', 'BrkPedlInfoCntr', 'BrkPedlInfoNotPsd', 'BrkPedlInfoPsd', 'BrkPedlInfoQf']}
    sig_group_dataid_dict = {'VehSpdSafe': 1044, 'VehSpd': 1043, 'EpbTotSts': 1050, 'BrkPedlInfo': 1049}

    class BrkPBoost:
        sig_name = "BrkPBoost"
        sig_start_bit = 39
        update_id_bit = 82
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
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class WhlMovgDirReChks:
        sig_name = "WhlMovgDirReChks"
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

    class WhlEdgeRL:
        sig_name = "WhlEdgeRL"
        sig_start_bit = 71
        update_id_bit = 84
        sig_length = 8
        sig_value_factor = None
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

    class VehMovgDirCntr:
        sig_name = "VehMovgDirCntr"
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

    class WhlPlsCntrRR:
        sig_name = "WhlPlsCntrRR"
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

    class WhlMovgDirFrnt_UB:
        sig_name = "WhlMovgDirFrnt_UB"
        sig_start_bit = 248
        update_id_bit = 248
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 248
        byte = 31
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class WhlMovgDirFrntChks:
        sig_name = "WhlMovgDirFrntChks"
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

    class WhlMovgDirReDirRi:
        sig_name = "WhlMovgDirReDirRi"
        sig_start_bit = 285
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
        startbit = 285
        byte = 35
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class AcbModePrim:
        sig_name = "AcbModePrim"
        sig_start_bit = 7
        update_id_bit = 4
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AcbMod_Ad': 0, 'AcbMod_Epedl': 1, 'AcbMod_CoastComp': 2, 'AcbMod_ExternalHold': 3, 'AcbMod_Reserved': 4}
        compute_method = None
        length = 3
        startbit = 7
        byte = 0
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class BrkLiReqChks:
        sig_name = "BrkLiReqChks"
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

    class VehMovgDirVehMovgDir:
        sig_name = "VehMovgDirVehMovgDir"
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
        sig_value_table = {'VehMovgDir_Unknown': 0, 'VehMovgDir_Standstill1': 1, 'VehMovgDir_Standstill2': 2, 'VehMovgDir_Standstill3': 3, 'VehMovgDir_Forward1': 4, 'VehMovgDir_Forward2': 5, 'VehMovgDir_Backward1': 6, 'VehMovgDir_Backward2': 7}
        compute_method = None
        length = 3
        startbit = 191
        byte = 23
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class WhlEdgeRR:
        sig_name = "WhlEdgeRR"
        sig_start_bit = 79
        update_id_bit = 83
        sig_length = 8
        sig_value_factor = None
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

    class WhlEdgeFR:
        sig_name = "WhlEdgeFR"
        sig_start_bit = 63
        update_id_bit = 85
        sig_length = 8
        sig_value_factor = None
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

    class WhlPlsCntrCntr:
        sig_name = "WhlPlsCntrCntr"
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

    class WhlPlsCntrRL:
        sig_name = "WhlPlsCntrRL"
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

    class VehMovgDirChks:
        sig_name = "VehMovgDirChks"
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

    class BrkPedStkPerc_UB:
        sig_name = "BrkPedStkPerc_UB"
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

    class RcwBrkActrAtv:
        sig_name = "RcwBrkActrAtv"
        sig_start_bit = 11
        update_id_bit = 9
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
        startbit = 11
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class WhlMovgDirFrntDirLe:
        sig_name = "WhlMovgDirFrntDirLe"
        sig_start_bit = 271
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
        startbit = 271
        byte = 33
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class WhlPlsCntrFR:
        sig_name = "WhlPlsCntrFR"
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

    class VehSpdSpd:
        sig_name = "VehSpdSpd"
        sig_start_bit = 215
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
        startbit = 215
        bmuws_info = [(26, 0b11111111, 0b00000000, 8, 0), (27, 0b11111110, 0b00000001, 7, 1)]

    class VehSpdSafeCntr:
        sig_name = "VehSpdSafeCntr"
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

    class WhlPlsCntrChks:
        sig_name = "WhlPlsCntrChks"
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

    class BrkLiReq_UB:
        sig_name = "BrkLiReq_UB"
        sig_start_bit = 28
        update_id_bit = 28
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 28
        byte = 3
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VehSpdSafeQf:
        sig_name = "VehSpdSafeQf"
        sig_start_bit = 239
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
        startbit = 239
        byte = 29
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class VehSpdQf:
        sig_name = "VehSpdQf"
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
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 207
        byte = 25
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class VehSpdChks:
        sig_name = "VehSpdChks"
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

    class BrkPedStkPercPerc:
        sig_name = "BrkPedStkPercPerc"
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

    class BrkPedlInfoChks:
        sig_name = "BrkPedlInfoChks"
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

    class VehMovgDir_UB:
        sig_name = "VehMovgDir_UB"
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

    class WhlPlsCntr_UB:
        sig_name = "WhlPlsCntr_UB"
        sig_start_bit = 292
        update_id_bit = 292
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 292
        byte = 36
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class EpbTotStsChks:
        sig_name = "EpbTotStsChks"
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

    class VehSpdSafe_UB:
        sig_name = "VehSpdSafe_UB"
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

    class WhlMovgDirFrntCntr:
        sig_name = "WhlMovgDirFrntCntr"
        sig_start_bit = 267
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
        startbit = 267
        byte = 33
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class BrkPedStkPercChks:
        sig_name = "BrkPedStkPercChks"
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

    class BrkPedlInfoCntr:
        sig_name = "BrkPedlInfoCntr"
        sig_start_bit = 131
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
        startbit = 131
        byte = 16
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DrvrBrkTqReq:
        sig_name = "DrvrBrkTqReq"
        sig_start_bit = 95
        update_id_bit = 96
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
        startbit = 95
        bmuws_info = [(11, 0b11111111, 0b00000000, 8, 0), (12, 0b11111110, 0b00000001, 7, 1)]

    class WhlEdgeFL:
        sig_name = "WhlEdgeFL"
        sig_start_bit = 55
        update_id_bit = 86
        sig_length = 8
        sig_value_factor = None
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

    class BrkLiReqCntr:
        sig_name = "BrkLiReqCntr"
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

    class BrkPedlInfoQf:
        sig_name = "BrkPedlInfoQf"
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
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 133
        byte = 16
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class VehSpdSafeChks:
        sig_name = "VehSpdSafeChks"
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

    class WhlPlsCntrFL:
        sig_name = "WhlPlsCntrFL"
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

    class VehSpdSafeSpd:
        sig_name = "VehSpdSafeSpd"
        sig_start_bit = 247
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
        startbit = 247
        bmuws_info = [(30, 0b11111111, 0b00000000, 8, 0), (31, 0b11111110, 0b00000001, 7, 1)]

    class EscSteerReq:
        sig_name = "EscSteerReq"
        sig_start_bit = 111
        update_id_bit = 113
        sig_length = 14
        sig_value_factor = 0.00390625
        sig_value_offset = 0
        sig_value_min = -7680
        sig_value_max = 7680
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 14
        startbit = 111
        bmuws_info = [(13, 0b11111111, 0b00000000, 8, 0), (14, 0b11111100, 0b00000011, 6, 2)]

    class VehSpd_UB:
        sig_name = "VehSpd_UB"
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

    class EpbTotStsEpbSt:
        sig_name = "EpbTotStsEpbSt"
        sig_start_bit = 175
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
        startbit = 175
        byte = 21
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class BrkLiReqBrkLiReq:
        sig_name = "BrkLiReqBrkLiReq"
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
        sig_value_table = {'ReqSts1_NotReqd': 0, 'ReqSts1_Reqd': 1}
        compute_method = None
        length = 1
        startbit = 31
        byte = 3
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class EpbTotSts_UB:
        sig_name = "EpbTotSts_UB"
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

    class RctaBrkActrAtv:
        sig_name = "RctaBrkActrAtv"
        sig_start_bit = 14
        update_id_bit = 12
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
        startbit = 14
        byte = 1
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class WhlMovgDirFrntDirRi:
        sig_name = "WhlMovgDirFrntDirRi"
        sig_start_bit = 269
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
        startbit = 269
        byte = 33
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class WhlMovgDirReDirLe:
        sig_name = "WhlMovgDirReDirLe"
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
        sig_value_table = {'DirLe_Undefined': 0, 'DirLe_Standstill': 1, 'DirLe_Forward': 2, 'DirLe_Backward': 3}
        compute_method = None
        length = 2
        startbit = 287
        byte = 35
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class WhlMovgDirReCntr:
        sig_name = "WhlMovgDirReCntr"
        sig_start_bit = 283
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
        startbit = 283
        byte = 35
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class LatStbIntvIndcn:
        sig_name = "LatStbIntvIndcn"
        sig_start_bit = 1
        update_id_bit = 15
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
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class WhlMovgDirRe_UB:
        sig_name = "WhlMovgDirRe_UB"
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

    class BrkPedlInfo_UB:
        sig_name = "BrkPedlInfo_UB"
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

    class BrkPedlInfoNotPsd:
        sig_name = "BrkPedlInfoNotPsd"
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
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 135
        byte = 16
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class EpbTotStsCntr:
        sig_name = "EpbTotStsCntr"
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

    class VehSpdCntr:
        sig_name = "VehSpdCntr"
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

    class DrvrBrkPReq:
        sig_name = "DrvrBrkPReq"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BrkPedStkPercCntr:
        sig_name = "BrkPedStkPercCntr"
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

    class BrkPedlInfoPsd:
        sig_name = "BrkPedlInfoPsd"
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
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 134
        byte = 16
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class EpbRollerActv:
        sig_name = "EpbRollerActv"
        sig_start_bit = 3
        update_id_bit = 2
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
        startbit = 3
        byte = 0
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3


class PSCM1Chassis1CANFDFr03:
    msg_name = "PSCM1Chassis1CANFDFr03"
    msg_id = 162
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "PSCM1"
    rx_nodes = ['CCUMCUAD']
    sig_group_dict = {'SteerADLatCtrlSts': ['SteerADLatCtrlStsAgReqNotInRangeSts', 'SteerADLatCtrlStsChks', 'SteerADLatCtrlStsCntr', 'SteerADLatCtrlStsDrvrOvrdReq', 'SteerADLatCtrlStsLowerLimActiveSts', 'SteerADLatCtrlStsRateLimActiveSts', 'SteerADLatCtrlStsReqNotMatchSts', 'SteerADLatCtrlStsSafeLimActiveSts', 'SteerADLatCtrlStsUpperLimActiveSts']}
    sig_group_dataid_dict = {}

    class SteerADLatCtrlStsCntr:
        sig_name = "SteerADLatCtrlStsCntr"
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

    class SteerADLatCtrlStsReqNotMatchSts:
        sig_name = "SteerADLatCtrlStsReqNotMatchSts"
        sig_start_bit = 21
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
        startbit = 21
        byte = 2
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class SteerADLatCtrlStsDrvrOvrdReq:
        sig_name = "SteerADLatCtrlStsDrvrOvrdReq"
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
        sig_value_table = {'ReqSts1_NotReqd': 0, 'ReqSts1_Reqd': 1}
        compute_method = None
        length = 1
        startbit = 31
        byte = 3
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class SteerADLatCtrlStsSafeLimActiveSts:
        sig_name = "SteerADLatCtrlStsSafeLimActiveSts"
        sig_start_bit = 19
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
        startbit = 19
        byte = 2
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class SteerADLatCtrlStsAgReqNotInRangeSts:
        sig_name = "SteerADLatCtrlStsAgReqNotInRangeSts"
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
        sig_value_table = {'ActvInActv2_Init': 0, 'ActvInActv2_InActv': 1, 'ActvInActv2_Actv': 2}
        compute_method = None
        length = 2
        startbit = 15
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class SteerADLatCtrlStsLowerLimActiveSts:
        sig_name = "SteerADLatCtrlStsLowerLimActiveSts"
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
        sig_value_table = {'ActvInActv2_Init': 0, 'ActvInActv2_InActv': 1, 'ActvInActv2_Actv': 2}
        compute_method = None
        length = 2
        startbit = 13
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class SteerADLatCtrlStsUpperLimActiveSts:
        sig_name = "SteerADLatCtrlStsUpperLimActiveSts"
        sig_start_bit = 17
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
        startbit = 17
        byte = 2
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class SteerADLatCtrlStsChks:
        sig_name = "SteerADLatCtrlStsChks"
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

    class SteerADLatCtrlSts_UB:
        sig_name = "SteerADLatCtrlSts_UB"
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

    class SteerADLatCtrlStsRateLimActiveSts:
        sig_name = "SteerADLatCtrlStsRateLimActiveSts"
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
        sig_value_table = {'ActvInActv2_Init': 0, 'ActvInActv2_InActv': 1, 'ActvInActv2_Actv': 2}
        compute_method = None
        length = 2
        startbit = 23
        byte = 2
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class PSCM1Chassis1CANFDFr02:
    msg_name = "PSCM1Chassis1CANFDFr02"
    msg_id = 96
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.015
    msg_length = 8
    tx_node = "PSCM1"
    rx_nodes = ['CCUMCUAD']
    sig_group_dict = {'SteerADASLatCtrlMod': ['SteerADASLatCtrlModChks', 'SteerADASLatCtrlModCntr', 'SteerADASLatCtrlModLatCtrlModCfmd']}
    sig_group_dataid_dict = {'SteerADASLatCtrlMod': 1039}

    class SteerExtReqTqVal:
        sig_name = "SteerExtReqTqVal"
        sig_start_bit = 22
        update_id_bit = 24
        sig_length = 14
        sig_value_factor = 0.00390625
        sig_value_offset = 0
        sig_value_min = -8192
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 14
        startbit = 22
        bmuws_info = [(2, 0b01111111, 0b10000000, 7, 0), (3, 0b11111110, 0b00000001, 7, 1)]

    class SteerADASLatCtrlModChks:
        sig_name = "SteerADASLatCtrlModChks"
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

    class SteerADASLatCtrlMod_UB:
        sig_name = "SteerADASLatCtrlMod_UB"
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

    class SteerADASLatCtrlModLatCtrlModCfmd:
        sig_name = "SteerADASLatCtrlModLatCtrlModCfmd"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 8
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AsyLatCtrlModReq_NoReq': 0, 'AsyLatCtrlModReq_LaneKeepAid': 1, 'AsyLatCtrlModReq_EmgyLaneKeepAid': 2, 'AsyLatCtrlModReq_EmgySteerSys': 3, 'AsyLatCtrlModReq_AutoEmgySteer': 4, 'AsyLatCtrlModReq_SteerAssc': 5, 'AsyLatCtrlModReq_DsrOverSteer': 6, 'AsyLatCtrlModReq_DsrMueSplit': 7, 'AsyLatCtrlModReq_DsrTrlrStaby': 8}
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class SteerADASLatCtrlModCntr:
        sig_name = "SteerADASLatCtrlModCntr"
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


class PSCM1ToCCUMCUADChassis1CANFDDiagRespFrame:
    msg_name = "PSCM1ToCCUMCUADChassis1CANFDDiagRespFrame"
    msg_id = 1648
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "PSCM1"
    rx_nodes = ['CCUMCUAD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class SUMChassis1CANFDFr03:
    msg_name = "SUMChassis1CANFDFr03"
    msg_id = 784
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.13
    msg_length = 16
    tx_node = "SUM"
    rx_nodes = ['CCUMCUAD', 'ETC']
    sig_group_dict = {'FrntAxleLoad': ['FrntAxleLoadLoadEstimn', 'FrntAxleLoadQF2'], 'ReAxleLoad': ['ReAxleLoadLoadEstimn', 'ReAxleLoadQF2']}
    sig_group_dataid_dict = {}

    class FrntAxleLoadLoadEstimn:
        sig_name = "FrntAxleLoadLoadEstimn"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 20
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

    class FrntAxleLoad_UB:
        sig_name = "FrntAxleLoad_UB"
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

    class URawSUM:
        sig_name = "URawSUM"
        sig_start_bit = 47
        update_id_bit = 54
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
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b10000000, 0b01111111, 1, 7)]

    class RoadIndex:
        sig_name = "RoadIndex"
        sig_start_bit = 38
        update_id_bit = 35
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'RoadIndex_Level1': 0, 'RoadIndex_Level2': 1, 'RoadIndex_Level3': 2, 'RoadIndex_Level4': 3, 'RoadIndex_Level5': 4, 'RoadIndex_Level6': 5, 'RoadIndex_Reserved1': 6, 'RoadIndex_Reserved2': 7}
        compute_method = None
        length = 3
        startbit = 38
        byte = 4
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class FrntAxleLoadQF2:
        sig_name = "FrntAxleLoadQF2"
        sig_start_bit = 1
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'QF2_Invalid': 0, 'QF2_Low': 1, 'QF2_High': 2}
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class ReAxleLoad_UB:
        sig_name = "ReAxleLoad_UB"
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

    class DamprActMod:
        sig_name = "DamprActMod"
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
        sig_value_table = {'DamprLvl_level1': 0, 'DamprLvl_level2': 1, 'DamprLvl_level3': 2, 'DamprLvl_Reserved1': 3, 'DamprLvl_Reserved2': 4, 'DamprLvl_Reserved3': 5, 'DamprLvl_Reserved4': 6, 'DamprLvl_Reserved5': 7}
        compute_method = None
        length = 3
        startbit = 7
        byte = 0
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class SUMLvlInhb:
        sig_name = "SUMLvlInhb"
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
        sig_value_table = {'LvlInhb_NoInhibit': 0, 'LvlInhb_LevelDownInhibit': 1, 'LvlInhb_LevelUpInhibit': 2, 'LvlInhb_LevelInhibit': 3}
        compute_method = None
        length = 2
        startbit = 34
        byte = 4
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class LCFailrIndcn:
        sig_name = "LCFailrIndcn"
        sig_start_bit = 25
        update_id_bit = 39
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FailrSts_NoError': 0, 'FailrSts_MajorErr': 1, 'FailrSts_CtitErr': 2}
        compute_method = None
        length = 2
        startbit = 25
        byte = 3
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class ReAxleLoadQF2:
        sig_name = "ReAxleLoadQF2"
        sig_start_bit = 49
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'QF2_Invalid': 0, 'QF2_Low': 1, 'QF2_High': 2}
        compute_method = None
        length = 2
        startbit = 49
        byte = 6
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class IRawSUM:
        sig_name = "IRawSUM"
        sig_start_bit = 23
        update_id_bit = 26
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
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111000, 0b00000111, 5, 3)]

    class ReAxleLoadLoadEstimn:
        sig_name = "ReAxleLoadLoadEstimn"
        sig_start_bit = 63
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 20
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


class CCUMCUADChassis1CANFDFr07:
    msg_name = "CCUMCUADChassis1CANFDFr07"
    msg_id = 642
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 64
    tx_node = "CCUMCUAD"
    rx_nodes = ['PSCM1', 'SUM']
    sig_group_dict = {'VehCfgDataGrp': ['VehCfgDataGrpVehCfgData1BlkIDBytePosn1', 'VehCfgDataGrpVehCfgData1BytePosn10', 'VehCfgDataGrpVehCfgData1BytePosn11', 'VehCfgDataGrpVehCfgData1BytePosn12', 'VehCfgDataGrpVehCfgData1BytePosn13', 'VehCfgDataGrpVehCfgData1BytePosn14', 'VehCfgDataGrpVehCfgData1BytePosn15', 'VehCfgDataGrpVehCfgData1BytePosn16', 'VehCfgDataGrpVehCfgData1BytePosn17', 'VehCfgDataGrpVehCfgData1BytePosn18', 'VehCfgDataGrpVehCfgData1BytePosn19', 'VehCfgDataGrpVehCfgData1BytePosn2', 'VehCfgDataGrpVehCfgData1BytePosn20', 'VehCfgDataGrpVehCfgData1BytePosn21', 'VehCfgDataGrpVehCfgData1BytePosn22', 'VehCfgDataGrpVehCfgData1BytePosn23', 'VehCfgDataGrpVehCfgData1BytePosn24', 'VehCfgDataGrpVehCfgData1BytePosn25', 'VehCfgDataGrpVehCfgData1BytePosn26', 'VehCfgDataGrpVehCfgData1BytePosn27', 'VehCfgDataGrpVehCfgData1BytePosn28', 'VehCfgDataGrpVehCfgData1BytePosn29', 'VehCfgDataGrpVehCfgData1BytePosn3', 'VehCfgDataGrpVehCfgData1BytePosn30', 'VehCfgDataGrpVehCfgData1BytePosn31', 'VehCfgDataGrpVehCfgData1BytePosn32', 'VehCfgDataGrpVehCfgData1BytePosn33', 'VehCfgDataGrpVehCfgData1BytePosn34', 'VehCfgDataGrpVehCfgData1BytePosn35', 'VehCfgDataGrpVehCfgData1BytePosn36', 'VehCfgDataGrpVehCfgData1BytePosn37', 'VehCfgDataGrpVehCfgData1BytePosn38', 'VehCfgDataGrpVehCfgData1BytePosn39', 'VehCfgDataGrpVehCfgData1BytePosn4', 'VehCfgDataGrpVehCfgData1BytePosn40', 'VehCfgDataGrpVehCfgData1BytePosn41', 'VehCfgDataGrpVehCfgData1BytePosn42', 'VehCfgDataGrpVehCfgData1BytePosn43', 'VehCfgDataGrpVehCfgData1BytePosn44', 'VehCfgDataGrpVehCfgData1BytePosn45', 'VehCfgDataGrpVehCfgData1BytePosn46', 'VehCfgDataGrpVehCfgData1BytePosn47', 'VehCfgDataGrpVehCfgData1BytePosn48', 'VehCfgDataGrpVehCfgData1BytePosn49', 'VehCfgDataGrpVehCfgData1BytePosn5', 'VehCfgDataGrpVehCfgData1BytePosn50', 'VehCfgDataGrpVehCfgData1BytePosn51', 'VehCfgDataGrpVehCfgData1BytePosn52', 'VehCfgDataGrpVehCfgData1BytePosn53', 'VehCfgDataGrpVehCfgData1BytePosn54', 'VehCfgDataGrpVehCfgData1BytePosn55', 'VehCfgDataGrpVehCfgData1BytePosn56', 'VehCfgDataGrpVehCfgData1BytePosn57', 'VehCfgDataGrpVehCfgData1BytePosn58', 'VehCfgDataGrpVehCfgData1BytePosn59', 'VehCfgDataGrpVehCfgData1BytePosn6', 'VehCfgDataGrpVehCfgData1BytePosn60', 'VehCfgDataGrpVehCfgData1BytePosn61', 'VehCfgDataGrpVehCfgData1BytePosn62', 'VehCfgDataGrpVehCfgData1BytePosn63', 'VehCfgDataGrpVehCfgData1BytePosn64', 'VehCfgDataGrpVehCfgData1BytePosn7', 'VehCfgDataGrpVehCfgData1BytePosn8', 'VehCfgDataGrpVehCfgData1BytePosn9']}
    sig_group_dataid_dict = {}

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


class PSCM1Chassis1CANFDFr08:
    msg_name = "PSCM1Chassis1CANFDFr08"
    msg_id = 928
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.4
    msg_length = 8
    tx_node = "PSCM1"
    rx_nodes = ['CCUMCUAD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class SteerAssiLvlCfmd:
        sig_name = "SteerAssiLvlCfmd"
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
        sig_value_table = {'SteerAssiLvl_UnknownLevel': 0, 'SteerAssiLvl_Level1': 1, 'SteerAssiLvl_Level2': 2, 'SteerAssiLvl_Level3': 3, 'SteerAssiLvl_Level4': 4, 'SteerAssiLvl_Reserved1': 5, 'SteerAssiLvl_Reserved2': 6, 'SteerAssiLvl_Reserved3': 7}
        compute_method = None
        length = 3
        startbit = 7
        byte = 0
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5


class CCUMCUADChassis1CANFDFr03:
    msg_name = "CCUMCUADChassis1CANFDFr03"
    msg_id = 256
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.025
    msg_length = 48
    tx_node = "CCUMCUAD"
    rx_nodes = ['PSCM1', 'SRS', 'BCU1']
    sig_group_dict = {'ReAutoEmgyBrk': ['ReAutoEmgyBrkChks', 'ReAutoEmgyBrkCntr', 'ReAutoEmgyBrkReq'], 'AEBBrkHptcWarnReq': ['AEBBrkHptcWarnReqBrkHptcWarnReqForAutDrv', 'AEBBrkHptcWarnReqChks', 'AEBBrkHptcWarnReqCntr'], 'DBSEnaDecelGroup': ['DBSEnaDecelGroupAsySftyEnaDecelByDBS', 'DBSEnaDecelGroupChks', 'DBSEnaDecelGroupCntr'], 'RcwBrkReq': ['RcwBrkReqChks', 'RcwBrkReqCntr', 'RcwBrkReqRcwBrkReq'], 'SteerTqAddlForAes': ['SteerTqAddlForAesChks', 'SteerTqAddlForAesCntr', 'SteerTqAddlForAesSteerTqAddl'], 'AEBDecelGroupSafe': ['AEBDecelGroupSafeChks', 'AEBDecelGroupSafeCntr', 'AEBDecelGroupSafeSftyDecelReq', 'AEBDecelGroupSafeSftyEnaDecel'], 'ADASLatCtrlModReqGroup': ['ADASLatCtrlModReqGroupChks', 'ADASLatCtrlModReqGroupCntr', 'ADASLatCtrlModReqGroupLatCtrlModCfmd'], 'SteerTqAddlForEss': ['SteerTqAddlForEssChks', 'SteerTqAddlForEssCntr', 'SteerTqAddlForEssSteerTqAddl'], 'RctaBrkReq': ['RctaBrkReqChks', 'RctaBrkReqCntr', 'RctaBrkReqRctaBrkReq']}
    sig_group_dataid_dict = {'ReAutoEmgyBrk': 1029, 'AEBBrkHptcWarnReq': 1026, 'DBSEnaDecelGroup': 1025, 'RcwBrkReq': 1027, 'SteerTqAddlForAes': 1031, 'AEBDecelGroupSafe': 1024, 'ADASLatCtrlModReqGroup': 1023, 'SteerTqAddlForEss': 1030, 'RctaBrkReq': 1028}

    class AEBBrkHptcWarnReqCntr:
        sig_name = "AEBBrkHptcWarnReqCntr"
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

    class ReAutoEmgyBrkCntr:
        sig_name = "ReAutoEmgyBrkCntr"
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

    class ReAutoEmgyBrk_UB:
        sig_name = "ReAutoEmgyBrk_UB"
        sig_start_bit = 138
        update_id_bit = 138
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 138
        byte = 17
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class ReAutoEmgyBrkReq:
        sig_name = "ReAutoEmgyBrkReq"
        sig_start_bit = 139
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
        startbit = 139
        byte = 17
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class AEBBrkHptcWarnReq_UB:
        sig_name = "AEBBrkHptcWarnReq_UB"
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

    class BrkPrefillReq:
        sig_name = "BrkPrefillReq"
        sig_start_bit = 18
        update_id_bit = 17
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
        startbit = 18
        byte = 2
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class DBSEnaDecelGroup_UB:
        sig_name = "DBSEnaDecelGroup_UB"
        sig_start_bit = 90
        update_id_bit = 90
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 90
        byte = 11
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class RcwBrkReq_UB:
        sig_name = "RcwBrkReq_UB"
        sig_start_bit = 122
        update_id_bit = 122
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 122
        byte = 15
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class CllsnMtgtnFctSts:
        sig_name = "CllsnMtgtnFctSts"
        sig_start_bit = 69
        update_id_bit = 66
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CllsnMtgtnFctSts_Reserved1': 0, 'CllsnMtgtnFctSts_Off': 1, 'CllsnMtgtnFctSts_On': 2, 'CllsnMtgtnFctSts_TemporaryError': 3, 'CllsnMtgtnFctSts_PermenentError': 4, 'CllsnMtgtnFctSts_AEB_PEDNotAvalid': 5, 'CllsnMtgtnFctSts_Reserved2': 6, 'CllsnMtgtnFctSts_Reserved3': 7}
        compute_method = None
        length = 3
        startbit = 69
        byte = 8
        mask = 0b00111000
        unmask = 0b11000111
        shift = 3

    class ReAutoEmgyBrkChks:
        sig_name = "ReAutoEmgyBrkChks"
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

    class SteerTqAddlForAesCntr:
        sig_name = "SteerTqAddlForAesCntr"
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

    class RctaBrkReqChks:
        sig_name = "RctaBrkReqChks"
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

    class ADASLatCtrlModReqGroupLatCtrlModCfmd:
        sig_name = "ADASLatCtrlModReqGroupLatCtrlModCfmd"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 8
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AsyLatCtrlModReq_NoReq': 0, 'AsyLatCtrlModReq_LaneKeepAid': 1, 'AsyLatCtrlModReq_EmgyLaneKeepAid': 2, 'AsyLatCtrlModReq_EmgySteerSys': 3, 'AsyLatCtrlModReq_AutoEmgySteer': 4, 'AsyLatCtrlModReq_SteerAssc': 5, 'AsyLatCtrlModReq_DsrOverSteer': 6, 'AsyLatCtrlModReq_DsrMueSplit': 7, 'AsyLatCtrlModReq_DsrTrlrStaby': 8}
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class AEBDecelGroupSafeChks:
        sig_name = "AEBDecelGroupSafeChks"
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

    class AEBDecelGroupSafeCntr:
        sig_name = "AEBDecelGroupSafeCntr"
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

    class SteerTqAddlForAesChks:
        sig_name = "SteerTqAddlForAesChks"
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

    class SteerTqAddlForAes_UB:
        sig_name = "SteerTqAddlForAes_UB"
        sig_start_bit = 173
        update_id_bit = 173
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 173
        byte = 21
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class RcwBrkReqCntr:
        sig_name = "RcwBrkReqCntr"
        sig_start_bit = 127
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
        startbit = 127
        byte = 15
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class CllsnThreat:
        sig_name = "CllsnThreat"
        sig_start_bit = 65
        update_id_bit = 79
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CllsnThreat1_Ukwn': 0, 'CllsnThreat1_ThreatLo': 1, 'CllsnThreat1_ThreatMed': 2, 'CllsnThreat1_ThreatHi': 3}
        compute_method = None
        length = 2
        startbit = 65
        byte = 8
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class AEBDecelGroupSafeSftyEnaDecel:
        sig_name = "AEBDecelGroupSafeSftyEnaDecel"
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

    class AEBBrkHptcWarnReqChks:
        sig_name = "AEBBrkHptcWarnReqChks"
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

    class RctaBrkReqRctaBrkReq:
        sig_name = "RctaBrkReqRctaBrkReq"
        sig_start_bit = 107
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'YesNo1_Yes': 0, 'YesNo1_No': 1}
        compute_method = None
        length = 1
        startbit = 107
        byte = 13
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class AEBDecelGroupSafe_UB:
        sig_name = "AEBDecelGroupSafe_UB"
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

    class ADASSteerWhlHptcWarnReq:
        sig_name = "ADASSteerWhlHptcWarnReq"
        sig_start_bit = 22
        update_id_bit = 21
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
        startbit = 22
        byte = 2
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class SteerTqAddlForEssCntr:
        sig_name = "SteerTqAddlForEssCntr"
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

    class ADASLatCtrlModReqGroupCntr:
        sig_name = "ADASLatCtrlModReqGroupCntr"
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

    class SteerTqAddlForEssSteerTqAddl:
        sig_name = "SteerTqAddlForEssSteerTqAddl"
        sig_start_bit = 187
        update_id_bit = None
        sig_length = 14
        sig_value_factor = 0.00390625
        sig_value_offset = 0
        sig_value_min = -8192
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 14
        startbit = 187
        bmuws_info = [(23, 0b00001111, 0b11110000, 4, 0), (24, 0b11111111, 0b00000000, 8, 0), (25, 0b11000000, 0b00111111, 2, 6)]

    class DBSEnaDecelGroupChks:
        sig_name = "DBSEnaDecelGroupChks"
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

    class AEBDecelGroupSafeSftyDecelReq:
        sig_name = "AEBDecelGroupSafeSftyDecelReq"
        sig_start_bit = 63
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 150
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

    class ADASLatCtrlModReqGroup_UB:
        sig_name = "ADASLatCtrlModReqGroup_UB"
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

    class SteerTqAddlForAesSteerTqAddl:
        sig_name = "SteerTqAddlForAesSteerTqAddl"
        sig_start_bit = 155
        update_id_bit = None
        sig_length = 14
        sig_value_factor = 0.00390625
        sig_value_offset = 0
        sig_value_min = -8192
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 14
        startbit = 155
        bmuws_info = [(19, 0b00001111, 0b11110000, 4, 0), (20, 0b11111111, 0b00000000, 8, 0), (21, 0b11000000, 0b00111111, 2, 6)]

    class RcwBrkReqRcwBrkReq:
        sig_name = "RcwBrkReqRcwBrkReq"
        sig_start_bit = 123
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
        startbit = 123
        byte = 15
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class DBSEnaDecelGroupAsySftyEnaDecelByDBS:
        sig_name = "DBSEnaDecelGroupAsySftyEnaDecelByDBS"
        sig_start_bit = 91
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
        startbit = 91
        byte = 11
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class RctaBrkReqCntr:
        sig_name = "RctaBrkReqCntr"
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

    class DBSEnaDecelGroupCntr:
        sig_name = "DBSEnaDecelGroupCntr"
        sig_start_bit = 95
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
        startbit = 95
        byte = 11
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class AEBBrkHptcWarnReqBrkHptcWarnReqForAutDrv:
        sig_name = "AEBBrkHptcWarnReqBrkHptcWarnReqForAutDrv"
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
        sig_value_table = {'CllsnThreat1_Ukwn': 0, 'CllsnThreat1_ThreatLo': 1, 'CllsnThreat1_ThreatMed': 2, 'CllsnThreat1_ThreatHi': 3}
        compute_method = None
        length = 2
        startbit = 39
        byte = 4
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class SteerTqAddlForEss_UB:
        sig_name = "SteerTqAddlForEss_UB"
        sig_start_bit = 205
        update_id_bit = 205
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 205
        byte = 25
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class AEBStandStillReq:
        sig_name = "AEBStandStillReq"
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

    class RcwBrkReqChks:
        sig_name = "RcwBrkReqChks"
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

    class RctaBrkReq_UB:
        sig_name = "RctaBrkReq_UB"
        sig_start_bit = 106
        update_id_bit = 106
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 106
        byte = 13
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class CllsnAidPost:
        sig_name = "CllsnAidPost"
        sig_start_bit = 71
        update_id_bit = 70
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
        startbit = 71
        byte = 8
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class SteerTqAddlForEssChks:
        sig_name = "SteerTqAddlForEssChks"
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

    class ADASLatCtrlModReqGroupChks:
        sig_name = "ADASLatCtrlModReqGroupChks"
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


class CCUMCUADToSUMChassis1CANFDDiagReqFrame:
    msg_name = "CCUMCUADToSUMChassis1CANFDDiagReqFrame"
    msg_id = 1812
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "CCUMCUAD"
    rx_nodes = ['SUM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class CCUMCUADChassis1CANFDNmFr:
    msg_name = "CCUMCUADChassis1CANFDNmFr"
    msg_id = 1282
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CCUMCUAD"
    rx_nodes = ['BCU1']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class CCUMCUADChassis1CANFDFr10:
    msg_name = "CCUMCUADChassis1CANFDFr10"
    msg_id = 643
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 32
    tx_node = "CCUMCUAD"
    rx_nodes = ['PSCM1', 'SUM']
    sig_group_dict = {'LoadPwrActSts': ['LoadPwrActStsACCMPwrActSts', 'LoadPwrActStsAFUPwrActSts', 'LoadPwrActStsAGMPwrActSts', 'LoadPwrActStsAGUPwrActSts', 'LoadPwrActStsALMLPwrActSts', 'LoadPwrActStsALMRPwrActSts', 'LoadPwrActStsAWMPwrActSts', 'LoadPwrActStsBCCPPwrActSts', 'LoadPwrActStsBCFVPwrActSts', 'LoadPwrActStsBCTVPwrActSts', 'LoadPwrActStsBEXVPwrActSts', 'LoadPwrActStsBNCMPwrActSts', 'LoadPwrActStsBoosterBlowerPwrActSts', 'LoadPwrActStsCCTVPwrActSts', 'LoadPwrActStsCDPwrActSts', 'LoadPwrActStsCERVPwrActSts', 'LoadPwrActStsCRCMPwrActSts', 'LoadPwrActStsCSOVPwrActSts', 'LoadPwrActStsDCTVPwrActSts', 'LoadPwrActStsDICPwrActSts', 'LoadPwrActStsDMFLPwrActSts', 'LoadPwrActStsDPODPwrActSts', 'LoadPwrActStsDRFPwrActSts', 'LoadPwrActStsDRMFRPwrActSts', 'LoadPwrActStsDRMRLPwrActSts', 'LoadPwrActStsDRMRRPwrActSts', 'LoadPwrActStsECTVPwrActSts', 'LoadPwrActStsEDCPPwrActSts', 'LoadPwrActStsEGSMPwrActSts', 'LoadPwrActStsEPMPwrActSts', 'LoadPwrActStsFCSIPwrActSts', 'LoadPwrActStsFEXVPwrActSts', 'LoadPwrActStsFLRPwrActSts', 'LoadPwrActStsFSRLPwrActSts', 'LoadPwrActStsFSRRPwrActSts', 'LoadPwrActStsHBMFPwrActSts', 'LoadPwrActStsHBMRPwrActSts', 'LoadPwrActStsHCCPPwrActSts', 'LoadPwrActStsHCMLPwrActSts', 'LoadPwrActStsHCMRPwrActSts', 'LoadPwrActStsHCTVPwrActSts', 'LoadPwrActStsHODPwrActSts', 'LoadPwrActStsHUBFPwrActSts', 'LoadPwrActStsHUBRPwrActSts', 'LoadPwrActStsHVAHPwrActSts', 'LoadPwrActStsHVCHPwrActSts', 'LoadPwrActStsHVCMPwrActSts', 'LoadPwrActStsIEMPwrActSts', 'LoadPwrActStsIRMMPwrActSts', 'LoadPwrActStsLCTVPwrActSts', 'LoadPwrActStsLPODPwrActSts', 'LoadPwrActStsMGMPwrActSts', 'LoadPwrActStsMMDPwrActSts', 'LoadPwrActStsMMPPwrActSts', 'LoadPwrActStsNKRPwrActSts', 'LoadPwrActStsOHCPwrActSts', 'LoadPwrActStsOPCFPwrActSts', 'LoadPwrActStsOPCRPwrActSts', 'LoadPwrActStsPMSIPwrActSts', 'LoadPwrActStsPOFPwrActSts', 'LoadPwrActStsPORPwrActSts', 'LoadPwrActStsPPODPwrActSts', 'LoadPwrActStsRCMLPwrActSts', 'LoadPwrActStsRCMRPwrActSts', 'LoadPwrActStsReserved1', 'LoadPwrActStsReserved10', 'LoadPwrActStsReserved11', 'LoadPwrActStsReserved12', 'LoadPwrActStsReserved13', 'LoadPwrActStsReserved14', 'LoadPwrActStsReserved15', 'LoadPwrActStsReserved16', 'LoadPwrActStsReserved17', 'LoadPwrActStsReserved18', 'LoadPwrActStsReserved2', 'LoadPwrActStsReserved3', 'LoadPwrActStsReserved4', 'LoadPwrActStsReserved5', 'LoadPwrActStsReserved6', 'LoadPwrActStsReserved7', 'LoadPwrActStsReserved8', 'LoadPwrActStsReserved9', 'LoadPwrActStsREXVPwrActSts', 'LoadPwrActStsRLMMPwrActSts', 'LoadPwrActStsRLSMPwrActSts', 'LoadPwrActStsRMLPwrActSts', 'LoadPwrActStsRPODPwrActSts', 'LoadPwrActStsRRMMPwrActSts', 'LoadPwrActStsRSOV1PwrActSts', 'LoadPwrActStsRSOV2PwrActSts', 'LoadPwrActStsSCMFPwrActSts', 'LoadPwrActStsSCMRPwrActSts', 'LoadPwrActStsSODLPwrActSts', 'LoadPwrActStsSODRPwrActSts', 'LoadPwrActStsSRSPwrActSts', 'LoadPwrActStsSWTLPwrActSts', 'LoadPwrActStsSWTRPwrActSts', 'LoadPwrActStsTERVPwrActSts', 'LoadPwrActStsUSBR1PwrActSts', 'LoadPwrActStsUSBR2PwrActSts', 'LoadPwrActStsUWBPwrActSts', 'LoadPwrActStsVCUPwrActSts', 'LoadPwrActStsWERVPwrActSts', 'LoadPwrActStsWPCPwrActSts']}
    sig_group_dataid_dict = {}

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


class PSCM1Chassis1CANFDNmFr:
    msg_name = "PSCM1Chassis1CANFDNmFr"
    msg_id = 1286
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "PSCM1"
    rx_nodes = ['CCUMCUAD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class PSCM1Chassis1CANFDFr04:
    msg_name = "PSCM1Chassis1CANFDFr04"
    msg_id = 257
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.025
    msg_length = 12
    tx_node = "PSCM1"
    rx_nodes = ['CCUMCUAD']
    sig_group_dict = {'SteerWhlHndOn': ['SteerWhlHndOnSts', 'SteerWhlHndOnStsQly'], 'SteerSysSts': ['SteerSysStsCapabilitySts', 'SteerSysStsChks', 'SteerSysStsCntr', 'SteerSysStsCtrlSts', 'SteerSysStsModCfmd', 'SteerSysStsQf', 'SteerSysStsSteerDegraded']}
    sig_group_dataid_dict = {}

    class SteerWhlHndOnStsQly:
        sig_name = "SteerWhlHndOnStsQly"
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

    class SteerWhlHndOn_UB:
        sig_name = "SteerWhlHndOn_UB"
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

    class SteerSysStsCtrlSts:
        sig_name = "SteerSysStsCtrlSts"
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
        sig_value_table = {'SteerADSLatCtrlRouteSts_Primary': 0, 'SteerADSLatCtrlRouteSts_Secondary': 1}
        compute_method = None
        length = 1
        startbit = 41
        byte = 5
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class SteerSysStsQf:
        sig_name = "SteerSysStsQf"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 2
        startbit = 47
        byte = 5
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class SteerSysStsSteerDegraded:
        sig_name = "SteerSysStsSteerDegraded"
        sig_start_bit = 45
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 11
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SteerADSLatCtrlDegradedSts_NotDegraded': 0, 'SteerADSLatCtrlDegradedSts_RedWarning': 1, 'SteerADSLatCtrlDegradedSts_YellowWarning1': 2, 'SteerADSLatCtrlDegradedSts_YellowWarning2': 3, 'SteerADSLatCtrlDegradedSts_YellowWarning3': 4, 'SteerADSLatCtrlDegradedSts_YellowWarning4': 5, 'SteerADSLatCtrlDegradedSts_YellowWarning5': 6, 'SteerADSLatCtrlDegradedSts_YellowWarning6': 7, 'SteerADSLatCtrlDegradedSts_YellowWarning7': 8, 'SteerADSLatCtrlDegradedSts_YellowWarning8': 9, 'SteerADSLatCtrlDegradedSts_YellowWarning9': 10, 'SteerADSLatCtrlDegradedSts_Reserved1': 11}
        compute_method = None
        length = 4
        startbit = 45
        byte = 5
        mask = 0b00111100
        unmask = 0b11000011
        shift = 2

    class SteerWhlHndOnSts:
        sig_name = "SteerWhlHndOnSts"
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
        sig_value_table = {'SteerWhlHndOnSts_NoInformation': 0, 'SteerWhlHndOnSts_HandsOffDetected': 1, 'SteerWhlHndOnSts_NotHandsOnOrHandsOff': 2, 'SteerWhlHndOnSts_HandsOnDetected': 3}
        compute_method = None
        length = 2
        startbit = 55
        byte = 6
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class SteerFailrSts:
        sig_name = "SteerFailrSts"
        sig_start_bit = 7
        update_id_bit = 4
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SteerFailrSts_NoFailure': 0, 'SteerFailrSts_NoUse': 1, 'SteerFailrSts_RedFailure': 2, 'SteerFailrSts_YellowFailure': 3, 'SteerFailrSts_TemperoryAssitFailure': 4, 'SteerFailrSts_Reserved1': 5, 'SteerFailrSts_Reserved2': 6, 'SteerFailrSts_Reserved3': 7}
        compute_method = None
        length = 3
        startbit = 7
        byte = 0
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class SteerServoAvlSts:
        sig_name = "SteerServoAvlSts"
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
        sig_value_table = {'AvlSts1_Avl': 0, 'AvlSts1_NotAvl': 1}
        compute_method = None
        length = 1
        startbit = 20
        byte = 2
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class SteerSysSts_UB:
        sig_name = "SteerSysSts_UB"
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

    class SteerMotTqVal:
        sig_name = "SteerMotTqVal"
        sig_start_bit = 3
        update_id_bit = 21
        sig_length = 14
        sig_value_factor = 0.00390625
        sig_value_offset = 0
        sig_value_min = -8192
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 14
        startbit = 3
        bmuws_info = [(0, 0b00001111, 0b11110000, 4, 0), (1, 0b11111111, 0b00000000, 8, 0), (2, 0b11000000, 0b00111111, 2, 6)]

    class SteerSysStsModCfmd:
        sig_name = "SteerSysStsModCfmd"
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
        sig_value_table = {'SteerADSLatCtrlModSts_NoADModeActivated': 0, 'SteerADSLatCtrlModSts_Parking': 1, 'SteerADSLatCtrlModSts_ANP': 2, 'SteerADSLatCtrlModSts_Reserved1': 3}
        compute_method = None
        length = 2
        startbit = 37
        byte = 4
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class SteerSysStsChks:
        sig_name = "SteerSysStsChks"
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

    class SteerSysStsCntr:
        sig_name = "SteerSysStsCntr"
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

    class SteerSysStsCapabilitySts:
        sig_name = "SteerSysStsCapabilitySts"
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
        sig_value_table = {'SteerADSLatCtrlFailrSts_Red': 0, 'SteerADSLatCtrlFailrSts_Yellow': 1, 'SteerADSLatCtrlFailrSts_Green': 2, 'SteerADSLatCtrlFailrSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 39
        byte = 4
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class BCU1Chassis1CANFDFr01:
    msg_name = "BCU1Chassis1CANFDFr01"
    msg_id = 48
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 48
    tx_node = "BCU1"
    rx_nodes = ['CCUMCUAD', 'PSCM1']
    sig_group_dict = {'BrkSysSt': ['BrkSysStBrkAdDegrad', 'BrkSysStCapibility', 'BrkSysStChks', 'BrkSysStCntr', 'BrkSysStCtrlSts', 'BrkSysStModCfmd'], 'EpbCoornPrim': ['EpbCoornPrimApplyFunctionalitiesAvailable', 'EpbCoornPrimChks', 'EpbCoornPrimCntr', 'EpbCoornPrimDiagOperationMode', 'EpbCoornPrimDriveAwayIntention', 'EpbCoornPrimHostAvailabilityFull', 'EpbCoornPrimHostAvailabilityRelOnly', 'EpbCoornPrimPrimarySystemAvailable', 'EpbCoornPrimReserve1', 'EpbCoornPrimReserve2', 'EpbCoornPrimReserve3', 'EpbCoornPrimRollerTestBench'], 'BrkMstCtrlModeReqRdnt': ['BrkMstCtrlModeReqRdntChks', 'BrkMstCtrlModeReqRdntCntr', 'BrkMstCtrlModeReqRdntReq'], 'WhlSpdRe': ['WhlSpdReChks', 'WhlSpdReCntr', 'WhlSpdReLeQf', 'WhlSpdReLeSpd', 'WhlSpdReRiQf', 'WhlSpdReRiSpd'], 'BrkSysStPrimRdnt': ['BrkSysStPrimRdntBrkSysSts', 'BrkSysStPrimRdntChks', 'BrkSysStPrimRdntCntr'], 'WhlSpdFrnt': ['WhlSpdFrntChks', 'WhlSpdFrntCntr', 'WhlSpdFrntLeQf', 'WhlSpdFrntLeSpd', 'WhlSpdFrntRiQf', 'WhlSpdFrntRiSpd'], 'EpbReqMst': ['EpbReqMstChks', 'EpbReqMstCntr', 'EpbReqMstEpbReq']}
    sig_group_dataid_dict = {'WhlSpdRe': 1055, 'WhlSpdFrnt': 1045}

    class EpbCoornPrimCntr:
        sig_name = "EpbCoornPrimCntr"
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

    class WhlSpdFrntLeSpd:
        sig_name = "WhlSpdFrntLeSpd"
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

    class BrkSysStChks:
        sig_name = "BrkSysStChks"
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

    class EpbCoornPrimPrimarySystemAvailable:
        sig_name = "EpbCoornPrimPrimarySystemAvailable"
        sig_start_bit = 86
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CoornSt_Inactive': 0, 'CoornSt_Active': 1}
        compute_method = None
        length = 1
        startbit = 86
        byte = 10
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class BrkSysStPrimRdntChks:
        sig_name = "BrkSysStPrimRdntChks"
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

    class BrkSysStCtrlSts:
        sig_name = "BrkSysStCtrlSts"
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
        sig_value_table = {'CtrlSts_Primary': 0, 'CtrlSts_Secondary': 1}
        compute_method = None
        length = 1
        startbit = 36
        byte = 4
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class EpbCoornPrimDiagOperationMode:
        sig_name = "EpbCoornPrimDiagOperationMode"
        sig_start_bit = 78
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CoornSt_Inactive': 0, 'CoornSt_Active': 1}
        compute_method = None
        length = 1
        startbit = 78
        byte = 9
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class EpbReqMstCntr:
        sig_name = "EpbReqMstCntr"
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

    class BrkMstCtrlModeReqRdntCntr:
        sig_name = "BrkMstCtrlModeReqRdntCntr"
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

    class BrkSysSt_UB:
        sig_name = "BrkSysSt_UB"
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

    class BrkMstCtrlModeReqRdntReq:
        sig_name = "BrkMstCtrlModeReqRdntReq"
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

    class EpbCoornPrim_UB:
        sig_name = "EpbCoornPrim_UB"
        sig_start_bit = 81
        update_id_bit = 81
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 81
        byte = 10
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class WhlSpdReChks:
        sig_name = "WhlSpdReChks"
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

    class BrkSysStPrimRdntBrkSysSts:
        sig_name = "BrkSysStPrimRdntBrkSysSts"
        sig_start_bit = 55
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
        startbit = 55
        byte = 6
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class EpbCoornPrimReserve1:
        sig_name = "EpbCoornPrimReserve1"
        sig_start_bit = 85
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CoornSt_Inactive': 0, 'CoornSt_Active': 1}
        compute_method = None
        length = 1
        startbit = 85
        byte = 10
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class WhlSpdFrntRiSpd:
        sig_name = "WhlSpdFrntRiSpd"
        sig_start_bit = 143
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
        startbit = 143
        bmuws_info = [(17, 0b11111111, 0b00000000, 8, 0), (18, 0b11111110, 0b00000001, 7, 1)]

    class BrkSysStModCfmd:
        sig_name = "BrkSysStModCfmd"
        sig_start_bit = 35
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
        startbit = 35
        byte = 4
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class EpbReqMstChks:
        sig_name = "EpbReqMstChks"
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

    class WhlSpdReLeSpd:
        sig_name = "WhlSpdReLeSpd"
        sig_start_bit = 175
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
        startbit = 175
        bmuws_info = [(21, 0b11111111, 0b00000000, 8, 0), (22, 0b11111110, 0b00000001, 7, 1)]

    class BrkMstCtrlModeReqRdnt_UB:
        sig_name = "BrkMstCtrlModeReqRdnt_UB"
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

    class EpbCoornPrimReserve2:
        sig_name = "EpbCoornPrimReserve2"
        sig_start_bit = 84
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CoornSt_Inactive': 0, 'CoornSt_Active': 1}
        compute_method = None
        length = 1
        startbit = 84
        byte = 10
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class EpbCoornPrimHostAvailabilityFull:
        sig_name = "EpbCoornPrimHostAvailabilityFull"
        sig_start_bit = 76
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CoornSt_Inactive': 0, 'CoornSt_Active': 1}
        compute_method = None
        length = 1
        startbit = 76
        byte = 9
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class BrkSysStCntr:
        sig_name = "BrkSysStCntr"
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

    class WhlSpdRe_UB:
        sig_name = "WhlSpdRe_UB"
        sig_start_bit = 205
        update_id_bit = 205
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 205
        byte = 25
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class EpbCoornPrimRollerTestBench:
        sig_name = "EpbCoornPrimRollerTestBench"
        sig_start_bit = 82
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CoornSt_Inactive': 0, 'CoornSt_Active': 1}
        compute_method = None
        length = 1
        startbit = 82
        byte = 10
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class WhlSpdReRiSpd:
        sig_name = "WhlSpdReRiSpd"
        sig_start_bit = 191
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
        startbit = 191
        bmuws_info = [(23, 0b11111111, 0b00000000, 8, 0), (24, 0b11111110, 0b00000001, 7, 1)]

    class BrkSysStBrkAdDegrad:
        sig_name = "BrkSysStBrkAdDegrad"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class EpbReqMstEpbReq:
        sig_name = "EpbReqMstEpbReq"
        sig_start_bit = 103
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EpbReq_Noreq': 0, 'EpbReq_RollerTestReq': 1, 'EpbReq_EmergencyApplyReq': 2, 'EpbReq_ApplyReq': 3, 'EpbReq_ReleaseReq': 4, 'EpbReq_DclBrkMechReq': 5, 'EpbReq_DARReq': 6, 'EpbReq_AAReq': 7, 'EpbReq_ApplyByExternal': 8, 'EpbReq_ReleaseByExternal': 9, 'EpbReq_BrkPadAdjust': 10, 'EpbReq_HappreparationReq': 11, 'EpbReq_EPbBackupReq': 12, 'EpbReq_ApplyByAVH': 13, 'EpbReq_ApplyByACB': 14, 'EpbReq_ReleaseBySoftSwt': 15}
        compute_method = None
        length = 4
        startbit = 103
        byte = 12
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class WhlSpdFrntChks:
        sig_name = "WhlSpdFrntChks"
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

    class EpbCoornPrimApplyFunctionalitiesAvailable:
        sig_name = "EpbCoornPrimApplyFunctionalitiesAvailable"
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
        sig_value_table = {'CoornSt_Inactive': 0, 'CoornSt_Active': 1}
        compute_method = None
        length = 1
        startbit = 79
        byte = 9
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class WhlSpdFrntCntr:
        sig_name = "WhlSpdFrntCntr"
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

    class WhlSpdReLeQf:
        sig_name = "WhlSpdReLeQf"
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
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 167
        byte = 20
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class WhlSpdReRiQf:
        sig_name = "WhlSpdReRiQf"
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
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 165
        byte = 20
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class BrkSysStCapibility:
        sig_name = "BrkSysStCapibility"
        sig_start_bit = 39
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
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class BrkSysStPrimRdnt_UB:
        sig_name = "BrkSysStPrimRdnt_UB"
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

    class WhlSpdFrntRiQf:
        sig_name = "WhlSpdFrntRiQf"
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
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 117
        byte = 14
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class WhlSpdFrnt_UB:
        sig_name = "WhlSpdFrnt_UB"
        sig_start_bit = 206
        update_id_bit = 206
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 206
        byte = 25
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class EpbCoornPrimHostAvailabilityRelOnly:
        sig_name = "EpbCoornPrimHostAvailabilityRelOnly"
        sig_start_bit = 87
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CoornSt_Inactive': 0, 'CoornSt_Active': 1}
        compute_method = None
        length = 1
        startbit = 87
        byte = 10
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class BrkMstCtrlModeReqRdntChks:
        sig_name = "BrkMstCtrlModeReqRdntChks"
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

    class EpbCoornPrimChks:
        sig_name = "EpbCoornPrimChks"
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

    class EpbReqMst_UB:
        sig_name = "EpbReqMst_UB"
        sig_start_bit = 207
        update_id_bit = 207
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 207
        byte = 25
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class WhlSpdReCntr:
        sig_name = "WhlSpdReCntr"
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

    class EpbCoornPrimDriveAwayIntention:
        sig_name = "EpbCoornPrimDriveAwayIntention"
        sig_start_bit = 77
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CoornSt_Inactive': 0, 'CoornSt_Active': 1}
        compute_method = None
        length = 1
        startbit = 77
        byte = 9
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class BrkSysStPrimRdntCntr:
        sig_name = "BrkSysStPrimRdntCntr"
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

    class EpbCoornPrimReserve3:
        sig_name = "EpbCoornPrimReserve3"
        sig_start_bit = 83
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CoornSt_Inactive': 0, 'CoornSt_Active': 1}
        compute_method = None
        length = 1
        startbit = 83
        byte = 10
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class WhlSpdFrntLeQf:
        sig_name = "WhlSpdFrntLeQf"
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


class CCUMCUADChassis1CANFDFr04:
    msg_name = "CCUMCUADChassis1CANFDFr04"
    msg_id = 352
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 32
    tx_node = "CCUMCUAD"
    rx_nodes = ['PSCM1', 'SUM', 'BCU1']
    sig_group_dict = {'Odometer': ['OdometerValidity', 'OdometerValue'], 'FuncStsOfStopLamp': ['FuncStsOfStopLampLightErrorCode', 'FuncStsOfStopLampLightPriority', 'FuncStsOfStopLampLightSts'], 'SteerWhlCntrCtrlReq': ['SteerWhlCntrCtrlReqSteerWhlCntrCtrlAgReq', 'SteerWhlCntrCtrlReqSteerWhlCntrCtrlReq']}
    sig_group_dataid_dict = {}

    class OdometerValue:
        sig_name = "OdometerValue"
        sig_start_bit = 37
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
        startbit = 37
        bmuws_info = [(4, 0b00111111, 0b11000000, 6, 0), (5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111110, 0b00000001, 7, 1)]

    class CbcSet:
        sig_name = "CbcSet"
        sig_start_bit = 127
        update_id_bit = 135
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EnableDisable_Enable': 0, 'EnableDisable_Disable': 1}
        compute_method = None
        length = 1
        startbit = 127
        byte = 15
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class SteerAssiConvReq:
        sig_name = "SteerAssiConvReq"
        sig_start_bit = 18
        update_id_bit = 17
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
        startbit = 18
        byte = 2
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class EscSet:
        sig_name = "EscSet"
        sig_start_bit = 122
        update_id_bit = 130
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EscSet_Normal': 0, 'EscSet_Sprot1': 1, 'EscSet_Off': 2, 'EscSet_OffRoad1': 3, 'EscSet_OffRoad2': 4, 'EscSet_OffRoad3': 5}
        compute_method = None
        length = 3
        startbit = 122
        byte = 15
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class Odometer_UB:
        sig_name = "Odometer_UB"
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

    class VehTiGlb:
        sig_name = "VehTiGlb"
        sig_start_bit = 95
        update_id_bit = 80
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
        startbit = 95
        bmuws_info = [(11, 0b11111111, 0b00000000, 8, 0), (12, 0b11111111, 0b00000000, 8, 0), (13, 0b11111111, 0b00000000, 8, 0), (14, 0b11111111, 0b00000000, 8, 0)]

    class FuncStsOfStopLampLightPriority:
        sig_name = "FuncStsOfStopLampLightPriority"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 255
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ModReqOfLvl:
        sig_name = "ModReqOfLvl"
        sig_start_bit = 31
        update_id_bit = 27
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
        startbit = 31
        byte = 3
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class FuncStsOfStopLampLightSts:
        sig_name = "FuncStsOfStopLampLightSts"
        sig_start_bit = 23
        update_id_bit = None
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
        startbit = 23
        byte = 2
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class SteerAssiLvlReq:
        sig_name = "SteerAssiLvlReq"
        sig_start_bit = 26
        update_id_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SteerAssiLvl_UnknownLevel': 0, 'SteerAssiLvl_Level1': 1, 'SteerAssiLvl_Level2': 2, 'SteerAssiLvl_Level3': 3, 'SteerAssiLvl_Level4': 4, 'SteerAssiLvl_Reserved1': 5, 'SteerAssiLvl_Reserved2': 6, 'SteerAssiLvl_Reserved3': 7}
        compute_method = None
        length = 3
        startbit = 26
        byte = 3
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class FuncStsOfStopLamp_UB:
        sig_name = "FuncStsOfStopLamp_UB"
        sig_start_bit = 19
        update_id_bit = 19
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 19
        byte = 2
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class OdometerValidity:
        sig_name = "OdometerValidity"
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
        sig_value_table = {'Validity_NotValid': 0, 'Validity_Valid': 1}
        compute_method = None
        length = 1
        startbit = 38
        byte = 4
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class DsrSet:
        sig_name = "DsrSet"
        sig_start_bit = 126
        update_id_bit = 134
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EnableDisable_Enable': 0, 'EnableDisable_Disable': 1}
        compute_method = None
        length = 1
        startbit = 126
        byte = 15
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class DtcSet:
        sig_name = "DtcSet"
        sig_start_bit = 125
        update_id_bit = 133
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EnableDisable_Enable': 0, 'EnableDisable_Disable': 1}
        compute_method = None
        length = 1
        startbit = 125
        byte = 15
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class SteerWhlCntrCtrlReq_UB:
        sig_name = "SteerWhlCntrCtrlReq_UB"
        sig_start_bit = 79
        update_id_bit = 79
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 79
        byte = 9
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class EbdSet:
        sig_name = "EbdSet"
        sig_start_bit = 123
        update_id_bit = 131
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EnableDisable_Enable': 0, 'EnableDisable_Disable': 1}
        compute_method = None
        length = 1
        startbit = 123
        byte = 15
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class SteerWhlCntrCtrlReqSteerWhlCntrCtrlAgReq:
        sig_name = "SteerWhlCntrCtrlReqSteerWhlCntrCtrlAgReq"
        sig_start_bit = 63
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 0.000976563
        sig_value_offset = 0
        sig_value_min = -16384
        sig_value_max = 16383
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 63
        bmuws_info = [(7, 0b11111111, 0b00000000, 8, 0), (8, 0b11111110, 0b00000001, 7, 1)]

    class FuncStsOfStopLampLightErrorCode:
        sig_name = "FuncStsOfStopLampLightErrorCode"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LightErrorCode_ChipError': 0, 'LightErrorCode_ShortError': 1, 'LightErrorCode_OpenError': 2, 'LightErrorCode_NoneError': 255}
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DtvSet:
        sig_name = "DtvSet"
        sig_start_bit = 124
        update_id_bit = 132
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EnableDisable_Enable': 0, 'EnableDisable_Disable': 1}
        compute_method = None
        length = 1
        startbit = 124
        byte = 15
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VehBattU:
        sig_name = "VehBattU"
        sig_start_bit = 76
        update_id_bit = 82
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
        startbit = 76
        bmuws_info = [(9, 0b00011111, 0b11100000, 5, 0), (10, 0b11111000, 0b00000111, 5, 3)]

    class SteerWhlCntrCtrlReqSteerWhlCntrCtrlReq:
        sig_name = "SteerWhlCntrCtrlReqSteerWhlCntrCtrlReq"
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
        sig_value_table = {'ReqSts1_NotReqd': 0, 'ReqSts1_Reqd': 1}
        compute_method = None
        length = 1
        startbit = 64
        byte = 8
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class SteerWhlHptcWarnReq:
        sig_name = "SteerWhlHptcWarnReq"
        sig_start_bit = 78
        update_id_bit = 77
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
        startbit = 78
        byte = 9
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6


class BCU1Chassis1CANFDFr04:
    msg_name = "BCU1Chassis1CANFDFr04"
    msg_id = 640
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "BCU1"
    rx_nodes = ['ETC']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class BrkBoostMode:
        sig_name = "BrkBoostMode"
        sig_start_bit = 7
        update_id_bit = 4
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BrkBoostMode_Normal': 0, 'BrkBoostMode_Reduced': 1, 'BrkBoostMode_TotalLost': 2, 'BrkBoostMode_Reserved': 3}
        compute_method = None
        length = 3
        startbit = 7
        byte = 0
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5


class PSCM1Chassis1CANFDFr06:
    msg_name = "PSCM1Chassis1CANFDFr06"
    msg_id = 353
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 8
    tx_node = "PSCM1"
    rx_nodes = ['CCUMCUAD']
    sig_group_dict = {'SteerWhlCntrCtrl': ['SteerWhlCntrCtrlAvlSts', 'SteerWhlCntrCtrlSts']}
    sig_group_dataid_dict = {}

    class SteerWhlCntrCtrlSts:
        sig_name = "SteerWhlCntrCtrlSts"
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
        sig_value_table = {'ActvInActv2_Init': 0, 'ActvInActv2_InActv': 1, 'ActvInActv2_Actv': 2}
        compute_method = None
        length = 2
        startbit = 22
        byte = 2
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class SteerPinionAgMaxVal:
        sig_name = "SteerPinionAgMaxVal"
        sig_start_bit = 7
        update_id_bit = 8
        sig_length = 15
        sig_value_factor = 0.000976563
        sig_value_offset = 0
        sig_value_min = -16384
        sig_value_max = 16383
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111110, 0b00000001, 7, 1)]

    class SteerWhlCntrCtrl_UB:
        sig_name = "SteerWhlCntrCtrl_UB"
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

    class SteerWhlCntrCtrlAvlSts:
        sig_name = "SteerWhlCntrCtrlAvlSts"
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
        sig_value_table = {'AvlSts2_NotAvl': 0, 'AvlSts2_Avl': 1}
        compute_method = None
        length = 1
        startbit = 23
        byte = 2
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7


class CCUMCUADToPSCM1Chassis1CANFDDiagReqFrame:
    msg_name = "CCUMCUADToPSCM1Chassis1CANFDDiagReqFrame"
    msg_id = 1904
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "CCUMCUAD"
    rx_nodes = ['PSCM1']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class CCUMCUADChassis1CANFDFr05:
    msg_name = "CCUMCUADChassis1CANFDFr05"
    msg_id = 528
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.08
    msg_length = 8
    tx_node = "CCUMCUAD"
    rx_nodes = ['SRS']
    sig_group_dict = {'ANPStatus': ['ANPStatusANPFuncStatus', 'ANPStatusChks', 'ANPStatusCntr', 'ANPStatusQf']}
    sig_group_dataid_dict = {}

    class ANPStatusChks:
        sig_name = "ANPStatusChks"
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

    class ANPStatusANPFuncStatus:
        sig_name = "ANPStatusANPFuncStatus"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 20
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ANPFuncStatus_Passive': 0, 'ANPFuncStatus_MPStandby': 1, 'ANPFuncStatus_MDStandby': 2, 'ANPFuncStatus_MPNormal': 3, 'ANPFuncStatus_MDNormal': 4, 'ANPFuncStatus_ACCNormal': 5, 'ANPFuncStatus_MPOverride': 6, 'ANPFuncStatus_MDOverride': 7, 'ANPFuncStatus_MPTakeover': 8, 'ANPFuncStatus_MDTakeover': 9, 'ANPFuncStatus_MPSafeStop': 10, 'ANPFuncStatus_MDSafeStop': 11, 'ANPFuncStatus_Fault': 12, 'ANPFuncStatus_MPTempPassive': 13, 'ANPFuncStatus_MDTempPassive': 14, 'ANPFuncStatus_ACCTakeOver': 15, 'ANPFuncStatus_ACCSafeStop': 16, 'ANPFuncStatus_BACUSafeStop': 17, 'ANPFuncStatus_Reserved1': 18, 'ANPFuncStatus_Reserved2': 19, 'ANPFuncStatus_Reserved3': 20}
        compute_method = None
        length = 8
        startbit = 23
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ANPStatusCntr:
        sig_name = "ANPStatusCntr"
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

    class ANPStatusQf:
        sig_name = "ANPStatusQf"
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
        sig_value_table = {'Qf1_DevOfDataUndefd': 0, 'Qf1_DataTmpUndefdAndEvlnInProgs': 1, 'Qf1_DevOfDataNotWithinRngAllwd': 2, 'Qf1_DataCalcdWithDevDefd': 3}
        compute_method = None
        length = 2
        startbit = 15
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class ANPStatus_UB:
        sig_name = "ANPStatus_UB"
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


class CCUMCUADToAllChassis1CANFDDiagFuncReqFrame:
    msg_name = "CCUMCUADToAllChassis1CANFDDiagFuncReqFrame"
    msg_id = 2047
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CCUMCUAD"
    rx_nodes = ['PSCM1', 'SUM', 'BCU1']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class CCUMCUADChassis1CANFDFr06:
    msg_name = "CCUMCUADChassis1CANFDFr06"
    msg_id = 641
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 48
    tx_node = "CCUMCUAD"
    rx_nodes = ['PSCM1', 'SUM', 'SRS', 'BCU1']
    sig_group_dict = {'Vin': ['VinInfoBytePosn1', 'VinInfoBytePosn10', 'VinInfoBytePosn11', 'VinInfoBytePosn12', 'VinInfoBytePosn13', 'VinInfoBytePosn14', 'VinInfoBytePosn15', 'VinInfoBytePosn16', 'VinInfoBytePosn17', 'VinInfoBytePosn2', 'VinInfoBytePosn3', 'VinInfoBytePosn4', 'VinInfoBytePosn5', 'VinInfoBytePosn6', 'VinInfoBytePosn7', 'VinInfoBytePosn8', 'VinInfoBytePosn9'], 'HeiReqOfRL': ['HeiReqOfRLHeightLevel', 'HeiReqOfRLHeightLevelPriority'], 'DamprFixPerc': ['DamprFixPercDampingFixPerc', 'DamprFixPercDamprFixPriority'], 'HeiReqOfFR': ['HeiReqOfFRHeightLevel', 'HeiReqOfFRHeightLevelPriority'], 'AmbTEstimd': ['AmbTEstimdT', 'AmbTEstimdTQF'], 'SusStfnInhbReq': ['SusStfnInhbReqStfnInhbReq', 'SusStfnInhbReqStfnInhbReqPriority'], 'HeiReqOfFL': ['HeiReqOfFLHeightLevel', 'HeiReqOfFLHeightLevelPriority'], 'HeiReqOfRR': ['HeiReqOfRRHeightLevel', 'HeiReqOfRRHeightLevelPriority'], 'SusConStfnReq': ['SusConStfnReqStfnConReq', 'SusConStfnReqStfnConReqPriority'], 'HeiLvlInhbReq': ['HeiLvlInhbReqLvlInhb', 'HeiLvlInhbReqLvlInhbPriority']}
    sig_group_dataid_dict = {}

    class VinInfoBytePosn16:
        sig_name = "VinInfoBytePosn16"
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

    class Vin_UB:
        sig_name = "Vin_UB"
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

    class SusStfnInhbReqStfnInhbReqPriority:
        sig_name = "SusStfnInhbReqStfnInhbReqPriority"
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

    class VinInfoBytePosn9:
        sig_name = "VinInfoBytePosn9"
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

    class HeiLvlInhbReqLvlInhbPriority:
        sig_name = "HeiLvlInhbReqLvlInhbPriority"
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

    class VinInfoBytePosn8:
        sig_name = "VinInfoBytePosn8"
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

    class HeiReqOfFLHeightLevel:
        sig_name = "HeiReqOfFLHeightLevel"
        sig_start_bit = 55
        update_id_bit = None
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
        startbit = 55
        byte = 6
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class HeiReqOfRRHeightLevelPriority:
        sig_name = "HeiReqOfRRHeightLevelPriority"
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

    class VinInfoBytePosn1:
        sig_name = "VinInfoBytePosn1"
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

    class HeiReqOfRLHeightLevelPriority:
        sig_name = "HeiReqOfRLHeightLevelPriority"
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

    class HeiReqOfRL_UB:
        sig_name = "HeiReqOfRL_UB"
        sig_start_bit = 83
        update_id_bit = 83
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 83
        byte = 10
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class HeiReqOfFRHeightLevel:
        sig_name = "HeiReqOfFRHeightLevel"
        sig_start_bit = 71
        update_id_bit = None
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
        startbit = 71
        byte = 8
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

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

    class SusConStfnReqStfnConReqPriority:
        sig_name = "SusConStfnReqStfnConReqPriority"
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

    class DamprFixPerc_UB:
        sig_name = "DamprFixPerc_UB"
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

    class HeiReqOfFR_UB:
        sig_name = "HeiReqOfFR_UB"
        sig_start_bit = 67
        update_id_bit = 67
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 67
        byte = 8
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VinInfoBytePosn10:
        sig_name = "VinInfoBytePosn10"
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

    class HeiReqOfFRHeightLevelPriority:
        sig_name = "HeiReqOfFRHeightLevelPriority"
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

    class VinInfoBytePosn14:
        sig_name = "VinInfoBytePosn14"
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

    class StandStillReqByAEBR:
        sig_name = "StandStillReqByAEBR"
        sig_start_bit = 66
        update_id_bit = 65
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
        startbit = 66
        byte = 8
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

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

    class VinInfoBytePosn17:
        sig_name = "VinInfoBytePosn17"
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

    class VinInfoBytePosn15:
        sig_name = "VinInfoBytePosn15"
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

    class VinInfoBytePosn6:
        sig_name = "VinInfoBytePosn6"
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

    class VinInfoBytePosn12:
        sig_name = "VinInfoBytePosn12"
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

    class SusStfnInhbReq_UB:
        sig_name = "SusStfnInhbReq_UB"
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

    class VinInfoBytePosn5:
        sig_name = "VinInfoBytePosn5"
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

    class HeiReqOfFL_UB:
        sig_name = "HeiReqOfFL_UB"
        sig_start_bit = 51
        update_id_bit = 51
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 51
        byte = 6
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VinInfoBytePosn3:
        sig_name = "VinInfoBytePosn3"
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

    class VinInfoBytePosn4:
        sig_name = "VinInfoBytePosn4"
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

    class HeiReqOfRR_UB:
        sig_name = "HeiReqOfRR_UB"
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

    class TrlrModSts:
        sig_name = "TrlrModSts"
        sig_start_bit = 82
        update_id_bit = 80
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
        startbit = 82
        byte = 10
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class VinInfoBytePosn13:
        sig_name = "VinInfoBytePosn13"
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

    class EasyEntryEna:
        sig_name = "EasyEntryEna"
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
        sig_value_table = {'EnableDisable2_Disabled': 0, 'EnableDisable2_Enabled': 1}
        compute_method = None
        length = 1
        startbit = 20
        byte = 2
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VinInfoBytePosn11:
        sig_name = "VinInfoBytePosn11"
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

    class HeiReqOfFLHeightLevelPriority:
        sig_name = "HeiReqOfFLHeightLevelPriority"
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

    class HeiLvlInhbReqLvlInhb:
        sig_name = "HeiLvlInhbReqLvlInhb"
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
        sig_value_table = {'LvlInhb_NoInhibit': 0, 'LvlInhb_LevelDownInhibit': 1, 'LvlInhb_LevelUpInhibit': 2, 'LvlInhb_LevelInhibit': 3}
        compute_method = None
        length = 2
        startbit = 39
        byte = 4
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class CargoReq:
        sig_name = "CargoReq"
        sig_start_bit = 22
        update_id_bit = 21
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 22
        byte = 2
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VinInfoBytePosn2:
        sig_name = "VinInfoBytePosn2"
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

    class SusConStfnReqStfnConReq:
        sig_name = "SusConStfnReqStfnConReq"
        sig_start_bit = 119
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
        startbit = 119
        byte = 14
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class EmgHeiStop:
        sig_name = "EmgHeiStop"
        sig_start_bit = 18
        update_id_bit = 17
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
        startbit = 18
        byte = 2
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class HeiReqOfRLHeightLevel:
        sig_name = "HeiReqOfRLHeightLevel"
        sig_start_bit = 87
        update_id_bit = None
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
        startbit = 87
        byte = 10
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class HeiReqOfRRHeightLevel:
        sig_name = "HeiReqOfRRHeightLevel"
        sig_start_bit = 103
        update_id_bit = None
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
        startbit = 103
        byte = 12
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class SusConStfnReq_UB:
        sig_name = "SusConStfnReq_UB"
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

    class HeiLvlInhbReq_UB:
        sig_name = "HeiLvlInhbReq_UB"
        sig_start_bit = 37
        update_id_bit = 37
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 37
        byte = 4
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class JackModReq:
        sig_name = "JackModReq"
        sig_start_bit = 36
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
        startbit = 36
        byte = 4
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class DamprFixPercDampingFixPerc:
        sig_name = "DamprFixPercDampingFixPerc"
        sig_start_bit = 279
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.393
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

    class DynoModSts:
        sig_name = "DynoModSts"
        sig_start_bit = 50
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
        startbit = 50
        byte = 6
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class DamprFixPercDamprFixPriority:
        sig_name = "DamprFixPercDamprFixPriority"
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

    class SusStfnInhbReqStfnInhbReq:
        sig_name = "SusStfnInhbReqStfnInhbReq"
        sig_start_bit = 112
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
        startbit = 112
        byte = 14
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class PassAirbDiReq:
        sig_name = "PassAirbDiReq"
        sig_start_bit = 34
        update_id_bit = 32
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EnableDisable4_NoCmd': 0, 'EnableDisable4_Disable': 1, 'EnableDisable4_Enable': 2}
        compute_method = None
        length = 2
        startbit = 34
        byte = 4
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class VinInfoBytePosn7:
        sig_name = "VinInfoBytePosn7"
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

    class AutLvlInhb:
        sig_name = "AutLvlInhb"
        sig_start_bit = 8
        update_id_bit = 23
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


