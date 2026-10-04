class SODRADRadarCANFD2Fr03:
    msg_name = "SODRADRadarCANFD2Fr03"
    msg_id = 258
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 64
    tx_node = "SODR"
    rx_nodes = ['ADSOCFSI']
    sig_group_dict = {'ReSideRdrRiSts': ['ReSideRdrRiStsChks', 'ReSideRdrRiStsCntr', 'ReSideRdrRiStsRdrStsCalibrationSts', 'ReSideRdrRiStsRdrStsDetnValid', 'ReSideRdrRiStsRdrStsDstbc', 'ReSideRdrRiStsRdrStsEolHoriAg', 'ReSideRdrRiStsRdrStsEolVerAg', 'ReSideRdrRiStsRdrStsFailureHighTemp', 'ReSideRdrRiStsRdrStsFailureNVM', 'ReSideRdrRiStsRdrStsFailureTemperature', 'ReSideRdrRiStsRdrStsFailureVoltage', 'ReSideRdrRiStsRdrStsFaulty', 'ReSideRdrRiStsRdrStsLastTimeLeap', 'ReSideRdrRiStsRdrStsMaxTimeLeap', 'ReSideRdrRiStsRdrStsMissCom', 'ReSideRdrRiStsRdrStsOnlineHoriAg', 'ReSideRdrRiStsRdrStsOnlineVerAg', 'ReSideRdrRiStsRdrStsOperationMode']}
    sig_group_dataid_dict = {'ReSideRdrRiSts': 1021}

    class ReSideRdrRiStsRdrStsOnlineVerAg:
        sig_name = "ReSideRdrRiStsRdrStsOnlineVerAg"
        sig_start_bit = 79
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
        startbit = 79
        bmuws_info = [(9, 0b11111111, 0b00000000, 8, 0), (10, 0b11000000, 0b00111111, 2, 6)]

    class ReSideRdrRiStsCntr:
        sig_name = "ReSideRdrRiStsCntr"
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

    class ReSideRdrRiStsRdrStsFailureNVM:
        sig_name = "ReSideRdrRiStsRdrStsFailureNVM"
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
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 80
        byte = 10
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ReSideRdrRiStsRdrStsEolHoriAg:
        sig_name = "ReSideRdrRiStsRdrStsEolHoriAg"
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

    class ReSideRdrRiStsRdrStsOnlineHoriAg:
        sig_name = "ReSideRdrRiStsRdrStsOnlineHoriAg"
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

    class ReSideRdrRiStsRdrStsFaulty:
        sig_name = "ReSideRdrRiStsRdrStsFaulty"
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

    class ReSideRdrRiStsRdrStsDstbc:
        sig_name = "ReSideRdrRiStsRdrStsDstbc"
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
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 82
        byte = 10
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class ReSideRdrRiSts_UB:
        sig_name = "ReSideRdrRiSts_UB"
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

    class ReSideRdrRiStsRdrStsEolVerAg:
        sig_name = "ReSideRdrRiStsRdrStsEolVerAg"
        sig_start_bit = 57
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
        startbit = 57
        bmuws_info = [(7, 0b00000011, 0b11111100, 2, 0), (8, 0b11111111, 0b00000000, 8, 0)]

    class ReSideRdrRiStsRdrStsMaxTimeLeap:
        sig_name = "ReSideRdrRiStsRdrStsMaxTimeLeap"
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

    class ReSideRdrRiStsRdrStsFailureTemperature:
        sig_name = "ReSideRdrRiStsRdrStsFailureTemperature"
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

    class ReSideRdrRiStsRdrStsFailureVoltage:
        sig_name = "ReSideRdrRiStsRdrStsFailureVoltage"
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

    class ReSideRdrRiStsRdrStsLastTimeLeap:
        sig_name = "ReSideRdrRiStsRdrStsLastTimeLeap"
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

    class ReSideRdrRiStsRdrStsMissCom:
        sig_name = "ReSideRdrRiStsRdrStsMissCom"
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

    class ReSideRdrRiStsChks:
        sig_name = "ReSideRdrRiStsChks"
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

    class ReSideRdrRiStsRdrStsFailureHighTemp:
        sig_name = "ReSideRdrRiStsRdrStsFailureHighTemp"
        sig_start_bit = 81
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
        startbit = 81
        byte = 10
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class ReSideRdrRiStsRdrStsCalibrationSts:
        sig_name = "ReSideRdrRiStsRdrStsCalibrationSts"
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

    class ReSideRdrRiStsRdrStsOperationMode:
        sig_name = "ReSideRdrRiStsRdrStsOperationMode"
        sig_start_bit = 85
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
        startbit = 85
        byte = 10
        mask = 0b00111000
        unmask = 0b11000111
        shift = 3

    class ReSideRdrRiStsRdrStsDetnValid:
        sig_name = "ReSideRdrRiStsRdrStsDetnValid"
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


class SODRADRadarCANFD2Fr01:
    msg_name = "SODRADRadarCANFD2Fr01"
    msg_id = 256
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "SODR"
    rx_nodes = ['ADSOCFSI']
    sig_group_dict = {'ReSideRdrRiDent3': ['ReSideRdrRiDent3RdrDetnChks', 'ReSideRdrRiDent3RdrDetnCntr', 'ReSideRdrRiDent3RdrDetnDynProp', 'ReSideRdrRiDent3RdrDetnElevn', 'ReSideRdrRiDent3RdrDetnID', 'ReSideRdrRiDent3RdrDetnLocationValid', 'ReSideRdrRiDent3RdrDetnPwr', 'ReSideRdrRiDent3RdrDetnRng', 'ReSideRdrRiDent3RdrDetnRngV', 'ReSideRdrRiDent3RdrDetnSNR'], 'ReSideRdrRiDent0': ['ReSideRdrRiDent0RdrDetnChks', 'ReSideRdrRiDent0RdrDetnCntr', 'ReSideRdrRiDent0RdrDetnDynProp', 'ReSideRdrRiDent0RdrDetnElevn', 'ReSideRdrRiDent0RdrDetnID', 'ReSideRdrRiDent0RdrDetnLocationValid', 'ReSideRdrRiDent0RdrDetnPwr', 'ReSideRdrRiDent0RdrDetnRng', 'ReSideRdrRiDent0RdrDetnRngV', 'ReSideRdrRiDent0RdrDetnSNR'], 'ReSideRdrRiDent2': ['ReSideRdrRiDent2RdrDetnChks', 'ReSideRdrRiDent2RdrDetnCntr', 'ReSideRdrRiDent2RdrDetnDynProp', 'ReSideRdrRiDent2RdrDetnElevn', 'ReSideRdrRiDent2RdrDetnID', 'ReSideRdrRiDent2RdrDetnLocationValid', 'ReSideRdrRiDent2RdrDetnPwr', 'ReSideRdrRiDent2RdrDetnRng', 'ReSideRdrRiDent2RdrDetnRngV', 'ReSideRdrRiDent2RdrDetnSNR'], 'ReSideRdrRiDent1': ['ReSideRdrRiDent1RdrDetnChks', 'ReSideRdrRiDent1RdrDetnCntr', 'ReSideRdrRiDent1RdrDetnDynProp', 'ReSideRdrRiDent1RdrDetnElevn', 'ReSideRdrRiDent1RdrDetnID', 'ReSideRdrRiDent1RdrDetnLocationValid', 'ReSideRdrRiDent1RdrDetnPwr', 'ReSideRdrRiDent1RdrDetnRng', 'ReSideRdrRiDent1RdrDetnRngV', 'ReSideRdrRiDent1RdrDetnSNR'], 'ReSideRdrRiDent5': ['ReSideRdrRiDent5RdrDetnChks', 'ReSideRdrRiDent5RdrDetnCntr', 'ReSideRdrRiDent5RdrDetnDynProp', 'ReSideRdrRiDent5RdrDetnElevn', 'ReSideRdrRiDent5RdrDetnID', 'ReSideRdrRiDent5RdrDetnLocationValid', 'ReSideRdrRiDent5RdrDetnPwr', 'ReSideRdrRiDent5RdrDetnRng', 'ReSideRdrRiDent5RdrDetnRngV', 'ReSideRdrRiDent5RdrDetnSNR'], 'ReSideRdrRiDent4': ['ReSideRdrRiDent4RdrDetnChks', 'ReSideRdrRiDent4RdrDetnCntr', 'ReSideRdrRiDent4RdrDetnDynProp', 'ReSideRdrRiDent4RdrDetnElevn', 'ReSideRdrRiDent4RdrDetnID', 'ReSideRdrRiDent4RdrDetnLocationValid', 'ReSideRdrRiDent4RdrDetnPwr', 'ReSideRdrRiDent4RdrDetnRng', 'ReSideRdrRiDent4RdrDetnRngV', 'ReSideRdrRiDent4RdrDetnSNR']}
    sig_group_dataid_dict = {}

    class ReSideRdrRiDent2RdrDetnRng:
        sig_name = "ReSideRdrRiDent2RdrDetnRng"
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

    class ReSideRdrRiDent1RdrDetnCntr:
        sig_name = "ReSideRdrRiDent1RdrDetnCntr"
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

    class ReSideRdrRiDent3_UB:
        sig_name = "ReSideRdrRiDent3_UB"
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

    class ReSideRdrRiDent0RdrDetnSNR:
        sig_name = "ReSideRdrRiDent0RdrDetnSNR"
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

    class ReSideRdrRiDent5RdrDetnChks:
        sig_name = "ReSideRdrRiDent5RdrDetnChks"
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

    class ReSideRdrRiDent5RdrDetnPwr:
        sig_name = "ReSideRdrRiDent5RdrDetnPwr"
        sig_start_bit = 396
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
        startbit = 396
        byte = 49
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class ReSideRdrRiDent3RdrDetnChks:
        sig_name = "ReSideRdrRiDent3RdrDetnChks"
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

    class ReSideRdrRiDent1RdrDetnID:
        sig_name = "ReSideRdrRiDent1RdrDetnID"
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

    class ReSideRdrRiDent0RdrDetnID:
        sig_name = "ReSideRdrRiDent0RdrDetnID"
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

    class ReSideRdrRiDent2RdrDetnPwr:
        sig_name = "ReSideRdrRiDent2RdrDetnPwr"
        sig_start_bit = 188
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
        startbit = 188
        byte = 23
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class ReSideRdrRiDent2RdrDetnLocationValid:
        sig_name = "ReSideRdrRiDent2RdrDetnLocationValid"
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
        sig_value_table = {'Validity2_Valid': 0, 'Validity2_Invalid': 1}
        compute_method = None
        length = 1
        startbit = 207
        byte = 25
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ReSideRdrRiDent1RdrDetnDynProp:
        sig_name = "ReSideRdrRiDent1RdrDetnDynProp"
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

    class ReSideRdrRiDent2RdrDetnChks:
        sig_name = "ReSideRdrRiDent2RdrDetnChks"
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

    class ReSideRdrRiDent3RdrDetnPwr:
        sig_name = "ReSideRdrRiDent3RdrDetnPwr"
        sig_start_bit = 260
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
        startbit = 260
        byte = 32
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class ReSideRdrRiDent1RdrDetnSNR:
        sig_name = "ReSideRdrRiDent1RdrDetnSNR"
        sig_start_bit = 135
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
        startbit = 135
        byte = 16
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class ReSideRdrRiDent4RdrDetnPwr:
        sig_name = "ReSideRdrRiDent4RdrDetnPwr"
        sig_start_bit = 324
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
        startbit = 324
        byte = 40
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class ReSideRdrRiDent0_UB:
        sig_name = "ReSideRdrRiDent0_UB"
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

    class ReSideRdrRiDent2RdrDetnDynProp:
        sig_name = "ReSideRdrRiDent2RdrDetnDynProp"
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

    class ReSideRdrRiDent3RdrDetnID:
        sig_name = "ReSideRdrRiDent3RdrDetnID"
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

    class ReSideRdrRiDent5RdrDetnCntr:
        sig_name = "ReSideRdrRiDent5RdrDetnCntr"
        sig_start_bit = 379
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 379
        byte = 47
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class ReSideRdrRiDent1RdrDetnRngV:
        sig_name = "ReSideRdrRiDent1RdrDetnRngV"
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

    class ReSideRdrRiDent3RdrDetnSNR:
        sig_name = "ReSideRdrRiDent3RdrDetnSNR"
        sig_start_bit = 271
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
        startbit = 271
        byte = 33
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class ReSideRdrRiDent4RdrDetnLocationValid:
        sig_name = "ReSideRdrRiDent4RdrDetnLocationValid"
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
        sig_value_table = {'Validity2_Valid': 0, 'Validity2_Invalid': 1}
        compute_method = None
        length = 1
        startbit = 343
        byte = 42
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ReSideRdrRiDent0RdrDetnRngV:
        sig_name = "ReSideRdrRiDent0RdrDetnRngV"
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

    class ReSideRdrRiDent2_UB:
        sig_name = "ReSideRdrRiDent2_UB"
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

    class ReSideRdrRiDent4RdrDetnChks:
        sig_name = "ReSideRdrRiDent4RdrDetnChks"
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

    class ReSideRdrRiDent5RdrDetnRngV:
        sig_name = "ReSideRdrRiDent5RdrDetnRngV"
        sig_start_bit = 391
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
        startbit = 391
        bmuws_info = [(48, 0b11111111, 0b00000000, 8, 0), (49, 0b11100000, 0b00011111, 3, 5)]

    class ReSideRdrRiDent4RdrDetnDynProp:
        sig_name = "ReSideRdrRiDent4RdrDetnDynProp"
        sig_start_bit = 328
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
        startbit = 328
        byte = 41
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ReSideRdrRiDent3RdrDetnRng:
        sig_name = "ReSideRdrRiDent3RdrDetnRng"
        sig_start_bit = 239
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
        startbit = 239
        bmuws_info = [(29, 0b11111111, 0b00000000, 8, 0), (30, 0b11110000, 0b00001111, 4, 4)]

    class ReSideRdrRiDent3RdrDetnDynProp:
        sig_name = "ReSideRdrRiDent3RdrDetnDynProp"
        sig_start_bit = 264
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
        startbit = 264
        byte = 33
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ReSideRdrRiDent3RdrDetnCntr:
        sig_name = "ReSideRdrRiDent3RdrDetnCntr"
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

    class ReSideRdrRiDent4RdrDetnRng:
        sig_name = "ReSideRdrRiDent4RdrDetnRng"
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

    class ReSideRdrRiDent1RdrDetnChks:
        sig_name = "ReSideRdrRiDent1RdrDetnChks"
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

    class ReSideRdrRiDent0RdrDetnCntr:
        sig_name = "ReSideRdrRiDent0RdrDetnCntr"
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

    class ReSideRdrRiDent2RdrDetnRngV:
        sig_name = "ReSideRdrRiDent2RdrDetnRngV"
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

    class ReSideRdrRiDent4RdrDetnRngV:
        sig_name = "ReSideRdrRiDent4RdrDetnRngV"
        sig_start_bit = 319
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
        startbit = 319
        bmuws_info = [(39, 0b11111111, 0b00000000, 8, 0), (40, 0b11100000, 0b00011111, 3, 5)]

    class ReSideRdrRiDent5RdrDetnRng:
        sig_name = "ReSideRdrRiDent5RdrDetnRng"
        sig_start_bit = 375
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
        startbit = 375
        bmuws_info = [(46, 0b11111111, 0b00000000, 8, 0), (47, 0b11110000, 0b00001111, 4, 4)]

    class ReSideRdrRiDent0RdrDetnDynProp:
        sig_name = "ReSideRdrRiDent0RdrDetnDynProp"
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

    class ReSideRdrRiDent0RdrDetnRng:
        sig_name = "ReSideRdrRiDent0RdrDetnRng"
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

    class ReSideRdrRiDent1RdrDetnRng:
        sig_name = "ReSideRdrRiDent1RdrDetnRng"
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

    class ReSideRdrRiDent3RdrDetnElevn:
        sig_name = "ReSideRdrRiDent3RdrDetnElevn"
        sig_start_bit = 223
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
        startbit = 223
        byte = 27
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ReSideRdrRiDent4RdrDetnCntr:
        sig_name = "ReSideRdrRiDent4RdrDetnCntr"
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

    class ReSideRdrRiDent1_UB:
        sig_name = "ReSideRdrRiDent1_UB"
        sig_start_bit = 70
        update_id_bit = 70
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 70
        byte = 8
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class ReSideRdrRiDent4RdrDetnSNR:
        sig_name = "ReSideRdrRiDent4RdrDetnSNR"
        sig_start_bit = 335
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
        startbit = 335
        byte = 41
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class ReSideRdrRiDent4RdrDetnElevn:
        sig_name = "ReSideRdrRiDent4RdrDetnElevn"
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

    class ReSideRdrRiDent1RdrDetnLocationValid:
        sig_name = "ReSideRdrRiDent1RdrDetnLocationValid"
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
        sig_value_table = {'Validity2_Valid': 0, 'Validity2_Invalid': 1}
        compute_method = None
        length = 1
        startbit = 64
        byte = 8
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ReSideRdrRiDent5RdrDetnSNR:
        sig_name = "ReSideRdrRiDent5RdrDetnSNR"
        sig_start_bit = 407
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
        startbit = 407
        byte = 50
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class ReSideRdrRiDent5RdrDetnDynProp:
        sig_name = "ReSideRdrRiDent5RdrDetnDynProp"
        sig_start_bit = 400
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
        startbit = 400
        byte = 50
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ReSideRdrRiDent5_UB:
        sig_name = "ReSideRdrRiDent5_UB"
        sig_start_bit = 341
        update_id_bit = 341
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 341
        byte = 42
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class ReSideRdrRiDent2RdrDetnSNR:
        sig_name = "ReSideRdrRiDent2RdrDetnSNR"
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

    class ReSideRdrRiDent5RdrDetnElevn:
        sig_name = "ReSideRdrRiDent5RdrDetnElevn"
        sig_start_bit = 359
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
        startbit = 359
        byte = 44
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ReSideRdrRiDent3RdrDetnLocationValid:
        sig_name = "ReSideRdrRiDent3RdrDetnLocationValid"
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
        sig_value_table = {'Validity2_Valid': 0, 'Validity2_Invalid': 1}
        compute_method = None
        length = 1
        startbit = 200
        byte = 25
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ReSideRdrRiDent5RdrDetnLocationValid:
        sig_name = "ReSideRdrRiDent5RdrDetnLocationValid"
        sig_start_bit = 336
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
        startbit = 336
        byte = 42
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ReSideRdrRiDent2RdrDetnID:
        sig_name = "ReSideRdrRiDent2RdrDetnID"
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

    class ReSideRdrRiDent0RdrDetnLocationValid:
        sig_name = "ReSideRdrRiDent0RdrDetnLocationValid"
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

    class ReSideRdrRiDent0RdrDetnElevn:
        sig_name = "ReSideRdrRiDent0RdrDetnElevn"
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

    class ReSideRdrRiDent2RdrDetnCntr:
        sig_name = "ReSideRdrRiDent2RdrDetnCntr"
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

    class ReSideRdrRiDent4_UB:
        sig_name = "ReSideRdrRiDent4_UB"
        sig_start_bit = 342
        update_id_bit = 342
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 342
        byte = 42
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class ReSideRdrRiDent2RdrDetnElevn:
        sig_name = "ReSideRdrRiDent2RdrDetnElevn"
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

    class ReSideRdrRiDent5RdrDetnID:
        sig_name = "ReSideRdrRiDent5RdrDetnID"
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

    class ReSideRdrRiDent4RdrDetnID:
        sig_name = "ReSideRdrRiDent4RdrDetnID"
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

    class ReSideRdrRiDent0RdrDetnPwr:
        sig_name = "ReSideRdrRiDent0RdrDetnPwr"
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

    class ReSideRdrRiDent1RdrDetnPwr:
        sig_name = "ReSideRdrRiDent1RdrDetnPwr"
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

    class ReSideRdrRiDent3RdrDetnRngV:
        sig_name = "ReSideRdrRiDent3RdrDetnRngV"
        sig_start_bit = 255
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
        startbit = 255
        bmuws_info = [(31, 0b11111111, 0b00000000, 8, 0), (32, 0b11100000, 0b00011111, 3, 5)]

    class ReSideRdrRiDent0RdrDetnChks:
        sig_name = "ReSideRdrRiDent0RdrDetnChks"
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

    class ReSideRdrRiDent1RdrDetnElevn:
        sig_name = "ReSideRdrRiDent1RdrDetnElevn"
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


class SODRADRadarCANFD2Fr02:
    msg_name = "SODRADRadarCANFD2Fr02"
    msg_id = 257
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "SODR"
    rx_nodes = ['ADSOCFSI']
    sig_group_dict = {'ReSideRdrRiDent9': ['ReSideRdrRiDent9RdrDetnChks', 'ReSideRdrRiDent9RdrDetnCntr', 'ReSideRdrRiDent9RdrDetnDynProp', 'ReSideRdrRiDent9RdrDetnElevn', 'ReSideRdrRiDent9RdrDetnID', 'ReSideRdrRiDent9RdrDetnLocationValid', 'ReSideRdrRiDent9RdrDetnPwr', 'ReSideRdrRiDent9RdrDetnRng', 'ReSideRdrRiDent9RdrDetnRngV', 'ReSideRdrRiDent9RdrDetnSNR'], 'ReSideRdrRiDent8': ['ReSideRdrRiDent8RdrDetnChks', 'ReSideRdrRiDent8RdrDetnCntr', 'ReSideRdrRiDent8RdrDetnDynProp', 'ReSideRdrRiDent8RdrDetnElevn', 'ReSideRdrRiDent8RdrDetnID', 'ReSideRdrRiDent8RdrDetnLocationValid', 'ReSideRdrRiDent8RdrDetnPwr', 'ReSideRdrRiDent8RdrDetnRng', 'ReSideRdrRiDent8RdrDetnRngV', 'ReSideRdrRiDent8RdrDetnSNR'], 'ReSideRdrRiDent6': ['ReSideRdrRiDent6RdrDetnChks', 'ReSideRdrRiDent6RdrDetnCntr', 'ReSideRdrRiDent6RdrDetnDynProp', 'ReSideRdrRiDent6RdrDetnElevn', 'ReSideRdrRiDent6RdrDetnID', 'ReSideRdrRiDent6RdrDetnLocationValid', 'ReSideRdrRiDent6RdrDetnPwr', 'ReSideRdrRiDent6RdrDetnRng', 'ReSideRdrRiDent6RdrDetnRngV', 'ReSideRdrRiDent6RdrDetnSNR'], 'ReSideRdrRiDent10': ['ReSideRdrRiDent10RdrDetnChks', 'ReSideRdrRiDent10RdrDetnCntr', 'ReSideRdrRiDent10RdrDetnDynProp', 'ReSideRdrRiDent10RdrDetnElevn', 'ReSideRdrRiDent10RdrDetnID', 'ReSideRdrRiDent10RdrDetnLocationValid', 'ReSideRdrRiDent10RdrDetnPwr', 'ReSideRdrRiDent10RdrDetnRng', 'ReSideRdrRiDent10RdrDetnRngV', 'ReSideRdrRiDent10RdrDetnSNR'], 'ReSideRdrRiDent7': ['ReSideRdrRiDent7RdrDetnChks', 'ReSideRdrRiDent7RdrDetnCntr', 'ReSideRdrRiDent7RdrDetnDynProp', 'ReSideRdrRiDent7RdrDetnElevn', 'ReSideRdrRiDent7RdrDetnID', 'ReSideRdrRiDent7RdrDetnLocationValid', 'ReSideRdrRiDent7RdrDetnPwr', 'ReSideRdrRiDent7RdrDetnRng', 'ReSideRdrRiDent7RdrDetnRngV', 'ReSideRdrRiDent7RdrDetnSNR']}
    sig_group_dataid_dict = {}

    class ReSideRdrRiDent8RdrDetnRng:
        sig_name = "ReSideRdrRiDent8RdrDetnRng"
        sig_start_bit = 239
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
        startbit = 239
        bmuws_info = [(29, 0b11111111, 0b00000000, 8, 0), (30, 0b11110000, 0b00001111, 4, 4)]

    class ReSideRdrRiDent6RdrDetnCntr:
        sig_name = "ReSideRdrRiDent6RdrDetnCntr"
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

    class ReSideRdrRiDent7RdrDetnPwr:
        sig_name = "ReSideRdrRiDent7RdrDetnPwr"
        sig_start_bit = 196
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
        startbit = 196
        byte = 24
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class ReSideRdrRiDent7RdrDetnCntr:
        sig_name = "ReSideRdrRiDent7RdrDetnCntr"
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

    class ReSideRdrRiDent9RdrDetnDynProp:
        sig_name = "ReSideRdrRiDent9RdrDetnDynProp"
        sig_start_bit = 336
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
        startbit = 336
        byte = 42
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ReSideRdrRiDent7RdrDetnSNR:
        sig_name = "ReSideRdrRiDent7RdrDetnSNR"
        sig_start_bit = 207
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
        startbit = 207
        byte = 25
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class ReSideRdrRiDent9_UB:
        sig_name = "ReSideRdrRiDent9_UB"
        sig_start_bit = 350
        update_id_bit = 350
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 350
        byte = 43
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class ReSideRdrRiDent9RdrDetnElevn:
        sig_name = "ReSideRdrRiDent9RdrDetnElevn"
        sig_start_bit = 295
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
        startbit = 295
        byte = 36
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ReSideRdrRiDent7RdrDetnRngV:
        sig_name = "ReSideRdrRiDent7RdrDetnRngV"
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

    class ReSideRdrRiDent7RdrDetnChks:
        sig_name = "ReSideRdrRiDent7RdrDetnChks"
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

    class ReSideRdrRiDent10RdrDetnRngV:
        sig_name = "ReSideRdrRiDent10RdrDetnRngV"
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

    class ReSideRdrRiDent10RdrDetnLocationValid:
        sig_name = "ReSideRdrRiDent10RdrDetnLocationValid"
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

    class ReSideRdrRiDent10RdrDetnRng:
        sig_name = "ReSideRdrRiDent10RdrDetnRng"
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

    class ReSideRdrRiDent10RdrDetnCntr:
        sig_name = "ReSideRdrRiDent10RdrDetnCntr"
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

    class ReSideRdrRiDent8RdrDetnRngV:
        sig_name = "ReSideRdrRiDent8RdrDetnRngV"
        sig_start_bit = 255
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
        startbit = 255
        bmuws_info = [(31, 0b11111111, 0b00000000, 8, 0), (32, 0b11100000, 0b00011111, 3, 5)]

    class ReSideRdrRiDent8RdrDetnID:
        sig_name = "ReSideRdrRiDent8RdrDetnID"
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

    class ReSideRdrRiDent9RdrDetnLocationValid:
        sig_name = "ReSideRdrRiDent9RdrDetnLocationValid"
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
        sig_value_table = {'Validity2_Valid': 0, 'Validity2_Invalid': 1}
        compute_method = None
        length = 1
        startbit = 272
        byte = 34
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ReSideRdrRiDent9RdrDetnCntr:
        sig_name = "ReSideRdrRiDent9RdrDetnCntr"
        sig_start_bit = 315
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 315
        byte = 39
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class ReSideRdrRiDent9RdrDetnID:
        sig_name = "ReSideRdrRiDent9RdrDetnID"
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

    class ReSideRdrRiDent10RdrDetnDynProp:
        sig_name = "ReSideRdrRiDent10RdrDetnDynProp"
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

    class ReSideRdrRiDent9RdrDetnSNR:
        sig_name = "ReSideRdrRiDent9RdrDetnSNR"
        sig_start_bit = 343
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
        startbit = 343
        byte = 42
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class ReSideRdrRiDent6RdrDetnElevn:
        sig_name = "ReSideRdrRiDent6RdrDetnElevn"
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

    class ReSideRdrRiDent9RdrDetnPwr:
        sig_name = "ReSideRdrRiDent9RdrDetnPwr"
        sig_start_bit = 332
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
        startbit = 332
        byte = 41
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class ReSideRdrRiDent10RdrDetnElevn:
        sig_name = "ReSideRdrRiDent10RdrDetnElevn"
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

    class ReSideRdrRiDent10RdrDetnPwr:
        sig_name = "ReSideRdrRiDent10RdrDetnPwr"
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

    class ReSideRdrRiDent7RdrDetnLocationValid:
        sig_name = "ReSideRdrRiDent7RdrDetnLocationValid"
        sig_start_bit = 136
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
        startbit = 136
        byte = 17
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ReSideRdrRiDent6RdrDetnRng:
        sig_name = "ReSideRdrRiDent6RdrDetnRng"
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

    class ReSideRdrRiDent6RdrDetnChks:
        sig_name = "ReSideRdrRiDent6RdrDetnChks"
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

    class ReSideRdrRiDent10RdrDetnChks:
        sig_name = "ReSideRdrRiDent10RdrDetnChks"
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

    class ReSideRdrRiDent10RdrDetnID:
        sig_name = "ReSideRdrRiDent10RdrDetnID"
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

    class ReSideRdrRiDent8RdrDetnLocationValid:
        sig_name = "ReSideRdrRiDent8RdrDetnLocationValid"
        sig_start_bit = 279
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
        startbit = 279
        byte = 34
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ReSideRdrRiDent7RdrDetnRng:
        sig_name = "ReSideRdrRiDent7RdrDetnRng"
        sig_start_bit = 175
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
        startbit = 175
        bmuws_info = [(21, 0b11111111, 0b00000000, 8, 0), (22, 0b11110000, 0b00001111, 4, 4)]

    class ReSideRdrRiDent8RdrDetnCntr:
        sig_name = "ReSideRdrRiDent8RdrDetnCntr"
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

    class ReSideRdrRiDent8_UB:
        sig_name = "ReSideRdrRiDent8_UB"
        sig_start_bit = 351
        update_id_bit = 351
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 351
        byte = 43
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ReSideRdrRiDent6_UB:
        sig_name = "ReSideRdrRiDent6_UB"
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

    class ReSideRdrRiDent6RdrDetnRngV:
        sig_name = "ReSideRdrRiDent6RdrDetnRngV"
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

    class ReSideRdrRiDent7RdrDetnDynProp:
        sig_name = "ReSideRdrRiDent7RdrDetnDynProp"
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
        sig_value_table = {'RdrDetnDynProp_Stationary': 0, 'RdrDetnDynProp_Moving': 1}
        compute_method = None
        length = 1
        startbit = 200
        byte = 25
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ReSideRdrRiDent8RdrDetnSNR:
        sig_name = "ReSideRdrRiDent8RdrDetnSNR"
        sig_start_bit = 271
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
        startbit = 271
        byte = 33
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class ReSideRdrRiDent10_UB:
        sig_name = "ReSideRdrRiDent10_UB"
        sig_start_bit = 70
        update_id_bit = 70
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 70
        byte = 8
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class ReSideRdrRiDent7RdrDetnID:
        sig_name = "ReSideRdrRiDent7RdrDetnID"
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

    class ReSideRdrRiDent7RdrDetnElevn:
        sig_name = "ReSideRdrRiDent7RdrDetnElevn"
        sig_start_bit = 159
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
        startbit = 159
        byte = 19
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ReSideRdrRiDent7_UB:
        sig_name = "ReSideRdrRiDent7_UB"
        sig_start_bit = 137
        update_id_bit = 137
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 137
        byte = 17
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class ReSideRdrRiDent9RdrDetnRng:
        sig_name = "ReSideRdrRiDent9RdrDetnRng"
        sig_start_bit = 311
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
        startbit = 311
        bmuws_info = [(38, 0b11111111, 0b00000000, 8, 0), (39, 0b11110000, 0b00001111, 4, 4)]

    class ReSideRdrRiDent8RdrDetnElevn:
        sig_name = "ReSideRdrRiDent8RdrDetnElevn"
        sig_start_bit = 223
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
        startbit = 223
        byte = 27
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ReSideRdrRiDent8RdrDetnDynProp:
        sig_name = "ReSideRdrRiDent8RdrDetnDynProp"
        sig_start_bit = 264
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
        startbit = 264
        byte = 33
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ReSideRdrRiDent8RdrDetnPwr:
        sig_name = "ReSideRdrRiDent8RdrDetnPwr"
        sig_start_bit = 260
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
        startbit = 260
        byte = 32
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class ReSideRdrRiDent10RdrDetnSNR:
        sig_name = "ReSideRdrRiDent10RdrDetnSNR"
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

    class ReSideRdrRiDent6RdrDetnPwr:
        sig_name = "ReSideRdrRiDent6RdrDetnPwr"
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

    class ReSideRdrRiDent8RdrDetnChks:
        sig_name = "ReSideRdrRiDent8RdrDetnChks"
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

    class ReSideRdrRiDent6RdrDetnLocationValid:
        sig_name = "ReSideRdrRiDent6RdrDetnLocationValid"
        sig_start_bit = 143
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
        startbit = 143
        byte = 17
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ReSideRdrRiDent6RdrDetnSNR:
        sig_name = "ReSideRdrRiDent6RdrDetnSNR"
        sig_start_bit = 135
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
        startbit = 135
        byte = 16
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class ReSideRdrRiDent9RdrDetnChks:
        sig_name = "ReSideRdrRiDent9RdrDetnChks"
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

    class ReSideRdrRiDent6RdrDetnDynProp:
        sig_name = "ReSideRdrRiDent6RdrDetnDynProp"
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

    class ReSideRdrRiDent6RdrDetnID:
        sig_name = "ReSideRdrRiDent6RdrDetnID"
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

    class ReSideRdrRiDent9RdrDetnRngV:
        sig_name = "ReSideRdrRiDent9RdrDetnRngV"
        sig_start_bit = 327
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
        startbit = 327
        bmuws_info = [(40, 0b11111111, 0b00000000, 8, 0), (41, 0b11100000, 0b00011111, 3, 5)]


class ADSOCFSIADRadarCANFD2NmFr:
    msg_name = "ADSOCFSIADRadarCANFD2NmFr"
    msg_id = 1281
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "ADSOCFSI"
    rx_nodes = ['SODR']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class SODRADRadarCANFD2NmFr:
    msg_name = "SODRADRadarCANFD2NmFr"
    msg_id = 1284
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "SODR"
    rx_nodes = ['ADSOCFSI']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class ADSOCFSIADRadarCANFD2TimeSynchFr01:
    msg_name = "ADSOCFSIADRadarCANFD2TimeSynchFr01"
    msg_id = 1
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "ADSOCFSI"
    rx_nodes = ['SODR']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


