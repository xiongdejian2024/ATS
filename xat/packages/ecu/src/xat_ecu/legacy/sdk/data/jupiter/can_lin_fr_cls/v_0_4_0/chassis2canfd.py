class CCUMCUCDChassis2CANFDFr01:
    msg_name = "CCUMCUCDChassis2CANFDFr01"
    msg_id = 54
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 48
    tx_node = "CCUMCUCD"
    rx_nodes = ['PSCM2', 'BCU2']
    sig_group_dict = {'BrkSysStPrimRdnt': ['BrkSysStPrimRdntBrkSysSts', 'BrkSysStPrimRdntChks', 'BrkSysStPrimRdntCntr'], 'ADSPinAgReqForBkp': ['ADSPinAgReqForBkpChks', 'ADSPinAgReqForBkpCntr', 'ADSPinAgReqForBkpReq'], 'EpbReqMst': ['EpbReqMstChks', 'EpbReqMstCntr', 'EpbReqMstEpbReq'], 'VMMGlbSig': ['VMMGlbSigCarModSts', 'VMMGlbSigChks', 'VMMGlbSigCntr', 'VMMGlbSigCnvincSubSts1', 'VMMGlbSigDrvgSubSts1', 'VMMGlbSigInactvSubSts1', 'VMMGlbSigLoBattModSts', 'VMMGlbSigUsgModSts'], 'BrkMstCtrlModeReqRdnt': ['BrkMstCtrlModeReqRdntChks', 'BrkMstCtrlModeReqRdntCntr', 'BrkMstCtrlModeReqRdntReq'], 'ADSALgtReqForBkp': ['ADSALgtReqForBkpChks', 'ADSALgtReqForBkpCntr', 'ADSALgtReqForBkpMax', 'ADSALgtReqForBkpMin'], 'EpbCoornPrim': ['EpbCoornPrimApplyFunctionalitiesAvailable', 'EpbCoornPrimChks', 'EpbCoornPrimCntr', 'EpbCoornPrimDiagOperationMode', 'EpbCoornPrimDriveAwayIntention', 'EpbCoornPrimHostAvailabilityFull', 'EpbCoornPrimHostAvailabilityRelOnly', 'EpbCoornPrimPrimarySystemAvailable', 'EpbCoornPrimReserve1', 'EpbCoornPrimReserve2', 'EpbCoornPrimReserve3', 'EpbCoornPrimRollerTestBench'], 'WhlSpdFrnt': ['WhlSpdFrntChks', 'WhlSpdFrntCntr', 'WhlSpdFrntLeQf', 'WhlSpdFrntLeSpd', 'WhlSpdFrntRiQf', 'WhlSpdFrntRiSpd'], 'WhlSpdRe': ['WhlSpdReChks', 'WhlSpdReCntr', 'WhlSpdReLeQf', 'WhlSpdReLeSpd', 'WhlSpdReRiQf', 'WhlSpdReRiSpd']}
    sig_group_dataid_dict = {'VMMGlbSig': 1074, 'WhlSpdFrnt': 1045, 'WhlSpdRe': 1055}

    class ADSPinAgReqForBkpCntr:
        sig_name = "ADSPinAgReqForBkpCntr"
        sig_start_bit = 87
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
        startbit = 87
        byte = 10
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class ADSPinAgReqForBkpChks:
        sig_name = "ADSPinAgReqForBkpChks"
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

    class EpbCoornPrimCntr:
        sig_name = "EpbCoornPrimCntr"
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

    class VMMGlbSigUsgModSts:
        sig_name = "VMMGlbSigUsgModSts"
        sig_start_bit = 163
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
        startbit = 163
        byte = 20
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class ADSALgtReqForBkpMax:
        sig_name = "ADSALgtReqForBkpMax"
        sig_start_bit = 11
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = -15.0
        sig_value_min = 0
        sig_value_max = 3000
        sig_byteorder = "Motorola"
        sig_value_init = 1500
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 11
        bmuws_info = [(1, 0b00001111, 0b11110000, 4, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class BrkSysStPrimRdntCntr:
        sig_name = "BrkSysStPrimRdntCntr"
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

    class BrkSysStPrimRdnt_UB:
        sig_name = "BrkSysStPrimRdnt_UB"
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

    class WhlSpdReRiSpd:
        sig_name = "WhlSpdReRiSpd"
        sig_start_bit = 287
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
        startbit = 287
        bmuws_info = [(35, 0b11111111, 0b00000000, 8, 0), (36, 0b11111110, 0b00000001, 7, 1)]

    class UsgModSts:
        sig_name = "UsgModSts"
        sig_start_bit = 99
        update_id_bit = 111
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
        startbit = 99
        byte = 12
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class BrkMstCtrlModeReqRdntChks:
        sig_name = "BrkMstCtrlModeReqRdntChks"
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

    class ADSPinAgReqForBkp_UB:
        sig_name = "ADSPinAgReqForBkp_UB"
        sig_start_bit = 100
        update_id_bit = 100
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
        startbit = 100
        byte = 12
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class EpbCoornPrimPrimarySystemAvailable:
        sig_name = "EpbCoornPrimPrimarySystemAvailable"
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
        sig_value_table = {'CoornSt_Inactive': 0, 'CoornSt_Active': 1}
        compute_method = None
        length = 1
        startbit = 123
        byte = 15
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class EpbCoornPrimReserve3:
        sig_name = "EpbCoornPrimReserve3"
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
        sig_value_table = {'CoornSt_Inactive': 0, 'CoornSt_Active': 1}
        compute_method = None
        length = 1
        startbit = 120
        byte = 15
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class EpbReqMst_UB:
        sig_name = "EpbReqMst_UB"
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

    class WhlSpdReLeQf:
        sig_name = "WhlSpdReLeQf"
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
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 263
        byte = 32
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class VMMGlbSig_UB:
        sig_name = "VMMGlbSig_UB"
        sig_start_bit = 198
        update_id_bit = 198
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
        startbit = 198
        byte = 24
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VMMGlbSigInactvSubSts1:
        sig_name = "VMMGlbSigInactvSubSts1"
        sig_start_bit = 191
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
        startbit = 191
        byte = 23
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BrkSysStPrimRdntChks:
        sig_name = "BrkSysStPrimRdntChks"
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

    class WhlSpdFrntRiQf:
        sig_name = "WhlSpdFrntRiQf"
        sig_start_bit = 213
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
        startbit = 213
        byte = 26
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class BrkMstCtrlModeReqRdnt_UB:
        sig_name = "BrkMstCtrlModeReqRdnt_UB"
        sig_start_bit = 33
        update_id_bit = 33
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
        startbit = 33
        byte = 4
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class EpbCoornPrimRollerTestBench:
        sig_name = "EpbCoornPrimRollerTestBench"
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
        sig_value_table = {'CoornSt_Inactive': 0, 'CoornSt_Active': 1}
        compute_method = None
        length = 1
        startbit = 135
        byte = 16
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VMMGlbSigCnvincSubSts1:
        sig_name = "VMMGlbSigCnvincSubSts1"
        sig_start_bit = 175
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
        startbit = 175
        byte = 21
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ADSALgtReqForBkp_UB:
        sig_name = "ADSALgtReqForBkp_UB"
        sig_start_bit = 35
        update_id_bit = 35
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
        startbit = 35
        byte = 4
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class EpbCoornPrimApplyFunctionalitiesAvailable:
        sig_name = "EpbCoornPrimApplyFunctionalitiesAvailable"
        sig_start_bit = 108
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
        startbit = 108
        byte = 13
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class WhlSpdReCntr:
        sig_name = "WhlSpdReCntr"
        sig_start_bit = 259
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
        startbit = 259
        byte = 32
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class EpbCoornPrimReserve2:
        sig_name = "EpbCoornPrimReserve2"
        sig_start_bit = 121
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
        startbit = 121
        byte = 15
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class EpbReqMstCntr:
        sig_name = "EpbReqMstCntr"
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

    class BrkSysStPrimRdntBrkSysSts:
        sig_name = "BrkSysStPrimRdntBrkSysSts"
        sig_start_bit = 71
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
        startbit = 71
        byte = 8
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class WhlSpdReLeSpd:
        sig_name = "WhlSpdReLeSpd"
        sig_start_bit = 271
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
        startbit = 271
        bmuws_info = [(33, 0b11111111, 0b00000000, 8, 0), (34, 0b11111110, 0b00000001, 7, 1)]

    class EpbCoornPrim_UB:
        sig_name = "EpbCoornPrim_UB"
        sig_start_bit = 109
        update_id_bit = 109
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
        startbit = 109
        byte = 13
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class WhlSpdReRiQf:
        sig_name = "WhlSpdReRiQf"
        sig_start_bit = 261
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
        startbit = 261
        byte = 32
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class VMMGlbSigCntr:
        sig_name = "VMMGlbSigCntr"
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

    class WhlSpdReChks:
        sig_name = "WhlSpdReChks"
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

    class WhlSpdFrntRiSpd:
        sig_name = "WhlSpdFrntRiSpd"
        sig_start_bit = 239
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
        startbit = 239
        bmuws_info = [(29, 0b11111111, 0b00000000, 8, 0), (30, 0b11111110, 0b00000001, 7, 1)]

    class ADSALgtReqForBkpMin:
        sig_name = "ADSALgtReqForBkpMin"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = -15.0
        sig_value_min = 0
        sig_value_max = 3000
        sig_byteorder = "Motorola"
        sig_value_init = 1500
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11110000, 0b00001111, 4, 4)]

    class ADSPinAgReqForBkpReq:
        sig_name = "ADSPinAgReqForBkpReq"
        sig_start_bit = 83
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
        startbit = 83
        bmuws_info = [(10, 0b00001111, 0b11110000, 4, 0), (11, 0b11111111, 0b00000000, 8, 0), (12, 0b11100000, 0b00011111, 3, 5)]

    class BrkMstCtrlModeReqRdntReq:
        sig_name = "BrkMstCtrlModeReqRdntReq"
        sig_start_bit = 55
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
        startbit = 55
        byte = 6
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class EpbReqMstChks:
        sig_name = "EpbReqMstChks"
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

    class EpbCoornPrimDriveAwayIntention:
        sig_name = "EpbCoornPrimDriveAwayIntention"
        sig_start_bit = 106
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
        startbit = 106
        byte = 13
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VMMGlbSigDrvgSubSts1:
        sig_name = "VMMGlbSigDrvgSubSts1"
        sig_start_bit = 183
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
        startbit = 183
        byte = 22
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class EpbCoornPrimHostAvailabilityFull:
        sig_name = "EpbCoornPrimHostAvailabilityFull"
        sig_start_bit = 105
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
        startbit = 105
        byte = 13
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VMMGlbSigCarModSts:
        sig_name = "VMMGlbSigCarModSts"
        sig_start_bit = 167
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
        startbit = 167
        byte = 20
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class EpbCoornPrimChks:
        sig_name = "EpbCoornPrimChks"
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

    class WhlSpdFrntChks:
        sig_name = "WhlSpdFrntChks"
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

    class WhlSpdFrnt_UB:
        sig_name = "WhlSpdFrnt_UB"
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

    class VMMGlbSigChks:
        sig_name = "VMMGlbSigChks"
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

    class ADSALgtReqForBkpCntr:
        sig_name = "ADSALgtReqForBkpCntr"
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

    class EpbCoornPrimReserve1:
        sig_name = "EpbCoornPrimReserve1"
        sig_start_bit = 122
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
        startbit = 122
        byte = 15
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class WhlSpdFrntLeSpd:
        sig_name = "WhlSpdFrntLeSpd"
        sig_start_bit = 223
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
        startbit = 223
        bmuws_info = [(27, 0b11111111, 0b00000000, 8, 0), (28, 0b11111110, 0b00000001, 7, 1)]

    class EpbCoornPrimDiagOperationMode:
        sig_name = "EpbCoornPrimDiagOperationMode"
        sig_start_bit = 107
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
        startbit = 107
        byte = 13
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class EpbCoornPrimHostAvailabilityRelOnly:
        sig_name = "EpbCoornPrimHostAvailabilityRelOnly"
        sig_start_bit = 104
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
        startbit = 104
        byte = 13
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class BrkMstCtrlModeReqRdntCntr:
        sig_name = "BrkMstCtrlModeReqRdntCntr"
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

    class EpbReqMstEpbReq:
        sig_name = "EpbReqMstEpbReq"
        sig_start_bit = 151
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
        startbit = 151
        byte = 18
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class WhlSpdFrntLeQf:
        sig_name = "WhlSpdFrntLeQf"
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

    class WhlSpdRe_UB:
        sig_name = "WhlSpdRe_UB"
        sig_start_bit = 288
        update_id_bit = 288
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
        startbit = 288
        byte = 36
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ADSALgtReqForBkpChks:
        sig_name = "ADSALgtReqForBkpChks"
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

    class WhlSpdFrntCntr:
        sig_name = "WhlSpdFrntCntr"
        sig_start_bit = 211
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
        startbit = 211
        byte = 26
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class VMMGlbSigLoBattModSts:
        sig_name = "VMMGlbSigLoBattModSts"
        sig_start_bit = 199
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
        startbit = 199
        byte = 24
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7


class PSCM2Chassis2CANFDCanNmFr:
    msg_name = "PSCM2Chassis2CANFDCanNmFr"
    msg_id = 1287
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "PSCM2"
    rx_nodes = ['MGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class BCU2Chassis2CANFDFr02:
    msg_name = "BCU2Chassis2CANFDFr02"
    msg_id = 144
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 48
    tx_node = "BCU2"
    rx_nodes = ['CCUMCUCD', 'PSCM2', 'MGM', 'VCU']
    sig_group_dict = {'BrkLiReqSec': ['BrkLiReqSecBrkLiReq', 'BrkLiReqSecChks', 'BrkLiReqSecCntr'], 'WhlPlsCntrSec': ['WhlPlsCntrSecChks', 'WhlPlsCntrSecCntr', 'WhlPlsCntrSecFL', 'WhlPlsCntrSecFR', 'WhlPlsCntrSecRL', 'WhlPlsCntrSecRR'], 'VehMovgDirSec': ['VehMovgDirSecChks', 'VehMovgDirSecCntr', 'VehMovgDirSecVehMovgDir'], 'EpbLampReqSec': ['EpbLampReqSecChks', 'EpbLampReqSecCntr', 'EpbLampReqSecEpbLampReq'], 'WhlMovgDirReSec': ['WhlMovgDirReSecChks', 'WhlMovgDirReSecCntr', 'WhlMovgDirReSecDirLe', 'WhlMovgDirReSecDirRi'], 'SecBrkEpbReq': ['SecBrkEpbReqAppRel', 'SecBrkEpbReqChks', 'SecBrkEpbReqCntr'], 'WhlMovgDirFrntSec': ['WhlMovgDirFrntSecChks', 'WhlMovgDirFrntSecCntr', 'WhlMovgDirFrntSecDirLe', 'WhlMovgDirFrntSecDirRi'], 'BrkSysStForBkp': ['BrkSysStForBkpBrkAdDegrad', 'BrkSysStForBkpCapibility', 'BrkSysStForBkpChks', 'BrkSysStForBkpCntr', 'BrkSysStForBkpCtrlSts', 'BrkSysStForBkpModCfmd'], 'VehSpdSec': ['VehSpdSecChks', 'VehSpdSecCntr', 'VehSpdSecQf', 'VehSpdSecSpd']}
    sig_group_dataid_dict = {}

    class BrkSysStForBkpCtrlSts:
        sig_name = "BrkSysStForBkpCtrlSts"
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
        sig_value_table = {'CtrlSts_Primary': 0, 'CtrlSts_Secondary': 1}
        compute_method = None
        length = 1
        startbit = 28
        byte = 3
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class BrkLiReqSec_UB:
        sig_name = "BrkLiReqSec_UB"
        sig_start_bit = 10
        update_id_bit = 10
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
        startbit = 10
        byte = 1
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VehSpdSecSpd:
        sig_name = "VehSpdSecSpd"
        sig_start_bit = 119
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
        startbit = 119
        bmuws_info = [(14, 0b11111111, 0b00000000, 8, 0), (15, 0b11111110, 0b00000001, 7, 1)]

    class SecBrkEpbReqCntr:
        sig_name = "SecBrkEpbReqCntr"
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

    class WhlMovgDirFrntSecDirLe:
        sig_name = "WhlMovgDirFrntSecDirLe"
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
        sig_value_table = {'DirLe_Undefined': 0, 'DirLe_Standstill': 1, 'DirLe_Forward': 2, 'DirLe_Backward': 3}
        compute_method = None
        length = 2
        startbit = 143
        byte = 17
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class WhlPlsCntrSec_UB:
        sig_name = "WhlPlsCntrSec_UB"
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

    class VehMovgDirSec_UB:
        sig_name = "VehMovgDirSec_UB"
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

    class WhlPlsCntrSecCntr:
        sig_name = "WhlPlsCntrSecCntr"
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

    class EpbLampReqSecChks:
        sig_name = "EpbLampReqSecChks"
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

    class BrkSysStForBkpCntr:
        sig_name = "BrkSysStForBkpCntr"
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

    class VehSpdSecChks:
        sig_name = "VehSpdSecChks"
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

    class EpbWarnReqSec:
        sig_name = "EpbWarnReqSec"
        sig_start_bit = 58
        update_id_bit = 57
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
        startbit = 58
        byte = 7
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class SecBrkEpbReqChks:
        sig_name = "SecBrkEpbReqChks"
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

    class VehSpdSecCntr:
        sig_name = "VehSpdSecCntr"
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

    class BrkLiReqSecCntr:
        sig_name = "BrkLiReqSecCntr"
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

    class EpbLampReqSec_UB:
        sig_name = "EpbLampReqSec_UB"
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

    class WhlMovgDirReSec_UB:
        sig_name = "WhlMovgDirReSec_UB"
        sig_start_bit = 167
        update_id_bit = 167
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
        startbit = 167
        byte = 20
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class EpbLampReqSecCntr:
        sig_name = "EpbLampReqSecCntr"
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

    class VehMovgDirSecChks:
        sig_name = "VehMovgDirSecChks"
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

    class SecBrkEpbReq_UB:
        sig_name = "SecBrkEpbReq_UB"
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

    class VehMovgDirSecCntr:
        sig_name = "VehMovgDirSecCntr"
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

    class WhlPlsCntrSecFL:
        sig_name = "WhlPlsCntrSecFL"
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

    class VehSpdSecQf:
        sig_name = "VehSpdSecQf"
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
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 111
        byte = 13
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class SecBrkEpbReqAppRel:
        sig_name = "SecBrkEpbReqAppRel"
        sig_start_bit = 79
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
        startbit = 79
        byte = 9
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class WhlMovgDirReSecDirLe:
        sig_name = "WhlMovgDirReSecDirLe"
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
        sig_value_table = {'DirLe_Undefined': 0, 'DirLe_Standstill': 1, 'DirLe_Forward': 2, 'DirLe_Backward': 3}
        compute_method = None
        length = 2
        startbit = 159
        byte = 19
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class WhlMovgDirReSecDirRi:
        sig_name = "WhlMovgDirReSecDirRi"
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
        sig_value_table = {'DirRi_Undefined': 0, 'DirRi_Standstill': 1, 'DirRi_Forward': 2, 'DirRi_Backward': 3}
        compute_method = None
        length = 2
        startbit = 157
        byte = 19
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class BrkSysStForBkpModCfmd:
        sig_name = "BrkSysStForBkpModCfmd"
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

    class WhlMovgDirFrntSec_UB:
        sig_name = "WhlMovgDirFrntSec_UB"
        sig_start_bit = 120
        update_id_bit = 120
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
        startbit = 120
        byte = 15
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class BrkLiReqSecBrkLiReq:
        sig_name = "BrkLiReqSecBrkLiReq"
        sig_start_bit = 11
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
        startbit = 11
        byte = 1
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class BrkLiReqSecChks:
        sig_name = "BrkLiReqSecChks"
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

    class WhlPlsCntrSecFR:
        sig_name = "WhlPlsCntrSecFR"
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

    class WhlMovgDirFrntSecDirRi:
        sig_name = "WhlMovgDirFrntSecDirRi"
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
        sig_value_table = {'DirRi_Undefined': 0, 'DirRi_Standstill': 1, 'DirRi_Forward': 2, 'DirRi_Backward': 3}
        compute_method = None
        length = 2
        startbit = 141
        byte = 17
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class BrkSysStForBkpBrkAdDegrad:
        sig_name = "BrkSysStForBkpBrkAdDegrad"
        sig_start_bit = 39
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
        startbit = 39
        byte = 4
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class WhlMovgDirReSecCntr:
        sig_name = "WhlMovgDirReSecCntr"
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

    class WhlPlsCntrSecRR:
        sig_name = "WhlPlsCntrSecRR"
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

    class BrkSysStForBkpCapibility:
        sig_name = "BrkSysStForBkpCapibility"
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

    class VehMovgDirSecVehMovgDir:
        sig_name = "VehMovgDirSecVehMovgDir"
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
        sig_value_table = {'VehMovgDir_Unknown': 0, 'VehMovgDir_Standstill1': 1, 'VehMovgDir_Standstill2': 2, 'VehMovgDir_Standstill3': 3, 'VehMovgDir_Forward1': 4, 'VehMovgDir_Forward2': 5, 'VehMovgDir_Backward1': 6, 'VehMovgDir_Backward2': 7}
        compute_method = None
        length = 3
        startbit = 95
        byte = 11
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class EpbMsgReqSec:
        sig_name = "EpbMsgReqSec"
        sig_start_bit = 63
        update_id_bit = 59
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
        startbit = 63
        byte = 7
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class WhlPlsCntrSecRL:
        sig_name = "WhlPlsCntrSecRL"
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

    class WhlMovgDirFrntSecCntr:
        sig_name = "WhlMovgDirFrntSecCntr"
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

    class BrkSysStForBkp_UB:
        sig_name = "BrkSysStForBkp_UB"
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

    class VehSpdSec_UB:
        sig_name = "VehSpdSec_UB"
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

    class WhlMovgDirReSecChks:
        sig_name = "WhlMovgDirReSecChks"
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

    class WhlMovgDirFrntSecChks:
        sig_name = "WhlMovgDirFrntSecChks"
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

    class BrkSysStForBkpChks:
        sig_name = "BrkSysStForBkpChks"
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

    class EpbLampReqSecEpbLampReq:
        sig_name = "EpbLampReqSecEpbLampReq"
        sig_start_bit = 55
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
        startbit = 55
        byte = 6
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class WhlPlsCntrSecChks:
        sig_name = "WhlPlsCntrSecChks"
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


class CCUMCUCDChassis2CANFDFr05:
    msg_name = "CCUMCUCDChassis2CANFDFr05"
    msg_id = 625
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 64
    tx_node = "CCUMCUCD"
    rx_nodes = ['PSCM2', 'VCU']
    sig_group_dict = {'LoadPwrActSts': ['LoadPwrActStsACCMPwrActSts', 'LoadPwrActStsAFUPwrActSts', 'LoadPwrActStsAGMPwrActSts', 'LoadPwrActStsAGUPwrActSts', 'LoadPwrActStsALMLPwrActSts', 'LoadPwrActStsALMRPwrActSts', 'LoadPwrActStsAWMPwrActSts', 'LoadPwrActStsBCCPPwrActSts', 'LoadPwrActStsBCFVPwrActSts', 'LoadPwrActStsBCTVPwrActSts', 'LoadPwrActStsBEXVPwrActSts', 'LoadPwrActStsBNCMPwrActSts', 'LoadPwrActStsBoosterBlowerPwrActSts', 'LoadPwrActStsCCTVPwrActSts', 'LoadPwrActStsCDPwrActSts', 'LoadPwrActStsCERVPwrActSts', 'LoadPwrActStsCRCMPwrActSts', 'LoadPwrActStsCSOVPwrActSts', 'LoadPwrActStsDCTVPwrActSts', 'LoadPwrActStsDICPwrActSts', 'LoadPwrActStsDMFLPwrActSts', 'LoadPwrActStsDPODPwrActSts', 'LoadPwrActStsDRFPwrActSts', 'LoadPwrActStsDRMFRPwrActSts', 'LoadPwrActStsDRMRLPwrActSts', 'LoadPwrActStsDRMRRPwrActSts', 'LoadPwrActStsECTVPwrActSts', 'LoadPwrActStsEDCPPwrActSts', 'LoadPwrActStsEGSMPwrActSts', 'LoadPwrActStsEPMPwrActSts', 'LoadPwrActStsFCSIPwrActSts', 'LoadPwrActStsFEXVPwrActSts', 'LoadPwrActStsFLRPwrActSts', 'LoadPwrActStsFSRLPwrActSts', 'LoadPwrActStsFSRRPwrActSts', 'LoadPwrActStsHBMFPwrActSts', 'LoadPwrActStsHBMRPwrActSts', 'LoadPwrActStsHCCPPwrActSts', 'LoadPwrActStsHCMLPwrActSts', 'LoadPwrActStsHCMRPwrActSts', 'LoadPwrActStsHCTVPwrActSts', 'LoadPwrActStsHODPwrActSts', 'LoadPwrActStsHUBFPwrActSts', 'LoadPwrActStsHUBRPwrActSts', 'LoadPwrActStsHVAHPwrActSts', 'LoadPwrActStsHVCHPwrActSts', 'LoadPwrActStsHVCMPwrActSts', 'LoadPwrActStsIEMPwrActSts', 'LoadPwrActStsIRMMPwrActSts', 'LoadPwrActStsLCTVPwrActSts', 'LoadPwrActStsLPODPwrActSts', 'LoadPwrActStsMGMPwrActSts', 'LoadPwrActStsMMDPwrActSts', 'LoadPwrActStsMMPPwrActSts', 'LoadPwrActStsNKRPwrActSts', 'LoadPwrActStsOHCPwrActSts', 'LoadPwrActStsOPCFPwrActSts', 'LoadPwrActStsOPCRPwrActSts', 'LoadPwrActStsPMSIPwrActSts', 'LoadPwrActStsPOFPwrActSts', 'LoadPwrActStsPORPwrActSts', 'LoadPwrActStsPPODPwrActSts', 'LoadPwrActStsRCMLPwrActSts', 'LoadPwrActStsRCMRPwrActSts', 'LoadPwrActStsReserved1', 'LoadPwrActStsReserved10', 'LoadPwrActStsReserved11', 'LoadPwrActStsReserved12', 'LoadPwrActStsReserved13', 'LoadPwrActStsReserved14', 'LoadPwrActStsReserved15', 'LoadPwrActStsReserved16', 'LoadPwrActStsReserved17', 'LoadPwrActStsReserved18', 'LoadPwrActStsReserved2', 'LoadPwrActStsReserved3', 'LoadPwrActStsReserved4', 'LoadPwrActStsReserved5', 'LoadPwrActStsReserved6', 'LoadPwrActStsReserved7', 'LoadPwrActStsReserved8', 'LoadPwrActStsReserved9', 'LoadPwrActStsREXVPwrActSts', 'LoadPwrActStsRLMMPwrActSts', 'LoadPwrActStsRLSMPwrActSts', 'LoadPwrActStsRMLPwrActSts', 'LoadPwrActStsRPODPwrActSts', 'LoadPwrActStsRRMMPwrActSts', 'LoadPwrActStsRSOV1PwrActSts', 'LoadPwrActStsRSOV2PwrActSts', 'LoadPwrActStsSCMFPwrActSts', 'LoadPwrActStsSCMRPwrActSts', 'LoadPwrActStsSODLPwrActSts', 'LoadPwrActStsSODRPwrActSts', 'LoadPwrActStsSRSPwrActSts', 'LoadPwrActStsSWTLPwrActSts', 'LoadPwrActStsSWTRPwrActSts', 'LoadPwrActStsTERVPwrActSts', 'LoadPwrActStsUSBR1PwrActSts', 'LoadPwrActStsUSBR2PwrActSts', 'LoadPwrActStsUWBPwrActSts', 'LoadPwrActStsVCUPwrActSts', 'LoadPwrActStsWERVPwrActSts', 'LoadPwrActStsWPCPwrActSts']}
    sig_group_dataid_dict = {}

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

    class LocalBookChrgnTarVal:
        sig_name = "LocalBookChrgnTarVal"
        sig_start_bit = 255
        update_id_bit = 261
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
        startbit = 255
        bmuws_info = [(31, 0b11111111, 0b00000000, 8, 0), (32, 0b11000000, 0b00111111, 2, 6)]

    class BookDischrgnTarVal:
        sig_name = "BookDischrgnTarVal"
        sig_start_bit = 220
        update_id_bit = 225
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
        startbit = 220
        bmuws_info = [(27, 0b00011111, 0b11100000, 5, 0), (28, 0b11111100, 0b00000011, 6, 2)]

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

    class ThermMngtHVPwrCritDes:
        sig_name = "ThermMngtHVPwrCritDes"
        sig_start_bit = 297
        update_id_bit = 316
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
        startbit = 297
        bmuws_info = [(37, 0b00000011, 0b11111100, 2, 0), (38, 0b11111111, 0b00000000, 8, 0), (39, 0b11100000, 0b00011111, 3, 5)]

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

    class PtInin:
        sig_name = "PtInin"
        sig_start_bit = 260
        update_id_bit = 259
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
        startbit = 260
        byte = 32
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

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

    class BookChrgingSetReq:
        sig_name = "BookChrgingSetReq"
        sig_start_bit = 223
        update_id_bit = 221
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
        startbit = 223
        byte = 27
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class PrpsnEgyRgnLvlSet:
        sig_name = "PrpsnEgyRgnLvlSet"
        sig_start_bit = 279
        update_id_bit = 256
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

    class RemBookChrgnTarVal:
        sig_name = "RemBookChrgnTarVal"
        sig_start_bit = 287
        update_id_bit = 293
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
        startbit = 287
        bmuws_info = [(35, 0b11111111, 0b00000000, 8, 0), (36, 0b11000000, 0b00111111, 2, 6)]

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

    class HVChrgnOrDchaReqSts:
        sig_name = "HVChrgnOrDchaReqSts"
        sig_start_bit = 247
        update_id_bit = 232
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HVChrgnOrDchaReqSts_Default': 0, 'HVChrgnOrDchaReqSts_HMIOn': 1, 'HVChrgnOrDchaReqSts_HMIOff': 2, 'HVChrgnOrDchaReqSts_APPOn': 3, 'HVChrgnOrDchaReqSts_APPOff': 4, 'HVChrgnOrDchaReqSts_BookChrgnOn': 5, 'HVChrgnOrDchaReqSts_BookChrgnOff': 6, 'HVChrgnOrDchaReqSts_DisChrgProtnOn': 7, 'HVChrgnOrDchaReqSts_DisChrgProtnOff': 8, 'HVChrgnOrDchaReqSts_HVIntelligentOn': 9, 'HVChrgnOrDchaReqSts_FotaOn': 10, 'HVChrgnOrDchaReqSts_Reserved1': 11, 'HVChrgnOrDchaReqSts_Reserved2': 12, 'HVChrgnOrDchaReqSts_Reserved3': 13, 'HVChrgnOrDchaReqSts_Reserved4': 14, 'HVChrgnOrDchaReqSts_Reserved': 15}
        compute_method = None
        length = 4
        startbit = 247
        byte = 30
        mask = 0b11110000
        unmask = 0b00001111
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

    class ThermMngtHVPwrNormDes:
        sig_name = "ThermMngtHVPwrNormDes"
        sig_start_bit = 315
        update_id_bit = 334
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
        startbit = 315
        bmuws_info = [(39, 0b00001111, 0b11110000, 4, 0), (40, 0b11111111, 0b00000000, 8, 0), (41, 0b10000000, 0b01111111, 1, 7)]

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

    class HVIntelligentChrgSWSt:
        sig_name = "HVIntelligentChrgSWSt"
        sig_start_bit = 243
        update_id_bit = 241
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
        startbit = 243
        byte = 30
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

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

    class BookStopTimeAchieved:
        sig_name = "BookStopTimeAchieved"
        sig_start_bit = 239
        update_id_bit = 237
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Falsetrue_Init': 0, 'Falsetrue_False': 1, 'Falsetrue_True': 2, 'Falsetrue_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 239
        byte = 29
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

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

    class ThermMngtHVEgyReq:
        sig_name = "ThermMngtHVEgyReq"
        sig_start_bit = 292
        update_id_bit = 298
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
        startbit = 292
        bmuws_info = [(36, 0b00011111, 0b11100000, 5, 0), (37, 0b11111000, 0b00000111, 5, 3)]

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

    class MaxAcInpCurrentSet:
        sig_name = "MaxAcInpCurrentSet"
        sig_start_bit = 271
        update_id_bit = 257
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

    class GearLvrIndcnVirtReq:
        sig_name = "GearLvrIndcnVirtReq"
        sig_start_bit = 236
        update_id_bit = 233
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GearLvrIndcn_Default': 0, 'GearLvrIndcn_P': 1, 'GearLvrIndcn_R': 2, 'GearLvrIndcn_N': 3, 'GearLvrIndcn_D': 4, 'GearLvrIndcn_Reserved1': 5, 'GearLvrIndcn_Reserved2': 6, 'GearLvrIndcn_Undefd': 7}
        compute_method = None
        length = 3
        startbit = 236
        byte = 29
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

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


class CCUMCUCDChassis2CANFDFr06:
    msg_name = "CCUMCUCDChassis2CANFDFr06"
    msg_id = 626
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 64
    tx_node = "CCUMCUCD"
    rx_nodes = ['PSCM2']
    sig_group_dict = {'VehCfgDataGrp': ['VehCfgDataGrpVehCfgData1BlkIDBytePosn1', 'VehCfgDataGrpVehCfgData1BytePosn10', 'VehCfgDataGrpVehCfgData1BytePosn11', 'VehCfgDataGrpVehCfgData1BytePosn12', 'VehCfgDataGrpVehCfgData1BytePosn13', 'VehCfgDataGrpVehCfgData1BytePosn14', 'VehCfgDataGrpVehCfgData1BytePosn15', 'VehCfgDataGrpVehCfgData1BytePosn16', 'VehCfgDataGrpVehCfgData1BytePosn17', 'VehCfgDataGrpVehCfgData1BytePosn18', 'VehCfgDataGrpVehCfgData1BytePosn19', 'VehCfgDataGrpVehCfgData1BytePosn2', 'VehCfgDataGrpVehCfgData1BytePosn20', 'VehCfgDataGrpVehCfgData1BytePosn21', 'VehCfgDataGrpVehCfgData1BytePosn22', 'VehCfgDataGrpVehCfgData1BytePosn23', 'VehCfgDataGrpVehCfgData1BytePosn24', 'VehCfgDataGrpVehCfgData1BytePosn25', 'VehCfgDataGrpVehCfgData1BytePosn26', 'VehCfgDataGrpVehCfgData1BytePosn27', 'VehCfgDataGrpVehCfgData1BytePosn28', 'VehCfgDataGrpVehCfgData1BytePosn29', 'VehCfgDataGrpVehCfgData1BytePosn3', 'VehCfgDataGrpVehCfgData1BytePosn30', 'VehCfgDataGrpVehCfgData1BytePosn31', 'VehCfgDataGrpVehCfgData1BytePosn32', 'VehCfgDataGrpVehCfgData1BytePosn33', 'VehCfgDataGrpVehCfgData1BytePosn34', 'VehCfgDataGrpVehCfgData1BytePosn35', 'VehCfgDataGrpVehCfgData1BytePosn36', 'VehCfgDataGrpVehCfgData1BytePosn37', 'VehCfgDataGrpVehCfgData1BytePosn38', 'VehCfgDataGrpVehCfgData1BytePosn39', 'VehCfgDataGrpVehCfgData1BytePosn4', 'VehCfgDataGrpVehCfgData1BytePosn40', 'VehCfgDataGrpVehCfgData1BytePosn41', 'VehCfgDataGrpVehCfgData1BytePosn42', 'VehCfgDataGrpVehCfgData1BytePosn43', 'VehCfgDataGrpVehCfgData1BytePosn44', 'VehCfgDataGrpVehCfgData1BytePosn45', 'VehCfgDataGrpVehCfgData1BytePosn46', 'VehCfgDataGrpVehCfgData1BytePosn47', 'VehCfgDataGrpVehCfgData1BytePosn48', 'VehCfgDataGrpVehCfgData1BytePosn49', 'VehCfgDataGrpVehCfgData1BytePosn5', 'VehCfgDataGrpVehCfgData1BytePosn50', 'VehCfgDataGrpVehCfgData1BytePosn51', 'VehCfgDataGrpVehCfgData1BytePosn52', 'VehCfgDataGrpVehCfgData1BytePosn53', 'VehCfgDataGrpVehCfgData1BytePosn54', 'VehCfgDataGrpVehCfgData1BytePosn55', 'VehCfgDataGrpVehCfgData1BytePosn56', 'VehCfgDataGrpVehCfgData1BytePosn57', 'VehCfgDataGrpVehCfgData1BytePosn58', 'VehCfgDataGrpVehCfgData1BytePosn59', 'VehCfgDataGrpVehCfgData1BytePosn6', 'VehCfgDataGrpVehCfgData1BytePosn60', 'VehCfgDataGrpVehCfgData1BytePosn61', 'VehCfgDataGrpVehCfgData1BytePosn62', 'VehCfgDataGrpVehCfgData1BytePosn63', 'VehCfgDataGrpVehCfgData1BytePosn64', 'VehCfgDataGrpVehCfgData1BytePosn7', 'VehCfgDataGrpVehCfgData1BytePosn8', 'VehCfgDataGrpVehCfgData1BytePosn9']}
    sig_group_dataid_dict = {}

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


class PSCM2Chassis2CANFDFr01:
    msg_name = "PSCM2Chassis2CANFDFr01"
    msg_id = 55
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 16
    tx_node = "PSCM2"
    rx_nodes = ['CCUMCUCD']
    sig_group_dict = {'SteerInfoRefForBkp': ['SteerInfoRefForBkpChks', 'SteerInfoRefForBkpCntr', 'SteerInfoRefForBkpSteerPinionAgSpdVal', 'SteerInfoRefForBkpSteerPinionAgSpdValQf', 'SteerInfoRefForBkpSteerPinionAgVal', 'SteerInfoRefForBkpSteerPinionAgValQf', 'SteerInfoRefForBkpSteerTorqueValQf', 'SteerInfoRefForBkpSteerWhlTqVal'], 'SteerSysStsForBkp': ['SteerSysStsForBkpCapabilitySts', 'SteerSysStsForBkpChks', 'SteerSysStsForBkpCntr', 'SteerSysStsForBkpCtrlSts', 'SteerSysStsForBkpModCfmd', 'SteerSysStsForBkpQf', 'SteerSysStsForBkpSteerDegraded']}
    sig_group_dataid_dict = {}

    class SteerInfoRefForBkp_UB:
        sig_name = "SteerInfoRefForBkp_UB"
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

    class SteerInfoRefForBkpSteerWhlTqVal:
        sig_name = "SteerInfoRefForBkpSteerWhlTqVal"
        sig_start_bit = 39
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
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111100, 0b00000011, 6, 2)]

    class SteerInfoRefForBkpSteerPinionAgSpdVal:
        sig_name = "SteerInfoRefForBkpSteerPinionAgSpdVal"
        sig_start_bit = 21
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
        startbit = 21
        bmuws_info = [(2, 0b00111111, 0b11000000, 6, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class SteerInfoRefForBkpChks:
        sig_name = "SteerInfoRefForBkpChks"
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

    class SteerInfoRefForBkpSteerPinionAgSpdValQf:
        sig_name = "SteerInfoRefForBkpSteerPinionAgSpdValQf"
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

    class SteerSysStsForBkpQf:
        sig_name = "SteerSysStsForBkpQf"
        sig_start_bit = 83
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
        startbit = 83
        byte = 10
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class SteerSysStsForBkp_UB:
        sig_name = "SteerSysStsForBkp_UB"
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

    class SteerInfoRefForBkpSteerPinionAgValQf:
        sig_name = "SteerInfoRefForBkpSteerPinionAgValQf"
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

    class SteerSysStsForBkpCapabilitySts:
        sig_name = "SteerSysStsForBkpCapabilitySts"
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
        sig_value_table = {'SteerADSLatCtrlFailrSts_Red': 0, 'SteerADSLatCtrlFailrSts_Yellow': 1, 'SteerADSLatCtrlFailrSts_Green': 2, 'SteerADSLatCtrlFailrSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 87
        byte = 10
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class SteerSysStsForBkpCtrlSts:
        sig_name = "SteerSysStsForBkpCtrlSts"
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
        sig_value_table = {'SteerADSLatCtrlRouteSts_Primary': 0, 'SteerADSLatCtrlRouteSts_Secondary': 1}
        compute_method = None
        length = 1
        startbit = 81
        byte = 10
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class SteerSysStsForBkpChks:
        sig_name = "SteerSysStsForBkpChks"
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

    class SteerInfoRefForBkpCntr:
        sig_name = "SteerInfoRefForBkpCntr"
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

    class SteerSysStsForBkpSteerDegraded:
        sig_name = "SteerSysStsForBkpSteerDegraded"
        sig_start_bit = 79
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
        startbit = 79
        byte = 9
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class SteerSysStsForBkpCntr:
        sig_name = "SteerSysStsForBkpCntr"
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

    class SteerSysStsForBkpModCfmd:
        sig_name = "SteerSysStsForBkpModCfmd"
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
        sig_value_table = {'SteerADSLatCtrlModSts_NoADModeActivated': 0, 'SteerADSLatCtrlModSts_Parking': 1, 'SteerADSLatCtrlModSts_ANP': 2, 'SteerADSLatCtrlModSts_Reserved1': 3}
        compute_method = None
        length = 2
        startbit = 85
        byte = 10
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class SteerInfoRefForBkpSteerPinionAgVal:
        sig_name = "SteerInfoRefForBkpSteerPinionAgVal"
        sig_start_bit = 41
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
        startbit = 41
        bmuws_info = [(5, 0b00000011, 0b11111100, 2, 0), (6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111000, 0b00000111, 5, 3)]

    class SteerInfoRefForBkpSteerTorqueValQf:
        sig_name = "SteerInfoRefForBkpSteerTorqueValQf"
        sig_start_bit = 23
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
        startbit = 23
        byte = 2
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class VCUChassis2CANFDFr03:
    msg_name = "VCUChassis2CANFDFr03"
    msg_id = 146
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 16
    tx_node = "VCU"
    rx_nodes = ['CCUMCUCD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class OnBdChrgrS2Sts:
        sig_name = "OnBdChrgrS2Sts"
        sig_start_bit = 31
        update_id_bit = 16
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

    class DCChrgnLockCtrl:
        sig_name = "DCChrgnLockCtrl"
        sig_start_bit = 1
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
        startbit = 1
        byte = 0
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class HMIEPedlInhbnFb:
        sig_name = "HMIEPedlInhbnFb"
        sig_start_bit = 12
        update_id_bit = 10
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
        startbit = 12
        byte = 1
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class VehSpdLimnModSts:
        sig_name = "VehSpdLimnModSts"
        sig_start_bit = 26
        update_id_bit = 24
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OffStbActvOvrd_Off': 0, 'OffStbActvOvrd_Stb': 1, 'OffStbActvOvrd_Actv': 2, 'OffStbActvOvrd_Ovrd': 3}
        compute_method = None
        length = 2
        startbit = 26
        byte = 3
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class PrpsnEgyRgnLvlAct:
        sig_name = "PrpsnEgyRgnLvlAct"
        sig_start_bit = 39
        update_id_bit = 47
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
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DisChrgrFlg:
        sig_name = "DisChrgrFlg"
        sig_start_bit = 15
        update_id_bit = 13
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
        startbit = 15
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class BrkPrioActvorNot:
        sig_name = "BrkPrioActvorNot"
        sig_start_bit = 4
        update_id_bit = 2
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
        startbit = 4
        byte = 0
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class HMIEPedlModSts:
        sig_name = "HMIEPedlModSts"
        sig_start_bit = 9
        update_id_bit = 23
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 1
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CrsCtrlrSts_Off': 1, 'CrsCtrlrSts_Stb': 2, 'CrsCtrlrSts_Actv': 3}
        compute_method = None
        length = 2
        startbit = 9
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class AccrpedlFltSts:
        sig_name = "AccrpedlFltSts"
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
        sig_value_table = {'Flt_Initial': 0, 'Flt_NoFault': 1, 'Flt_Fault': 2}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HVBattPreHeatgFaild:
        sig_name = "HVBattPreHeatgFaild"
        sig_start_bit = 19
        update_id_bit = 17
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
        startbit = 19
        byte = 2
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class HVBattChrgCmpl:
        sig_name = "HVBattChrgCmpl"
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
        sig_value_table = {'NoYesUkwn_No': 0, 'NoYesUkwn_Yes': 1, 'NoYesUkwn_Unknown': 2, 'NoYesUkwn_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 22
        byte = 2
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class VehSpdLimnAllwd:
        sig_name = "VehSpdLimnAllwd"
        sig_start_bit = 29
        update_id_bit = 27
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
        startbit = 29
        byte = 3
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4


class BCU2Chassis2CANFDFr01:
    msg_name = "BCU2Chassis2CANFDFr01"
    msg_id = 53
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 32
    tx_node = "BCU2"
    rx_nodes = ['VCU', 'CCUMCUCD']
    sig_group_dict = {'BrkSysStSecRdnt': ['BrkSysStSecRdntBrkSysSts', 'BrkSysStSecRdntChks', 'BrkSysStSecRdntCntr'], 'EpbCoornSec': ['EpbCoornSecChks', 'EpbCoornSecCntr', 'EpbCoornSecCommunicationAvl', 'EpbCoornSecHostAvailabilityFull', 'EpbCoornSecHostAvailabilityRelOnly', 'EpbCoornSecReserved1', 'EpbCoornSecReserved2', 'EpbCoornSecReserved3', 'EpbCoornSecReserved4', 'EpbCoornSecReserved5', 'EpbCoornSecReserved6', 'EpbCoornSecReserved7'], 'EPBHpsReqSec': ['EPBHpsReqSecChks', 'EPBHpsReqSecCntr', 'EPBHpsReqSecHpsReq'], 'WhlSpdFrntSec': ['WhlSpdFrntSecChks', 'WhlSpdFrntSecCntr', 'WhlSpdFrntSecLeQf', 'WhlSpdFrntSecLeSpd', 'WhlSpdFrntSecRiQf', 'WhlSpdFrntSecRiSpd'], 'WhlSpdReSec': ['WhlSpdReSecChks', 'WhlSpdReSecCntr', 'WhlSpdReSecLeQf', 'WhlSpdReSecLeSpd', 'WhlSpdReSecRiQf', 'WhlSpdReSecRiSpd']}
    sig_group_dataid_dict = {}

    class WhlSpdReSecChks:
        sig_name = "WhlSpdReSecChks"
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

    class WhlSpdFrntSecChks:
        sig_name = "WhlSpdFrntSecChks"
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

    class EPBHpsReqSecCntr:
        sig_name = "EPBHpsReqSecCntr"
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

    class WhlSpdFrntSecLeSpd:
        sig_name = "WhlSpdFrntSecLeSpd"
        sig_start_bit = 95
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
        startbit = 95
        bmuws_info = [(11, 0b11111111, 0b00000000, 8, 0), (12, 0b11111110, 0b00000001, 7, 1)]

    class EPBHpsTarPSec:
        sig_name = "EPBHpsTarPSec"
        sig_start_bit = 63
        update_id_bit = 71
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class EpbCoornSecCommunicationAvl:
        sig_name = "EpbCoornSecCommunicationAvl"
        sig_start_bit = 39
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
        startbit = 39
        byte = 4
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class WhlSpdReSecCntr:
        sig_name = "WhlSpdReSecCntr"
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

    class EpbCoornSecReserved4:
        sig_name = "EpbCoornSecReserved4"
        sig_start_bit = 19
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
        startbit = 19
        byte = 2
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class EpbCoornSecReserved1:
        sig_name = "EpbCoornSecReserved1"
        sig_start_bit = 22
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
        startbit = 22
        byte = 2
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class EpbCoornSecReserved5:
        sig_name = "EpbCoornSecReserved5"
        sig_start_bit = 18
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
        startbit = 18
        byte = 2
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class EpbCoornSecChks:
        sig_name = "EpbCoornSecChks"
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

    class WhlSpdFrntSecRiQf:
        sig_name = "WhlSpdFrntSecRiQf"
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

    class BrkSysStSecRdnt_UB:
        sig_name = "BrkSysStSecRdnt_UB"
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

    class EpbCoornSecReserved6:
        sig_name = "EpbCoornSecReserved6"
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
        sig_value_table = {'CoornSt_Inactive': 0, 'CoornSt_Active': 1}
        compute_method = None
        length = 1
        startbit = 17
        byte = 2
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class EpbCoornSec_UB:
        sig_name = "EpbCoornSec_UB"
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

    class EpbCoornSecHostAvailabilityFull:
        sig_name = "EpbCoornSecHostAvailabilityFull"
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
        sig_value_table = {'CoornSt_Inactive': 0, 'CoornSt_Active': 1}
        compute_method = None
        length = 1
        startbit = 38
        byte = 4
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class BrkSysStSecRdntBrkSysSts:
        sig_name = "BrkSysStSecRdntBrkSysSts"
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

    class EpbCoornSecReserved3:
        sig_name = "EpbCoornSecReserved3"
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
        sig_value_table = {'CoornSt_Inactive': 0, 'CoornSt_Active': 1}
        compute_method = None
        length = 1
        startbit = 20
        byte = 2
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class EPBHpsReqSec_UB:
        sig_name = "EPBHpsReqSec_UB"
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

    class WhlSpdReSecLeQf:
        sig_name = "WhlSpdReSecLeQf"
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
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 135
        byte = 16
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class WhlSpdReSecLeSpd:
        sig_name = "WhlSpdReSecLeSpd"
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

    class EpbCoornSecReserved2:
        sig_name = "EpbCoornSecReserved2"
        sig_start_bit = 21
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
        startbit = 21
        byte = 2
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class EpbCoornSecCntr:
        sig_name = "EpbCoornSecCntr"
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

    class BrkSysStSecRdntChks:
        sig_name = "BrkSysStSecRdntChks"
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

    class WhlSpdFrntSecCntr:
        sig_name = "WhlSpdFrntSecCntr"
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

    class WhlSpdReSecRiSpd:
        sig_name = "WhlSpdReSecRiSpd"
        sig_start_bit = 159
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
        startbit = 159
        bmuws_info = [(19, 0b11111111, 0b00000000, 8, 0), (20, 0b11111110, 0b00000001, 7, 1)]

    class BrkSysStSecRdntCntr:
        sig_name = "BrkSysStSecRdntCntr"
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

    class EpbCoornSecHostAvailabilityRelOnly:
        sig_name = "EpbCoornSecHostAvailabilityRelOnly"
        sig_start_bit = 37
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
        startbit = 37
        byte = 4
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class EpbCoornSecReserved7:
        sig_name = "EpbCoornSecReserved7"
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
        sig_value_table = {'CoornSt_Inactive': 0, 'CoornSt_Active': 1}
        compute_method = None
        length = 1
        startbit = 16
        byte = 2
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class WhlSpdFrntSec_UB:
        sig_name = "WhlSpdFrntSec_UB"
        sig_start_bit = 112
        update_id_bit = 112
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
        startbit = 112
        byte = 14
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class WhlSpdFrntSecLeQf:
        sig_name = "WhlSpdFrntSecLeQf"
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

    class WhlSpdReSec_UB:
        sig_name = "WhlSpdReSec_UB"
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

    class WhlSpdFrntSecRiSpd:
        sig_name = "WhlSpdFrntSecRiSpd"
        sig_start_bit = 111
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
        startbit = 111
        bmuws_info = [(13, 0b11111111, 0b00000000, 8, 0), (14, 0b11111110, 0b00000001, 7, 1)]

    class EPBHpsReqSecChks:
        sig_name = "EPBHpsReqSecChks"
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

    class EPBHpsReqSecHpsReq:
        sig_name = "EPBHpsReqSecHpsReq"
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
        sig_value_table = {'HpsReq_NoReq': 0, 'HpsReq_Normal': 1, 'HpsReq_Max': 2, 'HpsReq_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 55
        byte = 6
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class WhlSpdReSecRiQf:
        sig_name = "WhlSpdReSecRiQf"
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


class VCUChassis2CANFDFr06:
    msg_name = "VCUChassis2CANFDFr06"
    msg_id = 418
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 32
    tx_node = "VCU"
    rx_nodes = ['CCUMCUCD']
    sig_group_dict = {'VehAxleTqDistbnAct': ['VehAxleTqDistbnActManualAuto', 'VehAxleTqDistbnActPerc']}
    sig_group_dataid_dict = {}

    class TyreSlipRatReLe:
        sig_name = "TyreSlipRatReLe"
        sig_start_bit = 115
        update_id_bit = 124
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 115
        bmuws_info = [(14, 0b00001111, 0b11110000, 4, 0), (15, 0b11100000, 0b00011111, 3, 5)]

    class MaxACInpISetFdb:
        sig_name = "MaxACInpISetFdb"
        sig_start_bit = 15
        update_id_bit = 63
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

    class VehAxleTqDistbnActManualAuto:
        sig_name = "VehAxleTqDistbnActManualAuto"
        sig_start_bit = 151
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VehAxleTqDistbnMod_Initial': 0, 'VehAxleTqDistbnMod_Auto': 1, 'VehAxleTqDistbnMod_Manual': 2, 'VehAxleTqDistbnMod_Unknow': 3, 'VehAxleTqDistbnMod_Reserved': 4}
        compute_method = None
        length = 4
        startbit = 151
        byte = 18
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class OnBdChrgrIAct:
        sig_name = "OnBdChrgrIAct"
        sig_start_bit = 39
        update_id_bit = 61
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = -200.0
        sig_value_min = 0
        sig_value_max = 4000
        sig_byteorder = "Motorola"
        sig_value_init = 2000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11110000, 0b00001111, 4, 4)]

    class PwrEgyMgrAvl:
        sig_name = "PwrEgyMgrAvl"
        sig_start_bit = 81
        update_id_bit = 100
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
        startbit = 81
        bmuws_info = [(10, 0b00000011, 0b11111100, 2, 0), (11, 0b11111111, 0b00000000, 8, 0), (12, 0b11100000, 0b00011111, 3, 5)]

    class TyreSlipRatFrntLe:
        sig_name = "TyreSlipRatFrntLe"
        sig_start_bit = 99
        update_id_bit = 108
        sig_length = 7
        sig_value_factor = 1
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

    class PwrDegradedSts:
        sig_name = "PwrDegradedSts"
        sig_start_bit = 4
        update_id_bit = 0
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PwrDegraded_Default': 0, 'PwrDegraded_OBCOverT': 1, 'PwrDegraded_ChrgrOverT': 2, 'PwrDegraded_HndlLockgFlt': 3, 'PwrDegraded_IntElecFlt': 4, 'PwrDegraded_OBCCoolingOverT': 5, 'PwrDegraded_OBCLowT': 6, 'PwrDegraded_Reserved8': 7}
        compute_method = None
        length = 4
        startbit = 4
        byte = 0
        mask = 0b00011110
        unmask = 0b11100001
        shift = 1

    class OnBdChrgrCCResis:
        sig_name = "OnBdChrgrCCResis"
        sig_start_bit = 23
        update_id_bit = 62
        sig_length = 16
        sig_value_factor = 1
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

    class VehAxleTqDistbnActPerc:
        sig_name = "VehAxleTqDistbnActPerc"
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

    class HVChrgnAllwd:
        sig_name = "HVChrgnAllwd"
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
        sig_value_table = {'ChrgnAllwd_Init': 0, 'ChrgnAllwd_NOK': 1, 'ChrgnAllwd_OK': 2, 'ChrgnAllwd_HOLD': 3}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class TyreSlipRatReRi:
        sig_name = "TyreSlipRatReRi"
        sig_start_bit = 123
        update_id_bit = 132
        sig_length = 7
        sig_value_factor = 1
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

    class OnBdChrgrUDc:
        sig_name = "OnBdChrgrUDc"
        sig_start_bit = 79
        update_id_bit = 82
        sig_length = 13
        sig_value_factor = 0.2
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 6000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 79
        bmuws_info = [(9, 0b11111111, 0b00000000, 8, 0), (10, 0b11111000, 0b00000111, 5, 3)]

    class VehAxleTqDistbnAct_UB:
        sig_name = "VehAxleTqDistbnAct_UB"
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

    class V2XDchaSwtFdb:
        sig_name = "V2XDchaSwtFdb"
        sig_start_bit = 131
        update_id_bit = 128
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
        startbit = 131
        byte = 16
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class OnBdChrgrIDc:
        sig_name = "OnBdChrgrIDc"
        sig_start_bit = 43
        update_id_bit = 60
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = -200.0
        sig_value_min = 0
        sig_value_max = 4000
        sig_byteorder = "Motorola"
        sig_value_init = 2000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 43
        bmuws_info = [(5, 0b00001111, 0b11110000, 4, 0), (6, 0b11111111, 0b00000000, 8, 0)]

    class OnBdChrgrUAct:
        sig_name = "OnBdChrgrUAct"
        sig_start_bit = 59
        update_id_bit = 64
        sig_length = 11
        sig_value_factor = 0.25
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2044
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 59
        bmuws_info = [(7, 0b00001111, 0b11110000, 4, 0), (8, 0b11111110, 0b00000001, 7, 1)]

    class VehAxleTqDistbnModAct:
        sig_name = "VehAxleTqDistbnModAct"
        sig_start_bit = 145
        update_id_bit = 146
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VehAxleTqDistbnMod_Initial': 0, 'VehAxleTqDistbnMod_Auto': 1, 'VehAxleTqDistbnMod_Manual': 2, 'VehAxleTqDistbnMod_Unknow': 3, 'VehAxleTqDistbnMod_Reserved': 4}
        compute_method = None
        length = 4
        startbit = 145
        bmuws_info = [(18, 0b00000011, 0b11111100, 2, 0), (19, 0b11000000, 0b00111111, 2, 6)]

    class TyreSlipRatFrntRe:
        sig_name = "TyreSlipRatFrntRe"
        sig_start_bit = 107
        update_id_bit = 116
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 107
        bmuws_info = [(13, 0b00001111, 0b11110000, 4, 0), (14, 0b11100000, 0b00011111, 3, 5)]


class BCU2ToCCUMCUCDChassis2CANFDDiagRespFrame:
    msg_name = "BCU2ToCCUMCUCDChassis2CANFDDiagRespFrame"
    msg_id = 1539
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "BCU2"
    rx_nodes = ['CCUMCUCD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class BCU2Chassis2CANFDFr03:
    msg_name = "BCU2Chassis2CANFDFr03"
    msg_id = 624
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "BCU2"
    rx_nodes = ['CCUMCUCD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class IRawBCU2:
        sig_name = "IRawBCU2"
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

    class URawBCU2:
        sig_name = "URawBCU2"
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


class CCUMCUCDChassis2CANFDCanNmFr:
    msg_name = "CCUMCUCDChassis2CANFDCanNmFr"
    msg_id = 1281
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CCUMCUCD"
    rx_nodes = ['BCU2']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class CCUMCUCDChassis2CANFDFr02:
    msg_name = "CCUMCUCDChassis2CANFDFr02"
    msg_id = 145
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 48
    tx_node = "CCUMCUCD"
    rx_nodes = ['PSCM2', 'BCU2', 'VCU']
    sig_group_dict = {'VehSpd': ['VehSpdChks', 'VehSpdCntr', 'VehSpdQf', 'VehSpdSpd'], 'WhlPlsCntr': ['WhlPlsCntrChks', 'WhlPlsCntrCntr', 'WhlPlsCntrFL', 'WhlPlsCntrFR', 'WhlPlsCntrRL', 'WhlPlsCntrRR'], 'ADSCtrlStsBrkForBkp': ['ADSCtrlStsBrkForBkpAdMode', 'ADSCtrlStsBrkForBkpChks', 'ADSCtrlStsBrkForBkpCntr', 'ADSCtrlStsBrkForBkpCtrlSts', 'ADSCtrlStsBrkForBkpQf', 'ADSCtrlStsBrkForBkpSts'], 'VehMovgDir': ['VehMovgDirChks', 'VehMovgDirCntr', 'VehMovgDirVehMovgDir'], 'WhlMovgDirFrnt': ['WhlMovgDirFrntChks', 'WhlMovgDirFrntCntr', 'WhlMovgDirFrntDirLe', 'WhlMovgDirFrntDirRi'], 'IMUAgCmpData': ['IMUAgCmpDataChks', 'IMUAgCmpDataCntr', 'IMUAgCmpDataPitch', 'IMUAgCmpDataPitchQf', 'IMUAgCmpDataRoll', 'IMUAgCmpDataRollQf', 'IMUAgCmpDataYaw', 'IMUAgCmpDataYawQf'], 'ADSCtrlStsLatForBkp': ['ADSCtrlStsLatForBkpAdMode', 'ADSCtrlStsLatForBkpChks', 'ADSCtrlStsLatForBkpCntr', 'ADSCtrlStsLatForBkpCtrlSts', 'ADSCtrlStsLatForBkpQf', 'ADSCtrlStsLatForBkpSts'], 'HVActvReqFromSrv': ['HVActvReqFromSrvCmd', 'HVActvReqFromSrvSource'], 'ADSCtrlStsPropForBkp': ['ADSCtrlStsPropForBkpAdMode', 'ADSCtrlStsPropForBkpChks', 'ADSCtrlStsPropForBkpCntr', 'ADSCtrlStsPropForBkpCtrlSts', 'ADSCtrlStsPropForBkpQf', 'ADSCtrlStsPropForBkpSts'], 'WhlMovgDirRe': ['WhlMovgDirReChks', 'WhlMovgDirReCntr', 'WhlMovgDirReDirLe', 'WhlMovgDirReDirRi']}
    sig_group_dataid_dict = {'VehSpd': 1043}

    class ADSCtrlStsBrkForBkpCtrlSts:
        sig_name = "ADSCtrlStsBrkForBkpCtrlSts"
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
        sig_value_table = {'ADMasterTakeOverRequest_NoRequest': 0, 'ADMasterTakeOverRequest_Master': 1, 'ADMasterTakeOverRequest_SlaveTakeOver': 2, 'ADMasterTakeOverRequest_SlaveBrakeStop': 3}
        compute_method = None
        length = 2
        startbit = 23
        byte = 2
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class WhlMovgDirFrntDirRi:
        sig_name = "WhlMovgDirFrntDirRi"
        sig_start_bit = 221
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
        startbit = 221
        byte = 27
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class WhlPlsCntrRL:
        sig_name = "WhlPlsCntrRL"
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

    class VehSpd_UB:
        sig_name = "VehSpd_UB"
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

    class FLDoorOpenClsSts:
        sig_name = "FLDoorOpenClsSts"
        sig_start_bit = 85
        update_id_bit = 83
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
        startbit = 85
        byte = 10
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class ADSCtrlStsBrkForBkpCntr:
        sig_name = "ADSCtrlStsBrkForBkpCntr"
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

    class VehMovgDirCntr:
        sig_name = "VehMovgDirCntr"
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

    class VehMovgDirVehMovgDir:
        sig_name = "VehMovgDirVehMovgDir"
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
        sig_value_table = {'VehMovgDir_Unknown': 0, 'VehMovgDir_Standstill1': 1, 'VehMovgDir_Standstill2': 2, 'VehMovgDir_Standstill3': 3, 'VehMovgDir_Forward1': 4, 'VehMovgDir_Forward2': 5, 'VehMovgDir_Backward1': 6, 'VehMovgDir_Backward2': 7}
        compute_method = None
        length = 3
        startbit = 175
        byte = 21
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class ADSCtrlStsLatForBkpCtrlSts:
        sig_name = "ADSCtrlStsLatForBkpCtrlSts"
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
        sig_value_table = {'ADMasterTakeOverRequest_NoRequest': 0, 'ADMasterTakeOverRequest_Master': 1, 'ADMasterTakeOverRequest_SlaveTakeOver': 2, 'ADMasterTakeOverRequest_SlaveBrakeStop': 3}
        compute_method = None
        length = 2
        startbit = 47
        byte = 5
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class ADSDeactivePropReqForBkp:
        sig_name = "ADSDeactivePropReqForBkp"
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
        sig_value_table = {'ReqSts1_NotReqd': 0, 'ReqSts1_Reqd': 1}
        compute_method = None
        length = 1
        startbit = 75
        byte = 9
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class ADSCtrlStsBrkForBkpChks:
        sig_name = "ADSCtrlStsBrkForBkpChks"
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

    class WhlMovgDirFrntChks:
        sig_name = "WhlMovgDirFrntChks"
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

    class WhlMovgDirFrntDirLe:
        sig_name = "WhlMovgDirFrntDirLe"
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
        sig_value_table = {'DirLe_Undefined': 0, 'DirLe_Standstill': 1, 'DirLe_Forward': 2, 'DirLe_Backward': 3}
        compute_method = None
        length = 2
        startbit = 223
        byte = 27
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class ADSDeactiveLatReqForBkp:
        sig_name = "ADSDeactiveLatReqForBkp"
        sig_start_bit = 77
        update_id_bit = 76
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
        startbit = 77
        byte = 9
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class WhlPlsCntr_UB:
        sig_name = "WhlPlsCntr_UB"
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

    class ADSCtrlStsBrkForBkpAdMode:
        sig_name = "ADSCtrlStsBrkForBkpAdMode"
        sig_start_bit = 11
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
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class WhlMovgDirReDirLe:
        sig_name = "WhlMovgDirReDirLe"
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
        sig_value_table = {'DirLe_Undefined': 0, 'DirLe_Standstill': 1, 'DirLe_Forward': 2, 'DirLe_Backward': 3}
        compute_method = None
        length = 2
        startbit = 239
        byte = 29
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class ADSCtrlStsBrkForBkp_UB:
        sig_name = "ADSCtrlStsBrkForBkp_UB"
        sig_start_bit = 17
        update_id_bit = 17
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
        startbit = 17
        byte = 2
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VehMovgDir_UB:
        sig_name = "VehMovgDir_UB"
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

    class ADSCtrlStsPropForBkpCntr:
        sig_name = "ADSCtrlStsPropForBkpCntr"
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

    class WhlMovgDirFrnt_UB:
        sig_name = "WhlMovgDirFrnt_UB"
        sig_start_bit = 200
        update_id_bit = 200
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
        startbit = 200
        byte = 25
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ADSCtrlStsPropForBkpChks:
        sig_name = "ADSCtrlStsPropForBkpChks"
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

    class WhlMovgDirReChks:
        sig_name = "WhlMovgDirReChks"
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

    class WhlPlsCntrFR:
        sig_name = "WhlPlsCntrFR"
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

    class VehMovgDirChks:
        sig_name = "VehMovgDirChks"
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

    class EpbRollerActv:
        sig_name = "EpbRollerActv"
        sig_start_bit = 87
        update_id_bit = 86
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
        startbit = 87
        byte = 10
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ADSCtrlStsPropForBkpSts:
        sig_name = "ADSCtrlStsPropForBkpSts"
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
        sig_value_table = {'ColorSts_Red': 0, 'ColorSts_Yellow': 1, 'ColorSts_Green': 2, 'ColorSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 67
        byte = 8
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class ADSCtrlStsLatForBkpQf:
        sig_name = "ADSCtrlStsLatForBkpQf"
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

    class WhlPlsCntrCntr:
        sig_name = "WhlPlsCntrCntr"
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

    class WhlPlsCntrChks:
        sig_name = "WhlPlsCntrChks"
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

    class ADSCtrlStsBrkForBkpQf:
        sig_name = "ADSCtrlStsBrkForBkpQf"
        sig_start_bit = 21
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
        startbit = 21
        byte = 2
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class ADSCtrlStsLatForBkpAdMode:
        sig_name = "ADSCtrlStsLatForBkpAdMode"
        sig_start_bit = 39
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
        startbit = 39
        byte = 4
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

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

    class ADSCtrlStsPropForBkpCtrlSts:
        sig_name = "ADSCtrlStsPropForBkpCtrlSts"
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
        sig_value_table = {'ADMasterTakeOverRequest_NoRequest': 0, 'ADMasterTakeOverRequest_Master': 1, 'ADMasterTakeOverRequest_SlaveTakeOver': 2, 'ADMasterTakeOverRequest_SlaveBrakeStop': 3}
        compute_method = None
        length = 2
        startbit = 71
        byte = 8
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HVActvReqFromSrvSource:
        sig_name = "HVActvReqFromSrvSource"
        sig_start_bit = 293
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 7
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HVOnSource1_Rem': 0, 'HVOnSource1_LV': 1, 'HVOnSource1_Therm': 2, 'HVOnSource1_Diag': 3, 'HVOnSource1_Reserved1': 4, 'HVOnSource1_Reserved2': 5, 'HVOnSource1_HVReld': 6, 'HVOnSource1_Default': 7}
        compute_method = None
        length = 3
        startbit = 293
        byte = 36
        mask = 0b00111000
        unmask = 0b11000111
        shift = 3

    class ADSCtrlStsPropForBkpAdMode:
        sig_name = "ADSCtrlStsPropForBkpAdMode"
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

    class WhlMovgDirFrntCntr:
        sig_name = "WhlMovgDirFrntCntr"
        sig_start_bit = 219
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
        startbit = 219
        byte = 27
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

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

    class ADSCtrlStsLatForBkp_UB:
        sig_name = "ADSCtrlStsLatForBkp_UB"
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

    class VehSpdChks:
        sig_name = "VehSpdChks"
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

    class HVActvReqFromSrv_UB:
        sig_name = "HVActvReqFromSrv_UB"
        sig_start_bit = 290
        update_id_bit = 290
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
        startbit = 290
        byte = 36
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class HVActvReqFromSrvCmd:
        sig_name = "HVActvReqFromSrvCmd"
        sig_start_bit = 295
        update_id_bit = None
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
        startbit = 295
        byte = 36
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class ADSCtrlStsLatForBkpChks:
        sig_name = "ADSCtrlStsLatForBkpChks"
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

    class ADSCtrlStsBrkForBkpSts:
        sig_name = "ADSCtrlStsBrkForBkpSts"
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
        sig_value_table = {'ColorSts_Red': 0, 'ColorSts_Yellow': 1, 'ColorSts_Green': 2, 'ColorSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 19
        byte = 2
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class ADSCtrlStsPropForBkp_UB:
        sig_name = "ADSCtrlStsPropForBkp_UB"
        sig_start_bit = 65
        update_id_bit = 65
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
        startbit = 65
        byte = 8
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

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

    class WhlMovgDirRe_UB:
        sig_name = "WhlMovgDirRe_UB"
        sig_start_bit = 247
        update_id_bit = 247
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
        startbit = 247
        byte = 30
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VehSpdQf:
        sig_name = "VehSpdQf"
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
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 191
        byte = 23
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class VehSpdSpd:
        sig_name = "VehSpdSpd"
        sig_start_bit = 199
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
        startbit = 199
        bmuws_info = [(24, 0b11111111, 0b00000000, 8, 0), (25, 0b11111110, 0b00000001, 7, 1)]

    class WhlPlsCntrRR:
        sig_name = "WhlPlsCntrRR"
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

    class WhlMovgDirReDirRi:
        sig_name = "WhlMovgDirReDirRi"
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
        sig_value_table = {'DirRi_Undefined': 0, 'DirRi_Standstill': 1, 'DirRi_Forward': 2, 'DirRi_Backward': 3}
        compute_method = None
        length = 2
        startbit = 237
        byte = 29
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class ADSCtrlStsLatForBkpSts:
        sig_name = "ADSCtrlStsLatForBkpSts"
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
        sig_value_table = {'ColorSts_Red': 0, 'ColorSts_Yellow': 1, 'ColorSts_Green': 2, 'ColorSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 43
        byte = 5
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class ADSDeactiveBrkReqForBkp:
        sig_name = "ADSDeactiveBrkReqForBkp"
        sig_start_bit = 79
        update_id_bit = 78
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
        startbit = 79
        byte = 9
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class WhlPlsCntrFL:
        sig_name = "WhlPlsCntrFL"
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

    class ADSSlavePscmTemporaryoffForBkp:
        sig_name = "ADSSlavePscmTemporaryoffForBkp"
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
        sig_value_table = {'ReqSts1_NotReqd': 0, 'ReqSts1_Reqd': 1}
        compute_method = None
        length = 1
        startbit = 73
        byte = 9
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VehSpdCntr:
        sig_name = "VehSpdCntr"
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

    class ADSCtrlStsLatForBkpCntr:
        sig_name = "ADSCtrlStsLatForBkpCntr"
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

    class WhlMovgDirReCntr:
        sig_name = "WhlMovgDirReCntr"
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

    class ADSCtrlStsPropForBkpQf:
        sig_name = "ADSCtrlStsPropForBkpQf"
        sig_start_bit = 69
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
        startbit = 69
        byte = 8
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4


class CCUMCUCDToBCU2Chassis2CANFDDiagReqFrame:
    msg_name = "CCUMCUCDToBCU2Chassis2CANFDDiagReqFrame"
    msg_id = 1795
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "CCUMCUCD"
    rx_nodes = ['BCU2']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class CCUMCUCDToPSCM2Chassis2CANFDDiagReqFrame:
    msg_name = "CCUMCUCDToPSCM2Chassis2CANFDDiagReqFrame"
    msg_id = 1824
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "CCUMCUCD"
    rx_nodes = ['PSCM2']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class PSCM2Chassis2CANFDFr02:
    msg_name = "PSCM2Chassis2CANFDFr02"
    msg_id = 627
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "PSCM2"
    rx_nodes = ['CCUMCUCD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class IRawPSCM2:
        sig_name = "IRawPSCM2"
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

    class URawPSCM2:
        sig_name = "URawPSCM2"
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


class PSCM2ToCCUMCUCDChassis2CANFDDiagRespFrame:
    msg_name = "PSCM2ToCCUMCUCDChassis2CANFDDiagRespFrame"
    msg_id = 1568
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "PSCM2"
    rx_nodes = ['CCUMCUCD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class MGMChassis2CANFDCanNmFr:
    msg_name = "MGMChassis2CANFDCanNmFr"
    msg_id = 1289
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "MGM"
    rx_nodes = ['IEM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class VCUChassis2CANFDCanNmFr:
    msg_name = "VCUChassis2CANFDCanNmFr"
    msg_id = 1285
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "VCU"
    rx_nodes = ['PSCM2']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class CCUMCUCDChassis2CANFDFr03:
    msg_name = "CCUMCUCDChassis2CANFDFr03"
    msg_id = 336
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.04
    msg_length = 8
    tx_node = "CCUMCUCD"
    rx_nodes = ['BCU2']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class FLLtchPosn:
        sig_name = "FLLtchPosn"
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
        sig_value_table = {'LatPosn_Unknow': 0, 'LatPosn_FullOpen': 1, 'LatPosn_SecLtchPosn': 2, 'LatPosn_FullClose': 3}
        compute_method = None
        length = 2
        startbit = 3
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class EPBHpsAvl:
        sig_name = "EPBHpsAvl"
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
        sig_value_table = {'AvlSts2_NotAvl': 0, 'AvlSts2_Avl': 1}
        compute_method = None
        length = 1
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class EPBHpsAck:
        sig_name = "EPBHpsAck"
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
        sig_value_table = {'NoYes3_No': 0, 'NoYes3_Yes': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7


class IEMChassis2CANFDCanNmFr:
    msg_name = "IEMChassis2CANFDCanNmFr"
    msg_id = 1288
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "IEM"
    rx_nodes = ['CCUMCUCD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class VCUChassis2CANFDFr05:
    msg_name = "VCUChassis2CANFDFr05"
    msg_id = 417
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 64
    tx_node = "VCU"
    rx_nodes = ['CCUMCUCD']
    sig_group_dict = {'EgyConsSlopReducCoeff': ['EgyConsSlopReducCoeffSlop10', 'EgyConsSlopReducCoeffSlop12', 'EgyConsSlopReducCoeffSlop14', 'EgyConsSlopReducCoeffSlop2', 'EgyConsSlopReducCoeffSlop4', 'EgyConsSlopReducCoeffSlop6', 'EgyConsSlopReducCoeffSlop8'], 'EgyCnsFacVehSpd': ['EgyCnsFacVehSpdSpd10', 'EgyCnsFacVehSpdSpd100', 'EgyCnsFacVehSpdSpd120', 'EgyCnsFacVehSpdSpd140', 'EgyCnsFacVehSpdSpd20', 'EgyCnsFacVehSpdSpd40', 'EgyCnsFacVehSpdSpd60', 'EgyCnsFacVehSpdSpd80'], 'EgyConsSlopRiseCoeff': ['EgyConsSlopRiseCoeffSlop10', 'EgyConsSlopRiseCoeffSlop12', 'EgyConsSlopRiseCoeffSlop14', 'EgyConsSlopRiseCoeffSlop2', 'EgyConsSlopRiseCoeffSlop4', 'EgyConsSlopRiseCoeffSlop6', 'EgyConsSlopRiseCoeffSlop8']}
    sig_group_dataid_dict = {}

    class HMIVehSpdLimnIndcnMsg:
        sig_name = "HMIVehSpdLimnIndcnMsg"
        sig_start_bit = 407
        update_id_bit = 403
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
        startbit = 407
        byte = 50
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class EgyConsSlopRiseCoeffSlop8:
        sig_name = "EgyConsSlopRiseCoeffSlop8"
        sig_start_bit = 258
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
        startbit = 258
        bmuws_info = [(32, 0b00000111, 0b11111000, 3, 0), (33, 0b11110000, 0b00001111, 4, 4)]

    class EgyConsSlopRiseCoeffSlop4:
        sig_name = "EgyConsSlopRiseCoeffSlop4"
        sig_start_bit = 240
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
        startbit = 240
        bmuws_info = [(30, 0b00000001, 0b11111110, 1, 0), (31, 0b11111100, 0b00000011, 6, 2)]

    class DischrgStopByTarDrvrIndcn:
        sig_name = "DischrgStopByTarDrvrIndcn"
        sig_start_bit = 111
        update_id_bit = 109
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
        startbit = 111
        byte = 13
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class DrvModActInd:
        sig_name = "DrvModActInd"
        sig_start_bit = 119
        update_id_bit = 115
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
        startbit = 119
        byte = 14
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class EgyCnsFacVehSpdSpd10:
        sig_name = "EgyCnsFacVehSpdSpd10"
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

    class EgyConsSlopRiseCoeffSlop14:
        sig_name = "EgyConsSlopRiseCoeffSlop14"
        sig_start_bit = 285
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
        startbit = 285
        bmuws_info = [(35, 0b00111111, 0b11000000, 6, 0), (36, 0b10000000, 0b01111111, 1, 7)]

    class EgyResdOfDischrg:
        sig_name = "EgyResdOfDischrg"
        sig_start_bit = 303
        update_id_bit = 306
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
        startbit = 303
        bmuws_info = [(37, 0b11111111, 0b00000000, 8, 0), (38, 0b11111000, 0b00000111, 5, 3)]

    class EgyConsSlopReducCoeffSlop12:
        sig_name = "EgyConsSlopReducCoeffSlop12"
        sig_start_bit = 220
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
        startbit = 220
        bmuws_info = [(27, 0b00011111, 0b11100000, 5, 0), (28, 0b11000000, 0b00111111, 2, 6)]

    class BookChrgnTarSocFb:
        sig_name = "BookChrgnTarSocFb"
        sig_start_bit = 11
        update_id_bit = 17
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
        startbit = 11
        bmuws_info = [(1, 0b00001111, 0b11110000, 4, 0), (2, 0b11111100, 0b00000011, 6, 2)]

    class DchrgChrgnTarSOCFb:
        sig_name = "DchrgChrgnTarSOCFb"
        sig_start_bit = 91
        update_id_bit = 96
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 200
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 91
        bmuws_info = [(11, 0b00001111, 0b11110000, 4, 0), (12, 0b11111110, 0b00000001, 7, 1)]

    class HMIPrpsnSysEgyRgnPwrLimd:
        sig_name = "HMIPrpsnSysEgyRgnPwrLimd"
        sig_start_bit = 382
        update_id_bit = 380
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
        startbit = 382
        byte = 47
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class EgyConsSlopReducCoeffSlop4:
        sig_name = "EgyConsSlopReducCoeffSlop4"
        sig_start_bit = 184
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
        startbit = 184
        bmuws_info = [(23, 0b00000001, 0b11111110, 1, 0), (24, 0b11111100, 0b00000011, 6, 2)]

    class HMIHvBattEgyIn:
        sig_name = "HMIHvBattEgyIn"
        sig_start_bit = 367
        update_id_bit = 352
        sig_length = 8
        sig_value_factor = 0.5
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

    class HMIDstEstimdFromTarFb:
        sig_name = "HMIDstEstimdFromTarFb"
        sig_start_bit = 323
        update_id_bit = 320
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
        startbit = 323
        byte = 40
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class DrvModAct:
        sig_name = "DrvModAct"
        sig_start_bit = 108
        update_id_bit = 104
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
        startbit = 108
        byte = 13
        mask = 0b00011110
        unmask = 0b11100001
        shift = 1

    class EgyConsSlopRiseCoeffSlop6:
        sig_name = "EgyConsSlopRiseCoeffSlop6"
        sig_start_bit = 249
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
        startbit = 249
        bmuws_info = [(31, 0b00000011, 0b11111100, 2, 0), (32, 0b11111000, 0b00000111, 5, 3)]

    class EgyCnsFacVehSpdSpd80:
        sig_name = "EgyCnsFacVehSpdSpd80"
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

    class HMIVehSpdLimnVisAudWarn:
        sig_name = "HMIVehSpdLimnVisAudWarn"
        sig_start_bit = 394
        update_id_bit = 392
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AdjSpdLimnWarnCoding_NoWarn': 0, 'AdjSpdLimnWarnCoding_SoundWarn': 1, 'AdjSpdLimnWarnCoding_VisWarn': 2, 'AdjSpdLimnWarnCoding_SoundAndVisWarn': 3}
        compute_method = None
        length = 2
        startbit = 394
        byte = 49
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class AccrTqModSteplessAct:
        sig_name = "AccrTqModSteplessAct"
        sig_start_bit = 7
        update_id_bit = 15
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

    class ChrgnSpdIndcnVal:
        sig_name = "ChrgnSpdIndcnVal"
        sig_start_bit = 26
        update_id_bit = 47
        sig_length = 11
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 26
        bmuws_info = [(3, 0b00000111, 0b11111000, 3, 0), (4, 0b11111111, 0b00000000, 8, 0)]

    class HMIHvBattEgyOut:
        sig_name = "HMIHvBattEgyOut"
        sig_start_bit = 375
        update_id_bit = 383
        sig_length = 8
        sig_value_factor = 0.5
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

    class EgyCnsFacVehSpdSpd60:
        sig_name = "EgyCnsFacVehSpdSpd60"
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

    class HMIEstimdRemainDstRng:
        sig_name = "HMIEstimdRemainDstRng"
        sig_start_bit = 351
        update_id_bit = 357
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
        startbit = 351
        bmuws_info = [(43, 0b11111111, 0b00000000, 8, 0), (44, 0b11000000, 0b00111111, 2, 6)]

    class HMIBrkRgnPwrPercMin:
        sig_name = "HMIBrkRgnPwrPercMin"
        sig_start_bit = 318
        update_id_bit = 324
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = -50.0
        sig_value_min = -500
        sig_value_max = 500
        sig_byteorder = "Motorola"
        sig_value_init = 500
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 318
        bmuws_info = [(39, 0b01111111, 0b10000000, 7, 0), (40, 0b11100000, 0b00011111, 3, 5)]

    class EgyCnsFacVehSpdSpd140:
        sig_name = "EgyCnsFacVehSpdSpd140"
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

    class EgyConsSlopReducCoeff_UB:
        sig_name = "EgyConsSlopReducCoeff_UB"
        sig_start_bit = 238
        update_id_bit = 238
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
        startbit = 238
        byte = 29
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class EgyConsSlopReducCoeffSlop10:
        sig_name = "EgyConsSlopReducCoeffSlop10"
        sig_start_bit = 211
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
        startbit = 211
        bmuws_info = [(26, 0b00001111, 0b11110000, 4, 0), (27, 0b11100000, 0b00011111, 3, 5)]

    class CrpModStsAct:
        sig_name = "CrpModStsAct"
        sig_start_bit = 46
        update_id_bit = 44
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
        startbit = 46
        byte = 5
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class BookChrgnActStsFb:
        sig_name = "BookChrgnActStsFb"
        sig_start_bit = 14
        update_id_bit = 12
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BookChrgnSts_Default': 0, 'BookChrgnSts_Success': 1, 'BookChrgnSts_Finished': 2, 'BookChrgnSts_Fail': 3}
        compute_method = None
        length = 2
        startbit = 14
        byte = 1
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class EgyConsSlopRiseCoeffSlop2:
        sig_name = "EgyConsSlopRiseCoeffSlop2"
        sig_start_bit = 247
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
        startbit = 247
        byte = 30
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class EgyCnsFacVehSpd_UB:
        sig_name = "EgyCnsFacVehSpd_UB"
        sig_start_bit = 112
        update_id_bit = 112
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
        startbit = 112
        byte = 14
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class DchaUAct:
        sig_name = "DchaUAct"
        sig_start_bit = 87
        update_id_bit = 92
        sig_length = 11
        sig_value_factor = 0.25
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2044
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 87
        bmuws_info = [(10, 0b11111111, 0b00000000, 8, 0), (11, 0b11100000, 0b00011111, 3, 5)]

    class EgyConsSlopReducCoeffSlop14:
        sig_name = "EgyConsSlopReducCoeffSlop14"
        sig_start_bit = 229
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
        startbit = 229
        bmuws_info = [(28, 0b00111111, 0b11000000, 6, 0), (29, 0b10000000, 0b01111111, 1, 7)]

    class HMIEgyRgnLimCmpMsg:
        sig_name = "HMIEgyRgnLimCmpMsg"
        sig_start_bit = 340
        update_id_bit = 336
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
        startbit = 340
        byte = 42
        mask = 0b00011110
        unmask = 0b11100001
        shift = 1

    class EgyConsSlopRiseCoeffSlop10:
        sig_name = "EgyConsSlopRiseCoeffSlop10"
        sig_start_bit = 267
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
        startbit = 267
        bmuws_info = [(33, 0b00001111, 0b11110000, 4, 0), (34, 0b11100000, 0b00011111, 3, 5)]

    class EgyConsSlopReducCoeffSlop6:
        sig_name = "EgyConsSlopReducCoeffSlop6"
        sig_start_bit = 193
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
        startbit = 193
        bmuws_info = [(24, 0b00000011, 0b11111100, 2, 0), (25, 0b11111000, 0b00000111, 5, 3)]

    class HMIStopModAct:
        sig_name = "HMIStopModAct"
        sig_start_bit = 398
        update_id_bit = 395
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EPedlMod_Initial': 0, 'EPedlMod_Crp': 1, 'EPedlMod_EPedl': 2, 'EPedlMod_Roll': 3, 'EPedlMod_Resvd': 4}
        compute_method = None
        length = 3
        startbit = 398
        byte = 49
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class DchaEgyAct:
        sig_name = "DchaEgyAct"
        sig_start_bit = 43
        update_id_bit = 48
        sig_length = 11
        sig_value_factor = 100
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 43
        bmuws_info = [(5, 0b00001111, 0b11110000, 4, 0), (6, 0b11111110, 0b00000001, 7, 1)]

    class HMIPrpsnSysMod:
        sig_name = "HMIPrpsnSysMod"
        sig_start_bit = 356
        update_id_bit = 379
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
        startbit = 356
        byte = 44
        mask = 0b00011110
        unmask = 0b11100001
        shift = 1

    class EgyConsSlopReducCoeffSlop8:
        sig_name = "EgyConsSlopReducCoeffSlop8"
        sig_start_bit = 202
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
        startbit = 202
        bmuws_info = [(25, 0b00000111, 0b11111000, 3, 0), (26, 0b11110000, 0b00001111, 4, 4)]

    class HMIDstEstimdRemainDstRngECO:
        sig_name = "HMIDstEstimdRemainDstRngECO"
        sig_start_bit = 335
        update_id_bit = 341
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
        startbit = 335
        bmuws_info = [(41, 0b11111111, 0b00000000, 8, 0), (42, 0b11000000, 0b00111111, 2, 6)]

    class ChrgnOrDChrgnStsFb:
        sig_name = "ChrgnOrDChrgnStsFb"
        sig_start_bit = 16
        update_id_bit = 27
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 30
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ChrgnOrDChrgnSts_default': 0, 'ChrgnOrDChrgnSts_NoCharging': 1, 'ChrgnOrDChrgnSts_ACCharging': 2, 'ChrgnOrDChrgnSts_ACChargingEnd': 3, 'ChrgnOrDChrgnSts_ChrgnCmpl': 4, 'ChrgnOrDChrgnSts_Heating': 5, 'ChrgnOrDChrgnSts_BookCharging': 6, 'ChrgnOrDChrgnSts_NoDisCharging': 7, 'ChrgnOrDChrgnSts_DisCharging': 8, 'ChrgnOrDChrgnSts_DisChargingEnd': 9, 'ChrgnOrDChrgnSts_DisChrgnCmpl': 10, 'ChrgnOrDChrgnSts_ChrgnFault': 11, 'ChrgnOrDChrgnSts_DisChrgnFault': 12, 'ChrgnOrDChrgnSts_Reserved1': 13, 'ChrgnOrDChrgnSts_ACChrgnFltChrgrSide': 14, 'ChrgnOrDChrgnSts_DCCharging': 15, 'ChrgnOrDChrgnSts_Reserved2': 16, 'ChrgnOrDChrgnSts_Reserved3': 17, 'ChrgnOrDChrgnSts_ACChargingFaultVehSide': 18, 'ChrgnOrDChrgnSts_DCChargingFaultChrgrSideTemp': 19, 'ChrgnOrDChrgnSts_DCChargingFaultChrgrSideCon': 20, 'ChrgnOrDChrgnSts_DCChargingFaultChrgrSideHw': 21, 'ChrgnOrDChrgnSts_DCChargingFaultChrgrSideEmgy': 22, 'ChrgnOrDChrgnSts_DCChargingFaultChrgrSideCom': 23, 'ChrgnOrDChrgnSts_SuperCharging': 24, 'ChrgnOrDChrgnSts_ACChargingSuspend': 25, 'ChrgnOrDChrgnSts_DCChargingEnd': 26, 'ChrgnOrDChrgnSts_ACChrgnFltVehSide': 27, 'ChrgnOrDChrgnSts_BoostCharging': 28, 'ChrgnOrDChrgnSts_BoostchargingFlt': 29, 'ChrgnOrDChrgnSts_WirelessCharging': 30}
        compute_method = None
        length = 5
        startbit = 16
        bmuws_info = [(2, 0b00000001, 0b11111110, 1, 0), (3, 0b11110000, 0b00001111, 4, 4)]

    class DchaPwrAct:
        sig_name = "DchaPwrAct"
        sig_start_bit = 67
        update_id_bit = 72
        sig_length = 11
        sig_value_factor = 100
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 67
        bmuws_info = [(8, 0b00001111, 0b11110000, 4, 0), (9, 0b11111110, 0b00000001, 7, 1)]

    class EgyConsSlopRiseCoeff_UB:
        sig_name = "EgyConsSlopRiseCoeff_UB"
        sig_start_bit = 294
        update_id_bit = 294
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
        startbit = 294
        byte = 36
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class DchaIAct:
        sig_name = "DchaIAct"
        sig_start_bit = 63
        update_id_bit = 68
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 63
        bmuws_info = [(7, 0b11111111, 0b00000000, 8, 0), (8, 0b11100000, 0b00011111, 3, 5)]

    class EgyRgnLimCmpSts:
        sig_name = "EgyRgnLimCmpSts"
        sig_start_bit = 305
        update_id_bit = 319
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 1
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CrsCtrlrSts_Off': 1, 'CrsCtrlrSts_Stb': 2, 'CrsCtrlrSts_Actv': 3}
        compute_method = None
        length = 2
        startbit = 305
        byte = 38
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class EgyCnsFacVehSpdSpd120:
        sig_name = "EgyCnsFacVehSpdSpd120"
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

    class EgyCnsFacVehSpdSpd100:
        sig_name = "EgyCnsFacVehSpdSpd100"
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

    class HMIPwrPrpsnPercAct:
        sig_name = "HMIPwrPrpsnPercAct"
        sig_start_bit = 378
        update_id_bit = 399
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 378
        bmuws_info = [(47, 0b00000111, 0b11111000, 3, 0), (48, 0b11111111, 0b00000000, 8, 0)]

    class EgyCnsFacVehSpdSpd40:
        sig_name = "EgyCnsFacVehSpdSpd40"
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

    class EgyCnsFacVehSpdSpd20:
        sig_name = "EgyCnsFacVehSpdSpd20"
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

    class EgyConsSlopRiseCoeffSlop12:
        sig_name = "EgyConsSlopRiseCoeffSlop12"
        sig_start_bit = 276
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
        startbit = 276
        bmuws_info = [(34, 0b00011111, 0b11100000, 5, 0), (35, 0b11000000, 0b00111111, 2, 6)]

    class EgyConsSlopReducCoeffSlop2:
        sig_name = "EgyConsSlopReducCoeffSlop2"
        sig_start_bit = 191
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
        startbit = 191
        byte = 23
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1


class BCU2Chassis2CANFDCanNmFr:
    msg_name = "BCU2Chassis2CANFDCanNmFr"
    msg_id = 1284
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BCU2"
    rx_nodes = ['VCU']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class CCUMCUCDToAllChassis2CANFDDiagFuncReqFrame:
    msg_name = "CCUMCUCDToAllChassis2CANFDDiagFuncReqFrame"
    msg_id = 2047
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CCUMCUCD"
    rx_nodes = ['PSCM2', 'BCU2']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class VCUChassis2CANFDFr01:
    msg_name = "VCUChassis2CANFDFr01"
    msg_id = 56
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 16
    tx_node = "VCU"
    rx_nodes = ['CCUMCUCD']
    sig_group_dict = {'PropSysStBkp': ['PropSysStBkpCapibility', 'PropSysStBkpChks', 'PropSysStBkpCntr', 'PropSysStBkpCtrlSts', 'PropSysStBkpDegrad', 'PropSysStBkpModCfmd']}
    sig_group_dataid_dict = {}

    class PropSysStBkpCntr:
        sig_name = "PropSysStBkpCntr"
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

    class PropSysStBkp_UB:
        sig_name = "PropSysStBkp_UB"
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

    class AccrPedlValIntgr:
        sig_name = "AccrPedlValIntgr"
        sig_start_bit = 39
        update_id_bit = 29
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

    class PropSysStBkpModCfmd:
        sig_name = "PropSysStBkpModCfmd"
        sig_start_bit = 19
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
        startbit = 19
        byte = 2
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class GearAutoShiftModDsbl:
        sig_name = "GearAutoShiftModDsbl"
        sig_start_bit = 45
        update_id_bit = 27
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EnaDsblDefault_Default': 0, 'EnaDsblDefault_Enable': 1, 'EnaDsblDefault_Disable': 2, 'EnaDsblDefault_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 45
        byte = 5
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class PropSysStBkpCtrlSts:
        sig_name = "PropSysStBkpCtrlSts"
        sig_start_bit = 12
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
        startbit = 12
        byte = 1
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VehSpdLimnTqReq:
        sig_name = "VehSpdLimnTqReq"
        sig_start_bit = 55
        update_id_bit = 25
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

    class PropSysStBkpCapibility:
        sig_name = "PropSysStBkpCapibility"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DrvrGearShiftEna:
        sig_name = "DrvrGearShiftEna"
        sig_start_bit = 47
        update_id_bit = 28
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EnaDsblDefault_Default': 0, 'EnaDsblDefault_Enable': 1, 'EnaDsblDefault_Disable': 2, 'EnaDsblDefault_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 47
        byte = 5
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HVInhbReqFromSrvFb:
        sig_name = "HVInhbReqFromSrvFb"
        sig_start_bit = 43
        update_id_bit = 26
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

    class PropSysStBkpChks:
        sig_name = "PropSysStBkpChks"
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

    class PropSysStBkpDegrad:
        sig_name = "PropSysStBkpDegrad"
        sig_start_bit = 23
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
        startbit = 23
        byte = 2
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4


class CCUMCUCDChassis2CANFDFr04:
    msg_name = "CCUMCUCDChassis2CANFDFr04"
    msg_id = 416
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 48
    tx_node = "CCUMCUCD"
    rx_nodes = ['PSCM2', 'VCU']
    sig_group_dict = {'ChrgSoftSwCtrlSt': ['ChrgSoftSwCtrlStCmd', 'ChrgSoftSwCtrlStSource'], 'VehAxleTqDistbnReq': ['VehAxleTqDistbnReqManualAuto', 'VehAxleTqDistbnReqPerc'], 'Odometer': ['OdometerValidity', 'OdometerValue']}
    sig_group_dataid_dict = {}

    class LnchModReq:
        sig_name = "LnchModReq"
        sig_start_bit = 111
        update_id_bit = 96
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
        startbit = 111
        byte = 13
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HMIStopModReq:
        sig_name = "HMIStopModReq"
        sig_start_bit = 103
        update_id_bit = 100
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EPedlMod_Initial': 0, 'EPedlMod_Crp': 1, 'EPedlMod_EPedl': 2, 'EPedlMod_Roll': 3, 'EPedlMod_Resvd': 4}
        compute_method = None
        length = 3
        startbit = 103
        byte = 12
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class VehSpdLimnOnReq:
        sig_name = "VehSpdLimnOnReq"
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
        sig_value_table = {'SetSpdSts_Off': 0, 'SetSpdSts_ManuallySet': 1, 'SetSpdSts_AutomaticallySet': 2, 'SetSpdSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 114
        byte = 14
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class ChrgSoftSwCtrlStCmd:
        sig_name = "ChrgSoftSwCtrlStCmd"
        sig_start_bit = 151
        update_id_bit = None
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
        startbit = 151
        byte = 18
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class ChrgSoftSwCtrlSt_UB:
        sig_name = "ChrgSoftSwCtrlSt_UB"
        sig_start_bit = 145
        update_id_bit = 145
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
        startbit = 145
        byte = 18
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VehSpdLimnTargtValReq:
        sig_name = "VehSpdLimnTargtValReq"
        sig_start_bit = 143
        update_id_bit = 128
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
        startbit = 143
        byte = 17
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class OdometerValidity:
        sig_name = "OdometerValidity"
        sig_start_bit = 18
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
        startbit = 18
        byte = 2
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class IntllntChrgnReq:
        sig_name = "IntllntChrgnReq"
        sig_start_bit = 99
        update_id_bit = 97
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
        startbit = 99
        byte = 12
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class CstRgnModSet:
        sig_name = "CstRgnModSet"
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
        sig_value_table = {'OnOff2_On': 0, 'OnOff2_Off': 1}
        compute_method = None
        length = 1
        startbit = 75
        byte = 9
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class DrvModReqInd:
        sig_name = "DrvModReqInd"
        sig_start_bit = 95
        update_id_bit = 91
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
        startbit = 95
        byte = 11
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class ChrgSoftSwCtrlStSource:
        sig_name = "ChrgSoftSwCtrlStSource"
        sig_start_bit = 149
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 15
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HVCmdSource_HMI': 0, 'HVCmdSource_APP': 1, 'HVCmdSource_HVIntelligentChrgn': 2, 'HVCmdSource_Fota': 3, 'HVCmdSource_BookChrgn': 4, 'HVCmdSource_RemDrv': 5, 'HVCmdSource_Therm': 6, 'HVCmdSource_Reserved1': 7, 'HVCmdSource_Reserved2': 8, 'HVCmdSource_Default': 15}
        compute_method = None
        length = 4
        startbit = 149
        byte = 18
        mask = 0b00111100
        unmask = 0b11000011
        shift = 2

    class VehAxleTqDistbnReq_UB:
        sig_name = "VehAxleTqDistbnReq_UB"
        sig_start_bit = 131
        update_id_bit = 131
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
        startbit = 131
        byte = 16
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class EgyRgnLimCmpSet:
        sig_name = "EgyRgnLimCmpSet"
        sig_start_bit = 90
        update_id_bit = 88
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
        startbit = 90
        byte = 11
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class VehAxleTqDistbnModReq:
        sig_name = "VehAxleTqDistbnModReq"
        sig_start_bit = 119
        update_id_bit = 115
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VehAxleTqDistbnMod_Initial': 0, 'VehAxleTqDistbnMod_Auto': 1, 'VehAxleTqDistbnMod_Manual': 2, 'VehAxleTqDistbnMod_Unknow': 3, 'VehAxleTqDistbnMod_Reserved': 4}
        compute_method = None
        length = 4
        startbit = 119
        byte = 14
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class VehAxleTqDistbnReqManualAuto:
        sig_name = "VehAxleTqDistbnReqManualAuto"
        sig_start_bit = 135
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VehAxleTqDistbnMod_Initial': 0, 'VehAxleTqDistbnMod_Auto': 1, 'VehAxleTqDistbnMod_Manual': 2, 'VehAxleTqDistbnMod_Unknow': 3, 'VehAxleTqDistbnMod_Reserved': 4}
        compute_method = None
        length = 4
        startbit = 135
        byte = 16
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class V2XDchaSwt:
        sig_name = "V2XDchaSwt"
        sig_start_bit = 106
        update_id_bit = 104
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DisChrgrSW_Off': 0, 'DisChrgrSW_V2V': 1, 'DisChrgrSW_V2L': 2, 'DisChrgrSW_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 106
        byte = 13
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class AccrTqModSteplessReq:
        sig_name = "AccrTqModSteplessReq"
        sig_start_bit = 87
        update_id_bit = 72
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

    class OdometerValue:
        sig_name = "OdometerValue"
        sig_start_bit = 7
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
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111000, 0b00000111, 5, 3)]

    class VehAxleTqDistbnReqPerc:
        sig_name = "VehAxleTqDistbnReqPerc"
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

    class CrpModStsSet:
        sig_name = "CrpModStsSet"
        sig_start_bit = 78
        update_id_bit = 76
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
        startbit = 78
        byte = 9
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class VehTiGlb:
        sig_name = "VehTiGlb"
        sig_start_bit = 47
        update_id_bit = 79
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
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111111, 0b00000000, 8, 0), (8, 0b11111111, 0b00000000, 8, 0)]

    class VehBattU:
        sig_name = "VehBattU"
        sig_start_bit = 31
        update_id_bit = 37
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
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11000000, 0b00111111, 2, 6)]

    class LVBattChrgnReq:
        sig_name = "LVBattChrgnReq"
        sig_start_bit = 109
        update_id_bit = 107
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVChrgnReq_Idle': 0, 'LVChrgnReq_Chrgn': 1, 'LVChrgnReq_NoReq': 2, 'LVChrgnReq_Resvd': 3}
        compute_method = None
        length = 2
        startbit = 109
        byte = 13
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class Odometer_UB:
        sig_name = "Odometer_UB"
        sig_start_bit = 17
        update_id_bit = 17
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
        startbit = 17
        byte = 2
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1


class VCUChassis2CANFDFr02:
    msg_name = "VCUChassis2CANFDFr02"
    msg_id = 628
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 48
    tx_node = "VCU"
    rx_nodes = ['IEM', 'CCUMCUCD']
    sig_group_dict = {'RemBookStrtTiChrgnTmr': ['RemBookStrtTiChrgnTmrHr', 'RemBookStrtTiChrgnTmrMins'], 'DchaEgyStrg': ['DchaEgyStrgDchaCarTi', 'DchaEgyStrgDchaEgy'], 'BLEBookStrtTiChrgnTmr': ['BLEBookStrtTiChrgnTmrHr', 'BLEBookStrtTiChrgnTmrMins'], 'BLEBookStopTiChrgnTmr': ['BLEBookStopTiChrgnTmrHr', 'BLEBookStopTiChrgnTmrMins'], 'RemBookStopTiChrgnTmr': ['RemBookStopTiChrgnTmrHr', 'RemBookStopTiChrgnTmrMins']}
    sig_group_dataid_dict = {}

    class BLEBookStrtTiChrgnTmrHr:
        sig_name = "BLEBookStrtTiChrgnTmrHr"
        sig_start_bit = 19
        update_id_bit = None
        sig_length = 5
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 24
        sig_byteorder = "Motorola"
        sig_value_init = 24
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 19
        bmuws_info = [(2, 0b00001111, 0b11110000, 4, 0), (3, 0b10000000, 0b01111111, 1, 7)]

    class RemBookStrtTiChrgnTmr_UB:
        sig_name = "RemBookStrtTiChrgnTmr_UB"
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

    class HMILnchModFailIndcnMsg:
        sig_name = "HMILnchModFailIndcnMsg"
        sig_start_bit = 122
        update_id_bit = 133
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
        startbit = 122
        bmuws_info = [(15, 0b00000111, 0b11111000, 3, 0), (16, 0b11000000, 0b00111111, 2, 6)]

    class PrpsnSysDrftModAllwd:
        sig_name = "PrpsnSysDrftModAllwd"
        sig_start_bit = 204
        update_id_bit = 186
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
        startbit = 204
        byte = 25
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class PlsHeatgSts1:
        sig_name = "PlsHeatgSts1"
        sig_start_bit = 207
        update_id_bit = 185
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PlsHeatgSts_Idle': 0, 'PlsHeatgSts_Init': 1, 'PlsHeatgSts_Heatg': 2, 'PlsHeatgSts_Finish': 3, 'PlsHeatgSts_Err': 4, 'PlsHeatgSts_Inhb': 5, 'PlsHeatgSts_Reserve1': 6, 'PlsHeatgSts_Reserve2': 7}
        compute_method = None
        length = 3
        startbit = 207
        byte = 25
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DCChrgrUMaxDetn:
        sig_name = "DCChrgrUMaxDetn"
        sig_start_bit = 47
        update_id_bit = 63
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
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111111, 0b00000000, 8, 0)]

    class MCUBoostChrgRlyReq:
        sig_name = "MCUBoostChrgRlyReq"
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
        sig_value_table = {'ChrgRlySt_Open': 0, 'ChrgRlySt_Close': 1, 'ChrgRlySt_Reserved1': 2, 'ChrgRlySt_Reserved2': 3}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HVBattChrgPwrNormDes1:
        sig_name = "HVBattChrgPwrNormDes1"
        sig_start_bit = 165
        update_id_bit = 168
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
        startbit = 165
        bmuws_info = [(20, 0b00111111, 0b11000000, 6, 0), (21, 0b11111110, 0b00000001, 7, 1)]

    class HvBattDisChrgnTiEstim:
        sig_name = "HvBattDisChrgnTiEstim"
        sig_start_bit = 183
        update_id_bit = 188
        sig_length = 11
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 2047
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 183
        bmuws_info = [(22, 0b11111111, 0b00000000, 8, 0), (23, 0b11100000, 0b00011111, 3, 5)]

    class DrvgCycSts:
        sig_name = "DrvgCycSts"
        sig_start_bit = 111
        update_id_bit = 109
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OffOnInvld_Invalid1': 0, 'OffOnInvld_Off': 1, 'OffOnInvld_On': 2, 'OffOnInvld_Invalid2': 3}
        compute_method = None
        length = 2
        startbit = 111
        byte = 13
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class DchaEgyStrgDchaCarTi:
        sig_name = "DchaEgyStrgDchaCarTi"
        sig_start_bit = 79
        update_id_bit = None
        sig_length = 32
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4290000000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 32
        startbit = 79
        bmuws_info = [(9, 0b11111111, 0b00000000, 8, 0), (10, 0b11111111, 0b00000000, 8, 0), (11, 0b11111111, 0b00000000, 8, 0), (12, 0b11111111, 0b00000000, 8, 0)]

    class InhbPrpsnRdy:
        sig_name = "InhbPrpsnRdy"
        sig_start_bit = 271
        update_id_bit = 269
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoYesUkwn_No': 0, 'NoYesUkwn_Yes': 1, 'NoYesUkwn_Unknown': 2, 'NoYesUkwn_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 271
        byte = 33
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HMILnchModSts:
        sig_name = "HMILnchModSts"
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
        sig_value_table = {'LaunchModeSts_Disable': 0, 'LaunchModeSts_Initial': 1, 'LaunchModeSts_Standby': 2, 'LaunchModeSts_Ready': 3, 'LaunchModeSts_Active': 4, 'LaunchModeSts_Failed': 5, 'LaunchModeSts_Reserved1': 6, 'LaunchModeSts_Reserved2': 7}
        compute_method = None
        length = 3
        startbit = 132
        byte = 16
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class VehPrpsnSysActv:
        sig_name = "VehPrpsnSysActv"
        sig_start_bit = 263
        update_id_bit = 261
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
        startbit = 263
        byte = 32
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class RoadSlopInfo:
        sig_name = "RoadSlopInfo"
        sig_start_bit = 243
        update_id_bit = 248
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 243
        bmuws_info = [(30, 0b00001111, 0b11110000, 4, 0), (31, 0b11111110, 0b00000001, 7, 1)]

    class BookChrgSetResp:
        sig_name = "BookChrgSetResp"
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
        sig_value_table = {'BookChargeSetResponse_Default': 0, 'BookChargeSetResponse_Success': 1, 'BookChargeSetResponse_Cancelled': 2, 'BookChargeSetResponse_Fail': 3}
        compute_method = None
        length = 2
        startbit = 39
        byte = 4
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HMIGearShiftFailMsg:
        sig_name = "HMIGearShiftFailMsg"
        sig_start_bit = 115
        update_id_bit = 127
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

    class CstRgnModAct:
        sig_name = "CstRgnModAct"
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

    class VirtGearShiftModeAct:
        sig_name = "VirtGearShiftModeAct"
        sig_start_bit = 260
        update_id_bit = 259
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
        startbit = 260
        byte = 32
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class RemBookStrtTiChrgnTmrHr:
        sig_name = "RemBookStrtTiChrgnTmrHr"
        sig_start_bit = 239
        update_id_bit = None
        sig_length = 5
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 24
        sig_byteorder = "Motorola"
        sig_value_init = 24
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 239
        byte = 29
        mask = 0b11111000
        unmask = 0b00000111
        shift = 3

    class GearLvrIndcnVirt:
        sig_name = "GearLvrIndcnVirt"
        sig_start_bit = 108
        update_id_bit = 105
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GearLvrIndcn_Default': 0, 'GearLvrIndcn_P': 1, 'GearLvrIndcn_R': 2, 'GearLvrIndcn_N': 3, 'GearLvrIndcn_D': 4, 'GearLvrIndcn_Reserved1': 5, 'GearLvrIndcn_Reserved2': 6, 'GearLvrIndcn_Undefd': 7}
        compute_method = None
        length = 3
        startbit = 108
        byte = 13
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class RemBookStopTiChrgnTmrMins:
        sig_name = "RemBookStopTiChrgnTmrMins"
        sig_start_bit = 230
        update_id_bit = None
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 60
        sig_byteorder = "Motorola"
        sig_value_init = 60
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 230
        byte = 28
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class BLEBookStrtTiChrgnTmrMins:
        sig_name = "BLEBookStrtTiChrgnTmrMins"
        sig_start_bit = 30
        update_id_bit = None
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 60
        sig_byteorder = "Motorola"
        sig_value_init = 60
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 30
        byte = 3
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class DchaEgyStrg_UB:
        sig_name = "DchaEgyStrg_UB"
        sig_start_bit = 64
        update_id_bit = 64
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
        startbit = 64
        byte = 8
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class BLEBookStrtTiChrgnTmr_UB:
        sig_name = "BLEBookStrtTiChrgnTmr_UB"
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

    class InhbHvOn:
        sig_name = "InhbHvOn"
        sig_start_bit = 258
        update_id_bit = 256
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoYesUkwn_No': 0, 'NoYesUkwn_Yes': 1, 'NoYesUkwn_Unknown': 2, 'NoYesUkwn_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 258
        byte = 32
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class HMIEPedlIndcnMsg:
        sig_name = "HMIEPedlIndcnMsg"
        sig_start_bit = 119
        update_id_bit = 104
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
        startbit = 119
        byte = 14
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class PrpsnSysRaceModAllwd:
        sig_name = "PrpsnSysRaceModAllwd"
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
        sig_value_table = {'AllwdorNot_Init': 0, 'AllwdorNot_NotAllwd': 1, 'AllwdorNot_Allwd': 2, 'AllwdorNot_Resd1': 3}
        compute_method = None
        length = 2
        startbit = 212
        byte = 26
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class HMIGearShiftrFltMsg:
        sig_name = "HMIGearShiftrFltMsg"
        sig_start_bit = 126
        update_id_bit = 123
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
        startbit = 126
        byte = 15
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class BLEBookStopTiChrgnTmr_UB:
        sig_name = "BLEBookStopTiChrgnTmr_UB"
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

    class PrpsnSysSptModAllwd:
        sig_name = "PrpsnSysSptModAllwd"
        sig_start_bit = 209
        update_id_bit = 223
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
        startbit = 209
        byte = 26
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class PrpsnSysOffRoadModAllwd:
        sig_name = "PrpsnSysOffRoadModAllwd"
        sig_start_bit = 215
        update_id_bit = 213
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
        startbit = 215
        byte = 26
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HVBattChrgPwrCritDes1:
        sig_name = "HVBattChrgPwrCritDes1"
        sig_start_bit = 147
        update_id_bit = 166
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
        startbit = 147
        bmuws_info = [(18, 0b00001111, 0b11110000, 4, 0), (19, 0b11111111, 0b00000000, 8, 0), (20, 0b10000000, 0b01111111, 1, 7)]

    class RemBookStopTiChrgnTmr_UB:
        sig_name = "RemBookStopTiChrgnTmr_UB"
        sig_start_bit = 224
        update_id_bit = 224
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
        startbit = 224
        byte = 28
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class DCChrgPilBookChrgn:
        sig_name = "DCChrgPilBookChrgn"
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
        sig_value_table = {'ChrgPilBookChrgn_Default': 0, 'ChrgPilBookChrgn_On': 1, 'ChrgPilBookChrgn_Off': 2, 'ChrgPilBookChrgn_Reserve': 3}
        compute_method = None
        length = 2
        startbit = 34
        byte = 4
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class PrpsnSysECOPlusModAllwd:
        sig_name = "PrpsnSysECOPlusModAllwd"
        sig_start_bit = 202
        update_id_bit = 200
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
        startbit = 202
        byte = 25
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class DchaEgyStrgDchaEgy:
        sig_name = "DchaEgyStrgDchaEgy"
        sig_start_bit = 62
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 100
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 62
        bmuws_info = [(7, 0b01111111, 0b10000000, 7, 0), (8, 0b11110000, 0b00001111, 4, 4)]

    class BLEBookStopTiChrgnTmrHr:
        sig_name = "BLEBookStopTiChrgnTmrHr"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 5
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 24
        sig_byteorder = "Motorola"
        sig_value_init = 24
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 15
        byte = 1
        mask = 0b11111000
        unmask = 0b00000111
        shift = 3

    class RemBookStopTiChrgnTmrHr:
        sig_name = "RemBookStopTiChrgnTmrHr"
        sig_start_bit = 219
        update_id_bit = None
        sig_length = 5
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 24
        sig_byteorder = "Motorola"
        sig_value_init = 24
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 219
        bmuws_info = [(27, 0b00001111, 0b11110000, 4, 0), (28, 0b10000000, 0b01111111, 1, 7)]

    class MCUBoostStsReq:
        sig_name = "MCUBoostStsReq"
        sig_start_bit = 4
        update_id_bit = 1
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 5
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BoostStsReq_Init': 0, 'BoostStsReq_C1Precharge': 1, 'BoostStsReq_BoostReady': 2, 'BoostStsReq_BoostActive': 3, 'BoostStsReq_C1ActiveDisChrgn': 4, 'BoostStsReq_BoostOff': 5, 'BoostStsReq_Reserved1': 6, 'BoostStsReq_Reserved2': 7}
        compute_method = None
        length = 3
        startbit = 4
        byte = 0
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class HVBattChrgnTiEstim:
        sig_name = "HVBattChrgnTiEstim"
        sig_start_bit = 143
        update_id_bit = 148
        sig_length = 11
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 2047
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 143
        bmuws_info = [(17, 0b11111111, 0b00000000, 8, 0), (18, 0b11100000, 0b00011111, 3, 5)]

    class PrpsnSysTracModAllwd:
        sig_name = "PrpsnSysTracModAllwd"
        sig_start_bit = 222
        update_id_bit = 220
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
        startbit = 222
        byte = 27
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class BLEBookStopTiChrgnTmrMins:
        sig_name = "BLEBookStopTiChrgnTmrMins"
        sig_start_bit = 10
        update_id_bit = None
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 60
        sig_byteorder = "Motorola"
        sig_value_init = 60
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 10
        bmuws_info = [(1, 0b00000111, 0b11111000, 3, 0), (2, 0b11100000, 0b00011111, 3, 5)]

    class RemBookStrtTiChrgnTmrMins:
        sig_name = "RemBookStrtTiChrgnTmrMins"
        sig_start_bit = 234
        update_id_bit = None
        sig_length = 6
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 60
        sig_byteorder = "Motorola"
        sig_value_init = 60
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 234
        bmuws_info = [(29, 0b00000111, 0b11111000, 3, 0), (30, 0b11100000, 0b00011111, 3, 5)]

    class OnBdChrgrPortT:
        sig_name = "OnBdChrgrPortT"
        sig_start_bit = 199
        update_id_bit = 184
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 40
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 199
        byte = 24
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class VCUChassis2CANFDFr04:
    msg_name = "VCUChassis2CANFDFr04"
    msg_id = 291
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.03
    msg_length = 8
    tx_node = "VCU"
    rx_nodes = ['CCUMCUCD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HMIPrpsnSysErrIndcnReq:
        sig_name = "HMIPrpsnSysErrIndcnReq"
        sig_start_bit = 1
        update_id_bit = 0
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
        startbit = 1
        byte = 0
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class HMITurtlePwrLossIndcn:
        sig_name = "HMITurtlePwrLossIndcn"
        sig_start_bit = 10
        update_id_bit = 8
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
        startbit = 10
        byte = 1
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class AdjSpdLimnActvnOk:
        sig_name = "AdjSpdLimnActvnOk"
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
        sig_value_table = {'OnOffNoCmd_NoCmd': 0, 'OnOffNoCmd_OFF': 1, 'OnOffNoCmd_ON': 2}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HMIPrpsnSysFltMsg:
        sig_name = "HMIPrpsnSysFltMsg"
        sig_start_bit = 15
        update_id_bit = 11
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

    class HMIHzrdLiIndcnReq:
        sig_name = "HMIHzrdLiIndcnReq"
        sig_start_bit = 4
        update_id_bit = 2
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
        startbit = 4
        byte = 0
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3


