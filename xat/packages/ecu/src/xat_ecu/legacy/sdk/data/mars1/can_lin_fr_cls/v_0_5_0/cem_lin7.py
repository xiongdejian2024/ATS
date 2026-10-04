class CemCem_Lin7Fr01:
    msg_name = "CemCem_Lin7Fr01"
    msg_id = 6
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 7
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class DoorsOpenerReqVehMtnSts:
        sig_name = "DoorsOpenerReqVehMtnSts"
        sig_start_bit = 32
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
        startbit = 32
        byte = 4
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class DoorsOpenerReqTrigSrcPass:
        sig_name = "DoorsOpenerReqTrigSrcPass"
        sig_start_bit = 24
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoTrigSrc': 0, 'KeyRem': 1, 'HMI': 2, 'Telm': 3, 'OutdSwt': 4, 'InsdSwt': 5}
        compute_method = None
        length = 3
        startbit = 24
        byte = 3
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class DoorsOpenerReqTrigSrcDrvr:
        sig_name = "DoorsOpenerReqTrigSrcDrvr"
        sig_start_bit = 16
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoTrigSrc': 0, 'KeyRem': 1, 'HMI': 2, 'Telm': 3, 'OutdSwt': 4, 'InsdSwt': 5}
        compute_method = None
        length = 3
        startbit = 16
        byte = 2
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class DoorsOpenerReqDrvr:
        sig_name = "DoorsOpenerReqDrvr"
        sig_start_bit = 12
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorOpenerIdle': 0, 'DoorOpenerOpen': 1, 'DoorOpenerCls': 2, 'DoorOpenerStop': 3}
        compute_method = None
        length = 2
        startbit = 12
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class DoorsOpenerReqTrigSrcRiRe:
        sig_name = "DoorsOpenerReqTrigSrcRiRe"
        sig_start_bit = 27
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoTrigSrc': 0, 'KeyRem': 1, 'HMI': 2, 'Telm': 3, 'OutdSwt': 4, 'InsdSwt': 5}
        compute_method = None
        length = 3
        startbit = 27
        byte = 3
        mask = 0b00111000
        unmask = 0b11000111
        shift = 3

    class DoorsOpenerReqChks:
        sig_name = "DoorsOpenerReqChks"
        sig_start_bit = 0
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

    class DoorsOpenerReqPass:
        sig_name = "DoorsOpenerReqPass"
        sig_start_bit = 22
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorOpenerIdle': 0, 'DoorOpenerOpen': 1, 'DoorOpenerCls': 2, 'DoorOpenerStop': 3}
        compute_method = None
        length = 2
        startbit = 22
        byte = 2
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class DoorsOpenerReqTrigSrcLeRe:
        sig_name = "DoorsOpenerReqTrigSrcLeRe"
        sig_start_bit = 19
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoTrigSrc': 0, 'KeyRem': 1, 'HMI': 2, 'Telm': 3, 'OutdSwt': 4, 'InsdSwt': 5}
        compute_method = None
        length = 3
        startbit = 19
        byte = 2
        mask = 0b00111000
        unmask = 0b11000111
        shift = 3

    class DoorsOpenerReqRiRe:
        sig_name = "DoorsOpenerReqRiRe"
        sig_start_bit = 30
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorOpenerIdle': 0, 'DoorOpenerOpen': 1, 'DoorOpenerCls': 2, 'DoorOpenerStop': 3}
        compute_method = None
        length = 2
        startbit = 30
        byte = 3
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class DoorsOpenerReqCntr:
        sig_name = "DoorsOpenerReqCntr"
        sig_start_bit = 8
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
        startbit = 8
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DoorsOpenerReqLeRe:
        sig_name = "DoorsOpenerReqLeRe"
        sig_start_bit = 14
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorOpenerIdle': 0, 'DoorOpenerOpen': 1, 'DoorOpenerCls': 2, 'DoorOpenerStop': 3}
        compute_method = None
        length = 2
        startbit = 14
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class RpodCem_Lin7Fr01:
    msg_name = "RpodCem_Lin7Fr01"
    msg_id = 42
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 7
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class DoorRiRePosn:
        sig_name = "DoorRiRePosn"
        sig_start_bit = 16
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Intel"
        sig_value_init = 71
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 16
        byte = 2
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class DtcInfDoorRiReBoolean10:
        sig_name = "DtcInfDoorRiReBoolean10"
        sig_start_bit = 41
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
        startbit = 41
        byte = 5
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class DtcInfDoorRiReBoolean12:
        sig_name = "DtcInfDoorRiReBoolean12"
        sig_start_bit = 43
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
        startbit = 43
        byte = 5
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class DoorOpenerRiReSts_0_RpodCem_Lin7SignalIPdu01:
        sig_name = "DoorOpenerRiReSts_0_RpodCem_Lin7SignalIPdu01"
        sig_start_bit = 0
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorOpenerSts_Ukwn': 0, 'DoorOpenerSts_FullClsd': 1, 'DoorOpenerSts_MovgOut': 2, 'DoorOpenerSts_MovgOutBrkg': 3, 'DoorOpenerSts_StopDurgOpen': 4, 'DoorOpenerSts_FullOpend': 5, 'DoorOpenerSts_MovgIn': 6, 'DoorOpenerSts_MovgInBrkg': 7, 'DoorOpenerSts_StopDurgCls': 8, 'DoorOpenerSts_HalfClsd': 9, 'DoorOpenerSts_StopMinPntForCls': 10}
        compute_method = None
        length = 4
        startbit = 0
        byte = 0
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DtcInfDoorRiReBoolean5:
        sig_name = "DtcInfDoorRiReBoolean5"
        sig_start_bit = 36
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
        startbit = 36
        byte = 4
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class DoorRiReAntiPnch:
        sig_name = "DoorRiReAntiPnch"
        sig_start_bit = 4
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

    class DtcInfDoorRiReBoolean7:
        sig_name = "DtcInfDoorRiReBoolean7"
        sig_start_bit = 38
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
        startbit = 38
        byte = 4
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class DtcInfDoorRiReBoolean14:
        sig_name = "DtcInfDoorRiReBoolean14"
        sig_start_bit = 45
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
        startbit = 45
        byte = 5
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class DtcInfDoorRiReBoolean6:
        sig_name = "DtcInfDoorRiReBoolean6"
        sig_start_bit = 37
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
        startbit = 37
        byte = 4
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class DtcInfDoorRiReBoolean11:
        sig_name = "DtcInfDoorRiReBoolean11"
        sig_start_bit = 42
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
        startbit = 42
        byte = 5
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class DtcInfDoorRiReBoolean1:
        sig_name = "DtcInfDoorRiReBoolean1"
        sig_start_bit = 32
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
        startbit = 32
        byte = 4
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class DoorRiReOpenReqInsdSwt2:
        sig_name = "DoorRiReOpenReqInsdSwt2"
        sig_start_bit = 24
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PsdNotPsd3_NoInfo1': 0, 'PsdNotPsd3_Psd': 1, 'PsdNotPsd3_NotPsd': 2, 'PsdNotPsd3_NoInfo2': 3}
        compute_method = None
        length = 2
        startbit = 24
        byte = 3
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class DtcInfDoorRiReBoolean13:
        sig_name = "DtcInfDoorRiReBoolean13"
        sig_start_bit = 44
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
        startbit = 44
        byte = 5
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class DtcInfDoorRiReBoolean4:
        sig_name = "DtcInfDoorRiReBoolean4"
        sig_start_bit = 35
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
        startbit = 35
        byte = 4
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class DtcInfDoorRiReBoolean3:
        sig_name = "DtcInfDoorRiReBoolean3"
        sig_start_bit = 34
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
        startbit = 34
        byte = 4
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class DoorRiReOpenReqOutdSwt2:
        sig_name = "DoorRiReOpenReqOutdSwt2"
        sig_start_bit = 26
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PsdNotPsd3_NoInfo1': 0, 'PsdNotPsd3_Psd': 1, 'PsdNotPsd3_NotPsd': 2, 'PsdNotPsd3_NoInfo2': 3}
        compute_method = None
        length = 2
        startbit = 26
        byte = 3
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class DtcInfDoorRiReBoolean2:
        sig_name = "DtcInfDoorRiReBoolean2"
        sig_start_bit = 33
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

    class DtcInfDoorRiReBoolean9:
        sig_name = "DtcInfDoorRiReBoolean9"
        sig_start_bit = 40
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
        startbit = 40
        byte = 5
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class DtcInfDoorRiReBoolean8:
        sig_name = "DtcInfDoorRiReBoolean8"
        sig_start_bit = 39
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
        startbit = 39
        byte = 4
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7


class CemCem_Lin7Fr02:
    msg_name = "CemCem_Lin7Fr02"
    msg_id = 13
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 7
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class DoorLeReSts_2_CemCem_Lin7SignalIPdu02:
        sig_name = "DoorLeReSts_2_CemCem_Lin7SignalIPdu02"
        sig_start_bit = 4
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorSts2_Ukwn': 0, 'DoorSts2_Opend': 1, 'DoorSts2_Clsd': 2}
        compute_method = None
        length = 2
        startbit = 4
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class DoorRiReSts_2_CemCem_Lin7SignalIPdu02:
        sig_name = "DoorRiReSts_2_CemCem_Lin7SignalIPdu02"
        sig_start_bit = 6
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorSts2_Ukwn': 0, 'DoorSts2_Opend': 1, 'DoorSts2_Clsd': 2}
        compute_method = None
        length = 2
        startbit = 6
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class DoorLeReLatPawlSt_1_CemCem_Lin7SignalIPdu02:
        sig_name = "DoorLeReLatPawlSt_1_CemCem_Lin7SignalIPdu02"
        sig_start_bit = 12
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorSts2_Ukwn': 0, 'DoorSts2_Opend': 1, 'DoorSts2_Clsd': 2}
        compute_method = None
        length = 2
        startbit = 12
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class DoorLeReLatPosn_1_CemCem_Lin7SignalIPdu02:
        sig_name = "DoorLeReLatPosn_1_CemCem_Lin7SignalIPdu02"
        sig_start_bit = 20
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorPos_Undefined': 0, 'DoorPos_FullyClosed': 1, 'DoorPos_SecondaryPosition': 2, 'DoorPos_FullyOpen': 3}
        compute_method = None
        length = 2
        startbit = 20
        byte = 2
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class ObstStrDetcn:
        sig_name = "ObstStrDetcn"
        sig_start_bit = 55
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
        startbit = 55
        byte = 6
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class DoorRiReLatPosn_1_CemCem_Lin7SignalIPdu02:
        sig_name = "DoorRiReLatPosn_1_CemCem_Lin7SignalIPdu02"
        sig_start_bit = 22
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorPos_Undefined': 0, 'DoorPos_FullyClosed': 1, 'DoorPos_SecondaryPosition': 2, 'DoorPos_FullyOpen': 3}
        compute_method = None
        length = 2
        startbit = 22
        byte = 2
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class RollAgGlbForPOD:
        sig_name = "RollAgGlbForPOD"
        sig_start_bit = 40
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Intel"
        sig_value_init = 8
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PitchAndRoll_Invalid': 0, 'PitchAndRoll_Neg14': 1, 'PitchAndRoll_Neg13': 2, 'PitchAndRoll_Neg12': 3, 'PitchAndRoll_Neg11': 4, 'PitchAndRoll_Neg10': 5, 'PitchAndRoll_Neg9': 6, 'PitchAndRoll_Neg8': 7, 'PitchAndRoll_Neg7': 8, 'PitchAndRoll_Neg6': 9, 'PitchAndRoll_Neg5': 10, 'PitchAndRoll_Neg4': 11, 'PitchAndRoll_Neg3': 12, 'PitchAndRoll_Neg2': 13, 'PitchAndRoll_Neg1': 14, 'PitchAndRoll_Pos0': 15, 'PitchAndRoll_Pos1': 16, 'PitchAndRoll_Pos2': 17, 'PitchAndRoll_Pos3': 18, 'PitchAndRoll_Pos4': 19, 'PitchAndRoll_Pos5': 20, 'PitchAndRoll_Pos6': 21, 'PitchAndRoll_Pos7': 22, 'PitchAndRoll_Pos8': 23, 'PitchAndRoll_Pos9': 24, 'PitchAndRoll_Pos10': 25, 'PitchAndRoll_Pos11': 26, 'PitchAndRoll_Pos12': 27, 'PitchAndRoll_Pos13': 28, 'PitchAndRoll_Pos14': 29, 'PitchAndRoll_Reserved1': 30, 'PitchAndRoll_Reserved2': 31}
        compute_method = None
        length = 5
        startbit = 40
        byte = 5
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class RoadInclnForPOD:
        sig_name = "RoadInclnForPOD"
        sig_start_bit = 35
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Intel"
        sig_value_init = 8
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PitchAndRoll_Invalid': 0, 'PitchAndRoll_Neg14': 1, 'PitchAndRoll_Neg13': 2, 'PitchAndRoll_Neg12': 3, 'PitchAndRoll_Neg11': 4, 'PitchAndRoll_Neg10': 5, 'PitchAndRoll_Neg9': 6, 'PitchAndRoll_Neg8': 7, 'PitchAndRoll_Neg7': 8, 'PitchAndRoll_Neg6': 9, 'PitchAndRoll_Neg5': 10, 'PitchAndRoll_Neg4': 11, 'PitchAndRoll_Neg3': 12, 'PitchAndRoll_Neg2': 13, 'PitchAndRoll_Neg1': 14, 'PitchAndRoll_Pos0': 15, 'PitchAndRoll_Pos1': 16, 'PitchAndRoll_Pos2': 17, 'PitchAndRoll_Pos3': 18, 'PitchAndRoll_Pos4': 19, 'PitchAndRoll_Pos5': 20, 'PitchAndRoll_Pos6': 21, 'PitchAndRoll_Pos7': 22, 'PitchAndRoll_Pos8': 23, 'PitchAndRoll_Pos9': 24, 'PitchAndRoll_Pos10': 25, 'PitchAndRoll_Pos11': 26, 'PitchAndRoll_Pos12': 27, 'PitchAndRoll_Pos13': 28, 'PitchAndRoll_Pos14': 29, 'PitchAndRoll_Reserved1': 30, 'PitchAndRoll_Reserved2': 31}
        compute_method = None
        length = 5
        startbit = 35
        byte = 4
        mask = 0b11111000
        unmask = 0b00000111
        shift = 3

    class DoorDrvrSts_3_CemCem_Lin7SignalIPdu02:
        sig_name = "DoorDrvrSts_3_CemCem_Lin7SignalIPdu02"
        sig_start_bit = 0
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorSts2_Ukwn': 0, 'DoorSts2_Opend': 1, 'DoorSts2_Clsd': 2}
        compute_method = None
        length = 2
        startbit = 0
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class DoorPassLatPosn_1_CemCem_Lin7SignalIPdu02:
        sig_name = "DoorPassLatPosn_1_CemCem_Lin7SignalIPdu02"
        sig_start_bit = 18
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorPos_Undefined': 0, 'DoorPos_FullyClosed': 1, 'DoorPos_SecondaryPosition': 2, 'DoorPos_FullyOpen': 3}
        compute_method = None
        length = 2
        startbit = 18
        byte = 2
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class TempPodSys_1_CemCem_Lin7SignalIPdu02:
        sig_name = "TempPodSys_1_CemCem_Lin7SignalIPdu02"
        sig_start_bit = 48
        sig_length = 7
        sig_value_factor = 1.0
        sig_value_offset = "-40.0"
        sig_value_min = 0
        sig_value_max = 125
        sig_byteorder = "Intel"
        sig_value_init = 121
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 48
        byte = 6
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class DoorPassLatPawlSt_1_CemCem_Lin7SignalIPdu02:
        sig_name = "DoorPassLatPawlSt_1_CemCem_Lin7SignalIPdu02"
        sig_start_bit = 10
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorSts2_Ukwn': 0, 'DoorSts2_Opend': 1, 'DoorSts2_Clsd': 2}
        compute_method = None
        length = 2
        startbit = 10
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class CabPressPodCalc:
        sig_name = "CabPressPodCalc"
        sig_start_bit = 45
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PresScale_Undefined': 0, 'PresScale_VeryLow': 1, 'PresScale_Low': 2, 'PresScale_Medium': 3, 'PresScale_High': 4, 'PresScale_VeryHigh': 5}
        compute_method = None
        length = 3
        startbit = 45
        byte = 5
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DoorDrvrLatPosn_1_CemCem_Lin7SignalIPdu02:
        sig_name = "DoorDrvrLatPosn_1_CemCem_Lin7SignalIPdu02"
        sig_start_bit = 16
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorPos_Undefined': 0, 'DoorPos_FullyClosed': 1, 'DoorPos_SecondaryPosition': 2, 'DoorPos_FullyOpen': 3}
        compute_method = None
        length = 2
        startbit = 16
        byte = 2
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class RadioFrqAM_2_CemCem_Lin7SignalIPdu02:
        sig_name = "RadioFrqAM_2_CemCem_Lin7SignalIPdu02"
        sig_start_bit = 24
        sig_length = 11
        sig_value_factor = 1
        sig_value_offset = 522
        sig_value_min = 0
        sig_value_max = 1188
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 24
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11100000, 0b00011111, 3, 5)]

    class DoorPassSts_3_CemCem_Lin7SignalIPdu02:
        sig_name = "DoorPassSts_3_CemCem_Lin7SignalIPdu02"
        sig_start_bit = 2
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorSts2_Ukwn': 0, 'DoorSts2_Opend': 1, 'DoorSts2_Clsd': 2}
        compute_method = None
        length = 2
        startbit = 2
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class DoorRiReLatPawlSt_1_CemCem_Lin7SignalIPdu02:
        sig_name = "DoorRiReLatPawlSt_1_CemCem_Lin7SignalIPdu02"
        sig_start_bit = 14
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorSts2_Ukwn': 0, 'DoorSts2_Opend': 1, 'DoorSts2_Clsd': 2}
        compute_method = None
        length = 2
        startbit = 14
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class DoorDrvrLatPawlSt_1_CemCem_Lin7SignalIPdu02:
        sig_name = "DoorDrvrLatPawlSt_1_CemCem_Lin7SignalIPdu02"
        sig_start_bit = 8
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorSts2_Ukwn': 0, 'DoorSts2_Opend': 1, 'DoorSts2_Clsd': 2}
        compute_method = None
        length = 2
        startbit = 8
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0


class DpodCem_Lin7Fr01:
    msg_name = "DpodCem_Lin7Fr01"
    msg_id = 23
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 7
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class DoorDrvrOpenReqOutdSwt2:
        sig_name = "DoorDrvrOpenReqOutdSwt2"
        sig_start_bit = 26
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PsdNotPsd3_NoInfo1': 0, 'PsdNotPsd3_Psd': 1, 'PsdNotPsd3_NotPsd': 2, 'PsdNotPsd3_NoInfo2': 3}
        compute_method = None
        length = 2
        startbit = 26
        byte = 3
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class DtcInfDoorDrvrBoolean12:
        sig_name = "DtcInfDoorDrvrBoolean12"
        sig_start_bit = 43
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
        startbit = 43
        byte = 5
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class DtcInfDoorDrvrBoolean7:
        sig_name = "DtcInfDoorDrvrBoolean7"
        sig_start_bit = 38
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
        startbit = 38
        byte = 4
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class DoorOpenerDrvrSts_0_DpodCem_Lin7SignalIPdu01:
        sig_name = "DoorOpenerDrvrSts_0_DpodCem_Lin7SignalIPdu01"
        sig_start_bit = 0
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorOpenerSts_Ukwn': 0, 'DoorOpenerSts_FullClsd': 1, 'DoorOpenerSts_MovgOut': 2, 'DoorOpenerSts_MovgOutBrkg': 3, 'DoorOpenerSts_StopDurgOpen': 4, 'DoorOpenerSts_FullOpend': 5, 'DoorOpenerSts_MovgIn': 6, 'DoorOpenerSts_MovgInBrkg': 7, 'DoorOpenerSts_StopDurgCls': 8, 'DoorOpenerSts_HalfClsd': 9, 'DoorOpenerSts_StopMinPntForCls': 10}
        compute_method = None
        length = 4
        startbit = 0
        byte = 0
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DoorDrvrPosn:
        sig_name = "DoorDrvrPosn"
        sig_start_bit = 16
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Intel"
        sig_value_init = 71
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 16
        byte = 2
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class DtcInfDoorDrvrBoolean11:
        sig_name = "DtcInfDoorDrvrBoolean11"
        sig_start_bit = 42
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
        startbit = 42
        byte = 5
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class DoorDrvrOpenReqInsdSwt2:
        sig_name = "DoorDrvrOpenReqInsdSwt2"
        sig_start_bit = 24
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PsdNotPsd3_NoInfo1': 0, 'PsdNotPsd3_Psd': 1, 'PsdNotPsd3_NotPsd': 2, 'PsdNotPsd3_NoInfo2': 3}
        compute_method = None
        length = 2
        startbit = 24
        byte = 3
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class DtcInfDoorDrvrBoolean10:
        sig_name = "DtcInfDoorDrvrBoolean10"
        sig_start_bit = 41
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
        startbit = 41
        byte = 5
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class DtcInfDoorDrvrBoolean4:
        sig_name = "DtcInfDoorDrvrBoolean4"
        sig_start_bit = 35
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
        startbit = 35
        byte = 4
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class DtcInfDoorDrvrBoolean2:
        sig_name = "DtcInfDoorDrvrBoolean2"
        sig_start_bit = 33
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

    class DtcInfDoorDrvrBoolean9:
        sig_name = "DtcInfDoorDrvrBoolean9"
        sig_start_bit = 40
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
        startbit = 40
        byte = 5
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class DtcInfDoorDrvrBoolean13:
        sig_name = "DtcInfDoorDrvrBoolean13"
        sig_start_bit = 44
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
        startbit = 44
        byte = 5
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class DtcInfDoorDrvrBoolean8:
        sig_name = "DtcInfDoorDrvrBoolean8"
        sig_start_bit = 39
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
        startbit = 39
        byte = 4
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class DtcInfDoorDrvrBoolean1:
        sig_name = "DtcInfDoorDrvrBoolean1"
        sig_start_bit = 32
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
        startbit = 32
        byte = 4
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class DtcInfDoorDrvrBoolean6:
        sig_name = "DtcInfDoorDrvrBoolean6"
        sig_start_bit = 37
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
        startbit = 37
        byte = 4
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class DtcInfDoorDrvrBoolean14:
        sig_name = "DtcInfDoorDrvrBoolean14"
        sig_start_bit = 45
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
        startbit = 45
        byte = 5
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class DoorDrvrAntiPnch:
        sig_name = "DoorDrvrAntiPnch"
        sig_start_bit = 4
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

    class DtcInfDoorDrvrBoolean3:
        sig_name = "DtcInfDoorDrvrBoolean3"
        sig_start_bit = 34
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
        startbit = 34
        byte = 4
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class DtcInfDoorDrvrBoolean5:
        sig_name = "DtcInfDoorDrvrBoolean5"
        sig_start_bit = 36
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
        startbit = 36
        byte = 4
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4


class PpodCem_Lin7Fr01:
    msg_name = "PpodCem_Lin7Fr01"
    msg_id = 34
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 7
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class DtcInfDoorPassBoolean10:
        sig_name = "DtcInfDoorPassBoolean10"
        sig_start_bit = 41
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
        startbit = 41
        byte = 5
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class DtcInfDoorPassBoolean13:
        sig_name = "DtcInfDoorPassBoolean13"
        sig_start_bit = 44
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
        startbit = 44
        byte = 5
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class DtcInfDoorPassBoolean1:
        sig_name = "DtcInfDoorPassBoolean1"
        sig_start_bit = 32
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
        startbit = 32
        byte = 4
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class DoorOpenerPassSts_0_PpodCem_Lin7SignalIPdu01:
        sig_name = "DoorOpenerPassSts_0_PpodCem_Lin7SignalIPdu01"
        sig_start_bit = 0
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorOpenerSts_Ukwn': 0, 'DoorOpenerSts_FullClsd': 1, 'DoorOpenerSts_MovgOut': 2, 'DoorOpenerSts_MovgOutBrkg': 3, 'DoorOpenerSts_StopDurgOpen': 4, 'DoorOpenerSts_FullOpend': 5, 'DoorOpenerSts_MovgIn': 6, 'DoorOpenerSts_MovgInBrkg': 7, 'DoorOpenerSts_StopDurgCls': 8, 'DoorOpenerSts_HalfClsd': 9, 'DoorOpenerSts_StopMinPntForCls': 10}
        compute_method = None
        length = 4
        startbit = 0
        byte = 0
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DtcInfDoorPassBoolean11:
        sig_name = "DtcInfDoorPassBoolean11"
        sig_start_bit = 42
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
        startbit = 42
        byte = 5
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class DtcInfDoorPassBoolean8:
        sig_name = "DtcInfDoorPassBoolean8"
        sig_start_bit = 39
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
        startbit = 39
        byte = 4
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class DtcInfDoorPassBoolean2:
        sig_name = "DtcInfDoorPassBoolean2"
        sig_start_bit = 33
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

    class DtcInfDoorPassBoolean3:
        sig_name = "DtcInfDoorPassBoolean3"
        sig_start_bit = 34
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
        startbit = 34
        byte = 4
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class DtcInfDoorPassBoolean14:
        sig_name = "DtcInfDoorPassBoolean14"
        sig_start_bit = 45
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
        startbit = 45
        byte = 5
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class DtcInfDoorPassBoolean6:
        sig_name = "DtcInfDoorPassBoolean6"
        sig_start_bit = 37
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
        startbit = 37
        byte = 4
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class DtcInfDoorPassBoolean7:
        sig_name = "DtcInfDoorPassBoolean7"
        sig_start_bit = 38
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
        startbit = 38
        byte = 4
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class DtcInfDoorPassBoolean9:
        sig_name = "DtcInfDoorPassBoolean9"
        sig_start_bit = 40
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
        startbit = 40
        byte = 5
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class DtcInfDoorPassBoolean4:
        sig_name = "DtcInfDoorPassBoolean4"
        sig_start_bit = 35
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
        startbit = 35
        byte = 4
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class DtcInfDoorPassBoolean5:
        sig_name = "DtcInfDoorPassBoolean5"
        sig_start_bit = 36
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
        startbit = 36
        byte = 4
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class DoorPassOpenReqInsdSwt2:
        sig_name = "DoorPassOpenReqInsdSwt2"
        sig_start_bit = 24
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PsdNotPsd3_NoInfo1': 0, 'PsdNotPsd3_Psd': 1, 'PsdNotPsd3_NotPsd': 2, 'PsdNotPsd3_NoInfo2': 3}
        compute_method = None
        length = 2
        startbit = 24
        byte = 3
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class DtcInfDoorPassBoolean12:
        sig_name = "DtcInfDoorPassBoolean12"
        sig_start_bit = 43
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
        startbit = 43
        byte = 5
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class DoorPassPosn:
        sig_name = "DoorPassPosn"
        sig_start_bit = 16
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Intel"
        sig_value_init = 71
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 16
        byte = 2
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class DoorPassAntiPnch:
        sig_name = "DoorPassAntiPnch"
        sig_start_bit = 4
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

    class DoorPassOpenReqOutdSwt2:
        sig_name = "DoorPassOpenReqOutdSwt2"
        sig_start_bit = 26
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PsdNotPsd3_NoInfo1': 0, 'PsdNotPsd3_Psd': 1, 'PsdNotPsd3_NotPsd': 2, 'PsdNotPsd3_NoInfo2': 3}
        compute_method = None
        length = 2
        startbit = 26
        byte = 3
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2


class LpodCem_Lin7Fr01:
    msg_name = "LpodCem_Lin7Fr01"
    msg_id = 24
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 7
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class DtcInfDoorLeReBoolean13:
        sig_name = "DtcInfDoorLeReBoolean13"
        sig_start_bit = 44
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
        startbit = 44
        byte = 5
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class DtcInfDoorLeReBoolean10:
        sig_name = "DtcInfDoorLeReBoolean10"
        sig_start_bit = 41
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
        startbit = 41
        byte = 5
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class DoorLeRePosn:
        sig_name = "DoorLeRePosn"
        sig_start_bit = 16
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Intel"
        sig_value_init = 71
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 16
        byte = 2
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class DoorLeReOpenReqInsdSwt2:
        sig_name = "DoorLeReOpenReqInsdSwt2"
        sig_start_bit = 24
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PsdNotPsd3_NoInfo1': 0, 'PsdNotPsd3_Psd': 1, 'PsdNotPsd3_NotPsd': 2, 'PsdNotPsd3_NoInfo2': 3}
        compute_method = None
        length = 2
        startbit = 24
        byte = 3
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class DtcInfDoorLeReBoolean1:
        sig_name = "DtcInfDoorLeReBoolean1"
        sig_start_bit = 32
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
        startbit = 32
        byte = 4
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class DtcInfDoorLeReBoolean8:
        sig_name = "DtcInfDoorLeReBoolean8"
        sig_start_bit = 39
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
        startbit = 39
        byte = 4
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class DtcInfDoorLeReBoolean9:
        sig_name = "DtcInfDoorLeReBoolean9"
        sig_start_bit = 40
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
        startbit = 40
        byte = 5
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class DtcInfDoorLeReBoolean11:
        sig_name = "DtcInfDoorLeReBoolean11"
        sig_start_bit = 42
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
        startbit = 42
        byte = 5
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class DoorLeReAntiPnch:
        sig_name = "DoorLeReAntiPnch"
        sig_start_bit = 4
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

    class DtcInfDoorLeReBoolean5:
        sig_name = "DtcInfDoorLeReBoolean5"
        sig_start_bit = 36
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
        startbit = 36
        byte = 4
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class DtcInfDoorLeReBoolean3:
        sig_name = "DtcInfDoorLeReBoolean3"
        sig_start_bit = 34
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
        startbit = 34
        byte = 4
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class DtcInfDoorLeReBoolean4:
        sig_name = "DtcInfDoorLeReBoolean4"
        sig_start_bit = 35
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
        startbit = 35
        byte = 4
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class DtcInfDoorLeReBoolean12:
        sig_name = "DtcInfDoorLeReBoolean12"
        sig_start_bit = 43
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
        startbit = 43
        byte = 5
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class DtcInfDoorLeReBoolean7:
        sig_name = "DtcInfDoorLeReBoolean7"
        sig_start_bit = 38
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
        startbit = 38
        byte = 4
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class DtcInfDoorLeReBoolean2:
        sig_name = "DtcInfDoorLeReBoolean2"
        sig_start_bit = 33
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

    class DtcInfDoorLeReBoolean6:
        sig_name = "DtcInfDoorLeReBoolean6"
        sig_start_bit = 37
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
        startbit = 37
        byte = 4
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class DoorLeReOpenReqOutdSwt2:
        sig_name = "DoorLeReOpenReqOutdSwt2"
        sig_start_bit = 26
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PsdNotPsd3_NoInfo1': 0, 'PsdNotPsd3_Psd': 1, 'PsdNotPsd3_NotPsd': 2, 'PsdNotPsd3_NoInfo2': 3}
        compute_method = None
        length = 2
        startbit = 26
        byte = 3
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class DtcInfDoorLeReBoolean14:
        sig_name = "DtcInfDoorLeReBoolean14"
        sig_start_bit = 45
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
        startbit = 45
        byte = 5
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class DoorOpenerLeReSts_0_LpodCem_Lin7SignalIPdu01:
        sig_name = "DoorOpenerLeReSts_0_LpodCem_Lin7SignalIPdu01"
        sig_start_bit = 0
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorOpenerSts_Ukwn': 0, 'DoorOpenerSts_FullClsd': 1, 'DoorOpenerSts_MovgOut': 2, 'DoorOpenerSts_MovgOutBrkg': 3, 'DoorOpenerSts_StopDurgOpen': 4, 'DoorOpenerSts_FullOpend': 5, 'DoorOpenerSts_MovgIn': 6, 'DoorOpenerSts_MovgInBrkg': 7, 'DoorOpenerSts_StopDurgCls': 8, 'DoorOpenerSts_HalfClsd': 9, 'DoorOpenerSts_StopMinPntForCls': 10}
        compute_method = None
        length = 4
        startbit = 0
        byte = 0
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0


class Cem_Lin7LinTpDiagRespFrame:
    msg_name = "Cem_Lin7LinTpDiagRespFrame"
    msg_id = 61
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']


class DrmCem_Lin7Fr01:
    msg_name = "DrmCem_Lin7Fr01"
    msg_id = 14
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 7
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class DoorDrvrObstclDetn:
        sig_name = "DoorDrvrObstclDetn"
        sig_start_bit = 0
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
        startbit = 0
        byte = 0
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class DtcInfDoorObsDnBoolean5:
        sig_name = "DtcInfDoorObsDnBoolean5"
        sig_start_bit = 12
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
        startbit = 12
        byte = 1
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class DtcInfDoorObsDnBoolean6:
        sig_name = "DtcInfDoorObsDnBoolean6"
        sig_start_bit = 13
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
        startbit = 13
        byte = 1
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class DoorDrvrPosnToObst:
        sig_name = "DoorDrvrPosnToObst"
        sig_start_bit = 16
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Intel"
        sig_value_init = 98
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 16
        byte = 2
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class DoorPassPosnToObst:
        sig_name = "DoorPassPosnToObst"
        sig_start_bit = 32
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Intel"
        sig_value_init = 98
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 32
        byte = 4
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class DtcInfDoorObsDnBoolean1:
        sig_name = "DtcInfDoorObsDnBoolean1"
        sig_start_bit = 8
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
        startbit = 8
        byte = 1
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class DoorRiRePosnToObst:
        sig_name = "DoorRiRePosnToObst"
        sig_start_bit = 40
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Intel"
        sig_value_init = 98
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 40
        byte = 5
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class DoorRiReObstclDetn:
        sig_name = "DoorRiReObstclDetn"
        sig_start_bit = 3
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
        startbit = 3
        byte = 0
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class DtcInfDoorObsDnBoolean8:
        sig_name = "DtcInfDoorObsDnBoolean8"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class DoorLeReObstclDetn:
        sig_name = "DoorLeReObstclDetn"
        sig_start_bit = 1
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
        startbit = 1
        byte = 0
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class DoorObstclDetnCntr:
        sig_name = "DoorObstclDetnCntr"
        sig_start_bit = 4
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 2
        startbit = 4
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class DtcInfDoorObsDnBoolean4:
        sig_name = "DtcInfDoorObsDnBoolean4"
        sig_start_bit = 11
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
        startbit = 11
        byte = 1
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class DtcInfDoorObsDnBoolean7:
        sig_name = "DtcInfDoorObsDnBoolean7"
        sig_start_bit = 14
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
        startbit = 14
        byte = 1
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class DoorLeRePosnToObst:
        sig_name = "DoorLeRePosnToObst"
        sig_start_bit = 24
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Intel"
        sig_value_init = 98
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 24
        byte = 3
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class DoorPassObstclDetn:
        sig_name = "DoorPassObstclDetn"
        sig_start_bit = 2
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
        startbit = 2
        byte = 0
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class DtcInfDoorObsDnBoolean3:
        sig_name = "DtcInfDoorObsDnBoolean3"
        sig_start_bit = 10
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
        startbit = 10
        byte = 1
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class DtcInfDoorObsDnBoolean9:
        sig_name = "DtcInfDoorObsDnBoolean9"
        sig_start_bit = 6
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

    class DtcInfDoorObsDnBoolean10:
        sig_name = "DtcInfDoorObsDnBoolean10"
        sig_start_bit = 7
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
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class DtcInfDoorObsDnBoolean2:
        sig_name = "DtcInfDoorObsDnBoolean2"
        sig_start_bit = 9
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
        startbit = 9
        byte = 1
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1


class Cem_Lin7LinTpDiagReqFrame:
    msg_name = "Cem_Lin7LinTpDiagReqFrame"
    msg_id = 60
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']


