class VddmToEcmPropDiagReqFrame:
    msg_name = "VddmToEcmPropDiagReqFrame"
    msg_id = 1840
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class SrsEtcPropDevFr01:
    msg_name = "SrsEtcPropDevFr01"
    msg_id = 1456
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "SRS"
    rx_nodes = ['CCM']
    sig_group_dict = {'SRSdevelpsignalgroupTX': ['SRSdevelpsignalgroupTXFunctiondevpsignalgroup1', 'SRSdevelpsignalgroupTXFunctiondevpsignalgroup2', 'SRSdevelpsignalgroupTXFunctiondevpsignalgroup3', 'SRSdevelpsignalgroupTXFunctiondevpsignalgroup4', 'SRSdevelpsignalgroupTXFunctiondevpsignalgroup5', 'SRSdevelpsignalgroupTXFunctiondevpsignalgroup6', 'SRSdevelpsignalgroupTXFunctiondevpsignalgroup7', 'SRSdevelpsignalgroupTXFunctiondevpsignalgroup8']}
    sig_group_dataid_dict = {}

    class SRSdevelpsignalgroupTXFunctiondevpsignalgroup4:
        sig_name = "SRSdevelpsignalgroupTXFunctiondevpsignalgroup4"
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

    class SRSdevelpsignalgroupTXFunctiondevpsignalgroup2:
        sig_name = "SRSdevelpsignalgroupTXFunctiondevpsignalgroup2"
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

    class SRSdevelpsignalgroupTXFunctiondevpsignalgroup1:
        sig_name = "SRSdevelpsignalgroupTXFunctiondevpsignalgroup1"
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

    class SRSdevelpsignalgroupTXFunctiondevpsignalgroup8:
        sig_name = "SRSdevelpsignalgroupTXFunctiondevpsignalgroup8"
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

    class SRSdevelpsignalgroupTXFunctiondevpsignalgroup6:
        sig_name = "SRSdevelpsignalgroupTXFunctiondevpsignalgroup6"
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

    class SRSdevelpsignalgroupTXFunctiondevpsignalgroup5:
        sig_name = "SRSdevelpsignalgroupTXFunctiondevpsignalgroup5"
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

    class SRSdevelpsignalgroupTXFunctiondevpsignalgroup7:
        sig_name = "SRSdevelpsignalgroupTXFunctiondevpsignalgroup7"
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

    class SRSdevelpsignalgroupTXFunctiondevpsignalgroup3:
        sig_name = "SRSdevelpsignalgroupTXFunctiondevpsignalgroup3"
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


class MgmToVgmJ1979OBDPropDiagResFrame11:
    msg_name = "MgmToVgmJ1979OBDPropDiagResFrame11"
    msg_id = 2028
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "MGM"
    rx_nodes = ['BGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class SrsPropFr02:
    msg_name = "SrsPropFr02"
    msg_id = 53
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.2
    msg_length = 8
    tx_node = "SRS"
    rx_nodes = ['MGM', 'BECM1', 'IEM', 'ECM']
    sig_group_dict = {'CrashStsSafe': ['CrashStsSafeChks', 'CrashStsSafeCntr', 'CrashStsSafeSts']}
    sig_group_dataid_dict = {'CrashStsSafe': 1035}

    class CrashStsSafeChks:
        sig_name = "CrashStsSafeChks"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CrashStsSafeCntr:
        sig_name = "CrashStsSafeCntr"
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

    class CrashStsSafeSts:
        sig_name = "CrashStsSafeSts"
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
        sig_value_table = {'CrashSts2_NoCrash': 0, 'CrashSts2_Crash': 1}
        compute_method = None
        length = 1
        startbit = 4
        byte = 0
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class CrashStsSafe_UB:
        sig_name = "CrashStsSafe_UB"
        sig_start_bit = 5
        update_id_bit = 5
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
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5


class VddmPropFr19:
    msg_name = "VddmPropFr19"
    msg_id = 645
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.2
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['MGM', 'BECM1', 'EGSM', 'IEM', 'HVCM', 'ECM']
    sig_group_dict = {'VehBattU_0_CEMBackBoneSignalIpdu06': ['VehBattUSysU_0_CEMBackBoneSignalIpdu06', 'VehBattUSysUQf_0_CEMBackBoneSignalIpdu06'], 'AmbTRaw': ['AmbTRawAmbTVal', 'AmbTRawQly']}
    sig_group_dataid_dict = {}

    class VehBattUSysUQf_0_CEMBackBoneSignalIpdu06:
        sig_name = "VehBattUSysUQf_0_CEMBackBoneSignalIpdu06"
        sig_start_bit = 1
        update_id_bit = None
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
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class BkpOfDstTrvld_0_DIMBackBoneSignalIPdu04:
        sig_name = "BkpOfDstTrvld_0_DIMBackBoneSignalIPdu04"
        sig_start_bit = 20
        update_id_bit = 21
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
        startbit = 20
        bmuws_info = [(2, 0b00011111, 0b11100000, 5, 0), (3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111111, 0b00000000, 8, 0)]

    class AbsClrRdyReq:
        sig_name = "AbsClrRdyReq"
        sig_start_bit = 3
        update_id_bit = 4
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

    class VehBattU_0_CEMBackBoneSignalIpdu06_UB:
        sig_name = "VehBattU_0_CEMBackBoneSignalIpdu06_UB"
        sig_start_bit = 2
        update_id_bit = 2
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
        startbit = 2
        byte = 0
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VehBattUSysU_0_CEMBackBoneSignalIpdu06:
        sig_name = "VehBattUSysU_0_CEMBackBoneSignalIpdu06"
        sig_start_bit = 15
        update_id_bit = None
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class AmbTRawAmbTVal:
        sig_name = "AmbTRawAmbTVal"
        sig_start_bit = 42
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -70.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 700
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 42
        bmuws_info = [(5, 0b00000111, 0b11111000, 3, 0), (6, 0b11111111, 0b00000000, 8, 0)]

    class AmbTRawQly:
        sig_name = "AmbTRawQly"
        sig_start_bit = 44
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
        startbit = 44
        byte = 5
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class AmbTRaw_UB:
        sig_name = "AmbTRaw_UB"
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


class BecmPropFr09:
    msg_name = "BecmPropFr09"
    msg_id = 789
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.8
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['VDDM', 'ECM']
    sig_group_dict = {'HvBattT': ['HvBattTAvg', 'HvBattTMax', 'HvBattTMin']}
    sig_group_dataid_dict = {}

    class HvBattChrgnSts:
        sig_name = "HvBattChrgnSts"
        sig_start_bit = 56
        update_id_bit = 57
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ClimaSts_Start': 0, 'ClimaSts_Finish': 1}
        compute_method = None
        length = 1
        startbit = 56
        byte = 7
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class HvBattTAvg:
        sig_name = "HvBattTAvg"
        sig_start_bit = 6
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = -2560
        sig_value_max = 2559
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 6
        bmuws_info = [(0, 0b01111111, 0b10000000, 7, 0), (1, 0b11111100, 0b00000011, 6, 2)]

    class HvBattTMax:
        sig_name = "HvBattTMax"
        sig_start_bit = 9
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = -2560
        sig_value_max = 2559
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 9
        bmuws_info = [(1, 0b00000011, 0b11111100, 2, 0), (2, 0b11111111, 0b00000000, 8, 0), (3, 0b11100000, 0b00011111, 3, 5)]

    class HvBattT_UB:
        sig_name = "HvBattT_UB"
        sig_start_bit = 7
        update_id_bit = 7
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
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class HvBattTMin:
        sig_name = "HvBattTMin"
        sig_start_bit = 28
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = -2560
        sig_value_max = 2559
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 28
        bmuws_info = [(3, 0b00011111, 0b11100000, 5, 0), (4, 0b11111111, 0b00000000, 8, 0)]


class IemPropFr12:
    msg_name = "IemPropFr12"
    msg_id = 393
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.04
    msg_length = 8
    tx_node = "IEM"
    rx_nodes = ['ECM', 'VDDM']
    sig_group_dict = {'WhlMotSysSpdActSafe_0_IemPropSignalIPdu12': ['WhlMotSysSpdActSafeChks_0_IemPropSignalIPdu12', 'WhlMotSysSpdActSafeCntr_0_IemPropSignalIPdu12', 'WhlMotSysSpdActSafeIsgSpdWSgnTyp_0_IemPropSignalIPdu12', 'WhlMotSysSpdActSafeQf_0_IemPropSignalIPdu12']}
    sig_group_dataid_dict = {'WhlMotSysSpdActSafe_0_IemPropSignalIPdu12': 7001}

    class WhlMotSysSpdActSafeIsgSpdWSgnTyp_0_IemPropSignalIPdu12:
        sig_name = "WhlMotSysSpdActSafeIsgSpdWSgnTyp_0_IemPropSignalIPdu12"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = -16384
        sig_value_max = 16383
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111110, 0b00000001, 7, 1)]

    class WhlMotSysSpdActSafeCntr_0_IemPropSignalIPdu12:
        sig_name = "WhlMotSysSpdActSafeCntr_0_IemPropSignalIPdu12"
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

    class WhlMotSysSpdActSafeChks_0_IemPropSignalIPdu12:
        sig_name = "WhlMotSysSpdActSafeChks_0_IemPropSignalIPdu12"
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

    class WhlMotSysSpdActSafe_0_IemPropSignalIPdu12_UB:
        sig_name = "WhlMotSysSpdActSafe_0_IemPropSignalIPdu12_UB"
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

    class WhlMotSysSpdActSafeQf_0_IemPropSignalIPdu12:
        sig_name = "WhlMotSysSpdActSafeQf_0_IemPropSignalIPdu12"
        sig_start_bit = 5
        update_id_bit = None
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
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4


class VddmPropFr21:
    msg_name = "VddmPropFr21"
    msg_id = 296
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.025
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']
    sig_group_dict = {'EpbSts': ['EpbStsChks', 'EpbStsCntr', 'EpbStsEpbSts']}
    sig_group_dataid_dict = {'EpbSts': 132}

    class EpbStsCntr:
        sig_name = "EpbStsCntr"
        sig_start_bit = 11
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
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class EpbStsChks:
        sig_name = "EpbStsChks"
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

    class EpbSts_UB:
        sig_name = "EpbSts_UB"
        sig_start_bit = 23
        update_id_bit = 23
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
        startbit = 23
        byte = 2
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class EpbStsEpbSts:
        sig_name = "EpbStsEpbSts"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EpbSts_Resd0': 0, 'EpbSts_Resd1': 1, 'EpbSts_Resd2': 2, 'EpbSts_AllAppld': 3, 'EpbSts_Resd4': 4, 'EpbSts_AllInTran': 5, 'EpbSts_BrkgDynByActr': 6, 'EpbSts_Resd7': 7, 'EpbSts_Resd8': 8, 'EpbSts_ActrAllReld': 9, 'EpbSts_BrkgDynDegraded': 10, 'EpbSts_Resd11': 11, 'EpbSts_BrkgDyn': 12, 'EpbSts_Resd13': 13, 'EpbSts_Resd14': 14, 'EpbSts_Err': 15}
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4


class IgmMgmPropFr04:
    msg_name = "IgmMgmPropFr04"
    msg_id = 512
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.08
    msg_length = 8
    tx_node = "MGM"
    rx_nodes = ['VDDM']
    sig_group_dict = {'ImobEngChk3': ['ImobEngChk3ImobEngChkSts', 'ImobEngChk3ImobEngDataChk0', 'ImobEngChk3ImobEngDataChk1', 'ImobEngChk3ImobEngDataChk2', 'ImobEngChk3ImobEngDataChk3', 'ImobEngChk3ImobEngDataChk4', 'ImobEngChk3ImobEngDataChk5', 'ImobEngChk3ImobEngDataChk6']}
    sig_group_dataid_dict = {}

    class ImobEngChk3_UB:
        sig_name = "ImobEngChk3_UB"
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

    class ImobEngChk3ImobEngDataChk4:
        sig_name = "ImobEngChk3ImobEngDataChk4"
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

    class ImobEngChk3ImobEngDataChk5:
        sig_name = "ImobEngChk3ImobEngDataChk5"
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

    class ImobEngChk3ImobEngDataChk6:
        sig_name = "ImobEngChk3ImobEngDataChk6"
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

    class ImobEngChk3ImobEngDataChk1:
        sig_name = "ImobEngChk3ImobEngDataChk1"
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

    class ImobEngChk3ImobEngChkSts:
        sig_name = "ImobEngChk3ImobEngChkSts"
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
        sig_value_table = {'AvlSts2_NotAvl': 0, 'AvlSts2_Avl': 1}
        compute_method = None
        length = 1
        startbit = 0
        byte = 0
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ImobEngChk3ImobEngDataChk2:
        sig_name = "ImobEngChk3ImobEngDataChk2"
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

    class ImobEngChk3ImobEngDataChk0:
        sig_name = "ImobEngChk3ImobEngDataChk0"
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

    class ImobEngSts3:
        sig_name = "ImobEngSts3"
        sig_start_bit = 3
        update_id_bit = 4
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ImobSts_ImobUndefd': 0, 'ImobSts_ImobImobn': 1, 'ImobSts_ImobMtn': 2, 'ImobSts_ImobNoMtn': 3}
        compute_method = None
        length = 2
        startbit = 3
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class ImobEngChk3ImobEngDataChk3:
        sig_name = "ImobEngChk3ImobEngDataChk3"
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


class VddmPropFr02:
    msg_name = "VddmPropFr02"
    msg_id = 98
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.015
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']
    sig_group_dict = {'BrkTq': ['BrkTqChks', 'BrkTqCntr', 'BrkTqQf', 'BrkTqRgnAtAxleReReq', 'BrkTqSts', 'BrkTqTotReqForPt']}
    sig_group_dataid_dict = {'BrkTq': 1201}

    class BrkTqQf:
        sig_name = "BrkTqQf"
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
        sig_value_table = {'Qf1_DevOfDataUndefd': 0, 'Qf1_DataTmpUndefdAndEvlnInProgs': 1, 'Qf1_DevOfDataNotWithinRngAllwd': 2, 'Qf1_DataCalcdWithDevDefd': 3}
        compute_method = None
        length = 2
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class BrkTq_UB:
        sig_name = "BrkTq_UB"
        sig_start_bit = 6
        update_id_bit = 6
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
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class BrkTqCntr:
        sig_name = "BrkTqCntr"
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

    class ChrgHndlStrtEna:
        sig_name = "ChrgHndlStrtEna"
        sig_start_bit = 51
        update_id_bit = 50
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ChrgHndlStrtEna_PwrUpNotEna': 0, 'ChrgHndlStrtEna_PwrUpEna': 1}
        compute_method = None
        length = 1
        startbit = 51
        byte = 6
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class BrkTqRgnAtAxleReReq:
        sig_name = "BrkTqRgnAtAxleReReq"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = -16384
        sig_value_max = 16380
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111110, 0b00000001, 7, 1)]

    class BrkTqSts:
        sig_name = "BrkTqSts"
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
        sig_value_table = {'BrkSts_NoBrake': 0, 'BrkSts_Brake': 1}
        compute_method = None
        length = 1
        startbit = 24
        byte = 3
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class BrkTqTotReqForPt:
        sig_name = "BrkTqTotReqForPt"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = -16384
        sig_value_max = 16380
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111110, 0b00000001, 7, 1)]

    class BrkTqChks:
        sig_name = "BrkTqChks"
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

    class RoadSgnInfoSts:
        sig_name = "RoadSgnInfoSts"
        sig_start_bit = 54
        update_id_bit = 55
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TrfcSgnInfoSts_TSIUnknown': 0, 'TrfcSgnInfoSts_TSIOff': 1, 'TrfcSgnInfoSts_TSIOn_fusion': 2, 'TrfcSgnInfoSts_TSIOn_visiononlymode': 3, 'TrfcSgnInfoSts_TSIOn_navigationonlymode': 4, 'TrfcSgnInfoSts_TSIUnavailable': 5, 'TrfcSgnInfoSts_TSIServicerequired': 6, 'TrfcSgnInfoSts_Reserved': 7}
        compute_method = None
        length = 3
        startbit = 54
        byte = 6
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4


class SrsToVgmISO26021PropDiagResFrame11:
    msg_name = "SrsToVgmISO26021PropDiagResFrame11"
    msg_id = 2041
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "SRS"
    rx_nodes = ['BGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class BecmPropFr05:
    msg_name = "BecmPropFr05"
    msg_id = 661
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.6
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['VDDM', 'ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HVIL2Sts:
        sig_name = "HVIL2Sts"
        sig_start_bit = 35
        update_id_bit = 34
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OpenClose_Open': 0, 'OpenClose_Close': 1}
        compute_method = None
        length = 1
        startbit = 35
        byte = 4
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class HvBattCoolgSts:
        sig_name = "HvBattCoolgSts"
        sig_start_bit = 36
        update_id_bit = 37
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ClimaSts_Start': 0, 'ClimaSts_Finish': 1}
        compute_method = None
        length = 1
        startbit = 36
        byte = 4
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class HVIL3Sts:
        sig_name = "HVIL3Sts"
        sig_start_bit = 33
        update_id_bit = 32
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OpenClose_Open': 0, 'OpenClose_Close': 1}
        compute_method = None
        length = 1
        startbit = 33
        byte = 4
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class HvSysCrashFb:
        sig_name = "HvSysCrashFb"
        sig_start_bit = 54
        update_id_bit = 55
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CrashFb_Idle': 0, 'CrashFb_Evln': 1, 'CrashFb_Nok': 2, 'CrashFb_Ok': 3}
        compute_method = None
        length = 2
        startbit = 54
        byte = 6
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class HvBattPVal:
        sig_name = "HvBattPVal"
        sig_start_bit = 7
        update_id_bit = 10
        sig_length = 13
        sig_value_factor = 0.05
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 1000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111000, 0b00000111, 5, 3)]

    class HVIL1Sts:
        sig_name = "HVIL1Sts"
        sig_start_bit = 39
        update_id_bit = 38
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OpenClose_Open': 0, 'OpenClose_Close': 1}
        compute_method = None
        length = 1
        startbit = 39
        byte = 4
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class HvIsoSts:
        sig_name = "HvIsoSts"
        sig_start_bit = 52
        update_id_bit = 50
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Insulation_Default': 0, 'Insulation_Error_Battery_before_HV_Ready': 1, 'Insulation_Error_HV_bus_after_HV_Ready': 2, 'Insulation_OK': 3}
        compute_method = None
        length = 2
        startbit = 52
        byte = 6
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3


class EcmPropXEVFr16:
    msg_name = "EcmPropXEVFr16"
    msg_id = 649
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['BECM1']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HvBattChrgnILim:
        sig_name = "HvBattChrgnILim"
        sig_start_bit = 36
        update_id_bit = 55
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 36
        bmuws_info = [(4, 0b00011111, 0b11100000, 5, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class HvBattChrgnEgyCnsAllwd1:
        sig_name = "HvBattChrgnEgyCnsAllwd1"
        sig_start_bit = 52
        update_id_bit = 53
        sig_length = 13
        sig_value_factor = 20.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 52
        bmuws_info = [(6, 0b00011111, 0b11100000, 5, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class HvBattCoolgEgyCnsAllwd1:
        sig_name = "HvBattCoolgEgyCnsAllwd1"
        sig_start_bit = 17
        update_id_bit = 54
        sig_length = 10
        sig_value_factor = 20.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 17
        bmuws_info = [(2, 0b00000011, 0b11111100, 2, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class RadFanCoolgSts:
        sig_name = "RadFanCoolgSts"
        sig_start_bit = 39
        update_id_bit = 8
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
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5


class IgmMgmPropFr06:
    msg_name = "IgmMgmPropFr06"
    msg_id = 149
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "MGM"
    rx_nodes = ['BECM1', 'ECM', 'VDDM']
    sig_group_dict = {'IsgTqAct': ['IsgTqActChks', 'IsgTqActCntr', 'IsgTqActIsgTqAct', 'IsgTqActQualityFactor']}
    sig_group_dataid_dict = {'IsgTqAct': 70}

    class IsgTqActChks:
        sig_name = "IsgTqActChks"
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

    class IsgTqActQualityFactor:
        sig_name = "IsgTqActQualityFactor"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'QualityFactor_QfUndefd': 0, 'QualityFactor_QfInProgs': 1, 'QualityFactor_QfNotSpc': 2, 'QualityFactor_QfSnsrDataOk': 3}
        compute_method = None
        length = 2
        startbit = 23
        byte = 2
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class IsgCluSts:
        sig_name = "IsgCluSts"
        sig_start_bit = 47
        update_id_bit = 5
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CluStsIndcn_Open': 0, 'CluStsIndcn_Close': 1, 'CluStsIndcn_StuckOpen': 2, 'CluStsIndcn_StuckClose': 3, 'CluStsIndcn_Undefined': 4, 'CluStsIndcn_Ongoing': 5, 'CluStsIndcn_Reserved1': 6, 'CluStsIndcn_Reserved2': 7}
        compute_method = None
        length = 3
        startbit = 47
        byte = 5
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class IsgTqAct_UB:
        sig_name = "IsgTqAct_UB"
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

    class IsgModSts:
        sig_name = "IsgModSts"
        sig_start_bit = 38
        update_id_bit = 39
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 9
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'IsgModTyp2_Inin': 0, 'IsgModTyp2_Stb': 1, 'IsgModTyp2_TqCtrl': 2, 'IsgModTyp2_SpdCtrl': 3, 'IsgModTyp2_UDcCtrl': 4, 'IsgModTyp2_PreChrg': 5, 'IsgModTyp2_PwrDwn': 6, 'IsgModTyp2_Flt': 7, 'IsgModTyp2_TcsCtrl': 8, 'IsgModTyp2_CluOpe': 9}
        compute_method = None
        length = 4
        startbit = 38
        byte = 4
        mask = 0b01111000
        unmask = 0b10000111
        shift = 3

    class IsgTqActCntr:
        sig_name = "IsgTqActCntr"
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

    class BegCluReq:
        sig_name = "BegCluReq"
        sig_start_bit = 34
        update_id_bit = 32
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BegCluReq_Default': 0, 'BegCluReq_BegForCluReqClose': 1, 'BegCluReq_BegForCluReqOpen': 2, 'BegCluReq_Reserve': 3}
        compute_method = None
        length = 2
        startbit = 34
        byte = 4
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class IsgTqActIsgTqAct:
        sig_name = "IsgTqActIsgTqAct"
        sig_start_bit = 21
        update_id_bit = None
        sig_length = 14
        sig_value_factor = 1.0
        sig_value_offset = -8188.0
        sig_value_min = 0
        sig_value_max = 16380
        sig_byteorder = "Motorola"
        sig_value_init = 8188
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 14
        startbit = 21
        bmuws_info = [(2, 0b00111111, 0b11000000, 6, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class IsgSpdActSgn:
        sig_name = "IsgSpdActSgn"
        sig_start_bit = 54
        update_id_bit = 55
        sig_length = 15
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = -16384
        sig_value_max = 16383
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 54
        bmuws_info = [(6, 0b01111111, 0b10000000, 7, 0), (7, 0b11111111, 0b00000000, 8, 0)]


class EcmPropFr02:
    msg_name = "EcmPropFr02"
    msg_id = 102
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.015
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['IEM', 'VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class WhlMotSysModReq:
        sig_name = "WhlMotSysModReq"
        sig_start_bit = 58
        update_id_bit = 59
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WhlMotSysModStsTyp1_Inin': 0, 'WhlMotSysModStsTyp1_Stb': 1, 'WhlMotSysModStsTyp1_TqCtrl': 2, 'WhlMotSysModStsTyp1_SpdCtrlIdle': 3, 'WhlMotSysModStsTyp1_CluOper': 4, 'WhlMotSysModStsTyp1_PreChrg': 5, 'WhlMotSysModStsTyp1_PwrDwn': 6, 'WhlMotSysModStsTyp1_Flt': 7}
        compute_method = None
        length = 3
        startbit = 58
        byte = 7
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0


class IemEduPropFr01:
    msg_name = "IemEduPropFr01"
    msg_id = 76
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "IEM"
    rx_nodes = ['BECM1', 'ECM', 'VDDM']
    sig_group_dict = {'WhlMotSysTqAvl': ['WhlMotSysTqAvlTqAvlMax', 'WhlMotSysTqAvlTqAvlMin'], 'WhlMotSysTqEst': ['WhlMotSysTqEstChks', 'WhlMotSysTqEstCntr', 'WhlMotSysTqEstIsgTqAct', 'WhlMotSysTqEstQualityFactor']}
    sig_group_dataid_dict = {'WhlMotSysTqEst': 69}

    class WhlMotSysTqEstChks:
        sig_name = "WhlMotSysTqEstChks"
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

    class WhlMotSysTqEstCntr:
        sig_name = "WhlMotSysTqEstCntr"
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

    class WhlMotSysModSts:
        sig_name = "WhlMotSysModSts"
        sig_start_bit = 35
        update_id_bit = 36
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 8
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WhlMotSysModStsTyp2_Inin': 0, 'WhlMotSysModStsTyp2_Stb': 1, 'WhlMotSysModStsTyp2_TqCtrl': 2, 'WhlMotSysModStsTyp2_SpdCtrlIdle': 3, 'WhlMotSysModStsTyp2_CluOper': 4, 'WhlMotSysModStsTyp2_PreChrg': 5, 'WhlMotSysModStsTyp2_PwrDwn': 6, 'WhlMotSysModStsTyp2_Flt': 7, 'WhlMotSysModStsTyp2_TcsCtrl': 8}
        compute_method = None
        length = 4
        startbit = 35
        byte = 4
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class WhlMotSysTqAvlTqAvlMax:
        sig_name = "WhlMotSysTqAvlTqAvlMax"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 4.0
        sig_value_offset = -8188.0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 2047
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11110000, 0b00001111, 4, 4)]

    class WhlMotSysTqEstIsgTqAct:
        sig_name = "WhlMotSysTqEstIsgTqAct"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 14
        sig_value_factor = 1.0
        sig_value_offset = -8188.0
        sig_value_min = 0
        sig_value_max = 16380
        sig_byteorder = "Motorola"
        sig_value_init = 8188
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 14
        startbit = 15
        bmuws_info = [(1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111100, 0b00000011, 6, 2)]

    class WhlMotSysTqEstQualityFactor:
        sig_name = "WhlMotSysTqEstQualityFactor"
        sig_start_bit = 17
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'QualityFactor_QfUndefd': 0, 'QualityFactor_QfInProgs': 1, 'QualityFactor_QfNotSpc': 2, 'QualityFactor_QfSnsrDataOk': 3}
        compute_method = None
        length = 2
        startbit = 17
        byte = 2
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class WhlMotSysTqAvlTqAvlMin:
        sig_name = "WhlMotSysTqAvlTqAvlMin"
        sig_start_bit = 51
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 4.0
        sig_value_offset = -8188.0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 2047
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 51
        bmuws_info = [(6, 0b00001111, 0b11110000, 4, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class WhlMotSysTqAvl_UB:
        sig_name = "WhlMotSysTqAvl_UB"
        sig_start_bit = 37
        update_id_bit = 37
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
        startbit = 37
        byte = 4
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class WhlMotSysTqEst_UB:
        sig_name = "WhlMotSysTqEst_UB"
        sig_start_bit = 27
        update_id_bit = 27
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
        startbit = 27
        byte = 3
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3


class EcmPropXevFr06:
    msg_name = "EcmPropXevFr06"
    msg_id = 328
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.025
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['MGM', 'IEM']
    sig_group_dict = {'IsgTqAllwd': ['IsgTqAllwdChks', 'IsgTqAllwdCntr', 'IsgTqAllwdIsgTqAllwd']}
    sig_group_dataid_dict = {'IsgTqAllwd': 80}

    class IsgTqAllwdChks:
        sig_name = "IsgTqAllwdChks"
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

    class WhlMotSysPwrLimMin:
        sig_name = "WhlMotSysPwrLimMin"
        sig_start_bit = 23
        update_id_bit = 29
        sig_length = 10
        sig_value_factor = 0.5
        sig_value_offset = -511.0
        sig_value_min = 0
        sig_value_max = 1022
        sig_byteorder = "Motorola"
        sig_value_init = 1022
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11000000, 0b00111111, 2, 6)]

    class WhlMotSysActvDampgModReq:
        sig_name = "WhlMotSysActvDampgModReq"
        sig_start_bit = 50
        update_id_bit = 48
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WhlMotSysActvDampgModCodSts_NoDampg': 0, 'WhlMotSysActvDampgModCodSts_LoDampg': 1, 'WhlMotSysActvDampgModCodSts_MedDampg': 2, 'WhlMotSysActvDampgModCodSts_HiDampg': 3}
        compute_method = None
        length = 2
        startbit = 50
        byte = 6
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class IsgTqAllwdCntr:
        sig_name = "IsgTqAllwdCntr"
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

    class IsgTqAllwd_UB:
        sig_name = "IsgTqAllwd_UB"
        sig_start_bit = 54
        update_id_bit = 54
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
        startbit = 54
        byte = 6
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class IsgTqAllwdIsgTqAllwd:
        sig_name = "IsgTqAllwdIsgTqAllwd"
        sig_start_bit = 43
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
        startbit = 43
        byte = 5
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0


class EcmPropFr28:
    msg_name = "EcmPropFr28"
    msg_id = 401
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.07
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['MGM', 'IEM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class FrntHeatPwrAllwd:
        sig_name = "FrntHeatPwrAllwd"
        sig_start_bit = 7
        update_id_bit = 13
        sig_length = 8
        sig_value_factor = 50.0
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

    class FrntHeatModEnad:
        sig_name = "FrntHeatModEnad"
        sig_start_bit = 9
        update_id_bit = 12
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FrntHeatModEnad_Heatg': 0, 'FrntHeatModEnad_PwrLoss': 1, 'FrntHeatModEnad_Off': 2, 'FrntHeatModEnad_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 9
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class RearHeatPwrAllwd:
        sig_name = "RearHeatPwrAllwd"
        sig_start_bit = 23
        update_id_bit = 15
        sig_length = 8
        sig_value_factor = 50.0
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

    class RearHeatModEnad:
        sig_name = "RearHeatModEnad"
        sig_start_bit = 11
        update_id_bit = 14
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FrntHeatModEnad_Heatg': 0, 'FrntHeatModEnad_PwrLoss': 1, 'FrntHeatModEnad_Off': 2, 'FrntHeatModEnad_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 11
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2


class VddmPropFr35:
    msg_name = "VddmPropFr35"
    msg_id = 304
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.015
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['MGM']
    sig_group_dict = {'WhlDirRotlFrnt_3_AcuFLRCANFDSignalIPdu01': ['WhlDirRotlFrntChks_3_AcuFLRCANFDSignalIPdu01', 'WhlDirRotlFrntCntr_3_AcuFLRCANFDSignalIPdu01', 'WhlDirRotlFrntLe_3_AcuFLRCANFDSignalIPdu01', 'WhlDirRotlFrntRi_3_AcuFLRCANFDSignalIPdu01'], 'SpdRotlForWhlsAtAxleFrnt': ['SpdRotlForWhlsAtAxleFrntChks', 'SpdRotlForWhlsAtAxleFrntCntr', 'SpdRotlForWhlsAtAxleFrntSpdRotlForWhlsAtAxleFrnt']}
    sig_group_dataid_dict = {'WhlDirRotlFrnt_3_AcuFLRCANFDSignalIPdu01': 552, 'SpdRotlForWhlsAtAxleFrnt': 53}

    class WhlDirRotlFrntCntr_3_AcuFLRCANFDSignalIPdu01:
        sig_name = "WhlDirRotlFrntCntr_3_AcuFLRCANFDSignalIPdu01"
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

    class SpdRotlForWhlsAtAxleFrntCntr:
        sig_name = "SpdRotlForWhlsAtAxleFrntCntr"
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

    class SpdRotlForWhlsAtAxleFrntSpdRotlForWhlsAtAxleFrnt:
        sig_name = "SpdRotlForWhlsAtAxleFrntSpdRotlForWhlsAtAxleFrnt"
        sig_start_bit = 6
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 0.5
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 32767
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 6
        bmuws_info = [(0, 0b01111111, 0b10000000, 7, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class WhlDirRotlFrntLe_3_AcuFLRCANFDSignalIPdu01:
        sig_name = "WhlDirRotlFrntLe_3_AcuFLRCANFDSignalIPdu01"
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
        sig_value_table = {'WhlRotlDirStd1_Undefd': 0, 'WhlRotlDirStd1_StandStill': 1, 'WhlRotlDirStd1_Fwd': 2, 'WhlRotlDirStd1_Backw': 3}
        compute_method = None
        length = 2
        startbit = 43
        byte = 5
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class WhlDirRotlFrntRi_3_AcuFLRCANFDSignalIPdu01:
        sig_name = "WhlDirRotlFrntRi_3_AcuFLRCANFDSignalIPdu01"
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
        sig_value_table = {'WhlRotlDirStd1_Undefd': 0, 'WhlRotlDirStd1_StandStill': 1, 'WhlRotlDirStd1_Fwd': 2, 'WhlRotlDirStd1_Backw': 3}
        compute_method = None
        length = 2
        startbit = 41
        byte = 5
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class WhlDirRotlFrntChks_3_AcuFLRCANFDSignalIPdu01:
        sig_name = "WhlDirRotlFrntChks_3_AcuFLRCANFDSignalIPdu01"
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

    class WhlDirRotlFrnt_3_AcuFLRCANFDSignalIPdu01_UB:
        sig_name = "WhlDirRotlFrnt_3_AcuFLRCANFDSignalIPdu01_UB"
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

    class SpdRotlForWhlsAtAxleFrnt_UB:
        sig_name = "SpdRotlForWhlsAtAxleFrnt_UB"
        sig_start_bit = 7
        update_id_bit = 7
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
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class SpdRotlForWhlsAtAxleFrntChks:
        sig_name = "SpdRotlForWhlsAtAxleFrntChks"
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


class VddmBcmPropdTCFr01:
    msg_name = "VddmBcmPropdTCFr01"
    msg_id = 302
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['MGM', 'IEM']
    sig_group_dict = {'EscVariantToDmc': ['EscVariantToDmcChks', 'EscVariantToDmcCntr', 'EscVariantToDmcEscVariantToDmc']}
    sig_group_dataid_dict = {'EscVariantToDmc': 6564}

    class EscVariantToDmcChks:
        sig_name = "EscVariantToDmcChks"
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

    class EscVariantToDmcCntr:
        sig_name = "EscVariantToDmcCntr"
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

    class EscVariantToDmcEscVariantToDmc:
        sig_name = "EscVariantToDmcEscVariantToDmc"
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

    class EscVariantToDmc_UB:
        sig_name = "EscVariantToDmc_UB"
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


class MgmPropFr06:
    msg_name = "MgmPropFr06"
    msg_id = 384
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.04
    msg_length = 8
    tx_node = "MGM"
    rx_nodes = ['ECM']
    sig_group_dict = {'IsgSpdActSgnSafe_0_MgmPropSignalIPdu06': ['IsgSpdActSgnSafeChks_0_MgmPropSignalIPdu06', 'IsgSpdActSgnSafeCntr_0_MgmPropSignalIPdu06', 'IsgSpdActSgnSafeIsgSpdWSgnTyp_0_MgmPropSignalIPdu06', 'IsgSpdActSgnSafeQf_0_MgmPropSignalIPdu06']}
    sig_group_dataid_dict = {'IsgSpdActSgnSafe_0_MgmPropSignalIPdu06': 7003}

    class IsgSpdActSgnSafe_0_MgmPropSignalIPdu06_UB:
        sig_name = "IsgSpdActSgnSafe_0_MgmPropSignalIPdu06_UB"
        sig_start_bit = 6
        update_id_bit = 6
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
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class IsgSpdActSgnSafeChks_0_MgmPropSignalIPdu06:
        sig_name = "IsgSpdActSgnSafeChks_0_MgmPropSignalIPdu06"
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

    class IsgSpdActSgnSafeQf_0_MgmPropSignalIPdu06:
        sig_name = "IsgSpdActSgnSafeQf_0_MgmPropSignalIPdu06"
        sig_start_bit = 5
        update_id_bit = None
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
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class IsgSpdActSgnSafeCntr_0_MgmPropSignalIPdu06:
        sig_name = "IsgSpdActSgnSafeCntr_0_MgmPropSignalIPdu06"
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

    class IsgSpdActSgnSafeIsgSpdWSgnTyp_0_MgmPropSignalIPdu06:
        sig_name = "IsgSpdActSgnSafeIsgSpdWSgnTyp_0_MgmPropSignalIPdu06"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = -16384
        sig_value_max = 16383
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111110, 0b00000001, 7, 1)]


class VgmToBecmJ1979OBDPropCanReqFrame11:
    msg_name = "VgmToBecmJ1979OBDPropCanReqFrame11"
    msg_id = 2018
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['BECM1']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class BecmPropFr18:
    msg_name = "BecmPropFr18"
    msg_id = 838
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 1.0
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['VDDM', 'ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HvBattCooltOutletT:
        sig_name = "HvBattCooltOutletT"
        sig_start_bit = 7
        update_id_bit = 12
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -60.0
        sig_value_min = 0
        sig_value_max = 1850
        sig_byteorder = "Motorola"
        sig_value_init = 600
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11100000, 0b00011111, 3, 5)]

    class HvBattVoltMaxSerlNr:
        sig_name = "HvBattVoltMaxSerlNr"
        sig_start_bit = 23
        update_id_bit = 39
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 23
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvBattHeatgPwr:
        sig_name = "HvBattHeatgPwr"
        sig_start_bit = 47
        update_id_bit = 35
        sig_length = 11
        sig_value_factor = 100.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11100000, 0b00011111, 3, 5)]

    class HvBattCooltLvl:
        sig_name = "HvBattCooltLvl"
        sig_start_bit = 36
        update_id_bit = 37
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvBattCooltLvl_Full': 0, 'HvBattCooltLvl_Empty': 1}
        compute_method = None
        length = 1
        startbit = 36
        byte = 4
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class HvBattVoltMinSerlNr:
        sig_name = "HvBattVoltMinSerlNr"
        sig_start_bit = 31
        update_id_bit = 38
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class VddmPropFr06:
    msg_name = "VddmPropFr06"
    msg_id = 565
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['MGM', 'BECM1', 'EGSM', 'IEM', 'HVCM']
    sig_group_dict = {'VehCfgPrm_0_CEMBackBoneSignalIpdu06': ['VehCfgPrmBlkIDBytePosn1_0_CEMBackBoneSignalIpdu06', 'VehCfgPrmCCPBytePosn2_0_CEMBackBoneSignalIpdu06', 'VehCfgPrmCCPBytePosn3_0_CEMBackBoneSignalIpdu06', 'VehCfgPrmCCPBytePosn4_0_CEMBackBoneSignalIpdu06', 'VehCfgPrmCCPBytePosn5_0_CEMBackBoneSignalIpdu06', 'VehCfgPrmCCPBytePosn6_0_CEMBackBoneSignalIpdu06', 'VehCfgPrmCCPBytePosn7_0_CEMBackBoneSignalIpdu06', 'VehCfgPrmCCPBytePosn8_0_CEMBackBoneSignalIpdu06']}
    sig_group_dataid_dict = {}

    class VehCfgPrmCCPBytePosn4_0_CEMBackBoneSignalIpdu06:
        sig_name = "VehCfgPrmCCPBytePosn4_0_CEMBackBoneSignalIpdu06"
        sig_start_bit = 31
        update_id_bit = None
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

    class VehCfgPrmCCPBytePosn2_0_CEMBackBoneSignalIpdu06:
        sig_name = "VehCfgPrmCCPBytePosn2_0_CEMBackBoneSignalIpdu06"
        sig_start_bit = 15
        update_id_bit = None
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

    class VehCfgPrmCCPBytePosn5_0_CEMBackBoneSignalIpdu06:
        sig_name = "VehCfgPrmCCPBytePosn5_0_CEMBackBoneSignalIpdu06"
        sig_start_bit = 39
        update_id_bit = None
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

    class VehCfgPrmCCPBytePosn7_0_CEMBackBoneSignalIpdu06:
        sig_name = "VehCfgPrmCCPBytePosn7_0_CEMBackBoneSignalIpdu06"
        sig_start_bit = 55
        update_id_bit = None
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

    class VehCfgPrmBlkIDBytePosn1_0_CEMBackBoneSignalIpdu06:
        sig_name = "VehCfgPrmBlkIDBytePosn1_0_CEMBackBoneSignalIpdu06"
        sig_start_bit = 7
        update_id_bit = None
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

    class VehCfgPrmCCPBytePosn3_0_CEMBackBoneSignalIpdu06:
        sig_name = "VehCfgPrmCCPBytePosn3_0_CEMBackBoneSignalIpdu06"
        sig_start_bit = 23
        update_id_bit = None
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

    class VehCfgPrmCCPBytePosn6_0_CEMBackBoneSignalIpdu06:
        sig_name = "VehCfgPrmCCPBytePosn6_0_CEMBackBoneSignalIpdu06"
        sig_start_bit = 47
        update_id_bit = None
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

    class VehCfgPrmCCPBytePosn8_0_CEMBackBoneSignalIpdu06:
        sig_name = "VehCfgPrmCCPBytePosn8_0_CEMBackBoneSignalIpdu06"
        sig_start_bit = 63
        update_id_bit = None
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


class BecmPropFr33:
    msg_name = "BecmPropFr33"
    msg_id = 1026
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.3
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['S2SReceiver']
    sig_group_dict = {'RemoteBookStrtTiChrgnTmr': ['RemoteBookStrtTiChrgnTmrChrgnTmrhour', 'RemoteBookStrtTiChrgnTmrChrgnTmrmin'], 'RemoteBookStopTiChrgnTmr': ['RemoteBookStopTiChrgnTmrChrgnTmrhour', 'RemoteBookStopTiChrgnTmrChrgnTmrmin']}
    sig_group_dataid_dict = {}

    class RemoteBookStrtTiChrgnTmr_UB:
        sig_name = "RemoteBookStrtTiChrgnTmr_UB"
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

    class RemoteBookStrtTiChrgnTmrChrgnTmrhour:
        sig_name = "RemoteBookStrtTiChrgnTmrChrgnTmrhour"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 24
        sig_byteorder = "Motorola"
        sig_value_init = 24
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RemoteBookStrtTiChrgnTmrChrgnTmrmin:
        sig_name = "RemoteBookStrtTiChrgnTmrChrgnTmrmin"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 60
        sig_byteorder = "Motorola"
        sig_value_init = 60
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RemoteBookStopTiChrgnTmrChrgnTmrhour:
        sig_name = "RemoteBookStopTiChrgnTmrChrgnTmrhour"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 24
        sig_byteorder = "Motorola"
        sig_value_init = 24
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RemoteBookStopTiChrgnTmr_UB:
        sig_name = "RemoteBookStopTiChrgnTmr_UB"
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

    class RemoteBookStopTiChrgnTmrChrgnTmrmin:
        sig_name = "RemoteBookStopTiChrgnTmrChrgnTmrmin"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 60
        sig_byteorder = "Motorola"
        sig_value_init = 60
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class VddmPropdTCFr38:
    msg_name = "VddmPropdTCFr38"
    msg_id = 282
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['MGM', 'IEM']
    sig_group_dict = {'StcStsToDmc': ['StcStsToDmcChks', 'StcStsToDmcCntr', 'StcStsToDmcEngRotTarSpdDMCFrnt', 'StcStsToDmcEngRotTarSpdDMCRear', 'StcStsToDmcFrnt', 'StcStsToDmcRear']}
    sig_group_dataid_dict = {'StcStsToDmc': 6565}

    class StcStsToDmcEngRotTarSpdDMCFrnt:
        sig_name = "StcStsToDmcEngRotTarSpdDMCFrnt"
        sig_start_bit = 23
        update_id_bit = None
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

    class StcStsToDmcCntr:
        sig_name = "StcStsToDmcCntr"
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

    class StcStsToDmcFrnt:
        sig_name = "StcStsToDmcFrnt"
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
        sig_value_table = {'ModeDMC_Off': 0, 'ModeDMC_Rpm': 1, 'ModeDMC_Trq': 2}
        compute_method = None
        length = 8
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class StcStsToDmcEngRotTarSpdDMCRear:
        sig_name = "StcStsToDmcEngRotTarSpdDMCRear"
        sig_start_bit = 39
        update_id_bit = None
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
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class StcStsToDmcChks:
        sig_name = "StcStsToDmcChks"
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

    class StcStsToDmc_UB:
        sig_name = "StcStsToDmc_UB"
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

    class StcStsToDmcRear:
        sig_name = "StcStsToDmcRear"
        sig_start_bit = 63
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ModeDMC_Off': 0, 'ModeDMC_Rpm': 1, 'ModeDMC_Trq': 2}
        compute_method = None
        length = 8
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class MgmPropFr03:
    msg_name = "MgmPropFr03"
    msg_id = 640
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.12
    msg_length = 8
    tx_node = "MGM"
    rx_nodes = ['CCM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class CluDisConSucsCntr:
        sig_name = "CluDisConSucsCntr"
        sig_start_bit = 39
        update_id_bit = 61
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
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class CluDisConFailCntr:
        sig_name = "CluDisConFailCntr"
        sig_start_bit = 55
        update_id_bit = 62
        sig_length = 8
        sig_value_factor = None
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

    class CluConSucsCntr:
        sig_name = "CluConSucsCntr"
        sig_start_bit = 23
        update_id_bit = 63
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

    class CluConFailCntr:
        sig_name = "CluConFailCntr"
        sig_start_bit = 15
        update_id_bit = 0
        sig_length = 8
        sig_value_factor = None
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


class VddmToIemPropDiagReqFrame:
    msg_name = "VddmToIemPropDiagReqFrame"
    msg_id = 1847
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['IEM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class VddmPropFr18:
    msg_name = "VddmPropFr18"
    msg_id = 86
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.015
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['MGM', 'BECM1', 'EGSM', 'IEM', 'HVCM']
    sig_group_dict = {'VehModMngtGlbSafe1_0_CEMBackBoneSignalIpdu02': ['VehModMngtGlbSafe1CarModSts1_0_CEMBackBoneSignalIpdu02', 'VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp_0_CEMBackBoneSignalIpdu02', 'VehModMngtGlbSafe1Chks_0_CEMBackBoneSignalIpdu02', 'VehModMngtGlbSafe1Cntr_0_CEMBackBoneSignalIpdu02', 'VehModMngtGlbSafe1EgyLvlElecMai_0_CEMBackBoneSignalIpdu02', 'VehModMngtGlbSafe1EgyLvlElecSubtyp_0_CEMBackBoneSignalIpdu02', 'VehModMngtGlbSafe1FltEgyCnsWdSts_0_CEMBackBoneSignalIpdu02', 'VehModMngtGlbSafe1PwrLvlElecMai_0_CEMBackBoneSignalIpdu02', 'VehModMngtGlbSafe1PwrLvlElecSubtyp_0_CEMBackBoneSignalIpdu02', 'VehModMngtGlbSafe1UsgModSts_0_CEMBackBoneSignalIpdu02']}
    sig_group_dataid_dict = {'VehModMngtGlbSafe1_0_CEMBackBoneSignalIpdu02': 116}

    class VehModMngtGlbSafe1Chks_0_CEMBackBoneSignalIpdu02:
        sig_name = "VehModMngtGlbSafe1Chks_0_CEMBackBoneSignalIpdu02"
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

    class VehModMngtGlbSafe1EgyLvlElecSubtyp_0_CEMBackBoneSignalIpdu02:
        sig_name = "VehModMngtGlbSafe1EgyLvlElecSubtyp_0_CEMBackBoneSignalIpdu02"
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

    class VehModMngtGlbSafe1PwrLvlElecSubtyp_0_CEMBackBoneSignalIpdu02:
        sig_name = "VehModMngtGlbSafe1PwrLvlElecSubtyp_0_CEMBackBoneSignalIpdu02"
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

    class IntrBriSts_0_CEMBackBoneSignalIpdu03:
        sig_name = "IntrBriSts_0_CEMBackBoneSignalIpdu03"
        sig_start_bit = 44
        update_id_bit = 45
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
        startbit = 44
        byte = 5
        mask = 0b00011110
        unmask = 0b11100001
        shift = 1

    class VehModMngtGlbSafe1EgyLvlElecMai_0_CEMBackBoneSignalIpdu02:
        sig_name = "VehModMngtGlbSafe1EgyLvlElecMai_0_CEMBackBoneSignalIpdu02"
        sig_start_bit = 27
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
        startbit = 27
        byte = 3
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class VehModMngtGlbSafe1Cntr_0_CEMBackBoneSignalIpdu02:
        sig_name = "VehModMngtGlbSafe1Cntr_0_CEMBackBoneSignalIpdu02"
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

    class VehModMngtGlbSafe1FltEgyCnsWdSts_0_CEMBackBoneSignalIpdu02:
        sig_name = "VehModMngtGlbSafe1FltEgyCnsWdSts_0_CEMBackBoneSignalIpdu02"
        sig_start_bit = 33
        update_id_bit = None
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

    class ChrgnUReq:
        sig_name = "ChrgnUReq"
        sig_start_bit = 55
        update_id_bit = 40
        sig_length = 8
        sig_value_factor = 0.025
        sig_value_offset = 10.6
        sig_value_min = 0
        sig_value_max = 216
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

    class VehModMngtGlbSafe1CarModSts1_0_CEMBackBoneSignalIpdu02:
        sig_name = "VehModMngtGlbSafe1CarModSts1_0_CEMBackBoneSignalIpdu02"
        sig_start_bit = 39
        update_id_bit = None
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

    class VehModMngtGlbSafe1PwrLvlElecMai_0_CEMBackBoneSignalIpdu02:
        sig_name = "VehModMngtGlbSafe1PwrLvlElecMai_0_CEMBackBoneSignalIpdu02"
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

    class VehModMngtGlbSafe1UsgModSts_0_CEMBackBoneSignalIpdu02:
        sig_name = "VehModMngtGlbSafe1UsgModSts_0_CEMBackBoneSignalIpdu02"
        sig_start_bit = 11
        update_id_bit = None
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
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class TwliBriSts:
        sig_name = "TwliBriSts"
        sig_start_bit = 47
        update_id_bit = 46
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TwliBriSts1_Night': 0, 'TwliBriSts1_Day': 1}
        compute_method = None
        length = 1
        startbit = 47
        byte = 5
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp_0_CEMBackBoneSignalIpdu02:
        sig_name = "VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp_0_CEMBackBoneSignalIpdu02"
        sig_start_bit = 36
        update_id_bit = None
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

    class VehModMngtGlbSafe1_0_CEMBackBoneSignalIpdu02_UB:
        sig_name = "VehModMngtGlbSafe1_0_CEMBackBoneSignalIpdu02_UB"
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


class VddmToHvcmPropDiagReqFrame:
    msg_name = "VddmToHvcmPropDiagReqFrame"
    msg_id = 1872
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['HVCM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class VddmPropFr31:
    msg_name = "VddmPropFr31"
    msg_id = 1051
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.5
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['BECM1', 'ECM']
    sig_group_dict = {'AmbTEstimd': ['AmbTEstimdAmbTEstimd', 'AmbTEstimdQf'], 'BattThermMngtInFuture': ['BattThermMngtInFuturePwrAtTime', 'BattThermMngtInFutureSequenceNo', 'BattThermMngtInFutureTempAtTime', 'BattThermMngtInFutureThermModAtTime', 'BattThermMngtInFutureTime', 'BattThermMngtInFutureVersionNo']}
    sig_group_dataid_dict = {}

    class AmbTEstimdAmbTEstimd:
        sig_name = "AmbTEstimdAmbTEstimd"
        sig_start_bit = 50
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -70.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 700
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 50
        bmuws_info = [(6, 0b00000111, 0b11111000, 3, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class BattThermMngtInFutureTime:
        sig_name = "BattThermMngtInFutureTime"
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

    class BattThermMngtInFutureSequenceNo:
        sig_name = "BattThermMngtInFutureSequenceNo"
        sig_start_bit = 12
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
        startbit = 12
        byte = 1
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class BattThermMngtInFutureTempAtTime:
        sig_name = "BattThermMngtInFutureTempAtTime"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -50.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 50
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 23
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class AmbTEstimdQf:
        sig_name = "AmbTEstimdQf"
        sig_start_bit = 51
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvacTIfQf_SnsrDataNotOk': 0, 'HvacTIfQf_SnsrDataOk': 1}
        compute_method = None
        length = 1
        startbit = 51
        byte = 6
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class BattThermMngtInFuturePwrAtTime:
        sig_name = "BattThermMngtInFuturePwrAtTime"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 50.0
        sig_value_offset = -25000.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 500
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class BattThermMngtInFutureVersionNo:
        sig_name = "BattThermMngtInFutureVersionNo"
        sig_start_bit = 2
        update_id_bit = None
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
        startbit = 2
        byte = 0
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class AmbTEstimd_UB:
        sig_name = "AmbTEstimd_UB"
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

    class BattThermMngtInFutureThermModAtTime:
        sig_name = "BattThermMngtInFutureThermModAtTime"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Idle': 0, 'ThermalBalancing': 1, 'PassiveHeating': 2, 'ActiveHeating': 3, 'PassiveCooling': 4, 'ActiveCooling': 5, 'CombinedCooling': 6, 'Reserved': 7}
        compute_method = None
        length = 3
        startbit = 15
        byte = 1
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class BattThermMngtInFuture_UB:
        sig_name = "BattThermMngtInFuture_UB"
        sig_start_bit = 3
        update_id_bit = 3
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
        startbit = 3
        byte = 0
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3


class CddIgmPropFr02:
    msg_name = "CddIgmPropFr02"
    msg_id = 329
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 8
    tx_node = "HVCM"
    rx_nodes = ['VDDM', 'ECM']
    sig_group_dict = {'IDcDcActLoSide': ['IDcDcActLoSideChks', 'IDcDcActLoSideCntr', 'IDcDcActLoSideIDcDcActLoSide']}
    sig_group_dataid_dict = {'IDcDcActLoSide': 20}

    class IDcDcActLoSide_UB:
        sig_name = "IDcDcActLoSide_UB"
        sig_start_bit = 20
        update_id_bit = 20
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
        startbit = 20
        byte = 2
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class LimnIndcnDcDc:
        sig_name = "LimnIndcnDcDc"
        sig_start_bit = 55
        update_id_bit = 21
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
        startbit = 55
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class IDcDcActLoSideCntr:
        sig_name = "IDcDcActLoSideCntr"
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

    class IDcDcActLoSideChks:
        sig_name = "IDcDcActLoSideChks"
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

    class DcDcCoolgReq:
        sig_name = "DcDcCoolgReq"
        sig_start_bit = 10
        update_id_bit = 11
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvCoolg1_NoRequestForMoreCoolantPower': 0, 'HvCoolg1_IncreaseLevel1ForMoreCoolantPower': 1, 'HvCoolg1_IncreaseLevel2ForMoreCoolantPower': 2, 'HvCoolg1_MaxCoolingPower': 3, 'HvCoolg1_NotDefined': 4}
        compute_method = None
        length = 3
        startbit = 10
        byte = 1
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class IDcDcActLoSideIDcDcActLoSide:
        sig_name = "IDcDcActLoSideIDcDcActLoSide"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11110000, 0b00001111, 4, 4)]

    class TDcDc:
        sig_name = "TDcDc"
        sig_start_bit = 7
        update_id_bit = 12
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 40
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class MgmPropFr05:
    msg_name = "MgmPropFr05"
    msg_id = 148
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "MGM"
    rx_nodes = ['ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class IsgHeatPwrAct:
        sig_name = "IsgHeatPwrAct"
        sig_start_bit = 63
        update_id_bit = 51
        sig_length = 8
        sig_value_factor = 50.0
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


class BecmPropDevFr03:
    msg_name = "BecmPropDevFr03"
    msg_id = 1488
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['CCM']
    sig_group_dict = {'BECMdevelpsignalgroup3': ['BECMdevelpsignalgroup3Functiondevpsignalgroup1', 'BECMdevelpsignalgroup3Functiondevpsignalgroup2', 'BECMdevelpsignalgroup3Functiondevpsignalgroup3', 'BECMdevelpsignalgroup3Functiondevpsignalgroup4', 'BECMdevelpsignalgroup3Functiondevpsignalgroup5', 'BECMdevelpsignalgroup3Functiondevpsignalgroup6', 'BECMdevelpsignalgroup3Functiondevpsignalgroup7', 'BECMdevelpsignalgroup3Functiondevpsignalgroup8']}
    sig_group_dataid_dict = {}

    class BECMdevelpsignalgroup3Functiondevpsignalgroup8:
        sig_name = "BECMdevelpsignalgroup3Functiondevpsignalgroup8"
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

    class BECMdevelpsignalgroup3Functiondevpsignalgroup2:
        sig_name = "BECMdevelpsignalgroup3Functiondevpsignalgroup2"
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

    class BECMdevelpsignalgroup3Functiondevpsignalgroup4:
        sig_name = "BECMdevelpsignalgroup3Functiondevpsignalgroup4"
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

    class BECMdevelpsignalgroup3Functiondevpsignalgroup1:
        sig_name = "BECMdevelpsignalgroup3Functiondevpsignalgroup1"
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

    class BECMdevelpsignalgroup3Functiondevpsignalgroup5:
        sig_name = "BECMdevelpsignalgroup3Functiondevpsignalgroup5"
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

    class BECMdevelpsignalgroup3Functiondevpsignalgroup3:
        sig_name = "BECMdevelpsignalgroup3Functiondevpsignalgroup3"
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

    class BECMdevelpsignalgroup3Functiondevpsignalgroup6:
        sig_name = "BECMdevelpsignalgroup3Functiondevpsignalgroup6"
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

    class BECMdevelpsignalgroup3Functiondevpsignalgroup7:
        sig_name = "BECMdevelpsignalgroup3Functiondevpsignalgroup7"
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


class VddmToEgsmPropDiagReqFrame:
    msg_name = "VddmToEgsmPropDiagReqFrame"
    msg_id = 1843
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['EGSM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class IemPropulsionCANNmFr:
    msg_name = "IemPropulsionCANNmFr"
    msg_id = 1308
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "IEM"
    rx_nodes = ['EGSM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class MgmToVddmPropDiagRespFrame:
    msg_name = "MgmToVddmPropDiagRespFrame"
    msg_id = 1585
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "MGM"
    rx_nodes = ['VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class BecmToVgmJ1979OBDPropDiagResFrame11:
    msg_name = "BecmToVgmJ1979OBDPropDiagResFrame11"
    msg_id = 2026
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['BGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class IemPropFr02:
    msg_name = "IemPropFr02"
    msg_id = 1125
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.8
    msg_length = 8
    tx_node = "IEM"
    rx_nodes = ['CCM']
    sig_group_dict = {'IEMTestFr2': ['IEMTestFr2Byte0', 'IEMTestFr2Byte1', 'IEMTestFr2Byte2', 'IEMTestFr2Byte3', 'IEMTestFr2Byte4', 'IEMTestFr2Byte5', 'IEMTestFr2Byte6', 'IEMTestFr2Byte7']}
    sig_group_dataid_dict = {}

    class IEMTestFr2Byte4:
        sig_name = "IEMTestFr2Byte4"
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

    class IEMTestFr2Byte3:
        sig_name = "IEMTestFr2Byte3"
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

    class IEMTestFr2Byte7:
        sig_name = "IEMTestFr2Byte7"
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

    class IEMTestFr2Byte2:
        sig_name = "IEMTestFr2Byte2"
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

    class IEMTestFr2Byte5:
        sig_name = "IEMTestFr2Byte5"
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

    class IEMTestFr2Byte6:
        sig_name = "IEMTestFr2Byte6"
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

    class IEMTestFr2Byte1:
        sig_name = "IEMTestFr2Byte1"
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

    class IEMTestFr2Byte0:
        sig_name = "IEMTestFr2Byte0"
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


class BecmPropFr23:
    msg_name = "BecmPropFr23"
    msg_id = 322
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.03
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['VDDM', 'ECM']
    sig_group_dict = {'HvBattCellUInfo': ['HvBattCellUInfoU1', 'HvBattCellUInfoU2', 'HvBattCellUInfoU3', 'HvBattCellUInfoU4']}
    sig_group_dataid_dict = {}

    class HvBattCellUInfoU2:
        sig_name = "HvBattCellUInfoU2"
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

    class HvBattCellUInfo_UB:
        sig_name = "HvBattCellUInfo_UB"
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

    class HvBattCellUInfoU3:
        sig_name = "HvBattCellUInfoU3"
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

    class HvBattCellUInfoU1:
        sig_name = "HvBattCellUInfoU1"
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

    class HvBattCellUInfoU4:
        sig_name = "HvBattCellUInfoU4"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 13
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111000, 0b00000111, 5, 3)]

    class HvBattLimnIndcn:
        sig_name = "HvBattLimnIndcn"
        sig_start_bit = 55
        update_id_bit = 40
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
        startbit = 55
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111111, 0b00000000, 8, 0)]


class VddmPropFr10:
    msg_name = "VddmPropFr10"
    msg_id = 312
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.025
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']
    sig_group_dict = {'BrkFricTqAtWhlAct': ['BrkFricTqAtWhlActBrkFricTqAtWhlFrntLeAct', 'BrkFricTqAtWhlActBrkFricTqAtWhlFrntRiAct', 'BrkFricTqAtWhlActBrkFricTqAtWhlReLeAct', 'BrkFricTqAtWhlActBrkFricTqAtWhlReRiAct']}
    sig_group_dataid_dict = {}

    class BrkFricTqAtWhlActBrkFricTqAtWhlReLeAct:
        sig_name = "BrkFricTqAtWhlActBrkFricTqAtWhlReLeAct"
        sig_start_bit = 36
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 36
        bmuws_info = [(4, 0b00011111, 0b11100000, 5, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class BrkFricTqAtWhlAct_UB:
        sig_name = "BrkFricTqAtWhlAct_UB"
        sig_start_bit = 5
        update_id_bit = 5
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
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class BrkFricTqAtWhlActBrkFricTqAtWhlFrntRiAct:
        sig_name = "BrkFricTqAtWhlActBrkFricTqAtWhlFrntRiAct"
        sig_start_bit = 20
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 20
        bmuws_info = [(2, 0b00011111, 0b11100000, 5, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class BrkFricTqAtWhlActBrkFricTqAtWhlFrntLeAct:
        sig_name = "BrkFricTqAtWhlActBrkFricTqAtWhlFrntLeAct"
        sig_start_bit = 4
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 4
        bmuws_info = [(0, 0b00011111, 0b11100000, 5, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class BrkFricTqAtWhlActBrkFricTqAtWhlReRiAct:
        sig_name = "BrkFricTqAtWhlActBrkFricTqAtWhlReRiAct"
        sig_start_bit = 52
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 52
        bmuws_info = [(6, 0b00011111, 0b11100000, 5, 0), (7, 0b11111111, 0b00000000, 8, 0)]


class BecmPropFr01:
    msg_name = "BecmPropFr01"
    msg_id = 321
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['MGM', 'IEM', 'HVCM', 'ECM', 'VDDM']
    sig_group_dict = {'HvSysRlySts': ['HvSysRlyStsChks', 'HvSysRlyStsCntr', 'HvSysRlyStsHvSysRlySts']}
    sig_group_dataid_dict = {'HvSysRlySts': 21}

    class HvSysRlyStsCntr:
        sig_name = "HvSysRlyStsCntr"
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

    class HvSysActvnInhb:
        sig_name = "HvSysActvnInhb"
        sig_start_bit = 37
        update_id_bit = 38
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
        startbit = 37
        byte = 4
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class HvSysPwrOff:
        sig_name = "HvSysPwrOff"
        sig_start_bit = 59
        update_id_bit = 21
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
        startbit = 59
        byte = 7
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class HvSysSts:
        sig_name = "HvSysSts"
        sig_start_bit = 58
        update_id_bit = 56
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvSysSts_Inin': 0, 'HvSysSts_Test': 1, 'HvSysSts_Rdy': 2}
        compute_method = None
        length = 2
        startbit = 58
        byte = 7
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class HvSysRlyStsChks:
        sig_name = "HvSysRlyStsChks"
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

    class HvBattUDynMaxLim:
        sig_name = "HvBattUDynMaxLim"
        sig_start_bit = 34
        update_id_bit = 35
        sig_length = 11
        sig_value_factor = 0.25
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 2044
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 34
        bmuws_info = [(4, 0b00000111, 0b11111000, 3, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class HvBattUDc:
        sig_name = "HvBattUDc"
        sig_start_bit = 18
        update_id_bit = 19
        sig_length = 11
        sig_value_factor = 0.25
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 2044
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 18
        bmuws_info = [(2, 0b00000111, 0b11111000, 3, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class HvSysRlyStsHvSysRlySts:
        sig_name = "HvSysRlyStsHvSysRlySts"
        sig_start_bit = 5
        update_id_bit = None
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
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class HvSysRlySts_UB:
        sig_name = "HvSysRlySts_UB"
        sig_start_bit = 22
        update_id_bit = 22
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
        startbit = 22
        byte = 2
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6


class VddmToBecmPropDiagReqFrame:
    msg_name = "VddmToBecmPropDiagReqFrame"
    msg_id = 1845
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['BECM1']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class VddmToVgmJ1979OBDPropDiagResFrame11:
    msg_name = "VddmToVgmJ1979OBDPropDiagResFrame11"
    msg_id = 2030
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['BGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class HvcmPropulsionCANNmFr:
    msg_name = "HvcmPropulsionCANNmFr"
    msg_id = 1327
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "HVCM"
    rx_nodes = ['BGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class EcmPropFr22:
    msg_name = "EcmPropFr22"
    msg_id = 392
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.07
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['BECM1', 'VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class DchaPwrAllwd:
        sig_name = "DchaPwrAllwd"
        sig_start_bit = 9
        update_id_bit = 35
        sig_length = 10
        sig_value_factor = 20.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 9
        bmuws_info = [(1, 0b00000011, 0b11111100, 2, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class HvBattFlwEstmd:
        sig_name = "HvBattFlwEstmd"
        sig_start_bit = 40
        update_id_bit = 43
        sig_length = 9
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 40
        bmuws_info = [(5, 0b00000001, 0b11111110, 1, 0), (6, 0b11111111, 0b00000000, 8, 0)]

    class HvBattChrgnPwrAllwd1:
        sig_name = "HvBattChrgnPwrAllwd1"
        sig_start_bit = 7
        update_id_bit = 10
        sig_length = 13
        sig_value_factor = 20.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111000, 0b00000111, 5, 3)]

    class HvBattThermReqFb:
        sig_name = "HvBattThermReqFb"
        sig_start_bit = 47
        update_id_bit = 37
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 8
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvBattThermReqFb_Default': 0, 'HvBattThermReqFb_Heating': 1, 'HvBattThermReqFb_HeatFinished': 2, 'HvBattThermReqFb_RadiatorCooling': 3, 'HvBattThermReqFb_CompressorCooling': 4, 'HvBattThermReqFb_CoolingFinish': 5, 'HvBattThermReqFb_Inhibited': 6, 'HvBattThermReqFb_HeatingByEmotCoolt': 7, 'HvBattThermReqFb_Fault': 8}
        compute_method = None
        length = 4
        startbit = 47
        byte = 5
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4


class EcmPropFr00:
    msg_name = "EcmPropFr00"
    msg_id = 74
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['MGM', 'BGM', 'VDDM']
    sig_group_dict = {'AccrPedlRat_0_EcmPropSignalIPdu00': ['AccrPedlRatAccrPedlRat_0_EcmPropSignalIPdu00', 'AccrPedlRatChks_0_EcmPropSignalIPdu00', 'AccrPedlRatCntr_0_EcmPropSignalIPdu00']}
    sig_group_dataid_dict = {'AccrPedlRat_0_EcmPropSignalIPdu00': 868}

    class IsgModReq:
        sig_name = "IsgModReq"
        sig_start_bit = 47
        update_id_bit = 43
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'IsgModTyp1_Inin': 0, 'IsgModTyp1_Stb': 1, 'IsgModTyp1_TqCtrl': 2, 'IsgModTyp1_SpdCtrl': 3, 'IsgModTyp1_UDcCtrl': 4, 'IsgModTyp1_PreChrg': 5, 'IsgModTyp1_PwrDwn': 6, 'IsgModTyp1_Flt': 7, 'IsgModTyp1_TcsCtrl': 8, 'IsgModTyp1_Reserved1': 9, 'IsgModTyp1_Reserved2': 10, 'IsgModTyp1_Reserved3': 11, 'IsgModTyp1_Reserved4': 12, 'IsgModTyp1_Reserved5': 13, 'IsgModTyp1_Reserved6': 14, 'IsgModTyp1_Reserved7': 15}
        compute_method = None
        length = 4
        startbit = 47
        byte = 5
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class AccrPedlRatChks_0_EcmPropSignalIPdu00:
        sig_name = "AccrPedlRatChks_0_EcmPropSignalIPdu00"
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

    class IsgSpdReq:
        sig_name = "IsgSpdReq"
        sig_start_bit = 54
        update_id_bit = 55
        sig_length = 15
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = -16384
        sig_value_max = 16383
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 54
        bmuws_info = [(6, 0b01111111, 0b10000000, 7, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class IsgCluOperTypReq:
        sig_name = "IsgCluOperTypReq"
        sig_start_bit = 27
        update_id_bit = 24
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WhlMotSysCluStsTyp1_NoReq': 0, 'WhlMotSysCluStsTyp1_ReqDisEngd': 1, 'WhlMotSysCluStsTyp1_SlwPosDiffSpd': 2, 'WhlMotSysCluStsTyp1_FstPosDiffSpd': 3, 'WhlMotSysCluStsTyp1_SlwNegDiffSpd': 4, 'WhlMotSysCluStsTyp1_FstNegDiffSpd': 5, 'WhlMotSysCluStsTyp1_Reserved1': 6, 'WhlMotSysCluStsTyp1_Reserved2': 7}
        compute_method = None
        length = 3
        startbit = 27
        byte = 3
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class AccrPedlRatAccrPedlRat_0_EcmPropSignalIPdu00:
        sig_name = "AccrPedlRatAccrPedlRat_0_EcmPropSignalIPdu00"
        sig_start_bit = 6
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 0.00390625
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 25600
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 6
        bmuws_info = [(0, 0b01111111, 0b10000000, 7, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class AccrPedlRatCntr_0_EcmPropSignalIPdu00:
        sig_name = "AccrPedlRatCntr_0_EcmPropSignalIPdu00"
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

    class AccrPedlRat_0_EcmPropSignalIPdu00_UB:
        sig_name = "AccrPedlRat_0_EcmPropSignalIPdu00_UB"
        sig_start_bit = 7
        update_id_bit = 7
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
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7


class IgmMgmPropFr05:
    msg_name = "IgmMgmPropFr05"
    msg_id = 342
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "MGM"
    rx_nodes = ['BECM1', 'ECM', 'VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class IsgLimnIndcn:
        sig_name = "IsgLimnIndcn"
        sig_start_bit = 55
        update_id_bit = 20
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
        startbit = 55
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class IsgUDc:
        sig_name = "IsgUDc"
        sig_start_bit = 2
        update_id_bit = 3
        sig_length = 11
        sig_value_factor = 0.25
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 2044
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 2
        bmuws_info = [(0, 0b00000111, 0b11111000, 3, 0), (1, 0b11111111, 0b00000000, 8, 0)]


class HvcmToVddmPropDiagRespFrame:
    msg_name = "HvcmToVddmPropDiagRespFrame"
    msg_id = 1616
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "HVCM"
    rx_nodes = ['VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class VddmPropFr36:
    msg_name = "VddmPropFr36"
    msg_id = 1143
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.12
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['BECM1']
    sig_group_dict = {'Vin': ['VinBlockNr', 'VinVINSignalPos1', 'VinVINSignalPos2', 'VinVINSignalPos3', 'VinVINSignalPos4', 'VinVINSignalPos5', 'VinVINSignalPos6', 'VinVINSignalPos7']}
    sig_group_dataid_dict = {}

    class VinVINSignalPos2:
        sig_name = "VinVINSignalPos2"
        sig_start_bit = 23
        update_id_bit = None
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

    class VinVINSignalPos6:
        sig_name = "VinVINSignalPos6"
        sig_start_bit = 55
        update_id_bit = None
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

    class VinVINSignalPos3:
        sig_name = "VinVINSignalPos3"
        sig_start_bit = 31
        update_id_bit = None
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

    class VinBlockNr:
        sig_name = "VinBlockNr"
        sig_start_bit = 7
        update_id_bit = None
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

    class VinVINSignalPos4:
        sig_name = "VinVINSignalPos4"
        sig_start_bit = 39
        update_id_bit = None
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

    class VinVINSignalPos7:
        sig_name = "VinVINSignalPos7"
        sig_start_bit = 63
        update_id_bit = None
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

    class VinVINSignalPos1:
        sig_name = "VinVINSignalPos1"
        sig_start_bit = 15
        update_id_bit = None
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

    class VinVINSignalPos5:
        sig_name = "VinVINSignalPos5"
        sig_start_bit = 47
        update_id_bit = None
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


class BecmPropFr12:
    msg_name = "BecmPropFr12"
    msg_id = 769
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.6
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['VDDM', 'ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HvBattPwrCdn:
        sig_name = "HvBattPwrCdn"
        sig_start_bit = 7
        update_id_bit = 15
        sig_length = 8
        sig_value_factor = 0.5
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 200
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


class IgmMgmPropFr03:
    msg_name = "IgmMgmPropFr03"
    msg_id = 314
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "MGM"
    rx_nodes = ['BECM1', 'ECM', 'VDDM']
    sig_group_dict = {'IsgTqAvl': ['IsgTqAvlMax', 'IsgTqAvlMin']}
    sig_group_dataid_dict = {}

    class IsgIDc:
        sig_name = "IsgIDc"
        sig_start_bit = 53
        update_id_bit = 54
        sig_length = 14
        sig_value_factor = 0.1
        sig_value_offset = -818.8
        sig_value_min = 0
        sig_value_max = 16380
        sig_byteorder = "Motorola"
        sig_value_init = 8188
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 14
        startbit = 53
        bmuws_info = [(6, 0b00111111, 0b11000000, 6, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class IsgTqAvl_UB:
        sig_name = "IsgTqAvl_UB"
        sig_start_bit = 25
        update_id_bit = 25
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
        startbit = 25
        byte = 3
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class IsgMotT_0_VDDMBackBoneSignalIPdu20:
        sig_name = "IsgMotT_0_VDDMBackBoneSignalIPdu20"
        sig_start_bit = 39
        update_id_bit = 24
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -50.0
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Motorola"
        sig_value_init = 50
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class IsgTqAvlMin:
        sig_name = "IsgTqAvlMin"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 14
        sig_value_factor = 1.0
        sig_value_offset = -8188.0
        sig_value_min = 0
        sig_value_max = 16380
        sig_byteorder = "Motorola"
        sig_value_init = 8188
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 14
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111100, 0b00000011, 6, 2)]

    class IsgCooltT:
        sig_name = "IsgCooltT"
        sig_start_bit = 47
        update_id_bit = 55
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 40
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class IsgTqAvlMax:
        sig_name = "IsgTqAvlMax"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 14
        sig_value_factor = 1.0
        sig_value_offset = -8188.0
        sig_value_min = 0
        sig_value_max = 16380
        sig_byteorder = "Motorola"
        sig_value_init = 8188
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 14
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111100, 0b00000011, 6, 2)]


class VddmPropFr05:
    msg_name = "VddmPropFr05"
    msg_id = 118
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.015
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['MGM', 'BECM1', 'EGSM', 'IEM', 'HVCM']
    sig_group_dict = {'VehSpdLgt_3_AcuFLRCANFDSignalIPdu01': ['VehSpdLgtA_3_AcuFLRCANFDSignalIPdu01', 'VehSpdLgtChks_3_AcuFLRCANFDSignalIPdu01', 'VehSpdLgtCntr_3_AcuFLRCANFDSignalIPdu01', 'VehSpdLgtQf_3_AcuFLRCANFDSignalIPdu01'], 'VehMtnSt_3_AcuFLRCANFDSignalIPdu01': ['VehMtnStChks_3_AcuFLRCANFDSignalIPdu01', 'VehMtnStCntr_3_AcuFLRCANFDSignalIPdu01', 'VehMtnStVehMtnSt_3_AcuFLRCANFDSignalIPdu01']}
    sig_group_dataid_dict = {'VehSpdLgt_3_AcuFLRCANFDSignalIPdu01': 55, 'VehMtnSt_3_AcuFLRCANFDSignalIPdu01': 54}

    class VehSpdLgtChks_3_AcuFLRCANFDSignalIPdu01:
        sig_name = "VehSpdLgtChks_3_AcuFLRCANFDSignalIPdu01"
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

    class VehSpdLgtCntr_3_AcuFLRCANFDSignalIPdu01:
        sig_name = "VehSpdLgtCntr_3_AcuFLRCANFDSignalIPdu01"
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

    class VehMtnStChks_3_AcuFLRCANFDSignalIPdu01:
        sig_name = "VehMtnStChks_3_AcuFLRCANFDSignalIPdu01"
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

    class VehMtnStVehMtnSt_3_AcuFLRCANFDSignalIPdu01:
        sig_name = "VehMtnStVehMtnSt_3_AcuFLRCANFDSignalIPdu01"
        sig_start_bit = 18
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VehMtnSt2_Ukwn': 0, 'VehMtnSt2_StandStillVal1': 1, 'VehMtnSt2_StandStillVal2': 2, 'VehMtnSt2_StandStillVal3': 3, 'VehMtnSt2_RollgFwdVal1': 4, 'VehMtnSt2_RollgFwdVal2': 5, 'VehMtnSt2_RollgBackwVal1': 6, 'VehMtnSt2_RollgBackwVal2': 7}
        compute_method = None
        length = 3
        startbit = 18
        byte = 2
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class VehMtnStCntr_3_AcuFLRCANFDSignalIPdu01:
        sig_name = "VehMtnStCntr_3_AcuFLRCANFDSignalIPdu01"
        sig_start_bit = 22
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
        startbit = 22
        byte = 2
        mask = 0b01111000
        unmask = 0b10000111
        shift = 3

    class VehSpdLgtA_3_AcuFLRCANFDSignalIPdu01:
        sig_name = "VehSpdLgtA_3_AcuFLRCANFDSignalIPdu01"
        sig_start_bit = 38
        update_id_bit = None
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
        startbit = 38
        bmuws_info = [(4, 0b01111111, 0b10000000, 7, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class VehSpdLgt_3_AcuFLRCANFDSignalIPdu01_UB:
        sig_name = "VehSpdLgt_3_AcuFLRCANFDSignalIPdu01_UB"
        sig_start_bit = 39
        update_id_bit = 39
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
        startbit = 39
        byte = 4
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VehMtnSt_3_AcuFLRCANFDSignalIPdu01_UB:
        sig_name = "VehMtnSt_3_AcuFLRCANFDSignalIPdu01_UB"
        sig_start_bit = 57
        update_id_bit = 57
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
        startbit = 57
        byte = 7
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VehSpdLgtQf_3_AcuFLRCANFDSignalIPdu01:
        sig_name = "VehSpdLgtQf_3_AcuFLRCANFDSignalIPdu01"
        sig_start_bit = 59
        update_id_bit = None
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
        startbit = 59
        byte = 7
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2


class IemPropFr09:
    msg_name = "IemPropFr09"
    msg_id = 1126
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.8
    msg_length = 8
    tx_node = "IEM"
    rx_nodes = ['CCM']
    sig_group_dict = {'IEMTestFr3': ['IEMTestFr3Byte0', 'IEMTestFr3Byte1', 'IEMTestFr3Byte2', 'IEMTestFr3Byte3', 'IEMTestFr3Byte4', 'IEMTestFr3Byte5', 'IEMTestFr3Byte6', 'IEMTestFr3Byte7']}
    sig_group_dataid_dict = {}

    class IEMTestFr3Byte4:
        sig_name = "IEMTestFr3Byte4"
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

    class IEMTestFr3Byte1:
        sig_name = "IEMTestFr3Byte1"
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

    class IEMTestFr3Byte2:
        sig_name = "IEMTestFr3Byte2"
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

    class IEMTestFr3Byte6:
        sig_name = "IEMTestFr3Byte6"
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

    class IEMTestFr3Byte7:
        sig_name = "IEMTestFr3Byte7"
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

    class IEMTestFr3Byte3:
        sig_name = "IEMTestFr3Byte3"
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

    class IEMTestFr3Byte5:
        sig_name = "IEMTestFr3Byte5"
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

    class IEMTestFr3Byte0:
        sig_name = "IEMTestFr3Byte0"
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


class MgmPropFr01:
    msg_name = "MgmPropFr01"
    msg_id = 1178
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.8
    msg_length = 8
    tx_node = "MGM"
    rx_nodes = ['CCM']
    sig_group_dict = {'MGMTestFr1': ['MGMTestFr1Byte0', 'MGMTestFr1Byte1', 'MGMTestFr1Byte2', 'MGMTestFr1Byte3', 'MGMTestFr1Byte4', 'MGMTestFr1Byte5', 'MGMTestFr1Byte6', 'MGMTestFr1Byte7']}
    sig_group_dataid_dict = {}

    class MGMTestFr1Byte7:
        sig_name = "MGMTestFr1Byte7"
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

    class MGMTestFr1Byte4:
        sig_name = "MGMTestFr1Byte4"
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

    class MGMTestFr1Byte3:
        sig_name = "MGMTestFr1Byte3"
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

    class MGMTestFr1Byte0:
        sig_name = "MGMTestFr1Byte0"
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

    class MGMTestFr1Byte5:
        sig_name = "MGMTestFr1Byte5"
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

    class MGMTestFr1Byte2:
        sig_name = "MGMTestFr1Byte2"
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

    class MGMTestFr1Byte6:
        sig_name = "MGMTestFr1Byte6"
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

    class MGMTestFr1Byte1:
        sig_name = "MGMTestFr1Byte1"
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


class BecmPropFr02:
    msg_name = "BecmPropFr02"
    msg_id = 373
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['MGM', 'CCM', 'S2SReceiver', 'IEM', 'ECM', 'VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class JIDUChgrFlg:
        sig_name = "JIDUChgrFlg"
        sig_start_bit = 7
        update_id_bit = 5
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffCrit1_NotVld1': 0, 'OnOffCrit1_Off': 1, 'OnOffCrit1_On': 2, 'OnOffCrit1_NotVld2': 3}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HvBattUDynMinLim:
        sig_name = "HvBattUDynMinLim"
        sig_start_bit = 26
        update_id_bit = 27
        sig_length = 11
        sig_value_factor = 0.25
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 2044
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 26
        bmuws_info = [(3, 0b00000111, 0b11111000, 3, 0), (4, 0b11111111, 0b00000000, 8, 0)]

    class MaintainBattTFb:
        sig_name = "MaintainBattTFb"
        sig_start_bit = 59
        update_id_bit = 57
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
        startbit = 59
        byte = 7
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class MaintainBattTReq:
        sig_name = "MaintainBattTReq"
        sig_start_bit = 31
        update_id_bit = 30
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ClimaSts_Start': 0, 'ClimaSts_Finish': 1}
        compute_method = None
        length = 1
        startbit = 31
        byte = 3
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7


class BecmPropFr15:
    msg_name = "BecmPropFr15"
    msg_id = 323
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['MGM', 'HVCM', 'ECM', 'VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HvBattPwrLimDcha1:
        sig_name = "HvBattPwrLimDcha1"
        sig_start_bit = 34
        update_id_bit = 20
        sig_length = 11
        sig_value_factor = 0.25
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 34
        bmuws_info = [(4, 0b00000111, 0b11111000, 3, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class HvBattPreChrgReq:
        sig_name = "HvBattPreChrgReq"
        sig_start_bit = 37
        update_id_bit = 36
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
        startbit = 37
        byte = 4
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class HvBattIDc1:
        sig_name = "HvBattIDc1"
        sig_start_bit = 6
        update_id_bit = 7
        sig_length = 15
        sig_value_factor = 0.1
        sig_value_offset = -1638.0
        sig_value_min = 0
        sig_value_max = 32767
        sig_byteorder = "Motorola"
        sig_value_init = 16380
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 6
        bmuws_info = [(0, 0b01111111, 0b10000000, 7, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class DCChrgnHndlSts:
        sig_name = "DCChrgnHndlSts"
        sig_start_bit = 23
        update_id_bit = 35
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
        startbit = 23
        byte = 2
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class HvBattPwrLimChrg1:
        sig_name = "HvBattPwrLimChrg1"
        sig_start_bit = 18
        update_id_bit = 19
        sig_length = 11
        sig_value_factor = 0.25
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 18
        bmuws_info = [(2, 0b00000111, 0b11111000, 3, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class HvBattPwrLimDchaSoft:
        sig_name = "HvBattPwrLimDchaSoft"
        sig_start_bit = 55
        update_id_bit = 60
        sig_length = 11
        sig_value_factor = 0.25
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 55
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b11100000, 0b00011111, 3, 5)]


class BecmPropFr17:
    msg_name = "BecmPropFr17"
    msg_id = 837
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 1.0
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['VDDM', 'ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HvBattPreHeatgReq:
        sig_name = "HvBattPreHeatgReq"
        sig_start_bit = 60
        update_id_bit = 33
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PreHeatgReq_Default': 0, 'PreHeatgReq_On': 1, 'PreHeatgReq_Off': 2, 'PreHeatgReq_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 60
        byte = 7
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class HvBattThermMod:
        sig_name = "HvBattThermMod"
        sig_start_bit = 63
        update_id_bit = 34
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvBattThermMod_Idle': 0, 'HvBattThermMod_ThermalBalancing': 1, 'HvBattThermMod_PassiveHeating': 2, 'HvBattThermMod_ActiveHeating': 3, 'HvBattThermMod_PassiveCooling': 4, 'HvBattThermMod_ActiveCooling': 5, 'HvBattThermMod_CombinedCooling': 6, 'HvBattThermMod_Reserved': 7}
        compute_method = None
        length = 3
        startbit = 63
        byte = 7
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class HvBattCooltMaxTReq:
        sig_name = "HvBattCooltMaxTReq"
        sig_start_bit = 47
        update_id_bit = 36
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -50.0
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Motorola"
        sig_value_init = 50
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvBattTMinSerlNr:
        sig_name = "HvBattTMinSerlNr"
        sig_start_bit = 31
        update_id_bit = 37
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvBattCellTNr:
        sig_name = "HvBattCellTNr"
        sig_start_bit = 7
        update_id_bit = 39
        sig_length = 16
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 65531
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class HvBattTMaxSerlNr:
        sig_name = "HvBattTMaxSerlNr"
        sig_start_bit = 23
        update_id_bit = 38
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 23
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvBattCooltMinTReq:
        sig_name = "HvBattCooltMinTReq"
        sig_start_bit = 55
        update_id_bit = 35
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -50.0
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Motorola"
        sig_value_init = 50
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class EcmPropFr30:
    msg_name = "EcmPropFr30"
    msg_id = 1168
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 1.0
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['BECM1']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class CooltInletT:
        sig_name = "CooltInletT"
        sig_start_bit = 47
        update_id_bit = 57
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -60.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 600
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11100000, 0b00011111, 3, 5)]

    class CooltOutletT:
        sig_name = "CooltOutletT"
        sig_start_bit = 52
        update_id_bit = 56
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -60.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 600
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 52
        bmuws_info = [(6, 0b00011111, 0b11100000, 5, 0), (7, 0b11111100, 0b00000011, 6, 2)]


class BecmPropulsionCANNmFr:
    msg_name = "BecmPropulsionCANNmFr"
    msg_id = 1305
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class IemPropFr14:
    msg_name = "IemPropFr14"
    msg_id = 544
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.08
    msg_length = 8
    tx_node = "IEM"
    rx_nodes = ['ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class WhlMotSysHeatFdBck:
        sig_name = "WhlMotSysHeatFdBck"
        sig_start_bit = 15
        update_id_bit = 13
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WhlMotSysHeatFdBck_On': 0, 'WhlMotSysHeatFdBck_Off': 1, 'WhlMotSysHeatFdBck_Inhibt': 2, 'WhlMotSysHeatFdBck_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 15
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class WhlMotSysHeatPwrMax:
        sig_name = "WhlMotSysHeatPwrMax"
        sig_start_bit = 7
        update_id_bit = 12
        sig_length = 8
        sig_value_factor = 50.0
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


class IgmMgmPropFr07:
    msg_name = "IgmMgmPropFr07"
    msg_id = 627
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "MGM"
    rx_nodes = ['ECM', 'VDDM']
    sig_group_dict = {'IgmGeneric': ['IgmGenericADAlrmSt', 'IgmGenericDTCHig', 'IgmGenericDTCLow', 'IgmGenericDTCMid', 'IgmGenericDTCSts', 'IgmGenericEMQnty', 'IgmGenericEMSeqNr', 'IgmGenericFltAlrmSt', 'IgmGenericIacAlrmSt', 'IgmGenericInvrtTAlrmSt', 'IgmGenericModStatusRms', 'IgmGenericMotTAlrmSt', 'IgmGenericRslAlrmSt', 'IgmGenericSpdAlrmSt', 'IgmGenericTypeInfo', 'IgmGenericUDcAlrmSt']}
    sig_group_dataid_dict = {}

    class IgmGenericIacAlrmSt:
        sig_name = "IgmGenericIacAlrmSt"
        sig_start_bit = 51
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSt_Disarmd': 0, 'AlrmSt_Armd': 1, 'AlrmSt_Actv': 2}
        compute_method = None
        length = 2
        startbit = 51
        byte = 6
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class IgmGenericDTCSts:
        sig_name = "IgmGenericDTCSts"
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

    class IgmGenericInvrtTAlrmSt:
        sig_name = "IgmGenericInvrtTAlrmSt"
        sig_start_bit = 49
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSt_Disarmd': 0, 'AlrmSt_Armd': 1, 'AlrmSt_Actv': 2}
        compute_method = None
        length = 2
        startbit = 49
        byte = 6
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class IgmGenericRslAlrmSt:
        sig_name = "IgmGenericRslAlrmSt"
        sig_start_bit = 61
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSt_Disarmd': 0, 'AlrmSt_Armd': 1, 'AlrmSt_Actv': 2}
        compute_method = None
        length = 2
        startbit = 61
        byte = 7
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class IgmGenericSpdAlrmSt:
        sig_name = "IgmGenericSpdAlrmSt"
        sig_start_bit = 59
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSt_Disarmd': 0, 'AlrmSt_Armd': 1, 'AlrmSt_Actv': 2}
        compute_method = None
        length = 2
        startbit = 59
        byte = 7
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class IgmGenericEMSeqNr:
        sig_name = "IgmGenericEMSeqNr"
        sig_start_bit = 35
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
        startbit = 35
        byte = 4
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class IgmGenericUDcAlrmSt:
        sig_name = "IgmGenericUDcAlrmSt"
        sig_start_bit = 57
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSt_Disarmd': 0, 'AlrmSt_Armd': 1, 'AlrmSt_Actv': 2}
        compute_method = None
        length = 2
        startbit = 57
        byte = 7
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class IgmGenericDTCHig:
        sig_name = "IgmGenericDTCHig"
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

    class IgmGenericEMQnty:
        sig_name = "IgmGenericEMQnty"
        sig_start_bit = 39
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
        startbit = 39
        byte = 4
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class IgmGenericDTCLow:
        sig_name = "IgmGenericDTCLow"
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

    class IgmGenericADAlrmSt:
        sig_name = "IgmGenericADAlrmSt"
        sig_start_bit = 55
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSt_Disarmd': 0, 'AlrmSt_Armd': 1, 'AlrmSt_Actv': 2}
        compute_method = None
        length = 2
        startbit = 55
        byte = 6
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class IgmGenericTypeInfo:
        sig_name = "IgmGenericTypeInfo"
        sig_start_bit = 43
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
        startbit = 43
        byte = 5
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class IgmGenericModStatusRms:
        sig_name = "IgmGenericModStatusRms"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 3
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ModStatusRms_Invalid': 0, 'PModStatusRms_wrCns': 1, 'ModStatusRms_PwrGen': 2, 'ModStatusRms_OffSts': 3, 'ModStatusRms_RdySts': 4, 'ModStatusRms_Abnormal': 5, 'ModStatusRms_Invalid1': 6, 'ModStatusRms_Invalid2': 7, 'ModStatusRms_Invalid3': 8, 'ModStatusRms_Invalid4': 9, 'ModStatusRms_Invalid5': 10, 'ModStatusRms_Invalid6': 11, 'ModStatusRms_Invalid7': 12, 'ModStatusRms_Invalid8': 13, 'ModStatusRms_Invalid9': 14, 'ModStatusRms_Invalid10': 15}
        compute_method = None
        length = 4
        startbit = 47
        byte = 5
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class IgmGenericMotTAlrmSt:
        sig_name = "IgmGenericMotTAlrmSt"
        sig_start_bit = 63
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSt_Disarmd': 0, 'AlrmSt_Armd': 1, 'AlrmSt_Actv': 2}
        compute_method = None
        length = 2
        startbit = 63
        byte = 7
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class IgmGenericFltAlrmSt:
        sig_name = "IgmGenericFltAlrmSt"
        sig_start_bit = 53
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSt_Disarmd': 0, 'AlrmSt_Armd': 1, 'AlrmSt_Actv': 2}
        compute_method = None
        length = 2
        startbit = 53
        byte = 6
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class IgmGenericDTCMid:
        sig_name = "IgmGenericDTCMid"
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


class BecmPropFr03:
    msg_name = "BecmPropFr03"
    msg_id = 376
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.07
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['VDDM', 'IEM', 'ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HvSysLimnIndcn:
        sig_name = "HvSysLimnIndcn"
        sig_start_bit = 23
        update_id_bit = 35
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

    class HvBattSoc:
        sig_name = "HvBattSoc"
        sig_start_bit = 47
        update_id_bit = 52
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
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11100000, 0b00011111, 3, 5)]

    class HvBattULim:
        sig_name = "HvBattULim"
        sig_start_bit = 50
        update_id_bit = 51
        sig_length = 11
        sig_value_factor = 0.25
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 2044
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 50
        bmuws_info = [(6, 0b00000111, 0b11111000, 3, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class HvBattCoolgReq:
        sig_name = "HvBattCoolgReq"
        sig_start_bit = 39
        update_id_bit = 37
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvBattCoolgReq_NotReqd': 0, 'HvBattCoolgReq_LoReq': 1, 'HvBattCoolgReq_MedReq': 2, 'HvBattCoolgReq_HiReq': 3}
        compute_method = None
        length = 2
        startbit = 39
        byte = 4
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HvBattChrgnCmpl:
        sig_name = "HvBattChrgnCmpl"
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
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class HvBattILim:
        sig_name = "HvBattILim"
        sig_start_bit = 4
        update_id_bit = 5
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 4
        bmuws_info = [(0, 0b00011111, 0b11100000, 5, 0), (1, 0b11111111, 0b00000000, 8, 0)]


class VddmPropFr29:
    msg_name = "VddmPropFr29"
    msg_id = 49
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.015
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']
    sig_group_dict = {'AccrOvrdnAllwdForAutDrv': ['AccrOvrdnAllwdForAutDrvChks', 'AccrOvrdnAllwdForAutDrvCntr', 'AccrOvrdnAllwdForAutDrvYesNo1']}
    sig_group_dataid_dict = {}

    class AccrOvrdnAllwdForAutDrvCntr:
        sig_name = "AccrOvrdnAllwdForAutDrvCntr"
        sig_start_bit = 51
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
        startbit = 51
        byte = 6
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class AccrOvrdnAllwdForAutDrv_UB:
        sig_name = "AccrOvrdnAllwdForAutDrv_UB"
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

    class AccrOvrdnAllwdForAutDrvYesNo1:
        sig_name = "AccrOvrdnAllwdForAutDrvYesNo1"
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
        sig_value_table = {'YesNo1_Yes': 0, 'YesNo1_No': 1}
        compute_method = None
        length = 1
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class AccrOvrdnAllwdForAutDrvChks:
        sig_name = "AccrOvrdnAllwdForAutDrvChks"
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


class EcmPropFr25:
    msg_name = "EcmPropFr25"
    msg_id = 634
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['MGM', 'BECM1', 'IEM', 'VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class DrvgCyc:
        sig_name = "DrvgCyc"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class DChrgTarValLnr:
        sig_name = "DChrgTarValLnr"
        sig_start_bit = 34
        update_id_bit = 38
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
        startbit = 34
        bmuws_info = [(4, 0b00000111, 0b11111000, 3, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class ResdEgyOfDischrgn:
        sig_name = "ResdEgyOfDischrgn"
        sig_start_bit = 15
        update_id_bit = 39
        sig_length = 13
        sig_value_factor = 20.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 15
        bmuws_info = [(1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111000, 0b00000111, 5, 3)]


class BecmPropFr07:
    msg_name = "BecmPropFr07"
    msg_id = 662
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.6
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['VDDM', 'ECM']
    sig_group_dict = {'HvBattHeatStopReq': ['HvBattHeatStopReqBrkLiOnReqChks', 'HvBattHeatStopReqBrkLiOnReqCntr', 'HvBattHeatStopReqBrkLiOnReqSts']}
    sig_group_dataid_dict = {'HvBattHeatStopReq': 7005}

    class HvBattHeatStopReqBrkLiOnReqChks:
        sig_name = "HvBattHeatStopReqBrkLiOnReqChks"
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

    class FastChrgnLockCtrl:
        sig_name = "FastChrgnLockCtrl"
        sig_start_bit = 14
        update_id_bit = 13
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
        startbit = 14
        byte = 1
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class HvBattHeatStopReq_UB:
        sig_name = "HvBattHeatStopReq_UB"
        sig_start_bit = 12
        update_id_bit = 12
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
        startbit = 12
        byte = 1
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class HvBattHeatStopReqBrkLiOnReqCntr:
        sig_name = "HvBattHeatStopReqBrkLiOnReqCntr"
        sig_start_bit = 11
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
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class HvBattHeatStopReqBrkLiOnReqSts:
        sig_name = "HvBattHeatStopReqBrkLiOnReqSts"
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
        sig_value_table = {'ReqSts1_NotReqd': 0, 'ReqSts1_Reqd': 1}
        compute_method = None
        length = 1
        startbit = 31
        byte = 3
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class HvBattCooltTReq:
        sig_name = "HvBattCooltTReq"
        sig_start_bit = 7
        update_id_bit = 15
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -50.0
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Motorola"
        sig_value_init = 50
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class EcmPropFr24:
    msg_name = "EcmPropFr24"
    msg_id = 75
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['MGM', 'BECM1', 'EGSM', 'IEM', 'VDDM']
    sig_group_dict = {'DrvrDesDir': ['DrvrDesDirChks', 'DrvrDesDirCntr', 'DrvrDesDirDrvrDesDir'], 'EngSt1WdSts_1_EcmPropSignalIPdu24': ['EngSt1WdStsChks_1_EcmPropSignalIPdu24', 'EngSt1WdStsCntr_1_EcmPropSignalIPdu24', 'EngSt1WdStsEngSt1WdSts_1_EcmPropSignalIPdu24']}
    sig_group_dataid_dict = {'DrvrDesDir': 627, 'EngSt1WdSts_1_EcmPropSignalIPdu24': 137}

    class GearLvrIndcn_1_EcmPropSignalIPdu24:
        sig_name = "GearLvrIndcn_1_EcmPropSignalIPdu24"
        sig_start_bit = 27
        update_id_bit = 24
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
        startbit = 27
        byte = 3
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class DrvrDesDir_UB:
        sig_name = "DrvrDesDir_UB"
        sig_start_bit = 56
        update_id_bit = 56
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
        startbit = 56
        byte = 7
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class DrvrDesDirCntr:
        sig_name = "DrvrDesDirCntr"
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

    class DrvrDesDirDrvrDesDir:
        sig_name = "DrvrDesDirDrvrDesDir"
        sig_start_bit = 59
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DrvrDesDir1_Undefd': 0, 'DrvrDesDir1_Fwd': 1, 'DrvrDesDir1_Rvs': 2, 'DrvrDesDir1_Neut': 3, 'DrvrDesDir1_Resd0': 4, 'DrvrDesDir1_Resd1': 5, 'DrvrDesDir1_Resd2': 6, 'DrvrDesDir1_Resd3': 7}
        compute_method = None
        length = 3
        startbit = 59
        byte = 7
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class EngSt1WdStsChks_1_EcmPropSignalIPdu24:
        sig_name = "EngSt1WdStsChks_1_EcmPropSignalIPdu24"
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

    class WhlMotSysTqReq:
        sig_name = "WhlMotSysTqReq"
        sig_start_bit = 11
        update_id_bit = 12
        sig_length = 12
        sig_value_factor = 4.0
        sig_value_offset = -8188.0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 2047
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 11
        bmuws_info = [(1, 0b00001111, 0b11110000, 4, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class EngSt1WdStsEngSt1WdSts_1_EcmPropSignalIPdu24:
        sig_name = "EngSt1WdStsEngSt1WdSts_1_EcmPropSignalIPdu24"
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
        sig_value_table = {'EngSt1_Ini': 0, 'EngSt1_Awake': 1, 'EngSt1_Rdy': 2, 'EngSt1_PreStrtg': 3, 'EngSt1_StrtgInProgs': 4, 'EngSt1_RunngRunng': 5, 'EngSt1_RunngStb': 6, 'EngSt1_RunngStrtgInProgs': 7, 'EngSt1_RunngRemStrtd': 8, 'EngSt1_AftRun': 9}
        compute_method = None
        length = 4
        startbit = 43
        byte = 5
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class EngSt1WdSts_1_EcmPropSignalIPdu24_UB:
        sig_name = "EngSt1WdSts_1_EcmPropSignalIPdu24_UB"
        sig_start_bit = 31
        update_id_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class HvchSts:
        sig_name = "HvchSts"
        sig_start_bit = 7
        update_id_bit = 4
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvCooltHeatrSts_Off': 0, 'HvCooltHeatrSts_LockedUntilNextStart': 1, 'HvCooltHeatrSts_LockedUntilService': 2, 'HvCooltHeatrSts_LockedPermanent': 3, 'HvCooltHeatrSts_Operation': 4, 'HvCooltHeatrSts_Reserved1': 5, 'HvCooltHeatrSts_Reserved2': 6, 'HvCooltHeatrSts_Reserved3': 7}
        compute_method = None
        length = 3
        startbit = 7
        byte = 0
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class EngSt1WdStsCntr_1_EcmPropSignalIPdu24:
        sig_name = "EngSt1WdStsCntr_1_EcmPropSignalIPdu24"
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

    class DrvrDesDirChks:
        sig_name = "DrvrDesDirChks"
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


class EcmPropulsionCANNmFr:
    msg_name = "EcmPropulsionCANNmFr"
    msg_id = 1312
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['HVCM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class BecmPropDevFr01:
    msg_name = "BecmPropDevFr01"
    msg_id = 1472
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['CCM']
    sig_group_dict = {'BECMdevelpsignalgroup1': ['BECMdevelpsignalgroup1Functiondevpsignalgroup1', 'BECMdevelpsignalgroup1Functiondevpsignalgroup2', 'BECMdevelpsignalgroup1Functiondevpsignalgroup3', 'BECMdevelpsignalgroup1Functiondevpsignalgroup4', 'BECMdevelpsignalgroup1Functiondevpsignalgroup5', 'BECMdevelpsignalgroup1Functiondevpsignalgroup6', 'BECMdevelpsignalgroup1Functiondevpsignalgroup7', 'BECMdevelpsignalgroup1Functiondevpsignalgroup8']}
    sig_group_dataid_dict = {}

    class BECMdevelpsignalgroup1Functiondevpsignalgroup1:
        sig_name = "BECMdevelpsignalgroup1Functiondevpsignalgroup1"
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

    class BECMdevelpsignalgroup1Functiondevpsignalgroup7:
        sig_name = "BECMdevelpsignalgroup1Functiondevpsignalgroup7"
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

    class BECMdevelpsignalgroup1Functiondevpsignalgroup4:
        sig_name = "BECMdevelpsignalgroup1Functiondevpsignalgroup4"
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

    class BECMdevelpsignalgroup1Functiondevpsignalgroup2:
        sig_name = "BECMdevelpsignalgroup1Functiondevpsignalgroup2"
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

    class BECMdevelpsignalgroup1Functiondevpsignalgroup6:
        sig_name = "BECMdevelpsignalgroup1Functiondevpsignalgroup6"
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

    class BECMdevelpsignalgroup1Functiondevpsignalgroup8:
        sig_name = "BECMdevelpsignalgroup1Functiondevpsignalgroup8"
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

    class BECMdevelpsignalgroup1Functiondevpsignalgroup3:
        sig_name = "BECMdevelpsignalgroup1Functiondevpsignalgroup3"
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

    class BECMdevelpsignalgroup1Functiondevpsignalgroup5:
        sig_name = "BECMdevelpsignalgroup1Functiondevpsignalgroup5"
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


class EtcSrsPropDevFr01:
    msg_name = "EtcSrsPropDevFr01"
    msg_id = 1457
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CCM"
    rx_nodes = ['SRS']
    sig_group_dict = {'SRSdevelpsignalgroupRX': ['SRSdevelpsignalgroupRXFunctiondevpsignalgroup1', 'SRSdevelpsignalgroupRXFunctiondevpsignalgroup2', 'SRSdevelpsignalgroupRXFunctiondevpsignalgroup3', 'SRSdevelpsignalgroupRXFunctiondevpsignalgroup4', 'SRSdevelpsignalgroupRXFunctiondevpsignalgroup5', 'SRSdevelpsignalgroupRXFunctiondevpsignalgroup6', 'SRSdevelpsignalgroupRXFunctiondevpsignalgroup7', 'SRSdevelpsignalgroupRXFunctiondevpsignalgroup8']}
    sig_group_dataid_dict = {}

    class SRSdevelpsignalgroupRXFunctiondevpsignalgroup3:
        sig_name = "SRSdevelpsignalgroupRXFunctiondevpsignalgroup3"
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

    class SRSdevelpsignalgroupRXFunctiondevpsignalgroup8:
        sig_name = "SRSdevelpsignalgroupRXFunctiondevpsignalgroup8"
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

    class SRSdevelpsignalgroupRXFunctiondevpsignalgroup2:
        sig_name = "SRSdevelpsignalgroupRXFunctiondevpsignalgroup2"
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

    class SRSdevelpsignalgroupRXFunctiondevpsignalgroup5:
        sig_name = "SRSdevelpsignalgroupRXFunctiondevpsignalgroup5"
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

    class SRSdevelpsignalgroupRXFunctiondevpsignalgroup1:
        sig_name = "SRSdevelpsignalgroupRXFunctiondevpsignalgroup1"
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

    class SRSdevelpsignalgroupRXFunctiondevpsignalgroup7:
        sig_name = "SRSdevelpsignalgroupRXFunctiondevpsignalgroup7"
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

    class SRSdevelpsignalgroupRXFunctiondevpsignalgroup4:
        sig_name = "SRSdevelpsignalgroupRXFunctiondevpsignalgroup4"
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

    class SRSdevelpsignalgroupRXFunctiondevpsignalgroup6:
        sig_name = "SRSdevelpsignalgroupRXFunctiondevpsignalgroup6"
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


class VddmPropFr15:
    msg_name = "VddmPropFr15"
    msg_id = 609
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.08
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['BECM1', 'MGM']
    sig_group_dict = {'ImobEngMgrReq3': ['ImobEngMgrReq3ImobEngDataMgrReq0', 'ImobEngMgrReq3ImobEngDataMgrReq1', 'ImobEngMgrReq3ImobEngDataMgrReq2', 'ImobEngMgrReq3ImobEngDataMgrReq3', 'ImobEngMgrReq3ImobEngDataMgrReq4', 'ImobEngMgrReq3ImobEngDataMgrReq5', 'ImobEngMgrReq3ImobEngDataMgrReq6', 'ImobEngMgrReq3ImobEngMgrCmdTar1']}
    sig_group_dataid_dict = {}

    class ImobEngMgrReq3ImobEngDataMgrReq1:
        sig_name = "ImobEngMgrReq3ImobEngDataMgrReq1"
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

    class ImobEngMgrReq3_UB:
        sig_name = "ImobEngMgrReq3_UB"
        sig_start_bit = 2
        update_id_bit = 2
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
        startbit = 2
        byte = 0
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class MaintainBattTCtrl:
        sig_name = "MaintainBattTCtrl"
        sig_start_bit = 3
        update_id_bit = 4
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

    class ImobEngMgrReq3ImobEngDataMgrReq0:
        sig_name = "ImobEngMgrReq3ImobEngDataMgrReq0"
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

    class ImobEngMgrReq3ImobEngDataMgrReq5:
        sig_name = "ImobEngMgrReq3ImobEngDataMgrReq5"
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

    class ImobEngMgrReq3ImobEngDataMgrReq3:
        sig_name = "ImobEngMgrReq3ImobEngDataMgrReq3"
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

    class ImobEngMgrReq3ImobEngMgrCmdTar1:
        sig_name = "ImobEngMgrReq3ImobEngMgrCmdTar1"
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
        sig_value_table = {'ImobEngMgrReqCmd_ImobEngCmdTarIdle': 0, 'ImobEngMgrReqCmd_ImobEngMtnStrtReqCmd': 1, 'ImobEngMgrReqCmd_ImobEngNoMtnStrtReqCmd': 2, 'ImobEngMgrReqCmd_ImobEngTurnOffCmd': 3}
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class ImobEngMgrReq3ImobEngDataMgrReq2:
        sig_name = "ImobEngMgrReq3ImobEngDataMgrReq2"
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

    class ImobEngMgrReq3ImobEngDataMgrReq4:
        sig_name = "ImobEngMgrReq3ImobEngDataMgrReq4"
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

    class ImobEngMgrReq3ImobEngDataMgrReq6:
        sig_name = "ImobEngMgrReq3ImobEngDataMgrReq6"
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


class EcmPropFr11:
    msg_name = "EcmPropFr11"
    msg_id = 647
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.3
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['MGM', 'BECM1', 'IEM', 'HVCM', 'VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class CmptmtCoolgSts:
        sig_name = "CmptmtCoolgSts"
        sig_start_bit = 3
        update_id_bit = 4
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CmptmtCoolgSts_OffNoReq': 0, 'CmptmtCoolgSts_OffByEvaprTLo': 1, 'CmptmtCoolgSts_OffByPLo': 2, 'CmptmtCoolgSts_OffByAmbTOutOfRng': 3, 'CmptmtCoolgSts_OffBySysFailr': 4, 'CmptmtCoolgSts_OffByLoadCut': 5, 'CmptmtCoolgSts_OnWithBattCoolg': 6, 'CmptmtCoolgSts_On': 7}
        compute_method = None
        length = 4
        startbit = 3
        byte = 0
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class ChrgnSts:
        sig_name = "ChrgnSts"
        sig_start_bit = 44
        update_id_bit = 63
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 3
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ChrgnSts_Fault': 0, 'ChrgnSts_ChargingInParkingState': 1, 'ChrgnSts_ChargingInDrivingState': 2, 'ChrgnSts_NotCharging': 3, 'ChrgnSts_ChargingCompleted': 4, 'ChrgnSts_Invalid': 5}
        compute_method = None
        length = 3
        startbit = 44
        byte = 5
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class PrpsnSysActv:
        sig_name = "PrpsnSysActv"
        sig_start_bit = 20
        update_id_bit = 21
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NotCmpl1_NotCmpl': 0, 'NotCmpl1_Cmpl': 1}
        compute_method = None
        length = 1
        startbit = 20
        byte = 2
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class BookChargeSetResponse_1_BgmConnectivitySignalIPdu03:
        sig_name = "BookChargeSetResponse_1_BgmConnectivitySignalIPdu03"
        sig_start_bit = 62
        update_id_bit = 56
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
        startbit = 62
        byte = 7
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class DeactvtTestCom_1_EcmPropSignalIPdu11:
        sig_name = "DeactvtTestCom_1_EcmPropSignalIPdu11"
        sig_start_bit = 60
        update_id_bit = 57
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff2_On': 0, 'OnOff2_Off': 1}
        compute_method = None
        length = 1
        startbit = 60
        byte = 7
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class CooltTSigForDtElec:
        sig_name = "CooltTSigForDtElec"
        sig_start_bit = 39
        update_id_bit = 5
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 1800
        sig_byteorder = "Motorola"
        sig_value_init = 400
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11100000, 0b00011111, 3, 5)]

    class HvConvPwrAllwd:
        sig_name = "HvConvPwrAllwd"
        sig_start_bit = 15
        update_id_bit = 7
        sig_length = 10
        sig_value_factor = 20.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 1023
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 15
        bmuws_info = [(1, 0b11111111, 0b00000000, 8, 0), (2, 0b11000000, 0b00111111, 2, 6)]

    class CooltFlowForDtElec:
        sig_name = "CooltFlowForDtElec"
        sig_start_bit = 41
        update_id_bit = 6
        sig_length = 9
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 41
        bmuws_info = [(5, 0b00000011, 0b11111100, 2, 0), (6, 0b11111110, 0b00000001, 7, 1)]


class VgmToMgmJ1979OBDPropCanReqFrame11:
    msg_name = "VgmToMgmJ1979OBDPropCanReqFrame11"
    msg_id = 2020
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['MGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class BecmPropFr30:
    msg_name = "BecmPropFr30"
    msg_id = 1144
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 1.0
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class TotDchaEgy:
        sig_name = "TotDchaEgy"
        sig_start_bit = 7
        update_id_bit = 39
        sig_length = 32
        sig_value_factor = 1.0
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


class EgsmToVddmPropDiagRespFrame:
    msg_name = "EgsmToVddmPropDiagRespFrame"
    msg_id = 1587
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "EGSM"
    rx_nodes = ['VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class EtcToVddmDevelFr:
    msg_name = "EtcToVddmDevelFr"
    msg_id = 1513
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CCM"
    rx_nodes = ['VDDM']
    sig_group_dict = {'VDDMPropCANInternalDevReqMesg': ['VDDMPropCANInternalDevReqMesgFunctiondevpsignalgroup1', 'VDDMPropCANInternalDevReqMesgFunctiondevpsignalgroup2', 'VDDMPropCANInternalDevReqMesgFunctiondevpsignalgroup3', 'VDDMPropCANInternalDevReqMesgFunctiondevpsignalgroup4', 'VDDMPropCANInternalDevReqMesgFunctiondevpsignalgroup5', 'VDDMPropCANInternalDevReqMesgFunctiondevpsignalgroup6', 'VDDMPropCANInternalDevReqMesgFunctiondevpsignalgroup7', 'VDDMPropCANInternalDevReqMesgFunctiondevpsignalgroup8']}
    sig_group_dataid_dict = {}

    class VDDMPropCANInternalDevReqMesgFunctiondevpsignalgroup5:
        sig_name = "VDDMPropCANInternalDevReqMesgFunctiondevpsignalgroup5"
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

    class VDDMPropCANInternalDevReqMesgFunctiondevpsignalgroup6:
        sig_name = "VDDMPropCANInternalDevReqMesgFunctiondevpsignalgroup6"
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

    class VDDMPropCANInternalDevReqMesgFunctiondevpsignalgroup4:
        sig_name = "VDDMPropCANInternalDevReqMesgFunctiondevpsignalgroup4"
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

    class VDDMPropCANInternalDevReqMesgFunctiondevpsignalgroup8:
        sig_name = "VDDMPropCANInternalDevReqMesgFunctiondevpsignalgroup8"
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

    class VDDMPropCANInternalDevReqMesgFunctiondevpsignalgroup2:
        sig_name = "VDDMPropCANInternalDevReqMesgFunctiondevpsignalgroup2"
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

    class VDDMPropCANInternalDevReqMesgFunctiondevpsignalgroup1:
        sig_name = "VDDMPropCANInternalDevReqMesgFunctiondevpsignalgroup1"
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

    class VDDMPropCANInternalDevReqMesgFunctiondevpsignalgroup3:
        sig_name = "VDDMPropCANInternalDevReqMesgFunctiondevpsignalgroup3"
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

    class VDDMPropCANInternalDevReqMesgFunctiondevpsignalgroup7:
        sig_name = "VDDMPropCANInternalDevReqMesgFunctiondevpsignalgroup7"
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


class EcmPropFr01:
    msg_name = "EcmPropFr01"
    msg_id = 80
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['MGM', 'VDDM']
    sig_group_dict = {'AccrPedlLnr': ['AccrPedlLnrAccrPedlRat', 'AccrPedlLnrChks', 'AccrPedlLnrCntr']}
    sig_group_dataid_dict = {'AccrPedlLnr': 707}

    class AccrPedlLnrCntr:
        sig_name = "AccrPedlLnrCntr"
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

    class AccrPedlLnrAccrPedlRat:
        sig_name = "AccrPedlLnrAccrPedlRat"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 0.00390625
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 25600
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111110, 0b00000001, 7, 1)]

    class AccrPedlLnr_UB:
        sig_name = "AccrPedlLnr_UB"
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

    class IsgTqReq:
        sig_name = "IsgTqReq"
        sig_start_bit = 5
        update_id_bit = 6
        sig_length = 14
        sig_value_factor = 1.0
        sig_value_offset = -8188.0
        sig_value_min = 0
        sig_value_max = 16380
        sig_byteorder = "Motorola"
        sig_value_init = 8188
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 14
        startbit = 5
        bmuws_info = [(0, 0b00111111, 0b11000000, 6, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class AccrPedlLnrChks:
        sig_name = "AccrPedlLnrChks"
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

    class PrpsnTqFrntReq:
        sig_name = "PrpsnTqFrntReq"
        sig_start_bit = 55
        update_id_bit = 7
        sig_length = 16
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = -20000
        sig_value_max = 20000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 55
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111111, 0b00000000, 8, 0)]


class VddmPropFr11:
    msg_name = "VddmPropFr11"
    msg_id = 313
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.025
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['BECM1', 'IEM', 'ECM']
    sig_group_dict = {'LockgCenSts': ['LockgCenStsLockSt', 'LockgCenStsTrigSrc', 'LockgCenStsUpdEve'], 'BrkFricTqTotAtWhlsAct': ['BrkFricTqTotAtWhlsActBrkFricTqTotAtWhlsAct', 'BrkFricTqTotAtWhlsActChks', 'BrkFricTqTotAtWhlsActCntr']}
    sig_group_dataid_dict = {'BrkFricTqTotAtWhlsAct': 123}

    class YawStabyCtrlActv:
        sig_name = "YawStabyCtrlActv"
        sig_start_bit = 27
        update_id_bit = 26
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CtrlSts1_NoCtrl': 0, 'CtrlSts1_InCtrl': 1}
        compute_method = None
        length = 1
        startbit = 27
        byte = 3
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class SpdRotlForWhlsAtAxleRe:
        sig_name = "SpdRotlForWhlsAtAxleRe"
        sig_start_bit = 38
        update_id_bit = 39
        sig_length = 15
        sig_value_factor = 0.5
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 32767
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 38
        bmuws_info = [(4, 0b01111111, 0b10000000, 7, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class LockgCenStsUpdEve:
        sig_name = "LockgCenStsUpdEve"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 49
        byte = 6
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class BrkFricTqTotAtWhlsActBrkFricTqTotAtWhlsAct:
        sig_name = "BrkFricTqTotAtWhlsActBrkFricTqTotAtWhlsAct"
        sig_start_bit = 6
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 20000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 6
        bmuws_info = [(0, 0b01111111, 0b10000000, 7, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class LockgCenStsLockSt:
        sig_name = "LockgCenStsLockSt"
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
        sig_value_table = {'LockSt3_LockUndefd': 0, 'LockSt3_LockUnlckd': 1, 'LockSt3_LockTrUnlckd': 2, 'LockSt3_LockLockd': 3}
        compute_method = None
        length = 2
        startbit = 51
        byte = 6
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class BrkFricTqTotAtWhlsActChks:
        sig_name = "BrkFricTqTotAtWhlsActChks"
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

    class BrkFricTqTotAtWhlsActCntr:
        sig_name = "BrkFricTqTotAtWhlsActCntr"
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

    class LockgCenSts_UB:
        sig_name = "LockgCenSts_UB"
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

    class BrkFricTqTotAtWhlsAct_UB:
        sig_name = "BrkFricTqTotAtWhlsAct_UB"
        sig_start_bit = 7
        update_id_bit = 7
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
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class LockgCenStsTrigSrc:
        sig_name = "LockgCenStsTrigSrc"
        sig_start_bit = 55
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 12
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LockTrigSrc2_NoTrigSrc': 0, 'LockTrigSrc2_KeyRem': 1, 'LockTrigSrc2_Keyls': 2, 'LockTrigSrc2_IntrSwt': 3, 'LockTrigSrc2_SpdAut': 4, 'LockTrigSrc2_TmrAut': 5, 'LockTrigSrc2_Slam': 6, 'LockTrigSrc2_Telm': 7, 'LockTrigSrc2_Crash': 8, 'LockTrigSrc2_Apprch': 9, 'LockTrigSrc2_OutsOth': 10, 'LockTrigSrc2_InsOth': 11, 'Locktrigsrc2_NFC': 12}
        compute_method = None
        length = 4
        startbit = 55
        byte = 6
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4


class VddmToAllPropDiagReqFrame:
    msg_name = "VddmToAllPropDiagReqFrame"
    msg_id = 2047
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['MGM', 'BECM1', 'EGSM', 'IEM', 'HVCM', 'ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class VgmToVddmJ1979OBDPropCanReqFrame11:
    msg_name = "VgmToVddmJ1979OBDPropCanReqFrame11"
    msg_id = 2022
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class MgmPropFr08:
    msg_name = "MgmPropFr08"
    msg_id = 550
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.08
    msg_length = 8
    tx_node = "MGM"
    rx_nodes = ['ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class IsgHeatPwrMax:
        sig_name = "IsgHeatPwrMax"
        sig_start_bit = 7
        update_id_bit = 13
        sig_length = 8
        sig_value_factor = 50.0
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

    class IsgHeatFdBck:
        sig_name = "IsgHeatFdBck"
        sig_start_bit = 15
        update_id_bit = 12
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'IsgHeatFdBck_On': 0, 'IsgHeatFdBck_Off': 1, 'IsgHeatFdBck_Inhibt': 2, 'IsgHeatFdBck_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 15
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class EgsmPropulsionCANNmFr:
    msg_name = "EgsmPropulsionCANNmFr"
    msg_id = 1302
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "EGSM"
    rx_nodes = ['ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class VgmPropFr01:
    msg_name = "VgmPropFr01"
    msg_id = 786
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.6
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class OnBdDiagLostCom:
        sig_name = "OnBdDiagLostCom"
        sig_start_bit = 6
        update_id_bit = 7
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
        startbit = 6
        byte = 0
        mask = 0b01111000
        unmask = 0b10000111
        shift = 3


class EcmPropFr08:
    msg_name = "EcmPropFr08"
    msg_id = 369
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['MGM', 'BECM1', 'IEM', 'HVCM', 'VDDM']
    sig_group_dict = {'EngT_0_EcmPropSignalIPdu08': ['EngTEngT_0_EcmPropSignalIPdu08', 'EngTQf_0_EcmPropSignalIPdu08']}
    sig_group_dataid_dict = {}

    class HvOnMaiReq:
        sig_name = "HvOnMaiReq"
        sig_start_bit = 60
        update_id_bit = 58
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
        startbit = 60
        byte = 7
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class HvBattCoolgCmd:
        sig_name = "HvBattCoolgCmd"
        sig_start_bit = 63
        update_id_bit = 61
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HVBattChargnCmd_OK': 0, 'HVBattChargnCmd_NOK': 1, 'HVBattChargnCmd_INIT': 2, 'HVBattChargnCmd_HOLD': 3}
        compute_method = None
        length = 2
        startbit = 63
        byte = 7
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class EngTEngT_0_EcmPropSignalIPdu08:
        sig_name = "EngTEngT_0_EcmPropSignalIPdu08"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -50.0
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Motorola"
        sig_value_init = 50
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class PrpsnFbLimnIndcn:
        sig_name = "PrpsnFbLimnIndcn"
        sig_start_bit = 22
        update_id_bit = 23
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
        startbit = 22
        byte = 2
        mask = 0b01111000
        unmask = 0b10000111
        shift = 3

    class IsgActvDampgModReq:
        sig_name = "IsgActvDampgModReq"
        sig_start_bit = 39
        update_id_bit = 37
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WhlMotSysActvDampgModCodSts_NoDampg': 0, 'WhlMotSysActvDampgModCodSts_LoDampg': 1, 'WhlMotSysActvDampgModCodSts_MedDampg': 2, 'WhlMotSysActvDampgModCodSts_HiDampg': 3}
        compute_method = None
        length = 2
        startbit = 39
        byte = 4
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class EngT_0_EcmPropSignalIPdu08_UB:
        sig_name = "EngT_0_EcmPropSignalIPdu08_UB"
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

    class EngTQf_0_EcmPropSignalIPdu08:
        sig_name = "EngTQf_0_EcmPropSignalIPdu08"
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
        sig_value_table = {'Qf1_DevOfDataUndefd': 0, 'Qf1_DataTmpUndefdAndEvlnInProgs': 1, 'Qf1_DevOfDataNotWithinRngAllwd': 2, 'Qf1_DataCalcdWithDevDefd': 3}
        compute_method = None
        length = 2
        startbit = 33
        byte = 4
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0


class EcmPropFr09:
    msg_name = "EcmPropFr09"
    msg_id = 406
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.07
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['BECM1', 'VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HvBattChrgnCmd:
        sig_name = "HvBattChrgnCmd"
        sig_start_bit = 52
        update_id_bit = 53
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HVBattChargnCmd_OK': 0, 'HVBattChargnCmd_NOK': 1, 'HVBattChargnCmd_INIT': 2, 'HVBattChargnCmd_HOLD': 3}
        compute_method = None
        length = 2
        startbit = 52
        byte = 6
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class ChrgnOrDisChrgnStsFb:
        sig_name = "ChrgnOrDisChrgnStsFb"
        sig_start_bit = 29
        update_id_bit = 24
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 30
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ChrgnSts2_default': 0, 'ChrgnSts2_NoCharging': 1, 'ChrgnSts2_ACCharging': 2, 'ChrgnSts2_ACChargingEnd': 3, 'ChrgnSts2_ChargingCmpl': 4, 'ChrgnSts2_Heating': 5, 'ChrgnSts2_Booking': 6, 'ChrgnSts2_NoDischaring': 7, 'ChrgnSts2_Discharging': 8, 'ChrgnSts2_DischargingEnd': 9, 'ChrgnSts2_DischargingCmpl': 10, 'ChrgnSts2_Chargingfalut': 11, 'ChrgnSts2_DischargingFalut': 12, 'ChrgnSts2_ACChrgnFltChrgrSide': 14, 'ChrgnSts2_DCCharging': 15, 'ChrgnSts2_DCChrgnFltVehSide': 18, 'ChrgnSts2_DCChrgnFltChrgrSideTempFlt': 19, 'ChrgnSts2_DCChrgnFltChrgrSideConFlt': 20, 'ChrgnSts2_DCChrgnFltChrgrSideHwFlt': 21, 'ChrgnSts2_DCChrgnFltChrgrSideEmgyFlt': 22, 'ChrgnSts2_DCChrgnFltChrgrSideComFlt': 23, 'ChrgnSts2_SuperCharging': 24, 'ChrgnSts2_ACChargingSuspend': 25, 'ChrgnSts2_DCChargingEnd': 26, 'ChrgnSts2_ACChrgnFltVehSide': 27, 'ChrgnSts2_Boostcharging': 28, 'ChrgnSts2_BoostchargingFlt': 29, 'ChrgnSts2_WirelessCharging': 30}
        compute_method = None
        length = 5
        startbit = 29
        byte = 3
        mask = 0b00111110
        unmask = 0b11000001
        shift = 1

    class ObdAccrPedRat:
        sig_name = "ObdAccrPedRat"
        sig_start_bit = 63
        update_id_bit = 54
        sig_length = 8
        sig_value_factor = 0.3921568628
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


class IemPropFr07:
    msg_name = "IemPropFr07"
    msg_id = 643
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.15
    msg_length = 8
    tx_node = "IEM"
    rx_nodes = ['ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class WhlMotCooltFlowMinReq:
        sig_name = "WhlMotCooltFlowMinReq"
        sig_start_bit = 1
        update_id_bit = 54
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 1
        bmuws_info = [(0, 0b00000011, 0b11111100, 2, 0), (1, 0b11111111, 0b00000000, 8, 0)]


class BecmPropFr24:
    msg_name = "BecmPropFr24"
    msg_id = 656
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['S2SReceiver', 'VDDM']
    sig_group_dict = {'HvBattCellTInfo': ['HvBattCellTInfoHvBattSnsrT', 'HvBattCellTInfoHvBattTMax', 'HvBattCellTInfoHvBattTMin', 'HvBattCellTInfoHvBattTSnsrNr', 'HvBattCellTInfoHvTempSnsrTMaxsSerlNr', 'HvBattCellTInfoHvTempSnsrTMinSerlNr']}
    sig_group_dataid_dict = {}

    class HvBattCellTInfo_UB:
        sig_name = "HvBattCellTInfo_UB"
        sig_start_bit = 55
        update_id_bit = 55
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
        startbit = 55
        byte = 6
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class HvBattOptmzHint:
        sig_name = "HvBattOptmzHint"
        sig_start_bit = 53
        update_id_bit = 54
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
        startbit = 53
        byte = 6
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class LocalHvBattThermReqFb:
        sig_name = "LocalHvBattThermReqFb"
        sig_start_bit = 63
        update_id_bit = 56
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LocalHvBattThermReqFb_Idle': 0, 'LocalHvBattThermReqFb_Cooling': 1, 'LocalHvBattThermReqFb_Heating': 2, 'LocalHvBattThermReqFb_Erro': 3}
        compute_method = None
        length = 2
        startbit = 63
        byte = 7
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HvBattCellTInfoHvTempSnsrTMaxsSerlNr:
        sig_name = "HvBattCellTInfoHvTempSnsrTMaxsSerlNr"
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

    class HvBattCellTInfoHvBattTMin:
        sig_name = "HvBattCellTInfoHvBattTMin"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 40
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 23
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvBattCellTInfoHvBattSnsrT:
        sig_name = "HvBattCellTInfoHvBattSnsrT"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 40
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvBattCellTInfoHvTempSnsrTMinSerlNr:
        sig_name = "HvBattCellTInfoHvTempSnsrTMinSerlNr"
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

    class HvBattCellTInfoHvBattTSnsrNr:
        sig_name = "HvBattCellTInfoHvBattTSnsrNr"
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

    class HvBattCellTInfoHvBattTMax:
        sig_name = "HvBattCellTInfoHvBattTMax"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 40
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class VgmToEcmJ1979OBDPropCanReqFrame11:
    msg_name = "VgmToEcmJ1979OBDPropCanReqFrame11"
    msg_id = 2016
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class BecmPropFr16:
    msg_name = "BecmPropFr16"
    msg_id = 833
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 1.0
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['VDDM', 'ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class TotChrgEgy:
        sig_name = "TotChrgEgy"
        sig_start_bit = 39
        update_id_bit = 20
        sig_length = 32
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 4294967295
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 32
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class HvBattClrRdyReq:
        sig_name = "HvBattClrRdyReq"
        sig_start_bit = 18
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
        startbit = 18
        byte = 2
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class HvBattHeatgEgyReq:
        sig_name = "HvBattHeatgEgyReq"
        sig_start_bit = 17
        update_id_bit = 7
        sig_length = 10
        sig_value_factor = 20.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 17
        bmuws_info = [(2, 0b00000011, 0b11111100, 2, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class HvBattClimaPwr:
        sig_name = "HvBattClimaPwr"
        sig_start_bit = 2
        update_id_bit = 3
        sig_length = 11
        sig_value_factor = 100.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 2
        bmuws_info = [(0, 0b00000111, 0b11111000, 3, 0), (1, 0b11111111, 0b00000000, 8, 0)]


class BecmPropFr04:
    msg_name = "BecmPropFr04"
    msg_id = 659
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.4
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['VDDM', 'ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HvBattSocLimHi:
        sig_name = "HvBattSocLimHi"
        sig_start_bit = 42
        update_id_bit = 43
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
        startbit = 42
        bmuws_info = [(5, 0b00000111, 0b11111000, 3, 0), (6, 0b11111111, 0b00000000, 8, 0)]

    class HvBattSocLimLo:
        sig_name = "HvBattSocLimLo"
        sig_start_bit = 39
        update_id_bit = 44
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
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11100000, 0b00011111, 3, 5)]

    class HvBattHeatgReq:
        sig_name = "HvBattHeatgReq"
        sig_start_bit = 7
        update_id_bit = 5
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvBattCoolgReq_NotReqd': 0, 'HvBattCoolgReq_LoReq': 1, 'HvBattCoolgReq_MedReq': 2, 'HvBattCoolgReq_HiReq': 3}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HvBattSocLimMax:
        sig_name = "HvBattSocLimMax"
        sig_start_bit = 18
        update_id_bit = 19
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
        startbit = 18
        bmuws_info = [(2, 0b00000111, 0b11111000, 3, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class HvBattErrIndcnReq:
        sig_name = "HvBattErrIndcnReq"
        sig_start_bit = 21
        update_id_bit = 22
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

    class HvBattEgyCdn:
        sig_name = "HvBattEgyCdn"
        sig_start_bit = 63
        update_id_bit = 20
        sig_length = 8
        sig_value_factor = 0.5
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 200
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

    class HvBattSocLimMin:
        sig_name = "HvBattSocLimMin"
        sig_start_bit = 2
        update_id_bit = 23
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
        startbit = 2
        bmuws_info = [(0, 0b00000111, 0b11111000, 3, 0), (1, 0b11111111, 0b00000000, 8, 0)]


class BgmPropulsionFr05:
    msg_name = "BgmPropulsionFr05"
    msg_id = 42
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['BECM1']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class ChrgSoftSwCtrlSt:
        sig_name = "ChrgSoftSwCtrlSt"
        sig_start_bit = 7
        update_id_bit = 4
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
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class IemPropFr06:
    msg_name = "IemPropFr06"
    msg_id = 626
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "IEM"
    rx_nodes = ['ECM', 'VDDM']
    sig_group_dict = {'IemGeneric': ['IemGenericADAlrmSt', 'IemGenericDTCHig', 'IemGenericDTCLow', 'IemGenericDTCMid', 'IemGenericDTCSts', 'IemGenericEMQnty', 'IemGenericEMSeqNr', 'IemGenericFltAlrmSt', 'IemGenericIacAlrmSt', 'IemGenericInvrtTAlrmSt', 'IemGenericModStatusRms', 'IemGenericMotTAlrmSt', 'IemGenericRslAlrmSt', 'IemGenericSpdAlrmSt', 'IemGenericTypeInfo', 'IemGenericUDcAlrmSt']}
    sig_group_dataid_dict = {}

    class IemGenericInvrtTAlrmSt:
        sig_name = "IemGenericInvrtTAlrmSt"
        sig_start_bit = 49
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSt_Disarmd': 0, 'AlrmSt_Armd': 1, 'AlrmSt_Actv': 2}
        compute_method = None
        length = 2
        startbit = 49
        byte = 6
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class IemGenericDTCSts:
        sig_name = "IemGenericDTCSts"
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

    class IemGenericDTCMid:
        sig_name = "IemGenericDTCMid"
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

    class IemGenericDTCHig:
        sig_name = "IemGenericDTCHig"
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

    class IemGenericADAlrmSt:
        sig_name = "IemGenericADAlrmSt"
        sig_start_bit = 55
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSt_Disarmd': 0, 'AlrmSt_Armd': 1, 'AlrmSt_Actv': 2}
        compute_method = None
        length = 2
        startbit = 55
        byte = 6
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class IemGenericSpdAlrmSt:
        sig_name = "IemGenericSpdAlrmSt"
        sig_start_bit = 59
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSt_Disarmd': 0, 'AlrmSt_Armd': 1, 'AlrmSt_Actv': 2}
        compute_method = None
        length = 2
        startbit = 59
        byte = 7
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class IemGenericEMSeqNr:
        sig_name = "IemGenericEMSeqNr"
        sig_start_bit = 35
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
        startbit = 35
        byte = 4
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class IemGenericTypeInfo:
        sig_name = "IemGenericTypeInfo"
        sig_start_bit = 43
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
        startbit = 43
        byte = 5
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class IemGenericEMQnty:
        sig_name = "IemGenericEMQnty"
        sig_start_bit = 39
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
        startbit = 39
        byte = 4
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class IemGenericFltAlrmSt:
        sig_name = "IemGenericFltAlrmSt"
        sig_start_bit = 53
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSt_Disarmd': 0, 'AlrmSt_Armd': 1, 'AlrmSt_Actv': 2}
        compute_method = None
        length = 2
        startbit = 53
        byte = 6
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class IemGenericModStatusRms:
        sig_name = "IemGenericModStatusRms"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 3
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ModStatusRms_Invalid': 0, 'PModStatusRms_wrCns': 1, 'ModStatusRms_PwrGen': 2, 'ModStatusRms_OffSts': 3, 'ModStatusRms_RdySts': 4, 'ModStatusRms_Abnormal': 5, 'ModStatusRms_Invalid1': 6, 'ModStatusRms_Invalid2': 7, 'ModStatusRms_Invalid3': 8, 'ModStatusRms_Invalid4': 9, 'ModStatusRms_Invalid5': 10, 'ModStatusRms_Invalid6': 11, 'ModStatusRms_Invalid7': 12, 'ModStatusRms_Invalid8': 13, 'ModStatusRms_Invalid9': 14, 'ModStatusRms_Invalid10': 15}
        compute_method = None
        length = 4
        startbit = 47
        byte = 5
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class IemGenericUDcAlrmSt:
        sig_name = "IemGenericUDcAlrmSt"
        sig_start_bit = 57
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSt_Disarmd': 0, 'AlrmSt_Armd': 1, 'AlrmSt_Actv': 2}
        compute_method = None
        length = 2
        startbit = 57
        byte = 7
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class IemGenericRslAlrmSt:
        sig_name = "IemGenericRslAlrmSt"
        sig_start_bit = 61
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSt_Disarmd': 0, 'AlrmSt_Armd': 1, 'AlrmSt_Actv': 2}
        compute_method = None
        length = 2
        startbit = 61
        byte = 7
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class IemGenericIacAlrmSt:
        sig_name = "IemGenericIacAlrmSt"
        sig_start_bit = 51
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSt_Disarmd': 0, 'AlrmSt_Armd': 1, 'AlrmSt_Actv': 2}
        compute_method = None
        length = 2
        startbit = 51
        byte = 6
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class IemGenericMotTAlrmSt:
        sig_name = "IemGenericMotTAlrmSt"
        sig_start_bit = 63
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSt_Disarmd': 0, 'AlrmSt_Armd': 1, 'AlrmSt_Actv': 2}
        compute_method = None
        length = 2
        startbit = 63
        byte = 7
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class IemGenericDTCLow:
        sig_name = "IemGenericDTCLow"
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


class VddmPropFr17:
    msg_name = "VddmPropFr17"
    msg_id = 354
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['MGM', 'BECM1', 'EGSM', 'IEM', 'HVCM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class CarTiGlb_0_BgmADCANFDSignalIPdu04:
        sig_name = "CarTiGlb_0_BgmADCANFDSignalIPdu04"
        sig_start_bit = 7
        update_id_bit = 39
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

    class BattProtectSwt:
        sig_name = "BattProtectSwt"
        sig_start_bit = 59
        update_id_bit = 57
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
        startbit = 59
        byte = 7
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2


class EgsmPropFr02:
    msg_name = "EgsmPropFr02"
    msg_id = 310
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "EGSM"
    rx_nodes = ['ECM', 'VDDM']
    sig_group_dict = {'DrvrGearShiftDirReq2': ['DrvrGearShiftDirReq2Chks', 'DrvrGearShiftDirReq2Cntr', 'DrvrGearShiftDirReq2DwnDwnTipAut', 'DrvrGearShiftDirReq2DwnTipAut', 'DrvrGearShiftDirReq2PosnAut', 'DrvrGearShiftDirReq2UpTipAut', 'DrvrGearShiftDirReq2UpUpTipAut'], 'DrvrGearShiftDirReq1': ['DrvrGearShiftDirReq1Chks', 'DrvrGearShiftDirReq1Cntr', 'DrvrGearShiftDirReq1DwnDwnTipAut', 'DrvrGearShiftDirReq1DwnTipAut', 'DrvrGearShiftDirReq1PosnAut', 'DrvrGearShiftDirReq1UpTipAut', 'DrvrGearShiftDirReq1UpUpTipAut']}
    sig_group_dataid_dict = {'DrvrGearShiftDirReq2': 98, 'DrvrGearShiftDirReq1': 57}

    class DrvrGearShiftDirReq2DwnTipAut:
        sig_name = "DrvrGearShiftDirReq2DwnTipAut"
        sig_start_bit = 37
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DwnTipAut1_DwnTipAutNotActv': 0, 'DwnTipAut1_DwnTipAutActv': 1}
        compute_method = None
        length = 1
        startbit = 37
        byte = 4
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class DrvrGearShiftDirReq2Chks:
        sig_name = "DrvrGearShiftDirReq2Chks"
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

    class DrvrGearShiftDirReq2PosnAut:
        sig_name = "DrvrGearShiftDirReq2PosnAut"
        sig_start_bit = 38
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PosnAut_PosnAutNotActv': 0, 'PosnAut_PosnAutActv': 1}
        compute_method = None
        length = 1
        startbit = 38
        byte = 4
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class DrvrGearShiftDirReq1UpTipAut:
        sig_name = "DrvrGearShiftDirReq1UpTipAut"
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
        sig_value_table = {'UpTipAut1_UpTipAutNotActv': 0, 'UpTipAut1_UpTipAutActv': 1}
        compute_method = None
        length = 1
        startbit = 15
        byte = 1
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class DrvrGearShiftDirReq1DwnDwnTipAut:
        sig_name = "DrvrGearShiftDirReq1DwnDwnTipAut"
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
        sig_value_table = {'NotActvActv1_NotActv': 0, 'NotActvActv1_Actv': 1}
        compute_method = None
        length = 1
        startbit = 12
        byte = 1
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class DrvrGearShiftDirReq1Chks:
        sig_name = "DrvrGearShiftDirReq1Chks"
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

    class DrvrGearShiftDirReq2UpTipAut:
        sig_name = "DrvrGearShiftDirReq2UpTipAut"
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
        sig_value_table = {'UpTipAut1_UpTipAutNotActv': 0, 'UpTipAut1_UpTipAutActv': 1}
        compute_method = None
        length = 1
        startbit = 39
        byte = 4
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class DrvrGearShiftDirReq2_UB:
        sig_name = "DrvrGearShiftDirReq2_UB"
        sig_start_bit = 25
        update_id_bit = 25
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
        startbit = 25
        byte = 3
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class DrvrGearShiftDirReq1_UB:
        sig_name = "DrvrGearShiftDirReq1_UB"
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

    class DrvrGearShiftDirReq1DwnTipAut:
        sig_name = "DrvrGearShiftDirReq1DwnTipAut"
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
        sig_value_table = {'DwnTipAut1_DwnTipAutNotActv': 0, 'DwnTipAut1_DwnTipAutActv': 1}
        compute_method = None
        length = 1
        startbit = 13
        byte = 1
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class DrvrGearShiftDirReq1PosnAut:
        sig_name = "DrvrGearShiftDirReq1PosnAut"
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
        sig_value_table = {'PosnAut_PosnAutNotActv': 0, 'PosnAut_PosnAutActv': 1}
        compute_method = None
        length = 1
        startbit = 14
        byte = 1
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class DrvrGearShiftDirReq1Cntr:
        sig_name = "DrvrGearShiftDirReq1Cntr"
        sig_start_bit = 11
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
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DrvrGearShiftDirReq2UpUpTipAut:
        sig_name = "DrvrGearShiftDirReq2UpUpTipAut"
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
        sig_value_table = {'NotActvActv1_NotActv': 0, 'NotActvActv1_Actv': 1}
        compute_method = None
        length = 1
        startbit = 24
        byte = 3
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class DrvrGearShiftDirReq1UpUpTipAut:
        sig_name = "DrvrGearShiftDirReq1UpUpTipAut"
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
        sig_value_table = {'NotActvActv1_NotActv': 0, 'NotActvActv1_Actv': 1}
        compute_method = None
        length = 1
        startbit = 0
        byte = 0
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class DrvrGearShiftDirReq2DwnDwnTipAut:
        sig_name = "DrvrGearShiftDirReq2DwnDwnTipAut"
        sig_start_bit = 36
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NotActvActv1_NotActv': 0, 'NotActvActv1_Actv': 1}
        compute_method = None
        length = 1
        startbit = 36
        byte = 4
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class DrvrGearShiftDirReq2Cntr:
        sig_name = "DrvrGearShiftDirReq2Cntr"
        sig_start_bit = 35
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
        startbit = 35
        byte = 4
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0


class IemToVgmJ1979OBDPropDiagResFrame11:
    msg_name = "IemToVgmJ1979OBDPropDiagResFrame11"
    msg_id = 2027
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "IEM"
    rx_nodes = ['BGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class VddmPropFr08:
    msg_name = "VddmPropFr08"
    msg_id = 65
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['MGM', 'IEM', 'ECM']
    sig_group_dict = {'PtTqAtAxleMaxReq': ['PtTqAtAxleMaxReqChks', 'PtTqAtAxleMaxReqCntr', 'PtTqAtAxleMaxReqPtTqAtAxleFrntReq', 'PtTqAtAxleMaxReqPtTqAtAxleReReq']}
    sig_group_dataid_dict = {'PtTqAtAxleMaxReq': 1109}

    class PtTqAtAxleMaxReqCntr:
        sig_name = "PtTqAtAxleMaxReqCntr"
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

    class PtTqAtAxleMaxReqPtTqAtAxleFrntReq:
        sig_name = "PtTqAtAxleMaxReqPtTqAtAxleFrntReq"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = -20000
        sig_value_max = 20000
        sig_byteorder = "Motorola"
        sig_value_init = 20000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class PtTqAtAxleMaxReqChks:
        sig_name = "PtTqAtAxleMaxReqChks"
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

    class BrkTqAtWhlsReq:
        sig_name = "BrkTqAtWhlsReq"
        sig_start_bit = 7
        update_id_bit = 11
        sig_length = 12
        sig_value_factor = 4.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11110000, 0b00001111, 4, 4)]

    class PtTqAtAxleMaxReq_UB:
        sig_name = "PtTqAtAxleMaxReq_UB"
        sig_start_bit = 20
        update_id_bit = 20
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
        startbit = 20
        byte = 2
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class PtTqAtAxleMaxReqPtTqAtAxleReReq:
        sig_name = "PtTqAtAxleMaxReqPtTqAtAxleReReq"
        sig_start_bit = 55
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = -20000
        sig_value_max = 20000
        sig_byteorder = "Motorola"
        sig_value_init = 20000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 55
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111111, 0b00000000, 8, 0)]


class IemPropFr04:
    msg_name = "IemPropFr04"
    msg_id = 613
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.08
    msg_length = 8
    tx_node = "IEM"
    rx_nodes = ['VDDM']
    sig_group_dict = {'ImobEngChk2': ['ImobEngChk2ImobEngChkSts', 'ImobEngChk2ImobEngDataChk0', 'ImobEngChk2ImobEngDataChk1', 'ImobEngChk2ImobEngDataChk2', 'ImobEngChk2ImobEngDataChk3', 'ImobEngChk2ImobEngDataChk4', 'ImobEngChk2ImobEngDataChk5', 'ImobEngChk2ImobEngDataChk6']}
    sig_group_dataid_dict = {}

    class ImobEngChk2ImobEngDataChk4:
        sig_name = "ImobEngChk2ImobEngDataChk4"
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

    class ImobEngChk2ImobEngDataChk0:
        sig_name = "ImobEngChk2ImobEngDataChk0"
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

    class ImobEngChk2ImobEngDataChk6:
        sig_name = "ImobEngChk2ImobEngDataChk6"
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

    class ImobEngChk2ImobEngDataChk1:
        sig_name = "ImobEngChk2ImobEngDataChk1"
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

    class ImobEngChk2ImobEngChkSts:
        sig_name = "ImobEngChk2ImobEngChkSts"
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
        sig_value_table = {'AvlSts2_NotAvl': 0, 'AvlSts2_Avl': 1}
        compute_method = None
        length = 1
        startbit = 0
        byte = 0
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ImobEngChk2ImobEngDataChk3:
        sig_name = "ImobEngChk2ImobEngDataChk3"
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

    class ImobEngChk2_UB:
        sig_name = "ImobEngChk2_UB"
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

    class ImobEngChk2ImobEngDataChk5:
        sig_name = "ImobEngChk2ImobEngDataChk5"
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

    class ImobEngChk2ImobEngDataChk2:
        sig_name = "ImobEngChk2ImobEngDataChk2"
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


class EcmPropFr05:
    msg_name = "EcmPropFr05"
    msg_id = 132
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.025
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['MGM', 'BECM1', 'IEM', 'VDDM']
    sig_group_dict = {'WhlMotSysTqAllwd': ['WhlMotSysTqAllwdChks', 'WhlMotSysTqAllwdCntr', 'WhlMotSysTqAllwdWhlMotSysTqAllwd']}
    sig_group_dataid_dict = {'WhlMotSysTqAllwd': 79}

    class WhlMotSysTqAllwdCntr:
        sig_name = "WhlMotSysTqAllwdCntr"
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

    class IsgPwrLimMin:
        sig_name = "IsgPwrLimMin"
        sig_start_bit = 31
        update_id_bit = 37
        sig_length = 10
        sig_value_factor = 0.5
        sig_value_offset = -511.0
        sig_value_min = 0
        sig_value_max = 1022
        sig_byteorder = "Motorola"
        sig_value_init = 1022
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11000000, 0b00111111, 2, 6)]

    class HvPwrEgyPrio_0_VDDMBackBoneSignalIPdu20:
        sig_name = "HvPwrEgyPrio_0_VDDMBackBoneSignalIPdu20"
        sig_start_bit = 18
        update_id_bit = 19
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvPwrEgyPrio_Standby': 0, 'HvPwrEgyPrio_Dischrgning': 1, 'HvPwrEgyPrio_Chrgning': 2, 'HvPwrEgyPrio_ClimaWithAc': 3, 'HvPwrEgyPrio_ClimaWithoutAc': 4, 'HvPwrEgyPrio_RemoteClimatisaiton': 5}
        compute_method = None
        length = 3
        startbit = 18
        byte = 2
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class OnBdChrgrPwrEnaAllwd:
        sig_name = "OnBdChrgrPwrEnaAllwd"
        sig_start_bit = 51
        update_id_bit = 54
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
        startbit = 51
        byte = 6
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class IsgPwrLimMax:
        sig_name = "IsgPwrLimMax"
        sig_start_bit = 33
        update_id_bit = 55
        sig_length = 10
        sig_value_factor = 0.5
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1022
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 33
        bmuws_info = [(4, 0b00000011, 0b11111100, 2, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class WhlMotSysTqAllwd_UB:
        sig_name = "WhlMotSysTqAllwd_UB"
        sig_start_bit = 6
        update_id_bit = 6
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
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class WhlMotSysTqAllwdChks:
        sig_name = "WhlMotSysTqAllwdChks"
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

    class WhlMotSysTqAllwdWhlMotSysTqAllwd:
        sig_name = "WhlMotSysTqAllwdWhlMotSysTqAllwd"
        sig_start_bit = 5
        update_id_bit = None
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
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4


class IemPropFr03:
    msg_name = "IemPropFr03"
    msg_id = 773
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.6
    msg_length = 8
    tx_node = "IEM"
    rx_nodes = ['ECM', 'VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class WhlMotSysInvrT:
        sig_name = "WhlMotSysInvrT"
        sig_start_bit = 7
        update_id_bit = 15
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -50.0
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Motorola"
        sig_value_init = 50
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class WhlMotSysMotT:
        sig_name = "WhlMotSysMotT"
        sig_start_bit = 23
        update_id_bit = 8
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -50.0
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Motorola"
        sig_value_init = 50
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 23
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class WhlMotClrRdyReq:
        sig_name = "WhlMotClrRdyReq"
        sig_start_bit = 24
        update_id_bit = 25
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

    class WhlMotSysErrIndcnReq:
        sig_name = "WhlMotSysErrIndcnReq"
        sig_start_bit = 10
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
        startbit = 10
        byte = 1
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class WhlMotSysCoolgReq:
        sig_name = "WhlMotSysCoolgReq"
        sig_start_bit = 14
        update_id_bit = 11
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvCoolg1_NoRequestForMoreCoolantPower': 0, 'HvCoolg1_IncreaseLevel1ForMoreCoolantPower': 1, 'HvCoolg1_IncreaseLevel2ForMoreCoolantPower': 2, 'HvCoolg1_MaxCoolingPower': 3, 'HvCoolg1_NotDefined': 4}
        compute_method = None
        length = 3
        startbit = 14
        byte = 1
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4


class EtctoEcmXCPFr01:
    msg_name = "EtctoEcmXCPFr01"
    msg_id = 1412
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CCM"
    rx_nodes = ['ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class EcmPropComFr12:
    msg_name = "EcmPropComFr12"
    msg_id = 259
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['BECM1', 'VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class BookChrgTarValLnr:
        sig_name = "BookChrgTarValLnr"
        sig_start_bit = 31
        update_id_bit = 5
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 2000
        sig_byteorder = "Motorola"
        sig_value_init = 2000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11100000, 0b00011111, 3, 5)]


class VddmToEtcDevelFr:
    msg_name = "VddmToEtcDevelFr"
    msg_id = 1518
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['CCM']
    sig_group_dict = {'VDDMPropCANInternalDevRespMesg': ['VDDMPropCANInternalDevRespMesgFunctiondevpsignalgroup1', 'VDDMPropCANInternalDevRespMesgFunctiondevpsignalgroup2', 'VDDMPropCANInternalDevRespMesgFunctiondevpsignalgroup3', 'VDDMPropCANInternalDevRespMesgFunctiondevpsignalgroup4', 'VDDMPropCANInternalDevRespMesgFunctiondevpsignalgroup5', 'VDDMPropCANInternalDevRespMesgFunctiondevpsignalgroup6', 'VDDMPropCANInternalDevRespMesgFunctiondevpsignalgroup7', 'VDDMPropCANInternalDevRespMesgFunctiondevpsignalgroup8']}
    sig_group_dataid_dict = {}

    class VDDMPropCANInternalDevRespMesgFunctiondevpsignalgroup4:
        sig_name = "VDDMPropCANInternalDevRespMesgFunctiondevpsignalgroup4"
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

    class VDDMPropCANInternalDevRespMesgFunctiondevpsignalgroup3:
        sig_name = "VDDMPropCANInternalDevRespMesgFunctiondevpsignalgroup3"
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

    class VDDMPropCANInternalDevRespMesgFunctiondevpsignalgroup8:
        sig_name = "VDDMPropCANInternalDevRespMesgFunctiondevpsignalgroup8"
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

    class VDDMPropCANInternalDevRespMesgFunctiondevpsignalgroup7:
        sig_name = "VDDMPropCANInternalDevRespMesgFunctiondevpsignalgroup7"
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

    class VDDMPropCANInternalDevRespMesgFunctiondevpsignalgroup6:
        sig_name = "VDDMPropCANInternalDevRespMesgFunctiondevpsignalgroup6"
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

    class VDDMPropCANInternalDevRespMesgFunctiondevpsignalgroup1:
        sig_name = "VDDMPropCANInternalDevRespMesgFunctiondevpsignalgroup1"
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

    class VDDMPropCANInternalDevRespMesgFunctiondevpsignalgroup2:
        sig_name = "VDDMPropCANInternalDevRespMesgFunctiondevpsignalgroup2"
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

    class VDDMPropCANInternalDevRespMesgFunctiondevpsignalgroup5:
        sig_name = "VDDMPropCANInternalDevRespMesgFunctiondevpsignalgroup5"
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


class BecmPropDevFr04:
    msg_name = "BecmPropDevFr04"
    msg_id = 1489
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['CCM']
    sig_group_dict = {'BECMdevelpsignalgroup4': ['BECMdevelpsignalgroup4Functiondevpsignalgroup1', 'BECMdevelpsignalgroup4Functiondevpsignalgroup2', 'BECMdevelpsignalgroup4Functiondevpsignalgroup3', 'BECMdevelpsignalgroup4Functiondevpsignalgroup4', 'BECMdevelpsignalgroup4Functiondevpsignalgroup5', 'BECMdevelpsignalgroup4Functiondevpsignalgroup6', 'BECMdevelpsignalgroup4Functiondevpsignalgroup7', 'BECMdevelpsignalgroup4Functiondevpsignalgroup8']}
    sig_group_dataid_dict = {}

    class BECMdevelpsignalgroup4Functiondevpsignalgroup1:
        sig_name = "BECMdevelpsignalgroup4Functiondevpsignalgroup1"
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

    class BECMdevelpsignalgroup4Functiondevpsignalgroup8:
        sig_name = "BECMdevelpsignalgroup4Functiondevpsignalgroup8"
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

    class BECMdevelpsignalgroup4Functiondevpsignalgroup6:
        sig_name = "BECMdevelpsignalgroup4Functiondevpsignalgroup6"
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

    class BECMdevelpsignalgroup4Functiondevpsignalgroup7:
        sig_name = "BECMdevelpsignalgroup4Functiondevpsignalgroup7"
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

    class BECMdevelpsignalgroup4Functiondevpsignalgroup2:
        sig_name = "BECMdevelpsignalgroup4Functiondevpsignalgroup2"
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

    class BECMdevelpsignalgroup4Functiondevpsignalgroup5:
        sig_name = "BECMdevelpsignalgroup4Functiondevpsignalgroup5"
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

    class BECMdevelpsignalgroup4Functiondevpsignalgroup4:
        sig_name = "BECMdevelpsignalgroup4Functiondevpsignalgroup4"
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

    class BECMdevelpsignalgroup4Functiondevpsignalgroup3:
        sig_name = "BECMdevelpsignalgroup4Functiondevpsignalgroup3"
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


class VddmPropVFCInfoEnaFr:
    msg_name = "VddmPropVFCInfoEnaFr"
    msg_id = 1375
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 1
    tx_node = "VDDM"
    rx_nodes = ['BECM1', 'EGSM', 'HVCM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class VFCInfoEna:
        sig_name = "VFCInfoEna"
        sig_start_bit = 0
        update_id_bit = 1
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


class VgmToSrsISO26021PropDiagResFrame11:
    msg_name = "VgmToSrsISO26021PropDiagResFrame11"
    msg_id = 2033
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['SRS']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class BecmPropFr14:
    msg_name = "BecmPropFr14"
    msg_id = 646
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.14
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['VDDM', 'ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class PackNr:
        sig_name = "PackNr"
        sig_start_bit = 63
        update_id_bit = 7
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvBattEgyAvlDcha1:
        sig_name = "HvBattEgyAvlDcha1"
        sig_start_bit = 4
        update_id_bit = 5
        sig_length = 13
        sig_value_factor = 20.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 4
        bmuws_info = [(0, 0b00011111, 0b11100000, 5, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class HvBattHeatGenn:
        sig_name = "HvBattHeatGenn"
        sig_start_bit = 43
        update_id_bit = 48
        sig_length = 11
        sig_value_factor = 100.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 43
        bmuws_info = [(5, 0b00001111, 0b11110000, 4, 0), (6, 0b11111110, 0b00000001, 7, 1)]

    class HvBattPreHeatFaild:
        sig_name = "HvBattPreHeatFaild"
        sig_start_bit = 45
        update_id_bit = 44
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

    class HvBattDchaTiEstimd:
        sig_name = "HvBattDchaTiEstimd"
        sig_start_bit = 23
        update_id_bit = 28
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
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11100000, 0b00011111, 3, 5)]


class BgmPropulsionFr02:
    msg_name = "BgmPropulsionFr02"
    msg_id = 1008
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.2
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['BECM1']
    sig_group_dict = {'LocalBookStopTiChrgnTmr': ['LocalBookStopTiChrgnTmrChrgnTmrhour', 'LocalBookStopTiChrgnTmrChrgnTmrmin'], 'LocalBookStrtTiChrgnTmr': ['LocalBookStrtTiChrgnTmrChrgnTmrhour', 'LocalBookStrtTiChrgnTmrChrgnTmrmin']}
    sig_group_dataid_dict = {}

    class LocalBookStrtTiChrgnTmrChrgnTmrmin:
        sig_name = "LocalBookStrtTiChrgnTmrChrgnTmrmin"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 60
        sig_byteorder = "Motorola"
        sig_value_init = 60
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class LocalBookStopTiChrgnTmr_UB:
        sig_name = "LocalBookStopTiChrgnTmr_UB"
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

    class LocalBookStopTiChrgnTmrChrgnTmrmin:
        sig_name = "LocalBookStopTiChrgnTmrChrgnTmrmin"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 60
        sig_byteorder = "Motorola"
        sig_value_init = 60
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class LocalBookStrtTiChrgnTmr_UB:
        sig_name = "LocalBookStrtTiChrgnTmr_UB"
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

    class LocalBookStopTiChrgnTmrChrgnTmrhour:
        sig_name = "LocalBookStopTiChrgnTmrChrgnTmrhour"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 24
        sig_byteorder = "Motorola"
        sig_value_init = 24
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class LocalBookStrtTiChrgnTmrChrgnTmrhour:
        sig_name = "LocalBookStrtTiChrgnTmrChrgnTmrhour"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 24
        sig_byteorder = "Motorola"
        sig_value_init = 24
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class BecmPropDevFr02:
    msg_name = "BecmPropDevFr02"
    msg_id = 1473
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['CCM']
    sig_group_dict = {'BECMdevelpsignalgroup2': ['BECMdevelpsignalgroup2Functiondevpsignalgroup1', 'BECMdevelpsignalgroup2Functiondevpsignalgroup2', 'BECMdevelpsignalgroup2Functiondevpsignalgroup3', 'BECMdevelpsignalgroup2Functiondevpsignalgroup4', 'BECMdevelpsignalgroup2Functiondevpsignalgroup5', 'BECMdevelpsignalgroup2Functiondevpsignalgroup6', 'BECMdevelpsignalgroup2Functiondevpsignalgroup7', 'BECMdevelpsignalgroup2Functiondevpsignalgroup8']}
    sig_group_dataid_dict = {}

    class BECMdevelpsignalgroup2Functiondevpsignalgroup1:
        sig_name = "BECMdevelpsignalgroup2Functiondevpsignalgroup1"
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

    class BECMdevelpsignalgroup2Functiondevpsignalgroup2:
        sig_name = "BECMdevelpsignalgroup2Functiondevpsignalgroup2"
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

    class BECMdevelpsignalgroup2Functiondevpsignalgroup6:
        sig_name = "BECMdevelpsignalgroup2Functiondevpsignalgroup6"
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

    class BECMdevelpsignalgroup2Functiondevpsignalgroup7:
        sig_name = "BECMdevelpsignalgroup2Functiondevpsignalgroup7"
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

    class BECMdevelpsignalgroup2Functiondevpsignalgroup5:
        sig_name = "BECMdevelpsignalgroup2Functiondevpsignalgroup5"
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

    class BECMdevelpsignalgroup2Functiondevpsignalgroup3:
        sig_name = "BECMdevelpsignalgroup2Functiondevpsignalgroup3"
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

    class BECMdevelpsignalgroup2Functiondevpsignalgroup4:
        sig_name = "BECMdevelpsignalgroup2Functiondevpsignalgroup4"
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

    class BECMdevelpsignalgroup2Functiondevpsignalgroup8:
        sig_name = "BECMdevelpsignalgroup2Functiondevpsignalgroup8"
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


class IgmMgmPropFr02:
    msg_name = "IgmMgmPropFr02"
    msg_id = 629
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.16
    msg_length = 8
    tx_node = "MGM"
    rx_nodes = ['ECM', 'VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class IsgCoolgReqInvr:
        sig_name = "IsgCoolgReqInvr"
        sig_start_bit = 52
        update_id_bit = 3
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvCoolg1_NoRequestForMoreCoolantPower': 0, 'HvCoolg1_IncreaseLevel1ForMoreCoolantPower': 1, 'HvCoolg1_IncreaseLevel2ForMoreCoolantPower': 2, 'HvCoolg1_MaxCoolingPower': 3, 'HvCoolg1_NotDefined': 4}
        compute_method = None
        length = 3
        startbit = 52
        byte = 6
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class IsgCooltFlowMinReq:
        sig_name = "IsgCooltFlowMinReq"
        sig_start_bit = 25
        update_id_bit = 26
        sig_length = 10
        sig_value_factor = 0.01
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

    class IsgInvrT:
        sig_name = "IsgInvrT"
        sig_start_bit = 63
        update_id_bit = 4
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -50.0
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Motorola"
        sig_value_init = 50
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class EgsmPropVFCVectorFr:
    msg_name = "EgsmPropVFCVectorFr"
    msg_id = 1349
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "EGSM"
    rx_nodes = ['CCM']
    sig_group_dict = {'VFCVectorEGSM': ['VFCVectorEGSMBlockID', 'VFCVectorEGSMVFCid0', 'VFCVectorEGSMVFCid1', 'VFCVectorEGSMVFCid10', 'VFCVectorEGSMVFCid11', 'VFCVectorEGSMVFCid12', 'VFCVectorEGSMVFCid13', 'VFCVectorEGSMVFCid14', 'VFCVectorEGSMVFCid15', 'VFCVectorEGSMVFCid16', 'VFCVectorEGSMVFCid17', 'VFCVectorEGSMVFCid18', 'VFCVectorEGSMVFCid19', 'VFCVectorEGSMVFCid2', 'VFCVectorEGSMVFCid20', 'VFCVectorEGSMVFCid21', 'VFCVectorEGSMVFCid22', 'VFCVectorEGSMVFCid23', 'VFCVectorEGSMVFCid24', 'VFCVectorEGSMVFCid25', 'VFCVectorEGSMVFCid26', 'VFCVectorEGSMVFCid27', 'VFCVectorEGSMVFCid28', 'VFCVectorEGSMVFCid29', 'VFCVectorEGSMVFCid3', 'VFCVectorEGSMVFCid30', 'VFCVectorEGSMVFCid31', 'VFCVectorEGSMVFCid32', 'VFCVectorEGSMVFCid33', 'VFCVectorEGSMVFCid34', 'VFCVectorEGSMVFCid35', 'VFCVectorEGSMVFCid36', 'VFCVectorEGSMVFCid37', 'VFCVectorEGSMVFCid38', 'VFCVectorEGSMVFCid39', 'VFCVectorEGSMVFCid4', 'VFCVectorEGSMVFCid40', 'VFCVectorEGSMVFCid41', 'VFCVectorEGSMVFCid42', 'VFCVectorEGSMVFCid43', 'VFCVectorEGSMVFCid44', 'VFCVectorEGSMVFCid45', 'VFCVectorEGSMVFCid46', 'VFCVectorEGSMVFCid47', 'VFCVectorEGSMVFCid48', 'VFCVectorEGSMVFCid49', 'VFCVectorEGSMVFCid5', 'VFCVectorEGSMVFCid50', 'VFCVectorEGSMVFCid51', 'VFCVectorEGSMVFCid52', 'VFCVectorEGSMVFCid53', 'VFCVectorEGSMVFCid54', 'VFCVectorEGSMVFCid55', 'VFCVectorEGSMVFCid56', 'VFCVectorEGSMVFCid57', 'VFCVectorEGSMVFCid58', 'VFCVectorEGSMVFCid59', 'VFCVectorEGSMVFCid6', 'VFCVectorEGSMVFCid60', 'VFCVectorEGSMVFCid61', 'VFCVectorEGSMVFCid7', 'VFCVectorEGSMVFCid8', 'VFCVectorEGSMVFCid9']}
    sig_group_dataid_dict = {}

    class VFCVectorEGSMVFCid55:
        sig_name = "VFCVectorEGSMVFCid55"
        sig_start_bit = 57
        update_id_bit = None
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

    class VFCVectorEGSMVFCid16:
        sig_name = "VFCVectorEGSMVFCid16"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 18
        byte = 2
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorEGSMVFCid48:
        sig_name = "VFCVectorEGSMVFCid48"
        sig_start_bit = 50
        update_id_bit = None
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

    class VFCVectorEGSMVFCid25:
        sig_name = "VFCVectorEGSMVFCid25"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 27
        byte = 3
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorEGSMVFCid31:
        sig_name = "VFCVectorEGSMVFCid31"
        sig_start_bit = 33
        update_id_bit = None
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

    class VFCVectorEGSMVFCid38:
        sig_name = "VFCVectorEGSMVFCid38"
        sig_start_bit = 40
        update_id_bit = None
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

    class VFCVectorEGSMVFCid40:
        sig_name = "VFCVectorEGSMVFCid40"
        sig_start_bit = 42
        update_id_bit = None
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

    class VFCVectorEGSMVFCid34:
        sig_name = "VFCVectorEGSMVFCid34"
        sig_start_bit = 36
        update_id_bit = None
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

    class VFCVectorEGSMVFCid32:
        sig_name = "VFCVectorEGSMVFCid32"
        sig_start_bit = 34
        update_id_bit = None
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

    class VFCVectorEGSMVFCid14:
        sig_name = "VFCVectorEGSMVFCid14"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 16
        byte = 2
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorEGSMVFCid3:
        sig_name = "VFCVectorEGSMVFCid3"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorEGSMVFCid9:
        sig_name = "VFCVectorEGSMVFCid9"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 11
        byte = 1
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorEGSMVFCid13:
        sig_name = "VFCVectorEGSMVFCid13"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 15
        byte = 1
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorEGSMVFCid5:
        sig_name = "VFCVectorEGSMVFCid5"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorEGSMVFCid47:
        sig_name = "VFCVectorEGSMVFCid47"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 49
        byte = 6
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorEGSMVFCid54:
        sig_name = "VFCVectorEGSMVFCid54"
        sig_start_bit = 56
        update_id_bit = None
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

    class VFCVectorEGSMVFCid59:
        sig_name = "VFCVectorEGSMVFCid59"
        sig_start_bit = 61
        update_id_bit = None
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

    class VFCVectorEGSMVFCid7:
        sig_name = "VFCVectorEGSMVFCid7"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 9
        byte = 1
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorEGSMVFCid23:
        sig_name = "VFCVectorEGSMVFCid23"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 25
        byte = 3
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorEGSMVFCid51:
        sig_name = "VFCVectorEGSMVFCid51"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 53
        byte = 6
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorEGSMVFCid24:
        sig_name = "VFCVectorEGSMVFCid24"
        sig_start_bit = 26
        update_id_bit = None
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

    class VFCVectorEGSMVFCid56:
        sig_name = "VFCVectorEGSMVFCid56"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 58
        byte = 7
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorEGSMVFCid21:
        sig_name = "VFCVectorEGSMVFCid21"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 23
        byte = 2
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorEGSMVFCid2:
        sig_name = "VFCVectorEGSMVFCid2"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 4
        byte = 0
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorEGSMVFCid28:
        sig_name = "VFCVectorEGSMVFCid28"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 30
        byte = 3
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorEGSMVFCid30:
        sig_name = "VFCVectorEGSMVFCid30"
        sig_start_bit = 32
        update_id_bit = None
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

    class VFCVectorEGSMVFCid18:
        sig_name = "VFCVectorEGSMVFCid18"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 20
        byte = 2
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorEGSMVFCid60:
        sig_name = "VFCVectorEGSMVFCid60"
        sig_start_bit = 62
        update_id_bit = None
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

    class VFCVectorEGSMVFCid46:
        sig_name = "VFCVectorEGSMVFCid46"
        sig_start_bit = 48
        update_id_bit = None
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

    class VFCVectorEGSMVFCid57:
        sig_name = "VFCVectorEGSMVFCid57"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 59
        byte = 7
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorEGSMVFCid44:
        sig_name = "VFCVectorEGSMVFCid44"
        sig_start_bit = 46
        update_id_bit = None
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

    class VFCVectorEGSMVFCid50:
        sig_name = "VFCVectorEGSMVFCid50"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorEGSMVFCid6:
        sig_name = "VFCVectorEGSMVFCid6"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 8
        byte = 1
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorEGSMVFCid12:
        sig_name = "VFCVectorEGSMVFCid12"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 14
        byte = 1
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorEGSMVFCid43:
        sig_name = "VFCVectorEGSMVFCid43"
        sig_start_bit = 45
        update_id_bit = None
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

    class VFCVectorEGSMBlockID:
        sig_name = "VFCVectorEGSMBlockID"
        sig_start_bit = 1
        update_id_bit = None
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

    class VFCVectorEGSMVFCid8:
        sig_name = "VFCVectorEGSMVFCid8"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 10
        byte = 1
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorEGSMVFCid49:
        sig_name = "VFCVectorEGSMVFCid49"
        sig_start_bit = 51
        update_id_bit = None
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

    class VFCVectorEGSMVFCid22:
        sig_name = "VFCVectorEGSMVFCid22"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 24
        byte = 3
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorEGSMVFCid26:
        sig_name = "VFCVectorEGSMVFCid26"
        sig_start_bit = 28
        update_id_bit = None
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

    class VFCVectorEGSMVFCid19:
        sig_name = "VFCVectorEGSMVFCid19"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 21
        byte = 2
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorEGSMVFCid53:
        sig_name = "VFCVectorEGSMVFCid53"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 55
        byte = 6
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorEGSMVFCid61:
        sig_name = "VFCVectorEGSMVFCid61"
        sig_start_bit = 63
        update_id_bit = None
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

    class VFCVectorEGSMVFCid0:
        sig_name = "VFCVectorEGSMVFCid0"
        sig_start_bit = 2
        update_id_bit = None
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

    class VFCVectorEGSMVFCid41:
        sig_name = "VFCVectorEGSMVFCid41"
        sig_start_bit = 43
        update_id_bit = None
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

    class VFCVectorEGSMVFCid27:
        sig_name = "VFCVectorEGSMVFCid27"
        sig_start_bit = 29
        update_id_bit = None
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

    class VFCVectorEGSMVFCid29:
        sig_name = "VFCVectorEGSMVFCid29"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 31
        byte = 3
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorEGSMVFCid33:
        sig_name = "VFCVectorEGSMVFCid33"
        sig_start_bit = 35
        update_id_bit = None
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

    class VFCVectorEGSMVFCid35:
        sig_name = "VFCVectorEGSMVFCid35"
        sig_start_bit = 37
        update_id_bit = None
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

    class VFCVectorEGSMVFCid1:
        sig_name = "VFCVectorEGSMVFCid1"
        sig_start_bit = 3
        update_id_bit = None
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

    class VFCVectorEGSMVFCid15:
        sig_name = "VFCVectorEGSMVFCid15"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 17
        byte = 2
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorEGSMVFCid37:
        sig_name = "VFCVectorEGSMVFCid37"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 39
        byte = 4
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorEGSMVFCid17:
        sig_name = "VFCVectorEGSMVFCid17"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 19
        byte = 2
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorEGSMVFCid39:
        sig_name = "VFCVectorEGSMVFCid39"
        sig_start_bit = 41
        update_id_bit = None
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

    class VFCVectorEGSMVFCid4:
        sig_name = "VFCVectorEGSMVFCid4"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorEGSMVFCid20:
        sig_name = "VFCVectorEGSMVFCid20"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 22
        byte = 2
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorEGSMVFCid11:
        sig_name = "VFCVectorEGSMVFCid11"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 13
        byte = 1
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorEGSMVFCid10:
        sig_name = "VFCVectorEGSMVFCid10"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 12
        byte = 1
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorEGSMVFCid42:
        sig_name = "VFCVectorEGSMVFCid42"
        sig_start_bit = 44
        update_id_bit = None
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

    class VFCVectorEGSMVFCid45:
        sig_name = "VFCVectorEGSMVFCid45"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 47
        byte = 5
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorEGSMVFCid58:
        sig_name = "VFCVectorEGSMVFCid58"
        sig_start_bit = 60
        update_id_bit = None
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

    class VFCVectorEGSMVFCid36:
        sig_name = "VFCVectorEGSMVFCid36"
        sig_start_bit = 38
        update_id_bit = None
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

    class VFCVectorEGSMVFCid52:
        sig_name = "VFCVectorEGSMVFCid52"
        sig_start_bit = 54
        update_id_bit = None
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


class VddmPropFr12:
    msg_name = "VddmPropFr12"
    msg_id = 353
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.025
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class V2XDchaSwt:
        sig_name = "V2XDchaSwt"
        sig_start_bit = 54
        update_id_bit = 52
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DisChrgrSW_Off': 0, 'DisChrgrSW_V2V': 1, 'DisChrgrSW_V2L': 2}
        compute_method = None
        length = 2
        startbit = 54
        byte = 6
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5


class VcuPropFr02:
    msg_name = "VcuPropFr02"
    msg_id = 919
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.4
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['BECM1']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class ResvSupChrgThermSwt:
        sig_name = "ResvSupChrgThermSwt"
        sig_start_bit = 6
        update_id_bit = 7
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


class BecmPropFr32:
    msg_name = "BecmPropFr32"
    msg_id = 1025
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.3
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['S2SReceiver']
    sig_group_dict = {'BthBookStopTiChrgnTmr': ['BthBookStopTiChrgnTmrChrgnTmrhour', 'BthBookStopTiChrgnTmrChrgnTmrmin'], 'BthBookStrtTiChrgnTmr': ['BthBookStrtTiChrgnTmrChrgnTmrhour', 'BthBookStrtTiChrgnTmrChrgnTmrmin']}
    sig_group_dataid_dict = {}

    class BthBookStrtTiChrgnTmrChrgnTmrmin:
        sig_name = "BthBookStrtTiChrgnTmrChrgnTmrmin"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 60
        sig_byteorder = "Motorola"
        sig_value_init = 60
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BthBookStopTiChrgnTmr_UB:
        sig_name = "BthBookStopTiChrgnTmr_UB"
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

    class BthBookStrtTiChrgnTmrChrgnTmrhour:
        sig_name = "BthBookStrtTiChrgnTmrChrgnTmrhour"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 24
        sig_byteorder = "Motorola"
        sig_value_init = 24
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ChrgPilBookChrgn:
        sig_name = "ChrgPilBookChrgn"
        sig_start_bit = 55
        update_id_bit = 48
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ChrgPilBookChrgn_Default': 0, 'ChrgPilBookChrgn_On': 1, 'ChrgPilBookChrgn_Off': 2, 'ChrgPilBookChrgn_Reserve': 3}
        compute_method = None
        length = 2
        startbit = 55
        byte = 6
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class BthBookStrtTiChrgnTmr_UB:
        sig_name = "BthBookStrtTiChrgnTmr_UB"
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

    class BthBookStopTiChrgnTmrChrgnTmrhour:
        sig_name = "BthBookStopTiChrgnTmrChrgnTmrhour"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 24
        sig_byteorder = "Motorola"
        sig_value_init = 24
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BthBookStopTiChrgnTmrChrgnTmrmin:
        sig_name = "BthBookStopTiChrgnTmrChrgnTmrmin"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 60
        sig_byteorder = "Motorola"
        sig_value_init = 60
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class MgmPropulsionCANNmFr:
    msg_name = "MgmPropulsionCANNmFr"
    msg_id = 1325
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "MGM"
    rx_nodes = ['IEM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class BecmPropFr20:
    msg_name = "BecmPropFr20"
    msg_id = 325
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['VDDM', 'ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HvBattOverDchaFlg:
        sig_name = "HvBattOverDchaFlg"
        sig_start_bit = 34
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
        startbit = 34
        byte = 4
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class CellUMin:
        sig_name = "CellUMin"
        sig_start_bit = 47
        update_id_bit = 32
        sig_length = 13
        sig_value_factor = 0.001
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 5000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111000, 0b00000111, 5, 3)]

    class CellUMinId:
        sig_name = "CellUMinId"
        sig_start_bit = 63
        update_id_bit = 48
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 250
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

    class CellUMax:
        sig_name = "CellUMax"
        sig_start_bit = 7
        update_id_bit = 8
        sig_length = 13
        sig_value_factor = 0.001
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 5000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111000, 0b00000111, 5, 3)]

    class CellUMaxId:
        sig_name = "CellUMaxId"
        sig_start_bit = 23
        update_id_bit = 9
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 250
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

    class CellUMaxLim:
        sig_name = "CellUMaxLim"
        sig_start_bit = 31
        update_id_bit = 10
        sig_length = 13
        sig_value_factor = 0.001
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 5000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111000, 0b00000111, 5, 3)]


class VddmPropFr28:
    msg_name = "VddmPropFr28"
    msg_id = 667
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.2
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['BECM1', 'ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class ChrgStationPwr:
        sig_name = "ChrgStationPwr"
        sig_start_bit = 10
        update_id_bit = 0
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
        startbit = 10
        bmuws_info = [(1, 0b00000111, 0b11111000, 3, 0), (2, 0b11111110, 0b00000001, 7, 1)]

    class NOPCoolReq:
        sig_name = "NOPCoolReq"
        sig_start_bit = 2
        update_id_bit = 1
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
        startbit = 2
        byte = 0
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class EstimdLeSocToDest:
        sig_name = "EstimdLeSocToDest"
        sig_start_bit = 31
        update_id_bit = 24
        sig_length = 7
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 101
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 31
        byte = 3
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1


class EcmPropFr06:
    msg_name = "EcmPropFr06"
    msg_id = 816
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.26
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['BECM1', 'VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HvBattHeatgPwrPreEstimd:
        sig_name = "HvBattHeatgPwrPreEstimd"
        sig_start_bit = 10
        update_id_bit = 16
        sig_length = 10
        sig_value_factor = 20.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 10
        bmuws_info = [(1, 0b00000111, 0b11111000, 3, 0), (2, 0b11111110, 0b00000001, 7, 1)]

    class HvCooltWtrHeatrWtrTInOutl_1_EcmPropSignalIPdu06:
        sig_name = "HvCooltWtrHeatrWtrTInOutl_1_EcmPropSignalIPdu06"
        sig_start_bit = 7
        update_id_bit = 11
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 40
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvCooltHeatrStsSig_1_EcmPropSignalIPdu06:
        sig_name = "HvCooltHeatrStsSig_1_EcmPropSignalIPdu06"
        sig_start_bit = 15
        update_id_bit = 12
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvCooltHeatrSts_Off': 0, 'HvCooltHeatrSts_LockedUntilNextStart': 1, 'HvCooltHeatrSts_LockedUntilService': 2, 'HvCooltHeatrSts_LockedPermanent': 3, 'HvCooltHeatrSts_Operation': 4, 'HvCooltHeatrSts_Reserved1': 5, 'HvCooltHeatrSts_Reserved2': 6, 'HvCooltHeatrSts_Reserved3': 7}
        compute_method = None
        length = 3
        startbit = 15
        byte = 1
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5


class VddmToMgmPropDiagReqFrame:
    msg_name = "VddmToMgmPropDiagReqFrame"
    msg_id = 1841
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['MGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class VddmPropFr26:
    msg_name = "VddmPropFr26"
    msg_id = 566
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['MGM', 'BECM1', 'EGSM', 'IEM', 'HVCM']
    sig_group_dict = {'VehCfgPrmExt_0_CemBackBoneSignalIPdu23': ['VehCfgPrmExtBlkIDBytePosn1_0_CemBackBoneSignalIPdu23', 'VehCfgPrmExtCCPBytePosn2_0_CemBackBoneSignalIPdu23', 'VehCfgPrmExtCCPBytePosn3_0_CemBackBoneSignalIPdu23', 'VehCfgPrmExtCCPBytePosn4_0_CemBackBoneSignalIPdu23', 'VehCfgPrmExtCCPBytePosn5_0_CemBackBoneSignalIPdu23', 'VehCfgPrmExtCCPBytePosn6_0_CemBackBoneSignalIPdu23', 'VehCfgPrmExtCCPBytePosn7_0_CemBackBoneSignalIPdu23', 'VehCfgPrmExtCCPBytePosn8_0_CemBackBoneSignalIPdu23']}
    sig_group_dataid_dict = {}

    class VehCfgPrmExtCCPBytePosn8_0_CemBackBoneSignalIPdu23:
        sig_name = "VehCfgPrmExtCCPBytePosn8_0_CemBackBoneSignalIPdu23"
        sig_start_bit = 63
        update_id_bit = None
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

    class VehCfgPrmExtCCPBytePosn3_0_CemBackBoneSignalIPdu23:
        sig_name = "VehCfgPrmExtCCPBytePosn3_0_CemBackBoneSignalIPdu23"
        sig_start_bit = 23
        update_id_bit = None
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

    class VehCfgPrmExtCCPBytePosn4_0_CemBackBoneSignalIPdu23:
        sig_name = "VehCfgPrmExtCCPBytePosn4_0_CemBackBoneSignalIPdu23"
        sig_start_bit = 31
        update_id_bit = None
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

    class VehCfgPrmExtCCPBytePosn6_0_CemBackBoneSignalIPdu23:
        sig_name = "VehCfgPrmExtCCPBytePosn6_0_CemBackBoneSignalIPdu23"
        sig_start_bit = 47
        update_id_bit = None
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

    class VehCfgPrmExtCCPBytePosn5_0_CemBackBoneSignalIPdu23:
        sig_name = "VehCfgPrmExtCCPBytePosn5_0_CemBackBoneSignalIPdu23"
        sig_start_bit = 39
        update_id_bit = None
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

    class VehCfgPrmExtCCPBytePosn7_0_CemBackBoneSignalIPdu23:
        sig_name = "VehCfgPrmExtCCPBytePosn7_0_CemBackBoneSignalIPdu23"
        sig_start_bit = 55
        update_id_bit = None
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

    class VehCfgPrmExtCCPBytePosn2_0_CemBackBoneSignalIPdu23:
        sig_name = "VehCfgPrmExtCCPBytePosn2_0_CemBackBoneSignalIPdu23"
        sig_start_bit = 15
        update_id_bit = None
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

    class VehCfgPrmExtBlkIDBytePosn1_0_CemBackBoneSignalIPdu23:
        sig_name = "VehCfgPrmExtBlkIDBytePosn1_0_CemBackBoneSignalIPdu23"
        sig_start_bit = 7
        update_id_bit = None
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


class VddmPropFr07:
    msg_name = "VddmPropFr07"
    msg_id = 113
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.015
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class AxleSlipRelAct:
        sig_name = "AxleSlipRelAct"
        sig_start_bit = 53
        update_id_bit = 54
        sig_length = 14
        sig_value_factor = 0.003906369
        sig_value_offset = 0.0
        sig_value_min = -7679
        sig_value_max = 7680
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 14
        startbit = 53
        bmuws_info = [(6, 0b00111111, 0b11000000, 6, 0), (7, 0b11111111, 0b00000000, 8, 0)]


class BecmPropFr19:
    msg_name = "BecmPropFr19"
    msg_id = 839
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 1.0
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['VDDM', 'ECM']
    sig_group_dict = {'HvBattCod': ['HvBattCodPackCodeX1', 'HvBattCodPackCodeX2', 'HvBattCodPackCodeX3', 'HvBattCodPackCodeX4', 'HvBattCodPackCodeX5', 'HvBattCodPackCodeX6', 'HvBattCodPackIndex']}
    sig_group_dataid_dict = {}

    class HvBattCodPackCodeX2:
        sig_name = "HvBattCodPackCodeX2"
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

    class HvBattCodPackCodeX5:
        sig_name = "HvBattCodPackCodeX5"
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

    class HvBattCodPackCodeX6:
        sig_name = "HvBattCodPackCodeX6"
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

    class HvBattCod_UB:
        sig_name = "HvBattCod_UB"
        sig_start_bit = 63
        update_id_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class HvBattCodPackCodeX1:
        sig_name = "HvBattCodPackCodeX1"
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

    class HvBattCodPackIndex:
        sig_name = "HvBattCodPackIndex"
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

    class HvBattCodPackCodeX3:
        sig_name = "HvBattCodPackCodeX3"
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

    class HvBattCodPackCodeX4:
        sig_name = "HvBattCodPackCodeX4"
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


class VddmPropFr32:
    msg_name = "VddmPropFr32"
    msg_id = 1042
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.5
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']
    sig_group_dict = {'ClimateCtrlInFuture': ['ClimateCtrlInFuturePwrAtTime', 'ClimateCtrlInFutureSequenceNo', 'ClimateCtrlInFutureTempAtTime', 'ClimateCtrlInFutureThermModAtTime', 'ClimateCtrlInFutureTime', 'ClimateCtrlInFutureVersionNo']}
    sig_group_dataid_dict = {}

    class ClimateCtrlInFuturePwrAtTime:
        sig_name = "ClimateCtrlInFuturePwrAtTime"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 50.0
        sig_value_offset = -25000.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 500
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class ClimateCtrlInFutureThermModAtTime:
        sig_name = "ClimateCtrlInFutureThermModAtTime"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Idle': 0, 'ThermalBalancing': 1, 'PassiveHeating': 2, 'ActiveHeating': 3, 'PassiveCooling': 4, 'ActiveCooling': 5, 'CombinedCooling': 6, 'Reserved': 7}
        compute_method = None
        length = 3
        startbit = 15
        byte = 1
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class ClimateCtrlInFutureSequenceNo:
        sig_name = "ClimateCtrlInFutureSequenceNo"
        sig_start_bit = 12
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
        startbit = 12
        byte = 1
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class ClimateCtrlInFutureVersionNo:
        sig_name = "ClimateCtrlInFutureVersionNo"
        sig_start_bit = 2
        update_id_bit = None
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
        startbit = 2
        byte = 0
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class ClimateCtrlInFutureTempAtTime:
        sig_name = "ClimateCtrlInFutureTempAtTime"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -50.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 50
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 23
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ClimateCtrlInFutureTime:
        sig_name = "ClimateCtrlInFutureTime"
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

    class ClimateCtrlInFuture_UB:
        sig_name = "ClimateCtrlInFuture_UB"
        sig_start_bit = 3
        update_id_bit = 3
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
        startbit = 3
        byte = 0
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3


class CddIgmPropFr05:
    msg_name = "CddIgmPropFr05"
    msg_id = 1109
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.8
    msg_length = 8
    tx_node = "HVCM"
    rx_nodes = ['VDDM', 'ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class DcDcMinCooltFlow:
        sig_name = "DcDcMinCooltFlow"
        sig_start_bit = 7
        update_id_bit = 0
        sig_length = 7
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 127
        sig_byteorder = "Motorola"
        sig_value_init = 20
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 7
        byte = 0
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class TDcDcCoolt:
        sig_name = "TDcDcCoolt"
        sig_start_bit = 31
        update_id_bit = 16
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 40
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class EcmPropFr04:
    msg_name = "EcmPropFr04"
    msg_id = 305
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['BECM1', 'IEM', 'HVCM', 'VDDM']
    sig_group_dict = {'PtAllwdToTrsmActrSafe': ['PtAllwdToTrsmActrSafeChks', 'PtAllwdToTrsmActrSafeCntr', 'PtAllwdToTrsmActrSafePtAllwdToTrsmActr']}
    sig_group_dataid_dict = {'PtAllwdToTrsmActrSafe': 63}

    class DcDcActvdReq:
        sig_name = "DcDcActvdReq"
        sig_start_bit = 44
        update_id_bit = 42
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DcDcActvd_NoConversionToLVSide': 0, 'DcDcActvd_ConversionToLVSide': 1}
        compute_method = None
        length = 1
        startbit = 44
        byte = 5
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class PtAllwdToTrsmActrSafe_UB:
        sig_name = "PtAllwdToTrsmActrSafe_UB"
        sig_start_bit = 23
        update_id_bit = 23
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
        startbit = 23
        byte = 2
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class PtAllwdToTrsmActrSafeCntr:
        sig_name = "PtAllwdToTrsmActrSafeCntr"
        sig_start_bit = 11
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
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class WhlMotSysPwrLimMax:
        sig_name = "WhlMotSysPwrLimMax"
        sig_start_bit = 41
        update_id_bit = 45
        sig_length = 10
        sig_value_factor = 0.5
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1022
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 41
        bmuws_info = [(5, 0b00000011, 0b11111100, 2, 0), (6, 0b11111111, 0b00000000, 8, 0)]

    class PtAllwdToTrsmActrSafeChks:
        sig_name = "PtAllwdToTrsmActrSafeChks"
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

    class DispHvBattLvlOfChrg:
        sig_name = "DispHvBattLvlOfChrg"
        sig_start_bit = 39
        update_id_bit = 43
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11000000, 0b00111111, 2, 6)]

    class PtAllwdToTrsmActrSafePtAllwdToTrsmActr:
        sig_name = "PtAllwdToTrsmActrSafePtAllwdToTrsmActr"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PtAllwdToTrsmActr1_NotAllwd1': 0, 'PtAllwdToTrsmActr1_RvsAllwd': 1, 'PtAllwdToTrsmActr1_RvsNotAllwd': 2, 'PtAllwdToTrsmActr1_NotAllwd2': 3, 'PtAllwdToTrsmActr1_ParkRelsAllwd': 4, 'PtAllwdToTrsmActr1_RvsAllwdAndParkRelsAllwd': 5, 'PtAllwdToTrsmActr1_RvsNotAllwdAndParkRelsAllwd': 6, 'PtAllwdToTrsmActr1_NotAllwd3': 7, 'PtAllwdToTrsmActr1_ParkRelsNotAllwd': 8, 'PtAllwdToTrsmActr1_RvsAllwdAndParkRelsNotAllwd': 9, 'PtAllwdToTrsmActr1_RvsNotAllwdAndParkRelsNotAllwd': 10, 'PtAllwdToTrsmActr1_NotAllwd4': 11, 'PtAllwdToTrsmActr1_NotAllwd5': 12, 'PtAllwdToTrsmActr1_NotAllwd6': 13, 'PtAllwdToTrsmActr1_NotAllwd7': 14, 'PtAllwdToTrsmActr1_NotAllwd8': 15}
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class PtDrftSts:
        sig_name = "PtDrftSts"
        sig_start_bit = 22
        update_id_bit = 19
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
        startbit = 22
        byte = 2
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4


class VddmPropFr38:
    msg_name = "VddmPropFr38"
    msg_id = 819
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 1.0
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['BECM1']
    sig_group_dict = {'UTCTiFromEth': ['UTCTiFromEthDataValid', 'UTCTiFromEthDay', 'UTCTiFromEthHr1', 'UTCTiFromEthMins1', 'UTCTiFromEthMth1', 'UTCTiFromEthSec1', 'UTCTiFromEthYr1']}
    sig_group_dataid_dict = {}

    class UTCTiFromEth_UB:
        sig_name = "UTCTiFromEth_UB"
        sig_start_bit = 6
        update_id_bit = 6
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
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class UTCTiFromEthMth1:
        sig_name = "UTCTiFromEthMth1"
        sig_start_bit = 47
        update_id_bit = None
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
        startbit = 47
        byte = 5
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class GpsStatus:
        sig_name = "GpsStatus"
        sig_start_bit = 43
        update_id_bit = 42
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 43
        byte = 5
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class UTCTiFromEthYr1:
        sig_name = "UTCTiFromEthYr1"
        sig_start_bit = 39
        update_id_bit = None
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
        startbit = 39
        byte = 4
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class UTCTiFromEthMins1:
        sig_name = "UTCTiFromEthMins1"
        sig_start_bit = 23
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
        startbit = 23
        byte = 2
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class UTCTiFromEthDataValid:
        sig_name = "UTCTiFromEthDataValid"
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
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class UTCTiFromEthDay:
        sig_name = "UTCTiFromEthDay"
        sig_start_bit = 4
        update_id_bit = None
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
        startbit = 4
        byte = 0
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class UTCTiFromEthSec1:
        sig_name = "UTCTiFromEthSec1"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class UTCTiFromEthHr1:
        sig_name = "UTCTiFromEthHr1"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111000
        unmask = 0b00000111
        shift = 3


class IemToVddmPropDiagRespFrame:
    msg_name = "IemToVddmPropDiagRespFrame"
    msg_id = 1591
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "IEM"
    rx_nodes = ['VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class EcmPropVFCVectorFr:
    msg_name = "EcmPropVFCVectorFr"
    msg_id = 1347
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['CCM']
    sig_group_dict = {'VFCVectorECM': ['VFCVectorECMBlockID', 'VFCVectorECMVFCid0', 'VFCVectorECMVFCid1', 'VFCVectorECMVFCid10', 'VFCVectorECMVFCid11', 'VFCVectorECMVFCid12', 'VFCVectorECMVFCid13', 'VFCVectorECMVFCid14', 'VFCVectorECMVFCid15', 'VFCVectorECMVFCid16', 'VFCVectorECMVFCid17', 'VFCVectorECMVFCid18', 'VFCVectorECMVFCid19', 'VFCVectorECMVFCid2', 'VFCVectorECMVFCid20', 'VFCVectorECMVFCid21', 'VFCVectorECMVFCid22', 'VFCVectorECMVFCid23', 'VFCVectorECMVFCid24', 'VFCVectorECMVFCid25', 'VFCVectorECMVFCid26', 'VFCVectorECMVFCid27', 'VFCVectorECMVFCid28', 'VFCVectorECMVFCid29', 'VFCVectorECMVFCid3', 'VFCVectorECMVFCid30', 'VFCVectorECMVFCid31', 'VFCVectorECMVFCid32', 'VFCVectorECMVFCid33', 'VFCVectorECMVFCid34', 'VFCVectorECMVFCid35', 'VFCVectorECMVFCid36', 'VFCVectorECMVFCid37', 'VFCVectorECMVFCid38', 'VFCVectorECMVFCid39', 'VFCVectorECMVFCid4', 'VFCVectorECMVFCid40', 'VFCVectorECMVFCid41', 'VFCVectorECMVFCid42', 'VFCVectorECMVFCid43', 'VFCVectorECMVFCid44', 'VFCVectorECMVFCid45', 'VFCVectorECMVFCid46', 'VFCVectorECMVFCid47', 'VFCVectorECMVFCid48', 'VFCVectorECMVFCid49', 'VFCVectorECMVFCid5', 'VFCVectorECMVFCid50', 'VFCVectorECMVFCid51', 'VFCVectorECMVFCid52', 'VFCVectorECMVFCid53', 'VFCVectorECMVFCid54', 'VFCVectorECMVFCid55', 'VFCVectorECMVFCid56', 'VFCVectorECMVFCid57', 'VFCVectorECMVFCid58', 'VFCVectorECMVFCid59', 'VFCVectorECMVFCid6', 'VFCVectorECMVFCid60', 'VFCVectorECMVFCid61', 'VFCVectorECMVFCid7', 'VFCVectorECMVFCid8', 'VFCVectorECMVFCid9']}
    sig_group_dataid_dict = {}

    class VFCVectorECMVFCid35:
        sig_name = "VFCVectorECMVFCid35"
        sig_start_bit = 37
        update_id_bit = None
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

    class VFCVectorECMVFCid39:
        sig_name = "VFCVectorECMVFCid39"
        sig_start_bit = 41
        update_id_bit = None
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

    class VFCVectorECMVFCid45:
        sig_name = "VFCVectorECMVFCid45"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 47
        byte = 5
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorECMVFCid53:
        sig_name = "VFCVectorECMVFCid53"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 55
        byte = 6
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorECMVFCid33:
        sig_name = "VFCVectorECMVFCid33"
        sig_start_bit = 35
        update_id_bit = None
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

    class VFCVectorECMVFCid1:
        sig_name = "VFCVectorECMVFCid1"
        sig_start_bit = 3
        update_id_bit = None
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

    class VFCVectorECMVFCid4:
        sig_name = "VFCVectorECMVFCid4"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorECMVFCid17:
        sig_name = "VFCVectorECMVFCid17"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 19
        byte = 2
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorECMVFCid47:
        sig_name = "VFCVectorECMVFCid47"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 49
        byte = 6
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorECMVFCid16:
        sig_name = "VFCVectorECMVFCid16"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 18
        byte = 2
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorECMVFCid44:
        sig_name = "VFCVectorECMVFCid44"
        sig_start_bit = 46
        update_id_bit = None
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

    class VFCVectorECMVFCid23:
        sig_name = "VFCVectorECMVFCid23"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 25
        byte = 3
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorECMVFCid21:
        sig_name = "VFCVectorECMVFCid21"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 23
        byte = 2
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorECMVFCid13:
        sig_name = "VFCVectorECMVFCid13"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 15
        byte = 1
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorECMVFCid19:
        sig_name = "VFCVectorECMVFCid19"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 21
        byte = 2
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorECMVFCid40:
        sig_name = "VFCVectorECMVFCid40"
        sig_start_bit = 42
        update_id_bit = None
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

    class VFCVectorECMVFCid24:
        sig_name = "VFCVectorECMVFCid24"
        sig_start_bit = 26
        update_id_bit = None
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

    class VFCVectorECMVFCid25:
        sig_name = "VFCVectorECMVFCid25"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 27
        byte = 3
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorECMVFCid29:
        sig_name = "VFCVectorECMVFCid29"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 31
        byte = 3
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorECMVFCid30:
        sig_name = "VFCVectorECMVFCid30"
        sig_start_bit = 32
        update_id_bit = None
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

    class VFCVectorECMVFCid48:
        sig_name = "VFCVectorECMVFCid48"
        sig_start_bit = 50
        update_id_bit = None
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

    class VFCVectorECMVFCid58:
        sig_name = "VFCVectorECMVFCid58"
        sig_start_bit = 60
        update_id_bit = None
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

    class VFCVectorECMVFCid60:
        sig_name = "VFCVectorECMVFCid60"
        sig_start_bit = 62
        update_id_bit = None
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

    class VFCVectorECMVFCid14:
        sig_name = "VFCVectorECMVFCid14"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 16
        byte = 2
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorECMVFCid27:
        sig_name = "VFCVectorECMVFCid27"
        sig_start_bit = 29
        update_id_bit = None
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

    class VFCVectorECMVFCid18:
        sig_name = "VFCVectorECMVFCid18"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 20
        byte = 2
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorECMVFCid41:
        sig_name = "VFCVectorECMVFCid41"
        sig_start_bit = 43
        update_id_bit = None
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

    class VFCVectorECMVFCid5:
        sig_name = "VFCVectorECMVFCid5"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorECMVFCid61:
        sig_name = "VFCVectorECMVFCid61"
        sig_start_bit = 63
        update_id_bit = None
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

    class VFCVectorECMVFCid28:
        sig_name = "VFCVectorECMVFCid28"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 30
        byte = 3
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorECMVFCid54:
        sig_name = "VFCVectorECMVFCid54"
        sig_start_bit = 56
        update_id_bit = None
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

    class VFCVectorECMVFCid6:
        sig_name = "VFCVectorECMVFCid6"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 8
        byte = 1
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorECMVFCid7:
        sig_name = "VFCVectorECMVFCid7"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 9
        byte = 1
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorECMVFCid42:
        sig_name = "VFCVectorECMVFCid42"
        sig_start_bit = 44
        update_id_bit = None
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

    class VFCVectorECMVFCid36:
        sig_name = "VFCVectorECMVFCid36"
        sig_start_bit = 38
        update_id_bit = None
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

    class VFCVectorECMVFCid37:
        sig_name = "VFCVectorECMVFCid37"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 39
        byte = 4
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorECMVFCid12:
        sig_name = "VFCVectorECMVFCid12"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 14
        byte = 1
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorECMVFCid2:
        sig_name = "VFCVectorECMVFCid2"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 4
        byte = 0
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorECMVFCid38:
        sig_name = "VFCVectorECMVFCid38"
        sig_start_bit = 40
        update_id_bit = None
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

    class VFCVectorECMVFCid51:
        sig_name = "VFCVectorECMVFCid51"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 53
        byte = 6
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorECMVFCid49:
        sig_name = "VFCVectorECMVFCid49"
        sig_start_bit = 51
        update_id_bit = None
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

    class VFCVectorECMVFCid0:
        sig_name = "VFCVectorECMVFCid0"
        sig_start_bit = 2
        update_id_bit = None
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

    class VFCVectorECMVFCid57:
        sig_name = "VFCVectorECMVFCid57"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 59
        byte = 7
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorECMVFCid8:
        sig_name = "VFCVectorECMVFCid8"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 10
        byte = 1
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorECMVFCid9:
        sig_name = "VFCVectorECMVFCid9"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 11
        byte = 1
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorECMVFCid59:
        sig_name = "VFCVectorECMVFCid59"
        sig_start_bit = 61
        update_id_bit = None
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

    class VFCVectorECMVFCid10:
        sig_name = "VFCVectorECMVFCid10"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 12
        byte = 1
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorECMVFCid22:
        sig_name = "VFCVectorECMVFCid22"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 24
        byte = 3
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorECMVFCid43:
        sig_name = "VFCVectorECMVFCid43"
        sig_start_bit = 45
        update_id_bit = None
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

    class VFCVectorECMVFCid20:
        sig_name = "VFCVectorECMVFCid20"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 22
        byte = 2
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorECMVFCid11:
        sig_name = "VFCVectorECMVFCid11"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 13
        byte = 1
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorECMVFCid26:
        sig_name = "VFCVectorECMVFCid26"
        sig_start_bit = 28
        update_id_bit = None
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

    class VFCVectorECMVFCid31:
        sig_name = "VFCVectorECMVFCid31"
        sig_start_bit = 33
        update_id_bit = None
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

    class VFCVectorECMVFCid52:
        sig_name = "VFCVectorECMVFCid52"
        sig_start_bit = 54
        update_id_bit = None
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

    class VFCVectorECMVFCid3:
        sig_name = "VFCVectorECMVFCid3"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorECMBlockID:
        sig_name = "VFCVectorECMBlockID"
        sig_start_bit = 1
        update_id_bit = None
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

    class VFCVectorECMVFCid55:
        sig_name = "VFCVectorECMVFCid55"
        sig_start_bit = 57
        update_id_bit = None
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

    class VFCVectorECMVFCid56:
        sig_name = "VFCVectorECMVFCid56"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 58
        byte = 7
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorECMVFCid32:
        sig_name = "VFCVectorECMVFCid32"
        sig_start_bit = 34
        update_id_bit = None
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

    class VFCVectorECMVFCid15:
        sig_name = "VFCVectorECMVFCid15"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 17
        byte = 2
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorECMVFCid34:
        sig_name = "VFCVectorECMVFCid34"
        sig_start_bit = 36
        update_id_bit = None
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

    class VFCVectorECMVFCid46:
        sig_name = "VFCVectorECMVFCid46"
        sig_start_bit = 48
        update_id_bit = None
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

    class VFCVectorECMVFCid50:
        sig_name = "VFCVectorECMVFCid50"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4


class EcmToVgmJ1979OBDPropCanResFrame11:
    msg_name = "EcmToVgmJ1979OBDPropCanResFrame11"
    msg_id = 2024
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['BGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class BecmPropFr13:
    msg_name = "BecmPropFr13"
    msg_id = 664
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.6
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['VDDM', 'ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HvBattChrgnPwrCritDes1:
        sig_name = "HvBattChrgnPwrCritDes1"
        sig_start_bit = 10
        update_id_bit = 11
        sig_length = 11
        sig_value_factor = 100.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 10
        bmuws_info = [(1, 0b00000111, 0b11111000, 3, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class HvBattChrgnPwrCns1:
        sig_name = "HvBattChrgnPwrCns1"
        sig_start_bit = 7
        update_id_bit = 12
        sig_length = 11
        sig_value_factor = 100.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11100000, 0b00011111, 3, 5)]

    class HvBattChrgnPwrNormDes1:
        sig_name = "HvBattChrgnPwrNormDes1"
        sig_start_bit = 31
        update_id_bit = 36
        sig_length = 11
        sig_value_factor = 100.0
        sig_value_offset = 0.0
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

    class HvBattEgyAvlChrg1:
        sig_name = "HvBattEgyAvlChrg1"
        sig_start_bit = 52
        update_id_bit = 53
        sig_length = 13
        sig_value_factor = 20.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 52
        bmuws_info = [(6, 0b00011111, 0b11100000, 5, 0), (7, 0b11111111, 0b00000000, 8, 0)]


class BecmPropFr08:
    msg_name = "BecmPropFr08"
    msg_id = 834
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 1.0
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HvPackOverChrgFlt:
        sig_name = "HvPackOverChrgFlt"
        sig_start_bit = 11
        update_id_bit = 40
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FauLevel_Normal': 0, 'FauLevel_LevelI': 1, 'FauLevel_LevelII': 2, 'FauLevel_LevelIII': 3}
        compute_method = None
        length = 2
        startbit = 11
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class HvilFlt:
        sig_name = "HvilFlt"
        sig_start_bit = 0
        update_id_bit = 42
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevErrSts2_NoFlt': 0, 'DevErrSts2_Flt': 1}
        compute_method = None
        length = 1
        startbit = 0
        byte = 0
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class HvCellUOverFlt:
        sig_name = "HvCellUOverFlt"
        sig_start_bit = 53
        update_id_bit = 34
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FauLevel_Normal': 0, 'FauLevel_LevelI': 1, 'FauLevel_LevelII': 2, 'FauLevel_LevelIII': 3}
        compute_method = None
        length = 2
        startbit = 53
        byte = 6
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class HvPackUOverFlt:
        sig_name = "HvPackUOverFlt"
        sig_start_bit = 9
        update_id_bit = 36
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FauLevel_Normal': 0, 'FauLevel_LevelI': 1, 'FauLevel_LevelII': 2, 'FauLevel_LevelIII': 3}
        compute_method = None
        length = 2
        startbit = 9
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class HvCellUUnderFlt:
        sig_name = "HvCellUUnderFlt"
        sig_start_bit = 15
        update_id_bit = 33
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FauLevel_Normal': 0, 'FauLevel_LevelI': 1, 'FauLevel_LevelII': 2, 'FauLevel_LevelIII': 3}
        compute_method = None
        length = 2
        startbit = 15
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HvSocHiFlt:
        sig_name = "HvSocHiFlt"
        sig_start_bit = 63
        update_id_bit = 48
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FauLevel_Normal': 0, 'FauLevel_LevelI': 1, 'FauLevel_LevelII': 2, 'FauLevel_LevelIII': 3}
        compute_method = None
        length = 2
        startbit = 63
        byte = 7
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HvSocHopFlt:
        sig_name = "HvSocHopFlt"
        sig_start_bit = 45
        update_id_bit = 43
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FauLevel_Normal': 0, 'FauLevel_LevelI': 1, 'FauLevel_LevelII': 2, 'FauLevel_LevelIII': 3}
        compute_method = None
        length = 2
        startbit = 45
        byte = 5
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class HvSocLoFlt:
        sig_name = "HvSocLoFlt"
        sig_start_bit = 51
        update_id_bit = 49
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FauLevel_Normal': 0, 'FauLevel_LevelI': 1, 'FauLevel_LevelII': 2, 'FauLevel_LevelIII': 3}
        compute_method = None
        length = 2
        startbit = 51
        byte = 6
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class HvCellTDifFlt:
        sig_name = "HvCellTDifFlt"
        sig_start_bit = 6
        update_id_bit = 4
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FauLevel_Normal': 0, 'FauLevel_LevelI': 1, 'FauLevel_LevelII': 2, 'FauLevel_LevelIII': 3}
        compute_method = None
        length = 2
        startbit = 6
        byte = 0
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class HvCellTOverFlt:
        sig_name = "HvCellTOverFlt"
        sig_start_bit = 55
        update_id_bit = 35
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FauLevel_Normal': 0, 'FauLevel_LevelI': 1, 'FauLevel_LevelII': 2, 'FauLevel_LevelIII': 3}
        compute_method = None
        length = 2
        startbit = 55
        byte = 6
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HvCellUDifFlt:
        sig_name = "HvCellUDifFlt"
        sig_start_bit = 3
        update_id_bit = 1
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FauLevel_Normal': 0, 'FauLevel_LevelI': 1, 'FauLevel_LevelII': 2, 'FauLevel_LevelIII': 3}
        compute_method = None
        length = 2
        startbit = 3
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class HvIsoFlt:
        sig_name = "HvIsoFlt"
        sig_start_bit = 13
        update_id_bit = 41
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FauLevel_Normal': 0, 'FauLevel_LevelI': 1, 'FauLevel_LevelII': 2, 'FauLevel_LevelIII': 3}
        compute_method = None
        length = 2
        startbit = 13
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class HvBattMismatchFlt:
        sig_name = "HvBattMismatchFlt"
        sig_start_bit = 7
        update_id_bit = 38
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevErrSts2_NoFlt': 0, 'DevErrSts2_Flt': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class HvBattNr:
        sig_name = "HvBattNr"
        sig_start_bit = 31
        update_id_bit = 37
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvPackUUnderFlt:
        sig_name = "HvPackUUnderFlt"
        sig_start_bit = 47
        update_id_bit = 32
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FauLevel_Normal': 0, 'FauLevel_LevelI': 1, 'FauLevel_LevelII': 2, 'FauLevel_LevelIII': 3}
        compute_method = None
        length = 2
        startbit = 47
        byte = 5
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HvBattCodLen:
        sig_name = "HvBattCodLen"
        sig_start_bit = 23
        update_id_bit = 39
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 23
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class VddmPropFr14:
    msg_name = "VddmPropFr14"
    msg_id = 358
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']
    sig_group_dict = {'LimForDecel': ['LimForDecelChks', 'LimForDecelCntr', 'LimForDecelNotExcd']}
    sig_group_dataid_dict = {'LimForDecel': 139}

    class LimForDecelCntr:
        sig_name = "LimForDecelCntr"
        sig_start_bit = 51
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
        startbit = 51
        byte = 6
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class LimForDecelNotExcd:
        sig_name = "LimForDecelNotExcd"
        sig_start_bit = 52
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class LimForDecel_UB:
        sig_name = "LimForDecel_UB"
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

    class TiDrvgCycOff:
        sig_name = "TiDrvgCycOff"
        sig_start_bit = 23
        update_id_bit = 38
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

    class LimForDecelChks:
        sig_name = "LimForDecelChks"
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


class IemEduPropFr02:
    msg_name = "IemEduPropFr02"
    msg_id = 96
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "IEM"
    rx_nodes = ['BGM', 'BECM1', 'ECM', 'VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class WhlMotSysCooltT:
        sig_name = "WhlMotSysCooltT"
        sig_start_bit = 31
        update_id_bit = 16
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 40
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class WhlMotSysLimnIndcn:
        sig_name = "WhlMotSysLimnIndcn"
        sig_start_bit = 55
        update_id_bit = 39
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
        startbit = 55
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class WhlMotSysUdc:
        sig_name = "WhlMotSysUdc"
        sig_start_bit = 34
        update_id_bit = 38
        sig_length = 11
        sig_value_factor = 0.25
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 2044
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 34
        bmuws_info = [(4, 0b00000111, 0b11111000, 3, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class ImobEngSts2:
        sig_name = "ImobEngSts2"
        sig_start_bit = 36
        update_id_bit = 37
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ImobSts_ImobUndefd': 0, 'ImobSts_ImobImobn': 1, 'ImobSts_ImobMtn': 2, 'ImobSts_ImobNoMtn': 3}
        compute_method = None
        length = 2
        startbit = 36
        byte = 4
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class WhlMotSysSpdAct:
        sig_name = "WhlMotSysSpdAct"
        sig_start_bit = 6
        update_id_bit = 7
        sig_length = 15
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = -16384
        sig_value_max = 16383
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 6
        bmuws_info = [(0, 0b01111111, 0b10000000, 7, 0), (1, 0b11111111, 0b00000000, 8, 0)]


class IemPropdTCFr16:
    msg_name = "IemPropdTCFr16"
    msg_id = 272
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "IEM"
    rx_nodes = ['VDDM']
    sig_group_dict = {'DmcStsRearToEsc': ['DmcStsRearToEscChks', 'DmcStsRearToEscCntr', 'DmcStsRearToEscDmcActAppTarTq', 'DmcStsRearToEscDmcSts', 'DmcStsRearToEscDmcSWInfo']}
    sig_group_dataid_dict = {'DmcStsRearToEsc': 6015}

    class DmcStsRearToEscDmcSWInfo:
        sig_name = "DmcStsRearToEscDmcSWInfo"
        sig_start_bit = 39
        update_id_bit = None
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
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class DmcStsRearToEscChks:
        sig_name = "DmcStsRearToEscChks"
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

    class DmcStsRearToEscDmcSts:
        sig_name = "DmcStsRearToEscDmcSts"
        sig_start_bit = 11
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DMC_Init': 0, 'DMC_On': 1, 'DMC_Off': 2, 'DMC_Fault': 3}
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DmcStsRearToEsc_UB:
        sig_name = "DmcStsRearToEsc_UB"
        sig_start_bit = 56
        update_id_bit = 56
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
        startbit = 56
        byte = 7
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class DmcStsRearToEscDmcActAppTarTq:
        sig_name = "DmcStsRearToEscDmcActAppTarTq"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = -30000
        sig_value_max = 30000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class DmcStsRearToEscCntr:
        sig_name = "DmcStsRearToEscCntr"
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


class BgmPropulsionFr04:
    msg_name = "BgmPropulsionFr04"
    msg_id = 1018
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.32
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['ECM']
    sig_group_dict = {'CDCActT_1_BgmPropSignalIPdu04': ['CDCActTEngT_1_BgmPropSignalIPdu04', 'CDCActTEngTQf_1_BgmPropSignalIPdu04'], 'ACUActT_1_BgmPropSignalIPdu04': ['ACUActTEngT_1_BgmPropSignalIPdu04', 'ACUActTEngTQf_1_BgmPropSignalIPdu04']}
    sig_group_dataid_dict = {}

    class ACUCoolantFlwReq_1_BgmPropSignalIPdu04:
        sig_name = "ACUCoolantFlwReq_1_BgmPropSignalIPdu04"
        sig_start_bit = 23
        update_id_bit = 8
        sig_length = 9
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 511
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b10000000, 0b01111111, 1, 7)]

    class CDCActTEngTQf_1_BgmPropSignalIPdu04:
        sig_name = "CDCActTEngTQf_1_BgmPropSignalIPdu04"
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
        sig_value_table = {'Qf1_DevOfDataUndefd': 0, 'Qf1_DataTmpUndefdAndEvlnInProgs': 1, 'Qf1_DevOfDataNotWithinRngAllwd': 2, 'Qf1_DataCalcdWithDevDefd': 3}
        compute_method = None
        length = 2
        startbit = 47
        byte = 5
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class ACUActTEngTQf_1_BgmPropSignalIPdu04:
        sig_name = "ACUActTEngTQf_1_BgmPropSignalIPdu04"
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
        sig_value_table = {'Qf1_DevOfDataUndefd': 0, 'Qf1_DataTmpUndefdAndEvlnInProgs': 1, 'Qf1_DevOfDataNotWithinRngAllwd': 2, 'Qf1_DataCalcdWithDevDefd': 3}
        compute_method = None
        length = 2
        startbit = 15
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class CDCActTEngT_1_BgmPropSignalIPdu04:
        sig_name = "CDCActTEngT_1_BgmPropSignalIPdu04"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -50.0
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Motorola"
        sig_value_init = 50
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ACUActTEngT_1_BgmPropSignalIPdu04:
        sig_name = "ACUActTEngT_1_BgmPropSignalIPdu04"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -50.0
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Motorola"
        sig_value_init = 50
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CDCActT_1_BgmPropSignalIPdu04_UB:
        sig_name = "CDCActT_1_BgmPropSignalIPdu04_UB"
        sig_start_bit = 41
        update_id_bit = 41
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
        startbit = 41
        byte = 5
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class ACUActT_1_BgmPropSignalIPdu04_UB:
        sig_name = "ACUActT_1_BgmPropSignalIPdu04_UB"
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

    class CDCCoolantFlwReq_1_BgmPropSignalIPdu04:
        sig_name = "CDCCoolantFlwReq_1_BgmPropSignalIPdu04"
        sig_start_bit = 55
        update_id_bit = 40
        sig_length = 9
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 511
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 55
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b10000000, 0b01111111, 1, 7)]


class VddmPropulsionCANNmFr:
    msg_name = "VddmPropulsionCANNmFr"
    msg_id = 1318
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['SRS']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class CddIgmPropFr01:
    msg_name = "CddIgmPropFr01"
    msg_id = 331
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 8
    tx_node = "HVCM"
    rx_nodes = ['VDDM', 'ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class DcDcActvd:
        sig_name = "DcDcActvd"
        sig_start_bit = 25
        update_id_bit = 24
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DcDcActvd_NoConversionToLVSide': 0, 'DcDcActvd_ConversionToLVSide': 1}
        compute_method = None
        length = 1
        startbit = 25
        byte = 3
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class FltTDcDc:
        sig_name = "FltTDcDc"
        sig_start_bit = 9
        update_id_bit = 8
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevErrSts2_NoFlt': 0, 'DevErrSts2_Flt': 1}
        compute_method = None
        length = 1
        startbit = 9
        byte = 1
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class IDcDcActHiSide:
        sig_name = "IDcDcActHiSide"
        sig_start_bit = 23
        update_id_bit = 26
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = -410.0
        sig_value_min = 0
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 4100
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111000, 0b00000111, 5, 3)]

    class IDcDcAvlMaxLoSide:
        sig_name = "IDcDcAvlMaxLoSide"
        sig_start_bit = 55
        update_id_bit = 40
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 55
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b11110000, 0b00001111, 4, 4)]

    class UDcDcActHiSide:
        sig_name = "UDcDcActHiSide"
        sig_start_bit = 39
        update_id_bit = 42
        sig_length = 13
        sig_value_factor = 0.125
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 8184
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111000, 0b00000111, 5, 3)]

    class FltElecDcDc:
        sig_name = "FltElecDcDc"
        sig_start_bit = 11
        update_id_bit = 10
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevErrSts2_NoFlt': 0, 'DevErrSts2_Flt': 1}
        compute_method = None
        length = 1
        startbit = 11
        byte = 1
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3


class BecmPropFr11:
    msg_name = "BecmPropFr11"
    msg_id = 817
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 1.0
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['VDDM', 'ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class DCChrgnNegPortT:
        sig_name = "DCChrgnNegPortT"
        sig_start_bit = 63
        update_id_bit = 12
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -50.0
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Motorola"
        sig_value_init = 50
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvBattBalFlg:
        sig_name = "HvBattBalFlg"
        sig_start_bit = 11
        update_id_bit = 10
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

    class HvBattCooltT:
        sig_name = "HvBattCooltT"
        sig_start_bit = 47
        update_id_bit = 37
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -60.0
        sig_value_min = 0
        sig_value_max = 1850
        sig_byteorder = "Motorola"
        sig_value_init = 600
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11100000, 0b00011111, 3, 5)]

    class DCChrgnPosPortT:
        sig_name = "DCChrgnPosPortT"
        sig_start_bit = 31
        update_id_bit = 13
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -50.0
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Motorola"
        sig_value_init = 50
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvBattCoolgEgyReq1:
        sig_name = "HvBattCoolgEgyReq1"
        sig_start_bit = 7
        update_id_bit = 39
        sig_length = 10
        sig_value_factor = 20.0
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

    class HvBattCooltFlowReq:
        sig_name = "HvBattCooltFlowReq"
        sig_start_bit = 8
        update_id_bit = 38
        sig_length = 9
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]


class VgmToHvcmJ1979OBDPropCanReqFrame11:
    msg_name = "VgmToHvcmJ1979OBDPropCanReqFrame11"
    msg_id = 2021
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HVCM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class BecmPropFr29:
    msg_name = "BecmPropFr29"
    msg_id = 1161
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.9
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['ECM']
    sig_group_dict = {'HvBattThermInfoInFuture': ['HvBattThermInfoInFuturePwrAtTime', 'HvBattThermInfoInFutureSequenceNo', 'HvBattThermInfoInFutureTempAtTime', 'HvBattThermInfoInFutureThermModAtTime', 'HvBattThermInfoInFutureTime', 'HvBattThermInfoInFutureVersionNo']}
    sig_group_dataid_dict = {}

    class HvBattThermInfoInFutureTime:
        sig_name = "HvBattThermInfoInFutureTime"
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

    class HvBattThermInfoInFutureSequenceNo:
        sig_name = "HvBattThermInfoInFutureSequenceNo"
        sig_start_bit = 4
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
        startbit = 4
        byte = 0
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class HvBattThermInfoInFutureTempAtTime:
        sig_name = "HvBattThermInfoInFutureTempAtTime"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -50.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 50
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvBattThermInfoInFuturePwrAtTime:
        sig_name = "HvBattThermInfoInFuturePwrAtTime"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 50.0
        sig_value_offset = -25000.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 500
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111111, 0b00000000, 8, 0)]

    class HvBattThermInfoInFuture_UB:
        sig_name = "HvBattThermInfoInFuture_UB"
        sig_start_bit = 5
        update_id_bit = 5
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
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class HvBattThermInfoInFutureVersionNo:
        sig_name = "HvBattThermInfoInFutureVersionNo"
        sig_start_bit = 44
        update_id_bit = None
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
        startbit = 44
        byte = 5
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class HvBattThermInfoInFutureThermModAtTime:
        sig_name = "HvBattThermInfoInFutureThermModAtTime"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Idle': 0, 'ThermalBalancing': 1, 'PassiveHeating': 2, 'ActiveHeating': 3, 'PassiveCooling': 4, 'ActiveCooling': 5, 'CombinedCooling': 6, 'Reserved': 7}
        compute_method = None
        length = 3
        startbit = 47
        byte = 5
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5


class BgmPropulsionFr01:
    msg_name = "BgmPropulsionFr01"
    msg_id = 636
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['BECM1', 'S2SReceiver', 'EGSM', 'ECM']
    sig_group_dict = {'ExhibitionModeSts_1_BgmPropSignalIPdu01': ['ExhibitionModeStsChks_1_BgmPropSignalIPdu01', 'ExhibitionModeStsCntr_1_BgmPropSignalIPdu01', 'ExhibitionModeStsExhibitionModeSts_1_BgmPropSignalIPdu01']}
    sig_group_dataid_dict = {'ExhibitionModeSts_1_BgmPropSignalIPdu01': 9001}

    class ExhibitionModeSts_1_BgmPropSignalIPdu01_UB:
        sig_name = "ExhibitionModeSts_1_BgmPropSignalIPdu01_UB"
        sig_start_bit = 29
        update_id_bit = 29
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
        startbit = 29
        byte = 3
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class NOPCoolReqFromCDC_1_BgmPropSignalIPdu01:
        sig_name = "NOPCoolReqFromCDC_1_BgmPropSignalIPdu01"
        sig_start_bit = 6
        update_id_bit = 5
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
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class GearLvrIndcnInv:
        sig_name = "GearLvrIndcnInv"
        sig_start_bit = 47
        update_id_bit = 40
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 7
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GearLvrIndcnInv_P': 0, 'GearLvrIndcnInv_R': 1, 'GearLvrIndcnInv_D': 2, 'GearLvrIndcnInv_Reserved1': 3, 'GearLvrIndcnInv_Reserved2': 4, 'GearLvrIndcnInv_Reserved3': 5, 'GearLvrIndcnInv_Reserved4': 6, 'GearLvrIndcnInv_NOINDICATION': 7}
        compute_method = None
        length = 3
        startbit = 47
        byte = 5
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class ExhibitionModeStsChks_1_BgmPropSignalIPdu01:
        sig_name = "ExhibitionModeStsChks_1_BgmPropSignalIPdu01"
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

    class LocalHvBattThermTarT:
        sig_name = "LocalHvBattThermTarT"
        sig_start_bit = 55
        update_id_bit = 56
        sig_length = 8
        sig_value_factor = 0.5
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 80
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class LocalHvBattThermReq:
        sig_name = "LocalHvBattThermReq"
        sig_start_bit = 35
        update_id_bit = 32
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CmptSts_NoRequest': 0, 'CmptSts_CoolingRequest': 1, 'CmptSts_HeatingRequest': 2, 'CmptSts_CoolingAndHeatingRequest': 3, 'CmptSts_PostHeating': 4}
        compute_method = None
        length = 3
        startbit = 35
        byte = 4
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class RemHvBattHeatgTarT:
        sig_name = "RemHvBattHeatgTarT"
        sig_start_bit = 15
        update_id_bit = 3
        sig_length = 8
        sig_value_factor = 0.5
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 80
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ExhibitionModeStsExhibitionModeSts_1_BgmPropSignalIPdu01:
        sig_name = "ExhibitionModeStsExhibitionModeSts_1_BgmPropSignalIPdu01"
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

    class RemHvBattHeatgReq:
        sig_name = "RemHvBattHeatgReq"
        sig_start_bit = 7
        update_id_bit = 4
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'RemHvBattHeatgReq_OFF': 0, 'RemHvBattHeatgReq_ON': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ExhibitionModeStsCntr_1_BgmPropSignalIPdu01:
        sig_name = "ExhibitionModeStsCntr_1_BgmPropSignalIPdu01"
        sig_start_bit = 27
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
        startbit = 27
        byte = 3
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0


class EcmPropFr29:
    msg_name = "EcmPropFr29"
    msg_id = 278
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['BECM1']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HvAuxActPwr:
        sig_name = "HvAuxActPwr"
        sig_start_bit = 7
        update_id_bit = 13
        sig_length = 10
        sig_value_factor = 20.0
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


class MgmPropFr02:
    msg_name = "MgmPropFr02"
    msg_id = 1179
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.8
    msg_length = 8
    tx_node = "MGM"
    rx_nodes = ['CCM']
    sig_group_dict = {'MGMTestFr2': ['MGMTestFr2Byte0', 'MGMTestFr2Byte1', 'MGMTestFr2Byte2', 'MGMTestFr2Byte3', 'MGMTestFr2Byte4', 'MGMTestFr2Byte5', 'MGMTestFr2Byte6', 'MGMTestFr2Byte7']}
    sig_group_dataid_dict = {}

    class MGMTestFr2Byte0:
        sig_name = "MGMTestFr2Byte0"
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

    class MGMTestFr2Byte6:
        sig_name = "MGMTestFr2Byte6"
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

    class MGMTestFr2Byte1:
        sig_name = "MGMTestFr2Byte1"
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

    class MGMTestFr2Byte2:
        sig_name = "MGMTestFr2Byte2"
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

    class MGMTestFr2Byte5:
        sig_name = "MGMTestFr2Byte5"
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

    class MGMTestFr2Byte7:
        sig_name = "MGMTestFr2Byte7"
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

    class MGMTestFr2Byte3:
        sig_name = "MGMTestFr2Byte3"
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

    class MGMTestFr2Byte4:
        sig_name = "MGMTestFr2Byte4"
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


class SrsPropulsionCANNmFr:
    msg_name = "SrsPropulsionCANNmFr"
    msg_id = 1306
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "SRS"
    rx_nodes = ['MGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class EcmPropComFr10:
    msg_name = "EcmPropComFr10"
    msg_id = 341
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.025
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['EGSM', 'VDDM', 'CCM']
    sig_group_dict = {'TrsmParkLockd': ['TrsmParkLockdChks', 'TrsmParkLockdCntr', 'TrsmParkLockdTrsmParkLockd']}
    sig_group_dataid_dict = {'TrsmParkLockd': 50}

    class EGSMLightOn:
        sig_name = "EGSMLightOn"
        sig_start_bit = 7
        update_id_bit = 4
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EGSMLightOn_Default': 0, 'EGSMLightOn_LightOn': 1, 'EGSMLightOn_LightOff': 2}
        compute_method = None
        length = 3
        startbit = 7
        byte = 0
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class LgtCtrlModActvSts:
        sig_name = "LgtCtrlModActvSts"
        sig_start_bit = 3
        update_id_bit = 2
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
        startbit = 3
        byte = 0
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class TrsmParkLockdChks:
        sig_name = "TrsmParkLockdChks"
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

    class TrsmParkLockd_UB:
        sig_name = "TrsmParkLockd_UB"
        sig_start_bit = 22
        update_id_bit = 22
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
        startbit = 22
        byte = 2
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class TrsmParkLockdTrsmParkLockd:
        sig_name = "TrsmParkLockdTrsmParkLockd"
        sig_start_bit = 21
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 3
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TrsmParkLock1_ParkNotEngd': 0, 'TrsmParkLock1_ParkEngd': 1, 'TrsmParkLock1_NotInUse': 2, 'TrsmParkLock1_Undefd': 3}
        compute_method = None
        length = 2
        startbit = 21
        byte = 2
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class TrsmParkLockdCntr:
        sig_name = "TrsmParkLockdCntr"
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


class VgmToAllJ1979OBDPropCanReqFrame11:
    msg_name = "VgmToAllJ1979OBDPropCanReqFrame11"
    msg_id = 2015
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['MGM', 'BECM1', 'IEM', 'HVCM', 'ECM', 'VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class BecmToVddmPropDiagRespFrame:
    msg_name = "BecmToVddmPropDiagRespFrame"
    msg_id = 1589
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class BecmPropFr31:
    msg_name = "BecmPropFr31"
    msg_id = 261
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['S2SReceiver', 'ECM', 'CCM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class DCChrgrIMax:
        sig_name = "DCChrgrIMax"
        sig_start_bit = 7
        update_id_bit = 8
        sig_length = 15
        sig_value_factor = 0.1
        sig_value_offset = -1638.0
        sig_value_min = 0
        sig_value_max = 32767
        sig_byteorder = "Motorola"
        sig_value_init = 16380
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111110, 0b00000001, 7, 1)]


class VddmPropFr16:
    msg_name = "VddmPropFr16"
    msg_id = 597
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.08
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['IEM']
    sig_group_dict = {'ImobEngMgrReq2': ['ImobEngMgrReq2ImobEngDataMgrReq0', 'ImobEngMgrReq2ImobEngDataMgrReq1', 'ImobEngMgrReq2ImobEngDataMgrReq2', 'ImobEngMgrReq2ImobEngDataMgrReq3', 'ImobEngMgrReq2ImobEngDataMgrReq4', 'ImobEngMgrReq2ImobEngDataMgrReq5', 'ImobEngMgrReq2ImobEngDataMgrReq6', 'ImobEngMgrReq2ImobEngMgrCmdTar1']}
    sig_group_dataid_dict = {}

    class ImobEngMgrReq2_UB:
        sig_name = "ImobEngMgrReq2_UB"
        sig_start_bit = 2
        update_id_bit = 2
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
        startbit = 2
        byte = 0
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class ImobEngMgrReq2ImobEngDataMgrReq4:
        sig_name = "ImobEngMgrReq2ImobEngDataMgrReq4"
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

    class ImobEngMgrReq2ImobEngDataMgrReq2:
        sig_name = "ImobEngMgrReq2ImobEngDataMgrReq2"
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

    class ImobEngMgrReq2ImobEngDataMgrReq3:
        sig_name = "ImobEngMgrReq2ImobEngDataMgrReq3"
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

    class ImobEngMgrReq2ImobEngDataMgrReq6:
        sig_name = "ImobEngMgrReq2ImobEngDataMgrReq6"
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

    class ImobEngMgrReq2ImobEngMgrCmdTar1:
        sig_name = "ImobEngMgrReq2ImobEngMgrCmdTar1"
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
        sig_value_table = {'ImobEngMgrReqCmd_ImobEngCmdTarIdle': 0, 'ImobEngMgrReqCmd_ImobEngMtnStrtReqCmd': 1, 'ImobEngMgrReqCmd_ImobEngNoMtnStrtReqCmd': 2, 'ImobEngMgrReqCmd_ImobEngTurnOffCmd': 3}
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class ImobEngMgrReq2ImobEngDataMgrReq5:
        sig_name = "ImobEngMgrReq2ImobEngDataMgrReq5"
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

    class ImobEngMgrReq2ImobEngDataMgrReq0:
        sig_name = "ImobEngMgrReq2ImobEngDataMgrReq0"
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

    class ImobEngMgrReq2ImobEngDataMgrReq1:
        sig_name = "ImobEngMgrReq2ImobEngDataMgrReq1"
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


class EgsmPropFr01:
    msg_name = "EgsmPropFr01"
    msg_id = 309
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "EGSM"
    rx_nodes = ['BGM', 'S2SReceiver', 'ECM', 'VDDM']
    sig_group_dict = {'DrvrGearShiftParkReq': ['DrvrGearShiftParkReq1', 'DrvrGearShiftParkReqChks', 'DrvrGearShiftParkReqCntr', 'DrvrGearShiftParkReqSts']}
    sig_group_dataid_dict = {'DrvrGearShiftParkReq': 527}

    class DrvrGearShiftParkReqSts:
        sig_name = "DrvrGearShiftParkReqSts"
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
        sig_value_table = {'ClutchPedlPsd_No': 0, 'ClutchPedlPsd_Yes': 1, 'ClutchPedlPsd_Reserved1': 2, 'ClutchPedlPsd_Reserved2': 3}
        compute_method = None
        length = 2
        startbit = 13
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class GearLvrIllmnSts_0_EgsmPropSignalIPdu01:
        sig_name = "GearLvrIllmnSts_0_EgsmPropSignalIPdu01"
        sig_start_bit = 35
        update_id_bit = 34
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
        startbit = 35
        byte = 4
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class DrvrGearShiftReqInv:
        sig_name = "DrvrGearShiftReqInv"
        sig_start_bit = 47
        update_id_bit = 40
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DrvrGearShiftReqInv_NoPress': 0, 'DrvrGearShiftReqInv_PressP': 1, 'DrvrGearShiftReqInv_PressR': 2, 'DrvrGearShiftReqInv_PressD': 3, 'DrvrGearShiftReqInv_Reserved1': 4, 'DrvrGearShiftReqInv_Reserved2': 5, 'DrvrGearShiftReqInv_Reserved3': 6, 'DrvrGearShiftReqInv_Reserved4': 7}
        compute_method = None
        length = 3
        startbit = 47
        byte = 5
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class GearShiftUnitSts_0_EgsmPropSignalIPdu01:
        sig_name = "GearShiftUnitSts_0_EgsmPropSignalIPdu01"
        sig_start_bit = 26
        update_id_bit = 27
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoFlt': 0, 'NoUpTipAut': 1, 'NoDwnTipAut': 2, 'NoPark': 3, 'SrvRqrd': 4, 'NoUpUpTipAut': 5, 'NoDownDownTipAut': 6, 'Nounlock': 7}
        compute_method = None
        length = 3
        startbit = 26
        byte = 3
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class DrvrGearShiftParkReqCntr:
        sig_name = "DrvrGearShiftParkReqCntr"
        sig_start_bit = 11
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
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DrvrGearShiftParkReqChks:
        sig_name = "DrvrGearShiftParkReqChks"
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

    class GearLock:
        sig_name = "GearLock"
        sig_start_bit = 28
        update_id_bit = 29
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ActvInActv_Active': 0, 'ActvInActv_Inactive': 1}
        compute_method = None
        length = 1
        startbit = 28
        byte = 3
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class DrvrGearShiftParkReq_UB:
        sig_name = "DrvrGearShiftParkReq_UB"
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

    class DrvrGearShiftParkReq1:
        sig_name = "DrvrGearShiftParkReq1"
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
        sig_value_table = {'SwtPark1_SwtParkNotActv': 0, 'SwtPark1_SwtParkActv': 1}
        compute_method = None
        length = 1
        startbit = 14
        byte = 1
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6


class IemPropFr08:
    msg_name = "IemPropFr08"
    msg_id = 99
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "IEM"
    rx_nodes = ['ECM', 'VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class WhlMotSysHeatPwrAct:
        sig_name = "WhlMotSysHeatPwrAct"
        sig_start_bit = 31
        update_id_bit = 19
        sig_length = 8
        sig_value_factor = 50.0
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

    class WhlMotSysIdc:
        sig_name = "WhlMotSysIdc"
        sig_start_bit = 5
        update_id_bit = 6
        sig_length = 14
        sig_value_factor = 0.1
        sig_value_offset = -818.8
        sig_value_min = 0
        sig_value_max = 16380
        sig_byteorder = "Motorola"
        sig_value_init = 8188
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 14
        startbit = 5
        bmuws_info = [(0, 0b00111111, 0b11000000, 6, 0), (1, 0b11111111, 0b00000000, 8, 0)]


class BecmPropFr27:
    msg_name = "BecmPropFr27"
    msg_id = 1177
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 1.0
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['VDDM', 'ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HvBattCap:
        sig_name = "HvBattCap"
        sig_start_bit = 7
        update_id_bit = 23
        sig_length = 16
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 65535
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class TotChrgCap:
        sig_name = "TotChrgCap"
        sig_start_bit = 39
        update_id_bit = 22
        sig_length = 32
        sig_value_factor = 0.01
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 4294967295
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 32
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111111, 0b00000000, 8, 0)]


class HvcmToVgmJ1979OBDPropDiagResFrame11:
    msg_name = "HvcmToVgmJ1979OBDPropDiagResFrame11"
    msg_id = 2029
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "HVCM"
    rx_nodes = ['BGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class HvcmPropVFCVectorFr:
    msg_name = "HvcmPropVFCVectorFr"
    msg_id = 1366
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "HVCM"
    rx_nodes = ['CCM']
    sig_group_dict = {'VFCVectorHVCM': ['VFCVectorHVCMBlockID', 'VFCVectorHVCMVFCid0', 'VFCVectorHVCMVFCid1', 'VFCVectorHVCMVFCid10', 'VFCVectorHVCMVFCid11', 'VFCVectorHVCMVFCid12', 'VFCVectorHVCMVFCid13', 'VFCVectorHVCMVFCid14', 'VFCVectorHVCMVFCid15', 'VFCVectorHVCMVFCid16', 'VFCVectorHVCMVFCid17', 'VFCVectorHVCMVFCid18', 'VFCVectorHVCMVFCid19', 'VFCVectorHVCMVFCid2', 'VFCVectorHVCMVFCid20', 'VFCVectorHVCMVFCid21', 'VFCVectorHVCMVFCid22', 'VFCVectorHVCMVFCid23', 'VFCVectorHVCMVFCid24', 'VFCVectorHVCMVFCid25', 'VFCVectorHVCMVFCid26', 'VFCVectorHVCMVFCid27', 'VFCVectorHVCMVFCid28', 'VFCVectorHVCMVFCid29', 'VFCVectorHVCMVFCid3', 'VFCVectorHVCMVFCid30', 'VFCVectorHVCMVFCid31', 'VFCVectorHVCMVFCid32', 'VFCVectorHVCMVFCid33', 'VFCVectorHVCMVFCid34', 'VFCVectorHVCMVFCid35', 'VFCVectorHVCMVFCid36', 'VFCVectorHVCMVFCid37', 'VFCVectorHVCMVFCid38', 'VFCVectorHVCMVFCid39', 'VFCVectorHVCMVFCid4', 'VFCVectorHVCMVFCid40', 'VFCVectorHVCMVFCid41', 'VFCVectorHVCMVFCid42', 'VFCVectorHVCMVFCid43', 'VFCVectorHVCMVFCid44', 'VFCVectorHVCMVFCid45', 'VFCVectorHVCMVFCid46', 'VFCVectorHVCMVFCid47', 'VFCVectorHVCMVFCid48', 'VFCVectorHVCMVFCid49', 'VFCVectorHVCMVFCid5', 'VFCVectorHVCMVFCid50', 'VFCVectorHVCMVFCid51', 'VFCVectorHVCMVFCid52', 'VFCVectorHVCMVFCid53', 'VFCVectorHVCMVFCid54', 'VFCVectorHVCMVFCid55', 'VFCVectorHVCMVFCid56', 'VFCVectorHVCMVFCid57', 'VFCVectorHVCMVFCid58', 'VFCVectorHVCMVFCid59', 'VFCVectorHVCMVFCid6', 'VFCVectorHVCMVFCid60', 'VFCVectorHVCMVFCid61', 'VFCVectorHVCMVFCid7', 'VFCVectorHVCMVFCid8', 'VFCVectorHVCMVFCid9']}
    sig_group_dataid_dict = {}

    class VFCVectorHVCMVFCid29:
        sig_name = "VFCVectorHVCMVFCid29"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 31
        byte = 3
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorHVCMVFCid39:
        sig_name = "VFCVectorHVCMVFCid39"
        sig_start_bit = 41
        update_id_bit = None
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

    class VFCVectorHVCMVFCid21:
        sig_name = "VFCVectorHVCMVFCid21"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 23
        byte = 2
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorHVCMVFCid50:
        sig_name = "VFCVectorHVCMVFCid50"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorHVCMVFCid12:
        sig_name = "VFCVectorHVCMVFCid12"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 14
        byte = 1
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorHVCMVFCid16:
        sig_name = "VFCVectorHVCMVFCid16"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 18
        byte = 2
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorHVCMVFCid30:
        sig_name = "VFCVectorHVCMVFCid30"
        sig_start_bit = 32
        update_id_bit = None
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

    class VFCVectorHVCMVFCid0:
        sig_name = "VFCVectorHVCMVFCid0"
        sig_start_bit = 2
        update_id_bit = None
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

    class VFCVectorHVCMVFCid41:
        sig_name = "VFCVectorHVCMVFCid41"
        sig_start_bit = 43
        update_id_bit = None
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

    class VFCVectorHVCMVFCid19:
        sig_name = "VFCVectorHVCMVFCid19"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 21
        byte = 2
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorHVCMVFCid1:
        sig_name = "VFCVectorHVCMVFCid1"
        sig_start_bit = 3
        update_id_bit = None
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

    class VFCVectorHVCMVFCid8:
        sig_name = "VFCVectorHVCMVFCid8"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 10
        byte = 1
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorHVCMBlockID:
        sig_name = "VFCVectorHVCMBlockID"
        sig_start_bit = 1
        update_id_bit = None
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

    class VFCVectorHVCMVFCid61:
        sig_name = "VFCVectorHVCMVFCid61"
        sig_start_bit = 63
        update_id_bit = None
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

    class VFCVectorHVCMVFCid11:
        sig_name = "VFCVectorHVCMVFCid11"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 13
        byte = 1
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorHVCMVFCid18:
        sig_name = "VFCVectorHVCMVFCid18"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 20
        byte = 2
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorHVCMVFCid40:
        sig_name = "VFCVectorHVCMVFCid40"
        sig_start_bit = 42
        update_id_bit = None
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

    class VFCVectorHVCMVFCid46:
        sig_name = "VFCVectorHVCMVFCid46"
        sig_start_bit = 48
        update_id_bit = None
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

    class VFCVectorHVCMVFCid38:
        sig_name = "VFCVectorHVCMVFCid38"
        sig_start_bit = 40
        update_id_bit = None
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

    class VFCVectorHVCMVFCid43:
        sig_name = "VFCVectorHVCMVFCid43"
        sig_start_bit = 45
        update_id_bit = None
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

    class VFCVectorHVCMVFCid4:
        sig_name = "VFCVectorHVCMVFCid4"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorHVCMVFCid60:
        sig_name = "VFCVectorHVCMVFCid60"
        sig_start_bit = 62
        update_id_bit = None
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

    class VFCVectorHVCMVFCid57:
        sig_name = "VFCVectorHVCMVFCid57"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 59
        byte = 7
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorHVCMVFCid26:
        sig_name = "VFCVectorHVCMVFCid26"
        sig_start_bit = 28
        update_id_bit = None
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

    class VFCVectorHVCMVFCid58:
        sig_name = "VFCVectorHVCMVFCid58"
        sig_start_bit = 60
        update_id_bit = None
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

    class VFCVectorHVCMVFCid55:
        sig_name = "VFCVectorHVCMVFCid55"
        sig_start_bit = 57
        update_id_bit = None
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

    class VFCVectorHVCMVFCid51:
        sig_name = "VFCVectorHVCMVFCid51"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 53
        byte = 6
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorHVCMVFCid48:
        sig_name = "VFCVectorHVCMVFCid48"
        sig_start_bit = 50
        update_id_bit = None
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

    class VFCVectorHVCMVFCid25:
        sig_name = "VFCVectorHVCMVFCid25"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 27
        byte = 3
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorHVCMVFCid20:
        sig_name = "VFCVectorHVCMVFCid20"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 22
        byte = 2
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorHVCMVFCid6:
        sig_name = "VFCVectorHVCMVFCid6"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 8
        byte = 1
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorHVCMVFCid37:
        sig_name = "VFCVectorHVCMVFCid37"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 39
        byte = 4
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorHVCMVFCid9:
        sig_name = "VFCVectorHVCMVFCid9"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 11
        byte = 1
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorHVCMVFCid22:
        sig_name = "VFCVectorHVCMVFCid22"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 24
        byte = 3
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorHVCMVFCid59:
        sig_name = "VFCVectorHVCMVFCid59"
        sig_start_bit = 61
        update_id_bit = None
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

    class VFCVectorHVCMVFCid34:
        sig_name = "VFCVectorHVCMVFCid34"
        sig_start_bit = 36
        update_id_bit = None
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

    class VFCVectorHVCMVFCid28:
        sig_name = "VFCVectorHVCMVFCid28"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 30
        byte = 3
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorHVCMVFCid42:
        sig_name = "VFCVectorHVCMVFCid42"
        sig_start_bit = 44
        update_id_bit = None
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

    class VFCVectorHVCMVFCid56:
        sig_name = "VFCVectorHVCMVFCid56"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 58
        byte = 7
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorHVCMVFCid23:
        sig_name = "VFCVectorHVCMVFCid23"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 25
        byte = 3
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorHVCMVFCid35:
        sig_name = "VFCVectorHVCMVFCid35"
        sig_start_bit = 37
        update_id_bit = None
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

    class VFCVectorHVCMVFCid14:
        sig_name = "VFCVectorHVCMVFCid14"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 16
        byte = 2
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorHVCMVFCid33:
        sig_name = "VFCVectorHVCMVFCid33"
        sig_start_bit = 35
        update_id_bit = None
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

    class VFCVectorHVCMVFCid13:
        sig_name = "VFCVectorHVCMVFCid13"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 15
        byte = 1
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorHVCMVFCid24:
        sig_name = "VFCVectorHVCMVFCid24"
        sig_start_bit = 26
        update_id_bit = None
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

    class VFCVectorHVCMVFCid10:
        sig_name = "VFCVectorHVCMVFCid10"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 12
        byte = 1
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorHVCMVFCid15:
        sig_name = "VFCVectorHVCMVFCid15"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 17
        byte = 2
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorHVCMVFCid31:
        sig_name = "VFCVectorHVCMVFCid31"
        sig_start_bit = 33
        update_id_bit = None
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

    class VFCVectorHVCMVFCid3:
        sig_name = "VFCVectorHVCMVFCid3"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorHVCMVFCid17:
        sig_name = "VFCVectorHVCMVFCid17"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 19
        byte = 2
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorHVCMVFCid5:
        sig_name = "VFCVectorHVCMVFCid5"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorHVCMVFCid32:
        sig_name = "VFCVectorHVCMVFCid32"
        sig_start_bit = 34
        update_id_bit = None
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

    class VFCVectorHVCMVFCid2:
        sig_name = "VFCVectorHVCMVFCid2"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 4
        byte = 0
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorHVCMVFCid44:
        sig_name = "VFCVectorHVCMVFCid44"
        sig_start_bit = 46
        update_id_bit = None
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

    class VFCVectorHVCMVFCid45:
        sig_name = "VFCVectorHVCMVFCid45"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 47
        byte = 5
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorHVCMVFCid53:
        sig_name = "VFCVectorHVCMVFCid53"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 55
        byte = 6
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorHVCMVFCid49:
        sig_name = "VFCVectorHVCMVFCid49"
        sig_start_bit = 51
        update_id_bit = None
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

    class VFCVectorHVCMVFCid7:
        sig_name = "VFCVectorHVCMVFCid7"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 9
        byte = 1
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorHVCMVFCid36:
        sig_name = "VFCVectorHVCMVFCid36"
        sig_start_bit = 38
        update_id_bit = None
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

    class VFCVectorHVCMVFCid47:
        sig_name = "VFCVectorHVCMVFCid47"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 49
        byte = 6
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorHVCMVFCid52:
        sig_name = "VFCVectorHVCMVFCid52"
        sig_start_bit = 54
        update_id_bit = None
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

    class VFCVectorHVCMVFCid27:
        sig_name = "VFCVectorHVCMVFCid27"
        sig_start_bit = 29
        update_id_bit = None
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

    class VFCVectorHVCMVFCid54:
        sig_name = "VFCVectorHVCMVFCid54"
        sig_start_bit = 56
        update_id_bit = None
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


class MgmPropdTCFr09:
    msg_name = "MgmPropdTCFr09"
    msg_id = 299
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "MGM"
    rx_nodes = ['VDDM']
    sig_group_dict = {'DmcStsFrntToEsc': ['DmcStsFrntToEscChks', 'DmcStsFrntToEscCntr', 'DmcStsFrntToEscDmcActAppTarTq', 'DmcStsFrntToEscDmcSts', 'DmcStsFrntToEscDmcSWInfo']}
    sig_group_dataid_dict = {'DmcStsFrntToEsc': 6014}

    class DmcStsFrntToEscDmcActAppTarTq:
        sig_name = "DmcStsFrntToEscDmcActAppTarTq"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = -30000
        sig_value_max = 30000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class DmcStsFrntToEscDmcSWInfo:
        sig_name = "DmcStsFrntToEscDmcSWInfo"
        sig_start_bit = 39
        update_id_bit = None
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
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class DmcStsFrntToEscChks:
        sig_name = "DmcStsFrntToEscChks"
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

    class DmcStsFrntToEscCntr:
        sig_name = "DmcStsFrntToEscCntr"
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

    class DmcStsFrntToEscDmcSts:
        sig_name = "DmcStsFrntToEscDmcSts"
        sig_start_bit = 11
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DMC_Init': 0, 'DMC_On': 1, 'DMC_Off': 2, 'DMC_Fault': 3}
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DmcStsFrntToEsc_UB:
        sig_name = "DmcStsFrntToEsc_UB"
        sig_start_bit = 56
        update_id_bit = 56
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
        startbit = 56
        byte = 7
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0


class VgmToIemJ1979OBDPropCanReqFrame11:
    msg_name = "VgmToIemJ1979OBDPropCanReqFrame11"
    msg_id = 2019
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['IEM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class IemPropFr01:
    msg_name = "IemPropFr01"
    msg_id = 1111
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.8
    msg_length = 8
    tx_node = "IEM"
    rx_nodes = ['CCM']
    sig_group_dict = {'IEMTestFr1': ['IEMTestFr1Byte0', 'IEMTestFr1Byte1', 'IEMTestFr1Byte2', 'IEMTestFr1Byte3', 'IEMTestFr1Byte4', 'IEMTestFr1Byte5', 'IEMTestFr1Byte6', 'IEMTestFr1Byte7']}
    sig_group_dataid_dict = {}

    class IEMTestFr1Byte3:
        sig_name = "IEMTestFr1Byte3"
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

    class IEMTestFr1Byte1:
        sig_name = "IEMTestFr1Byte1"
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

    class IEMTestFr1Byte5:
        sig_name = "IEMTestFr1Byte5"
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

    class IEMTestFr1Byte7:
        sig_name = "IEMTestFr1Byte7"
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

    class IEMTestFr1Byte2:
        sig_name = "IEMTestFr1Byte2"
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

    class IEMTestFr1Byte4:
        sig_name = "IEMTestFr1Byte4"
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

    class IEMTestFr1Byte0:
        sig_name = "IEMTestFr1Byte0"
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

    class IEMTestFr1Byte6:
        sig_name = "IEMTestFr1Byte6"
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


class BecmPropFr28:
    msg_name = "BecmPropFr28"
    msg_id = 1180
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 1.0
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class TotDchaCap:
        sig_name = "TotDchaCap"
        sig_start_bit = 7
        update_id_bit = 39
        sig_length = 32
        sig_value_factor = 0.01
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


class BgmPropulsionCANNmFr:
    msg_name = "BgmPropulsionCANNmFr"
    msg_id = 1281
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['BECM1']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class EcmToVddmPropDiagRespFrame:
    msg_name = "EcmToVddmPropDiagRespFrame"
    msg_id = 1584
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class BecmPropVFCVectorFr:
    msg_name = "BecmPropVFCVectorFr"
    msg_id = 1345
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['CCM']
    sig_group_dict = {'VFCVectorBECM': ['VFCVectorBECMBlockID', 'VFCVectorBECMVFCid0', 'VFCVectorBECMVFCid1', 'VFCVectorBECMVFCid10', 'VFCVectorBECMVFCid11', 'VFCVectorBECMVFCid12', 'VFCVectorBECMVFCid13', 'VFCVectorBECMVFCid14', 'VFCVectorBECMVFCid15', 'VFCVectorBECMVFCid16', 'VFCVectorBECMVFCid17', 'VFCVectorBECMVFCid18', 'VFCVectorBECMVFCid19', 'VFCVectorBECMVFCid2', 'VFCVectorBECMVFCid20', 'VFCVectorBECMVFCid21', 'VFCVectorBECMVFCid22', 'VFCVectorBECMVFCid23', 'VFCVectorBECMVFCid24', 'VFCVectorBECMVFCid25', 'VFCVectorBECMVFCid26', 'VFCVectorBECMVFCid27', 'VFCVectorBECMVFCid28', 'VFCVectorBECMVFCid29', 'VFCVectorBECMVFCid3', 'VFCVectorBECMVFCid30', 'VFCVectorBECMVFCid31', 'VFCVectorBECMVFCid32', 'VFCVectorBECMVFCid33', 'VFCVectorBECMVFCid34', 'VFCVectorBECMVFCid35', 'VFCVectorBECMVFCid36', 'VFCVectorBECMVFCid37', 'VFCVectorBECMVFCid38', 'VFCVectorBECMVFCid39', 'VFCVectorBECMVFCid4', 'VFCVectorBECMVFCid40', 'VFCVectorBECMVFCid41', 'VFCVectorBECMVFCid42', 'VFCVectorBECMVFCid43', 'VFCVectorBECMVFCid44', 'VFCVectorBECMVFCid45', 'VFCVectorBECMVFCid46', 'VFCVectorBECMVFCid47', 'VFCVectorBECMVFCid48', 'VFCVectorBECMVFCid49', 'VFCVectorBECMVFCid5', 'VFCVectorBECMVFCid50', 'VFCVectorBECMVFCid51', 'VFCVectorBECMVFCid52', 'VFCVectorBECMVFCid53', 'VFCVectorBECMVFCid54', 'VFCVectorBECMVFCid55', 'VFCVectorBECMVFCid56', 'VFCVectorBECMVFCid57', 'VFCVectorBECMVFCid58', 'VFCVectorBECMVFCid59', 'VFCVectorBECMVFCid6', 'VFCVectorBECMVFCid60', 'VFCVectorBECMVFCid61', 'VFCVectorBECMVFCid7', 'VFCVectorBECMVFCid8', 'VFCVectorBECMVFCid9']}
    sig_group_dataid_dict = {}

    class VFCVectorBECMVFCid21:
        sig_name = "VFCVectorBECMVFCid21"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 23
        byte = 2
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorBECMVFCid38:
        sig_name = "VFCVectorBECMVFCid38"
        sig_start_bit = 40
        update_id_bit = None
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

    class VFCVectorBECMVFCid59:
        sig_name = "VFCVectorBECMVFCid59"
        sig_start_bit = 61
        update_id_bit = None
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

    class VFCVectorBECMVFCid14:
        sig_name = "VFCVectorBECMVFCid14"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 16
        byte = 2
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorBECMBlockID:
        sig_name = "VFCVectorBECMBlockID"
        sig_start_bit = 1
        update_id_bit = None
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

    class VFCVectorBECMVFCid15:
        sig_name = "VFCVectorBECMVFCid15"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 17
        byte = 2
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorBECMVFCid12:
        sig_name = "VFCVectorBECMVFCid12"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 14
        byte = 1
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorBECMVFCid1:
        sig_name = "VFCVectorBECMVFCid1"
        sig_start_bit = 3
        update_id_bit = None
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

    class VFCVectorBECMVFCid35:
        sig_name = "VFCVectorBECMVFCid35"
        sig_start_bit = 37
        update_id_bit = None
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

    class VFCVectorBECMVFCid40:
        sig_name = "VFCVectorBECMVFCid40"
        sig_start_bit = 42
        update_id_bit = None
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

    class VFCVectorBECMVFCid43:
        sig_name = "VFCVectorBECMVFCid43"
        sig_start_bit = 45
        update_id_bit = None
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

    class VFCVectorBECMVFCid52:
        sig_name = "VFCVectorBECMVFCid52"
        sig_start_bit = 54
        update_id_bit = None
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

    class VFCVectorBECMVFCid57:
        sig_name = "VFCVectorBECMVFCid57"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 59
        byte = 7
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorBECMVFCid50:
        sig_name = "VFCVectorBECMVFCid50"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorBECMVFCid27:
        sig_name = "VFCVectorBECMVFCid27"
        sig_start_bit = 29
        update_id_bit = None
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

    class VFCVectorBECMVFCid37:
        sig_name = "VFCVectorBECMVFCid37"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 39
        byte = 4
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorBECMVFCid13:
        sig_name = "VFCVectorBECMVFCid13"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 15
        byte = 1
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorBECMVFCid54:
        sig_name = "VFCVectorBECMVFCid54"
        sig_start_bit = 56
        update_id_bit = None
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

    class VFCVectorBECMVFCid47:
        sig_name = "VFCVectorBECMVFCid47"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 49
        byte = 6
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorBECMVFCid32:
        sig_name = "VFCVectorBECMVFCid32"
        sig_start_bit = 34
        update_id_bit = None
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

    class VFCVectorBECMVFCid24:
        sig_name = "VFCVectorBECMVFCid24"
        sig_start_bit = 26
        update_id_bit = None
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

    class VFCVectorBECMVFCid19:
        sig_name = "VFCVectorBECMVFCid19"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 21
        byte = 2
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorBECMVFCid53:
        sig_name = "VFCVectorBECMVFCid53"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 55
        byte = 6
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorBECMVFCid4:
        sig_name = "VFCVectorBECMVFCid4"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorBECMVFCid10:
        sig_name = "VFCVectorBECMVFCid10"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 12
        byte = 1
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorBECMVFCid20:
        sig_name = "VFCVectorBECMVFCid20"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 22
        byte = 2
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorBECMVFCid61:
        sig_name = "VFCVectorBECMVFCid61"
        sig_start_bit = 63
        update_id_bit = None
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

    class VFCVectorBECMVFCid49:
        sig_name = "VFCVectorBECMVFCid49"
        sig_start_bit = 51
        update_id_bit = None
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

    class VFCVectorBECMVFCid28:
        sig_name = "VFCVectorBECMVFCid28"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 30
        byte = 3
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorBECMVFCid29:
        sig_name = "VFCVectorBECMVFCid29"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 31
        byte = 3
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorBECMVFCid5:
        sig_name = "VFCVectorBECMVFCid5"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorBECMVFCid60:
        sig_name = "VFCVectorBECMVFCid60"
        sig_start_bit = 62
        update_id_bit = None
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

    class VFCVectorBECMVFCid58:
        sig_name = "VFCVectorBECMVFCid58"
        sig_start_bit = 60
        update_id_bit = None
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

    class VFCVectorBECMVFCid23:
        sig_name = "VFCVectorBECMVFCid23"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 25
        byte = 3
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorBECMVFCid25:
        sig_name = "VFCVectorBECMVFCid25"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 27
        byte = 3
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorBECMVFCid55:
        sig_name = "VFCVectorBECMVFCid55"
        sig_start_bit = 57
        update_id_bit = None
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

    class VFCVectorBECMVFCid7:
        sig_name = "VFCVectorBECMVFCid7"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 9
        byte = 1
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorBECMVFCid31:
        sig_name = "VFCVectorBECMVFCid31"
        sig_start_bit = 33
        update_id_bit = None
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

    class VFCVectorBECMVFCid45:
        sig_name = "VFCVectorBECMVFCid45"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 47
        byte = 5
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorBECMVFCid56:
        sig_name = "VFCVectorBECMVFCid56"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 58
        byte = 7
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorBECMVFCid26:
        sig_name = "VFCVectorBECMVFCid26"
        sig_start_bit = 28
        update_id_bit = None
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

    class VFCVectorBECMVFCid16:
        sig_name = "VFCVectorBECMVFCid16"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 18
        byte = 2
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorBECMVFCid30:
        sig_name = "VFCVectorBECMVFCid30"
        sig_start_bit = 32
        update_id_bit = None
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

    class VFCVectorBECMVFCid36:
        sig_name = "VFCVectorBECMVFCid36"
        sig_start_bit = 38
        update_id_bit = None
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

    class VFCVectorBECMVFCid39:
        sig_name = "VFCVectorBECMVFCid39"
        sig_start_bit = 41
        update_id_bit = None
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

    class VFCVectorBECMVFCid41:
        sig_name = "VFCVectorBECMVFCid41"
        sig_start_bit = 43
        update_id_bit = None
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

    class VFCVectorBECMVFCid44:
        sig_name = "VFCVectorBECMVFCid44"
        sig_start_bit = 46
        update_id_bit = None
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

    class VFCVectorBECMVFCid3:
        sig_name = "VFCVectorBECMVFCid3"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorBECMVFCid8:
        sig_name = "VFCVectorBECMVFCid8"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 10
        byte = 1
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorBECMVFCid33:
        sig_name = "VFCVectorBECMVFCid33"
        sig_start_bit = 35
        update_id_bit = None
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

    class VFCVectorBECMVFCid48:
        sig_name = "VFCVectorBECMVFCid48"
        sig_start_bit = 50
        update_id_bit = None
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

    class VFCVectorBECMVFCid18:
        sig_name = "VFCVectorBECMVFCid18"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 20
        byte = 2
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorBECMVFCid51:
        sig_name = "VFCVectorBECMVFCid51"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 53
        byte = 6
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorBECMVFCid42:
        sig_name = "VFCVectorBECMVFCid42"
        sig_start_bit = 44
        update_id_bit = None
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

    class VFCVectorBECMVFCid34:
        sig_name = "VFCVectorBECMVFCid34"
        sig_start_bit = 36
        update_id_bit = None
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

    class VFCVectorBECMVFCid17:
        sig_name = "VFCVectorBECMVFCid17"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 19
        byte = 2
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorBECMVFCid6:
        sig_name = "VFCVectorBECMVFCid6"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 8
        byte = 1
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorBECMVFCid0:
        sig_name = "VFCVectorBECMVFCid0"
        sig_start_bit = 2
        update_id_bit = None
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

    class VFCVectorBECMVFCid11:
        sig_name = "VFCVectorBECMVFCid11"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 13
        byte = 1
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorBECMVFCid2:
        sig_name = "VFCVectorBECMVFCid2"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 4
        byte = 0
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorBECMVFCid9:
        sig_name = "VFCVectorBECMVFCid9"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 11
        byte = 1
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorBECMVFCid22:
        sig_name = "VFCVectorBECMVFCid22"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 24
        byte = 3
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorBECMVFCid46:
        sig_name = "VFCVectorBECMVFCid46"
        sig_start_bit = 48
        update_id_bit = None
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


class BecmPropFr21:
    msg_name = "BecmPropFr21"
    msg_id = 648
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['VDDM', 'ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class DCChrgSt:
        sig_name = "DCChrgSt"
        sig_start_bit = 39
        update_id_bit = 20
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

    class HvBattChrgnTiEstimd:
        sig_name = "HvBattChrgnTiEstimd"
        sig_start_bit = 18
        update_id_bit = 19
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
        startbit = 18
        bmuws_info = [(2, 0b00000111, 0b11111000, 3, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class FastChrgnLEDIndctn:
        sig_name = "FastChrgnLEDIndctn"
        sig_start_bit = 35
        update_id_bit = 41
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FastChrgnLEDIndctn_Default': 0, 'FastChrgnLEDIndctn_Green1': 1, 'FastChrgnLEDIndctn_Green2': 2, 'FastChrgnLEDIndctn_Green3': 3, 'FastChrgnLEDIndctn_Green4': 4, 'FastChrgnLEDIndctn_Red': 5, 'FastChrgnLEDIndctn_Green5': 6, 'FastChrgnLEDIndctn_Reserved': 7}
        compute_method = None
        length = 3
        startbit = 35
        byte = 4
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class HvIsoR:
        sig_name = "HvIsoR"
        sig_start_bit = 7
        update_id_bit = 23
        sig_length = 16
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 60000
        sig_byteorder = "Motorola"
        sig_value_init = 5000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class HvBattWMDSts:
        sig_name = "HvBattWMDSts"
        sig_start_bit = 55
        update_id_bit = 49
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
        startbit = 55
        byte = 6
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2


class BecmPropFr22:
    msg_name = "BecmPropFr22"
    msg_id = 83
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['VDDM', 'ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class CPSRU:
        sig_name = "CPSRU"
        sig_start_bit = 39
        update_id_bit = 24
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
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvBattSupChrgThermSts:
        sig_name = "HvBattSupChrgThermSts"
        sig_start_bit = 22
        update_id_bit = 23
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ThermSts1_Idle': 0, 'ThermSts1_Prestart': 1, 'ThermSts1_Standby': 2, 'ThermSts1_Active': 3, 'ThermSts1_off': 4}
        compute_method = None
        length = 4
        startbit = 22
        byte = 2
        mask = 0b01111000
        unmask = 0b10000111
        shift = 3

    class ChrgEquipIDc:
        sig_name = "ChrgEquipIDc"
        sig_start_bit = 47
        update_id_bit = 48
        sig_length = 15
        sig_value_factor = 0.1
        sig_value_offset = -1638.0
        sig_value_min = 0
        sig_value_max = 32767
        sig_byteorder = "Motorola"
        sig_value_init = 16380
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111110, 0b00000001, 7, 1)]


class Ecm3PropDvelFr01:
    msg_name = "Ecm3PropDvelFr01"
    msg_id = 1530
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['CCM']
    sig_group_dict = {'Ecm3develpsignalgroup': ['Ecm3develpsignalgroupFunctiondevpsignalgroup1', 'Ecm3develpsignalgroupFunctiondevpsignalgroup2', 'Ecm3develpsignalgroupFunctiondevpsignalgroup3', 'Ecm3develpsignalgroupFunctiondevpsignalgroup4', 'Ecm3develpsignalgroupFunctiondevpsignalgroup5', 'Ecm3develpsignalgroupFunctiondevpsignalgroup6', 'Ecm3develpsignalgroupFunctiondevpsignalgroup7', 'Ecm3develpsignalgroupFunctiondevpsignalgroup8']}
    sig_group_dataid_dict = {}

    class Ecm3develpsignalgroupFunctiondevpsignalgroup3:
        sig_name = "Ecm3develpsignalgroupFunctiondevpsignalgroup3"
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

    class Ecm3develpsignalgroupFunctiondevpsignalgroup1:
        sig_name = "Ecm3develpsignalgroupFunctiondevpsignalgroup1"
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

    class Ecm3develpsignalgroupFunctiondevpsignalgroup5:
        sig_name = "Ecm3develpsignalgroupFunctiondevpsignalgroup5"
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

    class Ecm3develpsignalgroupFunctiondevpsignalgroup7:
        sig_name = "Ecm3develpsignalgroupFunctiondevpsignalgroup7"
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

    class Ecm3develpsignalgroupFunctiondevpsignalgroup2:
        sig_name = "Ecm3develpsignalgroupFunctiondevpsignalgroup2"
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

    class Ecm3develpsignalgroupFunctiondevpsignalgroup6:
        sig_name = "Ecm3develpsignalgroupFunctiondevpsignalgroup6"
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

    class Ecm3develpsignalgroupFunctiondevpsignalgroup8:
        sig_name = "Ecm3develpsignalgroupFunctiondevpsignalgroup8"
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

    class Ecm3develpsignalgroupFunctiondevpsignalgroup4:
        sig_name = "Ecm3develpsignalgroupFunctiondevpsignalgroup4"
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


class EcmPropFr14:
    msg_name = "EcmPropFr14"
    msg_id = 1160
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.8
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']
    sig_group_dict = {'HvBattThermInfoCorrInFuture': ['HvBattThermInfoCorrInFuturePwrAtTime', 'HvBattThermInfoCorrInFutureSequenceNo', 'HvBattThermInfoCorrInFutureTempAtTime', 'HvBattThermInfoCorrInFutureThermModAtTime', 'HvBattThermInfoCorrInFutureTime', 'HvBattThermInfoCorrInFutureVersionNo']}
    sig_group_dataid_dict = {}

    class HvBattThermInfoCorrInFutureTempAtTime:
        sig_name = "HvBattThermInfoCorrInFutureTempAtTime"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -50.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 50
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvBattThermInfoCorrInFuture_UB:
        sig_name = "HvBattThermInfoCorrInFuture_UB"
        sig_start_bit = 5
        update_id_bit = 5
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
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class HvBattThermInfoCorrInFutureSequenceNo:
        sig_name = "HvBattThermInfoCorrInFutureSequenceNo"
        sig_start_bit = 4
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
        startbit = 4
        byte = 0
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class HvBattThermInfoCorrInFutureVersionNo:
        sig_name = "HvBattThermInfoCorrInFutureVersionNo"
        sig_start_bit = 44
        update_id_bit = None
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
        startbit = 44
        byte = 5
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class HvBattThermInfoCorrInFutureTime:
        sig_name = "HvBattThermInfoCorrInFutureTime"
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

    class HvBattThermInfoCorrInFutureThermModAtTime:
        sig_name = "HvBattThermInfoCorrInFutureThermModAtTime"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Idle': 0, 'ThermalBalancing': 1, 'PassiveHeating': 2, 'ActiveHeating': 3, 'PassiveCooling': 4, 'ActiveCooling': 5, 'CombinedCooling': 6, 'Reserved': 7}
        compute_method = None
        length = 3
        startbit = 47
        byte = 5
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class HvBattThermInfoCorrInFuturePwrAtTime:
        sig_name = "HvBattThermInfoCorrInFuturePwrAtTime"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 50.0
        sig_value_offset = -25000.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 500
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 15
        bmuws_info = [(1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111111, 0b00000000, 8, 0)]


