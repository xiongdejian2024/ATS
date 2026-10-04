class CDSOCFSICDRadarCANFD1Fr05:
    msg_name = "CDSOCFSICDRadarCANFD1Fr05"
    msg_id = 768
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 32
    tx_node = "CDSOCFSI"
    rx_nodes = ['FSRR', 'FSRL']
    sig_group_dict = {'LoadPwrActSts': ['LoadPwrActStsACCMPwrActSts', 'LoadPwrActStsAFUPwrActSts', 'LoadPwrActStsAGMPwrActSts', 'LoadPwrActStsAGUPwrActSts', 'LoadPwrActStsALMLPwrActSts', 'LoadPwrActStsALMRPwrActSts', 'LoadPwrActStsAWMPwrActSts', 'LoadPwrActStsBCCPPwrActSts', 'LoadPwrActStsBCFVPwrActSts', 'LoadPwrActStsBCTVPwrActSts', 'LoadPwrActStsBEXVPwrActSts', 'LoadPwrActStsBNCMPwrActSts', 'LoadPwrActStsBoosterBlowerPwrActSts', 'LoadPwrActStsCCTVPwrActSts', 'LoadPwrActStsCDPwrActSts', 'LoadPwrActStsCERVPwrActSts', 'LoadPwrActStsCRCMPwrActSts', 'LoadPwrActStsCSOVPwrActSts', 'LoadPwrActStsDCTVPwrActSts', 'LoadPwrActStsDICPwrActSts', 'LoadPwrActStsDMFLPwrActSts', 'LoadPwrActStsDPODPwrActSts', 'LoadPwrActStsDRFPwrActSts', 'LoadPwrActStsDRMFRPwrActSts', 'LoadPwrActStsDRMRLPwrActSts', 'LoadPwrActStsDRMRRPwrActSts', 'LoadPwrActStsECTVPwrActSts', 'LoadPwrActStsEDCPPwrActSts', 'LoadPwrActStsEGSMPwrActSts', 'LoadPwrActStsEPMPwrActSts', 'LoadPwrActStsFCSIPwrActSts', 'LoadPwrActStsFEXVPwrActSts', 'LoadPwrActStsFLRPwrActSts', 'LoadPwrActStsFSRLPwrActSts', 'LoadPwrActStsFSRRPwrActSts', 'LoadPwrActStsHBMFPwrActSts', 'LoadPwrActStsHBMRPwrActSts', 'LoadPwrActStsHCCPPwrActSts', 'LoadPwrActStsHCMLPwrActSts', 'LoadPwrActStsHCMRPwrActSts', 'LoadPwrActStsHCTVPwrActSts', 'LoadPwrActStsHODPwrActSts', 'LoadPwrActStsHUBFPwrActSts', 'LoadPwrActStsHUBRPwrActSts', 'LoadPwrActStsHVAHPwrActSts', 'LoadPwrActStsHVCHPwrActSts', 'LoadPwrActStsHVCMPwrActSts', 'LoadPwrActStsIEMPwrActSts', 'LoadPwrActStsIRMMPwrActSts', 'LoadPwrActStsLCTVPwrActSts', 'LoadPwrActStsLPODPwrActSts', 'LoadPwrActStsMGMPwrActSts', 'LoadPwrActStsMMDPwrActSts', 'LoadPwrActStsMMPPwrActSts', 'LoadPwrActStsNKRPwrActSts', 'LoadPwrActStsOHCPwrActSts', 'LoadPwrActStsOPCFPwrActSts', 'LoadPwrActStsOPCRPwrActSts', 'LoadPwrActStsPMSIPwrActSts', 'LoadPwrActStsPOFPwrActSts', 'LoadPwrActStsPORPwrActSts', 'LoadPwrActStsPPODPwrActSts', 'LoadPwrActStsRCMLPwrActSts', 'LoadPwrActStsRCMRPwrActSts', 'LoadPwrActStsReserved1', 'LoadPwrActStsReserved10', 'LoadPwrActStsReserved11', 'LoadPwrActStsReserved12', 'LoadPwrActStsReserved13', 'LoadPwrActStsReserved14', 'LoadPwrActStsReserved15', 'LoadPwrActStsReserved16', 'LoadPwrActStsReserved17', 'LoadPwrActStsReserved18', 'LoadPwrActStsReserved2', 'LoadPwrActStsReserved3', 'LoadPwrActStsReserved4', 'LoadPwrActStsReserved5', 'LoadPwrActStsReserved6', 'LoadPwrActStsReserved7', 'LoadPwrActStsReserved8', 'LoadPwrActStsReserved9', 'LoadPwrActStsREXVPwrActSts', 'LoadPwrActStsRLMMPwrActSts', 'LoadPwrActStsRLSMPwrActSts', 'LoadPwrActStsRMLPwrActSts', 'LoadPwrActStsRPODPwrActSts', 'LoadPwrActStsRRMMPwrActSts', 'LoadPwrActStsRSOV1PwrActSts', 'LoadPwrActStsRSOV2PwrActSts', 'LoadPwrActStsSCMFPwrActSts', 'LoadPwrActStsSCMRPwrActSts', 'LoadPwrActStsSODLPwrActSts', 'LoadPwrActStsSODRPwrActSts', 'LoadPwrActStsSRSPwrActSts', 'LoadPwrActStsSWTLPwrActSts', 'LoadPwrActStsSWTRPwrActSts', 'LoadPwrActStsTERVPwrActSts', 'LoadPwrActStsUSBR1PwrActSts', 'LoadPwrActStsUSBR2PwrActSts', 'LoadPwrActStsUWBPwrActSts', 'LoadPwrActStsVCUPwrActSts', 'LoadPwrActStsWERVPwrActSts', 'LoadPwrActStsWPCPwrActSts'], 'VehDateAndTi': ['VehDateAndTiDay', 'VehDateAndTiHr', 'VehDateAndTiMins', 'VehDateAndTiMth', 'VehDateAndTiSec', 'VehDateAndTiValid', 'VehDateAndTiYr']}
    sig_group_dataid_dict = {}

    class LoadPwrActStsUWBPwrActSts:
        sig_name = "LoadPwrActStsUWBPwrActSts"
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

    class LoadPwrActStsReserved10:
        sig_name = "LoadPwrActStsReserved10"
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

    class LoadPwrActStsHBMFPwrActSts:
        sig_name = "LoadPwrActStsHBMFPwrActSts"
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

    class LoadPwrActStsREXVPwrActSts:
        sig_name = "LoadPwrActStsREXVPwrActSts"
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

    class VehDateAndTiValid:
        sig_name = "VehDateAndTiValid"
        sig_start_bit = 253
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
        startbit = 253
        byte = 31
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class LoadPwrActStsReserved5:
        sig_name = "LoadPwrActStsReserved5"
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

    class LoadPwrActStsWPCPwrActSts:
        sig_name = "LoadPwrActStsWPCPwrActSts"
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

    class LoadPwrActStsReserved6:
        sig_name = "LoadPwrActStsReserved6"
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

    class LoadPwrActStsReserved9:
        sig_name = "LoadPwrActStsReserved9"
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

    class LoadPwrActStsRRMMPwrActSts:
        sig_name = "LoadPwrActStsRRMMPwrActSts"
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

    class LoadPwrActStsDRMRRPwrActSts:
        sig_name = "LoadPwrActStsDRMRRPwrActSts"
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

    class VehDateAndTiDay:
        sig_name = "VehDateAndTiDay"
        sig_start_bit = 227
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
        startbit = 227
        bmuws_info = [(28, 0b00001111, 0b11110000, 4, 0), (29, 0b10000000, 0b01111111, 1, 7)]

    class LoadPwrActStsBoosterBlowerPwrActSts:
        sig_name = "LoadPwrActStsBoosterBlowerPwrActSts"
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

    class VehDateAndTiMth:
        sig_name = "VehDateAndTiMth"
        sig_start_bit = 231
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
        startbit = 231
        byte = 28
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class LoadPwrActStsNKRPwrActSts:
        sig_name = "LoadPwrActStsNKRPwrActSts"
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

    class LoadPwrActStsSCMFPwrActSts:
        sig_name = "LoadPwrActStsSCMFPwrActSts"
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

    class LoadPwrActStsIRMMPwrActSts:
        sig_name = "LoadPwrActStsIRMMPwrActSts"
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

    class VehDateAndTi_UB:
        sig_name = "VehDateAndTi_UB"
        sig_start_bit = 209
        update_id_bit = 209
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
        startbit = 209
        byte = 26
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class LoadPwrActStsReserved12:
        sig_name = "LoadPwrActStsReserved12"
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

    class LoadPwrActStsEGSMPwrActSts:
        sig_name = "LoadPwrActStsEGSMPwrActSts"
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

    class VehDateAndTiHr:
        sig_name = "VehDateAndTiHr"
        sig_start_bit = 238
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
        startbit = 238
        byte = 29
        mask = 0b01111100
        unmask = 0b10000011
        shift = 2

    class LoadPwrActStsSWTLPwrActSts:
        sig_name = "LoadPwrActStsSWTLPwrActSts"
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

    class LoadPwrActStsMMPPwrActSts:
        sig_name = "LoadPwrActStsMMPPwrActSts"
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

    class LoadPwrActStsDRMRLPwrActSts:
        sig_name = "LoadPwrActStsDRMRLPwrActSts"
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

    class LoadPwrActStsDRMFRPwrActSts:
        sig_name = "LoadPwrActStsDRMFRPwrActSts"
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

    class LoadPwrActStsReserved18:
        sig_name = "LoadPwrActStsReserved18"
        sig_start_bit = 211
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 211
        byte = 26
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class LoadPwrActStsFEXVPwrActSts:
        sig_name = "LoadPwrActStsFEXVPwrActSts"
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

    class LoadPwrActStsSODRPwrActSts:
        sig_name = "LoadPwrActStsSODRPwrActSts"
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

    class LoadPwrActStsFSRRPwrActSts:
        sig_name = "LoadPwrActStsFSRRPwrActSts"
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

    class LoadPwrActStsRSOV2PwrActSts:
        sig_name = "LoadPwrActStsRSOV2PwrActSts"
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

    class LoadPwrActStsReserved3:
        sig_name = "LoadPwrActStsReserved3"
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

    class LoadPwrActStsHCCPPwrActSts:
        sig_name = "LoadPwrActStsHCCPPwrActSts"
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

    class LoadPwrActStsDMFLPwrActSts:
        sig_name = "LoadPwrActStsDMFLPwrActSts"
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

    class LoadPwrActStsSWTRPwrActSts:
        sig_name = "LoadPwrActStsSWTRPwrActSts"
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

    class LoadPwrActStsReserved14:
        sig_name = "LoadPwrActStsReserved14"
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

    class VehDateAndTiSec:
        sig_name = "VehDateAndTiSec"
        sig_start_bit = 243
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
        startbit = 243
        bmuws_info = [(30, 0b00001111, 0b11110000, 4, 0), (31, 0b11000000, 0b00111111, 2, 6)]

    class LoadPwrActStsACCMPwrActSts:
        sig_name = "LoadPwrActStsACCMPwrActSts"
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

    class LoadPwrActStsRSOV1PwrActSts:
        sig_name = "LoadPwrActStsRSOV1PwrActSts"
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

    class LoadPwrActStsBCFVPwrActSts:
        sig_name = "LoadPwrActStsBCFVPwrActSts"
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

    class LoadPwrActStsDRFPwrActSts:
        sig_name = "LoadPwrActStsDRFPwrActSts"
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

    class LoadPwrActStsReserved7:
        sig_name = "LoadPwrActStsReserved7"
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

    class LoadPwrActStsReserved8:
        sig_name = "LoadPwrActStsReserved8"
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

    class LoadPwrActStsHCTVPwrActSts:
        sig_name = "LoadPwrActStsHCTVPwrActSts"
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

    class LoadPwrActStsBCCPPwrActSts:
        sig_name = "LoadPwrActStsBCCPPwrActSts"
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

    class LoadPwrActStsRLMMPwrActSts:
        sig_name = "LoadPwrActStsRLMMPwrActSts"
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

    class LoadPwrActStsPPODPwrActSts:
        sig_name = "LoadPwrActStsPPODPwrActSts"
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

    class LoadPwrActStsPOFPwrActSts:
        sig_name = "LoadPwrActStsPOFPwrActSts"
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

    class LoadPwrActStsCRCMPwrActSts:
        sig_name = "LoadPwrActStsCRCMPwrActSts"
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

    class LoadPwrActStsHUBRPwrActSts:
        sig_name = "LoadPwrActStsHUBRPwrActSts"
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

    class LoadPwrActStsLCTVPwrActSts:
        sig_name = "LoadPwrActStsLCTVPwrActSts"
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

    class LoadPwrActStsHCMRPwrActSts:
        sig_name = "LoadPwrActStsHCMRPwrActSts"
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

    class LoadPwrActStsDCTVPwrActSts:
        sig_name = "LoadPwrActStsDCTVPwrActSts"
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

    class LoadPwrActStsRPODPwrActSts:
        sig_name = "LoadPwrActStsRPODPwrActSts"
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

    class LoadPwrActStsTERVPwrActSts:
        sig_name = "LoadPwrActStsTERVPwrActSts"
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

    class LoadPwrActStsFSRLPwrActSts:
        sig_name = "LoadPwrActStsFSRLPwrActSts"
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

    class LoadPwrActStsReserved2:
        sig_name = "LoadPwrActStsReserved2"
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

    class LoadPwrActStsRCMRPwrActSts:
        sig_name = "LoadPwrActStsRCMRPwrActSts"
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

    class LoadPwrActStsCSOVPwrActSts:
        sig_name = "LoadPwrActStsCSOVPwrActSts"
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

    class LoadPwrActStsOPCRPwrActSts:
        sig_name = "LoadPwrActStsOPCRPwrActSts"
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

    class LoadPwrActStsHUBFPwrActSts:
        sig_name = "LoadPwrActStsHUBFPwrActSts"
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

    class LoadPwrActStsReserved15:
        sig_name = "LoadPwrActStsReserved15"
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

    class LoadPwrActStsHVCHPwrActSts:
        sig_name = "LoadPwrActStsHVCHPwrActSts"
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

    class LoadPwrActStsUSBR2PwrActSts:
        sig_name = "LoadPwrActStsUSBR2PwrActSts"
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

    class LoadPwrActStsLPODPwrActSts:
        sig_name = "LoadPwrActStsLPODPwrActSts"
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

    class LoadPwrActStsAFUPwrActSts:
        sig_name = "LoadPwrActStsAFUPwrActSts"
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

    class LoadPwrActStsFCSIPwrActSts:
        sig_name = "LoadPwrActStsFCSIPwrActSts"
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

    class LoadPwrActStsSRSPwrActSts:
        sig_name = "LoadPwrActStsSRSPwrActSts"
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

    class LoadPwrActStsIEMPwrActSts:
        sig_name = "LoadPwrActStsIEMPwrActSts"
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

    class LoadPwrActStsSCMRPwrActSts:
        sig_name = "LoadPwrActStsSCMRPwrActSts"
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

    class LoadPwrActStsReserved1:
        sig_name = "LoadPwrActStsReserved1"
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

    class LoadPwrActStsECTVPwrActSts:
        sig_name = "LoadPwrActStsECTVPwrActSts"
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

    class VehDateAndTiYr:
        sig_name = "VehDateAndTiYr"
        sig_start_bit = 223
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
        startbit = 223
        byte = 27
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class LoadPwrActStsHVAHPwrActSts:
        sig_name = "LoadPwrActStsHVAHPwrActSts"
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

    class LoadPwrActStsPORPwrActSts:
        sig_name = "LoadPwrActStsPORPwrActSts"
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

    class LoadPwrActStsReserved13:
        sig_name = "LoadPwrActStsReserved13"
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

    class LoadPwrActStsUSBR1PwrActSts:
        sig_name = "LoadPwrActStsUSBR1PwrActSts"
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

    class LoadPwrActStsBCTVPwrActSts:
        sig_name = "LoadPwrActStsBCTVPwrActSts"
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

    class LoadPwrActStsFLRPwrActSts:
        sig_name = "LoadPwrActStsFLRPwrActSts"
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

    class LoadPwrActStsBNCMPwrActSts:
        sig_name = "LoadPwrActStsBNCMPwrActSts"
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

    class LoadPwrActStsRLSMPwrActSts:
        sig_name = "LoadPwrActStsRLSMPwrActSts"
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

    class LoadPwrActStsAGMPwrActSts:
        sig_name = "LoadPwrActStsAGMPwrActSts"
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

    class LoadPwrActStsRMLPwrActSts:
        sig_name = "LoadPwrActStsRMLPwrActSts"
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

    class LoadPwrActStsALMLPwrActSts:
        sig_name = "LoadPwrActStsALMLPwrActSts"
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

    class LoadPwrActStsCDPwrActSts:
        sig_name = "LoadPwrActStsCDPwrActSts"
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

    class LoadPwrActStsCCTVPwrActSts:
        sig_name = "LoadPwrActStsCCTVPwrActSts"
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

    class LoadPwrActStsWERVPwrActSts:
        sig_name = "LoadPwrActStsWERVPwrActSts"
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

    class LoadPwrActStsOHCPwrActSts:
        sig_name = "LoadPwrActStsOHCPwrActSts"
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

    class LoadPwrActStsPMSIPwrActSts:
        sig_name = "LoadPwrActStsPMSIPwrActSts"
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

    class LoadPwrActStsReserved16:
        sig_name = "LoadPwrActStsReserved16"
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

    class LoadPwrActStsEDCPPwrActSts:
        sig_name = "LoadPwrActStsEDCPPwrActSts"
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

    class LoadPwrActStsMMDPwrActSts:
        sig_name = "LoadPwrActStsMMDPwrActSts"
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

    class LoadPwrActStsRCMLPwrActSts:
        sig_name = "LoadPwrActStsRCMLPwrActSts"
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

    class LoadPwrActStsVCUPwrActSts:
        sig_name = "LoadPwrActStsVCUPwrActSts"
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

    class VehDateAndTiMins:
        sig_name = "VehDateAndTiMins"
        sig_start_bit = 233
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
        startbit = 233
        bmuws_info = [(29, 0b00000011, 0b11111100, 2, 0), (30, 0b11110000, 0b00001111, 4, 4)]

    class LoadPwrActStsBEXVPwrActSts:
        sig_name = "LoadPwrActStsBEXVPwrActSts"
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

    class LoadPwrActStsReserved11:
        sig_name = "LoadPwrActStsReserved11"
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

    class LoadPwrActStsDPODPwrActSts:
        sig_name = "LoadPwrActStsDPODPwrActSts"
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

    class LoadPwrActStsReserved4:
        sig_name = "LoadPwrActStsReserved4"
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

    class LoadPwrActStsEPMPwrActSts:
        sig_name = "LoadPwrActStsEPMPwrActSts"
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

    class LoadPwrActStsHODPwrActSts:
        sig_name = "LoadPwrActStsHODPwrActSts"
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

    class LoadPwrActStsAWMPwrActSts:
        sig_name = "LoadPwrActStsAWMPwrActSts"
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

    class LoadPwrActStsMGMPwrActSts:
        sig_name = "LoadPwrActStsMGMPwrActSts"
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

    class LoadPwrActStsAGUPwrActSts:
        sig_name = "LoadPwrActStsAGUPwrActSts"
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

    class LoadPwrActStsOPCFPwrActSts:
        sig_name = "LoadPwrActStsOPCFPwrActSts"
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

    class LoadPwrActStsHVCMPwrActSts:
        sig_name = "LoadPwrActStsHVCMPwrActSts"
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

    class LoadPwrActStsALMRPwrActSts:
        sig_name = "LoadPwrActStsALMRPwrActSts"
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

    class LoadPwrActStsCERVPwrActSts:
        sig_name = "LoadPwrActStsCERVPwrActSts"
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

    class LoadPwrActStsReserved17:
        sig_name = "LoadPwrActStsReserved17"
        sig_start_bit = 213
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LVPowerSts_PowerOff': 0, 'LVPowerSts_PowerOn': 1, 'LVPowerSts_PowerGoingOff': 2, 'LVPowerSts_PowerFault': 3}
        compute_method = None
        length = 2
        startbit = 213
        byte = 26
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4


class CDSOCFSCDRadarCANFD1TimeSynchFr01:
    msg_name = "CDSOCFSCDRadarCANFD1TimeSynchFr01"
    msg_id = 1
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CDSOCFSI"
    rx_nodes = ['FSRR', 'FSRL']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class FSRRCDRadarCANFD1Fr03:
    msg_name = "FSRRCDRadarCANFD1Fr03"
    msg_id = 7
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 64
    tx_node = "FSRR"
    rx_nodes = ['CDSOCFSI']
    sig_group_dict = {'FrntSideRdrRiSts': ['FrntSideRdrRiStsChks', 'FrntSideRdrRiStsCntr', 'FrntSideRdrRiStsRdrStsCalibrationSts', 'FrntSideRdrRiStsRdrStsDetnValid', 'FrntSideRdrRiStsRdrStsDstbc', 'FrntSideRdrRiStsRdrStsEolHoriAg', 'FrntSideRdrRiStsRdrStsEolVerAg', 'FrntSideRdrRiStsRdrStsFailureHighTemp', 'FrntSideRdrRiStsRdrStsFailureNVM', 'FrntSideRdrRiStsRdrStsFailureTemperature', 'FrntSideRdrRiStsRdrStsFailureVoltage', 'FrntSideRdrRiStsRdrStsFaulty', 'FrntSideRdrRiStsRdrStsLastTimeLeap', 'FrntSideRdrRiStsRdrStsMaxTimeLeap', 'FrntSideRdrRiStsRdrStsMissCom', 'FrntSideRdrRiStsRdrStsOnlineHoriAg', 'FrntSideRdrRiStsRdrStsOnlineVerAg', 'FrntSideRdrRiStsRdrStsOperationMode']}
    sig_group_dataid_dict = {}

    class FrntSideRdrRiStsRdrStsFailureTemperature:
        sig_name = "FrntSideRdrRiStsRdrStsFailureTemperature"
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
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 49
        byte = 6
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class FrntSideRdrRiStsRdrStsOperationMode:
        sig_name = "FrntSideRdrRiStsRdrStsOperationMode"
        sig_start_bit = 68
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OperationMode_Reserved1': 0, 'OperationMode_Init': 1, 'OperationMode_Normal': 2, 'OperationMode_Degraded': 3, 'OperationMode_Blocked': 4}
        compute_method = None
        length = 3
        startbit = 68
        byte = 8
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class FrntSideRdrRiStsRdrStsEolHoriAg:
        sig_name = "FrntSideRdrRiStsRdrStsEolHoriAg"
        sig_start_bit = 63
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -10.0
        sig_value_min = 0
        sig_value_max = 2000
        sig_byteorder = "Motorola"
        sig_value_init = 1000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 63
        bmuws_info = [(7, 0b11111111, 0b00000000, 8, 0), (8, 0b11100000, 0b00011111, 3, 5)]

    class FrntSideRdrRiStsRdrStsDetnValid:
        sig_name = "FrntSideRdrRiStsRdrStsDetnValid"
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
        sig_value_table = {'Validity2_Valid': 0, 'Validity2_Invalid': 1}
        compute_method = None
        length = 1
        startbit = 16
        byte = 2
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FrntSideRdrRiStsRdrStsFailureHighTemp:
        sig_name = "FrntSideRdrRiStsRdrStsFailureHighTemp"
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
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 51
        byte = 6
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class FrntSideRdrRiStsRdrStsFailureNVM:
        sig_name = "FrntSideRdrRiStsRdrStsFailureNVM"
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
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 50
        byte = 6
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class FrntSideRdrRiStsRdrStsDstbc:
        sig_name = "FrntSideRdrRiStsRdrStsDstbc"
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
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class FrntSideRdrRiSts_UB:
        sig_name = "FrntSideRdrRiSts_UB"
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

    class FrntSideRdrRiStsRdrStsCalibrationSts:
        sig_name = "FrntSideRdrRiStsRdrStsCalibrationSts"
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
        sig_value_table = {'RdrStsCalibrationSts_Unknown': 0, 'RdrStsCalibrationSts_Calibrated': 1, 'RdrStsCalibrationSts_SensorMisalignmentDetected': 2, 'RdrStsCalibrationSts_CalibrationInProcess': 3, 'RdrStsCalibrationSts_NotCalibrated': 4, 'RdrStsCalibrationSts_Reserved1': 5, 'RdrStsCalibrationSts_Reserved2': 6, 'RdrStsCalibrationSts_Reserved3': 7}
        compute_method = None
        length = 3
        startbit = 19
        byte = 2
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class FrntSideRdrRiStsRdrStsEolVerAg:
        sig_name = "FrntSideRdrRiStsRdrStsEolVerAg"
        sig_start_bit = 65
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = -5.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 500
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 65
        bmuws_info = [(8, 0b00000011, 0b11111100, 2, 0), (9, 0b11111111, 0b00000000, 8, 0)]

    class FrntSideRdrRiStsRdrStsMaxTimeLeap:
        sig_name = "FrntSideRdrRiStsRdrStsMaxTimeLeap"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.0001
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11110000, 0b00001111, 4, 4)]

    class FrntSideRdrRiStsRdrStsFaulty:
        sig_name = "FrntSideRdrRiStsRdrStsFaulty"
        sig_start_bit = 93
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
        startbit = 93
        byte = 11
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class FrntSideRdrRiStsRdrStsLastTimeLeap:
        sig_name = "FrntSideRdrRiStsRdrStsLastTimeLeap"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.0001
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 15
        bmuws_info = [(1, 0b11111111, 0b00000000, 8, 0), (2, 0b11110000, 0b00001111, 4, 4)]

    class FrntSideRdrRiStsRdrStsOnlineHoriAg:
        sig_name = "FrntSideRdrRiStsRdrStsOnlineHoriAg"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -10.0
        sig_value_min = 0
        sig_value_max = 2000
        sig_byteorder = "Motorola"
        sig_value_init = 1000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11100000, 0b00011111, 3, 5)]

    class FrntSideRdrRiStsRdrStsFailureVoltage:
        sig_name = "FrntSideRdrRiStsRdrStsFailureVoltage"
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
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 48
        byte = 6
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FrntSideRdrRiStsCntr:
        sig_name = "FrntSideRdrRiStsCntr"
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

    class FrntSideRdrRiStsRdrStsOnlineVerAg:
        sig_name = "FrntSideRdrRiStsRdrStsOnlineVerAg"
        sig_start_bit = 87
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = -5.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 500
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 87
        bmuws_info = [(10, 0b11111111, 0b00000000, 8, 0), (11, 0b11000000, 0b00111111, 2, 6)]

    class FrntSideRdrRiStsRdrStsMissCom:
        sig_name = "FrntSideRdrRiStsRdrStsMissCom"
        sig_start_bit = 92
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
        startbit = 92
        byte = 11
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class FrntSideRdrRiStsChks:
        sig_name = "FrntSideRdrRiStsChks"
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


class CDSOCFSICDRadarCANFD1Fr06:
    msg_name = "CDSOCFSICDRadarCANFD1Fr06"
    msg_id = 769
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 64
    tx_node = "CDSOCFSI"
    rx_nodes = ['FSRR', 'FSRL']
    sig_group_dict = {'VehCfgDataGrp': ['VehCfgDataGrpVehCfgData1BlkIDBytePosn1', 'VehCfgDataGrpVehCfgData1BytePosn10', 'VehCfgDataGrpVehCfgData1BytePosn11', 'VehCfgDataGrpVehCfgData1BytePosn12', 'VehCfgDataGrpVehCfgData1BytePosn13', 'VehCfgDataGrpVehCfgData1BytePosn14', 'VehCfgDataGrpVehCfgData1BytePosn15', 'VehCfgDataGrpVehCfgData1BytePosn16', 'VehCfgDataGrpVehCfgData1BytePosn17', 'VehCfgDataGrpVehCfgData1BytePosn18', 'VehCfgDataGrpVehCfgData1BytePosn19', 'VehCfgDataGrpVehCfgData1BytePosn2', 'VehCfgDataGrpVehCfgData1BytePosn20', 'VehCfgDataGrpVehCfgData1BytePosn21', 'VehCfgDataGrpVehCfgData1BytePosn22', 'VehCfgDataGrpVehCfgData1BytePosn23', 'VehCfgDataGrpVehCfgData1BytePosn24', 'VehCfgDataGrpVehCfgData1BytePosn25', 'VehCfgDataGrpVehCfgData1BytePosn26', 'VehCfgDataGrpVehCfgData1BytePosn27', 'VehCfgDataGrpVehCfgData1BytePosn28', 'VehCfgDataGrpVehCfgData1BytePosn29', 'VehCfgDataGrpVehCfgData1BytePosn3', 'VehCfgDataGrpVehCfgData1BytePosn30', 'VehCfgDataGrpVehCfgData1BytePosn31', 'VehCfgDataGrpVehCfgData1BytePosn32', 'VehCfgDataGrpVehCfgData1BytePosn33', 'VehCfgDataGrpVehCfgData1BytePosn34', 'VehCfgDataGrpVehCfgData1BytePosn35', 'VehCfgDataGrpVehCfgData1BytePosn36', 'VehCfgDataGrpVehCfgData1BytePosn37', 'VehCfgDataGrpVehCfgData1BytePosn38', 'VehCfgDataGrpVehCfgData1BytePosn39', 'VehCfgDataGrpVehCfgData1BytePosn4', 'VehCfgDataGrpVehCfgData1BytePosn40', 'VehCfgDataGrpVehCfgData1BytePosn41', 'VehCfgDataGrpVehCfgData1BytePosn42', 'VehCfgDataGrpVehCfgData1BytePosn43', 'VehCfgDataGrpVehCfgData1BytePosn44', 'VehCfgDataGrpVehCfgData1BytePosn45', 'VehCfgDataGrpVehCfgData1BytePosn46', 'VehCfgDataGrpVehCfgData1BytePosn47', 'VehCfgDataGrpVehCfgData1BytePosn48', 'VehCfgDataGrpVehCfgData1BytePosn49', 'VehCfgDataGrpVehCfgData1BytePosn5', 'VehCfgDataGrpVehCfgData1BytePosn50', 'VehCfgDataGrpVehCfgData1BytePosn51', 'VehCfgDataGrpVehCfgData1BytePosn52', 'VehCfgDataGrpVehCfgData1BytePosn53', 'VehCfgDataGrpVehCfgData1BytePosn54', 'VehCfgDataGrpVehCfgData1BytePosn55', 'VehCfgDataGrpVehCfgData1BytePosn56', 'VehCfgDataGrpVehCfgData1BytePosn57', 'VehCfgDataGrpVehCfgData1BytePosn58', 'VehCfgDataGrpVehCfgData1BytePosn59', 'VehCfgDataGrpVehCfgData1BytePosn6', 'VehCfgDataGrpVehCfgData1BytePosn60', 'VehCfgDataGrpVehCfgData1BytePosn61', 'VehCfgDataGrpVehCfgData1BytePosn62', 'VehCfgDataGrpVehCfgData1BytePosn63', 'VehCfgDataGrpVehCfgData1BytePosn64', 'VehCfgDataGrpVehCfgData1BytePosn7', 'VehCfgDataGrpVehCfgData1BytePosn8', 'VehCfgDataGrpVehCfgData1BytePosn9']}
    sig_group_dataid_dict = {}

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


class CDSOCFSIToFSRRCDRadarCANFD1DiagReqFrame:
    msg_name = "CDSOCFSIToFSRRCDRadarCANFD1DiagReqFrame"
    msg_id = 1889
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "CDSOCFSI"
    rx_nodes = ['FSRR']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class FSRRCDRadarCANFD1NmFr:
    msg_name = "FSRRCDRadarCANFD1NmFr"
    msg_id = 1284
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "FSRR"
    rx_nodes = ['FSRL']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class FSRRCDRadarCANFD1Fr01:
    msg_name = "FSRRCDRadarCANFD1Fr01"
    msg_id = 260
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "FSRR"
    rx_nodes = ['CDSOCFSI']
    sig_group_dict = {'FrntSideRdrRiDent0': ['FrntSideRdrRiDent0RdrDetnChks', 'FrntSideRdrRiDent0RdrDetnCntr', 'FrntSideRdrRiDent0RdrDetnDynProp', 'FrntSideRdrRiDent0RdrDetnElevn', 'FrntSideRdrRiDent0RdrDetnID', 'FrntSideRdrRiDent0RdrDetnLocationValid', 'FrntSideRdrRiDent0RdrDetnPwr', 'FrntSideRdrRiDent0RdrDetnRng', 'FrntSideRdrRiDent0RdrDetnRngV', 'FrntSideRdrRiDent0RdrDetnSNR'], 'FrntSideRdrRiDent1': ['FrntSideRdrRiDent1RdrDetnChks', 'FrntSideRdrRiDent1RdrDetnCntr', 'FrntSideRdrRiDent1RdrDetnDynProp', 'FrntSideRdrRiDent1RdrDetnElevn', 'FrntSideRdrRiDent1RdrDetnID', 'FrntSideRdrRiDent1RdrDetnLocationValid', 'FrntSideRdrRiDent1RdrDetnPwr', 'FrntSideRdrRiDent1RdrDetnRng', 'FrntSideRdrRiDent1RdrDetnRngV', 'FrntSideRdrRiDent1RdrDetnSNR'], 'FrntSideRdrRiDent3': ['FrntSideRdrRiDent3RdrDetnChks', 'FrntSideRdrRiDent3RdrDetnCntr', 'FrntSideRdrRiDent3RdrDetnDynProp', 'FrntSideRdrRiDent3RdrDetnElevn', 'FrntSideRdrRiDent3RdrDetnID', 'FrntSideRdrRiDent3RdrDetnLocationValid', 'FrntSideRdrRiDent3RdrDetnPwr', 'FrntSideRdrRiDent3RdrDetnRng', 'FrntSideRdrRiDent3RdrDetnRngV', 'FrntSideRdrRiDent3RdrDetnSNR'], 'FrntSideRdrRiSync': ['FrntSideRdrRiSyncChks', 'FrntSideRdrRiSyncCntr', 'FrntSideRdrRiSyncRdrDetnTiStampNSec', 'FrntSideRdrRiSyncRdrDetnTiStampSec', 'FrntSideRdrRiSyncRdrNrDetn', 'FrntSideRdrRiSyncRdrObjLatency'], 'FrntSideRdrRiDent2': ['FrntSideRdrRiDent2RdrDetnChks', 'FrntSideRdrRiDent2RdrDetnCntr', 'FrntSideRdrRiDent2RdrDetnDynProp', 'FrntSideRdrRiDent2RdrDetnElevn', 'FrntSideRdrRiDent2RdrDetnID', 'FrntSideRdrRiDent2RdrDetnLocationValid', 'FrntSideRdrRiDent2RdrDetnPwr', 'FrntSideRdrRiDent2RdrDetnRng', 'FrntSideRdrRiDent2RdrDetnRngV', 'FrntSideRdrRiDent2RdrDetnSNR']}
    sig_group_dataid_dict = {'FrntSideRdrRiSync': 1034}

    class FrntSideRdrRiSyncCntr:
        sig_name = "FrntSideRdrRiSyncCntr"
        sig_start_bit = 367
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
        startbit = 367
        byte = 45
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class FrntSideRdrRiSyncRdrDetnTiStampSec:
        sig_name = "FrntSideRdrRiSyncRdrDetnTiStampSec"
        sig_start_bit = 319
        update_id_bit = None
        sig_length = 32
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4294967295
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 32
        startbit = 319
        bmuws_info = [(39, 0b11111111, 0b00000000, 8, 0), (40, 0b11111111, 0b00000000, 8, 0), (41, 0b11111111, 0b00000000, 8, 0), (42, 0b11111111, 0b00000000, 8, 0)]

    class FrntSideRdrRiDent1RdrDetnSNR:
        sig_name = "FrntSideRdrRiDent1RdrDetnSNR"
        sig_start_bit = 135
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 0.5
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 127
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 135
        byte = 16
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class FrntSideRdrRiDent3RdrDetnID:
        sig_name = "FrntSideRdrRiDent3RdrDetnID"
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

    class FrntSideRdrRiDent2RdrDetnRng:
        sig_name = "FrntSideRdrRiDent2RdrDetnRng"
        sig_start_bit = 167
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0.4
        sig_value_min = 0
        sig_value_max = 2996
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 167
        bmuws_info = [(20, 0b11111111, 0b00000000, 8, 0), (21, 0b11110000, 0b00001111, 4, 4)]

    class FrntSideRdrRiDent3RdrDetnSNR:
        sig_name = "FrntSideRdrRiDent3RdrDetnSNR"
        sig_start_bit = 271
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 0.5
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 127
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 271
        byte = 33
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class FrntSideRdrRiDent2RdrDetnLocationValid:
        sig_name = "FrntSideRdrRiDent2RdrDetnLocationValid"
        sig_start_bit = 207
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Validity2_Valid': 0, 'Validity2_Invalid': 1}
        compute_method = None
        length = 1
        startbit = 207
        byte = 25
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class FrntSideRdrRiSyncRdrNrDetn:
        sig_name = "FrntSideRdrRiSyncRdrNrDetn"
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

    class FrntSideRdrRiDent0RdrDetnRngV:
        sig_name = "FrntSideRdrRiDent0RdrDetnRngV"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -111.1
        sig_value_min = 0
        sig_value_max = 1667
        sig_byteorder = "Motorola"
        sig_value_init = 1111
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11100000, 0b00011111, 3, 5)]

    class FrntSideRdrRiDent3RdrDetnElevn:
        sig_name = "FrntSideRdrRiDent3RdrDetnElevn"
        sig_start_bit = 223
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.0039
        sig_value_offset = -0.5
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 128
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 223
        byte = 27
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntSideRdrRiDent3RdrDetnCntr:
        sig_name = "FrntSideRdrRiDent3RdrDetnCntr"
        sig_start_bit = 243
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
        startbit = 243
        byte = 30
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class FrntSideRdrRiDent0_UB:
        sig_name = "FrntSideRdrRiDent0_UB"
        sig_start_bit = 70
        update_id_bit = 70
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
        startbit = 70
        byte = 8
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class FrntSideRdrRiDent1_UB:
        sig_name = "FrntSideRdrRiDent1_UB"
        sig_start_bit = 69
        update_id_bit = 69
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
        startbit = 69
        byte = 8
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class FrntSideRdrRiDent1RdrDetnRngV:
        sig_name = "FrntSideRdrRiDent1RdrDetnRngV"
        sig_start_bit = 119
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -111.1
        sig_value_min = 0
        sig_value_max = 1667
        sig_byteorder = "Motorola"
        sig_value_init = 1111
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 119
        bmuws_info = [(14, 0b11111111, 0b00000000, 8, 0), (15, 0b11100000, 0b00011111, 3, 5)]

    class FrntSideRdrRiDent1RdrDetnDynProp:
        sig_name = "FrntSideRdrRiDent1RdrDetnDynProp"
        sig_start_bit = 128
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'RdrDetnDynProp_Stationary': 0, 'RdrDetnDynProp_Moving': 1}
        compute_method = None
        length = 1
        startbit = 128
        byte = 16
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FrntSideRdrRiDent0RdrDetnDynProp:
        sig_name = "FrntSideRdrRiDent0RdrDetnDynProp"
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
        sig_value_table = {'RdrDetnDynProp_Stationary': 0, 'RdrDetnDynProp_Moving': 1}
        compute_method = None
        length = 1
        startbit = 56
        byte = 7
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FrntSideRdrRiDent0RdrDetnCntr:
        sig_name = "FrntSideRdrRiDent0RdrDetnCntr"
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

    class FrntSideRdrRiDent2RdrDetnSNR:
        sig_name = "FrntSideRdrRiDent2RdrDetnSNR"
        sig_start_bit = 199
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 0.5
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 127
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 199
        byte = 24
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class FrntSideRdrRiDent0RdrDetnLocationValid:
        sig_name = "FrntSideRdrRiDent0RdrDetnLocationValid"
        sig_start_bit = 71
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Validity2_Valid': 0, 'Validity2_Invalid': 1}
        compute_method = None
        length = 1
        startbit = 71
        byte = 8
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class FrntSideRdrRiDent2RdrDetnDynProp:
        sig_name = "FrntSideRdrRiDent2RdrDetnDynProp"
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
        sig_value_table = {'RdrDetnDynProp_Stationary': 0, 'RdrDetnDynProp_Moving': 1}
        compute_method = None
        length = 1
        startbit = 192
        byte = 24
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FrntSideRdrRiDent0RdrDetnSNR:
        sig_name = "FrntSideRdrRiDent0RdrDetnSNR"
        sig_start_bit = 63
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 0.5
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 127
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 63
        byte = 7
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class FrntSideRdrRiDent2RdrDetnChks:
        sig_name = "FrntSideRdrRiDent2RdrDetnChks"
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

    class FrntSideRdrRiDent3_UB:
        sig_name = "FrntSideRdrRiDent3_UB"
        sig_start_bit = 67
        update_id_bit = 67
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
        startbit = 67
        byte = 8
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class FrntSideRdrRiDent1RdrDetnChks:
        sig_name = "FrntSideRdrRiDent1RdrDetnChks"
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

    class FrntSideRdrRiDent3RdrDetnPwr:
        sig_name = "FrntSideRdrRiDent3RdrDetnPwr"
        sig_start_bit = 260
        update_id_bit = None
        sig_length = 5
        sig_value_factor = 2
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Motorola"
        sig_value_init = 30
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 260
        byte = 32
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class FrntSideRdrRiDent1RdrDetnElevn:
        sig_name = "FrntSideRdrRiDent1RdrDetnElevn"
        sig_start_bit = 87
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.0039
        sig_value_offset = -0.5
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 128
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 87
        byte = 10
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntSideRdrRiDent2RdrDetnElevn:
        sig_name = "FrntSideRdrRiDent2RdrDetnElevn"
        sig_start_bit = 151
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.0039
        sig_value_offset = -0.5
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 128
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 151
        byte = 18
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntSideRdrRiDent2RdrDetnCntr:
        sig_name = "FrntSideRdrRiDent2RdrDetnCntr"
        sig_start_bit = 171
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
        startbit = 171
        byte = 21
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class FrntSideRdrRiDent3RdrDetnDynProp:
        sig_name = "FrntSideRdrRiDent3RdrDetnDynProp"
        sig_start_bit = 264
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'RdrDetnDynProp_Stationary': 0, 'RdrDetnDynProp_Moving': 1}
        compute_method = None
        length = 1
        startbit = 264
        byte = 33
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FrntSideRdrRiDent2RdrDetnID:
        sig_name = "FrntSideRdrRiDent2RdrDetnID"
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

    class FrntSideRdrRiDent3RdrDetnChks:
        sig_name = "FrntSideRdrRiDent3RdrDetnChks"
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

    class FrntSideRdrRiDent1RdrDetnRng:
        sig_name = "FrntSideRdrRiDent1RdrDetnRng"
        sig_start_bit = 103
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0.4
        sig_value_min = 0
        sig_value_max = 2996
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 103
        bmuws_info = [(12, 0b11111111, 0b00000000, 8, 0), (13, 0b11110000, 0b00001111, 4, 4)]

    class FrntSideRdrRiDent1RdrDetnID:
        sig_name = "FrntSideRdrRiDent1RdrDetnID"
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

    class FrntSideRdrRiDent1RdrDetnPwr:
        sig_name = "FrntSideRdrRiDent1RdrDetnPwr"
        sig_start_bit = 124
        update_id_bit = None
        sig_length = 5
        sig_value_factor = 2
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Motorola"
        sig_value_init = 30
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 124
        byte = 15
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class FrntSideRdrRiDent3RdrDetnRng:
        sig_name = "FrntSideRdrRiDent3RdrDetnRng"
        sig_start_bit = 239
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0.4
        sig_value_min = 0
        sig_value_max = 2996
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 239
        bmuws_info = [(29, 0b11111111, 0b00000000, 8, 0), (30, 0b11110000, 0b00001111, 4, 4)]

    class FrntSideRdrRiDent0RdrDetnRng:
        sig_name = "FrntSideRdrRiDent0RdrDetnRng"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0.4
        sig_value_min = 0
        sig_value_max = 2996
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11110000, 0b00001111, 4, 4)]

    class FrntSideRdrRiDent0RdrDetnPwr:
        sig_name = "FrntSideRdrRiDent0RdrDetnPwr"
        sig_start_bit = 52
        update_id_bit = None
        sig_length = 5
        sig_value_factor = 2
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Motorola"
        sig_value_init = 30
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 52
        byte = 6
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class FrntSideRdrRiDent1RdrDetnLocationValid:
        sig_name = "FrntSideRdrRiDent1RdrDetnLocationValid"
        sig_start_bit = 64
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Validity2_Valid': 0, 'Validity2_Invalid': 1}
        compute_method = None
        length = 1
        startbit = 64
        byte = 8
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FrntSideRdrRiDent0RdrDetnChks:
        sig_name = "FrntSideRdrRiDent0RdrDetnChks"
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

    class FrntSideRdrRiDent0RdrDetnElevn:
        sig_name = "FrntSideRdrRiDent0RdrDetnElevn"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.0039
        sig_value_offset = -0.5
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 128
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntSideRdrRiDent3RdrDetnRngV:
        sig_name = "FrntSideRdrRiDent3RdrDetnRngV"
        sig_start_bit = 255
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -111.1
        sig_value_min = 0
        sig_value_max = 1667
        sig_byteorder = "Motorola"
        sig_value_init = 1111
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 255
        bmuws_info = [(31, 0b11111111, 0b00000000, 8, 0), (32, 0b11100000, 0b00011111, 3, 5)]

    class FrntSideRdrRiDent1RdrDetnCntr:
        sig_name = "FrntSideRdrRiDent1RdrDetnCntr"
        sig_start_bit = 107
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
        startbit = 107
        byte = 13
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class FrntSideRdrRiSync_UB:
        sig_name = "FrntSideRdrRiSync_UB"
        sig_start_bit = 65
        update_id_bit = 65
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
        startbit = 65
        byte = 8
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class FrntSideRdrRiDent0RdrDetnID:
        sig_name = "FrntSideRdrRiDent0RdrDetnID"
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

    class FrntSideRdrRiDent2_UB:
        sig_name = "FrntSideRdrRiDent2_UB"
        sig_start_bit = 68
        update_id_bit = 68
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
        startbit = 68
        byte = 8
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class FrntSideRdrRiSyncRdrObjLatency:
        sig_name = "FrntSideRdrRiSyncRdrObjLatency"
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

    class FrntSideRdrRiDent2RdrDetnPwr:
        sig_name = "FrntSideRdrRiDent2RdrDetnPwr"
        sig_start_bit = 188
        update_id_bit = None
        sig_length = 5
        sig_value_factor = 2
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Motorola"
        sig_value_init = 30
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 188
        byte = 23
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class FrntSideRdrRiDent3RdrDetnLocationValid:
        sig_name = "FrntSideRdrRiDent3RdrDetnLocationValid"
        sig_start_bit = 200
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Validity2_Valid': 0, 'Validity2_Invalid': 1}
        compute_method = None
        length = 1
        startbit = 200
        byte = 25
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FrntSideRdrRiSyncChks:
        sig_name = "FrntSideRdrRiSyncChks"
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

    class FrntSideRdrRiSyncRdrDetnTiStampNSec:
        sig_name = "FrntSideRdrRiSyncRdrDetnTiStampNSec"
        sig_start_bit = 287
        update_id_bit = None
        sig_length = 32
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4294967295
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 32
        startbit = 287
        bmuws_info = [(35, 0b11111111, 0b00000000, 8, 0), (36, 0b11111111, 0b00000000, 8, 0), (37, 0b11111111, 0b00000000, 8, 0), (38, 0b11111111, 0b00000000, 8, 0)]

    class FrntSideRdrRiDent2RdrDetnRngV:
        sig_name = "FrntSideRdrRiDent2RdrDetnRngV"
        sig_start_bit = 183
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -111.1
        sig_value_min = 0
        sig_value_max = 1667
        sig_byteorder = "Motorola"
        sig_value_init = 1111
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 183
        bmuws_info = [(22, 0b11111111, 0b00000000, 8, 0), (23, 0b11100000, 0b00011111, 3, 5)]


class FSRLCDRadarCANFD1NmFr:
    msg_name = "FSRLCDRadarCANFD1NmFr"
    msg_id = 1283
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "FSRL"
    rx_nodes = ['CDSOCFSI']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class CDSOCFSIToAllCDRadarCANFD1DiagFuncReqFrame:
    msg_name = "CDSOCFSIToAllCDRadarCANFD1DiagFuncReqFrame"
    msg_id = 2047
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CDSOCFSI"
    rx_nodes = ['FSRR', 'FSRL']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class FSRLToCDSOCFSICDRadarCANFD1DiagRespFrame:
    msg_name = "FSRLToCDSOCFSICDRadarCANFD1DiagRespFrame"
    msg_id = 1632
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "FSRL"
    rx_nodes = ['CDSOCFSI']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class FSRRToCDSOCFSICDRadarCANFD1DiagRespFrame:
    msg_name = "FSRRToCDSOCFSICDRadarCANFD1DiagRespFrame"
    msg_id = 1633
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "FSRR"
    rx_nodes = ['CDSOCFSI']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class CDSOCFSICDRadarCANFD1Fr01:
    msg_name = "CDSOCFSICDRadarCANFD1Fr01"
    msg_id = 48
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 32
    tx_node = "CDSOCFSI"
    rx_nodes = ['FSRR', 'FSRL']
    sig_group_dict = {'SteerWhlSnsr': ['SteerWhlSnsrAg', 'SteerWhlSnsrAgSpd', 'SteerWhlSnsrChks', 'SteerWhlSnsrCntr', 'SteerWhlSnsrQf'], 'VMMGlbSig': ['VMMGlbSigCarModSts', 'VMMGlbSigChks', 'VMMGlbSigCntr', 'VMMGlbSigCnvincSubSts1', 'VMMGlbSigDrvgSubSts1', 'VMMGlbSigInactvSubSts1', 'VMMGlbSigLoBattModSts', 'VMMGlbSigUsgModSts'], 'SteerInfoRef': ['SteerInfoRefChks', 'SteerInfoRefCntr', 'SteerInfoRefSteerPinionAgSpdVal', 'SteerInfoRefSteerPinionAgSpdValQf', 'SteerInfoRefSteerPinionAgVal', 'SteerInfoRefSteerPinionAgValQf', 'SteerInfoRefSteerTorqueValQf', 'SteerInfoRefSteerWhlTqVal']}
    sig_group_dataid_dict = {'SteerWhlSnsr': 1056, 'VMMGlbSig': 1074, 'SteerInfoRef': 1037}

    class SteerWhlSnsrQf:
        sig_name = "SteerWhlSnsrQf"
        sig_start_bit = 89
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
        startbit = 89
        byte = 11
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class SteerWhlSnsr_UB:
        sig_name = "SteerWhlSnsr_UB"
        sig_start_bit = 104
        update_id_bit = 104
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
        startbit = 104
        byte = 13
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class SteerInfoRefSteerPinionAgSpdVal:
        sig_name = "SteerInfoRefSteerPinionAgSpdVal"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 14
        sig_value_factor = 0.0078125
        sig_value_offset = 0
        sig_value_min = -8192
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 14
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111100, 0b00000011, 6, 2)]

    class SteerWhlSnsrAg:
        sig_name = "SteerWhlSnsrAg"
        sig_start_bit = 103
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 0.000976563
        sig_value_offset = 0
        sig_value_min = -16384
        sig_value_max = 16383
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 103
        bmuws_info = [(12, 0b11111111, 0b00000000, 8, 0), (13, 0b11111110, 0b00000001, 7, 1)]

    class VMMGlbSigDrvgSubSts1:
        sig_name = "VMMGlbSigDrvgSubSts1"
        sig_start_bit = 151
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
        startbit = 151
        byte = 18
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SteerWhlSnsrChks:
        sig_name = "SteerWhlSnsrChks"
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

    class SteerWhlSnsrCntr:
        sig_name = "SteerWhlSnsrCntr"
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
        sig_start_bit = 135
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
        startbit = 135
        byte = 16
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class SteerInfoRefSteerTorqueValQf:
        sig_name = "SteerInfoRefSteerTorqueValQf"
        sig_start_bit = 41
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 2
        startbit = 41
        byte = 5
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class SteerInfoRefSteerWhlTqVal:
        sig_name = "SteerInfoRefSteerWhlTqVal"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 14
        sig_value_factor = 0.00390625
        sig_value_offset = 0
        sig_value_min = -8192
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 14
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111100, 0b00000011, 6, 2)]

    class VMMGlbSigUsgModSts:
        sig_name = "VMMGlbSigUsgModSts"
        sig_start_bit = 167
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
        startbit = 167
        byte = 20
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class VMMGlbSigLoBattModSts:
        sig_name = "VMMGlbSigLoBattModSts"
        sig_start_bit = 163
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
        startbit = 163
        byte = 20
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class SteerInfoRefChks:
        sig_name = "SteerInfoRefChks"
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

    class UsgModSts:
        sig_name = "UsgModSts"
        sig_start_bit = 119
        update_id_bit = 115
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
        startbit = 119
        byte = 14
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class SteerInfoRefSteerPinionAgValQf:
        sig_name = "SteerInfoRefSteerPinionAgValQf"
        sig_start_bit = 11
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 2
        startbit = 11
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class SteerInfoRefSteerPinionAgVal:
        sig_name = "SteerInfoRefSteerPinionAgVal"
        sig_start_bit = 55
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 0.000976563
        sig_value_offset = 0
        sig_value_min = -16384
        sig_value_max = 16383
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 55
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111110, 0b00000001, 7, 1)]

    class VMMGlbSigCarModSts:
        sig_name = "VMMGlbSigCarModSts"
        sig_start_bit = 131
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
        startbit = 131
        byte = 16
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class VMMGlbSigInactvSubSts1:
        sig_name = "VMMGlbSigInactvSubSts1"
        sig_start_bit = 159
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
        startbit = 159
        byte = 19
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SteerWhlSnsrAgSpd:
        sig_name = "SteerWhlSnsrAgSpd"
        sig_start_bit = 87
        update_id_bit = None
        sig_length = 14
        sig_value_factor = 0.0078125
        sig_value_offset = 0
        sig_value_min = -8192
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 14
        startbit = 87
        bmuws_info = [(10, 0b11111111, 0b00000000, 8, 0), (11, 0b11111100, 0b00000011, 6, 2)]

    class VMMGlbSigChks:
        sig_name = "VMMGlbSigChks"
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

    class SteerInfoRefCntr:
        sig_name = "SteerInfoRefCntr"
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

    class VMMGlbSig_UB:
        sig_name = "VMMGlbSig_UB"
        sig_start_bit = 114
        update_id_bit = 114
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
        startbit = 114
        byte = 14
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class SteerInfoRefSteerPinionAgSpdValQf:
        sig_name = "SteerInfoRefSteerPinionAgSpdValQf"
        sig_start_bit = 25
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 2
        startbit = 25
        byte = 3
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VMMGlbSigCnvincSubSts1:
        sig_name = "VMMGlbSigCnvincSubSts1"
        sig_start_bit = 143
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
        startbit = 143
        byte = 17
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SteerInfoRef_UB:
        sig_name = "SteerInfoRef_UB"
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


class FSRLCDRadarCANFD1Fr03:
    msg_name = "FSRLCDRadarCANFD1Fr03"
    msg_id = 259
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 64
    tx_node = "FSRL"
    rx_nodes = ['CDSOCFSI']
    sig_group_dict = {'FrntSideRdrLeSts': ['FrntSideRdrLeStsChks', 'FrntSideRdrLeStsCntr', 'FrntSideRdrLeStsRdrStsCalibrationSts', 'FrntSideRdrLeStsRdrStsDetnValid', 'FrntSideRdrLeStsRdrStsDstbc', 'FrntSideRdrLeStsRdrStsEolHoriAg', 'FrntSideRdrLeStsRdrStsEolVerAg', 'FrntSideRdrLeStsRdrStsFailureHighTemp', 'FrntSideRdrLeStsRdrStsFailureNVM', 'FrntSideRdrLeStsRdrStsFailureTemperature', 'FrntSideRdrLeStsRdrStsFailureVoltage', 'FrntSideRdrLeStsRdrStsFaulty', 'FrntSideRdrLeStsRdrStsLastTimeLeap', 'FrntSideRdrLeStsRdrStsMaxTimeLeap', 'FrntSideRdrLeStsRdrStsMissCom', 'FrntSideRdrLeStsRdrStsOnlineHoriAg', 'FrntSideRdrLeStsRdrStsOnlineVerAg', 'FrntSideRdrLeStsRdrStsOperationMode']}
    sig_group_dataid_dict = {}

    class FrntSideRdrLeStsRdrStsOnlineHoriAg:
        sig_name = "FrntSideRdrLeStsRdrStsOnlineHoriAg"
        sig_start_bit = 63
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -10.0
        sig_value_min = 0
        sig_value_max = 2000
        sig_byteorder = "Motorola"
        sig_value_init = 1000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 63
        bmuws_info = [(7, 0b11111111, 0b00000000, 8, 0), (8, 0b11100000, 0b00011111, 3, 5)]

    class FrntSideRdrLeStsRdrStsFailureTemperature:
        sig_name = "FrntSideRdrLeStsRdrStsFailureTemperature"
        sig_start_bit = 68
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 68
        byte = 8
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class FrntSideRdrLeStsRdrStsFailureHighTemp:
        sig_name = "FrntSideRdrLeStsRdrStsFailureHighTemp"
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
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 49
        byte = 6
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class FrntSideRdrLeSts_UB:
        sig_name = "FrntSideRdrLeSts_UB"
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

    class FrntSideRdrLeStsRdrStsLastTimeLeap:
        sig_name = "FrntSideRdrLeStsRdrStsLastTimeLeap"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.0001
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 15
        bmuws_info = [(1, 0b11111111, 0b00000000, 8, 0), (2, 0b11110000, 0b00001111, 4, 4)]

    class FrntSideRdrLeStsRdrStsMissCom:
        sig_name = "FrntSideRdrLeStsRdrStsMissCom"
        sig_start_bit = 92
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
        startbit = 92
        byte = 11
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class FrntSideRdrLeStsRdrStsFailureVoltage:
        sig_name = "FrntSideRdrLeStsRdrStsFailureVoltage"
        sig_start_bit = 67
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 67
        byte = 8
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class FrntSideRdrLeStsRdrStsOperationMode:
        sig_name = "FrntSideRdrLeStsRdrStsOperationMode"
        sig_start_bit = 52
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OperationMode_Reserved1': 0, 'OperationMode_Init': 1, 'OperationMode_Normal': 2, 'OperationMode_Degraded': 3, 'OperationMode_Blocked': 4}
        compute_method = None
        length = 3
        startbit = 52
        byte = 6
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class FrntSideRdrLeStsRdrStsFailureNVM:
        sig_name = "FrntSideRdrLeStsRdrStsFailureNVM"
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
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 48
        byte = 6
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FrntSideRdrLeStsRdrStsMaxTimeLeap:
        sig_name = "FrntSideRdrLeStsRdrStsMaxTimeLeap"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.0001
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11110000, 0b00001111, 4, 4)]

    class FrntSideRdrLeStsRdrStsDstbc:
        sig_name = "FrntSideRdrLeStsRdrStsDstbc"
        sig_start_bit = 93
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
        startbit = 93
        byte = 11
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class FrntSideRdrLeStsRdrStsCalibrationSts:
        sig_name = "FrntSideRdrLeStsRdrStsCalibrationSts"
        sig_start_bit = 35
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'RdrStsCalibrationSts_Unknown': 0, 'RdrStsCalibrationSts_Calibrated': 1, 'RdrStsCalibrationSts_SensorMisalignmentDetected': 2, 'RdrStsCalibrationSts_CalibrationInProcess': 3, 'RdrStsCalibrationSts_NotCalibrated': 4, 'RdrStsCalibrationSts_Reserved1': 5, 'RdrStsCalibrationSts_Reserved2': 6, 'RdrStsCalibrationSts_Reserved3': 7}
        compute_method = None
        length = 3
        startbit = 35
        byte = 4
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class FrntSideRdrLeStsRdrStsEolVerAg:
        sig_name = "FrntSideRdrLeStsRdrStsEolVerAg"
        sig_start_bit = 65
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = -5.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 500
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 65
        bmuws_info = [(8, 0b00000011, 0b11111100, 2, 0), (9, 0b11111111, 0b00000000, 8, 0)]

    class FrntSideRdrLeStsCntr:
        sig_name = "FrntSideRdrLeStsCntr"
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

    class FrntSideRdrLeStsRdrStsEolHoriAg:
        sig_name = "FrntSideRdrLeStsRdrStsEolHoriAg"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.01
        sig_value_offset = -10.0
        sig_value_min = 0
        sig_value_max = 2000
        sig_byteorder = "Motorola"
        sig_value_init = 1000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11100000, 0b00011111, 3, 5)]

    class FrntSideRdrLeStsRdrStsDetnValid:
        sig_name = "FrntSideRdrLeStsRdrStsDetnValid"
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
        sig_value_table = {'Validity2_Valid': 0, 'Validity2_Invalid': 1}
        compute_method = None
        length = 1
        startbit = 32
        byte = 4
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FrntSideRdrLeStsRdrStsOnlineVerAg:
        sig_name = "FrntSideRdrLeStsRdrStsOnlineVerAg"
        sig_start_bit = 87
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = -5.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 500
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 87
        bmuws_info = [(10, 0b11111111, 0b00000000, 8, 0), (11, 0b11000000, 0b00111111, 2, 6)]

    class FrntSideRdrLeStsRdrStsFaulty:
        sig_name = "FrntSideRdrLeStsRdrStsFaulty"
        sig_start_bit = 66
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
        startbit = 66
        byte = 8
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class FrntSideRdrLeStsChks:
        sig_name = "FrntSideRdrLeStsChks"
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


class FSRLCDRadarCANFD1Fr01:
    msg_name = "FSRLCDRadarCANFD1Fr01"
    msg_id = 257
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "FSRL"
    rx_nodes = ['CDSOCFSI']
    sig_group_dict = {'FrntSideRdrLeDent3': ['FrntSideRdrLeDent3RdrDetnChks', 'FrntSideRdrLeDent3RdrDetnCntr', 'FrntSideRdrLeDent3RdrDetnDynProp', 'FrntSideRdrLeDent3RdrDetnElevn', 'FrntSideRdrLeDent3RdrDetnID', 'FrntSideRdrLeDent3RdrDetnLocationValid', 'FrntSideRdrLeDent3RdrDetnPwr', 'FrntSideRdrLeDent3RdrDetnRng', 'FrntSideRdrLeDent3RdrDetnRngV', 'FrntSideRdrLeDent3RdrDetnSNR'], 'FrntSideRdrLeDent0': ['FrntSideRdrLeDent0RdrDetnChks', 'FrntSideRdrLeDent0RdrDetnCntr', 'FrntSideRdrLeDent0RdrDetnDynProp', 'FrntSideRdrLeDent0RdrDetnElevn', 'FrntSideRdrLeDent0RdrDetnID', 'FrntSideRdrLeDent0RdrDetnLocationValid', 'FrntSideRdrLeDent0RdrDetnPwr', 'FrntSideRdrLeDent0RdrDetnRng', 'FrntSideRdrLeDent0RdrDetnRngV', 'FrntSideRdrLeDent0RdrDetnSNR'], 'FrntSideRdrLeDent1': ['FrntSideRdrLeDent1RdrDetnChks', 'FrntSideRdrLeDent1RdrDetnCntr', 'FrntSideRdrLeDent1RdrDetnDynProp', 'FrntSideRdrLeDent1RdrDetnElevn', 'FrntSideRdrLeDent1RdrDetnID', 'FrntSideRdrLeDent1RdrDetnLocationValid', 'FrntSideRdrLeDent1RdrDetnPwr', 'FrntSideRdrLeDent1RdrDetnRng', 'FrntSideRdrLeDent1RdrDetnRngV', 'FrntSideRdrLeDent1RdrDetnSNR'], 'FrntSideRdrLeSync': ['FrntSideRdrLeSyncChks', 'FrntSideRdrLeSyncCntr', 'FrntSideRdrLeSyncRdrDetnTiStampNSec', 'FrntSideRdrLeSyncRdrDetnTiStampSec', 'FrntSideRdrLeSyncRdrNrDetn', 'FrntSideRdrLeSyncRdrObjLatency'], 'FrntSideRdrLeDent2': ['FrntSideRdrLeDent2RdrDetnChks', 'FrntSideRdrLeDent2RdrDetnCntr', 'FrntSideRdrLeDent2RdrDetnDynProp', 'FrntSideRdrLeDent2RdrDetnElevn', 'FrntSideRdrLeDent2RdrDetnID', 'FrntSideRdrLeDent2RdrDetnLocationValid', 'FrntSideRdrLeDent2RdrDetnPwr', 'FrntSideRdrLeDent2RdrDetnRng', 'FrntSideRdrLeDent2RdrDetnRngV', 'FrntSideRdrLeDent2RdrDetnSNR']}
    sig_group_dataid_dict = {'FrntSideRdrLeSync': 1033}

    class FrntSideRdrLeDent3RdrDetnLocationValid:
        sig_name = "FrntSideRdrLeDent3RdrDetnLocationValid"
        sig_start_bit = 200
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Validity2_Valid': 0, 'Validity2_Invalid': 1}
        compute_method = None
        length = 1
        startbit = 200
        byte = 25
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FrntSideRdrLeDent3RdrDetnElevn:
        sig_name = "FrntSideRdrLeDent3RdrDetnElevn"
        sig_start_bit = 223
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.0039
        sig_value_offset = -0.5
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 128
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 223
        byte = 27
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntSideRdrLeSyncRdrDetnTiStampSec:
        sig_name = "FrntSideRdrLeSyncRdrDetnTiStampSec"
        sig_start_bit = 335
        update_id_bit = None
        sig_length = 32
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4294967295
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 32
        startbit = 335
        bmuws_info = [(41, 0b11111111, 0b00000000, 8, 0), (42, 0b11111111, 0b00000000, 8, 0), (43, 0b11111111, 0b00000000, 8, 0), (44, 0b11111111, 0b00000000, 8, 0)]

    class FrntSideRdrLeDent1RdrDetnID:
        sig_name = "FrntSideRdrLeDent1RdrDetnID"
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

    class FrntSideRdrLeDent1RdrDetnCntr:
        sig_name = "FrntSideRdrLeDent1RdrDetnCntr"
        sig_start_bit = 107
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
        startbit = 107
        byte = 13
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class FrntSideRdrLeDent3RdrDetnRng:
        sig_name = "FrntSideRdrLeDent3RdrDetnRng"
        sig_start_bit = 239
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0.4
        sig_value_min = 0
        sig_value_max = 2996
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 239
        bmuws_info = [(29, 0b11111111, 0b00000000, 8, 0), (30, 0b11110000, 0b00001111, 4, 4)]

    class FrntSideRdrLeDent0RdrDetnLocationValid:
        sig_name = "FrntSideRdrLeDent0RdrDetnLocationValid"
        sig_start_bit = 71
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Validity2_Valid': 0, 'Validity2_Invalid': 1}
        compute_method = None
        length = 1
        startbit = 71
        byte = 8
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class FrntSideRdrLeDent2RdrDetnElevn:
        sig_name = "FrntSideRdrLeDent2RdrDetnElevn"
        sig_start_bit = 151
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.0039
        sig_value_offset = -0.5
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 128
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 151
        byte = 18
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntSideRdrLeDent0RdrDetnDynProp:
        sig_name = "FrntSideRdrLeDent0RdrDetnDynProp"
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
        sig_value_table = {'RdrDetnDynProp_Stationary': 0, 'RdrDetnDynProp_Moving': 1}
        compute_method = None
        length = 1
        startbit = 56
        byte = 7
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FrntSideRdrLeDent1RdrDetnDynProp:
        sig_name = "FrntSideRdrLeDent1RdrDetnDynProp"
        sig_start_bit = 128
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'RdrDetnDynProp_Stationary': 0, 'RdrDetnDynProp_Moving': 1}
        compute_method = None
        length = 1
        startbit = 128
        byte = 16
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FrntSideRdrLeDent2RdrDetnLocationValid:
        sig_name = "FrntSideRdrLeDent2RdrDetnLocationValid"
        sig_start_bit = 207
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Validity2_Valid': 0, 'Validity2_Invalid': 1}
        compute_method = None
        length = 1
        startbit = 207
        byte = 25
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class FrntSideRdrLeDent1RdrDetnElevn:
        sig_name = "FrntSideRdrLeDent1RdrDetnElevn"
        sig_start_bit = 87
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.0039
        sig_value_offset = -0.5
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 128
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 87
        byte = 10
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntSideRdrLeDent3RdrDetnRngV:
        sig_name = "FrntSideRdrLeDent3RdrDetnRngV"
        sig_start_bit = 255
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -111.1
        sig_value_min = 0
        sig_value_max = 1667
        sig_byteorder = "Motorola"
        sig_value_init = 1111
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 255
        bmuws_info = [(31, 0b11111111, 0b00000000, 8, 0), (32, 0b11100000, 0b00011111, 3, 5)]

    class FrntSideRdrLeSyncChks:
        sig_name = "FrntSideRdrLeSyncChks"
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

    class FrntSideRdrLeDent3RdrDetnChks:
        sig_name = "FrntSideRdrLeDent3RdrDetnChks"
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

    class FrntSideRdrLeDent3RdrDetnCntr:
        sig_name = "FrntSideRdrLeDent3RdrDetnCntr"
        sig_start_bit = 243
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
        startbit = 243
        byte = 30
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class FrntSideRdrLeDent0RdrDetnChks:
        sig_name = "FrntSideRdrLeDent0RdrDetnChks"
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

    class FrntSideRdrLeDent1RdrDetnChks:
        sig_name = "FrntSideRdrLeDent1RdrDetnChks"
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

    class FrntSideRdrLeDent0RdrDetnRngV:
        sig_name = "FrntSideRdrLeDent0RdrDetnRngV"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -111.1
        sig_value_min = 0
        sig_value_max = 1667
        sig_byteorder = "Motorola"
        sig_value_init = 1111
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11100000, 0b00011111, 3, 5)]

    class FrntSideRdrLeSyncRdrObjLatency:
        sig_name = "FrntSideRdrLeSyncRdrObjLatency"
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

    class FrntSideRdrLeDent0RdrDetnRng:
        sig_name = "FrntSideRdrLeDent0RdrDetnRng"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0.4
        sig_value_min = 0
        sig_value_max = 2996
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11110000, 0b00001111, 4, 4)]

    class FrntSideRdrLeDent3RdrDetnPwr:
        sig_name = "FrntSideRdrLeDent3RdrDetnPwr"
        sig_start_bit = 260
        update_id_bit = None
        sig_length = 5
        sig_value_factor = 2
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Motorola"
        sig_value_init = 30
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 260
        byte = 32
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class FrntSideRdrLeDent0RdrDetnSNR:
        sig_name = "FrntSideRdrLeDent0RdrDetnSNR"
        sig_start_bit = 63
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 0.5
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 127
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 63
        byte = 7
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class FrntSideRdrLeDent3RdrDetnDynProp:
        sig_name = "FrntSideRdrLeDent3RdrDetnDynProp"
        sig_start_bit = 264
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'RdrDetnDynProp_Stationary': 0, 'RdrDetnDynProp_Moving': 1}
        compute_method = None
        length = 1
        startbit = 264
        byte = 33
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FrntSideRdrLeDent1RdrDetnSNR:
        sig_name = "FrntSideRdrLeDent1RdrDetnSNR"
        sig_start_bit = 135
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 0.5
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 127
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 135
        byte = 16
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class FrntSideRdrLeDent3_UB:
        sig_name = "FrntSideRdrLeDent3_UB"
        sig_start_bit = 67
        update_id_bit = 67
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
        startbit = 67
        byte = 8
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class FrntSideRdrLeDent2RdrDetnChks:
        sig_name = "FrntSideRdrLeDent2RdrDetnChks"
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

    class FrntSideRdrLeDent3RdrDetnID:
        sig_name = "FrntSideRdrLeDent3RdrDetnID"
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

    class FrntSideRdrLeDent2RdrDetnID:
        sig_name = "FrntSideRdrLeDent2RdrDetnID"
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

    class FrntSideRdrLeDent3RdrDetnSNR:
        sig_name = "FrntSideRdrLeDent3RdrDetnSNR"
        sig_start_bit = 271
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 0.5
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 127
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 271
        byte = 33
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class FrntSideRdrLeDent2RdrDetnRng:
        sig_name = "FrntSideRdrLeDent2RdrDetnRng"
        sig_start_bit = 167
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0.4
        sig_value_min = 0
        sig_value_max = 2996
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 167
        bmuws_info = [(20, 0b11111111, 0b00000000, 8, 0), (21, 0b11110000, 0b00001111, 4, 4)]

    class FrntSideRdrLeDent0_UB:
        sig_name = "FrntSideRdrLeDent0_UB"
        sig_start_bit = 70
        update_id_bit = 70
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
        startbit = 70
        byte = 8
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class FrntSideRdrLeSyncCntr:
        sig_name = "FrntSideRdrLeSyncCntr"
        sig_start_bit = 367
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
        startbit = 367
        byte = 45
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class FrntSideRdrLeDent2RdrDetnPwr:
        sig_name = "FrntSideRdrLeDent2RdrDetnPwr"
        sig_start_bit = 188
        update_id_bit = None
        sig_length = 5
        sig_value_factor = 2
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Motorola"
        sig_value_init = 30
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 188
        byte = 23
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class FrntSideRdrLeDent0RdrDetnPwr:
        sig_name = "FrntSideRdrLeDent0RdrDetnPwr"
        sig_start_bit = 52
        update_id_bit = None
        sig_length = 5
        sig_value_factor = 2
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Motorola"
        sig_value_init = 30
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 52
        byte = 6
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class FrntSideRdrLeDent0RdrDetnID:
        sig_name = "FrntSideRdrLeDent0RdrDetnID"
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

    class FrntSideRdrLeDent1RdrDetnPwr:
        sig_name = "FrntSideRdrLeDent1RdrDetnPwr"
        sig_start_bit = 124
        update_id_bit = None
        sig_length = 5
        sig_value_factor = 2
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Motorola"
        sig_value_init = 30
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 124
        byte = 15
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class FrntSideRdrLeSyncRdrNrDetn:
        sig_name = "FrntSideRdrLeSyncRdrNrDetn"
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

    class FrntSideRdrLeDent0RdrDetnCntr:
        sig_name = "FrntSideRdrLeDent0RdrDetnCntr"
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

    class FrntSideRdrLeDent2RdrDetnSNR:
        sig_name = "FrntSideRdrLeDent2RdrDetnSNR"
        sig_start_bit = 199
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 0.5
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 127
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 199
        byte = 24
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class FrntSideRdrLeDent1RdrDetnRngV:
        sig_name = "FrntSideRdrLeDent1RdrDetnRngV"
        sig_start_bit = 119
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -111.1
        sig_value_min = 0
        sig_value_max = 1667
        sig_byteorder = "Motorola"
        sig_value_init = 1111
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 119
        bmuws_info = [(14, 0b11111111, 0b00000000, 8, 0), (15, 0b11100000, 0b00011111, 3, 5)]

    class FrntSideRdrLeDent1_UB:
        sig_name = "FrntSideRdrLeDent1_UB"
        sig_start_bit = 69
        update_id_bit = 69
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
        startbit = 69
        byte = 8
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class FrntSideRdrLeDent1RdrDetnRng:
        sig_name = "FrntSideRdrLeDent1RdrDetnRng"
        sig_start_bit = 103
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0.4
        sig_value_min = 0
        sig_value_max = 2996
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 103
        bmuws_info = [(12, 0b11111111, 0b00000000, 8, 0), (13, 0b11110000, 0b00001111, 4, 4)]

    class FrntSideRdrLeSync_UB:
        sig_name = "FrntSideRdrLeSync_UB"
        sig_start_bit = 65
        update_id_bit = 65
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
        startbit = 65
        byte = 8
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class FrntSideRdrLeDent0RdrDetnElevn:
        sig_name = "FrntSideRdrLeDent0RdrDetnElevn"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.0039
        sig_value_offset = -0.5
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 128
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntSideRdrLeDent1RdrDetnLocationValid:
        sig_name = "FrntSideRdrLeDent1RdrDetnLocationValid"
        sig_start_bit = 64
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Validity2_Valid': 0, 'Validity2_Invalid': 1}
        compute_method = None
        length = 1
        startbit = 64
        byte = 8
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FrntSideRdrLeDent2RdrDetnCntr:
        sig_name = "FrntSideRdrLeDent2RdrDetnCntr"
        sig_start_bit = 171
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
        startbit = 171
        byte = 21
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class FrntSideRdrLeDent2RdrDetnRngV:
        sig_name = "FrntSideRdrLeDent2RdrDetnRngV"
        sig_start_bit = 183
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -111.1
        sig_value_min = 0
        sig_value_max = 1667
        sig_byteorder = "Motorola"
        sig_value_init = 1111
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 183
        bmuws_info = [(22, 0b11111111, 0b00000000, 8, 0), (23, 0b11100000, 0b00011111, 3, 5)]

    class FrntSideRdrLeDent2_UB:
        sig_name = "FrntSideRdrLeDent2_UB"
        sig_start_bit = 68
        update_id_bit = 68
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
        startbit = 68
        byte = 8
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class FrntSideRdrLeSyncRdrDetnTiStampNSec:
        sig_name = "FrntSideRdrLeSyncRdrDetnTiStampNSec"
        sig_start_bit = 303
        update_id_bit = None
        sig_length = 32
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4294967295
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 32
        startbit = 303
        bmuws_info = [(37, 0b11111111, 0b00000000, 8, 0), (38, 0b11111111, 0b00000000, 8, 0), (39, 0b11111111, 0b00000000, 8, 0), (40, 0b11111111, 0b00000000, 8, 0)]

    class FrntSideRdrLeDent2RdrDetnDynProp:
        sig_name = "FrntSideRdrLeDent2RdrDetnDynProp"
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
        sig_value_table = {'RdrDetnDynProp_Stationary': 0, 'RdrDetnDynProp_Moving': 1}
        compute_method = None
        length = 1
        startbit = 192
        byte = 24
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0


class FSRRCDRadarCANFD1Fr02:
    msg_name = "FSRRCDRadarCANFD1Fr02"
    msg_id = 261
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "FSRR"
    rx_nodes = ['CDSOCFSI']
    sig_group_dict = {'FrntSideRdrRiDent4': ['FrntSideRdrRiDent4RdrDetnChks', 'FrntSideRdrRiDent4RdrDetnCntr', 'FrntSideRdrRiDent4RdrDetnDynProp', 'FrntSideRdrRiDent4RdrDetnElevn', 'FrntSideRdrRiDent4RdrDetnID', 'FrntSideRdrRiDent4RdrDetnLocationValid', 'FrntSideRdrRiDent4RdrDetnPwr', 'FrntSideRdrRiDent4RdrDetnRng', 'FrntSideRdrRiDent4RdrDetnRngV', 'FrntSideRdrRiDent4RdrDetnSNR'], 'FrntSideRdrRiDent6': ['FrntSideRdrRiDent6RdrDetnChks', 'FrntSideRdrRiDent6RdrDetnCntr', 'FrntSideRdrRiDent6RdrDetnDynProp', 'FrntSideRdrRiDent6RdrDetnElevn', 'FrntSideRdrRiDent6RdrDetnID', 'FrntSideRdrRiDent6RdrDetnLocationValid', 'FrntSideRdrRiDent6RdrDetnPwr', 'FrntSideRdrRiDent6RdrDetnRng', 'FrntSideRdrRiDent6RdrDetnRngV', 'FrntSideRdrRiDent6RdrDetnSNR'], 'FrntSideRdrRiDent5': ['FrntSideRdrRiDent5RdrDetnChks', 'FrntSideRdrRiDent5RdrDetnCntr', 'FrntSideRdrRiDent5RdrDetnDynProp', 'FrntSideRdrRiDent5RdrDetnElevn', 'FrntSideRdrRiDent5RdrDetnID', 'FrntSideRdrRiDent5RdrDetnLocationValid', 'FrntSideRdrRiDent5RdrDetnPwr', 'FrntSideRdrRiDent5RdrDetnRng', 'FrntSideRdrRiDent5RdrDetnRngV', 'FrntSideRdrRiDent5RdrDetnSNR'], 'FrntSideRdrRiDent9': ['FrntSideRdrRiDent9RdrDetnChks', 'FrntSideRdrRiDent9RdrDetnCntr', 'FrntSideRdrRiDent9RdrDetnDynProp', 'FrntSideRdrRiDent9RdrDetnElevn', 'FrntSideRdrRiDent9RdrDetnID', 'FrntSideRdrRiDent9RdrDetnLocationValid', 'FrntSideRdrRiDent9RdrDetnPwr', 'FrntSideRdrRiDent9RdrDetnRng', 'FrntSideRdrRiDent9RdrDetnRngV', 'FrntSideRdrRiDent9RdrDetnSNR'], 'FrntSideRdrRiDent10': ['FrntSideRdrRiDent10RdrDetnChks', 'FrntSideRdrRiDent10RdrDetnCntr', 'FrntSideRdrRiDent10RdrDetnDynProp', 'FrntSideRdrRiDent10RdrDetnElevn', 'FrntSideRdrRiDent10RdrDetnID', 'FrntSideRdrRiDent10RdrDetnLocationValid', 'FrntSideRdrRiDent10RdrDetnPwr', 'FrntSideRdrRiDent10RdrDetnRng', 'FrntSideRdrRiDent10RdrDetnRngV', 'FrntSideRdrRiDent10RdrDetnSNR'], 'FrntSideRdrRiDent8': ['FrntSideRdrRiDent8RdrDetnChks', 'FrntSideRdrRiDent8RdrDetnCntr', 'FrntSideRdrRiDent8RdrDetnDynProp', 'FrntSideRdrRiDent8RdrDetnElevn', 'FrntSideRdrRiDent8RdrDetnID', 'FrntSideRdrRiDent8RdrDetnLocationValid', 'FrntSideRdrRiDent8RdrDetnPwr', 'FrntSideRdrRiDent8RdrDetnRng', 'FrntSideRdrRiDent8RdrDetnRngV', 'FrntSideRdrRiDent8RdrDetnSNR'], 'FrntSideRdrRiDent7': ['FrntSideRdrRiDent7RdrDetnChks', 'FrntSideRdrRiDent7RdrDetnCntr', 'FrntSideRdrRiDent7RdrDetnDynProp', 'FrntSideRdrRiDent7RdrDetnElevn', 'FrntSideRdrRiDent7RdrDetnID', 'FrntSideRdrRiDent7RdrDetnLocationValid', 'FrntSideRdrRiDent7RdrDetnPwr', 'FrntSideRdrRiDent7RdrDetnRng', 'FrntSideRdrRiDent7RdrDetnRngV', 'FrntSideRdrRiDent7RdrDetnSNR']}
    sig_group_dataid_dict = {}

    class FrntSideRdrRiDent9RdrDetnRngV:
        sig_name = "FrntSideRdrRiDent9RdrDetnRngV"
        sig_start_bit = 455
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -111.1
        sig_value_min = 0
        sig_value_max = 1667
        sig_byteorder = "Motorola"
        sig_value_init = 1111
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 455
        bmuws_info = [(56, 0b11111111, 0b00000000, 8, 0), (57, 0b11100000, 0b00011111, 3, 5)]

    class FrntSideRdrRiDent6RdrDetnCntr:
        sig_name = "FrntSideRdrRiDent6RdrDetnCntr"
        sig_start_bit = 243
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
        startbit = 243
        byte = 30
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class FrntSideRdrRiDent4RdrDetnID:
        sig_name = "FrntSideRdrRiDent4RdrDetnID"
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

    class FrntSideRdrRiDent7RdrDetnCntr:
        sig_name = "FrntSideRdrRiDent7RdrDetnCntr"
        sig_start_bit = 307
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
        startbit = 307
        byte = 38
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class FrntSideRdrRiDent4RdrDetnLocationValid:
        sig_name = "FrntSideRdrRiDent4RdrDetnLocationValid"
        sig_start_bit = 64
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Validity2_Valid': 0, 'Validity2_Invalid': 1}
        compute_method = None
        length = 1
        startbit = 64
        byte = 8
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FrntSideRdrRiDent7RdrDetnPwr:
        sig_name = "FrntSideRdrRiDent7RdrDetnPwr"
        sig_start_bit = 324
        update_id_bit = None
        sig_length = 5
        sig_value_factor = 2
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Motorola"
        sig_value_init = 30
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 324
        byte = 40
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class FrntSideRdrRiDent7RdrDetnRngV:
        sig_name = "FrntSideRdrRiDent7RdrDetnRngV"
        sig_start_bit = 319
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -111.1
        sig_value_min = 0
        sig_value_max = 1667
        sig_byteorder = "Motorola"
        sig_value_init = 1111
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 319
        bmuws_info = [(39, 0b11111111, 0b00000000, 8, 0), (40, 0b11100000, 0b00011111, 3, 5)]

    class FrntSideRdrRiDent6RdrDetnID:
        sig_name = "FrntSideRdrRiDent6RdrDetnID"
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

    class FrntSideRdrRiDent4RdrDetnPwr:
        sig_name = "FrntSideRdrRiDent4RdrDetnPwr"
        sig_start_bit = 124
        update_id_bit = None
        sig_length = 5
        sig_value_factor = 2
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Motorola"
        sig_value_init = 30
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 124
        byte = 15
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class FrntSideRdrRiDent8RdrDetnLocationValid:
        sig_name = "FrntSideRdrRiDent8RdrDetnLocationValid"
        sig_start_bit = 336
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Validity2_Valid': 0, 'Validity2_Invalid': 1}
        compute_method = None
        length = 1
        startbit = 336
        byte = 42
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FrntSideRdrRiDent9RdrDetnID:
        sig_name = "FrntSideRdrRiDent9RdrDetnID"
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

    class FrntSideRdrRiDent8RdrDetnRng:
        sig_name = "FrntSideRdrRiDent8RdrDetnRng"
        sig_start_bit = 375
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0.4
        sig_value_min = 0
        sig_value_max = 2996
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 375
        bmuws_info = [(46, 0b11111111, 0b00000000, 8, 0), (47, 0b11110000, 0b00001111, 4, 4)]

    class FrntSideRdrRiDent4_UB:
        sig_name = "FrntSideRdrRiDent4_UB"
        sig_start_bit = 69
        update_id_bit = 69
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
        startbit = 69
        byte = 8
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class FrntSideRdrRiDent8RdrDetnSNR:
        sig_name = "FrntSideRdrRiDent8RdrDetnSNR"
        sig_start_bit = 407
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 0.5
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 127
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 407
        byte = 50
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class FrntSideRdrRiDent5RdrDetnRng:
        sig_name = "FrntSideRdrRiDent5RdrDetnRng"
        sig_start_bit = 167
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0.4
        sig_value_min = 0
        sig_value_max = 2996
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 167
        bmuws_info = [(20, 0b11111111, 0b00000000, 8, 0), (21, 0b11110000, 0b00001111, 4, 4)]

    class FrntSideRdrRiDent5RdrDetnLocationValid:
        sig_name = "FrntSideRdrRiDent5RdrDetnLocationValid"
        sig_start_bit = 207
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Validity2_Valid': 0, 'Validity2_Invalid': 1}
        compute_method = None
        length = 1
        startbit = 207
        byte = 25
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class FrntSideRdrRiDent8RdrDetnPwr:
        sig_name = "FrntSideRdrRiDent8RdrDetnPwr"
        sig_start_bit = 396
        update_id_bit = None
        sig_length = 5
        sig_value_factor = 2
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Motorola"
        sig_value_init = 30
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 396
        byte = 49
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class FrntSideRdrRiDent10RdrDetnRngV:
        sig_name = "FrntSideRdrRiDent10RdrDetnRngV"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -111.1
        sig_value_min = 0
        sig_value_max = 1667
        sig_byteorder = "Motorola"
        sig_value_init = 1111
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11100000, 0b00011111, 3, 5)]

    class FrntSideRdrRiDent5RdrDetnPwr:
        sig_name = "FrntSideRdrRiDent5RdrDetnPwr"
        sig_start_bit = 188
        update_id_bit = None
        sig_length = 5
        sig_value_factor = 2
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Motorola"
        sig_value_init = 30
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 188
        byte = 23
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class FrntSideRdrRiDent7RdrDetnRng:
        sig_name = "FrntSideRdrRiDent7RdrDetnRng"
        sig_start_bit = 303
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0.4
        sig_value_min = 0
        sig_value_max = 2996
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 303
        bmuws_info = [(37, 0b11111111, 0b00000000, 8, 0), (38, 0b11110000, 0b00001111, 4, 4)]

    class FrntSideRdrRiDent6RdrDetnChks:
        sig_name = "FrntSideRdrRiDent6RdrDetnChks"
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

    class FrntSideRdrRiDent6RdrDetnPwr:
        sig_name = "FrntSideRdrRiDent6RdrDetnPwr"
        sig_start_bit = 260
        update_id_bit = None
        sig_length = 5
        sig_value_factor = 2
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Motorola"
        sig_value_init = 30
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 260
        byte = 32
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class FrntSideRdrRiDent7RdrDetnSNR:
        sig_name = "FrntSideRdrRiDent7RdrDetnSNR"
        sig_start_bit = 335
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 0.5
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 127
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 335
        byte = 41
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class FrntSideRdrRiDent9RdrDetnLocationValid:
        sig_name = "FrntSideRdrRiDent9RdrDetnLocationValid"
        sig_start_bit = 479
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Validity2_Valid': 0, 'Validity2_Invalid': 1}
        compute_method = None
        length = 1
        startbit = 479
        byte = 59
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class FrntSideRdrRiDent10RdrDetnPwr:
        sig_name = "FrntSideRdrRiDent10RdrDetnPwr"
        sig_start_bit = 52
        update_id_bit = None
        sig_length = 5
        sig_value_factor = 2
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Motorola"
        sig_value_init = 30
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 52
        byte = 6
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class FrntSideRdrRiDent5RdrDetnCntr:
        sig_name = "FrntSideRdrRiDent5RdrDetnCntr"
        sig_start_bit = 171
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
        startbit = 171
        byte = 21
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class FrntSideRdrRiDent7RdrDetnElevn:
        sig_name = "FrntSideRdrRiDent7RdrDetnElevn"
        sig_start_bit = 287
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.0039
        sig_value_offset = -0.5
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 128
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 287
        byte = 35
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntSideRdrRiDent5RdrDetnElevn:
        sig_name = "FrntSideRdrRiDent5RdrDetnElevn"
        sig_start_bit = 151
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.0039
        sig_value_offset = -0.5
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 128
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 151
        byte = 18
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntSideRdrRiDent10RdrDetnChks:
        sig_name = "FrntSideRdrRiDent10RdrDetnChks"
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

    class FrntSideRdrRiDent7RdrDetnChks:
        sig_name = "FrntSideRdrRiDent7RdrDetnChks"
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

    class FrntSideRdrRiDent10RdrDetnSNR:
        sig_name = "FrntSideRdrRiDent10RdrDetnSNR"
        sig_start_bit = 63
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 0.5
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 127
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 63
        byte = 7
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class FrntSideRdrRiDent6RdrDetnLocationValid:
        sig_name = "FrntSideRdrRiDent6RdrDetnLocationValid"
        sig_start_bit = 200
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Validity2_Valid': 0, 'Validity2_Invalid': 1}
        compute_method = None
        length = 1
        startbit = 200
        byte = 25
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FrntSideRdrRiDent10RdrDetnCntr:
        sig_name = "FrntSideRdrRiDent10RdrDetnCntr"
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

    class FrntSideRdrRiDent8RdrDetnChks:
        sig_name = "FrntSideRdrRiDent8RdrDetnChks"
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

    class FrntSideRdrRiDent4RdrDetnElevn:
        sig_name = "FrntSideRdrRiDent4RdrDetnElevn"
        sig_start_bit = 87
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.0039
        sig_value_offset = -0.5
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 128
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 87
        byte = 10
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntSideRdrRiDent9RdrDetnRng:
        sig_name = "FrntSideRdrRiDent9RdrDetnRng"
        sig_start_bit = 439
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0.4
        sig_value_min = 0
        sig_value_max = 2996
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 439
        bmuws_info = [(54, 0b11111111, 0b00000000, 8, 0), (55, 0b11110000, 0b00001111, 4, 4)]

    class FrntSideRdrRiDent5RdrDetnDynProp:
        sig_name = "FrntSideRdrRiDent5RdrDetnDynProp"
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
        sig_value_table = {'RdrDetnDynProp_Stationary': 0, 'RdrDetnDynProp_Moving': 1}
        compute_method = None
        length = 1
        startbit = 192
        byte = 24
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FrntSideRdrRiDent6_UB:
        sig_name = "FrntSideRdrRiDent6_UB"
        sig_start_bit = 67
        update_id_bit = 67
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
        startbit = 67
        byte = 8
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class FrntSideRdrRiDent4RdrDetnRng:
        sig_name = "FrntSideRdrRiDent4RdrDetnRng"
        sig_start_bit = 103
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0.4
        sig_value_min = 0
        sig_value_max = 2996
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 103
        bmuws_info = [(12, 0b11111111, 0b00000000, 8, 0), (13, 0b11110000, 0b00001111, 4, 4)]

    class FrntSideRdrRiDent5_UB:
        sig_name = "FrntSideRdrRiDent5_UB"
        sig_start_bit = 68
        update_id_bit = 68
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
        startbit = 68
        byte = 8
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class FrntSideRdrRiDent8RdrDetnRngV:
        sig_name = "FrntSideRdrRiDent8RdrDetnRngV"
        sig_start_bit = 391
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -111.1
        sig_value_min = 0
        sig_value_max = 1667
        sig_byteorder = "Motorola"
        sig_value_init = 1111
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 391
        bmuws_info = [(48, 0b11111111, 0b00000000, 8, 0), (49, 0b11100000, 0b00011111, 3, 5)]

    class FrntSideRdrRiDent6RdrDetnDynProp:
        sig_name = "FrntSideRdrRiDent6RdrDetnDynProp"
        sig_start_bit = 264
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'RdrDetnDynProp_Stationary': 0, 'RdrDetnDynProp_Moving': 1}
        compute_method = None
        length = 1
        startbit = 264
        byte = 33
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FrntSideRdrRiDent8RdrDetnCntr:
        sig_name = "FrntSideRdrRiDent8RdrDetnCntr"
        sig_start_bit = 379
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
        startbit = 379
        byte = 47
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class FrntSideRdrRiDent10RdrDetnID:
        sig_name = "FrntSideRdrRiDent10RdrDetnID"
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

    class FrntSideRdrRiDent5RdrDetnRngV:
        sig_name = "FrntSideRdrRiDent5RdrDetnRngV"
        sig_start_bit = 183
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -111.1
        sig_value_min = 0
        sig_value_max = 1667
        sig_byteorder = "Motorola"
        sig_value_init = 1111
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 183
        bmuws_info = [(22, 0b11111111, 0b00000000, 8, 0), (23, 0b11100000, 0b00011111, 3, 5)]

    class FrntSideRdrRiDent9_UB:
        sig_name = "FrntSideRdrRiDent9_UB"
        sig_start_bit = 205
        update_id_bit = 205
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
        startbit = 205
        byte = 25
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class FrntSideRdrRiDent10_UB:
        sig_name = "FrntSideRdrRiDent10_UB"
        sig_start_bit = 70
        update_id_bit = 70
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
        startbit = 70
        byte = 8
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class FrntSideRdrRiDent8_UB:
        sig_name = "FrntSideRdrRiDent8_UB"
        sig_start_bit = 206
        update_id_bit = 206
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
        startbit = 206
        byte = 25
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class FrntSideRdrRiDent10RdrDetnRng:
        sig_name = "FrntSideRdrRiDent10RdrDetnRng"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0.4
        sig_value_min = 0
        sig_value_max = 2996
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11110000, 0b00001111, 4, 4)]

    class FrntSideRdrRiDent8RdrDetnElevn:
        sig_name = "FrntSideRdrRiDent8RdrDetnElevn"
        sig_start_bit = 359
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.0039
        sig_value_offset = -0.5
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 128
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 359
        byte = 44
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntSideRdrRiDent10RdrDetnDynProp:
        sig_name = "FrntSideRdrRiDent10RdrDetnDynProp"
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
        sig_value_table = {'RdrDetnDynProp_Stationary': 0, 'RdrDetnDynProp_Moving': 1}
        compute_method = None
        length = 1
        startbit = 56
        byte = 7
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FrntSideRdrRiDent5RdrDetnSNR:
        sig_name = "FrntSideRdrRiDent5RdrDetnSNR"
        sig_start_bit = 199
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 0.5
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 127
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 199
        byte = 24
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class FrntSideRdrRiDent9RdrDetnDynProp:
        sig_name = "FrntSideRdrRiDent9RdrDetnDynProp"
        sig_start_bit = 464
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'RdrDetnDynProp_Stationary': 0, 'RdrDetnDynProp_Moving': 1}
        compute_method = None
        length = 1
        startbit = 464
        byte = 58
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FrntSideRdrRiDent6RdrDetnSNR:
        sig_name = "FrntSideRdrRiDent6RdrDetnSNR"
        sig_start_bit = 271
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 0.5
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 127
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 271
        byte = 33
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class FrntSideRdrRiDent4RdrDetnDynProp:
        sig_name = "FrntSideRdrRiDent4RdrDetnDynProp"
        sig_start_bit = 128
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'RdrDetnDynProp_Stationary': 0, 'RdrDetnDynProp_Moving': 1}
        compute_method = None
        length = 1
        startbit = 128
        byte = 16
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FrntSideRdrRiDent4RdrDetnRngV:
        sig_name = "FrntSideRdrRiDent4RdrDetnRngV"
        sig_start_bit = 119
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -111.1
        sig_value_min = 0
        sig_value_max = 1667
        sig_byteorder = "Motorola"
        sig_value_init = 1111
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 119
        bmuws_info = [(14, 0b11111111, 0b00000000, 8, 0), (15, 0b11100000, 0b00011111, 3, 5)]

    class FrntSideRdrRiDent6RdrDetnRngV:
        sig_name = "FrntSideRdrRiDent6RdrDetnRngV"
        sig_start_bit = 255
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -111.1
        sig_value_min = 0
        sig_value_max = 1667
        sig_byteorder = "Motorola"
        sig_value_init = 1111
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 255
        bmuws_info = [(31, 0b11111111, 0b00000000, 8, 0), (32, 0b11100000, 0b00011111, 3, 5)]

    class FrntSideRdrRiDent10RdrDetnLocationValid:
        sig_name = "FrntSideRdrRiDent10RdrDetnLocationValid"
        sig_start_bit = 71
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Validity2_Valid': 0, 'Validity2_Invalid': 1}
        compute_method = None
        length = 1
        startbit = 71
        byte = 8
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class FrntSideRdrRiDent4RdrDetnChks:
        sig_name = "FrntSideRdrRiDent4RdrDetnChks"
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

    class FrntSideRdrRiDent9RdrDetnCntr:
        sig_name = "FrntSideRdrRiDent9RdrDetnCntr"
        sig_start_bit = 443
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
        startbit = 443
        byte = 55
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class FrntSideRdrRiDent7RdrDetnLocationValid:
        sig_name = "FrntSideRdrRiDent7RdrDetnLocationValid"
        sig_start_bit = 343
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Validity2_Valid': 0, 'Validity2_Invalid': 1}
        compute_method = None
        length = 1
        startbit = 343
        byte = 42
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class FrntSideRdrRiDent9RdrDetnSNR:
        sig_name = "FrntSideRdrRiDent9RdrDetnSNR"
        sig_start_bit = 471
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 0.5
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 127
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 471
        byte = 58
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class FrntSideRdrRiDent4RdrDetnCntr:
        sig_name = "FrntSideRdrRiDent4RdrDetnCntr"
        sig_start_bit = 107
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
        startbit = 107
        byte = 13
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class FrntSideRdrRiDent7_UB:
        sig_name = "FrntSideRdrRiDent7_UB"
        sig_start_bit = 66
        update_id_bit = 66
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
        startbit = 66
        byte = 8
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class FrntSideRdrRiDent9RdrDetnChks:
        sig_name = "FrntSideRdrRiDent9RdrDetnChks"
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

    class FrntSideRdrRiDent9RdrDetnPwr:
        sig_name = "FrntSideRdrRiDent9RdrDetnPwr"
        sig_start_bit = 460
        update_id_bit = None
        sig_length = 5
        sig_value_factor = 2
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Motorola"
        sig_value_init = 30
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 460
        byte = 57
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class FrntSideRdrRiDent8RdrDetnID:
        sig_name = "FrntSideRdrRiDent8RdrDetnID"
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

    class FrntSideRdrRiDent4RdrDetnSNR:
        sig_name = "FrntSideRdrRiDent4RdrDetnSNR"
        sig_start_bit = 135
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 0.5
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 127
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 135
        byte = 16
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class FrntSideRdrRiDent9RdrDetnElevn:
        sig_name = "FrntSideRdrRiDent9RdrDetnElevn"
        sig_start_bit = 423
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.0039
        sig_value_offset = -0.5
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 128
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 423
        byte = 52
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntSideRdrRiDent10RdrDetnElevn:
        sig_name = "FrntSideRdrRiDent10RdrDetnElevn"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.0039
        sig_value_offset = -0.5
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 128
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntSideRdrRiDent5RdrDetnChks:
        sig_name = "FrntSideRdrRiDent5RdrDetnChks"
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

    class FrntSideRdrRiDent6RdrDetnRng:
        sig_name = "FrntSideRdrRiDent6RdrDetnRng"
        sig_start_bit = 239
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0.4
        sig_value_min = 0
        sig_value_max = 2996
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 239
        bmuws_info = [(29, 0b11111111, 0b00000000, 8, 0), (30, 0b11110000, 0b00001111, 4, 4)]

    class FrntSideRdrRiDent8RdrDetnDynProp:
        sig_name = "FrntSideRdrRiDent8RdrDetnDynProp"
        sig_start_bit = 400
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'RdrDetnDynProp_Stationary': 0, 'RdrDetnDynProp_Moving': 1}
        compute_method = None
        length = 1
        startbit = 400
        byte = 50
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FrntSideRdrRiDent5RdrDetnID:
        sig_name = "FrntSideRdrRiDent5RdrDetnID"
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

    class FrntSideRdrRiDent7RdrDetnDynProp:
        sig_name = "FrntSideRdrRiDent7RdrDetnDynProp"
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
        sig_value_table = {'RdrDetnDynProp_Stationary': 0, 'RdrDetnDynProp_Moving': 1}
        compute_method = None
        length = 1
        startbit = 328
        byte = 41
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FrntSideRdrRiDent7RdrDetnID:
        sig_name = "FrntSideRdrRiDent7RdrDetnID"
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

    class FrntSideRdrRiDent6RdrDetnElevn:
        sig_name = "FrntSideRdrRiDent6RdrDetnElevn"
        sig_start_bit = 223
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.0039
        sig_value_offset = -0.5
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 128
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 223
        byte = 27
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class CDSOCFSICDRadarCANFD1Fr02:
    msg_name = "CDSOCFSICDRadarCANFD1Fr02"
    msg_id = 64
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "CDSOCFSI"
    rx_nodes = ['FSRR', 'FSRL']
    sig_group_dict = {'VehSpd': ['VehSpdChks', 'VehSpdCntr', 'VehSpdQf', 'VehSpdSpd']}
    sig_group_dataid_dict = {'VehSpd': 1043}

    class VehSpdSpd:
        sig_name = "VehSpdSpd"
        sig_start_bit = 9
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
        startbit = 9
        bmuws_info = [(1, 0b00000011, 0b11111100, 2, 0), (2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111000, 0b00000111, 5, 3)]

    class VehSpdChks:
        sig_name = "VehSpdChks"
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

    class VehSpd_UB:
        sig_name = "VehSpd_UB"
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

    class VehSpdCntr:
        sig_name = "VehSpdCntr"
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

    class VehSpdQf:
        sig_name = "VehSpdQf"
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


class CDSOCFSICDRadarCANFD1Fr04:
    msg_name = "CDSOCFSICDRadarCANFD1Fr04"
    msg_id = 512
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 16
    tx_node = "CDSOCFSI"
    rx_nodes = ['FSRR', 'FSRL']
    sig_group_dict = {'Odometer': ['OdometerValidity', 'OdometerValue']}
    sig_group_dataid_dict = {}

    class OdometerValidity:
        sig_name = "OdometerValidity"
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
        sig_value_table = {'Validity_NotValid': 0, 'Validity_Valid': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VehTiGlb:
        sig_name = "VehTiGlb"
        sig_start_bit = 39
        update_id_bit = 69
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
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class OdometerValue:
        sig_name = "OdometerValue"
        sig_start_bit = 6
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
        startbit = 6
        bmuws_info = [(0, 0b01111111, 0b10000000, 7, 0), (1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111100, 0b00000011, 6, 2)]

    class VehBattU:
        sig_name = "VehBattU"
        sig_start_bit = 17
        update_id_bit = 70
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
        startbit = 17
        bmuws_info = [(2, 0b00000011, 0b11111100, 2, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class Odometer_UB:
        sig_name = "Odometer_UB"
        sig_start_bit = 71
        update_id_bit = 71
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
        startbit = 71
        byte = 8
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7


class FSRLCDRadarCANFD1Fr02:
    msg_name = "FSRLCDRadarCANFD1Fr02"
    msg_id = 258
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "FSRL"
    rx_nodes = ['CDSOCFSI']
    sig_group_dict = {'FrntSideRdrLeDent8': ['FrntSideRdrLeDent8RdrDetnChks', 'FrntSideRdrLeDent8RdrDetnCntr', 'FrntSideRdrLeDent8RdrDetnDynProp', 'FrntSideRdrLeDent8RdrDetnElevn', 'FrntSideRdrLeDent8RdrDetnID', 'FrntSideRdrLeDent8RdrDetnLocationValid', 'FrntSideRdrLeDent8RdrDetnPwr', 'FrntSideRdrLeDent8RdrDetnRng', 'FrntSideRdrLeDent8RdrDetnRngV', 'FrntSideRdrLeDent8RdrDetnSNR'], 'FrntSideRdrLeDent10': ['FrntSideRdrLeDent10RdrDetnChks', 'FrntSideRdrLeDent10RdrDetnCntr', 'FrntSideRdrLeDent10RdrDetnDynProp', 'FrntSideRdrLeDent10RdrDetnElevn', 'FrntSideRdrLeDent10RdrDetnID', 'FrntSideRdrLeDent10RdrDetnLocationValid', 'FrntSideRdrLeDent10RdrDetnPwr', 'FrntSideRdrLeDent10RdrDetnRng', 'FrntSideRdrLeDent10RdrDetnRngV', 'FrntSideRdrLeDent10RdrDetnSNR'], 'FrntSideRdrLeDent5': ['FrntSideRdrLeDent5RdrDetnChks', 'FrntSideRdrLeDent5RdrDetnCntr', 'FrntSideRdrLeDent5RdrDetnDynProp', 'FrntSideRdrLeDent5RdrDetnElevn', 'FrntSideRdrLeDent5RdrDetnID', 'FrntSideRdrLeDent5RdrDetnLocationValid', 'FrntSideRdrLeDent5RdrDetnPwr', 'FrntSideRdrLeDent5RdrDetnRng', 'FrntSideRdrLeDent5RdrDetnRngV', 'FrntSideRdrLeDent5RdrDetnSNR'], 'FrntSideRdrLeDent4': ['FrntSideRdrLeDent4RdrDetnChks', 'FrntSideRdrLeDent4RdrDetnCntr', 'FrntSideRdrLeDent4RdrDetnDynProp', 'FrntSideRdrLeDent4RdrDetnElevn', 'FrntSideRdrLeDent4RdrDetnID', 'FrntSideRdrLeDent4RdrDetnLocationValid', 'FrntSideRdrLeDent4RdrDetnPwr', 'FrntSideRdrLeDent4RdrDetnRng', 'FrntSideRdrLeDent4RdrDetnRngV', 'FrntSideRdrLeDent4RdrDetnSNR'], 'FrntSideRdrLeDent7': ['FrntSideRdrLeDent7RdrDetnChks', 'FrntSideRdrLeDent7RdrDetnCntr', 'FrntSideRdrLeDent7RdrDetnDynProp', 'FrntSideRdrLeDent7RdrDetnElevn', 'FrntSideRdrLeDent7RdrDetnID', 'FrntSideRdrLeDent7RdrDetnLocationValid', 'FrntSideRdrLeDent7RdrDetnPwr', 'FrntSideRdrLeDent7RdrDetnRng', 'FrntSideRdrLeDent7RdrDetnRngV', 'FrntSideRdrLeDent7RdrDetnSNR'], 'FrntSideRdrLeDent6': ['FrntSideRdrLeDent6RdrDetnChks', 'FrntSideRdrLeDent6RdrDetnCntr', 'FrntSideRdrLeDent6RdrDetnDynProp', 'FrntSideRdrLeDent6RdrDetnElevn', 'FrntSideRdrLeDent6RdrDetnID', 'FrntSideRdrLeDent6RdrDetnLocationValid', 'FrntSideRdrLeDent6RdrDetnPwr', 'FrntSideRdrLeDent6RdrDetnRng', 'FrntSideRdrLeDent6RdrDetnRngV', 'FrntSideRdrLeDent6RdrDetnSNR'], 'FrntSideRdrLeDent9': ['FrntSideRdrLeDent9RdrDetnChks', 'FrntSideRdrLeDent9RdrDetnCntr', 'FrntSideRdrLeDent9RdrDetnDynProp', 'FrntSideRdrLeDent9RdrDetnElevn', 'FrntSideRdrLeDent9RdrDetnID', 'FrntSideRdrLeDent9RdrDetnLocationValid', 'FrntSideRdrLeDent9RdrDetnPwr', 'FrntSideRdrLeDent9RdrDetnRng', 'FrntSideRdrLeDent9RdrDetnRngV', 'FrntSideRdrLeDent9RdrDetnSNR']}
    sig_group_dataid_dict = {}

    class FrntSideRdrLeDent5RdrDetnChks:
        sig_name = "FrntSideRdrLeDent5RdrDetnChks"
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

    class FrntSideRdrLeDent6RdrDetnLocationValid:
        sig_name = "FrntSideRdrLeDent6RdrDetnLocationValid"
        sig_start_bit = 200
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Validity2_Valid': 0, 'Validity2_Invalid': 1}
        compute_method = None
        length = 1
        startbit = 200
        byte = 25
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FrntSideRdrLeDent8RdrDetnElevn:
        sig_name = "FrntSideRdrLeDent8RdrDetnElevn"
        sig_start_bit = 359
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.0039
        sig_value_offset = -0.5
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 128
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 359
        byte = 44
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntSideRdrLeDent8_UB:
        sig_name = "FrntSideRdrLeDent8_UB"
        sig_start_bit = 65
        update_id_bit = 65
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
        startbit = 65
        byte = 8
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class FrntSideRdrLeDent6RdrDetnChks:
        sig_name = "FrntSideRdrLeDent6RdrDetnChks"
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

    class FrntSideRdrLeDent4RdrDetnLocationValid:
        sig_name = "FrntSideRdrLeDent4RdrDetnLocationValid"
        sig_start_bit = 64
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Validity2_Valid': 0, 'Validity2_Invalid': 1}
        compute_method = None
        length = 1
        startbit = 64
        byte = 8
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FrntSideRdrLeDent7RdrDetnCntr:
        sig_name = "FrntSideRdrLeDent7RdrDetnCntr"
        sig_start_bit = 307
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
        startbit = 307
        byte = 38
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class FrntSideRdrLeDent10RdrDetnID:
        sig_name = "FrntSideRdrLeDent10RdrDetnID"
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

    class FrntSideRdrLeDent8RdrDetnSNR:
        sig_name = "FrntSideRdrLeDent8RdrDetnSNR"
        sig_start_bit = 407
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 0.5
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 127
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 407
        byte = 50
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class FrntSideRdrLeDent9RdrDetnCntr:
        sig_name = "FrntSideRdrLeDent9RdrDetnCntr"
        sig_start_bit = 443
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
        startbit = 443
        byte = 55
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class FrntSideRdrLeDent10_UB:
        sig_name = "FrntSideRdrLeDent10_UB"
        sig_start_bit = 70
        update_id_bit = 70
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
        startbit = 70
        byte = 8
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class FrntSideRdrLeDent4RdrDetnID:
        sig_name = "FrntSideRdrLeDent4RdrDetnID"
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

    class FrntSideRdrLeDent10RdrDetnChks:
        sig_name = "FrntSideRdrLeDent10RdrDetnChks"
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

    class FrntSideRdrLeDent4RdrDetnRng:
        sig_name = "FrntSideRdrLeDent4RdrDetnRng"
        sig_start_bit = 103
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0.4
        sig_value_min = 0
        sig_value_max = 2996
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 103
        bmuws_info = [(12, 0b11111111, 0b00000000, 8, 0), (13, 0b11110000, 0b00001111, 4, 4)]

    class FrntSideRdrLeDent10RdrDetnPwr:
        sig_name = "FrntSideRdrLeDent10RdrDetnPwr"
        sig_start_bit = 52
        update_id_bit = None
        sig_length = 5
        sig_value_factor = 2
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Motorola"
        sig_value_init = 30
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 52
        byte = 6
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class FrntSideRdrLeDent5RdrDetnRngV:
        sig_name = "FrntSideRdrLeDent5RdrDetnRngV"
        sig_start_bit = 183
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -111.1
        sig_value_min = 0
        sig_value_max = 1667
        sig_byteorder = "Motorola"
        sig_value_init = 1111
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 183
        bmuws_info = [(22, 0b11111111, 0b00000000, 8, 0), (23, 0b11100000, 0b00011111, 3, 5)]

    class FrntSideRdrLeDent5RdrDetnID:
        sig_name = "FrntSideRdrLeDent5RdrDetnID"
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

    class FrntSideRdrLeDent5_UB:
        sig_name = "FrntSideRdrLeDent5_UB"
        sig_start_bit = 68
        update_id_bit = 68
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
        startbit = 68
        byte = 8
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class FrntSideRdrLeDent5RdrDetnSNR:
        sig_name = "FrntSideRdrLeDent5RdrDetnSNR"
        sig_start_bit = 199
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 0.5
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 127
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 199
        byte = 24
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class FrntSideRdrLeDent9RdrDetnRngV:
        sig_name = "FrntSideRdrLeDent9RdrDetnRngV"
        sig_start_bit = 455
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -111.1
        sig_value_min = 0
        sig_value_max = 1667
        sig_byteorder = "Motorola"
        sig_value_init = 1111
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 455
        bmuws_info = [(56, 0b11111111, 0b00000000, 8, 0), (57, 0b11100000, 0b00011111, 3, 5)]

    class FrntSideRdrLeDent6RdrDetnID:
        sig_name = "FrntSideRdrLeDent6RdrDetnID"
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

    class FrntSideRdrLeDent9RdrDetnChks:
        sig_name = "FrntSideRdrLeDent9RdrDetnChks"
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

    class FrntSideRdrLeDent6RdrDetnPwr:
        sig_name = "FrntSideRdrLeDent6RdrDetnPwr"
        sig_start_bit = 260
        update_id_bit = None
        sig_length = 5
        sig_value_factor = 2
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Motorola"
        sig_value_init = 30
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 260
        byte = 32
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class FrntSideRdrLeDent10RdrDetnSNR:
        sig_name = "FrntSideRdrLeDent10RdrDetnSNR"
        sig_start_bit = 63
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 0.5
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 127
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 63
        byte = 7
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class FrntSideRdrLeDent4_UB:
        sig_name = "FrntSideRdrLeDent4_UB"
        sig_start_bit = 69
        update_id_bit = 69
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
        startbit = 69
        byte = 8
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class FrntSideRdrLeDent10RdrDetnLocationValid:
        sig_name = "FrntSideRdrLeDent10RdrDetnLocationValid"
        sig_start_bit = 71
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Validity2_Valid': 0, 'Validity2_Invalid': 1}
        compute_method = None
        length = 1
        startbit = 71
        byte = 8
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class FrntSideRdrLeDent4RdrDetnSNR:
        sig_name = "FrntSideRdrLeDent4RdrDetnSNR"
        sig_start_bit = 135
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 0.5
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 127
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 135
        byte = 16
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class FrntSideRdrLeDent6RdrDetnDynProp:
        sig_name = "FrntSideRdrLeDent6RdrDetnDynProp"
        sig_start_bit = 264
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'RdrDetnDynProp_Stationary': 0, 'RdrDetnDynProp_Moving': 1}
        compute_method = None
        length = 1
        startbit = 264
        byte = 33
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FrntSideRdrLeDent4RdrDetnPwr:
        sig_name = "FrntSideRdrLeDent4RdrDetnPwr"
        sig_start_bit = 124
        update_id_bit = None
        sig_length = 5
        sig_value_factor = 2
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Motorola"
        sig_value_init = 30
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 124
        byte = 15
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class FrntSideRdrLeDent10RdrDetnRngV:
        sig_name = "FrntSideRdrLeDent10RdrDetnRngV"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -111.1
        sig_value_min = 0
        sig_value_max = 1667
        sig_byteorder = "Motorola"
        sig_value_init = 1111
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11100000, 0b00011111, 3, 5)]

    class FrntSideRdrLeDent9RdrDetnSNR:
        sig_name = "FrntSideRdrLeDent9RdrDetnSNR"
        sig_start_bit = 471
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 0.5
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 127
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 471
        byte = 58
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class FrntSideRdrLeDent9RdrDetnLocationValid:
        sig_name = "FrntSideRdrLeDent9RdrDetnLocationValid"
        sig_start_bit = 479
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Validity2_Valid': 0, 'Validity2_Invalid': 1}
        compute_method = None
        length = 1
        startbit = 479
        byte = 59
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class FrntSideRdrLeDent7RdrDetnPwr:
        sig_name = "FrntSideRdrLeDent7RdrDetnPwr"
        sig_start_bit = 324
        update_id_bit = None
        sig_length = 5
        sig_value_factor = 2
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Motorola"
        sig_value_init = 30
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 324
        byte = 40
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class FrntSideRdrLeDent7RdrDetnRngV:
        sig_name = "FrntSideRdrLeDent7RdrDetnRngV"
        sig_start_bit = 319
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -111.1
        sig_value_min = 0
        sig_value_max = 1667
        sig_byteorder = "Motorola"
        sig_value_init = 1111
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 319
        bmuws_info = [(39, 0b11111111, 0b00000000, 8, 0), (40, 0b11100000, 0b00011111, 3, 5)]

    class FrntSideRdrLeDent8RdrDetnChks:
        sig_name = "FrntSideRdrLeDent8RdrDetnChks"
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

    class FrntSideRdrLeDent8RdrDetnLocationValid:
        sig_name = "FrntSideRdrLeDent8RdrDetnLocationValid"
        sig_start_bit = 336
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Validity2_Valid': 0, 'Validity2_Invalid': 1}
        compute_method = None
        length = 1
        startbit = 336
        byte = 42
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FrntSideRdrLeDent6RdrDetnCntr:
        sig_name = "FrntSideRdrLeDent6RdrDetnCntr"
        sig_start_bit = 243
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
        startbit = 243
        byte = 30
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class FrntSideRdrLeDent4RdrDetnElevn:
        sig_name = "FrntSideRdrLeDent4RdrDetnElevn"
        sig_start_bit = 87
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.0039
        sig_value_offset = -0.5
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 128
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 87
        byte = 10
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntSideRdrLeDent7_UB:
        sig_name = "FrntSideRdrLeDent7_UB"
        sig_start_bit = 66
        update_id_bit = 66
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
        startbit = 66
        byte = 8
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class FrntSideRdrLeDent9RdrDetnDynProp:
        sig_name = "FrntSideRdrLeDent9RdrDetnDynProp"
        sig_start_bit = 464
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'RdrDetnDynProp_Stationary': 0, 'RdrDetnDynProp_Moving': 1}
        compute_method = None
        length = 1
        startbit = 464
        byte = 58
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FrntSideRdrLeDent6_UB:
        sig_name = "FrntSideRdrLeDent6_UB"
        sig_start_bit = 67
        update_id_bit = 67
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
        startbit = 67
        byte = 8
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class FrntSideRdrLeDent8RdrDetnCntr:
        sig_name = "FrntSideRdrLeDent8RdrDetnCntr"
        sig_start_bit = 379
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
        startbit = 379
        byte = 47
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class FrntSideRdrLeDent9_UB:
        sig_name = "FrntSideRdrLeDent9_UB"
        sig_start_bit = 206
        update_id_bit = 206
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
        startbit = 206
        byte = 25
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class FrntSideRdrLeDent6RdrDetnElevn:
        sig_name = "FrntSideRdrLeDent6RdrDetnElevn"
        sig_start_bit = 223
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.0039
        sig_value_offset = -0.5
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 128
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 223
        byte = 27
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntSideRdrLeDent7RdrDetnSNR:
        sig_name = "FrntSideRdrLeDent7RdrDetnSNR"
        sig_start_bit = 335
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 0.5
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 127
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 335
        byte = 41
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class FrntSideRdrLeDent10RdrDetnElevn:
        sig_name = "FrntSideRdrLeDent10RdrDetnElevn"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.0039
        sig_value_offset = -0.5
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 128
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntSideRdrLeDent9RdrDetnRng:
        sig_name = "FrntSideRdrLeDent9RdrDetnRng"
        sig_start_bit = 439
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0.4
        sig_value_min = 0
        sig_value_max = 2996
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 439
        bmuws_info = [(54, 0b11111111, 0b00000000, 8, 0), (55, 0b11110000, 0b00001111, 4, 4)]

    class FrntSideRdrLeDent4RdrDetnRngV:
        sig_name = "FrntSideRdrLeDent4RdrDetnRngV"
        sig_start_bit = 119
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -111.1
        sig_value_min = 0
        sig_value_max = 1667
        sig_byteorder = "Motorola"
        sig_value_init = 1111
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 119
        bmuws_info = [(14, 0b11111111, 0b00000000, 8, 0), (15, 0b11100000, 0b00011111, 3, 5)]

    class FrntSideRdrLeDent6RdrDetnSNR:
        sig_name = "FrntSideRdrLeDent6RdrDetnSNR"
        sig_start_bit = 271
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 0.5
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 127
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 271
        byte = 33
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class FrntSideRdrLeDent8RdrDetnDynProp:
        sig_name = "FrntSideRdrLeDent8RdrDetnDynProp"
        sig_start_bit = 400
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'RdrDetnDynProp_Stationary': 0, 'RdrDetnDynProp_Moving': 1}
        compute_method = None
        length = 1
        startbit = 400
        byte = 50
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FrntSideRdrLeDent10RdrDetnCntr:
        sig_name = "FrntSideRdrLeDent10RdrDetnCntr"
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

    class FrntSideRdrLeDent8RdrDetnPwr:
        sig_name = "FrntSideRdrLeDent8RdrDetnPwr"
        sig_start_bit = 396
        update_id_bit = None
        sig_length = 5
        sig_value_factor = 2
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Motorola"
        sig_value_init = 30
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 396
        byte = 49
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class FrntSideRdrLeDent10RdrDetnRng:
        sig_name = "FrntSideRdrLeDent10RdrDetnRng"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0.4
        sig_value_min = 0
        sig_value_max = 2996
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11110000, 0b00001111, 4, 4)]

    class FrntSideRdrLeDent5RdrDetnDynProp:
        sig_name = "FrntSideRdrLeDent5RdrDetnDynProp"
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
        sig_value_table = {'RdrDetnDynProp_Stationary': 0, 'RdrDetnDynProp_Moving': 1}
        compute_method = None
        length = 1
        startbit = 192
        byte = 24
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FrntSideRdrLeDent5RdrDetnRng:
        sig_name = "FrntSideRdrLeDent5RdrDetnRng"
        sig_start_bit = 167
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0.4
        sig_value_min = 0
        sig_value_max = 2996
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 167
        bmuws_info = [(20, 0b11111111, 0b00000000, 8, 0), (21, 0b11110000, 0b00001111, 4, 4)]

    class FrntSideRdrLeDent9RdrDetnID:
        sig_name = "FrntSideRdrLeDent9RdrDetnID"
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

    class FrntSideRdrLeDent4RdrDetnCntr:
        sig_name = "FrntSideRdrLeDent4RdrDetnCntr"
        sig_start_bit = 107
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
        startbit = 107
        byte = 13
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class FrntSideRdrLeDent10RdrDetnDynProp:
        sig_name = "FrntSideRdrLeDent10RdrDetnDynProp"
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
        sig_value_table = {'RdrDetnDynProp_Stationary': 0, 'RdrDetnDynProp_Moving': 1}
        compute_method = None
        length = 1
        startbit = 56
        byte = 7
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FrntSideRdrLeDent7RdrDetnElevn:
        sig_name = "FrntSideRdrLeDent7RdrDetnElevn"
        sig_start_bit = 287
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.0039
        sig_value_offset = -0.5
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 128
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 287
        byte = 35
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntSideRdrLeDent4RdrDetnDynProp:
        sig_name = "FrntSideRdrLeDent4RdrDetnDynProp"
        sig_start_bit = 128
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'RdrDetnDynProp_Stationary': 0, 'RdrDetnDynProp_Moving': 1}
        compute_method = None
        length = 1
        startbit = 128
        byte = 16
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FrntSideRdrLeDent5RdrDetnLocationValid:
        sig_name = "FrntSideRdrLeDent5RdrDetnLocationValid"
        sig_start_bit = 207
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Validity2_Valid': 0, 'Validity2_Invalid': 1}
        compute_method = None
        length = 1
        startbit = 207
        byte = 25
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class FrntSideRdrLeDent7RdrDetnID:
        sig_name = "FrntSideRdrLeDent7RdrDetnID"
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

    class FrntSideRdrLeDent7RdrDetnChks:
        sig_name = "FrntSideRdrLeDent7RdrDetnChks"
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

    class FrntSideRdrLeDent6RdrDetnRng:
        sig_name = "FrntSideRdrLeDent6RdrDetnRng"
        sig_start_bit = 239
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0.4
        sig_value_min = 0
        sig_value_max = 2996
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 239
        bmuws_info = [(29, 0b11111111, 0b00000000, 8, 0), (30, 0b11110000, 0b00001111, 4, 4)]

    class FrntSideRdrLeDent7RdrDetnDynProp:
        sig_name = "FrntSideRdrLeDent7RdrDetnDynProp"
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
        sig_value_table = {'RdrDetnDynProp_Stationary': 0, 'RdrDetnDynProp_Moving': 1}
        compute_method = None
        length = 1
        startbit = 328
        byte = 41
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FrntSideRdrLeDent4RdrDetnChks:
        sig_name = "FrntSideRdrLeDent4RdrDetnChks"
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

    class FrntSideRdrLeDent5RdrDetnElevn:
        sig_name = "FrntSideRdrLeDent5RdrDetnElevn"
        sig_start_bit = 151
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.0039
        sig_value_offset = -0.5
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 128
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 151
        byte = 18
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntSideRdrLeDent9RdrDetnPwr:
        sig_name = "FrntSideRdrLeDent9RdrDetnPwr"
        sig_start_bit = 460
        update_id_bit = None
        sig_length = 5
        sig_value_factor = 2
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Motorola"
        sig_value_init = 30
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 460
        byte = 57
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class FrntSideRdrLeDent5RdrDetnCntr:
        sig_name = "FrntSideRdrLeDent5RdrDetnCntr"
        sig_start_bit = 171
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
        startbit = 171
        byte = 21
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class FrntSideRdrLeDent7RdrDetnRng:
        sig_name = "FrntSideRdrLeDent7RdrDetnRng"
        sig_start_bit = 303
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0.4
        sig_value_min = 0
        sig_value_max = 2996
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 303
        bmuws_info = [(37, 0b11111111, 0b00000000, 8, 0), (38, 0b11110000, 0b00001111, 4, 4)]

    class FrntSideRdrLeDent9RdrDetnElevn:
        sig_name = "FrntSideRdrLeDent9RdrDetnElevn"
        sig_start_bit = 423
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.0039
        sig_value_offset = -0.5
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 128
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 423
        byte = 52
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntSideRdrLeDent7RdrDetnLocationValid:
        sig_name = "FrntSideRdrLeDent7RdrDetnLocationValid"
        sig_start_bit = 343
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Validity2_Valid': 0, 'Validity2_Invalid': 1}
        compute_method = None
        length = 1
        startbit = 343
        byte = 42
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class FrntSideRdrLeDent5RdrDetnPwr:
        sig_name = "FrntSideRdrLeDent5RdrDetnPwr"
        sig_start_bit = 188
        update_id_bit = None
        sig_length = 5
        sig_value_factor = 2
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Motorola"
        sig_value_init = 30
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 188
        byte = 23
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class FrntSideRdrLeDent8RdrDetnRng:
        sig_name = "FrntSideRdrLeDent8RdrDetnRng"
        sig_start_bit = 375
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0.4
        sig_value_min = 0
        sig_value_max = 2996
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 375
        bmuws_info = [(46, 0b11111111, 0b00000000, 8, 0), (47, 0b11110000, 0b00001111, 4, 4)]

    class FrntSideRdrLeDent6RdrDetnRngV:
        sig_name = "FrntSideRdrLeDent6RdrDetnRngV"
        sig_start_bit = 255
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -111.1
        sig_value_min = 0
        sig_value_max = 1667
        sig_byteorder = "Motorola"
        sig_value_init = 1111
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 255
        bmuws_info = [(31, 0b11111111, 0b00000000, 8, 0), (32, 0b11100000, 0b00011111, 3, 5)]

    class FrntSideRdrLeDent8RdrDetnRngV:
        sig_name = "FrntSideRdrLeDent8RdrDetnRngV"
        sig_start_bit = 391
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -111.1
        sig_value_min = 0
        sig_value_max = 1667
        sig_byteorder = "Motorola"
        sig_value_init = 1111
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 391
        bmuws_info = [(48, 0b11111111, 0b00000000, 8, 0), (49, 0b11100000, 0b00011111, 3, 5)]

    class FrntSideRdrLeDent8RdrDetnID:
        sig_name = "FrntSideRdrLeDent8RdrDetnID"
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


class CDSOCFSICDRadarCANFD1NmFr:
    msg_name = "CDSOCFSICDRadarCANFD1NmFr"
    msg_id = 1282
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CDSOCFSI"
    rx_nodes = ['FSRR']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class CDSOCFSICDRadarCANFD1Fr03:
    msg_name = "CDSOCFSICDRadarCANFD1Fr03"
    msg_id = 256
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.04
    msg_length = 8
    tx_node = "CDSOCFSI"
    rx_nodes = ['FSRR', 'FSRL']
    sig_group_dict = {'AbsFctSts': ['AbsFctStsActv', 'AbsFctStsChks', 'AbsFctStsCntr', 'AbsFctStsEna', 'AbsFctStsSts2'], 'TcsSts': ['TcsStsActv', 'TcsStsChks', 'TcsStsCntr', 'TcsStsEna', 'TcsStsSts2']}
    sig_group_dataid_dict = {}

    class AbsFctStsChks:
        sig_name = "AbsFctStsChks"
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

    class TcsStsEna:
        sig_name = "TcsStsEna"
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
        sig_value_table = {'EnableDisable2_Disabled': 0, 'EnableDisable2_Enabled': 1}
        compute_method = None
        length = 1
        startbit = 35
        byte = 4
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class TcsStsSts2:
        sig_name = "TcsStsSts2"
        sig_start_bit = 34
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Sts2_Initial': 0, 'Sts2_Normal': 1, 'Sts2_Fault': 2, 'Sts2_Off': 3}
        compute_method = None
        length = 3
        startbit = 34
        byte = 4
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class TcsStsCntr:
        sig_name = "TcsStsCntr"
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

    class AbsFctSts_UB:
        sig_name = "AbsFctSts_UB"
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

    class AbsFctStsActv:
        sig_name = "AbsFctStsActv"
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
        sig_value_table = {'Actv_NoActv': 0, 'Actv_Actv': 1, 'Actv_Reserved1': 2, 'Actv_Reserved2': 3}
        compute_method = None
        length = 2
        startbit = 23
        byte = 2
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class AbsFctStsSts2:
        sig_name = "AbsFctStsSts2"
        sig_start_bit = 10
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Sts2_Initial': 0, 'Sts2_Normal': 1, 'Sts2_Fault': 2, 'Sts2_Off': 3}
        compute_method = None
        length = 3
        startbit = 10
        byte = 1
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class TcsStsChks:
        sig_name = "TcsStsChks"
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

    class AbsFctStsCntr:
        sig_name = "AbsFctStsCntr"
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

    class AbsFctStsEna:
        sig_name = "AbsFctStsEna"
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
        sig_value_table = {'EnableDisable2_Disabled': 0, 'EnableDisable2_Enabled': 1}
        compute_method = None
        length = 1
        startbit = 11
        byte = 1
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class TcsStsActv:
        sig_name = "TcsStsActv"
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
        sig_value_table = {'Actv_NoActv': 0, 'Actv_Actv': 1, 'Actv_Reserved1': 2, 'Actv_Reserved2': 3}
        compute_method = None
        length = 2
        startbit = 47
        byte = 5
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class TcsSts_UB:
        sig_name = "TcsSts_UB"
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


class CDSOCFSIToFSRLCDRadarCANFD1DiagReqFrame:
    msg_name = "CDSOCFSIToFSRLCDRadarCANFD1DiagReqFrame"
    msg_id = 1888
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "CDSOCFSI"
    rx_nodes = ['FSRL']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


