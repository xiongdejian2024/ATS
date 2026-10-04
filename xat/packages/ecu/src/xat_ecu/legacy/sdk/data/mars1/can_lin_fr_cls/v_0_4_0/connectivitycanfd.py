class VgmConnFr08:
    msg_name = "VgmConnFr08"
    msg_id = 512
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DoorOpenerDrvrSts:
        sig_name = "DoorOpenerDrvrSts"
        sig_start_bit = 7
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 10
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorOpenerSts_Ukwn': 0, 'DoorOpenerSts_FullClsd': 1, 'DoorOpenerSts_MovgOut': 2, 'DoorOpenerSts_MovgOutBrkg': 3, 'DoorOpenerSts_StopDurgOpen': 4, 'DoorOpenerSts_FullOpend': 5, 'DoorOpenerSts_MovgIn': 6, 'DoorOpenerSts_MovgInBrkg': 7, 'DoorOpenerSts_StopDurgCls': 8, 'DoorOpenerSts_HalfClsd': 9, 'DoorOpenerSts_StopMinPntForCls': 10}
        compute_method = None
        length = 4
        startbit = 7
        byte = 0
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DoorOpenerRiReSts:
        sig_name = "DoorOpenerRiReSts"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 10
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorOpenerSts_Ukwn': 0, 'DoorOpenerSts_FullClsd': 1, 'DoorOpenerSts_MovgOut': 2, 'DoorOpenerSts_MovgOutBrkg': 3, 'DoorOpenerSts_StopDurgOpen': 4, 'DoorOpenerSts_FullOpend': 5, 'DoorOpenerSts_MovgIn': 6, 'DoorOpenerSts_MovgInBrkg': 7, 'DoorOpenerSts_StopDurgCls': 8, 'DoorOpenerSts_HalfClsd': 9, 'DoorOpenerSts_StopMinPntForCls': 10}
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DoorPassLockSts:
        sig_name = "DoorPassLockSts"
        sig_start_bit = 53
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LockSts2_LockStsUkwn': 0, 'LockSts2_Unlckd': 1, 'LockSts2_Lockd': 2, 'LockSts2_SafeLockd': 3}
        compute_method = None
        length = 2
        startbit = 53
        byte = 6
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class DoorOpenerLeReSts:
        sig_name = "DoorOpenerLeReSts"
        sig_start_bit = 3
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 10
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorOpenerSts_Ukwn': 0, 'DoorOpenerSts_FullClsd': 1, 'DoorOpenerSts_MovgOut': 2, 'DoorOpenerSts_MovgOutBrkg': 3, 'DoorOpenerSts_StopDurgOpen': 4, 'DoorOpenerSts_FullOpend': 5, 'DoorOpenerSts_MovgIn': 6, 'DoorOpenerSts_MovgInBrkg': 7, 'DoorOpenerSts_StopDurgCls': 8, 'DoorOpenerSts_HalfClsd': 9, 'DoorOpenerSts_StopMinPntForCls': 10}
        compute_method = None
        length = 4
        startbit = 3
        byte = 0
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DoorLeReLockSts:
        sig_name = "DoorLeReLockSts"
        sig_start_bit = 55
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LockSts2_LockStsUkwn': 0, 'LockSts2_Unlckd': 1, 'LockSts2_Lockd': 2, 'LockSts2_SafeLockd': 3}
        compute_method = None
        length = 2
        startbit = 55
        byte = 6
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class DoorOpenerPassSts:
        sig_name = "DoorOpenerPassSts"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 10
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorOpenerSts_Ukwn': 0, 'DoorOpenerSts_FullClsd': 1, 'DoorOpenerSts_MovgOut': 2, 'DoorOpenerSts_MovgOutBrkg': 3, 'DoorOpenerSts_StopDurgOpen': 4, 'DoorOpenerSts_FullOpend': 5, 'DoorOpenerSts_MovgIn': 6, 'DoorOpenerSts_MovgInBrkg': 7, 'DoorOpenerSts_StopDurgCls': 8, 'DoorOpenerSts_HalfClsd': 9, 'DoorOpenerSts_StopMinPntForCls': 10}
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DoorLeReSts:
        sig_name = "DoorLeReSts"
        sig_start_bit = 39
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorSts2_Ukwn': 0, 'DoorSts2_Opend': 1, 'DoorSts2_Clsd': 2}
        compute_method = None
        length = 2
        startbit = 39
        byte = 4
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class DoorRiReSts:
        sig_name = "DoorRiReSts"
        sig_start_bit = 35
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorSts2_Ukwn': 0, 'DoorSts2_Opend': 1, 'DoorSts2_Clsd': 2}
        compute_method = None
        length = 2
        startbit = 35
        byte = 4
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class DoorPassSts:
        sig_name = "DoorPassSts"
        sig_start_bit = 37
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorSts2_Ukwn': 0, 'DoorSts2_Opend': 1, 'DoorSts2_Clsd': 2}
        compute_method = None
        length = 2
        startbit = 37
        byte = 4
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class DoorDrvrLockSts:
        sig_name = "DoorDrvrLockSts"
        sig_start_bit = 22
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LockSts2_LockStsUkwn': 0, 'LockSts2_Unlckd': 1, 'LockSts2_Lockd': 2, 'LockSts2_SafeLockd': 3}
        compute_method = None
        length = 2
        startbit = 22
        byte = 2
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class ClsdDueToRain:
        sig_name = "ClsdDueToRain"
        sig_start_bit = 16
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 16
        byte = 2
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class DoorRiReLockSts:
        sig_name = "DoorRiReLockSts"
        sig_start_bit = 51
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LockSts2_LockStsUkwn': 0, 'LockSts2_Unlckd': 1, 'LockSts2_Lockd': 2, 'LockSts2_SafeLockd': 3}
        compute_method = None
        length = 2
        startbit = 51
        byte = 6
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2


class VgmConnFr16:
    msg_name = "VgmConnFr16"
    msg_id = 343
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "BGM"
    rx_nodes = []

    class DigKeyBLEResp:
        sig_name = "DigKeyBLEResp"
        sig_start_bit = 0
        sig_length = 512
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = None
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 512
        startbit = 0
        bmuws_info = [(0, 0b00000001, 0b11111110, 1, 0), (1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111111, 0b00000000, 8, 0), (8, 0b11111111, 0b00000000, 8, 0), (9, 0b11111111, 0b00000000, 8, 0), (10, 0b11111111, 0b00000000, 8, 0), (11, 0b11111111, 0b00000000, 8, 0), (12, 0b11111111, 0b00000000, 8, 0), (13, 0b11111111, 0b00000000, 8, 0), (14, 0b11111111, 0b00000000, 8, 0), (15, 0b11111111, 0b00000000, 8, 0), (16, 0b11111111, 0b00000000, 8, 0), (17, 0b11111111, 0b00000000, 8, 0), (18, 0b11111111, 0b00000000, 8, 0), (19, 0b11111111, 0b00000000, 8, 0), (20, 0b11111111, 0b00000000, 8, 0), (21, 0b11111111, 0b00000000, 8, 0), (22, 0b11111111, 0b00000000, 8, 0), (23, 0b11111111, 0b00000000, 8, 0), (24, 0b11111111, 0b00000000, 8, 0), (25, 0b11111111, 0b00000000, 8, 0), (26, 0b11111111, 0b00000000, 8, 0), (27, 0b11111111, 0b00000000, 8, 0), (28, 0b11111111, 0b00000000, 8, 0), (29, 0b11111111, 0b00000000, 8, 0), (30, 0b11111111, 0b00000000, 8, 0), (31, 0b11111111, 0b00000000, 8, 0), (32, 0b11111111, 0b00000000, 8, 0), (33, 0b11111111, 0b00000000, 8, 0), (34, 0b11111111, 0b00000000, 8, 0), (35, 0b11111111, 0b00000000, 8, 0), (36, 0b11111111, 0b00000000, 8, 0), (37, 0b11111111, 0b00000000, 8, 0), (38, 0b11111111, 0b00000000, 8, 0), (39, 0b11111111, 0b00000000, 8, 0), (40, 0b11111111, 0b00000000, 8, 0), (41, 0b11111111, 0b00000000, 8, 0), (42, 0b11111111, 0b00000000, 8, 0), (43, 0b11111111, 0b00000000, 8, 0), (44, 0b11111111, 0b00000000, 8, 0), (45, 0b11111111, 0b00000000, 8, 0), (46, 0b11111111, 0b00000000, 8, 0), (47, 0b11111111, 0b00000000, 8, 0), (48, 0b11111111, 0b00000000, 8, 0), (49, 0b11111111, 0b00000000, 8, 0), (50, 0b11111111, 0b00000000, 8, 0), (51, 0b11111111, 0b00000000, 8, 0), (52, 0b11111111, 0b00000000, 8, 0), (53, 0b11111111, 0b00000000, 8, 0), (54, 0b11111111, 0b00000000, 8, 0), (55, 0b11111111, 0b00000000, 8, 0), (56, 0b11111111, 0b00000000, 8, 0), (57, 0b11111111, 0b00000000, 8, 0), (58, 0b11111111, 0b00000000, 8, 0), (59, 0b11111111, 0b00000000, 8, 0), (60, 0b11111111, 0b00000000, 8, 0), (61, 0b11111111, 0b00000000, 8, 0), (62, 0b11111111, 0b00000000, 8, 0), (63, 0b11111111, 0b00000000, 8, 0), (64, 0b11111110, 0b00000001, 7, 1)]


class TcamConnectivityFr04:
    msg_name = "TcamConnectivityFr04"
    msg_id = 330
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class ChrgLidTelmLockgReq:
        sig_name = "ChrgLidTelmLockgReq"
        sig_start_bit = 1
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class TankFlapTelmLockgReq:
        sig_name = "TankFlapTelmLockgReq"
        sig_start_bit = 7
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LockActvn2_LockActvnOff': 0, 'LockActvn2_LockActvnUnlck': 1, 'LockActvn2_LockActvnLock': 2, 'LockActvn2_LockActvnSafe': 3, 'LockActvn2_LockActvnUnlckByCrash': 4}
        compute_method = None
        length = 3
        startbit = 7
        byte = 0
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class CbnOverHeatProtnEnaFromTelm:
        sig_name = "CbnOverHeatProtnEnaFromTelm"
        sig_start_bit = 11
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 11
        byte = 1
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class RemChkTInVeh:
        sig_name = "RemChkTInVeh"
        sig_start_bit = 9
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ReqSts1_NotReqd': 0, 'ReqSts1_Reqd': 1}
        compute_method = None
        length = 1
        startbit = 9
        byte = 1
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1


class VgmConnFr01:
    msg_name = "VgmConnFr01"
    msg_id = 288
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class VehModMngtGlbSafe1FltEgyCnsWdSts:
        sig_name = "VehModMngtGlbSafe1FltEgyCnsWdSts"
        sig_start_bit = 33
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class VehModMngtGlbSafe1EgyLvlElecMai:
        sig_name = "VehModMngtGlbSafe1EgyLvlElecMai"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class VehModMngtGlbSafe1UsgModSts:
        sig_name = "VehModMngtGlbSafe1UsgModSts"
        sig_start_bit = 27
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 13
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

    class DoorAcsKeyIsReq:
        sig_name = "DoorAcsKeyIsReq"
        sig_start_bit = 63
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LockgCenReq2_Idle': 0, 'LockgCenReq2_Unlck': 1, 'LockgCenReq2_Lock': 2}
        compute_method = None
        length = 2
        startbit = 63
        byte = 7
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class VehModMngtGlbSafe1Cntr:
        sig_name = "VehModMngtGlbSafe1Cntr"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp:
        sig_name = "VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp"
        sig_start_bit = 36
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class WinPosnStsAtPass:
        sig_name = "WinPosnStsAtPass"
        sig_start_bit = 52
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 31
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WinAndRoofAndCurtPosnTyp_PosnUkwn': 0, 'WinAndRoofAndCurtPosnTyp_ClsFull': 1, 'WinAndRoofAndCurtPosnTyp_PercOpen4': 2, 'WinAndRoofAndCurtPosnTyp_PercOpen8': 3, 'WinAndRoofAndCurtPosnTyp_PercOpen12': 4, 'WinAndRoofAndCurtPosnTyp_PercOpen16': 5, 'WinAndRoofAndCurtPosnTyp_PercOpen20': 6, 'WinAndRoofAndCurtPosnTyp_PercOpen24': 7, 'WinAndRoofAndCurtPosnTyp_PercOpen28': 8, 'WinAndRoofAndCurtPosnTyp_PercOpen32': 9, 'WinAndRoofAndCurtPosnTyp_PercOpen36': 10, 'WinAndRoofAndCurtPosnTyp_PercOpen40': 11, 'WinAndRoofAndCurtPosnTyp_PercOpen44': 12, 'WinAndRoofAndCurtPosnTyp_PercOpen48': 13, 'WinAndRoofAndCurtPosnTyp_PercOpen52': 14, 'WinAndRoofAndCurtPosnTyp_PercOpen56': 15, 'WinAndRoofAndCurtPosnTyp_PercOpen60': 16, 'WinAndRoofAndCurtPosnTyp_PercOpen64': 17, 'WinAndRoofAndCurtPosnTyp_PercOpen68': 18, 'WinAndRoofAndCurtPosnTyp_PercOpen72': 19, 'WinAndRoofAndCurtPosnTyp_PercOpen76': 20, 'WinAndRoofAndCurtPosnTyp_PercOpen80': 21, 'WinAndRoofAndCurtPosnTyp_PercOpen84': 22, 'WinAndRoofAndCurtPosnTyp_PercOpen88': 23, 'WinAndRoofAndCurtPosnTyp_PercOpen92': 24, 'WinAndRoofAndCurtPosnTyp_PercOpen96': 25, 'WinAndRoofAndCurtPosnTyp_OpenFull': 26, 'WinAndRoofAndCurtPosnTyp_Resd1': 27, 'WinAndRoofAndCurtPosnTyp_Resd2': 28, 'WinAndRoofAndCurtPosnTyp_Resd3': 29, 'WinAndRoofAndCurtPosnTyp_Resd4': 30, 'WinAndRoofAndCurtPosnTyp_Movg': 31}
        compute_method = None
        length = 5
        startbit = 52
        byte = 6
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class VehModMngtGlbSafe1PwrLvlElecSubtyp:
        sig_name = "VehModMngtGlbSafe1PwrLvlElecSubtyp"
        sig_start_bit = 31
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class WinPosnStsAtDrvr:
        sig_name = "WinPosnStsAtDrvr"
        sig_start_bit = 44
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 31
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WinAndRoofAndCurtPosnTyp_PosnUkwn': 0, 'WinAndRoofAndCurtPosnTyp_ClsFull': 1, 'WinAndRoofAndCurtPosnTyp_PercOpen4': 2, 'WinAndRoofAndCurtPosnTyp_PercOpen8': 3, 'WinAndRoofAndCurtPosnTyp_PercOpen12': 4, 'WinAndRoofAndCurtPosnTyp_PercOpen16': 5, 'WinAndRoofAndCurtPosnTyp_PercOpen20': 6, 'WinAndRoofAndCurtPosnTyp_PercOpen24': 7, 'WinAndRoofAndCurtPosnTyp_PercOpen28': 8, 'WinAndRoofAndCurtPosnTyp_PercOpen32': 9, 'WinAndRoofAndCurtPosnTyp_PercOpen36': 10, 'WinAndRoofAndCurtPosnTyp_PercOpen40': 11, 'WinAndRoofAndCurtPosnTyp_PercOpen44': 12, 'WinAndRoofAndCurtPosnTyp_PercOpen48': 13, 'WinAndRoofAndCurtPosnTyp_PercOpen52': 14, 'WinAndRoofAndCurtPosnTyp_PercOpen56': 15, 'WinAndRoofAndCurtPosnTyp_PercOpen60': 16, 'WinAndRoofAndCurtPosnTyp_PercOpen64': 17, 'WinAndRoofAndCurtPosnTyp_PercOpen68': 18, 'WinAndRoofAndCurtPosnTyp_PercOpen72': 19, 'WinAndRoofAndCurtPosnTyp_PercOpen76': 20, 'WinAndRoofAndCurtPosnTyp_PercOpen80': 21, 'WinAndRoofAndCurtPosnTyp_PercOpen84': 22, 'WinAndRoofAndCurtPosnTyp_PercOpen88': 23, 'WinAndRoofAndCurtPosnTyp_PercOpen92': 24, 'WinAndRoofAndCurtPosnTyp_PercOpen96': 25, 'WinAndRoofAndCurtPosnTyp_OpenFull': 26, 'WinAndRoofAndCurtPosnTyp_Resd1': 27, 'WinAndRoofAndCurtPosnTyp_Resd2': 28, 'WinAndRoofAndCurtPosnTyp_Resd3': 29, 'WinAndRoofAndCurtPosnTyp_Resd4': 30, 'WinAndRoofAndCurtPosnTyp_Movg': 31}
        compute_method = None
        length = 5
        startbit = 44
        byte = 5
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class ErsStrtRes:
        sig_name = "ErsStrtRes"
        sig_start_bit = 60
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 19
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ErsStrtRes_ErsStrtNotSet': 0, 'ErsStrtRes_ErsStrtSuccess': 1, 'ErsStrtRes_ErsStrtInhMaxNoStart': 2, 'ErsStrtRes_ErsStrtInhCarUnlocked': 3, 'ErsStrtRes_ErsStrtInhKeyInCar': 4, 'ErsStrtRes_ErsStrtInhDoorOpen': 5, 'ErsStrtRes_ErsStrtInhHoodOpen': 6, 'ErsStrtRes_ErsStrtInhGearNotP': 7, 'ErsStrtRes_ErsStrtInhUserInCar': 8, 'ErsStrtRes_ErsStrtInhPedalPressed': 9, 'ErsStrtRes_ErsStrtInhLoFuel': 10, 'ErsStrtRes_ErsStrtInhLoBatt': 11, 'ErsStrtRes_ErsStrtInhEngCoolant': 12, 'ErsStrtRes_ErsStrtInhEngFault': 13, 'ErsStrtRes_ErsStrtInhOther': 14, 'ErsStrtRes_ErsStrtAbrtEngFault': 15, 'ErsStrtRes_ErsStrtAbrtEngCoolant': 16, 'ErsStrtRes_ErsStrtAbrtLoFuel': 17, 'ErsStrtRes_ErsStrtAbrtLoBatt': 18, 'ErsStrtRes_ErsStrtAbrtOther': 19}
        compute_method = None
        length = 5
        startbit = 60
        byte = 7
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class VehModMngtGlbSafe1Chks:
        sig_name = "VehModMngtGlbSafe1Chks"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class VehModMngtGlbSafe1EgyLvlElecSubtyp:
        sig_name = "VehModMngtGlbSafe1EgyLvlElecSubtyp"
        sig_start_bit = 23
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class VehModMngtGlbSafe1PwrLvlElecMai:
        sig_name = "VehModMngtGlbSafe1PwrLvlElecMai"
        sig_start_bit = 19
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class VehModMngtGlbSafe1CarModSts1:
        sig_name = "VehModMngtGlbSafe1CarModSts1"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
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

    class AjarChrgLidRearSwitch:
        sig_name = "AjarChrgLidRearSwitch"
        sig_start_bit = 47
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorSts2_Ukwn': 0, 'DoorSts2_Opend': 1, 'DoorSts2_Clsd': 2}
        compute_method = None
        length = 2
        startbit = 47
        byte = 5
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class VgmConnFr03:
    msg_name = "VgmConnFr03"
    msg_id = 832
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.09
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class FragCh3UseUpWrn:
        sig_name = "FragCh3UseUpWrn"
        sig_start_bit = 32
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Warn2_NoWarn': 0, 'Warn2_Warn': 1}
        compute_method = None
        length = 1
        startbit = 32
        byte = 4
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FragCh5UseUpWrn:
        sig_name = "FragCh5UseUpWrn"
        sig_start_bit = 34
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Warn2_NoWarn': 0, 'Warn2_Warn': 1}
        compute_method = None
        length = 1
        startbit = 34
        byte = 4
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class IntPm25LvlFrmClima:
        sig_name = "IntPm25LvlFrmClima"
        sig_start_bit = 42
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CmpmtAirPmLvl_Level1': 0, 'CmpmtAirPmLvl_Level2': 1, 'CmpmtAirPmLvl_Level3': 2, 'CmpmtAirPmLvl_Level4': 3, 'CmpmtAirPmLvl_Level5': 4, 'CmpmtAirPmLvl_Level6': 5, 'CmpmtAirPmLvl_Reserved': 6, 'CmpmtAirPmLvl_Invalid': 7}
        compute_method = None
        length = 3
        startbit = 42
        byte = 5
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class FragLvlFrmClima:
        sig_name = "FragLvlFrmClima"
        sig_start_bit = 39
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'RatUse_NoRequest': 0, 'RatUse_Low': 1, 'RatUse_Mid': 2, 'RatUse_High': 3}
        compute_method = None
        length = 2
        startbit = 39
        byte = 4
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class FragCh1UseUpWrn:
        sig_name = "FragCh1UseUpWrn"
        sig_start_bit = 30
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Warn2_NoWarn': 0, 'Warn2_Warn': 1}
        compute_method = None
        length = 1
        startbit = 30
        byte = 3
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class FragStsFrmClima:
        sig_name = "FragStsFrmClima"
        sig_start_bit = 37
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 1
        sig_value_max = 3
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AirFragSts_OFF': 1, 'AirFragSts_ON': 2, 'AirFragSts_Error': 3}
        compute_method = None
        length = 2
        startbit = 37
        byte = 4
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class RemClimaActv:
        sig_name = "RemClimaActv"
        sig_start_bit = 53
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 53
        byte = 6
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class LockgCenStsForUsrFb:
        sig_name = "LockgCenStsForUsrFb"
        sig_start_bit = 10
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LockSt2_Undefd': 0, 'LockSt2_Opend': 1, 'LockSt2_Clsd': 2, 'LockSt2_Lockd': 3, 'LockSt2_Safe': 4}
        compute_method = None
        length = 3
        startbit = 10
        byte = 1
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class SteerWhlHeatgAvlSts:
        sig_name = "SteerWhlHeatgAvlSts"
        sig_start_bit = 18
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'StsFd_None': 0, 'StsFd_On': 1, 'StsFd_Off': 2, 'StsFd_Error': 3, 'StsFd_Functionallimit': 4, 'StsFd_Energylimit': 5, 'StsFd_Resvd1': 6, 'StsFd_Resvd2': 7}
        compute_method = None
        length = 3
        startbit = 18
        byte = 2
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class FragCh4UseUpWrn:
        sig_name = "FragCh4UseUpWrn"
        sig_start_bit = 33
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Warn2_NoWarn': 0, 'Warn2_Warn': 1}
        compute_method = None
        length = 1
        startbit = 33
        byte = 4
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class FragCh2UseUpWrn:
        sig_name = "FragCh2UseUpWrn"
        sig_start_bit = 31
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Warn2_NoWarn': 0, 'Warn2_Warn': 1}
        compute_method = None
        length = 1
        startbit = 31
        byte = 3
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ClimaActv:
        sig_name = "ClimaActv"
        sig_start_bit = 28
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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


class VgmConnFr21:
    msg_name = "VgmConnFr21"
    msg_id = 824
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class RemClimaWarn:
        sig_name = "RemClimaWarn"
        sig_start_bit = 19
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 8
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ClimaWarn_NoWarn': 0, 'ClimaWarn_FuLo': 1, 'ClimaWarn_BattLo': 2, 'ClimaWarn_FuAndBattLo': 3, 'ClimaWarn_TLo': 4, 'ClimaWarn_THi': 5, 'ClimaWarn_Error': 6, 'ClimaWarn_HVError': 7, 'ClimaWarn_ActvnLimd': 8}
        compute_method = None
        length = 4
        startbit = 19
        byte = 2
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class MobDevRPASts:
        sig_name = "MobDevRPASts"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class BodyRemoteCarFindFBStatus:
        sig_name = "BodyRemoteCarFindFBStatus"
        sig_start_bit = 63
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 11
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Default': 0, 'NetWakeFail': 1, 'RVIAuthFail': 2, 'CarmodeFail': 3, 'UsagemodeFail': 4, 'DelayFail': 5, 'CarConfigFail': 6, 'reserve1Fail': 7, 'reserve2Fail': 8, 'reserve3Fail': 9, 'Success': 10, 'reserve4': 11}
        compute_method = None
        length = 4
        startbit = 63
        byte = 7
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class RemStrtClimaRspn:
        sig_name = "RemStrtClimaRspn"
        sig_start_bit = 4
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class ClimaOvrHeatProRspn:
        sig_name = "ClimaOvrHeatProRspn"
        sig_start_bit = 3
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 3
        byte = 0
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class BodyRemoteCarFindFBReserveSignal1:
        sig_name = "BodyRemoteCarFindFBReserveSignal1"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class RemClimaDelaySts:
        sig_name = "RemClimaDelaySts"
        sig_start_bit = 31
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 31
        byte = 3
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class RemClimaExtnTiRspn:
        sig_name = "RemClimaExtnTiRspn"
        sig_start_bit = 21
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 21
        byte = 2
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class RemClimaHvRspn:
        sig_name = "RemClimaHvRspn"
        sig_start_bit = 39
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 39
        byte = 4
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ClimaOvrHeatProWarn:
        sig_name = "ClimaOvrHeatProWarn"
        sig_start_bit = 28
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ClimaOvrheatProWarnSts_NoWarn': 0, 'ClimaOvrheatProWarnSts_Err': 1, 'ClimaOvrheatProWarnSts_PwrLo': 2, 'ClimaOvrheatProWarnSts_Tout': 3}
        compute_method = None
        length = 2
        startbit = 28
        byte = 3
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3


class BgmToNkrConnectivityDiagReqFrame:
    msg_name = "BgmToNkrConnectivityDiagReqFrame"
    msg_id = 1829
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []


class BncmConnectivityFr07:
    msg_name = "BncmConnectivityFr07"
    msg_id = 358
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = None
    rx_nodes = ['BGM']

    class DigKeyBLEReq:
        sig_name = "DigKeyBLEReq"
        sig_start_bit = 0
        sig_length = 512
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = None
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 512
        startbit = 0
        bmuws_info = [(0, 0b00000001, 0b11111110, 1, 0), (1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111111, 0b00000000, 8, 0), (8, 0b11111111, 0b00000000, 8, 0), (9, 0b11111111, 0b00000000, 8, 0), (10, 0b11111111, 0b00000000, 8, 0), (11, 0b11111111, 0b00000000, 8, 0), (12, 0b11111111, 0b00000000, 8, 0), (13, 0b11111111, 0b00000000, 8, 0), (14, 0b11111111, 0b00000000, 8, 0), (15, 0b11111111, 0b00000000, 8, 0), (16, 0b11111111, 0b00000000, 8, 0), (17, 0b11111111, 0b00000000, 8, 0), (18, 0b11111111, 0b00000000, 8, 0), (19, 0b11111111, 0b00000000, 8, 0), (20, 0b11111111, 0b00000000, 8, 0), (21, 0b11111111, 0b00000000, 8, 0), (22, 0b11111111, 0b00000000, 8, 0), (23, 0b11111111, 0b00000000, 8, 0), (24, 0b11111111, 0b00000000, 8, 0), (25, 0b11111111, 0b00000000, 8, 0), (26, 0b11111111, 0b00000000, 8, 0), (27, 0b11111111, 0b00000000, 8, 0), (28, 0b11111111, 0b00000000, 8, 0), (29, 0b11111111, 0b00000000, 8, 0), (30, 0b11111111, 0b00000000, 8, 0), (31, 0b11111111, 0b00000000, 8, 0), (32, 0b11111111, 0b00000000, 8, 0), (33, 0b11111111, 0b00000000, 8, 0), (34, 0b11111111, 0b00000000, 8, 0), (35, 0b11111111, 0b00000000, 8, 0), (36, 0b11111111, 0b00000000, 8, 0), (37, 0b11111111, 0b00000000, 8, 0), (38, 0b11111111, 0b00000000, 8, 0), (39, 0b11111111, 0b00000000, 8, 0), (40, 0b11111111, 0b00000000, 8, 0), (41, 0b11111111, 0b00000000, 8, 0), (42, 0b11111111, 0b00000000, 8, 0), (43, 0b11111111, 0b00000000, 8, 0), (44, 0b11111111, 0b00000000, 8, 0), (45, 0b11111111, 0b00000000, 8, 0), (46, 0b11111111, 0b00000000, 8, 0), (47, 0b11111111, 0b00000000, 8, 0), (48, 0b11111111, 0b00000000, 8, 0), (49, 0b11111111, 0b00000000, 8, 0), (50, 0b11111111, 0b00000000, 8, 0), (51, 0b11111111, 0b00000000, 8, 0), (52, 0b11111111, 0b00000000, 8, 0), (53, 0b11111111, 0b00000000, 8, 0), (54, 0b11111111, 0b00000000, 8, 0), (55, 0b11111111, 0b00000000, 8, 0), (56, 0b11111111, 0b00000000, 8, 0), (57, 0b11111111, 0b00000000, 8, 0), (58, 0b11111111, 0b00000000, 8, 0), (59, 0b11111111, 0b00000000, 8, 0), (60, 0b11111111, 0b00000000, 8, 0), (61, 0b11111111, 0b00000000, 8, 0), (62, 0b11111111, 0b00000000, 8, 0), (63, 0b11111111, 0b00000000, 8, 0), (64, 0b11111110, 0b00000001, 7, 1)]


class NkrToBgmConnectivityDiagRespFrame:
    msg_name = "NkrToBgmConnectivityDiagRespFrame"
    msg_id = 1573
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']


class TcamConnectivityFr01:
    msg_name = "TcamConnectivityFr01"
    msg_id = 357
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class ImobVehRemReqAndRespImobVehDataRemReq4:
        sig_name = "ImobVehRemReqAndRespImobVehDataRemReq4"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class ImobVehRemReqAndRespImobVehDataRemReq2:
        sig_name = "ImobVehRemReqAndRespImobVehDataRemReq2"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class ImobVehRemReqAndRespImobVehRemReqCmd:
        sig_name = "ImobVehRemReqAndRespImobVehRemReqCmd"
        sig_start_bit = 2
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ImobVehRemReqCmd_ImobRemReqIdle': 0, 'ImobVehRemReqCmd_NoImobnRemReq': 1, 'ImobVehRemReqCmd_ImobnRemReq': 2, 'ImobVehRemReqCmd_SpdLimRemReq': 3, 'ImobVehRemReqCmd_ImobRemChkReq': 4, 'ImobVehRemReqCmd_ImobRemStsReq': 5}
        compute_method = None
        length = 3
        startbit = 2
        byte = 0
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class ImobVehRemReqAndRespImobVehDataRemReq1:
        sig_name = "ImobVehRemReqAndRespImobVehDataRemReq1"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class ImobVehRemReqAndRespImobVehDataRemReq0:
        sig_name = "ImobVehRemReqAndRespImobVehDataRemReq0"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class ImobVehRemReqAndRespImobVehDataRemReq3:
        sig_name = "ImobVehRemReqAndRespImobVehDataRemReq3"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class ImobVehRemReqAndRespImobVehRemTmrOrSpdLim:
        sig_name = "ImobVehRemReqAndRespImobVehRemTmrOrSpdLim"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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


class TcamConnectivityFr33:
    msg_name = "TcamConnectivityFr33"
    msg_id = 383
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 16
    tx_node = None
    rx_nodes = ['BGM']

    class RVIResponseFromTelmByte2:
        sig_name = "RVIResponseFromTelmByte2"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class RVIResponseFromTelmByte0:
        sig_name = "RVIResponseFromTelmByte0"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class RVIResponseFromTelmByte5:
        sig_name = "RVIResponseFromTelmByte5"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class RVIResponseFromTelmByte12:
        sig_name = "RVIResponseFromTelmByte12"
        sig_start_bit = 103
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class RVIResponseFromTelmByte10:
        sig_name = "RVIResponseFromTelmByte10"
        sig_start_bit = 87
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class RVIResponseFromTelmByte6:
        sig_name = "RVIResponseFromTelmByte6"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class RVIResponseFromTelmByte1:
        sig_name = "RVIResponseFromTelmByte1"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class RVIResponseFromTelmByte3:
        sig_name = "RVIResponseFromTelmByte3"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class RVIResponseFromTelmByte4:
        sig_name = "RVIResponseFromTelmByte4"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class RVIResponseFromTelmByte13:
        sig_name = "RVIResponseFromTelmByte13"
        sig_start_bit = 111
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class RVIResponseFromTelmByte7:
        sig_name = "RVIResponseFromTelmByte7"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class RVIResponseFromTelmByte11:
        sig_name = "RVIResponseFromTelmByte11"
        sig_start_bit = 95
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class RVIResponseFromTelmByte8:
        sig_name = "RVIResponseFromTelmByte8"
        sig_start_bit = 71
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class RVIResponseFromTelmByte14:
        sig_name = "RVIResponseFromTelmByte14"
        sig_start_bit = 119
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class RVIResponseFromTelmByte9:
        sig_name = "RVIResponseFromTelmByte9"
        sig_start_bit = 79
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class RVIResponseFromTelmByte15:
        sig_name = "RVIResponseFromTelmByte15"
        sig_start_bit = 127
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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


class BgmToAllConnectivityDiagReqFrame:
    msg_name = "BgmToAllConnectivityDiagReqFrame"
    msg_id = 2047
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []


class BgmConnectivityFr11:
    msg_name = "BgmConnectivityFr11"
    msg_id = 384
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 16
    tx_node = "BGM"
    rx_nodes = []

    class RVIChallengeFromBodyByte10:
        sig_name = "RVIChallengeFromBodyByte10"
        sig_start_bit = 87
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class RVIChallengeFromBodyByte4:
        sig_name = "RVIChallengeFromBodyByte4"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class RVIChallengeFromBodyByte7:
        sig_name = "RVIChallengeFromBodyByte7"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class RVIChallengeFromBodyByte9:
        sig_name = "RVIChallengeFromBodyByte9"
        sig_start_bit = 79
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class RVIChallengeFromBodyByte2:
        sig_name = "RVIChallengeFromBodyByte2"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class RVIChallengeFromBodyByte8:
        sig_name = "RVIChallengeFromBodyByte8"
        sig_start_bit = 71
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class RVIChallengeFromBodyByte12:
        sig_name = "RVIChallengeFromBodyByte12"
        sig_start_bit = 103
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class RVIChallengeFromBodyByte3:
        sig_name = "RVIChallengeFromBodyByte3"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class RVIChallengeFromBodyByte15:
        sig_name = "RVIChallengeFromBodyByte15"
        sig_start_bit = 127
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class RVIChallengeFromBodyByte0:
        sig_name = "RVIChallengeFromBodyByte0"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class RVIChallengeFromBodyByte5:
        sig_name = "RVIChallengeFromBodyByte5"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class RVIChallengeFromBodyByte6:
        sig_name = "RVIChallengeFromBodyByte6"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class RVIChallengeFromBodyByte13:
        sig_name = "RVIChallengeFromBodyByte13"
        sig_start_bit = 111
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class RVIChallengeFromBodyByte14:
        sig_name = "RVIChallengeFromBodyByte14"
        sig_start_bit = 119
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class RVIChallengeFromBodyByte11:
        sig_name = "RVIChallengeFromBodyByte11"
        sig_start_bit = 95
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class RVIChallengeFromBodyByte1:
        sig_name = "RVIChallengeFromBodyByte1"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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


class BgmConnectivityFr09:
    msg_name = "BgmConnectivityFr09"
    msg_id = 533
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.09
    msg_length = 16
    tx_node = "BGM"
    rx_nodes = []

    class AVPAccountInfoByte6:
        sig_name = "AVPAccountInfoByte6"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class AVPAccountInfoByte12:
        sig_name = "AVPAccountInfoByte12"
        sig_start_bit = 103
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class AVPAccountInfoByte8:
        sig_name = "AVPAccountInfoByte8"
        sig_start_bit = 71
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class AVPAccountInfoByte14:
        sig_name = "AVPAccountInfoByte14"
        sig_start_bit = 119
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class AVPAccountInfoByte2:
        sig_name = "AVPAccountInfoByte2"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class AVPAccountInfoByte9:
        sig_name = "AVPAccountInfoByte9"
        sig_start_bit = 79
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class AVPAccountInfoByte7:
        sig_name = "AVPAccountInfoByte7"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class AVPAccountInfoByte13:
        sig_name = "AVPAccountInfoByte13"
        sig_start_bit = 111
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class AVPAccountInfoByte15:
        sig_name = "AVPAccountInfoByte15"
        sig_start_bit = 127
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class AVPAccountInfoByte11:
        sig_name = "AVPAccountInfoByte11"
        sig_start_bit = 95
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class AVPAccountInfoByte4:
        sig_name = "AVPAccountInfoByte4"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class AVPAccountInfoByte1:
        sig_name = "AVPAccountInfoByte1"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class AVPAccountInfoByte0:
        sig_name = "AVPAccountInfoByte0"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class AVPAccountInfoByte10:
        sig_name = "AVPAccountInfoByte10"
        sig_start_bit = 87
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class AVPAccountInfoByte3:
        sig_name = "AVPAccountInfoByte3"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class AVPAccountInfoByte5:
        sig_name = "AVPAccountInfoByte5"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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


class BgmConnectivityFr02:
    msg_name = "BgmConnectivityFr02"
    msg_id = 371
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DigKeyGidInfo2Byte3:
        sig_name = "DigKeyGidInfo2Byte3"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 32
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyGidInfo2Byte4:
        sig_name = "DigKeyGidInfo2Byte4"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 32
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyGidInfo2Byte5:
        sig_name = "DigKeyGidInfo2Byte5"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 32
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyGidInfo2Byte7:
        sig_name = "DigKeyGidInfo2Byte7"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 32
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyGidInfo2Byte2:
        sig_name = "DigKeyGidInfo2Byte2"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 32
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 23
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyGidInfo2Byte0:
        sig_name = "DigKeyGidInfo2Byte0"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 32
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyGidInfo2Byte1:
        sig_name = "DigKeyGidInfo2Byte1"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 32
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyGidInfo2Byte6:
        sig_name = "DigKeyGidInfo2Byte6"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 32
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class VgmConnFr09:
    msg_name = "VgmConnFr09"
    msg_id = 1056
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.085
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class SunRoofPosnSts:
        sig_name = "SunRoofPosnSts"
        sig_start_bit = 20
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 31
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WinAndRoofAndCurtPosnTyp_PosnUkwn': 0, 'WinAndRoofAndCurtPosnTyp_ClsFull': 1, 'WinAndRoofAndCurtPosnTyp_PercOpen4': 2, 'WinAndRoofAndCurtPosnTyp_PercOpen8': 3, 'WinAndRoofAndCurtPosnTyp_PercOpen12': 4, 'WinAndRoofAndCurtPosnTyp_PercOpen16': 5, 'WinAndRoofAndCurtPosnTyp_PercOpen20': 6, 'WinAndRoofAndCurtPosnTyp_PercOpen24': 7, 'WinAndRoofAndCurtPosnTyp_PercOpen28': 8, 'WinAndRoofAndCurtPosnTyp_PercOpen32': 9, 'WinAndRoofAndCurtPosnTyp_PercOpen36': 10, 'WinAndRoofAndCurtPosnTyp_PercOpen40': 11, 'WinAndRoofAndCurtPosnTyp_PercOpen44': 12, 'WinAndRoofAndCurtPosnTyp_PercOpen48': 13, 'WinAndRoofAndCurtPosnTyp_PercOpen52': 14, 'WinAndRoofAndCurtPosnTyp_PercOpen56': 15, 'WinAndRoofAndCurtPosnTyp_PercOpen60': 16, 'WinAndRoofAndCurtPosnTyp_PercOpen64': 17, 'WinAndRoofAndCurtPosnTyp_PercOpen68': 18, 'WinAndRoofAndCurtPosnTyp_PercOpen72': 19, 'WinAndRoofAndCurtPosnTyp_PercOpen76': 20, 'WinAndRoofAndCurtPosnTyp_PercOpen80': 21, 'WinAndRoofAndCurtPosnTyp_PercOpen84': 22, 'WinAndRoofAndCurtPosnTyp_PercOpen88': 23, 'WinAndRoofAndCurtPosnTyp_PercOpen92': 24, 'WinAndRoofAndCurtPosnTyp_PercOpen96': 25, 'WinAndRoofAndCurtPosnTyp_OpenFull': 26, 'WinAndRoofAndCurtPosnTyp_Resd1': 27, 'WinAndRoofAndCurtPosnTyp_Resd2': 28, 'WinAndRoofAndCurtPosnTyp_Resd3': 29, 'WinAndRoofAndCurtPosnTyp_Resd4': 30, 'WinAndRoofAndCurtPosnTyp_Movg': 31}
        compute_method = None
        length = 5
        startbit = 20
        byte = 2
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class PasAcsHmiPen:
        sig_name = "PasAcsHmiPen"
        sig_start_bit = 53
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'IdPen_ProfUkwn': 0, 'IdPen_Prof1': 1, 'IdPen_Prof2': 2, 'IdPen_Prof3': 3, 'IdPen_Prof4': 4, 'IdPen_Prof5': 5, 'IdPen_Prof6': 6, 'IdPen_Prof7': 7, 'IdPen_Prof8': 8, 'IdPen_Prof9': 9, 'IdPen_Prof10': 10, 'IdPen_Prof11': 11, 'IdPen_Prof12': 12, 'IdPen_Prof13': 13, 'IdPen_Resd14': 14, 'IdPen_ProfAll': 15}
        compute_method = None
        length = 4
        startbit = 53
        byte = 6
        mask = 0b00111100
        unmask = 0b11000011
        shift = 2

    class BleCtrlRPABtnStsLftTurn:
        sig_name = "BleCtrlRPABtnStsLftTurn"
        sig_start_bit = 5
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ActvnAvl4_Idle': 0, 'ActvnAvl4_Actvn': 1, 'ActvnAvl4_Deactvn': 2, 'ActvnAvl4_Recommand': 3}
        compute_method = None
        length = 2
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class ApproachLiSetReq:
        sig_name = "ApproachLiSetReq"
        sig_start_bit = 22
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ApproachLiSetReq_Off': 0, 'ApproachLiSetReq_ONStatic': 1, 'ApproachLiSetReq_ONDynamic': 2}
        compute_method = None
        length = 2
        startbit = 22
        byte = 2
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class AutoOpenSwtHmiReq:
        sig_name = "AutoOpenSwtHmiReq"
        sig_start_bit = 40
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class BleCtrlRPABtnStsFrnt:
        sig_name = "BleCtrlRPABtnStsFrnt"
        sig_start_bit = 7
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ActvnAvl4_Idle': 0, 'ActvnAvl4_Actvn': 1, 'ActvnAvl4_Deactvn': 2, 'ActvnAvl4_Recommand': 3}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class BleCtrlRPABtnStsRear:
        sig_name = "BleCtrlRPABtnStsRear"
        sig_start_bit = 3
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ActvnAvl4_Idle': 0, 'ActvnAvl4_Actvn': 1, 'ActvnAvl4_Deactvn': 2, 'ActvnAvl4_Recommand': 3}
        compute_method = None
        length = 2
        startbit = 3
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class BleCtrlRPABtnStsRgtTurn:
        sig_name = "BleCtrlRPABtnStsRgtTurn"
        sig_start_bit = 1
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ActvnAvl4_Idle': 0, 'ActvnAvl4_Actvn': 1, 'ActvnAvl4_Deactvn': 2, 'ActvnAvl4_Recommand': 3}
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class TrOpenerSts:
        sig_name = "TrOpenerSts"
        sig_start_bit = 35
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 10
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TrOpenerSts1_Ukwn': 0, 'TrOpenerSts1_FullClsd': 1, 'TrOpenerSts1_MovgUp': 2, 'TrOpenerSts1_MovgUpBrkg': 3, 'TrOpenerSts1_StopDurgOpen': 4, 'TrOpenerSts1_FullOpend': 5, 'TrOpenerSts1_MovgDwn': 6, 'TrOpenerSts1_MovgDwnBrkg': 7, 'TrOpenerSts1_StopDurgCls': 8, 'TrOpenerSts1_HalfClsd': 9, 'TrOpenerSts1_StopMinPntForCls': 10}
        compute_method = None
        length = 4
        startbit = 35
        byte = 4
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class PasAcsHmiSts:
        sig_name = "PasAcsHmiSts"
        sig_start_bit = 54
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 54
        byte = 6
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6


class VgmConnFr31:
    msg_name = "VgmConnFr31"
    msg_id = 61
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DriftModStsDriftModActSts:
        sig_name = "DriftModStsDriftModActSts"
        sig_start_bit = 23
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 23
        byte = 2
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class DriftModStsDriftModDendReason:
        sig_name = "DriftModStsDriftModDendReason"
        sig_start_bit = 7
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class DriftModStsDriftModDeactive:
        sig_name = "DriftModStsDriftModDeactive"
        sig_start_bit = 22
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 22
        byte = 2
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class DriftModStsDriftModEnaSts:
        sig_name = "DriftModStsDriftModEnaSts"
        sig_start_bit = 21
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EnaSts_ActvDi': 0, 'EnaSts_ActvEna': 1, 'EnaSts_OffDi': 2, 'EnaSts_OffEna': 3}
        compute_method = None
        length = 2
        startbit = 21
        byte = 2
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4


class WpcToBgmConnectivityDiagRespFrame:
    msg_name = "WpcToBgmConnectivityDiagRespFrame"
    msg_id = 1572
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']


class VgmConnFr13:
    msg_name = "VgmConnFr13"
    msg_id = 1152
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.225
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class VehSpdIndcdVeSpdIndcdUnit:
        sig_name = "VehSpdIndcdVeSpdIndcdUnit"
        sig_start_bit = 50
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VehSpdIndcdUnit_Kmph': 0, 'VehSpdIndcdUnit_Mph': 1, 'VehSpdIndcdUnit_UkwnUnit': 2}
        compute_method = None
        length = 2
        startbit = 50
        byte = 6
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class VehSpdIndcdVehSpdIndcd:
        sig_name = "VehSpdIndcdVehSpdIndcd"
        sig_start_bit = 48
        sig_length = 9
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 48
        bmuws_info = [(6, 0b00000001, 0b11111110, 1, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class CmptmtTFrntQf:
        sig_name = "CmptmtTFrntQf"
        sig_start_bit = 37
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CmptmtTFrntQf_SnsrDataUndefd': 0, 'CmptmtTFrntQf_FanNotRunning': 1, 'CmptmtTFrntQf_SnsrDataNotOk': 2, 'CmptmtTFrntQf_SnsrDataOk': 3}
        compute_method = None
        length = 2
        startbit = 37
        byte = 4
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class CmptmtTFrntCmptmtTFrnt:
        sig_name = "CmptmtTFrntCmptmtTFrnt"
        sig_start_bit = 34
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = "-60.0"
        sig_value_min = 0
        sig_value_max = 1850
        sig_value_init = 600
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 34
        bmuws_info = [(4, 0b00000111, 0b11111000, 3, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class BkpOfDstTrvld:
        sig_name = "BkpOfDstTrvld"
        sig_start_bit = 7
        sig_length = 21
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 2000000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 21
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111000, 0b00000111, 5, 3)]

    class VehBattUSysUQf:
        sig_name = "VehBattUSysUQf"
        sig_start_bit = 17
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 17
        byte = 2
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class CmptmtTFrntFanForCmptmtTRunng:
        sig_name = "CmptmtTFrntFanForCmptmtTRunng"
        sig_start_bit = 35
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flg1_Rst': 0, 'Flg1_Set': 1}
        compute_method = None
        length = 1
        startbit = 35
        byte = 4
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VehBattUSysU:
        sig_name = "VehBattUSysU"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 250
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


class BgmConnectivityFr03:
    msg_name = "BgmConnectivityFr03"
    msg_id = 372
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.09
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DstEstimdToEmptyForDrvgElec:
        sig_name = "DstEstimdToEmptyForDrvgElec"
        sig_start_bit = 36
        sig_length = 10
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 36
        bmuws_info = [(4, 0b00011111, 0b11100000, 5, 0), (5, 0b11111000, 0b00000111, 5, 3)]

    class BookChargeSetResponse:
        sig_name = "BookChargeSetResponse"
        sig_start_bit = 42
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BookChargeSetResponse_Default': 0, 'BookChargeSetResponse_Success': 1, 'BookChargeSetResponse_Cancelled': 2, 'BookChargeSetResponse_Fail': 3}
        compute_method = None
        length = 2
        startbit = 42
        byte = 5
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class HvBattChrgnTiEstimd:
        sig_name = "HvBattChrgnTiEstimd"
        sig_start_bit = 14
        sig_length = 11
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 2047
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 14
        bmuws_info = [(1, 0b01111111, 0b10000000, 7, 0), (2, 0b11110000, 0b00001111, 4, 4)]

    class ChrgnSpd:
        sig_name = "ChrgnSpd"
        sig_start_bit = 31
        sig_length = 11
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11100000, 0b00011111, 3, 5)]


class VgmConnFr12:
    msg_name = "VgmConnFr12"
    msg_id = 1136
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class GearLvrIndcn:
        sig_name = "GearLvrIndcn"
        sig_start_bit = 63
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_value_init = 7
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GearLvrIndcn2_ParkIndcn': 0, 'GearLvrIndcn2_RvsIndcn': 1, 'GearLvrIndcn2_NeutIndcn': 2, 'GearLvrIndcn2_DrvIndcn': 3, 'GearLvrIndcn2_ManModeIndcn': 4, 'GearLvrIndcn2_Resd1': 5, 'GearLvrIndcn2_Resd2': 6, 'GearLvrIndcn2_Undefd': 7}
        compute_method = None
        length = 3
        startbit = 63
        byte = 7
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class LockgCenStsLockSt:
        sig_name = "LockgCenStsLockSt"
        sig_start_bit = 42
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LockSt3_LockUndefd': 0, 'LockSt3_LockUnlckd': 1, 'LockSt3_LockTrUnlckd': 2, 'LockSt3_LockLockd': 3}
        compute_method = None
        length = 2
        startbit = 42
        byte = 5
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class BookChrgnStsFb:
        sig_name = "BookChrgnStsFb"
        sig_start_bit = 57
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BookChrgnStsFb_Default': 0, 'BookChrgnStsFb_Success': 1, 'BookChrgnStsFb_Fail': 2, 'BookChrgnStsFb_Finished': 3}
        compute_method = None
        length = 2
        startbit = 57
        byte = 7
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class RemClimaHvSts:
        sig_name = "RemClimaHvSts"
        sig_start_bit = 54
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 54
        byte = 6
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class LockgCenStsUpdEve:
        sig_name = "LockgCenStsUpdEve"
        sig_start_bit = 40
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class OnBdChrgrRdyTi:
        sig_name = "OnBdChrgrRdyTi"
        sig_start_bit = 38
        sig_length = 7
        sig_value_factor = 100
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 127
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 38
        byte = 4
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class LockgCenStsTrigSrc:
        sig_name = "LockgCenStsTrigSrc"
        sig_start_bit = 46
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 11
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LockTrigSrc2_NoTrigSrc': 0, 'LockTrigSrc2_KeyRem': 1, 'LockTrigSrc2_Keyls': 2, 'LockTrigSrc2_IntrSwt': 3, 'LockTrigSrc2_SpdAut': 4, 'LockTrigSrc2_TmrAut': 5, 'LockTrigSrc2_Slam': 6, 'LockTrigSrc2_Telm': 7, 'LockTrigSrc2_Crash': 8, 'LockTrigSrc2_Apprch': 9, 'LockTrigSrc2_OutsOth': 10, 'LockTrigSrc2_InsOth': 11}
        compute_method = None
        length = 4
        startbit = 46
        byte = 5
        mask = 0b01111000
        unmask = 0b10000111
        shift = 3

    class CarTiGlb:
        sig_name = "CarTiGlb"
        sig_start_bit = 7
        sig_length = 32
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 4294967295
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 32
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0)]


class BncmBsrmConnectivityFr04:
    msg_name = "BncmBsrmConnectivityFr04"
    msg_id = 325
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class RPAAuthReqDKDataByte6:
        sig_name = "RPAAuthReqDKDataByte6"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class RPAAuthReqHeader:
        sig_name = "RPAAuthReqHeader"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class RPAAuthReqDKDataByte2:
        sig_name = "RPAAuthReqDKDataByte2"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class RPAAuthReqDKDataByte1:
        sig_name = "RPAAuthReqDKDataByte1"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class RPAAuthReqDKDataByte3:
        sig_name = "RPAAuthReqDKDataByte3"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class RPAAuthReqDKDataByte4:
        sig_name = "RPAAuthReqDKDataByte4"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class RPAAuthReqDKDataByte5:
        sig_name = "RPAAuthReqDKDataByte5"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class RPAAuthReqAcknowledgment:
        sig_name = "RPAAuthReqAcknowledgment"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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


class BgmToWpcConnectivityDiagReqFrame:
    msg_name = "BgmToWpcConnectivityDiagReqFrame"
    msg_id = 1828
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []


class BgmConnectivityFr06:
    msg_name = "BgmConnectivityFr06"
    msg_id = 405
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 32
    tx_node = "BGM"
    rx_nodes = []

    class HavpModBtnSts2:
        sig_name = "HavpModBtnSts2"
        sig_start_bit = 87
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 2
        startbit = 87
        byte = 10
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HavpModBtnSts4:
        sig_name = "HavpModBtnSts4"
        sig_start_bit = 83
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 2
        startbit = 83
        byte = 10
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class HavpSts:
        sig_name = "HavpSts"
        sig_start_bit = 79
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Off': 0, 'Enable': 1, 'Standby': 2, 'Learningpath': 3, 'Active': 4, 'Pausing': 5, 'Completed': 6, 'Disabled': 7, 'Terminated': 8, 'Failure': 9, 'Reserve1': 10, 'Reserve2': 11, 'Reserve3': 12, 'Reserve4': 13, 'Reserve5': 14, 'Reserve6': 15}
        compute_method = None
        length = 4
        startbit = 79
        byte = 9
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class HavpModBtnSts3:
        sig_name = "HavpModBtnSts3"
        sig_start_bit = 85
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 2
        startbit = 85
        byte = 10
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class TotDstTrvld:
        sig_name = "TotDstTrvld"
        sig_start_bit = 114
        sig_length = 25
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 20000000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 25
        startbit = 114
        bmuws_info = [(14, 0b00000111, 0b11111000, 3, 0), (15, 0b11111111, 0b00000000, 8, 0), (16, 0b11111111, 0b00000000, 8, 0), (17, 0b11111100, 0b00000011, 6, 2)]

    class HvBattSoc:
        sig_name = "HvBattSoc"
        sig_start_bit = 103
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 2000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 103
        bmuws_info = [(12, 0b11111111, 0b00000000, 8, 0), (13, 0b11100000, 0b00011111, 3, 5)]

    class RemCntDwn:
        sig_name = "RemCntDwn"
        sig_start_bit = 108
        sig_length = 10
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 108
        bmuws_info = [(13, 0b00011111, 0b11100000, 5, 0), (14, 0b11111000, 0b00000111, 5, 3)]

    class SteerWhlSnsrQf:
        sig_name = "SteerWhlSnsrQf"
        sig_start_bit = 163
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 163
        byte = 20
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class ElecChromRoofFb:
        sig_name = "ElecChromRoofFb"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class SteerWhlSnsrCntr:
        sig_name = "SteerWhlSnsrCntr"
        sig_start_bit = 167
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 167
        byte = 20
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class HavpSysStsDisp:
        sig_name = "HavpSysStsDisp"
        sig_start_bit = 71
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class SteerWhlSnsrAgSpd:
        sig_name = "SteerWhlSnsrAgSpd"
        sig_start_bit = 178
        sig_length = 14
        sig_value_factor = 0.0078125
        sig_value_offset = 0.0
        sig_value_min = -6400
        sig_value_max = 6400
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 14
        startbit = 178
        bmuws_info = [(22, 0b00000111, 0b11111000, 3, 0), (23, 0b11111111, 0b00000000, 8, 0), (24, 0b11100000, 0b00011111, 3, 5)]

    class DCChrgnHndlSts:
        sig_name = "DCChrgnHndlSts"
        sig_start_bit = 42
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnBdChrgrHndlSts_Disconnected': 0, 'OnBdChrgrHndlSts_ConnectedWithoutPower': 1, 'OnBdChrgrHndlSts_PowerAvailableButNotActivated': 2, 'OnBdChrgrHndlSts_ConnectedWithPower': 3, 'OnBdChrgrHndlSts_Init': 4, 'OnBdChrgrHndlSts_Fault': 5}
        compute_method = None
        length = 3
        startbit = 42
        byte = 5
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class HavpBleFctSts:
        sig_name = "HavpBleFctSts"
        sig_start_bit = 75
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Reserve1': 0, 'Havpbluetooth_Unavailable': 1, 'Havpbluetooth_Available': 2, 'Reserve2': 3}
        compute_method = None
        length = 2
        startbit = 75
        byte = 9
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class SteerWhlSnsrAg:
        sig_name = "SteerWhlSnsrAg"
        sig_start_bit = 161
        sig_length = 15
        sig_value_factor = "9.765625E-4"
        sig_value_offset = 0.0
        sig_value_min = -14848
        sig_value_max = 14848
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 161
        bmuws_info = [(20, 0b00000011, 0b11111100, 2, 0), (21, 0b11111111, 0b00000000, 8, 0), (22, 0b11111000, 0b00000111, 5, 3)]

    class HavpModBtnSts1:
        sig_name = "HavpModBtnSts1"
        sig_start_bit = 73
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 2
        startbit = 73
        byte = 9
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class HavpReminder:
        sig_name = "HavpReminder"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class RPASysDisp:
        sig_name = "RPASysDisp"
        sig_start_bit = 151
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class SteerWhlSnsrChks:
        sig_name = "SteerWhlSnsrChks"
        sig_start_bit = 159
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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


class VgmConnFr04:
    msg_name = "VgmConnFr04"
    msg_id = 768
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class IntPm25VluFrmClima:
        sig_name = "IntPm25VluFrmClima"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class HoodSts:
        sig_name = "HoodSts"
        sig_start_bit = 47
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorSts2_Ukwn': 0, 'DoorSts2_Opend': 1, 'DoorSts2_Clsd': 2}
        compute_method = None
        length = 2
        startbit = 47
        byte = 5
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class VgmConnFr26:
    msg_name = "VgmConnFr26"
    msg_id = 1088
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DigKeyForNfcGidInfo1Byte5:
        sig_name = "DigKeyForNfcGidInfo1Byte5"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 32
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyForNfcGidInfo1Byte4:
        sig_name = "DigKeyForNfcGidInfo1Byte4"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 32
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyForNfcGidInfo1Byte7:
        sig_name = "DigKeyForNfcGidInfo1Byte7"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 32
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyForNfcGidInfo1Byte2:
        sig_name = "DigKeyForNfcGidInfo1Byte2"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 32
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 23
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyForNfcGidInfo1Byte3:
        sig_name = "DigKeyForNfcGidInfo1Byte3"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 32
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyForNfcGidInfo1Byte0:
        sig_name = "DigKeyForNfcGidInfo1Byte0"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 32
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyForNfcGidInfo1Byte6:
        sig_name = "DigKeyForNfcGidInfo1Byte6"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 32
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyForNfcGidInfo1Byte1:
        sig_name = "DigKeyForNfcGidInfo1Byte1"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 32
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class VgmConnFr51:
    msg_name = "VgmConnFr51"
    msg_id = 597
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.25
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class HmiStrangerModMenuSetActvInActv:
        sig_name = "HmiStrangerModMenuSetActvInActv"
        sig_start_bit = 50
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inact_Inactive': 0, 'Inact_Active': 1}
        compute_method = None
        length = 1
        startbit = 50
        byte = 6
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class HmiStrangerModMenuSetPasswordSt:
        sig_name = "HmiStrangerModMenuSetPasswordSt"
        sig_start_bit = 49
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 49
        byte = 6
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class HmiStrangerModMenuSetPrivateLockSt:
        sig_name = "HmiStrangerModMenuSetPrivateLockSt"
        sig_start_bit = 48
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class HmiStrangerModMenuSetSpdLim:
        sig_name = "HmiStrangerModMenuSetSpdLim"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class RemClimaDefrstSts:
        sig_name = "RemClimaDefrstSts"
        sig_start_bit = 30
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 30
        byte = 3
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6


class VgmConnFr10:
    msg_name = "VgmConnFr10"
    msg_id = 592
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class ErsDelayTiCfm:
        sig_name = "ErsDelayTiCfm"
        sig_start_bit = 6
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class ImobRemMgrChkImobDataRemMgrChk4:
        sig_name = "ImobRemMgrChkImobDataRemMgrChk4"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class ImobRemMgrChkSts:
        sig_name = "ImobRemMgrChkSts"
        sig_start_bit = 1
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AvlSts1_TmpNotAvl': 0, 'AvlSts1_PrmntNotAvl': 1, 'AvlSts1_Avl': 2}
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class ImobRemMgrChkImobDataRemMgrChk0:
        sig_name = "ImobRemMgrChkImobDataRemMgrChk0"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class ImobRemMgrChkImobDataRemMgrChk1:
        sig_name = "ImobRemMgrChkImobDataRemMgrChk1"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class ImobRemMgrChkImobDataRemMgrChk2:
        sig_name = "ImobRemMgrChkImobDataRemMgrChk2"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class ImobVehRemMgrSts1ImobVehRemMgrSts:
        sig_name = "ImobVehRemMgrSts1ImobVehRemMgrSts"
        sig_start_bit = 49
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ImobVehRemMgrSts_IdleRemMgrSts': 0, 'ImobVehRemMgrSts_ImobnRemMgrSts': 1, 'ImobVehRemMgrSts_NoImobnRemMgrSts': 2, 'ImobVehRemMgrSts_ImobnStrtDiRemMgrSts': 3}
        compute_method = None
        length = 2
        startbit = 49
        byte = 6
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class ImobVehRemMgrSts1SpdLimRemMgrSts:
        sig_name = "ImobVehRemMgrSts1SpdLimRemMgrSts"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class ClimaOvrHeatProActv:
        sig_name = "ClimaOvrHeatProActv"
        sig_start_bit = 55
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class ImobRemMgrChkImobDataRemMgrChk3:
        sig_name = "ImobRemMgrChkImobDataRemMgrChk3"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class ErsStrtApplSts:
        sig_name = "ErsStrtApplSts"
        sig_start_bit = 4
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ErsStrtApplSts_ErsStsOff': 0, 'ErsStrtApplSts_ErsStsStrtg': 1, 'ErsStrtApplSts_ErsStsRunng': 2}
        compute_method = None
        length = 2
        startbit = 4
        byte = 0
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3


class VgmConnFr05:
    msg_name = "VgmConnFr05"
    msg_id = 896
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.17
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class CarLoctrActvnSts:
        sig_name = "CarLoctrActvnSts"
        sig_start_bit = 47
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ActvnWithMsg_Idle': 0, 'ActvnWithMsg_Activation_Successful': 1, 'ActvnWithMsg_Activation_Fail': 2}
        compute_method = None
        length = 2
        startbit = 47
        byte = 5
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class BattURaw:
        sig_name = "BattURaw"
        sig_start_bit = 15
        sig_length = 9
        sig_value_factor = 0.025
        sig_value_offset = 5.0
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 15
        bmuws_info = [(1, 0b11111111, 0b00000000, 8, 0), (2, 0b10000000, 0b01111111, 1, 7)]

    class DCChrgSt:
        sig_name = "DCChrgSt"
        sig_start_bit = 39
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 13
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DCChrgrSts_Idle': 0, 'DCChrgrSts_Prestart': 1, 'DCChrgrSts_Charging': 2, 'DCChrgrSts_DCChrgnFltVehSide': 3, 'DCChrgrSts_DCChrgnFltChrgrSideTempFlt': 4, 'DCChrgrSts_DCChrgnFltChrgrSideConnectFlt': 5, 'DCChrgrSts_DCChrgnFltChrgrSideOtherFlt': 6, 'DCChrgrSts_DCChrgnFltChrgrSideEmgyFlt': 7, 'DCChrgrSts_DCChrgnFltChrgrSideComFlt': 8, 'DCChrgrSts_Bookcharging': 9, 'DCChrgrSts_Shuntdown': 10, 'DCChrgrSts_Heating': 11, 'DCChrgrSts_Supercharging': 12, 'DCChrgrSts_SuperchargingEnd': 13}
        compute_method = None
        length = 4
        startbit = 39
        byte = 4
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class TankFlapSts:
        sig_name = "TankFlapSts"
        sig_start_bit = 58
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorSts2_Ukwn': 0, 'DoorSts2_Opend': 1, 'DoorSts2_Clsd': 2}
        compute_method = None
        length = 2
        startbit = 58
        byte = 7
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class EngForbidRespFromVMM:
        sig_name = "EngForbidRespFromVMM"
        sig_start_bit = 44
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 44
        byte = 5
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class PrkgClimaWarn:
        sig_name = "PrkgClimaWarn"
        sig_start_bit = 20
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 8
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ClimaWarn_NoWarn': 0, 'ClimaWarn_FuLo': 1, 'ClimaWarn_BattLo': 2, 'ClimaWarn_FuAndBattLo': 3, 'ClimaWarn_TLo': 4, 'ClimaWarn_THi': 5, 'ClimaWarn_Error': 6, 'ClimaWarn_HVError': 7, 'ClimaWarn_ActvnLimd': 8}
        compute_method = None
        length = 4
        startbit = 20
        byte = 2
        mask = 0b00011110
        unmask = 0b11100001
        shift = 1

    class ChrgLidRearSts:
        sig_name = "ChrgLidRearSts"
        sig_start_bit = 43
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorSts2_Ukwn': 0, 'DoorSts2_Opend': 1, 'DoorSts2_Clsd': 2}
        compute_method = None
        length = 2
        startbit = 43
        byte = 5
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class ChrgLidFrntLockSts:
        sig_name = "ChrgLidFrntLockSts"
        sig_start_bit = 33
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LockSts2_LockStsUkwn': 0, 'LockSts2_Unlckd': 1, 'LockSts2_Lockd': 2, 'LockSts2_SafeLockd': 3}
        compute_method = None
        length = 2
        startbit = 33
        byte = 4
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class ChrgLidFrntSts:
        sig_name = "ChrgLidFrntSts"
        sig_start_bit = 41
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorSts2_Ukwn': 0, 'DoorSts2_Opend': 1, 'DoorSts2_Clsd': 2}
        compute_method = None
        length = 2
        startbit = 41
        byte = 5
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0


class VgmConnFr17:
    msg_name = "VgmConnFr17"
    msg_id = 1072
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.07
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class VinVINSignalPos2:
        sig_name = "VinVINSignalPos2"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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

    class VinVINSignalPos6:
        sig_name = "VinVINSignalPos6"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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

    class VinVINSignalPos1:
        sig_name = "VinVINSignalPos1"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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

    class VinVINSignalPos5:
        sig_name = "VinVINSignalPos5"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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

    class VinVINSignalPos7:
        sig_name = "VinVINSignalPos7"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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

    class VinBlockNr:
        sig_name = "VinBlockNr"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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

    class VinVINSignalPos4:
        sig_name = "VinVINSignalPos4"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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

    class VinVINSignalPos3:
        sig_name = "VinVINSignalPos3"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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


class VgmConnFr34:
    msg_name = "VgmConnFr34"
    msg_id = 389
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.045
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class MobDevKeyEnaStsToBLEKey5:
        sig_name = "MobDevKeyEnaStsToBLEKey5"
        sig_start_bit = 13
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeySts1_KeyStsIdle': 0, 'KeySts1_KeyStsDi': 1, 'KeySts1_KeyStsEna': 2, 'KeySts1_KeyStsLimd': 3}
        compute_method = None
        length = 2
        startbit = 13
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class MobDevKeyEnaStsToBLEKey9:
        sig_name = "MobDevKeyEnaStsToBLEKey9"
        sig_start_bit = 21
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeySts1_KeyStsIdle': 0, 'KeySts1_KeyStsDi': 1, 'KeySts1_KeyStsEna': 2, 'KeySts1_KeyStsLimd': 3}
        compute_method = None
        length = 2
        startbit = 21
        byte = 2
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class MobDevKeyEnaStsToBLEKey11:
        sig_name = "MobDevKeyEnaStsToBLEKey11"
        sig_start_bit = 17
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeySts1_KeyStsIdle': 0, 'KeySts1_KeyStsDi': 1, 'KeySts1_KeyStsEna': 2, 'KeySts1_KeyStsLimd': 3}
        compute_method = None
        length = 2
        startbit = 17
        byte = 2
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class MobDevKeyEnaStsToBLEKey0:
        sig_name = "MobDevKeyEnaStsToBLEKey0"
        sig_start_bit = 7
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeySts1_KeyStsIdle': 0, 'KeySts1_KeyStsDi': 1, 'KeySts1_KeyStsEna': 2, 'KeySts1_KeyStsLimd': 3}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class MobDevKeyEnaStsToBLEKey8:
        sig_name = "MobDevKeyEnaStsToBLEKey8"
        sig_start_bit = 23
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeySts1_KeyStsIdle': 0, 'KeySts1_KeyStsDi': 1, 'KeySts1_KeyStsEna': 2, 'KeySts1_KeyStsLimd': 3}
        compute_method = None
        length = 2
        startbit = 23
        byte = 2
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class MobDevKeyEnaStsToBLEKey7:
        sig_name = "MobDevKeyEnaStsToBLEKey7"
        sig_start_bit = 9
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeySts1_KeyStsIdle': 0, 'KeySts1_KeyStsDi': 1, 'KeySts1_KeyStsEna': 2, 'KeySts1_KeyStsLimd': 3}
        compute_method = None
        length = 2
        startbit = 9
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class DigKeyPasEntryDiSts:
        sig_name = "DigKeyPasEntryDiSts"
        sig_start_bit = 30
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 30
        byte = 3
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class MobDevKeyEnaStsToBLEKey10:
        sig_name = "MobDevKeyEnaStsToBLEKey10"
        sig_start_bit = 19
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeySts1_KeyStsIdle': 0, 'KeySts1_KeyStsDi': 1, 'KeySts1_KeyStsEna': 2, 'KeySts1_KeyStsLimd': 3}
        compute_method = None
        length = 2
        startbit = 19
        byte = 2
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class MobDevKeyEnaStsToBLEKey2:
        sig_name = "MobDevKeyEnaStsToBLEKey2"
        sig_start_bit = 3
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeySts1_KeyStsIdle': 0, 'KeySts1_KeyStsDi': 1, 'KeySts1_KeyStsEna': 2, 'KeySts1_KeyStsLimd': 3}
        compute_method = None
        length = 2
        startbit = 3
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class MobDevKeyEnaStsToBLEKey4:
        sig_name = "MobDevKeyEnaStsToBLEKey4"
        sig_start_bit = 15
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeySts1_KeyStsIdle': 0, 'KeySts1_KeyStsDi': 1, 'KeySts1_KeyStsEna': 2, 'KeySts1_KeyStsLimd': 3}
        compute_method = None
        length = 2
        startbit = 15
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class MobDevKeyEnaStsToBLEKey1:
        sig_name = "MobDevKeyEnaStsToBLEKey1"
        sig_start_bit = 5
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeySts1_KeyStsIdle': 0, 'KeySts1_KeyStsDi': 1, 'KeySts1_KeyStsEna': 2, 'KeySts1_KeyStsLimd': 3}
        compute_method = None
        length = 2
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class MobDevKeyEnaStsToBLEKey3:
        sig_name = "MobDevKeyEnaStsToBLEKey3"
        sig_start_bit = 1
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeySts1_KeyStsIdle': 0, 'KeySts1_KeyStsDi': 1, 'KeySts1_KeyStsEna': 2, 'KeySts1_KeyStsLimd': 3}
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class MobDevKeyEnaStsToBLEKey6:
        sig_name = "MobDevKeyEnaStsToBLEKey6"
        sig_start_bit = 11
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeySts1_KeyStsIdle': 0, 'KeySts1_KeyStsDi': 1, 'KeySts1_KeyStsEna': 2, 'KeySts1_KeyStsLimd': 3}
        compute_method = None
        length = 2
        startbit = 11
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2


class VgmConnectivityVFCInfoEnaFr:
    msg_name = "VgmConnectivityVFCInfoEnaFr"
    msg_id = 1375
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 1
    tx_node = "BGM"
    rx_nodes = []

    class VFCInfoEna:
        sig_name = "VFCInfoEna"
        sig_start_bit = 0
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EnableDisableCoding_Disabled': 0, 'EnableDisableCoding_Enabled': 1}
        compute_method = None
        length = 1
        startbit = 0
        byte = 0
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0


class VgmConnFr11:
    msg_name = "VgmConnFr11"
    msg_id = 1024
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class VehCfgPrmExtBlkIDBytePosn1:
        sig_name = "VehCfgPrmExtBlkIDBytePosn1"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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

    class VehCfgPrmExtCCPBytePosn7:
        sig_name = "VehCfgPrmExtCCPBytePosn7"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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

    class VehCfgPrmExtCCPBytePosn2:
        sig_name = "VehCfgPrmExtCCPBytePosn2"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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

    class VehCfgPrmExtCCPBytePosn3:
        sig_name = "VehCfgPrmExtCCPBytePosn3"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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

    class VehCfgPrmExtCCPBytePosn8:
        sig_name = "VehCfgPrmExtCCPBytePosn8"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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

    class VehCfgPrmExtCCPBytePosn6:
        sig_name = "VehCfgPrmExtCCPBytePosn6"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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

    class VehCfgPrmExtCCPBytePosn4:
        sig_name = "VehCfgPrmExtCCPBytePosn4"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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

    class VehCfgPrmExtCCPBytePosn5:
        sig_name = "VehCfgPrmExtCCPBytePosn5"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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


class VgmConnFr28:
    msg_name = "VgmConnFr28"
    msg_id = 48
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "BGM"
    rx_nodes = []

    class DigkeyBLEReq2:
        sig_name = "DigkeyBLEReq2"
        sig_start_bit = 0
        sig_length = 512
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = None
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 512
        startbit = 0
        bmuws_info = [(0, 0b00000001, 0b11111110, 1, 0), (1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111111, 0b00000000, 8, 0), (8, 0b11111111, 0b00000000, 8, 0), (9, 0b11111111, 0b00000000, 8, 0), (10, 0b11111111, 0b00000000, 8, 0), (11, 0b11111111, 0b00000000, 8, 0), (12, 0b11111111, 0b00000000, 8, 0), (13, 0b11111111, 0b00000000, 8, 0), (14, 0b11111111, 0b00000000, 8, 0), (15, 0b11111111, 0b00000000, 8, 0), (16, 0b11111111, 0b00000000, 8, 0), (17, 0b11111111, 0b00000000, 8, 0), (18, 0b11111111, 0b00000000, 8, 0), (19, 0b11111111, 0b00000000, 8, 0), (20, 0b11111111, 0b00000000, 8, 0), (21, 0b11111111, 0b00000000, 8, 0), (22, 0b11111111, 0b00000000, 8, 0), (23, 0b11111111, 0b00000000, 8, 0), (24, 0b11111111, 0b00000000, 8, 0), (25, 0b11111111, 0b00000000, 8, 0), (26, 0b11111111, 0b00000000, 8, 0), (27, 0b11111111, 0b00000000, 8, 0), (28, 0b11111111, 0b00000000, 8, 0), (29, 0b11111111, 0b00000000, 8, 0), (30, 0b11111111, 0b00000000, 8, 0), (31, 0b11111111, 0b00000000, 8, 0), (32, 0b11111111, 0b00000000, 8, 0), (33, 0b11111111, 0b00000000, 8, 0), (34, 0b11111111, 0b00000000, 8, 0), (35, 0b11111111, 0b00000000, 8, 0), (36, 0b11111111, 0b00000000, 8, 0), (37, 0b11111111, 0b00000000, 8, 0), (38, 0b11111111, 0b00000000, 8, 0), (39, 0b11111111, 0b00000000, 8, 0), (40, 0b11111111, 0b00000000, 8, 0), (41, 0b11111111, 0b00000000, 8, 0), (42, 0b11111111, 0b00000000, 8, 0), (43, 0b11111111, 0b00000000, 8, 0), (44, 0b11111111, 0b00000000, 8, 0), (45, 0b11111111, 0b00000000, 8, 0), (46, 0b11111111, 0b00000000, 8, 0), (47, 0b11111111, 0b00000000, 8, 0), (48, 0b11111111, 0b00000000, 8, 0), (49, 0b11111111, 0b00000000, 8, 0), (50, 0b11111111, 0b00000000, 8, 0), (51, 0b11111111, 0b00000000, 8, 0), (52, 0b11111111, 0b00000000, 8, 0), (53, 0b11111111, 0b00000000, 8, 0), (54, 0b11111111, 0b00000000, 8, 0), (55, 0b11111111, 0b00000000, 8, 0), (56, 0b11111111, 0b00000000, 8, 0), (57, 0b11111111, 0b00000000, 8, 0), (58, 0b11111111, 0b00000000, 8, 0), (59, 0b11111111, 0b00000000, 8, 0), (60, 0b11111111, 0b00000000, 8, 0), (61, 0b11111111, 0b00000000, 8, 0), (62, 0b11111111, 0b00000000, 8, 0), (63, 0b11111111, 0b00000000, 8, 0), (64, 0b11111110, 0b00000001, 7, 1)]


class VgmConnFr02:
    msg_name = "VgmConnFr02"
    msg_id = 336
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.035
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class VehSpdLgtCntr:
        sig_name = "VehSpdLgtCntr"
        sig_start_bit = 31
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class WinPosnStsAtReLe:
        sig_name = "WinPosnStsAtReLe"
        sig_start_bit = 36
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 31
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WinAndRoofAndCurtPosnTyp_PosnUkwn': 0, 'WinAndRoofAndCurtPosnTyp_ClsFull': 1, 'WinAndRoofAndCurtPosnTyp_PercOpen4': 2, 'WinAndRoofAndCurtPosnTyp_PercOpen8': 3, 'WinAndRoofAndCurtPosnTyp_PercOpen12': 4, 'WinAndRoofAndCurtPosnTyp_PercOpen16': 5, 'WinAndRoofAndCurtPosnTyp_PercOpen20': 6, 'WinAndRoofAndCurtPosnTyp_PercOpen24': 7, 'WinAndRoofAndCurtPosnTyp_PercOpen28': 8, 'WinAndRoofAndCurtPosnTyp_PercOpen32': 9, 'WinAndRoofAndCurtPosnTyp_PercOpen36': 10, 'WinAndRoofAndCurtPosnTyp_PercOpen40': 11, 'WinAndRoofAndCurtPosnTyp_PercOpen44': 12, 'WinAndRoofAndCurtPosnTyp_PercOpen48': 13, 'WinAndRoofAndCurtPosnTyp_PercOpen52': 14, 'WinAndRoofAndCurtPosnTyp_PercOpen56': 15, 'WinAndRoofAndCurtPosnTyp_PercOpen60': 16, 'WinAndRoofAndCurtPosnTyp_PercOpen64': 17, 'WinAndRoofAndCurtPosnTyp_PercOpen68': 18, 'WinAndRoofAndCurtPosnTyp_PercOpen72': 19, 'WinAndRoofAndCurtPosnTyp_PercOpen76': 20, 'WinAndRoofAndCurtPosnTyp_PercOpen80': 21, 'WinAndRoofAndCurtPosnTyp_PercOpen84': 22, 'WinAndRoofAndCurtPosnTyp_PercOpen88': 23, 'WinAndRoofAndCurtPosnTyp_PercOpen92': 24, 'WinAndRoofAndCurtPosnTyp_PercOpen96': 25, 'WinAndRoofAndCurtPosnTyp_OpenFull': 26, 'WinAndRoofAndCurtPosnTyp_Resd1': 27, 'WinAndRoofAndCurtPosnTyp_Resd2': 28, 'WinAndRoofAndCurtPosnTyp_Resd3': 29, 'WinAndRoofAndCurtPosnTyp_Resd4': 30, 'WinAndRoofAndCurtPosnTyp_Movg': 31}
        compute_method = None
        length = 5
        startbit = 36
        byte = 4
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class WinPosnStsAtReRi:
        sig_name = "WinPosnStsAtReRi"
        sig_start_bit = 44
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 31
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WinAndRoofAndCurtPosnTyp_PosnUkwn': 0, 'WinAndRoofAndCurtPosnTyp_ClsFull': 1, 'WinAndRoofAndCurtPosnTyp_PercOpen4': 2, 'WinAndRoofAndCurtPosnTyp_PercOpen8': 3, 'WinAndRoofAndCurtPosnTyp_PercOpen12': 4, 'WinAndRoofAndCurtPosnTyp_PercOpen16': 5, 'WinAndRoofAndCurtPosnTyp_PercOpen20': 6, 'WinAndRoofAndCurtPosnTyp_PercOpen24': 7, 'WinAndRoofAndCurtPosnTyp_PercOpen28': 8, 'WinAndRoofAndCurtPosnTyp_PercOpen32': 9, 'WinAndRoofAndCurtPosnTyp_PercOpen36': 10, 'WinAndRoofAndCurtPosnTyp_PercOpen40': 11, 'WinAndRoofAndCurtPosnTyp_PercOpen44': 12, 'WinAndRoofAndCurtPosnTyp_PercOpen48': 13, 'WinAndRoofAndCurtPosnTyp_PercOpen52': 14, 'WinAndRoofAndCurtPosnTyp_PercOpen56': 15, 'WinAndRoofAndCurtPosnTyp_PercOpen60': 16, 'WinAndRoofAndCurtPosnTyp_PercOpen64': 17, 'WinAndRoofAndCurtPosnTyp_PercOpen68': 18, 'WinAndRoofAndCurtPosnTyp_PercOpen72': 19, 'WinAndRoofAndCurtPosnTyp_PercOpen76': 20, 'WinAndRoofAndCurtPosnTyp_PercOpen80': 21, 'WinAndRoofAndCurtPosnTyp_PercOpen84': 22, 'WinAndRoofAndCurtPosnTyp_PercOpen88': 23, 'WinAndRoofAndCurtPosnTyp_PercOpen92': 24, 'WinAndRoofAndCurtPosnTyp_PercOpen96': 25, 'WinAndRoofAndCurtPosnTyp_OpenFull': 26, 'WinAndRoofAndCurtPosnTyp_Resd1': 27, 'WinAndRoofAndCurtPosnTyp_Resd2': 28, 'WinAndRoofAndCurtPosnTyp_Resd3': 29, 'WinAndRoofAndCurtPosnTyp_Resd4': 30, 'WinAndRoofAndCurtPosnTyp_Movg': 31}
        compute_method = None
        length = 5
        startbit = 44
        byte = 5
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class VehSpdLgtQf:
        sig_name = "VehSpdLgtQf"
        sig_start_bit = 27
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class DoorDrvrSts:
        sig_name = "DoorDrvrSts"
        sig_start_bit = 25
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorSts2_Ukwn': 0, 'DoorSts2_Opend': 1, 'DoorSts2_Clsd': 2}
        compute_method = None
        length = 2
        startbit = 25
        byte = 3
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VehSpdLgtA:
        sig_name = "VehSpdLgtA"
        sig_start_bit = 6
        sig_length = 15
        sig_value_factor = 0.00391
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 31970
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 6
        bmuws_info = [(0, 0b01111111, 0b10000000, 7, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class VehSpdLgtChks:
        sig_name = "VehSpdLgtChks"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class TrLockSts:
        sig_name = "TrLockSts"
        sig_start_bit = 47
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LockSts2_LockStsUkwn': 0, 'LockSts2_Unlckd': 1, 'LockSts2_Lockd': 2, 'LockSts2_SafeLockd': 3}
        compute_method = None
        length = 2
        startbit = 47
        byte = 5
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class BgmConnectivityFr01:
    msg_name = "BgmConnectivityFr01"
    msg_id = 367
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DigKeyGidInfo1Byte1:
        sig_name = "DigKeyGidInfo1Byte1"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 32
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyGidInfo1Byte2:
        sig_name = "DigKeyGidInfo1Byte2"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 32
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 23
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyGidInfo1Byte7:
        sig_name = "DigKeyGidInfo1Byte7"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 32
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyGidInfo1Byte4:
        sig_name = "DigKeyGidInfo1Byte4"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 32
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyGidInfo1Byte6:
        sig_name = "DigKeyGidInfo1Byte6"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 32
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyGidInfo1Byte5:
        sig_name = "DigKeyGidInfo1Byte5"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 32
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyGidInfo1Byte3:
        sig_name = "DigKeyGidInfo1Byte3"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 32
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyGidInfo1Byte0:
        sig_name = "DigKeyGidInfo1Byte0"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 32
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class TcamConnectivityFr12:
    msg_name = "TcamConnectivityFr12"
    msg_id = 356
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class RemStrtHvCtrlReqErsRunTime:
        sig_name = "RemStrtHvCtrlReqErsRunTime"
        sig_start_bit = 37
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 37
        byte = 4
        mask = 0b00111111
        unmask = 0b11000000
        shift = 0

    class RemStrtHvCtrlReqErsCmd:
        sig_name = "RemStrtHvCtrlReqErsCmd"
        sig_start_bit = 39
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ErsCmd_ErsCmdNotSet': 0, 'ErsCmd_ErsCmdOn': 1, 'ErsCmd_ErsCmdOff': 2}
        compute_method = None
        length = 2
        startbit = 39
        byte = 4
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class RemStrtExtnTiReq:
        sig_name = "RemStrtExtnTiReq"
        sig_start_bit = 31
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 31
        byte = 3
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class RemHvStrtActvReq:
        sig_name = "RemHvStrtActvReq"
        sig_start_bit = 41
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffNoReq_NoReq': 0, 'OnOffNoReq_On': 1, 'OnOffNoReq_Off': 2}
        compute_method = None
        length = 2
        startbit = 41
        byte = 5
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class RemDCChrgLidTelmReq:
        sig_name = "RemDCChrgLidTelmReq"
        sig_start_bit = 18
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffNoReq_NoReq': 0, 'OnOffNoReq_On': 1, 'OnOffNoReq_Off': 2}
        compute_method = None
        length = 2
        startbit = 18
        byte = 2
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1


class VgmConnFr15:
    msg_name = "VgmConnFr15"
    msg_id = 320
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DKDataFromCEMAcknowledgment:
        sig_name = "DKDataFromCEMAcknowledgment"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DKDataFromCEMHeader:
        sig_name = "DKDataFromCEMHeader"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DKDataFromCEMDKDataByte3:
        sig_name = "DKDataFromCEMDKDataByte3"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DKDataFromCEMDKDataByte4:
        sig_name = "DKDataFromCEMDKDataByte4"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DKDataFromCEMDKDataByte6:
        sig_name = "DKDataFromCEMDKDataByte6"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DKDataFromCEMDKDataByte1:
        sig_name = "DKDataFromCEMDKDataByte1"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DKDataFromCEMDKDataByte2:
        sig_name = "DKDataFromCEMDKDataByte2"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DKDataFromCEMDKDataByte5:
        sig_name = "DKDataFromCEMDKDataByte5"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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


class TcamConnectivityFr31:
    msg_name = "TcamConnectivityFr31"
    msg_id = 381
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 24
    tx_node = None
    rx_nodes = ['BGM']

    class TireRFNoiseMsgMinNoiseFlr:
        sig_name = "TireRFNoiseMsgMinNoiseFlr"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = 0.4
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
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

    class TireSnsrDataRID:
        sig_name = "TireSnsrDataRID"
        sig_start_bit = 71
        sig_length = 32
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 4294967295
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 32
        startbit = 71
        bmuws_info = [(8, 0b11111111, 0b00000000, 8, 0), (9, 0b11111111, 0b00000000, 8, 0), (10, 0b11111111, 0b00000000, 8, 0), (11, 0b11111111, 0b00000000, 8, 0)]

    class TireSnsrDataRFactory:
        sig_name = "TireSnsrDataRFactory"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class TelmWindowRVIReq:
        sig_name = "TelmWindowRVIReq"
        sig_start_bit = 175
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class TireSnsrDataRFct:
        sig_name = "TireSnsrDataRFct"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class TireSnsrDataRP:
        sig_name = "TireSnsrDataRP"
        sig_start_bit = 103
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 255
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 103
        byte = 12
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class TelmAVPReq:
        sig_name = "TelmAVPReq"
        sig_start_bit = 167
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 167
        byte = 20
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class TelmLockgCenRVIReq:
        sig_name = "TelmLockgCenRVIReq"
        sig_start_bit = 164
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TelmLockgCenReq2_TelmNoReq': 0, 'TelmLockgCenReq2_TelmLock': 1, 'TelmLockgCenReq2_TelmUnlck': 2, 'TelmLockgCenReq2_TelmUnlckByTrSwtEna': 3}
        compute_method = None
        length = 2
        startbit = 164
        byte = 20
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class TireSnsrDataRA:
        sig_name = "TireSnsrDataRA"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class TireSnsrDataRChks:
        sig_name = "TireSnsrDataRChks"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class RFFrameCntr:
        sig_name = "RFFrameCntr"
        sig_start_bit = 151
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class RSSI:
        sig_name = "RSSI"
        sig_start_bit = 159
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 255
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 159
        byte = 19
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class TireRFNoiseMsgAvgNoiseFlr:
        sig_name = "TireRFNoiseMsgAvgNoiseFlr"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 0.4
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
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

    class TireRFNoiseMsgNrOfSamples:
        sig_name = "TireRFNoiseMsgNrOfSamples"
        sig_start_bit = 23
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class TireSnsrDataRT:
        sig_name = "TireSnsrDataRT"
        sig_start_bit = 111
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 255
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 111
        byte = 13
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class TelmCarFindRVIReq:
        sig_name = "TelmCarFindRVIReq"
        sig_start_bit = 166
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CarFindrHornLiReqFromTelm_NoReq': 0, 'CarFindrHornLiReqFromTelm_HornReq': 1, 'CarFindrHornLiReqFromTelm_LiReq': 2, 'CarFindrHornLiReqFromTelm_HornLiReq': 3}
        compute_method = None
        length = 2
        startbit = 166
        byte = 20
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class TiStamping:
        sig_name = "TiStamping"
        sig_start_bit = 119
        sig_length = 24
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 24
        startbit = 119
        bmuws_info = [(14, 0b11111111, 0b00000000, 8, 0), (15, 0b11111111, 0b00000000, 8, 0), (16, 0b11111111, 0b00000000, 8, 0)]


class BgmConnectivityFr04:
    msg_name = "BgmConnectivityFr04"
    msg_id = 400
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.09
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class VehTiAndDataHr1:
        sig_name = "VehTiAndDataHr1"
        sig_start_bit = 31
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 31
        byte = 3
        mask = 0b11111000
        unmask = 0b00000111
        shift = 3

    class VehTiAndDataMins1:
        sig_name = "VehTiAndDataMins1"
        sig_start_bit = 9
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 9
        bmuws_info = [(1, 0b00000011, 0b11111100, 2, 0), (2, 0b11110000, 0b00001111, 4, 4)]

    class VehTiAndDataYr1:
        sig_name = "VehTiAndDataYr1"
        sig_start_bit = 7
        sig_length = 7
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 7
        byte = 0
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class VehTiAndDataDataValid:
        sig_name = "VehTiAndDataDataValid"
        sig_start_bit = 0
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class VehTiAndDataDay:
        sig_name = "VehTiAndDataDay"
        sig_start_bit = 26
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 1
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 26
        bmuws_info = [(3, 0b00000111, 0b11111000, 3, 0), (4, 0b11000000, 0b00111111, 2, 6)]

    class VehTiAndDataMth1:
        sig_name = "VehTiAndDataMth1"
        sig_start_bit = 19
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 1
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 19
        byte = 2
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class VehTiAndDataSec1:
        sig_name = "VehTiAndDataSec1"
        sig_start_bit = 15
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 15
        byte = 1
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2


class VgmConnFr33:
    msg_name = "VgmConnFr33"
    msg_id = 596
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.12
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class RemVentActvSts:
        sig_name = "RemVentActvSts"
        sig_start_bit = 5
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class RemVentWarnSts:
        sig_name = "RemVentWarnSts"
        sig_start_bit = 15
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'RemVentWarningSts_NoErr': 0, 'RemVentWarningSts_Err': 1, 'RemVentWarningSts_PwrNotAllwd': 2, 'RemVentWarningSts_EgyNotAllwd': 3}
        compute_method = None
        length = 2
        startbit = 15
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class SceneModSeld:
        sig_name = "SceneModSeld"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 13
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PatSeld_NoSeld': 0, 'PatSeld_RefrshPatSeld': 1, 'PatSeld_ParentchildPatSeld': 2, 'PatSeld_Restpatseld': 3, 'PatSeld_RomanticPatseld': 4, 'PatSeld_StrangerPatseld': 5, 'PatSeld_TheaterPatseld': 6, 'PatSeld_PetPatseld': 7, 'PatSeld_BiochalPatseld': 8, 'PatSeld_CarWashPatseld': 9, 'PatSeld_EcoPatseld': 10, 'PatSeld_KingPatseld': 11, 'PatSeld_CustomizationPatseld': 12, 'PatSeld_MeetingPatseld': 13}
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class RemVentReqRspnFb:
        sig_name = "RemVentReqRspnFb"
        sig_start_bit = 4
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class ClimaOvrHeatProActvSts:
        sig_name = "ClimaOvrHeatProActvSts"
        sig_start_bit = 6
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class CdsParkgClimaActv:
        sig_name = "CdsParkgClimaActv"
        sig_start_bit = 7
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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


class BgmConnectivityCANNmFr:
    msg_name = "BgmConnectivityCANNmFr"
    msg_id = 1331
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []


class BncmConnectivityFr12:
    msg_name = "BncmConnectivityFr12"
    msg_id = 16
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class DigKeyIDFndInStsByte1:
        sig_name = "DigKeyIDFndInStsByte1"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DigKeyIDFndInStsDigKeyInSearchSts:
        sig_name = "DigKeyIDFndInStsDigKeyInSearchSts"
        sig_start_bit = 3
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 8
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DigKeyInSearchSts_DigKeySearchInIdle': 0, 'DigKeyInSearchSts_DigKeySearchInInProgs': 1, 'DigKeyInSearchSts_DigKeySearchInNoPrsnt': 2, 'DigKeyInSearchSts_DigKeySearchInDrvrFrntFnd': 3, 'DigKeyInSearchSts_DigKeySearchInCntrCnslFnd': 4, 'DigKeyInSearchSts_DigKeySearchInPassFrntFnd': 5, 'DigKeyInSearchSts_DigKeySearchInPassRearFnd': 6, 'DigKeyInSearchSts_DigKeySearchInTrFnd': 7, 'DigKeyInSearchSts_Resd': 8}
        compute_method = None
        length = 4
        startbit = 3
        byte = 0
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DigKeyIDFndInStsByte6:
        sig_name = "DigKeyIDFndInStsByte6"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DigKeyIDFndInStsByte5:
        sig_name = "DigKeyIDFndInStsByte5"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DigKeyIDFndInStsByte4:
        sig_name = "DigKeyIDFndInStsByte4"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DigKeyIDFndInStsByte3:
        sig_name = "DigKeyIDFndInStsByte3"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DigKeyIDFndInStsByte2:
        sig_name = "DigKeyIDFndInStsByte2"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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


class BncmConnectivityFr16:
    msg_name = "BncmConnectivityFr16"
    msg_id = 329
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = None
    rx_nodes = ['BGM']

    class DigKeyBLEResp2:
        sig_name = "DigKeyBLEResp2"
        sig_start_bit = 0
        sig_length = 512
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = None
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 512
        startbit = 0
        bmuws_info = [(0, 0b00000001, 0b11111110, 1, 0), (1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111111, 0b00000000, 8, 0), (8, 0b11111111, 0b00000000, 8, 0), (9, 0b11111111, 0b00000000, 8, 0), (10, 0b11111111, 0b00000000, 8, 0), (11, 0b11111111, 0b00000000, 8, 0), (12, 0b11111111, 0b00000000, 8, 0), (13, 0b11111111, 0b00000000, 8, 0), (14, 0b11111111, 0b00000000, 8, 0), (15, 0b11111111, 0b00000000, 8, 0), (16, 0b11111111, 0b00000000, 8, 0), (17, 0b11111111, 0b00000000, 8, 0), (18, 0b11111111, 0b00000000, 8, 0), (19, 0b11111111, 0b00000000, 8, 0), (20, 0b11111111, 0b00000000, 8, 0), (21, 0b11111111, 0b00000000, 8, 0), (22, 0b11111111, 0b00000000, 8, 0), (23, 0b11111111, 0b00000000, 8, 0), (24, 0b11111111, 0b00000000, 8, 0), (25, 0b11111111, 0b00000000, 8, 0), (26, 0b11111111, 0b00000000, 8, 0), (27, 0b11111111, 0b00000000, 8, 0), (28, 0b11111111, 0b00000000, 8, 0), (29, 0b11111111, 0b00000000, 8, 0), (30, 0b11111111, 0b00000000, 8, 0), (31, 0b11111111, 0b00000000, 8, 0), (32, 0b11111111, 0b00000000, 8, 0), (33, 0b11111111, 0b00000000, 8, 0), (34, 0b11111111, 0b00000000, 8, 0), (35, 0b11111111, 0b00000000, 8, 0), (36, 0b11111111, 0b00000000, 8, 0), (37, 0b11111111, 0b00000000, 8, 0), (38, 0b11111111, 0b00000000, 8, 0), (39, 0b11111111, 0b00000000, 8, 0), (40, 0b11111111, 0b00000000, 8, 0), (41, 0b11111111, 0b00000000, 8, 0), (42, 0b11111111, 0b00000000, 8, 0), (43, 0b11111111, 0b00000000, 8, 0), (44, 0b11111111, 0b00000000, 8, 0), (45, 0b11111111, 0b00000000, 8, 0), (46, 0b11111111, 0b00000000, 8, 0), (47, 0b11111111, 0b00000000, 8, 0), (48, 0b11111111, 0b00000000, 8, 0), (49, 0b11111111, 0b00000000, 8, 0), (50, 0b11111111, 0b00000000, 8, 0), (51, 0b11111111, 0b00000000, 8, 0), (52, 0b11111111, 0b00000000, 8, 0), (53, 0b11111111, 0b00000000, 8, 0), (54, 0b11111111, 0b00000000, 8, 0), (55, 0b11111111, 0b00000000, 8, 0), (56, 0b11111111, 0b00000000, 8, 0), (57, 0b11111111, 0b00000000, 8, 0), (58, 0b11111111, 0b00000000, 8, 0), (59, 0b11111111, 0b00000000, 8, 0), (60, 0b11111111, 0b00000000, 8, 0), (61, 0b11111111, 0b00000000, 8, 0), (62, 0b11111111, 0b00000000, 8, 0), (63, 0b11111111, 0b00000000, 8, 0), (64, 0b11111110, 0b00000001, 7, 1)]


class VgmConnFr32:
    msg_name = "VgmConnFr32"
    msg_id = 853
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.15
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class VehHomePrkgSysSts:
        sig_name = "VehHomePrkgSysSts"
        sig_start_bit = 12
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 18
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HomePrkgSysSts_Off': 0, 'HomePrkgSysSts_Standby': 1, 'HomePrkgSysSts_MapBuilding': 2, 'HomePrkgSysSts_Localization': 3, 'HomePrkgSysSts_Cruse': 4, 'HomePrkgSysSts_Reserved1': 5, 'HomePrkgSysSts_Reserved2': 6, 'HomePrkgSysSts_Reserved3': 7, 'HomePrkgSysSts_ParkingInPreactive': 8, 'HomePrkgSysSts_ParkingInProcess': 9, 'HomePrkgSysSts_Reserved4': 10, 'HomePrkgSysSts_Reserved5': 11, 'HomePrkgSysSts_ParkingOutPreactive': 12, 'HomePrkgSysSts_ParkingOutProcess': 13, 'HomePrkgSysSts_Reserved6': 14, 'HomePrkgSysSts_Reserved7': 15, 'HomePrkgSysSts_FunctionCompleted': 16, 'HomePrkgSysSts_Abort': 17, 'HomePrkgSysSts_Suspend': 18}
        compute_method = None
        length = 5
        startbit = 12
        byte = 1
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0


class BgmConnectivityFr10:
    msg_name = "BgmConnectivityFr10"
    msg_id = 804
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.145
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class CarCfgInfoToWPC:
        sig_name = "CarCfgInfoToWPC"
        sig_start_bit = 0
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 0
        bmuws_info = [(0, 0b00000001, 0b11111110, 1, 0), (1, 0b11100000, 0b00011111, 3, 5)]

    class RadioFrqAM:
        sig_name = "RadioFrqAM"
        sig_start_bit = 5
        sig_length = 11
        sig_value_factor = 1
        sig_value_offset = 522
        sig_value_min = 0
        sig_value_max = 1188
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 5
        bmuws_info = [(0, 0b00111111, 0b11000000, 6, 0), (1, 0b11111000, 0b00000111, 5, 3)]

    class KeyScanActv:
        sig_name = "KeyScanActv"
        sig_start_bit = 47
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 47
        byte = 5
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class RlyPwrDistbnCmd1WdPreBattSaveCmd:
        sig_name = "RlyPwrDistbnCmd1WdPreBattSaveCmd"
        sig_start_bit = 16
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 16
        byte = 2
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class WirelschrgActvReqFromHmi:
        sig_name = "WirelschrgActvReqFromHmi"
        sig_start_bit = 4
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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


class VgmConnFr52:
    msg_name = "VgmConnFr52"
    msg_id = 346
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class HvSysRlyStsHvSysRlySts:
        sig_name = "HvSysRlyStsHvSysRlySts"
        sig_start_bit = 53
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvActvnSts_Open': 0, 'HvActvnSts_Clsd': 1, 'HvActvnSts_KeepSt': 2, 'HvActvnSts_OpenAndReqActvDcha': 3}
        compute_method = None
        length = 2
        startbit = 53
        byte = 6
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class HvSysRlyStsChks:
        sig_name = "HvSysRlyStsChks"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class HvSysRlyStsCntr:
        sig_name = "HvSysRlyStsCntr"
        sig_start_bit = 51
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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


class VgmConnFr06:
    msg_name = "VgmConnFr06"
    msg_id = 816
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class VehCfgPrmCCPBytePosn5:
        sig_name = "VehCfgPrmCCPBytePosn5"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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

    class VehCfgPrmCCPBytePosn7:
        sig_name = "VehCfgPrmCCPBytePosn7"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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

    class VehCfgPrmCCPBytePosn6:
        sig_name = "VehCfgPrmCCPBytePosn6"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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

    class VehCfgPrmCCPBytePosn4:
        sig_name = "VehCfgPrmCCPBytePosn4"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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

    class VehCfgPrmCCPBytePosn3:
        sig_name = "VehCfgPrmCCPBytePosn3"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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

    class VehCfgPrmCCPBytePosn2:
        sig_name = "VehCfgPrmCCPBytePosn2"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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

    class VehCfgPrmBlkIDBytePosn1:
        sig_name = "VehCfgPrmBlkIDBytePosn1"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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

    class VehCfgPrmCCPBytePosn8:
        sig_name = "VehCfgPrmCCPBytePosn8"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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


class BgmConnectivityFr08:
    msg_name = "BgmConnectivityFr08"
    msg_id = 901
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class BodyRemoteLockFBStatus:
        sig_name = "BodyRemoteLockFBStatus"
        sig_start_bit = 27
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 11
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Default': 0, 'NetWakeFail': 1, 'RVIAuthFail': 2, 'CarmodeFail': 3, 'UsagemodeFail': 4, 'DelayFail': 5, 'DoorsOpenFail': 6, 'Reserve1Fail': 7, 'Reserve2Fail': 8, 'Reserve3Fail': 9, 'Success': 10, 'Reserve4': 11}
        compute_method = None
        length = 4
        startbit = 27
        byte = 3
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class BodyRemoteWindowFBBodyRemoteWindowFRPosnAtDrvr:
        sig_name = "BodyRemoteWindowFBBodyRemoteWindowFRPosnAtDrvr"
        sig_start_bit = 39
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 31
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WinAndRoofAndCurtPosnTyp_PosnUkwn': 0, 'WinAndRoofAndCurtPosnTyp_ClsFull': 1, 'WinAndRoofAndCurtPosnTyp_PercOpen4': 2, 'WinAndRoofAndCurtPosnTyp_PercOpen8': 3, 'WinAndRoofAndCurtPosnTyp_PercOpen12': 4, 'WinAndRoofAndCurtPosnTyp_PercOpen16': 5, 'WinAndRoofAndCurtPosnTyp_PercOpen20': 6, 'WinAndRoofAndCurtPosnTyp_PercOpen24': 7, 'WinAndRoofAndCurtPosnTyp_PercOpen28': 8, 'WinAndRoofAndCurtPosnTyp_PercOpen32': 9, 'WinAndRoofAndCurtPosnTyp_PercOpen36': 10, 'WinAndRoofAndCurtPosnTyp_PercOpen40': 11, 'WinAndRoofAndCurtPosnTyp_PercOpen44': 12, 'WinAndRoofAndCurtPosnTyp_PercOpen48': 13, 'WinAndRoofAndCurtPosnTyp_PercOpen52': 14, 'WinAndRoofAndCurtPosnTyp_PercOpen56': 15, 'WinAndRoofAndCurtPosnTyp_PercOpen60': 16, 'WinAndRoofAndCurtPosnTyp_PercOpen64': 17, 'WinAndRoofAndCurtPosnTyp_PercOpen68': 18, 'WinAndRoofAndCurtPosnTyp_PercOpen72': 19, 'WinAndRoofAndCurtPosnTyp_PercOpen76': 20, 'WinAndRoofAndCurtPosnTyp_PercOpen80': 21, 'WinAndRoofAndCurtPosnTyp_PercOpen84': 22, 'WinAndRoofAndCurtPosnTyp_PercOpen88': 23, 'WinAndRoofAndCurtPosnTyp_PercOpen92': 24, 'WinAndRoofAndCurtPosnTyp_PercOpen96': 25, 'WinAndRoofAndCurtPosnTyp_OpenFull': 26, 'WinAndRoofAndCurtPosnTyp_Resd1': 27, 'WinAndRoofAndCurtPosnTyp_Resd2': 28, 'WinAndRoofAndCurtPosnTyp_Resd3': 29, 'WinAndRoofAndCurtPosnTyp_Resd4': 30, 'WinAndRoofAndCurtPosnTyp_Movg': 31}
        compute_method = None
        length = 5
        startbit = 39
        byte = 4
        mask = 0b11111000
        unmask = 0b00000111
        shift = 3

    class TireFilFilSwt:
        sig_name = "TireFilFilSwt"
        sig_start_bit = 13
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 13
        byte = 1
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class BodyRemoteWindowFBBodyRemoteWindowFRPosnAtReRi:
        sig_name = "BodyRemoteWindowFBBodyRemoteWindowFRPosnAtReRi"
        sig_start_bit = 40
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 31
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WinAndRoofAndCurtPosnTyp_PosnUkwn': 0, 'WinAndRoofAndCurtPosnTyp_ClsFull': 1, 'WinAndRoofAndCurtPosnTyp_PercOpen4': 2, 'WinAndRoofAndCurtPosnTyp_PercOpen8': 3, 'WinAndRoofAndCurtPosnTyp_PercOpen12': 4, 'WinAndRoofAndCurtPosnTyp_PercOpen16': 5, 'WinAndRoofAndCurtPosnTyp_PercOpen20': 6, 'WinAndRoofAndCurtPosnTyp_PercOpen24': 7, 'WinAndRoofAndCurtPosnTyp_PercOpen28': 8, 'WinAndRoofAndCurtPosnTyp_PercOpen32': 9, 'WinAndRoofAndCurtPosnTyp_PercOpen36': 10, 'WinAndRoofAndCurtPosnTyp_PercOpen40': 11, 'WinAndRoofAndCurtPosnTyp_PercOpen44': 12, 'WinAndRoofAndCurtPosnTyp_PercOpen48': 13, 'WinAndRoofAndCurtPosnTyp_PercOpen52': 14, 'WinAndRoofAndCurtPosnTyp_PercOpen56': 15, 'WinAndRoofAndCurtPosnTyp_PercOpen60': 16, 'WinAndRoofAndCurtPosnTyp_PercOpen64': 17, 'WinAndRoofAndCurtPosnTyp_PercOpen68': 18, 'WinAndRoofAndCurtPosnTyp_PercOpen72': 19, 'WinAndRoofAndCurtPosnTyp_PercOpen76': 20, 'WinAndRoofAndCurtPosnTyp_PercOpen80': 21, 'WinAndRoofAndCurtPosnTyp_PercOpen84': 22, 'WinAndRoofAndCurtPosnTyp_PercOpen88': 23, 'WinAndRoofAndCurtPosnTyp_PercOpen92': 24, 'WinAndRoofAndCurtPosnTyp_PercOpen96': 25, 'WinAndRoofAndCurtPosnTyp_OpenFull': 26, 'WinAndRoofAndCurtPosnTyp_Resd1': 27, 'WinAndRoofAndCurtPosnTyp_Resd2': 28, 'WinAndRoofAndCurtPosnTyp_Resd3': 29, 'WinAndRoofAndCurtPosnTyp_Resd4': 30, 'WinAndRoofAndCurtPosnTyp_Movg': 31}
        compute_method = None
        length = 5
        startbit = 40
        bmuws_info = [(5, 0b00000001, 0b11111110, 1, 0), (6, 0b11110000, 0b00001111, 4, 4)]

    class BodyRemoteWindowFBBodyRemoteWindowFRPosnAtPass:
        sig_name = "BodyRemoteWindowFBBodyRemoteWindowFRPosnAtPass"
        sig_start_bit = 34
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 31
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WinAndRoofAndCurtPosnTyp_PosnUkwn': 0, 'WinAndRoofAndCurtPosnTyp_ClsFull': 1, 'WinAndRoofAndCurtPosnTyp_PercOpen4': 2, 'WinAndRoofAndCurtPosnTyp_PercOpen8': 3, 'WinAndRoofAndCurtPosnTyp_PercOpen12': 4, 'WinAndRoofAndCurtPosnTyp_PercOpen16': 5, 'WinAndRoofAndCurtPosnTyp_PercOpen20': 6, 'WinAndRoofAndCurtPosnTyp_PercOpen24': 7, 'WinAndRoofAndCurtPosnTyp_PercOpen28': 8, 'WinAndRoofAndCurtPosnTyp_PercOpen32': 9, 'WinAndRoofAndCurtPosnTyp_PercOpen36': 10, 'WinAndRoofAndCurtPosnTyp_PercOpen40': 11, 'WinAndRoofAndCurtPosnTyp_PercOpen44': 12, 'WinAndRoofAndCurtPosnTyp_PercOpen48': 13, 'WinAndRoofAndCurtPosnTyp_PercOpen52': 14, 'WinAndRoofAndCurtPosnTyp_PercOpen56': 15, 'WinAndRoofAndCurtPosnTyp_PercOpen60': 16, 'WinAndRoofAndCurtPosnTyp_PercOpen64': 17, 'WinAndRoofAndCurtPosnTyp_PercOpen68': 18, 'WinAndRoofAndCurtPosnTyp_PercOpen72': 19, 'WinAndRoofAndCurtPosnTyp_PercOpen76': 20, 'WinAndRoofAndCurtPosnTyp_PercOpen80': 21, 'WinAndRoofAndCurtPosnTyp_PercOpen84': 22, 'WinAndRoofAndCurtPosnTyp_PercOpen88': 23, 'WinAndRoofAndCurtPosnTyp_PercOpen92': 24, 'WinAndRoofAndCurtPosnTyp_PercOpen96': 25, 'WinAndRoofAndCurtPosnTyp_OpenFull': 26, 'WinAndRoofAndCurtPosnTyp_Resd1': 27, 'WinAndRoofAndCurtPosnTyp_Resd2': 28, 'WinAndRoofAndCurtPosnTyp_Resd3': 29, 'WinAndRoofAndCurtPosnTyp_Resd4': 30, 'WinAndRoofAndCurtPosnTyp_Movg': 31}
        compute_method = None
        length = 5
        startbit = 34
        bmuws_info = [(4, 0b00000111, 0b11111000, 3, 0), (5, 0b11000000, 0b00111111, 2, 6)]

    class BodyRemoteWindowFBStatus:
        sig_name = "BodyRemoteWindowFBStatus"
        sig_start_bit = 51
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 11
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Default': 0, 'NetWakeFail': 1, 'RVIAuthFail': 2, 'CarmodeFail': 3, 'UsagemodeFail': 4, 'DelayFail': 5, 'WindowfFaultFail': 6, 'reserve1Fail': 7, 'reserve2Fail': 8, 'reserve3Fail': 9, 'Success': 10, 'reserve4': 11}
        compute_method = None
        length = 4
        startbit = 51
        byte = 6
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class TireFilNoiseFlrSwt:
        sig_name = "TireFilNoiseFlrSwt"
        sig_start_bit = 12
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NormalMode': 0, 'PolarPlotMode': 1}
        compute_method = None
        length = 1
        startbit = 12
        byte = 1
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class BodyRemoteLockFBPassLockSts:
        sig_name = "BodyRemoteLockFBPassLockSts"
        sig_start_bit = 29
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LockSts2_LockStsUkwn': 0, 'LockSts2_Unlckd': 1, 'LockSts2_Lockd': 2, 'LockSts2_SafeLockd': 3}
        compute_method = None
        length = 2
        startbit = 29
        byte = 3
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class RemBookChrgnTarVal:
        sig_name = "RemBookChrgnTarVal"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class TireFilRxSwt:
        sig_name = "TireFilRxSwt"
        sig_start_bit = 11
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 11
        byte = 1
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class TireFilPollingMod:
        sig_name = "TireFilPollingMod"
        sig_start_bit = 23
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PollingMod_PolllingMode': 0, 'PollingMod_RunningMode': 1, 'PollingMod_ActivePollingMode': 2}
        compute_method = None
        length = 2
        startbit = 23
        byte = 2
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class BodyRemoteLockFBLeReLockSts:
        sig_name = "BodyRemoteLockFBLeReLockSts"
        sig_start_bit = 31
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LockSts2_LockStsUkwn': 0, 'LockSts2_Unlckd': 1, 'LockSts2_Lockd': 2, 'LockSts2_SafeLockd': 3}
        compute_method = None
        length = 2
        startbit = 31
        byte = 3
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class TireFilSnsrID:
        sig_name = "TireFilSnsrID"
        sig_start_bit = 10
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 10
        byte = 1
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class BodyRemoteLockFBDrvLockSts:
        sig_name = "BodyRemoteLockFBDrvLockSts"
        sig_start_bit = 19
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LockSts2_LockStsUkwn': 0, 'LockSts2_Unlckd': 1, 'LockSts2_Lockd': 2, 'LockSts2_SafeLockd': 3}
        compute_method = None
        length = 2
        startbit = 19
        byte = 2
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class BodyRemoteWindowFBBodyRemoteWindowFRPosnAtReLe:
        sig_name = "BodyRemoteWindowFBBodyRemoteWindowFRPosnAtReLe"
        sig_start_bit = 45
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 31
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WinAndRoofAndCurtPosnTyp_PosnUkwn': 0, 'WinAndRoofAndCurtPosnTyp_ClsFull': 1, 'WinAndRoofAndCurtPosnTyp_PercOpen4': 2, 'WinAndRoofAndCurtPosnTyp_PercOpen8': 3, 'WinAndRoofAndCurtPosnTyp_PercOpen12': 4, 'WinAndRoofAndCurtPosnTyp_PercOpen16': 5, 'WinAndRoofAndCurtPosnTyp_PercOpen20': 6, 'WinAndRoofAndCurtPosnTyp_PercOpen24': 7, 'WinAndRoofAndCurtPosnTyp_PercOpen28': 8, 'WinAndRoofAndCurtPosnTyp_PercOpen32': 9, 'WinAndRoofAndCurtPosnTyp_PercOpen36': 10, 'WinAndRoofAndCurtPosnTyp_PercOpen40': 11, 'WinAndRoofAndCurtPosnTyp_PercOpen44': 12, 'WinAndRoofAndCurtPosnTyp_PercOpen48': 13, 'WinAndRoofAndCurtPosnTyp_PercOpen52': 14, 'WinAndRoofAndCurtPosnTyp_PercOpen56': 15, 'WinAndRoofAndCurtPosnTyp_PercOpen60': 16, 'WinAndRoofAndCurtPosnTyp_PercOpen64': 17, 'WinAndRoofAndCurtPosnTyp_PercOpen68': 18, 'WinAndRoofAndCurtPosnTyp_PercOpen72': 19, 'WinAndRoofAndCurtPosnTyp_PercOpen76': 20, 'WinAndRoofAndCurtPosnTyp_PercOpen80': 21, 'WinAndRoofAndCurtPosnTyp_PercOpen84': 22, 'WinAndRoofAndCurtPosnTyp_PercOpen88': 23, 'WinAndRoofAndCurtPosnTyp_PercOpen92': 24, 'WinAndRoofAndCurtPosnTyp_PercOpen96': 25, 'WinAndRoofAndCurtPosnTyp_OpenFull': 26, 'WinAndRoofAndCurtPosnTyp_Resd1': 27, 'WinAndRoofAndCurtPosnTyp_Resd2': 28, 'WinAndRoofAndCurtPosnTyp_Resd3': 29, 'WinAndRoofAndCurtPosnTyp_Resd4': 30, 'WinAndRoofAndCurtPosnTyp_Movg': 31}
        compute_method = None
        length = 5
        startbit = 45
        byte = 5
        mask = 0b00111110
        unmask = 0b11000001
        shift = 1

    class BodyRemoteLockFBRiReLockSts:
        sig_name = "BodyRemoteLockFBRiReLockSts"
        sig_start_bit = 17
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LockSts2_LockStsUkwn': 0, 'LockSts2_Unlckd': 1, 'LockSts2_Lockd': 2, 'LockSts2_SafeLockd': 3}
        compute_method = None
        length = 2
        startbit = 17
        byte = 2
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0


class VgmConnFr23:
    msg_name = "VgmConnFr23"
    msg_id = 323
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class RPAAuthRespHeader:
        sig_name = "RPAAuthRespHeader"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class RPAAuthRespDKDataByte5:
        sig_name = "RPAAuthRespDKDataByte5"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class RPAAuthRespDKDataByte4:
        sig_name = "RPAAuthRespDKDataByte4"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class RPAAuthRespAcknowledgment:
        sig_name = "RPAAuthRespAcknowledgment"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class RPAAuthRespDKDataByte6:
        sig_name = "RPAAuthRespDKDataByte6"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class RPAAuthRespDKDataByte3:
        sig_name = "RPAAuthRespDKDataByte3"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class RPAAuthRespDKDataByte1:
        sig_name = "RPAAuthRespDKDataByte1"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class RPAAuthRespDKDataByte2:
        sig_name = "RPAAuthRespDKDataByte2"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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


class VgmConnFr30:
    msg_name = "VgmConnFr30"
    msg_id = 58
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.085
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class PrkgOutModBtnStsToAPPPrkgOutModBtnSts5:
        sig_name = "PrkgOutModBtnStsToAPPPrkgOutModBtnSts5"
        sig_start_bit = 11
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ActvnAvl4_Idle': 0, 'ActvnAvl4_Actvn': 1, 'ActvnAvl4_Deactvn': 2, 'ActvnAvl4_Recommand': 3}
        compute_method = None
        length = 2
        startbit = 11
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class PrkgOutModBtnStsToAPPPrkgOutModBtnSts1:
        sig_name = "PrkgOutModBtnStsToAPPPrkgOutModBtnSts1"
        sig_start_bit = 3
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ActvnAvl4_Idle': 0, 'ActvnAvl4_Actvn': 1, 'ActvnAvl4_Deactvn': 2, 'ActvnAvl4_Recommand': 3}
        compute_method = None
        length = 2
        startbit = 3
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class PrkgOutModBtnStsToAPPPrkgOutModBtnSts2:
        sig_name = "PrkgOutModBtnStsToAPPPrkgOutModBtnSts2"
        sig_start_bit = 1
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ActvnAvl4_Idle': 0, 'ActvnAvl4_Actvn': 1, 'ActvnAvl4_Deactvn': 2, 'ActvnAvl4_Recommand': 3}
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class PrkgOutModBtnStsToAPPPrkgOutModBtnSts3:
        sig_name = "PrkgOutModBtnStsToAPPPrkgOutModBtnSts3"
        sig_start_bit = 15
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ActvnAvl4_Idle': 0, 'ActvnAvl4_Actvn': 1, 'ActvnAvl4_Deactvn': 2, 'ActvnAvl4_Recommand': 3}
        compute_method = None
        length = 2
        startbit = 15
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class PrkgOutModBtnStsToAPPPrkgOutModBtnSts4:
        sig_name = "PrkgOutModBtnStsToAPPPrkgOutModBtnSts4"
        sig_start_bit = 13
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ActvnAvl4_Idle': 0, 'ActvnAvl4_Actvn': 1, 'ActvnAvl4_Deactvn': 2, 'ActvnAvl4_Recommand': 3}
        compute_method = None
        length = 2
        startbit = 13
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class PrkgOutModBtnStsToAPPPrkgOutModBtnSts6:
        sig_name = "PrkgOutModBtnStsToAPPPrkgOutModBtnSts6"
        sig_start_bit = 9
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ActvnAvl4_Idle': 0, 'ActvnAvl4_Actvn': 1, 'ActvnAvl4_Deactvn': 2, 'ActvnAvl4_Recommand': 3}
        compute_method = None
        length = 2
        startbit = 9
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0


class BncmBsrmConnectivityFr03:
    msg_name = "BncmBsrmConnectivityFr03"
    msg_id = 375
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class BleConSts:
        sig_name = "BleConSts"
        sig_start_bit = 7
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7


class WpcConnFr02:
    msg_name = "WpcConnFr02"
    msg_id = 769
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class WPCModuleSts:
        sig_name = "WPCModuleSts"
        sig_start_bit = 12
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WPCModuleSts_OverTemperatureProtected': 0, 'WPCModuleSts_Standby': 1, 'WPCModuleSts_Charging': 2, 'WPCModuleSts_FOD': 3, 'WPCModuleSts_VoltageProtected': 4, 'WPCModuleSts_OverPowerProtected': 5, 'WPCModuleSts_Transmittingcoildisable': 6, 'WPCModuleSts_OFF': 7, 'WPCModuleSts_ChargingCompleted': 8, 'WPCModuleSts_DeactivatedbyUser': 9, 'WPCModuleSts_Resvd2': 10, 'WPCModuleSts_Resvd3': 11, 'WPCModuleSts_Resvd4': 12, 'WPCModuleSts_Resvd5': 13, 'WPCModuleSts_Resvd6': 14, 'WPCModuleSts_Invalid': 15}
        compute_method = None
        length = 4
        startbit = 12
        byte = 1
        mask = 0b00011110
        unmask = 0b11100001
        shift = 1

    class WPCCtrlRes:
        sig_name = "WPCCtrlRes"
        sig_start_bit = 4
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WPCCtrlRes_WPCenabled': 0, 'WPCCtrlRes_WPCdisabledbyPEPS': 1, 'WPCCtrlRes_WPCshutdownbySwitchOrCAN': 2, 'WPCCtrlRes_WPCdisabledbyNFC': 3}
        compute_method = None
        length = 2
        startbit = 4
        byte = 0
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class WPCFailureSts:
        sig_name = "WPCFailureSts"
        sig_start_bit = 0
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WPCFailureSts_NoFailure': 0, 'WPCFailureSts_OverTemperature': 1, 'WPCFailureSts_RFOD': 2, 'WPCFailureSts_VoltageProtected': 3, 'WPCFailureSts_OverPowerProtected': 4, 'WPCFailureSts_InternalFailure': 5, 'WPCFailureSts_SmartPhoneNoResponseOrUnknown': 6, 'WPCFailureSts_OFOD': 7, 'WPCFailureSts_Reserved1': 8, 'WPCFailureSts_Reserved2': 9, 'WPCFailureSts_Reserved3': 10, 'WPCFailureSts_Reserved4': 11, 'WPCFailureSts_Reserved5': 12, 'WPCFailureSts_Reserved6': 13, 'WPCFailureSts_Reserved7': 14, 'WPCFailureSts_Invalid': 15}
        compute_method = None
        length = 4
        startbit = 0
        bmuws_info = [(0, 0b00000001, 0b11111110, 1, 0), (1, 0b11100000, 0b00011111, 3, 5)]

    class PhoneForgottenRmn:
        sig_name = "PhoneForgottenRmn"
        sig_start_bit = 6
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class WPCChrgnSts:
        sig_name = "WPCChrgnSts"
        sig_start_bit = 8
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WPCChrgnSts_Standby': 0, 'WPCChrgnSts_Charging': 1, 'WPCChrgnSts_ChargingcompletedAvailedwhenRxsupport': 2, 'WPCChrgnSts_Notinstandby': 3}
        compute_method = None
        length = 2
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b10000000, 0b01111111, 1, 7)]


class VgmConnFr18:
    msg_name = "VgmConnFr18"
    msg_id = 820
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.11
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class EngSt1WdStsCntr:
        sig_name = "EngSt1WdStsCntr"
        sig_start_bit = 63
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 63
        byte = 7
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class FragCh4Id:
        sig_name = "FragCh4Id"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class FragCh3Id:
        sig_name = "FragCh3Id"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class FragCh2Id:
        sig_name = "FragCh2Id"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class FragCh5Id:
        sig_name = "FragCh5Id"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class FragCh1Id:
        sig_name = "FragCh1Id"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class EngSt1WdStsEngSt1WdSts:
        sig_name = "EngSt1WdStsEngSt1WdSts"
        sig_start_bit = 59
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 9
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EngSt1_Ini': 0, 'EngSt1_Awake': 1, 'EngSt1_Rdy': 2, 'EngSt1_PreStrtg': 3, 'EngSt1_StrtgInProgs': 4, 'EngSt1_RunngRunng': 5, 'EngSt1_RunngStb': 6, 'EngSt1_RunngStrtgInProgs': 7, 'EngSt1_RunngRemStrtd': 8, 'EngSt1_AftRun': 9}
        compute_method = None
        length = 4
        startbit = 59
        byte = 7
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class CbnOverHeatProtnEna:
        sig_name = "CbnOverHeatProtnEna"
        sig_start_bit = 47
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class EngSt1WdStsChks:
        sig_name = "EngSt1WdStsChks"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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


class TcamConnectivityFr30:
    msg_name = "TcamConnectivityFr30"
    msg_id = 380
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class TelmDefrostReq:
        sig_name = "TelmDefrostReq"
        sig_start_bit = 58
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffNoReq_NoReq': 0, 'OnOffNoReq_On': 1, 'OnOffNoReq_Off': 2}
        compute_method = None
        length = 2
        startbit = 58
        byte = 7
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1


class BncmConnectivityFr08:
    msg_name = "BncmConnectivityFr08"
    msg_id = 374
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = None
    rx_nodes = ['BGM']

    class DigKeyBLEReq3:
        sig_name = "DigKeyBLEReq3"
        sig_start_bit = 0
        sig_length = 512
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = None
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 512
        startbit = 0
        bmuws_info = [(0, 0b00000001, 0b11111110, 1, 0), (1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111111, 0b00000000, 8, 0), (8, 0b11111111, 0b00000000, 8, 0), (9, 0b11111111, 0b00000000, 8, 0), (10, 0b11111111, 0b00000000, 8, 0), (11, 0b11111111, 0b00000000, 8, 0), (12, 0b11111111, 0b00000000, 8, 0), (13, 0b11111111, 0b00000000, 8, 0), (14, 0b11111111, 0b00000000, 8, 0), (15, 0b11111111, 0b00000000, 8, 0), (16, 0b11111111, 0b00000000, 8, 0), (17, 0b11111111, 0b00000000, 8, 0), (18, 0b11111111, 0b00000000, 8, 0), (19, 0b11111111, 0b00000000, 8, 0), (20, 0b11111111, 0b00000000, 8, 0), (21, 0b11111111, 0b00000000, 8, 0), (22, 0b11111111, 0b00000000, 8, 0), (23, 0b11111111, 0b00000000, 8, 0), (24, 0b11111111, 0b00000000, 8, 0), (25, 0b11111111, 0b00000000, 8, 0), (26, 0b11111111, 0b00000000, 8, 0), (27, 0b11111111, 0b00000000, 8, 0), (28, 0b11111111, 0b00000000, 8, 0), (29, 0b11111111, 0b00000000, 8, 0), (30, 0b11111111, 0b00000000, 8, 0), (31, 0b11111111, 0b00000000, 8, 0), (32, 0b11111111, 0b00000000, 8, 0), (33, 0b11111111, 0b00000000, 8, 0), (34, 0b11111111, 0b00000000, 8, 0), (35, 0b11111111, 0b00000000, 8, 0), (36, 0b11111111, 0b00000000, 8, 0), (37, 0b11111111, 0b00000000, 8, 0), (38, 0b11111111, 0b00000000, 8, 0), (39, 0b11111111, 0b00000000, 8, 0), (40, 0b11111111, 0b00000000, 8, 0), (41, 0b11111111, 0b00000000, 8, 0), (42, 0b11111111, 0b00000000, 8, 0), (43, 0b11111111, 0b00000000, 8, 0), (44, 0b11111111, 0b00000000, 8, 0), (45, 0b11111111, 0b00000000, 8, 0), (46, 0b11111111, 0b00000000, 8, 0), (47, 0b11111111, 0b00000000, 8, 0), (48, 0b11111111, 0b00000000, 8, 0), (49, 0b11111111, 0b00000000, 8, 0), (50, 0b11111111, 0b00000000, 8, 0), (51, 0b11111111, 0b00000000, 8, 0), (52, 0b11111111, 0b00000000, 8, 0), (53, 0b11111111, 0b00000000, 8, 0), (54, 0b11111111, 0b00000000, 8, 0), (55, 0b11111111, 0b00000000, 8, 0), (56, 0b11111111, 0b00000000, 8, 0), (57, 0b11111111, 0b00000000, 8, 0), (58, 0b11111111, 0b00000000, 8, 0), (59, 0b11111111, 0b00000000, 8, 0), (60, 0b11111111, 0b00000000, 8, 0), (61, 0b11111111, 0b00000000, 8, 0), (62, 0b11111111, 0b00000000, 8, 0), (63, 0b11111111, 0b00000000, 8, 0), (64, 0b11111110, 0b00000001, 7, 1)]


class TcamConnectivityFr13:
    msg_name = "TcamConnectivityFr13"
    msg_id = 360
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class RCcontrolForDCchargeLid:
        sig_name = "RCcontrolForDCchargeLid"
        sig_start_bit = 6
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PsdNotPsd1_NotPsd': 0, 'PsdNotPsd1_Psd': 1}
        compute_method = None
        length = 1
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6


class TcamConnectivityFr06:
    msg_name = "TcamConnectivityFr06"
    msg_id = 293
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class DKDataFromTelmDKDataByte3:
        sig_name = "DKDataFromTelmDKDataByte3"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DKDataFromTelmDKDataByte6:
        sig_name = "DKDataFromTelmDKDataByte6"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DKDataFromTelmHeader:
        sig_name = "DKDataFromTelmHeader"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DKDataFromTelmDKDataByte2:
        sig_name = "DKDataFromTelmDKDataByte2"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DKDataFromTelmDKDataByte1:
        sig_name = "DKDataFromTelmDKDataByte1"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DKDataFromTelmAcknowledgment:
        sig_name = "DKDataFromTelmAcknowledgment"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DKDataFromTelmDKDataByte5:
        sig_name = "DKDataFromTelmDKDataByte5"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DKDataFromTelmDKDataByte4:
        sig_name = "DKDataFromTelmDKDataByte4"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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


class BgmToBncmConnectivityDiagReqFrame:
    msg_name = "BgmToBncmConnectivityDiagReqFrame"
    msg_id = 1827
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []


class TcamConnectivityFr02:
    msg_name = "TcamConnectivityFr02"
    msg_id = 544
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class ClimaTmrStsTelmRqrd:
        sig_name = "ClimaTmrStsTelmRqrd"
        sig_start_bit = 22
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class ClimaRqrd1:
        sig_name = "ClimaRqrd1"
        sig_start_bit = 13
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffNoReq_NoReq': 0, 'OnOffNoReq_On': 1, 'OnOffNoReq_Off': 2}
        compute_method = None
        length = 2
        startbit = 13
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class TelmPM25Req:
        sig_name = "TelmPM25Req"
        sig_start_bit = 18
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class TelmClimaTmr:
        sig_name = "TelmClimaTmr"
        sig_start_bit = 39
        sig_length = 16
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 65535
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class TelmClimaTSetTempRange:
        sig_name = "TelmClimaTSetTempRange"
        sig_start_bit = 28
        sig_length = 5
        sig_value_factor = 0.5
        sig_value_offset = 15.5
        sig_value_min = 0
        sig_value_max = 26
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 28
        byte = 3
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class TelmClimaReq:
        sig_name = "TelmClimaReq"
        sig_start_bit = 21
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffNoReq_NoReq': 0, 'OnOffNoReq_On': 1, 'OnOffNoReq_Off': 2}
        compute_method = None
        length = 2
        startbit = 21
        byte = 2
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class ReqFragLvlTelm:
        sig_name = "ReqFragLvlTelm"
        sig_start_bit = 17
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ReqFragLvl_OFF': 0, 'ReqFragLvl_Level1': 1, 'ReqFragLvl_Level2': 2, 'ReqFragLvl_Level3': 3}
        compute_method = None
        length = 2
        startbit = 17
        byte = 2
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class TelmClimaTSetHmiCmptmtTSpSpcl:
        sig_name = "TelmClimaTSetHmiCmptmtTSpSpcl"
        sig_start_bit = 30
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HmiCmptmtTSpSpcl_Norm': 0, 'HmiCmptmtTSpSpcl_Lo': 1, 'HmiCmptmtTSpSpcl_Hi': 2}
        compute_method = None
        length = 2
        startbit = 30
        byte = 3
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class SeatHeatDurgClimaEnadFromTelm:
        sig_name = "SeatHeatDurgClimaEnadFromTelm"
        sig_start_bit = 10
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SeatHeatDurgClimaEnad2_SeatHeatOff': 0, 'SeatHeatDurgClimaEnad2_SeatDrvOn': 1, 'SeatHeatDurgClimaEnad2_SeatPassOn': 2, 'SeatHeatDurgClimaEnad2_SeatDrvrAndPass': 3, 'SeatHeatDurgClimaEnad2_SeatLeftRearOn': 4, 'SeatHeatDurgClimaEnad2_SeatRightRearOn': 5}
        compute_method = None
        length = 3
        startbit = 10
        byte = 1
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0


class BncmConnectivityFr14:
    msg_name = "BncmConnectivityFr14"
    msg_id = 24
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class MobDevDistStsKey0:
        sig_name = "MobDevDistStsKey0"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1023
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class MobDevDistStsKey5:
        sig_name = "MobDevDistStsKey5"
        sig_start_bit = 53
        sig_length = 10
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1023
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 53
        bmuws_info = [(6, 0b00111111, 0b11000000, 6, 0), (7, 0b11110000, 0b00001111, 4, 4)]

    class MobDevDistStsKey1:
        sig_name = "MobDevDistStsKey1"
        sig_start_bit = 13
        sig_length = 10
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1023
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 13
        bmuws_info = [(1, 0b00111111, 0b11000000, 6, 0), (2, 0b11110000, 0b00001111, 4, 4)]

    class MobDevDistStsKey3:
        sig_name = "MobDevDistStsKey3"
        sig_start_bit = 25
        sig_length = 10
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1023
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 25
        bmuws_info = [(3, 0b00000011, 0b11111100, 2, 0), (4, 0b11111111, 0b00000000, 8, 0)]

    class MobDevDistStsKey4:
        sig_name = "MobDevDistStsKey4"
        sig_start_bit = 47
        sig_length = 10
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1023
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class PasEntryEnaReq:
        sig_name = "PasEntryEnaReq"
        sig_start_bit = 58
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 58
        byte = 7
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class MobDevDistStsKey2:
        sig_name = "MobDevDistStsKey2"
        sig_start_bit = 19
        sig_length = 10
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1023
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 19
        bmuws_info = [(2, 0b00001111, 0b11110000, 4, 0), (3, 0b11111100, 0b00000011, 6, 2)]


class WpcConnectivityCANNmFr:
    msg_name = "WpcConnectivityCANNmFr"
    msg_id = 1296
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']


class BncmConnectivityFr17:
    msg_name = "BncmConnectivityFr17"
    msg_id = 408
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class UsgModChgReqFromBLE:
        sig_name = "UsgModChgReqFromBLE"
        sig_start_bit = 6
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ReqSts1_NotReqd': 0, 'ReqSts1_Reqd': 1}
        compute_method = None
        length = 1
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class BLEConRPACtrlLeft:
        sig_name = "BLEConRPACtrlLeft"
        sig_start_bit = 2
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoRequest': 0, 'Touch': 1, 'Release': 2, 'Reserved': 3}
        compute_method = None
        length = 3
        startbit = 2
        byte = 0
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class BLEConRPACtrlRgt:
        sig_name = "BLEConRPACtrlRgt"
        sig_start_bit = 12
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoRequest': 0, 'Touch': 1, 'Release': 2, 'Reserved': 3}
        compute_method = None
        length = 3
        startbit = 12
        byte = 1
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class BLEConRPACtrlRear:
        sig_name = "BLEConRPACtrlRear"
        sig_start_bit = 15
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoRequest': 0, 'Touch': 1, 'Release': 2, 'Reserved': 3}
        compute_method = None
        length = 3
        startbit = 15
        byte = 1
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class BLEConRPACtrlFrnt:
        sig_name = "BLEConRPACtrlFrnt"
        sig_start_bit = 5
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoRequest': 0, 'Touch': 1, 'Release': 2, 'Reserved': 3}
        compute_method = None
        length = 3
        startbit = 5
        byte = 0
        mask = 0b00111000
        unmask = 0b11000111
        shift = 3


class TcamConnectivityFr03:
    msg_name = "TcamConnectivityFr03"
    msg_id = 837
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class TelmSeatPassHeatClimaLvl:
        sig_name = "TelmSeatPassHeatClimaLvl"
        sig_start_bit = 13
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TelmSeatClimaLvl_off': 0, 'TelmSeatClimaLvl_Lvl1': 1, 'TelmSeatClimaLvl_Lvl2': 2, 'TelmSeatClimaLvl_Lvl3': 3}
        compute_method = None
        length = 2
        startbit = 13
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class TelmSeatDrvHeatClimaLvl:
        sig_name = "TelmSeatDrvHeatClimaLvl"
        sig_start_bit = 33
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TelmSeatClimaLvl_off': 0, 'TelmSeatClimaLvl_Lvl1': 1, 'TelmSeatClimaLvl_Lvl2': 2, 'TelmSeatClimaLvl_Lvl3': 3}
        compute_method = None
        length = 2
        startbit = 33
        byte = 4
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class TelmSeatSecLeHeatClimaLvl:
        sig_name = "TelmSeatSecLeHeatClimaLvl"
        sig_start_bit = 21
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TelmSeatClimaLvl_off': 0, 'TelmSeatClimaLvl_Lvl1': 1, 'TelmSeatClimaLvl_Lvl2': 2, 'TelmSeatClimaLvl_Lvl3': 3}
        compute_method = None
        length = 2
        startbit = 21
        byte = 2
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class TelmFctReq:
        sig_name = "TelmFctReq"
        sig_start_bit = 27
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class TelmSeatPassVentnClimaLvl:
        sig_name = "TelmSeatPassVentnClimaLvl"
        sig_start_bit = 23
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TelmSeatClimaLvl_off': 0, 'TelmSeatClimaLvl_Lvl1': 1, 'TelmSeatClimaLvl_Lvl2': 2, 'TelmSeatClimaLvl_Lvl3': 3}
        compute_method = None
        length = 2
        startbit = 23
        byte = 2
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class SteerWhlHeatgDurgClimaEnadFromTelm:
        sig_name = "SteerWhlHeatgDurgClimaEnadFromTelm"
        sig_start_bit = 11
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 11
        byte = 1
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class EngPermitReqFromTelm:
        sig_name = "EngPermitReqFromTelm"
        sig_start_bit = 41
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ReqSts1_NotReqd': 0, 'ReqSts1_Reqd': 1}
        compute_method = None
        length = 1
        startbit = 41
        byte = 5
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class TelmSeatSecRiVentnClimaLvl:
        sig_name = "TelmSeatSecRiVentnClimaLvl"
        sig_start_bit = 29
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TelmSeatClimaLvl_off': 0, 'TelmSeatClimaLvl_Lvl1': 1, 'TelmSeatClimaLvl_Lvl2': 2, 'TelmSeatClimaLvl_Lvl3': 3}
        compute_method = None
        length = 2
        startbit = 29
        byte = 3
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class TelmSeatSecLeVentnClimaLvl:
        sig_name = "TelmSeatSecLeVentnClimaLvl"
        sig_start_bit = 19
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TelmSeatClimaLvl_off': 0, 'TelmSeatClimaLvl_Lvl1': 1, 'TelmSeatClimaLvl_Lvl2': 2, 'TelmSeatClimaLvl_Lvl3': 3}
        compute_method = None
        length = 2
        startbit = 19
        byte = 2
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class EngForbidReqFromTelm:
        sig_name = "EngForbidReqFromTelm"
        sig_start_bit = 40
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ReqSts1_NotReqd': 0, 'ReqSts1_Reqd': 1}
        compute_method = None
        length = 1
        startbit = 40
        byte = 5
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class TelmSeatDrvVentnClimaLvl:
        sig_name = "TelmSeatDrvVentnClimaLvl"
        sig_start_bit = 15
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TelmSeatClimaLvl_off': 0, 'TelmSeatClimaLvl_Lvl1': 1, 'TelmSeatClimaLvl_Lvl2': 2, 'TelmSeatClimaLvl_Lvl3': 3}
        compute_method = None
        length = 2
        startbit = 15
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class RemVentReq:
        sig_name = "RemVentReq"
        sig_start_bit = 26
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffNoReq_NoReq': 0, 'OnOffNoReq_On': 1, 'OnOffNoReq_Off': 2}
        compute_method = None
        length = 2
        startbit = 26
        byte = 3
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class TelmSeatSecRiHeatClimaLvl:
        sig_name = "TelmSeatSecRiHeatClimaLvl"
        sig_start_bit = 31
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TelmSeatClimaLvl_off': 0, 'TelmSeatClimaLvl_Lvl1': 1, 'TelmSeatClimaLvl_Lvl2': 2, 'TelmSeatClimaLvl_Lvl3': 3}
        compute_method = None
        length = 2
        startbit = 31
        byte = 3
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class BncmConnectivityFr13:
    msg_name = "BncmConnectivityFr13"
    msg_id = 20
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class DigKeyIDFndOutStsByte1:
        sig_name = "DigKeyIDFndOutStsByte1"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DigKeyIDFndOutStsByte4:
        sig_name = "DigKeyIDFndOutStsByte4"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DigKeyIDFndOutStsByte3:
        sig_name = "DigKeyIDFndOutStsByte3"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DigKeyIDFndOutStsByte5:
        sig_name = "DigKeyIDFndOutStsByte5"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DigKeyIDFndOutStsDigKeyOutSearchSts:
        sig_name = "DigKeyIDFndOutStsDigKeyOutSearchSts"
        sig_start_bit = 2
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 6
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DigKeyOutSearchSts_Idle': 0, 'DigKeyOutSearchSts_InProgs': 1, 'DigKeyOutSearchSts_Fnd': 2, 'DigKeyOutSearchSts_NotPrsnt': 3, 'DigKeyOutSearchSts_LeftFnd': 4, 'DigKeyOutSearchSts_RightFnd': 5, 'DigKeyOutSearchSts_RearFnd': 6}
        compute_method = None
        length = 3
        startbit = 2
        byte = 0
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class DigKeyIDFndOutStsByte6:
        sig_name = "DigKeyIDFndOutStsByte6"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DigKeyIDFndOutStsByte2:
        sig_name = "DigKeyIDFndOutStsByte2"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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


class VgmConnFr27:
    msg_name = "VgmConnFr27"
    msg_id = 1093
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DigKeyForNfcGidInfo2Byte5:
        sig_name = "DigKeyForNfcGidInfo2Byte5"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 32
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyForNfcGidInfo2Byte6:
        sig_name = "DigKeyForNfcGidInfo2Byte6"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 32
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyForNfcGidInfo2Byte2:
        sig_name = "DigKeyForNfcGidInfo2Byte2"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 32
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 23
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyForNfcGidInfo2Byte7:
        sig_name = "DigKeyForNfcGidInfo2Byte7"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 32
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyForNfcGidInfo2Byte1:
        sig_name = "DigKeyForNfcGidInfo2Byte1"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 32
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyForNfcGidInfo2Byte0:
        sig_name = "DigKeyForNfcGidInfo2Byte0"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 32
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyForNfcGidInfo2Byte3:
        sig_name = "DigKeyForNfcGidInfo2Byte3"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 32
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyForNfcGidInfo2Byte4:
        sig_name = "DigKeyForNfcGidInfo2Byte4"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 32
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class VgmConnFr14:
    msg_name = "VgmConnFr14"
    msg_id = 864
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.155
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class SeatVentnLvlStsRowSecRi:
        sig_name = "SeatVentnLvlStsRowSecRi"
        sig_start_bit = 33
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SeatClimaLvl_Off': 0, 'SeatClimaLvl_Lvl1': 1, 'SeatClimaLvl_Lvl2': 2, 'SeatClimaLvl_Lvl3': 3}
        compute_method = None
        length = 2
        startbit = 33
        byte = 4
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class DrvrSeatVentnLvlSts:
        sig_name = "DrvrSeatVentnLvlSts"
        sig_start_bit = 39
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SeatClimaLvl_Off': 0, 'SeatClimaLvl_Lvl1': 1, 'SeatClimaLvl_Lvl2': 2, 'SeatClimaLvl_Lvl3': 3}
        compute_method = None
        length = 2
        startbit = 39
        byte = 4
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class DrvrSeatHeatgLvlSts:
        sig_name = "DrvrSeatHeatgLvlSts"
        sig_start_bit = 1
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SeatClimaLvl_Off': 0, 'SeatClimaLvl_Lvl1': 1, 'SeatClimaLvl_Lvl2': 2, 'SeatClimaLvl_Lvl3': 3}
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class TrSts:
        sig_name = "TrSts"
        sig_start_bit = 47
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorSts2_Ukwn': 0, 'DoorSts2_Opend': 1, 'DoorSts2_Clsd': 2}
        compute_method = None
        length = 2
        startbit = 47
        byte = 5
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class PassSeatHeatgLvlSts:
        sig_name = "PassSeatHeatgLvlSts"
        sig_start_bit = 9
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SeatClimaLvl_Off': 0, 'SeatClimaLvl_Lvl1': 1, 'SeatClimaLvl_Lvl2': 2, 'SeatClimaLvl_Lvl3': 3}
        compute_method = None
        length = 2
        startbit = 9
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class PassSeatHeatgAvlSts:
        sig_name = "PassSeatHeatgAvlSts"
        sig_start_bit = 4
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'StsFd_None': 0, 'StsFd_On': 1, 'StsFd_Off': 2, 'StsFd_Error': 3, 'StsFd_Functionallimit': 4, 'StsFd_Energylimit': 5, 'StsFd_Resvd1': 6, 'StsFd_Resvd2': 7}
        compute_method = None
        length = 3
        startbit = 4
        byte = 0
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class DrvrSeatVentAvlSts:
        sig_name = "DrvrSeatVentAvlSts"
        sig_start_bit = 23
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'StsFd_None': 0, 'StsFd_On': 1, 'StsFd_Off': 2, 'StsFd_Error': 3, 'StsFd_Functionallimit': 4, 'StsFd_Energylimit': 5, 'StsFd_Resvd1': 6, 'StsFd_Resvd2': 7}
        compute_method = None
        length = 3
        startbit = 23
        byte = 2
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class EcoClimaSts:
        sig_name = "EcoClimaSts"
        sig_start_bit = 45
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 45
        byte = 5
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class PassSeatVentnLvlSts:
        sig_name = "PassSeatVentnLvlSts"
        sig_start_bit = 37
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SeatClimaLvl_Off': 0, 'SeatClimaLvl_Lvl1': 1, 'SeatClimaLvl_Lvl2': 2, 'SeatClimaLvl_Lvl3': 3}
        compute_method = None
        length = 2
        startbit = 37
        byte = 4
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class DrvrSeatHeatgAvlSts:
        sig_name = "DrvrSeatHeatgAvlSts"
        sig_start_bit = 7
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'StsFd_None': 0, 'StsFd_On': 1, 'StsFd_Off': 2, 'StsFd_Error': 3, 'StsFd_Functionallimit': 4, 'StsFd_Energylimit': 5, 'StsFd_Resvd1': 6, 'StsFd_Resvd2': 7}
        compute_method = None
        length = 3
        startbit = 7
        byte = 0
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class PassSeatVentAvlSts:
        sig_name = "PassSeatVentAvlSts"
        sig_start_bit = 20
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'StsFd_None': 0, 'StsFd_On': 1, 'StsFd_Off': 2, 'StsFd_Error': 3, 'StsFd_Functionallimit': 4, 'StsFd_Energylimit': 5, 'StsFd_Resvd1': 6, 'StsFd_Resvd2': 7}
        compute_method = None
        length = 3
        startbit = 20
        byte = 2
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2


class BgmConnectivityFr05:
    msg_name = "BgmConnectivityFr05"
    msg_id = 373
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "BGM"
    rx_nodes = []

    class DigKeyBLEResp3:
        sig_name = "DigKeyBLEResp3"
        sig_start_bit = 0
        sig_length = 512
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = None
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 512
        startbit = 0
        bmuws_info = [(0, 0b00000001, 0b11111110, 1, 0), (1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111111, 0b00000000, 8, 0), (8, 0b11111111, 0b00000000, 8, 0), (9, 0b11111111, 0b00000000, 8, 0), (10, 0b11111111, 0b00000000, 8, 0), (11, 0b11111111, 0b00000000, 8, 0), (12, 0b11111111, 0b00000000, 8, 0), (13, 0b11111111, 0b00000000, 8, 0), (14, 0b11111111, 0b00000000, 8, 0), (15, 0b11111111, 0b00000000, 8, 0), (16, 0b11111111, 0b00000000, 8, 0), (17, 0b11111111, 0b00000000, 8, 0), (18, 0b11111111, 0b00000000, 8, 0), (19, 0b11111111, 0b00000000, 8, 0), (20, 0b11111111, 0b00000000, 8, 0), (21, 0b11111111, 0b00000000, 8, 0), (22, 0b11111111, 0b00000000, 8, 0), (23, 0b11111111, 0b00000000, 8, 0), (24, 0b11111111, 0b00000000, 8, 0), (25, 0b11111111, 0b00000000, 8, 0), (26, 0b11111111, 0b00000000, 8, 0), (27, 0b11111111, 0b00000000, 8, 0), (28, 0b11111111, 0b00000000, 8, 0), (29, 0b11111111, 0b00000000, 8, 0), (30, 0b11111111, 0b00000000, 8, 0), (31, 0b11111111, 0b00000000, 8, 0), (32, 0b11111111, 0b00000000, 8, 0), (33, 0b11111111, 0b00000000, 8, 0), (34, 0b11111111, 0b00000000, 8, 0), (35, 0b11111111, 0b00000000, 8, 0), (36, 0b11111111, 0b00000000, 8, 0), (37, 0b11111111, 0b00000000, 8, 0), (38, 0b11111111, 0b00000000, 8, 0), (39, 0b11111111, 0b00000000, 8, 0), (40, 0b11111111, 0b00000000, 8, 0), (41, 0b11111111, 0b00000000, 8, 0), (42, 0b11111111, 0b00000000, 8, 0), (43, 0b11111111, 0b00000000, 8, 0), (44, 0b11111111, 0b00000000, 8, 0), (45, 0b11111111, 0b00000000, 8, 0), (46, 0b11111111, 0b00000000, 8, 0), (47, 0b11111111, 0b00000000, 8, 0), (48, 0b11111111, 0b00000000, 8, 0), (49, 0b11111111, 0b00000000, 8, 0), (50, 0b11111111, 0b00000000, 8, 0), (51, 0b11111111, 0b00000000, 8, 0), (52, 0b11111111, 0b00000000, 8, 0), (53, 0b11111111, 0b00000000, 8, 0), (54, 0b11111111, 0b00000000, 8, 0), (55, 0b11111111, 0b00000000, 8, 0), (56, 0b11111111, 0b00000000, 8, 0), (57, 0b11111111, 0b00000000, 8, 0), (58, 0b11111111, 0b00000000, 8, 0), (59, 0b11111111, 0b00000000, 8, 0), (60, 0b11111111, 0b00000000, 8, 0), (61, 0b11111111, 0b00000000, 8, 0), (62, 0b11111111, 0b00000000, 8, 0), (63, 0b11111111, 0b00000000, 8, 0), (64, 0b11111110, 0b00000001, 7, 1)]


class BncmToBgmConnectivityDiagRespFrame:
    msg_name = "BncmToBgmConnectivityDiagRespFrame"
    msg_id = 1571
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']


