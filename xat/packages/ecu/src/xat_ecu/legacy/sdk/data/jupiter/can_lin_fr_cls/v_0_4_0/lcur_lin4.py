lin_scheduleTable = {'LCUR_LIN4ScheduleSerlNrPartNr_LCUR_LIN4': [(0, 'AFULCUR_LIN4Fr01', 0.015), (1, 'AFULCUR_LIN4Fr02', 0.015), (2, 'AGULCUR_LIN4Fr01', 0.015), (3, 'AGULCUR_LIN4Fr02', 0.015), (4, 'MMPLCUR_LIN4Fr01', 0.015), (5, 'MMPLCUR_LIN4Fr02', 0.015), (6, 'PMSILCUR_LIN4Fr01', 0.015), (7, 'PMSILCUR_LIN4Fr02', 0.015), (8, 'RRMMLCUR_LIN4Fr01', 0.015), (9, 'RRMMLCUR_LIN4Fr02', 0.015)], 'LCUR_LIN4_DiagSchedule01': [(0, 'DiagRequest5', 0.015), (1, 'DiagResponse5', 0.015)], 'LCUR_LIN4Schedule01_LCUR_LIN4': [(0, 'AFULCUR_LIN4Fr03', 0.015), (1, 'AFULCUR_LIN4Fr04', 0.015), (2, 'AFULCUR_LIN4Fr05', 0.015), (3, 'AGULCUR_LIN4Fr03', 0.015), (4, 'LCURLCUR_LIN4Fr01', 0.015), (5, 'LCURLCUR_LIN4Fr02', 0.015), (6, 'LCURLCUR_LIN4Fr03', 0.015), (7, 'LCURLCUR_LIN4Fr04', 0.015), (8, 'MMPLCUR_LIN4Fr03', 0.015), (9, 'PMSILCUR_LIN4Fr03', 0.015), (10, 'RRMMLCUR_LIN4Fr03', 0.015)]}


class LCURLCUR_LIN4Fr02:
    msg_name = "LCURLCUR_LIN4Fr02"
    msg_id = 9
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "LCUR"
    rx_nodes = ['RRMM', 'MMP']
    sig_group_dict = {'Odometer': ['OdometerValidity', 'OdometerValue'], 'SeatMassgActReRi': ['SeatMassgActReRiMassgProg', 'SeatMassgActReRiReqLvl'], 'SeatMassgActFrntRi': ['SeatMassgActFrntRiMassgProg', 'SeatMassgActFrntRiReqLvl']}
    sig_group_dataid_dict = {}

    class SeatMassgActFrntRiMassgProg:
        sig_name = "SeatMassgActFrntRiMassgProg"
        sig_start_bit = 32
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'MassgProg_Prog0': 0, 'MassgProg_Prog1': 1, 'MassgProg_Prog2': 2, 'MassgProg_Prog3': 3, 'MassgProg_Prog4': 4, 'MassgProg_Prog5': 5, 'MassgProg_Prog6': 6, 'MassgProg_Prog7': 7}
        compute_method = None
        length = 3
        startbit = 32
        byte = 4
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class SeatLumActReRi:
        sig_name = "SeatLumActReRi"
        sig_start_bit = 27
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SeatDir_Idle': 0, 'SeatDir_Up_Fwd_ReleaseOn': 1, 'SeatDir_Dwn_Backw_ReleaseOff': 2, 'SeatDir_Fault': 3, 'SeatDir_Reserved2': 4, 'SeatDir_Reserved3': 5, 'SeatDir_Reserved4': 6, 'SeatDir_Reserved5': 7}
        compute_method = None
        length = 3
        startbit = 27
        byte = 3
        mask = 0b00111000
        unmask = 0b11000111
        shift = 3

    class VehBattU:
        sig_name = "VehBattU"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.02
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1022
        sig_byteorder = "Intel"
        sig_value_init = 1023
        sig_value_type = "SCALE_LINEAR_AND_TEXTTABLE"
        sig_value_table = {'BattU2_BMSVolWakeUpThd': 1023}
        compute_method = None
        length = 10
        startbit = 40
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b00000011, 0b11111100, 2, 0)]

    class SeatMassgActFrntRiReqLvl:
        sig_name = "SeatMassgActFrntRiReqLvl"
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
        sig_value_table = {'ReqLvl_NoReq': 0, 'ReqLvl_LoReq': 1, 'ReqLvl_MidReq': 2, 'ReqLvl_HiReq': 3}
        compute_method = None
        length = 2
        startbit = 30
        byte = 3
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class OdometerValue:
        sig_name = "OdometerValue"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 21
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 21
        startbit = 0
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0), (2, 0b00011111, 0b11100000, 5, 0)]

    class OdometerValidity:
        sig_name = "OdometerValidity"
        sig_start_bit = 21
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
        startbit = 21
        byte = 2
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class SeatMassgActReRiMassgProg:
        sig_name = "SeatMassgActReRiMassgProg"
        sig_start_bit = 35
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'MassgProg_Prog0': 0, 'MassgProg_Prog1': 1, 'MassgProg_Prog2': 2, 'MassgProg_Prog3': 3, 'MassgProg_Prog4': 4, 'MassgProg_Prog5': 5, 'MassgProg_Prog6': 6, 'MassgProg_Prog7': 7}
        compute_method = None
        length = 3
        startbit = 35
        byte = 4
        mask = 0b00111000
        unmask = 0b11000111
        shift = 3

    class SeatLumActFrntRi:
        sig_name = "SeatLumActFrntRi"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SeatDir_Idle': 0, 'SeatDir_Up_Fwd_ReleaseOn': 1, 'SeatDir_Dwn_Backw_ReleaseOff': 2, 'SeatDir_Fault': 3, 'SeatDir_Reserved2': 4, 'SeatDir_Reserved3': 5, 'SeatDir_Reserved4': 6, 'SeatDir_Reserved5': 7}
        compute_method = None
        length = 3
        startbit = 24
        byte = 3
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class SeatMassgActReRiReqLvl:
        sig_name = "SeatMassgActReRiReqLvl"
        sig_start_bit = 38
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ReqLvl_NoReq': 0, 'ReqLvl_LoReq': 1, 'ReqLvl_MidReq': 2, 'ReqLvl_HiReq': 3}
        compute_method = None
        length = 2
        startbit = 38
        byte = 4
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class RRMMLCUR_LIN4Fr03:
    msg_name = "RRMMLCUR_LIN4Fr03"
    msg_id = 20
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "RRMM"
    rx_nodes = ['LCUR']
    sig_group_dict = {'SeatMassgReRiRunSts': ['SeatMassgReRiRunStsMassgLvlSts', 'SeatMassgReRiRunStsMassgProg', 'SeatMassgReRiRunStsOnOffNoCmd']}
    sig_group_dataid_dict = {}

    class SeatMassgReRiRunStsOnOffNoCmd:
        sig_name = "SeatMassgReRiRunStsOnOffNoCmd"
        sig_start_bit = 6
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffNoCmd_NoCmd': 0, 'OnOffNoCmd_OFF': 1, 'OnOffNoCmd_ON': 2}
        compute_method = None
        length = 2
        startbit = 6
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class SeatMassgEcuReRiErrSts:
        sig_name = "SeatMassgEcuReRiErrSts"
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
        sig_value_table = {'EcuErrorType_Idle': 0, 'EcuErrorType_InternalError': 1, 'EcuErrorType_ExternalError': 2, 'EcuErrorType_reserved': 3}
        compute_method = None
        length = 2
        startbit = 2
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class SeatMassgReRiRunStsMassgLvlSts:
        sig_name = "SeatMassgReRiRunStsMassgLvlSts"
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
        sig_value_table = {'MassgLvlSts_Idle': 0, 'MassgLvlSts_Low': 1, 'MassgLvlSts_Mid': 2, 'MassgLvlSts_High': 3}
        compute_method = None
        length = 2
        startbit = 4
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class SeatLumReRiRunSts:
        sig_name = "SeatLumReRiRunSts"
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
        sig_value_table = {'OffOnNoCmd_NoCmd': 0, 'OffOnNoCmd_Off': 1, 'OffOnNoCmd_On': 2}
        compute_method = None
        length = 2
        startbit = 0
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class SeatMassgReRiRunStsMassgProg:
        sig_name = "SeatMassgReRiRunStsMassgProg"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'MassgProg_Prog0': 0, 'MassgProg_Prog1': 1, 'MassgProg_Prog2': 2, 'MassgProg_Prog3': 3, 'MassgProg_Prog4': 4, 'MassgProg_Prog5': 5, 'MassgProg_Prog6': 6, 'MassgProg_Prog7': 7}
        compute_method = None
        length = 3
        startbit = 8
        byte = 1
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0


class DiagResponse5:
    msg_name = "DiagResponse5"
    msg_id = 61
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['LCUR']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class AFULCUR_LIN4Fr03:
    msg_name = "AFULCUR_LIN4Fr03"
    msg_id = 2
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "AFU"
    rx_nodes = ['LCUR']
    sig_group_dict = {'AFUCh2Sts': ['AFUCh2StsAvlTi', 'AFUCh2StsChgSts', 'AFUCh2StsMotErr', 'AFUCh2StsRelsRatFb', 'AFUCh2StsRunngSts', 'AFUCh2StsTyp'], 'AFUCh1Sts': ['AFUCh1StsAvlTi', 'AFUCh1StsChgSts', 'AFUCh1StsMotErr', 'AFUCh1StsRelsRatFb', 'AFUCh1StsRunngSts', 'AFUCh1StsTyp']}
    sig_group_dataid_dict = {}

    class AFUActPwr:
        sig_name = "AFUActPwr"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 0
        byte = 0
        mask = 0b00111111
        unmask = 0b11000000
        shift = 0

    class AFUCh2StsMotErr:
        sig_name = "AFUCh2StsMotErr"
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
        sig_value_table = {'AirFragMotErr_NoErr': 0, 'AirFragMotErr_Err': 1}
        compute_method = None
        length = 1
        startbit = 36
        byte = 4
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class AFUCh2StsChgSts:
        sig_name = "AFUCh2StsChgSts"
        sig_start_bit = 38
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AirFragChgSts_Initial': 0, 'AirFragChgSts_Changing': 1, 'AirFragChgSts_ChangeSucceeded': 2, 'AirFragChgSts_ChangeFailed': 3}
        compute_method = None
        length = 2
        startbit = 38
        byte = 4
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class AFUCh2StsRelsRatFb:
        sig_name = "AFUCh2StsRelsRatFb"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 7
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 40
        byte = 5
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class AFUCh1StsRunngSts:
        sig_name = "AFUCh1StsRunngSts"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 34
        byte = 4
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class AFUCh1StsAvlTi:
        sig_name = "AFUCh1StsAvlTi"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 9
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 7
        bmuws_info = [(0, 0b10000000, 0b01111111, 1, 7), (1, 0b11111111, 0b00000000, 8, 0)]

    class AFUCh1StsRelsRatFb:
        sig_name = "AFUCh1StsRelsRatFb"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 7
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 16
        byte = 2
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class AFUCh1StsTyp:
        sig_name = "AFUCh1StsTyp"
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

    class AFUCh2StsAvlTi:
        sig_name = "AFUCh2StsAvlTi"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 9
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 47
        bmuws_info = [(5, 0b10000000, 0b01111111, 1, 7), (6, 0b11111111, 0b00000000, 8, 0)]

    class AFUCh1StsChgSts:
        sig_name = "AFUCh1StsChgSts"
        sig_start_bit = 32
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AirFragChgSts_Initial': 0, 'AirFragChgSts_Changing': 1, 'AirFragChgSts_ChangeSucceeded': 2, 'AirFragChgSts_ChangeFailed': 3}
        compute_method = None
        length = 2
        startbit = 32
        byte = 4
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class AFUCh2StsRunngSts:
        sig_name = "AFUCh2StsRunngSts"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 37
        byte = 4
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class AFUCh1StsMotErr:
        sig_name = "AFUCh1StsMotErr"
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
        sig_value_table = {'AirFragMotErr_NoErr': 0, 'AirFragMotErr_Err': 1}
        compute_method = None
        length = 1
        startbit = 23
        byte = 2
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class AFUCh2StsTyp:
        sig_name = "AFUCh2StsTyp"
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


class AGULCUR_LIN4Fr02:
    msg_name = "AGULCUR_LIN4Fr02"
    msg_id = 6
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "AGU"
    rx_nodes = ['LCUR']
    sig_group_dict = {'AGUSerNo': ['AGUSerNoNr1', 'AGUSerNoNr2', 'AGUSerNoNr3', 'AGUSerNoNr4']}
    sig_group_dataid_dict = {}

    class AGUSerNoNr2:
        sig_name = "AGUSerNoNr2"
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

    class AGUSerNoNr1:
        sig_name = "AGUSerNoNr1"
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

    class AGUSerNoNr3:
        sig_name = "AGUSerNoNr3"
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

    class AGUSerNoNr4:
        sig_name = "AGUSerNoNr4"
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


class MMPLCUR_LIN4Fr03:
    msg_name = "MMPLCUR_LIN4Fr03"
    msg_id = 14
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "MMP"
    rx_nodes = ['LCUR']
    sig_group_dict = {'SeatMassgFrntRiRunSts': ['SeatMassgFrntRiRunStsMassgLvlSts', 'SeatMassgFrntRiRunStsMassgProg', 'SeatMassgFrntRiRunStsOnOffNoCmd']}
    sig_group_dataid_dict = {}

    class SeatMassgEcuFrntRiErrSts:
        sig_name = "SeatMassgEcuFrntRiErrSts"
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
        sig_value_table = {'EcuErrorType_Idle': 0, 'EcuErrorType_InternalError': 1, 'EcuErrorType_ExternalError': 2, 'EcuErrorType_reserved': 3}
        compute_method = None
        length = 2
        startbit = 2
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class SeatMassgFrntRiRunStsMassgProg:
        sig_name = "SeatMassgFrntRiRunStsMassgProg"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'MassgProg_Prog0': 0, 'MassgProg_Prog1': 1, 'MassgProg_Prog2': 2, 'MassgProg_Prog3': 3, 'MassgProg_Prog4': 4, 'MassgProg_Prog5': 5, 'MassgProg_Prog6': 6, 'MassgProg_Prog7': 7}
        compute_method = None
        length = 3
        startbit = 8
        byte = 1
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class SeatMassgFrntRiRunStsMassgLvlSts:
        sig_name = "SeatMassgFrntRiRunStsMassgLvlSts"
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
        sig_value_table = {'MassgLvlSts_Idle': 0, 'MassgLvlSts_Low': 1, 'MassgLvlSts_Mid': 2, 'MassgLvlSts_High': 3}
        compute_method = None
        length = 2
        startbit = 4
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class SeatMassgFrntRiRunStsOnOffNoCmd:
        sig_name = "SeatMassgFrntRiRunStsOnOffNoCmd"
        sig_start_bit = 6
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffNoCmd_NoCmd': 0, 'OnOffNoCmd_OFF': 1, 'OnOffNoCmd_ON': 2}
        compute_method = None
        length = 2
        startbit = 6
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class SeatLumFrntRiRunSts:
        sig_name = "SeatLumFrntRiRunSts"
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
        sig_value_table = {'OffOnNoCmd_NoCmd': 0, 'OffOnNoCmd_Off': 1, 'OffOnNoCmd_On': 2}
        compute_method = None
        length = 2
        startbit = 0
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0


class MMPLCUR_LIN4Fr02:
    msg_name = "MMPLCUR_LIN4Fr02"
    msg_id = 13
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "MMP"
    rx_nodes = ['LCUR']
    sig_group_dict = {'MMPSerNo': ['MMPSerNoNr1', 'MMPSerNoNr2', 'MMPSerNoNr3', 'MMPSerNoNr4']}
    sig_group_dataid_dict = {}

    class MMPSerNoNr4:
        sig_name = "MMPSerNoNr4"
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

    class MMPSerNoNr1:
        sig_name = "MMPSerNoNr1"
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

    class MMPSerNoNr3:
        sig_name = "MMPSerNoNr3"
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

    class MMPSerNoNr2:
        sig_name = "MMPSerNoNr2"
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


class PMSILCUR_LIN4Fr02:
    msg_name = "PMSILCUR_LIN4Fr02"
    msg_id = 16
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "PMSI"
    rx_nodes = ['LCUR']
    sig_group_dict = {'PMSISerNo': ['PMSISerNoNr1', 'PMSISerNoNr2', 'PMSISerNoNr3', 'PMSISerNoNr4']}
    sig_group_dataid_dict = {}

    class PMSISerNoNr1:
        sig_name = "PMSISerNoNr1"
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

    class PMSISerNoNr2:
        sig_name = "PMSISerNoNr2"
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

    class PMSISerNoNr4:
        sig_name = "PMSISerNoNr4"
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

    class PMSISerNoNr3:
        sig_name = "PMSISerNoNr3"
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


class DiagRequest5:
    msg_name = "DiagRequest5"
    msg_id = 60
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "LCUR"
    rx_nodes = []
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class AFULCUR_LIN4Fr04:
    msg_name = "AFULCUR_LIN4Fr04"
    msg_id = 3
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "AFU"
    rx_nodes = ['LCUR']
    sig_group_dict = {'AFUCh4Sts': ['AFUCh4StsAvlTi', 'AFUCh4StsChgSts', 'AFUCh4StsMotErr', 'AFUCh4StsRelsRatFb', 'AFUCh4StsRunngSts', 'AFUCh4StsTyp'], 'AFUCh3Sts': ['AFUCh3StsAvlTi', 'AFUCh3StsChgSts', 'AFUCh3StsMotErr', 'AFUCh3StsRelsRatFb', 'AFUCh3StsRunngSts', 'AFUCh3StsTyp']}
    sig_group_dataid_dict = {}

    class AFUCh4StsAvlTi:
        sig_name = "AFUCh4StsAvlTi"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 9
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 39
        bmuws_info = [(4, 0b10000000, 0b01111111, 1, 7), (5, 0b11111111, 0b00000000, 8, 0)]

    class AFUCh4StsRunngSts:
        sig_name = "AFUCh4StsRunngSts"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class AFUCh3StsAvlTi:
        sig_name = "AFUCh3StsAvlTi"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 9
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 0
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b00000001, 0b11111110, 1, 0)]

    class AFUCh4StsChgSts:
        sig_name = "AFUCh4StsChgSts"
        sig_start_bit = 28
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AirFragChgSts_Initial': 0, 'AirFragChgSts_Changing': 1, 'AirFragChgSts_ChangeSucceeded': 2, 'AirFragChgSts_ChangeFailed': 3}
        compute_method = None
        length = 2
        startbit = 28
        byte = 3
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class AFUCh3StsMotErr:
        sig_name = "AFUCh3StsMotErr"
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
        sig_value_table = {'AirFragMotErr_NoErr': 0, 'AirFragMotErr_Err': 1}
        compute_method = None
        length = 1
        startbit = 26
        byte = 3
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class AFUCh4StsRelsRatFb:
        sig_name = "AFUCh4StsRelsRatFb"
        sig_start_bit = 32
        update_id_bit = None
        sig_length = 7
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 32
        byte = 4
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class AFUCh3StsRelsRatFb:
        sig_name = "AFUCh3StsRelsRatFb"
        sig_start_bit = 9
        update_id_bit = None
        sig_length = 7
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 9
        byte = 1
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class AFUCh4StsMotErr:
        sig_name = "AFUCh4StsMotErr"
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
        sig_value_table = {'AirFragMotErr_NoErr': 0, 'AirFragMotErr_Err': 1}
        compute_method = None
        length = 1
        startbit = 30
        byte = 3
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class AFUCh3StsChgSts:
        sig_name = "AFUCh3StsChgSts"
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
        sig_value_table = {'AirFragChgSts_Initial': 0, 'AirFragChgSts_Changing': 1, 'AirFragChgSts_ChangeSucceeded': 2, 'AirFragChgSts_ChangeFailed': 3}
        compute_method = None
        length = 2
        startbit = 24
        byte = 3
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class AFUCh3StsRunngSts:
        sig_name = "AFUCh3StsRunngSts"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 27
        byte = 3
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class AFUCh3StsTyp:
        sig_name = "AFUCh3StsTyp"
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

    class AFUCh4StsTyp:
        sig_name = "AFUCh4StsTyp"
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


class PMSILCUR_LIN4Fr01:
    msg_name = "PMSILCUR_LIN4Fr01"
    msg_id = 15
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "PMSI"
    rx_nodes = ['LCUR']
    sig_group_dict = {'PMSIPartNo': ['PMSIPartNoEndSgn1', 'PMSIPartNoEndSgn2', 'PMSIPartNoEndSgn3', 'PMSIPartNoNr1', 'PMSIPartNoNr2', 'PMSIPartNoNr3', 'PMSIPartNoNr4', 'PMSIPartNoNr5']}
    sig_group_dataid_dict = {}

    class PMSIPartNoNr2:
        sig_name = "PMSIPartNoNr2"
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

    class PMSIPartNoNr3:
        sig_name = "PMSIPartNoNr3"
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

    class PMSIPartNoEndSgn2:
        sig_name = "PMSIPartNoEndSgn2"
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

    class PMSIPartNoNr5:
        sig_name = "PMSIPartNoNr5"
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

    class PMSIPartNoEndSgn1:
        sig_name = "PMSIPartNoEndSgn1"
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

    class PMSIPartNoNr4:
        sig_name = "PMSIPartNoNr4"
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

    class PMSIPartNoEndSgn3:
        sig_name = "PMSIPartNoEndSgn3"
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

    class PMSIPartNoNr1:
        sig_name = "PMSIPartNoNr1"
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


class MMPLCUR_LIN4Fr01:
    msg_name = "MMPLCUR_LIN4Fr01"
    msg_id = 12
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "MMP"
    rx_nodes = ['LCUR']
    sig_group_dict = {'MMPPartNo': ['MMPPartNoEndSgn1', 'MMPPartNoEndSgn2', 'MMPPartNoEndSgn3', 'MMPPartNoNr1', 'MMPPartNoNr2', 'MMPPartNoNr3', 'MMPPartNoNr4', 'MMPPartNoNr5']}
    sig_group_dataid_dict = {}

    class MMPPartNoNr5:
        sig_name = "MMPPartNoNr5"
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

    class MMPPartNoNr3:
        sig_name = "MMPPartNoNr3"
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

    class MMPPartNoNr4:
        sig_name = "MMPPartNoNr4"
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

    class MMPPartNoEndSgn2:
        sig_name = "MMPPartNoEndSgn2"
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

    class MMPPartNoEndSgn1:
        sig_name = "MMPPartNoEndSgn1"
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

    class MMPPartNoNr2:
        sig_name = "MMPPartNoNr2"
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

    class MMPPartNoNr1:
        sig_name = "MMPPartNoNr1"
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

    class MMPPartNoEndSgn3:
        sig_name = "MMPPartNoEndSgn3"
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


class AFULCUR_LIN4Fr01:
    msg_name = "AFULCUR_LIN4Fr01"
    msg_id = 0
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "AFU"
    rx_nodes = ['LCUR']
    sig_group_dict = {'AFUPartNo': ['AFUPartNoEndSgn1', 'AFUPartNoEndSgn2', 'AFUPartNoEndSgn3', 'AFUPartNoNr1', 'AFUPartNoNr2', 'AFUPartNoNr3', 'AFUPartNoNr4', 'AFUPartNoNr5']}
    sig_group_dataid_dict = {}

    class AFUPartNoNr2:
        sig_name = "AFUPartNoNr2"
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

    class AFUPartNoNr4:
        sig_name = "AFUPartNoNr4"
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

    class AFUPartNoNr5:
        sig_name = "AFUPartNoNr5"
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

    class AFUPartNoNr1:
        sig_name = "AFUPartNoNr1"
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

    class AFUPartNoEndSgn1:
        sig_name = "AFUPartNoEndSgn1"
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

    class AFUPartNoEndSgn2:
        sig_name = "AFUPartNoEndSgn2"
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

    class AFUPartNoEndSgn3:
        sig_name = "AFUPartNoEndSgn3"
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

    class AFUPartNoNr3:
        sig_name = "AFUPartNoNr3"
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


class RRMMLCUR_LIN4Fr01:
    msg_name = "RRMMLCUR_LIN4Fr01"
    msg_id = 18
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "RRMM"
    rx_nodes = ['LCUR']
    sig_group_dict = {'RRMMPartNo': ['RRMMPartNoEndSgn1', 'RRMMPartNoEndSgn2', 'RRMMPartNoEndSgn3', 'RRMMPartNoNr1', 'RRMMPartNoNr2', 'RRMMPartNoNr3', 'RRMMPartNoNr4', 'RRMMPartNoNr5']}
    sig_group_dataid_dict = {}

    class RRMMPartNoEndSgn3:
        sig_name = "RRMMPartNoEndSgn3"
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

    class RRMMPartNoEndSgn2:
        sig_name = "RRMMPartNoEndSgn2"
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

    class RRMMPartNoNr2:
        sig_name = "RRMMPartNoNr2"
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

    class RRMMPartNoNr1:
        sig_name = "RRMMPartNoNr1"
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

    class RRMMPartNoNr4:
        sig_name = "RRMMPartNoNr4"
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

    class RRMMPartNoNr5:
        sig_name = "RRMMPartNoNr5"
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

    class RRMMPartNoNr3:
        sig_name = "RRMMPartNoNr3"
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

    class RRMMPartNoEndSgn1:
        sig_name = "RRMMPartNoEndSgn1"
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


class AGULCUR_LIN4Fr01:
    msg_name = "AGULCUR_LIN4Fr01"
    msg_id = 5
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "AGU"
    rx_nodes = ['LCUR']
    sig_group_dict = {'AGUPartNo': ['AGUPartNoEndSgn1', 'AGUPartNoEndSgn2', 'AGUPartNoEndSgn3', 'AGUPartNoNr1', 'AGUPartNoNr2', 'AGUPartNoNr3', 'AGUPartNoNr4', 'AGUPartNoNr5']}
    sig_group_dataid_dict = {}

    class AGUPartNoNr1:
        sig_name = "AGUPartNoNr1"
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

    class AGUPartNoNr4:
        sig_name = "AGUPartNoNr4"
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

    class AGUPartNoEndSgn3:
        sig_name = "AGUPartNoEndSgn3"
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

    class AGUPartNoEndSgn1:
        sig_name = "AGUPartNoEndSgn1"
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

    class AGUPartNoEndSgn2:
        sig_name = "AGUPartNoEndSgn2"
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

    class AGUPartNoNr3:
        sig_name = "AGUPartNoNr3"
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

    class AGUPartNoNr5:
        sig_name = "AGUPartNoNr5"
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

    class AGUPartNoNr2:
        sig_name = "AGUPartNoNr2"
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


class PMSILCUR_LIN4Fr03:
    msg_name = "PMSILCUR_LIN4Fr03"
    msg_id = 17
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "PMSI"
    rx_nodes = ['LCUR']
    sig_group_dict = {'InsdAirPM25Sts': ['InsdAirPM25StsElecErr', 'InsdAirPM25StsFanErr', 'InsdAirPM25StsIntErr', 'InsdAirPM25StsRunngSts', 'InsdAirPM25StsTempErr', 'InsdAirPM25StsVoltErr']}
    sig_group_dataid_dict = {}

    class InsdAirPM25StsVoltErr:
        sig_name = "InsdAirPM25StsVoltErr"
        sig_start_bit = 21
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VoltErr_Normal': 0, 'VoltErr_UnderVolt': 1, 'VoltErr_OverVolt': 2, 'VoltErr_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 21
        byte = 2
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class InsdAirPM25StsElecErr:
        sig_name = "InsdAirPM25StsElecErr"
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
        sig_value_table = {'ElecErr_Normal': 0, 'ElecErr_ShortToGroundOrOpenCircuit': 1, 'ElecErr_ShortToBatt': 2, 'ElecErr_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 10
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class InsdAirPM25StsRunngSts:
        sig_name = "InsdAirPM25StsRunngSts"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PM25RunngSts_Initial': 0, 'PM25RunngSts_Collecting': 1, 'PM25RunngSts_Complete': 2, 'PM25RunngSts_Error': 3}
        compute_method = None
        length = 3
        startbit = 16
        byte = 2
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class InsdAirPM25StsIntErr:
        sig_name = "InsdAirPM25StsIntErr"
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
        sig_value_table = {'PM25IntErr_False': 0, 'PM25IntErr_True': 1, 'PM25IntErr_Reserved': 2, 'PM25IntErr_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 14
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class InsdAirPM25StsFanErr:
        sig_name = "InsdAirPM25StsFanErr"
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
        sig_value_table = {'PM25FanErr_NoErr': 0, 'PM25FanErr_SpeedUnstable': 1, 'PM25FanErr_PoorContact': 2, 'PM25FanErr_BrokenLine': 3}
        compute_method = None
        length = 2
        startbit = 12
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class InsdAirPM25Dens:
        sig_name = "InsdAirPM25Dens"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 10
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 0
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b00000011, 0b11111100, 2, 0)]

    class InsdAirPM25StsTempErr:
        sig_name = "InsdAirPM25StsTempErr"
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
        sig_value_table = {'TempErr_Normal': 0, 'TempErr_OverTemp': 1, 'TempErr_UnderTemp': 2, 'TempErr_Invalid': 3}
        compute_method = None
        length = 2
        startbit = 19
        byte = 2
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3


class AFULCUR_LIN4Fr02:
    msg_name = "AFULCUR_LIN4Fr02"
    msg_id = 1
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "AFU"
    rx_nodes = ['LCUR']
    sig_group_dict = {'AFUSerNo': ['AFUSerNoNr1', 'AFUSerNoNr2', 'AFUSerNoNr3', 'AFUSerNoNr4']}
    sig_group_dataid_dict = {}

    class AFUSerNoNr1:
        sig_name = "AFUSerNoNr1"
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

    class AFUSerNoNr4:
        sig_name = "AFUSerNoNr4"
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

    class AFUSerNoNr3:
        sig_name = "AFUSerNoNr3"
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

    class AFUSerNoNr2:
        sig_name = "AFUSerNoNr2"
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


class LCURLCUR_LIN4Fr04:
    msg_name = "LCURLCUR_LIN4Fr04"
    msg_id = 11
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "LCUR"
    rx_nodes = ['RRMM']
    sig_group_dict = {'VMMGlbSig': ['VMMGlbSigCarModSts', 'VMMGlbSigChks', 'VMMGlbSigCntr', 'VMMGlbSigCnvincSubSts1', 'VMMGlbSigDrvgSubSts1', 'VMMGlbSigInactvSubSts1', 'VMMGlbSigLoBattModSts', 'VMMGlbSigUsgModSts']}
    sig_group_dataid_dict = {'VMMGlbSig': 1074}

    class VMMGlbSigLoBattModSts:
        sig_name = "VMMGlbSigLoBattModSts"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 40
        byte = 5
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VMMGlbSigCarModSts:
        sig_name = "VMMGlbSigCarModSts"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 8
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CarModStsType_CarModNorm': 0, 'CarModStsType_CarModTrnsp': 1, 'CarModStsType_CarModFcy': 2, 'CarModStsType_CarModExhib': 3, 'CarModStsType_CarModCrash': 8}
        compute_method = None
        length = 4
        startbit = 0
        byte = 0
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class VMMGlbSigChks:
        sig_name = "VMMGlbSigChks"
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

    class VMMGlbSigUsgModSts:
        sig_name = "VMMGlbSigUsgModSts"
        sig_start_bit = 41
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 13
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'UsgModSts1_UsgModAbdnd': 0, 'UsgModSts1_UsgModInActv': 1, 'UsgModSts1_UsgModCnvinc': 2, 'UsgModSts1_UsgModDrvg': 13}
        compute_method = None
        length = 4
        startbit = 41
        byte = 5
        mask = 0b00011110
        unmask = 0b11100001
        shift = 1

    class VMMGlbSigInactvSubSts1:
        sig_name = "VMMGlbSigInactvSubSts1"
        sig_start_bit = 32
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'InactvSubSts_Invalid': 0, 'InactvSubSts_Awake': 1, 'InactvSubSts_UserPresent': 2}
        compute_method = None
        length = 8
        startbit = 32
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VMMGlbSigDrvgSubSts1:
        sig_name = "VMMGlbSigDrvgSubSts1"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DrvgSubSts_Invalid': 0, 'DrvgSubSts_Manual': 1, 'DrvgSubSts_Automatic': 2, 'DrvgSubSts_NoTorque': 3}
        compute_method = None
        length = 8
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VMMGlbSigCnvincSubSts1:
        sig_name = "VMMGlbSigCnvincSubSts1"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CnvincSubSts_Invalid': 0, 'CnvincSubSts_EnterExit': 1, 'CnvincSubSts_AllDoorClosed': 2}
        compute_method = None
        length = 8
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VMMGlbSigCntr:
        sig_name = "VMMGlbSigCntr"
        sig_start_bit = 4
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
        startbit = 4
        byte = 0
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4


class LCURLCUR_LIN4Fr01:
    msg_name = "LCURLCUR_LIN4Fr01"
    msg_id = 8
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "LCUR"
    rx_nodes = ['PMSI', 'AFU', 'AGU']
    sig_group_dict = {'AFUOnOffReq': ['AFUOnOffReqCh1', 'AFUOnOffReqCh2', 'AFUOnOffReqCh3', 'AFUOnOffReqCh4', 'AFUOnOffReqCh5'], 'AFURelsRatReq': ['AFURelsRatReqCh1', 'AFURelsRatReqCh2', 'AFURelsRatReqCh3', 'AFURelsRatReqCh4', 'AFURelsRatReqCh5']}
    sig_group_dataid_dict = {}

    class AFUOnOffReqCh3:
        sig_name = "AFUOnOffReqCh3"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 3
        byte = 0
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class AFUOnOffReqCh4:
        sig_name = "AFUOnOffReqCh4"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 4
        byte = 0
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class AFURelsLvlReq:
        sig_name = "AFURelsLvlReq"
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
        sig_value_table = {'ReqLvl_NoReq': 0, 'ReqLvl_LoReq': 1, 'ReqLvl_MidReq': 2, 'ReqLvl_HiReq': 3}
        compute_method = None
        length = 2
        startbit = 6
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class AFURelsRatReqCh4:
        sig_name = "AFURelsRatReqCh4"
        sig_start_bit = 32
        update_id_bit = None
        sig_length = 7
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 32
        byte = 4
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class InsdAirPM25ActvCmd:
        sig_name = "InsdAirPM25ActvCmd"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 48
        byte = 6
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class AFURelsRatReqCh1:
        sig_name = "AFURelsRatReqCh1"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 7
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 8
        byte = 1
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class AFUOnOffReqCh1:
        sig_name = "AFUOnOffReqCh1"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 1
        byte = 0
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class AFUOnOffReqCh2:
        sig_name = "AFUOnOffReqCh2"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 2
        byte = 0
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class AFURelsRatReqCh3:
        sig_name = "AFURelsRatReqCh3"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 7
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 24
        byte = 3
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class AFURelsRatReqCh2:
        sig_name = "AFURelsRatReqCh2"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 7
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 16
        byte = 2
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class AFURelsRatReqCh5:
        sig_name = "AFURelsRatReqCh5"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 7
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 40
        byte = 5
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class AFUOnOffReqCh5:
        sig_name = "AFUOnOffReqCh5"
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

    class AFUActvCmd:
        sig_name = "AFUActvCmd"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 0
        byte = 0
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class AGUActvCmd:
        sig_name = "AGUActvCmd"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7


class AGULCUR_LIN4Fr03:
    msg_name = "AGULCUR_LIN4Fr03"
    msg_id = 7
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "AGU"
    rx_nodes = ['LCUR']
    sig_group_dict = {'AGUSts': ['AGUStsElecErr', 'AGUStsRunngSts', 'AGUStsVoltErr']}
    sig_group_dataid_dict = {}

    class AGUStsVoltErr:
        sig_name = "AGUStsVoltErr"
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
        sig_value_table = {'VoltErr_Normal': 0, 'VoltErr_UnderVolt': 1, 'VoltErr_OverVolt': 2, 'VoltErr_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 4
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class AGUStsElecErr:
        sig_name = "AGUStsElecErr"
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
        sig_value_table = {'ElecErr_Normal': 0, 'ElecErr_ShortToGroundOrOpenCircuit': 1, 'ElecErr_ShortToBatt': 2, 'ElecErr_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 0
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class AGUStsRunngSts:
        sig_name = "AGUStsRunngSts"
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
        sig_value_table = {'AGURunngSts_Off': 0, 'AGURunngSts_On': 1, 'AGURunngSts_Sleep': 2, 'AGURunngSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 2
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2


class RRMMLCUR_LIN4Fr02:
    msg_name = "RRMMLCUR_LIN4Fr02"
    msg_id = 19
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "RRMM"
    rx_nodes = ['LCUR']
    sig_group_dict = {'RRMMSerNo': ['RRMMSerNoNr1', 'RRMMSerNoNr2', 'RRMMSerNoNr3', 'RRMMSerNoNr4']}
    sig_group_dataid_dict = {}

    class RRMMSerNoNr2:
        sig_name = "RRMMSerNoNr2"
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

    class RRMMSerNoNr1:
        sig_name = "RRMMSerNoNr1"
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

    class RRMMSerNoNr4:
        sig_name = "RRMMSerNoNr4"
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

    class RRMMSerNoNr3:
        sig_name = "RRMMSerNoNr3"
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


class AFULCUR_LIN4Fr05:
    msg_name = "AFULCUR_LIN4Fr05"
    msg_id = 4
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "AFU"
    rx_nodes = ['LCUR']
    sig_group_dict = {'AFUCh5Sts': ['AFUCh5StsAvlTi', 'AFUCh5StsChgSts', 'AFUCh5StsMotErr', 'AFUCh5StsRelsRatFb', 'AFUCh5StsRunngSts', 'AFUCh5StsTyp'], 'AFUCtrlrErr': ['AFUCtrlrErrFan', 'AFUCtrlrErrMemChks', 'AFUCtrlrErrOverVolt', 'AFUCtrlrErrTemp', 'AFUCtrlrErrUnderVolt']}
    sig_group_dataid_dict = {}

    class AFURelsLvlFb:
        sig_name = "AFURelsLvlFb"
        sig_start_bit = 36
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ReqLvl_NoReq': 0, 'ReqLvl_LoReq': 1, 'ReqLvl_MidReq': 2, 'ReqLvl_HiReq': 3}
        compute_method = None
        length = 2
        startbit = 36
        byte = 4
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class AFUCh5StsChgSts:
        sig_name = "AFUCh5StsChgSts"
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
        sig_value_table = {'AirFragChgSts_Initial': 0, 'AirFragChgSts_Changing': 1, 'AirFragChgSts_ChangeSucceeded': 2, 'AirFragChgSts_ChangeFailed': 3}
        compute_method = None
        length = 2
        startbit = 24
        byte = 3
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class AFUCh5StsMotErr:
        sig_name = "AFUCh5StsMotErr"
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
        sig_value_table = {'AirFragMotErr_NoErr': 0, 'AirFragMotErr_Err': 1}
        compute_method = None
        length = 1
        startbit = 26
        byte = 3
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class AFUCtrlrErrMemChks:
        sig_name = "AFUCtrlrErrMemChks"
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
        sig_value_table = {'Err1_NoErr': 0, 'Err1_Err': 1}
        compute_method = None
        length = 1
        startbit = 29
        byte = 3
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class AFUCtrlrErrTemp:
        sig_name = "AFUCtrlrErrTemp"
        sig_start_bit = 32
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TempErr_Normal': 0, 'TempErr_OverTemp': 1, 'TempErr_UnderTemp': 2, 'TempErr_Invalid': 3}
        compute_method = None
        length = 2
        startbit = 32
        byte = 4
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class AFUInitSts:
        sig_name = "AFUInitSts"
        sig_start_bit = 34
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'InitialSts_NoInitialization': 0, 'InitialSts_Initializing': 1, 'InitialSts_InitializationOK': 2, 'InitialSts_InitializationFailed': 3}
        compute_method = None
        length = 2
        startbit = 34
        byte = 4
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class AFUCtrlrErrOverVolt:
        sig_name = "AFUCtrlrErrOverVolt"
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
        sig_value_table = {'Err1_NoErr': 0, 'Err1_Err': 1}
        compute_method = None
        length = 1
        startbit = 30
        byte = 3
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class AFUCh5StsTyp:
        sig_name = "AFUCh5StsTyp"
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

    class AFUCtrlrErrFan:
        sig_name = "AFUCtrlrErrFan"
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
        sig_value_table = {'Err1_NoErr': 0, 'Err1_Err': 1}
        compute_method = None
        length = 1
        startbit = 28
        byte = 3
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class AFUCh5StsAvlTi:
        sig_name = "AFUCh5StsAvlTi"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 9
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 0
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b00000001, 0b11111110, 1, 0)]

    class AFUCtrlrErrUnderVolt:
        sig_name = "AFUCtrlrErrUnderVolt"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class AFUCh5StsRelsRatFb:
        sig_name = "AFUCh5StsRelsRatFb"
        sig_start_bit = 9
        update_id_bit = None
        sig_length = 7
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 9
        byte = 1
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class AFUCh5StsRunngSts:
        sig_name = "AFUCh5StsRunngSts"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 27
        byte = 3
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3


class LCURLCUR_LIN4Fr03:
    msg_name = "LCURLCUR_LIN4Fr03"
    msg_id = 10
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "LCUR"
    rx_nodes = ['RRMM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class VehTiGlb:
        sig_name = "VehTiGlb"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 32
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4294967295
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 32
        startbit = 0
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0)]


