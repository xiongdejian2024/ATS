class CCUMCUCDInfoCANFDFr06:
    msg_name = "CCUMCUCDInfoCANFDFr06"
    msg_id = 659
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 64
    tx_node = "CCUMCUCD"
    rx_nodes = ['BNCM', 'CD', 'TPM', 'ETC']
    sig_group_dict = {'ActFusnSeatSts': ['ActFusnSeatStsDrvrSeatSts', 'ActFusnSeatStsPassSeatSts', 'ActFusnSeatStsSecRowLeSeatSts', 'ActFusnSeatStsSecRowMidSeatSts', 'ActFusnSeatStsSecRowRiSeatSts', 'ActFusnSeatStsThrdRowLeSeatSts', 'ActFusnSeatStsThrdRowMidSeatSts', 'ActFusnSeatStsThrdRowRiSeatSts'], 'AmbTEstimd': ['AmbTEstimdT', 'AmbTEstimdTQF'], 'VehDateAndTi': ['VehDateAndTiDay', 'VehDateAndTiHr', 'VehDateAndTiMins', 'VehDateAndTiMth', 'VehDateAndTiSec', 'VehDateAndTiValid', 'VehDateAndTiYr'], 'Vin': ['VinInfoBytePosn1', 'VinInfoBytePosn10', 'VinInfoBytePosn11', 'VinInfoBytePosn12', 'VinInfoBytePosn13', 'VinInfoBytePosn14', 'VinInfoBytePosn15', 'VinInfoBytePosn16', 'VinInfoBytePosn17', 'VinInfoBytePosn2', 'VinInfoBytePosn3', 'VinInfoBytePosn4', 'VinInfoBytePosn5', 'VinInfoBytePosn6', 'VinInfoBytePosn7', 'VinInfoBytePosn8', 'VinInfoBytePosn9'], 'VisFusnSeatSts': ['VisFusnSeatStsDrvrSeatSts', 'VisFusnSeatStsPassSeatSts', 'VisFusnSeatStsSecRowLeSeatSts', 'VisFusnSeatStsSecRowMidSeatSts', 'VisFusnSeatStsSecRowRiSeatSts', 'VisFusnSeatStsThrdRowLeSeatSts', 'VisFusnSeatStsThrdRowMidSeatSts', 'VisFusnSeatStsThrdRowRiSeatSts']}
    sig_group_dataid_dict = {}

    class CDSOCShutDwnReq:
        sig_name = "CDSOCShutDwnReq"
        sig_start_bit = 500
        update_id_bit = 443
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SOCShutDownReq_Idle': 0, 'SOCShutDownReq_STR': 1, 'SOCShutDownReq_OFF': 2, 'SOCShutDownReq_Reset': 3, 'SOCShutDownReq_ErrorOFF': 4}
        compute_method = None
        length = 3
        startbit = 500
        byte = 62
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class VinInfoBytePosn14:
        sig_name = "VinInfoBytePosn14"
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

    class VinInfoBytePosn1:
        sig_name = "VinInfoBytePosn1"
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

    class VisFusnSeatStsSecRowLeSeatSts:
        sig_name = "VisFusnSeatStsSecRowLeSeatSts"
        sig_start_bit = 411
        update_id_bit = None
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
        startbit = 411
        byte = 51
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class CDNADShutDwnStsExt:
        sig_name = "CDNADShutDwnStsExt"
        sig_start_bit = 494
        update_id_bit = 448
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 6
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SOCShutDownSts_Idle': 0, 'SOCShutDownSts_STRAck': 1, 'SOCShutDownSts_STRFailed': 2, 'SOCShutDownSts_STRDone': 3, 'SOCShutDownSts_OFFAck': 4, 'SOCShutDownSts_OFFAllowed': 5, 'SOCShutDownSts_ToStart': 6}
        compute_method = None
        length = 3
        startbit = 494
        byte = 61
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class VehDateAndTiMth:
        sig_name = "VehDateAndTiMth"
        sig_start_bit = 268
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 3
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 268
        byte = 33
        mask = 0b00011110
        unmask = 0b11100001
        shift = 1

    class ActFusnSeatStsThrdRowMidSeatSts:
        sig_name = "ActFusnSeatStsThrdRowMidSeatSts"
        sig_start_bit = 9
        update_id_bit = None
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
        startbit = 9
        byte = 1
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class ActFusnSeatStsSecRowMidSeatSts:
        sig_name = "ActFusnSeatStsSecRowMidSeatSts"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 12
        byte = 1
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VinInfoBytePosn13:
        sig_name = "VinInfoBytePosn13"
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

    class DisplayMode:
        sig_name = "DisplayMode"
        sig_start_bit = 436
        update_id_bit = 441
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DisplayMode_Unknow': 0, 'DisplayMode_DayMode': 1, 'DisplayMode_NightMode': 2, 'DisplayMode_Reserved1': 3}
        compute_method = None
        length = 2
        startbit = 436
        byte = 54
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class CDNADStrtStsExt:
        sig_name = "CDNADStrtStsExt"
        sig_start_bit = 491
        update_id_bit = 488
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SOCStrtSts_Idle': 0, 'SOCStrtSts_ColdStartInit': 1, 'SOCStrtSts_ColdStartComplete': 2, 'SOCStrtSts_WarmStartInit': 3, 'SOCStrtSts_WarmStartComplete': 4, 'SOCStrtSts_Failed': 5}
        compute_method = None
        length = 3
        startbit = 491
        byte = 61
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class CDSOCOperModSts:
        sig_name = "CDSOCOperModSts"
        sig_start_bit = 503
        update_id_bit = 442
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CDSOCOperModSts_Lite': 0, 'CDSOCOperModSts_Standard': 1, 'CDSOCOperModSts_StandardFOTA': 2, 'CDSOCOperModSts_StandardStamina': 3}
        compute_method = None
        length = 3
        startbit = 503
        byte = 62
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class ScreenDispErrProcess:
        sig_name = "ScreenDispErrProcess"
        sig_start_bit = 434
        update_id_bit = 455
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 2
        startbit = 434
        byte = 54
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class VehDateAndTiValid:
        sig_name = "VehDateAndTiValid"
        sig_start_bit = 240
        update_id_bit = None
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
        startbit = 240
        byte = 30
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ActFusnSeatSts_UB:
        sig_name = "ActFusnSeatSts_UB"
        sig_start_bit = 444
        update_id_bit = 444
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
        startbit = 444
        byte = 55
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class RTPReqSts:
        sig_name = "RTPReqSts"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VinInfoBytePosn3:
        sig_name = "VinInfoBytePosn3"
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

    class VisFusnSeatStsSecRowMidSeatSts:
        sig_name = "VisFusnSeatStsSecRowMidSeatSts"
        sig_start_bit = 412
        update_id_bit = None
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
        startbit = 412
        byte = 51
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class AmbTEstimdTQF:
        sig_name = "AmbTEstimdTQF"
        sig_start_bit = 421
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HVACTempQf_SnsrDataNotOk': 0, 'HVACTempQf_SnsrDataOk': 1}
        compute_method = None
        length = 1
        startbit = 421
        byte = 52
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class ActFusnSeatStsThrdRowLeSeatSts:
        sig_name = "ActFusnSeatStsThrdRowLeSeatSts"
        sig_start_bit = 10
        update_id_bit = None
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
        startbit = 10
        byte = 1
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class AmbTEstimd_UB:
        sig_name = "AmbTEstimd_UB"
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

    class CDNADRstReqExt:
        sig_name = "CDNADRstReqExt"
        sig_start_bit = 475
        update_id_bit = 496
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
        startbit = 475
        byte = 59
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VisFusnSeatStsThrdRowLeSeatSts:
        sig_name = "VisFusnSeatStsThrdRowLeSeatSts"
        sig_start_bit = 415
        update_id_bit = None
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
        startbit = 415
        byte = 51
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class CDNADShutDwnReqExt:
        sig_name = "CDNADShutDwnReqExt"
        sig_start_bit = 474
        update_id_bit = 454
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SOCShutDownReq_Idle': 0, 'SOCShutDownReq_STR': 1, 'SOCShutDownReq_OFF': 2, 'SOCShutDownReq_Reset': 3, 'SOCShutDownReq_ErrorOFF': 4}
        compute_method = None
        length = 3
        startbit = 474
        byte = 59
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class VehDateAndTi_UB:
        sig_name = "VehDateAndTi_UB"
        sig_start_bit = 452
        update_id_bit = 452
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
        startbit = 452
        byte = 56
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class SetDigKeyWakeUpZone:
        sig_name = "SetDigKeyWakeUpZone"
        sig_start_bit = 471
        update_id_bit = 467
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DigKeyWakeUpZone_Unkown': 0, 'DigKeyWakeUpZone_Connected': 1, 'DigKeyWakeUpZone_Welcome': 2, 'DigKeyWakeUpZone_WalkAway': 3, 'DigKeyWakeUpZone_PE': 4, 'DigKeyWakeUpZone_Reserved1': 5, 'DigKeyWakeUpZone_Reserved2': 6, 'DigKeyWakeUpZone_Reserved3': 7}
        compute_method = None
        length = 3
        startbit = 471
        byte = 58
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class CallSysWarnSts:
        sig_name = "CallSysWarnSts"
        sig_start_bit = 479
        update_id_bit = 466
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CallSysWarnSts_Unkown': 0, 'CallSysWarnSts_Normal': 1, 'CallSysWarnSts_MinorFailure': 2, 'CallSysWarnSts_MajorFailure': 3}
        compute_method = None
        length = 2
        startbit = 479
        byte = 59
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class VehDateAndTiHr:
        sig_name = "VehDateAndTiHr"
        sig_start_bit = 263
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
        startbit = 263
        byte = 32
        mask = 0b11111000
        unmask = 0b00000111
        shift = 3

    class AmbTEstimdT:
        sig_name = "AmbTEstimdT"
        sig_start_bit = 420
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = -256.0
        sig_value_min = 0
        sig_value_max = 5119
        sig_byteorder = "Motorola"
        sig_value_init = 2560
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 420
        bmuws_info = [(52, 0b00011111, 0b11100000, 5, 0), (53, 0b11111111, 0b00000000, 8, 0)]

    class CDNADHeartBeatSigExt:
        sig_name = "CDNADHeartBeatSigExt"
        sig_start_bit = 487
        update_id_bit = 464
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
        startbit = 487
        byte = 60
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VisFusnSeatStsThrdRowMidSeatSts:
        sig_name = "VisFusnSeatStsThrdRowMidSeatSts"
        sig_start_bit = 410
        update_id_bit = None
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
        startbit = 410
        byte = 51
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class MuteReqSts:
        sig_name = "MuteReqSts"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VinInfoBytePosn6:
        sig_name = "VinInfoBytePosn6"
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

    class VisFusnUsrInCarSts:
        sig_name = "VisFusnUsrInCarSts"
        sig_start_bit = 423
        update_id_bit = 449
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
        startbit = 423
        byte = 52
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ActFusnSeatStsDrvrSeatSts:
        sig_name = "ActFusnSeatStsDrvrSeatSts"
        sig_start_bit = 15
        update_id_bit = None
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
        startbit = 15
        byte = 1
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ActFusnSeatStsSecRowLeSeatSts:
        sig_name = "ActFusnSeatStsSecRowLeSeatSts"
        sig_start_bit = 13
        update_id_bit = None
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
        startbit = 13
        byte = 1
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VinInfoBytePosn9:
        sig_name = "VinInfoBytePosn9"
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

    class ActFusnSeatStsSecRowRiSeatSts:
        sig_name = "ActFusnSeatStsSecRowRiSeatSts"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 11
        byte = 1
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class CCUCDPwrSrcExt:
        sig_name = "CCUCDPwrSrcExt"
        sig_start_bit = 477
        update_id_bit = 465
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CCUPwrSrc_Unknown': 0, 'CCUPwrSrc_KL30': 1, 'CCUPwrSrc_BackupBattery': 2}
        compute_method = None
        length = 2
        startbit = 477
        byte = 59
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class VinInfoBytePosn7:
        sig_name = "VinInfoBytePosn7"
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

    class UsrInCarSts:
        sig_name = "UsrInCarSts"
        sig_start_bit = 239
        update_id_bit = 453
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
        startbit = 239
        byte = 29
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class SetDigKeyMaxWakeUpTime:
        sig_name = "SetDigKeyMaxWakeUpTime"
        sig_start_bit = 463
        update_id_bit = 468
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
        startbit = 463
        byte = 57
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VinInfoBytePosn4:
        sig_name = "VinInfoBytePosn4"
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

    class Vin_UB:
        sig_name = "Vin_UB"
        sig_start_bit = 451
        update_id_bit = 451
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
        startbit = 451
        byte = 56
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VinInfoBytePosn17:
        sig_name = "VinInfoBytePosn17"
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

    class VinInfoBytePosn10:
        sig_name = "VinInfoBytePosn10"
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

    class VisFusnSeatStsDrvrSeatSts:
        sig_name = "VisFusnSeatStsDrvrSeatSts"
        sig_start_bit = 408
        update_id_bit = None
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
        startbit = 408
        byte = 51
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VehDateAndTiMins:
        sig_name = "VehDateAndTiMins"
        sig_start_bit = 258
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
        startbit = 258
        bmuws_info = [(32, 0b00000111, 0b11111000, 3, 0), (33, 0b11100000, 0b00011111, 3, 5)]

    class VinInfoBytePosn11:
        sig_name = "VinInfoBytePosn11"
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

    class VehDateAndTiDay:
        sig_name = "VehDateAndTiDay"
        sig_start_bit = 247
        update_id_bit = None
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 2
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 247
        byte = 30
        mask = 0b11111000
        unmask = 0b00000111
        shift = 3

    class VehDateAndTiSec:
        sig_name = "VehDateAndTiSec"
        sig_start_bit = 237
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
        startbit = 237
        byte = 29
        mask = 0b00111111
        unmask = 0b11000000
        shift = 0

    class VisFusnSeatStsThrdRowRiSeatSts:
        sig_name = "VisFusnSeatStsThrdRowRiSeatSts"
        sig_start_bit = 413
        update_id_bit = None
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
        startbit = 413
        byte = 51
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VinInfoBytePosn5:
        sig_name = "VinInfoBytePosn5"
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

    class ActFusnSeatStsThrdRowRiSeatSts:
        sig_name = "ActFusnSeatStsThrdRowRiSeatSts"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 8
        byte = 1
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ActFusnSeatStsPassSeatSts:
        sig_name = "ActFusnSeatStsPassSeatSts"
        sig_start_bit = 14
        update_id_bit = None
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
        startbit = 14
        byte = 1
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VisFusnSeatSts_UB:
        sig_name = "VisFusnSeatSts_UB"
        sig_start_bit = 450
        update_id_bit = 450
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
        startbit = 450
        byte = 56
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VisFusnSeatStsPassSeatSts:
        sig_name = "VisFusnSeatStsPassSeatSts"
        sig_start_bit = 409
        update_id_bit = None
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
        startbit = 409
        byte = 51
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class CDNADKeepPwrReqExt:
        sig_name = "CDNADKeepPwrReqExt"
        sig_start_bit = 495
        update_id_bit = 497
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
        startbit = 495
        byte = 61
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VehDateAndTiYr:
        sig_name = "VehDateAndTiYr"
        sig_start_bit = 255
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 21
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 255
        byte = 31
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class OnBdChrgrHndlSts:
        sig_name = "OnBdChrgrHndlSts"
        sig_start_bit = 3
        update_id_bit = 264
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 14
        sig_byteorder = "Motorola"
        sig_value_init = 8
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OBCChrgrHndlSt_Disconnected': 0, 'OBCChrgrHndlSt_ConnectedWithoutPower': 1, 'OBCChrgrHndlSt_PowerAvailableButNotActivated': 2, 'OBCChrgrHndlSt_ConnectedWithPower': 3, 'OBCChrgrHndlSt_DischargeConnectwithoutpowerincar': 4, 'OBCChrgrHndlSt_DischargeConnectwithoutpoweroutcar': 5, 'OBCChrgrHndlSt_DischargeConnectwithpowerincar': 6, 'OBCChrgrHndlSt_DischargeConnectwithpoweroutcar': 7, 'OBCChrgrHndlSt_Init': 8, 'OBCChrgrHndlSt_Fault': 9, 'OBCChrgrHndlSt_NotCompleteConnnected': 10, 'OBCChrgrHndlSt_ConnectedWithPowerButNotPWM': 11, 'OBCChrgrHndlSt_Reserved1': 12, 'OBCChrgrHndlSt_Reserved2': 13, 'OBCChrgrHndlSt_Reserved3': 14}
        compute_method = None
        length = 4
        startbit = 3
        byte = 0
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class VinInfoBytePosn15:
        sig_name = "VinInfoBytePosn15"
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

    class VinInfoBytePosn16:
        sig_name = "VinInfoBytePosn16"
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

    class VisFusnSeatStsSecRowRiSeatSts:
        sig_name = "VisFusnSeatStsSecRowRiSeatSts"
        sig_start_bit = 414
        update_id_bit = None
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
        startbit = 414
        byte = 51
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VinInfoBytePosn8:
        sig_name = "VinInfoBytePosn8"
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

    class VinInfoBytePosn2:
        sig_name = "VinInfoBytePosn2"
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

    class VinInfoBytePosn12:
        sig_name = "VinInfoBytePosn12"
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


class CCUMCUCDtoBNCMDigKeyRemReqInfoCANFDFrame:
    msg_name = "CCUMCUCDtoBNCMDigKeyRemReqInfoCANFDFrame"
    msg_id = 772
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "CCUMCUCD"
    rx_nodes = ['BNCM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class CCUMCUCDInfoCANFDFr11:
    msg_name = "CCUMCUCDInfoCANFDFr11"
    msg_id = 1
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CCUMCUCD"
    rx_nodes = ['DRF', 'ETC']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class RoofFolderDisplayFoldedReq:
        sig_name = "RoofFolderDisplayFoldedReq"
        sig_start_bit = 15
        update_id_bit = 11
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 2
        startbit = 15
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class RoofFolderDisplayBrightnessLevelReq:
        sig_name = "RoofFolderDisplayBrightnessLevelReq"
        sig_start_bit = 7
        update_id_bit = 12
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "SCALE_LINEAR_AND_TEXTTABLE"
        sig_value_table = {'BattSOH_Invalid': 255}
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class BNCMInfoCANFDFr08:
    msg_name = "BNCMInfoCANFDFr08"
    msg_id = 523
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 64
    tx_node = "BNCM"
    rx_nodes = ['ETC']
    sig_group_dict = {'DigKeyLocData3': ['DigKeyLocData3CalibrationDataByte0', 'DigKeyLocData3CalibrationDataByte1', 'DigKeyLocData3CalibrationDataByte10', 'DigKeyLocData3CalibrationDataByte11', 'DigKeyLocData3CalibrationDataByte12', 'DigKeyLocData3CalibrationDataByte13', 'DigKeyLocData3CalibrationDataByte14', 'DigKeyLocData3CalibrationDataByte15', 'DigKeyLocData3CalibrationDataByte16', 'DigKeyLocData3CalibrationDataByte17', 'DigKeyLocData3CalibrationDataByte18', 'DigKeyLocData3CalibrationDataByte19', 'DigKeyLocData3CalibrationDataByte2', 'DigKeyLocData3CalibrationDataByte3', 'DigKeyLocData3CalibrationDataByte4', 'DigKeyLocData3CalibrationDataByte5', 'DigKeyLocData3CalibrationDataByte6', 'DigKeyLocData3CalibrationDataByte7', 'DigKeyLocData3CalibrationDataByte8', 'DigKeyLocData3CalibrationDataByte9', 'DigKeyLocData3FrntLeBLERSSI', 'DigKeyLocData3FrntLeUWBDistance', 'DigKeyLocData3FrntRiBLERSSI', 'DigKeyLocData3FrntRiUWBDistance', 'DigKeyLocData3InVehReBLERSSI', 'DigKeyLocData3InVehReUWBDistance', 'DigKeyLocData3KeyIdByte0', 'DigKeyLocData3KeyIdByte1', 'DigKeyLocData3KeyIdByte10', 'DigKeyLocData3KeyIdByte11', 'DigKeyLocData3KeyIdByte12', 'DigKeyLocData3KeyIdByte13', 'DigKeyLocData3KeyIdByte14', 'DigKeyLocData3KeyIdByte15', 'DigKeyLocData3KeyIdByte2', 'DigKeyLocData3KeyIdByte3', 'DigKeyLocData3KeyIdByte4', 'DigKeyLocData3KeyIdByte5', 'DigKeyLocData3KeyIdByte6', 'DigKeyLocData3KeyIdByte7', 'DigKeyLocData3KeyIdByte8', 'DigKeyLocData3KeyIdByte9', 'DigKeyLocData3MainBLERSSI', 'DigKeyLocData3MainUWBDistance', 'DigKeyLocData3ReLeBLERSSI', 'DigKeyLocData3ReLeUWBDistance', 'DigKeyLocData3ReRiBLERSSI', 'DigKeyLocData3ReRiUWBDistance']}
    sig_group_dataid_dict = {}

    class DigKeyLocData3CalibrationDataByte5:
        sig_name = "DigKeyLocData3CalibrationDataByte5"
        sig_start_bit = 191
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
        startbit = 191
        byte = 23
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData3KeyIdByte13:
        sig_name = "DigKeyLocData3KeyIdByte13"
        sig_start_bit = 415
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
        startbit = 415
        byte = 51
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData3CalibrationDataByte1:
        sig_name = "DigKeyLocData3CalibrationDataByte1"
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

    class DigKeyLocData3KeyIdByte2:
        sig_name = "DigKeyLocData3KeyIdByte2"
        sig_start_bit = 327
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
        startbit = 327
        byte = 40
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData3CalibrationDataByte2:
        sig_name = "DigKeyLocData3CalibrationDataByte2"
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

    class DigKeyLocData3ReRiUWBDistance:
        sig_name = "DigKeyLocData3ReRiUWBDistance"
        sig_start_bit = 63
        update_id_bit = None
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 65535
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 63
        bmuws_info = [(7, 0b11111111, 0b00000000, 8, 0), (8, 0b11111111, 0b00000000, 8, 0)]

    class DigKeyLocData3CalibrationDataByte4:
        sig_name = "DigKeyLocData3CalibrationDataByte4"
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

    class DigKeyLocData3KeyIdByte11:
        sig_name = "DigKeyLocData3KeyIdByte11"
        sig_start_bit = 399
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
        startbit = 399
        byte = 49
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData3CalibrationDataByte11:
        sig_name = "DigKeyLocData3CalibrationDataByte11"
        sig_start_bit = 239
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
        startbit = 239
        byte = 29
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData3KeyIdByte8:
        sig_name = "DigKeyLocData3KeyIdByte8"
        sig_start_bit = 375
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
        startbit = 375
        byte = 46
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData3InVehReBLERSSI:
        sig_name = "DigKeyLocData3InVehReBLERSSI"
        sig_start_bit = 127
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
        startbit = 127
        byte = 15
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData3CalibrationDataByte6:
        sig_name = "DigKeyLocData3CalibrationDataByte6"
        sig_start_bit = 199
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
        startbit = 199
        byte = 24
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData3KeyIdByte9:
        sig_name = "DigKeyLocData3KeyIdByte9"
        sig_start_bit = 383
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
        startbit = 383
        byte = 47
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData3CalibrationDataByte8:
        sig_name = "DigKeyLocData3CalibrationDataByte8"
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

    class DigKeyLocData3KeyIdByte5:
        sig_name = "DigKeyLocData3KeyIdByte5"
        sig_start_bit = 351
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
        startbit = 351
        byte = 43
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData3MainBLERSSI:
        sig_name = "DigKeyLocData3MainBLERSSI"
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

    class DigKeyLocData3KeyIdByte6:
        sig_name = "DigKeyLocData3KeyIdByte6"
        sig_start_bit = 359
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
        startbit = 359
        byte = 44
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData3KeyIdByte7:
        sig_name = "DigKeyLocData3KeyIdByte7"
        sig_start_bit = 367
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
        startbit = 367
        byte = 45
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData3FrntRiBLERSSI:
        sig_name = "DigKeyLocData3FrntRiBLERSSI"
        sig_start_bit = 103
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
        startbit = 103
        byte = 12
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData3ReLeUWBDistance:
        sig_name = "DigKeyLocData3ReLeUWBDistance"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 65535
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class DigKeyLocData3KeyIdByte4:
        sig_name = "DigKeyLocData3KeyIdByte4"
        sig_start_bit = 343
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
        startbit = 343
        byte = 42
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData3CalibrationDataByte9:
        sig_name = "DigKeyLocData3CalibrationDataByte9"
        sig_start_bit = 223
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
        startbit = 223
        byte = 27
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData3CalibrationDataByte15:
        sig_name = "DigKeyLocData3CalibrationDataByte15"
        sig_start_bit = 271
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
        startbit = 271
        byte = 33
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData3CalibrationDataByte0:
        sig_name = "DigKeyLocData3CalibrationDataByte0"
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

    class DigKeyLocData3CalibrationDataByte13:
        sig_name = "DigKeyLocData3CalibrationDataByte13"
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

    class DigKeyLocData3FrntLeUWBDistance:
        sig_name = "DigKeyLocData3FrntLeUWBDistance"
        sig_start_bit = 87
        update_id_bit = None
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 65535
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 87
        bmuws_info = [(10, 0b11111111, 0b00000000, 8, 0), (11, 0b11111111, 0b00000000, 8, 0)]

    class DigKeyLocData3CalibrationDataByte7:
        sig_name = "DigKeyLocData3CalibrationDataByte7"
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

    class DigKeyLocData3MainUWBDistance:
        sig_name = "DigKeyLocData3MainUWBDistance"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 65535
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 15
        bmuws_info = [(1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DigKeyLocData3KeyIdByte10:
        sig_name = "DigKeyLocData3KeyIdByte10"
        sig_start_bit = 391
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
        startbit = 391
        byte = 48
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData3KeyIdByte0:
        sig_name = "DigKeyLocData3KeyIdByte0"
        sig_start_bit = 311
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
        startbit = 311
        byte = 38
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData3FrntLeBLERSSI:
        sig_name = "DigKeyLocData3FrntLeBLERSSI"
        sig_start_bit = 79
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
        startbit = 79
        byte = 9
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData3ReLeBLERSSI:
        sig_name = "DigKeyLocData3ReLeBLERSSI"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData3KeyIdByte1:
        sig_name = "DigKeyLocData3KeyIdByte1"
        sig_start_bit = 319
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
        startbit = 319
        byte = 39
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData3CalibrationDataByte14:
        sig_name = "DigKeyLocData3CalibrationDataByte14"
        sig_start_bit = 263
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
        startbit = 263
        byte = 32
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData3KeyIdByte14:
        sig_name = "DigKeyLocData3KeyIdByte14"
        sig_start_bit = 423
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
        startbit = 423
        byte = 52
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData3KeyIdByte12:
        sig_name = "DigKeyLocData3KeyIdByte12"
        sig_start_bit = 407
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
        startbit = 407
        byte = 50
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData3CalibrationDataByte10:
        sig_name = "DigKeyLocData3CalibrationDataByte10"
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

    class DigKeyLocData3CalibrationDataByte17:
        sig_name = "DigKeyLocData3CalibrationDataByte17"
        sig_start_bit = 287
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
        startbit = 287
        byte = 35
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData3ReRiBLERSSI:
        sig_name = "DigKeyLocData3ReRiBLERSSI"
        sig_start_bit = 55
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
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData3CalibrationDataByte3:
        sig_name = "DigKeyLocData3CalibrationDataByte3"
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

    class DigKeyLocData3CalibrationDataByte18:
        sig_name = "DigKeyLocData3CalibrationDataByte18"
        sig_start_bit = 295
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
        startbit = 295
        byte = 36
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData3FrntRiUWBDistance:
        sig_name = "DigKeyLocData3FrntRiUWBDistance"
        sig_start_bit = 111
        update_id_bit = None
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 65535
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 111
        bmuws_info = [(13, 0b11111111, 0b00000000, 8, 0), (14, 0b11111111, 0b00000000, 8, 0)]

    class DigKeyLocData3KeyIdByte3:
        sig_name = "DigKeyLocData3KeyIdByte3"
        sig_start_bit = 335
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
        startbit = 335
        byte = 41
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData3CalibrationDataByte19:
        sig_name = "DigKeyLocData3CalibrationDataByte19"
        sig_start_bit = 303
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
        startbit = 303
        byte = 37
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData3CalibrationDataByte12:
        sig_name = "DigKeyLocData3CalibrationDataByte12"
        sig_start_bit = 247
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
        startbit = 247
        byte = 30
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData3KeyIdByte15:
        sig_name = "DigKeyLocData3KeyIdByte15"
        sig_start_bit = 431
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
        startbit = 431
        byte = 53
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData3CalibrationDataByte16:
        sig_name = "DigKeyLocData3CalibrationDataByte16"
        sig_start_bit = 279
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
        startbit = 279
        byte = 34
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData3InVehReUWBDistance:
        sig_name = "DigKeyLocData3InVehReUWBDistance"
        sig_start_bit = 135
        update_id_bit = None
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 65535
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 135
        bmuws_info = [(16, 0b11111111, 0b00000000, 8, 0), (17, 0b11111111, 0b00000000, 8, 0)]


class CCUMCUCDInfoCANFDFr04:
    msg_name = "CCUMCUCDInfoCANFDFr04"
    msg_id = 402
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 64
    tx_node = "CCUMCUCD"
    rx_nodes = ['BNCM', 'CD', 'WPC3', 'WPC2', 'ETC']
    sig_group_dict = {'FRDoorPosnSts': ['FRDoorPosnStsDoorAngPosn', 'FRDoorPosnStsDoorPercPosn'], 'KeyFindRespToService': ['KeyFindRespToServiceKeyFindSts', 'KeyFindRespToServiceKeyIdByte0', 'KeyFindRespToServiceKeyIdByte1', 'KeyFindRespToServiceKeyIdByte10', 'KeyFindRespToServiceKeyIdByte11', 'KeyFindRespToServiceKeyIdByte12', 'KeyFindRespToServiceKeyIdByte13', 'KeyFindRespToServiceKeyIdByte14', 'KeyFindRespToServiceKeyIdByte15', 'KeyFindRespToServiceKeyIdByte2', 'KeyFindRespToServiceKeyIdByte3', 'KeyFindRespToServiceKeyIdByte4', 'KeyFindRespToServiceKeyIdByte5', 'KeyFindRespToServiceKeyIdByte6', 'KeyFindRespToServiceKeyIdByte7', 'KeyFindRespToServiceKeyIdByte8', 'KeyFindRespToServiceKeyIdByte9', 'KeyFindRespToServiceKeyLocnSts', 'KeyFindRespToServiceKeyTyp'], 'KeyFindRespToVMM': ['KeyFindRespToVMMKeyFindSts', 'KeyFindRespToVMMKeyIdByte0', 'KeyFindRespToVMMKeyIdByte1', 'KeyFindRespToVMMKeyIdByte10', 'KeyFindRespToVMMKeyIdByte11', 'KeyFindRespToVMMKeyIdByte12', 'KeyFindRespToVMMKeyIdByte13', 'KeyFindRespToVMMKeyIdByte14', 'KeyFindRespToVMMKeyIdByte15', 'KeyFindRespToVMMKeyIdByte2', 'KeyFindRespToVMMKeyIdByte3', 'KeyFindRespToVMMKeyIdByte4', 'KeyFindRespToVMMKeyIdByte5', 'KeyFindRespToVMMKeyIdByte6', 'KeyFindRespToVMMKeyIdByte7', 'KeyFindRespToVMMKeyIdByte8', 'KeyFindRespToVMMKeyIdByte9', 'KeyFindRespToVMMKeyLocnSts', 'KeyFindRespToVMMKeyTyp'], 'KeyFindRespToLockg': ['KeyFindRespToLockgKeyFindSts', 'KeyFindRespToLockgKeyIdByte0', 'KeyFindRespToLockgKeyIdByte1', 'KeyFindRespToLockgKeyIdByte10', 'KeyFindRespToLockgKeyIdByte11', 'KeyFindRespToLockgKeyIdByte12', 'KeyFindRespToLockgKeyIdByte13', 'KeyFindRespToLockgKeyIdByte14', 'KeyFindRespToLockgKeyIdByte15', 'KeyFindRespToLockgKeyIdByte2', 'KeyFindRespToLockgKeyIdByte3', 'KeyFindRespToLockgKeyIdByte4', 'KeyFindRespToLockgKeyIdByte5', 'KeyFindRespToLockgKeyIdByte6', 'KeyFindRespToLockgKeyIdByte7', 'KeyFindRespToLockgKeyIdByte8', 'KeyFindRespToLockgKeyIdByte9', 'KeyFindRespToLockgKeyLocnSts', 'KeyFindRespToLockgKeyTyp'], 'ChargeLidAntiPnchSts': ['ChargeLidAntiPnchStsCloseAntiPnchSts', 'ChargeLidAntiPnchStsOPenAntiPnchSts'], 'FRDoorAntiPnchFb': ['FRDoorAntiPnchFbCloseAntiPnchSts', 'FRDoorAntiPnchFbOPenAntiPnchSts'], 'SeatOccpSts': ['SeatOccpStsDrvrSeatSts', 'SeatOccpStsPassSeatSts', 'SeatOccpStsSecRowLeSeatSts', 'SeatOccpStsSecRowMidSeatSts', 'SeatOccpStsSecRowRiSeatSts', 'SeatOccpStsThrdRowLeSeatSts', 'SeatOccpStsThrdRowMidSeatSts', 'SeatOccpStsThrdRowRiSeatSts'], 'FLDoorAntiPnchFb': ['FLDoorAntiPnchFbCloseAntiPnchSts', 'FLDoorAntiPnchFbOPenAntiPnchSts'], 'FLDoorPosnSts': ['FLDoorPosnStsDoorAngPosn', 'FLDoorPosnStsDoorPercPosn']}
    sig_group_dataid_dict = {}

    class SeatOccpStsSecRowLeSeatSts:
        sig_name = "SeatOccpStsSecRowLeSeatSts"
        sig_start_bit = 493
        update_id_bit = None
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
        startbit = 493
        byte = 61
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class KeyFindRespToServiceKeyIdByte13:
        sig_name = "KeyFindRespToServiceKeyIdByte13"
        sig_start_bit = 247
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
        startbit = 247
        byte = 30
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class KeyFindRespToServiceKeyIdByte6:
        sig_name = "KeyFindRespToServiceKeyIdByte6"
        sig_start_bit = 271
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
        startbit = 271
        byte = 33
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class KeyFindRespToServiceKeyIdByte2:
        sig_name = "KeyFindRespToServiceKeyIdByte2"
        sig_start_bit = 239
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
        startbit = 239
        byte = 29
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class KeyFindRespToServiceKeyFindSts:
        sig_name = "KeyFindRespToServiceKeyFindSts"
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
        sig_value_table = {'KeyPrsntSts_Idle': 0, 'KeyPrsntSts_InProgs': 1, 'KeyPrsntSts_NotPrsnt': 2, 'KeyPrsntSts_Prsnt': 3}
        compute_method = None
        length = 2
        startbit = 149
        byte = 18
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class FRDoorAntiPnchFbCloseAntiPnchSts:
        sig_name = "FRDoorAntiPnchFbCloseAntiPnchSts"
        sig_start_bit = 441
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
        startbit = 441
        byte = 55
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class KeyFindRespToVMMKeyIdByte1:
        sig_name = "KeyFindRespToVMMKeyIdByte1"
        sig_start_bit = 383
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
        startbit = 383
        byte = 47
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class KeyFindRespToLockgKeyIdByte3:
        sig_name = "KeyFindRespToLockgKeyIdByte3"
        sig_start_bit = 111
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
        startbit = 111
        byte = 13
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class KeyFindRespToLockgKeyIdByte0:
        sig_name = "KeyFindRespToLockgKeyIdByte0"
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

    class KeyFindRespToServiceKeyIdByte12:
        sig_name = "KeyFindRespToServiceKeyIdByte12"
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

    class FRDoorPosnSts_UB:
        sig_name = "FRDoorPosnSts_UB"
        sig_start_bit = 484
        update_id_bit = 484
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
        startbit = 484
        byte = 60
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class KeyFindRespToServiceKeyIdByte4:
        sig_name = "KeyFindRespToServiceKeyIdByte4"
        sig_start_bit = 191
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
        startbit = 191
        byte = 23
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class KeyFindRespToVMMKeyIdByte12:
        sig_name = "KeyFindRespToVMMKeyIdByte12"
        sig_start_bit = 303
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
        startbit = 303
        byte = 37
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class KeyFindRespToVMMKeyIdByte13:
        sig_name = "KeyFindRespToVMMKeyIdByte13"
        sig_start_bit = 319
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
        startbit = 319
        byte = 39
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FRDoorMtnSts:
        sig_name = "FRDoorMtnSts"
        sig_start_bit = 431
        update_id_bit = 485
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 9
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorMtnSts_IniVal': 0, 'DoorMtnSts_FullOpen': 1, 'DoorMtnSts_FullClose': 2, 'DoorMtnSts_StopDurOpen': 3, 'DoorMtnSts_StopDurClose': 4, 'DoorMtnSts_MovingOut': 5, 'DoorMtnSts_MovingIn': 6, 'DoorMtnSts_HalfClose': 7, 'DoorMtnSts_Unknow': 8, 'DoorMtnSts_OnlyOpenPosn': 9}
        compute_method = None
        length = 4
        startbit = 431
        byte = 53
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class KeyFindRespToService_UB:
        sig_name = "KeyFindRespToService_UB"
        sig_start_bit = 481
        update_id_bit = 481
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
        startbit = 481
        byte = 60
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class KeyFindRespToLockgKeyIdByte6:
        sig_name = "KeyFindRespToLockgKeyIdByte6"
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

    class KeyFindRespToLockgKeyIdByte2:
        sig_name = "KeyFindRespToLockgKeyIdByte2"
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

    class KeyFindRespToVMMKeyIdByte2:
        sig_name = "KeyFindRespToVMMKeyIdByte2"
        sig_start_bit = 311
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
        startbit = 311
        byte = 38
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class KeyFindRespToVMMKeyIdByte9:
        sig_name = "KeyFindRespToVMMKeyIdByte9"
        sig_start_bit = 375
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
        startbit = 375
        byte = 46
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SeatOccpStsSecRowMidSeatSts:
        sig_name = "SeatOccpStsSecRowMidSeatSts"
        sig_start_bit = 492
        update_id_bit = None
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
        startbit = 492
        byte = 61
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class KeyFindRespToLockgKeyIdByte15:
        sig_name = "KeyFindRespToLockgKeyIdByte15"
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

    class KeyFindRespToServiceKeyIdByte0:
        sig_name = "KeyFindRespToServiceKeyIdByte0"
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

    class KeyFindRespToServiceKeyIdByte15:
        sig_name = "KeyFindRespToServiceKeyIdByte15"
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

    class KeyFindRespToVMMKeyIdByte6:
        sig_name = "KeyFindRespToVMMKeyIdByte6"
        sig_start_bit = 391
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
        startbit = 391
        byte = 48
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class KeyFindRespToVMM_UB:
        sig_name = "KeyFindRespToVMM_UB"
        sig_start_bit = 480
        update_id_bit = 480
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
        startbit = 480
        byte = 60
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class KeyFindRespToServiceKeyIdByte1:
        sig_name = "KeyFindRespToServiceKeyIdByte1"
        sig_start_bit = 263
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
        startbit = 263
        byte = 32
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class KeyFindRespToLockg_UB:
        sig_name = "KeyFindRespToLockg_UB"
        sig_start_bit = 482
        update_id_bit = 482
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
        startbit = 482
        byte = 60
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class BrightnessLvlSet:
        sig_name = "BrightnessLvlSet"
        sig_start_bit = 439
        update_id_bit = 283
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "SCALE_LINEAR_AND_TEXTTABLE"
        sig_value_table = {'BattSOH_Invalid': 255}
        compute_method = None
        length = 8
        startbit = 439
        byte = 54
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class KeyFindRespToServiceKeyIdByte5:
        sig_name = "KeyFindRespToServiceKeyIdByte5"
        sig_start_bit = 199
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
        startbit = 199
        byte = 24
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class KeyFindRespToLockgKeyIdByte8:
        sig_name = "KeyFindRespToLockgKeyIdByte8"
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

    class ChargeLidAntiPnchSts_UB:
        sig_name = "ChargeLidAntiPnchSts_UB"
        sig_start_bit = 282
        update_id_bit = 282
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
        startbit = 282
        byte = 35
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class KeyFindRespToLockgKeyLocnSts:
        sig_name = "KeyFindRespToLockgKeyLocnSts"
        sig_start_bit = 87
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeyLocnReq_Idle': 0, 'KeyLocnReq_PEAllExtAndInt': 1, 'KeyLocnReq_PEAllExt': 2, 'KeyLocnReq_PEDrvrExt': 3, 'KeyLocnReq_PEPassExt': 4, 'KeyLocnReq_PEFrntExt': 5, 'KeyLocnReq_PERearExt': 6, 'KeyLocnReq_PEAllInt': 7, 'KeyLocnReq_PSAllInt': 8, 'KeyLocnReq_Reserved1': 9, 'KeyLocnReq_Reserved2': 10}
        compute_method = None
        length = 4
        startbit = 87
        byte = 10
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class KeyFindRespToLockgKeyIdByte14:
        sig_name = "KeyFindRespToLockgKeyIdByte14"
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

    class KeyFindRespToVMMKeyIdByte14:
        sig_name = "KeyFindRespToVMMKeyIdByte14"
        sig_start_bit = 335
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
        startbit = 335
        byte = 41
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class KeyFindRespToServiceKeyLocnSts:
        sig_name = "KeyFindRespToServiceKeyLocnSts"
        sig_start_bit = 287
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeyLocnReq_Idle': 0, 'KeyLocnReq_PEAllExtAndInt': 1, 'KeyLocnReq_PEAllExt': 2, 'KeyLocnReq_PEDrvrExt': 3, 'KeyLocnReq_PEPassExt': 4, 'KeyLocnReq_PEFrntExt': 5, 'KeyLocnReq_PERearExt': 6, 'KeyLocnReq_PEAllInt': 7, 'KeyLocnReq_PSAllInt': 8, 'KeyLocnReq_Reserved1': 9, 'KeyLocnReq_Reserved2': 10}
        compute_method = None
        length = 4
        startbit = 287
        byte = 35
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class FRDoorAntiPnchFb_UB:
        sig_name = "FRDoorAntiPnchFb_UB"
        sig_start_bit = 486
        update_id_bit = 486
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
        startbit = 486
        byte = 60
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class KeyFindRespToVMMKeyIdByte8:
        sig_name = "KeyFindRespToVMMKeyIdByte8"
        sig_start_bit = 359
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
        startbit = 359
        byte = 44
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class KeyFindRespToVMMKeyIdByte15:
        sig_name = "KeyFindRespToVMMKeyIdByte15"
        sig_start_bit = 423
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
        startbit = 423
        byte = 52
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class KeyFindRespToServiceKeyIdByte8:
        sig_name = "KeyFindRespToServiceKeyIdByte8"
        sig_start_bit = 279
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
        startbit = 279
        byte = 34
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class KeyFindRespToServiceKeyIdByte3:
        sig_name = "KeyFindRespToServiceKeyIdByte3"
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

    class KeyFindRespToVMMKeyIdByte5:
        sig_name = "KeyFindRespToVMMKeyIdByte5"
        sig_start_bit = 351
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
        startbit = 351
        byte = 43
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class KeyFindRespToLockgKeyIdByte5:
        sig_name = "KeyFindRespToLockgKeyIdByte5"
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

    class KeyFindRespToServiceKeyIdByte11:
        sig_name = "KeyFindRespToServiceKeyIdByte11"
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

    class KeyFindRespToServiceKeyIdByte14:
        sig_name = "KeyFindRespToServiceKeyIdByte14"
        sig_start_bit = 223
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
        startbit = 223
        byte = 27
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class KeyFindRespToLockgKeyFindSts:
        sig_name = "KeyFindRespToLockgKeyFindSts"
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
        sig_value_table = {'KeyPrsntSts_Idle': 0, 'KeyPrsntSts_InProgs': 1, 'KeyPrsntSts_NotPrsnt': 2, 'KeyPrsntSts_Prsnt': 3}
        compute_method = None
        length = 2
        startbit = 151
        byte = 18
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class SeatOccpSts_UB:
        sig_name = "SeatOccpSts_UB"
        sig_start_bit = 499
        update_id_bit = 499
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
        startbit = 499
        byte = 62
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class KeyFindReq:
        sig_name = "KeyFindReq"
        sig_start_bit = 7
        update_id_bit = 483
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeyLocnReq_Idle': 0, 'KeyLocnReq_PEAllExtAndInt': 1, 'KeyLocnReq_PEAllExt': 2, 'KeyLocnReq_PEDrvrExt': 3, 'KeyLocnReq_PEPassExt': 4, 'KeyLocnReq_PEFrntExt': 5, 'KeyLocnReq_PERearExt': 6, 'KeyLocnReq_PEAllInt': 7, 'KeyLocnReq_PSAllInt': 8, 'KeyLocnReq_Reserved1': 9, 'KeyLocnReq_Reserved2': 10}
        compute_method = None
        length = 4
        startbit = 7
        byte = 0
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class FLDoorAntiPnchFbCloseAntiPnchSts:
        sig_name = "FLDoorAntiPnchFbCloseAntiPnchSts"
        sig_start_bit = 445
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
        startbit = 445
        byte = 55
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class KeyFindRespToLockgKeyIdByte9:
        sig_name = "KeyFindRespToLockgKeyIdByte9"
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

    class FRDoorPosnStsDoorAngPosn:
        sig_name = "FRDoorPosnStsDoorAngPosn"
        sig_start_bit = 479
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 127
        sig_byteorder = "Motorola"
        sig_value_init = 101
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 479
        byte = 59
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class KeyFindRespToVMMKeyTyp:
        sig_name = "KeyFindRespToVMMKeyTyp"
        sig_start_bit = 399
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 9
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeyTyp_NoKeyConnected': 0, 'KeyTyp_NFC_Card': 1, 'KeyTyp_BLE_UWB_KeyFob': 2, 'KeyTyp_Phone_NFC_Key': 3, 'KeyTyp_Phone_BLE_Key': 4, 'KeyTyp_Phone_UWB_Key': 5, 'KeyTyp_Reserved1': 6, 'KeyTyp_Reserved2': 7, 'KeyTyp_Reserved3': 8, 'KeyTyp_Reserved4': 9}
        compute_method = None
        length = 4
        startbit = 399
        byte = 49
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class KeyFindRespToVMMKeyIdByte3:
        sig_name = "KeyFindRespToVMMKeyIdByte3"
        sig_start_bit = 327
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
        startbit = 327
        byte = 40
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class KeyFindRespToServiceKeyTyp:
        sig_name = "KeyFindRespToServiceKeyTyp"
        sig_start_bit = 147
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 9
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeyTyp_NoKeyConnected': 0, 'KeyTyp_NFC_Card': 1, 'KeyTyp_BLE_UWB_KeyFob': 2, 'KeyTyp_Phone_NFC_Key': 3, 'KeyTyp_Phone_BLE_Key': 4, 'KeyTyp_Phone_UWB_Key': 5, 'KeyTyp_Reserved1': 6, 'KeyTyp_Reserved2': 7, 'KeyTyp_Reserved3': 8, 'KeyTyp_Reserved4': 9}
        compute_method = None
        length = 4
        startbit = 147
        byte = 18
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class SeatOccpStsThrdRowRiSeatSts:
        sig_name = "SeatOccpStsThrdRowRiSeatSts"
        sig_start_bit = 488
        update_id_bit = None
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
        startbit = 488
        byte = 61
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ChargeLidMoveSts:
        sig_name = "ChargeLidMoveSts"
        sig_start_bit = 427
        update_id_bit = 443
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ChargeLidMtnSts_IniVal': 0, 'ChargeLidMtnSts_Moving': 1, 'ChargeLidMtnSts_Close': 2, 'ChargeLidMtnSts_Open': 3, 'ChargeLidMtnSts_Unknow': 4}
        compute_method = None
        length = 3
        startbit = 427
        byte = 53
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class KeyFindRespToLockgKeyTyp:
        sig_name = "KeyFindRespToLockgKeyTyp"
        sig_start_bit = 83
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 9
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeyTyp_NoKeyConnected': 0, 'KeyTyp_NFC_Card': 1, 'KeyTyp_BLE_UWB_KeyFob': 2, 'KeyTyp_Phone_NFC_Key': 3, 'KeyTyp_Phone_BLE_Key': 4, 'KeyTyp_Phone_UWB_Key': 5, 'KeyTyp_Reserved1': 6, 'KeyTyp_Reserved2': 7, 'KeyTyp_Reserved3': 8, 'KeyTyp_Reserved4': 9}
        compute_method = None
        length = 4
        startbit = 83
        byte = 10
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class FLDoorAntiPnchFb_UB:
        sig_name = "FLDoorAntiPnchFb_UB"
        sig_start_bit = 456
        update_id_bit = 456
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
        startbit = 456
        byte = 57
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class KeyFindRespToVMMKeyFindSts:
        sig_name = "KeyFindRespToVMMKeyFindSts"
        sig_start_bit = 281
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeyPrsntSts_Idle': 0, 'KeyPrsntSts_InProgs': 1, 'KeyPrsntSts_NotPrsnt': 2, 'KeyPrsntSts_Prsnt': 3}
        compute_method = None
        length = 2
        startbit = 281
        byte = 35
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class KeyFindRespToLockgKeyIdByte4:
        sig_name = "KeyFindRespToLockgKeyIdByte4"
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

    class KeyFindRespToVMMKeyIdByte0:
        sig_name = "KeyFindRespToVMMKeyIdByte0"
        sig_start_bit = 295
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
        startbit = 295
        byte = 36
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class KeyFindRespToLockgKeyIdByte7:
        sig_name = "KeyFindRespToLockgKeyIdByte7"
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

    class FLDoorPosnStsDoorAngPosn:
        sig_name = "FLDoorPosnStsDoorAngPosn"
        sig_start_bit = 463
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 127
        sig_byteorder = "Motorola"
        sig_value_init = 101
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 463
        byte = 57
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class WirelschrgActvReqFromHmiPass:
        sig_name = "WirelschrgActvReqFromHmiPass"
        sig_start_bit = 501
        update_id_bit = 497
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
        startbit = 501
        byte = 62
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class KeyFindRespToServiceKeyIdByte7:
        sig_name = "KeyFindRespToServiceKeyIdByte7"
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

    class FLDoorMtnSts:
        sig_name = "FLDoorMtnSts"
        sig_start_bit = 3
        update_id_bit = 472
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 9
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorMtnSts_IniVal': 0, 'DoorMtnSts_FullOpen': 1, 'DoorMtnSts_FullClose': 2, 'DoorMtnSts_StopDurOpen': 3, 'DoorMtnSts_StopDurClose': 4, 'DoorMtnSts_MovingOut': 5, 'DoorMtnSts_MovingIn': 6, 'DoorMtnSts_HalfClose': 7, 'DoorMtnSts_Unknow': 8, 'DoorMtnSts_OnlyOpenPosn': 9}
        compute_method = None
        length = 4
        startbit = 3
        byte = 0
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class SeatOccpStsSecRowRiSeatSts:
        sig_name = "SeatOccpStsSecRowRiSeatSts"
        sig_start_bit = 491
        update_id_bit = None
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
        startbit = 491
        byte = 61
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class KeyFindRespToServiceKeyIdByte10:
        sig_name = "KeyFindRespToServiceKeyIdByte10"
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

    class KeyFindRespToLockgKeyIdByte13:
        sig_name = "KeyFindRespToLockgKeyIdByte13"
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

    class DKSrvSts:
        sig_name = "DKSrvSts"
        sig_start_bit = 424
        update_id_bit = 442
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
        startbit = 424
        byte = 53
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class SeatOccpStsThrdRowLeSeatSts:
        sig_name = "SeatOccpStsThrdRowLeSeatSts"
        sig_start_bit = 490
        update_id_bit = None
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
        startbit = 490
        byte = 61
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class SeatOccpStsThrdRowMidSeatSts:
        sig_name = "SeatOccpStsThrdRowMidSeatSts"
        sig_start_bit = 489
        update_id_bit = None
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
        startbit = 489
        byte = 61
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class KeyFindRespToVMMKeyIdByte11:
        sig_name = "KeyFindRespToVMMKeyIdByte11"
        sig_start_bit = 415
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
        startbit = 415
        byte = 51
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class KeyFindRespToServiceKeyIdByte9:
        sig_name = "KeyFindRespToServiceKeyIdByte9"
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

    class WirelschrgActvReqFromHmi:
        sig_name = "WirelschrgActvReqFromHmi"
        sig_start_bit = 503
        update_id_bit = 498
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
        startbit = 503
        byte = 62
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class FLDoorPosnStsDoorPercPosn:
        sig_name = "FLDoorPosnStsDoorPercPosn"
        sig_start_bit = 455
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 101
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 455
        byte = 56
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class KeyFindRespToVMMKeyIdByte4:
        sig_name = "KeyFindRespToVMMKeyIdByte4"
        sig_start_bit = 407
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
        startbit = 407
        byte = 50
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ChargeLidAntiPnchStsOPenAntiPnchSts:
        sig_name = "ChargeLidAntiPnchStsOPenAntiPnchSts"
        sig_start_bit = 446
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
        startbit = 446
        byte = 55
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class KeyFindRespToLockgKeyIdByte11:
        sig_name = "KeyFindRespToLockgKeyIdByte11"
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

    class FRDoorAntiPnchFbOPenAntiPnchSts:
        sig_name = "FRDoorAntiPnchFbOPenAntiPnchSts"
        sig_start_bit = 440
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
        startbit = 440
        byte = 55
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class KeyFindRespToVMMKeyIdByte10:
        sig_name = "KeyFindRespToVMMKeyIdByte10"
        sig_start_bit = 367
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
        startbit = 367
        byte = 45
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FLDoorPosnSts_UB:
        sig_name = "FLDoorPosnSts_UB"
        sig_start_bit = 487
        update_id_bit = 487
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
        startbit = 487
        byte = 60
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class KeyFindRespToLockgKeyIdByte12:
        sig_name = "KeyFindRespToLockgKeyIdByte12"
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

    class FLDoorAntiPnchFbOPenAntiPnchSts:
        sig_name = "FLDoorAntiPnchFbOPenAntiPnchSts"
        sig_start_bit = 444
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
        startbit = 444
        byte = 55
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class KeyFindRespToVMMKeyLocnSts:
        sig_name = "KeyFindRespToVMMKeyLocnSts"
        sig_start_bit = 395
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeyLocnReq_Idle': 0, 'KeyLocnReq_PEAllExtAndInt': 1, 'KeyLocnReq_PEAllExt': 2, 'KeyLocnReq_PEDrvrExt': 3, 'KeyLocnReq_PEPassExt': 4, 'KeyLocnReq_PEFrntExt': 5, 'KeyLocnReq_PERearExt': 6, 'KeyLocnReq_PEAllInt': 7, 'KeyLocnReq_PSAllInt': 8, 'KeyLocnReq_Reserved1': 9, 'KeyLocnReq_Reserved2': 10}
        compute_method = None
        length = 4
        startbit = 395
        byte = 49
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class FRDoorPosnStsDoorPercPosn:
        sig_name = "FRDoorPosnStsDoorPercPosn"
        sig_start_bit = 471
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 101
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 471
        byte = 58
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SeatOccpStsPassSeatSts:
        sig_name = "SeatOccpStsPassSeatSts"
        sig_start_bit = 494
        update_id_bit = None
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
        startbit = 494
        byte = 61
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class KeyFindRespToVMMKeyIdByte7:
        sig_name = "KeyFindRespToVMMKeyIdByte7"
        sig_start_bit = 343
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
        startbit = 343
        byte = 42
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SeatOccpStsDrvrSeatSts:
        sig_name = "SeatOccpStsDrvrSeatSts"
        sig_start_bit = 495
        update_id_bit = None
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
        startbit = 495
        byte = 61
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ChargeLidAntiPnchStsCloseAntiPnchSts:
        sig_name = "ChargeLidAntiPnchStsCloseAntiPnchSts"
        sig_start_bit = 447
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
        startbit = 447
        byte = 55
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class KeyFindRespToLockgKeyIdByte10:
        sig_name = "KeyFindRespToLockgKeyIdByte10"
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

    class KeyFindRespToLockgKeyIdByte1:
        sig_name = "KeyFindRespToLockgKeyIdByte1"
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


class BNCMInfoCANFDFr06:
    msg_name = "BNCMInfoCANFDFr06"
    msg_id = 525
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 64
    tx_node = "BNCM"
    rx_nodes = ['ETC']
    sig_group_dict = {'DigKeyLocData1': ['DigKeyLocData1CalibrationDataByte0', 'DigKeyLocData1CalibrationDataByte1', 'DigKeyLocData1CalibrationDataByte10', 'DigKeyLocData1CalibrationDataByte11', 'DigKeyLocData1CalibrationDataByte12', 'DigKeyLocData1CalibrationDataByte13', 'DigKeyLocData1CalibrationDataByte14', 'DigKeyLocData1CalibrationDataByte15', 'DigKeyLocData1CalibrationDataByte16', 'DigKeyLocData1CalibrationDataByte17', 'DigKeyLocData1CalibrationDataByte18', 'DigKeyLocData1CalibrationDataByte19', 'DigKeyLocData1CalibrationDataByte2', 'DigKeyLocData1CalibrationDataByte3', 'DigKeyLocData1CalibrationDataByte4', 'DigKeyLocData1CalibrationDataByte5', 'DigKeyLocData1CalibrationDataByte6', 'DigKeyLocData1CalibrationDataByte7', 'DigKeyLocData1CalibrationDataByte8', 'DigKeyLocData1CalibrationDataByte9', 'DigKeyLocData1FrntLeBLERSSI', 'DigKeyLocData1FrntLeUWBDistance', 'DigKeyLocData1FrntRiBLERSSI', 'DigKeyLocData1FrntRiUWBDistance', 'DigKeyLocData1InVehReBLERSSI', 'DigKeyLocData1InVehReUWBDistance', 'DigKeyLocData1KeyIdByte0', 'DigKeyLocData1KeyIdByte1', 'DigKeyLocData1KeyIdByte10', 'DigKeyLocData1KeyIdByte11', 'DigKeyLocData1KeyIdByte12', 'DigKeyLocData1KeyIdByte13', 'DigKeyLocData1KeyIdByte14', 'DigKeyLocData1KeyIdByte15', 'DigKeyLocData1KeyIdByte2', 'DigKeyLocData1KeyIdByte3', 'DigKeyLocData1KeyIdByte4', 'DigKeyLocData1KeyIdByte5', 'DigKeyLocData1KeyIdByte6', 'DigKeyLocData1KeyIdByte7', 'DigKeyLocData1KeyIdByte8', 'DigKeyLocData1KeyIdByte9', 'DigKeyLocData1MainBLERSSI', 'DigKeyLocData1MainUWBDistance', 'DigKeyLocData1ReLeBLERSSI', 'DigKeyLocData1ReLeUWBDistance', 'DigKeyLocData1ReRiBLERSSI', 'DigKeyLocData1ReRiUWBDistance']}
    sig_group_dataid_dict = {}

    class DigKeyLocData1CalibrationDataByte8:
        sig_name = "DigKeyLocData1CalibrationDataByte8"
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

    class DigKeyLocData1KeyIdByte7:
        sig_name = "DigKeyLocData1KeyIdByte7"
        sig_start_bit = 367
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
        startbit = 367
        byte = 45
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData1KeyIdByte1:
        sig_name = "DigKeyLocData1KeyIdByte1"
        sig_start_bit = 319
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
        startbit = 319
        byte = 39
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData1CalibrationDataByte11:
        sig_name = "DigKeyLocData1CalibrationDataByte11"
        sig_start_bit = 239
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
        startbit = 239
        byte = 29
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData1ReLeUWBDistance:
        sig_name = "DigKeyLocData1ReLeUWBDistance"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 65535
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class DigKeyLocData1CalibrationDataByte1:
        sig_name = "DigKeyLocData1CalibrationDataByte1"
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

    class DigKeyLocData1FrntLeBLERSSI:
        sig_name = "DigKeyLocData1FrntLeBLERSSI"
        sig_start_bit = 79
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
        startbit = 79
        byte = 9
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData1CalibrationDataByte5:
        sig_name = "DigKeyLocData1CalibrationDataByte5"
        sig_start_bit = 191
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
        startbit = 191
        byte = 23
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData1KeyIdByte13:
        sig_name = "DigKeyLocData1KeyIdByte13"
        sig_start_bit = 415
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
        startbit = 415
        byte = 51
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData1MainBLERSSI:
        sig_name = "DigKeyLocData1MainBLERSSI"
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

    class DigKeyLocData1ReRiUWBDistance:
        sig_name = "DigKeyLocData1ReRiUWBDistance"
        sig_start_bit = 63
        update_id_bit = None
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 65535
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 63
        bmuws_info = [(7, 0b11111111, 0b00000000, 8, 0), (8, 0b11111111, 0b00000000, 8, 0)]

    class DigKeyLocData1ReLeBLERSSI:
        sig_name = "DigKeyLocData1ReLeBLERSSI"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData1KeyIdByte2:
        sig_name = "DigKeyLocData1KeyIdByte2"
        sig_start_bit = 327
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
        startbit = 327
        byte = 40
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData1CalibrationDataByte0:
        sig_name = "DigKeyLocData1CalibrationDataByte0"
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

    class DigKeyLocData1CalibrationDataByte16:
        sig_name = "DigKeyLocData1CalibrationDataByte16"
        sig_start_bit = 279
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
        startbit = 279
        byte = 34
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData1CalibrationDataByte19:
        sig_name = "DigKeyLocData1CalibrationDataByte19"
        sig_start_bit = 303
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
        startbit = 303
        byte = 37
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData1CalibrationDataByte7:
        sig_name = "DigKeyLocData1CalibrationDataByte7"
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

    class DigKeyLocData1KeyIdByte12:
        sig_name = "DigKeyLocData1KeyIdByte12"
        sig_start_bit = 407
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
        startbit = 407
        byte = 50
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData1CalibrationDataByte17:
        sig_name = "DigKeyLocData1CalibrationDataByte17"
        sig_start_bit = 287
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
        startbit = 287
        byte = 35
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData1KeyIdByte4:
        sig_name = "DigKeyLocData1KeyIdByte4"
        sig_start_bit = 343
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
        startbit = 343
        byte = 42
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData1KeyIdByte14:
        sig_name = "DigKeyLocData1KeyIdByte14"
        sig_start_bit = 423
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
        startbit = 423
        byte = 52
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData1KeyIdByte0:
        sig_name = "DigKeyLocData1KeyIdByte0"
        sig_start_bit = 311
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
        startbit = 311
        byte = 38
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData1FrntRiBLERSSI:
        sig_name = "DigKeyLocData1FrntRiBLERSSI"
        sig_start_bit = 103
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
        startbit = 103
        byte = 12
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData1CalibrationDataByte9:
        sig_name = "DigKeyLocData1CalibrationDataByte9"
        sig_start_bit = 223
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
        startbit = 223
        byte = 27
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData1CalibrationDataByte4:
        sig_name = "DigKeyLocData1CalibrationDataByte4"
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

    class DigKeyLocData1FrntLeUWBDistance:
        sig_name = "DigKeyLocData1FrntLeUWBDistance"
        sig_start_bit = 87
        update_id_bit = None
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 65535
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 87
        bmuws_info = [(10, 0b11111111, 0b00000000, 8, 0), (11, 0b11111111, 0b00000000, 8, 0)]

    class DigKeyLocData1CalibrationDataByte14:
        sig_name = "DigKeyLocData1CalibrationDataByte14"
        sig_start_bit = 263
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
        startbit = 263
        byte = 32
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData1MainUWBDistance:
        sig_name = "DigKeyLocData1MainUWBDistance"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 65535
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 15
        bmuws_info = [(1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DigKeyLocData1CalibrationDataByte3:
        sig_name = "DigKeyLocData1CalibrationDataByte3"
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

    class DigKeyLocData1CalibrationDataByte18:
        sig_name = "DigKeyLocData1CalibrationDataByte18"
        sig_start_bit = 295
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
        startbit = 295
        byte = 36
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData1FrntRiUWBDistance:
        sig_name = "DigKeyLocData1FrntRiUWBDistance"
        sig_start_bit = 111
        update_id_bit = None
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 65535
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 111
        bmuws_info = [(13, 0b11111111, 0b00000000, 8, 0), (14, 0b11111111, 0b00000000, 8, 0)]

    class DigKeyLocData1KeyIdByte9:
        sig_name = "DigKeyLocData1KeyIdByte9"
        sig_start_bit = 383
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
        startbit = 383
        byte = 47
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData1CalibrationDataByte12:
        sig_name = "DigKeyLocData1CalibrationDataByte12"
        sig_start_bit = 247
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
        startbit = 247
        byte = 30
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData1CalibrationDataByte2:
        sig_name = "DigKeyLocData1CalibrationDataByte2"
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

    class DigKeyLocData1CalibrationDataByte13:
        sig_name = "DigKeyLocData1CalibrationDataByte13"
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

    class DigKeyLocData1CalibrationDataByte6:
        sig_name = "DigKeyLocData1CalibrationDataByte6"
        sig_start_bit = 199
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
        startbit = 199
        byte = 24
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData1ReRiBLERSSI:
        sig_name = "DigKeyLocData1ReRiBLERSSI"
        sig_start_bit = 55
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
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData1KeyIdByte11:
        sig_name = "DigKeyLocData1KeyIdByte11"
        sig_start_bit = 399
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
        startbit = 399
        byte = 49
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData1KeyIdByte5:
        sig_name = "DigKeyLocData1KeyIdByte5"
        sig_start_bit = 351
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
        startbit = 351
        byte = 43
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData1CalibrationDataByte15:
        sig_name = "DigKeyLocData1CalibrationDataByte15"
        sig_start_bit = 271
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
        startbit = 271
        byte = 33
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData1KeyIdByte10:
        sig_name = "DigKeyLocData1KeyIdByte10"
        sig_start_bit = 391
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
        startbit = 391
        byte = 48
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData1CalibrationDataByte10:
        sig_name = "DigKeyLocData1CalibrationDataByte10"
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

    class DigKeyLocData1KeyIdByte6:
        sig_name = "DigKeyLocData1KeyIdByte6"
        sig_start_bit = 359
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
        startbit = 359
        byte = 44
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData1KeyIdByte3:
        sig_name = "DigKeyLocData1KeyIdByte3"
        sig_start_bit = 335
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
        startbit = 335
        byte = 41
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData1KeyIdByte8:
        sig_name = "DigKeyLocData1KeyIdByte8"
        sig_start_bit = 375
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
        startbit = 375
        byte = 46
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData1InVehReBLERSSI:
        sig_name = "DigKeyLocData1InVehReBLERSSI"
        sig_start_bit = 127
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
        startbit = 127
        byte = 15
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData1KeyIdByte15:
        sig_name = "DigKeyLocData1KeyIdByte15"
        sig_start_bit = 431
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
        startbit = 431
        byte = 53
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData1InVehReUWBDistance:
        sig_name = "DigKeyLocData1InVehReUWBDistance"
        sig_start_bit = 135
        update_id_bit = None
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 65535
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 135
        bmuws_info = [(16, 0b11111111, 0b00000000, 8, 0), (17, 0b11111111, 0b00000000, 8, 0)]


class WPC2InfoCANFDFr01:
    msg_name = "WPC2InfoCANFDFr01"
    msg_id = 663
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 16
    tx_node = "WPC2"
    rx_nodes = ['BNCM', 'CCUMCUCD', 'ETC']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class NFCKeyInvldSts:
        sig_name = "NFCKeyInvldSts"
        sig_start_bit = 7
        update_id_bit = 21
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
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class WirelsChrgnSetFb:
        sig_name = "WirelsChrgnSetFb"
        sig_start_bit = 23
        update_id_bit = 47
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
        startbit = 23
        byte = 2
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class WirelsChrgnPanT:
        sig_name = "WirelsChrgnPanT"
        sig_start_bit = 20
        update_id_bit = 22
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = -256.0
        sig_value_min = 0
        sig_value_max = 5119
        sig_byteorder = "Motorola"
        sig_value_init = 2560
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 20
        bmuws_info = [(2, 0b00011111, 0b11100000, 5, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class WirelessChrgnFltTSts:
        sig_name = "WirelessChrgnFltTSts"
        sig_start_bit = 15
        update_id_bit = 35
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVFaultSts_Idle': 0, 'LVFaultSts_Fault': 1, 'LVFaultSts_NoFault': 2, 'LVFaultSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 15
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class WirelsChrgnModSts:
        sig_name = "WirelsChrgnModSts"
        sig_start_bit = 10
        update_id_bit = 32
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WirelsChrgnModSts_Standby': 0, 'WirelsChrgnModSts_Charging': 1, 'WirelsChrgnModSts_QFOD': 2, 'WirelsChrgnModSts_PFOD': 3, 'WirelsChrgnModSts_CardProt': 4, 'WirelsChrgnModSts_PhoneForgotten': 5, 'WirelsChrgnModSts_Reserved1': 6, 'WirelsChrgnModSts_Reserved2': 7}
        compute_method = None
        length = 3
        startbit = 10
        byte = 1
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class WirelessChrgnFltHwSts:
        sig_name = "WirelessChrgnFltHwSts"
        sig_start_bit = 3
        update_id_bit = 37
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVFaultSts_Idle': 0, 'LVFaultSts_Fault': 1, 'LVFaultSts_NoFault': 2, 'LVFaultSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 3
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class WirelessChrgnFltUSts:
        sig_name = "WirelessChrgnFltUSts"
        sig_start_bit = 13
        update_id_bit = 34
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVFaultSts_Idle': 0, 'LVFaultSts_Fault': 1, 'LVFaultSts_NoFault': 2, 'LVFaultSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 13
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class WirelessChrgnFltPwrSts:
        sig_name = "WirelessChrgnFltPwrSts"
        sig_start_bit = 1
        update_id_bit = 36
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVFaultSts_Idle': 0, 'LVFaultSts_Fault': 1, 'LVFaultSts_NoFault': 2, 'LVFaultSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class NFCOpenSts:
        sig_name = "NFCOpenSts"
        sig_start_bit = 6
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
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class WirelsChrgnCoolgFanSts:
        sig_name = "WirelsChrgnCoolgFanSts"
        sig_start_bit = 11
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
        startbit = 11
        byte = 1
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class PhoneDetn:
        sig_name = "PhoneDetn"
        sig_start_bit = 5
        update_id_bit = 38
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PhoneDetn_Idle': 0, 'PhoneDetn_Yes': 1, 'PhoneDetn_No': 2, 'PhoneDetn_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4


class CCUMCUCDtoBNCMInfoCANFDFCFrame:
    msg_name = "CCUMCUCDtoBNCMInfoCANFDFCFrame"
    msg_id = 785
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "CCUMCUCD"
    rx_nodes = ['BNCM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class CCUMCUCDInfoCANFDFr07:
    msg_name = "CCUMCUCDInfoCANFDFr07"
    msg_id = 779
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.2
    msg_length = 64
    tx_node = "CCUMCUCD"
    rx_nodes = ['ETC', 'CD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class DKComErrCod:
        sig_name = "DKComErrCod"
        sig_start_bit = 2
        update_id_bit = 23
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DigKeyComErrCode_NoErr': 0, 'DigKeyComErrCode_AntiReplayErr': 1, 'DigKeyComErrCode_MACErr': 2, 'DigKeyComErrCode_UndefinedCmd': 3, 'DigKeyComErrCode_DataLengthErr': 4, 'DigKeyComErrCode_Reserved1': 5, 'DigKeyComErrCode_Reserved2': 6, 'DigKeyComErrCode_Reserved3': 7}
        compute_method = None
        length = 3
        startbit = 2
        byte = 0
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class CDSOCKeepPwrReq:
        sig_name = "CDSOCKeepPwrReq"
        sig_start_bit = 39
        update_id_bit = 21
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
        startbit = 39
        byte = 4
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class CDCoolgReq:
        sig_name = "CDCoolgReq"
        sig_start_bit = 15
        update_id_bit = 9
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
        startbit = 15
        byte = 1
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class DisplayTheme:
        sig_name = "DisplayTheme"
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
        sig_value_table = {'DisplayTheme_Unknow': 0, 'DisplayTheme1': 1, 'DisplayTheme2': 2, 'DisplayTheme3': 3}
        compute_method = None
        length = 2
        startbit = 13
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class CDSOCShutDwnSts:
        sig_name = "CDSOCShutDwnSts"
        sig_start_bit = 37
        update_id_bit = 19
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 6
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SOCShutDownSts_Idle': 0, 'SOCShutDownSts_STRAck': 1, 'SOCShutDownSts_STRFailed': 2, 'SOCShutDownSts_STRDone': 3, 'SOCShutDownSts_OFFAck': 4, 'SOCShutDownSts_OFFAllowed': 5, 'SOCShutDownSts_ToStart': 6}
        compute_method = None
        length = 3
        startbit = 37
        byte = 4
        mask = 0b00111000
        unmask = 0b11000111
        shift = 3

    class CDSOCRstReq:
        sig_name = "CDSOCRstReq"
        sig_start_bit = 38
        update_id_bit = 20
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
        startbit = 38
        byte = 4
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class CDSOCHeartBeatSig:
        sig_name = "CDSOCHeartBeatSig"
        sig_start_bit = 31
        update_id_bit = 22
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

    class BLEChrgLidCtrlErrCod:
        sig_name = "BLEChrgLidCtrlErrCod"
        sig_start_bit = 7
        update_id_bit = 11
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BLEChrgLidCtrlErrCod_Idle': 0, 'BLEChrgLidCtrlErrCod_LockStsErr': 1, 'BLEChrgLidCtrlErrCod_SeatStsErr': 2, 'BLEChrgLidCtrlErrCod_KeyPrsntStsErr': 3, 'BLEChrgLidCtrlErrCod_UsgModeErr': 4, 'BLEChrgLidCtrlErrCod_CarModeErr': 5, 'BLEChrgLidCtrlErrCod_Reserved1': 6, 'BLEChrgLidCtrlErrCod_Reserved2': 7}
        compute_method = None
        length = 3
        startbit = 7
        byte = 0
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class CDSOCStrtSts:
        sig_name = "CDSOCStrtSts"
        sig_start_bit = 34
        update_id_bit = 18
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SOCStrtSts_Idle': 0, 'SOCStrtSts_ColdStartInit': 1, 'SOCStrtSts_ColdStartComplete': 2, 'SOCStrtSts_WarmStartInit': 3, 'SOCStrtSts_WarmStartComplete': 4, 'SOCStrtSts_Failed': 5}
        compute_method = None
        length = 3
        startbit = 34
        byte = 4
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0


class BNCMtoCCUMCUCDDigKeyBLEReqInfoCANFDFrame:
    msg_name = "BNCMtoCCUMCUCDDigKeyBLEReqInfoCANFDFrame"
    msg_id = 768
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "BNCM"
    rx_nodes = ['CCUMCUCD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class CCUMCUCDtoBNCMDigKeyRKERespInfoCANFDFrame:
    msg_name = "CCUMCUCDtoBNCMDigKeyRKERespInfoCANFDFrame"
    msg_id = 771
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "CCUMCUCD"
    rx_nodes = ['BNCM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class NKRToCCUMCUCDInfoCANFDDiagRespFrame:
    msg_name = "NKRToCCUMCUCDInfoCANFDDiagRespFrame"
    msg_id = 1573
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "NKR"
    rx_nodes = ['CCUMCUCD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class TPMInfoCANFDNmFr:
    msg_name = "TPMInfoCANFDNmFr"
    msg_id = 1285
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "TPM"
    rx_nodes = ['NKR']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class BNCMtoCCUMCUCDDigKeyLogInfoInfoCANFDFrame:
    msg_name = "BNCMtoCCUMCUCDDigKeyLogInfoInfoCANFDFrame"
    msg_id = 784
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "BNCM"
    rx_nodes = ['CCUMCUCD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class BNCMtoCCUMCUCDDigKeyRemRespInfoCANFDFrame:
    msg_name = "BNCMtoCCUMCUCDDigKeyRemRespInfoCANFDFrame"
    msg_id = 773
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "BNCM"
    rx_nodes = ['CCUMCUCD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class WPC3InfoCANFDFr01:
    msg_name = "WPC3InfoCANFDFr01"
    msg_id = 664
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 16
    tx_node = "WPC3"
    rx_nodes = ['CCUMCUCD', 'ETC']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class WirelsChrgnPanTPass:
        sig_name = "WirelsChrgnPanTPass"
        sig_start_bit = 31
        update_id_bit = 16
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = -256.0
        sig_value_min = 0
        sig_value_max = 5119
        sig_byteorder = "Motorola"
        sig_value_init = 2560
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111000, 0b00000111, 5, 3)]

    class WirelessChrgnFltUStsPass:
        sig_name = "WirelessChrgnFltUStsPass"
        sig_start_bit = 15
        update_id_bit = 20
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVFaultSts_Idle': 0, 'LVFaultSts_Fault': 1, 'LVFaultSts_NoFault': 2, 'LVFaultSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 15
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class WirelsChrgnModStsPass:
        sig_name = "WirelsChrgnModStsPass"
        sig_start_bit = 12
        update_id_bit = 18
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WirelsChrgnModSts_Standby': 0, 'WirelsChrgnModSts_Charging': 1, 'WirelsChrgnModSts_QFOD': 2, 'WirelsChrgnModSts_PFOD': 3, 'WirelsChrgnModSts_CardProt': 4, 'WirelsChrgnModSts_PhoneForgotten': 5, 'WirelsChrgnModSts_Reserved1': 6, 'WirelsChrgnModSts_Reserved2': 7}
        compute_method = None
        length = 3
        startbit = 12
        byte = 1
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class WirelsChrgnCoolgFanStsPass:
        sig_name = "WirelsChrgnCoolgFanStsPass"
        sig_start_bit = 13
        update_id_bit = 19
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
        startbit = 13
        byte = 1
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class WirelessChrgnFltPwrStsPass:
        sig_name = "WirelessChrgnFltPwrStsPass"
        sig_start_bit = 3
        update_id_bit = 22
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVFaultSts_Idle': 0, 'LVFaultSts_Fault': 1, 'LVFaultSts_NoFault': 2, 'LVFaultSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 3
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class WirelessChrgnFltTStsPass:
        sig_name = "WirelessChrgnFltTStsPass"
        sig_start_bit = 1
        update_id_bit = 21
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVFaultSts_Idle': 0, 'LVFaultSts_Fault': 1, 'LVFaultSts_NoFault': 2, 'LVFaultSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class PhoneDetnPass:
        sig_name = "PhoneDetnPass"
        sig_start_bit = 7
        update_id_bit = 8
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PhoneDetn_Idle': 0, 'PhoneDetn_Yes': 1, 'PhoneDetn_No': 2, 'PhoneDetn_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class WirelessChrgnFltHwStsPass:
        sig_name = "WirelessChrgnFltHwStsPass"
        sig_start_bit = 5
        update_id_bit = 23
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVFaultSts_Idle': 0, 'LVFaultSts_Fault': 1, 'LVFaultSts_NoFault': 2, 'LVFaultSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class WirelsChrgnSetFbPass:
        sig_name = "WirelsChrgnSetFbPass"
        sig_start_bit = 9
        update_id_bit = 17
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


class CCUMCUCDInfoCANFDFr03:
    msg_name = "CCUMCUCDInfoCANFDFr03"
    msg_id = 401
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 64
    tx_node = "CCUMCUCD"
    rx_nodes = ['BNCM', 'ETC']
    sig_group_dict = {'NFCLockUnlockReq': ['NFCLockUnlockReqKeyIdByte0', 'NFCLockUnlockReqKeyIdByte1', 'NFCLockUnlockReqKeyIdByte10', 'NFCLockUnlockReqKeyIdByte11', 'NFCLockUnlockReqKeyIdByte12', 'NFCLockUnlockReqKeyIdByte13', 'NFCLockUnlockReqKeyIdByte14', 'NFCLockUnlockReqKeyIdByte15', 'NFCLockUnlockReqKeyIdByte2', 'NFCLockUnlockReqKeyIdByte3', 'NFCLockUnlockReqKeyIdByte4', 'NFCLockUnlockReqKeyIdByte5', 'NFCLockUnlockReqKeyIdByte6', 'NFCLockUnlockReqKeyIdByte7', 'NFCLockUnlockReqKeyIdByte8', 'NFCLockUnlockReqKeyIdByte9', 'NFCLockUnlockReqKeyPrsntSts'], 'RLDoorPosnSts': ['RLDoorPosnStsDoorAngPosn', 'RLDoorPosnStsDoorPercPosn'], 'CentralLockSts': ['CentralLockStsCenLockSts', 'CentralLockStsTrigSrc', 'CentralLockStsTrigSrcType', 'CentralLockStsUpdateEvnt'], 'DKMgrFctRdySts': ['DKMgrFctRdyStsFctRdySts', 'DKMgrFctRdyStsRnd'], 'DigKeyApproachReq': ['DigKeyApproachReqDigKeyApproaReq', 'DigKeyApproachReqKeyIdByte0', 'DigKeyApproachReqKeyIdByte1', 'DigKeyApproachReqKeyIdByte10', 'DigKeyApproachReqKeyIdByte11', 'DigKeyApproachReqKeyIdByte12', 'DigKeyApproachReqKeyIdByte13', 'DigKeyApproachReqKeyIdByte14', 'DigKeyApproachReqKeyIdByte15', 'DigKeyApproachReqKeyIdByte2', 'DigKeyApproachReqKeyIdByte3', 'DigKeyApproachReqKeyIdByte4', 'DigKeyApproachReqKeyIdByte5', 'DigKeyApproachReqKeyIdByte6', 'DigKeyApproachReqKeyIdByte7', 'DigKeyApproachReqKeyIdByte8', 'DigKeyApproachReqKeyIdByte9', 'DigKeyApproachReqKeyTyp'], 'RLDoorAntiPnchFb': ['RLDoorAntiPnchFbCloseAntiPnchSts', 'RLDoorAntiPnchFbOPenAntiPnchSts'], 'DigKeyLiReq': ['DigKeyLiReqDigKeyApproachLightSts', 'DigKeyLiReqKeyIdByte0', 'DigKeyLiReqKeyIdByte1', 'DigKeyLiReqKeyIdByte10', 'DigKeyLiReqKeyIdByte11', 'DigKeyLiReqKeyIdByte12', 'DigKeyLiReqKeyIdByte13', 'DigKeyLiReqKeyIdByte14', 'DigKeyLiReqKeyIdByte15', 'DigKeyLiReqKeyIdByte2', 'DigKeyLiReqKeyIdByte3', 'DigKeyLiReqKeyIdByte4', 'DigKeyLiReqKeyIdByte5', 'DigKeyLiReqKeyIdByte6', 'DigKeyLiReqKeyIdByte7', 'DigKeyLiReqKeyIdByte8', 'DigKeyLiReqKeyIdByte9', 'DigKeyLiReqKeyTyp']}
    sig_group_dataid_dict = {}

    class NFCLockUnlockReqKeyIdByte2:
        sig_name = "NFCLockUnlockReqKeyIdByte2"
        sig_start_bit = 391
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
        startbit = 391
        byte = 48
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RLDoorPosnStsDoorPercPosn:
        sig_name = "RLDoorPosnStsDoorPercPosn"
        sig_start_bit = 495
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 101
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 495
        byte = 61
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class NFCLockUnlockReq_UB:
        sig_name = "NFCLockUnlockReq_UB"
        sig_start_bit = 464
        update_id_bit = 464
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
        startbit = 464
        byte = 58
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class RLChdLockSts:
        sig_name = "RLChdLockSts"
        sig_start_bit = 335
        update_id_bit = 479
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorLockSts_Unknow': 0, 'DoorLockSts_Lock': 1, 'DoorLockSts_Unlock': 2}
        compute_method = None
        length = 2
        startbit = 335
        byte = 41
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class DigKeyLiReqKeyTyp:
        sig_name = "DigKeyLiReqKeyTyp"
        sig_start_bit = 295
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 9
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeyTyp_NoKeyConnected': 0, 'KeyTyp_NFC_Card': 1, 'KeyTyp_BLE_UWB_KeyFob': 2, 'KeyTyp_Phone_NFC_Key': 3, 'KeyTyp_Phone_BLE_Key': 4, 'KeyTyp_Phone_UWB_Key': 5, 'KeyTyp_Reserved1': 6, 'KeyTyp_Reserved2': 7, 'KeyTyp_Reserved3': 8, 'KeyTyp_Reserved4': 9}
        compute_method = None
        length = 4
        startbit = 295
        byte = 36
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class AlrmStsDbg:
        sig_name = "AlrmStsDbg"
        sig_start_bit = 3
        update_id_bit = 289
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmStsDbg_Disarm': 0, 'AlrmStsDbg_PreArm': 1, 'AlrmStsDbg_CmplArmd': 2, 'AlrmStsDbg_NotCmplArmd': 3, 'AlrmStsDbg_Actv': 4, 'AlrmStsDbg_Reserved1': 5, 'AlrmStsDbg_Reserved2': 6, 'AlrmStsDbg_Reserved3': 7}
        compute_method = None
        length = 3
        startbit = 3
        byte = 0
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class DigKeyLiReqKeyIdByte5:
        sig_name = "DigKeyLiReqKeyIdByte5"
        sig_start_bit = 263
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
        startbit = 263
        byte = 32
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLiReqKeyIdByte7:
        sig_name = "DigKeyLiReqKeyIdByte7"
        sig_start_bit = 199
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
        startbit = 199
        byte = 24
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLiReqKeyIdByte6:
        sig_name = "DigKeyLiReqKeyIdByte6"
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

    class DigKeyLiReqKeyIdByte4:
        sig_name = "DigKeyLiReqKeyIdByte4"
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

    class DigKeyLiReqKeyIdByte11:
        sig_name = "DigKeyLiReqKeyIdByte11"
        sig_start_bit = 271
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
        startbit = 271
        byte = 33
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class NFCLockUnlockReqKeyIdByte10:
        sig_name = "NFCLockUnlockReqKeyIdByte10"
        sig_start_bit = 351
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
        startbit = 351
        byte = 43
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyApproachReqKeyIdByte12:
        sig_name = "DigKeyApproachReqKeyIdByte12"
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

    class NFCLockUnlockReqKeyIdByte5:
        sig_name = "NFCLockUnlockReqKeyIdByte5"
        sig_start_bit = 367
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
        startbit = 367
        byte = 45
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RLDoorPosnStsDoorAngPosn:
        sig_name = "RLDoorPosnStsDoorAngPosn"
        sig_start_bit = 487
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 127
        sig_byteorder = "Motorola"
        sig_value_init = 101
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 487
        byte = 60
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class NFCLockUnlockReqKeyIdByte11:
        sig_name = "NFCLockUnlockReqKeyIdByte11"
        sig_start_bit = 343
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
        startbit = 343
        byte = 42
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DKMgrFctRdyStsFctRdySts:
        sig_name = "DKMgrFctRdyStsFctRdySts"
        sig_start_bit = 288
        update_id_bit = None
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
        startbit = 288
        byte = 36
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class DigKeyApproachReqKeyIdByte8:
        sig_name = "DigKeyApproachReqKeyIdByte8"
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

    class DigKeyLiReqKeyIdByte9:
        sig_name = "DigKeyLiReqKeyIdByte9"
        sig_start_bit = 191
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
        startbit = 191
        byte = 23
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RLDoorPosnSts_UB:
        sig_name = "RLDoorPosnSts_UB"
        sig_start_bit = 476
        update_id_bit = 476
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
        startbit = 476
        byte = 59
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class DigKeyApproachReqKeyTyp:
        sig_name = "DigKeyApproachReqKeyTyp"
        sig_start_bit = 43
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 9
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeyTyp_NoKeyConnected': 0, 'KeyTyp_NFC_Card': 1, 'KeyTyp_BLE_UWB_KeyFob': 2, 'KeyTyp_Phone_NFC_Key': 3, 'KeyTyp_Phone_BLE_Key': 4, 'KeyTyp_Phone_UWB_Key': 5, 'KeyTyp_Reserved1': 6, 'KeyTyp_Reserved2': 7, 'KeyTyp_Reserved3': 8, 'KeyTyp_Reserved4': 9}
        compute_method = None
        length = 4
        startbit = 43
        byte = 5
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class NFCLockUnlockReqKeyIdByte8:
        sig_name = "NFCLockUnlockReqKeyIdByte8"
        sig_start_bit = 455
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
        startbit = 455
        byte = 56
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class NFCLockUnlockReqKeyIdByte0:
        sig_name = "NFCLockUnlockReqKeyIdByte0"
        sig_start_bit = 423
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
        startbit = 423
        byte = 52
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLiReqKeyIdByte14:
        sig_name = "DigKeyLiReqKeyIdByte14"
        sig_start_bit = 247
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
        startbit = 247
        byte = 30
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class NFCLockUnlockReqKeyIdByte14:
        sig_name = "NFCLockUnlockReqKeyIdByte14"
        sig_start_bit = 447
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
        startbit = 447
        byte = 55
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyApproachReqKeyIdByte11:
        sig_name = "DigKeyApproachReqKeyIdByte11"
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

    class DigKeyApproachReqKeyIdByte9:
        sig_name = "DigKeyApproachReqKeyIdByte9"
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

    class NFCLockUnlockReqKeyIdByte15:
        sig_name = "NFCLockUnlockReqKeyIdByte15"
        sig_start_bit = 359
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
        startbit = 359
        byte = 44
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DKMgrFctRdyStsRnd:
        sig_name = "DKMgrFctRdyStsRnd"
        sig_start_bit = 303
        update_id_bit = None
        sig_length = 32
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 32
        startbit = 303
        bmuws_info = [(37, 0b11111111, 0b00000000, 8, 0), (38, 0b11111111, 0b00000000, 8, 0), (39, 0b11111111, 0b00000000, 8, 0), (40, 0b11111111, 0b00000000, 8, 0)]

    class CentralLockSts_UB:
        sig_name = "CentralLockSts_UB"
        sig_start_bit = 468
        update_id_bit = 468
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
        startbit = 468
        byte = 58
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class NFCLockUnlockReqKeyIdByte9:
        sig_name = "NFCLockUnlockReqKeyIdByte9"
        sig_start_bit = 463
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
        startbit = 463
        byte = 57
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CentralLockStsCenLockSts:
        sig_name = "CentralLockStsCenLockSts"
        sig_start_bit = 10
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LockSts_IniVal': 0, 'LockSts_CenLocked': 1, 'LockSts_CenUnLcked': 2, 'LockSts_OnlyTrUnlcked': 3}
        compute_method = None
        length = 2
        startbit = 10
        byte = 1
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class DKMgrFctRdySts_UB:
        sig_name = "DKMgrFctRdySts_UB"
        sig_start_bit = 465
        update_id_bit = 465
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
        startbit = 465
        byte = 58
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class NFCLockUnlockReqKeyIdByte12:
        sig_name = "NFCLockUnlockReqKeyIdByte12"
        sig_start_bit = 399
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
        startbit = 399
        byte = 49
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CentralLockStsTrigSrc:
        sig_name = "CentralLockStsTrigSrc"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 20
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TrigSrc_IniVal': 0, 'TrigSrc_RKE_Outd': 1, 'TrigSrc_PE_APP': 2, 'TrigSrc_Approach_APP': 3, 'TrigSrc_PE_KeyFob': 4, 'TrigSrc_Approach_KeyFob': 5, 'TrigSrc_NFC': 6, 'TrigSrc_Telematic_Outd': 7, 'TrigSrc_Relock': 8, 'TrigSrc_OutdVoice': 9, 'TrigSrc_OutdLockCtrl': 10, 'TrigSrc_SpdLock': 11, 'TrigSrc_GearPUnlck': 12, 'TrigSrc_InsdSwtUnlck': 13, 'TrigSrc_InsdVoice': 14, 'TrigSrc_CrashUnlck': 15, 'TrigSrc_HMI': 16, 'TrigSrc_RKE_Insd': 17, 'TrigSrc_Telematic_Insd': 18, 'TrigSrc_ThermAwayUnlck': 19, 'TrigSrc_InsdLockCtrl': 20}
        compute_method = None
        length = 5
        startbit = 23
        byte = 2
        mask = 0b11111000
        unmask = 0b00000111
        shift = 3

    class DigKeyApproachReq_UB:
        sig_name = "DigKeyApproachReq_UB"
        sig_start_bit = 467
        update_id_bit = 467
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
        startbit = 467
        byte = 58
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class DigKeyLiReqKeyIdByte3:
        sig_name = "DigKeyLiReqKeyIdByte3"
        sig_start_bit = 223
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
        startbit = 223
        byte = 27
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class AlrmTrigSrc:
        sig_name = "AlrmTrigSrc"
        sig_start_bit = 0
        update_id_bit = 470
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmTrigSrc_NoTrigSrc': 0, 'AlrmTrigSrc_DoorDrvr': 1, 'AlrmTrigSrc_DoorPass': 2, 'AlrmTrigSrc_DoorReLe': 3, 'AlrmTrigSrc_DoorReRi': 4, 'AlrmTrigSrc_Hood': 5, 'AlrmTrigSrc_Tr': 6, 'AlrmTrigSrc_IMMOFaild': 7, 'AlrmTrigSrc_Alcohol': 8, 'AlrmTrigSrc_SnsrSoundrBattBacked': 9, 'AlrmTrigSrc_SnsrIncln': 10, 'AlrmTrigSrc_SnsrIntrScanr': 11, 'AlrmTrigSrc_VSTD': 12, 'AlrmTrigSrc_Reserved1': 13, 'AlrmTrigSrc_Reserved2': 14, 'AlrmTrigSrc_Reserved3': 15}
        compute_method = None
        length = 4
        startbit = 0
        bmuws_info = [(0, 0b00000001, 0b11111110, 1, 0), (1, 0b11100000, 0b00011111, 3, 5)]

    class DigKeyApproachReqKeyIdByte10:
        sig_name = "DigKeyApproachReqKeyIdByte10"
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

    class DigKeyLiReqKeyIdByte1:
        sig_name = "DigKeyLiReqKeyIdByte1"
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

    class DigKeyLiReqKeyIdByte2:
        sig_name = "DigKeyLiReqKeyIdByte2"
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

    class NFCLockUnlockReqKeyIdByte3:
        sig_name = "NFCLockUnlockReqKeyIdByte3"
        sig_start_bit = 415
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
        startbit = 415
        byte = 51
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class NFCLockUnlockReqKeyIdByte7:
        sig_name = "NFCLockUnlockReqKeyIdByte7"
        sig_start_bit = 375
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
        startbit = 375
        byte = 46
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLiReqKeyIdByte0:
        sig_name = "DigKeyLiReqKeyIdByte0"
        sig_start_bit = 287
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
        startbit = 287
        byte = 35
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyApproachReqKeyIdByte3:
        sig_name = "DigKeyApproachReqKeyIdByte3"
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

    class DigKeyLiReqDigKeyApproachLightSts:
        sig_name = "DigKeyLiReqDigKeyApproachLightSts"
        sig_start_bit = 291
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EnableDisable2_Disabled': 0, 'EnableDisable2_Enabled': 1}
        compute_method = None
        length = 1
        startbit = 291
        byte = 36
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class DigKeyLiReqKeyIdByte15:
        sig_name = "DigKeyLiReqKeyIdByte15"
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

    class NFCLockUnlockReqKeyIdByte6:
        sig_name = "NFCLockUnlockReqKeyIdByte6"
        sig_start_bit = 439
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
        startbit = 439
        byte = 54
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyApproachReqKeyIdByte0:
        sig_name = "DigKeyApproachReqKeyIdByte0"
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

    class DigKeyLiReqKeyIdByte10:
        sig_name = "DigKeyLiReqKeyIdByte10"
        sig_start_bit = 239
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
        startbit = 239
        byte = 29
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLiReqKeyIdByte13:
        sig_name = "DigKeyLiReqKeyIdByte13"
        sig_start_bit = 279
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
        startbit = 279
        byte = 34
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RLDoorAntiPnchFbOPenAntiPnchSts:
        sig_name = "RLDoorAntiPnchFbOPenAntiPnchSts"
        sig_start_bit = 328
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
        startbit = 328
        byte = 41
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class DigKeyApproachReqKeyIdByte6:
        sig_name = "DigKeyApproachReqKeyIdByte6"
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

    class DigKeyApproachReqKeyIdByte15:
        sig_name = "DigKeyApproachReqKeyIdByte15"
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

    class RLDoorMtnSts:
        sig_name = "RLDoorMtnSts"
        sig_start_bit = 333
        update_id_bit = 477
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 9
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorMtnSts_IniVal': 0, 'DoorMtnSts_FullOpen': 1, 'DoorMtnSts_FullClose': 2, 'DoorMtnSts_StopDurOpen': 3, 'DoorMtnSts_StopDurClose': 4, 'DoorMtnSts_MovingOut': 5, 'DoorMtnSts_MovingIn': 6, 'DoorMtnSts_HalfClose': 7, 'DoorMtnSts_Unknow': 8, 'DoorMtnSts_OnlyOpenPosn': 9}
        compute_method = None
        length = 4
        startbit = 333
        byte = 41
        mask = 0b00111100
        unmask = 0b11000011
        shift = 2

    class AlrmAcoustReq:
        sig_name = "AlrmAcoustReq"
        sig_start_bit = 7
        update_id_bit = 16
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
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class DigKeyLiReqKeyIdByte12:
        sig_name = "DigKeyLiReqKeyIdByte12"
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

    class NFCLockUnlockReqKeyIdByte4:
        sig_name = "NFCLockUnlockReqKeyIdByte4"
        sig_start_bit = 431
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
        startbit = 431
        byte = 53
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLiReqKeyIdByte8:
        sig_name = "DigKeyLiReqKeyIdByte8"
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

    class DigKeyApproachReqKeyIdByte13:
        sig_name = "DigKeyApproachReqKeyIdByte13"
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

    class CentralLockStsTrigSrcType:
        sig_name = "CentralLockStsTrigSrcType"
        sig_start_bit = 18
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TrigSrcType_IniVal': 0, 'TrigSrcType_Outd': 1, 'TrigSrcType_Insd': 2}
        compute_method = None
        length = 2
        startbit = 18
        byte = 2
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class AlrmSts:
        sig_name = "AlrmSts"
        sig_start_bit = 5
        update_id_bit = 290
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSts_Disarmd': 0, 'AlrmSts_Armd': 1, 'AlrmSts_Actv': 2, 'AlrmSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class DigKeyApproachReqKeyIdByte7:
        sig_name = "DigKeyApproachReqKeyIdByte7"
        sig_start_bit = 111
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
        startbit = 111
        byte = 13
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RLDoorAntiPnchFb_UB:
        sig_name = "RLDoorAntiPnchFb_UB"
        sig_start_bit = 478
        update_id_bit = 478
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
        startbit = 478
        byte = 59
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class DigKeyApproachReqKeyIdByte1:
        sig_name = "DigKeyApproachReqKeyIdByte1"
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

    class DigKeyLiReq_UB:
        sig_name = "DigKeyLiReq_UB"
        sig_start_bit = 466
        update_id_bit = 466
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
        startbit = 466
        byte = 58
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class DigKeyApproachReqKeyIdByte5:
        sig_name = "DigKeyApproachReqKeyIdByte5"
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

    class NFCLockUnlockReqKeyIdByte13:
        sig_name = "NFCLockUnlockReqKeyIdByte13"
        sig_start_bit = 407
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
        startbit = 407
        byte = 50
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyApproachReqKeyIdByte14:
        sig_name = "DigKeyApproachReqKeyIdByte14"
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

    class NFCLockUnlockReqKeyIdByte1:
        sig_name = "NFCLockUnlockReqKeyIdByte1"
        sig_start_bit = 383
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
        startbit = 383
        byte = 47
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CentralLockStsUpdateEvnt:
        sig_name = "CentralLockStsUpdateEvnt"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 8
        byte = 1
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class RLDoorAntiPnchFbCloseAntiPnchSts:
        sig_name = "RLDoorAntiPnchFbCloseAntiPnchSts"
        sig_start_bit = 329
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
        startbit = 329
        byte = 41
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class DigKeyApproachReqDigKeyApproaReq:
        sig_name = "DigKeyApproachReqDigKeyApproaReq"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DigKeyApproaReq_Idle': 0, 'DigKeyApproaReq_ApproachUnlockWithoutDoorOpen': 1, 'DigKeyApproaReq_ApproachUnlockWithDrvrDoorMinAngleOpen': 2, 'DigKeyApproaReq_ApproachUnlockWithDrvrDoorFullOpen': 3, 'DigKeyApproaReq_WalkAwayLockWithoutAnyDoorClose': 4, 'DigKeyApproaReq_WalkAwayLockWithDriverDoorClose': 5, 'DigKeyApproaReq_WalkAwayLockWithSideDoorClose': 6, 'DigKeyApproaReq_WalkAwayLockWithAllDoorClose': 7, 'DigKeyApproaReq_Reserved1': 8, 'DigKeyApproaReq_Reserved2': 9, 'DigKeyApproaReq_Reserved3': 10}
        compute_method = None
        length = 4
        startbit = 47
        byte = 5
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class NFCLockUnlockReqKeyPrsntSts:
        sig_name = "NFCLockUnlockReqKeyPrsntSts"
        sig_start_bit = 471
        update_id_bit = None
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
        startbit = 471
        byte = 58
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class DigKeyApproachReqKeyIdByte2:
        sig_name = "DigKeyApproachReqKeyIdByte2"
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

    class DigKeyApproachReqKeyIdByte4:
        sig_name = "DigKeyApproachReqKeyIdByte4"
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


class CCUMCUCDInfoCANFDFr10:
    msg_name = "CCUMCUCDInfoCANFDFr10"
    msg_id = 403
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 64
    tx_node = "CCUMCUCD"
    rx_nodes = ['BNCM', 'CD', 'WPC3', 'NKR', 'WPC2', 'DRF', 'ETC']
    sig_group_dict = {'RRDoorPosnSts': ['RRDoorPosnStsDoorAngPosn', 'RRDoorPosnStsDoorPercPosn'], 'Odometer': ['OdometerValidity', 'OdometerValue'], 'RRDoorAntiPnchFb': ['RRDoorAntiPnchFbCloseAntiPnchSts', 'RRDoorAntiPnchFbOPenAntiPnchSts'], 'TrAntiPnchSts': ['TrAntiPnchStsCloseAntiPnchSts', 'TrAntiPnchStsOPenAntiPnchSts'], 'ChrgSoftSwCtrlSt': ['ChrgSoftSwCtrlStCmd', 'ChrgSoftSwCtrlStSource']}
    sig_group_dataid_dict = {}

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

    class TrAng:
        sig_name = "TrAng"
        sig_start_bit = 39
        update_id_bit = 118
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 127
        sig_byteorder = "Motorola"
        sig_value_init = 101
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 39
        byte = 4
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class RRDoorPosnSts_UB:
        sig_name = "RRDoorPosnSts_UB"
        sig_start_bit = 119
        update_id_bit = 119
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
        startbit = 119
        byte = 14
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class RRDoorMtnSts:
        sig_name = "RRDoorMtnSts"
        sig_start_bit = 29
        update_id_bit = 104
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 9
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorMtnSts_IniVal': 0, 'DoorMtnSts_FullOpen': 1, 'DoorMtnSts_FullClose': 2, 'DoorMtnSts_StopDurOpen': 3, 'DoorMtnSts_StopDurClose': 4, 'DoorMtnSts_MovingOut': 5, 'DoorMtnSts_MovingIn': 6, 'DoorMtnSts_HalfClose': 7, 'DoorMtnSts_Unknow': 8, 'DoorMtnSts_OnlyOpenPosn': 9}
        compute_method = None
        length = 4
        startbit = 29
        byte = 3
        mask = 0b00111100
        unmask = 0b11000011
        shift = 2

    class RLDoorLoglLockSts:
        sig_name = "RLDoorLoglLockSts"
        sig_start_bit = 167
        update_id_bit = 112
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorLockSts_Unknow': 0, 'DoorLockSts_Lock': 1, 'DoorLockSts_Unlock': 2}
        compute_method = None
        length = 2
        startbit = 167
        byte = 20
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class RRDoorLoglLockSts:
        sig_name = "RRDoorLoglLockSts"
        sig_start_bit = 165
        update_id_bit = 144
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorLockSts_Unknow': 0, 'DoorLockSts_Lock': 1, 'DoorLockSts_Unlock': 2}
        compute_method = None
        length = 2
        startbit = 165
        byte = 20
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class FRDoorLoglLockSts:
        sig_name = "FRDoorLoglLockSts"
        sig_start_bit = 157
        update_id_bit = 154
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorLockSts_Unknow': 0, 'DoorLockSts_Lock': 1, 'DoorLockSts_Unlock': 2}
        compute_method = None
        length = 2
        startbit = 157
        byte = 19
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class Odometer_UB:
        sig_name = "Odometer_UB"
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

    class RRDoorPosnStsDoorPercPosn:
        sig_name = "RRDoorPosnStsDoorPercPosn"
        sig_start_bit = 103
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 101
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 103
        byte = 12
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

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

    class RRDoorAntiPnchFbOPenAntiPnchSts:
        sig_name = "RRDoorAntiPnchFbOPenAntiPnchSts"
        sig_start_bit = 30
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
        startbit = 30
        byte = 3
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class RRDoorAntiPnchFb_UB:
        sig_name = "RRDoorAntiPnchFb_UB"
        sig_start_bit = 42
        update_id_bit = 42
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
        startbit = 42
        byte = 5
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class RRDoorAntiPnchFbCloseAntiPnchSts:
        sig_name = "RRDoorAntiPnchFbCloseAntiPnchSts"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class TrAntiPnchStsOPenAntiPnchSts:
        sig_name = "TrAntiPnchStsOPenAntiPnchSts"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 24
        byte = 3
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FLDoorLoglLockSts:
        sig_name = "FLDoorLoglLockSts"
        sig_start_bit = 159
        update_id_bit = 155
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorLockSts_Unknow': 0, 'DoorLockSts_Lock': 1, 'DoorLockSts_Unlock': 2}
        compute_method = None
        length = 2
        startbit = 159
        byte = 19
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class FrntScrnWakeup:
        sig_name = "FrntScrnWakeup"
        sig_start_bit = 153
        update_id_bit = 152
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
        startbit = 153
        byte = 19
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class TrAntiPnchStsCloseAntiPnchSts:
        sig_name = "TrAntiPnchStsCloseAntiPnchSts"
        sig_start_bit = 25
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
        startbit = 25
        byte = 3
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class CDNADPwrSubStsExt:
        sig_name = "CDNADPwrSubStsExt"
        sig_start_bit = 251
        update_id_bit = 240
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SOCPwrSubSts_Default': 0, 'SOCPwrSubSts_ColdStart': 1, 'SOCPwrSubSts_WarmStart': 2, 'SOCPwrSubSts_ShutDownToSTR': 3, 'SOCPwrSubSts_ShutDownToOFF': 4, 'SOCPwrSubSts_ErrorToOFF': 5, 'SOCPwrSubSts_Reset': 6, 'SOCPwrSubSts_STRFailedToOFF': 7, 'SOCPwrSubSts_StartFailed': 8, 'SOCPwrSubSts_StartInhibit': 9, 'SOCPwrSubSts_SelfWakeup': 10}
        compute_method = None
        length = 4
        startbit = 251
        byte = 31
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class TrMtnSts:
        sig_name = "TrMtnSts"
        sig_start_bit = 47
        update_id_bit = 116
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 9
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorMtnSts_IniVal': 0, 'DoorMtnSts_FullOpen': 1, 'DoorMtnSts_FullClose': 2, 'DoorMtnSts_StopDurOpen': 3, 'DoorMtnSts_StopDurClose': 4, 'DoorMtnSts_MovingOut': 5, 'DoorMtnSts_MovingIn': 6, 'DoorMtnSts_HalfClose': 7, 'DoorMtnSts_Unknow': 8, 'DoorMtnSts_OnlyOpenPosn': 9}
        compute_method = None
        length = 4
        startbit = 47
        byte = 5
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class TrAntiPnchSts_UB:
        sig_name = "TrAntiPnchSts_UB"
        sig_start_bit = 117
        update_id_bit = 117
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
        startbit = 117
        byte = 14
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

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

    class CDNADPwrStsExt:
        sig_name = "CDNADPwrStsExt"
        sig_start_bit = 255
        update_id_bit = 241
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SOCPwrModSts_Default': 0, 'SOCPwrModSts_OFF': 1, 'SOCPwrModSts_STR': 2, 'SOCPwrModSts_Start': 3, 'SOCPwrModSts_PowerOn': 4, 'SOCPwrModSts_ShutDown': 5}
        compute_method = None
        length = 4
        startbit = 255
        byte = 31
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class VehTiGlb:
        sig_name = "VehTiGlb"
        sig_start_bit = 71
        update_id_bit = 113
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
        startbit = 71
        bmuws_info = [(8, 0b11111111, 0b00000000, 8, 0), (9, 0b11111111, 0b00000000, 8, 0), (10, 0b11111111, 0b00000000, 8, 0), (11, 0b11111111, 0b00000000, 8, 0)]

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

    class RRChdLockSts:
        sig_name = "RRChdLockSts"
        sig_start_bit = 17
        update_id_bit = 43
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorLockSts_Unknow': 0, 'DoorLockSts_Lock': 1, 'DoorLockSts_Unlock': 2}
        compute_method = None
        length = 2
        startbit = 17
        byte = 2
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class TrPosn:
        sig_name = "TrPosn"
        sig_start_bit = 63
        update_id_bit = 115
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 101
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RRDoorPosnStsDoorAngPosn:
        sig_name = "RRDoorPosnStsDoorAngPosn"
        sig_start_bit = 111
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 127
        sig_byteorder = "Motorola"
        sig_value_init = 101
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 111
        byte = 13
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

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

    class VehBattU:
        sig_name = "VehBattU"
        sig_start_bit = 41
        update_id_bit = 114
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
        startbit = 41
        bmuws_info = [(5, 0b00000011, 0b11111100, 2, 0), (6, 0b11111111, 0b00000000, 8, 0)]


class CCUMCUCDtoBNCMBLEVehDataUpdInfoCANFDFrame:
    msg_name = "CCUMCUCDtoBNCMBLEVehDataUpdInfoCANFDFrame"
    msg_id = 786
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "CCUMCUCD"
    rx_nodes = ['BNCM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class CCUMCUCDInfoCANFDFr13:
    msg_name = "CCUMCUCDInfoCANFDFr13"
    msg_id = 404
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 8
    tx_node = "CCUMCUCD"
    rx_nodes = ['ETC', 'CD']
    sig_group_dict = {'DisplayGear': ['DisplayGearChks', 'DisplayGearCntr', 'DisplayGearLvl'], 'DisplaySafeEnable': ['DisplaySafeEnableChks', 'DisplaySafeEnableCntr', 'DisplaySafeEnableSts'], 'CabinControlFlt': ['CabinControlFltChks', 'CabinControlFltCntr', 'CabinControlFltsts']}
    sig_group_dataid_dict = {}

    class DisplayGear_UB:
        sig_name = "DisplayGear_UB"
        sig_start_bit = 40
        update_id_bit = 40
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
        startbit = 40
        byte = 5
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class DisplaySafeEnable_UB:
        sig_name = "DisplaySafeEnable_UB"
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

    class CabinControlFltCntr:
        sig_name = "CabinControlFltCntr"
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

    class CDSOCPwrSubSts:
        sig_name = "CDSOCPwrSubSts"
        sig_start_bit = 3
        update_id_bit = 14
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SOCPwrSubSts_Default': 0, 'SOCPwrSubSts_ColdStart': 1, 'SOCPwrSubSts_WarmStart': 2, 'SOCPwrSubSts_ShutDownToSTR': 3, 'SOCPwrSubSts_ShutDownToOFF': 4, 'SOCPwrSubSts_ErrorToOFF': 5, 'SOCPwrSubSts_Reset': 6, 'SOCPwrSubSts_STRFailedToOFF': 7, 'SOCPwrSubSts_StartFailed': 8, 'SOCPwrSubSts_StartInhibit': 9, 'SOCPwrSubSts_SelfWakeup': 10}
        compute_method = None
        length = 4
        startbit = 3
        byte = 0
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DisplayGearCntr:
        sig_name = "DisplayGearCntr"
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

    class DisplaySafeEnableCntr:
        sig_name = "DisplaySafeEnableCntr"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DisplaySafeEnableSts:
        sig_name = "DisplaySafeEnableSts"
        sig_start_bit = 59
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EnableDisable_Enable': 0, 'EnableDisable_Disable': 1}
        compute_method = None
        length = 1
        startbit = 59
        byte = 7
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class CabinControlFlt_UB:
        sig_name = "CabinControlFlt_UB"
        sig_start_bit = 26
        update_id_bit = 26
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
        startbit = 26
        byte = 3
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class DisplayGearLvl:
        sig_name = "DisplayGearLvl"
        sig_start_bit = 43
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GearLvrIndcn_Default': 0, 'GearLvrIndcn_P': 1, 'GearLvrIndcn_R': 2, 'GearLvrIndcn_N': 3, 'GearLvrIndcn_D': 4, 'GearLvrIndcn_Reserved1': 5, 'GearLvrIndcn_Reserved2': 6, 'GearLvrIndcn_Undefd': 7}
        compute_method = None
        length = 3
        startbit = 43
        byte = 5
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class DisplayGearChks:
        sig_name = "DisplayGearChks"
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

    class CDSOCPwrSts:
        sig_name = "CDSOCPwrSts"
        sig_start_bit = 7
        update_id_bit = 15
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SOCPwrModSts_Default': 0, 'SOCPwrModSts_OFF': 1, 'SOCPwrModSts_STR': 2, 'SOCPwrModSts_Start': 3, 'SOCPwrModSts_PowerOn': 4, 'SOCPwrModSts_ShutDown': 5}
        compute_method = None
        length = 4
        startbit = 7
        byte = 0
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class CabinControlFltsts:
        sig_name = "CabinControlFltsts"
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
        sig_value_table = {'Flt1_NoFault': 0, 'Flt1_Fault': 1}
        compute_method = None
        length = 1
        startbit = 27
        byte = 3
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class DisplaySafeEnableChks:
        sig_name = "DisplaySafeEnableChks"
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

    class CabinControlFltChks:
        sig_name = "CabinControlFltChks"
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


class DRFInfoCANFDNmFr:
    msg_name = "DRFInfoCANFDNmFr"
    msg_id = 1284
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "DRF"
    rx_nodes = ['CD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class ETCMInfoCANFDNmFr:
    msg_name = "ETCMInfoCANFDNmFr"
    msg_id = 1289
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "ETCM"
    rx_nodes = ['DRF']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class BNCMtoWPC2NFCKeyRespInsdInfoCANFDFrame:
    msg_name = "BNCMtoWPC2NFCKeyRespInsdInfoCANFDFrame"
    msg_id = 777
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "BNCM"
    rx_nodes = ['WPC2']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class WPC2ToCCUMCUCDInfoCANFDDiagRespFrame:
    msg_name = "WPC2ToCCUMCUCDInfoCANFDDiagRespFrame"
    msg_id = 1572
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "WPC2"
    rx_nodes = ['CCUMCUCD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class DRFToCCUMCUCDInfoCANFDDiagRespFrame:
    msg_name = "DRFToCCUMCUCDInfoCANFDDiagRespFrame"
    msg_id = 1577
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "DRF"
    rx_nodes = ['CCUMCUCD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class CDInfoCANFDNmFr:
    msg_name = "CDInfoCANFDNmFr"
    msg_id = 1283
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CD"
    rx_nodes = ['CCUMCUCD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class WPC2InfoCANFDNmFr:
    msg_name = "WPC2InfoCANFDNmFr"
    msg_id = 1286
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "WPC2"
    rx_nodes = ['TPM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class BNCMtoCCUMCUCDInfoCANFDFCFrame:
    msg_name = "BNCMtoCCUMCUCDInfoCANFDFCFrame"
    msg_id = 787
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "BNCM"
    rx_nodes = ['CCUMCUCD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class WPC3InfoCANFDNmFr:
    msg_name = "WPC3InfoCANFDNmFr"
    msg_id = 1287
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "WPC3"
    rx_nodes = ['WPC2']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class CCUMCUCDInfoCANFDFr05:
    msg_name = "CCUMCUCDInfoCANFDFr05"
    msg_id = 658
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 64
    tx_node = "CCUMCUCD"
    rx_nodes = ['CD']
    sig_group_dict = {'VehCfgDataGrp': ['VehCfgDataGrpVehCfgData1BlkIDBytePosn1', 'VehCfgDataGrpVehCfgData1BytePosn10', 'VehCfgDataGrpVehCfgData1BytePosn11', 'VehCfgDataGrpVehCfgData1BytePosn12', 'VehCfgDataGrpVehCfgData1BytePosn13', 'VehCfgDataGrpVehCfgData1BytePosn14', 'VehCfgDataGrpVehCfgData1BytePosn15', 'VehCfgDataGrpVehCfgData1BytePosn16', 'VehCfgDataGrpVehCfgData1BytePosn17', 'VehCfgDataGrpVehCfgData1BytePosn18', 'VehCfgDataGrpVehCfgData1BytePosn19', 'VehCfgDataGrpVehCfgData1BytePosn2', 'VehCfgDataGrpVehCfgData1BytePosn20', 'VehCfgDataGrpVehCfgData1BytePosn21', 'VehCfgDataGrpVehCfgData1BytePosn22', 'VehCfgDataGrpVehCfgData1BytePosn23', 'VehCfgDataGrpVehCfgData1BytePosn24', 'VehCfgDataGrpVehCfgData1BytePosn25', 'VehCfgDataGrpVehCfgData1BytePosn26', 'VehCfgDataGrpVehCfgData1BytePosn27', 'VehCfgDataGrpVehCfgData1BytePosn28', 'VehCfgDataGrpVehCfgData1BytePosn29', 'VehCfgDataGrpVehCfgData1BytePosn3', 'VehCfgDataGrpVehCfgData1BytePosn30', 'VehCfgDataGrpVehCfgData1BytePosn31', 'VehCfgDataGrpVehCfgData1BytePosn32', 'VehCfgDataGrpVehCfgData1BytePosn33', 'VehCfgDataGrpVehCfgData1BytePosn34', 'VehCfgDataGrpVehCfgData1BytePosn35', 'VehCfgDataGrpVehCfgData1BytePosn36', 'VehCfgDataGrpVehCfgData1BytePosn37', 'VehCfgDataGrpVehCfgData1BytePosn38', 'VehCfgDataGrpVehCfgData1BytePosn39', 'VehCfgDataGrpVehCfgData1BytePosn4', 'VehCfgDataGrpVehCfgData1BytePosn40', 'VehCfgDataGrpVehCfgData1BytePosn41', 'VehCfgDataGrpVehCfgData1BytePosn42', 'VehCfgDataGrpVehCfgData1BytePosn43', 'VehCfgDataGrpVehCfgData1BytePosn44', 'VehCfgDataGrpVehCfgData1BytePosn45', 'VehCfgDataGrpVehCfgData1BytePosn46', 'VehCfgDataGrpVehCfgData1BytePosn47', 'VehCfgDataGrpVehCfgData1BytePosn48', 'VehCfgDataGrpVehCfgData1BytePosn49', 'VehCfgDataGrpVehCfgData1BytePosn5', 'VehCfgDataGrpVehCfgData1BytePosn50', 'VehCfgDataGrpVehCfgData1BytePosn51', 'VehCfgDataGrpVehCfgData1BytePosn52', 'VehCfgDataGrpVehCfgData1BytePosn53', 'VehCfgDataGrpVehCfgData1BytePosn54', 'VehCfgDataGrpVehCfgData1BytePosn55', 'VehCfgDataGrpVehCfgData1BytePosn56', 'VehCfgDataGrpVehCfgData1BytePosn57', 'VehCfgDataGrpVehCfgData1BytePosn58', 'VehCfgDataGrpVehCfgData1BytePosn59', 'VehCfgDataGrpVehCfgData1BytePosn6', 'VehCfgDataGrpVehCfgData1BytePosn60', 'VehCfgDataGrpVehCfgData1BytePosn61', 'VehCfgDataGrpVehCfgData1BytePosn62', 'VehCfgDataGrpVehCfgData1BytePosn63', 'VehCfgDataGrpVehCfgData1BytePosn64', 'VehCfgDataGrpVehCfgData1BytePosn7', 'VehCfgDataGrpVehCfgData1BytePosn8', 'VehCfgDataGrpVehCfgData1BytePosn9']}
    sig_group_dataid_dict = {}

    class VehCfgDataGrpVehCfgData1BytePosn58:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn58"
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

    class VehCfgDataGrpVehCfgData1BytePosn36:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn36"
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

    class VehCfgDataGrpVehCfgData1BytePosn25:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn25"
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

    class VehCfgDataGrpVehCfgData1BytePosn26:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn26"
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

    class VehCfgDataGrpVehCfgData1BytePosn17:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn17"
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

    class VehCfgDataGrpVehCfgData1BytePosn60:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn60"
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

    class VehCfgDataGrpVehCfgData1BytePosn2:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn2"
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

    class VehCfgDataGrpVehCfgData1BytePosn33:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn33"
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

    class VehCfgDataGrpVehCfgData1BytePosn11:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn11"
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

    class VehCfgDataGrpVehCfgData1BytePosn19:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn19"
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

    class VehCfgDataGrpVehCfgData1BytePosn49:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn49"
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

    class VehCfgDataGrpVehCfgData1BytePosn29:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn29"
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

    class VehCfgDataGrpVehCfgData1BytePosn16:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn16"
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

    class VehCfgDataGrpVehCfgData1BytePosn50:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn50"
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

    class VehCfgDataGrpVehCfgData1BytePosn27:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn27"
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

    class VehCfgDataGrpVehCfgData1BytePosn44:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn44"
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

    class VehCfgDataGrpVehCfgData1BytePosn28:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn28"
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

    class VehCfgDataGrpVehCfgData1BytePosn8:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn8"
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

    class VehCfgDataGrpVehCfgData1BytePosn56:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn56"
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

    class VehCfgDataGrpVehCfgData1BytePosn6:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn6"
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

    class VehCfgDataGrpVehCfgData1BytePosn10:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn10"
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

    class VehCfgDataGrpVehCfgData1BytePosn5:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn5"
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

    class VehCfgDataGrpVehCfgData1BytePosn32:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn32"
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

    class VehCfgDataGrpVehCfgData1BytePosn41:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn41"
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

    class VehCfgDataGrpVehCfgData1BytePosn54:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn54"
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

    class VehCfgDataGrpVehCfgData1BytePosn34:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn34"
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

    class VehCfgDataGrpVehCfgData1BytePosn3:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn3"
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

    class VehCfgDataGrpVehCfgData1BytePosn63:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn63"
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

    class VehCfgDataGrpVehCfgData1BytePosn9:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn9"
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

    class VehCfgDataGrpVehCfgData1BytePosn55:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn55"
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

    class VehCfgDataGrpVehCfgData1BytePosn30:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn30"
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

    class VehCfgDataGrpVehCfgData1BlkIDBytePosn1:
        sig_name = "VehCfgDataGrpVehCfgData1BlkIDBytePosn1"
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

    class VehCfgDataGrpVehCfgData1BytePosn45:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn45"
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

    class VehCfgDataGrpVehCfgData1BytePosn7:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn7"
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

    class VehCfgDataGrpVehCfgData1BytePosn57:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn57"
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

    class VehCfgDataGrpVehCfgData1BytePosn43:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn43"
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

    class VehCfgDataGrpVehCfgData1BytePosn42:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn42"
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

    class VehCfgDataGrpVehCfgData1BytePosn59:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn59"
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

    class VehCfgDataGrpVehCfgData1BytePosn21:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn21"
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

    class VehCfgDataGrpVehCfgData1BytePosn38:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn38"
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

    class VehCfgDataGrpVehCfgData1BytePosn47:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn47"
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

    class VehCfgDataGrpVehCfgData1BytePosn20:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn20"
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

    class VehCfgDataGrpVehCfgData1BytePosn52:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn52"
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

    class VehCfgDataGrpVehCfgData1BytePosn31:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn31"
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

    class VehCfgDataGrpVehCfgData1BytePosn48:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn48"
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

    class VehCfgDataGrpVehCfgData1BytePosn37:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn37"
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

    class VehCfgDataGrpVehCfgData1BytePosn40:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn40"
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

    class VehCfgDataGrpVehCfgData1BytePosn22:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn22"
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

    class VehCfgDataGrpVehCfgData1BytePosn61:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn61"
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

    class VehCfgDataGrpVehCfgData1BytePosn64:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn64"
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

    class VehCfgDataGrpVehCfgData1BytePosn15:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn15"
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

    class VehCfgDataGrpVehCfgData1BytePosn46:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn46"
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

    class VehCfgDataGrpVehCfgData1BytePosn51:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn51"
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

    class VehCfgDataGrpVehCfgData1BytePosn62:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn62"
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

    class VehCfgDataGrpVehCfgData1BytePosn13:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn13"
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

    class VehCfgDataGrpVehCfgData1BytePosn53:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn53"
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

    class VehCfgDataGrpVehCfgData1BytePosn4:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn4"
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

    class VehCfgDataGrpVehCfgData1BytePosn14:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn14"
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

    class VehCfgDataGrpVehCfgData1BytePosn18:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn18"
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

    class VehCfgDataGrpVehCfgData1BytePosn39:
        sig_name = "VehCfgDataGrpVehCfgData1BytePosn39"
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


class NKRInfoCANFDFr01:
    msg_name = "NKRInfoCANFDFr01"
    msg_id = 661
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 16
    tx_node = "NKR"
    rx_nodes = ['BNCM', 'CCUMCUCD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class NFCSts:
        sig_name = "NFCSts"
        sig_start_bit = 7
        update_id_bit = 5
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NFCSts_NotDetected': 0, 'NFCSts_Detected': 1}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class BNCMInfoCANFDFr04:
    msg_name = "BNCMInfoCANFDFr04"
    msg_id = 778
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.2
    msg_length = 64
    tx_node = "BNCM"
    rx_nodes = ['CCUMCUCD', 'ETC']
    sig_group_dict = {'BLEChrgrPileInfo': ['BLEChrgrPileInfoChrgrPileInfo', 'BLEChrgrPileInfoChrgrPilePwr', 'BLEChrgrPileInfoChrgrPileTyp'], 'DigKeyApproachFailSts': ['DigKeyApproachFailStsDigKeyApproachFailCod', 'DigKeyApproachFailStsDigKeyApproachFct']}
    sig_group_dataid_dict = {}

    class BLELocnActvSts:
        sig_name = "BLELocnActvSts"
        sig_start_bit = 0
        update_id_bit = 167
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
        startbit = 0
        byte = 0
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class BLEChrgrPileInfoChrgrPilePwr:
        sig_name = "BLEChrgrPileInfoChrgrPilePwr"
        sig_start_bit = 3
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ChrgrPilePwr_Invalid': 0, 'ChrgrPilePwr_7KW': 1, 'ChrgrPilePwr_360KW': 2, 'ChrgrPilePwr_800KW': 3, 'ChrgrPilePwr_Reserved1': 4, 'ChrgrPilePwr_Reserved2': 5, 'ChrgrPilePwr_Reserved3': 6, 'ChrgrPilePwr_Reserved4': 7}
        compute_method = None
        length = 3
        startbit = 3
        byte = 0
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class BLEChrgrPileInfo_UB:
        sig_name = "BLEChrgrPileInfo_UB"
        sig_start_bit = 153
        update_id_bit = 153
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
        startbit = 153
        byte = 19
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class BLEChrgrPileInfoChrgrPileTyp:
        sig_name = "BLEChrgrPileInfoChrgrPileTyp"
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
        sig_value_table = {'ChrgrPileTyp_Invalid': 0, 'ChrgrPileTyp_DC': 1, 'ChrgrPileTyp_AC': 2, 'ChrgrPileTyp_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class BLEComErrCod:
        sig_name = "BLEComErrCod"
        sig_start_bit = 15
        update_id_bit = 152
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DigKeyComErrCode_NoErr': 0, 'DigKeyComErrCode_AntiReplayErr': 1, 'DigKeyComErrCode_MACErr': 2, 'DigKeyComErrCode_UndefinedCmd': 3, 'DigKeyComErrCode_DataLengthErr': 4, 'DigKeyComErrCode_Reserved1': 5, 'DigKeyComErrCode_Reserved2': 6, 'DigKeyComErrCode_Reserved3': 7}
        compute_method = None
        length = 3
        startbit = 15
        byte = 1
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class BLEWarnSts:
        sig_name = "BLEWarnSts"
        sig_start_bit = 12
        update_id_bit = 165
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
        startbit = 12
        byte = 1
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class DigKeyApproachFailSts_UB:
        sig_name = "DigKeyApproachFailSts_UB"
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

    class InsdNFCWarnSts:
        sig_name = "InsdNFCWarnSts"
        sig_start_bit = 87
        update_id_bit = 162
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
        startbit = 87
        byte = 10
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class NFCAuthLockUnlckFailCod:
        sig_name = "NFCAuthLockUnlckFailCod"
        sig_start_bit = 159
        update_id_bit = 161
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NFCAuthFailCode_Idle': 0, 'NFCAuthFailCode_BNCMRootKeyMissed': 1, 'NFCAuthFailCode_NotInWhiteList': 2, 'NFCAuthFailCode_AuthFailure': 3, 'NFCAuthFailCode_TimeOut': 4, 'NFCAuthFailCode_Reserved1': 5, 'NFCAuthFailCode_Reserved2': 6, 'NFCAuthFailCode_Reserved3': 7}
        compute_method = None
        length = 3
        startbit = 159
        byte = 19
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class BLESlotKeyWhiteListVers:
        sig_name = "BLESlotKeyWhiteListVers"
        sig_start_bit = 23
        update_id_bit = 166
        sig_length = 64
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 64
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111111, 0b00000000, 8, 0), (8, 0b11111111, 0b00000000, 8, 0), (9, 0b11111111, 0b00000000, 8, 0)]

    class NFCStrtAuthFailSts:
        sig_name = "NFCStrtAuthFailSts"
        sig_start_bit = 11
        update_id_bit = 160
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NFCAuthFailCode_Idle': 0, 'NFCAuthFailCode_BNCMRootKeyMissed': 1, 'NFCAuthFailCode_NotInWhiteList': 2, 'NFCAuthFailCode_AuthFailure': 3, 'NFCAuthFailCode_TimeOut': 4, 'NFCAuthFailCode_Reserved1': 5, 'NFCAuthFailCode_Reserved2': 6, 'NFCAuthFailCode_Reserved3': 7}
        compute_method = None
        length = 3
        startbit = 11
        byte = 1
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class OutdNFCWarnSts:
        sig_name = "OutdNFCWarnSts"
        sig_start_bit = 8
        update_id_bit = 175
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
        startbit = 8
        byte = 1
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class UWBLocnActvSts:
        sig_name = "UWBLocnActvSts"
        sig_start_bit = 156
        update_id_bit = 174
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'UWBLocnActvSts_Unkown': 0, 'UWBLocnActvSts_NonActivated': 1, 'UWBLocnActvSts_ApproachActivated': 2, 'UWBLocnActvSts_WalkAwayActivated': 3, 'UWBLocnActvSts_FindKeyActivated': 4, 'UWBLocnActvSts_Reserved1': 5, 'UWBLocnActvSts_Reserved2': 6, 'UWBLocnActvSts_Reserved3': 7}
        compute_method = None
        length = 3
        startbit = 156
        byte = 19
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class DigKeyApproachFailStsDigKeyApproachFailCod:
        sig_name = "DigKeyApproachFailStsDigKeyApproachFailCod"
        sig_start_bit = 83
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DigKeyApproachFailCod_Idle': 0, 'DigKeyApproachFailCod_CarModeNotMet': 1, 'DigKeyApproachFailCod_UsgModeNotMet': 2, 'DigKeyApproachFailCod_DisabledByProtection': 3, 'DigKeyApproachFailCod_LockStsNotMet': 4, 'DigKeyApproachFailCod_OccupyStsNotMet': 5, 'DigKeyApproachFailCod_FunctionSettingIsOFF': 6, 'DigKeyApproachFailCod_OtherKeyExist': 7, 'DigKeyApproachFailCod_Reserved1': 8, 'DigKeyApproachFailCod_Reserved2': 9, 'DigKeyApproachFailCod_Reserved3': 10}
        compute_method = None
        length = 4
        startbit = 83
        byte = 10
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class EntityKeyWhiteListVers:
        sig_name = "EntityKeyWhiteListVers"
        sig_start_bit = 95
        update_id_bit = 163
        sig_length = 64
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 64
        startbit = 95
        bmuws_info = [(11, 0b11111111, 0b00000000, 8, 0), (12, 0b11111111, 0b00000000, 8, 0), (13, 0b11111111, 0b00000000, 8, 0), (14, 0b11111111, 0b00000000, 8, 0), (15, 0b11111111, 0b00000000, 8, 0), (16, 0b11111111, 0b00000000, 8, 0), (17, 0b11111111, 0b00000000, 8, 0), (18, 0b11111111, 0b00000000, 8, 0)]

    class BLEChrgrPileInfoChrgrPileInfo:
        sig_name = "BLEChrgrPileInfoChrgrPileInfo"
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
        sig_value_table = {'ChrgrPileInfo_Invalid': 0, 'ChrgrPileInfo_Private': 1, 'ChrgrPileInfo_Public': 2, 'ChrgrPileInfo_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class DigKeyApproachFailStsDigKeyApproachFct:
        sig_name = "DigKeyApproachFailStsDigKeyApproachFct"
        sig_start_bit = 86
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DigKeyApproachFct_Idle': 0, 'DigKeyApproachFct_WakeUp': 1, 'DigKeyApproachFct_WelcomeLight': 2, 'DigKeyApproachFct_AutoUnLock': 3, 'DigKeyApproachFct_AutoLock': 4}
        compute_method = None
        length = 3
        startbit = 86
        byte = 10
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4


class CCUMCUCDToDRFInfoCANFDDiagReqFrame:
    msg_name = "CCUMCUCDToDRFInfoCANFDDiagReqFrame"
    msg_id = 1833
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "CCUMCUCD"
    rx_nodes = ['DRF']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class CCUMCUCDToWPC2InfoCANFDDiagReqFrame:
    msg_name = "CCUMCUCDToWPC2InfoCANFDDiagReqFrame"
    msg_id = 1828
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "CCUMCUCD"
    rx_nodes = ['WPC2']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class CDToCCUMCUCDInfoCANFDDiagRespFrame:
    msg_name = "CDToCCUMCUCDInfoCANFDDiagRespFrame"
    msg_id = 1665
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "CD"
    rx_nodes = ['CCUMCUCD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class BNCMtoNKRNFCKeyRespOutdInfoCANFDFrame:
    msg_name = "BNCMtoNKRNFCKeyRespOutdInfoCANFDFrame"
    msg_id = 775
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "BNCM"
    rx_nodes = ['NKR']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class CDInfoCANFDFr03:
    msg_name = "CDInfoCANFDFr03"
    msg_id = 576
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 16
    tx_node = "CD"
    rx_nodes = ['CCUMCUCD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class DisplayAreaSts:
        sig_name = "DisplayAreaSts"
        sig_start_bit = 34
        update_id_bit = 70
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 7
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 34
        byte = 4
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class LuminanceLevelFedBck:
        sig_name = "LuminanceLevelFedBck"
        sig_start_bit = 63
        update_id_bit = 65
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "SCALE_LINEAR_AND_TEXTTABLE"
        sig_value_table = {'BattSOH_Invalid': 255}
        compute_method = None
        length = 8
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class CCUMCUCDToCDInfoCANFDDiagReqFrame:
    msg_name = "CCUMCUCDToCDInfoCANFDDiagReqFrame"
    msg_id = 1921
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "CCUMCUCD"
    rx_nodes = ['CD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class BNCMToCCUMCUCDInfoCANFDDiagRespFrame:
    msg_name = "BNCMToCCUMCUCDInfoCANFDDiagRespFrame"
    msg_id = 1571
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "BNCM"
    rx_nodes = ['CCUMCUCD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class DRFInfoCANFDFr01:
    msg_name = "DRFInfoCANFDFr01"
    msg_id = 2
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "DRF"
    rx_nodes = ['CCUMCUCD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class RoofFolderDisplayFoldedStatus:
        sig_name = "RoofFolderDisplayFoldedStatus"
        sig_start_bit = 23
        update_id_bit = 19
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 2
        startbit = 23
        byte = 2
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class RoofFolderDisplayBrightnessLevelStatus:
        sig_name = "RoofFolderDisplayBrightnessLevelStatus"
        sig_start_bit = 7
        update_id_bit = 21
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "SCALE_LINEAR_AND_TEXTTABLE"
        sig_value_table = {'BattSOH_Invalid': 255}
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RoofFolderDisplayErrorStatus:
        sig_name = "RoofFolderDisplayErrorStatus"
        sig_start_bit = 15
        update_id_bit = 20
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


class CCUMCUCDToTPMInfoCANFDDiagReqFrame:
    msg_name = "CCUMCUCDToTPMInfoCANFDDiagReqFrame"
    msg_id = 1834
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "CCUMCUCD"
    rx_nodes = ['TPM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class BNCMInfoCANFDFr03:
    msg_name = "BNCMInfoCANFDFr03"
    msg_id = 657
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 64
    tx_node = "BNCM"
    rx_nodes = ['CCUMCUCD']
    sig_group_dict = {'DigKeyCnctInfo4': ['DigKeyCnctInfo4AutoLockOnLeaveSetting', 'DigKeyCnctInfo4AutoUnlockOnApproachSetting', 'DigKeyCnctInfo4AutoZoneKeyPrsntSts', 'DigKeyCnctInfo4BattWarn', 'DigKeyCnctInfo4KeyConnectInfo', 'DigKeyCnctInfo4KeyIdByte0', 'DigKeyCnctInfo4KeyIdByte1', 'DigKeyCnctInfo4KeyIdByte10', 'DigKeyCnctInfo4KeyIdByte11', 'DigKeyCnctInfo4KeyIdByte12', 'DigKeyCnctInfo4KeyIdByte13', 'DigKeyCnctInfo4KeyIdByte14', 'DigKeyCnctInfo4KeyIdByte15', 'DigKeyCnctInfo4KeyIdByte2', 'DigKeyCnctInfo4KeyIdByte3', 'DigKeyCnctInfo4KeyIdByte4', 'DigKeyCnctInfo4KeyIdByte5', 'DigKeyCnctInfo4KeyIdByte6', 'DigKeyCnctInfo4KeyIdByte7', 'DigKeyCnctInfo4KeyIdByte8', 'DigKeyCnctInfo4KeyIdByte9', 'DigKeyCnctInfo4KeyTyp', 'DigKeyCnctInfo4PEKeyPrsntSts', 'DigKeyCnctInfo4PSEnaSts'], 'DigKeyCnctInfo3': ['DigKeyCnctInfo3AutoLockOnLeaveSetting', 'DigKeyCnctInfo3AutoUnlockOnApproachSetting', 'DigKeyCnctInfo3AutoZoneKeyPrsntSts', 'DigKeyCnctInfo3BattWarn', 'DigKeyCnctInfo3KeyConnectInfo', 'DigKeyCnctInfo3KeyIdByte0', 'DigKeyCnctInfo3KeyIdByte1', 'DigKeyCnctInfo3KeyIdByte10', 'DigKeyCnctInfo3KeyIdByte11', 'DigKeyCnctInfo3KeyIdByte12', 'DigKeyCnctInfo3KeyIdByte13', 'DigKeyCnctInfo3KeyIdByte14', 'DigKeyCnctInfo3KeyIdByte15', 'DigKeyCnctInfo3KeyIdByte2', 'DigKeyCnctInfo3KeyIdByte3', 'DigKeyCnctInfo3KeyIdByte4', 'DigKeyCnctInfo3KeyIdByte5', 'DigKeyCnctInfo3KeyIdByte6', 'DigKeyCnctInfo3KeyIdByte7', 'DigKeyCnctInfo3KeyIdByte8', 'DigKeyCnctInfo3KeyIdByte9', 'DigKeyCnctInfo3KeyTyp', 'DigKeyCnctInfo3PEKeyPrsntSts', 'DigKeyCnctInfo3PSEnaSts']}
    sig_group_dataid_dict = {}

    class DigKeyCnctInfo3PSEnaSts:
        sig_name = "DigKeyCnctInfo3PSEnaSts"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EnableDisable2_Disabled': 0, 'EnableDisable2_Enabled': 1}
        compute_method = None
        length = 1
        startbit = 47
        byte = 5
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class DigKeyCnctInfo4KeyTyp:
        sig_name = "DigKeyCnctInfo4KeyTyp"
        sig_start_bit = 235
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 9
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeyTyp_NoKeyConnected': 0, 'KeyTyp_NFC_Card': 1, 'KeyTyp_BLE_UWB_KeyFob': 2, 'KeyTyp_Phone_NFC_Key': 3, 'KeyTyp_Phone_BLE_Key': 4, 'KeyTyp_Phone_UWB_Key': 5, 'KeyTyp_Reserved1': 6, 'KeyTyp_Reserved2': 7, 'KeyTyp_Reserved3': 8, 'KeyTyp_Reserved4': 9}
        compute_method = None
        length = 4
        startbit = 235
        byte = 29
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DigKeyCnctInfo3KeyConnectInfo:
        sig_name = "DigKeyCnctInfo3KeyConnectInfo"
        sig_start_bit = 111
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ConnectionSts_Disconnect': 0, 'ConnectionSts_Connect': 1}
        compute_method = None
        length = 1
        startbit = 111
        byte = 13
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class DigKeyCnctInfo4KeyIdByte14:
        sig_name = "DigKeyCnctInfo4KeyIdByte14"
        sig_start_bit = 199
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
        startbit = 199
        byte = 24
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyCnctInfo3KeyIdByte7:
        sig_name = "DigKeyCnctInfo3KeyIdByte7"
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

    class DigKeyCnctInfo3KeyIdByte12:
        sig_name = "DigKeyCnctInfo3KeyIdByte12"
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

    class DigKeyCnctInfo4AutoUnlockOnApproachSetting:
        sig_name = "DigKeyCnctInfo4AutoUnlockOnApproachSetting"
        sig_start_bit = 147
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ApproachUnlockSetting_Unkown': 0, 'ApproachUnlockSetting_Off': 1, 'ApproachUnlockSetting_OnWithoutDoorOpen': 2, 'ApproachUnlockSetting_OnWithDoorMinAngleOpen': 3, 'ApproachUnlockSetting_OnWithDoorFullOpen': 4}
        compute_method = None
        length = 3
        startbit = 147
        byte = 18
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class DigKeyCnctInfo3AutoUnlockOnApproachSetting:
        sig_name = "DigKeyCnctInfo3AutoUnlockOnApproachSetting"
        sig_start_bit = 110
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ApproachUnlockSetting_Unkown': 0, 'ApproachUnlockSetting_Off': 1, 'ApproachUnlockSetting_OnWithoutDoorOpen': 2, 'ApproachUnlockSetting_OnWithDoorMinAngleOpen': 3, 'ApproachUnlockSetting_OnWithDoorFullOpen': 4}
        compute_method = None
        length = 3
        startbit = 110
        byte = 13
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class DigKeyCnctInfo4KeyIdByte6:
        sig_name = "DigKeyCnctInfo4KeyIdByte6"
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

    class DigKeyCnctInfo3PEKeyPrsntSts:
        sig_name = "DigKeyCnctInfo3PEKeyPrsntSts"
        sig_start_bit = 107
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PELocnSts_Idle': 0, 'PELocnSts_PEAllExt': 1, 'PELocnSts_PEDrvrExt': 2, 'PELocnSts_PEPassExt': 3, 'PELocnSts_PEFrntExt': 4, 'PELocnSts_PERearExt': 5, 'PELocnSts_PEAllInt': 6, 'PELocnSts_Reserved': 7}
        compute_method = None
        length = 3
        startbit = 107
        byte = 13
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class DigKeyCnctInfo3KeyIdByte2:
        sig_name = "DigKeyCnctInfo3KeyIdByte2"
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

    class DigKeyCnctInfo4KeyIdByte7:
        sig_name = "DigKeyCnctInfo4KeyIdByte7"
        sig_start_bit = 287
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
        startbit = 287
        byte = 35
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyCnctInfo4KeyIdByte8:
        sig_name = "DigKeyCnctInfo4KeyIdByte8"
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

    class DigKeyCnctInfo4KeyIdByte4:
        sig_name = "DigKeyCnctInfo4KeyIdByte4"
        sig_start_bit = 247
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
        startbit = 247
        byte = 30
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyCnctInfo3KeyIdByte9:
        sig_name = "DigKeyCnctInfo3KeyIdByte9"
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

    class DigKeyCnctInfo4KeyIdByte1:
        sig_name = "DigKeyCnctInfo4KeyIdByte1"
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

    class DigKeyCnctInfo3KeyIdByte0:
        sig_name = "DigKeyCnctInfo3KeyIdByte0"
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

    class DigKeyCnctInfo3KeyIdByte11:
        sig_name = "DigKeyCnctInfo3KeyIdByte11"
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

    class DigKeyCnctInfo3KeyIdByte15:
        sig_name = "DigKeyCnctInfo3KeyIdByte15"
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

    class DigKeyCnctInfo4KeyIdByte3:
        sig_name = "DigKeyCnctInfo4KeyIdByte3"
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

    class DigKeyCnctInfo3KeyIdByte1:
        sig_name = "DigKeyCnctInfo3KeyIdByte1"
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

    class DigKeyCnctInfo3KeyIdByte10:
        sig_name = "DigKeyCnctInfo3KeyIdByte10"
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

    class DigKeyCnctInfo3KeyIdByte5:
        sig_name = "DigKeyCnctInfo3KeyIdByte5"
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

    class DigKeyCnctInfo4KeyIdByte13:
        sig_name = "DigKeyCnctInfo4KeyIdByte13"
        sig_start_bit = 295
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
        startbit = 295
        byte = 36
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyCnctInfo4KeyIdByte15:
        sig_name = "DigKeyCnctInfo4KeyIdByte15"
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

    class DigKeyCnctInfo4KeyIdByte10:
        sig_name = "DigKeyCnctInfo4KeyIdByte10"
        sig_start_bit = 223
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
        startbit = 223
        byte = 27
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyCnctInfo4KeyIdByte5:
        sig_name = "DigKeyCnctInfo4KeyIdByte5"
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

    class DigKeyCnctInfo4KeyIdByte2:
        sig_name = "DigKeyCnctInfo4KeyIdByte2"
        sig_start_bit = 271
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
        startbit = 271
        byte = 33
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyCnctInfo3KeyIdByte8:
        sig_name = "DigKeyCnctInfo3KeyIdByte8"
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

    class DigKeyCnctInfo3AutoLockOnLeaveSetting:
        sig_name = "DigKeyCnctInfo3AutoLockOnLeaveSetting"
        sig_start_bit = 46
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AutoLockOnLeaveSetting_Unkown': 0, 'AutoLockOnLeaveSetting_Off': 1, 'AutoLockOnLeaveSetting_OnWithoutAnyDoorClose': 2, 'AutoLockOnLeaveSetting_OnWithDriverDoorClose': 3, 'AutoLockOnLeaveSetting_OnWithSideDoorClose': 4, 'AutoLockOnLeaveSetting_OnWithAllDoorClose': 5}
        compute_method = None
        length = 3
        startbit = 46
        byte = 5
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class DigKeyCnctInfo3KeyIdByte6:
        sig_name = "DigKeyCnctInfo3KeyIdByte6"
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

    class DigKeyCnctInfo3AutoZoneKeyPrsntSts:
        sig_name = "DigKeyCnctInfo3AutoZoneKeyPrsntSts"
        sig_start_bit = 43
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeyPrsntZoneInfo_NotConnected': 0, 'KeyPrsntZoneInfo_Connected': 1, 'KeyPrsntZoneInfo_Welcome': 2, 'KeyPrsntZoneInfo_WalkAway': 3, 'KeyPrsntZoneInfo_LockUnlockBuffer': 4, 'KeyPrsntZoneInfo_Approach': 5, 'KeyPrsntZoneInfo_Door': 6, 'KeyPrsntZoneInfo_InCar': 7, 'KeyPrsntZoneInfo_InFL': 8, 'KeyPrsntZoneInfo_InFR': 9, 'KeyPrsntZoneInfo_InRL': 10, 'KeyPrsntZoneInfo_InRR': 11, 'KeyPrsntZoneInfo_Tr': 12, 'KeyPrsntZoneInfo_Reserved1': 13, 'KeyPrsntZoneInfo_Reserved2': 14, 'KeyPrsntZoneInfo_Reserved3': 15}
        compute_method = None
        length = 4
        startbit = 43
        byte = 5
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DigKeyCnctInfo3BattWarn:
        sig_name = "DigKeyCnctInfo3BattWarn"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 104
        byte = 13
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class DigKeyCnctInfo4KeyIdByte9:
        sig_name = "DigKeyCnctInfo4KeyIdByte9"
        sig_start_bit = 263
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
        startbit = 263
        byte = 32
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyCnctInfo4AutoZoneKeyPrsntSts:
        sig_name = "DigKeyCnctInfo4AutoZoneKeyPrsntSts"
        sig_start_bit = 255
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeyPrsntZoneInfo_NotConnected': 0, 'KeyPrsntZoneInfo_Connected': 1, 'KeyPrsntZoneInfo_Welcome': 2, 'KeyPrsntZoneInfo_WalkAway': 3, 'KeyPrsntZoneInfo_LockUnlockBuffer': 4, 'KeyPrsntZoneInfo_Approach': 5, 'KeyPrsntZoneInfo_Door': 6, 'KeyPrsntZoneInfo_InCar': 7, 'KeyPrsntZoneInfo_InFL': 8, 'KeyPrsntZoneInfo_InFR': 9, 'KeyPrsntZoneInfo_InRL': 10, 'KeyPrsntZoneInfo_InRR': 11, 'KeyPrsntZoneInfo_Tr': 12, 'KeyPrsntZoneInfo_Reserved1': 13, 'KeyPrsntZoneInfo_Reserved2': 14, 'KeyPrsntZoneInfo_Reserved3': 15}
        compute_method = None
        length = 4
        startbit = 255
        byte = 31
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DigKeyCnctInfo3KeyTyp:
        sig_name = "DigKeyCnctInfo3KeyTyp"
        sig_start_bit = 151
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 9
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeyTyp_NoKeyConnected': 0, 'KeyTyp_NFC_Card': 1, 'KeyTyp_BLE_UWB_KeyFob': 2, 'KeyTyp_Phone_NFC_Key': 3, 'KeyTyp_Phone_BLE_Key': 4, 'KeyTyp_Phone_UWB_Key': 5, 'KeyTyp_Reserved1': 6, 'KeyTyp_Reserved2': 7, 'KeyTyp_Reserved3': 8, 'KeyTyp_Reserved4': 9}
        compute_method = None
        length = 4
        startbit = 151
        byte = 18
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DigKeyCnctInfo4KeyIdByte0:
        sig_name = "DigKeyCnctInfo4KeyIdByte0"
        sig_start_bit = 191
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
        startbit = 191
        byte = 23
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyCnctInfo4_UB:
        sig_name = "DigKeyCnctInfo4_UB"
        sig_start_bit = 302
        update_id_bit = 302
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
        startbit = 302
        byte = 37
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class DigKeyCnctInfo3KeyIdByte4:
        sig_name = "DigKeyCnctInfo3KeyIdByte4"
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

    class DigKeyCnctInfo3KeyIdByte14:
        sig_name = "DigKeyCnctInfo3KeyIdByte14"
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

    class DigKeyCnctInfo3_UB:
        sig_name = "DigKeyCnctInfo3_UB"
        sig_start_bit = 303
        update_id_bit = 303
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
        startbit = 303
        byte = 37
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class DigKeyCnctInfo4PSEnaSts:
        sig_name = "DigKeyCnctInfo4PSEnaSts"
        sig_start_bit = 248
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EnableDisable2_Disabled': 0, 'EnableDisable2_Enabled': 1}
        compute_method = None
        length = 1
        startbit = 248
        byte = 31
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class DigKeyCnctInfo4BattWarn:
        sig_name = "DigKeyCnctInfo4BattWarn"
        sig_start_bit = 239
        update_id_bit = None
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
        startbit = 239
        byte = 29
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class DigKeyCnctInfo3KeyIdByte3:
        sig_name = "DigKeyCnctInfo3KeyIdByte3"
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

    class DigKeyCnctInfo4PEKeyPrsntSts:
        sig_name = "DigKeyCnctInfo4PEKeyPrsntSts"
        sig_start_bit = 238
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PELocnSts_Idle': 0, 'PELocnSts_PEAllExt': 1, 'PELocnSts_PEDrvrExt': 2, 'PELocnSts_PEPassExt': 3, 'PELocnSts_PEFrntExt': 4, 'PELocnSts_PERearExt': 5, 'PELocnSts_PEAllInt': 6, 'PELocnSts_Reserved': 7}
        compute_method = None
        length = 3
        startbit = 238
        byte = 29
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class DigKeyCnctInfo4KeyIdByte12:
        sig_name = "DigKeyCnctInfo4KeyIdByte12"
        sig_start_bit = 279
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
        startbit = 279
        byte = 34
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyCnctInfo4KeyConnectInfo:
        sig_name = "DigKeyCnctInfo4KeyConnectInfo"
        sig_start_bit = 144
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ConnectionSts_Disconnect': 0, 'ConnectionSts_Connect': 1}
        compute_method = None
        length = 1
        startbit = 144
        byte = 18
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class DigKeyCnctInfo3KeyIdByte13:
        sig_name = "DigKeyCnctInfo3KeyIdByte13"
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

    class DigKeyCnctInfo4AutoLockOnLeaveSetting:
        sig_name = "DigKeyCnctInfo4AutoLockOnLeaveSetting"
        sig_start_bit = 251
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AutoLockOnLeaveSetting_Unkown': 0, 'AutoLockOnLeaveSetting_Off': 1, 'AutoLockOnLeaveSetting_OnWithoutAnyDoorClose': 2, 'AutoLockOnLeaveSetting_OnWithDriverDoorClose': 3, 'AutoLockOnLeaveSetting_OnWithSideDoorClose': 4, 'AutoLockOnLeaveSetting_OnWithAllDoorClose': 5}
        compute_method = None
        length = 3
        startbit = 251
        byte = 31
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class DigKeyCnctInfo4KeyIdByte11:
        sig_name = "DigKeyCnctInfo4KeyIdByte11"
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


class CCUMCUCDInfoCANFDFr14:
    msg_name = "CCUMCUCDInfoCANFDFr14"
    msg_id = 512
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 32
    tx_node = "CCUMCUCD"
    rx_nodes = ['BNCM', 'WPC3', 'NKR', 'WPC2', 'DRF', 'CD']
    sig_group_dict = {'LoadPwrActSts': ['LoadPwrActStsACCMPwrActSts', 'LoadPwrActStsAFUPwrActSts', 'LoadPwrActStsAGMPwrActSts', 'LoadPwrActStsAGUPwrActSts', 'LoadPwrActStsALMLPwrActSts', 'LoadPwrActStsALMRPwrActSts', 'LoadPwrActStsAWMPwrActSts', 'LoadPwrActStsBCCPPwrActSts', 'LoadPwrActStsBCFVPwrActSts', 'LoadPwrActStsBCTVPwrActSts', 'LoadPwrActStsBEXVPwrActSts', 'LoadPwrActStsBNCMPwrActSts', 'LoadPwrActStsBoosterBlowerPwrActSts', 'LoadPwrActStsCCTVPwrActSts', 'LoadPwrActStsCDPwrActSts', 'LoadPwrActStsCERVPwrActSts', 'LoadPwrActStsCRCMPwrActSts', 'LoadPwrActStsCSOVPwrActSts', 'LoadPwrActStsDCTVPwrActSts', 'LoadPwrActStsDICPwrActSts', 'LoadPwrActStsDMFLPwrActSts', 'LoadPwrActStsDPODPwrActSts', 'LoadPwrActStsDRFPwrActSts', 'LoadPwrActStsDRMFRPwrActSts', 'LoadPwrActStsDRMRLPwrActSts', 'LoadPwrActStsDRMRRPwrActSts', 'LoadPwrActStsECTVPwrActSts', 'LoadPwrActStsEDCPPwrActSts', 'LoadPwrActStsEGSMPwrActSts', 'LoadPwrActStsEPMPwrActSts', 'LoadPwrActStsFCSIPwrActSts', 'LoadPwrActStsFEXVPwrActSts', 'LoadPwrActStsFLRPwrActSts', 'LoadPwrActStsFSRLPwrActSts', 'LoadPwrActStsFSRRPwrActSts', 'LoadPwrActStsHBMFPwrActSts', 'LoadPwrActStsHBMRPwrActSts', 'LoadPwrActStsHCCPPwrActSts', 'LoadPwrActStsHCMLPwrActSts', 'LoadPwrActStsHCMRPwrActSts', 'LoadPwrActStsHCTVPwrActSts', 'LoadPwrActStsHODPwrActSts', 'LoadPwrActStsHUBFPwrActSts', 'LoadPwrActStsHUBRPwrActSts', 'LoadPwrActStsHVAHPwrActSts', 'LoadPwrActStsHVCHPwrActSts', 'LoadPwrActStsHVCMPwrActSts', 'LoadPwrActStsIEMPwrActSts', 'LoadPwrActStsIRMMPwrActSts', 'LoadPwrActStsLCTVPwrActSts', 'LoadPwrActStsLPODPwrActSts', 'LoadPwrActStsMGMPwrActSts', 'LoadPwrActStsMMDPwrActSts', 'LoadPwrActStsMMPPwrActSts', 'LoadPwrActStsNKRPwrActSts', 'LoadPwrActStsOHCPwrActSts', 'LoadPwrActStsOPCFPwrActSts', 'LoadPwrActStsOPCRPwrActSts', 'LoadPwrActStsPMSIPwrActSts', 'LoadPwrActStsPOFPwrActSts', 'LoadPwrActStsPORPwrActSts', 'LoadPwrActStsPPODPwrActSts', 'LoadPwrActStsRCMLPwrActSts', 'LoadPwrActStsRCMRPwrActSts', 'LoadPwrActStsReserved1', 'LoadPwrActStsReserved10', 'LoadPwrActStsReserved11', 'LoadPwrActStsReserved12', 'LoadPwrActStsReserved13', 'LoadPwrActStsReserved14', 'LoadPwrActStsReserved15', 'LoadPwrActStsReserved16', 'LoadPwrActStsReserved17', 'LoadPwrActStsReserved18', 'LoadPwrActStsReserved2', 'LoadPwrActStsReserved3', 'LoadPwrActStsReserved4', 'LoadPwrActStsReserved5', 'LoadPwrActStsReserved6', 'LoadPwrActStsReserved7', 'LoadPwrActStsReserved8', 'LoadPwrActStsReserved9', 'LoadPwrActStsREXVPwrActSts', 'LoadPwrActStsRLMMPwrActSts', 'LoadPwrActStsRLSMPwrActSts', 'LoadPwrActStsRMLPwrActSts', 'LoadPwrActStsRPODPwrActSts', 'LoadPwrActStsRRMMPwrActSts', 'LoadPwrActStsRSOV1PwrActSts', 'LoadPwrActStsRSOV2PwrActSts', 'LoadPwrActStsSCMFPwrActSts', 'LoadPwrActStsSCMRPwrActSts', 'LoadPwrActStsSODLPwrActSts', 'LoadPwrActStsSODRPwrActSts', 'LoadPwrActStsSRSPwrActSts', 'LoadPwrActStsSWTLPwrActSts', 'LoadPwrActStsSWTRPwrActSts', 'LoadPwrActStsTERVPwrActSts', 'LoadPwrActStsUSBR1PwrActSts', 'LoadPwrActStsUSBR2PwrActSts', 'LoadPwrActStsUWBPwrActSts', 'LoadPwrActStsVCUPwrActSts', 'LoadPwrActStsWERVPwrActSts', 'LoadPwrActStsWPCPwrActSts']}
    sig_group_dataid_dict = {}

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


class WPC3ToCCUMCUCDInfoCANFDDiagRespFrame:
    msg_name = "WPC3ToCCUMCUCDInfoCANFDDiagRespFrame"
    msg_id = 1574
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "WPC3"
    rx_nodes = ['CCUMCUCD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class BNCMInfoCANFDFr02:
    msg_name = "BNCMInfoCANFDFr02"
    msg_id = 656
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 64
    tx_node = "BNCM"
    rx_nodes = ['CCUMCUCD', 'ETC']
    sig_group_dict = {'DigKeyCnctInfo2': ['DigKeyCnctInfo2AutoLockOnLeaveSetting', 'DigKeyCnctInfo2AutoUnlockOnApproachSetting', 'DigKeyCnctInfo2AutoZoneKeyPrsntSts', 'DigKeyCnctInfo2BattWarn', 'DigKeyCnctInfo2KeyConnectInfo', 'DigKeyCnctInfo2KeyIdByte0', 'DigKeyCnctInfo2KeyIdByte1', 'DigKeyCnctInfo2KeyIdByte10', 'DigKeyCnctInfo2KeyIdByte11', 'DigKeyCnctInfo2KeyIdByte12', 'DigKeyCnctInfo2KeyIdByte13', 'DigKeyCnctInfo2KeyIdByte14', 'DigKeyCnctInfo2KeyIdByte15', 'DigKeyCnctInfo2KeyIdByte2', 'DigKeyCnctInfo2KeyIdByte3', 'DigKeyCnctInfo2KeyIdByte4', 'DigKeyCnctInfo2KeyIdByte5', 'DigKeyCnctInfo2KeyIdByte6', 'DigKeyCnctInfo2KeyIdByte7', 'DigKeyCnctInfo2KeyIdByte8', 'DigKeyCnctInfo2KeyIdByte9', 'DigKeyCnctInfo2KeyTyp', 'DigKeyCnctInfo2PEKeyPrsntSts', 'DigKeyCnctInfo2PSEnaSts'], 'DigKeyCnctInfo1': ['DigKeyCnctInfo1AutoLockOnLeaveSetting', 'DigKeyCnctInfo1AutoUnlockOnApproachSetting', 'DigKeyCnctInfo1AutoZoneKeyPrsntSts', 'DigKeyCnctInfo1BattWarn', 'DigKeyCnctInfo1KeyConnectInfo', 'DigKeyCnctInfo1KeyIdByte0', 'DigKeyCnctInfo1KeyIdByte1', 'DigKeyCnctInfo1KeyIdByte10', 'DigKeyCnctInfo1KeyIdByte11', 'DigKeyCnctInfo1KeyIdByte12', 'DigKeyCnctInfo1KeyIdByte13', 'DigKeyCnctInfo1KeyIdByte14', 'DigKeyCnctInfo1KeyIdByte15', 'DigKeyCnctInfo1KeyIdByte2', 'DigKeyCnctInfo1KeyIdByte3', 'DigKeyCnctInfo1KeyIdByte4', 'DigKeyCnctInfo1KeyIdByte5', 'DigKeyCnctInfo1KeyIdByte6', 'DigKeyCnctInfo1KeyIdByte7', 'DigKeyCnctInfo1KeyIdByte8', 'DigKeyCnctInfo1KeyIdByte9', 'DigKeyCnctInfo1KeyTyp', 'DigKeyCnctInfo1PEKeyPrsntSts', 'DigKeyCnctInfo1PSEnaSts'], 'BLEKeyPrsntSts': ['BLEKeyPrsntStsApproachZoneKeyPrsntSts', 'BLEKeyPrsntStsConnectZoneKeyPrsntSts', 'BLEKeyPrsntStsDoorSideZoneKeyPrsntSts', 'BLEKeyPrsntStsPEExtZoneKeyPrsntSts', 'BLEKeyPrsntStsPEIntZoneKeyPrsntSts', 'BLEKeyPrsntStsPSZoneKeyPrsntSts', 'BLEKeyPrsntStsWalkAwayZoneKeyPrsntSts', 'BLEKeyPrsntStsWelcomeZoneKeyPrsntSts']}
    sig_group_dataid_dict = {}

    class DigKeyCnctInfo1KeyIdByte4:
        sig_name = "DigKeyCnctInfo1KeyIdByte4"
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

    class DigKeyCnctInfo2PSEnaSts:
        sig_name = "DigKeyCnctInfo2PSEnaSts"
        sig_start_bit = 217
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EnableDisable2_Disabled': 0, 'EnableDisable2_Enabled': 1}
        compute_method = None
        length = 1
        startbit = 217
        byte = 27
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class DigKeyCnctInfo2KeyIdByte3:
        sig_name = "DigKeyCnctInfo2KeyIdByte3"
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

    class DigKeyCnctInfo2KeyTyp:
        sig_name = "DigKeyCnctInfo2KeyTyp"
        sig_start_bit = 147
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 9
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeyTyp_NoKeyConnected': 0, 'KeyTyp_NFC_Card': 1, 'KeyTyp_BLE_UWB_KeyFob': 2, 'KeyTyp_Phone_NFC_Key': 3, 'KeyTyp_Phone_BLE_Key': 4, 'KeyTyp_Phone_UWB_Key': 5, 'KeyTyp_Reserved1': 6, 'KeyTyp_Reserved2': 7, 'KeyTyp_Reserved3': 8, 'KeyTyp_Reserved4': 9}
        compute_method = None
        length = 4
        startbit = 147
        byte = 18
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DigKeyCnctInfo2KeyIdByte1:
        sig_name = "DigKeyCnctInfo2KeyIdByte1"
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

    class DigKeyCnctInfo2KeyIdByte10:
        sig_name = "DigKeyCnctInfo2KeyIdByte10"
        sig_start_bit = 287
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
        startbit = 287
        byte = 35
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyCnctInfo2KeyIdByte7:
        sig_name = "DigKeyCnctInfo2KeyIdByte7"
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

    class DigKeyCnctInfo2KeyIdByte6:
        sig_name = "DigKeyCnctInfo2KeyIdByte6"
        sig_start_bit = 279
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
        startbit = 279
        byte = 34
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyCnctInfo2KeyIdByte0:
        sig_name = "DigKeyCnctInfo2KeyIdByte0"
        sig_start_bit = 191
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
        startbit = 191
        byte = 23
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyCnctInfo1AutoLockOnLeaveSetting:
        sig_name = "DigKeyCnctInfo1AutoLockOnLeaveSetting"
        sig_start_bit = 151
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AutoLockOnLeaveSetting_Unkown': 0, 'AutoLockOnLeaveSetting_Off': 1, 'AutoLockOnLeaveSetting_OnWithoutAnyDoorClose': 2, 'AutoLockOnLeaveSetting_OnWithDriverDoorClose': 3, 'AutoLockOnLeaveSetting_OnWithSideDoorClose': 4, 'AutoLockOnLeaveSetting_OnWithAllDoorClose': 5}
        compute_method = None
        length = 3
        startbit = 151
        byte = 18
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DigKeyCnctInfo2AutoZoneKeyPrsntSts:
        sig_name = "DigKeyCnctInfo2AutoZoneKeyPrsntSts"
        sig_start_bit = 236
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeyPrsntZoneInfo_NotConnected': 0, 'KeyPrsntZoneInfo_Connected': 1, 'KeyPrsntZoneInfo_Welcome': 2, 'KeyPrsntZoneInfo_WalkAway': 3, 'KeyPrsntZoneInfo_LockUnlockBuffer': 4, 'KeyPrsntZoneInfo_Approach': 5, 'KeyPrsntZoneInfo_Door': 6, 'KeyPrsntZoneInfo_InCar': 7, 'KeyPrsntZoneInfo_InFL': 8, 'KeyPrsntZoneInfo_InFR': 9, 'KeyPrsntZoneInfo_InRL': 10, 'KeyPrsntZoneInfo_InRR': 11, 'KeyPrsntZoneInfo_Tr': 12, 'KeyPrsntZoneInfo_Reserved1': 13, 'KeyPrsntZoneInfo_Reserved2': 14, 'KeyPrsntZoneInfo_Reserved3': 15}
        compute_method = None
        length = 4
        startbit = 236
        byte = 29
        mask = 0b00011110
        unmask = 0b11100001
        shift = 1

    class DigKeyCnctInfo1KeyIdByte15:
        sig_name = "DigKeyCnctInfo1KeyIdByte15"
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

    class BLEKeyPrsntStsApproachZoneKeyPrsntSts:
        sig_name = "BLEKeyPrsntStsApproachZoneKeyPrsntSts"
        sig_start_bit = 303
        update_id_bit = None
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
        startbit = 303
        byte = 37
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class DigKeyWakeUpZoneSts:
        sig_name = "DigKeyWakeUpZoneSts"
        sig_start_bit = 335
        update_id_bit = 331
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DigKeyWakeUpZone_Unkown': 0, 'DigKeyWakeUpZone_Connected': 1, 'DigKeyWakeUpZone_Welcome': 2, 'DigKeyWakeUpZone_WalkAway': 3, 'DigKeyWakeUpZone_PE': 4, 'DigKeyWakeUpZone_Reserved1': 5, 'DigKeyWakeUpZone_Reserved2': 6, 'DigKeyWakeUpZone_Reserved3': 7}
        compute_method = None
        length = 3
        startbit = 335
        byte = 41
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DigKeyCnctInfo1AutoUnlockOnApproachSetting:
        sig_name = "DigKeyCnctInfo1AutoUnlockOnApproachSetting"
        sig_start_bit = 4
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ApproachUnlockSetting_Unkown': 0, 'ApproachUnlockSetting_Off': 1, 'ApproachUnlockSetting_OnWithoutDoorOpen': 2, 'ApproachUnlockSetting_OnWithDoorMinAngleOpen': 3, 'ApproachUnlockSetting_OnWithDoorFullOpen': 4}
        compute_method = None
        length = 3
        startbit = 4
        byte = 0
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class DigKeyCnctInfo1KeyIdByte12:
        sig_name = "DigKeyCnctInfo1KeyIdByte12"
        sig_start_bit = 111
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
        startbit = 111
        byte = 13
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BLEKeyPrsntStsPEExtZoneKeyPrsntSts:
        sig_name = "BLEKeyPrsntStsPEExtZoneKeyPrsntSts"
        sig_start_bit = 300
        update_id_bit = None
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
        startbit = 300
        byte = 37
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class DigKeyCnctInfo1PSEnaSts:
        sig_name = "DigKeyCnctInfo1PSEnaSts"
        sig_start_bit = 148
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EnableDisable2_Disabled': 0, 'EnableDisable2_Enabled': 1}
        compute_method = None
        length = 1
        startbit = 148
        byte = 18
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class DigKeyCnctInfo1KeyIdByte13:
        sig_name = "DigKeyCnctInfo1KeyIdByte13"
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

    class DigKeyCnctInfo1KeyIdByte3:
        sig_name = "DigKeyCnctInfo1KeyIdByte3"
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

    class BLEKeyPrsntStsWalkAwayZoneKeyPrsntSts:
        sig_name = "BLEKeyPrsntStsWalkAwayZoneKeyPrsntSts"
        sig_start_bit = 297
        update_id_bit = None
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
        startbit = 297
        byte = 37
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class DigKeyCnctInfo1KeyIdByte9:
        sig_name = "DigKeyCnctInfo1KeyIdByte9"
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

    class DigKeyCnctInfo1AutoZoneKeyPrsntSts:
        sig_name = "DigKeyCnctInfo1AutoZoneKeyPrsntSts"
        sig_start_bit = 27
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeyPrsntZoneInfo_NotConnected': 0, 'KeyPrsntZoneInfo_Connected': 1, 'KeyPrsntZoneInfo_Welcome': 2, 'KeyPrsntZoneInfo_WalkAway': 3, 'KeyPrsntZoneInfo_LockUnlockBuffer': 4, 'KeyPrsntZoneInfo_Approach': 5, 'KeyPrsntZoneInfo_Door': 6, 'KeyPrsntZoneInfo_InCar': 7, 'KeyPrsntZoneInfo_InFL': 8, 'KeyPrsntZoneInfo_InFR': 9, 'KeyPrsntZoneInfo_InRL': 10, 'KeyPrsntZoneInfo_InRR': 11, 'KeyPrsntZoneInfo_Tr': 12, 'KeyPrsntZoneInfo_Reserved1': 13, 'KeyPrsntZoneInfo_Reserved2': 14, 'KeyPrsntZoneInfo_Reserved3': 15}
        compute_method = None
        length = 4
        startbit = 27
        byte = 3
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DigKeyCnctInfo2KeyIdByte9:
        sig_name = "DigKeyCnctInfo2KeyIdByte9"
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

    class DigKeyCnctInfo2AutoLockOnLeaveSetting:
        sig_name = "DigKeyCnctInfo2AutoLockOnLeaveSetting"
        sig_start_bit = 220
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AutoLockOnLeaveSetting_Unkown': 0, 'AutoLockOnLeaveSetting_Off': 1, 'AutoLockOnLeaveSetting_OnWithoutAnyDoorClose': 2, 'AutoLockOnLeaveSetting_OnWithDriverDoorClose': 3, 'AutoLockOnLeaveSetting_OnWithSideDoorClose': 4, 'AutoLockOnLeaveSetting_OnWithAllDoorClose': 5}
        compute_method = None
        length = 3
        startbit = 220
        byte = 27
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class DigKeyCnctInfo2KeyIdByte5:
        sig_name = "DigKeyCnctInfo2KeyIdByte5"
        sig_start_bit = 199
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
        startbit = 199
        byte = 24
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyCnctInfo1KeyIdByte7:
        sig_name = "DigKeyCnctInfo1KeyIdByte7"
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

    class DigKeyCnctInfo2KeyIdByte8:
        sig_name = "DigKeyCnctInfo2KeyIdByte8"
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

    class DigKeyCnctInfo2_UB:
        sig_name = "DigKeyCnctInfo2_UB"
        sig_start_bit = 305
        update_id_bit = 305
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
        startbit = 305
        byte = 38
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class DigKeyCnctInfo2KeyIdByte14:
        sig_name = "DigKeyCnctInfo2KeyIdByte14"
        sig_start_bit = 271
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
        startbit = 271
        byte = 33
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyMaxWakeUpTimeSts:
        sig_name = "DigKeyMaxWakeUpTimeSts"
        sig_start_bit = 327
        update_id_bit = 332
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 4
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 327
        byte = 40
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyCnctInfo2KeyConnectInfo:
        sig_name = "DigKeyCnctInfo2KeyConnectInfo"
        sig_start_bit = 232
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ConnectionSts_Disconnect': 0, 'ConnectionSts_Connect': 1}
        compute_method = None
        length = 1
        startbit = 232
        byte = 29
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class BLEKeyPrsntStsDoorSideZoneKeyPrsntSts:
        sig_name = "BLEKeyPrsntStsDoorSideZoneKeyPrsntSts"
        sig_start_bit = 301
        update_id_bit = None
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
        startbit = 301
        byte = 37
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class DigKeyCnctInfo2KeyIdByte2:
        sig_name = "DigKeyCnctInfo2KeyIdByte2"
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

    class DigKeyCnctInfo1KeyIdByte1:
        sig_name = "DigKeyCnctInfo1KeyIdByte1"
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

    class DigKeyCnctInfo2PEKeyPrsntSts:
        sig_name = "DigKeyCnctInfo2PEKeyPrsntSts"
        sig_start_bit = 239
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PELocnSts_Idle': 0, 'PELocnSts_PEAllExt': 1, 'PELocnSts_PEDrvrExt': 2, 'PELocnSts_PEPassExt': 3, 'PELocnSts_PEFrntExt': 4, 'PELocnSts_PERearExt': 5, 'PELocnSts_PEAllInt': 6, 'PELocnSts_Reserved': 7}
        compute_method = None
        length = 3
        startbit = 239
        byte = 29
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DigKeyCnctInfo1KeyConnectInfo:
        sig_name = "DigKeyCnctInfo1KeyConnectInfo"
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
        sig_value_table = {'ConnectionSts_Disconnect': 0, 'ConnectionSts_Connect': 1}
        compute_method = None
        length = 1
        startbit = 0
        byte = 0
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class DigKeyCnctInfo1_UB:
        sig_name = "DigKeyCnctInfo1_UB"
        sig_start_bit = 306
        update_id_bit = 306
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
        startbit = 306
        byte = 38
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class ActualWakeUpTimeSts:
        sig_name = "ActualWakeUpTimeSts"
        sig_start_bit = 319
        update_id_bit = 304
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
        startbit = 319
        byte = 39
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyCnctInfo2KeyIdByte4:
        sig_name = "DigKeyCnctInfo2KeyIdByte4"
        sig_start_bit = 263
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
        startbit = 263
        byte = 32
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyCnctInfo1BattWarn:
        sig_name = "DigKeyCnctInfo1BattWarn"
        sig_start_bit = 1
        update_id_bit = None
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
        startbit = 1
        byte = 0
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class DigKeyCnctInfo2KeyIdByte12:
        sig_name = "DigKeyCnctInfo2KeyIdByte12"
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

    class DigKeyCnctInfo1KeyIdByte10:
        sig_name = "DigKeyCnctInfo1KeyIdByte10"
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

    class BLEKeyPrsntStsWelcomeZoneKeyPrsntSts:
        sig_name = "BLEKeyPrsntStsWelcomeZoneKeyPrsntSts"
        sig_start_bit = 296
        update_id_bit = None
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
        startbit = 296
        byte = 37
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class DigKeyCnctInfo1KeyIdByte2:
        sig_name = "DigKeyCnctInfo1KeyIdByte2"
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

    class BLEKeyPrsntStsPEIntZoneKeyPrsntSts:
        sig_name = "BLEKeyPrsntStsPEIntZoneKeyPrsntSts"
        sig_start_bit = 299
        update_id_bit = None
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
        startbit = 299
        byte = 37
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class BLEKeyPrsntSts_UB:
        sig_name = "BLEKeyPrsntSts_UB"
        sig_start_bit = 308
        update_id_bit = 308
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
        startbit = 308
        byte = 38
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class DigKeyCnctInfo1PEKeyPrsntSts:
        sig_name = "DigKeyCnctInfo1PEKeyPrsntSts"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PELocnSts_Idle': 0, 'PELocnSts_PEAllExt': 1, 'PELocnSts_PEDrvrExt': 2, 'PELocnSts_PEPassExt': 3, 'PELocnSts_PEFrntExt': 4, 'PELocnSts_PERearExt': 5, 'PELocnSts_PEAllInt': 6, 'PELocnSts_Reserved': 7}
        compute_method = None
        length = 3
        startbit = 7
        byte = 0
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class BLEWorkSts:
        sig_name = "BLEWorkSts"
        sig_start_bit = 311
        update_id_bit = 307
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BLEWorkSts_Unkown': 0, 'BLEWorkSts_BroadcastOnly': 1, 'BLEWorkSts_BroadcastAndScan': 2, 'BLEWorkSts_ScanOnly': 3, 'BLEWorkSts_Error': 4, 'BLEWorkSts_Reserved1': 5, 'BLEWorkSts_Reserved2': 6, 'BLEWorkSts_Reserved3': 7}
        compute_method = None
        length = 3
        startbit = 311
        byte = 38
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DigKeyCnctInfo1KeyTyp:
        sig_name = "DigKeyCnctInfo1KeyTyp"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 9
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeyTyp_NoKeyConnected': 0, 'KeyTyp_NFC_Card': 1, 'KeyTyp_BLE_UWB_KeyFob': 2, 'KeyTyp_Phone_NFC_Key': 3, 'KeyTyp_Phone_BLE_Key': 4, 'KeyTyp_Phone_UWB_Key': 5, 'KeyTyp_Reserved1': 6, 'KeyTyp_Reserved2': 7, 'KeyTyp_Reserved3': 8, 'KeyTyp_Reserved4': 9}
        compute_method = None
        length = 4
        startbit = 31
        byte = 3
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DigKeyCnctInfo2KeyIdByte13:
        sig_name = "DigKeyCnctInfo2KeyIdByte13"
        sig_start_bit = 247
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
        startbit = 247
        byte = 30
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyCnctInfo2KeyIdByte15:
        sig_name = "DigKeyCnctInfo2KeyIdByte15"
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

    class DigKeyCnctInfo1KeyIdByte6:
        sig_name = "DigKeyCnctInfo1KeyIdByte6"
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

    class DigKeyCnctInfo1KeyIdByte5:
        sig_name = "DigKeyCnctInfo1KeyIdByte5"
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

    class DigKeyCnctInfo2AutoUnlockOnApproachSetting:
        sig_name = "DigKeyCnctInfo2AutoUnlockOnApproachSetting"
        sig_start_bit = 223
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ApproachUnlockSetting_Unkown': 0, 'ApproachUnlockSetting_Off': 1, 'ApproachUnlockSetting_OnWithoutDoorOpen': 2, 'ApproachUnlockSetting_OnWithDoorMinAngleOpen': 3, 'ApproachUnlockSetting_OnWithDoorFullOpen': 4}
        compute_method = None
        length = 3
        startbit = 223
        byte = 27
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DigKeyCnctInfo2BattWarn:
        sig_name = "DigKeyCnctInfo2BattWarn"
        sig_start_bit = 216
        update_id_bit = None
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
        startbit = 216
        byte = 27
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class DigKeyCnctInfo1KeyIdByte14:
        sig_name = "DigKeyCnctInfo1KeyIdByte14"
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

    class DigKeyCnctInfo1KeyIdByte8:
        sig_name = "DigKeyCnctInfo1KeyIdByte8"
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

    class DigKeyCnctInfo1KeyIdByte11:
        sig_name = "DigKeyCnctInfo1KeyIdByte11"
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

    class DigKeyCnctInfo2KeyIdByte11:
        sig_name = "DigKeyCnctInfo2KeyIdByte11"
        sig_start_bit = 295
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
        startbit = 295
        byte = 36
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BLEKeyPrsntStsPSZoneKeyPrsntSts:
        sig_name = "BLEKeyPrsntStsPSZoneKeyPrsntSts"
        sig_start_bit = 298
        update_id_bit = None
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
        startbit = 298
        byte = 37
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class DigKeyCnctInfo1KeyIdByte0:
        sig_name = "DigKeyCnctInfo1KeyIdByte0"
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

    class BLEKeyPrsntStsConnectZoneKeyPrsntSts:
        sig_name = "BLEKeyPrsntStsConnectZoneKeyPrsntSts"
        sig_start_bit = 302
        update_id_bit = None
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
        startbit = 302
        byte = 37
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6


class BNCMtoCCUMCUCDDigKeyRKEReqInfoCANFDFrame:
    msg_name = "BNCMtoCCUMCUCDDigKeyRKEReqInfoCANFDFrame"
    msg_id = 770
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "BNCM"
    rx_nodes = ['CCUMCUCD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class NKRtoBNCMNFCKeyReqOutdInfoCANFDFrame:
    msg_name = "NKRtoBNCMNFCKeyReqOutdInfoCANFDFrame"
    msg_id = 774
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "NKR"
    rx_nodes = ['BNCM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class BNCMInfoCANFDFr07:
    msg_name = "BNCMInfoCANFDFr07"
    msg_id = 524
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 64
    tx_node = "BNCM"
    rx_nodes = ['ETC']
    sig_group_dict = {'DigKeyLocData2': ['DigKeyLocData2CalibrationDataByte0', 'DigKeyLocData2CalibrationDataByte1', 'DigKeyLocData2CalibrationDataByte10', 'DigKeyLocData2CalibrationDataByte11', 'DigKeyLocData2CalibrationDataByte12', 'DigKeyLocData2CalibrationDataByte13', 'DigKeyLocData2CalibrationDataByte14', 'DigKeyLocData2CalibrationDataByte15', 'DigKeyLocData2CalibrationDataByte16', 'DigKeyLocData2CalibrationDataByte17', 'DigKeyLocData2CalibrationDataByte18', 'DigKeyLocData2CalibrationDataByte19', 'DigKeyLocData2CalibrationDataByte2', 'DigKeyLocData2CalibrationDataByte3', 'DigKeyLocData2CalibrationDataByte4', 'DigKeyLocData2CalibrationDataByte5', 'DigKeyLocData2CalibrationDataByte6', 'DigKeyLocData2CalibrationDataByte7', 'DigKeyLocData2CalibrationDataByte8', 'DigKeyLocData2CalibrationDataByte9', 'DigKeyLocData2FrntLeBLERSSI', 'DigKeyLocData2FrntLeUWBDistance', 'DigKeyLocData2FrntRiBLERSSI', 'DigKeyLocData2FrntRiUWBDistance', 'DigKeyLocData2InVehReBLERSSI', 'DigKeyLocData2InVehReUWBDistance', 'DigKeyLocData2KeyIdByte0', 'DigKeyLocData2KeyIdByte1', 'DigKeyLocData2KeyIdByte10', 'DigKeyLocData2KeyIdByte11', 'DigKeyLocData2KeyIdByte12', 'DigKeyLocData2KeyIdByte13', 'DigKeyLocData2KeyIdByte14', 'DigKeyLocData2KeyIdByte15', 'DigKeyLocData2KeyIdByte2', 'DigKeyLocData2KeyIdByte3', 'DigKeyLocData2KeyIdByte4', 'DigKeyLocData2KeyIdByte5', 'DigKeyLocData2KeyIdByte6', 'DigKeyLocData2KeyIdByte7', 'DigKeyLocData2KeyIdByte8', 'DigKeyLocData2KeyIdByte9', 'DigKeyLocData2MainBLERSSI', 'DigKeyLocData2MainUWBDistance', 'DigKeyLocData2ReLeBLERSSI', 'DigKeyLocData2ReLeUWBDistance', 'DigKeyLocData2ReRiBLERSSI', 'DigKeyLocData2ReRiUWBDistance']}
    sig_group_dataid_dict = {}

    class DigKeyLocData2CalibrationDataByte8:
        sig_name = "DigKeyLocData2CalibrationDataByte8"
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

    class DigKeyLocData2CalibrationDataByte11:
        sig_name = "DigKeyLocData2CalibrationDataByte11"
        sig_start_bit = 239
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
        startbit = 239
        byte = 29
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData2CalibrationDataByte15:
        sig_name = "DigKeyLocData2CalibrationDataByte15"
        sig_start_bit = 271
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
        startbit = 271
        byte = 33
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData2KeyIdByte1:
        sig_name = "DigKeyLocData2KeyIdByte1"
        sig_start_bit = 319
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
        startbit = 319
        byte = 39
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData2KeyIdByte13:
        sig_name = "DigKeyLocData2KeyIdByte13"
        sig_start_bit = 415
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
        startbit = 415
        byte = 51
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData2KeyIdByte15:
        sig_name = "DigKeyLocData2KeyIdByte15"
        sig_start_bit = 431
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
        startbit = 431
        byte = 53
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData2MainBLERSSI:
        sig_name = "DigKeyLocData2MainBLERSSI"
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

    class DigKeyLocData2CalibrationDataByte7:
        sig_name = "DigKeyLocData2CalibrationDataByte7"
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

    class DigKeyLocData2CalibrationDataByte17:
        sig_name = "DigKeyLocData2CalibrationDataByte17"
        sig_start_bit = 287
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
        startbit = 287
        byte = 35
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData2KeyIdByte0:
        sig_name = "DigKeyLocData2KeyIdByte0"
        sig_start_bit = 311
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
        startbit = 311
        byte = 38
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData2KeyIdByte3:
        sig_name = "DigKeyLocData2KeyIdByte3"
        sig_start_bit = 335
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
        startbit = 335
        byte = 41
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData2KeyIdByte4:
        sig_name = "DigKeyLocData2KeyIdByte4"
        sig_start_bit = 343
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
        startbit = 343
        byte = 42
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData2CalibrationDataByte10:
        sig_name = "DigKeyLocData2CalibrationDataByte10"
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

    class DigKeyLocData2FrntRiUWBDistance:
        sig_name = "DigKeyLocData2FrntRiUWBDistance"
        sig_start_bit = 111
        update_id_bit = None
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 65535
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 111
        bmuws_info = [(13, 0b11111111, 0b00000000, 8, 0), (14, 0b11111111, 0b00000000, 8, 0)]

    class DigKeyLocData2FrntRiBLERSSI:
        sig_name = "DigKeyLocData2FrntRiBLERSSI"
        sig_start_bit = 103
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
        startbit = 103
        byte = 12
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData2FrntLeBLERSSI:
        sig_name = "DigKeyLocData2FrntLeBLERSSI"
        sig_start_bit = 79
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
        startbit = 79
        byte = 9
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData2KeyIdByte2:
        sig_name = "DigKeyLocData2KeyIdByte2"
        sig_start_bit = 327
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
        startbit = 327
        byte = 40
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData2KeyIdByte8:
        sig_name = "DigKeyLocData2KeyIdByte8"
        sig_start_bit = 375
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
        startbit = 375
        byte = 46
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData2CalibrationDataByte16:
        sig_name = "DigKeyLocData2CalibrationDataByte16"
        sig_start_bit = 279
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
        startbit = 279
        byte = 34
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData2KeyIdByte6:
        sig_name = "DigKeyLocData2KeyIdByte6"
        sig_start_bit = 359
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
        startbit = 359
        byte = 44
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData2FrntLeUWBDistance:
        sig_name = "DigKeyLocData2FrntLeUWBDistance"
        sig_start_bit = 87
        update_id_bit = None
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 65535
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 87
        bmuws_info = [(10, 0b11111111, 0b00000000, 8, 0), (11, 0b11111111, 0b00000000, 8, 0)]

    class DigKeyLocData2ReLeUWBDistance:
        sig_name = "DigKeyLocData2ReLeUWBDistance"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 65535
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class DigKeyLocData2InVehReBLERSSI:
        sig_name = "DigKeyLocData2InVehReBLERSSI"
        sig_start_bit = 127
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
        startbit = 127
        byte = 15
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData2CalibrationDataByte18:
        sig_name = "DigKeyLocData2CalibrationDataByte18"
        sig_start_bit = 295
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
        startbit = 295
        byte = 36
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData2CalibrationDataByte6:
        sig_name = "DigKeyLocData2CalibrationDataByte6"
        sig_start_bit = 199
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
        startbit = 199
        byte = 24
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData2ReRiBLERSSI:
        sig_name = "DigKeyLocData2ReRiBLERSSI"
        sig_start_bit = 55
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
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData2KeyIdByte7:
        sig_name = "DigKeyLocData2KeyIdByte7"
        sig_start_bit = 367
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
        startbit = 367
        byte = 45
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData2CalibrationDataByte19:
        sig_name = "DigKeyLocData2CalibrationDataByte19"
        sig_start_bit = 303
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
        startbit = 303
        byte = 37
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData2ReLeBLERSSI:
        sig_name = "DigKeyLocData2ReLeBLERSSI"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData2ReRiUWBDistance:
        sig_name = "DigKeyLocData2ReRiUWBDistance"
        sig_start_bit = 63
        update_id_bit = None
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 65535
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 63
        bmuws_info = [(7, 0b11111111, 0b00000000, 8, 0), (8, 0b11111111, 0b00000000, 8, 0)]

    class DigKeyLocData2CalibrationDataByte9:
        sig_name = "DigKeyLocData2CalibrationDataByte9"
        sig_start_bit = 223
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
        startbit = 223
        byte = 27
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData2CalibrationDataByte2:
        sig_name = "DigKeyLocData2CalibrationDataByte2"
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

    class DigKeyLocData2CalibrationDataByte13:
        sig_name = "DigKeyLocData2CalibrationDataByte13"
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

    class DigKeyLocData2InVehReUWBDistance:
        sig_name = "DigKeyLocData2InVehReUWBDistance"
        sig_start_bit = 135
        update_id_bit = None
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 65535
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 135
        bmuws_info = [(16, 0b11111111, 0b00000000, 8, 0), (17, 0b11111111, 0b00000000, 8, 0)]

    class DigKeyLocData2KeyIdByte10:
        sig_name = "DigKeyLocData2KeyIdByte10"
        sig_start_bit = 391
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
        startbit = 391
        byte = 48
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData2CalibrationDataByte4:
        sig_name = "DigKeyLocData2CalibrationDataByte4"
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

    class DigKeyLocData2KeyIdByte11:
        sig_name = "DigKeyLocData2KeyIdByte11"
        sig_start_bit = 399
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
        startbit = 399
        byte = 49
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData2KeyIdByte14:
        sig_name = "DigKeyLocData2KeyIdByte14"
        sig_start_bit = 423
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
        startbit = 423
        byte = 52
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData2CalibrationDataByte1:
        sig_name = "DigKeyLocData2CalibrationDataByte1"
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

    class DigKeyLocData2MainUWBDistance:
        sig_name = "DigKeyLocData2MainUWBDistance"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 65535
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 15
        bmuws_info = [(1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DigKeyLocData2CalibrationDataByte14:
        sig_name = "DigKeyLocData2CalibrationDataByte14"
        sig_start_bit = 263
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
        startbit = 263
        byte = 32
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData2CalibrationDataByte3:
        sig_name = "DigKeyLocData2CalibrationDataByte3"
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

    class DigKeyLocData2CalibrationDataByte5:
        sig_name = "DigKeyLocData2CalibrationDataByte5"
        sig_start_bit = 191
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
        startbit = 191
        byte = 23
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData2CalibrationDataByte12:
        sig_name = "DigKeyLocData2CalibrationDataByte12"
        sig_start_bit = 247
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
        startbit = 247
        byte = 30
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData2KeyIdByte5:
        sig_name = "DigKeyLocData2KeyIdByte5"
        sig_start_bit = 351
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
        startbit = 351
        byte = 43
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData2CalibrationDataByte0:
        sig_name = "DigKeyLocData2CalibrationDataByte0"
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

    class DigKeyLocData2KeyIdByte12:
        sig_name = "DigKeyLocData2KeyIdByte12"
        sig_start_bit = 407
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
        startbit = 407
        byte = 50
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData2KeyIdByte9:
        sig_name = "DigKeyLocData2KeyIdByte9"
        sig_start_bit = 383
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
        startbit = 383
        byte = 47
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class BNCMInfoCANFDNmFr:
    msg_name = "BNCMInfoCANFDNmFr"
    msg_id = 1282
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BNCM"
    rx_nodes = ['WPC3']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class BNCMInfoCANFDFr01:
    msg_name = "BNCMInfoCANFDFr01"
    msg_id = 400
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 64
    tx_node = "BNCM"
    rx_nodes = ['CCUMCUCD', 'WPC2', 'ETC']
    sig_group_dict = {'BLEMgrFctRdySts': ['BLEMgrFctRdyStsFctRdySts', 'BLEMgrFctRdyStsRnd'], 'KeyFindResp': ['KeyFindRespKeyFindSts', 'KeyFindRespKeyIdByte0', 'KeyFindRespKeyIdByte1', 'KeyFindRespKeyIdByte10', 'KeyFindRespKeyIdByte11', 'KeyFindRespKeyIdByte12', 'KeyFindRespKeyIdByte13', 'KeyFindRespKeyIdByte14', 'KeyFindRespKeyIdByte15', 'KeyFindRespKeyIdByte2', 'KeyFindRespKeyIdByte3', 'KeyFindRespKeyIdByte4', 'KeyFindRespKeyIdByte5', 'KeyFindRespKeyIdByte6', 'KeyFindRespKeyIdByte7', 'KeyFindRespKeyIdByte8', 'KeyFindRespKeyIdByte9', 'KeyFindRespKeyLocnSts', 'KeyFindRespKeyTyp', 'KeyFindRespMAC', 'KeyFindRespRnd']}
    sig_group_dataid_dict = {}

    class KeyFindRespKeyIdByte2:
        sig_name = "KeyFindRespKeyIdByte2"
        sig_start_bit = 263
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
        startbit = 263
        byte = 32
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class KeyFindRespKeyFindSts:
        sig_name = "KeyFindRespKeyFindSts"
        sig_start_bit = 279
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeyPrsntSts_Idle': 0, 'KeyPrsntSts_InProgs': 1, 'KeyPrsntSts_NotPrsnt': 2, 'KeyPrsntSts_Prsnt': 3}
        compute_method = None
        length = 2
        startbit = 279
        byte = 34
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class BLEMgrFctRdySts_UB:
        sig_name = "BLEMgrFctRdySts_UB"
        sig_start_bit = 34
        update_id_bit = 34
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
        startbit = 34
        byte = 4
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class KeyFindResp_UB:
        sig_name = "KeyFindResp_UB"
        sig_start_bit = 276
        update_id_bit = 276
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
        startbit = 276
        byte = 34
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class BNCMNetworkReq:
        sig_name = "BNCMNetworkReq"
        sig_start_bit = 38
        update_id_bit = 33
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
        startbit = 38
        byte = 4
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class KeyFindRespKeyIdByte10:
        sig_name = "KeyFindRespKeyIdByte10"
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

    class BLEMgrFctRdyStsRnd:
        sig_name = "BLEMgrFctRdyStsRnd"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 32
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 32
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class KeyFindRespKeyIdByte0:
        sig_name = "KeyFindRespKeyIdByte0"
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

    class NFCLinkCtrl:
        sig_name = "NFCLinkCtrl"
        sig_start_bit = 36
        update_id_bit = 277
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NFCLinkCtrl_Invalid': 0, 'NFCLinkCtrl_NFCLinkSetup': 1, 'NFCLinkCtrl_NFCLinkTeardownAndReset': 2}
        compute_method = None
        length = 2
        startbit = 36
        byte = 4
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class KeyFindRespKeyIdByte12:
        sig_name = "KeyFindRespKeyIdByte12"
        sig_start_bit = 223
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
        startbit = 223
        byte = 27
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class KeyFindRespMAC:
        sig_name = "KeyFindRespMAC"
        sig_start_bit = 71
        update_id_bit = None
        sig_length = 64
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 64
        startbit = 71
        bmuws_info = [(8, 0b11111111, 0b00000000, 8, 0), (9, 0b11111111, 0b00000000, 8, 0), (10, 0b11111111, 0b00000000, 8, 0), (11, 0b11111111, 0b00000000, 8, 0), (12, 0b11111111, 0b00000000, 8, 0), (13, 0b11111111, 0b00000000, 8, 0), (14, 0b11111111, 0b00000000, 8, 0), (15, 0b11111111, 0b00000000, 8, 0)]

    class KeyFindRespKeyIdByte9:
        sig_name = "KeyFindRespKeyIdByte9"
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

    class KeyFindRespKeyIdByte6:
        sig_name = "KeyFindRespKeyIdByte6"
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

    class KeyFindRespKeyIdByte3:
        sig_name = "KeyFindRespKeyIdByte3"
        sig_start_bit = 199
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
        startbit = 199
        byte = 24
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyAprchEve:
        sig_name = "DigKeyAprchEve"
        sig_start_bit = 37
        update_id_bit = 32
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
        startbit = 37
        byte = 4
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class KeyFindRespKeyIdByte13:
        sig_name = "KeyFindRespKeyIdByte13"
        sig_start_bit = 239
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
        startbit = 239
        byte = 29
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class KeyFindRespKeyIdByte15:
        sig_name = "KeyFindRespKeyIdByte15"
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

    class BLEMgrFctRdyStsFctRdySts:
        sig_name = "BLEMgrFctRdyStsFctRdySts"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 39
        byte = 4
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class KeyFindRespKeyIdByte7:
        sig_name = "KeyFindRespKeyIdByte7"
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

    class KeyFindRespKeyTyp:
        sig_name = "KeyFindRespKeyTyp"
        sig_start_bit = 55
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 9
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeyTyp_NoKeyConnected': 0, 'KeyTyp_NFC_Card': 1, 'KeyTyp_BLE_UWB_KeyFob': 2, 'KeyTyp_Phone_NFC_Key': 3, 'KeyTyp_Phone_BLE_Key': 4, 'KeyTyp_Phone_UWB_Key': 5, 'KeyTyp_Reserved1': 6, 'KeyTyp_Reserved2': 7, 'KeyTyp_Reserved3': 8, 'KeyTyp_Reserved4': 9}
        compute_method = None
        length = 4
        startbit = 55
        byte = 6
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class KeyFindRespKeyIdByte1:
        sig_name = "KeyFindRespKeyIdByte1"
        sig_start_bit = 247
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
        startbit = 247
        byte = 30
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class KeyFindRespKeyIdByte8:
        sig_name = "KeyFindRespKeyIdByte8"
        sig_start_bit = 271
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
        startbit = 271
        byte = 33
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class KeyFindRespKeyLocnSts:
        sig_name = "KeyFindRespKeyLocnSts"
        sig_start_bit = 51
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeyLocnReq_Idle': 0, 'KeyLocnReq_PEAllExtAndInt': 1, 'KeyLocnReq_PEAllExt': 2, 'KeyLocnReq_PEDrvrExt': 3, 'KeyLocnReq_PEPassExt': 4, 'KeyLocnReq_PEFrntExt': 5, 'KeyLocnReq_PERearExt': 6, 'KeyLocnReq_PEAllInt': 7, 'KeyLocnReq_PSAllInt': 8, 'KeyLocnReq_Reserved1': 9, 'KeyLocnReq_Reserved2': 10}
        compute_method = None
        length = 4
        startbit = 51
        byte = 6
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class KeyFindRespKeyIdByte5:
        sig_name = "KeyFindRespKeyIdByte5"
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

    class KeyFindRespKeyIdByte4:
        sig_name = "KeyFindRespKeyIdByte4"
        sig_start_bit = 191
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
        startbit = 191
        byte = 23
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class KeyFindRespKeyIdByte14:
        sig_name = "KeyFindRespKeyIdByte14"
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

    class KeyFindRespRnd:
        sig_name = "KeyFindRespRnd"
        sig_start_bit = 159
        update_id_bit = None
        sig_length = 32
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 32
        startbit = 159
        bmuws_info = [(19, 0b11111111, 0b00000000, 8, 0), (20, 0b11111111, 0b00000000, 8, 0), (21, 0b11111111, 0b00000000, 8, 0), (22, 0b11111111, 0b00000000, 8, 0)]

    class KeyFindRespKeyIdByte11:
        sig_name = "KeyFindRespKeyIdByte11"
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


class CDInfoCANFDFr01:
    msg_name = "CDInfoCANFDFr01"
    msg_id = 145
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 16
    tx_node = "CD"
    rx_nodes = ['CCUMCUCD']
    sig_group_dict = {'DimSts': ['DimStsChks', 'DimStsCntr', 'DimStsSts'], 'ScreenICSts': ['ScreenICStsChks', 'ScreenICStsCntr', 'ScreenICStsSts'], 'ScreenTchIC': ['ScreenTchICChks', 'ScreenTchICCntr', 'ScreenTchICSts']}
    sig_group_dataid_dict = {'DimSts': 1061, 'ScreenICSts': 1060}

    class ScreenTchICChks:
        sig_name = "ScreenTchICChks"
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

    class ScreenICStsSts:
        sig_name = "ScreenICStsSts"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DimStsCntr:
        sig_name = "DimStsCntr"
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

    class ScreenTchICCntr:
        sig_name = "ScreenTchICCntr"
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

    class DimSts_UB:
        sig_name = "DimSts_UB"
        sig_start_bit = 53
        update_id_bit = 53
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
        startbit = 53
        byte = 6
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class ScreenICSts_UB:
        sig_name = "ScreenICSts_UB"
        sig_start_bit = 51
        update_id_bit = 51
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
        startbit = 51
        byte = 6
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class ScreenTchIC_UB:
        sig_name = "ScreenTchIC_UB"
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

    class ScreenICStsCntr:
        sig_name = "ScreenICStsCntr"
        sig_start_bit = 41
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
        startbit = 41
        bmuws_info = [(5, 0b00000011, 0b11111100, 2, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class ScreenICStsChks:
        sig_name = "ScreenICStsChks"
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

    class ScreenTchICSts:
        sig_name = "ScreenTchICSts"
        sig_start_bit = 9
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
        startbit = 9
        bmuws_info = [(1, 0b00000011, 0b11111100, 2, 0), (2, 0b11110000, 0b00001111, 4, 4)]

    class DimStsSts:
        sig_name = "DimStsSts"
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
        sig_value_table = {'DimmingSts_Off': 0, 'DimmingSts_Ready': 1, 'DimmingSts_Fault': 2, 'DimmingSts_Reserve': 3}
        compute_method = None
        length = 2
        startbit = 11
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class DimStsChks:
        sig_name = "DimStsChks"
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


class BNCMInfoCANFDFr05:
    msg_name = "BNCMInfoCANFDFr05"
    msg_id = 16
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BNCM"
    rx_nodes = ['CCUMCUCD', 'ETC']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class BLEDCChrgLidReq:
        sig_name = "BLEDCChrgLidReq"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OpenClsCtrlReq_Idle': 0, 'OpenClsCtrlReq_Open': 1, 'OpenClsCtrlReq_Close': 2}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class CDInfoCANFDFr02:
    msg_name = "CDInfoCANFDFr02"
    msg_id = 660
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 16
    tx_node = "CD"
    rx_nodes = ['CCUMCUCD']
    sig_group_dict = {'BackLight': ['BackLightChks', 'BackLightCntr', 'BackLightSts']}
    sig_group_dataid_dict = {}

    class BrightnessLvlSts:
        sig_name = "BrightnessLvlSts"
        sig_start_bit = 23
        update_id_bit = 8
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "SCALE_LINEAR_AND_TEXTTABLE"
        sig_value_table = {'BattSOH_Invalid': 255}
        compute_method = None
        length = 8
        startbit = 23
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntScrnWorkSts:
        sig_name = "FrntScrnWorkSts"
        sig_start_bit = 55
        update_id_bit = 32
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FrntScrnWorkSts_Unknow': 0, 'FrntScrnWorkSts_Start_up': 1, 'FrntScrnWorkSts_Shut_down': 2, 'FrntScrnWorkSts_Work_On': 3, 'FrntScrnWorkSts_Reserve1': 4, 'FrntScrnWorkSts_Reserve2': 5, 'FrntScrnWorkSts_Reserve3': 6, 'FrntScrnWorkSts_Reserve4': 7}
        compute_method = None
        length = 3
        startbit = 55
        byte = 6
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class BackLightSts:
        sig_name = "BackLightSts"
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
        sig_value_table = {'BackLightSts_Off': 0, 'BackLightSts_Ready': 1, 'BackLightSts_Fault': 2, 'BackLightSts_Reserved1': 3}
        compute_method = None
        length = 2
        startbit = 15
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class SrceenTouchSts:
        sig_name = "SrceenTouchSts"
        sig_start_bit = 36
        update_id_bit = 33
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OkNotOk1_Ok': 0, 'OkNotOk1_NotOk': 1}
        compute_method = None
        length = 1
        startbit = 36
        byte = 4
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class GearDispFedBck:
        sig_name = "GearDispFedBck"
        sig_start_bit = 52
        update_id_bit = 49
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GearFltSts_Normal': 0, 'GearFltSts_PFlt': 1, 'GearFltSts_RFlt': 2, 'GearFltSts_NFlt': 3, 'GearFltSts_DFlt': 4, 'GearFltSts_SrvReq': 5, 'GearFltSts_Reserved1': 6, 'GearFltSts_Reserved2': 7}
        compute_method = None
        length = 3
        startbit = 52
        byte = 6
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class BackLightCntr:
        sig_name = "BackLightCntr"
        sig_start_bit = 13
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
        startbit = 13
        byte = 1
        mask = 0b00111100
        unmask = 0b11000011
        shift = 2

    class BackLightChks:
        sig_name = "BackLightChks"
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

    class BackLight_UB:
        sig_name = "BackLight_UB"
        sig_start_bit = 9
        update_id_bit = 9
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
        startbit = 9
        byte = 1
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class ScreenDispErrSts:
        sig_name = "ScreenDispErrSts"
        sig_start_bit = 31
        update_id_bit = 34
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


class CCUMCUCDToWPC3InfoCANFDDiagReqFrame:
    msg_name = "CCUMCUCDToWPC3InfoCANFDDiagReqFrame"
    msg_id = 1830
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "CCUMCUCD"
    rx_nodes = ['WPC3']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class TPMInfoCANFDFr01:
    msg_name = "TPMInfoCANFDFr01"
    msg_id = 662
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 32
    tx_node = "TPM"
    rx_nodes = ['CCUMCUCD']
    sig_group_dict = {'RearRightTyreAlarmInfo': ['RearRightTyreAlarmInfoBattLowWarnFlag', 'RearRightTyreAlarmInfoFastLoseWarnFlag', 'RearRightTyreAlarmInfoPWarnFlag', 'RearRightTyreAlarmInfoSysWarnFlag', 'RearRightTyreAlarmInfoTWarnFlag'], 'FrontRightTyreAlarmInfo': ['FrontRightTyreAlarmInfoBattLowWarnFlag', 'FrontRightTyreAlarmInfoFastLoseWarnFlag', 'FrontRightTyreAlarmInfoPWarnFlag', 'FrontRightTyreAlarmInfoSysWarnFlag', 'FrontRightTyreAlarmInfoTWarnFlag'], 'FrontRightTyreData': ['FrontRightTyreDataTyrePressure', 'FrontRightTyreDataTyreTemperature'], 'RearLeftTyreAlarmInfo': ['RearLeftTyreAlarmInfoBattLowWarnFlag', 'RearLeftTyreAlarmInfoFastLoseWarnFlag', 'RearLeftTyreAlarmInfoPWarnFlag', 'RearLeftTyreAlarmInfoSysWarnFlag', 'RearLeftTyreAlarmInfoTWarnFlag'], 'RearRightTyreData': ['RearRightTyreDataTyrePressure', 'RearRightTyreDataTyreTemperature'], 'RearLeftTyreData': ['RearLeftTyreDataTyrePressure', 'RearLeftTyreDataTyreTemperature'], 'FrontLeftTyreData': ['FrontLeftTyreDataTyrePressure', 'FrontLeftTyreDataTyreTemperature'], 'FrontLeftTyreAlarmInfo': ['FrontLeftTyreAlarmInfoBattLowWarnFlag', 'FrontLeftTyreAlarmInfoFastLoseWarnFlag', 'FrontLeftTyreAlarmInfoPWarnFlag', 'FrontLeftTyreAlarmInfoSysWarnFlag', 'FrontLeftTyreAlarmInfoTWarnFlag']}
    sig_group_dataid_dict = {}

    class RearRightTyreAlarmInfoBattLowWarnFlag:
        sig_name = "RearRightTyreAlarmInfoBattLowWarnFlag"
        sig_start_bit = 79
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BattLowWarnFlag_Normal': 0, 'BattLowWarnFlag_Warning': 1}
        compute_method = None
        length = 1
        startbit = 79
        byte = 9
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class RearRightTyreAlarmInfoFastLoseWarnFlag:
        sig_name = "RearRightTyreAlarmInfoFastLoseWarnFlag"
        sig_start_bit = 73
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FastLoseWarnFlag_Normal': 0, 'FastLoseWarnFlag_Warning': 1}
        compute_method = None
        length = 1
        startbit = 73
        byte = 9
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class RearRightTyreAlarmInfo_UB:
        sig_name = "RearRightTyreAlarmInfo_UB"
        sig_start_bit = 101
        update_id_bit = 101
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
        startbit = 101
        byte = 12
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class RearLeftTyreAlarmInfoSysWarnFlag:
        sig_name = "RearLeftTyreAlarmInfoSysWarnFlag"
        sig_start_bit = 52
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SysWarnFlag_Nromal': 0, 'SysWarnFlag_Warning': 1}
        compute_method = None
        length = 1
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class FrontRightTyreAlarmInfo_UB:
        sig_name = "FrontRightTyreAlarmInfo_UB"
        sig_start_bit = 48
        update_id_bit = 48
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
        startbit = 48
        byte = 6
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class RearLeftTyreAlarmInfoFastLoseWarnFlag:
        sig_name = "RearLeftTyreAlarmInfoFastLoseWarnFlag"
        sig_start_bit = 49
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FastLoseWarnFlag_Normal': 0, 'FastLoseWarnFlag_Warning': 1}
        compute_method = None
        length = 1
        startbit = 49
        byte = 6
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class RearRightTyreDataTyrePressure:
        sig_name = "RearRightTyreDataTyrePressure"
        sig_start_bit = 87
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.373
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 255
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 87
        byte = 10
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrontLeftTyreDataTyrePressure:
        sig_name = "FrontLeftTyreDataTyrePressure"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.373
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 255
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 23
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrontRightTyreDataTyrePressure:
        sig_name = "FrontRightTyreDataTyrePressure"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.373
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

    class FrontRightTyreData_UB:
        sig_name = "FrontRightTyreData_UB"
        sig_start_bit = 72
        update_id_bit = 72
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
        startbit = 72
        byte = 9
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class RearLeftTyreAlarmInfo_UB:
        sig_name = "RearLeftTyreAlarmInfo_UB"
        sig_start_bit = 103
        update_id_bit = 103
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
        startbit = 103
        byte = 12
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class RearRightTyreData_UB:
        sig_name = "RearRightTyreData_UB"
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

    class RearLeftTyreData_UB:
        sig_name = "RearLeftTyreData_UB"
        sig_start_bit = 102
        update_id_bit = 102
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
        startbit = 102
        byte = 12
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class RearLeftTyreDataTyrePressure:
        sig_name = "RearLeftTyreDataTyrePressure"
        sig_start_bit = 63
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.373
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 255
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearLeftTyreAlarmInfoTWarnFlag:
        sig_name = "RearLeftTyreAlarmInfoTWarnFlag"
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
        sig_value_table = {'TWarnFlag_Nromal': 0, 'TWarnFlag_HighTWarn': 1, 'TWarnFlag_Reserve1': 2, 'TWarnFlag_Reserve2': 3}
        compute_method = None
        length = 2
        startbit = 55
        byte = 6
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class FrontRightTyreAlarmInfoFastLoseWarnFlag:
        sig_name = "FrontRightTyreAlarmInfoFastLoseWarnFlag"
        sig_start_bit = 25
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FastLoseWarnFlag_Normal': 0, 'FastLoseWarnFlag_Warning': 1}
        compute_method = None
        length = 1
        startbit = 25
        byte = 3
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class FrontLeftTyreAlarmInfoPWarnFlag:
        sig_name = "FrontLeftTyreAlarmInfoPWarnFlag"
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
        sig_value_table = {'PWarnFlag_Normal': 0, 'PWarnFlag_LowPWarn': 1, 'PWarnFlag_Reserve1': 2, 'PWarnFlag_Reserve2': 3}
        compute_method = None
        length = 2
        startbit = 3
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class FrontLeftTyreDataTyreTemperature:
        sig_name = "FrontLeftTyreDataTyreTemperature"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -50.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 255
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrontLeftTyreAlarmInfoSysWarnFlag:
        sig_name = "FrontLeftTyreAlarmInfoSysWarnFlag"
        sig_start_bit = 1
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SysWarnFlag_Nromal': 0, 'SysWarnFlag_Warning': 1}
        compute_method = None
        length = 1
        startbit = 1
        byte = 0
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class FrontRightTyreAlarmInfoSysWarnFlag:
        sig_name = "FrontRightTyreAlarmInfoSysWarnFlag"
        sig_start_bit = 30
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SysWarnFlag_Nromal': 0, 'SysWarnFlag_Warning': 1}
        compute_method = None
        length = 1
        startbit = 30
        byte = 3
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class FrontRightTyreDataTyreTemperature:
        sig_name = "FrontRightTyreDataTyreTemperature"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -50.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 255
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearRightTyreDataTyreTemperature:
        sig_name = "RearRightTyreDataTyreTemperature"
        sig_start_bit = 95
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -50.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 255
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 95
        byte = 11
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrontRightTyreAlarmInfoPWarnFlag:
        sig_name = "FrontRightTyreAlarmInfoPWarnFlag"
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
        sig_value_table = {'PWarnFlag_Normal': 0, 'PWarnFlag_LowPWarn': 1, 'PWarnFlag_Reserve1': 2, 'PWarnFlag_Reserve2': 3}
        compute_method = None
        length = 2
        startbit = 29
        byte = 3
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class FrontLeftTyreData_UB:
        sig_name = "FrontLeftTyreData_UB"
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

    class FrontRightTyreAlarmInfoBattLowWarnFlag:
        sig_name = "FrontRightTyreAlarmInfoBattLowWarnFlag"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BattLowWarnFlag_Normal': 0, 'BattLowWarnFlag_Warning': 1}
        compute_method = None
        length = 1
        startbit = 31
        byte = 3
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class RearLeftTyreAlarmInfoBattLowWarnFlag:
        sig_name = "RearLeftTyreAlarmInfoBattLowWarnFlag"
        sig_start_bit = 53
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BattLowWarnFlag_Normal': 0, 'BattLowWarnFlag_Warning': 1}
        compute_method = None
        length = 1
        startbit = 53
        byte = 6
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class FrontLeftTyreAlarmInfoFastLoseWarnFlag:
        sig_name = "FrontLeftTyreAlarmInfoFastLoseWarnFlag"
        sig_start_bit = 5
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FastLoseWarnFlag_Normal': 0, 'FastLoseWarnFlag_Warning': 1}
        compute_method = None
        length = 1
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class RearRightTyreAlarmInfoTWarnFlag:
        sig_name = "RearRightTyreAlarmInfoTWarnFlag"
        sig_start_bit = 78
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TWarnFlag_Nromal': 0, 'TWarnFlag_HighTWarn': 1, 'TWarnFlag_Reserve1': 2, 'TWarnFlag_Reserve2': 3}
        compute_method = None
        length = 2
        startbit = 78
        byte = 9
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class FrontLeftTyreAlarmInfoBattLowWarnFlag:
        sig_name = "FrontLeftTyreAlarmInfoBattLowWarnFlag"
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
        sig_value_table = {'BattLowWarnFlag_Normal': 0, 'BattLowWarnFlag_Warning': 1}
        compute_method = None
        length = 1
        startbit = 4
        byte = 0
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class FrontLeftTyreAlarmInfoTWarnFlag:
        sig_name = "FrontLeftTyreAlarmInfoTWarnFlag"
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
        sig_value_table = {'TWarnFlag_Nromal': 0, 'TWarnFlag_HighTWarn': 1, 'TWarnFlag_Reserve1': 2, 'TWarnFlag_Reserve2': 3}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class FrontRightTyreAlarmInfoTWarnFlag:
        sig_name = "FrontRightTyreAlarmInfoTWarnFlag"
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
        sig_value_table = {'TWarnFlag_Nromal': 0, 'TWarnFlag_HighTWarn': 1, 'TWarnFlag_Reserve1': 2, 'TWarnFlag_Reserve2': 3}
        compute_method = None
        length = 2
        startbit = 27
        byte = 3
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class RearLeftTyreDataTyreTemperature:
        sig_name = "RearLeftTyreDataTyreTemperature"
        sig_start_bit = 71
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -50.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 255
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 71
        byte = 8
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RearLeftTyreAlarmInfoPWarnFlag:
        sig_name = "RearLeftTyreAlarmInfoPWarnFlag"
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
        sig_value_table = {'PWarnFlag_Normal': 0, 'PWarnFlag_LowPWarn': 1, 'PWarnFlag_Reserve1': 2, 'PWarnFlag_Reserve2': 3}
        compute_method = None
        length = 2
        startbit = 51
        byte = 6
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class FrontLeftTyreAlarmInfo_UB:
        sig_name = "FrontLeftTyreAlarmInfo_UB"
        sig_start_bit = 0
        update_id_bit = 0
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
        startbit = 0
        byte = 0
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class RearRightTyreAlarmInfoSysWarnFlag:
        sig_name = "RearRightTyreAlarmInfoSysWarnFlag"
        sig_start_bit = 76
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SysWarnFlag_Nromal': 0, 'SysWarnFlag_Warning': 1}
        compute_method = None
        length = 1
        startbit = 76
        byte = 9
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class RearRightTyreAlarmInfoPWarnFlag:
        sig_name = "RearRightTyreAlarmInfoPWarnFlag"
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
        sig_value_table = {'PWarnFlag_Normal': 0, 'PWarnFlag_LowPWarn': 1, 'PWarnFlag_Reserve1': 2, 'PWarnFlag_Reserve2': 3}
        compute_method = None
        length = 2
        startbit = 75
        byte = 9
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2


class TPMToCCUMCUCDInfoCANFDDiagRespFrame:
    msg_name = "TPMToCCUMCUCDInfoCANFDDiagRespFrame"
    msg_id = 1578
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "TPM"
    rx_nodes = ['CCUMCUCD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class CCUMCUCDInfoCANFDFr01:
    msg_name = "CCUMCUCDInfoCANFDFr01"
    msg_id = 64
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 16
    tx_node = "CCUMCUCD"
    rx_nodes = ['BNCM', 'TPM', 'WPC3', 'NKR', 'WPC2', 'DRF', 'CD']
    sig_group_dict = {'VMMGlbSig': ['VMMGlbSigCarModSts', 'VMMGlbSigChks', 'VMMGlbSigCntr', 'VMMGlbSigCnvincSubSts1', 'VMMGlbSigDrvgSubSts1', 'VMMGlbSigInactvSubSts1', 'VMMGlbSigLoBattModSts', 'VMMGlbSigUsgModSts'], 'GearLvrIndcnReal': ['GearLvrIndcnRealChks', 'GearLvrIndcnRealCntr', 'GearLvrIndcnRealGearLvrIndcn']}
    sig_group_dataid_dict = {'VMMGlbSig': 1074, 'GearLvrIndcnReal': 1065}

    class VMMGlbSig_UB:
        sig_name = "VMMGlbSig_UB"
        sig_start_bit = 53
        update_id_bit = 53
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
        startbit = 53
        byte = 6
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VMMGlbSigLoBattModSts:
        sig_name = "VMMGlbSigLoBattModSts"
        sig_start_bit = 55
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
        startbit = 55
        byte = 6
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VMMGlbSigCnvincSubSts1:
        sig_name = "VMMGlbSigCnvincSubSts1"
        sig_start_bit = 39
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
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VMMGlbSigChks:
        sig_name = "VMMGlbSigChks"
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

    class GearLvrIndcnReal_UB:
        sig_name = "GearLvrIndcnReal_UB"
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

    class VMMGlbSigCntr:
        sig_name = "VMMGlbSigCntr"
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

    class VMMGlbSigUsgModSts:
        sig_name = "VMMGlbSigUsgModSts"
        sig_start_bit = 3
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
        startbit = 3
        byte = 0
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class UsgModSts:
        sig_name = "UsgModSts"
        sig_start_bit = 7
        update_id_bit = 54
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
        startbit = 7
        byte = 0
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class VMMGlbSigCarModSts:
        sig_name = "VMMGlbSigCarModSts"
        sig_start_bit = 11
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
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class GearLvrIndcnRealCntr:
        sig_name = "GearLvrIndcnRealCntr"
        sig_start_bit = 71
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
        startbit = 71
        byte = 8
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class GearLvrIndcnRealGearLvrIndcn:
        sig_name = "GearLvrIndcnRealGearLvrIndcn"
        sig_start_bit = 67
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 7
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GearLvrIndcn_Default': 0, 'GearLvrIndcn_P': 1, 'GearLvrIndcn_R': 2, 'GearLvrIndcn_N': 3, 'GearLvrIndcn_D': 4, 'GearLvrIndcn_Reserved1': 5, 'GearLvrIndcn_Reserved2': 6, 'GearLvrIndcn_Undefd': 7}
        compute_method = None
        length = 3
        startbit = 67
        byte = 8
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class GearLvrIndcnRealChks:
        sig_name = "GearLvrIndcnRealChks"
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

    class VMMGlbSigDrvgSubSts1:
        sig_name = "VMMGlbSigDrvgSubSts1"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VMMGlbSigInactvSubSts1:
        sig_name = "VMMGlbSigInactvSubSts1"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class CCUMCUCDtoBNCMDigKeyBLERespInfoCANFDFrame:
    msg_name = "CCUMCUCDtoBNCMDigKeyBLERespInfoCANFDFrame"
    msg_id = 769
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "CCUMCUCD"
    rx_nodes = ['BNCM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class WPC2toBNCMNFCKeyReqInsdInfoCANFDFrame:
    msg_name = "WPC2toBNCMNFCKeyReqInsdInfoCANFDFrame"
    msg_id = 776
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "WPC2"
    rx_nodes = ['BNCM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class CCUMCUCDToBNCMInfoCANFDDiagReqFrame:
    msg_name = "CCUMCUCDToBNCMInfoCANFDDiagReqFrame"
    msg_id = 1827
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "CCUMCUCD"
    rx_nodes = ['BNCM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class CCUMCUCDInfoCANFDFr09:
    msg_name = "CCUMCUCDInfoCANFDFr09"
    msg_id = 1024
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 1.0
    msg_length = 8
    tx_node = "CCUMCUCD"
    rx_nodes = ['TPM']
    sig_group_dict = {'AmbPBasLocn': ['AmbPBasLocnP', 'AmbPBasLocnPQf'], 'VehAlti': ['VehAltiAlti', 'VehAltiAltiQf']}
    sig_group_dataid_dict = {}

    class VehAltiAlti:
        sig_name = "VehAltiAlti"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 0.1
        sig_value_offset = -100.0
        sig_value_min = 0
        sig_value_max = 61000
        sig_byteorder = "Motorola"
        sig_value_init = 1000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111111, 0b00000000, 8, 0)]

    class AmbPBasLocnPQf:
        sig_name = "AmbPBasLocnPQf"
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
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 23
        byte = 2
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class AmbPBasLocn_UB:
        sig_name = "AmbPBasLocn_UB"
        sig_start_bit = 21
        update_id_bit = 21
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
        startbit = 21
        byte = 2
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VehAlti_UB:
        sig_name = "VehAlti_UB"
        sig_start_bit = 18
        update_id_bit = 18
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
        startbit = 18
        byte = 2
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class AmbPBasLocnP:
        sig_name = "AmbPBasLocnP"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 0.025
        sig_value_offset = 0
        sig_value_min = 10400
        sig_value_max = 50400
        sig_byteorder = "Motorola"
        sig_value_init = 40520
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class VehAltiAltiQf:
        sig_name = "VehAltiAltiQf"
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
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 17
        byte = 2
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0


class NKRInfoCANFDNmFr:
    msg_name = "NKRInfoCANFDNmFr"
    msg_id = 1288
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "NKR"
    rx_nodes = ['ETCM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class CCUMCUCDToAllInfoCANFDDiagFuncReqFrame:
    msg_name = "CCUMCUCDToAllInfoCANFDDiagFuncReqFrame"
    msg_id = 2047
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CCUMCUCD"
    rx_nodes = ['BNCM', 'TPM', 'WPC3', 'NKR', 'WPC2', 'DRF', 'CD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class CCUMCUCDInfoCANFDFr02:
    msg_name = "CCUMCUCDInfoCANFDFr02"
    msg_id = 144
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 32
    tx_node = "CCUMCUCD"
    rx_nodes = ['BNCM', 'CD', 'TPM', 'WPC3', 'NKR', 'WPC2', 'DRF', 'ETC']
    sig_group_dict = {'WhlPlsCntr': ['WhlPlsCntrChks', 'WhlPlsCntrCntr', 'WhlPlsCntrFL', 'WhlPlsCntrFR', 'WhlPlsCntrRL', 'WhlPlsCntrRR'], 'VehSpd': ['VehSpdChks', 'VehSpdCntr', 'VehSpdQf', 'VehSpdSpd']}
    sig_group_dataid_dict = {'VehSpd': 1043}

    class VehSpdChks:
        sig_name = "VehSpdChks"
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

    class VldKeyInCarFlg:
        sig_name = "VldKeyInCarFlg"
        sig_start_bit = 99
        update_id_bit = 88
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
        startbit = 99
        byte = 12
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VehSpdSpd:
        sig_name = "VehSpdSpd"
        sig_start_bit = 7
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
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111110, 0b00000001, 7, 1)]

    class WhlPlsCntrRL:
        sig_name = "WhlPlsCntrRL"
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

    class FRDoorOpenClsSts:
        sig_name = "FRDoorOpenClsSts"
        sig_start_bit = 75
        update_id_bit = 80
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
        startbit = 75
        byte = 9
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class RRDoorOpenClsSts:
        sig_name = "RRDoorOpenClsSts"
        sig_start_bit = 85
        update_id_bit = 93
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

    class FLDoorOpenClsSts:
        sig_name = "FLDoorOpenClsSts"
        sig_start_bit = 25
        update_id_bit = 81
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
        startbit = 25
        byte = 3
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class WhlPlsCntrFL:
        sig_name = "WhlPlsCntrFL"
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

    class VehSpdCntr:
        sig_name = "VehSpdCntr"
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

    class WhlPlsCntrRR:
        sig_name = "WhlPlsCntrRR"
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

    class WhlPlsCntrFR:
        sig_name = "WhlPlsCntrFR"
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

    class WhlPlsCntrChks:
        sig_name = "WhlPlsCntrChks"
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

    class WhlPlsCntr_UB:
        sig_name = "WhlPlsCntr_UB"
        sig_start_bit = 90
        update_id_bit = 90
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
        startbit = 90
        byte = 11
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class TrSts:
        sig_name = "TrSts"
        sig_start_bit = 83
        update_id_bit = 92
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
        startbit = 83
        byte = 10
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class HoodSts:
        sig_name = "HoodSts"
        sig_start_bit = 73
        update_id_bit = 95
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
        startbit = 73
        byte = 9
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class WhlPlsCntrCntr:
        sig_name = "WhlPlsCntrCntr"
        sig_start_bit = 79
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
        startbit = 79
        byte = 9
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class KeyFindReqFromVMM:
        sig_name = "KeyFindReqFromVMM"
        sig_start_bit = 103
        update_id_bit = 89
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeyLocnReq_Idle': 0, 'KeyLocnReq_PEAllExtAndInt': 1, 'KeyLocnReq_PEAllExt': 2, 'KeyLocnReq_PEDrvrExt': 3, 'KeyLocnReq_PEPassExt': 4, 'KeyLocnReq_PEFrntExt': 5, 'KeyLocnReq_PERearExt': 6, 'KeyLocnReq_PEAllInt': 7, 'KeyLocnReq_PSAllInt': 8, 'KeyLocnReq_Reserved1': 9, 'KeyLocnReq_Reserved2': 10}
        compute_method = None
        length = 4
        startbit = 103
        byte = 12
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class RLDoorOpenClsSts:
        sig_name = "RLDoorOpenClsSts"
        sig_start_bit = 87
        update_id_bit = 94
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
        startbit = 87
        byte = 10
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class VehSpdQf:
        sig_name = "VehSpdQf"
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
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 27
        byte = 3
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VehSpd_UB:
        sig_name = "VehSpd_UB"
        sig_start_bit = 91
        update_id_bit = 91
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
        startbit = 91
        byte = 11
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3


class CCUMCUCDInfoCANFDFr08:
    msg_name = "CCUMCUCDInfoCANFDFr08"
    msg_id = 780
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.5
    msg_length = 8
    tx_node = "CCUMCUCD"
    rx_nodes = ['ETC']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class CDActT:
        sig_name = "CDActT"
        sig_start_bit = 7
        update_id_bit = 15
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 25
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class BNCMInfoCANFDFr09:
    msg_name = "BNCMInfoCANFDFr09"
    msg_id = 522
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 64
    tx_node = "BNCM"
    rx_nodes = ['ETC']
    sig_group_dict = {'DigKeyLocData4': ['DigKeyLocData4CalibrationDataByte0', 'DigKeyLocData4CalibrationDataByte1', 'DigKeyLocData4CalibrationDataByte10', 'DigKeyLocData4CalibrationDataByte11', 'DigKeyLocData4CalibrationDataByte12', 'DigKeyLocData4CalibrationDataByte13', 'DigKeyLocData4CalibrationDataByte14', 'DigKeyLocData4CalibrationDataByte15', 'DigKeyLocData4CalibrationDataByte16', 'DigKeyLocData4CalibrationDataByte17', 'DigKeyLocData4CalibrationDataByte18', 'DigKeyLocData4CalibrationDataByte19', 'DigKeyLocData4CalibrationDataByte2', 'DigKeyLocData4CalibrationDataByte3', 'DigKeyLocData4CalibrationDataByte4', 'DigKeyLocData4CalibrationDataByte5', 'DigKeyLocData4CalibrationDataByte6', 'DigKeyLocData4CalibrationDataByte7', 'DigKeyLocData4CalibrationDataByte8', 'DigKeyLocData4CalibrationDataByte9', 'DigKeyLocData4FrntLeBLERSSI', 'DigKeyLocData4FrntLeUWBDistance', 'DigKeyLocData4FrntRiBLERSSI', 'DigKeyLocData4FrntRiUWBDistance', 'DigKeyLocData4InVehReBLERSSI', 'DigKeyLocData4InVehReUWBDistance', 'DigKeyLocData4KeyIdByte0', 'DigKeyLocData4KeyIdByte1', 'DigKeyLocData4KeyIdByte10', 'DigKeyLocData4KeyIdByte11', 'DigKeyLocData4KeyIdByte12', 'DigKeyLocData4KeyIdByte13', 'DigKeyLocData4KeyIdByte14', 'DigKeyLocData4KeyIdByte15', 'DigKeyLocData4KeyIdByte2', 'DigKeyLocData4KeyIdByte3', 'DigKeyLocData4KeyIdByte4', 'DigKeyLocData4KeyIdByte5', 'DigKeyLocData4KeyIdByte6', 'DigKeyLocData4KeyIdByte7', 'DigKeyLocData4KeyIdByte8', 'DigKeyLocData4KeyIdByte9', 'DigKeyLocData4MainBLERSSI', 'DigKeyLocData4MainUWBDistance', 'DigKeyLocData4ReLeBLERSSI', 'DigKeyLocData4ReLeUWBDistance', 'DigKeyLocData4ReRiBLERSSI', 'DigKeyLocData4ReRiUWBDistance']}
    sig_group_dataid_dict = {}

    class DigKeyLocData4CalibrationDataByte6:
        sig_name = "DigKeyLocData4CalibrationDataByte6"
        sig_start_bit = 199
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
        startbit = 199
        byte = 24
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData4KeyIdByte3:
        sig_name = "DigKeyLocData4KeyIdByte3"
        sig_start_bit = 335
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
        startbit = 335
        byte = 41
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData4KeyIdByte14:
        sig_name = "DigKeyLocData4KeyIdByte14"
        sig_start_bit = 423
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
        startbit = 423
        byte = 52
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData4KeyIdByte7:
        sig_name = "DigKeyLocData4KeyIdByte7"
        sig_start_bit = 367
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
        startbit = 367
        byte = 45
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData4CalibrationDataByte16:
        sig_name = "DigKeyLocData4CalibrationDataByte16"
        sig_start_bit = 279
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
        startbit = 279
        byte = 34
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData4FrntRiUWBDistance:
        sig_name = "DigKeyLocData4FrntRiUWBDistance"
        sig_start_bit = 111
        update_id_bit = None
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 65535
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 111
        bmuws_info = [(13, 0b11111111, 0b00000000, 8, 0), (14, 0b11111111, 0b00000000, 8, 0)]

    class DigKeyLocData4KeyIdByte1:
        sig_name = "DigKeyLocData4KeyIdByte1"
        sig_start_bit = 319
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
        startbit = 319
        byte = 39
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData4KeyIdByte6:
        sig_name = "DigKeyLocData4KeyIdByte6"
        sig_start_bit = 359
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
        startbit = 359
        byte = 44
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData4ReRiBLERSSI:
        sig_name = "DigKeyLocData4ReRiBLERSSI"
        sig_start_bit = 55
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
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData4ReLeBLERSSI:
        sig_name = "DigKeyLocData4ReLeBLERSSI"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData4CalibrationDataByte10:
        sig_name = "DigKeyLocData4CalibrationDataByte10"
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

    class DigKeyLocData4CalibrationDataByte8:
        sig_name = "DigKeyLocData4CalibrationDataByte8"
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

    class DigKeyLocData4CalibrationDataByte0:
        sig_name = "DigKeyLocData4CalibrationDataByte0"
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

    class DigKeyLocData4KeyIdByte12:
        sig_name = "DigKeyLocData4KeyIdByte12"
        sig_start_bit = 407
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
        startbit = 407
        byte = 50
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData4CalibrationDataByte15:
        sig_name = "DigKeyLocData4CalibrationDataByte15"
        sig_start_bit = 271
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
        startbit = 271
        byte = 33
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData4CalibrationDataByte11:
        sig_name = "DigKeyLocData4CalibrationDataByte11"
        sig_start_bit = 239
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
        startbit = 239
        byte = 29
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData4KeyIdByte0:
        sig_name = "DigKeyLocData4KeyIdByte0"
        sig_start_bit = 311
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
        startbit = 311
        byte = 38
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData4MainBLERSSI:
        sig_name = "DigKeyLocData4MainBLERSSI"
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

    class DigKeyLocData4KeyIdByte15:
        sig_name = "DigKeyLocData4KeyIdByte15"
        sig_start_bit = 431
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
        startbit = 431
        byte = 53
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData4CalibrationDataByte19:
        sig_name = "DigKeyLocData4CalibrationDataByte19"
        sig_start_bit = 303
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
        startbit = 303
        byte = 37
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData4ReRiUWBDistance:
        sig_name = "DigKeyLocData4ReRiUWBDistance"
        sig_start_bit = 63
        update_id_bit = None
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 65535
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 63
        bmuws_info = [(7, 0b11111111, 0b00000000, 8, 0), (8, 0b11111111, 0b00000000, 8, 0)]

    class DigKeyLocData4CalibrationDataByte4:
        sig_name = "DigKeyLocData4CalibrationDataByte4"
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

    class DigKeyLocData4CalibrationDataByte13:
        sig_name = "DigKeyLocData4CalibrationDataByte13"
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

    class DigKeyLocData4KeyIdByte13:
        sig_name = "DigKeyLocData4KeyIdByte13"
        sig_start_bit = 415
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
        startbit = 415
        byte = 51
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData4KeyIdByte4:
        sig_name = "DigKeyLocData4KeyIdByte4"
        sig_start_bit = 343
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
        startbit = 343
        byte = 42
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData4KeyIdByte8:
        sig_name = "DigKeyLocData4KeyIdByte8"
        sig_start_bit = 375
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
        startbit = 375
        byte = 46
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData4CalibrationDataByte9:
        sig_name = "DigKeyLocData4CalibrationDataByte9"
        sig_start_bit = 223
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
        startbit = 223
        byte = 27
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData4KeyIdByte11:
        sig_name = "DigKeyLocData4KeyIdByte11"
        sig_start_bit = 399
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
        startbit = 399
        byte = 49
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData4CalibrationDataByte18:
        sig_name = "DigKeyLocData4CalibrationDataByte18"
        sig_start_bit = 295
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
        startbit = 295
        byte = 36
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData4FrntRiBLERSSI:
        sig_name = "DigKeyLocData4FrntRiBLERSSI"
        sig_start_bit = 103
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
        startbit = 103
        byte = 12
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData4CalibrationDataByte1:
        sig_name = "DigKeyLocData4CalibrationDataByte1"
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

    class DigKeyLocData4CalibrationDataByte12:
        sig_name = "DigKeyLocData4CalibrationDataByte12"
        sig_start_bit = 247
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
        startbit = 247
        byte = 30
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData4FrntLeBLERSSI:
        sig_name = "DigKeyLocData4FrntLeBLERSSI"
        sig_start_bit = 79
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
        startbit = 79
        byte = 9
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData4KeyIdByte10:
        sig_name = "DigKeyLocData4KeyIdByte10"
        sig_start_bit = 391
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
        startbit = 391
        byte = 48
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData4CalibrationDataByte5:
        sig_name = "DigKeyLocData4CalibrationDataByte5"
        sig_start_bit = 191
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
        startbit = 191
        byte = 23
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData4KeyIdByte2:
        sig_name = "DigKeyLocData4KeyIdByte2"
        sig_start_bit = 327
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
        startbit = 327
        byte = 40
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData4CalibrationDataByte3:
        sig_name = "DigKeyLocData4CalibrationDataByte3"
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

    class DigKeyLocData4CalibrationDataByte7:
        sig_name = "DigKeyLocData4CalibrationDataByte7"
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

    class DigKeyLocData4KeyIdByte9:
        sig_name = "DigKeyLocData4KeyIdByte9"
        sig_start_bit = 383
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
        startbit = 383
        byte = 47
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData4FrntLeUWBDistance:
        sig_name = "DigKeyLocData4FrntLeUWBDistance"
        sig_start_bit = 87
        update_id_bit = None
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 65535
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 87
        bmuws_info = [(10, 0b11111111, 0b00000000, 8, 0), (11, 0b11111111, 0b00000000, 8, 0)]

    class DigKeyLocData4MainUWBDistance:
        sig_name = "DigKeyLocData4MainUWBDistance"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 65535
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 15
        bmuws_info = [(1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DigKeyLocData4CalibrationDataByte14:
        sig_name = "DigKeyLocData4CalibrationDataByte14"
        sig_start_bit = 263
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
        startbit = 263
        byte = 32
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData4ReLeUWBDistance:
        sig_name = "DigKeyLocData4ReLeUWBDistance"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 65535
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class DigKeyLocData4CalibrationDataByte17:
        sig_name = "DigKeyLocData4CalibrationDataByte17"
        sig_start_bit = 287
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
        startbit = 287
        byte = 35
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData4KeyIdByte5:
        sig_name = "DigKeyLocData4KeyIdByte5"
        sig_start_bit = 351
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
        startbit = 351
        byte = 43
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData4CalibrationDataByte2:
        sig_name = "DigKeyLocData4CalibrationDataByte2"
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

    class DigKeyLocData4InVehReBLERSSI:
        sig_name = "DigKeyLocData4InVehReBLERSSI"
        sig_start_bit = 127
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
        startbit = 127
        byte = 15
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DigKeyLocData4InVehReUWBDistance:
        sig_name = "DigKeyLocData4InVehReUWBDistance"
        sig_start_bit = 135
        update_id_bit = None
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 65535
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 135
        bmuws_info = [(16, 0b11111111, 0b00000000, 8, 0), (17, 0b11111111, 0b00000000, 8, 0)]


class CCUMCUCDInfoCANFDNmFr:
    msg_name = "CCUMCUCDInfoCANFDNmFr"
    msg_id = 1339
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CCUMCUCD"
    rx_nodes = ['BNCM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class CCUMCUCDInfoCANFDFr12:
    msg_name = "CCUMCUCDInfoCANFDFr12"
    msg_id = 800
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "CCUMCUCD"
    rx_nodes = ['CD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class LuminanceLevelReq:
        sig_name = "LuminanceLevelReq"
        sig_start_bit = 15
        update_id_bit = 1
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "SCALE_LINEAR_AND_TEXTTABLE"
        sig_value_table = {'BattSOH_Invalid': 255}
        compute_method = None
        length = 8
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DisplayAreaCtrl:
        sig_name = "DisplayAreaCtrl"
        sig_start_bit = 5
        update_id_bit = 2
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 7
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 5
        byte = 0
        mask = 0b00111000
        unmask = 0b11000111
        shift = 3


class CCUMCUCDToNKRInfoCANFDDiagReqFrame:
    msg_name = "CCUMCUCDToNKRInfoCANFDDiagReqFrame"
    msg_id = 1829
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "CCUMCUCD"
    rx_nodes = ['NKR']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


