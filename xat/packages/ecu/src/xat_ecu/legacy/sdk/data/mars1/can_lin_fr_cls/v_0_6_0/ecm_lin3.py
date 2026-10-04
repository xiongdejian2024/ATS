class CexvEcm_Lin3PartNrFr04:
    msg_name = "CexvEcm_Lin3PartNrFr04"
    msg_id = 16
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 8
    tx_node = "CEXV"
    rx_nodes = ['ECM']

    class CEXVPartNo10CmplNr2:
        sig_name = "CEXVPartNo10CmplNr2"
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

    class CEXVPartNo10CmplEndSgn3:
        sig_name = "CEXVPartNo10CmplEndSgn3"
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

    class CEXVPartNo10CmplNr5:
        sig_name = "CEXVPartNo10CmplNr5"
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

    class CEXVPartNo10CmplNr4:
        sig_name = "CEXVPartNo10CmplNr4"
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

    class CEXVPartNo10CmplEndSgn2:
        sig_name = "CEXVPartNo10CmplEndSgn2"
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

    class CEXVPartNo10CmplNr1:
        sig_name = "CEXVPartNo10CmplNr1"
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

    class CEXVPartNo10CmplEndSgn1:
        sig_name = "CEXVPartNo10CmplEndSgn1"
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

    class CEXVPartNo10CmplNr3:
        sig_name = "CEXVPartNo10CmplNr3"
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


class BexvEcm_Lin3Fr01:
    msg_name = "BexvEcm_Lin3Fr01"
    msg_id = 31
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 7
    tx_node = "BEXV"
    rx_nodes = ['ECM']

    class BexvNVMFlt:
        sig_name = "BexvNVMFlt"
        sig_start_bit = 22
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
        startbit = 22
        byte = 2
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class BexvStsExvPreHeatgSts:
        sig_name = "BexvStsExvPreHeatgSts"
        sig_start_bit = 19
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
        startbit = 19
        byte = 2
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class BexvStsExvBlkErr:
        sig_name = "BexvStsExvBlkErr"
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
        sig_value_table = {'Err1_NoErr': 0, 'Err1_Err': 1}
        compute_method = None
        length = 1
        startbit = 10
        byte = 1
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class BexvStsExvOvrTrvlErr:
        sig_name = "BexvStsExvOvrTrvlErr"
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
        sig_value_table = {'Err1_NoErr': 0, 'Err1_Err': 1}
        compute_method = None
        length = 1
        startbit = 18
        byte = 2
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class BexvStsExvActrPosn:
        sig_name = "BexvStsExvActrPosn"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.2
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 500
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 0
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b00000011, 0b11111100, 2, 0)]

    class BexvStsExvOvrTempErr:
        sig_name = "BexvStsExvOvrTempErr"
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
        sig_value_table = {'Err1_NoErr': 0, 'Err1_Err': 1}
        compute_method = None
        length = 1
        startbit = 17
        byte = 2
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class BexvStsExvCalibSts:
        sig_name = "BexvStsExvCalibSts"
        sig_start_bit = 11
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
        startbit = 11
        byte = 1
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class BexvStsExvVoltgRangErr:
        sig_name = "BexvStsExvVoltgRangErr"
        sig_start_bit = 20
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VoltgRangErr_NoErr': 0, 'VoltgRangErr_UnderVoltageErr': 1, 'VoltgRangErr_OverVoltageErr': 2, 'VoltgRangErr_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 20
        byte = 2
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class BexvStsExvMovSts:
        sig_name = "BexvStsExvMovSts"
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
        sig_value_table = {'ExvMovSts_NotMove': 0, 'ExvMovSts_Moving': 1}
        compute_method = None
        length = 1
        startbit = 16
        byte = 2
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class BexvStsExvElecStsErr:
        sig_name = "BexvStsExvElecStsErr"
        sig_start_bit = 13
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
        startbit = 13
        byte = 1
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5


class EcmEcm_Lin3Fr05:
    msg_name = "EcmEcm_Lin3Fr05"
    msg_id = 6
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 7
    tx_node = "ECM"
    rx_nodes = ['ETC']

    class SecDcDcActvdReq:
        sig_name = "SecDcDcActvdReq"
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
        sig_value_table = {'DcDcActvd_NoConversionToLVSide': 0, 'DcDcActvd_ConversionToLVSide': 1}
        compute_method = None
        length = 1
        startbit = 38
        byte = 4
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class HvConvSecPwrAllwd:
        sig_name = "HvConvSecPwrAllwd"
        sig_start_bit = 44
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 20.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Intel"
        sig_value_init = 35
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 44
        bmuws_info = [(5, 0b11110000, 0b00001111, 4, 4), (6, 0b00111111, 0b11000000, 6, 0)]


class CexvEcm_Lin3Fr01:
    msg_name = "CexvEcm_Lin3Fr01"
    msg_id = 14
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 7
    tx_node = "CEXV"
    rx_nodes = ['ECM']

    class CexvStsExvBlkErr:
        sig_name = "CexvStsExvBlkErr"
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
        sig_value_table = {'Err1_NoErr': 0, 'Err1_Err': 1}
        compute_method = None
        length = 1
        startbit = 10
        byte = 1
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class CexvStsExvOvrTrvlErr:
        sig_name = "CexvStsExvOvrTrvlErr"
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
        sig_value_table = {'Err1_NoErr': 0, 'Err1_Err': 1}
        compute_method = None
        length = 1
        startbit = 18
        byte = 2
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class CexvStsExvMovSts:
        sig_name = "CexvStsExvMovSts"
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
        sig_value_table = {'ExvMovSts_NotMove': 0, 'ExvMovSts_Moving': 1}
        compute_method = None
        length = 1
        startbit = 16
        byte = 2
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class CexvStsExvCalibSts:
        sig_name = "CexvStsExvCalibSts"
        sig_start_bit = 11
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
        startbit = 11
        byte = 1
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class CexvStsExvVoltgRangErr:
        sig_name = "CexvStsExvVoltgRangErr"
        sig_start_bit = 20
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VoltgRangErr_NoErr': 0, 'VoltgRangErr_UnderVoltageErr': 1, 'VoltgRangErr_OverVoltageErr': 2, 'VoltgRangErr_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 20
        byte = 2
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class CexvNVMFlt:
        sig_name = "CexvNVMFlt"
        sig_start_bit = 22
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
        startbit = 22
        byte = 2
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class CexvStsExvPreHeatgSts:
        sig_name = "CexvStsExvPreHeatgSts"
        sig_start_bit = 19
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
        startbit = 19
        byte = 2
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class CexvStsExvActrPosn:
        sig_name = "CexvStsExvActrPosn"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.2
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 500
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 0
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b00000011, 0b11111100, 2, 0)]

    class CexvStsExvOvrTempErr:
        sig_name = "CexvStsExvOvrTempErr"
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
        sig_value_table = {'Err1_NoErr': 0, 'Err1_Err': 1}
        compute_method = None
        length = 1
        startbit = 17
        byte = 2
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class CexvStsExvElecStsErr:
        sig_name = "CexvStsExvElecStsErr"
        sig_start_bit = 13
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
        startbit = 13
        byte = 1
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5


class DiagRequest9:
    msg_name = "DiagRequest9"
    msg_id = 60
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = []


class DiagResponse9:
    msg_name = "DiagResponse9"
    msg_id = 61
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['ECM']


class HvscEcm_Lin3Fr02:
    msg_name = "HvscEcm_Lin3Fr02"
    msg_id = 5
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 8
    tx_node = "ETC"
    rx_nodes = ['ECM']

    class ISecDcDcActLoSideChks_0_HvscEcm_Lin3SignalIPdu02:
        sig_name = "ISecDcDcActLoSideChks_0_HvscEcm_Lin3SignalIPdu02"
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

    class ISecDcDcActLoSideCntr_0_HvscEcm_Lin3SignalIPdu02:
        sig_name = "ISecDcDcActLoSideCntr_0_HvscEcm_Lin3SignalIPdu02"
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

    class ISecDcDcActLoSideIDcDcActLoSide_0_HvscEcm_Lin3SignalIPdu02:
        sig_name = "ISecDcDcActLoSideIDcDcActLoSide_0_HvscEcm_Lin3SignalIPdu02"
        sig_start_bit = 12
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
        startbit = 12
        bmuws_info = [(1, 0b11110000, 0b00001111, 4, 4), (2, 0b11111111, 0b00000000, 8, 0)]


class CexvEcm_Lin3SerNrFr08:
    msg_name = "CexvEcm_Lin3SerNrFr08"
    msg_id = 33
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 4
    tx_node = "CEXV"
    rx_nodes = ['ECM']

    class CEXVSerNoNr4:
        sig_name = "CEXVSerNoNr4"
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

    class CEXVSerNoNr3:
        sig_name = "CEXVSerNoNr3"
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

    class CEXVSerNoNr2:
        sig_name = "CEXVSerNoNr2"
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

    class CEXVSerNoNr1:
        sig_name = "CEXVSerNoNr1"
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


class EcmEcm_Lin3Fr01:
    msg_name = "EcmEcm_Lin3Fr01"
    msg_id = 11
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 7
    tx_node = "ECM"
    rx_nodes = ['EEXV', 'ETC', 'BEXV', 'CEXV']

    class RexvPosnReqExvMovEnable:
        sig_name = "RexvPosnReqExvMovEnable"
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
        sig_value_table = {'EXVNotEnable': 0, 'EXVEnable': 1}
        compute_method = None
        length = 1
        startbit = 42
        byte = 5
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class CexvPosnReqExvCalibReq:
        sig_name = "CexvPosnReqExvCalibReq"
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

    class EexvPosnReqExvHeatdReq_1_EcmEcm_Lin3SignalIPdu01:
        sig_name = "EexvPosnReqExvHeatdReq_1_EcmEcm_Lin3SignalIPdu01"
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
        sig_value_table = {'ExvHeatdReq_NoReq': 0, 'ExvHeatdReq_PreHeatedReq': 1}
        compute_method = None
        length = 1
        startbit = 27
        byte = 3
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class EexvPosnReqExvMovEnable_1_EcmEcm_Lin3SignalIPdu01:
        sig_name = "EexvPosnReqExvMovEnable_1_EcmEcm_Lin3SignalIPdu01"
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
        sig_value_table = {'EXVNotEnable': 0, 'EXVEnable': 1}
        compute_method = None
        length = 1
        startbit = 28
        byte = 3
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class BexvPosnReqExvMovEnable:
        sig_name = "BexvPosnReqExvMovEnable"
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
        sig_value_table = {'EXVNotEnable': 0, 'EXVEnable': 1}
        compute_method = None
        length = 1
        startbit = 2
        byte = 0
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class CexvPosnReqExvPosnReq:
        sig_name = "CexvPosnReqExvPosnReq"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.2
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 500
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 16
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b00000011, 0b11111100, 2, 0)]

    class RexvPosnReqExvPosnReq:
        sig_name = "RexvPosnReqExvPosnReq"
        sig_start_bit = 46
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.2
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 500
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 46
        bmuws_info = [(5, 0b11000000, 0b00111111, 2, 6), (6, 0b11111111, 0b00000000, 8, 0)]

    class EexvPosnReqExvPosnReq_1_EcmEcm_Lin3SignalIPdu01:
        sig_name = "EexvPosnReqExvPosnReq_1_EcmEcm_Lin3SignalIPdu01"
        sig_start_bit = 30
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.2
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 500
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 30
        bmuws_info = [(3, 0b11000000, 0b00111111, 2, 6), (4, 0b11111111, 0b00000000, 8, 0)]

    class EexvPosnReqExvCalibReq_1_EcmEcm_Lin3SignalIPdu01:
        sig_name = "EexvPosnReqExvCalibReq_1_EcmEcm_Lin3SignalIPdu01"
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
        sig_value_table = {'ExvCalibReq_NoReq': 0, 'ExvCalibReq_InitializationReq': 1}
        compute_method = None
        length = 1
        startbit = 26
        byte = 3
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class BexvPosnReqExvPosnReq:
        sig_name = "BexvPosnReqExvPosnReq"
        sig_start_bit = 3
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.2
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 500
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 3
        bmuws_info = [(0, 0b11111000, 0b00000111, 5, 3), (1, 0b00011111, 0b11100000, 5, 0)]

    class RexvPosnReqExvCalibReq:
        sig_name = "RexvPosnReqExvCalibReq"
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
        sig_value_table = {'ExvCalibReq_NoReq': 0, 'ExvCalibReq_InitializationReq': 1}
        compute_method = None
        length = 1
        startbit = 40
        byte = 5
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class RexvPosnReqExvHeatdReq:
        sig_name = "RexvPosnReqExvHeatdReq"
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
        sig_value_table = {'ExvHeatdReq_NoReq': 0, 'ExvHeatdReq_PreHeatedReq': 1}
        compute_method = None
        length = 1
        startbit = 41
        byte = 5
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class BexvPosnReqExvHeatdReq:
        sig_name = "BexvPosnReqExvHeatdReq"
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
        sig_value_table = {'ExvHeatdReq_NoReq': 0, 'ExvHeatdReq_PreHeatedReq': 1}
        compute_method = None
        length = 1
        startbit = 1
        byte = 0
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class CexvPosnReqExvHeatdReq:
        sig_name = "CexvPosnReqExvHeatdReq"
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
        sig_value_table = {'ExvHeatdReq_NoReq': 0, 'ExvHeatdReq_PreHeatedReq': 1}
        compute_method = None
        length = 1
        startbit = 14
        byte = 1
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class BexvPosnReqExvCalibReq:
        sig_name = "BexvPosnReqExvCalibReq"
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
        sig_value_table = {'ExvCalibReq_NoReq': 0, 'ExvCalibReq_InitializationReq': 1}
        compute_method = None
        length = 1
        startbit = 0
        byte = 0
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class CexvPosnReqExvMovEnable:
        sig_name = "CexvPosnReqExvMovEnable"
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
        sig_value_table = {'EXVNotEnable': 0, 'EXVEnable': 1}
        compute_method = None
        length = 1
        startbit = 15
        byte = 1
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7


class EexvCcm_Lin2SerNrFr01:
    msg_name = "EexvCcm_Lin2SerNrFr01"
    msg_id = 34
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 4
    tx_node = "EEXV"
    rx_nodes = ['ECM']

    class EEXVSerNoNr3:
        sig_name = "EEXVSerNoNr3"
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

    class EEXVSerNoNr4:
        sig_name = "EEXVSerNoNr4"
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

    class EEXVSerNoNr1:
        sig_name = "EEXVSerNoNr1"
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

    class EEXVSerNoNr2:
        sig_name = "EEXVSerNoNr2"
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


class CexvEcm_Lin3PartNrFr08:
    msg_name = "CexvEcm_Lin3PartNrFr08"
    msg_id = 47
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 7
    tx_node = "CEXV"
    rx_nodes = ['ECM']

    class CEXVPartNoCmplEndSgn1:
        sig_name = "CEXVPartNoCmplEndSgn1"
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

    class CEXVPartNoCmplEndSgn3:
        sig_name = "CEXVPartNoCmplEndSgn3"
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

    class CEXVPartNoCmplNr4:
        sig_name = "CEXVPartNoCmplNr4"
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

    class CEXVPartNoCmplNr2:
        sig_name = "CEXVPartNoCmplNr2"
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

    class CEXVPartNoCmplNr1:
        sig_name = "CEXVPartNoCmplNr1"
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

    class CEXVPartNoCmplNr3:
        sig_name = "CEXVPartNoCmplNr3"
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

    class CEXVPartNoCmplEndSgn2:
        sig_name = "CEXVPartNoCmplEndSgn2"
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


class EexvCcm_Lin2PartNrFr04:
    msg_name = "EexvCcm_Lin2PartNrFr04"
    msg_id = 32
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 8
    tx_node = "EEXV"
    rx_nodes = ['ECM']

    class EEXVPartNo10CmplEndSgn1:
        sig_name = "EEXVPartNo10CmplEndSgn1"
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

    class EEXVPartNo10CmplNr1:
        sig_name = "EEXVPartNo10CmplNr1"
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

    class EEXVPartNo10CmplNr5:
        sig_name = "EEXVPartNo10CmplNr5"
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

    class EEXVPartNo10CmplEndSgn2:
        sig_name = "EEXVPartNo10CmplEndSgn2"
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

    class EEXVPartNo10CmplNr2:
        sig_name = "EEXVPartNo10CmplNr2"
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

    class EEXVPartNo10CmplNr3:
        sig_name = "EEXVPartNo10CmplNr3"
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

    class EEXVPartNo10CmplEndSgn3:
        sig_name = "EEXVPartNo10CmplEndSgn3"
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

    class EEXVPartNo10CmplNr4:
        sig_name = "EEXVPartNo10CmplNr4"
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


class BexvEcm_Lin3PartNrFr08:
    msg_name = "BexvEcm_Lin3PartNrFr08"
    msg_id = 45
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 7
    tx_node = "BEXV"
    rx_nodes = ['ECM']

    class BEXVPartNoCmplEndSgn1:
        sig_name = "BEXVPartNoCmplEndSgn1"
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

    class BEXVPartNoCmplEndSgn3:
        sig_name = "BEXVPartNoCmplEndSgn3"
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

    class BEXVPartNoCmplNr1:
        sig_name = "BEXVPartNoCmplNr1"
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

    class BEXVPartNoCmplNr2:
        sig_name = "BEXVPartNoCmplNr2"
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

    class BEXVPartNoCmplEndSgn2:
        sig_name = "BEXVPartNoCmplEndSgn2"
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

    class BEXVPartNoCmplNr3:
        sig_name = "BEXVPartNoCmplNr3"
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

    class BEXVPartNoCmplNr4:
        sig_name = "BEXVPartNoCmplNr4"
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


class RexvEcm_Lin3Fr01:
    msg_name = "RexvEcm_Lin3Fr01"
    msg_id = 27
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 7
    tx_node = "ETC"
    rx_nodes = ['ECM']

    class RexvStsExvVoltgRangErr:
        sig_name = "RexvStsExvVoltgRangErr"
        sig_start_bit = 20
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VoltgRangErr_NoErr': 0, 'VoltgRangErr_UnderVoltageErr': 1, 'VoltgRangErr_OverVoltageErr': 2, 'VoltgRangErr_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 20
        byte = 2
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class RexvStsExvActrPosn:
        sig_name = "RexvStsExvActrPosn"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.2
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 500
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 0
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b00000011, 0b11111100, 2, 0)]

    class RexvStsExvCalibSts:
        sig_name = "RexvStsExvCalibSts"
        sig_start_bit = 11
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
        startbit = 11
        byte = 1
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class RexvStsExvMovSts:
        sig_name = "RexvStsExvMovSts"
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
        sig_value_table = {'ExvMovSts_NotMove': 0, 'ExvMovSts_Moving': 1}
        compute_method = None
        length = 1
        startbit = 16
        byte = 2
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class RexvStsExvBlkErr:
        sig_name = "RexvStsExvBlkErr"
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
        sig_value_table = {'Err1_NoErr': 0, 'Err1_Err': 1}
        compute_method = None
        length = 1
        startbit = 10
        byte = 1
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class RexvNVMFlt:
        sig_name = "RexvNVMFlt"
        sig_start_bit = 22
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
        startbit = 22
        byte = 2
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class RexvStsExvOvrTrvlErr:
        sig_name = "RexvStsExvOvrTrvlErr"
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
        sig_value_table = {'Err1_NoErr': 0, 'Err1_Err': 1}
        compute_method = None
        length = 1
        startbit = 18
        byte = 2
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class RexvStsExvOvrTempErr:
        sig_name = "RexvStsExvOvrTempErr"
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
        sig_value_table = {'Err1_NoErr': 0, 'Err1_Err': 1}
        compute_method = None
        length = 1
        startbit = 17
        byte = 2
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class RexvStsExvElecStsErr:
        sig_name = "RexvStsExvElecStsErr"
        sig_start_bit = 13
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
        startbit = 13
        byte = 1
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class RexvStsExvPreHeatgSts:
        sig_name = "RexvStsExvPreHeatgSts"
        sig_start_bit = 19
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
        startbit = 19
        byte = 2
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3


class EexvCcm_Lin2Fr01:
    msg_name = "EexvCcm_Lin2Fr01"
    msg_id = 36
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 7
    tx_node = "EEXV"
    rx_nodes = ['ECM']

    class EexvStsExvPreHeatgSts_0_EexvCcm_Lin2SignalIPdu01:
        sig_name = "EexvStsExvPreHeatgSts_0_EexvCcm_Lin2SignalIPdu01"
        sig_start_bit = 19
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
        startbit = 19
        byte = 2
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class EexvStsExvMovSts_0_EexvCcm_Lin2SignalIPdu01:
        sig_name = "EexvStsExvMovSts_0_EexvCcm_Lin2SignalIPdu01"
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
        sig_value_table = {'ExvMovSts_NotMove': 0, 'ExvMovSts_Moving': 1}
        compute_method = None
        length = 1
        startbit = 16
        byte = 2
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class EexvStsExvElecStsErr_0_EexvCcm_Lin2SignalIPdu01:
        sig_name = "EexvStsExvElecStsErr_0_EexvCcm_Lin2SignalIPdu01"
        sig_start_bit = 13
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
        startbit = 13
        byte = 1
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class EexvNVMFlt:
        sig_name = "EexvNVMFlt"
        sig_start_bit = 22
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
        startbit = 22
        byte = 2
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class EexvStsExvOvrTempErr_0_EexvCcm_Lin2SignalIPdu01:
        sig_name = "EexvStsExvOvrTempErr_0_EexvCcm_Lin2SignalIPdu01"
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
        sig_value_table = {'Err1_NoErr': 0, 'Err1_Err': 1}
        compute_method = None
        length = 1
        startbit = 17
        byte = 2
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class EexvStsExvCalibSts_0_EexvCcm_Lin2SignalIPdu01:
        sig_name = "EexvStsExvCalibSts_0_EexvCcm_Lin2SignalIPdu01"
        sig_start_bit = 11
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
        startbit = 11
        byte = 1
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class EexvStsExvOvrTrvlErr_0_EexvCcm_Lin2SignalIPdu01:
        sig_name = "EexvStsExvOvrTrvlErr_0_EexvCcm_Lin2SignalIPdu01"
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
        sig_value_table = {'Err1_NoErr': 0, 'Err1_Err': 1}
        compute_method = None
        length = 1
        startbit = 18
        byte = 2
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class EexvStsExvActrPosn_0_EexvCcm_Lin2SignalIPdu01:
        sig_name = "EexvStsExvActrPosn_0_EexvCcm_Lin2SignalIPdu01"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.2
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 500
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 0
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b00000011, 0b11111100, 2, 0)]

    class EexvStsExvVoltgRangErr_0_EexvCcm_Lin2SignalIPdu01:
        sig_name = "EexvStsExvVoltgRangErr_0_EexvCcm_Lin2SignalIPdu01"
        sig_start_bit = 20
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VoltgRangErr_NoErr': 0, 'VoltgRangErr_UnderVoltageErr': 1, 'VoltgRangErr_OverVoltageErr': 2, 'VoltgRangErr_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 20
        byte = 2
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class EexvStsExvBlkErr_0_EexvCcm_Lin2SignalIPdu01:
        sig_name = "EexvStsExvBlkErr_0_EexvCcm_Lin2SignalIPdu01"
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
        sig_value_table = {'Err1_NoErr': 0, 'Err1_Err': 1}
        compute_method = None
        length = 1
        startbit = 10
        byte = 1
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2


class EexvCcm_Lin2PartNrFr08:
    msg_name = "EexvCcm_Lin2PartNrFr08"
    msg_id = 52
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 7
    tx_node = "EEXV"
    rx_nodes = ['ECM']

    class EEXVPartNoCmplNr3:
        sig_name = "EEXVPartNoCmplNr3"
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

    class EEXVPartNoCmplNr4:
        sig_name = "EEXVPartNoCmplNr4"
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

    class EEXVPartNoCmplEndSgn3:
        sig_name = "EEXVPartNoCmplEndSgn3"
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

    class EEXVPartNoCmplEndSgn1:
        sig_name = "EEXVPartNoCmplEndSgn1"
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

    class EEXVPartNoCmplEndSgn2:
        sig_name = "EEXVPartNoCmplEndSgn2"
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

    class EEXVPartNoCmplNr2:
        sig_name = "EEXVPartNoCmplNr2"
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

    class EEXVPartNoCmplNr1:
        sig_name = "EEXVPartNoCmplNr1"
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


class BexvEcm_Lin3SerNrFr01:
    msg_name = "BexvEcm_Lin3SerNrFr01"
    msg_id = 18
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 4
    tx_node = "BEXV"
    rx_nodes = ['ECM']

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


class BexvEcm_Lin3PartNrFr04:
    msg_name = "BexvEcm_Lin3PartNrFr04"
    msg_id = 13
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 8
    tx_node = "BEXV"
    rx_nodes = ['ECM']

    class BEXVPartNo10CmplNr1:
        sig_name = "BEXVPartNo10CmplNr1"
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

    class BEXVPartNo10CmplNr5:
        sig_name = "BEXVPartNo10CmplNr5"
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

    class BEXVPartNo10CmplEndSgn1:
        sig_name = "BEXVPartNo10CmplEndSgn1"
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

    class BEXVPartNo10CmplNr4:
        sig_name = "BEXVPartNo10CmplNr4"
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

    class BEXVPartNo10CmplEndSgn2:
        sig_name = "BEXVPartNo10CmplEndSgn2"
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

    class BEXVPartNo10CmplNr2:
        sig_name = "BEXVPartNo10CmplNr2"
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

    class BEXVPartNo10CmplEndSgn3:
        sig_name = "BEXVPartNo10CmplEndSgn3"
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

    class BEXVPartNo10CmplNr3:
        sig_name = "BEXVPartNo10CmplNr3"
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


class HvscEcm_Lin3Fr01:
    msg_name = "HvscEcm_Lin3Fr01"
    msg_id = 3
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 8
    tx_node = "ETC"
    rx_nodes = ['ECM']

    class FltTSecDcDc_0_HvscEcm_Lin3SignalIPdu01:
        sig_name = "FltTSecDcDc_0_HvscEcm_Lin3SignalIPdu01"
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
        sig_value_table = {'DevErrSts2_NoFlt': 0, 'DevErrSts2_Flt': 1}
        compute_method = None
        length = 1
        startbit = 29
        byte = 3
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class ISecDcDcActHiSide_0_HvscEcm_Lin3SignalIPdu01:
        sig_name = "ISecDcDcActHiSide_0_HvscEcm_Lin3SignalIPdu01"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = "-410.0"
        sig_value_min = 0
        sig_value_max = 8191
        sig_byteorder = "Intel"
        sig_value_init = 4100
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 16
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b00011111, 0b11100000, 5, 0)]

    class USecDcDcActHiSide_0_HvscEcm_Lin3SignalIPdu01:
        sig_name = "USecDcDcActHiSide_0_HvscEcm_Lin3SignalIPdu01"
        sig_start_bit = 32
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 0.125
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 8184
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 32
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b00011111, 0b11100000, 5, 0)]

    class LimnIndcnSecDcDc_0_HvscEcm_Lin3SignalIPdu01:
        sig_name = "LimnIndcnSecDcDc_0_HvscEcm_Lin3SignalIPdu01"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 0
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class FltElecSecDcDc_0_HvscEcm_Lin3SignalIPdu01:
        sig_name = "FltElecSecDcDc_0_HvscEcm_Lin3SignalIPdu01"
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
        sig_value_table = {'DevErrSts2_NoFlt': 0, 'DevErrSts2_Flt': 1}
        compute_method = None
        length = 1
        startbit = 60
        byte = 7
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class SecDcDcActvd_0_HvscEcm_Lin3SignalIPdu01:
        sig_name = "SecDcDcActvd_0_HvscEcm_Lin3SignalIPdu01"
        sig_start_bit = 30
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DcDcActvd2_DcDcInactive': 0, 'DcDcActvd2_DcDcActive': 1, 'DcDcActvd2_Abnormal': 2, 'DcDcActvd2_Invalid': 3}
        compute_method = None
        length = 2
        startbit = 30
        byte = 3
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


