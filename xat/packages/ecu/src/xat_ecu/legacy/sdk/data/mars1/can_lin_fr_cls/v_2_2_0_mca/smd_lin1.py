lin_scheduleTable = {'FM_Diagnostics_SMD_LIN1': [(0, 'DiagRequest8', 0.015), (1, 'DiagResponse8', 0.015)], 'Smd_Lin1ScheduleTable1': [(0, 'MmdSmd_Lin1Fr01', 0.005), (1, 'SmdSmd_Lin1Fr01', 0.01)], 'Smd_Lin1ScheduleSerNrPartNr': [(0, 'MmdSmd_Lin1PartNrFr01', 0.01), (1, 'MmdSmd_Lin1PartNrFr02', 0.015)]}


class MmdSmd_Lin1PartNrFr02:
    msg_name = "MmdSmd_Lin1PartNrFr02"
    msg_id = 7
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "MMD"
    rx_nodes = ['SMD']
    sig_group_dict = {'MMDPartNo10Cmpl': ['MMDPartNo10CmplEndSgn1', 'MMDPartNo10CmplEndSgn2', 'MMDPartNo10CmplEndSgn3', 'MMDPartNo10CmplNr1', 'MMDPartNo10CmplNr2', 'MMDPartNo10CmplNr3', 'MMDPartNo10CmplNr4', 'MMDPartNo10CmplNr5']}
    sig_group_dataid_dict = {}

    class MMDPartNo10CmplNr2:
        sig_name = "MMDPartNo10CmplNr2"
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

    class MMDPartNo10CmplNr3:
        sig_name = "MMDPartNo10CmplNr3"
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

    class MMDPartNo10CmplNr4:
        sig_name = "MMDPartNo10CmplNr4"
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

    class MMDPartNo10CmplEndSgn2:
        sig_name = "MMDPartNo10CmplEndSgn2"
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

    class MMDPartNo10CmplEndSgn1:
        sig_name = "MMDPartNo10CmplEndSgn1"
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

    class MMDPartNo10CmplNr5:
        sig_name = "MMDPartNo10CmplNr5"
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

    class MMDPartNo10CmplEndSgn3:
        sig_name = "MMDPartNo10CmplEndSgn3"
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

    class MMDPartNo10CmplNr1:
        sig_name = "MMDPartNo10CmplNr1"
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


class DiagResponse5:
    msg_name = "DiagResponse5"
    msg_id = 61
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['SMD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class MmdSmd_Lin1Fr01:
    msg_name = "MmdSmd_Lin1Fr01"
    msg_id = 1
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 1
    tx_node = "MMD"
    rx_nodes = ['SMD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class SeatMassgRunngDrvr:
        sig_name = "SeatMassgRunngDrvr"
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

    class SeatMassgFltStsForEcuDrvr:
        sig_name = "SeatMassgFltStsForEcuDrvr"
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
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 2
        byte = 0
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class SeatMassgSlvAutMovmtDrvr:
        sig_name = "SeatMassgSlvAutMovmtDrvr"
        sig_start_bit = 5
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
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class SeatMassgBackBlstrFailrDrvr:
        sig_name = "SeatMassgBackBlstrFailrDrvr"
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
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 0
        byte = 0
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class SeatMassgCmftHwFailrDrvr:
        sig_name = "SeatMassgCmftHwFailrDrvr"
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
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class SeatMassgPnmFailrDrvr:
        sig_name = "SeatMassgPnmFailrDrvr"
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
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 3
        byte = 0
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class SeatMassgCushBlstrFailrDrvr:
        sig_name = "SeatMassgCushBlstrFailrDrvr"
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
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 1
        byte = 0
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1


class SmdSmd_Lin1Fr01:
    msg_name = "SmdSmd_Lin1Fr01"
    msg_id = 3
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 7
    tx_node = "SMD"
    rx_nodes = ['MMD']
    sig_group_dict = {'SeatMassgFctDrvr': ['SeatMassgFctDrvrMassgInten', 'SeatMassgFctDrvrMassgProg', 'SeatMassgFctDrvrOnOff'], 'SeatMassgLoadAndStoreReqDrvr': ['SeatMassgLoadAndStoreReqDrvrErgoPosn', 'SeatMassgLoadAndStoreReqDrvrErgoSetgEve', 'SeatMassgLoadAndStoreReqDrvrIdPen', 'SeatMassgLoadAndStoreReqDrvrInOutEasy']}
    sig_group_dataid_dict = {}

    class SeatMassgLumMotrEnaDrvr:
        sig_name = "SeatMassgLumMotrEnaDrvr"
        sig_start_bit = 44
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'MotrCfgTyp_NoMotr': 0, 'MotrCfgTyp_MotrWoSnsr': 1, 'MotrCfgTyp_MotrWthSnsr': 2}
        compute_method = None
        length = 2
        startbit = 44
        byte = 5
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class SeatMassgLoadAndStoreReqDrvrInOutEasy:
        sig_name = "SeatMassgLoadAndStoreReqDrvrInOutEasy"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 15
        byte = 1
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class SeatMassgCushBlstrCtrlDrvr:
        sig_name = "SeatMassgCushBlstrCtrlDrvr"
        sig_start_bit = 27
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SwtVertSts1_Idle': 0, 'SwtVertSts1_Up': 1, 'SwtVertSts1_Dwn': 2}
        compute_method = None
        length = 2
        startbit = 27
        byte = 3
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class SeatMassgLoadAndStoreReqDrvrErgoPosn:
        sig_name = "SeatMassgLoadAndStoreReqDrvrErgoPosn"
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
        sig_value_table = {'MemPosn_ProfPosn': 0, 'MemPosn_MemBnk1': 1, 'MemPosn_MemBnk2': 2, 'MemPosn_MemBnk3': 3}
        compute_method = None
        length = 2
        startbit = 16
        byte = 2
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class SeatMassgBackBlstrEnaDrvr:
        sig_name = "SeatMassgBackBlstrEnaDrvr"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 26
        byte = 3
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class SeatMassgLumHeiCtrlDrvr:
        sig_name = "SeatMassgLumHeiCtrlDrvr"
        sig_start_bit = 42
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SwtVertSts1_Idle': 0, 'SwtVertSts1_Up': 1, 'SwtVertSts1_Dwn': 2}
        compute_method = None
        length = 2
        startbit = 42
        byte = 5
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class SeatMassgCushBlstrEnaDrvr:
        sig_name = "SeatMassgCushBlstrEnaDrvr"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 29
        byte = 3
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class SeatMassgBackBlstrCtrlDrvr:
        sig_name = "SeatMassgBackBlstrCtrlDrvr"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SwtHozlSts1_Idle': 0, 'SwtHozlSts1_Fwd': 1, 'SwtHozlSts1_Backw': 2}
        compute_method = None
        length = 2
        startbit = 24
        byte = 3
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class SeatMassgFctDrvrMassgInten:
        sig_name = "SeatMassgFctDrvrMassgInten"
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
        sig_value_table = {'MassgIntenLvl_IntenLo': 0, 'MassgIntenLvl_IntenNorm': 1, 'MassgIntenLvl_IntenHi': 2, 'MassgIntenLvl_Off': 3}
        compute_method = None
        length = 2
        startbit = 0
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class SeatMassgSaveToMemDrvr:
        sig_name = "SeatMassgSaveToMemDrvr"
        sig_start_bit = 46
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OffOnAut1_Off': 0, 'OffOnAut1_On': 1, 'OffOnAut1_Aut': 2}
        compute_method = None
        length = 2
        startbit = 46
        byte = 5
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class SeatMassgLumExtnCtrlDrvr:
        sig_name = "SeatMassgLumExtnCtrlDrvr"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SwtHozlSts1_Idle': 0, 'SwtHozlSts1_Fwd': 1, 'SwtHozlSts1_Backw': 2}
        compute_method = None
        length = 2
        startbit = 40
        byte = 5
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class SeatMassgLoadAndStoreReqDrvrErgoSetgEve:
        sig_name = "SeatMassgLoadAndStoreReqDrvrErgoSetgEve"
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
        sig_value_table = {'EveMemPosn_Idle': 0, 'EveMemPosn_Store': 1, 'EveMemPosn_Load': 2, 'EveMemPosn_Stop': 3, 'EveMemPosn_AutMovmt': 4, 'EveMemPosn_Upload': 5, 'EveMemPosn_Download': 6, 'EveMemPosn_Clear': 7}
        compute_method = None
        length = 3
        startbit = 12
        byte = 1
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class SeatMassgEngPAmbAir1Drvr:
        sig_name = "SeatMassgEngPAmbAir1Drvr"
        sig_start_bit = 32
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 5.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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

    class SeatMassgDiAutCorrnDrvr:
        sig_name = "SeatMassgDiAutCorrnDrvr"
        sig_start_bit = 30
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
        startbit = 30
        byte = 3
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class SeatMassgFctDrvrMassgProg:
        sig_name = "SeatMassgFctDrvrMassgProg"
        sig_start_bit = 2
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'MassgProgTyp_Prog1': 0, 'MassgProgTyp_Prog2': 1, 'MassgProgTyp_Prog3': 2, 'MassgProgTyp_Prog4': 3, 'MassgProgTyp_Prog5': 4, 'MassgProgTyp_Prog6': 5, 'MassgProgTyp_Prog7': 6, 'MassgProgTyp_Prog8': 7}
        compute_method = None
        length = 3
        startbit = 2
        byte = 0
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class SeatMassgLoadAndStoreReqDrvrIdPen:
        sig_name = "SeatMassgLoadAndStoreReqDrvrIdPen"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'IdPen_ProfUkwn': 0, 'IdPen_Prof1': 1, 'IdPen_Prof2': 2, 'IdPen_Prof3': 3, 'IdPen_Prof4': 4, 'IdPen_Prof5': 5, 'IdPen_Prof6': 6, 'IdPen_Prof7': 7, 'IdPen_Prof8': 8, 'IdPen_Prof9': 9, 'IdPen_Prof10': 10, 'IdPen_Prof11': 11, 'IdPen_Prof12': 12, 'IdPen_Prof13': 13, 'IdPen_Resd14': 14, 'IdPen_ProfAll': 15}
        compute_method = None
        length = 4
        startbit = 8
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class SeatMassgFctDrvrOnOff:
        sig_name = "SeatMassgFctDrvrOnOff"
        sig_start_bit = 5
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
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5


class DiagRequest5:
    msg_name = "DiagRequest5"
    msg_id = 60
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "SMD"
    rx_nodes = []
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class MmdSmd_Lin1PartNrFr01:
    msg_name = "MmdSmd_Lin1PartNrFr01"
    msg_id = 6
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 7
    tx_node = "MMD"
    rx_nodes = ['SMD']
    sig_group_dict = {'MMDPartNoCmpl': ['MMDPartNoCmplEndSgn1', 'MMDPartNoCmplEndSgn2', 'MMDPartNoCmplEndSgn3', 'MMDPartNoCmplNr1', 'MMDPartNoCmplNr2', 'MMDPartNoCmplNr3', 'MMDPartNoCmplNr4']}
    sig_group_dataid_dict = {}

    class MMDPartNoCmplNr1:
        sig_name = "MMDPartNoCmplNr1"
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

    class MMDPartNoCmplEndSgn1:
        sig_name = "MMDPartNoCmplEndSgn1"
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

    class MMDPartNoCmplNr4:
        sig_name = "MMDPartNoCmplNr4"
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

    class MMDPartNoCmplNr3:
        sig_name = "MMDPartNoCmplNr3"
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

    class MMDPartNoCmplNr2:
        sig_name = "MMDPartNoCmplNr2"
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

    class MMDPartNoCmplEndSgn3:
        sig_name = "MMDPartNoCmplEndSgn3"
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

    class MMDPartNoCmplEndSgn2:
        sig_name = "MMDPartNoCmplEndSgn2"
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


