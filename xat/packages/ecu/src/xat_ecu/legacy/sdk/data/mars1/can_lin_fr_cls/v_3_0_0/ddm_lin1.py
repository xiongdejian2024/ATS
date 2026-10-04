lin_scheduleTable = {'Ddm_Lin1ScheduleSerNrPartNr': [(0, 'DdsDdm_Lin1PartNrFr05', 0.015), (1, 'DdsDdm_Lin1PartNrFr08', 0.01), (2, 'DdsDdm_Lin1SerNrFr01', 0.01)], 'Ddm_Lin1_DiagResponseSchedule01': [(0, 'DiagResponse8', 0.015)], 'Ddm_Lin1ScheduleTable01': [(0, 'DdmDdm_Lin1Fr01', 0.015), (1, 'DdsDdm_Lin1Fr01', 0.01)], 'Ddm_Lin1_DiagRequestSchedule01': [(0, 'DiagRequest8', 0.015)]}


class DdsDdm_Lin1Fr01:
    msg_name = "DdsDdm_Lin1Fr01"
    msg_id = 54
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 7
    tx_node = "DDS"
    rx_nodes = ['DDM']
    sig_group_dict = {'WinSwtReq': ['WinSwtReqChks', 'WinSwtReqCntr', 'WinSwtReqFrntLe', 'WinSwtReqFrntRi', 'WinSwtReqReLe', 'WinSwtReqReRi']}
    sig_group_dataid_dict = {'WinSwtReq': 1118}

    class MirrDirReq:
        sig_name = "MirrDirReq"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'MirrDirReqTyp_Idle': 0, 'MirrDirReqTyp_Up': 1, 'MirrDirReqTyp_Down': 2, 'MirrDirReqTyp_Left': 3, 'MirrDirReqTyp_Right': 4}
        compute_method = None
        length = 3
        startbit = 0
        byte = 0
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class ChdPrtnLeftSwReq:
        sig_name = "ChdPrtnLeftSwReq"
        sig_start_bit = 6
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
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class WinSwtReqCntr:
        sig_name = "WinSwtReqCntr"
        sig_start_bit = 28
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
        startbit = 28
        byte = 3
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class WinSwtReqFrntRi:
        sig_name = "WinSwtReqFrntRi"
        sig_start_bit = 45
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WinPosnReq_Idle': 0, 'WinPosnReq_UpMan': 1, 'WinPosnReq_UpAut': 2, 'WinPosnReq_DwnMan': 3, 'WinPosnReq_DwnAut': 4, 'WinPosnReq_NotDefd': 5}
        compute_method = None
        length = 3
        startbit = 45
        byte = 5
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class WinSwtReqReLe:
        sig_name = "WinSwtReqReLe"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WinPosnReq_Idle': 0, 'WinPosnReq_UpMan': 1, 'WinPosnReq_UpAut': 2, 'WinPosnReq_DwnMan': 3, 'WinPosnReq_DwnAut': 4, 'WinPosnReq_NotDefd': 5}
        compute_method = None
        length = 3
        startbit = 40
        byte = 5
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class WinSwtReqReRi:
        sig_name = "WinSwtReqReRi"
        sig_start_bit = 48
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WinPosnReq_Idle': 0, 'WinPosnReq_UpMan': 1, 'WinPosnReq_UpAut': 2, 'WinPosnReq_DwnMan': 3, 'WinPosnReq_DwnAut': 4, 'WinPosnReq_NotDefd': 5}
        compute_method = None
        length = 3
        startbit = 48
        byte = 6
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class MirrSelnReq:
        sig_name = "MirrSelnReq"
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
        sig_value_table = {'MirrSelnReqTyp_Idle': 0, 'MirrSelnReqTyp_Le': 1, 'MirrSelnReqTyp_Ri': 2, 'MirrSelnReqTyp_LeAndRi': 3}
        compute_method = None
        length = 2
        startbit = 14
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class ChdPrtnRightSwReq:
        sig_name = "ChdPrtnRightSwReq"
        sig_start_bit = 20
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
        startbit = 20
        byte = 2
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class WinSwtReqFrntLe:
        sig_name = "WinSwtReqFrntLe"
        sig_start_bit = 25
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WinPosnReq_Idle': 0, 'WinPosnReq_UpMan': 1, 'WinPosnReq_UpAut': 2, 'WinPosnReq_DwnMan': 3, 'WinPosnReq_DwnAut': 4, 'WinPosnReq_NotDefd': 5}
        compute_method = None
        length = 3
        startbit = 25
        byte = 3
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class WinSwtReqChks:
        sig_name = "WinSwtReqChks"
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


class DiagRequest5:
    msg_name = "DiagRequest5"
    msg_id = 60
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "DDM"
    rx_nodes = []
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class DdmDdm_Lin1Fr01:
    msg_name = "DdmDdm_Lin1Fr01"
    msg_id = 0
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "DDM"
    rx_nodes = ['DDS']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class ChdPrtnRightLedReq:
        sig_name = "ChdPrtnRightLedReq"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffSafe1_OnOffSafeInvld1': 0, 'OnOffSafe1_OnOffSafeOn': 1, 'OnOffSafe1_OnOffSafeOff': 2, 'OnOffSafe1_OnOffSafeInvld2': 3}
        compute_method = None
        length = 2
        startbit = 8
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class ChdPrtnLeftLedReq:
        sig_name = "ChdPrtnLeftLedReq"
        sig_start_bit = 34
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffSafe1_OnOffSafeInvld1': 0, 'OnOffSafe1_OnOffSafeOn': 1, 'OnOffSafe1_OnOffSafeOff': 2, 'OnOffSafe1_OnOffSafeInvld2': 3}
        compute_method = None
        length = 2
        startbit = 34
        byte = 4
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class IntrBriSts:
        sig_name = "IntrBriSts"
        sig_start_bit = 16
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
        startbit = 16
        byte = 2
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class TwliBriSts:
        sig_name = "TwliBriSts"
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
        sig_value_table = {'TwliBriSts1_Night': 0, 'TwliBriSts1_Day': 1}
        compute_method = None
        length = 1
        startbit = 39
        byte = 4
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ActvnOfDoorSwtIllmn:
        sig_name = "ActvnOfDoorSwtIllmn"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 33
        byte = 4
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VoltLvl:
        sig_name = "VoltLvl"
        sig_start_bit = 29
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 29
        byte = 3
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class MirrSeldIndcn:
        sig_name = "MirrSeldIndcn"
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
        sig_value_table = {'MirrSeldIndcnTyp_LedOff': 0, 'MirrSeldIndcnTyp_LedOnLe': 1, 'MirrSeldIndcnTyp_LedOnRi': 2, 'MirrSeldIndcnTyp_LedOnLeAndRi': 3}
        compute_method = None
        length = 2
        startbit = 24
        byte = 3
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class DoorDrvrIntrSwtLedLockgCmd:
        sig_name = "DoorDrvrIntrSwtLedLockgCmd"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 61
        byte = 7
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5


class DdsDdm_Lin1SerNrFr01:
    msg_name = "DdsDdm_Lin1SerNrFr01"
    msg_id = 47
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "DDS"
    rx_nodes = ['DDM']
    sig_group_dict = {'DDSSerNo': ['DDSSerNoNr1', 'DDSSerNoNr2', 'DDSSerNoNr3', 'DDSSerNoNr4']}
    sig_group_dataid_dict = {}

    class DDSSerNoNr3:
        sig_name = "DDSSerNoNr3"
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

    class DDSSerNoNr4:
        sig_name = "DDSSerNoNr4"
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

    class DDSSerNoNr1:
        sig_name = "DDSSerNoNr1"
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

    class DDSSerNoNr2:
        sig_name = "DDSSerNoNr2"
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


class DdsDdm_Lin1PartNrFr05:
    msg_name = "DdsDdm_Lin1PartNrFr05"
    msg_id = 43
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "DDS"
    rx_nodes = ['DDM']
    sig_group_dict = {'DDSPartNo10Cmpl': ['DDSPartNo10CmplEndSgn1', 'DDSPartNo10CmplEndSgn2', 'DDSPartNo10CmplEndSgn3', 'DDSPartNo10CmplNr1', 'DDSPartNo10CmplNr2', 'DDSPartNo10CmplNr3', 'DDSPartNo10CmplNr4', 'DDSPartNo10CmplNr5']}
    sig_group_dataid_dict = {}

    class DDSPartNo10CmplNr3:
        sig_name = "DDSPartNo10CmplNr3"
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

    class DDSPartNo10CmplNr4:
        sig_name = "DDSPartNo10CmplNr4"
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

    class DDSPartNo10CmplEndSgn2:
        sig_name = "DDSPartNo10CmplEndSgn2"
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

    class DDSPartNo10CmplEndSgn1:
        sig_name = "DDSPartNo10CmplEndSgn1"
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

    class DDSPartNo10CmplNr2:
        sig_name = "DDSPartNo10CmplNr2"
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

    class DDSPartNo10CmplNr5:
        sig_name = "DDSPartNo10CmplNr5"
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

    class DDSPartNo10CmplEndSgn3:
        sig_name = "DDSPartNo10CmplEndSgn3"
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

    class DDSPartNo10CmplNr1:
        sig_name = "DDSPartNo10CmplNr1"
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


class DdsDdm_Lin1PartNrFr08:
    msg_name = "DdsDdm_Lin1PartNrFr08"
    msg_id = 46
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 7
    tx_node = "DDS"
    rx_nodes = ['DDM']
    sig_group_dict = {'DDSPartNoCmpl': ['DDSPartNoCmplEndSgn1', 'DDSPartNoCmplEndSgn2', 'DDSPartNoCmplEndSgn3', 'DDSPartNoCmplNr1', 'DDSPartNoCmplNr2', 'DDSPartNoCmplNr3', 'DDSPartNoCmplNr4']}
    sig_group_dataid_dict = {}

    class DDSPartNoCmplNr4:
        sig_name = "DDSPartNoCmplNr4"
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

    class DDSPartNoCmplEndSgn2:
        sig_name = "DDSPartNoCmplEndSgn2"
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

    class DDSPartNoCmplNr3:
        sig_name = "DDSPartNoCmplNr3"
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

    class DDSPartNoCmplEndSgn3:
        sig_name = "DDSPartNoCmplEndSgn3"
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

    class DDSPartNoCmplNr2:
        sig_name = "DDSPartNoCmplNr2"
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

    class DDSPartNoCmplNr1:
        sig_name = "DDSPartNoCmplNr1"
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

    class DDSPartNoCmplEndSgn1:
        sig_name = "DDSPartNoCmplEndSgn1"
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


class DiagResponse5:
    msg_name = "DiagResponse5"
    msg_id = 61
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['DDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


