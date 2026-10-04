lin_scheduleTable = {'Ccm_Lin3_DiagResponseSchedule01': [(0, 'DiagResponse7', 0.015)], 'Ccm_Lin3_DiagRequestSchedule01': [(0, 'DiagRequest7', 0.015)], 'Ccm_Lin3ScheduleTable1_CCM_LIN3': [(0, 'VgaCcm_Lin3Vga09Fr01', 0.015), (1, 'VgaCcm_Lin3Vga10Fr01', 0.015), (2, 'VgaCcm_Lin3Vga01Fr01', 0.015), (3, 'VgaCcm_Lin3Vga02Fr01', 0.015), (4, 'VgaCcm_Lin3Vga03Fr01', 0.015), (5, 'VgaCcm_Lin3Vga04Fr01', 0.015), (6, 'VgaCcm_Lin3Vga05Fr01', 0.015), (7, 'VgaCcm_Lin3Vga06Fr01', 0.015), (8, 'VgaCcm_Lin3Vga07Fr01', 0.015), (9, 'VgaCcm_Lin3Vga08Fr01', 0.015), (10, 'CcmCcm_Lin3Fr03', 0.015)]}


class DiagResponse7:
    msg_name = "DiagResponse7"
    msg_id = 61
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['CCM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class VgaCcm_Lin3Vga06Fr01:
    msg_name = "VgaCcm_Lin3Vga06Fr01"
    msg_id = 26
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "VGC"
    rx_nodes = ['CCM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class VentnActr06MovDir:
        sig_name = "VentnActr06MovDir"
        sig_start_bit = 60
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotDir_CW': 0, 'VentnMotDir_CCW': 1, 'VentnMotDir_Reserved': 2, 'VentnMotDir_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 60
        byte = 7
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class VentnActr06UrgcExist:
        sig_name = "VentnActr06UrgcExist"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01UrgcExist_False': 0, 'VentnActr01UrgcExist_True': 1, 'VentnActr01UrgcExist_Reserved': 2, 'VentnActr01UrgcExist_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 8
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VentnActr06ResetSts:
        sig_name = "VentnActr06ResetSts"
        sig_start_bit = 14
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01ResetSts_NoReset': 0, 'VentnActr01ResetSts_Reset': 1, 'VentnActr01ResetSts_Reserved': 2, 'VentnActr01ResetSts_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 14
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class VentnActr06DrvDir:
        sig_name = "VentnActr06DrvDir"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01DrvDir_Downward': 0, 'VentnActr01DrvDir_Upward': 1, 'VentnActr01DrvDir_Initialization': 2, 'VentnActr01DrvDir_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 40
        byte = 5
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VentnActr06BusAdr:
        sig_name = "VentnActr06BusAdr"
        sig_start_bit = 48
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 255
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 48
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VentnActr06UrgcPson:
        sig_name = "VentnActr06UrgcPson"
        sig_start_bit = 58
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotUrgcPson_Bottom': 0, 'VentnMotUrgcPson_Top': 1, 'VentnMotUrgcPson_Reserved': 2, 'VentnMotUrgcPson_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 58
        byte = 7
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VentnActr06UrgcSts:
        sig_name = "VentnActr06UrgcSts"
        sig_start_bit = 56
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotUrgcUnlck_Off': 0, 'VentnMotUrgcUnlck_On': 1, 'VentnMotUrgcUnlck_Reserved': 2, 'VentnMotUrgcUnlck_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 56
        byte = 7
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VentnActr06VoltErr:
        sig_name = "VentnActr06VoltErr"
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
        sig_value_table = {'VentnActr01VoltErr_Normal': 0, 'VentnActr01VoltErr_UnderVolt': 1, 'VentnActr01VoltErr_OvrVolt': 2, 'VentnActr01VoltErr_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 6
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class VentnActr06ElecErr:
        sig_name = "VentnActr06ElecErr"
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
        sig_value_table = {'VentnActr01ElecErr_Normal': 0, 'VentnActr01ElecErr_ElecErr': 1, 'VentnActr01ElecErr_PrmntElecErr': 2, 'VentnActr01ElecErr_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 4
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class VentnActr06BlckSts:
        sig_name = "VentnActr06BlckSts"
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
        sig_value_table = {'VentnActr01BlckSts_NoBlock': 0, 'VentnActr01BlckSts_Block': 1, 'VentnActr01BlckSts_Reserved': 2, 'VentnActr01BlckSts_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 12
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class VentnActr06CoilSts:
        sig_name = "VentnActr06CoilSts"
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
        sig_value_table = {'VentnMotUrgcUnlck_Off': 0, 'VentnMotUrgcUnlck_On': 1, 'VentnMotUrgcUnlck_Reserved': 2, 'VentnMotUrgcUnlck_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 16
        byte = 2
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VentnActr06ActPson:
        sig_name = "VentnActr06ActPson"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 32767
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 24
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111111, 0b00000000, 8, 0)]

    class VentnActr06OvrTempErr:
        sig_name = "VentnActr06OvrTempErr"
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
        sig_value_table = {'VentnActr01OvrTempErr_Normal': 0, 'VentnActr01OvrTempErr_OvrTempErr': 1, 'VentnActr01OvrTempErr_Reserved': 2, 'VentnActr01OvrTempErr_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 2
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VentnActr06BlckInd:
        sig_name = "VentnActr06BlckInd"
        sig_start_bit = 10
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01BlckInd_Disabled': 0, 'VentnActr01BlckInd_Enabled': 1, 'VentnActr01BlckInd_Reserved': 2, 'VentnActr01BlckInd_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 10
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VentnActr06PsonSts:
        sig_name = "VentnActr06PsonSts"
        sig_start_bit = 18
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotPsonAvl_Targetpositionvalid': 0, 'VentnMotPsonAvl_Startpositionvalid': 1, 'VentnMotPsonAvl_Bothpositionsinvalid': 2, 'VentnMotPsonAvl_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 18
        byte = 2
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VentnActr06Mode:
        sig_name = "VentnActr06Mode"
        sig_start_bit = 62
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotMode_Normal': 0, 'VentnMotMode_Stop': 1, 'VentnMotMode_Reserved_orMaintainence': 2, 'VentnMotMode_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 62
        byte = 7
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class VentnActr06SpclFct:
        sig_name = "VentnActr06SpclFct"
        sig_start_bit = 44
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 3
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01SpclFct_None': 0, 'VentnActr01SpclFct_SpecialFunction1active': 1, 'VentnActr01SpclFct_Reserved': 2, 'VentnActr01SpclFct_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 44
        byte = 5
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class VentnActr06TrqSts:
        sig_name = "VentnActr06TrqSts"
        sig_start_bit = 42
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 3
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotUrgcUnlck_Off': 0, 'VentnMotUrgcUnlck_On': 1, 'VentnMotUrgcUnlck_Reserved': 2, 'VentnMotUrgcUnlck_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 42
        byte = 5
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VentnActr06SpdSts:
        sig_name = "VentnActr06SpdSts"
        sig_start_bit = 20
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01SpdSts_Stop': 0, 'VentnActr01SpdSts_Speedlevel1': 1, 'VentnActr01SpdSts_Speedlevel2': 2, 'VentnActr01SpdSts_Speedlevel3': 3, 'VentnActr01SpdSts_Speedlevel4': 4, 'VentnActr01SpdSts_Autospeed': 5, 'VentnActr01SpdSts_Reserved0': 6, 'VentnActr01SpdSts_Reserved1': 7, 'VentnActr01SpdSts_Reserved2': 8, 'VentnActr01SpdSts_Reserved3': 9, 'VentnActr01SpdSts_Reserved4': 10, 'VentnActr01SpdSts_Reserved5': 11, 'VentnActr01SpdSts_Reserved6': 12, 'VentnActr01SpdSts_Reserved7': 13, 'VentnActr01SpdSts_Reserved8': 14, 'VentnActr01SpdSts_Signalinvalid': 15}
        compute_method = None
        length = 4
        startbit = 20
        byte = 2
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4


class VgaCcm_Lin3Vga07Fr01:
    msg_name = "VgaCcm_Lin3Vga07Fr01"
    msg_id = 27
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "VGC"
    rx_nodes = ['CCM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class VentnActr07VoltErr:
        sig_name = "VentnActr07VoltErr"
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
        sig_value_table = {'VentnActr01VoltErr_Normal': 0, 'VentnActr01VoltErr_UnderVolt': 1, 'VentnActr01VoltErr_OvrVolt': 2, 'VentnActr01VoltErr_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 6
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class VentnActr07BlckInd:
        sig_name = "VentnActr07BlckInd"
        sig_start_bit = 10
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01BlckInd_Disabled': 0, 'VentnActr01BlckInd_Enabled': 1, 'VentnActr01BlckInd_Reserved': 2, 'VentnActr01BlckInd_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 10
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VentnActr07Mode:
        sig_name = "VentnActr07Mode"
        sig_start_bit = 62
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotMode_Normal': 0, 'VentnMotMode_Stop': 1, 'VentnMotMode_Reserved_orMaintainence': 2, 'VentnMotMode_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 62
        byte = 7
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class VentnActr07UrgcExist:
        sig_name = "VentnActr07UrgcExist"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01UrgcExist_False': 0, 'VentnActr01UrgcExist_True': 1, 'VentnActr01UrgcExist_Reserved': 2, 'VentnActr01UrgcExist_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 8
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VentnActr07MovDir:
        sig_name = "VentnActr07MovDir"
        sig_start_bit = 60
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotDir_CW': 0, 'VentnMotDir_CCW': 1, 'VentnMotDir_Reserved': 2, 'VentnMotDir_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 60
        byte = 7
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class VentnActr07ActPson:
        sig_name = "VentnActr07ActPson"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 32767
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 24
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111111, 0b00000000, 8, 0)]

    class VentnActr07ElecErr:
        sig_name = "VentnActr07ElecErr"
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
        sig_value_table = {'VentnActr01ElecErr_Normal': 0, 'VentnActr01ElecErr_ElecErr': 1, 'VentnActr01ElecErr_PrmntElecErr': 2, 'VentnActr01ElecErr_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 4
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class VentnActr07UrgcPson:
        sig_name = "VentnActr07UrgcPson"
        sig_start_bit = 58
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotUrgcPson_Bottom': 0, 'VentnMotUrgcPson_Top': 1, 'VentnMotUrgcPson_Reserved': 2, 'VentnMotUrgcPson_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 58
        byte = 7
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VentnActr07TrqSts:
        sig_name = "VentnActr07TrqSts"
        sig_start_bit = 42
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 3
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotUrgcUnlck_Off': 0, 'VentnMotUrgcUnlck_On': 1, 'VentnMotUrgcUnlck_Reserved': 2, 'VentnMotUrgcUnlck_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 42
        byte = 5
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VentnActr07CoilSts:
        sig_name = "VentnActr07CoilSts"
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
        sig_value_table = {'VentnMotUrgcUnlck_Off': 0, 'VentnMotUrgcUnlck_On': 1, 'VentnMotUrgcUnlck_Reserved': 2, 'VentnMotUrgcUnlck_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 16
        byte = 2
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VentnActr07BlckSts:
        sig_name = "VentnActr07BlckSts"
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
        sig_value_table = {'VentnActr01BlckSts_NoBlock': 0, 'VentnActr01BlckSts_Block': 1, 'VentnActr01BlckSts_Reserved': 2, 'VentnActr01BlckSts_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 12
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class VentnActr07UrgcSts:
        sig_name = "VentnActr07UrgcSts"
        sig_start_bit = 56
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotUrgcUnlck_Off': 0, 'VentnMotUrgcUnlck_On': 1, 'VentnMotUrgcUnlck_Reserved': 2, 'VentnMotUrgcUnlck_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 56
        byte = 7
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VentnActr07SpclFct:
        sig_name = "VentnActr07SpclFct"
        sig_start_bit = 44
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 3
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01SpclFct_None': 0, 'VentnActr01SpclFct_SpecialFunction1active': 1, 'VentnActr01SpclFct_Reserved': 2, 'VentnActr01SpclFct_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 44
        byte = 5
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class VentnActr07DrvDir:
        sig_name = "VentnActr07DrvDir"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01DrvDir_Downward': 0, 'VentnActr01DrvDir_Upward': 1, 'VentnActr01DrvDir_Initialization': 2, 'VentnActr01DrvDir_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 40
        byte = 5
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VentnActr07SpdSts:
        sig_name = "VentnActr07SpdSts"
        sig_start_bit = 20
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01SpdSts_Stop': 0, 'VentnActr01SpdSts_Speedlevel1': 1, 'VentnActr01SpdSts_Speedlevel2': 2, 'VentnActr01SpdSts_Speedlevel3': 3, 'VentnActr01SpdSts_Speedlevel4': 4, 'VentnActr01SpdSts_Autospeed': 5, 'VentnActr01SpdSts_Reserved0': 6, 'VentnActr01SpdSts_Reserved1': 7, 'VentnActr01SpdSts_Reserved2': 8, 'VentnActr01SpdSts_Reserved3': 9, 'VentnActr01SpdSts_Reserved4': 10, 'VentnActr01SpdSts_Reserved5': 11, 'VentnActr01SpdSts_Reserved6': 12, 'VentnActr01SpdSts_Reserved7': 13, 'VentnActr01SpdSts_Reserved8': 14, 'VentnActr01SpdSts_Signalinvalid': 15}
        compute_method = None
        length = 4
        startbit = 20
        byte = 2
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class VentnActr07PsonSts:
        sig_name = "VentnActr07PsonSts"
        sig_start_bit = 18
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotPsonAvl_Targetpositionvalid': 0, 'VentnMotPsonAvl_Startpositionvalid': 1, 'VentnMotPsonAvl_Bothpositionsinvalid': 2, 'VentnMotPsonAvl_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 18
        byte = 2
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VentnActr07OvrTempErr:
        sig_name = "VentnActr07OvrTempErr"
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
        sig_value_table = {'VentnActr01OvrTempErr_Normal': 0, 'VentnActr01OvrTempErr_OvrTempErr': 1, 'VentnActr01OvrTempErr_Reserved': 2, 'VentnActr01OvrTempErr_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 2
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VentnActr07BusAdr:
        sig_name = "VentnActr07BusAdr"
        sig_start_bit = 48
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 255
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 48
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VentnActr07ResetSts:
        sig_name = "VentnActr07ResetSts"
        sig_start_bit = 14
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01ResetSts_NoReset': 0, 'VentnActr01ResetSts_Reset': 1, 'VentnActr01ResetSts_Reserved': 2, 'VentnActr01ResetSts_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 14
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class CcmCcm_Lin3Fr03:
    msg_name = "CcmCcm_Lin3Fr03"
    msg_id = 9
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "CCM"
    rx_nodes = ['VGC', 'VGA10', 'VGA9']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class VentnMotPsonAvl:
        sig_name = "VentnMotPsonAvl"
        sig_start_bit = 18
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotPsonAvl_Targetpositionvalid': 0, 'VentnMotPsonAvl_Startpositionvalid': 1, 'VentnMotPsonAvl_Bothpositionsinvalid': 2, 'VentnMotPsonAvl_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 18
        byte = 2
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VentnMotDir:
        sig_name = "VentnMotDir"
        sig_start_bit = 60
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotDir_CW': 0, 'VentnMotDir_CCW': 1, 'VentnMotDir_Reserved': 2, 'VentnMotDir_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 60
        byte = 7
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class VentnMotCoilPwrOn:
        sig_name = "VentnMotCoilPwrOn"
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
        sig_value_table = {'VentnMotUrgcUnlck_Off': 0, 'VentnMotUrgcUnlck_On': 1, 'VentnMotUrgcUnlck_Reserved': 2, 'VentnMotUrgcUnlck_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 16
        byte = 2
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VentnMotTargtPson:
        sig_name = "VentnMotTargtPson"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 65535
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 24
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111111, 0b00000000, 8, 0)]

    class VentnMotUrgcUnlck:
        sig_name = "VentnMotUrgcUnlck"
        sig_start_bit = 56
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotUrgcUnlck_Off': 0, 'VentnMotUrgcUnlck_On': 1, 'VentnMotUrgcUnlck_Reserved': 2, 'VentnMotUrgcUnlck_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 56
        byte = 7
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VentnMotSpdSet:
        sig_name = "VentnMotSpdSet"
        sig_start_bit = 20
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotSpdSet_Reserved0': 0, 'VentnMotSpdSet_Speedlevel1': 1, 'VentnMotSpdSet_Speedlevel2': 2, 'VentnMotSpdSet_Speedlevel3': 3, 'VentnMotSpdSet_Speedlevel4': 4, 'VentnMotSpdSet_Autospeed': 5, 'VentnMotSpdSet_Reserved1': 6, 'VentnMotSpdSet_Reserved2': 7, 'VentnMotSpdSet_Reserved3': 8, 'VentnMotSpdSet_Reserved4': 9, 'VentnMotSpdSet_Reserved5': 10, 'VentnMotSpdSet_Reserved6': 11, 'VentnMotSpdSet_Reserved7': 12, 'VentnMotSpdSet_Reserved8': 13, 'VentnMotSpdSet_Reserved9': 14, 'VentnMotSpdSet_Signalinvalid': 15}
        compute_method = None
        length = 4
        startbit = 20
        byte = 2
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class VentnMotBlockCmd:
        sig_name = "VentnMotBlockCmd"
        sig_start_bit = 10
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotBlockCmd_Blockdelectiondisable': 0, 'VentnMotBlockCmd_Blockdelectionenable': 1, 'VentnMotBlockCmd_Reserved': 2, 'VentnMotBlockCmd_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 10
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VentnMotAdr:
        sig_name = "VentnMotAdr"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 255
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VentnMotClearReq:
        sig_name = "VentnMotClearReq"
        sig_start_bit = 12
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
        startbit = 12
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class VentnMotSaveData:
        sig_name = "VentnMotSaveData"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotSaveData_Notsavedata': 0, 'VentnMotSaveData_Savedata': 1, 'VentnMotSaveData_Reserved': 2, 'VentnMotSaveData_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 8
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VentnMotMode:
        sig_name = "VentnMotMode"
        sig_start_bit = 62
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotMode_Normal': 0, 'VentnMotMode_Stop': 1, 'VentnMotMode_Reserved_orMaintainence': 2, 'VentnMotMode_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 62
        byte = 7
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class VentnMotStrtPson:
        sig_name = "VentnMotStrtPson"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 65535
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 40
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111111, 0b00000000, 8, 0)]

    class VentnMotUrgcPson:
        sig_name = "VentnMotUrgcPson"
        sig_start_bit = 58
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotUrgcPson_Bottom': 0, 'VentnMotUrgcPson_Top': 1, 'VentnMotUrgcPson_Reserved': 2, 'VentnMotUrgcPson_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 58
        byte = 7
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2


class VgaCcm_Lin3Vga08Fr01:
    msg_name = "VgaCcm_Lin3Vga08Fr01"
    msg_id = 28
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "VGC"
    rx_nodes = ['CCM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class VentnActr08BlckInd:
        sig_name = "VentnActr08BlckInd"
        sig_start_bit = 10
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01BlckInd_Disabled': 0, 'VentnActr01BlckInd_Enabled': 1, 'VentnActr01BlckInd_Reserved': 2, 'VentnActr01BlckInd_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 10
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VentnActr08UrgcPson:
        sig_name = "VentnActr08UrgcPson"
        sig_start_bit = 58
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotUrgcPson_Bottom': 0, 'VentnMotUrgcPson_Top': 1, 'VentnMotUrgcPson_Reserved': 2, 'VentnMotUrgcPson_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 58
        byte = 7
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VentnActr08BlckSts:
        sig_name = "VentnActr08BlckSts"
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
        sig_value_table = {'VentnActr01BlckSts_NoBlock': 0, 'VentnActr01BlckSts_Block': 1, 'VentnActr01BlckSts_Reserved': 2, 'VentnActr01BlckSts_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 12
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class VentnActr08DrvDir:
        sig_name = "VentnActr08DrvDir"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01DrvDir_Downward': 0, 'VentnActr01DrvDir_Upward': 1, 'VentnActr01DrvDir_Initialization': 2, 'VentnActr01DrvDir_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 40
        byte = 5
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VentnActr08PsonSts:
        sig_name = "VentnActr08PsonSts"
        sig_start_bit = 18
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotPsonAvl_Targetpositionvalid': 0, 'VentnMotPsonAvl_Startpositionvalid': 1, 'VentnMotPsonAvl_Bothpositionsinvalid': 2, 'VentnMotPsonAvl_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 18
        byte = 2
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VentnActr08ResetSts:
        sig_name = "VentnActr08ResetSts"
        sig_start_bit = 14
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01ResetSts_NoReset': 0, 'VentnActr01ResetSts_Reset': 1, 'VentnActr01ResetSts_Reserved': 2, 'VentnActr01ResetSts_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 14
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class VentnActr08SpdSts:
        sig_name = "VentnActr08SpdSts"
        sig_start_bit = 20
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01SpdSts_Stop': 0, 'VentnActr01SpdSts_Speedlevel1': 1, 'VentnActr01SpdSts_Speedlevel2': 2, 'VentnActr01SpdSts_Speedlevel3': 3, 'VentnActr01SpdSts_Speedlevel4': 4, 'VentnActr01SpdSts_Autospeed': 5, 'VentnActr01SpdSts_Reserved0': 6, 'VentnActr01SpdSts_Reserved1': 7, 'VentnActr01SpdSts_Reserved2': 8, 'VentnActr01SpdSts_Reserved3': 9, 'VentnActr01SpdSts_Reserved4': 10, 'VentnActr01SpdSts_Reserved5': 11, 'VentnActr01SpdSts_Reserved6': 12, 'VentnActr01SpdSts_Reserved7': 13, 'VentnActr01SpdSts_Reserved8': 14, 'VentnActr01SpdSts_Signalinvalid': 15}
        compute_method = None
        length = 4
        startbit = 20
        byte = 2
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class VentnActr08ActPson:
        sig_name = "VentnActr08ActPson"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 32767
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 24
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111111, 0b00000000, 8, 0)]

    class VentnActr08VoltErr:
        sig_name = "VentnActr08VoltErr"
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
        sig_value_table = {'VentnActr01VoltErr_Normal': 0, 'VentnActr01VoltErr_UnderVolt': 1, 'VentnActr01VoltErr_OvrVolt': 2, 'VentnActr01VoltErr_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 6
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class VentnActr08CoilSts:
        sig_name = "VentnActr08CoilSts"
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
        sig_value_table = {'VentnMotUrgcUnlck_Off': 0, 'VentnMotUrgcUnlck_On': 1, 'VentnMotUrgcUnlck_Reserved': 2, 'VentnMotUrgcUnlck_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 16
        byte = 2
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VentnActr08MovDir:
        sig_name = "VentnActr08MovDir"
        sig_start_bit = 60
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotDir_CW': 0, 'VentnMotDir_CCW': 1, 'VentnMotDir_Reserved': 2, 'VentnMotDir_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 60
        byte = 7
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class VentnActr08Mode:
        sig_name = "VentnActr08Mode"
        sig_start_bit = 62
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotMode_Normal': 0, 'VentnMotMode_Stop': 1, 'VentnMotMode_Reserved_orMaintainence': 2, 'VentnMotMode_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 62
        byte = 7
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class VentnActr08BusAdr:
        sig_name = "VentnActr08BusAdr"
        sig_start_bit = 48
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 255
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 48
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VentnActr08TrqSts:
        sig_name = "VentnActr08TrqSts"
        sig_start_bit = 42
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 3
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotUrgcUnlck_Off': 0, 'VentnMotUrgcUnlck_On': 1, 'VentnMotUrgcUnlck_Reserved': 2, 'VentnMotUrgcUnlck_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 42
        byte = 5
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VentnActr08SpclFct:
        sig_name = "VentnActr08SpclFct"
        sig_start_bit = 44
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 3
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01SpclFct_None': 0, 'VentnActr01SpclFct_SpecialFunction1active': 1, 'VentnActr01SpclFct_Reserved': 2, 'VentnActr01SpclFct_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 44
        byte = 5
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class VentnActr08OvrTempErr:
        sig_name = "VentnActr08OvrTempErr"
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
        sig_value_table = {'VentnActr01OvrTempErr_Normal': 0, 'VentnActr01OvrTempErr_OvrTempErr': 1, 'VentnActr01OvrTempErr_Reserved': 2, 'VentnActr01OvrTempErr_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 2
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VentnActr08UrgcExist:
        sig_name = "VentnActr08UrgcExist"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01UrgcExist_False': 0, 'VentnActr01UrgcExist_True': 1, 'VentnActr01UrgcExist_Reserved': 2, 'VentnActr01UrgcExist_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 8
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VentnActr08UrgcSts:
        sig_name = "VentnActr08UrgcSts"
        sig_start_bit = 56
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotUrgcUnlck_Off': 0, 'VentnMotUrgcUnlck_On': 1, 'VentnMotUrgcUnlck_Reserved': 2, 'VentnMotUrgcUnlck_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 56
        byte = 7
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VentnActr08ElecErr:
        sig_name = "VentnActr08ElecErr"
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
        sig_value_table = {'VentnActr01ElecErr_Normal': 0, 'VentnActr01ElecErr_ElecErr': 1, 'VentnActr01ElecErr_PrmntElecErr': 2, 'VentnActr01ElecErr_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 4
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4


class VgaCcm_Lin3Vga03Fr01:
    msg_name = "VgaCcm_Lin3Vga03Fr01"
    msg_id = 20
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "VGC"
    rx_nodes = ['CCM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class VentnActr03DrvDir:
        sig_name = "VentnActr03DrvDir"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01DrvDir_Downward': 0, 'VentnActr01DrvDir_Upward': 1, 'VentnActr01DrvDir_Initialization': 2, 'VentnActr01DrvDir_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 40
        byte = 5
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VentnActr03TrqSts:
        sig_name = "VentnActr03TrqSts"
        sig_start_bit = 42
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 3
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotUrgcUnlck_Off': 0, 'VentnMotUrgcUnlck_On': 1, 'VentnMotUrgcUnlck_Reserved': 2, 'VentnMotUrgcUnlck_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 42
        byte = 5
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VentnActr03BlckInd:
        sig_name = "VentnActr03BlckInd"
        sig_start_bit = 10
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01BlckInd_Disabled': 0, 'VentnActr01BlckInd_Enabled': 1, 'VentnActr01BlckInd_Reserved': 2, 'VentnActr01BlckInd_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 10
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VentnActr03BlckSts:
        sig_name = "VentnActr03BlckSts"
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
        sig_value_table = {'VentnActr01BlckSts_NoBlock': 0, 'VentnActr01BlckSts_Block': 1, 'VentnActr01BlckSts_Reserved': 2, 'VentnActr01BlckSts_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 12
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class VentnActr03ActPson:
        sig_name = "VentnActr03ActPson"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 32767
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 24
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111111, 0b00000000, 8, 0)]

    class VentnActr03PsonSts:
        sig_name = "VentnActr03PsonSts"
        sig_start_bit = 18
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotPsonAvl_Targetpositionvalid': 0, 'VentnMotPsonAvl_Startpositionvalid': 1, 'VentnMotPsonAvl_Bothpositionsinvalid': 2, 'VentnMotPsonAvl_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 18
        byte = 2
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VentnActr03UrgcSts:
        sig_name = "VentnActr03UrgcSts"
        sig_start_bit = 56
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotUrgcUnlck_Off': 0, 'VentnMotUrgcUnlck_On': 1, 'VentnMotUrgcUnlck_Reserved': 2, 'VentnMotUrgcUnlck_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 56
        byte = 7
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VentnActr03BusAdr:
        sig_name = "VentnActr03BusAdr"
        sig_start_bit = 48
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 255
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 48
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VentnActr03UrgcExist:
        sig_name = "VentnActr03UrgcExist"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01UrgcExist_False': 0, 'VentnActr01UrgcExist_True': 1, 'VentnActr01UrgcExist_Reserved': 2, 'VentnActr01UrgcExist_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 8
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VentnActr03OvrTempErr:
        sig_name = "VentnActr03OvrTempErr"
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
        sig_value_table = {'VentnActr01OvrTempErr_Normal': 0, 'VentnActr01OvrTempErr_OvrTempErr': 1, 'VentnActr01OvrTempErr_Reserved': 2, 'VentnActr01OvrTempErr_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 2
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VentnActr03SpclFct:
        sig_name = "VentnActr03SpclFct"
        sig_start_bit = 44
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 3
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01SpclFct_None': 0, 'VentnActr01SpclFct_SpecialFunction1active': 1, 'VentnActr01SpclFct_Reserved': 2, 'VentnActr01SpclFct_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 44
        byte = 5
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class VentnActr03Mode:
        sig_name = "VentnActr03Mode"
        sig_start_bit = 62
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotMode_Normal': 0, 'VentnMotMode_Stop': 1, 'VentnMotMode_Reserved_orMaintainence': 2, 'VentnMotMode_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 62
        byte = 7
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class VentnActr03ElecErr:
        sig_name = "VentnActr03ElecErr"
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
        sig_value_table = {'VentnActr01ElecErr_Normal': 0, 'VentnActr01ElecErr_ElecErr': 1, 'VentnActr01ElecErr_PrmntElecErr': 2, 'VentnActr01ElecErr_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 4
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class VentnActr03ResetSts:
        sig_name = "VentnActr03ResetSts"
        sig_start_bit = 14
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01ResetSts_NoReset': 0, 'VentnActr01ResetSts_Reset': 1, 'VentnActr01ResetSts_Reserved': 2, 'VentnActr01ResetSts_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 14
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class VentnActr03MovDir:
        sig_name = "VentnActr03MovDir"
        sig_start_bit = 60
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotDir_CW': 0, 'VentnMotDir_CCW': 1, 'VentnMotDir_Reserved': 2, 'VentnMotDir_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 60
        byte = 7
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class VentnActr03VoltErr:
        sig_name = "VentnActr03VoltErr"
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
        sig_value_table = {'VentnActr01VoltErr_Normal': 0, 'VentnActr01VoltErr_UnderVolt': 1, 'VentnActr01VoltErr_OvrVolt': 2, 'VentnActr01VoltErr_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 6
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class VentnActr03UrgcPson:
        sig_name = "VentnActr03UrgcPson"
        sig_start_bit = 58
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotUrgcPson_Bottom': 0, 'VentnMotUrgcPson_Top': 1, 'VentnMotUrgcPson_Reserved': 2, 'VentnMotUrgcPson_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 58
        byte = 7
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VentnActr03SpdSts:
        sig_name = "VentnActr03SpdSts"
        sig_start_bit = 20
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01SpdSts_Stop': 0, 'VentnActr01SpdSts_Speedlevel1': 1, 'VentnActr01SpdSts_Speedlevel2': 2, 'VentnActr01SpdSts_Speedlevel3': 3, 'VentnActr01SpdSts_Speedlevel4': 4, 'VentnActr01SpdSts_Autospeed': 5, 'VentnActr01SpdSts_Reserved0': 6, 'VentnActr01SpdSts_Reserved1': 7, 'VentnActr01SpdSts_Reserved2': 8, 'VentnActr01SpdSts_Reserved3': 9, 'VentnActr01SpdSts_Reserved4': 10, 'VentnActr01SpdSts_Reserved5': 11, 'VentnActr01SpdSts_Reserved6': 12, 'VentnActr01SpdSts_Reserved7': 13, 'VentnActr01SpdSts_Reserved8': 14, 'VentnActr01SpdSts_Signalinvalid': 15}
        compute_method = None
        length = 4
        startbit = 20
        byte = 2
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class VentnActr03CoilSts:
        sig_name = "VentnActr03CoilSts"
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
        sig_value_table = {'VentnMotUrgcUnlck_Off': 0, 'VentnMotUrgcUnlck_On': 1, 'VentnMotUrgcUnlck_Reserved': 2, 'VentnMotUrgcUnlck_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 16
        byte = 2
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0


class VgaCcm_Lin3Vga09Fr01:
    msg_name = "VgaCcm_Lin3Vga09Fr01"
    msg_id = 29
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "VGC5"
    rx_nodes = ['CCM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class VentnActr09PsonSts:
        sig_name = "VentnActr09PsonSts"
        sig_start_bit = 18
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotPsonAvl_Targetpositionvalid': 0, 'VentnMotPsonAvl_Startpositionvalid': 1, 'VentnMotPsonAvl_Bothpositionsinvalid': 2, 'VentnMotPsonAvl_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 18
        byte = 2
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VentnActr09BlckSts:
        sig_name = "VentnActr09BlckSts"
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
        sig_value_table = {'VentnActr01BlckSts_NoBlock': 0, 'VentnActr01BlckSts_Block': 1, 'VentnActr01BlckSts_Reserved': 2, 'VentnActr01BlckSts_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 12
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class VentnActr09ElecErr:
        sig_name = "VentnActr09ElecErr"
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
        sig_value_table = {'VentnActr01ElecErr_Normal': 0, 'VentnActr01ElecErr_ElecErr': 1, 'VentnActr01ElecErr_PrmntElecErr': 2, 'VentnActr01ElecErr_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 4
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class VentnActr09UrgcExist:
        sig_name = "VentnActr09UrgcExist"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01UrgcExist_False': 0, 'VentnActr01UrgcExist_True': 1, 'VentnActr01UrgcExist_Reserved': 2, 'VentnActr01UrgcExist_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 8
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VentnActr09TrqSts:
        sig_name = "VentnActr09TrqSts"
        sig_start_bit = 42
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 3
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Invalid': 0, 'Valid': 1, 'Reserved': 2, 'Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 42
        byte = 5
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VentnActr09VoltErr:
        sig_name = "VentnActr09VoltErr"
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
        sig_value_table = {'VentnActr01VoltErr_Normal': 0, 'VentnActr01VoltErr_UnderVolt': 1, 'VentnActr01VoltErr_OvrVolt': 2, 'VentnActr01VoltErr_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 6
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class VentnActr09BlckInd:
        sig_name = "VentnActr09BlckInd"
        sig_start_bit = 10
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01BlckInd_Disabled': 0, 'VentnActr01BlckInd_Enabled': 1, 'VentnActr01BlckInd_Reserved': 2, 'VentnActr01BlckInd_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 10
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VentnActr09DrvDir:
        sig_name = "VentnActr09DrvDir"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01DrvDir_Downward': 0, 'VentnActr01DrvDir_Upward': 1, 'VentnActr01DrvDir_Initialization': 2, 'VentnActr01DrvDir_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 40
        byte = 5
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VentnActr09SpdSts:
        sig_name = "VentnActr09SpdSts"
        sig_start_bit = 20
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01SpdSts_Stop': 0, 'VentnActr01SpdSts_Speedlevel1': 1, 'VentnActr01SpdSts_Speedlevel2': 2, 'VentnActr01SpdSts_Speedlevel3': 3, 'VentnActr01SpdSts_Speedlevel4': 4, 'VentnActr01SpdSts_Autospeed': 5, 'VentnActr01SpdSts_Reserved0': 6, 'VentnActr01SpdSts_Reserved1': 7, 'VentnActr01SpdSts_Reserved2': 8, 'VentnActr01SpdSts_Reserved3': 9, 'VentnActr01SpdSts_Reserved4': 10, 'VentnActr01SpdSts_Reserved5': 11, 'VentnActr01SpdSts_Reserved6': 12, 'VentnActr01SpdSts_Reserved7': 13, 'VentnActr01SpdSts_Reserved8': 14, 'VentnActr01SpdSts_Signalinvalid': 15}
        compute_method = None
        length = 4
        startbit = 20
        byte = 2
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class VentnActr09CoilSts:
        sig_name = "VentnActr09CoilSts"
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
        sig_value_table = {'VentnMotUrgcUnlck_Off': 0, 'VentnMotUrgcUnlck_On': 1, 'VentnMotUrgcUnlck_Reserved': 2, 'VentnMotUrgcUnlck_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 16
        byte = 2
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VentnActr09Mode:
        sig_name = "VentnActr09Mode"
        sig_start_bit = 62
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotMode_Normal': 0, 'VentnMotMode_Stop': 1, 'VentnMotMode_Reserved_orMaintainence': 2, 'VentnMotMode_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 62
        byte = 7
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class VentnActr09SpclFct:
        sig_name = "VentnActr09SpclFct"
        sig_start_bit = 44
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 3
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01SpclFct_None': 0, 'VentnActr01SpclFct_SpecialFunction1active': 1, 'VentnActr01SpclFct_Reserved': 2, 'VentnActr01SpclFct_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 44
        byte = 5
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class VentnActr09UrgcPson:
        sig_name = "VentnActr09UrgcPson"
        sig_start_bit = 58
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotUrgcPson_Bottom': 0, 'VentnMotUrgcPson_Top': 1, 'VentnMotUrgcPson_Reserved': 2, 'VentnMotUrgcPson_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 58
        byte = 7
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VentnActr09ActPson:
        sig_name = "VentnActr09ActPson"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 32767
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 24
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111111, 0b00000000, 8, 0)]

    class VentnActr09ResetSts:
        sig_name = "VentnActr09ResetSts"
        sig_start_bit = 14
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01ResetSts_NoReset': 0, 'VentnActr01ResetSts_Reset': 1, 'VentnActr01ResetSts_Reserved': 2, 'VentnActr01ResetSts_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 14
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class VentnActr09MovDir:
        sig_name = "VentnActr09MovDir"
        sig_start_bit = 60
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotDir_CW': 0, 'VentnMotDir_CCW': 1, 'VentnMotDir_Reserved': 2, 'VentnMotDir_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 60
        byte = 7
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class VentnActr09UrgcSts:
        sig_name = "VentnActr09UrgcSts"
        sig_start_bit = 56
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotUrgcUnlck_Off': 0, 'VentnMotUrgcUnlck_On': 1, 'VentnMotUrgcUnlck_Reserved': 2, 'VentnMotUrgcUnlck_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 56
        byte = 7
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VentnActr09BusAdr:
        sig_name = "VentnActr09BusAdr"
        sig_start_bit = 48
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 255
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 48
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VentnActr09OvrTempErr:
        sig_name = "VentnActr09OvrTempErr"
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
        sig_value_table = {'VentnActr01OvrTempErr_Normal': 0, 'VentnActr01OvrTempErr_OvrTempErr': 1, 'VentnActr01OvrTempErr_Reserved': 2, 'VentnActr01OvrTempErr_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 2
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2


class VgaCcm_Lin3Vga01Fr01:
    msg_name = "VgaCcm_Lin3Vga01Fr01"
    msg_id = 17
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "VGC"
    rx_nodes = ['CCM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class VentnActr01ResetSts:
        sig_name = "VentnActr01ResetSts"
        sig_start_bit = 14
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01ResetSts_NoReset': 0, 'VentnActr01ResetSts_Reset': 1, 'VentnActr01ResetSts_Reserved': 2, 'VentnActr01ResetSts_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 14
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class VentnActr01PsonSts:
        sig_name = "VentnActr01PsonSts"
        sig_start_bit = 18
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotPsonAvl_Targetpositionvalid': 0, 'VentnMotPsonAvl_Startpositionvalid': 1, 'VentnMotPsonAvl_Bothpositionsinvalid': 2, 'VentnMotPsonAvl_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 18
        byte = 2
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VentnActr01UrgcSts:
        sig_name = "VentnActr01UrgcSts"
        sig_start_bit = 56
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotUrgcUnlck_Off': 0, 'VentnMotUrgcUnlck_On': 1, 'VentnMotUrgcUnlck_Reserved': 2, 'VentnMotUrgcUnlck_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 56
        byte = 7
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VentnActr01CoilSts:
        sig_name = "VentnActr01CoilSts"
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
        sig_value_table = {'VentnMotUrgcUnlck_Off': 0, 'VentnMotUrgcUnlck_On': 1, 'VentnMotUrgcUnlck_Reserved': 2, 'VentnMotUrgcUnlck_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 16
        byte = 2
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VentnActr01MovDir:
        sig_name = "VentnActr01MovDir"
        sig_start_bit = 60
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotDir_CW': 0, 'VentnMotDir_CCW': 1, 'VentnMotDir_Reserved': 2, 'VentnMotDir_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 60
        byte = 7
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class VentnActr01OvrTempErr:
        sig_name = "VentnActr01OvrTempErr"
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
        sig_value_table = {'VentnActr01OvrTempErr_Normal': 0, 'VentnActr01OvrTempErr_OvrTempErr': 1, 'VentnActr01OvrTempErr_Reserved': 2, 'VentnActr01OvrTempErr_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 2
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VentnActr01SpdSts:
        sig_name = "VentnActr01SpdSts"
        sig_start_bit = 20
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01SpdSts_Stop': 0, 'VentnActr01SpdSts_Speedlevel1': 1, 'VentnActr01SpdSts_Speedlevel2': 2, 'VentnActr01SpdSts_Speedlevel3': 3, 'VentnActr01SpdSts_Speedlevel4': 4, 'VentnActr01SpdSts_Autospeed': 5, 'VentnActr01SpdSts_Reserved0': 6, 'VentnActr01SpdSts_Reserved1': 7, 'VentnActr01SpdSts_Reserved2': 8, 'VentnActr01SpdSts_Reserved3': 9, 'VentnActr01SpdSts_Reserved4': 10, 'VentnActr01SpdSts_Reserved5': 11, 'VentnActr01SpdSts_Reserved6': 12, 'VentnActr01SpdSts_Reserved7': 13, 'VentnActr01SpdSts_Reserved8': 14, 'VentnActr01SpdSts_Signalinvalid': 15}
        compute_method = None
        length = 4
        startbit = 20
        byte = 2
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class VentnActr01ElecErr:
        sig_name = "VentnActr01ElecErr"
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
        sig_value_table = {'VentnActr01ElecErr_Normal': 0, 'VentnActr01ElecErr_ElecErr': 1, 'VentnActr01ElecErr_PrmntElecErr': 2, 'VentnActr01ElecErr_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 4
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class VentnActr01BlckSts:
        sig_name = "VentnActr01BlckSts"
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
        sig_value_table = {'VentnActr01BlckSts_NoBlock': 0, 'VentnActr01BlckSts_Block': 1, 'VentnActr01BlckSts_Reserved': 2, 'VentnActr01BlckSts_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 12
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class VentnActr01Mode:
        sig_name = "VentnActr01Mode"
        sig_start_bit = 62
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotMode_Normal': 0, 'VentnMotMode_Stop': 1, 'VentnMotMode_Reserved_orMaintainence': 2, 'VentnMotMode_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 62
        byte = 7
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class VentnActr01TrqSts:
        sig_name = "VentnActr01TrqSts"
        sig_start_bit = 42
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 3
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotUrgcUnlck_Off': 0, 'VentnMotUrgcUnlck_On': 1, 'VentnMotUrgcUnlck_Reserved': 2, 'VentnMotUrgcUnlck_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 42
        byte = 5
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VentnActr01BusAdr:
        sig_name = "VentnActr01BusAdr"
        sig_start_bit = 48
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 255
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 48
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VentnActr01DrvDir:
        sig_name = "VentnActr01DrvDir"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01DrvDir_Downward': 0, 'VentnActr01DrvDir_Upward': 1, 'VentnActr01DrvDir_Initialization': 2, 'VentnActr01DrvDir_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 40
        byte = 5
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VentnActr01SpclFct:
        sig_name = "VentnActr01SpclFct"
        sig_start_bit = 44
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 3
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01SpclFct_None': 0, 'VentnActr01SpclFct_SpecialFunction1active': 1, 'VentnActr01SpclFct_Reserved': 2, 'VentnActr01SpclFct_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 44
        byte = 5
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class VentnActr01VoltErr:
        sig_name = "VentnActr01VoltErr"
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
        sig_value_table = {'VentnActr01VoltErr_Normal': 0, 'VentnActr01VoltErr_UnderVolt': 1, 'VentnActr01VoltErr_OvrVolt': 2, 'VentnActr01VoltErr_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 6
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class VentnActr01UrgcExist:
        sig_name = "VentnActr01UrgcExist"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01UrgcExist_False': 0, 'VentnActr01UrgcExist_True': 1, 'VentnActr01UrgcExist_Reserved': 2, 'VentnActr01UrgcExist_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 8
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VentnActr01BlckInd:
        sig_name = "VentnActr01BlckInd"
        sig_start_bit = 10
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01BlckInd_Disabled': 0, 'VentnActr01BlckInd_Enabled': 1, 'VentnActr01BlckInd_Reserved': 2, 'VentnActr01BlckInd_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 10
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VentnActr01UrgcPson:
        sig_name = "VentnActr01UrgcPson"
        sig_start_bit = 58
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotUrgcPson_Bottom': 0, 'VentnMotUrgcPson_Top': 1, 'VentnMotUrgcPson_Reserved': 2, 'VentnMotUrgcPson_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 58
        byte = 7
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VentnActr01ActPson:
        sig_name = "VentnActr01ActPson"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 32767
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 24
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111111, 0b00000000, 8, 0)]


class VgaCcm_Lin3Vga10Fr01:
    msg_name = "VgaCcm_Lin3Vga10Fr01"
    msg_id = 30
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "VGA10"
    rx_nodes = ['CCM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class VentnActr10UrgcPson:
        sig_name = "VentnActr10UrgcPson"
        sig_start_bit = 58
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotUrgcPson_Bottom': 0, 'VentnMotUrgcPson_Top': 1, 'VentnMotUrgcPson_Reserved': 2, 'VentnMotUrgcPson_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 58
        byte = 7
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VentnActr10DrvDir:
        sig_name = "VentnActr10DrvDir"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01DrvDir_Downward': 0, 'VentnActr01DrvDir_Upward': 1, 'VentnActr01DrvDir_Initialization': 2, 'VentnActr01DrvDir_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 40
        byte = 5
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VentnActr10Mode:
        sig_name = "VentnActr10Mode"
        sig_start_bit = 62
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotMode_Normal': 0, 'VentnMotMode_Stop': 1, 'VentnMotMode_Reserved_orMaintainence': 2, 'VentnMotMode_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 62
        byte = 7
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class VentnActr10SpclFct:
        sig_name = "VentnActr10SpclFct"
        sig_start_bit = 44
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 3
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01SpclFct_None': 0, 'VentnActr01SpclFct_SpecialFunction1active': 1, 'VentnActr01SpclFct_Reserved': 2, 'VentnActr01SpclFct_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 44
        byte = 5
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class VentnActr10VoltErr:
        sig_name = "VentnActr10VoltErr"
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
        sig_value_table = {'VentnActr01VoltErr_Normal': 0, 'VentnActr01VoltErr_UnderVolt': 1, 'VentnActr01VoltErr_OvrVolt': 2, 'VentnActr01VoltErr_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 6
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class VentnActr10MovDir:
        sig_name = "VentnActr10MovDir"
        sig_start_bit = 60
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotDir_CW': 0, 'VentnMotDir_CCW': 1, 'VentnMotDir_Reserved': 2, 'VentnMotDir_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 60
        byte = 7
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class VentnActr10ActPson:
        sig_name = "VentnActr10ActPson"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 32767
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 24
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111111, 0b00000000, 8, 0)]

    class VentnActr10UrgcSts:
        sig_name = "VentnActr10UrgcSts"
        sig_start_bit = 56
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotUrgcUnlck_Off': 0, 'VentnMotUrgcUnlck_On': 1, 'VentnMotUrgcUnlck_Reserved': 2, 'VentnMotUrgcUnlck_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 56
        byte = 7
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VentnActr10ResetSts:
        sig_name = "VentnActr10ResetSts"
        sig_start_bit = 14
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01ResetSts_NoReset': 0, 'VentnActr01ResetSts_Reset': 1, 'VentnActr01ResetSts_Reserved': 2, 'VentnActr01ResetSts_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 14
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class VentnActr10ElecErr:
        sig_name = "VentnActr10ElecErr"
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
        sig_value_table = {'VentnActr01ElecErr_Normal': 0, 'VentnActr01ElecErr_ElecErr': 1, 'VentnActr01ElecErr_PrmntElecErr': 2, 'VentnActr01ElecErr_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 4
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class VentnActr10UrgcExist:
        sig_name = "VentnActr10UrgcExist"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01UrgcExist_False': 0, 'VentnActr01UrgcExist_True': 1, 'VentnActr01UrgcExist_Reserved': 2, 'VentnActr01UrgcExist_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 8
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VentnActr10TrqSts:
        sig_name = "VentnActr10TrqSts"
        sig_start_bit = 42
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 3
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Invalid': 0, 'Valid': 1, 'Reserved': 2, 'Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 42
        byte = 5
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VentnActr10SpdSts:
        sig_name = "VentnActr10SpdSts"
        sig_start_bit = 20
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01SpdSts_Stop': 0, 'VentnActr01SpdSts_Speedlevel1': 1, 'VentnActr01SpdSts_Speedlevel2': 2, 'VentnActr01SpdSts_Speedlevel3': 3, 'VentnActr01SpdSts_Speedlevel4': 4, 'VentnActr01SpdSts_Autospeed': 5, 'VentnActr01SpdSts_Reserved0': 6, 'VentnActr01SpdSts_Reserved1': 7, 'VentnActr01SpdSts_Reserved2': 8, 'VentnActr01SpdSts_Reserved3': 9, 'VentnActr01SpdSts_Reserved4': 10, 'VentnActr01SpdSts_Reserved5': 11, 'VentnActr01SpdSts_Reserved6': 12, 'VentnActr01SpdSts_Reserved7': 13, 'VentnActr01SpdSts_Reserved8': 14, 'VentnActr01SpdSts_Signalinvalid': 15}
        compute_method = None
        length = 4
        startbit = 20
        byte = 2
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class VentnActr10BusAdr:
        sig_name = "VentnActr10BusAdr"
        sig_start_bit = 48
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 255
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 48
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VentnActr10PsonSts:
        sig_name = "VentnActr10PsonSts"
        sig_start_bit = 18
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotPsonAvl_Targetpositionvalid': 0, 'VentnMotPsonAvl_Startpositionvalid': 1, 'VentnMotPsonAvl_Bothpositionsinvalid': 2, 'VentnMotPsonAvl_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 18
        byte = 2
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VentnActr10BlckSts:
        sig_name = "VentnActr10BlckSts"
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
        sig_value_table = {'VentnActr01BlckSts_NoBlock': 0, 'VentnActr01BlckSts_Block': 1, 'VentnActr01BlckSts_Reserved': 2, 'VentnActr01BlckSts_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 12
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class VentnActr10OvrTempErr:
        sig_name = "VentnActr10OvrTempErr"
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
        sig_value_table = {'VentnActr01OvrTempErr_Normal': 0, 'VentnActr01OvrTempErr_OvrTempErr': 1, 'VentnActr01OvrTempErr_Reserved': 2, 'VentnActr01OvrTempErr_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 2
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VentnActr10CoilSts:
        sig_name = "VentnActr10CoilSts"
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
        sig_value_table = {'VentnMotUrgcUnlck_Off': 0, 'VentnMotUrgcUnlck_On': 1, 'VentnMotUrgcUnlck_Reserved': 2, 'VentnMotUrgcUnlck_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 16
        byte = 2
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VentnActr10BlckInd:
        sig_name = "VentnActr10BlckInd"
        sig_start_bit = 10
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01BlckInd_Disabled': 0, 'VentnActr01BlckInd_Enabled': 1, 'VentnActr01BlckInd_Reserved': 2, 'VentnActr01BlckInd_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 10
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2


class DiagRequest7:
    msg_name = "DiagRequest7"
    msg_id = 60
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CCM"
    rx_nodes = []
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class VgaCcm_Lin3Vga02Fr01:
    msg_name = "VgaCcm_Lin3Vga02Fr01"
    msg_id = 18
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "VGC"
    rx_nodes = ['CCM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class VentnActr02Mode:
        sig_name = "VentnActr02Mode"
        sig_start_bit = 62
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotMode_Normal': 0, 'VentnMotMode_Stop': 1, 'VentnMotMode_Reserved_orMaintainence': 2, 'VentnMotMode_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 62
        byte = 7
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class VentnActr02SpdSts:
        sig_name = "VentnActr02SpdSts"
        sig_start_bit = 20
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01SpdSts_Stop': 0, 'VentnActr01SpdSts_Speedlevel1': 1, 'VentnActr01SpdSts_Speedlevel2': 2, 'VentnActr01SpdSts_Speedlevel3': 3, 'VentnActr01SpdSts_Speedlevel4': 4, 'VentnActr01SpdSts_Autospeed': 5, 'VentnActr01SpdSts_Reserved0': 6, 'VentnActr01SpdSts_Reserved1': 7, 'VentnActr01SpdSts_Reserved2': 8, 'VentnActr01SpdSts_Reserved3': 9, 'VentnActr01SpdSts_Reserved4': 10, 'VentnActr01SpdSts_Reserved5': 11, 'VentnActr01SpdSts_Reserved6': 12, 'VentnActr01SpdSts_Reserved7': 13, 'VentnActr01SpdSts_Reserved8': 14, 'VentnActr01SpdSts_Signalinvalid': 15}
        compute_method = None
        length = 4
        startbit = 20
        byte = 2
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class VentnActr02SpclFct:
        sig_name = "VentnActr02SpclFct"
        sig_start_bit = 44
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 3
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01SpclFct_None': 0, 'VentnActr01SpclFct_SpecialFunction1active': 1, 'VentnActr01SpclFct_Reserved': 2, 'VentnActr01SpclFct_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 44
        byte = 5
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class VentnActr02BlckSts:
        sig_name = "VentnActr02BlckSts"
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
        sig_value_table = {'VentnActr01BlckSts_NoBlock': 0, 'VentnActr01BlckSts_Block': 1, 'VentnActr01BlckSts_Reserved': 2, 'VentnActr01BlckSts_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 12
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class VentnActr02PsonSts:
        sig_name = "VentnActr02PsonSts"
        sig_start_bit = 18
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotPsonAvl_Targetpositionvalid': 0, 'VentnMotPsonAvl_Startpositionvalid': 1, 'VentnMotPsonAvl_Bothpositionsinvalid': 2, 'VentnMotPsonAvl_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 18
        byte = 2
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VentnActr02UrgcPson:
        sig_name = "VentnActr02UrgcPson"
        sig_start_bit = 58
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotUrgcPson_Bottom': 0, 'VentnMotUrgcPson_Top': 1, 'VentnMotUrgcPson_Reserved': 2, 'VentnMotUrgcPson_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 58
        byte = 7
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VentnActr02ResetSts:
        sig_name = "VentnActr02ResetSts"
        sig_start_bit = 14
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01ResetSts_NoReset': 0, 'VentnActr01ResetSts_Reset': 1, 'VentnActr01ResetSts_Reserved': 2, 'VentnActr01ResetSts_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 14
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class VentnActr02BlckInd:
        sig_name = "VentnActr02BlckInd"
        sig_start_bit = 10
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01BlckInd_Disabled': 0, 'VentnActr01BlckInd_Enabled': 1, 'VentnActr01BlckInd_Reserved': 2, 'VentnActr01BlckInd_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 10
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VentnActr02ActPson:
        sig_name = "VentnActr02ActPson"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 32767
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 24
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111111, 0b00000000, 8, 0)]

    class VentnActr02OvrTempErr:
        sig_name = "VentnActr02OvrTempErr"
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
        sig_value_table = {'VentnActr01OvrTempErr_Normal': 0, 'VentnActr01OvrTempErr_OvrTempErr': 1, 'VentnActr01OvrTempErr_Reserved': 2, 'VentnActr01OvrTempErr_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 2
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VentnActr02CoilSts:
        sig_name = "VentnActr02CoilSts"
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
        sig_value_table = {'VentnMotUrgcUnlck_Off': 0, 'VentnMotUrgcUnlck_On': 1, 'VentnMotUrgcUnlck_Reserved': 2, 'VentnMotUrgcUnlck_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 16
        byte = 2
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VentnActr02UrgcExist:
        sig_name = "VentnActr02UrgcExist"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01UrgcExist_False': 0, 'VentnActr01UrgcExist_True': 1, 'VentnActr01UrgcExist_Reserved': 2, 'VentnActr01UrgcExist_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 8
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VentnActr02TrqSts:
        sig_name = "VentnActr02TrqSts"
        sig_start_bit = 42
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 3
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotUrgcUnlck_Off': 0, 'VentnMotUrgcUnlck_On': 1, 'VentnMotUrgcUnlck_Reserved': 2, 'VentnMotUrgcUnlck_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 42
        byte = 5
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VentnActr02UrgcSts:
        sig_name = "VentnActr02UrgcSts"
        sig_start_bit = 56
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotUrgcUnlck_Off': 0, 'VentnMotUrgcUnlck_On': 1, 'VentnMotUrgcUnlck_Reserved': 2, 'VentnMotUrgcUnlck_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 56
        byte = 7
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VentnActr02BusAdr:
        sig_name = "VentnActr02BusAdr"
        sig_start_bit = 48
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 255
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 48
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VentnActr02MovDir:
        sig_name = "VentnActr02MovDir"
        sig_start_bit = 60
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotDir_CW': 0, 'VentnMotDir_CCW': 1, 'VentnMotDir_Reserved': 2, 'VentnMotDir_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 60
        byte = 7
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class VentnActr02ElecErr:
        sig_name = "VentnActr02ElecErr"
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
        sig_value_table = {'VentnActr01ElecErr_Normal': 0, 'VentnActr01ElecErr_ElecErr': 1, 'VentnActr01ElecErr_PrmntElecErr': 2, 'VentnActr01ElecErr_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 4
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class VentnActr02DrvDir:
        sig_name = "VentnActr02DrvDir"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01DrvDir_Downward': 0, 'VentnActr01DrvDir_Upward': 1, 'VentnActr01DrvDir_Initialization': 2, 'VentnActr01DrvDir_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 40
        byte = 5
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VentnActr02VoltErr:
        sig_name = "VentnActr02VoltErr"
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
        sig_value_table = {'VentnActr01VoltErr_Normal': 0, 'VentnActr01VoltErr_UnderVolt': 1, 'VentnActr01VoltErr_OvrVolt': 2, 'VentnActr01VoltErr_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 6
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class VgaCcm_Lin3Vga05Fr01:
    msg_name = "VgaCcm_Lin3Vga05Fr01"
    msg_id = 25
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "VGC"
    rx_nodes = ['CCM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class VentnActr05BusAdr:
        sig_name = "VentnActr05BusAdr"
        sig_start_bit = 48
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 255
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 48
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VentnActr05SpdSts:
        sig_name = "VentnActr05SpdSts"
        sig_start_bit = 20
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01SpdSts_Stop': 0, 'VentnActr01SpdSts_Speedlevel1': 1, 'VentnActr01SpdSts_Speedlevel2': 2, 'VentnActr01SpdSts_Speedlevel3': 3, 'VentnActr01SpdSts_Speedlevel4': 4, 'VentnActr01SpdSts_Autospeed': 5, 'VentnActr01SpdSts_Reserved0': 6, 'VentnActr01SpdSts_Reserved1': 7, 'VentnActr01SpdSts_Reserved2': 8, 'VentnActr01SpdSts_Reserved3': 9, 'VentnActr01SpdSts_Reserved4': 10, 'VentnActr01SpdSts_Reserved5': 11, 'VentnActr01SpdSts_Reserved6': 12, 'VentnActr01SpdSts_Reserved7': 13, 'VentnActr01SpdSts_Reserved8': 14, 'VentnActr01SpdSts_Signalinvalid': 15}
        compute_method = None
        length = 4
        startbit = 20
        byte = 2
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class VentnActr05ElecErr:
        sig_name = "VentnActr05ElecErr"
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
        sig_value_table = {'VentnActr01ElecErr_Normal': 0, 'VentnActr01ElecErr_ElecErr': 1, 'VentnActr01ElecErr_PrmntElecErr': 2, 'VentnActr01ElecErr_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 4
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class VentnActr05UrgcPson:
        sig_name = "VentnActr05UrgcPson"
        sig_start_bit = 58
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotUrgcPson_Bottom': 0, 'VentnMotUrgcPson_Top': 1, 'VentnMotUrgcPson_Reserved': 2, 'VentnMotUrgcPson_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 58
        byte = 7
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VentnActr05UrgcExist:
        sig_name = "VentnActr05UrgcExist"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01UrgcExist_False': 0, 'VentnActr01UrgcExist_True': 1, 'VentnActr01UrgcExist_Reserved': 2, 'VentnActr01UrgcExist_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 8
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VentnActr05OvrTempErr:
        sig_name = "VentnActr05OvrTempErr"
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
        sig_value_table = {'VentnActr01OvrTempErr_Normal': 0, 'VentnActr01OvrTempErr_OvrTempErr': 1, 'VentnActr01OvrTempErr_Reserved': 2, 'VentnActr01OvrTempErr_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 2
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VentnActr05PsonSts:
        sig_name = "VentnActr05PsonSts"
        sig_start_bit = 18
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotPsonAvl_Targetpositionvalid': 0, 'VentnMotPsonAvl_Startpositionvalid': 1, 'VentnMotPsonAvl_Bothpositionsinvalid': 2, 'VentnMotPsonAvl_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 18
        byte = 2
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VentnActr05BlckSts:
        sig_name = "VentnActr05BlckSts"
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
        sig_value_table = {'VentnActr01BlckSts_NoBlock': 0, 'VentnActr01BlckSts_Block': 1, 'VentnActr01BlckSts_Reserved': 2, 'VentnActr01BlckSts_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 12
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class VentnActr05TrqSts:
        sig_name = "VentnActr05TrqSts"
        sig_start_bit = 42
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 3
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotUrgcUnlck_Off': 0, 'VentnMotUrgcUnlck_On': 1, 'VentnMotUrgcUnlck_Reserved': 2, 'VentnMotUrgcUnlck_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 42
        byte = 5
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VentnActr05DrvDir:
        sig_name = "VentnActr05DrvDir"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01DrvDir_Downward': 0, 'VentnActr01DrvDir_Upward': 1, 'VentnActr01DrvDir_Initialization': 2, 'VentnActr01DrvDir_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 40
        byte = 5
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VentnActr05MovDir:
        sig_name = "VentnActr05MovDir"
        sig_start_bit = 60
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotDir_CW': 0, 'VentnMotDir_CCW': 1, 'VentnMotDir_Reserved': 2, 'VentnMotDir_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 60
        byte = 7
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class VentnActr05CoilSts:
        sig_name = "VentnActr05CoilSts"
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
        sig_value_table = {'VentnMotUrgcUnlck_Off': 0, 'VentnMotUrgcUnlck_On': 1, 'VentnMotUrgcUnlck_Reserved': 2, 'VentnMotUrgcUnlck_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 16
        byte = 2
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VentnActr05Mode:
        sig_name = "VentnActr05Mode"
        sig_start_bit = 62
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotMode_Normal': 0, 'VentnMotMode_Stop': 1, 'VentnMotMode_Reserved_orMaintainence': 2, 'VentnMotMode_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 62
        byte = 7
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class VentnActr05UrgcSts:
        sig_name = "VentnActr05UrgcSts"
        sig_start_bit = 56
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotUrgcUnlck_Off': 0, 'VentnMotUrgcUnlck_On': 1, 'VentnMotUrgcUnlck_Reserved': 2, 'VentnMotUrgcUnlck_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 56
        byte = 7
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VentnActr05ResetSts:
        sig_name = "VentnActr05ResetSts"
        sig_start_bit = 14
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01ResetSts_NoReset': 0, 'VentnActr01ResetSts_Reset': 1, 'VentnActr01ResetSts_Reserved': 2, 'VentnActr01ResetSts_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 14
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class VentnActr05SpclFct:
        sig_name = "VentnActr05SpclFct"
        sig_start_bit = 44
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 3
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01SpclFct_None': 0, 'VentnActr01SpclFct_SpecialFunction1active': 1, 'VentnActr01SpclFct_Reserved': 2, 'VentnActr01SpclFct_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 44
        byte = 5
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class VentnActr05BlckInd:
        sig_name = "VentnActr05BlckInd"
        sig_start_bit = 10
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01BlckInd_Disabled': 0, 'VentnActr01BlckInd_Enabled': 1, 'VentnActr01BlckInd_Reserved': 2, 'VentnActr01BlckInd_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 10
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VentnActr05ActPson:
        sig_name = "VentnActr05ActPson"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 32767
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 24
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111111, 0b00000000, 8, 0)]

    class VentnActr05VoltErr:
        sig_name = "VentnActr05VoltErr"
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
        sig_value_table = {'VentnActr01VoltErr_Normal': 0, 'VentnActr01VoltErr_UnderVolt': 1, 'VentnActr01VoltErr_OvrVolt': 2, 'VentnActr01VoltErr_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 6
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class VgaCcm_Lin3Vga04Fr01:
    msg_name = "VgaCcm_Lin3Vga04Fr01"
    msg_id = 23
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "VGC"
    rx_nodes = ['CCM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class VentnActr04UrgcSts:
        sig_name = "VentnActr04UrgcSts"
        sig_start_bit = 56
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotUrgcUnlck_Off': 0, 'VentnMotUrgcUnlck_On': 1, 'VentnMotUrgcUnlck_Reserved': 2, 'VentnMotUrgcUnlck_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 56
        byte = 7
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VentnActr04SpclFct:
        sig_name = "VentnActr04SpclFct"
        sig_start_bit = 44
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 3
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01SpclFct_None': 0, 'VentnActr01SpclFct_SpecialFunction1active': 1, 'VentnActr01SpclFct_Reserved': 2, 'VentnActr01SpclFct_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 44
        byte = 5
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class VentnActr04CoilSts:
        sig_name = "VentnActr04CoilSts"
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
        sig_value_table = {'VentnMotUrgcUnlck_Off': 0, 'VentnMotUrgcUnlck_On': 1, 'VentnMotUrgcUnlck_Reserved': 2, 'VentnMotUrgcUnlck_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 16
        byte = 2
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VentnActr04TrqSts:
        sig_name = "VentnActr04TrqSts"
        sig_start_bit = 42
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 3
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotUrgcUnlck_Off': 0, 'VentnMotUrgcUnlck_On': 1, 'VentnMotUrgcUnlck_Reserved': 2, 'VentnMotUrgcUnlck_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 42
        byte = 5
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VentnActr04MovDir:
        sig_name = "VentnActr04MovDir"
        sig_start_bit = 60
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotDir_CW': 0, 'VentnMotDir_CCW': 1, 'VentnMotDir_Reserved': 2, 'VentnMotDir_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 60
        byte = 7
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class VentnActr04ElecErr:
        sig_name = "VentnActr04ElecErr"
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
        sig_value_table = {'VentnActr01ElecErr_Normal': 0, 'VentnActr01ElecErr_ElecErr': 1, 'VentnActr01ElecErr_PrmntElecErr': 2, 'VentnActr01ElecErr_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 4
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class VentnActr04VoltErr:
        sig_name = "VentnActr04VoltErr"
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
        sig_value_table = {'VentnActr01VoltErr_Normal': 0, 'VentnActr01VoltErr_UnderVolt': 1, 'VentnActr01VoltErr_OvrVolt': 2, 'VentnActr01VoltErr_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 6
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class VentnActr04OvrTempErr:
        sig_name = "VentnActr04OvrTempErr"
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
        sig_value_table = {'VentnActr01OvrTempErr_Normal': 0, 'VentnActr01OvrTempErr_OvrTempErr': 1, 'VentnActr01OvrTempErr_Reserved': 2, 'VentnActr01OvrTempErr_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 2
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VentnActr04BlckSts:
        sig_name = "VentnActr04BlckSts"
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
        sig_value_table = {'VentnActr01BlckSts_NoBlock': 0, 'VentnActr01BlckSts_Block': 1, 'VentnActr01BlckSts_Reserved': 2, 'VentnActr01BlckSts_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 12
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class VentnActr04ResetSts:
        sig_name = "VentnActr04ResetSts"
        sig_start_bit = 14
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01ResetSts_NoReset': 0, 'VentnActr01ResetSts_Reset': 1, 'VentnActr01ResetSts_Reserved': 2, 'VentnActr01ResetSts_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 14
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class VentnActr04BlckInd:
        sig_name = "VentnActr04BlckInd"
        sig_start_bit = 10
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01BlckInd_Disabled': 0, 'VentnActr01BlckInd_Enabled': 1, 'VentnActr01BlckInd_Reserved': 2, 'VentnActr01BlckInd_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 10
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VentnActr04PsonSts:
        sig_name = "VentnActr04PsonSts"
        sig_start_bit = 18
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotPsonAvl_Targetpositionvalid': 0, 'VentnMotPsonAvl_Startpositionvalid': 1, 'VentnMotPsonAvl_Bothpositionsinvalid': 2, 'VentnMotPsonAvl_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 18
        byte = 2
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VentnActr04ActPson:
        sig_name = "VentnActr04ActPson"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 32767
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 24
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111111, 0b00000000, 8, 0)]

    class VentnActr04Mode:
        sig_name = "VentnActr04Mode"
        sig_start_bit = 62
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotMode_Normal': 0, 'VentnMotMode_Stop': 1, 'VentnMotMode_Reserved_orMaintainence': 2, 'VentnMotMode_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 62
        byte = 7
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class VentnActr04SpdSts:
        sig_name = "VentnActr04SpdSts"
        sig_start_bit = 20
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01SpdSts_Stop': 0, 'VentnActr01SpdSts_Speedlevel1': 1, 'VentnActr01SpdSts_Speedlevel2': 2, 'VentnActr01SpdSts_Speedlevel3': 3, 'VentnActr01SpdSts_Speedlevel4': 4, 'VentnActr01SpdSts_Autospeed': 5, 'VentnActr01SpdSts_Reserved0': 6, 'VentnActr01SpdSts_Reserved1': 7, 'VentnActr01SpdSts_Reserved2': 8, 'VentnActr01SpdSts_Reserved3': 9, 'VentnActr01SpdSts_Reserved4': 10, 'VentnActr01SpdSts_Reserved5': 11, 'VentnActr01SpdSts_Reserved6': 12, 'VentnActr01SpdSts_Reserved7': 13, 'VentnActr01SpdSts_Reserved8': 14, 'VentnActr01SpdSts_Signalinvalid': 15}
        compute_method = None
        length = 4
        startbit = 20
        byte = 2
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class VentnActr04UrgcPson:
        sig_name = "VentnActr04UrgcPson"
        sig_start_bit = 58
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnMotUrgcPson_Bottom': 0, 'VentnMotUrgcPson_Top': 1, 'VentnMotUrgcPson_Reserved': 2, 'VentnMotUrgcPson_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 58
        byte = 7
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VentnActr04UrgcExist:
        sig_name = "VentnActr04UrgcExist"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01UrgcExist_False': 0, 'VentnActr01UrgcExist_True': 1, 'VentnActr01UrgcExist_Reserved': 2, 'VentnActr01UrgcExist_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 8
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VentnActr04DrvDir:
        sig_name = "VentnActr04DrvDir"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01DrvDir_Downward': 0, 'VentnActr01DrvDir_Upward': 1, 'VentnActr01DrvDir_Initialization': 2, 'VentnActr01DrvDir_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 40
        byte = 5
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VentnActr04BusAdr:
        sig_name = "VentnActr04BusAdr"
        sig_start_bit = 48
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 255
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 48
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


