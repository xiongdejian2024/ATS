class HcmrBodyExpoFr02:
    msg_name = "HcmrBodyExpoFr02"
    msg_id = 594
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 3
    tx_node = "HCMR"
    rx_nodes = ['BGM', 'S2SReceiver']

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


class HcmrBodyExposedCANNmFr:
    msg_name = "HcmrBodyExposedCANNmFr"
    msg_id = 1330
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "HCMR"
    rx_nodes = ['BGM']


class CemBodyExpoFr45:
    msg_name = "CemBodyExpoFr45"
    msg_id = 612
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.065
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCML', 'HCMR']

    class WipgInfoWipgSpdInfo_1_CemBodyExpoSignalIPdu45:
        sig_name = "WipgInfoWipgSpdInfo_1_CemBodyExpoSignalIPdu45"
        sig_start_bit = 26
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WipgSpdInfo_Off': 0, 'WipgSpdInfo_IntlLo': 1, 'WipgSpdInfo_IntlHi': 2, 'WipgSpdInfo_WipgSpd4045': 3, 'WipgSpdInfo_WipgSpd4650': 4, 'WipgSpdInfo_WipgSpd5155': 5, 'WipgSpdInfo_WipgSpd5660': 6, 'WipgSpdInfo_WiprErr': 7}
        compute_method = None
        length = 3
        startbit = 26
        byte = 3
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class WipgInfoWiprInWipgAr_1_CemBodyExpoSignalIPdu45:
        sig_name = "WipgInfoWiprInWipgAr_1_CemBodyExpoSignalIPdu45"
        sig_start_bit = 28
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
        startbit = 28
        byte = 3
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class WipgInfoWiprActv_1_CemBodyExpoSignalIPdu45:
        sig_name = "WipgInfoWiprActv_1_CemBodyExpoSignalIPdu45"
        sig_start_bit = 27
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
        startbit = 27
        byte = 3
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class BrkPedlValBrkPedlVal_1_CemBodyExpoSignalIPdu45:
        sig_name = "BrkPedlValBrkPedlVal_1_CemBodyExpoSignalIPdu45"
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

    class BrkPedlValQf_1_CemBodyExpoSignalIPdu45:
        sig_name = "BrkPedlValQf_1_CemBodyExpoSignalIPdu45"
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


class CemBodyExpoDevFr02:
    msg_name = "CemBodyExpoDevFr02"
    msg_id = 1431
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['CCM']

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


class BgmBodyExposedCANFr01:
    msg_name = "BgmBodyExposedCANFr01"
    msg_id = 368
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCML', 'RCMM', 'HCMR']

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


class BgmToRcmmBodyExpoDiagReqFrame:
    msg_name = "BgmToRcmmBodyExpoDiagReqFrame"
    msg_id = 1975
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RCMM']


class HcmlToBgmBodyExpoDiagRespFrame:
    msg_name = "HcmlToBgmBodyExpoDiagRespFrame"
    msg_id = 1715
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "HCML"
    rx_nodes = ['BGM']


class CemBodyExpoCommonFr05:
    msg_name = "CemBodyExpoCommonFr05"
    msg_id = 384
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR', 'HCML', 'RCMM', 'RCML', 'RCMR']

    class VehCfgPrmCCPBytePosn7_2_CemBodyExpoCommonSignalIPdu05:
        sig_name = "VehCfgPrmCCPBytePosn7_2_CemBodyExpoCommonSignalIPdu05"
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

    class VehCfgPrmCCPBytePosn2_2_CemBodyExpoCommonSignalIPdu05:
        sig_name = "VehCfgPrmCCPBytePosn2_2_CemBodyExpoCommonSignalIPdu05"
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

    class VehCfgPrmCCPBytePosn3_2_CemBodyExpoCommonSignalIPdu05:
        sig_name = "VehCfgPrmCCPBytePosn3_2_CemBodyExpoCommonSignalIPdu05"
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

    class VehCfgPrmBlkIDBytePosn1_2_CemBodyExpoCommonSignalIPdu05:
        sig_name = "VehCfgPrmBlkIDBytePosn1_2_CemBodyExpoCommonSignalIPdu05"
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

    class VehCfgPrmCCPBytePosn8_2_CemBodyExpoCommonSignalIPdu05:
        sig_name = "VehCfgPrmCCPBytePosn8_2_CemBodyExpoCommonSignalIPdu05"
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

    class VehCfgPrmCCPBytePosn5_2_CemBodyExpoCommonSignalIPdu05:
        sig_name = "VehCfgPrmCCPBytePosn5_2_CemBodyExpoCommonSignalIPdu05"
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

    class VehCfgPrmCCPBytePosn6_2_CemBodyExpoCommonSignalIPdu05:
        sig_name = "VehCfgPrmCCPBytePosn6_2_CemBodyExpoCommonSignalIPdu05"
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

    class VehCfgPrmCCPBytePosn4_2_CemBodyExpoCommonSignalIPdu05:
        sig_name = "VehCfgPrmCCPBytePosn4_2_CemBodyExpoCommonSignalIPdu05"
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


class BgmBodyExposedCANFr04:
    msg_name = "BgmBodyExposedCANFr04"
    msg_id = 148
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 64
    tx_node = "BGM"
    rx_nodes = ['RCMM', 'RCML', 'RCMR']

    class CrossReRiX1Y7:
        sig_name = "CrossReRiX1Y7"
        sig_start_bit = 135
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
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

    class CrossReLeX1Y5:
        sig_name = "CrossReLeX1Y5"
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

    class CrossReMidX1Y5:
        sig_name = "CrossReMidX1Y5"
        sig_start_bit = 199
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
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

    class CrossReMidX1Y33:
        sig_name = "CrossReMidX1Y33"
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

    class CrossReMidX1Y23:
        sig_name = "CrossReMidX1Y23"
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

    class CrossReLeX1Y4:
        sig_name = "CrossReLeX1Y4"
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

    class CrossReMidX1Y9:
        sig_name = "CrossReMidX1Y9"
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

    class CrossReMidX1Y25:
        sig_name = "CrossReMidX1Y25"
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

    class CrossReMidX1Y22:
        sig_name = "CrossReMidX1Y22"
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

    class CrossReMidX1Y4:
        sig_name = "CrossReMidX1Y4"
        sig_start_bit = 191
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 191
        byte = 23
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class CrossReMidX1Y36:
        sig_name = "CrossReMidX1Y36"
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

    class CrossReLeX1Y1:
        sig_name = "CrossReLeX1Y1"
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

    class CrossReLeX1Y8:
        sig_name = "CrossReLeX1Y8"
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

    class CrossReMidX1Y19:
        sig_name = "CrossReMidX1Y19"
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

    class CrossReRiX1Y1:
        sig_name = "CrossReRiX1Y1"
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

    class CrossReMidX1Y10:
        sig_name = "CrossReMidX1Y10"
        sig_start_bit = 239
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 239
        byte = 29
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class CrossReRiX1Y5:
        sig_name = "CrossReRiX1Y5"
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

    class CrossReMidX1Y16:
        sig_name = "CrossReMidX1Y16"
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

    class CrossReMidX1Y30:
        sig_name = "CrossReMidX1Y30"
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

    class CrossReRiX1Y3:
        sig_name = "CrossReRiX1Y3"
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

    class CrossReMidX1Y13:
        sig_name = "CrossReMidX1Y13"
        sig_start_bit = 263
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
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

    class CrossReMidX1Y35:
        sig_name = "CrossReMidX1Y35"
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

    class CrossReMidX1Y20:
        sig_name = "CrossReMidX1Y20"
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

    class CrossReMidX1Y11:
        sig_name = "CrossReMidX1Y11"
        sig_start_bit = 247
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 247
        byte = 30
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class CrossReLeX1Y3:
        sig_name = "CrossReLeX1Y3"
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

    class CrossReLeX1Y10:
        sig_name = "CrossReLeX1Y10"
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

    class CrossReRiX1Y6:
        sig_name = "CrossReRiX1Y6"
        sig_start_bit = 127
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 127
        byte = 15
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class CrossReRiX1Y4:
        sig_name = "CrossReRiX1Y4"
        sig_start_bit = 111
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 111
        byte = 13
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class CrossReMidX1Y15:
        sig_name = "CrossReMidX1Y15"
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

    class CrossReMidX1Y31:
        sig_name = "CrossReMidX1Y31"
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

    class CrossReMidX1Y3:
        sig_name = "CrossReMidX1Y3"
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

    class CrossReMidX1Y27:
        sig_name = "CrossReMidX1Y27"
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

    class CrossReRiX1Y10:
        sig_name = "CrossReRiX1Y10"
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

    class CrossReMidX1Y17:
        sig_name = "CrossReMidX1Y17"
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

    class CrossReMidX1Y29:
        sig_name = "CrossReMidX1Y29"
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

    class CrossReMidX1Y14:
        sig_name = "CrossReMidX1Y14"
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

    class CrossReLeX1Y9:
        sig_name = "CrossReLeX1Y9"
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

    class CrossReLeX1Y6:
        sig_name = "CrossReLeX1Y6"
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

    class CrossReMidX1Y21:
        sig_name = "CrossReMidX1Y21"
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

    class CrossReMidX1Y28:
        sig_name = "CrossReMidX1Y28"
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

    class CrossReMidX1Y26:
        sig_name = "CrossReMidX1Y26"
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

    class CrossReMidX1Y1:
        sig_name = "CrossReMidX1Y1"
        sig_start_bit = 167
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 167
        byte = 20
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class CrossReMidX1Y18:
        sig_name = "CrossReMidX1Y18"
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

    class CrossReMidX1Y32:
        sig_name = "CrossReMidX1Y32"
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

    class CrossReLeX1Y2:
        sig_name = "CrossReLeX1Y2"
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

    class CrossReMidX1Y38:
        sig_name = "CrossReMidX1Y38"
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

    class CrossReMidX1Y24:
        sig_name = "CrossReMidX1Y24"
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

    class CrossReMidX1Y7:
        sig_name = "CrossReMidX1Y7"
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

    class CrossReRiX1Y2:
        sig_name = "CrossReRiX1Y2"
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

    class CrossReMidX1Y2:
        sig_name = "CrossReMidX1Y2"
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

    class CrossReLeX1Y7:
        sig_name = "CrossReLeX1Y7"
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

    class CrossReMidX1Y34:
        sig_name = "CrossReMidX1Y34"
        sig_start_bit = 431
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
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

    class CrossReRiX1Y8:
        sig_name = "CrossReRiX1Y8"
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

    class CrossReMidX1Y37:
        sig_name = "CrossReMidX1Y37"
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

    class CrossReMidX1Y6:
        sig_name = "CrossReMidX1Y6"
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

    class CrossReMidX1Y8:
        sig_name = "CrossReMidX1Y8"
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

    class CrossReRiX1Y9:
        sig_name = "CrossReRiX1Y9"
        sig_start_bit = 151
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 151
        byte = 18
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class CrossReMidX1Y12:
        sig_name = "CrossReMidX1Y12"
        sig_start_bit = 255
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
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


class HcmlBodyExpoFr05:
    msg_name = "HcmlBodyExpoFr05"
    msg_id = 256
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.03
    msg_length = 8
    tx_node = "HCML"
    rx_nodes = ['BGM', 'S2SReceiver']

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


class RcmrBodyExposedCANeNmFr:
    msg_name = "RcmrBodyExposedCANeNmFr"
    msg_id = 1332
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "RCMR"
    rx_nodes = ['HCML']


class CemBodyExpoDevDiagFr01:
    msg_name = "CemBodyExpoDevDiagFr01"
    msg_id = 1432
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['CCM']

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


class RcmlBodyExposedCANNmFr:
    msg_name = "RcmlBodyExposedCANNmFr"
    msg_id = 1331
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "RCML"
    rx_nodes = ['HCMR']


class HcmmBodyExposedCANNmFr:
    msg_name = "HcmmBodyExposedCANNmFr"
    msg_id = 1334
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['RCML']


class CemBodyExpoFr51:
    msg_name = "CemBodyExpoFr51"
    msg_id = 538
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR', 'HCML', 'RCML', 'RCMR']

    class IndcrPatCmd1WdTiOn_0_CemBodyExpoSignalIPdu51:
        sig_name = "IndcrPatCmd1WdTiOn_0_CemBodyExpoSignalIPdu51"
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

    class ActvnOfIndcrIndcrOut_1_CemBodyExpoSignalIPdu51:
        sig_name = "ActvnOfIndcrIndcrOut_1_CemBodyExpoSignalIPdu51"
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

    class ActvnOfIndcrIndcrOutChks_1_CemBodyExpoSignalIPdu51:
        sig_name = "ActvnOfIndcrIndcrOutChks_1_CemBodyExpoSignalIPdu51"
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

    class IndcrPatCmd1WdTiOff_0_CemBodyExpoSignalIPdu51:
        sig_name = "IndcrPatCmd1WdTiOff_0_CemBodyExpoSignalIPdu51"
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

    class ActvnOfIndcrIndcrOutCntr_1_CemBodyExpoSignalIPdu51:
        sig_name = "ActvnOfIndcrIndcrOutCntr_1_CemBodyExpoSignalIPdu51"
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

    class IndcrSts_1_CemBodyExpoSignalIPdu51:
        sig_name = "IndcrSts_1_CemBodyExpoSignalIPdu51"
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


class BgmBodyExposedCANNmFr:
    msg_name = "BgmBodyExposedCANNmFr"
    msg_id = 1322
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RCMR']


class CemBodyExpoCommonFr02:
    msg_name = "CemBodyExpoCommonFr02"
    msg_id = 768
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.045
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCML', 'HCMR']

    class BrkPedlrRatQf_1_CemBodyExpoCommonSignalIPdu02:
        sig_name = "BrkPedlrRatQf_1_CemBodyExpoCommonSignalIPdu02"
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

    class YawRateReqdByDrvr_1_CemBodyExpoCommonSignalIPdu02:
        sig_name = "YawRateReqdByDrvr_1_CemBodyExpoCommonSignalIPdu02"
        sig_start_bit = 7
        update_id_bit = 21
        sig_length = 16
        sig_value_factor = "2.44140625E-4"
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

    class BrkPedlrRatPerc_1_CemBodyExpoCommonSignalIPdu02:
        sig_name = "BrkPedlrRatPerc_1_CemBodyExpoCommonSignalIPdu02"
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


class CemBodyExpoFr50:
    msg_name = "CemBodyExpoFr50"
    msg_id = 522
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR', 'HCML', 'RCMM', 'RCML', 'RCMR']

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


class HcmlBodyExposedCANNmFr:
    msg_name = "HcmlBodyExposedCANNmFr"
    msg_id = 1329
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "HCML"
    rx_nodes = ['RCMM']


class CemBodyExpoCommonFr01:
    msg_name = "CemBodyExpoCommonFr01"
    msg_id = 82
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCML', 'CCM', 'HCMR']

    class SteerWhlSnsrAg_3_CemBodyExpoCommonSignalIPdu01:
        sig_name = "SteerWhlSnsrAg_3_CemBodyExpoCommonSignalIPdu01"
        sig_start_bit = 6
        update_id_bit = None
        sig_length = 15
        sig_value_factor = "9.765625E-4"
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

    class SteerWhlSnsrChks_3_CemBodyExpoCommonSignalIPdu01:
        sig_name = "SteerWhlSnsrChks_3_CemBodyExpoCommonSignalIPdu01"
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

    class SteerWhlSnsrAgSpd_3_CemBodyExpoCommonSignalIPdu01:
        sig_name = "SteerWhlSnsrAgSpd_3_CemBodyExpoCommonSignalIPdu01"
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

    class SteerWhlSnsrQf_3_CemBodyExpoCommonSignalIPdu01:
        sig_name = "SteerWhlSnsrQf_3_CemBodyExpoCommonSignalIPdu01"
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

    class LiOprnMod_1_CemBodyExpoCommonSignalIPdu01:
        sig_name = "LiOprnMod_1_CemBodyExpoCommonSignalIPdu01"
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

    class SteerWhlSnsrCntr_3_CemBodyExpoCommonSignalIPdu01:
        sig_name = "SteerWhlSnsrCntr_3_CemBodyExpoCommonSignalIPdu01"
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


class BgmBodyExposedCANFr06:
    msg_name = "BgmBodyExposedCANFr06"
    msg_id = 150
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 64
    tx_node = "BGM"
    rx_nodes = ['HCML']

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


class CemBodyExpoCommonFr21:
    msg_name = "CemBodyExpoCommonFr21"
    msg_id = 64
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.015
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR', 'HCML', 'CCM', 'RCMM', 'RCML', 'RCMR']

    class VehModMngtGlbSafe1EgyLvlElecMai_4_CemBodyExpoCommonSignalIPdu21:
        sig_name = "VehModMngtGlbSafe1EgyLvlElecMai_4_CemBodyExpoCommonSignalIPdu21"
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

    class VehModMngtGlbSafe1FltEgyCnsWdSts_4_CemBodyExpoCommonSignalIPdu21:
        sig_name = "VehModMngtGlbSafe1FltEgyCnsWdSts_4_CemBodyExpoCommonSignalIPdu21"
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

    class VehModMngtGlbSafe1PwrLvlElecSubtyp_4_CemBodyExpoCommonSignalIPdu21:
        sig_name = "VehModMngtGlbSafe1PwrLvlElecSubtyp_4_CemBodyExpoCommonSignalIPdu21"
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

    class VehModMngtGlbSafe1PwrLvlElecMai_4_CemBodyExpoCommonSignalIPdu21:
        sig_name = "VehModMngtGlbSafe1PwrLvlElecMai_4_CemBodyExpoCommonSignalIPdu21"
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

    class VehModMngtGlbSafe1UsgModSts_4_CemBodyExpoCommonSignalIPdu21:
        sig_name = "VehModMngtGlbSafe1UsgModSts_4_CemBodyExpoCommonSignalIPdu21"
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

    class VehModMngtGlbSafe1EgyLvlElecSubtyp_4_CemBodyExpoCommonSignalIPdu21:
        sig_name = "VehModMngtGlbSafe1EgyLvlElecSubtyp_4_CemBodyExpoCommonSignalIPdu21"
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

    class VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp_4_CemBodyExpoCommonSignalIPdu21:
        sig_name = "VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp_4_CemBodyExpoCommonSignalIPdu21"
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

    class VehModMngtGlbSafe1Chks_4_CemBodyExpoCommonSignalIPdu21:
        sig_name = "VehModMngtGlbSafe1Chks_4_CemBodyExpoCommonSignalIPdu21"
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

    class VehModMngtGlbSafe1Cntr_4_CemBodyExpoCommonSignalIPdu21:
        sig_name = "VehModMngtGlbSafe1Cntr_4_CemBodyExpoCommonSignalIPdu21"
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

    class RainLi_1_CemBodyExpoCommonSignalIPdu21:
        sig_name = "RainLi_1_CemBodyExpoCommonSignalIPdu21"
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

    class VehModMngtGlbSafe1CarModSts1_4_CemBodyExpoCommonSignalIPdu21:
        sig_name = "VehModMngtGlbSafe1CarModSts1_4_CemBodyExpoCommonSignalIPdu21"
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


class CemBodyExpoCommonFr04:
    msg_name = "CemBodyExpoCommonFr04"
    msg_id = 80
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.04
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR', 'HCML', 'RCMM', 'RCML', 'RCMR']

    class VehSpdLgtChks_3_CEMBodyExpoCommonSignalIPdu04:
        sig_name = "VehSpdLgtChks_3_CEMBodyExpoCommonSignalIPdu04"
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

    class VehSpdLgtCntr_3_CEMBodyExpoCommonSignalIPdu04:
        sig_name = "VehSpdLgtCntr_3_CEMBodyExpoCommonSignalIPdu04"
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

    class VehSpdLgtA_3_CEMBodyExpoCommonSignalIPdu04:
        sig_name = "VehSpdLgtA_3_CEMBodyExpoCommonSignalIPdu04"
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

    class VehSpdLgtQf_3_CEMBodyExpoCommonSignalIPdu04:
        sig_name = "VehSpdLgtQf_3_CEMBodyExpoCommonSignalIPdu04"
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


class EtctoHcmlXCPFr01:
    msg_name = "EtctoHcmlXCPFr01"
    msg_id = 1430
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CCM"
    rx_nodes = ['HCML']


class RcmmBodyExpoFr02:
    msg_name = "RcmmBodyExpoFr02"
    msg_id = 596
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 12
    tx_node = "RCMM"
    rx_nodes = ['BGM', 'S2SReceiver']

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


class BgmBodyExposedCANFr07:
    msg_name = "BgmBodyExposedCANFr07"
    msg_id = 151
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 64
    tx_node = "BGM"
    rx_nodes = ['HCMR']

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


class BgmToRcmrBodyExpoDiagReqFrame:
    msg_name = "BgmToRcmrBodyExpoDiagReqFrame"
    msg_id = 1974
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RCMR']


class EtctoHcmrXCPFr01:
    msg_name = "EtctoHcmrXCPFr01"
    msg_id = 1428
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CCM"
    rx_nodes = ['HCMR']


class BgmToAllFuncBodyExpoDiagReqFrame:
    msg_name = "BgmToAllFuncBodyExpoDiagReqFrame"
    msg_id = 2047
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR', 'HCML', 'RCMM', 'RCML', 'RCMR']


class CEMBodyExpoCommonFr07:
    msg_name = "CEMBodyExpoCommonFr07"
    msg_id = 544
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.06
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR', 'HCML', 'RCMM', 'RCML', 'RCMR']

    class TrSts_1_CEMBodyExpoCommonSignalIPdu07:
        sig_name = "TrSts_1_CEMBodyExpoCommonSignalIPdu07"
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

    class CarTiGlb_6_CEMBodyExpoCommonSignalIPdu07:
        sig_name = "CarTiGlb_6_CEMBodyExpoCommonSignalIPdu07"
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


class BgmBodyExposedCANFr03:
    msg_name = "BgmBodyExposedCANFr03"
    msg_id = 147
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 64
    tx_node = "BGM"
    rx_nodes = ['HCML', 'HCMR']

    class HiBeamLe:
        sig_name = "HiBeamLe"
        sig_start_bit = 367
        update_id_bit = 360
        sig_length = 7
        sig_value_factor = 1
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

    class CrossFrntX1Y41:
        sig_name = "CrossFrntX1Y41"
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

    class CrossFrntX1Y32:
        sig_name = "CrossFrntX1Y32"
        sig_start_bit = 255
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
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

    class CrossFrntX1Y8:
        sig_name = "CrossFrntX1Y8"
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

    class CrossFrntX1Y22:
        sig_name = "CrossFrntX1Y22"
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

    class CrossFrntX1Y28:
        sig_name = "CrossFrntX1Y28"
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

    class CrossFrntX1Y20:
        sig_name = "CrossFrntX1Y20"
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

    class CrossFrntX1Y38:
        sig_name = "CrossFrntX1Y38"
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

    class CrossFrntX1Y11:
        sig_name = "CrossFrntX1Y11"
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

    class CrossFrntX1Y17:
        sig_name = "CrossFrntX1Y17"
        sig_start_bit = 135
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
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

    class CrossFrntX1Y36:
        sig_name = "CrossFrntX1Y36"
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

    class CrossFrntX1Y21:
        sig_name = "CrossFrntX1Y21"
        sig_start_bit = 167
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 167
        byte = 20
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class CrossFrntX1Y23:
        sig_name = "CrossFrntX1Y23"
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

    class HiBeamRi:
        sig_name = "HiBeamRi"
        sig_start_bit = 375
        update_id_bit = 368
        sig_length = 7
        sig_value_factor = 1
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

    class CrossFrntX1Y18:
        sig_name = "CrossFrntX1Y18"
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

    class CrossFrntX1Y39:
        sig_name = "CrossFrntX1Y39"
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

    class CrossFrntX1Y7:
        sig_name = "CrossFrntX1Y7"
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

    class CrossFrntX1Y24:
        sig_name = "CrossFrntX1Y24"
        sig_start_bit = 191
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 191
        byte = 23
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class CrossFrntX1Y5:
        sig_name = "CrossFrntX1Y5"
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

    class CrossFrntX1Y31:
        sig_name = "CrossFrntX1Y31"
        sig_start_bit = 247
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 247
        byte = 30
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class CrossFrntX1Y6:
        sig_name = "CrossFrntX1Y6"
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

    class CrossFrntX1Y2:
        sig_name = "CrossFrntX1Y2"
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

    class CrossFrntX1Y30:
        sig_name = "CrossFrntX1Y30"
        sig_start_bit = 239
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 239
        byte = 29
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class CrossFrntX1Y29:
        sig_name = "CrossFrntX1Y29"
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

    class LoBeamRi:
        sig_name = "LoBeamRi"
        sig_start_bit = 391
        update_id_bit = 384
        sig_length = 7
        sig_value_factor = 1
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

    class CrossFrntX1Y19:
        sig_name = "CrossFrntX1Y19"
        sig_start_bit = 151
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 151
        byte = 18
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class CrossFrntX1Y43:
        sig_name = "CrossFrntX1Y43"
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

    class CrossFrntX1Y13:
        sig_name = "CrossFrntX1Y13"
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

    class CrossFrntX1Y34:
        sig_name = "CrossFrntX1Y34"
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

    class CrossFrntX1Y10:
        sig_name = "CrossFrntX1Y10"
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

    class CrossFrntX1Y33:
        sig_name = "CrossFrntX1Y33"
        sig_start_bit = 263
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
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

    class CrossFrntX1Y3:
        sig_name = "CrossFrntX1Y3"
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

    class CrossFrntX1Y35:
        sig_name = "CrossFrntX1Y35"
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

    class CrossFrntX1Y12:
        sig_name = "CrossFrntX1Y12"
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

    class CrossFrntX1Y26:
        sig_name = "CrossFrntX1Y26"
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

    class LoBeamLe:
        sig_name = "LoBeamLe"
        sig_start_bit = 383
        update_id_bit = 376
        sig_length = 7
        sig_value_factor = 1
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

    class CrossFrntX1Y16:
        sig_name = "CrossFrntX1Y16"
        sig_start_bit = 127
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 127
        byte = 15
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class CrossFrntX1Y9:
        sig_name = "CrossFrntX1Y9"
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

    class CrossFrntX1Y15:
        sig_name = "CrossFrntX1Y15"
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

    class CrossFrntX1Y14:
        sig_name = "CrossFrntX1Y14"
        sig_start_bit = 111
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 111
        byte = 13
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class CrossFrntX1Y37:
        sig_name = "CrossFrntX1Y37"
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

    class CrossFrntX1Y44:
        sig_name = "CrossFrntX1Y44"
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

    class CrossFrntX1Y4:
        sig_name = "CrossFrntX1Y4"
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

    class CrossFrntX1Y40:
        sig_name = "CrossFrntX1Y40"
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

    class CrossFrntX1Y45:
        sig_name = "CrossFrntX1Y45"
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

    class CrossFrntX1Y27:
        sig_name = "CrossFrntX1Y27"
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

    class CrossFrntX1Y42:
        sig_name = "CrossFrntX1Y42"
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

    class CrossFrntX1Y25:
        sig_name = "CrossFrntX1Y25"
        sig_start_bit = 199
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
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


class BgmBodyExposedCANFr08:
    msg_name = "BgmBodyExposedCANFr08"
    msg_id = 152
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 64
    tx_node = "BGM"
    rx_nodes = ['RCML']

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


class CemBodyExpoCommonFr08:
    msg_name = "CemBodyExpoCommonFr08"
    msg_id = 128
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCML', 'HCMR']

    class AccrPedlRatCntr_2_CemBodyExpoCommonSignalIPdu08:
        sig_name = "AccrPedlRatCntr_2_CemBodyExpoCommonSignalIPdu08"
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

    class AccrPedlRatChks_2_CemBodyExpoCommonSignalIPdu08:
        sig_name = "AccrPedlRatChks_2_CemBodyExpoCommonSignalIPdu08"
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

    class BrkPedlSnsrQf_1_CemBodyExpoCommonSignalIPdu08:
        sig_name = "BrkPedlSnsrQf_1_CemBodyExpoCommonSignalIPdu08"
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

    class AmbTRawAmbTVal_1_CemBodyExpoCommonSignalIPdu08:
        sig_name = "AmbTRawAmbTVal_1_CemBodyExpoCommonSignalIPdu08"
        sig_start_bit = 50
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = "-70.0"
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

    class BrkPedlSnsrChks_1_CemBodyExpoCommonSignalIPdu08:
        sig_name = "BrkPedlSnsrChks_1_CemBodyExpoCommonSignalIPdu08"
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

    class BrkPedlSnsrCntr_1_CemBodyExpoCommonSignalIPdu08:
        sig_name = "BrkPedlSnsrCntr_1_CemBodyExpoCommonSignalIPdu08"
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

    class AmbTRawQly_1_CemBodyExpoCommonSignalIPdu08:
        sig_name = "AmbTRawQly_1_CemBodyExpoCommonSignalIPdu08"
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

    class BrkPedlSnsrSt_1_CemBodyExpoCommonSignalIPdu08:
        sig_name = "BrkPedlSnsrSt_1_CemBodyExpoCommonSignalIPdu08"
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

    class AccrPedlRatAccrPedlRat_2_CemBodyExpoCommonSignalIPdu08:
        sig_name = "AccrPedlRatAccrPedlRat_2_CemBodyExpoCommonSignalIPdu08"
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


class RcmlToBgmBodyExpoDiagRespFrame:
    msg_name = "RcmlToBgmBodyExpoDiagRespFrame"
    msg_id = 1717
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "RCML"
    rx_nodes = ['BGM']


class RcmmBodyExposedCANNmFr:
    msg_name = "RcmmBodyExposedCANNmFr"
    msg_id = 1333
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "RCMM"
    rx_nodes = []


class CemBodyExpoCommonFr22:
    msg_name = "CemBodyExpoCommonFr22"
    msg_id = 400
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.045
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCML', 'HCMR']

    class SuspPosnVertLvlRe_1_CemBodyExpoCommonSignalIPdu22:
        sig_name = "SuspPosnVertLvlRe_1_CemBodyExpoCommonSignalIPdu22"
        sig_start_bit = 30
        update_id_bit = None
        sig_length = 15
        sig_value_factor = "6.2E-5"
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

    class SuspPosnVertLvlFrntQf_1_CemBodyExpoCommonSignalIPdu22:
        sig_name = "SuspPosnVertLvlFrntQf_1_CemBodyExpoCommonSignalIPdu22"
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

    class SuspPosnVertLvlFrnt_1_CemBodyExpoCommonSignalIPdu22:
        sig_name = "SuspPosnVertLvlFrnt_1_CemBodyExpoCommonSignalIPdu22"
        sig_start_bit = 14
        update_id_bit = None
        sig_length = 15
        sig_value_factor = "6.2E-5"
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

    class SuspPosnVertAgSuspPosnVertAg_1_CemBodyExpoCommonSignalIPdu22:
        sig_name = "SuspPosnVertAgSuspPosnVertAg_1_CemBodyExpoCommonSignalIPdu22"
        sig_start_bit = 43
        update_id_bit = None
        sig_length = 12
        sig_value_factor = "1.278941807E-4"
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

    class SuspPosnVertLvlReQf_1_CemBodyExpoCommonSignalIPdu22:
        sig_name = "SuspPosnVertLvlReQf_1_CemBodyExpoCommonSignalIPdu22"
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

    class SuspPosnVertAgGenQf_1_CemBodyExpoCommonSignalIPdu22:
        sig_name = "SuspPosnVertAgGenQf_1_CemBodyExpoCommonSignalIPdu22"
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


class RcmrToBgmBodyExpoDiagRespFrame:
    msg_name = "RcmrToBgmBodyExpoDiagRespFrame"
    msg_id = 1718
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "RCMR"
    rx_nodes = ['BGM']


class BgmBodyExposedCANFr02:
    msg_name = "BgmBodyExposedCANFr02"
    msg_id = 146
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR', 'HCML', 'RCML', 'RCMR']

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

    class DrvrDesDirCntr_1_BgmBodyExpoSignalIPdu02:
        sig_name = "DrvrDesDirCntr_1_BgmBodyExpoSignalIPdu02"
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

    class DrvrDesDirChks_1_BgmBodyExpoSignalIPdu02:
        sig_name = "DrvrDesDirChks_1_BgmBodyExpoSignalIPdu02"
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

    class DrvrDesDirDrvrDesDir_1_BgmBodyExpoSignalIPdu02:
        sig_name = "DrvrDesDirDrvrDesDir_1_BgmBodyExpoSignalIPdu02"
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


class HcmlBodyExpoFr04:
    msg_name = "HcmlBodyExpoFr04"
    msg_id = 124
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 8
    tx_node = "HCML"
    rx_nodes = ['BGM']

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


class HcmrBodyExpoFr04:
    msg_name = "HcmrBodyExpoFr04"
    msg_id = 127
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 8
    tx_node = "HCMR"
    rx_nodes = ['BGM']

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


class RcmlBodyExpoFr01:
    msg_name = "RcmlBodyExpoFr01"
    msg_id = 592
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 8
    tx_node = "RCML"
    rx_nodes = ['BGM', 'S2SReceiver']

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


class HcmrToBgmBodyExpoDiagRespFrame:
    msg_name = "HcmrToBgmBodyExpoDiagRespFrame"
    msg_id = 1716
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "HCMR"
    rx_nodes = ['BGM']


class EtcToCemBodyExpoDevDiagFr03:
    msg_name = "EtcToCemBodyExpoDevDiagFr03"
    msg_id = 1425
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CCM"
    rx_nodes = ['BGM']

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


class BgmToHcmlBodyExpoDiagReqFrame:
    msg_name = "BgmToHcmlBodyExpoDiagReqFrame"
    msg_id = 1971
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCML']


class HcmltoEtcXCPFr01:
    msg_name = "HcmltoEtcXCPFr01"
    msg_id = 1424
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "HCML"
    rx_nodes = ['CCM']


class RcmrBodyExpoFr01:
    msg_name = "RcmrBodyExpoFr01"
    msg_id = 608
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 8
    tx_node = "RCMR"
    rx_nodes = ['BGM', 'S2SReceiver']

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


class CemBodyExpoCommonFr09:
    msg_name = "CemBodyExpoCommonFr09"
    msg_id = 387
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR', 'HCML', 'RCMM', 'RCML', 'RCMR']

    class VehCfgPrmExtCCPBytePosn5_2_CemBodyExpoCommonSignalIPdu09:
        sig_name = "VehCfgPrmExtCCPBytePosn5_2_CemBodyExpoCommonSignalIPdu09"
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

    class VehCfgPrmExtCCPBytePosn7_2_CemBodyExpoCommonSignalIPdu09:
        sig_name = "VehCfgPrmExtCCPBytePosn7_2_CemBodyExpoCommonSignalIPdu09"
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

    class VehCfgPrmExtCCPBytePosn3_2_CemBodyExpoCommonSignalIPdu09:
        sig_name = "VehCfgPrmExtCCPBytePosn3_2_CemBodyExpoCommonSignalIPdu09"
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

    class VehCfgPrmExtCCPBytePosn6_2_CemBodyExpoCommonSignalIPdu09:
        sig_name = "VehCfgPrmExtCCPBytePosn6_2_CemBodyExpoCommonSignalIPdu09"
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

    class VehCfgPrmExtCCPBytePosn2_2_CemBodyExpoCommonSignalIPdu09:
        sig_name = "VehCfgPrmExtCCPBytePosn2_2_CemBodyExpoCommonSignalIPdu09"
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

    class VehCfgPrmExtCCPBytePosn4_2_CemBodyExpoCommonSignalIPdu09:
        sig_name = "VehCfgPrmExtCCPBytePosn4_2_CemBodyExpoCommonSignalIPdu09"
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

    class VehCfgPrmExtCCPBytePosn8_2_CemBodyExpoCommonSignalIPdu09:
        sig_name = "VehCfgPrmExtCCPBytePosn8_2_CemBodyExpoCommonSignalIPdu09"
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

    class VehCfgPrmExtBlkIDBytePosn1_2_CemBodyExpoCommonSignalIPdu09:
        sig_name = "VehCfgPrmExtBlkIDBytePosn1_2_CemBodyExpoCommonSignalIPdu09"
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


class HcmrtoEtcXCPFr01:
    msg_name = "HcmrtoEtcXCPFr01"
    msg_id = 1426
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "HCMR"
    rx_nodes = ['CCM']


class BgmBodyExposedCANFr09:
    msg_name = "BgmBodyExposedCANFr09"
    msg_id = 153
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 64
    tx_node = "BGM"
    rx_nodes = ['RCML', 'RCMR']

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


class BgmToHcmrBodyExpoDiagReqFrame:
    msg_name = "BgmToHcmrBodyExpoDiagReqFrame"
    msg_id = 1972
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR']


class BgmToRcmlBodyExpoDiagReqFrame:
    msg_name = "BgmToRcmlBodyExpoDiagReqFrame"
    msg_id = 1973
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RCML']


class HcmlBodyExpoFr02:
    msg_name = "HcmlBodyExpoFr02"
    msg_id = 593
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 3
    tx_node = "HCML"
    rx_nodes = ['BGM', 'S2SReceiver']

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


class RcmmToBgmBodyExpoDiagRespFrame:
    msg_name = "RcmmToBgmBodyExpoDiagRespFrame"
    msg_id = 1719
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "RCMM"
    rx_nodes = ['BGM']


class HcmrBodyExpoFr05:
    msg_name = "HcmrBodyExpoFr05"
    msg_id = 272
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.03
    msg_length = 8
    tx_node = "HCMR"
    rx_nodes = ['BGM', 'S2SReceiver']

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


class BgmBodyExposedCANFr10:
    msg_name = "BgmBodyExposedCANFr10"
    msg_id = 154
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 64
    tx_node = "BGM"
    rx_nodes = ['HCMR', 'HCML', 'RCMM', 'RCML', 'RCMR']

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


class CEMBodyExpoCommonFr06:
    msg_name = "CEMBodyExpoCommonFr06"
    msg_id = 512
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HCMR', 'HCML', 'RCMM', 'RCML', 'RCMR']

    class VehBattUSysU_4_CEMBodyExpoCommonSignalIPdu06:
        sig_name = "VehBattUSysU_4_CEMBodyExpoCommonSignalIPdu06"
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

    class VehBattUSysUQf_4_CEMBodyExpoCommonSignalIPdu06:
        sig_name = "VehBattUSysUQf_4_CEMBodyExpoCommonSignalIPdu06"
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

    class BkpOfDstTrvld_3_CEMBodyExpoCommonSignalIPdu06:
        sig_name = "BkpOfDstTrvld_3_CEMBodyExpoCommonSignalIPdu06"
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


