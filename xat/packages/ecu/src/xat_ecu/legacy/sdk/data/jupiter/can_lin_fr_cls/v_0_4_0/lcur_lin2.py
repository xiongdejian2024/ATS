lin_scheduleTable = {'LCUR_LIN2Schedule01_LCUR_LIN2': [(0, 'BEXVLCUR_LIN2Fr03', 0.015), (1, 'CERVLCUR_LIN2Fr03', 0.015), (2, 'FEXVLCUR_LIN2Fr03', 0.015), (3, 'LCURLCUR_LIN2Fr01', 0.015), (4, 'LCURLCUR_LIN2Fr02', 0.015), (5, 'REXVLCUR_LIN2Fr03', 0.015), (6, 'TERVLCUR_LIN2Fr03', 0.015), (7, 'WERVLCUR_LIN2Fr03', 0.015)], 'LCUR_LIN2_DiagSchedule01': [(0, 'DiagRequest3', 0.015), (1, 'DiagResponse3', 0.015)], 'LCUR_LIN2ScheduleSerlNrPartNr_LCUR_LIN2': [(0, 'BEXVLCUR_LIN2Fr01', 0.015), (1, 'BEXVLCUR_LIN2Fr02', 0.015), (2, 'CERVLCUR_LIN2Fr01', 0.015), (3, 'CERVLCUR_LIN2Fr02', 0.015), (4, 'FEXVLCUR_LIN2Fr01', 0.015), (5, 'FEXVLCUR_LIN2Fr02', 0.015), (6, 'REXVLCUR_LIN2Fr01', 0.015), (7, 'REXVLCUR_LIN2Fr02', 0.015), (8, 'TERVLCUR_LIN2Fr01', 0.015), (9, 'TERVLCUR_LIN2Fr02', 0.015), (10, 'WERVLCUR_LIN2Fr01', 0.015), (11, 'WERVLCUR_LIN2Fr02', 0.015)]}


class FEXVLCUR_LIN2Fr03:
    msg_name = "FEXVLCUR_LIN2Fr03"
    msg_id = 8
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "FEXV"
    rx_nodes = ['LCUR']
    sig_group_dict = {'EEXVSts': ['EEXVStsExvBlkErr', 'EEXVStsExvCalSts', 'EEXVStsExvElecErr', 'EEXVStsExvMoveSts', 'EEXVStsExvOvrTempErr', 'EEXVStsExvOvrTrvlErr', 'EEXVStsExvPosnAct', 'EEXVStsExvURangErr', 'EEXVStsPreHeatgSts']}
    sig_group_dataid_dict = {}

    class EEXVStsExvOvrTempErr:
        sig_name = "EEXVStsExvOvrTempErr"
        sig_start_bit = 10
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err_Initial': 0, 'Err_NoError': 1, 'Err_Error': 2, 'Err_Reserve': 3}
        compute_method = None
        length = 2
        startbit = 10
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class EEXVStsExvElecErr:
        sig_name = "EEXVStsExvElecErr"
        sig_start_bit = 4
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvElecStsErr_NoError': 0, 'ExvElecStsErr_OpenCircuit': 1, 'ExvElecStsErr_ShortCircuit': 2, 'ExvElecStsErr_OverTemperatureShutdown': 3, 'ExvElecStsErr_IndeterminateElectricFault': 4, 'ExvElecStsErr_Reserved': 5}
        compute_method = None
        length = 3
        startbit = 4
        byte = 0
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class EEXVStsExvPosnAct:
        sig_name = "EEXVStsExvPosnAct"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 16
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b00000011, 0b11111100, 2, 0)]

    class EEXVStsExvOvrTrvlErr:
        sig_name = "EEXVStsExvOvrTrvlErr"
        sig_start_bit = 12
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err_Initial': 0, 'Err_NoError': 1, 'Err_Error': 2, 'Err_Reserve': 3}
        compute_method = None
        length = 2
        startbit = 12
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class EEXVStsExvCalSts:
        sig_name = "EEXVStsExvCalSts"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvCalibSts_NotInitialized': 0, 'ExvCalibSts_InitializationInProcess': 1, 'ExvCalibSts_Initialized': 2, 'ExvCalibSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 8
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class EEXVStsExvMoveSts:
        sig_name = "EEXVStsExvMoveSts"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvMovSts_NotMove': 0, 'ExvMovSts_Moving': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class EEXVStsExvURangErr:
        sig_name = "EEXVStsExvURangErr"
        sig_start_bit = 14
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvVoltgRangErr_NoErr': 0, 'ExvVoltgRangErr_UnderVoltageErr': 1, 'ExvVoltgRangErr_OverVoltageErr': 2, 'ExvVoltgRangErr_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 14
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class EEXVStsExvBlkErr:
        sig_name = "EEXVStsExvBlkErr"
        sig_start_bit = 2
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err_Initial': 0, 'Err_NoError': 1, 'Err_Error': 2, 'Err_Reserve': 3}
        compute_method = None
        length = 2
        startbit = 2
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class EEXVNVMFlt:
        sig_name = "EEXVNVMFlt"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flt_Initial': 0, 'Flt_NoFault': 1, 'Flt_Fault': 2}
        compute_method = None
        length = 2
        startbit = 0
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class EEXVStsPreHeatgSts:
        sig_name = "EEXVStsPreHeatgSts"
        sig_start_bit = 26
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 26
        byte = 3
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2


class REXVLCUR_LIN2Fr03:
    msg_name = "REXVLCUR_LIN2Fr03"
    msg_id = 13
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "REXV"
    rx_nodes = ['LCUR']
    sig_group_dict = {'REXVSts': ['REXVStsExvBlkErr', 'REXVStsExvCalSts', 'REXVStsExvElecErr', 'REXVStsExvMoveSts', 'REXVStsExvOvrTempErr', 'REXVStsExvOvrTrvlErr', 'REXVStsExvPosnAct', 'REXVStsExvURangErr', 'REXVStsPreHeatgSts']}
    sig_group_dataid_dict = {}

    class REXVStsExvElecErr:
        sig_name = "REXVStsExvElecErr"
        sig_start_bit = 4
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvElecStsErr_NoError': 0, 'ExvElecStsErr_OpenCircuit': 1, 'ExvElecStsErr_ShortCircuit': 2, 'ExvElecStsErr_OverTemperatureShutdown': 3, 'ExvElecStsErr_IndeterminateElectricFault': 4, 'ExvElecStsErr_Reserved': 5}
        compute_method = None
        length = 3
        startbit = 4
        byte = 0
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class REXVStsExvCalSts:
        sig_name = "REXVStsExvCalSts"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvCalibSts_NotInitialized': 0, 'ExvCalibSts_InitializationInProcess': 1, 'ExvCalibSts_Initialized': 2, 'ExvCalibSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 8
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class REXVStsExvOvrTempErr:
        sig_name = "REXVStsExvOvrTempErr"
        sig_start_bit = 10
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err_Initial': 0, 'Err_NoError': 1, 'Err_Error': 2, 'Err_Reserve': 3}
        compute_method = None
        length = 2
        startbit = 10
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class REXVNVMFlt:
        sig_name = "REXVNVMFlt"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flt_Initial': 0, 'Flt_NoFault': 1, 'Flt_Fault': 2}
        compute_method = None
        length = 2
        startbit = 0
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class REXVStsExvBlkErr:
        sig_name = "REXVStsExvBlkErr"
        sig_start_bit = 2
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err_Initial': 0, 'Err_NoError': 1, 'Err_Error': 2, 'Err_Reserve': 3}
        compute_method = None
        length = 2
        startbit = 2
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class REXVStsPreHeatgSts:
        sig_name = "REXVStsPreHeatgSts"
        sig_start_bit = 26
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 26
        byte = 3
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class REXVStsExvOvrTrvlErr:
        sig_name = "REXVStsExvOvrTrvlErr"
        sig_start_bit = 12
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err_Initial': 0, 'Err_NoError': 1, 'Err_Error': 2, 'Err_Reserve': 3}
        compute_method = None
        length = 2
        startbit = 12
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class REXVStsExvMoveSts:
        sig_name = "REXVStsExvMoveSts"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvMovSts_NotMove': 0, 'ExvMovSts_Moving': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class REXVStsExvURangErr:
        sig_name = "REXVStsExvURangErr"
        sig_start_bit = 14
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvVoltgRangErr_NoErr': 0, 'ExvVoltgRangErr_UnderVoltageErr': 1, 'ExvVoltgRangErr_OverVoltageErr': 2, 'ExvVoltgRangErr_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 14
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class REXVStsExvPosnAct:
        sig_name = "REXVStsExvPosnAct"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 16
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b00000011, 0b11111100, 2, 0)]


class REXVLCUR_LIN2Fr01:
    msg_name = "REXVLCUR_LIN2Fr01"
    msg_id = 11
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "REXV"
    rx_nodes = ['LCUR']
    sig_group_dict = {'REXVPartNo': ['REXVPartNoEndSgn1', 'REXVPartNoEndSgn2', 'REXVPartNoEndSgn3', 'REXVPartNoNr1', 'REXVPartNoNr2', 'REXVPartNoNr3', 'REXVPartNoNr4', 'REXVPartNoNr5']}
    sig_group_dataid_dict = {}

    class REXVPartNoEndSgn2:
        sig_name = "REXVPartNoEndSgn2"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 8
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class REXVPartNoNr2:
        sig_name = "REXVPartNoNr2"
        sig_start_bit = 32
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 32
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class REXVPartNoNr4:
        sig_name = "REXVPartNoNr4"
        sig_start_bit = 48
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 48
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class REXVPartNoEndSgn1:
        sig_name = "REXVPartNoEndSgn1"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class REXVPartNoNr5:
        sig_name = "REXVPartNoNr5"
        sig_start_bit = 56
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 56
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class REXVPartNoNr3:
        sig_name = "REXVPartNoNr3"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 40
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class REXVPartNoEndSgn3:
        sig_name = "REXVPartNoEndSgn3"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class REXVPartNoNr1:
        sig_name = "REXVPartNoNr1"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class WERVLCUR_LIN2Fr01:
    msg_name = "WERVLCUR_LIN2Fr01"
    msg_id = 17
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "WERV"
    rx_nodes = ['LCUR']
    sig_group_dict = {'WERVPartNo': ['WERVPartNoEndSgn1', 'WERVPartNoEndSgn2', 'WERVPartNoEndSgn3', 'WERVPartNoNr1', 'WERVPartNoNr2', 'WERVPartNoNr3', 'WERVPartNoNr4', 'WERVPartNoNr5']}
    sig_group_dataid_dict = {}

    class WERVPartNoEndSgn1:
        sig_name = "WERVPartNoEndSgn1"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class WERVPartNoNr5:
        sig_name = "WERVPartNoNr5"
        sig_start_bit = 56
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 56
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class WERVPartNoNr1:
        sig_name = "WERVPartNoNr1"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class WERVPartNoNr2:
        sig_name = "WERVPartNoNr2"
        sig_start_bit = 32
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 32
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class WERVPartNoEndSgn3:
        sig_name = "WERVPartNoEndSgn3"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class WERVPartNoEndSgn2:
        sig_name = "WERVPartNoEndSgn2"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 8
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class WERVPartNoNr3:
        sig_name = "WERVPartNoNr3"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 40
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class WERVPartNoNr4:
        sig_name = "WERVPartNoNr4"
        sig_start_bit = 48
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 48
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class REXVLCUR_LIN2Fr02:
    msg_name = "REXVLCUR_LIN2Fr02"
    msg_id = 12
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "REXV"
    rx_nodes = ['LCUR']
    sig_group_dict = {'REXVSerNo': ['REXVSerNoNr1', 'REXVSerNoNr2', 'REXVSerNoNr3', 'REXVSerNoNr4']}
    sig_group_dataid_dict = {}

    class REXVSerNoNr2:
        sig_name = "REXVSerNoNr2"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 8
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class REXVSerNoNr1:
        sig_name = "REXVSerNoNr1"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class REXVSerNoNr3:
        sig_name = "REXVSerNoNr3"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class REXVSerNoNr4:
        sig_name = "REXVSerNoNr4"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class TERVLCUR_LIN2Fr01:
    msg_name = "TERVLCUR_LIN2Fr01"
    msg_id = 14
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "TERV"
    rx_nodes = ['LCUR']
    sig_group_dict = {'TERVPartNo': ['TERVPartNoEndSgn1', 'TERVPartNoEndSgn2', 'TERVPartNoEndSgn3', 'TERVPartNoNr1', 'TERVPartNoNr2', 'TERVPartNoNr3', 'TERVPartNoNr4', 'TERVPartNoNr5']}
    sig_group_dataid_dict = {}

    class TERVPartNoEndSgn1:
        sig_name = "TERVPartNoEndSgn1"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class TERVPartNoNr1:
        sig_name = "TERVPartNoNr1"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class TERVPartNoEndSgn2:
        sig_name = "TERVPartNoEndSgn2"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 8
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class TERVPartNoNr5:
        sig_name = "TERVPartNoNr5"
        sig_start_bit = 56
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 56
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class TERVPartNoNr2:
        sig_name = "TERVPartNoNr2"
        sig_start_bit = 32
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 32
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class TERVPartNoEndSgn3:
        sig_name = "TERVPartNoEndSgn3"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class TERVPartNoNr3:
        sig_name = "TERVPartNoNr3"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 40
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class TERVPartNoNr4:
        sig_name = "TERVPartNoNr4"
        sig_start_bit = 48
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 48
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class TERVLCUR_LIN2Fr02:
    msg_name = "TERVLCUR_LIN2Fr02"
    msg_id = 15
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "TERV"
    rx_nodes = ['LCUR']
    sig_group_dict = {'TERVSerNo': ['TERVSerNoNr1', 'TERVSerNoNr2', 'TERVSerNoNr3', 'TERVSerNoNr4']}
    sig_group_dataid_dict = {}

    class TERVSerNoNr1:
        sig_name = "TERVSerNoNr1"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class TERVSerNoNr2:
        sig_name = "TERVSerNoNr2"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 8
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class TERVSerNoNr3:
        sig_name = "TERVSerNoNr3"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class TERVSerNoNr4:
        sig_name = "TERVSerNoNr4"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class BEXVLCUR_LIN2Fr03:
    msg_name = "BEXVLCUR_LIN2Fr03"
    msg_id = 2
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "BEXV"
    rx_nodes = ['LCUR']
    sig_group_dict = {'BEXVSts': ['BEXVStsExvBlkErr', 'BEXVStsExvCalSts', 'BEXVStsExvElecErr', 'BEXVStsExvMoveSts', 'BEXVStsExvOvrTempErr', 'BEXVStsExvOvrTrvlErr', 'BEXVStsExvPosnAct', 'BEXVStsExvURangErr', 'BEXVStsPreHeatgSts']}
    sig_group_dataid_dict = {}

    class BEXVStsExvOvrTempErr:
        sig_name = "BEXVStsExvOvrTempErr"
        sig_start_bit = 6
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err_Initial': 0, 'Err_NoError': 1, 'Err_Error': 2, 'Err_Reserve': 3}
        compute_method = None
        length = 2
        startbit = 6
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class BEXVStsExvOvrTrvlErr:
        sig_name = "BEXVStsExvOvrTrvlErr"
        sig_start_bit = 12
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err_Initial': 0, 'Err_NoError': 1, 'Err_Error': 2, 'Err_Reserve': 3}
        compute_method = None
        length = 2
        startbit = 12
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class BEXVStsExvURangErr:
        sig_name = "BEXVStsExvURangErr"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvVoltgRangErr_NoErr': 0, 'ExvVoltgRangErr_UnderVoltageErr': 1, 'ExvVoltgRangErr_OverVoltageErr': 2, 'ExvVoltgRangErr_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 24
        byte = 3
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class BEXVStsPreHeatgSts:
        sig_name = "BEXVStsPreHeatgSts"
        sig_start_bit = 26
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 26
        byte = 3
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class BEXVStsExvPosnAct:
        sig_name = "BEXVStsExvPosnAct"
        sig_start_bit = 14
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 14
        bmuws_info = [(1, 0b11000000, 0b00111111, 2, 6), (2, 0b11111111, 0b00000000, 8, 0)]

    class BEXVStsExvBlkErr:
        sig_name = "BEXVStsExvBlkErr"
        sig_start_bit = 2
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err_Initial': 0, 'Err_NoError': 1, 'Err_Error': 2, 'Err_Reserve': 3}
        compute_method = None
        length = 2
        startbit = 2
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class BEXVStsExvCalSts:
        sig_name = "BEXVStsExvCalSts"
        sig_start_bit = 4
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvCalibSts_NotInitialized': 0, 'ExvCalibSts_InitializationInProcess': 1, 'ExvCalibSts_Initialized': 2, 'ExvCalibSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 4
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class BEXVStsExvMoveSts:
        sig_name = "BEXVStsExvMoveSts"
        sig_start_bit = 11
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvMovSts_NotMove': 0, 'ExvMovSts_Moving': 1}
        compute_method = None
        length = 1
        startbit = 11
        byte = 1
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class BEXVStsExvElecErr:
        sig_name = "BEXVStsExvElecErr"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvElecStsErr_NoError': 0, 'ExvElecStsErr_OpenCircuit': 1, 'ExvElecStsErr_ShortCircuit': 2, 'ExvElecStsErr_OverTemperatureShutdown': 3, 'ExvElecStsErr_IndeterminateElectricFault': 4, 'ExvElecStsErr_Reserved': 5}
        compute_method = None
        length = 3
        startbit = 8
        byte = 1
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class BEXVNVMFlt:
        sig_name = "BEXVNVMFlt"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flt_Initial': 0, 'Flt_NoFault': 1, 'Flt_Fault': 2}
        compute_method = None
        length = 2
        startbit = 0
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0


class CERVLCUR_LIN2Fr01:
    msg_name = "CERVLCUR_LIN2Fr01"
    msg_id = 3
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "CERV"
    rx_nodes = ['LCUR']
    sig_group_dict = {'CERVPartNo': ['CERVPartNoEndSgn1', 'CERVPartNoEndSgn2', 'CERVPartNoEndSgn3', 'CERVPartNoNr1', 'CERVPartNoNr2', 'CERVPartNoNr3', 'CERVPartNoNr4', 'CERVPartNoNr5']}
    sig_group_dataid_dict = {}

    class CERVPartNoEndSgn2:
        sig_name = "CERVPartNoEndSgn2"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 8
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CERVPartNoNr1:
        sig_name = "CERVPartNoNr1"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CERVPartNoNr3:
        sig_name = "CERVPartNoNr3"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 40
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CERVPartNoEndSgn1:
        sig_name = "CERVPartNoEndSgn1"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CERVPartNoEndSgn3:
        sig_name = "CERVPartNoEndSgn3"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CERVPartNoNr2:
        sig_name = "CERVPartNoNr2"
        sig_start_bit = 32
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 32
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CERVPartNoNr5:
        sig_name = "CERVPartNoNr5"
        sig_start_bit = 56
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 56
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CERVPartNoNr4:
        sig_name = "CERVPartNoNr4"
        sig_start_bit = 48
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 48
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class FEXVLCUR_LIN2Fr02:
    msg_name = "FEXVLCUR_LIN2Fr02"
    msg_id = 7
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "FEXV"
    rx_nodes = ['LCUR']
    sig_group_dict = {'FEXVSerNo': ['FEXVSerNoNr1', 'FEXVSerNoNr2', 'FEXVSerNoNr3', 'FEXVSerNoNr4']}
    sig_group_dataid_dict = {}

    class FEXVSerNoNr4:
        sig_name = "FEXVSerNoNr4"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FEXVSerNoNr1:
        sig_name = "FEXVSerNoNr1"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FEXVSerNoNr2:
        sig_name = "FEXVSerNoNr2"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 8
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FEXVSerNoNr3:
        sig_name = "FEXVSerNoNr3"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class TERVLCUR_LIN2Fr03:
    msg_name = "TERVLCUR_LIN2Fr03"
    msg_id = 16
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "TERV"
    rx_nodes = ['LCUR']
    sig_group_dict = {'TERVSts': ['TERVStsExvBlkErr', 'TERVStsExvCalSts', 'TERVStsExvElecErr', 'TERVStsExvMoveSts', 'TERVStsExvOvrTempErr', 'TERVStsExvOvrTrvlErr', 'TERVStsExvPosnAct', 'TERVStsExvURangErr', 'TERVStsPreHeatgSts']}
    sig_group_dataid_dict = {}

    class TERVStsExvPosnAct:
        sig_name = "TERVStsExvPosnAct"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 16
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b00000011, 0b11111100, 2, 0)]

    class TERVNVMFlt:
        sig_name = "TERVNVMFlt"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flt_Initial': 0, 'Flt_NoFault': 1, 'Flt_Fault': 2}
        compute_method = None
        length = 2
        startbit = 0
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class TERVStsExvBlkErr:
        sig_name = "TERVStsExvBlkErr"
        sig_start_bit = 2
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err_Initial': 0, 'Err_NoError': 1, 'Err_Error': 2, 'Err_Reserve': 3}
        compute_method = None
        length = 2
        startbit = 2
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class TERVStsExvMoveSts:
        sig_name = "TERVStsExvMoveSts"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvMovSts_NotMove': 0, 'ExvMovSts_Moving': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class TERVStsExvCalSts:
        sig_name = "TERVStsExvCalSts"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvCalibSts_NotInitialized': 0, 'ExvCalibSts_InitializationInProcess': 1, 'ExvCalibSts_Initialized': 2, 'ExvCalibSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 8
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class TERVStsExvURangErr:
        sig_name = "TERVStsExvURangErr"
        sig_start_bit = 14
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvVoltgRangErr_NoErr': 0, 'ExvVoltgRangErr_UnderVoltageErr': 1, 'ExvVoltgRangErr_OverVoltageErr': 2, 'ExvVoltgRangErr_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 14
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class TERVStsExvElecErr:
        sig_name = "TERVStsExvElecErr"
        sig_start_bit = 4
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvElecStsErr_NoError': 0, 'ExvElecStsErr_OpenCircuit': 1, 'ExvElecStsErr_ShortCircuit': 2, 'ExvElecStsErr_OverTemperatureShutdown': 3, 'ExvElecStsErr_IndeterminateElectricFault': 4, 'ExvElecStsErr_Reserved': 5}
        compute_method = None
        length = 3
        startbit = 4
        byte = 0
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class TERVStsExvOvrTrvlErr:
        sig_name = "TERVStsExvOvrTrvlErr"
        sig_start_bit = 12
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err_Initial': 0, 'Err_NoError': 1, 'Err_Error': 2, 'Err_Reserve': 3}
        compute_method = None
        length = 2
        startbit = 12
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class TERVStsExvOvrTempErr:
        sig_name = "TERVStsExvOvrTempErr"
        sig_start_bit = 10
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err_Initial': 0, 'Err_NoError': 1, 'Err_Error': 2, 'Err_Reserve': 3}
        compute_method = None
        length = 2
        startbit = 10
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class TERVStsPreHeatgSts:
        sig_name = "TERVStsPreHeatgSts"
        sig_start_bit = 26
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 26
        byte = 3
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2


class WERVLCUR_LIN2Fr02:
    msg_name = "WERVLCUR_LIN2Fr02"
    msg_id = 18
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "WERV"
    rx_nodes = ['LCUR']
    sig_group_dict = {'WERVSerNo': ['WERVSerNoNr1', 'WERVSerNoNr2', 'WERVSerNoNr3', 'WERVSerNoNr4']}
    sig_group_dataid_dict = {}

    class WERVSerNoNr1:
        sig_name = "WERVSerNoNr1"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class WERVSerNoNr4:
        sig_name = "WERVSerNoNr4"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class WERVSerNoNr2:
        sig_name = "WERVSerNoNr2"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 8
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class WERVSerNoNr3:
        sig_name = "WERVSerNoNr3"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class CERVLCUR_LIN2Fr02:
    msg_name = "CERVLCUR_LIN2Fr02"
    msg_id = 4
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "CERV"
    rx_nodes = ['LCUR']
    sig_group_dict = {'CERVSerNo': ['CERVSerNoNr1', 'CERVSerNoNr2', 'CERVSerNoNr3', 'CERVSerNoNr4']}
    sig_group_dataid_dict = {}

    class CERVSerNoNr2:
        sig_name = "CERVSerNoNr2"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 8
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CERVSerNoNr4:
        sig_name = "CERVSerNoNr4"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CERVSerNoNr3:
        sig_name = "CERVSerNoNr3"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CERVSerNoNr1:
        sig_name = "CERVSerNoNr1"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class LCURLCUR_LIN2Fr02:
    msg_name = "LCURLCUR_LIN2Fr02"
    msg_id = 10
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "LCUR"
    rx_nodes = ['WERV', 'TERV']
    sig_group_dict = {'WERVReq': ['WERVReqExvCalReq', 'WERVReqExvMovEna', 'WERVReqExvPosnReq', 'WERVReqExvPreHeatgReq'], 'TERVReq': ['TERVReqExvCalReq', 'TERVReqExvMovEna', 'TERVReqExvPosnReq', 'TERVReqExvPreHeatgReq']}
    sig_group_dataid_dict = {}

    class TERVReqExvPosnReq:
        sig_name = "TERVReqExvPosnReq"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 0
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b00000011, 0b11111100, 2, 0)]

    class WERVReqExvPreHeatgReq:
        sig_name = "WERVReqExvPreHeatgReq"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvHeatdReq_NoReq': 0, 'ExvHeatdReq_PreHeatedReq': 1}
        compute_method = None
        length = 1
        startbit = 15
        byte = 1
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class WERVReqExvMovEna:
        sig_name = "WERVReqExvMovEna"
        sig_start_bit = 14
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvMovEnable_EXVNotEnable': 0, 'ExvMovEnable_EXVEnable': 1}
        compute_method = None
        length = 1
        startbit = 14
        byte = 1
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class TERVReqExvPreHeatgReq:
        sig_name = "TERVReqExvPreHeatgReq"
        sig_start_bit = 12
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvHeatdReq_NoReq': 0, 'ExvHeatdReq_PreHeatedReq': 1}
        compute_method = None
        length = 1
        startbit = 12
        byte = 1
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class TERVReqExvCalReq:
        sig_name = "TERVReqExvCalReq"
        sig_start_bit = 10
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvCalibReq_NoReq': 0, 'ExvCalibReq_InitializationReq': 1}
        compute_method = None
        length = 1
        startbit = 10
        byte = 1
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class WERVReqExvCalReq:
        sig_name = "WERVReqExvCalReq"
        sig_start_bit = 13
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvCalibReq_NoReq': 0, 'ExvCalibReq_InitializationReq': 1}
        compute_method = None
        length = 1
        startbit = 13
        byte = 1
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class TERVReqExvMovEna:
        sig_name = "TERVReqExvMovEna"
        sig_start_bit = 11
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvMovEnable_EXVNotEnable': 0, 'ExvMovEnable_EXVEnable': 1}
        compute_method = None
        length = 1
        startbit = 11
        byte = 1
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class WERVReqExvPosnReq:
        sig_name = "WERVReqExvPosnReq"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 16
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b00000011, 0b11111100, 2, 0)]


class DiagResponse3:
    msg_name = "DiagResponse3"
    msg_id = 61
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['LCUR']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class CERVLCUR_LIN2Fr03:
    msg_name = "CERVLCUR_LIN2Fr03"
    msg_id = 5
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "CERV"
    rx_nodes = ['LCUR']
    sig_group_dict = {'CERVSts': ['CERVStsExvBlkErr', 'CERVStsExvCalSts', 'CERVStsExvElecErr', 'CERVStsExvMoveSts', 'CERVStsExvOvrTempErr', 'CERVStsExvOvrTrvlErr', 'CERVStsExvPosnAct', 'CERVStsExvURangErr', 'CERVStsPreHeatgSts']}
    sig_group_dataid_dict = {}

    class CERVStsExvBlkErr:
        sig_name = "CERVStsExvBlkErr"
        sig_start_bit = 2
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err_Initial': 0, 'Err_NoError': 1, 'Err_Error': 2, 'Err_Reserve': 3}
        compute_method = None
        length = 2
        startbit = 2
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class CERVStsPreHeatgSts:
        sig_name = "CERVStsPreHeatgSts"
        sig_start_bit = 26
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 26
        byte = 3
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class CERVStsExvCalSts:
        sig_name = "CERVStsExvCalSts"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvCalibSts_NotInitialized': 0, 'ExvCalibSts_InitializationInProcess': 1, 'ExvCalibSts_Initialized': 2, 'ExvCalibSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 8
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class CERVStsExvOvrTrvlErr:
        sig_name = "CERVStsExvOvrTrvlErr"
        sig_start_bit = 12
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err_Initial': 0, 'Err_NoError': 1, 'Err_Error': 2, 'Err_Reserve': 3}
        compute_method = None
        length = 2
        startbit = 12
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class CERVStsExvPosnAct:
        sig_name = "CERVStsExvPosnAct"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 16
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b00000011, 0b11111100, 2, 0)]

    class CERVStsExvURangErr:
        sig_name = "CERVStsExvURangErr"
        sig_start_bit = 14
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvVoltgRangErr_NoErr': 0, 'ExvVoltgRangErr_UnderVoltageErr': 1, 'ExvVoltgRangErr_OverVoltageErr': 2, 'ExvVoltgRangErr_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 14
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class CERVStsExvOvrTempErr:
        sig_name = "CERVStsExvOvrTempErr"
        sig_start_bit = 10
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err_Initial': 0, 'Err_NoError': 1, 'Err_Error': 2, 'Err_Reserve': 3}
        compute_method = None
        length = 2
        startbit = 10
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class CERVStsExvMoveSts:
        sig_name = "CERVStsExvMoveSts"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvMovSts_NotMove': 0, 'ExvMovSts_Moving': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class CERVNVMFlt:
        sig_name = "CERVNVMFlt"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flt_Initial': 0, 'Flt_NoFault': 1, 'Flt_Fault': 2}
        compute_method = None
        length = 2
        startbit = 0
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class CERVStsExvElecErr:
        sig_name = "CERVStsExvElecErr"
        sig_start_bit = 4
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvElecStsErr_NoError': 0, 'ExvElecStsErr_OpenCircuit': 1, 'ExvElecStsErr_ShortCircuit': 2, 'ExvElecStsErr_OverTemperatureShutdown': 3, 'ExvElecStsErr_IndeterminateElectricFault': 4, 'ExvElecStsErr_Reserved': 5}
        compute_method = None
        length = 3
        startbit = 4
        byte = 0
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4


class LCURLCUR_LIN2Fr01:
    msg_name = "LCURLCUR_LIN2Fr01"
    msg_id = 9
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "LCUR"
    rx_nodes = ['CERV', 'REXV', 'BEXV', 'FEXV']
    sig_group_dict = {'EEXVReq': ['EEXVReqExvCalReq', 'EEXVReqExvMovEna', 'EEXVReqExvPosnReq', 'EEXVReqExvPreHeatgReq'], 'CERVReq': ['CERVReqExvCalReq', 'CERVReqExvMovEna', 'CERVReqExvPosnReq', 'CERVReqExvPreHeatgReq'], 'REXVReq': ['REXVReqExvCalReq', 'REXVReqExvMovEna', 'REXVReqExvPosnReq', 'REXVReqExvPreHeatgReq'], 'BEXVReq': ['BEXVReqExvCalReq', 'BEXVReqExvMovEna', 'BEXVReqExvPosnReq', 'BEXVReqExvPreHeatgReq']}
    sig_group_dataid_dict = {}

    class BEXVReqExvPosnReq:
        sig_name = "BEXVReqExvPosnReq"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 0
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b00000011, 0b11111100, 2, 0)]

    class BEXVReqExvCalReq:
        sig_name = "BEXVReqExvCalReq"
        sig_start_bit = 10
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvCalibReq_NoReq': 0, 'ExvCalibReq_InitializationReq': 1}
        compute_method = None
        length = 1
        startbit = 10
        byte = 1
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class REXVReqExvPosnReq:
        sig_name = "REXVReqExvPosnReq"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 40
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b00000011, 0b11111100, 2, 0)]

    class CERVReqExvPreHeatgReq:
        sig_name = "CERVReqExvPreHeatgReq"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvHeatdReq_NoReq': 0, 'ExvHeatdReq_PreHeatedReq': 1}
        compute_method = None
        length = 1
        startbit = 15
        byte = 1
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class EEXVReqExvPreHeatgReq:
        sig_name = "EEXVReqExvPreHeatgReq"
        sig_start_bit = 29
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvHeatdReq_NoReq': 0, 'ExvHeatdReq_PreHeatedReq': 1}
        compute_method = None
        length = 1
        startbit = 29
        byte = 3
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class EEXVReqExvCalReq:
        sig_name = "EEXVReqExvCalReq"
        sig_start_bit = 27
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvCalibReq_NoReq': 0, 'ExvCalibReq_InitializationReq': 1}
        compute_method = None
        length = 1
        startbit = 27
        byte = 3
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class REXVReqExvMovEna:
        sig_name = "REXVReqExvMovEna"
        sig_start_bit = 51
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvMovEnable_EXVNotEnable': 0, 'ExvMovEnable_EXVEnable': 1}
        compute_method = None
        length = 1
        startbit = 51
        byte = 6
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class BEXVReqExvMovEna:
        sig_name = "BEXVReqExvMovEna"
        sig_start_bit = 11
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvMovEnable_EXVNotEnable': 0, 'ExvMovEnable_EXVEnable': 1}
        compute_method = None
        length = 1
        startbit = 11
        byte = 1
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class CERVReqExvCalReq:
        sig_name = "CERVReqExvCalReq"
        sig_start_bit = 13
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvCalibReq_NoReq': 0, 'ExvCalibReq_InitializationReq': 1}
        compute_method = None
        length = 1
        startbit = 13
        byte = 1
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class EEXVReqExvPosnReq:
        sig_name = "EEXVReqExvPosnReq"
        sig_start_bit = 30
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 30
        bmuws_info = [(3, 0b11000000, 0b00111111, 2, 6), (4, 0b11111111, 0b00000000, 8, 0)]

    class CERVReqExvPosnReq:
        sig_name = "CERVReqExvPosnReq"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 16
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b00000011, 0b11111100, 2, 0)]

    class CERVReqExvMovEna:
        sig_name = "CERVReqExvMovEna"
        sig_start_bit = 14
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvMovEnable_EXVNotEnable': 0, 'ExvMovEnable_EXVEnable': 1}
        compute_method = None
        length = 1
        startbit = 14
        byte = 1
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class REXVReqExvCalReq:
        sig_name = "REXVReqExvCalReq"
        sig_start_bit = 50
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvCalibReq_NoReq': 0, 'ExvCalibReq_InitializationReq': 1}
        compute_method = None
        length = 1
        startbit = 50
        byte = 6
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class BEXVReqExvPreHeatgReq:
        sig_name = "BEXVReqExvPreHeatgReq"
        sig_start_bit = 12
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvHeatdReq_NoReq': 0, 'ExvHeatdReq_PreHeatedReq': 1}
        compute_method = None
        length = 1
        startbit = 12
        byte = 1
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class REXVReqExvPreHeatgReq:
        sig_name = "REXVReqExvPreHeatgReq"
        sig_start_bit = 52
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvHeatdReq_NoReq': 0, 'ExvHeatdReq_PreHeatedReq': 1}
        compute_method = None
        length = 1
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class EEXVReqExvMovEna:
        sig_name = "EEXVReqExvMovEna"
        sig_start_bit = 28
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvMovEnable_EXVNotEnable': 0, 'ExvMovEnable_EXVEnable': 1}
        compute_method = None
        length = 1
        startbit = 28
        byte = 3
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4


class DiagRequest3:
    msg_name = "DiagRequest3"
    msg_id = 60
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "LCUR"
    rx_nodes = []
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class WERVLCUR_LIN2Fr03:
    msg_name = "WERVLCUR_LIN2Fr03"
    msg_id = 19
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "WERV"
    rx_nodes = ['LCUR']
    sig_group_dict = {'WERVSts': ['WERVStsExvBlkErr', 'WERVStsExvCalSts', 'WERVStsExvElecErr', 'WERVStsExvMoveSts', 'WERVStsExvOvrTempErr', 'WERVStsExvOvrTrvlErr', 'WERVStsExvPosnAct', 'WERVStsExvURangErr', 'WERVStsPreHeatgSts']}
    sig_group_dataid_dict = {}

    class WERVStsPreHeatgSts:
        sig_name = "WERVStsPreHeatgSts"
        sig_start_bit = 26
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 26
        byte = 3
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class WERVStsExvURangErr:
        sig_name = "WERVStsExvURangErr"
        sig_start_bit = 14
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvVoltgRangErr_NoErr': 0, 'ExvVoltgRangErr_UnderVoltageErr': 1, 'ExvVoltgRangErr_OverVoltageErr': 2, 'ExvVoltgRangErr_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 14
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class WERVStsExvOvrTrvlErr:
        sig_name = "WERVStsExvOvrTrvlErr"
        sig_start_bit = 12
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err_Initial': 0, 'Err_NoError': 1, 'Err_Error': 2, 'Err_Reserve': 3}
        compute_method = None
        length = 2
        startbit = 12
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class WERVNVMFlt:
        sig_name = "WERVNVMFlt"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flt_Initial': 0, 'Flt_NoFault': 1, 'Flt_Fault': 2}
        compute_method = None
        length = 2
        startbit = 0
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class WERVStsExvOvrTempErr:
        sig_name = "WERVStsExvOvrTempErr"
        sig_start_bit = 10
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err_Initial': 0, 'Err_NoError': 1, 'Err_Error': 2, 'Err_Reserve': 3}
        compute_method = None
        length = 2
        startbit = 10
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class WERVStsExvCalSts:
        sig_name = "WERVStsExvCalSts"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvCalibSts_NotInitialized': 0, 'ExvCalibSts_InitializationInProcess': 1, 'ExvCalibSts_Initialized': 2, 'ExvCalibSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 8
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class WERVStsExvPosnAct:
        sig_name = "WERVStsExvPosnAct"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 16
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b00000011, 0b11111100, 2, 0)]

    class WERVStsExvBlkErr:
        sig_name = "WERVStsExvBlkErr"
        sig_start_bit = 2
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err_Initial': 0, 'Err_NoError': 1, 'Err_Error': 2, 'Err_Reserve': 3}
        compute_method = None
        length = 2
        startbit = 2
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class WERVStsExvElecErr:
        sig_name = "WERVStsExvElecErr"
        sig_start_bit = 4
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvElecStsErr_NoError': 0, 'ExvElecStsErr_OpenCircuit': 1, 'ExvElecStsErr_ShortCircuit': 2, 'ExvElecStsErr_OverTemperatureShutdown': 3, 'ExvElecStsErr_IndeterminateElectricFault': 4, 'ExvElecStsErr_Reserved': 5}
        compute_method = None
        length = 3
        startbit = 4
        byte = 0
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class WERVStsExvMoveSts:
        sig_name = "WERVStsExvMoveSts"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvMovSts_NotMove': 0, 'ExvMovSts_Moving': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7


class BEXVLCUR_LIN2Fr01:
    msg_name = "BEXVLCUR_LIN2Fr01"
    msg_id = 0
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "BEXV"
    rx_nodes = ['LCUR']
    sig_group_dict = {'BEXVPartNo': ['BEXVPartNoEndSgn1', 'BEXVPartNoEndSgn2', 'BEXVPartNoEndSgn3', 'BEXVPartNoNr1', 'BEXVPartNoNr2', 'BEXVPartNoNr3', 'BEXVPartNoNr4', 'BEXVPartNoNr5']}
    sig_group_dataid_dict = {}

    class BEXVPartNoEndSgn2:
        sig_name = "BEXVPartNoEndSgn2"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 8
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BEXVPartNoNr2:
        sig_name = "BEXVPartNoNr2"
        sig_start_bit = 32
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 32
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BEXVPartNoNr4:
        sig_name = "BEXVPartNoNr4"
        sig_start_bit = 48
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 48
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BEXVPartNoNr5:
        sig_name = "BEXVPartNoNr5"
        sig_start_bit = 56
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 56
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BEXVPartNoNr1:
        sig_name = "BEXVPartNoNr1"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BEXVPartNoEndSgn3:
        sig_name = "BEXVPartNoEndSgn3"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BEXVPartNoNr3:
        sig_name = "BEXVPartNoNr3"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 40
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BEXVPartNoEndSgn1:
        sig_name = "BEXVPartNoEndSgn1"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class FEXVLCUR_LIN2Fr01:
    msg_name = "FEXVLCUR_LIN2Fr01"
    msg_id = 6
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "FEXV"
    rx_nodes = ['LCUR']
    sig_group_dict = {'FEXVPartNo': ['FEXVPartNoEndSgn1', 'FEXVPartNoEndSgn2', 'FEXVPartNoEndSgn3', 'FEXVPartNoNr1', 'FEXVPartNoNr2', 'FEXVPartNoNr3', 'FEXVPartNoNr4', 'FEXVPartNoNr5']}
    sig_group_dataid_dict = {}

    class FEXVPartNoNr1:
        sig_name = "FEXVPartNoNr1"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FEXVPartNoEndSgn3:
        sig_name = "FEXVPartNoEndSgn3"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FEXVPartNoNr3:
        sig_name = "FEXVPartNoNr3"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 40
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FEXVPartNoNr5:
        sig_name = "FEXVPartNoNr5"
        sig_start_bit = 56
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 56
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FEXVPartNoNr2:
        sig_name = "FEXVPartNoNr2"
        sig_start_bit = 32
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 32
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FEXVPartNoEndSgn2:
        sig_name = "FEXVPartNoEndSgn2"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 8
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FEXVPartNoEndSgn1:
        sig_name = "FEXVPartNoEndSgn1"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FEXVPartNoNr4:
        sig_name = "FEXVPartNoNr4"
        sig_start_bit = 48
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 48
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class BEXVLCUR_LIN2Fr02:
    msg_name = "BEXVLCUR_LIN2Fr02"
    msg_id = 1
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "BEXV"
    rx_nodes = ['LCUR']
    sig_group_dict = {'BEXVSerNo': ['BEXVSerNoNr1', 'BEXVSerNoNr2', 'BEXVSerNoNr3', 'BEXVSerNoNr4']}
    sig_group_dataid_dict = {}

    class BEXVSerNoNr2:
        sig_name = "BEXVSerNoNr2"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 8
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BEXVSerNoNr3:
        sig_name = "BEXVSerNoNr3"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BEXVSerNoNr1:
        sig_name = "BEXVSerNoNr1"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BEXVSerNoNr4:
        sig_name = "BEXVSerNoNr4"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


