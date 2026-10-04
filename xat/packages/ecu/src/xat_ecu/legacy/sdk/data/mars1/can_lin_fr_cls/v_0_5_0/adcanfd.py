class AcuADCANFDFr03:
    msg_name = "AcuADCANFDFr03"
    msg_id = 645
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.07
    msg_length = 32
    tx_node = "ACU"
    rx_nodes = ['BGM']

    class SnsrFltReShoSideLe:
        sig_name = "SnsrFltReShoSideLe"
        sig_start_bit = 116
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

    class PrkgDstCtrlSts:
        sig_name = "PrkgDstCtrlSts"
        sig_start_bit = 95
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

    class FrntRiOfSideDoor:
        sig_name = "FrntRiOfSideDoor"
        sig_start_bit = 39
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoDistance': 0, 'Range1': 1, 'Range2': 2, 'Range3': 3, 'Range4': 4, 'Range5': 5, 'Range6': 6, 'Range7': 7, 'Range8': 8, 'Range9': 9, 'Range10': 10, 'Range11': 11, 'Range12': 12, 'Range13': 13, 'Reserve1': 14, 'Reserve2': 15}
        compute_method = None
        length = 4
        startbit = 39
        byte = 4
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class InsdRiOfSnsrPrkgAssiRe:
        sig_name = "InsdRiOfSnsrPrkgAssiRe"
        sig_start_bit = 51
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoDistance': 0, 'Range1': 1, 'Range2': 2, 'Range3': 3, 'Range4': 4, 'Range5': 5, 'Range6': 6, 'Range7': 7, 'Range8': 8, 'Range9': 9, 'Range10': 10, 'Range11': 11, 'Range12': 12, 'Range13': 13, 'Reserve1': 14, 'Reserve2': 15}
        compute_method = None
        length = 4
        startbit = 51
        byte = 6
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class InsdLeOfSnsrPrkgAssiFrnt:
        sig_name = "InsdLeOfSnsrPrkgAssiFrnt"
        sig_start_bit = 47
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoDistance': 0, 'Range1': 1, 'Range2': 2, 'Range3': 3, 'Range4': 4, 'Range5': 5, 'Range6': 6, 'Range7': 7, 'Range8': 8, 'Range9': 9, 'Range10': 10, 'Range11': 11, 'Range12': 12, 'Range13': 13, 'Reserve1': 14, 'Reserve2': 15}
        compute_method = None
        length = 4
        startbit = 47
        byte = 5
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class AudWarnLvOfSnsrParkAssiRe:
        sig_name = "AudWarnLvOfSnsrParkAssiRe"
        sig_start_bit = 3
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BuzzerOFF': 0, 'BuzzerON_Keep': 1, 'BuzzerON_2Hz': 2, 'BuzzerON_4Hz': 3}
        compute_method = None
        length = 2
        startbit = 3
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class FrntLeOfSideDoor:
        sig_name = "FrntLeOfSideDoor"
        sig_start_bit = 31
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoDistance': 0, 'Range1': 1, 'Range2': 2, 'Range3': 3, 'Range4': 4, 'Range5': 5, 'Range6': 6, 'Range7': 7, 'Range8': 8, 'Range9': 9, 'Range10': 10, 'Range11': 11, 'Range12': 12, 'Range13': 13, 'Reserve1': 14, 'Reserve2': 15}
        compute_method = None
        length = 4
        startbit = 31
        byte = 3
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class AudWarnOfSnsrParkAssiLePosn:
        sig_name = "AudWarnOfSnsrParkAssiLePosn"
        sig_start_bit = 12
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

    class InsdRiOfSnsrPrkgAssiFrnt:
        sig_name = "InsdRiOfSnsrPrkgAssiFrnt"
        sig_start_bit = 55
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoDistance': 0, 'Range1': 1, 'Range2': 2, 'Range3': 3, 'Range4': 4, 'Range5': 5, 'Range6': 6, 'Range7': 7, 'Range8': 8, 'Range9': 9, 'Range10': 10, 'Range11': 11, 'Range12': 12, 'Range13': 13, 'Reserve1': 14, 'Reserve2': 15}
        compute_method = None
        length = 4
        startbit = 55
        byte = 6
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class InsdLeOfSnsrPrkgAssiRe:
        sig_name = "InsdLeOfSnsrPrkgAssiRe"
        sig_start_bit = 43
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoDistance': 0, 'Range1': 1, 'Range2': 2, 'Range3': 3, 'Range4': 4, 'Range5': 5, 'Range6': 6, 'Range7': 7, 'Range8': 8, 'Range9': 9, 'Range10': 10, 'Range11': 11, 'Range12': 12, 'Range13': 13, 'Reserve1': 14, 'Reserve2': 15}
        compute_method = None
        length = 4
        startbit = 43
        byte = 5
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class InsdSnsrFltFrntShoLe:
        sig_name = "InsdSnsrFltFrntShoLe"
        sig_start_bit = 63
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
        sig_start_bit = 91
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoDistance': 0, 'Range1': 1, 'Range2': 2, 'Range3': 3, 'Range4': 4, 'Range5': 5, 'Range6': 6, 'Range7': 7, 'Range8': 8, 'Range9': 9, 'Range10': 10, 'Range11': 11, 'Range12': 12, 'Range13': 13, 'Reserve1': 14, 'Reserve2': 15}
        compute_method = None
        length = 4
        startbit = 91
        byte = 11
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class OutdSnsrFltReShoLe:
        sig_name = "OutdSnsrFltReShoLe"
        sig_start_bit = 83
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

    class InsdSnsrFltReShoLe:
        sig_name = "InsdSnsrFltReShoLe"
        sig_start_bit = 59
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

    class OutdRiOfSnsrPrkgAssiRe:
        sig_name = "OutdRiOfSnsrPrkgAssiRe"
        sig_start_bit = 75
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoDistance': 0, 'Range1': 1, 'Range2': 2, 'Range3': 3, 'Range4': 4, 'Range5': 5, 'Range6': 6, 'Range7': 7, 'Range8': 8, 'Range9': 9, 'Range10': 10, 'Range11': 11, 'Range12': 12, 'Range13': 13, 'Reserve1': 14, 'Reserve2': 15}
        compute_method = None
        length = 4
        startbit = 75
        byte = 9
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class AudWarnLvOfSnsrParkAssiRgt:
        sig_name = "AudWarnLvOfSnsrParkAssiRgt"
        sig_start_bit = 1
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BuzzerOFF': 0, 'BuzzerON_Keep': 1, 'BuzzerON_2Hz': 2, 'BuzzerON_4Hz': 3}
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class SnsrFltFrntShoSideLe:
        sig_name = "SnsrFltFrntShoSideLe"
        sig_start_bit = 107
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
        startbit = 107
        byte = 13
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class OutdRiOfSnsrPrkgAssiFrnt:
        sig_name = "OutdRiOfSnsrPrkgAssiFrnt"
        sig_start_bit = 79
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoDistance': 0, 'Range1': 1, 'Range2': 2, 'Range3': 3, 'Range4': 4, 'Range5': 5, 'Range6': 6, 'Range7': 7, 'Range8': 8, 'Range9': 9, 'Range10': 10, 'Range11': 11, 'Range12': 12, 'Range13': 13, 'Reserve1': 14, 'Reserve2': 15}
        compute_method = None
        length = 4
        startbit = 79
        byte = 9
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class OutdSnsrFltReShoRi:
        sig_name = "OutdSnsrFltReShoRi"
        sig_start_bit = 81
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

    class AudWarnOfSnsrParkAssiFrntPosn:
        sig_name = "AudWarnOfSnsrParkAssiFrntPosn"
        sig_start_bit = 15
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

    class AudWarnLvOfSnsrParkAssiLe:
        sig_name = "AudWarnLvOfSnsrParkAssiLe"
        sig_start_bit = 5
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BuzzerOFF': 0, 'BuzzerON_Keep': 1, 'BuzzerON_2Hz': 2, 'BuzzerON_4Hz': 3}
        compute_method = None
        length = 2
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class AudWarnOfSnsrParkAssiRgtPosn:
        sig_name = "AudWarnOfSnsrParkAssiRgtPosn"
        sig_start_bit = 20
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

    class ReRiOfSideDoor:
        sig_name = "ReRiOfSideDoor"
        sig_start_bit = 99
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoDistance': 0, 'Range1': 1, 'Range2': 2, 'Range3': 3, 'Range4': 4, 'Range5': 5, 'Range6': 6, 'Range7': 7, 'Range8': 8, 'Range9': 9, 'Range10': 10, 'Range11': 11, 'Range12': 12, 'Range13': 13, 'Reserve1': 14, 'Reserve2': 15}
        compute_method = None
        length = 4
        startbit = 99
        byte = 12
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class AudWarnLvOfSnsrParkAssiFrnt:
        sig_name = "AudWarnLvOfSnsrParkAssiFrnt"
        sig_start_bit = 7
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BuzzerOFF': 0, 'BuzzerON_Keep': 1, 'BuzzerON_2Hz': 2, 'BuzzerON_4Hz': 3}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class OutdSnsrFltFrntShoLe:
        sig_name = "OutdSnsrFltFrntShoLe"
        sig_start_bit = 87
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

    class PrkgDstCtrlWarn:
        sig_name = "PrkgDstCtrlWarn"
        sig_start_bit = 9
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

    class ReLeOfSnsrOfPrkgAssiSide:
        sig_name = "ReLeOfSnsrOfPrkgAssiSide"
        sig_start_bit = 103
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoDistance': 0, 'Range1': 1, 'Range2': 2, 'Range3': 3, 'Range4': 4, 'Range5': 5, 'Range6': 6, 'Range7': 7, 'Range8': 8, 'Range9': 9, 'Range10': 10, 'Range11': 11, 'Range12': 12, 'Range13': 13, 'Reserve1': 14, 'Reserve2': 15}
        compute_method = None
        length = 4
        startbit = 103
        byte = 12
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class SnsrFltOfPrkgDstCtrl:
        sig_name = "SnsrFltOfPrkgDstCtrl"
        sig_start_bit = 119
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoFault': 0, 'Front_USS_Fault': 1, 'Rear_USS_Fault': 2, 'Front_and_Rear_USS_Fault': 3, 'Reserve1': 4, 'Reserve2': 5, 'Reserve3': 6, 'Reserve4': 7}
        compute_method = None
        length = 3
        startbit = 119
        byte = 14
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class InsdSnsrFltReShoRi:
        sig_name = "InsdSnsrFltReShoRi"
        sig_start_bit = 57
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

    class OutdSnsrFltFrntShoRi:
        sig_name = "OutdSnsrFltFrntShoRi"
        sig_start_bit = 85
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

    class OutdLeOfSnsrPrkgAssiFrnt:
        sig_name = "OutdLeOfSnsrPrkgAssiFrnt"
        sig_start_bit = 71
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoDistance': 0, 'Range1': 1, 'Range2': 2, 'Range3': 3, 'Range4': 4, 'Range5': 5, 'Range6': 6, 'Range7': 7, 'Range8': 8, 'Range9': 9, 'Range10': 10, 'Range11': 11, 'Range12': 12, 'Range13': 13, 'Reserve1': 14, 'Reserve2': 15}
        compute_method = None
        length = 4
        startbit = 71
        byte = 8
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class SnsrFltFrntShoSideRi:
        sig_name = "SnsrFltFrntShoSideRi"
        sig_start_bit = 105
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
        startbit = 105
        byte = 13
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class ReRiOfSnsrOfPrkgAssiSide:
        sig_name = "ReRiOfSnsrOfPrkgAssiSide"
        sig_start_bit = 111
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoDistance': 0, 'Range1': 1, 'Range2': 2, 'Range3': 3, 'Range4': 4, 'Range5': 5, 'Range6': 6, 'Range7': 7, 'Range8': 8, 'Range9': 9, 'Range10': 10, 'Range11': 11, 'Range12': 12, 'Range13': 13, 'Reserve1': 14, 'Reserve2': 15}
        compute_method = None
        length = 4
        startbit = 111
        byte = 13
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class FrntRiOfSnsrOfPrkgAssiSide:
        sig_name = "FrntRiOfSnsrOfPrkgAssiSide"
        sig_start_bit = 35
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoDistance': 0, 'Range1': 1, 'Range2': 2, 'Range3': 3, 'Range4': 4, 'Range5': 5, 'Range6': 6, 'Range7': 7, 'Range8': 8, 'Range9': 9, 'Range10': 10, 'Range11': 11, 'Range12': 12, 'Range13': 13, 'Reserve1': 14, 'Reserve2': 15}
        compute_method = None
        length = 4
        startbit = 35
        byte = 4
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class FrntLeOfSnsrOfPrkgAssiSide:
        sig_name = "FrntLeOfSnsrOfPrkgAssiSide"
        sig_start_bit = 27
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoDistance': 0, 'Range1': 1, 'Range2': 2, 'Range3': 3, 'Range4': 4, 'Range5': 5, 'Range6': 6, 'Range7': 7, 'Range8': 8, 'Range9': 9, 'Range10': 10, 'Range11': 11, 'Range12': 12, 'Range13': 13, 'Reserve1': 14, 'Reserve2': 15}
        compute_method = None
        length = 4
        startbit = 27
        byte = 3
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class InsdSnsrFltFrntShoRi:
        sig_name = "InsdSnsrFltFrntShoRi"
        sig_start_bit = 61
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

    class AudWarnOfSnsrParkAssiRePosn:
        sig_name = "AudWarnOfSnsrParkAssiRePosn"
        sig_start_bit = 23
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

    class OutdLeOfSnsrPrkgAssiRe:
        sig_name = "OutdLeOfSnsrPrkgAssiRe"
        sig_start_bit = 67
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoDistance': 0, 'Range1': 1, 'Range2': 2, 'Range3': 3, 'Range4': 4, 'Range5': 5, 'Range6': 6, 'Range7': 7, 'Range8': 8, 'Range9': 9, 'Range10': 10, 'Range11': 11, 'Range12': 12, 'Range13': 13, 'Reserve1': 14, 'Reserve2': 15}
        compute_method = None
        length = 4
        startbit = 67
        byte = 8
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class SnsrFltReShoSideRi:
        sig_name = "SnsrFltReShoSideRi"
        sig_start_bit = 114
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


class AcuADCANFDNmFr:
    msg_name = "AcuADCANFDNmFr"
    msg_id = 1282
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "ACU"
    rx_nodes = ['BGM']


class BgmADCANFDFr03:
    msg_name = "BgmADCANFDFr03"
    msg_id = 321
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['ACU']

    class VehTiAndDataDay_0_BgmADCANFDSignalIPdu03:
        sig_name = "VehTiAndDataDay_0_BgmADCANFDSignalIPdu03"
        sig_start_bit = 28
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

    class VehTiAndDataDataValid_0_BgmADCANFDSignalIPdu03:
        sig_name = "VehTiAndDataDataValid_0_BgmADCANFDSignalIPdu03"
        sig_start_bit = 6
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

    class VehTiAndDataHr1_0_BgmADCANFDSignalIPdu03:
        sig_name = "VehTiAndDataHr1_0_BgmADCANFDSignalIPdu03"
        sig_start_bit = 20
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

    class VehTiAndDataMth1_0_BgmADCANFDSignalIPdu03:
        sig_name = "VehTiAndDataMth1_0_BgmADCANFDSignalIPdu03"
        sig_start_bit = 35
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

    class VehTiAndDataMins1_0_BgmADCANFDSignalIPdu03:
        sig_name = "VehTiAndDataMins1_0_BgmADCANFDSignalIPdu03"
        sig_start_bit = 13
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

    class VehTiAndDataYr1_0_BgmADCANFDSignalIPdu03:
        sig_name = "VehTiAndDataYr1_0_BgmADCANFDSignalIPdu03"
        sig_start_bit = 46
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

    class VehTiAndDataSec1_0_BgmADCANFDSignalIPdu03:
        sig_name = "VehTiAndDataSec1_0_BgmADCANFDSignalIPdu03"
        sig_start_bit = 5
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


class AcuADCANFDFr01:
    msg_name = "AcuADCANFDFr01"
    msg_id = 304
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "ACU"
    rx_nodes = ['BGM']

    class WhlSpdCmpFac:
        sig_name = "WhlSpdCmpFac"
        sig_start_bit = 7
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


class BgmADCANFDFr01:
    msg_name = "BgmADCANFDFr01"
    msg_id = 784
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['BGM']

    class HandsOnDetectionChks_1_BgmADCANFDSignalIPdu01:
        sig_name = "HandsOnDetectionChks_1_BgmADCANFDSignalIPdu01"
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

    class HandsOnDetectionErrorStatus_1_BgmADCANFDSignalIPdu01:
        sig_name = "HandsOnDetectionErrorStatus_1_BgmADCANFDSignalIPdu01"
        sig_start_bit = 14
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

    class HandsOnDetectionHandsOnStatus_1_BgmADCANFDSignalIPdu01:
        sig_name = "HandsOnDetectionHandsOnStatus_1_BgmADCANFDSignalIPdu01"
        sig_start_bit = 1
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

    class HandsOnDetectionCntr_1_BgmADCANFDSignalIPdu01:
        sig_name = "HandsOnDetectionCntr_1_BgmADCANFDSignalIPdu01"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = None
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


class BgmADCANFDFr05:
    msg_name = "BgmADCANFDFr05"
    msg_id = 506
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.03
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['ACU']

    class AsySecChStsChks:
        sig_name = "AsySecChStsChks"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
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

    class AsySecChFltStsPNCSysFailr:
        sig_name = "AsySecChFltStsPNCSysFailr"
        sig_start_bit = 10
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

    class AsySecChStsADModActvnCfm:
        sig_name = "AsySecChStsADModActvnCfm"
        sig_start_bit = 35
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Cfmd1_NotCfmd': 0, 'Cfmd1_Cfmd': 1}
        compute_method = None
        length = 1
        startbit = 35
        byte = 4
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class AsySecChFltStsReserved5:
        sig_name = "AsySecChFltStsReserved5"
        sig_start_bit = 21
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
        startbit = 21
        byte = 2
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class AsySecChFltStsReserved3:
        sig_name = "AsySecChFltStsReserved3"
        sig_start_bit = 23
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
        startbit = 23
        byte = 2
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class AsySecChFltStsCntr:
        sig_name = "AsySecChFltStsCntr"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = None
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

    class AsySecChStsADModDeactvnCfm:
        sig_name = "AsySecChStsADModDeactvnCfm"
        sig_start_bit = 34
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Cfmd1_NotCfmd': 0, 'Cfmd1_Cfmd': 1}
        compute_method = None
        length = 1
        startbit = 34
        byte = 4
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class AsySecChFltStsPerceptionSysFailr:
        sig_name = "AsySecChFltStsPerceptionSysFailr"
        sig_start_bit = 11
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

    class AsySecChStsReserved1:
        sig_name = "AsySecChStsReserved1"
        sig_start_bit = 33
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

    class AsySecChStsCntr:
        sig_name = "AsySecChStsCntr"
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

    class AsySecChStsReserved4:
        sig_name = "AsySecChStsReserved4"
        sig_start_bit = 46
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
        startbit = 46
        byte = 5
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class AsySecChFltStsReserved1:
        sig_name = "AsySecChFltStsReserved1"
        sig_start_bit = 9
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
        startbit = 9
        byte = 1
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class AsySecChFltStsChks:
        sig_name = "AsySecChFltStsChks"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
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

    class AsySecChFltStsReserved2:
        sig_name = "AsySecChFltStsReserved2"
        sig_start_bit = 8
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

    class AsySecChFltStsReserved6:
        sig_name = "AsySecChFltStsReserved6"
        sig_start_bit = 20
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
        startbit = 20
        byte = 2
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class AsySecChStsSecCtrlrSts:
        sig_name = "AsySecChStsSecCtrlrSts"
        sig_start_bit = 45
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
        startbit = 45
        byte = 5
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class AsySecChFltStsReserved4:
        sig_name = "AsySecChFltStsReserved4"
        sig_start_bit = 22
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
        startbit = 22
        byte = 2
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class AsySecChStsReserved2:
        sig_name = "AsySecChStsReserved2"
        sig_start_bit = 32
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
        startbit = 32
        byte = 4
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class AsySecChStsReserved3:
        sig_name = "AsySecChStsReserved3"
        sig_start_bit = 47
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


class BgmADCANFDFr04:
    msg_name = "BgmADCANFDFr04"
    msg_id = 848
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.6
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['ACU', 'BGM']

    class CarTiGlb_0_BgmADCANFDSignalIPdu04:
        sig_name = "CarTiGlb_0_BgmADCANFDSignalIPdu04"
        sig_start_bit = 39
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


class BgmADCANFDFr02:
    msg_name = "BgmADCANFDFr02"
    msg_id = 320
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.045
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['ACU']

    class SteerWhlTouchBdCrsResuQf1:
        sig_name = "SteerWhlTouchBdCrsResuQf1"
        sig_start_bit = 23
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
        startbit = 23
        byte = 2
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class SteerWhlTouchBdCnclCntr:
        sig_name = "SteerWhlTouchBdCnclCntr"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = None
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

    class SteerWhlTouchBdCnclQf1:
        sig_name = "SteerWhlTouchBdCnclQf1"
        sig_start_bit = 15
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

    class SteerWhlTouchBdCrsResuSteerWhlTouchBdSts:
        sig_name = "SteerWhlTouchBdCrsResuSteerWhlTouchBdSts"
        sig_start_bit = 21
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SteerWhlTouchBdSts_NotActive': 0, 'SteerWhlTouchBdSts_Touch': 1, 'SteerWhlTouchBdSts_TouchAndPress': 2, 'SteerWhlTouchBdSts_Invalid': 3}
        compute_method = None
        length = 2
        startbit = 21
        byte = 2
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class SteerWhlTouchBdADAS:
        sig_name = "SteerWhlTouchBdADAS"
        sig_start_bit = 19
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SteerWhlTouchBdSts_NotActive': 0, 'SteerWhlTouchBdSts_Touch': 1, 'SteerWhlTouchBdSts_TouchAndPress': 2, 'SteerWhlTouchBdSts_Invalid': 3}
        compute_method = None
        length = 2
        startbit = 19
        byte = 2
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class SteerWhlTouchBdCnclSteerWhlTouchBdSts:
        sig_name = "SteerWhlTouchBdCnclSteerWhlTouchBdSts"
        sig_start_bit = 13
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SteerWhlTouchBdSts_NotActive': 0, 'SteerWhlTouchBdSts_Touch': 1, 'SteerWhlTouchBdSts_TouchAndPress': 2, 'SteerWhlTouchBdSts_Invalid': 3}
        compute_method = None
        length = 2
        startbit = 13
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class BLEConRPACtrlLeft:
        sig_name = "BLEConRPACtrlLeft"
        sig_start_bit = 35
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

    class BLEConRPACtrlRgt:
        sig_name = "BLEConRPACtrlRgt"
        sig_start_bit = 44
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

    class BLEConRPACtrlFrnt:
        sig_name = "BLEConRPACtrlFrnt"
        sig_start_bit = 38
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

    class BLEConRPACtrlRear:
        sig_name = "BLEConRPACtrlRear"
        sig_start_bit = 47
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

    class SteerWhlTouchBdCnclChks:
        sig_name = "SteerWhlTouchBdCnclChks"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
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


class BgmADCANFDNmFr:
    msg_name = "BgmADCANFDNmFr"
    msg_id = 1281
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['ACU']


