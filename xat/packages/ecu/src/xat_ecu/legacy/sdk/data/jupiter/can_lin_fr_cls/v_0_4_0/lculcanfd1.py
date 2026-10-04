class DRMFLLCULCANFD1Fr01:
    msg_name = "DRMFLLCULCANFD1Fr01"
    msg_id = 144
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "DRMFL"
    rx_nodes = ['DPOD', 'LCUL']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class FLDoorObstclDst:
        sig_name = "FLDoorObstclDst"
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


class LCULLCULCANFD1Fr07:
    msg_name = "LCULLCULCANFD1Fr07"
    msg_id = 2
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "LCUL"
    rx_nodes = ['DRMRL', 'DRMFL']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class ReLeDoorRdrModReq:
        sig_name = "ReLeDoorRdrModReq"
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

    class FrntLeDoorRdrModReq:
        sig_name = "FrntLeDoorRdrModReq"
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


class LCULLCULCANFD1Fr02:
    msg_name = "LCULLCULCANFD1Fr02"
    msg_id = 146
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 64
    tx_node = "LCUL"
    rx_nodes = ['LPOD', 'DPOD', 'DRMRL', 'DRMFL']
    sig_group_dict = {'VehMovgDir': ['VehMovgDirChks', 'VehMovgDirCntr', 'VehMovgDirVehMovgDir'], 'VehSpd': ['VehSpdChks', 'VehSpdCntr', 'VehSpdQf', 'VehSpdSpd']}
    sig_group_dataid_dict = {'VehSpd': 1043}

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

    class RLDoorOpenClsSts:
        sig_name = "RLDoorOpenClsSts"
        sig_start_bit = 5
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
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

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

    class FRDoorOpenClsSts:
        sig_name = "FRDoorOpenClsSts"
        sig_start_bit = 3
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
        startbit = 3
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2


class LCULLCULCANFD1TimeSynchFr01:
    msg_name = "LCULLCULCANFD1TimeSynchFr01"
    msg_id = 1
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "LCUL"
    rx_nodes = ['DRMRL', 'DRMFL']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class LPODLCULCANFD1Fr02:
    msg_name = "LPODLCULCANFD1Fr02"
    msg_id = 661
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 64
    tx_node = "LPOD"
    rx_nodes = ['LCUL']
    sig_group_dict = {'RLPwrDoorErrFb': ['RLPwrDoorErrFbBoolean', 'RLPwrDoorErrFbHallErrFb', 'RLPwrDoorErrFbMotThermErrFb', 'RLPwrDoorErrFbPosnUnknowFb', 'RLPwrDoorErrFbRollAngErrFb']}
    sig_group_dataid_dict = {}

    class RLDoorManResistSts:
        sig_name = "RLDoorManResistSts"
        sig_start_bit = 7
        update_id_bit = 1
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

    class RLPwrDoorErrFbBoolean:
        sig_name = "RLPwrDoorErrFbBoolean"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 20
        byte = 2
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class RLDoorSpdModeFb:
        sig_name = "RLDoorSpdModeFb"
        sig_start_bit = 3
        update_id_bit = 17
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
        startbit = 3
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class RLPwrDoorErrFbRollAngErrFb:
        sig_name = "RLPwrDoorErrFbRollAngErrFb"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 22
        byte = 2
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class RLPwrDoorErrFbPosnUnknowFb:
        sig_name = "RLPwrDoorErrFbPosnUnknowFb"
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

    class RLPwrDoorErrFb_UB:
        sig_name = "RLPwrDoorErrFb_UB"
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

    class RLPwrDoorErrFbMotThermErrFb:
        sig_name = "RLPwrDoorErrFbMotThermErrFb"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 21
        byte = 2
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class RLDoorMaxPosnSetFb:
        sig_name = "RLDoorMaxPosnSetFb"
        sig_start_bit = 15
        update_id_bit = 0
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

    class RLDoorModSts:
        sig_name = "RLDoorModSts"
        sig_start_bit = 5
        update_id_bit = 18
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
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class RLPwrDoorErrFbHallErrFb:
        sig_name = "RLPwrDoorErrFbHallErrFb"
        sig_start_bit = 23
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
        startbit = 23
        byte = 2
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class RLDoorOpenTrigSrc:
        sig_name = "RLDoorOpenTrigSrc"
        sig_start_bit = 31
        update_id_bit = 27
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
        startbit = 31
        byte = 3
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4


class LCULToDRMFLLCULCANFD1DiagReqFrame:
    msg_name = "LCULToDRMFLLCULCANFD1DiagReqFrame"
    msg_id = 1840
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "LCUL"
    rx_nodes = ['DRMFL']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class DRMFLLCULCANFD1Fr03:
    msg_name = "DRMFLLCULCANFD1Fr03"
    msg_id = 402
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 64
    tx_node = "DRMFL"
    rx_nodes = ['LCUL']
    sig_group_dict = {'FrntLeDoorRdrObj15': ['FrntLeDoorRdrObj15RdrObjDstX', 'FrntLeDoorRdrObj15RdrObjDstY', 'FrntLeDoorRdrObj15RdrObjDstZ', 'FrntLeDoorRdrObj15RdrObjV'], 'FrntLeDoorRdrObj11': ['FrntLeDoorRdrObj11RdrObjDstX', 'FrntLeDoorRdrObj11RdrObjDstY', 'FrntLeDoorRdrObj11RdrObjDstZ', 'FrntLeDoorRdrObj11RdrObjV'], 'FrntLeDoorRdrObj13': ['FrntLeDoorRdrObj13RdrObjDstX', 'FrntLeDoorRdrObj13RdrObjDstY', 'FrntLeDoorRdrObj13RdrObjDstZ', 'FrntLeDoorRdrObj13RdrObjV'], 'FrntLeDoorRdrObj16': ['FrntLeDoorRdrObj16RdrObjDstX', 'FrntLeDoorRdrObj16RdrObjDstY', 'FrntLeDoorRdrObj16RdrObjDstZ', 'FrntLeDoorRdrObj16RdrObjV'], 'FrntLeDoorRdrObj14': ['FrntLeDoorRdrObj14RdrObjDstX', 'FrntLeDoorRdrObj14RdrObjDstY', 'FrntLeDoorRdrObj14RdrObjDstZ', 'FrntLeDoorRdrObj14RdrObjV'], 'FrntLeDoorRdrObj12': ['FrntLeDoorRdrObj12RdrObjDstX', 'FrntLeDoorRdrObj12RdrObjDstY', 'FrntLeDoorRdrObj12RdrObjDstZ', 'FrntLeDoorRdrObj12RdrObjV']}
    sig_group_dataid_dict = {}

    class FrntLeDoorRdrObj13RdrObjDstZ:
        sig_name = "FrntLeDoorRdrObj13RdrObjDstZ"
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

    class FrntLeDoorRdrObj11RdrObjDstZ:
        sig_name = "FrntLeDoorRdrObj11RdrObjDstZ"
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

    class FrntLeDoorRdrObj13RdrObjDstY:
        sig_name = "FrntLeDoorRdrObj13RdrObjDstY"
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

    class FrntLeDoorRdrObj13RdrObjV:
        sig_name = "FrntLeDoorRdrObj13RdrObjV"
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

    class FrntLeDoorRdrObj15_UB:
        sig_name = "FrntLeDoorRdrObj15_UB"
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

    class FrntLeDoorRdrObj12RdrObjDstZ:
        sig_name = "FrntLeDoorRdrObj12RdrObjDstZ"
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

    class FrntLeDoorRdrObj11_UB:
        sig_name = "FrntLeDoorRdrObj11_UB"
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

    class FrntLeDoorRdrObj13_UB:
        sig_name = "FrntLeDoorRdrObj13_UB"
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

    class FrntLeDoorRdrObj15RdrObjV:
        sig_name = "FrntLeDoorRdrObj15RdrObjV"
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

    class FrntLeDoorRdrObj16_UB:
        sig_name = "FrntLeDoorRdrObj16_UB"
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

    class FrntLeDoorRdrObj13RdrObjDstX:
        sig_name = "FrntLeDoorRdrObj13RdrObjDstX"
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

    class FrntLeDoorRdrObj15RdrObjDstY:
        sig_name = "FrntLeDoorRdrObj15RdrObjDstY"
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

    class FrntLeDoorRdrObj16RdrObjDstZ:
        sig_name = "FrntLeDoorRdrObj16RdrObjDstZ"
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

    class FrntLeDoorRdrObj15RdrObjDstZ:
        sig_name = "FrntLeDoorRdrObj15RdrObjDstZ"
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

    class FrntLeDoorRdrObj11RdrObjV:
        sig_name = "FrntLeDoorRdrObj11RdrObjV"
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

    class FrntLeDoorRdrObj14_UB:
        sig_name = "FrntLeDoorRdrObj14_UB"
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

    class FrntLeDoorRdrObj14RdrObjDstX:
        sig_name = "FrntLeDoorRdrObj14RdrObjDstX"
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

    class FrntLeDoorRdrObj11RdrObjDstX:
        sig_name = "FrntLeDoorRdrObj11RdrObjDstX"
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

    class FrntLeDoorRdrObj14RdrObjV:
        sig_name = "FrntLeDoorRdrObj14RdrObjV"
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

    class FrntLeDoorRdrObj14RdrObjDstZ:
        sig_name = "FrntLeDoorRdrObj14RdrObjDstZ"
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

    class FrntLeDoorRdrObj14RdrObjDstY:
        sig_name = "FrntLeDoorRdrObj14RdrObjDstY"
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

    class FrntLeDoorRdrObj16RdrObjV:
        sig_name = "FrntLeDoorRdrObj16RdrObjV"
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

    class FrntLeDoorRdrObj12_UB:
        sig_name = "FrntLeDoorRdrObj12_UB"
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

    class FrntLeDoorRdrObj12RdrObjDstY:
        sig_name = "FrntLeDoorRdrObj12RdrObjDstY"
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

    class FrntLeDoorRdrObj15RdrObjDstX:
        sig_name = "FrntLeDoorRdrObj15RdrObjDstX"
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

    class FrntLeDoorRdrObj16RdrObjDstY:
        sig_name = "FrntLeDoorRdrObj16RdrObjDstY"
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

    class FrntLeDoorRdrObj16RdrObjDstX:
        sig_name = "FrntLeDoorRdrObj16RdrObjDstX"
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

    class FrntLeDoorRdrObj12RdrObjDstX:
        sig_name = "FrntLeDoorRdrObj12RdrObjDstX"
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

    class FrntLeDoorRdrObj12RdrObjV:
        sig_name = "FrntLeDoorRdrObj12RdrObjV"
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

    class FrntLeDoorRdrObj11RdrObjDstY:
        sig_name = "FrntLeDoorRdrObj11RdrObjDstY"
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


class LPODToLCULLCULCANFD1DiagRespFrame:
    msg_name = "LPODToLCULLCULCANFD1DiagRespFrame"
    msg_id = 1602
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "LPOD"
    rx_nodes = ['LCUL']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class DRMRLLCULCANFD1Fr01:
    msg_name = "DRMRLLCULCANFD1Fr01"
    msg_id = 145
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "DRMRL"
    rx_nodes = ['LPOD', 'LCUL']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class RLDoorObstclDst:
        sig_name = "RLDoorObstclDst"
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


class DPODToLCULLCULCANFD1DiagRespFrame:
    msg_name = "DPODToLCULLCULCANFD1DiagRespFrame"
    msg_id = 1600
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "DPOD"
    rx_nodes = ['LCUL']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class DPODLCULCANFD1NmFr:
    msg_name = "DPODLCULCANFD1NmFr"
    msg_id = 1281
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "DPOD"
    rx_nodes = ['LPOD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class DRMRLLCULCANFD1Fr03:
    msg_name = "DRMRLLCULCANFD1Fr03"
    msg_id = 404
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 64
    tx_node = "DRMRL"
    rx_nodes = ['LCUL']
    sig_group_dict = {'ReLeDoorRdrObj13': ['ReLeDoorRdrObj13RdrObjDstX', 'ReLeDoorRdrObj13RdrObjDstY', 'ReLeDoorRdrObj13RdrObjDstZ', 'ReLeDoorRdrObj13RdrObjV'], 'ReLeDoorRdrObj15': ['ReLeDoorRdrObj15RdrObjDstX', 'ReLeDoorRdrObj15RdrObjDstY', 'ReLeDoorRdrObj15RdrObjDstZ', 'ReLeDoorRdrObj15RdrObjV'], 'ReLeDoorRdrObj11': ['ReLeDoorRdrObj11RdrObjDstX', 'ReLeDoorRdrObj11RdrObjDstY', 'ReLeDoorRdrObj11RdrObjDstZ', 'ReLeDoorRdrObj11RdrObjV'], 'ReLeDoorRdrObj16': ['ReLeDoorRdrObj16RdrObjDstX', 'ReLeDoorRdrObj16RdrObjDstY', 'ReLeDoorRdrObj16RdrObjDstZ', 'ReLeDoorRdrObj16RdrObjV'], 'ReLeDoorRdrObj14': ['ReLeDoorRdrObj14RdrObjDstX', 'ReLeDoorRdrObj14RdrObjDstY', 'ReLeDoorRdrObj14RdrObjDstZ', 'ReLeDoorRdrObj14RdrObjV'], 'ReLeDoorRdrObj12': ['ReLeDoorRdrObj12RdrObjDstX', 'ReLeDoorRdrObj12RdrObjDstY', 'ReLeDoorRdrObj12RdrObjDstZ', 'ReLeDoorRdrObj12RdrObjV']}
    sig_group_dataid_dict = {}

    class ReLeDoorRdrObj13RdrObjDstZ:
        sig_name = "ReLeDoorRdrObj13RdrObjDstZ"
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

    class ReLeDoorRdrObj13_UB:
        sig_name = "ReLeDoorRdrObj13_UB"
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

    class ReLeDoorRdrObj12RdrObjDstY:
        sig_name = "ReLeDoorRdrObj12RdrObjDstY"
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

    class ReLeDoorRdrObj11RdrObjDstZ:
        sig_name = "ReLeDoorRdrObj11RdrObjDstZ"
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

    class ReLeDoorRdrObj13RdrObjV:
        sig_name = "ReLeDoorRdrObj13RdrObjV"
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

    class ReLeDoorRdrObj15_UB:
        sig_name = "ReLeDoorRdrObj15_UB"
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

    class ReLeDoorRdrObj11_UB:
        sig_name = "ReLeDoorRdrObj11_UB"
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

    class ReLeDoorRdrObj12RdrObjDstZ:
        sig_name = "ReLeDoorRdrObj12RdrObjDstZ"
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

    class ReLeDoorRdrObj11RdrObjV:
        sig_name = "ReLeDoorRdrObj11RdrObjV"
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

    class ReLeDoorRdrObj11RdrObjDstX:
        sig_name = "ReLeDoorRdrObj11RdrObjDstX"
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

    class ReLeDoorRdrObj11RdrObjDstY:
        sig_name = "ReLeDoorRdrObj11RdrObjDstY"
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

    class ReLeDoorRdrObj15RdrObjDstY:
        sig_name = "ReLeDoorRdrObj15RdrObjDstY"
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

    class ReLeDoorRdrObj16_UB:
        sig_name = "ReLeDoorRdrObj16_UB"
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

    class ReLeDoorRdrObj16RdrObjDstZ:
        sig_name = "ReLeDoorRdrObj16RdrObjDstZ"
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

    class ReLeDoorRdrObj14RdrObjDstZ:
        sig_name = "ReLeDoorRdrObj14RdrObjDstZ"
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

    class ReLeDoorRdrObj13RdrObjDstY:
        sig_name = "ReLeDoorRdrObj13RdrObjDstY"
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

    class ReLeDoorRdrObj14_UB:
        sig_name = "ReLeDoorRdrObj14_UB"
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

    class ReLeDoorRdrObj15RdrObjDstX:
        sig_name = "ReLeDoorRdrObj15RdrObjDstX"
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

    class ReLeDoorRdrObj13RdrObjDstX:
        sig_name = "ReLeDoorRdrObj13RdrObjDstX"
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

    class ReLeDoorRdrObj12RdrObjDstX:
        sig_name = "ReLeDoorRdrObj12RdrObjDstX"
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

    class ReLeDoorRdrObj15RdrObjV:
        sig_name = "ReLeDoorRdrObj15RdrObjV"
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

    class ReLeDoorRdrObj12RdrObjV:
        sig_name = "ReLeDoorRdrObj12RdrObjV"
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

    class ReLeDoorRdrObj15RdrObjDstZ:
        sig_name = "ReLeDoorRdrObj15RdrObjDstZ"
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

    class ReLeDoorRdrObj16RdrObjDstY:
        sig_name = "ReLeDoorRdrObj16RdrObjDstY"
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

    class ReLeDoorRdrObj16RdrObjDstX:
        sig_name = "ReLeDoorRdrObj16RdrObjDstX"
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

    class ReLeDoorRdrObj12_UB:
        sig_name = "ReLeDoorRdrObj12_UB"
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

    class ReLeDoorRdrObj14RdrObjV:
        sig_name = "ReLeDoorRdrObj14RdrObjV"
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

    class ReLeDoorRdrObj14RdrObjDstY:
        sig_name = "ReLeDoorRdrObj14RdrObjDstY"
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

    class ReLeDoorRdrObj16RdrObjV:
        sig_name = "ReLeDoorRdrObj16RdrObjV"
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

    class ReLeDoorRdrObj14RdrObjDstX:
        sig_name = "ReLeDoorRdrObj14RdrObjDstX"
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


class DRMFLToLCULLCULCANFD1DiagRespFrame:
    msg_name = "DRMFLToLCULLCULCANFD1DiagRespFrame"
    msg_id = 1584
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "DRMFL"
    rx_nodes = ['LCUL']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class LCULToAllLCULCANFD1DiagFuncReqFrame:
    msg_name = "LCULToAllLCULCANFD1DiagFuncReqFrame"
    msg_id = 2047
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "LCUL"
    rx_nodes = ['LPOD', 'DPOD', 'DRMRL', 'DRMFL']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class DRMRLLCULCANFD1Fr02:
    msg_name = "DRMRLLCULCANFD1Fr02"
    msg_id = 403
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 64
    tx_node = "DRMRL"
    rx_nodes = ['LPOD', 'LCUL']
    sig_group_dict = {'ReLeDoorRdrObj9': ['ReLeDoorRdrObj9RdrObjDstX', 'ReLeDoorRdrObj9RdrObjDstY', 'ReLeDoorRdrObj9RdrObjDstZ', 'ReLeDoorRdrObj9RdrObjV'], 'ReLeDoorRdrObj5': ['ReLeDoorRdrObj5RdrObjDstX', 'ReLeDoorRdrObj5RdrObjDstY', 'ReLeDoorRdrObj5RdrObjDstZ', 'ReLeDoorRdrObj5RdrObjV'], 'ReLeDoorRdrObj8': ['ReLeDoorRdrObj8RdrObjDstX', 'ReLeDoorRdrObj8RdrObjDstY', 'ReLeDoorRdrObj8RdrObjDstZ', 'ReLeDoorRdrObj8RdrObjV'], 'ReLeDoorRdrObj1': ['ReLeDoorRdrObj1RdrObjDstX', 'ReLeDoorRdrObj1RdrObjDstY', 'ReLeDoorRdrObj1RdrObjDstZ', 'ReLeDoorRdrObj1RdrObjV'], 'ReLeDoorRdrObj4': ['ReLeDoorRdrObj4RdrObjDstX', 'ReLeDoorRdrObj4RdrObjDstY', 'ReLeDoorRdrObj4RdrObjDstZ', 'ReLeDoorRdrObj4RdrObjV'], 'ReLeDoorRdrObj7': ['ReLeDoorRdrObj7RdrObjDstX', 'ReLeDoorRdrObj7RdrObjDstY', 'ReLeDoorRdrObj7RdrObjDstZ', 'ReLeDoorRdrObj7RdrObjV'], 'ReLeDoorRdrObj6': ['ReLeDoorRdrObj6RdrObjDstX', 'ReLeDoorRdrObj6RdrObjDstY', 'ReLeDoorRdrObj6RdrObjDstZ', 'ReLeDoorRdrObj6RdrObjV'], 'ReLeDoorRdrObj3': ['ReLeDoorRdrObj3RdrObjDstX', 'ReLeDoorRdrObj3RdrObjDstY', 'ReLeDoorRdrObj3RdrObjDstZ', 'ReLeDoorRdrObj3RdrObjV'], 'ReLeDoorRdrObj10': ['ReLeDoorRdrObj10RdrObjDstX', 'ReLeDoorRdrObj10RdrObjDstY', 'ReLeDoorRdrObj10RdrObjDstZ', 'ReLeDoorRdrObj10RdrObjV'], 'ReLeDoorRdrObj2': ['ReLeDoorRdrObj2RdrObjDstX', 'ReLeDoorRdrObj2RdrObjDstY', 'ReLeDoorRdrObj2RdrObjDstZ', 'ReLeDoorRdrObj2RdrObjV']}
    sig_group_dataid_dict = {}

    class ReLeDoorRdrObj5RdrObjDstY:
        sig_name = "ReLeDoorRdrObj5RdrObjDstY"
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

    class ReLeDoorRdrObj4RdrObjDstX:
        sig_name = "ReLeDoorRdrObj4RdrObjDstX"
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

    class ReLeDoorRdrObj3RdrObjDstX:
        sig_name = "ReLeDoorRdrObj3RdrObjDstX"
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

    class ReLeDoorRdrObj10RdrObjV:
        sig_name = "ReLeDoorRdrObj10RdrObjV"
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

    class ReLeDoorRdrObj7RdrObjDstZ:
        sig_name = "ReLeDoorRdrObj7RdrObjDstZ"
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

    class ReLeDoorRdrObj2RdrObjDstY:
        sig_name = "ReLeDoorRdrObj2RdrObjDstY"
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

    class ReLeDoorRdrObj7RdrObjV:
        sig_name = "ReLeDoorRdrObj7RdrObjV"
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

    class ReLeDoorRdrObj3RdrObjV:
        sig_name = "ReLeDoorRdrObj3RdrObjV"
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

    class ReLeDoorRdrObj9_UB:
        sig_name = "ReLeDoorRdrObj9_UB"
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

    class ReLeDoorRdrObj6RdrObjV:
        sig_name = "ReLeDoorRdrObj6RdrObjV"
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

    class ReLeDoorRdrObj9RdrObjV:
        sig_name = "ReLeDoorRdrObj9RdrObjV"
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

    class ReLeDoorRdrObj9RdrObjDstX:
        sig_name = "ReLeDoorRdrObj9RdrObjDstX"
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

    class ReLeDoorRdrObj4RdrObjV:
        sig_name = "ReLeDoorRdrObj4RdrObjV"
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

    class ReLeDoorRdrObj5_UB:
        sig_name = "ReLeDoorRdrObj5_UB"
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

    class ReLeDoorRdrObj10RdrObjDstX:
        sig_name = "ReLeDoorRdrObj10RdrObjDstX"
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

    class ReLeDoorRdrObj1RdrObjDstZ:
        sig_name = "ReLeDoorRdrObj1RdrObjDstZ"
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

    class ReLeDoorRdrFlt:
        sig_name = "ReLeDoorRdrFlt"
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

    class ReLeDoorRdrObj8_UB:
        sig_name = "ReLeDoorRdrObj8_UB"
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

    class ReLeDoorRdrObj1_UB:
        sig_name = "ReLeDoorRdrObj1_UB"
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

    class ReLeDoorRdrObj7RdrObjDstY:
        sig_name = "ReLeDoorRdrObj7RdrObjDstY"
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

    class ReLeDoorRdrObj1RdrObjDstY:
        sig_name = "ReLeDoorRdrObj1RdrObjDstY"
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

    class ReLeDoorRdrObj3RdrObjDstY:
        sig_name = "ReLeDoorRdrObj3RdrObjDstY"
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

    class RLRdrWorkSts:
        sig_name = "RLRdrWorkSts"
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

    class ReLeDoorRdrObj2RdrObjV:
        sig_name = "ReLeDoorRdrObj2RdrObjV"
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

    class ReLeDoorRdrObj9RdrObjDstZ:
        sig_name = "ReLeDoorRdrObj9RdrObjDstZ"
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

    class ReLeDoorRdrObj8RdrObjDstZ:
        sig_name = "ReLeDoorRdrObj8RdrObjDstZ"
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

    class ReLeDoorRdrObj1RdrObjDstX:
        sig_name = "ReLeDoorRdrObj1RdrObjDstX"
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

    class ReLeDoorRdrObj3RdrObjDstZ:
        sig_name = "ReLeDoorRdrObj3RdrObjDstZ"
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

    class ReLeDoorRdrObj4RdrObjDstZ:
        sig_name = "ReLeDoorRdrObj4RdrObjDstZ"
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

    class ReLeDoorRdrObj10RdrObjDstY:
        sig_name = "ReLeDoorRdrObj10RdrObjDstY"
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

    class ReLeDoorRdrObj2RdrObjDstX:
        sig_name = "ReLeDoorRdrObj2RdrObjDstX"
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

    class ReLeDoorRdrObj1RdrObjV:
        sig_name = "ReLeDoorRdrObj1RdrObjV"
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

    class ReLeDoorRdrObj7RdrObjDstX:
        sig_name = "ReLeDoorRdrObj7RdrObjDstX"
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

    class ReLeDoorRdrObj4_UB:
        sig_name = "ReLeDoorRdrObj4_UB"
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

    class ReLeDoorRdrObj8RdrObjDstY:
        sig_name = "ReLeDoorRdrObj8RdrObjDstY"
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

    class ReLeDoorRdrObj9RdrObjDstY:
        sig_name = "ReLeDoorRdrObj9RdrObjDstY"
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

    class ReLeDoorRdrObj5RdrObjDstZ:
        sig_name = "ReLeDoorRdrObj5RdrObjDstZ"
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

    class ReLeDoorRdrObj7_UB:
        sig_name = "ReLeDoorRdrObj7_UB"
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

    class ReLeDoorRdrObj6RdrObjDstX:
        sig_name = "ReLeDoorRdrObj6RdrObjDstX"
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

    class ReLeDoorRdrObj6_UB:
        sig_name = "ReLeDoorRdrObj6_UB"
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

    class ReLeDoorRdrObj8RdrObjDstX:
        sig_name = "ReLeDoorRdrObj8RdrObjDstX"
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

    class ReLeDoorRdrObj10RdrObjDstZ:
        sig_name = "ReLeDoorRdrObj10RdrObjDstZ"
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

    class ReLeDoorRdrObj8RdrObjV:
        sig_name = "ReLeDoorRdrObj8RdrObjV"
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

    class ReLeDoorRdrObj5RdrObjDstX:
        sig_name = "ReLeDoorRdrObj5RdrObjDstX"
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

    class ReLeDoorRdrObj3_UB:
        sig_name = "ReLeDoorRdrObj3_UB"
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

    class ReLeDoorRdrObj6RdrObjDstZ:
        sig_name = "ReLeDoorRdrObj6RdrObjDstZ"
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

    class ReLeDoorRdrObj10_UB:
        sig_name = "ReLeDoorRdrObj10_UB"
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

    class ReLeDoorRdrMod:
        sig_name = "ReLeDoorRdrMod"
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

    class ReLeDoorRdrObj5RdrObjV:
        sig_name = "ReLeDoorRdrObj5RdrObjV"
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

    class ReLeDoorRdrObj4RdrObjDstY:
        sig_name = "ReLeDoorRdrObj4RdrObjDstY"
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

    class ReLeDoorRdrObj2_UB:
        sig_name = "ReLeDoorRdrObj2_UB"
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

    class ReLeDoorRdrObj2RdrObjDstZ:
        sig_name = "ReLeDoorRdrObj2RdrObjDstZ"
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

    class ReLeDoorRdrObj6RdrObjDstY:
        sig_name = "ReLeDoorRdrObj6RdrObjDstY"
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


class LPODLCULCANFD1Fr01:
    msg_name = "LPODLCULCANFD1Fr01"
    msg_id = 406
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 64
    tx_node = "LPOD"
    rx_nodes = ['LCUL']
    sig_group_dict = {'RLPwrDoorMotPrm': ['RLPwrDoorMotPrmPwrDoorStsFb', 'RLPwrDoorMotPrmStopEvnt'], 'RLDoorAntiPnchFb': ['RLDoorAntiPnchFbCloseAntiPnchSts', 'RLDoorAntiPnchFbOPenAntiPnchSts'], 'RLDoorPosnSts': ['RLDoorPosnStsDoorAngPosn', 'RLDoorPosnStsDoorPercPosn']}
    sig_group_dataid_dict = {}

    class RLPwrDoorMotPrmStopEvnt:
        sig_name = "RLPwrDoorMotPrmStopEvnt"
        sig_start_bit = 35
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
        startbit = 35
        byte = 4
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class RLDoorAntiPnchFbOPenAntiPnchSts:
        sig_name = "RLDoorAntiPnchFbOPenAntiPnchSts"
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

    class RLPwrDoorMotPrm_UB:
        sig_name = "RLPwrDoorMotPrm_UB"
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

    class RLDoorPosnStsDoorPercPosn:
        sig_name = "RLDoorPosnStsDoorPercPosn"
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

    class RLDoorAntiPnchFbCloseAntiPnchSts:
        sig_name = "RLDoorAntiPnchFbCloseAntiPnchSts"
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

    class RLDoorSpd:
        sig_name = "RLDoorSpd"
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

    class RLDoorAntiPnchFb_UB:
        sig_name = "RLDoorAntiPnchFb_UB"
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

    class RLPwrDoorMotPrmPwrDoorStsFb:
        sig_name = "RLPwrDoorMotPrmPwrDoorStsFb"
        sig_start_bit = 39
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
        startbit = 39
        byte = 4
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class RLDoorMtnSts:
        sig_name = "RLDoorMtnSts"
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

    class RLDoorPosnSts_UB:
        sig_name = "RLDoorPosnSts_UB"
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

    class RLDoorPosnStsDoorAngPosn:
        sig_name = "RLDoorPosnStsDoorAngPosn"
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


class LCULLCULCANFD1Fr06:
    msg_name = "LCULLCULCANFD1Fr06"
    msg_id = 660
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 64
    tx_node = "LCUL"
    rx_nodes = ['LPOD', 'DPOD']
    sig_group_dict = {'VehCfgDataGrp': ['VehCfgDataGrpVehCfgData1BlkIDBytePosn1', 'VehCfgDataGrpVehCfgData1BytePosn10', 'VehCfgDataGrpVehCfgData1BytePosn11', 'VehCfgDataGrpVehCfgData1BytePosn12', 'VehCfgDataGrpVehCfgData1BytePosn13', 'VehCfgDataGrpVehCfgData1BytePosn14', 'VehCfgDataGrpVehCfgData1BytePosn15', 'VehCfgDataGrpVehCfgData1BytePosn16', 'VehCfgDataGrpVehCfgData1BytePosn17', 'VehCfgDataGrpVehCfgData1BytePosn18', 'VehCfgDataGrpVehCfgData1BytePosn19', 'VehCfgDataGrpVehCfgData1BytePosn2', 'VehCfgDataGrpVehCfgData1BytePosn20', 'VehCfgDataGrpVehCfgData1BytePosn21', 'VehCfgDataGrpVehCfgData1BytePosn22', 'VehCfgDataGrpVehCfgData1BytePosn23', 'VehCfgDataGrpVehCfgData1BytePosn24', 'VehCfgDataGrpVehCfgData1BytePosn25', 'VehCfgDataGrpVehCfgData1BytePosn26', 'VehCfgDataGrpVehCfgData1BytePosn27', 'VehCfgDataGrpVehCfgData1BytePosn28', 'VehCfgDataGrpVehCfgData1BytePosn29', 'VehCfgDataGrpVehCfgData1BytePosn3', 'VehCfgDataGrpVehCfgData1BytePosn30', 'VehCfgDataGrpVehCfgData1BytePosn31', 'VehCfgDataGrpVehCfgData1BytePosn32', 'VehCfgDataGrpVehCfgData1BytePosn33', 'VehCfgDataGrpVehCfgData1BytePosn34', 'VehCfgDataGrpVehCfgData1BytePosn35', 'VehCfgDataGrpVehCfgData1BytePosn36', 'VehCfgDataGrpVehCfgData1BytePosn37', 'VehCfgDataGrpVehCfgData1BytePosn38', 'VehCfgDataGrpVehCfgData1BytePosn39', 'VehCfgDataGrpVehCfgData1BytePosn4', 'VehCfgDataGrpVehCfgData1BytePosn40', 'VehCfgDataGrpVehCfgData1BytePosn41', 'VehCfgDataGrpVehCfgData1BytePosn42', 'VehCfgDataGrpVehCfgData1BytePosn43', 'VehCfgDataGrpVehCfgData1BytePosn44', 'VehCfgDataGrpVehCfgData1BytePosn45', 'VehCfgDataGrpVehCfgData1BytePosn46', 'VehCfgDataGrpVehCfgData1BytePosn47', 'VehCfgDataGrpVehCfgData1BytePosn48', 'VehCfgDataGrpVehCfgData1BytePosn49', 'VehCfgDataGrpVehCfgData1BytePosn5', 'VehCfgDataGrpVehCfgData1BytePosn50', 'VehCfgDataGrpVehCfgData1BytePosn51', 'VehCfgDataGrpVehCfgData1BytePosn52', 'VehCfgDataGrpVehCfgData1BytePosn53', 'VehCfgDataGrpVehCfgData1BytePosn54', 'VehCfgDataGrpVehCfgData1BytePosn55', 'VehCfgDataGrpVehCfgData1BytePosn56', 'VehCfgDataGrpVehCfgData1BytePosn57', 'VehCfgDataGrpVehCfgData1BytePosn58', 'VehCfgDataGrpVehCfgData1BytePosn59', 'VehCfgDataGrpVehCfgData1BytePosn6', 'VehCfgDataGrpVehCfgData1BytePosn60', 'VehCfgDataGrpVehCfgData1BytePosn61', 'VehCfgDataGrpVehCfgData1BytePosn62', 'VehCfgDataGrpVehCfgData1BytePosn63', 'VehCfgDataGrpVehCfgData1BytePosn64', 'VehCfgDataGrpVehCfgData1BytePosn7', 'VehCfgDataGrpVehCfgData1BytePosn8', 'VehCfgDataGrpVehCfgData1BytePosn9']}
    sig_group_dataid_dict = {}

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


class LCULLCULCANFD1Fr03:
    msg_name = "LCULLCULCANFD1Fr03"
    msg_id = 304
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.04
    msg_length = 64
    tx_node = "LCUL"
    rx_nodes = ['LPOD', 'DPOD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class FRLtchPosn:
        sig_name = "FRLtchPosn"
        sig_start_bit = 3
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
        startbit = 3
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

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

    class RLLtchPosn:
        sig_name = "RLLtchPosn"
        sig_start_bit = 5
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
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

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


class DRMRLLCULCANFD1NmFr:
    msg_name = "DRMRLLCULCANFD1NmFr"
    msg_id = 1285
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "DRMRL"
    rx_nodes = ['DRMFL']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class DRMRLLCULCANFD1Fr04:
    msg_name = "DRMRLLCULCANFD1Fr04"
    msg_id = 658
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "DRMRL"
    rx_nodes = ['LPOD']
    sig_group_dict = {'RLRdrErrFb': ['RLRdrErrFbOverTempErrFb', 'RLRdrErrFbOverVoltagepErrFb', 'RLRdrErrFbSnsrBlkErrFb']}
    sig_group_dataid_dict = {}

    class RLRdrErrFb_UB:
        sig_name = "RLRdrErrFb_UB"
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

    class RLRdrErrFbOverTempErrFb:
        sig_name = "RLRdrErrFbOverTempErrFb"
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

    class RLRdrErrFbOverVoltagepErrFb:
        sig_name = "RLRdrErrFbOverVoltagepErrFb"
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

    class RLRdrErrFbSnsrBlkErrFb:
        sig_name = "RLRdrErrFbSnsrBlkErrFb"
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


class LCULLCULCANFD1Fr04:
    msg_name = "LCULLCULCANFD1Fr04"
    msg_id = 405
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 64
    tx_node = "LCUL"
    rx_nodes = ['LPOD', 'DPOD', 'DRMRL', 'DRMFL']
    sig_group_dict = {'FLPwrSideDoorCtrlReq': ['FLPwrSideDoorCtrlReqChks', 'FLPwrSideDoorCtrlReqCntr', 'FLPwrSideDoorCtrlReqPwrSideDoorCtrlReq', 'FLPwrSideDoorCtrlReqPwrSideDoorCtrlTrigSrc'], 'RLPwrSideDoorCtrlReq': ['RLPwrSideDoorCtrlReqChks', 'RLPwrSideDoorCtrlReqCntr', 'RLPwrSideDoorCtrlReqPwrSideDoorCtrlReq', 'RLPwrSideDoorCtrlReqPwrSideDoorCtrlTrigSrc'], 'SeatOccpSts': ['SeatOccpStsDrvrSeatSts', 'SeatOccpStsPassSeatSts', 'SeatOccpStsSecRowLeSeatSts', 'SeatOccpStsSecRowMidSeatSts', 'SeatOccpStsSecRowRiSeatSts', 'SeatOccpStsThrdRowLeSeatSts', 'SeatOccpStsThrdRowMidSeatSts', 'SeatOccpStsThrdRowRiSeatSts'], 'RLPwrSideDoorPosnSet': ['RLPwrSideDoorPosnSetChks', 'RLPwrSideDoorPosnSetCntr', 'RLPwrSideDoorPosnSetPosnCtrl', 'RLPwrSideDoorPosnSetPosnCtrlSrc'], 'Odometer': ['OdometerValidity', 'OdometerValue'], 'FLPwrSideDoorPosnSet': ['FLPwrSideDoorPosnSetChks', 'FLPwrSideDoorPosnSetCntr', 'FLPwrSideDoorPosnSetPosnCtrl', 'FLPwrSideDoorPosnSetPosnCtrlSrc']}
    sig_group_dataid_dict = {}

    class FLPwrSideDoorCtrlReqChks:
        sig_name = "FLPwrSideDoorCtrlReqChks"
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

    class FLPwrSideDoorCtrlReq_UB:
        sig_name = "FLPwrSideDoorCtrlReq_UB"
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

    class FLPwrSideDoorMaxPosnSet:
        sig_name = "FLPwrSideDoorMaxPosnSet"
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

    class RLPwrSideDoorCtrlReq_UB:
        sig_name = "RLPwrSideDoorCtrlReq_UB"
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

    class FLPwrSideDoorPosnSetPosnCtrlSrc:
        sig_name = "FLPwrSideDoorPosnSetPosnCtrlSrc"
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

    class RLPwrSideDoorCtrlReqCntr:
        sig_name = "RLPwrSideDoorCtrlReqCntr"
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

    class FLPwrSideDoorPosnSetCntr:
        sig_name = "FLPwrSideDoorPosnSetCntr"
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

    class RLPwrSideDoorCtrlReqPwrSideDoorCtrlReq:
        sig_name = "RLPwrSideDoorCtrlReqPwrSideDoorCtrlReq"
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

    class FLPwrSideDoorPosnSetChks:
        sig_name = "FLPwrSideDoorPosnSetChks"
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

    class RLPwrSideDoorCtrlReqPwrSideDoorCtrlTrigSrc:
        sig_name = "RLPwrSideDoorCtrlReqPwrSideDoorCtrlTrigSrc"
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

    class RLPwrSideDoorCtrlReqChks:
        sig_name = "RLPwrSideDoorCtrlReqChks"
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

    class RLPwrSideDoorMaxPosnSet:
        sig_name = "RLPwrSideDoorMaxPosnSet"
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

    class RLPwrSideDoorPosnSetPosnCtrlSrc:
        sig_name = "RLPwrSideDoorPosnSetPosnCtrlSrc"
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

    class RLPwrSideDoorPosnSetCntr:
        sig_name = "RLPwrSideDoorPosnSetCntr"
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

    class FLPwrSideDoorCtrlReqPwrSideDoorCtrlReq:
        sig_name = "FLPwrSideDoorCtrlReqPwrSideDoorCtrlReq"
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

    class RLPwrSideDoorPosnSetChks:
        sig_name = "RLPwrSideDoorPosnSetChks"
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

    class FLPwrSideDoorCtrlReqCntr:
        sig_name = "FLPwrSideDoorCtrlReqCntr"
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

    class RLPwrSideDoorPosnSetPosnCtrl:
        sig_name = "RLPwrSideDoorPosnSetPosnCtrl"
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

    class RLPwrSideDoorPosnSet_UB:
        sig_name = "RLPwrSideDoorPosnSet_UB"
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

    class FLPwrSideDoorPosnSetPosnCtrl:
        sig_name = "FLPwrSideDoorPosnSetPosnCtrl"
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

    class FLPwrSideDoorPosnSet_UB:
        sig_name = "FLPwrSideDoorPosnSet_UB"
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

    class FLPwrSideDoorCtrlReqPwrSideDoorCtrlTrigSrc:
        sig_name = "FLPwrSideDoorCtrlReqPwrSideDoorCtrlTrigSrc"
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


class LCULLCULCANFD1Fr01:
    msg_name = "LCULLCULCANFD1Fr01"
    msg_id = 64
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 64
    tx_node = "LCUL"
    rx_nodes = ['LPOD', 'DPOD', 'DRMRL', 'DRMFL']
    sig_group_dict = {'VMMGlbSig': ['VMMGlbSigCarModSts', 'VMMGlbSigChks', 'VMMGlbSigCntr', 'VMMGlbSigCnvincSubSts1', 'VMMGlbSigDrvgSubSts1', 'VMMGlbSigInactvSubSts1', 'VMMGlbSigLoBattModSts', 'VMMGlbSigUsgModSts'], 'GearLvrIndcnReal': ['GearLvrIndcnRealChks', 'GearLvrIndcnRealCntr', 'GearLvrIndcnRealGearLvrIndcn']}
    sig_group_dataid_dict = {'VMMGlbSig': 1074, 'GearLvrIndcnReal': 1065}

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


class DPODLCULCANFD1Fr01:
    msg_name = "DPODLCULCANFD1Fr01"
    msg_id = 400
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 64
    tx_node = "DPOD"
    rx_nodes = ['LCUL']
    sig_group_dict = {'FLDoorPosnSts': ['FLDoorPosnStsDoorAngPosn', 'FLDoorPosnStsDoorPercPosn'], 'FLDoorAntiPnchFb': ['FLDoorAntiPnchFbCloseAntiPnchSts', 'FLDoorAntiPnchFbOPenAntiPnchSts'], 'FLPwrDoorMotPrm': ['FLPwrDoorMotPrmPwrDoorStsFb', 'FLPwrDoorMotPrmStopEvnt']}
    sig_group_dataid_dict = {}

    class FLDoorAntiPnchFbCloseAntiPnchSts:
        sig_name = "FLDoorAntiPnchFbCloseAntiPnchSts"
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

    class FLDoorPosnStsDoorAngPosn:
        sig_name = "FLDoorPosnStsDoorAngPosn"
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

    class FLDoorPosnSts_UB:
        sig_name = "FLDoorPosnSts_UB"
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

    class FLDoorPosnStsDoorPercPosn:
        sig_name = "FLDoorPosnStsDoorPercPosn"
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

    class FLPwrDoorMotPrmPwrDoorStsFb:
        sig_name = "FLPwrDoorMotPrmPwrDoorStsFb"
        sig_start_bit = 39
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
        startbit = 39
        byte = 4
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class FLDoorAntiPnchFb_UB:
        sig_name = "FLDoorAntiPnchFb_UB"
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

    class FLPwrDoorMotPrmStopEvnt:
        sig_name = "FLPwrDoorMotPrmStopEvnt"
        sig_start_bit = 35
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
        startbit = 35
        byte = 4
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class FLPwrDoorMotPrm_UB:
        sig_name = "FLPwrDoorMotPrm_UB"
        sig_start_bit = 43
        update_id_bit = 43
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
        startbit = 43
        byte = 5
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class FLDoorMtnSts:
        sig_name = "FLDoorMtnSts"
        sig_start_bit = 5
        update_id_bit = 47
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

    class FLDoorAntiPnchFbOPenAntiPnchSts:
        sig_name = "FLDoorAntiPnchFbOPenAntiPnchSts"
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

    class FLDoorSpdModeFb:
        sig_name = "FLDoorSpdModeFb"
        sig_start_bit = 1
        update_id_bit = 44
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
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class FLDoorSpd:
        sig_name = "FLDoorSpd"
        sig_start_bit = 31
        update_id_bit = 45
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


class DRMFLLCULCANFD1Fr04:
    msg_name = "DRMFLLCULCANFD1Fr04"
    msg_id = 657
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "DRMFL"
    rx_nodes = ['DPOD']
    sig_group_dict = {'FLRdrErrFb': ['FLRdrErrFbOverTempErrFb', 'FLRdrErrFbOverVoltagepErrFb', 'FLRdrErrFbSnsrBlkErrFb']}
    sig_group_dataid_dict = {}

    class FLRdrErrFbSnsrBlkErrFb:
        sig_name = "FLRdrErrFbSnsrBlkErrFb"
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

    class FLRdrErrFbOverTempErrFb:
        sig_name = "FLRdrErrFbOverTempErrFb"
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

    class FLRdrErrFbOverVoltagepErrFb:
        sig_name = "FLRdrErrFbOverVoltagepErrFb"
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

    class FLRdrErrFb_UB:
        sig_name = "FLRdrErrFb_UB"
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


class DRMFLLCULCANFD1Fr02:
    msg_name = "DRMFLLCULCANFD1Fr02"
    msg_id = 401
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 64
    tx_node = "DRMFL"
    rx_nodes = ['DPOD', 'LCUL']
    sig_group_dict = {'FrntLeDoorRdrObj5': ['FrntLeDoorRdrObj5RdrObjDstX', 'FrntLeDoorRdrObj5RdrObjDstY', 'FrntLeDoorRdrObj5RdrObjDstZ', 'FrntLeDoorRdrObj5RdrObjV'], 'FrntLeDoorRdrObj3': ['FrntLeDoorRdrObj3RdrObjDstX', 'FrntLeDoorRdrObj3RdrObjDstY', 'FrntLeDoorRdrObj3RdrObjDstZ', 'FrntLeDoorRdrObj3RdrObjV'], 'FrntLeDoorRdrObj10': ['FrntLeDoorRdrObj10RdrObjDstX', 'FrntLeDoorRdrObj10RdrObjDstY', 'FrntLeDoorRdrObj10RdrObjDstZ', 'FrntLeDoorRdrObj10RdrObjV'], 'FrntLeDoorRdrObj9': ['FrntLeDoorRdrObj9RdrObjDstX', 'FrntLeDoorRdrObj9RdrObjDstY', 'FrntLeDoorRdrObj9RdrObjDstZ', 'FrntLeDoorRdrObj9RdrObjV'], 'FrntLeDoorRdrObj4': ['FrntLeDoorRdrObj4RdrObjDstX', 'FrntLeDoorRdrObj4RdrObjDstY', 'FrntLeDoorRdrObj4RdrObjDstZ', 'FrntLeDoorRdrObj4RdrObjV'], 'FrntLeDoorRdrObj8': ['FrntLeDoorRdrObj8RdrObjDstX', 'FrntLeDoorRdrObj8RdrObjDstY', 'FrntLeDoorRdrObj8RdrObjDstZ', 'FrntLeDoorRdrObj8RdrObjV'], 'FrntLeDoorRdrObj2': ['FrntLeDoorRdrObj2RdrObjDstX', 'FrntLeDoorRdrObj2RdrObjDstY', 'FrntLeDoorRdrObj2RdrObjDstZ', 'FrntLeDoorRdrObj2RdrObjV'], 'FrntLeDoorRdrObj6': ['FrntLeDoorRdrObj6RdrObjDstX', 'FrntLeDoorRdrObj6RdrObjDstY', 'FrntLeDoorRdrObj6RdrObjDstZ', 'FrntLeDoorRdrObj6RdrObjV'], 'FrntLeDoorRdrObj7': ['FrntLeDoorRdrObj7RdrObjDstX', 'FrntLeDoorRdrObj7RdrObjDstY', 'FrntLeDoorRdrObj7RdrObjDstZ', 'FrntLeDoorRdrObj7RdrObjV'], 'FrntLeDoorRdrObj1': ['FrntLeDoorRdrObj1RdrObjDstX', 'FrntLeDoorRdrObj1RdrObjDstY', 'FrntLeDoorRdrObj1RdrObjDstZ', 'FrntLeDoorRdrObj1RdrObjV']}
    sig_group_dataid_dict = {}

    class FrntLeDoorRdrObj4RdrObjDstZ:
        sig_name = "FrntLeDoorRdrObj4RdrObjDstZ"
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

    class FrntLeDoorRdrObj5_UB:
        sig_name = "FrntLeDoorRdrObj5_UB"
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

    class FrntLeDoorRdrObj6RdrObjV:
        sig_name = "FrntLeDoorRdrObj6RdrObjV"
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

    class FrntLeDoorRdrObj2RdrObjDstX:
        sig_name = "FrntLeDoorRdrObj2RdrObjDstX"
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

    class FrntLeDoorRdrObj3_UB:
        sig_name = "FrntLeDoorRdrObj3_UB"
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

    class FrntLeDoorRdrObj8RdrObjDstZ:
        sig_name = "FrntLeDoorRdrObj8RdrObjDstZ"
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

    class FrntLeDoorRdrObj4RdrObjDstX:
        sig_name = "FrntLeDoorRdrObj4RdrObjDstX"
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

    class FrntLeDoorRdrObj8RdrObjDstY:
        sig_name = "FrntLeDoorRdrObj8RdrObjDstY"
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

    class FrntLeDoorRdrObj10_UB:
        sig_name = "FrntLeDoorRdrObj10_UB"
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

    class FrntLeDoorRdrMod:
        sig_name = "FrntLeDoorRdrMod"
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

    class FrntLeDoorRdrObj6RdrObjDstZ:
        sig_name = "FrntLeDoorRdrObj6RdrObjDstZ"
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

    class FrntLeDoorRdrObj10RdrObjDstZ:
        sig_name = "FrntLeDoorRdrObj10RdrObjDstZ"
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

    class FrntLeDoorRdrObj3RdrObjDstZ:
        sig_name = "FrntLeDoorRdrObj3RdrObjDstZ"
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

    class FrntLeDoorRdrObj9RdrObjDstY:
        sig_name = "FrntLeDoorRdrObj9RdrObjDstY"
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

    class FrntLeDoorRdrObj9_UB:
        sig_name = "FrntLeDoorRdrObj9_UB"
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

    class FrntLeDoorRdrObj2RdrObjDstZ:
        sig_name = "FrntLeDoorRdrObj2RdrObjDstZ"
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

    class FrntLeDoorRdrObj3RdrObjDstX:
        sig_name = "FrntLeDoorRdrObj3RdrObjDstX"
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

    class FrntLeDoorRdrObj1RdrObjDstZ:
        sig_name = "FrntLeDoorRdrObj1RdrObjDstZ"
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

    class FrntLeDoorRdrObj6RdrObjDstX:
        sig_name = "FrntLeDoorRdrObj6RdrObjDstX"
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

    class FrntLeDoorRdrObj4RdrObjV:
        sig_name = "FrntLeDoorRdrObj4RdrObjV"
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

    class FrntLeDoorRdrFlt:
        sig_name = "FrntLeDoorRdrFlt"
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

    class FrntLeDoorRdrObj9RdrObjV:
        sig_name = "FrntLeDoorRdrObj9RdrObjV"
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

    class FrntLeDoorRdrObj8RdrObjDstX:
        sig_name = "FrntLeDoorRdrObj8RdrObjDstX"
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

    class FrntLeDoorRdrObj10RdrObjDstX:
        sig_name = "FrntLeDoorRdrObj10RdrObjDstX"
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

    class FrntLeDoorRdrObj5RdrObjDstZ:
        sig_name = "FrntLeDoorRdrObj5RdrObjDstZ"
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

    class FrntLeDoorRdrObj1RdrObjDstX:
        sig_name = "FrntLeDoorRdrObj1RdrObjDstX"
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

    class FrntLeDoorRdrObj8RdrObjV:
        sig_name = "FrntLeDoorRdrObj8RdrObjV"
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

    class FrntLeDoorRdrObj1RdrObjDstY:
        sig_name = "FrntLeDoorRdrObj1RdrObjDstY"
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

    class FrntLeDoorRdrObj4_UB:
        sig_name = "FrntLeDoorRdrObj4_UB"
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

    class FrntLeDoorRdrObj7RdrObjV:
        sig_name = "FrntLeDoorRdrObj7RdrObjV"
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

    class FrntLeDoorRdrObj10RdrObjDstY:
        sig_name = "FrntLeDoorRdrObj10RdrObjDstY"
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

    class FrntLeDoorRdrObj8_UB:
        sig_name = "FrntLeDoorRdrObj8_UB"
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

    class FrntLeDoorRdrObj9RdrObjDstX:
        sig_name = "FrntLeDoorRdrObj9RdrObjDstX"
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

    class FrntLeDoorRdrObj2_UB:
        sig_name = "FrntLeDoorRdrObj2_UB"
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

    class FrntLeDoorRdrObj3RdrObjDstY:
        sig_name = "FrntLeDoorRdrObj3RdrObjDstY"
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

    class FrntLeDoorRdrObj5RdrObjV:
        sig_name = "FrntLeDoorRdrObj5RdrObjV"
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

    class FrntLeDoorRdrObj2RdrObjDstY:
        sig_name = "FrntLeDoorRdrObj2RdrObjDstY"
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

    class FrntLeDoorRdrObj5RdrObjDstY:
        sig_name = "FrntLeDoorRdrObj5RdrObjDstY"
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

    class FrntLeDoorRdrObj6RdrObjDstY:
        sig_name = "FrntLeDoorRdrObj6RdrObjDstY"
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

    class FrntLeDoorRdrObj6_UB:
        sig_name = "FrntLeDoorRdrObj6_UB"
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

    class FrntLeDoorRdrObj7RdrObjDstX:
        sig_name = "FrntLeDoorRdrObj7RdrObjDstX"
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

    class FrntLeDoorRdrObj3RdrObjV:
        sig_name = "FrntLeDoorRdrObj3RdrObjV"
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

    class FrntLeDoorRdrObj5RdrObjDstX:
        sig_name = "FrntLeDoorRdrObj5RdrObjDstX"
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

    class FrntLeDoorRdrObj7RdrObjDstY:
        sig_name = "FrntLeDoorRdrObj7RdrObjDstY"
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

    class FrntLeDoorRdrObj7_UB:
        sig_name = "FrntLeDoorRdrObj7_UB"
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

    class FrntLeDoorRdrObj1RdrObjV:
        sig_name = "FrntLeDoorRdrObj1RdrObjV"
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

    class FrntLeDoorRdrObj10RdrObjV:
        sig_name = "FrntLeDoorRdrObj10RdrObjV"
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

    class FrntLeDoorRdrObj9RdrObjDstZ:
        sig_name = "FrntLeDoorRdrObj9RdrObjDstZ"
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

    class FLRdrWorkSts:
        sig_name = "FLRdrWorkSts"
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

    class FrntLeDoorRdrObj4RdrObjDstY:
        sig_name = "FrntLeDoorRdrObj4RdrObjDstY"
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

    class FrntLeDoorRdrObj2RdrObjV:
        sig_name = "FrntLeDoorRdrObj2RdrObjV"
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

    class FrntLeDoorRdrObj1_UB:
        sig_name = "FrntLeDoorRdrObj1_UB"
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

    class FrntLeDoorRdrObj7RdrObjDstZ:
        sig_name = "FrntLeDoorRdrObj7RdrObjDstZ"
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


class LCULToDRMRLLCULCANFD1DiagReqFrame:
    msg_name = "LCULToDRMRLLCULCANFD1DiagReqFrame"
    msg_id = 1842
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "LCUL"
    rx_nodes = ['DRMRL']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class LCULLCULCANFD1NmFr:
    msg_name = "LCULLCULCANFD1NmFr"
    msg_id = 1283
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "LCUL"
    rx_nodes = ['DRMRL']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class LCULLCULCANFD1Fr08:
    msg_name = "LCULLCULCANFD1Fr08"
    msg_id = 768
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 64
    tx_node = "LCUL"
    rx_nodes = ['LPOD', 'DPOD', 'DRMRL', 'DRMFL']
    sig_group_dict = {'LoadPwrActSts': ['LoadPwrActStsACCMPwrActSts', 'LoadPwrActStsAFUPwrActSts', 'LoadPwrActStsAGMPwrActSts', 'LoadPwrActStsAGUPwrActSts', 'LoadPwrActStsALMLPwrActSts', 'LoadPwrActStsALMRPwrActSts', 'LoadPwrActStsAWMPwrActSts', 'LoadPwrActStsBCCPPwrActSts', 'LoadPwrActStsBCFVPwrActSts', 'LoadPwrActStsBCTVPwrActSts', 'LoadPwrActStsBEXVPwrActSts', 'LoadPwrActStsBNCMPwrActSts', 'LoadPwrActStsBoosterBlowerPwrActSts', 'LoadPwrActStsCCTVPwrActSts', 'LoadPwrActStsCDPwrActSts', 'LoadPwrActStsCERVPwrActSts', 'LoadPwrActStsCRCMPwrActSts', 'LoadPwrActStsCSOVPwrActSts', 'LoadPwrActStsDCTVPwrActSts', 'LoadPwrActStsDICPwrActSts', 'LoadPwrActStsDMFLPwrActSts', 'LoadPwrActStsDPODPwrActSts', 'LoadPwrActStsDRFPwrActSts', 'LoadPwrActStsDRMFRPwrActSts', 'LoadPwrActStsDRMRLPwrActSts', 'LoadPwrActStsDRMRRPwrActSts', 'LoadPwrActStsECTVPwrActSts', 'LoadPwrActStsEDCPPwrActSts', 'LoadPwrActStsEGSMPwrActSts', 'LoadPwrActStsEPMPwrActSts', 'LoadPwrActStsFCSIPwrActSts', 'LoadPwrActStsFEXVPwrActSts', 'LoadPwrActStsFLRPwrActSts', 'LoadPwrActStsFSRLPwrActSts', 'LoadPwrActStsFSRRPwrActSts', 'LoadPwrActStsHBMFPwrActSts', 'LoadPwrActStsHBMRPwrActSts', 'LoadPwrActStsHCCPPwrActSts', 'LoadPwrActStsHCMLPwrActSts', 'LoadPwrActStsHCMRPwrActSts', 'LoadPwrActStsHCTVPwrActSts', 'LoadPwrActStsHODPwrActSts', 'LoadPwrActStsHUBFPwrActSts', 'LoadPwrActStsHUBRPwrActSts', 'LoadPwrActStsHVAHPwrActSts', 'LoadPwrActStsHVCHPwrActSts', 'LoadPwrActStsHVCMPwrActSts', 'LoadPwrActStsIEMPwrActSts', 'LoadPwrActStsIRMMPwrActSts', 'LoadPwrActStsLCTVPwrActSts', 'LoadPwrActStsLPODPwrActSts', 'LoadPwrActStsMGMPwrActSts', 'LoadPwrActStsMMDPwrActSts', 'LoadPwrActStsMMPPwrActSts', 'LoadPwrActStsNKRPwrActSts', 'LoadPwrActStsOHCPwrActSts', 'LoadPwrActStsOPCFPwrActSts', 'LoadPwrActStsOPCRPwrActSts', 'LoadPwrActStsPMSIPwrActSts', 'LoadPwrActStsPOFPwrActSts', 'LoadPwrActStsPORPwrActSts', 'LoadPwrActStsPPODPwrActSts', 'LoadPwrActStsRCMLPwrActSts', 'LoadPwrActStsRCMRPwrActSts', 'LoadPwrActStsReserved1', 'LoadPwrActStsReserved10', 'LoadPwrActStsReserved11', 'LoadPwrActStsReserved12', 'LoadPwrActStsReserved13', 'LoadPwrActStsReserved14', 'LoadPwrActStsReserved15', 'LoadPwrActStsReserved16', 'LoadPwrActStsReserved17', 'LoadPwrActStsReserved18', 'LoadPwrActStsReserved2', 'LoadPwrActStsReserved3', 'LoadPwrActStsReserved4', 'LoadPwrActStsReserved5', 'LoadPwrActStsReserved6', 'LoadPwrActStsReserved7', 'LoadPwrActStsReserved8', 'LoadPwrActStsReserved9', 'LoadPwrActStsREXVPwrActSts', 'LoadPwrActStsRLMMPwrActSts', 'LoadPwrActStsRLSMPwrActSts', 'LoadPwrActStsRMLPwrActSts', 'LoadPwrActStsRPODPwrActSts', 'LoadPwrActStsRRMMPwrActSts', 'LoadPwrActStsRSOV1PwrActSts', 'LoadPwrActStsRSOV2PwrActSts', 'LoadPwrActStsSCMFPwrActSts', 'LoadPwrActStsSCMRPwrActSts', 'LoadPwrActStsSODLPwrActSts', 'LoadPwrActStsSODRPwrActSts', 'LoadPwrActStsSRSPwrActSts', 'LoadPwrActStsSWTLPwrActSts', 'LoadPwrActStsSWTRPwrActSts', 'LoadPwrActStsTERVPwrActSts', 'LoadPwrActStsUSBR1PwrActSts', 'LoadPwrActStsUSBR2PwrActSts', 'LoadPwrActStsUWBPwrActSts', 'LoadPwrActStsVCUPwrActSts', 'LoadPwrActStsWERVPwrActSts', 'LoadPwrActStsWPCPwrActSts']}
    sig_group_dataid_dict = {}

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


class DRMFLLCULCANFD1NmFr:
    msg_name = "DRMFLLCULCANFD1NmFr"
    msg_id = 1284
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "DRMFL"
    rx_nodes = ['DPOD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class DPODLCULCANFD1Fr02:
    msg_name = "DPODLCULCANFD1Fr02"
    msg_id = 656
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 64
    tx_node = "DPOD"
    rx_nodes = ['LCUL']
    sig_group_dict = {'FLPwrDoorErrFb': ['FLPwrDoorErrFbBoolean', 'FLPwrDoorErrFbHallErrFb', 'FLPwrDoorErrFbMotThermErrFb', 'FLPwrDoorErrFbPosnUnknowFb', 'FLPwrDoorErrFbRollAngErrFb']}
    sig_group_dataid_dict = {}

    class FLPwrDoorErrFbRollAngErrFb:
        sig_name = "FLPwrDoorErrFbRollAngErrFb"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 22
        byte = 2
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class FLPwrDoorErrFbHallErrFb:
        sig_name = "FLPwrDoorErrFbHallErrFb"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 21
        byte = 2
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class FLDoorManResistSts:
        sig_name = "FLDoorManResistSts"
        sig_start_bit = 7
        update_id_bit = 3
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

    class FLPwrDoorErrFb_UB:
        sig_name = "FLPwrDoorErrFb_UB"
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

    class FLDoorMaxPosnSetFb:
        sig_name = "FLDoorMaxPosnSetFb"
        sig_start_bit = 15
        update_id_bit = 2
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

    class FLDoorModSts:
        sig_name = "FLDoorModSts"
        sig_start_bit = 5
        update_id_bit = 1
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
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class FLDoorOpenTrigSrc:
        sig_name = "FLDoorOpenTrigSrc"
        sig_start_bit = 31
        update_id_bit = 18
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
        startbit = 31
        byte = 3
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class FLPwrDoorErrFbMotThermErrFb:
        sig_name = "FLPwrDoorErrFbMotThermErrFb"
        sig_start_bit = 23
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
        startbit = 23
        byte = 2
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class FLPwrDoorErrFbBoolean:
        sig_name = "FLPwrDoorErrFbBoolean"
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

    class FLPwrDoorErrFbPosnUnknowFb:
        sig_name = "FLPwrDoorErrFbPosnUnknowFb"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 20
        byte = 2
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4


class LCULToLPODLCULCANFD1DiagReqFrame:
    msg_name = "LCULToLPODLCULCANFD1DiagReqFrame"
    msg_id = 1858
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "LCUL"
    rx_nodes = ['LPOD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class LPODLCULCANFD1NmFr:
    msg_name = "LPODLCULCANFD1NmFr"
    msg_id = 1282
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "LPOD"
    rx_nodes = ['LCUL']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class DRMRLToLCULLCULCANFD1DiagRespFrame:
    msg_name = "DRMRLToLCULLCULCANFD1DiagRespFrame"
    msg_id = 1586
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "DRMRL"
    rx_nodes = ['LCUL']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class LCULLCULCANFD1Fr05:
    msg_name = "LCULLCULCANFD1Fr05"
    msg_id = 659
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 64
    tx_node = "LCUL"
    rx_nodes = ['LPOD', 'DPOD', 'ETC']
    sig_group_dict = {'CmptmtAirFlwEstimd': ['CmptmtAirFlwEstimdFrnt', 'CmptmtAirFlwEstimdRe'], 'AmbIllmnFwdSts': ['AmbIllmnFwdStsAmbIllmn1', 'AmbIllmnFwdStsAmbIllmn2', 'AmbIllmnFwdStsChks', 'AmbIllmnFwdStsCntr'], 'HudSnsrErr': ['HudSnsrErrParChk', 'HudSnsrErrSnsrErr']}
    sig_group_dataid_dict = {}

    class WinReLeRippleCntr:
        sig_name = "WinReLeRippleCntr"
        sig_start_bit = 11
        update_id_bit = 291
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
        startbit = 11
        bmuws_info = [(1, 0b00001111, 0b11110000, 4, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class CmptmtAirFlwEstimdRe:
        sig_name = "CmptmtAirFlwEstimdRe"
        sig_start_bit = 33
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
        startbit = 33
        bmuws_info = [(4, 0b00000011, 0b11111100, 2, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class HudSnsrErrSnsrErr:
        sig_name = "HudSnsrErrSnsrErr"
        sig_start_bit = 278
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SnsrErr_FltStsTestPassd1': 0, 'SnsrErr_FltStsTestFaild2': 1}
        compute_method = None
        length = 1
        startbit = 278
        byte = 34
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class AmbIllmnFwdStsAmbIllmn1:
        sig_name = "AmbIllmnFwdStsAmbIllmn1"
        sig_start_bit = 440
        update_id_bit = None
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 440
        bmuws_info = [(55, 0b00000001, 0b11111110, 1, 0), (56, 0b11111111, 0b00000000, 8, 0)]

    class AmbIllmnFwdStsCntr:
        sig_name = "AmbIllmnFwdStsCntr"
        sig_start_bit = 479
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
        startbit = 479
        byte = 59
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class RecircRat:
        sig_name = "RecircRat"
        sig_start_bit = 257
        update_id_bit = 294
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
        startbit = 257
        bmuws_info = [(32, 0b00000011, 0b11111100, 2, 0), (33, 0b11111111, 0b00000000, 8, 0)]

    class RLDoorManResistCtrl:
        sig_name = "RLDoorManResistCtrl"
        sig_start_bit = 285
        update_id_bit = 290
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
        startbit = 285
        byte = 35
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class CmptmtAirFlwEstimd_UB:
        sig_name = "CmptmtAirFlwEstimd_UB"
        sig_start_bit = 283
        update_id_bit = 283
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
        startbit = 283
        byte = 35
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class WinDrvrRippleCntr:
        sig_name = "WinDrvrRippleCntr"
        sig_start_bit = 7
        update_id_bit = 292
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
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11110000, 0b00001111, 4, 4)]

    class ReBlwrAftRunSts:
        sig_name = "ReBlwrAftRunSts"
        sig_start_bit = 287
        update_id_bit = 280
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
        startbit = 287
        byte = 35
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ReBlwrLvlSts:
        sig_name = "ReBlwrLvlSts"
        sig_start_bit = 261
        update_id_bit = 295
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 12
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FrntBlwrLvl_Off': 0, 'FrntBlwrLvl_LvlMan1': 1, 'FrntBlwrLvl_LvlMan2': 2, 'FrntBlwrLvl_LvlMan3': 3, 'FrntBlwrLvl_LvlMan4': 4, 'FrntBlwrLvl_LvlMan5': 5, 'FrntBlwrLvl_LvlMan6': 6, 'FrntBlwrLvl_LvlMan7': 7, 'FrntBlwrLvl_LvlMan8': 8, 'FrntBlwrLvl_LvlMan9': 9, 'FrntBlwrLvl_LvlAutoLo': 10, 'FrntBlwrLvl_LvlAutoNormal': 11, 'FrntBlwrLvl_LvlAutoHi': 12}
        compute_method = None
        length = 4
        startbit = 261
        byte = 32
        mask = 0b00111100
        unmask = 0b11000011
        shift = 2

    class AmbIllmnFwdStsChks:
        sig_name = "AmbIllmnFwdStsChks"
        sig_start_bit = 471
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 471
        byte = 58
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class AmbIllmnFwdSts_UB:
        sig_name = "AmbIllmnFwdSts_UB"
        sig_start_bit = 434
        update_id_bit = 434
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
        startbit = 434
        byte = 54
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class AmbIllmnFwdStsAmbIllmn2:
        sig_name = "AmbIllmnFwdStsAmbIllmn2"
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

    class FLDoorManResistCtrl:
        sig_name = "FLDoorManResistCtrl"
        sig_start_bit = 55
        update_id_bit = 282
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
        startbit = 55
        byte = 6
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class RemClimaReqIndcr:
        sig_name = "RemClimaReqIndcr"
        sig_start_bit = 286
        update_id_bit = 293
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flg1_Rst': 0, 'Flg1_Set': 1}
        compute_method = None
        length = 1
        startbit = 286
        byte = 35
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class CmptmtAirFlwEstimdFrnt:
        sig_name = "CmptmtAirFlwEstimdFrnt"
        sig_start_bit = 31
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
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11000000, 0b00111111, 2, 6)]

    class HudSnsrErr_UB:
        sig_name = "HudSnsrErr_UB"
        sig_start_bit = 272
        update_id_bit = 272
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
        startbit = 272
        byte = 34
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class HudSnsrErrParChk:
        sig_name = "HudSnsrErrParChk"
        sig_start_bit = 279
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ParChk_Unevennrof': 0, 'ParChk_Evennrof': 1}
        compute_method = None
        length = 1
        startbit = 279
        byte = 34
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7


class LCULToDPODLCULCANFD1DiagReqFrame:
    msg_name = "LCULToDPODLCULCANFD1DiagReqFrame"
    msg_id = 1856
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "LCUL"
    rx_nodes = ['DPOD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


