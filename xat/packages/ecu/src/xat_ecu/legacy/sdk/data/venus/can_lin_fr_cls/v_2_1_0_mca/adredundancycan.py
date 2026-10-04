class BbmAdRedundancyFr14:
    msg_name = "BbmAdRedundancyFr14"
    msg_id = 86
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "BBM"
    rx_nodes = ['CDC', 'ACU']
    sig_group_dict = {'WhlVAgrFrntForBkp': ['WhlVAgrFrntForBkpWhlVAgrFrntLe', 'WhlVAgrFrntForBkpWhlVAgrFrntLeQf', 'WhlVAgrFrntForBkpWhlVAgrFrntRi', 'WhlVAgrFrntForBkpWhlVAgrFrntRiQf']}
    sig_group_dataid_dict = {}

    class WhlVAgrFrntForBkpWhlVAgrFrntRiQf:
        sig_name = "WhlVAgrFrntForBkpWhlVAgrFrntRiQf"
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
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 9
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class WhlVAgrFrntForBkpWhlVAgrFrntLe:
        sig_name = "WhlVAgrFrntForBkpWhlVAgrFrntLe"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 0.0078125
        sig_value_offset = 0.0
        sig_value_min = -32640
        sig_value_max = 32640
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class WhlVAgrFrntForBkp_UB:
        sig_name = "WhlVAgrFrntForBkp_UB"
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

    class WhlVAgrFrntForBkpWhlVAgrFrntRi:
        sig_name = "WhlVAgrFrntForBkpWhlVAgrFrntRi"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 0.0078125
        sig_value_offset = 0.0
        sig_value_min = -32640
        sig_value_max = 32640
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class WhlVAgrFrntForBkpWhlVAgrFrntLeQf:
        sig_name = "WhlVAgrFrntForBkpWhlVAgrFrntLeQf"
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
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 11
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2


class PscmAdRedundancyFr02:
    msg_name = "PscmAdRedundancyFr02"
    msg_id = 48
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "PSCM2"
    rx_nodes = ['CDC']
    sig_group_dict = {'ADL3LatCtrlStsForBkp': ['ADL3LatCtrlStsForBkpADMod', 'ADL3LatCtrlStsForBkpChks', 'ADL3LatCtrlStsForBkpCntr', 'ADL3LatCtrlStsForBkpCtrlSts', 'ADL3LatCtrlStsForBkpDegraded', 'ADL3LatCtrlStsForBkpQf', 'ADL3LatCtrlStsForBkpSts']}
    sig_group_dataid_dict = {'ADL3LatCtrlStsForBkp': 1121}

    class ADL3LatCtrlStsForBkpQf:
        sig_name = "ADL3LatCtrlStsForBkpQf"
        sig_start_bit = 4
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
        startbit = 4
        byte = 0
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class ADL3LatCtrlStsForBkpSts:
        sig_name = "ADL3LatCtrlStsForBkpSts"
        sig_start_bit = 6
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ColorSts_Red': 0, 'ColorSts_Yellow': 1, 'ColorSts_Green': 2, 'ColorSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 6
        byte = 0
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class ADL3LatCtrlStsForBkpChks:
        sig_name = "ADL3LatCtrlStsForBkpChks"
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

    class ADL3LatCtrlStsForBkpADMod:
        sig_name = "ADL3LatCtrlStsForBkpADMod"
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
        sig_value_table = {'ADMod_NAD_Mod': 0, 'ADMod_MarsParking': 1, 'ADMod_ANP': 2, 'ADMod_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class ADL3LatCtrlStsForBkp_UB:
        sig_name = "ADL3LatCtrlStsForBkp_UB"
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

    class ADL3LatCtrlStsForBkpCtrlSts:
        sig_name = "ADL3LatCtrlStsForBkpCtrlSts"
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
        sig_value_table = {'Primary': 0, 'Secondary': 1}
        compute_method = None
        length = 1
        startbit = 2
        byte = 0
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class ADL3LatCtrlStsForBkpCntr:
        sig_name = "ADL3LatCtrlStsForBkpCntr"
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

    class ADL3LatCtrlStsForBkpDegraded:
        sig_name = "ADL3LatCtrlStsForBkpDegraded"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 11
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LatDegrad_NoDegradation_Green': 0, 'LatDegrad_Red_fault1': 1, 'LatDegrad_Yellow_fault2': 2, 'LatDegrad_Yellow_fault3': 3, 'LatDegrad_Yellow_fault4': 4, 'LatDegrad_Yellow_fault5': 5, 'LatDegrad_Yellow_fault6': 6, 'LatDegrad_Yellow_fault7': 7, 'LatDegrad_Yellow_fault8': 8, 'LatDegrad_Yellow_fault9': 9, 'LatDegrad_Yellow_fault10': 10, 'LatDegrad_Reserved1': 11}
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4


class CdcADRedundancyFr01:
    msg_name = "CdcADRedundancyFr01"
    msg_id = 130
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "CDC"
    rx_nodes = ['ACU']
    sig_group_dict = {'AsySecChFltSts': ['AsySecChFltStsADStsLampFailr', 'AsySecChFltStsCameraFailr', 'AsySecChFltStsCentrDispFailr', 'AsySecChFltStsChks', 'AsySecChFltStsCntr', 'AsySecChFltStsDrvrTakeoverLampFailr', 'AsySecChFltStsFLRFailr', 'AsySecChFltStsLossComADETH', 'AsySecChFltStsPosngSysFailr', 'AsySecChFltStsReserved1', 'AsySecChFltStsReserved2', 'AsySecChFltStsReserved3', 'AsySecChFltStsReserved4', 'AsySecChFltStsReserved5', 'AsySecChFltStsReserved6', 'AsySecChFltStsSecCtrlFailr', 'AsySecChFltStsSecHWFailr', 'AsySecChFltStsTiSyncnFailr'], 'AsySecChSts': ['AsySecChStsADModActvnCfm', 'AsySecChStsADModDeactvnCfm', 'AsySecChStsAsySecADSts', 'AsySecChStsChks', 'AsySecChStsCntr', 'AsySecChStsReserved1', 'AsySecChStsReserved2', 'AsySecChStsSecCtrlrSts']}
    sig_group_dataid_dict = {'AsySecChFltSts': 3712, 'AsySecChSts': 3711}

    class AsySecChFltStsSecHWFailr:
        sig_name = "AsySecChFltStsSecHWFailr"
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
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 28
        byte = 3
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class AsySecChFltStsChks:
        sig_name = "AsySecChFltStsChks"
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

    class AsySecChStsAsySecADSts:
        sig_name = "AsySecChStsAsySecADSts"
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
        sig_value_table = {'AsySecADSts_Standby': 0, 'AsySecADSts_Active1': 1, 'AsySecADSts_Active2': 2, 'AsySecADSts_OtherStatus': 3}
        compute_method = None
        length = 2
        startbit = 55
        byte = 6
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class AsySecChStsADModActvnCfm:
        sig_name = "AsySecChStsADModActvnCfm"
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
        sig_value_table = {'Cfmd1_NotCfmd': 0, 'Cfmd1_Cfmd': 1}
        compute_method = None
        length = 1
        startbit = 43
        byte = 5
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class AsySecChStsADModDeactvnCfm:
        sig_name = "AsySecChStsADModDeactvnCfm"
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
        sig_value_table = {'Cfmd1_NotCfmd': 0, 'Cfmd1_Cfmd': 1}
        compute_method = None
        length = 1
        startbit = 42
        byte = 5
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class AsySecChFltStsCntr:
        sig_name = "AsySecChFltStsCntr"
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

    class AsySecChFltStsCameraFailr:
        sig_name = "AsySecChFltStsCameraFailr"
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
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 10
        byte = 1
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class AsySecChFltStsDrvrTakeoverLampFailr:
        sig_name = "AsySecChFltStsDrvrTakeoverLampFailr"
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
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 18
        byte = 2
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class AsySecChStsCntr:
        sig_name = "AsySecChStsCntr"
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

    class AsySecChFltStsCentrDispFailr:
        sig_name = "AsySecChFltStsCentrDispFailr"
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
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 19
        byte = 2
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class AsySecChFltStsPosngSysFailr:
        sig_name = "AsySecChFltStsPosngSysFailr"
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
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 30
        byte = 3
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class AsySecChFltStsLossComADETH:
        sig_name = "AsySecChFltStsLossComADETH"
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
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 31
        byte = 3
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class AsySecChFltStsReserved2:
        sig_name = "AsySecChFltStsReserved2"
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
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 8
        byte = 1
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class AsySecChStsChks:
        sig_name = "AsySecChStsChks"
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

    class AsySecChFltSts_UB:
        sig_name = "AsySecChFltSts_UB"
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

    class AsySecChFltStsReserved6:
        sig_name = "AsySecChFltStsReserved6"
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
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 20
        byte = 2
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class AsySecChFltStsReserved5:
        sig_name = "AsySecChFltStsReserved5"
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
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 21
        byte = 2
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class AsySecChFltStsTiSyncnFailr:
        sig_name = "AsySecChFltStsTiSyncnFailr"
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
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 27
        byte = 3
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class AsySecChFltStsReserved4:
        sig_name = "AsySecChFltStsReserved4"
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
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 22
        byte = 2
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class AsySecChStsReserved2:
        sig_name = "AsySecChStsReserved2"
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
        sig_value_table = {'ReqSts1_NotReqd': 0, 'ReqSts1_Reqd': 1}
        compute_method = None
        length = 1
        startbit = 40
        byte = 5
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class AsySecChStsReserved1:
        sig_name = "AsySecChStsReserved1"
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
        sig_value_table = {'ReqSts1_NotReqd': 0, 'ReqSts1_Reqd': 1}
        compute_method = None
        length = 1
        startbit = 41
        byte = 5
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class AsySecChStsSecCtrlrSts:
        sig_name = "AsySecChStsSecCtrlrSts"
        sig_start_bit = 53
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ADSecCtrlsts_Red': 0, 'ADSecCtrlsts_Yellow1': 1, 'ADSecCtrlsts_Yellow2': 2, 'ADSecCtrlsts_Green': 3, 'ADSecCtrlsts_Reserved1': 4, 'ADSecCtrlsts_Reserved2': 5, 'ADSecCtrlsts_Reserved3': 6, 'ADSecCtrlsts_Reserved4': 7}
        compute_method = None
        length = 3
        startbit = 53
        byte = 6
        mask = 0b00111000
        unmask = 0b11000111
        shift = 3

    class AsySecChFltStsSecCtrlFailr:
        sig_name = "AsySecChFltStsSecCtrlFailr"
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
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 29
        byte = 3
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class AsySecChSts_UB:
        sig_name = "AsySecChSts_UB"
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

    class AsySecChFltStsReserved3:
        sig_name = "AsySecChFltStsReserved3"
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
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 23
        byte = 2
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class AsySecChFltStsADStsLampFailr:
        sig_name = "AsySecChFltStsADStsLampFailr"
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
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 11
        byte = 1
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class AsySecChFltStsFLRFailr:
        sig_name = "AsySecChFltStsFLRFailr"
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
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 17
        byte = 2
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class AsySecChFltStsReserved1:
        sig_name = "AsySecChFltStsReserved1"
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
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 9
        byte = 1
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1


class AcuADRedundancyCANFr05:
    msg_name = "AcuADRedundancyCANFr05"
    msg_id = 129
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "ACU"
    rx_nodes = ['CDC']
    sig_group_dict = {'PrimAsyALgtPinionAgReq': ['PrimAsyALgtPinionAgReqChks', 'PrimAsyALgtPinionAgReqCntr', 'PrimAsyALgtPinionAgReqPrimAsyALgtReqRngForSafeMax', 'PrimAsyALgtPinionAgReqPrimAsyALgtReqRngForSafeMin', 'PrimAsyALgtPinionAgReqPrimAsyPinionAgReqSafe']}
    sig_group_dataid_dict = {'PrimAsyALgtPinionAgReq': 3716}

    class PrimAsyALgtPinionAgReqPrimAsyALgtReqRngForSafeMin:
        sig_name = "PrimAsyALgtPinionAgReqPrimAsyALgtReqRngForSafeMin"
        sig_start_bit = 27
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = -15.0
        sig_value_min = 0
        sig_value_max = 3000
        sig_byteorder = "Motorola"
        sig_value_init = 1500
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 27
        bmuws_info = [(3, 0b00001111, 0b11110000, 4, 0), (4, 0b11111111, 0b00000000, 8, 0)]

    class PrimAsyALgtPinionAgReq_UB:
        sig_name = "PrimAsyALgtPinionAgReq_UB"
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

    class PrimAsyALgtPinionAgReqPrimAsyALgtReqRngForSafeMax:
        sig_name = "PrimAsyALgtPinionAgReqPrimAsyALgtReqRngForSafeMax"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = -15.0
        sig_value_min = 0
        sig_value_max = 3000
        sig_byteorder = "Motorola"
        sig_value_init = 1500
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11110000, 0b00001111, 4, 4)]

    class PrimAsyALgtPinionAgReqCntr:
        sig_name = "PrimAsyALgtPinionAgReqCntr"
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

    class PrimAsyALgtPinionAgReqPrimAsyPinionAgReqSafe:
        sig_name = "PrimAsyALgtPinionAgReqPrimAsyPinionAgReqSafe"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 0.0009765625
        sig_value_offset = -14.5
        sig_value_min = 0
        sig_value_max = 32767
        sig_byteorder = "Motorola"
        sig_value_init = 14848
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111110, 0b00000001, 7, 1)]

    class PrimAsyALgtPinionAgReqChks:
        sig_name = "PrimAsyALgtPinionAgReqChks"
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


class FlcAdRedundancyFr03:
    msg_name = "FlcAdRedundancyFr03"
    msg_id = 295
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "CDC"
    rx_nodes = ['BBM']
    sig_group_dict = {'AsyALgtReqRngForSafeForBkp': ['AsyALgtReqRngForSafeForBkpChks', 'AsyALgtReqRngForSafeForBkpCntr', 'AsyALgtReqRngForSafeForBkpMax', 'AsyALgtReqRngForSafeForBkpMin']}
    sig_group_dataid_dict = {'AsyALgtReqRngForSafeForBkp': 3703}

    class AsyALgtReqRngForSafeForBkpChks:
        sig_name = "AsyALgtReqRngForSafeForBkpChks"
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

    class AsyALgtReqRngForSafeForBkpMin:
        sig_name = "AsyALgtReqRngForSafeForBkpMin"
        sig_start_bit = 27
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = -15.0
        sig_value_min = 0
        sig_value_max = 3000
        sig_byteorder = "Motorola"
        sig_value_init = 1500
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 27
        bmuws_info = [(3, 0b00001111, 0b11110000, 4, 0), (4, 0b11111111, 0b00000000, 8, 0)]

    class AsyALgtReqRngForSafeForBkp_UB:
        sig_name = "AsyALgtReqRngForSafeForBkp_UB"
        sig_start_bit = 47
        update_id_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class AsyALgtReqRngForSafeForBkpMax:
        sig_name = "AsyALgtReqRngForSafeForBkpMax"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = -15.0
        sig_value_min = 0
        sig_value_max = 3000
        sig_byteorder = "Motorola"
        sig_value_init = 1500
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11110000, 0b00001111, 4, 4)]

    class AsyALgtReqRngForSafeForBkpCntr:
        sig_name = "AsyALgtReqRngForSafeForBkpCntr"
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


class PscmToEtcAdRedXcpFr03:
    msg_name = "PscmToEtcAdRedXcpFr03"
    msg_id = 1419
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "PSCM2"
    rx_nodes = ['CCM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class AcuADRedundancyCANNmFr:
    msg_name = "AcuADRedundancyCANNmFr"
    msg_id = 1286
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "ACU"
    rx_nodes = ['PSCM2']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class BbmAdRedundancyFr07:
    msg_name = "BbmAdRedundancyFr07"
    msg_id = 260
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.04
    msg_length = 8
    tx_node = "BBM"
    rx_nodes = ['PSCM2']
    sig_group_dict = {'VehModMngtGlbSafe1': ['VehModMngtGlbSafe1CarModSts1', 'VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp', 'VehModMngtGlbSafe1Chks', 'VehModMngtGlbSafe1Cntr', 'VehModMngtGlbSafe1EgyLvlElecMai', 'VehModMngtGlbSafe1EgyLvlElecSubtyp', 'VehModMngtGlbSafe1FltEgyCnsWdSts', 'VehModMngtGlbSafe1PwrLvlElecMai', 'VehModMngtGlbSafe1PwrLvlElecSubtyp', 'VehModMngtGlbSafe1UsgModSts']}
    sig_group_dataid_dict = {'VehModMngtGlbSafe1': 116}

    class VehModMngtGlbSafe1_UB:
        sig_name = "VehModMngtGlbSafe1_UB"
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

    class VehModMngtGlbSafe1CarModSts1:
        sig_name = "VehModMngtGlbSafe1CarModSts1"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp:
        sig_name = "VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp"
        sig_start_bit = 60
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
        startbit = 60
        byte = 7
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class VehModMngtGlbSafe1EgyLvlElecMai:
        sig_name = "VehModMngtGlbSafe1EgyLvlElecMai"
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

    class VehModMngtGlbSafe1FltEgyCnsWdSts:
        sig_name = "VehModMngtGlbSafe1FltEgyCnsWdSts"
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
        sig_value_table = {'FltEgyCns1_NoFlt': 0, 'FltEgyCns1_Flt': 1}
        compute_method = None
        length = 1
        startbit = 57
        byte = 7
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VehModMngtGlbSafe1PwrLvlElecSubtyp:
        sig_name = "VehModMngtGlbSafe1PwrLvlElecSubtyp"
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

    class VehModMngtGlbSafe1PwrLvlElecMai:
        sig_name = "VehModMngtGlbSafe1PwrLvlElecMai"
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

    class VehModMngtGlbSafe1Cntr:
        sig_name = "VehModMngtGlbSafe1Cntr"
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

    class VehModMngtGlbSafe1Chks:
        sig_name = "VehModMngtGlbSafe1Chks"
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

    class VehModMngtGlbSafe1UsgModSts:
        sig_name = "VehModMngtGlbSafe1UsgModSts"
        sig_start_bit = 51
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
        startbit = 51
        byte = 6
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class VehModMngtGlbSafe1EgyLvlElecSubtyp:
        sig_name = "VehModMngtGlbSafe1EgyLvlElecSubtyp"
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


class BbmToAllADRedundancyCANDiagReqFrame:
    msg_name = "BbmToAllADRedundancyCANDiagReqFrame"
    msg_id = 2047
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BBM"
    rx_nodes = ['PSCM2']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class BbmAdRedundancyFr02:
    msg_name = "BbmAdRedundancyFr02"
    msg_id = 64
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "BBM"
    rx_nodes = ['CDC', 'PSCM2', 'ACU']
    sig_group_dict = {'IMU2ComStsa': ['IMU2ComStsaChks', 'IMU2ComStsaCntr', 'IMU2ComStsaHvSysPwrOff'], 'VehSpdLgtForBkp': ['VehSpdLgtForBkpVehSpdLgtA', 'VehSpdLgtForBkpVehSpdLgtChks', 'VehSpdLgtForBkpVehSpdLgtCntr', 'VehSpdLgtForBkpVehSpdLgtQf']}
    sig_group_dataid_dict = {'IMU2ComStsa': 3503, 'VehSpdLgtForBkp': 6503}

    class IMU2ComStsaHvSysPwrOff:
        sig_name = "IMU2ComStsaHvSysPwrOff"
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
        sig_value_table = {'OkNotOk1_Ok': 0, 'OkNotOk1_NotOk': 1}
        compute_method = None
        length = 1
        startbit = 43
        byte = 5
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VehSpdLgtForBkpVehSpdLgtChks:
        sig_name = "VehSpdLgtForBkpVehSpdLgtChks"
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

    class IMU2ComStsa_UB:
        sig_name = "IMU2ComStsa_UB"
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

    class VehSpdLgtForBkp_UB:
        sig_name = "VehSpdLgtForBkp_UB"
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

    class IMU2ComStsaChks:
        sig_name = "IMU2ComStsaChks"
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

    class VehSpdLgtForBkpVehSpdLgtQf:
        sig_name = "VehSpdLgtForBkpVehSpdLgtQf"
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
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VehSpdLgtForBkpVehSpdLgtA:
        sig_name = "VehSpdLgtForBkpVehSpdLgtA"
        sig_start_bit = 14
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
        startbit = 14
        bmuws_info = [(1, 0b01111111, 0b10000000, 7, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class IMU2ComStsaCntr:
        sig_name = "IMU2ComStsaCntr"
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

    class VehSpdLgtForBkpVehSpdLgtCntr:
        sig_name = "VehSpdLgtForBkpVehSpdLgtCntr"
        sig_start_bit = 5
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
        startbit = 5
        byte = 0
        mask = 0b00111100
        unmask = 0b11000011
        shift = 2


class BbmAdRedundancyFr16:
    msg_name = "BbmAdRedundancyFr16"
    msg_id = 89
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "BBM"
    rx_nodes = ['CDC', 'ACU']
    sig_group_dict = {'WhlVAgrReForBkp': ['WhlVAgrReForBkpWhlVAgrReLe', 'WhlVAgrReForBkpWhlVAgrReLeQf', 'WhlVAgrReForBkpWhlVAgrReRi', 'WhlVAgrReForBkpWhlVAgrReRiQf']}
    sig_group_dataid_dict = {}

    class WhlVAgrReForBkpWhlVAgrReLeQf:
        sig_name = "WhlVAgrReForBkpWhlVAgrReLeQf"
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
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 11
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class WhlVAgrReForBkp_UB:
        sig_name = "WhlVAgrReForBkp_UB"
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

    class WhlVAgrReForBkpWhlVAgrReRi:
        sig_name = "WhlVAgrReForBkpWhlVAgrReRi"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 0.0078125
        sig_value_offset = 0.0
        sig_value_min = -32640
        sig_value_max = 32640
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class WhlVAgrReForBkpWhlVAgrReRiQf:
        sig_name = "WhlVAgrReForBkpWhlVAgrReRiQf"
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
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 9
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class WhlVAgrReForBkpWhlVAgrReLe:
        sig_name = "WhlVAgrReForBkpWhlVAgrReLe"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 0.0078125
        sig_value_offset = 0.0
        sig_value_min = -32640
        sig_value_max = 32640
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0)]


class FlcAdRedundancyFr01:
    msg_name = "FlcAdRedundancyFr01"
    msg_id = 121
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "CDC"
    rx_nodes = ['PSCM2']
    sig_group_dict = {'AsyPinionAgReqForBkp': ['AsyPinionAgReqForBkpAsyPinionAgReq', 'AsyPinionAgReqForBkpChks', 'AsyPinionAgReqForBkpCntr']}
    sig_group_dataid_dict = {'AsyPinionAgReqForBkp': 3702}

    class AsyPinionAgReqForBkpChks:
        sig_name = "AsyPinionAgReqForBkpChks"
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

    class AsyPinionAgReqForBkp_UB:
        sig_name = "AsyPinionAgReqForBkp_UB"
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

    class AsyPinionAgReqForBkpCntr:
        sig_name = "AsyPinionAgReqForBkpCntr"
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

    class AsyPinionAgReqForBkpAsyPinionAgReq:
        sig_name = "AsyPinionAgReqForBkpAsyPinionAgReq"
        sig_start_bit = 6
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 0.0009765625
        sig_value_offset = -14.5
        sig_value_min = 0
        sig_value_max = 32767
        sig_byteorder = "Motorola"
        sig_value_init = 14848
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 6
        bmuws_info = [(0, 0b01111111, 0b10000000, 7, 0), (1, 0b11111111, 0b00000000, 8, 0)]


class BbmADRedundancyCANNmFr:
    msg_name = "BbmADRedundancyCANNmFr"
    msg_id = 1284
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BBM"
    rx_nodes = ['CDC']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class AcuADRedundancyCANFr04:
    msg_name = "AcuADRedundancyCANFr04"
    msg_id = 100
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "ACU"
    rx_nodes = ['CDC']
    sig_group_dict = {'AsyPrimChFltSts': ['AsyPrimChFltStsCameraFailr', 'AsyPrimChFltStsChks', 'AsyPrimChFltStsCntr', 'AsyPrimChFltStsFLRFailr', 'AsyPrimChFltStsHDMapFailr', 'AsyPrimChFltStsLidarFailr', 'AsyPrimChFltStsPosngSysFailr', 'AsyPrimChFltStsPrimCtrlFailr', 'AsyPrimChFltStsPrimHwFailr', 'AsyPrimChFltStsReserved1', 'AsyPrimChFltStsReserved2', 'AsyPrimChFltStsReserved3', 'AsyPrimChFltStsReserved4', 'AsyPrimChFltStsSurRoundRdrFailr', 'AsyPrimChFltStsTiSyncnFailr', 'AsyPrimChFltStsUSSFailr'], 'AsyPrimChSts': ['AsyPrimChStsADModActvn', 'AsyPrimChStsADModActvnCfm', 'AsyPrimChStsADModDeactvn', 'AsyPrimChStsADModDeactvnCfm', 'AsyPrimChStsADMode2', 'AsyPrimChStsAsyPrimADSts', 'AsyPrimChStsChks', 'AsyPrimChStsCntr', 'AsyPrimChStsPrimChCtrlrSts', 'AsyPrimChStsReserved1']}
    sig_group_dataid_dict = {'AsyPrimChFltSts': 3714, 'AsyPrimChSts': 3713}

    class AsyPrimChStsPrimChCtrlrSts:
        sig_name = "AsyPrimChStsPrimChCtrlrSts"
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
        sig_value_table = {'ColorSts_Red': 0, 'ColorSts_Yellow': 1, 'ColorSts_Green': 2, 'ColorSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 47
        byte = 5
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class AsyPrimChFltStsReserved1:
        sig_name = "AsyPrimChFltStsReserved1"
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
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 22
        byte = 2
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class AsyPrimChFltStsChks:
        sig_name = "AsyPrimChFltStsChks"
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

    class AsyPrimChStsADModActvnCfm:
        sig_name = "AsyPrimChStsADModActvnCfm"
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
        sig_value_table = {'Cfmd1_NotCfmd': 0, 'Cfmd1_Cfmd': 1}
        compute_method = None
        length = 1
        startbit = 44
        byte = 5
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class AsyPrimChFltStsPrimHwFailr:
        sig_name = "AsyPrimChFltStsPrimHwFailr"
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
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 23
        byte = 2
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class AsyPrimChFltStsPrimCtrlFailr:
        sig_name = "AsyPrimChFltStsPrimCtrlFailr"
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
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 17
        byte = 2
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class AsyPrimChStsChks:
        sig_name = "AsyPrimChStsChks"
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

    class AsyPrimChStsADMode2:
        sig_name = "AsyPrimChStsADMode2"
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
        sig_value_table = {'ADMod_NAD_Mod': 0, 'ADMod_MarsParking': 1, 'ADMod_ANP': 2, 'ADMod_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 53
        byte = 6
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class AsyPrimChFltStsSurRoundRdrFailr:
        sig_name = "AsyPrimChFltStsSurRoundRdrFailr"
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
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 31
        byte = 3
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class AsyPrimChFltSts_UB:
        sig_name = "AsyPrimChFltSts_UB"
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

    class AsyPrimChFltStsCntr:
        sig_name = "AsyPrimChFltStsCntr"
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

    class AsyPrimChFltStsTiSyncnFailr:
        sig_name = "AsyPrimChFltStsTiSyncnFailr"
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
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 16
        byte = 2
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class AsyPrimChFltStsReserved4:
        sig_name = "AsyPrimChFltStsReserved4"
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
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 19
        byte = 2
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class AsyPrimChFltStsFLRFailr:
        sig_name = "AsyPrimChFltStsFLRFailr"
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
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 13
        byte = 1
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class AsyPrimChStsADModDeactvn:
        sig_name = "AsyPrimChStsADModDeactvn"
        sig_start_bit = 55
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ReqSts1_NotReqd': 0, 'ReqSts1_Reqd': 1}
        compute_method = None
        length = 1
        startbit = 55
        byte = 6
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class AsyPrimChStsADModActvn:
        sig_name = "AsyPrimChStsADModActvn"
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
        sig_value_table = {'ReqSts1_NotReqd': 0, 'ReqSts1_Reqd': 1}
        compute_method = None
        length = 1
        startbit = 45
        byte = 5
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class AsyPrimChFltStsReserved2:
        sig_name = "AsyPrimChFltStsReserved2"
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
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 21
        byte = 2
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class AsyPrimChFltStsReserved3:
        sig_name = "AsyPrimChFltStsReserved3"
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
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 20
        byte = 2
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class AsyPrimChFltStsUSSFailr:
        sig_name = "AsyPrimChFltStsUSSFailr"
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
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 30
        byte = 3
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class AsyPrimChStsADModDeactvnCfm:
        sig_name = "AsyPrimChStsADModDeactvnCfm"
        sig_start_bit = 54
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Cfmd1_NotCfmd': 0, 'Cfmd1_Cfmd': 1}
        compute_method = None
        length = 1
        startbit = 54
        byte = 6
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class AsyPrimChStsAsyPrimADSts:
        sig_name = "AsyPrimChStsAsyPrimADSts"
        sig_start_bit = 50
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AsyPrimADSts_Passive': 0, 'AsyPrimADSts_Standby': 1, 'AsyPrimADSts_Active': 2, 'AsyPrimADSts_OtherStatus': 3}
        compute_method = None
        length = 2
        startbit = 50
        byte = 6
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class AsyPrimChFltStsLidarFailr:
        sig_name = "AsyPrimChFltStsLidarFailr"
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
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 18
        byte = 2
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class AsyPrimChStsCntr:
        sig_name = "AsyPrimChStsCntr"
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

    class AsyPrimChFltStsHDMapFailr:
        sig_name = "AsyPrimChFltStsHDMapFailr"
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
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 15
        byte = 1
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class AsyPrimChStsReserved1:
        sig_name = "AsyPrimChStsReserved1"
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
        sig_value_table = {'ReqSts1_NotReqd': 0, 'ReqSts1_Reqd': 1}
        compute_method = None
        length = 1
        startbit = 51
        byte = 6
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class AsyPrimChFltStsCameraFailr:
        sig_name = "AsyPrimChFltStsCameraFailr"
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
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 14
        byte = 1
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class AsyPrimChSts_UB:
        sig_name = "AsyPrimChSts_UB"
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

    class AsyPrimChFltStsPosngSysFailr:
        sig_name = "AsyPrimChFltStsPosngSysFailr"
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
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 12
        byte = 1
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4


class CdcADRedundancyCANNmFr:
    msg_name = "CdcADRedundancyCANNmFr"
    msg_id = 1297
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CDC"
    rx_nodes = ['ACU']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class ImuAdRedundancyFr01:
    msg_name = "ImuAdRedundancyFr01"
    msg_id = 336
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "IMU"
    rx_nodes = ['CDC', 'BBM']
    sig_group_dict = {'JBkpSig1Orig': ['JBkpSig1OrigAY', 'JBkpSig1OrigAYSts', 'JBkpSig1OrigChks', 'JBkpSig1OrigCLUSts', 'JBkpSig1OrigCntr', 'JBkpSig1OrigResd1', 'JBkpSig1OrigYawRate', 'JBkpSig1OrigYawRateSts']}
    sig_group_dataid_dict = {}

    class JBkpSig1OrigResd1:
        sig_name = "JBkpSig1OrigResd1"
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

    class JBkpSig1OrigCLUSts:
        sig_name = "JBkpSig1OrigCLUSts"
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

    class JBkpSig1OrigAYSts:
        sig_name = "JBkpSig1OrigAYSts"
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

    class JBkpSig1OrigYawRateSts:
        sig_name = "JBkpSig1OrigYawRateSts"
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

    class JBkpSig1OrigCntr:
        sig_name = "JBkpSig1OrigCntr"
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

    class JBkpSig1OrigYawRate:
        sig_name = "JBkpSig1OrigYawRate"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 0.005
        sig_value_offset = -163.84
        sig_value_min = 0
        sig_value_max = 65534
        sig_byteorder = "Motorola"
        sig_value_init = 32768
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class JBkpSig1OrigChks:
        sig_name = "JBkpSig1OrigChks"
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

    class JBkpSig1OrigAY:
        sig_name = "JBkpSig1OrigAY"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 0.000127462
        sig_value_offset = -4.1768
        sig_value_min = 0
        sig_value_max = 65534
        sig_byteorder = "Motorola"
        sig_value_init = 32769
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0)]


class EtcToPscmAdRedXcpFr03:
    msg_name = "EtcToPscmAdRedXcpFr03"
    msg_id = 1418
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CCM"
    rx_nodes = ['PSCM2']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class BbmAdRedundancyFr03:
    msg_name = "BbmAdRedundancyFr03"
    msg_id = 72
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "BBM"
    rx_nodes = ['CDC', 'ACU']
    sig_group_dict = {'WhlSpdCircumlReForBkp': ['WhlSpdCircumlReForBkpWhlSpdCircumlReChks', 'WhlSpdCircumlReForBkpWhlSpdCircumlReCntr', 'WhlSpdCircumlReForBkpWhlSpdCircumlReLe', 'WhlSpdCircumlReForBkpWhlSpdCircumlReLeQf', 'WhlSpdCircumlReForBkpWhlSpdCircumlReRi', 'WhlSpdCircumlReForBkpWhlSpdCircumlReRiQf']}
    sig_group_dataid_dict = {'WhlSpdCircumlReForBkp': 6505}

    class WhlSpdCircumlReForBkpWhlSpdCircumlReLe:
        sig_name = "WhlSpdCircumlReForBkpWhlSpdCircumlReLe"
        sig_start_bit = 39
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
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111110, 0b00000001, 7, 1)]

    class WhlSpdCircumlReForBkpWhlSpdCircumlReLeQf:
        sig_name = "WhlSpdCircumlReForBkpWhlSpdCircumlReLeQf"
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

    class WhlSpdCircumlReForBkpWhlSpdCircumlReCntr:
        sig_name = "WhlSpdCircumlReForBkpWhlSpdCircumlReCntr"
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

    class WhlSpdCircumlReForBkpWhlSpdCircumlReChks:
        sig_name = "WhlSpdCircumlReForBkpWhlSpdCircumlReChks"
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

    class WhlSpdCircumlReForBkpWhlSpdCircumlReRiQf:
        sig_name = "WhlSpdCircumlReForBkpWhlSpdCircumlReRiQf"
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
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 25
        byte = 3
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class WhlSpdCircumlReForBkpWhlSpdCircumlReRi:
        sig_name = "WhlSpdCircumlReForBkpWhlSpdCircumlReRi"
        sig_start_bit = 55
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
        startbit = 55
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111110, 0b00000001, 7, 1)]

    class WhlSpdCircumlReForBkp_UB:
        sig_name = "WhlSpdCircumlReForBkp_UB"
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


class BbmAdRedundancyFr13:
    msg_name = "BbmAdRedundancyFr13"
    msg_id = 87
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "BBM"
    rx_nodes = ['CDC', 'PSCM2', 'ACU']
    sig_group_dict = {'VehMtnStForBkp': ['VehMtnStForBkpVehMtnSt', 'VehMtnStForBkpVehMtnStChks', 'VehMtnStForBkpVehMtnStCntr']}
    sig_group_dataid_dict = {'VehMtnStForBkp': 6509}

    class VehMtnStForBkpVehMtnStChks:
        sig_name = "VehMtnStForBkpVehMtnStChks"
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

    class VehMtnStForBkpVehMtnStCntr:
        sig_name = "VehMtnStForBkpVehMtnStCntr"
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

    class VehMtnStForBkp_UB:
        sig_name = "VehMtnStForBkp_UB"
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

    class VehMtnStForBkpVehMtnSt:
        sig_name = "VehMtnStForBkpVehMtnSt"
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
        sig_value_table = {'VehMtnSt2_Ukwn': 0, 'VehMtnSt2_StandStillVal1': 1, 'VehMtnSt2_StandStillVal2': 2, 'VehMtnSt2_StandStillVal3': 3, 'VehMtnSt2_RollgFwdVal1': 4, 'VehMtnSt2_RollgFwdVal2': 5, 'VehMtnSt2_RollgBackwVal1': 6, 'VehMtnSt2_RollgBackwVal2': 7}
        compute_method = None
        length = 3
        startbit = 59
        byte = 7
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1


class Pscm2ToBbmADRedundancyCANDiagReqFrame:
    msg_name = "Pscm2ToBbmADRedundancyCANDiagReqFrame"
    msg_id = 1568
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "PSCM2"
    rx_nodes = ['BBM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class PscmAdRedundancyFr01:
    msg_name = "PscmAdRedundancyFr01"
    msg_id = 133
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "PSCM2"
    rx_nodes = ['CDC', 'ACU']
    sig_group_dict = {'PinionSteerAgGroupForBkp': ['PinionSteerAgGroupForBkpChks', 'PinionSteerAgGroupForBkpCntr', 'PinionSteerAgGroupForBkpPinionSteerAgForBkp', 'PinionSteerAgGroupForBkpPinionSteerAgQfForBkp', 'PinionSteerAgGroupForBkpPinionSteerAgSpdForBkp', 'PinionSteerAgGroupForBkpPinionSteerAgSpdQfForBkp', 'PinionSteerAgGroupForBkpSteerWhlTqForBkp', 'PinionSteerAgGroupForBkpSteerWhlTqQfForBkp']}
    sig_group_dataid_dict = {'PinionSteerAgGroupForBkp': 1031}

    class PinionSteerAgGroupForBkpSteerWhlTqForBkp:
        sig_name = "PinionSteerAgGroupForBkpSteerWhlTqForBkp"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 14
        sig_value_factor = 0.00390625
        sig_value_offset = 0.0
        sig_value_min = -7680
        sig_value_max = 7680
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 14
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111100, 0b00000011, 6, 2)]

    class PinionSteerAgGroupForBkpChks:
        sig_name = "PinionSteerAgGroupForBkpChks"
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

    class PinionSteerAgGroupForBkpCntr:
        sig_name = "PinionSteerAgGroupForBkpCntr"
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

    class PinionSteerAgGroupForBkpSteerWhlTqQfForBkp:
        sig_name = "PinionSteerAgGroupForBkpSteerWhlTqQfForBkp"
        sig_start_bit = 25
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
        startbit = 25
        byte = 3
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class PinionSteerAgGroupForBkp_UB:
        sig_name = "PinionSteerAgGroupForBkp_UB"
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

    class PinionSteerAgGroupForBkpPinionSteerAgForBkp:
        sig_name = "PinionSteerAgGroupForBkpPinionSteerAgForBkp"
        sig_start_bit = 55
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 0.0009765625
        sig_value_offset = 0.0
        sig_value_min = -14848
        sig_value_max = 14848
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 55
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111110, 0b00000001, 7, 1)]

    class PinionSteerAgGroupForBkpPinionSteerAgSpdForBkp:
        sig_name = "PinionSteerAgGroupForBkpPinionSteerAgSpdForBkp"
        sig_start_bit = 39
        update_id_bit = None
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
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111100, 0b00000011, 6, 2)]

    class PinionSteerAgGroupForBkpPinionSteerAgSpdQfForBkp:
        sig_name = "PinionSteerAgGroupForBkpPinionSteerAgSpdQfForBkp"
        sig_start_bit = 9
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
        startbit = 9
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class PinionSteerAgGroupForBkpPinionSteerAgQfForBkp:
        sig_name = "PinionSteerAgGroupForBkpPinionSteerAgQfForBkp"
        sig_start_bit = 11
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
        startbit = 11
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2


class BbmToPscm2ADRedundancyCANDiagReqFrame:
    msg_name = "BbmToPscm2ADRedundancyCANDiagReqFrame"
    msg_id = 1824
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BBM"
    rx_nodes = ['PSCM2']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class CdcADRedundancyFr02:
    msg_name = "CdcADRedundancyFr02"
    msg_id = 304
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.06
    msg_length = 8
    tx_node = "CDC"
    rx_nodes = ['ACU']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class MmedHdPwrMod:
        sig_name = "MmedHdPwrMod"
        sig_start_bit = 7
        update_id_bit = 0
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'MmedMaiPwrMod_OnlyMCURunning': 0, 'MmedMaiPwrMod_STR': 1, 'MmedMaiPwrMod_SystemInit': 2, 'MmedMaiPwrMod_HMIOFF': 3, 'MmedMaiPwrMod_RunMode': 4, 'MmedMaiPwrMod_RemoteMode': 5, 'MmedMaiPwrMod_ReadyToSTR': 6, 'MmedMaiPwrMod_ReadyToSleep': 7}
        compute_method = None
        length = 3
        startbit = 7
        byte = 0
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5


class BbmAdRedundancyFr04:
    msg_name = "BbmAdRedundancyFr04"
    msg_id = 82
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "BBM"
    rx_nodes = ['CDC', 'ACU']
    sig_group_dict = {'WhlSpdCircumlFrntForBkp': ['WhlSpdCircumlFrntForBkpWhlSpdCircumlFrntChks', 'WhlSpdCircumlFrntForBkpWhlSpdCircumlFrntCntr', 'WhlSpdCircumlFrntForBkpWhlSpdCircumlFrntLe', 'WhlSpdCircumlFrntForBkpWhlSpdCircumlFrntLeQf', 'WhlSpdCircumlFrntForBkpWhlSpdCircumlFrntRiQf', 'WhlSpdCircumlFrntForBkpWhlSpdCircumlFrntWhlSpdCircumlFrntRi']}
    sig_group_dataid_dict = {'WhlSpdCircumlFrntForBkp': 6504}

    class WhlSpdCircumlFrntForBkpWhlSpdCircumlFrntCntr:
        sig_name = "WhlSpdCircumlFrntForBkpWhlSpdCircumlFrntCntr"
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

    class WhlSpdCircumlFrntForBkpWhlSpdCircumlFrntRiQf:
        sig_name = "WhlSpdCircumlFrntForBkpWhlSpdCircumlFrntRiQf"
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
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 25
        byte = 3
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class WhlSpdCircumlFrntForBkpWhlSpdCircumlFrntLe:
        sig_name = "WhlSpdCircumlFrntForBkpWhlSpdCircumlFrntLe"
        sig_start_bit = 39
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
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111110, 0b00000001, 7, 1)]

    class WhlSpdCircumlFrntForBkpWhlSpdCircumlFrntWhlSpdCircumlFrntRi:
        sig_name = "WhlSpdCircumlFrntForBkpWhlSpdCircumlFrntWhlSpdCircumlFrntRi"
        sig_start_bit = 55
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
        startbit = 55
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111110, 0b00000001, 7, 1)]

    class WhlSpdCircumlFrntForBkp_UB:
        sig_name = "WhlSpdCircumlFrntForBkp_UB"
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

    class WhlSpdCircumlFrntForBkpWhlSpdCircumlFrntLeQf:
        sig_name = "WhlSpdCircumlFrntForBkpWhlSpdCircumlFrntLeQf"
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

    class WhlSpdCircumlFrntForBkpWhlSpdCircumlFrntChks:
        sig_name = "WhlSpdCircumlFrntForBkpWhlSpdCircumlFrntChks"
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


class BbmAdRedundancyFr01:
    msg_name = "BbmAdRedundancyFr01"
    msg_id = 69
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "BBM"
    rx_nodes = ['CDC', 'ACU']
    sig_group_dict = {'ADL3LgtCtrlStsForBkp': ['ADL3LgtCtrlStsForBkpADMode', 'ADL3LgtCtrlStsForBkpChks', 'ADL3LgtCtrlStsForBkpCntr', 'ADL3LgtCtrlStsForBkpCtrlStatus', 'ADL3LgtCtrlStsForBkpDegraded', 'ADL3LgtCtrlStsForBkpQf', 'ADL3LgtCtrlStsForBkpSts'], 'WhlDirRotlFrntForBkp': ['WhlDirRotlFrntForBkpChks', 'WhlDirRotlFrntForBkpCntr', 'WhlDirRotlFrntForBkpLe', 'WhlDirRotlFrntForBkpRi']}
    sig_group_dataid_dict = {'ADL3LgtCtrlStsForBkp': 6580, 'WhlDirRotlFrntForBkp': 6506}

    class ADL3LgtCtrlStsForBkpDegraded:
        sig_name = "ADL3LgtCtrlStsForBkpDegraded"
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
        sig_value_table = {'LgtDegrad1_NoDegradation_Green': 0, 'LgtDegrad1_LgtFailr_Red': 1, 'LgtDegrad1_AbsEscTemporarilyOff_Yellow': 2, 'LgtDegrad1_EscServiceRequired_Yellow': 3, 'LgtDegrad1_EscTemporarilyOff_Yellow': 4, 'LgtDegrad1_StcTemporarilyOff_Yellow': 5, 'LgtDegrad1_EpbFailr_Yellow': 6, 'LgtDegrad1_VdswNOK_Yellow': 7, 'LgtDegrad1_PropADModCtrlInhbn_Yellow': 8, 'LgtDegrad1_PropTrqLimitation_Yellow': 9, 'LgtDegrad1_PropTotallyFault_Yellow': 10, 'LgtDegrad1_GeneralBrakeFailure_Yellow': 11, 'LgtDegrad1_Reserved4': 12, 'LgtDegrad1_Reserved5': 13, 'LgtDegrad1_Reserved6': 14, 'LgtDegrad1_Reserved7': 15}
        compute_method = None
        length = 4
        startbit = 27
        byte = 3
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class ADL3LgtCtrlStsForBkpChks:
        sig_name = "ADL3LgtCtrlStsForBkpChks"
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

    class ADL3LgtCtrlStsForBkpADMode:
        sig_name = "ADL3LgtCtrlStsForBkpADMode"
        sig_start_bit = 34
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ADMod_NAD_Mod': 0, 'ADMod_MarsParking': 1, 'ADMod_ANP': 2, 'ADMod_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 34
        byte = 4
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class WhlDirRotlFrntForBkpLe:
        sig_name = "WhlDirRotlFrntForBkpLe"
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
        sig_value_table = {'WhlRotlDirStd1_Undefd': 0, 'WhlRotlDirStd1_StandStill': 1, 'WhlRotlDirStd1_Fwd': 2, 'WhlRotlDirStd1_Backw': 3}
        compute_method = None
        length = 2
        startbit = 59
        byte = 7
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class WhlDirRotlFrntForBkpRi:
        sig_name = "WhlDirRotlFrntForBkpRi"
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
        sig_value_table = {'WhlRotlDirStd1_Undefd': 0, 'WhlRotlDirStd1_StandStill': 1, 'WhlRotlDirStd1_Fwd': 2, 'WhlRotlDirStd1_Backw': 3}
        compute_method = None
        length = 2
        startbit = 57
        byte = 7
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class ADL3LgtCtrlStsForBkp_UB:
        sig_name = "ADL3LgtCtrlStsForBkp_UB"
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

    class ADL3LgtCtrlStsForBkpCntr:
        sig_name = "ADL3LgtCtrlStsForBkpCntr"
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

    class ADL3LgtCtrlStsForBkpSts:
        sig_name = "ADL3LgtCtrlStsForBkpSts"
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
        sig_value_table = {'ColorSts_Red': 0, 'ColorSts_Yellow': 1, 'ColorSts_Green': 2, 'ColorSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 37
        byte = 4
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class WhlDirRotlFrntForBkp_UB:
        sig_name = "WhlDirRotlFrntForBkp_UB"
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

    class WhlDirRotlFrntForBkpCntr:
        sig_name = "WhlDirRotlFrntForBkpCntr"
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

    class WhlDirRotlFrntForBkpChks:
        sig_name = "WhlDirRotlFrntForBkpChks"
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

    class DrvBrkReqDmat:
        sig_name = "DrvBrkReqDmat"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 45
        byte = 5
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class ADL3LgtCtrlStsForBkpCtrlStatus:
        sig_name = "ADL3LgtCtrlStsForBkpCtrlStatus"
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
        sig_value_table = {'Primary': 0, 'Secondary': 1}
        compute_method = None
        length = 1
        startbit = 35
        byte = 4
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class ADL3LgtCtrlStsForBkpQf:
        sig_name = "ADL3LgtCtrlStsForBkpQf"
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
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 39
        byte = 4
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class BbmAdRedundancyFr19:
    msg_name = "BbmAdRedundancyFr19"
    msg_id = 90
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "BBM"
    rx_nodes = ['CDC', 'PSCM2', 'ACU']
    sig_group_dict = {'JBkpSig1a': ['JBkpSig1aAY', 'JBkpSig1aAYSts', 'JBkpSig1aChks', 'JBkpSig1aCLUSts', 'JBkpSig1aCntr', 'JBkpSig1aResd1', 'JBkpSig1aYawRate', 'JBkpSig1aYawRateSts']}
    sig_group_dataid_dict = {'JBkpSig1a': 3501}

    class JBkpSig1aCntr:
        sig_name = "JBkpSig1aCntr"
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

    class JBkpSig1aYawRate:
        sig_name = "JBkpSig1aYawRate"
        sig_start_bit = 55
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 0.005
        sig_value_offset = -163.84
        sig_value_min = 0
        sig_value_max = 65534
        sig_byteorder = "Motorola"
        sig_value_init = 32768
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 55
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class JBkpSig1aAYSts:
        sig_name = "JBkpSig1aAYSts"
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

    class JBkpSig1aAY:
        sig_name = "JBkpSig1aAY"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 0.000127462
        sig_value_offset = -4.1768
        sig_value_min = 0
        sig_value_max = 65534
        sig_byteorder = "Motorola"
        sig_value_init = 32769
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class JBkpSig1aYawRateSts:
        sig_name = "JBkpSig1aYawRateSts"
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

    class JBkpSig1aCLUSts:
        sig_name = "JBkpSig1aCLUSts"
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

    class JBkpSig1aChks:
        sig_name = "JBkpSig1aChks"
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

    class JBkpSig1aResd1:
        sig_name = "JBkpSig1aResd1"
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


class BbmAdRedundancyFr15:
    msg_name = "BbmAdRedundancyFr15"
    msg_id = 88
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "BBM"
    rx_nodes = ['CDC', 'ACU']
    sig_group_dict = {'BrkPedlTrvl': ['BrkPedlTrvlAct', 'BrkPedlTrvlChks', 'BrkPedlTrvlCntr', 'BrkPedlTrvlQf', 'BrkPedlTrvlSt', 'BrkPedlTrvlStQf', 'BrkPedlTrvlTar']}
    sig_group_dataid_dict = {'BrkPedlTrvl': 179}

    class BrkPedlTrvlQf:
        sig_name = "BrkPedlTrvlQf"
        sig_start_bit = 11
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
        startbit = 11
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class BrkPedlTrvlCntr:
        sig_name = "BrkPedlTrvlCntr"
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

    class BrkPedlTrvlTar:
        sig_name = "BrkPedlTrvlTar"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 0.01
        sig_value_offset = -5.0
        sig_value_min = 0
        sig_value_max = 5200
        sig_byteorder = "Motorola"
        sig_value_init = 500
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111000, 0b00000111, 5, 3)]

    class BrkPedlTrvl_UB:
        sig_name = "BrkPedlTrvl_UB"
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

    class BrkPedlTrvlSt:
        sig_name = "BrkPedlTrvlSt"
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
        sig_value_table = {'PsdNotPsd_NotPsd': 0, 'PsdNotPsd_Psd': 1}
        compute_method = None
        length = 1
        startbit = 26
        byte = 3
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class BrkPedlTrvlAct:
        sig_name = "BrkPedlTrvlAct"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 0.01
        sig_value_offset = -5.0
        sig_value_min = 0
        sig_value_max = 5200
        sig_byteorder = "Motorola"
        sig_value_init = 500
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111000, 0b00000111, 5, 3)]

    class BrkPedlTrvlChks:
        sig_name = "BrkPedlTrvlChks"
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

    class BrkPedlTrvlStQf:
        sig_name = "BrkPedlTrvlStQf"
        sig_start_bit = 9
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
        startbit = 9
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0


class BbmAdRedundancyFr20:
    msg_name = "BbmAdRedundancyFr20"
    msg_id = 97
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "BBM"
    rx_nodes = ['CDC', 'ACU']
    sig_group_dict = {'JBkpSig2a': ['JBkpSig2aAX', 'JBkpSig2aAXSts', 'JBkpSig2aChks', 'JBkpSig2aCLUDiag', 'JBkpSig2aCLUSts5', 'JBkpSig2aCntr', 'JBkpSig2aResd1', 'JBkpSig2aResd2', 'JBkpSig2aResd3']}
    sig_group_dataid_dict = {'JBkpSig2a': 3502}

    class JBkpSig2aCLUDiag:
        sig_name = "JBkpSig2aCLUDiag"
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

    class JBkpSig2aCntr:
        sig_name = "JBkpSig2aCntr"
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

    class JBkpSig2aAXSts:
        sig_name = "JBkpSig2aAXSts"
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

    class JBkpSig2aResd1:
        sig_name = "JBkpSig2aResd1"
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

    class JBkpSig2aResd3:
        sig_name = "JBkpSig2aResd3"
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

    class JBkpSig2aAX:
        sig_name = "JBkpSig2aAX"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 0.000127462
        sig_value_offset = -4.1768
        sig_value_min = 0
        sig_value_max = 65534
        sig_byteorder = "Motorola"
        sig_value_init = 32769
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class JBkpSig2aCLUSts5:
        sig_name = "JBkpSig2aCLUSts5"
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

    class JBkpSig2aChks:
        sig_name = "JBkpSig2aChks"
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

    class JBkpSig2aResd2:
        sig_name = "JBkpSig2aResd2"
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


class BbmtoEtcXcpFr01:
    msg_name = "BbmtoEtcXcpFr01"
    msg_id = 1365
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BBM"
    rx_nodes = ['CCM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class ImuAdRedundancyFr02:
    msg_name = "ImuAdRedundancyFr02"
    msg_id = 337
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "IMU"
    rx_nodes = ['CDC', 'BBM']
    sig_group_dict = {'JBkpSig2Orig': ['JBkpSig2OrigAX', 'JBkpSig2OrigAXSts', 'JBkpSig2OrigChks', 'JBkpSig2OrigCLUDiag', 'JBkpSig2OrigCLUSts5', 'JBkpSig2OrigCntr', 'JBkpSig2OrigResd1', 'JBkpSig2OrigResd2', 'JBkpSig2OrigResd3']}
    sig_group_dataid_dict = {}

    class JBkpSig2OrigResd1:
        sig_name = "JBkpSig2OrigResd1"
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

    class JBkpSig2OrigAX:
        sig_name = "JBkpSig2OrigAX"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 0.000127462
        sig_value_offset = -4.1768
        sig_value_min = 0
        sig_value_max = 65534
        sig_byteorder = "Motorola"
        sig_value_init = 32769
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class JBkpSig2OrigCLUDiag:
        sig_name = "JBkpSig2OrigCLUDiag"
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

    class JBkpSig2OrigCntr:
        sig_name = "JBkpSig2OrigCntr"
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

    class JBkpSig2OrigCLUSts5:
        sig_name = "JBkpSig2OrigCLUSts5"
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

    class JBkpSig2OrigAXSts:
        sig_name = "JBkpSig2OrigAXSts"
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

    class JBkpSig2OrigResd3:
        sig_name = "JBkpSig2OrigResd3"
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

    class JBkpSig2OrigChks:
        sig_name = "JBkpSig2OrigChks"
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

    class JBkpSig2OrigResd2:
        sig_name = "JBkpSig2OrigResd2"
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


class FlcAdRedundancyFr08:
    msg_name = "FlcAdRedundancyFr08"
    msg_id = 65
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "CDC"
    rx_nodes = ['PSCM2', 'BBM']
    sig_group_dict = {'AsyADModeReqForBkp': ['AsyADModeReqForBkpADActiveReq', 'AsyADModeReqForBkpADDeactiveReq', 'AsyADModeReqForBkpChks', 'AsyADModeReqForBkpCntr'], 'AsyADL3FuncCtrlStsForBkp': ['AsyADL3FuncCtrlStsForBkpADMod', 'AsyADL3FuncCtrlStsForBkpCtrlSts', 'AsyADL3FuncCtrlStsForBkpDegraded', 'AsyADL3FuncCtrlStsForBkpQf', 'AsyADL3FuncCtrlStsForBkpSts']}
    sig_group_dataid_dict = {'AsyADModeReqForBkp': 3729}

    class AsyADL3FuncCtrlStsForBkpSts:
        sig_name = "AsyADL3FuncCtrlStsForBkpSts"
        sig_start_bit = 14
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ColorSts_Red': 0, 'ColorSts_Yellow': 1, 'ColorSts_Green': 2, 'ColorSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 14
        byte = 1
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class AsyADModeReqForBkpADDeactiveReq:
        sig_name = "AsyADModeReqForBkpADDeactiveReq"
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
        sig_value_table = {'ReqSts1_NotReqd': 0, 'ReqSts1_Reqd': 1}
        compute_method = None
        length = 1
        startbit = 10
        byte = 1
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class AsyADModeReqForBkpCntr:
        sig_name = "AsyADModeReqForBkpCntr"
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

    class AsyADL3FuncCtrlStsForBkpDegraded:
        sig_name = "AsyADL3FuncCtrlStsForBkpDegraded"
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

    class AsyADModeReqForBkpChks:
        sig_name = "AsyADModeReqForBkpChks"
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

    class AsyADModeReqForBkp_UB:
        sig_name = "AsyADModeReqForBkp_UB"
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

    class AsyADL3FuncCtrlStsForBkpADMod:
        sig_name = "AsyADL3FuncCtrlStsForBkpADMod"
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
        sig_value_table = {'ADMod_NAD_Mod': 0, 'ADMod_MarsParking': 1, 'ADMod_ANP': 2, 'ADMod_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class AsyADL3FuncCtrlStsForBkpQf:
        sig_name = "AsyADL3FuncCtrlStsForBkpQf"
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
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class AsyADModeReqForBkpADActiveReq:
        sig_name = "AsyADModeReqForBkpADActiveReq"
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
        sig_value_table = {'ReqSts1_NotReqd': 0, 'ReqSts1_Reqd': 1}
        compute_method = None
        length = 1
        startbit = 11
        byte = 1
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class AsyADL3FuncCtrlStsForBkp_UB:
        sig_name = "AsyADL3FuncCtrlStsForBkp_UB"
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

    class AsyADL3FuncCtrlStsForBkpCtrlSts:
        sig_name = "AsyADL3FuncCtrlStsForBkpCtrlSts"
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
        sig_value_table = {'Primary': 0, 'Secondary': 1}
        compute_method = None
        length = 1
        startbit = 15
        byte = 1
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7


class Pscm2ADRedundancyCANNmFr:
    msg_name = "Pscm2ADRedundancyCANNmFr"
    msg_id = 1281
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "PSCM2"
    rx_nodes = ['BBM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class BbmAdRedundancyFr18:
    msg_name = "BbmAdRedundancyFr18"
    msg_id = 113
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "BBM"
    rx_nodes = ['CDC', 'ACU']
    sig_group_dict = {'WhlRotToothCntrForBkp': ['WhlRotToothCntrForBkpChks', 'WhlRotToothCntrForBkpCntr', 'WhlRotToothCntrForBkpWhlRotToothCntrFrntLe', 'WhlRotToothCntrForBkpWhlRotToothCntrFrntRi', 'WhlRotToothCntrForBkpWhlRotToothCntrReLe', 'WhlRotToothCntrForBkpWhlRotToothCntrReRi'], 'WhlDirRotlReForBkp': ['WhlDirRotlReForBkpChks', 'WhlDirRotlReForBkpCntr', 'WhlDirRotlReForBkpLe', 'WhlDirRotlReForBkpRi']}
    sig_group_dataid_dict = {'WhlDirRotlReForBkp': 6507}

    class WhlRotToothCntrForBkpChks:
        sig_name = "WhlRotToothCntrForBkpChks"
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

    class WhlDirRotlReForBkpChks:
        sig_name = "WhlDirRotlReForBkpChks"
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

    class WhlRotToothCntrForBkpWhlRotToothCntrReRi:
        sig_name = "WhlRotToothCntrForBkpWhlRotToothCntrReRi"
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

    class WhlRotToothCntrForBkpWhlRotToothCntrFrntLe:
        sig_name = "WhlRotToothCntrForBkpWhlRotToothCntrFrntLe"
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

    class WhlDirRotlReForBkpLe:
        sig_name = "WhlDirRotlReForBkpLe"
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
        sig_value_table = {'WhlRotlDirStd1_Undefd': 0, 'WhlRotlDirStd1_StandStill': 1, 'WhlRotlDirStd1_Fwd': 2, 'WhlRotlDirStd1_Backw': 3}
        compute_method = None
        length = 2
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class WhlRotToothCntrForBkpWhlRotToothCntrFrntRi:
        sig_name = "WhlRotToothCntrForBkpWhlRotToothCntrFrntRi"
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

    class WhlRotToothCntrForBkpCntr:
        sig_name = "WhlRotToothCntrForBkpCntr"
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

    class WhlRotToothCntrForBkp_UB:
        sig_name = "WhlRotToothCntrForBkp_UB"
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

    class WhlDirRotlReForBkpCntr:
        sig_name = "WhlDirRotlReForBkpCntr"
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

    class WhlRotToothCntrForBkpWhlRotToothCntrReLe:
        sig_name = "WhlRotToothCntrForBkpWhlRotToothCntrReLe"
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

    class WhlDirRotlReForBkp_UB:
        sig_name = "WhlDirRotlReForBkp_UB"
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

    class WhlDirRotlReForBkpRi:
        sig_name = "WhlDirRotlReForBkpRi"
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
        sig_value_table = {'WhlRotlDirStd1_Undefd': 0, 'WhlRotlDirStd1_StandStill': 1, 'WhlRotlDirStd1_Fwd': 2, 'WhlRotlDirStd1_Backw': 3}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


