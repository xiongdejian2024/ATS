class LCURToPPODLCURCANFD1DiagReqFrame:
    msg_name = "LCURToPPODLCURCANFD1DiagReqFrame"
    msg_id = 1857
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "LCUR"
    rx_nodes = ['PPOD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class RPODLCURCANFD1Fr01:
    msg_name = "RPODLCURCANFD1Fr01"
    msg_id = 406
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 64
    tx_node = "RPOD"
    rx_nodes = ['LCUR']
    sig_group_dict = {'RRDoorPosnSts': ['RRDoorPosnStsDoorAngPosn', 'RRDoorPosnStsDoorPercPosn'], 'RRDoorAntiPnchFb': ['RRDoorAntiPnchFbCloseAntiPnchSts', 'RRDoorAntiPnchFbOPenAntiPnchSts'], 'RRPwrDoorMotPrm': ['RRPwrDoorMotPrmPwrDoorStsFb', 'RRPwrDoorMotPrmStopEvnt']}
    sig_group_dataid_dict = {}

    class RRDoorPosnSts_UB:
        sig_name = "RRDoorPosnSts_UB"
        sig_start_bit = 15
        update_id_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class RRDoorAntiPnchFb_UB:
        sig_name = "RRDoorAntiPnchFb_UB"
        sig_start_bit = 1
        update_id_bit = 1
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
        startbit = 1
        byte = 0
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class RRDoorSpd:
        sig_name = "RRDoorSpd"
        sig_start_bit = 31
        update_id_bit = 47
        sig_length = 8
        sig_value_factor = 0.5
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 255
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RRDoorAntiPnchFbCloseAntiPnchSts:
        sig_name = "RRDoorAntiPnchFbCloseAntiPnchSts"
        sig_start_bit = 7
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
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class RRDoorPosnStsDoorPercPosn:
        sig_name = "RRDoorPosnStsDoorPercPosn"
        sig_start_bit = 23
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
        startbit = 23
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RRDoorPosnStsDoorAngPosn:
        sig_name = "RRDoorPosnStsDoorAngPosn"
        sig_start_bit = 14
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
        startbit = 14
        byte = 1
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class RRPwrDoorMotPrmStopEvnt:
        sig_name = "RRPwrDoorMotPrmStopEvnt"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'StopEvnt_NONE': 0, 'StopEvnt_BRAKE': 1, 'StopEvnt_KEY': 2, 'StopEvnt_VEHSPEED': 3, 'StopEvnt_RADAR': 4, 'StopEvnt_SLOWDOWN': 5, 'StopEvnt_ITINERARYL': 6, 'StopEvnt_TIMEOut': 7, 'StopEvnt_LATCH': 8, 'StopEvnt_OCP': 9, 'StopEvnt_ANTIPINCH': 10, 'StopEvnt_NOPLAYING': 11, 'StopEvnt_HALL': 12, 'StopEvnt_NORMAL': 13, 'StopEvnt_HAND': 14, 'StopEvnt_ERROR': 15}
        compute_method = None
        length = 4
        startbit = 39
        byte = 4
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class RRPwrDoorMotPrmPwrDoorStsFb:
        sig_name = "RRPwrDoorMotPrmPwrDoorStsFb"
        sig_start_bit = 35
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 6
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PwrDoorStsFb_DoorStUndef': 0, 'PwrDoorStsFb_DoorStWait': 1, 'PwrDoorStsFb_DoorStOpen': 2, 'PwrDoorStsFb_DoorStClose': 3, 'PwrDoorStsFb_DoorStRollBack': 4, 'PwrDoorStsFb_DoorSecondOpen': 5, 'PwrDoorStsFb_DoorTipToRun': 6}
        compute_method = None
        length = 4
        startbit = 35
        byte = 4
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class RRPwrDoorMotPrm_UB:
        sig_name = "RRPwrDoorMotPrm_UB"
        sig_start_bit = 46
        update_id_bit = 46
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
        startbit = 46
        byte = 5
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class RRDoorAntiPnchFbOPenAntiPnchSts:
        sig_name = "RRDoorAntiPnchFbOPenAntiPnchSts"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class RRDoorMtnSts:
        sig_name = "RRDoorMtnSts"
        sig_start_bit = 5
        update_id_bit = 0
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
        startbit = 5
        byte = 0
        mask = 0b00111100
        unmask = 0b11000011
        shift = 2


class DRMFRLCURCANFD1Fr02:
    msg_name = "DRMFRLCURCANFD1Fr02"
    msg_id = 401
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 64
    tx_node = "DRMFR"
    rx_nodes = ['PPOD', 'LCUR']
    sig_group_dict = {'FrntRiDoorRdrObj10': ['FrntRiDoorRdrObj10RdrObjDstX', 'FrntRiDoorRdrObj10RdrObjDstY', 'FrntRiDoorRdrObj10RdrObjDstZ', 'FrntRiDoorRdrObj10RdrObjV'], 'FrntRiDoorRdrObj9': ['FrntRiDoorRdrObj9RdrObjDstX', 'FrntRiDoorRdrObj9RdrObjDstY', 'FrntRiDoorRdrObj9RdrObjDstZ', 'FrntRiDoorRdrObj9RdrObjV'], 'FrntRiDoorRdrObj8': ['FrntRiDoorRdrObj8RdrObjDstX', 'FrntRiDoorRdrObj8RdrObjDstY', 'FrntRiDoorRdrObj8RdrObjDstZ', 'FrntRiDoorRdrObj8RdrObjV'], 'FrntRiDoorRdrObj7': ['FrntRiDoorRdrObj7RdrObjDstX', 'FrntRiDoorRdrObj7RdrObjDstY', 'FrntRiDoorRdrObj7RdrObjDstZ', 'FrntRiDoorRdrObj7RdrObjV'], 'FrntRiDoorRdrObj2': ['FrntRiDoorRdrObj2RdrObjDstX', 'FrntRiDoorRdrObj2RdrObjDstY', 'FrntRiDoorRdrObj2RdrObjDstZ', 'FrntRiDoorRdrObj2RdrObjV'], 'FrntRiDoorRdrObj1': ['FrntRiDoorRdrObj1RdrObjDstX', 'FrntRiDoorRdrObj1RdrObjDstY', 'FrntRiDoorRdrObj1RdrObjDstZ', 'FrntRiDoorRdrObj1RdrObjV'], 'FrntRiDoorRdrObj3': ['FrntRiDoorRdrObj3RdrObjDstX', 'FrntRiDoorRdrObj3RdrObjDstY', 'FrntRiDoorRdrObj3RdrObjDstZ', 'FrntRiDoorRdrObj3RdrObjV'], 'FrntRiDoorRdrObj4': ['FrntRiDoorRdrObj4RdrObjDstX', 'FrntRiDoorRdrObj4RdrObjDstY', 'FrntRiDoorRdrObj4RdrObjDstZ', 'FrntRiDoorRdrObj4RdrObjV'], 'FrntRiDoorRdrObj6': ['FrntRiDoorRdrObj6RdrObjDstX', 'FrntRiDoorRdrObj6RdrObjDstY', 'FrntRiDoorRdrObj6RdrObjDstZ', 'FrntRiDoorRdrObj6RdrObjV'], 'FrntRiDoorRdrObj5': ['FrntRiDoorRdrObj5RdrObjDstX', 'FrntRiDoorRdrObj5RdrObjDstY', 'FrntRiDoorRdrObj5RdrObjDstZ', 'FrntRiDoorRdrObj5RdrObjV']}
    sig_group_dataid_dict = {}

    class FrntRiDoorRdrFlt:
        sig_name = "FrntRiDoorRdrFlt"
        sig_start_bit = 484
        update_id_bit = 475
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 6
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorRdrFlt_NoFault': 0, 'DoorRdrFlt_VoltageTooHigh': 1, 'DoorRdrFlt_VoltageTooLow': 2, 'DoorRdrFlt_BusOff': 3, 'DoorRdrFlt_LostCommunication': 4, 'DoorRdrFlt_Covered': 5, 'DoorRdrFlt_TimeSyncError': 6}
        compute_method = None
        length = 3
        startbit = 484
        byte = 60
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class FrntRiDoorRdrObj1RdrObjDstZ:
        sig_name = "FrntRiDoorRdrObj1RdrObjDstZ"
        sig_start_bit = 19
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 19
        bmuws_info = [(2, 0b00001111, 0b11110000, 4, 0), (3, 0b11111100, 0b00000011, 6, 2)]

    class FrntRiDoorRdrObj7RdrObjDstX:
        sig_name = "FrntRiDoorRdrObj7RdrObjDstX"
        sig_start_bit = 295
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 295
        bmuws_info = [(36, 0b11111111, 0b00000000, 8, 0), (37, 0b11000000, 0b00111111, 2, 6)]

    class FrntRiDoorRdrObj3RdrObjDstX:
        sig_name = "FrntRiDoorRdrObj3RdrObjDstX"
        sig_start_bit = 103
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 103
        bmuws_info = [(12, 0b11111111, 0b00000000, 8, 0), (13, 0b11000000, 0b00111111, 2, 6)]

    class FrntRiDoorRdrObj2RdrObjV:
        sig_name = "FrntRiDoorRdrObj2RdrObjV"
        sig_start_bit = 73
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -2000
        sig_value_max = 2000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 73
        bmuws_info = [(9, 0b00000011, 0b11111100, 2, 0), (10, 0b11111111, 0b00000000, 8, 0), (11, 0b11000000, 0b00111111, 2, 6)]

    class FrntRiDoorRdrObj2RdrObjDstZ:
        sig_name = "FrntRiDoorRdrObj2RdrObjDstZ"
        sig_start_bit = 67
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 67
        bmuws_info = [(8, 0b00001111, 0b11110000, 4, 0), (9, 0b11111100, 0b00000011, 6, 2)]

    class FrntRiDoorRdrObj10_UB:
        sig_name = "FrntRiDoorRdrObj10_UB"
        sig_start_bit = 477
        update_id_bit = 477
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
        startbit = 477
        byte = 59
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class FrntRiDoorRdrObj9RdrObjDstY:
        sig_name = "FrntRiDoorRdrObj9RdrObjDstY"
        sig_start_bit = 397
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 397
        bmuws_info = [(49, 0b00111111, 0b11000000, 6, 0), (50, 0b11110000, 0b00001111, 4, 4)]

    class FrntRiDoorRdrObj2RdrObjDstY:
        sig_name = "FrntRiDoorRdrObj2RdrObjDstY"
        sig_start_bit = 61
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 61
        bmuws_info = [(7, 0b00111111, 0b11000000, 6, 0), (8, 0b11110000, 0b00001111, 4, 4)]

    class FrntRiDoorRdrObj5RdrObjV:
        sig_name = "FrntRiDoorRdrObj5RdrObjV"
        sig_start_bit = 217
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -2000
        sig_value_max = 2000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 217
        bmuws_info = [(27, 0b00000011, 0b11111100, 2, 0), (28, 0b11111111, 0b00000000, 8, 0), (29, 0b11000000, 0b00111111, 2, 6)]

    class FrntRiDoorRdrObj9RdrObjV:
        sig_name = "FrntRiDoorRdrObj9RdrObjV"
        sig_start_bit = 409
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -2000
        sig_value_max = 2000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 409
        bmuws_info = [(51, 0b00000011, 0b11111100, 2, 0), (52, 0b11111111, 0b00000000, 8, 0), (53, 0b11000000, 0b00111111, 2, 6)]

    class FrntRiDoorRdrObj4RdrObjDstZ:
        sig_name = "FrntRiDoorRdrObj4RdrObjDstZ"
        sig_start_bit = 163
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 163
        bmuws_info = [(20, 0b00001111, 0b11110000, 4, 0), (21, 0b11111100, 0b00000011, 6, 2)]

    class FrntRiDoorRdrObj10RdrObjDstZ:
        sig_name = "FrntRiDoorRdrObj10RdrObjDstZ"
        sig_start_bit = 451
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 451
        bmuws_info = [(56, 0b00001111, 0b11110000, 4, 0), (57, 0b11111100, 0b00000011, 6, 2)]

    class FrntRiDoorRdrObj9_UB:
        sig_name = "FrntRiDoorRdrObj9_UB"
        sig_start_bit = 429
        update_id_bit = 429
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
        startbit = 429
        byte = 53
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class FrntRiDoorRdrObj4RdrObjDstY:
        sig_name = "FrntRiDoorRdrObj4RdrObjDstY"
        sig_start_bit = 157
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 157
        bmuws_info = [(19, 0b00111111, 0b11000000, 6, 0), (20, 0b11110000, 0b00001111, 4, 4)]

    class FRRdrWorkSts:
        sig_name = "FRRdrWorkSts"
        sig_start_bit = 487
        update_id_bit = 476
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Worksts_Inactive': 0, 'Worksts_Init': 1, 'Worksts_Active': 2, 'Worksts_Resd1': 3, 'Worksts_Resd2': 4, 'Worksts_Resd3': 5}
        compute_method = None
        length = 3
        startbit = 487
        byte = 60
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class FrntRiDoorRdrObj7RdrObjDstY:
        sig_name = "FrntRiDoorRdrObj7RdrObjDstY"
        sig_start_bit = 301
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 301
        bmuws_info = [(37, 0b00111111, 0b11000000, 6, 0), (38, 0b11110000, 0b00001111, 4, 4)]

    class FrntRiDoorRdrMod:
        sig_name = "FrntRiDoorRdrMod"
        sig_start_bit = 481
        update_id_bit = 474
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorRdrMod_NormalMode': 0, 'DoorRdrMod_ParkingMode': 1}
        compute_method = None
        length = 2
        startbit = 481
        byte = 60
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class FrntRiDoorRdrObj10RdrObjDstY:
        sig_name = "FrntRiDoorRdrObj10RdrObjDstY"
        sig_start_bit = 445
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 445
        bmuws_info = [(55, 0b00111111, 0b11000000, 6, 0), (56, 0b11110000, 0b00001111, 4, 4)]

    class FrntRiDoorRdrObj10RdrObjDstX:
        sig_name = "FrntRiDoorRdrObj10RdrObjDstX"
        sig_start_bit = 439
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 439
        bmuws_info = [(54, 0b11111111, 0b00000000, 8, 0), (55, 0b11000000, 0b00111111, 2, 6)]

    class FrntRiDoorRdrObj9RdrObjDstX:
        sig_name = "FrntRiDoorRdrObj9RdrObjDstX"
        sig_start_bit = 391
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 391
        bmuws_info = [(48, 0b11111111, 0b00000000, 8, 0), (49, 0b11000000, 0b00111111, 2, 6)]

    class FrntRiDoorRdrObj8_UB:
        sig_name = "FrntRiDoorRdrObj8_UB"
        sig_start_bit = 381
        update_id_bit = 381
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
        startbit = 381
        byte = 47
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class FrntRiDoorRdrObj6RdrObjDstZ:
        sig_name = "FrntRiDoorRdrObj6RdrObjDstZ"
        sig_start_bit = 259
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 259
        bmuws_info = [(32, 0b00001111, 0b11110000, 4, 0), (33, 0b11111100, 0b00000011, 6, 2)]

    class FrntRiDoorRdrObj7_UB:
        sig_name = "FrntRiDoorRdrObj7_UB"
        sig_start_bit = 333
        update_id_bit = 333
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
        startbit = 333
        byte = 41
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class FrntRiDoorRdrObj1RdrObjV:
        sig_name = "FrntRiDoorRdrObj1RdrObjV"
        sig_start_bit = 25
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -2000
        sig_value_max = 2000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 25
        bmuws_info = [(3, 0b00000011, 0b11111100, 2, 0), (4, 0b11111111, 0b00000000, 8, 0), (5, 0b11000000, 0b00111111, 2, 6)]

    class FrntRiDoorRdrObj3RdrObjDstY:
        sig_name = "FrntRiDoorRdrObj3RdrObjDstY"
        sig_start_bit = 109
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 109
        bmuws_info = [(13, 0b00111111, 0b11000000, 6, 0), (14, 0b11110000, 0b00001111, 4, 4)]

    class FrntRiDoorRdrObj3RdrObjDstZ:
        sig_name = "FrntRiDoorRdrObj3RdrObjDstZ"
        sig_start_bit = 115
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 115
        bmuws_info = [(14, 0b00001111, 0b11110000, 4, 0), (15, 0b11111100, 0b00000011, 6, 2)]

    class FrntRiDoorRdrObj8RdrObjV:
        sig_name = "FrntRiDoorRdrObj8RdrObjV"
        sig_start_bit = 361
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -2000
        sig_value_max = 2000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 361
        bmuws_info = [(45, 0b00000011, 0b11111100, 2, 0), (46, 0b11111111, 0b00000000, 8, 0), (47, 0b11000000, 0b00111111, 2, 6)]

    class FrntRiDoorRdrObj5RdrObjDstY:
        sig_name = "FrntRiDoorRdrObj5RdrObjDstY"
        sig_start_bit = 205
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 205
        bmuws_info = [(25, 0b00111111, 0b11000000, 6, 0), (26, 0b11110000, 0b00001111, 4, 4)]

    class FrntRiDoorRdrObj3RdrObjV:
        sig_name = "FrntRiDoorRdrObj3RdrObjV"
        sig_start_bit = 121
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -2000
        sig_value_max = 2000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 121
        bmuws_info = [(15, 0b00000011, 0b11111100, 2, 0), (16, 0b11111111, 0b00000000, 8, 0), (17, 0b11000000, 0b00111111, 2, 6)]

    class FrntRiDoorRdrObj1RdrObjDstX:
        sig_name = "FrntRiDoorRdrObj1RdrObjDstX"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class FrntRiDoorRdrObj2_UB:
        sig_name = "FrntRiDoorRdrObj2_UB"
        sig_start_bit = 93
        update_id_bit = 93
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
        startbit = 93
        byte = 11
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class FrntRiDoorRdrObj6RdrObjV:
        sig_name = "FrntRiDoorRdrObj6RdrObjV"
        sig_start_bit = 265
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -2000
        sig_value_max = 2000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 265
        bmuws_info = [(33, 0b00000011, 0b11111100, 2, 0), (34, 0b11111111, 0b00000000, 8, 0), (35, 0b11000000, 0b00111111, 2, 6)]

    class FrntRiDoorRdrObj2RdrObjDstX:
        sig_name = "FrntRiDoorRdrObj2RdrObjDstX"
        sig_start_bit = 55
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 55
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b11000000, 0b00111111, 2, 6)]

    class FrntRiDoorRdrObj8RdrObjDstX:
        sig_name = "FrntRiDoorRdrObj8RdrObjDstX"
        sig_start_bit = 343
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 343
        bmuws_info = [(42, 0b11111111, 0b00000000, 8, 0), (43, 0b11000000, 0b00111111, 2, 6)]

    class FrntRiDoorRdrObj10RdrObjV:
        sig_name = "FrntRiDoorRdrObj10RdrObjV"
        sig_start_bit = 457
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -2000
        sig_value_max = 2000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 457
        bmuws_info = [(57, 0b00000011, 0b11111100, 2, 0), (58, 0b11111111, 0b00000000, 8, 0), (59, 0b11000000, 0b00111111, 2, 6)]

    class FrntRiDoorRdrObj8RdrObjDstY:
        sig_name = "FrntRiDoorRdrObj8RdrObjDstY"
        sig_start_bit = 349
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 349
        bmuws_info = [(43, 0b00111111, 0b11000000, 6, 0), (44, 0b11110000, 0b00001111, 4, 4)]

    class FrntRiDoorRdrObj9RdrObjDstZ:
        sig_name = "FrntRiDoorRdrObj9RdrObjDstZ"
        sig_start_bit = 403
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 403
        bmuws_info = [(50, 0b00001111, 0b11110000, 4, 0), (51, 0b11111100, 0b00000011, 6, 2)]

    class FrntRiDoorRdrObj4RdrObjDstX:
        sig_name = "FrntRiDoorRdrObj4RdrObjDstX"
        sig_start_bit = 151
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 151
        bmuws_info = [(18, 0b11111111, 0b00000000, 8, 0), (19, 0b11000000, 0b00111111, 2, 6)]

    class FrntRiDoorRdrObj6RdrObjDstY:
        sig_name = "FrntRiDoorRdrObj6RdrObjDstY"
        sig_start_bit = 253
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 253
        bmuws_info = [(31, 0b00111111, 0b11000000, 6, 0), (32, 0b11110000, 0b00001111, 4, 4)]

    class FrntRiDoorRdrObj5RdrObjDstZ:
        sig_name = "FrntRiDoorRdrObj5RdrObjDstZ"
        sig_start_bit = 211
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 211
        bmuws_info = [(26, 0b00001111, 0b11110000, 4, 0), (27, 0b11111100, 0b00000011, 6, 2)]

    class FrntRiDoorRdrObj7RdrObjV:
        sig_name = "FrntRiDoorRdrObj7RdrObjV"
        sig_start_bit = 313
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -2000
        sig_value_max = 2000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 313
        bmuws_info = [(39, 0b00000011, 0b11111100, 2, 0), (40, 0b11111111, 0b00000000, 8, 0), (41, 0b11000000, 0b00111111, 2, 6)]

    class FrntRiDoorRdrObj1_UB:
        sig_name = "FrntRiDoorRdrObj1_UB"
        sig_start_bit = 45
        update_id_bit = 45
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
        startbit = 45
        byte = 5
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class FrntRiDoorRdrObj6RdrObjDstX:
        sig_name = "FrntRiDoorRdrObj6RdrObjDstX"
        sig_start_bit = 247
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 247
        bmuws_info = [(30, 0b11111111, 0b00000000, 8, 0), (31, 0b11000000, 0b00111111, 2, 6)]

    class FrntRiDoorRdrObj7RdrObjDstZ:
        sig_name = "FrntRiDoorRdrObj7RdrObjDstZ"
        sig_start_bit = 307
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 307
        bmuws_info = [(38, 0b00001111, 0b11110000, 4, 0), (39, 0b11111100, 0b00000011, 6, 2)]

    class FrntRiDoorRdrObj8RdrObjDstZ:
        sig_name = "FrntRiDoorRdrObj8RdrObjDstZ"
        sig_start_bit = 355
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 355
        bmuws_info = [(44, 0b00001111, 0b11110000, 4, 0), (45, 0b11111100, 0b00000011, 6, 2)]

    class FrntRiDoorRdrObj3_UB:
        sig_name = "FrntRiDoorRdrObj3_UB"
        sig_start_bit = 141
        update_id_bit = 141
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
        startbit = 141
        byte = 17
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class FrntRiDoorRdrObj5RdrObjDstX:
        sig_name = "FrntRiDoorRdrObj5RdrObjDstX"
        sig_start_bit = 199
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 199
        bmuws_info = [(24, 0b11111111, 0b00000000, 8, 0), (25, 0b11000000, 0b00111111, 2, 6)]

    class FrntRiDoorRdrObj4_UB:
        sig_name = "FrntRiDoorRdrObj4_UB"
        sig_start_bit = 189
        update_id_bit = 189
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
        startbit = 189
        byte = 23
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class FrntRiDoorRdrObj6_UB:
        sig_name = "FrntRiDoorRdrObj6_UB"
        sig_start_bit = 285
        update_id_bit = 285
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
        startbit = 285
        byte = 35
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class FrntRiDoorRdrObj5_UB:
        sig_name = "FrntRiDoorRdrObj5_UB"
        sig_start_bit = 237
        update_id_bit = 237
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
        startbit = 237
        byte = 29
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class FrntRiDoorRdrObj4RdrObjV:
        sig_name = "FrntRiDoorRdrObj4RdrObjV"
        sig_start_bit = 169
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -2000
        sig_value_max = 2000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 169
        bmuws_info = [(21, 0b00000011, 0b11111100, 2, 0), (22, 0b11111111, 0b00000000, 8, 0), (23, 0b11000000, 0b00111111, 2, 6)]

    class FrntRiDoorRdrObj1RdrObjDstY:
        sig_name = "FrntRiDoorRdrObj1RdrObjDstY"
        sig_start_bit = 13
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 13
        bmuws_info = [(1, 0b00111111, 0b11000000, 6, 0), (2, 0b11110000, 0b00001111, 4, 4)]


class RPODToLCURLCURCANFD1DiagRespFrame:
    msg_name = "RPODToLCURLCURCANFD1DiagRespFrame"
    msg_id = 1603
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "RPOD"
    rx_nodes = ['LCUR']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class DRMRRLCURCANFD1Fr02:
    msg_name = "DRMRRLCURCANFD1Fr02"
    msg_id = 403
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 64
    tx_node = "DRMRR"
    rx_nodes = ['RPOD', 'LCUR']
    sig_group_dict = {'ReRiDoorRdrObj5': ['ReRiDoorRdrObj5RdrObjDstX', 'ReRiDoorRdrObj5RdrObjDstY', 'ReRiDoorRdrObj5RdrObjDstZ', 'ReRiDoorRdrObj5RdrObjV'], 'ReRiDoorRdrObj1': ['ReRiDoorRdrObj1RdrObjDstX', 'ReRiDoorRdrObj1RdrObjDstY', 'ReRiDoorRdrObj1RdrObjDstZ', 'ReRiDoorRdrObj1RdrObjV'], 'ReRiDoorRdrObj9': ['ReRiDoorRdrObj9RdrObjDstX', 'ReRiDoorRdrObj9RdrObjDstY', 'ReRiDoorRdrObj9RdrObjDstZ', 'ReRiDoorRdrObj9RdrObjV'], 'ReRiDoorRdrObj4': ['ReRiDoorRdrObj4RdrObjDstX', 'ReRiDoorRdrObj4RdrObjDstY', 'ReRiDoorRdrObj4RdrObjDstZ', 'ReRiDoorRdrObj4RdrObjV'], 'ReRiDoorRdrObj7': ['ReRiDoorRdrObj7RdrObjDstX', 'ReRiDoorRdrObj7RdrObjDstY', 'ReRiDoorRdrObj7RdrObjDstZ', 'ReRiDoorRdrObj7RdrObjV'], 'ReRiDoorRdrObj6': ['ReRiDoorRdrObj6RdrObjDstX', 'ReRiDoorRdrObj6RdrObjDstY', 'ReRiDoorRdrObj6RdrObjDstZ', 'ReRiDoorRdrObj6RdrObjV'], 'ReRiDoorRdrObj10': ['ReRiDoorRdrObj10RdrObjDstX', 'ReRiDoorRdrObj10RdrObjDstY', 'ReRiDoorRdrObj10RdrObjDstZ', 'ReRiDoorRdrObj10RdrObjV'], 'ReRiDoorRdrObj3': ['ReRiDoorRdrObj3RdrObjDstX', 'ReRiDoorRdrObj3RdrObjDstY', 'ReRiDoorRdrObj3RdrObjDstZ', 'ReRiDoorRdrObj3RdrObjV'], 'ReRiDoorRdrObj8': ['ReRiDoorRdrObj8RdrObjDstX', 'ReRiDoorRdrObj8RdrObjDstY', 'ReRiDoorRdrObj8RdrObjDstZ', 'ReRiDoorRdrObj8RdrObjV'], 'ReRiDoorRdrObj2': ['ReRiDoorRdrObj2RdrObjDstX', 'ReRiDoorRdrObj2RdrObjDstY', 'ReRiDoorRdrObj2RdrObjDstZ', 'ReRiDoorRdrObj2RdrObjV']}
    sig_group_dataid_dict = {}

    class ReRiDoorRdrObj10RdrObjDstX:
        sig_name = "ReRiDoorRdrObj10RdrObjDstX"
        sig_start_bit = 439
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 439
        bmuws_info = [(54, 0b11111111, 0b00000000, 8, 0), (55, 0b11000000, 0b00111111, 2, 6)]

    class ReRiDoorRdrObj5_UB:
        sig_name = "ReRiDoorRdrObj5_UB"
        sig_start_bit = 237
        update_id_bit = 237
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
        startbit = 237
        byte = 29
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class ReRiDoorRdrObj3RdrObjDstY:
        sig_name = "ReRiDoorRdrObj3RdrObjDstY"
        sig_start_bit = 109
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 109
        bmuws_info = [(13, 0b00111111, 0b11000000, 6, 0), (14, 0b11110000, 0b00001111, 4, 4)]

    class ReRiDoorRdrObj8RdrObjDstY:
        sig_name = "ReRiDoorRdrObj8RdrObjDstY"
        sig_start_bit = 349
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 349
        bmuws_info = [(43, 0b00111111, 0b11000000, 6, 0), (44, 0b11110000, 0b00001111, 4, 4)]

    class ReRiDoorRdrObj10RdrObjV:
        sig_name = "ReRiDoorRdrObj10RdrObjV"
        sig_start_bit = 457
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -2000
        sig_value_max = 2000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 457
        bmuws_info = [(57, 0b00000011, 0b11111100, 2, 0), (58, 0b11111111, 0b00000000, 8, 0), (59, 0b11000000, 0b00111111, 2, 6)]

    class ReRiDoorRdrObj3RdrObjV:
        sig_name = "ReRiDoorRdrObj3RdrObjV"
        sig_start_bit = 121
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -2000
        sig_value_max = 2000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 121
        bmuws_info = [(15, 0b00000011, 0b11111100, 2, 0), (16, 0b11111111, 0b00000000, 8, 0), (17, 0b11000000, 0b00111111, 2, 6)]

    class ReRiDoorRdrObj10RdrObjDstY:
        sig_name = "ReRiDoorRdrObj10RdrObjDstY"
        sig_start_bit = 445
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 445
        bmuws_info = [(55, 0b00111111, 0b11000000, 6, 0), (56, 0b11110000, 0b00001111, 4, 4)]

    class ReRiDoorRdrObj3RdrObjDstX:
        sig_name = "ReRiDoorRdrObj3RdrObjDstX"
        sig_start_bit = 103
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 103
        bmuws_info = [(12, 0b11111111, 0b00000000, 8, 0), (13, 0b11000000, 0b00111111, 2, 6)]

    class ReRiDoorRdrObj4RdrObjV:
        sig_name = "ReRiDoorRdrObj4RdrObjV"
        sig_start_bit = 169
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -2000
        sig_value_max = 2000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 169
        bmuws_info = [(21, 0b00000011, 0b11111100, 2, 0), (22, 0b11111111, 0b00000000, 8, 0), (23, 0b11000000, 0b00111111, 2, 6)]

    class ReRiDoorRdrObj3RdrObjDstZ:
        sig_name = "ReRiDoorRdrObj3RdrObjDstZ"
        sig_start_bit = 115
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 115
        bmuws_info = [(14, 0b00001111, 0b11110000, 4, 0), (15, 0b11111100, 0b00000011, 6, 2)]

    class ReRiDoorRdrFlt:
        sig_name = "ReRiDoorRdrFlt"
        sig_start_bit = 484
        update_id_bit = 475
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 6
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorRdrFlt_NoFault': 0, 'DoorRdrFlt_VoltageTooHigh': 1, 'DoorRdrFlt_VoltageTooLow': 2, 'DoorRdrFlt_BusOff': 3, 'DoorRdrFlt_LostCommunication': 4, 'DoorRdrFlt_Covered': 5, 'DoorRdrFlt_TimeSyncError': 6}
        compute_method = None
        length = 3
        startbit = 484
        byte = 60
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class ReRiDoorRdrObj10RdrObjDstZ:
        sig_name = "ReRiDoorRdrObj10RdrObjDstZ"
        sig_start_bit = 451
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 451
        bmuws_info = [(56, 0b00001111, 0b11110000, 4, 0), (57, 0b11111100, 0b00000011, 6, 2)]

    class ReRiDoorRdrObj1_UB:
        sig_name = "ReRiDoorRdrObj1_UB"
        sig_start_bit = 45
        update_id_bit = 45
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
        startbit = 45
        byte = 5
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class ReRiDoorRdrObj9RdrObjV:
        sig_name = "ReRiDoorRdrObj9RdrObjV"
        sig_start_bit = 409
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -2000
        sig_value_max = 2000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 409
        bmuws_info = [(51, 0b00000011, 0b11111100, 2, 0), (52, 0b11111111, 0b00000000, 8, 0), (53, 0b11000000, 0b00111111, 2, 6)]

    class ReRiDoorRdrObj7RdrObjDstY:
        sig_name = "ReRiDoorRdrObj7RdrObjDstY"
        sig_start_bit = 301
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 301
        bmuws_info = [(37, 0b00111111, 0b11000000, 6, 0), (38, 0b11110000, 0b00001111, 4, 4)]

    class ReRiDoorRdrObj9_UB:
        sig_name = "ReRiDoorRdrObj9_UB"
        sig_start_bit = 429
        update_id_bit = 429
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
        startbit = 429
        byte = 53
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class ReRiDoorRdrObj1RdrObjV:
        sig_name = "ReRiDoorRdrObj1RdrObjV"
        sig_start_bit = 25
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -2000
        sig_value_max = 2000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 25
        bmuws_info = [(3, 0b00000011, 0b11111100, 2, 0), (4, 0b11111111, 0b00000000, 8, 0), (5, 0b11000000, 0b00111111, 2, 6)]

    class ReRiDoorRdrObj8RdrObjDstZ:
        sig_name = "ReRiDoorRdrObj8RdrObjDstZ"
        sig_start_bit = 355
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 355
        bmuws_info = [(44, 0b00001111, 0b11110000, 4, 0), (45, 0b11111100, 0b00000011, 6, 2)]

    class ReRiDoorRdrObj2RdrObjV:
        sig_name = "ReRiDoorRdrObj2RdrObjV"
        sig_start_bit = 73
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -2000
        sig_value_max = 2000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 73
        bmuws_info = [(9, 0b00000011, 0b11111100, 2, 0), (10, 0b11111111, 0b00000000, 8, 0), (11, 0b11000000, 0b00111111, 2, 6)]

    class ReRiDoorRdrObj4_UB:
        sig_name = "ReRiDoorRdrObj4_UB"
        sig_start_bit = 189
        update_id_bit = 189
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
        startbit = 189
        byte = 23
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class ReRiDoorRdrObj2RdrObjDstY:
        sig_name = "ReRiDoorRdrObj2RdrObjDstY"
        sig_start_bit = 61
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 61
        bmuws_info = [(7, 0b00111111, 0b11000000, 6, 0), (8, 0b11110000, 0b00001111, 4, 4)]

    class ReRiDoorRdrObj6RdrObjV:
        sig_name = "ReRiDoorRdrObj6RdrObjV"
        sig_start_bit = 265
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -2000
        sig_value_max = 2000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 265
        bmuws_info = [(33, 0b00000011, 0b11111100, 2, 0), (34, 0b11111111, 0b00000000, 8, 0), (35, 0b11000000, 0b00111111, 2, 6)]

    class ReRiDoorRdrObj7RdrObjDstZ:
        sig_name = "ReRiDoorRdrObj7RdrObjDstZ"
        sig_start_bit = 307
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 307
        bmuws_info = [(38, 0b00001111, 0b11110000, 4, 0), (39, 0b11111100, 0b00000011, 6, 2)]

    class ReRiDoorRdrObj4RdrObjDstZ:
        sig_name = "ReRiDoorRdrObj4RdrObjDstZ"
        sig_start_bit = 163
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 163
        bmuws_info = [(20, 0b00001111, 0b11110000, 4, 0), (21, 0b11111100, 0b00000011, 6, 2)]

    class ReRiDoorRdrObj7_UB:
        sig_name = "ReRiDoorRdrObj7_UB"
        sig_start_bit = 333
        update_id_bit = 333
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
        startbit = 333
        byte = 41
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class ReRiDoorRdrObj6RdrObjDstY:
        sig_name = "ReRiDoorRdrObj6RdrObjDstY"
        sig_start_bit = 253
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 253
        bmuws_info = [(31, 0b00111111, 0b11000000, 6, 0), (32, 0b11110000, 0b00001111, 4, 4)]

    class ReRiDoorRdrObj2RdrObjDstZ:
        sig_name = "ReRiDoorRdrObj2RdrObjDstZ"
        sig_start_bit = 67
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 67
        bmuws_info = [(8, 0b00001111, 0b11110000, 4, 0), (9, 0b11111100, 0b00000011, 6, 2)]

    class ReRiDoorRdrObj4RdrObjDstY:
        sig_name = "ReRiDoorRdrObj4RdrObjDstY"
        sig_start_bit = 157
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 157
        bmuws_info = [(19, 0b00111111, 0b11000000, 6, 0), (20, 0b11110000, 0b00001111, 4, 4)]

    class ReRiDoorRdrObj1RdrObjDstY:
        sig_name = "ReRiDoorRdrObj1RdrObjDstY"
        sig_start_bit = 13
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 13
        bmuws_info = [(1, 0b00111111, 0b11000000, 6, 0), (2, 0b11110000, 0b00001111, 4, 4)]

    class ReRiDoorRdrObj5RdrObjV:
        sig_name = "ReRiDoorRdrObj5RdrObjV"
        sig_start_bit = 217
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -2000
        sig_value_max = 2000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 217
        bmuws_info = [(27, 0b00000011, 0b11111100, 2, 0), (28, 0b11111111, 0b00000000, 8, 0), (29, 0b11000000, 0b00111111, 2, 6)]

    class ReRiDoorRdrObj9RdrObjDstY:
        sig_name = "ReRiDoorRdrObj9RdrObjDstY"
        sig_start_bit = 397
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 397
        bmuws_info = [(49, 0b00111111, 0b11000000, 6, 0), (50, 0b11110000, 0b00001111, 4, 4)]

    class ReRiDoorRdrObj9RdrObjDstZ:
        sig_name = "ReRiDoorRdrObj9RdrObjDstZ"
        sig_start_bit = 403
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 403
        bmuws_info = [(50, 0b00001111, 0b11110000, 4, 0), (51, 0b11111100, 0b00000011, 6, 2)]

    class ReRiDoorRdrObj1RdrObjDstZ:
        sig_name = "ReRiDoorRdrObj1RdrObjDstZ"
        sig_start_bit = 19
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 19
        bmuws_info = [(2, 0b00001111, 0b11110000, 4, 0), (3, 0b11111100, 0b00000011, 6, 2)]

    class ReRiDoorRdrObj5RdrObjDstX:
        sig_name = "ReRiDoorRdrObj5RdrObjDstX"
        sig_start_bit = 199
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 199
        bmuws_info = [(24, 0b11111111, 0b00000000, 8, 0), (25, 0b11000000, 0b00111111, 2, 6)]

    class ReRiDoorRdrObj6_UB:
        sig_name = "ReRiDoorRdrObj6_UB"
        sig_start_bit = 285
        update_id_bit = 285
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
        startbit = 285
        byte = 35
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class RRRdrWorkSts:
        sig_name = "RRRdrWorkSts"
        sig_start_bit = 487
        update_id_bit = 476
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Worksts_Inactive': 0, 'Worksts_Init': 1, 'Worksts_Active': 2, 'Worksts_Resd1': 3, 'Worksts_Resd2': 4, 'Worksts_Resd3': 5}
        compute_method = None
        length = 3
        startbit = 487
        byte = 60
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class ReRiDoorRdrObj6RdrObjDstZ:
        sig_name = "ReRiDoorRdrObj6RdrObjDstZ"
        sig_start_bit = 259
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 259
        bmuws_info = [(32, 0b00001111, 0b11110000, 4, 0), (33, 0b11111100, 0b00000011, 6, 2)]

    class ReRiDoorRdrObj5RdrObjDstY:
        sig_name = "ReRiDoorRdrObj5RdrObjDstY"
        sig_start_bit = 205
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 205
        bmuws_info = [(25, 0b00111111, 0b11000000, 6, 0), (26, 0b11110000, 0b00001111, 4, 4)]

    class ReRiDoorRdrObj6RdrObjDstX:
        sig_name = "ReRiDoorRdrObj6RdrObjDstX"
        sig_start_bit = 247
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 247
        bmuws_info = [(30, 0b11111111, 0b00000000, 8, 0), (31, 0b11000000, 0b00111111, 2, 6)]

    class ReRiDoorRdrObj7RdrObjV:
        sig_name = "ReRiDoorRdrObj7RdrObjV"
        sig_start_bit = 313
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -2000
        sig_value_max = 2000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 313
        bmuws_info = [(39, 0b00000011, 0b11111100, 2, 0), (40, 0b11111111, 0b00000000, 8, 0), (41, 0b11000000, 0b00111111, 2, 6)]

    class ReRiDoorRdrObj9RdrObjDstX:
        sig_name = "ReRiDoorRdrObj9RdrObjDstX"
        sig_start_bit = 391
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 391
        bmuws_info = [(48, 0b11111111, 0b00000000, 8, 0), (49, 0b11000000, 0b00111111, 2, 6)]

    class ReRiDoorRdrObj10_UB:
        sig_name = "ReRiDoorRdrObj10_UB"
        sig_start_bit = 477
        update_id_bit = 477
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
        startbit = 477
        byte = 59
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class ReRiDoorRdrMod:
        sig_name = "ReRiDoorRdrMod"
        sig_start_bit = 481
        update_id_bit = 474
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorRdrMod_NormalMode': 0, 'DoorRdrMod_ParkingMode': 1}
        compute_method = None
        length = 2
        startbit = 481
        byte = 60
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class ReRiDoorRdrObj1RdrObjDstX:
        sig_name = "ReRiDoorRdrObj1RdrObjDstX"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class ReRiDoorRdrObj8RdrObjV:
        sig_name = "ReRiDoorRdrObj8RdrObjV"
        sig_start_bit = 361
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -2000
        sig_value_max = 2000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 361
        bmuws_info = [(45, 0b00000011, 0b11111100, 2, 0), (46, 0b11111111, 0b00000000, 8, 0), (47, 0b11000000, 0b00111111, 2, 6)]

    class ReRiDoorRdrObj3_UB:
        sig_name = "ReRiDoorRdrObj3_UB"
        sig_start_bit = 141
        update_id_bit = 141
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
        startbit = 141
        byte = 17
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class ReRiDoorRdrObj4RdrObjDstX:
        sig_name = "ReRiDoorRdrObj4RdrObjDstX"
        sig_start_bit = 151
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 151
        bmuws_info = [(18, 0b11111111, 0b00000000, 8, 0), (19, 0b11000000, 0b00111111, 2, 6)]

    class ReRiDoorRdrObj8_UB:
        sig_name = "ReRiDoorRdrObj8_UB"
        sig_start_bit = 381
        update_id_bit = 381
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
        startbit = 381
        byte = 47
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class ReRiDoorRdrObj8RdrObjDstX:
        sig_name = "ReRiDoorRdrObj8RdrObjDstX"
        sig_start_bit = 343
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 343
        bmuws_info = [(42, 0b11111111, 0b00000000, 8, 0), (43, 0b11000000, 0b00111111, 2, 6)]

    class ReRiDoorRdrObj2_UB:
        sig_name = "ReRiDoorRdrObj2_UB"
        sig_start_bit = 93
        update_id_bit = 93
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
        startbit = 93
        byte = 11
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class ReRiDoorRdrObj7RdrObjDstX:
        sig_name = "ReRiDoorRdrObj7RdrObjDstX"
        sig_start_bit = 295
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 295
        bmuws_info = [(36, 0b11111111, 0b00000000, 8, 0), (37, 0b11000000, 0b00111111, 2, 6)]

    class ReRiDoorRdrObj2RdrObjDstX:
        sig_name = "ReRiDoorRdrObj2RdrObjDstX"
        sig_start_bit = 55
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 55
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b11000000, 0b00111111, 2, 6)]

    class ReRiDoorRdrObj5RdrObjDstZ:
        sig_name = "ReRiDoorRdrObj5RdrObjDstZ"
        sig_start_bit = 211
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 211
        bmuws_info = [(26, 0b00001111, 0b11110000, 4, 0), (27, 0b11111100, 0b00000011, 6, 2)]


class LCURLCURCANFD1Fr05:
    msg_name = "LCURLCURCANFD1Fr05"
    msg_id = 512
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 64
    tx_node = "LCUR"
    rx_nodes = ['RPOD', 'PPOD']
    sig_group_dict = {'VehCfgDataGrp': ['VehCfgDataGrpVehCfgData1BlkIDBytePosn1', 'VehCfgDataGrpVehCfgData1BytePosn10', 'VehCfgDataGrpVehCfgData1BytePosn11', 'VehCfgDataGrpVehCfgData1BytePosn12', 'VehCfgDataGrpVehCfgData1BytePosn13', 'VehCfgDataGrpVehCfgData1BytePosn14', 'VehCfgDataGrpVehCfgData1BytePosn15', 'VehCfgDataGrpVehCfgData1BytePosn16', 'VehCfgDataGrpVehCfgData1BytePosn17', 'VehCfgDataGrpVehCfgData1BytePosn18', 'VehCfgDataGrpVehCfgData1BytePosn19', 'VehCfgDataGrpVehCfgData1BytePosn2', 'VehCfgDataGrpVehCfgData1BytePosn20', 'VehCfgDataGrpVehCfgData1BytePosn21', 'VehCfgDataGrpVehCfgData1BytePosn22', 'VehCfgDataGrpVehCfgData1BytePosn23', 'VehCfgDataGrpVehCfgData1BytePosn24', 'VehCfgDataGrpVehCfgData1BytePosn25', 'VehCfgDataGrpVehCfgData1BytePosn26', 'VehCfgDataGrpVehCfgData1BytePosn27', 'VehCfgDataGrpVehCfgData1BytePosn28', 'VehCfgDataGrpVehCfgData1BytePosn29', 'VehCfgDataGrpVehCfgData1BytePosn3', 'VehCfgDataGrpVehCfgData1BytePosn30', 'VehCfgDataGrpVehCfgData1BytePosn31', 'VehCfgDataGrpVehCfgData1BytePosn32', 'VehCfgDataGrpVehCfgData1BytePosn33', 'VehCfgDataGrpVehCfgData1BytePosn34', 'VehCfgDataGrpVehCfgData1BytePosn35', 'VehCfgDataGrpVehCfgData1BytePosn36', 'VehCfgDataGrpVehCfgData1BytePosn37', 'VehCfgDataGrpVehCfgData1BytePosn38', 'VehCfgDataGrpVehCfgData1BytePosn39', 'VehCfgDataGrpVehCfgData1BytePosn4', 'VehCfgDataGrpVehCfgData1BytePosn40', 'VehCfgDataGrpVehCfgData1BytePosn41', 'VehCfgDataGrpVehCfgData1BytePosn42', 'VehCfgDataGrpVehCfgData1BytePosn43', 'VehCfgDataGrpVehCfgData1BytePosn44', 'VehCfgDataGrpVehCfgData1BytePosn45', 'VehCfgDataGrpVehCfgData1BytePosn46', 'VehCfgDataGrpVehCfgData1BytePosn47', 'VehCfgDataGrpVehCfgData1BytePosn48', 'VehCfgDataGrpVehCfgData1BytePosn49', 'VehCfgDataGrpVehCfgData1BytePosn5', 'VehCfgDataGrpVehCfgData1BytePosn50', 'VehCfgDataGrpVehCfgData1BytePosn51', 'VehCfgDataGrpVehCfgData1BytePosn52', 'VehCfgDataGrpVehCfgData1BytePosn53', 'VehCfgDataGrpVehCfgData1BytePosn54', 'VehCfgDataGrpVehCfgData1BytePosn55', 'VehCfgDataGrpVehCfgData1BytePosn56', 'VehCfgDataGrpVehCfgData1BytePosn57', 'VehCfgDataGrpVehCfgData1BytePosn58', 'VehCfgDataGrpVehCfgData1BytePosn59', 'VehCfgDataGrpVehCfgData1BytePosn6', 'VehCfgDataGrpVehCfgData1BytePosn60', 'VehCfgDataGrpVehCfgData1BytePosn61', 'VehCfgDataGrpVehCfgData1BytePosn62', 'VehCfgDataGrpVehCfgData1BytePosn63', 'VehCfgDataGrpVehCfgData1BytePosn64', 'VehCfgDataGrpVehCfgData1BytePosn7', 'VehCfgDataGrpVehCfgData1BytePosn8', 'VehCfgDataGrpVehCfgData1BytePosn9']}
    sig_group_dataid_dict = {}

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


class DRMRRLCURCANFD1NmFr:
    msg_name = "DRMRRLCURCANFD1NmFr"
    msg_id = 1282
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "DRMRR"
    rx_nodes = ['DRMFR']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class PPODLCURCANFD1Fr02:
    msg_name = "PPODLCURCANFD1Fr02"
    msg_id = 660
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 64
    tx_node = "PPOD"
    rx_nodes = ['LCUR']
    sig_group_dict = {'FRPwrDoorErrFb': ['FRPwrDoorErrFbBoolean', 'FRPwrDoorErrFbHallErrFb', 'FRPwrDoorErrFbMotThermErrFb', 'FRPwrDoorErrFbPosnUnknowFb', 'FRPwrDoorErrFbRollAngErrFb']}
    sig_group_dataid_dict = {}

    class FRDoorSpdModeFb:
        sig_name = "FRDoorSpdModeFb"
        sig_start_bit = 21
        update_id_bit = 2
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SpdMode_Low': 0, 'SpdMode_Middle': 1, 'SpdMode_High': 2}
        compute_method = None
        length = 2
        startbit = 21
        byte = 2
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class FRPwrDoorErrFbMotThermErrFb:
        sig_name = "FRPwrDoorErrFbMotThermErrFb"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 17
        byte = 2
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class FRDoorManResistSts:
        sig_name = "FRDoorManResistSts"
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
        sig_value_table = {'DoorManResistsSts_NoResist': 0, 'DoorManResistsSts_Level1': 1, 'DoorManResistsSts_Level2': 2}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class FRPwrDoorErrFbHallErrFb:
        sig_name = "FRPwrDoorErrFbHallErrFb"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 16
        byte = 2
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FRDoorOpenTrigSrc:
        sig_name = "FRDoorOpenTrigSrc"
        sig_start_bit = 30
        update_id_bit = 0
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 9
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorCtrlTriSrc_NoTrigSrc': 0, 'DoorCtrlTriSrc_InsdSwt': 1, 'DoorCtrlTriSrc_OutdSwt': 2, 'DoorCtrlTriSrc_NFC': 3, 'DoorCtrlTriSrc_Aproch': 4, 'DoorCtrlTriSrc_OutdCtrl': 5, 'DoorCtrlTriSrc_InsdCtrl': 6, 'DoorCtrlTriSrc_Resd1': 7, 'DoorCtrlTriSrc_Resd2': 8, 'DoorCtrlTriSrc_Resd3': 9}
        compute_method = None
        length = 4
        startbit = 30
        byte = 3
        mask = 0b01111000
        unmask = 0b10000111
        shift = 3

    class FRPwrDoorErrFb_UB:
        sig_name = "FRPwrDoorErrFb_UB"
        sig_start_bit = 1
        update_id_bit = 1
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
        startbit = 1
        byte = 0
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class FRPwrDoorErrFbRollAngErrFb:
        sig_name = "FRPwrDoorErrFbRollAngErrFb"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 31
        byte = 3
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class FRPwrDoorErrFbBoolean:
        sig_name = "FRPwrDoorErrFbBoolean"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 18
        byte = 2
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class FRDoorModSts:
        sig_name = "FRDoorModSts"
        sig_start_bit = 23
        update_id_bit = 3
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorModSts_ElecMode': 0, 'DoorModSts_ManualMode': 1}
        compute_method = None
        length = 2
        startbit = 23
        byte = 2
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class FRDoorMaxPosnSetFb:
        sig_name = "FRDoorMaxPosnSetFb"
        sig_start_bit = 15
        update_id_bit = 4
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FRPwrDoorErrFbPosnUnknowFb:
        sig_name = "FRPwrDoorErrFbPosnUnknowFb"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 19
        byte = 2
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3


class PPODLCURCANFD1Fr01:
    msg_name = "PPODLCURCANFD1Fr01"
    msg_id = 256
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 64
    tx_node = "PPOD"
    rx_nodes = ['LCUR']
    sig_group_dict = {'FRPwrDoorMotPrm': ['FRPwrDoorMotPrmPwrDoorStsFb', 'FRPwrDoorMotPrmStopEvnt'], 'FRDoorAntiPnchFb': ['FRDoorAntiPnchFbCloseAntiPnchSts', 'FRDoorAntiPnchFbOPenAntiPnchSts'], 'FRDoorPosnSts': ['FRDoorPosnStsDoorAngPosn', 'FRDoorPosnStsDoorPercPosn']}
    sig_group_dataid_dict = {}

    class FRDoorMtnSts:
        sig_name = "FRDoorMtnSts"
        sig_start_bit = 5
        update_id_bit = 0
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
        startbit = 5
        byte = 0
        mask = 0b00111100
        unmask = 0b11000011
        shift = 2

    class FRDoorPosnStsDoorPercPosn:
        sig_name = "FRDoorPosnStsDoorPercPosn"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FRPwrDoorMotPrm_UB:
        sig_name = "FRPwrDoorMotPrm_UB"
        sig_start_bit = 46
        update_id_bit = 46
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
        startbit = 46
        byte = 5
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class FRDoorAntiPnchFbCloseAntiPnchSts:
        sig_name = "FRDoorAntiPnchFbCloseAntiPnchSts"
        sig_start_bit = 7
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
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class FRDoorPosnStsDoorAngPosn:
        sig_name = "FRDoorPosnStsDoorAngPosn"
        sig_start_bit = 23
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
        startbit = 23
        byte = 2
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class FRDoorAntiPnchFb_UB:
        sig_name = "FRDoorAntiPnchFb_UB"
        sig_start_bit = 1
        update_id_bit = 1
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
        startbit = 1
        byte = 0
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class FRDoorSpd:
        sig_name = "FRDoorSpd"
        sig_start_bit = 31
        update_id_bit = 47
        sig_length = 8
        sig_value_factor = 0.5
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 255
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FRPwrDoorMotPrmPwrDoorStsFb:
        sig_name = "FRPwrDoorMotPrmPwrDoorStsFb"
        sig_start_bit = 35
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 6
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PwrDoorStsFb_DoorStUndef': 0, 'PwrDoorStsFb_DoorStWait': 1, 'PwrDoorStsFb_DoorStOpen': 2, 'PwrDoorStsFb_DoorStClose': 3, 'PwrDoorStsFb_DoorStRollBack': 4, 'PwrDoorStsFb_DoorSecondOpen': 5, 'PwrDoorStsFb_DoorTipToRun': 6}
        compute_method = None
        length = 4
        startbit = 35
        byte = 4
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class FRDoorAntiPnchFbOPenAntiPnchSts:
        sig_name = "FRDoorAntiPnchFbOPenAntiPnchSts"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class FRDoorPosnSts_UB:
        sig_name = "FRDoorPosnSts_UB"
        sig_start_bit = 16
        update_id_bit = 16
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
        startbit = 16
        byte = 2
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FRPwrDoorMotPrmStopEvnt:
        sig_name = "FRPwrDoorMotPrmStopEvnt"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'StopEvnt_NONE': 0, 'StopEvnt_BRAKE': 1, 'StopEvnt_KEY': 2, 'StopEvnt_VEHSPEED': 3, 'StopEvnt_RADAR': 4, 'StopEvnt_SLOWDOWN': 5, 'StopEvnt_ITINERARYL': 6, 'StopEvnt_TIMEOut': 7, 'StopEvnt_LATCH': 8, 'StopEvnt_OCP': 9, 'StopEvnt_ANTIPINCH': 10, 'StopEvnt_NOPLAYING': 11, 'StopEvnt_HALL': 12, 'StopEvnt_NORMAL': 13, 'StopEvnt_HAND': 14, 'StopEvnt_ERROR': 15}
        compute_method = None
        length = 4
        startbit = 39
        byte = 4
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4


class DRMRRLCURCANFD1Fr04:
    msg_name = "DRMRRLCURCANFD1Fr04"
    msg_id = 658
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "DRMRR"
    rx_nodes = ['RPOD']
    sig_group_dict = {'RRRdrErrFb': ['RRRdrErrFbOverTempErrFb', 'RRRdrErrFbOverVoltagepErrFb', 'RRRdrErrFbSnsrBlkErrFb']}
    sig_group_dataid_dict = {}

    class RRRdrErrFbOverTempErrFb:
        sig_name = "RRRdrErrFbOverTempErrFb"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class RRRdrErrFbSnsrBlkErrFb:
        sig_name = "RRRdrErrFbSnsrBlkErrFb"
        sig_start_bit = 7
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
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class RRRdrErrFb_UB:
        sig_name = "RRRdrErrFb_UB"
        sig_start_bit = 4
        update_id_bit = 4
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
        startbit = 4
        byte = 0
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class RRRdrErrFbOverVoltagepErrFb:
        sig_name = "RRRdrErrFbOverVoltagepErrFb"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6


class RPODLCURCANFD1NmFr:
    msg_name = "RPODLCURCANFD1NmFr"
    msg_id = 1285
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "RPOD"
    rx_nodes = ['PPOD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class DRMFRLCURCANFD1Fr01:
    msg_name = "DRMFRLCURCANFD1Fr01"
    msg_id = 144
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "DRMFR"
    rx_nodes = ['PPOD', 'LCUR']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class FRDoorObstclDst:
        sig_name = "FRDoorObstclDst"
        sig_start_bit = 7
        update_id_bit = 15
        sig_length = 8
        sig_value_factor = 0.5
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 255
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class PPODLCURCANFD1NmFr:
    msg_name = "PPODLCURCANFD1NmFr"
    msg_id = 1283
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "PPOD"
    rx_nodes = ['LCUR']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class LCURToRPODLCURCANFD1DiagReqFrame:
    msg_name = "LCURToRPODLCURCANFD1DiagReqFrame"
    msg_id = 1859
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "LCUR"
    rx_nodes = ['RPOD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class DRMFRLCURCANFD1Fr03:
    msg_name = "DRMFRLCURCANFD1Fr03"
    msg_id = 402
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 64
    tx_node = "DRMFR"
    rx_nodes = ['LCUR']
    sig_group_dict = {'FrntRiDoorRdrObj13': ['FrntRiDoorRdrObj13RdrObjDstX', 'FrntRiDoorRdrObj13RdrObjDstY', 'FrntRiDoorRdrObj13RdrObjDstZ', 'FrntRiDoorRdrObj13RdrObjV'], 'FrntRiDoorRdrObj11': ['FrntRiDoorRdrObj11RdrObjDstX', 'FrntRiDoorRdrObj11RdrObjDstY', 'FrntRiDoorRdrObj11RdrObjDstZ', 'FrntRiDoorRdrObj11RdrObjV'], 'FrntRiDoorRdrObj16': ['FrntRiDoorRdrObj16RdrObjDstX', 'FrntRiDoorRdrObj16RdrObjDstY', 'FrntRiDoorRdrObj16RdrObjDstZ', 'FrntRiDoorRdrObj16RdrObjV'], 'FrntRiDoorRdrObj12': ['FrntRiDoorRdrObj12RdrObjDstX', 'FrntRiDoorRdrObj12RdrObjDstY', 'FrntRiDoorRdrObj12RdrObjDstZ', 'FrntRiDoorRdrObj12RdrObjV'], 'FrntRiDoorRdrObj15': ['FrntRiDoorRdrObj15RdrObjDstX', 'FrntRiDoorRdrObj15RdrObjDstY', 'FrntRiDoorRdrObj15RdrObjDstZ', 'FrntRiDoorRdrObj15RdrObjV'], 'FrntRiDoorRdrObj14': ['FrntRiDoorRdrObj14RdrObjDstX', 'FrntRiDoorRdrObj14RdrObjDstY', 'FrntRiDoorRdrObj14RdrObjDstZ', 'FrntRiDoorRdrObj14RdrObjV']}
    sig_group_dataid_dict = {}

    class FrntRiDoorRdrObj11RdrObjDstZ:
        sig_name = "FrntRiDoorRdrObj11RdrObjDstZ"
        sig_start_bit = 19
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 19
        bmuws_info = [(2, 0b00001111, 0b11110000, 4, 0), (3, 0b11111100, 0b00000011, 6, 2)]

    class FrntRiDoorRdrObj15RdrObjDstZ:
        sig_name = "FrntRiDoorRdrObj15RdrObjDstZ"
        sig_start_bit = 211
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 211
        bmuws_info = [(26, 0b00001111, 0b11110000, 4, 0), (27, 0b11111100, 0b00000011, 6, 2)]

    class FrntRiDoorRdrObj16RdrObjV:
        sig_name = "FrntRiDoorRdrObj16RdrObjV"
        sig_start_bit = 265
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -2000
        sig_value_max = 2000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 265
        bmuws_info = [(33, 0b00000011, 0b11111100, 2, 0), (34, 0b11111111, 0b00000000, 8, 0), (35, 0b11000000, 0b00111111, 2, 6)]

    class FrntRiDoorRdrObj12RdrObjDstX:
        sig_name = "FrntRiDoorRdrObj12RdrObjDstX"
        sig_start_bit = 55
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 55
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b11000000, 0b00111111, 2, 6)]

    class FrntRiDoorRdrObj15RdrObjDstX:
        sig_name = "FrntRiDoorRdrObj15RdrObjDstX"
        sig_start_bit = 199
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 199
        bmuws_info = [(24, 0b11111111, 0b00000000, 8, 0), (25, 0b11000000, 0b00111111, 2, 6)]

    class FrntRiDoorRdrObj16RdrObjDstZ:
        sig_name = "FrntRiDoorRdrObj16RdrObjDstZ"
        sig_start_bit = 259
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 259
        bmuws_info = [(32, 0b00001111, 0b11110000, 4, 0), (33, 0b11111100, 0b00000011, 6, 2)]

    class FrntRiDoorRdrObj11RdrObjV:
        sig_name = "FrntRiDoorRdrObj11RdrObjV"
        sig_start_bit = 25
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -2000
        sig_value_max = 2000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 25
        bmuws_info = [(3, 0b00000011, 0b11111100, 2, 0), (4, 0b11111111, 0b00000000, 8, 0), (5, 0b11000000, 0b00111111, 2, 6)]

    class FrntRiDoorRdrObj11RdrObjDstX:
        sig_name = "FrntRiDoorRdrObj11RdrObjDstX"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class FrntRiDoorRdrObj14RdrObjDstY:
        sig_name = "FrntRiDoorRdrObj14RdrObjDstY"
        sig_start_bit = 157
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 157
        bmuws_info = [(19, 0b00111111, 0b11000000, 6, 0), (20, 0b11110000, 0b00001111, 4, 4)]

    class FrntRiDoorRdrObj13RdrObjDstX:
        sig_name = "FrntRiDoorRdrObj13RdrObjDstX"
        sig_start_bit = 103
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 103
        bmuws_info = [(12, 0b11111111, 0b00000000, 8, 0), (13, 0b11000000, 0b00111111, 2, 6)]

    class FrntRiDoorRdrObj13_UB:
        sig_name = "FrntRiDoorRdrObj13_UB"
        sig_start_bit = 141
        update_id_bit = 141
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
        startbit = 141
        byte = 17
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class FrntRiDoorRdrObj11_UB:
        sig_name = "FrntRiDoorRdrObj11_UB"
        sig_start_bit = 45
        update_id_bit = 45
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
        startbit = 45
        byte = 5
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class FrntRiDoorRdrObj16_UB:
        sig_name = "FrntRiDoorRdrObj16_UB"
        sig_start_bit = 285
        update_id_bit = 285
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
        startbit = 285
        byte = 35
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class FrntRiDoorRdrObj13RdrObjV:
        sig_name = "FrntRiDoorRdrObj13RdrObjV"
        sig_start_bit = 121
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -2000
        sig_value_max = 2000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 121
        bmuws_info = [(15, 0b00000011, 0b11111100, 2, 0), (16, 0b11111111, 0b00000000, 8, 0), (17, 0b11000000, 0b00111111, 2, 6)]

    class FrntRiDoorRdrObj15RdrObjV:
        sig_name = "FrntRiDoorRdrObj15RdrObjV"
        sig_start_bit = 217
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -2000
        sig_value_max = 2000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 217
        bmuws_info = [(27, 0b00000011, 0b11111100, 2, 0), (28, 0b11111111, 0b00000000, 8, 0), (29, 0b11000000, 0b00111111, 2, 6)]

    class FrntRiDoorRdrObj12_UB:
        sig_name = "FrntRiDoorRdrObj12_UB"
        sig_start_bit = 93
        update_id_bit = 93
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
        startbit = 93
        byte = 11
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class FrntRiDoorRdrObj16RdrObjDstY:
        sig_name = "FrntRiDoorRdrObj16RdrObjDstY"
        sig_start_bit = 253
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 253
        bmuws_info = [(31, 0b00111111, 0b11000000, 6, 0), (32, 0b11110000, 0b00001111, 4, 4)]

    class FrntRiDoorRdrObj12RdrObjDstZ:
        sig_name = "FrntRiDoorRdrObj12RdrObjDstZ"
        sig_start_bit = 67
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 67
        bmuws_info = [(8, 0b00001111, 0b11110000, 4, 0), (9, 0b11111100, 0b00000011, 6, 2)]

    class FrntRiDoorRdrObj11RdrObjDstY:
        sig_name = "FrntRiDoorRdrObj11RdrObjDstY"
        sig_start_bit = 13
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 13
        bmuws_info = [(1, 0b00111111, 0b11000000, 6, 0), (2, 0b11110000, 0b00001111, 4, 4)]

    class FrntRiDoorRdrObj14RdrObjDstX:
        sig_name = "FrntRiDoorRdrObj14RdrObjDstX"
        sig_start_bit = 151
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 151
        bmuws_info = [(18, 0b11111111, 0b00000000, 8, 0), (19, 0b11000000, 0b00111111, 2, 6)]

    class FrntRiDoorRdrObj15_UB:
        sig_name = "FrntRiDoorRdrObj15_UB"
        sig_start_bit = 237
        update_id_bit = 237
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
        startbit = 237
        byte = 29
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class FrntRiDoorRdrObj12RdrObjV:
        sig_name = "FrntRiDoorRdrObj12RdrObjV"
        sig_start_bit = 73
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -2000
        sig_value_max = 2000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 73
        bmuws_info = [(9, 0b00000011, 0b11111100, 2, 0), (10, 0b11111111, 0b00000000, 8, 0), (11, 0b11000000, 0b00111111, 2, 6)]

    class FrntRiDoorRdrObj13RdrObjDstZ:
        sig_name = "FrntRiDoorRdrObj13RdrObjDstZ"
        sig_start_bit = 115
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 115
        bmuws_info = [(14, 0b00001111, 0b11110000, 4, 0), (15, 0b11111100, 0b00000011, 6, 2)]

    class FrntRiDoorRdrObj13RdrObjDstY:
        sig_name = "FrntRiDoorRdrObj13RdrObjDstY"
        sig_start_bit = 109
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 109
        bmuws_info = [(13, 0b00111111, 0b11000000, 6, 0), (14, 0b11110000, 0b00001111, 4, 4)]

    class FrntRiDoorRdrObj14_UB:
        sig_name = "FrntRiDoorRdrObj14_UB"
        sig_start_bit = 189
        update_id_bit = 189
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
        startbit = 189
        byte = 23
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class FrntRiDoorRdrObj14RdrObjDstZ:
        sig_name = "FrntRiDoorRdrObj14RdrObjDstZ"
        sig_start_bit = 163
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 163
        bmuws_info = [(20, 0b00001111, 0b11110000, 4, 0), (21, 0b11111100, 0b00000011, 6, 2)]

    class FrntRiDoorRdrObj15RdrObjDstY:
        sig_name = "FrntRiDoorRdrObj15RdrObjDstY"
        sig_start_bit = 205
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 205
        bmuws_info = [(25, 0b00111111, 0b11000000, 6, 0), (26, 0b11110000, 0b00001111, 4, 4)]

    class FrntRiDoorRdrObj12RdrObjDstY:
        sig_name = "FrntRiDoorRdrObj12RdrObjDstY"
        sig_start_bit = 61
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 61
        bmuws_info = [(7, 0b00111111, 0b11000000, 6, 0), (8, 0b11110000, 0b00001111, 4, 4)]

    class FrntRiDoorRdrObj16RdrObjDstX:
        sig_name = "FrntRiDoorRdrObj16RdrObjDstX"
        sig_start_bit = 247
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 247
        bmuws_info = [(30, 0b11111111, 0b00000000, 8, 0), (31, 0b11000000, 0b00111111, 2, 6)]

    class FrntRiDoorRdrObj14RdrObjV:
        sig_name = "FrntRiDoorRdrObj14RdrObjV"
        sig_start_bit = 169
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -2000
        sig_value_max = 2000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 169
        bmuws_info = [(21, 0b00000011, 0b11111100, 2, 0), (22, 0b11111111, 0b00000000, 8, 0), (23, 0b11000000, 0b00111111, 2, 6)]


class LCURToDRMRRLCURCANFD1DiagReqFrame:
    msg_name = "LCURToDRMRRLCURCANFD1DiagReqFrame"
    msg_id = 1843
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "LCUR"
    rx_nodes = ['DRMRR']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class LCURLCURCANFD1Fr07:
    msg_name = "LCURLCURCANFD1Fr07"
    msg_id = 2
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "LCUR"
    rx_nodes = ['DRMFR', 'DRMRR']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class ReRiDoorRdrModReq:
        sig_name = "ReRiDoorRdrModReq"
        sig_start_bit = 5
        update_id_bit = 2
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorRdrModReq_NormalModeRequest': 0, 'DoorRdrModReq_ParkingModeRequest': 1}
        compute_method = None
        length = 2
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class FrntRiDoorRdrModReq:
        sig_name = "FrntRiDoorRdrModReq"
        sig_start_bit = 7
        update_id_bit = 3
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorRdrModReq_NormalModeRequest': 0, 'DoorRdrModReq_ParkingModeRequest': 1}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class LCURLCURCANFD1NmFr:
    msg_name = "LCURLCURCANFD1NmFr"
    msg_id = 1284
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "LCUR"
    rx_nodes = ['DRMRR']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class RPODLCURCANFD1Fr02:
    msg_name = "RPODLCURCANFD1Fr02"
    msg_id = 661
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 64
    tx_node = "RPOD"
    rx_nodes = ['LCUR']
    sig_group_dict = {'RRPwrDoorErrFb': ['RRPwrDoorErrFbBoolean', 'RRPwrDoorErrFbHallErrFb', 'RRPwrDoorErrFbMotThermErrFb', 'RRPwrDoorErrFbPosnUnknowFb', 'RRPwrDoorErrFbRollAngErrFb']}
    sig_group_dataid_dict = {}

    class RRPwrDoorErrFbHallErrFb:
        sig_name = "RRPwrDoorErrFbHallErrFb"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 16
        byte = 2
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class RRPwrDoorErrFbBoolean:
        sig_name = "RRPwrDoorErrFbBoolean"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 18
        byte = 2
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class RRPwrDoorErrFb_UB:
        sig_name = "RRPwrDoorErrFb_UB"
        sig_start_bit = 1
        update_id_bit = 1
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
        startbit = 1
        byte = 0
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class RRDoorOpenTrigSrc:
        sig_name = "RRDoorOpenTrigSrc"
        sig_start_bit = 30
        update_id_bit = 0
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 9
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorCtrlTriSrc_NoTrigSrc': 0, 'DoorCtrlTriSrc_InsdSwt': 1, 'DoorCtrlTriSrc_OutdSwt': 2, 'DoorCtrlTriSrc_NFC': 3, 'DoorCtrlTriSrc_Aproch': 4, 'DoorCtrlTriSrc_OutdCtrl': 5, 'DoorCtrlTriSrc_InsdCtrl': 6, 'DoorCtrlTriSrc_Resd1': 7, 'DoorCtrlTriSrc_Resd2': 8, 'DoorCtrlTriSrc_Resd3': 9}
        compute_method = None
        length = 4
        startbit = 30
        byte = 3
        mask = 0b01111000
        unmask = 0b10000111
        shift = 3

    class RRPwrDoorErrFbPosnUnknowFb:
        sig_name = "RRPwrDoorErrFbPosnUnknowFb"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 17
        byte = 2
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class RRDoorManResistSts:
        sig_name = "RRDoorManResistSts"
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
        sig_value_table = {'DoorManResistsSts_NoResist': 0, 'DoorManResistsSts_Level1': 1, 'DoorManResistsSts_Level2': 2}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class RRPwrDoorErrFbMotThermErrFb:
        sig_name = "RRPwrDoorErrFbMotThermErrFb"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 31
        byte = 3
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class RRDoorSpdModeFb:
        sig_name = "RRDoorSpdModeFb"
        sig_start_bit = 21
        update_id_bit = 2
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SpdMode_Low': 0, 'SpdMode_Middle': 1, 'SpdMode_High': 2}
        compute_method = None
        length = 2
        startbit = 21
        byte = 2
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class RRDoorMaxPosnSetFb:
        sig_name = "RRDoorMaxPosnSetFb"
        sig_start_bit = 15
        update_id_bit = 4
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RRDoorModSts:
        sig_name = "RRDoorModSts"
        sig_start_bit = 23
        update_id_bit = 3
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorModSts_ElecMode': 0, 'DoorModSts_ManualMode': 1}
        compute_method = None
        length = 2
        startbit = 23
        byte = 2
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class RRPwrDoorErrFbRollAngErrFb:
        sig_name = "RRPwrDoorErrFbRollAngErrFb"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 19
        byte = 2
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3


class DRMFRToLCURLCURCANFD1DiagRespFrame:
    msg_name = "DRMFRToLCURLCURCANFD1DiagRespFrame"
    msg_id = 1585
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "DRMFR"
    rx_nodes = ['LCUR']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class LCURToAllLCURCANFD1DiagFuncReqFrame:
    msg_name = "LCURToAllLCURCANFD1DiagFuncReqFrame"
    msg_id = 2047
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "LCUR"
    rx_nodes = ['PPOD', 'DRMRR', 'RPOD', 'DRMFR']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class DRMFRLCURCANFD1NmFr:
    msg_name = "DRMFRLCURCANFD1NmFr"
    msg_id = 1281
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "DRMFR"
    rx_nodes = ['RPOD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class LCURLCURCANFD1Fr04:
    msg_name = "LCURLCURCANFD1Fr04"
    msg_id = 405
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 64
    tx_node = "LCUR"
    rx_nodes = ['PPOD', 'DRMRR', 'RPOD', 'DRMFR']
    sig_group_dict = {'RRPwrSideDoorCtrlReq': ['RRPwrSideDoorCtrlReqChks', 'RRPwrSideDoorCtrlReqCntr', 'RRPwrSideDoorCtrlReqPwrSideDoorCtrlReq', 'RRPwrSideDoorCtrlReqPwrSideDoorCtrlTrigSrc'], 'SeatOccpSts': ['SeatOccpStsDrvrSeatSts', 'SeatOccpStsPassSeatSts', 'SeatOccpStsSecRowLeSeatSts', 'SeatOccpStsSecRowMidSeatSts', 'SeatOccpStsSecRowRiSeatSts', 'SeatOccpStsThrdRowLeSeatSts', 'SeatOccpStsThrdRowMidSeatSts', 'SeatOccpStsThrdRowRiSeatSts'], 'Odometer': ['OdometerValidity', 'OdometerValue'], 'RRPwrSideDoorPosnSet': ['RRPwrSideDoorPosnSetChks', 'RRPwrSideDoorPosnSetCntr', 'RRPwrSideDoorPosnSetPosnCtrl', 'RRPwrSideDoorPosnSetPosnCtrlSrc'], 'FRPwrSideDoorPosnSet': ['FRPwrSideDoorPosnSetChks', 'FRPwrSideDoorPosnSetCntr', 'FRPwrSideDoorPosnSetPosnCtrl', 'FRPwrSideDoorPosnSetPosnCtrlSrc'], 'FRPwrSideDoorCtrlReq': ['FRPwrSideDoorCtrlReqChks', 'FRPwrSideDoorCtrlReqCntr', 'FRPwrSideDoorCtrlReqPwrSideDoorCtrlReq', 'FRPwrSideDoorCtrlReqPwrSideDoorCtrlTrigSrc']}
    sig_group_dataid_dict = {}

    class SeatOccpStsDrvrSeatSts:
        sig_name = "SeatOccpStsDrvrSeatSts"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 199
        byte = 24
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class SeatOccpStsThrdRowMidSeatSts:
        sig_name = "SeatOccpStsThrdRowMidSeatSts"
        sig_start_bit = 193
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
        startbit = 193
        byte = 24
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VehBattU:
        sig_name = "VehBattU"
        sig_start_bit = 143
        update_id_bit = 156
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
        startbit = 143
        bmuws_info = [(17, 0b11111111, 0b00000000, 8, 0), (18, 0b11000000, 0b00111111, 2, 6)]

    class SeatOccpStsThrdRowLeSeatSts:
        sig_name = "SeatOccpStsThrdRowLeSeatSts"
        sig_start_bit = 194
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
        startbit = 194
        byte = 24
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class RRPwrSideDoorPosnSetPosnCtrlSrc:
        sig_name = "RRPwrSideDoorPosnSetPosnCtrlSrc"
        sig_start_bit = 219
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CtrlTrigsrc_NoCtrlReq': 0, 'CtrlTrigsrc_OutdCtrl': 1, 'CtrlTrigsrc_InsdCtrl': 2}
        compute_method = None
        length = 2
        startbit = 219
        byte = 27
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class SeatOccpStsSecRowMidSeatSts:
        sig_name = "SeatOccpStsSecRowMidSeatSts"
        sig_start_bit = 196
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
        startbit = 196
        byte = 24
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class RRPwrSideDoorCtrlReq_UB:
        sig_name = "RRPwrSideDoorCtrlReq_UB"
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

    class SeatOccpSts_UB:
        sig_name = "SeatOccpSts_UB"
        sig_start_bit = 81
        update_id_bit = 81
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
        startbit = 81
        byte = 10
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class FRPwrSideDoorCtrlReqChks:
        sig_name = "FRPwrSideDoorCtrlReqChks"
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

    class RRPwrSideDoorCtrlReqChks:
        sig_name = "RRPwrSideDoorCtrlReqChks"
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

    class FRPwrSideDoorPosnSetPosnCtrlSrc:
        sig_name = "FRPwrSideDoorPosnSetPosnCtrlSrc"
        sig_start_bit = 153
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CtrlTrigsrc_NoCtrlReq': 0, 'CtrlTrigsrc_OutdCtrl': 1, 'CtrlTrigsrc_InsdCtrl': 2}
        compute_method = None
        length = 2
        startbit = 153
        byte = 19
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class RRRdrEnadCtrlReq:
        sig_name = "RRRdrEnadCtrlReq"
        sig_start_bit = 159
        update_id_bit = 157
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
        startbit = 159
        byte = 19
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class PwrSideDoorModeSet:
        sig_name = "PwrSideDoorModeSet"
        sig_start_bit = 84
        update_id_bit = 148
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorModSts_ElecMode': 0, 'DoorModSts_ManualMode': 1}
        compute_method = None
        length = 2
        startbit = 84
        byte = 10
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class SeatOccpStsSecRowRiSeatSts:
        sig_name = "SeatOccpStsSecRowRiSeatSts"
        sig_start_bit = 195
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
        startbit = 195
        byte = 24
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class FRPwrSideDoorMaxPosnSet:
        sig_name = "FRPwrSideDoorMaxPosnSet"
        sig_start_bit = 31
        update_id_bit = 16
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class Odometer_UB:
        sig_name = "Odometer_UB"
        sig_start_bit = 149
        update_id_bit = 149
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
        startbit = 149
        byte = 18
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class RRPwrSideDoorPosnSetChks:
        sig_name = "RRPwrSideDoorPosnSetChks"
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

    class FRRdrEnadCtrlReq:
        sig_name = "FRRdrEnadCtrlReq"
        sig_start_bit = 82
        update_id_bit = 80
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
        startbit = 82
        byte = 10
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class RRPwrSideDoorPosnSet_UB:
        sig_name = "RRPwrSideDoorPosnSet_UB"
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

    class FRPwrSideDoorPosnSetPosnCtrl:
        sig_name = "FRPwrSideDoorPosnSetPosnCtrl"
        sig_start_bit = 175
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
        startbit = 175
        byte = 21
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RRPwrSideDoorPosnSetPosnCtrl:
        sig_name = "RRPwrSideDoorPosnSetPosnCtrl"
        sig_start_bit = 215
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
        startbit = 215
        byte = 26
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RRPwrSideDoorCtrlReqPwrSideDoorCtrlTrigSrc:
        sig_name = "RRPwrSideDoorCtrlReqPwrSideDoorCtrlTrigSrc"
        sig_start_bit = 75
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 9
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorCtrlTriSrc_NoTrigSrc': 0, 'DoorCtrlTriSrc_InsdSwt': 1, 'DoorCtrlTriSrc_OutdSwt': 2, 'DoorCtrlTriSrc_NFC': 3, 'DoorCtrlTriSrc_Aproch': 4, 'DoorCtrlTriSrc_OutdCtrl': 5, 'DoorCtrlTriSrc_InsdCtrl': 6, 'DoorCtrlTriSrc_Resd1': 7, 'DoorCtrlTriSrc_Resd2': 8, 'DoorCtrlTriSrc_Resd3': 9}
        compute_method = None
        length = 4
        startbit = 75
        byte = 9
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class VehTiGlb:
        sig_name = "VehTiGlb"
        sig_start_bit = 111
        update_id_bit = 155
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
        startbit = 111
        bmuws_info = [(13, 0b11111111, 0b00000000, 8, 0), (14, 0b11111111, 0b00000000, 8, 0), (15, 0b11111111, 0b00000000, 8, 0), (16, 0b11111111, 0b00000000, 8, 0)]

    class OdometerValidity:
        sig_name = "OdometerValidity"
        sig_start_bit = 58
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
        startbit = 58
        byte = 7
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class RRPwrSideDoorCtrlReqPwrSideDoorCtrlReq:
        sig_name = "RRPwrSideDoorCtrlReqPwrSideDoorCtrlReq"
        sig_start_bit = 87
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorCtrlReq_Idle': 0, 'DoorCtrlReq_Open': 1, 'DoorCtrlReq_Close': 2, 'DoorCtrlReq_Stop': 3, 'DoorCtrlReq_OpenMinAng': 4, 'DoorCtrlReq_Resd2': 5}
        compute_method = None
        length = 3
        startbit = 87
        byte = 10
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class SeatOccpStsThrdRowRiSeatSts:
        sig_name = "SeatOccpStsThrdRowRiSeatSts"
        sig_start_bit = 192
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
        startbit = 192
        byte = 24
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FLRdrEnadCtrlReq:
        sig_name = "FLRdrEnadCtrlReq"
        sig_start_bit = 57
        update_id_bit = 56
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
        startbit = 57
        byte = 7
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class RRPwrSideDoorCtrlReqCntr:
        sig_name = "RRPwrSideDoorCtrlReqCntr"
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

    class FRPwrSideDoorPosnSetChks:
        sig_name = "FRPwrSideDoorPosnSetChks"
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

    class FRPwrSideDoorPosnSet_UB:
        sig_name = "FRPwrSideDoorPosnSet_UB"
        sig_start_bit = 154
        update_id_bit = 154
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
        startbit = 154
        byte = 19
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class RLRdrEnadCtrlReq:
        sig_name = "RLRdrEnadCtrlReq"
        sig_start_bit = 144
        update_id_bit = 158
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
        startbit = 144
        byte = 18
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FRPwrSideDoorCtrlReq_UB:
        sig_name = "FRPwrSideDoorCtrlReq_UB"
        sig_start_bit = 4
        update_id_bit = 4
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
        startbit = 4
        byte = 0
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class RRPwrSideDoorPosnSetCntr:
        sig_name = "RRPwrSideDoorPosnSetCntr"
        sig_start_bit = 223
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
        startbit = 223
        byte = 27
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class SeatOccpStsSecRowLeSeatSts:
        sig_name = "SeatOccpStsSecRowLeSeatSts"
        sig_start_bit = 197
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
        startbit = 197
        byte = 24
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class FRPwrSideDoorCtrlReqCntr:
        sig_name = "FRPwrSideDoorCtrlReqCntr"
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

    class FRPwrSideDoorPosnSetCntr:
        sig_name = "FRPwrSideDoorPosnSetCntr"
        sig_start_bit = 183
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
        startbit = 183
        byte = 22
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class RRPwrSideDoorMaxPosnSet:
        sig_name = "RRPwrSideDoorMaxPosnSet"
        sig_start_bit = 39
        update_id_bit = 146
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
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SeatOccpStsPassSeatSts:
        sig_name = "SeatOccpStsPassSeatSts"
        sig_start_bit = 198
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
        startbit = 198
        byte = 24
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class FRPwrSideDoorCtrlReqPwrSideDoorCtrlTrigSrc:
        sig_name = "FRPwrSideDoorCtrlReqPwrSideDoorCtrlTrigSrc"
        sig_start_bit = 20
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 9
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorCtrlTriSrc_NoTrigSrc': 0, 'DoorCtrlTriSrc_InsdSwt': 1, 'DoorCtrlTriSrc_OutdSwt': 2, 'DoorCtrlTriSrc_NFC': 3, 'DoorCtrlTriSrc_Aproch': 4, 'DoorCtrlTriSrc_OutdCtrl': 5, 'DoorCtrlTriSrc_InsdCtrl': 6, 'DoorCtrlTriSrc_Resd1': 7, 'DoorCtrlTriSrc_Resd2': 8, 'DoorCtrlTriSrc_Resd3': 9}
        compute_method = None
        length = 4
        startbit = 20
        byte = 2
        mask = 0b00011110
        unmask = 0b11100001
        shift = 1

    class FRPwrSideDoorCtrlReqPwrSideDoorCtrlReq:
        sig_name = "FRPwrSideDoorCtrlReqPwrSideDoorCtrlReq"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorCtrlReq_Idle': 0, 'DoorCtrlReq_Open': 1, 'DoorCtrlReq_Close': 2, 'DoorCtrlReq_Stop': 3, 'DoorCtrlReq_OpenMinAng': 4, 'DoorCtrlReq_Resd2': 5}
        compute_method = None
        length = 3
        startbit = 23
        byte = 2
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DoorSpdModeSet:
        sig_name = "DoorSpdModeSet"
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
        sig_value_table = {'SpdMode_Low': 0, 'SpdMode_Middle': 1, 'SpdMode_High': 2}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class OdometerValue:
        sig_name = "OdometerValue"
        sig_start_bit = 47
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
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111000, 0b00000111, 5, 3)]


class PPODToLCURLCURCANFD1DiagRespFrame:
    msg_name = "PPODToLCURLCURCANFD1DiagRespFrame"
    msg_id = 1601
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "PPOD"
    rx_nodes = ['LCUR']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class DRMRRLCURCANFD1Fr03:
    msg_name = "DRMRRLCURCANFD1Fr03"
    msg_id = 404
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 64
    tx_node = "DRMRR"
    rx_nodes = ['LCUR']
    sig_group_dict = {'ReRiDoorRdrObj13': ['ReRiDoorRdrObj13RdrObjDstX', 'ReRiDoorRdrObj13RdrObjDstY', 'ReRiDoorRdrObj13RdrObjDstZ', 'ReRiDoorRdrObj13RdrObjV'], 'ReRiDoorRdrObj16': ['ReRiDoorRdrObj16RdrObjDstX', 'ReRiDoorRdrObj16RdrObjDstY', 'ReRiDoorRdrObj16RdrObjDstZ', 'ReRiDoorRdrObj16RdrObjV'], 'ReRiDoorRdrObj14': ['ReRiDoorRdrObj14RdrObjDstX', 'ReRiDoorRdrObj14RdrObjDstY', 'ReRiDoorRdrObj14RdrObjDstZ', 'ReRiDoorRdrObj14RdrObjV'], 'ReRiDoorRdrObj12': ['ReRiDoorRdrObj12RdrObjDstX', 'ReRiDoorRdrObj12RdrObjDstY', 'ReRiDoorRdrObj12RdrObjDstZ', 'ReRiDoorRdrObj12RdrObjV'], 'ReRiDoorRdrObj15': ['ReRiDoorRdrObj15RdrObjDstX', 'ReRiDoorRdrObj15RdrObjDstY', 'ReRiDoorRdrObj15RdrObjDstZ', 'ReRiDoorRdrObj15RdrObjV'], 'ReRiDoorRdrObj11': ['ReRiDoorRdrObj11RdrObjDstX', 'ReRiDoorRdrObj11RdrObjDstY', 'ReRiDoorRdrObj11RdrObjDstZ', 'ReRiDoorRdrObj11RdrObjV']}
    sig_group_dataid_dict = {}

    class ReRiDoorRdrObj11RdrObjDstZ:
        sig_name = "ReRiDoorRdrObj11RdrObjDstZ"
        sig_start_bit = 19
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 19
        bmuws_info = [(2, 0b00001111, 0b11110000, 4, 0), (3, 0b11111100, 0b00000011, 6, 2)]

    class ReRiDoorRdrObj15RdrObjV:
        sig_name = "ReRiDoorRdrObj15RdrObjV"
        sig_start_bit = 217
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -2000
        sig_value_max = 2000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 217
        bmuws_info = [(27, 0b00000011, 0b11111100, 2, 0), (28, 0b11111111, 0b00000000, 8, 0), (29, 0b11000000, 0b00111111, 2, 6)]

    class ReRiDoorRdrObj15RdrObjDstY:
        sig_name = "ReRiDoorRdrObj15RdrObjDstY"
        sig_start_bit = 205
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 205
        bmuws_info = [(25, 0b00111111, 0b11000000, 6, 0), (26, 0b11110000, 0b00001111, 4, 4)]

    class ReRiDoorRdrObj11RdrObjDstX:
        sig_name = "ReRiDoorRdrObj11RdrObjDstX"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class ReRiDoorRdrObj14RdrObjDstX:
        sig_name = "ReRiDoorRdrObj14RdrObjDstX"
        sig_start_bit = 151
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 151
        bmuws_info = [(18, 0b11111111, 0b00000000, 8, 0), (19, 0b11000000, 0b00111111, 2, 6)]

    class ReRiDoorRdrObj12RdrObjDstZ:
        sig_name = "ReRiDoorRdrObj12RdrObjDstZ"
        sig_start_bit = 67
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 67
        bmuws_info = [(8, 0b00001111, 0b11110000, 4, 0), (9, 0b11111100, 0b00000011, 6, 2)]

    class ReRiDoorRdrObj11RdrObjV:
        sig_name = "ReRiDoorRdrObj11RdrObjV"
        sig_start_bit = 25
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -2000
        sig_value_max = 2000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 25
        bmuws_info = [(3, 0b00000011, 0b11111100, 2, 0), (4, 0b11111111, 0b00000000, 8, 0), (5, 0b11000000, 0b00111111, 2, 6)]

    class ReRiDoorRdrObj15RdrObjDstX:
        sig_name = "ReRiDoorRdrObj15RdrObjDstX"
        sig_start_bit = 199
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 199
        bmuws_info = [(24, 0b11111111, 0b00000000, 8, 0), (25, 0b11000000, 0b00111111, 2, 6)]

    class ReRiDoorRdrObj13_UB:
        sig_name = "ReRiDoorRdrObj13_UB"
        sig_start_bit = 141
        update_id_bit = 141
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
        startbit = 141
        byte = 17
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class ReRiDoorRdrObj14RdrObjDstZ:
        sig_name = "ReRiDoorRdrObj14RdrObjDstZ"
        sig_start_bit = 163
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 163
        bmuws_info = [(20, 0b00001111, 0b11110000, 4, 0), (21, 0b11111100, 0b00000011, 6, 2)]

    class ReRiDoorRdrObj16RdrObjDstY:
        sig_name = "ReRiDoorRdrObj16RdrObjDstY"
        sig_start_bit = 253
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 253
        bmuws_info = [(31, 0b00111111, 0b11000000, 6, 0), (32, 0b11110000, 0b00001111, 4, 4)]

    class ReRiDoorRdrObj15RdrObjDstZ:
        sig_name = "ReRiDoorRdrObj15RdrObjDstZ"
        sig_start_bit = 211
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 211
        bmuws_info = [(26, 0b00001111, 0b11110000, 4, 0), (27, 0b11111100, 0b00000011, 6, 2)]

    class ReRiDoorRdrObj16RdrObjV:
        sig_name = "ReRiDoorRdrObj16RdrObjV"
        sig_start_bit = 265
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -2000
        sig_value_max = 2000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 265
        bmuws_info = [(33, 0b00000011, 0b11111100, 2, 0), (34, 0b11111111, 0b00000000, 8, 0), (35, 0b11000000, 0b00111111, 2, 6)]

    class ReRiDoorRdrObj16_UB:
        sig_name = "ReRiDoorRdrObj16_UB"
        sig_start_bit = 285
        update_id_bit = 285
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
        startbit = 285
        byte = 35
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class ReRiDoorRdrObj12RdrObjDstX:
        sig_name = "ReRiDoorRdrObj12RdrObjDstX"
        sig_start_bit = 55
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 55
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b11000000, 0b00111111, 2, 6)]

    class ReRiDoorRdrObj13RdrObjV:
        sig_name = "ReRiDoorRdrObj13RdrObjV"
        sig_start_bit = 121
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -2000
        sig_value_max = 2000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 121
        bmuws_info = [(15, 0b00000011, 0b11111100, 2, 0), (16, 0b11111111, 0b00000000, 8, 0), (17, 0b11000000, 0b00111111, 2, 6)]

    class ReRiDoorRdrObj13RdrObjDstY:
        sig_name = "ReRiDoorRdrObj13RdrObjDstY"
        sig_start_bit = 109
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 109
        bmuws_info = [(13, 0b00111111, 0b11000000, 6, 0), (14, 0b11110000, 0b00001111, 4, 4)]

    class ReRiDoorRdrObj16RdrObjDstZ:
        sig_name = "ReRiDoorRdrObj16RdrObjDstZ"
        sig_start_bit = 259
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 259
        bmuws_info = [(32, 0b00001111, 0b11110000, 4, 0), (33, 0b11111100, 0b00000011, 6, 2)]

    class ReRiDoorRdrObj14_UB:
        sig_name = "ReRiDoorRdrObj14_UB"
        sig_start_bit = 189
        update_id_bit = 189
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
        startbit = 189
        byte = 23
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class ReRiDoorRdrObj14RdrObjV:
        sig_name = "ReRiDoorRdrObj14RdrObjV"
        sig_start_bit = 169
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -2000
        sig_value_max = 2000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 169
        bmuws_info = [(21, 0b00000011, 0b11111100, 2, 0), (22, 0b11111111, 0b00000000, 8, 0), (23, 0b11000000, 0b00111111, 2, 6)]

    class ReRiDoorRdrObj14RdrObjDstY:
        sig_name = "ReRiDoorRdrObj14RdrObjDstY"
        sig_start_bit = 157
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 157
        bmuws_info = [(19, 0b00111111, 0b11000000, 6, 0), (20, 0b11110000, 0b00001111, 4, 4)]

    class ReRiDoorRdrObj12_UB:
        sig_name = "ReRiDoorRdrObj12_UB"
        sig_start_bit = 93
        update_id_bit = 93
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
        startbit = 93
        byte = 11
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class ReRiDoorRdrObj16RdrObjDstX:
        sig_name = "ReRiDoorRdrObj16RdrObjDstX"
        sig_start_bit = 247
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 247
        bmuws_info = [(30, 0b11111111, 0b00000000, 8, 0), (31, 0b11000000, 0b00111111, 2, 6)]

    class ReRiDoorRdrObj15_UB:
        sig_name = "ReRiDoorRdrObj15_UB"
        sig_start_bit = 237
        update_id_bit = 237
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
        startbit = 237
        byte = 29
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class ReRiDoorRdrObj12RdrObjDstY:
        sig_name = "ReRiDoorRdrObj12RdrObjDstY"
        sig_start_bit = 61
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 61
        bmuws_info = [(7, 0b00111111, 0b11000000, 6, 0), (8, 0b11110000, 0b00001111, 4, 4)]

    class ReRiDoorRdrObj13RdrObjDstZ:
        sig_name = "ReRiDoorRdrObj13RdrObjDstZ"
        sig_start_bit = 115
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 115
        bmuws_info = [(14, 0b00001111, 0b11110000, 4, 0), (15, 0b11111100, 0b00000011, 6, 2)]

    class ReRiDoorRdrObj11_UB:
        sig_name = "ReRiDoorRdrObj11_UB"
        sig_start_bit = 45
        update_id_bit = 45
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
        startbit = 45
        byte = 5
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class ReRiDoorRdrObj12RdrObjV:
        sig_name = "ReRiDoorRdrObj12RdrObjV"
        sig_start_bit = 73
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -2000
        sig_value_max = 2000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 73
        bmuws_info = [(9, 0b00000011, 0b11111100, 2, 0), (10, 0b11111111, 0b00000000, 8, 0), (11, 0b11000000, 0b00111111, 2, 6)]

    class ReRiDoorRdrObj13RdrObjDstX:
        sig_name = "ReRiDoorRdrObj13RdrObjDstX"
        sig_start_bit = 103
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 103
        bmuws_info = [(12, 0b11111111, 0b00000000, 8, 0), (13, 0b11000000, 0b00111111, 2, 6)]

    class ReRiDoorRdrObj11RdrObjDstY:
        sig_name = "ReRiDoorRdrObj11RdrObjDstY"
        sig_start_bit = 13
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0
        sig_value_min = -1000
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 13
        bmuws_info = [(1, 0b00111111, 0b11000000, 6, 0), (2, 0b11110000, 0b00001111, 4, 4)]


class LCURLCURCANFD1Fr03:
    msg_name = "LCURLCURCANFD1Fr03"
    msg_id = 304
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.04
    msg_length = 64
    tx_node = "LCUR"
    rx_nodes = ['RPOD', 'PPOD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class FLLtchPosn:
        sig_name = "FLLtchPosn"
        sig_start_bit = 7
        update_id_bit = 15
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
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class RRLtchPosn:
        sig_name = "RRLtchPosn"
        sig_start_bit = 1
        update_id_bit = 12
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
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class FRLtchPosn:
        sig_name = "FRLtchPosn"
        sig_start_bit = 5
        update_id_bit = 14
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
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class RLLtchPosn:
        sig_name = "RLLtchPosn"
        sig_start_bit = 3
        update_id_bit = 13
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


class LCURLCURCANFD1Fr06:
    msg_name = "LCURLCURCANFD1Fr06"
    msg_id = 659
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 64
    tx_node = "LCUR"
    rx_nodes = ['PPOD', 'ETC', 'RPOD']
    sig_group_dict = {'CmptmtAirFlwEstimd': ['CmptmtAirFlwEstimdFrnt', 'CmptmtAirFlwEstimdRe']}
    sig_group_dataid_dict = {}

    class CmptmtAirFlwEstimdRe:
        sig_name = "CmptmtAirFlwEstimdRe"
        sig_start_bit = 9
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 9
        bmuws_info = [(1, 0b00000011, 0b11111100, 2, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class RecircRat:
        sig_name = "RecircRat"
        sig_start_bit = 271
        update_id_bit = 232
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 271
        bmuws_info = [(33, 0b11111111, 0b00000000, 8, 0), (34, 0b11000000, 0b00111111, 2, 6)]

    class FRDoorManResistCtrl:
        sig_name = "FRDoorManResistCtrl"
        sig_start_bit = 239
        update_id_bit = 234
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorManResistCmd_Idle': 0, 'DoorManResistCmd_AddLevel1Cmd': 1, 'DoorManResistCmd_AddLevel2Cmd': 2, 'DoorManResistCmd_SubCmd': 3}
        compute_method = None
        length = 2
        startbit = 239
        byte = 29
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class RRDoorManResistCtrl:
        sig_name = "RRDoorManResistCtrl"
        sig_start_bit = 237
        update_id_bit = 283
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorManResistCmd_Idle': 0, 'DoorManResistCmd_AddLevel1Cmd': 1, 'DoorManResistCmd_AddLevel2Cmd': 2, 'DoorManResistCmd_SubCmd': 3}
        compute_method = None
        length = 2
        startbit = 237
        byte = 29
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class WinReRiRippleCntr:
        sig_name = "WinReRiRippleCntr"
        sig_start_bit = 251
        update_id_bit = 284
        sig_length = 12
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 251
        bmuws_info = [(31, 0b00001111, 0b11110000, 4, 0), (32, 0b11111111, 0b00000000, 8, 0)]

    class CmptmtAirFlwEstimd_UB:
        sig_name = "CmptmtAirFlwEstimd_UB"
        sig_start_bit = 235
        update_id_bit = 235
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
        startbit = 235
        byte = 29
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class WinPassRippleCntr:
        sig_name = "WinPassRippleCntr"
        sig_start_bit = 247
        update_id_bit = 285
        sig_length = 12
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 247
        bmuws_info = [(30, 0b11111111, 0b00000000, 8, 0), (31, 0b11110000, 0b00001111, 4, 4)]

    class CmptmtAirFlwEstimdFrnt:
        sig_name = "CmptmtAirFlwEstimdFrnt"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]


class DRMFRLCURCANFD1Fr04:
    msg_name = "DRMFRLCURCANFD1Fr04"
    msg_id = 657
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "DRMFR"
    rx_nodes = ['PPOD']
    sig_group_dict = {'FRRdrErrFb': ['FRRdrErrFbOverTempErrFb', 'FRRdrErrFbOverVoltagepErrFb', 'FRRdrErrFbSnsrBlkErrFb']}
    sig_group_dataid_dict = {}

    class FRRdrErrFb_UB:
        sig_name = "FRRdrErrFb_UB"
        sig_start_bit = 4
        update_id_bit = 4
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
        startbit = 4
        byte = 0
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class FRRdrErrFbSnsrBlkErrFb:
        sig_name = "FRRdrErrFbSnsrBlkErrFb"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class FRRdrErrFbOverVoltagepErrFb:
        sig_name = "FRRdrErrFbOverVoltagepErrFb"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class FRRdrErrFbOverTempErrFb:
        sig_name = "FRRdrErrFbOverTempErrFb"
        sig_start_bit = 7
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
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7


class LCURLCURCANFD1Fr02:
    msg_name = "LCURLCURCANFD1Fr02"
    msg_id = 146
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 64
    tx_node = "LCUR"
    rx_nodes = ['PPOD', 'DRMRR', 'RPOD', 'DRMFR']
    sig_group_dict = {'VehSpd': ['VehSpdChks', 'VehSpdCntr', 'VehSpdQf', 'VehSpdSpd'], 'VehMovgDir': ['VehMovgDirChks', 'VehMovgDirCntr', 'VehMovgDirVehMovgDir']}
    sig_group_dataid_dict = {'VehSpd': 1043}

    class FRDoorOpenClsSts:
        sig_name = "FRDoorOpenClsSts"
        sig_start_bit = 5
        update_id_bit = 49
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
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class VehSpdChks:
        sig_name = "VehSpdChks"
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

    class VehMovgDirChks:
        sig_name = "VehMovgDirChks"
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

    class VehSpdCntr:
        sig_name = "VehSpdCntr"
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

    class VehMovgDirVehMovgDir:
        sig_name = "VehMovgDirVehMovgDir"
        sig_start_bit = 19
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
        startbit = 19
        byte = 2
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class RLDoorOpenClsSts:
        sig_name = "RLDoorOpenClsSts"
        sig_start_bit = 3
        update_id_bit = 48
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
        startbit = 3
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VehSpd_UB:
        sig_name = "VehSpd_UB"
        sig_start_bit = 61
        update_id_bit = 61
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
        startbit = 61
        byte = 7
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VehMovgDirCntr:
        sig_name = "VehMovgDirCntr"
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

    class VehSpdQf:
        sig_name = "VehSpdQf"
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
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 51
        byte = 6
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class FLDoorOpenClsSts:
        sig_name = "FLDoorOpenClsSts"
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
        sig_value_table = {'DoorSts_Unknow': 0, 'DoorSts_Open': 1, 'DoorSts_Close': 2}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class RRDoorOpenClsSts:
        sig_name = "RRDoorOpenClsSts"
        sig_start_bit = 1
        update_id_bit = 63
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
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VehSpdSpd:
        sig_name = "VehSpdSpd"
        sig_start_bit = 31
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
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111110, 0b00000001, 7, 1)]

    class VehMovgDir_UB:
        sig_name = "VehMovgDir_UB"
        sig_start_bit = 62
        update_id_bit = 62
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
        startbit = 62
        byte = 7
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6


class DRMRRToLCURLCURCANFD1DiagRespFrame:
    msg_name = "DRMRRToLCURLCURCANFD1DiagRespFrame"
    msg_id = 1587
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "DRMRR"
    rx_nodes = ['LCUR']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class LCURLCURCANFD1Fr01:
    msg_name = "LCURLCURCANFD1Fr01"
    msg_id = 64
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 64
    tx_node = "LCUR"
    rx_nodes = ['PPOD', 'DRMRR', 'RPOD', 'DRMFR']
    sig_group_dict = {'GearLvrIndcnReal': ['GearLvrIndcnRealChks', 'GearLvrIndcnRealCntr', 'GearLvrIndcnRealGearLvrIndcn'], 'VMMGlbSig': ['VMMGlbSigCarModSts', 'VMMGlbSigChks', 'VMMGlbSigCntr', 'VMMGlbSigCnvincSubSts1', 'VMMGlbSigDrvgSubSts1', 'VMMGlbSigInactvSubSts1', 'VMMGlbSigLoBattModSts', 'VMMGlbSigUsgModSts']}
    sig_group_dataid_dict = {'GearLvrIndcnReal': 1065, 'VMMGlbSig': 1074}

    class VMMGlbSigCntr:
        sig_name = "VMMGlbSigCntr"
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

    class VMMGlbSigDrvgSubSts1:
        sig_name = "VMMGlbSigDrvgSubSts1"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VMMGlbSigCarModSts:
        sig_name = "VMMGlbSigCarModSts"
        sig_start_bit = 27
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
        startbit = 27
        byte = 3
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class GearLvrIndcnReal_UB:
        sig_name = "GearLvrIndcnReal_UB"
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

    class VMMGlbSigUsgModSts:
        sig_name = "VMMGlbSigUsgModSts"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class UsgModSts:
        sig_name = "UsgModSts"
        sig_start_bit = 15
        update_id_bit = 11
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
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class VMMGlbSigLoBattModSts:
        sig_name = "VMMGlbSigLoBattModSts"
        sig_start_bit = 59
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
        startbit = 59
        byte = 7
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class GearLvrIndcnRealCntr:
        sig_name = "GearLvrIndcnRealCntr"
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

    class GearLvrIndcnRealChks:
        sig_name = "GearLvrIndcnRealChks"
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

    class CurrentLvl:
        sig_name = "CurrentLvl"
        sig_start_bit = 7
        update_id_bit = 3
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 14
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HeightLevel_LowLevel5': 0, 'HeightLevel_LowLevel4': 1, 'HeightLevel_LowLevel3': 2, 'HeightLevel_LowLevel2': 3, 'HeightLevel_LowLevel1': 4, 'HeightLevel_NormaLevel': 5, 'HeightLevel_HighLevel1': 6, 'HeightLevel_HighLevel2': 7, 'HeightLevel_HighLevel3': 8, 'HeightLevel_HighLevel4': 9, 'HeightLevel_HighLevel5': 10, 'HeightLevel_Reserved1': 11, 'HeightLevel_Reserved2': 12, 'HeightLevel_Reserved3': 13, 'HeightLevel_InitUnknow': 14, 'HeightLevel_Invalid': 15}
        compute_method = None
        length = 4
        startbit = 7
        byte = 0
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

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

    class GearLvrIndcnRealGearLvrIndcn:
        sig_name = "GearLvrIndcnRealGearLvrIndcn"
        sig_start_bit = 75
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
        startbit = 75
        byte = 9
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class VMMGlbSigInactvSubSts1:
        sig_name = "VMMGlbSigInactvSubSts1"
        sig_start_bit = 55
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
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VMMGlbSig_UB:
        sig_name = "VMMGlbSig_UB"
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


class LCURLCURCANFD1Fr08:
    msg_name = "LCURLCURCANFD1Fr08"
    msg_id = 768
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 32
    tx_node = "LCUR"
    rx_nodes = ['PPOD', 'DRMRR', 'RPOD', 'DRMFR']
    sig_group_dict = {'LoadPwrActSts': ['LoadPwrActStsACCMPwrActSts', 'LoadPwrActStsAFUPwrActSts', 'LoadPwrActStsAGMPwrActSts', 'LoadPwrActStsAGUPwrActSts', 'LoadPwrActStsALMLPwrActSts', 'LoadPwrActStsALMRPwrActSts', 'LoadPwrActStsAWMPwrActSts', 'LoadPwrActStsBCCPPwrActSts', 'LoadPwrActStsBCFVPwrActSts', 'LoadPwrActStsBCTVPwrActSts', 'LoadPwrActStsBEXVPwrActSts', 'LoadPwrActStsBNCMPwrActSts', 'LoadPwrActStsBoosterBlowerPwrActSts', 'LoadPwrActStsCCTVPwrActSts', 'LoadPwrActStsCDPwrActSts', 'LoadPwrActStsCERVPwrActSts', 'LoadPwrActStsCRCMPwrActSts', 'LoadPwrActStsCSOVPwrActSts', 'LoadPwrActStsDCTVPwrActSts', 'LoadPwrActStsDICPwrActSts', 'LoadPwrActStsDMFLPwrActSts', 'LoadPwrActStsDPODPwrActSts', 'LoadPwrActStsDRFPwrActSts', 'LoadPwrActStsDRMFRPwrActSts', 'LoadPwrActStsDRMRLPwrActSts', 'LoadPwrActStsDRMRRPwrActSts', 'LoadPwrActStsECTVPwrActSts', 'LoadPwrActStsEDCPPwrActSts', 'LoadPwrActStsEGSMPwrActSts', 'LoadPwrActStsEPMPwrActSts', 'LoadPwrActStsFCSIPwrActSts', 'LoadPwrActStsFEXVPwrActSts', 'LoadPwrActStsFLRPwrActSts', 'LoadPwrActStsFSRLPwrActSts', 'LoadPwrActStsFSRRPwrActSts', 'LoadPwrActStsHBMFPwrActSts', 'LoadPwrActStsHBMRPwrActSts', 'LoadPwrActStsHCCPPwrActSts', 'LoadPwrActStsHCMLPwrActSts', 'LoadPwrActStsHCMRPwrActSts', 'LoadPwrActStsHCTVPwrActSts', 'LoadPwrActStsHODPwrActSts', 'LoadPwrActStsHUBFPwrActSts', 'LoadPwrActStsHUBRPwrActSts', 'LoadPwrActStsHVAHPwrActSts', 'LoadPwrActStsHVCHPwrActSts', 'LoadPwrActStsHVCMPwrActSts', 'LoadPwrActStsIEMPwrActSts', 'LoadPwrActStsIRMMPwrActSts', 'LoadPwrActStsLCTVPwrActSts', 'LoadPwrActStsLPODPwrActSts', 'LoadPwrActStsMGMPwrActSts', 'LoadPwrActStsMMDPwrActSts', 'LoadPwrActStsMMPPwrActSts', 'LoadPwrActStsNKRPwrActSts', 'LoadPwrActStsOHCPwrActSts', 'LoadPwrActStsOPCFPwrActSts', 'LoadPwrActStsOPCRPwrActSts', 'LoadPwrActStsPMSIPwrActSts', 'LoadPwrActStsPOFPwrActSts', 'LoadPwrActStsPORPwrActSts', 'LoadPwrActStsPPODPwrActSts', 'LoadPwrActStsRCMLPwrActSts', 'LoadPwrActStsRCMRPwrActSts', 'LoadPwrActStsReserved1', 'LoadPwrActStsReserved10', 'LoadPwrActStsReserved11', 'LoadPwrActStsReserved12', 'LoadPwrActStsReserved13', 'LoadPwrActStsReserved14', 'LoadPwrActStsReserved15', 'LoadPwrActStsReserved16', 'LoadPwrActStsReserved17', 'LoadPwrActStsReserved18', 'LoadPwrActStsReserved2', 'LoadPwrActStsReserved3', 'LoadPwrActStsReserved4', 'LoadPwrActStsReserved5', 'LoadPwrActStsReserved6', 'LoadPwrActStsReserved7', 'LoadPwrActStsReserved8', 'LoadPwrActStsReserved9', 'LoadPwrActStsREXVPwrActSts', 'LoadPwrActStsRLMMPwrActSts', 'LoadPwrActStsRLSMPwrActSts', 'LoadPwrActStsRMLPwrActSts', 'LoadPwrActStsRPODPwrActSts', 'LoadPwrActStsRRMMPwrActSts', 'LoadPwrActStsRSOV1PwrActSts', 'LoadPwrActStsRSOV2PwrActSts', 'LoadPwrActStsSCMFPwrActSts', 'LoadPwrActStsSCMRPwrActSts', 'LoadPwrActStsSODLPwrActSts', 'LoadPwrActStsSODRPwrActSts', 'LoadPwrActStsSRSPwrActSts', 'LoadPwrActStsSWTLPwrActSts', 'LoadPwrActStsSWTRPwrActSts', 'LoadPwrActStsTERVPwrActSts', 'LoadPwrActStsUSBR1PwrActSts', 'LoadPwrActStsUSBR2PwrActSts', 'LoadPwrActStsUWBPwrActSts', 'LoadPwrActStsVCUPwrActSts', 'LoadPwrActStsWERVPwrActSts', 'LoadPwrActStsWPCPwrActSts']}
    sig_group_dataid_dict = {}

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


class DRMRRLCURCANFD1Fr01:
    msg_name = "DRMRRLCURCANFD1Fr01"
    msg_id = 145
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "DRMRR"
    rx_nodes = ['RPOD', 'LCUR']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class RRDoorObstclDst:
        sig_name = "RRDoorObstclDst"
        sig_start_bit = 7
        update_id_bit = 15
        sig_length = 8
        sig_value_factor = 0.5
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 255
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class LCURLCURCANFD1TimeSynchFr01:
    msg_name = "LCURLCURCANFD1TimeSynchFr01"
    msg_id = 1
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "LCUR"
    rx_nodes = ['DRMFR', 'DRMRR']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class LCURToDRMFRLCURCANFD1DiagReqFrame:
    msg_name = "LCURToDRMFRLCURCANFD1DiagReqFrame"
    msg_id = 1841
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "LCUR"
    rx_nodes = ['DRMFR']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


