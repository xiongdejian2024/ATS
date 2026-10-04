lin_scheduleTable = {'Ecm_Lin1LinSchedule01_ECM_LIN1': [(0, 'HvchEcm_Lin1Fr01', 0.01), (1, 'AccmEcm_Lin1Fr01', 0.01), (2, 'EcmEcm_Lin1Fr02', 0.01), (3, 'BctvEcm_Lin1Fr01', 0.015), (4, 'HvahEcm_Lin1Fr01', 0.015), (5, 'EcmEcm_Lin1Fr01', 0.015), (6, 'HvahEcm_Lin1Fr02', 0.01), (7, 'AccmEcm_Lin1Fr02', 0.015), (8, 'AccmEcm_Lin1Fr03', 0.015), (9, 'EcrvEcm_Lin1Fr01', 0.015), (10, 'EcmEcm_Lin1Fr03', 0.01), (11, 'HvchEcm_Lin1Fr02', 0.01), (12, 'BcfvEcm_Lin1Fr01', 0.015), (13, 'EcmEcm_Lin1Fr05', 0.01), (14, 'HvchEcm_Lin1Fr03', 0.01)], 'Ecm_Lin1_DiagResponseSchedule01': [(0, 'DiagResponse8', 0.015)], 'Ecm_Lin1LinScheduleSerNrPartNrTable_ECM_LIN1': [(0, 'AccmEcm_Lin1PartNrFr01', 0.015), (1, 'AccmEcm_Lin1PartNrFr02', 0.015), (2, 'AccmEcm_Lin1SerNrFr01', 0.015), (3, 'HvchEcm_Lin1PartNr10Fr04', 0.015), (4, 'HvchEcm_Lin1PartNr10Fr08', 0.01), (5, 'HvchEcm_Lin1SerNrFr01', 0.01), (6, 'BctvEcm_Lin1PartNrFr01', 0.015), (7, 'BctvEcm_Lin1PartNrFr02', 0.01), (8, 'BctvEcm_Lin1SerNrFr01', 0.01), (9, 'BcfvEcm_Lin1PartNrFr01', 0.015), (10, 'BcfvEcm_Lin1PartNrFr02', 0.01), (11, 'BcfvEcm_Lin1SerNrFr01', 0.01)], 'Ecm_Lin1_DiagRequestSchedule01': [(0, 'DiagRequest8', 0.015)]}


class AccmEcm_Lin1Fr01:
    msg_name = "AccmEcm_Lin1Fr01"
    msg_id = 36
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 7
    tx_node = "ACCM"
    rx_nodes = ['ECM']
    sig_group_dict = {'CmprDiagcFb': ['CmprDiagcFbCmprCmprSpdErr', 'CmprDiagcFbCmprCtrlrErr', 'CmprDiagcFbCmprDrvrCircSnsr', 'CmprDiagcFbCmprDrvrCircSnsrPlaus', 'CmprDiagcFbCmprHvSnsr1', 'CmprDiagcFbCmprHvSnsr2', 'CmprDiagcFbCmprHvSnsrI', 'CmprDiagcFbCmprHvSnsrICrct', 'CmprDiagcFbCmprHvSnsrIPlaus', 'CmprDiagcFbCmprHvSnsrPlaus', 'CmprDiagcFbCmprHvSplyErr', 'CmprDiagcFbCmprPhaseWire', 'CmprDiagcFbCmprT1', 'CmprDiagcFbCmprT2', 'CmprDiagcFbCmprTOperErr1', 'CmprDiagcFbCmprTOperErr2', 'CmprDiagcFbCmprTPlaus', 'CmprDiagcFbCmprUSplyErr']}
    sig_group_dataid_dict = {}

    class CmprDiagcFbCmprT2:
        sig_name = "CmprDiagcFbCmprT2"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 8
        byte = 1
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class CmprDiagcFbCmprT1:
        sig_name = "CmprDiagcFbCmprT1"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 0
        byte = 0
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class CmprDiagcFbCmprHvSnsr2:
        sig_name = "CmprDiagcFbCmprHvSnsr2"
        sig_start_bit = 27
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 27
        byte = 3
        mask = 0b00111000
        unmask = 0b11000111
        shift = 3

    class CmprDiagcFbCmprHvSnsrPlaus:
        sig_name = "CmprDiagcFbCmprHvSnsrPlaus"
        sig_start_bit = 48
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 2
        startbit = 48
        byte = 6
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class CmprDiagcFbCmprCmprSpdErr:
        sig_name = "CmprDiagcFbCmprCmprSpdErr"
        sig_start_bit = 21
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 21
        byte = 2
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class CmprDiagcFbCmprCtrlrErr:
        sig_name = "CmprDiagcFbCmprCtrlrErr"
        sig_start_bit = 30
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 2
        startbit = 30
        byte = 3
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class CmprDiagcFbCmprHvSplyErr:
        sig_name = "CmprDiagcFbCmprHvSplyErr"
        sig_start_bit = 35
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 35
        byte = 4
        mask = 0b00111000
        unmask = 0b11000111
        shift = 3

    class CmprDiagcFbCmprTOperErr2:
        sig_name = "CmprDiagcFbCmprTOperErr2"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 40
        byte = 5
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class CmprDiagcFbCmprHvSnsrICrct:
        sig_name = "CmprDiagcFbCmprHvSnsrICrct"
        sig_start_bit = 5
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 5
        byte = 0
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class CmprDiagcFbCmprDrvrCircSnsr:
        sig_name = "CmprDiagcFbCmprDrvrCircSnsr"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 16
        byte = 2
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class CmprDiagcFbCmprHvSnsrIPlaus:
        sig_name = "CmprDiagcFbCmprHvSnsrIPlaus"
        sig_start_bit = 46
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 2
        startbit = 46
        byte = 5
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class CmprDiagcFbCmprTPlaus:
        sig_name = "CmprDiagcFbCmprTPlaus"
        sig_start_bit = 52
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 2
        startbit = 52
        byte = 6
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class CmprDiagcFbCmprPhaseWire:
        sig_name = "CmprDiagcFbCmprPhaseWire"
        sig_start_bit = 50
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 2
        startbit = 50
        byte = 6
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class CmprDiagcFbCmprTOperErr1:
        sig_name = "CmprDiagcFbCmprTOperErr1"
        sig_start_bit = 13
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 13
        byte = 1
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class CmprDiagcFbCmprHvSnsr1:
        sig_name = "CmprDiagcFbCmprHvSnsr1"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 24
        byte = 3
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class CmprDiagcFbCmprHvSnsrI:
        sig_name = "CmprDiagcFbCmprHvSnsrI"
        sig_start_bit = 32
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 32
        byte = 4
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class CmprDiagcFbCmprDrvrCircSnsrPlaus:
        sig_name = "CmprDiagcFbCmprDrvrCircSnsrPlaus"
        sig_start_bit = 38
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 2
        startbit = 38
        byte = 4
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class CmprDiagcFbCmprUSplyErr:
        sig_name = "CmprDiagcFbCmprUSplyErr"
        sig_start_bit = 43
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 43
        byte = 5
        mask = 0b00111000
        unmask = 0b11000111
        shift = 3


class BctvEcm_Lin1SerNrFr01:
    msg_name = "BctvEcm_Lin1SerNrFr01"
    msg_id = 46
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "BCTV"
    rx_nodes = ['ECM']
    sig_group_dict = {'BCTVSerNo': ['BCTVSerNoNr1', 'BCTVSerNoNr2', 'BCTVSerNoNr3', 'BCTVSerNoNr4']}
    sig_group_dataid_dict = {}

    class BCTVSerNoNr3:
        sig_name = "BCTVSerNoNr3"
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

    class BCTVSerNoNr4:
        sig_name = "BCTVSerNoNr4"
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

    class BCTVSerNoNr1:
        sig_name = "BCTVSerNoNr1"
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

    class BCTVSerNoNr2:
        sig_name = "BCTVSerNoNr2"
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


class BctvEcm_Lin1Fr01:
    msg_name = "BctvEcm_Lin1Fr01"
    msg_id = 43
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "BCTV"
    rx_nodes = ['ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HpBattVlvRunSts:
        sig_name = "HpBattVlvRunSts"
        sig_start_bit = 18
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VlvRunSts_NotMoving': 0, 'VlvRunSts_Moving': 1}
        compute_method = None
        length = 1
        startbit = 18
        byte = 2
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class HpBattVlvMode:
        sig_name = "HpBattVlvMode"
        sig_start_bit = 4
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VlvMode_NormalOperation': 0, 'VlvMode_Mot_Off': 1, 'VlvMode_Learning': 2, 'VlvMode_Fail_Safe': 3, 'VlvMode_SNA': 15}
        compute_method = None
        length = 4
        startbit = 4
        byte = 0
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class HpBattVlvFltSts:
        sig_name = "HpBattVlvFltSts"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FaultSts_NoError': 0, 'FaultSts_PositionUnknown': 1, 'FaultSts_PCTR_Error': 2, 'FaultSts_Blocking_Err': 3, 'FaultSts_SetPoint_Err': 4, 'FaultSts_Learning_Err': 5, 'FaultSts_MotorCoilShort': 6, 'FaultSts_MotorCoilOpen': 7, 'FaultSts_MotorDrvOvertemperatureShutdown': 8, 'FaultSts_Indeterminate': 9, 'FaultSts_Reserved': 10, 'FaultSts_SNA': 15}
        compute_method = None
        length = 4
        startbit = 0
        byte = 0
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class HpBattVlvPosRec:
        sig_name = "HpBattVlvPosRec"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 8
        bmuws_info = [(1, 0b11111111, 0b00000000, 8, 0), (2, 0b00000011, 0b11111100, 2, 0)]

    class HpBattVlvTempSts:
        sig_name = "HpBattVlvTempSts"
        sig_start_bit = 21
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TempSts_Temperatureok': 0, 'TempSts_OvertemperatureWarning': 1, 'TempSts_PCBOvertemperature': 2, 'TempSts_LowTemperature': 3, 'TempSts_notused': 4, 'TempSts_SNA': 7}
        compute_method = None
        length = 3
        startbit = 21
        byte = 2
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class HpBattVlvSpdLvl:
        sig_name = "HpBattVlvSpdLvl"
        sig_start_bit = 19
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SpeedLvl_SpeedLevelLow': 0, 'SpeedLvl_SpeedLevelNormal': 1, 'SpeedLvl_SpeedLevelFast': 2, 'SpeedLvl_SNA': 3}
        compute_method = None
        length = 2
        startbit = 19
        byte = 2
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class BctvNVMFlt:
        sig_name = "BctvNVMFlt"
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
        sig_value_table = {'Flt_NoFault': 0, 'Flt_Fault': 1}
        compute_method = None
        length = 1
        startbit = 27
        byte = 3
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class HpBattVlvVoltSts:
        sig_name = "HpBattVlvVoltSts"
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
        sig_value_table = {'VoltSts_VoltageOK': 0, 'VoltSts_OverVoltage': 1, 'VoltSts_UnderVoltage': 2, 'VoltSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 24
        byte = 3
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0


class EcrvEcm_Lin1Fr01:
    msg_name = "EcrvEcm_Lin1Fr01"
    msg_id = 10
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "ECRV"
    rx_nodes = ['ECM']
    sig_group_dict = {'EctvStat': ['EctvStatVlvFaultSts', 'EctvStatVlvPosSts', 'EctvStatVlvRunSts', 'EctvStatVlvSpdLvl', 'EctvStatVlvTempSts', 'EctvStatVoltSts']}
    sig_group_dataid_dict = {}

    class EctvStatVlvTempSts:
        sig_name = "EctvStatVlvTempSts"
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
        sig_value_table = {'VlvTempSts_TemperaureOK': 0, 'VlvTempSts_OverTemperatureWarning': 1, 'VlvTempSts_Reserved1': 2, 'VlvTempSts_Reserved2': 3}
        compute_method = None
        length = 2
        startbit = 4
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class EctvStatVlvFaultSts:
        sig_name = "EctvStatVlvFaultSts"
        sig_start_bit = 1
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VlvFaultSts_NoFault': 0, 'VlvFaultSts_MotorCoilShort': 1, 'VlvFaultSts_MotorCoilOpen': 2, 'VlvFaultSts_OverTemperatureShutdown': 3, 'VlvFaultSts_FaultStateIndeterminate': 4, 'VlvFaultSts_Reserved': 5}
        compute_method = None
        length = 3
        startbit = 1
        byte = 0
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class EctvStatVlvSpdLvl:
        sig_name = "EctvStatVlvSpdLvl"
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
        sig_value_table = {'VlvSpdLvl_Invalid': 0, 'VlvSpdLvl_Level1': 1, 'VlvSpdLvl_Level2': 2, 'VlvSpdLvl_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 14
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class EctvStatVlvRunSts:
        sig_name = "EctvStatVlvRunSts"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VlvRunSts_NotMoving': 0, 'VlvRunSts_Moving': 1}
        compute_method = None
        length = 1
        startbit = 8
        byte = 1
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class EctvStatVlvPosSts:
        sig_name = "EctvStatVlvPosSts"
        sig_start_bit = 9
        update_id_bit = None
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 22
        sig_byteorder = "Intel"
        sig_value_init = 21
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VlvPosSts_FullClosePosition': 0, 'VlvPosSts_Level1OpenPosition': 1, 'VlvPosSts_Level2OpenPosition': 2, 'VlvPosSts_Level3OpenPosition': 3, 'VlvPosSts_Level4OpenPosition': 4, 'VlvPosSts_Level5OpenPosition': 5, 'VlvPosSts_Level6OpenPosition': 6, 'VlvPosSts_Level7OpenPosition': 7, 'VlvPosSts_Level8OpenPosition': 8, 'VlvPosSts_Level9OpenPosition': 9, 'VlvPosSts_Level10OpenPosition': 10, 'VlvPosSts_Level11OpenPosition': 11, 'VlvPosSts_Level12OpenPosition': 12, 'VlvPosSts_Level13OpenPosition': 13, 'VlvPosSts_Level14OpenPosition': 14, 'VlvPosSts_Level15OpenPosition': 15, 'VlvPosSts_Level16OpenPosition': 16, 'VlvPosSts_Level17OpenPosition': 17, 'VlvPosSts_Level18OpenPosition': 18, 'VlvPosSts_Level19OpenPosition': 19, 'VlvPosSts_FullOpenPosition': 20, 'VlvPosSts_UnknowPosition': 21, 'VlvPosSts_Reserved': 22}
        compute_method = None
        length = 5
        startbit = 9
        byte = 1
        mask = 0b00111110
        unmask = 0b11000001
        shift = 1

    class EctvStatVoltSts:
        sig_name = "EctvStatVoltSts"
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
        sig_value_table = {'VoltSts_VoltageOK': 0, 'VoltSts_OverVoltage': 1, 'VoltSts_UnderVoltage': 2, 'VoltSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 6
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class HvchEcm_Lin1Fr03:
    msg_name = "HvchEcm_Lin1Fr03"
    msg_id = 52
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 3
    tx_node = "HVCH"
    rx_nodes = ['ECM']
    sig_group_dict = {'HvCooltHeatrStsWhE2E': ['HvCooltHeatrStsWhE2EChks', 'HvCooltHeatrStsWhE2ECntr', 'HvCooltHeatrStsWhE2EHvchSts']}
    sig_group_dataid_dict = {'HvCooltHeatrStsWhE2E': 6002}

    class HvCooltHeatrStsWhE2EChks:
        sig_name = "HvCooltHeatrStsWhE2EChks"
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

    class HvCooltHeatrStsWhE2EHvchSts:
        sig_name = "HvCooltHeatrStsWhE2EHvchSts"
        sig_start_bit = 12
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvCooltHeatrSts_Off': 0, 'HvCooltHeatrSts_LockedUntilNextStart': 1, 'HvCooltHeatrSts_LockedUntilService': 2, 'HvCooltHeatrSts_LockedPermanent': 3, 'HvCooltHeatrSts_Operation': 4, 'HvCooltHeatrSts_Reserved1': 5, 'HvCooltHeatrSts_Reserved2': 6, 'HvCooltHeatrSts_Reserved3': 7}
        compute_method = None
        length = 3
        startbit = 12
        byte = 1
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class HvCooltHeatrStsWhE2ECntr:
        sig_name = "HvCooltHeatrStsWhE2ECntr"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 8
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0


class BcfvEcm_Lin1PartNrFr01:
    msg_name = "BcfvEcm_Lin1PartNrFr01"
    msg_id = 13
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "BCFV"
    rx_nodes = ['ECM']
    sig_group_dict = {'BCFVPartNo10Cmpl': ['BCFVPartNo10CmplEndSgn1', 'BCFVPartNo10CmplEndSgn2', 'BCFVPartNo10CmplEndSgn3', 'BCFVPartNo10CmplNr1', 'BCFVPartNo10CmplNr2', 'BCFVPartNo10CmplNr3', 'BCFVPartNo10CmplNr4', 'BCFVPartNo10CmplNr5']}
    sig_group_dataid_dict = {}

    class BCFVPartNo10CmplNr1:
        sig_name = "BCFVPartNo10CmplNr1"
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

    class BCFVPartNo10CmplNr3:
        sig_name = "BCFVPartNo10CmplNr3"
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

    class BCFVPartNo10CmplEndSgn3:
        sig_name = "BCFVPartNo10CmplEndSgn3"
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

    class BCFVPartNo10CmplNr2:
        sig_name = "BCFVPartNo10CmplNr2"
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

    class BCFVPartNo10CmplNr5:
        sig_name = "BCFVPartNo10CmplNr5"
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

    class BCFVPartNo10CmplNr4:
        sig_name = "BCFVPartNo10CmplNr4"
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

    class BCFVPartNo10CmplEndSgn1:
        sig_name = "BCFVPartNo10CmplEndSgn1"
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

    class BCFVPartNo10CmplEndSgn2:
        sig_name = "BCFVPartNo10CmplEndSgn2"
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


class AccmEcm_Lin1Fr03:
    msg_name = "AccmEcm_Lin1Fr03"
    msg_id = 18
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "ACCM"
    rx_nodes = ['ECM']
    sig_group_dict = {'CmprFb': ['CmprFbCmprI', 'CmprFbCmprIPha', 'CmprFbCmprSpd', 'CmprFbCmprSts1', 'CmprFbCmprSts2', 'CmprFbCmprT1', 'CmprFbCmprT2', 'CmprFbCmprU']}
    sig_group_dataid_dict = {}

    class CmprFbCmprU:
        sig_name = "CmprFbCmprU"
        sig_start_bit = 48
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 2.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 48
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b00000011, 0b11111100, 2, 0)]

    class CmprFbCmprIPha:
        sig_name = "CmprFbCmprIPha"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.5
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 254
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CmprFbCmprI:
        sig_name = "CmprFbCmprI"
        sig_start_bit = 32
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 32
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b00001111, 0b11110000, 4, 0)]

    class CmprFbCmprSpd:
        sig_name = "CmprFbCmprSpd"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 50.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 254
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 8
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CmprFbCmprT2:
        sig_name = "CmprFbCmprT2"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -50.0
        sig_value_min = 0
        sig_value_max = 254
        sig_byteorder = "Intel"
        sig_value_init = 50
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CmprFbCmprSts1:
        sig_name = "CmprFbCmprSts1"
        sig_start_bit = 59
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CmprSts_CmprOff': 0, 'CmprSts_CmprOn': 1, 'CmprSts_CmprPwrLimd': 2, 'CmprSts_CmprPreHeat': 3, 'CmprSts_Reserved1': 4, 'CmprSts_Reserved2': 5, 'CmprSts_Reserved3': 6, 'CmprSts_SigNotAvl': 7}
        compute_method = None
        length = 3
        startbit = 59
        byte = 7
        mask = 0b00111000
        unmask = 0b11000111
        shift = 3

    class CmprFbCmprT1:
        sig_name = "CmprFbCmprT1"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -50.0
        sig_value_min = 0
        sig_value_max = 254
        sig_byteorder = "Intel"
        sig_value_init = 50
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CmprFbCmprSts2:
        sig_name = "CmprFbCmprSts2"
        sig_start_bit = 44
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CompStat_NormalOperation': 0, 'CompStat_DegradedOperation': 1, 'CompStat_Inoperative': 2}
        compute_method = None
        length = 4
        startbit = 44
        byte = 5
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4


class EcmEcm_Lin1Fr03:
    msg_name = "EcmEcm_Lin1Fr03"
    msg_id = 34
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "ECM"
    rx_nodes = ['HVCH']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HvCooltHeatrEnad:
        sig_name = "HvCooltHeatrEnad"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 27
        byte = 3
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class CooltFlowInCmptmtCirc:
        sig_name = "CooltFlowInCmptmtCirc"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.05
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 16
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b00000011, 0b11111100, 2, 0)]

    class HvWtrHeatrPwrCnsAllwd:
        sig_name = "HvWtrHeatrPwrCnsAllwd"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 40.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvWtrHeatrWtrTDes:
        sig_name = "HvWtrHeatrWtrTDes"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Intel"
        sig_value_init = 40
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 8
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class HvchEcm_Lin1SerNrFr01:
    msg_name = "HvchEcm_Lin1SerNrFr01"
    msg_id = 37
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "HVCH"
    rx_nodes = ['ECM']
    sig_group_dict = {'HVCHSerNo': ['HVCHSerNoNr1', 'HVCHSerNoNr2', 'HVCHSerNoNr3', 'HVCHSerNoNr4']}
    sig_group_dataid_dict = {}

    class HVCHSerNoNr2:
        sig_name = "HVCHSerNoNr2"
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

    class HVCHSerNoNr3:
        sig_name = "HVCHSerNoNr3"
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

    class HVCHSerNoNr1:
        sig_name = "HVCHSerNoNr1"
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

    class HVCHSerNoNr4:
        sig_name = "HVCHSerNoNr4"
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


class BcfvEcm_Lin1SerNrFr01:
    msg_name = "BcfvEcm_Lin1SerNrFr01"
    msg_id = 44
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "BCFV"
    rx_nodes = ['ECM']
    sig_group_dict = {'BCFVSerNo': ['BCFVSerNoNr1', 'BCFVSerNoNr2', 'BCFVSerNoNr3', 'BCFVSerNoNr4']}
    sig_group_dataid_dict = {}

    class BCFVSerNoNr4:
        sig_name = "BCFVSerNoNr4"
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

    class BCFVSerNoNr3:
        sig_name = "BCFVSerNoNr3"
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

    class BCFVSerNoNr1:
        sig_name = "BCFVSerNoNr1"
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

    class BCFVSerNoNr2:
        sig_name = "BCFVSerNoNr2"
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


class BctvEcm_Lin1PartNrFr02:
    msg_name = "BctvEcm_Lin1PartNrFr02"
    msg_id = 40
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 7
    tx_node = "BCTV"
    rx_nodes = ['ECM']
    sig_group_dict = {'BCTVPartNoCmpl': ['BCTVPartNoCmplEndSgn1', 'BCTVPartNoCmplEndSgn2', 'BCTVPartNoCmplEndSgn3', 'BCTVPartNoCmplNr1', 'BCTVPartNoCmplNr2', 'BCTVPartNoCmplNr3', 'BCTVPartNoCmplNr4']}
    sig_group_dataid_dict = {}

    class BCTVPartNoCmplNr1:
        sig_name = "BCTVPartNoCmplNr1"
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

    class BCTVPartNoCmplEndSgn1:
        sig_name = "BCTVPartNoCmplEndSgn1"
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

    class BCTVPartNoCmplNr2:
        sig_name = "BCTVPartNoCmplNr2"
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

    class BCTVPartNoCmplEndSgn3:
        sig_name = "BCTVPartNoCmplEndSgn3"
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

    class BCTVPartNoCmplNr3:
        sig_name = "BCTVPartNoCmplNr3"
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

    class BCTVPartNoCmplNr4:
        sig_name = "BCTVPartNoCmplNr4"
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

    class BCTVPartNoCmplEndSgn2:
        sig_name = "BCTVPartNoCmplEndSgn2"
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


class HvchEcm_Lin1Fr02:
    msg_name = "HvchEcm_Lin1Fr02"
    msg_id = 23
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 3
    tx_node = "HVCH"
    rx_nodes = ['ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HvHeatrPwrCnsDes:
        sig_name = "HvHeatrPwrCnsDes"
        sig_start_bit = 10
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 20.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 10
        bmuws_info = [(1, 0b11111100, 0b00000011, 6, 2), (2, 0b00001111, 0b11110000, 4, 0)]

    class HvHeatrPwrCns:
        sig_name = "HvHeatrPwrCns"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 20.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 0
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b00000011, 0b11111100, 2, 0)]


class AccmEcm_Lin1PartNrFr01:
    msg_name = "AccmEcm_Lin1PartNrFr01"
    msg_id = 9
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "ACCM"
    rx_nodes = ['ECM']
    sig_group_dict = {'ACCMPartNo10Cmpl': ['ACCMPartNo10CmplEndSgn1', 'ACCMPartNo10CmplEndSgn2', 'ACCMPartNo10CmplEndSgn3', 'ACCMPartNo10CmplNr1', 'ACCMPartNo10CmplNr2', 'ACCMPartNo10CmplNr3', 'ACCMPartNo10CmplNr4', 'ACCMPartNo10CmplNr5']}
    sig_group_dataid_dict = {}

    class ACCMPartNo10CmplNr3:
        sig_name = "ACCMPartNo10CmplNr3"
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

    class ACCMPartNo10CmplNr2:
        sig_name = "ACCMPartNo10CmplNr2"
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

    class ACCMPartNo10CmplEndSgn2:
        sig_name = "ACCMPartNo10CmplEndSgn2"
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

    class ACCMPartNo10CmplNr4:
        sig_name = "ACCMPartNo10CmplNr4"
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

    class ACCMPartNo10CmplNr1:
        sig_name = "ACCMPartNo10CmplNr1"
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

    class ACCMPartNo10CmplNr5:
        sig_name = "ACCMPartNo10CmplNr5"
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

    class ACCMPartNo10CmplEndSgn1:
        sig_name = "ACCMPartNo10CmplEndSgn1"
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

    class ACCMPartNo10CmplEndSgn3:
        sig_name = "ACCMPartNo10CmplEndSgn3"
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


class HvahEcm_Lin1Fr02:
    msg_name = "HvahEcm_Lin1Fr02"
    msg_id = 22
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 6
    tx_node = "ETC"
    rx_nodes = ['ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class AirPtcPwrDerating:
        sig_name = "AirPtcPwrDerating"
        sig_start_bit = 29
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PTCPwrDerating_Reserved': 0, 'PTCPwrDerating_PCBovertempderatingpower': 1, 'PTCPwrDerating_IGBTovertempderatingpower': 2, 'PTCPwrDerating_COREovertempderatingpower': 3, 'PTCPwrDerating_SHUNTovertempderatingpower': 4}
        compute_method = None
        length = 3
        startbit = 29
        byte = 3
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class AirPtcPCBOvrTempFlt:
        sig_name = "AirPtcPCBOvrTempFlt"
        sig_start_bit = 38
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err1_NoErr': 0, 'Err1_Err': 1}
        compute_method = None
        length = 1
        startbit = 38
        byte = 4
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class AirPtcOCPTempSnsrFlt:
        sig_name = "AirPtcOCPTempSnsrFlt"
        sig_start_bit = 36
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err1_NoErr': 0, 'Err1_Err': 1}
        compute_method = None
        length = 1
        startbit = 36
        byte = 4
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class AirPtcPCBTempSnsrFlt:
        sig_name = "AirPtcPCBTempSnsrFlt"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err1_NoErr': 0, 'Err1_Err': 1}
        compute_method = None
        length = 1
        startbit = 39
        byte = 4
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class AirPtcOCPTempActl:
        sig_name = "AirPtcOCPTempActl"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Intel"
        sig_value_init = 40
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 8
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class AirPtcOCPOvrTempFlt:
        sig_name = "AirPtcOCPOvrTempFlt"
        sig_start_bit = 35
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err1_NoErr': 0, 'Err1_Err': 1}
        compute_method = None
        length = 1
        startbit = 35
        byte = 4
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class AirPtcPCBTempActl:
        sig_name = "AirPtcPCBTempActl"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Intel"
        sig_value_init = 40
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class AirPtcFlt:
        sig_name = "AirPtcFlt"
        sig_start_bit = 33
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
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

    class AirPtc15VDrvrFlt:
        sig_name = "AirPtc15VDrvrFlt"
        sig_start_bit = 32
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err1_NoErr': 0, 'Err1_Err': 1}
        compute_method = None
        length = 1
        startbit = 32
        byte = 4
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class AirPtcDutyFb:
        sig_name = "AirPtcDutyFb"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.5
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 200
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class AirPtcOvrCurrFlt:
        sig_name = "AirPtcOvrCurrFlt"
        sig_start_bit = 37
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err1_NoErr': 0, 'Err1_Err': 1}
        compute_method = None
        length = 1
        startbit = 37
        byte = 4
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class AirPtcLINTimeOutFlt:
        sig_name = "AirPtcLINTimeOutFlt"
        sig_start_bit = 34
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
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


class BcfvEcm_Lin1PartNrFr02:
    msg_name = "BcfvEcm_Lin1PartNrFr02"
    msg_id = 17
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 7
    tx_node = "BCFV"
    rx_nodes = ['ECM']
    sig_group_dict = {'BCFVPartNoCmpl': ['BCFVPartNoCmplEndSgn1', 'BCFVPartNoCmplEndSgn2', 'BCFVPartNoCmplEndSgn3', 'BCFVPartNoCmplNr1', 'BCFVPartNoCmplNr2', 'BCFVPartNoCmplNr3', 'BCFVPartNoCmplNr4']}
    sig_group_dataid_dict = {}

    class BCFVPartNoCmplEndSgn2:
        sig_name = "BCFVPartNoCmplEndSgn2"
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

    class BCFVPartNoCmplEndSgn3:
        sig_name = "BCFVPartNoCmplEndSgn3"
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

    class BCFVPartNoCmplNr3:
        sig_name = "BCFVPartNoCmplNr3"
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

    class BCFVPartNoCmplNr2:
        sig_name = "BCFVPartNoCmplNr2"
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

    class BCFVPartNoCmplNr1:
        sig_name = "BCFVPartNoCmplNr1"
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

    class BCFVPartNoCmplNr4:
        sig_name = "BCFVPartNoCmplNr4"
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

    class BCFVPartNoCmplEndSgn1:
        sig_name = "BCFVPartNoCmplEndSgn1"
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


class EcmEcm_Lin1Fr05:
    msg_name = "EcmEcm_Lin1Fr05"
    msg_id = 51
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 3
    tx_node = "ECM"
    rx_nodes = ['HVCH']
    sig_group_dict = {'HvCooltHeatrEnadWhE2E': ['HvCooltHeatrEnadWhE2EChks', 'HvCooltHeatrEnadWhE2ECntr', 'HvCooltHeatrEnadWhE2EHvchEnad']}
    sig_group_dataid_dict = {'HvCooltHeatrEnadWhE2E': 6001}

    class HvCooltHeatrEnadWhE2EChks:
        sig_name = "HvCooltHeatrEnadWhE2EChks"
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

    class HvCooltHeatrEnadWhE2EHvchEnad:
        sig_name = "HvCooltHeatrEnadWhE2EHvchEnad"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 12
        byte = 1
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class HvCooltHeatrEnadWhE2ECntr:
        sig_name = "HvCooltHeatrEnadWhE2ECntr"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 8
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0


class AccmEcm_Lin1SerNrFr01:
    msg_name = "AccmEcm_Lin1SerNrFr01"
    msg_id = 7
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "ACCM"
    rx_nodes = ['ECM']
    sig_group_dict = {'ACCMSerNo': ['ACCMSerNoNr1', 'ACCMSerNoNr2', 'ACCMSerNoNr3', 'ACCMSerNoNr4']}
    sig_group_dataid_dict = {}

    class ACCMSerNoNr2:
        sig_name = "ACCMSerNoNr2"
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

    class ACCMSerNoNr1:
        sig_name = "ACCMSerNoNr1"
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

    class ACCMSerNoNr4:
        sig_name = "ACCMSerNoNr4"
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

    class ACCMSerNoNr3:
        sig_name = "ACCMSerNoNr3"
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


class BcfvEcm_Lin1Fr01:
    msg_name = "BcfvEcm_Lin1Fr01"
    msg_id = 19
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "BCFV"
    rx_nodes = ['ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HpBattFwvFltSts:
        sig_name = "HpBattFwvFltSts"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FaultSts_NoError': 0, 'FaultSts_PositionUnknown': 1, 'FaultSts_PCTR_Error': 2, 'FaultSts_Blocking_Err': 3, 'FaultSts_SetPoint_Err': 4, 'FaultSts_Learning_Err': 5, 'FaultSts_MotorCoilShort': 6, 'FaultSts_MotorCoilOpen': 7, 'FaultSts_MotorDrvOvertemperatureShutdown': 8, 'FaultSts_Indeterminate': 9, 'FaultSts_Reserved': 10, 'FaultSts_SNA': 15}
        compute_method = None
        length = 4
        startbit = 0
        byte = 0
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class HpBattFwvVoltSts:
        sig_name = "HpBattFwvVoltSts"
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
        sig_value_table = {'VoltSts_VoltageOK': 0, 'VoltSts_OverVoltage': 1, 'VoltSts_UnderVoltage': 2, 'VoltSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 24
        byte = 3
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class HpBattFwvPosRec:
        sig_name = "HpBattFwvPosRec"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 8
        bmuws_info = [(1, 0b11111111, 0b00000000, 8, 0), (2, 0b00000011, 0b11111100, 2, 0)]

    class BcfvNVMFlt:
        sig_name = "BcfvNVMFlt"
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
        sig_value_table = {'Flt_NoFault': 0, 'Flt_Fault': 1}
        compute_method = None
        length = 1
        startbit = 27
        byte = 3
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class HpBattFwvSpdLvl:
        sig_name = "HpBattFwvSpdLvl"
        sig_start_bit = 19
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SpeedLvl_SpeedLevelLow': 0, 'SpeedLvl_SpeedLevelNormal': 1, 'SpeedLvl_SpeedLevelFast': 2, 'SpeedLvl_SNA': 3}
        compute_method = None
        length = 2
        startbit = 19
        byte = 2
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class HpBattFwvRunSts:
        sig_name = "HpBattFwvRunSts"
        sig_start_bit = 18
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VlvRunSts_NotMoving': 0, 'VlvRunSts_Moving': 1}
        compute_method = None
        length = 1
        startbit = 18
        byte = 2
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class HpBattFwvTempSts:
        sig_name = "HpBattFwvTempSts"
        sig_start_bit = 21
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TempSts_Temperatureok': 0, 'TempSts_OvertemperatureWarning': 1, 'TempSts_PCBOvertemperature': 2, 'TempSts_LowTemperature': 3, 'TempSts_notused': 4, 'TempSts_SNA': 7}
        compute_method = None
        length = 3
        startbit = 21
        byte = 2
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class HpBattFwvMode:
        sig_name = "HpBattFwvMode"
        sig_start_bit = 4
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VlvMode_NormalOperation': 0, 'VlvMode_Mot_Off': 1, 'VlvMode_Learning': 2, 'VlvMode_Fail_Safe': 3, 'VlvMode_SNA': 15}
        compute_method = None
        length = 4
        startbit = 4
        byte = 0
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4


class DiagResponse7:
    msg_name = "DiagResponse7"
    msg_id = 61
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class HvahEcm_Lin1Fr01:
    msg_name = "HvahEcm_Lin1Fr01"
    msg_id = 20
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "ETC"
    rx_nodes = ['ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class AirPtcIgbt1OvrTempFlt:
        sig_name = "AirPtcIgbt1OvrTempFlt"
        sig_start_bit = 60
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err1_NoErr': 0, 'Err1_Err': 1}
        compute_method = None
        length = 1
        startbit = 60
        byte = 7
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class AirPtcHVLowFlt:
        sig_name = "AirPtcHVLowFlt"
        sig_start_bit = 58
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err1_NoErr': 0, 'Err1_Err': 1}
        compute_method = None
        length = 1
        startbit = 58
        byte = 7
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class AirPtcIgbtShrtFlt:
        sig_name = "AirPtcIgbtShrtFlt"
        sig_start_bit = 54
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err1_NoErr': 0, 'Err1_Err': 1}
        compute_method = None
        length = 1
        startbit = 54
        byte = 6
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class AirPtcIgbt1TempActl:
        sig_name = "AirPtcIgbt1TempActl"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Intel"
        sig_value_init = 40
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class AirPtcHVPwrActl:
        sig_name = "AirPtcHVPwrActl"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 20
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 8
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class AirPtcIgbt2TempActl:
        sig_name = "AirPtcIgbt2TempActl"
        sig_start_bit = 32
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Intel"
        sig_value_init = 40
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 32
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class AirPtcHVVoltActl:
        sig_name = "AirPtcHVVoltActl"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.5
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 40
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b00000011, 0b11111100, 2, 0)]

    class AirPtcIgbt1TempSnsrFlt:
        sig_name = "AirPtcIgbt1TempSnsrFlt"
        sig_start_bit = 61
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err1_NoErr': 0, 'Err1_Err': 1}
        compute_method = None
        length = 1
        startbit = 61
        byte = 7
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class AirPtcHVCurrActl:
        sig_name = "AirPtcHVCurrActl"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.2
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 254
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class AirPtcHVSnsrFlt:
        sig_name = "AirPtcHVSnsrFlt"
        sig_start_bit = 59
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err1_NoErr': 0, 'Err1_Err': 1}
        compute_method = None
        length = 1
        startbit = 59
        byte = 7
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class AirPtcIgbt2OvrTempFlt:
        sig_name = "AirPtcIgbt2OvrTempFlt"
        sig_start_bit = 62
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err1_NoErr': 0, 'Err1_Err': 1}
        compute_method = None
        length = 1
        startbit = 62
        byte = 7
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class AirPtcHVCurrSnsrFlt:
        sig_name = "AirPtcHVCurrSnsrFlt"
        sig_start_bit = 56
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err1_NoErr': 0, 'Err1_Err': 1}
        compute_method = None
        length = 1
        startbit = 56
        byte = 7
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class AirPtcIgbt2TempSnsrFlt:
        sig_name = "AirPtcIgbt2TempSnsrFlt"
        sig_start_bit = 63
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err1_NoErr': 0, 'Err1_Err': 1}
        compute_method = None
        length = 1
        startbit = 63
        byte = 7
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class AirPtcHVHighFlt:
        sig_name = "AirPtcHVHighFlt"
        sig_start_bit = 57
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err1_NoErr': 0, 'Err1_Err': 1}
        compute_method = None
        length = 1
        startbit = 57
        byte = 7
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class AirPtcIgbtDrvrFlt:
        sig_name = "AirPtcIgbtDrvrFlt"
        sig_start_bit = 55
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err1_NoErr': 0, 'Err1_Err': 1}
        compute_method = None
        length = 1
        startbit = 55
        byte = 6
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7


class AccmEcm_Lin1Fr02:
    msg_name = "AccmEcm_Lin1Fr02"
    msg_id = 53
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "ACCM"
    rx_nodes = ['ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class CmprSpdIncrReq:
        sig_name = "CmprSpdIncrReq"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Validity_NotValid': 0, 'Validity_Valid': 1}
        compute_method = None
        length = 1
        startbit = 23
        byte = 2
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class CmprLostCommStat:
        sig_name = "CmprLostCommStat"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flt_NoFault': 0, 'Flt_Fault': 1}
        compute_method = None
        length = 1
        startbit = 16
        byte = 2
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class CmprRotorLockStat:
        sig_name = "CmprRotorLockStat"
        sig_start_bit = 25
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flt_NoFault': 0, 'Flt_Fault': 1}
        compute_method = None
        length = 1
        startbit = 25
        byte = 3
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class CmprEEPROMFault:
        sig_name = "CmprEEPROMFault"
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
        sig_value_table = {'Flt_NoFault': 0, 'Flt_Fault': 1}
        compute_method = None
        length = 1
        startbit = 10
        byte = 1
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class CmprMotorCurrOverCurrStat:
        sig_name = "CmprMotorCurrOverCurrStat"
        sig_start_bit = 17
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flt_NoFault': 0, 'Flt_Fault': 1}
        compute_method = None
        length = 1
        startbit = 17
        byte = 2
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class CmprRAMFault:
        sig_name = "CmprRAMFault"
        sig_start_bit = 18
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flt_NoFault': 0, 'Flt_Fault': 1}
        compute_method = None
        length = 1
        startbit = 18
        byte = 2
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class CmprInCurrOverCurrStat:
        sig_name = "CmprInCurrOverCurrStat"
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
        sig_value_table = {'Flt_NoFault': 0, 'Flt_Fault': 1}
        compute_method = None
        length = 1
        startbit = 14
        byte = 1
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class CmprOverMotorCurrStat:
        sig_name = "CmprOverMotorCurrStat"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CompOverMotorCurrStat_Normal': 0, 'CompOverMotorCurrStat_ImmediatelyShutdown': 1, 'CompOverMotorCurrStat_SpeedIncreased': 2, 'CompOverMotorCurrStat_SpeedDecreased': 3, 'CompOverMotorCurrStat_Shutdown': 4}
        compute_method = None
        length = 4
        startbit = 0
        byte = 0
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class CmprHVoltResonanceStat:
        sig_name = "CmprHVoltResonanceStat"
        sig_start_bit = 11
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AcHVoltResonanceStat_Normal': 0, 'AcHVoltResonanceStat_SpeedDecreased': 1, 'AcHVoltResonanceStat_Inoperative': 2, 'AcHVoltResonanceStat_Reserved': 3}
        compute_method = None
        length = 3
        startbit = 11
        byte = 1
        mask = 0b00111000
        unmask = 0b11000111
        shift = 3

    class CmprOverPowerStat:
        sig_name = "CmprOverPowerStat"
        sig_start_bit = 4
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CompOverPowerStat_Normal': 0, 'CompOverPowerStat_SpeedDecreasedforOverPower': 1, 'CompOverPowerStat_SpeedDecreasedforOverCurrent': 2, 'CompOverPowerStat_InoperativeforOverPower': 3, 'CompOverPowerStat_InoperativeforOverCurrent': 4}
        compute_method = None
        length = 4
        startbit = 4
        byte = 0
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class CmprROMFault:
        sig_name = "CmprROMFault"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flt_NoFault': 0, 'Flt_Fault': 1}
        compute_method = None
        length = 1
        startbit = 24
        byte = 3
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class CmprLiquidSluggingStat:
        sig_name = "CmprLiquidSluggingStat"
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
        sig_value_table = {'Flt_NoFault': 0, 'Flt_Fault': 1}
        compute_method = None
        length = 1
        startbit = 15
        byte = 1
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7


class HvchEcm_Lin1Fr01:
    msg_name = "HvchEcm_Lin1Fr01"
    msg_id = 39
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 7
    tx_node = "HVCH"
    rx_nodes = ['ECM']
    sig_group_dict = {'HvCooltHeatrSnsrFltSig': ['HvCooltHeatrSnsrFltSigCooltTInSnsrFlt', 'HvCooltHeatrSnsrFltSigCooltTOutSnsrFlt', 'HvCooltHeatrSnsrFltSigResdForSnsrFlt', 'HvCooltHeatrSnsrFltSigTInMtrlSnsrFlt'], 'HvCooltHeatrWarnSig': ['HvCooltHeatrWarnSigCooltTOutOfRng', 'HvCooltHeatrWarnSigFltInCom', 'HvCooltHeatrWarnSigFltPrsnt', 'HvCooltHeatrWarnSigFltPrsntResd', 'HvCooltHeatrWarnSigHvOutOfRng', 'HvCooltHeatrWarnSigULoOutOfRng'], 'HvCooltHeatrProtnOfSelfTmpSig': ['HvCooltHeatrProtnOfSelfTmpSigHwProtn', 'HvCooltHeatrProtnOfSelfTmpSigOvrheatg', 'HvCooltHeatrProtnOfSelfTmpSigProtnOfSelfTmp', 'HvCooltHeatrProtnOfSelfTmpSigProtnOfSelfTmpResd'], 'HvCooltHeatrSrvRqrdSig': ['HvCooltHeatrSrvRqrdSigCircForDrvrShoOrOpen', 'HvCooltHeatrSrvRqrdSigICnsOutOfRng', 'HvCooltHeatrSrvRqrdSigMemErr', 'HvCooltHeatrSrvRqrdSigSrvRqrd', 'HvCooltHeatrSrvRqrdSigSrvRqrdResd']}
    sig_group_dataid_dict = {}

    class HvCooltHeatrProtnOfSelfTmpSigHwProtn:
        sig_name = "HvCooltHeatrProtnOfSelfTmpSigHwProtn"
        sig_start_bit = 48
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 48
        byte = 6
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class HvCooltHeatrSrvRqrdSigCircForDrvrShoOrOpen:
        sig_name = "HvCooltHeatrSrvRqrdSigCircForDrvrShoOrOpen"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
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

    class HvCooltHeatrWarnSigULoOutOfRng:
        sig_name = "HvCooltHeatrWarnSigULoOutOfRng"
        sig_start_bit = 45
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 45
        byte = 5
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class HvCooltHeatrProtnOfSelfTmpSigProtnOfSelfTmpResd:
        sig_name = "HvCooltHeatrProtnOfSelfTmpSigProtnOfSelfTmpResd"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 51
        byte = 6
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class HvCooltHeatrStsSig:
        sig_name = "HvCooltHeatrStsSig"
        sig_start_bit = 5
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvCooltHeatrSts_Off': 0, 'HvCooltHeatrSts_LockedUntilNextStart': 1, 'HvCooltHeatrSts_LockedUntilService': 2, 'HvCooltHeatrSts_LockedPermanent': 3, 'HvCooltHeatrSts_Operation': 4, 'HvCooltHeatrSts_Reserved1': 5, 'HvCooltHeatrSts_Reserved2': 6, 'HvCooltHeatrSts_Reserved3': 7}
        compute_method = None
        length = 3
        startbit = 5
        byte = 0
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class HvCooltHeatrSrvRqrdSigSrvRqrdResd:
        sig_name = "HvCooltHeatrSrvRqrdSigSrvRqrdResd"
        sig_start_bit = 4
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
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

    class HvCooltHeatrSrvRqrdSigSrvRqrd:
        sig_name = "HvCooltHeatrSrvRqrdSigSrvRqrd"
        sig_start_bit = 3
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
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

    class HvCooltHeatrSnsrFltSigResdForSnsrFlt:
        sig_name = "HvCooltHeatrSnsrFltSigResdForSnsrFlt"
        sig_start_bit = 54
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 54
        byte = 6
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class HvCooltHeatrWarnSigFltInCom:
        sig_name = "HvCooltHeatrWarnSigFltInCom"
        sig_start_bit = 41
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
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

    class HvCooltHeatrSrvRqrdSigICnsOutOfRng:
        sig_name = "HvCooltHeatrSrvRqrdSigICnsOutOfRng"
        sig_start_bit = 1
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
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

    class HvCooltHeatrSnsrFltSigCooltTOutSnsrFlt:
        sig_name = "HvCooltHeatrSnsrFltSigCooltTOutSnsrFlt"
        sig_start_bit = 53
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 53
        byte = 6
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class HvCooltHeatrSplyUForCtrlUnitValSig:
        sig_name = "HvCooltHeatrSplyUForCtrlUnitValSig"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvCooltHeatrICnsSig:
        sig_name = "HvCooltHeatrICnsSig"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.25
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvCooltHeatrProtnOfSelfTmpSigOvrheatg:
        sig_name = "HvCooltHeatrProtnOfSelfTmpSigOvrheatg"
        sig_start_bit = 49
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
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

    class HvCooltHeatrWarnSigCooltTOutOfRng:
        sig_name = "HvCooltHeatrWarnSigCooltTOutOfRng"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 40
        byte = 5
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class HvCooltHeatrSnsrFltSigCooltTInSnsrFlt:
        sig_name = "HvCooltHeatrSnsrFltSigCooltTInSnsrFlt"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class HvCooltHeatrSrvRqrdSigMemErr:
        sig_name = "HvCooltHeatrSrvRqrdSigMemErr"
        sig_start_bit = 2
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
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

    class HvCooltWtrHeatrWtrTInOutl:
        sig_name = "HvCooltWtrHeatrWtrTInOutl"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Intel"
        sig_value_init = 40
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 8
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvCooltHeatrWarnSigHvOutOfRng:
        sig_name = "HvCooltHeatrWarnSigHvOutOfRng"
        sig_start_bit = 44
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 44
        byte = 5
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class HvCooltWtrHeatrWtrTInIntk:
        sig_name = "HvCooltWtrHeatrWtrTInIntk"
        sig_start_bit = 32
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Intel"
        sig_value_init = 40
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 32
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvCooltHeatrProtnOfSelfTmpSigProtnOfSelfTmp:
        sig_name = "HvCooltHeatrProtnOfSelfTmpSigProtnOfSelfTmp"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 50
        byte = 6
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class HvCooltHeatrWarnSigFltPrsntResd:
        sig_name = "HvCooltHeatrWarnSigFltPrsntResd"
        sig_start_bit = 43
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 43
        byte = 5
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class HvCooltHeatrWarnSigFltPrsnt:
        sig_name = "HvCooltHeatrWarnSigFltPrsnt"
        sig_start_bit = 42
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
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

    class HvCooltHeatrInfoCompProtn:
        sig_name = "HvCooltHeatrInfoCompProtn"
        sig_start_bit = 46
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
        startbit = 46
        byte = 5
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class HvCooltHeatrSnsrFltSigTInMtrlSnsrFlt:
        sig_name = "HvCooltHeatrSnsrFltSigTInMtrlSnsrFlt"
        sig_start_bit = 55
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 55
        byte = 6
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7


class AccmEcm_Lin1PartNrFr02:
    msg_name = "AccmEcm_Lin1PartNrFr02"
    msg_id = 16
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 7
    tx_node = "ACCM"
    rx_nodes = ['ECM']
    sig_group_dict = {'ACCMPartNoCmpl': ['ACCMPartNoCmplEndSgn1', 'ACCMPartNoCmplEndSgn2', 'ACCMPartNoCmplEndSgn3', 'ACCMPartNoCmplNr1', 'ACCMPartNoCmplNr2', 'ACCMPartNoCmplNr3', 'ACCMPartNoCmplNr4']}
    sig_group_dataid_dict = {}

    class ACCMPartNoCmplNr3:
        sig_name = "ACCMPartNoCmplNr3"
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

    class ACCMPartNoCmplEndSgn2:
        sig_name = "ACCMPartNoCmplEndSgn2"
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

    class ACCMPartNoCmplEndSgn3:
        sig_name = "ACCMPartNoCmplEndSgn3"
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

    class ACCMPartNoCmplNr4:
        sig_name = "ACCMPartNoCmplNr4"
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

    class ACCMPartNoCmplNr1:
        sig_name = "ACCMPartNoCmplNr1"
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

    class ACCMPartNoCmplNr2:
        sig_name = "ACCMPartNoCmplNr2"
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

    class ACCMPartNoCmplEndSgn1:
        sig_name = "ACCMPartNoCmplEndSgn1"
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


class BctvEcm_Lin1PartNrFr01:
    msg_name = "BctvEcm_Lin1PartNrFr01"
    msg_id = 24
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "BCTV"
    rx_nodes = ['ECM']
    sig_group_dict = {'BCTVPartNo10Cmpl': ['BCTVPartNo10CmplEndSgn1', 'BCTVPartNo10CmplEndSgn2', 'BCTVPartNo10CmplEndSgn3', 'BCTVPartNo10CmplNr1', 'BCTVPartNo10CmplNr2', 'BCTVPartNo10CmplNr3', 'BCTVPartNo10CmplNr4', 'BCTVPartNo10CmplNr5']}
    sig_group_dataid_dict = {}

    class BCTVPartNo10CmplNr1:
        sig_name = "BCTVPartNo10CmplNr1"
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

    class BCTVPartNo10CmplNr2:
        sig_name = "BCTVPartNo10CmplNr2"
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

    class BCTVPartNo10CmplNr5:
        sig_name = "BCTVPartNo10CmplNr5"
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

    class BCTVPartNo10CmplNr3:
        sig_name = "BCTVPartNo10CmplNr3"
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

    class BCTVPartNo10CmplEndSgn3:
        sig_name = "BCTVPartNo10CmplEndSgn3"
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

    class BCTVPartNo10CmplEndSgn1:
        sig_name = "BCTVPartNo10CmplEndSgn1"
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

    class BCTVPartNo10CmplEndSgn2:
        sig_name = "BCTVPartNo10CmplEndSgn2"
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

    class BCTVPartNo10CmplNr4:
        sig_name = "BCTVPartNo10CmplNr4"
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


class HvchEcm_Lin1PartNr10Fr04:
    msg_name = "HvchEcm_Lin1PartNr10Fr04"
    msg_id = 32
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "HVCH"
    rx_nodes = ['ECM']
    sig_group_dict = {'HVCHPartNo10Cmpl': ['HVCHPartNo10CmplEndSgn1', 'HVCHPartNo10CmplEndSgn2', 'HVCHPartNo10CmplEndSgn3', 'HVCHPartNo10CmplNr1', 'HVCHPartNo10CmplNr2', 'HVCHPartNo10CmplNr3', 'HVCHPartNo10CmplNr4', 'HVCHPartNo10CmplNr5']}
    sig_group_dataid_dict = {}

    class HVCHPartNo10CmplEndSgn1:
        sig_name = "HVCHPartNo10CmplEndSgn1"
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

    class HVCHPartNo10CmplNr5:
        sig_name = "HVCHPartNo10CmplNr5"
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

    class HVCHPartNo10CmplEndSgn3:
        sig_name = "HVCHPartNo10CmplEndSgn3"
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

    class HVCHPartNo10CmplNr2:
        sig_name = "HVCHPartNo10CmplNr2"
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

    class HVCHPartNo10CmplNr4:
        sig_name = "HVCHPartNo10CmplNr4"
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

    class HVCHPartNo10CmplEndSgn2:
        sig_name = "HVCHPartNo10CmplEndSgn2"
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

    class HVCHPartNo10CmplNr1:
        sig_name = "HVCHPartNo10CmplNr1"
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

    class HVCHPartNo10CmplNr3:
        sig_name = "HVCHPartNo10CmplNr3"
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


class DiagRequest7:
    msg_name = "DiagRequest7"
    msg_id = 60
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = []
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class HvchEcm_Lin1PartNr10Fr08:
    msg_name = "HvchEcm_Lin1PartNr10Fr08"
    msg_id = 38
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 7
    tx_node = "HVCH"
    rx_nodes = ['ECM']
    sig_group_dict = {'HVCHPartNoCmpl': ['HVCHPartNoCmplEndSgn1', 'HVCHPartNoCmplEndSgn2', 'HVCHPartNoCmplEndSgn3', 'HVCHPartNoCmplNr1', 'HVCHPartNoCmplNr2', 'HVCHPartNoCmplNr3', 'HVCHPartNoCmplNr4']}
    sig_group_dataid_dict = {}

    class HVCHPartNoCmplEndSgn2:
        sig_name = "HVCHPartNoCmplEndSgn2"
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

    class HVCHPartNoCmplEndSgn1:
        sig_name = "HVCHPartNoCmplEndSgn1"
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

    class HVCHPartNoCmplNr2:
        sig_name = "HVCHPartNoCmplNr2"
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

    class HVCHPartNoCmplEndSgn3:
        sig_name = "HVCHPartNoCmplEndSgn3"
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

    class HVCHPartNoCmplNr4:
        sig_name = "HVCHPartNoCmplNr4"
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

    class HVCHPartNoCmplNr3:
        sig_name = "HVCHPartNoCmplNr3"
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

    class HVCHPartNoCmplNr1:
        sig_name = "HVCHPartNoCmplNr1"
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


class EcmEcm_Lin1Fr01:
    msg_name = "EcmEcm_Lin1Fr01"
    msg_id = 8
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['ECRV', 'BCTV', 'BCFV']
    sig_group_dict = {'EctvCmd': ['EctvCmdVlvMovEna', 'EctvCmdVlvPosSetReq', 'EctvCmdVlvSpdLvlReq']}
    sig_group_dataid_dict = {}

    class HpBattFwvPosSetReq:
        sig_name = "HpBattFwvPosSetReq"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class EctvCmdVlvPosSetReq:
        sig_name = "EctvCmdVlvPosSetReq"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 21
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VlvPosSetReq_MovetofullClosePosition': 0, 'VlvPosSetReq_MovetoLevel1OpenPosition': 1, 'VlvPosSetReq_MovetoLevel2OpenPosition': 2, 'VlvPosSetReq_MovetoLevel3OpenPosition': 3, 'VlvPosSetReq_MovetoLevel4OpenPosition': 4, 'VlvPosSetReq_MovetoLevel5OpenPosition': 5, 'VlvPosSetReq_MovetoLevel6OpenPosition': 6, 'VlvPosSetReq_MovetoLevel7OpenPosition': 7, 'VlvPosSetReq_MovetoLevel8OpenPosition': 8, 'VlvPosSetReq_MovetoLevel9OpenPosition': 9, 'VlvPosSetReq_MovetoLevel10OpenPosition': 10, 'VlvPosSetReq_MovetoLevel11OpenPosition': 11, 'VlvPosSetReq_MovetoLevel12OpenPosition': 12, 'VlvPosSetReq_MovetoLevel13OpenPosition': 13, 'VlvPosSetReq_MovetoLevel14OpenPosition': 14, 'VlvPosSetReq_MovetoLevel15OpenPosition': 15, 'VlvPosSetReq_MovetoLevel16OpenPosition': 16, 'VlvPosSetReq_MovetoLevel17OpenPosition': 17, 'VlvPosSetReq_MovetoLevel18OpenPosition': 18, 'VlvPosSetReq_MovetoLevel19OpenPosition': 19, 'VlvPosSetReq_MovetofullOpenPosition': 20, 'VlvPosSetReq_Reserved': 21}
        compute_method = None
        length = 5
        startbit = 8
        byte = 1
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class EctvCmdVlvMovEna:
        sig_name = "EctvCmdVlvMovEna"
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
        sig_value_table = {'MoveDisable': 0, 'MoveEnable': 1}
        compute_method = None
        length = 1
        startbit = 13
        byte = 1
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class EctvCmdVlvSpdLvlReq:
        sig_name = "EctvCmdVlvSpdLvlReq"
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
        sig_value_table = {'VlvSpdLvlReq_Invalid': 0, 'VlvSpdLvlReq_Level1': 1, 'VlvSpdLvlReq_Level2': 2, 'VlvSpdLvlReq_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 14
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HpBattVlvPosSetReq:
        sig_name = "HpBattVlvPosSetReq"
        sig_start_bit = 32
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 32
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HpBattVlvActvSaveReq:
        sig_name = "HpBattVlvActvSaveReq"
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
        sig_value_table = {'ActiveSaveReq_NoReq': 0, 'ActiveSaveReq_ActiveSave_Req': 1, 'ActiveSaveReq_Reserved': 2, 'ActiveSaveReq_SNA': 3}
        compute_method = None
        length = 2
        startbit = 6
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HpBattVlvRefDrvReq:
        sig_name = "HpBattVlvRefDrvReq"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'RefDrvReq_NoReq': 0, 'RefDrvReq_REFDRV_Req': 1, 'RefDrvReq_Reserved': 2, 'RefDrvReq_SNA': 3}
        compute_method = None
        length = 2
        startbit = 40
        byte = 5
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class HpBattVlvSpdLvlReq:
        sig_name = "HpBattVlvSpdLvlReq"
        sig_start_bit = 42
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SpdLvlReq_Level0_Slow': 0, 'SpdLvlReq_Level1_Normal': 1, 'SpdLvlReq_Level2_Fast': 2, 'SpdLvlReq_SNA': 3}
        compute_method = None
        length = 2
        startbit = 42
        byte = 5
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class HpBattFwvRefDrvReq:
        sig_name = "HpBattFwvRefDrvReq"
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
        sig_value_table = {'RefDrvReq_NoReq': 0, 'RefDrvReq_REFDRV_Req': 1, 'RefDrvReq_Reserved': 2, 'RefDrvReq_SNA': 3}
        compute_method = None
        length = 2
        startbit = 2
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class HpBattFwvSpdLvlReq:
        sig_name = "HpBattFwvSpdLvlReq"
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
        sig_value_table = {'SpdLvlReq_Level0_Slow': 0, 'SpdLvlReq_Level1_Normal': 1, 'SpdLvlReq_Level2_Fast': 2, 'SpdLvlReq_SNA': 3}
        compute_method = None
        length = 2
        startbit = 4
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class HpBattFwvActvSaveReq:
        sig_name = "HpBattFwvActvSaveReq"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ActiveSaveReq_NoReq': 0, 'ActiveSaveReq_ActiveSave_Req': 1, 'ActiveSaveReq_Reserved': 2, 'ActiveSaveReq_SNA': 3}
        compute_method = None
        length = 2
        startbit = 0
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0


class EcmEcm_Lin1Fr02:
    msg_name = "EcmEcm_Lin1Fr02"
    msg_id = 48
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 7
    tx_node = "ECM"
    rx_nodes = ['ACCM', 'ETC']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class CmprReqCmprSpdReq:
        sig_name = "CmprReqCmprSpdReq"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 50.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 254
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 8
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class AirPtcHvPwrReq:
        sig_name = "AirPtcHvPwrReq"
        sig_start_bit = 48
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 20
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 48
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CmprReqCmprRunReq:
        sig_name = "CmprReqCmprRunReq"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CmprRunReq_CmprOff': 0, 'CmprRunReq_CmprOn': 1, 'CmprRunReq_Resd': 2, 'CmprRunReq_SigNotAvl': 3}
        compute_method = None
        length = 2
        startbit = 16
        byte = 2
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class CmprReqCmprPwrLim:
        sig_name = "CmprReqCmprPwrLim"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 40.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class AirPtcEnad:
        sig_name = "AirPtcEnad"
        sig_start_bit = 32
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 32
        byte = 4
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class AirPtcDutyReq:
        sig_name = "AirPtcDutyReq"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.5
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 200
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 40
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class AirPtcModeReq:
        sig_name = "AirPtcModeReq"
        sig_start_bit = 33
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PTCModeReq_Power': 0, 'PTCModeReq_Duty': 1, 'PTCModeReq_Direct': 2}
        compute_method = None
        length = 2
        startbit = 33
        byte = 4
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1


