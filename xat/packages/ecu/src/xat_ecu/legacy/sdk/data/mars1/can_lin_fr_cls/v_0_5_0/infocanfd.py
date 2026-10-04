class BgmInfoCANFDNmFr:
    msg_name = "BgmInfoCANFDNmFr"
    msg_id = 1281
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['CDC']


class BgmInfoCanFdFr19:
    msg_name = "BgmInfoCanFdFr19"
    msg_id = 789
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.045
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['CDC']

    class VehTiAndDataHr1_3_BgmInfoCanFdSignalIPdu19:
        sig_name = "VehTiAndDataHr1_3_BgmInfoCanFdSignalIPdu19"
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

    class VehTiAndDataDay_3_BgmInfoCanFdSignalIPdu19:
        sig_name = "VehTiAndDataDay_3_BgmInfoCanFdSignalIPdu19"
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

    class VehTiAndDataSec1_3_BgmInfoCanFdSignalIPdu19:
        sig_name = "VehTiAndDataSec1_3_BgmInfoCanFdSignalIPdu19"
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

    class VehTiAndDataDataValid_3_BgmInfoCanFdSignalIPdu19:
        sig_name = "VehTiAndDataDataValid_3_BgmInfoCanFdSignalIPdu19"
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

    class VehTiAndDataYr1_3_BgmInfoCanFdSignalIPdu19:
        sig_name = "VehTiAndDataYr1_3_BgmInfoCanFdSignalIPdu19"
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

    class VehTiAndDataMth1_3_BgmInfoCanFdSignalIPdu19:
        sig_name = "VehTiAndDataMth1_3_BgmInfoCanFdSignalIPdu19"
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

    class VehTiAndDataMins1_3_BgmInfoCanFdSignalIPdu19:
        sig_name = "VehTiAndDataMins1_3_BgmInfoCanFdSignalIPdu19"
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


class BgmInfoCanFdFr02:
    msg_name = "BgmInfoCanFdFr02"
    msg_id = 773
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 1.0
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['BGM']

    class SteerWhlTouchBdADAS_2_BgmInfoCanFdSignalIPdu02:
        sig_name = "SteerWhlTouchBdADAS_2_BgmInfoCanFdSignalIPdu02"
        sig_start_bit = 7
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
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class SteerWhlTouchBdCnclQf1_2_BgmInfoCanFdSignalIPdu02:
        sig_name = "SteerWhlTouchBdCnclQf1_2_BgmInfoCanFdSignalIPdu02"
        sig_start_bit = 45
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
        startbit = 45
        byte = 5
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class SteerWhlTouchBdCnclCntr_2_BgmInfoCanFdSignalIPdu02:
        sig_name = "SteerWhlTouchBdCnclCntr_2_BgmInfoCanFdSignalIPdu02"
        sig_start_bit = 43
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

    class SteerWhlTouchBdCnclSteerWhlTouchBdSts_2_BgmInfoCanFdSignalIPdu02:
        sig_name = "SteerWhlTouchBdCnclSteerWhlTouchBdSts_2_BgmInfoCanFdSignalIPdu02"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class SteerWhlTouchBdCnclChks_2_BgmInfoCanFdSignalIPdu02:
        sig_name = "SteerWhlTouchBdCnclChks_2_BgmInfoCanFdSignalIPdu02"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
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

    class SteerWhlTouchBdCrsResuQf1_2_BgmInfoCanFdSignalIPdu02:
        sig_name = "SteerWhlTouchBdCrsResuQf1_2_BgmInfoCanFdSignalIPdu02"
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

    class SteerWhlTouchBdCrsResuSteerWhlTouchBdSts_2_BgmInfoCanFdSignalIPdu02:
        sig_name = "SteerWhlTouchBdCrsResuSteerWhlTouchBdSts_2_BgmInfoCanFdSignalIPdu02"
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


class BgmInfoCanFdFr17:
    msg_name = "BgmInfoCanFdFr17"
    msg_id = 800
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.03
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['BGM', 'CDC']

    class FuSnsrActvSideGenQF:
        sig_name = "FuSnsrActvSideGenQF"
        sig_start_bit = 12
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
        startbit = 12
        byte = 1
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class FuSnsrActvSideFuLvlSnsrRawVal:
        sig_name = "FuSnsrActvSideFuLvlSnsrRawVal"
        sig_start_bit = 7
        sig_length = 11
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11100000, 0b00011111, 3, 5)]

    class IndirectLifeDetnAndCareDiWarn:
        sig_name = "IndirectLifeDetnAndCareDiWarn"
        sig_start_bit = 29
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Warn2_NoWarn': 0, 'Warn2_Warn': 1}
        compute_method = None
        length = 1
        startbit = 29
        byte = 3
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class FuSnsrPasSideFuLvlSnsrRawVal:
        sig_name = "FuSnsrPasSideFuLvlSnsrRawVal"
        sig_start_bit = 10
        sig_length = 11
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 10
        bmuws_info = [(1, 0b00000111, 0b11111000, 3, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class IndirectLifeDetnAndCareLvl1Warn:
        sig_name = "IndirectLifeDetnAndCareLvl1Warn"
        sig_start_bit = 28
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Warn2_NoWarn': 0, 'Warn2_Warn': 1}
        compute_method = None
        length = 1
        startbit = 28
        byte = 3
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class FuSnsrPasSideGenQF:
        sig_name = "FuSnsrPasSideGenQF"
        sig_start_bit = 31
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

    class WhlSpdCmpFac_1_BgmInfoCanFdSignalIPdu17:
        sig_name = "WhlSpdCmpFac_1_BgmInfoCanFdSignalIPdu17"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111000
        unmask = 0b00000111
        shift = 3


class CdcInfoCANFDNmFr:
    msg_name = "CdcInfoCANFDNmFr"
    msg_id = 1282
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CDC"
    rx_nodes = ['BGM']


class CdcInfoCanFdFr04:
    msg_name = "CdcInfoCanFdFr04"
    msg_id = 256
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.06
    msg_length = 8
    tx_node = "CDC"
    rx_nodes = ['BGM']

    class AsySftyHWLReqBkp:
        sig_name = "AsySftyHWLReqBkp"
        sig_start_bit = 39
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AsySftyHWLReq_NoRequest': 0, 'AsySftyHWLReq_TurnOn': 1, 'AsySftyHWLReq_TurnOff': 2, 'AsySftyHWLReq_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 39
        byte = 4
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class FaceIdnResForProfYesNo:
        sig_name = "FaceIdnResForProfYesNo"
        sig_start_bit = 3
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
        startbit = 3
        byte = 0
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class FaceIdnStsMsg:
        sig_name = "FaceIdnStsMsg"
        sig_start_bit = 2
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FaceIdnStsMsg_unavailable': 0, 'FaceIdnStsMsg_notDetected': 1, 'FaceIdnStsMsg_detectedButNotRecognized': 2, 'FaceIdnStsMsg_detectedAndRecognized': 3}
        compute_method = None
        length = 2
        startbit = 2
        byte = 0
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class LiLvrDiagc:
        sig_name = "LiLvrDiagc"
        sig_start_bit = 15
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 3
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LiLvrDiagc_LiLvrNotConnect': 0, 'LiLvrDiagc_LiLvrBtnStuck': 1, 'LiLvrDiagc_LiLvrSwtUndefd': 2, 'LiLvrDiagc_LiLvrOk': 3}
        compute_method = None
        length = 2
        startbit = 15
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class FaceIdnResForProfIdPen:
        sig_name = "FaceIdnResForProfIdPen"
        sig_start_bit = 7
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'IdPen_ProfUkwn': 0, 'IdPen_Prof1': 1, 'IdPen_Prof2': 2, 'IdPen_Prof3': 3, 'IdPen_Prof4': 4, 'IdPen_Prof5': 5, 'IdPen_Prof6': 6, 'IdPen_Prof7': 7, 'IdPen_Prof8': 8, 'IdPen_Prof9': 9, 'IdPen_Prof10': 10, 'IdPen_Prof11': 11, 'IdPen_Prof12': 12, 'IdPen_Prof13': 13, 'IdPen_Resd14': 14, 'IdPen_ProfAll': 15}
        compute_method = None
        length = 4
        startbit = 7
        byte = 0
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4


class CdcInfoCanFdFr09:
    msg_name = "CdcInfoCanFdFr09"
    msg_id = 517
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.03
    msg_length = 8
    tx_node = "CDC"
    rx_nodes = ['BGM']

    class AsySecChStsADModActvnCfm_0_CdcInfoCanFdSignalIPdu09:
        sig_name = "AsySecChStsADModActvnCfm_0_CdcInfoCanFdSignalIPdu09"
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

    class AsySecChFltStsReserved2_0_CdcInfoCanFdSignalIPdu09:
        sig_name = "AsySecChFltStsReserved2_0_CdcInfoCanFdSignalIPdu09"
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

    class AsySecChStsReserved1_0_CdcInfoCanFdSignalIPdu09:
        sig_name = "AsySecChStsReserved1_0_CdcInfoCanFdSignalIPdu09"
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

    class AsySecChFltStsReserved1_0_CdcInfoCanFdSignalIPdu09:
        sig_name = "AsySecChFltStsReserved1_0_CdcInfoCanFdSignalIPdu09"
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

    class AsySecChStsADModDeactvnCfm_0_CdcInfoCanFdSignalIPdu09:
        sig_name = "AsySecChStsADModDeactvnCfm_0_CdcInfoCanFdSignalIPdu09"
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

    class AsySecChFltStsChks_0_CdcInfoCanFdSignalIPdu09:
        sig_name = "AsySecChFltStsChks_0_CdcInfoCanFdSignalIPdu09"
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

    class AsySecChFltStsPNCSysFailr_0_CdcInfoCanFdSignalIPdu09:
        sig_name = "AsySecChFltStsPNCSysFailr_0_CdcInfoCanFdSignalIPdu09"
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

    class AsySecChStsReserved3_0_CdcInfoCanFdSignalIPdu09:
        sig_name = "AsySecChStsReserved3_0_CdcInfoCanFdSignalIPdu09"
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

    class AsySecChFltStsReserved4_0_CdcInfoCanFdSignalIPdu09:
        sig_name = "AsySecChFltStsReserved4_0_CdcInfoCanFdSignalIPdu09"
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

    class AsySecChStsChks_0_CdcInfoCanFdSignalIPdu09:
        sig_name = "AsySecChStsChks_0_CdcInfoCanFdSignalIPdu09"
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

    class AsySecChFltStsReserved3_0_CdcInfoCanFdSignalIPdu09:
        sig_name = "AsySecChFltStsReserved3_0_CdcInfoCanFdSignalIPdu09"
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

    class AsySecChStsCntr_0_CdcInfoCanFdSignalIPdu09:
        sig_name = "AsySecChStsCntr_0_CdcInfoCanFdSignalIPdu09"
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

    class AsySecChFltStsCntr_0_CdcInfoCanFdSignalIPdu09:
        sig_name = "AsySecChFltStsCntr_0_CdcInfoCanFdSignalIPdu09"
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

    class AsySecChFltStsPerceptionSysFailr_0_CdcInfoCanFdSignalIPdu09:
        sig_name = "AsySecChFltStsPerceptionSysFailr_0_CdcInfoCanFdSignalIPdu09"
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

    class AsySecChFltStsReserved5_0_CdcInfoCanFdSignalIPdu09:
        sig_name = "AsySecChFltStsReserved5_0_CdcInfoCanFdSignalIPdu09"
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

    class AsySecChStsSecCtrlrSts_0_CdcInfoCanFdSignalIPdu09:
        sig_name = "AsySecChStsSecCtrlrSts_0_CdcInfoCanFdSignalIPdu09"
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

    class AsySecChFltStsReserved6_0_CdcInfoCanFdSignalIPdu09:
        sig_name = "AsySecChFltStsReserved6_0_CdcInfoCanFdSignalIPdu09"
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

    class AsySecChStsReserved2_0_CdcInfoCanFdSignalIPdu09:
        sig_name = "AsySecChStsReserved2_0_CdcInfoCanFdSignalIPdu09"
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

    class AsySecChStsReserved4_0_CdcInfoCanFdSignalIPdu09:
        sig_name = "AsySecChStsReserved4_0_CdcInfoCanFdSignalIPdu09"
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


class BgmInfoCanFdFr20:
    msg_name = "BgmInfoCanFdFr20"
    msg_id = 821
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.07
    msg_length = 32
    tx_node = "BGM"
    rx_nodes = ['CDC']

    class SnsrFltFrntShoSideLe_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "SnsrFltFrntShoSideLe_1_BgmInfoCanFdSignalIPdu20"
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

    class AudWarnLvOfSnsrParkAssiLe_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "AudWarnLvOfSnsrParkAssiLe_1_BgmInfoCanFdSignalIPdu20"
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

    class SnsrFltReShoSideRi_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "SnsrFltReShoSideRi_1_BgmInfoCanFdSignalIPdu20"
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

    class OutdSnsrFltReShoRi_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "OutdSnsrFltReShoRi_1_BgmInfoCanFdSignalIPdu20"
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

    class FrntLeOfSideDoor_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "FrntLeOfSideDoor_1_BgmInfoCanFdSignalIPdu20"
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

    class AudWarnOfSnsrParkAssiRePosn_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "AudWarnOfSnsrParkAssiRePosn_1_BgmInfoCanFdSignalIPdu20"
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

    class SnsrFltOfPrkgDstCtrl_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "SnsrFltOfPrkgDstCtrl_1_BgmInfoCanFdSignalIPdu20"
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

    class FrntLeOfSnsrOfPrkgAssiSide_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "FrntLeOfSnsrOfPrkgAssiSide_1_BgmInfoCanFdSignalIPdu20"
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

    class ReRiOfSideDoor_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "ReRiOfSideDoor_1_BgmInfoCanFdSignalIPdu20"
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

    class InsdSnsrFltFrntShoRi_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "InsdSnsrFltFrntShoRi_1_BgmInfoCanFdSignalIPdu20"
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

    class SnsrFltFrntShoSideRi_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "SnsrFltFrntShoSideRi_1_BgmInfoCanFdSignalIPdu20"
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

    class ReLeOfSnsrOfPrkgAssiSide_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "ReLeOfSnsrOfPrkgAssiSide_1_BgmInfoCanFdSignalIPdu20"
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

    class OutdRiOfSnsrPrkgAssiRe_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "OutdRiOfSnsrPrkgAssiRe_1_BgmInfoCanFdSignalIPdu20"
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

    class AudWarnOfSnsrParkAssiLePosn_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "AudWarnOfSnsrParkAssiLePosn_1_BgmInfoCanFdSignalIPdu20"
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

    class PrkgDstCtrlWarn_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "PrkgDstCtrlWarn_1_BgmInfoCanFdSignalIPdu20"
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

    class OutdLeOfSnsrPrkgAssiRe_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "OutdLeOfSnsrPrkgAssiRe_1_BgmInfoCanFdSignalIPdu20"
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

    class OutdSnsrFltFrntShoLe_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "OutdSnsrFltFrntShoLe_1_BgmInfoCanFdSignalIPdu20"
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

    class InsdRiOfSnsrPrkgAssiRe_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "InsdRiOfSnsrPrkgAssiRe_1_BgmInfoCanFdSignalIPdu20"
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

    class AudWarnOfSnsrParkAssiFrntPosn_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "AudWarnOfSnsrParkAssiFrntPosn_1_BgmInfoCanFdSignalIPdu20"
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

    class OutdSnsrFltReShoLe_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "OutdSnsrFltReShoLe_1_BgmInfoCanFdSignalIPdu20"
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

    class InsdSnsrFltReShoLe_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "InsdSnsrFltReShoLe_1_BgmInfoCanFdSignalIPdu20"
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

    class AudWarnLvOfSnsrParkAssiFrnt_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "AudWarnLvOfSnsrParkAssiFrnt_1_BgmInfoCanFdSignalIPdu20"
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

    class SnsrFltReShoSideLe_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "SnsrFltReShoSideLe_1_BgmInfoCanFdSignalIPdu20"
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

    class OutdLeOfSnsrPrkgAssiFrnt_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "OutdLeOfSnsrPrkgAssiFrnt_1_BgmInfoCanFdSignalIPdu20"
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

    class PrkgDstCtrlSts_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "PrkgDstCtrlSts_1_BgmInfoCanFdSignalIPdu20"
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

    class AudWarnLvOfSnsrParkAssiRe_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "AudWarnLvOfSnsrParkAssiRe_1_BgmInfoCanFdSignalIPdu20"
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

    class ReLeOfSideDoor_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "ReLeOfSideDoor_1_BgmInfoCanFdSignalIPdu20"
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

    class InsdSnsrFltReShoRi_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "InsdSnsrFltReShoRi_1_BgmInfoCanFdSignalIPdu20"
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

    class FrntRiOfSnsrOfPrkgAssiSide_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "FrntRiOfSnsrOfPrkgAssiSide_1_BgmInfoCanFdSignalIPdu20"
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

    class OutdRiOfSnsrPrkgAssiFrnt_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "OutdRiOfSnsrPrkgAssiFrnt_1_BgmInfoCanFdSignalIPdu20"
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

    class InsdLeOfSnsrPrkgAssiRe_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "InsdLeOfSnsrPrkgAssiRe_1_BgmInfoCanFdSignalIPdu20"
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

    class AudWarnOfSnsrParkAssiRgtPosn_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "AudWarnOfSnsrParkAssiRgtPosn_1_BgmInfoCanFdSignalIPdu20"
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

    class AudWarnLvOfSnsrParkAssiRgt_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "AudWarnLvOfSnsrParkAssiRgt_1_BgmInfoCanFdSignalIPdu20"
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

    class InsdSnsrFltFrntShoLe_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "InsdSnsrFltFrntShoLe_1_BgmInfoCanFdSignalIPdu20"
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

    class OutdSnsrFltFrntShoRi_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "OutdSnsrFltFrntShoRi_1_BgmInfoCanFdSignalIPdu20"
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

    class ReRiOfSnsrOfPrkgAssiSide_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "ReRiOfSnsrOfPrkgAssiSide_1_BgmInfoCanFdSignalIPdu20"
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

    class FrntRiOfSideDoor_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "FrntRiOfSideDoor_1_BgmInfoCanFdSignalIPdu20"
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

    class InsdLeOfSnsrPrkgAssiFrnt_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "InsdLeOfSnsrPrkgAssiFrnt_1_BgmInfoCanFdSignalIPdu20"
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

    class InsdRiOfSnsrPrkgAssiFrnt_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "InsdRiOfSnsrPrkgAssiFrnt_1_BgmInfoCanFdSignalIPdu20"
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


class BgmInfoCanFdFr18:
    msg_name = "BgmInfoCanFdFr18"
    msg_id = 528
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['CDC']

    class CarTiGlb_4_BgmInfoCanFdSignalIPdu18:
        sig_name = "CarTiGlb_4_BgmInfoCanFdSignalIPdu18"
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


class CdcInfoCanFdFr03:
    msg_name = "CdcInfoCanFdFr03"
    msg_id = 768
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.06
    msg_length = 8
    tx_node = "CDC"
    rx_nodes = ['BGM']

    class DiagcSigSWM:
        sig_name = "DiagcSigSWM"
        sig_start_bit = 4
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Nofault': 0, 'Commonfailure': 1, 'KL30overvoltage': 2, 'HSSovercurInSWSorhartoSWS': 3}
        compute_method = None
        length = 2
        startbit = 4
        byte = 0
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class MmedHdPwrMod:
        sig_name = "MmedHdPwrMod"
        sig_start_bit = 39
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'MmedMaiPwrMod_IHUStateSleep': 0, 'MmedMaiPwrMod_IHUStateStandby': 1, 'MmedMaiPwrMod_IHUStatePartial': 2, 'MmedMaiPwrMod_IHUStateOn': 3}
        compute_method = None
        length = 2
        startbit = 39
        byte = 4
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class CdcInfoCanFdFr01:
    msg_name = "CdcInfoCanFdFr01"
    msg_id = 48
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "CDC"
    rx_nodes = ['BGM']

    class ActvnOfSteerWhlIllmn_0_CdcInfoCanFdSignalIPdu01:
        sig_name = "ActvnOfSteerWhlIllmn_0_CdcInfoCanFdSignalIPdu01"
        sig_start_bit = 43
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
        startbit = 43
        byte = 5
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3


class BgmInfoCanFdFr12:
    msg_name = "BgmInfoCanFdFr12"
    msg_id = 56
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.8
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['CDC']

    class DiagcFailrTouchPanSWTRVibrationFltSts_1_BgmInfoCanFdSignalIPdu12:
        sig_name = "DiagcFailrTouchPanSWTRVibrationFltSts_1_BgmInfoCanFdSignalIPdu12"
        sig_start_bit = 1
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltSts_NoFlt': 0, 'FltSts_VibrationShoCirc': 1, 'FltSts_VibrationOpenCirc': 2, 'FltSts_invalid': 3}
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class DiagcFailrTouchPanSWTRSnsrFltSts_1_BgmInfoCanFdSignalIPdu12:
        sig_name = "DiagcFailrTouchPanSWTRSnsrFltSts_1_BgmInfoCanFdSignalIPdu12"
        sig_start_bit = 6
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SnsrFltSts_NoFlt': 0, 'SnsrFltSts_FSnsrInvld': 1, 'SnsrFltSts_FSnsrShoCircToGnd': 2, 'SnsrFltSts_FSnsrShoCircToBatt': 3, 'SnsrFltSts_FSnsrOpenCirc': 4}
        compute_method = None
        length = 3
        startbit = 6
        byte = 0
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class DiagcFailrTouchPanSWTRCmnFltSts_1_BgmInfoCanFdSignalIPdu12:
        sig_name = "DiagcFailrTouchPanSWTRCmnFltSts_1_BgmInfoCanFdSignalIPdu12"
        sig_start_bit = 7
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CmnFltSts_NoFlt': 0, 'CmnFltSts_OutdURng': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class DiagcFailrTouchPanSWTRTouchdFltSts_1_BgmInfoCanFdSignalIPdu12:
        sig_name = "DiagcFailrTouchPanSWTRTouchdFltSts_1_BgmInfoCanFdSignalIPdu12"
        sig_start_bit = 3
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltSts_NoFlt': 0, 'FltSts_TouchdInvld': 1, 'FltSts_TouchdOutdOfRng': 2}
        compute_method = None
        length = 2
        startbit = 3
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2


class BgmInfoCanFdFr06:
    msg_name = "BgmInfoCanFdFr06"
    msg_id = 52
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.8
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['CDC']

    class DiagcFailrTouchPanSWTLSnsrFltSts_1_BgmInfoCanFdSignalIPdu06:
        sig_name = "DiagcFailrTouchPanSWTLSnsrFltSts_1_BgmInfoCanFdSignalIPdu06"
        sig_start_bit = 6
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SnsrFltSts_NoFlt': 0, 'SnsrFltSts_FSnsrInvld': 1, 'SnsrFltSts_FSnsrShoCircToGnd': 2, 'SnsrFltSts_FSnsrShoCircToBatt': 3, 'SnsrFltSts_FSnsrOpenCirc': 4}
        compute_method = None
        length = 3
        startbit = 6
        byte = 0
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class DiagcFailrTouchPanSWTLCmnFltSts_1_BgmInfoCanFdSignalIPdu06:
        sig_name = "DiagcFailrTouchPanSWTLCmnFltSts_1_BgmInfoCanFdSignalIPdu06"
        sig_start_bit = 7
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CmnFltSts_NoFlt': 0, 'CmnFltSts_OutdURng': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class DiagcFailrTouchPanSWTLVibrationFltSts_1_BgmInfoCanFdSignalIPdu06:
        sig_name = "DiagcFailrTouchPanSWTLVibrationFltSts_1_BgmInfoCanFdSignalIPdu06"
        sig_start_bit = 1
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltSts_NoFlt': 0, 'FltSts_VibrationShoCirc': 1, 'FltSts_VibrationOpenCirc': 2, 'FltSts_invalid': 3}
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class DiagcFailrTouchPanSWTLTouchdFltSts_1_BgmInfoCanFdSignalIPdu06:
        sig_name = "DiagcFailrTouchPanSWTLTouchdFltSts_1_BgmInfoCanFdSignalIPdu06"
        sig_start_bit = 3
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltSts_NoFlt': 0, 'FltSts_TouchdInvld': 1, 'FltSts_TouchdOutdOfRng': 2}
        compute_method = None
        length = 2
        startbit = 3
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2


