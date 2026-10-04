class VgmConnFr21:
    msg_name = "VgmConnFr21"
    msg_id = 824
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['TCAM', 'BNCM']

    class RemClimaExtnTiRspn_1_VgmConnSignalIPdu21:
        sig_name = "RemClimaExtnTiRspn_1_VgmConnSignalIPdu21"
        sig_start_bit = 21
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
        startbit = 21
        byte = 2
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class ClimaOvrHeatProWarn_1_VgmConnSignalIPdu21:
        sig_name = "ClimaOvrHeatProWarn_1_VgmConnSignalIPdu21"
        sig_start_bit = 28
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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

    class BodyRemoteCarFindFBReserveSignal1:
        sig_name = "BodyRemoteCarFindFBReserveSignal1"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
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

    class RemClimaDelaySts_1_VgmConnSignalIPdu21:
        sig_name = "RemClimaDelaySts_1_VgmConnSignalIPdu21"
        sig_start_bit = 31
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

    class MobDevRPASts:
        sig_name = "MobDevRPASts"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
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

    class BodyRemoteCarFindFBStatus:
        sig_name = "BodyRemoteCarFindFBStatus"
        sig_start_bit = 63
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 11
        sig_byteorder = "Motorola"
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

    class RemStrtClimaRspn_1_VgmConnSignalIPdu21:
        sig_name = "RemStrtClimaRspn_1_VgmConnSignalIPdu21"
        sig_start_bit = 4
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
        startbit = 4
        byte = 0
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class ClimaOvrHeatProRspn_1_VgmConnSignalIPdu21:
        sig_name = "ClimaOvrHeatProRspn_1_VgmConnSignalIPdu21"
        sig_start_bit = 3
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
        startbit = 3
        byte = 0
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class RemClimaWarn_1_VgmConnSignalIPdu21:
        sig_name = "RemClimaWarn_1_VgmConnSignalIPdu21"
        sig_start_bit = 19
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 8
        sig_byteorder = "Motorola"
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

    class RemClimaHvRspn_1_VgmConnSignalIPdu21:
        sig_name = "RemClimaHvRspn_1_VgmConnSignalIPdu21"
        sig_start_bit = 39
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
        startbit = 39
        byte = 4
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7


class VgmConnFr06:
    msg_name = "VgmConnFr06"
    msg_id = 816
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['TCAM', 'BNCM']

    class VehCfgPrmCCPBytePosn4_4_VgmConnSignalIPdu06:
        sig_name = "VehCfgPrmCCPBytePosn4_4_VgmConnSignalIPdu06"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
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

    class VehCfgPrmCCPBytePosn7_4_VgmConnSignalIPdu06:
        sig_name = "VehCfgPrmCCPBytePosn7_4_VgmConnSignalIPdu06"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
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

    class VehCfgPrmCCPBytePosn3_4_VgmConnSignalIPdu06:
        sig_name = "VehCfgPrmCCPBytePosn3_4_VgmConnSignalIPdu06"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
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

    class VehCfgPrmCCPBytePosn6_4_VgmConnSignalIPdu06:
        sig_name = "VehCfgPrmCCPBytePosn6_4_VgmConnSignalIPdu06"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
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

    class VehCfgPrmCCPBytePosn5_4_VgmConnSignalIPdu06:
        sig_name = "VehCfgPrmCCPBytePosn5_4_VgmConnSignalIPdu06"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
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

    class VehCfgPrmBlkIDBytePosn1_4_VgmConnSignalIPdu06:
        sig_name = "VehCfgPrmBlkIDBytePosn1_4_VgmConnSignalIPdu06"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
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

    class VehCfgPrmCCPBytePosn8_4_VgmConnSignalIPdu06:
        sig_name = "VehCfgPrmCCPBytePosn8_4_VgmConnSignalIPdu06"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
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

    class VehCfgPrmCCPBytePosn2_4_VgmConnSignalIPdu06:
        sig_name = "VehCfgPrmCCPBytePosn2_4_VgmConnSignalIPdu06"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
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


class TcamConnectivityFr33:
    msg_name = "TcamConnectivityFr33"
    msg_id = 383
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 16
    tx_node = "TCAM"
    rx_nodes = ['BGM']

    class RVIResponseFromTelmByte0:
        sig_name = "RVIResponseFromTelmByte0"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
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

    class RVIResponseFromTelmByte1:
        sig_name = "RVIResponseFromTelmByte1"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
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

    class RVIResponseFromTelmByte2:
        sig_name = "RVIResponseFromTelmByte2"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
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

    class RVIResponseFromTelmByte11:
        sig_name = "RVIResponseFromTelmByte11"
        sig_start_bit = 95
        sig_length = 8
        sig_value_factor = None
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

    class RVIResponseFromTelmByte8:
        sig_name = "RVIResponseFromTelmByte8"
        sig_start_bit = 71
        sig_length = 8
        sig_value_factor = None
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

    class RVIResponseFromTelmByte3:
        sig_name = "RVIResponseFromTelmByte3"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
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

    class RVIResponseFromTelmByte13:
        sig_name = "RVIResponseFromTelmByte13"
        sig_start_bit = 111
        sig_length = 8
        sig_value_factor = None
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

    class RVIResponseFromTelmByte5:
        sig_name = "RVIResponseFromTelmByte5"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
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

    class RVIResponseFromTelmByte7:
        sig_name = "RVIResponseFromTelmByte7"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
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

    class RVIResponseFromTelmByte10:
        sig_name = "RVIResponseFromTelmByte10"
        sig_start_bit = 87
        sig_length = 8
        sig_value_factor = None
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

    class RVIResponseFromTelmByte12:
        sig_name = "RVIResponseFromTelmByte12"
        sig_start_bit = 103
        sig_length = 8
        sig_value_factor = None
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

    class RVIResponseFromTelmByte15:
        sig_name = "RVIResponseFromTelmByte15"
        sig_start_bit = 127
        sig_length = 8
        sig_value_factor = None
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

    class RVIResponseFromTelmByte9:
        sig_name = "RVIResponseFromTelmByte9"
        sig_start_bit = 79
        sig_length = 8
        sig_value_factor = None
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

    class RVIResponseFromTelmByte14:
        sig_name = "RVIResponseFromTelmByte14"
        sig_start_bit = 119
        sig_length = 8
        sig_value_factor = None
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

    class RVIResponseFromTelmByte6:
        sig_name = "RVIResponseFromTelmByte6"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
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

    class RVIResponseFromTelmByte4:
        sig_name = "RVIResponseFromTelmByte4"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
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


class TcamConnectivityCANNmFr:
    msg_name = "TcamConnectivityCANNmFr"
    msg_id = 1289
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "TCAM"
    rx_nodes = ['NKR']


class BgmConnectivityFr05:
    msg_name = "BgmConnectivityFr05"
    msg_id = 373
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "BGM"
    rx_nodes = ['BNCM']

    class DigKeyBLEResp3:
        sig_name = "DigKeyBLEResp3"
        sig_start_bit = 0
        sig_length = 512
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Opaque"
        sig_value_init = None
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 512
        startbit = 0
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111111, 0b00000000, 8, 0), (8, 0b11111111, 0b00000000, 8, 0), (9, 0b11111111, 0b00000000, 8, 0), (10, 0b11111111, 0b00000000, 8, 0), (11, 0b11111111, 0b00000000, 8, 0), (12, 0b11111111, 0b00000000, 8, 0), (13, 0b11111111, 0b00000000, 8, 0), (14, 0b11111111, 0b00000000, 8, 0), (15, 0b11111111, 0b00000000, 8, 0), (16, 0b11111111, 0b00000000, 8, 0), (17, 0b11111111, 0b00000000, 8, 0), (18, 0b11111111, 0b00000000, 8, 0), (19, 0b11111111, 0b00000000, 8, 0), (20, 0b11111111, 0b00000000, 8, 0), (21, 0b11111111, 0b00000000, 8, 0), (22, 0b11111111, 0b00000000, 8, 0), (23, 0b11111111, 0b00000000, 8, 0), (24, 0b11111111, 0b00000000, 8, 0), (25, 0b11111111, 0b00000000, 8, 0), (26, 0b11111111, 0b00000000, 8, 0), (27, 0b11111111, 0b00000000, 8, 0), (28, 0b11111111, 0b00000000, 8, 0), (29, 0b11111111, 0b00000000, 8, 0), (30, 0b11111111, 0b00000000, 8, 0), (31, 0b11111111, 0b00000000, 8, 0), (32, 0b11111111, 0b00000000, 8, 0), (33, 0b11111111, 0b00000000, 8, 0), (34, 0b11111111, 0b00000000, 8, 0), (35, 0b11111111, 0b00000000, 8, 0), (36, 0b11111111, 0b00000000, 8, 0), (37, 0b11111111, 0b00000000, 8, 0), (38, 0b11111111, 0b00000000, 8, 0), (39, 0b11111111, 0b00000000, 8, 0), (40, 0b11111111, 0b00000000, 8, 0), (41, 0b11111111, 0b00000000, 8, 0), (42, 0b11111111, 0b00000000, 8, 0), (43, 0b11111111, 0b00000000, 8, 0), (44, 0b11111111, 0b00000000, 8, 0), (45, 0b11111111, 0b00000000, 8, 0), (46, 0b11111111, 0b00000000, 8, 0), (47, 0b11111111, 0b00000000, 8, 0), (48, 0b11111111, 0b00000000, 8, 0), (49, 0b11111111, 0b00000000, 8, 0), (50, 0b11111111, 0b00000000, 8, 0), (51, 0b11111111, 0b00000000, 8, 0), (52, 0b11111111, 0b00000000, 8, 0), (53, 0b11111111, 0b00000000, 8, 0), (54, 0b11111111, 0b00000000, 8, 0), (55, 0b11111111, 0b00000000, 8, 0), (56, 0b11111111, 0b00000000, 8, 0), (57, 0b11111111, 0b00000000, 8, 0), (58, 0b11111111, 0b00000000, 8, 0), (59, 0b11111111, 0b00000000, 8, 0), (60, 0b11111111, 0b00000000, 8, 0), (61, 0b11111111, 0b00000000, 8, 0), (62, 0b11111111, 0b00000000, 8, 0), (63, 0b11111111, 0b00000000, 8, 0)]


class BgmConnectivityFr10:
    msg_name = "BgmConnectivityFr10"
    msg_id = 804
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.145
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['WPC']

    class CarCfgInfoToWPC:
        sig_name = "CarCfgInfoToWPC"
        sig_start_bit = 0
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
        startbit = 0
        byte = 0
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class RadioFrqAM_0_BgmConnectivitySignalIPdu10:
        sig_name = "RadioFrqAM_0_BgmConnectivitySignalIPdu10"
        sig_start_bit = 5
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
        startbit = 5
        bmuws_info = [(0, 0b11100000, 0b00011111, 3, 5), (1, 0b11111111, 0b00000000, 8, 0)]

    class RlyPwrDistbnCmd1WdPreBattSaveCmd_0_BgmConnectivitySignalIPdu10:
        sig_name = "RlyPwrDistbnCmd1WdPreBattSaveCmd_0_BgmConnectivitySignalIPdu10"
        sig_start_bit = 16
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

    class KeyScanActv:
        sig_name = "KeyScanActv"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7


class BncmConnectivityFr16:
    msg_name = "BncmConnectivityFr16"
    msg_id = 329
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "BNCM"
    rx_nodes = ['BGM']

    class DigKeyBLEResp2:
        sig_name = "DigKeyBLEResp2"
        sig_start_bit = 0
        sig_length = 512
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Opaque"
        sig_value_init = None
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 512
        startbit = 0
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111111, 0b00000000, 8, 0), (8, 0b11111111, 0b00000000, 8, 0), (9, 0b11111111, 0b00000000, 8, 0), (10, 0b11111111, 0b00000000, 8, 0), (11, 0b11111111, 0b00000000, 8, 0), (12, 0b11111111, 0b00000000, 8, 0), (13, 0b11111111, 0b00000000, 8, 0), (14, 0b11111111, 0b00000000, 8, 0), (15, 0b11111111, 0b00000000, 8, 0), (16, 0b11111111, 0b00000000, 8, 0), (17, 0b11111111, 0b00000000, 8, 0), (18, 0b11111111, 0b00000000, 8, 0), (19, 0b11111111, 0b00000000, 8, 0), (20, 0b11111111, 0b00000000, 8, 0), (21, 0b11111111, 0b00000000, 8, 0), (22, 0b11111111, 0b00000000, 8, 0), (23, 0b11111111, 0b00000000, 8, 0), (24, 0b11111111, 0b00000000, 8, 0), (25, 0b11111111, 0b00000000, 8, 0), (26, 0b11111111, 0b00000000, 8, 0), (27, 0b11111111, 0b00000000, 8, 0), (28, 0b11111111, 0b00000000, 8, 0), (29, 0b11111111, 0b00000000, 8, 0), (30, 0b11111111, 0b00000000, 8, 0), (31, 0b11111111, 0b00000000, 8, 0), (32, 0b11111111, 0b00000000, 8, 0), (33, 0b11111111, 0b00000000, 8, 0), (34, 0b11111111, 0b00000000, 8, 0), (35, 0b11111111, 0b00000000, 8, 0), (36, 0b11111111, 0b00000000, 8, 0), (37, 0b11111111, 0b00000000, 8, 0), (38, 0b11111111, 0b00000000, 8, 0), (39, 0b11111111, 0b00000000, 8, 0), (40, 0b11111111, 0b00000000, 8, 0), (41, 0b11111111, 0b00000000, 8, 0), (42, 0b11111111, 0b00000000, 8, 0), (43, 0b11111111, 0b00000000, 8, 0), (44, 0b11111111, 0b00000000, 8, 0), (45, 0b11111111, 0b00000000, 8, 0), (46, 0b11111111, 0b00000000, 8, 0), (47, 0b11111111, 0b00000000, 8, 0), (48, 0b11111111, 0b00000000, 8, 0), (49, 0b11111111, 0b00000000, 8, 0), (50, 0b11111111, 0b00000000, 8, 0), (51, 0b11111111, 0b00000000, 8, 0), (52, 0b11111111, 0b00000000, 8, 0), (53, 0b11111111, 0b00000000, 8, 0), (54, 0b11111111, 0b00000000, 8, 0), (55, 0b11111111, 0b00000000, 8, 0), (56, 0b11111111, 0b00000000, 8, 0), (57, 0b11111111, 0b00000000, 8, 0), (58, 0b11111111, 0b00000000, 8, 0), (59, 0b11111111, 0b00000000, 8, 0), (60, 0b11111111, 0b00000000, 8, 0), (61, 0b11111111, 0b00000000, 8, 0), (62, 0b11111111, 0b00000000, 8, 0), (63, 0b11111111, 0b00000000, 8, 0)]


class ETCtoTCAMConnectivityCanDevFr01:
    msg_name = "ETCtoTCAMConnectivityCanDevFr01"
    msg_id = 1424
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CCM"
    rx_nodes = ['TCAM']

    class TCAMdevelpsignalgroupreqFunctiondevpsignalgroup7:
        sig_name = "TCAMdevelpsignalgroupreqFunctiondevpsignalgroup7"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
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

    class TCAMdevelpsignalgroupreqFunctiondevpsignalgroup3:
        sig_name = "TCAMdevelpsignalgroupreqFunctiondevpsignalgroup3"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
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

    class TCAMdevelpsignalgroupreqFunctiondevpsignalgroup5:
        sig_name = "TCAMdevelpsignalgroupreqFunctiondevpsignalgroup5"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
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

    class TCAMdevelpsignalgroupreqFunctiondevpsignalgroup6:
        sig_name = "TCAMdevelpsignalgroupreqFunctiondevpsignalgroup6"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
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

    class TCAMdevelpsignalgroupreqFunctiondevpsignalgroup1:
        sig_name = "TCAMdevelpsignalgroupreqFunctiondevpsignalgroup1"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
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

    class TCAMdevelpsignalgroupreqFunctiondevpsignalgroup4:
        sig_name = "TCAMdevelpsignalgroupreqFunctiondevpsignalgroup4"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
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

    class TCAMdevelpsignalgroupreqFunctiondevpsignalgroup2:
        sig_name = "TCAMdevelpsignalgroupreqFunctiondevpsignalgroup2"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
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

    class TCAMdevelpsignalgroupreqFunctiondevpsignalgroup8:
        sig_name = "TCAMdevelpsignalgroupreqFunctiondevpsignalgroup8"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
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


class TcamConnectivityFr04:
    msg_name = "TcamConnectivityFr04"
    msg_id = 330
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.04
    msg_length = 8
    tx_node = "TCAM"
    rx_nodes = ['BGM']

    class ChrgLidTelmLockgReq:
        sig_name = "ChrgLidTelmLockgReq"
        sig_start_bit = 1
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

    class CbnOverHeatProtnEnaFromTelm_0_TcamConnectivitySignalIPdu04:
        sig_name = "CbnOverHeatProtnEnaFromTelm_0_TcamConnectivitySignalIPdu04"
        sig_start_bit = 11
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

    class RemChkTInVeh_0_TcamConnectivitySignalIPdu04:
        sig_name = "RemChkTInVeh_0_TcamConnectivitySignalIPdu04"
        sig_start_bit = 9
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
        startbit = 9
        byte = 1
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
        sig_byteorder = "Motorola"
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


class BncmConnectivityCANNmFr:
    msg_name = "BncmConnectivityCANNmFr"
    msg_id = 1291
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BNCM"
    rx_nodes = ['TCAM']


class BncmConnectivityFr07:
    msg_name = "BncmConnectivityFr07"
    msg_id = 358
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "BNCM"
    rx_nodes = ['BGM']

    class DigKeyBLEReq:
        sig_name = "DigKeyBLEReq"
        sig_start_bit = 0
        sig_length = 512
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Opaque"
        sig_value_init = None
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 512
        startbit = 0
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111111, 0b00000000, 8, 0), (8, 0b11111111, 0b00000000, 8, 0), (9, 0b11111111, 0b00000000, 8, 0), (10, 0b11111111, 0b00000000, 8, 0), (11, 0b11111111, 0b00000000, 8, 0), (12, 0b11111111, 0b00000000, 8, 0), (13, 0b11111111, 0b00000000, 8, 0), (14, 0b11111111, 0b00000000, 8, 0), (15, 0b11111111, 0b00000000, 8, 0), (16, 0b11111111, 0b00000000, 8, 0), (17, 0b11111111, 0b00000000, 8, 0), (18, 0b11111111, 0b00000000, 8, 0), (19, 0b11111111, 0b00000000, 8, 0), (20, 0b11111111, 0b00000000, 8, 0), (21, 0b11111111, 0b00000000, 8, 0), (22, 0b11111111, 0b00000000, 8, 0), (23, 0b11111111, 0b00000000, 8, 0), (24, 0b11111111, 0b00000000, 8, 0), (25, 0b11111111, 0b00000000, 8, 0), (26, 0b11111111, 0b00000000, 8, 0), (27, 0b11111111, 0b00000000, 8, 0), (28, 0b11111111, 0b00000000, 8, 0), (29, 0b11111111, 0b00000000, 8, 0), (30, 0b11111111, 0b00000000, 8, 0), (31, 0b11111111, 0b00000000, 8, 0), (32, 0b11111111, 0b00000000, 8, 0), (33, 0b11111111, 0b00000000, 8, 0), (34, 0b11111111, 0b00000000, 8, 0), (35, 0b11111111, 0b00000000, 8, 0), (36, 0b11111111, 0b00000000, 8, 0), (37, 0b11111111, 0b00000000, 8, 0), (38, 0b11111111, 0b00000000, 8, 0), (39, 0b11111111, 0b00000000, 8, 0), (40, 0b11111111, 0b00000000, 8, 0), (41, 0b11111111, 0b00000000, 8, 0), (42, 0b11111111, 0b00000000, 8, 0), (43, 0b11111111, 0b00000000, 8, 0), (44, 0b11111111, 0b00000000, 8, 0), (45, 0b11111111, 0b00000000, 8, 0), (46, 0b11111111, 0b00000000, 8, 0), (47, 0b11111111, 0b00000000, 8, 0), (48, 0b11111111, 0b00000000, 8, 0), (49, 0b11111111, 0b00000000, 8, 0), (50, 0b11111111, 0b00000000, 8, 0), (51, 0b11111111, 0b00000000, 8, 0), (52, 0b11111111, 0b00000000, 8, 0), (53, 0b11111111, 0b00000000, 8, 0), (54, 0b11111111, 0b00000000, 8, 0), (55, 0b11111111, 0b00000000, 8, 0), (56, 0b11111111, 0b00000000, 8, 0), (57, 0b11111111, 0b00000000, 8, 0), (58, 0b11111111, 0b00000000, 8, 0), (59, 0b11111111, 0b00000000, 8, 0), (60, 0b11111111, 0b00000000, 8, 0), (61, 0b11111111, 0b00000000, 8, 0), (62, 0b11111111, 0b00000000, 8, 0), (63, 0b11111111, 0b00000000, 8, 0)]


class VgmConnectivityVFCInfoEnaFr:
    msg_name = "VgmConnectivityVFCInfoEnaFr"
    msg_id = 1375
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 1
    tx_node = "BGM"
    rx_nodes = ['TCAM', 'BNCM']

    class VFCInfoEna_2_VgmConnectivityVFCInfoEnaSignalIPdu:
        sig_name = "VFCInfoEna_2_VgmConnectivityVFCInfoEnaSignalIPdu"
        sig_start_bit = 0
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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


class VgmConnFr08:
    msg_name = "VgmConnFr08"
    msg_id = 512
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['TCAM', 'WPC', 'BNCM']

    class DoorOpenerRiReSts_2_VgmConnSignalIPdu08:
        sig_name = "DoorOpenerRiReSts_2_VgmConnSignalIPdu08"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
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

    class DoorRiReSts_3_VgmConnSignalIPdu08:
        sig_name = "DoorRiReSts_3_VgmConnSignalIPdu08"
        sig_start_bit = 35
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
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

    class DoorOpenerLeReSts_2_VgmConnSignalIPdu08:
        sig_name = "DoorOpenerLeReSts_2_VgmConnSignalIPdu08"
        sig_start_bit = 3
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
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

    class DoorOpenerPassSts_2_VgmConnSignalIPdu08:
        sig_name = "DoorOpenerPassSts_2_VgmConnSignalIPdu08"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
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

    class DoorPassSts_4_VgmConnSignalIPdu08:
        sig_name = "DoorPassSts_4_VgmConnSignalIPdu08"
        sig_start_bit = 37
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
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

    class DoorRiReLockSts_2_VgmConnSignalIPdu08:
        sig_name = "DoorRiReLockSts_2_VgmConnSignalIPdu08"
        sig_start_bit = 51
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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

    class DoorPassLockSts_2_VgmConnSignalIPdu08:
        sig_name = "DoorPassLockSts_2_VgmConnSignalIPdu08"
        sig_start_bit = 53
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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

    class DoorLeReLockSts_2_VgmConnSignalIPdu08:
        sig_name = "DoorLeReLockSts_2_VgmConnSignalIPdu08"
        sig_start_bit = 55
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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

    class DoorLeReSts_3_VgmConnSignalIPdu08:
        sig_name = "DoorLeReSts_3_VgmConnSignalIPdu08"
        sig_start_bit = 39
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
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

    class ClsdDueToRain:
        sig_name = "ClsdDueToRain"
        sig_start_bit = 16
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

    class DoorDrvrLockSts_2_VgmConnSignalIPdu08:
        sig_name = "DoorDrvrLockSts_2_VgmConnSignalIPdu08"
        sig_start_bit = 22
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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

    class DoorOpenerDrvrSts_2_VgmConnSignalIPdu08:
        sig_name = "DoorOpenerDrvrSts_2_VgmConnSignalIPdu08"
        sig_start_bit = 7
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
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


class VgmConnFr13:
    msg_name = "VgmConnFr13"
    msg_id = 1152
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.225
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['TCAM', 'WPC', 'BNCM']

    class CmptmtTFrntQf_2_VgmConnSignalIPdu13:
        sig_name = "CmptmtTFrntQf_2_VgmConnSignalIPdu13"
        sig_start_bit = 37
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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

    class CmptmtTFrntCmptmtTFrnt_2_VgmConnSignalIPdu13:
        sig_name = "CmptmtTFrntCmptmtTFrnt_2_VgmConnSignalIPdu13"
        sig_start_bit = 34
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = "-60.0"
        sig_value_min = 0
        sig_value_max = 1850
        sig_byteorder = "Motorola"
        sig_value_init = 600
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 34
        bmuws_info = [(4, 0b00000111, 0b11111000, 3, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class VehSpdIndcdVehSpdIndcd_1_VgmConnSignalIPdu13:
        sig_name = "VehSpdIndcdVehSpdIndcd_1_VgmConnSignalIPdu13"
        sig_start_bit = 48
        sig_length = 9
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 48
        bmuws_info = [(6, 0b00000001, 0b11111110, 1, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class VehBattUSysUQf_6_VgmConnSignalIPdu13:
        sig_name = "VehBattUSysUQf_6_VgmConnSignalIPdu13"
        sig_start_bit = 17
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
        startbit = 17
        byte = 2
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VehSpdIndcdVeSpdIndcdUnit_1_VgmConnSignalIPdu13:
        sig_name = "VehSpdIndcdVeSpdIndcdUnit_1_VgmConnSignalIPdu13"
        sig_start_bit = 50
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
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

    class CmptmtTFrntFanForCmptmtTRunng_2_VgmConnSignalIPdu13:
        sig_name = "CmptmtTFrntFanForCmptmtTRunng_2_VgmConnSignalIPdu13"
        sig_start_bit = 35
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
        startbit = 35
        byte = 4
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VehBattUSysU_6_VgmConnSignalIPdu13:
        sig_name = "VehBattUSysU_6_VgmConnSignalIPdu13"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 250
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

    class BkpOfDstTrvld_6_VgmConnSignalIPdu13:
        sig_name = "BkpOfDstTrvld_6_VgmConnSignalIPdu13"
        sig_start_bit = 7
        sig_length = 21
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 2000000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 21
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111000, 0b00000111, 5, 3)]


class BncmBsrmConnectivityFr05:
    msg_name = "BncmBsrmConnectivityFr05"
    msg_id = 1075
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "BNCM"
    rx_nodes = ['WPC']


class VgmConnFr15:
    msg_name = "VgmConnFr15"
    msg_id = 320
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['TCAM']

    class DKDataFromCEMDKDataByte6:
        sig_name = "DKDataFromCEMDKDataByte6"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
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

    class DKDataFromCEMDKDataByte5:
        sig_name = "DKDataFromCEMDKDataByte5"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
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

    class DKDataFromCEMHeader:
        sig_name = "DKDataFromCEMHeader"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
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

    class DKDataFromCEMDKDataByte1:
        sig_name = "DKDataFromCEMDKDataByte1"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
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

    class DKDataFromCEMDKDataByte3:
        sig_name = "DKDataFromCEMDKDataByte3"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
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

    class DKDataFromCEMAcknowledgment:
        sig_name = "DKDataFromCEMAcknowledgment"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
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

    class DKDataFromCEMDKDataByte4:
        sig_name = "DKDataFromCEMDKDataByte4"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
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

    class DKDataFromCEMDKDataByte2:
        sig_name = "DKDataFromCEMDKDataByte2"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
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


class TcamConnectivityVFCVectorFr:
    msg_name = "TcamConnectivityVFCVectorFr"
    msg_id = 1353
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "TCAM"
    rx_nodes = ['CCM']

    class VFCVectorTCAMVFCid5:
        sig_name = "VFCVectorTCAMVFCid5"
        sig_start_bit = 7
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorTCAMBlockID:
        sig_name = "VFCVectorTCAMBlockID"
        sig_start_bit = 1
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
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VFCVectorTCAMVFCid30:
        sig_name = "VFCVectorTCAMVFCid30"
        sig_start_bit = 32
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 32
        byte = 4
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorTCAMVFCid56:
        sig_name = "VFCVectorTCAMVFCid56"
        sig_start_bit = 58
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 58
        byte = 7
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorTCAMVFCid22:
        sig_name = "VFCVectorTCAMVFCid22"
        sig_start_bit = 24
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 24
        byte = 3
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorTCAMVFCid27:
        sig_name = "VFCVectorTCAMVFCid27"
        sig_start_bit = 29
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 29
        byte = 3
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorTCAMVFCid47:
        sig_name = "VFCVectorTCAMVFCid47"
        sig_start_bit = 49
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 49
        byte = 6
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorTCAMVFCid58:
        sig_name = "VFCVectorTCAMVFCid58"
        sig_start_bit = 60
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 60
        byte = 7
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorTCAMVFCid61:
        sig_name = "VFCVectorTCAMVFCid61"
        sig_start_bit = 63
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 63
        byte = 7
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorTCAMVFCid11:
        sig_name = "VFCVectorTCAMVFCid11"
        sig_start_bit = 13
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 13
        byte = 1
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorTCAMVFCid53:
        sig_name = "VFCVectorTCAMVFCid53"
        sig_start_bit = 55
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 55
        byte = 6
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorTCAMVFCid36:
        sig_name = "VFCVectorTCAMVFCid36"
        sig_start_bit = 38
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 38
        byte = 4
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorTCAMVFCid38:
        sig_name = "VFCVectorTCAMVFCid38"
        sig_start_bit = 40
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 40
        byte = 5
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorTCAMVFCid15:
        sig_name = "VFCVectorTCAMVFCid15"
        sig_start_bit = 17
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 17
        byte = 2
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorTCAMVFCid14:
        sig_name = "VFCVectorTCAMVFCid14"
        sig_start_bit = 16
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 16
        byte = 2
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorTCAMVFCid3:
        sig_name = "VFCVectorTCAMVFCid3"
        sig_start_bit = 5
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorTCAMVFCid35:
        sig_name = "VFCVectorTCAMVFCid35"
        sig_start_bit = 37
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 37
        byte = 4
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorTCAMVFCid55:
        sig_name = "VFCVectorTCAMVFCid55"
        sig_start_bit = 57
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 57
        byte = 7
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorTCAMVFCid17:
        sig_name = "VFCVectorTCAMVFCid17"
        sig_start_bit = 19
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 19
        byte = 2
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorTCAMVFCid20:
        sig_name = "VFCVectorTCAMVFCid20"
        sig_start_bit = 22
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 22
        byte = 2
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorTCAMVFCid41:
        sig_name = "VFCVectorTCAMVFCid41"
        sig_start_bit = 43
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 43
        byte = 5
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorTCAMVFCid13:
        sig_name = "VFCVectorTCAMVFCid13"
        sig_start_bit = 15
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 15
        byte = 1
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorTCAMVFCid48:
        sig_name = "VFCVectorTCAMVFCid48"
        sig_start_bit = 50
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 50
        byte = 6
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorTCAMVFCid45:
        sig_name = "VFCVectorTCAMVFCid45"
        sig_start_bit = 47
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 47
        byte = 5
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorTCAMVFCid9:
        sig_name = "VFCVectorTCAMVFCid9"
        sig_start_bit = 11
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 11
        byte = 1
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorTCAMVFCid16:
        sig_name = "VFCVectorTCAMVFCid16"
        sig_start_bit = 18
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 18
        byte = 2
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorTCAMVFCid19:
        sig_name = "VFCVectorTCAMVFCid19"
        sig_start_bit = 21
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 21
        byte = 2
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorTCAMVFCid24:
        sig_name = "VFCVectorTCAMVFCid24"
        sig_start_bit = 26
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 26
        byte = 3
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorTCAMVFCid12:
        sig_name = "VFCVectorTCAMVFCid12"
        sig_start_bit = 14
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 14
        byte = 1
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorTCAMVFCid26:
        sig_name = "VFCVectorTCAMVFCid26"
        sig_start_bit = 28
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 28
        byte = 3
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorTCAMVFCid18:
        sig_name = "VFCVectorTCAMVFCid18"
        sig_start_bit = 20
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 20
        byte = 2
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorTCAMVFCid46:
        sig_name = "VFCVectorTCAMVFCid46"
        sig_start_bit = 48
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 48
        byte = 6
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorTCAMVFCid42:
        sig_name = "VFCVectorTCAMVFCid42"
        sig_start_bit = 44
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 44
        byte = 5
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorTCAMVFCid29:
        sig_name = "VFCVectorTCAMVFCid29"
        sig_start_bit = 31
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 31
        byte = 3
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorTCAMVFCid7:
        sig_name = "VFCVectorTCAMVFCid7"
        sig_start_bit = 9
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 9
        byte = 1
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorTCAMVFCid33:
        sig_name = "VFCVectorTCAMVFCid33"
        sig_start_bit = 35
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 35
        byte = 4
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorTCAMVFCid37:
        sig_name = "VFCVectorTCAMVFCid37"
        sig_start_bit = 39
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 39
        byte = 4
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorTCAMVFCid21:
        sig_name = "VFCVectorTCAMVFCid21"
        sig_start_bit = 23
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 23
        byte = 2
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorTCAMVFCid31:
        sig_name = "VFCVectorTCAMVFCid31"
        sig_start_bit = 33
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 33
        byte = 4
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorTCAMVFCid32:
        sig_name = "VFCVectorTCAMVFCid32"
        sig_start_bit = 34
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 34
        byte = 4
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorTCAMVFCid44:
        sig_name = "VFCVectorTCAMVFCid44"
        sig_start_bit = 46
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 46
        byte = 5
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorTCAMVFCid0:
        sig_name = "VFCVectorTCAMVFCid0"
        sig_start_bit = 2
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 2
        byte = 0
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorTCAMVFCid43:
        sig_name = "VFCVectorTCAMVFCid43"
        sig_start_bit = 45
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 45
        byte = 5
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorTCAMVFCid10:
        sig_name = "VFCVectorTCAMVFCid10"
        sig_start_bit = 12
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 12
        byte = 1
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorTCAMVFCid8:
        sig_name = "VFCVectorTCAMVFCid8"
        sig_start_bit = 10
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 10
        byte = 1
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorTCAMVFCid40:
        sig_name = "VFCVectorTCAMVFCid40"
        sig_start_bit = 42
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 42
        byte = 5
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorTCAMVFCid6:
        sig_name = "VFCVectorTCAMVFCid6"
        sig_start_bit = 8
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 8
        byte = 1
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorTCAMVFCid54:
        sig_name = "VFCVectorTCAMVFCid54"
        sig_start_bit = 56
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 56
        byte = 7
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorTCAMVFCid2:
        sig_name = "VFCVectorTCAMVFCid2"
        sig_start_bit = 4
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 4
        byte = 0
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorTCAMVFCid59:
        sig_name = "VFCVectorTCAMVFCid59"
        sig_start_bit = 61
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 61
        byte = 7
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorTCAMVFCid60:
        sig_name = "VFCVectorTCAMVFCid60"
        sig_start_bit = 62
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 62
        byte = 7
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorTCAMVFCid4:
        sig_name = "VFCVectorTCAMVFCid4"
        sig_start_bit = 6
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorTCAMVFCid1:
        sig_name = "VFCVectorTCAMVFCid1"
        sig_start_bit = 3
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 3
        byte = 0
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorTCAMVFCid25:
        sig_name = "VFCVectorTCAMVFCid25"
        sig_start_bit = 27
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 27
        byte = 3
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorTCAMVFCid49:
        sig_name = "VFCVectorTCAMVFCid49"
        sig_start_bit = 51
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 51
        byte = 6
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorTCAMVFCid23:
        sig_name = "VFCVectorTCAMVFCid23"
        sig_start_bit = 25
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 25
        byte = 3
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorTCAMVFCid39:
        sig_name = "VFCVectorTCAMVFCid39"
        sig_start_bit = 41
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 41
        byte = 5
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorTCAMVFCid50:
        sig_name = "VFCVectorTCAMVFCid50"
        sig_start_bit = 52
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorTCAMVFCid52:
        sig_name = "VFCVectorTCAMVFCid52"
        sig_start_bit = 54
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 54
        byte = 6
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorTCAMVFCid57:
        sig_name = "VFCVectorTCAMVFCid57"
        sig_start_bit = 59
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 59
        byte = 7
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorTCAMVFCid28:
        sig_name = "VFCVectorTCAMVFCid28"
        sig_start_bit = 30
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 30
        byte = 3
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorTCAMVFCid51:
        sig_name = "VFCVectorTCAMVFCid51"
        sig_start_bit = 53
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 53
        byte = 6
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorTCAMVFCid34:
        sig_name = "VFCVectorTCAMVFCid34"
        sig_start_bit = 36
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 36
        byte = 4
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4


class VgmConnFr01:
    msg_name = "VgmConnFr01"
    msg_id = 288
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['NKR', 'BNCM', 'TCAM', 'WPC']

    class VehModMngtGlbSafe1Chks_6_VgmConnSignalIPdu01:
        sig_name = "VehModMngtGlbSafe1Chks_6_VgmConnSignalIPdu01"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
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

    class VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp_6_VgmConnSignalIPdu01:
        sig_name = "VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp_6_VgmConnSignalIPdu01"
        sig_start_bit = 36
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
        startbit = 36
        byte = 4
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class VehModMngtGlbSafe1EgyLvlElecMai_6_VgmConnSignalIPdu01:
        sig_name = "VehModMngtGlbSafe1EgyLvlElecMai_6_VgmConnSignalIPdu01"
        sig_start_bit = 11
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

    class VehModMngtGlbSafe1EgyLvlElecSubtyp_6_VgmConnSignalIPdu01:
        sig_name = "VehModMngtGlbSafe1EgyLvlElecSubtyp_6_VgmConnSignalIPdu01"
        sig_start_bit = 23
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

    class AjarChrgLidRearSwitch:
        sig_name = "AjarChrgLidRearSwitch"
        sig_start_bit = 47
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
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

    class ErsStrtRes:
        sig_name = "ErsStrtRes"
        sig_start_bit = 60
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 19
        sig_byteorder = "Motorola"
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

    class VehModMngtGlbSafe1CarModSts1_6_VgmConnSignalIPdu01:
        sig_name = "VehModMngtGlbSafe1CarModSts1_6_VgmConnSignalIPdu01"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
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

    class VehModMngtGlbSafe1PwrLvlElecSubtyp_6_VgmConnSignalIPdu01:
        sig_name = "VehModMngtGlbSafe1PwrLvlElecSubtyp_6_VgmConnSignalIPdu01"
        sig_start_bit = 31
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

    class VehModMngtGlbSafe1Cntr_6_VgmConnSignalIPdu01:
        sig_name = "VehModMngtGlbSafe1Cntr_6_VgmConnSignalIPdu01"
        sig_start_bit = 15
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

    class DoorAcsKeyIsReq:
        sig_name = "DoorAcsKeyIsReq"
        sig_start_bit = 63
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
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

    class VehModMngtGlbSafe1PwrLvlElecMai_6_VgmConnSignalIPdu01:
        sig_name = "VehModMngtGlbSafe1PwrLvlElecMai_6_VgmConnSignalIPdu01"
        sig_start_bit = 19
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

    class VehModMngtGlbSafe1UsgModSts_6_VgmConnSignalIPdu01:
        sig_name = "VehModMngtGlbSafe1UsgModSts_6_VgmConnSignalIPdu01"
        sig_start_bit = 27
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 13
        sig_byteorder = "Motorola"
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

    class VehModMngtGlbSafe1FltEgyCnsWdSts_6_VgmConnSignalIPdu01:
        sig_name = "VehModMngtGlbSafe1FltEgyCnsWdSts_6_VgmConnSignalIPdu01"
        sig_start_bit = 33
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class WinPosnStsAtDrvr_2_VgmConnSignalIPdu01:
        sig_name = "WinPosnStsAtDrvr_2_VgmConnSignalIPdu01"
        sig_start_bit = 44
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Motorola"
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

    class WinPosnStsAtPass_2_VgmConnSignalIPdu01:
        sig_name = "WinPosnStsAtPass_2_VgmConnSignalIPdu01"
        sig_start_bit = 52
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Motorola"
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


class TcamConnectivityFr30:
    msg_name = "TcamConnectivityFr30"
    msg_id = 380
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "TCAM"
    rx_nodes = ['BGM']

    class TelmDefrostReq_0_TcamConnectivitySignalIPdu30:
        sig_name = "TelmDefrostReq_0_TcamConnectivitySignalIPdu30"
        sig_start_bit = 58
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
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


class NfcrConnFr02:
    msg_name = "NfcrConnFr02"
    msg_id = 401
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.085
    msg_length = 8
    tx_node = "NKR"
    rx_nodes = ['BNCM']

    class NFCStatus:
        sig_name = "NFCStatus"
        sig_start_bit = 7
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


class BgmConnectivityFr02:
    msg_name = "BgmConnectivityFr02"
    msg_id = 371
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['TCAM']

    class DigKeyGidInfo2Byte5_0_BgmConnectivitySignalIPdu02:
        sig_name = "DigKeyGidInfo2Byte5_0_BgmConnectivitySignalIPdu02"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
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

    class DigKeyGidInfo2Byte3_0_BgmConnectivitySignalIPdu02:
        sig_name = "DigKeyGidInfo2Byte3_0_BgmConnectivitySignalIPdu02"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
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

    class DigKeyGidInfo2Byte0_0_BgmConnectivitySignalIPdu02:
        sig_name = "DigKeyGidInfo2Byte0_0_BgmConnectivitySignalIPdu02"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
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

    class DigKeyGidInfo2Byte6_0_BgmConnectivitySignalIPdu02:
        sig_name = "DigKeyGidInfo2Byte6_0_BgmConnectivitySignalIPdu02"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
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

    class DigKeyGidInfo2Byte2_0_BgmConnectivitySignalIPdu02:
        sig_name = "DigKeyGidInfo2Byte2_0_BgmConnectivitySignalIPdu02"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
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

    class DigKeyGidInfo2Byte7_0_BgmConnectivitySignalIPdu02:
        sig_name = "DigKeyGidInfo2Byte7_0_BgmConnectivitySignalIPdu02"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
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

    class DigKeyGidInfo2Byte1_0_BgmConnectivitySignalIPdu02:
        sig_name = "DigKeyGidInfo2Byte1_0_BgmConnectivitySignalIPdu02"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
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

    class DigKeyGidInfo2Byte4_0_BgmConnectivitySignalIPdu02:
        sig_name = "DigKeyGidInfo2Byte4_0_BgmConnectivitySignalIPdu02"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
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


class BncmBsrmConnectivityFr03:
    msg_name = "BncmBsrmConnectivityFr03"
    msg_id = 375
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.08
    msg_length = 8
    tx_node = "BNCM"
    rx_nodes = ['BGM', 'WPC']

    class BleConSts:
        sig_name = "BleConSts"
        sig_start_bit = 7
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

    class NFCLinkCtrl:
        sig_name = "NFCLinkCtrl"
        sig_start_bit = 5
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Invalid': 0, 'NFCLinkSetup': 1, 'NFCLinkTeardownAndReset': 2}
        compute_method = None
        length = 2
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4


class VgmConnFr18:
    msg_name = "VgmConnFr18"
    msg_id = 820
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.11
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['TCAM']

    class EngSt1WdStsEngSt1WdSts_2_VgmConnSignalIPdu18:
        sig_name = "EngSt1WdStsEngSt1WdSts_2_VgmConnSignalIPdu18"
        sig_start_bit = 59
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 9
        sig_byteorder = "Motorola"
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

    class FragCh2Id_2_VgmConnSignalIPdu18:
        sig_name = "FragCh2Id_2_VgmConnSignalIPdu18"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
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

    class FragCh5Id_2_VgmConnSignalIPdu18:
        sig_name = "FragCh5Id_2_VgmConnSignalIPdu18"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
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

    class CbnOverHeatProtnEna_1_VgmConnSignalIPdu18:
        sig_name = "CbnOverHeatProtnEna_1_VgmConnSignalIPdu18"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class FragCh4Id_2_VgmConnSignalIPdu18:
        sig_name = "FragCh4Id_2_VgmConnSignalIPdu18"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
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

    class EngSt1WdStsChks_2_VgmConnSignalIPdu18:
        sig_name = "EngSt1WdStsChks_2_VgmConnSignalIPdu18"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
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

    class EngSt1WdStsCntr_2_VgmConnSignalIPdu18:
        sig_name = "EngSt1WdStsCntr_2_VgmConnSignalIPdu18"
        sig_start_bit = 63
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

    class FragCh1Id_2_VgmConnSignalIPdu18:
        sig_name = "FragCh1Id_2_VgmConnSignalIPdu18"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
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

    class FragCh3Id_2_VgmConnSignalIPdu18:
        sig_name = "FragCh3Id_2_VgmConnSignalIPdu18"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
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


class VgmConnFr11:
    msg_name = "VgmConnFr11"
    msg_id = 1024
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['TCAM', 'BNCM']

    class VehCfgPrmExtCCPBytePosn8_4_VgmConnSignalIPdu11:
        sig_name = "VehCfgPrmExtCCPBytePosn8_4_VgmConnSignalIPdu11"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
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

    class VehCfgPrmExtCCPBytePosn4_4_VgmConnSignalIPdu11:
        sig_name = "VehCfgPrmExtCCPBytePosn4_4_VgmConnSignalIPdu11"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
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

    class VehCfgPrmExtBlkIDBytePosn1_4_VgmConnSignalIPdu11:
        sig_name = "VehCfgPrmExtBlkIDBytePosn1_4_VgmConnSignalIPdu11"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
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

    class VehCfgPrmExtCCPBytePosn2_4_VgmConnSignalIPdu11:
        sig_name = "VehCfgPrmExtCCPBytePosn2_4_VgmConnSignalIPdu11"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
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

    class VehCfgPrmExtCCPBytePosn6_4_VgmConnSignalIPdu11:
        sig_name = "VehCfgPrmExtCCPBytePosn6_4_VgmConnSignalIPdu11"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
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

    class VehCfgPrmExtCCPBytePosn7_4_VgmConnSignalIPdu11:
        sig_name = "VehCfgPrmExtCCPBytePosn7_4_VgmConnSignalIPdu11"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
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

    class VehCfgPrmExtCCPBytePosn3_4_VgmConnSignalIPdu11:
        sig_name = "VehCfgPrmExtCCPBytePosn3_4_VgmConnSignalIPdu11"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
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

    class VehCfgPrmExtCCPBytePosn5_4_VgmConnSignalIPdu11:
        sig_name = "VehCfgPrmExtCCPBytePosn5_4_VgmConnSignalIPdu11"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
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


class VgmConnFr03:
    msg_name = "VgmConnFr03"
    msg_id = 832
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.09
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['TCAM']

    class FragCh1UseUpWrn_2_VgmConnSignalIPdu03:
        sig_name = "FragCh1UseUpWrn_2_VgmConnSignalIPdu03"
        sig_start_bit = 30
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class RemClimaActv_1_VgmConnSignalIPdu03:
        sig_name = "RemClimaActv_1_VgmConnSignalIPdu03"
        sig_start_bit = 53
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
        startbit = 53
        byte = 6
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class ClimaActv_2_VgmConnSignalIPdu03:
        sig_name = "ClimaActv_2_VgmConnSignalIPdu03"
        sig_start_bit = 28
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
        startbit = 28
        byte = 3
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class IntPm25LvlFrmClima_2_VgmConnSignalIPdu03:
        sig_name = "IntPm25LvlFrmClima_2_VgmConnSignalIPdu03"
        sig_start_bit = 42
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
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

    class FragLvlFrmClima_2_VgmConnSignalIPdu03:
        sig_name = "FragLvlFrmClima_2_VgmConnSignalIPdu03"
        sig_start_bit = 39
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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

    class FragStsFrmClima_2_VgmConnSignalIPdu03:
        sig_name = "FragStsFrmClima_2_VgmConnSignalIPdu03"
        sig_start_bit = 37
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 1
        sig_value_max = 3
        sig_byteorder = "Motorola"
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

    class FragCh3UseUpWrn_2_VgmConnSignalIPdu03:
        sig_name = "FragCh3UseUpWrn_2_VgmConnSignalIPdu03"
        sig_start_bit = 32
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class SteerWhlHeatgAvlSts_1_VgmConnSignalIPdu03:
        sig_name = "SteerWhlHeatgAvlSts_1_VgmConnSignalIPdu03"
        sig_start_bit = 18
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
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

    class FragCh2UseUpWrn_2_VgmConnSignalIPdu03:
        sig_name = "FragCh2UseUpWrn_2_VgmConnSignalIPdu03"
        sig_start_bit = 31
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class FragCh5UseUpWrn_2_VgmConnSignalIPdu03:
        sig_name = "FragCh5UseUpWrn_2_VgmConnSignalIPdu03"
        sig_start_bit = 34
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class LockgCenStsForUsrFb_1_VgmConnSignalIPdu03:
        sig_name = "LockgCenStsForUsrFb_1_VgmConnSignalIPdu03"
        sig_start_bit = 10
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_byteorder = "Motorola"
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

    class FragCh4UseUpWrn_2_VgmConnSignalIPdu03:
        sig_name = "FragCh4UseUpWrn_2_VgmConnSignalIPdu03"
        sig_start_bit = 33
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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


class VgmConnFr10:
    msg_name = "VgmConnFr10"
    msg_id = 592
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['TCAM']

    class ImobRemMgrChkSts:
        sig_name = "ImobRemMgrChkSts"
        sig_start_bit = 1
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
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

    class ImobVehRemMgrSts1SpdLimRemMgrSts:
        sig_name = "ImobVehRemMgrSts1SpdLimRemMgrSts"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
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

    class ImobRemMgrChkImobDataRemMgrChk0:
        sig_name = "ImobRemMgrChkImobDataRemMgrChk0"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
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

    class ClimaOvrHeatProActv_1_VgmConnSignalIPdu10:
        sig_name = "ClimaOvrHeatProActv_1_VgmConnSignalIPdu10"
        sig_start_bit = 55
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

    class ImobRemMgrChkImobDataRemMgrChk4:
        sig_name = "ImobRemMgrChkImobDataRemMgrChk4"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
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

    class ImobRemMgrChkImobDataRemMgrChk1:
        sig_name = "ImobRemMgrChkImobDataRemMgrChk1"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
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

    class ImobRemMgrChkImobDataRemMgrChk3:
        sig_name = "ImobRemMgrChkImobDataRemMgrChk3"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
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

    class ImobVehRemMgrSts1ImobVehRemMgrSts:
        sig_name = "ImobVehRemMgrSts1ImobVehRemMgrSts"
        sig_start_bit = 49
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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

    class ErsStrtApplSts:
        sig_name = "ErsStrtApplSts"
        sig_start_bit = 4
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
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

    class ErsDelayTiCfm:
        sig_name = "ErsDelayTiCfm"
        sig_start_bit = 6
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
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class ImobRemMgrChkImobDataRemMgrChk2:
        sig_name = "ImobRemMgrChkImobDataRemMgrChk2"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
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


class VgmConnFr02:
    msg_name = "VgmConnFr02"
    msg_id = 336
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.035
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['TCAM', 'WPC', 'BNCM']

    class WinPosnStsAtReRi_2_VgmConnSignalIPdu02:
        sig_name = "WinPosnStsAtReRi_2_VgmConnSignalIPdu02"
        sig_start_bit = 44
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Motorola"
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

    class TrLockSts_1_VgmConnSignalIPdu02:
        sig_name = "TrLockSts_1_VgmConnSignalIPdu02"
        sig_start_bit = 47
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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

    class VehSpdLgtQf_4_VgmConnSignalIPdu02:
        sig_name = "VehSpdLgtQf_4_VgmConnSignalIPdu02"
        sig_start_bit = 27
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
        startbit = 27
        byte = 3
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class DoorDrvrSts_4_VgmConnSignalIPdu02:
        sig_name = "DoorDrvrSts_4_VgmConnSignalIPdu02"
        sig_start_bit = 25
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
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

    class VehSpdLgtChks_4_VgmConnSignalIPdu02:
        sig_name = "VehSpdLgtChks_4_VgmConnSignalIPdu02"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
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

    class WinPosnStsAtReLe_2_VgmConnSignalIPdu02:
        sig_name = "WinPosnStsAtReLe_2_VgmConnSignalIPdu02"
        sig_start_bit = 36
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Motorola"
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

    class VehSpdLgtCntr_4_VgmConnSignalIPdu02:
        sig_name = "VehSpdLgtCntr_4_VgmConnSignalIPdu02"
        sig_start_bit = 31
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

    class VehSpdLgtA_4_VgmConnSignalIPdu02:
        sig_name = "VehSpdLgtA_4_VgmConnSignalIPdu02"
        sig_start_bit = 6
        sig_length = 15
        sig_value_factor = 0.00391
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 31970
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 6
        bmuws_info = [(0, 0b01111111, 0b10000000, 7, 0), (1, 0b11111111, 0b00000000, 8, 0)]


class VgmConnFr34:
    msg_name = "VgmConnFr34"
    msg_id = 389
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.045
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['BNCM']

    class MobDevKeyEnaStsToBLEKey2:
        sig_name = "MobDevKeyEnaStsToBLEKey2"
        sig_start_bit = 3
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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
        sig_byteorder = "Motorola"
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

    class MobDevKeyEnaStsToBLEKey9:
        sig_name = "MobDevKeyEnaStsToBLEKey9"
        sig_start_bit = 21
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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

    class MobDevKeyEnaStsToBLEKey10:
        sig_name = "MobDevKeyEnaStsToBLEKey10"
        sig_start_bit = 19
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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

    class MobDevKeyEnaStsToBLEKey3:
        sig_name = "MobDevKeyEnaStsToBLEKey3"
        sig_start_bit = 1
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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

    class MobDevKeyEnaStsToBLEKey8:
        sig_name = "MobDevKeyEnaStsToBLEKey8"
        sig_start_bit = 23
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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

    class MobDevKeyEnaStsToBLEKey6:
        sig_name = "MobDevKeyEnaStsToBLEKey6"
        sig_start_bit = 11
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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

    class MobDevKeyEnaStsToBLEKey5:
        sig_name = "MobDevKeyEnaStsToBLEKey5"
        sig_start_bit = 13
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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

    class DigKeyPasEntryDiSts:
        sig_name = "DigKeyPasEntryDiSts"
        sig_start_bit = 30
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

    class MobDevKeyEnaStsToBLEKey1:
        sig_name = "MobDevKeyEnaStsToBLEKey1"
        sig_start_bit = 5
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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

    class MobDevKeyEnaStsToBLEKey11:
        sig_name = "MobDevKeyEnaStsToBLEKey11"
        sig_start_bit = 17
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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
        sig_byteorder = "Motorola"
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

    class MobDevKeyEnaStsToBLEKey7:
        sig_name = "MobDevKeyEnaStsToBLEKey7"
        sig_start_bit = 9
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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


class VgmConnFr30:
    msg_name = "VgmConnFr30"
    msg_id = 58
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.085
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['BNCM']

    class PrkgOutModBtnStsToAPPPrkgOutModBtnSts5:
        sig_name = "PrkgOutModBtnStsToAPPPrkgOutModBtnSts5"
        sig_start_bit = 11
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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
        sig_byteorder = "Motorola"
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

    class PrkgOutModBtnStsToAPPPrkgOutModBtnSts6:
        sig_name = "PrkgOutModBtnStsToAPPPrkgOutModBtnSts6"
        sig_start_bit = 9
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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

    class PrkgOutModBtnStsToAPPPrkgOutModBtnSts3:
        sig_name = "PrkgOutModBtnStsToAPPPrkgOutModBtnSts3"
        sig_start_bit = 15
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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

    class PrkgOutModBtnStsToAPPPrkgOutModBtnSts2:
        sig_name = "PrkgOutModBtnStsToAPPPrkgOutModBtnSts2"
        sig_start_bit = 1
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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

    class PrkgOutModBtnStsToAPPPrkgOutModBtnSts4:
        sig_name = "PrkgOutModBtnStsToAPPPrkgOutModBtnSts4"
        sig_start_bit = 13
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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


class VgmConnFr31:
    msg_name = "VgmConnFr31"
    msg_id = 61
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['TCAM']

    class DriftModStsDriftModDendReason_1_VgmConnSignalIPdu31:
        sig_name = "DriftModStsDriftModDendReason_1_VgmConnSignalIPdu31"
        sig_start_bit = 7
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class DriftModStsDriftModDeactive_1_VgmConnSignalIPdu31:
        sig_name = "DriftModStsDriftModDeactive_1_VgmConnSignalIPdu31"
        sig_start_bit = 22
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

    class DriftModStsDriftModActSts_1_VgmConnSignalIPdu31:
        sig_name = "DriftModStsDriftModActSts_1_VgmConnSignalIPdu31"
        sig_start_bit = 23
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

    class DriftModStsDriftModEnaSts_1_VgmConnSignalIPdu31:
        sig_name = "DriftModStsDriftModEnaSts_1_VgmConnSignalIPdu31"
        sig_start_bit = 21
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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
    tx_node = "WPC"
    rx_nodes = ['BGM']


class BgmConnectivityFr08:
    msg_name = "BgmConnectivityFr08"
    msg_id = 901
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['TCAM', 'BNCM']

    class BodyRemoteWindowFBBodyRemoteWindowFRPosnAtPass:
        sig_name = "BodyRemoteWindowFBBodyRemoteWindowFRPosnAtPass"
        sig_start_bit = 34
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WinAndRoofAndCurtPosnTyp_PosnUkwn': 0, 'WinAndRoofAndCurtPosnTyp_ClsFull': 1, 'WinAndRoofAndCurtPosnTyp_PercOpen4': 2, 'WinAndRoofAndCurtPosnTyp_PercOpen8': 3, 'WinAndRoofAndCurtPosnTyp_PercOpen12': 4, 'WinAndRoofAndCurtPosnTyp_PercOpen16': 5, 'WinAndRoofAndCurtPosnTyp_PercOpen20': 6, 'WinAndRoofAndCurtPosnTyp_PercOpen24': 7, 'WinAndRoofAndCurtPosnTyp_PercOpen28': 8, 'WinAndRoofAndCurtPosnTyp_PercOpen32': 9, 'WinAndRoofAndCurtPosnTyp_PercOpen36': 10, 'WinAndRoofAndCurtPosnTyp_PercOpen40': 11, 'WinAndRoofAndCurtPosnTyp_PercOpen44': 12, 'WinAndRoofAndCurtPosnTyp_PercOpen48': 13, 'WinAndRoofAndCurtPosnTyp_PercOpen52': 14, 'WinAndRoofAndCurtPosnTyp_PercOpen56': 15, 'WinAndRoofAndCurtPosnTyp_PercOpen60': 16, 'WinAndRoofAndCurtPosnTyp_PercOpen64': 17, 'WinAndRoofAndCurtPosnTyp_PercOpen68': 18, 'WinAndRoofAndCurtPosnTyp_PercOpen72': 19, 'WinAndRoofAndCurtPosnTyp_PercOpen76': 20, 'WinAndRoofAndCurtPosnTyp_PercOpen80': 21, 'WinAndRoofAndCurtPosnTyp_PercOpen84': 22, 'WinAndRoofAndCurtPosnTyp_PercOpen88': 23, 'WinAndRoofAndCurtPosnTyp_PercOpen92': 24, 'WinAndRoofAndCurtPosnTyp_PercOpen96': 25, 'WinAndRoofAndCurtPosnTyp_OpenFull': 26, 'WinAndRoofAndCurtPosnTyp_Resd1': 27, 'WinAndRoofAndCurtPosnTyp_Resd2': 28, 'WinAndRoofAndCurtPosnTyp_Resd3': 29, 'WinAndRoofAndCurtPosnTyp_Resd4': 30, 'WinAndRoofAndCurtPosnTyp_Movg': 31}
        compute_method = None
        length = 5
        startbit = 34
        bmuws_info = [(4, 0b00000111, 0b11111000, 3, 0), (5, 0b11000000, 0b00111111, 2, 6)]

    class BodyRemoteLockFBLeReLockSts:
        sig_name = "BodyRemoteLockFBLeReLockSts"
        sig_start_bit = 31
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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

    class TireFilRxSwt:
        sig_name = "TireFilRxSwt"
        sig_start_bit = 11
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

    class BodyRemoteWindowFBBodyRemoteWindowFRPosnAtDrvr:
        sig_name = "BodyRemoteWindowFBBodyRemoteWindowFRPosnAtDrvr"
        sig_start_bit = 39
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Motorola"
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

    class BodyRemoteWindowFBBodyRemoteWindowFRPosnAtReRi:
        sig_name = "BodyRemoteWindowFBBodyRemoteWindowFRPosnAtReRi"
        sig_start_bit = 40
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WinAndRoofAndCurtPosnTyp_PosnUkwn': 0, 'WinAndRoofAndCurtPosnTyp_ClsFull': 1, 'WinAndRoofAndCurtPosnTyp_PercOpen4': 2, 'WinAndRoofAndCurtPosnTyp_PercOpen8': 3, 'WinAndRoofAndCurtPosnTyp_PercOpen12': 4, 'WinAndRoofAndCurtPosnTyp_PercOpen16': 5, 'WinAndRoofAndCurtPosnTyp_PercOpen20': 6, 'WinAndRoofAndCurtPosnTyp_PercOpen24': 7, 'WinAndRoofAndCurtPosnTyp_PercOpen28': 8, 'WinAndRoofAndCurtPosnTyp_PercOpen32': 9, 'WinAndRoofAndCurtPosnTyp_PercOpen36': 10, 'WinAndRoofAndCurtPosnTyp_PercOpen40': 11, 'WinAndRoofAndCurtPosnTyp_PercOpen44': 12, 'WinAndRoofAndCurtPosnTyp_PercOpen48': 13, 'WinAndRoofAndCurtPosnTyp_PercOpen52': 14, 'WinAndRoofAndCurtPosnTyp_PercOpen56': 15, 'WinAndRoofAndCurtPosnTyp_PercOpen60': 16, 'WinAndRoofAndCurtPosnTyp_PercOpen64': 17, 'WinAndRoofAndCurtPosnTyp_PercOpen68': 18, 'WinAndRoofAndCurtPosnTyp_PercOpen72': 19, 'WinAndRoofAndCurtPosnTyp_PercOpen76': 20, 'WinAndRoofAndCurtPosnTyp_PercOpen80': 21, 'WinAndRoofAndCurtPosnTyp_PercOpen84': 22, 'WinAndRoofAndCurtPosnTyp_PercOpen88': 23, 'WinAndRoofAndCurtPosnTyp_PercOpen92': 24, 'WinAndRoofAndCurtPosnTyp_PercOpen96': 25, 'WinAndRoofAndCurtPosnTyp_OpenFull': 26, 'WinAndRoofAndCurtPosnTyp_Resd1': 27, 'WinAndRoofAndCurtPosnTyp_Resd2': 28, 'WinAndRoofAndCurtPosnTyp_Resd3': 29, 'WinAndRoofAndCurtPosnTyp_Resd4': 30, 'WinAndRoofAndCurtPosnTyp_Movg': 31}
        compute_method = None
        length = 5
        startbit = 40
        bmuws_info = [(5, 0b00000001, 0b11111110, 1, 0), (6, 0b11110000, 0b00001111, 4, 4)]

    class BodyRemoteLockFBPassLockSts:
        sig_name = "BodyRemoteLockFBPassLockSts"
        sig_start_bit = 29
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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

    class BodyRemoteWindowFBBodyRemoteWindowFRPosnAtReLe:
        sig_name = "BodyRemoteWindowFBBodyRemoteWindowFRPosnAtReLe"
        sig_start_bit = 45
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Motorola"
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

    class BodyRemoteLockFBDrvLockSts:
        sig_name = "BodyRemoteLockFBDrvLockSts"
        sig_start_bit = 19
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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

    class BodyRemoteLockFBRiReLockSts:
        sig_name = "BodyRemoteLockFBRiReLockSts"
        sig_start_bit = 17
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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

    class TireFilNoiseFlrSwt:
        sig_name = "TireFilNoiseFlrSwt"
        sig_start_bit = 12
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class RemBookChrgnTarVal_0_BgmConnSignalIPdu08:
        sig_name = "RemBookChrgnTarVal_0_BgmConnSignalIPdu08"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0.0
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

    class BodyRemoteLockFBStatus:
        sig_name = "BodyRemoteLockFBStatus"
        sig_start_bit = 27
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 11
        sig_byteorder = "Motorola"
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

    class TireFilFilSwt:
        sig_name = "TireFilFilSwt"
        sig_start_bit = 13
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

    class TireFilSnsrID:
        sig_name = "TireFilSnsrID"
        sig_start_bit = 10
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
        startbit = 10
        byte = 1
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class BodyRemoteWindowFBStatus:
        sig_name = "BodyRemoteWindowFBStatus"
        sig_start_bit = 51
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 11
        sig_byteorder = "Motorola"
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

    class TireFilPollingMod:
        sig_name = "TireFilPollingMod"
        sig_start_bit = 23
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
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


class VgmConnFr27:
    msg_name = "VgmConnFr27"
    msg_id = 1093
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['TCAM']

    class DigKeyForNfcGidInfo2Byte2_1_VgmConnSignalIPdu27:
        sig_name = "DigKeyForNfcGidInfo2Byte2_1_VgmConnSignalIPdu27"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
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

    class DigKeyForNfcGidInfo2Byte6_1_VgmConnSignalIPdu27:
        sig_name = "DigKeyForNfcGidInfo2Byte6_1_VgmConnSignalIPdu27"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
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

    class DigKeyForNfcGidInfo2Byte5_1_VgmConnSignalIPdu27:
        sig_name = "DigKeyForNfcGidInfo2Byte5_1_VgmConnSignalIPdu27"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
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

    class DigKeyForNfcGidInfo2Byte0_1_VgmConnSignalIPdu27:
        sig_name = "DigKeyForNfcGidInfo2Byte0_1_VgmConnSignalIPdu27"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
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

    class DigKeyForNfcGidInfo2Byte1_1_VgmConnSignalIPdu27:
        sig_name = "DigKeyForNfcGidInfo2Byte1_1_VgmConnSignalIPdu27"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
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

    class DigKeyForNfcGidInfo2Byte3_1_VgmConnSignalIPdu27:
        sig_name = "DigKeyForNfcGidInfo2Byte3_1_VgmConnSignalIPdu27"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
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

    class DigKeyForNfcGidInfo2Byte4_1_VgmConnSignalIPdu27:
        sig_name = "DigKeyForNfcGidInfo2Byte4_1_VgmConnSignalIPdu27"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
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

    class DigKeyForNfcGidInfo2Byte7_1_VgmConnSignalIPdu27:
        sig_name = "DigKeyForNfcGidInfo2Byte7_1_VgmConnSignalIPdu27"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
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


class BgmConnectivityFr01:
    msg_name = "BgmConnectivityFr01"
    msg_id = 367
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['TCAM']

    class DigKeyGidInfo1Byte2_0_BgmConnectivitySignalIPdu01:
        sig_name = "DigKeyGidInfo1Byte2_0_BgmConnectivitySignalIPdu01"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
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

    class DigKeyGidInfo1Byte1_0_BgmConnectivitySignalIPdu01:
        sig_name = "DigKeyGidInfo1Byte1_0_BgmConnectivitySignalIPdu01"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
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

    class DigKeyGidInfo1Byte6_0_BgmConnectivitySignalIPdu01:
        sig_name = "DigKeyGidInfo1Byte6_0_BgmConnectivitySignalIPdu01"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
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

    class DigKeyGidInfo1Byte5_0_BgmConnectivitySignalIPdu01:
        sig_name = "DigKeyGidInfo1Byte5_0_BgmConnectivitySignalIPdu01"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
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

    class DigKeyGidInfo1Byte3_0_BgmConnectivitySignalIPdu01:
        sig_name = "DigKeyGidInfo1Byte3_0_BgmConnectivitySignalIPdu01"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
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

    class DigKeyGidInfo1Byte7_0_BgmConnectivitySignalIPdu01:
        sig_name = "DigKeyGidInfo1Byte7_0_BgmConnectivitySignalIPdu01"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
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

    class DigKeyGidInfo1Byte0_0_BgmConnectivitySignalIPdu01:
        sig_name = "DigKeyGidInfo1Byte0_0_BgmConnectivitySignalIPdu01"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
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

    class DigKeyGidInfo1Byte4_0_BgmConnectivitySignalIPdu01:
        sig_name = "DigKeyGidInfo1Byte4_0_BgmConnectivitySignalIPdu01"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
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


class VgmConnFr51:
    msg_name = "VgmConnFr51"
    msg_id = 597
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.25
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['TCAM']

    class HmiStrangerModMenuSetPasswordSt_1_VgmConnSignalIPdu51:
        sig_name = "HmiStrangerModMenuSetPasswordSt_1_VgmConnSignalIPdu51"
        sig_start_bit = 49
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
        startbit = 49
        byte = 6
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class HmiStrangerModMenuSetActvInActv_1_VgmConnSignalIPdu51:
        sig_name = "HmiStrangerModMenuSetActvInActv_1_VgmConnSignalIPdu51"
        sig_start_bit = 50
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class HmiStrangerModMenuSetPrivateLockSt_1_VgmConnSignalIPdu51:
        sig_name = "HmiStrangerModMenuSetPrivateLockSt_1_VgmConnSignalIPdu51"
        sig_start_bit = 48
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
        startbit = 48
        byte = 6
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class HmiStrangerModMenuSetSpdLim_1_VgmConnSignalIPdu51:
        sig_name = "HmiStrangerModMenuSetSpdLim_1_VgmConnSignalIPdu51"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
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

    class RemClimaDefrstSts_1_VgmConnSignalIPdu51:
        sig_name = "RemClimaDefrstSts_1_VgmConnSignalIPdu51"
        sig_start_bit = 30
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


class VgmConnFr17:
    msg_name = "VgmConnFr17"
    msg_id = 1072
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.07
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['TCAM', 'BNCM']

    class VinVINSignalPos5_1_VgmConnSignalIPdu17:
        sig_name = "VinVINSignalPos5_1_VgmConnSignalIPdu17"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
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

    class VinBlockNr_1_VgmConnSignalIPdu17:
        sig_name = "VinBlockNr_1_VgmConnSignalIPdu17"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
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

    class VinVINSignalPos4_1_VgmConnSignalIPdu17:
        sig_name = "VinVINSignalPos4_1_VgmConnSignalIPdu17"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
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

    class VinVINSignalPos3_1_VgmConnSignalIPdu17:
        sig_name = "VinVINSignalPos3_1_VgmConnSignalIPdu17"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
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

    class VinVINSignalPos7_1_VgmConnSignalIPdu17:
        sig_name = "VinVINSignalPos7_1_VgmConnSignalIPdu17"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
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

    class VinVINSignalPos6_1_VgmConnSignalIPdu17:
        sig_name = "VinVINSignalPos6_1_VgmConnSignalIPdu17"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
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

    class VinVINSignalPos1_1_VgmConnSignalIPdu17:
        sig_name = "VinVINSignalPos1_1_VgmConnSignalIPdu17"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
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

    class VinVINSignalPos2_1_VgmConnSignalIPdu17:
        sig_name = "VinVINSignalPos2_1_VgmConnSignalIPdu17"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
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


class BncmConnectivityFr17:
    msg_name = "BncmConnectivityFr17"
    msg_id = 408
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "BNCM"
    rx_nodes = ['BGM', 'BGM']

    class BLEMobDevSts:
        sig_name = "BLEMobDevSts"
        sig_start_bit = 19
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
        startbit = 19
        byte = 2
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class BLEConRPACtrlFrnt_0_BncmConnectivitySignalIPdu17:
        sig_name = "BLEConRPACtrlFrnt_0_BncmConnectivitySignalIPdu17"
        sig_start_bit = 5
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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

    class UsgModChgReqFromBLE:
        sig_name = "UsgModChgReqFromBLE"
        sig_start_bit = 6
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
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class BLEConStsForAVP:
        sig_name = "BLEConStsForAVP"
        sig_start_bit = 21
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

    class BLEConRPACtrlRgt_0_BncmConnectivitySignalIPdu17:
        sig_name = "BLEConRPACtrlRgt_0_BncmConnectivitySignalIPdu17"
        sig_start_bit = 12
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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

    class BLEConRPACtrlLeft_0_BncmConnectivitySignalIPdu17:
        sig_name = "BLEConRPACtrlLeft_0_BncmConnectivitySignalIPdu17"
        sig_start_bit = 2
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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

    class BLEConRPACtrlRear_0_BncmConnectivitySignalIPdu17:
        sig_name = "BLEConRPACtrlRear_0_BncmConnectivitySignalIPdu17"
        sig_start_bit = 15
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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


class BncmConnectivityVFCVectorFr:
    msg_name = "BncmConnectivityVFCVectorFr"
    msg_id = 1355
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BNCM"
    rx_nodes = ['CCM']

    class VFCVectorBNCMVFCid12:
        sig_name = "VFCVectorBNCMVFCid12"
        sig_start_bit = 14
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 14
        byte = 1
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorBNCMVFCid25:
        sig_name = "VFCVectorBNCMVFCid25"
        sig_start_bit = 27
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 27
        byte = 3
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorBNCMVFCid60:
        sig_name = "VFCVectorBNCMVFCid60"
        sig_start_bit = 62
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 62
        byte = 7
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorBNCMVFCid22:
        sig_name = "VFCVectorBNCMVFCid22"
        sig_start_bit = 24
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 24
        byte = 3
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorBNCMVFCid55:
        sig_name = "VFCVectorBNCMVFCid55"
        sig_start_bit = 57
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 57
        byte = 7
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorBNCMVFCid36:
        sig_name = "VFCVectorBNCMVFCid36"
        sig_start_bit = 38
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 38
        byte = 4
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorBNCMVFCid18:
        sig_name = "VFCVectorBNCMVFCid18"
        sig_start_bit = 20
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 20
        byte = 2
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorBNCMVFCid21:
        sig_name = "VFCVectorBNCMVFCid21"
        sig_start_bit = 23
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 23
        byte = 2
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorBNCMVFCid40:
        sig_name = "VFCVectorBNCMVFCid40"
        sig_start_bit = 42
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 42
        byte = 5
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorBNCMVFCid45:
        sig_name = "VFCVectorBNCMVFCid45"
        sig_start_bit = 47
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 47
        byte = 5
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorBNCMVFCid49:
        sig_name = "VFCVectorBNCMVFCid49"
        sig_start_bit = 51
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 51
        byte = 6
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorBNCMVFCid42:
        sig_name = "VFCVectorBNCMVFCid42"
        sig_start_bit = 44
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 44
        byte = 5
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorBNCMVFCid11:
        sig_name = "VFCVectorBNCMVFCid11"
        sig_start_bit = 13
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 13
        byte = 1
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorBNCMVFCid53:
        sig_name = "VFCVectorBNCMVFCid53"
        sig_start_bit = 55
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 55
        byte = 6
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorBNCMVFCid2:
        sig_name = "VFCVectorBNCMVFCid2"
        sig_start_bit = 4
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 4
        byte = 0
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorBNCMBlockID:
        sig_name = "VFCVectorBNCMBlockID"
        sig_start_bit = 1
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
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VFCVectorBNCMVFCid5:
        sig_name = "VFCVectorBNCMVFCid5"
        sig_start_bit = 7
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorBNCMVFCid54:
        sig_name = "VFCVectorBNCMVFCid54"
        sig_start_bit = 56
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 56
        byte = 7
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorBNCMVFCid57:
        sig_name = "VFCVectorBNCMVFCid57"
        sig_start_bit = 59
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 59
        byte = 7
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorBNCMVFCid15:
        sig_name = "VFCVectorBNCMVFCid15"
        sig_start_bit = 17
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 17
        byte = 2
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorBNCMVFCid44:
        sig_name = "VFCVectorBNCMVFCid44"
        sig_start_bit = 46
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 46
        byte = 5
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorBNCMVFCid14:
        sig_name = "VFCVectorBNCMVFCid14"
        sig_start_bit = 16
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 16
        byte = 2
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorBNCMVFCid51:
        sig_name = "VFCVectorBNCMVFCid51"
        sig_start_bit = 53
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 53
        byte = 6
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorBNCMVFCid35:
        sig_name = "VFCVectorBNCMVFCid35"
        sig_start_bit = 37
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 37
        byte = 4
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorBNCMVFCid4:
        sig_name = "VFCVectorBNCMVFCid4"
        sig_start_bit = 6
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorBNCMVFCid46:
        sig_name = "VFCVectorBNCMVFCid46"
        sig_start_bit = 48
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 48
        byte = 6
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorBNCMVFCid58:
        sig_name = "VFCVectorBNCMVFCid58"
        sig_start_bit = 60
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 60
        byte = 7
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorBNCMVFCid26:
        sig_name = "VFCVectorBNCMVFCid26"
        sig_start_bit = 28
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 28
        byte = 3
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorBNCMVFCid32:
        sig_name = "VFCVectorBNCMVFCid32"
        sig_start_bit = 34
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 34
        byte = 4
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorBNCMVFCid1:
        sig_name = "VFCVectorBNCMVFCid1"
        sig_start_bit = 3
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 3
        byte = 0
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorBNCMVFCid6:
        sig_name = "VFCVectorBNCMVFCid6"
        sig_start_bit = 8
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 8
        byte = 1
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorBNCMVFCid17:
        sig_name = "VFCVectorBNCMVFCid17"
        sig_start_bit = 19
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 19
        byte = 2
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorBNCMVFCid37:
        sig_name = "VFCVectorBNCMVFCid37"
        sig_start_bit = 39
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 39
        byte = 4
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorBNCMVFCid29:
        sig_name = "VFCVectorBNCMVFCid29"
        sig_start_bit = 31
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 31
        byte = 3
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorBNCMVFCid48:
        sig_name = "VFCVectorBNCMVFCid48"
        sig_start_bit = 50
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 50
        byte = 6
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorBNCMVFCid56:
        sig_name = "VFCVectorBNCMVFCid56"
        sig_start_bit = 58
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 58
        byte = 7
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorBNCMVFCid8:
        sig_name = "VFCVectorBNCMVFCid8"
        sig_start_bit = 10
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 10
        byte = 1
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorBNCMVFCid47:
        sig_name = "VFCVectorBNCMVFCid47"
        sig_start_bit = 49
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 49
        byte = 6
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorBNCMVFCid27:
        sig_name = "VFCVectorBNCMVFCid27"
        sig_start_bit = 29
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 29
        byte = 3
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorBNCMVFCid13:
        sig_name = "VFCVectorBNCMVFCid13"
        sig_start_bit = 15
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 15
        byte = 1
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorBNCMVFCid3:
        sig_name = "VFCVectorBNCMVFCid3"
        sig_start_bit = 5
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorBNCMVFCid30:
        sig_name = "VFCVectorBNCMVFCid30"
        sig_start_bit = 32
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 32
        byte = 4
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorBNCMVFCid33:
        sig_name = "VFCVectorBNCMVFCid33"
        sig_start_bit = 35
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 35
        byte = 4
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorBNCMVFCid9:
        sig_name = "VFCVectorBNCMVFCid9"
        sig_start_bit = 11
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 11
        byte = 1
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorBNCMVFCid16:
        sig_name = "VFCVectorBNCMVFCid16"
        sig_start_bit = 18
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 18
        byte = 2
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorBNCMVFCid10:
        sig_name = "VFCVectorBNCMVFCid10"
        sig_start_bit = 12
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 12
        byte = 1
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorBNCMVFCid0:
        sig_name = "VFCVectorBNCMVFCid0"
        sig_start_bit = 2
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 2
        byte = 0
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorBNCMVFCid19:
        sig_name = "VFCVectorBNCMVFCid19"
        sig_start_bit = 21
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 21
        byte = 2
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorBNCMVFCid38:
        sig_name = "VFCVectorBNCMVFCid38"
        sig_start_bit = 40
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 40
        byte = 5
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorBNCMVFCid52:
        sig_name = "VFCVectorBNCMVFCid52"
        sig_start_bit = 54
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 54
        byte = 6
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorBNCMVFCid59:
        sig_name = "VFCVectorBNCMVFCid59"
        sig_start_bit = 61
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 61
        byte = 7
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorBNCMVFCid7:
        sig_name = "VFCVectorBNCMVFCid7"
        sig_start_bit = 9
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 9
        byte = 1
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorBNCMVFCid50:
        sig_name = "VFCVectorBNCMVFCid50"
        sig_start_bit = 52
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorBNCMVFCid43:
        sig_name = "VFCVectorBNCMVFCid43"
        sig_start_bit = 45
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 45
        byte = 5
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorBNCMVFCid31:
        sig_name = "VFCVectorBNCMVFCid31"
        sig_start_bit = 33
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 33
        byte = 4
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorBNCMVFCid24:
        sig_name = "VFCVectorBNCMVFCid24"
        sig_start_bit = 26
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 26
        byte = 3
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorBNCMVFCid28:
        sig_name = "VFCVectorBNCMVFCid28"
        sig_start_bit = 30
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 30
        byte = 3
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorBNCMVFCid23:
        sig_name = "VFCVectorBNCMVFCid23"
        sig_start_bit = 25
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 25
        byte = 3
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorBNCMVFCid34:
        sig_name = "VFCVectorBNCMVFCid34"
        sig_start_bit = 36
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 36
        byte = 4
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorBNCMVFCid39:
        sig_name = "VFCVectorBNCMVFCid39"
        sig_start_bit = 41
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 41
        byte = 5
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorBNCMVFCid61:
        sig_name = "VFCVectorBNCMVFCid61"
        sig_start_bit = 63
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 63
        byte = 7
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorBNCMVFCid20:
        sig_name = "VFCVectorBNCMVFCid20"
        sig_start_bit = 22
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 22
        byte = 2
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorBNCMVFCid41:
        sig_name = "VFCVectorBNCMVFCid41"
        sig_start_bit = 43
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 43
        byte = 5
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3


class BgmConnectivityFr03:
    msg_name = "BgmConnectivityFr03"
    msg_id = 372
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.09
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['BNCM']

    class BookChargeSetResponse_1_BgmConnectivitySignalIPdu03:
        sig_name = "BookChargeSetResponse_1_BgmConnectivitySignalIPdu03"
        sig_start_bit = 42
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
        startbit = 42
        byte = 5
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class ChrgnSpd_1_BgmConnectivitySignalIPdu03:
        sig_name = "ChrgnSpd_1_BgmConnectivitySignalIPdu03"
        sig_start_bit = 31
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
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11100000, 0b00011111, 3, 5)]

    class HvBattChrgnTiEstimd_1_BgmConnectivitySignalIPdu03:
        sig_name = "HvBattChrgnTiEstimd_1_BgmConnectivitySignalIPdu03"
        sig_start_bit = 14
        sig_length = 11
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 2047
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 14
        bmuws_info = [(1, 0b01111111, 0b10000000, 7, 0), (2, 0b11110000, 0b00001111, 4, 4)]

    class DstEstimdToEmptyForDrvgElec_1_BgmConnectivitySignalIPdu03:
        sig_name = "DstEstimdToEmptyForDrvgElec_1_BgmConnectivitySignalIPdu03"
        sig_start_bit = 36
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
        startbit = 36
        bmuws_info = [(4, 0b00011111, 0b11100000, 5, 0), (5, 0b11111000, 0b00000111, 5, 3)]


class VgmConnFr26:
    msg_name = "VgmConnFr26"
    msg_id = 1088
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['TCAM']

    class DigKeyForNfcGidInfo1Byte7_1_VgmConnSignalIPdu26:
        sig_name = "DigKeyForNfcGidInfo1Byte7_1_VgmConnSignalIPdu26"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
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

    class DigKeyForNfcGidInfo1Byte0_1_VgmConnSignalIPdu26:
        sig_name = "DigKeyForNfcGidInfo1Byte0_1_VgmConnSignalIPdu26"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
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

    class DigKeyForNfcGidInfo1Byte5_1_VgmConnSignalIPdu26:
        sig_name = "DigKeyForNfcGidInfo1Byte5_1_VgmConnSignalIPdu26"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
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

    class DigKeyForNfcGidInfo1Byte6_1_VgmConnSignalIPdu26:
        sig_name = "DigKeyForNfcGidInfo1Byte6_1_VgmConnSignalIPdu26"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
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

    class DigKeyForNfcGidInfo1Byte1_1_VgmConnSignalIPdu26:
        sig_name = "DigKeyForNfcGidInfo1Byte1_1_VgmConnSignalIPdu26"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
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

    class DigKeyForNfcGidInfo1Byte4_1_VgmConnSignalIPdu26:
        sig_name = "DigKeyForNfcGidInfo1Byte4_1_VgmConnSignalIPdu26"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
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

    class DigKeyForNfcGidInfo1Byte2_1_VgmConnSignalIPdu26:
        sig_name = "DigKeyForNfcGidInfo1Byte2_1_VgmConnSignalIPdu26"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
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

    class DigKeyForNfcGidInfo1Byte3_1_VgmConnSignalIPdu26:
        sig_name = "DigKeyForNfcGidInfo1Byte3_1_VgmConnSignalIPdu26"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
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


class WpcConnectivityCANNmFr:
    msg_name = "WpcConnectivityCANNmFr"
    msg_id = 1296
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "WPC"
    rx_nodes = ['BGM']


class TcamConnectivityFr31:
    msg_name = "TcamConnectivityFr31"
    msg_id = 381
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 24
    tx_node = "TCAM"
    rx_nodes = ['BGM']

    class TireRFNoiseMsgNrOfSamples:
        sig_name = "TireRFNoiseMsgNrOfSamples"
        sig_start_bit = 23
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class TireSnsrDataRFactory:
        sig_name = "TireSnsrDataRFactory"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
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

    class TelmAVPReq:
        sig_name = "TelmAVPReq"
        sig_start_bit = 167
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
        startbit = 167
        byte = 20
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class RSSI:
        sig_name = "RSSI"
        sig_start_bit = 159
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
        startbit = 159
        byte = 19
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
        sig_byteorder = "Motorola"
        sig_value_init = 4294967295
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 32
        startbit = 71
        bmuws_info = [(8, 0b11111111, 0b00000000, 8, 0), (9, 0b11111111, 0b00000000, 8, 0), (10, 0b11111111, 0b00000000, 8, 0), (11, 0b11111111, 0b00000000, 8, 0)]

    class TelmLockgCenRVIReq:
        sig_name = "TelmLockgCenRVIReq"
        sig_start_bit = 164
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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

    class TireSnsrDataRFct:
        sig_name = "TireSnsrDataRFct"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
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

    class TireSnsrDataRA:
        sig_name = "TireSnsrDataRA"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
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

    class TiStamping:
        sig_name = "TiStamping"
        sig_start_bit = 119
        sig_length = 24
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 24
        startbit = 119
        bmuws_info = [(14, 0b11111111, 0b00000000, 8, 0), (15, 0b11111111, 0b00000000, 8, 0), (16, 0b11111111, 0b00000000, 8, 0)]

    class TireSnsrDataRP:
        sig_name = "TireSnsrDataRP"
        sig_start_bit = 103
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

    class TireRFNoiseMsgMinNoiseFlr:
        sig_name = "TireRFNoiseMsgMinNoiseFlr"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = 0.4
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

    class RFFrameCntr:
        sig_name = "RFFrameCntr"
        sig_start_bit = 151
        sig_length = 8
        sig_value_factor = None
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

    class TireSnsrDataRChks:
        sig_name = "TireSnsrDataRChks"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
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

    class TireSnsrDataRT:
        sig_name = "TireSnsrDataRT"
        sig_start_bit = 111
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
        startbit = 111
        byte = 13
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

    class TelmCarFindRVIReq:
        sig_name = "TelmCarFindRVIReq"
        sig_start_bit = 166
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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

    class TireRFNoiseMsgAvgNoiseFlr:
        sig_name = "TireRFNoiseMsgAvgNoiseFlr"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 0.4
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


class TcamConnectivityFr01:
    msg_name = "TcamConnectivityFr01"
    msg_id = 357
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.06
    msg_length = 8
    tx_node = "TCAM"
    rx_nodes = ['BGM']

    class ImobVehRemReqAndRespImobVehDataRemReq0:
        sig_name = "ImobVehRemReqAndRespImobVehDataRemReq0"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
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

    class ImobVehRemReqAndRespImobVehRemReqCmd:
        sig_name = "ImobVehRemReqAndRespImobVehRemReqCmd"
        sig_start_bit = 2
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
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

    class ImobVehRemReqAndRespImobVehRemTmrOrSpdLim:
        sig_name = "ImobVehRemReqAndRespImobVehRemTmrOrSpdLim"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
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

    class ImobVehRemReqAndRespImobVehDataRemReq1:
        sig_name = "ImobVehRemReqAndRespImobVehDataRemReq1"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
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

    class ImobVehRemReqAndRespImobVehDataRemReq4:
        sig_name = "ImobVehRemReqAndRespImobVehDataRemReq4"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
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

    class ImobVehRemReqAndRespImobVehDataRemReq3:
        sig_name = "ImobVehRemReqAndRespImobVehDataRemReq3"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
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

    class ImobVehRemReqAndRespImobVehDataRemReq2:
        sig_name = "ImobVehRemReqAndRespImobVehDataRemReq2"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
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


class BgmConnectivityFr11:
    msg_name = "BgmConnectivityFr11"
    msg_id = 384
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 16
    tx_node = "BGM"
    rx_nodes = ['TCAM']

    class RVIChallengeFromBodyByte14:
        sig_name = "RVIChallengeFromBodyByte14"
        sig_start_bit = 119
        sig_length = 8
        sig_value_factor = None
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

    class RVIChallengeFromBodyByte3:
        sig_name = "RVIChallengeFromBodyByte3"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
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

    class RVIChallengeFromBodyByte5:
        sig_name = "RVIChallengeFromBodyByte5"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
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

    class RVIChallengeFromBodyByte8:
        sig_name = "RVIChallengeFromBodyByte8"
        sig_start_bit = 71
        sig_length = 8
        sig_value_factor = None
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

    class RVIChallengeFromBodyByte10:
        sig_name = "RVIChallengeFromBodyByte10"
        sig_start_bit = 87
        sig_length = 8
        sig_value_factor = None
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

    class RVIChallengeFromBodyByte13:
        sig_name = "RVIChallengeFromBodyByte13"
        sig_start_bit = 111
        sig_length = 8
        sig_value_factor = None
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

    class RVIChallengeFromBodyByte9:
        sig_name = "RVIChallengeFromBodyByte9"
        sig_start_bit = 79
        sig_length = 8
        sig_value_factor = None
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

    class RVIChallengeFromBodyByte2:
        sig_name = "RVIChallengeFromBodyByte2"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
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

    class RVIChallengeFromBodyByte11:
        sig_name = "RVIChallengeFromBodyByte11"
        sig_start_bit = 95
        sig_length = 8
        sig_value_factor = None
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

    class RVIChallengeFromBodyByte1:
        sig_name = "RVIChallengeFromBodyByte1"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
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

    class RVIChallengeFromBodyByte12:
        sig_name = "RVIChallengeFromBodyByte12"
        sig_start_bit = 103
        sig_length = 8
        sig_value_factor = None
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

    class RVIChallengeFromBodyByte0:
        sig_name = "RVIChallengeFromBodyByte0"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
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

    class RVIChallengeFromBodyByte15:
        sig_name = "RVIChallengeFromBodyByte15"
        sig_start_bit = 127
        sig_length = 8
        sig_value_factor = None
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

    class RVIChallengeFromBodyByte7:
        sig_name = "RVIChallengeFromBodyByte7"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
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

    class RVIChallengeFromBodyByte4:
        sig_name = "RVIChallengeFromBodyByte4"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
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

    class RVIChallengeFromBodyByte6:
        sig_name = "RVIChallengeFromBodyByte6"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
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


class BgmToBncmConnectivityDiagReqFrame:
    msg_name = "BgmToBncmConnectivityDiagReqFrame"
    msg_id = 1827
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['BNCM']


class WpcConnFr02:
    msg_name = "WpcConnFr02"
    msg_id = 769
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.085
    msg_length = 8
    tx_node = "WPC"
    rx_nodes = ['BGM', 'BNCM']

    class PhoneForgottenRmn:
        sig_name = "PhoneForgottenRmn"
        sig_start_bit = 6
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

    class WPCModuleSts:
        sig_name = "WPCModuleSts"
        sig_start_bit = 12
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
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

    class WPCChrgnSts:
        sig_name = "WPCChrgnSts"
        sig_start_bit = 8
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WPCChrgnSts_Standby': 0, 'WPCChrgnSts_Charging': 1, 'WPCChrgnSts_ChargingcompletedAvailedwhenRxsupport': 2, 'WPCChrgnSts_Notinstandby': 3}
        compute_method = None
        length = 2
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b10000000, 0b01111111, 1, 7)]

    class WPCCtrlRes:
        sig_name = "WPCCtrlRes"
        sig_start_bit = 4
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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

    class WPCTearResFeedback:
        sig_name = "WPCTearResFeedback"
        sig_start_bit = 2
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Invalid': 0, 'NFCFeedbackkSts_RestSuccessfully': 1}
        compute_method = None
        length = 2
        startbit = 2
        byte = 0
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class WPCFailureSts:
        sig_name = "WPCFailureSts"
        sig_start_bit = 0
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WPCFailureSts_NoFailure': 0, 'WPCFailureSts_OverTemperature': 1, 'WPCFailureSts_RFOD': 2, 'WPCFailureSts_VoltageProtected': 3, 'WPCFailureSts_OverPowerProtected': 4, 'WPCFailureSts_InternalFailure': 5, 'WPCFailureSts_SmartPhoneNoResponseOrUnknown': 6, 'WPCFailureSts_OFOD': 7, 'WPCFailureSts_Reserved1': 8, 'WPCFailureSts_Reserved2': 9, 'WPCFailureSts_Reserved3': 10, 'WPCFailureSts_Reserved4': 11, 'WPCFailureSts_Reserved5': 12, 'WPCFailureSts_Reserved6': 13, 'WPCFailureSts_Reserved7': 14, 'WPCFailureSts_Invalid': 15}
        compute_method = None
        length = 4
        startbit = 0
        bmuws_info = [(0, 0b00000001, 0b11111110, 1, 0), (1, 0b11100000, 0b00011111, 3, 5)]


class VgmConnFr28:
    msg_name = "VgmConnFr28"
    msg_id = 48
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "BGM"
    rx_nodes = ['BNCM']

    class DigkeyBLEReq2:
        sig_name = "DigkeyBLEReq2"
        sig_start_bit = 0
        sig_length = 512
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Opaque"
        sig_value_init = None
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 512
        startbit = 0
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111111, 0b00000000, 8, 0), (8, 0b11111111, 0b00000000, 8, 0), (9, 0b11111111, 0b00000000, 8, 0), (10, 0b11111111, 0b00000000, 8, 0), (11, 0b11111111, 0b00000000, 8, 0), (12, 0b11111111, 0b00000000, 8, 0), (13, 0b11111111, 0b00000000, 8, 0), (14, 0b11111111, 0b00000000, 8, 0), (15, 0b11111111, 0b00000000, 8, 0), (16, 0b11111111, 0b00000000, 8, 0), (17, 0b11111111, 0b00000000, 8, 0), (18, 0b11111111, 0b00000000, 8, 0), (19, 0b11111111, 0b00000000, 8, 0), (20, 0b11111111, 0b00000000, 8, 0), (21, 0b11111111, 0b00000000, 8, 0), (22, 0b11111111, 0b00000000, 8, 0), (23, 0b11111111, 0b00000000, 8, 0), (24, 0b11111111, 0b00000000, 8, 0), (25, 0b11111111, 0b00000000, 8, 0), (26, 0b11111111, 0b00000000, 8, 0), (27, 0b11111111, 0b00000000, 8, 0), (28, 0b11111111, 0b00000000, 8, 0), (29, 0b11111111, 0b00000000, 8, 0), (30, 0b11111111, 0b00000000, 8, 0), (31, 0b11111111, 0b00000000, 8, 0), (32, 0b11111111, 0b00000000, 8, 0), (33, 0b11111111, 0b00000000, 8, 0), (34, 0b11111111, 0b00000000, 8, 0), (35, 0b11111111, 0b00000000, 8, 0), (36, 0b11111111, 0b00000000, 8, 0), (37, 0b11111111, 0b00000000, 8, 0), (38, 0b11111111, 0b00000000, 8, 0), (39, 0b11111111, 0b00000000, 8, 0), (40, 0b11111111, 0b00000000, 8, 0), (41, 0b11111111, 0b00000000, 8, 0), (42, 0b11111111, 0b00000000, 8, 0), (43, 0b11111111, 0b00000000, 8, 0), (44, 0b11111111, 0b00000000, 8, 0), (45, 0b11111111, 0b00000000, 8, 0), (46, 0b11111111, 0b00000000, 8, 0), (47, 0b11111111, 0b00000000, 8, 0), (48, 0b11111111, 0b00000000, 8, 0), (49, 0b11111111, 0b00000000, 8, 0), (50, 0b11111111, 0b00000000, 8, 0), (51, 0b11111111, 0b00000000, 8, 0), (52, 0b11111111, 0b00000000, 8, 0), (53, 0b11111111, 0b00000000, 8, 0), (54, 0b11111111, 0b00000000, 8, 0), (55, 0b11111111, 0b00000000, 8, 0), (56, 0b11111111, 0b00000000, 8, 0), (57, 0b11111111, 0b00000000, 8, 0), (58, 0b11111111, 0b00000000, 8, 0), (59, 0b11111111, 0b00000000, 8, 0), (60, 0b11111111, 0b00000000, 8, 0), (61, 0b11111111, 0b00000000, 8, 0), (62, 0b11111111, 0b00000000, 8, 0), (63, 0b11111111, 0b00000000, 8, 0)]


class BgmToAllConnectivityDiagReqFrame:
    msg_name = "BgmToAllConnectivityDiagReqFrame"
    msg_id = 2047
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['NKR', 'WPC', 'BNCM']


class VgmConnFr04:
    msg_name = "VgmConnFr04"
    msg_id = 768
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['TCAM', 'BNCM']

    class HoodSts_1_VgmConnSignalIPdu04:
        sig_name = "HoodSts_1_VgmConnSignalIPdu04"
        sig_start_bit = 47
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
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

    class IntPm25VluFrmClima_2_VgmConnSignalIPdu04:
        sig_name = "IntPm25VluFrmClima_2_VgmConnSignalIPdu04"
        sig_start_bit = 7
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
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]


class VgmConnFr09:
    msg_name = "VgmConnFr09"
    msg_id = 1056
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.085
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['BNCM']

    class AutoOpenSwtHmiReq:
        sig_name = "AutoOpenSwtHmiReq"
        sig_start_bit = 40
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
        startbit = 40
        byte = 5
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ApproachLiSetReq:
        sig_name = "ApproachLiSetReq"
        sig_start_bit = 22
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
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

    class PasAcsHmiPen:
        sig_name = "PasAcsHmiPen"
        sig_start_bit = 53
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
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

    class PasAcsHmiSts:
        sig_name = "PasAcsHmiSts"
        sig_start_bit = 54
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
        startbit = 54
        byte = 6
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class BleCtrlRPABtnStsRear:
        sig_name = "BleCtrlRPABtnStsRear"
        sig_start_bit = 3
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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

    class BleCtrlRPABtnStsFrnt:
        sig_name = "BleCtrlRPABtnStsFrnt"
        sig_start_bit = 7
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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

    class TrOpenerSts_2_VgmConnSignalIPdu09:
        sig_name = "TrOpenerSts_2_VgmConnSignalIPdu09"
        sig_start_bit = 35
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
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

    class BleCtrlRPABtnStsLftTurn:
        sig_name = "BleCtrlRPABtnStsLftTurn"
        sig_start_bit = 5
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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

    class BleCtrlRPABtnStsRgtTurn:
        sig_name = "BleCtrlRPABtnStsRgtTurn"
        sig_start_bit = 1
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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

    class SunRoofPosnSts_2_VgmConnSignalIPdu09:
        sig_name = "SunRoofPosnSts_2_VgmConnSignalIPdu09"
        sig_start_bit = 20
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Motorola"
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


class BgmConnectivityCANNmFr:
    msg_name = "BgmConnectivityCANNmFr"
    msg_id = 1331
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['WPC']


class BgmConnectivityFr04:
    msg_name = "BgmConnectivityFr04"
    msg_id = 400
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.09
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['BNCM']

    class VehTiAndDataDataValid_2_BgmConnectivitySignalIPdu04:
        sig_name = "VehTiAndDataDataValid_2_BgmConnectivitySignalIPdu04"
        sig_start_bit = 0
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
        startbit = 0
        byte = 0
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VehTiAndDataMth1_2_BgmConnectivitySignalIPdu04:
        sig_name = "VehTiAndDataMth1_2_BgmConnectivitySignalIPdu04"
        sig_start_bit = 19
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
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

    class VehTiAndDataMins1_2_BgmConnectivitySignalIPdu04:
        sig_name = "VehTiAndDataMins1_2_BgmConnectivitySignalIPdu04"
        sig_start_bit = 9
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

    class VehTiAndDataYr1_2_BgmConnectivitySignalIPdu04:
        sig_name = "VehTiAndDataYr1_2_BgmConnectivitySignalIPdu04"
        sig_start_bit = 7
        sig_length = 7
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
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

    class VehTiAndDataHr1_2_BgmConnectivitySignalIPdu04:
        sig_name = "VehTiAndDataHr1_2_BgmConnectivitySignalIPdu04"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111000
        unmask = 0b00000111
        shift = 3

    class VehTiAndDataDay_2_BgmConnectivitySignalIPdu04:
        sig_name = "VehTiAndDataDay_2_BgmConnectivitySignalIPdu04"
        sig_start_bit = 26
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 26
        bmuws_info = [(3, 0b00000111, 0b11111000, 3, 0), (4, 0b11000000, 0b00111111, 2, 6)]

    class VehTiAndDataSec1_2_BgmConnectivitySignalIPdu04:
        sig_name = "VehTiAndDataSec1_2_BgmConnectivitySignalIPdu04"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2


class VgmConnFr12:
    msg_name = "VgmConnFr12"
    msg_id = 1136
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['TCAM', 'WPC', 'BNCM']

    class OnBdChrgrRdyTi_1_VgmConnSignalIPdu12:
        sig_name = "OnBdChrgrRdyTi_1_VgmConnSignalIPdu12"
        sig_start_bit = 38
        sig_length = 7
        sig_value_factor = 100
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 127
        sig_byteorder = "Motorola"
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

    class LockgCenStsLockSt_2_VgmConnSignalIPdu12:
        sig_name = "LockgCenStsLockSt_2_VgmConnSignalIPdu12"
        sig_start_bit = 42
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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

    class CarTiGlb_8_VgmConnSignalIPdu12:
        sig_name = "CarTiGlb_8_VgmConnSignalIPdu12"
        sig_start_bit = 7
        sig_length = 32
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 4294967295
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 32
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class BookChrgnStsFb_1_VgmConnSignalIPdu12:
        sig_name = "BookChrgnStsFb_1_VgmConnSignalIPdu12"
        sig_start_bit = 57
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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

    class LockgCenStsTrigSrc_2_VgmConnSignalIPdu12:
        sig_name = "LockgCenStsTrigSrc_2_VgmConnSignalIPdu12"
        sig_start_bit = 46
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 11
        sig_byteorder = "Motorola"
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

    class RemClimaHvSts_1_VgmConnSignalIPdu12:
        sig_name = "RemClimaHvSts_1_VgmConnSignalIPdu12"
        sig_start_bit = 54
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
        startbit = 54
        byte = 6
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class GearLvrIndcn_2_VgmConnSignalIPdu12:
        sig_name = "GearLvrIndcn_2_VgmConnSignalIPdu12"
        sig_start_bit = 63
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
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

    class LockgCenStsUpdEve_2_VgmConnSignalIPdu12:
        sig_name = "LockgCenStsUpdEve_2_VgmConnSignalIPdu12"
        sig_start_bit = 40
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
        startbit = 40
        byte = 5
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0


class VgmConnFr32:
    msg_name = "VgmConnFr32"
    msg_id = 853
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.15
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['TCAM']

    class VehHomePrkgSysSts_1_VgmConnSignalIPdu32:
        sig_name = "VehHomePrkgSysSts_1_VgmConnSignalIPdu32"
        sig_start_bit = 12
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 18
        sig_byteorder = "Motorola"
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


class TcamConnectivityFr13:
    msg_name = "TcamConnectivityFr13"
    msg_id = 360
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.04
    msg_length = 8
    tx_node = "TCAM"
    rx_nodes = ['BGM']

    class RCcontrolForDCchargeLid:
        sig_name = "RCcontrolForDCchargeLid"
        sig_start_bit = 6
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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


class NkrConnectivityCANNmFr:
    msg_name = "NkrConnectivityCANNmFr"
    msg_id = 1297
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "NKR"
    rx_nodes = ['BNCM']


class BncmToBgmConnectivityDiagRespFrame:
    msg_name = "BncmToBgmConnectivityDiagRespFrame"
    msg_id = 1571
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BNCM"
    rx_nodes = ['BGM']


class VgmConnFr52:
    msg_name = "VgmConnFr52"
    msg_id = 346
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['TCAM']

    class HvSysRlyStsChks_2_VgmConnSignalIPdu52:
        sig_name = "HvSysRlyStsChks_2_VgmConnSignalIPdu52"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
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

    class HvSysRlyStsHvSysRlySts_2_VgmConnSignalIPdu52:
        sig_name = "HvSysRlyStsHvSysRlySts_2_VgmConnSignalIPdu52"
        sig_start_bit = 53
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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

    class HvSysRlyStsCntr_2_VgmConnSignalIPdu52:
        sig_name = "HvSysRlyStsCntr_2_VgmConnSignalIPdu52"
        sig_start_bit = 51
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


class BgmToWpcConnectivityDiagReqFrame:
    msg_name = "BgmToWpcConnectivityDiagReqFrame"
    msg_id = 1828
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['WPC']


class BgmToNkrConnectivityDiagReqFrame:
    msg_name = "BgmToNkrConnectivityDiagReqFrame"
    msg_id = 1829
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['NKR']


class TcamConnectivityFr02:
    msg_name = "TcamConnectivityFr02"
    msg_id = 544
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "TCAM"
    rx_nodes = ['BGM']

    class TelmClimaTmr_0_TcamConnectivitySignalIPdu02:
        sig_name = "TelmClimaTmr_0_TcamConnectivitySignalIPdu02"
        sig_start_bit = 39
        sig_length = 16
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 65535
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class TelmClimaReq_0_TcamConnectivitySignalIPdu02:
        sig_name = "TelmClimaReq_0_TcamConnectivitySignalIPdu02"
        sig_start_bit = 21
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
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

    class TelmPM25Req_0_TcamConnectivitySignalIPdu02:
        sig_name = "TelmPM25Req_0_TcamConnectivitySignalIPdu02"
        sig_start_bit = 18
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
        startbit = 18
        byte = 2
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class ReqFragLvlTelm_0_TcamConnectivitySignalIPdu02:
        sig_name = "ReqFragLvlTelm_0_TcamConnectivitySignalIPdu02"
        sig_start_bit = 17
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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

    class ClimaTmrStsTelmRqrd_0_TcamConnectivitySignalIPdu02:
        sig_name = "ClimaTmrStsTelmRqrd_0_TcamConnectivitySignalIPdu02"
        sig_start_bit = 22
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
        startbit = 22
        byte = 2
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class ClimaRqrd1_0_TcamConnectivitySignalIPdu02:
        sig_name = "ClimaRqrd1_0_TcamConnectivitySignalIPdu02"
        sig_start_bit = 13
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
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

    class TelmClimaTSetHmiCmptmtTSpSpcl_0_TcamConnectivitySignalIPdu02:
        sig_name = "TelmClimaTSetHmiCmptmtTSpSpcl_0_TcamConnectivitySignalIPdu02"
        sig_start_bit = 30
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
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

    class SeatHeatDurgClimaEnadFromTelm_0_TcamConnectivitySignalIPdu02:
        sig_name = "SeatHeatDurgClimaEnadFromTelm_0_TcamConnectivitySignalIPdu02"
        sig_start_bit = 10
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
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

    class TelmClimaTSetTempRange_0_TcamConnectivitySignalIPdu02:
        sig_name = "TelmClimaTSetTempRange_0_TcamConnectivitySignalIPdu02"
        sig_start_bit = 28
        sig_length = 5
        sig_value_factor = 0.5
        sig_value_offset = 15.5
        sig_value_min = 0
        sig_value_max = 26
        sig_byteorder = "Motorola"
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


class VgmConnFr33:
    msg_name = "VgmConnFr33"
    msg_id = 596
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.12
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['TCAM']

    class SceneModSeld_1_VgmConnSignalIPdu33:
        sig_name = "SceneModSeld_1_VgmConnSignalIPdu33"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 13
        sig_byteorder = "Motorola"
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

    class RemVentActvSts_1_VgmConnSignalIPdu33:
        sig_name = "RemVentActvSts_1_VgmConnSignalIPdu33"
        sig_start_bit = 5
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
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class ClimaOvrHeatProActvSts_2_VgmConnSignalIPdu33:
        sig_name = "ClimaOvrHeatProActvSts_2_VgmConnSignalIPdu33"
        sig_start_bit = 6
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

    class CdsParkgClimaActv_1_VgmConnSignalIPdu33:
        sig_name = "CdsParkgClimaActv_1_VgmConnSignalIPdu33"
        sig_start_bit = 7
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

    class RemVentWarnSts_1_VgmConnSignalIPdu33:
        sig_name = "RemVentWarnSts_1_VgmConnSignalIPdu33"
        sig_start_bit = 15
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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

    class RemVentReqRspnFb_1_VgmConnSignalIPdu33:
        sig_name = "RemVentReqRspnFb_1_VgmConnSignalIPdu33"
        sig_start_bit = 4
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
        startbit = 4
        byte = 0
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4


class TcamConnectivityFr12:
    msg_name = "TcamConnectivityFr12"
    msg_id = 356
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.04
    msg_length = 8
    tx_node = "TCAM"
    rx_nodes = ['BGM']

    class RemHvStrtActvReq_0_TcamConnectivitySignalIPdu12:
        sig_name = "RemHvStrtActvReq_0_TcamConnectivitySignalIPdu12"
        sig_start_bit = 41
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
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

    class RemStrtExtnTiReq_0_TcamConnectivitySignalIPdu12:
        sig_name = "RemStrtExtnTiReq_0_TcamConnectivitySignalIPdu12"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class RemStrtHvCtrlReqErsRunTime_0_TcamConnectivitySignalIPdu12:
        sig_name = "RemStrtHvCtrlReqErsRunTime_0_TcamConnectivitySignalIPdu12"
        sig_start_bit = 37
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
        startbit = 37
        byte = 4
        mask = 0b00111111
        unmask = 0b11000000
        shift = 0

    class RemDCChrgLidTelmReq:
        sig_name = "RemDCChrgLidTelmReq"
        sig_start_bit = 18
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
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

    class RemStrtHvCtrlReqErsCmd_0_TcamConnectivitySignalIPdu12:
        sig_name = "RemStrtHvCtrlReqErsCmd_0_TcamConnectivitySignalIPdu12"
        sig_start_bit = 39
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
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


class NfcrConnFr01:
    msg_name = "NfcrConnFr01"
    msg_id = 822
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "NKR"
    rx_nodes = ['BNCM']


class BgmConnectivityFr06:
    msg_name = "BgmConnectivityFr06"
    msg_id = 405
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 32
    tx_node = "BGM"
    rx_nodes = ['BNCM']

    class HavpModBtnSts2:
        sig_name = "HavpModBtnSts2"
        sig_start_bit = 87
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
        startbit = 87
        byte = 10
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class SteerWhlSnsrCntr_2_BgmConnSignalIPdu06:
        sig_name = "SteerWhlSnsrCntr_2_BgmConnSignalIPdu06"
        sig_start_bit = 167
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
        startbit = 167
        byte = 20
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class RemCntDwn:
        sig_name = "RemCntDwn"
        sig_start_bit = 108
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
        startbit = 108
        bmuws_info = [(13, 0b00011111, 0b11100000, 5, 0), (14, 0b11111000, 0b00000111, 5, 3)]

    class ElecChromRoofFb_1_BgmConnSignalIPdu06:
        sig_name = "ElecChromRoofFb_1_BgmConnSignalIPdu06"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class DCChrgnHndlSts_1_BgmConnSignalIPdu06:
        sig_name = "DCChrgnHndlSts_1_BgmConnSignalIPdu06"
        sig_start_bit = 42
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
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

    class HavpSts:
        sig_name = "HavpSts"
        sig_start_bit = 79
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
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

    class HavpSysStsDisp:
        sig_name = "HavpSysStsDisp"
        sig_start_bit = 71
        sig_length = 8
        sig_value_factor = None
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

    class RPASysDisp:
        sig_name = "RPASysDisp"
        sig_start_bit = 151
        sig_length = 8
        sig_value_factor = None
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

    class SteerWhlSnsrChks_2_BgmConnSignalIPdu06:
        sig_name = "SteerWhlSnsrChks_2_BgmConnSignalIPdu06"
        sig_start_bit = 159
        sig_length = 8
        sig_value_factor = None
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

    class SteerWhlSnsrAg_2_BgmConnSignalIPdu06:
        sig_name = "SteerWhlSnsrAg_2_BgmConnSignalIPdu06"
        sig_start_bit = 161
        sig_length = 15
        sig_value_factor = "9.765625E-4"
        sig_value_offset = 0.0
        sig_value_min = -14848
        sig_value_max = 14848
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 161
        bmuws_info = [(20, 0b00000011, 0b11111100, 2, 0), (21, 0b11111111, 0b00000000, 8, 0), (22, 0b11111000, 0b00000111, 5, 3)]

    class HavpModBtnSts4:
        sig_name = "HavpModBtnSts4"
        sig_start_bit = 83
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
        startbit = 83
        byte = 10
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class HavpReminder:
        sig_name = "HavpReminder"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
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

    class SteerWhlSnsrQf_2_BgmConnSignalIPdu06:
        sig_name = "SteerWhlSnsrQf_2_BgmConnSignalIPdu06"
        sig_start_bit = 163
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
        startbit = 163
        byte = 20
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class HvBattSoc_1_BgmConnSignalIPdu06:
        sig_name = "HvBattSoc_1_BgmConnSignalIPdu06"
        sig_start_bit = 103
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 2000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 103
        bmuws_info = [(12, 0b11111111, 0b00000000, 8, 0), (13, 0b11100000, 0b00011111, 3, 5)]

    class HavpModBtnSts1:
        sig_name = "HavpModBtnSts1"
        sig_start_bit = 73
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
        startbit = 73
        byte = 9
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class HavpBleFctSts:
        sig_name = "HavpBleFctSts"
        sig_start_bit = 75
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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

    class TotDstTrvld_0_BgmConnSignalIPdu06:
        sig_name = "TotDstTrvld_0_BgmConnSignalIPdu06"
        sig_start_bit = 114
        sig_length = 25
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 20000000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 25
        startbit = 114
        bmuws_info = [(14, 0b00000111, 0b11111000, 3, 0), (15, 0b11111111, 0b00000000, 8, 0), (16, 0b11111111, 0b00000000, 8, 0), (17, 0b11111100, 0b00000011, 6, 2)]

    class HavpModBtnSts3:
        sig_name = "HavpModBtnSts3"
        sig_start_bit = 85
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
        startbit = 85
        byte = 10
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class SteerWhlSnsrAgSpd_2_BgmConnSignalIPdu06:
        sig_name = "SteerWhlSnsrAgSpd_2_BgmConnSignalIPdu06"
        sig_start_bit = 178
        sig_length = 14
        sig_value_factor = 0.0078125
        sig_value_offset = 0.0
        sig_value_min = -6400
        sig_value_max = 6400
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 14
        startbit = 178
        bmuws_info = [(22, 0b00000111, 0b11111000, 3, 0), (23, 0b11111111, 0b00000000, 8, 0), (24, 0b11100000, 0b00011111, 3, 5)]


class BncmBsrmConnectivityFr06:
    msg_name = "BncmBsrmConnectivityFr06"
    msg_id = 782
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "BNCM"
    rx_nodes = ['NKR']


class TcamConnectivityCanDevFr01:
    msg_name = "TcamConnectivityCanDevFr01"
    msg_id = 1425
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "TCAM"
    rx_nodes = ['CCM']

    class TCAMdevelpsignalgrouprespFunctiondevpsignalgroup1:
        sig_name = "TCAMdevelpsignalgrouprespFunctiondevpsignalgroup1"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
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

    class TCAMdevelpsignalgrouprespFunctiondevpsignalgroup4:
        sig_name = "TCAMdevelpsignalgrouprespFunctiondevpsignalgroup4"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
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

    class TCAMdevelpsignalgrouprespFunctiondevpsignalgroup3:
        sig_name = "TCAMdevelpsignalgrouprespFunctiondevpsignalgroup3"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
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

    class TCAMdevelpsignalgrouprespFunctiondevpsignalgroup7:
        sig_name = "TCAMdevelpsignalgrouprespFunctiondevpsignalgroup7"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
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

    class TCAMdevelpsignalgrouprespFunctiondevpsignalgroup2:
        sig_name = "TCAMdevelpsignalgrouprespFunctiondevpsignalgroup2"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
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

    class TCAMdevelpsignalgrouprespFunctiondevpsignalgroup8:
        sig_name = "TCAMdevelpsignalgrouprespFunctiondevpsignalgroup8"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
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

    class TCAMdevelpsignalgrouprespFunctiondevpsignalgroup5:
        sig_name = "TCAMdevelpsignalgrouprespFunctiondevpsignalgroup5"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
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

    class TCAMdevelpsignalgrouprespFunctiondevpsignalgroup6:
        sig_name = "TCAMdevelpsignalgrouprespFunctiondevpsignalgroup6"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
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


class TcamConnectivityFr06:
    msg_name = "TcamConnectivityFr06"
    msg_id = 293
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "TCAM"
    rx_nodes = ['BGM']

    class DKDataFromTelmDKDataByte6:
        sig_name = "DKDataFromTelmDKDataByte6"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
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

    class DKDataFromTelmDKDataByte5:
        sig_name = "DKDataFromTelmDKDataByte5"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
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

    class DKDataFromTelmDKDataByte3:
        sig_name = "DKDataFromTelmDKDataByte3"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
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

    class DKDataFromTelmHeader:
        sig_name = "DKDataFromTelmHeader"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
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

    class DKDataFromTelmDKDataByte4:
        sig_name = "DKDataFromTelmDKDataByte4"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
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

    class DKDataFromTelmDKDataByte1:
        sig_name = "DKDataFromTelmDKDataByte1"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
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

    class DKDataFromTelmAcknowledgment:
        sig_name = "DKDataFromTelmAcknowledgment"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
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

    class DKDataFromTelmDKDataByte2:
        sig_name = "DKDataFromTelmDKDataByte2"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
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


class VgmConnFr23:
    msg_name = "VgmConnFr23"
    msg_id = 323
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['BNCM']

    class RPAAuthRespAcknowledgment:
        sig_name = "RPAAuthRespAcknowledgment"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
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

    class RPAAuthRespDKDataByte1:
        sig_name = "RPAAuthRespDKDataByte1"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
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

    class RPAAuthRespDKDataByte6:
        sig_name = "RPAAuthRespDKDataByte6"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
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

    class RPAAuthRespDKDataByte4:
        sig_name = "RPAAuthRespDKDataByte4"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
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

    class RPAAuthRespHeader:
        sig_name = "RPAAuthRespHeader"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
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

    class RPAAuthRespDKDataByte3:
        sig_name = "RPAAuthRespDKDataByte3"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
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

    class RPAAuthRespDKDataByte5:
        sig_name = "RPAAuthRespDKDataByte5"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
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

    class RPAAuthRespDKDataByte2:
        sig_name = "RPAAuthRespDKDataByte2"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
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


class NkrToBgmConnectivityDiagRespFrame:
    msg_name = "NkrToBgmConnectivityDiagRespFrame"
    msg_id = 1573
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "NKR"
    rx_nodes = ['BGM']


class TcamConnectivityFr03:
    msg_name = "TcamConnectivityFr03"
    msg_id = 837
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "TCAM"
    rx_nodes = ['BGM']

    class TelmFctReq:
        sig_name = "TelmFctReq"
        sig_start_bit = 27
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
        startbit = 27
        byte = 3
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class TelmSeatDrvHeatClimaLvl_0_TcamConnectivitySignalIPdu03:
        sig_name = "TelmSeatDrvHeatClimaLvl_0_TcamConnectivitySignalIPdu03"
        sig_start_bit = 33
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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

    class TelmSeatSecRiHeatClimaLvl_0_TcamConnectivitySignalIPdu03:
        sig_name = "TelmSeatSecRiHeatClimaLvl_0_TcamConnectivitySignalIPdu03"
        sig_start_bit = 31
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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

    class TelmSeatPassHeatClimaLvl_0_TcamConnectivitySignalIPdu03:
        sig_name = "TelmSeatPassHeatClimaLvl_0_TcamConnectivitySignalIPdu03"
        sig_start_bit = 13
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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

    class TelmSeatPassVentnClimaLvl_0_TcamConnectivitySignalIPdu03:
        sig_name = "TelmSeatPassVentnClimaLvl_0_TcamConnectivitySignalIPdu03"
        sig_start_bit = 23
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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

    class TelmSeatSecRiVentnClimaLvl_0_TcamConnectivitySignalIPdu03:
        sig_name = "TelmSeatSecRiVentnClimaLvl_0_TcamConnectivitySignalIPdu03"
        sig_start_bit = 29
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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

    class TelmSeatDrvVentnClimaLvl_0_TcamConnectivitySignalIPdu03:
        sig_name = "TelmSeatDrvVentnClimaLvl_0_TcamConnectivitySignalIPdu03"
        sig_start_bit = 15
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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

    class TelmSeatSecLeVentnClimaLvl_0_TcamConnectivitySignalIPdu03:
        sig_name = "TelmSeatSecLeVentnClimaLvl_0_TcamConnectivitySignalIPdu03"
        sig_start_bit = 19
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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
        sig_byteorder = "Motorola"
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

    class TelmSeatSecLeHeatClimaLvl_0_TcamConnectivitySignalIPdu03:
        sig_name = "TelmSeatSecLeHeatClimaLvl_0_TcamConnectivitySignalIPdu03"
        sig_start_bit = 21
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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

    class EngPermitReqFromTelm:
        sig_name = "EngPermitReqFromTelm"
        sig_start_bit = 41
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
        startbit = 41
        byte = 5
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class RemVentReq_0_TcamConnectivitySignalIPdu03:
        sig_name = "RemVentReq_0_TcamConnectivitySignalIPdu03"
        sig_start_bit = 26
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
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

    class SteerWhlHeatgDurgClimaEnadFromTelm_0_TcamConnectivitySignalIPdu03:
        sig_name = "SteerWhlHeatgDurgClimaEnadFromTelm_0_TcamConnectivitySignalIPdu03"
        sig_start_bit = 11
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


class BncmConnectivityFr14:
    msg_name = "BncmConnectivityFr14"
    msg_id = 24
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.045
    msg_length = 8
    tx_node = "BNCM"
    rx_nodes = ['BGM']

    class MobDevDistStsKey3:
        sig_name = "MobDevDistStsKey3"
        sig_start_bit = 25
        sig_length = 10
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
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
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class MobDevDistStsKey5:
        sig_name = "MobDevDistStsKey5"
        sig_start_bit = 53
        sig_length = 10
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
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
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 13
        bmuws_info = [(1, 0b00111111, 0b11000000, 6, 0), (2, 0b11110000, 0b00001111, 4, 4)]

    class PasEntryEnaReq:
        sig_name = "PasEntryEnaReq"
        sig_start_bit = 58
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
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 19
        bmuws_info = [(2, 0b00001111, 0b11110000, 4, 0), (3, 0b11111100, 0b00000011, 6, 2)]

    class MobDevDistStsKey0:
        sig_name = "MobDevDistStsKey0"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]


class BgmConnectivityFr09:
    msg_name = "BgmConnectivityFr09"
    msg_id = 533
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.09
    msg_length = 16
    tx_node = "BGM"
    rx_nodes = ['BNCM']

    class AVPAccountInfoByte3:
        sig_name = "AVPAccountInfoByte3"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
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

    class AVPAccountInfoByte5:
        sig_name = "AVPAccountInfoByte5"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
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

    class AVPAccountInfoByte14:
        sig_name = "AVPAccountInfoByte14"
        sig_start_bit = 119
        sig_length = 8
        sig_value_factor = None
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

    class AVPAccountInfoByte15:
        sig_name = "AVPAccountInfoByte15"
        sig_start_bit = 127
        sig_length = 8
        sig_value_factor = None
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

    class AVPAccountInfoByte4:
        sig_name = "AVPAccountInfoByte4"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
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

    class AVPAccountInfoByte11:
        sig_name = "AVPAccountInfoByte11"
        sig_start_bit = 95
        sig_length = 8
        sig_value_factor = None
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

    class AVPAccountInfoByte2:
        sig_name = "AVPAccountInfoByte2"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
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

    class AVPAccountInfoByte13:
        sig_name = "AVPAccountInfoByte13"
        sig_start_bit = 111
        sig_length = 8
        sig_value_factor = None
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

    class AVPAccountInfoByte9:
        sig_name = "AVPAccountInfoByte9"
        sig_start_bit = 79
        sig_length = 8
        sig_value_factor = None
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

    class AVPAccountInfoByte6:
        sig_name = "AVPAccountInfoByte6"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
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

    class AVPAccountInfoByte8:
        sig_name = "AVPAccountInfoByte8"
        sig_start_bit = 71
        sig_length = 8
        sig_value_factor = None
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

    class AVPAccountInfoByte1:
        sig_name = "AVPAccountInfoByte1"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
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

    class AVPAccountInfoByte0:
        sig_name = "AVPAccountInfoByte0"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
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

    class AVPAccountInfoByte7:
        sig_name = "AVPAccountInfoByte7"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
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

    class AVPAccountInfoByte12:
        sig_name = "AVPAccountInfoByte12"
        sig_start_bit = 103
        sig_length = 8
        sig_value_factor = None
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

    class AVPAccountInfoByte10:
        sig_name = "AVPAccountInfoByte10"
        sig_start_bit = 87
        sig_length = 8
        sig_value_factor = None
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


class VgmConnFr16:
    msg_name = "VgmConnFr16"
    msg_id = 343
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "BGM"
    rx_nodes = ['BNCM']

    class DigKeyBLEResp:
        sig_name = "DigKeyBLEResp"
        sig_start_bit = 0
        sig_length = 512
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Opaque"
        sig_value_init = None
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 512
        startbit = 0
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111111, 0b00000000, 8, 0), (8, 0b11111111, 0b00000000, 8, 0), (9, 0b11111111, 0b00000000, 8, 0), (10, 0b11111111, 0b00000000, 8, 0), (11, 0b11111111, 0b00000000, 8, 0), (12, 0b11111111, 0b00000000, 8, 0), (13, 0b11111111, 0b00000000, 8, 0), (14, 0b11111111, 0b00000000, 8, 0), (15, 0b11111111, 0b00000000, 8, 0), (16, 0b11111111, 0b00000000, 8, 0), (17, 0b11111111, 0b00000000, 8, 0), (18, 0b11111111, 0b00000000, 8, 0), (19, 0b11111111, 0b00000000, 8, 0), (20, 0b11111111, 0b00000000, 8, 0), (21, 0b11111111, 0b00000000, 8, 0), (22, 0b11111111, 0b00000000, 8, 0), (23, 0b11111111, 0b00000000, 8, 0), (24, 0b11111111, 0b00000000, 8, 0), (25, 0b11111111, 0b00000000, 8, 0), (26, 0b11111111, 0b00000000, 8, 0), (27, 0b11111111, 0b00000000, 8, 0), (28, 0b11111111, 0b00000000, 8, 0), (29, 0b11111111, 0b00000000, 8, 0), (30, 0b11111111, 0b00000000, 8, 0), (31, 0b11111111, 0b00000000, 8, 0), (32, 0b11111111, 0b00000000, 8, 0), (33, 0b11111111, 0b00000000, 8, 0), (34, 0b11111111, 0b00000000, 8, 0), (35, 0b11111111, 0b00000000, 8, 0), (36, 0b11111111, 0b00000000, 8, 0), (37, 0b11111111, 0b00000000, 8, 0), (38, 0b11111111, 0b00000000, 8, 0), (39, 0b11111111, 0b00000000, 8, 0), (40, 0b11111111, 0b00000000, 8, 0), (41, 0b11111111, 0b00000000, 8, 0), (42, 0b11111111, 0b00000000, 8, 0), (43, 0b11111111, 0b00000000, 8, 0), (44, 0b11111111, 0b00000000, 8, 0), (45, 0b11111111, 0b00000000, 8, 0), (46, 0b11111111, 0b00000000, 8, 0), (47, 0b11111111, 0b00000000, 8, 0), (48, 0b11111111, 0b00000000, 8, 0), (49, 0b11111111, 0b00000000, 8, 0), (50, 0b11111111, 0b00000000, 8, 0), (51, 0b11111111, 0b00000000, 8, 0), (52, 0b11111111, 0b00000000, 8, 0), (53, 0b11111111, 0b00000000, 8, 0), (54, 0b11111111, 0b00000000, 8, 0), (55, 0b11111111, 0b00000000, 8, 0), (56, 0b11111111, 0b00000000, 8, 0), (57, 0b11111111, 0b00000000, 8, 0), (58, 0b11111111, 0b00000000, 8, 0), (59, 0b11111111, 0b00000000, 8, 0), (60, 0b11111111, 0b00000000, 8, 0), (61, 0b11111111, 0b00000000, 8, 0), (62, 0b11111111, 0b00000000, 8, 0), (63, 0b11111111, 0b00000000, 8, 0)]


class VgmConnFr05:
    msg_name = "VgmConnFr05"
    msg_id = 896
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.17
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['TCAM', 'BNCM']

    class ChrgLidFrntLockSts:
        sig_name = "ChrgLidFrntLockSts"
        sig_start_bit = 33
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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

    class ChrgLidFrntSts_1_VgmConnSignalIPdu05:
        sig_name = "ChrgLidFrntSts_1_VgmConnSignalIPdu05"
        sig_start_bit = 41
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
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

    class ChrgLidRearSts_2_VgmConnSignalIPdu05:
        sig_name = "ChrgLidRearSts_2_VgmConnSignalIPdu05"
        sig_start_bit = 43
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
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

    class CarLoctrActvnSts:
        sig_name = "CarLoctrActvnSts"
        sig_start_bit = 47
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
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

    class PrkgClimaWarn_2_VgmConnSignalIPdu05:
        sig_name = "PrkgClimaWarn_2_VgmConnSignalIPdu05"
        sig_start_bit = 20
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 8
        sig_byteorder = "Motorola"
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

    class DCChrgSt_1_VgmConnSignalIPdu05:
        sig_name = "DCChrgSt_1_VgmConnSignalIPdu05"
        sig_start_bit = 39
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 13
        sig_byteorder = "Motorola"
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

    class EngForbidRespFromVMM:
        sig_name = "EngForbidRespFromVMM"
        sig_start_bit = 44
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
        startbit = 44
        byte = 5
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class BattURaw_2_VgmConnSignalIPdu05:
        sig_name = "BattURaw_2_VgmConnSignalIPdu05"
        sig_start_bit = 15
        sig_length = 9
        sig_value_factor = 0.025
        sig_value_offset = 5.0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 15
        bmuws_info = [(1, 0b11111111, 0b00000000, 8, 0), (2, 0b10000000, 0b01111111, 1, 7)]

    class TankFlapSts_1_VgmConnSignalIPdu05:
        sig_name = "TankFlapSts_1_VgmConnSignalIPdu05"
        sig_start_bit = 58
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
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


class BncmConnectivityFr08:
    msg_name = "BncmConnectivityFr08"
    msg_id = 374
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "BNCM"
    rx_nodes = ['BGM']

    class DigKeyBLEReq3:
        sig_name = "DigKeyBLEReq3"
        sig_start_bit = 0
        sig_length = 512
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Opaque"
        sig_value_init = None
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 512
        startbit = 0
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111111, 0b00000000, 8, 0), (8, 0b11111111, 0b00000000, 8, 0), (9, 0b11111111, 0b00000000, 8, 0), (10, 0b11111111, 0b00000000, 8, 0), (11, 0b11111111, 0b00000000, 8, 0), (12, 0b11111111, 0b00000000, 8, 0), (13, 0b11111111, 0b00000000, 8, 0), (14, 0b11111111, 0b00000000, 8, 0), (15, 0b11111111, 0b00000000, 8, 0), (16, 0b11111111, 0b00000000, 8, 0), (17, 0b11111111, 0b00000000, 8, 0), (18, 0b11111111, 0b00000000, 8, 0), (19, 0b11111111, 0b00000000, 8, 0), (20, 0b11111111, 0b00000000, 8, 0), (21, 0b11111111, 0b00000000, 8, 0), (22, 0b11111111, 0b00000000, 8, 0), (23, 0b11111111, 0b00000000, 8, 0), (24, 0b11111111, 0b00000000, 8, 0), (25, 0b11111111, 0b00000000, 8, 0), (26, 0b11111111, 0b00000000, 8, 0), (27, 0b11111111, 0b00000000, 8, 0), (28, 0b11111111, 0b00000000, 8, 0), (29, 0b11111111, 0b00000000, 8, 0), (30, 0b11111111, 0b00000000, 8, 0), (31, 0b11111111, 0b00000000, 8, 0), (32, 0b11111111, 0b00000000, 8, 0), (33, 0b11111111, 0b00000000, 8, 0), (34, 0b11111111, 0b00000000, 8, 0), (35, 0b11111111, 0b00000000, 8, 0), (36, 0b11111111, 0b00000000, 8, 0), (37, 0b11111111, 0b00000000, 8, 0), (38, 0b11111111, 0b00000000, 8, 0), (39, 0b11111111, 0b00000000, 8, 0), (40, 0b11111111, 0b00000000, 8, 0), (41, 0b11111111, 0b00000000, 8, 0), (42, 0b11111111, 0b00000000, 8, 0), (43, 0b11111111, 0b00000000, 8, 0), (44, 0b11111111, 0b00000000, 8, 0), (45, 0b11111111, 0b00000000, 8, 0), (46, 0b11111111, 0b00000000, 8, 0), (47, 0b11111111, 0b00000000, 8, 0), (48, 0b11111111, 0b00000000, 8, 0), (49, 0b11111111, 0b00000000, 8, 0), (50, 0b11111111, 0b00000000, 8, 0), (51, 0b11111111, 0b00000000, 8, 0), (52, 0b11111111, 0b00000000, 8, 0), (53, 0b11111111, 0b00000000, 8, 0), (54, 0b11111111, 0b00000000, 8, 0), (55, 0b11111111, 0b00000000, 8, 0), (56, 0b11111111, 0b00000000, 8, 0), (57, 0b11111111, 0b00000000, 8, 0), (58, 0b11111111, 0b00000000, 8, 0), (59, 0b11111111, 0b00000000, 8, 0), (60, 0b11111111, 0b00000000, 8, 0), (61, 0b11111111, 0b00000000, 8, 0), (62, 0b11111111, 0b00000000, 8, 0), (63, 0b11111111, 0b00000000, 8, 0)]


class BncmBsrmConnectivityFr04:
    msg_name = "BncmBsrmConnectivityFr04"
    msg_id = 325
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BNCM"
    rx_nodes = ['BGM']

    class RPAAuthReqHeader:
        sig_name = "RPAAuthReqHeader"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
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

    class RPAAuthReqDKDataByte4:
        sig_name = "RPAAuthReqDKDataByte4"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
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

    class RPAAuthReqDKDataByte3:
        sig_name = "RPAAuthReqDKDataByte3"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
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

    class RPAAuthReqDKDataByte2:
        sig_name = "RPAAuthReqDKDataByte2"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
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

    class RPAAuthReqDKDataByte6:
        sig_name = "RPAAuthReqDKDataByte6"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
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

    class RPAAuthReqDKDataByte1:
        sig_name = "RPAAuthReqDKDataByte1"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
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

    class RPAAuthReqDKDataByte5:
        sig_name = "RPAAuthReqDKDataByte5"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
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

    class RPAAuthReqAcknowledgment:
        sig_name = "RPAAuthReqAcknowledgment"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
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


class VgmConnFr14:
    msg_name = "VgmConnFr14"
    msg_id = 864
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.155
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['TCAM', 'BNCM']

    class PassSeatHeatgAvlSts_2_VgmConnSignalIPdu14:
        sig_name = "PassSeatHeatgAvlSts_2_VgmConnSignalIPdu14"
        sig_start_bit = 4
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
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

    class DrvrSeatHeatgLvlSts_2_VgmConnSignalIPdu14:
        sig_name = "DrvrSeatHeatgLvlSts_2_VgmConnSignalIPdu14"
        sig_start_bit = 1
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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

    class DrvrSeatVentnLvlSts_2_VgmConnSignalIPdu14:
        sig_name = "DrvrSeatVentnLvlSts_2_VgmConnSignalIPdu14"
        sig_start_bit = 39
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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

    class EcoClimaSts_2_VgmConnSignalIPdu14:
        sig_name = "EcoClimaSts_2_VgmConnSignalIPdu14"
        sig_start_bit = 45
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
        startbit = 45
        byte = 5
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class PassSeatHeatgLvlSts_2_VgmConnSignalIPdu14:
        sig_name = "PassSeatHeatgLvlSts_2_VgmConnSignalIPdu14"
        sig_start_bit = 9
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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

    class PassSeatVentAvlSts_2_VgmConnSignalIPdu14:
        sig_name = "PassSeatVentAvlSts_2_VgmConnSignalIPdu14"
        sig_start_bit = 20
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
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

    class SeatVentnLvlStsRowSecRi_1_VgmConnSignalIPdu14:
        sig_name = "SeatVentnLvlStsRowSecRi_1_VgmConnSignalIPdu14"
        sig_start_bit = 33
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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

    class DrvrSeatVentAvlSts_2_VgmConnSignalIPdu14:
        sig_name = "DrvrSeatVentAvlSts_2_VgmConnSignalIPdu14"
        sig_start_bit = 23
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
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

    class DrvrSeatHeatgAvlSts_2_VgmConnSignalIPdu14:
        sig_name = "DrvrSeatHeatgAvlSts_2_VgmConnSignalIPdu14"
        sig_start_bit = 7
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
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

    class TrSts_3_VgmConnSignalIPdu14:
        sig_name = "TrSts_3_VgmConnSignalIPdu14"
        sig_start_bit = 47
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
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

    class PassSeatVentnLvlSts_2_VgmConnSignalIPdu14:
        sig_name = "PassSeatVentnLvlSts_2_VgmConnSignalIPdu14"
        sig_start_bit = 37
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
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


class BncmConnectivityFr12:
    msg_name = "BncmConnectivityFr12"
    msg_id = 16
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "BNCM"
    rx_nodes = ['BGM']

    class DigKeyIDFndInStsByte2:
        sig_name = "DigKeyIDFndInStsByte2"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
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

    class DigKeyIDFndInStsDigKeyInSearchSts:
        sig_name = "DigKeyIDFndInStsDigKeyInSearchSts"
        sig_start_bit = 3
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 8
        sig_byteorder = "Motorola"
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

    class DigKeyIDFndInStsByte3:
        sig_name = "DigKeyIDFndInStsByte3"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
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

    class DigKeyIDFndInStsByte6:
        sig_name = "DigKeyIDFndInStsByte6"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
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

    class DigKeyIDFndInStsByte4:
        sig_name = "DigKeyIDFndInStsByte4"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
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

    class DigKeyIDFndInStsByte1:
        sig_name = "DigKeyIDFndInStsByte1"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
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

    class DigKeyIDFndInStsByte5:
        sig_name = "DigKeyIDFndInStsByte5"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
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


class WpcConnFr01:
    msg_name = "WpcConnFr01"
    msg_id = 810
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "WPC"
    rx_nodes = ['BNCM']


class BncmConnectivityFr13:
    msg_name = "BncmConnectivityFr13"
    msg_id = 20
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "BNCM"
    rx_nodes = ['BGM']

    class DigKeyIDFndOutStsByte4:
        sig_name = "DigKeyIDFndOutStsByte4"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
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

    class DigKeyIDFndOutStsByte6:
        sig_name = "DigKeyIDFndOutStsByte6"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
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

    class DigKeyIDFndOutStsByte2:
        sig_name = "DigKeyIDFndOutStsByte2"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
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

    class DigKeyIDFndOutStsDigKeyOutSearchSts:
        sig_name = "DigKeyIDFndOutStsDigKeyOutSearchSts"
        sig_start_bit = 2
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 6
        sig_byteorder = "Motorola"
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

    class DigKeyIDFndOutStsByte5:
        sig_name = "DigKeyIDFndOutStsByte5"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
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

    class DigKeyIDFndOutStsByte1:
        sig_name = "DigKeyIDFndOutStsByte1"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
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

    class DigKeyIDFndOutStsByte3:
        sig_name = "DigKeyIDFndOutStsByte3"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
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


