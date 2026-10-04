class AsdmPassSafeCANFr11:
    msg_name = "AsdmPassSafeCANFr11"
    msg_id = 815
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.085
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RML']

    class BkpOfDstTrvld_0_AsdmPassSafeCANSignalIPdu11:
        sig_name = "BkpOfDstTrvld_0_AsdmPassSafeCANSignalIPdu11"
        sig_start_bit = 20
        update_id_bit = 21
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
        startbit = 20
        bmuws_info = [(2, 0b00011111, 0b11100000, 5, 0), (3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111111, 0b00000000, 8, 0)]


class BgmPassiveSafetyCANNmFr:
    msg_name = "BgmPassiveSafetyCANNmFr"
    msg_id = 1281
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['SRS']


class AsdmPassSafeCANFr18:
    msg_name = "AsdmPassSafeCANFr18"
    msg_id = 118
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.04
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RML']

    class GearLvrIndcn_1_AsdmPassSafeCANSignalIPdu18:
        sig_name = "GearLvrIndcn_1_AsdmPassSafeCANSignalIPdu18"
        sig_start_bit = 54
        update_id_bit = 55
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 7
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GearLvrIndcn2_ParkIndcn': 0, 'GearLvrIndcn2_RvsIndcn': 1, 'GearLvrIndcn2_NeutIndcn': 2, 'GearLvrIndcn2_DrvIndcn': 3, 'GearLvrIndcn2_ManModeIndcn': 4, 'GearLvrIndcn2_Resd1': 5, 'GearLvrIndcn2_Resd2': 6, 'GearLvrIndcn2_Undefd': 7}
        compute_method = None
        length = 3
        startbit = 54
        byte = 6
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4


class BgmToRmlPassSafeDiagReqFrame:
    msg_name = "BgmToRmlPassSafeDiagReqFrame"
    msg_id = 1808
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RML']


class AsdmPassSafeCANFr16:
    msg_name = "AsdmPassSafeCANFr16"
    msg_id = 288
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RML']

    class VehSpdLgtChks_1_AsdmPassSafeCANSignalIPdu16:
        sig_name = "VehSpdLgtChks_1_AsdmPassSafeCANSignalIPdu16"
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

    class VehSpdLgtA_1_AsdmPassSafeCANSignalIPdu16:
        sig_name = "VehSpdLgtA_1_AsdmPassSafeCANSignalIPdu16"
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

    class VehSpdLgtCntr_1_AsdmPassSafeCANSignalIPdu16:
        sig_name = "VehSpdLgtCntr_1_AsdmPassSafeCANSignalIPdu16"
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

    class VehSpdLgtQf_1_AsdmPassSafeCANSignalIPdu16:
        sig_name = "VehSpdLgtQf_1_AsdmPassSafeCANSignalIPdu16"
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


class AsdmPassSafeCANFr29:
    msg_name = "AsdmPassSafeCANFr29"
    msg_id = 528
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.12
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RML']

    class ADTakeoverReqGroupCntr_1_AsdmPassSafeCANSignalIPdu29:
        sig_name = "ADTakeoverReqGroupCntr_1_AsdmPassSafeCANSignalIPdu29"
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

    class ADTakeoverReqGroupADTakeoverMsg_1_AsdmPassSafeCANSignalIPdu29:
        sig_name = "ADTakeoverReqGroupADTakeoverMsg_1_AsdmPassSafeCANSignalIPdu29"
        sig_start_bit = 6
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TakeoverMsg_NoRequest': 0, 'TakeoverMsg_Inattention': 1, 'TakeoverMsg_TakeoverRequest': 2, 'TakeoverMsg_SpeedReduce': 3, 'TakeoverMsg_SafeStop': 4, 'TakeoverMsg_AEB': 5, 'TakeoverMsg_Reserved2': 6, 'TakeoverMsg_Reserved3': 7}
        compute_method = None
        length = 3
        startbit = 6
        byte = 0
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class ADTakeoverReqGroupADTakeoverAudio_1_AsdmPassSafeCANSignalIPdu29:
        sig_name = "ADTakeoverReqGroupADTakeoverAudio_1_AsdmPassSafeCANSignalIPdu29"
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
        sig_value_table = {'LowHigh_NoRequest': 0, 'LowHigh_Low': 1, 'LowHigh_High': 2, 'LowHigh_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 23
        byte = 2
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class ADTakeoverReqGroupChks_1_AsdmPassSafeCANSignalIPdu29:
        sig_name = "ADTakeoverReqGroupChks_1_AsdmPassSafeCANSignalIPdu29"
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


class RmlPassSafeCANDevFr01:
    msg_name = "RmlPassSafeCANDevFr01"
    msg_id = 1425
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "RML"
    rx_nodes = ['CCM']

    class RMLdevelpsignalgroupFunctiondevpsignalgroup2:
        sig_name = "RMLdevelpsignalgroupFunctiondevpsignalgroup2"
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

    class RMLdevelpsignalgroupFunctiondevpsignalgroup8:
        sig_name = "RMLdevelpsignalgroupFunctiondevpsignalgroup8"
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

    class RMLdevelpsignalgroupFunctiondevpsignalgroup1:
        sig_name = "RMLdevelpsignalgroupFunctiondevpsignalgroup1"
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

    class RMLdevelpsignalgroupFunctiondevpsignalgroup6:
        sig_name = "RMLdevelpsignalgroupFunctiondevpsignalgroup6"
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

    class RMLdevelpsignalgroupFunctiondevpsignalgroup5:
        sig_name = "RMLdevelpsignalgroupFunctiondevpsignalgroup5"
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

    class RMLdevelpsignalgroupFunctiondevpsignalgroup4:
        sig_name = "RMLdevelpsignalgroupFunctiondevpsignalgroup4"
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

    class RMLdevelpsignalgroupFunctiondevpsignalgroup3:
        sig_name = "RMLdevelpsignalgroupFunctiondevpsignalgroup3"
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

    class RMLdevelpsignalgroupFunctiondevpsignalgroup7:
        sig_name = "RMLdevelpsignalgroupFunctiondevpsignalgroup7"
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


class SrsPassSafeCANFr01:
    msg_name = "SrsPassSafeCANFr01"
    msg_id = 137
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.06
    msg_length = 8
    tx_node = "SRS"
    rx_nodes = ['RML']

    class AgDataRawSafeYawRateQf_1_SrsPassSafeCANSignalIPdu01:
        sig_name = "AgDataRawSafeYawRateQf_1_SrsPassSafeCANSignalIPdu01"
        sig_start_bit = 49
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
        startbit = 49
        byte = 6
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class AgDataRawSafeYawRate_1_SrsPassSafeCANSignalIPdu01:
        sig_name = "AgDataRawSafeYawRate_1_SrsPassSafeCANSignalIPdu01"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 16
        sig_value_factor = "2.44140625E-4"
        sig_value_offset = 0.0
        sig_value_min = -24576
        sig_value_max = 24576
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111111, 0b00000000, 8, 0)]

    class BltLockStAtDrvrBltLockSts:
        sig_name = "BltLockStAtDrvrBltLockSts"
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
        sig_value_table = {'DevErrSts2_NoFlt': 0, 'DevErrSts2_Flt': 1}
        compute_method = None
        length = 1
        startbit = 56
        byte = 7
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class BltLockStAtDrvrBltLockSt1:
        sig_name = "BltLockStAtDrvrBltLockSt1"
        sig_start_bit = 57
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BltLockSt1_Unlock': 0, 'BltLockSt1_Lock': 1}
        compute_method = None
        length = 1
        startbit = 57
        byte = 7
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class BltLockStAtPassBltLockSt1_0_SRSBackBoneSignalIPdu04:
        sig_name = "BltLockStAtPassBltLockSt1_0_SRSBackBoneSignalIPdu04"
        sig_start_bit = 63
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BltLockSt1_Unlock': 0, 'BltLockSt1_Lock': 1}
        compute_method = None
        length = 1
        startbit = 63
        byte = 7
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class AgDataRawSafeChks_1_SrsPassSafeCANSignalIPdu01:
        sig_name = "AgDataRawSafeChks_1_SrsPassSafeCANSignalIPdu01"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 255
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BltCrashNotifDrvr:
        sig_name = "BltCrashNotifDrvr"
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
        sig_value_table = {'NoYesCrit1_NotVld1': 0, 'NoYesCrit1_No': 1, 'NoYesCrit1_Yes': 2, 'NoYesCrit1_NotVld2': 3}
        compute_method = None
        length = 2
        startbit = 3
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class AgDataRawSafeRollRate_1_SrsPassSafeCANSignalIPdu01:
        sig_name = "AgDataRawSafeRollRate_1_SrsPassSafeCANSignalIPdu01"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 16
        sig_value_factor = "2.44140625E-4"
        sig_value_offset = 0.0
        sig_value_min = -24576
        sig_value_max = 24576
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 15
        bmuws_info = [(1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class BltCrashNotifPass:
        sig_name = "BltCrashNotifPass"
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
        sig_value_table = {'NoYesCrit1_NotVld1': 0, 'NoYesCrit1_No': 1, 'NoYesCrit1_Yes': 2, 'NoYesCrit1_NotVld2': 3}
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class AgDataRawSafeRollRateQf_1_SrsPassSafeCANSignalIPdu01:
        sig_name = "AgDataRawSafeRollRateQf_1_SrsPassSafeCANSignalIPdu01"
        sig_start_bit = 51
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
        startbit = 51
        byte = 6
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class AgDataRawSafeCntr_1_SrsPassSafeCANSignalIPdu01:
        sig_name = "AgDataRawSafeCntr_1_SrsPassSafeCANSignalIPdu01"
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

    class BltLockStAtPassBltLockSts_0_SRSBackBoneSignalIPdu04:
        sig_name = "BltLockStAtPassBltLockSts_0_SRSBackBoneSignalIPdu04"
        sig_start_bit = 62
        update_id_bit = None
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
        startbit = 62
        byte = 7
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6


class RmlPassSafeCANFrame1:
    msg_name = "RmlPassSafeCANFrame1"
    msg_id = 339
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.055
    msg_length = 8
    tx_node = "RML"
    rx_nodes = ['BGM', 'SRS']

    class StsForRtrctrRvsbLe:
        sig_name = "StsForRtrctrRvsbLe"
        sig_start_bit = 5
        update_id_bit = 8
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NotOkOk_NotOk': 0, 'NotOkOk_Ok': 1, 'NotOkOk_Di': 2, 'NotOkOk_Resd': 3}
        compute_method = None
        length = 2
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class ActvnStsOfRtrctrRvsbLe:
        sig_name = "ActvnStsOfRtrctrRvsbLe"
        sig_start_bit = 3
        update_id_bit = 6
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Enumeration1_NotActvd': 0, 'Enumeration1_Actvd': 1}
        compute_method = None
        length = 1
        startbit = 3
        byte = 0
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class MsgReqForRtrctrRvsbLe:
        sig_name = "MsgReqForRtrctrRvsbLe"
        sig_start_bit = 9
        update_id_bit = 7
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
        startbit = 9
        byte = 1
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1


class RmlToEtcXcpFr01:
    msg_name = "RmlToEtcXcpFr01"
    msg_id = 1410
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "RML"
    rx_nodes = ['CCM']


class AsdmPassSafeCANFr09:
    msg_name = "AsdmPassSafeCANFr09"
    msg_id = 781
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RML']

    class VehCfgPrmCCPBytePosn3_0_AsdmPassSafeCANSignalIPdu09:
        sig_name = "VehCfgPrmCCPBytePosn3_0_AsdmPassSafeCANSignalIPdu09"
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

    class VehCfgPrmCCPBytePosn6_0_AsdmPassSafeCANSignalIPdu09:
        sig_name = "VehCfgPrmCCPBytePosn6_0_AsdmPassSafeCANSignalIPdu09"
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

    class VehCfgPrmCCPBytePosn4_0_AsdmPassSafeCANSignalIPdu09:
        sig_name = "VehCfgPrmCCPBytePosn4_0_AsdmPassSafeCANSignalIPdu09"
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

    class VehCfgPrmBlkIDBytePosn1_0_AsdmPassSafeCANSignalIPdu09:
        sig_name = "VehCfgPrmBlkIDBytePosn1_0_AsdmPassSafeCANSignalIPdu09"
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

    class VehCfgPrmCCPBytePosn2_0_AsdmPassSafeCANSignalIPdu09:
        sig_name = "VehCfgPrmCCPBytePosn2_0_AsdmPassSafeCANSignalIPdu09"
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

    class VehCfgPrmCCPBytePosn7_0_AsdmPassSafeCANSignalIPdu09:
        sig_name = "VehCfgPrmCCPBytePosn7_0_AsdmPassSafeCANSignalIPdu09"
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

    class VehCfgPrmCCPBytePosn5_0_AsdmPassSafeCANSignalIPdu09:
        sig_name = "VehCfgPrmCCPBytePosn5_0_AsdmPassSafeCANSignalIPdu09"
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

    class VehCfgPrmCCPBytePosn8_0_AsdmPassSafeCANSignalIPdu09:
        sig_name = "VehCfgPrmCCPBytePosn8_0_AsdmPassSafeCANSignalIPdu09"
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


class SrsPassSafeCANFr02:
    msg_name = "SrsPassSafeCANFr02"
    msg_id = 16
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.2
    msg_length = 4
    tx_node = "SRS"
    rx_nodes = []

    class CrashStsSafeCntr_1_SrsPassSafeCANSignalIPdu02:
        sig_name = "CrashStsSafeCntr_1_SrsPassSafeCANSignalIPdu02"
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

    class CrashStsSafeSts_1_SrsPassSafeCANSignalIPdu02:
        sig_name = "CrashStsSafeSts_1_SrsPassSafeCANSignalIPdu02"
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
        sig_value_table = {'CrashSts2_NoCrash': 0, 'CrashSts2_Crash': 1}
        compute_method = None
        length = 1
        startbit = 4
        byte = 0
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class CrashStsSafeChks_1_SrsPassSafeCANSignalIPdu02:
        sig_name = "CrashStsSafeChks_1_SrsPassSafeCANSignalIPdu02"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 255
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class SrsPassSafeCANFr04:
    msg_name = "SrsPassSafeCANFr04"
    msg_id = 18
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "SRS"
    rx_nodes = ['RML']

    class ADataRawSafeCntr_3_AcuFLRCANFDSignalIPdu02:
        sig_name = "ADataRawSafeCntr_3_AcuFLRCANFDSignalIPdu02"
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

    class ADataRawSafeALat1Qf_3_AcuFLRCANFDSignalIPdu02:
        sig_name = "ADataRawSafeALat1Qf_3_AcuFLRCANFDSignalIPdu02"
        sig_start_bit = 11
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
        startbit = 11
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class ADataRawSafeAVert_3_AcuFLRCANFDSignalIPdu02:
        sig_name = "ADataRawSafeAVert_3_AcuFLRCANFDSignalIPdu02"
        sig_start_bit = 55
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 0.0085
        sig_value_offset = 0.0
        sig_value_min = -16352
        sig_value_max = 16353
        sig_byteorder = "Motorola"
        sig_value_init = 1155
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 55
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111110, 0b00000001, 7, 1)]

    class ADataRawSafeALgt_3_AcuFLRCANFDSignalIPdu02:
        sig_name = "ADataRawSafeALgt_3_AcuFLRCANFDSignalIPdu02"
        sig_start_bit = 38
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 0.0085
        sig_value_offset = 0.0
        sig_value_min = -16352
        sig_value_max = 16353
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 38
        bmuws_info = [(4, 0b01111111, 0b10000000, 7, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class ADataRawSafeALat_3_AcuFLRCANFDSignalIPdu02:
        sig_name = "ADataRawSafeALat_3_AcuFLRCANFDSignalIPdu02"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 0.0085
        sig_value_offset = 0.0
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

    class ADataRawSafeChks_3_AcuFLRCANFDSignalIPdu02:
        sig_name = "ADataRawSafeChks_3_AcuFLRCANFDSignalIPdu02"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 255
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ADataRawSafeAVertQf_3_AcuFLRCANFDSignalIPdu02:
        sig_name = "ADataRawSafeAVertQf_3_AcuFLRCANFDSignalIPdu02"
        sig_start_bit = 24
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
        startbit = 24
        bmuws_info = [(3, 0b00000001, 0b11111110, 1, 0), (4, 0b10000000, 0b01111111, 1, 7)]

    class ADataRawSafeALgt1Qf_3_AcuFLRCANFDSignalIPdu02:
        sig_name = "ADataRawSafeALgt1Qf_3_AcuFLRCANFDSignalIPdu02"
        sig_start_bit = 9
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
        startbit = 9
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0


class AsdmPassSafeCANFr02:
    msg_name = "AsdmPassSafeCANFr02"
    msg_id = 131
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.04
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RML']

    class DoorDrvrSts_0_AsdmPassSafeCANSignalIPdu02:
        sig_name = "DoorDrvrSts_0_AsdmPassSafeCANSignalIPdu02"
        sig_start_bit = 1
        update_id_bit = 2
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
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class FctaIndcnRi_1_AsdmPassSafeCANSignalIPdu02:
        sig_name = "FctaIndcnRi_1_AsdmPassSafeCANSignalIPdu02"
        sig_start_bit = 17
        update_id_bit = 18
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LcmaIndcn_NoLcmaWarn': 0, 'LcmaIndcn_LcmaWarnLvl1': 1, 'LcmaIndcn_NotUsed': 2, 'LcmaIndcn_LcmaWarnLvl2': 3}
        compute_method = None
        length = 2
        startbit = 17
        byte = 2
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class FctaIndcnLe_1_AsdmPassSafeCANSignalIPdu02:
        sig_name = "FctaIndcnLe_1_AsdmPassSafeCANSignalIPdu02"
        sig_start_bit = 59
        update_id_bit = 50
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LcmaIndcn_NoLcmaWarn': 0, 'LcmaIndcn_LcmaWarnLvl1': 1, 'LcmaIndcn_NotUsed': 2, 'LcmaIndcn_LcmaWarnLvl2': 3}
        compute_method = None
        length = 2
        startbit = 59
        byte = 7
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class CllsnThreat_1_AsdmPassSafeCANSignalIPdu02:
        sig_name = "CllsnThreat_1_AsdmPassSafeCANSignalIPdu02"
        sig_start_bit = 23
        update_id_bit = 21
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
        startbit = 23
        byte = 2
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class AsdmPassSafeCANFr12:
    msg_name = "AsdmPassSafeCANFr12"
    msg_id = 849
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.45
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RML']

    class RMLCmftFctReq:
        sig_name = "RMLCmftFctReq"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 4
        byte = 0
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class RMRCmftFctReq:
        sig_name = "RMRCmftFctReq"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 2
        byte = 0
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class DoorPassSts_0_AsdmPassSafeCANSignalIPdu12:
        sig_name = "DoorPassSts_0_AsdmPassSafeCANSignalIPdu12"
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
        sig_value_table = {'DoorSts2_Ukwn': 0, 'DoorSts2_Opend': 1, 'DoorSts2_Clsd': 2}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class PassAirbSts_1_AsdmPassSafeCANSignalIPdu12:
        sig_name = "PassAirbSts_1_AsdmPassSafeCANSignalIPdu12"
        sig_start_bit = 15
        update_id_bit = 14
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
        startbit = 15
        byte = 1
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7


class AsdmPassSafeCANFr15:
    msg_name = "AsdmPassSafeCANFr15"
    msg_id = 953
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.08
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RML']

    class VehTiAndDataMins1_0_AsdmPassSafeCANSignalIPdu15:
        sig_name = "VehTiAndDataMins1_0_AsdmPassSafeCANSignalIPdu15"
        sig_start_bit = 13
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
        startbit = 13
        byte = 1
        mask = 0b00111111
        unmask = 0b11000000
        shift = 0

    class VehTiAndDataSec1_0_AsdmPassSafeCANSignalIPdu15:
        sig_name = "VehTiAndDataSec1_0_AsdmPassSafeCANSignalIPdu15"
        sig_start_bit = 5
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
        startbit = 5
        byte = 0
        mask = 0b00111111
        unmask = 0b11000000
        shift = 0

    class VehTiAndDataHr1_0_AsdmPassSafeCANSignalIPdu15:
        sig_name = "VehTiAndDataHr1_0_AsdmPassSafeCANSignalIPdu15"
        sig_start_bit = 20
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
        startbit = 20
        byte = 2
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class VehTiAndDataYr1_0_AsdmPassSafeCANSignalIPdu15:
        sig_name = "VehTiAndDataYr1_0_AsdmPassSafeCANSignalIPdu15"
        sig_start_bit = 46
        update_id_bit = None
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

    class VehTiAndDataDay_0_AsdmPassSafeCANSignalIPdu15:
        sig_name = "VehTiAndDataDay_0_AsdmPassSafeCANSignalIPdu15"
        sig_start_bit = 28
        update_id_bit = None
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

    class VehTiAndDataMth1_0_AsdmPassSafeCANSignalIPdu15:
        sig_name = "VehTiAndDataMth1_0_AsdmPassSafeCANSignalIPdu15"
        sig_start_bit = 35
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
        startbit = 35
        byte = 4
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class VehTiAndDataDataValid_0_AsdmPassSafeCANSignalIPdu15:
        sig_name = "VehTiAndDataDataValid_0_AsdmPassSafeCANSignalIPdu15"
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
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6


class BgmPassSafeCANFr01:
    msg_name = "BgmPassSafeCANFr01"
    msg_id = 533
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['SRS']

    class SteerWhlTouchTurnLightSwtRiChks_2_BgmPassSafeCANSignalIPdu01:
        sig_name = "SteerWhlTouchTurnLightSwtRiChks_2_BgmPassSafeCANSignalIPdu01"
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

    class SteerWhlTouchTurnLightSwtLeCntr_2_BgmPassSafeCANSignalIPdu01:
        sig_name = "SteerWhlTouchTurnLightSwtLeCntr_2_BgmPassSafeCANSignalIPdu01"
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

    class SteerWhlTouchTurnLightSwtLeSteerWhlTouchTurnLightSwtLe_2_BgmPassSafeCANSignalIPdu01:
        sig_name = "SteerWhlTouchTurnLightSwtLeSteerWhlTouchTurnLightSwtLe_2_BgmPassSafeCANSignalIPdu01"
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
        sig_value_table = {'SteerWhlTouchTurnLightSwt_NotAvailable': 0, 'SteerWhlTouchTurnLightSwt_LightPress': 1, 'SteerWhlTouchTurnLightSwt_FullPress': 2, 'SteerWhlTouchTurnLightSwt_Error': 3}
        compute_method = None
        length = 2
        startbit = 15
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class SteerWhlTouchTurnLightSwtRiCntr_2_BgmPassSafeCANSignalIPdu01:
        sig_name = "SteerWhlTouchTurnLightSwtRiCntr_2_BgmPassSafeCANSignalIPdu01"
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

    class SteerWhlTouchTurnLightSwtLeChks_2_BgmPassSafeCANSignalIPdu01:
        sig_name = "SteerWhlTouchTurnLightSwtLeChks_2_BgmPassSafeCANSignalIPdu01"
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

    class SteerWhlTouchTurnLightSwtRiSteerWhlTouchTurnLightSwtLe_2_BgmPassSafeCANSignalIPdu01:
        sig_name = "SteerWhlTouchTurnLightSwtRiSteerWhlTouchTurnLightSwtLe_2_BgmPassSafeCANSignalIPdu01"
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
        sig_value_table = {'SteerWhlTouchTurnLightSwt_NotAvailable': 0, 'SteerWhlTouchTurnLightSwt_LightPress': 1, 'SteerWhlTouchTurnLightSwt_FullPress': 2, 'SteerWhlTouchTurnLightSwt_Error': 3}
        compute_method = None
        length = 2
        startbit = 31
        byte = 3
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class AsdmPassSafeCANFr04:
    msg_name = "AsdmPassSafeCANFr04"
    msg_id = 133
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.025
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RML']

    class RctaIndcnLe_1_AsdmPassSafeCANSignalIPdu04:
        sig_name = "RctaIndcnLe_1_AsdmPassSafeCANSignalIPdu04"
        sig_start_bit = 41
        update_id_bit = 42
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LcmaIndcn_NoLcmaWarn': 0, 'LcmaIndcn_LcmaWarnLvl1': 1, 'LcmaIndcn_NotUsed': 2, 'LcmaIndcn_LcmaWarnLvl2': 3}
        compute_method = None
        length = 2
        startbit = 41
        byte = 5
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class RctaIndcnRi_1_AsdmPassSafeCANSignalIPdu04:
        sig_name = "RctaIndcnRi_1_AsdmPassSafeCANSignalIPdu04"
        sig_start_bit = 55
        update_id_bit = 53
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LcmaIndcn_NoLcmaWarn': 0, 'LcmaIndcn_LcmaWarnLvl1': 1, 'LcmaIndcn_NotUsed': 2, 'LcmaIndcn_LcmaWarnLvl2': 3}
        compute_method = None
        length = 2
        startbit = 55
        byte = 6
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class CllsnWarnReIndcn_1_AsdmPassSafeCANSignalIPdu04:
        sig_name = "CllsnWarnReIndcn_1_AsdmPassSafeCANSignalIPdu04"
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
        sig_value_table = {'LcmaIndcn_NoLcmaWarn': 0, 'LcmaIndcn_LcmaWarnLvl1': 1, 'LcmaIndcn_NotUsed': 2, 'LcmaIndcn_LcmaWarnLvl2': 3}
        compute_method = None
        length = 2
        startbit = 47
        byte = 5
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class CarTiGlb_0_AsdmPassSafeCANSignalIPdu04:
        sig_name = "CarTiGlb_0_AsdmPassSafeCANSignalIPdu04"
        sig_start_bit = 7
        update_id_bit = 43
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


class SrsPassSafeCANFr05:
    msg_name = "SrsPassSafeCANFr05"
    msg_id = 19
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "SRS"
    rx_nodes = ['RML']

    class AsyDataWithCmpSafeALat1Qf:
        sig_name = "AsyDataWithCmpSafeALat1Qf"
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
        sig_value_table = {'Qf1_DevOfDataUndefd': 0, 'Qf1_DataTmpUndefdAndEvlnInProgs': 1, 'Qf1_DevOfDataNotWithinRngAllwd': 2, 'Qf1_DataCalcdWithDevDefd': 3}
        compute_method = None
        length = 2
        startbit = 41
        byte = 5
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class AsyDataWithCmpSafeYawRateQf:
        sig_name = "AsyDataWithCmpSafeYawRateQf"
        sig_start_bit = 33
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
        startbit = 33
        byte = 4
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class AsyDataWithCmpSafeYawRateWithCmp:
        sig_name = "AsyDataWithCmpSafeYawRateWithCmp"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 16
        sig_value_factor = "2.44140625E-4"
        sig_value_offset = 0.0
        sig_value_min = -24576
        sig_value_max = 24576
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class AsyDataWithCmpSafeALgt1Qf:
        sig_name = "AsyDataWithCmpSafeALgt1Qf"
        sig_start_bit = 43
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
        startbit = 43
        byte = 5
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class AsyDataWithCmpSafeGrdtOfALgt:
        sig_name = "AsyDataWithCmpSafeGrdtOfALgt"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 14
        sig_value_factor = 0.00390625
        sig_value_offset = 0.0
        sig_value_min = -7680
        sig_value_max = 7680
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 14
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111100, 0b00000011, 6, 2)]

    class AsyDataWithCmpSafeChks:
        sig_name = "AsyDataWithCmpSafeChks"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 255
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 23
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class AsyDataWithCmpSafeALatWithCmp:
        sig_name = "AsyDataWithCmpSafeALatWithCmp"
        sig_start_bit = 55
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 0.0085
        sig_value_offset = 0.0
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

    class AsyDataWithCmpSafeCntr:
        sig_name = "AsyDataWithCmpSafeCntr"
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


class RmlPassSafeCANFrame2:
    msg_name = "RmlPassSafeCANFrame2"
    msg_id = 847
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "RML"
    rx_nodes = ['CCM']

    class BuymessageCSresultRMLByte7:
        sig_name = "BuymessageCSresultRMLByte7"
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

    class BuymessageCSresultRMLByte2:
        sig_name = "BuymessageCSresultRMLByte2"
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

    class BuymessageCSresultRMLByte5:
        sig_name = "BuymessageCSresultRMLByte5"
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

    class BuymessageCSresultRMLByte4:
        sig_name = "BuymessageCSresultRMLByte4"
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

    class BuymessageCSresultRMLByte6:
        sig_name = "BuymessageCSresultRMLByte6"
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

    class BuymessageCSresultRMLByte0:
        sig_name = "BuymessageCSresultRMLByte0"
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

    class BuymessageCSresultRMLByte3:
        sig_name = "BuymessageCSresultRMLByte3"
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

    class BuymessageCSresultRMLByte1:
        sig_name = "BuymessageCSresultRMLByte1"
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


class RmlPassiveSafetyCANNmFr:
    msg_name = "RmlPassiveSafetyCANNmFr"
    msg_id = 1294
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "RML"
    rx_nodes = ['BGM']


class SrsPassiveSafetyCANNmFr:
    msg_name = "SrsPassiveSafetyCANNmFr"
    msg_id = 1291
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "SRS"
    rx_nodes = ['RML']


class AsdmPassSafeCANFr14:
    msg_name = "AsdmPassSafeCANFr14"
    msg_id = 338
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.025
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RML']

    class VehModMngtGlbSafe1EgyLvlElecMai_0_AsdmPassSafeCANSignalIPdu14:
        sig_name = "VehModMngtGlbSafe1EgyLvlElecMai_0_AsdmPassSafeCANSignalIPdu14"
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

    class VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp_0_AsdmPassSafeCANSignalIPdu14:
        sig_name = "VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp_0_AsdmPassSafeCANSignalIPdu14"
        sig_start_bit = 36
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
        startbit = 36
        byte = 4
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class VehModMngtGlbSafe1CarModSts1_0_AsdmPassSafeCANSignalIPdu14:
        sig_name = "VehModMngtGlbSafe1CarModSts1_0_AsdmPassSafeCANSignalIPdu14"
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

    class VehModMngtGlbSafe1Chks_0_AsdmPassSafeCANSignalIPdu14:
        sig_name = "VehModMngtGlbSafe1Chks_0_AsdmPassSafeCANSignalIPdu14"
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

    class VehModMngtGlbSafe1Cntr_0_AsdmPassSafeCANSignalIPdu14:
        sig_name = "VehModMngtGlbSafe1Cntr_0_AsdmPassSafeCANSignalIPdu14"
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

    class VehModMngtGlbSafe1PwrLvlElecSubtyp_0_AsdmPassSafeCANSignalIPdu14:
        sig_name = "VehModMngtGlbSafe1PwrLvlElecSubtyp_0_AsdmPassSafeCANSignalIPdu14"
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

    class VehModMngtGlbSafe1UsgModSts_0_AsdmPassSafeCANSignalIPdu14:
        sig_name = "VehModMngtGlbSafe1UsgModSts_0_AsdmPassSafeCANSignalIPdu14"
        sig_start_bit = 27
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
        startbit = 27
        byte = 3
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class VehModMngtGlbSafe1EgyLvlElecSubtyp_0_AsdmPassSafeCANSignalIPdu14:
        sig_name = "VehModMngtGlbSafe1EgyLvlElecSubtyp_0_AsdmPassSafeCANSignalIPdu14"
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

    class VehModMngtGlbSafe1PwrLvlElecMai_0_AsdmPassSafeCANSignalIPdu14:
        sig_name = "VehModMngtGlbSafe1PwrLvlElecMai_0_AsdmPassSafeCANSignalIPdu14"
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

    class VehModMngtGlbSafe1FltEgyCnsWdSts_0_AsdmPassSafeCANSignalIPdu14:
        sig_name = "VehModMngtGlbSafe1FltEgyCnsWdSts_0_AsdmPassSafeCANSignalIPdu14"
        sig_start_bit = 33
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
        startbit = 33
        byte = 4
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1


class DmmPassSafeCANFr02:
    msg_name = "DmmPassSafeCANFr02"
    msg_id = 69
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.015
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RML']

    class DrvrPfmncAlrmReq_1_DmmPassSafeCANSignalIPdu02:
        sig_name = "DrvrPfmncAlrmReq_1_DmmPassSafeCANSignalIPdu02"
        sig_start_bit = 63
        update_id_bit = 48
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 6
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DrvrPfmncWarnReq_Unavailable': 0, 'DrvrPfmncWarnReq_Unknown': 1, 'DrvrPfmncWarnReq_NoWarning': 2, 'DrvrPfmncWarnReq_Distractive': 3, 'DrvrPfmncWarnReq_Warninglevel1': 4, 'DrvrPfmncWarnReq_Warninglevel2': 5, 'DrvrPfmncWarnReq_Reserved': 6}
        compute_method = None
        length = 3
        startbit = 63
        byte = 7
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5


class AsdmPassSafeCANFr23:
    msg_name = "AsdmPassSafeCANFr23"
    msg_id = 442
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RML']

    class VehBattUSysU_0_AsdmPassSafeCANSignalIPdu23:
        sig_name = "VehBattUSysU_0_AsdmPassSafeCANSignalIPdu23"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehBattUSysUQf_0_AsdmPassSafeCANSignalIPdu23:
        sig_name = "VehBattUSysUQf_0_AsdmPassSafeCANSignalIPdu23"
        sig_start_bit = 49
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
        startbit = 49
        byte = 6
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0


class AsdmPassSafeCANFr22:
    msg_name = "AsdmPassSafeCANFr22"
    msg_id = 84
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RML']

    class BrkSysCylPMstCntr_1_AsdmPassSafeCANSignalIPdu22:
        sig_name = "BrkSysCylPMstCntr_1_AsdmPassSafeCANSignalIPdu22"
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

    class BrkSysCylPMstVirtQf_1_AsdmPassSafeCANSignalIPdu22:
        sig_name = "BrkSysCylPMstVirtQf_1_AsdmPassSafeCANSignalIPdu22"
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

    class BrkSysCylPMstVirt_1_AsdmPassSafeCANSignalIPdu22:
        sig_name = "BrkSysCylPMstVirt_1_AsdmPassSafeCANSignalIPdu22"
        sig_start_bit = 35
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.25
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 35
        bmuws_info = [(4, 0b00001111, 0b11110000, 4, 0), (5, 0b11111100, 0b00000011, 6, 2)]

    class BrkSysCylPMstAct_1_AsdmPassSafeCANSignalIPdu22:
        sig_name = "BrkSysCylPMstAct_1_AsdmPassSafeCANSignalIPdu22"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.3
        sig_value_offset = "-30.0"
        sig_value_min = 0
        sig_value_max = 1022
        sig_byteorder = "Motorola"
        sig_value_init = 100
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11000000, 0b00111111, 2, 6)]

    class BrkSysCylPMstTar_1_AsdmPassSafeCANSignalIPdu22:
        sig_name = "BrkSysCylPMstTar_1_AsdmPassSafeCANSignalIPdu22"
        sig_start_bit = 29
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.25
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 29
        bmuws_info = [(3, 0b00111111, 0b11000000, 6, 0), (4, 0b11110000, 0b00001111, 4, 4)]

    class BrkSysCylPMstActQf_1_AsdmPassSafeCANSignalIPdu22:
        sig_name = "BrkSysCylPMstActQf_1_AsdmPassSafeCANSignalIPdu22"
        sig_start_bit = 5
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
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class BrkSysCylPMstChks_1_AsdmPassSafeCANSignalIPdu22:
        sig_name = "BrkSysCylPMstChks_1_AsdmPassSafeCANSignalIPdu22"
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


class AsdmPassSafeCANFr39:
    msg_name = "AsdmPassSafeCANFr39"
    msg_id = 863
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CCM"
    rx_nodes = ['RML']

    class BuymessagefunctionBmf:
        sig_name = "BuymessagefunctionBmf"
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
        sig_value_table = {'Bmf_Undefine': 0, 'Bmf_Timestamp1': 1, 'Bmf_BuyMAC1': 2}
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class BuymessagefunctionByte6:
        sig_name = "BuymessagefunctionByte6"
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

    class BuymessagefunctionByte7:
        sig_name = "BuymessagefunctionByte7"
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

    class BuymessagefunctionByte5:
        sig_name = "BuymessagefunctionByte5"
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

    class BuymessagefunctionByte4:
        sig_name = "BuymessagefunctionByte4"
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

    class BuymessagefunctionByte3:
        sig_name = "BuymessagefunctionByte3"
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

    class BuymessagefunctionByte2:
        sig_name = "BuymessagefunctionByte2"
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


class BgmToAllPassSafeDiagReqFrame:
    msg_name = "BgmToAllPassSafeDiagReqFrame"
    msg_id = 2047
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RML']


class SrsPassSafeCANFr06:
    msg_name = "SrsPassSafeCANFr06"
    msg_id = 33
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "SRS"
    rx_nodes = ['RML']

    class ActvnReqOfRtrctrRvsbLe:
        sig_name = "ActvnReqOfRtrctrRvsbLe"
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
        sig_value_table = {'ActvnReqOfRtrctrRvsb1_NoActvn': 0, 'ActvnReqOfRtrctrRvsb1_ActvnFLo': 1, 'ActvnReqOfRtrctrRvsb1_ActvnFHi': 2, 'ActvnReqOfRtrctrRvsb1_Resd1': 3, 'ActvnReqOfRtrctrRvsb1_Resd2': 4}
        compute_method = None
        length = 3
        startbit = 7
        byte = 0
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class ActvnReqOfRtrctrRvsbRi:
        sig_name = "ActvnReqOfRtrctrRvsbRi"
        sig_start_bit = 3
        update_id_bit = 0
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ActvnReqOfRtrctrRvsb1_NoActvn': 0, 'ActvnReqOfRtrctrRvsb1_ActvnFLo': 1, 'ActvnReqOfRtrctrRvsb1_ActvnFHi': 2, 'ActvnReqOfRtrctrRvsb1_Resd1': 3, 'ActvnReqOfRtrctrRvsb1_Resd2': 4}
        compute_method = None
        length = 3
        startbit = 3
        byte = 0
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1


class AsdmPassSafeCANFr08:
    msg_name = "AsdmPassSafeCANFr08"
    msg_id = 747
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RML']

    class VehCfgPrmExtCCPBytePosn3_0_AsdmPassSafeCANSignalIPdu08:
        sig_name = "VehCfgPrmExtCCPBytePosn3_0_AsdmPassSafeCANSignalIPdu08"
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

    class VehCfgPrmExtCCPBytePosn7_0_AsdmPassSafeCANSignalIPdu08:
        sig_name = "VehCfgPrmExtCCPBytePosn7_0_AsdmPassSafeCANSignalIPdu08"
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

    class VehCfgPrmExtCCPBytePosn6_0_AsdmPassSafeCANSignalIPdu08:
        sig_name = "VehCfgPrmExtCCPBytePosn6_0_AsdmPassSafeCANSignalIPdu08"
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

    class VehCfgPrmExtCCPBytePosn2_0_AsdmPassSafeCANSignalIPdu08:
        sig_name = "VehCfgPrmExtCCPBytePosn2_0_AsdmPassSafeCANSignalIPdu08"
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

    class VehCfgPrmExtCCPBytePosn5_0_AsdmPassSafeCANSignalIPdu08:
        sig_name = "VehCfgPrmExtCCPBytePosn5_0_AsdmPassSafeCANSignalIPdu08"
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

    class VehCfgPrmExtCCPBytePosn8_0_AsdmPassSafeCANSignalIPdu08:
        sig_name = "VehCfgPrmExtCCPBytePosn8_0_AsdmPassSafeCANSignalIPdu08"
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

    class VehCfgPrmExtCCPBytePosn4_0_AsdmPassSafeCANSignalIPdu08:
        sig_name = "VehCfgPrmExtCCPBytePosn4_0_AsdmPassSafeCANSignalIPdu08"
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

    class VehCfgPrmExtBlkIDBytePosn1_0_AsdmPassSafeCANSignalIPdu08:
        sig_name = "VehCfgPrmExtBlkIDBytePosn1_0_AsdmPassSafeCANSignalIPdu08"
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


class RmlToBgmPassSafeDiagRespFrame:
    msg_name = "RmlToBgmPassSafeDiagRespFrame"
    msg_id = 1552
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "RML"
    rx_nodes = ['BGM']


class AsdmPassSafeCANFr17:
    msg_name = "AsdmPassSafeCANFr17"
    msg_id = 101
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RML']

    class SteerWhlSnsrChks_1_AsdmPassSafeCANSignalIPdu17:
        sig_name = "SteerWhlSnsrChks_1_AsdmPassSafeCANSignalIPdu17"
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

    class SteerWhlSnsrAgSpd_1_AsdmPassSafeCANSignalIPdu17:
        sig_name = "SteerWhlSnsrAgSpd_1_AsdmPassSafeCANSignalIPdu17"
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

    class SteerWhlSnsrAg_1_AsdmPassSafeCANSignalIPdu17:
        sig_name = "SteerWhlSnsrAg_1_AsdmPassSafeCANSignalIPdu17"
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

    class SteerWhlSnsrQf_1_AsdmPassSafeCANSignalIPdu17:
        sig_name = "SteerWhlSnsrQf_1_AsdmPassSafeCANSignalIPdu17"
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

    class SteerWhlSnsrCntr_1_AsdmPassSafeCANSignalIPdu17:
        sig_name = "SteerWhlSnsrCntr_1_AsdmPassSafeCANSignalIPdu17"
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


class EtcToRmlXcpFr01:
    msg_name = "EtcToRmlXcpFr01"
    msg_id = 1412
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CCM"
    rx_nodes = ['RML']


class AsdmPassSafeCANFr21:
    msg_name = "AsdmPassSafeCANFr21"
    msg_id = 518
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RML']

    class AccrPedlRatChks_1_AsdmPassSafeCANSignalIPdu21:
        sig_name = "AccrPedlRatChks_1_AsdmPassSafeCANSignalIPdu21"
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

    class AccrPedlRatGrdt_1_AsdmPassSafeCANSignalIPdu21:
        sig_name = "AccrPedlRatGrdt_1_AsdmPassSafeCANSignalIPdu21"
        sig_start_bit = 54
        update_id_bit = 55
        sig_length = 15
        sig_value_factor = 0.0625
        sig_value_offset = 0.0
        sig_value_min = -16000
        sig_value_max = 16000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 54
        bmuws_info = [(6, 0b01111111, 0b10000000, 7, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class AccrPedlRatCntr_1_AsdmPassSafeCANSignalIPdu21:
        sig_name = "AccrPedlRatCntr_1_AsdmPassSafeCANSignalIPdu21"
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

    class AccrPedlRatAccrPedlRat_1_AsdmPassSafeCANSignalIPdu21:
        sig_name = "AccrPedlRatAccrPedlRat_1_AsdmPassSafeCANSignalIPdu21"
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


